"""observe/chiral.py — READ-ONLY diagnostics of the chiral candidate (layers/chiral.py). Nothing here changes a state.

* ChiralView(tensor, coupling_block, links_block): index bookkeeping of the doublet (matter + partner), Higgs, weak links
  and 2-path gears inside a composed tensor.
* Exact local SU(2) Noether/Gauss identity (x2 to stay integer: the matter generator is t_a Pi_W = 2 t_a P_W):
      J2_a(x, t+1) - J2_a(x, t) = sum_c B_c(t) (2 T_a (r(t) - r(t+1)))_c        (exact Python ints)
  with 2T_a = t_a Pi_W on the matter at x, 2 L_a on the Higgs at x, 2 L_a on links / 2-paths based at x, -2 R_a on links /
  2-paths arriving at x (B = physical values: vacuum A, P0, v added).
* J-number N_J = sum D a^T J b over the doublet (exact two-time Noether charge; its sign separates the clock senses).
* Click-space J-Wronskian W_J(t) = sum_x ell(t+1)^T J ell(t), ell(t) = b(t+1) + a(t) = the click sizes of update t
  (HAND-M2's J+ readout; passive, two-time, node-local).
"""
from __future__ import annotations

import numpy as np

from ..core.engine import State
from ..core.lattice import lattice
from ..core.tensor import Tensor
from ..layers.chiral import HIGGS, chiral_algebra
from ..layers.gauge import ALGEBRAS
from ..layers.matter import matter_names

AXES = ("x", "y", "z")
UNIT = ((1, 0, 0), (0, 1, 0), (0, 0, 1))


class ChiralView:
    def __init__(self, tensor: Tensor, coupling, links):
        self.tensor = tensor
        cp, lp = coupling.params, links.params
        self.Q, self.D = cp["Q"], 6 * cp["Q"]
        self.v, self.A = cp["v"], lp["A"]
        self.P0 = lp.get("P0", 0)
        self.use_P = lp.get("use_P", False)
        q = lambda blk, g: f"{blk}.{g}"
        self.matter = [tensor.gear_index(q(cp["matter"], g)) for g in matter_names("pair")] + \
                      [tensor.gear_index(q(cp["partner"], g)) for g in matter_names("pair")]
        self.higgs = [tensor.gear_index(q(coupling.name, h)) for h in HIGGS]
        comps = ("1", "i", "j", "k")
        self.links = {k: [tensor.gear_index(q(links.name, f"U{AXES[k]}_{c}")) for c in comps] for k in range(3)}
        self.paths = {}
        if self.use_P:
            for k1 in range(3):
                for k2 in range(3):
                    if k1 != k2:
                        self.paths[(k1, k2)] = [tensor.gear_index(q(links.name, f"P{AXES[k1]}{AXES[k2]}_{c}"))
                                                for c in comps]
        self.x0 = np.zeros(tensor.G, dtype=object)
        self.x0[self.higgs[0]] = self.v
        for k in range(3):
            self.x0[self.links[k][0]] = self.A
        for gl in self.paths.values():
            self.x0[gl[0]] = self.P0
        self.alg = chiral_algebra()
        H = ALGEBRAS["su2"]
        self.Lq = [H.left_matrix(e) for e in ((0, 1, 0, 0), (0, 0, 1, 0), (0, 0, 0, 1))]
        self.Rq = [H.right_matrix(e) for e in ((0, 1, 0, 0), (0, 0, 1, 0), (0, 0, 0, 1))]

    # ------------------------------------------------------------------ Noether pieces (offset, src, dst, coeff), x2
    def pieces(self, a: int) -> list:
        out = []
        Xm = self.alg["t"][a] @ self.alg["PiW"]
        rows, cols = np.nonzero(Xm)
        for i, j in zip(rows, cols):
            out.append(((0, 0, 0), self.matter[j], self.matter[i], int(Xm[i, j])))
        La, Ra = self.Lq[a], self.Rq[a]
        for c in range(4):
            for b in range(4):
                if La[c][b]:
                    out.append(((0, 0, 0), self.higgs[b], self.higgs[c], 2 * La[c][b]))
        for k in range(3):
            back = tuple(-e for e in UNIT[k])
            for c in range(4):
                for b in range(4):
                    if La[c][b]:
                        out.append(((0, 0, 0), self.links[k][b], self.links[k][c], 2 * La[c][b]))
                    if Ra[c][b]:
                        out.append((back, self.links[k][b], self.links[k][c], -2 * Ra[c][b]))
        for (k1, k2), gl in self.paths.items():
            back = tuple(-x - y for x, y in zip(UNIT[k1], UNIT[k2]))
            for c in range(4):
                for b in range(4):
                    if La[c][b]:
                        out.append(((0, 0, 0), gl[b], gl[c], 2 * La[c][b]))
                    if Ra[c][b]:
                        out.append((back, gl[b], gl[c], -2 * Ra[c][b]))
        return out

    def _bilinear(self, first, second, a, L, scale, second_raw=False, only=None):
        lat = lattice(L)
        by_off: dict = {}
        for off, src, dst, coef in self.pieces(a):
            if only is not None and dst not in only:
                continue
            by_off.setdefault(off, []).append((src, dst, coef))
        J = np.zeros(lat.N, dtype=object)
        for off, lst in by_off.items():
            F = np.zeros(lat.N, dtype=object)
            for src, dst, coef in lst:
                fa = first[dst].astype(object) + self.x0[dst]
                fb = second[src].astype(object) + (0 if second_raw else self.x0[src])
                F = F + coef * fa * fb
            J = J + F[lat.shift_index(off)]
        return scale * J

    def charge2(self, state: State, a: int, parts: str = "all") -> np.ndarray:
        only = None if parts == "all" else set(self.matter)
        return self._bilinear(state.a, state.b, a, state.L, self.D, only=only)

    def remainder_term2(self, s0: State, s1: State, a: int) -> np.ndarray:
        dr = s0.r.astype(object) - s1.r.astype(object)
        return self._bilinear(s0.b, dr, a, s0.L, 1, second_raw=True)

    def gauss_check(self, history: list) -> dict:
        checks = fails = 0
        max_J = max_R = max_dJm = 0
        for t in range(len(history) - 1):
            s0, s1 = history[t], history[t + 1]
            for a in range(3):
                lhs = self.charge2(s1, a) - self.charge2(s0, a)
                rhs = self.remainder_term2(s0, s1, a)
                fails += int(np.sum(lhs != rhs))
                checks += len(lhs)
                max_R = max(max_R, max(abs(int(x)) for x in rhs))
                max_J = max(max_J, max(abs(int(x)) for x in self.charge2(s0, a)))
                dm = self.charge2(s1, a, "matter") - self.charge2(s0, a, "matter")
                max_dJm = max(max_dJm, max(abs(int(x)) for x in dm))
        return {"checks": checks, "failures": fails, "max_abs_J2": max_J, "max_abs_remainder_term2": max_R,
                "max_abs_matter_only_change": max_dJm}

    # ------------------------------------------------------------------ clock sense
    def j_number(self, state: State) -> int:
        J = self.alg["J"]
        a = state.a[self.matter].astype(object)
        b = state.b[self.matter].astype(object)
        return int(self.D * np.sum(a * (J.astype(object) @ b)))

    def click_wronskian(self, s0: State, s1: State, s2: State) -> int:
        """W_J for the two updates s0 -> s1 -> s2: sum_x ell1(x)^T J ell0(x), ell_t = b(t+1) + a(t).
        Raw state-derived quotients include non-click fixed points; not an official-event-only observable."""
        m = self.matter
        ell0 = s1.b[m].astype(object) + s0.a[m].astype(object)
        ell1 = s2.b[m].astype(object) + s1.a[m].astype(object)
        J = self.alg["J"].astype(object)
        return int(np.sum(ell1 * (J @ ell0)))


__all__ = ["ChiralView"]
