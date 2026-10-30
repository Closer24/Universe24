"""The discrete energy of (1)'s swing, swing by swing, over 214 swings (30,000 ticks): wander or drift.

usage: python3 -I q1b_energy.py <tensor24 src>
"""
import sys

sys.path.insert(0, sys.argv[1])
import numpy as np  # noqa: E402

from tensor24.algebra.carry import home  # noqa: E402
from tensor24.engine import step  # noqa: E402
from tensor24.engine.state import Gearing, Layout, Plan, State  # noqa: E402

GAMMA, w, D, m = 1000, 500, 1, 30
cstar = m * m // D
obj = lambda x: np.asarray(x, dtype=object)  # noqa: E731
nb = np.zeros((6, 1), int)  # one Node-clock, its own neighbour on every Spoke: the board's mean alone
layout = Layout(nb, np.zeros((6, 1), int), obj(np.zeros((2, 3), int)),
                Gearing(obj([[w], [1]]), obj([[w], [1]]), 1, obj([[D], [0]]), 1, obj([[1], [1]])),
                Plan(np.array([1], np.intp), np.array([1], np.intp), obj([1]), np.array([0], np.intp)),
                obj([[GAMMA]]), GAMMA)
a = obj([[0], [m]])
s = State(a, a.copy(), obj([[home(w, 0)], [0]]), obj([[0], [0]]), obj([[0], [0]]), obj([[0]]), obj([[0]]), obj([[0]]))
E, tops = [], []
prev = 0
for t in range(30000):
    s, _ = step.tick(layout, s, 1)
    p = w * (s.a[0, 0] - s.b[0, 0]) + (s.r[0, 0] - home(w, s.go[0, 0]))
    E.append(int(p * p + w * D * (s.a[0, 0] - cstar) * (s.b[0, 0] - cstar)))
    tops.append(int(s.a[0, 0]))
per = 30000 // 140
means = [sum(E[i * 140:(i + 1) * 140]) / 140 for i in range(per)]
peaks = [max(tops[i * 140:(i + 1) * 140]) for i in range(per)]
x = np.arange(per)
slope = np.polyfit(x, means, 1)[0]
print(f"one Node-clock (the board's mean), 30,000 ticks, {per} windows of 140 ticks:")
print(f"  the energy's window means: {min(means):,.0f} to {max(means):,.0f}, first {means[0]:,.0f}, last {means[-1]:,.0f};"
      f" a straight line through them moves {slope * per / means[0]:+.3%} of the first over the run")
print(f"  the windows' largest counts: {min(peaks):,} to {max(peaks):,} (2 c* = {2 * cstar:,})")
print(f"  the means of the first 50 windows {np.mean(means[:50]):,.0f} and of the last 50 {np.mean(means[-50:]):,.0f}")
