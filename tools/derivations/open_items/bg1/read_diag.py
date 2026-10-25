"""bg1: the reader of diag.py's lines: the summary, the mean volume's tops and bottoms (a top where x_mean(i-1) <= x_mean(i) >= x_mean(i+1) with one strict and the run on both sides at least `run` long), the terms of the carrier's line at marks (mass, Links, write per Node to the unit, the forms by row per Node), the board-wide turns, and the retrace between two cycles (x_mean compared by the cycle's length). Usage: read_diag.py <out.jsonl> [marks i,i,...]"""
import json
import sys

lines = [json.loads(l) for l in open(sys.argv[1], encoding="utf-8")]
summary, rows = lines[0]["summary"], lines[1:]
nodes = 1
print("SUMMARY", json.dumps({k: v for k, v in summary.items() if k != "volume_mean_marks"}))
print("MARKS (i, volume mean, content min/mean/max):", summary["volume_mean_marks"])
xm = [r["x_mean"] for r in rows]
# the cube from the first mass_sum: mass per Node is at least 1 at X >= Gamma; take nodes from turned at a board-wide turn or from the world
world = json.load(open(sys.argv[1].replace("out/", "worlds/").split("_")[0] + ".json")) if False else None
tops, bottoms = [], []
for k in range(1, len(xm) - 1):
    if xm[k - 1] <= xm[k] >= xm[k + 1] and (xm[k - 1] < xm[k] or xm[k + 1] < xm[k]):
        tops.append((rows[k]["i"], xm[k]))
    if xm[k - 1] >= xm[k] <= xm[k + 1] and (xm[k - 1] > xm[k] or xm[k + 1] > xm[k]):
        bottoms.append((rows[k]["i"], xm[k]))
def runs(seq):
    found, start, sign = [], 0, 0
    for k in range(1, len(seq)):
        s = (seq[k] > seq[k - 1]) - (seq[k] < seq[k - 1])
        if s == 0:
            continue
        if s != sign:
            if sign != 0:
                found.append((sign, rows[start]["i"], rows[k - 1]["i"], seq[start], seq[k - 1]))
            start, sign = k - 1, s
    found.append((sign, rows[start]["i"], rows[-1]["i"], seq[start], seq[-1]))
    return found
long = [r for r in runs(xm) if r[2] - r[1] >= 20 or abs(r[4] - r[3]) >= 100]
print("RUNS of the mean volume (sign, from, to, X from, X to), the long ones:", long[:40])
print("TOPS of x_mean (i, X), first 12:", tops[:12], "count", len(tops))
print("BOTTOMS (i, X), first 12:", bottoms[:12], "count", len(bottoms))
board = [(r["i"], r["turned"]) for r in rows if r["turned"] > 0]
big = [t for t in board if t[1] >= max(x[1] for x in board) if board]
print("TURN EVENTS: intervals with a turn", len(board), "; the largest turns (i, Nodes):", sorted(board, key=lambda t: -t[1])[:8])
print("CONTENT MAX by 100s:", [(r["i"], r["content_max"]) for r in rows if r["i"] % 100 == 0 or r["i"] == 1])
marks = [int(x) for x in sys.argv[2].split(",")] if len(sys.argv) > 2 else [1, 10, 50, 100, 200, 300, 400, 600, 800, 1000, 1400, 1800, 2400]
print("TERMS at marks: i | x_mean x_max | mass links write (board sums) | forms_sum | trace p0^2 share | rows {name: [u_in u_out, (-aF) div w]} | turned | births body_clicks | transient bits")
for r in rows:
    if r["i"] in marks or r["i"] == rows[-1]["i"]:
        print(r["i"], "|", r["x_mean"], r["x_max"], "|", r["mass_sum"], r["links_sum"], r["write_sum"], "|", r["forms_sum"], "|", r["rows"], "|", r["turned"], "|", r["births"], r["body_clicks"], "|", r["transient_bits"], "| num bits", r["num_bits"], "| p0 min", r["p0_min"])
# the retrace between cycles: the intervals of board-wide turns
if len(board) >= 2:
    tops_i = [t[0] for t in sorted(board, key=lambda t: -t[1])[:6]]
    tops_i.sort()
    print("BOARD-WIDE TURNS at", tops_i)
    if len(tops_i) >= 2:
        L = tops_i[1] - tops_i[0]
        c1 = xm[tops_i[0] - 1 - L + 1: tops_i[0]] if tops_i[0] - L >= 0 else None
        a = xm[0:tops_i[0]]
        b = xm[tops_i[0]:tops_i[0] + len(a)]
        print("RETRACE: the rise to the first turn", len(a), "intervals; the fall after it compared mirrored:", sum(1 for u, v in zip(a, reversed(b)) if u == v), "of", min(len(a), len(b)), "equal; cycle 1 against cycle 2 (length", L, "):", sum(1 for k in range(min(L, len(xm) - L)) if xm[k] == xm[k + L]), "of", min(L, len(xm) - L), "equal")
