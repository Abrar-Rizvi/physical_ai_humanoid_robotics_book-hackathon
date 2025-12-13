# Quickstart Guide: RAG Embeddings Pipeline

**Feature**: 006-rag-embeddings-pipeline
**Date**: 2025-12-12
**Version**: 1.0.0

## Overview

This guide will walk you through setting up and running the RAG embeddings pipeline to extract content from Docusaurus book URLs, generate embeddings using Cohere, and store them in Qdrant vector database.

**Time to complete**: ~15 minutes
**Prerequisites**: Python 3.11+, Docker (for Qdrant)

---

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Installation](#installation)
3. [Configuration](#configuration)
4. [First Run](#first-run)
5. [Verification](#verification)
6. [Next Steps](#next-steps)
7. [Troubleshooting](#troubleshooting)

---

## Prerequisites

### Required Software

- **Python 3.11+**: [Download from python.org](https://www.python.org/downloads/)
- **Docker**: [Install Docker Desktop](https://www.docker.com/products/docker-desktop/)
- **Cohere API Key**: [Sign up at cohere.com](https://cohere.com/)

### Verify Installation

```bash
# Check Python version
python --version  # Should be 3.11 or higher

# Check Docker
docker --version

# Check UV (will install in next step if missing)
uv --version
```

---

## Installation

### Step 1: Install UV Package Manager

UV is a fast Python package manager and virtual environment tool.

**Windows (PowerShell)**:
```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

**Linux/macOS**:
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Verify installation:
```bash
uv --version
```

### Step 2: Create Backend Directory

```bash
# Navigate to project root
cd D:\Quarter 4\ai-book\humanoid-robotic-book

# Create backend directory
mkdir backend
cd backend
```

### Step 3: Initialize Python Project with UV

```bash
# Initialize UV project
uv init --name rag-pipeline --python 3.11

# Create virtual environment
uv venv

# Activate virtual environment
# Windows:
.venv\Scripts\activate
# Linux/Mac:
source .venv/bin/activate
```

### Step 4: Install Dependencies

```bash
# Add dependencies using UV
uv add beautifulsoup4 lxml cohere qdrant-client requests python-dotenv langchain tiktoken

# Development dependencies
uv add --dev pytest pytest-asyncio
```

**Dependencies installed**:
- `beautifulsoup4` + `lxml`: HTML parsing and content extraction
- `cohere`: Embedding generation API
- `qdrant-client`: Vector database client
- `requests`: HTTP client for URL fetching
- `python-dotenv`: Environment variable management
- `langchain`: Text chunking utilities
- `tiktoken`: Token counting for OpenAI/Cohere models
- `pytest`: Testing framework

---

## Configuration

### Step 1: Start Qdrant Vector Database

Using Docker (recommended for development):

```bash
# Pull and run Qdrant in Docker
docker run -d -p 6333:6333 -p 6334:6334 \
    -v qdrant_storage:/qdrant/storage:z \
    --name qdrant \
    qdrant/qdrant
```

**Verify Qdrant is running**:
```bash
# Check container status
docker ps | grep qdrant

# Test Qdrant API (should return JSON)
curl http://localhost:6333
```

### Step 2: Get Cohere API Key

1. Go to [cohere.com/dashboard](https://dashboard.cohere.com/)
2. Sign up or log in
3. Navigate to **API Keys** section
4. Create a new API key or copy existing key
5. **Important**: Use **Production** tier for best performance (free tier has rate limits)

### Step 3: Create Environment File

Create `.env` file in `backend/` directory:

```bash
# Navigate to backend directory
cd backend

# Create .env file
```

**Contents of `.env`**:

```bash
# ===========================
# Cohere Configuration (Required)
# ===========================
COHERE_API_KEY=your-cohere-api-key-here
COHERE_MODEL=embed-english-v3.0
COHERE_MAX_RETRIES=3

# ===========================
# Qdrant Configuration (Required)
# ===========================
QDRANT_URL=http://localhost:6333
QDRANT_API_KEY=  # Leave empty for local Docker
QDRANT_COLLECTION_NAME=book_embeddings
QDRANT_VECTOR_SIZE=1024
QDRANT_DISTANCE_METRIC=cosine

# ===========================
# Pipeline Configuration (Optional - has defaults)
# ===========================
CHUNK_SIZE_TOKENS=400
CHUNK_OVERLAP_TOKENS=50
MIN_SIMILARITY_THRESHOLD=0.7
TOP_K_RESULTS=5
MAX_CONCURRENT_URLS=10

# ===========================
# Logging Configuration (Optional)
# ===========================
LOG_LEVEL=INFO  # DEBUG, INFO, WARNING, ERROR
LOG_FILE=pipeline.log
```

**⚠️ Important**: Replace `your-cohere-api-key-here` with your actual API key!

### Step 4: Create URLs File

Create `urls.txt` in `backend/` directory with book URLs (one per line):

```text
https://your-docusaurus-book.com/docs/intro
https://your-docusaurus-book.com/docs/chapter1
https://your-docusaurus-book.com/docs/chapter2
# Add more URLs as needed
```

**Example for testing** (using public Docusaurus sites):
```text
https://docusaurus.io/docs
https://docusaurus.io/docs/installation
https://docusaurus.io/docs/configuration
```

---

## First Run

### Step 1: Create main.py

The implementation will be in `backend/main.py` (to be created in implementation phase). For now, verify your setup is correct.

### Step 2: Verify Environment

```bash
# Activate virtual environment if not already active
# Windows:
.venv\Scripts\activate
# Linux/Mac:
source .venv/bin/activate

# Verify Python packages
uv pip list
```

You should see:
- `beautifulsoup4`
- `cohere`
- `qdrant-client`
- `requests`
- `python-dotenv`
- `langchain`
- `tiktoken`

### Step 3: Test Qdrant Connection

```bash
# Test Qdrant API
curl http://localhost:6333/collections
```

Expected response (initially empty):
```json
{
  "result": {
    "collections": []
  }
}
```

### Step 4: Test Cohere API

Create a test script `test_cohere.py`:

```python
import os
from dotenv import load_dotenv
import cohere

# Load environment variables
load_dotenv()

# Initialize Cohere client
co = cohere.Client(os.getenv("COHERE_API_KEY"))

# Test embedding generation
response = co.embed(
    texts=["This is a test sentence."],
    model="embed-english-v3.0",
    input_type="search_document"
)

print(f"✅ Cohere API working! Embedding dimension: {len(response.embeddings[0])}")
print(f"Expected dimension: 1024")
assert len(response.embeddings[0]) == 1024, "Dimension mismatch!"
```

Run the test:
```bash
python test_cohere.py
```

Expected output:
```
✅ Cohere API working! Embedding dimension: 1024
Expected dimension: 1024
```

---

## Verification

After implementation (Phase: Implementation), you'll be able to run:

```bash
# Run pipeline with dry-run (test without writing to Qdrant)
python main.py --urls-file urls.txt --dry-run --verbose

# Run actual pipeline
python main.py --urls-file urls.txt --verbose

# Check results in Qdrant
python -c "
from qdrant_client import QdrantClient
client = QdrantClient(url='http://localhost:6333')
collections = client.get_collections()
print(f'Collections: {collections}')

if collections.collections:
    count = client.count('book_embeddings')
    print(f'Total embeddings: {count.count}')
"
```

---

## Next Steps

### Implementation Phase (Feature 006 - Current)

1. **Implement `main.py`**: Single-file pipeline with all functionality
2. **Write tests**: Unit and integration tests for extraction, embeddings, storage
3. **Run pipeline**: Process book URLs and verify embeddings
4. **Validate retrieval**: Test semantic search queries

### Future Enhancements (Separate Features)

- **RAG Query API**: REST API for semantic search queries
- **Chatbot UI**: Frontend interface for asking questions
- **Incremental Updates**: Content change detection and re-indexing
- **Multi-language Support**: Handle non-English content

---

## Troubleshooting

### Issue: Qdrant not starting

**Symptoms**: `curl http://localhost:6333` fails

**Solutions**:
```bash
# Check if Docker is running
docker ps

# Check Qdrant container logs
docker logs qdrant

# Restart Qdrant
docker restart qdrant

# If port 6333 is in use, change port mapping:
docker run -d -p 6335:6333 -p 6336:6334 \
    -v qdrant_storage:/qdrant/storage:z \
    --name qdrant \
    qdrant/qdrant

# Update .env: QDRANT_URL=http://localhost:6335
```

### Issue: Cohere API authentication fails

**Symptoms**: `CohereAPIError: invalid api token`

**Solutions**:
1. Verify API key in `.env` file (no extra spaces)
2. Check API key is valid at [cohere.com/dashboard](https://dashboard.cohere.com/)
3. Ensure `.env` file is in `backend/` directory
4. Restart virtual environment after changing `.env`

### Issue: UV command not found

**Symptoms**: `bash: uv: command not found`

**Solutions**:
```bash
# Windows: Add UV to PATH manually
# Check UV installation location:
where uv

# Linux/Mac: Reload shell configuration
source ~/.bashrc  # or ~/.zshrc

# Re-install UV if needed (see Installation section)
```

### Issue: Python version too old

**Symptoms**: `Python 3.9 is installed, but 3.11+ is required`

**Solutions**:
1. Install Python 3.11+ from [python.org](https://www.python.org/downloads/)
2. Use `python3.11` command explicitly:
   ```bash
   uv venv --python 3.11
   ```

### Issue: Dependencies not installing

**Symptoms**: `uv add beautifulsoup4` fails

**Solutions**:
```bash
# Ensure virtual environment is activated
# Windows:
.venv\Scripts\activate
# Linux/Mac:
source .venv/bin/activate

# Try installing with pip fallback
uv pip install beautifulsoup4 lxml cohere qdrant-client requests python-dotenv langchain tiktoken

# Clear UV cache if corrupted
uv cache clean
```

### Issue: Rate limit errors from Cohere

**Symptoms**: `429 Too Many Requests`

**Solutions**:
1. Upgrade to **Production tier** at [cohere.com/pricing](https://cohere.com/pricing)
2. Reduce batch size: `--batch-size 50` (default is 96)
3. Add delays between API calls (implementation detail)
4. Check quota usage at [dashboard](https://dashboard.cohere.com/)

### Issue: BeautifulSoup can't parse HTML

**Symptoms**: `No parser was explicitly specified`

**Solutions**:
```bash
# Ensure lxml is installed (faster and more robust)
uv add lxml

# Alternative parsers (slower):
# - html.parser (built-in)
# - html5lib (install with: uv add html5lib)
```

### Issue: URLs file not found

**Symptoms**: `FileNotFoundError: urls.txt`

**Solutions**:
```bash
# Verify file exists
ls urls.txt

# Use absolute path
python main.py --urls-file "D:\Quarter 4\ai-book\humanoid-robotic-book\backend\urls.txt"

# Or create sample URLs file
echo "https://docusaurus.io/docs" > urls.txt
```

---

## File Structure Summary

After setup, your `backend/` directory should look like:

```text
backend/
├── .env                    # Environment variables (DO NOT COMMIT)
├── .venv/                  # Virtual environment (DO NOT COMMIT)
├── pyproject.toml          # UV project configuration
├── uv.lock                 # UV lock file
├── urls.txt                # Book URLs (one per line)
├── main.py                 # Pipeline implementation (to be created)
├── test_cohere.py          # Cohere API test script
└── tests/                  # Test directory
    ├── test_extraction.py  # (to be created)
    ├── test_embeddings.py  # (to be created)
    └── test_storage.py     # (to be created)
```

---

## Environment Variables Reference

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `COHERE_API_KEY` | ✅ Yes | - | Cohere API authentication key |
| `COHERE_MODEL` | No | `embed-english-v3.0` | Cohere embedding model |
| `COHERE_MAX_RETRIES` | No | `3` | Max retry attempts for API calls |
| `QDRANT_URL` | ✅ Yes | - | Qdrant instance URL |
| `QDRANT_API_KEY` | No | - | Qdrant API key (not needed for local) |
| `QDRANT_COLLECTION_NAME` | No | `book_embeddings` | Collection name in Qdrant |
| `QDRANT_VECTOR_SIZE` | No | `1024` | Embedding dimension |
| `QDRANT_DISTANCE_METRIC` | No | `cosine` | Distance metric (cosine, dot, euclidean) |
| `CHUNK_SIZE_TOKENS` | No | `400` | Target tokens per chunk |
| `CHUNK_OVERLAP_TOKENS` | No | `50` | Token overlap between chunks |
| `MIN_SIMILARITY_THRESHOLD` | No | `0.7` | Min similarity for retrieval |
| `TOP_K_RESULTS` | No | `5` | Number of results to return |
| `MAX_CONCURRENT_URLS` | No | `10` | Max parallel URL processing |
| `LOG_LEVEL` | No | `INFO` | Logging level |
| `LOG_FILE` | No | `pipeline.log` | Log file path |

---

## Performance Expectations

Based on research findings (see `research.md`):

| Metric | Target | Notes |
|--------|--------|-------|
| **Processing time** | <10 min for 50-page book | With Cohere Production tier |
| **Embedding generation** | ~4 seconds for 333 chunks | Using batch size 96 |
| **Storage** | ~4 MB per 50-page book | In Qdrant |
| **Cost** | ~$0.013 per 50-page book | Cohere embed-english-v3.0 |
| **Success rate** | ≥95% URLs processed | Per spec SC-001 |

---

## Architecture Overview

```
┌─────────────────┐
│  URLs File      │
│  (urls.txt)     │
└────────┬────────┘
         │
         ▼
┌─────────────────────────────────────────┐
│  1. Content Extraction                  │
│     - Fetch HTML (requests)             │
│     - Parse HTML (BeautifulSoup)        │
│     - Extract text (remove nav/footer)  │
└────────┬────────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────────┐
│  2. Text Chunking                       │
│     - Tokenize (tiktoken)               │
│     - Split (LangChain)                 │
│     - Target: 400 tokens, 50 overlap    │
└────────┬────────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────────┐
│  3. Embedding Generation                │
│     - Batch: 96 chunks per request      │
│     - API: Cohere embed-english-v3.0    │
│     - Dimension: 1024                   │
└────────┬────────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────────┐
│  4. Vector Storage                      │
│     - Store in Qdrant                   │
│     - Collection: book_embeddings       │
│     - Distance: Cosine similarity       │
│     - Payload: metadata (URL, title)    │
└─────────────────────────────────────────┘
```

---

## Support and Resources

- **Cohere Documentation**: [docs.cohere.com](https://docs.cohere.com/)
- **Qdrant Documentation**: [qdrant.tech/documentation](https://qdrant.tech/documentation/)
- **LangChain Text Splitters**: [python.langchain.com/docs/modules/data_connection/document_transformers](https://python.langchain.com/docs/modules/data_connection/document_transformers/)
- **UV Documentation**: [docs.astral.sh/uv](https://docs.astral.sh/uv/)

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2025-12-12 | Initial quickstart guide |

---

## Next: Implementation

Once setup is complete, proceed to implementation phase where `main.py` will be created with:
- URL collection and validation
- Content extraction with BeautifulSoup
- Text chunking with LangChain
- Embedding generation with Cohere
- Vector storage in Qdrant
- Retrieval validation

See `specs/006-rag-embeddings-pipeline/tasks.md` (to be generated by `/sp.tasks` command).
