"""hp2: the cycle's reading of a probe stream: the frozen count per interval (its histogram and max), the intervals where every Node is frozen, the turn count there, the X per Node after such an interval, the board's content sum over time, the clicks. Usage: hp2_cycle.py <probe.jsonl> [every]"""
import json
import sys

sys.set_int_max_str_digits(0)
L = [json.loads(l) for l in open(sys.argv[1])]
head = L[0]; body = [l for l in L[1:] if not l.get("tail")]; tail = L[-1] if L[-1].get("tail") else None
N = 1
for s in head["shape"]: N *= s
every = int(sys.argv[2]) if len(sys.argv) > 2 else 50
fc = [len(l["frozen"]) for l in body]
hist = {}
for f in fc: hist[f] = hist.get(f, 0) + 1
allf = [l["i"] for l in body if len(l["frozen"]) == N]
print("world", head["world"].split("/")[-1], "Nodes", N, "intervals", len(body), "run back", tail and tail["run back"], "max transient", max(l["max transient"] for l in body), "state bits", max(l["state bits"] for l in body))
print("frozen count per interval: max", max(fc), "histogram", dict(sorted(hist.items())))
print("intervals with every Node frozen:", len(allf), allf[:20])
if allf:
    i0 = allf[0]
    for l in [l for l in body if l["i"] in (i0, i0 + 1, i0 + 2, i0 + 3)]:
        xs = sorted(set(l["X_watch"].values()))
        print("  i", l["i"], "frozen", len(l["frozen"]), "turned", len(l["turned"]), "content sum", l["board_content_sum"], "distinct X", len(xs), "X min/max", xs[0], xs[-1])
turns = [(l["i"], len(l["turned"])) for l in body]
print("turn count per interval: max", max(t for _, t in turns), "intervals with every Node turned", [i for i, t in turns if t == N][:10])
print("board content sum, frozen, turned, ever, clicks at every", every, ":", [(l["i"], l["board_content_sum"], len(l["frozen"]), len(l["turned"]), l["ever"], len(l["clicks"])) for l in body if l["i"] % every == 0 or l["i"] == len(body)])
first = next((l["i"] for l in body if l["frozen"]), None)
print("first freeze", first, "clicks from it on", sum(len(l["clicks"]) for l in body if first is not None and l["i"] >= first), "clicks in all", sum(len(l["clicks"]) for l in body), "last click", max((l["i"] for l in body if l["clicks"]), default=None))
if first:
    aft = [l for l in body if l["i"] >= first]
    xs_end = sorted(set(aft[-1]["X_watch"].values()))
    print("at the end: watch Nodes", len(aft[-1]["X_watch"]), "distinct X", len(xs_end), "X min/max", xs_end[0], xs_end[-1], "contents min/max", min(aft[-1]["content_watch"].values()), max(aft[-1]["content_watch"].values()))
if tail: print("counts", tail["counts"])
