"""STEADY1 probe: the board's own energy along a run of the engine's own act (no passing change), whole numbers:
4E = SUM_g D_g (a_g - b_g)^2 + 2 (V(a) + V(b)), D = W(a) + W(b) the edge's dial, V = SUM over J's potential's
monomials of f PROD legs (J_i = -dV/dx_i, the plan's own convention); and the edge books' passings, summed over the
run by edge (the edge form's P), against one key. Usage: python -I energy.py <universe> <piece> <setting>"""
import json, sys
from pathlib import Path
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.joinpath("wt", "src")))
sys.set_int_max_str_digits(0)
import numpy as np
from tensor24 import main as tmain
from tensor24.engine import step
from tensor24.engine.state import State
from tensor24.runner import load as loadmod
from tensor24.runner.files import sites_of, star

paths = [Path(p) for p in sys.argv[1:4]]
universe, piece, setting = (json.loads(p.read_text(encoding="utf-8")) for p in paths)
shape = piece["shape"]
kinds, c, square = tmain.made(star(len(shape)))
loaded, found = loadmod.load(universe, setting, sites_of(shape), kinds, c, square)
layout = tmain.layout(universe, shape, loaded)
s = State(*loaded.state)
factor, legs = loaded.potential
legs = np.stack(legs, axis=1).astype(np.intp)
live = [m for m in range(len(factor)) if int(factor[m]) != 0]
f, L = np.asarray(factor, dtype=object)[live][:, None], legs[live]

def V(x):
    v = step.valued(x)[L]  # (M, 4, S)
    return (f * v[:, 0] * v[:, 1] * v[:, 2] * v[:, 3]).sum()

def E4(s):
    a, b = s.a, s.b
    wa, wb = step.dials(layout, s)
    return int(((wa + wb) * (a - b) * (a - b)).sum() + 2 * (V(a) + V(b)))

ticks = setting["ticks"]
width = universe["integers"]["width"]
e0 = E4(s)
print("4E at the lay:", e0, "| width", width, "| ticks", ticks)
for at in range(1, ticks + 1):
    s, _ = step.act(layout, s)
    wide = max(int(abs(int(x))).bit_length() for x in np.concatenate((s.a.ravel(), s.b.ravel())))
    if at % 50 == 0 or wide > width or at <= 2:
        e = E4(s)
        print(f"round {at}: 4E {e if len(str(e)) < 40 else str(e)[:12] + '...(' + str(len(str(abs(e)))) + ' digits)'}, 4E - 4E0 {e - e0 if len(str(e - e0)) < 40 else '(' + str(len(str(abs(e - e0)))) + ' digits)'}, widest count {wide} bits")
    if wide > width:
        print(f"first count past the width after round {at}")
        break
