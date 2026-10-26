"""The angular momentum and the momentum at the birth under the kick's inverse (H-Kick-And-Lay-One-Act-1): integers only, doubled coordinates (2J, 2r), every move booked at its Node (the take at the taker's Node, each child's lay at its end, each far end's move of the taken line at its far end); per birth the P balance (every move summed), the J balance about the centre and about the taker's Node, the pair's relative L about its midpoint (the children's own per-end momentum alone), the remainder's share of the recoil in permille, the made share against the walls booked (MS-S1), the made share per level (the linear cost); summed over the record per class. Usage: kl1_moment.py <record.json> [centre2 as c,c,c]"""
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


def read(record: dict[str, Any], c2: list[int] | None = None) -> dict[str, Any]:
    log = record["log"]
    cube = int(record.get("cube") or (max(max(e["node"]) for e in log if e.get("node")) + 1))
    if c2 is None:
        c2 = [cube - 1] * 3
    z = [0, 0, 0]
    n = {"credits": 0, "births": 0, "births with the inverse": 0, "far-end moves": 0, "births: P balance 0 (every move summed)": 0,
         "births: J balance 0 about the centre": 0, "births: J balance 0 about the taker's Node": 0, "births: the system's rank 6": 0,
         "births: the rational solution integer (remainder 0)": 0, "births: W_children summing 0": 0, "births: the taker at one end of the Link": 0,
         "births: the pair's relative L about its midpoint 0": 0, "births: the children's per-end momentum 0 (onto nothing)": 0,
         "births: made share positive": 0}
    J = {"credits": list(z), "births' takes": list(z), "births' children": list(z), "births' far-end moves": list(z)}
    P = {k: list(z) for k in J}
    permille, made_permille, made_per_level, worst_p, worst_j, head_lost, head_worst_p = [], [], [], 0, 0, 0, 0
    levels_take, levels_inverse = 0, 0
    per_birth, l_rel_sum = [], list(z)
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
        at, minus, plus = e["node"], e["minus"], e["plus"]
        n["births: the taker at one end of the Link"] += at in (plus, minus)
        n["births: W_children summing 0"] += sum(int(w) for w in e["W_children"]) == 0
        dp1 = [int(x) for x in e["dP_take"]]
        moves = [("births' takes", at, dp1)]
        ends = e.get("dP_lay_ends")
        if ends is not None:
            for where, dpe in zip((minus, plus), ends, strict=True):
                moves.append(("births' children", where, [int(x) for x in dpe]))
        else:
            moves.append(("births' children", plus, [int(x) for x in e["dP_lay"]]))
        mid2 = add(unwrap(minus, at, cube), unwrap(plus, at, cube))
        mid2 = [x // 2 for x in mid2]
        l_rel = list(z)
        for cls, where, dp in moves[1:]:
            l_rel = add(l_rel, cross(arm(unwrap(where, at, cube), mid2), dp))
        n["births: the pair's relative L about its midpoint 0"] += l_rel == z
        n["births: the children's per-end momentum 0 (onto nothing)"] += all(dp == z for _c, _w, dp in moves[1:])
        l_rel_sum = add(l_rel_sum, l_rel)
        ki = e.get("kick_inverse")
        head_p = list(z)
        for _c, _w, dp in moves:
            head_p = add(head_p, dp)
        head_worst_p = max(head_worst_p, max(abs(x) for x in head_p))
        if ki is not None:
            n["births with the inverse"] += 1
            n["births: the system's rank 6"] += ki["rank"] == 6
            n["births: the rational solution integer (remainder 0)"] += ki["broken"] == 0
            n["births: made share positive"] += int(ki["made"]) > 0
            levels_take += abs(int(e["levels"]))
            levels_inverse += int(ki["levels_abs"])
            for one in ki["moves"]:
                n["far-end moves"] += 1
                moves.append(("births' far-end moves", one["node"], [int(x) for x in one["dP"]]))
            made_permille.append(1000 * int(ki["made"]) // int(ki["booked"]) if int(ki["booked"]) else None)
            made_per_level.append(int(ki["made"]) // int(ki["levels_abs"]) if int(ki["levels_abs"]) else None)
        p_bal, j_bal, j_at = list(z), list(z), list(z)
        r_at2 = [2 * x for x in at]
        for cls, where, dp in moves:
            r2 = unwrap(where, at, cube)
            p_bal = add(p_bal, dp)
            j_bal = add(j_bal, cross(arm(r2, c2), dp))
            j_at = add(j_at, cross(arm(r2, r_at2), dp))
            J[cls] = add(J[cls], cross(arm([2 * x for x in where], c2), dp))
            P[cls] = add(P[cls], dp)
        size = sum(abs(x) for x in head_p)
        if size:
            permille.append(1000 * sum(abs(x) for x in p_bal) // size)
        n["births: P balance 0 (every move summed)"] += p_bal == z
        n["births: J balance 0 about the centre"] += j_bal == z
        n["births: J balance 0 about the taker's Node"] += j_at == z
        worst_p = max(worst_p, max(abs(x) for x in p_bal))
        worst_j = max(worst_j, max(abs(x) for x in j_bal))
        per_birth.append({"i": e["i"], "node": at, "dP_take": dp1, "head P balance": head_p, "P balance": p_bal, "J2 balance about the centre": j_bal,
                          "J2 about the taker's Node": j_at, "pair relative 2L": l_rel, "recoil left permille": (1000 * sum(abs(x) for x in p_bal) // size) if size else None,
                          "inverse": None if ki is None else {"deltas": ki["deltas"], "rank": ki["rank"], "broken": ki["broken"], "remainder": ki["remainder"], "made": ki["made"], "booked": ki["booked"], "levels": e["levels"]}})
    total, ptot = list(z), list(z)
    for v in J.values():
        total = add(total, v)
    for v in P.values():
        ptot = add(ptot, v)
    return {"cube": cube, "centre2": c2, "counts": n, "J2 by class": J, "P by class": P, "J2 clicks": total, "P clicks": ptot,
            "pair relative 2L summed": l_rel_sum,
            "worst |P balance| at a birth": worst_p, "worst |P balance| at a birth without the inverse (the head's)": head_worst_p,
            "worst |2J balance| at a birth about the centre": worst_j,
            "recoil left permille per birth (min, max)": [min(permille), max(permille)] if permille else None,
            "made share permille of the walls booked (min, max)": [min(x for x in made_permille if x is not None), max(x for x in made_permille if x is not None)] if any(x is not None for x in made_permille) else None,
            "made share per level moved (min, max)": [min(x for x in made_per_level if x is not None), max(x for x in made_per_level if x is not None)] if any(x is not None for x in made_per_level) else None,
            "levels: the takes summed, the far-end moves summed": [levels_take, levels_inverse],
            "per_birth": per_birth}


if __name__ == "__main__":
    rec = json.load(open(sys.argv[1]))
    found = read(rec, [int(x) for x in sys.argv[2].split(",")] if len(sys.argv) > 2 and sys.argv[2] else None)
    found["record"] = sys.argv[1].split("/")[-1]
    print(json.dumps(found, indent=1))
