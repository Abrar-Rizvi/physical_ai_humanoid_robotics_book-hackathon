"""
Tests for the Qdrant Retrieval Module
"""

import pytest
import os
from unittest.mock import Mock, patch
import numpy as np

# Import the retrieve module
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from retrieve import QdrantRetriever


class TestQdrantRetriever:
    """
    Test class for QdrantRetriever functionality
    """

    @patch('retrieve.QdrantClient')
    def test_initialization(self, mock_client):
        """
        Test that QdrantRetriever initializes correctly with environment variables
        """
        # Mock the client methods we need
        mock_instance = Mock()
        mock_instance.get_collections.return_value = Mock()
        mock_instance.get_collections.return_value.collections = [Mock(name='test_collection')]
        mock_client.return_value = mock_instance

        # Set up environment variables for testing
        with patch.dict(os.environ, {
            'QDRANT_HOST': 'localhost',
            'QDRANT_PORT': '6333',
            'COLLECTION_NAME': 'test_collection'
        }):
            retriever = QdrantRetriever()

            assert retriever.host == 'localhost'
            assert retriever.port == 6333
            assert retriever.collection_name == 'test_collection'
            assert mock_client.called

    @patch('retrieve.QdrantClient')
    def test_search_functionality(self, mock_client):
        """
        Test the search functionality of QdrantRetriever
        """
        # Mock the client methods
        mock_instance = Mock()
        mock_instance.get_collections.return_value = Mock()
        mock_instance.get_collections.return_value.collections = [Mock(name='test_collection')]

        # Mock search results
        mock_search_result = [
            Mock(id='id1', score=0.9, payload={'text': 'test1'}),
            Mock(id='id2', score=0.8, payload={'text': 'test2'}),
            Mock(id='id3', score=0.7, payload={'text': 'test3'})
        ]
        mock_instance.search.return_value = mock_search_result
        mock_client.return_value = mock_instance

        with patch.dict(os.environ, {
            'QDRANT_HOST': 'localhost',
            'QDRANT_PORT': '6333',
            'COLLECTION_NAME': 'test_collection'
        }):
            retriever = QdrantRetriever()

            # Test search
            query_vector = [0.1, 0.2, 0.3]
            results = retriever.search(query_vector, top_k=3)

            # Verify the search was called correctly
            mock_instance.search.assert_called_once_with(
                collection_name='test_collection',
                query_vector=query_vector,
                limit=3,
                query_filter=None
            )

            # Verify the results are formatted correctly
            assert len(results) == 3
            assert results[0]['id'] == 'id1'
            assert results[0]['score'] == 0.9
            assert results[0]['payload'] == {'text': 'test1'}

    @patch('retrieve.QdrantClient')
    def test_validate_pipeline(self, mock_client):
        """
        Test the pipeline validation functionality
        """
        # Mock the client methods
        mock_instance = Mock()
        mock_instance.get_collections.return_value = Mock()
        mock_instance.get_collections.return_value.collections = [Mock(name='test_collection')]

        # Mock search results that include 2 out of 3 expected IDs
        mock_search_result = [
            Mock(id='id1', score=0.9, payload={'text': 'test1'}),
            Mock(id='id2', score=0.8, payload={'text': 'test2'}),
            Mock(id='id4', score=0.6, payload={'text': 'test4'})  # Not expected
        ]
        mock_instance.search.return_value = mock_search_result
        mock_client.return_value = mock_instance

        with patch.dict(os.environ, {
            'QDRANT_HOST': 'localhost',
            'QDRANT_PORT': '6333',
            'COLLECTION_NAME': 'test_collection'
        }):
            retriever = QdrantRetriever()

            # Test validation
            query_text = "test query"
            expected_ids = ['id1', 'id2', 'id3']  # id3 is missing in results
            query_vector = [0.1, 0.2, 0.3]

            result = retriever.validate_pipeline(query_text, expected_ids, query_vector, top_k=3)

            # Verify accuracy calculation (2 out of 3 expected items found)
            assert result['accuracy_score'] == 2/3  # ~0.667
            assert result['validation_passed'] is False  # Below 95% threshold
            assert result['details']['correct_retrievals'] == 2
            assert 'id3' in result['details']['missing_ids']  # id3 was expected but not retrieved
            assert 'id4' in result['details']['extra_ids']  # id4 was retrieved but not expected

    @patch('retrieve.QdrantClient')
    def test_get_collection_info(self, mock_client):
        """
        Test getting collection information
        """
        # Mock the client methods
        mock_instance = Mock()
        mock_instance.get_collections.return_value = Mock()
        mock_instance.get_collections.return_value.collections = [Mock(name='test_collection')]

        # Mock collection info
        mock_collection_info = Mock()
        mock_collection_info.config.params = Mock()
        mock_collection_info.config.params.distance = 'Cosine'
        mock_collection_info.points_count = 100
        mock_collection_info.indexed_vectors_count = 100
        mock_instance.get_collection.return_value = mock_collection_info
        mock_client.return_value = mock_instance

        with patch.dict(os.environ, {
            'QDRANT_HOST': 'localhost',
            'QDRANT_PORT': '6333',
            'COLLECTION_NAME': 'test_collection'
        }):
            retriever = QdrantRetriever()

            info = retriever.get_collection_info()

            # Verify the collection info was retrieved
            mock_instance.get_collection.assert_called_once_with('test_collection')
            assert info['points_count'] == 100
            assert info['indexed_vectors_count'] == 100


def test_main_function():
    """
    Test the main function (basic execution)
    """
    with patch('retrieve.QdrantRetriever') as mock_retriever_class:
        mock_retriever_instance = Mock()
        mock_retriever_instance.collection_name = 'test_collection'
        mock_retriever_instance.get_collection_info.return_value = {'points_count': 10}
        mock_retriever_class.return_value = mock_retriever_instance

        from retrieve import main
        result = main()

        assert result == 0  # Success exit code
        assert mock_retriever_class.called


if __name__ == "__main__":
    pytest.main([__file__])