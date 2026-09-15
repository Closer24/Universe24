"""Bounded host reuse of pure, immutable local transition results."""

from collections import OrderedDict
from collections.abc import Callable, Hashable


class _ReuseKey[Key: Hashable]:
    """Hash the complete immutable input once; equality still checks its values."""

    __slots__ = ("value", "code")

    def __init__(self, value: Key) -> None:
        self.value = value
        self.code = hash(value)

    def __hash__(self) -> int:
        return self.code

    def __eq__(self, other: object) -> bool:
        return isinstance(other, _ReuseKey) and self.value == other.value


class PlanReuse[Key: Hashable, Value]:
    """Share computation, never physical ownership, time or modeled charges.

    One instance belongs to one immutable law in one simulation. Keys contain
    every argument to that law. Only successful immutable results may be reused.
    Caller certification of purity is required; arbitrary plugins are not cached.
    """

    def __init__(self, capacity: int = 4096) -> None:
        if type(capacity) is not int or capacity < 0:
            raise ValueError("plan reuse capacity must be a nonnegative integer")
        self.capacity = capacity
        self._entries: OrderedDict[_ReuseKey[Key], Value] = OrderedDict()
        self.requests = 0
        self.evaluations = 0
        self.hits = 0

    def resolve(
        self, keys: tuple[Key, ...], evaluate: Callable[[tuple[Key, ...]], tuple[Value, ...]]
    ) -> tuple[Value, ...]:
        self.requests += len(keys)
        if not self.capacity:
            self.evaluations += len(keys)
            return evaluate(keys)
        prepared = tuple(_ReuseKey(key) for key in keys)
        found: dict[_ReuseKey[Key], Value] = {}
        missing: dict[_ReuseKey[Key], None] = {}
        for key in prepared:
            if key in found or key in missing:
                self.hits += 1
            elif key in self._entries:
                found[key] = self._entries[key]
                self._entries.move_to_end(key)
                self.hits += 1
            else:
                missing[key] = None
        if missing:
            self.evaluations += len(missing)
            values = evaluate(tuple(key.value for key in missing))
            if len(values) != len(missing):
                raise ValueError("planner result count differs from request count")
            for key, value in zip(missing, values, strict=True):
                found[key] = value
                self._entries[key] = value
                if len(self._entries) > self.capacity:
                    self._entries.popitem(last=False)
        return tuple(found[key] for key in prepared)

    def one(self, key: Key, evaluate: Callable[[], Value]) -> Value:
        """Avoid temporary batch dictionaries on the ordinary serial path."""
        self.requests += 1
        if not self.capacity:
            self.evaluations += 1
            return evaluate()
        prepared = _ReuseKey(key)
        try:
            result = self._entries[prepared]
        except KeyError:
            self.evaluations += 1
            result = evaluate()
            self._entries[prepared] = result
            if len(self._entries) > self.capacity:
                self._entries.popitem(last=False)
        else:
            self.hits += 1
            self._entries.move_to_end(prepared)
        return result

    def report(self) -> dict[str, int]:
        return {
            "capacity": self.capacity,
            "entries": len(self._entries),
            "requests": self.requests,
            "evaluations": self.evaluations,
            "hits": self.hits,
        }

    def clear(self) -> None:
        self._entries.clear()
