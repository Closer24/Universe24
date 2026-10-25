"""Hand y1's shared readings (2026-10-25): the bare 3-cube hole seed of the tests' small universe, a full snapshot of every array as Python's integers, its digest, and the cube's 48 as signed permutations about the origin. Integers only; no float anywhere."""
from __future__ import annotations

import hashlib
import itertools
import json
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))  # tests.laws_universe
from event_universe import world_files  # noqa: E402
from event_universe.lattice import Lattice  # noqa: E402
from event_universe.world_files import load_world  # noqa: E402
from tests.laws_universe import bare_torus  # noqa: E402


def board_of(folder: Path, lines: list | None = None, cube: int = 3) -> Lattice:
    folder.mkdir(parents=True, exist_ok=True)
    world_files.REPOSITORY_ROOT = folder
    return Lattice(load_world(bare_torus(folder, cube)), output=None if lines is None else lines.append)


def ints(a) -> list[int]:
    return [int(x) for x in np.asarray(a, dtype=object).reshape(-1)]


def snapshot(board: Lattice) -> dict[str, list[int]]:
    """Every array of every family's state as Python's integers, keyed by family, kind and number."""
    found: dict[str, list[int]] = {}
    for i, s in enumerate(board.states):
        name = board.families[i].name
        for n, line in enumerate(s.lines):
            for part, a in (("now", line.now), ("before", line.before), ("remainder", line.remainder)):
                found[f"{name} line {n} {part}"] = ints(a)
        for n, w in enumerate(s.write_remainders):
            found[f"{name} write {n}"] = ints(w)
        for r, row in enumerate(s.phases):
            for n, line in enumerate(row):
                for part, a in (("now", line.now), ("before", line.before), ("remainder", line.remainder)):
                    found[f"{name} row {r} phase {n} {part}"] = ints(a)
    found["interval"] = [int(board.interval)]
    return found


def digest(snap: dict[str, list[int]]) -> str:
    return hashlib.sha256(json.dumps(snap, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


def bits_of(snap: dict[str, list[int]]) -> tuple[int, str]:
    found = (0, "")
    for key, values in snap.items():
        if key == "interval":
            continue
        b = max((abs(v).bit_length() for v in values), default=0)
        if b > found[0]:
            found = (b, key)
    return found


def count_of(snap: dict[str, list[int]]) -> int:
    """The integers one Node holds: the arrays' count (every array one integer per Node)."""
    return sum(1 for key in snap if key != "interval")


def signed_permutations() -> list[tuple[tuple[int, int, int], tuple[int, int, int]]]:
    """The 48 as (pi, s): the axis a goes to pi[a] with the sign s[a]."""
    return [
        (pi, s) for pi in itertools.permutations(range(3)) for s in itertools.product((1, -1), repeat=3)
    ]


def image_of(a: np.ndarray, pi: tuple[int, int, int], s: tuple[int, int, int]) -> np.ndarray:
    """The array carried by the signed permutation about the origin: B[g x] = A[x], g e_a = s_a e_pi(a); on the torus the reflection is i -> (-i) mod n about the origin."""
    inverse = [pi.index(b) for b in range(3)]  # the source axis of each image axis
    moved = np.transpose(np.asarray(a, dtype=object), inverse)
    for b in range(3):
        if s[inverse[b]] < 0:
            n = moved.shape[b]
            moved = np.take(moved, [(-i) % n for i in range(n)], axis=b)
    return moved
