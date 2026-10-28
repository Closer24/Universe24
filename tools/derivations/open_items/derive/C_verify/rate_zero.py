"""Verifier's probe for claim 4 (integers only): the rate chain's zero at Gamma 1000 read from the head's own
core/rates.py and features/stretch: the stopped load, its rate and mesh rate, the stretch X_c of that load, and the
load reading on both sides of X_c. Also the condition 2 p0^2 < Gamma at the stop, and the floor X_f.
Usage: python -I rate_zero.py ROOT"""
import sys
root = sys.argv[1]
sys.path[:0] = [root + "/src"]
import numpy as np
from event_universe.core import rates
from event_universe.features import stretch

G = 1000
c = rates.stopped_load(G)
p, pm = rates.rate(G, c), rates.mesh_rate(G, c)
pb, pmb = rates.rate(G, c - 1), rates.mesh_rate(G, c - 1)
print("stopped load", c, "rate", p, "mesh rate", pm, "| load", c - 1, "rate", pb, "mesh rate", pmb)
print("2 p0^2 < Gamma at the stop:", 2 * p * p < G, "| at the load before:", 2 * pb * pb < G)
Xc = int(stretch.stretch_of(G, np.array([c], dtype=object))[0])
print("X_c = stretch_of(stopped load) =", Xc, "| ceil(G^5 / p^4) =", -(-G**5 // p**4), "| 4 G^3 =", 4 * G**3)
for x in (Xc - 1, Xc, Xc + 1):
    a = int(stretch.load_of(G, np.array([x], dtype=object))[0])
    print(f"  load_of({x}) = {a}, mesh rate there {rates.mesh_rate(G, a)}")
# every load below the stop has a mesh rate > 0 (the chain's first zero)
print("first zero of the mesh rate is the stopped load:", all(rates.mesh_rate(G, k) > 0 for k in range(c)))
xf = int(stretch.stretch_of(G, np.array([-G], dtype=object))[0])
print("floor X_f =", xf, "a_c^2 = (G/p)^2 =", (G * G) / (p * p), "2 Gamma =", 2 * G)
