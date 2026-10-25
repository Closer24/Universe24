"""bb2: the 48 on the board read from a run.py record: for a seed symmetric about the centre of the cube, X and the content at every interval are compared under every one of the 48 cube symmetries (24 rotations, 24 reflections) about the centre; the count of (interval, element) pairs equal and apart. The clicks' 48 on a record with no click is the board's. Integers only.
Usage: check48.py <out.json>
"""
import itertools
import json
import sys


def elements():
    found = []
    for perm in itertools.permutations(range(3)):
        for signs in itertools.product((1, -1), repeat=3):
            found.append((perm, signs))
    return found


def main(argv):
    r = json.load(open(argv[1]))
    cube = r["cube"]
    c = cube // 2
    n = cube ** 3
    els = elements()
    maps = []
    for perm, signs in els:
        m = []
        for i in range(n):
            v = (i // (cube * cube) - c, (i // cube) % cube - c, i % cube - c)
            w = [signs[a] * v[perm[a]] for a in range(3)]
            m.append(((w[0] + c) % cube) * cube * cube + ((w[1] + c) % cube) * cube + (w[2] + c) % cube)
        maps.append(m)
    equal_x = apart_x = equal_c = apart_c = 0
    first_apart = None
    for line in r["nodes"]:
        xs, cs = line["X"], line["content"]
        for m in maps:
            ok_x = all(xs[m[i]] == xs[i] for i in range(n))
            ok_c = all(cs[m[i]] == cs[i] for i in range(n))
            equal_x += ok_x
            apart_x += not ok_x
            equal_c += ok_c
            apart_c += not ok_c
            if not ok_x and first_apart is None:
                first_apart = line["i"]
    print(json.dumps({"world": r["world"]["seed"][:3], "elements": len(els), "intervals": len(r["nodes"]),
                      "X equal / apart": [equal_x, apart_x], "content equal / apart": [equal_c, apart_c],
                      "first interval apart": first_apart, "births": r["counts"]["births"]}))


if __name__ == "__main__":
    main(sys.argv)
