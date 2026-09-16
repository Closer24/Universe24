"""Host-only indexed deadlines for actual Register work, without stale entries."""

from .disturbance_state import Address3, bounded
from .register_contracts import WorkKind

QueueKey = tuple[Address3, int, WorkKind, int]


class DeadlineQueue:
    """An indexed minimum heap retains exactly one entry per live work handle.

    Replacing or cancelling a deadline removes its old heap entry immediately.
    Queue entries contain scheduling metadata only, never physical payloads.
    Work and memory here are host costs, not a local physical operation charge.
    """

    def __init__(self) -> None:
        self._heap: list[tuple[int, QueueKey]] = []
        self._positions: dict[QueueKey, int] = {}
        self.popped = 0
        self.peak_entries = 0

    def __len__(self) -> int:
        return len(self._heap)

    def _swap(self, first: int, second: int) -> None:
        self._heap[first], self._heap[second] = self._heap[second], self._heap[first]
        self._positions[self._heap[first][1]] = first
        self._positions[self._heap[second][1]] = second

    def _up(self, index: int) -> int:
        while index:
            parent = (index - 1) // 2
            if self._heap[parent] <= self._heap[index]:
                break
            self._swap(parent, index)
            index = parent
        return index

    def _down(self, index: int) -> None:
        while 2 * index + 1 < len(self._heap):
            child = 2 * index + 1
            if child + 1 < len(self._heap) and self._heap[child + 1] < self._heap[child]:
                child += 1
            if self._heap[index] <= self._heap[child]:
                break
            self._swap(index, child)
            index = child

    @staticmethod
    def _validate(key: QueueKey, tick: int) -> None:
        node, port, kind, index = key
        if len(node) != 3 or any(type(value) is not int or value < 0 for value in node):
            raise ValueError("queue Node address must contain three nonnegative integers")
        if type(port) is not int or not 0 <= port < 6:
            raise ValueError("queue requires one of six Register Ports")
        if kind not in ("compute", "commit", "arrival"):
            raise ValueError("unsupported Register deadline kind")
        if type(index) is not int or not 0 <= index < 192 or (kind != "arrival" and index != 0):
            raise ValueError("deadline index exceeds the fixed owner capacity")
        if type(tick) is not int or bounded(tick) < 0:
            raise ValueError("deadline must be a bounded nonnegative integer")

    def set(self, key: QueueKey, tick: int) -> None:
        """Insert or replace one live deadline without retaining cancelled history."""
        self._validate(key, tick)
        if key in self._positions:
            index = self._positions[key]
            self._heap[index] = (tick, key)
            self._down(self._up(index))
        else:
            self._positions[key] = len(self._heap)
            self._heap.append((tick, key))
            self._up(len(self._heap) - 1)
        self.peak_entries = max(self.peak_entries, len(self._heap))

    def cancel(self, key: QueueKey) -> None:
        """Remove an existing handle; cancelling an absent handle has no effect."""
        index = self._positions.pop(key, None)
        if index is None:
            return
        last = self._heap.pop()
        if index < len(self._heap):
            self._heap[index] = last
            self._positions[last[1]] = index
            self._down(self._up(index))

    def take(self, tick: int) -> tuple[QueueKey, ...]:
        """Consume only work due at this phase's tick; skipped deadlines fault."""
        if self._heap and self._heap[0][0] < tick:
            raise ValueError("a Register deadline was skipped")
        ready = []
        while self._heap and self._heap[0][0] == tick:
            key = self._heap[0][1]
            self.cancel(key)
            ready.append(key)
        self.popped += len(ready)
        return tuple(ready)

    def report(self) -> dict[str, int]:
        return {"entries": len(self), "peak_entries": self.peak_entries, "popped": self.popped}
