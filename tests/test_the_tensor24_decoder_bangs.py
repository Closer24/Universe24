"""Tensor24's decoder, row 46: each later bang shows more, read from the clicks each bang lays and from the ledger's
windings held at its end, the bangs read from the load; nothing raised, and each reading failing on its own mutant."""

import json
import subprocess
import sys
from pathlib import Path

from tensor24.decoder import bangs, records

TOOL = Path(__file__).resolve().parent.parent / "tools" / "tensor24_decode.py"

# trains: 0 the time gear, 1 light, 2 matter, 3 a pair of matter (depth 1), 4 a pair bound with light (depth 2)
PARTS = {0: [], 1: [], 2: [], 3: [2, 2], 4: [3, 1]}
CARDS = [
    {"index": t, "label": f"train {t}", "kinds": [0], "part": 1, "winding": 1, "parts": p}
    for t, p in PARTS.items()
]
H = {"kind": "header", "record": "tensor24", "major": 1, "minor": 1, "trains": CARDS, "time_gear": 0}
E = {"kind": "end", "rounds": 14, "undone": 0, "exact": 1}
LOAD = [0, 3, 5, 3, 0, 3, 5, 3, 0, 3, 5, 3, 0, 3]  # three bangs whole: rounds 1 to 4, 5 to 8 and 9 to 12


def lay(train):
    return {"train": train, "windings": [0, 1], "kept": [0, 0]}


def click(round_, train, laid=(), site=0, **more):
    """A whole click at round and site, its own train's, laying the trains named at the click."""
    line = {"kind": "whole", "round": round_, "site": site, "count": round_, "train": train}
    return line | {"taken": [], "laid": [lay(t) for t in laid], "ends": []} | more


def ends(train):
    return [
        {"site": s, "spoke": 0, "taken": [], "laid": [lay(train)], "push": [0, 0, 0]} for s in (0, 1)
    ]


CHILD = {"train": 3, "site": 0, "sweep": 0, "push": [0, 0, 0], "moment": [0, 0, 0]}
SPLIT = {"kind": "split", "round": 11, "site": 1, "count": 11, "train": 3}
CLICKS = [  # bang 1 lays matter; bang 2 a pair, as a child; bang 3 the pair bound with light, at both ends of a Mesh
    click(2, 1, [2]),
    click(6, 1, [2]),
    click(7, 2, children=[CHILD]),
    click(10, 1, [2]),
    click(10, 2, [3], site=1),
    click(11, 3, ends=ends(4)),
    SPLIT,
]
HELD = {
    4: [(2, 1), (4, 0)],
    8: [(3, 1)],
    12: [(4, 1)],
}  # at each bang's end, after the clicks: train, windings
PAIR_HELD = {**HELD, 12: [(3, 1)]}  # bang 3 ends holding the pair alone, a clock of depth 1


def ledger(load=LOAD, held=HELD):
    steps = [{"round": r, "at": "step", "train": 0, "windings": w} for r, w in enumerate(load, start=1)]
    after = [
        {"round": r, "at": "clicks", "train": t, "windings": w}
        for r, pairs in held.items()
        for t, w in pairs
    ]
    return (
        steps + after + [{"round": 3, "at": "clicks", "train": 0, "windings": 0}]
    )  # the time gear after clicks


def row(tmp_path, lines=CLICKS, held=HELD, header=H, lines_of_ledger=None, absent=False):
    """Row 46 on a record of the header and the lines given, and on its ledger, or on none where it is absent."""
    path = tmp_path / "record.jsonl"
    path.write_text("".join(json.dumps(x) + "\n" for x in [header, *lines, E]))
    record, cause = records.read(str(path))
    assert record is not None, cause
    found = ledger(held=held) if lines_of_ledger is None else lines_of_ledger
    return bangs.row_46(record, None if absent else found)


SHOWN = {
    "kind": "SHOWN",
    "cause": "each of the 3 bangs whole shows more than the last: the click kinds [1, 2, 4], the deepest clock laid "
    "[0, 1, 2] and held [0, 1, 2]",
    "bangs": [(1, 4), (5, 8), (9, 12)],
    "kinds": [1, 2, 4],
    "laid": [0, 1, 2],
    "held": [0, 1, 2],
}


def test_the_tool_prints_row_46_from_the_record_and_its_ledger(tmp_path):
    record, held = tmp_path / "record.jsonl", tmp_path / "ledger.jsonl"
    record.write_text("".join(json.dumps(x) + "\n" for x in [H, *CLICKS, E]))
    held.write_text("".join(json.dumps(x) + "\n" for x in ledger()))
    run = subprocess.run(
        [sys.executable, "-I", str(TOOL), str(record), str(held)], capture_output=True, text=True
    )
    assert run.returncode == 0 and run.stderr == "" and f"row 46: {SHOWN}" in run.stdout.splitlines()


NO_MORE = (
    "bang 3 shows no more than bang 2: {} click kinds against 2, its deepest clock laid {} against 1"
)
SHOWS_LESS = {  # bang 3's clicks, and the cause: the same as bang 2's, fewer kinds, a shallower clock
    "the same kinds and depth": (
        [*CLICKS[:3], click(10, 1, [2]), click(11, 2, [3])],
        NO_MORE.format(2, 1),
    ),
    "fewer kinds": ([*CLICKS[:3], click(11, 3, ends=ends(4))], NO_MORE.format(1, 2)),
    "a shallower clock": (
        [*CLICKS[:3], click(10, 1, [2]), click(10, 2, [2], site=1), SPLIT],
        NO_MORE.format(3, 0),
    ),
}


def parted(train, parts):
    """The header with one train's card holding the parts given, or none where parts is None."""
    cards = [{k: v for k, v in c.items() if k != "parts" or c["index"] != train} for c in CARDS]
    return {
        **H,
        "trains": [c | ({"parts": parts} if c["index"] == train and parts else {}) for c in cards],
    }


DEPTHLESS = "the train {} is a clock of no depth: its card or a part's names no parts"
UNREAD = {  # a record or a ledger the row cannot frame or read, and its cause
    "the ledger absent": ({"absent": True}, "the ledger is absent"),
    "no time gear": ({"header": {**H, "time_gear": "t"}}, "the header names no time gear"),
    "a round with no load": (
        {"lines_of_ledger": [x for x in ledger() if x["round"] != 7]},
        "the ledger holds no load at round 7",
    ),
    "one bang whole": (
        {"lines_of_ledger": ledger(LOAD[:9], {4: [(2, 1)]})},
        "the bangs whole number 1, where the row compares two or more",
    ),
    "a card without its parts": ({"header": parted(3, None)}, DEPTHLESS.format(3)),
    "parts that bind themselves": ({"header": parted(3, [3])}, DEPTHLESS.format(3)),
    "a part no card names": ({"header": parted(4, [3, 9])}, DEPTHLESS.format(4)),
    "a part that is a row": ({"header": parted(3, [[2], 2])}, DEPTHLESS.format(3)),
}


EDGES = {  # a load, and its bottoms' places
    "a bottom held two rounds": ([3, 0, 0, 3], [2]),
    "a top held two rounds": ([0, 3, 3, 0], []),
    "the last round falling": ([0, 3, 0, 3, 0], [2]),
    "the first round lowest": ([0, 3, 5], []),
}


def test_each_later_bang_shows_more_or_reads_not_shown_or_not_read_named(tmp_path):
    """Row 46's one law: each later bang shows more clocks by its kinds or its depth, else not shown, or not read, named."""
    assert row(tmp_path) == SHOWN
    kinds_alone = [*CLICKS[:5], click(11, 1, [3], site=0), SPLIT]  # bang 3: 3 kinds, its deepest laid 1
    deeper_alone = [
        *CLICKS[:3],
        click(10, 1, [2]),
        click(11, 3, ends=ends(4)),
    ]  # bang 3: 2 kinds, laid 2
    held = PAIR_HELD
    assert (
        row(tmp_path, kinds_alone, held)["kind"] == row(tmp_path, deeper_alone, held)["kind"] == "SHOWN"
    )
    for name in sorted(SHOWS_LESS):
        lines, cause = SHOWS_LESS[name]
        assert row(tmp_path, lines, PAIR_HELD)["cause"] == cause
    verdict = row(tmp_path, held={**HELD, 12: [(2, 1)]})
    assert verdict["kind"] == "NOT SHOWN"
    assert verdict["cause"] == "the deepest clock held falls from 1 to 0 at bang 3's end"
    for name in sorted(UNREAD):
        frame, cause = UNREAD[name]
        assert row(tmp_path, **frame) == {"kind": "NOT READ", "cause": cause}
    for name in sorted(EDGES):
        load, places = EDGES[name]
        assert bangs.bottoms(load) == places
