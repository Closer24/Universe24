"""THIRD7's word on mode 11's memory (#2187 6540451346 item 4): the triangle's tooth and twin turned at K = 3 obey
L^2 = 38 L - I, so the landings follow a two-step recurrence and, at a steady passing, a period. Here, at several
steady circulating passings y = a x 3D (the triangle alone; the edge teeth do not reach its landings): the landing
rate, after one landing the next against independent, after two in a row a third against the rate after one, and
the round at which the triangle's tooth and twin first return to their birth (the period), up to the rounds run.
Whole numbers and Rule3's carry alone.

Usage: python3 -I memrates.py <src> <rounds> <num> <den>   (the rate a = num / den of the dial 3D)
"""
import sys

sys.path.insert(0, sys.argv[1])
sys.path.insert(0, ".")
from tensor24.algebra.carry import carry  # noqa: E402

import circ  # noqa: E402
import edgeclick as E  # noqa: E402

rounds, num, den = int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4])
universe, shape, held, lay, s0, world = E.load_world(sys.argv[1], "tensor24-click")
ed = E.Edges(world, int(lay.click.key[0, 0]), 1, [t["kinds"] for t in universe["trains"]])
st = circ.Stepper(ed)
ga, ab, gb = ed.triangles[0]
y, _ = carry(st.D3 * num, den, 0)
fl = [0] * st.n
fl[ab] = y
gs, ts, es = st.born()
start = (ts[0], es[0])
c, period = [], None
for t in range(1, rounds + 1):
    st.step(fl, gs, ts, es)
    c.append(1 if st.last_w[0] else 0)
    if period is None and (ts[0], es[0]) == start:
        period = t
n1 = sum(c)
n11 = sum(c[t] * c[t - 1] for t in range(1, rounds))
n111 = sum(c[t] * c[t - 1] * c[t - 2] for t in range(2, rounds))
e11, _ = carry(n1 * n1, rounds, 0)
e111, _ = carry(n11 * n1, rounds, 0)
r11, _ = carry(1000 * n11, e11, 0) if e11 else (0, 0)
r111, _ = carry(1000 * n111, e111, 0) if e111 else (0, 0)
print(f"a = {num}/{den}, y = {y} at the dial {st.D3}, {rounds} rounds: {n1} landings; after one the next {n11} against"
      f" {e11} independent ({r11} per mille); after two in a row a third {n111} against {e111} ({r111} per mille);"
      f" the tooth and twin back at their birth first at round {period}")
