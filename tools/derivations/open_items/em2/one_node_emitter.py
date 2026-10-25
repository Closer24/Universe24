"""em2's one-Node emitter test (section 2 of the report): a 5-cube with no sea, one record of ONE sense (a charged body, W above 0) laid at rest over the raised cosine of half-width 2 at the centre on the heavy row (row 2 of universe_toy.json, g 84 hundredths), the carrier held by hand at the content c at every Node (the emitter fed at a content; c = 0 the vacuum); N intervals forward, then 10 back. Read, integers only: the planes' Wronskian at the centre per interval (its breathing), the body's beat at the centre (the intervals between upward zero crossings of its re line), the light laid (the engine's count), the massless re line's level at the centre and at the far Node two Links along +z per interval, the far Node's period (its upward crossings), the max bits and the census, the run back. Under EM2_EMISSION=quantum the flagged copy lays EM-S1's form; absent, the default. Usage: PYTHONPATH=<src or src_em2> python one_node_emitter.py <content> <intervals> <quanta> <out.json>"""
import json
import os
import sys

sys.set_int_max_str_digits(0)
import numpy as np

from event_universe import seed
from event_universe.features import volume
from event_universe.links import wronskian
from event_universe.loader.world import load_world
from event_universe.node import Node
from event_universe.rows import CARRIER, PLANE

HERE = os.path.dirname(os.path.abspath(__file__))
content, n_int, quanta, out_path = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]), sys.argv[4]
universe, world = load_world(os.path.join(HERE, "worlds", "world_hole.json"))
world = {"universe": world["universe"], "shape": [5, 5, 5], "intervals": n_int, "seed": []}


class Held(Node):
    """The engine's Node with the carrier held by hand at one content (the toy's `well` control, `held`): the carrier's act returns its lines unchanged."""

    def carried(self, lines, r, numerators, direction, top, kept):
        return lines


node = Held(universe, world)
m = node.row(CARRIER).lines[0]
level = int(np.asarray(volume.volume_of(node.gamma, np.array([content], dtype=object)), dtype=object).reshape(-1)[0])
m.now[...] = level
m.before[...] = level
node.ride_walls()
centre, far = (2, 2, 2), (2, 2, 4)
rec = 2  # the heavy row: records() order is the file's gapped planes first; row index 2 of the file is the third gapped... use by_index
row = node.by_index[2]
rec = node.records().index(row)
envelope, w0 = seed.envelope_of(node, centre, 2)
node.start_content = node.content()
amplitude = seed.fitted(node, row, envelope, w0, quanta * node.units[rec])
re, im = seed.rest_record(node, row, envelope, w0, amplitude, 1)  # ONE sense: a charged body
node.lay(rec, Ellipsis, (re.now, re.before, im.now, im.before))
# em2: the rows are replaced by set_rows at every step, so every line is read afresh from its row below

series = []
hashes = []
for t in range(n_int):
    if t >= n_int - 10:
        hashes.append(node.state_hash())
    w_c = int(wronskian(*row.lines)[centre])
    series.append({"i": node.interval, "W_centre": w_c, "re_centre": int(row.lines[0].now[centre]), "light_centre": int(node.row(PLANE, gap=0).lines[0].now[centre]), "light_far": int(node.row(PLANE, gap=0).lines[0].now[far]), "light_neighbour": int(node.row(PLANE, gap=0).lines[0].now[(2, 2, 3)]), "laid": node.counts["laid"]})
    node.step()
exact = 0
for k in range(len(hashes)):
    node.step_back()
    exact += node.state_hash() == hashes[len(hashes) - 1 - k]


def crossings(values):
    """The intervals of the upward zero crossings of a series and the spacings between them."""
    ups = [k for k in range(1, len(values)) if values[k - 1] < 0 <= values[k]]
    return ups, [b - a for a, b in zip(ups, ups[1:])]


ups_body, beats = crossings([s["re_centre"] for s in series])
ups_far, far_periods = crossings([s["light_far"] for s in series])
ups_c, c_periods = crossings([s["light_centre"] for s in series])
ws = [s["W_centre"] for s in series]
out = {
    "flag": os.environ.get("EM2_EMISSION"), "content": content, "clock p0": int(node.start_content.reshape(-1)[0]) and None,
    "amplitude": amplitude, "unit": node.units[rec], "quanta": quanta, "T": node.T, "drift": node.drift,
    "W_centre first/min/max/last": [ws[0], min(ws), max(ws), ws[-1]],
    "W_centre change max over an interval": max(abs(b - a) for a, b in zip(ws, ws[1:])),
    "body beat: upward crossings at the centre": len(ups_body), "spacings": beats,
    "laid (engine count) at the end": node.counts["laid"], "laid_nodes": node.counts["laid_nodes"],
    "light centre level min/max": [min(s["light_centre"] for s in series), max(s["light_centre"] for s in series)],
    "light far level min/max": [min(s["light_far"] for s in series), max(s["light_far"] for s in series)],
    "light far: first interval with a level": next((s["i"] for s in series if s["light_far"] != 0), None),
    "light far upward crossings": len(ups_far), "far spacings": far_periods,
    "light centre upward crossings": len(ups_c), "centre spacings": c_periods,
    "run back exact of 10": exact, "census (integers, bits)": list(node.census()), "max transient bits": node.max_transient,
    "turns": node.counts["turns"], "births": node.counts["births"], "body_clicks": node.counts["body_clicks"],
}
from event_universe.core import paces
out["clock p0 at the content"] = paces.clock(node.gamma, content)
out["Gamma"] = node.gamma
json.dump({"summary": out, "series": series}, open(out_path, "w"))
print(json.dumps(out))
