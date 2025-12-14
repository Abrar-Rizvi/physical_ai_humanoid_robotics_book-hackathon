"""
Base Qdrant connection module for Qdrant Retrieval Pipeline Testing

This module provides base functionality for connecting to Qdrant.
"""

import logging
from typing import Optional, Dict, Any
from qdrant_client import QdrantClient
from qdrant_client.http import models
from backend.config.qdrant_config import QdrantConfig


class QdrantConnection:
    """
    Base class for Qdrant connection handling
    """
    def __init__(self, config: QdrantConfig):
        """
        Initialize Qdrant connection with configuration

        Args:
            config: QdrantConfig instance with connection parameters
        """
        self.config = config
        self.client: Optional[QdrantClient] = None
        self._initialize_client()

    def _initialize_client(self):
        """
        Initialize the Qdrant client based on configuration
        """
        try:
            client_params = self.config.get_client_params()
            self.client = QdrantClient(**client_params)
            logging.info(f"Successfully initialized Qdrant client for {self.config.host}:{self.config.port}")
        except Exception as e:
            logging.error(f"Failed to initialize Qdrant client: {e}")
            raise

    def get_client(self) -> QdrantClient:
        """
        Get the Qdrant client instance

        Returns:
            QdrantClient instance
        """
        if self.client is None:
            raise RuntimeError("Qdrant client not initialized")
        return self.client

    def test_connection(self) -> bool:
        """
        Test the connection to Qdrant

        Returns:
            True if connection is successful, False otherwise
        """
        try:
            if self.client is None:
                return False

            # Try to get collections to test the connection
            self.client.get_collections()
            logging.info("Qdrant connection test successful")
            return True
        except Exception as e:
            logging.error(f"Qdrant connection test failed: {e}")
            return False

    def get_collection_info(self, collection_name: str) -> Optional[Dict[str, Any]]:
        """
        Get information about a specific collection

        Args:
            collection_name: Name of the collection

        Returns:
            Dictionary with collection information or None if collection doesn't exist
        """
        try:
            collection_info = self.client.get_collection(collection_name)
            return {
                "name": collection_info.config.params.vectors_count,
                "vector_size": getattr(collection_info.config.params, 'vector_size', 'N/A'),
                "distance": collection_info.config.params.distance,
                "points_count": collection_info.points_count,
                "indexed_vectors_count": collection_info.indexed_vectors_count,
                "config": collection_info.config.dict() if hasattr(collection_info.config, 'dict') else {}
            }
        except Exception as e:
            logging.error(f"Failed to get collection info for {collection_name}: {e}")
            return None

    def collection_exists(self, collection_name: str) -> bool:
        """
        Check if a collection exists

        Args:
            collection_name: Name of the collection to check

        Returns:
            True if collection exists, False otherwise
        """
        try:
            collections = self.client.get_collections()
            collection_names = [c.name for c in collections.collections]
            return collection_name in collection_names
        except Exception as e:
            logging.error(f"Failed to check if collection exists {collection_name}: {e}")
            return False

    def create_collection(
        self,
        collection_name: str,
        vector_size: int,
        distance: str = "Cosine",
        shard_number: int = 1,
        replication_factor: int = 1
    ) -> bool:
        """
        Create a new collection in Qdrant

        Args:
            collection_name: Name of the collection to create
            vector_size: Size of the vectors
            distance: Distance metric to use (Cosine, Euclid, Dot)
            shard_number: Number of shards
            replication_factor: Replication factor

        Returns:
            True if collection was created successfully, False otherwise
        """
        try:
            if self.collection_exists(collection_name):
                logging.info(f"Collection {collection_name} already exists")
                return True

            self.client.create_collection(
                collection_name=collection_name,
                vectors_config=models.VectorParams(
                    size=vector_size,
                    distance=models.Distance[distance.upper()]
                ),
                shard_number=shard_number,
                replication_factor=replication_factor
            )
            logging.info(f"Successfully created collection {collection_name}")
            return True
        except Exception as e:
            logging.error(f"Failed to create collection {collection_name}: {e}")
            return False

    def close(self):
        """
        Close the Qdrant connection
        """
        if self.client:
            # QdrantClient doesn't have a close method, so we just set it to None
            self.client = None
            logging.info("Qdrant connection closed")