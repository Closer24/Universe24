"""Local record-operation interface; no world access or physical-name semantics."""

from typing import Protocol

from .disturbance_state import DisturbanceRecord, LocalPlan


class RecordPolicy(Protocol):
    """Pure proposals over fixed local slots and already-delivered records.

    Shared immutable definitions live in the implementation, outside node state.
    Implementations preserve slot count and pending locks, validate integer
    results, and must not retain mutable state or read a world or a clock.
    """

    def has_work(self, records: tuple[DisturbanceRecord | None, ...]) -> bool: ...

    def receive(
        self,
        resident: tuple[DisturbanceRecord | None, ...],
        arrivals: tuple[DisturbanceRecord, ...],
        locked: frozenset[int],
    ) -> tuple[DisturbanceRecord | None, ...]: ...

    def report_cost(self, plan: LocalPlan) -> LocalPlan: ...
