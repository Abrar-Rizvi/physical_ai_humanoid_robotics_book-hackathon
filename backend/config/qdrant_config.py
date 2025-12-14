"""
Qdrant configuration module for Qdrant Retrieval Pipeline Testing

This module provides configuration management for Qdrant connections.
"""

import os
from dataclasses import dataclass
from typing import Optional


@dataclass
class QdrantConfig:
    """
    Configuration class for Qdrant connection parameters
    """
    host: str = "localhost"
    port: int = 6333
    api_key: Optional[str] = None
    collection_name: str = "default_collection"
    grpc_port: int = 6334
    prefer_grpc: bool = False
    https: bool = False
    timeout: int = 30
    distance: str = "Cosine"

    @classmethod
    def from_env(cls) -> "QdrantConfig":
        """
        Create QdrantConfig from environment variables
        """
        return cls(
            host=os.getenv("QDRANT_HOST", "localhost"),
            port=int(os.getenv("QDRANT_PORT", "6333")),
            api_key=os.getenv("QDRANT_API_KEY"),
            collection_name=os.getenv("QDRANT_COLLECTION_NAME", "default_collection"),
            grpc_port=int(os.getenv("QDRANT_GRPC_PORT", "6334")),
            prefer_grpc=os.getenv("QDRANT_PREFER_GRPC", "False").lower() == "true",
            https=os.getenv("QDRANT_HTTPS", "False").lower() == "true",
            timeout=int(os.getenv("QDRANT_TIMEOUT", "30")),
            distance=os.getenv("QDRANT_DISTANCE", "Cosine")
        )

    def get_client_params(self) -> dict:
        """
        Get parameters for initializing Qdrant client
        """
        params = {
            "host": self.host,
            "port": self.port,
            "timeout": self.timeout
        }

        if self.api_key:
            params["api_key"] = self.api_key

        if self.https:
            params["https"] = True

        if self.prefer_grpc:
            params["prefer_grpc"] = True
            params["grpc_port"] = self.grpc_port

        return params