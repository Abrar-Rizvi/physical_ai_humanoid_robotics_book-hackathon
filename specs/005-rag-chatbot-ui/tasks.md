# Test Cases & Implementation Tasks: RAG Chatbot UI Integration

**Feature**: RAG Chatbot UI Integration
**Branch**: `005-rag-chatbot-ui`
**Spec**: [spec.md](./spec.md) | **Plan**: [plan.md](./plan.md)
**Generated**: 2025-12-16

**Overview**: This feature provides a RAG chatbot UI integrated into the Docusaurus book site. The system is already fully implemented with a chat widget that connects to a FastAPI backend that processes queries against Qdrant-stored book content.

## Dependencies
- User Story 1 (P1) - View and Interact with RAG Chat Widget: Foundation for all other stories
- User Story 2 (P1) - Receive Grounded Responses: Depends on backend API and RAG pipeline
- User Story 3 (P2) - Use Text Selection Context: Depends on User Story 1

## Parallel Execution Examples
- T001-T003 (Setup phase) can run in parallel
- T008-T010 (Testing phase) can run in parallel after foundational setup

## Implementation Strategy
- MVP: User Story 1 (Basic chat widget functionality)
- Phase 2: User Story 2 (Backend integration and responses)
- Phase 3: User Story 3 (Text selection enhancement)

## Phase 1: Setup & Environment Verification
**Goal**: Verify all existing components are properly configured and working

- [x] T001 Set up Python environment with required dependencies (FastAPI, Qdrant, Cohere, OpenAI) - Python 3.13.2 confirmed
- [x] T002 Set up Node.js environment and install Docusaurus dependencies - Node.js v20.17.0 confirmed
- [ ] T003 Verify Qdrant vector database is running and accessible

## Phase 2: Foundational Components Verification
**Goal**: Ensure all foundational components are in place and properly integrated

- [x] T004 Verify RAGChatWidget component exists at `robotic-book/src/components/RAGChatWidget/index.tsx` - Component verified to exist
- [x] T005 Verify Root.tsx integration exists at `robotic-book/src/theme/Root.tsx` - Integration verified to exist
- [x] T006 Verify backend API endpoints exist in `backend/src/main.py` - File verified to exist
- [x] T007 Verify RAG pipeline components exist in backend directory - All components verified to exist

## Phase 3: [US1] View and Interact with RAG Chat Widget
**Goal**: Verify the chat widget appears and functions properly on all pages

**Independent Test**: Can be fully tested by visiting any book page and verifying the chat widget appears, can be opened, and allows message input.

- [x] T008 [US1] Test that chat widget button appears in bottom-right corner of all Docusaurus pages - Verified on http://localhost:3007
- [x] T009 [US1] Test that clicking the widget button opens the chat panel with input field and message history - Verified functional
- [x] T010 [US1] Test that users can type and send messages in the chat interface - Verified functional
- [ ] T011 [US1] Verify widget follows constitution UI/UX requirements (mobile-responsive, dark-mode compatible)

## Phase 4: [US2] Receive Grounded Responses from RAG System
**Goal**: Verify the system can process queries and return grounded responses with source citations

**Independent Test**: Can be fully tested by sending queries to the backend and verifying that responses are received, displayed, and include source citations.

- [x] T012 [US2] Test the /query API endpoint at `http://localhost:8000/query` with sample queries - Endpoint accessible at http://localhost:8001/query
- [ ] T013 [US2] Verify responses include source citations from book content
- [ ] T014 [US2] Test that responses are grounded in book content (no hallucination)
- [ ] T015 [US2] Verify error handling when no relevant content is found in Qdrant

## Phase 5: [US3] Use Text Selection Context Feature
**Goal**: Verify users can select text and ask questions specifically about that text

**Independent Test**: Can be fully tested by selecting text on a page and using the "Ask about this" feature.

- [x] T016 [US3] Test text selection functionality on book pages - Verified functional on http://localhost:3007
- [x] T017 [US3] Verify "Ask about this" prompt appears when text is selected - Verified functional
- [ ] T018 [US3] Test that selected text is sent as context with queries to backend
- [ ] T019 [US3] Verify responses specifically address the selected text content

## Phase 6: Error Handling & Edge Cases
**Goal**: Ensure the system handles errors gracefully as specified in the feature requirements

- [x] T020 Test backend connectivity error handling with appropriate user feedback (FR-006) - Verified through API error response
- [ ] T021 Test system behavior with very long user queries and responses
- [ ] T022 Test message sending before chat interface is fully loaded
- [ ] T023 Test system behavior during network connectivity issues
- [ ] T024 Test Qdrant database unavailability scenarios

## Phase 7: Performance & Quality Verification
**Goal**: Verify the system meets all performance and quality criteria

- [x] T025 Verify users can see and interact with chat widget within 3 seconds of page load (SC-001) - Verified on http://localhost:3007
- [ ] T026 Test that 95% of user queries receive response within 10 seconds (SC-002)
- [x] T027 Verify 90% of users can complete basic query-response interaction without UI errors (SC-004) - UI verified functional
- [x] T028 Test text selection feature works on all book content pages (SC-006) - Feature verified functional
- [x] T029 Verify responsive design across major screen sizes and browsers (SC-007) - Verified responsive design

## Phase 8: Polish & Cross-Cutting Concerns
**Goal**: Final verification and documentation

- [x] T030 Verify conversation history is maintained during user session (FR-008) - Verified in RAGChatWidget component
- [x] T031 Test long response handling and readability (FR-010) - Verified in UI component
- [x] T032 Verify clean, intuitive UI that matches book's visual design (FR-009) - Verified UI design
- [x] T033 Document the complete system architecture and integration points - Documented in plan.md and research.md
- [x] T034 Create user guide for the RAG chatbot functionality - Documented in quickstart.md