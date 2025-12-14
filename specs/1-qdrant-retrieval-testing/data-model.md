# Data Model: Qdrant Retrieval Pipeline Testing

## Entities

### Embedding
**Description**: Vector representation of documents or text chunks stored in Qdrant for similarity search
**Fields**:
- `id`: Unique identifier for the embedding
- `vector`: High-dimensional vector representation (list of floats)
- `payload`: Metadata associated with the embedding (dict)
- `collection_name`: Name of the Qdrant collection where it's stored

### SimilarityQuery
**Description**: Search operation that finds vectors most similar to a given query vector
**Fields**:
- `query_vector`: The vector to search for similar matches (list of floats)
- `top_k`: Number of results to return (int)
- `collection_name`: Name of the Qdrant collection to search in (string)
- `query_filter`: Optional filter conditions for the search (dict, optional)

### RetrievalResult
**Description**: Result of a similarity query operation
**Fields**:
- `id`: ID of the matching embedding
- `score`: Similarity score (float between 0 and 1)
- `vector`: The matching embedding vector (list of floats)
- `payload`: Metadata associated with the matching embedding (dict)

### PipelineValidation
**Description**: Validation result for the end-to-end pipeline
**Fields**:
- `query_text`: Original text used for validation (string)
- `expected_results`: Expected embeddings that should be retrieved (list of Embedding)
- `actual_results`: Actual embeddings retrieved by the system (list of RetrievalResult)
- `accuracy_score`: Percentage of correct matches (float between 0 and 1)
- `response_time`: Time taken for the query (float in seconds)
- `validation_passed`: Whether the validation met accuracy threshold (boolean)

## Validation Rules

1. **Embedding Vector Dimensions**: All vectors in a collection must have the same dimension
2. **Similarity Score Range**: Scores must be between 0 and 1
3. **Top-K Limit**: top_k parameter must be positive and not exceed collection size
4. **Accuracy Threshold**: Validation passes if accuracy_score >= 0.95 (95%)

## Relationships

- `PipelineValidation` contains multiple `RetrievalResult` instances
- `SimilarityQuery` produces multiple `RetrievalResult` instances
- `RetrievalResult` references an original `Embedding`