"""Tensor24's decoder on schema 1.4's sides, records written in memory: each edge between two clocks read at its place,
its two sides' q summing to 0 and their teeth to the key less 1, before and after; each click line that breaks a rule
of the edges refused by name, and read without the guard."""

import json

from tensor24.decoder import records
from tensor24.record import schema

KEY = 7  # the edge key on every train card
CARDS = [
    {"index": t, "label": f"train {t}", "kinds": [0], "part": 1, "winding": 1, "key": KEY, "square": 0}
    for t in (0, 1, 2)
]
KIND = {"index": 0, "label": "A1", "dimension": 1, "characters": [1] * 24}
HEADER = {"kind": "header", "record": "tensor24", "major": 1, "minor": schema.MINOR, "sides": [1, 1, 1]}
HEAD, END = (
    HEADER | {"kinds": [KIND], "trains": CARDS},
    {"kind": "end", "rounds": 1, "undone": 0, "exact": 1},
)


def line(train, *sides):
    """A click line at round 1 and site 0 holding its sides, its q their sum."""
    q = sum(side[1] for side in sides)
    return {"kind": "click", "round": 1, "site": 0, "train": train, "q": q, "sides": [*map(list, sides)]}


def read(events, tmp_path, guards=records.GUARDS):
    """The record of these events between the header and the end, read under the guards: the record and its cause."""
    path = tmp_path / "sides.jsonl"
    path.write_text("".join(json.dumps(x) + "\n" for x in [HEAD, *events, END]), encoding="utf-8")
    return records.read(str(path), guards)


# a place where three clocks meet: the edges 0-1 and 0-2 carried, each pair of teeth summing to the key less 1
GIVE = line(0, (1, -1, 3, 6), (2, -1, 2, 5))
TAKE = [line(1, (0, 1, 3, 0)), line(2, (0, 1, 4, 1))]
OFF = "line 2's sides have not the form [u, q, tooth before, tooth after]"
REFUSED = [
    ([{**GIVE, "tooth": [3, 6]}, *TAKE], "line 2 holds a tooth beside its sides, or no sides"),
    ([{**GIVE, "sides": []}, *TAKE], "line 2 holds a tooth beside its sides, or no sides"),
    ([{**GIVE, "sides": [[1, -1, 3]]}, *TAKE], OFF),
    ([line(0, (0, -1, 3, 6))], "line 2's side names its own train 0"),
    ([line(0, (5, -1, 3, 6))], "line 2's side names train 5, which no train card names"),
    (
        [line(0, (2, -1, 2, 5), (1, -1, 3, 6)), *TAKE],
        "line 2's sides stand out of their trains' order or name one twice",
    ),
    (
        [line(0, (1, -1, 3, 6), (1, -1, 3, 6)), *TAKE],
        "line 2's sides stand out of their trains' order or name one twice",
    ),
    ([{**GIVE, "q": -1}, *TAKE], "line 2's sides sum to -2, not its q -1"),
    ([line(0, (1, -1, 3, KEY), (2, -1, 2, 5)), *TAKE], "line 2 holds a side's tooth outside [0, 7)"),
    ([GIVE, TAKE[0]], "line 2's side to train 2 has no partner at its place"),
    (
        [GIVE, line(1, (0, 2, 3, 0)), TAKE[1]],
        "line 2's side to train 1 and its partner hold q -1 and 2, not 0 summed",
    ),
    (
        [GIVE, line(1, (0, 1, 3, 1)), TAKE[1]],
        "line 2's side to train 1 and its partner hold teeth not summing to the key less 1, 6",
    ),
    (
        [GIVE, line(1, (0, 1, 2, 0)), TAKE[1]],
        "line 2's side to train 1 and its partner hold teeth not summing to the key less 1, 6",
    ),
]


def test_each_edge_closes_at_its_place_and_each_line_breaking_a_rule_of_the_sides_is_refused_by_name(
    tmp_path,
):
    """Yes: a place where three clocks meet, its giver's line and its two takers' with their teeth, reads in order, and
    so does one with a side at q 0 beside its partner. No: each record of REFUSED by its own cause, and none without
    the guard."""
    record, cause = read([GIVE, *TAKE], tmp_path)
    assert cause == "" and record is not None and record.of("click") == [GIVE, *TAKE]
    # the edge 0-2 listed at q 0, not carried, beside the edges 0-1 and 2-1 that carried
    still = [
        line(0, (1, -1, 3, 6), (2, 0, 2, 2)),
        line(1, (0, 1, 3, 0), (2, 1, 1, 4)),
        line(2, (0, 0, 4, 4), (1, -1, 5, 2)),
    ]
    assert read(still, tmp_path)[1] == ""
    for events, wanted in REFUSED:
        assert read(events, tmp_path)[1] == wanted
        assert read(events, tmp_path, records.GUARDS[:-1])[1] == ""
