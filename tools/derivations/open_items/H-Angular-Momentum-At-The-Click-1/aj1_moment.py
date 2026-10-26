"""The angular momentum at the click, read on the click lines alone (H-Angular-Momentum-At-The-Click-1): integers only, doubled coordinates (2J, 2r), a Link's reach.

Per credit line: the take's moment (2r - 2c) x dP_take about the centre. Per birth line: the taker's moment about the centre and about the Link's midpoint (2 r_mid = r_minus + r_plus, the wrap folded), split along the Link's axis and transverse; the lay's moment per end where the line carries dP_lay_ends (the flagged form) and at the + end otherwise; the per-event balance (the taker's moment plus the children's lays' moment, 0 where J is conserved at the event); the theorem's two readings: the moment about the Link's own axis is 0 for the take and the lay alike (the arm is along the axis), and the lay's dP lies along the axis. The pair's one pseudovector, the dipole r_plus - r_minus (one Link), summed; the charges W summed. The remainder per event class: the credits standing, the births' takes, the births' lays, the mergers' two ends."""
import json
import sys
from typing import Any

sys.set_int_max_str_digits(0)


def cross(u, v):
    return [u[1] * v[2] - u[2] * v[1], u[2] * v[0] - u[0] * v[2], u[0] * v[1] - u[1] * v[0]]


def add(u, v):
    return [a + b for a, b in zip(u, v, strict=True)]


def arm(r2, c2):
    return [x - c for x, c in zip(r2, c2, strict=True)]


def dipole(minus, plus, cube):
    """r_plus - r_minus on the torus, each coordinate in -1, 0, 1."""
    d = [(p - m) % cube for p, m in zip(plus, minus, strict=True)]
    return [x - cube if x > cube // 2 else x for x in d]


def read(record: dict[str, Any], c2: list[int] | None = None) -> dict[str, Any]:
    log = record["log"]
    cube = int(record.get("cube") or (max(max(e["node"]) for e in log if e.get("node")) + 1))
    if c2 is None:
        c2 = [cube - 1] * 3
    z = [0, 0, 0]
    J = {"credits": list(z), "births' takes": list(z), "births' lays": list(z), "mergers' takes": list(z), "mergers' lays": list(z)}
    P = {k: list(z) for k in J}
    n = {"credits": 0, "credits laid back": 0, "births": 0, "mergers": 0,
         "births: taker's moment about the Link's midpoint 0": 0, "births: lay's moment about the Link's midpoint 0": 0,
         "births: moment about the Link's own axis 0 (take and lay)": 0, "births: dP_lay along the Link's axis": 0,
         "births: dP_lay 0": 0, "births: dP_take along the Link's axis only": 0, "births: balance 0 about the centre (J conserved at the event)": 0,
         "births: W_children summing 0": 0, "births: dP_lay_ends present": 0, "births: dP_lay_ends summing to dP_lay": 0, "births: the taker at one end of the Link": 0}
    dip, wsum, per_i = [0, 0, 0], 0, {}
    worst = 0
    births_i: dict[int, int] = {}
    for e in log:
        kind = e.get("event")
        if kind == "credit":
            dp = [int(x) for x in e["dP_take"]]
            m = cross(arm([2 * x for x in e["node"]], c2), dp)
            n["credits"] += 1
            n["credits laid back"] += "laid_back" in e
            J["credits"] = add(J["credits"], m); P["credits"] = add(P["credits"], dp)
        elif kind == "birth":
            merger = "takes" in e
            cls = "mergers" if merger else "births"
            n[cls] += 1
            births_i[int(e["i"])] = births_i.get(int(e["i"]), 0) + 1
            minus, plus = e["minus"], e["plus"]
            d = dipole(minus, plus, cube)
            ax = [a for a in range(3) if d[a] != 0]
            ax = ax[0] if len(ax) == 1 else None
            takes = [(t["node"], [int(x) for x in t["dP_take"]]) for t in e["takes"]] if merger else [(e["node"], [int(x) for x in e["dP_take"]])]
            mt, mt_mid, dpt = list(z), list(z), list(z)
            for where, dp in takes:
                r2 = [2 * x for x in where]
                mt = add(mt, cross(arm(r2, c2), dp))
                mt_mid = add(mt_mid, cross(d if list(where) == list(plus) else [-x for x in d], dp))
                n["births: the taker at one end of the Link"] += list(where) in (list(plus), list(minus))
                dpt = add(dpt, dp)
            dpl = [int(x) for x in e["dP_lay"]]
            ends = e.get("dP_lay_ends")
            ml, ml_mid = list(z), list(z)
            if ends is not None:
                n["births: dP_lay_ends present"] += 1
                n["births: dP_lay_ends summing to dP_lay"] += add([int(x) for x in ends[0]], [int(x) for x in ends[1]]) == dpl
                for where, dpe in zip((minus, plus), ends, strict=True):
                    r2 = [2 * x for x in where]
                    dpe = [int(x) for x in dpe]
                    ml = add(ml, cross(arm(r2, c2), dpe))
                    ml_mid = add(ml_mid, cross([-x for x in d] if where is minus else d, dpe))
            else:
                ml = cross(arm([2 * x for x in plus], c2), dpl)
                ml_mid = cross(d, dpl)
            m = add(mt, ml)
            J[cls + "' takes"] = add(J[cls + "' takes"], mt); J[cls + "' lays"] = add(J[cls + "' lays"], ml)
            P[cls + "' takes"] = add(P[cls + "' takes"], dpt); P[cls + "' lays"] = add(P[cls + "' lays"], dpl)
            if not merger:
                n["births: taker's moment about the Link's midpoint 0"] += mt_mid == z
                n["births: lay's moment about the Link's midpoint 0"] += ml_mid == z
                if ax is not None:
                    n["births: moment about the Link's own axis 0 (take and lay)"] += mt_mid[ax] == 0 and ml_mid[ax] == 0
                    n["births: dP_lay along the Link's axis"] += all(dpl[b] == 0 for b in range(3) if b != ax)
                    n["births: dP_take along the Link's axis only"] += all(dpt[b] == 0 for b in range(3) if b != ax)
                n["births: dP_lay 0"] += dpl == z
                n["births: balance 0 about the centre (J conserved at the event)"] += m == z
                n["births: W_children summing 0"] += sum(int(w) for w in e["W_children"]) == 0
                worst = max(worst, max(abs(x) for x in m))
            dip = add(dip, d)
            wsum += sum(int(w) for w in e["W_children"])
        else:
            continue
        per_i[int(e["i"])] = add(per_i.get(int(e["i"]), z), m)
    total = list(z)
    for v in J.values():
        total = add(total, v)
    ptot = list(z)
    for v in P.values():
        ptot = add(ptot, v)
    return {"cube": cube, "centre2": c2, "counts": n, "J2 by class": J, "P by class": P, "J2 clicks": total, "P clicks": ptot,
            "J2 remainder = the births' takes (the lays carrying 0)": J["births' takes"],
            "worst |2J| balance at a birth": worst, "dipole sum (r_plus - r_minus, Links)": dip, "W_children summed over births": wsum,
            "intervals with a click moment not 0": sum(1 for v in per_i.values() if v != z),
            "births per interval": {str(k): v for k, v in sorted(births_i.items())},
            "per_interval": {str(k): v for k, v in sorted(per_i.items())}}


if __name__ == "__main__":
    rec = json.load(open(sys.argv[1]))
    found = read(rec, [int(x) for x in sys.argv[2].split(",")] if len(sys.argv) > 2 and sys.argv[2] else None)
    found.pop("per_interval")
    found["record"] = sys.argv[1].split("/")[-1]
    print(json.dumps(found, indent=1))
