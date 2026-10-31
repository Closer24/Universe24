"""Trace the pair world under B-edge past its ticks, rounds FROM..TO: the held counts, the tied first T1 rows, the held
dial's g on the out-edge, d_out = W(a) + W(a') + g_out, T's curvature 2 c |k|^2 against 4W. Whole numbers only.
Usage: python3 -I trace_fall.py <universe> <piece> <setting> FROM TO"""
import json, sys, runpy
from pathlib import Path
HERE = Path(__file__).resolve().parent.parent
FROM, TO = int(sys.argv[4]), int(sys.argv[5])
sys.argv = [str(HERE.joinpath("b_edge.py")), sys.argv[1], sys.argv[2], sys.argv[3], f"rounds=0", "noback"]
g = runpy.run_path(str(HERE.joinpath("b_edge.py")), run_name="b_edge_lib")
step, layout, s, H, T, gco, W, FOUR_W = g["step"], g["layout"], g["s0"], g["H"], g["T"], g["gco"], g["W"], g["FOUR_W"]
for n in range(1, TO + 1):
    s1 = step.tick(layout, s)
    if n >= FROM:
        go = gco(s.a, s1.a)
        h = [int(x) for x in s1.a[H, 0]]
        tg, tt = int(s1.a[2, 0]), int(s1.a[8, 0])
        d = 2 * W + int(go[H[0], 0])
        kt = 12000 * sum(x * x for x in h)
        print(f"round {n}: held {h}; giver row 2 {tg}, taker row 8 {tt}; g_out {int(go[H[0], 0])}; d_out {d}; T's curvature 2c|k|^2 {kt} against 4W {FOUR_W}", flush=True)
    s = s1
