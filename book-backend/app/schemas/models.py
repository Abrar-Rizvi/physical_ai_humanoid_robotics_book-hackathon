# book-backend/app/schemas/models.py
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
from datetime import datetime

# --- Data Models for Book Content ---

class BookContentChunk(BaseModel):
    id: str
    text: str
    source_url: str
    chapter_title: str
    position: str

class Embedding(BaseModel):
    id: str
    vector: List[float]
    chunk_id: str
    model_used: Optional[str] = None

# --- Data Models for Chatbot Interaction ---

class UserQuery(BaseModel):
    id: str
    text: str
    timestamp: datetime
    user_session_id: str
    context_text_selected: Optional[str] = None

class RetrievedChunk(BaseModel):
    chunk_id: str
    text: str
    source_url: str
    score: Optional[float] = None

class ChatbotResponse(BaseModel):
    id: str
    query_id: str
    text: str
    timestamp: datetime
    retrieved_chunk_ids: List[str]
    llm_model_used: Optional[str] = None
    confidence_score: Optional[float] = None