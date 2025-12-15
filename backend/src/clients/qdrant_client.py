from qdrant_client import QdrantClient
from qdrant_client.http import models
from ..config import settings


def create_qdrant_client() -> QdrantClient:
    """
    Create and configure Qdrant client with connection details from settings
    """
    client = QdrantClient(
        url=settings.qdrant_url,
        api_key=settings.qdrant_api_key,
        prefer_grpc=False  # Set to True if you have gRPC available
    )
    return client


def verify_collection_exists(client: QdrantClient, collection_name: str) -> bool:
    """
    Verify that the specified collection exists in Qdrant
    """
    try:
        client.get_collection(collection_name)
        return True
    except Exception:
        return False


# Global client instance
qdrant_client = create_qdrant_client()