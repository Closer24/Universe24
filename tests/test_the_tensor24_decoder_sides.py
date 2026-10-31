"""Tensor24's decoder on schema 1.4's sides, records written in memory: each edge between two clocks read at its place,
its two sides' q summing to 0 and their teeth to the key less 1, before and after; each click line that breaks a rule
of the edges refused by name, and read without the guard."""

import json

from tensor24.decoder import records, shadow
from tensor24.record import schema

KEY = 7  # the edge key on every train card but train 3's, which holds none
CARDS = [
    {"index": t, "label": f"train {t}", "kinds": [0], "part": 1, "winding": 1, "key": KEY, "square": 0}
    for t in (0, 1, 2)
]
CARDS += [{k: v for k, v in CARDS[0].items() if k != "key"} | {"index": 3, "label": "train 3"}]
KIND = {"index": 0, "label": "A1", "dimension": 1, "characters": [1] * 24}
HEADER = {"kind": "header", "record": "tensor24", "major": 1, "minor": schema.MINOR, "sides": [2, 1, 1]}
# a board of two Node-clocks and two rounds, so a partner at another Node-clock or round is no partner
HEAD, END = (
    HEADER | {"kinds": [KIND], "trains": CARDS},
    {"kind": "end", "rounds": 2, "undone": 0, "exact": 1},
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
# sides off their form: refused by the schema's own shape where it types the sides (writer B's 1.4 line), else here
SHAPE, OFF = (
    "line 2's sides has not its shape in the schema",
    "line 2's sides have not the form [u, q, tooth before, tooth after]",
)
BARE = "line 2 holds a tooth beside its sides, or no sides"
# a side across the Mesh: train 1 at site 0 gives one quantum to train 1 at site 1, beside the place's own edges, the
# far line holding no sides in its site, as writer B writes it
NEAR = {**TAKE[0], "q": 0, "across": [[1, 1, -1, 2, 5]]}
FAR = {**line(1), "site": 1, "q": 1, "across": [[1, 0, 1, 4, 1]]}
CROSSED = [GIVE, NEAR, TAKE[1], FAR]
ACROSS = "line 3's sides across a Mesh have not the form [u, place, q, tooth before, tooth after]"
FORMLESS = [
    ([{**GIVE, "sides": [[1, -1, 3]]}, *TAKE], (OFF, SHAPE)),
    ([line(0, (1, -1, 3, 6, 0), (2, -1, 2, 5)), *TAKE], (OFF, SHAPE)),
    ([line(0, (1, -1, "3", 6), (2, -1, 2, 5)), *TAKE], (OFF, SHAPE)),
    ([{**GIVE, "sides": 5}, *TAKE], (BARE, SHAPE)),
    (
        [GIVE, {**NEAR, "across": [[1, 1, -1, 2]]}, TAKE[1], FAR],
        (ACROSS, "line 3's across has not its shape in the schema"),
    ),
]
KEYLESS, APART = (
    "line 2 names no train whose card holds a whole key",
    "line 2's side to train 1 has no partner at its place",
)
UNORDERED, ACROSS_ORDER = (
    "line 2's sides stand out of their trains' order or name one twice",
    "line 3's sides across a Mesh stand out of their places' order or name one twice",
)
HOLD, HELD = (
    "line 2's side to train 1 and its partner hold",
    "line 3's side to train 1 and its partner hold",
)
REFUSED = [
    ([{**GIVE, "tooth": [3, 6]}, *TAKE], BARE),
    ([{**GIVE, "sides": []}, *TAKE], BARE),
    ([{k: v for k, v in GIVE.items() if k != "train"}, *TAKE], KEYLESS),
    ([line(3, (0, -1, 3, 6))], KEYLESS),
    ([line(0, (0, -1, 3, 6))], "line 2's side names its own train 0"),
    ([line(0, (5, -1, 3, 6))], "line 2's side names train 5, which no train card names"),
    ([line(0, (2, -1, 2, 5), (1, -1, 3, 6)), *TAKE], UNORDERED),
    ([line(0, (1, -1, 3, 6), (1, -1, 3, 6)), *TAKE], UNORDERED),
    ([{**GIVE, "q": -1}, *TAKE], "line 2's sides sum to -2, not its q -1"),
    ([line(0, (1, -1, 3, KEY), (2, -1, 2, 5)), *TAKE], "line 2 holds a side's tooth outside [0, 7)"),
    ([line(0, (1, -1, -1, 6), (2, -1, 2, 5)), *TAKE], "line 2 holds a side's tooth outside [0, 7)"),
    ([GIVE, TAKE[0]], "line 2's side to train 2 has no partner at its place"),
    ([GIVE, TAKE[1], {**TAKE[0], "site": 1}], APART),
    ([GIVE, TAKE[1], {**TAKE[0], "round": 2}], APART),
    ([GIVE, NEAR, TAKE[1]], "line 3's side to train 1 has no partner at its place"),
    ([GIVE, {**NEAR, "q": 1}, TAKE[1], FAR], "line 3's sides sum to 0, not its q 1"),
    ([GIVE, {**NEAR, "across": [[1, 1, -1, 2, 5]] * 2}, TAKE[1], FAR], ACROSS_ORDER),
    (
        [GIVE, {**NEAR, "across": [[5, 1, -1, 2, 5]]}, TAKE[1], FAR],
        "line 3's side names train 5, which no train card names",
    ),
    (
        [GIVE, {**NEAR, "across": [[1, 1, -1, 2, KEY]]}, TAKE[1], FAR],
        "line 3 holds a side's tooth outside [0, 7)",
    ),
    ([*CROSSED[:-1], {**FAR, "q": 2, "across": [[1, 0, 2, 4, 1]]}], f"{HELD} q -1 and 2, not 0 summed"),
    (
        [*CROSSED[:-1], {**FAR, "across": [[1, 0, 1, 3, 1]]}],
        f"{HELD} teeth not summing to the key less 1, 6",
    ),
    ([GIVE, line(1, (0, 2, 3, 0)), TAKE[1]], f"{HOLD} q -1 and 2, not 0 summed"),
    ([GIVE, line(1, (0, 1, 3, 1)), TAKE[1]], f"{HOLD} teeth not summing to the key less 1, 6"),
    ([GIVE, line(1, (0, 1, 2, 0)), TAKE[1]], f"{HOLD} teeth not summing to the key less 1, 6"),
]


def test_each_edge_closes_at_its_place_and_each_line_breaking_a_rule_of_the_sides_is_refused_by_name(
    tmp_path,
):
    """Yes: a place where three clocks meet, its giver's line and its two takers' with their teeth, reads in order, and
    so do one with a side at q 0 beside its partner and one with a side across a Mesh. No: each of FORMLESS by the
    guard that owns the side's form, and each of REFUSED by its own cause, none refused without the sides' guard."""
    record, cause = read([GIVE, *TAKE], tmp_path)
    assert cause == "" and record is not None and record.of("click") == [GIVE, *TAKE]
    # the edge 0-2 listed at q 0, not carried, beside the edges 0-1 and 2-1 that carried
    still = [
        line(0, (1, -1, 3, 6), (2, 0, 2, 2)),
        line(1, (0, 1, 3, 0), (2, 1, 1, 4)),
        line(2, (0, 0, 4, 4), (1, -1, 5, 2)),
    ]
    assert read(still, tmp_path)[1] == "" and read(CROSSED, tmp_path)[1] == ""
    for events, wanted in FORMLESS:
        assert read(events, tmp_path)[1] in wanted
    for events, wanted in REFUSED:
        assert read(events, tmp_path)[1] == wanted
        assert read(events, tmp_path, records.GUARDS[:-1])[1] == ""


def test_the_books_close_each_edge_across_a_mesh_at_both_its_places(tmp_path):
    """Yes: the place whose side across a Mesh carried, its far line beside it, closes its books, each side across
    booked at both its places. No, read without the sides' guard: the far line's partner side dropped opens them, and
    so does a side across cut short, booking nothing and raising nothing."""
    unguarded = [*CROSSED[:-1], {**FAR, "across": []}], FORMLESS[-1][0]
    found = [
        shadow.books(read(events, tmp_path, records.GUARDS[:-1])[0]) for events in (CROSSED, *unguarded)
    ]
    assert [verdict["kind"] for verdict in found] == ["SHOWN", "NOT SHOWN", "NOT SHOWN"]
