"""Integration tests for FastAPI endpoints."""

import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock

from app.main import app

client = TestClient(app)


class TestHealthEndpoint:
    """Tests for /health endpoint."""

    def test_health_check(self):
        """Test health check endpoint."""
        response = client.get("/health")

        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert "timestamp" in data


class TestQueryEndpoint:
    """Tests for /query endpoint."""

    def test_query_valid_request(self):
        """Test valid query request."""
        with patch("app.main.retrieve_similar_chunks") as mock_retrieve, \
             patch("app.main.synthesize_answer") as mock_synthesize:

            mock_retrieve.return_value = [
                {
                    "chunk_text": "Test content from page 5",
                    "page_num": 5,
                    "chunk_id": 0,
                    "section_title": "Introduction",
                    "similarity_score": 0.85
                }
            ]
            mock_synthesize.return_value = ("This is a test answer", False)

            response = client.post(
                "/query",
                json={"question": "What is this?", "book_id": "test-book"}
            )

            assert response.status_code == 200
            data = response.json()
            assert "answer" in data
            assert "sources" in data
            assert "is_fallback" in data
            assert data["model"] is not None
            assert data["latency_ms"] > 0

    def test_query_empty_question(self):
        """Test query with empty question."""
        response = client.post(
            "/query",
            json={"question": "", "book_id": "test-book"}
        )

        # Should fail Pydantic validation
        assert response.status_code == 422

    def test_query_with_selected_text(self):
        """Test query with selected text."""
        with patch("app.main.retrieve_similar_chunks") as mock_retrieve, \
             patch("app.main.synthesize_answer") as mock_synthesize:

            mock_retrieve.return_value = []
            mock_synthesize.return_value = ("Answer", False)

            response = client.post(
                "/query",
                json={
                    "question": "What does this mean?",
                    "selected_text": "Some selected text from page",
                    "book_id": "test-book"
                }
            )

            assert response.status_code == 200

    def test_query_with_fallback_response(self):
        """Test query that returns fallback answer."""
        with patch("app.main.retrieve_similar_chunks") as mock_retrieve, \
             patch("app.main.synthesize_answer") as mock_synthesize:

            mock_retrieve.return_value = []
            mock_synthesize.return_value = ("Based on general knowledge...", True)

            response = client.post(
                "/query",
                json={"question": "Unrelated question?", "book_id": "test-book"}
            )

            assert response.status_code == 200
            data = response.json()
            assert data["is_fallback"] is True


class TestSessionEndpoint:
    """Tests for session management endpoints."""

    def test_create_session(self):
        """Test session creation."""
        response = client.post("/session")

        assert response.status_code == 200
        data = response.json()
        assert "session_id" in data
        assert "message" in data

    def test_get_session_info(self):
        """Test getting session info."""
        # First create a session
        create_response = client.post("/session")
        session_id = create_response.json()["session_id"]

        # Get session info
        response = client.get(f"/session/{session_id}")

        assert response.status_code == 200
        data = response.json()
        assert data["session_id"] == session_id
        assert "created_at" in data
        assert "expires_at" in data
        assert data["message_count"] >= 0

    def test_get_nonexistent_session(self):
        """Test getting non-existent session."""
        response = client.get("/session/nonexistent-id")

        assert response.status_code == 404


class TestBooksEndpoint:
    """Tests for book listing endpoint."""

    def test_list_books_empty(self):
        """Test listing books when none ingested."""
        response = client.get("/books")

        assert response.status_code == 200
        data = response.json()
        assert "books" in data
        assert "total" in data
        assert data["total"] >= 0


class TestIngestEndpoint:
    """Tests for book ingestion endpoint."""

    def test_ingest_book_invalid_format(self):
        """Test book ingestion with invalid file format."""
        # Create a fake file content
        invalid_file = ("invalid.docx", b"fake content", "application/vnd.openxmlformats-officedocument.wordprocessingml.document")

        response = client.post(
            "/ingest",
            data={"book_id": "test-book"},
            files={"file": invalid_file}
        )

        assert response.status_code == 400
        assert "PDF" in response.json()["detail"] or "TXT" in response.json()["detail"]

    def test_ingest_book_invalid_book_id(self):
        """Test book ingestion with invalid book_id."""
        from io import BytesIO

        pdf_content = BytesIO(b"fake pdf content")

        response = client.post(
            "/ingest",
            data={"book_id": ""},  # Empty book_id
            files={"file": ("test.pdf", pdf_content, "application/pdf")}
        )

        # Should fail validation
        assert response.status_code in [400, 422]


class TestPrivacyEndpoints:
    """Tests for privacy audit and management."""

    def test_privacy_audit(self):
        """Test privacy audit endpoint."""
        response = client.get("/audit/privacy")

        assert response.status_code == 200
        data = response.json()
        assert "total_sessions" in data
        assert "active_sessions" in data
        assert "audit_status" in data
        assert data["audit_status"] in ["clean", "warning"]

    def test_purge_expired_sessions(self):
        """Test manual session purge endpoint."""
        response = client.post("/admin/purge-sessions")

        assert response.status_code == 200
        data = response.json()
        assert "status" in data
        assert "purged_count" in data


class TestSelectionBasedQueries:
    """Tests for selection-based query feature (User Story 2)."""

    def test_query_with_selected_text_and_chunks(self):
        """Test query where both selected text and retrieved chunks are provided."""
        with patch("app.main.retrieve_similar_chunks") as mock_retrieve, \
             patch("app.main.synthesize_answer") as mock_synthesize:

            mock_retrieve.return_value = [
                {
                    "chunk_text": "Supplementary information",
                    "page_num": 10,
                    "chunk_id": 5,
                    "similarity_score": 0.75
                }
            ]
            mock_synthesize.return_value = ("Answer based on selection and supplementary content", False)

            response = client.post(
                "/query",
                json={
                    "question": "What does this mean?",
                    "selected_text": "User selected: Some important passage",
                    "book_id": "test-book"
                }
            )

            assert response.status_code == 200
            data = response.json()
            assert "answer" in data
            # Verify that synthesize_answer was called with selected_text
            mock_synthesize.assert_called_once()
            call_args = mock_synthesize.call_args
            assert call_args[1]["selected_text"] == "User selected: Some important passage"


class TestFallbackBehavior:
    """Tests for fallback behavior (User Story 6)."""

    def test_query_with_fallback_flag(self):
        """Test that is_fallback flag is properly set in response."""
        with patch("app.main.retrieve_similar_chunks") as mock_retrieve, \
             patch("app.main.synthesize_answer") as mock_synthesize:

            # No chunks found - should trigger fallback
            mock_retrieve.return_value = []
            mock_synthesize.return_value = ("Based on general knowledge: Answer", True)

            response = client.post(
                "/query",
                json={"question": "Unrelated topic?", "book_id": "test-book"}
            )

            assert response.status_code == 200
            data = response.json()
            assert data["is_fallback"] is True
            assert "general knowledge" in data["answer"].lower() or "Based on" in data["answer"]


class TestErrorHandling:
    """Tests for error handling."""

    def test_query_with_retrieval_error(self):
        """Test query when retrieval fails."""
        with patch("app.main.retrieve_similar_chunks") as mock_retrieve:
            mock_retrieve.side_effect = Exception("Retrieval error")

            response = client.post(
                "/query",
                json={"question": "Test?", "book_id": "test-book"}
            )

            assert response.status_code == 500
            data = response.json()
            assert "detail" in data
