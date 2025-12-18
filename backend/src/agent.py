import asyncio
import uuid
import logging
import traceback
from datetime import datetime
from typing import Dict, Any, Optional
from .models.request_models import QueryRequest
from .models.response_models import Response as ResponseModel
from .retrieval import retrieve_and_format_context
from .clients.openai_client import openai_client
from .config import settings
from .utils.embeddings import get_embedding

# Configure logging
logger = logging.getLogger(__name__)


async def process_query_with_agent(request: QueryRequest) -> ResponseModel:
    """
    Process a user query using the RAG agent with OpenAI and retrieved context
    """
    query_id = str(uuid.uuid4())
    timestamp = datetime.utcnow().isoformat() + "Z"

    try:
        logger.info(f"Processing query: {request.query[:100]}...")  # Log query for debugging

        # Retrieve relevant context from Qdrant
        logger.info("Step 1: Retrieving context from Qdrant...")
        formatted_context, retrieved_context = retrieve_and_format_context(
            request.query,
            request.parameters.get("top_k") if request.parameters else None
        )
        logger.info(f"Step 1 complete: Retrieved {len(retrieved_context.documents) if retrieved_context else 0} documents")

        # Check if we have any relevant context
        if not formatted_context or not formatted_context.strip():
            logger.warning("No relevant context found in Qdrant")
            # No context found, return appropriate response
            return ResponseModel(
                answer="I couldn't find any relevant information in the knowledge base to answer your query.",
                sources=[],
                query_id=query_id,
                timestamp=timestamp,
                status="no_context"
            )

        # Prepare the system message with grounding instructions
        system_message = f"""You are a helpful assistant for the Physical AI and Humanoid Robotics book. Only respond based on the book content provided below. If the provided context contains relevant information, use it to answer the user's query. If the context doesn't contain information about the query, respond politely with: "I don't have information about this topic in the book. Please refer to the relevant chapters for detailed information." Do not use any external knowledge or general information.

{formatted_context}"""

        # Prepare the user message
        user_message = f"Based on the provided context, please answer the following query: {request.query}"

        # Get temperature from parameters or use default
        temperature = 0.3  # Conservative temperature for factual responses
        if request.parameters and "temperature" in request.parameters:
            temperature = request.parameters["temperature"]

        logger.info(f"Step 2: Calling OpenAI API with model gpt-4-turbo, temperature={temperature}...")

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
        logger.info("Step 2 complete: OpenAI API call successful")

        # Extract the answer from the response
        answer = response.choices[0].message.content
        logger.info(f"Step 3: Extracted answer with {len(answer) if answer else 0} characters")

        # Create source attribution from retrieved context
        sources = []
        if retrieved_context and retrieved_context.documents:
            for doc in retrieved_context.documents:
                # Use a lower threshold for source attribution to include more results
                # since the initial query already used a permissive threshold
                if doc.get("score", 0) > 0.3:  # Lower threshold for source attribution
                    source = {
                        "id": doc.get("id", ""),
                        "content_snippet": doc.get("content", "")[:200] + "..." if len(doc.get("content", "")) > 200 else doc.get("content", ""),
                        "confidence": doc.get("score", 0.0)
                    }
                    sources.append(source)
        else:
            logger.warning("No documents found in retrieved_context for source attribution")

        logger.info(f"Step 4: Created {len(sources)} sources for attribution")

        # Return the response
        result = ResponseModel(
            answer=answer,
            sources=sources,
            query_id=query_id,
            timestamp=timestamp,
            status="success"
        )
        logger.info(f"Query {query_id} processed successfully")
        return result

    except Exception as e:
        # Enhanced error logging with full traceback
        error_msg = f"Error processing query: {str(e)}"
        error_traceback = traceback.format_exc()
        logger.error(f"{error_msg}\nFull traceback:\n{error_traceback}")

        # Handle any errors in the process with detailed logging
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