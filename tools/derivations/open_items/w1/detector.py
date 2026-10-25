"""A body's light at a detector Node (hand w1, BRIEF_w (b), (c)): the bare 7-cube torus at the 54-bit den with the light sea standing (one quantum per Node but the lay's origin), one body (one quantum of the point family with g nearest 0.83) laid at the centre, or none (the control), run `intervals` intervals; every credit, birth and refused line of the board's own close is kept with its Node, its proper time and its readings. Printed: the body's own credits at its Node (the beat, the intervals between its clicks in the board's interval and in the Node's proper), the clicks at the Node three Links away along z and at every Node by their distance from the body, the control's clicks, the content U at the body's Node and at the detector Node at the end, the ratio of the clicks' spacing far and near against e^(U_body - U_detector), and the uncertainty floor of each reading.

Usage: python detector.py <den> <body 0|1> <intervals>
"""

from __future__ import annotations

import json
import math
import sys
import time
from collections import Counter, defaultdict
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import w1lib  # noqa: E402

den = int(sys.argv[1]) if len(sys.argv) > 1 else w1lib.DEN54
with_body = int(sys.argv[2]) if len(sys.argv) > 2 else 1
intervals = int(sys.argv[3]) if len(sys.argv) > 3 else 300
cube = 7
tag = f"det_{den}_body{with_body}_{intervals}"
folder = Path("/dev/shm/tmp/w1") / tag
out = Path(__file__).resolve().parent / "out"
out.mkdir(exist_ok=True)

lines: list[dict] = []
board = w1lib.board_of(folder, den, cube, intervals, lines)
k, name, num, den_k, g = w1lib.family_with_gap(board, 0.83)
centre = cube // 2
at = (centre, centre, centre)
detector = (centre, centre, (centre + 3) % cube)
if with_body:
    board.born_point(k)
    w1lib.lay_body(board, k, at, 0, 1)
gamma = board.world.node_clock
shape = board.shape
print(f"family {k} {name!r} g {g:.4f}; body {'at ' + str(at) if with_body else 'absent'}; detector Node {detector}; seed family {board.world.seed} unit {board.credit.units[board.world.seed]}")
light = board.world.seed
t0 = time.time()
u_rows = []
share_rows = []
for step in range(intervals):
    board.step()
    if board.interval in (1, 10, 50, 100, 150, 200, 250, 300) or board.interval == intervals:
        u = w1lib.content_u(board)
        ls, _frozen = board.share_of(light)
        ls = np.asarray(ls, dtype=object).astype(float) / float(board.credit.units[light])
        body_share = float(w1lib.record_share(board, k, 0)[at]) if with_body else 0.0
        u_rows.append({"interval": board.interval, "U_body": float(u[at]), "U_det": float(u[detector]), "U_far": float(u[0, 0, 0]), "U_max": float(u.max()), "light_at_body": float(ls[at]), "light_at_det": float(ls[detector]), "light_max": float(ls.max()), "body_share_at_node": body_share, "body_quanta": float(w1lib.record_share(board, k, 0).sum()) if with_body else 0.0})
        r = u_rows[-1]
        n_credit = sum(1 for li in lines if li.get("event") == "credit")
        print(f"t {r['interval']:4d} U_body {r['U_body']:.4f} U_det {r['U_det']:.4f} U_far {r['U_far']:.4f} light@body {r['light_at_body']:.3f} light@det {r['light_at_det']:.3f} light_max {r['light_max']:.3f} body@node {r['body_share_at_node']:.3f} quanta {r['body_quanta']:.3f} credits {n_credit} ({time.time() - t0:.0f} s)")


def node_of(place: int) -> tuple[int, int, int]:
    return tuple(int(x) for x in np.unravel_index(int(place), shape))


def dist(a, b) -> int:
    return sum(min(abs(a[i] - b[i]), cube - abs(a[i] - b[i])) for i in range(3))


credits = [li for li in lines if li.get("event") == "credit"]
births = [li for li in lines if li.get("event") == "birth"]
refused = [li for li in lines if li.get("event") == "refused"]
by_node: dict[tuple, list] = defaultdict(list)
for li in credits:
    by_node[node_of(li["node_detector"])].append(li)
body_credits = [li for li in credits if li.get("realised") == name]
light_credits = [li for li in credits if li.get("realised") != name]
print(f"credits {len(credits)} (body's {len(body_credits)}, births' {len(light_credits)}), births {len(births)}, refused {len(refused)} by cause {Counter(li.get('cause') for li in refused)}")
own = [li for li in body_credits if node_of(li["node_detector"]) == at]
own_intervals = [li["interval"] for li in own]
own_proper = [li["proper"] for li in own]
print("body's clicks at its Node: intervals", own_intervals[:40], "proper", own_proper[:40])
print("body's clicks elsewhere:", Counter(node_of(li["node_detector"]) for li in body_credits if node_of(li["node_detector"]) != at))
spacing_board = np.diff(own_intervals).tolist() if len(own_intervals) > 1 else []
spacing_proper = np.diff(own_proper).tolist() if len(own_proper) > 1 else []
print("spacing of the body's clicks: board", spacing_board, "proper", spacing_proper)
beats = [li.get("beat") for li in own]
points = [li.get("point") for li in own]
print("the body's credit readings: beat", beats[:10], "point", points[:5], "windows", [li.get("windows") for li in own][:10])
by_distance: dict[int, list] = defaultdict(list)
for li in credits:
    by_distance[dist(node_of(li["node_detector"]), at)].append(li["interval"])
print("credits by distance from the body (count, first, last):", {d: (len(v), min(v), max(v)) for d, v in sorted(by_distance.items())})
det = by_node.get(detector, [])
det_intervals = [li["interval"] for li in det]
det_proper = [li["proper"] for li in det]
print(f"detector Node {detector}: {len(det)} credits at intervals {det_intervals[:40]} proper {det_proper[:40]} realised {Counter(li.get('realised') for li in det)}")
det_spacing = np.diff(det_intervals).tolist() if len(det_intervals) > 1 else []
first_births = sorted({li["interval"] for li in births})[:20]
print("birth intervals (first 20 distinct):", first_births, "birth Nodes:", Counter(tuple(li["nodes"][0]) for li in births).most_common(8))
u = w1lib.content_u(board)
ratio = math.exp(float(u[at]) - float(u[detector]))
summary = {
    "den": den, "with_body": with_body, "intervals": intervals, "family": [k, name, g], "body_node": list(at), "detector_node": list(detector),
    "credits": len(credits), "body_credits": len(body_credits), "birth_credits": len(light_credits), "births": len(births), "refused": len(refused),
    "refused_causes": dict(Counter(li.get("cause") for li in refused)),
    "own_click_intervals": own_intervals, "own_click_proper": own_proper, "own_spacing_board": spacing_board, "own_spacing_proper": spacing_proper,
    "own_beats": beats, "detector_intervals": det_intervals, "detector_proper": det_proper, "detector_spacing": det_spacing,
    "credits_by_distance": {str(d): len(v) for d, v in sorted(by_distance.items())},
    "U_body_end": float(u[at]), "U_det_end": float(u[detector]), "exp_dU": ratio,
    "mean_own_spacing_board": float(np.mean(spacing_board)) if spacing_board else None,
    "mean_own_spacing_proper": float(np.mean(spacing_proper)) if spacing_proper else None,
    "mean_det_spacing": float(np.mean(det_spacing)) if det_spacing else None,
    "u_rows": u_rows, "seconds": time.time() - t0,
}
print("SUMMARY", json.dumps({k2: v for k2, v in summary.items() if k2 not in ("u_rows",)}))
(out / f"{tag}.json").write_text(json.dumps({"summary": summary, "credits": credits[:400], "births": births[:200], "refused": refused[:200]}, indent=1, default=str), encoding="utf-8")
