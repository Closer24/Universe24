"""THE MOMENTUM READING'S INGREDIENTS on the moving chain body: per interval the reading n, the body's wall W = 3 Q M, the weight the count's line hands the reading, the current's sum per axis, T and M; against the velocity of the counts' centroid. Usage: momentum_trace.py <m> <ticks>."""

import json
import math
import sys
import tempfile
from pathlib import Path

import numpy as np

sys.path.insert(0, ".")
sys.path.insert(0, "src")
import event_universe.world_files as wf
from event_universe.events import momentum_reading
from event_universe.events.detector_law import DetectorLawSimulation
from event_universe.world_files import load_world
from tests.laws import load_file

ROOT = Path(".")
TOOL = load_file("pixel_mode", ROOT / "tools" / "pixel_mode.py")
m, ticks = int(sys.argv[1]), int(sys.argv[2])
LENGTH, QUANTA = 240, 600
d = Path(tempfile.mkdtemp())
wf.REPOSITORY_ROOT = d
events = ROOT / "examples" / "events"
universe = json.loads((events / "planck_6000.json").read_text())
for family in universe["families"]:
    if family.get("name") == "gravity":
        family["held"]["divisor"] = 10_000
(d / "u.json").write_text(json.dumps(universe))
(d / "e.json").write_bytes((events / "engine_start.json").read_bytes())
body = dict(
    family="matter",
    nodes=[dict(node=[LENGTH // 2, 0, 0], count=QUANTA)],
    momentum=[0, 0, 0],
    momentum_before=[0, 0, 0],
    phase_denominator=1024,
)
document = dict(
    shape=[LENGTH, 1, 1],
    boundary=dict(x="open", y="periodic", z="periodic"),
    detectors=[],
    ticks=ticks,
    N=65536,
    face_depth=1,
    universe="u.json",
    engine="e.json",
    measured=[body],
)
rest = d / "rest.json"
rest.write_text(json.dumps(document))
TOOL.main(["--input", str(rest)])
mode = json.loads(rest.with_suffix(".mode.json").read_text())
entry = mode["bodies"][0]
now = np.array(entry["moving"]["now"], dtype=np.int64)
before = np.array(entry["moving"]["before"], dtype=np.int64)
peak = int(np.argmax(np.abs(now)))
cos_b = before[peak] / now[peak]
sin_b = math.sqrt(1 - cos_b * cos_b)
k = 2 * math.pi * m / LENGTH
x = np.arange(LENGTH) - peak
factor = 1.0692
m_now = np.rint(factor * now * np.cos(k * x)).astype(np.int64)
m_before = np.rint(factor * now * (np.cos(k * x) * cos_b - np.sin(k * x) * sin_b)).astype(np.int64)
e = mode["bodies"][0]
e["moving"] = {"now": m_now.tolist(), "before": m_before.tolist()}
e["profile"] = m_now.tolist()
e["amplitude"] = int(np.abs(m_now).max())
grow = max(factor, e["amplitude"] / e["clock"][1])
e["clock"] = [int(round(e["clock"][0] * grow)), int(round(e["clock"][1] * grow))]
moving = d / "moving.json"
moving.write_text(rest.read_text())
moving.with_suffix(".mode.json").write_text(json.dumps(mode))

TRACE = {}
_read = momentum_reading.read_momentum


def tracing(loop, block, arrived, wall):
    live = block.own
    port_now, port_before = arrived[0][0], arrived[1][0]  # the +x Port's arrivals of now and before
    total = int((port_now * live.before - port_before * live.now).sum(dtype=object))
    TRACE["last"] = dict(
        weight_handed=int(wall),
        W=int(loop.wall_of(block)),
        M=int(loop._body_count(block)),
        T=int(loop.world.quantum_action),
        total_x=total,
        num=int(loop.pair_arrays(live.family, live.pair)[0].max()),
        den=int(loop.pair_arrays(live.family, live.pair)[1].max()),
    )
    return _read(loop, block, arrived, wall)


momentum_reading.read_momentum = tracing
sim = DetectorLawSimulation(load_world(moving))
block = sim.blocks[0]
sim._read_momentum = lambda b, a, w: tracing(sim, b, a, w)
previous = None
for t in range(1, ticks + 1):
    sim.step()
    counts = np.asarray(block.counts, dtype=np.int64)
    total = int(counts.sum())
    centroid = float((np.arange(LENGTH) * counts[:, 0, 0]).sum() / total)
    v = None if previous is None else centroid - previous
    previous = centroid
    tr = TRACE.get("last", {})
    if tr:
        # the law's normalization: n = 3 Q j div T with j the current in the form's units, num x the bilinear sum, per interval; W v for a rigid packet
        law = 3 * (tr["W"] // (3 * tr["M"])) * tr["num"] * tr["total_x"] // tr["T"]
        print(
            f"t={t:3d} reading n_x {block.momentum[0]:12d} | W {tr['W']} M {tr['M']} T {tr['T']} weight handed {tr['weight_handed']} num {tr['num']} den {tr['den']} | current sum SUM (now_j before_i - before_j now_i) over +x {tr['total_x']:14d} | n = 3 Q num SUM div T {law:10d} | W x centroid velocity {'' if v is None else round(tr['W'] * v)} (v {'' if v is None else round(v, 4)})",
            flush=True,
        )
