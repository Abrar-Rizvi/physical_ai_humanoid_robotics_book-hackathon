import asyncio
import os
from typing import List, Union
import numpy as np
from openai import OpenAI
import cohere
from ..clients.openai_client import openai_client
from ..config import settings


def get_embedding(text: str, model: str = None) -> List[float]:
    """
    Get embedding for a single text using either OpenAI or Cohere based on configuration
    """
    if model is None:
        model = settings.embedding_model

    # Check if we should use Cohere based on the model name or an environment variable
    use_cohere = settings.embedding_model.startswith('embed-') or os.getenv('USE_COHERE_EMBEDDINGS', '').lower() == 'true'

    if use_cohere:
        # Use Cohere embeddings (typically 1024 dimensions)
        cohere_api_key = settings.cohere_api_key
        if not cohere_api_key:
            raise ValueError("COHERE_API_KEY environment variable is required when using Cohere embeddings")

        cohere_client = cohere.Client(cohere_api_key)

        # Cohere embedding call
        response = cohere_client.embed(
            texts=[text],
            model=settings.embedding_model if settings.embedding_model.startswith('embed-') else "embed-english-v3.0",
            input_type="search_query"  # or "search_document" for documents
        )
        return response.embeddings[0]
    else:
        # Use OpenAI embeddings
        response = openai_client.embeddings.create(
            input=text,
            model=model
        )
        return response.data[0].embedding


def get_embeddings(texts: List[str], model: str = None) -> List[List[float]]:
    """
    Get embeddings for multiple texts using either OpenAI or Cohere based on configuration
    """
    if model is None:
        model = settings.embedding_model

    # Check if we should use Cohere based on the model name or an environment variable
    use_cohere = settings.embedding_model.startswith('embed-') or os.getenv('USE_COHERE_EMBEDDINGS', '').lower() == 'true'

    if use_cohere:
        # Use Cohere embeddings (typically 1024 dimensions)
        cohere_api_key = settings.cohere_api_key
        if not cohere_api_key:
            raise ValueError("COHERE_API_KEY environment variable is required when using Cohere embeddings")

        cohere_client = cohere.Client(cohere_api_key)

        # Cohere embedding call
        response = cohere_client.embed(
            texts=texts,
            model=settings.embedding_model if settings.embedding_model.startswith('embed-') else "embed-english-v3.0",
            input_type="search_document"  # or "search_query" for queries
        )
        return response.embeddings
    else:
        # Use OpenAI embeddings
        response = openai_client.embeddings.create(
            input=texts,
            model=model
        )
        return [item.embedding for item in response.data]


async def aget_embedding(text: str, model: str = None) -> List[float]:
    """
    Async version to get embedding for a single text
    Note: Currently using synchronous calls since Cohere doesn't have native async support
    """
    # For now, just call the sync version since Cohere doesn't have native async support
    return get_embedding(text, model)


async def aget_embeddings(texts: List[str], model: str = None) -> List[List[float]]:
    """
    Async version to get embeddings for multiple texts
    Note: Currently using synchronous calls since Cohere doesn't have native async support
    """
    # For now, just call the sync version since Cohere doesn't have native async support
    return get_embeddings(texts, model)


def cosine_similarity(vec1: List[float], vec2: List[float]) -> float:
    """
    Calculate cosine similarity between two vectors
    """
    # Convert to numpy arrays
    v1 = np.array(vec1)
    v2 = np.array(vec2)

    # Calculate cosine similarity
    dot_product = np.dot(v1, v2)
    norm_v1 = np.linalg.norm(v1)
    norm_v2 = np.linalg.norm(v2)

    if norm_v1 == 0 or norm_v2 == 0:
        return 0.0

    return float(dot_product / (norm_v1 * norm_v2))