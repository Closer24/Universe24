"""Light through a slowed slab on 7a's own tick: the beat alone against the beat with the grip at both ends' rates.

A real A1 gear on a ring of L sites (sides L, 1, 1), W = W+ = 4 Gamma^2, s = 1, no spring, no J, so the vacuum's
speed is 1/2 Mesh a tick. Inside the slab every Node-clock's rate is p < Gamma, so its gears tick on a fraction
N = p / Gamma of the rounds. Case "beat": the grip is the vacuum's, Gamma^2, on every Mesh. Case "grip": the grip of
the Mesh between sites i and j is rate_i rate_j (the Mesh's rate as the product of its two clocks'). The pulse's
peak is timed at a detector past the slab; the extra delay over the vacuum's is set against the continuum's
L_slab (1 / v_in - 1 / v0), v_in = N v0 (beat) or N^2 v0 (grip).

Usage: python slab7b.py <the repository's root> [p, 800 by default]; slab7b.txt holds p = 800, 900 and 950.
"""

import math
import sys

import numpy as np

sys.path.insert(0, sys.argv[1] + "/src")
from tensor24.algebra.carry import home  # noqa: E402
from tensor24.engine import step  # noqa: E402
from tensor24.engine.state import Gearing, Layout, Plan, State  # noqa: E402
from tensor24.runner.board import board  # noqa: E402

L, GAMMA, P = 400, 1000, int(sys.argv[2]) if len(sys.argv) > 2 else 800
SLAB, X0, XD, SIGMA, AMP = (150, 190), 60, 300, 8.0, 10**9
W = 4 * GAMMA * GAMMA


def layout(case):
    nb, meshes = board((L, 1, 1))
    n = L
    inside = np.zeros(n, dtype=bool)
    inside[SLAB[0] : SLAB[1]] = True
    rate = np.where(inside, P, GAMMA).astype(object) if case != "vacuum" else np.full(n, GAMMA, dtype=object)
    grip = np.zeros((1, 3 * n), dtype=object)
    if case == "grip":
        grip[0, :n] = rate * np.roll(rate, -1)  # Mesh i joins site i and i + 1
    else:
        grip[0, :n] = GAMMA * GAMMA
    one = np.ones((1, 1), dtype=object)
    gearing = Gearing(np.full((1, n), W, dtype=object), np.full((1, n), W, dtype=object), one, 0 * one, one, one)
    none = np.zeros(0, dtype=np.intp)
    plan = Plan(none, none, none.astype(object), none)
    return Layout(nb, meshes, grip, gearing, plan, rate[None, :], GAMMA)


def start():
    x = np.arange(L)
    a = np.array([round(AMP * math.exp(-((i - X0) ** 2) / (2 * SIGMA**2))) for i in x], dtype=object)
    b = np.array([round(AMP * math.exp(-((i + 0.5 - X0) ** 2) / (2 * SIGMA**2))) for i in x], dtype=object)
    zero = np.zeros((1, L), dtype=object)
    r = np.full((1, L), home(W, 0), dtype=object)
    return State(a[None, :], b[None, :], r, zero.copy(), zero.copy(), zero.copy(), zero.copy(), zero.copy())


def arrival(case, rounds=900):
    lay, s = layout(case), start()
    allowed = np.ones((1, L), dtype=object)
    trace = []
    for _ in range(rounds):
        s, _ = step.tick(lay, s, allowed)
        trace.append(s.a[0, XD])
    trace = np.array(trace, dtype=object)
    t = int(np.argmax(trace))
    # the peak's round, refined by a parabola through its two neighbours
    y0, y1, y2 = (float(trace[t + d]) for d in (-1, 0, 1))
    return t + 1 + 0.5 * (y0 - y2) / (y0 - 2 * y1 + y2), float(trace[t]) / AMP


if __name__ == "__main__":
    n_rate = P / GAMMA
    v0, width = 0.5, SLAB[1] - SLAB[0]
    tv, hv = arrival("vacuum")
    print(f"Gamma {GAMMA}, p {P}, N {n_rate}, slab {width} Meshes, vacuum speed {v0} Mesh per tick")
    print(f"vacuum: peak at round {tv:.2f} (height {hv:.3f})")
    for case, v_in in (("beat", n_rate * v0), ("grip", n_rate * n_rate * v0)):
        t, h = arrival(case)
        want = width * (1 / v_in - 1 / v0)
        print(f"{case}: peak at round {t:.2f} (height {h:.3f}); extra delay {t - tv:.2f}, continuum {want:.2f}")
