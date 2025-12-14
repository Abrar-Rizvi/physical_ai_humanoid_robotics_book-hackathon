"""
PipelineValidation entity model for Qdrant Retrieval Pipeline Testing

This module defines the PipelineValidation entity as specified in the data model.
"""

from dataclasses import dataclass
from typing import List, Dict, Any
from .embedding import Embedding
from .retrieval_result import RetrievalResult


@dataclass
class PipelineValidation:
    """
    Validation result for the end-to-end pipeline
    """
    query_text: str  # Original text used for validation (string)
    expected_results: List[Embedding]  # Expected embeddings that should be retrieved (list of Embedding)
    actual_results: List[RetrievalResult]  # Actual embeddings retrieved by the system (list of RetrievalResult)
    accuracy_score: float  # Percentage of correct matches (float between 0 and 1)
    response_time: float  # Time taken for the query (float in seconds)
    validation_passed: bool  # Whether the validation met accuracy threshold (boolean)
    details: Dict[str, Any]  # Additional validation details
    query_vector: List[float] = None  # The query vector used for validation
    collection_name: str = "default_collection"  # Name of the collection tested

    def __post_init__(self):
        """
        Validate the pipeline validation after initialization
        """
        if not isinstance(self.query_text, str):
            raise ValueError("Query text must be a string")

        if not isinstance(self.expected_results, list):
            raise ValueError("Expected results must be a list")

        if not isinstance(self.actual_results, list):
            raise ValueError("Actual results must be a list")

        if not isinstance(self.accuracy_score, (int, float)) or self.accuracy_score < 0 or self.accuracy_score > 1:
            raise ValueError("Accuracy score must be a float between 0 and 1")

        if not isinstance(self.response_time, (int, float)) or self.response_time < 0:
            raise ValueError("Response time must be a non-negative number")

        if not isinstance(self.validation_passed, bool):
            raise ValueError("Validation passed must be a boolean")

        if not isinstance(self.details, dict):
            raise ValueError("Details must be a dictionary")