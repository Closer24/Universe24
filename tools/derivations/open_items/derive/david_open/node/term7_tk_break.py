"""Term 7's third text, 2.5's reduction at s T_k above 1, with cases built to break it (David), on node-live's act at
f72067cdf. The lay and the acts are the mathematician's t7_tk (his second reading); each hypothesis is broken in turn.
Whole numbers alone, every division the tensor24 carry: no float, root, search or circular function.

Drive act A: teeth W, grips g, stretch s, kick T_k, drive T_d, edge tooth s T_k e1 + c.
Reduced act R: teeth W / (s T_k), grips g / T_k, stretch 1, kick 1, drive T_d, edge tooth e1 (the same counts and r_d).
The reduction holds when s T_k divides W, T_k divides the grips and c lies within [-s T_k rho1, s T_k (4 - rho1) - 1],
rho1 = (e1 + 2 W1) mod 4; the lay here is at rho1 = 0, so the window is 0 to 4 s T_k - 1.

Usage: python3 -I term7_tk_break.py <src of node-live at f72067cdf> (about 65 s)
"""

import sys

import numpy as np

sys.path.insert(0, sys.argv[1])
from tensor24.algebra.carry import carry  # noqa: E402
from tensor24.engine import step  # noqa: E402
from tensor24.engine.contract import pushes  # noqa: E402
from tensor24.engine.state import Click, Gearing, Layout, Plan, Read, State  # noqa: E402
from tensor24.runner.board import board  # noqa: E402
from tensor24.runner.load import geometry  # noqa: E402

NONE_I = np.zeros(0, dtype=np.intp)
NONE_O = np.zeros(0, dtype=object)
UNREAD = Read(NONE_I, NONE_O, NONE_I)
NOPLAN = Plan(NONE_I, NONE_I, NONE_I, NONE_O, NONE_I)
UNIT = -1


def generator(seed):
    state = seed

    def pick(span):
        nonlocal state
        _, state = carry(1103515245 * state + 12345, 2147483648, 0)
        return carry(state, 2 * span + 1, 0)[1] - span

    return pick


def make(w, g, s, tk, td, spring):
    nb = board((3, 3, 3))
    sites = nb.shape[1]
    spokes, meshes = geometry(nb, 3)
    one = np.ones((1, 1), dtype=object)
    gearing = Gearing(w * one, s * one, tk * one, td * one, one.copy())
    click = Click(NONE_I, NONE_I, NONE_O, NONE_I, np.ones((1, 1), dtype=object))
    plan = pushes(np.array([spring], dtype=object), tuple(np.array([x], dtype=np.intp) for x in (0, 0, UNIT, UNIT)))
    grip = np.full((1, 3 * sites), g, dtype=object)
    return Layout(nb, spokes, meshes, grip, gearing, plan, UNREAD, UNREAD, click, NOPLAN, NOPLAN), sites


def compare(label, w, g, s, tk, td, spring, rounds, seed, g_off=0, e_off=0):
    """A at (w, g + g_off, s, tk, td) with the edge tooth s T_k e1 + e_off, against R at (w / (s tk), g / tk, 1, 1, td)
    with the edge tooth e1; w1 = carry(w, s tk) when s tk does not divide w."""
    st = s * tk
    la, sites = make(w, g + g_off, s, tk, td, spring)
    w1, _ = carry(w, st, 0)
    g1, _ = carry(g, tk, 0)
    lr, _ = make(w1, g1, 1, 1, td, spring)
    pick = generator(seed)
    a = np.array([[pick(3000) for _ in range(sites)]], dtype=object)
    b = np.array([[a[0, i] - pick(100) for i in range(sites)]], dtype=object)
    e1 = np.array([[4 * carry(pick(10**6), w1, 0)[1] - 2 * w1 for _ in range(sites)]], dtype=object)
    rd = np.array([[carry(pick(10**6), td, 0)[1] for _ in range(sites)]], dtype=object)
    k = np.zeros((1, sites), dtype=object)
    sa = State(a, b, st * e1 + e_off, rd, k)
    sr = State(a.copy(), b.copy(), e1.copy(), rd.copy(), k.copy())
    dr = 0
    first_r = None
    for n in range(rounds):
        sa, sr = step.tick(la, sa), step.tick(lr, sr)
        if bool((sa.a != sr.a).any()):
            dr += 1
            first_r = n + 1 if first_r is None else first_r
    print(f"  {label}: the counts of A and R differ in {dr} of {rounds} rounds (first {first_r})", flush=True)


print("2.5's reduction with one hypothesis broken at a time (the first line keeps them all, as t7_tk's first case):")
compare("all kept: W 6000, grips 300, s 2, T_k 3, T_d 7, spring 73", 6000, 300, 2, 3, 7, 73, 5000, 151)
compare("T_k not dividing the grips: grips 301 in A, 100 in R", 6000, 300, 2, 3, 7, 73, 5000, 151, g_off=1)
compare("the edge tooth s T_k e1 + 1 in A", 6000, 300, 2, 3, 7, 73, 5000, 151, e_off=1)
compare("the edge tooth s T_k e1 + 2 in A", 6000, 300, 2, 3, 7, 73, 5000, 151, e_off=2)
compare("s T_k not dividing W: W 6004 in A, 1000 in R", 6004, 300, 2, 3, 7, 73, 5000, 151)
print("The edge tooth's offset c in A, s T_k e1 + c, at the residue 0 (e1 + 2 W1 a multiple of 4): the window"
      " 0 <= c <= 4 s T_k - 1 = 23 by 2.5's argument, and one step beyond each end:")
for c in (23, 24, -1):
    for seed in (151, 152, 153):
        compare(f"c = {c}, seed {seed}", 6000, 300, 2, 3, 7, 73, 5000, seed, e_off=c)
