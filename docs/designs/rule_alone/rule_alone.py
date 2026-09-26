"""THE RULE ALONE, a checking runner outside the engine (the Boss's records 2134 to 2137 of
2026-09-26, the owner's hard question: can the engine be built from the rule 9.57 (1) alone?).

One integer rule, written here from ALGEBRA.md 9.91 (2) and nothing else, stepped over a
GameBoard of Nodes with the remainders kept at every Node and NO motion rule of any kind:

    w a_next + r' = SUM over the six Ports of R a_neighbour + S a_now - w a_before + r,
    0 <= r' < w,
    p = Gamma - c (the pace at the Node, c the content read there),
    R = 2 p^2 num, S = 12 den Gamma^2 - 6 (p^2 + Gamma^2) (den - num) - 12 num p^2,
    w = 6 den Gamma^2,

num and den the pair at the Node (the record's kind, lowered on a well). The content c is a
declared integer field of this runner (a gradient, or the static level of a body's count);
the record is two integer arrays (now, before) and one of remainders. Every reading is a HOST
computation of the runner's own integers; nothing here is tuned to a number of the algebra
(record 2137: the run is written before the algebra's number is looked at).
"""

from __future__ import annotations

import math

import numpy as np

GAMMA = 10_000
INT = np.int64


def coefficients(num: np.ndarray, den: np.ndarray, content: np.ndarray, gamma: int = GAMMA):
    """(R, S, w) per Node as int64 arrays."""
    pace = gamma - content.astype(INT)
    p2 = pace * pace
    g2 = INT(gamma) * INT(gamma)
    read = 2 * p2 * num
    own = 12 * den * g2 - 6 * (p2 + g2) * (den - num) - 12 * num * p2
    wall = 6 * den * g2
    return read, own, wall


def neighbour_sum(a: np.ndarray, wrap: tuple[bool, bool, bool]) -> np.ndarray:
    """The six neighbours' levels summed; beyond an open face the level is 0."""
    total = np.zeros_like(a)
    for axis in range(3):
        for shift in (1, -1):
            rolled = np.roll(a, shift, axis=axis)
            if not wrap[axis]:
                edge = [slice(None)] * 3
                edge[axis] = slice(0, 1) if shift == 1 else slice(a.shape[axis] - 1, a.shape[axis])
                rolled[tuple(edge)] = 0
            total += rolled
    return total


def step(
    now: np.ndarray,
    before: np.ndarray,
    remainder: np.ndarray,
    read: np.ndarray,
    own: np.ndarray,
    wall: np.ndarray,
    wrap: tuple[bool, bool, bool],
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """One interval of the rule at every Node; returns (now', before', remainder')."""
    total = read * neighbour_sum(now, wrap) + own * now - wall * before + remainder
    nxt = np.floor_divide(total, wall)
    return nxt, now, total - wall * nxt


def rest_rotation(read: np.ndarray, own: np.ndarray, wall: np.ndarray) -> np.ndarray:
    """cos omega at each Node for a uniform standing level: 2 cos omega = (6 R + S) / w."""
    return (6 * read + own) / (2.0 * wall)


def envelope_squared(now: np.ndarray, before: np.ndarray, cos_omega: np.ndarray) -> np.ndarray:
    """The amplitude envelope squared of the rotating pair (now, before) at the local rest
    rotation: A^2 = (now^2 + before^2 - 2 now before cos omega) / sin^2 omega (HOST floats)."""
    sin2 = np.maximum(1.0 - cos_omega * cos_omega, 1e-12)
    n = now.astype(np.float64)
    b = before.astype(np.float64)
    return (n * n + b * b - 2.0 * n * b * cos_omega) / sin2


def centroid(weight: np.ndarray) -> tuple[float, float, float]:
    total = float(weight.sum())
    if total <= 0.0:
        return (math.nan, math.nan, math.nan)
    out = []
    for axis in range(3):
        coordinate = np.arange(weight.shape[axis], dtype=np.float64)
        shape = [1, 1, 1]
        shape[axis] = weight.shape[axis]
        out.append(float((weight * coordinate.reshape(shape)).sum()) / total)
    return (out[0], out[1], out[2])


def gaussian_packet(
    shape: tuple[int, int, int],
    centre: tuple[float, float, float],
    width: float,
    amplitude: int,
    cos_omega: float,
) -> tuple[np.ndarray, np.ndarray]:
    """A standing packet: now = round(A exp(-r^2 / (2 width^2))), before = round(now cos omega)
    (the reviewer's start of record 2132, in three dimensions)."""
    grids = np.meshgrid(*[np.arange(n, dtype=np.float64) for n in shape], indexing="ij")
    r2 = sum((g - c) ** 2 for g, c in zip(grids, centre, strict=True))
    envelope = amplitude * np.exp(-r2 / (2.0 * width * width))
    now = np.rint(envelope).astype(INT)
    before = np.rint(envelope * cos_omega).astype(INT)
    return now, before
