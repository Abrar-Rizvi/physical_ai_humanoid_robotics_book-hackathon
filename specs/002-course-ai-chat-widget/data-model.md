# Data Model: Course AI Chat Widget

**Feature**: Course AI Chat Widget (002-course-ai-chat-widget)
**Date**: 2025-12-09
**Phase**: 1 - Design & Contracts

## Overview

This document defines the core entities, their relationships, and validation rules for the Course AI Chat Widget feature. The data model supports a stateless, session-based chat interface with page-aware context.

---

## 1. Core Entities

### 1.1 Message

Represents a single message in the chat conversation.

**Attributes**:

| Field | Type | Required | Validation | Description |
|-------|------|----------|------------|-------------|
| `id` | `string` | Yes | UUID v4 | Unique message identifier |
| `text` | `string` | Yes | 1-2000 chars | Message content |
| `sender` | `enum` | Yes | `'user' \| 'bot'` | Message sender type |
| `timestamp` | `number` | Yes | Unix timestamp (ms) | When message was created |
| `status` | `enum` | No | `'pending' \| 'sent' \| 'error'` | Message delivery status (frontend only) |

**Relationships**:

- Belongs to one `ChatSession` (in-memory, not persisted)

**Validation Rules**:

- `text` must not be empty after trimming whitespace
- `timestamp` must be ≤ current time
- `sender` must be exactly `'user'` or `'bot'`

**State Transitions** (for `status`):

```
pending → sent (successful API response)
pending → error (API failure)
error → pending (user retries)
```

**Example**:

```typescript
{
  id: "550e8400-e29b-41d4-a716-446655440000",
  text: "What is ROS 2?",
  sender: "user",
  timestamp: 1702123456789,
  status: "sent"
}
```

---

### 1.2 ChatSession

Represents an ephemeral chat session (client-side only, not persisted on backend).

**Attributes**:

| Field | Type | Required | Validation | Description |
|-------|------|----------|------------|-------------|
| `sessionId` | `string` | Yes | UUID v4 | Unique session identifier |
| `messages` | `Message[]` | Yes | Max 50 items | Array of messages in conversation |
| `startedAt` | `number` | Yes | Unix timestamp (ms) | Session creation time |
| `lastActivityAt` | `number` | Yes | Unix timestamp (ms) | Last user/bot interaction |

**Relationships**:

- Has many `Message` entities

**Validation Rules**:

- `messages` array is capped at 50 items (oldest removed on overflow)
- `lastActivityAt` ≥ `startedAt`
- Session auto-expires after 24 hours of inactivity (client-side logic)

**Lifecycle**:

- Created when widget is first opened
- Cleared when user closes widget or refreshes page
- Not persisted to backend (stateless design)

**Example**:

```typescript
{
  sessionId: "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
  messages: [
    { id: "...", text: "Hello", sender: "user", timestamp: 1702123456789 },
    { id: "...", text: "Hi! How can I help?", sender: "bot", timestamp: 1702123457000 }
  ],
  startedAt: 1702123456789,
  lastActivityAt: 1702123457000
}
```

---

### 1.3 PageContext

Represents the current page context sent with each query.

**Attributes**:

| Field | Type | Required | Validation | Description |
|-------|------|----------|------------|-------------|
| `title` | `string` | Yes | 1-200 chars | Document title (from `document.title`) |
| `pathname` | `string` | Yes | Valid URL path | Current page path (e.g., `/docs/chapter-3`) |
| `section` | `string` | No | 0-100 chars | Optional section identifier |

**Validation Rules**:

- `pathname` must start with `/`
- `title` must not be empty

**Example**:

```typescript
{
  title: "Chapter 3: ROS 2 Fundamentals - Physical AI Book",
  pathname: "/docs/chapter-3",
  section: "ros2-architecture"
}
```

---

### 1.4 ChatRequest (API Payload)

Sent from frontend to backend for each user query.

**Attributes**:

| Field | Type | Required | Validation | Description |
|-------|------|----------|------------|-------------|
| `user_query` | `string` | Yes | 1-500 chars | User's question or message |
| `page_context` | `PageContext` | Yes | Valid `PageContext` object | Current page metadata |
| `session_id` | `string` | No | UUID v4 | Optional session tracking ID |

**Validation Rules**:

- `user_query` sanitized (HTML stripped, trimmed)
- `page_context.pathname` validated against known routes (optional strict mode)

**Example**:

```json
{
  "user_query": "Explain ROS 2 nodes",
  "page_context": {
    "title": "Chapter 3: ROS 2 Fundamentals",
    "pathname": "/docs/chapter-3"
  },
  "session_id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890"
}
```

---

### 1.5 ChatResponse (API Payload)

Returned from backend to frontend after processing query.

**Attributes**:

| Field | Type | Required | Validation | Description |
|-------|------|----------|------------|-------------|
| `response_text` | `string` | Yes | 1-4000 chars | Claude's response |
| `sources` | `Source[]` | No | Max 5 items | References to book sections |
| `metadata` | `ResponseMetadata` | No | Valid object | Performance/debugging info |

**Example**:

```json
{
  "response_text": "ROS 2 nodes are independent processes that perform computation...",
  "sources": [
    {
      "title": "Chapter 3, Section 2: Node Architecture",
      "url": "/docs/chapter-3#node-architecture"
    }
  ],
  "metadata": {
    "processing_time_ms": 1234,
    "model_used": "claude-sonnet-4",
    "tokens_used": 450
  }
}
```

---

### 1.6 Source (Nested in ChatResponse)

Represents a reference to book content used in the response.

**Attributes**:

| Field | Type | Required | Validation | Description |
|-------|------|----------|------------|-------------|
| `title` | `string` | Yes | 1-100 chars | Human-readable source title |
| `url` | `string` | Yes | Valid relative URL | Link to source section |

**Example**:

```typescript
{
  title: "Chapter 5: Gazebo Simulation",
  url: "/docs/chapter-5#simulation-basics"
}
```

---

### 1.7 ResponseMetadata (Nested in ChatResponse)

Optional debugging/performance data returned with response.

**Attributes**:

| Field | Type | Required | Validation | Description |
|-------|------|----------|------------|-------------|
| `processing_time_ms` | `number` | No | ≥ 0 | Backend processing duration |
| `model_used` | `string` | No | Non-empty string | Claude model identifier |
| `tokens_used` | `number` | No | ≥ 0 | Approximate token count |

---

### 1.8 ErrorState

Represents error conditions in the widget UI.

**Attributes**:

| Field | Type | Required | Validation | Description |
|-------|------|----------|------------|-------------|
| `hasError` | `boolean` | Yes | N/A | Whether an error is active |
| `errorType` | `enum` | Conditional | `'network' \| 'api' \| 'rate_limit' \| 'unknown'` | Error category (required if `hasError` is true) |
| `errorMessage` | `string` | Conditional | 1-200 chars | User-facing error message (required if `hasError` is true) |
| `retryable` | `boolean` | No | N/A | Whether user can retry (default: `true`) |

**Error Type Mapping**:

| `errorType` | `errorMessage` | `retryable` |
|-------------|----------------|-------------|
| `network` | "Connection lost. Check your internet and retry." | `true` |
| `api` | "Sorry, I couldn't process that. Please try again." | `true` |
| `rate_limit` | "Too many requests. Please wait 30 seconds." | `false` |
| `unknown` | "An unexpected error occurred." | `true` |

**Example**:

```typescript
{
  hasError: true,
  errorType: "network",
  errorMessage: "Connection lost. Check your internet and retry.",
  retryable: true
}
```

---

## 2. Entity Relationships

```
ChatSession (1) ──< (many) Message
   │
   └─ Contains up to 50 messages
   └─ Cleared on page refresh/widget close

ChatRequest (1) ──── (1) PageContext
   │
   └─ Sent with every user query

ChatResponse (1) ──< (0-5) Source
   │
   └─ Optionally includes source references
```

---

## 3. Data Flow

### 3.1 User Sends Message

1. User types message and clicks "Send"
2. Frontend creates `Message` object:
   - `id`: Generate UUID
   - `text`: User input
   - `sender`: `'user'`
   - `timestamp`: `Date.now()`
   - `status`: `'pending'`
3. Frontend adds message to `ChatSession.messages`
4. Frontend constructs `ChatRequest`:
   - `user_query`: Message text
   - `page_context`: Extracted from DOM
   - `session_id`: From `ChatSession.sessionId`
5. Frontend sends `POST /api/v1/chat` with `ChatRequest`

### 3.2 Backend Processes Query

1. Backend validates `ChatRequest`
2. Backend calls context7 MCP to retrieve relevant embeddings
3. Backend sends retrieved content + query to Claude (via MCP)
4. Backend constructs `ChatResponse`:
   - `response_text`: Claude's answer
   - `sources`: Extracted from embeddings metadata
   - `metadata`: Processing time, model info
5. Backend returns `ChatResponse` with HTTP 200

### 3.3 Frontend Displays Response

1. Frontend receives `ChatResponse`
2. Frontend updates user message status: `'pending'` → `'sent'`
3. Frontend creates bot `Message` object:
    - `id`: Generate UUID
    - `text`: `response_text` from API
    - `sender`: `'bot'`
    - `timestamp`: `Date.now()`
4. Frontend adds bot message to `ChatSession.messages`
5. Frontend scrolls to latest message

### 3.4 Error Handling

If step 10 fails (network error, API 4xx/5xx):

- Frontend updates user message status: `'pending'` → `'error'`
- Frontend sets `ErrorState`:
  - `hasError`: `true`
  - `errorType`: Determined from response/error code
  - `errorMessage`: User-friendly message
  - `retryable`: Based on error type
- Frontend displays error banner with retry button (if retryable)

---

## 4. Validation Rules Summary

### Frontend Validation

| Field | Rule |
|-------|------|
| `user_query` | Non-empty after trim, ≤ 500 chars |
| `page_context.title` | Non-empty, ≤ 200 chars |
| `page_context.pathname` | Starts with `/`, ≤ 200 chars |
| `messages` array | ≤ 50 items (auto-prune oldest) |

### Backend Validation (Pydantic Models)

```python
from pydantic import BaseModel, Field, validator

class PageContext(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    pathname: str = Field(..., min_length=1, max_length=200)
    section: str | None = Field(None, max_length=100)

    @validator('pathname')
    def pathname_must_start_with_slash(cls, v):
        if not v.startswith('/'):
            raise ValueError('pathname must start with /')
        return v

class ChatRequest(BaseModel):
    user_query: str = Field(..., min_length=1, max_length=500)
    page_context: PageContext
    session_id: str | None = Field(None, regex=r'^[a-f0-9\-]{36}$')

    @validator('user_query')
    def sanitize_query(cls, v):
        # Strip HTML tags, trim whitespace
        import re
        clean = re.sub(r'<[^>]+>', '', v).strip()
        if not clean:
            raise ValueError('user_query cannot be empty')
        return clean

class Source(BaseModel):
    title: str = Field(..., min_length=1, max_length=100)
    url: str = Field(..., min_length=1, max_length=200)

class ResponseMetadata(BaseModel):
    processing_time_ms: int | None = Field(None, ge=0)
    model_used: str | None = None
    tokens_used: int | None = Field(None, ge=0)

class ChatResponse(BaseModel):
    response_text: str = Field(..., min_length=1, max_length=4000)
    sources: list[Source] = Field(default_factory=list, max_items=5)
    metadata: ResponseMetadata | None = None
```

---

## 5. Storage & Persistence

### Frontend (Browser)

- **Storage**: In-memory React state (no localStorage/sessionStorage)
- **Lifetime**: Until page refresh or widget close
- **Reason**: Constitution requires stateless design; no PII storage

### Backend (FastAPI)

- **Storage**: None (stateless API)
- **Logging**: Request/response logs for debugging (sanitized, no PII)
- **Caching**: Optional Redis cache for repeated queries (future enhancement)

### Database

- **Not Used**: No database required for MVP
- **Future**: Optional analytics DB for usage metrics (aggregate only)

---

## 6. Performance Considerations

### Message Limit (50 messages)

**Rationale**: Prevent memory bloat in long sessions

**Implementation**:

```typescript
function addMessage(session: ChatSession, message: Message): ChatSession {
  const updatedMessages = [...session.messages, message];
  if (updatedMessages.length > 50) {
    updatedMessages.shift(); // Remove oldest message
  }
  return {
    ...session,
    messages: updatedMessages,
    lastActivityAt: Date.now(),
  };
}
```

### Response Size Limit (4000 chars)

**Rationale**: Prevent UI overflow, keep responses concise

**Backend Enforcement**:

- Truncate Claude response if > 4000 chars
- Append "..." to indicate truncation
- Log warning for monitoring

---

## 7. Security & Privacy

### Data Sanitization

- **User Input**: Strip HTML tags, limit length (500 chars)
- **Page Context**: Validate pathname format (no XSS vectors)

### No PII Storage

- **Session IDs**: Not logged or persisted
- **User Queries**: Logged in aggregate only (no individual tracking)
- **Compliance**: No cookies, no tracking, GDPR-friendly

### Rate Limiting (Backend)

- **IP-based**: 10 requests/minute per IP
- **Session-based**: 5 requests/minute per `session_id` (optional)

---

## 8. TypeScript Type Definitions

```typescript
// types.ts

export type MessageSender = 'user' | 'bot';
export type MessageStatus = 'pending' | 'sent' | 'error';
export type ErrorType = 'network' | 'api' | 'rate_limit' | 'unknown';

export interface Message {
  id: string;
  text: string;
  sender: MessageSender;
  timestamp: number;
  status?: MessageStatus;
}

export interface ChatSession {
  sessionId: string;
  messages: Message[];
  startedAt: number;
  lastActivityAt: number;
}

export interface PageContext {
  title: string;
  pathname: string;
  section?: string;
}

export interface ChatRequest {
  user_query: string;
  page_context: PageContext;
  session_id?: string;
}

export interface Source {
  title: string;
  url: string;
}

export interface ResponseMetadata {
  processing_time_ms?: number;
  model_used?: string;
  tokens_used?: number;
}

export interface ChatResponse {
  response_text: string;
  sources?: Source[];
  metadata?: ResponseMetadata;
}

export interface ErrorState {
  hasError: boolean;
  errorType?: ErrorType;
  errorMessage?: string;
  retryable?: boolean;
}

export interface WidgetState {
  isOpen: boolean;
  session: ChatSession | null;
  inputValue: string;
  isLoading: boolean;
  error: ErrorState;
}
```

---

## Next Steps

- Phase 1 continues with API contract specification (OpenAPI YAML)
- Phase 1 concludes with quickstart.md for developer setup
- Phase 2 will generate tasks.md based on this data model

**Data Model Complete**: All entities, relationships, and validation rules defined.
