# Quickstart Guide: Course AI Chat Widget

**Feature**: Course AI Chat Widget (002-course-ai-chat-widget)
**Date**: 2025-12-09
**Target Audience**: Developers implementing the widget

## Overview

This guide walks you through setting up the development environment and implementing the Course AI Chat Widget feature from scratch. By the end, you'll have a working chat widget integrated into the Docusaurus site with a backend API connected to Claude via MCP.

**Estimated Setup Time**: 30-45 minutes

---

## Prerequisites

### Required Software

| Tool | Version | Purpose |
|------|---------|---------|
| Node.js | ≥ 20.0 | Frontend development |
| npm | ≥ 10.0 | Package management |
| Python | ≥ 3.11 | Backend API |
| Git | Latest | Version control |

### Required Knowledge

- React functional components and hooks
- TypeScript basics
- FastAPI fundamentals
- REST API concepts
- CSS Modules

### Environment Setup

Ensure you have:

- A code editor (VS Code recommended)
- Terminal access
- MCP server credentials (for backend)
- Claude API key (for backend)

---

## Step 1: Clone and Setup Repository

```bash
# Clone the repository
cd "D:\Quarter 4\ai-book\humanoid-robotic-book"

# Verify current branch
git branch
# Should show: * 002-course-ai-chat-widget

# Install frontend dependencies
cd robotic-book
npm install

# Verify Docusaurus runs
npm start
# Should open http://localhost:3000
```

**Checkpoint**: Docusaurus site should load without errors.

---

## Step 2: Review Project Structure

```
humanoid-robotic-book/
├── robotic-book/                   # Docusaurus frontend
│   ├── src/
│   │   ├── components/
│   │   │   └── CourseChatWidget/   # ← Widget will go here (to be created)
│   │   ├── theme/
│   │   │   └── Root.js             # ← Global wrapper (to be created)
│   │   └── css/
│   │       └── custom.css          # Existing Docusaurus theme variables
│   ├── docusaurus.config.ts        # Docusaurus configuration
│   └── package.json
│
├── book-backend/                   # FastAPI backend
│   ├── app/
│   │   ├── main.py                 # FastAPI app entry point
│   │   ├── routes/
│   │   │   └── chat.py             # ← Chat endpoint (to be created)
│   │   ├── services/
│   │   │   └── mcp_client.py       # ← MCP integration (to be created)
│   │   └── models/
│   │       └── schemas.py          # ← Pydantic models (to be created)
│   └── requirements.txt
│
└── specs/002-course-ai-chat-widget/
    ├── plan.md                     # This implementation plan
    ├── research.md                 # Technology decisions
    ├── data-model.md               # Data entities
    ├── contracts/
    │   └── chat-api.yaml           # OpenAPI specification
    └── quickstart.md               # This guide
```

---

## Step 3: Create Frontend Widget Component

### 3.1 Create Widget Directory

```bash
cd robotic-book/src/components
mkdir CourseChatWidget
cd CourseChatWidget
```

### 3.2 Create Type Definitions

Create `types.ts`:

```typescript
// robotic-book/src/components/CourseChatWidget/types.ts

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

export interface ChatResponse {
  response_text: string;
  sources?: { title: string; url: string }[];
  metadata?: {
    processing_time_ms?: number;
    model_used?: string;
  };
}

export interface WidgetState {
  isOpen: boolean;
  messages: Message[];
  inputValue: string;
  isLoading: boolean;
  errorMessage: string | null;
}
```

### 3.3 Create Widget Component

Create `index.tsx`:

```typescript
// robotic-book/src/components/CourseChatWidget/index.tsx

import React, { useState, useRef, useEffect } from 'react';
import styles from './styles.module.css';
import type { Message, WidgetState, ChatRequest, ChatResponse } from './types';

const API_BASE_URL = process.env.NODE_ENV === 'production'
  ? 'https://api.example.com/api/v1'  // Replace with actual production URL
  : 'http://localhost:8000/api/v1';

function generateId(): string {
  return `${Date.now()}-${Math.random().toString(36).substr(2, 9)}`;
}

function extractPageContext() {
  return {
    title: document.title,
    pathname: window.location.pathname,
  };
}

export default function CourseChatWidget() {
  const [state, setState] = useState<WidgetState>({
    isOpen: false,
    messages: [],
    inputValue: '',
    isLoading: false,
    errorMessage: null,
  });

  const messagesEndRef = useRef<HTMLDivElement>(null);
  const inputRef = useRef<HTMLInputElement>(null);

  // Auto-scroll to latest message
  useEffect(() => {
    if (state.isOpen) {
      messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
    }
  }, [state.messages, state.isOpen]);

  // Focus input when widget opens
  useEffect(() => {
    if (state.isOpen) {
      inputRef.current?.focus();
    }
  }, [state.isOpen]);

  const toggleWidget = () => {
    setState(prev => ({ ...prev, isOpen: !prev.isOpen }));
  };

  const sendMessage = async () => {
    if (!state.inputValue.trim() || state.isLoading) return;

    const userMessage: Message = {
      id: generateId(),
      text: state.inputValue.trim(),
      sender: 'user',
      timestamp: Date.now(),
      status: 'pending',
    };

    setState(prev => ({
      ...prev,
      messages: [...prev.messages, userMessage],
      inputValue: '',
      isLoading: true,
      errorMessage: null,
    }));

    try {
      const payload: ChatRequest = {
        user_query: userMessage.text,
        page_context: extractPageContext(),
      };

      const response = await fetch(`${API_BASE_URL}/chat`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload),
      });

      if (!response.ok) {
        throw new Error(`HTTP ${response.status}`);
      }

      const data: ChatResponse = await response.json();

      const botMessage: Message = {
        id: generateId(),
        text: data.response_text,
        sender: 'bot',
        timestamp: Date.now(),
      };

      setState(prev => ({
        ...prev,
        messages: prev.messages.map(msg =>
          msg.id === userMessage.id ? { ...msg, status: 'sent' } : msg
        ).concat(botMessage),
        isLoading: false,
      }));
    } catch (error) {
      console.error('Chat error:', error);
      setState(prev => ({
        ...prev,
        messages: prev.messages.map(msg =>
          msg.id === userMessage.id ? { ...msg, status: 'error' } : msg
        ),
        isLoading: false,
        errorMessage: 'Failed to send message. Please try again.',
      }));
    }
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  };

  return (
    <div className={styles.container}>
      {!state.isOpen && (
        <button
          className={styles.toggleButton}
          onClick={toggleWidget}
          aria-label="Open course chat assistant"
        >
          💬
        </button>
      )}

      {state.isOpen && (
        <div className={styles.panel} role="dialog" aria-label="Course chat assistant">
          <div className={styles.header}>
            <h3>Course Assistant</h3>
            <button
              className={styles.closeButton}
              onClick={toggleWidget}
              aria-label="Close chat"
            >
              ✕
            </button>
          </div>

          <div className={styles.messagesContainer}>
            {state.messages.map(msg => (
              <div
                key={msg.id}
                className={`${styles.message} ${styles[msg.sender]}`}
              >
                {msg.text}
              </div>
            ))}
            {state.isLoading && <div className={styles.loadingIndicator}>...</div>}
            <div ref={messagesEndRef} />
          </div>

          {state.errorMessage && (
            <div className={styles.errorBanner}>{state.errorMessage}</div>
          )}

          <div className={styles.inputContainer}>
            <input
              ref={inputRef}
              type="text"
              value={state.inputValue}
              onChange={e => setState(prev => ({ ...prev, inputValue: e.target.value }))}
              onKeyPress={handleKeyPress}
              placeholder="Ask about this page..."
              className={styles.input}
              disabled={state.isLoading}
            />
            <button
              onClick={sendMessage}
              disabled={!state.inputValue.trim() || state.isLoading}
              className={styles.sendButton}
            >
              Send
            </button>
          </div>
        </div>
      )}
    </div>
  );
}
```

### 3.4 Create Styles

Create `styles.module.css`:

```css
/* robotic-book/src/components/CourseChatWidget/styles.module.css */

.container {
  position: fixed;
  bottom: 20px;
  right: 20px;
  z-index: var(--ifm-z-index-fixed);
  font-family: var(--ifm-font-family-base);
}

.toggleButton {
  width: 60px;
  height: 60px;
  border-radius: 50%;
  border: none;
  background: var(--ifm-color-primary);
  color: white;
  font-size: 24px;
  cursor: pointer;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
  transition: transform 0.2s, box-shadow 0.2s;
}

.toggleButton:hover {
  transform: scale(1.05);
  box-shadow: 0 6px 16px rgba(0, 0, 0, 0.2);
}

.panel {
  width: 400px;
  height: 500px;
  background: var(--ifm-background-surface-color);
  border: 1px solid var(--ifm-color-emphasis-300);
  border-radius: 12px;
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.2);
  display: flex;
  flex-direction: column;
  animation: slideUp 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

@keyframes slideUp {
  from {
    transform: translateY(100%);
    opacity: 0;
  }
  to {
    transform: translateY(0);
    opacity: 1;
  }
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 16px;
  border-bottom: 1px solid var(--ifm-color-emphasis-300);
  background: var(--ifm-color-primary);
  color: white;
  border-radius: 12px 12px 0 0;
}

.header h3 {
  margin: 0;
  font-size: 18px;
}

.closeButton {
  background: transparent;
  border: none;
  color: white;
  font-size: 24px;
  cursor: pointer;
  padding: 0;
  width: 32px;
  height: 32px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.messagesContainer {
  flex: 1;
  overflow-y: auto;
  padding: 16px;
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.message {
  max-width: 80%;
  padding: 10px 14px;
  border-radius: 12px;
  word-wrap: break-word;
}

.message.user {
  align-self: flex-end;
  background: var(--ifm-color-primary);
  color: white;
}

.message.bot {
  align-self: flex-start;
  background: var(--ifm-color-emphasis-200);
  color: var(--ifm-font-color-base);
}

.loadingIndicator {
  align-self: flex-start;
  padding: 10px 14px;
  color: var(--ifm-color-emphasis-600);
  font-style: italic;
}

.errorBanner {
  background: var(--ifm-color-danger);
  color: white;
  padding: 12px;
  text-align: center;
  font-size: 14px;
}

.inputContainer {
  display: flex;
  gap: 8px;
  padding: 16px;
  border-top: 1px solid var(--ifm-color-emphasis-300);
}

.input {
  flex: 1;
  padding: 10px 12px;
  border: 1px solid var(--ifm-color-emphasis-400);
  border-radius: 8px;
  background: var(--ifm-background-color);
  color: var(--ifm-font-color-base);
  font-size: 14px;
}

.input:focus {
  outline: none;
  border-color: var(--ifm-color-primary);
}

.sendButton {
  padding: 10px 20px;
  background: var(--ifm-color-primary);
  color: white;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-weight: 600;
}

.sendButton:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

/* Mobile responsive */
@media (max-width: 768px) {
  .container {
    left: 20px;
    right: 20px;
    bottom: 20px;
  }

  .panel {
    width: 100%;
    max-width: calc(100vw - 40px);
  }
}
```

---

## Step 4: Integrate Widget into Docusaurus

### 4.1 Create Root Wrapper

Create `robotic-book/src/theme/Root.js`:

```javascript
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

### 4.2 Verify Integration

```bash
# Restart Docusaurus dev server
npm start
```

**Checkpoint**: You should see a floating chat icon (💬) in the bottom-right corner.

---

## Step 5: Setup Backend API

### 5.1 Navigate to Backend Directory

```bash
cd ../../book-backend
```

### 5.2 Create Virtual Environment

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 5.3 Install Dependencies

Create `requirements.txt`:

```txt
fastapi==0.104.1
uvicorn[standard]==0.24.0
pydantic==2.5.0
python-dotenv==1.0.0
httpx==0.25.2
```

Install:

```bash
pip install -r requirements.txt
```

### 5.4 Create Pydantic Models

Create `app/models/schemas.py`:

```python
from pydantic import BaseModel, Field, validator
from typing import Optional

class PageContext(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    pathname: str = Field(..., min_length=1, max_length=200)
    section: Optional[str] = Field(None, max_length=100)

    @validator('pathname')
    def pathname_must_start_with_slash(cls, v):
        if not v.startswith('/'):
            raise ValueError('pathname must start with /')
        return v

class ChatRequest(BaseModel):
    user_query: str = Field(..., min_length=1, max_length=500)
    page_context: PageContext
    session_id: Optional[str] = None

class Source(BaseModel):
    title: str
    url: str

class ResponseMetadata(BaseModel):
    processing_time_ms: Optional[int] = None
    model_used: Optional[str] = None

class ChatResponse(BaseModel):
    response_text: str
    sources: list[Source] = []
    metadata: Optional[ResponseMetadata] = None
```

### 5.5 Create Chat Route

Create `app/routes/chat.py`:

```python
from fastapi import APIRouter, HTTPException
from app.models.schemas import ChatRequest, ChatResponse, Source
import time

router = APIRouter()

@router.post("/chat", response_model=ChatResponse)
async def handle_chat(request: ChatRequest):
    start_time = time.time()

    # TODO: Replace with actual MCP integration
    # For now, return a mock response
    response_text = f"This is a simulated response to: '{request.user_query}' from page: {request.page_context.pathname}"

    processing_time = int((time.time() - start_time) * 1000)

    return ChatResponse(
        response_text=response_text,
        sources=[
            Source(title="Example Source", url=request.page_context.pathname)
        ],
        metadata={
            "processing_time_ms": processing_time,
            "model_used": "mock"
        }
    )
```

### 5.6 Create Main App

Create/update `app/main.py`:

```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import chat

app = FastAPI(title="Course AI Chat Widget API", version="1.0.0")

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",  # Docusaurus dev
        "https://devabdullah90.github.io",  # Production
    ],
    allow_methods=["POST", "OPTIONS"],
    allow_headers=["Content-Type"],
)

app.include_router(chat.router, prefix="/api/v1")

@app.get("/health")
async def health_check():
    return {"status": "healthy"}
```

### 5.7 Run Backend

```bash
uvicorn app.main:app --reload --port 8000
```

**Checkpoint**: API should be running at `http://localhost:8000`. Visit `/docs` for Swagger UI.

---

## Step 6: Test End-to-End Flow

1. **Start Docusaurus** (if not running):

   ```bash
   cd robotic-book
   npm start
   ```

2. **Start FastAPI** (if not running):

   ```bash
   cd book-backend
   uvicorn app.main:app --reload --port 8000
   ```

3. **Test the widget**:
   - Open `http://localhost:3000`
   - Click the chat icon (💬)
   - Type a message and press "Send"
   - Verify you receive a mock response

**Expected Behavior**:

- Message appears as "user" bubble on right
- Loading indicator appears briefly
- Bot response appears as "bot" bubble on left

---

## Step 7: Next Steps (Post-Quickstart)

### Immediate Tasks

1. **Implement MCP Integration**:
   - Create `app/services/mcp_client.py`
   - Configure context7 MCP server connection
   - Replace mock response with real Claude calls

2. **Add Error Handling**:
   - Network errors → retry button
   - Rate limiting → cooldown message
   - API errors → friendly user message

3. **Improve UX**:
   - Add typing indicator animation
   - Implement keyboard shortcuts (Esc to close)
   - Add click-outside-to-close functionality

### Testing

- Write unit tests for widget component (Jest + RTL)
- Write API endpoint tests (pytest)
- Perform manual accessibility testing (keyboard nav, screen readers)

### Deployment

- Configure production API URL in frontend
- Set up environment variables for MCP credentials
- Deploy backend to cloud service (Render/Railway/AWS)
- Update CORS settings for production domain

---

## Troubleshooting

### Widget not appearing

- Check browser console for errors
- Verify `Root.js` is created in correct location: `robotic-book/src/theme/Root.js`
- Clear Docusaurus cache: `npm run clear && npm start`

### API connection failed

- Verify backend is running on `http://localhost:8000`
- Check CORS configuration in `app/main.py`
- Inspect browser Network tab for failed requests

### Styles not applying

- Ensure CSS Modules are working (Docusaurus default)
- Check for typos in `className` references
- Verify CSS variables exist in Docusaurus theme

---

## Resources

- [Docusaurus Documentation](https://docusaurus.io/docs)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [React Hooks Reference](https://react.dev/reference/react)
- [OpenAPI Specification](./contracts/chat-api.yaml)
- [Data Model](./data-model.md)
- [Research Decisions](./research.md)

---

**Quickstart Complete**: You now have a working Course AI Chat Widget. Proceed to implement MCP integration and deploy to production.
