"""The six-heading gas of the Beam Law as a lattice gas: an integer host map
on the collision table (read-only, the derivation mathematician,
2026-09-21; DERIVATIONS_BEAM.md section 25, round 2). The table is
imported as law data (`collision_table`, `class_key`, nature_beam.py);
nothing runs the engine. Exact arithmetic (Fractions) throughout; decimal
only where a check needs it (the second-order expansion at a small
velocity, the eigenvalues of the relaxation block, the eigenvalues of the
full plane-wave map).

Parts: (A) the 256 binary slot states, their conservation and the parity
of the rest count; (B) the invariant measure; (C) the momentum flux to
second order in the velocity (the Galilean factor, the cube's
anisotropy); (D) the linearized collision operator; (E) the plane-wave
expansion to second order in the wavenumber (the sound speed, the
longitudinal viscosity, the frozen shear wave); (F) the tagged unit's walk
and the diffusion tensor; (G) the temperature reading on series G2's
stars; (H) the ideal gas identity per body; (I) the lamp's cooling
recurrence against the Bell lamp's record.

Two closures are carried through (D) to (F): the law's own sector, "pair"
(rest units arise only in pairs, one slot of two units with its own
density), and the classical lattice-gas closure, "product" (eight
independent slots), for comparison.

Run from the repository root:

    .venv/bin/python docs/designs/derivations_beam/lattice_gas.py > docs/designs/derivations_beam/lattice_gas.out
"""

from __future__ import annotations

import json
import math
import sys
from fractions import Fraction as Fr
from itertools import product
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "src"))

from event_universe.core.game_board import PORT_HEADINGS  # noqa: E402
from event_universe.events.nature_beam import (  # noqa: E402
    COLLISION_SLOTS,
    SLOT_STATES,
    class_key,
    collision_table,
    state_code,
)

SLOTS = COLLISION_SLOTS
HEADINGS = [tuple(int(x) for x in h) for h in PORT_HEADINGS] + [(0, 0, 0), (0, 0, 0)]
C_LIGHT = Fr(32, 55)  # the flight on a heading, Links per interval (2.1)
Q = 64
WAVE = 64  # the wavelength, in Links, of the sound wave whose decay is pinned
DENSITIES = (Fr(1, 16), Fr(1, 8), Fr(1, 4), Fr(1, 2))

Vec = list[Fr]
Mat = list[list[Fr]]


def decode(code: int) -> tuple[int, ...]:
    digits = []
    for _ in range(SLOTS):
        digits.append(code % SLOT_STATES)
        code //= SLOT_STATES
    return tuple(digits)


def dot(u: Vec, v: Vec) -> Fr:
    return sum((a * b for a, b in zip(u, v, strict=True)), Fr(0))


def matvec(m: Mat, v: Vec) -> Vec:
    return [dot(row, v) for row in m]


def solve(m: Mat, rhs: Vec) -> Vec:
    """Gauss-Jordan over the rationals on a square, invertible matrix."""
    n = len(m)
    a = [list(row) + [b] for row, b in zip(m, rhs, strict=True)]
    for col in range(n):
        pivot = next(r for r in range(col, n) if a[r][col] != 0)
        a[col], a[pivot] = a[pivot], a[col]
        p = a[col][col]
        a[col] = [x / p for x in a[col]]
        for r in range(n):
            if r != col and a[r][col] != 0:
                f = a[r][col]
                a[r] = [x - f * y for x, y in zip(a[r], a[col], strict=True)]
    return [row[n] for row in a]


def nullspace(rows: list[Vec], n: int) -> list[Vec]:
    """An orthogonal basis (Gram-Schmidt over the rationals) of the vectors
    of length n orthogonal to every given row."""
    a = [list(r) for r in rows]
    pivots: list[int] = []
    r = 0
    for col in range(n):
        piv = next((i for i in range(r, len(a)) if a[i][col] != 0), None)
        if piv is None:
            continue
        a[r], a[piv] = a[piv], a[r]
        a[r] = [x / a[r][col] for x in a[r]]
        for i in range(len(a)):
            if i != r and a[i][col] != 0:
                f = a[i][col]
                a[i] = [x - f * y for x, y in zip(a[i], a[r], strict=True)]
        pivots.append(col)
        r += 1
    free = [c for c in range(n) if c not in pivots]
    basis = []
    for fcol in free:
        v = [Fr(0)] * n
        v[fcol] = Fr(1)
        for i, pcol in enumerate(pivots):
            v[pcol] = -a[i][fcol]
        for e in basis:
            v = [x - dot(v, e) / dot(e, e) * y for x, y in zip(v, e, strict=True)]
        basis.append(v)
    return basis


def fmt(x: Fr, places: int = 5) -> str:
    return f"{x} = {float(x):.{places}f}" if x.denominator != 1 else str(x)


def dec(x: Fr, places: int = 5) -> str:
    return f"{float(x):.{places}f}"


# --- (A) the binary slot states -------------------------------------------------
table = collision_table()
binary = list(product((0, 1), repeat=SLOTS))
forward = {s: decode(int(table.forward[state_code(s)])) for s in binary}
moving = [s for s in binary if forward[s] != s]
assert all(class_key(s) == class_key(forward[s]) for s in binary)
assert all(all(v in (0, 1) for v in forward[s]) for s in binary)
assert len({forward[s] for s in binary}) == len(binary)
assert all((sum(s[6:]) - sum(forward[s][6:])) % 2 == 0 for s in binary)
print("(A) The binary slot gas: 2^8 = 256 states of the eight slots (six headings in Port")
print("    order, two rest slots), the table's forward map restricted to them.")
print(f"  states {len(binary)}, moving {len(moving)}, fixed {len(binary) - len(moving)}")
print("  the map is a bijection of the 256 (checked) and keeps the class (the crowd mask,")
print("  the number of singles n, the vector sum S of their headings) of every state (checked):")
print("  n and S_x, S_y, S_z are conserved at every Node, hence on every line of Nodes")
print("  along an axis a the sum of S_a is conserved by the flight and the table together")
print("  (a unit with p_a != 0 moves along its own line and never leaves it).")
print("  The parity of the rest count is conserved (checked on the 256): a gas born on the")
print("  headings holds its rest units in pairs at every Node, never one alone.")
pair_cycle = []
s = (1, 1, 0, 0, 0, 0, 0, 0)
for _ in range(4):
    pair_cycle.append(s)
    s = forward[s]
names = ["+x", "-x", "+y", "-y", "+z", "-z", "ha", "hb"]
print(
    "  the head-on pair's cycle: "
    + " -> ".join(" ".join(names[i] for i in range(SLOTS) if st[i]) for st in pair_cycle)
    + " -> ..."
)
print("  the unit's assignment (`collide`, nature_beam.py): the k-th single in slot order")
print("  goes to the k-th occupied slot of the image, so +x -> ha -> +z -> +y -> +x: a")
print("  head-on meeting turns the pair's axis x -> z -> y -> x, one axis per two intervals.")

# --- the slot models ---------------------------------------------------------------


class Model:
    """Groups of slots: each group one binary variable, `units` units when
    occupied, a velocity (lattice units) and the eight-slot pattern it
    fills. `pair`: six headings and the rest pair; `product`: eight slots."""

    def __init__(self, name: str, groups: list[tuple[tuple[int, ...], int]]):
        self.name = name
        self.groups = groups
        self.n = len(groups)
        self.units = [Fr(u) for _, u in groups]
        self.velocity = [[Fr(HEADINGS[slots[0]][a]) for a in range(3)] for slots, _ in groups]
        self.states = list(product((0, 1), repeat=self.n))
        self.forward: dict[tuple[int, ...], tuple[int, ...]] = {}
        for st in self.states:
            full = [0] * SLOTS
            for (slots, _), bit in zip(groups, st, strict=True):
                for sl in slots:
                    full[sl] = bit
            image = forward[tuple(full)]
            out = []
            for slots, _ in groups:
                bits = {image[sl] for sl in slots}
                assert len(bits) == 1, "the image leaves the model's sector"
                out.append(bits.pop())
            self.forward[st] = tuple(out)

    def densities(self, d: Fr) -> Vec:
        """The equilibrium at rest: a heading at d = F(h), a group of u
        units at F(u h) = d^u / (d^u + (1 - d)^u)."""
        return [d**u / (d**u + (1 - d) ** u) for u in self.units]

    def linearized(self, f: Vec) -> Mat:
        a = [[Fr(0)] * self.n for _ in range(self.n)]
        for st in self.states:
            weight = Fr(1)
            for bit, fg in zip(st, f, strict=True):
                weight *= fg if bit else 1 - fg
            out = self.forward[st]
            for i in range(self.n):
                delta = out[i] - st[i]
                if delta == 0:
                    continue
                for j in range(self.n):
                    a[i][j] += delta * weight * (st[j] - f[j]) / (f[j] * (1 - f[j]))
        return a


PAIR = Model("pair", [((i,), 1) for i in range(6)] + [((6, 7), 2)])
PRODUCT = Model("product", [((i,), 1) for i in range(SLOTS)])

# --- (B) the invariant measure -----------------------------------------------------
print()
print("(B) The invariant measure. A product measure over the slots with the weight")
print("    w(s) = exp(-eta n(s) - q . S(s)), n counting every unit, gives every state of one")
print("    class the same weight; the table permutes the class, so the measure is unchanged")
print("    by the collision at every Node, exactly, for every (eta, q): the Fermi-Dirac family")
print("    f_i = 1 / (1 + exp(eta + q . c_i)) on the headings; and on the law's sector the rest")
print("    PAIR at f_p = 1 / (1 + exp(2 eta)) = d^2 / (d^2 + (1 - d)^2), d = 1 / (1 + exp(eta)).")
print("    (Semi-detailed balance holds trivially: the map is a permutation of each class.)")

# --- (C) the momentum flux to second order -------------------------------------------


def fermi(x: float) -> float:
    return 1.0 / (1.0 + math.exp(x))


def gas(h: float, q: tuple[float, float, float]) -> dict[str, object]:
    f = [fermi(h + sum(qa * ca for qa, ca in zip(q, HEADINGS[i], strict=True))) for i in range(6)]
    fp = fermi(2 * h)
    rho = sum(f) + 2 * fp
    j = [sum(f[i] * HEADINGS[i][a] for i in range(6)) for a in range(3)]
    u = [ja / rho for ja in j]
    pi = [
        [sum(f[i] * HEADINGS[i][a] * HEADINGS[i][b] for i in range(6)) for b in range(3)]
        for a in range(3)
    ]
    return {"f": f, "fp": fp, "rho": rho, "u": u, "pi": pi}


print()
print("(C) The momentum flux tensor Pi_ab = sum_i c_ia c_ib f_i to second order in the")
print("    velocity u (lattice units: one Link per step on a heading). Derived in 25.5:")
print("    Pi_ab = delta_ab [2 d + g(d) rho u_a^2] + O(u^4) at a fixed eta (d = F(eta) the heading's")
print("    rest density, rho = 6 d + 2 d_p, g(d) = rho (1 - 2 d) / (4 d (1 - d))); in terms of the")
print("    local density, delta_ab [P(rho) + g rho (u_a^2 - c_s^2 u^2)]; Pi_ab = 0 off the")
print("    diagonal for EVERY state (the headings are axis-aligned). Checked at d = 1/4 (eta = ln 3):")
h = math.log(3.0)
d0 = fermi(h)
dp0 = fermi(2 * h)
rho0 = 6 * d0 + 2 * dp0
g0 = rho0 * (1 - 2 * d0) / (4 * d0 * (1 - d0))
for eps in (1e-2, 5e-3):
    q = (eps, 0.6 * eps, 0.3 * eps)
    state = gas(h, q)
    rho, u, pi = state["rho"], state["u"], state["pi"]
    u2 = sum(x * x for x in u)
    res = [pi[a][a] - 2 * d0 - g0 * rho * u[a] ** 2 for a in range(3)]
    off = max(abs(pi[a][b]) for a in range(3) for b in range(3) if a != b)
    print(
        f"  eps {eps:g}: |u| {math.sqrt(u2):.5f}, residual of Pi_aa {max(abs(r) for r in res):.3e}"
        f" (the O(u^4) term), off-diagonal {off:.1e}"
    )
print(f"  d = 1/4: d_p = 1/10, rho = 17/10, g = {g0:.6f} = 17/15")

# --- (D) the linearized collision operator -----------------------------------------
print()
print("(D) The linearized collision operator A_ij = d Delta_i / d f_j at the equilibrium at")
print("    rest (the Boltzmann level: the product measure over the model's groups at every")
print("    Node). Left null vectors: the mass (the units per group) and the momentum c_a;")
print("    right null vectors: the tangents of the equilibrium family (checked). The")
print("    relaxing modes span the annihilator of the conserved functionals; A on it as a")
print("    block B, with its eigenvalues (decimal check).")


def reduction(model: Model, d: Fr) -> dict[str, object]:
    f = model.densities(d)
    a = model.linearized(f)
    n = model.n
    w_rho = list(model.units)
    w_mom = [[model.units[g] * model.velocity[g][ax] for g in range(n)] for ax in range(3)]
    v_rho = [model.units[g] * f[g] * (1 - f[g]) for g in range(n)]
    v_mom = [
        [model.units[g] * model.velocity[g][ax] * f[g] * (1 - f[g]) for g in range(n)] for ax in range(3)
    ]
    zero = [Fr(0)] * n
    at = [[a[j][i] for j in range(n)] for i in range(n)]
    assert matvec(a, v_rho) == zero and all(matvec(a, v) == zero for v in v_mom)
    assert matvec(at, w_rho) == zero and all(matvec(at, w) == zero for w in w_mom)
    qbasis = nullspace([w_rho, *w_mom], n)
    assert len(qbasis) == n - 4
    cols = []
    for e in qbasis:
        ae = matvec(a, e)
        coords = [dot(g, ae) / dot(g, g) for g in qbasis]
        back = [sum((c * g[i] for c, g in zip(coords, qbasis, strict=True)), Fr(0)) for i in range(n)]
        assert back == ae
        cols.append(coords)
    block = [[cols[m][k] for m in range(n - 4)] for k in range(n - 4)]
    return {
        "f": f,
        "a": a,
        "w_rho": w_rho,
        "w_mom": w_mom,
        "v_rho": v_rho,
        "v_mom": v_mom,
        "qbasis": qbasis,
        "block": block,
    }


def eigen(block: Mat) -> list[float]:
    return sorted(
        float(x.real) for x in np.linalg.eigvals(np.array([[float(x) for x in row] for row in block]))
    )


reductions: dict[tuple[str, Fr], dict[str, object]] = {}
for model in (PAIR, PRODUCT):
    for d in DENSITIES:
        reductions[(model.name, d)] = reduction(model, d)
for d in DENSITIES:
    for model in (PAIR, PRODUCT):
        r = reductions[(model.name, d)]
        ev = eigen(r["block"])
        print(f"  {model.name:>7}, d = {d}: eigenvalues of B " + ", ".join(f"{x:.5f}" for x in ev))
r = reductions[("pair", Fr(1, 4))]
print("  the pair model's block at d = 1/4 (an orthogonal basis of the three relaxing modes):")
for row in r["block"]:
    print("    [" + ", ".join(f"{x!s:>14}" for x in row) + "]")
for e in r["qbasis"]:
    print("    mode " + " ".join(f"{x!s:>6}" for x in e))

# --- (E) the plane wave along x to second order in k ---------------------------------
print()
print("(E) A plane wave along x, exp(i k x), on the linearized lattice Boltzmann map")
print("    L(k) = diag(exp(-i k c_ix)) (I + A), reduced to the conserved modes to O(k^2):")
print("    M = P + k P L1 P + k^2 [P L2 P + P L1 Q (I - L0)^-1 Q L1 P], L1 = -i C (I + A),")
print("    L2 = -(1/2) C^2 (I + A), C = diag(c_ix). Coordinates a = delta rho, b = delta j_x:")
print("      a' = a - i k b + k^2 m_aa a;   b' = b - i k c_s^2 a + k^2 m_bb b  (m_ab = m_ba = 0),")
print("    the modes ln lambda = -+ i c_s k - Gamma k^2 with Gamma = -(m_aa + m_bb) / 2 - c_s^2 / 2,")
print("    the longitudinal viscosity nu_L = 2 Gamma (25.5). The transverse modes (b_y, b_z)")
print("    have lambda = 1 exactly: no shear viscosity.")


def plane_wave(r: dict[str, object], model: Model) -> dict[str, Fr]:
    n = model.n
    a, qbasis = r["a"], r["qbasis"]
    c = [model.velocity[g][0] for g in range(n)]
    w_rho, w_x, v_rho, v_x = r["w_rho"], r["w_mom"][0], r["v_rho"], r["v_mom"][0]
    n_rho, n_x = dot(w_rho, v_rho), dot(w_x, v_x)
    v_all = [v_rho, *r["v_mom"]]
    w_all = [w_rho, *r["w_mom"]]
    norms = [dot(w, v) for w, v in zip(w_all, v_all, strict=True)]

    def project_q(x: Vec) -> Vec:
        px = [Fr(0)] * n
        for v, w, nm in zip(v_all, w_all, norms, strict=True):
            coef = dot(w, x) / nm
            px = [p + coef * vi for p, vi in zip(px, v, strict=True)]
        return [xi - pi for xi, pi in zip(x, px, strict=True)]

    def a_inverse_on_q(x: Vec) -> Vec:
        coords = [dot(g, x) / dot(g, g) for g in qbasis]
        y = solve(r["block"], coords)
        return [sum((yc * g[i] for yc, g in zip(y, qbasis, strict=True)), Fr(0)) for i in range(n)]

    def apply_c(x: Vec) -> Vec:
        return [ci * xi for ci, xi in zip(c, x, strict=True)]

    def apply_l0(x: Vec) -> Vec:
        ax = matvec(a, x)
        return [xi + yi for xi, yi in zip(x, ax, strict=True)]

    def second_order(v: Vec) -> Vec:
        """[P L2 P + P L1 Q (I - L0)^-1 Q L1 P] v, before the left projection,
        for v in the P-space: -(1/2) C^2 v - C (I + A) Q (-A_Q)^-1 Q C v."""
        l2 = [-Fr(1, 2) * ci * ci * vi for ci, vi in zip(c, v, strict=True)]
        y = project_q(apply_c(v))
        y = a_inverse_on_q(y)  # A_Q^-1 y
        y = [-yi for yi in y]  # (-A_Q)^-1
        y = project_q(y)
        y = apply_l0(y)
        y = apply_c(y)
        return [l2i - yi for l2i, yi in zip(l2, y, strict=True)]

    m1_ab = dot(w_rho, apply_c(v_x)) / n_x  # a' gets -i k m1_ab b
    m1_ba = dot(w_x, apply_c(v_rho)) / n_rho  # b' gets -i k m1_ba a
    m1_aa = dot(w_rho, apply_c(v_rho)) / n_rho
    m1_bb = dot(w_x, apply_c(v_x)) / n_x
    assert m1_aa == 0 and m1_bb == 0 and m1_ab == 1
    s_rho, s_x = second_order(v_rho), second_order(v_x)
    m_aa = dot(w_rho, s_rho) / n_rho
    m_ab = dot(w_rho, s_x) / n_x
    m_ba = dot(w_x, s_rho) / n_rho
    m_bb = dot(w_x, s_x) / n_x
    assert m_ab == 0 and m_ba == 0
    # the transverse modes: C v_y = 0 and (I + A) v_y = v_y
    assert all(x == 0 for x in apply_c(r["v_mom"][1])) and apply_l0(r["v_mom"][1]) == r["v_mom"][1]
    cs2 = m1_ba
    gamma = -(m_aa + m_bb) / 2 - cs2 / 2
    return {"cs2": cs2, "m_aa": m_aa, "m_bb": m_bb, "gamma": gamma, "nu_l": 2 * gamma}


waves: dict[tuple[str, Fr], dict[str, Fr]] = {}
for model in (PAIR, PRODUCT):
    for d in DENSITIES:
        waves[(model.name, d)] = plane_wave(reductions[(model.name, d)], model)
print("  the law's sector (pair):")
for d in DENSITIES:
    wv = waves[("pair", d)]
    cs = math.sqrt(float(wv["cs2"]))
    print(
        f"  d = {d}: c_s^2 = {fmt(wv['cs2'])}, m_aa = {dec(wv['m_aa'])}, m_bb = {dec(wv['m_bb'])},"
        f" Gamma = {fmt(wv['gamma'])}, nu_L = {fmt(wv['nu_l'])} (lattice units)"
    )
    cs_phys = cs * float(C_LIGHT)
    nu_phys = float(wv["nu_l"] * C_LIGHT**2)
    decay = 1 / (float(wv["gamma"] * C_LIGHT**2) * (2 * math.pi / WAVE) ** 2)
    print(
        f"           in Links and intervals: c_s = {cs:.5f} c = {cs_phys:.5f} Links per interval,"
        f" nu_L = {nu_phys:.5f} Links^2 per interval; a sound wave of {WAVE} Links falls to 1/e"
        f" in {decay:.0f} intervals"
    )
print("  the classical closure (product; the rest slots independent):")
for d in DENSITIES:
    wv = waves[("product", d)]
    print(
        f"  d = {d}: c_s^2 = {fmt(wv['cs2'])}, Gamma = {fmt(wv['gamma'])}, nu_L = {fmt(wv['nu_l'])}"
        f" (lattice units); in Links^2 per interval {float(wv['nu_l'] * C_LIGHT**2):.5f}"
    )
print("  a decimal check of the reduction: the eigenvalues of the full L(k) at a small k")
print("  against -+ i c_s k - Gamma k^2 (the sound pair) and 1 (the two shear modes):")
for model in (PAIR, PRODUCT):
    for d in DENSITIES:
        r = reductions[(model.name, d)]
        wv = waves[(model.name, d)]
        l0 = np.eye(model.n) + np.array([[float(x) for x in row] for row in r["a"]])
        gamma, cs = float(wv["gamma"]), math.sqrt(float(wv["cs2"]))
        for k in (1e-2, 5e-3):
            e = np.diag([np.exp(-1j * k * float(model.velocity[g][0])) for g in range(model.n)])
            lam = np.linalg.eigvals(e @ l0)
            logs = np.log(lam)
            sound = sorted(logs, key=lambda z: abs(z.imag - cs * k))[0]
            unit = sum(1 for z in lam if abs(z - 1) < 1e-12)
            print(
                f"  {model.name:>7}, d = {d}, k = {k:g}: ln lambda = {sound.real:+.4e} {sound.imag:+.7f} i"
                f" against {-gamma * k * k:+.4e} {cs * k:+.7f} i; modes at exactly 1: {unit}"
            )

# --- (F) the tagged unit's walk ----------------------------------------------------
print()
print("(F) The tagged unit on the law's sector: from a heading, the other five headings")
print("    each held with probability d and the rest pair with d_p; from a rest slot, its")
print("    partner present with certainty (the pair) and the headings at d. The new slot by")
print("    the table's rule (the k-th single in slot order to the k-th occupied slot of the")
print("    image). Transition matrix T_ij(d) on the eight slots; the equilibrium occupation")
print("    (d per heading, d_p per rest slot) is stationary (checked). The diffusion tensor")
print("    D_ab = c^2 [C_0^ab / 2 + sum_{k >= 1} (C_k^ab + C_k^ba) / 2], C_k^ab = <e_a(0) e_b(k)>.")


def tagged(d: Fr) -> tuple[Mat, Vec]:
    dp = d * d / (d * d + (1 - d) * (1 - d))
    t = [[Fr(0)] * SLOTS for _ in range(SLOTS)]
    for i in range(SLOTS):
        heads = [j for j in range(6) if j != i]
        rest_i = i >= 6
        for bits in product((0, 1), repeat=len(heads)):
            for pair in (1,) if rest_i else (0, 1):
                s = [0] * SLOTS
                s[i] = 1
                for j, bit in zip(heads, bits, strict=True):
                    s[j] = bit
                if pair:
                    s[6] = s[7] = 1
                n_other = sum(bits)
                weight = d**n_other * (1 - d) ** (len(heads) - n_other)
                if not rest_i:
                    weight *= dp if pair else 1 - dp
                st = tuple(s)
                out = forward[st]
                if out == st:
                    t[i][i] += weight
                    continue
                singles_in = [j for j in range(SLOTS) if st[j] == 1]
                singles_out = [j for j in range(SLOTS) if out[j] == 1]
                t[i][singles_out[singles_in.index(i)]] += weight
    total = 6 * d + 2 * dp
    pi = [d / total] * 6 + [dp / total] * 2
    return t, pi


for d in DENSITIES:
    t, pi = tagged(d)
    assert all(sum(row) == 1 for row in t)
    assert [sum(pi[i] * t[i][j] for i in range(SLOTS)) for j in range(SLOTS)] == pi
    tails = []
    for ax in range(3):
        e = [Fr(HEADINGS[i][ax]) for i in range(SLOTS)]
        m = [[(Fr(1) if i == j else Fr(0)) - t[i][j] for j in range(SLOTS)] for i in range(SLOTS)]
        rhs = list(e)
        m[SLOTS - 1] = list(pi)
        rhs[SLOTS - 1] = Fr(0)
        tails.append(matvec(t, solve(m, rhs)))  # sum_{k >= 1} T^k e_a
    e_ax = [[Fr(HEADINGS[i][ax]) for i in range(SLOTS)] for ax in range(3)]
    tensor = [
        [
            sum((pi[i] * e_ax[a][i] * e_ax[b][i] for i in range(SLOTS)), Fr(0)) / 2
            + (
                sum((pi[i] * e_ax[a][i] * tails[b][i] for i in range(SLOTS)), Fr(0))
                + sum((pi[i] * e_ax[b][i] * tails[a][i] for i in range(SLOTS)), Fr(0))
            )
            / 2
            for b in range(3)
        ]
        for a in range(3)
    ]
    turn = [1 - t[i][i] for i in range(6)]
    park = [t[i][6] + t[i][7] for i in range(6)]
    print(f"  d = {d} (d_p = {d * d / (d * d + (1 - d) ** 2)}):")
    print(
        "    turning probability per interval, +x -x +y -y +z -z: " + ", ".join(dec(x, 4) for x in turn)
    )
    print("    parking probability (into the rest pair):          " + ", ".join(dec(x, 4) for x in park))
    print("    D (lattice units), rows x, y, z:")
    for row in tensor:
        print("      [" + ", ".join(f"{dec(x, 5):>9}" for x in row) + "]")
    phys = [[x * C_LIGHT**2 for x in row] for row in tensor]
    print(
        "    in Links^2 per interval: diagonal "
        + ", ".join(dec(phys[a][a]) for a in range(3))
        + "; off-diagonal xy, xz, yz "
        + ", ".join(dec(phys[a][b]) for a in range(3) for b in range(a + 1, 3))
    )
    ev = sorted(np.linalg.eigvalsh(np.array([[float(x) for x in row] for row in phys])))
    trace = sum(phys[a][a] for a in range(3))
    print(
        f"    principal values {', '.join(f'{x:.5f}' for x in ev)} Links^2 per interval;"
        f" the mean D = tr / 3 = {dec(trace / 3)}; the memoryless 1 / (3 p_turn) at +x would be"
        f" {float(C_LIGHT**2 / (3 * turn[0])):.5f}"
    )
    if d == Fr(1, 8):
        print(
            "    exact at d = 1/8, lattice units: D_xx = "
            + str(tensor[0][0])
            + ", D_xz = "
            + str(tensor[0][2])
        )

# --- (G) the temperature reading on series G2 ---------------------------------------
print()
print("(G) Theta_a = (1 / n) sum p_a^2 / (Q S M) on series G2's 24 stars (the declared")
print("    momenta of examples/events/hubble_stars/coasting_none.json; S = 2^20, M = 2^22,")
print("    Q S M = 2^48), and the kinetic form (1 / n) sum p_a v_a, v_a = |p_a| / (Q S M + |p_a|).")
world = json.loads((ROOT / "examples" / "events" / "hubble_stars" / "coasting_none.json").read_text())
stars = [m for m in world["measured"] if m["family"].startswith("s_")]
assert len(stars) == 24
QSM = Q * world["width"] * stars[0]["held"]["mass"]
assert QSM == 2**48
for ax, name in enumerate("xyz"):
    ps = [Fr(s["momentum"][ax]) for s in stars]
    theta = sum(p * p for p in ps) / (24 * QSM)
    kinetic = sum(p * p / (QSM + abs(p)) for p in ps) / 24
    paces = [abs(p) / (QSM + abs(p)) for p in ps if p]
    print(
        f"  axis {name}: Theta / (Q S M) = {float(theta / QSM):.6f} (the mean of (p_a / Q S M)^2),"
        f" the kinetic mean over Q S M {float(kinetic / QSM):.6f}, the ratio {float(kinetic / theta):.5f};"
        f" paces {min(map(float, paces)):.4f} .. {max(map(float, paces)):.4f}"
    )
    print(
        f"          Theta = {theta.numerator}/{theta.denominator} = {float(theta):.1f} label^2 per content unit"
    )

# --- (H) the ideal gas identity per body ---------------------------------------------
print()
print("(H) One free body of content M on a bar of L Links along x between two fixed")
print("    occupants declaring `rerelease`: the impulse per bounce 2 |p|, the bounces per")
print("    interval v / (2 L), the mean force on one wall p v / L, so P V = p v exactly")
print("    in the mean, against Theta = p^2 / (Q S M): the ratio 1 - v (25.7). At Q S M = 4096:")
for p in (220, 1024, 4096):
    v = Fr(p, 4096 + p)
    print(
        f"  p = {p}: v = {fmt(v)}, p v = {fmt(p * v, 3)}, p^2 / (Q S M) = {fmt(Fr(p * p, 4096), 3)},"
        f" ratio {fmt(1 - v)}"
    )

# --- (I) the lamp's cooling ----------------------------------------------------------
print()
print("(I) The lamp's content under its own release: the turn accumulator gains M(t) x n")
print("    per self-creation and pays h b s_t, s_t its whole part in units of d (engine.py")
print("    `_frame_all`, by_drive). The Bell lamp (examples/events/bell): M_0 = K + 2,")
print("    K = 2^20 = [1, K], h = 1, b = 2 directions; registered: one stall, at tick 4,")
print("    159 births in 160.")
K = 2**20
acc, M = 0, K + 2
births, stalls = 0, []
rate = Fr(2, K)
worst = Fr(0)
for tick in range(1, 161):
    acc += M
    s = acc // K
    acc -= s * K
    if s == 0:
        stalls.append(tick)
    else:
        births += 1
        M -= 2 * s
    exact = (K + 2) * (1 - rate) ** tick
    worst = max(worst, abs(M - exact))
print(f"  the recurrence: births {births}, stalls at ticks {stalls}, content after 160 ticks {M}")
print(f"  |M(t) - M_0 (1 - r)^t| over the run at most {float(worst):.6f} < h b = 2 (25.9's bound)")
