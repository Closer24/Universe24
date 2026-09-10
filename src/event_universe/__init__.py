"""Integer, local, three-dimensional event-field research simulator."""

from .api import CausalStreamSimulation, LinkedSimulation, Simulation
from .core.links import LinkConfig
from .core.state import CellState, Config, ParticleState
from .models.causal_stream import CausalStreamConfig

__version__ = "0.1.0"
__all__ = [
    "CellState",
    "Config",
    "ParticleState",
    "Simulation",
    "CausalStreamSimulation",
    "CausalStreamConfig",
    "LinkedSimulation",
    "LinkConfig",
    "__version__",
]
