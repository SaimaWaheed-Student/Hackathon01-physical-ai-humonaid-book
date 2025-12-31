# Feature Specification: RAG Chatbot Integration for Digital Books

**Feature Branch**: `001-rag-chatbot-integration`
**Created**: 2025-12-30
**Status**: Draft
**Input**: Develop and integrate a Retrieval-Augmented Generation (RAG) chatbot into a published book platform

## User Scenarios & Testing *(mandatory)*

<!--
  IMPORTANT: User stories should be PRIORITIZED as user journeys ordered by importance.
  Each user story/journey must be INDEPENDENTLY TESTABLE - meaning if you implement just ONE of them,
  you should still have a viable MVP (Minimum Viable Product) that delivers value.
  
  Assign priorities (P1, P2, P3, etc.) to each story, where P1 is the most critical.
  Think of each story as a standalone slice of functionality that can be:
  - Developed independently
  - Tested independently
  - Deployed independently
  - Demonstrated to users independently
-->

### User Story 1 - Ask Questions About Entire Book Content (Priority: P1)

A reader is studying a book and wants to understand a concept that spans multiple chapters. They open the embedded chatbot and ask a question like "What are the main differences between chapter 3 and chapter 7?" The chatbot searches the entire book content via RAG, retrieves relevant sections from both chapters, and provides a comprehensive answer synthesizing information across the book.

**Why this priority**: This is the core RAG functionality that justifies the chatbot's existence. Full-book semantic search is the primary value proposition.

**Independent Test**: Can be fully tested by (1) ingesting a complete book, (2) asking a cross-chapter question, (3) verifying the chatbot retrieves and synthesizes sections from multiple parts of the book, and (4) validating the answer is accurate and comprehensive.

**Acceptance Scenarios**:

1. **Given** a complete book has been ingested and embedded in the vector database, **When** a user asks a question that requires context from multiple chapters, **Then** the system retrieves relevant sections from all applicable chapters and synthesizes a cohesive answer.
2. **Given** a user submits a question, **When** no relevant sections exist in the book, **Then** the chatbot falls back to its general knowledge with a note like "I didn't find this in the book, but based on general knowledge..."
3. **Given** multiple relevant sections exist, **When** the user asks a question, **Then** the chatbot ranks results by relevance and includes citations (e.g., "In Chapter 5: ...") so users know where information came from.

---

### User Story 2 - Query Based on Selected Text (Priority: P1)

A reader is reading Chapter 4 and selects a specific passage about quantum entanglement. They right-click the selection and ask the chatbot "Tell me more about this concept" or "How does this relate to other parts of the book?" The chatbot treats the selected text as the primary context, optionally searching the rest of the book for related content, and provides targeted answers.

**Why this priority**: Supporting user-initiated selections enables lightweight, focused queries without requiring full-book retrieval. This is essential for active reading and supports the requirement for selection-based queries.

**Independent Test**: Can be fully tested by (1) selecting a specific text passage from an embedded book page, (2) submitting a query with that selection as context, (3) verifying the system uses the selected text as primary context, and (4) confirming results are relevant to the selection.

**Acceptance Scenarios**:

1. **Given** a user selects text from the book, **When** they submit a query about that selection, **Then** the system treats the selected text as the primary context and responds accordingly.
2. **Given** a user selects text and asks a question, **When** the selection doesn't provide enough context, **Then** the chatbot can optionally search the full book for supplementary information with clear indication of what was found locally vs. in the broader book.
3. **Given** a user selects text, **When** they ask an unrelated question, **Then** the system gracefully handles the context mismatch and provides a helpful response (e.g., "Your selection is about [topic], but you asked about [other topic]. Did you mean...?").

---

### User Story 3 - Embedded Chatbot Widget Integration (Priority: P1)

A publisher has deployed an e-book on their web platform. They embed the chatbot as a web component (via ChatKit) in a sidebar or modal on the book page. Readers can click the chatbot icon at any time and start asking questions without leaving the reading experience. The chatbot is responsive, maintains session state across questions, and feels like a native part of the book interface.

**Why this priority**: Without seamless embedding, the chatbot is disconnected from the reading experience. Integration is essential for adoption and usability.

**Independent Test**: Can be fully tested by (1) embedding the ChatKit web component on a book page, (2) verifying the component loads without errors, (3) confirming the chatbot is responsive and interactive, (4) testing session persistence across multiple queries, and (5) validating the UI doesn't disrupt the reading experience.

**Acceptance Scenarios**:

1. **Given** a ChatKit web component is embedded on a book page, **When** the page loads, **Then** the chatbot widget is visible and ready to accept queries.
2. **Given** a user submits a query, **When** the chatbot processes it, **Then** the response appears in the widget in under 3 seconds (accounting for network latency).
3. **Given** a user asks multiple questions, **When** they interact with the chatbot, **Then** the conversation context is maintained (e.g., follow-up questions are understood in context of prior exchanges).

---

### User Story 4 - Book Content Ingestion Setup (Priority: P2)

An administrator has a PDF or text file of a book they want to make queryable. They use a setup tool or API to upload the book content, which is automatically chunked, embedded, and stored. Minimal manual configuration is required; the system handles the heavy lifting of parsing, chunking, and vector storage.

**Why this priority**: Without this, the chatbot can't function. However, it's often a one-time or infrequent operation, so it's P2 (essential but not user-facing day-to-day).

**Independent Test**: Can be fully tested by (1) uploading a sample book file, (2) verifying chunks are created appropriately, (3) confirming embeddings are generated and stored in Qdrant, (4) testing retrieval with a simple query, and (5) validating book metadata is stored in Postgres.

**Acceptance Scenarios**:

1. **Given** an administrator uploads a PDF or text file, **When** the ingestion process completes, **Then** the book content is indexed and queryable within 5 minutes.
2. **Given** a book is ingested, **When** the chunking strategy is applied, **Then** chunks are semantically coherent (e.g., ~1000 tokens per chunk with intelligent sentence boundaries) and overlap slightly to preserve context.
3. **Given** a book is ingested, **When** embeddings are generated, **Then** they are stored in Qdrant with metadata (book ID, chunk ID, page number) for traceability.

---

### User Story 5 - Privacy and Session Management (Priority: P2)

A user asks multiple questions about a book over several minutes. The chatbot maintains their session state (conversation history) only in memory. When the session ends or the browser tab is closed, all conversation history is immediately discarded. No user data (queries, identities, behavior) is stored persistently beyond the session duration.

**Why this priority**: Privacy is non-negotiable for user trust, but it doesn't block the core chatbot functionality. It's essential for compliance and user confidence.

**Independent Test**: Can be fully tested by (1) submitting queries through a chatbot session, (2) verifying session state is maintained during the session, (3) closing the session and confirming no data persists in the database, and (4) validating chat logs don't exist in any backend storage.

**Acceptance Scenarios**:

1. **Given** a user submits queries in a session, **When** the session is active, **Then** the conversation history is accessible within the session (e.g., for context in follow-up queries).
2. **Given** a user closes the browser or navigates away, **When** a new session is initiated, **Then** the previous conversation history is not accessible.
3. **Given** an administrator checks the database, **When** they query for user conversation logs, **Then** no personal queries or conversation data are found (only operational logs for system monitoring).

---

### User Story 6 - Fallback to General Knowledge (Priority: P3)

A user asks the chatbot a question that the book doesn't address (e.g., asking about a recent news event). The chatbot gracefully acknowledges that the book doesn't contain the information and provides a helpful response based on its general knowledge, with a clear disclaimer that the answer is not from the book.

**Why this priority**: This improves user experience and chatbot utility, but it's not critical to MVP. A basic implementation can simply say "I don't find this in the book," and P3 allows for enhancement later.

**Independent Test**: Can be fully tested by (1) asking a question outside the book's scope, (2) verifying the chatbot doesn't attempt to force-fit a book answer, (3) confirming the fallback response is provided with a clear disclaimer, and (4) checking that the disclaimer is distinct from actual book-based answers.

**Acceptance Scenarios**:

1. **Given** a user asks a question unrelated to the book, **When** no relevant book sections are retrieved (relevance threshold not met), **Then** the chatbot can provide a general knowledge response prefixed with "Based on general knowledge (not from the book): ...".
2. **Given** the chatbot provides a general knowledge answer, **When** the user sees it, **Then** it's clear the answer is not from the book (e.g., different styling, explicit disclaimer).

---

### Edge Cases

- What happens when a user selects text but then asks an unrelated question? System should gracefully handle context mismatches.
- How does the system handle very long selected text passages (e.g., 5000+ tokens)? Should it truncate or summarize intelligently.
- What happens when a book file is corrupted, has encoding issues, or is in an unsupported format? System should fail gracefully with user-friendly error messages.
- How does the system behave if Qdrant Cloud is temporarily unavailable? Should it queue embeddings or provide graceful fallback.
- What happens when a chunk has low embedding quality or is semantically incoherent? Should the system detect and handle this.
- How does the chatbot handle multi-language queries if the book is in English? Should it translate and flag that it's working outside the book's scope.
- What if a user session is idle for extended periods? Should the system automatically expire the session to prevent memory leaks.
- How does the system handle extremely large books (100,000+ pages)? Should chunking and embedding scale efficiently.
- What happens if OpenRouter API rate limits are exceeded? Should the system queue requests or provide a graceful user message.
- How does the system handle concurrent queries from the same or different sessions? Should it manage request rate limiting and prevent abuse.
- What if selected text contains special characters, code snippets, or non-standard formatting? Should the system preserve context correctly.

## Requirements *(mandatory)*

### Functional Requirements

#### Core Retrieval-Augmented Generation
- **FR-001**: System MUST accept user queries and retrieve relevant book content sections via semantic search from the vector database
- **FR-002**: System MUST use OpenRouter API for all LLM calls (embeddings and text generation), never making direct OpenAI API calls
- **FR-003**: System MUST rank retrieved sections by relevance and synthesize them into coherent, citation-aware responses
- **FR-004**: System MUST handle queries based on user-selected text as the primary context, with optional supplementary full-book search

#### Book Content Ingestion and Storage
- **FR-005**: System MUST accept book content in PDF and plain text formats and parse them into processable text
- **FR-006**: System MUST chunk book content into semantically coherent segments (default ~1000 tokens per chunk) with configurable overlap
- **FR-007**: System MUST generate embeddings for each chunk using OpenRouter API and store them in Qdrant Cloud
- **FR-008**: System MUST store book metadata (title, author, upload date, total chunks) and chunk metadata (book ID, chunk ID, page/section number) in Neon Postgres
- **FR-009**: System MUST support hybrid search (vector similarity + keyword matching) to improve retrieval accuracy

#### User Interaction and UI Integration
- **FR-010**: System MUST embed the chatbot as a web component (via ChatKit) on the book's web page, supporting iframe or JavaScript embed methods
- **FR-011**: System MUST maintain session-level conversation context to support follow-up questions
- **FR-012**: System MUST display response streaming in real-time to provide immediate feedback to users
- **FR-013**: System MUST provide visual or textual citations (e.g., "In Chapter 5: ...") so users know where answers originate

#### API Endpoints
- **FR-014**: System MUST expose `/api/query` endpoint accepting a user query and optional selected text, returning a streaming response
- **FR-015**: System MUST expose `/api/ingest` endpoint for uploading and processing new book files
- **FR-016**: System MUST expose `/api/books` endpoint for listing available ingested books
- **FR-017**: System MUST expose `/api/health` endpoint for monitoring system availability

#### Privacy and Data Handling
- **FR-018**: System MUST store conversation history only in-memory for the duration of a user session
- **FR-019**: System MUST immediately purge all session data (queries, responses, context) when a session expires or the user closes their browser
- **FR-020**: System MUST NOT persist user identities, query logs, or behavioral data to any permanent storage
- **FR-021**: System MUST NOT share user queries with third-party services (except OpenRouter for LLM inference, as required)

#### Error Handling and Fallbacks
- **FR-022**: System MUST provide fallback responses when no relevant book sections are retrieved (e.g., "I didn't find this in the book, but based on general knowledge...")
- **FR-023**: System MUST handle gracefully when external services (Qdrant, Neon, OpenRouter) are unavailable with user-friendly error messages
- **FR-024**: System MUST validate input formats and sizes, rejecting malformed queries or excessively long selections with clear error messages

#### Performance and Scalability
- **FR-025**: System MUST respond to queries within 3 seconds under normal operating conditions (including network latency)
- **FR-026**: System MUST support ingesting books up to 100,000 pages without performance degradation
- **FR-027**: System MUST handle concurrent queries from multiple users/sessions without blocking or resource exhaustion

### Key Entities

- **Book**: Represents a digital book that has been ingested. Attributes: ID, title, author, upload timestamp, total chunks, source file (PDF/text), format version. Relationships: contains many Chunks, has one embedding index in Qdrant.

- **Chunk**: A semantically coherent segment of a book (typically ~1000 tokens). Attributes: ID, book ID, content text, page/section number, token count, embedding vector. Relationships: belongs to one Book, has one vector embedding in Qdrant, has metadata in Postgres.

- **Session**: A user's active conversation with the chatbot. Attributes: ID, creation timestamp, expiration timestamp, conversation history (in-memory). Relationships: contains many Messages, tracks user context. Scope: ephemeral, deleted upon session expiration.

- **Message**: A single user query or chatbot response within a session. Attributes: ID, session ID, role (user/assistant), content text, timestamp, metadata (e.g., selected text context, sources used). Relationships: belongs to one Session. Scope: ephemeral, deleted with session.

- **Book Metadata**: Metadata for chunks and books stored in Postgres. Attributes: book ID, chunk ID, title, author, chunk text, chunk embedding, page/section reference, upload date. Purpose: enables SQL queries for book discovery and pagination while Qdrant handles vector search.

## Success Criteria *(mandatory)*

### Measurable Outcomes

#### Functionality
- **SC-001**: Full-book queries return relevant results with citations in under 3 seconds for books up to 100,000 pages
- **SC-002**: Selection-based queries correctly identify selected text as primary context and provide accurate targeted answers in under 2 seconds
- **SC-003**: 95% of queries that have relevant book content retrieve at least one semantically related section (top-k recall >= 0.95)
- **SC-004**: Chatbot accurately cites the source (chapter/section) for 100% of book-based answers

#### Reliability and Performance
- **SC-005**: System maintains 99.5% uptime during normal operating hours (excluding planned maintenance)
- **SC-006**: Book ingestion processes files up to 10,000 pages within 5 minutes with zero data loss
- **SC-007**: Concurrent queries from 50+ users are processed without blocking, with response time variance < 10%
- **SC-008**: Session expiration occurs automatically after 30 minutes of inactivity, purging all conversation history within 5 seconds

#### Privacy and Security
- **SC-009**: Zero user queries or conversation data persist in Postgres or Qdrant after session termination (verified via database audit)
- **SC-010**: No query logs or personally identifiable information are accessible via API or database inspection
- **SC-011**: All API communication uses HTTPS/TLS encryption; OpenRouter API calls do not log user content beyond transient processing

#### User Experience
- **SC-012**: Chatbot widget loads and becomes interactive within 2 seconds on the book page
- **SC-013**: 90% of users can successfully ask a question and receive an answer on their first attempt without documentation
- **SC-014**: Response streaming provides visible feedback to users (first token appears within 1 second of query submission)
- **SC-015**: Fallback responses (when book content is insufficient) are distinguishable from book-based answers, reducing user confusion

#### Scalability and Cost Efficiency
- **SC-016**: System operates within free/tier-1 cost limits: Qdrant Cloud Free Tier, Neon Serverless Free Tier, and OpenRouter API credits for reasonable usage (< 1000 queries/day)
- **SC-017**: Book chunks and embeddings are stored efficiently, with average storage cost < 1 cent per 1000-page book
- **SC-018**: The system can support 10+ ingested books and 100+ concurrent user sessions without exceeding free-tier quotas

## Assumptions

- **Book Format**: Books are provided in PDF or plain text format. OCR for scanned PDFs is not in scope; books are assumed to be digital text or machine-readable PDFs.
- **Text Language**: Primary language is English. Non-English queries or books may work but are not optimized.
- **No User Authentication**: The feature does not require user login or persistent identity. All interactions are anonymous and session-based.
- **Stateless Backend**: The system assumes FastAPI can horizontally scale; sessions are not shared across server instances (sticky sessions or in-memory stores are acceptable for MVP).
- **OpenRouter API Availability**: The system assumes reliable access to OpenRouter API with reasonable rate limits (>=1000 tokens/min). Temporary outages are handled gracefully.
- **Book Metadata Availability**: Book titles, authors, and section breaks are available or inferred from the book content. Perfect structured metadata is not required.
- **Chunk Relevance**: Semantic chunking (not random splitting) is assumed to preserve context. Default ~1000 token chunks are adequate for typical book content.
- **Citation Accuracy**: The system extracts page/chapter information from book metadata or infers it from chunk positioning. 100% citation accuracy is expected but minor ambiguities are acceptable.
- **No Real-Time Updates**: Books are treated as static content after ingestion. Real-time updates to book content during user sessions are out of scope.
- **Session Duration**: User sessions are assumed to last minutes to hours, not days. Conversation history fits comfortably in-memory for typical usage.

## Dependencies

### External Services (Required)
- **OpenRouter API**: For embeddings generation and LLM inference (gpt-4, Claude, or compatible models)
- **Qdrant Cloud Free Tier**: For vector database and semantic search
- **Neon Serverless Postgres**: For storing book metadata, chunk metadata, and ingestion logs
- **ChatKit (OpenAI AgentKit)**: For embeddable chatbot UI components

### Internal Components (To Be Built)
- **FastAPI Backend**: Core API server for query handling, ingestion, and session management
- **Book Ingestion Pipeline**: PDF/text parsing, chunking, embedding generation, and storage
- **Session Manager**: In-memory session storage, cleanup, and timeout handling
- **RAG Pipeline**: Vector search, result ranking, response synthesis, and citation extraction

### Browser/Client Environment
- **Modern Web Browser**: Supporting ES6+, fetch API, and web components
- **JavaScript Runtime**: For embedding ChatKit web components and managing session state on the client

## Notes

- **MVP Scope**: The specification focuses on a Minimum Viable Product with core RAG functionality. Nice-to-have features (e.g., conversation history export, analytics, advanced summarization) are deferred.
- **Security Considerations**: While privacy is a priority (no persistent user data), the system does not implement advanced authentication, rate limiting, or DDoS protection in MVP. These can be added in future iterations based on production needs.
- **Cost Optimization**: Free/tier-1 pricing is a hard constraint. The system must be cost-efficient by default (reasonable chunk sizes, selective full-book searches, query result caching where possible).
- **Accessibility**: The chatbot should be keyboard-navigable and screen-reader friendly, following WCAG 2.1 AA standards for web components.
- **Testing Strategy**: Unit tests for individual components (chunking, embedding, retrieval), integration tests for the full RAG pipeline, and end-to-end tests for user workflows are required before launch.
- **Future Enhancements**: Multi-language support, fine-tuned embeddings, conversation history export, advanced filtering (by chapter/section), and user feedback loops are candidates for post-MVP iterations.
