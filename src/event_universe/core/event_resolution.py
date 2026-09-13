"""Local extension protocol; the scheduler does not interpret domain payloads."""

from collections.abc import Callable, Mapping
from dataclasses import dataclass
from typing import Protocol, runtime_checkable

from .disturbance_state import Address3, DisturbanceRecord, LocalPlan, Values
from .source_emission import SourceDeposit
from .source_emission_node import EmittingEnvelopeNode
from .spatial_state import SpatialState

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


@runtime_checkable
class CausalSourceResolver(Protocol):
    """A local source owner, separate from quantum status and ordinary inventory."""

    def source_nodes(self) -> Mapping[Address3, EmittingEnvelopeNode]: ...

    def start_sources(self, tick: int) -> None: ...

    def prepare_source(
        self, address: Address3, tick: int, states: tuple[SpatialState, ...], node_cost: int
    ) -> SourceDeposit | None: ...

    def commit_source(self, address: Address3, tick: int) -> None: ...
