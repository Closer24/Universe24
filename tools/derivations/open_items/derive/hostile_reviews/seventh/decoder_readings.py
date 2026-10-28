"""Row 15 and the ticks at the head (823690afc) on records the schema and the plan call lawful or broken.

usage: python3 -I decoder_readings.py <worktree> <scratch folder>

Each case writes a record (and a ledger) under the scratch folder, reads it with the head's decoder, and prints what it
reads beside what the plan or the schema says it is. The tool is run on two of them as a program.
"""

import json
import subprocess
import sys
from pathlib import Path

WT, SCRATCH = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve()
sys.path.insert(0, str(WT / "src"))
from tensor24.decoder import books, clocks, records  # noqa: E402

SCRATCH.mkdir(parents=True, exist_ok=True)
H = {"kind": "header", "record": "tensor24", "major": 1, "minor": 0}
HT = {**H, "trains": [{"index": t, "label": f"t{t}", "kinds": [0], "part": 1, "winding": 1} for t in (0, 1)]}
E = {"kind": "end", "rounds": 1, "digest": "", "undone": 0, "exact": 1}


def hold(t, w, k=(0, 0)):
    return {"train": t, "windings": list(w), "kept": list(k)}


def click(r, s, taken=(), laid=(), ends=(), train=1, q=None, count=None):
    c = {"kind": "whole", "round": r, "site": s, "count": r if count is None else count, "train": train}
    c |= {"taken": list(taken), "laid": list(laid), "ends": list(ends)}
    return c if q is None else {**c, "q": q}


def rate(r, s, count, k):
    return {"kind": "rate", "round": r, "site": s, "count": count, "dial": 0, "k": k}


def ledger(r, held):
    return [{"round": r, "at": a, "train": t, "wind": v} for t, pair in held.items() for a, v in zip(("step", "clicks"), pair)]


def write(name, lines):
    p = SCRATCH / name
    p.write_text("".join((x if isinstance(x, str) else json.dumps(x)) + "\n" for x in lines), encoding="utf-8")
    return str(p)


def row(lines, led):
    record, cause = records.read(write("r.jsonl", lines))
    if record is None:
        return f"not read: {cause}"
    v = books.row_15(record, led)
    return f"{v['kind']}: {v['cause']}"


TAKE = click(1, 0, [hold(1, (7, 4), (3, 2))], [hold(0, (0, 4))])  # the tests' TAKE: train 1's 3 windings and 1 kept into train 0
GOOD = ledger(1, {0: (0, 4), 1: (10, 6)})
cases = []

# 1. the second reading is "the wind over every train" (TENSOR24.md 837 and 1676; part C row 15); the decoder sums the
#    trains the ledger lists at the round, whatever they are
cases += [
    ("lawful: TAKE, the header naming trains 0 and 1, the ledger's every train", "SHOWN", row([HT, TAKE, E], GOOD)),
    ("broken ledger: it holds train 7 alone, a train of no record", "NOT READ", row([HT, TAKE, E], ledger(1, {7: (5, 5)}))),
    ("broken ledger: train 1 (which the click took from) left out", "NOT READ", row([HT, TAKE, E], ledger(1, {0: (0, 4)}))),
    ("broken ledger: train 0 (which the click laid into) left out, the click's wind lost", "NOT READ", row([HT, TAKE, E], ledger(1, {1: (10, 10)}))),
]

# 2. the first reading, K3: "taken + the remainder before - the remainder after = booked"; the decoder sums the
#    holdings, so a click whose books hold nothing, or hold the wrong train, closes
cases += [
    ("broken: a whole click of q 5 windings with no books at all", "books open or not read", row([HT, click(1, 0, q=5), E], ledger(1, {0: (0, 0), 1: (10, 10)}))),
    ("broken: a take that gains its windings (4 to 8) laid from a train that loses them", "books open or not read", row([HT, click(1, 0, [hold(1, (4, 8))], [hold(0, (4, 0))], q=4), E], ledger(1, {0: (4, 0), 1: (6, 10)}))),
    ("broken: a click of train 1 that takes from train 0 alone, q 4", "books open or not read", row([HT, click(1, 0, [hold(0, (4, 0))], [hold(1, (0, 4))], q=4), E], ledger(1, {0: (4, 0), 1: (6, 10)}))),
]

# 3. the record's places: a site off the board (Header: the sites in the order named), a round past the end's rounds
off_board = {**HT, "sides": [1, 1, 1], "order": "xyz"}
cases += [
    ("broken: a whole click at site 99 of a board of one site", "not read", row([off_board, click(1, 99, TAKE["taken"], TAKE["laid"]), E], GOOD)),
    ("broken: a whole click at site -1", "not read", row([off_board, click(1, -1, TAKE["taken"], TAKE["laid"]), E], GOOD)),
    ("broken: a whole click at round 5 of a record of 1 round", "not read", row([HT, click(5, 0, TAKE["taken"], TAKE["laid"]), E], ledger(5, {0: (0, 4), 1: (10, 6)}))),
    ("broken: a whole click at round -3", "not read", row([HT, click(-3, 0, TAKE["taken"], TAKE["laid"], count=1), E], ledger(-3, {0: (0, 4), 1: (10, 6)}))),
]

# 4. the schema's own line 1: "JSON Lines of whole numbers and labels"; a field the schema does not name is not read
for name, value in (("a float", 0.5), ("NaN", "NaN"), ("a truth value", True), ("null", None)):
    raw = json.dumps({**TAKE, "note": 0}).replace('"note": 0', f'"note": {json.dumps(value) if name != "NaN" else "NaN"}')
    cases.append((f"broken: {name} in a field the schema does not name", "not read", row([HT, raw, E], GOOD)))
cases.append(("broken: the end's digest \"\" (the schema: a digest is SHA-256 in hex)", "not read", row([HT, TAKE, E], GOOD)))

# 5. the ticks: k is a bit (state.py's Layout: "so the beat's k is a bit"); a rate line stands where k differs from the
#    last beat's (schema.Rate); a whole click's count is the count its beat reached, the first beat being 1
ticks = []
for name, lines, count, lawful in (
    ("k 2 at every beat", [(1, 1 + 1)], 4, "not read"),
    ("k -1 at every beat", [(1, -1)], 4, "not read"),
    ("a second line repeating k 1 at beat 3", [(1, 1), (1 + 1 + 1, 1)], 4, "not read (or 4)"),
    ("a whole click at count 0 (before any beat)", [(1, 1)], 0, "not read"),
):
    ticks.append((name, lawful, clocks.ticks_to(lines, count), clocks.unread(lines, count)))

# 6. the library without the tool's lift: a lawful line holding a whole number past the interpreter's digits
wide = '{"kind": "rate", "round": 1, "site": 0, "count": 1, "dial": ' + "9" * (sys.int_info.default_max_str_digits + 1) + ', "k": 1}'
sys.set_int_max_str_digits(sys.int_info.default_max_str_digits)
wide_cause = records.read(write("wide.jsonl", [H, wide, E]))[1]

for name, lawful, got in cases:
    print(f"{name}\n    the plan or schema: {lawful}\n    the head reads:     {got}")
for name, lawful, got, why in ticks:
    print(f"ticks, {name}\n    the plan or schema: {lawful}\n    the head reads:     {got} ticks{f' ({why})' if why else ''}")
print(f"the library, a lawful rate line of a {sys.int_info.default_max_str_digits + 1}-digit dial\n    the head reads:     {wide_cause}")

# the tool as a program on two of the cases
for name, lines, led in (
    ("the ledger of train 7 alone", [HT, TAKE, rate(1, 0, 1, 1), E], ledger(1, {7: (5, 5)})),
    ("a click with no books, q 5", [HT, click(1, 0, q=5), rate(1, 0, 1, -1), E], ledger(1, {0: (0, 0), 1: (10, 10)})),
):
    r, lg = write("tool_r.jsonl", lines), write("tool_l.jsonl", led)
    got = subprocess.run([sys.executable, "-I", str(WT / "tools" / "tensor24_decode.py"), r, lg], capture_output=True, text=True)
    print(f"the tool, {name}: exit {got.returncode}\n    " + got.stdout.strip().replace("\n", "\n    "))
