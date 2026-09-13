"""Public assembly of the generic disturbance simulator."""

from typing import TYPE_CHECKING

from event_universe.core.coupling_selectors import selected_type_set
from event_universe.core.disturbance_engine import DisturbanceEngine, EventSink
from event_universe.core.disturbance_state import InitialState
from event_universe.fields.disturbances import DisturbanceLaw
from event_universe.fields.node_conservation import LocalBalanceGuard
from event_universe.fields.record_operations import RecordOperations
from event_universe.fields.spatial_coupling import SpatialCouplingLaw
from event_universe.fields.spatial_decay import SpatialDecayLaw
from event_universe.fields.spatial_interactions import JointSpatialCouplingLaw
from event_universe.fields.spatial_plan import SpatialLaw

if TYPE_CHECKING:
    from event_universe.diagnostics.local_conservation import LocalConservationAudit


class Simulation(DisturbanceEngine):
    """Run configured local rules over Nodes connected by Links."""

    def __init__(self, initial: InitialState, *, observer: EventSink | None = None) -> None:
        event_space, resolver = None, None
        if initial.event_program is not None:
            from event_universe.integration.event_runtime import build_event_runtime

            event_space, resolver = build_event_runtime(initial)
        spatial_law = SpatialLaw(
            initial.fields,
            initial.spatial_fields,
            initial.emissions,
            initial.operation_costs,
            initial.field_rules,
        )
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
            spatial_law,
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
                selected_type_set(initial.spatial_couplings, initial.spatial_interactions),
            ),
            event_space=event_space,
            resolver=resolver,
            field_guard=spatial_law.validate_guards,
            balance_guard=(
                LocalBalanceGuard(
                    initial.fields,
                    initial.spatial_fields,
                    initial.operation_costs,
                    initial.conservation_contract,
                )
                if initial.conservation_contract is not None
                else None
            ),
        )
        self._audit: LocalConservationAudit | None = None
        if initial.conservation is not None:
            from event_universe.diagnostics.local_conservation import LocalConservationAudit

            self._audit = LocalConservationAudit(initial, self.inventory_view)
        self._external_observer = observer
        if self._audit is not None:
            self._observer = self._observe_conservation
            if self._spatial is not None:
                self._spatial.observer = self._observe_conservation

    def _observe_conservation(self, event: dict[str, object]) -> None:
        assert self._audit is not None
        try:
            self._audit.observe(event)
        finally:
            if self._external_observer is not None:
                self._external_observer(event)

    def conservation_report(self) -> dict[str, object]:
        """Read configured guard coverage and optional passive measurements."""
        report: dict[str, object] = (
            {"status": "not_configured"} if self._audit is None else self._audit.report()
        )
        contract = self.initial.conservation_contract
        if contract is not None:
            from event_universe.diagnostics.node_conservation import node_contract_report

            if self._audit is None:
                report = {"status": "guarded"}
            report["node_contract"] = node_contract_report(self.initial, self.inventory_view())
        return report
