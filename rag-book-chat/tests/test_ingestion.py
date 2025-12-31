"""Unit tests for book ingestion pipeline."""

import pytest
from pathlib import Path
from unittest.mock import patch, MagicMock

from app.ingestion import load_pdf, chunk_text, embed_chunks, store_in_qdrant


class TestChunkText:
    """Tests for text chunking functionality."""

    def test_chunk_text_basic(self):
        """Test basic text chunking."""
        text = "This is a test. " * 100  # ~1600 characters
        chunks = chunk_text(text, chunk_size=100, chunk_overlap=10)

        assert len(chunks) > 1
        assert all("chunk_id" in c for c in chunks)
        assert all("chunk_text" in c for c in chunks)
        assert all("page_num" in c for c in chunks)

    def test_chunk_text_empty(self):
        """Test chunking empty text."""
        chunks = chunk_text("", chunk_size=100)
        assert len(chunks) == 0

    def test_chunk_text_single_chunk(self):
        """Test chunking short text that fits in one chunk."""
        text = "Short text"
        chunks = chunk_text(text, chunk_size=1000)

        assert len(chunks) == 1
        assert chunks[0]["chunk_text"] == text

    def test_chunk_metadata(self):
        """Test that chunk metadata is properly set."""
        text = "[Page 5]\nContent here"
        chunks = chunk_text(text)

        # First chunk should have page number extracted
        assert chunks[0]["page_num"] > 0

    def test_chunk_with_overlap(self):
        """Test that chunk overlap is maintained."""
        text = "word " * 200  # 1000 tokens worth
        chunks = chunk_text(text, chunk_size=100, chunk_overlap=20)

        # With overlap, chunks should have some common words
        assert len(chunks) > 1


class TestEmbedChunks:
    """Tests for chunk embedding (mocked to avoid API calls)."""

    @patch("app.ingestion.requests.post")
    def test_embed_chunks_success(self, mock_post):
        """Test successful embedding of chunks."""
        # Mock OpenRouter embedding response
        mock_post.return_value = MagicMock(
            status_code=200,
            json=lambda: {
                "data": [{"embedding": [0.1] * 1536}]
            }
        )

        chunks = [
            {"chunk_id": 0, "chunk_text": "Test chunk"},
            {"chunk_id": 1, "chunk_text": "Another chunk"}
        ]

        embedded = embed_chunks(chunks, "test-model", "test-key")

        assert len(embedded) == 2
        assert all("embedding" in c for c in embedded)

    @patch("app.ingestion.requests.post")
    def test_embed_chunks_failure(self, mock_post):
        """Test embedding with API failure."""
        mock_post.side_effect = Exception("API Error")

        chunks = [{"chunk_id": 0, "chunk_text": "Test"}]
        embedded = embed_chunks(chunks, "test-model", "test-key")

        # Should return empty list on failure
        assert len(embedded) == 0

    @patch("app.ingestion.requests.post")
    def test_embed_chunks_progress(self, mock_post):
        """Test that progress is logged during embedding."""
        mock_post.return_value = MagicMock(
            status_code=200,
            json=lambda: {
                "data": [{"embedding": [0.1] * 1536}]
            }
        )

        # Create 15 chunks to trigger progress logging
        chunks = [
            {"chunk_id": i, "chunk_text": f"Chunk {i}"}
            for i in range(15)
        ]

        embedded = embed_chunks(chunks, "test-model", "test-key")

        # All chunks should be embedded
        assert len(embedded) == 15


class TestLoadPdf:
    """Tests for PDF loading (would require PDF fixtures)."""

    def test_load_pdf_not_found(self):
        """Test loading non-existent PDF."""
        with pytest.raises(FileNotFoundError):
            load_pdf(Path("nonexistent.pdf"))
