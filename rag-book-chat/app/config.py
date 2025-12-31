"""Configuration management for RAG Chatbot application."""

import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class Config:
    """Application configuration."""

    # Qdrant Cloud Configuration
    QDRANT_URL = os.getenv("QDRANT_URL", "https://your-url:6333")
    QDRANT_API_KEY = os.getenv("QDRANT_API_KEY", "your-key")
    COLLECTION_NAME = os.getenv("COLLECTION_NAME", "book_v1")

    # OpenRouter API Configuration
    OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY", "sk-or-v1-...")
    EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "text-embedding-3-small")
    CHAT_MODEL = os.getenv("CHAT_MODEL", "openai/gpt-4o-mini")

    # Book Configuration
    BOOK_PATH = Path(__file__).parent.parent / "book.pdf"
    CHUNK_SIZE = int(os.getenv("CHUNK_SIZE", "850"))
    CHUNK_OVERLAP = int(os.getenv("CHUNK_OVERLAP", "180"))

    # Server Configuration
    APP_PORT = int(os.getenv("APP_PORT", "8001"))

    # RAG Configuration
    RELEVANCE_THRESHOLD = 0.6
    TOP_K_DEFAULT = 5
    SESSION_TIMEOUT_SECONDS = 1800  # 30 minutes


# Validate that API keys are configured
if Config.QDRANT_API_KEY == "your-key":
    print("WARNING: QDRANT_API_KEY not configured in .env file")

if Config.OPENROUTER_API_KEY == "sk-or-v1-...":
    print("WARNING: OPENROUTER_API_KEY not configured in .env file")
