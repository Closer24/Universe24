"""Shared pieces of hand V2's measurements (2026-10-25, the pump and light's redshift): the worktree's root on the path, the tests' small universe written beside a world file of any shape, the volume's time line and its three tension lines imposed by hand at every interval (the content the Nodes read set from outside, the volume's write off), and the paces at a content with the integer readings derived from them (the owner's word, Addition 3: no float in a reader; a float stands only as a named check beside its integer reading). Nothing here edits src/; every function is a reading or an imposition on a Lattice the engine built."""

from __future__ import annotations

import json
import math
import sys
from dataclasses import replace
from pathlib import Path
from typing import Any

import numpy as np

HERE = Path(__file__).resolve()
ROOT = HERE.parents[3]  # the worktree's root: tools/derivations/v2/common.py
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from event_universe import records, world_files  # noqa: E402
from event_universe.core import paces, rule3  # noqa: E402
from event_universe.core.ports import LINK_UNIT  # noqa: E402
from event_universe.core.rule3 import division_forward  # noqa: E402
from event_universe.features import volume  # noqa: E402
from event_universe.lattice import Lattice  # noqa: E402
from event_universe.world_files import load_world  # noqa: E402
from tests.laws_universe import GAMMA, SMALL, small_universe  # noqa: E402

DEN = SMALL["integers"]["den"]
ACTION = SMALL["integers"]["quantum_action"]
SCALE = 10**6  # the fixed scale of a quotient read to six digits, an integer reading with its remainder
OUT = HERE.parent  # the outputs beside the scripts


def quotient(numerator: int, wall: int) -> dict[str, int]:
    """An integer reading of a ratio: the quotient and the remainder of the one carried division at the wall (core/rule3.division_forward), and the bit length of the numerator (the width's check)."""
    found, rest = division_forward(numerator, wall, 0)
    return {"quotient": int(found), "remainder": int(rest), "wall": int(wall), "bits": int(numerator).bit_length()}


def scaled(numerator: int, wall: int) -> int:
    """The ratio numerator / wall read to the fixed scale as one integer, (numerator x SCALE) div wall."""
    return int(division_forward(numerator * SCALE, wall, 0)[0])


def world_of(folder: Path, shape: tuple[int, int, int], intervals: int = 60) -> Path:
    """The folded world's three keys on a torus of `shape` with the tests' small universe beside it."""
    folder.mkdir(parents=True, exist_ok=True)
    small_universe(folder)
    world = {"universe": "u.json", "shape": list(shape), "intervals": intervals}
    path = folder / "bare.json"
    path.write_text(json.dumps(world), encoding="utf-8")
    world_files.REPOSITORY_ROOT = folder
    return path


def lattice_of(folder: Path, shape: tuple[int, int, int], lines: list | None = None) -> Lattice:
    """A Lattice of the small universe on a torus of `shape`, its output lines kept where `lines` is given."""
    return Lattice(load_world(world_of(folder, shape)), output=None if lines is None else lines.append)


def write_off(board: Lattice) -> None:
    """The volume holder's one write weighed 0 (a reading-side replacement of the loader's row, no line of src/ changed): the held row's numerators are the write weight times the sources' bookings, so the volume's time line and its tension lines take no write and the content the Nodes read is the one imposed by hand."""
    held = board.held[0]
    board.families = tuple(
        replace(family, write_weight=0) if index == held else family
        for index, family in enumerate(board.families)
    )


def impose_volume(board: Lattice, now: int, before: int) -> None:
    """The volume holder's time line set at every Node to (now, before) and its three tension lines to 0, the remainders as they stand: the content every record reads at the interval's start is the level of `now`, and no tension stands on any Link (every Link's factor G^2)."""
    state = board.states[board.held[0]]
    kind = board.kind
    lines = list(state.lines)
    lines[0] = records.Record(
        records.full(board.shape, now, kind), records.full(board.shape, before, kind), lines[0].remainder
    )
    for axis in range(1, 4):
        lines[axis] = records.Record(
            records.zeros(board.shape, kind), records.zeros(board.shape, kind), lines[axis].remainder
        )
    state.lines = lines


def volume_at(level: int) -> int:
    """The volume X of a content level a, the engine's own conversion (features/volume `volume_of`)."""
    return int(
        np.asarray(volume.volume_of(GAMMA, np.array([level], dtype=object)), dtype=object).reshape(-1)[0]
    )


def paces_at(level: int) -> dict[str, Any]:
    """The composed paces at a content level and the integer readings derived from them: p_0, p_a (core/paces), the clock's ratio e^U = Gamma / p_0 and the frame's weight (Gamma / p_a)^2 each as a quotient with its remainder at the scale, the massless line's reach R and the wall w of the small universe; the float U = ln(Gamma / p_0) a named check beside them."""
    p_0, p_a = paces.node_paces(GAMMA, level)
    p_0, p_a = int(p_0), int(p_a)
    wall = rule3.wall_of(DEN, GAMMA, LINK_UNIT)
    reach = 2 * DEN * p_a * p_a * LINK_UNIT * LINK_UNIT
    return {
        "level": level,
        "p_0": p_0,
        "p_a": p_a,
        "e_U_scaled": scaled(GAMMA, p_0) if p_0 else None,
        "weight_scaled": scaled(GAMMA * GAMMA, p_a * p_a) if p_a else None,
        "check_U_float": math.log(GAMMA / p_0) if p_0 else None,
        "w": wall,
        "R": reach,
    }


def dump(name: str, found: Any) -> Path:
    """The measurement written beside the scripts as JSON."""
    path = OUT / name
    path.write_text(json.dumps(found, indent=1, default=str), encoding="utf-8")
    return path
