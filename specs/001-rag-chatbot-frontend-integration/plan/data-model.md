# Data Models: RAG Chatbot Backend-Frontend Integration

## 1. Frontend Data Models

### ChatQuery
Represents a user's query sent from the frontend to the backend.

```typescript
interface ChatQuery {
  query: string;              // The main question or query text
  context?: string;           // Optional context from selected text
  session_id?: string;        // Optional session identifier for conversation context
  metadata?: QueryMetadata;   // Additional metadata about the query
}
```

**Fields:**
- `query`: Required string containing the user's question (max 2000 chars per constitution compliance)
- `context`: Optional string containing selected text or additional context (max 5000 chars per constitution compliance)
- `session_id`: Optional string to maintain conversation state
- `metadata`: Optional object with additional query information

### QueryMetadata
Additional information about the query context.

```typescript
interface QueryMetadata {
  page_url?: string;          // URL of the page where query originated
  selected_text_position?: {  // Position of selected text in document
    start: number;
    end: number;
  };
  timestamp: string;          // ISO timestamp of query submission
  user_agent?: string;        // Information about the user's browser/device
}
```

### ChatResponse
Represents the response received from the backend RAG agent.

```typescript
interface ChatResponse {
  response: string;           // The AI-generated response text
  sources: SourceReference[]; // List of sources used to generate the response
  session_id: string;         // Session identifier for conversation context
  confidence?: number;        // Optional confidence score (0-1)
  metadata?: ResponseMetadata;// Additional response metadata
}
```

**Fields:**
- `response`: The AI-generated answer to the user's query (grounded in book content per constitution)
- `sources`: Array of source references used in the response (for attribution per constitution)
- `session_id`: Session identifier for maintaining conversation state
- `confidence`: Optional confidence score for the response
- `metadata`: Optional object with additional response information

### SourceReference
Represents a source document or section used in the response.

```typescript
interface SourceReference {
  id: string;                 // Unique identifier for the source
  title: string;              // Title or heading of the source
  content: string;            // Snippet of content from the source
  url?: string;               // URL to the source document
  page?: number;              // Page number if applicable
  score?: number;             // Relevance score (0-1)
  metadata?: Record<string, any>; // Additional metadata about the source
}
```

### ResponseMetadata
Additional information about the response.

```typescript
interface ResponseMetadata {
  processing_time: number;    // Time taken to process the query (in milliseconds)
  tokens_used: number;        // Number of tokens used in the response
  model: string;              // Name of the model used to generate the response
  timestamp: string;          // ISO timestamp of response generation
}
```

### ChatSession
Represents the state of a conversation session.

```typescript
interface ChatSession {
  id: string;                 // Unique session identifier
  created_at: string;         // ISO timestamp of session creation
  last_activity: string;      // ISO timestamp of last activity
  messages: ChatMessage[];    // Array of messages in the conversation
  metadata?: SessionMetadata; // Additional session metadata
}
```

### ChatMessage
Represents a single message in a conversation.

```typescript
interface ChatMessage {
  id: string;                 // Unique message identifier
  role: 'user' | 'assistant'; // Role of the message sender
  content: string;            // The message content
  timestamp: string;          // ISO timestamp of message creation
  sources?: SourceReference[];// Sources referenced in the message (for assistant responses)
}
```

### SessionMetadata
Additional metadata about the session.

```typescript
interface SessionMetadata {
  page_context?: string;      // Context of the page where session started
  user_preferences?: UserPreferences; // User preferences for this session
}
```

### UserPreferences
User preferences for the chat experience.

```typescript
interface UserPreferences {
  response_length?: 'short' | 'medium' | 'long'; // Preferred response length
  citation_style?: 'formal' | 'casual' | 'minimal'; // Preferred citation style
  enable_typing_indicator?: boolean; // Whether to show typing indicators
}
```

## 2. API Request/Response Models

### API Request Model
```json
{
  "query": "What is the main concept of this chapter?",
  "context": "The chapter discusses the fundamentals of machine learning...",
  "session_id": "session-12345",
  "metadata": {
    "page_url": "https://example.com/book/chapter-1",
    "timestamp": "2025-12-15T10:30:00Z"
  }
}
```

### API Response Model
```json
{
  "response": "The main concept of this chapter is...",
  "sources": [
    {
      "id": "doc-123",
      "title": "Chapter 1: Fundamentals",
      "content": "The chapter discusses the fundamentals of machine learning...",
      "url": "https://example.com/book/chapter-1#section-1",
      "score": 0.95
    }
  ],
  "session_id": "session-12345",
  "confidence": 0.89,
  "metadata": {
    "processing_time": 2450,
    "tokens_used": 120,
    "model": "gpt-4",
    "timestamp": "2025-12-15T10:30:02Z"
  }
}
```

### API Error Response Model
```json
{
  "error": "Error message describing what went wrong",
  "code": "ERROR_CODE",
  "details": {
    "message": "More detailed error information",
    "timestamp": "2025-12-15T10:30:02Z"
  }
}
```

## 3. Frontend State Models

### ChatState
Represents the current state of the chat interface.

```typescript
interface ChatState {
  messages: ChatMessage[];    // Current messages in the conversation
  isLoading: boolean;         // Whether a response is being generated
  error: string | null;       // Any error message to display
  session: ChatSession | null;// Current session information
  preferences: UserPreferences; // Current user preferences
}
```

### UI Configuration
Configuration options for the chat interface.

```typescript
interface UIConfiguration {
  position: 'bottom-right';   // Fixed position per constitution requirement (20px offset)
  title: string;              // Title displayed in the chat interface
  initial_open: boolean;      // Whether the chat should be open by default (false per constitution)
  theme: 'light' | 'dark';    // Theme using CSS variables for automatic light/dark mode
  max_height: number;         // Maximum height of the chat interface
  max_width: number;          // Maximum width: 400px desktop, full-width-20px mobile per constitution
}
```

## 4. Validation Rules

### Input Validation
- Query text must be 1-2000 characters (per constitution compliance)
- Context text (if provided) must be 1-5000 characters (per constitution compliance)
- Session ID must be a valid string identifier
- Metadata fields are optional but must be valid if provided
- All inputs must be sanitized to prevent XSS (per security requirements)

### Response Validation
- Response text must be present and non-empty
- Sources array may be empty but must be an array if present
- Session ID in response must match the request
- Confidence score (if present) must be between 0 and 1
- Response must be grounded in provided context per constitution (no hallucination)

### Error Handling
- All API responses must include appropriate HTTP status codes
- Error responses must follow the standard error format
- Client-side validation should occur before API requests when possible
- Error messages must be user-friendly and not expose internal details

### Constitution Compliance Validation
- All responses must be grounded in book content (per constitution section 14.2-14.3)
- No hallucination of information outside provided context (per constitution section 14.4)
- Privacy requirements met (no PII collection without consent per constitution section 9.119-9.120)
- Lightweight implementation that doesn't affect page load (per constitution section 4.37)