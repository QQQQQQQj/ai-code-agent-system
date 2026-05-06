"""
Logging utilities for AI Code Agent System.

This module provides centralized logging configuration with support for:
- Rich console output with formatted messages
- File-based logging with timestamps
- Token usage tracking and cost monitoring
- Performance metrics logging
"""

import logging
import time
from pathlib import Path
from typing import Optional

from rich.logging import RichHandler


class TokenTracker:
    """Track token usage and costs for monitoring and optimization."""

    def __init__(self):
        self.total_tokens: int = 0
        self.total_cost: float = 0.0
        self.call_count: int = 0
        self.start_time: float = time.time()

    def record_call(self, tokens: int, cost: float) -> None:
        """Record a model API call with token usage and cost."""
        self.total_tokens += tokens
        self.total_cost += cost
        self.call_count += 1

    def get_stats(self) -> dict:
        """Get current usage statistics."""
        elapsed = time.time() - self.start_time
        return {
            "total_tokens": self.total_tokens,
            "total_cost": round(self.total_cost, 4),
            "call_count": self.call_count,
            "avg_tokens_per_call": self.total_tokens / max(1, self.call_count),
            "avg_cost_per_call": round(self.total_cost / max(1, self.call_count), 4),
            "elapsed_seconds": round(elapsed, 2),
            "tokens_per_second": round(self.total_tokens / max(1, elapsed), 2),
        }


# Global token tracker instance
token_tracker = TokenTracker()


def _setup_root_logger() -> None:
    """Initialize the root logger with Rich handler for console output."""
    logger = logging.getLogger("minisweagent")
    logger.setLevel(logging.DEBUG)
    _handler = RichHandler(
        show_path=False,
        show_time=False,
        show_level=False,
        markup=True,
    )
    _formatter = logging.Formatter("%(name)s: %(levelname)s: %(message)s")
    _handler.setFormatter(_formatter)
    logger.addHandler(_handler)


def add_file_handler(path: Path | str, level: int = logging.DEBUG, *, print_path: bool = True) -> None:
    """
    Add a file handler to the root logger.

    Args:
        path: Path to the log file
        level: Logging level (default: DEBUG)
        print_path: Whether to print the log path to console
    """
    logger = logging.getLogger("minisweagent")
    handler = logging.FileHandler(path)
    handler.setLevel(level)
    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    if print_path:
        print(f"Logging to '{path}'")


def log_token_usage(prompt_tokens: int, completion_tokens: int, cost: float) -> None:
    """
    Log token usage information for tracking and monitoring.

    Args:
        prompt_tokens: Number of tokens in the prompt
        completion_tokens: Number of tokens in the completion
        cost: Cost of the API call in USD
    """
    total = prompt_tokens + completion_tokens
    token_tracker.record_call(total, cost)

    logger = logging.getLogger("minisweagent.token_tracker")
    logger.debug(
        f"Token usage - Prompt: {prompt_tokens}, Completion: {completion_tokens}, "
        f"Total: {total}, Cost: ${cost:.4f}"
    )


_setup_root_logger()
logger = logging.getLogger("minisweagent")


__all__ = ["logger", "token_tracker", "log_token_usage"]
