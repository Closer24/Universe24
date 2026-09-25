"""The families together as one board: the coupled step of ALGEBRA.md 8.5 on integers, and the
property test of 9.20 on it (equivariance under the 48, translation on the torus, the invariant
J between clicks, reversibility, locality). Not engine code; a prototype beside board_algebra.py.

Two families on a torus of N^3: a massive kind [800, 809] with a well [800, 801] of side 2 (its
record seeded on the composed operator's bound mode) and light [1, 1] with no record at first.
The coupling on the well's cells with g = [1, 1000] and G = [1, 50] (8.5): the massive step reads
light's backward difference, then light's step reads the massive forward difference, both folded
into the rows' walls (one division per row per interval, the remainder kept). The invariant J =
I_m + alpha I_l + g SUM over the cells of D_i (delta m)(delta l), alpha = g D_in / G, is conserved
exactly before the remainders (8.5, PROVED); on integers to the remainder's grain."""

import itertools

import numpy as np

N = 8
SHAPE = (N, N, N)
G_N, G_D = 1, 50  # light's row gains -G x (the massive forward difference), G = G_N / G_D
g_N, g_D = 1, 1000  # the massive row gains g x (light's backward difference), g = g_N / g_D


def s6(a):
    return sum(np.roll(a, s, axis=ax) for ax in range(3) for s in (1, -1))


def obj(x):
    return np.array(x, dtype=object)


class Board:
    """One element: the two families' rows with their remainders; one operator: the pairs."""

    def __init__(self, well_vertex=(1, 2, 3), side=2, amplitude=1 << 12):
        self.num_m = np.full(SHAPE, 800, dtype=object)
        self.den_m = np.full(SHAPE, 809, dtype=object)
        self.cells = np.zeros(SHAPE, dtype=bool)
        for d in itertools.product(range(side), repeat=3):
            self.cells[tuple((np.array(well_vertex) + d) % N)] = True
        self.num_m[self.cells] = 800
        self.den_m[self.cells] = 801
        self.num_l = np.full(SHAPE, 1, dtype=object)
        self.den_l = np.full(SHAPE, 1, dtype=object)
        # the walls carry the couplings' denominators (one division per row per interval)
        self.wall_m = 3 * self.den_m * g_D
        self.wall_l = 3 * self.den_l * G_D
        lam, mode = self.bound_mode()
        self.lam = lam
        seed = obj(np.rint(mode * amplitude).astype(np.int64))
        zero = np.zeros(SHAPE, dtype=object)
        self.m = [
            seed.copy(),
            seed.copy(),
            zero.copy(),
        ]  # now, before, remainder (on the wall 3 den g_D)
        self.l = [zero.copy(), zero.copy(), zero.copy()]

    def bound_mode(self):
        ratio = self.den_m.astype(float) / self.num_m.astype(float)
        sc = 1 / np.sqrt(ratio)
        n = N**3
        A = np.zeros((n, n))
        idx = np.arange(n).reshape(SHAPE)
        for ax in range(3):
            for s in (1, -1):
                nb = np.roll(idx, s, axis=ax)
                A[idx.ravel(), nb.ravel()] += 1
        M = (sc.ravel()[:, None] * A * sc.ravel()[None, :]) / 3
        w, v = np.linalg.eigh(M)
        mode = (v[:, -1] * sc.ravel()).reshape(SHAPE)
        mode = mode / np.abs(mode).max()
        if mode.ravel()[np.argmax(np.abs(mode))] < 0:
            mode = -mode
        return w[-1], mode

    def step(self):
        """8.5's column order: the massive step with light's backward difference, then light's
        step with the massive forward difference; each row divided once by its wall."""
        m_now, m_before, m_r = self.m
        l_now, l_before, l_r = self.l
        delta_l = np.where(self.cells, l_now - l_before, 0)
        total = (
            g_D * self.num_m * s6(m_now) - self.wall_m * m_before + m_r + 3 * self.den_m * g_N * delta_l
        )
        m_next = total // self.wall_m
        m_r2 = total % self.wall_m
        delta_m = np.where(self.cells, m_next - m_now, 0)
        total = (
            G_D * self.num_l * s6(l_now) - self.wall_l * l_before + l_r - 3 * self.den_l * G_N * delta_m
        )
        l_next = total // self.wall_l
        l_r2 = total % self.wall_l
        self.m = [m_next, m_now, m_r2]
        self.l = [l_next, l_now, l_r2]

    def step_inverse(self):
        """The inverse, in the reverse column order (8.8): light first, then the massive row."""
        m_now, m_before, m_r = self.m  # m_now = a_next, m_before = a_now of the forward step
        l_now, l_before, l_r = self.l
        delta_m = np.where(self.cells, m_now - m_before, 0)
        total = (
            G_D * self.num_l * s6(l_before) - self.wall_l * l_now - l_r - 3 * self.den_l * G_N * delta_m
        )
        l_prev = -((-total) // self.wall_l)  # ceil
        l_r_prev = self.wall_l * l_prev - total
        self.l = [l_before, l_prev, l_r_prev]
        l_now, l_before, _ = self.l
        delta_l = np.where(self.cells, l_now - l_before, 0)
        total = (
            g_D * self.num_m * s6(m_before) - self.wall_m * m_now - m_r + 3 * self.den_m * g_N * delta_l
        )
        m_prev = -((-total) // self.wall_m)
        m_r_prev = self.wall_m * m_prev - total
        self.m = [m_before, m_prev, m_r_prev]

    def form_I(self, rows, num, den):
        now, before, _ = rows
        D = den.astype(float) / num.astype(float)
        a_next, a_now = now.astype(float), before.astype(float)
        return float(np.sum(D * (a_next**2 + a_now**2)) - np.sum(a_next * s6(a_now)) / 3)

    def J(self):
        """8.5's invariant, in floats from the integer state: I_m + alpha I_l + g sum D (delta m)(delta l)."""
        g = g_N / g_D
        G = G_N / G_D
        D_in = 801 / 800
        alpha = g * D_in / G
        I_m = self.form_I(self.m, self.num_m, self.den_m)
        I_l = self.form_I(self.l, self.num_l, self.den_l)
        dm = (self.m[0] - self.m[1]).astype(float)
        dl = (self.l[0] - self.l[1]).astype(float)
        cross = g * float(np.sum(np.where(self.cells, D_in * dm * dl, 0.0)))
        return I_m + alpha * I_l + cross, I_m, I_l

    def state(self):
        return [a.copy() for a in self.m] + [a.copy() for a in self.l]


def all_48():
    return [
        (p, s) for p in itertools.permutations(range(3)) for s in itertools.product((1, -1), repeat=3)
    ]


def apply_g(arr, g):
    perm, signs = g
    src = np.indices(SHAPE).reshape(3, -1)
    dst = np.empty_like(src)
    for k in range(3):
        dst[k] = (signs[k] * src[perm[k]]) % N
    out = np.empty_like(arr)
    out[dst[0], dst[1], dst[2]] = arr[src[0], src[1], src[2]]
    return out


def transformed(board, g):
    t = Board.__new__(Board)
    for name in ("num_m", "den_m", "num_l", "den_l", "wall_m", "wall_l", "cells"):
        setattr(t, name, apply_g(getattr(board, name), g))
    t.m = [apply_g(a, g) for a in board.m]
    t.l = [apply_g(a, g) for a in board.l]
    t.lam = board.lam
    return t


def equal(b1, b2):
    return all(np.array_equal(x, y) for x, y in zip(b1.state(), b2.state(), strict=True))


def main():
    steps = 40
    b = Board()
    print(
        f"the coupled board {N}^3: the well [800, 801] on [800, 809] with lambda_max {b.lam:.6f} (< 2), light coupled on its cells with g = 1/1000, G = 1/50"
    )
    # J between clicks, and the block radiating
    b = Board()
    J0, Im0, Il0 = b.J()
    worst = 0.0
    for _t in range(200):
        b.step()
        J, Im, Il = b.J()
        worst = max(worst, abs(J - J0) / J0)
    print(
        f"(3) J over 200 intervals: relative drift at most {worst:.2e} (the remainder's grain; exact before the remainders, 8.5); the well radiates: I_m {Im0:.4e} -> {Im:.4e}, I_l {Il0:.1f} -> {Il:.4e}"
    )
    # equivariance under the 48
    ref = Board()
    for _ in range(steps):
        ref.step()
    ok = 0
    for g in all_48():
        tb = transformed(Board(), g)
        for _ in range(steps):
            tb.step()
        ok += equal(tb, transformed(ref, g))
    print(
        f"(1) equivariance under the 48 of the coupled step over {steps} intervals: {ok} of 48 identical bit for bit"
    )
    # translation
    ok = 0
    shifts = [(1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, 1), (0, 0, -1), (3, 5, 7)]
    for sh in shifts:
        tb = Board(well_vertex=tuple((np.array((1, 2, 3)) + sh) % N))
        for _ in range(steps):
            tb.step()
        ok += all(
            np.array_equal(x, np.roll(y, sh, axis=(0, 1, 2)))
            for x, y in zip(tb.state(), ref.state(), strict=True)
        )
    print(f"(2) translation on the torus, 7 shifts: {ok} of 7 identical")
    # reversibility
    b = Board()
    start = b.state()
    for _ in range(steps):
        b.step()
    for _ in range(steps):
        b.step_inverse()
    rev = all(np.array_equal(x, y) for x, y in zip(start, b.state(), strict=True))
    print(
        f"(4) reversibility of the coupled step: {steps} forward then {steps} inverse return both families bit for bit, remainders included: {rev}"
    )
    # locality: a unit change of light at one Node
    b1, b2 = Board(), Board()
    b2.l[0][5, 5, 5] += 1
    inside = True
    for m in range(1, 8):
        b1.step()
        b2.step()
        diff = np.zeros(SHAPE, dtype=bool)
        for x, y in zip(b1.state(), b2.state(), strict=True):
            diff |= x != y
        ix = np.indices(SHAPE)
        dist = sum(np.minimum((ix[a] - 5) % N, (5 - ix[a]) % N) for a in range(3))
        inside = inside and not np.any(diff & (dist > m))
    print(
        f"(5) locality across the coupling: a one-unit change of light at one Node stays inside the Manhattan ball of radius m at interval m, m = 1..7: {inside}"
    )


if __name__ == "__main__":
    main()
