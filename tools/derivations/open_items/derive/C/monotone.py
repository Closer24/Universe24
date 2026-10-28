"""Draft C, theorem C2's probe (random property test on the head's own acts, integers only): on a board alike at every
Node-clock the regulator's time gear steps by Rule3's turn at its gearing (the grips' sum cancels: every neighbour alike)
and then by its drive carry, clock.act's two acts. Claim: with the spring D = 0 and every drive numerator N >= 0, the
first difference never falls, X+ - X >= X - X-, so after a rise no weak maximum (law 4's top) can come. The probe draws
random states (X, X-, r in [0, w), r_d in [0, T_d)) at the bang's calibre and checks the claim on the head's acts.carry,
then shows the claim FAILS as soon as either premise goes: a spring D > 0 (the regulator's typed pair) or N < 0.
Usage: python -I monotone.py ROOT DRAWS"""
import random
import sys

root, draws = sys.argv[1], int(sys.argv[2])
sys.path[:0] = [root + "/src", root]
from event_universe.core.acts import carry  # noqa: E402
from event_universe.core.rule3 import held_teeth, spring as spring_of, teeth_of, mesh_unit_of  # noqa: E402

rim, gamma, key, trace = 15162856759112389, 1000, 36000, 6
G = mesh_unit_of(gamma)
w = teeth_of(rim, gamma, G)
td = held_teeth(trace, rim, gamma, key, 4)
pinion_regulator = rim - rim // gamma
rng = random.Random(24)


def step(x, x_before, r, rd, n, spring):
    """The head's regulator act on the time gear at a uniform board: the turn (hold 2 w - D - SUM R_j, grips' SUM cancels)
    then the drive, both by acts.carry; returns (X+, r', rd')."""
    total = (w + w - spring) * x - w * x_before
    x_next, r_next = carry(total, w, r, 1)
    q, rd_next = carry(n, td, rd, 1)
    return x_next + q, r_next, rd_next


counts = {"D = 0, N >= 0: X+ - X >= X - X-": [0, 0], "D > 0 (the regulator's pair), N = 0": [0, 0], "D = 0, N of either sign": [0, 0]}
for _ in range(draws):
    x = rng.randrange(1, 10**10)
    x_before = x - rng.randrange(-10**6, 10**6)
    r, rd = rng.randrange(w), rng.randrange(td)
    p0 = rng.randrange(1, gamma + 1)
    n_pos = rng.randrange(0, 10**6) * rng.randrange(0, td)
    n_any = rng.randrange(-10**6, 10**6) * rng.randrange(0, td)
    d_reg = spring_of(pinion_regulator, rim, p0, G)
    for name, (spring, n) in (
        ("D = 0, N >= 0: X+ - X >= X - X-", (0, n_pos)),
        ("D > 0 (the regulator's pair), N = 0", (d_reg, 0)),
        ("D = 0, N of either sign", (0, n_any)),
    ):
        x_next, _r, _rd = step(x, x_before, r, rd, n, spring)
        counts[name][0] += int(x_next - x >= x - x_before)
        counts[name][1] += 1
for name, (held, total) in counts.items():
    print(f"{name}: the first difference held in {held} of {total} draws")
