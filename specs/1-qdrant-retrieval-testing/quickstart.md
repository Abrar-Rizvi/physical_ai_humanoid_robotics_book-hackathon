# Quickstart: Qdrant Retrieval Pipeline Testing

## Prerequisites

- Python 3.11+
- Qdrant server running (local or remote)
- Embeddings already stored in Qdrant collection
- Access to environment variables for Qdrant connection

## Setup

1. **Install dependencies**:
   ```bash
   pip install qdrant-client python-dotenv numpy
   ```

2. **Configure environment**:
   Copy `.env.example` to `.env` and update with your Qdrant connection details:
   ```bash
   QDRANT_HOST=localhost
   QDRANT_PORT=6333
   QDRANT_API_KEY=your_api_key_here  # if using cloud instance
   COLLECTION_NAME=your_collection_name
   ```

3. **Verify Qdrant connection**:
   Ensure your Qdrant instance is running and accessible with the provided credentials.

## Basic Usage

1. **Import the retrieval module**:
   ```python
   from backend.retrieve import QdrantRetriever
   ```

2. **Initialize the retriever**:
   ```python
   retriever = QdrantRetriever()
   ```

3. **Perform a similarity search**:
   ```python
   query_vector = [0.1, 0.2, 0.3, ...]  # Your query embedding
   results = retriever.search(query_vector, top_k=5)
   ```

4. **Validate pipeline**:
   ```python
   validation_result = retriever.validate_pipeline(
       query_text="Your test query",
       expected_ids=["id1", "id2", "id3"]
   )
   print(f"Accuracy: {validation_result['accuracy_score']}")
   print(f"Response time: {validation_result['response_time']}s")
   ```

## Testing

Run the tests to verify functionality:
```bash
cd backend
python -m pytest tests/test_retrieve.py -v
```

## Environment Variables

- `QDRANT_HOST`: Qdrant server host (default: localhost)
- `QDRANT_PORT`: Qdrant server port (default: 6333)
- `QDRANT_API_KEY`: API key for Qdrant Cloud (optional)
- `COLLECTION_NAME`: Name of the Qdrant collection to query
- `EMBEDDING_DIM`: Dimension of the embeddings (for validation)