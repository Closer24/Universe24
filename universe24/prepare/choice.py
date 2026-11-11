"""Initial data for the CHOICE layer (data only: nothing here runs the engine or touches a running state).

Ring phase convention (Study 5): the period-6 clock sequence of b is p = (A, A, 0, -A, -A, 0) (from (a, b) = (0, A)
under (a, b) -> (b, b - a)); a ring of phase phi at time t has gear j at (a, b) = (p[2j + phi + t - 1], p[2j + phi + t])
(indices mod 6). The period-4 pair (u = 0, (a, b) -> (b, -a)) uses p4 = (A, 0, -A, 0) with gear j at phase j + lag.
Fibre profiles: a right-moving profile b(x, t) = g(x - t) has a(x) = g(x + 1); a left-moving one b = h(x + t) has
a(x) = h(x - 1).
"""
from __future__ import annotations

import numpy as np

from ..core.engine import OBJ, State
from ..core.lattice import lattice
from ..core.tensor import Tensor, vacuum_map


def p6(A: int, k: int) -> int:
    return (A, A, 0, -A, -A, 0)[k % 6] if A else 0


def p4(A: int, k: int) -> int:
    return (A, 0, -A, 0)[k % 4]


def ring_state(A: int, phase: int, t: int = 0):
    """[(a_j, b_j)] of a period-6 ring of amplitude A and phase ``phase`` at time t."""
    return [(p6(A, 2 * j + phase + t - 1), p6(A, 2 * j + phase + t)) for j in range(3)]


def pair4_state(A: int, lag: int):
    """[(a_j, b_j)] of a period-4 pair (gear 1 one step ahead of gear 0), lag ``lag``."""
    return [(p4(A, j + lag - 1), p4(A, j + lag)) for j in range(2)]


def ring_b(A: int, phase: int, t: int = 0):
    return [p6(A, 2 * j + phase + t) for j in range(3)]


class Prep:
    """Mutable builder of ONE initial State (Python-int object arrays). ``set(gear, nodes, a, b, r)`` writes
    per-node values (scalars or arrays aligned with ``nodes``, flat node indices). ``state()`` returns the State."""

    def __init__(self, tensor: Tensor, L: int, *blocks, default_r: int = 0):
        self.tensor, self.L, self.D = tensor, L, 6
        lat = lattice(L)
        self.N = lat.N
        r0 = vacuum_map(*blocks)
        G = tensor.G
        self.a = np.zeros((G, self.N), dtype=OBJ)
        self.b = np.zeros((G, self.N), dtype=OBJ)
        self.r = np.zeros((G, self.N), dtype=OBJ)
        for i, name in enumerate(tensor.names):
            v = r0.get(name, default_r)
            if not 0 <= v < self.D:
                raise ValueError("vacuum remainder outside 0..D-1")
            self.r[i, :] = v

    def set(self, gear: str, nodes, a=None, b=None, r=None):
        g = self.tensor.gear_index(gear)
        nodes = np.asarray(nodes, dtype=np.intp)
        for arr, v in ((self.a, a), (self.b, b), (self.r, r)):
            if v is None:
                continue
            vals = np.asarray(v, dtype=OBJ) if np.ndim(v) else np.full(len(nodes), v, dtype=OBJ)
            arr[g, nodes] = vals
        if r is not None:
            rr = self.r[g, nodes]
            if any((int(x) < 0 or int(x) >= self.D) for x in np.atleast_1d(rr)):
                raise ValueError("remainder outside 0..D-1")

    def node(self, x, y, z) -> int:
        return lattice(self.L).index(x, y, z)

    def nodes_x(self, x, yz):
        """flat indices of nodes (x, y, z) for (y, z) in ``yz``."""
        lat = lattice(self.L)
        return np.array([lat.index(x, y, z) for (y, z) in yz], dtype=np.intp)

    def state(self) -> State:
        return State(self.L, self.a.copy(), self.b.copy(), self.r.copy())


def yz_lines(L: int, n: int):
    """The first n (y, z) lines in row order; raises if L^2 < n."""
    if n > L * L:
        raise ValueError(f"need {n} lines, the cube has {L * L}")
    return [(i // L, i % L) for i in range(n)]


__all__ = ["p6", "p4", "ring_state", "pair4_state", "ring_b", "Prep", "yz_lines"]
