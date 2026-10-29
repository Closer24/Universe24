"""The decoder's source mutants against its tests (Animate): every mutant must fail tests/test_the_tensor24_decoder.py
or tests/test_the_tensor24_decoder_cases.py.

usage: python -I mutants.py <worktree> <scratch folder>
Each mutant is one or more textual changes in a scratch copy of src/tensor24, tools/tensor24_decode.py and the decoder's
two tests; "killed" names the first test that fails with it, "SURVIVED" means all of them pass. The mutants: each guard
of the record and of the ledger dropped from its tuple; each part of each rule, reading and verdict changed; the fifth
hostile review's sixteen, the seventh's eighteen and the twelfth's twenty-five as they read on this text
(decoder_mutants.py, decoder_mutants_s8.py and mutants_s13.py there); the Boss's ruling on A3 and A4; David's A6, each
train's windings at its own winding, with the header's train cards; row 46, each later bang shows more; and the tool's
lines.
"""

import shutil
import subprocess
import sys
from pathlib import Path

REC, BOOKS, CLOCKS, BANGS, TOOL = (
    "src/tensor24/decoder/records.py",
    "src/tensor24/decoder/books.py",
    "src/tensor24/decoder/clocks.py",
    "src/tensor24/decoder/bangs.py",
    "tools/tensor24_decode.py",
)
TESTS = (
    "tests/test_the_tensor24_decoder.py",
    "tests/test_the_tensor24_decoder_cases.py",
    "tests/test_the_tensor24_decoder_bangs.py",
)
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
SHOWN_IF = '    if opened or agree < read:\n        return verdict("NOT SHOWN", books, lacks, wind or barred or lines, **readings)\n'
READ_IF = '    if lacking or lines:\n        return verdict("NOT READ", lacks, "" if lacking else books, lines, **readings)\n'
WALL_IF = '    if barred:\n        return verdict("NOT READ", barred, books, lacks, **readings)\n'
BESIDE = "wind or barred or lines, **readings"
OWN = 'own = click.get("train") in trains'
CHAIN = 'elif h["windings"][0] == last["windings"][1] and h["kept"][0] == last["kept"][1]:'
SIDES = 'taken, laid = chained(part["taken"]), chained(part["laid"])'
LEFT = 'return sum(h["windings"][0] - h["windings"][1] for p in parts(click) for h in p["taken"])'
UNWOUND_IF = '    if not all(h["train"] in winding for h in held):\n        return UNWOUND\n'


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
            'KINDS = ("whole", "split", "rate", "books")',
            'KINDS = ("rate", "split", "whole", "books")',
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
        (REC, "return sides, sites, len(sides) + len(sides)", "return sides, sites, len(sides)")
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
    "the books close at any end": [(BOOKS, "each = all(part_closes", "each = any(part_closes")],
    "a part that takes nothing read": [(BOOKS, "        bool(taken)\n", "        True\n")],
    "a take that gains read": gone(BOOKS, "        and all(gained([h], winding) < 0 for h in taken)\n"),
    "a laid holding that loses read": gone(
        BOOKS, "        and all(gained([h], winding) > 0 for h in laid)\n"
    ),
    "the books close over the two ends together": [
        (BOOKS, "        and gained(taken, winding) + gained(laid, winding) == 0\n", ""),
        (
            BOOKS,
            "    each = all(part_closes(p, winding) for p in parts(click))\n",
            '    each = all(part_closes(p, winding) for p in parts(click)) and sum(gained(p["taken"], winding) + gained(p["laid"], winding) for p in parts(click)) == 0\n',
        ),
    ],
    "the click's own train not read": [(BOOKS, OWN, "own = True")],
    "q not read": [
        (BOOKS, 'counted = not whole(click.get("q")) or click["q"] == left(click)', "counted = True")
    ],
    "q read with the kept": [
        (
            BOOKS,
            LEFT,
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
            "held = [h for p in held_by for key in BOOKS for h in p.get(key, [])]",
            'held = [h for p in held_by for h in p.get("taken", [])]',
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
            "second = None if ledger is None else second_reading(record, ledger)",
            "second = second_reading(record, [] if ledger is None else ledger)",
        )
    ],
    "a header that names no train not named": [
        (BOOKS, 'return "" if second["trains"] else "the header names no train"', 'return ""')
    ],
    "the ledger shown where it is read at some rounds alone": [
        (BOOKS, "    if lacking or lines:\n", "    if lacking:\n")
    ],
    "a click that lacks its books read among the others": [
        (BOOKS, "    if lacking or lines:\n", "    if lines:\n")
    ],
    "a click that lacks its books hiding an open one": [
        (BOOKS, READ_IF, ""),
        (BOOKS, SHOWN_IF, READ_IF + SHOWN_IF),
    ],
    "the lines named where every round with a click reads": [
        (BOOKS, "        if not barred and read < rounds\n", "        if not barred\n")
    ],
    "the lines not named where a round with a click is not read": [
        (BOOKS, "        if not barred and read < rounds\n", "        if False\n")
    ],
    "the books named beside a click that lacks a field": [
        (BOOKS, '"" if lacking else books, lines', "books, lines")
    ],
    "the books not named where the ledger is read in part": [
        (BOOKS, '"" if lacking else books, lines', '"", lines')
    ],
    # the twelfth review's changes: the values where the line's record names them, the names in ASCII, the board by its
    # sides, the books per train, and the verdict's order with the gap named beside the open books
    "a line's ends and children read on every kind": [
        (REC, " if key in fields for part in line.get(key, [])", " for part in line.get(key, [])")
    ],
    "a line's ends' Spokes read on every kind": [
        (REC, 'ends = line.get("ends", []) if "ends" in fields else []', 'ends = line.get("ends", [])')
    ],
    "a count read on every kind": [
        (REC, 'if "count" in fields and whole(line.get("count"))', 'if whole(line.get("count"))')
    ],
    "the board named by its sites": [
        (REC, 'off the board of sides {sides}"', 'off the board of {size} sites"')
    ],
    "a side below 1 read": [
        (REC, "    if made[0] and not all(side >= 1 for side in made[0]):\n", "    if False:\n")
    ],
    "a side of 0 read": [(REC, "side >= 1 for side", "side >= 0 for side")],
    "a field's name printed raw": [(REC, "{ascii(found[0][1])[1:-1]}", "{found[0][1]}")],
    "a kind printed raw": [(REC, "{ascii(unknown)}", "{unknown}")],
    "a chain read on its windings alone": [(BOOKS, CHAIN, CHAIN.split(" and ")[0] + ":")],
    "a chain read on its kept alone": [(BOOKS, CHAIN, "elif " + CHAIN.split(" and ")[1])],
    "any two holdings of a train read as a chain": [(BOOKS, CHAIN, "elif True:")],
    "a taken train listed twice read": [
        (BOOKS, SIDES, 'taken, laid = part["taken"], chained(part["laid"])')
    ],
    "a laid train listed twice read": [
        (BOOKS, SIDES, 'taken, laid = chained(part["taken"]), part["laid"]')
    ],
    "a train on both sides of a part read": [
        (BOOKS, ' or {h["train"] for h in taken} & {h["train"] for h in laid}', "")
    ],
    "a part that books a train twice closes": [
        (
            BOOKS,
            "    if held is None:\n        return False\n",
            "    if held is None:\n        return True\n",
        )
    ],
    "a click that books a train twice read": [
        (BOOKS, 'return TWICE if any(per_train(p) is None for p in parts(click)) else ""', 'return ""')
    ],
    "a pair that books a train twice at one end read": [
        (BOOKS, "TWICE if any(per_train", "TWICE if all(per_train")
    ],
    "the gap not named beside open books": [(BOOKS, BESIDE, "wind, **readings")],
    "the wall not named beside open books": [(BOOKS, BESIDE, "wind or lines, **readings")],
    "the lines not named beside open books": [(BOOKS, BESIDE, "wind or barred, **readings")],
    "the wind not named beside open books": [(BOOKS, BESIDE, "barred or lines, **readings")],
    "the wall read after a ledger read at no round": [
        (BOOKS, WALL_IF, ""),
        (BOOKS, "    if lacking or lines:\n", WALL_IF + "    if lacking or lines:\n"),
    ],
    "a train card counted from 0": [
        (
            BOOKS,
            'enumerate(record.header.get("trains", []), start=1)',
            'enumerate(record.header.get("trains", []), start=0)',
        )
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
    # the Boss's ruling of 04:4x UTC (6488101036, A3 and A4): a whole click's q at least 1, every holding's windings from 0
    "a whole click's q below 1 read": [
        (
            REC,
            '    if line["kind"] == "whole" and whole(line.get("q")) and line["q"] < 1:\n',
            "    if False:\n",
        )
    ],
    "a whole click's q of 0 read": [(REC, 'line["q"] < 1:', 'line["q"] < 0:')],
    "the q rule read on every kind": [
        (REC, 'line["kind"] == "whole" and whole(line.get("q"))', 'whole(line.get("q"))')
    ],
    "a holding's windings below 0 read": [
        (
            REC,
            '    return f"holds a holding\'s windings {low[0]}, below 0" if low else ""\n',
            '    return ""\n',
        )
    ],
    "a holding's windings of 0 refused": [(REC, "if whole(w) and w < 0]", "if whole(w) and w < 1]")],
    "an end's holdings not read for their windings": [
        (REC, "for part in [line, *ends] for key in BOOKED", "for part in [line] for key in BOOKED")
    ],
    "the laid holdings not read for their windings": [
        (REC, "for key in BOOKED if key in fields", "for key in BOOKED[:1] if key in fields")
    ],
    # David's A6 (6488889537, item 2): each train's windings at its own winding, as the header's train cards give it
    "the books read unweighted": [(BOOKS, ' * winding[h["train"]]', "")],
    "the kept weighed too": [
        (
            BOOKS,
            '+ h["kept"][1] - h["kept"][0]\n',
            '+ (h["kept"][1] - h["kept"][0]) * winding[h["train"]]\n',
        )
    ],
    "every holding at the first card's winding": [
        (BOOKS, 'winding[h["train"]]', "next(iter(winding.values()))")
    ],
    "a train with no winding read at 1 (the patch's default)": [
        (BOOKS, 'winding[h["train"]]', 'winding.get(h["train"], 1)'),
        (BOOKS, UNWOUND_IF, ""),
    ],
    "a train with no winding read (its check dropped)": [(BOOKS, UNWOUND_IF, "")],
    "a card's winding read without its index": [
        (BOOKS, 'if whole(t.get("index")) and whole(t.get("winding"))', 'if whole(t.get("winding"))')
    ],
    "a card's index read without its winding": [
        (BOOKS, 'if whole(t.get("index")) and whole(t.get("winding"))', 'if whole(t.get("index"))')
    ],
    "row 15's lacking read with no windings": [
        (BOOKS, "    winding = windings_of(record)\n    lacking", "    winding = {}\n    lacking")
    ],
    "the books named closed where none is read": [
        (BOOKS, '        if lacking and first["read"]\n', "        if lacking\n")
    ],
    "the cards' rule dropped from the guard": [
        (REC, '    if cards:\n        return f"line 1\'s {cards}"\n', "")
    ],
    "a card's winding below 1 read": [
        (
            REC,
            '        return f"train card {low[0][0]} holds the winding {low[0][1]}, below 1"\n',
            '        return ""\n',
        )
    ],
    "a card's winding of 0 read": [(REC, 't["winding"] < 1', 't["winding"] < 0')],
    "a train on two cards read": [
        (REC, "twice = [i for n, i in enumerate(trains) if i in trains[:n]]", "twice = []")
    ],
    # row 46, each later bang shows more (the owner's word to Animate of 06:3x UTC: "ever more complex clocks")
    "a composite at its deepest part's depth": [
        (
            BANGS,
            "found[train] = 1 + max(found[p] for p in of)",
            "found[train] = max(found[p] for p in of)",
        )
    ],
    "an elementary train at depth 1": [
        (BANGS, "for p in of) if of else 0", "for p in of) if of else 1")
    ],
    "a part that is a row read": [(BANGS, '        and all(whole(p) for p in t["parts"])\n', "")],
    "a bottom held two rounds missed": [(BANGS, "load[n] <= load[n - 1]", "load[n] < load[n - 1]")],
    "a bottom counted twice where it is held": [
        (BANGS, "load[n] < load[n + 1]", "load[n] <= load[n + 1]")
    ],
    "a bang closing at its next bottom": [
        (BANGS, "(rounds[a], rounds[b] - 1)", "(rounds[a], rounds[b])")
    ],
    "the first bang dropped": [(BANGS, "starts = [0, *bottoms(load)]", "starts = bottoms(load)")],
    "an end's lays not read": [(BANGS, 'parts = [click, *click.get("ends", [])]', "parts = [click]")],
    "a click's children not read": [(BANGS, '[*holdings, *click.get("children", [])]', "holdings")],
    "a split click not counted": [(BANGS, 'CLICKS = ("whole", "split")', 'CLICKS = ("whole",)')],
    "the click kinds by kind alone": [
        (
            BANGS,
            'kinds = {(e["kind"], e.get("train")) for e in clicks}',
            'kinds = {e["kind"] for e in clicks}',
        )
    ],
    "a bang's clicks read past its last round": [
        (BANGS, 'first <= e["round"] <= last', 'first <= e["round"]')
    ],
    "the clocks held read after the step": [
        (
            BANGS,
            'at = "clicks" if any(line["at"] == "clicks" for line in lines) else "step"',
            'at = "step"',
        )
    ],
    "a winding of 0 held": [(BANGS, 'line["windings"] > 0', 'line["windings"] >= 0')],
    "no time gear read as one": [
        (BANGS, '    if not whole(gear):\n        return [], "the header names no time gear"\n', "")
    ],
    "the load read after the clicks too": [
        (BANGS, 'if line["at"] == "step" and line["train"] == gear', 'if line["train"] == gear')
    ],
    "one bang whole compared": [(BANGS, "if len(found) < 1 + 1:", "if len(found) < 1:")],
    "a clock of no depth read": [(BANGS, "    if deep:\n", "    if False:\n")],
    "a bang shows more only by both": [
        (
            BANGS,
            "kinds[n] > kinds[n - 1] or laid_deepest[n] > laid_deepest[n - 1]",
            "kinds[n] > kinds[n - 1] and laid_deepest[n] > laid_deepest[n - 1]",
        )
    ],
    "a later bang against the first": [
        (
            BANGS,
            "more = kinds[n] >= kinds[n - 1] and laid_deepest[n] >= laid_deepest[n - 1]",
            "more = kinds[n] >= kinds[0] and laid_deepest[n] >= laid_deepest[0]",
        ),
        (
            BANGS,
            "kinds[n] > kinds[n - 1] or laid_deepest[n] > laid_deepest[n - 1]",
            "kinds[n] > kinds[0] or laid_deepest[n] > laid_deepest[0]",
        ),
    ],
    "a held clock's fall not read": [
        (BANGS, "        if held_deepest[n] < held_deepest[n - 1]:\n", "        if False:\n")
    ],
    "the tool prints no row 46": [
        (TOOL, '    print(f"row 46: {bangs.row_46(record, ledger, why)}")\n', "")
    ],
    # the twelfth hostile review's twenty-five (mutants_s13.py there), as they read on this text
    "a negative site read": [
        (REC, "whole(size) and not 0 <= s < size]", "whole(size) and not s < size]")
    ],
    "a negative Spoke read": [(REC, "if not 0 <= s < spokes]", "if not s < spokes]")],
    "a child's site not read (the ends' read)": [
        (REC, 'for key in ("ends", "children")', 'for key in ("ends",)')
    ],
    "the line's own round, site and count read on rate lines alone": [
        (REC, 'event = line["kind"] in KINDS', 'event = line["kind"] == "rate"')
    ],
    "a count before the first beat read but on a rate line": [
        (
            REC,
            'if "count" in fields and whole(line.get("count"))',
            'if line["kind"] == "rate" and whole(line.get("count"))',
        )
    ],
    "an end without its rounds raises": [
        (
            REC,
            'if event and whole(rounds) and not 1 <= line["round"] <= rounds:',
            'if event and not 1 <= line["round"] <= rounds:',
        )
    ],
    "an end or child without its site raises": [
        (
            REC,
            "far = [s for s in sites if whole(s) and whole(size)",
            "far = [s for s in sites if whole(size)",
        )
    ],
    "an end without its Spoke raises": [(REC, "if whole(s) and whole(spokes)]", "if whole(spokes)]")],
    "a kind that is no label let through (absent alone refused)": [
        (
            REC,
            'if isinstance(line, str) or not isinstance(line.get("kind"), str):',
            'if isinstance(line, str) or "kind" not in line:',
        )
    ],
    "an unnamed mapping not walked": [
        (
            REC,
            "        if isinstance(item, dict):\n            left += item.values()\n",
            "        if isinstance(item, dict):\n            pass\n",
        )
    ],
    "an unnamed row refused": [
        (
            REC,
            "        elif isinstance(item, list):\n            left += item\n",
            "        elif isinstance(item, list):\n            return False\n",
        )
    ],
    "a taken holding that keeps its windings read": [
        (
            BOOKS,
            "all(gained([h], winding) < 0 for h in taken)",
            "all(gained([h], winding) <= 0 for h in taken)",
        )
    ],
    "a laid holding that gains nothing read": [
        (
            BOOKS,
            "all(gained([h], winding) > 0 for h in laid)",
            "all(gained([h], winding) >= 0 for h in laid)",
        )
    ],
    "q read as at most the windings that left": [
        (BOOKS, 'click["q"] == left(click)', 'click["q"] <= left(click)')
    ],
    "a click without its train read (its train not asked)": gone(
        BOOKS, '        and "train" in click\n'
    ),
    "q read over the click's own books, not its ends": [
        (BOOKS, LEFT, LEFT.replace("for p in parts(click)", "for p in [click]"))
    ],
    "a gap before the books' failure (the docstring's order)": [
        (BOOKS, "    if opened or agree < read:\n", "    if read and (opened or agree < read):\n")
    ],
    "the clicks lines may hold a train the header lacks (the step's held to the header)": [
        (
            BOOKS,
            "        and set(step) == set(clicks) == trains\n",
            "        and set(step) <= set(clicks)\n        and set(step) == trains\n",
        )
    ],
    "a train card without its index raises": [
        (
            BOOKS,
            'trains = {t["index"] for t in cards} if indexed else set()',
            'trains = {t["index"] for t in cards}',
        )
    ],
    "a count before the first beat named unread (ticks_to still 0)": [
        (CLOCKS, "if not whole(count) or count < 0:", "if not whole(count) or count < 1:")
    ],
    "the tool reads every click against the first click's Node-clock": [
        (
            TOOL,
            "clocks.ticks_at(lines.get(site, []),",
            'clocks.ticks_at(lines.get(clicks[0]["site"], []),',
        )
    ],
    "the tool matches a Node-clock's counts to its clicks backward": [
        (TOOL, "                ats,\n", "                ats[::-1],\n")
    ],
    "the tool's last read is its first": [
        (TOOL, "the last read {read[-1:]}", "the last read {read[:1]}")
    ],
    "the tool counts a click of 0 ticks as not read": [
        (TOOL, "if found[at] is not None]", "if found[at]]")
    ],
    "the tool names the last click not read as the first": [
        (
            TOOL,
            "f\", the first not read at round {unread[0]['round']}, site {unread[0]['site']}: \"",
            "f\", the first not read at round {unread[-1]['round']}, site {unread[-1]['site']}: \"",
        )
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
    for test in TESTS:
        shutil.copy(WT / test, tree / test)
    shutil.copy(WT / TOOL, tree / TOOL)
    (tree / "pytest.ini").write_text("[pytest]\naddopts = --import-mode=importlib\npythonpath = src\n")
    for rel, old, new in changes:
        path = tree / rel
        text = path.read_text()
        assert text.count(old) == 1, (name, old)
        path.write_text(text.replace(old, new))
    got = subprocess.run(
        [sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider", "-x", *TESTS],
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
