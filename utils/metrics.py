"""Metrics collection utilities."""

from typing import Dict, Any, List
from collections import defaultdict
import time


class MetricsCollector:
    """Simple metrics collector for agent operations."""

    def __init__(self):
        self.metrics: Dict[str, List[float]] = defaultdict(list)
        self.counts: Dict[str, int] = defaultdict(int)
        self.errors: Dict[str, int] = defaultdict(int)

    def record_timing(self, operation: str, duration: float):
        """Record timing metric.

        Args:
            operation: Operation name
            duration: Duration in seconds
        """
        self.metrics[f"{operation}_duration"].append(duration)
        self.counts[operation] += 1

    def record_error(self, operation: str):
        """Record error metric.

        Args:
            operation: Operation name
        """
        self.errors[operation] += 1

    def get_summary(self) -> Dict[str, Any]:
        """Get metrics summary.

        Returns:
            Dictionary with metrics summary
        """
        summary = {}

        for operation, durations in self.metrics.items():
            if durations:
                summary[operation] = {
                    "count": len(durations),
                    "min": min(durations),
                    "max": max(durations),
                    "avg": sum(durations) / len(durations),
                    "total": sum(durations),
                }

        summary["counts"] = dict(self.counts)
        summary["errors"] = dict(self.errors)

        return summary

    def reset(self):
        """Reset all metrics."""
        self.metrics.clear()
        self.counts.clear()
        self.errors.clear()


# Global metrics collector instance
metrics_collector = MetricsCollector()

