"""STEADY1 probe: each row's stiffness from J's potential, d2V/dx2 at the now slot (SUM over the live monomials holding
the row twice of 2 f PROD other legs), against the act's window 4 W (the leapfrog's: a+ - 2a + b = push / W, so a
row with stiffness kappa is stable iff kappa < 4 W, the docstring's 0 < 2 spring < 4 W); per round the largest
kappa over 4 W in permille (carry), for the held train's rows and the other rows, along the engine's own act.
Usage: python -I window.py <universe> <piece> <setting> [<rounds to read>]"""
import json, sys
from pathlib import Path
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.joinpath("wt", "src")))
sys.set_int_max_str_digits(0)
import numpy as np
from tensor24 import main as tmain
from tensor24.algebra.carry import carry
from tensor24.engine import step
from tensor24.engine.state import State
from tensor24.runner import load as loadmod, plans
from tensor24.runner.files import sites_of, star

paths = [Path(p) for p in sys.argv[1:4]]
universe, piece, setting = (json.loads(p.read_text(encoding="utf-8")) for p in paths)
shape = piece["shape"]
kinds, c, square = tmain.made(star(len(shape)))
loaded, _ = loadmod.load(universe, setting, sites_of(shape), kinds, c, square)
layout = tmain.layout(universe, shape, loaded)
s = State(*loaded.state)
factor, legs = loaded.potential
legs = np.stack(legs, axis=1).astype(np.intp)
_, of, _, _, _ = plans.rows_of(loaded.trains)
held_t = int(np.argmax(np.asarray(loaded.trains.held, dtype=np.int64)))
rows = len(of)
terms = []  # (row, factor, the other two legs) for every live monomial holding the row twice
for m in range(len(factor)):
    f = int(factor[m])
    if f == 0:
        continue
    lg = [int(x) for x in legs[m]]
    for r in set(x for x in lg if x >= 0):
        if lg.count(r) == 2:
            rest = list(lg); rest.remove(r); rest.remove(r)
            terms.append((r, f, rest))
def kappa(a):
    v = step.valued(a)
    k = 0 * a
    for r, f, rest in terms:
        k[r] = k[r] + 2 * f * v[rest[0]] * v[rest[1]]
    return k
def worst(s):
    wa, _ = step.dials(layout, s)
    ratio, _ = carry(1000 * kappa(s.a), 4 * wa, 0)
    h = max(int(x) for r in range(rows) if of[r] == held_t for x in ratio[r])
    o = max([int(x) for r in range(rows) if of[r] != held_t for x in ratio[r]] or [0])
    return h, o
n = int(sys.argv[4]) if len(sys.argv) > 4 else setting["ticks"]
h, o = worst(s)
print(f"at the lay: the held rows' largest stiffness {h} permille of 4 W, the other rows' {o}")
out, top = [], (h, 0)
for at in range(1, n + 1):
    s, _ = step.act(layout, s)
    h, o = worst(s)
    top = max(top, (h, at))
    wide = max(int(abs(int(x))).bit_length() for x in s.a.ravel())
    if at % 50 == 0 or wide > 128 or at in (1, 2, 3, 4, 5, 6, 7, 8):
        print(f"round {at}: held {h}, other {o} permille of 4 W; widest now count {wide} bits")
    if wide > 128:
        break
print(f"the held rows' largest over the run read: {top[0]} permille at round {top[1]}")
