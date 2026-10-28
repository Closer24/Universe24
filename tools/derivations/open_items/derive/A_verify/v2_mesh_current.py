"""V2 (verifier A): the step's current across each Mesh, and where it fails to be antisymmetric.

At each tick's carry, for each coupled hand, the engine's own turned neighbour m_j(x) (clock.offset_pull with
the hand's meshes as tick.pulls builds them) gives the weighted current out of x through spoke j:
    A_j(x) = eps(x) S_j(x) Im(conj(a(x)) m_j(x)),   S_j = grip_j / mr(x)^2 (symmetric between the ends)
The step's own change of Q* is minus SUM_x SUM_j A_j(x) (plus the carry's rounding), so a conserved current needs
    T_j(x) = A_j(x) + A_-j(x + e_j) = 0  at every Mesh.
Each Mesh is classed by its pawl sign f (the neighbour read conjugated where f = -1) and by whether its
tangent-triple turn (the odd gear and the skew) is the identity. Units: vacuum sweep units (X = mr = Gamma).
argv: world file, ticks.
"""
import sys
from collections import defaultdict
from fractions import Fraction
from pathlib import Path

S = '/tmp/claude-0/-home-user-Universe24/e136d210-1915-523c-8c8e-0abbdf97855b/scratchpad'
sys.path[:0] = [S + '/t24/src']
import numpy as np  # noqa: E402
from event_universe.assembly.piece import read_piece  # noqa: E402
from event_universe.clock import Clock  # noqa: E402
from event_universe import tick as T, readings  # noqa: E402
from event_universe.core.spokes import SPOKES, SPOKE_SIDES, across, spoke_of  # noqa: E402
from event_universe.meshes import coupling_of, skewed  # noqa: E402
from event_universe.regulation import rest_rate_of  # noqa: E402

world, ticks = sys.argv[1], int(sys.argv[2])
calibre, piece = read_piece(Path(S + '/t24/tests/worlds/' + world))
clock = Clock(calibre, piece)
G = clock.full_rate
coupled = [k for k, h in enumerate(clock.hands()) if coupling_of(h) == 1]
w_ref = int(clock.teeth) * G
cls = defaultdict(lambda: [0, Fraction(0), Fraction(0)])   # count, SUM |T|, max |T|
orig_carry = T.Tick.carry


def carry(self):
    clk = self.clock
    eps = 1 - 2 * np.asarray(self.ratchet.gears[0].fine, dtype=object)
    X = np.asarray(self.stretch_now, dtype=object)
    mr = np.asarray(self.mesh_rate, dtype=object) * np.ones(clk.size, dtype=object)
    for k in coupled:
        r = clk.hands()[k]
        t = self.where[id(r)]
        a = self.starts[t]
        gearing = readings.gearing_of(clk, r, self.load, self.factors)
        rotation = coupling_of(r) * rest_rate_of(clk, r.ratio)
        turn = skewed(self.meshes_at[coupling_of(r)], rotation, self.flow_gears, clk.full_rate)
        Aj = []
        for j in range(SPOKES):
            m = clk.offset_pull([across(x, j) for x in a], j, turn)
            im = a[0] * m[1] - a[1] * m[0]
            Aj.append(eps * gearing.grips[j] * im)   # still to be divided by mr(x)^2 X... (S_j = grip/mr^2)
        for j in range(SPOKES):
            axis, side = SPOKE_SIDES[j]
            if side != 1:
                continue
            jo = spoke_of(axis, 1)
            far = across(Aj[jo], j)
            far_mr = across(mr, j)
            for x in np.ndindex(clk.size):
                lam_x = Fraction(G ** 2, int(mr[x]) ** 2) if int(mr[x]) else Fraction(0)
                lam_y = Fraction(G ** 2, int(far_mr[x]) ** 2) if int(far_mr[x]) else Fraction(0)
                tval = (Fraction(int(Aj[j][x])) * lam_x + Fraction(int(far[x])) * lam_y) / w_ref * Fraction(G, 1)
                # tval in vacuum sweep units per tick: X Im(...) / w with X = G at the vacuum
                f = int(turn[j].pawl[x]) if np.ndim(turn[j].pawl) else int(turn[j].pawl)
                odd = turn[j].odd[x] if np.ndim(turn[j].odd) else turn[j].odd
                sk = turn[j].skew[1]
                sk = sk[x] if np.ndim(sk) else sk
                ident = int(odd) == 0 and int(sk) == 0
                key = (k, 'pawl wall' if f < 0 else 'one frame', 'identity triple' if ident else 'odd/skew turn')
                c = cls[key]
                c[0] += 1
                c[1] += abs(tval)
                c[2] = max(c[2], abs(tval))
    orig_carry(self)


T.Tick.carry = carry
for _ in range(ticks):
    clock.tick()
print(f"{world}, {ticks} ticks: the weighted Mesh current's failure of antisymmetry |T| per Mesh-tick (vacuum sweep units)")
for key in sorted(cls):
    n, s, m = cls[key]
    print(f"  hand {key[0]}, {key[1]:9s}, {key[2]:15s}: {n:6d} Mesh-ticks, SUM |T| {float(s):12.1f}, max |T| {float(m):10.1f}")
