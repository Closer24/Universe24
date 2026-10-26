"""The one reader of the row (H-Readings-One-Reader-1): every reading of a record row is ONE bilinear x.M.y line by line, M one of the shape's matrices: G (the Gram), GJ (the charge's, the current's), G Gamma_a (the density's), K (the conjugation, the frame's and the swap's); the share, the period's ratio, the stress parts, the shear and the flux are the same bilinear at other arguments. The matrices are the engine's own (gram.py, quartet.py); the lines here are the readings' names."""

from __future__ import annotations

from functools import lru_cache
from typing import Any

import numpy as np

from event_universe import gram as engine
from event_universe.core.ports import AXES, across, port_of, wrap
from event_universe.links import gradient

Matrix = list[list[int]]


@lru_cache
def matrix(shape: int, kind: str) -> Matrix:
    """The row's matrix by name: the Gram as G, the charge's as GJ, the conjugation as K, the density's G Gamma_a as GA0 to GA2."""
    g = engine.gram(shape)
    if kind == "G":
        return g
    if kind == "GJ":
        return engine.matmul(g, engine.rotation(shape))
    if kind == "K":
        return engine.conjugation(shape)
    return engine.matmul(g, engine.axes(shape)[int(kind[2])])


def lines(shape: int, kind: str, xs: list[Any], ys: list[Any]) -> list[Any]:
    """The one bilinear line by line: x_k (M y)_k, the plain products at the identity."""
    m = matrix(shape, kind)
    if m == engine.identity(len(xs)):
        return [x * y for x, y in zip(xs, ys, strict=True)]
    return [x * my for x, my in zip(xs, engine.matvec(m, ys), strict=True)]


def form(shape: int, kind: str, xs: list[Any], ys: list[Any]) -> Any:
    """The bilinear summed over the lines."""
    return sum(lines(shape, kind, xs, ys), start=0)


def charge(shape: int, befores: list[Any], nows: list[Any]) -> Any:
    """W = B.GJ.N, the plane's Wronskian at G = I."""
    return form(shape, "GJ", befores, nows)


def conjugated(shape: int, xs: list[Any], f: Any) -> list[Any]:
    """A neighbour's lines in the Node's frame: K x where the frame sign is -1."""
    return [np.where(f == -1, k, x) for k, x in zip(engine.matvec(matrix(shape, "K"), xs), xs, strict=True)]


def current(shape: int, nows: list[Any], frames: list[Any]) -> list[Any]:
    """J_a = dN_a.GJ.N, the neighbours read in the Node's frame."""
    found = []
    for a in range(AXES):
        up = conjugated(shape, [across(n, port_of(a, 0)) for n in nows], frames[port_of(a, 0)])
        down = conjugated(shape, [across(n, port_of(a, 1)) for n in nows], frames[port_of(a, 1)])
        found.append(form(shape, "GJ", [u - d for u, d in zip(up, down, strict=True)], nows))
    return found


def density(shape: int, nows: list[Any]) -> list[Any]:
    """s_a = N.G Gamma_a.N, none for a row with no axis matrices."""
    return [form(shape, f"GA{a}", nows, nows) for a in range(len(engine.axes(shape)))]


def curl(odd: list[Any]) -> list[Any]:
    """Phi_a = d_b A_c - d_c A_b, the one-Link curl of the odd lines."""
    return [
        gradient(odd[wrap(a - 1, AXES)], wrap(a + 1, AXES)) - gradient(odd[wrap(a + 1, AXES)], wrap(a - 1, AXES))
        for a in range(AXES)
    ]


def term(shape: int, coefficient: Any, phi: list[Any], xs: list[Any]) -> list[Any]:
    """SUM_a coefficient Phi_a (Gamma_a x) per line, 0 with no axis matrices."""
    found: list[Any] = [0] * len(xs)
    for a, ga in enumerate(engine.axes(shape)):
        found = [f + coefficient * phi[a] * g for f, g in zip(found, engine.matvec(ga, xs), strict=True)]
    return found


def stress(shape: int, levels: list[Any], a: int, b: int) -> Any:
    """d_a.G.d_b, the stress's part on the axes (a, b): the diagonal at a = b, the shear at b = a + 1."""
    return form(shape, "G", [gradient(x, a) for x in levels], [gradient(x, b) for x in levels])


def flux(shape: int, nows: list[Any], velocities: list[Any], axis: int) -> Any:
    """u.G.D_a N, the record's count flux on an axis."""
    return form(shape, "G", velocities, [gradient(n, axis) for n in nows])
