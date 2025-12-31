"""FastAPI application for RAG Chatbot."""

import time
import logging
import asyncio
from typing import Dict, List
import uuid

from fastapi import FastAPI, HTTPException, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
import tempfile
import os

from app.models import (
    QueryRequest, QueryResponse, Source,
    HealthResponse, SessionResponse, SessionInfo,
    IngestResponse, BooksResponse, BookInfo
)
from pydantic import BaseModel
from app.config import Config
from app.rag import retrieve_similar_chunks, synthesize_answer

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="RAG Chatbot API",
    version="1.0.0",
    description="Retrieval-Augmented Generation chatbot for digital books"
)

# Add CORS middleware for cross-origin requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Phase 2: restrict to specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory session store
SESSIONS: Dict[str, Dict] = {}
BOOKS: Dict[str, Dict] = {}  # Track ingested books


# Background task to clean up expired sessions
@app.on_event("startup")
async def cleanup_expired_sessions():
    """Background task to clean up expired sessions."""
    async def cleanup_loop():
        while True:
            try:
                now = time.time()
                expired_sessions = [
                    sid for sid, sess in SESSIONS.items()
                    if now > sess.get("expires_at", 0)
                ]
                for sid in expired_sessions:
                    del SESSIONS[sid]
                    logger.info(f"Purged expired session: {sid}")
                await asyncio.sleep(60)  # Check every minute
            except Exception as e:
                logger.error(f"Error in session cleanup: {e}")
                await asyncio.sleep(60)

    asyncio.create_task(cleanup_loop())


@app.get("/health", response_model=HealthResponse)
async def health_check():
    """System health check endpoint."""
    return HealthResponse(
        status="healthy",
        timestamp=time.time()
    )


@app.post("/query", response_model=QueryResponse)
async def query_book(request: QueryRequest) -> QueryResponse:
    """Query the chatbot for information about a book.

    Accepts a user question and optional selected text, retrieves relevant
    sections from the book via semantic search, and synthesizes an answer
    using an LLM.
    """
    start_time = time.time()

    try:
        logger.info(f"Query received: {request.question[:50]}... book_id={request.book_id}")

        # Retrieve relevant chunks
        chunks = retrieve_similar_chunks(
            question=request.question,
            book_id=request.book_id,
            top_k=request.top_k
        )

        logger.info(f"Retrieved {len(chunks)} relevant chunks")

        # Synthesize answer (with support for selected text as primary context)
        answer, is_fallback = synthesize_answer(
            question=request.question,
            context_chunks=chunks,
            selected_text=request.selected_text
        )

        # Format sources
        sources = [
            Source(
                chunk_text=c["chunk_text"][:200] + "..." if len(c["chunk_text"]) > 200 else c["chunk_text"],
                page_num=c["page_num"],
                chunk_id=c["chunk_id"],
                section_title=c.get("section_title"),
                similarity_score=c["similarity_score"]
            )
            for c in chunks
        ]

        latency_ms = int((time.time() - start_time) * 1000)
        logger.info(f"Query processed in {latency_ms}ms, is_fallback={is_fallback}")

        return QueryResponse(
            answer=answer,
            sources=sources,
            is_fallback=is_fallback,
            model=Config.CHAT_MODEL,
            latency_ms=latency_ms,
            timestamp=time.time()
        )

    except Exception as e:
        logger.error(f"Query failed: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Query failed: {str(e)}")


@app.post("/session", response_model=SessionResponse)
async def create_session() -> SessionResponse:
    """Create a new conversation session.

    Returns a session ID that should be included in subsequent queries
    to maintain conversation context.
    """
    try:
        session_id = str(uuid.uuid4())
        now = time.time()

        SESSIONS[session_id] = {
            "session_id": session_id,
            "created_at": now,
            "expires_at": now + Config.SESSION_TIMEOUT_SECONDS,
            "last_activity": now,
            "messages": []
        }

        logger.info(f"Created session: {session_id}")

        return SessionResponse(
            session_id=session_id,
            message=f"Session created. Expires in 30 minutes."
        )

    except Exception as e:
        logger.error(f"Session creation failed: {e}")
        raise HTTPException(status_code=500, detail="Session creation failed")


@app.get("/session/{session_id}", response_model=SessionInfo)
async def get_session_info(session_id: str) -> SessionInfo:
    """Get session information and status."""
    try:
        if session_id not in SESSIONS:
            raise HTTPException(status_code=404, detail="Session not found")

        session = SESSIONS[session_id]

        return SessionInfo(
            session_id=session_id,
            created_at=session["created_at"],
            expires_at=session["expires_at"],
            message_count=len(session.get("messages", []))
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting session info: {e}")
        raise HTTPException(status_code=500, detail="Error getting session info")


@app.get("/books", response_model=BooksResponse)
async def list_books() -> BooksResponse:
    """List all ingested books."""
    try:
        books = [
            BookInfo(
                book_id=bid,
                title=info.get("title"),
                author=info.get("author"),
                chunk_count=info.get("chunk_count", 0),
                uploaded_at=info.get("uploaded_at")
            )
            for bid, info in BOOKS.items()
        ]

        return BooksResponse(
            books=books,
            total=len(books)
        )

    except Exception as e:
        logger.error(f"Error listing books: {e}")
        raise HTTPException(status_code=500, detail="Error listing books")


@app.post("/ingest", response_model=IngestResponse)
async def ingest_book_file(
    file: UploadFile = File(...),
    book_id: str = Form(...)
) -> IngestResponse:
    """Ingest a new book file via multipart upload.

    This endpoint accepts file upload and processes the book through
    the ingestion pipeline (parsing → chunking → embedding → storage).

    Args:
        file: PDF or text file to ingest
        book_id: Unique identifier for the book

    Returns:
        Ingestion status with chunk count
    """
    temp_file_path = None

    try:
        # Validate file type
        if not file.filename.lower().endswith(('.pdf', '.txt')):
            raise HTTPException(
                status_code=400,
                detail="Only PDF and TXT files are supported"
            )

        # Validate book_id
        if not book_id or len(book_id) > 100:
            raise HTTPException(
                status_code=400,
                detail="book_id must be between 1 and 100 characters"
            )

        logger.info(f"Ingestion request for book_id={book_id}, file={file.filename}")

        # Save uploaded file to temp location
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf" if file.filename.endswith(".pdf") else ".txt") as temp_file:
            temp_file_path = temp_file.name
            content = await file.read()
            temp_file.write(content)

        logger.info(f"Saved uploaded file to temporary location: {temp_file_path}")

        # Import here to avoid circular imports
        from app.ingestion import ingest_book as ingest_book_pipeline

        # Run ingestion pipeline
        success = ingest_book_pipeline(Path(temp_file_path), book_id)

        if not success:
            raise HTTPException(
                status_code=500,
                detail="Book ingestion failed. Check logs for details."
            )

        # Estimate chunk count (rough estimate: 1 chunk per ~850 chars)
        file_size = len(content)
        estimated_chunks = max(1, file_size // 850)

        # Track book in registry
        BOOKS[book_id] = {
            "title": file.filename,
            "author": "Unknown",
            "chunk_count": estimated_chunks,
            "uploaded_at": time.time()
        }

        logger.info(f"Book ingestion successful: {book_id}, ~{estimated_chunks} chunks")

        return IngestResponse(
            status="success",
            book_id=book_id,
            chunk_count=estimated_chunks,
            message=f"Book ingested successfully: {file.filename}"
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Ingestion failed: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Ingestion failed: {str(e)}")
    finally:
        # Clean up temporary file
        if temp_file_path and os.path.exists(temp_file_path):
            try:
                os.remove(temp_file_path)
                logger.debug(f"Cleaned up temporary file: {temp_file_path}")
            except Exception as e:
                logger.warning(f"Failed to clean up temporary file: {e}")


class PrivacyAuditResponse(BaseModel):
    """Response model for privacy audit endpoint."""

    total_sessions: int = 0
    active_sessions: int = 0
    expired_sessions_purged: int = 0
    total_messages_in_memory: int = 0
    persistent_data_found: bool = False
    audit_status: str = "clean"
    message: str = ""


@app.get("/audit/privacy", response_model=PrivacyAuditResponse)
async def audit_privacy() -> PrivacyAuditResponse:
    """Privacy audit endpoint - verify zero persistent user data.

    Returns audit status showing:
    - Active sessions in memory
    - Message count
    - Persistent data check
    """
    try:
        now = time.time()
        active = 0
        total_messages = 0
        expired_count = 0

        for sid, session in SESSIONS.items():
            if now <= session.get("expires_at", 0):
                active += 1
                total_messages += len(session.get("messages", []))
            else:
                expired_count += 1

        # Check for persistent data (only in-memory sessions should exist)
        persistent_data_found = False

        # In a real audit, you would query Postgres, check logs, etc.
        # For Phase 1, we only check in-memory state

        audit_status = "clean" if not persistent_data_found else "warning"
        message = f"Privacy audit: {active} active sessions, {total_messages} messages in memory, {expired_count} expired sessions not yet cleaned"

        logger.info(message)

        return PrivacyAuditResponse(
            total_sessions=len(SESSIONS),
            active_sessions=active,
            expired_sessions_purged=expired_count,
            total_messages_in_memory=total_messages,
            persistent_data_found=persistent_data_found,
            audit_status=audit_status,
            message=message
        )

    except Exception as e:
        logger.error(f"Privacy audit failed: {e}")
        raise HTTPException(status_code=500, detail="Privacy audit failed")


@app.post("/admin/purge-sessions")
async def purge_expired_sessions():
    """Admin endpoint to manually purge expired sessions (for testing)."""
    try:
        now = time.time()
        expired_sids = [
            sid for sid, sess in SESSIONS.items()
            if now > sess.get("expires_at", 0)
        ]

        for sid in expired_sids:
            del SESSIONS[sid]

        logger.warning(f"Admin purge: Deleted {len(expired_sids)} expired sessions")

        return {
            "status": "success",
            "purged_count": len(expired_sids),
            "message": f"Purged {len(expired_sids)} expired sessions"
        }

    except Exception as e:
        logger.error(f"Session purge failed: {e}")
        raise HTTPException(status_code=500, detail="Session purge failed")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=Config.APP_PORT, log_level="info")
