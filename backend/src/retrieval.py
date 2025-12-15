import asyncio
import logging
from typing import List, Dict, Any, Optional
from qdrant_client.http import models
from .clients.qdrant_client import qdrant_client
from .utils.embeddings import get_embedding
from .config import settings
from .models.response_models import RetrievedContext

# Configure logging
logger = logging.getLogger(__name__)


def retrieve_context(query: str, top_k: int = None) -> RetrievedContext:
    """
    Retrieve relevant context from Qdrant based on the query
    """
    if top_k is None:
        top_k = settings.top_k_results

    try:
        logger.info(f"Retrieving context for query: {query[:100]}...")

        # Get embedding for the query
        query_embedding = get_embedding(query)
        logger.info(f"Generated embedding with {len(query_embedding) if query_embedding else 0} dimensions")

        # Query Qdrant for similar vectors using the newer API
        # Use a more permissive threshold for initial search, then filter results afterward
        search_results = qdrant_client.query_points(
            collection_name=settings.qdrant_collection_name,
            query=query_embedding,
            limit=top_k,
            with_payload=True,
            score_threshold=0.1  # Lower threshold to ensure we get results, then filter afterward
        )
        logger.info(f"Qdrant search completed, found {len(search_results.points)} results")

        # Format the results - query_points returns a different structure
        # The results are in search_results.points for the new API
        documents = []
        for result in search_results.points:  # Changed from search_results to search_results.points
            document = {
                "id": result.id,
                "content": result.payload.get("text", "") if result.payload else "",  # Changed from "content" to "text"
                "metadata": result.payload.get("metadata", {}) if result.payload else {},
                "score": result.score
            }
            documents.append(document)

        logger.info(f"Formatted {len(documents)} documents from search results")

        # Create RetrievedContext object
        retrieved_context = RetrievedContext(
            documents=documents,
            query_embedding=query_embedding,
            retrieval_method="semantic_search"
        )

        return retrieved_context
    except Exception as e:
        logger.error(f"Error retrieving context from Qdrant: {str(e)}")
        # Return an empty RetrievedContext instead of raising to allow graceful handling in agent
        return RetrievedContext(
            documents=[],
            query_embedding=None,
            retrieval_method="semantic_search"
        )


def format_context_for_agent(retrieved_context: RetrievedContext) -> str:
    """
    Format the retrieved context into a string that can be injected into the agent prompt
    """
    if not retrieved_context or not retrieved_context.documents:
        logger.warning("No documents to format for context")
        return ""

    try:
        context_parts = ["Here is the relevant context for your response:"]
        for i, doc in enumerate(retrieved_context.documents):
            content = doc.get("content", "")
            metadata = doc.get("metadata", {})
            source = metadata.get("source", "Unknown source") or metadata.get("page_title", "Unknown source")  # Use page_title as fallback
            context_parts.append(f"\nDocument {i+1} (Source: {source}):\n{content}\n")

        formatted_context = "\n".join(context_parts)
        logger.info(f"Formatted context with {len(retrieved_context.documents)} documents, {len(formatted_context)} characters")
        return formatted_context
    except Exception as e:
        logger.error(f"Error formatting context: {str(e)}")
        return ""


def retrieve_and_format_context(query: str, top_k: int = None) -> tuple[str, RetrievedContext]:
    """
    Retrieve context and format it for the agent in a single call
    Returns both the formatted context string and the original RetrievedContext object
    """
    try:
        logger.info(f"Starting retrieve_and_format_context for query: {query[:100]}...")
        retrieved_context = retrieve_context(query, top_k)
        formatted_context = format_context_for_agent(retrieved_context)
        logger.info(f"Completed retrieve_and_format_context, formatted context length: {len(formatted_context)}")
        return formatted_context, retrieved_context
    except Exception as e:
        logger.error(f"Error in retrieve_and_format_context: {str(e)}")
        # Return empty context and empty retrieved_context to allow graceful handling
        empty_context = RetrievedContext(
            documents=[],
            query_embedding=None,
            retrieval_method="semantic_search"
        )
        return "", empty_context