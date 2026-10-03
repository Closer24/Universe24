"""The erasing front (the owner's word of 2026-10-03, 03:25 Israel, "it starts erasing at the speed of light"; the mathematician's 182 and the advisor's second hand, #1563 comment 5963124874, two hands; ALGEBRA.md, The click writes on the GameBoard): when a record's count reaches 0 in the books, from every Node written in that draw, at every interval t after it the loop presents the face to that record alone on the shell of Nodes at Link-metric distance exactly t from the Node, one shell per interval from the interval after the click, the shells one interval behind the causal bound and inside the click's light cone, |dx| + |dy| + |dz| = t with a periodic axis wrapped as the receding face handles it, so that the ball of distance at most t is empty of the record and every Node beyond it holds the whole NodeState bit for bit as the run without the front holds it (the dependency radius one Link: no write inside the cone is seen outside it, the front invisible ahead of itself); every other record untouched, nothing in the Node, Rule3 untouched, a loop's act beside the receding face. This folder holds the shell's mask alone, a pure function of the shape, the origin and the distance."""

from __future__ import annotations

from typing import Any

import numpy as np


def shell(
    shape: tuple[int, int, int],
    origin: tuple[int, int, int],
    distance: int,
    periodic: tuple[bool, bool, bool],
) -> np.ndarray:
    """The mask of the Nodes at Link-metric distance exactly `distance` from `origin` over the board: per axis the distance |d| along the axis, or on a periodic axis the lesser of |d| and the extent less |d| (the way round the wrap), summed over the three axes; empty beyond the board's diameter."""
    total: Any = 0
    for axis, (extent, at) in enumerate(zip(shape, origin, strict=True)):
        along = np.abs(np.arange(extent) - at)
        if periodic[axis]:
            along = np.minimum(along, extent - along)
        view = [1, 1, 1]
        view[axis] = extent
        total = total + along.reshape(view)
    return np.asarray(total == distance)
