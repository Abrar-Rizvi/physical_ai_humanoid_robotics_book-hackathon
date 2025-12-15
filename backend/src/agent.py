import asyncio
import uuid
from datetime import datetime
from typing import Dict, Any, Optional
from .models.request_models import QueryRequest
from .models.response_models import Response as ResponseModel
from .retrieval import retrieve_and_format_context
from .clients.openai_client import openai_client
from .config import settings
from .utils.embeddings import get_embedding


async def process_query_with_agent(request: QueryRequest) -> ResponseModel:
    """
    Process a user query using the RAG agent with OpenAI and retrieved context
    """
    query_id = str(uuid.uuid4())
    timestamp = datetime.utcnow().isoformat() + "Z"

    try:
        # Retrieve relevant context from Qdrant
        formatted_context, retrieved_context = await retrieve_and_format_context(
            request.query,
            request.parameters.get("top_k") if request.parameters else None
        )

        # Check if we have any relevant context
        if not formatted_context.strip():
            # No context found, return appropriate response
            return ResponseModel(
                answer="I couldn't find any relevant information in the knowledge base to answer your query.",
                sources=[],
                query_id=query_id,
                timestamp=timestamp,
                status="no_context"
            )

        # Prepare the system message with grounding instructions
        system_message = f"""You are a helpful assistant that only responds based on the context provided below. Do not use any prior knowledge or information not present in the provided context. If the context doesn't contain information to answer the query, respond with "I don't have sufficient context to answer this question."

{formatted_context}"""

        # Prepare the user message
        user_message = f"Based on the provided context, please answer the following query: {request.query}"

        # Get temperature from parameters or use default
        temperature = 0.3  # Conservative temperature for factual responses
        if request.parameters and "temperature" in request.parameters:
            temperature = request.parameters["temperature"]

        # Call OpenAI API to generate response
        response = openai_client.chat.completions.create(
            model="gpt-4-turbo",  # Using GPT-4 Turbo for better reasoning
            messages=[
                {"role": "system", "content": system_message},
                {"role": "user", "content": user_message}
            ],
            temperature=temperature,
            max_tokens=request.parameters.get("max_tokens", 1000) if request.parameters else 1000
        )

        # Extract the answer from the response
        answer = response.choices[0].message.content

        # Create source attribution from retrieved context
        sources = []
        for doc in retrieved_context.documents:
            if doc.get("score", 0) > settings.min_similarity_threshold:  # Only include relevant sources
                source = {
                    "id": doc.get("id", ""),
                    "content_snippet": doc.get("content", "")[:200] + "..." if len(doc.get("content", "")) > 200 else doc.get("content", ""),
                    "confidence": doc.get("score", 0.0)
                }
                sources.append(source)

        # Return the response
        return ResponseModel(
            answer=answer,
            sources=sources,
            query_id=query_id,
            timestamp=timestamp,
            status="success"
        )

    except Exception as e:
        # Handle any errors in the process
        return ResponseModel(
            answer="An error occurred while processing your query. Please try again later.",
            sources=[],
            query_id=query_id,
            timestamp=timestamp,
            status="error"
        )


async def create_rag_agent():
    """
    Create and configure the RAG agent with grounding constraints
    """
    # In this implementation, we're using the OpenAI API directly with system messages
    # to enforce grounding constraints rather than creating a separate assistant
    pass


async def query_agent(query: str, context: str = None) -> str:
    """
    Query the agent with optional context
    """
    system_message = "You are a helpful assistant. If context is provided, base your response only on that context."

    if context:
        system_message += f"\n\nContext: {context}"

    response = openai_client.chat.completions.create(
        model="gpt-4-turbo",
        messages=[
            {"role": "system", "content": system_message},
            {"role": "user", "content": query}
        ],
        temperature=0.3
    )

    return response.choices[0].message.content