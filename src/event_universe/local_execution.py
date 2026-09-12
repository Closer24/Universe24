"""Host workers for immutable local proposals, without publishing physical state."""

from collections import deque
from collections.abc import Callable, Generator, Sequence
from dataclasses import dataclass, fields, is_dataclass
from typing import TYPE_CHECKING

from .core.event_resolution import Planner
from .core.local_execution import ProposalInput, ProposalResult, validate_execution_options
from .core.record_policy import RecordPolicy
from .fields.disturbances import DisturbanceLaw
from .fields.record_operations import RecordOperations

if TYPE_CHECKING:
    from concurrent.futures import Executor, Future


_PLANNER_METHODS: tuple[tuple[str, object], ...] = tuple(
    (name, method) for name, method in vars(DisturbanceLaw).items() if callable(method)
)
_POLICY_METHODS: tuple[tuple[str, object], ...] = tuple(
    (name, method) for name, method in vars(RecordOperations).items() if callable(method)
)


@dataclass(frozen=True, slots=True)
class WorkerResult:
    process: int
    interpreter: int
    proposals: tuple[ProposalResult, ...]


_worker_planner: Planner | None = None


def worker_initializer(planner: Planner) -> tuple[Callable[..., object], tuple[object, ...]]:
    import pickle
    from pathlib import Path
    from runpy import run_path

    from . import worker_bootstrap

    return run_path, (
        str(Path(worker_bootstrap.__file__).resolve()),
        {
            "_event_universe_source": str(Path(__file__).resolve().parents[1]),
            "_event_universe_planner": pickle.dumps(planner),
        },
        "__event_universe_worker__",
    )


def _evaluate_chunk(inputs: tuple[ProposalInput, ...]) -> WorkerResult:
    from concurrent.interpreters import get_current
    from os import getpid

    from event_universe import local_execution

    planner = local_execution._worker_planner
    if planner is None:
        raise RuntimeError("local worker has no immutable planner")
    proposals = []
    for item in inputs:
        try:
            plan = planner(item.records, item.residuals, item.received)
        except Exception as error:
            proposals.append(ProposalResult(error=error))
        else:
            proposals.append(ProposalResult(plan=plan))
    return WorkerResult(getpid(), get_current().id, tuple(proposals))


class LocalExecution:
    """Persistent interpreters with at most two queued chunks per requested worker.

    Only the public composition owner supplies the known immutable planner and
    record policy. Replaced callbacks are ineligible for speculation. Worker
    exceptions are data until the serial owner reaches that address's planner.
    No worker receives cells, links, clocks, observers, resolvers or a world.
    """

    def __init__(
        self,
        planner: Planner,
        record_policy: RecordPolicy,
        *,
        workers: int = 1,
        parallel_threshold: int = 64,
        chunk_size: int = 32,
        executor: Executor | None = None,
        execution_backend: str = "interpreters",
    ) -> None:
        validate_execution_options(workers, parallel_threshold, chunk_size)
        self.planner = planner
        self.record_policy = record_policy
        self.workers = workers
        self.parallel_enabled = workers > 1 or executor is not None
        self.parallel_threshold = parallel_threshold
        self.chunk_size = chunk_size
        self.execution_backend = execution_backend
        self.closed = False
        self._pool: Executor | None = executor
        self._owns_pool = executor is None
        self._workers_used: set[tuple[int, int]] = set()
        self._submitted_chunks = 0
        self._evaluated_proposals = 0
        self._serial_proposals = 0
        self._peak_pending_chunks = 0
        self._fallback_reasons: dict[str, int] = {}
        if not is_dataclass(planner) or not is_dataclass(record_policy):
            raise TypeError("parallel composition requires immutable law definitions")
        self._planner_state: tuple[tuple[str, object], ...] = tuple(
            (item.name, getattr(planner, item.name)) for item in fields(planner)
        )
        self._policy_state: tuple[tuple[str, object], ...] = tuple(
            (item.name, getattr(record_policy, item.name)) for item in fields(record_policy)
        )
        self._policy_keys: frozenset[str] = frozenset(name for name, _ in self._policy_state)

    def planner_unchanged(self, planner: Planner) -> bool:
        return (
            planner is self.planner
            and type(planner) is DisturbanceLaw
            and all(getattr(planner, name) is value for name, value in self._planner_state)
            and all(getattr(type(planner), name) is method for name, method in _PLANNER_METHODS)
        )

    def policy_unchanged(self, policy: RecordPolicy) -> bool:
        return (
            policy is self.record_policy
            and type(policy) is RecordOperations
            and vars(policy).keys() == self._policy_keys
            and all(getattr(policy, name) is value for name, value in self._policy_state)
            and all(getattr(type(policy), name) is method for name, method in _POLICY_METHODS)
        )

    def supported(self, planner: Planner, record_policy: RecordPolicy) -> bool:
        return self.planner_unchanged(planner) and self.policy_unchanged(record_policy)

    def record_serial(self, reason: str) -> None:
        self._serial_proposals += 1
        if self.parallel_enabled:
            self._fallback_reasons[reason] = self._fallback_reasons.get(reason, 0) + 1

    def _read_result(self, future: Future[WorkerResult], count: int) -> tuple[ProposalResult, ...]:
        try:
            result = future.result()
        except Exception as error:
            # Infrastructure failures also surface only at the owner address.
            return (ProposalResult(error=error),) * count
        self._workers_used.add((result.process, result.interpreter))
        self._evaluated_proposals += len(result.proposals)
        return result.proposals

    def evaluate(self, inputs: Sequence[ProposalInput]) -> Generator[ProposalResult]:
        if self.closed:
            raise RuntimeError("local execution is closed")
        if self._pool is None:
            from concurrent.futures import InterpreterPoolExecutor

            initializer, initargs = worker_initializer(self.planner)
            self._pool = InterpreterPoolExecutor(
                max_workers=self.workers,
                initializer=initializer,
                initargs=initargs,
                thread_name_prefix="event-universe-local",
            )
        chunks = (
            tuple(inputs[start : start + self.chunk_size])
            for start in range(0, len(inputs), self.chunk_size)
        )
        pending: deque[tuple[Future[WorkerResult], int]] = deque()

        def submit() -> None:
            chunk = next(chunks, None)
            if chunk is None:
                return
            assert self._pool is not None
            pending.append((self._pool.submit(_evaluate_chunk, chunk), len(chunk)))
            self._submitted_chunks += 1
            self._peak_pending_chunks = max(self._peak_pending_chunks, len(pending))

        try:
            for _ in range(2 * self.workers):
                submit()
            while pending:
                future, count = pending.popleft()
                proposals = self._read_result(future, count)
                submit()
                yield from proposals
        finally:
            # Discard unpublished work after an owner failure or callback change.
            # Running chunks remain bounded, pure and accounted for before return.
            for future, count in pending:
                if not future.cancel():
                    self._read_result(future, count)

    def report(self) -> dict[str, object]:
        return {
            "backend": self.execution_backend if self._submitted_chunks else "serial",
            "requested_workers": self.workers,
            "parallel_threshold": self.parallel_threshold,
            "chunk_size": self.chunk_size,
            "workers_used": [
                {"process": process, "interpreter": interpreter}
                for process, interpreter in sorted(self._workers_used)
            ],
            "submitted_chunks": self._submitted_chunks,
            "evaluated_proposals": self._evaluated_proposals,
            "serial_proposals": self._serial_proposals,
            "peak_pending_chunks": self._peak_pending_chunks,
            "fallback_reasons": self._fallback_reasons.copy(),
            "closed": self.closed,
            "owns_executor": self._owns_pool,
        }

    def close(self) -> None:
        if not self.closed:
            self.closed = True
            if self._pool is not None and self._owns_pool:
                self._pool.shutdown(wait=True, cancel_futures=True)
                self._pool = None
