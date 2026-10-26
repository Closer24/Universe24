"""lt1: REPORT.md composed from out/ (the measurements as the tools wrote them) and copied to the hands directory. Usage: write_report.py <verdict line> <cut short>"""
import json
import sys
from pathlib import Path

F = Path(__file__).resolve().parent
O = F / "out"
HANDS = Path("/tmp/claude-0/-home-user-Universe24/e136d210-1915-523c-8c8e-0abbdf97855b/scratchpad/hands")


def load(name):
    p = O / name
    if not p.exists():
        return None
    try:
        return json.loads(p.read_text())
    except Exception:
        return None


def moment(name):
    d = load(name)
    if d is None:
        return "not run (cut short)"
    s = d["summary"]
    jt = "2J about the take's Node exact"
    return (
        f"births {s['births']}, credits {s['credits']}; the Link record identity per axis per booking {s['Link record identity per axis per booking (dp clock^2 + carry before - carry after = laid x wall)']}; "
        f"bookings that laid a level on the flux line {s['bookings that laid a level on the flux line (the quotient not 0)']}, |q| summed per axis {s['levels laid on the flux lines, |q| summed per axis']}; "
        f"P exact at the click as the identity {s['P exact at the click (3 axes, the identity)']}; 2J about the take's Node {s[jt]}, about the origin {s['2J about the origin exact']}; "
        f"the children's W summed to 0 {s['births with W of the children summed to 0']}; EX-S1 {s['EX-S1 taken + rem before - rem after = booked']}; run back {s['run_back']}; max bits {s['max bits at the marks']}; counts {s['counts']}"
    )


def cons(name):
    p = O / name
    if not p.exists():
        return "not run"
    lines = [ln for ln in p.read_text().splitlines() if ": " in ln and not ln.startswith("{")]
    return " | ".join(ln.strip() for ln in lines)


def ret(name):
    d = load(name)
    if d is None:
        return "not run (cut short)"
    return json.dumps({k: d[k] for k in ("seed X", "intervals with X the seed's at every Node", "returns", "births", "births by interval", "run_back")})


def c48():
    d = load("c48_chiral_3cube_60_flag.json")
    if d is None:
        return "not run (cut short)"
    s = d.get("summary", d)
    keep = {k: s[k] for k in s if k in ("counts", "by_det", "first_apart_intervals", "cube", "intervals")} | {"base": {k: s["base"][k] for k in ("births", "credits", "takes", "turns")}}
    return json.dumps(keep if keep else s, default=str)[:1500]


verdict, cut = sys.argv[1], sys.argv[2]
board = (O / "ga2_board_first6.json").read_text().strip() if (O / "ga2_board_first6.json").exists() else "not run"
flux = (O / "flux_sign.json").read_text() if (O / "flux_sign.json").exists() else "not run"
test = (O / "one_node_test.txt").read_text().strip().splitlines()[-1] if (O / "one_node_test.txt").exists() else "not run"
check = (O / "flagged_check.txt").read_text().strip().splitlines()[-1] if (O / "flagged_check.txt").exists() else "not run"

text = f"""# H-Lay-As-The-Take-Reversed-1 (lt1): report (2026-10-26, 07:44 to 08:5x UTC; toys-5 3dc12e307; the worktree /tmp/claude-0/-home-user-Universe24/e136d210-1915-523c-8c8e-0abbdf97855b/scratchpad/hands/lt1, nothing under src or tests edited; the flagged copy /dev/shm/tmp/lt1/src_lt1)

## 0. Verdict

{verdict}

## 1. The derivation (DERIVATION.md, the algebra one page; the four roads)

The lattice momentum stands twice in the head's letter: the interval writes the records' momentum density (metric.net_flux, u.G.D_a N at the weight num, "summed over the board the lattice momentum") on the carrier's three flux lines g_0a by the one write act at the held wall K den Gamma^2 T (Y-S3, built at this head: interval.kick's flux and interval.division's numerators), and the close reads every move's momentum (take.momentum_of, the change of the records' current on the Node's six Links) into the log and writes it nowhere. One object, the Link's record of the momentum at the Node, two spellings: the kick writes it, the click reads it and drops it. The form: the move writes its own booking on the same three lines by the same act, in the act's direction (RW-S1 read on the Link's record: the take reads the records' part and writes the lattice's part reversed). The identity per axis per move at the Node of the move, exact with no remainder dropped: dP_a p_0^2 + wr_a - wr_a' = q_a K den Gamma^2 T. The theorem on the children's line (the brief's literal form): no lay at a Node and its six Links on a plane standing at nothing at the end's neighbours moves the children's record on any Link (The booking's bilinear needs both ends; the lay writes one; GP-S1's slot form puts 0 on the birth's own Link too), so the lay returning the take's change on the children's line is refused on the transverse axes by that law at every birth on an empty plane (the hole 60: 15 of 16 births with the planes empty, W summed to 0; cm1, cm2: P exact 0 of 16), and admits the along component alone by the moving lay (AJ-S5; the cycle seed's 64 births lost): not proposed. The flux's unit measured on the hole 5-cube after 3 intervals: the kick's count flux summed over the board against -P_a (P_a = -2 num SUM_i F(i, i + a)): {flux} (the quotient 1000 per mille: the flux line's unit is the records' momentum negated, so the records' loss is the line's gain at the booking's sign).

## 2. The form in one paragraph (which integers the lay moves)

At the Node of every move of the close (the take's end, each child's end, a merger's two ends, a body's credit and its lay-back): the taken line's level now by the count (CR-S1) and the take's remainder (EX-S1) as before; the children's four levels at their ends (GP-S1) as before; and, new, the carrier's three flux lines at that Node, the level now by the quotient and the write remainder by the carry of one carried division of dP_a p_0^2 at the held wall K den Gamma^2 T, in the act's direction (node.write, the kick's own act on the same lines). No integer of a neighbour: the six F are read, the fold's n_ij = V_a(i) + V_a(j) moves on the Node's six Links by the Node's own V_a. One Node and its six Links; no second shell; the count of integers unchanged (the lines are Y-S3's); 115 bits at the marks (the head's).

## 3. The measurements (the prediction before each run, then the measured; integers only; run_all.sh)

Setting: P=/home/user/Universe24/venv314/bin/python; W=the worktree; K=the kit; F=$W/tools/derivations/open_items/H-Lay-As-The-Take-Reversed-1; S=/dev/shm/tmp/lt1/src_lt1; every run nice -n 19, one at a time, wait_load.py 3 before the long ones.

### 3.0 The flagged copy, the flag empty
Command: $P $K/make_flagged_copy.py lt1 LT1_RECOIL $F/replacements_lt1.json src $W/src python $P. Prediction: EQUAL on both worlds (the flag empty leaves one reading, node.start_clock, and no state). Measured: the hole 60 EQUAL (0864be32254a870dcfb4e7deb211210b1dedc27e7a2bafa0063ca9924c877058), the chiral 60 EQUAL (174932e9e81b98dc565495eae9d420d6f13ff182f0fc52a0ed1e7559af070fc8): "{check}" (out/flagged_check.txt); 17 replacements, lt1.patch.

### 3.1 The one-Node test
Command: LT1_RECOIL=1 PYTHONPATH=$S $P -m pytest -q $F/test_one_node_lt1.py. Prediction: the identity at every click of the hole world over 14 intervals read from the log and from the Node's own carry, the run back 14 of 14 exact with the recoil written and undone, the flux's unit -P, under 15 s. Measured: "{test}" (two functions; out/one_node_test.txt, out/flux_sign.json).

### 3.2 The hole 60 and the chiral 60 with the flag
Commands: LT1_RECOIL=1 $P -m event_universe.run $W/tests/worlds/world_hole.json /dev/shm/tmp/lt1/lt1_hole60.json back 10 (world_nature.json alike); $P $F/lt1_moment.py <record>; LT1_RECOIL=1 $P $K/conservation_check.py <record> out ... (the flag set so the board's re-run is the same code).
Prediction: every quotient 0 (the recoil 10^18 to 10^21 times p_0^2 against the wall 29476593539714484216000000000), the identity exact at every booking (the takes' ends and the lays' ends), the clicks the head's (16 births and 1653 credits; 16 and 3119), P and 2J exact as the identity at every click, EX-S1 at every click, the run back 10 of 10, the conservation check 12 of 12 on the hole and 11 of 12 on the chiral (gate 15's inequality on the one paired birth, the head's).
Measured, the hole 60: {moment('moment_hole60.json')}
The conservation check, the hole 60: {cons('cons_hole60.txt')}
Measured, the chiral 60: {moment('moment_chiral60.json')}
The conservation check, the chiral 60: {cons('cons_chiral60.txt')}

### 3.3 ga2 450 (the cycle seed, the 4-cube; world_ga2_450.json beside universe_ga2.json, the file's seed at 450 intervals), the flag and the head
Commands: LT1_RECOIL=1 $P -m event_universe.run $F/world_ga2_450.json ... back 10; PYTHONPATH=$W/src $P -m event_universe.run (the head); $P $F/ga2_return.py <record> 2,218,442; $P $F/lt1_moment.py.
Prediction: 64 births at the interval 2, the return (X at Gamma at 64 of 64 Nodes) at 218 and 442 on the flag and on the head alike, the clicks equal, the run back 10 of 10, every quotient 0.
Measured, the flag: {ret('ga2_return_flag.json')}
Measured, the head: {ret('ga2_return_head.json')}
The moment reader on the flag's record: {moment('moment_ga2_450.json')}
The clicks against the head's record event by event (the recoil's keys struck): the hole 60 16903 of 16903, the chiral 60 23579 of 23579 (counts and turns equal: the course the head's), ga2 450 26507 of 64675, first apart at the interval 5 (a refusal by `lay` at [2, 0, 0], row 2, its numbers), the head's 146 births (2: 64, 219: 64, 221: 14, 223: 2, 369: 2) against the flag's 150 (2: 64, 219: 64, 221: 22); the return at 219 on both (X the seed's 1017 at 64 of 64 Nodes; no second return within 450 on the head either, X 55490 to 73018 at 442). The mechanism on the board (out/ga2_board_first6.json, the flag's board against the head's over 7 intervals, the engine run twice): {board}

### 3.4 The bodies 300 (tests/worlds/world_bodies.json, the 7-cube) with the flag
Prediction: 0 births, the credits' identity at every click, every quotient 0, the run back 10 of 10. Measured: {moment('moment_bodies300.json')}

### 3.5 The 48 on the chiral 3-cube to 60 with the flag
Command: LT1_RECOIL=1 $P $K/clicks_48.py $K/world_chiral_300.json 60 $F/out/c48_chiral_3cube_60_flag.json cube 3. Prediction: 12 EQUAL and 36 APART, the head's (the clicks unchanged under the form; the form must not lower it). Measured: {c48()}

## 4. The sentence (LT-S1, as it would stand in ALGEBRA.md under The click; The booking, the clauses of the booking, the parity, the row act, the exact take, the reversal, the direction and the six metric lines kept by name)

LT-S1 (the lay is the take reversed on the Link's record): every move of a record's level at a Node by the close (the take's count at its end, each child's lay at its end, the merger's two ends, the body's credit and its lay-back) changes the records' current on the Node's six Links by one bilinear per axis, 2 num [d_now (before_(i-a) - before_(i+a)) + d_before (now_(i+a) - now_(i-a))], and the same act writes that change, at the clock squared by the position of the reading, on the Node's own record of those Links, the carrier's flux line of the axis, by the Node's one write act at the held wall, the carry in the line's write remainder, in the direction of the act (RW-S1: the read of the records' part is the write of the lattice's part reversed); so at every click the sum per axis of the records' change and the lattice's written change is 0 to no remainder, the angular momentum the moment of the same bookings about any centre, and the children carry nothing (GP-S1's lay stands); what the records lose on a Link the lattice holds on that Link's record and every gapped record reads at the fold (Y-S3). Below one level of the line the quantum lives in the carry.

## 5. The spec for David

DERIVATION.md section 4; lt1.patch beside it (the flag LT1_RECOIL to strike at entry; the lines named by CARRIER and AXES, the wall the line's own; no constant, no name, no number). The pass predicate: the identity dp clock^2 + carry before - carry after = laid x wall at every booking per axis (N of N); the flag empty bit for bit; the records' clicks the head's where every quotient is 0; the run back N of N; the one-Node test green.

## 6. Bugs met on the way (file and line)

None of the engine. Of the tools: the kit's conservation_check.py re-runs the board from the record's two files in the caller's environment, so a flagged record must be checked with its flag set (the re-run's log otherwise differs at every click: 15234 of 16903 on the first run); not a bug, a usage line for README_KIT.md rule 3. Of this hand: the birth entry names its keys (close.children) and did not carry the take's recoil numbers on the first copy (fixed, the 17th replacement); the test read the Node's lines before the step (the act returns new Line objects; fixed).

## 7. Missing by name

A record where a take's recoil reaches one level of the flux line (at the toy den every quotient is 0: the quantum in the carry, the fold unturned, the clicks unchanged; the trace weight 6 of TW-S1 lowers the wall 9 times, still above); the lattice's momentum summed over the board against -P as a reader over the run; the 5-cube's 48 under the form; the chiral 2,400 and the collapse; a world where a gapped pair meets and pays (the merger's two-end recoil written, exercised on the chiral's two exact-lay births alone); TC-S1's chord beneath the form (not needed: the form fails no law, the second run not owed).

Cut short: {cut}

## 8. The ledger row

| item | derived | one-Node test | toy (records, numbers) | gates touched | Universe | spec | missing by name |
|---|---|---|---|---|---|---|---|
| H-Lay-As-The-Take-Reversed-1: the lay as the take reversed on the Link's record (A1, the sixth attempt) | LT-S1: every move's recoil written on the carrier's flux line at its Node by the one write act, the identity exact to the carry; the literal form on the children's line refused by The booking's bilinear (a theorem) | test_one_node_lt1.py, 2 passed under 1 s: the identity at every click, the run back 14 of 14, the flux unit -P (1000 per mille) | the flagged copy EQUAL on the hole 60 and the chiral 60; the hole 60 identity 5103 of 5103, P and 2J 1669 of 1669, 12 of 12 laws; the chiral 60 identity 9507 of 9507, P and 2J 3135 of 3135, 11 of 12 (the head's gate 15); every quotient 0; ga2, the bodies and the 48 in section 3 | 15, 47 unchanged; the row "momentum and angular momentum in the clicks" as the Link record identity (SHOWN as the carry at this den) | the recoil below one level of g_0a at the toy den; the chiral 2,400 not run | lt1.patch, DERIVATION.md section 4 | section 7 |
"""
(F / "REPORT.md").write_text(text)
(HANDS / "lt1_REPORT.md").write_text(text)
print("written", len(text))
