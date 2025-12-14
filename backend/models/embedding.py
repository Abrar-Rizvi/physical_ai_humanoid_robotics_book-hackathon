"""
Embedding entity model for Qdrant Retrieval Pipeline Testing

This module defines the Embedding entity as specified in the data model.
"""

from dataclasses import dataclass
from typing import Dict, Any, Optional


@dataclass
class Embedding:
    """
    Vector representation of documents or text chunks stored in Qdrant for similarity search
    """
    id: str
    vector: list  # High-dimensional vector representation (list of floats)
    payload: Dict[str, Any]  # Metadata associated with the embedding
    collection_name: str  # Name of the Qdrant collection where it's stored
    text_content: Optional[str] = None  # Optional original text content
    created_at: Optional[str] = None  # Optional timestamp
    updated_at: Optional[str] = None  # Optional timestamp

    def __post_init__(self):
        """
        Validate the embedding after initialization
        """
        if not isinstance(self.vector, list):
            raise ValueError("Vector must be a list")

        if not all(isinstance(v, (int, float)) for v in self.vector):
            raise ValueError("All vector elements must be numeric")

        if not isinstance(self.payload, dict):
            raise ValueError("Payload must be a dictionary")