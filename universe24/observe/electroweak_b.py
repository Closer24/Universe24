"""observe/electroweak_b.py — READ-ONLY diagnostics of route B (layers/electroweak_b.py). Nothing here changes a state.

EWBView(tensor, ewb_block):
* pieces(gen): the local generator gen in {t1, t2, t3, Y} at a node y, x2 (layers.electroweak_b.generator_actions):
  matter (both pairs) and Higgs at y; U(2) links / 2-paths: left action if based at y, right action if they ARRIVE at y;
  B: +Tr X if based at y, -Tr X if arriving; Xi(x,a): -Tr X at x, the doublet action at x + e_a; Xi'(x,a): the doublet
  action at x, -Tr X at x + e_a.
* lie(state, gen): <grad Psi_phys, X_y B_phys> summed over the board, per node y (exact Python ints): 0 at every node
  is the polynomial identity "Psi is locally invariant" evaluated on that state.
* Exact discrete Noether / Gauss identity (as observe/chiral.py):
      J2(y, t+1) - J2(y, t) = sum_c B_c(t) (2T (r(t) - r(t+1)))_c ,   J2 = D sum a_phys^T (2T) b_phys
* electric charge: charge = (t3 + Y)/2, i.e. J2_charge = (J2_t3 + J2_Y)/2 (exact when both are).
"""
from __future__ import annotations
import numpy as np
from ..core.engine import State
from ..core.lattice import lattice
from ..core.tensor import Tensor
from ..layers.chiral import HIGGS
from ..layers.electroweak_b import COMP, DCOMP, generator_actions
from ..layers.matter import matter_names
AXES = ('x', 'y', 'z')
UNIT = ((1, 0, 0), (0, 1, 0), (0, 0, 1))

class EWBView:

    def __init__(self, tensor: Tensor, ewb):
        self.tensor = tensor
        p = ewb.params
        self.D, = (6,)
        ns = ewb.name
        gi = lambda n: tensor.gear_index(f'{ns}.{n}')
        self.matter = [tensor.gear_index(f"{p['matter']}.{g}") for g in matter_names('pair')] + [tensor.gear_index(f"{p['partner']}.{g}") for g in matter_names('pair')]
        self.higgs = [gi(h) for h in HIGGS]
        self.V = {a: [gi(f'V{AXES[a]}_{c}') for c in COMP] for a in range(3)}
        self.P = {}
        if p.get('use_P', True) and p['kappa_P']:
            for a in range(3):
                for b in range(3):
                    if a != b:
                        self.P[a, b] = [gi(f'P{AXES[a]}{AXES[b]}_{c}') for c in COMP]
        self.B = {a: [gi(f'B{AXES[a]}_re'), gi(f'B{AXES[a]}_im')] for a in range(3)}
        self.X = {a: [gi(f'X{AXES[a]}_{c}') for c in DCOMP] for a in range(3)}
        self.Y = {a: [gi(f'Y{AXES[a]}_{c}') for c in DCOMP] for a in range(3)}
        self.R = {}
        if p.get('plaquette'):
            for a in range(3):
                for b in range(3):
                    if a != b:
                        self.R[a, b] = [gi(f'R{AXES[a]}{AXES[b]}_{c}') for c in COMP]
        self.S = {}
        if p.get('plaquette') and p.get('w_B'):
            for a in range(3):
                for b in range(3):
                    if a != b:
                        self.S[a, b] = [gi(f'S{AXES[a]}{AXES[b]}_re'), gi(f'S{AXES[a]}{AXES[b]}_im')]
        self.x0 = np.zeros(tensor.G, dtype=object)
        for name, val in p['X0'].items():
            self.x0[tensor.gear_index(name)] = val
        self._pieces = {}

    def pieces(self, gen: str) -> list:
        if gen in self._pieces:
            return self._pieces[gen]
        act = generator_actions(gen)
        out = []

        def add(off, idx, M):
            M = np.asarray(M)
            rows, cols = np.nonzero(M)
            for i, j in zip(rows, cols):
                out.append((tuple(off), idx[j], idx[i], int(M[i, j])))
        add((0, 0, 0), self.matter, act['matter'])
        add((0, 0, 0), self.higgs, act['higgs'])
        for a in range(3):
            back = tuple((-e for e in UNIT[a]))
            add((0, 0, 0), self.V[a], act['link_left'])
            add(back, self.V[a], act['link_right'])
            add((0, 0, 0), self.B[a], act['B_left'])
            add(back, self.B[a], act['B_right'])
            add((0, 0, 0), self.X[a], act['xi_phase'])
            add(back, self.X[a], act['doublet'])
            add((0, 0, 0), self.Y[a], act['doublet'])
            add(back, self.Y[a], act['xi_phase'])
        for (a, b), idx in self.P.items():
            back = tuple((-x - y for x, y in zip(UNIT[a], UNIT[b])))
            add((0, 0, 0), idx, act['link_left'])
            add(back, idx, act['link_right'])
        for (a, b), idx in self.R.items():
            add(tuple((-e for e in UNIT[a])), idx, act['link_left'])
            add(tuple((-x - y for x, y in zip(UNIT[a], UNIT[b]))), idx, act['link_right'])
        for (a, b), idx in self.S.items():
            add(tuple((-e for e in UNIT[a])), idx, act['B_left'])
            add(tuple((-x - y for x, y in zip(UNIT[a], UNIT[b]))), idx, act['B_right'])
        self._pieces[gen] = out
        return out

    def _bilinear(self, first, second, gen, L, scale, first_raw=False, second_raw=False):
        lat = lattice(L)
        by_off: dict = {}
        for off, src, dst, coef in self.pieces(gen):
            by_off.setdefault(off, []).append((src, dst, coef))
        J = np.zeros(lat.N, dtype=object)
        for off, lst in by_off.items():
            F = np.zeros(lat.N, dtype=object)
            for src, dst, coef in lst:
                fa = first[dst].astype(object) + (0 if first_raw else self.x0[dst])
                fb = second[src].astype(object) + (0 if second_raw else self.x0[src])
                F = F + coef * fa * fb
            J = J + F[lat.shift_index(off)]
        return scale * J

    def charge2(self, state: State, gen: str) -> np.ndarray:
        return self._bilinear(state.a, state.b, gen, state.L, self.D)

    def remainder_term2(self, s0: State, s1: State, gen: str) -> np.ndarray:
        dr = s0.r.astype(object) - s1.r.astype(object)
        return self._bilinear(s0.b, dr, gen, s0.L, 1, second_raw=True)

    def lie(self, engine, state: State, gen: str) -> np.ndarray:
        """Per-node <grad Psi_phys(B), X_y B> with grad Psi_phys = u + D x0 (exact)."""
        u = engine.inputs(state).astype(object)
        gphys = u + self.D * self.x0[:, None]
        return self._bilinear(gphys, state.b, gen, state.L, 1, first_raw=True)

    def gauss_check(self, history: list, gens=('t1', 't2', 't3', 'Y')) -> dict:
        out = {}
        for g in gens:
            checks = fails = 0
            max_J = 0
            for t in range(len(history) - 1):
                s0, s1 = (history[t], history[t + 1])
                lhs = self.charge2(s1, g) - self.charge2(s0, g)
                rhs = self.remainder_term2(s0, s1, g)
                fails += int(np.sum(lhs != rhs))
                checks += len(lhs)
                max_J = max(max_J, max((abs(int(x)) for x in self.charge2(s0, g))))
            out[g] = {'checks': checks, 'failures': fails, 'max_abs_J2': max_J}
        return out

    def global_charge2(self, state: State, gen: str) -> int:
        return int(np.sum(self.charge2(state, gen)))
__all__ = ['EWBView']
