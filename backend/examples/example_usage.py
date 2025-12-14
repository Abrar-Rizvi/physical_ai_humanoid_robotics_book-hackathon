"""
Example usage of the Qdrant Retrieval Module

This file demonstrates how to use the Qdrant retrieval module for testing RAG pipelines.
"""

import logging
from backend.retrieve import QdrantRetriever
from backend.config.qdrant_config import QdrantConfig
from backend.monitor.health_monitor import HealthMonitor


def example_basic_search():
    """
    Example: Basic similarity search functionality
    """
    print("=== Basic Search Example ===")

    # Initialize the retriever with default config (from environment)
    retriever = QdrantRetriever()

    # Example query vector (in real usage, this would come from embedding a text query)
    query_vector = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]

    try:
        # Perform similarity search
        results = retriever.search(query_vector, top_k=3)

        print(f"Found {len(results)} similar embeddings:")
        for i, result in enumerate(results, 1):
            print(f"  {i}. ID: {result['id']}, Score: {result['score']:.3f}")

    except Exception as e:
        print(f"Search failed: {e}")


def example_pipeline_validation():
    """
    Example: Pipeline validation functionality
    """
    print("\n=== Pipeline Validation Example ===")

    # Initialize the retriever
    retriever = QdrantRetriever()

    # Example validation
    query_text = "Artificial intelligence and machine learning concepts"
    expected_ids = ["doc_001", "doc_002", "doc_003"]  # IDs we expect to retrieve
    query_vector = [0.8, 0.7, 0.6, 0.5, 0.4, 0.3, 0.2, 0.1, 0.9, 0.8]

    try:
        # Validate the pipeline
        validation_result = retriever.validate_pipeline(
            query_text=query_text,
            expected_ids=expected_ids,
            query_vector=query_vector,
            top_k=5
        )

        print(f"Query: {query_text}")
        print(f"Expected IDs: {expected_ids}")
        print(f"Retrieved IDs: {validation_result['retrieved_ids']}")
        print(f"Accuracy: {validation_result['accuracy_score']:.2%}")
        print(f"Response Time: {validation_result['response_time']:.3f}s")
        print(f"Validation Passed: {validation_result['validation_passed']}")

        if validation_result['details']['missing_ids']:
            print(f"Missing IDs: {validation_result['details']['missing_ids']}")
        if validation_result['details']['extra_ids']:
            print(f"Extra IDs: {validation_result['details']['extra_ids']}")

    except Exception as e:
        print(f"Pipeline validation failed: {e}")


def example_health_monitoring():
    """
    Example: Health monitoring functionality
    """
    print("\n=== Health Monitoring Example ===")

    # Initialize the health monitor
    monitor = HealthMonitor()

    try:
        # Perform health check
        health_result = monitor.perform_health_check()

        print(f"Overall Status: {health_result['overall_status']}")
        print(f"Total Response Time: {health_result['total_response_time']:.3f}s")
        print(f"Within 30s Threshold: {health_result['within_threshold']}")

        print("\nComponent Statuses:")
        for component, details in health_result['components'].items():
            print(f"  {component.title()}: {details['status']}")
            print(f"    Response Time: {details['response_time']:.3f}s")

        # Print detailed report
        print("\nDetailed Health Report:")
        print(monitor.get_health_report())

    except Exception as e:
        print(f"Health monitoring failed: {e}")


def example_response_time_measurement():
    """
    Example: Response time measurement functionality
    """
    print("\n=== Response Time Measurement Example ===")

    # Initialize the retriever
    retriever = QdrantRetriever()

    # Example query vector
    query_vector = [0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5]

    try:
        # Measure response time
        timing_result = retriever.measure_response_time(query_vector, top_k=2)

        print(f"Response Time: {timing_result['response_time']:.3f}s")
        print(f"Within 2s Threshold: {timing_result['within_threshold']}")
        print(f"Number of Results: {len(timing_result['results'])}")

    except Exception as e:
        print(f"Response time measurement failed: {e}")


def example_custom_configuration():
    """
    Example: Using custom configuration
    """
    print("\n=== Custom Configuration Example ===")

    # Create custom configuration
    config = QdrantConfig(
        host="localhost",
        port=6333,
        collection_name="my_collection",
        timeout=30
    )

    # Initialize retriever with custom config
    retriever = QdrantRetriever(config=config)

    try:
        # Get collection info
        info = retriever.get_collection_info()
        print(f"Collection Info: {info}")

    except Exception as e:
        print(f"Custom configuration example failed: {e}")


def main():
    """
    Main function to run all examples
    """
    # Set up logging
    logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

    print("Qdrant Retrieval Module - Usage Examples")
    print("=" * 50)

    # Run all examples
    example_basic_search()
    example_pipeline_validation()
    example_health_monitoring()
    example_response_time_measurement()
    example_custom_configuration()

    print("\nAll examples completed!")


if __name__ == "__main__":
    main()