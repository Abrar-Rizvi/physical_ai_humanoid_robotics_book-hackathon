from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime


class RetrievedContext(BaseModel):
    """Represents the relevant document fragments retrieved from the vector database"""
    documents: List[Dict[str, Any]] = Field(
        ...,
        description="Retrieved document fragments with metadata"
    )
    query_embedding: Optional[List[float]] = Field(
        default=None,
        description="Vector representation of the query"
    )
    retrieval_method: Optional[str] = Field(
        default=None,
        description="Method used for retrieval"
    )

    class Config:
        json_schema_extra = {
            "example": {
                "documents": [
                    {
                        "id": "doc-123",
                        "content": "Humanoid robotics focuses on creating robots with human-like form and behavior...",
                        "metadata": {
                            "source": "humanoid_robots_chapter1.md",
                            "title": "Introduction to Humanoid Robotics",
                            "url": "https://example.com/docs/humanoid_robots"
                        },
                        "score": 0.85
                    }
                ],
                "query_embedding": [0.1, 0.3, 0.5, 0.2],
                "retrieval_method": "semantic_search"
            }
        }


class Response(BaseModel):
    """Contains the AI-generated answer along with metadata including source attribution and confidence indicators"""
    answer: str = Field(..., description="The AI-generated response")
    sources: List[Dict[str, Any]] = Field(
        ...,
        description="Source attribution for the response"
    )
    query_id: Optional[str] = Field(
        default=None,
        description="Unique identifier for the query"
    )
    timestamp: str = Field(
        ...,
        description="ISO 8601 timestamp of response generation"
    )
    status: str = Field(
        ...,
        description="Response status",
        pattern="^(success|no_context|error)$"
    )

    class Config:
        json_schema_extra = {
            "example": {
                "answer": "The key principles of humanoid robotics include anthropomorphic design, bipedal locomotion, and human-like interaction capabilities...",
                "sources": [
                    {
                        "id": "doc-123",
                        "content_snippet": "Humanoid robotics focuses on creating robots with human-like form and behavior...",
                        "confidence": 0.95
                    }
                ],
                "query_id": "query-456",
                "timestamp": "2025-12-15T10:30:05Z",
                "status": "success"
            }
        }


class HealthStatus(BaseModel):
    """Contains system health information including service availability and performance metrics"""
    status: str = Field(
        ...,
        description="Overall service status",
        pattern="^(healthy|degraded|unhealthy)$"
    )
    timestamp: str = Field(
        ...,
        description="ISO 8601 timestamp of status check"
    )
    services: Optional[Dict[str, str]] = Field(
        default=None,
        description="Status of individual services"
    )
    metrics: Optional[Dict[str, Any]] = Field(
        default=None,
        description="Performance metrics"
    )

    class Config:
        json_schema_extra = {
            "example": {
                "status": "healthy",
                "timestamp": "2025-12-15T10:30:00Z",
                "services": {
                    "qdrant": "connected",
                    "openai": "connected"
                },
                "metrics": {
                    "response_time_ms": 150,
                    "uptime_seconds": 3600
                }
            }
        }