"""Probe 1: the vacuum gearing's coefficients, the dispersion, the species' scales, the doubler."""
import math
import sys
from fractions import Fraction as F

sys.path.insert(0, "/tmp/claude-0/-home-user-Universe24/e136d210-1915-523c-8c8e-0abbdf97855b/scratchpad/t24/src")
from event_universe.core import rule3  # noqa: E402

rim = 15162856759112389
gamma = 1000
G = rule3.mesh_unit_of(gamma)
rows = {
    "light": rim,
    "electron(row1)": 15162854575528411,
    "proton(row2)": 2458210083751875,
    "neutron(row3)": 2580388913625285,
    "held field": 15011228191521265,
    "regulator": rim - rim // gamma,
}
print("mesh unit G =", G)
for name, pin in rows.items():
    g = rule3.gearing(pin, rim, gamma, gamma, gamma, None, G)
    w, D, R = g.teeth, g.spring, g.grips[0]
    centre = 2 * w - D - 6 * R  # coefficient of a_now in w a_next = ... (the hold)
    assert centre == g.hold
    c2 = F(R, w)  # Laplacian coefficient
    cos0 = F(2 * w - D, 2 * w)
    print(f"{name:15s} hold(centre coeff)={centre}  R/w={float(c2):.6g} pinion/(3rim)={pin/(3*rim):.6g}  cos w0={float(cos0):.12g} pinion/rim={pin/rim:.12g}")

print("\nspecies scales (vacuum, lattice units: Mesh, tick)")
c_light = 1 / math.sqrt(3)
for name, pin in rows.items():
    c0 = pin / rim
    w0 = math.acos(c0)
    s0 = math.sqrt(1 - c0 * c0)
    if w0 == 0:
        print(f"{name:15s} w0=0 (massless), c^2=1/3")
        continue
    # long-wave limiting speed: w^2 ~ w0^2 + (w0 cot w0 / 3) k^2
    c2 = w0 / math.tan(w0) / 3
    # max group velocity along an axis in the band cos w = c0 * (2 + cos k)/3
    vmax = 0.0
    for i in range(1, 20001):
        k = math.pi * i / 20000
        cw = c0 * (2 + math.cos(k)) / 3
        ww = math.acos(cw)
        vg = c0 * math.sin(k) / (3 * math.sin(ww))
        vmax = max(vmax, vg)
    print(f"{name:15s} w0={w0:.6g} rad/tick beat(pi/w0)={math.pi/w0:.6g} ticks  sin w0={s0:.6g}  "
          f"Compton length c/w0={c_light/w0:.4g} Mesh  limiting speed/c={math.sqrt(c2)/c_light:.4f}  max v_g/c={vmax/c_light:.4f}")

w0e = math.acos(rows["electron(row1)"] / rim)
w0p = math.acos(rows["proton(row2)"] / rim)
w0n = math.acos(rows["neutron(row3)"] / rim)
print("\nratio of sines p/e =", math.sin(w0p) / math.sin(w0e), " n/e =", math.sin(w0n) / math.sin(w0e))
print("ratio of rest beats (frequencies) p/e =", w0p / w0e, " n/e =", w0n / w0e)
print("hbar_eff = winding/w0 ~ sin(w0)/w0: e", math.sin(w0e) / w0e, " p", math.sin(w0p) / w0p)

# Doubler: the vacuum step is a_next + a_before = (pinion/(3 rim)) * sum of six neighbours (centre coefficient 0)
# so the sublattices of x+y+z+t even/odd decouple exactly. Check on an 6^3 torus with exact rationals.
import itertools
n = 6
c = F(1, 3)
def step(now, before):
    nxt = {}
    for x, y, z in itertools.product(range(n), repeat=3):
        s = sum(now[((x + dx) % n, (y + dy) % n, (z + dz) % n)] for dx, dy, dz in
                [(1,0,0),(-1,0,0),(0,1,0),(0,-1,0),(0,0,1),(0,0,-1)])
        nxt[(x, y, z)] = c * s - before[(x, y, z)]
    return nxt
import random
random.seed(1)
now = {p: (F(random.randint(-9, 9)) if (sum(p)) % 2 == 0 else F(0)) for p in itertools.product(range(n), repeat=3)}
before = {p: (F(random.randint(-9, 9)) if (sum(p)) % 2 == 1 else F(0)) for p in itertools.product(range(n), repeat=3)}
other_now = {p: F(0) for p in now}
other_before = {p: F(0) for p in now}
# field on sublattice (x+y+z+t) even only: at t=0 even sites, at t=-1 odd sites
leak = 0
for t in range(1, 30):
    now, before = step(now, before), now
    # at time t the field must vanish where x+y+z+t is odd
    leak += sum(1 for p, v in now.items() if (sum(p) + t) % 2 == 1 and v != 0)
print("\nsublattice leak over 29 ticks (must be 0 if decoupled):", leak)
# doubler symmetry: the checkerboard sign (-1)^(x+y+z+t) maps solutions to solutions with the same wind form
