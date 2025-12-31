"""Unit tests for RAG retrieval and synthesis."""

import pytest
from unittest.mock import patch, MagicMock

from app.rag import retrieve_similar_chunks, synthesize_answer


class TestRetrieveSimilarChunks:
    """Tests for semantic search retrieval."""

    @patch("app.rag.requests.post")
    @patch("app.rag.QdrantClient")
    def test_retrieve_chunks_success(self, mock_qdrant, mock_post):
        """Test successful chunk retrieval."""
        # Mock embedding response
        mock_post.return_value = MagicMock(
            status_code=200,
            json=lambda: {
                "data": [{"embedding": [0.1] * 1536}]
            }
        )

        # Mock Qdrant search response
        mock_client = MagicMock()
        mock_qdrant.return_value = mock_client

        mock_search_result = MagicMock(
            score=0.85,
            payload={
                "chunk_text": "Test content",
                "page_num": 5,
                "chunk_id": 0,
                "section_title": "Introduction"
            }
        )
        mock_client.search.return_value = [mock_search_result]

        results = retrieve_similar_chunks("What is this?")

        assert len(results) == 1
        assert results[0]["chunk_text"] == "Test content"
        assert results[0]["page_num"] == 5

    @patch("app.rag.requests.post")
    def test_retrieve_chunks_embedding_failure(self, mock_post):
        """Test retrieval when embedding fails."""
        mock_post.side_effect = Exception("API Error")

        results = retrieve_similar_chunks("Test question")

        # Should return empty list on failure
        assert len(results) == 0

    @patch("app.rag.requests.post")
    @patch("app.rag.QdrantClient")
    def test_retrieve_chunks_threshold(self, mock_qdrant, mock_post):
        """Test that low-relevance chunks are filtered."""
        # Mock embedding response
        mock_post.return_value = MagicMock(
            status_code=200,
            json=lambda: {
                "data": [{"embedding": [0.1] * 1536}]
            }
        )

        # Mock Qdrant with low-score result
        mock_client = MagicMock()
        mock_qdrant.return_value = mock_client

        mock_low_score = MagicMock(
            score=0.4,  # Below 0.6 threshold
            payload={
                "chunk_text": "Low relevance",
                "page_num": 1,
                "chunk_id": 0,
                "section_title": None
            }
        )
        mock_client.search.return_value = [mock_low_score]

        results = retrieve_similar_chunks("Question", threshold=0.6)

        # Should be filtered out by threshold
        assert len(results) == 0

    @patch("app.rag.requests.post")
    @patch("app.rag.QdrantClient")
    def test_retrieve_chunks_multiple_results(self, mock_qdrant, mock_post):
        """Test retrieval of multiple relevant chunks."""
        mock_post.return_value = MagicMock(
            status_code=200,
            json=lambda: {
                "data": [{"embedding": [0.1] * 1536}]
            }
        )

        mock_client = MagicMock()
        mock_qdrant.return_value = mock_client

        # Create multiple mock results
        mock_results = [
            MagicMock(
                score=0.9 - (i * 0.05),
                payload={
                    "chunk_text": f"Content {i}",
                    "page_num": i + 1,
                    "chunk_id": i,
                    "section_title": None
                }
            )
            for i in range(5)
        ]
        mock_client.search.return_value = mock_results

        results = retrieve_similar_chunks("Question", top_k=5)

        assert len(results) == 5
        # Should be sorted by score (descending)
        assert results[0]["similarity_score"] > results[1]["similarity_score"]


class TestSynthesizeAnswer:
    """Tests for LLM-based answer synthesis."""

    @patch("app.rag.requests.post")
    def test_synthesize_with_context(self, mock_post):
        """Test synthesis with context chunks."""
        mock_post.return_value = MagicMock(
            status_code=200,
            json=lambda: {
                "choices": [{"message": {"content": "Test answer"}}]
            }
        )

        chunks = [
            {
                "chunk_text": "Relevant information",
                "page_num": 5,
                "chunk_id": 0,
                "similarity_score": 0.9
            }
        ]

        answer, is_fallback = synthesize_answer("What is this?", chunks)

        assert answer == "Test answer"
        assert is_fallback is False

    @patch("app.rag.requests.post")
    def test_synthesize_no_context_with_fallback(self, mock_post):
        """Test synthesis without context using fallback."""
        mock_post.return_value = MagicMock(
            status_code=200,
            json=lambda: {
                "choices": [{"message": {"content": "General knowledge answer"}}]
            }
        )

        answer, is_fallback = synthesize_answer("Question", [], include_fallback=True)

        assert answer == "General knowledge answer"
        assert is_fallback is True

    @patch("app.rag.requests.post")
    def test_synthesize_no_context_no_fallback(self, mock_post):
        """Test synthesis without context and no fallback allowed."""
        answer, is_fallback = synthesize_answer("Question", [], include_fallback=False)

        assert "couldn't find" in answer.lower()
        assert is_fallback is False

    @patch("app.rag.requests.post")
    def test_synthesize_llm_failure(self, mock_post):
        """Test synthesis when LLM call fails."""
        mock_post.side_effect = Exception("LLM Error")

        chunks = [
            {"chunk_text": "Content", "page_num": 1, "chunk_id": 0, "similarity_score": 0.9}
        ]

        answer, is_fallback = synthesize_answer("Question", chunks)

        assert "Error" in answer
        assert is_fallback is False
