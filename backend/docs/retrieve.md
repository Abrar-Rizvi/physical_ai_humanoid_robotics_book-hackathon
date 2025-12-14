# Qdrant Retrieval Module Documentation

## Overview

The Qdrant Retrieval Module is designed for testing and validating the RAG (Retrieval-Augmented Generation) pipeline. It provides functionality to retrieve stored embeddings from Qdrant, run similarity queries, and validate the end-to-end extraction + embedding + vector storage pipeline.

## Architecture

The module follows a layered architecture:

```
┌─────────────────┐
│   Application   │
├─────────────────┤
│   QdrantRetriever│
├─────────────────┤
│   Core Modules  │
│  - QdrantConnection │
│  - CollectionValidator │
├─────────────────┤
│   Config/Utils  │
│  - QdrantConfig │
│  - Validation  │
│  - Performance │
└─────────────────┘
```

## Core Components

### QdrantRetriever

The main class for retrieval operations:

- **Purpose**: Handles retrieval operations from Qdrant for testing
- **Key Methods**:
  - `search()`: Perform similarity search in Qdrant
  - `validate_pipeline()`: Validate end-to-end pipeline
  - `get_collection_info()`: Get collection information
  - `measure_response_time()`: Measure response time for operations

### QdrantConnection

- **Purpose**: Manages connection to Qdrant instance
- **Features**: Connection initialization, testing, and management

### CollectionValidator

- **Purpose**: Validates Qdrant collections for proper setup
- **Features**: Schema validation, health checks, access validation

## Configuration

The module uses environment variables for configuration:

```bash
QDRANT_HOST=localhost
QDRANT_PORT=6333
QDRANT_API_KEY=your_api_key  # Optional
QDRANT_COLLECTION_NAME=your_collection
```

Or you can pass a `QdrantConfig` object directly to the constructor.

## Usage Examples

### Basic Usage

```python
from backend.retrieve import QdrantRetriever

# Initialize retriever with environment config
retriever = QdrantRetriever()

# Perform a similarity search
query_vector = [0.1, 0.2, 0.3, 0.4, 0.5]
results = retriever.search(query_vector, top_k=5)

print(f"Found {len(results)} similar embeddings")
for result in results:
    print(f"ID: {result['id']}, Score: {result['score']}")
```

### Pipeline Validation

```python
# Validate the end-to-end pipeline
query_text = "Test query for validation"
expected_ids = ["doc1", "doc2", "doc3"]
query_vector = [0.5, 0.4, 0.3, 0.2, 0.1]

validation_result = retriever.validate_pipeline(
    query_text=query_text,
    expected_ids=expected_ids,
    query_vector=query_vector,
    top_k=5
)

print(f"Accuracy: {validation_result['accuracy_score']:.2%}")
print(f"Passed: {validation_result['validation_passed']}")
print(f"Response time: {validation_result['response_time']:.3f}s")
```

### With Custom Configuration

```python
from backend.config.qdrant_config import QdrantConfig

config = QdrantConfig(
    host="your-qdrant-host.com",
    port=6333,
    collection_name="your_collection",
    api_key="your-api-key"
)

retriever = QdrantRetriever(config=config)
```

## Testing

The module includes comprehensive tests:

- `test_similarity_search.py`: Tests for similarity search functionality
- `test_pipeline_validation.py`: Tests for end-to-end pipeline validation
- `test_health_monitor.py`: Tests for health monitoring functionality

Run tests with pytest:

```bash
cd backend
python -m pytest tests/ -v
```

## Health Monitoring

The module includes a health monitoring system:

```python
from backend.monitor.health_monitor import HealthMonitor

monitor = HealthMonitor()
health_report = monitor.perform_health_check()
print(health_report['overall_status'])

# Get detailed report
detailed_report = monitor.get_health_report()
print(detailed_report)
```

## Performance Metrics

The module tracks performance metrics:

- Response times for search operations
- Accuracy of retrieval
- Pipeline validation times
- Health check completion times

## Error Handling

The module provides comprehensive error handling:

- Connection errors
- Collection validation errors
- Search operation errors
- Pipeline validation errors

## Validation Rules

The module implements several validation rules:

- Embedding vector dimensions must match
- Similarity scores between 0 and 1
- Top-K limits must be positive
- Accuracy threshold of 95% for validation

## Integration

The module integrates with:

- Qdrant vector database
- Environment configuration
- Logging systems
- Performance monitoring

## API Reference

### QdrantRetriever Methods

#### `search(query_vector, top_k=5, query_filter=None)`
Performs similarity search in Qdrant.

**Parameters:**
- `query_vector`: List of floats representing the query embedding
- `top_k`: Number of results to return (default: 5)
- `query_filter`: Optional filter conditions (default: None)

**Returns:** List of results with id, score, and payload

#### `validate_pipeline(query_text, expected_ids, query_vector, top_k=5)`
Validates the end-to-end pipeline by checking if expected embeddings are retrieved.

**Parameters:**
- `query_text`: Original text used for validation
- `expected_ids`: Expected embedding IDs that should be retrieved
- `query_vector`: The embedding vector to search for
- `top_k`: Number of results to return for validation

**Returns:** Dictionary with validation results

#### `get_collection_info()`
Gets information about the collection being used for retrieval.

**Returns:** Dictionary with collection information

## Best Practices

1. Always validate configuration before using the retriever
2. Monitor response times to ensure performance requirements
3. Use appropriate top_k values based on use case
4. Implement proper error handling in production code
5. Regularly check component health using the health monitor

## Troubleshooting

### Common Issues

1. **Connection Issues**: Verify QDRANT_HOST and QDRANT_PORT are correct
2. **Collection Not Found**: Ensure QDRANT_COLLECTION_NAME exists in Qdrant
3. **Authentication Issues**: Check QDRANT_API_KEY if using cloud instance
4. **Performance Issues**: Monitor response times and optimize queries

### Debugging

Enable logging to troubleshoot issues:

```python
import logging
logging.basicConfig(level=logging.INFO)
```

## Version Compatibility

- Python 3.8+
- Qdrant client library
- Compatible with Qdrant server 1.0+

## Security Considerations

- Store API keys securely using environment variables
- Use HTTPS connections when possible
- Validate all input vectors before processing
- Implement proper access controls for production deployments