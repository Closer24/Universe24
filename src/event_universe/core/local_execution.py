"""Immutable proposal messages and the scheduler-facing execution protocol."""

from collections.abc import Generator, Iterable
from dataclasses import dataclass
from typing import Protocol

from .disturbance_state import DisturbanceRecord, LocalPlan
from .event_resolution import Planner
from .record_policy import RecordPolicy


def validate_execution_options(workers: int, parallel_threshold: int, chunk_size: int) -> None:
    for name, value in (
        ("workers", workers),
        ("parallel_threshold", parallel_threshold),
        ("chunk_size", chunk_size),
    ):
        if type(value) is not int or value < 1:
            raise ValueError(f"{name} must be a positive integer")


@dataclass(frozen=True, slots=True)
class ProposalInput:
    records: tuple[DisturbanceRecord | None, ...]
    residuals: tuple[int, ...]
    received: int


@dataclass(frozen=True, slots=True)
class ProposalResult:
    plan: LocalPlan | None = None
    error: Exception | None = None

    def result(self) -> LocalPlan:
        if self.error is not None:
            raise self.error
        if self.plan is None:
            raise RuntimeError("local worker returned no proposal")
        return self.plan


class LocalExecutor(Protocol):
    """Host evaluation is optional; only the serial engine publishes results."""

    workers: int
    parallel_threshold: int
    parallel_enabled: bool

    def supported(self, planner: Planner, record_policy: RecordPolicy) -> bool: ...

    def planner_unchanged(self, planner: Planner) -> bool: ...

    def policy_unchanged(self, policy: RecordPolicy) -> bool: ...

    def record_serial(self, reason: str) -> None: ...

    def evaluate(self, inputs: Iterable[ProposalInput]) -> Generator[ProposalResult]: ...

    def report(self) -> dict[str, object]: ...

    def close(self) -> None: ...
