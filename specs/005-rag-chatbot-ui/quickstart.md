# Quickstart: RAG Chatbot UI + Backend Integration

## Overview
The RAG Chatbot is already fully implemented and integrated. This guide explains how to run and use the existing system.

## Prerequisites
- Python 3.11+
- Node.js 20+
- Qdrant vector database running locally (port 6333)
- Cohere API key
- OpenAI API key

## Setup

### 1. Backend Setup
```bash
cd backend
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

Create `.env` file with your API keys:
```env
COHERE_API_KEY=your_cohere_api_key
OPENAI_API_KEY=your_openai_api_key
QDRANT_URL=http://localhost:6333
QDRANT_API_KEY=your_qdrant_api_key_if_using_cloud
```

### 2. Start the Backend
```bash
cd backend
uvicorn src.main:app --reload --port 8000
```

### 3. Index Book Content (if not already done)
```bash
# Run the embedding pipeline to index book content
python main.py --urls-file urls.txt
```

## Frontend Setup

### 1. Navigate to Docusaurus Project
```bash
cd robotic-book
```

### 2. Install Dependencies
```bash
npm install
```

### 3. Start Development Server
```bash
npm start
```

## Usage

### 1. Chat Interface
- Visit your Docusaurus site (typically http://localhost:3000)
- Look for the chat widget button in the bottom-right corner
- Click to open the chat panel
- Type your question about the book content
- The system will retrieve relevant information and generate a grounded response

### 2. Text Selection Feature
- Select text on any book page
- A contextual prompt will appear
- Click "Ask about this" to query specifically about the selected text

## Architecture

### Frontend (Docusaurus)
- `RAGChatWidget` component in `robotic-book/src/components/RAGChatWidget/index.tsx`
- Integrated via `Root.tsx` to appear on all pages
- Makes POST requests to `http://localhost:8000/query`

### Backend (FastAPI)
- `/query` endpoint processes user queries
- Retrieves relevant content from Qdrant vector database
- Uses OpenAI GPT-4 Turbo with retrieved context for grounded responses
- Enforces no hallucination beyond book content

## API Endpoints

### POST /query
Request:
```json
{
  "query": "Your question here",
  "context": "Optional selected text",
  "parameters": {
    "top_k": 5,
    "temperature": 0.3
  }
}
```

Response:
```json
{
  "answer": "AI-generated response",
  "sources": [
    {
      "id": "document_id",
      "content_snippet": "Relevant content snippet...",
      "confidence": 0.85
    }
  ],
  "query_id": "unique_query_id",
  "timestamp": "2025-12-16T10:30:00Z",
  "status": "success"
}
```

## Troubleshooting

### Common Issues
1. **Backend not responding**: Ensure FastAPI server is running on port 8000
2. **No results**: Verify Qdrant has indexed book content
3. **API errors**: Check that API keys are properly configured in `.env`

### Health Check
- Backend health: `GET http://localhost:8000/health`
- Frontend: Chat widget should appear on all pages