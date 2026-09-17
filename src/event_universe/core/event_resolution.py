"""Local extension protocol; the scheduler does not interpret domain payloads."""

from dataclasses import dataclass
from typing import Protocol, runtime_checkable

from .disturbance_state import Address3, DisturbanceRecord, LocalPlan, Values


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
    # Computation load pricing a departure through each of the six ports.
    port_loads: tuple[int, ...] = (0, 0, 0, 0, 0, 0)


class EventResolver(Protocol):
    def has_work(self, context: LocalContext) -> bool: ...

    def resolve(self, context: LocalContext, planner: Planner) -> LocalPlan: ...

    def advance(self, tick: int) -> None: ...

    def report(self) -> dict[str, object]: ...


@runtime_checkable
class CommitResolver(Protocol):
    """Optional finite local alternatives, selected only after commit preflight.

    Alternatives may replace reserved slots, never change routing, source deltas,
    reactions or cycle cost. The token is local bookkeeping, not executable data.
    """

    def alternatives(
        self, context: LocalContext, token: int
    ) -> tuple[tuple[tuple[int, DisturbanceRecord | None], ...], ...]: ...

    def commit_choice(
        self, context: LocalContext, token: int, following_events: int
    ) -> tuple[int, int]: ...

    def begin_tick(self, tick: int) -> None: ...

    def inventory(self) -> Values: ...
