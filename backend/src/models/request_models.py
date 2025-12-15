from pydantic import BaseModel, Field
from typing import Optional, Dict, Any


class QueryRequest(BaseModel):
    """Represents a user query sent to the AI agent"""
    query: str = Field(..., description="The user's query text", min_length=1)
    parameters: Optional[Dict[str, Any]] = Field(
        default=None,
        description="Additional parameters for the query"
    )

    class Config:
        json_schema_extra = {
            "example": {
                "query": "What are the key principles of humanoid robotics?",
                "parameters": {
                    "temperature": 0.7,
                    "max_tokens": 500,
                    "top_k": 5
                }
            }
        }