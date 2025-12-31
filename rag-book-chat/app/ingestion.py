"""Book ingestion pipeline for RAG Chatbot."""

import logging
from pathlib import Path
from typing import List, Dict
import requests

from pypdf import PdfReader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct

from app.config import Config

logger = logging.getLogger(__name__)


def load_pdf(file_path: Path) -> str:
    """Load PDF and extract text.

    Args:
        file_path: Path to PDF file

    Returns:
        Extracted text from PDF
    """
    if not file_path.exists():
        raise FileNotFoundError(f"PDF not found: {file_path}")

    logger.info(f"Loading PDF: {file_path}")

    reader = PdfReader(file_path)
    text = ""

    for page_num, page in enumerate(reader.pages, 1):
        text += f"\n[Page {page_num}]\n"
        try:
            text += page.extract_text()
        except Exception as e:
            logger.warning(f"Failed to extract text from page {page_num}: {e}")

    logger.info(f"Extracted {len(text)} characters from {len(reader.pages)} pages")
    return text


def load_txt(file_path: Path) -> str:
    """Load TXT file and extract text.

    Args:
        file_path: Path to TXT file

    Returns:
        Extracted text from TXT
    """
    if not file_path.exists():
        raise FileNotFoundError(f"TXT not found: {file_path}")

    logger.info(f"Loading TXT: {file_path}")

    with open(file_path, 'r', encoding='utf-8') as f:
        text = f.read()

    logger.info(f"Extracted {len(text)} characters")
    return text


def chunk_text(
    text: str,
    chunk_size: int = 850,
    chunk_overlap: int = 180
) -> List[Dict]:
    """Split text into semantic chunks.

    Uses LangChain's RecursiveCharacterTextSplitter to chunk text
    at semantic boundaries (paragraphs → sentences → characters).

    Args:
        text: Text to chunk
        chunk_size: Target chunk size in characters
        chunk_overlap: Overlap between chunks

    Returns:
        List of chunk dictionaries with metadata
    """
    logger.info(f"Chunking text (size={chunk_size}, overlap={chunk_overlap})")

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        separators=["\n\n", "\n", " ", ""]
    )

    chunks = splitter.split_text(text)
    logger.info(f"Created {len(chunks)} chunks")

    # Add metadata
    result = []
    current_page = 1

    for chunk_id, chunk_text in enumerate(chunks):
        # Extract page number if present in text
        if "[Page" in chunk_text:
            try:
                page_num = int(chunk_text.split("[Page ")[1].split("]")[0])
                current_page = page_num
            except (ValueError, IndexError):
                pass

        result.append({
            "chunk_id": chunk_id,
            "chunk_text": chunk_text,
            "page_num": current_page,
            "section_title": None
        })

    return result


def embed_chunks(
    chunks: List[Dict],
    model: str,
    api_key: str
) -> List[Dict]:
    """Generate embeddings for chunks via OpenRouter.

    Args:
        chunks: List of chunk dictionaries
        model: Embedding model name
        api_key: OpenRouter API key

    Returns:
        Chunks with embeddings added
    """
    logger.info(f"Generating embeddings for {len(chunks)} chunks using {model}")

    url = "https://openrouter.ai/api/v1/embeddings"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    embedded_chunks = []
    failed_chunks = 0

    for i, chunk in enumerate(chunks):
        try:
            # Limit chunk text for embedding (avoid token overflow)
            chunk_text_limited = chunk["chunk_text"][:2000]

            data = {
                "model": model,
                "input": chunk_text_limited
            }

            response = requests.post(url, json=data, headers=headers, timeout=10)
            response.raise_for_status()

            embedding = response.json()["data"][0]["embedding"]
            chunk["embedding"] = embedding
            embedded_chunks.append(chunk)

            if (i + 1) % 10 == 0:
                logger.info(f"Embedded {i + 1}/{len(chunks)} chunks...")

        except Exception as e:
            logger.error(f"Failed to embed chunk {chunk['chunk_id']}: {e}")
            failed_chunks += 1

    if failed_chunks > 0:
        logger.warning(f"Failed to embed {failed_chunks} chunks")

    logger.info(f"Successfully embedded {len(embedded_chunks)} chunks")
    return embedded_chunks


def store_in_qdrant(
    chunks: List[Dict],
    qdrant_url: str,
    api_key: str,
    collection_name: str,
    book_id: str = "default"
) -> bool:
    """Store embeddings in Qdrant Cloud.

    Args:
        chunks: List of chunks with embeddings
        qdrant_url: Qdrant Cloud URL
        api_key: Qdrant API key
        collection_name: Name of collection to store in
        book_id: Book identifier

    Returns:
        True if successful, False otherwise
    """
    try:
        logger.info(f"Connecting to Qdrant: {qdrant_url}")

        client = QdrantClient(
            url=qdrant_url,
            api_key=api_key,
            timeout=10
        )

        # Create or recreate collection
        try:
            from qdrant_client.models import VectorParams, Distance, PayloadSchemaType

            client.recreate_collection(
                collection_name=collection_name,
                vectors_config=VectorParams(
                    size=1536,  # text-embedding-3-small dimension
                    distance=Distance.COSINE
                )
            )
            logger.info(f"Created collection: {collection_name}")

            # Create payload index for book_id field
            client.create_payload_index(
                collection_name=collection_name,
                field_name="book_id",
                field_schema=PayloadSchemaType.KEYWORD
            )
            logger.info("Created index on book_id field")
        except Exception as e:
            logger.warning(f"Collection creation or recreation: {e}")

        # Create points for Qdrant
        points = [
            PointStruct(
                id=chunk["chunk_id"],
                vector=chunk["embedding"],
                payload={
                    "book_id": book_id,
                    "chunk_id": chunk["chunk_id"],
                    "chunk_text": chunk["chunk_text"],
                    "page_num": chunk["page_num"],
                    "section_title": chunk.get("section_title")
                }
            )
            for chunk in chunks
        ]

        logger.info(f"Uploading {len(points)} points to Qdrant...")

        # Upload to Qdrant
        client.upsert(
            collection_name=collection_name,
            points=points,
            wait=True
        )

        logger.info(f"Successfully stored {len(points)} chunks in Qdrant")
        return True

    except Exception as e:
        logger.error(f"Failed to store in Qdrant: {e}", exc_info=True)
        return False


def ingest_book(
    pdf_path: Path,
    book_id: str = "default"
) -> bool:
    """Full ingestion pipeline: load → chunk → embed → store.

    Args:
        pdf_path: Path to PDF file
        book_id: Unique identifier for book

    Returns:
        True if successful, False otherwise
    """
    try:
        logger.info(f"Starting book ingestion: {pdf_path}")
        print(f"\nIngesting {pdf_path}...")

        # Step 1: Load file
        print("1. Loading file...")
        if pdf_path.suffix.lower() == ".pdf":
            text = load_pdf(pdf_path)
        elif pdf_path.suffix.lower() == ".txt":
            text = load_txt(pdf_path)
        else:
            raise ValueError(f"Unsupported file type: {pdf_path.suffix}")
        print(f"   Loaded {len(text)} characters")

        # Step 2: Chunk text
        print("2. Chunking text...")
        chunks = chunk_text(text, Config.CHUNK_SIZE, Config.CHUNK_OVERLAP)
        print(f"   Created {len(chunks)} chunks")

        # Step 3: Generate embeddings
        print("3. Generating embeddings...")
        chunks = embed_chunks(
            chunks,
            Config.EMBEDDING_MODEL,
            Config.OPENROUTER_API_KEY
        )

        if not chunks:
            print("   ERROR: No chunks were successfully embedded")
            return False

        print(f"   Embedded {len(chunks)} chunks")

        # Step 4: Store in Qdrant
        print("4. Storing in Qdrant...")
        success = store_in_qdrant(
            chunks,
            Config.QDRANT_URL,
            Config.QDRANT_API_KEY,
            Config.COLLECTION_NAME,
            book_id
        )

        if success:
            print(f"\nSUCCESS: Ingestion complete!")
            print(f"   Book ID: {book_id}")
            print(f"   Chunks stored: {len(chunks)}")
            logger.info(f"Book ingestion successful: {book_id}")

        return success

    except Exception as e:
        logger.error(f"Book ingestion failed: {e}", exc_info=True)
        print(f"\nERROR: Ingestion failed: {e}")
        return False
