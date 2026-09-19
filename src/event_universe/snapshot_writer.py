"""The final snapshot written Node by Node.

`state.json` is the world's snapshot as JSON text, byte for byte
`json.dumps(world.snapshot(), indent=2)`, written from the engine's
`snapshot_stream` one entry at a time so that a filled board is never held as
one object (the performance review of 2026-09-18, docs/EXPERIMENTS.md).
Nothing of the physics is read here: the entries are the engine's, this module
only lays them out as the JSON encoder does.
"""

from __future__ import annotations

import json
from collections.abc import Iterator
from typing import IO, Protocol

INDENT = 2


class SnapshotSource(Protocol):
    """A world whose snapshot streams as (key, value) pairs
    (`RaySimulation.snapshot_stream`)."""

    def snapshot_stream(self) -> Iterator[tuple[str, object]]: ...


def _nested(text: str, depth: int) -> str:
    """The text of one value encoded at depth 0, moved to `depth`: every line
    break gains the depth's indentation (an encoded string holds no line break)."""
    return text.replace("\n", "\n" + " " * (INDENT * depth))


def _write_list(stream: IO[str], items: Iterator[object], depth: int) -> None:
    """A list at `depth`, its items one at a time, laid out as the encoder lays
    out a list with `indent`: `[]` when empty, else one item per line."""
    stream.write("[")
    empty = True
    for item in items:
        stream.write(("" if empty else ",") + "\n" + " " * (INDENT * (depth + 1)))
        stream.write(_nested(json.dumps(item, indent=INDENT), depth + 1))
        empty = False
    stream.write("]" if empty else "\n" + " " * (INDENT * depth) + "]")


def write_snapshot(world: SnapshotSource, stream: IO[str]) -> None:
    """Write the world's snapshot to `stream` as `json.dumps(world.snapshot(),
    indent=2)` would, one Node at a time (no trailing line break)."""
    stream.write("{")
    first = True
    for key, value in world.snapshot_stream():
        stream.write(("" if first else ",") + "\n" + " " * INDENT + json.dumps(key) + ": ")
        first = False
        if isinstance(value, Iterator):
            _write_list(stream, value, 1)
        else:
            stream.write(_nested(json.dumps(value, indent=INDENT), 1))
    stream.write("}" if first else "\n}")
