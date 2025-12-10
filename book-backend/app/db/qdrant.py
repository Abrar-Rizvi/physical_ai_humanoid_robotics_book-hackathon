# book-backend/app/db/qdrant.py
import os
from qdrant_client import QdrantClient, models
from typing import List, Dict, Any

QDRANT_URL = os.getenv("QDRANT_URL")
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")
QDRANT_COLLECTION_NAME = os.getenv("QDRANT_COLLECTION_NAME", "rag_book_content")

qdrant_client = QdrantClient(
    url=QDRANT_URL,
    api_key=QDRANT_API_KEY,
)

async def initialize_qdrant_collection(vector_size: int = 1536):
    """
    Initializes the Qdrant collection if it does not already exist.
    """
    try:
        qdrant_client.recreate_collection(
            collection_name=QDRANT_COLLECTION_NAME,
            vectors_config=models.VectorParams(size=vector_size, distance=models.Distance.COSINE),
        )
        print(f"Collection '{QDRANT_COLLECTION_NAME}' re-created successfully.")
    except Exception as e:
        print(f"Collection '{QDRANT_COLLECTION_NAME}' already exists or failed to re-create: {e}")

async def upsert_vectors(points: List[models.PointStruct]):
    """
    Upserts (inserts or updates) vectors into the Qdrant collection.
    """
    try:
        response = qdrant_client.upsert(
            collection_name=QDRANT_COLLECTION_NAME,
            wait=True,
            points=points
        )
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to upsert vectors to Qdrant: {e}")

async def search_vectors(
    query_vector: List[float],
    limit: int = 5,
    query_filter: Dict[str, Any] = None
):
    """
    Searches the Qdrant collection for vectors similar to the query vector.
    """
    try:
        search_result = qdrant_client.search(
            collection_name=QDRANT_COLLECTION_NAME,
            query_vector=query_vector,
            query_filter=query_filter,
            limit=limit,
        )
        return search_result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to search Qdrant: {e}")
