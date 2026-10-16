"""The ramp pass: the law's push coefficient measured on the engine's own step (ALGEBRA.md, The push).

A content ramp s (x - 24), s = +-1 and +-2 content units per Link (and s = 0, the null), is laid on gravity's time line,
which alone is held at its lay plus the ramp after every step (gravity's held write is nil at its wall), so that
dU/dx = s / Gamma exactly; the body at the centre x = 24 of the 49 x 17 x 17 open board, so the two walls' pushes cancel.
Two records fall down the ramp for 120 intervals: the body (the matter pixel of examples/events/matter_alone, its own
binding row written and moving with it) and a free packet (a rotating Gaussian of the matter line, amplitude 3,000,
sigma 3 Links, now = A G and before = round(nu A G), every holder held at its rest, no body). The reading: the centroid's
acceleration a(s) from a quadratic fit over the windows 30, 50, 80 and 120, the coefficient (a(+s) - a(-s)) / 2 / (s / Gamma)
per slope, against the law's 2 (1 - nu) N^2 (R / w) / sin^2(omega_0) at the record's own content (cos omega_0 =
1 - (1 - nu) N^2; N^2 and R / w weighted by the share). The world files go under runs/two_bodies/ at the repository root
with the result ramp_pass.json (the fits per slope and window, the coefficients, the formula's values and the ratios);
the shipped copy stands beside this script.

    python examples/events/two_bodies/ramp_pass.py
"""

import json
import sys
import time
from pathlib import Path

import numpy as np

REPO = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(REPO / "src"))

from event_universe import node  # noqa: E402
from event_universe.core import paces  # noqa: E402
from event_universe.lattice import Lattice  # noqa: E402
from event_universe.records import Record  # noqa: E402
from event_universe.world_files import input_digest, load_world  # noqa: E402

OUT = REPO / "runs" / "two_bodies"
GAMMA, NUM, DEN = 6000, 4000, 6000
NU = NUM / DEN
X, YZ, CENTRE = 49, 17, 24
CROP = (25 - YZ) // 2
T = 120
WINDOWS = (30, 50, 80, 120)
SLOPES = (1, -1, 0, 2, -2)
PACKET_AMPLITUDE, PACKET_SIGMA = 3000, 3.0


def log(*a):
    print(time.strftime("%H:%M:%S"), *a, flush=True)


w0 = json.loads((REPO / "examples/events/matter_alone/pixel.json").read_text())
m0 = json.loads((REPO / "examples/events/matter_alone/pixel.mode.json").read_text())
e0 = m0["bodies"][0]
now0 = np.array(e0["moving"]["now"], dtype=object).reshape(25, 25, 25)
bef0 = np.array(e0["moving"]["before"], dtype=object).reshape(25, 25, 25)
nodes0 = w0["bodies"][0]["nodes"]


def world(name, centres):
    """The world file and its mode file: the pixel's record embedded at each centre, none for the packet's board."""
    doc = {
        "shape": [X, YZ, YZ],
        "boundary": {"x": "open", "y": "open", "z": "open"},
        "face_depth": 1,
        "intervals": T,
        "universe": "examples/events/rule.json",
        "engine": "examples/events/engine_start.json",
        "bodies": [],
        "node_detectors": [],
    }
    p = OUT / f"{name}.json"
    if not centres:
        p.write_text(json.dumps(doc))
        return p
    entries = []
    blk_now = now0[:, CROP : CROP + YZ, CROP : CROP + YZ]
    blk_bef = bef0[:, CROP : CROP + YZ, CROP : CROP + YZ]
    for xc in centres:
        dx = xc - 12
        bn = np.zeros((X, YZ, YZ), dtype=object)
        bb = np.zeros((X, YZ, YZ), dtype=object)
        bn[dx : dx + 25] = blk_now
        bb[dx : dx + 25] = blk_bef
        kept = [
            n for n in nodes0 if CROP <= n["node"][1] < CROP + YZ and CROP <= n["node"][2] < CROP + YZ
        ]
        doc["bodies"].append(
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
    mode = {"world_digest": input_digest(doc), "bodies": entries, "packets": []}
    p.write_text(json.dumps(doc))
    p.with_suffix(".mode.json").write_text(json.dumps(mode))
    return p


def loaded(path):
    board = Lattice(load_world(path), (lambda s: None))
    return board, {f.name: i for i, f in enumerate(board.families)}


def snapshot(board, index):
    """A held family's lines and write remainders as they stand, to be held there after every step."""
    state = board.states[index]
    lines = [
        (np.asarray(li.now).copy(), np.asarray(li.before).copy(), np.asarray(li.remainder).copy())
        for li in state.lines
    ]
    return lines, [np.asarray(r).copy() for r in state.write_remainders]


def hold(board, saved, gravity, ramp):
    """Every saved family put back at its snapshot, gravity's time line at its lay plus the ramp."""
    for index, (lines, remainders) in saved.items():
        state = board.states[index]
        for k, (now, bef, rem) in enumerate(lines):
            add = ramp if (index == gravity and k == 0) else 0
            state.lines[k] = Record(now + add, bef + add, rem.copy())
        state.write_remainders = [r.copy() for r in remainders]


def centroid(board, mi):
    cnt = np.asarray(board.quanta(mi)[0], dtype=float)
    xs = np.arange(cnt.shape[0], dtype=float)
    tot = cnt.sum()
    return float((cnt.sum(axis=(1, 2)) * xs).sum() / tot), float(tot)


def formula(board, mi):
    """The law's coefficient at the record's own content, 2 (1 - nu) N^2 (R / w) / sin^2(omega_0), weighted by the share."""
    content, _ = node.read_lines(mi, board.families, board.states, 1, 0)
    cnt = np.asarray(board.quanta(mi)[0], dtype=float)
    p0, pi = paces.node_paces(GAMMA, np.asarray(content).astype(int))
    p0, pi = np.asarray(p0, float), np.asarray(pi, float)
    n2 = float(((p0 / GAMMA) ** 2 * cnt).sum() / cnt.sum())
    rw = float((NUM * pi**2 / (3 * DEN * GAMMA**2) * cnt).sum() / cnt.sum())
    cos0 = 1 - (1 - NU) * n2
    return 2 * (1 - NU) * n2 * rw / (1 - cos0**2), n2, rw


def fallen(board, names, held, s, label):
    """One record down the ramp s for T intervals: the centroid's acceleration per window."""
    mi, gi = names["matter"], names["gravity"]
    saved = {h: snapshot(board, h) for h in held}
    kind = np.asarray(board.states[mi].lines[0].now).dtype
    ramp = (
        (s * (np.arange(X, dtype=np.int64) - CENTRE))[:, None, None]
        * np.ones((1, YZ, YZ), dtype=np.int64)
    ).astype(kind)
    hold(board, saved, gi, ramp)
    coefficient, n2, rw = formula(board, mi)
    cx, n = [], []
    t0 = time.time()
    for t in range(T + 1):
        c, tot = centroid(board, mi)
        cx.append(c)
        n.append(tot)
        if t < T:
            board.step()
            hold(board, saved, gi, ramp)
    tt = np.arange(T + 1, dtype=float)
    fits = {str(w): float(2 * np.polyfit(tt[: w + 1], np.array(cx[: w + 1]), 2)[0]) for w in WINDOWS}
    log(
        f"{label} s={s:+d}: N^2 {n2:.4f} R/w {rw:.4f} formula {coefficient:.4f}; share {n[0]:.0f} -> {n[-1]:.0f}; "
        f"cx {cx[0]:.4f} -> {cx[-1]:.4f}; "
        + " ".join(f"a(0..{w}) {fits[str(w)]:+.3e}" for w in WINDOWS)
        + f"  ({time.time() - t0:.0f} s)"
    )
    return {"fits": fits, "formula": coefficient, "N2": n2, "Rw": rw, "share": [n[0], n[-1]]}


def packet(board, mi):
    """The free packet laid on the matter line: a Gaussian at the centre, rotating as the band has it."""
    kind = np.asarray(board.states[mi].lines[0].now).dtype
    g = np.indices((X, YZ, YZ)).astype(float)
    r2 = (g[0] - CENTRE) ** 2 + (g[1] - YZ // 2) ** 2 + (g[2] - YZ // 2) ** 2
    amp = PACKET_AMPLITUDE * np.exp(-r2 / (2 * PACKET_SIGMA**2))
    remainder = np.asarray(board.states[mi].lines[0].remainder).copy()
    board.states[mi].lines[0] = Record(
        np.rint(amp).astype(kind), np.rint(NU * amp).astype(kind), remainder
    )


def coefficients(results, label):
    """Per window the coefficient at s = 1 and s = 2, (a(+s) - a(-s)) / 2 / (s / Gamma), and the ratio to the formula."""
    found = {}
    for w in WINDOWS:
        w = str(w)
        c1 = (results[f"{label} s=1"]["fits"][w] - results[f"{label} s=-1"]["fits"][w]) / 2 / (1 / GAMMA)
        c2 = (results[f"{label} s=2"]["fits"][w] - results[f"{label} s=-2"]["fits"][w]) / 2 / (2 / GAMMA)
        law = results[f"{label} s=1"]["formula"]
        found[w] = {
            "s=1": c1,
            "s=2": c2,
            "formula": law,
            "ratios": [c1 / law, c2 / law],
            "null": results[f"{label} s=0"]["fits"][w],
        }
        log(
            f"{label.upper()} window 0..{w}: coefficient at s=1 {c1:.4f}, at s=2 {c2:.4f}; the formula's {law:.4f}; ratios {c1 / law:.3f}, {c2 / law:.3f}; s=0 a {found[w]['null']:+.1e}"
        )
    return found


OUT.mkdir(parents=True, exist_ok=True)
results = {}
for s in SLOPES:
    board, names = loaded(world(f"ramp_body_{s}", [CENTRE]))
    results[f"body s={s}"] = fallen(board, names, (names["gravity"],), s, "body")
board_file = world("ramp_packet", [])
for s in SLOPES:
    board, names = loaded(board_file)
    packet(board, names["matter"])
    results[f"packet s={s}"] = fallen(board, names, tuple(board.held), s, "packet")
summary = {
    "body": coefficients(results, "body"),
    "packet": coefficients(results, "packet"),
    "runs": results,
}
(OUT / "ramp_pass.json").write_text(json.dumps(summary, indent=1))
log("done")
