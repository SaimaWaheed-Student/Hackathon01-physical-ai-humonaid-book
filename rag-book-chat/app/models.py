"""Pydantic models for request/response validation."""

from pydantic import BaseModel, Field
from typing import List, Optional


class QueryRequest(BaseModel):
    """Request model for query endpoint."""

    question: str = Field(..., min_length=1, max_length=500, description="User question")
    selected_text: Optional[str] = Field(None, max_length=5000, description="Optional selected text from user")
    book_id: str = Field("default", description="ID of the book to query")
    top_k: int = Field(5, ge=1, le=20, description="Number of top chunks to retrieve")
    session_id: Optional[str] = Field(None, description="Session ID for conversation context")


class Source(BaseModel):
    """Source model for citations in response."""

    chunk_text: str = Field(..., description="Truncated chunk text for display")
    page_num: int = Field(..., description="Page number of the source")
    chunk_id: int = Field(..., description="Chunk ID")
    section_title: Optional[str] = Field(None, description="Optional section/chapter title")
    similarity_score: float = Field(..., ge=0.0, le=1.0, description="Cosine similarity score")


class QueryResponse(BaseModel):
    """Response model for query endpoint."""

    answer: str = Field(..., description="Generated answer from RAG")
    sources: List[Source] = Field(default_factory=list, description="Source citations")
    is_fallback: bool = Field(False, description="Whether this is a fallback (general knowledge) answer")
    model: str = Field(..., description="LLM model used for synthesis")
    latency_ms: float = Field(..., description="Response latency in milliseconds")
    timestamp: float = Field(..., description="Response timestamp (Unix time)")


class HealthResponse(BaseModel):
    """Response model for health check endpoint."""

    status: str = Field(..., description="Health status (healthy/unhealthy)")
    timestamp: float = Field(..., description="Timestamp of health check")


class IngestRequest(BaseModel):
    """Request model for ingestion endpoint."""

    book_id: str = Field(..., min_length=1, max_length=100, description="Unique book identifier")
    # File upload handled by FastAPI's UploadFile


class IngestResponse(BaseModel):
    """Response model for ingestion endpoint."""

    status: str = Field(..., description="Ingestion status (success/error)")
    book_id: str = Field(..., description="Book ID")
    chunk_count: int = Field(..., description="Number of chunks created")
    message: str = Field(..., description="Status message")


class BookInfo(BaseModel):
    """Model for book metadata."""

    book_id: str = Field(..., description="Unique book identifier")
    title: Optional[str] = Field(None, description="Book title")
    author: Optional[str] = Field(None, description="Book author")
    chunk_count: int = Field(..., description="Number of chunks in book")
    uploaded_at: Optional[str] = Field(None, description="Upload timestamp")


class BooksResponse(BaseModel):
    """Response model for listing books."""

    books: List[BookInfo] = Field(default_factory=list, description="List of available books")
    total: int = Field(0, description="Total number of books")


class SessionInfo(BaseModel):
    """Model for session information."""

    session_id: str = Field(..., description="Unique session ID")
    created_at: float = Field(..., description="Session creation timestamp")
    expires_at: float = Field(..., description="Session expiration timestamp")
    message_count: int = Field(0, description="Number of messages in session")


class SessionResponse(BaseModel):
    """Response model for session creation/info endpoint."""

    session_id: str = Field(..., description="Unique session ID")
    message: str = Field(..., description="Status message")
