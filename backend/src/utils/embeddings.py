import asyncio
from typing import List, Union
import numpy as np
from openai import OpenAI
from ..clients.openai_client import openai_client
from ..config import settings


def get_embedding(text: str, model: str = None) -> List[float]:
    """
    Get embedding for a single text using OpenAI's embedding API
    """
    if model is None:
        model = settings.embedding_model

    response = openai_client.embeddings.create(
        input=text,
        model=model
    )
    return response.data[0].embedding


def get_embeddings(texts: List[str], model: str = None) -> List[List[float]]:
    """
    Get embeddings for multiple texts using OpenAI's embedding API
    """
    if model is None:
        model = settings.embedding_model

    response = openai_client.embeddings.create(
        input=texts,
        model=model
    )
    return [item.embedding for item in response.data]


async def aget_embedding(text: str, model: str = None) -> List[float]:
    """
    Async version to get embedding for a single text
    """
    if model is None:
        model = settings.embedding_model

    response = await openai_client.embeddings.create(
        input=text,
        model=model
    )
    return response.data[0].embedding


async def aget_embeddings(texts: List[str], model: str = None) -> List[List[float]]:
    """
    Async version to get embeddings for multiple texts
    """
    if model is None:
        model = settings.embedding_model

    response = await openai_client.embeddings.create(
        input=texts,
        model=model
    )
    return [item.embedding for item in response.data]


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