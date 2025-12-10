# book-backend/app/models/schemas.py

from pydantic import BaseModel, Field, field_validator
from typing import Optional

class PageContext(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    pathname: str = Field(..., min_length=1, max_length=200)
    section: Optional[str] = Field(None, max_length=100)

    @field_validator('pathname')
    @classmethod
    def pathname_must_start_with_slash(cls, v: str) -> str:
        if not v.startswith('/'):
            raise ValueError('pathname must start with /')
        return v

class ChatRequest(BaseModel):
    user_query: str = Field(..., min_length=1, max_length=500)
    page_context: PageContext
    session_id: Optional[str] = Field(None, pattern=r'^[a-f0-9\-]{36}$')

    @field_validator('user_query')
    @classmethod
    def sanitize_query(cls, v: str) -> str:
        # Strip HTML tags and trim whitespace
        import re
        clean = re.sub(r'<[^>]+>', '', v).strip()
        if not clean:
            raise ValueError('user_query cannot be empty after sanitization')
        return clean

class Source(BaseModel):
    title: str = Field(..., min_length=1, max_length=100)
    url: str = Field(..., min_length=1, max_length=200)

class ResponseMetadata(BaseModel):
    processing_time_ms: Optional[int] = Field(None, ge=0)
    model_used: Optional[str] = None
    tokens_used: Optional[int] = Field(None, ge=0)

class ChatResponse(BaseModel):
    response_text: str = Field(..., min_length=1, max_length=4000)
    sources: list[Source] = Field(default_factory=list, max_length=5)
    metadata: Optional[ResponseMetadata] = None
