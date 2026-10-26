"""bb2: the reader of a run.py record (the engine's own record, nothing fed): per interval the mean X, min, max, the neighbours' spread in thousandths (max over the Links), the Links at or above the threshold, the turned count; then the summary: the runs of the mean (tops and bottoms), the exact returns (every Node at the seed's X), the intervals where every Node turned at once, the births by interval, the counts, the bits, the run back. Integers only.

Usage: read_record.py <out.json> [threshold] [marks: comma list of intervals]
"""
import json
import sys


def neighbours(cube):
    n = cube ** 3
    found = []
    for i in range(n):
        x, y, z = i // (cube * cube), (i // cube) % cube, i % cube
        for a, (dx, dy, dz) in enumerate(((1, 0, 0), (0, 1, 0), (0, 0, 1))):
            j = ((x + dx) % cube) * cube * cube + ((y + dy) % cube) * cube + (z + dz) % cube
            found.append((i, j))
    return found


def main(argv):
    sys.set_int_max_str_digits(0)
    r = json.load(open(argv[1]))
    threshold = int(argv[2]) if len(argv) > 2 else 63
    marks = [int(m) for m in argv[3].split(",")] if len(argv) > 3 else []
    cube = r["cube"]
    n = cube ** 3
    links = neighbours(cube)
    seed = None
    means, at_seed, turned_all, e_rows = [], [], [], []
    for line in r["nodes"]:
        xs = line["X"]
        if seed is None:
            seed = r["gamma"]
        i = line["i"]
        mean = sum(xs) // n
        e_max, above = 0, 0
        for a, b in links:
            lo = min(xs[a], xs[b])
            e = (1000 * abs(xs[a] - xs[b])) // lo if lo > 0 else 10 ** 9
            e_max = max(e_max, e)
            above += e >= threshold
        means.append((i, mean, min(xs), max(xs), e_max, above, len(line["turned"]), len(line["frozen"])))
        if all(x == seed for x in xs):
            at_seed.append(i)
        if len(line["turned"]) == n:
            turned_all.append(i)
    runs = []
    direction = 0
    start = means[0]
    for k in range(1, len(means)):
        d = (means[k][1] > means[k - 1][1]) - (means[k][1] < means[k - 1][1])
        if d != 0 and d != direction:
            if direction != 0:
                runs.append((("rise" if direction > 0 else "fall"), start[0], start[1], means[k - 1][0], means[k - 1][1]))
            direction = d
            start = means[k - 1]
    runs.append((("rise" if direction > 0 else "fall"), start[0], start[1], means[-1][0], means[-1][1]))
    long_runs = [x for x in runs if x[3] - x[1] >= 5]
    births = {}
    for ev in r["log"]:
        if ev.get("event") == "birth":
            births[ev["i"]] = births.get(ev["i"], 0) + 1
    e_course = [(m[0], m[4], m[5]) for m in means if m[0] in marks or m[0] in (1, 2, 5, 10, 20, 40, 58, 80, 100, 115, 116, 130, 150, 173, 200, 230, 231, 260, 288, 300, 345, 346, 400)]
    first_above = next((m[0] for m in means if m[4] >= threshold), None)
    print(json.dumps({
        "world": r["world"].get("seed"), "cube": cube, "intervals": r["intervals"],
        "long runs of the mean (kind, from i, X, to i, X)": long_runs[:16],
        "exact returns (every Node at the seed's X)": at_seed[:20],
        "every Node turned at once at": turned_all[:20],
        "e max / Links above threshold at marks": e_course,
        "e max over the run": max(m[4] for m in means), "first interval with e >= threshold": first_above,
        "mean at marks": [(m[0], m[1], m[2], m[3]) for m in means if m[0] in marks or m[0] in (1, 58, 100, 115, 116, 173, 200, 230, 231, 288, 300, 345, 346, 400)],
        "births by interval": births, "counts": r["counts"], "run back": r["run_back"],
        "integers / state bits / transient bits": [r["rows"][-1]["integers"], r["rows"][-1]["max bits"], r["rows"][-1]["max transient bits"]],
        "frozen max": max(m[7] for m in means),
    }))


if __name__ == "__main__":
    main(sys.argv)
