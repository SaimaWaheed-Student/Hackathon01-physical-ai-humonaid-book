"""CLI script for ingesting books into RAG chatbot."""

import sys
from pathlib import Path
import argparse

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.ingestion import ingest_book


def main():
    """Main entry point for book ingestion."""
    parser = argparse.ArgumentParser(
        description="Ingest a book into the RAG chatbot"
    )
    parser.add_argument(
        "pdf_path",
        nargs="?",
        default="book.pdf",
        help="Path to PDF file (default: book.pdf)"
    )
    parser.add_argument(
        "--book-id",
        default="default",
        help="Unique identifier for book (default: default)"
    )
    parser.add_argument(
        "--chunk-size",
        type=int,
        default=850,
        help="Chunk size in characters (default: 850)"
    )
    parser.add_argument(
        "--chunk-overlap",
        type=int,
        default=180,
        help="Chunk overlap in characters (default: 180)"
    )

    args = parser.parse_args()

    pdf_path = Path(args.pdf_path)

    if not pdf_path.exists():
        print(f"ERROR: File not found: {pdf_path}")
        sys.exit(1)

    if not pdf_path.suffix.lower() in [".pdf", ".txt"]:
        print(f"ERROR: File must be PDF or TXT: {pdf_path}")
        sys.exit(1)

    # Ingest the book
    success = ingest_book(pdf_path, args.book_id)

    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
