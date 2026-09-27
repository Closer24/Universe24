"""The click readers of examples/events/massive_record/read_runs.py on tracked and hand-made click and gather lines: counts per Node, centroid, maxima and visibility as exact fractions, the first click and the mean interval; clicks only, no line of the GameBoard read."""

from __future__ import annotations

import json
from collections import Counter
from fractions import Fraction
from pathlib import Path

from tests.worlds import load_file

ROOT = Path(__file__).resolve().parents[1]
RECORD = ROOT / "examples" / "events" / "massive_record"


READER = load_file("massive_record_read_runs_readers", RECORD / "read_runs.py")


def tracked(world: str) -> list[dict]:
    path = RECORD / f"EXPLORATORY_layer_{world}_14" / "events.jsonl"
    with path.open(encoding="utf-8") as stream:
        return [json.loads(line) for line in stream]


def test_the_tracked_rest_run_reads_its_train_by_the_same_reader_as_the_block_clock():
    """The rest layer's 88 clicks at the block's corner: over [200, 3500] 83 clicks with
    the mean interval 3219 / 82 = 39.26 (BUILD_READINGS.md, the layer pin world at rest);
    the first click 28 intervals after the birth stamp 0; the readers agree with the
    block-clock reader `clock` uses."""
    lines = tracked("rest")
    clicks = READER.clicks_of(lines)
    assert len(clicks) == 88
    assert all(click.node == (57, 57, 0) and click.cell is None for click in clicks)
    assert [click.tick for click in clicks] == sorted(click.tick for click in clicks)
    whole = READER.light_clicks(clicks, birth=0)
    assert whole["kind"] == "DETECTOR"
    assert whole["count"] == 88
    assert whole["first_tick"] == 28 and whole["first_interval"] == 28
    assert len(whole["intervals"]) == 87 and sum(whole["intervals"]) == whole["last_tick"] - 28
    hold = READER.light_clicks(clicks, birth=0, window=(200, 3500))
    assert hold["count"] == 83
    assert hold["first_tick"] == 240 and hold["first_interval"] == 240
    assert hold["mean_interval"] == Fraction(3219, 82)
    assert abs(float(hold["mean_interval"]) - 39.26) < 0.005
    ticks = [line["tick"] for line in lines if line["event"] == "click" and 200 <= line["tick"] <= 3500]
    assert READER.click_mean_interval(ticks) == hold["mean_interval"]
    assert abs(hold["line_omega"] - 2.0 * 3.141592653589793 / float(hold["mean_interval"])) < 1e-12
    # the train's line by the block clock's reader is the same fraction, converted once
    assert float(hold["mean_interval"]) == (ticks[-1] - ticks[0]) / (len(ticks) - 1)


def test_the_tracked_moving_run_counts_its_clicks_per_node_along_x():
    """The pushed layer's 261 clicks step along x with the block (the corner's Node on
    each click line): the counts per Node equal a plain tally, the row's axis is x, the
    centroid is the exact count-weighted mean of x, every maximum is a strict local
    maximum of the counts along x, and the visibility is (5 - 1) / (5 + 1)."""
    lines = tracked("k3")
    clicks = READER.clicks_of(lines)
    assert len(clicks) == 261
    tally = Counter(tuple(line["node"]) for line in lines if line["event"] == "click")
    screen = READER.screen_clicks(clicks)
    assert screen["kind"] == "DETECTOR" and screen["axis"] == "x"
    assert screen["counts"] == {node: tally[node] for node in sorted(tally, key=lambda n: n[0])}
    assert screen["total"] == 261 and screen["unplaced"] == 0
    assert screen["centroid"] == Fraction(sum(n[0] * c for n, c in tally.items()), 261)
    assert screen["centroid"] == Fraction(17131, 261)
    assert screen["max"] == 5 and screen["min"] == 1
    assert screen["visibility"] == Fraction(2, 3)
    ordered = sorted(tally, key=lambda n: n[0])
    values = [tally[node] for node in ordered]
    for position in screen["maxima"]:
        assert position.denominator in (1, 2)
        index = [node[0] for node in ordered].index(int(position))
        assert values[index] > 0
        assert index == 0 or values[index - 1] <= values[index]
    # the hold [1500, 9500]: 224 clicks, the mean interval 35.73 (BUILD_READINGS.md)
    hold = READER.light_clicks(clicks, window=(1500, 9500))
    assert hold["count"] == 224
    assert abs(float(hold["mean_interval"]) - 35.73) < 0.005
    assert hold["birth"] is None and hold["first_interval"] is None


def test_a_hand_made_screen_row_reads_its_centroid_maxima_and_visibility_exactly():
    """A detector row of five Nodes along y with the counts [1, 3, 1, 0, 2]: the centroid
    (0 + 3 + 2 + 0 + 8) / 7 = 13 / 7, the maxima at y = 1 and y = 4, the visibility
    (3 - 0) / (3 + 0) = 1 with the Node without a click counted as 0; a plateau of two
    equal maxima at y = 1 and y = 2 is one maximum at 3 / 2; a click without a Node is
    counted as unplaced and enters nothing else."""
    row = [(8, y, 0) for y in range(5)]

    def clicks_at(counts: list[int]) -> list:
        found = []
        tick = 0
        for y, count in enumerate(counts):
            for _ in range(count):
                tick += 1
                found.append(READER.Click(tick=tick, node=(8, y, 0), cell="screen"))
        return found

    screen = READER.screen_clicks(clicks_at([1, 3, 1, 0, 2]), row=row)
    assert screen["axis"] == "y"
    assert screen["counts"] == {(8, 0, 0): 1, (8, 1, 0): 3, (8, 2, 0): 1, (8, 3, 0): 0, (8, 4, 0): 2}
    assert screen["total"] == 7
    assert screen["centroid"] == Fraction(13, 7)
    assert screen["maxima"] == [Fraction(1), Fraction(4)]
    assert screen["visibility"] == Fraction(1)
    plateau = READER.screen_clicks(clicks_at([1, 3, 3, 1, 0]), row=row)
    assert plateau["maxima"] == [Fraction(3, 2)]
    assert plateau["centroid"] == Fraction(0 + 3 + 6 + 3, 8)
    flat = READER.screen_clicks(clicks_at([2, 2, 2, 2, 2]), row=row)
    assert flat["maxima"] == [] and flat["visibility"] == Fraction(0)
    mixed = clicks_at([1, 0, 0, 0, 0]) + [READER.Click(tick=9, node=None, cell="wide")]
    reading = READER.screen_clicks(mixed, row=row)
    assert reading["total"] == 1 and reading["unplaced"] == 1
    assert reading["centroid"] == Fraction(0)
    # the declared fringe window [0, 2] along y leaves the edge Node without a click out
    # of the visibility, (3 - 1) / (3 + 1) = 1 / 2; the centroid and the maxima unchanged
    fringed = READER.screen_clicks(clicks_at([1, 3, 1, 0, 2]), row=row, fringe=(0, 2))
    assert fringed["fringe"] == [0, 2]
    assert fringed["max"] == 3 and fringed["min"] == 1 and fringed["visibility"] == Fraction(1, 2)
    assert fringed["centroid"] == Fraction(13, 7) and fringed["maxima"] == [Fraction(1), Fraction(4)]
    assert screen["fringe"] is None
    edge = READER.screen_clicks(clicks_at([0, 4, 4, 4, 0]), row=row)
    assert edge["visibility"] == Fraction(1)
    edge_fringed = READER.screen_clicks(clicks_at([0, 4, 4, 4, 0]), row=row, fringe=(1, 3))
    assert edge_fringed["visibility"] == Fraction(0)
    outside = READER.screen_clicks(clicks_at([1, 3, 1, 0, 2]), row=row, fringe=(7, 9))
    assert outside["max"] == 0 and outside["visibility"] is None
    windowed = READER.screen_clicks(clicks_at([1, 3, 1, 0, 2]), row=row, window=(1, 4))
    assert windowed["counts"] == {(8, 0, 0): 1, (8, 1, 0): 3, (8, 2, 0): 0, (8, 3, 0): 0, (8, 4, 0): 0}


def test_gather_lines_are_clicks_at_the_chosen_cells_one_node_and_escapes_are_not():
    """Under the detector law a light record's click is its `gather` line: the click at
    the `click` interval (the first rung), the cell the chosen set, the Node the set's
    one declared Node (a set of two Nodes gives no Node), the birth stamp carried; a
    gather with no chosen cell is an escape, not a click; a `measured:<n>` cell is the
    measured event's Node."""
    world = {
        "measured": [
            {"position": [2, 0, 0], "family": "light", "lamp": {}},
            {"position": [70, 0, 0], "family": "light"},
        ],
        "detectors": [
            {"name": "screen", "positions": [[70, 0, 0]]},
            {"name": "wide", "positions": [[60, 0, 0], [61, 0, 0]]},
        ],
    }
    cells = READER.detector_nodes(world)
    assert cells == {
        "measured:0": [(2, 0, 0)],
        "measured:1": [(70, 0, 0)],
        "screen": [(70, 0, 0)],
        "wide": [(60, 0, 0), (61, 0, 0)],
    }
    lines = [
        {"event": "gather", "tick": 200, "click": 130, "birth": 12, "chosen": [["screen", 0, "0"]]},
        {"event": "gather", "tick": 210, "click": 150, "birth": 30, "chosen": None},
        {"event": "gather", "tick": 220, "click": 141, "birth": 20, "chosen": [["wide", 0, "0"]]},
        {"event": "block", "tick": 221, "sum": 5},
        {
            "event": "gather",
            "tick": 230,
            "click": 152,
            "birth": 33,
            "chosen": [["measured:1", 0, "0"]],
            "clock": 152,
        },
        {"event": "click", "tick": 160, "node": [0, 0, 0], "detector": "face:-x", "clock": 7},
    ]
    clicks = READER.clicks_of(lines, cells)
    assert [(c.tick, c.node, c.cell, c.birth, c.clock) for c in clicks] == [
        (130, (70, 0, 0), "screen", 12, None),
        (141, None, "wide", 20, None),
        (152, (70, 0, 0), "measured:1", 33, 152),
        (160, (0, 0, 0), "face:-x", None, 7),
    ]
    train = READER.light_clicks([c for c in clicks if c.cell == "screen"])
    assert train["count"] == 1 and train["birth"] == 12 and train["first_interval"] == 118
    assert train["birth_intervals"] == [118]
    assert train["mean_interval"] is None and train["line_omega"] is None
    declared = READER.light_clicks(clicks, birth=100)
    assert declared["first_interval"] == 30 and declared["intervals"] == [11, 11, 8]
    assert declared["mean_interval"] == Fraction(30, 3)
    assert declared["birth_intervals"] == [118, 121, 119]
    # a train of many records (the light clock, one record per period): each click's
    # interval from its own birth stamp; the first click's from its own, none declared;
    # the window keeps a click with its own stamp
    many = READER.light_clicks(clicks)
    assert many["birth"] == 12 and many["first_interval"] == 118
    assert many["birth_intervals"] == [118, 121, 119]
    later = READER.light_clicks(clicks, window=(140, 155))
    assert later["count"] == 2 and later["birth"] == 20 and later["first_interval"] == 121
    assert later["birth_intervals"] == [121, 119] and later["intervals"] == [11]
    screen = READER.screen_clicks(clicks, row=[(70, 0, 0)])
    assert screen["counts"] == {(70, 0, 0): 2} and screen["unplaced"] == 1


def test_an_empty_train_reads_zero_clicks_and_raises_nothing():
    assert READER.clicks_of([]) == []
    assert READER.clicks_of([{"event": "block", "tick": 1}]) == []
    screen = READER.screen_clicks([])
    assert screen["total"] == 0 and screen["counts"] == {} and screen["unplaced"] == 0
    assert screen["centroid"] is None and screen["maxima"] == [] and screen["visibility"] is None
    row = [(0, y, 0) for y in range(3)]
    empty_row = READER.screen_clicks([], row=row)
    assert empty_row["counts"] == {node: 0 for node in row} and empty_row["centroid"] is None
    train = READER.light_clicks([], birth=5)
    assert train["count"] == 0 and train["first_tick"] is None and train["first_interval"] is None
    assert train["intervals"] == [] and train["mean_interval"] is None and train["line_omega"] is None
    assert train["birth_intervals"] == []
    one = READER.light_clicks([READER.Click(tick=9, node=None, cell=None)], birth=5)
    assert one["count"] == 1 and one["first_interval"] == 4 and one["mean_interval"] is None
    assert READER.click_mean_interval([]) is None and READER.click_mean_interval([4]) is None
