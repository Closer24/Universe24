"""Source mutants of the decoder's new text (823690afc) that Animate's 50 do not hold, and each guard removed.

usage: python3 -I decoder_mutants_s8.py <worktree> <scratch folder>   (PYTHONPATH unset)

Each mutant is one or more textual changes in a scratch copy of src/tensor24, tools/tensor24_decode.py and
tests/test_the_tensor24_decoder.py; the decoder's tests run on the copy (no -x, so every failing test counts).
"killed" names the first failing test; "SURVIVED" means every test passes on the mutant. After each survivor the
probe runs a witness: a record or ledger the mutant reads wrongly (or raises on), with what the head reads on it.
"""

import shutil
import subprocess
import sys
from pathlib import Path

REC, BOOKS, CLOCKS, TOOL = (
    "src/tensor24/decoder/records.py",
    "src/tensor24/decoder/books.py",
    "src/tensor24/decoder/clocks.py",
    "tools/tensor24_decode.py",
)
TEST = "tests/test_the_tensor24_decoder.py"
GUARDS = ("jsoned", "framed", "headed", "majored", "ended", "kinded", "placed", "shaped", "booked", "ordered")
LEDGER_GUARDS = ("objects", "standing", "fitted", "once")


def removed(name, tuple_name, names):
    """The guard dropped from its tuple."""
    if tuple_name == "GUARDS":
        old = "GUARDS: tuple[Guard, ...] = (\n" + "".join(f"    {g},\n" for g in names) + ")"
    else:
        old = f"LEDGER_GUARDS: tuple[Guard, ...] = ({', '.join(names)})"
    kept = [g for g in names if g != name]
    new = (
        "GUARDS: tuple[Guard, ...] = (\n" + "".join(f"    {g},\n" for g in kept) + ")"
        if tuple_name == "GUARDS"
        else f"LEDGER_GUARDS: tuple[Guard, ...] = ({', '.join(kept)})"
    )
    return [(REC, old, new)]


MUTANTS = {
    **{f"the guard {g} removed from GUARDS": removed(g, "GUARDS", GUARDS) for g in GUARDS},
    **{f"the guard {g} removed from LEDGER_GUARDS": removed(g, "LEDGER", LEDGER_GUARDS) for g in LEDGER_GUARDS},
    # G2's label half
    "a label's shape not read (any value fits a str field)": [
        (REC, "    if shape is str:\n        return isinstance(value, str)\n", "    if shape is str:\n        return True\n")
    ],
    # the cause names the last misfit field, not the first
    "misfit names the last wrong field": [(REC, "return wrong[0] if wrong else \"\"", "return wrong[-1] if wrong else \"\"")],
    # the schema's order (round, kind, site, train): the train dropped
    "the order read without the train": [
        (REC, 'return round_, KINDS.index(e["kind"]), site, train', 'return round_, KINDS.index(e["kind"]), site, 0')
    ],
    # the place guard's round half
    "an event's round not checked (site alone)": [(REC, 'PLACE = ("round", "site")', 'PLACE = ("site",)')],
    # G3's laid half
    "a click booked again in its laid alone read (G3)": [
        (REC, 'if ends and (click.get("taken") or click.get("laid")):', 'if ends and click.get("taken"):')
    ],
    # G3's count: three ends
    "a click with three ends read (G3)": [(REC, "if ends and len(ends) != len(ENDS):", "if ends and len(ends) < len(ENDS):")],
    # the ledger's place guard: round and train
    "a ledger line's round and train not checked": [(REC, 'ENTRY = ("round", "train")', "ENTRY = ()")],
    "a ledger line's train not checked": [(REC, 'ENTRY = ("round", "train")', 'ENTRY = ("round",)')],
    # G1 in the books: a holding's windings, a laid holding
    "a holding's lacking windings read (G1)": [(BOOKS, 'HELD = ("windings", "kept")', 'HELD = ("kept",)')],
    "a laid holding's lacking fields read (G1)": [
        (BOOKS, "held = [h for p in sides for key in BOOKS for h in p.get(key, [])]", 'held = [h for p in sides for h in p.get("taken", [])]')
    ],
    # the verdict: the books closed where some whole click closes
    "the books read closed where any whole click closes": [
        (BOOKS, 'every = first["closed"] == first["whole clicks"]', 'every = first["closed"] > 0')
    ],
    # the second reading: a round whose clicks lines hold trains the step lacks
    "a round read whose clicks lines hold more trains than the step's": [
        (BOOKS, "        and set(step) == set(clicks)\n", "        and set(step) <= set(clicks)\n")
    ],
    "the clicks lines' wind not checked whole": [
        (BOOKS, "and all(whole(w) for w in [*step.values(), *clicks.values()])", "and all(whole(w) for w in step.values())")
    ],
    # the parse: a JSON value that is no object let through parsed()
    "a JSON value that is no object let through parsed()": [
        (REC, "return line if isinstance(line, dict) else None", "return line")
    ],
    # the major's whole check
    "a major that is no whole number read by its value": [(REC, "if not whole(major):", "if major is None:")],
    # the tool
    "the tool takes four arguments": [(TOOL, "if len(argv) not in (2, 3):", "if len(argv) < 2:")],
    "the tool reads on past a record not read": [
        (TOOL, '        print(f"not read: {cause}")\n        return 0\n', '        print(f"not read: {cause}")\n')
    ],
    "the tool counts a click's unread ticks as read": [(TOOL, "            unread.append(f\"round {c['round']}, site {c['site']}: {clocks.unread(held, c.get('count'))}\")\n", "            read.append(0)\n")],
}

WITNESS = r'''
import json, subprocess, sys
from pathlib import Path
sys.path.insert(0, "src")
from tensor24.decoder import books, clocks, records
H = {"kind": "header", "record": "tensor24", "major": 1, "minor": 0}
E = {"kind": "end", "rounds": 1, "digest": "", "undone": 0, "exact": 1}
def hold(t, w, k=(0, 0)):
    return {"train": t, "windings": list(w), "kept": list(k)}
def click(r, s, taken=(), laid=(), ends=(), train=0):
    return {"kind": "whole", "round": r, "site": s, "count": r, "train": train, "taken": list(taken), "laid": list(laid), "ends": list(ends)}
def end_of(s, taken, laid):
    return {"site": s, "spoke": 0, "taken": taken, "laid": laid, "push": [0, 0, 0]}
TAKE = click(1, 0, [hold(1, (7, 4), (3, 2))], [hold(0, (0, 4))])
PAIR = click(1, 0, ends=[end_of(0, [hold(0, (5, 0), (0, 1))], [hold(1, (0, 4))]), end_of(1, [hold(0, (5, 0))], [hold(1, (0, 5))])])
def write(name, lines):
    p = Path(name)
    p.write_text("".join((l if isinstance(l, str) else json.dumps(l)) + "\n" for l in lines), encoding="utf-8")
    return str(p)
def safe(f, *a):
    try:
        return f(*a)
    except Exception as e:
        return f"RAISES {type(e).__name__}: {e}"
GOOD = [{"round": 1, "at": "step", "train": 0, "wind": 0}, {"round": 1, "at": "clicks", "train": 0, "wind": 4},
        {"round": 1, "at": "step", "train": 1, "wind": 10}, {"round": 1, "at": "clicks", "train": 1, "wind": 6}]
w = sys.argv[1]
if w == "label":
    print("End's digest 5, the header's engine [1]:", safe(records.read, write("r.jsonl", [{**H, "engine": [1]}, {**E, "digest": 5}]))[1] or "read")
elif w == "misfit":
    print("a rate line with count 1.5 and k 0.5:", safe(records.read, write("r.jsonl", [H, {"kind": "rate", "round": 1, "site": 0, "count": 1.5, "dial": 0, "k": 0.5}, E]))[1])
elif w == "train":
    print("two whole clicks at one round and site, train 1 before train 0:", safe(records.read, write("r.jsonl", [H, {**TAKE, "train": 1}, {**TAKE, "train": 0}, E]))[1] or "read")
elif w == "round":
    print("an event without its round:", safe(records.read, write("r.jsonl", [H, {"kind": "rate", "site": 0, "count": 1, "k": 1}, E])))
elif w == "laid":
    rec = safe(records.read, write("r.jsonl", [H, {**PAIR, "laid": [hold(1, (0, 99))]}, E]))
    print("a pair booked at its ends and again in the click's laid:", rec[1] or books.row_15(rec[0], [{"round": 1, "at": a, "train": t, "wind": v} for t, (x, y) in {0: (10, 1), 1: (0, 9)}.items() for a, v in (("step", x), ("clicks", y))])["kind"])
elif w == "three":
    rec = safe(records.read, write("r.jsonl", [H, click(1, 0, ends=[*PAIR["ends"], PAIR["ends"][1]]), E]))
    print("a whole click with three ends:", rec[1] or "read")
elif w == "entry":
    l = write("l.jsonl", [*GOOD, {"at": "step", "train": 0, "wind": 4}])
    print("a ledger line without its round:", safe(records.read_ledger, l))
    l = write("l.jsonl", [*GOOD, {"round": 1, "at": "step", "wind": 4}])
    print("a ledger line without its train:", safe(records.read_ledger, l))
elif w == "windings":
    rec = records.read(write("r.jsonl", [H, click(1, 0, [{"train": 1, "kept": [3, 2]}], [hold(0, (0, 4))]), E]))[0]
    print("a taken holding without its windings:", safe(books.row_15, rec, GOOD))
elif w == "laidheld":
    rec = records.read(write("r.jsonl", [H, click(1, 0, [hold(1, (7, 4), (3, 2))], [{"train": 0, "windings": [0, 4]}]), E]))[0]
    print("a laid holding without its kept:", safe(books.row_15, rec, GOOD))
elif w == "every":
    opened = click(1, 0, [hold(1, (7, 4), (3, 3))], [hold(0, (0, 4))], train=1)
    rec = records.read(write("r.jsonl", [H, TAKE, opened, E]))[0]
    led = [{"round": 1, "at": a, "train": t, "wind": v} for t, (x, y) in {0: (0, 8), 1: (10, 2)}.items() for a, v in (("step", x), ("clicks", y))]
    print("one whole click closed, one open, the ledger agreeing:", safe(books.row_15, rec, led)["kind"])
elif w == "subset":
    rec = records.read(write("r.jsonl", [H, TAKE, E]))[0]
    led = [{"round": 1, "at": "step", "train": 0, "wind": 10}, {"round": 1, "at": "clicks", "train": 0, "wind": 4}, {"round": 1, "at": "clicks", "train": 1, "wind": 6}]
    print("the step lines hold train 0 alone, the clicks lines trains 0 and 1:", safe(books.row_15, rec, led))
elif w == "clickswind":
    rec = records.read(write("r.jsonl", [H, TAKE, E]))[0]
    led = [*GOOD[:3], {"round": 1, "at": "clicks", "train": 1}]
    print("a clicks line without its wind:", safe(books.row_15, rec, led))
elif w == "notobject":
    print("a record line that is a JSON list:", safe(records.read, write("r.jsonl", [H, "[1, 2]", E])))
elif w == "major":
    print("a header whose major is true:", safe(records.read, write("r.jsonl", [{**H, "major": True}, E])))
elif w in ("four", "readon", "ticks"):
    r = write("r.jsonl", [H, TAKE, E] if w == "ticks" else [H, "no json", E])
    args = [r, "l.jsonl", "extra"] if w == "four" else [r]
    got = subprocess.run([sys.executable, "-I", "tools/tensor24_decode.py", *args], capture_output=True, text=True)
    print(f"the tool on {args}: exit {got.returncode}; stdout {got.stdout.strip()!r}; stderr tail {got.stderr.strip().splitlines()[-1:]!r}")
'''

WITNESSES = {
    "a label's shape not read (any value fits a str field)": "label",
    "misfit names the last wrong field": "misfit",
    "the order read without the train": "train",
    "an event's round not checked (site alone)": "round",
    "a click booked again in its laid alone read (G3)": "laid",
    "a click with three ends read (G3)": "three",
    "a ledger line's round and train not checked": "entry",
    "a ledger line's train not checked": "entry",
    "a holding's lacking windings read (G1)": "windings",
    "a laid holding's lacking fields read (G1)": "laidheld",
    "the books read closed where any whole click closes": "every",
    "a round read whose clicks lines hold more trains than the step's": "subset",
    "the clicks lines' wind not checked whole": "clickswind",
    "a JSON value that is no object let through parsed()": "notobject",
    "a major that is no whole number read by its value": "major",
    "the tool takes four arguments": "four",
    "the tool reads on past a record not read": "readon",
    "the tool counts a click's unread ticks as read": "ticks",
}


def scratch(name, changes):
    tree = SCRATCH / "".join(ch if ch.isalnum() else "_" for ch in name)[:80]
    shutil.rmtree(tree, ignore_errors=True)
    shutil.copytree(WT / "src" / "tensor24", tree / "src" / "tensor24", ignore=shutil.ignore_patterns("__pycache__"))
    (tree / "tests").mkdir()
    (tree / "tools").mkdir()
    shutil.copy(WT / "tests" / "__init__.py", tree / "tests" / "__init__.py")
    shutil.copy(WT / TEST, tree / TEST)
    shutil.copy(WT / TOOL, tree / TOOL)
    (tree / "pytest.ini").write_text("[pytest]\naddopts = --import-mode=importlib\npythonpath = src\n")
    for rel, old, new in changes:
        path = tree / rel
        text = path.read_text()
        assert text.count(old) == 1, (name, old)
        path.write_text(text.replace(old, new))
    return tree


def run(name, changes):
    tree = scratch(name, changes)
    got = subprocess.run(
        [sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider", TEST], cwd=tree, capture_output=True, text=True
    )
    failed = [ln.split("::", 1)[-1] for ln in got.stdout.splitlines() if ln.startswith(("FAILED", "ERROR"))]
    return tree, got.returncode, failed, (got.stdout.strip().splitlines() or [""])[-1]


def witness(tree, key):
    (tree / "w.py").write_text(WITNESS)
    got = subprocess.run([sys.executable, "-I", "w.py", key], cwd=tree, capture_output=True, text=True)
    return (got.stdout + got.stderr).strip()


if __name__ == "__main__":
    WT, SCRATCH = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve()
    tree, code, failed, tail = run("unmutated", [])
    print(f"unmutated: rc={code} {tail}")
    assert code == 0, failed
    head_tree = tree
    survivors = []
    for name, changes in MUTANTS.items():
        tree, code, failed, tail = run(name, changes)
        print(f"{'SURVIVED' if code == 0 else 'killed  '} {name}" + (f"  <- {failed[0].split(' - ')[0]} ({len(failed)} failing)" if failed else ""))
        if name in WITNESSES and code == 0:
            print(f"    mutant: {witness(tree, WITNESSES[name])}")
            print(f"    head:   {witness(head_tree, WITNESSES[name])}")
        survivors += [name] if code == 0 else []
        shutil.rmtree(tree)
    shutil.rmtree(head_tree)
    print(f"{len(MUTANTS)} mutants, {len(survivors)} survived")
