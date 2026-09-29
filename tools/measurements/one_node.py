"""ONE NODE WITH NUMBERS: the chain body of Gamma 6000 laid by the pixel tool; at its centre Node and at a shell Node, before each interval the Node's inputs are copied (the two levels, the remainder, the six arrivals, the content, the count and its remainder, the currents), and the engine's writes are recomputed by hand from the law's line alone: w a_next + r' = R (arr+ + arr-) + S a_now - w a_before + r with (R, S, w) from the paces, and W_c c_next + r' = W_c c_now + SUM F + r."""

import json
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, ".")
sys.path.insert(0, "src")
import event_universe.world_files as wf
from event_universe.events.detector_law import DetectorLawSimulation
from event_universe.world_files import load_world
from tests.laws import chain_body_world, load_file

TOOL = load_file("pixel_mode", Path("tools/pixel_mode.py"))
d = Path(tempfile.mkdtemp())
wf.REPOSITORY_ROOT = d
world = chain_body_world(d, TOOL)
doc = json.loads(world.read_text())
nodes = sorted(n["node"][0] for n in doc["measured"][0]["nodes"])
sim = DetectorLawSimulation(load_world(world))
block = sim.blocks[0]
live = block.own
G, (num, den), T = sim.node_clock, block.definition.pair, sim.world.quantum_action
sim.step()  # the lay
Wc = sim.count_wall(block)
weight = sim.kind_wall(block.family, block.definition.pair)
print(
    f"Gamma {G}, pair [{num}, {den}], T {T}, W_c = 3 den T = {Wc}, the current's weight {weight}; the body's Nodes x = {nodes[0]}..{nodes[-1]} ({len(nodes)} Nodes)"
)
centre, shell = (nodes[len(nodes) // 2], 0, 0), (nodes[0], 0, 0)
checks = mismatches = 0
for t in range(2, 14):
    snap = {}
    for name, node in (("centre", centre), ("shell", shell)):
        x = node[0]
        c = int(sim._effective_content(block.family)[node])
        now, before, rem = int(live.now[node]), int(live.before[node]), int(live.remainder[node])
        arr = int(live.now[x - 1, 0, 0]) + int(
            live.now[x + 1, 0, 0]
        )  # the x axis on the chain; y and z wrap on one Node: the Node itself twice
        arr_self = 2 * now
        count, crem = int(block.counts[node]), int(block.count_remainder[node])
        snap[name] = (c, now, before, rem, arr, arr_self, count, crem)
    sim.step()
    for name, node in (("centre", centre), ("shell", shell)):
        c, now, before, rem, arr, arr_self, count, crem = snap[name]
        x = node[
            0
        ]  # THE COUNT'S LINE READS THE LEVELS AFTER THE STEP (its place (ii) after (i)): the currents from now' and before' = now
        n_i, b_i = int(live.now[node]), int(live.before[node])
        flux = sum(
            weight * (n_i * int(live.before[j, 0, 0]) - b_i * int(live.now[j, 0, 0]))
            for j in (x - 1, x + 1)
        )
        (R, _, _), S, w = sim.families and __import__(
            "event_universe.core.rule3", fromlist=["coefficients"]
        ).coefficients(num, den, G, c)
        total = R * arr + R * arr_self + R * arr_self + S * now - w * before + rem
        a_next, r_next = total // w, total % w
        count_total = Wc * count + flux + crem
        c_next, cr_next = count_total // Wc, count_total % Wc
        got = (
            int(live.now[node]),
            int(live.remainder[node]),
            int(block.counts[node]),
            int(block.count_remainder[node]),
        )
        ok = got == (a_next, r_next, c_next, cr_next)
        checks += 1
        mismatches += not ok
        if t <= 4 or not ok:
            print(
                f"t={t:2d} {name:6s} in: c={c} now={now} before={before} r={rem} arr={arr} count={count} r_c={crem} flux={flux} | (R,S,w)=({R},{S},{w}) | hand: a'={a_next} r'={r_next} c'={c_next} r_c'={cr_next} | engine: {got} {'OK' if ok else 'MISMATCH'}"
            )
print(f"{checks} checks, {mismatches} mismatches")
