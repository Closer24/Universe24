"""The retrace (CS6-S1) read from the record's Node lines (a reader, no act): at a top T every Node ends the interval at its pre-state exchanged, so X_T = X_(T-2) and the course is mirrored about T - 1: X(T - 1 + j) = X(T - 1 - j) at every Node for every j until the mirror of the last click before the top, 2 T - 2 - c for a click at the interval c; the first j where the mirror parts is measured against that prediction. Also the cube's size entering nowhere: two uniform records of different cubes compared on X per interval."""
import json
import sys

sys.set_int_max_str_digits(0)


def course(name):
    r = json.load(open("/dev/shm/tmp/ag2_" + name + ".json"))
    return r, {n["i"]: n["X"] for n in r["nodes"]}


def retrace(name):
    r, xs = course(name)
    count = len(r["nodes"][0]["X"])
    tops = [n["i"] for n in r["nodes"] if len(n["turned"]) == count]
    clicks = sorted(e["i"] for e in r["log"] if e["event"] in ("credit", "birth"))
    out = []
    for top in tops[:2]:
        centre = top - 1
        j = 1
        while centre - j >= 1 and centre + j in xs and xs[centre + j] == xs[centre - j]:
            j += 1
        before = [c for c in clicks if c < top]
        predicted = (2 * top - 2 - max(before)) if before else None
        out.append({"top": top, "mirror holds for j up to": j - 1, "parts at interval": centre + j if centre + j in xs else "end of record", "predicted parting (mirror of the last click before the top)": predicted, "clicks before the top": len(before)})
    return out


if __name__ == "__main__":
    for name in sys.argv[1:]:
        print(name, json.dumps(retrace(name)))
    for small, big in (("world_sea_3", "world_sea"), ("world_universe_3", "world_universe")):
        try:
            ra, xa = course(small)
            rb, xb = course(big)
        except FileNotFoundError:
            continue
        common = min(max(xa), max(xb))
        equal = [i for i in range(1, common + 1) if xa[i][0] == xb[i][0]]
        print(small, "against", big, "intervals compared", common, "X at the first Node equal at", len(equal), "intervals; first unequal", next((i for i in range(1, common + 1) if i not in set(equal)), None), "every Node alike on both", all(len(set(xa[i])) == 1 for i in xa) and all(len(set(xb[i])) == 1 for i in xb), "counts small/big credits", ra["counts"]["body_clicks"], rb["counts"]["body_clicks"], "laid back", ra["counts"]["laid_back"], rb["counts"]["laid_back"])
