"""Host-only parallel execution for immutable local Node planning inputs."""

from collections.abc import Callable, Generator
from concurrent.futures import InterpreterPoolExecutor
from dataclasses import dataclass
from typing import TypeVar

from .disturbance_state import DisturbanceRecord, LocalPlan
from .event_resolution import Planner as DisturbancePlanner
from .plan_reuse import PlanReuse
from .spatial_state import Rays, Remainders, SpatialPlan, SpatialState

SpatialPlanner = Callable[
    [
        tuple[SpatialState, ...],
        tuple[DisturbanceRecord | None, ...],
        int,
        int,
        tuple[Rays, ...],
        int,
        int,
        int,
        Remainders,
        Remainders,
    ],
    SpatialPlan,
]

MAX_NODE_WORKERS = 64
PlanningInput = TypeVar("PlanningInput")


@dataclass(frozen=True, slots=True)
class DisturbancePlanningInput:
    records: tuple[DisturbanceRecord | None, ...]
    residuals: tuple[int, ...]
    received: int
    port_loads: tuple[int, ...] = (0, 0, 0, 0, 0, 0)


@dataclass(frozen=True, slots=True)
class SpatialPlanningInput:
    states: tuple[SpatialState, ...]
    records: tuple[DisturbanceRecord | None, ...]
    received: int
    node_cost: int = 0
    rays: tuple[Rays, ...] = ()
    tick: int = 0
    # 0 forwards normally, 1 holds resident rays, 2 also advances their phase.
    ray_hold: int = 0
    # The Port the bound group held at the Node departs through this interval,
    # or -1 (bound-group-motion-v1): decided by the Node from its register.
    bound_port: int = -1
    # The Node's remainder registers and their phases (field-remainder-v1).
    remainders: Remainders = ()
    remainder_phases: Remainders = ()


PlanningRequest = DisturbancePlanningInput | SpatialPlanningInput | None
PlanningResult = LocalPlan | SpatialPlan | None
PlanningCycle = Generator[PlanningRequest, PlanningResult]


def finish_local_cycle(
    cycle: PlanningCycle, disturbance: DisturbancePlanner | None, spatial: SpatialPlanner | None
) -> None:
    """Drive one Node's transition locally with the same immutable request boundary."""
    result: PlanningResult = None
    try:
        while True:
            try:
                request = cycle.send(result)
            except StopIteration:
                return
            if isinstance(request, DisturbancePlanningInput):
                assert disturbance is not None
                result = disturbance(
                    request.records,
                    request.residuals,
                    request.received,
                    port_loads=request.port_loads,
                )
            elif isinstance(request, SpatialPlanningInput):
                assert spatial is not None
                result = spatial(
                    request.states,
                    request.records,
                    request.received,
                    request.node_cost,
                    request.rays,
                    request.tick,
                    request.ray_hold,
                    request.bound_port,
                    request.remainders,
                    request.remainder_phases,
                )
            else:
                result = None
    finally:
        cycle.close()


def _plan_disturbance_batch(
    planner: DisturbancePlanner, items: tuple[DisturbancePlanningInput, ...]
) -> tuple[LocalPlan, ...]:
    return tuple(
        planner(item.records, item.residuals, item.received, port_loads=item.port_loads)
        for item in items
    )


def _plan_spatial_batch(
    planner: SpatialPlanner, items: tuple[SpatialPlanningInput, ...]
) -> tuple[SpatialPlan, ...]:
    return tuple(
        planner(
            item.states,
            item.records,
            item.received,
            item.node_cost,
            item.rays,
            item.tick,
            item.ray_hold,
            item.bound_port,
            item.remainders,
            item.remainder_phases,
        )
        for item in items
    )


class NodeExecution:
    """Plan every eligible Node in bounded isolated-interpreter batches."""

    def __init__(
        self,
        workers: int,
        disturbance_planner: DisturbancePlanner,
        spatial_planner: SpatialPlanner | None,
        *,
        reuse_carriers: bool = False,
        reuse_fields: bool = False,
    ) -> None:
        if type(workers) is not int or not 1 <= workers <= MAX_NODE_WORKERS:
            raise ValueError(f"node_workers must be an integer from 1 through {MAX_NODE_WORKERS}")
        self.workers = workers
        self._disturbance_planner = disturbance_planner
        self._spatial_planner = spatial_planner
        self._executor: InterpreterPoolExecutor | None = None
        self._disturbance_tasks = 0
        self._spatial_tasks = 0
        self._parallel_batches = 0
        self._largest_batch = 0
        self._carrier_reuse = PlanReuse[DisturbancePlanningInput, LocalPlan](
            4096 if reuse_carriers else 0
        )
        self._field_reuse = PlanReuse[SpatialPlanningInput, SpatialPlan](4096 if reuse_fields else 0)

    def disturbance(
        self,
        records: tuple[DisturbanceRecord | None, ...],
        residuals: tuple[int, ...],
        received: int,
        *,
        port_loads: tuple[int, ...] = (0, 0, 0, 0, 0, 0),
    ) -> LocalPlan:
        request = DisturbancePlanningInput(records, residuals, received, port_loads)
        return self._carrier_reuse.one(request, lambda: self._evaluate_carriers((request,))[0])

    def spatial(
        self,
        states: tuple[SpatialState, ...],
        records: tuple[DisturbanceRecord | None, ...],
        received: int,
        node_cost: int = 0,
        rays: tuple[Rays, ...] = (),
        tick: int = 0,
        ray_hold: int = 0,
        bound_port: int = -1,
        remainders: Remainders = (),
        remainder_phases: Remainders = (),
    ) -> SpatialPlan:
        request = SpatialPlanningInput(
            states,
            records,
            received,
            node_cost,
            rays,
            tick,
            ray_hold,
            bound_port,
            remainders,
            remainder_phases,
        )
        return self._field_reuse.one(request, lambda: self._evaluate_fields((request,))[0])

    def _evaluate_carriers(self, items: tuple[DisturbancePlanningInput, ...]) -> tuple[LocalPlan, ...]:
        if not self.parallel:
            return _plan_disturbance_batch(self._disturbance_planner, items)
        return self._submit_carriers(items)

    def _evaluate_fields(self, items: tuple[SpatialPlanningInput, ...]) -> tuple[SpatialPlan, ...]:
        if not items:
            return ()
        if self._spatial_planner is None:
            raise RuntimeError("spatial planning requires a configured planner")
        if not self.parallel:
            return _plan_spatial_batch(self._spatial_planner, items)
        return self._submit_fields(items)

    @property
    def parallel(self) -> bool:
        return self.workers > 1

    def _pool(self) -> InterpreterPoolExecutor:
        if self._executor is None:
            self._executor = InterpreterPoolExecutor(
                max_workers=self.workers,
                thread_name_prefix="event-universe-node",
            )
        return self._executor

    def _record_batch(self, size: int) -> None:
        if size:
            self._parallel_batches += 1
            self._largest_batch = max(self._largest_batch, size)

    def _chunks(self, items: tuple[PlanningInput, ...]) -> tuple[tuple[PlanningInput, ...], ...]:
        count = min(self.workers, len(items))
        if count == 0:
            return ()
        width, extra = divmod(len(items), count)
        chunks = []
        start = 0
        for index in range(count):
            end = start + width + int(index < extra)
            chunks.append(items[start:end])
            start = end
        return tuple(chunks)

    def _submit_carriers(self, items: tuple[DisturbancePlanningInput, ...]) -> tuple[LocalPlan, ...]:
        if not self.parallel:
            raise RuntimeError("parallel submission requires more than one Node worker")
        if not items:
            return ()
        self._record_batch(len(items))
        self._disturbance_tasks += len(items)
        pool = self._pool()
        chunks = self._chunks(items)
        futures = tuple(
            pool.submit(_plan_disturbance_batch, self._disturbance_planner, chunk) for chunk in chunks
        )
        return tuple(plan for future in futures for plan in future.result())

    def _submit_fields(self, items: tuple[SpatialPlanningInput, ...]) -> tuple[SpatialPlan, ...]:
        if not self.parallel:
            raise RuntimeError("parallel submission requires more than one Node worker")
        if not items:
            return ()
        self._record_batch(len(items))
        self._spatial_tasks += len(items)
        if self._spatial_planner is None:
            raise RuntimeError("parallel spatial planning requires a configured planner")
        pool = self._pool()
        chunks = self._chunks(items)
        futures = tuple(
            pool.submit(_plan_spatial_batch, self._spatial_planner, chunk) for chunk in chunks
        )
        return tuple(plan for future in futures for plan in future.result())

    def plan_disturbances(self, items: tuple[DisturbancePlanningInput, ...]) -> tuple[LocalPlan, ...]:
        return self._carrier_reuse.resolve(items, self._evaluate_carriers)

    def plan_spatial(self, items: tuple[SpatialPlanningInput, ...]) -> tuple[SpatialPlan, ...]:
        return self._field_reuse.resolve(items, self._evaluate_fields)

    def finish_cycles(self, cycles: tuple[PlanningCycle, ...]) -> None:
        """Batch immutable requests, then resume local owners in deterministic order.

        Generators stay on the scheduler thread and are discarded after this tick.
        Workers receive only request records and immutable configured planners.
        """
        active = list(cycles)
        results: list[PlanningResult] = [None] * len(active)
        try:
            while active:
                waiting = []
                requests: list[PlanningRequest] = []
                for cycle, result in zip(active, results, strict=True):
                    try:
                        request = cycle.send(result)
                    except StopIteration:
                        continue
                    waiting.append(cycle)
                    requests.append(request)
                carrier = self.plan_disturbances(
                    tuple(r for r in requests if isinstance(r, DisturbancePlanningInput))
                )
                fields = self.plan_spatial(
                    tuple(r for r in requests if isinstance(r, SpatialPlanningInput))
                )
                carrier_results, field_results = iter(carrier), iter(fields)
                results = [
                    next(carrier_results)
                    if isinstance(r, DisturbancePlanningInput)
                    else next(field_results)
                    if isinstance(r, SpatialPlanningInput)
                    else None
                    for r in requests
                ]
                active = waiting
        finally:
            for cycle in cycles:
                cycle.close()

    def report(self) -> dict[str, object]:
        return {
            "backend": "isolated-interpreters" if self.parallel else "serial",
            "node_workers": self.workers,
            "disturbance_node_tasks": self._disturbance_tasks,
            "spatial_node_tasks": self._spatial_tasks,
            "parallel_batches": self._parallel_batches,
            "largest_batch": self._largest_batch,
            "carrier_plan_reuse": self._carrier_reuse.report(),
            "spatial_plan_reuse": self._field_reuse.report(),
        }

    def close(self) -> None:
        self._carrier_reuse.clear()
        self._field_reuse.clear()
        if self._executor is not None:
            self._executor.shutdown(wait=True, cancel_futures=True)
            self._executor = None
