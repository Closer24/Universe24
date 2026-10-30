"""Hostile physicist, check D: 'a bound clock's active mass is its energy' (N2 P3): <4K - 2V> = E on the engine's
act for the harmonic spring and for a quartic one (a cubic force, the kind of term G3's vertex adds).

Clock: one hand on one Node-clock, held by -g a (harmonic) or by -k a^3 (quartic), the metric standing.
Algebra: whole numbers; the engine's step.tick with a Plan monomial; the sum form W (sigma_b^2 + sigma_a^2) - 2V
accumulated over many swings against the start's energy, at strides of hundreds so the floor is below a percent.
Board: one Node-clock.
Clicks: the texts read rho + 3 pr = 4K - 2V averaging to the swing's energy; for V ~ a^n the virial gives
4 (n - 1) / (n + 2) E: 1 for n = 2, 2 for n = 4.

Run: <t24b>/.venv/bin/python -I d_virial_quartic.py
"""

import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE / "copy" / "n2_second"))

import numpy as np  # noqa: E402
from n2b_lib import A1ROWS, ROWS, UNIT, VALUE, State, at, carry, engine_plan, layout, step, terms  # noqa: E402

W = 3 * 10**7  # teeth large enough that strides of hundreds stand below a percent of the floor's share
CLOCK = A1ROWS[0]
A0 = 1000
T = 20000


def permille(num, den):
    q, _ = carry(1000 * num, den, 0)
    return int(q)


def run(plan, two_v, four_e0, name):
    L = layout((1, 1, 1), W, W, 1, 1, 1, clock="none")._replace(plan=engine_plan(plan))
    a = np.zeros((ROWS, 1), dtype=object)
    a[CLOCK, 0] = A0
    s = State(a, a.copy(), 0 * a, 0 * a)  # at rest at the turning point: sigma_b = 0
    acc = 0
    lo, hi, smax = A0, A0, 0
    for _ in range(T):
        a0, b0 = int(s.a[CLOCK, 0]), int(s.b[CLOCK, 0])
        s = step.tick(L, s)
        a1 = int(s.a[CLOCK, 0])
        sb, sa = a0 - b0, a1 - a0
        acc += 2 * W * (sb * sb + sa * sa) - 2 * two_v(a0)  # 2 (4K - 2V) = 2 W (sigma_b^2 + sigma_a^2) - 4V
        lo, hi, smax = min(lo, a1), max(hi, a1), max(smax, abs(sa))
    # acc = 2 sum (4K - 2V); E = four_e0 / 4: <4K - 2V> / E = acc / (2 T E) = acc / (T four_e0 / 2) = 2 acc / (T four_e0)
    print(f"  {name}: over {T} rounds the count ranged over [{lo}, {hi}], the largest stride {smax}; <4K - 2V> / E = {permille(2 * acc, T * four_e0)} permille")


print("== D. <4K - 2V> against the swing's energy E on the engine's act, the sum form, at W = 3 x 10^7")
G = 3 * 10**6  # omega^2 = g / W = 1 / 10
run(terms([(at(VALUE, CLOCK), UNIT, UNIT, -G, CLOCK)]), lambda a: G * a * a, 2 * G * A0 * A0, "harmonic, V = g a^2 / 2 (omega^2 = 1/10)")
K = 1  # omega^2 at the turning point 3 k a0^2 / W = 1 / 10
run(terms([(at(VALUE, CLOCK), at(VALUE, CLOCK), at(VALUE, CLOCK), -K, CLOCK)]), lambda a: (K * a**4) // 2, K * A0**4, "quartic, V = k a^4 / 4 (3 k a0^2 / W = 1/10)")
print("  reading: the identity 'active mass = energy' is the harmonic spring's K-bar = V-bar; a quartic hand sources twice its energy. P3 holds for term 6's spring alone and not for G3's vertex")
