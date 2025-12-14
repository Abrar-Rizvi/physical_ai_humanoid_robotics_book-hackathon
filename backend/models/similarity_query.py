"""
SimilarityQuery entity model for Qdrant Retrieval Pipeline Testing

This module defines the SimilarityQuery entity as specified in the data model.
"""

from dataclasses import dataclass
from typing import Dict, Any, Optional


@dataclass
class SimilarityQuery:
    """
    Search operation that finds vectors most similar to a given query vector
    """
    query_vector: list  # The vector to search for similar matches (list of floats)
    collection_name: str  # Name of the Qdrant collection to search in (string)
    top_k: int = 5  # Number of results to return (int)
    query_filter: Optional[Dict[str, Any]] = None  # Optional filter conditions for the search (dict, optional)
    query_text: Optional[str] = None  # Optional original text that generated the query vector
    search_params: Optional[Dict[str, Any]] = None  # Optional search parameters

    def __post_init__(self):
        """
        Validate the similarity query after initialization
        """
        if not isinstance(self.query_vector, list):
            raise ValueError("Query vector must be a list")

        if not all(isinstance(v, (int, float)) for v in self.query_vector):
            raise ValueError("All query vector elements must be numeric")

        if not isinstance(self.top_k, int) or self.top_k <= 0:
            raise ValueError("top_k must be a positive integer")

        if self.query_filter is not None and not isinstance(self.query_filter, dict):
            raise ValueError("Query filter must be a dictionary or None")