"""
Similarity search tests for Qdrant Retrieval Pipeline Testing

This module contains tests for similarity search functionality.
"""

import pytest
import os
from unittest.mock import Mock, patch, MagicMock
import numpy as np

# Import the modules we need to test
from backend.retrieve import QdrantRetriever
from backend.config.qdrant_config import QdrantConfig
from backend.core.qdrant_connection import QdrantConnection


class TestSimilaritySearch:
    """
    Test class for similarity search functionality
    """

    @pytest.fixture
    def mock_config(self):
        """
        Fixture to create a mock QdrantConfig
        """
        config = Mock(spec=QdrantConfig)
        config.host = "localhost"
        config.port = 6333
        config.api_key = None
        config.collection_name = "test_collection"
        return config

    @pytest.fixture
    def mock_qdrant_connection(self):
        """
        Fixture to create a mock QdrantConnection
        """
        connection = Mock(spec=QdrantConnection)
        connection.get_client.return_value = Mock()
        connection.test_connection.return_value = True
        return connection

    @patch('backend.retrieve.QdrantConnection')
    @patch('backend.retrieve.CollectionValidator')
    def test_query_vector_handling(self, mock_collection_validator, mock_qdrant_connection, mock_config):
        """
        T021: Test query vector handling
        """
        # Setup mocks
        mock_client = Mock()
        mock_qdrant_connection.return_value.get_client.return_value = mock_client
        mock_qdrant_connection.return_value.test_connection.return_value = True

        # Mock collection validation to pass
        mock_validator_instance = Mock()
        mock_validator_instance.validate_collection_exists.return_value = Mock()
        mock_validator_instance.validate_collection_exists.return_value.is_valid = True
        mock_validator_instance.validate_collection_exists.return_value.issues = []
        mock_collection_validator.return_value = mock_validator_instance

        # Mock search results
        mock_search_result = [
            Mock(id='id1', score=0.9, payload={'text': 'test1'}),
            Mock(id='id2', score=0.8, payload={'text': 'test2'})
        ]
        mock_client.search.return_value = mock_search_result

        # Create retriever instance
        retriever = QdrantRetriever(config=mock_config)

        # Test with valid query vector
        query_vector = [0.1, 0.2, 0.3, 0.4]
        top_k = 2

        results = retriever.search(query_vector, top_k)

        # Verify the search was called with correct parameters
        mock_client.search.assert_called_once_with(
            collection_name=mock_config.collection_name,
            query_vector=query_vector,
            limit=top_k,
            query_filter=None
        )

        # Verify results format
        assert len(results) == 2
        assert results[0]['id'] == 'id1'
        assert results[0]['score'] == 0.9
        assert results[0]['payload'] == {'text': 'test1'}

    @patch('backend.retrieve.QdrantConnection')
    @patch('backend.retrieve.CollectionValidator')
    def test_result_ranking_by_relevance_score(self, mock_collection_validator, mock_qdrant_connection, mock_config):
        """
        T022: Test result ranking by relevance score
        """
        # Setup mocks
        mock_client = Mock()
        mock_qdrant_connection.return_value.get_client.return_value = mock_client
        mock_qdrant_connection.return_value.test_connection.return_value = True

        # Mock collection validation to pass
        mock_validator_instance = Mock()
        mock_validator_instance.validate_collection_exists.return_value = Mock()
        mock_validator_instance.validate_collection_exists.return_value.is_valid = True
        mock_validator_instance.validate_collection_exists.return_value.issues = []
        mock_collection_validator.return_value = mock_validator_instance

        # Mock search results with scores in non-sorted order (Qdrant handles sorting internally)
        mock_search_result = [
            Mock(id='id3', score=0.7, payload={'text': 'test3'}),
            Mock(id='id1', score=0.9, payload={'text': 'test1'}),
            Mock(id='id2', score=0.8, payload={'text': 'test2'})
        ]
        mock_client.search.return_value = mock_search_result

        # Create retriever instance
        retriever = QdrantRetriever(config=mock_config)

        query_vector = [0.1, 0.2, 0.3, 0.4]
        top_k = 5

        results = retriever.search(query_vector, top_k)

        # Note: Qdrant returns results already sorted by score (descending)
        # So the first result should have the highest score
        assert results[0]['score'] >= results[1]['score']
        if len(results) > 2:
            assert results[1]['score'] >= results[2]['score']

        # Verify all results are returned as Qdrant sorts internally
        assert len(results) == 3

    @patch('backend.retrieve.time.perf_counter')
    @patch('backend.retrieve.QdrantConnection')
    @patch('backend.retrieve.CollectionValidator')
    def test_response_time_within_2_seconds(self, mock_collection_validator, mock_qdrant_connection, mock_time, mock_config):
        """
        T023: Test response time within 2 seconds
        """
        # Setup time mock to simulate a response time of 1.5 seconds
        mock_time.side_effect = [100.0, 101.5]  # start_time, end_time (1.5 seconds difference)

        # Setup other mocks
        mock_client = Mock()
        mock_qdrant_connection.return_value.get_client.return_value = mock_client
        mock_qdrant_connection.return_value.test_connection.return_value = True

        # Mock collection validation to pass
        mock_validator_instance = Mock()
        mock_validator_instance.validate_collection_exists.return_value = Mock()
        mock_validator_instance.validate_collection_exists.return_value.is_valid = True
        mock_validator_instance.validate_collection_exists.return_value.issues = []
        mock_collection_validator.return_value = mock_validator_instance

        # Mock search results
        mock_search_result = [
            Mock(id='id1', score=0.9, payload={'text': 'test1'})
        ]
        mock_client.search.return_value = mock_search_result

        # Create retriever instance
        retriever = QdrantRetriever(config=mock_config)

        query_vector = [0.1, 0.2, 0.3, 0.4]
        top_k = 1

        # Capture the result with response time measurement
        result_with_timing = retriever.measure_response_time(query_vector, top_k)

        # Verify that response time is within 2 seconds threshold
        assert result_with_timing['response_time'] == 1.5
        assert result_with_timing['within_threshold'] is True  # 1.5 < 2.0

    @patch('backend.retrieve.time.perf_counter')
    @patch('backend.retrieve.QdrantConnection')
    @patch('backend.retrieve.CollectionValidator')
    def test_acceptance_scenario_1_embeddings_retrieval(self, mock_collection_validator, mock_qdrant_connection, mock_time, mock_config):
        """
        T024: Test acceptance scenario 1: embeddings retrieval with acceptable response time
        """
        # Setup time mock to simulate a response time of 1.2 seconds
        mock_time.side_effect = [100.0, 101.2]  # start_time, end_time (1.2 seconds difference)

        # Setup other mocks
        mock_client = Mock()
        mock_qdrant_connection.return_value.get_client.return_value = mock_client
        mock_qdrant_connection.return_value.test_connection.return_value = True

        # Mock collection validation to pass
        mock_validator_instance = Mock()
        mock_validator_instance.validate_collection_exists.return_value = Mock()
        mock_validator_instance.validate_collection_exists.return_value.is_valid = True
        mock_validator_instance.validate_collection_exists.return_value.issues = []
        mock_collection_validator.return_value = mock_validator_instance

        # Mock search results
        mock_search_result = [
            Mock(id='doc1', score=0.95, payload={'text': 'This is the first document', 'source': 'test'}),
            Mock(id='doc2', score=0.87, payload={'text': 'This is the second document', 'source': 'test'})
        ]
        mock_client.search.return_value = mock_search_result

        # Create retriever instance
        retriever = QdrantRetriever(config=mock_config)

        query_vector = [0.1, 0.2, 0.3, 0.4, 0.5]
        top_k = 2

        # Perform the search
        results = retriever.search(query_vector, top_k)

        # Verify that embeddings were retrieved successfully
        assert len(results) == 2
        assert results[0]['id'] == 'doc1'
        assert results[0]['score'] == 0.95
        assert results[1]['id'] == 'doc2'
        assert results[1]['score'] == 0.87

        # Verify that response time is acceptable (< 2 seconds)
        result_with_timing = retriever.measure_response_time(query_vector, top_k)
        assert result_with_timing['within_threshold'] is True  # 1.2 < 2.0

    @patch('backend.retrieve.time.perf_counter')
    @patch('backend.retrieve.QdrantConnection')
    @patch('backend.retrieve.CollectionValidator')
    def test_acceptance_scenario_2_relevance_score_ranking(self, mock_collection_validator, mock_qdrant_connection, mock_time, mock_config):
        """
        T025: Test acceptance scenario 2: relevance score ranking
        """
        # Setup time mock
        mock_time.side_effect = [100.0, 100.8]

        # Setup other mocks
        mock_client = Mock()
        mock_qdrant_connection.return_value.get_client.return_value = mock_client
        mock_qdrant_connection.return_value.test_connection.return_value = True

        # Mock collection validation to pass
        mock_validator_instance = Mock()
        mock_validator_instance.validate_collection_exists.return_value = Mock()
        mock_validator_instance.validate_collection_exists.return_value.is_valid = True
        mock_validator_instance.validate_collection_exists.return_value.issues = []
        mock_collection_validator.return_value = mock_validator_instance

        # Mock search results - Qdrant should return them sorted by relevance (highest score first)
        mock_search_result = [
            Mock(id='high_score_doc', score=0.92, payload={'text': 'High relevance content'}),
            Mock(id='medium_score_doc', score=0.75, payload={'text': 'Medium relevance content'}),
            Mock(id='low_score_doc', score=0.45, payload={'text': 'Low relevance content'})
        ]
        mock_client.search.return_value = mock_search_result

        # Create retriever instance
        retriever = QdrantRetriever(config=mock_config)

        query_vector = [0.5, 0.4, 0.3, 0.2, 0.1]
        top_k = 3

        results = retriever.search(query_vector, top_k)

        # Verify that results are ranked by relevance score (highest first)
        assert results[0]['score'] >= results[1]['score']
        assert results[1]['score'] >= results[2]['score']
        assert results[0]['id'] == 'high_score_doc'
        assert results[0]['score'] == 0.92
        assert results[2]['score'] == 0.45

    @patch('backend.retrieve.QdrantConnection')
    @patch('backend.retrieve.CollectionValidator')
    def test_validate_connect_to_qdrant(self, mock_collection_validator, mock_qdrant_connection, mock_config):
        """
        T026: Validate FR-001: connect to Qdrant vector database
        """
        # Setup mocks
        mock_client = Mock()
        mock_qdrant_connection.return_value.get_client.return_value = mock_client
        mock_qdrant_connection.return_value.test_connection.return_value = True

        # Mock collection validation to pass
        mock_validator_instance = Mock()
        mock_validator_instance.validate_collection_exists.return_value = Mock()
        mock_validator_instance.validate_collection_exists.return_value.is_valid = True
        mock_validator_instance.validate_collection_exists.return_value.issues = []
        mock_collection_validator.return_value = mock_validator_instance

        # Create retriever instance
        retriever = QdrantRetriever(config=mock_config)

        # Test connection functionality
        connection_result = retriever.connect_to_qdrant()
        assert connection_result is True

    @patch('backend.retrieve.QdrantConnection')
    @patch('backend.retrieve.CollectionValidator')
    def test_validate_execute_similarity_queries(self, mock_collection_validator, mock_qdrant_connection, mock_config):
        """
        T027: Validate FR-002: execute similarity queries against stored embeddings
        """
        # Setup mocks
        mock_client = Mock()
        mock_qdrant_connection.return_value.get_client.return_value = mock_client
        mock_qdrant_connection.return_value.test_connection.return_value = True

        # Mock collection validation to pass
        mock_validator_instance = Mock()
        mock_validator_instance.validate_collection_exists.return_value = Mock()
        mock_validator_instance.validate_collection_exists.return_value.is_valid = True
        mock_validator_instance.validate_collection_exists.return_value.issues = []
        mock_collection_validator.return_value = mock_validator_instance

        # Mock search results
        mock_search_result = [Mock(id='test_id', score=0.85, payload={'content': 'test'})]
        mock_client.search.return_value = mock_search_result

        # Create retriever instance
        retriever = QdrantRetriever(config=mock_config)

        # Execute similarity query
        query_vector = [0.1, 0.2, 0.3]
        results = retriever.search(query_vector)

        # Verify that similarity query was executed
        mock_client.search.assert_called_once()
        assert len(results) == 1
        assert results[0]['id'] == 'test_id'

    @patch('backend.retrieve.time.perf_counter')
    @patch('backend.retrieve.QdrantConnection')
    @patch('backend.retrieve.CollectionValidator')
    def test_validate_measure_response_times(self, mock_collection_validator, mock_qdrant_connection, mock_time, mock_config):
        """
        T028: Validate FR-005: measure and report response times
        """
        # Setup time mock
        mock_time.side_effect = [100.0, 101.0]  # 1.0 second response time

        # Setup other mocks
        mock_client = Mock()
        mock_qdrant_connection.return_value.get_client.return_value = mock_client
        mock_qdrant_connection.return_value.test_connection.return_value = True

        # Mock collection validation to pass
        mock_validator_instance = Mock()
        mock_validator_instance.validate_collection_exists.return_value = Mock()
        mock_validator_instance.validate_collection_exists.return_value.is_valid = True
        mock_validator_instance.validate_collection_exists.return_value.issues = []
        mock_collection_validator.return_value = mock_validator_instance

        # Mock search results
        mock_search_result = [Mock(id='result_id', score=0.75, payload={'data': 'test'})]
        mock_client.search.return_value = mock_search_result

        # Create retriever instance
        retriever = QdrantRetriever(config=mock_config)

        # Test response time measurement
        timing_result = retriever.measure_response_time([0.1, 0.2], top_k=1)

        assert timing_result['response_time'] == 1.0
        assert 'results' in timing_result

    @patch('backend.retrieve.time.perf_counter')
    @patch('backend.retrieve.QdrantConnection')
    @patch('backend.retrieve.CollectionValidator')
    def test_validate_response_time_within_threshold(self, mock_collection_validator, mock_qdrant_connection, mock_time, mock_config):
        """
        T029: Validate SC-002: similarity queries return results within 2 seconds
        """
        # Setup time mock for response just under threshold: 1.8 seconds
        mock_time.side_effect = [100.0, 101.8]

        # Setup other mocks
        mock_client = Mock()
        mock_qdrant_connection.return_value.get_client.return_value = mock_client
        mock_qdrant_connection.return_value.test_connection.return_value = True

        # Mock collection validation to pass
        mock_validator_instance = Mock()
        mock_validator_instance.validate_collection_exists.return_value = Mock()
        mock_validator_instance.validate_collection_exists.return_value.is_valid = True
        mock_validator_instance.validate_collection_exists.return_value.issues = []
        mock_collection_validator.return_value = mock_validator_instance

        # Mock search results
        mock_search_result = [Mock(id='result', score=0.8, payload={'text': 'test'})]
        mock_client.search.return_value = mock_search_result

        # Create retriever instance
        retriever = QdrantRetriever(config=mock_config)

        # Test that response time is within 2-second threshold
        timing_result = retriever.measure_response_time([0.1, 0.2, 0.3], top_k=1)

        assert timing_result['response_time'] == 1.8
        assert timing_result['within_threshold'] is True  # 1.8 < 2.0


if __name__ == "__main__":
    pytest.main([__file__])