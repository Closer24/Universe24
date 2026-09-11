"""Reusable fixed-neighborhood field operations, independent of simulator models."""

from importlib import import_module
from typing import Any

__all__ = ["ScalarField", "ScalarFieldRule", "ScalarSample"]


def __getattr__(name: str) -> Any:
    """Load historical scalar interfaces only when explicitly requested."""
    if name not in __all__:
        raise AttributeError(name)
    return getattr(import_module(".scalar", __name__), name)
