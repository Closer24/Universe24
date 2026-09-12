"""Public assembly of the generic disturbance simulator."""

from event_universe.core.disturbance_engine import DisturbanceEngine, EventSink
from event_universe.core.disturbance_state import InitialState
from event_universe.fields.disturbances import DisturbanceLaw


class Simulation(DisturbanceEngine):
    """Run the fields, disturbances and integer laws supplied by initialization."""

    def __init__(self, initial: InitialState, *, observer: EventSink | None = None) -> None:
        super().__init__(
            initial,
            DisturbanceLaw(
                initial.fields,
                initial.disturbances,
                initial.couplings,
                initial.operation_costs,
                initial.interactions,
            ),
            observer,
        )
