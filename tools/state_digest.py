"""THE STATE DIGEST of a run, a HOST reading: SHA-256 over what the run is, never over how the code
holds it (the Boss's word on PR #1172): the output lines the run wrote; the engine's own state
stream (`snapshot_stream`: the interval, the bodies' contents, momenta and spins, the held
families' levels and the live records' integers, each under the world file's family names,
record identities and body numbers); every live record's levels now and before and its
remainder; every held family's levels before and its remainder; every read's remainder (by the
reading and the read family's names and the axis); the clicks; and the books. Every key is a name
of the world's files or a word of the ledger, never a Python attribute name, so a cut that renames
or moves the engine's attributes while every run stays bit for bit leaves the digest where it is.
Nothing physical is read: the digest is a HOST reading of the state, bit for bit, never a
measurement. The property tests of `tests/test_genericity.py` compare digests of drawn universes
(a rename or a reorder of the files bit for bit); no shipped world is recorded or replayed (the
owner's decision of 2026-09-27: the worlds recorded on the earlier engine are no reference).
"""

from __future__ import annotations

import dataclasses
import hashlib
from typing import Any

import numpy as np

from event_universe.events.detector_law import DetectorLawSimulation


def canonical(value: Any, out: list[bytes], seen: dict[int, int] | None = None) -> None:
    """The canonical dump: a fixed byte form for every kind of state the engine holds. A
    container met a second time (the engine's objects point at each other) is written as the
    order number of its first visit, so the dump is finite and the same for the same state."""
    if seen is None:
        seen = {}
    if (
        isinstance(value, (list, tuple, dict, set, frozenset))
        or (dataclasses.is_dataclass(value) and not isinstance(value, type))
        or (hasattr(value, "__dict__") and not callable(value) and not isinstance(value, np.ndarray))
    ):
        if id(value) in seen:
            out.append(f"<again {seen[id(value)]}>".encode())
            return
        seen[id(value)] = len(seen)
    if isinstance(value, bool) or value is None or isinstance(value, str):
        out.append(repr(value).encode())
    elif isinstance(value, int):
        # an integer by its bytes, never its decimal string: the books' conserved forms run to
        # thousands of digits (GAMEBOARD readings, ALGEBRA.md #the-direction)
        out.append(b"int " + value.to_bytes((value.bit_length() + 8) // 8, "big", signed=True))
    elif isinstance(value, float):
        out.append(value.hex().encode())
    elif isinstance(value, np.ndarray):
        out.append(f"array {value.dtype} {value.shape} ".encode())
        out.append(np.ascontiguousarray(value).tobytes())
    elif isinstance(value, np.generic):
        canonical(value.item(), out, seen)
    elif isinstance(value, (list, tuple)):
        out.append(b"[")
        for item in value:
            canonical(item, out, seen)
            out.append(b",")
        out.append(b"]")
    elif isinstance(value, dict):
        out.append(b"{")
        for key in sorted(value, key=repr):
            out.append(repr(key).encode())
            out.append(b":")
            canonical(value[key], out, seen)
            out.append(b",")
        out.append(b"}")
    elif isinstance(value, (set, frozenset)):
        canonical(sorted(value, key=repr), out, seen)
    elif dataclasses.is_dataclass(value) and not isinstance(value, type):
        out.append(type(value).__name__.encode())
        canonical({f.name: getattr(value, f.name) for f in dataclasses.fields(value)}, out, seen)
    elif callable(value):
        out.append(b"<callable>")
    elif hasattr(value, "__dict__"):
        out.append(type(value).__name__.encode())
        canonical(vars(value), out, seen)
    else:
        raise TypeError(f"no canonical form for {type(value).__name__}")


def run_reading(simulation: DetectorLawSimulation, lines: list[dict[str, object]]) -> dict[str, Any]:
    """What the run is, under stable names: the output lines, the engine's state stream, the
    records' and the held families' levels and remainders, the clicks
    and the books, every family by its name. The engine's containers are read by their present names (`records`,
    `held_records`, `layer.gathers`): a cut that renames one breaks this reader
    aloud, and the reader follows; the digest never moves on its own."""
    names = [family.name for family in simulation.families]
    records = {
        str(live.identity): {
            "family": names[live.family],
            "now": live.now,
            "before": live.before,
            "remainder": live.remainder,
        }
        for live in simulation.records.values()
    }
    held = {
        names[family]: {"before": record.before, "remainder": record.remainder}
        for family, record in simulation.held_records.items()
    }
    state = dict(simulation.snapshot_stream())
    # the engine lists a body's held stocks and the held families by the family's position in
    # the universe file; the reading names them, so that order is not in the digest
    state["measured"] = [
        {**body, "held": dict(zip(names, body["held"], strict=True))} for body in state["measured"]
    ]
    state["held_fields"] = {
        field["family"]: {key: value for key, value in field.items() if key != "family"}
        for field in state["held_fields"]
    }
    return {
        "lines": lines,
        "state": state,
        "records": records,
        "held families": held,
        "clicks": simulation.layer.gathers,
        "books": simulation.books(),
    }


def digest_of(reading: dict[str, Any]) -> str:
    parts: list[bytes] = []
    canonical(reading, parts)
    return hashlib.sha256(b"".join(parts)).hexdigest()
