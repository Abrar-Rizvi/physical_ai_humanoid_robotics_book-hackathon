# Quickstart Guide: RAG Agent Backend

## Prerequisites

- Python 3.9 or higher
- OpenAI API key
- Access to Qdrant instance (local or cloud)

## Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd <repository-directory>
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**
   Create a `.env` file with the following variables:
   ```env
   OPENAI_API_KEY=your_openai_api_key
   QDRANT_URL=your_qdrant_url
   QDRANT_API_KEY=your_qdrant_api_key  # if using cloud
   QDRANT_COLLECTION_NAME=your_collection_name
   EMBEDDING_MODEL=text-embedding-3-small  # or the model used for existing embeddings
   ```

## Running the Service

1. **Start the FastAPI server**
   ```bash
   uvicorn main:app --reload --host 0.0.0.0 --port 8000
   ```

2. **Verify the service is running**
   Open your browser to `http://localhost:8000/health` or run:
   ```bash
   curl http://localhost:8000/health
   ```

## Making a Query

1. **Send a query using curl**
   ```bash
   curl -X POST http://localhost:8000/query \
     -H "Content-Type: application/json" \
     -d '{
       "query": "What are the key principles of humanoid robotics?"
     }'
   ```

2. **Example response**
   ```json
   {
     "answer": "The key principles of humanoid robotics include anthropomorphic design, bipedal locomotion, and human-like interaction capabilities...",
     "sources": [
       {
         "id": "doc-123",
         "content_snippet": "Humanoid robotics focuses on creating robots with human-like form and behavior...",
         "confidence": 0.95
       }
     ],
     "query_id": "query-456",
     "timestamp": "2025-12-15T10:30:05Z",
     "status": "success"
   }
   ```

## Testing the API

1. **Run unit tests**
   ```bash
   pytest tests/unit/
   ```

2. **Run integration tests**
   ```bash
   pytest tests/integration/
   ```

## API Documentation

- Interactive API documentation available at `http://localhost:8000/docs`
- OpenAPI schema available at `http://localhost:8000/openapi.json`