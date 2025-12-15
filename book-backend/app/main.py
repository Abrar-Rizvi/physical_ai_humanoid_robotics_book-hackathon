from fastapi import FastAPI
from book_backend.app.api import embeddings
from book_backend.app.api import store
from book_backend.app.api import query
from book_backend.app.api import chat

app = FastAPI()

app.include_router(embeddings.router, prefix="/api/v1")
app.include_router(store.router, prefix="/api/v1")
app.include_router(query.router, prefix="/api/v1")
app.include_router(chat.router, prefix="/api/v1")

@app.get("/")
async def root():
    return {"message": "RAG Chatbot Backend is running!"}
