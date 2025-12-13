# Tasks: RAG Embeddings Pipeline

**Feature**: 006-rag-embeddings-pipeline
**Input**: Design documents from `specs/006-rag-embeddings-pipeline/`
**Prerequisites**: plan.md, spec.md, data-model.md, contracts/cli-interface.md, quickstart.md

**Tests**: Tests are NOT explicitly requested in the feature specification. Test tasks are omitted per template guidance.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3, US4)
- Include exact file paths in descriptions

## Path Conventions

Per plan.md structure:
- Backend: `backend/main.py` (single-file implementation)
- Tests: `backend/tests/`
- Environment: `backend/.env`
- Configuration: `backend/pyproject.toml`

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [X] T001 Create backend directory structure per plan.md
- [X] T002 Initialize UV project with pyproject.toml in backend/ directory
- [X] T003 [P] Create virtual environment using UV in backend/.venv
- [X] T004 [P] Install core dependencies (beautifulsoup4, lxml, cohere, qdrant-client, requests, python-dotenv, langchain, tiktoken) via UV
- [X] T005 [P] Install development dependencies (pytest, pytest-asyncio) via UV
- [X] T006 Create .env.example file in backend/ with all required environment variables from cli-interface.md
- [X] T007 Create .gitignore to exclude backend/.venv, backend/.env, and backend/*.log
- [X] T008 Create urls.txt.example in backend/ with sample Docusaurus URLs

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [ ] T009 Initialize Qdrant Docker container (docker run command per quickstart.md) - SKIPPED (user will configure manually)
- [ ] T010 Verify Qdrant connection and API accessibility at http://localhost:6333 - IMPLEMENTED (verify_qdrant_connection function)
- [X] T011 Create backend/main.py with basic CLI argument parsing structure (--urls-file, --urls, --collection-name, --verbose, --dry-run, --force-reindex, --batch-size, --chunk-size, --chunk-overlap, --output-report)
- [X] T012 Implement environment variable loading from .env using python-dotenv in backend/main.py
- [X] T013 Setup logging infrastructure (INFO/DEBUG levels, file and console handlers) in backend/main.py
- [X] T014 Implement exit code handling (0-5 per cli-interface.md) in backend/main.py
- [X] T015 Create Qdrant collection initialization function with 1024-dimensional vectors and cosine distance in backend/main.py

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Content Extraction and Processing (Priority: P1) 🎯 MVP

**Goal**: Automatically extract and process text content from all book website URLs without manual intervention

**Independent Test**: Given a list of valid book URLs, verify that text content is successfully extracted from each URL with proper error handling

### Implementation for User Story 1

- [X] T016 [P] [US1] Implement URL validation function (HTTP/HTTPS only, no malformed URLs) in backend/main.py
- [X] T017 [P] [US1] Implement URL file parser (read urls.txt, skip comments and blank lines) in backend/main.py
- [X] T018 [US1] Implement HTML fetching function with requests library (timeout: 30s, max retries: 3) in backend/main.py
- [X] T019 [US1] Implement BeautifulSoup HTML parsing with lxml parser and fallback parsers in backend/main.py
- [X] T020 [US1] Implement Docusaurus content extraction (selector: article.theme-doc-markdown, remove nav/aside/footer) in backend/main.py
- [X] T021 [US1] Implement text preprocessing (clean whitespace, preserve code blocks, extract headings) in backend/main.py
- [X] T022 [US1] Create Content Document data structure (source_url, page_title, content_text, extraction_timestamp, content_hash, word_count, chapter, section, has_code, has_images) in backend/main.py
- [X] T023 [US1] Implement SHA-256 content hashing for change detection in backend/main.py
- [X] T024 [US1] Implement error handling for HTTP errors (404, 500, timeout) with logging and graceful continuation in backend/main.py
- [X] T025 [US1] Add progress tracking and console output (INFO level: "Processing URL X/N") in backend/main.py

**Checkpoint**: At this point, the pipeline can extract content from URLs and handle errors gracefully. Test with sample Docusaurus URLs.

---

## Phase 4: User Story 2 - Embedding Generation and Storage (Priority: P2)

**Goal**: Automatically convert extracted content into semantic embeddings and store in vector database with metadata

**Independent Test**: Given pre-extracted text samples, verify embeddings are generated and stored in Qdrant with correct metadata (source URL, page title, timestamp)

### Implementation for User Story 2

- [X] T026 [P] [US2] Implement tiktoken-based tokenization function (cl100k_base encoding) in backend/main.py
- [X] T027 [P] [US2] Implement LangChain RecursiveCharacterTextSplitter integration (chunk_size=400, chunk_overlap=50, semantic boundaries) in backend/main.py
- [X] T028 [US2] Create Text Segment data structure (segment_id, parent_document_url, segment_text, token_count, character_count, chunk_index, total_chunks, overlap_with_previous, overlap_with_next, heading_hierarchy, contains_code) in backend/main.py
- [X] T029 [US2] Implement chunking validation (95% chunks between 100-500 tokens, 0% exceed 512 tokens per spec SC-007) in backend/main.py
- [X] T030 [US2] Implement Cohere client initialization with API key and model (embed-english-v3.0) in backend/main.py
- [X] T031 [US2] Implement batch embedding generation (batch_size=96, input_type=search_document) with Cohere API in backend/main.py
- [X] T032 [US2] Implement API retry logic with exponential backoff (max_retries=3) in backend/main.py
- [X] T033 [US2] Implement rate limiting handling (429 errors, respect Cohere Production tier limits) in backend/main.py
- [X] T034 [US2] Create Embedding Metadata payload structure (text, source_url, page_title, chapter, section, subsection, chunk_index, total_chunks, token_count, extraction_timestamp, content_hash, has_code, embedding_model) per data-model.md in backend/main.py
- [X] T035 [US2] Implement Qdrant point creation (UUID as ID, 1024-dim vector, payload with metadata) in backend/main.py
- [X] T036 [US2] Implement Qdrant upsert operation with batch processing in backend/main.py
- [X] T037 [US2] Implement dry-run mode (--dry-run flag: skip Qdrant writes, log what would be stored) in backend/main.py
- [X] T038 [US2] Add embedding generation metrics tracking (latency, batch efficiency, API calls) in backend/main.py

**Checkpoint**: At this point, the pipeline can chunk content, generate embeddings, and store them in Qdrant. Test with sample content and verify Qdrant storage.

---

## Phase 5: User Story 3 - Retrieval Validation (Priority: P3)

**Goal**: Verify that stored embeddings return accurate and relevant content snippets for test queries before chatbot integration

**Independent Test**: Execute sample semantic queries against Qdrant and verify returned results are contextually relevant with appropriate similarity scores (≥0.7 per spec SC-003)

### Implementation for User Story 3

- [ ] T039 [P] [US3] Implement Cohere query embedding generation (input_type=search_query) in backend/main.py
- [ ] T040 [US3] Implement Qdrant semantic search function (top_k=5, score_threshold=0.7, cosine distance) in backend/main.py
- [ ] T041 [US3] Implement search result formatting (score, text snippet, source URL, page title, chunk_index) in backend/main.py
- [ ] T042 [US3] Add --validate-retrieval CLI flag for post-processing validation in backend/main.py
- [ ] T043 [US3] Implement sample query validation (3-5 test queries specific to book content) in backend/main.py
- [ ] T044 [US3] Add retrieval metrics logging (average similarity score, top-k accuracy, result count) in backend/main.py
- [ ] T045 [US3] Implement similarity score validation (verify ≥0.7 for known-good queries per spec SC-003) in backend/main.py

**Checkpoint**: At this point, the pipeline can validate that embeddings are retrievable and semantically relevant. Test with known-good queries.

---

## Phase 6: User Story 4 - Pipeline Automation (Priority: P4)

**Goal**: Enable entire extraction-to-storage pipeline to run automatically on demand with comprehensive reporting

**Independent Test**: Trigger automated pipeline and verify all steps execute successfully from URL extraction through embedding storage with detailed logging

### Implementation for User Story 4

- [ ] T046 [P] [US4] Create Processing Job data structure (job_id, start_time, end_time, status, urls_requested, urls_processed, urls_failed, documents_extracted, chunks_generated, embeddings_generated, embeddings_stored, error_log, processing_time_seconds, average_tokens_per_chunk) per data-model.md in backend/main.py
- [ ] T047 [US4] Implement end-to-end pipeline orchestration (extract → chunk → embed → store) in backend/main.py
- [ ] T048 [US4] Implement processing state tracking (resume capability after failures per spec FR-014) in backend/main.py
- [ ] T049 [US4] Implement content hash comparison for incremental updates (skip unchanged pages) in backend/main.py
- [ ] T050 [US4] Implement --force-reindex flag to bypass content hash checks in backend/main.py
- [ ] T051 [US4] Create JSON report structure (job summary, metrics, errors, warnings per cli-interface.md) in backend/main.py
- [ ] T052 [US4] Implement --output-report flag to save JSON report to specified file path in backend/main.py
- [ ] T053 [US4] Implement verbose logging (--verbose flag: DEBUG level with detailed timing, API calls, chunk stats) in backend/main.py
- [ ] T054 [US4] Add console output formatting (progress bar, success/error counts, total time per cli-interface.md) in backend/main.py
- [ ] T055 [US4] Implement error aggregation and summary reporting (URLs failed, error types, retry attempts) in backend/main.py
- [ ] T056 [US4] Add performance metrics validation (verify <10 minutes for 50-page book per spec SC-004) in backend/main.py

**Checkpoint**: At this point, the full pipeline is automated and production-ready. Test with complete book URL list (50+ pages).

---

## Phase 7: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories and prepare for production

- [ ] T057 [P] Create comprehensive .env file with all environment variables from quickstart.md in backend/.env (DO NOT COMMIT - add to .gitignore)
- [ ] T058 [P] Create production-ready urls.txt with actual book URLs in backend/ (one URL per line, comments supported)
- [ ] T059 [P] Update backend/README.md with quickstart instructions, CLI usage examples, and troubleshooting guide
- [ ] T060 [P] Add input validation for all CLI arguments (chunk_size: 100-512, batch_size: 1-96, overlap < chunk_size)
- [ ] T061 Add comprehensive error messages matching cli-interface.md specifications (exit codes 0-5)
- [ ] T062 [P] Implement graceful shutdown handling (Ctrl+C cleanup, partial progress save)
- [ ] T063 Code cleanup and refactoring (extract functions, add docstrings, improve naming)
- [ ] T064 [P] Add type hints throughout backend/main.py for better IDE support
- [ ] T065 Performance optimization (parallel URL processing if feasible, connection pooling)
- [ ] T066 Security hardening (URL allowlist validation, prevent SSRF attacks, sanitize inputs)
- [ ] T067 Run quickstart.md validation (verify setup instructions work end-to-end)
- [ ] T068 [P] Create example output report JSON file (backend/example-report.json) showing successful run
- [ ] T069 Final end-to-end test with production Cohere API key and actual book URLs

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3-6)**: All depend on Foundational phase completion
  - User stories have **SEQUENTIAL dependencies** due to single-file architecture:
    - US1 (Extraction) → US2 (Embedding) → US3 (Retrieval) → US4 (Automation)
  - Each story extends backend/main.py incrementally
- **Polish (Phase 7)**: Depends on all user stories being complete

### User Story Dependencies

- **User Story 1 (P1) - Content Extraction**: Can start after Foundational (Phase 2) - Foundation for all other stories
- **User Story 2 (P2) - Embedding Generation**: Depends on US1 completion - Requires extracted content
- **User Story 3 (P3) - Retrieval Validation**: Depends on US2 completion - Requires stored embeddings
- **User Story 4 (P4) - Pipeline Automation**: Depends on US1, US2, US3 completion - Orchestrates all previous components

### Within Each User Story

- Tasks within a story marked [P] can run in parallel (different functions/sections)
- Implementation tasks must respect data flow (extraction → chunking → embedding → storage)
- Story complete before moving to next priority

### Parallel Opportunities

- **Setup Phase**: T003, T004, T005, T006, T008 can run in parallel
- **User Story 1**: T016 and T017 can run in parallel (different validation functions)
- **User Story 2**: T026 and T027 can run in parallel (tokenization and chunking setup)
- **User Story 3**: T039 can start while T040 is being designed
- **User Story 4**: T046 (data structure) can run in parallel with state tracking design
- **Polish Phase**: T057, T058, T059, T060, T062, T064, T068 can run in parallel (different files/concerns)

**Note**: Due to single-file architecture (backend/main.py), parallelism is LIMITED. Most tasks are sequential edits to the same file.

---

## Parallel Example: User Story 2 (Limited by Single File)

```bash
# These can be designed/prototyped in parallel, then integrated sequentially:
Task: T026 - Implement tokenization function (separate function)
Task: T027 - Implement text splitter (separate function)

# Sequential integration required:
Task: T028 - Create data structure (must exist before T029)
Task: T029 - Implement validation (depends on T028)
Task: T030-033 - Cohere integration (sequential: init → generate → retry → rate limit)
Task: T034-036 - Qdrant integration (sequential: metadata → point creation → upsert)
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup (T001-T008)
2. Complete Phase 2: Foundational (T009-T015) - **CRITICAL**
3. Complete Phase 3: User Story 1 (T016-T025)
4. **STOP and VALIDATE**: Test extraction with sample URLs
   - Verify: Content extracted from ≥95% of URLs (spec SC-001)
   - Verify: Error handling works (404, timeout, malformed HTML)
   - Verify: Content hash generation for change detection
5. Demo extraction pipeline before proceeding

### Incremental Delivery

1. **Setup + Foundational** → Foundation ready (Qdrant running, CLI skeleton, logging infrastructure)
2. **+ User Story 1** → Extract content from URLs → **MVP 1: Content Scraper**
3. **+ User Story 2** → Generate and store embeddings → **MVP 2: Embedding Pipeline**
4. **+ User Story 3** → Validate retrieval quality → **MVP 3: Validated RAG Foundation**
5. **+ User Story 4** → Full automation and reporting → **MVP 4: Production Pipeline**
6. **+ Polish** → Production-ready → **FINAL: Deployable System**

Each increment adds value and can be tested independently.

### Sequential Single-Developer Strategy

**Recommended approach for single-file architecture**:

1. Developer completes Setup + Foundational together (T001-T015)
2. Once Foundational is done:
   - Implement User Story 1 completely (T016-T025)
   - Test US1 independently before proceeding
   - Implement User Story 2 completely (T026-T038)
   - Test US2 independently (extraction + embedding + storage working)
   - Implement User Story 3 completely (T039-T045)
   - Test US3 independently (retrieval validation working)
   - Implement User Story 4 completely (T046-T056)
   - Test US4 independently (full pipeline automation working)
3. Polish and production-readiness (T057-T069)

**Justification**: Single-file architecture (backend/main.py) limits parallelism. Sequential implementation ensures each story is stable before adding complexity.

---

## Success Criteria Validation

Each user story has measurable success criteria from spec.md:

**User Story 1 (Content Extraction)**:
- ✅ SC-001: System extracts text from ≥95% of provided URLs
- Verify with: Real book URL list, check error_log for failures

**User Story 2 (Embedding & Storage)**:
- ✅ SC-002: Embeddings stored with 100% metadata accuracy
- ✅ SC-007: 95% of chunks between 100-500 tokens
- Verify with: Query Qdrant payload, inspect chunk token_count distribution

**User Story 3 (Retrieval Validation)**:
- ✅ SC-003: Retrieval returns results with similarity scores ≥0.7
- Verify with: Sample queries, check score distribution in results

**User Story 4 (Pipeline Automation)**:
- ✅ SC-004: Process 50-page book in <10 minutes
- ✅ SC-005: Detailed error logs enable debugging within 5 minutes
- ✅ SC-006: 90%+ automated runs succeed without intervention
- Verify with: Full book processing run, timing metrics, error report

---

## Notes

- **[P] tasks**: Different functions/sections, can be designed in parallel (implementation still sequential in main.py)
- **[Story] label**: Maps task to specific user story for traceability
- **Single-file architecture**: Limits parallel execution, favors incremental sequential development
- **No test tasks**: Tests not requested in feature specification (spec.md out-of-scope section)
- **Commit strategy**: Commit after each user story phase completion
- **Validation checkpoints**: Test each user story independently before proceeding
- **Performance target**: Keep 10-minute processing time in mind (spec SC-004)
- **Error handling**: Graceful degradation at every stage (spec FR-007)

---

## Total Task Count: 69 tasks

- Setup: 8 tasks
- Foundational: 7 tasks
- User Story 1: 10 tasks
- User Story 2: 13 tasks
- User Story 3: 7 tasks
- User Story 4: 11 tasks
- Polish: 13 tasks

**MVP Scope (Recommended)**: T001-T025 (Setup + Foundational + User Story 1) = **25 tasks**
**Full Pipeline**: T001-T056 (All user stories) = **56 tasks**
**Production Ready**: T001-T069 (All tasks) = **69 tasks**
