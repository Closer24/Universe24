"""Generic local disturbance simulation defined by initialization data."""

from importlib import import_module
from typing import Any

from .core.disturbance_state import InitialState
from .disturbance_api import Simulation

__version__ = "0.2.0"
__all__ = ["InitialState", "Simulation", "load_initial_state", "__version__"]


def __getattr__(name: str) -> Any:
    """Load the initialization parser on demand, keeping the package import light."""
    modules = {"load_initial_state": ".initialization"}
    if name not in modules:
        raise AttributeError(name)
    return getattr(import_module(modules[name], __name__), name)
