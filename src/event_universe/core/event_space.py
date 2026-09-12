"""Bounded, domain-neutral event identities and explicitly typed causal edges.

This host ledger stores provenance, not physical inventories or wave amplitudes.
A dependency edge never grants a physical cell permission to read its ancestor.
"""

from dataclasses import dataclass

from .disturbance_state import Address3, bounded
from .integer import checked_work
from .topology import neighbor_address


@dataclass(frozen=True, slots=True)
class CausalEvent:
    id: int
    tick: int
    addresses: tuple[Address3, ...]
    owner: str
    kind: str
    parents: tuple[int, ...]
    physical_parents: tuple[int, ...]
    payload_ref: int
    model_cost: int = 0


class CausalEventSpace:
    """One append-only identity namespace; payloads remain with their owners.

    Bounded-degree insertion checks direct parents only. Ancestor traversal is a
    separate host operation, never part of an ordinary physical local update.
    Retention is bounded and fail-stop; this is not infinite-history compression.
    """

    def __init__(
        self,
        capacity: int = 100_000,
        *,
        shape: Address3 | None = None,
        boundary: str = "open",
        link_ticks: int = 1,
    ) -> None:
        if bounded(capacity) < 1 or bounded(link_ticks) < 1:
            raise ValueError("positive event capacity and link time required")
        if boundary not in ("open", "periodic"):
            raise ValueError("unknown event-space boundary")
        if shape is not None and (len(shape) != 3 or any(bounded(x) < 1 for x in shape)):
            raise ValueError("invalid event-space shape")
        self.capacity = capacity
        self.shape = shape
        self.boundary = boundary
        self.link_ticks = link_ticks
        self._events: list[CausalEvent] = []
        self._cost = 0

    @property
    def next_id(self) -> int:
        return len(self._events)

    @property
    def events(self) -> tuple[CausalEvent, ...]:
        return tuple(self._events)

    @property
    def model_cost(self) -> int:
        return self._cost

    def event(self, event_id: int) -> CausalEvent:
        if not 0 <= bounded(event_id) < self.next_id:
            raise ValueError("unknown causal event identity")
        return self._events[event_id]

    def require_room(self, count: int) -> None:
        if bounded(count) < 0 or self.next_id + count > self.capacity:
            raise OverflowError("causal event capacity exceeded")

    def _causal(self, parent: CausalEvent, addresses: tuple[Address3, ...], tick: int) -> bool:
        for a in parent.addresses:
            for b in addresses:
                if a == b and parent.tick <= tick:
                    return True
                if tick - parent.tick < self.link_ticks:
                    continue
                if self.shape is None:
                    if sum(abs(checked_work(x - y)) for x, y in zip(a, b, strict=True)) == 1:
                        return True
                elif any(neighbor_address(a, port, self.shape, self.boundary) == b for port in range(6)):
                    return True
        return False

    def append(
        self,
        *,
        tick: int,
        addresses: tuple[Address3, ...],
        owner: str,
        kind: str,
        parents: tuple[int, ...] = (),
        physical_parents: tuple[int, ...] = (),
        payload_ref: int = 0,
        model_cost: int = 0,
    ) -> CausalEvent:
        self.require_room(1)
        if bounded(tick) < 0 or bounded(model_cost) < 0 or bounded(payload_ref) < 0:
            raise ValueError("negative event time, cost or payload reference")
        if not owner or not kind or len(owner) > 128 or len(kind) > 128:
            raise ValueError("bounded nonempty owner and kind required")
        if type(addresses) is not tuple or not 1 <= len(addresses) <= 30:
            raise ValueError("bounded immutable event support required")
        for address in addresses:
            if type(address) is not tuple or len(address) != 3:
                raise ValueError("three integer coordinates required")
            for axis, value in enumerate(address):
                bounded(value)
                if self.shape is not None and not 0 <= value < self.shape[axis]:
                    raise ValueError("event outside physical domain")
        if type(parents) is not tuple or type(physical_parents) is not tuple:
            raise TypeError("immutable parent tuples required")
        if len(parents) + len(physical_parents) > 256:
            raise ValueError("event parent inputs exceed fixed bound")
        all_parents = tuple(dict.fromkeys((*parents, *physical_parents)))
        if len(all_parents) > 256:
            raise ValueError("event parent fan-in exceeds fixed bound")
        for identity in all_parents:
            parent = self.event(identity)
            if parent.tick > tick:
                raise ValueError("event cannot depend on a future record")
            if identity in physical_parents and not self._causal(parent, addresses, tick):
                raise ValueError("physical cause lacks a completed local link")
        cost = checked_work(self._cost + model_cost)
        event = CausalEvent(
            self.next_id,
            tick,
            addresses,
            owner,
            kind,
            all_parents,
            tuple(dict.fromkeys(physical_parents)),
            payload_ref,
            model_cost,
        )
        self._events.append(event)
        self._cost = cost
        return event

    def ancestors(self, root: int) -> tuple[int, ...]:
        """Read-only diagnostic traversal; no physical result or clock mutation."""
        found: set[int] = set()
        pending = [root]
        while pending:
            identity = pending.pop()
            if identity not in found:
                found.add(identity)
                pending.extend(self.event(identity).parents)
        return tuple(sorted(found))
