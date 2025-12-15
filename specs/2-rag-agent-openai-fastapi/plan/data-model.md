# Data Model: RAG Agent Backend

**Feature**: AI Agent with Context Retrieval and API Interface
**Created**: 2025-12-15

## Entity Definitions

### Query Request
**Description**: Represents a user query sent to the AI agent

**Fields**:
- `query` (string, required): The user's query text
- `parameters` (object, optional): Additional parameters for the query
  - `temperature` (number, optional): Controls randomness (0.0-1.0)
  - `max_tokens` (integer, optional): Maximum tokens in response
  - `top_k` (integer, optional): Number of context documents to retrieve

**Validation Rules**:
- Query must be non-empty string
- Temperature between 0.0 and 1.0 if provided
- Max tokens positive integer if provided
- Top_k between 1 and 10 if provided

### Retrieved Context
**Description**: Represents the relevant document fragments retrieved from the vector database

**Fields**:
- `documents` (array of objects, required): Retrieved document fragments
  - `id` (string, required): Unique identifier for the document
  - `content` (string, required): The text content of the fragment
  - `metadata` (object, optional): Additional document metadata
    - `source` (string, optional): Source of the document
    - `title` (string, optional): Title of the document
    - `url` (string, optional): URL of the document
  - `score` (number, required): Relevance score (0.0-1.0)
- `query_embedding` (array of numbers, optional): Vector representation of the query
- `retrieval_method` (string, optional): Method used for retrieval

**Validation Rules**:
- Documents array must not be empty when context found
- Content must be non-empty string
- Score between 0.0 and 1.0

### Response
**Description**: Contains the AI-generated answer along with metadata including source attribution and confidence indicators

**Fields**:
- `answer` (string, required): The AI-generated response
- `sources` (array of objects, required): Source attribution for the response
  - `id` (string, required): Document ID from which information was derived
  - `content_snippet` (string, required): Relevant snippet from the source
  - `confidence` (number, required): Confidence level (0.0-1.0)
- `query_id` (string, optional): Unique identifier for the query
- `timestamp` (string, required): ISO 8601 timestamp of response generation
- `status` (string, required): Response status ("success", "no_context", "error")

**Validation Rules**:
- Answer must be non-empty string when status is "success"
- Sources array must match the information used in the answer
- Confidence between 0.0 and 1.0

### Health Status
**Description**: Contains system health information including service availability and performance metrics

**Fields**:
- `status` (string, required): Overall service status ("healthy", "degraded", "unhealthy")
- `timestamp` (string, required): ISO 8601 timestamp of status check
- `services` (object, optional): Status of individual services
  - `qdrant` (string, optional): Qdrant connection status
  - `openai` (string, optional): OpenAI API connection status
- `metrics` (object, optional): Performance metrics
  - `response_time_ms` (number, optional): Average response time in milliseconds
  - `uptime_seconds` (number, optional): Service uptime in seconds

**Validation Rules**:
- Status must be one of the allowed values
- Timestamp must be valid ISO 8601 format