"""The world's key `uniform` (ALGEBRA.md, The closed lattice has no rest; item 6 of what is open, the closed board's double root): its one value `carried`, the board's declaration that its held rows' uniform mode is carried by Rule3's own line at k = 0 on a board periodic on every axis (`uniform_of`, `UNIFORM`, `CARRIED`), read by loader/world.py into `World.uniform` and by features/start `rest`."""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from event_universe.loader.keys import AXES

UNIFORM, CARRIED = "uniform", "carried"  # the board's uniform mode carried where no face sinks it


def uniform_of(value: object, faces: Mapping[str, Any]) -> bool:
    """The world's key `uniform` (ALGEBRA.md, The closed lattice has no rest; item 6 of what is open, the closed board's double root; the build of 2026-10-21): its one value `carried`, the board's declaration that its held rows' uniform mode, the k = 0 component the massless row's rest cannot carry on a board with no sink, is carried by Rule3's own line at k = 0 (the double root: every Node's level and the level before step their uniform part exactly, the one write per interval adds the sources' mean; `Lattice.step`, features/start `rest`), the rest solved for the zero-mean part; refused by name at any other value, and refused by name where a face is open or closed: a board with a sink has no free uniform mode, its rest sinks the sources' mean through the face (the open board's wells, 3 / (4 pi r) far), and nothing is carried there; the massless row's other double root, the staggered mode, stays refused on every even box (`even_box_refused`)."""
    if value != CARRIED:
        raise ValueError(
            f"{UNIFORM} is {CARRIED!r} where the board carries its held rows' uniform mode, got {value!r}"
        )
    sunk = [axis for axis in AXES if faces[axis] != "periodic"]
    if sunk:
        raise ValueError(
            f"{UNIFORM}: {CARRIED} on a board whose {sunk[0]} face is {faces[sunk[0]]!r}: a board with a sink "
            "has no free uniform mode, its rest sinking the sources' mean through the face; the uniform mode is "
            "carried on a board periodic on every axis alone (ALGEBRA.md, The closed lattice has no rest)"
        )
    return True
