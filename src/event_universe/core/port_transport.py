"""External causal Link deadlines retain handles to the existing PortBank owners."""

from .deadline_queue import DeadlineQueue, QueueKey
from .disturbance_state import Address3
from .register_contracts import OutgoingIntent


class PortTransport:
    """Schedule actual outgoing slots and retain reference bank-creation order."""

    def __init__(self) -> None:
        self.deadlines = DeadlineQueue()
        self._order: dict[Address3, int] = {}

    def register_owner(self, node: Address3) -> None:
        if node not in self._order:
            self._order[node] = len(self._order)

    def schedule(self, node: Address3, intents: tuple[OutgoingIntent, ...], tick: int) -> None:
        self.register_owner(node)
        if len(intents) > 192:
            raise ValueError("outgoing handles exceed the fixed Node PortBank capacity")
        for intent in intents:
            if intent.arrival_tick <= tick:
                raise ValueError("an outgoing Link must arrive strictly after the current tick")
            self.deadlines.set((node, intent.port, "arrival", intent.slot), intent.arrival_tick)

    def take(self, tick: int) -> tuple[QueueKey, ...]:
        return tuple(sorted(self.deadlines.take(tick), key=lambda key: (self._order[key[0]], key[3])))
