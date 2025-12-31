# Research Phase Output: RAG Chatbot Integration

**Date**: 2025-12-30
**Feature**: RAG Chatbot for Digital Books
**Status**: Complete

## Summary

This document captures findings from research activities conducted to resolve technical ambiguities and validate technology choices for Phase 1 implementation.

---

## Technology Validations

### 1. Vector Database Selection

**Decision**: Qdrant Cloud Free Tier

**Rationale**:
- Free tier supports up to 1GB storage (~100,000 vectors for 1536-dim embeddings)
- Open-source alternative available (self-hosted fallback)
- Native support for scalar filters (book_id, page_num) + vector search
- REST API + Python client well-documented
- Cosine distance metric standard for text embeddings

**Alternatives Considered**:
- **Pinecone**: Managed, fully-hosted, but $0.25/day minimum + $0.08 per 100k vectors (exceeded budget)
- **Weaviate**: Open-source but requires docker-compose setup (deferred to Phase 2 for self-hosted option)
- **pgvector**: Free (PostgreSQL extension), but requires running Postgres (added complexity; deferred to Phase 2)
- **FAISS**: Local/CPU-based, no remote storage (won't work for team collaboration in Phase 2+)

**Best Practices Applied**:
- Use 1536-dim embeddings (text-embedding-3-small standard)
- Index payload metadata (book_id, chunk_id) for filtering
- Monitor Free Tier usage dashboard monthly
- Plan migration path to Qdrant Self-Hosted or Enterprise if quota exceeded

---

### 2. LLM Provider & API Routing

**Decision**: OpenRouter API for all LLM calls (no direct OpenAI)

**Rationale**:
- Supports model switching (OpenAI GPT-4o-mini, Claude 3.5 Sonnet, Gemini, open-source)
- Cost optimization: cheaper models available (Gemini 2.0 Flash $0.05 per 1M tokens vs GPT-4 $0.15)
- Single API key and endpoint (simplifies code)
- LangChain's langchain-openai library supports custom base_url (OpenRouter)
- No vendor lock-in

**Embedding Model**: text-embedding-3-small
- 1536 dimensions (optimal for semantic search)
- $0.02 per 1M tokens (very cheap)
- Fast (~100ms per call)

**LLM Model (Phase 1)**: openai/gpt-4o-mini
- Excellent reasoning, good context handling
- $0.15 per 1M input + $0.60 per 1M output tokens
- Response time: 1-2 seconds typically

**Alternatives Considered**:
- **Direct OpenAI API**: Vendor lock-in, no cost optimization
- **Anthropic Claude**: Single model, must switch providers if costs spike
- **Local models (Llama 2)**: GPU required, latency issues, insufficient context for RAG

**Best Practices Applied**:
- Implement OpenRouter client wrapper (easy model switching)
- Use streaming for LLM responses (real-time feedback to user)
- Batch embedding requests where possible
- Monitor token usage via OpenRouter dashboard

---

### 3. Embedding Strategy & Chunking

**Decision**: Semantic chunking (LangChain RecursiveCharacterTextSplitter) with 850 tokens per chunk, 180 token overlap

**Rationale**:
- Splits on paragraph/sentence boundaries (preserves meaning)
- 850 tokens = ~3,400 characters (typical paragraph)
- 180-token overlap (21% overlap) ensures no context loss
- Allows follow-up questions (overlap provides continuity)

**Alternative Chunking Strategies**:
- **Fixed-size (1024 tokens)**: Simple but may split mid-sentence
- **Sentence-based**: Too granular, loses paragraph context
- **Section-based (chapters)**: Too coarse, overloaded chunks

**Validation**:
- Test on actual Physical AI book (confirm chunks are coherent)
- Monitor embedding quality via cosine similarity scores
- Adjust chunk_size if queries frequently miss relevant sections

**Best Practices Applied**:
- Use LangChain's RecursiveCharacterTextSplitter (nested: paragraphs → sentences → chars)
- Store chunk_text in Qdrant payload for citation/display
- Reserve context window: 850 tokens chunk + 180 token overlap leaves room for LLM synthesis

---

### 4. FastAPI + Async Architecture

**Decision**: FastAPI with uvicorn ASGI server, async endpoints

**Rationale**:
- Native async support (non-blocking I/O for Qdrant, OpenRouter calls)
- Automatic OpenAPI documentation
- Type hints + Pydantic validation (reduces bugs)
- Excellent performance (comparable to Node.js)
- Built-in dependency injection (clean code)

**Performance Expectations**:
- Single endpoint can handle ~500 requests/second (with 4-8 workers)
- Typical request latency: 1.5-3 seconds (embedding + retrieval + synthesis)
- Throughput for Phase 1: 1000+ queries/day easily

**Alternatives Considered**:
- **Flask**: Synchronous, requires threading/async workarounds
- **Django**: Overkill for single-purpose API, slower startup
- **Node.js/Express**: Unnecessary language switch, loss of LangChain benefits

**Best Practices Applied**:
- Use async/await for all I/O operations
- Implement connection pooling for Qdrant client
- Add request/response logging for debugging
- Rate limiting via middleware (Phase 2)

---

### 5. Database Strategy (Metadata Storage)

**Decision (Phase 1)**: In-memory Python dicts for sessions; defer Postgres to Phase 2

**Decision (Phase 2+)**: Neon Serverless Postgres for book metadata + optional session logs

**Rationale**:
- Phase 1: In-memory is sufficient (MVP, no multi-process deployment)
- Phase 2: Neon Free Tier provides 0.5 project, no storage cost
- Postgres enables future analytics, session persistence, user profiles

**Schema Design** (Phase 2):
```sql
CREATE TABLE books (
  id SERIAL PRIMARY KEY,
  book_id VARCHAR(255) UNIQUE NOT NULL,
  title VARCHAR(255),
  author VARCHAR(255),
  uploaded_at TIMESTAMP DEFAULT NOW(),
  chunk_count INTEGER
);

CREATE TABLE chunks (
  id SERIAL PRIMARY KEY,
  book_id VARCHAR(255),
  chunk_id INTEGER,
  chunk_text TEXT NOT NULL,
  page_num INTEGER,
  section_title VARCHAR(255),
  created_at TIMESTAMP DEFAULT NOW(),
  FOREIGN KEY (book_id) REFERENCES books(book_id),
  INDEX idx_book_chunk (book_id, chunk_id)
);
```

**Best Practices Applied**:
- Denormalize chunk_text in Postgres (avoid extra lookups)
- Use Qdrant for vector search (faster than pgvector for Phase 1)
- Plan migration to pgvector + hybrid search if Qdrant quota exceeded

---

### 6. Testing Strategy

**Decision**: pytest + pytest-asyncio for unit/integration tests; mock external APIs

**Rationale**:
- pytest is industry standard for Python
- pytest-asyncio handles async test functions
- Mocking reduces external API calls (faster tests, no rate limits)
- TestClient from FastAPI allows in-memory endpoint testing

**Test Coverage Goals**:
- Unit tests: Ingestion (chunking, embedding), RAG (retrieval, synthesis) — >80%
- Integration tests: FastAPI endpoints — >70%
- E2E tests: Real Qdrant + OpenRouter (manual, weekly)

**Alternatives Considered**:
- **unittest**: Verbose, requires more boilerplate than pytest
- **Hypothesis**: Property-based testing (overkill for Phase 1)

**Best Practices Applied**:
- Fixture-based mocks for Qdrant/OpenRouter responses
- Isolated test cases (no shared state)
- Parameterized tests for multiple chunk sizes, models
- CI/CD ready (can integrate with GitHub Actions)

---

### 7. Session Management (Privacy)

**Decision**: In-memory sessions with UUID, auto-expire after 30 minutes

**Rationale**:
- No persistent user data (privacy compliance)
- UUID prevents session hijacking
- 30-minute expiration balances UX (long enough for typical reading sessions) + privacy
- Python dict with background cleanup task

**Implementation Details**:
```python
# In-memory session store
SESSIONS: Dict[str, Session] = {}

@app.on_event("startup")
async def cleanup_expired_sessions():
    while True:
        now = time.time()
        expired = [sid for sid, sess in SESSIONS.items() if now > sess.expires_at]
        for sid in expired:
            del SESSIONS[sid]
        await asyncio.sleep(60)  # Check every minute
```

**Alternatives Considered**:
- **Redis**: Overkill for Phase 1, adds infrastructure
- **Postgres sessions**: Defeats privacy goal (persistent data)
- **JWT tokens**: Stateless but doesn't solve data retention issue

**Best Practices Applied**:
- No query logs or user identifiers stored
- Explicit session expiration (no stale data lingering)
- Clear conversation history on session close

---

### 8. Error Handling & Fallback Strategy

**Decision**: Graceful degradation with "Not in book" fallback

**Rationale**:
- If Qdrant search returns low-relevance results (<0.6 cosine similarity), trigger fallback
- Fallback: Use LLM general knowledge with explicit disclaimer
- If OpenRouter unavailable: Cached responses (Phase 2) or error message
- If Qdrant unavailable: Return error (cannot query without vectors)

**Implementation**:
```python
def synthesize_answer(question: str, chunks: List[dict], llm_client) -> dict:
    if not chunks or max([c["score"] for c in chunks]) < RELEVANCE_THRESHOLD:
        return {
            "answer": llm_client.call("Answer without book context...",
                                      disclaimer="Not in book."),
            "sources": [],
            "is_fallback": True
        }
    return {
        "answer": llm_client.call("Use provided excerpts..."),
        "sources": chunks,
        "is_fallback": False
    }
```

**Best Practices Applied**:
- Explicit relevance threshold (configurable)
- Disclaimer clearly indicates fallback answer
- Monitor fallback rate (if >50%, improve chunking/retrieval)

---

## API Design Decisions

### Query Endpoint (`POST /query`)

**Request**:
```json
{
  "question": "What is ROS 2?",
  "selected_text": "optional user-selected passage",
  "book_id": "robotics-book-v1",
  "top_k": 5
}
```

**Response**:
```json
{
  "answer": "ROS 2 is...",
  "sources": [
    {"chunk_text": "...", "page_num": 42, "chunk_id": 15}
  ],
  "is_fallback": false,
  "model": "openai/gpt-4o-mini",
  "latency_ms": 2340,
  "timestamp": 1704067200
}
```

**Rationale**:
- `selected_text`: Enables Phase 2 feature (selection-based context)
- `top_k`: Allows tuning retrieval depth (trade-off: precision vs. context)
- `sources`: Enable citations + transparency
- `is_fallback`: Distinguish general knowledge from book answers
- `latency_ms`: Monitor performance degradation

**Alternatives Considered**:
- **GET /query?question=...**: POST is safer for sensitive queries, handles large text
- **WebSocket**: Needed only for streaming (Phase 2)

---

## Dependency Management

### Required Packages (Phase 1)

| Package | Version | Reason | Risk |
|---------|---------|--------|------|
| fastapi | 0.115+ | ASGI web framework | Low (stable) |
| uvicorn | 0.32+ | ASGI server | Low (stable) |
| qdrant-client | 1.12+ | Vector DB client | Low (maintained) |
| langchain | 0.3.8 | RAG orchestration | Medium (rapid changes) |
| langchain-openai | 0.2.2 | Custom base_url support | Medium (rapid changes) |
| pypdf | 5.1+ | PDF parsing | Low (stable) |
| python-dotenv | 1.0+ | Config management | Low (stable) |
| tiktoken | 0.8+ | Token counting | Low (stable) |
| pytest | Latest | Testing framework | Low (stable) |
| pytest-asyncio | Latest | Async test support | Low (stable) |

**Risk Mitigation**:
- Pin exact versions in requirements.txt (reproducibility)
- Monitor LangChain releases (frequent updates); test before upgrading
- Use virtual environment (avoid system Python conflicts)

---

## Cost Estimation (Monthly)

**Assumptions**:
- 1000 queries/day = 30,000 queries/month
- Average 5 chunks retrieved per query
- Qdrant Free Tier: 1GB storage free
- Neon Free Tier: 0.5 project free (Phase 2)

| Component | Cost | Notes |
|-----------|------|-------|
| **OpenRouter Embeddings** | $0.60 | 30,000 queries × 5 chunks = 150k tokens @ $0.02/1M |
| **OpenRouter LLM (gpt-4o-mini)** | $4.50 | Input: 150k tokens; Output: 300k tokens (avg 10 tokens) |
| **Qdrant Cloud Free** | $0 | 1GB free (3 books × 100 chunks sufficient) |
| **Neon Postgres Free** | $0 | 0.5 project free (Phase 2) |
| **Total** | **$5.10** | Ultra-low cost MVP |

**Upgrade Path**:
- If 1GB Qdrant storage exceeded → Self-host Qdrant (free) or upgrade tier ($50-200/mo)
- If OpenRouter costs spike → Switch to cheaper model (Claude 3 Haiku)

---

## Security Considerations

### Data Privacy

- **Session data**: Ephemeral, auto-expiring, no persistence ✅
- **Query logging**: Optional (Phase 2), user-controlled ✅
- **API keys**: Environment variables, never logged ✅
- **HTTPS/TLS**: Enforce in production (Phase 2) ✅

### Input Validation

- Pydantic models validate request types + max lengths ✅
- Rate limiting (Phase 2) prevents abuse ✅
- PDF parsing sanitized (PyPDF handles malformed files) ✅

### Third-Party API Security

- OpenRouter key never exposed to frontend (all calls from backend) ✅
- Qdrant API key stored as env var ✅
- Use HTTPS for all API calls ✅

---

## Performance Benchmarks (Expected)

**Single Query (typical)**:
- PDF ingestion: 50ms (PyPDF parsing)
- Chunk embedding: 500ms (OpenRouter embedding API)
- Qdrant search: 50ms (vector search)
- LLM synthesis: 2000ms (OpenRouter LLM call)
- Total: ~2.6 seconds

**Bottlenecks**:
- LLM synthesis dominates (~75% of latency)
- Batch embeddings during ingestion (faster)
- Use streaming LLM responses (Phase 2) for perceived speed

**Scaling Capacity**:
- FastAPI: 500+ concurrent requests on single worker
- Qdrant Free Tier: Up to ~100k vectors
- OpenRouter: Rate limits depend on plan (typically 100k tokens/min for free)

---

## Future Considerations (Post-MVP)

1. **Fine-tuned Embeddings**: Train on Physics/AI textbooks for domain-specific retrieval
2. **Hybrid Search**: Combine vector + keyword search (pgvector + full-text search)
3. **Query Expansion**: Rephrase question before embedding (multi-turn reasoning)
4. **Batch Processing**: Async job queue for bulk ingestion
5. **Analytics**: Track query patterns, user feedback (opt-in)
6. **Multi-language**: Support non-English books + queries
7. **Real-time Updates**: Hot-reload books without downtime

---

## Conclusion

All major technical decisions have been validated through research. No unresolved clarifications remain. Phase 1 implementation can proceed with high confidence in technology stack alignment and cost efficiency.

**Next Step**: Generate task list via `/sp.tasks` for Phase 1 implementation.
