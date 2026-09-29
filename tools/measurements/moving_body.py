"""A BODY AT REST AND THE SAME BODY MOVING (the owner's word of 2026-09-29): the chain body of Gamma 6000 laid by the pixel tool at rest; the moving one its standing record times the plane wave's character cos(k x) at `now` and cos(k x + omega_b) at `before`, omega_b the mode's own rotation read from the standing pair; both stepped by the engine alone on the chain, x open. Per interval: the count's ledger SUM (W_c c + r) (the theorem, to the bit), the quanta on the board, the form's share SUM E_i / 2, the momentum reading, the counts' centroid, and the quanta that crossed the body's shell out and in (a click is a whole quantum across a Link). Usage: moving_body.py <m> <ticks> <every>; k = 2 pi m / length."""

import json
import math
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
m, ticks, every = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3])
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
ratios = sorted(
    set(round(float(b) / float(a), 4) for a, b in zip(now, before, strict=True) if abs(a) > 100)
)
print(
    f"the standing pair's ratio before/now at the peak {cos_b:.5f} (omega_b {math.acos(cos_b):.4f}); ratios across the body {ratios[:4]}...{ratios[-2:]}"
)
k = 2 * math.pi * m / LENGTH
x = np.arange(LENGTH) - peak
m_now = np.rint(now * np.cos(k * x)).astype(np.int64)
m_before = np.rint(now * (np.cos(k * x) * cos_b - np.sin(k * x) * sin_b)).astype(np.int64)
moving_doc = json.loads(rest.read_text())
moving_mode = json.loads(json.dumps(mode))
moving_mode["bodies"][0]["moving"] = {"now": m_now.tolist(), "before": m_before.tolist()}
moving_mode["bodies"][0]["profile"] = m_now.tolist()
moving = d / "moving.json"
moving.write_text(json.dumps(moving_doc))
moving.with_suffix(".mode.json").write_text(json.dumps(moving_mode))


def watch(path, label):
    print(f"=== {label}")
    for attempt in range(6):
        sim = DetectorLawSimulation(load_world(path))
        try:
            sim.step()
            break
        except ValueError as stop:
            words = str(stop).split(" ")
            if "lays" not in words:
                print(f"REFUSED at interval 1: {str(stop)[:400]}")
                return
            declared, laid = int(words[words.index("count") + 1]), int(words[words.index("lays") + 1])
            # the declared counts scaled to the laid total (the count is the record's form: the declaration is a reading), the mode file's digest with them
            world_doc = json.loads(path.read_text())
            nodes = world_doc["measured"][0]["nodes"]
            for node in nodes:
                node["count"] = max(1, int(round(node["count"] * laid / declared)))
            path.write_text(json.dumps(world_doc))
            doc = json.loads(path.with_suffix(".mode.json").read_text())
            doc["world_digest"] = TOOL.input_digest(world_doc)
            path.with_suffix(".mode.json").write_text(json.dumps(doc))
            print(
                f"the gate: declared {declared}, laid {laid}; the declared counts scaled to {sum(n['count'] for n in nodes)} (attempt {attempt + 1})"
            )
    else:
        print("no lay within the gate after 6 attempts")
        return
    block = sim.blocks[0]
    prev_counts = prev_mask = None
    out_clicks = in_clicks = shifts = 0
    ledger0 = None
    share_prev = counts_prev = rem_prev = None
    worst_defects = []
    drift = np.zeros((LENGTH, 1, 1), dtype=np.int64)
    for t in range(1, ticks + 1):
        try:
            if t > 1:
                sim.step()
        except Exception as stop:
            print(f"REFUSED at interval {t}: {str(stop)[:400]}")
            return
        counts = np.asarray(block.counts, dtype=np.int64)
        rem = np.asarray(block.count_remainder, dtype=np.int64)
        wall = sim.count_wall(block)
        mask = np.asarray(block.mask, dtype=bool)
        ledger = int((wall * counts + rem).sum())
        if ledger0 is None:
            ledger0 = ledger
        if prev_counts is not None:
            beyond = ~prev_mask
            delta = int(counts[beyond].sum() - prev_counts[beyond].sum())
            if delta > 0:
                out_clicks += delta
            if delta < 0:
                in_clicks -= delta
            if not np.array_equal(mask, prev_mask):
                shifts += 1
        prev_counts, prev_mask = counts.copy(), mask.copy()
        share_now = np.asarray(sim.count_share(block, block.own), dtype=np.int64)
        if share_prev is not None and counts_prev is not None and rem_prev is not None:
            defect = (share_now - share_prev) - (wall * (counts - counts_prev) + (rem - rem_prev))
            worst = int(np.argmax(np.abs(defect)))
            worst_defects.append((t, worst, int(defect.ravel()[worst])))
            drift += defect
        share_prev, counts_prev, rem_prev = share_now.copy(), counts.copy(), rem.copy()
        if t % every == 0 or t == 1:
            share = int(share_now.sum())
            if t > 1:
                recent = max(worst_defects[-every:], key=lambda w: abs(w[2]))
                print(
                    f"      the continuity's defect Delta share - (W Delta c + Delta r): worst in the last {every} intervals {recent[2] / wall:+.3f} quanta at x = {recent[1]} (t = {recent[0]}); the drift so far, summed: {int(drift.sum()) / wall:+.2f} quanta, at x 110..135 (in quanta): {[round(int(v) / wall, 1) for v in drift[110:136, 0, 0]]}"
                )
                print(f"      counts at x 108..135: {counts[108:136, 0, 0].tolist()}")
            xs = np.arange(LENGTH)
            total = int(counts.sum())
            centroid = float((xs * counts[:, 0, 0]).sum() / total) if total else float("nan")
            print(
                f"t={t:4d} ledger-ledger0 {ledger - ledger0:3d} quanta {total:4d} in the set {int(counts[mask].sum()):4d} beyond {int(counts[~mask].sum()):4d} min {int(counts.min()):3d} | SUM E/2 {share:14d} | momentum {block.momentum} | centroid {centroid:8.2f} | clicks out {out_clicks:4d} in {in_clicks:4d} | set shifts {shifts:3d}",
                flush=True,
            )


watch(rest, "AT REST")
watch(moving, f"MOVING, k = 2 pi {m} / {LENGTH}")
