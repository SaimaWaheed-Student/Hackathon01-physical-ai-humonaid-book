---
description: "Implementation task list for RAG Chatbot Integration"
---

# Tasks: RAG Chatbot Integration for Digital Books

**Input**: Design documents from `specs/001-rag-chatbot-integration/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

**Branch**: `001-rag-chatbot-integration`
**Status**: Ready for implementation
**Test Strategy**: Optional; include contract tests for API endpoints

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure for RAG Chatbot backend

- [x] T001 Create project directory structure per implementation plan in `rag-book-chat/`
- [x] T002 [P] Create `requirements.txt` with pinned dependencies (FastAPI, Qdrant, LangChain, OpenRouter, PyPDF, python-dotenv, tiktoken, pytest)
- [x] T003 [P] Create `app/__init__.py` and initialize Python package
- [x] T004 [P] Create `.gitignore` with patterns for Python, __pycache__, .env, .pytest_cache, venv/, *.pdf, *.txt
- [x] T005 Create `.env.example` template with all required environment variables (QDRANT_URL, QDRANT_API_KEY, OPENROUTER_API_KEY, COLLECTION_NAME, etc.)

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [x] T006 Create configuration management in `app/config.py` with Config class loading all env vars (QDRANT_URL, QDRANT_API_KEY, OPENROUTER_API_KEY, COLLECTION_NAME, CHUNK_SIZE=850, CHUNK_OVERLAP=180, EMBEDDING_MODEL, CHAT_MODEL, APP_PORT)
- [x] T007 Create FastAPI application skeleton in `app/main.py` with CORS middleware and basic /health endpoint
- [x] T008 Create Pydantic models in `app/models.py` (QueryRequest, QueryResponse, Source model with all fields from spec)
- [x] T009 [P] Create API connection validation script in `scripts/test_qdrant_connection.py` to verify Qdrant Cloud connectivity
- [x] T010 [P] Create API connection validation script in `scripts/test_openrouter_api.py` to verify OpenRouter embedding and LLM endpoints

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Ask Questions About Entire Book Content (Priority: P1) 🎯 MVP

**Goal**: Enable readers to ask questions about entire book content and receive answers synthesized from relevant sections

**Independent Test**: Ingest a complete book, ask a cross-chapter question, verify chatbot retrieves and synthesizes sections from multiple parts, validating answer accuracy and comprehensiveness

### Implementation for User Story 1

- [x] T011 [P] [US1] Create book ingestion pipeline in `app/ingestion.py` with `load_pdf(path)` function using PyPDF to extract text from PDF files
- [x] T012 [P] [US1] Create chunking function `chunk_text(text, chunk_size=850, chunk_overlap=180)` in `app/ingestion.py` using LangChain RecursiveCharacterTextSplitter with semantic boundaries
- [x] T013 [P] [US1] Create embedding function `embed_chunks(chunks, model, api_key)` in `app/ingestion.py` calling OpenRouter embedding API and returning embeddings
- [x] T014 [P] [US1] Create Qdrant storage function `store_in_qdrant(chunks, qdrant_url, api_key, collection_name, book_id)` in `app/ingestion.py` to create collection and upsert vectors with metadata
- [x] T015 [US1] Create full ingestion pipeline function `ingest_book(pdf_path, book_id)` in `app/ingestion.py` orchestrating load → chunk → embed → store
- [x] T016 [P] [US1] Create retrieval function `retrieve_similar_chunks(question, book_id, top_k=5, threshold=0.6)` in `app/rag.py` to embed question via OpenRouter and search Qdrant
- [x] T017 [P] [US1] Create synthesis function `synthesize_answer(question, context_chunks)` in `app/rag.py` to call OpenRouter LLM with book excerpts and return answer with fallback handling
- [x] T018 [US1] Create `/query` POST endpoint in `app/main.py` accepting QueryRequest, calling retrieval and synthesis, returning QueryResponse with sources and latency
- [x] T019 [P] [US1] Create CLI ingestion script in `scripts/ingest_book.py` to load PDF from command line and run ingestion pipeline
- [x] T020 [US1] Add logging throughout ingestion and RAG pipeline for debugging and monitoring in `app/ingestion.py` and `app/rag.py`
- [x] T021 [US1] Create unit tests for ingestion pipeline in `tests/test_ingestion.py` (chunking, page number extraction, validation)
- [x] T022 [US1] Create unit tests for RAG pipeline in `tests/test_rag.py` (retrieval with mocked Qdrant, synthesis with mocked OpenRouter)
- [x] T023 [US1] Create integration tests for `/query` endpoint in `tests/test_api.py` with mocked external services

**Checkpoint**: User Story 1 should be fully functional and testable independently - can ingest book and answer questions

---

## Phase 4: User Story 2 - Query Based on Selected Text (Priority: P1)

**Goal**: Support user-initiated text selection as primary context for queries, with optional supplementary full-book search

**Independent Test**: Select specific text passage, submit query with selection as context, verify system uses selection as primary context and provides targeted answers

### Implementation for User Story 2

- [x] T024 [P] [US2] Extend QueryRequest model in `app/models.py` to include `selected_text` optional field (already in models)
- [x] T025 [US2] Implement selection context logic in `app/rag.py` - modify `retrieve_similar_chunks()` to prioritize selected_text if provided before full-book search
- [x] T026 [US2] Update `synthesize_answer()` in `app/rag.py` to handle selected text as primary context and flag in response
- [x] T027 [US2] Update `/query` endpoint in `app/main.py` to pass selected_text to RAG pipeline and include context_type in response (selected vs full-book)
- [x] T028 [P] [US2] Create integration test in `tests/test_api.py` for selected text queries with mocked services
- [x] T029 [US2] Add validation in `app/models.py` for selected_text (max 5000 chars, non-empty if provided)

**Checkpoint**: User Story 2 should support both full-book and selection-based queries independently

---

## Phase 5: User Story 3 - Embedded Chatbot Widget Integration (Priority: P1)

**Goal**: Make chatbot responsive and embeddable via web component with session state persistence across questions

**Independent Test**: Embed ChatKit web component on book page, verify component loads, test multiple queries in session, validate UI doesn't disrupt reading experience

### Implementation for User Story 3

- [x] T030 [P] [US3] Create session management in-memory store in `app/main.py` with SESSIONS dict and Session dataclass
- [x] T031 [P] [US3] Implement session creation and expiration logic in `app/main.py` with UUID generation and 30-minute timeout
- [x] T032 [US3] Add background task in `app/main.py` to clean up expired sessions every 60 seconds
- [x] T033 [P] [US3] Add session_id support to QueryRequest model in `app/models.py` (or create via header/cookie)
- [x] T034 [US3] Update `/query` endpoint in `app/main.py` to maintain session message history in SESSIONS dict
- [x] T035 [P] [US3] Add CORS configuration to `app/main.py` for cross-origin requests from book pages
- [x] T036 [US3] Create `/session` endpoints in `app/main.py` for creating new session and retrieving session status
- [x] T037 [P] [US3] Create basic HTML embedding template in `docs/embed-example.html` showing how to embed ChatKit component (defer full ChatKit integration to Phase 2)
- [x] T038 [US3] Add response time tracking and include latency_ms in QueryResponse for monitoring
- [x] T039 [P] [US3] Create integration tests in `tests/test_api.py` for session management and multi-turn queries

**Checkpoint**: Chatbot should support session-based conversation flow with message history

---

## Phase 6: User Story 4 - Book Content Ingestion Setup (Priority: P2)

**Goal**: Provide straightforward setup tool for administrators to upload and index book content

**Independent Test**: Upload sample book file, verify chunks created appropriately, confirm embeddings stored in Qdrant, validate book queryable within 5 minutes

### Implementation for User Story 4

- [x] T040 [P] [US4] Create `/ingest` POST endpoint in `app/main.py` accepting file upload and returning ingestion status
- [x] T041 [P] [US4] Add multipart file upload handling to QueryRequest or create separate IngestRequest model in `app/models.py`
- [x] T042 [US4] Implement file upload and save to temporary location in `/ingest` endpoint
- [x] T043 [US4] Add `/books` GET endpoint in `app/main.py` to list ingested books with metadata (title, author, chunk_count, upload_date)
- [x] T044 [US4] Create in-memory book registry to track ingested books during Phase 1 (book_id → {title, author, chunk_count})
- [x] T045 [P] [US4] Add validation for file format (PDF or TXT) in `/ingest` endpoint
- [x] T046 [US4] Add ingestion progress tracking/logging to provide feedback to administrator
- [x] T047 [P] [US4] Create integration tests in `tests/test_api.py` for `/ingest` and `/books` endpoints with mocked services

**Checkpoint**: Administrators should be able to upload books via API endpoint

---

## Phase 7: User Story 5 - Privacy and Session Management (Priority: P2)

**Goal**: Ensure no persistent user data storage - sessions ephemeral, conversation history discarded on session expiration

**Independent Test**: Submit queries in session, verify context maintained during session, close session and confirm no data in database, audit backend storage for zero persistence

### Implementation for User Story 5

- [x] T048 [P] [US5] Implement strict session expiration cleanup in `app/main.py` background task - delete entire session dict on expiration
- [x] T049 [P] [US5] Ensure no logging of user queries or responses in production logging (only operational metrics like response time)
- [x] T050 [US5] Add explicit privacy statement/disclaimer in API documentation
- [x] T051 [P] [US5] Create audit test in `tests/test_api.py` to verify zero persistence of queries after session expiration (verify SESSIONS dict is empty)
- [x] T052 [US5] Add configuration option to disable verbose logging in production mode in `app/config.py`

**Checkpoint**: Privacy guarantees verified - zero persistent user data storage

---

## Phase 8: User Story 6 - Fallback to General Knowledge (Priority: P3)

**Goal**: Gracefully handle out-of-book queries with general knowledge fallback and clear disclaimer

**Independent Test**: Ask question outside book scope, verify chatbot provides fallback response with explicit disclaimer, confirm fallback distinct from book-based answers

### Implementation for User Story 6

- [x] T053 [P] [US6] Update `synthesize_answer()` in `app/rag.py` to handle low-relevance results (similarity_score < 0.6) with fallback prompt
- [x] T054 [P] [US6] Add `is_fallback` boolean flag to QueryResponse in `app/models.py` to distinguish fallback vs book-based answers
- [x] T055 [US6] Update OpenRouter prompt in `app/rag.py` to clearly indicate when using general knowledge vs book excerpts
- [x] T056 [P] [US6] Add relevance threshold configuration to `app/config.py` (default 0.6)
- [x] T057 [US6] Create unit tests in `tests/test_rag.py` for fallback behavior with low-relevance results
- [x] T058 [P] [US6] Create integration tests in `tests/test_api.py` to verify is_fallback flag in response

**Checkpoint**: Fallback behavior implemented with clear user communication

---

## Phase 9: Core Tests & Validation

**Purpose**: Comprehensive testing across all user stories

- [x] T059 [P] Run all unit tests in `tests/test_ingestion.py` and `tests/test_rag.py` with pytest
- [x] T060 [P] Run all integration tests in `tests/test_api.py` with mocked Qdrant/OpenRouter
- [x] T061 [P] Run full test suite with coverage analysis: `pytest tests/ --cov=app --cov-report=html`
- [x] T062 Verify test coverage >80% for critical paths (ingestion, retrieval, synthesis, endpoints)
- [x] T063 Manual end-to-end test: Ingest sample book → Query via curl → Verify answer from book
- [x] T064 Manual test: Session persistence → Create session → Ask question → Ask follow-up → Verify history maintained

---

## Phase 10: Polish & Cross-Cutting Concerns

**Purpose**: Final validation, documentation, and deployment readiness

- [x] T065 [P] Create `README.md` in project root with project overview, setup instructions, and quick start
- [x] T066 [P] Create `docs/API.md` with OpenAPI specification and endpoint documentation (auto-generate from FastAPI or write manually)
- [x] T067 [P] Create `docs/ARCHITECTURE.md` with design decisions, flow diagrams, and data model explanations
- [x] T068 Create `QUICKSTART.md` in specs directory with step-by-step Phase 1 MVP guide (reference from quickstart.md in specs)
- [x] T069 [P] Verify all secrets in `.env` (not git-tracked), `.env.example` has safe placeholders
- [x] T070 [P] Create Docker setup files (optional Phase 2): `Dockerfile` and `docker-compose.yml` for local testing
- [x] T071 Run security audit: verify no API keys logged, no user data stored, HTTPS ready in docs
- [x] T072 [P] Add error handling improvements: better error messages for common failures (invalid PDF, rate limits, connection errors)
- [x] T073 Create deployment checklist in `docs/DEPLOYMENT.md` for moving to production
- [x] T074 Run `/health` endpoint and verify response format matches contract
- [x] T075 Final validation: All Phase 1 acceptance criteria pass

**Final Checkpoint**: Phase 1 MVP complete and ready for user testing

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - **BLOCKS all user stories**
- **User Stories (Phase 3+)**:
  - Phase 3 (US1): Depends on Foundational completion - can start immediately after
  - Phase 4 (US2): Depends on Phase 3 (US1) completion
  - Phase 5 (US3): Can start after Foundational (independent of US1/US2)
  - Phase 6 (US4): Can start after Foundational (independent of US1-US3)
  - Phase 7 (US5): Can start after Phase 5 (US3) completion
  - Phase 8 (US6): Can start after Phase 3 (US1) completion (but adds fallback behavior)
- **Tests & Validation (Phase 9)**: Depends on all implementation phases
- **Polish (Phase 10)**: Depends on all phases

### Recommended Execution Order (Single Developer)

1. Complete Phase 1: Setup (10 min)
2. Complete Phase 2: Foundational (30 min)
3. Complete Phase 3: User Story 1 (2-3 hours) — FULL-BOOK QUERIES
4. **STOP & TEST**: Ingest book, ask questions, verify RAG works
5. Complete Phase 4: User Story 2 (30 min) — SELECTION-BASED QUERIES
6. Complete Phase 5: User Story 3 (30 min) — SESSION MANAGEMENT
7. Complete Phase 6: User Story 4 (30 min) — BOOK INGESTION API
8. Complete Phase 7: User Story 5 (20 min) — PRIVACY VERIFICATION
9. Complete Phase 8: User Story 6 (20 min) — FALLBACK BEHAVIOR
10. Complete Phase 9: Tests & Validation (1 hour)
11. Complete Phase 10: Polish & Documentation (1 hour)

**Total Estimated Time**: 6-8 hours for Phase 1 MVP (full-book queries + session management + basic ingestion)

### Parallel Opportunities (Multi-Developer)

- **Phase 1 Setup**: All [P] tasks can run in parallel (dependencies, config)
- **Phase 2 Foundational**: All [P] tasks can run in parallel (config, models, validation scripts)
- **Phase 3 (US1)**: All [P] ingestion subtasks can run in parallel (load_pdf, chunking, embedding, storage)
- **Phase 5 (US3) & Phase 4 (US2)** can run in parallel after Phase 3 completes
- **Phase 6 (US4)** can start after Phase 2 (foundational) completes
- **Phase 8 (US6)** can start after Phase 3 completes

**With 3 developers**:
- Dev 1: Phase 1 + Phase 2 (setup foundation)
- Dev 2: Phase 3 (US1) + Phase 4 (US2) sequentially
- Dev 3: Phase 5 (US3) + Phase 6 (US4) in parallel (after foundational done)
- All: Phase 9 & 10 (testing, docs)

---

## Parallel Example: Phase 3 (User Story 1)

```
All [P] tasks can run in parallel (different files, no dependencies):

Task T011: Create load_pdf() in app/ingestion.py
Task T012: Create chunk_text() in app/ingestion.py  [parallelizable, but in same file so sequential]
Task T013: Create embed_chunks() in app/ingestion.py [parallelizable, but in same file so sequential]
Task T014: Create store_in_qdrant() in app/ingestion.py [parallelizable, but in same file so sequential]

Task T016: Create retrieve_similar_chunks() in app/rag.py [can run parallel with T011-T015]
Task T017: Create synthesize_answer() in app/rag.py [can run parallel with T011-T015]

Task T019: Create scripts/ingest_book.py [can run parallel once T015 done]

Tests T021-T023: Can run parallel after implementation
```

---

## Implementation Strategy

### MVP First (User Stories 1-3 Only)

1. Complete Phase 1: Setup ✅
2. Complete Phase 2: Foundational ✅
3. Complete Phase 3: User Story 1 (full-book queries) ✅
4. Complete Phase 5: User Story 3 (session management) ✅
5. **STOP and VALIDATE**: Test US1 + US3 together
6. **Deploy/demo Phase 1 MVP** — Readers can ask questions and system maintains session

### Incremental Delivery (Full Feature)

1. Phase 1-2: Setup + Foundational (foundation ready)
2. Phase 3: US1 → Test independently → Deploy (MVP: full-book queries!)
3. Phase 4: US2 → Test independently → Deploy (add selection-based queries)
4. Phase 5: US3 → Test independently → Deploy (add web integration)
5. Phase 6: US4 → Test independently → Deploy (add admin ingestion UI)
6. Phase 7: US5 → Test independently → Deploy (verify privacy)
7. Phase 8: US6 → Test independently → Deploy (add fallback behavior)
8. Phase 9-10: Tests + Polish → Final validation

Each user story adds value without breaking previous stories.

---

## Acceptance Criteria (Phase 1 MVP)

✅ **Phase 1-2 Complete**:
- [x] Project structure created
- [x] Config management working
- [x] Qdrant connection verified
- [x] OpenRouter APIs verified

✅ **Phase 3 (US1) Complete**:
- [x] Book ingestion pipeline works (PDF → Qdrant in <5 min)
- [x] `/query` endpoint returns real book answers (not hallucinated)
- [x] Answers include citations (page numbers)
- [x] Query response time <3 seconds
- [x] Unit tests pass (ingestion, RAG)
- [x] Integration tests pass (API endpoints)

✅ **Phase 5 (US3) Complete**:
- [x] Session management working (create, expire, cleanup)
- [x] Multi-turn conversations maintain context
- [x] Sessions auto-expire after 30 minutes
- [x] No session data persists after expiration

✅ **Phase 9-10 Complete**:
- [x] All tests passing (>80% coverage)
- [x] Documentation complete (README, API, Architecture)
- [x] No secrets in git
- [x] Quickstart guide verified
- [x] Manual end-to-end test passes

---

## Notes

- [P] tasks = different files, no dependencies on same file
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Phases must complete in order within dependencies
- Commit after each completed task or logical group
- Stop at any checkpoint to validate story independently
- Phase 1 MVP = Phases 1-3 + 5 (full-book queries + session management)
- Phase 2 MVP = All phases 1-8 complete
- Avoid: vague tasks, same-file conflicts, cross-story dependencies that break independence
