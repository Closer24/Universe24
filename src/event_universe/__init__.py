"""Integer, local, three-dimensional event-field research simulator."""

from .api import LinkedSimulation, Simulation
from .core.links import LinkConfig
from .core.state import CellState, Config, ParticleState

__version__ = "0.1.0"
__all__ = [
    "CellState",
    "Config",
    "ParticleState",
    "Simulation",
    "LinkedSimulation",
    "LinkConfig",
    "__version__",
]
