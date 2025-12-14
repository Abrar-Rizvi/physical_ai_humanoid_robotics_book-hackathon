"""
Validation rules module for Qdrant Retrieval Pipeline Testing

This module provides validation utilities for the retrieval pipeline.
"""

from typing import List, Any, Union
import numpy as np
from backend.models.embedding import Embedding
from backend.models.similarity_query import SimilarityQuery


def validate_embedding_dimensions(embeddings: List[Embedding]) -> bool:
    """
    Validate that all embeddings have the same dimension

    Args:
        embeddings: List of embeddings to validate

    Returns:
        True if all embeddings have the same dimension, False otherwise
    """
    if not embeddings:
        return True

    first_dim = len(embeddings[0].vector)
    return all(len(embedding.vector) == first_dim for embedding in embeddings)


def validate_similarity_score_range(score: float) -> bool:
    """
    Validate that similarity score is between 0 and 1

    Args:
        score: Similarity score to validate

    Returns:
        True if score is in valid range, False otherwise
    """
    return 0.0 <= score <= 1.0


def validate_top_k_limit(top_k: int, collection_size: int = None) -> bool:
    """
    Validate that top_k parameter is positive and not exceed collection size if provided

    Args:
        top_k: Number of results to return
        collection_size: Optional collection size to compare against

    Returns:
        True if top_k is valid, False otherwise
    """
    if top_k <= 0:
        return False

    if collection_size is not None and top_k > collection_size:
        return False

    return True


def validate_accuracy_threshold(accuracy_score: float, threshold: float = 0.95) -> bool:
    """
    Validate that accuracy score meets the threshold

    Args:
        accuracy_score: Accuracy score to validate
        threshold: Minimum threshold (default 0.95 for 95%)

    Returns:
        True if accuracy meets threshold, False otherwise
    """
    return accuracy_score >= threshold


def validate_vector_dimensions(vector: List[float], expected_dimension: int = None) -> bool:
    """
    Validate vector dimensions

    Args:
        vector: Vector to validate
        expected_dimension: Expected dimension if known

    Returns:
        True if vector dimensions are valid, False otherwise
    """
    if not isinstance(vector, list):
        return False

    if not all(isinstance(v, (int, float)) for v in vector):
        return False

    if expected_dimension is not None and len(vector) != expected_dimension:
        return False

    return True


def validate_embedding_vector_consistency(embedding: Embedding, expected_dimension: int = None) -> bool:
    """
    Validate that an embedding's vector is consistent with expected dimensions

    Args:
        embedding: Embedding to validate
        expected_dimension: Expected dimension if known

    Returns:
        True if embedding vector is consistent, False otherwise
    """
    return validate_vector_dimensions(embedding.vector, expected_dimension)


def validate_similarity_query_consistency(query: SimilarityQuery, expected_dimension: int = None) -> bool:
    """
    Validate that a similarity query is consistent

    Args:
        query: Query to validate
        expected_dimension: Expected dimension if known

    Returns:
        True if query is consistent, False otherwise
    """
    # Validate query vector
    if not validate_vector_dimensions(query.query_vector, expected_dimension):
        return False

    # Validate top_k
    if not validate_top_k_limit(query.top_k):
        return False

    return True


def validate_retrieval_result_consistency(result: Any, expected_dimension: int = None) -> bool:
    """
    Validate that a retrieval result is consistent

    Args:
        result: Result to validate
        expected_dimension: Expected dimension if known

    Returns:
        True if result is consistent, False otherwise
    """
    # This would need to be implemented based on the actual result structure
    # For now, we'll just validate that it's not None
    return result is not None


def validate_pipeline_consistency(expected_ids: List[str], retrieved_ids: List[str]) -> dict:
    """
    Validate pipeline consistency by comparing expected vs retrieved IDs

    Args:
        expected_ids: List of expected IDs
        retrieved_ids: List of retrieved IDs

    Returns:
        Dictionary with validation results
    """
    expected_set = set(expected_ids)
    retrieved_set = set(retrieved_ids)

    correct_retrievals = len(expected_set.intersection(retrieved_set))
    total_expected = len(expected_ids)
    total_retrieved = len(retrieved_ids)

    accuracy = correct_retrievals / total_expected if total_expected > 0 else 1.0

    return {
        "accuracy": accuracy,
        "correct_retrievals": correct_retrievals,
        "total_expected": total_expected,
        "total_retrieved": total_retrieved,
        "missing_ids": list(expected_set - retrieved_set),
        "extra_ids": list(retrieved_set - expected_set),
        "passed_threshold": accuracy >= 0.95  # 95% threshold
    }