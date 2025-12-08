# book-backend/app/api/query.py
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
from book_backend.app.db.qdrant import search_vectors
from book_backend.app.api.embeddings import EmbedRequest, embed_content # Reuse embedding logic
from book_backend.app.schemas.models import RetrievedChunk

router = APIRouter()

class QueryRequest(BaseModel):
    user_query: str
    context_text_selected: Optional[str] = None

class QueryResponse(BaseModel):
    retrieved_chunks: List[RetrievedChunk]

@router.post("/query", response_model=QueryResponse)
async def query_content(request: QueryRequest):
    """
    Queries Qdrant for relevant book content based on the user's query.
    """
    try:
        # 1. Embed the user's query
        combined_query_text = request.user_query
        if request.context_text_selected:
            combined_query_text = f"{request.context_text_selected} {request.user_query}"
        
        # This calls the internal embed_content function, not the API endpoint
        # You'd need a way to get the embedding model without an HTTP call
        # For simulation, we'll call the API directly or mock the embedding
        
        # Simulate embedding the user query
        # In a real app, you'd use OpenAI client directly or a dedicated embedding service
        simulated_embed_response = await embed_content(
            EmbedRequest(
                text=combined_query_text,
                source_url="user_query",
                chapter_title="user_query",
                position="user_query"
            )
        )
        query_vector = simulated_embed_response.embedding

        # 2. Search Qdrant
        search_results = await search_vectors(
            query_vector=query_vector,
            limit=5 # Limit to 5 most relevant chunks
        )

        retrieved_chunks = []
        for hit in search_results:
            # Assuming payload contains 'text' and 'source_url'
            retrieved_chunks.append(RetrievedChunk(
                chunk_id=str(hit.id), # Qdrant hit.id can be int or str
                text=hit.payload.get("text", ""),
                source_url=hit.payload.get("source_url", ""),
                score=hit.score
            ))

        return QueryResponse(retrieved_chunks=retrieved_chunks)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Query failed: {str(e)}")
