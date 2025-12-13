# RAG Embeddings Pipeline

Automated pipeline for extracting content from Docusaurus book URLs, generating embeddings using Cohere, and storing them in Qdrant vector database.

## Quick Start

See [`specs/006-rag-embeddings-pipeline/quickstart.md`](../specs/006-rag-embeddings-pipeline/quickstart.md) for detailed setup instructions.

## Prerequisites

- Python 3.11+
- Docker (for Qdrant)
- Cohere API key

## Installation

```bash
# Install UV package manager (if not already installed)
# Windows:
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
# Linux/macOS:
curl -LsSf https://astral.sh/uv/install.sh | sh

# Create virtual environment
cd backend
uv venv

# Activate virtual environment
# Windows:
.venv\Scripts\activate
# Linux/Mac:
source .venv/bin/activate

# Install dependencies
uv sync
```

## Configuration

1. Start Qdrant:
```bash
docker run -d -p 6333:6333 -p 6334:6334 \
    -v qdrant_storage:/qdrant/storage:z \
    --name qdrant \
    qdrant/qdrant
```

2. Create `.env` file (copy from `.env.example`):
```bash
cp .env.example .env
```

3. Edit `.env` and add your Cohere API key

4. Create `urls.txt` with your book URLs (one per line)

## Usage

```bash
# Basic usage
python main.py --urls-file urls.txt

# With verbose output
python main.py --urls-file urls.txt --verbose

# Dry run (test without writing to Qdrant)
python main.py --urls-file urls.txt --dry-run

# Generate JSON report
python main.py --urls-file urls.txt --output-report report.json

# Direct URLs (no file)
python main.py --urls "https://book.com/ch1,https://book.com/ch2"
```

## CLI Options

- `--urls-file`: Path to file containing URLs (one per line)
- `--urls`: Comma-separated URLs (alternative to --urls-file)
- `--collection-name`: Qdrant collection name (default: book_embeddings)
- `--verbose`: Enable debug logging
- `--dry-run`: Test without writing to Qdrant
- `--force-reindex`: Re-process all URLs (ignore content hash)
- `--batch-size`: Cohere API batch size (default: 96, max: 96)
- `--chunk-size`: Target tokens per chunk (default: 400, range: 100-512)
- `--chunk-overlap`: Token overlap between chunks (default: 50)
- `--output-report`: Save processing report to JSON file

## Architecture

1. **Content Extraction**: Fetch HTML → Parse with BeautifulSoup → Extract text
2. **Text Chunking**: Tokenize → Split with LangChain (400 tokens, 50 overlap)
3. **Embedding Generation**: Batch process (96 chunks) → Cohere API → 1024-dim vectors
4. **Vector Storage**: Store in Qdrant with metadata (URL, title, chunk info)

## Exit Codes

- `0`: Success (all URLs processed)
- `1`: Partial success (some URLs failed)
- `2`: Configuration error (missing env vars)
- `3`: Connection error (Qdrant/Cohere unavailable)
- `4`: Input error (invalid URLs file)
- `5`: Processing error (critical failure)

## Troubleshooting

See [`specs/006-rag-embeddings-pipeline/quickstart.md#troubleshooting`](../specs/006-rag-embeddings-pipeline/quickstart.md#troubleshooting) for common issues and solutions.

## Development

```bash
# Run tests
pytest

# Install dev dependencies
uv sync --dev
```

## Documentation

- **Feature Specification**: `specs/006-rag-embeddings-pipeline/spec.md`
- **Implementation Plan**: `specs/006-rag-embeddings-pipeline/plan.md`
- **Data Model**: `specs/006-rag-embeddings-pipeline/data-model.md`
- **CLI Interface Contract**: `specs/006-rag-embeddings-pipeline/contracts/cli-interface.md`
- **Quick Start Guide**: `specs/006-rag-embeddings-pipeline/quickstart.md`
