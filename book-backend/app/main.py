from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from book_backend.app.api import embeddings
from book_backend.app.api import store
from book_backend.app.api import query
from book_backend.app.api import chat
import os

app = FastAPI(title="Course AI Backend", version="1.0.0")

# CORS Configuration for Course AI Chat Widget
cors_origins = os.getenv("CORS_ORIGINS", "http://localhost:3000").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["Content-Type", "Authorization"],
    allow_credentials=False,
)

app.include_router(embeddings.router, prefix="/api/v1")
app.include_router(store.router, prefix="/api/v1")
app.include_router(query.router, prefix="/api/v1")
app.include_router(chat.router, prefix="/api/v1")

@app.get("/")
async def root():
    return {"message": "RAG Chatbot Backend is running!"}

@app.get("/health")
async def health_check():
    """Health check endpoint for Course AI Chat Widget"""
    return {
        "status": "healthy",
        "timestamp": int(__import__('time').time() * 1000),
        "services": {
            "api": "operational"
        }
    }
