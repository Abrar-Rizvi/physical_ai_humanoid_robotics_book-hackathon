"""
Collection validation module for Qdrant Retrieval Pipeline Testing

This module provides functionality for validating Qdrant collections.
"""

import logging
from typing import Dict, Any, Optional, List
from qdrant_client import QdrantClient
from backend.core.qdrant_connection import QdrantConnection
from backend.config.qdrant_config import QdrantConfig


class CollectionValidationResult:
    """
    Result of a collection validation
    """
    def __init__(
        self,
        is_valid: bool,
        collection_name: str,
        issues: List[str],
        details: Dict[str, Any]
    ):
        self.is_valid = is_valid
        self.collection_name = collection_name
        self.issues = issues
        self.details = details

    def __str__(self) -> str:
        status = "VALID" if self.is_valid else "INVALID"
        return f"Collection '{self.collection_name}': {status} - {len(self.issues)} issues"


class CollectionValidator:
    """
    Class for validating Qdrant collections
    """
    def __init__(self, qdrant_connection: QdrantConnection):
        """
        Initialize the collection validator

        Args:
            qdrant_connection: QdrantConnection instance
        """
        self.qdrant_connection = qdrant_connection
        self.client = qdrant_connection.get_client()

    def validate_collection_exists(self, collection_name: str) -> CollectionValidationResult:
        """
        Validate that a collection exists

        Args:
            collection_name: Name of the collection to validate

        Returns:
            CollectionValidationResult with validation details
        """
        issues = []

        if not self.qdrant_connection.collection_exists(collection_name):
            issues.append(f"Collection '{collection_name}' does not exist")

        return CollectionValidationResult(
            is_valid=len(issues) == 0,
            collection_name=collection_name,
            issues=issues,
            details={"exists": len(issues) == 0}
        )

    def validate_collection_schema(self, collection_name: str, expected_vector_size: Optional[int] = None) -> CollectionValidationResult:
        """
        Validate the schema of a collection (vector size, distance metric, etc.)

        Args:
            collection_name: Name of the collection to validate
            expected_vector_size: Expected vector size (optional)

        Returns:
            CollectionValidationResult with validation details
        """
        issues = []

        # Check if collection exists first
        exists_result = self.validate_collection_exists(collection_name)
        if not exists_result.is_valid:
            issues.extend(exists_result.issues)
            return CollectionValidationResult(
                is_valid=False,
                collection_name=collection_name,
                issues=issues,
                details={}
            )

        try:
            collection_info = self.client.get_collection(collection_name)
            config = collection_info.config

            # Check vector size if expected size is provided
            if expected_vector_size is not None:
                actual_vector_size = getattr(config.params, 'vector_size', None)
                if actual_vector_size != expected_vector_size:
                    issues.append(
                        f"Vector size mismatch: expected {expected_vector_size}, "
                        f"got {actual_vector_size}"
                    )

            # Check distance metric
            actual_distance = config.params.distance
            if not actual_distance:
                issues.append("Distance metric not defined in collection")

            # Check if vectors config is properly set
            if not config.params.vectors_count:
                issues.append("Collection has no vectors configured")

        except Exception as e:
            issues.append(f"Failed to get collection schema: {str(e)}")

        return CollectionValidationResult(
            is_valid=len(issues) == 0,
            collection_name=collection_name,
            issues=issues,
            details={
                "expected_vector_size": expected_vector_size,
                "actual_vector_size": getattr(config.params, 'vector_size', None) if 'config' in locals() else None,
                "distance_metric": config.params.distance if 'config' in locals() else None
            }
        )

    def validate_collection_health(self, collection_name: str) -> CollectionValidationResult:
        """
        Validate the health of a collection (indexed vectors, points count, etc.)

        Args:
            collection_name: Name of the collection to validate

        Returns:
            CollectionValidationResult with validation details
        """
        issues = []

        # Check if collection exists first
        exists_result = self.validate_collection_exists(collection_name)
        if not exists_result.is_valid:
            issues.extend(exists_result.issues)
            return CollectionValidationResult(
                is_valid=False,
                collection_name=collection_name,
                issues=issues,
                details={}
            )

        try:
            collection_info = self.client.get_collection(collection_name)

            # Check if there are any points in the collection
            points_count = collection_info.points_count
            indexed_vectors_count = collection_info.indexed_vectors_count

            details = {
                "points_count": points_count,
                "indexed_vectors_count": indexed_vectors_count,
                "is_empty": points_count == 0
            }

            # Check if all vectors are indexed
            if points_count > 0 and indexed_vectors_count == 0:
                issues.append("Collection has points but no indexed vectors - search may not work properly")

            # Check if there's a significant gap between points and indexed vectors
            if points_count > 0 and indexed_vectors_count < points_count * 0.9:
                issues.append(
                    f"Only {indexed_vectors_count}/{points_count} vectors are indexed "
                    f"({indexed_vectors_count/points_count*100:.1f}%)"
                )

        except Exception as e:
            issues.append(f"Failed to get collection health info: {str(e)}")
            details = {}

        return CollectionValidationResult(
            is_valid=len(issues) == 0,
            collection_name=collection_name,
            issues=issues,
            details=details
        )

    def validate_collection_access(self, collection_name: str) -> CollectionValidationResult:
        """
        Validate that the collection can be accessed (read/write operations)

        Args:
            collection_name: Name of the collection to validate

        Returns:
            CollectionValidationResult with validation details
        """
        issues = []

        # Check if collection exists first
        exists_result = self.validate_collection_exists(collection_name)
        if not exists_result.is_valid:
            issues.extend(exists_result.issues)
            return CollectionValidationResult(
                is_valid=False,
                collection_name=collection_name,
                issues=issues,
                details={}
            )

        try:
            # Try a simple count operation to test read access
            collection_info = self.client.get_collection(collection_name)
            points_count = collection_info.points_count

            # Store details about access test
            details = {
                "read_access": True,
                "points_count": points_count
            }

            # If we got here, read access is working
            logging.info(f"Collection {collection_name} access validation passed")

        except Exception as e:
            issues.append(f"Failed to access collection: {str(e)}")
            details = {"read_access": False}

        return CollectionValidationResult(
            is_valid=len(issues) == 0,
            collection_name=collection_name,
            issues=issues,
            details=details
        )

    def validate_collection_completely(self, collection_name: str, expected_vector_size: Optional[int] = None) -> CollectionValidationResult:
        """
        Perform complete validation of a collection

        Args:
            collection_name: Name of the collection to validate
            expected_vector_size: Expected vector size (optional)

        Returns:
            CollectionValidationResult with validation details
        """
        all_issues = []

        # Run all validation checks
        exists_result = self.validate_collection_exists(collection_name)
        if not exists_result.is_valid:
            all_issues.extend(exists_result.issues)
            # If collection doesn't exist, we can't continue with other validations
            return CollectionValidationResult(
                is_valid=False,
                collection_name=collection_name,
                issues=all_issues,
                details=exists_result.details
            )

        schema_result = self.validate_collection_schema(collection_name, expected_vector_size)
        health_result = self.validate_collection_health(collection_name)
        access_result = self.validate_collection_access(collection_name)

        # Combine all issues
        all_issues.extend(schema_result.issues)
        all_issues.extend(health_result.issues)
        all_issues.extend(access_result.issues)

        # Combine all details
        combined_details = {
            "exists": exists_result.details,
            "schema": schema_result.details,
            "health": health_result.details,
            "access": access_result.details
        }

        return CollectionValidationResult(
            is_valid=len(all_issues) == 0,
            collection_name=collection_name,
            issues=all_issues,
            details=combined_details
        )

    def validate_all_collections(self) -> Dict[str, CollectionValidationResult]:
        """
        Validate all collections in the Qdrant instance

        Returns:
            Dictionary mapping collection names to their validation results
        """
        results = {}

        try:
            collections = self.client.get_collections()
            collection_names = [c.name for c in collections.collections]

            for collection_name in collection_names:
                results[collection_name] = self.validate_collection_completely(collection_name)

        except Exception as e:
            logging.error(f"Failed to validate all collections: {str(e)}")

        return results