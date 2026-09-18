"""The final snapshot written Node by Node (the performance review of 2026-09-18).

`state.json` is the world's snapshot as JSON text, byte for byte
`json.dumps(world.snapshot(), indent=2)`; `snapshot` holds every Node of the
board as an object at once, and on a board that a field fills the dense
region's Nodes read back as Node state cost about 16 KB each before the text
is built, which is what killed the r = 20 runner of A5s Run 2 at 11.4 GB
(docs/EXPERIMENTS.md). This host module writes the same text from
`DisturbanceEngine.snapshot_stream`, the per-Node lists one entry at a time,
the dense region's Nodes read one at a time from its arrays one x-slab at a
time (`SpatialEngine.snapshot_nodes`), so the peak memory of the final
snapshot is the arrays plus one slab's positions, one Node's state and one
entry's text. Nothing of the physics is read here: the entries are the
engine's, this module only lays them out as the JSON encoder does.
"""

from __future__ import annotations

import json
from collections.abc import Iterator
from typing import IO

from event_universe.core.disturbance_engine import DisturbanceEngine

INDENT = 2


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


def write_snapshot(world: DisturbanceEngine, stream: IO[str]) -> None:
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
