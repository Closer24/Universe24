"""The angular momentum and momentum of the clicks under the six-Link lay, read on the click lines alone (H-Birth-On-Six-Links-2): integers only, doubled coordinates (2J, 2r), the centre (cube - 1) per doubled axis. Per credit: (2r - 2c) x dP_take. Per take (a birth line or several at one Node, then its `six` line): the taker's moment, the children's lays' moments (the ends' lays booked under dP_lay_ends where present, at the + end otherwise), the six ends' lays' moments at their own Nodes; the balance of the take (0 where J is conserved at the event) and of P. Totals: the clicks' J2 and P by class and summed; the maximum laid integer; the charges W summed; the per-interval moments. Usage: sl2_moment.py <record.json> [cx,cy,cz]"""
import json
import sys

sys.set_int_max_str_digits(0)
Z = [0, 0, 0]


def cross(u, v):
    return [u[1] * v[2] - u[2] * v[1], u[2] * v[0] - u[0] * v[2], u[0] * v[1] - u[1] * v[0]]


def add(u, v):
    return [a + b for a, b in zip(u, v, strict=True)]


def arm(where, c2):
    return [2 * x - c for x, c in zip(where, c2, strict=True)]


def arm_from(at, where, c2, cube):
    """The arm of an end of one of the Node's Links: the Node's arm plus the Link's own vector (the torus unwrapped about the Node, so the end one Link from the Node is read one Link from it)."""
    d = [((w - a + cube // 2) % cube) - cube // 2 for w, a in zip(where, at, strict=True)]
    return [x + 2 * e for x, e in zip(arm(at, c2), d, strict=True)]


def ints(v):
    return [int(x) for x in v]


def read(record, c2=None):
    log = record["log"]
    cube = int(record["cube"])
    if c2 is None:
        c2 = [cube - 1] * 3
    J = {"credits": list(Z), "takes": list(Z), "children": list(Z), "six": list(Z)}
    P = {k: list(Z) for k in J}
    n = {"credits": 0, "credits laid back": 0, "births": 0, "takes": 0, "six lines": 0, "six solved": 0, "six closed": 0, "six open (remainder named)": 0,
         "takes with J balance 0 about the centre": 0, "takes with P balance 0": 0, "births: W_children summing 0": 0, "births: dP_lay 0": 0, "mergers": 0}
    max_laid, max_level_bits = 0, 0
    per_i = {}
    open_rem = []
    pending = {}
    worst = 0
    for e in log:
        kind = e.get("event")
        if kind == "credit":
            dp = ints(e["dP_take"])
            m = cross(arm(e["node"], c2), dp)
            n["credits"] += 1
            n["credits laid back"] += "laid_back" in e
            J["credits"], P["credits"] = add(J["credits"], m), add(P["credits"], dp)
        elif kind == "birth":
            key = (int(e["i"]), tuple(e["node"]), int(e["taken_row"]))
            n["births"] += 1
            n["mergers"] += "takes" in e
            n["births: W_children summing 0"] += sum(int(w) for w in e["W_children"]) == 0
            dpl = ints(e["dP_lay"])
            n["births: dP_lay 0"] += dpl == Z
            ends = e.get("dP_lay_ends")
            if ends is not None:
                ml = list(Z)
                for where, dpe in zip((e["minus"], e["plus"]), ends, strict=True):
                    ml = add(ml, cross(arm_from(e["node"], where, c2, cube), ints(dpe)))
            else:
                ml = cross(arm_from(e["node"], e["plus"], c2, cube), dpl)
            grp = pending.setdefault(key, {"mt": list(Z), "dpt": list(Z), "ml": list(Z), "dpl": list(Z), "taken": False})
            if not grp["taken"]:
                takes = [(t["node"], ints(t["dP_take"])) for t in e["takes"]] if "takes" in e else [(e["node"], ints(e["dP_take"]))]
                for where, dp in takes:
                    grp["mt"] = add(grp["mt"], cross(arm(where, c2), dp))
                    grp["dpt"] = add(grp["dpt"], dp)
                grp["taken"] = True
            grp["ml"], grp["dpl"] = add(grp["ml"], ml), add(grp["dpl"], dpl)
            m = add(cross(arm(e["node"], c2), ints(e["dP_take"])) if not pending.get(("counted", key)) else Z, ml)
            pending[("counted", key)] = True
            continue
        elif kind == "six":
            key = (int(e["i"]), tuple(e["node"]), int(e["taken_row"]))
            n["six lines"] += 1
            n["six solved"] += bool(e.get("solved"))
            n["six closed"] += bool(e.get("closed"))
            if not e.get("closed"):
                n["six open (remainder named)"] += 1
                open_rem.append({"i": e["i"], "node": e["node"], "solved": e.get("solved"), "remainder": e.get("remainder"), "bits_ok": e.get("bits_ok", None), "target_P": e["target_P"]})
            if e.get("lays"):
                max_laid = max(max_laid, max(abs(int(v)) for l_ in e["lays"] for v in l_))
            ms, dps = list(Z), list(Z)
            for j, dpe in zip(e["ends"], e.get("dP_ends", []), strict=False):
                if e.get("lays"):
                    ms = add(ms, cross(arm_from(e["node"], j, c2, cube), ints(dpe)))
                    dps = add(dps, ints(dpe))
            grp = pending.pop(key, {"mt": list(Z), "dpt": list(Z), "ml": list(Z), "dpl": list(Z)})
            pending.pop(("counted", key), None)
            n["takes"] += 1
            J["takes"], J["children"], J["six"] = add(J["takes"], grp["mt"]), add(J["children"], grp["ml"]), add(J["six"], ms)
            P["takes"], P["children"], P["six"] = add(P["takes"], grp["dpt"]), add(P["children"], grp["dpl"]), add(P["six"], dps)
            bal = add(add(grp["mt"], grp["ml"]), ms)
            pbal = add(add(grp["dpt"], grp["dpl"]), dps)
            n["takes with J balance 0 about the centre"] += bal == Z
            n["takes with P balance 0"] += pbal == Z
            worst = max(worst, max(abs(x) for x in bal))
            m = bal
        else:
            continue
        per_i[int(e["i"])] = add(per_i.get(int(e["i"]), Z), m)
    for key, grp in list(pending.items()):
        if key[0] == "counted":
            continue
        n["takes"] += 1
        J["takes"], J["children"] = add(J["takes"], grp["mt"]), add(J["children"], grp["ml"])
        P["takes"], P["children"] = add(P["takes"], grp["dpt"]), add(P["children"], grp["dpl"])
        bal = add(grp["mt"], grp["ml"])
        n["takes with J balance 0 about the centre"] += bal == Z
        n["takes with P balance 0"] += add(grp["dpt"], grp["dpl"]) == Z
        worst = max(worst, max(abs(x) for x in bal))
    total, ptot = list(Z), list(Z)
    for k in J:
        total, ptot = add(total, J[k]), add(ptot, P[k])
    bits = 0
    for row in record.get("rows", []):
        for line in (row.get("lines", []) if isinstance(row, dict) else []):
            for arr in (line if isinstance(line, list) else []):
                pass
    return {"cube": cube, "centre2": c2, "counts": n, "J2 by class": J, "P by class": P, "J2 clicks": total, "P clicks": ptot,
            "worst |2J| balance at a take": worst, "max |laid integer| at the six ends": max_laid,
            "intervals with a click moment not 0": sum(1 for v in per_i.values() if v != Z), "open remainders": open_rem[:8],
            "run_back": record.get("run_back"), "counts_record": {k: str(v) for k, v in record.get("counts", {}).items()}}


if __name__ == "__main__":
    rec = json.load(open(sys.argv[1]))
    c2 = ints(sys.argv[2].split(",")) if len(sys.argv) > 2 and sys.argv[2] else None
    found = read(rec, c2)
    found["record"] = sys.argv[1].split("/")[-1]
    print(json.dumps(found, indent=1, default=str))
