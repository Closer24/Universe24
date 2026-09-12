"""Local extension protocol; the scheduler does not interpret domain payloads."""

from collections.abc import Callable
from dataclasses import dataclass
from typing import Protocol

from .disturbance_state import Address3, DisturbanceRecord, LocalPlan

Planner = Callable[[tuple[DisturbanceRecord | None, ...], tuple[int, ...], int], LocalPlan]


@dataclass(frozen=True, slots=True)
class LocalContext:
    tick: int
    address: Address3
    records: tuple[DisturbanceRecord | None, ...]
    residuals: tuple[int, ...]
    received: int
    cause: int | None


class EventResolver(Protocol):
    def has_work(self, context: LocalContext) -> bool: ...

    def resolve(self, context: LocalContext, planner: Planner) -> LocalPlan: ...

    def advance(self, tick: int) -> None: ...

    def report(self) -> dict[str, object]: ...
