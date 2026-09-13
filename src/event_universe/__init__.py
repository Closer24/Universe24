"""Generic local disturbance simulation, with explicit historical research APIs."""

from importlib import import_module
from typing import Any

from .core.disturbance_state import InitialState
from .disturbance_api import Simulation

__version__ = "0.2.0"
__all__ = ["InitialState", "Simulation", "load_initial_state", "__version__"]


def __getattr__(name: str) -> Any:
    """Load initialization or explicitly requested historical APIs on demand."""
    modules = {
        "load_initial_state": ".initialization",
        "ScalarSimulation": ".particle_api",
        "LinkedSimulation": ".particle_api",
        "BalancedSimulation": ".particle_api",
        "CausalStreamSimulation": ".particle_api",
        "Config": ".core.state",
        "NodeState": ".core.state",
        "ParticleState": ".core.state",
        "LinkConfig": ".core.links",
        "CausalStreamConfig": ".models.causal_stream",
    }
    if name not in modules:
        raise AttributeError(name)
    return getattr(import_module(modules[name], __name__), name)
