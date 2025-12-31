# RAG Chatbot Integration for Digital Books

A Retrieval-Augmented Generation (RAG) chatbot that answers reader questions about digital books by retrieving relevant content via semantic search and synthesizing responses using LLMs.

## Features (Phase 1 MVP)

- **Full-Book Semantic Search**: Ask questions about entire book content, get answers synthesized from relevant sections
- **Session-Based Conversations**: Maintain conversation context across multiple queries within a session
- **Real-Time Response Streaming**: Display answers as they're generated
- **Privacy-First Design**: No persistent user data, sessions auto-expire
- **Smart Fallbacks**: Graceful handling of out-of-scope questions with general knowledge

## Technology Stack

- **Backend**: Python 3.10+, FastAPI, Uvicorn
- **Vector DB**: Qdrant Cloud (semantic search)
- **LLM**: OpenRouter API (gpt-4o-mini, Claude, or custom models)
- **Text Processing**: LangChain, PyPDF
- **Testing**: pytest, pytest-asyncio

## Quick Start

### Prerequisites

1. **API Keys**:
   - Qdrant Cloud: https://cloud.qdrant.io (free tier)
   - OpenRouter: https://openrouter.ai (free trial)

2. **Python**: Version 3.10 or higher

3. **Book File**: PDF or text file of a book to ingest

### Setup (5 minutes)

```bash
# Clone or create project
git clone <repo> rag-book-chat
cd rag-book-chat

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env with your API keys:
# - QDRANT_URL=https://your-cluster-url:6333
# - QDRANT_API_KEY=your-key
# - OPENROUTER_API_KEY=sk-or-v1-your-key
```

### Validate Setup (10 minutes)

```bash
# Test Qdrant connection
python scripts/test_qdrant_connection.py

# Test OpenRouter APIs
python scripts/test_openrouter_api.py

# Run unit tests
pytest tests/ -v
```

### Ingest a Book (5 minutes)

```bash
# Place PDF in repo root or provide path
python scripts/ingest_book.py path/to/book.pdf --book-id my-book

# Expected output:
# 1. Loading PDF...
# 2. Chunking text...
# 3. Generating embeddings...
# 4. Storing in Qdrant...
# ✅ Ingestion complete!
```

### Start the Server

```bash
uvicorn app.main:app --port 8001 --reload
```

### Query via API

```bash
# Full-book query
curl -X POST http://localhost:8001/query \
  -H "Content-Type: application/json" \
  -d '{
    "question": "What is the main topic of chapter 1?",
    "book_id": "my-book"
  }'

# Response:
{
  "answer": "In Chapter 1, the book introduces...",
  "sources": [
    {
      "chunk_text": "Chapter 1 begins with...",
      "page_num": 3,
      "chunk_id": 0,
      "similarity_score": 0.89
    }
  ],
  "is_fallback": false,
  "model": "openai/gpt-4o-mini",
  "latency_ms": 2340,
  "timestamp": 1704067200.0
}
```

## Project Structure

```
rag-book-chat/
├── app/
│   ├── __init__.py          # Package initialization
│   ├── config.py            # Configuration management
│   ├── main.py              # FastAPI application
│   ├── models.py            # Pydantic request/response models
│   ├── ingestion.py         # Book ingestion pipeline
│   └── rag.py               # RAG retrieval and synthesis
├── tests/
│   ├── __init__.py
│   ├── test_ingestion.py    # Unit tests for ingestion
│   ├── test_rag.py          # Unit tests for RAG
│   └── test_api.py          # Integration tests for API
├── scripts/
│   ├── ingest_book.py       # CLI script for book ingestion
│   ├── test_qdrant_connection.py    # Validate Qdrant setup
│   └── test_openrouter_api.py       # Validate OpenRouter setup
├── docs/
│   ├── API.md               # API documentation
│   ├── ARCHITECTURE.md      # Design decisions
│   └── QUICKSTART.md        # Detailed setup guide
├── requirements.txt         # Python dependencies
├── .env.example             # Environment template
├── .gitignore              # Git ignore rules
└── README.md               # This file
```

## API Endpoints

### Query (POST `/query`)
Ask questions about a book.

**Request**:
```json
{
  "question": "What is ROS 2?",
  "selected_text": "optional selected passage",
  "book_id": "my-book",
  "top_k": 5
}
```

**Response**:
```json
{
  "answer": "ROS 2 is...",
  "sources": [...],
  "is_fallback": false,
  "model": "openai/gpt-4o-mini",
  "latency_ms": 2340,
  "timestamp": 1704067200.0
}
```

### Session (POST `/session`)
Create a new conversation session.

**Response**:
```json
{
  "session_id": "550e8400-e29b-41d4-a716-446655440000",
  "message": "Session created. Expires in 30 minutes."
}
```

### Books (GET `/books`)
List ingested books.

**Response**:
```json
{
  "books": [
    {
      "book_id": "my-book",
      "title": "My Book",
      "author": "Author Name",
      "chunk_count": 523,
      "uploaded_at": "2025-12-31T12:00:00"
    }
  ],
  "total": 1
}
```

### Health (GET `/health`)
System health check.

**Response**:
```json
{
  "status": "healthy",
  "timestamp": 1704067200.0
}
```

## Configuration

Edit `.env` to customize:

```bash
# Qdrant Cloud
QDRANT_URL=https://your-cluster-url:6333
QDRANT_API_KEY=your-api-key

# OpenRouter
OPENROUTER_API_KEY=sk-or-v1-your-key

# RAG Settings
CHUNK_SIZE=850              # Characters per chunk
CHUNK_OVERLAP=180           # Overlap between chunks
EMBEDDING_MODEL=text-embedding-3-small
CHAT_MODEL=openai/gpt-4o-mini

# Server
APP_PORT=8001
```

## Testing

```bash
# Run all tests
pytest tests/ -v

# Run with coverage
pytest tests/ --cov=app --cov-report=html

# Run specific test
pytest tests/test_api.py::TestQueryEndpoint -v
```

## Troubleshooting

### "Qdrant connection failed"
- Check `QDRANT_URL` and `QDRANT_API_KEY` in `.env`
- Verify internet connection
- Test manually: `curl -H "Authorization: Bearer $KEY" $QDRANT_URL/health`

### "Invalid API key" from OpenRouter
- Verify `OPENROUTER_API_KEY` in `.env`
- Ensure no trailing whitespace
- Check OpenRouter dashboard for rate limits

### "PDF not found"
- Place PDF in repo root as `book.pdf`
- Or provide full path: `python scripts/ingest_book.py /path/to/book.pdf`

### "Chunk embedding failed"
- Check internet connection
- Verify OpenRouter API quota
- Check for rate limiting

## Phase 1 MVP Checklist

- [x] Project structure and configuration
- [x] FastAPI application with endpoints
- [x] Qdrant Cloud integration
- [x] OpenRouter API integration
- [x] Book ingestion pipeline (PDF → chunks → embeddings → storage)
- [x] RAG retrieval and synthesis
- [x] Session management (in-memory, auto-expire)
- [x] Unit and integration tests
- [x] Error handling and logging

## Phase 2+ Roadmap

- [ ] ChatKit web component embedding
- [ ] Selection-based query context
- [ ] Neon Postgres metadata storage
- [ ] Response streaming (Server-Sent Events)
- [ ] Rate limiting and abuse detection
- [ ] Analytics and user feedback loops
- [ ] Multi-language support
- [ ] Fine-tuned embeddings

## Development

### Running with Hot Reload

```bash
uvicorn app.main:app --port 8001 --reload
```

### Logging

Logs are written to console by default. Set log level in `app/config.py`:

```python
logging.basicConfig(level=logging.DEBUG)
```

### Code Style

This project follows PEP 8. Format with:

```bash
pip install black
black app/ tests/
```

## Cost Estimation (Monthly, 1000 queries/day)

| Component | Cost |
|-----------|------|
| OpenRouter Embeddings | $0.60 |
| OpenRouter LLM (gpt-4o-mini) | $4.50 |
| Qdrant Cloud Free | $0.00 |
| Neon Postgres Free | $0.00 |
| **Total** | **$5.10** |

Free tier sufficient for MVP. Upgrade as needed.

## Privacy & Security

- **Zero Data Retention**: Queries and responses deleted on session expiration
- **No User Tracking**: No identities, behavior logs, or persistent data
- **Secure APIs**: HTTPS/TLS for all communication
- **No Third-Party Logging**: User queries not logged to third parties

## License

MIT (or specify your license)

## Support

For issues or questions:
1. Check `docs/QUICKSTART.md` for detailed setup guide
2. Review `docs/ARCHITECTURE.md` for design decisions
3. Check logs for error details
4. Run test scripts to validate setup

---

**Ready to build?** Start with `python scripts/test_qdrant_connection.py` ✅
