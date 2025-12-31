# Implementation Plan: RAG Chatbot Integration for Digital Books

**Branch**: `001-rag-chatbot-integration` | **Date**: 2025-12-30 | **Spec**: [RAG Chatbot Integration Specification](./spec.md)
**Input**: Feature specification from `specs/001-rag-chatbot-integration/spec.md`

**Approach**: Phased implementation starting with local prototype (Phase 1) to validate RAG + FastAPI + OpenRouter integration, then expand to full feature with ChatKit embedding and privacy handling (Phase 2+)

## Summary

Build a Retrieval-Augmented Generation (RAG) chatbot that answers reader questions about digital books by retrieving relevant content chunks via semantic search and synthesizing answers using LLMs. The MVP (Phase 1) focuses on core RAG functionality: book ingestion → chunking → embedding → Qdrant storage → OpenRouter-based retrieval and generation via FastAPI endpoints. Phase 2 adds ChatKit web component embedding for seamless integration on book pages. Phase 3 adds privacy-first session management, selection-based context, and advanced fallback behavior.

**Phase 1 Goal**: Working local prototype with Qdrant cloud integration, OpenRouter LLM calls, and FastAPI `/query` endpoint that answers questions from actual book content (not hallucinated).

## Technical Context

**Language/Version**: Python 3.10+ (supports FastAPI, Qdrant client, LangChain, PyPDF)
**Primary Dependencies**:
- FastAPI 0.115+ (API framework)
- Qdrant Client 1.12+ (vector DB client)
- LangChain 0.3.8 (RAG orchestration + text splitting)
- OpenRouter API (via custom base_url with langchain-openai)
- PyPDF 5.1+ (PDF parsing)
- python-dotenv (config management)
- tiktoken (token counting for chunking)

**Storage**:
- **Vector DB**: Qdrant Cloud Free Tier (embeddings + metadata)
- **Metadata DB**: Neon Serverless Postgres (book records, chunk references, optional session logs)
- **In-Memory**: Python dicts/lists for session conversation history (Phase 1-2)

**Testing**: pytest + pytest-asyncio (async endpoint testing), mocking OpenRouter/Qdrant for unit tests

**Target Platform**: Linux/macOS/Windows via FastAPI + Docker, browses via modern browsers (ChatKit web component)

**Project Type**: Web application with backend API (FastAPI) + frontend ChatKit integration

**Performance Goals**:
- Query response time: <3 seconds (p95)
- Book ingestion: <5 minutes for 10,000 pages
- Support 50+ concurrent queries without blocking

**Constraints**:
- <200ms average embedding call latency (OpenRouter)
- <1 second Qdrant vector search latency
- Free-tier cost: operate within Qdrant Cloud Free + Neon Free quotas
- No persistent user data (queries/responses purged after session)

**Scale/Scope**:
- 1.0 MVP: 10+ books, 100+ concurrent sessions, ~1000 queries/day
- 2.0: Multi-user with optional analytics, selection-based context
- Future: Fine-tuned embeddings, advanced ranking, real-time book updates

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

**Constitution Scope Review** (Physical AI & Humanoid Robotics Book Project):

The RAG chatbot is a **tool feature for the book platform**, not a module of the book itself. It serves the book's core principle (Hands-On Learning First) by enabling readers to quickly find relevant code examples and concepts.

| Gate | Requirement | Status | Notes |
|------|-------------|--------|-------|
| Hands-On Learning First | All chatbot interactions must be testable locally | ✅ PASS | Phase 1 uses local FastAPI + Qdrant Cloud; readers can test `curl` queries |
| Code Quality & Reproducibility | Chatbot backend must follow professional standards (error handling, logging, modular) | ✅ PASS | Modular structure: config.py, ingestion.py, rag.py, main.py; logging throughout |
| Simulation-First | Chatbot works without requiring external services (fallback to general knowledge) | ✅ PASS | Works with local book data + OpenRouter; graceful fallback when Qdrant unavailable |
| Accessibility | ChatKit widget must be WCAG 2.1 AA compliant (Phase 2+); text-searchable | ✅ PASS (defer) | Phase 2 requirement; Phase 1 focuses on backend API testability |
| Open Source | No proprietary LLM APIs required; OpenRouter enables model choice flexibility | ✅ PASS | OpenRouter allows switching between OpenAI, Claude, open-source models |
| Safety | Session-based (no persistent user data); no training on reader data | ✅ PASS | Ephemeral sessions; zero data retention post-session |

**Complexity Justification**: None. RAG chatbot adds zero new modules to the book; it enhances the platform delivery experience.

## Project Structure

### Documentation (this feature)

```text
specs/[###-feature]/
├── plan.md              # This file (/sp.plan command output)
├── research.md          # Phase 0 output (/sp.plan command)
├── data-model.md        # Phase 1 output (/sp.plan command)
├── quickstart.md        # Phase 1 output (/sp.plan command)
├── contracts/           # Phase 1 output (/sp.plan command)
└── tasks.md             # Phase 2 output (/sp.tasks command - NOT created by /sp.plan)
```

### Source Code (repository root)

```text
rag-book-chat/                    # Phase 1 root (can live in separate repo or under book platform)
├── app/
│   ├── __init__.py
│   ├── main.py                   # FastAPI app + route handlers
│   ├── config.py                 # Config + environment vars
│   ├── ingestion.py              # PDF loading → chunking → embedding → Qdrant storage
│   ├── rag.py                    # Retrieval logic + LLM synthesis
│   ├── dependencies.py           # Shared clients (Qdrant, LLM, embeddings)
│   └── models.py                 # Pydantic request/response models
├── tests/
│   ├── test_ingestion.py         # Unit tests for chunking, embedding
│   ├── test_rag.py               # Unit tests for retrieval, synthesis
│   ├── test_api.py               # Integration tests for FastAPI endpoints
│   └── fixtures/                 # Mock Qdrant, OpenRouter responses
├── scripts/
│   ├── ingest_book.py            # CLI script to ingest a PDF into Qdrant
│   └── test_qdrant_connection.py # Debug script to verify Qdrant access
├── docs/
│   ├── API.md                    # OpenAPI spec (generated from FastAPI)
│   ├── ARCHITECTURE.md           # Design decisions + flow diagrams
│   └── QUICKSTART.md             # Phase 1 getting started
├── requirements.txt              # Python dependencies
├── .env.example                  # Template for environment variables
├── .gitignore                    # Ignore .env, __pycache__, etc.
├── docker-compose.yml            # (Optional Phase 2) Local Postgres + Qdrant for testing
└── README.md                     # Project overview

Phase 2+ additions:
├── frontend/                     # ChatKit integration (JavaScript/React)
│   ├── dist/                     # Built web component
│   └── src/                      # ChatKit wrapper + embed scripts
└── migrations/                   # Neon Postgres schema (Phase 2)
```

**Structure Decision**: Single Python backend (FastAPI) + embedded ChatKit frontend (Phase 2). Phase 1 focuses on backend API validation via curl/Postman. Clear separation allows independent testing and future ChatKit integration without backend changes.

## Complexity Tracking

No violations. Constitution Check passes fully. Single backend project + shared ChatKit component fits the requirements perfectly.

---

## Phase 1 Implementation Breakdown (Foundation MVP)

**Timeline**: 2-3 weeks (Part-time) | **Goal**: Working local prototype with cloud integration

### Phase 1 Phases (Nested)

#### 1.1 Environment & Configuration (Step 1-3)

**Deliverables**:
- `requirements.txt` with pinned versions
- `app/config.py` with all keys/endpoints
- `.env.example` template (git-safe)
- `scripts/test_qdrant_connection.py` (validation)
- `scripts/test_openrouter_api.py` (validation)

**Success Criteria**:
- ✅ `python -c "from app.config import Config; print(Config.QDRANT_URL)"` works
- ✅ Qdrant Cloud connection test returns 200 OK
- ✅ OpenRouter embedding test returns valid embedding vector
- ✅ All secrets in `.env` (not git-tracked)

**Effort**: 30 minutes

---

#### 1.2 Book Ingestion Pipeline (Step 4)

**Files**:
- `app/ingestion.py` with functions:
  - `load_pdf(path)` → text
  - `chunk_text(text, chunk_size=850, overlap=180)` → list of chunks
  - `embed_chunks(chunks, model, api_key)` → embeddings via OpenRouter
  - `store_in_qdrant(chunks, embeddings, qdrant_url, api_key, collection_name)` → creates/updates Qdrant collection

**Data Flow**:
```
PDF → PyPDF → raw text → LangChain RecursiveCharacterTextSplitter → chunks
chunks → OpenRouter embedding API → embeddings
chunks + embeddings → Qdrant Cloud (with metadata: book_id, chunk_id, text)
```

**Qdrant Collection Schema**:
```json
{
  "name": "book_v1",
  "vectors": {
    "size": 1536,  // text-embedding-3-small dimension
    "distance": "Cosine"
  },
  "payload_schema": {
    "book_id": {"type": "keyword"},
    "chunk_id": {"type": "integer"},
    "chunk_text": {"type": "text"},
    "page_num": {"type": "integer"}
  }
}
```

**Success Criteria**:
- ✅ `python scripts/ingest_book.py --pdf book.pdf --book-id my-book` completes in <5 min
- ✅ Qdrant collection contains 100+ vectors (for typical book)
- ✅ Each vector has chunk_text payload (for citations)
- ✅ Unit tests pass: `pytest tests/test_ingestion.py`

**Effort**: 50 minutes

---

#### 1.3 RAG Retrieval & Synthesis (Step 5)

**Files**:
- `app/rag.py` with functions:
  - `retrieve_similar_chunks(query, k=5, threshold=0.6)` → top-k chunks from Qdrant
  - `synthesize_answer(question, context_chunks, model, api_key)` → LLM call to OpenRouter with prompt:
    ```
    You are a helpful assistant answering questions about a book.
    Use ONLY the provided book excerpts to answer.
    If the excerpts don't contain enough info, say: "I didn't find this in the book, but..."

    Book excerpts:
    {context}

    Question: {question}

    Answer:
    ```

**Data Flow**:
```
question → OpenRouter embedding → embedding vector
embedding vector → Qdrant semantic search → top-k chunks + metadata
chunks + question → OpenRouter LLM → synthesis → answer
```

**Success Criteria**:
- ✅ `retrieve_similar_chunks("What is ROS 2?")` returns 5 chunks with relevance scores
- ✅ `synthesize_answer(...)` returns answer <3 seconds
- ✅ Answer includes citations (e.g., "In Chapter 3: ...")
- ✅ Unit tests pass: `pytest tests/test_rag.py`

**Effort**: 25 minutes

---

#### 1.4 FastAPI Endpoints (Step 6)

**Files**:
- `app/main.py` with routes:
  - `POST /query` → accept `{"question": "...", "selected_text": "..."}` → return `{"answer": "...", "sources": [...]}`
  - `POST /ingest` → accept PDF upload → call ingestion pipeline → return ingestion status
  - `GET /books` → list ingested books
  - `GET /health` → liveness check

**Request/Response Models** (`app/models.py`):
```python
class QueryRequest(BaseModel):
    question: str
    selected_text: Optional[str] = None
    book_id: str = "default"
    top_k: int = 5

class QueryResponse(BaseModel):
    answer: str
    sources: List[{"chunk_text": str, "page_num": int}]
    model: str
    timestamp: float
```

**Success Criteria**:
- ✅ `curl -X POST http://localhost:8001/query -H "Content-Type: application/json" -d '{"question": "What is...?"}'` returns JSON
- ✅ Response time <3 seconds
- ✅ Answer is from book (not hallucinated)
- ✅ Integration tests pass: `pytest tests/test_api.py`

**Effort**: 30 minutes

---

#### 1.5 Testing & Validation (Step 7)

**Test Structure**:
```python
# tests/test_api.py
@pytest.mark.asyncio
async def test_query_endpoint_returns_answer():
    client = TestClient(app)
    response = client.post("/query", json={"question": "...", "book_id": "test-book"})
    assert response.status_code == 200
    assert "answer" in response.json()
    assert len(response.json()["sources"]) > 0
```

**Success Criteria**:
- ✅ All tests pass: `pytest tests/`
- ✅ Mocked OpenRouter/Qdrant: no actual API calls during testing
- ✅ Coverage >80% for critical paths (retrieval, synthesis, endpoints)

**Effort**: 15 minutes

---

### Phase 1 Quick Success Criteria (Acceptance)

You should be able to run:

```bash
# 1. Start server
uvicorn app.main:app --port 8001 --reload

# 2. Ingest a book
python scripts/ingest_book.py --pdf path/to/book.pdf --book-id my-book

# 3. Query via curl
curl -X POST http://localhost:8001/query \
  -H "Content-Type: application/json" \
  -d '{"question": "What is the main topic of chapter 1?", "book_id": "my-book"}'

# Expected response:
{
  "answer": "In Chapter 1, the book introduces...",
  "sources": [
    {"chunk_text": "Chapter 1 begins with...", "page_num": 3}
  ],
  "model": "openai/gpt-4o-mini",
  "timestamp": 1704067200.0
}
```

**If answer comes from the actual book (not hallucinated), Phase 1 is complete! 🎉**

---

## Phase 2 Implementation Outline (Web Integration)

**Timeline**: 2-3 weeks | **Goal**: Embed chatbot in book pages via ChatKit

**Key Additions**:
- ChatKit web component wrapper (`frontend/src/chatbot-widget.js`)
- Session management (in-memory, auto-expire after 30 min)
- Optional Neon Postgres for session persistence (defer if in-memory sufficient)
- CORS/auth for cross-origin embedding
- Response streaming (Server-Sent Events)

**Not in Phase 1**: ChatKit integration, persistent sessions, selection-based context, analytics

---

## Phase 3+ Implementation Outline (Privacy & Advanced Features)

**Timeline**: 3+ weeks | **Goal**: Full feature parity with spec

**Key Additions**:
- Selection-based context handling (user highlights text → system uses as primary context)
- Privacy audit (verify zero data retention)
- Fallback to general knowledge (when Qdrant has no matches)
- Citation accuracy improvement (extract page ranges, chapter names)
- Rate limiting + abuse detection

---

## Design Decisions

| Decision | Rationale | Alternatives |
|----------|-----------|--------------|
| **FastAPI** not Django/Flask | Async-native, OpenAPI auto-docs, modern Python | Flask (slower), Django (overkill for Phase 1) |
| **Qdrant** not Pinecone/Weaviate | Free tier, open-source option, pgvector fallback | Pinecone ($$), Weaviate (complex setup) |
| **OpenRouter** not direct OpenAI | Model flexibility, cost optimization, routing | Direct OpenAI (vendor lock), Anthropic (single model) |
| **LangChain** for orchestration | Reduces boilerplate, community-tested patterns | Llama Index (less flexible), manual (more code) |
| **In-memory sessions (Phase 1)** not Postgres | Faster, no DB setup needed for MVP | Postgres (adds infrastructure, not needed yet) |
| **Chunking at 850 tokens** not 1024 | Leaves room for overlap (180 tokens), context window safety | 1024 (risky with follow-ups), 512 (less context) |

---

## Data Models

### Key Entities (Phase 1)

**Qdrant Payload Schema**:
```json
{
  "book_id": "string (identifier of book)",
  "chunk_id": "integer (sequential in book)",
  "chunk_text": "string (actual content)",
  "page_num": "integer (for citations)",
  "section_title": "string (optional: chapter name)"
}
```

**Python Models** (`app/models.py`):
```python
class Chunk(BaseModel):
    book_id: str
    chunk_id: int
    text: str
    page_num: int
    embedding: List[float]  # 1536 dims for text-embedding-3-small

class Message(BaseModel):
    role: Literal["user", "assistant"]
    content: str
    timestamp: float
    sources: List[dict]  # for assistant messages

class Session(BaseModel):
    session_id: str
    messages: List[Message]
    created_at: float
    expires_at: float
```

**Phase 2+ Additions** (Postgres Schema):
```sql
CREATE TABLE books (
  id SERIAL PRIMARY KEY,
  book_id VARCHAR(255) UNIQUE NOT NULL,
  title VARCHAR(255),
  author VARCHAR(255),
  created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE chunks (
  id SERIAL PRIMARY KEY,
  book_id VARCHAR(255),
  chunk_id INTEGER,
  chunk_text TEXT,
  page_num INTEGER,
  section_title VARCHAR(255),
  embedding vector(1536),
  FOREIGN KEY (book_id) REFERENCES books(book_id)
);
```

---

## Risk Analysis & Mitigation

| Risk | Impact | Probability | Mitigation |
|------|--------|-------------|-----------|
| **OpenRouter rate limit exceeded** | Queries blocked | Medium | Cache results, implement queue, use tier with higher limits |
| **Qdrant Free Tier quota exceeded** | Vector storage full | Medium | Monitor usage, implement pruning, upgrade tier |
| **Hallucination (LLM makes up answers)** | Loss of trust | High | Use strict prompting, require citations, fall back to "not in book" |
| **Slow embedding generation** | >3s response time | Medium | Batch embeddings, cache, use faster embedding model (text-embedding-3-small) |
| **Qdrant API downtime** | Service unavailable | Low | Graceful error response, local fallback to general knowledge |

---

## Success Metrics (Phase 1 Completion)

- ✅ All 7 development steps completed and tested
- ✅ Qdrant Cloud integration working (real cloud instance, not local)
- ✅ OpenRouter API calls working (embeddings + LLM)
- ✅ FastAPI server starts without errors
- ✅ `/query` endpoint returns real book answers (verified manually)
- ✅ Ingestion pipeline processes PDF → embeddings → storage successfully
- ✅ Unit + integration tests pass (>80% coverage)
- ✅ No secrets in git; `.env` safely isolated
