"""Explicit model assumptions, not claims about host runtime or established physics.

One *successful oracle call* costs one model operation and zero simulated ticks.
This does not reduce its host work, remove resource limits, or define a collapse.
The physical candidate model and its identity remain unchanged.
"""

from typing import Final, NamedTuple

QUANTUM_MODEL_ID: Final = "deferred-unit-cost-oracle-v1"


class OracleCost(NamedTuple):
    """Immutable, fixed-size cost in the user's simulated-world cost model."""

    model_units: int
    world_ticks: int


ORACLE_COST: Final = OracleCost(model_units=1, world_ticks=0)
