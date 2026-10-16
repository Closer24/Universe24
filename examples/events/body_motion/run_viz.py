"""A bound matter body pushed along +x on a long open board, recorded for the page body_motion.html.

The lay is the matter pixel's standing record (examples/events/matter_alone) cropped to 17 x 17 across and embedded in a
61 x 17 x 17 board, the pushed body's levels the record times cos(k x') with k = pi / 8 and its level before with the envelope shifted by the
band's velocity v; the engine's own start lays the wells; 200 intervals (the first argument), the held writes on. Per
interval: the share read at the paces, its centroid, the rms radius, the share beyond a sphere of radius 9 about the
centroid, the largest level and the content at the centroid; per interval also the slices the page draws, the level now and the
content on the middle plane z = 8 and the share per layer of x. The world files and the record go under
runs/body_motion/ at the repository root (viz_results.json; build_page.py embeds it in the page). Run from anywhere:

    python examples/events/body_motion/run_viz.py [intervals]
"""

import json
import math
import re
import sys
import time
from pathlib import Path

import numpy as np

REPO = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(REPO / "src"))

from event_universe import node  # noqa: E402
from event_universe.core import paces  # noqa: E402
from event_universe.lattice import Lattice  # noqa: E402
from event_universe.world_files import input_digest, load_world  # noqa: E402

OUT = REPO / "runs" / "body_motion"
GAMMA, NUM, DEN = 6000, 4000, 6000
K_WAVE = (1, 8)  # k = pi * 1/8 per Link along +x
X, DX = 61, 2
YZ = 17
CROP = (25 - YZ) // 2
MID = YZ // 2
INTERVALS = int(sys.argv[1]) if len(sys.argv) > 1 else 200
SHED_RADIUS = 9.0


def log(*a):
    print(time.strftime("%H:%M:%S"), *a, flush=True)


w0 = json.loads((REPO / "examples/events/matter_alone/pixel.json").read_text())
m0 = json.loads((REPO / "examples/events/matter_alone/pixel.mode.json").read_text())
e0 = m0["bodies"][0]
now0 = np.array(e0["moving"]["now"], dtype=object).reshape(25, 25, 25)
bef0 = np.array(e0["moving"]["before"], dtype=object).reshape(25, 25, 25)

# the content and the reach over the body, from the engine's own start on the original board
log("loading the original pixel for its content map")
world = load_world(REPO / "examples/events/matter_alone/pixel.json")
board = Lattice(world, (lambda s: None))
mi = {f.name: i for i, f in enumerate(board.families)}["matter"]
content, _axes = node.read_lines(mi, board.families, board.states, 1, 0)
clock, pace = paces.node_paces(GAMMA, content)
pace_f = np.asarray(pace, dtype=float)
Rw = NUM * pace_f**2 / (3 * DEN * GAMMA**2)  # R / w per Node, the exact ratio in floats
phi = now0.astype(float)
weight = phi**2
Rw_mean = float((Rw * weight).sum() / weight.sum())
c_centre = int(np.asarray(content)[12, 12, 12])
two_cos0 = e0["clock"][0] / e0["clock"][1]
om0 = math.acos(two_cos0 / 2)
k = math.pi * K_WAVE[0] / K_WAVE[1]
two_cos = two_cos0 - 2 * Rw_mean * (1 - math.cos(k))
om = math.acos(two_cos / 2)
v = Rw_mean * math.sin(k) / math.sin(om)
log(
    f"content at centre {c_centre}, pace centre {int(pace[12, 12, 12])}, R/w vacuum {Rw[0, 0, 0]:.4f} "
    f"centre {Rw[12, 12, 12]:.4f} phi2-mean {Rw_mean:.4f}"
)
log(
    f"omega0 {om0:.4f} (2cos {two_cos0:.4f}); k {k:.4f}; omega {om:.4f} (2cos {two_cos:.4f}); "
    f"v {v:.4f} Links/interval -> {v * INTERVALS:.1f} Links in {INTERVALS}"
)
del board, world


def embed(arr):
    big = np.zeros((X, YZ, YZ), dtype=object)
    big[DX : DX + 25, :, :] = arr[:, CROP : CROP + YZ, CROP : CROP + YZ]
    return big


xc = 12 + DX
xs = (np.arange(X) - xc)[:, None, None].astype(float)
phi_big = embed(now0).astype(float)
phi_next = np.roll(phi_big, -1, axis=0)
phi_next[-1] = 0
phi_shift = phi_big + v * (phi_next - phi_big)  # phi(x' + v), the envelope one interval earlier


def rnd(a):
    return np.vectorize(lambda t: int(round(t)), otypes=[object])(a)


lays = {
    "boost": (rnd(phi_big * np.cos(k * xs)), rnd(phi_shift * np.cos(k * xs + om))),
}
kept = [
    n
    for n in w0["bodies"][0]["nodes"]
    if CROP <= n["node"][1] < CROP + YZ and CROP <= n["node"][2] < CROP + YZ
]
nodes = [
    {"node": [n["node"][0] + DX, n["node"][1] - CROP, n["node"][2] - CROP], "count": n["count"]}
    for n in kept
]
declared = sum(n["count"] for n in nodes)


def write_world(name, now, bef):
    doc = {
        "shape": [X, YZ, YZ],
        "boundary": {"x": "open", "y": "open", "z": "open"},
        "face_depth": 1,
        "intervals": INTERVALS,
        "universe": "examples/events/rule.json",
        "engine": "examples/events/engine_start.json",
        "bodies": [{"family": "matter", "nodes": nodes}],
        "node_detectors": [],
    }
    entry = {kk: vv for kk, vv in e0.items() if kk not in ("moving", "profile")}
    entry["moving"] = {"now": [int(t) for t in now.ravel()], "before": [int(t) for t in bef.ravel()]}
    mode = {"world_digest": input_digest(doc), "bodies": [entry], "packets": []}
    p = OUT / f"viz_{name}.json"
    p.write_text(json.dumps(doc))
    p.with_suffix(".mode.json").write_text(json.dumps(mode))
    return p


def load_gated(name, now, bef):
    """The world loaded under the start's gate: where the share read is off the declared count, the levels rescaled."""
    for _attempt in range(4):
        p = write_world(name, now, bef)
        try:
            world = load_world(p)
            lines = []
            board = Lattice(world, lines.append)
            return board, world
        except ValueError as err:
            m = re.search(r"declares the count (\d+) and its family's share reads (\d+)", str(err))
            if not m:
                raise
            dec, read = int(m.group(1)), int(m.group(2))
            s = math.sqrt(dec / read)
            log(f"{name}: gate read {read} against {dec}; rescaling levels by {s:.4f}")
            now = rnd(now.astype(float) * s)
            bef = rnd(bef.astype(float) * s)
    raise RuntimeError("gate not met")


OUT.mkdir(parents=True, exist_ok=True)
coords = np.stack(np.meshgrid(np.arange(X), np.arange(YZ), np.arange(YZ), indexing="ij"), -1).astype(
    float
)
slices = {"now": [], "content": [], "count_x": []}
results = {
    "params": {
        "k_wave": K_WAVE,
        "k": k,
        "omega0": om0,
        "omega": om,
        "v": v,
        "Rw_mean": Rw_mean,
        "X": X,
        "xc": xc,
        "declared": declared,
        "intervals": INTERVALS,
    },
    "runs": {},
}
for name, (now, bef) in lays.items():
    log(f"== {name}: loading (the start lays the wells)")
    t0 = time.time()
    board, world = load_gated(name, now, bef)
    log(f"{name}: start done in {time.time() - t0:.0f}s")
    rows = []
    t0 = time.time()
    for t in range(INTERVALS + 1):
        cnt = np.asarray(board.quanta(mi)[0], dtype=float)
        total = cnt.sum()
        cen = (cnt[..., None] * coords).sum(axis=(0, 1, 2)) / total if total else np.zeros(3)
        d2 = ((coords - cen) ** 2).sum(-1)
        rms = math.sqrt((cnt * d2).sum() / total) if total else 0.0
        inside = cnt[d2 <= SHED_RADIUS**2].sum()
        lv = np.asarray(board.states[mi].lines[0].now, dtype=float)
        ci = tuple(int(round(c)) for c in cen)
        content_now, _ = node.read_lines(mi, board.families, board.states, 1, 0)
        row = {
            "t": t,
            "count": float(total),
            "cx": float(cen[0]),
            "cy": float(cen[1]),
            "cz": float(cen[2]),
            "rms": rms,
            "shed": float(total - inside),
            "max_level": float(np.abs(lv).max()),
            "content_centroid": int(np.asarray(content_now)[ci]),
        }
        rows.append(row)
        now_mid = np.asarray(board.states[mi].lines[0].now)[:, :, MID].tolist()
        slices["now"].append([[int(v) for v in r_] for r_ in now_mid])
        slices["content"].append(
            [[int(v) for v in r_] for r_ in np.asarray(content_now)[:, :, MID].tolist()]
        )
        slices["count_x"].append([float(v) for v in cnt.sum(axis=(1, 2)).tolist()])
        if t % 20 == 0:
            log(
                f"{name} t={t:3d} count={total:8.1f} cx={cen[0]:6.2f} rms={rms:5.2f} shed={total - inside:7.1f} "
                f"max={row['max_level']:6.0f} c_centroid={row['content_centroid']}"
            )
        if t < INTERVALS:
            board.step()
    results["runs"][name] = rows
    results["slices"] = slices
    results["params"]["YZ"] = YZ
    results["params"]["mid"] = MID
    log(f"{name}: {INTERVALS} intervals in {time.time() - t0:.0f}s")
    (OUT / "viz_results.json").write_text(json.dumps(results))
log("done")
