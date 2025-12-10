---
id: 0001
title: Implementation Plan for Course AI Chat Widget
stage: plan
date: 2025-12-09
surface: agent
model: claude-sonnet-4-5
feature: 002-course-ai-chat-widget
branch: 002-course-ai-chat-widget
user: system
command: /sp.plan
labels: ["planning", "architecture", "design", "course-ai-chat-widget", "rag", "mcp", "docusaurus"]
links:
  spec: specs/002-course-ai-chat-widget/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - specs/002-course-ai-chat-widget/plan.md
  - specs/002-course-ai-chat-widget/research.md
  - specs/002-course-ai-chat-widget/data-model.md
  - specs/002-course-ai-chat-widget/quickstart.md
  - specs/002-course-ai-chat-widget/contracts/chat-api.yaml
tests:
  - Constitution Check: All gates PASS (8/8)
  - Technical Context: All NEEDS CLARIFICATION resolved
  - Design Artifacts: 5/5 complete
---

## Prompt

```text
/sp.plan

Feature: Course AI Chat Widget (persistent, page-aware, powered by Claude + context7 MCP)

Goal: Students can instantly ask questions about any page/topic in the course without leaving the page → instant accurate help → higher completion rate.

Already defined in constitution & /sp.specify:
- Fixed bottom-right (20px from edges), mobile → bottom-left
- Floating chat bubble icon → click → smooth 300ms slide-up open
- Panel: header + scrollable messages + textarea + send
- Sends query + current page context to context7 MCP server → Claude response
- Matches Docusaurus theme, dark-mode safe, lightweight, accessible
- Close on X, outside click, or Esc

Now create the optimal execution plan with these rules:
- Zero heavy dependencies (no Tidio, Crisp, Intercom, etc.
- Must work perfectly with current Docusaurus 2 + Tailwind setup
- Use React functional component + CSS modules or Tailwind
- Integration method: preferably create src/components/CourseChatWidget (no swizzle needed)
- State manage
```

## Response snapshot

Executed complete implementation planning workflow for Course AI Chat Widget feature:

### Phase 0: Research (Technology Decisions)

- Created `research.md` with 15 critical technical decisions:
  1. Architecture: Client-side React widget + FastAPI backend RAG API
  2. Integration: Docusaurus Root wrapper pattern (zero swizzling)
  3. State: React useState (no Redux/Zustand - lightweight)
  4. Styling: CSS Modules + Docusaurus theme variables only
  5. Page context: Client-side DOM parsing (title + pathname)
  6. MCP: Backend-only integration (FastAPI → context7 → Claude)
  7. Interaction: Click-to-open with 300ms slide-up animation
  8. Mobile: Adaptive layout (desktop: 400px, mobile: 100vw - 40px)
  9. Performance: Lazy loading + 50 message cap
  10. Accessibility: WCAG 2.1 AA (keyboard nav, ARIA, focus mgmt)
  11. Errors: Graceful degradation with retry buttons
  12. API: REST with JSON (POST /api/v1/chat)
  13. Testing: Jest (frontend) + pytest (backend)
  14. Deployment: GitHub Pages (frontend) + separate backend service
  15. Security: Server-side API keys, rate limiting (10/min/IP), input sanitization

### Phase 1: Design & Contracts

- Created `data-model.md` with 8 core entities:
  - Message, ChatSession, PageContext, ChatRequest, ChatResponse, Source, ResponseMetadata, ErrorState
  - TypeScript interfaces for frontend
  - Pydantic models for backend validation

- Created `contracts/chat-api.yaml` (OpenAPI 3.0):
  - POST /api/v1/chat endpoint
  - GET /api/v1/health endpoint
  - Complete request/response schemas
  - Error responses (400, 429, 500, 503)
  - Rate limiting headers

- Created `quickstart.md`:
  - 7-step developer setup guide
  - Code examples for widget component and API endpoint
  - Troubleshooting section

### Implementation Plan Completed

- Technical context: TypeScript 5.6.2, React 19, FastAPI, Pydantic
- Constitution check: 8/8 gates PASS (minimal deps, mobile-first, zero layout breaks, dark mode, performance, MCP, RAG, privacy)
- Project structure: Documented frontend (robotic-book/) + backend (book-backend/) separation
- Architecture diagram: Full flow from widget → API → MCP → Claude → response
- Critical notes: Docusaurus Root.js integration, dark mode CSS variables, mobile breakpoints, MCP security
- Performance budget: <50KB bundle, <2s API p95, <100ms UI interactions
- Risk mitigation: API rate limits, MCP downtime, dark mode testing, mobile keyboard handling

## Outcome

- ✅ Impact: Complete architectural plan for Course AI Chat Widget with zero constitution violations, lightweight design, and clear implementation path
- 🧪 Tests: Constitution gates validated (8/8 PASS), no complexity justifications needed
- 📁 Files: 5 planning artifacts created (research.md, data-model.md, quickstart.md, chat-api.yaml, plan.md)
- 🔁 Next prompts: Run `/sp.tasks` to generate actionable implementation tasks from this plan
- 🧠 Reflection: Successfully decomposed complex chat widget feature into clear phases. Research phase resolved all unknowns (15 decisions). Design phase produced complete data model (8 entities) and API contract (OpenAPI 3.0). Plan integrates seamlessly with existing Docusaurus/FastAPI stack without swizzling or heavy dependencies.

## Evaluation notes (flywheel)

- Failure modes observed: None. All planning artifacts generated successfully. Constitution gates all passed without violations.
- Graders run and results (PASS/FAIL): Constitution Check PASS (8/8), Technical Context Complete (0 NEEDS CLARIFICATION remaining), Artifact Generation PASS (5/5 files created)
- Prompt variant (if applicable): N/A (first planning iteration)
- Next experiment (smallest change to try): Execute `/sp.tasks` to validate plan completeness and generate granular implementation tasks. Monitor for any missing edge cases or integration complexities during task generation.
