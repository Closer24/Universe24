"""Public assembly of the generic disturbance simulator."""

from collections.abc import Callable
from typing import TYPE_CHECKING

from event_universe.core.disturbance_engine import DisturbanceEngine, EventSink
from event_universe.core.disturbance_state import InitialState
from event_universe.core.event_resolution import Planner
from event_universe.core.local_execution import validate_execution_options
from event_universe.fields.disturbances import DisturbanceLaw
from event_universe.fields.record_operations import RecordOperations
from event_universe.fields.spatial_coupling import SpatialCouplingLaw
from event_universe.fields.spatial_decay import SpatialDecayLaw
from event_universe.fields.spatial_interactions import JointSpatialCouplingLaw
from event_universe.fields.spatial_plan import SpatialLaw
from event_universe.local_execution import LocalExecution

if TYPE_CHECKING:
    from concurrent.futures import Executor


class Simulation(DisturbanceEngine):
    """Run the fields, disturbances and integer laws supplied by initialization."""

    def __init__(
        self,
        initial: InitialState,
        *,
        observer: EventSink | None = None,
        workers: int = 1,
        parallel_threshold: int = 64,
        chunk_size: int = 32,
        executor_factory: Callable[[Planner], Executor] | None = None,
        execution_backend: str = "interpreters",
    ) -> None:
        validate_execution_options(workers, parallel_threshold, chunk_size)
        event_space, resolver = None, None
        if initial.event_program is not None:
            from event_universe.integration.event_runtime import build_event_runtime

            event_space, resolver = build_event_runtime(initial)
        planner = DisturbanceLaw(
            initial.fields,
            initial.disturbances,
            initial.couplings,
            initial.operation_costs,
            initial.interactions,
        )
        record_policy = RecordOperations(
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
        )
        executor = None if executor_factory is None else executor_factory(planner)
        super().__init__(
            initial,
            planner,
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
            record_policy=record_policy,
            event_space=event_space,
            resolver=resolver,
            local_execution=LocalExecution(
                planner,
                record_policy,
                workers=workers,
                parallel_threshold=parallel_threshold,
                chunk_size=chunk_size,
                executor=executor,
                execution_backend=execution_backend,
            ),
        )
