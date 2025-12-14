"""
RetrievalResult entity model for Qdrant Retrieval Pipeline Testing

This module defines the RetrievalResult entity as specified in the data model.
"""

from dataclasses import dataclass
from typing import Dict, Any


@dataclass
class RetrievalResult:
    """
    Result of a similarity query operation
    """
    id: str  # ID of the matching embedding
    score: float  # Similarity score (float between 0 and 1)
    vector: list  # The matching embedding vector (list of floats)
    payload: Dict[str, Any]  # Metadata associated with the matching embedding (dict)
    collection_name: Optional[str] = None  # Name of the collection where result was found
    distance: Optional[float] = None  # Distance metric (if applicable)

    def __post_init__(self):
        """
        Validate the retrieval result after initialization
        """
        if not isinstance(self.score, (int, float)) or self.score < 0 or self.score > 1:
            raise ValueError("Score must be a float between 0 and 1")

        if not isinstance(self.vector, list):
            raise ValueError("Vector must be a list")

        if not all(isinstance(v, (int, float)) for v in self.vector):
            raise ValueError("All vector elements must be numeric")

        if not isinstance(self.payload, dict):
            raise ValueError("Payload must be a dictionary")