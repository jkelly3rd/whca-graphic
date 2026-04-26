"""
Lightweight helpers for inspecting runtime memory usage.

Only relies on optional diagnostics tools. Callers should install the
``diagnostics`` extra (``uv sync --extra diagnostics``) or ``psutil``
individually before importing ``show_process_memory``.
"""

from __future__ import annotations

import os
from typing import Any

try:
    import psutil
except ImportError:  # pragma: no cover
    psutil = None  # type: ignore[assignment]


def show_process_memory(prefix: str | None = None) -> None:
    """
    Print RSS and virtual memory for the current Python process.

    Args:
        prefix: Optional label to prepend to the message.
    """
    if psutil is None:  # pragma: no cover
        raise ImportError(
            "psutil is required for show_process_memory. Install it via `uv sync --extra diagnostics`"
            " or `uv add psutil`."
        )

    process = psutil.Process(os.getpid())
    memory = process.memory_info()
    label = f"{prefix} " if prefix else ""
    print(
        f"{label}PID={process.pid} RSS={memory.rss / 1024**2:.1f} MB "
        f"VMS={memory.vms / 1024**2:.1f} MB"
    )


def dataframe_memory_mb(df: Any, deep: bool = True) -> float:
    """
    Estimate DataFrame memory usage in megabytes.

    Works with pandas (and polars via ``to_pandas`` beforehand).

    Args:
        df: Object exposing ``memory_usage`` (pandas DataFrame or Series).
        deep: Whether to account for full object references (pandas ``deep`` flag).

    Returns:
        Memory consumption in megabytes.
    """
    if not hasattr(df, "memory_usage"):
        raise TypeError("Expected a pandas-like object with a memory_usage method")

    memory_bytes = df.memory_usage(deep=deep)
    # pandas returns a Series for DataFrame memory_usage, scalars otherwise
    if hasattr(memory_bytes, "sum"):
        memory_bytes = memory_bytes.sum()
    return float(memory_bytes) / 1024**2


__all__ = ["show_process_memory", "dataframe_memory_mb"]
