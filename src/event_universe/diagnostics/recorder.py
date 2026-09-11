"""Optional observers. Growing history belongs here, never in physical cell state."""

import json
from collections import defaultdict
from typing import TextIO

from event_universe.core.contracts import CollisionRecord, ForceRecord, MoveRecord


class TraceRecorder:
    """In-memory compatibility trace for small experiments and regression tests."""

    def __init__(self) -> None:
        self.paths: dict[int, list[tuple[int, int, int, int]]] = defaultdict(list)
        self.force_records: list[ForceRecord] = []
        self.collisions: list[MoveRecord] = []
        self.collision_records: list[CollisionRecord] = []

    def on_move(self, event: MoveRecord) -> None:
        self.paths[event.pid].append((event.tick, event.x, event.y, event.z))

    def on_force(self, event: ForceRecord) -> None:
        self.force_records.append(event)

    def on_blocked(self, event: MoveRecord) -> None:
        self.collisions.append(event)

    def on_collision(self, event: CollisionRecord) -> None:
        self.collision_records.append(event)


class JsonlRecorder:
    """Stream immutable events to a caller-owned file without retaining their history."""

    def __init__(self, stream: TextIO) -> None:
        self.stream = stream

    def _write(self, kind: str, event: MoveRecord | ForceRecord) -> None:
        self.stream.write(json.dumps({"kind": kind, **event._asdict()}) + "\n")

    def on_move(self, event: MoveRecord) -> None:
        self._write("move", event)

    def on_force(self, event: ForceRecord) -> None:
        self._write("force", event)

    def on_blocked(self, event: MoveRecord) -> None:
        self._write("blocked_move", event)

    def on_collision(self, event: CollisionRecord) -> None:
        data = event._asdict()
        for name in ("before_first", "before_second", "after_first", "after_second"):
            data[name] = getattr(event, name)._asdict()
        self.stream.write(json.dumps({"kind": "particle_collision", **data}) + "\n")
