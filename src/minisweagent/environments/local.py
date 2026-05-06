"""
Local execution environment for AI Code Agent System.

This module provides a local shell environment for executing commands.
It supports resource limits, command history tracking, and enhanced error handling
for robust agent operation in development and production scenarios.
"""

import os
import platform
import subprocess
import time
from typing import Any, Optional
from dataclasses import dataclass, field

from pydantic import BaseModel

from minisweagent.exceptions import Submitted
from minisweagent.utils.serialize import recursive_merge


@dataclass
class CommandExecution:
    """Track individual command execution details."""
    command: str
    returncode: int
    duration: float
    timestamp: float = field(default_factory=time.time)
    output_length: int = 0


class LocalEnvironmentConfig(BaseModel):
    """Configuration for local execution environment with advanced options."""

    cwd: str = ""
    env: dict[str, str] = {}
    timeout: int = 30

    # Resource limits for safety
    max_output_size: int = 10 * 1024 * 1024  # 10MB max output
    allowed_commands: list[str] = []  # Empty means all commands allowed
    blocked_commands: list[str] = ["rm -rf /", "format", "mkfs"]  # Safety blocklist

    # Execution tracking
    track_history: bool = True
    max_history_size: int = 1000

    # Performance optimization
    use_cache: bool = False
    cache_ttl: int = 300  # 5 minutes


class LocalEnvironment:
    """
    Local execution environment that runs bash commands on the host machine.

    Features:
    - Resource limiting (output size, timeout)
    - Command history tracking
    - Security controls (allowed/blocked commands)
    - Enhanced error handling and logging
    """

    def __init__(self, *, config_class: type = LocalEnvironmentConfig, **kwargs):
        """Initialize local environment with configuration."""
        self.config = config_class(**kwargs)
        self.command_history: list[CommandExecution] = []
        self.execution_count: int = 0
        self.total_execution_time: float = 0.0

    def execute(self, action: dict, cwd: str = "", *, timeout: int | None = None) -> dict[str, Any]:
        """
        Execute a command in the local environment with safety checks.

        Args:
            action: Dict containing 'command' key with the command to execute
            cwd: Working directory override
            timeout: Timeout override in seconds

        Returns:
            Dict with 'output', 'returncode', and optional 'exception_info'
        """
        start_time = time.time()
        command = action.get("command", "")
        cwd = cwd or self.config.cwd or os.getcwd()

        # Security check
        if not self._is_command_allowed(command):
            return {
                "output": "",
                "returncode": -1,
                "exception_info": f"Command blocked by security policy: {command[:50]}",
            }

        try:
            result = subprocess.run(
                command,
                shell=True,
                text=True,
                cwd=cwd,
                env=os.environ | self.config.env,
                timeout=timeout or self.config.timeout,
                encoding="utf-8",
                errors="replace",
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
            )

            # Truncate output if exceeds limit
            output = result.stdout
            if len(output) > self.config.max_output_size:
                output = output[:self.config.max_output_size] + f"\n... [Output truncated, exceeded {self.config.max_output_size} bytes]"

            exec_result = {"output": output, "returncode": result.returncode, "exception_info": ""}

            # Track execution
            duration = time.time() - start_time
            self._track_command(command, result.returncode, duration, len(output))

        except subprocess.TimeoutExpired as e:
            exec_result = {
                "output": f"Command timed out after {timeout or self.config.timeout} seconds",
                "returncode": -1,
                "exception_info": f"Timeout error: {str(e)}",
                "extra": {"exception_type": "TimeoutExpired"},
            }
            self._track_command(command, -1, time.time() - start_time, 0)
        except Exception as e:
            raw_output = getattr(e, "output", None)
            raw_output = (
                raw_output.decode("utf-8", errors="replace") if isinstance(raw_output, bytes) else (raw_output or "")
            )
            exec_result = {
                "output": raw_output,
                "returncode": -1,
                "exception_info": f"An error occurred while executing the command: {e}",
                "extra": {"exception_type": type(e).__name__, "exception": str(e)},
            }
            self._track_command(command, -1, time.time() - start_time, len(raw_output))

        self._check_finished(exec_result)
        return exec_result

    def _is_command_allowed(self, command: str) -> bool:
        """Check if command passes security policy."""
        cmd_lower = command.lower().strip()

        # Check blocked commands
        for blocked in self.config.blocked_commands:
            if blocked.lower() in cmd_lower:
                return False

        # Check allowed commands (if specified)
        if self.config.allowed_commands:
            return any(allowed in cmd_lower for allowed in self.config.allowed_commands)

        return True

    def _track_command(self, command: str, returncode: int, duration: float, output_len: int) -> None:
        """Record command execution in history."""
        if not self.config.track_history:
            return

        self.execution_count += 1
        self.total_execution_time += duration

        execution = CommandExecution(
            command=command[:200],  # Truncate long commands
            returncode=returncode,
            duration=duration,
            output_length=output_len,
        )

        self.command_history.append(execution)

        # Trim history if too large
        if len(self.command_history) > self.config.max_history_size:
            self.command_history = self.command_history[-self.config.max_history_size:]

    def get_stats(self) -> dict:
        """Get execution statistics."""
        return {
            "total_executions": self.execution_count,
            "total_time": round(self.total_execution_time, 2),
            "avg_time": round(self.total_execution_time / max(1, self.execution_count), 3),
            "history_size": len(self.command_history),
            "success_rate": sum(1 for c in self.command_history if c.returncode == 0) / max(1, len(self.command_history)),
        }

    def _check_finished(self, output: dict):
        """Raises Submitted if the output indicates task completion."""
        lines = output.get("output", "").lstrip().splitlines(keepends=True)
        if lines and lines[0].strip() == "COMPLETE_TASK_AND_SUBMIT_FINAL_OUTPUT" and output["returncode"] == 0:
            submission = "".join(lines[1:])
            raise Submitted(
                {
                    "role": "exit",
                    "content": submission,
                    "extra": {"exit_status": "Submitted", "submission": submission},
                }
            )

    def get_template_vars(self, **kwargs) -> dict[str, Any]:
        return recursive_merge(self.config.model_dump(), platform.uname()._asdict(), os.environ, kwargs)

    def serialize(self) -> dict:
        return {
            "info": {
                "config": {
                    "environment": self.config.model_dump(mode="json"),
                    "environment_type": f"{self.__class__.__module__}.{self.__class__.__name__}",
                }
            }
        }
