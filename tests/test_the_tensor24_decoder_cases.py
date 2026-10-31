"""Tensor24's decoder, its second file: the twelfth hostile review's cases, each read as the plan, the schema and the
decoder's own comments say, nothing raised, and each failing on the reader's mutant it was written for."""

import json
import subprocess
import sys
from pathlib import Path

from tensor24.decoder import records

TOOL = Path(__file__).resolve().parent.parent / "tools" / "tensor24_decode.py"
TRAINS = [{"index": t, "label": f"train {t}", "kinds": [0], "part": 1, "winding": 1} for t in (0, 1)]
H = {"kind": "header", "record": "tensor24", "major": 1, "minor": 1, "trains": TRAINS}
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


def write(lines, path):
    path.write_text("".join((x if isinstance(x, str) else json.dumps(x)) + "\n" for x in lines))
    return str(path)


def cause_of(lines, tmp_path):
    """The cause a record of the given lines is not read, or "" where it is read."""
    return records.read(write(lines, tmp_path / "record.jsonl"))[1]


# three windings and one kept of train 1 laid as four of train 0; a pair of train 0 taken at both ends into train 1
TAKE = click(1, 0, [hold(1, (7, 4), (3, 2))], [hold(0, (0, 4))])
ENDED = [
    end_of(0, [hold(0, (5, 0), (0, 1))], [hold(1, (0, 4))]),
    end_of(1, [hold(0, (5, 0))], [hold(1, (0, 5))]),
]
PAIR = click(1, 0, train=0, ends=ENDED)
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
    assert read.returncode == 0 and read.stderr == "" and read.stdout.startswith("the ledger: ")
