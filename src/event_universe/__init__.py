"""Integer, local, three-dimensional event-field research simulator."""

from .api import LinkedSimulation, SharedActionSimulation, Simulation
from .core.links import LinkConfig
from .core.state import CellState, Config, ParticleState
from .models.shared_action import SharedActionConfig

__version__ = "0.1.0"
__all__ = [
    "CellState",
    "Config",
    "ParticleState",
    "Simulation",
    "SharedActionSimulation",
    "SharedActionConfig",
    "LinkedSimulation",
    "LinkConfig",
    "__version__",
]
