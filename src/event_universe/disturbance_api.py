"""Public assembly of the generic disturbance simulator."""

from event_universe.core.disturbance_engine import DisturbanceEngine, EventSink
from event_universe.core.disturbance_state import InitialState
from event_universe.fields.disturbances import DisturbanceLaw
from event_universe.fields.spatial_coupling import SpatialCouplingLaw
from event_universe.fields.spatial_decay import SpatialDecayLaw
from event_universe.fields.spatial_plan import SpatialLaw


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
            SpatialLaw(
                initial.fields, initial.spatial_fields, initial.emissions, initial.operation_costs
            ),
            (
                SpatialCouplingLaw(
                    initial.fields,
                    initial.spatial_couplings,
                    initial.operation_costs,
                    initial.spatial_fields,
                )
                if initial.spatial_couplings
                else None
            ),
            (
                SpatialDecayLaw(initial.fields, initial.spatial_fields, initial.operation_costs)
                if initial.schema_version == 2
                else None
            ),
        )
