"""
CLI interface for Qdrant Retrieval Pipeline Testing

This module provides a command-line interface for testing the retrieval pipeline.
"""

import argparse
import json
import logging
import sys
from typing import List, Dict, Any, Optional

from backend.retrieve import QdrantRetriever
from backend.config.qdrant_config import QdrantConfig
from backend.monitor.health_monitor import HealthMonitor
from backend.utils.performance import PerformanceTimer


class RetrieveCLI:
    """
    Command-line interface for the Qdrant retrieval pipeline testing
    """
    def __init__(self):
        self.retriever = None
        self.health_monitor = None

    def setup_logging(self, verbose: bool = False):
        """
        Set up logging based on verbosity level

        Args:
            verbose: If True, use DEBUG level; otherwise INFO
        """
        level = logging.DEBUG if verbose else logging.INFO
        logging.basicConfig(
            level=level,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )

    def initialize_retriever(self, config: QdrantConfig = None):
        """
        Initialize the QdrantRetriever with configuration

        Args:
            config: Optional QdrantConfig instance
        """
        try:
            self.retriever = QdrantRetriever(config)
            logging.info("QdrantRetriever initialized successfully")
        except Exception as e:
            logging.error(f"Failed to initialize QdrantRetriever: {e}")
            raise

    def initialize_health_monitor(self, config: QdrantConfig = None):
        """
        Initialize the HealthMonitor with configuration

        Args:
            config: Optional QdrantConfig instance
        """
        try:
            self.health_monitor = HealthMonitor(config)
            logging.info("HealthMonitor initialized successfully")
        except Exception as e:
            logging.error(f"Failed to initialize HealthMonitor: {e}")
            raise

    def search_command(self, args: argparse.Namespace):
        """
        Handle the search command

        Args:
            args: Parsed command-line arguments
        """
        if not self.retriever:
            config = self._get_config_from_args(args)
            self.initialize_retriever(config)

        try:
            # Parse query vector from arguments
            query_vector = self._parse_vector(args.query_vector)

            # Parse query filter if provided
            query_filter = None
            if args.query_filter:
                query_filter = json.loads(args.query_filter)

            # Perform search
            results = self.retriever.search(
                query_vector=query_vector,
                top_k=args.top_k,
                query_filter=query_filter
            )

            # Output results
            if args.json_output:
                print(json.dumps(results, indent=2))
            else:
                print(f"Found {len(results)} similar embeddings:")
                for i, result in enumerate(results, 1):
                    print(f"  {i}. ID: {result['id']}, Score: {result['score']:.3f}")
                    if args.verbose_payload:
                        print(f"     Payload: {result['payload']}")

        except Exception as e:
            logging.error(f"Search command failed: {e}")
            if args.json_output:
                print(json.dumps({"error": str(e)}))
            else:
                print(f"Error: {e}")
            sys.exit(1)

    def validate_command(self, args: argparse.Namespace):
        """
        Handle the validate pipeline command

        Args:
            args: Parsed command-line arguments
        """
        if not self.retriever:
            config = self._get_config_from_args(args)
            self.initialize_retriever(config)

        try:
            # Parse query vector from arguments
            query_vector = self._parse_vector(args.query_vector)

            # Parse expected IDs
            expected_ids = args.expected_ids.split(',') if args.expected_ids else []

            # Perform pipeline validation
            validation_result = self.retriever.validate_pipeline(
                query_text=args.query_text,
                expected_ids=expected_ids,
                query_vector=query_vector,
                top_k=args.top_k
            )

            # Output results
            if args.json_output:
                print(json.dumps(validation_result, indent=2))
            else:
                print(f"Pipeline Validation Results:")
                print(f"  Query: {validation_result['query_text']}")
                print(f"  Expected IDs: {validation_result['expected_ids']}")
                print(f"  Retrieved IDs: {validation_result['retrieved_ids']}")
                print(f"  Accuracy: {validation_result['accuracy_score']:.2%}")
                print(f"  Response Time: {validation_result['response_time']:.3f}s")
                print(f"  Validation Passed: {validation_result['validation_passed']}")

                if validation_result['details']['missing_ids']:
                    print(f"  Missing IDs: {validation_result['details']['missing_ids']}")
                if validation_result['details']['extra_ids']:
                    print(f"  Extra IDs: {validation_result['details']['extra_ids']}")

        except Exception as e:
            logging.error(f"Validate command failed: {e}")
            if args.json_output:
                print(json.dumps({"error": str(e)}))
            else:
                print(f"Error: {e}")
            sys.exit(1)

    def health_command(self, args: argparse.Namespace):
        """
        Handle the health check command

        Args:
            args: Parsed command-line arguments
        """
        if not self.health_monitor:
            config = self._get_config_from_args(args)
            self.initialize_health_monitor(config)

        try:
            # Perform health check
            if args.component:
                # Check specific component
                health_result = self.health_monitor.check_component_status(args.component)

                if args.json_output:
                    result_dict = {
                        'name': health_result.name,
                        'status': health_result.status,
                        'response_time': health_result.response_time,
                        'details': health_result.details
                    }
                    print(json.dumps(result_dict, indent=2))
                else:
                    print(f"Component: {health_result.name}")
                    print(f"Status: {health_result.status}")
                    print(f"Response Time: {health_result.response_time:.3f}s")
                    print(f"Details: {health_result.details}")
            else:
                # Check all components
                health_result = self.health_monitor.perform_health_check()

                if args.json_output:
                    print(json.dumps(health_result, indent=2))
                else:
                    print(f"Overall Status: {health_result['overall_status']}")
                    print(f"Total Response Time: {health_result['total_response_time']:.3f}s")
                    print(f"Within 30s Threshold: {health_result['within_threshold']}")
                    print("\nComponent Statuses:")
                    for component, details in health_result['components'].items():
                        print(f"  {component.title()}: {details['status']}")
                        print(f"    Response Time: {details['response_time']:.3f}s")

        except Exception as e:
            logging.error(f"Health command failed: {e}")
            if args.json_output:
                print(json.dumps({"error": str(e)}))
            else:
                print(f"Error: {e}")
            sys.exit(1)

    def benchmark_command(self, args: argparse.Namespace):
        """
        Handle the benchmark command

        Args:
            args: Parsed command-line arguments
        """
        try:
            from backend.performance.benchmarks import PerformanceBenchmark

            config = self._get_config_from_args(args)
            benchmark = PerformanceBenchmark(config)

            if args.operation == "search":
                result = benchmark.run_search_benchmark(
                    iterations=args.iterations,
                    top_k=args.top_k
                )
            elif args.operation == "validation":
                result = benchmark.run_pipeline_validation_benchmark(
                    iterations=args.iterations
                )
            elif args.operation == "response_time":
                result = benchmark.run_response_time_monitoring_benchmark(
                    iterations=args.iterations
                )
            else:
                raise ValueError(f"Unknown benchmark operation: {args.operation}")

            # Output results
            if args.json_output:
                result_dict = {
                    'operation': result.operation,
                    'iterations': result.iterations,
                    'total_time': result.total_time,
                    'avg_time': result.avg_time,
                    'min_time': result.min_time,
                    'max_time': result.max_time,
                    'median_time': result.median_time,
                    'p95_time': result.p95_time,
                    'p99_time': result.p99_time,
                    'throughput': result.throughput,
                    'successful_ops': result.successful_ops,
                    'failed_ops': result.failed_ops
                }
                print(json.dumps(result_dict, indent=2))
            else:
                print(f"Benchmark Results for {result.operation}:")
                print(f"  Iterations: {result.iterations}")
                print(f"  Successful: {result.successful_ops}")
                print(f"  Failed: {result.failed_ops}")
                print(f"  Total Time: {result.total_time:.4f}s")
                print(f"  Avg Response Time: {result.avg_time:.4f}s")
                print(f"  Min Response Time: {result.min_time:.4f}s")
                print(f"  Max Response Time: {result.max_time:.4f}s")
                print(f"  Median Response Time: {result.median_time:.4f}s")
                print(f"  95th Percentile: {result.p95_time:.4f}s")
                print(f"  99th Percentile: {result.p99_time:.4f}s")
                print(f"  Throughput: {result.throughput:.2f} ops/sec")

        except Exception as e:
            logging.error(f"Benchmark command failed: {e}")
            if args.json_output:
                print(json.dumps({"error": str(e)}))
            else:
                print(f"Error: {e}")
            sys.exit(1)

    def _get_config_from_args(self, args: argparse.Namespace) -> Optional[QdrantConfig]:
        """
        Create QdrantConfig from command-line arguments

        Args:
            args: Parsed command-line arguments

        Returns:
            QdrantConfig instance or None if no args provided
        """
        config_params = {}

        if hasattr(args, 'host') and args.host:
            config_params['host'] = args.host
        if hasattr(args, 'port') and args.port:
            config_params['port'] = args.port
        if hasattr(args, 'api_key') and args.api_key:
            config_params['api_key'] = args.api_key
        if hasattr(args, 'collection_name') and args.collection_name:
            config_params['collection_name'] = args.collection_name

        if config_params:
            return QdrantConfig(**config_params)
        else:
            return None

    def _parse_vector(self, vector_str: str) -> List[float]:
        """
        Parse a string representation of a vector into a list of floats

        Args:
            vector_str: String representation of a vector (e.g., "0.1,0.2,0.3" or "[0.1,0.2,0.3]")

        Returns:
            List of floats representing the vector
        """
        # Remove brackets if present
        vector_str = vector_str.strip().strip('[]')

        # Split by comma and convert to floats
        try:
            vector = [float(x.strip()) for x in vector_str.split(',')]
            return vector
        except ValueError:
            raise ValueError(f"Invalid vector format: {vector_str}. Use format like '0.1,0.2,0.3'")

    def create_parser(self) -> argparse.ArgumentParser:
        """
        Create the argument parser for the CLI

        Returns:
            Configured ArgumentParser instance
        """
        parser = argparse.ArgumentParser(
            description="Qdrant Retrieval Pipeline Testing CLI",
            formatter_class=argparse.RawDescriptionHelpFormatter,
            epilog="""
Examples:
  # Search for similar embeddings
  python -m backend.cli.retrieve_cli search --query_vector "0.1,0.2,0.3,0.4,0.5" --top_k 5

  # Validate pipeline with expected results
  python -m backend.cli.retrieve_cli validate --query_text "Test query" --query_vector "0.5,0.4,0.3,0.2,0.1" --expected_ids "doc1,doc2,doc3"

  # Check health of all components
  python -m backend.cli.retrieve_cli health

  # Run search benchmark
  python -m backend.cli.retrieve_cli benchmark --operation search --iterations 100
            """
        )

        parser.add_argument(
            '--verbose', '-v',
            action='store_true',
            help='Enable verbose logging'
        )

        parser.add_argument(
            '--json-output',
            action='store_true',
            help='Output results in JSON format'
        )

        # Qdrant configuration arguments
        config_group = parser.add_argument_group('Qdrant Configuration')
        config_group.add_argument(
            '--host',
            type=str,
            help='Qdrant host (default: from environment)'
        )
        config_group.add_argument(
            '--port',
            type=int,
            help='Qdrant port (default: from environment)'
        )
        config_group.add_argument(
            '--api-key',
            dest='api_key',
            type=str,
            help='Qdrant API key (default: from environment)'
        )
        config_group.add_argument(
            '--collection-name',
            dest='collection_name',
            type=str,
            help='Qdrant collection name (default: from environment)'
        )

        subparsers = parser.add_subparsers(dest='command', help='Available commands')

        # Search command
        search_parser = subparsers.add_parser('search', help='Perform similarity search')
        search_parser.add_argument(
            '--query-vector', '-q',
            type=str,
            required=True,
            help='Query vector as comma-separated values (e.g., "0.1,0.2,0.3")'
        )
        search_parser.add_argument(
            '--top-k',
            type=int,
            default=5,
            help='Number of results to return (default: 5)'
        )
        search_parser.add_argument(
            '--query-filter',
            type=str,
            help='Query filter as JSON string (e.g., \'{"field": {"$eq": "value"}}\')'
        )
        search_parser.add_argument(
            '--verbose-payload',
            action='store_true',
            help='Show full payload in results'
        )
        search_parser.set_defaults(func=self.search_command)

        # Validate command
        validate_parser = subparsers.add_parser('validate', help='Validate pipeline')
        validate_parser.add_argument(
            '--query-text',
            type=str,
            required=True,
            help='Query text for validation'
        )
        validate_parser.add_argument(
            '--query-vector', '-q',
            type=str,
            required=True,
            help='Query vector as comma-separated values (e.g., "0.1,0.2,0.3")'
        )
        validate_parser.add_argument(
            '--expected-ids',
            type=str,
            help='Expected IDs as comma-separated values (e.g., "doc1,doc2,doc3")'
        )
        validate_parser.add_argument(
            '--top-k',
            type=int,
            default=5,
            help='Number of results to return for validation (default: 5)'
        )
        validate_parser.set_defaults(func=self.validate_command)

        # Health command
        health_parser = subparsers.add_parser('health', help='Check system health')
        health_parser.add_argument(
            '--component',
            type=str,
            choices=['extraction', 'embedding', 'storage', 'retrieval'],
            help='Check specific component health'
        )
        health_parser.set_defaults(func=self.health_command)

        # Benchmark command
        benchmark_parser = subparsers.add_parser('benchmark', help='Run performance benchmarks')
        benchmark_parser.add_argument(
            '--operation',
            type=str,
            choices=['search', 'validation', 'response_time'],
            default='search',
            help='Operation to benchmark (default: search)'
        )
        benchmark_parser.add_argument(
            '--iterations',
            type=int,
            default=50,
            help='Number of iterations to run (default: 50)'
        )
        benchmark_parser.add_argument(
            '--top-k',
            type=int,
            default=5,
            help='Top-k value for search operations (default: 5)'
        )
        benchmark_parser.set_defaults(func=self.benchmark_command)

        return parser

    def run(self, args: List[str] = None):
        """
        Run the CLI with the provided arguments

        Args:
            args: List of arguments (if None, use sys.argv)
        """
        parser = self.create_parser()
        parsed_args = parser.parse_args(args)

        # Set up logging
        self.setup_logging(parsed_args.verbose)

        if hasattr(parsed_args, 'func'):
            parsed_args.func(parsed_args)
        else:
            parser.print_help()


def main():
    """
    Main entry point for the CLI
    """
    cli = RetrieveCLI()
    cli.run()


if __name__ == "__main__":
    main()