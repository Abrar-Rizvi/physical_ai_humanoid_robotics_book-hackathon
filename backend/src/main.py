from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import logging
import os
from datetime import datetime
from .models.request_models import QueryRequest
from .models.response_models import Response as ResponseModel, HealthStatus
from .config import settings

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application lifespan events
    """
    logger.info("Starting up RAG Agent Backend...")
    # Startup logic can go here
    yield
    # Shutdown logic can go here
    logger.info("Shutting down RAG Agent Backend...")


# Create FastAPI app
app = FastAPI(
    title="RAG Agent Backend",
    description="Backend API for RAG-powered AI Agent with OpenAI and Qdrant integration",
    version="0.1.0",
    lifespan=lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://physical-ai-humanoid-robotics-book-lime.vercel.app"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    """
    Root endpoint for basic health check
    """
    return {"message": "RAG Agent Backend is running"}


@app.get("/health", response_model=HealthStatus)
async def health_check():
    """
    Health check endpoint to monitor system status
    """
    from .health import get_health_status
    return await get_health_status()


@app.post("/query", response_model=ResponseModel)
async def query_endpoint(request: QueryRequest):
    """
    Query processing endpoint - accepts user queries and returns AI-generated responses
    """
    from .agent import process_query_with_agent
    try:
        response = await process_query_with_agent(request)
        return response
    except Exception as e:
        logger.error(f"Error processing query: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


# Include this to make the module importable
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)