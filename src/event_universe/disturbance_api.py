"""Public assembly of the generic disturbance simulator."""

from typing import TYPE_CHECKING

from event_universe.core.coupling_selectors import selected_type_set
from event_universe.core.disturbance_engine import DisturbanceEngine, EventSink
from event_universe.core.disturbance_state import InitialState
from event_universe.core.topology import validate_topology_configuration
from event_universe.fields.disturbances import DisturbanceLaw
from event_universe.fields.record_operations import RecordOperations
from event_universe.fields.spatial_coupling import SpatialCouplingLaw
from event_universe.fields.spatial_decay import SpatialDecayLaw
from event_universe.fields.spatial_interactions import JointSpatialCouplingLaw
from event_universe.fields.spatial_plan import SpatialLaw

if TYPE_CHECKING:
    from event_universe.diagnostics.local_conservation import LocalConservationAudit


class Simulation(DisturbanceEngine):
    """Run the fields, disturbances and integer laws supplied by initialization."""

    def __init__(self, initial: InitialState, *, observer: EventSink | None = None) -> None:
        validate_topology_configuration(initial)
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
                port_offsets=initial.topology.offsets,
            ),
            observer,
            SpatialLaw(
                initial.fields,
                initial.spatial_fields,
                initial.emissions,
                initial.operation_costs,
                initial.field_rules,
                port_count=len(initial.topology.offsets),
            ),
            (
                JointSpatialCouplingLaw(
                    initial.fields,
                    initial.spatial_couplings,
                    initial.operation_costs,
                    initial.spatial_fields,
                    initial.spatial_interactions,
                    port_offsets=initial.topology.offsets,
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
                    port_offsets=initial.topology.offsets,
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
                selected_type_set(initial.spatial_couplings, initial.spatial_interactions),
            ),
            event_space=event_space,
            resolver=resolver,
        )
        self._audit: LocalConservationAudit | None = None
        if initial.conservation is not None:
            from event_universe.diagnostics.local_conservation import LocalConservationAudit

            self._audit = LocalConservationAudit(initial, self.inventory_view)
        self._external_observer = observer
        if self._audit is not None:
            self.set_observer(self._observe_conservation)

    def _observe_conservation(self, event: dict[str, object]) -> None:
        assert self._audit is not None
        try:
            self._audit.observe(event)
        finally:
            if self._external_observer is not None:
                self._external_observer(event)

    def conservation_report(self) -> dict[str, object]:
        """Read the optional candidate energy/momentum audit without advancing time."""
        return {"status": "not_configured"} if self._audit is None else self._audit.report()
