# Implementation Plan: Course AI Chat Widget

**Branch**: `002-course-ai-chat-widget` | **Date**: 2025-12-09 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/002-course-ai-chat-widget/spec.md`

**Note**: This template is filled in by the `/sp.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

The Course AI Chat Widget enables students to ask questions about course content directly within the Docusaurus website without leaving the page. The widget uses a lightweight React component (bottom-right, click-to-open) that sends user queries with page context to a FastAPI backend. The backend implements a RAG (Retrieval-Augmented Generation) pipeline using the context7 MCP server to retrieve relevant book content, which is then sent to Claude for grounded, context-aware responses. This approach ensures instant, accurate help while maintaining zero layout disruption and full dark-mode compatibility.

## Technical Context

**Language/Version**:
- Frontend: TypeScript 5.6.2, React 19.0.0
- Backend: Python 3.11+

**Primary Dependencies**:
- Frontend: Docusaurus 3.9.2, React 19, CSS Modules (no additional libraries)
- Backend: FastAPI 0.104.1+, Pydantic 2.5.0+, httpx 0.25.2+ (for MCP client)

**Storage**: N/A (stateless design, no persistence required)

**Testing**:
- Frontend: Jest + React Testing Library
- Backend: pytest
- Integration: Manual E2E (user query → backend → mock MCP → response)

**Target Platform**:
- Frontend: Modern browsers (Chrome 90+, Firefox 88+, Safari 14+, Edge 90+), mobile responsive
- Backend: Linux/Windows server (Docker-compatible)

**Project Type**: Web application (separated frontend + backend)

**Performance Goals**:
- Frontend: <100ms UI response time (open/close/typing)
- Backend: <2s p95 API response time (including MCP/Claude calls)
- Bundle size: <50KB additional JavaScript (widget only)

**Constraints**:
- Zero heavy dependencies (no Tidio, Intercom, Redux, Tailwind)
- Must work with Docusaurus 2 (no swizzling core components)
- Mobile-first, dark-mode safe, WCAG 2.1 AA accessible
- Fixed positioning only (no layout shifts)

**Scale/Scope**:
- Expected users: 100-500 concurrent students
- Message history: Max 50 messages per session (client-side limit)
- API rate limit: 10 requests/minute per IP
- Book content: ~20 chapters, ~100 sections (for MCP embeddings)

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Principle | Requirement | Status | Justification |
|-----------|-------------|--------|---------------|
| **Minimal Dependencies** | Lightweight architecture, no heavy libraries | ✅ PASS | React component uses only Docusaurus built-in React 19, CSS Modules. Backend uses FastAPI (lightweight). Zero third-party chat SDKs. |
| **User-Centric Design** | Mobile-first, accessible interfaces | ✅ PASS | Responsive breakpoints (desktop: 400px width, mobile: full-width minus 40px margins). WCAG 2.1 AA: keyboard nav, ARIA labels, focus management. Touch targets ≥44px. |
| **Zero Layout Breaks** | No layout-breaking changes | ✅ PASS | Widget uses `position: fixed` with `bottom: 20px; right: 20px`. No impact on document flow. Docusaurus Root wrapper pattern (no swizzling). |
| **Dark Mode Compatible** | Works in light and dark themes | ✅ PASS | All colors use Docusaurus CSS variables: `--ifm-background-surface-color`, `--ifm-font-color-base`, `--ifm-color-primary`. Auto-adapts to theme switches. |
| **Performance** | Lightweight components | ✅ PASS | Widget lazy-loaded on first interaction (React.lazy). Message history capped at 50 items. No blocking scripts on page load. Bundle size <50KB. |
| **Claude via MCP** | Use approved AI technologies | ✅ PASS | Backend integrates context7 MCP server for embeddings retrieval, then calls Claude for response generation (per constitution Section 14.3). |
| **RAG Pipeline** | Grounded responses only | ✅ PASS | Strict RAG flow: 1) Chunk book content, 2) Store embeddings, 3) Retrieve relevant snippets, 4) Send to Claude with "only answer from provided context" constraint. No hallucination allowed (constitution Section 14.4). |
| **Privacy & Safety** | No PII collection, secure API calls | ✅ PASS | No localStorage/cookies. Session IDs not logged. MCP credentials server-side only. CORS restricted to Docusaurus domain. Rate limiting (10 req/min per IP). |

**Re-Check After Phase 1 Design**: All gates remain PASS. No constitution violations detected.

## Project Structure

### Documentation (this feature)

```text
specs/002-course-ai-chat-widget/
├── plan.md              # This file (/sp.plan command output)
├── research.md          # Phase 0 output: Technology decisions ✅
├── data-model.md        # Phase 1 output: Entities & validation ✅
├── quickstart.md        # Phase 1 output: Developer setup guide ✅
├── contracts/           # Phase 1 output: API specifications ✅
│   └── chat-api.yaml    # OpenAPI 3.0 specification
└── tasks.md             # Phase 2 output (/sp.tasks command - NOT YET CREATED)
```

### Source Code (repository root)

```text
humanoid-robotic-book/
├── robotic-book/                          # Docusaurus frontend
│   ├── src/
│   │   ├── components/
│   │   │   ├── CourseChatWidget/          # ← NEW: Chat widget feature
│   │   │   │   ├── index.tsx              # Main component logic
│   │   │   │   ├── types.ts               # TypeScript interfaces
│   │   │   │   └── styles.module.css      # Component styles
│   │   │   ├── ChatbotUI.jsx              # EXISTING: Legacy chatbot (to be replaced/removed)
│   │   │   ├── Citation.js                # EXISTING: Book citation component
│   │   │   ├── CodeExample.js             # EXISTING: Code snippet component
│   │   │   └── Diagram.js                 # EXISTING: Diagram renderer
│   │   ├── theme/
│   │   │   └── Root.js                    # ← NEW: Global widget wrapper
│   │   ├── pages/
│   │   │   └── index.tsx                  # EXISTING: Homepage
│   │   └── css/
│   │       └── custom.css                 # EXISTING: Theme variables
│   ├── docs/                              # EXISTING: Book content (Markdown)
│   ├── docusaurus.config.ts               # EXISTING: Docusaurus configuration
│   ├── package.json                       # EXISTING: Frontend dependencies
│   └── tsconfig.json                      # EXISTING: TypeScript config
│
├── book-backend/                          # FastAPI backend
│   ├── app/
│   │   ├── main.py                        # EXISTING: FastAPI app entry point
│   │   ├── routes/
│   │   │   └── chat.py                    # ← NEW: Chat endpoint
│   │   ├── services/
│   │   │   └── mcp_client.py              # ← NEW: context7 MCP integration
│   │   └── models/
│   │       └── schemas.py                 # ← NEW: Pydantic request/response models
│   ├── tests/                             # ← NEW: Backend tests
│   │   ├── test_chat_api.py               # API endpoint tests
│   │   └── test_mcp_client.py             # MCP client tests
│   ├── requirements.txt                   # EXISTING: Python dependencies
│   └── .env.example                       # ← NEW: Environment variable template
│
└── specs/002-course-ai-chat-widget/       # This directory
    └── [documentation files listed above]
```

**Structure Decision**: Web application with separated frontend (Docusaurus/React) and backend (FastAPI). This structure was chosen because:

1. **Docusaurus Frontend**: Existing `robotic-book/` directory is the established Docusaurus site. Widget integrates as a new component under `src/components/CourseChatWidget/` with global activation via `src/theme/Root.js` (Docusaurus pattern for site-wide features).

2. **FastAPI Backend**: Existing `book-backend/` directory already contains FastAPI infrastructure. New chat feature adds:
   - `/routes/chat.py` for REST endpoint
   - `/services/mcp_client.py` for MCP server integration
   - `/models/schemas.py` for Pydantic validation

3. **Separation Rationale**:
   - Security: MCP credentials stay server-side
   - Scalability: Backend can be deployed independently
   - Performance: Server-side caching, rate limiting
   - Constitution compliance: "Lightweight frontend" (no heavy client-side ML)

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

**No violations detected.** All constitution checks passed. This section is intentionally left blank as there are no complexity justifications required.

---

## Implementation Phases

### Phase 0: Research (✅ COMPLETE)

**Objective**: Resolve all technical unknowns and document technology decisions.

**Deliverables**:
- ✅ `research.md` created with 15 technical decisions documented
- ✅ All "NEEDS CLARIFICATION" items resolved

**Key Decisions Made**:
1. Architecture: Client-side widget + backend RAG API
2. Integration: Docusaurus Root wrapper (no swizzling)
3. State management: React useState (no Redux/Zustand)
4. Styling: CSS Modules + Docusaurus theme variables
5. Page context: Client-side DOM parsing
6. MCP integration: Backend-only (FastAPI → context7)
7. Interaction: Click-to-open with slide-up animation
8. Mobile: Adaptive layout with breakpoint-based sizing
9. Performance: Lazy loading + 50 message limit
10. Accessibility: WCAG 2.1 AA (keyboard nav, ARIA)
11. Error handling: Graceful degradation with retry
12. API contract: REST with JSON payloads
13. Testing: Unit (Jest/pytest) + integration tests
14. Deployment: Static frontend (GitHub Pages) + separate backend service
15. Security: API key protection, rate limiting, input sanitization

---

### Phase 1: Design & Contracts (✅ COMPLETE)

**Objective**: Define data models, API contracts, and developer documentation.

**Deliverables**:
- ✅ `data-model.md` created with 8 core entities:
  - Message, ChatSession, PageContext, ChatRequest, ChatResponse, Source, ResponseMetadata, ErrorState
- ✅ TypeScript type definitions for frontend
- ✅ Pydantic models for backend validation
- ✅ `contracts/chat-api.yaml` created (OpenAPI 3.0 specification):
  - POST `/api/v1/chat` endpoint
  - GET `/api/v1/health` endpoint
  - Request/response schemas with validation rules
  - Error responses (400, 429, 500, 503)
  - Rate limiting headers
- ✅ `quickstart.md` created with:
  - Step-by-step setup guide (6 steps)
  - Code examples for widget component, API endpoint
  - Troubleshooting section

**Agent Context Update**: To be performed via `.specify/scripts/powershell/update-agent-context.ps1 -AgentType claude`

---

### Phase 2: Task Generation (⏳ PENDING)

**Objective**: Generate actionable, dependency-ordered tasks for implementation.

**Command**: `/sp.tasks`

**Expected Output**: `tasks.md` with:
- Prioritized user stories (P1, P2, P3)
- Granular tasks for frontend widget implementation
- Granular tasks for backend API implementation
- MCP integration tasks
- Testing tasks (unit + integration)
- Deployment tasks

**Estimated Task Count**: 20-30 tasks

---

## Design Artifacts Summary

| Artifact | Status | Location | Purpose |
|----------|--------|----------|---------|
| Research | ✅ Complete | `research.md` | Technology decisions & rationale |
| Data Model | ✅ Complete | `data-model.md` | Entities, relationships, validation rules |
| API Contract | ✅ Complete | `contracts/chat-api.yaml` | OpenAPI 3.0 specification |
| Quickstart Guide | ✅ Complete | `quickstart.md` | Developer setup & implementation guide |
| Implementation Plan | ✅ Complete | `plan.md` (this file) | Overall architecture & execution plan |
| Tasks | ⏳ Pending | `tasks.md` | Actionable implementation tasks (Phase 2) |

---

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                     Docusaurus Website                          │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │  Book Content (Markdown Docs)                             │  │
│  │  ┌────────┐ ┌────────┐ ┌────────┐                        │  │
│  │  │Chapter1│ │Chapter2│ │ ...    │                        │  │
│  │  └────────┘ └────────┘ └────────┘                        │  │
│  └───────────────────────────────────────────────────────────┘  │
│                                                                  │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │  src/theme/Root.js (Global Wrapper)                       │  │
│  │  ┌─────────────────────────────────────────────────────┐  │  │
│  │  │  CourseChatWidget (React Component)                  │  │  │
│  │  │  ┌──────────────────────────────────────────────┐    │  │  │
│  │  │  │  State: isOpen, messages[], isLoading        │    │  │  │
│  │  │  │  UI: Icon → Panel (header + messages + input) │    │  │  │
│  │  │  │  Style: CSS Modules + Theme Variables        │    │  │  │
│  │  │  └──────────────────────────────────────────────┘    │  │  │
│  │  └─────────────────────────────────────────────────────┘  │  │
│  └───────────────────────────────────────────────────────────┘  │
└────────────────────────┬────────────────────────────────────────┘
                         │ REST API Call
                         │ POST /api/v1/chat
                         │ { user_query, page_context }
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│                    FastAPI Backend                              │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │  /routes/chat.py                                          │  │
│  │  ┌─────────────────────────────────────────────────────┐  │  │
│  │  │  1. Validate request (Pydantic)                     │  │  │
│  │  │  2. Extract page context + user query              │  │  │
│  │  │  3. Call MCP client service                        │  │  │
│  │  └─────────────────────────────────────────────────────┘  │  │
│  └───────────────────────────────────────────────────────────┘  │
│                         │                                        │
│                         ▼                                        │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │  /services/mcp_client.py                                  │  │
│  │  ┌─────────────────────────────────────────────────────┐  │  │
│  │  │  A. Query context7 MCP for relevant embeddings     │  │  │
│  │  │     Input: user_query + page_context               │  │  │
│  │  │     Output: Top 3-5 relevant book snippets         │  │  │
│  │  │                                                     │  │  │
│  │  │  B. Send to Claude via MCP                         │  │  │
│  │  │     Prompt: "Answer based ONLY on this context:"  │  │  │
│  │  │     Context: Retrieved snippets from step A        │  │  │
│  │  │     Query: user_query                              │  │  │
│  │  │     Output: Grounded response from Claude          │  │  │
│  │  └─────────────────────────────────────────────────────┘  │  │
│  └───────────────────────────────────────────────────────────┘  │
│                         │                                        │
│                         ▼                                        │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │  Response: { response_text, sources[], metadata }         │  │
│  └───────────────────────────────────────────────────────────┘  │
└────────────────────────┬────────────────────────────────────────┘
                         │ JSON Response
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│              CourseChatWidget (Frontend)                        │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │  1. Display bot message in chat panel                   │    │
│  │  2. Render sources as clickable links (optional)        │    │
│  │  3. Auto-scroll to latest message                       │    │
│  └─────────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────────┘
```

---

## Critical Implementation Notes

### 1. Docusaurus Integration (Zero Swizzling)

**Approach**: Create `robotic-book/src/theme/Root.js` to wrap all pages.

**Why**: Docusaurus automatically uses `src/theme/Root.js` as a global wrapper without requiring swizzling or config changes. This is the recommended pattern for site-wide components.

**File Structure**:
```javascript
// robotic-book/src/theme/Root.js
import React from 'react';
import CourseChatWidget from '@site/src/components/CourseChatWidget';

export default function Root({children}) {
  return (
    <>
      {children}
      <CourseChatWidget />
    </>
  );
}
```

### 2. Dark Mode Compatibility

**Critical Rule**: Use ONLY Docusaurus CSS variables. Never hardcode colors.

**Allowed Variables**:
- `--ifm-background-surface-color` (widget background)
- `--ifm-font-color-base` (text color)
- `--ifm-color-primary` (buttons, header)
- `--ifm-color-emphasis-200` (bot message background)
- `--ifm-color-emphasis-300` (borders)
- `--ifm-color-danger` (error banner)

**Testing**: Toggle dark mode in Docusaurus UI. Widget colors must adapt instantly.

### 3. Mobile Responsiveness

**Breakpoint**: 768px (Docusaurus default)

**Desktop (>768px)**:
- Width: 400px fixed
- Position: `bottom: 20px; right: 20px`

**Mobile (≤768px)**:
- Width: `calc(100vw - 40px)` (full width minus margins)
- Position: `bottom: 20px; left: 20px; right: 20px`

### 4. MCP Integration (Backend)

**MCP Server**: context7

**Flow**:
1. Backend calls context7 MCP with query
2. MCP returns embeddings of relevant book sections
3. Backend constructs prompt: "Answer this question using ONLY the following context: [embeddings]. Question: [user_query]"
4. Backend sends prompt to Claude via MCP
5. Claude response is returned to frontend

**Security**: MCP credentials stored in `.env` (server-side only). Never exposed to frontend.

### 5. Performance Budget

| Metric | Target | Measurement |
|--------|--------|-------------|
| Widget JS bundle | <50KB | `npm run build` → check bundle size |
| API response time | <2s p95 | Backend logging + monitoring |
| UI interaction (open/close) | <100ms | Manual testing with DevTools Performance tab |
| First page load impact | 0ms | Widget lazy-loaded on first interaction |

---

## Risks & Mitigation

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| **Claude API rate limits** | Medium | High | Implement server-side caching for repeated queries. Add user-facing rate limit warnings. |
| **MCP server downtime** | Low | High | Graceful degradation: show "AI assistant temporarily unavailable" message. No crash. |
| **Dark mode color mismatch** | Medium | Medium | Strict CSS variable usage. Test in both themes before deployment. |
| **Mobile keyboard covers input** | High | Medium | Adjust viewport on input focus. Add padding-bottom to panel. |
| **Layout shift on widget open** | Low | Critical | Use `position: fixed` + CSS transform. No document reflow. Verify with Lighthouse. |
| **Existing ChatbotUI.jsx conflicts** | Low | Low | Widget uses isolated component structure. Legacy component can coexist temporarily. |

---

## Next Steps (After /sp.plan)

1. **Run `/sp.tasks`** to generate implementation tasks from this plan
2. **Review generated tasks** for completeness and priority
3. **Begin implementation** following task order (likely: frontend widget → backend endpoint → MCP integration → testing)
4. **Create ADR** if any architecturally significant decisions emerge during implementation (use `/sp.adr` command)

---

**Planning Phase Complete**: Ready for task generation (Phase 2).

**Branch**: `002-course-ai-chat-widget`
**Specs Directory**: `D:\Quarter 4\ai-book\humanoid-robotic-book\specs\002-course-ai-chat-widget`
**Artifacts Generated**:
- ✅ research.md
- ✅ data-model.md
- ✅ contracts/chat-api.yaml
- ✅ quickstart.md
- ✅ plan.md (this file)
