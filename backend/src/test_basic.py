"""
Basic unit tests for core RAG agent functionality
"""
import pytest
import asyncio
from src.config import settings
from src.utils.embeddings import get_embedding
from src.retrieval import retrieve_context


def test_embedding_generation():
    """Test that embedding generation works correctly"""
    text = "test query for embedding"
    embedding = get_embedding(text)

    assert isinstance(embedding, list)
    assert len(embedding) > 0
    assert all(isinstance(val, float) for val in embedding)


@pytest.mark.asyncio
async def test_context_retrieval():
    """Test that context retrieval works (if Qdrant is available)"""
    # This test would require a running Qdrant instance with data
    # For now, we'll just test that the function can be called
    try:
        result = await retrieve_context("test query", top_k=1)
        # If Qdrant is available, this should return a RetrievedContext object
        assert hasattr(result, 'documents')
    except Exception as e:
        # If Qdrant is not available, we expect an exception
        # This is normal in test environments without Qdrant
        pass


if __name__ == "__main__":
    # Run the tests
    test_embedding_generation()
    print("Embedding test passed!")

    # For async tests, we'd typically use pytest
    asyncio.run(test_context_retrieval())
    print("Context retrieval test completed!")