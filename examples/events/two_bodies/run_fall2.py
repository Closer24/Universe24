"""Two bound matter bodies at rest on a long open board, nothing declared but their lay, and one body alone as the
control.

The lay is the matter pixel's standing record (examples/events/matter_alone) cropped to 17 x 17 across and embedded at
each centre, 12 and X - 13; the engine's own start lays the wells; the held writes on. Per interval, for each half of the
board (cut at X // 2): the share read at the paces, its centroid, the rms radius, the share beyond a sphere of radius 9
about the centroid and the content at the centroid. The control is the same body alone at x = 12 on the same board, the
same distance from the open face. The arguments are the intervals, the board's length X and its width across:

    python examples/events/two_bodies/run_fall2.py [300 [49 [17]]]

The world files (fall_pair_49x17.json, fall_alone_49x17.json with their mode files) and the record (fall_results_49x17.json,
the shipped copy beside this script; the three checks read the two world files) go under runs/two_bodies/ at the
repository root.
"""

import json
import math
import sys
import time
from pathlib import Path

import numpy as np

REPO = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(REPO / "src"))

from event_universe import node  # noqa: E402
from event_universe.lattice import Lattice  # noqa: E402
from event_universe.world_files import input_digest, load_world  # noqa: E402

OUT = REPO / "runs" / "two_bodies"
INTERVALS = int(sys.argv[1]) if len(sys.argv) > 1 else 300
X = int(sys.argv[2]) if len(sys.argv) > 2 else 49
YZ = int(sys.argv[3]) if len(sys.argv) > 3 else 17
CENTRES = {"pair": [12, X - 13], "alone": [12]}
TAG = f"_{X}x{YZ}"
CROP = (25 - YZ) // 2
SHED_RADIUS = 9.0


def log(*a):
    print(time.strftime("%H:%M:%S"), *a, flush=True)


w0 = json.loads((REPO / "examples/events/matter_alone/pixel.json").read_text())
m0 = json.loads((REPO / "examples/events/matter_alone/pixel.mode.json").read_text())
e0 = m0["bodies"][0]
now0 = np.array(e0["moving"]["now"], dtype=object).reshape(25, 25, 25)
bef0 = np.array(e0["moving"]["before"], dtype=object).reshape(25, 25, 25)
nodes0 = w0["bodies"][0]["nodes"]


def build(name, centres):
    """The world file and its mode file for the bodies at `centres`, the pixel's record embedded at each."""
    now = np.zeros((X, YZ, YZ), dtype=object)
    bef = np.zeros((X, YZ, YZ), dtype=object)
    bodies = []
    entries = []
    blk_now = now0[:, CROP : CROP + YZ, CROP : CROP + YZ]
    blk_bef = bef0[:, CROP : CROP + YZ, CROP : CROP + YZ]
    for xc in centres:
        dx = xc - 12
        bn = np.zeros((X, YZ, YZ), dtype=object)
        bb = np.zeros((X, YZ, YZ), dtype=object)
        bn[dx : dx + 25] = blk_now
        bb[dx : dx + 25] = blk_bef
        now = now + bn
        bef = bef + bb
        kept = [
            n for n in nodes0 if CROP <= n["node"][1] < CROP + YZ and CROP <= n["node"][2] < CROP + YZ
        ]
        bodies.append(
            {
                "family": "matter",
                "nodes": [
                    {
                        "node": [n["node"][0] + dx, n["node"][1] - CROP, n["node"][2] - CROP],
                        "count": n["count"],
                    }
                    for n in kept
                ],
            }
        )
        entry = {kk: vv for kk, vv in e0.items() if kk not in ("moving", "profile")}
        entry["moving"] = {"now": [int(t) for t in bn.ravel()], "before": [int(t) for t in bb.ravel()]}
        entries.append(entry)
    doc = {
        "shape": [X, YZ, YZ],
        "boundary": {"x": "open", "y": "open", "z": "open"},
        "face_depth": 1,
        "intervals": INTERVALS,
        "universe": "examples/events/rule.json",
        "engine": "examples/events/engine_start.json",
        "bodies": bodies,
        "node_detectors": [],
    }
    mode = {"world_digest": input_digest(doc), "bodies": entries, "packets": []}
    p = OUT / f"fall_{name}{TAG}.json"
    p.write_text(json.dumps(doc))
    p.with_suffix(".mode.json").write_text(json.dumps(mode))
    return p


OUT.mkdir(parents=True, exist_ok=True)
coords = np.stack(np.meshgrid(np.arange(X), np.arange(YZ), np.arange(YZ), indexing="ij"), -1).astype(
    float
)
results = {"params": {"X": X, "YZ": YZ, "centres": CENTRES, "intervals": INTERVALS}, "runs": {}}
for name, centres in CENTRES.items():
    log(f"== {name}: building and loading (the start lays the wells)")
    p = build(name, centres)
    t0 = time.time()
    world = load_world(p)
    board = Lattice(world, (lambda s: None))
    mi = {f.name: i for i, f in enumerate(board.families)}["matter"]
    log(f"{name}: start done in {time.time() - t0:.0f}s")
    halves = [(0, X)] if len(centres) == 1 else [(0, X // 2), (X // 2, X)]
    rows = []
    t0 = time.time()
    for t in range(INTERVALS + 1):
        cnt = np.asarray(board.quanta(mi)[0], dtype=float)
        content_now, _ = node.read_lines(mi, board.families, board.states, 1, 0)
        content_now = np.asarray(content_now)
        row = {"t": t, "count_total": float(cnt.sum()), "bodies": []}
        for lo, hi in halves:
            c = cnt[lo:hi]
            co = coords[lo:hi]
            tot = c.sum()
            cen = (c[..., None] * co).sum(axis=(0, 1, 2)) / tot if tot else np.zeros(3)
            d2 = ((co - cen) ** 2).sum(-1)
            rms = math.sqrt((c * d2).sum() / tot) if tot else 0.0
            inside = c[d2 <= SHED_RADIUS**2].sum()
            ci = tuple(int(round(v)) for v in cen)
            row["bodies"].append(
                {
                    "count": float(tot),
                    "cx": float(cen[0]),
                    "cy": float(cen[1]),
                    "cz": float(cen[2]),
                    "rms": rms,
                    "shed": float(tot - inside),
                    "content_centroid": int(content_now[ci]),
                }
            )
        rows.append(row)
        if t % 25 == 0:
            log(
                f"{name} t={t:3d} "
                + " | ".join(
                    f"cx={b['cx']:6.3f} n={b['count']:7.1f} rms={b['rms']:5.2f} c={b['content_centroid']}"
                    for b in row["bodies"]
                )
            )
        if t < INTERVALS:
            board.step()
    results["runs"][name] = rows
    log(f"{name}: {INTERVALS} intervals in {time.time() - t0:.0f}s")
    (OUT / f"fall_results{TAG}.json").write_text(json.dumps(results))
log("done")
