import asyncio
from typing import List, Dict, Any, Optional
from qdrant_client.http import models
from .clients.qdrant_client import qdrant_client
from .utils.embeddings import get_embedding
from .config import settings
from .models.response_models import RetrievedContext


async def retrieve_context(query: str, top_k: int = None) -> RetrievedContext:
    """
    Retrieve relevant context from Qdrant based on the query
    """
    if top_k is None:
        top_k = settings.top_k_results

    # Get embedding for the query
    query_embedding = get_embedding(query)

    # Search in Qdrant for similar vectors
    search_results = qdrant_client.search(
        collection_name=settings.qdrant_collection_name,
        query_vector=query_embedding,
        limit=top_k,
        with_payload=True,
        score_threshold=settings.min_similarity_threshold
    )

    # Format the results
    documents = []
    for result in search_results:
        document = {
            "id": result.id,
            "content": result.payload.get("content", ""),
            "metadata": result.payload.get("metadata", {}),
            "score": result.score
        }
        documents.append(document)

    # Create RetrievedContext object
    retrieved_context = RetrievedContext(
        documents=documents,
        query_embedding=query_embedding,
        retrieval_method="semantic_search"
    )

    return retrieved_context


def format_context_for_agent(retrieved_context: RetrievedContext) -> str:
    """
    Format the retrieved context into a string that can be injected into the agent prompt
    """
    if not retrieved_context.documents:
        return ""

    context_parts = ["Here is the relevant context for your response:"]
    for i, doc in enumerate(retrieved_context.documents):
        content = doc.get("content", "")
        metadata = doc.get("metadata", {})
        source = metadata.get("source", "Unknown source")
        context_parts.append(f"\nDocument {i+1} (Source: {source}):\n{content}\n")

    return "\n".join(context_parts)


async def retrieve_and_format_context(query: str, top_k: int = None) -> tuple[str, RetrievedContext]:
    """
    Retrieve context and format it for the agent in a single call
    Returns both the formatted context string and the original RetrievedContext object
    """
    retrieved_context = await retrieve_context(query, top_k)
    formatted_context = format_context_for_agent(retrieved_context)
    return formatted_context, retrieved_context