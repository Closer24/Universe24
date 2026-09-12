"""Public assembly of the generic disturbance simulator."""

from event_universe.core.disturbance_engine import DisturbanceEngine, EventSink
from event_universe.core.disturbance_state import InitialState
from event_universe.fields.disturbances import DisturbanceLaw
from event_universe.fields.record_operations import RecordOperations
from event_universe.fields.spatial_coupling import SpatialCouplingLaw
from event_universe.fields.spatial_decay import SpatialDecayLaw
from event_universe.fields.spatial_interactions import JointSpatialCouplingLaw
from event_universe.fields.spatial_plan import SpatialLaw


class Simulation(DisturbanceEngine):
    """Run the fields, disturbances and integer laws supplied by initialization."""

    def __init__(self, initial: InitialState, *, observer: EventSink | None = None) -> None:
        event_space, resolver = None, None
        if initial.event_program is not None:
            from event_universe.integration.event_runtime import build_event_runtime

            event_space, resolver = build_event_runtime(initial)
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
                initial.fields,
                initial.spatial_fields,
                initial.emissions,
                initial.operation_costs,
                initial.field_rules,
            ),
            (
                JointSpatialCouplingLaw(
                    initial.fields,
                    initial.spatial_couplings,
                    initial.operation_costs,
                    initial.spatial_fields,
                    initial.spatial_interactions,
                )
                if initial.spatial_interactions
                or (
                    initial.spatial_couplings
                    and any(field.transport == "local" for field in initial.spatial_fields)
                )
                else SpatialCouplingLaw(
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
            record_policy=RecordOperations(
                initial.fields,
                initial.disturbances,
                initial.couplings,
                initial.interactions,
                frozenset(
                    (
                        *(rule.type_index for rule in initial.spatial_couplings),
                        *(rule.type_index for rule in initial.spatial_interactions),
                    )
                ),
            ),
            event_space=event_space,
            resolver=resolver,
        )
