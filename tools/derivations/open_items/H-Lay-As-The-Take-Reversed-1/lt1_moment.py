"""lt1's reader of a record run with LT1_RECOIL=1 (cp2_moment.py re-cut for the Link's record): per click (birth and credit) and per axis the identity of the Link's record, dp x clock^2 + carry before - carry after = levels laid x the flux line's write wall (the carrier's axis wall, trace den Gamma^2 T from the record's universe), at the take's end(s) and at the two lays' ends; the birth's P balance as the identity (dP_take + dP_lay_ends + the records' loss written at the Nodes = 0 per axis, exact where the identity holds); the J balance about the take's Node and about the origin as the moments of the same bookings (every booking at the Node of its move, so 2J closes where P closes at every Node); the levels the flux line gained (the quotients) counted; the children's W; EX-S1 at every click; the run back. Usage: lt1_moment.py <record.json> > summary (integers only)."""
import json
import sys

sys.set_int_max_str_digits(0)
rec = json.load(open(sys.argv[1]))
ints = rec["universe"]["integers"]
den, gamma, action, trace = (int(ints[k]) for k in ("den", "node_clock", "quantum_action", "trace"))
wwall = trace * den * gamma * gamma * action
cube = int(rec["cube"])
log = rec["log"]
births = [e for e in log if e["event"] == "birth"]
credits = [e for e in log if e["event"] == "credit"]


def cross3(r, p):
    return [r[1] * p[2] - r[2] * p[1], r[2] * p[0] - r[0] * p[2], r[0] * p[1] - r[1] * p[0]]


def rel(n, at):
    return [((n[a] - at[a] + cube // 2) % cube) - cube // 2 for a in range(3)]


def identity(dp, clock, laid, was, after):
    """Per axis: dp clock^2 + carry before - carry after == laid x wall."""
    return [int(dp[a]) * clock * clock + int(was[a]) - int(after[a]) == int(laid[a]) * wwall for a in range(3)]


def take_ends(e):
    """The take's ends of a click entry: (node, dP_take, clock, recoil, carry_was, carry) per end."""
    found = []
    for t in e.get("takes", [e]):
        node = t.get("node", e["node"])
        if "carry" not in t:
            return None
        found.append((node, [int(x) for x in t["dP_take"]], int(t["clock"]), t["recoil"], t["carry_was"], t["carry"]))
    return found


ident_ok = ident_all = 0
levels_laid = [0, 0, 0]
writes_nonzero = 0
missing = 0
P_exact = J_taker_exact = J_origin_exact = 0
W_zero = 0
ex_ok = ex_all = 0
rows = []
for e in births + credits:
    ends = take_ends(e)
    if ends is None:
        missing += 1
        continue
    bookings = []  # (node, dP of the records, dP written on the Link's record = -the booking)
    for node, dp, clock, laid, was, after in ends:
        ok = identity(dp, clock, laid, was, after)
        ident_ok += sum(ok)
        ident_all += 3
        writes_nonzero += any(int(x) != 0 for x in laid)
        levels_laid = [levels_laid[a] + abs(int(laid[a])) for a in range(3)]
        bookings.append((node, dp, all(ok)))
    if e["event"] == "birth" and "clock_ends" in e:
        for k, where in enumerate((e["minus"], e["plus"])):
            dp = [int(x) for x in e["dP_lay_ends"][k]]
            ok = identity(dp, int(e["clock_ends"][k]), e["recoil_ends"][k], e["carry_was_ends"][k], e["carry_ends"][k])
            ident_ok += sum(ok)
            ident_all += 3
            writes_nonzero += any(int(x) != 0 for x in e["recoil_ends"][k])
            bookings.append((where, dp, all(ok)))
    # P: the records' change at every booking less the same written on the Link's record: 0 where the identity holds
    p = [0, 0, 0]
    j_taker, j_origin = [0, 0, 0], [0, 0, 0]
    at = e["node"]
    closed = True
    for node, dp, ok in bookings:
        closed = closed and ok
        net = [dp[a] - dp[a] for a in range(3)] if ok else dp
        p = [p[a] + net[a] for a in range(3)]
        j_taker = [x + y for x, y in zip(j_taker, cross3([2 * r for r in rel(node, at)], net))]
        j_origin = [x + y for x, y in zip(j_origin, cross3([2 * r for r in node], net))]
    P_exact += p == [0, 0, 0]
    J_taker_exact += j_taker == [0, 0, 0]
    J_origin_exact += j_origin == [0, 0, 0]
    if "remainder_was" in e:
        ex_all += 1
        ex_ok += int(e["taken"]) + int(e["remainder_was"]) - int(e["remainder"]) == int(e["booked"])
    if e["event"] == "birth":
        W_zero += sum(int(x) for x in e["W_children"]) == 0
        rows.append({"i": e["i"], "at": at, "dP_take": [int(x) for x in e["dP_take"]], "dP_lay_ends": e["dP_lay_ends"],
                     "recoil_laid": [t.get("recoil") for t in e.get("takes", [e])], "closed": closed, "W_children": e["W_children"],
                     "taken": e["taken"], "booked": e["booked"]})
summary = {
    "record": sys.argv[1], "births": len(births), "credits": len(credits), "clicks without the recoil's numbers": missing,
    "Link record identity per axis per booking (dp clock^2 + carry before - carry after = laid x wall)": [ident_ok, ident_all],
    "bookings that laid a level on the flux line (the quotient not 0)": writes_nonzero,
    "levels laid on the flux lines, |q| summed per axis": levels_laid,
    "flux line write wall (trace den Gamma^2 T)": wwall,
    "P exact at the click (3 axes, the identity)": [P_exact, len(births) + len(credits) - missing],
    "2J about the take's Node exact": [J_taker_exact, len(births) + len(credits) - missing],
    "2J about the origin exact": [J_origin_exact, len(births) + len(credits) - missing],
    "births with W of the children summed to 0": [W_zero, len(births)],
    "EX-S1 taken + rem before - rem after = booked": [ex_ok, ex_all],
    "counts": rec.get("counts"), "run_back": rec.get("run_back"), "max bits at the marks": max(int(r["max bits"]) for r in rec["rows"]),
}
print(json.dumps({"summary": summary, "births": rows}, default=str))
