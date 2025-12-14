"""
Health monitoring functionality for Qdrant Retrieval Pipeline Testing

This module provides tools to monitor and diagnose the retrieval pipeline.
"""

import time
import logging
from typing import Dict, Any, List, Optional
from dataclasses import dataclass

from backend.config.qdrant_config import QdrantConfig
from backend.core.qdrant_connection import QdrantConnection
from backend.core.collection_validator import CollectionValidator


@dataclass
class ComponentHealth:
    """
    Data class to represent the health status of a pipeline component
    """
    name: str
    status: str  # 'healthy', 'degraded', 'unhealthy', 'unknown'
    response_time: float
    details: Dict[str, Any]
    timestamp: float


class HealthMonitor:
    """
    Class to monitor and diagnose the retrieval pipeline components
    """
    def __init__(self, config: QdrantConfig = None):
        """
        Initialize the health monitor with configuration

        Args:
            config: Optional QdrantConfig instance. If not provided, will use environment variables.
        """
        self.config = config or QdrantConfig.from_env()
        self.qdrant_connection = QdrantConnection(self.config)
        self.collection_validator = CollectionValidator(self.qdrant_connection)
        self.client = self.qdrant_connection.get_client()

    def check_component_status(self, component_name: str) -> ComponentHealth:
        """
        Check the status of a specific component

        Args:
            component_name: Name of the component to check ('extraction', 'embedding', 'storage', 'retrieval')

        Returns:
            ComponentHealth object with status information
        """
        start_time = time.perf_counter()

        if component_name == "extraction":
            status, details = self._check_extraction_component()
        elif component_name == "embedding":
            status, details = self._check_embedding_component()
        elif component_name == "storage":
            status, details = self._check_storage_component()
        elif component_name == "retrieval":
            status, details = self._check_retrieval_component()
        else:
            status = "unknown"
            details = {"error": f"Unknown component: {component_name}"}

        response_time = time.perf_counter() - start_time

        return ComponentHealth(
            name=component_name,
            status=status,
            response_time=response_time,
            details=details,
            timestamp=time.time()
        )

    def _check_extraction_component(self) -> tuple[str, Dict[str, Any]]:
        """
        Check the health of the extraction component

        Returns:
            Tuple of (status, details)
        """
        # For now, we'll assume extraction is healthy if environment is set up properly
        # In a real implementation, this would check actual extraction services
        try:
            # Check if required environment variables for extraction are set
            extraction_vars = ["EXTRACTION_SOURCE_URL", "EXTRACTION_API_KEY"]
            missing_vars = [var for var in extraction_vars if not self.config.__dict__.get(var.lower().replace("extra_", "").replace("_", ""))]

            if not missing_vars:
                return "healthy", {"message": "Extraction component configuration is complete"}
            else:
                return "degraded", {"message": "Some extraction configuration missing", "missing_vars": missing_vars}
        except Exception as e:
            return "unhealthy", {"error": str(e)}

    def _check_embedding_component(self) -> tuple[str, Dict[str, Any]]:
        """
        Check the health of the embedding component

        Returns:
            Tuple of (status, details)
        """
        # For now, we'll assume embedding is healthy if environment is set up properly
        # In a real implementation, this would check actual embedding services
        try:
            # Check if required environment variables for embedding are set
            embedding_vars = ["COHERE_API_KEY", "EMBEDDING_MODEL"]
            missing_vars = [var for var in embedding_vars if not self.config.__dict__.get(var.lower().replace("embedding_", "").replace("_", ""))]

            if not missing_vars:
                return "healthy", {"message": "Embedding component configuration is complete"}
            else:
                return "degraded", {"message": "Some embedding configuration missing", "missing_vars": missing_vars}
        except Exception as e:
            return "unhealthy", {"error": str(e)}

    def _check_storage_component(self) -> tuple[str, Dict[str, Any]]:
        """
        Check the health of the storage component (Qdrant)

        Returns:
            Tuple of (status, details)
        """
        try:
            # Check Qdrant connection
            if not self.qdrant_connection.test_connection():
                return "unhealthy", {"error": "Cannot connect to Qdrant"}

            # Validate collection
            validation_result = self.collection_validator.validate_collection_completely(self.config.collection_name)

            if validation_result.is_valid:
                return "healthy", {
                    "message": "Storage component (Qdrant) is healthy",
                    "collection": self.config.collection_name,
                    "issues": validation_result.issues
                }
            else:
                if "does not exist" in str(validation_result.issues):
                    return "unhealthy", {
                        "error": f"Collection {self.config.collection_name} does not exist",
                        "issues": validation_result.issues
                    }
                else:
                    return "degraded", {
                        "message": "Storage component has issues but is accessible",
                        "issues": validation_result.issues
                    }
        except Exception as e:
            return "unhealthy", {"error": str(e)}

    def _check_retrieval_component(self) -> tuple[str, Dict[str, Any]]:
        """
        Check the health of the retrieval component

        Returns:
            Tuple of (status, details)
        """
        try:
            # Test a simple retrieval operation
            # Use a simple vector for testing
            test_vector = [0.1] * 10  # Simple test vector

            # Perform a quick search to test retrieval
            search_results = self.client.search(
                collection_name=self.config.collection_name,
                query_vector=test_vector,
                limit=1
            )

            # If we get results or at least no error, retrieval is working
            return "healthy", {
                "message": "Retrieval component is functional",
                "test_query_results": len(search_results)
            }
        except Exception as e:
            return "unhealthy", {"error": str(e)}

    def perform_health_check(self) -> Dict[str, Any]:
        """
        Perform a comprehensive health check of all pipeline components

        Returns:
            Dictionary with health check results
        """
        start_time = time.perf_counter()

        components = ["extraction", "embedding", "storage", "retrieval"]
        component_health = {}

        for component in components:
            component_health[component] = self.check_component_status(component)

        total_response_time = time.perf_counter() - start_time

        # Determine overall health status
        statuses = [health.status for health in component_health.values()]
        if "unhealthy" in statuses:
            overall_status = "unhealthy"
        elif "degraded" in statuses:
            overall_status = "degraded"
        else:
            overall_status = "healthy"

        return {
            "overall_status": overall_status,
            "timestamp": time.time(),
            "total_response_time": total_response_time,
            "within_threshold": total_response_time < 30.0,  # T048: Health check timing under 30 seconds
            "components": {name: {
                "status": health.status,
                "response_time": health.response_time,
                "details": health.details
            } for name, health in component_health.items()}
        }

    def get_health_report(self) -> str:
        """
        Get a formatted health report as a string

        Returns:
            Formatted health report string
        """
        health_check = self.perform_health_check()

        report_lines = [
            "Pipeline Health Report",
            "=" * 30,
            f"Overall Status: {health_check['overall_status']}",
            f"Total Response Time: {health_check['total_response_time']:.2f}s",
            f"Completed Within 30s Threshold: {'Yes' if health_check['within_threshold'] else 'No'}",
            "",
            "Component Statuses:"
        ]

        for component, details in health_check['components'].items():
            report_lines.append(f"  {component.title()}: {details['status']}")
            report_lines.append(f"    Response Time: {details['response_time']:.3f}s")
            if details['details']:
                report_lines.append(f"    Details: {details['details']}")

        return "\n".join(report_lines)

    def monitor_extraction_component(self) -> ComponentHealth:
        """
        T044: Implement extraction component monitoring
        """
        return self.check_component_status("extraction")

    def monitor_embedding_component(self) -> ComponentHealth:
        """
        T045: Implement embedding component monitoring
        """
        return self.check_component_status("embedding")

    def monitor_storage_component(self) -> ComponentHealth:
        """
        T046: Implement storage component monitoring
        """
        return self.check_component_status("storage")

    def monitor_retrieval_component(self) -> ComponentHealth:
        """
        T047: Implement retrieval component monitoring
        """
        return self.check_component_status("retrieval")

    def implement_health_check_timing(self) -> Dict[str, Any]:
        """
        T048: Implement health check timing (under 30 seconds)
        """
        health_check = self.perform_health_check()

        # Ensure health check completes under 30 seconds as per requirement
        if health_check['total_response_time'] > 30.0:
            logging.warning(f"Health check exceeded 30-second threshold: {health_check['total_response_time']:.2f}s")

        return health_check