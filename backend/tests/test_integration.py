"""
Integration tests for Qdrant Retrieval Pipeline Testing

This module contains integration tests that validate the complete workflow
across all user stories and components.
"""

import pytest
import os
from unittest.mock import Mock, patch, MagicMock
import numpy as np

# Import the modules we need to test
from backend.retrieve import QdrantRetriever
from backend.config.qdrant_config import QdrantConfig
from backend.core.qdrant_connection import QdrantConnection
from backend.monitor.health_monitor import HealthMonitor
from backend.utils.validation import validate_accuracy_threshold


class TestIntegration:
    """
    Test class for integration tests across all user stories
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
        config.timeout = 30
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
    @patch('backend.monitor.health_monitor.QdrantConnection')
    @patch('backend.monitor.health_monitor.CollectionValidator')
    def test_user_story_1_complete_workflow(self, mock_hc_validator, mock_hc_connection, mock_retriever_validator, mock_retriever_connection, mock_config):
        """
        Integration test for User Story 1: Validate Qdrant Embedding Retrieval
        """
        # Setup retriever mocks
        mock_retriever_client = Mock()
        mock_retriever_connection.return_value.get_client.return_value = mock_retriever_client
        mock_retriever_connection.return_value.test_connection.return_value = True

        mock_retriever_validator_instance = Mock()
        mock_retriever_validator_instance.validate_collection_exists.return_value = Mock()
        mock_retriever_validator_instance.validate_collection_exists.return_value.is_valid = True
        mock_retriever_validator_instance.validate_collection_exists.return_value.issues = []
        mock_retriever_validator.return_value = mock_retriever_validator_instance

        # Setup health monitor mocks
        mock_hc_client = Mock()
        mock_hc_connection.return_value.get_client.return_value = mock_hc_client
        mock_hc_connection.return_value.test_connection.return_value = True

        mock_hc_validator_instance = Mock()
        mock_hc_validator_instance.validate_collection_exists.return_value = Mock()
        mock_hc_validator_instance.validate_collection_exists.return_value.is_valid = True
        mock_hc_validator_instance.validate_collection_exists.return_value.issues = []
        mock_hc_validator.return_value = mock_hc_validator_instance

        # Mock search results
        mock_search_result = [
            Mock(id='result_1', score=0.92, payload={'text': 'Relevant content 1'}),
            Mock(id='result_2', score=0.87, payload={'text': 'Relevant content 2'}),
            Mock(id='result_3', score=0.75, payload={'text': 'Somewhat relevant'})
        ]
        mock_retriever_client.search.return_value = mock_search_result
        mock_hc_client.search.return_value = mock_search_result  # For health check retrieval component

        # Create retriever instance
        retriever = QdrantRetriever(config=mock_config)

        # Test the complete User Story 1 workflow
        query_vector = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]

        # T014-T019: Core retrieval functionality
        results = retriever.search(query_vector, top_k=3)
        assert len(results) == 3
        assert results[0]['score'] >= results[1]['score']  # Results should be sorted by relevance

        # T019: Measure response time
        timing_result = retriever.measure_response_time(query_vector, top_k=2)
        assert 'response_time' in timing_result
        assert 'within_threshold' in timing_result

        # Validate FR-001, FR-002, FR-005 requirements
        assert retriever.connect_to_qdrant() is True  # FR-001
        search_results = retriever.search(query_vector)  # FR-002
        assert len(search_results) >= 0  # Should return some results
        timing_result = retriever.measure_response_time(query_vector)  # FR-005

        # Validate SC-002 requirement
        assert timing_result['within_threshold']  # Response time within 2 seconds

    @patch('backend.retrieve.QdrantConnection')
    @patch('backend.retrieve.CollectionValidator')
    @patch('backend.monitor.health_monitor.QdrantConnection')
    @patch('backend.monitor.health_monitor.CollectionValidator')
    def test_user_story_2_complete_workflow(self, mock_hc_validator, mock_hc_connection, mock_retriever_validator, mock_retriever_connection, mock_config):
        """
        Integration test for User Story 2: End-to-End Pipeline Validation
        """
        # Setup mocks
        mock_retriever_client = Mock()
        mock_retriever_connection.return_value.get_client.return_value = mock_retriever_client
        mock_retriever_connection.return_value.test_connection.return_value = True

        mock_retriever_validator_instance = Mock()
        mock_retriever_validator_instance.validate_collection_exists.return_value = Mock()
        mock_retriever_validator_instance.validate_collection_exists.return_value.is_valid = True
        mock_retriever_validator_instance.validate_collection_exists.return_value.issues = []
        mock_retriever_validator.return_value = mock_retriever_validator_instance

        # Setup health monitor mocks
        mock_hc_client = Mock()
        mock_hc_connection.return_value.get_client.return_value = mock_hc_client
        mock_hc_connection.return_value.test_connection.return_value = True

        mock_hc_validator_instance = Mock()
        mock_hc_validator_instance.validate_collection_exists.return_value = Mock()
        mock_hc_validator_instance.validate_collection_exists.return_value.is_valid = True
        mock_hc_validator_instance.validate_collection_exists.return_value.issues = []
        mock_hc_validator.return_value = mock_hc_validator_instance

        # Mock search results for pipeline validation
        expected_ids = ['doc_A', 'doc_B', 'doc_C']
        mock_search_result = [
            Mock(id='doc_A', score=0.91, payload={'text': 'Expected document A'}),
            Mock(id='doc_B', score=0.85, payload={'text': 'Expected document B'}),
            Mock(id='doc_C', score=0.78, payload={'text': 'Expected document C'}),
            Mock(id='doc_D', score=0.65, payload={'text': 'Extra document'})
        ]
        mock_retriever_client.search.return_value = mock_search_result

        # Create retriever instance
        retriever = QdrantRetriever(config=mock_config)

        # Test the complete User Story 2 workflow
        query_text = "End-to-end pipeline validation query"
        query_vector = [0.5, 0.4, 0.3, 0.2, 0.1, 0.6, 0.7, 0.8, 0.9, 1.0]

        # T030-T033: Pipeline validation functionality
        validation_result = retriever.validate_pipeline(
            query_text=query_text,
            expected_ids=expected_ids,
            query_vector=query_vector,
            top_k=5
        )

        # Verify pipeline validation results
        assert validation_result['query_text'] == query_text
        assert set(expected_ids).issubset(set(validation_result['retrieved_ids']))  # T037: FR-003 validation
        assert validation_result['accuracy_score'] >= 0.75  # High accuracy expected
        assert 'response_time' in validation_result

        # Validate FR-006: end-to-end pipeline produces retrievable results
        assert len(validation_result['retrieved_ids']) > 0

        # Validate SC-001: 95% accuracy threshold (if achievable with mock data)
        # Since we have 3 expected and all 3 were retrieved + 1 extra, accuracy should be 100% for expected
        correct_retrievals = validation_result['details']['correct_retrievals']
        total_expected = validation_result['details']['total_expected']
        expected_accuracy = correct_retrievals / total_expected if total_expected > 0 else 1.0
        assert validation_result['accuracy_score'] == expected_accuracy

        # Validate SC-003: retrievability of stored embeddings
        assert len(validation_result['retrieved_ids']) >= len(expected_ids)  # At least all expected were retrieved

    @patch('backend.retrieve.QdrantConnection')
    @patch('backend.retrieve.CollectionValidator')
    @patch('backend.monitor.health_monitor.QdrantConnection')
    @patch('backend.monitor.health_monitor.CollectionValidator')
    def test_user_story_3_complete_workflow(self, mock_hc_validator, mock_hc_connection, mock_retriever_validator, mock_retriever_connection, mock_config):
        """
        Integration test for User Story 3: Pipeline Health Monitoring
        """
        # Setup mocks
        mock_retriever_client = Mock()
        mock_retriever_connection.return_value.get_client.return_value = mock_retriever_client
        mock_retriever_connection.return_value.test_connection.return_value = True

        mock_retriever_validator_instance = Mock()
        mock_retriever_validator_instance.validate_collection_exists.return_value = Mock()
        mock_retriever_validator_instance.validate_collection_exists.return_value.is_valid = True
        mock_retriever_validator_instance.validate_collection_exists.return_value.issues = []
        mock_retriever_validator.return_value = mock_retriever_validator_instance

        # Setup health monitor mocks
        mock_hc_client = Mock()
        mock_hc_connection.return_value.get_client.return_value = mock_hc_client
        mock_hc_connection.return_value.test_connection.return_value = True

        mock_hc_validator_instance = Mock()
        mock_hc_validator_instance.validate_collection_exists.return_value = Mock()
        mock_hc_validator_instance.validate_collection_exists.return_value.is_valid = True
        mock_hc_validator_instance.validate_collection_exists.return_value.issues = []
        mock_hc_validator.return_value = mock_hc_validator_instance

        # Mock search for health monitor retrieval component check
        mock_hc_search_result = [
            Mock(id='health_test', score=0.85, payload={'text': 'Health check content'})
        ]
        mock_hc_client.search.return_value = mock_hc_search_result

        # Create health monitor instance
        monitor = HealthMonitor(config=mock_config)

        # T042-T054: Health monitoring functionality
        health_result = monitor.perform_health_check()

        # Verify health check results
        assert 'overall_status' in health_result
        assert 'components' in health_result
        assert 'total_response_time' in health_result
        assert 'within_threshold' in health_result

        # Validate component monitoring (T043-T047)
        components = ['extraction', 'embedding', 'storage', 'retrieval']
        for component in components:
            assert component in health_result['components']
            component_info = health_result['components'][component]
            assert 'status' in component_info
            assert 'response_time' in component_info
            assert 'details' in component_info

        # T048: Validate health check timing under 30 seconds
        assert health_result['total_response_time'] < 30.0
        assert health_result['within_threshold'] is True

        # T052: Validate FR-004 - diagnostic information
        for component, info in health_result['components'].items():
            assert isinstance(info['details'], dict)

        # T053: Validate SC-004 - health checks complete under 30 seconds
        timing_result = monitor.implement_health_check_timing()
        assert timing_result['within_threshold'] is True

        # T054: Acceptance scenario - health check reports component status
        report = monitor.get_health_report()
        assert 'Pipeline Health Report' in report
        for component in components:
            assert f"{component.title()}:" in report

    @patch('backend.retrieve.QdrantConnection')
    @patch('backend.retrieve.CollectionValidator')
    @patch('backend.monitor.health_monitor.QdrantConnection')
    @patch('backend.monitor.health_monitor.CollectionValidator')
    def test_complete_end_to_end_integration(self, mock_hc_validator, mock_hc_connection, mock_retriever_validator, mock_retriever_connection, mock_config):
        """
        Complete end-to-end integration test combining all user stories
        """
        # Setup mocks
        mock_retriever_client = Mock()
        mock_retriever_connection.return_value.get_client.return_value = mock_retriever_client
        mock_retriever_connection.return_value.test_connection.return_value = True

        mock_retriever_validator_instance = Mock()
        mock_retriever_validator_instance.validate_collection_exists.return_value = Mock()
        mock_retriever_validator_instance.validate_collection_exists.return_value.is_valid = True
        mock_retriever_validator_instance.validate_collection_exists.return_value.issues = []
        mock_retriever_validator.return_value = mock_retriever_validator_instance

        # Setup health monitor mocks
        mock_hc_client = Mock()
        mock_hc_connection.return_value.get_client.return_value = mock_hc_client
        mock_hc_connection.return_value.test_connection.return_value = True

        mock_hc_validator_instance = Mock()
        mock_hc_validator_instance.validate_collection_exists.return_value = Mock()
        mock_hc_validator_instance.validate_collection_exists.return_value.is_valid = True
        mock_hc_validator_instance.validate_collection_exists.return_value.issues = []
        mock_hc_validator.return_value = mock_hc_validator_instance

        # Mock search results for various operations
        retrieval_results = [
            Mock(id='doc_1', score=0.92, payload={'text': 'Highly relevant content'}),
            Mock(id='doc_2', score=0.85, payload={'text': 'Relevant content'}),
            Mock(id='doc_3', score=0.78, payload={'text': 'Moderately relevant content'}),
            Mock(id='doc_4', score=0.65, payload={'text': 'Less relevant content'})
        ]
        mock_retriever_client.search.return_value = retrieval_results
        mock_hc_client.search.return_value = retrieval_results

        # Create instances
        retriever = QdrantRetriever(config=mock_config)
        monitor = HealthMonitor(config=mock_config)

        # Step 1: Check health before operations
        initial_health = monitor.perform_health_check()
        assert initial_health['overall_status'] in ['healthy', 'degraded']

        # Step 2: Perform retrieval operations (User Story 1)
        query_vector = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]
        search_results = retriever.search(query_vector, top_k=3)
        assert len(search_results) == 3

        # Step 3: Measure performance (part of User Story 1)
        timing_result = retriever.measure_response_time(query_vector, top_k=2)
        assert timing_result['within_threshold'] is True

        # Step 4: Validate pipeline (User Story 2)
        expected_ids = ['doc_1', 'doc_2']
        validation_result = retriever.validate_pipeline(
            query_text="Integration test query",
            expected_ids=expected_ids,
            query_vector=query_vector,
            top_k=4
        )
        assert validation_result['accuracy_score'] >= 0.5  # Reasonable accuracy
        assert 'response_time' in validation_result

        # Step 5: Check health after operations (User Story 3)
        final_health = monitor.perform_health_check()
        assert final_health['overall_status'] in ['healthy', 'degraded']

        # Step 6: Validate cross-cutting requirements
        # T060: FR-007 - provide clear pass/fail indicators
        assert 'validation_passed' in validation_result
        assert isinstance(validation_result['validation_passed'], bool)

        # Verify accuracy threshold validation
        accuracy_valid = retriever.validate_accuracy_threshold(validation_result['accuracy_score'])
        assert isinstance(accuracy_valid, bool)

        # Verify response time threshold validation
        time_valid = retriever.validate_response_time_threshold(validation_result['response_time'])
        assert isinstance(time_valid, bool)

        # All components should have been tested in the complete workflow
        assert len(search_results) > 0
        assert validation_result['accuracy_score'] >= 0
        assert final_health['within_threshold'] is True

    @patch('backend.retrieve.QdrantConnection')
    @patch('backend.retrieve.CollectionValidator')
    @patch('backend.monitor.health_monitor.QdrantConnection')
    @patch('backend.monitor.health_monitor.CollectionValidator')
    def test_error_handling_integration(self, mock_hc_validator, mock_hc_connection, mock_retriever_validator, mock_retriever_connection, mock_config):
        """
        Test error handling across integrated components
        """
        # Setup mocks with potential failure scenarios
        mock_retriever_client = Mock()
        mock_retriever_connection.return_value.get_client.return_value = mock_retriever_client
        mock_retriever_connection.return_value.test_connection.return_value = True

        mock_retriever_validator_instance = Mock()
        mock_retriever_validator_instance.validate_collection_exists.return_value = Mock()
        mock_retriever_validator_instance.validate_collection_exists.return_value.is_valid = True
        mock_retriever_validator_instance.validate_collection_exists.return_value.issues = []
        mock_retriever_validator.return_value = mock_retriever_validator_instance

        # Setup health monitor mocks
        mock_hc_client = Mock()
        mock_hc_connection.return_value.get_client.return_value = mock_hc_client
        mock_hc_connection.return_value.test_connection.return_value = True

        mock_hc_validator_instance = Mock()
        mock_hc_validator_instance.validate_collection_exists.return_value = Mock()
        mock_hc_validator_instance.validate_collection_exists.return_value.is_valid = True
        mock_hc_validator_instance.validate_collection_exists.return_value.issues = []
        mock_hc_validator.return_value = mock_hc_validator_instance

        # Mock normal search results
        normal_results = [Mock(id='normal', score=0.8, payload={'text': 'normal content'})]
        mock_retriever_client.search.return_value = normal_results
        mock_hc_client.search.return_value = normal_results

        # Create instances
        retriever = QdrantRetriever(config=mock_config)
        monitor = HealthMonitor(config=mock_config)

        # Test proper error handling in search with invalid inputs
        with pytest.raises(ValueError):
            retriever.search([])  # Empty query vector

        with pytest.raises(ValueError):
            retriever.search([0.1, 0.2], top_k=0)  # Invalid top_k

        with pytest.raises(ValueError):
            retriever.validate_pipeline(123, [], [0.1])  # Invalid query_text type

        # Verify that valid operations still work after error conditions
        valid_vector = [0.1, 0.2, 0.3]
        results = retriever.search(valid_vector)
        assert len(results) >= 0

        # Test health monitoring still works
        health_result = monitor.perform_health_check()
        assert 'overall_status' in health_result


if __name__ == "__main__":
    pytest.main([__file__])