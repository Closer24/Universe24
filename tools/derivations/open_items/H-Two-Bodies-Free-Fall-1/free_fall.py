"""Free fall in a hand-laid well (hand w1, gate 13): the bare 7-cube torus at the 54-bit den with the light emptied, the volume holder's time line set by hand (tests/laws_universe.time_line_set) to the volume X = Gamma e^(4 U) of a hollow U(r) = U0 e^(-r / R) about the Node `well` (r the torus distance in Links), both levels alike; one body (one quantum of the point family with g nearest 0.83, or `count` quanta) laid `off` Links from the well's centre along z; per interval the body's share-weighted position along z, its peak Node, its share at the lay Node and at the well's centre, U at the lay Node, at the centre and the gradient across the lay Node; the position's slope and its second difference (the acceleration), against the law's free-packet line a = Delta |d omega / d c| grad c with Delta = (num / (3 den)) / sin omega_0 and d omega / dc = 2 g e^(-2U) / (Gamma sin omega) at the lay Node.

Usage: python free_fall.py <den> <U0> <R> <off> <intervals> [count]
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
from tests.laws_universe import time_line_set  # noqa: E402

den = int(sys.argv[1]) if len(sys.argv) > 1 else w1lib.DEN54
u0 = float(sys.argv[2]) if len(sys.argv) > 2 else 0.3
radius = float(sys.argv[3]) if len(sys.argv) > 3 else 2.0
off = int(sys.argv[4]) if len(sys.argv) > 4 else 3
intervals = int(sys.argv[5]) if len(sys.argv) > 5 else 200
count = int(sys.argv[6]) if len(sys.argv) > 6 else 1
cube = 7
tag = f"fall_{den}_U{u0}_R{radius}_off{off}_{intervals}_c{count}"
folder = Path("/dev/shm/tmp/w1") / tag
out = Path(__file__).resolve().parent / "out"
out.mkdir(exist_ok=True)

lines: list[dict] = []
board = w1lib.board_of(folder, den, cube, intervals, lines)
w1lib.light_emptied(board)
gamma = board.world.node_clock
centre = cube // 2
well = (centre, centre, centre)
coords = np.indices(board.shape)
r = np.zeros(board.shape)
for axis in range(3):
    d = np.abs(coords[axis] - well[axis])
    r += np.minimum(d, cube - d) ** 2
r = np.sqrt(r)
u_hand = u0 * np.exp(-r / radius)
x_hand = np.vectorize(lambda u: int(round(gamma * math.exp(4 * u))), otypes=[object])(u_hand)
time_line_set(board, x_hand, x_hand.copy())
k, name, num, den_k, g = w1lib.family_with_gap(board, 0.83)
board.born_point(k)
at = (centre, centre, (centre - off) % cube)
w1lib.lay_body(board, k, at, 0, 1, count)
u_start = w1lib.content_u(board)
omega0 = math.acos(num / den_k)
delta = (num / (3 * den_k)) / math.sin(omega0)
print(f"family {k} {name!r} g {g:.4f} omega0 {omega0:.4f} Delta {delta:.5f}; well at {well} U0 {u0} R {radius}; body ({count} quanta) at {at}, U there {u_start[at]:.4f}, U at centre {u_start[well]:.4f}")
rows = []
t0 = time.time()
for step in range(intervals):
    board.step()
    s = np.maximum(w1lib.record_share(board, k, 0), 0)
    u = w1lib.content_u(board)
    pos = w1lib.centroid(s, 2, cube)
    peak = tuple(int(x) for x in np.unravel_index(int(np.argmax(s)), s.shape))
    za, zm, zp = (at[2] - 1) % cube, at[2], (at[2] + 1) % cube
    grad_u = (float(u[centre, centre, zp]) - float(u[centre, centre, za])) / 2
    rows.append({"interval": board.interval, "pos": pos, "pos_rel": w1lib.torus_distance(pos, well[2], cube), "peak": peak, "share_at_lay": float(s[at]), "share_at_centre": float(s[well]), "quanta": float(s.sum()), "U_lay": float(u[at]), "U_centre": float(u[well]), "gradU_at_lay": grad_u, "turned": int(board.turned.sum())})
    if board.interval in (1, 2, 5, 10, 20, 30, 50, 75, 100, 150, 200, 250, 300) or board.interval == intervals:
        rr = rows[-1]
        print(f"t {rr['interval']:4d} pos {rr['pos']:.4f} (to centre {rr['pos_rel']:.4f}) peak {rr['peak'][2]} share@lay {rr['share_at_lay']:.3f} @centre {rr['share_at_centre']:.3f} quanta {rr['quanta']:.3f} U_lay {rr['U_lay']:.4f} U_centre {rr['U_centre']:.4f} gradU {rr['gradU_at_lay']:+.4f} turned {rr['turned']} ({time.time() - t0:.0f} s)")
ts = [x["interval"] for x in rows]
pr = [x["pos_rel"] for x in rows]
a_all, _ = w1lib.slope(ts, pr)
n = len(rows)
a_1, _ = w1lib.slope(ts[: n // 3], pr[: n // 3])
a_2, _ = w1lib.slope(ts[n // 3 : 2 * n // 3], pr[n // 3 : 2 * n // 3])
a_3, _ = w1lib.slope(ts[2 * n // 3 :], pr[2 * n // 3 :])
# the law's free-packet line at the start: a = Delta |d omega / dc| grad c, grad c = Gamma grad U / ln(1 / (1 - 1 / Gamma)) levels per Link
u_at = float(u_start[at])
cos_w = 1 - g * math.exp(-2 * u_at)
sin_w = math.sqrt(max(0.0, 1 - cos_w * cos_w))
domega_dc = 2 * g * math.exp(-2 * u_at) / (gamma * sin_w) if sin_w else float("nan")
grad_c0 = rows[0]["gradU_at_lay"] / (-math.log(1 - 1 / gamma))
a_law = delta * domega_dc * grad_c0
summary = {"den": den, "family": [k, name, g], "U0": u0, "R": radius, "off": off, "count": count, "intervals": intervals, "pos_rel_first": pr[0], "pos_rel_last": pr[-1], "slope_all": a_all, "slope_thirds": [a_1, a_2, a_3], "peak_first": rows[0]["peak"], "peak_last": rows[-1]["peak"], "quanta_last": rows[-1]["quanta"], "share_at_lay_last": rows[-1]["share_at_lay"], "U_lay_first": rows[0]["U_lay"], "U_lay_last": rows[-1]["U_lay"], "U_centre_last": rows[-1]["U_centre"], "gradU_first": rows[0]["gradU_at_lay"], "law_free_packet_acceleration": a_law, "law_displacement_over_run": 0.5 * a_law * intervals ** 2, "Delta": delta, "domega_dc": domega_dc, "seconds": time.time() - t0}
print("SUMMARY", json.dumps(summary))
(out / f"{tag}.json").write_text(json.dumps({"summary": summary, "rows": rows}, indent=1), encoding="utf-8")
