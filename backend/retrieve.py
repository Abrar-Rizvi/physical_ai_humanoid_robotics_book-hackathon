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


class QdrantRetriever:
    """
    A class to handle retrieval operations from Qdrant for testing purposes.
    """

    def __init__(self):
        """
        Initialize the QdrantRetriever with connection parameters from environment.
        """
        self.host = os.getenv("QDRANT_HOST", "localhost")
        self.port = int(os.getenv("QDRANT_PORT", 6333))
        self.api_key = os.getenv("QDRANT_API_KEY")
        self.collection_name = os.getenv("COLLECTION_NAME", "default_collection")

        # Initialize Qdrant client
        if self.api_key:
            self.client = QdrantClient(
                host=self.host,
                port=self.port,
                api_key=self.api_key
            )
        else:
            self.client = QdrantClient(host=self.host, port=self.port)

        logging.info(f"Connected to Qdrant at {self.host}:{self.port}")
        self._validate_collection_exists()

    def _validate_collection_exists(self):
        """
        Validate that the specified collection exists in Qdrant.
        """
        try:
            collections = self.client.get_collections()
            collection_names = [c.name for c in collections.collections]

            if self.collection_name not in collection_names:
                raise ValueError(f"Collection '{self.collection_name}' does not exist in Qdrant. "
                               f"Available collections: {collection_names}")

            logging.info(f"Collection '{self.collection_name}' exists and is accessible")
        except Exception as e:
            logging.error(f"Failed to validate collection: {e}")
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
        """
        start_time = time.perf_counter()

        try:
            # Prepare filter if provided
            qdrant_filter = None
            if query_filter:
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
                collection_name=self.collection_name,
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
            logging.info(f"Search completed in {response_time:.4f}s, found {len(formatted_results)} results")

            return formatted_results

        except Exception as e:
            logging.error(f"Search failed: {e}")
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
        """
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

            logging.info(f"Pipeline validation completed - Accuracy: {accuracy_score:.2%}, "
                        f"Response time: {response_time:.4f}s, "
                        f"Passed: {validation_passed}")

            return validation_result

        except Exception as e:
            logging.error(f"Pipeline validation failed: {e}")
            raise

    def get_collection_info(self) -> Dict[str, Any]:
        """
        Get information about the collection being used for retrieval.

        Returns:
            Dictionary with collection information
        """
        try:
            collection_info = self.client.get_collection(self.collection_name)

            info = {
                'name': collection_info.config.params.vectors_count,
                'vector_size': collection_info.config.params.vector_size if hasattr(collection_info.config.params, 'vector_size') else 'N/A',
                'distance': collection_info.config.params.distance,
                'points_count': collection_info.points_count,
                'indexed_vectors_count': collection_info.indexed_vectors_count
            }

            return info
        except Exception as e:
            logging.error(f"Failed to get collection info: {e}")
            raise


def main():
    """
    Main function to demonstrate the usage of QdrantRetriever.
    """
    logging.basicConfig(level=logging.INFO)

    try:
        # Initialize the retriever
        retriever = QdrantRetriever()

        # Example usage - this would need actual embedding vectors to work
        print("Qdrant Retrieval Module initialized successfully")
        print(f"Connected to collection: {retriever.collection_name}")

        # Show collection info
        collection_info = retriever.get_collection_info()
        print(f"Collection info: {collection_info}")

        # Example search (with placeholder vector - would need real embedding in practice)
        # query_vector = [0.1, 0.2, 0.3]  # This would be a real embedding vector
        # results = retriever.search(query_vector, top_k=3)
        # print(f"Search results: {results}")

    except Exception as e:
        logging.error(f"Error in main: {e}")
        return 1

    return 0


if __name__ == "__main__":
    exit(main())