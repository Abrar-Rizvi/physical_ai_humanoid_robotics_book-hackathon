"""
Performance measurement utilities for Qdrant Retrieval Pipeline Testing

This module provides utilities for measuring and tracking performance metrics.
"""

import time
import functools
from typing import Callable, Any, Dict
from contextlib import contextmanager


class PerformanceTimer:
    """
    A utility class for measuring execution time of operations
    """
    def __init__(self):
        self.start_time = None
        self.end_time = None

    def start(self):
        """
        Start the timer
        """
        self.start_time = time.perf_counter()

    def stop(self):
        """
        Stop the timer
        """
        self.end_time = time.perf_counter()

    @property
    def elapsed_time(self) -> float:
        """
        Get the elapsed time in seconds
        """
        if self.start_time is None:
            return 0.0
        if self.end_time is None:
            return time.perf_counter() - self.start_time
        return self.end_time - self.start_time

    def elapsed_ms(self) -> float:
        """
        Get the elapsed time in milliseconds
        """
        return self.elapsed_time * 1000


@contextmanager
def timer():
    """
    Context manager for timing code blocks
    """
    perf_timer = PerformanceTimer()
    perf_timer.start()
    try:
        yield perf_timer
    finally:
        perf_timer.stop()


def time_function(func: Callable) -> Callable:
    """
    Decorator to time function execution
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.perf_counter()
        result = func(*args, **kwargs)
        end_time = time.perf_counter()
        elapsed = end_time - start_time

        print(f"Function {func.__name__} took {elapsed:.4f}s to execute")
        return result

    return wrapper


class PerformanceTracker:
    """
    A utility class for tracking performance metrics
    """
    def __init__(self):
        self.metrics: Dict[str, list] = {}

    def record_metric(self, name: str, value: float):
        """
        Record a performance metric

        Args:
            name: Name of the metric
            value: Value of the metric
        """
        if name not in self.metrics:
            self.metrics[name] = []
        self.metrics[name].append(value)

    def get_average(self, name: str) -> float:
        """
        Get the average value for a metric

        Args:
            name: Name of the metric

        Returns:
            Average value of the metric
        """
        if name not in self.metrics or not self.metrics[name]:
            return 0.0
        return sum(self.metrics[name]) / len(self.metrics[name])

    def get_min(self, name: str) -> float:
        """
        Get the minimum value for a metric

        Args:
            name: Name of the metric

        Returns:
            Minimum value of the metric
        """
        if name not in self.metrics or not self.metrics[name]:
            return 0.0
        return min(self.metrics[name])

    def get_max(self, name: str) -> float:
        """
        Get the maximum value for a metric

        Args:
            name: Name of the metric

        Returns:
            Maximum value of the metric
        """
        if name not in self.metrics or not self.metrics[name]:
            return 0.0
        return max(self.metrics[name])

    def get_stats(self, name: str) -> Dict[str, float]:
        """
        Get statistics for a metric

        Args:
            name: Name of the metric

        Returns:
            Dictionary with average, min, max, and count
        """
        if name not in self.metrics or not self.metrics[name]:
            return {"average": 0.0, "min": 0.0, "max": 0.0, "count": 0}

        values = self.metrics[name]
        return {
            "average": sum(values) / len(values),
            "min": min(values),
            "max": max(values),
            "count": len(values)
        }

    def reset(self):
        """
        Reset all metrics
        """
        self.metrics = {}


# Global performance tracker instance
global_tracker = PerformanceTracker()


def track_performance(metric_name: str):
    """
    Decorator to track performance of a function

    Args:
        metric_name: Name of the metric to track
    """
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            start_time = time.perf_counter()
            result = func(*args, **kwargs)
            end_time = time.perf_counter()
            elapsed = end_time - start_time

            global_tracker.record_metric(metric_name, elapsed)
            return result

        return wrapper
    return decorator


def validate_response_time_threshold(response_time: float, threshold: float = 2.0) -> bool:
    """
    Validate that response time is within threshold

    Args:
        response_time: Response time in seconds
        threshold: Maximum allowed response time in seconds (default 2.0s)

    Returns:
        True if response time is within threshold, False otherwise
    """
    return response_time <= threshold


def validate_throughput(operations: int, time_taken: float, threshold_ops_per_sec: float = 1.0) -> bool:
    """
    Validate that throughput meets threshold

    Args:
        operations: Number of operations completed
        time_taken: Time taken in seconds
        threshold_ops_per_sec: Minimum operations per second threshold

    Returns:
        True if throughput meets threshold, False otherwise
    """
    if time_taken <= 0:
        return False

    actual_throughput = operations / time_taken
    return actual_throughput >= threshold_ops_per_sec


def format_time(seconds: float) -> str:
    """
    Format time in seconds to a human-readable string

    Args:
        seconds: Time in seconds

    Returns:
        Formatted time string
    """
    if seconds < 1e-6:
        return f"{seconds * 1e9:.2f} ns"
    elif seconds < 1e-3:
        return f"{seconds * 1e6:.2f} µs"
    elif seconds < 1:
        return f"{seconds * 1e3:.2f} ms"
    else:
        return f"{seconds:.4f} s"