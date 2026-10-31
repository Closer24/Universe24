"""Tensor24's decoder on the three clicks (decoder/three.py), records of schema 1.4 written in memory: the structure per
place, which side lands, R2 within one record and the check against the board's passing, each with its yes and its
no, and the checks on two records, R1, R2's two-record form and the swap, each read SHOWN and NOT SHOWN."""

import json

from tensor24.decoder import records, three
from tensor24.record import schema

KEY = 7  # the edge key on every train card, and the header's dial
CARDS = [
    {"index": t, "label": f"train {t}", "kinds": [0], "part": 1, "winding": 1, "key": KEY, "square": 0}
    for t in (0, 1, 2)
]
KIND = {"index": 0, "label": "A1", "dimension": 1, "characters": [1] * 24}
HEAD = {"kind": "header", "record": "tensor24", "major": 1, "minor": schema.MINOR, "sides": [2, 1, 1]}
HEAD |= {"kinds": [KIND], "trains": CARDS, "dial": KEY}
READINGS = {
    "pasts": [1],
    "count": 2,
    "parts": 2,
}  # R2's past ladder, its count and the record's parts, named


def line(round_, site, train, *sides):
    """A click line holding its sides in their trains' order, its q their sum."""
    q = sum(side[1] for side in sides)
    return {
        "kind": "click",
        "round": round_,
        "site": site,
        "train": train,
        "q": q,
        "sides": [*map(list, sides)],
    }


def read(events, tmp_path, rounds=2, head=HEAD, guards=records.GUARDS):
    """The record of these events, in the schema's order between the header and an end of these rounds, read."""
    end = {"kind": "end", "rounds": rounds, "undone": 0, "exact": 1}
    ordered = sorted(events, key=lambda e: (e["round"], e["site"], e["train"]))
    path = tmp_path / "three.jsonl"
    path.write_text("".join(json.dumps(x) + "\n" for x in [head, *ordered, end]), encoding="utf-8")
    return records.read(str(path), guards)[0]


def landing(round_, giver=0):
    """At site 1, two clocks alone: the giver hands the other train one quantum at this round."""
    taker = 1 - giver
    return [line(round_, 1, giver, (taker, -1, 3, 6)), line(round_, 1, taker, (giver, 1, 3, 0))]


# round 1: three clocks pairwise joined at site 0, train 0 giving one quantum to each other; two clocks alone at site 1
TRIANGLE = [
    line(1, 0, 0, (1, -1, 3, 6), (2, -1, 2, 5)),
    line(1, 0, 1, (0, 1, 3, 0), (2, 0, 1, 1)),
    line(1, 0, 2, (0, 1, 4, 1), (1, 0, 5, 5)),
]
PAIR = landing(1)
# round 2 at site 0: train 1 gives to train 2 alone, the edge 0-2 its site holds left out of the lines, a path
PATH = [
    line(2, 0, 0, (1, 0, 3, 3)),
    line(2, 0, 1, (0, 0, 3, 3), (2, -1, 2, 5)),
    line(2, 0, 2, (1, 1, 4, 1)),
]


def test_the_structure_per_place_is_read_from_the_sides_each_edge_seen_from_both_ends(tmp_path):
    """Yes: three clocks pairwise joined, two alone and a path, each place named, the site its places' union, the path's
    lines leaving out two sides their site holds, and a meeting across a Mesh. No: a pair seen from one end alone, read
    without the sides' guard, is no edge; a line of schema 1.3 is not read; a record of no click line is no click."""
    found = three.structure(read([*TRIANGLE, *PAIR, *PATH], tmp_path))
    joined, alone, path = (
        (3, 3, "all pairwise joined"),
        (2, 1, "two clocks alone"),
        (3, 2, "not all joined"),
    )
    assert found["kind"] == three.READ and found["kinds"] == {joined: 1, alone: 1, path: 1}
    assert found["sites"] == {joined: 1, alone: 1} and found["omitted"] == len(["0-2", "2-0"])
    lone = [line(1, 1, 0, (1, -1, 3, 6), (2, 0, 2, 2)), PAIR[1]]
    assert three.structure(read(lone, tmp_path, guards=records.GUARDS[:-1]))["kind"] == "NOT SHOWN"
    bare = {"kind": "click", "round": 1, "site": 0, "train": 0, "q": -1, "tooth": [3, 6]}
    assert three.structure(read([bare], tmp_path))["kind"] == "NOT READ"
    assert three.structure(read([], tmp_path))["kind"] == "NO CLICK"
    # a clock with no edge in its site writes no sides beside its sides across a Mesh (writer B's line)
    across = [
        {**PAIR[0], "site": 0, "sides": [], "across": [[0, 1, -1, 3, 6]]},
        {**PAIR[1], "train": 0, "sides": [], "across": [[0, 0, 1, 3, 0]]},
    ]
    crossed = three.structure(read(across, tmp_path))
    assert crossed["across"] == 1 and crossed["kinds"] == {(1, 0, "no edge in its site"): len(across)}


def test_the_passings_and_the_split_s_weights_are_a_check_read_where_every_side_and_the_dial_stand(
    tmp_path,
):
    """Yes: x = D q + k_after - k_before on every side, D the header's dial, and the giver's weights (u, x_tu, X_t) where
    it meets two clocks, none where a clock meets one. No: a header with no dial, and lines leaving out a side their
    site holds, are not read."""
    found = three.passing(read([*TRIANGLE, *PAIR], tmp_path))
    given = [(u, KEY * q + after - before) for u, q, before, after in TRIANGLE[0]["sides"]]
    split = {(1, 0, 0): [(u, x, sum(x for _, x in given)) for u, x in given]}  # both its sides give
    assert found["kind"] == three.READ and found["weights"] == split
    undialled = {k: v for k, v in HEAD.items() if k != "dial"}
    assert three.passing(read(TRIANGLE, tmp_path, head=undialled))["kind"] == "NOT READ"
    assert three.passing(read([*TRIANGLE, *PATH], tmp_path))["kind"] == "NOT READ"


def test_which_side_lands_is_read_where_the_giver_meets_two_clocks_or_more(tmp_path):
    """Yes: the giver at three clocks pairwise joined lands a quantum on each taker it names, the pair's passing the
    first click's beside them. No: a record of two clocks alone lands nothing."""
    found = three.lands(read([*TRIANGLE, *PAIR], tmp_path))
    takers = {(0, u): 1 for u, *_ in TRIANGLE[0]["sides"]}
    assert found["landed"] == takers and found["first"] == 1
    assert three.lands(read(PAIR, tmp_path))["landed"] == {}


def test_r2_within_one_record_reads_a_single_one_way_side_whose_pasts_do_not_fix_its_next_q(tmp_path):
    """Yes: a side landing as drawn, its pasts followed by two different q's twice in each part. No: a carried beat,
    one such past a part; the readings unnamed; sides landing two quanta at once, sides passing both ways, and a side
    landing in one part alone, not read."""
    drawn, carried = (1, 2, 5, 6, 7, 10), (1, 3, 4, 6, 8, 9)  # ten rounds, two parts of five
    heavy = [(line(r, 1, 0, (1, -2, 3, 6)), line(r, 1, 1, (0, 2, 3, 0))) for r in drawn]
    both = [landing(r, giver=int(r > drawn[2])) for r in drawn]
    cases = [([landing(r) for r in drawn], READINGS), ([landing(r) for r in carried], READINGS)]
    cases += [([landing(r) for r in drawn], None), (heavy, READINGS), (both, READINGS)]
    cases += [([landing(r) for r in drawn if r <= drawn[2]], READINGS)]
    records_ = [
        (read([x for pair in pairs for x in pair], tmp_path, drawn[-1]), held) for pairs, held in cases
    ]
    kinds = [three.within(record, held)["kind"] for record, held in records_]
    assert kinds == ["SHOWN", "NOT SHOWN", "NOT READ", "NOT READ", "NOT READ", "NOT READ"]


def relabel(events, swap):
    """The events of a lay with the swap's trains exchanged in the files, each line and side named so."""
    named = [{**e, "train": swap.get(e["train"], e["train"])} for e in events]
    return [{**e, "sides": sorted([swap.get(u, u), *rest] for u, *rest in e["sides"])} for e in named]


def test_the_checks_on_two_records_compare_their_q_s_alone_line_for_line(tmp_path):
    """Yes: the lay and its swap, its trains named back, alike line for line; the lay against one of other teeth alike
    on the q's alone (R1); a record cut short apart from its round (R2's). No: the lay against itself through the swap;
    the record cut short (R1); the lay against itself (R2's); no trains named for the swap, not read."""
    lay, short = read([*TRIANGLE, *PAIR, *PATH], tmp_path), read([*TRIANGLE, *PAIR], tmp_path)
    toothed = [line(1, 1, 0, (1, -1, 2, 5)), line(1, 1, 1, (0, 1, 4, 1))]  # PAIR's q, other teeth
    retoothed = read([*TRIANGLE, *toothed, *PATH], tmp_path)
    exchanged, trains = read(relabel([*TRIANGLE, *PAIR, *PATH], {1: 2, 2: 1}), tmp_path), [1, 2]
    assert three.swapped(lay, exchanged, trains)["kind"] == "SHOWN"
    assert three.swapped(lay, lay, trains)["kind"] == "NOT SHOWN"
    assert three.swapped(lay, exchanged, [])["kind"] == "NOT READ"
    assert (
        three.twice(lay, retoothed)["kind"] == "SHOWN" and three.twice(lay, short)["kind"] == "NOT SHOWN"
    )
    assert three.apart(lay, short)["kind"] == "SHOWN" and three.apart(lay, lay)["kind"] == "NOT SHOWN"
    assert three.apart(lay, short)["apart"] == [PATH[0]["round"]]
