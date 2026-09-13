"""Host-only parallel execution for immutable local Node planning inputs."""

from collections.abc import Callable
from concurrent.futures import InterpreterPoolExecutor
from dataclasses import dataclass
from typing import TypeVar

from .disturbance_state import DisturbanceRecord, LocalPlan
from .event_resolution import Planner as DisturbancePlanner
from .spatial_state import SpatialPlan, SpatialState

SpatialPlanner = Callable[
    [tuple[SpatialState, ...], tuple[DisturbanceRecord | None, ...], int], SpatialPlan
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
    return tuple(planner(item.states, item.records, item.received) for item in items)


class NodeExecution:
    """Plan every eligible Node in bounded isolated-interpreter batches."""

    def __init__(
        self,
        workers: int,
        disturbance_planner: DisturbancePlanner,
        spatial_planner: SpatialPlanner | None,
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

    def plan_disturbances(self, items: tuple[DisturbancePlanningInput, ...]) -> tuple[LocalPlan, ...]:
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

    def plan_spatial(self, items: tuple[SpatialPlanningInput, ...]) -> tuple[SpatialPlan, ...]:
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

    def report(self) -> dict[str, object]:
        return {
            "backend": "isolated-interpreters" if self.parallel else "serial",
            "node_workers": self.workers,
            "disturbance_node_tasks": self._disturbance_tasks,
            "spatial_node_tasks": self._spatial_tasks,
            "parallel_batches": self._parallel_batches,
            "largest_batch": self._largest_batch,
        }

    def close(self) -> None:
        if self._executor is not None:
            self._executor.shutdown(wait=True, cancel_futures=True)
            self._executor = None
