"""Independent full-register audits for component preparations and trajectories.

The routing oracle is derived from exact 4x4 matrices in research.reference;
no production coupling table, scalar updater, or State constructor is used.
This module reads completed data and has no role in forward evolution.
"""
from __future__ import annotations

from dataclasses import dataclass
from functools import lru_cache
import hashlib
import gzip
import json
from pathlib import Path
from types import MappingProxyType

from research.reference.algebra import DIRECTIONS, coupling as matrix_coupling


def digest_file(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def _triple(value):
    value = tuple(value)
    if len(value) != 3 or any(type(item) is not int for item in value):
        raise ValueError("Expected three exact integer coordinates")
    if not 0 <= value[2] < 6:
        raise ValueError("Remainder outside 0..5")
    return value


@dataclass(frozen=True)
class Snapshot:
    side: int
    background: tuple
    cells: object

    def __post_init__(self):
        if type(self.side) is not int or self.side < 3:
            raise ValueError("Expected cube side >= 3")
        background = _triple(self.background)
        if background[:2] != (0, 0):
            raise ValueError("Sparse background must have zero counters")
        cells = {}
        for key, value in self.cells.items():
            address = tuple(key)
            if (len(address) != 4 or any(type(c) is not int for c in address)
                    or not all(0 <= c < self.side for c in address[:3])
                    or not 0 <= address[3] < 48):
                raise ValueError("Invalid complete channel address")
            value = _triple(value)
            if value != background:
                cells[address] = value
        object.__setattr__(self, "background", background)
        object.__setattr__(self, "cells", MappingProxyType(cells))

    def at(self, address):
        return self.cells.get(tuple(address), self.background)

    def canonical(self):
        return {"side": self.side, "background": list(self.background),
                "cells": [[*address, *value]
                          for address, value in sorted(self.cells.items())]}


def from_state(state):
    """Copy a production state for comparison, without trusting its updater."""
    return Snapshot(state.cube.side, tuple(state.background), dict(state.cells))


def from_checkpoint(checkpoint):
    if checkpoint["format"] != "universe24-checkpoint-v1":
        raise ValueError("Unknown checkpoint format")
    experiment = checkpoint["experiment"]
    cells = {}
    for entry in experiment["seed_changes"]:
        address = (*entry["position"], entry["channel"])
        if address in cells:
            raise ValueError("Duplicate checkpoint address")
        cells[address] = tuple(entry["state"])
    return Snapshot(experiment["side"], tuple(experiment["background"]), cells)


@lru_cache(maxsize=8)
def _routing(signs):
    reference = matrix_coupling(signs)
    inverse_rows = tuple({sender: receiver for receiver, sender in enumerate(row)}
                         for row in reference.ports)
    return reference, inverse_rows


def coupling_fingerprint(signs):
    reference, _ = _routing(tuple(signs))
    blob = json.dumps(["universe24-2O-body-013-v1", reference.ports,
                       reference.weights], separators=(",", ":")).encode()
    return hashlib.sha256(blob).hexdigest()


def _step(old, signs, reverse):
    reference, inverse_rows = _routing(tuple(signs))
    component = 0 if reverse else 1
    candidates = set(old.cells)
    for (x, y, z, sender), value in old.cells.items():
        if not value[component]:
            continue
        for d, (dx, dy, dz) in enumerate(DIRECTIONS):
            candidates.add(((x-dx) % old.side, (y-dy) % old.side,
                            (z-dz) % old.side, inverse_rows[d][sender]))
    values = {}
    for address in candidates:
        x, y, z, receiver = address
        a, b, r = old.at(address)
        incoming = sum(reference.weights[d][receiver] * old.at(
            ((x+dx) % old.side, (y+dy) % old.side, (z+dz) % old.side,
             reference.ports[d][receiver]))[component]
            for d, (dx, dy, dz) in enumerate(DIRECTIONS))
        if reverse:
            offset = r - 2*incoming
            prior_r = offset - 6*(offset//6)
            value = ((2*incoming + prior_r - r)//6 - b, a, prior_r)
        else:
            numerator = 2*incoming + r
            quotient = numerator//6
            value = (b, quotient-a, numerator - 6*quotient)
        if value != old.background:
            values[address] = value
    return Snapshot(old.side, old.background, values)


def advance(old, signs=(1, 1, 1)):
    return _step(old, tuple(signs), False)


def rewind(new, signs=(1, 1, 1)):
    return _step(new, tuple(signs), True)


def net_inputs(state, addresses, signs=(1, 1, 1)):
    reference, _ = _routing(tuple(signs))
    result = []
    for x, y, z, channel in addresses:
        result.append(sum(reference.weights[d][channel] * state.at(
            ((x+dx) % state.side, (y+dy) % state.side, (z+dz) % state.side,
             reference.ports[d][channel]))[1]
            for d, (dx, dy, dz) in enumerate(DIRECTIONS)))
    return result


def transition_events(before, after, addresses):
    """Read C and R separately; an R change alone is never a C event."""
    arithmetic, remainder = [], []
    for address in addresses:
        address = tuple(address)
        old, new = before.at(address), after.at(address)
        if new[2] != old[2]:
            remainder.append(address)
        quotient = new[1] + old[0]
        if quotient != 0 and new != old:
            arithmetic.append({"address": address, "quotient": quotient,
                               "kind": ((new[2]-old[2])//2) % 3})
    return {"arithmetic": arithmetic, "remainder": remainder}


def audit_checkpoints(path, *, expected_initial=None, expected_signs=None):
    """Verify every retained channel and independent inverse in one JSONL trace."""
    path = Path(path)
    raw = gzip.decompress(path.read_bytes()).decode() if path.suffix == ".gz" else path.read_text()
    records = [json.loads(line) for line in raw.splitlines() if line]
    if not records:
        raise AssertionError("Empty trajectory")
    previous = initial = None
    signs = None
    for index, record in enumerate(records):
        if record["completed_steps"] != index:
            raise AssertionError(("Unexpected step index", index))
        here_signs = tuple(record["experiment"]["coupling_signs"])
        if signs is None:
            signs = here_signs
        if here_signs != signs or (expected_signs is not None
                                   and signs != tuple(expected_signs)):
            raise AssertionError("Coupling changed or differs from registered signs")
        if record["coupling_fingerprint"] != coupling_fingerprint(signs):
            raise AssertionError("Checkpoint tensor fingerprint differs from independent construction")
        current = from_checkpoint(record)
        if previous is None:
            initial = current
            if expected_initial is not None and current != expected_initial:
                raise AssertionError("Initial state differs from independent preparation")
        else:
            if advance(previous, signs) != current:
                raise AssertionError(("Independent forward mismatch", index))
            if rewind(current, signs) != previous:
                raise AssertionError(("Independent inverse mismatch", index))
        previous = current
    return {"path": str(path), "frames": len(records),
            "transitions": len(records)-1, "forward_and_inverse_passed": True,
            "source_sha256": digest_file(__file__), "trace_sha256": digest_file(path),
            "coupling_signs": list(signs),
            "initial_state_sha256": hashlib.sha256(json.dumps(
                initial.canonical(), sort_keys=True, separators=(",", ":")).encode()).hexdigest()}

