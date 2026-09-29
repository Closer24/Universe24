"""A BOUND BODY INSIDE A BOUND BODY, laid apart and set together (the owner's word of 2026-09-29): the outer body of 600 quanta on the middle Node of the open chain and the inner of `inner` quanta `offset` Nodes beside it, each laid alone by the pixel tool in its own world (the tool lays two bodies sharing Nodes as one body, HIGHLIGHTS.md: detectors stand apart so that their modes do not merge), then both set in one world with one mode file; stepped by the engine alone. Per interval and per body: the count's ledger SUM (W_c c + r), the quanta in its set and beyond, the counts' centroid and the quanta that crossed its shell out and in. Usage: nested_by_hand.py <offset> <inner> <ticks> <every>."""

import json
import sys
import tempfile
from pathlib import Path

import numpy as np

sys.path.insert(0, ".")
sys.path.insert(0, "src")
import event_universe.world_files as wf
from event_universe.events.detector_law import DetectorLawSimulation
from event_universe.world_files import load_world
from tests.laws import load_file

ROOT = Path(".")
TOOL = load_file("pixel_mode", ROOT / "tools" / "pixel_mode.py")
offset, inner, ticks, every = (int(a) for a in sys.argv[1:5])
LENGTH = 240
d = Path(tempfile.mkdtemp())
wf.REPOSITORY_ROOT = d
events = ROOT / "examples" / "events"
universe = json.loads((events / "planck_6000.json").read_text())
for family in universe["families"]:
    if family.get("name") == "gravity":
        family["held"]["divisor"] = 10_000
(d / "u.json").write_text(json.dumps(universe))
(d / "e.json").write_bytes((events / "engine_start.json").read_bytes())


def body(x, count):
    return dict(
        family="matter",
        nodes=[dict(node=[x, 0, 0], count=count)],
        momentum=[0, 0, 0],
        momentum_before=[0, 0, 0],
        phase_denominator=1024,
    )


def document(bodies):
    return dict(
        shape=[LENGTH, 1, 1],
        boundary=dict(x="open", y="periodic", z="periodic"),
        detectors=[],
        ticks=ticks,
        N=65536,
        face_depth=1,
        universe="u.json",
        engine="e.json",
        measured=bodies,
    )


laid, entries = [], []
for name, b in (("outer", body(LENGTH // 2, 600)), ("inner", body(LENGTH // 2 + offset, inner))):
    world = d / f"{name}.json"
    world.write_text(json.dumps(document([b])))
    TOOL.main(["--input", str(world)])
    laid.append(json.loads(world.read_text())["measured"][0])
    entries.append(json.loads(world.with_suffix(".mode.json").read_text())["bodies"][0])
    xs = [n["node"][0] for n in laid[-1]["nodes"]]
    print(
        f"the {name} body laid alone: x {min(xs)}..{max(xs)}, {sum(n['count'] for n in laid[-1]['nodes'])} quanta, clock {entries[-1]['clock']}, amplitude {entries[-1]['amplitude']}"
    )
both = document(laid)
world = d / "both.json"
world.write_text(json.dumps(both))
world.with_suffix(".mode.json").write_text(
    json.dumps({"world_digest": TOOL.input_digest(both), "bodies": entries})
)
try:
    sim = DetectorLawSimulation(load_world(world))
except Exception as stop:
    print(f"REFUSED at the load: {str(stop)[:500]}")
    sys.exit()
state = [dict(prev=None, mask=None, out=0, inn=0, ledger0=None) for _ in sim.blocks]
for t in range(1, ticks + 1):
    try:
        sim.step()
    except Exception as stop:
        print(f"REFUSED at interval {t}: {str(stop)[:500]}")
        break
    line = f"t={t:4d}"
    for block, s in zip(sim.blocks, state, strict=True):
        counts = np.asarray(block.counts, dtype=np.int64)
        rem = np.asarray(block.count_remainder, dtype=np.int64)
        wall = sim.count_wall(block)
        mask = np.asarray(block.mask, dtype=bool)
        ledger = int((wall * counts + rem).sum())
        if s["ledger0"] is None:
            s["ledger0"] = ledger
        if s["prev"] is not None:
            delta = int(counts[~s["mask"]].sum() - s["prev"][~s["mask"]].sum())
            if delta > 0:
                s["out"] += delta
            if delta < 0:
                s["inn"] -= delta
        s["prev"], s["mask"] = counts.copy(), mask.copy()
        total = int(counts.sum())
        centroid = float((np.arange(LENGTH) * counts[:, 0, 0]).sum() / total) if total else float("nan")
        xs = np.nonzero(mask[:, 0, 0])[0]
        line += f" | body {block.number}: ledger {ledger - s['ledger0']:2d} quanta {total:4d} set x {xs.min()}..{xs.max()} in {int(counts[mask].sum()):4d} beyond {int(counts[~mask].sum()):3d} min {int(counts.min()):2d} centroid {centroid:7.2f} out {s['out']:3d} in {s['inn']:3d}"
    if t % every == 0 or t <= 2:
        print(line, flush=True)
