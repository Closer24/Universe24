"""ONE read-only observables (Study 22, ONE-A). Nothing here changes a state or feeds back into a run: every function
reads complete snapshots produced by Engine.step and returns numbers.

Exact cosmic ledgers per update (before -> after), with ell = after.b + before.a (Rule3: a' = b, b' = ell - a):
  events   ell_dp - ell_dm = I = b_M1^2 + b_M2^2 (before) at every node        (matched pair: K+ - K- = D I)
  lock     r_dp = r_dm at every node                                              (shared remainder)
  Born     N+ = Sum ell_dp = floor((tok + Sum K+)/D), K+ = 2 u_dp = 2c I b_Lp   (sigma-delta ledger, per node)
  N_J      rho = D (a_M1 b_M2 - a_M2 b_M1):  rho' - rho = Sum_y 2h (Th_x + Th_y)(b1_x b2_y - b2_x b1_y)
                                               + b1 (r2 - r2') - b2 (r1 - r1')    (local continuity, link current)
plus the hand's board statistics, Delta = b_dp - b_dm, seed distances and click/outcome records.
"""
from __future__ import annotations

import hashlib

import numpy as np

from ..core.engine import OBJ, State
from ..layers.one import COSMIC_GEARS, COSMIC_NS


def _obj(row, L: int) -> np.ndarray:
    return np.asarray(row).astype(OBJ).reshape(L, L, L)


def _nbr_sum(f):
    return sum(np.roll(f, s, ax) for ax in range(3) for s in (1, -1))


class CosmicView:
    """Index map of the cosmic gears in a composed tensor (read-only helpers)."""

    def __init__(self, tensor, ns: str = COSMIC_NS):
        self.ns = ns
        self.rows = {g: tensor.gear_index(f"{ns}.{g}") for g in COSMIC_GEARS}
        self.D = 6 * tensor.Q
        names = tensor.names
        self.package_rows = np.array([i for i, n in enumerate(names) if n.split(".", 1)[0] != ns], dtype=np.intp)
        self.cosmic_rows = np.array(sorted(self.rows.values()), dtype=np.intp)

    def f(self, state: State, g: str, field: str) -> np.ndarray:
        return _obj(getattr(state, field)[self.rows[g]], state.L)

    def intensity(self, state: State) -> np.ndarray:
        b1, b2 = self.f(state, "M1", "b"), self.f(state, "M2", "b")
        return b1 * b1 + b2 * b2

    def delta(self, state: State) -> np.ndarray:
        return self.f(state, "dp", "b") - self.f(state, "dm", "b")

    def quotients(self, before: State, after: State, g: str) -> np.ndarray:
        return self.f(after, g, "b") + self.f(before, g, "a")

    def hand(self, state: State) -> dict:
        th = self.f(state, "Th", "b")
        tot = int(np.sum(th))
        mn, mx = int(np.min(th)), int(np.max(th))
        return {"sum": tot, "mean": tot / th.size, "min": mn, "max": mx, "split": mx - mn}


class CosmicLedger:
    """Exact state-derived carry ledgers. Weights are not counts of official click records."""

    def __init__(self, view: CosmicView, seed: State, h: int, c_pair: int):
        self.v, self.h, self.D, self.c = view, h, view.D, c_pair
        self.tok = view.f(seed, "dp", "r")
        L = seed.L
        z = np.zeros((L, L, L), dtype=OBJ)
        self.sumKp, self.Nplus, self.Nminus = z.copy(), z.copy(), z.copy()
        self.fail = {"events": 0, "lock": 0, "born": 0, "N_J": 0}
        self.checks = 0
        self.events_total = 0

    def update(self, before: State, after: State) -> dict:
        v, D, h = self.v, self.D, self.h
        I = v.intensity(before)
        lp, lm = v.quotients(before, after, "dp"), v.quotients(before, after, "dm")
        out = {"events": int(np.sum((lp - lm) != I)),
               "lock": int(np.sum(v.f(after, "dp", "r") != v.f(after, "dm", "r")))}
        self.sumKp = self.sumKp + 2 * self.c * I * v.f(before, "Lp", "b")
        self.Nplus = self.Nplus + lp
        self.Nminus = self.Nminus - lm
        out["born"] = int(np.sum(self.Nplus != (self.tok + self.sumKp) // D))
        a1, a2 = v.f(before, "M1", "a"), v.f(before, "M2", "a")
        b1, b2 = v.f(before, "M1", "b"), v.f(before, "M2", "b")
        r1, r2 = v.f(before, "M1", "r"), v.f(before, "M2", "r")
        A1, A2 = v.f(after, "M1", "a"), v.f(after, "M2", "a")
        B1, B2 = v.f(after, "M1", "b"), v.f(after, "M2", "b")
        R1, R2 = v.f(after, "M1", "r"), v.f(after, "M2", "r")
        th = v.f(before, "Th", "b")
        cur = np.zeros_like(I)
        for ax in range(3):
            for sh in (1, -1):
                ty, y1, y2 = np.roll(th, sh, ax), np.roll(b1, sh, ax), np.roll(b2, sh, ax)
                cur = cur + 2 * h * (th + ty) * (b1 * y2 - b2 * y1)
        rho0 = D * (a1 * b2 - a2 * b1)
        rho1 = D * (A1 * B2 - A2 * B1)
        remf = b1 * (r2 - R2) - b2 * (r1 - R1)
        out["N_J"] = int(np.sum((rho1 - rho0) != (cur + remf)))
        for k in self.fail:
            self.fail[k] += out[k]
        self.checks += 1
        self.events_total += int(np.sum(I))
        out["I_sum"] = int(np.sum(I))
        return out

    def born_frequencies(self, seed: State, load_sum: int, min_events: int = 10 ** 4) -> dict:
        p = self.v.f(seed, "Lp", "b")
        Q = load_sum
        tot = self.Nplus + self.Nminus
        devs = []
        for n_p, n_t, pv in zip(self.Nplus.ravel(), tot.ravel(), p.ravel()):
            if int(n_t) >= min_events:
                devs.append(abs(int(n_p) / int(n_t) - int(pv) / Q))
        return {"nodes_with_min_events": len(devs), "min_events": min_events,
                "max_abs_dev": max(devs) if devs else None, "mean_abs_dev": (sum(devs) / len(devs)) if devs else None,
                "total_events": int(np.sum(tot)), "N_plus_total": int(np.sum(self.Nplus))}


def rel_distance(cur: list, ref: list) -> tuple[float, str]:
    """min(|cur - ref|^2, |cur + ref|^2) / |ref|^2 over flat integer lists (exact sums, float ratio)."""
    n0 = sum(x * x for x in ref) or 1
    dp = sum((x - y) ** 2 for x, y in zip(cur, ref))
    dm = sum((x + y) ** 2 for x, y in zip(cur, ref))
    return (min(dp, dm) / n0, "+" if dp <= dm else "-")


def flat(state: State, rows) -> list:
    return [int(x) for x in np.asarray(state.b[rows]).ravel()]


def flat_ab(state: State, rows) -> list:
    return [int(x) for x in np.asarray(state.a[rows]).ravel()] + [int(x) for x in np.asarray(state.b[rows]).ravel()]


def knz(state: State, rows, N: int) -> list:
    """N (b - mean b) per gear row: the k != 0 part (exact integers), CC-A's packet measure."""
    out = []
    for g in rows:
        v = [int(x) for x in np.asarray(state.b[g]).ravel()]
        mu = sum(v)
        out += [N * x - mu for x in v]
    return out


def state_hash(state: State, rows) -> str:
    """Canonical exact-value hash, independent of int64/object storage.

    Format v2 includes geometry and subset shape. Pre-v2 run hashes are not
    comparable: they encoded int64 bytes on one execution path and text on another.
    """
    h = hashlib.sha256(b"universe24-state-values-v2|")
    h.update(str(state.L).encode())
    for arr in (state.a, state.b, state.r):
        sub = np.asarray(arr[rows])
        h.update(str(sub.shape).encode())
        h.update(b":")
        h.update(",".join(str(int(x)) for x in sub.ravel()).encode())
        h.update(b"|")
    return h.hexdigest()


def namespace_bits(state: State, ns_rows: dict) -> dict:
    out = {}
    for ns, rows in ns_rows.items():
        sub = np.asarray(state.b[rows])
        m = max(int(sub.max()), -int(sub.min())) if sub.size else 0
        out[ns] = m.bit_length()
    return out


__all__ = ["CosmicView", "CosmicLedger", "rel_distance", "flat", "flat_ab", "knz", "state_hash", "namespace_bits"]
