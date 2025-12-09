# Implementation Tasks: Course AI Chat Widget

**Feature**: Course AI Chat Widget (002-course-ai-chat-widget)
**Branch**: `002-course-ai-chat-widget`
**Date**: 2025-12-09
**Plan**: [plan.md](./plan.md)

## User Stories (Derived from Requirements)

Based on the implementation plan and requirements, the feature has been decomposed into these independently testable user stories:

### User Story 1: Basic Chat Widget UI (Priority: P1)

**Description**: As a student, I can open a chat widget from any page, type a question, and see a response in the chat panel, so I can get help without leaving the current page.

**Why this priority**: Core MVP functionality. Without this, the feature doesn't exist. Delivers immediate value: students can interact with an AI assistant.

**Independent Test**: Open any Docusaurus page → click chat icon → widget opens → type "test" → send → see message in chat panel. Widget is visible, interactive, and non-intrusive.

**Acceptance Scenarios**:
1. **Given** I'm on any Docusaurus page, **When** I click the floating chat icon (💬), **Then** the chat panel slides up smoothly in 300ms
2. **Given** the chat panel is open, **When** I type a message and press Enter (or click Send), **Then** my message appears as a user bubble on the right
3. **Given** I have messages in the chat, **When** I click the X button, **Then** the panel closes smoothly and the icon reappears

---

### User Story 2: AI-Powered Responses (Priority: P2)

**Description**: As a student, I want my questions to be answered by Claude with relevant information from the course book, so I get accurate, grounded answers specific to the current chapter/page.

**Why this priority**: Delivers the core value proposition: AI-powered help based on course content. Requires backend RAG pipeline (context7 MCP + Claude).

**Independent Test**: Open widget → ask "What is ROS 2?" → receive response containing accurate information from the book → response appears as bot bubble on left. Sources are optionally shown.

**Acceptance Scenarios**:
1. **Given** I'm on the ROS 2 chapter page, **When** I ask "What is ROS 2?", **Then** I receive a response grounded in the chapter content within 2 seconds
2. **Given** I've sent a query, **When** the backend is processing, **Then** I see a loading indicator ("...")
3. **Given** the AI responds, **When** the response includes sources, **Then** I see clickable links to relevant book sections

---

### User Story 3: Error Handling & Resilience (Priority: P3)

**Description**: As a student, I want clear error messages when something goes wrong (network failure, API error), so I know what happened and can retry if possible.

**Why this priority**: Improves user experience by handling failure gracefully. Not required for MVP but critical for production quality.

**Independent Test**: Disconnect from network → send message → see "Connection lost" error banner → reconnect → click retry → message sends successfully.

**Acceptance Scenarios**:
1. **Given** I have no internet connection, **When** I send a message, **Then** I see "Connection lost. Check your internet and retry." with a retry button
2. **Given** the backend returns a 429 rate limit error, **When** I send too many messages, **Then** I see "Too many requests. Please wait 30 seconds." without a retry button
3. **Given** an API error occurs, **When** my message fails, **Then** my message shows an error state and I can retry

---

### User Story 4: Mobile Responsiveness & Accessibility (Priority: P4)

**Description**: As a student on a mobile device or using assistive technology, I can use the chat widget with proper keyboard navigation and screen reader support, so everyone can access help.

**Why this priority**: Ensures inclusivity and constitutional compliance (WCAG 2.1 AA). Important but can be implemented after core functionality.

**Independent Test**: Open on mobile phone (viewport <768px) → widget adapts to full-width layout → use Tab key to navigate → use screen reader → all interactions work correctly.

**Acceptance Scenarios**:
1. **Given** I'm on a mobile device (<768px width), **When** the widget opens, **Then** it takes full width minus 20px margins on each side
2. **Given** I'm using a keyboard only, **When** I press Tab, **Then** I can navigate to the chat icon → input field → send button
3. **Given** I'm using a screen reader, **When** I open the widget, **Then** I hear "Course chat assistant" and can understand the UI structure

---

### User Story 5: Dark Mode & Theme Compatibility (Priority: P5)

**Description**: As a student who prefers dark mode, I want the chat widget to match the Docusaurus theme (light or dark), so the UI feels consistent and doesn't hurt my eyes.

**Why this priority**: Constitution requirement but doesn't block core functionality. Can be implemented alongside US1 with proper CSS variable usage.

**Independent Test**: Toggle Docusaurus theme (light ↔ dark) → widget colors adapt instantly → no hardcoded colors visible → text remains readable in both modes.

**Acceptance Scenarios**:
1. **Given** I have dark mode enabled, **When** I open the widget, **Then** the widget background, text, and buttons use dark theme colors
2. **Given** I toggle from light to dark mode, **When** the widget is open, **Then** the widget colors update instantly without requiring reload
3. **Given** any theme is active, **When** I view the widget, **Then** all text has sufficient contrast (WCAG AA: 4.5:1 ratio)

---

## Edge Cases

- **Widget overlaps footer on short pages**: Use `position: fixed` with `z-index` to ensure widget stays above content
- **Long messages overflow UI**: Implement word-wrap and max-width constraints
- **50 message limit reached**: Automatically remove oldest message when limit exceeded
- **Backend downtime**: Show "AI assistant temporarily unavailable" instead of generic error
- **XSS attempts in user input**: Sanitize input on backend before processing
- **CORS issues in production**: Configure allowed origins correctly in backend
- **Mobile keyboard covers input field**: Adjust viewport or add padding when keyboard appears

---

## Implementation Strategy

### MVP Scope (Recommended First Deployment)

**User Story 1 only**: Basic chat widget UI with mock responses
- Students can open/close widget
- Students can send messages (mock response)
- Zero backend dependency
- Validates UI/UX before backend complexity

**Timeline**: 1-2 days
**Value**: Immediate visual feedback, UX validation, can demo to stakeholders

### Full Feature Scope

**User Stories 1-5 complete**: Production-ready chat widget
- US1: Widget UI ✅
- US2: AI responses (backend + MCP integration)
- US3: Error handling
- US4: Mobile + accessibility
- US5: Dark mode (can be done in parallel with US1)

**Timeline**: 5-7 days
**Value**: Complete, production-quality feature

---

## Task Organization

Tasks are organized into phases:
1. **Phase 1: Setup** - Project initialization, dependencies
2. **Phase 2: Foundational** - Shared infrastructure needed by all user stories
3. **Phase 3: User Story 1** - Basic chat widget UI (MVP)
4. **Phase 4: User Story 2** - AI-powered responses (backend + RAG)
5. **Phase 5: User Story 3** - Error handling
6. **Phase 6: User Story 4** - Mobile & accessibility
7. **Phase 7: User Story 5** - Dark mode (can be done earlier)
8. **Phase 8: Polish** - Cross-cutting concerns, optimization

Tasks marked with **[P]** can be executed in parallel (different files, no blocking dependencies).

---

## Phase 1: Setup & Project Initialization

**Goal**: Prepare development environment and project structure for implementation.

**Tasks**:

- [X] T001 Create feature branch `002-course-ai-chat-widget` from main
- [X] T002 [P] Create frontend component directory structure: `robotic-book/src/components/CourseChatWidget/`
- [X] T003 [P] Create backend route directory: `book-backend/app/routes/` (if not exists)
- [X] T004 [P] Create backend services directory: `book-backend/app/services/` (if not exists)
- [X] T005 [P] Create backend models directory: `book-backend/app/models/` (if not exists)
- [X] T006 Install frontend dependencies (verify React 19, TypeScript 5.6.2 in `robotic-book/package.json`)
- [X] T007 Install backend dependencies: `fastapi==0.104.1`, `pydantic==2.5.0`, `httpx==0.25.2` in `book-backend/requirements.txt`
- [X] T008 Create `.env.example` file in `book-backend/` with MCP credential placeholders

**Validation**:
- All directories exist and are committed to git
- Dependencies installed successfully
- Backend runs: `uvicorn app.main:app --reload` (no errors)
- Frontend runs: `npm start` (no errors)

---

## Phase 2: Foundational Infrastructure

**Goal**: Build shared infrastructure needed by all user stories.

**Tasks**:

- [X] T009 [P] Create TypeScript type definitions in `robotic-book/src/components/CourseChatWidget/types.ts` (Message, ChatSession, PageContext, ChatRequest, ChatResponse, WidgetState, ErrorState)
- [X] T010 [P] Create Pydantic models in `book-backend/app/models/schemas.py` (PageContext, ChatRequest, ChatResponse, Source, ResponseMetadata)
- [X] T011 [P] Update FastAPI main app in `book-backend/app/main.py` to include CORS middleware (allow `http://localhost:3000` and production domain)
- [X] T012 Create health check endpoint `GET /health` in `book-backend/app/main.py`

**Validation**:
- Type definitions compile without errors
- Pydantic models validate correctly (run `pytest` if tests exist)
- CORS allows requests from Docusaurus dev server
- Health check returns 200: `curl http://localhost:8000/health`

---

## Phase 3: User Story 1 - Basic Chat Widget UI (MVP)

**Goal**: Implement functional chat widget UI with open/close, message display, and mock responses.

**Independent Test**: Open widget → type message → send → see user message + mock bot response → close widget. All interactions work smoothly.

### Frontend Tasks

- [X] T013 [US1] Create widget component scaffold in `robotic-book/src/components/CourseChatWidget/index.tsx` with basic state (isOpen, messages, inputValue, isLoading)
- [X] T014 [US1] Implement `generateId()` helper function for message IDs in `robotic-book/src/components/CourseChatWidget/index.tsx`
- [X] T015 [US1] Implement `extractPageContext()` function to get title + pathname in `robotic-book/src/components/CourseChatWidget/index.tsx`
- [X] T016 [US1] Build toggle button (💬 icon) with click handler in `robotic-book/src/components/CourseChatWidget/index.tsx`
- [X] T017 [US1] Build chat panel JSX structure (header, messages container, input container) in `robotic-book/src/components/CourseChatWidget/index.tsx`
- [X] T018 [US1] Implement message rendering (user/bot bubbles) in `robotic-book/src/components/CourseChatWidget/index.tsx`
- [X] T019 [US1] Implement `sendMessage()` function with mock response (no API call yet) in `robotic-book/src/components/CourseChatWidget/index.tsx`
- [X] T020 [US1] Add auto-scroll to latest message (useEffect with messagesEndRef) in `robotic-book/src/components/CourseChatWidget/index.tsx`
- [X] T021 [US1] Add focus management (focus input when widget opens) in `robotic-book/src/components/CourseChatWidget/index.tsx`
- [X] T022 [US1] Implement keyboard support (Enter to send, Escape to close) in `robotic-book/src/components/CourseChatWidget/index.tsx`

### Styling Tasks

- [X] T023 [P] [US1] Create CSS Module file `robotic-book/src/components/CourseChatWidget/styles.module.css`
- [X] T024 [P] [US1] Style toggle button (fixed position, bottom-right, 60×60px, circular) in `styles.module.css`
- [X] T025 [P] [US1] Style chat panel (400px width, 500px height, fixed position, slide-up animation) in `styles.module.css`
- [X] T026 [P] [US1] Style header (primary color background, white text, close button) in `styles.module.css`
- [X] T027 [P] [US1] Style messages container (scrollable, flex column, gap) in `styles.module.css`
- [X] T028 [P] [US1] Style user/bot message bubbles (different colors, alignment) in `styles.module.css`
- [X] T029 [P] [US1] Style input container (flex row, input + send button) in `styles.module.css`
- [X] T030 [P] [US1] Add slide-up animation (@keyframes, 300ms cubic-bezier) in `styles.module.css`

### Integration Tasks

- [X] T031 [US1] Create Docusaurus Root wrapper in `robotic-book/src/theme/Root.js` to include CourseChatWidget globally
- [X] T032 [US1] Test widget on multiple Docusaurus pages (homepage, docs page, about page) to verify global presence

**Phase 3 Validation**:
- ✅ Widget icon appears bottom-right on all pages
- ✅ Click icon → panel slides up in 300ms
- ✅ Type message → press Enter → user bubble appears on right
- ✅ Mock bot response appears on left after 1 second
- ✅ Click X → panel closes smoothly
- ✅ Press Escape → panel closes
- ✅ Messages auto-scroll to latest
- ✅ Input field gets focus when panel opens

**Phase 3 Parallel Opportunities**:
- T023-T030 (all styling tasks) can run in parallel if one developer works on component logic (T013-T022) and another on CSS

---

## Phase 4: User Story 2 - AI-Powered Responses (Backend + RAG)

**Goal**: Integrate FastAPI backend with context7 MCP server and Claude to provide grounded AI responses.

**Independent Test**: Send query "What is ROS 2?" from widget → backend retrieves relevant embeddings → Claude responds with accurate information → response appears in widget within 2 seconds.

### Backend API Tasks

- [ ] T033 [US2] Create chat endpoint `POST /api/v1/chat` in `book-backend/app/routes/chat.py` with request validation (Pydantic)
- [ ] T034 [US2] Implement request logging (log user_query + page_context, sanitize PII) in `book-backend/app/routes/chat.py`
- [ ] T035 [US2] Add response timing tracking (start_time, processing_time_ms) in `book-backend/app/routes/chat.py`
- [ ] T036 [US2] Create mock response logic (temporary, before MCP integration) in `book-backend/app/routes/chat.py`
- [ ] T037 [US2] Mount chat router to main app in `book-backend/app/main.py` with prefix `/api/v1`

### MCP Integration Tasks

- [ ] T038 [US2] Create MCP client service in `book-backend/app/services/mcp_client.py` with context7 connection setup
- [ ] T039 [US2] Implement `retrieve_embeddings(query: str, page_context: PageContext)` function in `mcp_client.py` to query context7
- [ ] T040 [US2] Implement `call_claude(query: str, retrieved_content: list)` function in `mcp_client.py` to send prompt to Claude
- [ ] T041 [US2] Build grounding prompt template: "Answer based ONLY on this context: {retrieved_content}. Question: {query}" in `mcp_client.py`
- [ ] T042 [US2] Add MCP error handling (connection failures, timeout, empty responses) in `mcp_client.py`
- [ ] T043 [US2] Replace mock response in chat endpoint with real MCP client call in `book-backend/app/routes/chat.py`

### Frontend API Integration Tasks

- [ ] T044 [US2] Update `sendMessage()` function in `robotic-book/src/components/CourseChatWidget/index.tsx` to call `POST /api/v1/chat` with fetch
- [ ] T045 [US2] Add API base URL configuration (dev: `http://localhost:8000/api/v1`, prod: production URL) in `index.tsx`
- [ ] T046 [US2] Implement loading state (set isLoading true → false) in `index.tsx`
- [ ] T047 [US2] Display loading indicator ("..." bubble) in messages container in `index.tsx`
- [ ] T048 [US2] Parse ChatResponse and create bot message with response_text in `index.tsx`
- [ ] T049 [P] [US2] Optionally render sources as clickable links below bot message in `index.tsx`

**Phase 4 Validation**:
- ✅ Backend returns 200 for valid requests
- ✅ Backend validates requests (400 for invalid input)
- ✅ MCP client retrieves embeddings from context7
- ✅ Claude returns grounded responses (no hallucination)
- ✅ Frontend displays bot responses within 2 seconds (p95)
- ✅ Sources render as clickable links (if provided)
- ✅ API errors are logged (not exposed to user yet - that's US3)

**Phase 4 Parallel Opportunities**:
- T038-T042 (MCP integration) can run in parallel with T033-T037 (API endpoint with mock) if two developers work separately
- T049 (sources rendering) can run in parallel with core API integration

---

## Phase 5: User Story 3 - Error Handling & Resilience

**Goal**: Gracefully handle network failures, API errors, and rate limiting with user-friendly messages.

**Independent Test**: Disconnect network → send message → see "Connection lost" error → reconnect → click retry → message sends successfully.

### Frontend Error Handling Tasks

- [ ] T050 [US3] Add errorMessage state to WidgetState in `robotic-book/src/components/CourseChatWidget/index.tsx`
- [ ] T051 [US3] Implement try-catch in `sendMessage()` to catch fetch errors in `index.tsx`
- [ ] T052 [US3] Detect network errors (fetch rejection) and set errorMessage: "Connection lost..." in `index.tsx`
- [ ] T053 [US3] Detect rate limit (HTTP 429) and set errorMessage: "Too many requests..." in `index.tsx`
- [ ] T054 [US3] Detect API errors (HTTP 4xx/5xx) and set errorMessage: "Sorry, I couldn't process that..." in `index.tsx`
- [ ] T055 [US3] Update message status from 'pending' to 'error' on failure in `index.tsx`
- [ ] T056 [US3] Render error banner component above input container in `index.tsx`
- [ ] T057 [US3] Add retry button in error banner (only for network/API errors, not rate limit) in `index.tsx`
- [ ] T058 [US3] Implement retry logic (re-send last failed message) in `index.tsx`

### Backend Error Handling Tasks

- [ ] T059 [P] [US3] Add rate limiting middleware (10 requests/minute per IP) in `book-backend/app/main.py` using slowapi or custom logic
- [ ] T060 [P] [US3] Return 429 with Retry-After header when rate limit exceeded in rate limiting middleware
- [ ] T061 [P] [US3] Add global exception handler for unexpected errors in `book-backend/app/main.py`
- [ ] T062 [P] [US3] Return 503 when MCP server is unavailable in `book-backend/app/routes/chat.py`

### Styling Tasks

- [ ] T063 [P] [US3] Style error banner (red background, white text, center-aligned) in `robotic-book/src/components/CourseChatWidget/styles.module.css`
- [ ] T064 [P] [US3] Style retry button (white background, red text, margin-top) in `styles.module.css`
- [ ] T065 [P] [US3] Style error message status indicator (red dot, italic text) in `styles.module.css`

**Phase 5 Validation**:
- ✅ Network error → user sees "Connection lost" + retry button
- ✅ Retry button → message re-sends successfully
- ✅ Rate limit (send 11 messages in 1 minute) → user sees "Too many requests" + no retry button
- ✅ API error (backend returns 500) → user sees generic error + retry button
- ✅ MCP downtime → user sees "AI assistant temporarily unavailable"
- ✅ Error banner disappears after successful retry

**Phase 5 Parallel Opportunities**:
- T059-T062 (backend error handling) and T050-T058 (frontend error handling) can run in parallel
- T063-T065 (styling) can run in parallel with error logic implementation

---

## Phase 6: User Story 4 - Mobile Responsiveness & Accessibility

**Goal**: Ensure widget works on mobile devices and meets WCAG 2.1 AA accessibility standards.

**Independent Test**: Open on mobile (<768px) → widget adapts to full-width layout → use keyboard only (Tab navigation) → use screen reader (NVDA/JAWS) → all functionality accessible.

### Mobile Responsiveness Tasks

- [ ] T066 [P] [US4] Add mobile breakpoint media query (@media (max-width: 768px)) in `robotic-book/src/components/CourseChatWidget/styles.module.css`
- [ ] T067 [P] [US4] Set widget width to `calc(100vw - 40px)` on mobile in `styles.module.css`
- [ ] T068 [P] [US4] Adjust positioning to `left: 20px; right: 20px; bottom: 20px` on mobile in `styles.module.css`
- [ ] T069 [P] [US4] Ensure touch targets are ≥44px (icon button, send button, close button) in `styles.module.css`
- [ ] T070 [P] [US4] Test on mobile device (Chrome DevTools mobile view + real device) and verify no horizontal scroll

### Accessibility Tasks

- [ ] T071 [US4] Add ARIA attributes: `role="dialog"`, `aria-label="Course chat assistant"`, `aria-modal="true"` to panel in `robotic-book/src/components/CourseChatWidget/index.tsx`
- [ ] T072 [US4] Add `aria-label` to toggle button: "Open course chat assistant" in `index.tsx`
- [ ] T073 [US4] Add `aria-label` to close button: "Close chat" in `index.tsx`
- [ ] T074 [US4] Add `aria-label` to send button: "Send message" in `index.tsx`
- [ ] T075 [US4] Implement focus trap (Tab cycles within panel when open) in `index.tsx`
- [ ] T076 [US4] Restore focus to toggle button when panel closes in `index.tsx`
- [ ] T077 [US4] Add screen reader announcements for new messages (aria-live="polite" region) in `index.tsx`
- [ ] T078 [US4] Test with keyboard only (Tab, Enter, Escape) to verify all interactions work
- [ ] T079 [US4] Test with screen reader (NVDA on Windows or VoiceOver on macOS) to verify semantic structure

**Phase 6 Validation**:
- ✅ Mobile (<768px): Widget full-width minus margins, no layout overflow
- ✅ Touch targets: All buttons ≥44×44px
- ✅ Keyboard navigation: Tab moves through icon → input → send → close
- ✅ Enter key sends message, Escape closes panel
- ✅ Focus trap: Tab stays within panel when open
- ✅ Focus restoration: Focus returns to icon when panel closes
- ✅ Screen reader: Announces "Course chat assistant" on open
- ✅ Screen reader: New messages announced via aria-live
- ✅ Color contrast: All text meets 4.5:1 ratio (WCAG AA)

**Phase 6 Parallel Opportunities**:
- T066-T070 (mobile CSS) and T071-T079 (accessibility) can run in parallel if one developer handles CSS and another handles ARIA/focus management

---

## Phase 7: User Story 5 - Dark Mode & Theme Compatibility

**Goal**: Ensure widget adapts to Docusaurus light/dark themes using CSS variables.

**Independent Test**: Toggle Docusaurus theme switcher (light ↔ dark) → widget colors update instantly → verify no hardcoded colors → text remains readable.

**Note**: This can be done earlier (alongside Phase 3) if CSS variables are used from the start.

### Dark Mode Tasks

- [ ] T080 [P] [US5] Replace all hardcoded colors with Docusaurus CSS variables in `robotic-book/src/components/CourseChatWidget/styles.module.css`:
  - `background: var(--ifm-background-surface-color)`
  - `color: var(--ifm-font-color-base)`
  - `background (header/buttons): var(--ifm-color-primary)`
  - `background (bot message): var(--ifm-color-emphasis-200)`
  - `border: var(--ifm-color-emphasis-300)`
  - `background (error): var(--ifm-color-danger)`
- [ ] T081 [US5] Test widget in light mode: verify all colors use theme variables
- [ ] T082 [US5] Toggle to dark mode: verify widget colors update instantly (no page reload needed)
- [ ] T083 [US5] Test contrast ratios in both modes using browser DevTools (Lighthouse accessibility audit)
- [ ] T084 [US5] Verify no hardcoded hex/rgb colors remain in styles.module.css (grep search for `#` and `rgb(`)

**Phase 7 Validation**:
- ✅ Light mode: Widget uses light theme colors
- ✅ Dark mode: Widget uses dark theme colors
- ✅ Theme toggle: Widget updates instantly without reload
- ✅ No hardcoded colors: All colors use CSS variables
- ✅ Contrast ratios: All text meets 4.5:1 in both modes (Lighthouse score ≥90)

**Phase 7 Parallel Opportunities**:
- This entire phase can run in parallel with other phases if CSS variables are used from the start (recommended)

---

## Phase 8: Polish & Cross-Cutting Concerns

**Goal**: Optimize performance, add final touches, and prepare for deployment.

### Performance Optimization Tasks

- [ ] T085 [P] Implement lazy loading for widget using React.lazy() in `robotic-book/src/theme/Root.js`
- [ ] T086 [P] Add Suspense wrapper with fallback={null} in `robotic-book/src/theme/Root.js`
- [ ] T087 [P] Implement 50-message limit: remove oldest message when messages.length > 50 in `robotic-book/src/components/CourseChatWidget/index.tsx`
- [ ] T088 [P] Verify bundle size <50KB using `npm run build` and webpack-bundle-analyzer
- [ ] T089 [P] Run Lighthouse performance audit (target: Performance score ≥90, no layout shifts)

### Documentation Tasks

- [ ] T090 [P] Update README in `robotic-book/` with widget setup instructions (if applicable)
- [ ] T091 [P] Create `.env.example` for production with API URL placeholder in `robotic-book/`
- [ ] T092 [P] Document deployment steps in `specs/002-course-ai-chat-widget/quickstart.md` (production API URL, CORS setup)

### Testing Tasks (Optional - only if tests are requested)

**Note**: No explicit test requirement found in spec. If tests are needed, add:

- [ ] T093 [P] Write unit tests for CourseChatWidget component (Jest + RTL) in `robotic-book/src/components/CourseChatWidget/__tests__/index.test.tsx`
- [ ] T094 [P] Write backend API tests for /chat endpoint (pytest) in `book-backend/tests/test_chat_api.py`
- [ ] T095 [P] Write MCP client tests with mocked context7 (pytest) in `book-backend/tests/test_mcp_client.py`
- [ ] T096 [P] Run all tests and verify >80% coverage

### Final Validation

- [ ] T097 Manual E2E test: Open Docusaurus → open widget → send query → receive AI response → verify sources → close widget → repeat on mobile
- [ ] T098 Verify all constitution checks pass: minimal deps ✅, mobile ✅, zero layout breaks ✅, dark mode ✅, performance ✅, MCP ✅, RAG ✅, privacy ✅
- [ ] T099 Create git commit with all changes: `git add . && git commit -m "feat: Implement Course AI Chat Widget"`
- [ ] T100 Push branch and create pull request for review

**Phase 8 Validation**:
- ✅ Widget lazy-loads (no impact on initial page load)
- ✅ Message limit enforced (oldest removed when >50)
- ✅ Bundle size <50KB
- ✅ Lighthouse Performance ≥90, Accessibility ≥90
- ✅ No layout shifts (CLS = 0)
- ✅ All tests pass (if written)
- ✅ Documentation updated
- ✅ Constitution checks all pass

---

## Dependency Graph (User Story Completion Order)

```
Phase 1 (Setup)
    ↓
Phase 2 (Foundational)
    ↓
Phase 3 (US1: Basic Widget UI) ← MVP DEPLOYMENT POINT
    ↓
    ├─→ Phase 7 (US5: Dark Mode) [Can be done in parallel with Phase 3 if CSS vars used from start]
    ↓
Phase 4 (US2: AI Responses) ← Requires backend + MCP integration
    ↓
Phase 5 (US3: Error Handling) ← Requires API integration from Phase 4
    ↓
Phase 6 (US4: Mobile + Accessibility) [Can start in parallel with Phase 5]
    ↓
Phase 8 (Polish)
```

**Critical Path**: Setup → Foundational → US1 → US2 → US3 → Polish
**Parallel Paths**: US5 (Dark Mode) can run alongside US1 if CSS variables used early. US4 (Mobile/A11y) can run alongside US5.

---

## Parallel Execution Opportunities

### Within Phase 3 (US1):
- **Stream 1** (Component Logic): T013-T022 (developer A)
- **Stream 2** (Styling): T023-T030 (developer B)
- **Merge**: Both complete before T031 (integration)

### Within Phase 4 (US2):
- **Stream 1** (Backend Mock API): T033-T037 (backend developer)
- **Stream 2** (MCP Integration): T038-T042 (backend developer or separate)
- **Stream 3** (Frontend API Integration): T044-T049 (frontend developer, uses mock initially)
- **Merge**: T043 (replace mock with real MCP)

### Within Phase 5 (US3):
- **Stream 1** (Frontend Errors): T050-T058 (frontend developer)
- **Stream 2** (Backend Errors): T059-T062 (backend developer)
- **Stream 3** (Error Styling): T063-T065 (frontend developer or designer)
- **Merge**: All complete, no blocking dependencies

### Within Phase 6 (US4):
- **Stream 1** (Mobile CSS): T066-T070 (frontend developer)
- **Stream 2** (Accessibility): T071-T079 (frontend developer)
- **Merge**: Both complete for full US4 validation

### Cross-Phase Parallelism:
- **Phase 7 (US5: Dark Mode)** can run in parallel with **Phase 3 (US1)** if CSS variables are used from the start
- **Phase 6 (US4: Mobile)** can run in parallel with **Phase 5 (US3: Errors)** as they touch different concerns

---

## Summary

| Metric | Value |
|--------|-------|
| **Total Tasks** | 100 |
| **User Stories** | 5 (P1: Basic UI, P2: AI Responses, P3: Errors, P4: Mobile/A11y, P5: Dark Mode) |
| **MVP Scope** | Phase 1-3 (32 tasks) → Basic widget with mock responses |
| **Full Feature** | Phase 1-8 (100 tasks) → Production-ready widget |
| **Estimated Timeline (MVP)** | 2-3 days (1 developer) |
| **Estimated Timeline (Full)** | 5-7 days (1 developer), 3-4 days (2 developers with parallel execution) |
| **Parallel Opportunities** | 40+ tasks marked [P] can run in parallel |
| **Test Tasks** | Optional (T093-T096) - only if tests requested |

---

## Task Execution Checklist Format Validation

✅ All tasks follow the required format:
- `- [ ] TaskID [P?] [Story?] Description with file path`
- Task IDs: T001-T100 (sequential)
- [P] markers: 40+ parallelizable tasks identified
- [Story] labels: US1-US5 applied to all user story phase tasks
- File paths: Included in all implementation tasks
- Descriptions: Clear, actionable, specific

---

## Next Steps

1. **Review tasks** with team/stakeholders for completeness
2. **Decide on scope**:
   - **MVP**: Implement Phase 1-3 only (validate UI before backend complexity)
   - **Full**: Implement all phases (production-ready feature)
3. **Assign tasks** to developers (use [P] markers for parallel work)
4. **Begin implementation** starting with Phase 1 (Setup)
5. **Track progress** using checkboxes (- [ ] → - [x])
6. **Test after each phase** using validation criteria
7. **Deploy MVP** after Phase 3 for early feedback
8. **Complete remaining phases** based on feedback
9. **Create PR** after Phase 8 (all tasks complete)

---

**Tasks Document Complete**: Ready for implementation.
