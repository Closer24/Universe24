"""Local extension protocol; the scheduler does not interpret domain payloads."""

from dataclasses import dataclass
from typing import Protocol

from .disturbance_state import Address3, DisturbanceRecord, LocalPlan


class Planner(Protocol):
    def __call__(
        self,
        records: tuple[DisturbanceRecord | None, ...],
        coupling_remainders: tuple[int, ...],
        received_count: int,
        /,
        *,
        port_loads: tuple[int, ...] = (0, 0, 0, 0, 0, 0),
    ) -> LocalPlan: ...


@dataclass(frozen=True, slots=True)
class LocalContext:
    tick: int
    address: Address3
    records: tuple[DisturbanceRecord | None, ...]
    residuals: tuple[int, ...]
    received: int
    cause: int | None
    # Computation load pricing a departure through each of the six ports.
    port_loads: tuple[int, ...] = (0, 0, 0, 0, 0, 0)


class EventResolver(Protocol):
    def has_work(self, context: LocalContext) -> bool: ...

    def resolve(self, context: LocalContext, planner: Planner) -> LocalPlan: ...

    def advance(self, tick: int) -> None: ...

    def report(self) -> dict[str, object]: ...
