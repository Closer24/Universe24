"""hr1: the fed one-Node stream read: per interval the centre's content, X, before, the write's quotient q = next - 2 now + before (next the level the step left: the before slot where the Node turned), the velocity, turned, frozen; the six neighbours' content; the board's content sum; the clicks at the centre and at its neighbours; the period of the centre's course; the run back. Usage: hr1_one_read.py <stream.jsonl> <out.json>"""
import json
import sys

sys.set_int_max_str_digits(0)
lines = [json.loads(l) for l in open(sys.argv[1])]
head, rows, tail = lines[0], [l for l in lines if "i" in l], next((l for l in lines if l.get("tail")), None)
centre, nb = tuple(head["centre"]), [tuple(p) for p in head["neighbours"]]
course = []
prev = None
for r in rows:
    nxt = r["Xb"] if r["turned"] else r["X"]
    q = None if prev is None else nxt - 2 * prev["X"] + prev["Xb"]
    course.append({"i": r["i"], "content": r["content"], "v": r["X"] - r["Xb"], "q": q, "turned": r["turned"], "frozen": r["frozen"], "frozen count": r["frozen count"], "nb content": r["neighbours content"], "board sum": sum(r["board content"]), "clock": r["clock increment"], "clicks": [(c["event"], list(c["node"]), int(c.get("levels", 0))) for c in r["clicks"]]})
    prev = r
contents = [c["content"] for c in course]
def period(seq):
    for p in range(1, 200):
        if len(seq) > 4 * p and all(seq[-k] == seq[-k - p] for k in range(1, 3 * p)):
            return p
    return None
clicks_centre = [c for r in rows for c in r["clicks"] if tuple(c["node"]) == centre]
clicks_nb = [c for r in rows for c in r["clicks"] if tuple(c["node"]) in nb]
clicks_all = [c for r in rows for c in r["clicks"]]
out = {
    "stream": sys.argv[1], "fed": {k: head[k] for k in ("content", "before", "frozen content", "X fed", "X before fed")}, "intervals": len(rows),
    "run back": tail["run back"] if tail else None, "counts": tail["counts"] if tail else None, "max transient": max(r["max transient"] for r in rows), "max state bits": max(r["state bits"] for r in rows),
    "frozen intervals": sum(1 for c in course if c["frozen"]), "turned intervals": sum(1 for c in course if c["turned"]), "frozen and turned": sum(1 for c in course if c["frozen"] and c["turned"]),
    "frozen twice in a row": sum(1 for a, b in zip(course, course[1:]) if a["frozen"] and b["frozen"]),
    "centre content min/max": [min(contents), max(contents)], "period of the centre's content (late)": period(contents),
    "centre content first 40": contents[:40], "centre content last 24": contents[-24:],
    "q abs max / |v| max": [max(abs(c["q"]) for c in course if c["q"] is not None), max(abs(c["v"]) for c in course)],
    "q at the frozen intervals (first 8)": [(c["i"], c["q"]) for c in course if c["frozen"]][:8],
    "q sum over the run": sum(c["q"] for c in course if c["q"] is not None),
    "neighbours content first/last": [course[0]["nb content"], course[-1]["nb content"]], "neighbours content min/max over the run": [min(min(c["nb content"]) for c in course), max(max(c["nb content"]) for c in course)],
    "board sum first/last/min/max": [course[0]["board sum"], course[-1]["board sum"], min(c["board sum"] for c in course), max(c["board sum"] for c in course)],
    "clock increments sum at centre": sum(c["clock"] for c in course),
    "clicks at centre": len(clicks_centre), "clicks at neighbours": len(clicks_nb), "clicks on the board": len(clicks_all),
    "clicks at centre by interval (first 10)": [(c["i"], c["event"]) for r in rows for c in r["clicks"] if tuple(c["node"]) == centre][:10],
    "clicks on the board last interval": max((c["i"] for c in clicks_all), default=None),
    "clicks per 500 intervals (board)": {str(k): sum(1 for c in clicks_all if k * 500 < c["i"] <= (k + 1) * 500) for k in range(len(rows) // 500 + 1)},
    "course": course[:40] + course[40::max(1, len(course) // 60)],
}
json.dump(out, open(sys.argv[2], "w"), default=str, indent=1)
print(json.dumps({k: v for k, v in out.items() if k != "course"}, default=str))
