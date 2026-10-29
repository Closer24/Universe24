"""Planck's key as swept area: a hand's quanta are its swept area over the key, and its energy per quantum is W key sin omega.

usage: python3 -I planck_key.py <tensor24 src>

On 7a's act (the engine's own tick), a Gaussian hand of one train runs on a ring of L Node-clocks at the vacuum's
gearing, laid as a positive-frequency wave at the wave number k. Each round reads, in whole numbers:
  Q = SUM Im(conj(a) b), the hand's swept area per tick (twice the triangle from its now to its before), the law's
      adiabatic invariant A^2 sin omega summed over the ring (ALGEBRA.md, Planck's relation on the lattice);
  E = W SUM (a - b)^2 - s SUM a F(b), the act's own conserved form, F the pull through the Meshes less the spring.
The law's one quantum is 2 A^2 sin omega = T, T the key (rows 10 and 13 of The conventions and the units), so the
count is n = 2 Q div key, a carry, and for a mode E = 2 W sin(omega) Q, so E / n = W key sin omega: one constant
W key for every train, light or massive, at every wave number. The run measures Q's drift, E / (2 W Q sin omega) and
E / (n W key sin omega) for light and for a massive train at three wave numbers each, sin omega from the act's
dispersion 4 sin^2(omega / 2) = (s / W)(grip (2 - 2 cos k) + D).
"""

import math
import sys

sys.path.insert(0, sys.argv[1])
import numpy as np  # noqa: E402

from tensor24.algebra.carry import home  # noqa: E402
from tensor24.engine import step  # noqa: E402
from tensor24.engine.state import Gearing, Layout, Plan, State  # noqa: E402

KEY = 36000  # the example universe's key (examples/tensor24/universe.json)


def ring(n):
    i = np.arange(n)
    nb = np.stack([(i + 1) % n, (i - 1) % n, i, i, i, i])
    meshes = np.empty((6, n), dtype=np.intp)
    for axis in range(3):
        meshes[2 * axis] = axis * n + i
        meshes[2 * axis + 1] = axis * n + nb[2 * axis + 1]
    return nb, meshes


def layout(n, w, s, grip, d, gamma):
    nb, meshes = ring(n)
    g = np.array([grip] * (3 * n), dtype=object).reshape(1, -1)
    none = np.zeros(0, dtype=np.intp)
    plan = Plan(none, none, none.astype(object), none)
    gearing = Gearing(w, w, s, d, 1, 1)
    rate = np.array([[gamma] * n], dtype=object)
    return Layout(nb, meshes, g, gearing, plan, rate, gamma)


def laid(n, amp, k, omega, w):
    x = np.arange(n)
    now = amp * np.exp(1j * k * x)
    before = amp * np.exp(1j * (k * x + omega))
    a = np.array([[int(round(v.real)) for v in now], [int(round(v.imag)) for v in now]], dtype=object)
    b = np.array([[int(round(v.real)) for v in before], [int(round(v.imag)) for v in before]], dtype=object)
    go = np.zeros((2, n), dtype=object)
    r = np.array([[home(w, 0)] * n] * 2, dtype=object)
    rd = np.zeros((2, n), dtype=object)
    one = np.zeros((1, n), dtype=object)
    return State(a, b, r, go, rd, one.copy(), one.copy(), one.copy())


def swept(st):
    a, b = st.a, st.b
    return int(sum(a[0] * b[1] - a[1] * b[0]))


def form(lay, st, w, s, grip, d):
    a, b = st.a, st.b
    pull_b = grip * (np.roll(b, -1, axis=1) + np.roll(b, 1, axis=1) - 2 * b)
    force_b = pull_b - d * b
    return int((w * (a - b) * (a - b)).sum() - s * (a * force_b).sum())


def main():
    n, gamma = 24, 1000
    w, s = 6 * 1000 * 16 * 16, 1  # W = T at a small den, s = 1: the hand on its own teeth
    grip = w // 6  # the doubler's hold, s grip / W = 1/6
    quanta = 4000
    print(f"a ring of {n} Node-clocks, W = W+ = {w}, s = {s}, the grip W / 6 = {grip}, the key {KEY}, {quanta} quanta laid")
    print("train      k        sin w     drift of Q   E / (2 W Q sin w)   n = 2Q div key   E / (n W key sin w)")
    rows = []
    for name, d in (("light", 0), ("massive", w // 40)):
        for m in (1, 2, 3):
            k = 2 * math.pi * m / n
            lam = grip * (2 - 2 * math.cos(k)) + d
            omega = 2 * math.asin(math.sqrt(s * lam / w) / 2)
            amp = math.sqrt(quanta * KEY / (2 * n * math.sin(omega)))
            lay = layout(n, w, s, grip, d, gamma)
            st = laid(n, amp, k, omega, w)
            allowed = np.ones((1, n), dtype=object)
            period = int(round(2 * math.pi / omega))
            qs, es = [], []
            for _ in range(3 * period):
                qs.append(swept(st))
                es.append(form(lay, st, w, s, grip, d))
                st, _ = step.tick(lay, st, allowed)
            q0 = qs[0]
            drift = max(abs(x - q0) for x in qs) / q0
            ratio = [e / (2 * w * q * math.sin(omega)) for e, q in zip(es, qs)]
            counts = [(2 * q) // KEY for q in qs]
            per = [e / (c * w * KEY * math.sin(omega)) for e, c in zip(es, counts)]
            rows.append((name, k, math.sin(omega), drift, min(ratio), max(ratio), min(counts), max(counts), min(per), max(per)))
            print(
                f"{name:9s} {k:6.4f}   {math.sin(omega):7.5f}   {drift:9.2e}   {min(ratio):.6f} to {max(ratio):.6f}"
                f"   {min(counts)} to {max(counts)}   {min(per):.5f} to {max(per):.5f}"
            )
    lo = min(r[8] for r in rows)
    hi = max(r[9] for r in rows)
    print(f"over both trains and the six waves, 3 turns each: E / (n W key sin omega) lies in [{lo:.5f}, {hi:.5f}]")
    # the swept area per tick is a whole number at every tick, so the count is Rule3's carry with its remainder kept
    print("Q is a whole number at every tick (the product of Gaussian integers), so n = 2 Q div key is one carry, the remainder kept")


if __name__ == "__main__":
    main()
