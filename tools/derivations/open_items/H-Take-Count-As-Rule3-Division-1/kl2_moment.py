"""The angular momentum and the momentum at the birth under the kick's inverse (H-Kick-And-Lay-One-Act-2): integers only, doubled coordinates (2J, 2r); every move booked at its Node (the take at the taker's Node, each child's lay at its end, each inverse lay at its far end); per take the P balance (every move summed), the 2J balance about the centre and about the taker's Node; the pair's relative 2L about its midpoint (the children's own lays); the inverse's levels, its share remainder against the walls booked; summed over the record; the bits of the largest integer in the log. Usage: kl2_moment.py <record.json> [centre2 as c,c,c]"""
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


def unwrap(where, at, cube):
    out = []
    for w, a in zip(where, at, strict=True):
        d = (w - a) % cube
        d = d - cube if d > cube // 2 else d
        out.append(2 * (a + d))
    return out


def bits_of(x: Any) -> int:
    if isinstance(x, bool):
        return 0
    if isinstance(x, int):
        return abs(x).bit_length()
    if isinstance(x, str):
        try:
            return abs(int(x)).bit_length()
        except ValueError:
            return 0
    if isinstance(x, list):
        return max((bits_of(v) for v in x), default=0)
    if isinstance(x, dict):
        return max((bits_of(v) for v in x.values()), default=0)
    return 0


def read(record: dict[str, Any], c2: list[int] | None = None) -> dict[str, Any]:
    log = record["log"]
    cube = int(record.get("cube") or (max(max(e["node"]) for e in log if e.get("node")) + 1))
    if c2 is None:
        c2 = [cube - 1] * 3
    z = [0, 0, 0]
    n = {"credits": 0, "births": 0, "takes (one take, its children, its inverse)": 0, "takes with the inverse laid": 0, "takes with the inverse refused (remainder named)": 0,
         "takes: P balance 0": 0, "takes: 2J balance 0 about the centre": 0, "takes: 2J balance 0 about the taker's Node": 0,
         "births: the pair's relative 2L about its midpoint 0": 0, "births: W_children summing 0": 0, "births: child's end dP along the Link alone": 0,
         "inverse: share remainder below a tenth of the walls": 0, "inverse: share remainder below a hundredth of the walls": 0}
    J = {"credits": list(z), "births' takes": list(z), "births' children": list(z), "inverse lays": list(z)}
    P = {k: list(z) for k in J}
    per = []
    worst_p = worst_j = 0
    levels_max = 0
    share_permille = []
    inverses = {}
    for e in log:
        if e.get("event") == "inverse":
            inverses[(e["i"], tuple(e["node"]), e["taken_row"])] = e
    groups: dict[tuple, list] = {}
    for e in log:
        kind = e.get("event")
        if kind == "credit":
            dp = [int(x) for x in e["dP_take"]]
            n["credits"] += 1
            J["credits"] = add(J["credits"], cross(arm([2 * x for x in e["node"]], c2), dp))
            P["credits"] = add(P["credits"], dp)
            continue
        if kind != "birth" or "takes" in e:
            continue
        n["births"] += 1
        groups.setdefault((e["i"], tuple(e["node"]), e["taken_row"]), []).append(e)
    for key, kids in groups.items():
        i, at, rec = key
        n["takes (one take, its children, its inverse)"] += 1
        r_at2 = [2 * x for x in at]
        moves = [("births' takes", at, [int(x) for x in kids[0]["dP_take"]])]
        for e in kids:
            minus, plus = e["minus"], e["plus"]
            n["births: W_children summing 0"] += sum(int(w) for w in e["W_children"]) == 0
            ends = e.get("dP_lay_ends")
            ends = [[int(x) for x in d] for d in ends] if ends is not None else [[0, 0, 0], [int(x) for x in e["dP_lay"]]]
            m2 = unwrap(minus, at, cube)
            p2 = unwrap(plus, at, cube)
            mid2 = [(a + b) for a, b in zip(m2, p2, strict=True)]  # 4 r_mid
            rel = add(cross([2 * a - b for a, b in zip(m2, mid2, strict=True)], ends[0]),
                      cross([2 * a - b for a, b in zip(p2, mid2, strict=True)], ends[1]))  # 4 L: the arm 4 (r_end - r_mid)
            n["births: the pair's relative 2L about its midpoint 0"] += rel == z
            ax = [a for a in range(3) if m2[a] != p2[a]][0]
            n["births: child's end dP along the Link alone"] += all(d[b] == 0 for d in ends for b in range(3) if b != ax)
            for where, d in zip((minus, plus), ends, strict=True):
                moves.append(("births' children", where, d))
        inv = inverses.get(key)
        laid = inv is not None and inv["laid"]
        if laid:
            n["takes with the inverse laid"] += 1
            for one in inv["lays"]:
                moves.append(("inverse lays", one["node"], [int(x) for x in one["dP"]]))
            levels_max = max(levels_max, int(inv["max_level"]))
            ds, booked = abs(int(inv["d_share"])), int(inv["booked"])
            share_permille.append(1000 * ds // booked if booked else None)
            n["inverse: share remainder below a tenth of the walls"] += 10 * ds < booked
            n["inverse: share remainder below a hundredth of the walls"] += 100 * ds < booked
        elif inv is not None:
            n["takes with the inverse refused (remainder named)"] += 1
        p_bal, j_bal, j_at = list(z), list(z), list(z)
        for cls, where, dp in moves:
            r2 = unwrap(where, at, cube)
            p_bal = add(p_bal, dp)
            j_bal = add(j_bal, cross(arm(r2, c2), dp))
            j_at = add(j_at, cross(arm(r2, r_at2), dp))
            J[cls] = add(J[cls], cross(arm([2 * x for x in where], c2), dp))
            P[cls] = add(P[cls], dp)
        n["takes: P balance 0"] += p_bal == z
        n["takes: 2J balance 0 about the centre"] += j_bal == z
        n["takes: 2J balance 0 about the taker's Node"] += j_at == z
        worst_p = max(worst_p, max(abs(x) for x in p_bal))
        worst_j = max(worst_j, max(abs(x) for x in j_bal))
        per.append({"i": i, "node": list(at), "kids": len(kids), "dP_take": moves[0][2], "P balance": p_bal, "2J balance about the centre": j_bal, "2J about the taker's Node": j_at,
                    "inverse": None if inv is None else {"laid": laid, "remainder": inv["remainder"], "max_level": inv.get("max_level"), "d_share": inv.get("d_share"), "booked": inv.get("booked")}})
    total, ptot = list(z), list(z)
    for v in J.values():
        total = add(total, v)
    for v in P.values():
        ptot = add(ptot, v)
    sp = [x for x in share_permille if x is not None]
    return {"cube": cube, "centre2": c2, "counts": n, "J2 by class": J, "P by class": P, "J2 clicks summed": total, "P clicks summed": ptot,
            "worst |P balance| at a take": worst_p, "worst |2J balance| at a take about the centre": worst_j,
            "inverse: the largest level laid": levels_max, "inverse: |share remainder| permille of the walls (min, max)": [min(sp), max(sp)] if sp else None,
            "bits of the largest integer in the log": bits_of(log), "per_take": per}


if __name__ == "__main__":
    rec = json.load(open(sys.argv[1]))
    found = read(rec, [int(x) for x in sys.argv[2].split(",")] if len(sys.argv) > 2 and sys.argv[2] else None)
    found["record"] = sys.argv[1].split("/")[-1]
    print(json.dumps(found, indent=1))
