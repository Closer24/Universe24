"""The decoder's source mutants against its tests (Animate): every mutant must fail tests/test_the_tensor24_decoder.py.

usage: python -I mutants.py <worktree> <scratch folder>
Each mutant is one or more textual changes in a scratch copy of src/tensor24, tools/tensor24_decode.py and the decoder's
test; "killed" names the tests that fail with it, "SURVIVED" means all of them pass. The mutants are the fifth hostile
review's sixteen as they read on the decoder's new text (decoder_mutants.py there), and one or more for every guard,
reading and line of the tool added for the review's three changes and Sofer's G1 to G3.
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
CLOSES = 'return all(gained(p["taken"]) + gained(p["laid"]) == 0 for p in parts(click))'
AGREE = "agree = sum(sum(step.values()) == sum(clicks.values()) for step, clicks in read)"

MUTANTS = {
    # the fifth review's sixteen, on the new text
    "the books close at any end, not every end": [
        (BOOKS, CLOSES, CLOSES.replace("return all(", "return any("))
    ],
    "the books close over the two ends together, not at each": [
        (BOOKS, CLOSES, 'return sum(gained(p["taken"]) + gained(p["laid"]) for p in parts(click)) == 0')
    ],
    "the round's winds summed over every round (the round dropped)": [
        (
            BOOKS,
            'winds.setdefault((line["round"], line["at"]), {})',
            'winds.setdefault((0, line["at"]), {})',
        ),
        (
            BOOKS,
            'winds.get((r, "step"), {}), winds.get((r, "clicks"), {})',
            'winds.get((0, "step"), {}), winds.get((0, "clicks"), {})',
        ),
    ],
    "the ledger agreeing where the clicks' wind is at least the step's": [
        (BOOKS, AGREE, AGREE.replace(" == ", " >= "))
    ],
    "the ledger agreeing where the clicks' wind is at most the step's": [
        (BOOKS, AGREE, AGREE.replace(" == ", " <= "))
    ],
    "SHOWN wherever the ledger agrees, the books open or not": [
        (BOOKS, "held = every and agree == read", "held = agree == read")
    ],
    "SHOWN wherever the record reads": [(BOOKS, "held = every and agree == read", "held = True")],
    "the ledger absent read as an empty ledger": [
        (
            BOOKS,
            "    if ledger is None:\n",
            "    if ledger is None:\n        ledger = []\n    if ledger is None:\n",
        )
    ],
    "the rate lines read by the round, not by the beat's count": [
        (
            CLOCKS,
            'append((line.get("count"), line.get("k")))',
            'append((line.get("round"), line.get("k")))',
        )
    ],
    "the rate lines of every Node-clock read as one": [
        (CLOCKS, 'by_site.setdefault(line["site"], [])', "by_site.setdefault(0, [])")
    ],
    "the broken line named one line on": [
        (
            REC,
            "            for n, line in enumerate(lines, start=1)\n            if line is None or",
            "            for n, line in enumerate(lines, start=1 + 1)\n            if line is None or",
        )
    ],
    "the unplaced event named one line back": [
        (REC, "enumerate(events, start=1 + 1)", "enumerate(events, start=1)")
    ],
    "the two causes of the major swapped": [
        (
            REC,
            'return "the header holds no major version"',
            'return f"the major version {major} is unknown"',
        )
    ],
    "the order read by round and kind alone": [
        (
            REC,
            'return round_, KINDS.index(e["kind"]), site, train',
            'return round_, KINDS.index(e["kind"]), 0, 0',
        )
    ],
    "the kinds' order within a round changed (rate before turnover)": [
        (
            REC,
            'KINDS = ("whole", "split", "turnover", "rate", "books")',
            'KINDS = ("whole", "split", "rate", "turnover", "books")',
        )
    ],
    "a line with no kind let through the first guard": [
        (REC, 'if line is None or not isinstance(line.get("kind"), str)', "if line is None")
    ],
    # the review's three changes and its follow-ups
    "a line past the interpreter's depth or digits raises (JSON's own error caught alone)": [
        (REC, "except ValueError, RecursionError:", "except json.JSONDecodeError:")
    ],
    "a key twice read as its last value": [
        (REC, "return line if len(line) == len(pairs) else None", "return line")
    ],
    "the lines split by splitlines": [
        (
            REC,
            'texts = f.read().split("\\n")',
            'texts = f.read().splitlines()\n            texts.append("")',
        )
    ],
    "the file read with universal newlines": [(REC, 'encoding="utf-8", newline=""', 'encoding="utf-8"')],
    "the file's last line feed read as an empty line": [
        (REC, '(texts[:-1] if texts[-1] == "" else texts)', "texts")
    ],
    "a file's cause unnamed": [(REC, 'cause = cause and f"the {whose} file {cause}"', "cause = cause")],
    "an empty file let through the frame": [
        (REC, 'len(lines) < len(("header", "end"))', "len(lines) < 1")
    ],
    "a newer major read": [(REC, "if major != schema.MAJOR else", "if major < schema.MAJOR else")],
    "the header's and end's kinds read as events' kinds": [
        (
            REC,
            '{e["kind"] for e in events_of(lines)} - set(KINDS)',
            '{e["kind"] for e in lines if e} - set(KINDS)',
        )
    ],
    "the ticks not read past the first missing rate line (the tool's zip)": [
        (CLOCKS, '    if not lines:\n        return "its Node-clock holds no rate line"\n', "")
    ],
    "the tool's usage line dropped": [(TOOL, "if len(argv) not in (2, 3):", "if not argv:")],
    "the tool keeps the interpreter's digits": [(TOOL, "    sys.set_int_max_str_digits(0)\n", "")],
    "the ledger's at not read": [(REC, ' and line.get("at") in AT)', ")")],
    "the ledger's fields' shapes not read": [
        (REC, 'if line is not None and misfit(line, shapes["ledger"], shapes)', "if line is None")
    ],
    "a ledger line at the place of an earlier one read": [
        (REC, "if earliest[entry] != n]", "if earliest[entry] != earliest[entry]]")
    ],
    # Sofer's G1 to G3
    "a truth value read as a whole number (G2)": [
        (REC, "        return whole(value)\n", "        return isinstance(value, int)\n")
    ],
    "a float read as a whole number (G2)": [
        (REC, "        return whole(value)\n", "        return isinstance(value, int | float)\n")
    ],
    "a row of any length (G1)": [(REC, "        and len(value) == len(rows)\n", "")],
    "a record of the schema read as any mapping (G1)": [
        (
            REC,
            "return isinstance(value, dict) and not misfit(value, shapes[shape.__name__.lower()], shapes)",
            "return isinstance(value, dict)",
        )
    ],
    "the header and the end not shaped (G1)": [
        (
            REC,
            '        for n, line in enumerate(lines, start=1)\n        if line is not None and line["kind"] in shapes',
            '        for n, line in enumerate(lines, start=1)\n        if line is not None and line["kind"] in KINDS',
        )
    ],
    "a click booked at the click and again at its ends read (G3)": [
        (REC, 'if ends and (click.get("taken") or click.get("laid")):', "if False:")
    ],
    "a click with one end read at that end (G3)": [
        (REC, "if ends and len(ends) != len(ENDS):", "if False:")
    ],
    "a click's lacking ends read (G1)": [(BOOKS, '        "ends" in click\n        and ', "        ")],
    "a holding's lacking kept read (G1)": [
        (BOOKS, "        and all(key in h for h in held for key in HELD)\n", "")
    ],
    "a click that lacks its books read among the others (G1)": [
        (BOOKS, 'if first["read"] < first["whole clicks"]:', "if False:")
    ],
    # the second reading, the plan's
    "a split click's round not read (whole clicks alone)": [
        (BOOKS, 'CLICKS = ("whole", "split")', 'CLICKS = ("whole",)')
    ],
    "a round read whose step and clicks lines hold other trains": [
        (BOOKS, "        and set(step) == set(clicks)\n", "")
    ],
    "a round read whose wind is no whole number": [
        (BOOKS, "        and all(whole(w) for w in [*step.values(), *clicks.values()])\n", "")
    ],
    "the ledger shown where it is read at some rounds alone": [
        (BOOKS, "if not read or (held and read < rounds):", "if not read:")
    ],
    # the ticks
    "a negative count read": [(CLOCKS, "if not whole(count) or count < 0:", "if not whole(count):")],
    "a rate line's lacking k read": [
        (
            CLOCKS,
            "if not all(whole(c) and whole(k) for c, k in lines):",
            "if not all(whole(c) for c, k in lines):",
        )
    ],
    "the first rate line read at any beat": [(CLOCKS, "if counts[0] != 1:", "if False:")],
    "rate lines that do not rise read": [
        (CLOCKS, "if not all(a < b for a, b in zip(counts, counts[1:], strict=False)):", "if False:")
    ],
    "a stretch read past its count": [
        (CLOCKS, "(following if following <= count else count + 1)", "following")
    ],
}


def run(name, changes):
    tree = SCRATCH / "".join(ch if ch.isalnum() else "_" for ch in name)[:80]
    shutil.rmtree(tree, ignore_errors=True)
    shutil.copytree(
        WT / "src" / "tensor24", tree / "src" / "tensor24", ignore=shutil.ignore_patterns("__pycache__")
    )
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
    got = subprocess.run(
        [sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider", "-x", TEST],
        cwd=tree,
        capture_output=True,
        text=True,
    )
    failed = [
        ln.split("::", 1)[-1] for ln in got.stdout.splitlines() if ln.startswith(("FAILED", "ERROR"))
    ]
    shutil.rmtree(tree)
    return got.returncode, failed, (got.stdout.strip().splitlines() or [""])[-1]


if __name__ == "__main__":
    WT, SCRATCH = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve()
    code, failed, tail = run("unmutated", [])
    print(f"unmutated: rc={code} {tail}")
    assert code == 0, failed
    survivors = []
    for name, changes in MUTANTS.items():
        code, failed, tail = run(name, changes)
        print(
            f"{'SURVIVED' if code == 0 else 'killed  '} {name}"
            + (f"  <- {failed[0].split(' - ')[0]}" if failed else "")
        )
        survivors += [name] if code == 0 else []
    print(f"{len(MUTANTS)} mutants, {len(survivors)} survived")
