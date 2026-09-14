"""Shared configuration and append-only host accounting for local node execution."""

from collections.abc import Callable
from dataclasses import dataclass

from .disturbance_state import Address3, InitialState, Values, bounded
from .event_resolution import EventResolver, Planner
from .event_space import CausalEventSpace
from .integer import ceil_div, checked_work
from .node_conservation import NodeConservationGuard
from .record_policy import RecordPolicy


def port_count(initial: InitialState) -> int:
    """The fixed local degree is six until a configured topology is supplied."""
    return 6


EventSink = Callable[[dict[str, object]], None]


def cycle_timing(cost: int, budget: int, link_ticks: int) -> tuple[int, int]:
    if min(budget, link_ticks) < 1 or cost < 0:
        raise ValueError("invalid cost, normal budget, or fixed link time")
    cycles = max(1, ceil_div(cost, budget))
    return bounded(checked_work((cycles - 1) * link_ticks)), bounded(checked_work(cycles * link_ticks))


class NodeEvents:
    """Append causal identities and publish diagnostics; never offer graph reads."""

    def __init__(self, space: CausalEventSpace | None, observer: EventSink | None) -> None:
        self.__space = space
        self.__observer = observer

    @property
    def enabled(self) -> bool:
        return self.__space is not None

    def require_room(self, count: int) -> None:
        if self.__space is not None:
            self.__space.require_room(count)

    def record(
        self,
        event: str,
        tick: int,
        position: Address3,
        cause: int | None,
        *,
        causes: tuple[int, ...] = (),
        event_cost: int = 0,
        owner: str = "disturbance",
        **data: object,
    ) -> tuple[int | None, dict[str, object]]:
        identity = None
        if self.__space is not None:
            entry = self.__space.append(
                tick=tick,
                addresses=(position,),
                owner=owner,
                kind=event,
                physical_parents=causes if cause is None else (*causes, cause),
                model_cost=event_cost,
            )
            identity = entry.id
            data = {**data, "event_id": identity, "parents": entry.parents}
        return identity, {"event": event, "tick": tick, "position": position, **data}

    def publish(self, message: dict[str, object]) -> None:
        if self.__observer is not None:
            self.__observer(message)

    def set_observer(self, observer: EventSink | None) -> None:
        """Replace the host notification sink without exposing a read interface."""
        self.__observer = observer


@dataclass(slots=True)
class WorkLedger:
    """Host totals are outputs and must never select a physical proposal."""

    work: int = 0
    cycles: int = 0


class NodeAccounting:
    """Write-side account interface; node code cannot read global audit totals."""

    def __init__(self, ledger: WorkLedger, sources: list[list[int]]) -> None:
        self.__ledger = ledger
        self.__sources = sources

    def charge_cycle(self, cost: int) -> None:
        work = checked_work(self.__ledger.work + cost)
        cycles = checked_work(self.__ledger.cycles + 1)
        self.__ledger.work, self.__ledger.cycles = work, cycles

    def record_sources(self, values: Values) -> None:
        add_audit_delta(self.__sources, values)


def add_audit_delta(target: list[list[int]], values: Values) -> None:
    """Accumulate already validated local output; never produce a physical input."""
    for index, payload in enumerate(values):
        for component, value in enumerate(payload):
            target[index][component] += value


@dataclass(frozen=True, slots=True)
class NodeServices:
    """One shared run definition, law providers and write-side audit services.

    The definition excludes seeds. No world, neighbor lookup or transport index
    is available here. The resolver is the explicit optional quantum extension.
    """

    initial: InitialState
    planner: Planner
    record_policy: RecordPolicy
    events: NodeEvents
    accounting: NodeAccounting
    coupled_types: frozenset[int]
    zero_delays: tuple[int, ...]
    resolver: EventResolver | None = None
    balance_guard: NodeConservationGuard | None = None

    def __post_init__(self) -> None:
        if self.initial.node_execution and (
            self.initial.conservation_contract is None or self.balance_guard is None
        ):
            raise ValueError("node_execution requires a conservation contract and balance guard")
