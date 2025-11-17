"""Tracing utilities for agent observability."""

import time
import asyncio
from typing import Dict, Any, Optional
from functools import wraps


class TraceContext:
    """Context manager for tracing agent operations."""

    def __init__(self, operation_name: str, metadata: Optional[Dict[str, Any]] = None):
        self.operation_name = operation_name
        self.metadata = metadata or {}
        self.start_time = None
        self.end_time = None

    def __enter__(self):
        self.start_time = time.time()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.end_time = time.time()
        duration = self.end_time - self.start_time
        self.metadata["duration_seconds"] = duration
        self.metadata["success"] = exc_type is None
        return False

    def to_dict(self) -> Dict[str, Any]:
        """Convert trace to dictionary."""
        return {
            "operation": self.operation_name,
            "start_time": self.start_time,
            "end_time": self.end_time,
            "duration": self.end_time - self.start_time if self.end_time else None,
            **self.metadata,
        }


def trace_operation(operation_name: Optional[str] = None):
    """Decorator to trace function execution.

    Args:
        operation_name: Optional operation name (uses function name if not provided)
    """
    def decorator(func):
        @wraps(func)
        async def async_wrapper(*args, **kwargs):
            name = operation_name or func.__name__
            with TraceContext(name) as trace:
                try:
                    result = await func(*args, **kwargs)
                    trace.metadata["result_type"] = type(result).__name__
                    return result
                except Exception as e:
                    trace.metadata["error"] = str(e)
                    raise

        @wraps(func)
        def sync_wrapper(*args, **kwargs):
            name = operation_name or func.__name__
            with TraceContext(name) as trace:
                try:
                    result = func(*args, **kwargs)
                    trace.metadata["result_type"] = type(result).__name__
                    return result
                except Exception as e:
                    trace.metadata["error"] = str(e)
                    raise

        if asyncio.iscoroutinefunction(func):
            return async_wrapper
        else:
            return sync_wrapper

    return decorator


def log_trace(trace: TraceContext, logger: Optional[Any] = None):
    """Log a trace context.

    Args:
        trace: TraceContext instance
        logger: Optional logger instance
    """
    if logger:
        logger.info(f"Trace: {trace.to_dict()}")
    else:
        import logging
        logging.info(f"Trace: {trace.to_dict()}")

