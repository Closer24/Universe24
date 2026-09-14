"""Fixed-size local references; event history and domain payloads live elsewhere."""

from dataclasses import dataclass


@dataclass(slots=True, eq=False)
class EventCursor:
    """A shared handle advanced only by its event-space owner.

    Public properties are read-only. A Node holds these three integers, never a
    growing list or an executable rule. Host compaction preserves physical time.
    """

    _stream_id: int
    _event_id: int | None = None
    _physical_tick: int = 0

    @property
    def stream_id(self) -> int:
        return self._stream_id

    @property
    def head(self) -> int | None:
        return self._event_id

    @property
    def physical_tick(self) -> int:
        return self._physical_tick


@dataclass(slots=True, eq=False)
class EventReferences:
    """Fixed local origin identities and the latest interaction marker."""

    _origins: tuple[int, ...] = ()
    _event_id: int | None = None
    _consumed_id: int | None = None

    @property
    def origins(self) -> tuple[int, ...]:
        return self._origins

    @property
    def event_id(self) -> int | None:
        return self._event_id

    @property
    def consumed_id(self) -> int | None:
        return self._consumed_id

    def replace(self, origins: tuple[int, ...], event_id: int | None) -> None:
        """Validate the complete bounded update before publishing either value."""
        from .disturbance_state import bounded

        if type(origins) is not tuple or len(origins) > 6:
            raise ValueError("at most six immutable origin identities required")
        if any(bounded(origin) < 0 for origin in origins):
            raise ValueError("nonnegative origin identities required")
        if len(set(origins)) != len(origins):
            raise ValueError("distinct origin identities required")
        if event_id is not None and bounded(event_id) < 0:
            raise ValueError("nonnegative event identity required")
        self._origins = origins
        self._event_id = event_id

    def consume(self) -> None:
        self._consumed_id = self._event_id
