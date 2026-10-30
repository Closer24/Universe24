"""Tensor24's decoder, its second file: the twelfth hostile review's cases, each read as the plan, the schema and the
decoder's own comments say, nothing raised, and each failing on the reader's mutant it was written for."""

import json
import subprocess
import sys
from pathlib import Path

from tensor24.decoder import books, records

TOOL = Path(__file__).resolve().parent.parent / "tools" / "tensor24_decode.py"
TRAINS = [{"index": t, "label": f"train {t}", "kinds": [0], "part": 1, "winding": 1} for t in (0, 1)]
WOUND = dict.fromkeys(range(3), 1)  # each train's winding by its index: TRAINS', and train 2's at 1
H = {"kind": "header", "record": "tensor24", "major": 1, "minor": 1, "trains": TRAINS}
THIRD = {**H, "trains": [*TRAINS, {**TRAINS[1], "index": 2, "label": "train 2"}]}  # train 2's card added
B = {**H, "sides": [1 + 1, 1, 1]}  # a board of two sites on its x axis, and six Spokes
E = {"kind": "end", "rounds": 6, "undone": 0, "exact": 1}


def wound(*windings):  # the header with each of its trains' windings given, in turn
    return {**H, "trains": [{**t, "winding": w} for t, w in zip(TRAINS, windings, strict=True)]}


def hold(train, windings, kept=(0, 0)):
    return {"train": train, "windings": list(windings), "kept": list(kept)}


def click(round_, site, taken=(), laid=(), train=1, **more):
    """A whole click of a train, train 1 unless named, at the count of its round, its books at the click."""
    place = {"kind": "whole", "round": round_, "site": site, "count": round_, "train": train}
    return place | {"taken": list(taken), "laid": list(laid), "ends": []} | more


def end_of(site, taken, laid):
    return {"site": site, "spoke": 0, "taken": taken, "laid": laid, "push": [0, 0, 0]}


def rate(round_, site, count, k, **more):
    return {"kind": "rate", "round": round_, "site": site, "count": count, "dial": 0, "k": k} | more


def without(line, key):
    return {name: value for name, value in line.items() if name != key}


def ledger(round_, held):
    """Per train, its wind after the step and after the clicks at one round."""
    pairs = [
        (t, at, wind) for t, pair in held.items() for at, wind in zip(records.AT, pair, strict=True)
    ]
    return [{"round": round_, "at": at, "train": t, "wind": wind} for t, at, wind in pairs]


def write(lines, path):
    path.write_text("".join((x if isinstance(x, str) else json.dumps(x)) + "\n" for x in lines))
    return str(path)


def cause_of(lines, tmp_path):
    """The cause a record of the given lines is not read, or "" where it is read."""
    return records.read(write(lines, tmp_path / "record.jsonl"))[1]


def row(lines, held, tmp_path):
    """Row 15's verdict on a record of the given lines and a ledger (None where it is absent): its kind and cause."""
    record, cause = records.read(write(lines, tmp_path / "record.jsonl"))
    assert record is not None, cause
    verdict = books.row_15(record, held)
    return verdict["kind"], verdict["cause"]


# three windings and one kept of train 1 laid as four of train 0; a pair of train 0 taken at both ends into train 1
TAKE = click(1, 0, [hold(1, (7, 4), (3, 2))], [hold(0, (0, 4))])
# TAKE's round: the wind over every train 10 after the step and the clicks
GOOD = ledger(1, {0: (0, 4), 1: (10, 6)})
ENDED = [
    end_of(0, [hold(0, (5, 0), (0, 1))], [hold(1, (0, 4))]),
    end_of(1, [hold(0, (5, 0))], [hold(1, (0, 5))]),
]
PAIR = click(1, 0, train=0, ends=ENDED)
PAIRED = ledger(1, {0: (10, 1), 1: (0, 9)})
CHILD = {"train": 0, "site": 9, "sweep": 0, "push": [0, 0, 0], "moment": [0, 0, 0]}
SITE, SHAPE = (
    "line 2 names site {}, off the board of sides [2, 1, 1]",
    "line 2's {} has not its shape in the schema",
)
# the Boss's ruling of 04:4x UTC (6488101036): a whole click is the carry's quotient at least 1, and windings count from 0
Q_BELOW, LOW = (
    "line 2 holds the whole click's q {}, below 1",
    "line 2 holds a holding's windings {}, below 0",
)
BOOKED = {"kind": "books", "round": 1, "site": 0, "train": 0, "kept": 1}
WINDING = "line 1's train card {} holds the winding {}, below 1"
TWO_CARDS = "line 1's train cards name the train 0 twice"

READS = {  # each record read: a field the schema does not name holds whole numbers and labels, a field absent
    "a rate line's unnamed ends": [B, rate(1, 0, 1, 1, ends=[1]), E],
    "a rate line's unnamed children": [B, rate(1, 0, 1, 1, children="x"), E],
    "a rate line's unnamed ends off the board": [B, rate(1, 0, 1, 1, ends=[{"site": 9}]), E],
    "a rate line's unnamed q 0": [B, rate(1, 0, 1, 1, q=0), E],
    "a books line's unnamed children": [B, {**BOOKED, "children": [[1]]}, E],
    "a books line's unnamed count 0": [B, {**BOOKED, "count": 0}, E],
    "the header's unnamed ends": [{**B, "ends": [5]}, rate(1, 0, 1, 1), E],
    "an unnamed row of whole numbers": [H, rate(1, 0, 1, 1, note=[1, 1 + 1]), E],
    "an end without its rounds": [H, rate(1, 0, 1, 1), {"kind": "end"}],
    "a pair's end without its site": [B, {**PAIR, "ends": [ENDED[0], without(ENDED[1], "site")]}, E],
    "a pair's end without its Spoke": [B, {**PAIR, "ends": [ENDED[0], without(ENDED[1], "spoke")]}, E],
}
REFUSED = {  # each record not read, its own cause named
    "a rate line at a site below 0": ([B, rate(1, -1, 1, 1), E], SITE.format(-1)),
    "a whole click at a site off the board": ([B, {**TAKE, "site": 1 + 1}, E], SITE.format(1 + 1)),
    "a whole click past the end's rounds": (
        [H, {**TAKE, "round": 7}, E],
        "line 2 stands at round 7, off the record's rounds 1 to 6",
    ),
    "a child laid off the board": ([B, {**TAKE, "children": [CHILD]}, E], SITE.format(9)),
    "a pair's end at a Spoke below 0": (
        [B, {**PAIR, "ends": [ENDED[0], {**ENDED[1], "spoke": -1}]}, E],
        "line 2 names Spoke -1, off the board's Spokes 0 to 5",
    ),
    "a whole click at count 0": (
        [H, {**TAKE, "count": 0}, E],
        "line 2 holds the count 0, before the first beat",
    ),
    "a kind that is no label": (
        [H, {"kind": 1, "round": 1, "site": 0}, {"kind": "chime", "round": 1, "site": 0}, E],
        "line 2 is no JSON object with its kind",
    ),
    "a kind past ASCII": (
        [H, {"kind": "\xe9", "round": 1, "site": 0}, E],
        "the line kinds ['\\xe9'] are unknown",
    ),
    "a float in an unnamed mapping": ([H, rate(1, 0, 1, 1, note={"a": 0.5}), E], SHAPE.format("note")),
    "a side below 1": (
        [{**B, "sides": [1 + 1, -1, -1]}, rate(1, 1, 1, 1), E],
        "line 1's sides [2, -1, -1] make no board, a side below 1",
    ),
    "a side of 0": (
        [{**B, "sides": [1 + 1, 0, 1]}, rate(1, 1, 1, 1), E],
        "line 1's sides [2, 0, 1] make no board, a side below 1",
    ),
    "a whole click at q 0, no click": ([H, {**TAKE, "q": 0}, E], Q_BELOW.format(0)),
    "a train card's winding 0": ([wound(0, 1), TAKE, E], WINDING.format(1, 0)),
    "a train card's winding -4": ([wound(1, -4), TAKE, E], WINDING.format(1 + 1, -4)),
    "a train on two cards": ([{**H, "trains": [*TRAINS, TRAINS[0]]}, TAKE, E], TWO_CARDS),
    "a whole click at q -3 (A4)": ([H, {**TAKE, "q": -3}, E], Q_BELOW.format(-3)),
    "a take below 0 (A3)": (
        [H, click(1, 0, [hold(1, (0, -3))], [hold(0, (0, 3))], q=3), E],
        LOW.format(-3),
    ),
    "an end's laid holding below 0": (
        [H, {**PAIR, "ends": [ENDED[0], end_of(1, [hold(0, (5, 0))], [hold(1, (-1, 4))])]}, E],
        LOW.format(-1),
    ),
    "a field named with a line feed": ([H, {**rate(1, 0, 1, 1), "a\nb": 0.5}, E], SHAPE.format("a\\nb")),
    "a field named with a lone surrogate": (
        [H, {**rate(1, 0, 1, 1), "\ud800": 0.5}, E],
        SHAPE.format("\\ud800"),
    ),
}


TWICE = "the whole click at round 1, site 0 books one train twice in a part"
BOOKED_TWICE = {  # a part that books a train twice: on one side unchained, or on both sides
    "a taken train listed twice": click(
        1, 0, [hold(1, (7, 4)), hold(1, (7, 4))], [hold(0, (0, 6))], q=6
    ),
    "a laid train listed twice": click(1, 0, [hold(1, (7, 4))], [hold(0, (0, 3)), hold(0, (0, 3))], q=3),
    "a train taken and laid": click(1, 0, [hold(1, (7, 4))], [hold(1, (100, 103))], q=3),
    "a chain broken on its windings": click(
        1, 0, [hold(1, (7, 4)), hold(1, (5, 1))], [hold(0, (0, 7))], q=7
    ),
    "a chain broken on its kept": click(
        1, 0, [hold(1, (7, 4), (3, 2)), hold(1, (4, 1), (3, 0))], [hold(0, (0, 10))], q=6
    ),
    "an end that books a train twice": click(
        1, 0, train=0, ends=[end_of(0, [hold(0, (5, 0)), hold(0, (5, 0))], [hold(1, (0, 10))]), ENDED[1]]
    ),
}


LACKS = "the whole click at round 1, site 0 lacks a field its books are read from"


# three windings taken, four laid: law 8 broken
OPENED = click(1, 0, [hold(1, (7, 4), (3, 3))], [hold(0, (0, 4))])
OPEN_BOOKS, CLOSED_BOOKS = (
    "the books open at 1 of 1 whole clicks read",
    "the books close at every whole click",
)
UNREAD_LINES = "the ledger's lines are read at 0 of 1 rounds with a click"
CARDLESS = {**H, "trains": [*TRAINS, without(TRAINS[1], "index")]}
GAPS = {  # a gap in the second reading: the header, the ledger, the gap's cause and the verdict beside closed books
    "the ledger absent": (H, None, "the ledger is absent", f"the ledger is absent; {CLOSED_BOOKS}"),
    "an empty ledger": (H, [], UNREAD_LINES, f"{CLOSED_BOOKS}; {UNREAD_LINES}"),
    "a ledger of round 2 alone": (
        H,
        ledger(1 + 1, {0: (0, 4), 1: (10, 6)}),
        UNREAD_LINES,
        f"{CLOSED_BOOKS}; {UNREAD_LINES}",
    ),
    "a train card without its index": (
        CARDLESS,
        GOOD,
        "the header's train card 3 holds no index",
        f"the header's train card 3 holds no index; {CLOSED_BOOKS}",
    ),
    "a ledger whose clicks lines hold a train the header lacks": (
        H,
        [*ledger(1, {0: (0, 0), 1: (10, 6)}), {"round": 1, "at": "clicks", "train": 7, "wind": 4}],
        UNREAD_LINES,
        f"{CLOSED_BOOKS}; {UNREAD_LINES}",
    ),
}


# David's A6 (6488889537, item 2): each train's windings at its winding of notches, the kept in notches; at 4, one
# winding of train 1 leaves with 3 notches kept back, and two windings of 3 notches are laid as three of 2
WEIGHED = click(1, 0, [hold(1, (5, 4), (-1, 2))], [hold(0, (0, 1), (1, -2))], q=1)
MIXED = click(1, 0, [hold(1, (1 + 1, 0))], [hold(0, (0, 3))], q=1 + 1)
UNWOUND = "the whole click at round 1, site 0 books a train the header gives no winding"


OPEN_AT_A_BOUND = {  # a whole click whose books open at one side of a bound, each train booked once
    "a taken holding that keeps its windings": click(
        1, 0, [hold(0, (4, 0)), hold(1 + 1, (4, 4))], [hold(1, (0, 4))], train=0, q=4
    ),
    "a laid holding that gains nothing": click(
        1, 0, [hold(1, (7, 4), (3, 2))], [hold(0, (0, 4)), hold(1 + 1, (5, 5))]
    ),
    "a q below the windings that left": {**TAKE, "q": 1},
    "a pair's q per end": {**PAIR, "q": 5},
}


def test_the_books_read_each_holding_once_at_its_own_winding_and_name_what_they_cannot_read(tmp_path):
    """The books' cases: each holding once at its train's winding, the gaps and bounds named, a lacking train not read."""
    for name in sorted(BOOKED_TWICE):
        twice = BOOKED_TWICE[name]
        assert not books.closes(twice, WOUND) and books.unread_books(twice, WOUND) == books.TWICE
        assert row([H, twice, E], ledger(1, {0: (0, 0), 1: (0, 0)}), tmp_path) == ("NOT READ", TWICE)
    chained = click(1, 0, [hold(1, (7, 4), (3, 2)), hold(1, (4, 1), (1 + 1, 0))], [hold(0, (0, 9))], q=6)
    laid_in_two = click(1, 0, [hold(1, (7, 4))], [hold(0, (0, 1)), hold(0, (1, 1 + 1 + 1))], q=3)
    moved = ledger(1, {0: (0, 9), 1: (10, 1)})
    assert books.closes(chained, WOUND) and books.closes(laid_in_two, WOUND)
    assert row([H, chained, E], moved, tmp_path)[0] == "SHOWN"
    assert row([H, without(TAKE, "train"), E], GOOD, tmp_path) == ("NOT READ", LACKS)
    for name in sorted(GAPS):
        header, held, gap, closed = GAPS[name]
        assert row([header, OPENED, E], held, tmp_path) == ("NOT SHOWN", f"{OPEN_BOOKS}; {gap}")
        assert row([header, TAKE, E], held, tmp_path) == ("NOT READ", closed)
    record = records.Record(H, [OPENED], E)
    wind = "the wind over every train agrees after the clicks and after the step at 1 of 1 rounds read, of 1 with a click"
    assert books.row_15(record, GOOD)["cause"] == f"{OPEN_BOOKS}; {wind}"
    first_card = books.row_15(records.Record({**H, "trains": [{}, *TRAINS]}, [TAKE], E), GOOD)
    assert first_card["cause"] == f"the header's train card 1 holds no index; {CLOSED_BOOKS}"
    fours, mixed = wound(4, 4), wound(1 + 1, 3)
    shown = [row([fours, WEIGHED, E], GOOD, tmp_path), row([mixed, MIXED, E], GOOD, tmp_path)]
    opened = [row([H, WEIGHED, E], GOOD, tmp_path), row([fours, MIXED, E], GOOD, tmp_path)]
    assert all(k == "SHOWN" for k, _ in shown) and all(k == "NOT SHOWN" for k, _ in opened)
    unwound = {**H, "trains": [TRAINS[0], without(TRAINS[1], "winding")]}
    elsewhere = click(1, 0, [hold(1, (7, 4), (3, 2))], [hold(1 + 1, (0, 4))])  # laid into train 2
    lines = [[unwound, TAKE, E], [H, elsewhere, E]]
    assert all(row(x, GOOD, tmp_path) == ("NOT READ", UNWOUND) for x in lines)
    no_train = row([{**H, "trains": []}, OPENED, E], GOOD, tmp_path)
    assert no_train == ("NOT READ", f"the header names no train; {UNWOUND}")
    for name in sorted(OPEN_AT_A_BOUND):
        both_ends = {**PAIR, "q": 5 + 5}  # a pair's q counts the windings that left at both its ends
        assert books.closes(both_ends, WOUND) and books.closes({**TAKE, "q": 1 + 1 + 1}, WOUND)
        assert not books.closes(OPEN_AT_A_BOUND[name], WOUND)
        assert row([THIRD, OPEN_AT_A_BOUND[name], E], GOOD, tmp_path)[0] == "NOT SHOWN"
        assert row([H, both_ends, E], PAIRED, tmp_path)[0] == "SHOWN"


def tool(path):
    return subprocess.run([sys.executable, "-I", str(TOOL), path], capture_output=True, text=True)


def test_the_reader_reads_unnamed_and_absent_fields_and_names_each_refusal_in_ascii(tmp_path):
    """The reader's cases: unnamed and absent fields read; each refusal, a board past the digits too, named in ASCII."""
    for name in sorted(READS):
        assert cause_of(READS[name], tmp_path) == ""
    for name in sorted(REFUSED):
        lines, cause = REFUSED[name]
        assert cause_of(lines, tmp_path) == cause
    sides = [10**4000, 10**4000, 1]
    cause = cause_of([{**B, "sides": sides}, rate(1, -1, 1, 1), E], tmp_path)
    assert cause == f"line 2 names site -1, off the board of sides {sides}"
    named = {
        "\ud800": "not read: line 2's \\ud800 has not its shape in the schema\n",
        "a\nnot read: forged": "not read: line 2's a\\nnot read: forged has not its shape in the schema\n",
    }
    runs = {
        key: tool(write([H, {**rate(1, 0, 1, 1), key: 0.5}, E], tmp_path / "r.jsonl")) for key in named
    }
    assert all(
        run.returncode == 0 and run.stderr == "" and run.stdout == named[key]
        for key, run in runs.items()
    )
    read = tool(write([H, rate(1, 0, 1, 1, ends=[1]), E], tmp_path / "read.jsonl"))
    assert read.returncode == 0 and read.stderr == "" and read.stdout.startswith("row 15: ")
