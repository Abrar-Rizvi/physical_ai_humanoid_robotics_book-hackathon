# Data Model: RAG Backend URL Update

**Feature**: RAG Backend URL Update
**Date**: 2025-12-17

## Entity: API Configuration

### Description
Configuration settings for API communication between frontend and backend.

### Fields
- `apiBaseUrl` (string, required): The base URL for backend API calls
- `apiEndpoints` (object, required): Object containing endpoint paths relative to base URL
- `timeout` (number, optional): Request timeout in milliseconds (default: 30000)
- `retries` (number, optional): Number of retry attempts for failed requests (default: 3)

### Validation Rules
- `apiBaseUrl` must be a valid URL with https protocol for production
- `apiEndpoints` must contain required endpoint definitions
- `timeout` must be between 5000 and 60000 milliseconds
- `retries` must be between 0 and 5

## Entity: API Request

### Description
Structure for API requests sent from frontend to backend.

### Fields
- `query` (string, required): The user's query text
- `context` (string, optional): Additional context for the query (default: "")
- `session_id` (string, required): Unique identifier for the session
- `timestamp` (Date, optional): When the request was made

### Validation Rules
- `query` must be 1-2000 characters
- `session_id` must be a valid string identifier
- `context` can be empty but must be a string if provided

## Entity: API Response

### Description
Structure for API responses from backend to frontend.

### Fields
- `answer` (string, required): The AI-generated answer
- `sources` (array, optional): Array of source documents used (default: [])
- `status` (string, optional): Status of the request (default: "success")
- `error` (string, optional): Error message if request failed
- `timestamp` (Date, optional): When the response was generated

### Validation Rules
- `answer` must be provided when status is "success"
- `sources` must be an array of source objects
- `status` must be one of "success", "error", or "processing"
- `error` must be provided when status is "error"

## Entity: Chat Message

### Description
Represents a message in the chat conversation between user and assistant.

### Fields
- `id` (string, required): Unique identifier for the message
- `text` (string, required): The content of the message
- `sender` (string, required): "user" or "assistant"
- `timestamp` (Date, required): When the message was created
- `sources` (array, optional): Source documents for assistant responses

### Validation Rules
- `id` must be a unique string
- `text` must be 1-5000 characters
- `sender` must be one of the allowed values
- `timestamp` must be a valid date

## Relationships
- API Configuration contains multiple API Requests
- API Request generates one API Response
- API Response creates Chat Message for assistant responses
- User input creates Chat Message for user messages