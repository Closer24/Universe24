"""Addition 2 (the detector from the seed alone): a reader of a record's log, no run. A standing body at a Node is a record row's credit there (the body's beat the credit's); its origin is the latest birth of that row with an end inside the past cone of the credit (one Link per interval on the torus). A born child's click is the first credit of its row at its end after the birth (the Bell reader's). The click is a measurement click where a body of another row stands at that Node at the click (a credit of that row at the Node within its beat of the click's interval) whose origin birth and the pair's birth lie outside each other's cones (the torus distance above the interval difference); the spontaneous clicks (no such body) are the control. The outcome: the child's sense (a plane child carries no axis) or, for a quartet child, the sign of its axial on the body's axis (a quartet body's dominant axis; a plane body's none: the sense as the setting); the setting the body's sense or axis sign. The cells over the pairs measured at both ends, S as [num, den]; integers only.
Usage: python measure_from_seed.py <record.json> <out.json>"""
import json
import sys
from collections import Counter, defaultdict


def sign(x):
    return (x > 0) - (x < 0)


def dist(a, b, cube):
    return sum(min((x - y) % cube, (y - x) % cube) for x, y in zip(a, b))


def main():
    rec = json.load(open(sys.argv[1]))
    cube, log = int(rec["cube"]), rec["log"]
    births = [x for x in log if x["event"] == "birth"]
    credits = [x for x in log if x["event"] == "credit"]
    by_node_row = defaultdict(list)
    for c in credits:
        by_node_row[(tuple(c["node"]), int(c["line"]))].append(c)
    births_by_row = defaultdict(list)
    for b in births:
        births_by_row[int(b["line_pair"])].append(b)

    def origin_of(p, i, row):
        found = None
        for b in births_by_row[row]:
            if int(b["i"]) >= i:
                break
            for end in ("minus", "plus"):
                if dist(tuple(b[end]), p, cube) <= i - int(b["i"]):
                    found = b
        return found

    def first_click(where, row, after):
        for c in by_node_row.get((tuple(where), row), []):
            if int(c["i"]) > after:
                return c
        return None

    def bodies_at(p, i, row_c):
        found = []
        for (q, row), cs in by_node_row.items():
            if q != p or row == row_c:
                continue
            near = min(cs, key=lambda c: abs(int(c["i"]) - i))
            if abs(int(near["i"]) - i) <= max(int(near["beat"]), 1):
                found.append((row, near))
        return found

    out = {"record": sys.argv[1], "births": len(births), "credits": len(credits), "cube": cube}
    kinds = Counter()
    cells = defaultdict(Counter)
    cells_ctrl = defaultdict(Counter)
    examples = []
    for b in births:
        s, i_b = int(b["line_pair"]), int(b["i"])
        ends = []
        for end in ("minus", "plus"):
            c = first_click(b[end], s, i_b)
            if c is None:
                ends.append(None)
                continue
            p, i_c = tuple(c["node"]), int(c["i"])
            measured = None
            for row_b, cb in bodies_at(p, i_c, s):
                ob = origin_of(p, int(cb["i"]), row_b)
                independent = ob is not None and dist(tuple(ob["node"]), tuple(b["node"]), cube) > abs(int(ob["i"]) - i_b)
                kinds["body at the click (any root)"] += 1
                if independent:
                    measured = (row_b, cb, ob)
                    break
            if measured is None:
                kinds["spontaneous click (no independent body)"] += 1
                ends.append(("spont", c))
            else:
                kinds["measurement click (independent body)"] += 1
                row_b, cb, ob = measured
                frame_b = cb["frame"]
                if "axial" in c["frame"] and "axial" in frame_b:
                    ax = max(range(3), key=lambda k: abs(int(frame_b["axial"][k])))
                    outcome, setting = sign(int(c["frame"]["axial"][ax])), sign(int(frame_b["axial"][ax]))
                else:
                    outcome, setting = int(c["sense"]), int(cb["sense"])
                ends.append(("meas", c, outcome, setting))
                if len(examples) < 5:
                    examples.append({"pair birth": [i_b, b["node"]], "end": end, "click": [i_c, list(p)], "body row": row_b, "body credit i": int(cb["i"]), "body origin": [int(ob["i"]), ob["node"]], "outcome": outcome, "setting": setting})
        if all(e is not None and e[0] == "meas" for e in ends):
            kinds["pairs measured at both ends"] += 1
            (_, c1, o1, a), (_, c2, o2, bb) = ends
            if 0 not in (o1, o2, a, bb):
                cells[(a, bb)][o1 * o2] += 1
        elif all(e is not None and e[0] == "spont" for e in ends):
            kinds["pairs spontaneous at both ends"] += 1
            o1, o2 = int(ends[0][1]["sense"]), int(ends[1][1]["sense"])
            a, bb = (1 if ends[0][1]["turned"] else -1), (1 if ends[1][1]["turned"] else -1)
            if 0 not in (o1, o2):
                cells_ctrl[(a, bb)][o1 * o2] += 1
        elif all(e is not None for e in ends):
            kinds["pairs measured at one end"] += 1
    sys.path.insert(0, "/dev/shm/tmp/qc1/src_qc1")
    sys.path.insert(0, sys.argv[0].rsplit("/", 1)[0])
    from hq_reader import s_of
    out["clicks by kind"] = dict(kinds)
    out["cells (measured pairs)"] = s_of(cells)
    out["cells (spontaneous pairs, the control: the sense by the turned bit)"] = s_of(cells_ctrl)
    out["examples"] = examples
    json.dump(out, open(sys.argv[2], "w"), indent=1)
    print(json.dumps({k: v for k, v in out.items() if k != "examples"}))


if __name__ == "__main__":
    main()
