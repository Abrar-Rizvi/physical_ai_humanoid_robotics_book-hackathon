"""
Environment validation module for Qdrant Retrieval Pipeline Testing

This module provides validation for environment variables and configuration.
"""

import os
from typing import List, Tuple
from .qdrant_config import QdrantConfig


class EnvironmentValidationError(Exception):
    """
    Exception raised when environment validation fails
    """
    pass


def validate_required_env_vars(required_vars: List[str]) -> List[str]:
    """
    Validate that required environment variables are set

    Args:
        required_vars: List of required environment variable names

    Returns:
        List of missing environment variable names
    """
    missing_vars = []
    for var in required_vars:
        if not os.getenv(var):
            missing_vars.append(var)
    return missing_vars


def validate_qdrant_connection_params() -> Tuple[bool, List[str]]:
    """
    Validate Qdrant connection parameters from environment

    Returns:
        Tuple of (is_valid, list_of_errors)
    """
    errors = []

    # Validate QDRANT_HOST
    host = os.getenv("QDRANT_HOST")
    if not host:
        errors.append("QDRANT_HOST environment variable is not set")

    # Validate QDRANT_PORT
    port_str = os.getenv("QDRANT_PORT")
    if port_str:
        try:
            port = int(port_str)
            if port <= 0 or port > 65535:
                errors.append(f"QDRANT_PORT must be between 1 and 65535, got {port}")
        except ValueError:
            errors.append(f"QDRANT_PORT must be a valid integer, got {port_str}")
    else:
        # If not set, default port 6333 will be used, which is valid
        pass

    # Validate QDRANT_COLLECTION_NAME
    collection_name = os.getenv("QDRANT_COLLECTION_NAME")
    if not collection_name:
        errors.append("QDRANT_COLLECTION_NAME environment variable is not set")

    return len(errors) == 0, errors


def validate_environment() -> Tuple[bool, List[str]]:
    """
    Validate the complete environment for Qdrant retrieval pipeline

    Returns:
        Tuple of (is_valid, list_of_errors)
    """
    errors = []

    # Validate required environment variables
    required_vars = ["QDRANT_HOST", "QDRANT_COLLECTION_NAME"]
    missing_vars = validate_required_env_vars(required_vars)
    errors.extend([f"Missing required environment variable: {var}" for var in missing_vars])

    # Validate Qdrant connection parameters
    _, qdrant_errors = validate_qdrant_connection_params()
    errors.extend(qdrant_errors)

    return len(errors) == 0, errors


def ensure_environment() -> QdrantConfig:
    """
    Ensure environment is valid and return QdrantConfig

    Returns:
        QdrantConfig instance

    Raises:
        EnvironmentValidationError: If environment validation fails
    """
    is_valid, errors = validate_environment()
    if not is_valid:
        raise EnvironmentValidationError(
            f"Environment validation failed with {len(errors)} error(s):\n" +
            "\n".join(f"- {error}" for error in errors)
        )

    return QdrantConfig.from_env()