#!/usr/bin/env python
"""
Simple book ingestion without PyTorch dependency.
Works around Windows DLL loading issues.
"""

import argparse
import logging
from pathlib import Path
import sys

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger(__name__)

def chunk_text_simple(text, chunk_size=850, overlap=180):
    """Simple text chunking without LangChain."""
    chunks = []
    start = 0

    while start < len(text):
        # Get chunk
        end = min(start + chunk_size, len(text))

        # Try to break at a sentence boundary
        if end < len(text):
            last_period = text.rfind('.', start, end)
            if last_period > start + chunk_size * 0.5:  # Only if not too far back
                end = last_period + 1

        chunk = text[start:end].strip()
        if chunk:
            chunks.append({'text': chunk, 'index': len(chunks)})

        # Move to next chunk with overlap
        start = end - overlap
        if start <= 0:
            break

    return chunks

def load_text_file(file_path):
    """Load text from file."""
    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")

    if path.suffix.lower() == '.pdf':
        try:
            from PyPDF2 import PdfReader
            logger.info(f"📖 Loading PDF: {file_path}")
            reader = PdfReader(file_path)
            text = ""
            for page_num, page in enumerate(reader.pages, 1):
                try:
                    text += f"\n[Page {page_num}]\n"
                    text += page.extract_text()
                except Exception as e:
                    logger.warning(f"⚠️ Failed to extract page {page_num}: {e}")
            logger.info(f"✅ Extracted {len(text)} characters from {len(reader.pages)} pages")
            return text
        except ImportError:
            logger.error("❌ PyPDF2 not installed. Run: pip install PyPDF2")
            sys.exit(1)
    else:
        # Assume text file
        logger.info(f"📄 Loading text file: {file_path}")
        with open(file_path, 'r', encoding='utf-8') as f:
            text = f.read()
        logger.info(f"✅ Loaded {len(text)} characters")
        return text

def ingest_book(file_path, book_id):
    """Main ingestion function."""
    logger.info("\n🚀 Starting book ingestion...")
    logger.info(f"📚 Book ID: {book_id}")
    logger.info(f"📁 File: {file_path}\n")

    try:
        # Load text
        logger.info("[1/4] Loading text...")
        text = load_text_file(file_path)
        logger.info(f"✅ Loaded {len(text):,} characters\n")

        # Chunk text
        logger.info("[2/4] Chunking text...")
        chunks = chunk_text_simple(text, chunk_size=850, overlap=180)
        logger.info(f"✅ Created {len(chunks)} chunks\n")

        logger.info("[3/4] Note: Embedding and storage require backend API")
        logger.info("Use the normal ingest_book.py with backend running:\n")
        logger.info("  # Start backend:")
        logger.info("  uvicorn app.main:app --port 8001\n")
        logger.info("  # Then ingest:")
        logger.info("  python scripts/ingest_book.py book.pdf --book-id my-book\n")

        # Display sample chunk
        logger.info("[4/4] Sample chunk:")
        logger.info("─" * 80)
        sample = chunks[0]['text'][:200] + "..."
        logger.info(sample)
        logger.info("─" * 80)

        logger.info("\n✅ Text processing complete!")
        logger.info(f"\n💡 Next steps:")
        logger.info("  1. Make sure .env has API keys configured")
        logger.info("  2. Start backend: uvicorn app.main:app --port 8001")
        logger.info("  3. Run full ingestion: python scripts/ingest_book.py book.pdf --book-id my-book")

        return True

    except Exception as e:
        logger.error(f"\n❌ Ingestion failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Simple book ingestion (preview mode)')
    parser.add_argument('file', help='Path to book file (PDF or TXT)')
    parser.add_argument('--book-id', default='my-book', help='Book identifier')

    args = parser.parse_args()

    ingest_book(args.file, args.book_id)
