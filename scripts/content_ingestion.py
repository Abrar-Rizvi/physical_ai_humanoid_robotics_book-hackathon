# scripts/content_ingestion.py
import os
import requests
import frontmatter # You'd need to install python-frontmatter
import uuid
from pathlib import Path
from typing import List, Dict, Any

# Configuration
DOCUSAURUS_DOCS_PATH = "./robotic-book/docs"
BACKEND_EMBED_URL = "http://localhost:8000/api/v1/embed"
BACKEND_STORE_URL = "http://localhost:8000/api/v1/store"

def get_docusaurus_markdown_files(path: str) -> List[Path]:
    """
    Recursively finds all markdown and mdx files in the Docusaurus docs path.
    """
    markdown_files = []
    for root, _, files in os.walk(path):
        for file in files:
            if file.endswith((".md", ".mdx")):
                markdown_files.append(Path(root) / file)
    return markdown_files

def chunk_content(file_path: Path, content: str, metadata: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    Simple placeholder for chunking logic.
    In a real scenario, this would involve more sophisticated text splitting.
    """
    # For now, treat the whole file as one chunk
    chunk_id = str(uuid.uuid4())
    return [{
        "id": chunk_id,
        "text": content,
        "source_url": f"/docs/{file_path.relative_to(DOCUSAURUS_DOCS_PATH).with_suffix('')}",
        "chapter_title": metadata.get("title", file_path.stem),
        "position": "full_document" # Placeholder
    }]

async def process_document(file_path: Path):
    """
    Reads a Docusaurus markdown file, chunks its content, generates embeddings,
    and stores them in the backend.
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        post = frontmatter.load(f) # Parses markdown with frontmatter
        content = post.content
        metadata = post.metadata # Includes title, sidebar_position etc.

    print(f"Processing {file_path}...")

    chunks = chunk_content(file_path, content, metadata)

    for chunk in chunks:
        # 1. Generate Embedding
        embed_payload = {
            "text": chunk["text"],
            "source_url": chunk["source_url"],
            "chapter_title": chunk["chapter_title"],
            "position": chunk["position"]
        }
        try:
            embed_response = requests.post(BACKEND_EMBED_URL, json=embed_payload)
            embed_response.raise_for_status()
            embedding_data = embed_response.json()
            embedding_vector = embedding_data["embedding"]
            chunk_id = embedding_data["chunk_id"] # Use chunk_id returned from backend
        except requests.exceptions.RequestException as e:
            print(f"Error embedding chunk from {file_path}: {e}")
            continue

        # 2. Store Embedding
        store_payload = {
            "chunk_id": chunk_id,
            "embedding": embedding_vector,
            "metadata": {
                "source_url": chunk["source_url"],
                "chapter_title": chunk["chapter_title"],
                "position": chunk["position"]
            }
        }
        try:
            store_response = requests.post(BACKEND_STORE_URL, json=store_payload)
            store_response.raise_for_status()
            print(f"Stored embedding for {chunk_id} from {file_path}")
        except requests.exceptions.RequestException as e:
            print(f"Error storing embedding for {chunk_id} from {file_path}: {e}")
            continue

async def main():
    markdown_files = get_docusaurus_markdown_files(DOCUSAURUS_DOCS_PATH)
    for file_path in markdown_files:
        await process_document(file_path)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
