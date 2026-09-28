"""The reader of worlds (a) and (b) of the rule's universe (examples/events/experiments/rules_universe/axis_tallies.py) on made-up outputs: the net and the raw tallies per axis from the clicks at the pixel's detector against the blind numbers."""

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "examples" / "events" / "experiments" / "rules_universe"))

import axis_tallies  # noqa: E402


def made_up(where: Path, tallies: list[tuple[int, list[int]]], net: list[int], band: float | None):
    """A world's expectation with the `axes` section (the blind net per interval `net`) and a runner output whose clicks at the pixel carry the tallies (interval, [x, y, z]), written to `where`."""
    world, output = where / "made_up.json", where / "made_up.output.json"
    world.write_text("{}\n", encoding="utf-8")
    axes = {"detector": "at_pixel", "net_per_interval": net, "raw_ratio": [1, 1, 1], "first_click": 1}
    axes |= {"band": band}
    world.with_suffix(".expectation.json").write_text(json.dumps({"axes": axes}), encoding="utf-8")
    clicks = [{"detector": "at_pixel", "interval": t, "tally": tally} for t, tally in tallies]
    clicks.append({"detector": "at_puller", "interval": 1, "tally": [9, 9, 9]})
    output.write_text(json.dumps({"verdict": "LAWFUL", "clicks": clicks}), encoding="utf-8")
    return world, output


def verdict(where: Path, tallies: list, net: list[int], band: float | None) -> str:
    """The `axes` row's verdict on the made-up output."""
    return axis_tallies.report(*made_up(where, tallies, net, band))["axes"]["verdict"]


def test_the_tallies_per_axis_on_made_up_outputs(tmp_path: Path):
    """Six clicks of one quantum through the six Ports read the net 0 on every axis and the raw 2 : 2 : 2 (1 : 1 : 1): white, MATCH within the band 0 of 0 : 0 : 0; clicks leaning along x (4 and -2 at interval 1, 3 at interval 2 with 1 and -1 on y and z) read the net [5, 1, -1], the raw [9, 1, 1], the peak 3 at interval 2: MATCH within the band 1 of [3, 0, 0], not white; the puller's clicks are not counted; no band reads alone; no click reads so; the moves per axis from made-up counts at the Node and its six neighbours; the record's period, amplitude and count over the last period from made-up levels against Cheshbon's b and period."""
    ports = [(1, [1, 0, 0]), (1, [-1, 0, 0]), (2, [0, 1, 0])]
    ports += [(2, [0, -1, 0]), (3, [0, 0, 1]), (3, [0, 0, -1])]
    rows = axis_tallies.report(*made_up(tmp_path, ports, [0, 0, 0], 0))["axes"]
    assert rows["net"] == [0, 0, 0] and rows["raw"] == [2, 2, 2] and rows["white"]
    assert rows["verdict"] == "MATCH"
    assert rows["raw_over_axes"] == [[1, 1]] * 3 and rows["first_click"] == 1 and rows["clicks"] == 6
    leaning = [(1, [4, 0, 0]), (1, [-2, 0, 0]), (2, [3, 1, -1])]
    rows = axis_tallies.report(*made_up(tmp_path, leaning, [3, 0, 0], 1))["axes"]
    assert rows["net"] == [5, 1, -1] and rows["raw"] == [9, 1, 1] and not rows["white"]
    assert rows["peak_interval"] == 2 and rows["net_per_interval_at_peak"] == [3, 1, -1]
    assert rows["verdict"] == "MATCH" and rows["net_over_axes"] == [[1, 1], [1, 5], [-1, 5]]
    assert verdict(tmp_path, leaning, [3, 0, 0], None) == "no band yet"
    assert verdict(tmp_path, [], [0, 0, 0], 0) == "no click at the detector"
    series = [[9, 0, 0, 0, 0, 0, 0], [6, 2, 0, 1, 0, 0, 0], [5, 3, 0, 1, 0, 0, 0]]
    moves = axis_tallies.moves_per_axis(series)
    assert moves["net"] == [3, 1, 0] and moves["raw"] == [3, 1, 0] and moves["peak_interval"] == 1
    assert moves["net_per_interval_at_peak"] == [2, 1, 0] and moves["pixel_count"]["least"] == 5
    record = axis_tallies.record_reading(
        [5, 3, -2, -5, -3, 2, 5, 3, -2, -5], [10] * 10, {"b": 5, "period": 6.5}
    )
    assert (
        record["period_intervals"] == 6.0
        and record["amplitude_b"] == 5
        and record["b_verdict"] == "MATCH"
    )
    assert record["period_verdict"] == "MATCH" and record["count_over_the_last_period"] == 10
