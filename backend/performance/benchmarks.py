"""
Performance benchmarks for Qdrant Retrieval Pipeline Testing

This module contains performance benchmarks to measure the efficiency
of the retrieval pipeline under various conditions.
"""

import time
import logging
from typing import List, Dict, Any
from dataclasses import dataclass
import statistics
from backend.retrieve import QdrantRetriever
from backend.config.qdrant_config import QdrantConfig
from backend.utils.performance import PerformanceTimer


@dataclass
class BenchmarkResult:
    """
    Data class to represent benchmark results
    """
    operation: str
    iterations: int
    total_time: float
    avg_time: float
    min_time: float
    max_time: float
    median_time: float
    p95_time: float
    p99_time: float
    throughput: float  # operations per second
    successful_ops: int
    failed_ops: int


class PerformanceBenchmark:
    """
    Class to run performance benchmarks on the retrieval pipeline
    """
    def __init__(self, config: QdrantConfig = None):
        """
        Initialize the performance benchmark with configuration

        Args:
            config: Optional QdrantConfig instance. If not provided, will use environment variables.
        """
        self.config = config or QdrantConfig.from_env()
        self.retriever = QdrantRetriever(self.config)

    def run_search_benchmark(self, iterations: int = 100, top_k: int = 5) -> BenchmarkResult:
        """
        Run benchmark for search operations

        Args:
            iterations: Number of iterations to run
            top_k: Number of results to return in each search

        Returns:
            BenchmarkResult with performance metrics
        """
        logging.info(f"Running search benchmark with {iterations} iterations, top_k={top_k}")

        times = []
        successful_ops = 0
        failed_ops = 0

        # Generate test query vectors
        test_vectors = self._generate_test_vectors(iterations, 10)  # 10-dimensional vectors

        for i in range(iterations):
            query_vector = test_vectors[i]

            timer = PerformanceTimer()
            timer.start()

            try:
                # Perform search operation
                results = self.retriever.search(query_vector, top_k=top_k)
                timer.stop()

                times.append(timer.elapsed_time)
                successful_ops += 1

                if i % 20 == 0:  # Log progress every 20 iterations
                    logging.info(f"Search benchmark: {i+1}/{iterations} completed")

            except Exception as e:
                timer.stop()
                times.append(timer.elapsed_time)  # Still record the time even if operation failed
                failed_ops += 1
                logging.warning(f"Search operation {i+1} failed: {e}")

        return self._calculate_benchmark_metrics("search", iterations, times, successful_ops, failed_ops)

    def run_pipeline_validation_benchmark(self, iterations: int = 50) -> BenchmarkResult:
        """
        Run benchmark for pipeline validation operations

        Args:
            iterations: Number of iterations to run

        Returns:
            BenchmarkResult with performance metrics
        """
        logging.info(f"Running pipeline validation benchmark with {iterations} iterations")

        times = []
        successful_ops = 0
        failed_ops = 0

        # Generate test data
        test_vectors = self._generate_test_vectors(iterations, 10)
        test_expected_ids = [[f'doc_{i}_{j}' for j in range(3)] for i in range(iterations)]

        for i in range(iterations):
            query_vector = test_vectors[i]
            expected_ids = test_expected_ids[i]
            query_text = f"Benchmark query {i}"

            timer = PerformanceTimer()
            timer.start()

            try:
                # Perform pipeline validation
                result = self.retriever.validate_pipeline(
                    query_text=query_text,
                    expected_ids=expected_ids,
                    query_vector=query_vector,
                    top_k=5
                )
                timer.stop()

                times.append(timer.elapsed_time)
                successful_ops += 1

                if i % 10 == 0:  # Log progress every 10 iterations
                    logging.info(f"Pipeline validation benchmark: {i+1}/{iterations} completed")

            except Exception as e:
                timer.stop()
                times.append(timer.elapsed_time)  # Still record the time even if operation failed
                failed_ops += 1
                logging.warning(f"Pipeline validation operation {i+1} failed: {e}")

        return self._calculate_benchmark_metrics("pipeline_validation", iterations, times, successful_ops, failed_ops)

    def run_concurrent_operations_benchmark(self, operation_type: str = "search",
                                          concurrent_ops: int = 10,
                                          per_operation: int = 10) -> List[BenchmarkResult]:
        """
        Run benchmark for concurrent operations

        Args:
            operation_type: Type of operation ('search' or 'validation')
            concurrent_ops: Number of concurrent operations to simulate
            per_operation: Number of iterations per concurrent operation

        Returns:
            List of BenchmarkResult with performance metrics for each concurrent operation
        """
        logging.info(f"Running concurrent {operation_type} benchmark with {concurrent_ops} concurrent operations, {per_operation} each")

        results = []
        test_vectors = self._generate_test_vectors(concurrent_ops * per_operation, 10)

        for i in range(concurrent_ops):
            # Get vectors for this concurrent operation
            start_idx = i * per_operation
            end_idx = start_idx + per_operation
            op_vectors = test_vectors[start_idx:end_idx]

            times = []
            successful_ops = 0
            failed_ops = 0

            for j, query_vector in enumerate(op_vectors):
                timer = PerformanceTimer()
                timer.start()

                try:
                    if operation_type == "search":
                        results_op = self.retriever.search(query_vector, top_k=5)
                    elif operation_type == "validation":
                        expected_ids = [f'doc_{i}_{j}_{k}' for k in range(3)]
                        validation_result = self.retriever.validate_pipeline(
                            f"Concurrent validation {i}-{j}",
                            expected_ids,
                            query_vector,
                            top_k=5
                        )
                    else:
                        raise ValueError(f"Unknown operation type: {operation_type}")

                    timer.stop()
                    times.append(timer.elapsed_time)
                    successful_ops += 1

                except Exception as e:
                    timer.stop()
                    times.append(timer.elapsed_time)
                    failed_ops += 1
                    logging.warning(f"Concurrent operation {i}, {j} failed: {e}")

            result = self._calculate_benchmark_metrics(
                f"concurrent_{operation_type}_{i}",
                per_operation,
                times,
                successful_ops,
                failed_ops
            )
            results.append(result)

        return results

    def run_response_time_monitoring_benchmark(self, iterations: int = 100) -> BenchmarkResult:
        """
        Run benchmark specifically for response time measurement functionality

        Args:
            iterations: Number of iterations to run

        Returns:
            BenchmarkResult with performance metrics
        """
        logging.info(f"Running response time monitoring benchmark with {iterations} iterations")

        times = []
        successful_ops = 0
        failed_ops = 0

        test_vectors = self._generate_test_vectors(iterations, 10)

        for i in range(iterations):
            query_vector = test_vectors[i]

            timer = PerformanceTimer()
            timer.start()

            try:
                # Test the response time measurement functionality
                result = self.retriever.measure_response_time(query_vector, top_k=3)
                timer.stop()

                times.append(result['response_time'])  # Use the measured response time
                successful_ops += 1

                if i % 20 == 0:  # Log progress every 20 iterations
                    logging.info(f"Response time monitoring benchmark: {i+1}/{iterations} completed")

            except Exception as e:
                timer.stop()
                times.append(timer.elapsed_time)
                failed_ops += 1
                logging.warning(f"Response time measurement operation {i+1} failed: {e}")

        return self._calculate_benchmark_metrics("response_time_measurement", iterations, times, successful_ops, failed_ops)

    def _generate_test_vectors(self, count: int, dimensions: int) -> List[List[float]]:
        """
        Generate test vectors for benchmarking

        Args:
            count: Number of vectors to generate
            dimensions: Number of dimensions for each vector

        Returns:
            List of test vectors
        """
        import random
        vectors = []
        for _ in range(count):
            vector = [random.random() for _ in range(dimensions)]
            vectors.append(vector)
        return vectors

    def _calculate_benchmark_metrics(self, operation: str, iterations: int, times: List[float],
                                   successful_ops: int, failed_ops: int) -> BenchmarkResult:
        """
        Calculate benchmark metrics from timing data

        Args:
            operation: Name of the operation being benchmarked
            iterations: Total number of iterations
            times: List of execution times
            successful_ops: Number of successful operations
            failed_ops: Number of failed operations

        Returns:
            BenchmarkResult with calculated metrics
        """
        if not times:
            return BenchmarkResult(
                operation=operation,
                iterations=iterations,
                total_time=0.0,
                avg_time=0.0,
                min_time=0.0,
                max_time=0.0,
                median_time=0.0,
                p95_time=0.0,
                p99_time=0.0,
                throughput=0.0,
                successful_ops=successful_ops,
                failed_ops=failed_ops
            )

        total_time = sum(times)
        avg_time = statistics.mean(times) if times else 0.0
        min_time = min(times) if times else 0.0
        max_time = max(times) if times else 0.0
        median_time = statistics.median(times) if times else 0.0

        # Calculate percentiles
        sorted_times = sorted(times)
        n = len(sorted_times)
        p95_idx = int(0.95 * n) - 1 if n > 0 else 0
        p99_idx = int(0.99 * n) - 1 if n > 0 else 0

        p95_time = sorted_times[min(p95_idx, n-1)] if n > 0 else 0.0
        p99_time = sorted_times[min(p99_idx, n-1)] if n > 0 else 0.0

        # Calculate throughput (operations per second)
        throughput = successful_ops / total_time if total_time > 0 else 0.0

        return BenchmarkResult(
            operation=operation,
            iterations=iterations,
            total_time=total_time,
            avg_time=avg_time,
            min_time=min_time,
            max_time=max_time,
            median_time=median_time,
            p95_time=p95_time,
            p99_time=p99_time,
            throughput=throughput,
            successful_ops=successful_ops,
            failed_ops=failed_ops
        )

    def run_all_benchmarks(self) -> Dict[str, Any]:
        """
        Run all benchmarks and return comprehensive results

        Returns:
            Dictionary with all benchmark results
        """
        logging.info("Starting comprehensive benchmark suite")

        results = {}

        # Run search benchmark
        logging.info("Running search benchmark...")
        results['search'] = self.run_search_benchmark(iterations=50, top_k=5)

        # Run pipeline validation benchmark
        logging.info("Running pipeline validation benchmark...")
        results['pipeline_validation'] = self.run_pipeline_validation_benchmark(iterations=25)

        # Run response time monitoring benchmark
        logging.info("Running response time monitoring benchmark...")
        results['response_time_monitoring'] = self.run_response_time_monitoring_benchmark(iterations=50)

        # Run concurrent operations benchmark for search
        logging.info("Running concurrent search benchmark...")
        results['concurrent_search'] = self.run_concurrent_operations_benchmark(
            operation_type="search",
            concurrent_ops=5,
            per_operation=10
        )

        # Run concurrent operations benchmark for validation
        logging.info("Running concurrent validation benchmark...")
        results['concurrent_validation'] = self.run_concurrent_operations_benchmark(
            operation_type="validation",
            concurrent_ops=3,
            per_operation=10
        )

        logging.info("All benchmarks completed")

        return results

    def print_benchmark_report(self, results: Dict[str, Any]):
        """
        Print a formatted benchmark report

        Args:
            results: Dictionary of benchmark results
        """
        print("\n" + "="*80)
        print("PERFORMANCE BENCHMARK REPORT")
        print("="*80)

        for test_name, result in results.items():
            if isinstance(result, list):  # Concurrent results
                print(f"\n{test_name.upper()} BENCHMARK:")
                print(f"  Total Operations: {sum(r.iterations for r in result)}")
                print(f"  Successful: {sum(r.successful_ops for r in result)}")
                print(f"  Failed: {sum(r.failed_ops for r in result)}")
                print(f"  Avg Response Time: {statistics.mean(r.avg_time for r in result):.4f}s")
                print(f"  Throughput: {sum(r.throughput for r in result):.2f} ops/sec")
            elif isinstance(result, BenchmarkResult):
                print(f"\n{test_name.upper()} BENCHMARK:")
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
            else:
                print(f"\n{test_name.upper()}: {result}")

        print("\n" + "="*80)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    # Run benchmarks
    benchmark = PerformanceBenchmark()
    results = benchmark.run_all_benchmarks()
    benchmark.print_benchmark_report(results)