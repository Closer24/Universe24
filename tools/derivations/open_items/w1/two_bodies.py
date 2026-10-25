"""Two bodies on one gapped line (hand w1, BRIEF_w (a)): two records of the point family with g nearest 0.83 (the heavy prime 617's lift at the 54-bit den), one quantum each, laid `sep` Links apart along z on the bare 7-cube torus with the light emptied (nothing else sources the held rows), run `intervals` intervals; per interval the two records' shares (quanta, in the record's own unit) with their share-weighted positions along z on the torus, their peak Nodes, the content U at the two lay Nodes and at the midpoint, the records' standing quanta (the leakage), the Link tensions' size; then the distance's least-squares slope over the run, and the run back by `step_inverse` to the laid state compared bit for bit (every array of every state, tests/laws_universe.node_arrays).

Usage: python two_bodies.py <den> <sep> <senseA> <senseB> <intervals> [runback 0|1] [light empty|sea]
"""

from __future__ import annotations

import json
import math
import sys
import time
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import w1lib  # noqa: E402

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))
from tests.laws_universe import node_arrays  # noqa: E402

den = int(sys.argv[1]) if len(sys.argv) > 1 else w1lib.DEN54
sep = int(sys.argv[2]) if len(sys.argv) > 2 else 2
sense_a = int(sys.argv[3]) if len(sys.argv) > 3 else 1
sense_b = int(sys.argv[4]) if len(sys.argv) > 4 else 1
intervals = int(sys.argv[5]) if len(sys.argv) > 5 else 300
runback = int(sys.argv[6]) if len(sys.argv) > 6 else 0
light = sys.argv[7] if len(sys.argv) > 7 else "empty"
cube = 7
tag = f"two_{den}_s{sep}_{sense_a:+d}{sense_b:+d}_{intervals}_{light}"
folder = Path("/dev/shm/tmp/w1") / tag
out = Path(__file__).resolve().parent / "out"
out.mkdir(exist_ok=True)

lines: list[dict] = []
board = w1lib.board_of(folder, den, cube, intervals, lines)
if light == "empty":
    w1lib.light_emptied(board)
k, name, num, den_k, g = w1lib.family_with_gap(board, 0.83)
board.born_point(k)
centre = cube // 2
at_a = (centre, centre, centre - sep // 2)
at_b = (centre, centre, at_a[2] + sep)
w1lib.lay_body(board, k, at_a, 0, sense_a)
w1lib.lay_body(board, k, at_b, 1, sense_b)
laid_state = node_arrays(board)
gamma = board.world.node_clock
print(f"family {k} {name!r} num {num} den {den_k} g {g:.4f}; bodies at {at_a} and {at_b}, senses {sense_a} {sense_b}; unit W_rec {board.credit.units[k]}")
shares0 = [w1lib.record_share(board, k, r) for r in (0, 1)]
print("laid quanta per record:", [float(s.sum()) for s in shares0], "at the lay Nodes:", [float(shares0[0][at_a]), float(shares0[1][at_b])])

rows = []
t0 = time.time()
mid = (centre, centre, (at_a[2] + at_b[2]) / 2)
for step in range(intervals):
    board.step()
    s = [w1lib.record_share(board, k, r) for r in (0, 1)]
    u = w1lib.content_u(board)
    pos = [w1lib.centroid(np.maximum(s[r], 0), 2, cube) for r in (0, 1)]
    si = [w1lib.record_share_int(board, k, r) for r in (0, 1)]
    pos_int = [w1lib.position_int(si[0], 2, at_a[2], cube), w1lib.position_int(si[1], 2, at_b[2], cube)]
    quanta_int = [divmod(int(sum(int(x) for x in si[r].reshape(-1))), int(board.credit.units[k])) for r in (0, 1)]
    peaks = [tuple(int(x) for x in np.unravel_index(int(np.argmax(s[r])), s[r].shape)) for r in (0, 1)]
    held = board.held[0]
    tensions = [int(np.abs(np.asarray(board.states[held].lines[1 + a].now, dtype=object)).max()) for a in range(3)]
    u_mid = float(u[centre, centre, int(math.floor(mid[2]))]) if sep % 2 == 0 else float((u[centre, centre, int(math.floor(mid[2]))] + u[centre, centre, int(math.ceil(mid[2]))]) / 2)
    rows.append({
        "interval": board.interval,
        "pos": pos,
        "pos_int": pos_int,
        "quanta_int": [[q, r] for q, r in quanta_int],
        "distance": w1lib.torus_distance(pos[0], pos[1], cube),
        "peaks": peaks,
        "peak_distance": w1lib.torus_distance(peaks[0][2], peaks[1][2], cube),
        "share_at_lay": [float(s[0][at_a]), float(s[1][at_b])],
        "share_at_peak": [float(s[0][peaks[0]]), float(s[1][peaks[1]])],
        "quanta": [float(s[0].sum()), float(s[1].sum())],
        "U_a": float(u[at_a]), "U_b": float(u[at_b]), "U_mid": u_mid,
        "U_max": float(u.max()),
        "U_far": float(u[0, 0, 0]),
        "tension_max": tensions,
        "turned": int(board.turned.sum()),
    })
    if board.interval in (1, 2, 5, 10, 20, 50, 100, 150, 200, 250, 300) or board.interval == intervals:
        r = rows[-1]
        print('   integer readings: pos_int (quotient, remainder, divisor) from the lay Nodes', r['pos_int'], 'quanta (whole, remainder)', r['quanta_int'])
        print(f"t {r['interval']:4d} pos {r['pos'][0]:.4f} {r['pos'][1]:.4f} dist {r['distance']:.4f} peaks {r['peaks'][0][2]} {r['peaks'][1][2]} share@lay {r['share_at_lay'][0]:.3f} {r['share_at_lay'][1]:.3f} quanta {r['quanta'][0]:.3f} {r['quanta'][1]:.3f} U_a {r['U_a']:.4f} U_mid {r['U_mid']:.4f} U_far {r['U_far']:.4f} tens {r['tension_max']} turned {r['turned']} ({time.time() - t0:.0f} s)")

ts = [r["interval"] for r in rows]
d = [r["distance"] for r in rows]
a_all, b_all = w1lib.slope(ts, d)
half = len(rows) // 2
a_late, b_late = w1lib.slope(ts[half:], d[half:])
a_early, _ = w1lib.slope(ts[:half], d[:half])
summary = {
    "den": den, "cube": cube, "light": light, "family": [k, name, num, den_k, g], "sep": sep, "senses": [sense_a, sense_b],
    "intervals": intervals, "distance_first": d[0], "distance_last": d[-1],
    "slope_all": a_all, "slope_first_half": a_early, "slope_second_half": a_late,
    "peak_distance_first": rows[0]["peak_distance"], "peak_distance_last": rows[-1]["peak_distance"],
    "quanta_last": rows[-1]["quanta"], "U_a_last": rows[-1]["U_a"], "U_mid_last": rows[-1]["U_mid"], "U_far_last": rows[-1]["U_far"],
    "credits": sum(1 for li in lines if li.get("event") == "credit"), "births": sum(1 for li in lines if li.get("event") == "birth"),
    "refused": sum(1 for li in lines if li.get("event") == "refused"),
    "seconds": time.time() - t0,
}
print("SUMMARY", json.dumps(summary))
(out / f"{tag}.json").write_text(json.dumps({"summary": summary, "rows": rows}, indent=1), encoding="utf-8")

if runback:
    t1 = time.time()
    for _ in range(intervals):
        board.step_inverse()
    back = node_arrays(board)
    same = set(back) == set(laid_state) and all(
        all(np.array_equal(np.asarray(x, dtype=object), np.asarray(y, dtype=object)) for x, y in zip(back[key], laid_state[key], strict=True))
        for key in laid_state
    )
    print(f"RUNBACK {'MATCH' if same else 'MISMATCH'} over {intervals} intervals back to the laid state, interval now {board.interval} ({time.time() - t1:.0f} s)")
    summary["runback"] = "MATCH" if same else "MISMATCH"
    (out / f"{tag}.json").write_text(json.dumps({"summary": summary, "rows": rows}, indent=1), encoding="utf-8")
