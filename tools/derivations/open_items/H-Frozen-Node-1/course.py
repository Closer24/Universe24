"""bh1: the course of a record at its deepest Node, read from the record's own Node lines and reader rows (integers only).

Usage: course.py <record.json> [every]
Prints: the record's counts and run back; per interval (every `every`, default 50, and the last): the max content, the Node that holds it
and its X (bits), the count of frozen Nodes (the Link pace 0), the Links held at the wall (the factor 0), the turned Nodes;
the reader rows' max transient bits, max state bits, links at the wall, births, body clicks; the content at the doublings of the
interval (the log law's reading: c(2t) - c(t) constant where c grows as A ln t); the first interval at which the max content passes
each hundred, as a table.
"""
import json, sys


def main(argv):
    sys.set_int_max_str_digits(0)
    rec = json.load(open(argv[1]))
    every = int(argv[2]) if len(argv) > 2 else 50
    nodes = rec["nodes"]
    rows = rec["rows"]
    print("counts:", rec["counts"])
    print("run back:", rec["run_back"])
    print("intervals:", rec["intervals"], "cube:", rec["cube"], "den:", rec["den"])
    print("reader rows (i, max bits, max transient bits, links at the wall, turns, births, body_clicks, volume mean, content min/mean/max):")
    for r in rows:
        print("  ", r["i"], r["max bits"], r["max transient bits"], r["links at the wall"], r["turns"], r["births"], r["body_clicks"], r["volume mean"], r["content min/mean/max"])
    print("course (i, cmax, node index, X at it, X bits, frozen count, held Links, turned count):")
    course = []
    for line in nodes:
        c = line["content"]
        k = max(range(len(c)), key=lambda j: c[j])
        x = int(line["X"][k])
        course.append((line["i"], c[k], k, x, x.bit_length(), len(line["frozen"]), len(line["held"]), len(line["turned"])))
    for row in course:
        if row[0] % every == 0 or row[0] == course[-1][0] or row[0] == 1:
            print("  ", row)
    n = len(course)
    print("content at the doublings (t, cmax, cmax(2t) - cmax(t)):")
    t = 25
    while 2 * t <= n:
        c1, c2 = course[t - 1][1], course[2 * t - 1][1]
        print("  ", t, c1, 2 * t, c2, c2 - c1)
        t *= 2
    print("first interval at which the max content passes each hundred:")
    passed = 0
    found = []
    for row in course:
        while row[1] >= passed + 100:
            passed += 100
            found.append((passed, row[0]))
    print("  ", found)
    held_first = next((row[0] for row in course if row[6] > 0), None)
    frozen_first = next((row[0] for row in course if row[5] > 0), None)
    print("first interval with a Link held at the wall:", held_first, "; first frozen Node:", frozen_first)
    print("max held Links over the run:", max(row[6] for row in course), "max frozen:", max(row[5] for row in course))
    # the deepest Node's X course: its velocity v = X_t - X_{t-1} at the end, in bits
    k_end = course[-1][2]
    xs = [int(line["X"][k_end]) for line in nodes]
    cs = [line["content"][k_end] for line in nodes]
    print("the deepest Node at the end (index %d): content at every %d intervals:" % (k_end, every), [cs[i] for i in range(0, n, every)] + [cs[-1]])
    print("its X at the end", xs[-1], "bits", xs[-1].bit_length(), "; v at the end", xs[-1] - xs[-2], "; v at the middle", xs[n // 2] - xs[n // 2 - 1])
    # the clicks at the deepest Node and the last credit's interval, the credits' spacing at that Node (the stopped clock's reading)
    log = rec["log"]
    cube = rec["cube"]
    at = (k_end // (cube * cube), (k_end // cube) % cube, k_end % cube)
    credits = [e for e in log if e["event"] == "credit" and tuple(e["node"]) == at]
    births = [e for e in log if e["event"] == "birth" and tuple(e["node"]) == at]
    print("the deepest Node", at, ": credits", len(credits), "births", len(births))
    if credits:
        spac = [b["i"] - a["i"] for a, b in zip(credits, credits[1:])]
        print("  credit intervals (first 8, last 8):", [c["i"] for c in credits][:8], [c["i"] for c in credits][-8:])
        print("  spacings in board intervals (first 8, last 8):", spac[:8], spac[-8:])
        print("  the contents at the credits (first 4, last 4):", [c["content"] for c in credits][:4], [c["content"] for c in credits][-4:])
        print("  proper at the credits (last 4):", [c["proper"] for c in credits][-4:], "beats (last 4):", [c["beat"] for c in credits][-4:])
    all_credits = [e for e in log if e["event"] == "credit"]
    print("credits in the record:", len(all_credits), "; the deepest content at a credit:", max((e["content"] for e in all_credits), default=None))


if __name__ == "__main__":
    main(sys.argv)
