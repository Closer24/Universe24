"""The decoder's source mutants against its tests (Animate): every mutant must fail tests/test_the_tensor24_decoder.py.

usage: python -I mutants.py <worktree> <scratch folder>
Each mutant is one or more textual changes in a scratch copy of src/tensor24, tools/tensor24_decode.py and the decoder's
test; "killed" names the first test that fails with it, "SURVIVED" means all of them pass. The mutants: each guard of
the record and of the ledger dropped from its tuple; each part of each rule, reading and verdict changed; the fifth
hostile review's sixteen and the seventh's eighteen as they read on this text (decoder_mutants.py and
decoder_mutants_s8.py there); and the tool's lines.
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
GUARDS = (
    "jsoned",
    "framed",
    "headed",
    "majored",
    "ended",
    "kinded",
    "placed",
    "shaped",
    "valued",
    "booked",
    "ordered",
)
LEDGER_GUARDS = ("objects", "standing", "fitted", "once")
AGREE = "agree = sum(sum(step.values()) == sum(clicks.values()) for step, clicks in read)"
SHOWN_IF = '    if opened or agree < read:\n        return verdict("NOT SHOWN", books, lacks, wind, first=first, second=second)\n'
READ_IF = '    if lacking or read < rounds:\n        partly = lines if read < rounds else ""\n        return verdict("NOT READ", lacks, "" if lacking else books, partly, first=first, second=second)\n'
OWN = 'own = not whole(click.get("train")) or click["train"] in trains'


def dropped(name):
    """A guard dropped from its tuple."""
    if name in GUARDS:
        return [(REC, f"    {name},\n", "")]
    kept = ", ".join(g for g in LEDGER_GUARDS if g != name)
    return [
        (
            REC,
            f"LEDGER_GUARDS: tuple[Guard, ...] = ({', '.join(LEDGER_GUARDS)})",
            f"LEDGER_GUARDS: tuple[Guard, ...] = ({kept})",
        )
    ]


def gone(path, text):
    """One line or more of text taken out."""
    return [(path, text, "")]


MUTANTS = {
    **{f"the guard {g} dropped": dropped(g) for g in (*GUARDS, *LEDGER_GUARDS)},
    # the parse and the file
    "a line with no kind let through": [
        (
            REC,
            'if isinstance(line, str) or not isinstance(line.get("kind"), str):',
            "if isinstance(line, str):",
        )
    ],
    "a key twice read as its last value": [
        (REC, "return line if len(line) == len(pairs) else None", "return line")
    ],
    "the depth's cause unnamed": [
        (REC, '        return "nests past the interpreter\'s depth"', "        return NO_JSON")
    ],
    "the digits' cause unnamed": [
        (
            REC,
            '        return "holds a whole number past the interpreter\'s digits"',
            "        return NO_JSON",
        )
    ],
    "the depth and the digits raise": [
        (REC, "    except RecursionError:", "    except ZeroDivisionError:"),
        (REC, "    except ValueError:\n", "    except ZeroDivisionError:\n"),
    ],
    "a JSON value that is no object let through": [
        (REC, "return line if isinstance(line, dict) else NO_JSON", "return line")
    ],
    "the lines split by splitlines": [
        (
            REC,
            'texts = f.read().split("\\n")',
            'texts = f.read().splitlines()\n            texts.append("")',
        )
    ],
    "the file read with universal newlines": [(REC, 'encoding="utf-8", newline=""', 'encoding="utf-8"')],
    "the last line feed read as a line": [(REC, '(texts[:-1] if texts[-1] == "" else texts)', "texts")],
    "a file's cause unnamed": [(REC, 'cause = cause and f"the {whose} file {cause}"', "cause = cause")],
    "a path holding a NUL raises": [(REC, "    except OSError, ValueError:", "    except OSError:")],
    # the frame, the header, the end, the kinds and the places
    "an empty file let through the frame": [
        (REC, 'len(lines) < len(("header", "end"))', "len(lines) < 1")
    ],
    "a newer major read": [(REC, "if major != schema.MAJOR else", "if major < schema.MAJOR else")],
    "the two causes of the major swapped": [
        (
            REC,
            'return "the header holds no major version"',
            'return f"the major version {major} is unknown"',
        )
    ],
    "a major that is no whole number read by its value": [
        (REC, "if not whole(major):", "if major is None:")
    ],
    "the header's and end's kinds read as events' kinds": [
        (
            REC,
            '{e["kind"] for e in events_of(lines)} - set(KINDS)',
            '{e["kind"] for e in lines if isinstance(e, dict)} - set(KINDS)',
        )
    ],
    "the broken line named one on": [
        (
            REC,
            "    for n, line in enumerate(lines, start=1):\n        if isinstance(line, str) and line != NO_JSON:",
            "    for n, line in enumerate(lines, start=1 + 1):\n        if isinstance(line, str) and line != NO_JSON:",
        )
    ],
    "the unplaced event named one back": [
        (REC, "enumerate(events, start=1 + 1)", "enumerate(events, start=1)")
    ],
    "an event's round not checked": [(REC, 'PLACE = ("round", "site")', 'PLACE = ("site",)')],
    "the order read by round and kind alone": [
        (
            REC,
            'return round_, KINDS.index(e["kind"]), site, train',
            'return round_, KINDS.index(e["kind"]), 0, 0',
        )
    ],
    "the order read without the train": [
        (
            REC,
            'return round_, KINDS.index(e["kind"]), site, train',
            'return round_, KINDS.index(e["kind"]), site, 0',
        )
    ],
    "the kinds' order changed": [
        (
            REC,
            'KINDS = ("whole", "split", "turnover", "rate", "books")',
            'KINDS = ("whole", "split", "rate", "turnover", "books")',
        )
    ],
    # the shapes (G1, G2)
    "a truth value read as a whole number": [
        (
            REC,
            "    if shape is int:\n        return whole(value)\n",
            "    if shape is int:\n        return isinstance(value, int)\n",
        )
    ],
    "a float read as a whole number": [
        (
            REC,
            "    if shape is int:\n        return whole(value)\n",
            "    if shape is int:\n        return isinstance(value, int | float)\n",
        )
    ],
    "a label's shape not read": [
        (
            REC,
            "    if shape is str:\n        return isinstance(value, str)\n",
            "    if shape is str:\n        return True\n",
        )
    ],
    "a row of any length": gone(REC, "        and len(value) == len(rows)\n"),
    "a record of the schema read as any mapping": [
        (
            REC,
            "return isinstance(value, dict) and not misfit(value, shapes[shape.__name__.lower()], shapes)",
            "return isinstance(value, dict)",
        )
    ],
    "the header and the end not shaped": [
        (
            REC,
            'if isinstance(line, dict) and line["kind"] in shapes',
            'if isinstance(line, dict) and line["kind"] in KINDS',
        )
    ],
    "the last misfit field named": [
        (REC, 'return wrong[0] if wrong else ""', 'return wrong[-1] if wrong else ""')
    ],
    "a field the schema does not name not read": [
        (
            REC,
            "unnamed = [name for name, value in line.items() if name not in fields and not leaves(value)]",
            "unnamed: list[str] = []",
        )
    ],
    "a float let through an unnamed field": [
        (
            REC,
            "elif not (whole(item) or isinstance(item, str)):",
            "elif not (whole(item) or isinstance(item, str | float)):",
        )
    ],
    "an unnamed row not walked": [
        (
            REC,
            "        elif isinstance(item, list):\n            left += item\n",
            "        elif isinstance(item, list):\n            pass\n",
        )
    ],
    # the values
    "rounds not read": [
        (REC, 'if event and whole(rounds) and not 1 <= line["round"] <= rounds:', "if False:")
    ],
    "a round 0 read": [(REC, 'not 1 <= line["round"] <= rounds', 'not 0 <= line["round"] <= rounds')],
    "sites not read": [(REC, "    if far:", "    if False:")],
    "an end's or a child's site not read": [(REC, 'for key in ("ends", "children")', "for key in ()")],
    "Spokes not read": [(REC, "    if wide:", "    if False:")],
    "the board's sites the sum of its sides": [
        (REC, "        sites = sites * side\n", "        sites = sites + side\n")
    ],
    "the board's sites its last side": [
        (REC, "        sites = sites * side\n", "        sites = side\n")
    ],
    "the board's Spokes one a side": [
        (REC, "return sites, len(sides) + len(sides)", "return sites, len(sides)")
    ],
    "a count of 0 read": [(REC, 'line["count"] < 1', 'line["count"] < 0')],
    # the books' guard (G3)
    "a click booked at the click and its ends read": [
        (REC, 'if ends and (click.get("taken") or click.get("laid")):', "if False:")
    ],
    "a click booked again in its laid alone read": [
        (
            REC,
            'if ends and (click.get("taken") or click.get("laid")):',
            'if ends and click.get("taken"):',
        )
    ],
    "a click with one end read": [(REC, "if ends and len(ends) != len(ENDS):", "if False:")],
    "a click with three ends read": [
        (REC, "if ends and len(ends) != len(ENDS):", "if ends and len(ends) < len(ENDS):")
    ],
    # the ledger's guards
    "the ledger's at not read": [(REC, ' and line.get("at") in AT)', ")")],
    "a ledger line's round and train not read": [(REC, 'ENTRY = ("round", "train")', "ENTRY = ()")],
    "a ledger line's train not read": [(REC, 'ENTRY = ("round", "train")', 'ENTRY = ("round",)')],
    "a ledger line's fields' shapes not read": [
        (REC, 'if isinstance(line, dict) and misfit(line, shapes["ledger"], shapes)', "if False")
    ],
    "a ledger line at the place of an earlier one read": [
        (REC, "if earliest[entry] != n]", "if earliest[entry] != earliest[entry]]")
    ],
    # the first reading: the books hold the click
    "the books close at any end": [(BOOKS, "    each = all(\n", "    each = any(\n")],
    "a part that takes nothing read": gone(BOOKS, '        p["taken"]\n        and '),
    "a take that gains read": gone(BOOKS, '        and all(gained([h]) < 0 for h in p["taken"])\n'),
    "a laid holding that loses read": gone(
        BOOKS, '        and all(gained([h]) > 0 for h in p["laid"])\n'
    ),
    "the books close over the two ends together": [
        (
            BOOKS,
            '        and gained(p["taken"]) + gained(p["laid"]) == 0\n        for p in parts(click)\n    )\n',
            '        for p in parts(click)\n    ) and sum(gained(p["taken"]) + gained(p["laid"]) for p in parts(click)) == 0\n',
        )
    ],
    "the click's own train not read": [(BOOKS, OWN, "own = True")],
    "q not read": [
        (BOOKS, 'counted = not whole(click.get("q")) or click["q"] == left(click)', "counted = True")
    ],
    "q read with the kept": [
        (
            BOOKS,
            'return sum(h["windings"][0] - h["windings"][1] for p in parts(click) for h in p["taken"])',
            'return sum(h["windings"][0] - h["windings"][1] + h["kept"][0] - h["kept"][1] for p in parts(click) for h in p["taken"])',
        )
    ],
    "a click's lacking ends read": [(BOOKS, '        "ends" in click\n        and ', "        ")],
    "a holding's lacking fields read": gone(
        BOOKS, "        and all(key in h for h in held for key in HELD)\n"
    ),
    "a holding's lacking train read": [
        (BOOKS, 'HELD = ("train", "windings", "kept")', 'HELD = ("windings", "kept")')
    ],
    "a holding's lacking windings read": [
        (BOOKS, 'HELD = ("train", "windings", "kept")', 'HELD = ("train", "kept")')
    ],
    "a laid holding's lacking fields read": [
        (
            BOOKS,
            "held = [h for p in sides for key in BOOKS for h in p.get(key, [])]",
            'held = [h for p in sides for h in p.get("taken", [])]',
        )
    ],
    # the second reading: the wind over every train of the header
    "the trains the ledger lists read in place of the header's": [
        (
            BOOKS,
            "        and set(step) == set(clicks) == trains\n",
            "        and set(step) == set(clicks)\n",
        )
    ],
    "a round read whose clicks lines hold more trains than the step's": [
        (
            BOOKS,
            "        and set(step) == set(clicks) == trains\n",
            "        and set(step) <= set(clicks)\n",
        )
    ],
    "a header that names no train read": [
        (BOOKS, "        if trains\n        and set", "        if True\n        and set")
    ],
    "a split click's round not read": [(BOOKS, 'CLICKS = ("whole", "split")', 'CLICKS = ("whole",)')],
    "a round read whose wind is no whole number": gone(
        BOOKS, "        and all(whole(w) for w in [*step.values(), *clicks.values()])\n"
    ),
    "the clicks lines' wind not read whole": [
        (
            BOOKS,
            "and all(whole(w) for w in [*step.values(), *clicks.values()])",
            "and all(whole(w) for w in step.values())",
        )
    ],
    "the ledger agreeing at least": [(BOOKS, AGREE, AGREE.replace(" == ", " >= "))],
    "the ledger agreeing at most": [(BOOKS, AGREE, AGREE.replace(" == ", " <= "))],
    "the round dropped": [
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
    # the verdict
    "SHOWN wherever the ledger agrees": [
        (BOOKS, "    if opened or agree < read:\n", "    if agree < read:\n")
    ],
    "SHOWN wherever the record reads": [(BOOKS, "    if opened or agree < read:\n", "    if False:\n")],
    "the ledger absent read as an empty ledger": [
        (
            BOOKS,
            "    if ledger is None:\n",
            "    if ledger is None:\n        ledger = []\n    if ledger is None:\n",
        )
    ],
    "a header that names no train not named": [
        (BOOKS, '    if not second["trains"]:\n', "    if False:\n")
    ],
    "the ledger shown where it is read at some rounds alone": [
        (BOOKS, "    if lacking or read < rounds:\n", "    if lacking:\n")
    ],
    "a click that lacks its books read among the others": [
        (BOOKS, "    if lacking or read < rounds:\n", "    if read < rounds:\n")
    ],
    "a click that lacks its books hiding an open one": [(BOOKS, SHOWN_IF + READ_IF, READ_IF + SHOWN_IF)],
    "the lines named where every round with a click reads": [
        (BOOKS, 'partly = lines if read < rounds else ""', "partly = lines")
    ],
    "the lines not named where a round with a click is not read": [
        (BOOKS, 'partly = lines if read < rounds else ""', 'partly = ""')
    ],
    "the books named beside a click that lacks a field": [
        (BOOKS, '"" if lacking else books, partly', "books, partly")
    ],
    "the books not named where the ledger is read in part": [
        (BOOKS, '"" if lacking else books, partly', '"", partly')
    ],
    # the ticks
    "the rate lines read by the round": [
        (
            CLOCKS,
            'append((line.get("count"), line.get("k")))',
            'append((line.get("round"), line.get("k")))',
        )
    ],
    "the rate lines of every Node-clock read as one": [
        (CLOCKS, 'by_site.setdefault(line["site"], [])', "by_site.setdefault(0, [])")
    ],
    "no rate line read": gone(
        CLOCKS, '    if not lines:\n        return "its Node-clock holds no rate line"\n'
    ),
    "a rate line's lacking k read": [
        (
            CLOCKS,
            "if not all(whole(c) and whole(k) for c, k in lines):",
            "if not all(whole(c) for c, k in lines):",
        )
    ],
    "a k that is no bit read": [(CLOCKS, "    if not all(k in BIT for k in ks):", "    if False:")],
    "the first rate line read at any beat": [(CLOCKS, "    if counts[0] != 1:", "    if False:")],
    "rate lines that do not rise read": [
        (
            CLOCKS,
            "    if not all(a < b for a, b in zip(counts, counts[1:], strict=False)):",
            "    if False:",
        )
    ],
    "a repeated k read": [
        (CLOCKS, "    if not all(a != b for a, b in zip(ks, ks[1:], strict=False)):", "    if False:")
    ],
    "a negative count read": [(CLOCKS, "if not whole(count) or count < 0:", "if not whole(count):")],
    "a stretch's ticks counted one beat on": [
        (CLOCKS, "before[-1] + k * (following - start)", "before[-1] + k * (following - start + 1)")
    ],
    "a count's own beat not counted": [
        (CLOCKS, "ks[at] * (count - starts[at] + 1)", "ks[at] * (count - starts[at])")
    ],
    "a count read at the stretch before": [
        (CLOCKS, "bisect.bisect_right(starts, count) - 1", "bisect.bisect_left(starts, count) - 1")
    ],
    # the tool
    "the tool takes four arguments": [
        (TOOL, "    if not named or named[1 + 1 :]:", "    if not named:")
    ],
    "the tool keeps the interpreter's digits": gone(TOOL, "    sys.set_int_max_str_digits(0)\n"),
    "the tool reads on past a record not read": [
        (
            TOOL,
            '        print(f"not read: {cause}")\n        return 0\n',
            '        print(f"not read: {cause}")\n',
        )
    ],
    "the tool names no first click not read": [
        (TOOL, "        if unread\n        else", "        if False\n        else")
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
