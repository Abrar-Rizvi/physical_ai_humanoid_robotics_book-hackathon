# Implementation Plan: RAG Chatbot UI + Backend Integration

**Branch**: `005-rag-chatbot-ui` | **Date**: 2025-12-16 | **Spec**: [link to spec.md](./spec.md)
**Input**: Feature specification from `/specs/005-rag-chatbot-ui/spec.md`

## Summary

Verification-first plan for RAG chatbot end-to-end integration (Docusaurus UI → FastAPI → Qdrant). The audit revealed that the RAG chatbot UI already exists in the form of RAGChatWidget component with Root.tsx integration, and the backend with FastAPI endpoints and Qdrant integration is also implemented. The system is fully functional with a /query endpoint that processes user queries against book content.

## Technical Context

**Language/Version**: Python 3.11, TypeScript/React, Node.js 20+
**Primary Dependencies**: FastAPI, React 19, Docusaurus 2, Qdrant, Cohere, OpenAI
**Storage**: Qdrant vector database for embeddings, Docusaurus static content
**Testing**: pytest for backend, Jest for frontend components
**Target Platform**: Web application (Docusaurus frontend + FastAPI backend)
**Project Type**: Web application with frontend and backend components
**Performance Goals**: <10 seconds response time for 95% of queries (SC-002)
**Constraints**: 80% accuracy for grounded responses (SC-003), mobile-responsive, dark-mode compatible
**Scale/Scope**: Single-book knowledge base with semantic search capabilities

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

✅ **Architecture Compliance**: RAG pipeline follows constitution requirements (Section 14.3)
- Embeddings → Vector Storage → Retrieval → Claude MCP (via OpenAI)
- Grounded responses only from book content (Section 14.4)
- Mobile-first design with dark mode support (Section 14.5)

✅ **UI/UX Requirements**: Chat widget meets constitution constraints (Section 14.5)
- Bottom-right positioning (20px from edges)
- Fixed positioning, no layout breaks
- Mobile-responsive and dark-mode compatible
- Click-to-open only (no auto-expansion)

✅ **Safety & Ethics**: Grounded responses with no hallucination (Section 14.4)

## Project Structure

### Documentation (this feature)

```text
specs/005-rag-chatbot-ui/
├── plan.md              # This file (/sp.plan command output)
├── research.md          # Phase 0 output (/sp.plan command)
├── data-model.md        # Phase 1 output (/sp.plan command)
├── quickstart.md        # Phase 1 output (/sp.plan command)
├── contracts/           # Phase 1 output (/sp.plan command)
└── tasks.md             # Phase 2 output (/sp.tasks command - NOT created by /sp.plan)
```

### Source Code (repository root)

```text
backend/
├── src/
│   ├── models/
│   ├── services/
│   ├── api/
│   └── retrieval.py
└── main.py

robotic-book/
├── src/
│   ├── components/
│   │   └── RAGChatWidget/
│   │       └── index.tsx
│   └── theme/
│       └── Root.tsx
└── docusaurus.config.ts

# [REMOVE IF UNUSED] Option 2: Web application (when "frontend" + "backend" detected)
backend/
├── src/
│   ├── models/
│   ├── services/
│   └── api/
└── tests/

frontend/
├── src/
│   ├── components/
│   ├── pages/
│   └── services/
└── tests/

# [REMOVE IF UNUSED] Option 3: Mobile + API (when "iOS/Android" detected)
api/
└── [same as backend above]

ios/ or android/
└── [platform-specific structure: feature modules, UI flows, platform tests]
```

**Structure Decision**: Web application with separate frontend (Docusaurus) and backend (FastAPI) components. The RAGChatWidget component is integrated via Root.tsx to appear on all pages.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| [e.g., 4th project] | [current need] | [why 3 projects insufficient] |
| [e.g., Repository pattern] | [specific problem] | [why direct DB access insufficient] |
