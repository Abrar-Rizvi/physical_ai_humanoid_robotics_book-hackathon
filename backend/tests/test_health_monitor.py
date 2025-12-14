"""
Health monitoring tests for Qdrant Retrieval Pipeline Testing

This module contains tests for health monitoring functionality.
"""

import pytest
import time
from unittest.mock import Mock, patch, MagicMock
import numpy as np

# Import the modules we need to test
from backend.monitor.health_monitor import HealthMonitor, ComponentHealth
from backend.config.qdrant_config import QdrantConfig
from backend.core.qdrant_connection import QdrantConnection


class TestHealthMonitor:
    """
    Test class for health monitoring functionality
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

    @patch('backend.monitor.health_monitor.QdrantConnection')
    @patch('backend.monitor.health_monitor.CollectionValidator')
    def test_health_check_completion_under_30_seconds(self, mock_collection_validator, mock_qdrant_connection, mock_config):
        """
        T050: Test health check completion under 30 seconds
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

        # Mock search for retrieval test
        mock_client.search.return_value = []

        # Create health monitor instance
        monitor = HealthMonitor(config=mock_config)

        # Perform health check
        start_time = time.time()
        health_result = monitor.implement_health_check_timing()
        end_time = time.time()

        # Verify that health check completed within 30 seconds
        assert health_result['total_response_time'] < 30.0
        assert health_result['within_threshold'] is True

        # Also verify actual elapsed time
        actual_time = end_time - start_time
        assert actual_time < 30.0

        # Verify that all components were checked
        assert 'extraction' in health_result['components']
        assert 'embedding' in health_result['components']
        assert 'storage' in health_result['components']
        assert 'retrieval' in health_result['components']

    @patch('backend.monitor.health_monitor.time.perf_counter')
    @patch('backend.monitor.health_monitor.QdrantConnection')
    @patch('backend.monitor.health_monitor.CollectionValidator')
    def test_component_status_reporting(self, mock_collection_validator, mock_qdrant_connection, mock_time, mock_config):
        """
        T051: Test component status reporting
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

        # Mock search for retrieval test
        mock_client.search.return_value = []

        # Mock time to measure response times
        mock_time.side_effect = [100.0, 100.1, 100.2, 100.3, 100.4, 100.5, 100.6, 100.7, 100.8]  # Sequential times

        # Create health monitor instance
        monitor = HealthMonitor(config=mock_config)

        # Test individual component status reporting
        extraction_health = monitor.monitor_extraction_component()
        embedding_health = monitor.monitor_embedding_component()
        storage_health = monitor.monitor_storage_component()
        retrieval_health = monitor.monitor_retrieval_component()

        # Verify component health objects
        assert isinstance(extraction_health, ComponentHealth)
        assert extraction_health.name == "extraction"
        assert extraction_health.status in ["healthy", "degraded", "unhealthy", "unknown"]
        assert isinstance(extraction_health.response_time, float)
        assert isinstance(extraction_health.details, dict)
        assert isinstance(extraction_health.timestamp, float)

        assert isinstance(embedding_health, ComponentHealth)
        assert embedding_health.name == "embedding"
        assert isinstance(embedding_health.response_time, float)

        assert isinstance(storage_health, ComponentHealth)
        assert storage_health.name == "storage"
        assert isinstance(storage_health.response_time, float)

        assert isinstance(retrieval_health, ComponentHealth)
        assert retrieval_health.name == "retrieval"
        assert isinstance(retrieval_health.response_time, float)

        # Perform full health check and verify component reporting
        full_health = monitor.perform_health_check()
        assert 'components' in full_health
        assert len(full_health['components']) == 4

    @patch('backend.monitor.health_monitor.QdrantConnection')
    @patch('backend.monitor.health_monitor.CollectionValidator')
    def test_validate_diagnostic_information_components(self, mock_collection_validator, mock_qdrant_connection, mock_config):
        """
        T052: Validate FR-004: provide diagnostic information about components
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

        # Mock search for retrieval test
        mock_client.search.return_value = []

        # Create health monitor instance
        monitor = HealthMonitor(config=mock_config)

        # Perform health check
        health_result = monitor.perform_health_check()

        # Verify that diagnostic information is provided for each component
        for component_name, component_info in health_result['components'].items():
            assert 'status' in component_info
            assert 'response_time' in component_info
            assert 'details' in component_info

            # Verify that details contain diagnostic information
            assert isinstance(component_info['details'], dict)

        # Verify overall diagnostic information
        assert 'overall_status' in health_result
        assert 'timestamp' in health_result
        assert 'total_response_time' in health_result
        assert 'components' in health_result

        # Verify that the health report can be generated
        report = monitor.get_health_report()
        assert isinstance(report, str)
        assert 'Pipeline Health Report' in report
        assert 'Overall Status:' in report

    @patch('backend.monitor.health_monitor.QdrantConnection')
    @patch('backend.monitor.health_monitor.CollectionValidator')
    def test_validate_health_checks_complete_under_30_seconds(self, mock_collection_validator, mock_qdrant_connection, mock_config):
        """
        T053: Validate SC-004: health checks complete in under 30 seconds
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

        # Mock search for retrieval test
        mock_client.search.return_value = []

        # Create health monitor instance
        monitor = HealthMonitor(config=mock_config)

        # Perform health check using the method that ensures timing requirement
        health_result = monitor.implement_health_check_timing()

        # Verify that health checks complete under 30 seconds as per requirement
        assert health_result['total_response_time'] < 30.0
        assert health_result['within_threshold'] is True

        # Verify the timing requirement is explicitly checked
        assert 'within_threshold' in health_result
        assert isinstance(health_result['within_threshold'], bool)

    @patch('backend.monitor.health_monitor.QdrantConnection')
    @patch('backend.monitor.health_monitor.CollectionValidator')
    def test_acceptance_scenario_health_check_reports_status(self, mock_collection_validator, mock_qdrant_connection, mock_config):
        """
        T054: Test acceptance scenario 1: health check reports component status
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

        # Mock search for retrieval test
        mock_client.search.return_value = []

        # Create health monitor instance
        monitor = HealthMonitor(config=mock_config)

        # Perform comprehensive health check
        health_result = monitor.perform_health_check()

        # Verify that the health check reports status for each component
        assert 'components' in health_result
        components = health_result['components']

        # Check that all required components are reported
        required_components = ['extraction', 'embedding', 'storage', 'retrieval']
        for component in required_components:
            assert component in components
            component_info = components[component]
            assert 'status' in component_info
            assert 'response_time' in component_info
            assert 'details' in component_info

            # Verify status is one of the valid values
            assert component_info['status'] in ['healthy', 'degraded', 'unhealthy', 'unknown']

            # Verify response time is measured
            assert isinstance(component_info['response_time'], float)
            assert component_info['response_time'] >= 0

        # Verify overall status is calculated
        assert health_result['overall_status'] in ['healthy', 'degraded', 'unhealthy']

        # Verify timestamp is included
        assert 'timestamp' in health_result
        assert isinstance(health_result['timestamp'], (int, float))

        # Verify the health report can be generated and contains status information
        report = monitor.get_health_report()
        assert 'Overall Status:' in report
        for component in required_components:
            assert f"{component.title()}:" in report

    @patch('backend.monitor.health_monitor.QdrantConnection')
    @patch('backend.monitor.health_monitor.CollectionValidator')
    def test_extraction_component_monitoring(self, mock_collection_validator, mock_qdrant_connection, mock_config):
        """
        T044: Implement extraction component monitoring
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

        # Create health monitor instance
        monitor = HealthMonitor(config=mock_config)

        # Test extraction component monitoring
        extraction_health = monitor.monitor_extraction_component()

        # Verify extraction monitoring works
        assert extraction_health.name == "extraction"
        assert extraction_health.status in ["healthy", "degraded", "unhealthy", "unknown"]
        assert isinstance(extraction_health.response_time, float)
        assert isinstance(extraction_health.details, dict)

    @patch('backend.monitor.health_monitor.QdrantConnection')
    @patch('backend.monitor.health_monitor.CollectionValidator')
    def test_embedding_component_monitoring(self, mock_collection_validator, mock_qdrant_connection, mock_config):
        """
        T045: Implement embedding component monitoring
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

        # Create health monitor instance
        monitor = HealthMonitor(config=mock_config)

        # Test embedding component monitoring
        embedding_health = monitor.monitor_embedding_component()

        # Verify embedding monitoring works
        assert embedding_health.name == "embedding"
        assert embedding_health.status in ["healthy", "degraded", "unhealthy", "unknown"]
        assert isinstance(embedding_health.response_time, float)
        assert isinstance(embedding_health.details, dict)

    @patch('backend.monitor.health_monitor.QdrantConnection')
    @patch('backend.monitor.health_monitor.CollectionValidator')
    def test_storage_component_monitoring(self, mock_collection_validator, mock_qdrant_connection, mock_config):
        """
        T046: Implement storage component monitoring
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

        # Create health monitor instance
        monitor = HealthMonitor(config=mock_config)

        # Test storage component monitoring
        storage_health = monitor.monitor_storage_component()

        # Verify storage monitoring works
        assert storage_health.name == "storage"
        assert storage_health.status in ["healthy", "degraded", "unhealthy", "unknown"]
        assert isinstance(storage_health.response_time, float)
        assert isinstance(storage_health.details, dict)

    @patch('backend.monitor.health_monitor.QdrantConnection')
    @patch('backend.monitor.health_monitor.CollectionValidator')
    def test_retrieval_component_monitoring(self, mock_collection_validator, mock_qdrant_connection, mock_config):
        """
        T047: Implement retrieval component monitoring
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

        # Mock search for retrieval test
        mock_client.search.return_value = []

        # Create health monitor instance
        monitor = HealthMonitor(config=mock_config)

        # Test retrieval component monitoring
        retrieval_health = monitor.monitor_retrieval_component()

        # Verify retrieval monitoring works
        assert retrieval_health.name == "retrieval"
        assert retrieval_health.status in ["healthy", "degraded", "unhealthy", "unknown"]
        assert isinstance(retrieval_health.response_time, float)
        assert isinstance(retrieval_health.details, dict)

    @patch('backend.monitor.health_monitor.time.perf_counter')
    @patch('backend.monitor.health_monitor.QdrantConnection')
    @patch('backend.monitor.health_monitor.CollectionValidator')
    def test_health_check_timing_implementation(self, mock_collection_validator, mock_qdrant_connection, mock_time, mock_config):
        """
        T048: Implement health check timing (under 30 seconds)
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

        # Mock search for retrieval test
        mock_client.search.return_value = []

        # Mock time to simulate timing
        mock_time.side_effect = [100.0, 101.5, 102.0, 102.5, 103.0, 103.5, 104.0]  # Total ~4 seconds

        # Create health monitor instance
        monitor = HealthMonitor(config=mock_config)

        # Test health check timing implementation
        timing_result = monitor.implement_health_check_timing()

        # Verify timing requirements are met
        assert timing_result['total_response_time'] < 30.0
        assert timing_result['within_threshold'] is True
        assert isinstance(timing_result['total_response_time'], float)


if __name__ == "__main__":
    pytest.main([__file__])