"""The one-Node test of EX-S1 (hand ex2): the 3-cube world (worlds/world_node.json) stepped 3 intervals, then one Node fed
40 drifts of the gap-0 line (the seed's `at` form, one lay act) and taken 20 times of 2 x unit_gap0 (a birth's walls)
through the engine's take_at with the flag on. Read per take: the default's excess (fall_of at carry 0 on the same state,
the control), the carry before, the levels, the fall, the remainder after, the identity taken + rem_before == booked +
rem_after, and rem_after < the level's step at the levels taken. Then the run back through the engine's own path: 20
intervals forward from the seed with the flag on, 20 back, the hashes compared (births on the 3-cube included).
Predictions (written before the run): identity exact 20 of 20; rem_after < step 20 of 20; the default's excess > 0 on
every take with levels >= 1 (the departure the brief names); sum fall = 20 walls + rem_20; at least one take with fewer
levels than the default's would take (the repayment); run back 20 of 20; the state's count 98 + 4 arrays at the 3-cube.
Usage: EX2_CARRY=1 PYTHONPATH=engine python one_node.py"""
import json, os, sys
from pathlib import Path

import numpy as np

sys.set_int_max_str_digits(0)
assert os.environ.get("EX2_CARRY") == "1", "run with EX2_CARRY=1"
from event_universe import readings, take
from event_universe.core import paces
from event_universe.core.rule3 import quotient
from event_universe.loader.world import load_world
from event_universe.node import Node
from event_universe.rows import PLANE

HERE = Path(__file__).resolve().parent
universe, world = load_world(str(HERE / "worlds" / "world_node.json"))
node = Node(universe, world)
for _ in range(3):
    node.step()
gap0 = node.row(PLANE, gap=0)
rec0 = node.records().index(gap0)
z = gap0.lines[0]
at = (1, 1, 1)
node.lay(rec0, at, (40 * node.drift, 0, 0, 0))  # the fed quantum: 40 drifts at one Node, the seed's `at` form
c = node.start_content
frozen = readings.frozen_of(node, c)
factors = node.link_factors(None, frozen)
r = node.rule_of(gap0, c, factors)
walls = 2 * node.unit_gap0
print(json.dumps({"den": node.den, "T": node.T, "unit_gap0": node.unit_gap0, "walls": walls, "drift": node.drift,
                  "now, before at the Node after the feed": [int(z.now[at]), int(z.before[at])],
                  "integers, bits (census)": list(node.census())}))


def fall_at(s: int) -> int:
    """The share's fall at s levels toward before, fall_of's own quadratic (the control's copy for the step)."""
    now, before = int(z.now[at]), int(z.before[at])
    t = 1 if before > now else -1
    own, w = int(np.asarray(r.self_coefficient)[at]), int(r.wall)
    reached = sum(int(np.asarray(reach)[at]) * int(z.before[take.neighbour(node, at, port)]) for port, reach in enumerate(r.reaches))
    pace = int(np.asarray(paces.link_pace_of(node.gamma, node.start_content), dtype=object)[at])
    weight = 2 * pace * pace * node.G * node.G + (1 if pace == 0 else 0)
    return int(quotient(w * (now * now - (now + t * s) ** 2) - t * s * (own * before + reached), weight))


rows = []
exact = within = positive_default = fewer = 0
sum_fall = 0
for k in range(20):
    carry = int(node.taken_rem[rec0][at])
    d_levels, d_fall = take.fall_of(node, at, walls, r, z, 0)  # the default's take on the same state (the control)
    got = take.take_at(node, at, walls, r, 1)
    if got is None:
        rows.append({"take": k + 1, "refused": "stop", "carry": carry, "default": [d_levels, d_fall]})
        continue
    levels, fall, now, before = got
    rem = int(node.taken_rem[rec0][at])
    step = (fall_at(levels) - fall_at(levels - 1)) if levels >= 1 else None
    # fall_at reads the state after the lay; the step at the taken level on the state before: recompute on the levels of the take
    identity = fall + carry == walls + rem
    exact += identity
    within += (step is None) or (rem < step)
    positive_default += (d_fall is not None and d_fall - walls > 0)
    fewer += (d_levels is not None and levels < d_levels)
    sum_fall += fall
    rows.append({"take": k + 1, "default excess (fall - walls) at carry 0": (None if d_fall is None else d_fall - walls),
                 "default levels": d_levels, "carry before": carry, "levels": levels, "fall": fall, "rem after": rem,
                 "identity": identity, "step at the levels (control's quadratic, after the lay)": step, "now was": now})
for row in rows:
    print(json.dumps(row))
rem_end = int(node.taken_rem[rec0][at])
print(json.dumps({"identity exact of 20": exact, "rem < step of 20": within, "default excess > 0 of 20": positive_default,
                  "takes with fewer levels than the default's": fewer,
                  "sum fall == 20 walls + rem_20": sum_fall == 20 * walls + rem_end, "sum fall": sum_fall, "rem_20": rem_end,
                  "rem_20 bits": rem_end.bit_length(), "integers, bits (census)": list(node.census())}))

# the run back through the engine's own path, from the seed, 20 intervals
node2 = Node(universe, world)
hashes = []
for _ in range(20):
    hashes.append(node2.state_hash())
    node2.step()
held = sum(int(x) for a in node2.taken_rem for x in a.reshape(-1))
back = 0
for k in range(20):
    node2.step_back()
    back += node2.state_hash() == hashes[19 - k]
print(json.dumps({"run back (engine path, 3-cube, 20 intervals, flag on)": [back, 20], "births": node2.counts["births"],
                  "remainder held at the end of the forward run (share units)": held,
                  "remainder held after the run back (0 expected)": sum(int(x) for a in node2.taken_rem for x in a.reshape(-1)),
                  "counts": {k: v for k, v in node2.counts.items() if k in ("taken_all", "booked_all", "take_rem_held", "takes_from_carry", "refused_stop")}}))
