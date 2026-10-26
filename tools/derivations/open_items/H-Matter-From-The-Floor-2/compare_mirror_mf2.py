"""mf2: the births of a reflected world carried back through the reflection and compared with the base's (the kit's verdicts per birth: EQUAL the same take's Node, - and + ends and line_pair; CONJUGATE the ends exchanged; APART otherwise); the reflection a signed permutation given as e.g. z (z -> -z mod n) or x.
Usage: compare_mirror_mf2.py <base.json> <image.json> <axis letter> [n 4]"""
import json
import sys


def main():
    base = json.load(open(sys.argv[1]))
    image = json.load(open(sys.argv[2]))
    axis = "xyz".index(sys.argv[3])
    n = int(sys.argv[4]) if len(sys.argv) > 4 else 4

    def back(p):
        q = list(p)
        q[axis] = (n - q[axis]) % n
        return tuple(q)

    def key(e):
        return (e["i"], tuple(e["node"]), e["line_pair"], e["taken_row"])

    bb = {}
    for e in base["log"]:
        if e["event"] == "birth":
            bb.setdefault(key(e), []).append((tuple(e["minus"]), tuple(e["plus"])))
    verdict = {"EQUAL": 0, "CONJUGATE": 0, "APART": 0}
    first = {}
    per_row = {}
    for e in image["log"]:
        if e["event"] != "birth":
            continue
        k = (e["i"], back(e["node"]), e["line_pair"], e["taken_row"])
        ends = (back(e["minus"]), back(e["plus"]))
        found = bb.get(k, [])
        if ends in found:
            v = "EQUAL"
        elif (ends[1], ends[0]) in found:
            v = "CONJUGATE"
        else:
            v = "APART"
        verdict[v] += 1
        first.setdefault(v, e["i"])
        r = per_row.setdefault(str(e["taken_row"]), {"EQUAL": 0, "CONJUGATE": 0, "APART": 0})
        r[v] += 1
    nb = sum(1 for e in base["log"] if e["event"] == "birth")
    ni = sum(verdict.values())
    print(json.dumps({"base": sys.argv[1], "image": sys.argv[2], "axis": sys.argv[3], "base births": nb, "image births": ni, "verdicts": verdict, "first interval": first, "per taken row": per_row}))


main()
