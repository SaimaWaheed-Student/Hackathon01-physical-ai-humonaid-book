# Data Model: RAG Chatbot Integration

**Date**: 2025-12-30
**Feature**: RAG Chatbot for Digital Books
**Phase**: 1 (MVP) + 2+ Planning

---

## Entity Relationship Diagram (Phase 1)

```
┌─────────────────┐
│   Book (File)   │
│  - title        │
│  - author       │
│  - format       │
│  - path         │
└────────┬────────┘
         │
         │ contains 100+
         │
         ▼
┌──────────────────────────┐         ┌──────────────────┐
│  Chunk (In Qdrant)       │         │ Session (In-Mem) │
│ - book_id       (key)    │         │ - session_id     │
│ - chunk_id      (key)    │         │ - messages[]     │
│ - chunk_text             │         │ - created_at     │
│ - page_num               │         │ - expires_at     │
│ - section_title          │         └──────────────────┘
│ - embedding (1536-dim)   │              │
└──────────────────────────┘              │
                                          │
                        ┌─────────────────▼─────────────────┐
                        │   Message (In-Mem, per Session)   │
                        │ - role ("user" | "assistant")     │
                        │ - content (text)                  │
                        │ - timestamp                       │
                        │ - sources[] (for citations)       │
                        └─────────────────────────────────────┘
```

---

## Phase 1 Entities (MVP)

### 1. Book (Metadata)

**Source**: File system (PDF)
**Storage**: In-memory during ingestion, then discarded
**Purpose**: Represent a book being ingested

```python
@dataclass
class Book:
    title: str              # "Physical AI and Humanoid Robotics"
    author: str             # "Author Name"
    file_path: Path         # /path/to/book.pdf
    format: Literal["pdf", "txt"]
    total_pages: int        # For page number tracking
    total_chunks: int       # After ingestion complete
    created_at: float       # Timestamp when ingested
```

**Validation Rules**:
- file_path must exist and be readable
- format must be pdf or txt
- total_pages > 0

**State Transitions**:
- NEW → INGESTING → COMPLETE → ERROR (with retry)

---

### 2. Chunk (Vector + Metadata)

**Source**: Book splitting + embedding
**Storage**: Qdrant Cloud (vector DB)
**Purpose**: Atomic unit of book content for RAG retrieval

```python
@dataclass
class Chunk:
    book_id: str                    # "robotics-book-v1"
    chunk_id: int                   # 0, 1, 2, ... (sequential)
    chunk_text: str                 # 850 tokens of actual content
    page_num: int                   # For citations (1-indexed)
    section_title: Optional[str]    # "Chapter 3: Navigation"
    embedding: List[float]          # 1536-dimensional vector
    token_count: int                # Actual tokens in chunk
    similarity_score: Optional[float] = None  # Set during retrieval
```

**Validation Rules**:
- chunk_text length: 500–2000 characters
- token_count should match tiktoken count of chunk_text
- page_num > 0
- embedding length == 1536 (for text-embedding-3-small)

**Qdrant Payload Schema** (stored alongside vector):
```json
{
  "book_id": {
    "type": "keyword"
  },
  "chunk_id": {
    "type": "integer"
  },
  "chunk_text": {
    "type": "text"
  },
  "page_num": {
    "type": "integer"
  },
  "section_title": {
    "type": "keyword"
  },
  "token_count": {
    "type": "integer"
  }
}
```

**Index Strategy**:
- Vector index: Cosine distance (standard for text embeddings)
- Payload filters: book_id (for multi-book queries)
- No full-text search in Phase 1 (deferred to Phase 2)

---

### 3. QueryResult (Retrieval Output)

**Source**: Qdrant search
**Storage**: In-memory, returned to user
**Purpose**: Represent chunks retrieved during RAG

```python
@dataclass
class QueryResult:
    chunk: Chunk
    similarity_score: float         # 0.0–1.0 (cosine similarity)
    rank: int                       # 1, 2, 3, ... (top-k order)
```

**Validation Rules**:
- similarity_score >= 0.0 and <= 1.0
- rank >= 1

**Usage**:
```python
results: List[QueryResult] = retrieve_similar_chunks(
    question="What is ROS 2?",
    book_id="robotics-book",
    top_k=5,
    min_score=0.6
)
# Returns top 5 chunks with similarity >= 0.6
```

---

### 4. Message (Session Conversation)

**Source**: User queries + LLM responses
**Storage**: In-memory (session dict), discarded on expiration
**Purpose**: Represent one turn in a conversation

```python
@dataclass
class Message:
    role: Literal["user", "assistant"]
    content: str                    # Query text or LLM response
    timestamp: float                # Unix timestamp
    sources: List[Chunk] = None     # For assistant messages (citations)
    tokens: int = None              # Token count (for budget tracking)
```

**Validation Rules**:
- role must be "user" or "assistant"
- content length: 1–10,000 characters
- timestamp must be valid Unix time
- sources (if present) must be non-empty list

**State Transitions** (per message):
- NEW → CREATED → SENT → (deleted on session expiration)

---

### 5. Session (Conversation Context)

**Source**: Client request (implicit via UUID)
**Storage**: In-memory Python dict
**Purpose**: Maintain conversation history + context for a user

```python
@dataclass
class Session:
    session_id: str                 # UUID, unique per user session
    messages: List[Message]         # Conversation history
    book_id: str                    # Current book being queried
    created_at: float               # Unix timestamp
    expires_at: float               # created_at + 30 minutes
    last_activity: float            # Updated on each message
```

**Validation Rules**:
- session_id must be unique (UUID4)
- messages list preserves order
- expires_at = created_at + 1800 (30 minutes)

**State Transitions** (per session):
- NEW → ACTIVE → EXPIRED (auto-cleanup every 1 minute)

**In-Memory Implementation**:
```python
# Globally maintained session store
SESSIONS: Dict[str, Session] = {}

# Access pattern:
if session_id in SESSIONS:
    session = SESSIONS[session_id]
    session.messages.append(new_message)
    session.last_activity = time.time()
```

**Cleanup Task** (background):
```python
@app.on_event("startup")
async def cleanup_expired_sessions():
    while True:
        now = time.time()
        expired = [
            sid for sid, sess in SESSIONS.items()
            if now > sess.expires_at
        ]
        for sid in expired:
            del SESSIONS[sid]  # Purge entire session
            print(f"Purged session {sid}")
        await asyncio.sleep(60)  # Check every minute
```

**Privacy Guarantee**: Once deleted, zero traces remain (no logs, no DB records, no caches).

---

## Phase 2+ Entities (Additions)

### 6. BookRecord (Postgres)

**Storage**: Neon Serverless Postgres
**Purpose**: Persistent metadata for ingested books

```python
@dataclass
class BookRecord:
    id: int                         # PK, auto-increment
    book_id: str                    # "robotics-book-v1", UNIQUE
    title: str
    author: str
    file_format: str                # "pdf" or "txt"
    uploaded_at: datetime
    chunk_count: int                # Total chunks in Qdrant
    embedding_model: str            # "text-embedding-3-small"
```

**SQL Schema**:
```sql
CREATE TABLE books (
    id SERIAL PRIMARY KEY,
    book_id VARCHAR(255) UNIQUE NOT NULL,
    title VARCHAR(255) NOT NULL,
    author VARCHAR(255),
    file_format VARCHAR(10) NOT NULL,
    uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    chunk_count INTEGER DEFAULT 0,
    embedding_model VARCHAR(100) DEFAULT 'text-embedding-3-small',
    INDEX idx_book_id (book_id)
);
```

**Relationships**:
- One Book → Many Chunks (in Qdrant)

---

### 7. ChunkRecord (Postgres)

**Storage**: Neon Serverless Postgres (denormalized for lookups)
**Purpose**: Persistent mapping of chunks + embedding vectors (pgvector Phase 2.5+)

```sql
CREATE TABLE chunks (
    id SERIAL PRIMARY KEY,
    book_id VARCHAR(255) NOT NULL,
    chunk_id INTEGER NOT NULL,
    chunk_text TEXT NOT NULL,
    page_num INTEGER,
    section_title VARCHAR(255),
    token_count INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    -- Phase 2.5: Add pgvector column for hybrid search
    -- embedding vector(1536),
    FOREIGN KEY (book_id) REFERENCES books(book_id),
    UNIQUE (book_id, chunk_id),
    INDEX idx_book_chunk (book_id, chunk_id)
);
```

**Purpose**: Backup + audit trail; enable full-text search (Phase 2)

---

### 8. SessionLog (Optional, Phase 2+)

**Storage**: Neon Serverless Postgres
**Purpose**: Audit trail + analytics (opt-in, privacy-conscious)

```sql
CREATE TABLE session_logs (
    id SERIAL PRIMARY KEY,
    session_id VARCHAR(36),  -- UUID
    book_id VARCHAR(255),
    query_count INTEGER,
    created_at TIMESTAMP,
    expires_at TIMESTAMP,
    is_completed BOOLEAN DEFAULT FALSE,
    INDEX idx_session (session_id)
);
```

**Privacy Note**: Intentionally does NOT store actual queries or responses. Only session metadata.

---

## Data Validation Rules (Global)

### Input Validation

| Field | Type | Constraints | Example |
|-------|------|-------------|---------|
| question | str | 1–500 chars | "What is ROS 2?" |
| selected_text | str (optional) | 0–5000 chars | "The robotics operating system..." |
| book_id | str | 1–100 chars, alphanumeric | "robotics-book-v1" |
| top_k | int | 1–20 | 5 |
| page_num | int | 1–10000 | 42 |
| similarity_score | float | 0.0–1.0 | 0.85 |
| timestamp | float | Unix time, recent | 1704067200.0 |

### Business Logic Validation

**Chunk Validity**:
- chunk_text length >= 100 chars (minimum context)
- chunk_text length <= 5000 chars (maximum)
- token_count matches actual token count (via tiktoken)
- page_num is within book's total_pages

**Query Validity**:
- question is non-empty and non-spam
- book_id exists in loaded books
- top_k <= total chunks in book
- similarity_score threshold (0.6 default) is reasonable

**Session Validity**:
- session_id is valid UUID4
- created_at <= last_activity <= expires_at (chronological order)
- messages list preserves ordering
- No duplicate session_ids

---

## State Machines

### Chunk Ingestion State

```
PDF File
   │
   ├─ PARSING ──(50ms)─► TEXT
   │
   ├─ CHUNKING ──(100ms)─► CHUNKS
   │
   ├─ EMBEDDING ──(500ms per batch)─► EMBEDDED_CHUNKS
   │
   ├─ STORING ──(100ms)─► QDRANT (✓ Complete)
   │
   └─ ERROR ──(retry mechanism)─► FAILED (manual intervention)
```

### Query Processing State

```
Client Request (session_id, question)
   │
   ├─ VALIDATING ──(10ms)─► VALID
   │
   ├─ EMBEDDING_QUERY ──(100ms)─► QUERY_EMBEDDING
   │
   ├─ SEARCHING ──(50ms)─► RESULTS (top-k)
   │
   ├─ SYNTHESIZING ──(2000ms)─► ANSWER
   │
   └─ RESPONSE ──(serialize)─► JSON (✓ Complete)
```

### Session State

```
NEW (created on first request)
   │
   ├─ ACTIVE (accepts new messages)
   │  └─ LAST_ACTIVITY updated on each message
   │
   └─ EXPIRED (after 30 min inactivity)
      └─ PURGED (auto-deleted, zero recovery)
```

---

## Error Handling & Edge Cases

### Data Integrity

| Scenario | Handling |
|----------|----------|
| Chunk with mismatched token count | Log warning, use actual token count (trust tiktoken) |
| Similarity score outside 0.0–1.0 | Clamp to valid range, log anomaly |
| Null/missing page_num | Default to -1 (unknown page) |
| Session expired but query received | Reject with 401 (session expired), user starts new session |
| Qdrant unavailable | Return 503 with fallback message |
| PDF corrupted/unreadable | Fail gracefully, return error to admin |

### Validation Errors

```python
# Pydantic will raise ValidationError for:
try:
    result = QueryRequest(
        question="",  # Empty! Fails validation
        book_id="robotics-book"
    )
except ValidationError as e:
    return {"error": str(e), "status": 400}
```

---

## Migration Path (Phase 1 → 2)

**Phase 1 Data**: Ephemeral (sessions, in-memory chunks during ingestion)

**Phase 2 Data**: Persistent (BookRecord, ChunkRecord, optional SessionLog)

**Migration Strategy**:
1. Create Postgres schema (books, chunks, session_logs tables)
2. On next book ingestion, write to both Qdrant + Postgres
3. On session expiration, optionally write SessionLog (metadata only)
4. No data loss: Qdrant remains source-of-truth for vectors

---

## Conclusion

This data model supports Phase 1 MVP with in-memory sessions and cloud Qdrant storage. Clear relationships and validation rules ensure data integrity. Phase 2 adds persistent storage (Postgres) while maintaining privacy (no query logs, only metadata). Future hybrid search (Phase 2.5) will leverage both Qdrant vectors + pgvector with full-text search for better retrieval accuracy.
