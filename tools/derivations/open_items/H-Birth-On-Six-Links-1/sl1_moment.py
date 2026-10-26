"""The angular momentum and the momentum at the birth under the six-Link lay (H-Birth-On-Six-Links-1): integers only, doubled coordinates (2J, 2r), every move booked at its Node (the take at the taker's Node, each child's lay at its end, each recoil lay at its far end, the recoil's take at the taker's Node); per birth the P balance (the sum of every move's dP, 0 where conserved), the J balance about the centre and about the taker's Node, the moment about the Link's midpoint (the couple the one-Link lay could not carry), the transverse remainder's share of the transverse recoil in permille; summed over the record per class."""
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
    d = [(p - m) % cube for p, m in zip(plus, minus, strict=True)]
    return [x - cube if x > cube // 2 else x for x in d]


def unwrap(where, at, cube):
    """A Node's doubled place read beside the Node `at` on the torus (the arm one Link at most per axis)."""
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
    n = {"credits": 0, "births": 0, "births with a recoil lay": 0, "recoil lays": 0, "recoil lays onto nothing (dP along the lay's axis alone)": 0,
         "births: P balance 0 (every move summed)": 0, "births: J balance 0 about the centre": 0, "births: J balance 0 about the taker's Node": 0,
         "births: moment about the Link's midpoint 0": 0, "births: transverse P balance 0": 0, "births: W_children summing 0": 0,
         "births: the taker at one end of the Link": 0, "births: recoil lays' W 0 (re_before alone)": 0, "births: recoil take present": 0}
    J = {"credits": list(z), "births' takes": list(z), "births' children": list(z), "births' recoil lays": list(z), "births' recoil takes": list(z)}
    P = {k: list(z) for k in J}
    permille, worst_p, worst_j, head_lost = [], 0, 0, 0
    per_birth = []
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
        d = dipole(minus, plus, cube)
        ax = [a for a in range(3) if d[a] != 0][0]
        moves = [("births' takes", at, [int(x) for x in e["dP_take"]])]
        ends = e.get("dP_lay_ends")
        if ends is not None:
            for where, dpe in zip((minus, plus), ends, strict=True):
                moves.append(("births' children", where, [int(x) for x in dpe]))
        else:
            moves.append(("births' children", plus, [int(x) for x in e["dP_lay"]]))
        rec = e.get("recoil")
        if rec is not None:
            n["births with a recoil lay"] += 1
            for one in rec["lays"]:
                n["recoil lays"] += 1
                dpl = [int(x) for x in one["dP"]]
                n["recoil lays onto nothing (dP along the lay's axis alone)"] += all(dpl[b] == 0 for b in range(3) if b != one["axis"])
                moves.append(("births' recoil lays", one["node"], dpl))
            n["births: recoil lays' W 0 (re_before alone)"] += 1
            if "taken_line" in rec["take"]:
                n["births: recoil take present"] += 1
                moves.append(("births' recoil takes", rec["take"]["node"], [int(x) for x in rec["take"]["dP_take"]]))
        p_bal, j_bal, j_at, j_mid = list(z), list(z), list(z), list(z)
        r_at2 = [2 * x for x in at]
        mid2 = add(r_at2, [-x for x in d]) if at == plus else add(r_at2, d)
        mid2 = [(a + b) // 1 for a, b in zip(r_at2, [x if at == minus else -x for x in d])]
        for cls, where, dp in moves:
            r2 = unwrap(where, at, cube)
            p_bal = add(p_bal, dp)
            j_bal = add(j_bal, cross(arm(r2, c2), dp))
            j_at = add(j_at, cross(arm(r2, r_at2), dp))
            j_mid = add(j_mid, cross(arm(r2, mid2), dp))
            J[cls] = add(J[cls], cross(arm([2 * x for x in where], c2), dp))
            P[cls] = add(P[cls], dp)
        dp1 = moves[0][2]
        perp = sum(abs(dp1[b]) for b in range(3) if b != ax)
        perp_left = sum(abs(p_bal[b]) for b in range(3) if b != ax)
        if perp:
            permille.append(1000 * perp_left // perp)
        n["births: P balance 0 (every move summed)"] += p_bal == z
        n["births: J balance 0 about the centre"] += j_bal == z
        n["births: J balance 0 about the taker's Node"] += j_at == z
        n["births: moment about the Link's midpoint 0"] += j_mid == z
        n["births: transverse P balance 0"] += perp_left == 0
        worst_p = max(worst_p, max(abs(x) for x in p_bal))
        worst_j = max(worst_j, max(abs(x) for x in j_bal))
        head_lost = max(head_lost, max(abs(x) for x in cross(d, dp1)))
        per_birth.append({"i": e["i"], "node": at, "axis": ax, "dP_take": dp1, "P balance": p_bal, "J2 balance about the centre": j_bal,
                          "J2 about the taker's Node": j_at, "2 x moment about the midpoint": j_mid, "transverse left permille": (1000 * perp_left // perp) if perp else None,
                          "recoil": None if rec is None else {"betas": [x["beta"] for x in rec["lays"]], "axes": [x["axis"] for x in rec["lays"]], "take dP": rec["take"]["dP_take"], "take levels": rec["take"].get("levels", 0)}})
    total, ptot = list(z), list(z)
    for v in J.values():
        total = add(total, v)
    for v in P.values():
        ptot = add(ptot, v)
    return {"cube": cube, "centre2": c2, "counts": n, "J2 by class": J, "P by class": P, "J2 clicks": total, "P clicks": ptot,
            "worst |P balance| at a birth": worst_p, "worst |2J balance| at a birth about the centre": worst_j,
            "the one-Link lay's lost couple |e x dP_take| worst (the head's)": head_lost,
            "transverse recoil left permille per birth (min, max)": [min(permille), max(permille)] if permille else None,
            "per_birth": per_birth}


if __name__ == "__main__":
    rec = json.load(open(sys.argv[1]))
    found = read(rec, [int(x) for x in sys.argv[2].split(",")] if len(sys.argv) > 2 and sys.argv[2] else None)
    found["record"] = sys.argv[1].split("/")[-1]
    print(json.dumps(found, indent=1))
