# Data Model: RAG Chatbot UI + Backend Integration

## Key Entities from Feature Spec

### ChatMessage
- **Description**: Represents a single message in the conversation
- **Fields**:
  - `id` (string): Unique identifier for the message
  - `role` (string): Sender role ('user' or 'bot')
  - `content` (string): Message text content
  - `timestamp` (datetime): When the message was created
  - `sources` (array of strings, optional): Source citations for bot responses

### QueryRequest
- **Description**: Represents a user query sent to the backend RAG agent
- **Fields**:
  - `query` (string): The user's question or query text
  - `context` (string, optional): Optional context text (e.g., selected text from page)
  - `parameters` (object, optional): Additional query parameters (top_k, temperature, etc.)

### QueryResponse
- **Description**: Represents the backend response to a user query
- **Fields**:
  - `answer` (string): The AI-generated response to the query
  - `sources` (array of objects): Source citations with content snippets and confidence scores
  - `query_id` (string): Unique identifier for the query
  - `timestamp` (string): When the response was generated
  - `status` (string): Status of the query processing ('success', 'no_context', 'error')

## Backend-Specific Models

### RetrievedContext
- **Description**: Container for context retrieved from Qdrant
- **Fields**:
  - `documents` (array of objects): Retrieved documents with content and metadata
  - `query_embedding` (array of numbers): Embedding vector of the original query
  - `retrieval_method` (string): Method used for retrieval ('semantic_search')

### Document
- **Description**: Individual document retrieved from Qdrant
- **Fields**:
  - `id` (string): Unique identifier of the document in Qdrant
  - `content` (string): Text content of the retrieved document
  - `metadata` (object): Additional metadata (source URL, page title, etc.)
  - `score` (number): Relevance score from the semantic search

### Source
- **Description**: Source citation for attribution in responses
- **Fields**:
  - `id` (string): Document ID from Qdrant
  - `content_snippet` (string): Brief excerpt from the source document
  - `confidence` (number): Confidence/relevance score of the source

## Frontend State Models

### RAGChatWidget State
- **Fields**:
  - `isOpen` (boolean): Whether the chat panel is open
  - `messages` (array of ChatMessage): Current conversation history
  - `inputValue` (string): Current value in the input field
  - `isLoading` (boolean): Whether waiting for a response
  - `selectedText` (string or null): Currently selected text on the page