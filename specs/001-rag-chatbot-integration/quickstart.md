# Quickstart: RAG Chatbot Phase 1 MVP

**Goal**: Get a working RAG chatbot answering questions about your book in 2-3 hours

**Prerequisite Knowledge**:
- Python 3.10+
- Basic FastAPI concepts (not required, will be simple)
- PDF or text files for books

**Timeline**:
- Setup & Config: 15 minutes
- Testing Connections: 20 minutes
- Building Components: 2-3 hours
- Testing & Validation: 30 minutes
- **Total**: 3-4 hours for Phase 1 MVP

---

## Prerequisites

### 1. Get API Keys

#### Qdrant Cloud
1. Go to https://cloud.qdrant.io
2. Sign up (free tier)
3. Create a new cluster (default settings)
4. Copy the `QDRANT_URL` and `QDRANT_API_KEY` from credentials page

Example:
```
QDRANT_URL=https://260e542a-02d1-46bd-b397-f4420a6fb08b.us-east4-0.gcp.cloud.qdrant.io:6333
QDRANT_API_KEY=ey...
```

#### OpenRouter
1. Go to https://openrouter.ai
2. Sign up (free trial credits available)
3. Go to API Keys page
4. Copy your API key

Example:
```
OPENROUTER_API_KEY=sk-or-v1-acf1a7...
```

#### Book File
- Prepare a PDF or text file of a book you want to make queryable
- Place it in repo root: `book.pdf` or `book.txt`
- For testing, any ~100 page PDF works

### 2. Install Python & Dependencies

```bash
# Verify Python 3.10+
python --version

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Clone or create project directory
mkdir rag-book-chat
cd rag-book-chat

# Create requirements.txt (see below) and install
pip install -r requirements.txt
```

---

## Phase 1 Step-by-Step Implementation

### Step 1: Project Structure & Config (10 min)

**Create directory structure:**
```bash
mkdir -p app tests scripts docs
touch app/__init__.py
touch requirements.txt .env .gitignore
```

**requirements.txt**:
```
fastapi==0.115.0
uvicorn==0.32.0
qdrant-client==1.12.0
langchain==0.3.8
langchain-openai==0.2.2
python-dotenv==1.0.1
pypdf==5.1.0
tiktoken==0.8.0
pytest==7.4.3
pytest-asyncio==0.23.3
httpx==0.25.2
```

**.env.example** (commit this, but NOT .env):
```
QDRANT_URL=https://your-cluster-url:6333
QDRANT_API_KEY=your-key-here
OPENROUTER_API_KEY=sk-or-v1-...
COLLECTION_NAME=book_v1
CHUNK_SIZE=850
CHUNK_OVERLAP=180
EMBEDDING_MODEL=text-embedding-3-small
CHAT_MODEL=openai/gpt-4o-mini
APP_PORT=8001
```

**.gitignore**:
```
.env
__pycache__/
*.pyc
.pytest_cache/
.venv/
venv/
*.pdf
*.txt
dist/
build/
```

**app/config.py**:
```python
import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Qdrant
    QDRANT_URL = os.getenv("QDRANT_URL", "https://your-url:6333")
    QDRANT_API_KEY = os.getenv("QDRANT_API_KEY", "your-key")
    COLLECTION_NAME = os.getenv("COLLECTION_NAME", "book_v1")

    # OpenRouter
    OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY", "sk-or-v1-...")
    EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "text-embedding-3-small")
    CHAT_MODEL = os.getenv("CHAT_MODEL", "openai/gpt-4o-mini")

    # Book
    BOOK_PATH = Path(__file__).parent.parent / "book.pdf"
    CHUNK_SIZE = int(os.getenv("CHUNK_SIZE", "850"))
    CHUNK_OVERLAP = int(os.getenv("CHUNK_OVERLAP", "180"))

    # Server
    APP_PORT = int(os.getenv("APP_PORT", "8001"))
```

**Verify config loads**:
```bash
python -c "from app.config import Config; print(Config.QDRANT_URL)"
```

---

### Step 2: Test Qdrant Connection (10 min)

**scripts/test_qdrant_connection.py**:
```python
from qdrant_client import QdrantClient
from app.config import Config

def test_qdrant():
    try:
        client = QdrantClient(
            url=Config.QDRANT_URL,
            api_key=Config.QDRANT_API_KEY,
            timeout=5.0
        )

        # Test connection
        info = client.get_collection_names()
        print(f"✅ Qdrant connected! Collections: {info.collections}")

        # Try to create a test collection
        # (will fail if already exists, which is fine)
        try:
            client.recreate_collection(
                collection_name=f"{Config.COLLECTION_NAME}_test",
                vectors_config={
                    "size": 1536,
                    "distance": "Cosine"
                }
            )
            print(f"✅ Created test collection")
            client.delete_collection(f"{Config.COLLECTION_NAME}_test")
        except Exception as e:
            print(f"ℹ️  Test collection creation skipped: {e}")

        return True
    except Exception as e:
        print(f"❌ Qdrant connection failed: {e}")
        return False

if __name__ == "__main__":
    success = test_qdrant()
    exit(0 if success else 1)
```

**Run it**:
```bash
python scripts/test_qdrant_connection.py
```

Expected output: `✅ Qdrant connected!`

---

### Step 3: Test OpenRouter API (10 min)

**scripts/test_openrouter_api.py**:
```python
import requests
from app.config import Config

def test_embedding():
    """Test embedding via OpenRouter"""
    try:
        url = "https://openrouter.ai/api/v1/embeddings"
        headers = {
            "Authorization": f"Bearer {Config.OPENROUTER_API_KEY}",
            "Content-Type": "application/json"
        }
        data = {
            "model": Config.EMBEDDING_MODEL,
            "input": "What is ROS 2?"
        }

        response = requests.post(url, json=data, headers=headers, timeout=10)
        response.raise_for_status()

        embedding = response.json()["data"][0]["embedding"]
        print(f"✅ Embedding generated! Dimension: {len(embedding)}")
        return True
    except Exception as e:
        print(f"❌ Embedding failed: {e}")
        return False

def test_llm():
    """Test LLM inference via OpenRouter"""
    try:
        url = "https://openrouter.ai/api/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {Config.OPENROUTER_API_KEY}",
            "Content-Type": "application/json"
        }
        data = {
            "model": Config.CHAT_MODEL,
            "messages": [{"role": "user", "content": "Say 'Hello from RAG!'"}],
            "temperature": 0.7
        }

        response = requests.post(url, json=data, headers=headers, timeout=10)
        response.raise_for_status()

        message = response.json()["choices"][0]["message"]["content"]
        print(f"✅ LLM response: {message}")
        return True
    except Exception as e:
        print(f"❌ LLM call failed: {e}")
        return False

if __name__ == "__main__":
    print("Testing embedding...")
    emb_ok = test_embedding()
    print("\nTesting LLM...")
    llm_ok = test_llm()

    if emb_ok and llm_ok:
        print("\n✅ All OpenRouter tests passed!")
    exit(0 if (emb_ok and llm_ok) else 1)
```

**Run it**:
```bash
python scripts/test_openrouter_api.py
```

Expected output:
```
✅ Embedding generated! Dimension: 1536
✅ LLM response: Hello from RAG!
```

---

### Step 4: Implement Book Ingestion (45 min)

**app/ingestion.py**:
```python
from pathlib import Path
from typing import List
import logging
from PyPDF2 import PdfReader
from langchain.text_splitter import RecursiveCharacterTextSplitter
import requests
from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct
from app.config import Config

logger = logging.getLogger(__name__)

def load_pdf(file_path: Path) -> str:
    """Load PDF and extract text"""
    if not file_path.exists():
        raise FileNotFoundError(f"PDF not found: {file_path}")

    reader = PdfReader(file_path)
    text = ""
    for page_num, page in enumerate(reader.pages, 1):
        text += f"\n[Page {page_num}]\n"
        text += page.extract_text()

    return text

def chunk_text(text: str, chunk_size: int = 850, chunk_overlap: int = 180) -> List[dict]:
    """Split text into semantic chunks"""
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        separators=["\n\n", "\n", " ", ""]
    )

    chunks = splitter.split_text(text)

    # Add metadata
    result = []
    for chunk_id, chunk_text in enumerate(chunks):
        # Extract page number if present
        page_num = 1
        if "[Page" in chunk_text:
            try:
                page_num = int(chunk_text.split("[Page ")[1].split("]")[0])
            except:
                pass

        result.append({
            "chunk_id": chunk_id,
            "chunk_text": chunk_text,
            "page_num": page_num,
            "section_title": None
        })

    return result

def embed_chunks(chunks: List[dict], model: str, api_key: str) -> List[dict]:
    """Generate embeddings for chunks via OpenRouter"""
    url = "https://openrouter.ai/api/v1/embeddings"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    embedded_chunks = []

    for chunk in chunks:
        try:
            data = {
                "model": model,
                "input": chunk["chunk_text"][:1000]  # Limit to 1000 chars for embedding
            }

            response = requests.post(url, json=data, headers=headers, timeout=10)
            response.raise_for_status()

            embedding = response.json()["data"][0]["embedding"]

            chunk["embedding"] = embedding
            embedded_chunks.append(chunk)

            if len(embedded_chunks) % 10 == 0:
                print(f"Embedded {len(embedded_chunks)} chunks...")

        except Exception as e:
            logger.error(f"Failed to embed chunk {chunk['chunk_id']}: {e}")

    return embedded_chunks

def store_in_qdrant(
    chunks: List[dict],
    qdrant_url: str,
    api_key: str,
    collection_name: str,
    book_id: str = "default"
) -> bool:
    """Store embeddings in Qdrant"""
    try:
        client = QdrantClient(
            url=qdrant_url,
            api_key=api_key,
            timeout=10
        )

        # Create collection if not exists
        try:
            client.recreate_collection(
                collection_name=collection_name,
                vectors_config={
                    "size": 1536,
                    "distance": "Cosine"
                }
            )
            print(f"Created collection: {collection_name}")
        except:
            print(f"Collection {collection_name} already exists")

        # Create points
        points = [
            PointStruct(
                id=chunk["chunk_id"],
                vector=chunk["embedding"],
                payload={
                    "book_id": book_id,
                    "chunk_id": chunk["chunk_id"],
                    "chunk_text": chunk["chunk_text"],
                    "page_num": chunk["page_num"],
                    "section_title": chunk.get("section_title")
                }
            )
            for chunk in chunks
        ]

        # Upload to Qdrant
        client.upsert(
            collection_name=collection_name,
            points=points,
            wait=True
        )

        print(f"✅ Stored {len(points)} chunks in Qdrant")
        return True

    except Exception as e:
        logger.error(f"Failed to store in Qdrant: {e}")
        return False

def ingest_book(pdf_path: Path, book_id: str = "default") -> bool:
    """Full ingestion pipeline"""
    print(f"Ingesting {pdf_path}...")

    # Load
    print("1. Loading PDF...")
    text = load_pdf(pdf_path)
    print(f"   Loaded {len(text)} characters")

    # Chunk
    print("2. Chunking text...")
    chunks = chunk_text(text, Config.CHUNK_SIZE, Config.CHUNK_OVERLAP)
    print(f"   Created {len(chunks)} chunks")

    # Embed
    print("3. Generating embeddings...")
    chunks = embed_chunks(chunks, Config.EMBEDDING_MODEL, Config.OPENROUTER_API_KEY)
    print(f"   Embedded {len(chunks)} chunks")

    # Store
    print("4. Storing in Qdrant...")
    success = store_in_qdrant(
        chunks,
        Config.QDRANT_URL,
        Config.QDRANT_API_KEY,
        Config.COLLECTION_NAME,
        book_id
    )

    if success:
        print(f"\n✅ Ingestion complete! {len(chunks)} chunks stored.")
    return success
```

**Create ingest script**:
```bash
# scripts/ingest_book.py
if __name__ == "__main__":
    from app.ingestion import ingest_book
    from pathlib import Path
    import sys

    book_path = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("book.pdf")
    book_id = sys.argv[2] if len(sys.argv) > 2 else "default"

    ingest_book(book_path, book_id)
```

**Run ingestion**:
```bash
python scripts/ingest_book.py book.pdf my-book
```

Expected output:
```
Ingesting book.pdf...
1. Loading PDF...
   Loaded 523000 characters
2. Chunking text...
   Created 523 chunks
3. Generating embeddings...
   Embedded 523 chunks...
4. Storing in Qdrant...
✅ Ingestion complete! 523 chunks stored.
```

---

### Step 5: Implement RAG Retrieval & Synthesis (25 min)

**app/rag.py**:
```python
from typing import List, Tuple
import logging
import requests
from qdrant_client import QdrantClient
from app.config import Config

logger = logging.getLogger(__name__)

def retrieve_similar_chunks(
    question: str,
    book_id: str = "default",
    top_k: int = 5,
    threshold: float = 0.6
) -> List[dict]:
    """Retrieve chunks similar to the question"""

    # Embed the question
    url = "https://openrouter.ai/api/v1/embeddings"
    headers = {
        "Authorization": f"Bearer {Config.OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "model": Config.EMBEDDING_MODEL,
        "input": question
    }

    try:
        response = requests.post(url, json=data, headers=headers, timeout=10)
        response.raise_for_status()
        question_embedding = response.json()["data"][0]["embedding"]
    except Exception as e:
        logger.error(f"Failed to embed question: {e}")
        return []

    # Search Qdrant
    try:
        client = QdrantClient(
            url=Config.QDRANT_URL,
            api_key=Config.QDRANT_API_KEY,
            timeout=10
        )

        search_results = client.search(
            collection_name=Config.COLLECTION_NAME,
            query_vector=question_embedding,
            query_filter={
                "must": [
                    {
                        "key": "book_id",
                        "match": {"value": book_id}
                    }
                ]
            },
            limit=top_k
        )

        # Filter by threshold and format
        results = []
        for result in search_results:
            if result.score >= threshold:
                results.append({
                    "chunk_text": result.payload["chunk_text"],
                    "page_num": result.payload["page_num"],
                    "chunk_id": result.payload["chunk_id"],
                    "section_title": result.payload.get("section_title"),
                    "similarity_score": result.score
                })

        return results
    except Exception as e:
        logger.error(f"Failed to search Qdrant: {e}")
        return []

def synthesize_answer(
    question: str,
    context_chunks: List[dict],
    include_fallback: bool = True
) -> Tuple[str, bool]:
    """Synthesize answer using LLM"""

    if context_chunks:
        # Use book context
        context_text = "\n\n".join([
            f"[Page {c['page_num']}] {c['chunk_text']}"
            for c in context_chunks
        ])

        prompt = f"""You are a helpful assistant answering questions about a book.
Use ONLY the provided excerpts to answer the question.
If the excerpts don't contain enough information, say: "I didn't find sufficient information in the book about this."

Book excerpts:
{context_text}

Question: {question}

Answer:"""
    else:
        # No context, use general knowledge
        if not include_fallback:
            return "I couldn't find information about this in the book.", False

        prompt = f"""Answer this question based on general knowledge, but note that it's not from the book:

Question: {question}

Answer: Based on general knowledge (not from the book):"""

    try:
        url = "https://openrouter.ai/api/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {Config.OPENROUTER_API_KEY}",
            "Content-Type": "application/json"
        }
        data = {
            "model": Config.CHAT_MODEL,
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.7,
            "max_tokens": 500
        }

        response = requests.post(url, json=data, headers=headers, timeout=30)
        response.raise_for_status()

        answer = response.json()["choices"][0]["message"]["content"]
        is_fallback = len(context_chunks) == 0

        return answer, is_fallback
    except Exception as e:
        logger.error(f"Failed to synthesize: {e}")
        return f"Error generating answer: {e}", False
```

---

### Step 6: Build FastAPI Endpoints (30 min)

**app/models.py**:
```python
from pydantic import BaseModel, Field
from typing import List, Optional

class QueryRequest(BaseModel):
    question: str = Field(..., min_length=1, max_length=500)
    selected_text: Optional[str] = None
    book_id: str = "default"
    top_k: int = 5

class Source(BaseModel):
    chunk_text: str
    page_num: int
    chunk_id: int
    section_title: Optional[str] = None
    similarity_score: float

class QueryResponse(BaseModel):
    answer: str
    sources: List[Source]
    is_fallback: bool
    model: str
    latency_ms: float
    timestamp: float
```

**app/main.py**:
```python
import time
import logging
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from app.models import QueryRequest, QueryResponse, Source
from app.rag import retrieve_similar_chunks, synthesize_answer
from app.config import Config

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="RAG Chatbot API",
    version="1.0.0",
    description="Retrieval-Augmented Generation chatbot for digital books"
)

# CORS (needed for browser embedding in Phase 2)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Phase 2: restrict to specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/query", response_model=QueryResponse)
async def query_book(request: QueryRequest) -> QueryResponse:
    """Query the chatbot for information about a book"""
    start_time = time.time()

    try:
        # Retrieve relevant chunks
        chunks = retrieve_similar_chunks(
            question=request.question,
            book_id=request.book_id,
            top_k=request.top_k
        )

        # Synthesize answer
        answer, is_fallback = synthesize_answer(
            question=request.question,
            context_chunks=chunks
        )

        # Format sources
        sources = [
            Source(
                chunk_text=c["chunk_text"][:200] + "...",  # Truncate for response
                page_num=c["page_num"],
                chunk_id=c["chunk_id"],
                section_title=c.get("section_title"),
                similarity_score=c["similarity_score"]
            )
            for c in chunks
        ]

        latency_ms = int((time.time() - start_time) * 1000)

        return QueryResponse(
            answer=answer,
            sources=sources,
            is_fallback=is_fallback,
            model=Config.CHAT_MODEL,
            latency_ms=latency_ms,
            timestamp=time.time()
        )

    except Exception as e:
        logger.error(f"Query failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    """System health check"""
    return {
        "status": "healthy",
        "timestamp": time.time()
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=Config.APP_PORT)
```

---

### Step 7: Test Everything (30 min)

**Start the server**:
```bash
uvicorn app.main:app --port 8001 --reload
```

**Test via curl**:
```bash
curl -X POST http://localhost:8001/query \
  -H "Content-Type: application/json" \
  -d '{
    "question": "What is the main topic of chapter 1?",
    "book_id": "my-book",
    "top_k": 5
  }'
```

**Expected response**:
```json
{
  "answer": "In Chapter 1, the book introduces...",
  "sources": [
    {
      "chunk_text": "Chapter 1 begins with an overview of...",
      "page_num": 3,
      "chunk_id": 0,
      "section_title": null,
      "similarity_score": 0.89
    }
  ],
  "is_fallback": false,
  "model": "openai/gpt-4o-mini",
  "latency_ms": 2340,
  "timestamp": 1704067200.0
}
```

**Write basic tests** (`tests/test_api.py`):
```python
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"

def test_query_invalid():
    response = client.post("/query", json={"question": ""})
    assert response.status_code == 422  # Pydantic validation error

def test_query_valid(monkeypatch):
    # Mock Qdrant retrieval
    def mock_retrieve(*args, **kwargs):
        return [{
            "chunk_text": "Sample book text",
            "page_num": 1,
            "chunk_id": 0,
            "similarity_score": 0.9
        }]

    def mock_synthesize(*args, **kwargs):
        return "This is a test answer", False

    monkeypatch.setattr("app.rag.retrieve_similar_chunks", mock_retrieve)
    monkeypatch.setattr("app.rag.synthesize_answer", mock_synthesize)

    response = client.post("/query", json={"question": "Test?"})
    assert response.status_code == 200
    assert "answer" in response.json()
```

**Run tests**:
```bash
pytest tests/ -v
```

---

## Success Criteria (Phase 1 Completion)

✅ All done when:
1. Qdrant connection test passes
2. OpenRouter API tests pass (embedding + LLM)
3. Book ingestion completes (PDF → Qdrant)
4. FastAPI server starts without errors
5. `/query` endpoint returns real book answers (verified with `curl`)
6. Unit tests pass (`pytest`)
7. No API keys in git (`.env` ignored)

**If all green**, you've completed Phase 1! 🎉

---

## Next Steps (Phase 2+)

1. **Add ChatKit web component embedding** for book pages
2. **Implement session management** with auto-expiration
3. **Add selection-based context** (user highlights text)
4. **Optional**: Add Postgres for book metadata + analytics
5. **Optional**: Implement response streaming (Server-Sent Events)

---

## Troubleshooting

### "qdrant connection failed"
- Check QDRANT_URL and API_KEY in `.env`
- Verify internet connection
- Test endpoint manually: `curl -H "Authorization: Bearer $KEY" $QDRANT_URL/health`

### "Invalid API key" from OpenRouter
- Verify OPENROUTER_API_KEY in `.env`
- Ensure no extra whitespace
- Check OpenRouter dashboard for rate limits

### "PDF not found"
- Ensure `book.pdf` is in repo root
- Or pass full path: `python scripts/ingest_book.py /path/to/book.pdf`

### "Chunk embedding failed"
- Check internet connection
- Verify OpenRouter API quota
- Review ingestion logs for specific error

---

**You're ready! Start with Step 1 and follow through. Good luck! 🚀**
