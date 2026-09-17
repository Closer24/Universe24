"""Public assembly of the generic disturbance simulator."""

from typing import TYPE_CHECKING

from event_universe.core.disturbance_engine import DisturbanceEngine, EventSink
from event_universe.core.disturbance_state import InitialState
from event_universe.fields.disturbances import DisturbanceLaw
from event_universe.fields.node_conservation import LocalBalanceGuard
from event_universe.fields.spatial_coupling import SpatialCouplingLaw
from event_universe.fields.spatial_decay import SpatialDecayLaw
from event_universe.fields.spatial_interactions import JointSpatialCouplingLaw
from event_universe.fields.spatial_plan import SpatialLaw

if TYPE_CHECKING:
    from event_universe.diagnostics.local_conservation import LocalConservationAudit


class Simulation(DisturbanceEngine):
    """Run configured local rules over Nodes connected by Links."""

    def __init__(
        self,
        initial: InitialState,
        *,
        observer: EventSink | None = None,
        node_workers: int = 1,
    ) -> None:
        responses = tuple(rule for rule in initial.spatial_couplings if rule.mode != "absorb")
        spatial_law = SpatialLaw(
            initial.fields,
            initial.spatial_fields,
            initial.emissions,
            initial.operation_costs,
            initial.field_rules,
            ray_interactions=initial.ray_interactions,
            absorptions=tuple(rule for rule in initial.spatial_couplings if rule.mode == "absorb"),
            allocation_phase=initial.allocation_phase,
            computation_field=initial.computation_field,
            least_delay_direction=initial.delay_direction if initial.least_delay_routing else None,
            sampling_profile=initial.sampling_profile,
            return_mode=initial.return_mode,
        )
        super().__init__(
            initial,
            DisturbanceLaw(
                initial.fields,
                initial.disturbances,
                initial.couplings,
                initial.operation_costs,
                initial.interactions,
                initial.least_delay_routing,
            ),
            observer,
            spatial_law,
            (
                JointSpatialCouplingLaw(
                    initial.fields,
                    responses,
                    initial.operation_costs,
                    initial.spatial_fields,
                    emissions=initial.emissions,
                    interactions=initial.spatial_interactions,
                )
                if initial.spatial_interactions
                or (responses and any(field.transport == "local" for field in initial.spatial_fields))
                else SpatialCouplingLaw(
                    initial.fields,
                    responses,
                    initial.operation_costs,
                    initial.spatial_fields,
                    emissions=initial.emissions,
                )
                if responses
                else None
            ),
            (
                SpatialDecayLaw(initial.fields, initial.spatial_fields, initial.operation_costs)
                if initial.schema_version == 2
                else None
            ),
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
            node_workers=node_workers,
            reuse_carrier_plans=initial.focus,
            reuse_spatial_plans=initial.focus,
        )
        if initial.dense_field:
            # The dense mode (dense-field-v1): the board's pure-field Nodes cycled
            # as one step by a component composed here, outside the core; the
            # admission is the parser's (`validate_dense_field_admission`).
            from event_universe.dense_field import DenseField

            if node_workers > 1:
                raise ValueError("dense_field does not support parallel Node execution")
            assert self._spatial is not None
            self._spatial.dense = DenseField(initial, self._spatial)
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
