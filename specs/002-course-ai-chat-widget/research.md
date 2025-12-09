# Research: Course AI Chat Widget

**Feature**: Course AI Chat Widget (002-course-ai-chat-widget)
**Date**: 2025-12-09
**Phase**: 0 - Research & Technical Decisions

## Overview

This document resolves all technical unknowns and clarifies implementation decisions for the Course AI Chat Widget feature. The widget enables students to ask questions about course content directly within the Docusaurus website, powered by Claude via the context7 MCP server.

---

## 1. Architecture Pattern Decision

### Decision: Client-Side Widget with Backend RAG API

**Rationale**:

- Separation of concerns: UI widget remains lightweight and focused on interaction
- Backend handles complex RAG pipeline (embeddings, retrieval, Claude API calls via MCP)
- Enables caching, rate limiting, and monitoring at API layer
- Allows future expansion (analytics, A/B testing, fine-tuning)

**Alternatives Considered**:

1. **Pure client-side with direct MCP calls**: Rejected due to:
   - Security risks (exposing MCP credentials in browser)
   - Cannot implement server-side caching or rate limiting
   - Poor control over Claude API usage/costs

2. **Server-side rendering with full page reload**: Rejected due to:
   - Poor UX (breaks conversational flow)
   - Violates lightweight, non-intrusive design principle
   - Unnecessary complexity for chat interaction

**Implementation Impact**:

- Frontend: React component in `robotic-book/src/components/CourseChatWidget/`
- Backend: FastAPI service (already exists at `book-backend/`)
- Integration: REST API calls from widget to backend

---

## 2. Widget Integration Method

### Decision: Docusaurus Root Component Wrapper (No Swizzling)

**Rationale**:

- Cleanest integration without modifying Docusaurus internals
- Update-safe (won't break on Docusaurus version upgrades)
- Global availability across all pages
- Leverages Docusaurus's built-in Root component pattern

**Alternatives Considered**:

1. **Swizzling Layout component**: Rejected due to:
   - Maintenance burden (custom code for core Docusaurus component)
   - Risk of breaking on Docusaurus updates
   - Constitution constraint: "zero layout breaks"

2. **Plugin-based injection**: Rejected due to:
   - Unnecessary complexity for a single widget
   - Additional build configuration overhead

**Implementation Approach**:

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

---

## 3. State Management

### Decision: React useState (Component-Level State)

**Rationale**:

- Widget state is isolated and ephemeral
- No cross-component state sharing needed
- Aligns with "lightweight, minimal dependencies" principle
- Sufficient for: open/close, messages array, input value, loading state

**Alternatives Considered**:

1. **Redux/Zustand**: Rejected due to:
   - Overkill for single-component state
   - Adds bundle size (~45KB for Redux)
   - Violates "zero heavy dependencies" constraint

2. **Context API**: Rejected due to:
   - No need for state sharing across component tree
   - Unnecessary complexity for isolated widget

**State Schema**:

```typescript
interface WidgetState {
  isOpen: boolean;
  messages: Message[];
  inputValue: string;
  isLoading: boolean;
  error: string | null;
}

interface Message {
  id: string;
  text: string;
  sender: 'user' | 'bot';
  timestamp: number;
}
```

---

## 4. Styling Approach

### Decision: CSS Modules + Docusaurus Theme Variables

**Rationale**:

- Scoped styles prevent conflicts with Docusaurus theme
- Direct access to Docusaurus CSS variables for dark mode compatibility
- No additional build tools or dependencies required
- Already used in existing components (HomepageFeatures)

**Alternatives Considered**:

1. **Tailwind CSS**: Rejected due to:
   - Project already uses CSS Modules pattern
   - Would require additional build configuration
   - Adds ~50KB to bundle (violates lightweight constraint)

2. **Inline styles**: Rejected due to:
   - Cannot access CSS variables for dark mode
   - Poor maintainability for complex animations
   - No media query support for responsive design

**Implementation Pattern**:

```css
/* CourseChatWidget.module.css */
.container {
  position: fixed;
  bottom: 20px;
  right: 20px;
  z-index: var(--ifm-z-index-fixed);
  background: var(--ifm-background-surface-color);
  color: var(--ifm-font-color-base);
}
```

---

## 5. Page Context Extraction

### Decision: Client-Side DOM Parsing with Title + Pathname

**Rationale**:

- No server-side rendering changes required
- Lightweight (<5KB additional code)
- Accurate current page context
- Works seamlessly with Docusaurus routing

**Alternatives Considered**:

1. **URL-based parsing only**: Rejected due to:
   - Less accurate context (URL may not reflect content structure)
   - Misses dynamically generated content

2. **Full page content scraping**: Rejected due to:
   - Performance overhead (large payloads to backend)
   - RAG pipeline already handles retrieval
   - Unnecessary duplication of embeddings work

**Implementation**:

```javascript
function extractPageContext() {
  return {
    title: document.title,
    pathname: window.location.pathname,
    section: document.querySelector('article')?.getAttribute('data-section') || '',
  };
}
```

---

## 6. MCP Integration Architecture

### Decision: Backend-Only MCP Client (FastAPI → context7)

**Rationale**:

- Security: MCP credentials stay server-side
- Performance: Server-to-MCP latency is minimal
- Control: Centralized logging, monitoring, rate limiting
- Aligns with constitution: "Claude via MCP" for RAG chatbot

**MCP Flow**:

1. User query → Frontend → FastAPI endpoint
2. FastAPI extracts page context + query
3. FastAPI calls context7 MCP for relevant book embeddings
4. FastAPI sends retrieved content + query to Claude (via MCP)
5. Claude response → FastAPI → Frontend

**Alternatives Considered**:

1. **Direct browser → MCP**: Rejected (security violation)
2. **Separate MCP proxy service**: Rejected (unnecessary complexity)

---

## 7. Interaction Patterns

### Decision: Click-to-Open Icon with Slide-Up Animation

**Rationale**:

- Meets constitution requirement: "click-to-open only"
- Non-intrusive: icon is small (60×60px)
- Smooth UX: 300ms CSS transition
- Mobile-friendly: large touch target (44×44px minimum)

**Animation Approach**:

```css
.panel {
  transform: translateY(100%);
  transition: transform 300ms cubic-bezier(0.4, 0, 0.2, 1);
}

.panel.open {
  transform: translateY(0);
}
```

**Close Triggers** (per constitution):

- Click on close (X) button
- Click outside widget (useOutsideClick hook)
- Press Escape key (keyboard event listener)

---

## 8. Mobile Responsiveness

### Decision: Adaptive Layout with Breakpoint-Based Sizing

**Rationale**:

- Desktop: Fixed 400px width, bottom-right (20px offsets)
- Mobile: Full-width minus 20px margins, bottom positioning
- Meets constitution: "mobile → bottom-left" positioning

**Breakpoint**:

```css
@media (max-width: 768px) {
  .container {
    left: 20px;
    right: 20px;
    bottom: 20px;
    max-width: calc(100vw - 40px);
  }
}
```

---

## 9. Performance Optimization

### Decision: Lazy Loading + Message Limit

**Rationale**:

- Widget code only loads on first interaction (React.lazy)
- Message history capped at 50 messages (prevent memory bloat)
- Constitution requirement: "No blocking scripts on initial page load"

**Implementation**:

```javascript
const CourseChatWidget = React.lazy(() =>
  import('./CourseChatWidget')
);

// In Root.js
<Suspense fallback={null}>
  <CourseChatWidget />
</Suspense>
```

---

## 10. Accessibility

### Decision: WCAG 2.1 AA Compliance

**Requirements**:

- Keyboard navigation: Tab, Enter, Escape
- ARIA labels: `role="dialog"`, `aria-label="Course chat assistant"`
- Focus management: Trap focus when open, restore on close
- Screen reader announcements for new messages

**Implementation**:

```javascript
<div
  role="dialog"
  aria-label="Course chat assistant"
  aria-modal="true"
>
  {/* Widget content */}
</div>
```

---

## 11. Error Handling

### Decision: Graceful Degradation with Retry

**Error Scenarios**:

1. **Network failure**: Show retry button, cache user input
2. **API error (4xx/5xx)**: Display friendly message, log to console
3. **MCP unavailable**: Fallback message: "AI assistant temporarily unavailable"
4. **Rate limit**: Show cooldown message with timer

**User-Facing Messages**:

- Generic error: "Sorry, I couldn't process that. Please try again."
- Network error: "Connection lost. Check your internet and retry."
- Rate limit: "Too many requests. Please wait 30 seconds."

---

## 12. API Contract (Frontend ↔ Backend)

### Decision: REST API with JSON Payload

**Endpoint**: `POST /api/v1/chat`

**Request**:

```json
{
  "user_query": "What is ROS 2?",
  "page_context": {
    "title": "Chapter 3: ROS 2 Fundamentals",
    "pathname": "/docs/chapter-3"
  },
  "session_id": "optional-session-uuid"
}
```

**Response**:

```json
{
  "response_text": "ROS 2 is...",
  "sources": [
    {"title": "Chapter 3, Section 2", "url": "/docs/chapter-3#section-2"}
  ],
  "metadata": {
    "processing_time_ms": 1230,
    "model_used": "claude-sonnet-4"
  }
}
```

---

## 13. Testing Strategy

### Decision: Unit + Integration Tests

**Frontend Tests** (Jest + React Testing Library):

- Component rendering (open/close states)
- User interactions (typing, sending messages)
- Keyboard navigation (Escape, Enter)
- Accessibility (ARIA attributes, focus management)

**Backend Tests** (pytest):

- API endpoint validation
- MCP integration (mocked)
- Error handling
- Rate limiting

**Integration Tests**:

- End-to-end flow: user query → backend → mock MCP → response
- No real Claude API calls in tests (use fixtures)

---

## 14. Deployment Considerations

### Decision: Static Frontend + Separate Backend Service

**Frontend Deployment**:

- Part of Docusaurus build process
- Deployed to GitHub Pages (current setup)
- No environment variables needed (API URL hardcoded or injected at build)

**Backend Deployment**:

- FastAPI service on separate host (e.g., Render, Railway, AWS Lambda)
- Environment variables: `MCP_API_KEY`, `CLAUDE_API_KEY`, `CORS_ORIGINS`
- CORS configuration to allow Docusaurus domain

**CORS Setup**:

```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://devabdullah90.github.io"],
    allow_methods=["POST"],
    allow_headers=["Content-Type"],
)
```

---

## 15. Security Considerations

### Decision: API Key Protection + Rate Limiting

**Security Measures**:

1. **No client-side secrets**: All MCP/Claude API keys stay in backend
2. **Rate limiting**: 10 requests/minute per IP (prevents abuse)
3. **Input validation**: Sanitize user queries (max 500 chars)
4. **CORS restrictions**: Only allow requests from Docusaurus domain
5. **HTTPS only**: Reject non-HTTPS requests in production

**Input Sanitization**:

```python
from pydantic import BaseModel, validator

class ChatRequest(BaseModel):
    user_query: str

    @validator('user_query')
    def validate_query(cls, v):
        if len(v) > 500:
            raise ValueError('Query too long')
        return v.strip()
```

---

## Risks & Mitigations

| Risk | Impact | Mitigation |
|------|--------|-----------|
| Claude API rate limits | Users get error messages | Implement queue + retry logic |
| Backend downtime | Widget non-functional | Show clear "offline" state, no silent failures |
| Layout shift on widget open | Poor UX, constitution violation | Use `position: fixed` + transform animations |
| Dark mode color mismatch | Accessibility issue | Use Docusaurus CSS variables exclusively |
| Mobile keyboard covering input | Input field hidden | Adjust viewport on focus, add padding |

---

## Next Steps (Phase 1)

1. Generate `data-model.md` with Message, ChatSession, ErrorState entities
2. Create API contract specification in `contracts/chat-api.yaml` (OpenAPI)
3. Write `quickstart.md` with developer setup instructions
4. Update agent context with technology decisions from this research

---

**Research Complete**: All NEEDS CLARIFICATION items resolved. Ready for Phase 1 design.
