# Tasks: RAG Chatbot Integration

**Input**: Design documents from `specs/1-rag-chatbot/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

## Phase 1: Setup

**Purpose**: Project initialization and basic structure for the RAG chatbot backend.

- [x] T001 Create `book-backend` folder at project root: `book-backend/`
- [x] T002 Initialize FastAPI project structure within `book-backend/`: `book-backend/app/main.py`, `book-backend/app/api/`, `book-backend/tests/`
- [x] T003 Create `scripts` folder at project root: `scripts/`
- [x] T004 Initialize Python virtual environment and dependencies for `book-backend/`: `book-backend/requirements.txt`
- [x] T005 Configure environment variables for OpenAI API key, Neon Postgres, Qdrant Cloud.

## Phase 2: Foundational Tasks (Backend Core)

**Purpose**: Implement core RAG backend services.
**Checkpoint**: Core API endpoints are functional for embedding, storing, querying, and basic chat.

- [x] T006 [P] Implement basic FastAPI application setup in `book-backend/app/main.py`
- [x] T007 [P] Implement `/embed` API endpoint in `book-backend/app/api/embeddings.py` (using OpenAI Embeddings)
- [x] T008 [P] Implement `/store` API endpoint in `book-backend/app/api/store.py` (for Qdrant)
- [x] T009 [P] Implement Qdrant client initialization and operations in `book-backend/app/db/qdrant.py`
- [x] T010 [P] Implement Neon Postgres client initialization and logging in `book-backend/app/db/postgres.py`
- [x] T011 [P] Implement Pydantic models for data (Book Content Chunk, Embedding, User Query, Chatbot Response) in `book-backend/app/schemas/`.
- [x] T012 [P] Implement content ingestion script for parsing Docusaurus markdown and generating embeddings in `scripts/content_ingestion.py`
- [x] T013 Run `scripts/content_ingestion.py` to populate Qdrant and Neon with initial book content.

## Phase 3: User Story 1 - Ask Questions from Book Content (Priority: P1) 🎯 MVP

**Goal**: A user can ask questions and receive grounded answers from the chatbot embedded in the Docusaurus UI.
**Independent Test**: A user can activate the chatbot, ask a question based on a specific chapter, and receive an accurate, relevant answer that directly references the book's text.

### Implementation for User Story 1

- [x] T014 [P] [US1] Implement `/query` API endpoint in `book-backend/app/api/query.py` (for Qdrant retrieval)
- [x] T015 [P] [US1] Implement `/chat` API endpoint in `book-backend/app/api/chat.py` (for LLM interaction using OpenAI Agents/ChatKit)
- [x] T016 [P] [US1] Develop Docusaurus React component for chatbot UI in `robotic-book/src/components/ChatbotUI.jsx`
- [x] T017 [P] [US1] Integrate ChatbotUI component into Docusaurus theme/pages (e.g., in a layout or specific chapter's MDX).
- [x] T018 [US1] Connect frontend ChatbotUI to backend API endpoints (`/chat` and potentially `/query` for direct retrieval demonstration).

## Phase 4: Polish & Cross-Cutting Concerns

**Purpose**: Improve reliability, performance, and deployability.

- [x] T019 [P] Set up CI/CD for `book-backend` (e.g., Dockerfile, Render/Fly.io config for automated deployments).
- [x] T020 [P] Set up CI/CD for `robotic-book` (frontend deployment to Vercel/Netlify).
- [x] T021 [P] Implement comprehensive unit tests for `book-backend` in `book-backend/tests/`.
- [x] T022 [P] Implement end-to-end integration tests for the full RAG pipeline.
- [x] T023 Performance testing and optimization for chatbot response time (targeting <3 seconds).
- [x] T024 Refine LLM prompts and RAG retrieval strategy for groundedness and hallucination prevention.

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately.
- **Foundational Tasks (Phase 2)**: Depends on Setup completion - BLOCKS User Story 1 implementation.
- **User Story 1 (Phase 3)**: Depends on Foundational Tasks completion.
- **Polish (Phase 4)**: Depends on User Story 1 being functional.

### Within Each User Story

- API endpoints (embedding, storing, querying, chat) should be developed before frontend integration.
- Content ingestion should be completed before end-to-end testing.

### Parallel Opportunities

- Tasks T006-T011 (Backend Core foundational tasks) can be parallelized.
- Tasks T014-T017 (User Story 1 implementation) can be parallelized.
- Tasks T019-T022 (Polish phase tasks) can be parallelized.

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational Tasks (CRITICAL - blocks all stories)
3. Complete Phase 3: User Story 1
4. **STOP and VALIDATE**: Test User Story 1 independently (user can ask questions and get grounded answers in Docusaurus UI).
5. Deploy/demo if ready.

### Incremental Delivery

- Each phase builds upon the previous, enabling incremental validation.
- Core backend functionality (Phase 2) serves as a standalone component before UI integration.

## Notes

- [P] tasks = different files, no dependencies
- [US1] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Verify tests fail before implementing
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
