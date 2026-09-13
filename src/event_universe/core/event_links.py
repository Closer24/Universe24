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


@dataclass(frozen=True, slots=True)
class EventPredecessor:
    stream_id: int
    event_id: int | None
