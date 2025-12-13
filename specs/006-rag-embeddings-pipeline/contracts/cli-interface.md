# CLI Interface Contract: RAG Embeddings Pipeline

**Feature**: 006-rag-embeddings-pipeline
**Date**: 2025-12-12
**Version**: 1.0.0

## Overview

This document defines the command-line interface contract for the RAG embeddings pipeline script (`backend/main.py`). The script extracts content from Docusaurus URLs, generates embeddings, and stores them in Qdrant.

---

## Command-Line Interface

### Basic Usage

```bash
# Activate virtual environment
cd backend
source .venv/bin/activate  # Linux/Mac
# or
.venv\Scripts\activate  # Windows

# Run pipeline
python main.py --urls-file urls.txt

# Run with custom configuration
python main.py --urls-file urls.txt --collection-name my-book --verbose
```

### Command-Line Arguments

| Argument | Type | Required | Default | Description |
|----------|------|----------|---------|-------------|
| `--urls-file` | `str` | Yes | - | Path to file containing URLs (one per line) |
| `--urls` | `str` | No | - | Comma-separated URLs (alternative to --urls-file) |
| `--collection-name` | `str` | No | `book_embeddings` | Qdrant collection name |
| `--verbose` | `flag` | No | False | Enable verbose logging |
| `--dry-run` | `flag` | No | False | Test without writing to Qdrant |
| `--force-reindex` | `flag` | No | False | Re-process all URLs (ignore content hash) |
| `--batch-size` | `int` | No | `96` | Cohere API batch size (max 96) |
| `--chunk-size` | `int` | No | `400` | Target tokens per chunk |
| `--chunk-overlap` | `int` | No | `50` | Token overlap between chunks |
| `--output-report` | `str` | No | - | Save processing report to JSON file |

### Examples

```bash
# Process URLs from file
python main.py --urls-file book-urls.txt

# Process specific URLs with verbose output
python main.py --urls "https://book.com/ch1,https://book.com/ch2" --verbose

# Dry run to test extraction
python main.py --urls-file urls.txt --dry-run

# Force re-indexing all content
python main.py --urls-file urls.txt --force-reindex

# Save processing report
python main.py --urls-file urls.txt --output-report report.json
```

---

## Input Formats

### URLs File Format

**File**: `urls.txt` (plain text, one URL per line)

```text
https://book.example.com/docs/intro
https://book.example.com/docs/chapter1
https://book.example.com/docs/chapter2
# Comments are ignored
https://book.example.com/docs/chapter3

# Blank lines are ignored
https://book.example.com/docs/chapter4
```

**Validation**:
- Lines starting with `#` are comments (ignored)
- Empty lines are ignored
- Each URL must be valid HTTP/HTTPS format
- Minimum 1 URL required

---

## Environment Variables

All sensitive configuration should be in `.env` file:

```bash
# Cohere Configuration (Required)
COHERE_API_KEY=your-cohere-api-key-here
COHERE_MODEL=embed-english-v3.0
COHERE_MAX_RETRIES=3

# Qdrant Configuration (Required)
QDRANT_URL=http://localhost:6333
QDRANT_API_KEY=  # Optional, leave empty for local Docker
QDRANT_COLLECTION_NAME=book_embeddings
QDRANT_VECTOR_SIZE=1024
QDRANT_DISTANCE_METRIC=cosine

# Pipeline Configuration (Optional - has defaults)
CHUNK_SIZE_TOKENS=400
CHUNK_OVERLAP_TOKENS=50
MIN_SIMILARITY_THRESHOLD=0.7
TOP_K_RESULTS=5
MAX_CONCURRENT_URLS=10

# Logging Configuration (Optional)
LOG_LEVEL=INFO  # DEBUG, INFO, WARNING, ERROR
LOG_FILE=pipeline.log  # Optional log file path
```

**Required Environment Variables**:
- `COHERE_API_KEY` - Cohere API authentication key
- `QDRANT_URL` - Qdrant instance URL

**Optional Environment Variables**:
- All others have sensible defaults

---

## Output Formats

### Console Output (Standard)

```
[INFO] 2025-12-12 10:00:00 - Starting RAG Embeddings Pipeline
[INFO] 2025-12-12 10:00:00 - Loaded 50 URLs from urls.txt
[INFO] 2025-12-12 10:00:01 - Qdrant collection 'book_embeddings' ready
[INFO] 2025-12-12 10:00:02 - Processing URL 1/50: https://book.com/ch1
[INFO] 2025-12-12 10:00:03 - Extracted 1247 words from https://book.com/ch1
[INFO] 2025-12-12 10:00:04 - Generated 15 chunks (avg 387 tokens/chunk)
[INFO] 2025-12-12 10:00:05 - Created 15 embeddings in 1 batch (234ms)
[INFO] 2025-12-12 10:00:06 - Stored 15 embeddings in Qdrant
[INFO] 2025-12-12 10:00:06 - Completed URL 1/50 in 4.2s
...
[INFO] 2025-12-12 10:08:34 - ✅ Pipeline completed successfully!
[INFO] 2025-12-12 10:08:34 - Processed: 50/50 URLs (100.0%)
[INFO] 2025-12-12 10:08:34 - Generated: 745 embeddings
[INFO] 2025-12-12 10:08:34 - Total time: 8m 34s
```

### Verbose Output

With `--verbose` flag, additional details are logged:

```
[DEBUG] 2025-12-12 10:00:02 - Fetching HTML from https://book.com/ch1
[DEBUG] 2025-12-12 10:00:03 - HTML parsed successfully (lxml parser)
[DEBUG] 2025-12-12 10:00:03 - Extracted main content using selector: article div.theme-doc-markdown
[DEBUG] 2025-12-12 10:00:03 - Removed navigation elements: nav, aside, footer
[DEBUG] 2025-12-12 10:00:04 - Chunking strategy: RecursiveCharacterTextSplitter
[DEBUG] 2025-12-12 10:00:04 - Chunk 0: 387 tokens (validated)
[DEBUG] 2025-12-12 10:00:04 - Chunk 1: 412 tokens (validated)
...
[DEBUG] 2025-12-12 10:00:05 - Cohere API call: 15 texts, batch_id=abc123
[DEBUG] 2025-12-12 10:00:05 - Cohere response: 15 embeddings, 234ms latency
[DEBUG] 2025-12-12 10:00:06 - Qdrant upsert: 15 points to collection 'book_embeddings'
```

### JSON Report Output

With `--output-report report.json`, a structured report is saved:

```json
{
  "job_id": "770e8400-e29b-41d4-a716-446655440002",
  "start_time": "2025-12-12T10:00:00Z",
  "end_time": "2025-12-12T10:08:34Z",
  "status": "completed",
  "summary": {
    "urls_requested": 50,
    "urls_processed": 48,
    "urls_failed": 2,
    "success_rate": 0.96,
    "documents_extracted": 48,
    "chunks_generated": 745,
    "embeddings_generated": 745,
    "embeddings_stored": 745,
    "processing_time_seconds": 514.2,
    "average_tokens_per_chunk": 387.3
  },
  "metrics": {
    "extraction_success_rate": 0.96,
    "chunks_in_target_range_pct": 0.97,
    "chunks_over_limit_pct": 0.0,
    "average_extraction_time_ms": 1234,
    "average_embedding_time_ms": 234,
    "average_storage_time_ms": 45
  },
  "errors": [
    {
      "url": "https://book.com/missing-page",
      "stage": "extraction",
      "error_type": "HTTPError",
      "error_message": "404 Not Found",
      "timestamp": "2025-12-12T10:02:15Z",
      "retry_count": 3
    },
    {
      "url": "https://book.com/timeout-page",
      "stage": "extraction",
      "error_type": "Timeout",
      "error_message": "Request timeout after 30s",
      "timestamp": "2025-12-12T10:05:42Z",
      "retry_count": 3
    }
  ],
  "warnings": [
    {
      "url": "https://book.com/large-page",
      "message": "Content very large (5000 words), generated 52 chunks"
    }
  ]
}
```

---

## Exit Codes

| Code | Status | Description |
|------|--------|-------------|
| `0` | Success | All URLs processed successfully |
| `1` | Partial Success | Some URLs processed, some failed (check report) |
| `2` | Configuration Error | Missing required environment variables or invalid config |
| `3` | Connection Error | Cannot connect to Qdrant or Cohere API |
| `4` | Input Error | Invalid URL file or malformed URLs |
| `5` | Processing Error | Critical error during processing (unrecoverable) |

### Exit Code Usage

```bash
# Check exit code in shell script
python main.py --urls-file urls.txt
EXIT_CODE=$?

if [ $EXIT_CODE -eq 0 ]; then
    echo "✅ Success!"
elif [ $EXIT_CODE -eq 1 ]; then
    echo "⚠️ Partial success - check logs"
else
    echo "❌ Failed with code $EXIT_CODE"
    exit 1
fi
```

---

## Error Messages

### Configuration Errors

```
[ERROR] Missing required environment variable: COHERE_API_KEY
Please set COHERE_API_KEY in .env file or environment.
Exit code: 2
```

```
[ERROR] Cannot connect to Qdrant at http://localhost:6333
Please ensure Qdrant is running: docker run -p 6333:6333 qdrant/qdrant
Exit code: 3
```

### Input Errors

```
[ERROR] URLs file not found: urls.txt
Please provide a valid file path with --urls-file
Exit code: 4
```

```
[ERROR] No valid URLs found in urls.txt
Ensure file contains at least one valid HTTP/HTTPS URL
Exit code: 4
```

### Processing Errors

```
[ERROR] Cohere API authentication failed: Invalid API key
Please check COHERE_API_KEY in .env file
Exit code: 3
```

```
[ERROR] Rate limit exceeded (429 Too Many Requests)
Consider upgrading to Production tier or reducing batch size
Exit code: 5
```

---

## Validation Rules

### URL Validation

```python
# Valid URLs
✅ https://book.example.com/docs/intro
✅ http://localhost:3000/docs/chapter1
✅ https://book.example.com/docs/page?version=1.0

# Invalid URLs
❌ book.example.com/docs  # Missing protocol
❌ ftp://book.example.com  # Invalid protocol (only HTTP/HTTPS)
❌ https://  # Incomplete URL
❌ javascript:alert('xss')  # Security risk
```

### Argument Validation

```python
# Chunk size validation
✅ --chunk-size 400  # Within range
❌ --chunk-size 50   # Too small (min 100)
❌ --chunk-size 600  # Too large (max 512)

# Batch size validation
✅ --batch-size 96   # Max allowed
❌ --batch-size 100  # Exceeds Cohere limit

# Overlap validation
✅ --chunk-overlap 50  # Reasonable
❌ --chunk-overlap 450 # Exceeds chunk size
```

---

## Integration Examples

### Shell Script Integration

```bash
#!/bin/bash
# process-book.sh

set -e  # Exit on error

echo "Starting RAG pipeline..."

# Load environment
source .venv/bin/activate

# Run pipeline with error handling
if python main.py \
    --urls-file book-urls.txt \
    --output-report "reports/$(date +%Y%m%d_%H%M%S).json" \
    --verbose; then
    echo "✅ Pipeline completed successfully"
else
    EXIT_CODE=$?
    echo "❌ Pipeline failed with code $EXIT_CODE"
    exit $EXIT_CODE
fi

# Optional: Verify embeddings count
python -c "
from qdrant_client import QdrantClient
client = QdrantClient(url='http://localhost:6333')
count = client.count('book_embeddings')
print(f'Total embeddings: {count.count}')
"
```

### Python Integration

```python
# external_script.py
import subprocess
import json
from pathlib import Path

def run_embeddings_pipeline(url_file: str, output_dir: str) -> dict:
    """Run embeddings pipeline and return results."""

    report_file = Path(output_dir) / "pipeline_report.json"

    # Run pipeline
    result = subprocess.run(
        [
            "python", "backend/main.py",
            "--urls-file", url_file,
            "--output-report", str(report_file),
            "--verbose"
        ],
        capture_output=True,
        text=True
    )

    # Check exit code
    if result.returncode not in [0, 1]:
        raise RuntimeError(f"Pipeline failed: {result.stderr}")

    # Load report
    with open(report_file) as f:
        report = json.load(f)

    return {
        "success": result.returncode == 0,
        "report": report,
        "stdout": result.stdout,
        "stderr": result.stderr
    }

# Usage
results = run_embeddings_pipeline("urls.txt", "reports/")
print(f"Processed {results['report']['summary']['urls_processed']} URLs")
```

---

## Testing

### Manual Testing

```bash
# Test with dry run (no Qdrant writes)
python main.py --urls "https://docusaurus.io/docs" --dry-run --verbose

# Test single URL
python main.py --urls "https://docusaurus.io/docs" --verbose

# Test with small batch
echo "https://docusaurus.io/docs" > test-urls.txt
python main.py --urls-file test-urls.txt --collection-name test_collection
```

### Automated Testing

```bash
# Unit tests
pytest backend/tests/test_extraction.py
pytest backend/tests/test_embeddings.py
pytest backend/tests/test_storage.py

# Integration test
pytest backend/tests/test_integration.py -v
```

---

## Performance Expectations

Based on spec requirements (SC-004):

| Metric | Target | Measurement |
|--------|--------|-------------|
| **Processing time** | <10 min for 50-page book | Monitor `processing_time_seconds` |
| **Success rate** | ≥95% URLs processed | Check `summary.success_rate` |
| **Chunk quality** | 95% chunks in 100-500 token range | Check `metrics.chunks_in_target_range_pct` |
| **Concurrent URLs** | ≥10 URLs simultaneously | N/A (single-threaded for simplicity) |

---

## Monitoring

### Log Files

```bash
# Default log location
backend/pipeline.log

# Custom log location (via environment)
LOG_FILE=logs/pipeline_$(date +%Y%m%d).log python main.py --urls-file urls.txt
```

### Metrics to Track

1. **Extraction Metrics**:
   - URLs processed per second
   - Average extraction time per URL
   - Extraction success rate

2. **Embedding Metrics**:
   - Embeddings generated per second
   - Average API latency
   - Batch efficiency (texts per request)

3. **Storage Metrics**:
   - Qdrant upsert time
   - Storage success rate
   - Total embeddings in collection

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2025-12-12 | Initial CLI interface specification |

---

## References

- Data Model: `specs/006-rag-embeddings-pipeline/data-model.md`
- Feature Spec: `specs/006-rag-embeddings-pipeline/spec.md`
- Quickstart Guide: `specs/006-rag-embeddings-pipeline/quickstart.md`
