"""The period search on one record (sb1): the board's volume vector hashed at every interval, every pair of equal hashes named, and the mean's course, so a return to the first pair is read and not guessed."""
import hashlib
import json
import sys


def main(path):
    r = json.load(open(path))
    lines = r["nodes"]
    seen, repeats = {}, []
    means = []
    for line in lines:
        i = int(line["i"])
        xs = [int(x) for x in line["X"]]
        means.append((i, sum(xs) // len(xs), max(xs), min(xs), len(line.get("frozen", []))))
        key = hashlib.sha256(json.dumps(xs, separators=(",", ":")).encode("ascii")).hexdigest()
        if key in seen:
            repeats.append((seen[key], i))
        else:
            seen[key] = i
    print("record", path, "intervals", len(lines))
    print("the volume vector repeated at the pairs (first ten)", repeats[:10], "count", len(repeats))
    print("the mean at the first, middle and last interval", means[0], means[len(means) // 2], means[-1])
    print("the frozen Nodes, the largest over the record", max(m[4] for m in means))
    print("the content-bearing max X", max(m[2] for m in means), "the least min X", min(m[3] for m in means))


if __name__ == "__main__":
    for p in sys.argv[1:]:
        main(p)
        print("-" * 30)
