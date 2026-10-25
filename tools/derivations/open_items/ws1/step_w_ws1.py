"""ws1: the step's part named on cl1's single body (single_d3, the 15-cube at universe_middle): the first intervals, where no Node turns
and no click lands (the wlog's turned 0, births 0, credits 0 at 1 and 2), the board's W of the plane with a gap read plain (SUM W_i) and
weighted by the law's weight 1 / p_i^2 (The sign is the rotation sense: the weighted total exactly invariant in the rationals at fixed
paces; the plain total drifts where the paces differ), the weighted sum an exact rational given as numerator and denominator (integers),
with the paces' spread (min, max of the Link pace over the board and over the packet's Nodes) and the turn's size (the sign level's
extreme, 0 at the first interval: the arrivals unturned). Also the count of Nodes whose W changed in the step. Integers only.
Usage: PYTHONPATH=src_ws1 python step_w_ws1.py <world.json> <intervals>"""
import sys
from fractions import Fraction

import numpy as np

sys.set_int_max_str_digits(0)
from event_universe import node as node_module
from event_universe import readings, seed
from event_universe.links import wronskian
from event_universe.loader.world import load_world
from event_universe.node import Node
from event_universe.rows import POTENTIAL

import lay_ws1

seed.lay_world = lay_ws1.lay_world
node_module.seed.lay_world = lay_ws1.lay_world
universe, world = load_world(sys.argv[1])
n = int(sys.argv[2])
node = Node(universe, world)


def readout():
    gap = node.gapped_indices()
    total = None
    for k in gap:
        ww = wronskian(*node.rows()[k])
        total = ww if total is None else total + ww
    content = node.content()
    _clock, pace = readings.paces_of(node, content)
    ws = [int(x) for x in total.reshape(-1)]
    ps = [int(x) for x in np.asarray(pace, dtype=object).reshape(-1)]
    plain = sum(ws)
    weighted = sum(Fraction(w, p * p) for w, p in zip(ws, ps) if p)
    packet = [p for w, p in zip(ws, ps) if w != 0]
    phi = node.row(POTENTIAL).lines[0].now
    return plain, weighted, (min(ps), max(ps)), (min(packet), max(packet)) if packet else None, max(abs(int(x)) for x in phi.reshape(-1)), ws


p0, q0, s0, k0, phi0, ws0 = readout()
print("interval 0: W plain", p0, "weighted num/den", q0.numerator, q0.denominator, "paces board", s0, "paces where W != 0", k0, "sign level max", phi0)
for t in range(n):
    node.step()
    p1, q1, s1, k1, phi1, ws1 = readout()
    changed = sum(1 for a, b in zip(ws0, ws1) if a != b)
    nz = sum(1 for b in ws1 if b != 0)
    print("interval", node.interval, ": W plain", p1, "change", p1 - p0, "| weighted num/den", q1.numerator, q1.denominator, "| weighted change num/den", (q1 - q0).numerator, (q1 - q0).denominator,
          "| paces board", s1, "paces where W != 0", k1, "| sign level max", phi1, "| turned", int(node.turned.sum()), "births", node.counts["births"], "credits", node.counts["body_clicks"],
          "| Nodes whose W changed", changed, "Nodes with W != 0", nz)
    p0, q0, ws0 = p1, q1, ws1
