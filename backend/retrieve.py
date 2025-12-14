"""
Qdrant Retrieval Module for Testing RAG Pipeline

This module provides functionality to retrieve stored embeddings from Qdrant,
run similarity queries, and validate the end-to-end extraction + embedding +
vector storage pipeline works correctly.
"""

import os
import time
import logging
from typing import List, Dict, Any, Optional
from dotenv import load_dotenv
import numpy as np

# Load environment variables
load_dotenv()

try:
    from qdrant_client import QdrantClient
    from qdrant_client.http import models
    from qdrant_client.http.models import Distance, VectorParams, PointStruct
except ImportError:
    raise ImportError("Please install qdrant-client: pip install qdrant-client")

from backend.config.qdrant_config import QdrantConfig
from backend.core.qdrant_connection import QdrantConnection
from backend.core.collection_validator import CollectionValidator
from backend.utils.performance import PerformanceTimer, validate_response_time_threshold


class QdrantRetriever:
    """
    A class to handle retrieval operations from Qdrant for testing purposes.
    """

    def __init__(self, config: QdrantConfig = None):
        """
        Initialize the QdrantRetriever with connection parameters from environment or config.

        Args:
            config: Optional QdrantConfig instance. If not provided, will use environment variables.
        """
        self.config = config or QdrantConfig.from_env()
        try:
            self.qdrant_connection = QdrantConnection(self.config)
            self.client = self.qdrant_connection.get_client()
            self.collection_validator = CollectionValidator(self.qdrant_connection)

            logging.info(f"Connected to Qdrant at {self.config.host}:{self.config.port}")
            self._validate_collection_exists()
        except Exception as e:
            logging.error(f"Failed to initialize QdrantRetriever: {e}")
            raise

    def _validate_collection_exists(self):
        """
        Validate that the specified collection exists in Qdrant.
        """
        try:
            validation_result = self.collection_validator.validate_collection_exists(self.config.collection_name)

            if not validation_result.is_valid:
                raise ValueError(f"Collection '{self.config.collection_name}' does not exist in Qdrant. "
                               f"Issues: {validation_result.issues}")

            logging.info(f"Collection '{self.config.collection_name}' exists and is accessible")
        except ValueError:
            # Re-raise ValueError as is since it's a validation issue
            raise
        except Exception as e:
            logging.error(f"Unexpected error during collection validation: {e}")
            raise

    def search(self, query_vector: List[float], top_k: int = 5, query_filter: Optional[Dict] = None) -> List[Dict[str, Any]]:
        """
        Perform a similarity search in Qdrant.

        Args:
            query_vector: The embedding vector to search for
            top_k: Number of results to return
            query_filter: Optional filter conditions for the search

        Returns:
            List of matching results with id, score, and payload

        Raises:
            Exception: If search operation fails
        """
        start_time = time.perf_counter()

        # Validate inputs
        if not isinstance(query_vector, list) or not query_vector:
            raise ValueError("query_vector must be a non-empty list")

        if not isinstance(top_k, int) or top_k <= 0:
            raise ValueError("top_k must be a positive integer")

        try:
            # Prepare filter if provided
            qdrant_filter = None
            if query_filter:
                if not isinstance(query_filter, dict):
                    raise ValueError("query_filter must be a dictionary")

                qdrant_filter = models.Filter(
                    must=[
                        models.FieldCondition(
                            key=key,
                            match=models.MatchValue(value=value)
                        ) for key, value in query_filter.items()
                    ]
                )

            # Perform the search
            results = self.client.search(
                collection_name=self.config.collection_name,
                query_vector=query_vector,
                limit=top_k,
                query_filter=qdrant_filter
            )

            # Format results
            formatted_results = []
            for result in results:
                formatted_results.append({
                    'id': result.id,
                    'score': result.score,
                    'payload': result.payload
                })

            response_time = time.perf_counter() - start_time

            # Validate response time threshold (T019)
            time_within_threshold = validate_response_time_threshold(response_time, 2.0)
            status_msg = "within" if time_within_threshold else "exceeding"
            logging.info(f"Search completed {status_msg} threshold in {response_time:.4f}s, found {len(formatted_results)} results")

            return formatted_results

        except Exception as e:
            error_msg = f"Search failed for query vector of length {len(query_vector)} with top_k={top_k}: {e}"
            logging.error(error_msg)
            raise

    def validate_pipeline(self, query_text: str, expected_ids: List[str], query_vector: List[float], top_k: int = 5) -> Dict[str, Any]:
        """
        Validate the end-to-end pipeline by checking if expected embeddings are retrieved.

        Args:
            query_text: Original text used for validation
            expected_ids: Expected embedding IDs that should be retrieved
            query_vector: The embedding vector to search for
            top_k: Number of results to return for validation

        Returns:
            Dictionary with validation results including accuracy and response time

        Raises:
            Exception: If pipeline validation fails
        """
        if not isinstance(query_text, str):
            raise ValueError("query_text must be a string")

        if not isinstance(expected_ids, list):
            raise ValueError("expected_ids must be a list")

        if not isinstance(query_vector, list) or not query_vector:
            raise ValueError("query_vector must be a non-empty list")

        if not isinstance(top_k, int) or top_k <= 0:
            raise ValueError("top_k must be a positive integer")

        start_time = time.perf_counter()

        try:
            # Perform the search
            results = self.search(query_vector, top_k)

            # Calculate accuracy
            retrieved_ids = [result['id'] for result in results]
            expected_set = set(expected_ids)
            retrieved_set = set(retrieved_ids)

            # Calculate accuracy as percentage of expected items that were retrieved
            if len(expected_ids) > 0:
                correct_retrievals = len(expected_set.intersection(retrieved_set))
                accuracy_score = correct_retrievals / len(expected_ids)
            else:
                accuracy_score = 1.0  # Perfect if nothing expected

            response_time = time.perf_counter() - start_time

            # Determine if validation passed (using 95% threshold)
            validation_passed = accuracy_score >= 0.95

            validation_result = {
                'query_text': query_text,
                'expected_ids': expected_ids,
                'retrieved_ids': retrieved_ids,
                'accuracy_score': accuracy_score,
                'response_time': response_time,
                'validation_passed': validation_passed,
                'details': {
                    'correct_retrievals': correct_retrievals,
                    'total_expected': len(expected_ids),
                    'total_retrieved': len(retrieved_ids),
                    'missing_ids': list(expected_set - retrieved_set),
                    'extra_ids': list(retrieved_set - expected_set)
                }
            }

            # Validate response time threshold (T029)
            time_within_threshold = validate_response_time_threshold(response_time, 2.0)
            status_msg = "within" if time_within_threshold else "exceeding"
            logging.info(f"Pipeline validation completed - Accuracy: {accuracy_score:.2%}, "
                        f"Response time {status_msg} threshold: {response_time:.4f}s, "
                        f"Passed: {validation_passed}")

            return validation_result

        except Exception as e:
            error_msg = f"Pipeline validation failed for query '{query_text[:50]}...' with {len(expected_ids)} expected IDs: {e}"
            logging.error(error_msg)
            raise

    def get_collection_info(self) -> Dict[str, Any]:
        """
        Get information about the collection being used for retrieval.

        Returns:
            Dictionary with collection information

        Raises:
            Exception: If collection info retrieval fails
        """
        try:
            collection_info = self.client.get_collection(self.config.collection_name)

            info = {
                'name': self.config.collection_name,
                'vector_size': getattr(collection_info.config.params, 'vector_size', 'N/A'),
                'distance': collection_info.config.params.distance,
                'points_count': collection_info.points_count,
                'indexed_vectors_count': collection_info.indexed_vectors_count
            }

            return info
        except Exception as e:
            logging.error(f"Failed to get collection info for {self.config.collection_name}: {e}")
            raise

    def connect_to_qdrant(self):
        """
        T015: Implement Qdrant connection initialization
        """
        try:
            # This is already handled in __init__ via QdrantConnection
            result = self.qdrant_connection.test_connection()
            if result:
                logging.info("Qdrant connection initialization successful")
            else:
                logging.warning("Qdrant connection initialization failed")
            return result
        except Exception as e:
            logging.error(f"Error during Qdrant connection initialization: {e}")
            raise

    def validate_collection(self):
        """
        T016: Implement collection validation
        """
        try:
            result = self.collection_validator.validate_collection_completely(self.config.collection_name)
            logging.info(f"Collection validation completed for {self.config.collection_name}: {result}")
            return result
        except Exception as e:
            logging.error(f"Error during collection validation: {e}")
            raise

    def implement_query_filtering(self, query_vector: List[float], top_k: int = 5, query_filter: Optional[Dict] = None):
        """
        T018: Implement query filtering functionality
        """
        try:
            # This is already implemented in the search method
            result = self.search(query_vector, top_k, query_filter)
            logging.info(f"Query filtering executed with {len(result)} results returned")
            return result
        except Exception as e:
            logging.error(f"Error during query filtering: {e}")
            raise

    def measure_response_time(self, query_vector: List[float], top_k: int = 5):
        """
        T019: Implement response time measurement
        """
        try:
            timer = PerformanceTimer()
            timer.start()

            results = self.search(query_vector, top_k)

            timer.stop()
            response_time = timer.elapsed_time

            logging.info(f"Measured response time: {response_time:.4f}s for search with {top_k} results")

            return {
                'results': results,
                'response_time': response_time,
                'within_threshold': validate_response_time_threshold(response_time, 2.0)
            }
        except Exception as e:
            logging.error(f"Error during response time measurement: {e}")
            raise

    def validate_response_time_threshold(self, response_time: float, threshold: float = 2.0) -> bool:
        """
        Validate if response time is within acceptable threshold

        Args:
            response_time: Response time in seconds
            threshold: Maximum allowed response time in seconds

        Returns:
            True if within threshold, False otherwise
        """
        try:
            is_within = response_time <= threshold
            logging.debug(f"Response time {response_time:.4f}s {'is' if is_within else 'is not'} within threshold {threshold}s")
            return is_within
        except Exception as e:
            logging.error(f"Error validating response time threshold: {e}")
            return False

    def validate_accuracy_threshold(self, accuracy_score: float, threshold: float = 0.95) -> bool:
        """
        Validate if accuracy score meets the required threshold

        Args:
            accuracy_score: Accuracy score between 0 and 1
            threshold: Minimum required accuracy

        Returns:
            True if meets threshold, False otherwise
        """
        try:
            meets_threshold = accuracy_score >= threshold
            logging.debug(f"Accuracy {accuracy_score:.4f} {'meets' if meets_threshold else 'does not meet'} threshold {threshold}")
            return meets_threshold
        except Exception as e:
            logging.error(f"Error validating accuracy threshold: {e}")
            return False


def main():
    """
    Main function to demonstrate the usage of QdrantRetriever.
    """
    logging.basicConfig(level=logging.INFO)

    try:
        # Initialize the retriever
        retriever = QdrantRetriever()

        # Example usage - this would need actual embedding vectors to work
        logging.info("Qdrant Retrieval Module initialized successfully")
        logging.info(f"Connected to collection: {retriever.config.collection_name}")

        # Show collection info
        collection_info = retriever.get_collection_info()
        logging.info(f"Collection info: {collection_info}")

        # Example search (with placeholder vector - would need real embedding in practice)
        # query_vector = [0.1, 0.2, 0.3]  # This would be a real embedding vector
        # results = retriever.search(query_vector, top_k=3)
        # logging.info(f"Search results: {results}")

    except Exception as e:
        logging.error(f"Error in main: {e}", exc_info=True)
        return 1

    logging.info("Qdrant Retrieval Module execution completed successfully")
    return 0


if __name__ == "__main__":
    exit(main())