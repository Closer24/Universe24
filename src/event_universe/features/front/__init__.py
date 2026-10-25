"""The erasing front (the owner's word, "it starts erasing at the speed of light"; the mathematician's hand and the advisor's second hand, two hands; ALGEBRA.md, The click writes on the lattice): when a record's count reaches 0 in the books, from every Node written in that draw, at every interval t after it the loop presents the face to that record alone on the shell of Nodes at Link-metric distance exactly t from the Node, one shell per interval from the interval after the click, the shells one interval behind the causal bound and inside the click's light cone, |dx| + |dy| + |dz| = t with a periodic axis wrapped as the receding face handles it, so that the ball of distance at most t is empty of the record and every Node beyond it holds the whole NodeState bit for bit as the run without the front holds it (the dependency radius one Link: no write inside the cone is seen outside it, the front invisible ahead of itself); every other record untouched, nothing in the Node, Rule3 untouched, a loop's act beside the receding face. This folder holds the shell's mask alone, a pure function of the shape, the origin and the distance, and the ball about a set of Nodes in the same metric (`ball`), the record's light cone the meeting that runs back steps alone (`meeting_back`)."""

from __future__ import annotations

from collections.abc import Sequence
from typing import Any

import numpy as np


def distances(
    shape: tuple[int, int, int], origin: tuple[int, int, int], periodic: tuple[bool, bool, bool]
) -> Any:
    """The Link-metric distance of every Node of the board from `origin`: per axis the distance |d| along the axis, or on a periodic axis the lesser of |d| and the extent less |d| (the way round the wrap), summed over the three axes."""
    total: Any = 0
    for axis, (extent, at) in enumerate(zip(shape, origin, strict=True)):
        along = np.abs(np.arange(extent) - at)
        if periodic[axis]:
            along = np.minimum(along, extent - along)
        view = [1, 1, 1]
        view[axis] = extent
        total = total + along.reshape(view)
    return total


def shell(
    shape: tuple[int, int, int],
    origin: tuple[int, int, int],
    distance: int,
    periodic: tuple[bool, bool, bool],
) -> np.ndarray:
    """The mask of the Nodes at Link-metric distance exactly `distance` from `origin` over the board (`distances`); empty beyond the board's diameter."""
    return np.asarray(distances(shape, origin, periodic) == distance)


def distance_map(
    shape: tuple[int, int, int],
    origins: Sequence[tuple[int, int, int]],
    periodic: tuple[bool, bool, bool],
) -> np.ndarray:
    """The Link-metric distance of every Node of the board from the nearest of the `origins`, the wrap as `distances` counts it, as one distance transform axis by axis (the metric a sum over the axes, so the least sum over the origins is the least over one axis at a time): the origins at 0 and every other Node beyond the board's diameter, then along each axis the two sweeps that give every Node the lesser of its own distance and its neighbour's plus one, the sweeps run round once more on a periodic axis; the board's diameter plus one where no origin is named."""
    far = sum(shape) + 1
    found = np.full(shape, far, dtype=int)
    for origin in origins:
        found[origin] = 0
    for axis in range(3):
        extent, along = shape[axis], np.moveaxis(found, axis, 0)
        for _ in range(2 if periodic[axis] else 1):
            for i in range(1, extent):
                along[i] = np.minimum(along[i], along[i - 1] + 1)
            if periodic[axis]:
                along[0] = np.minimum(along[0], along[-1] + 1)
        for _ in range(2 if periodic[axis] else 1):
            for i in range(extent - 2, -1, -1):
                along[i] = np.minimum(along[i], along[i + 1] + 1)
            if periodic[axis]:
                along[-1] = np.minimum(along[-1], along[0] + 1)
    return found


def ball(
    shape: tuple[int, int, int],
    origins: Sequence[tuple[int, int, int]],
    radius: int,
    periodic: tuple[bool, bool, bool],
) -> np.ndarray:
    """The mask of the Nodes within `radius` Links of any of the `origins` over the board, the Link metric with the wrap as the shell counts it (`distance_map`, `distances`): the record's light cone about its lay's Nodes, G(t) = S_0 within t + 1 Links at the interval t (ALGEBRA.md, The interval's dependency radius is one Link; `meeting_back`), the page's shading the same ball; empty where no origin is named."""
    if not origins:
        return np.zeros(shape, dtype=bool)
    return np.asarray(distance_map(shape, origins, periodic) <= radius)
