"""The bending's reading tools: the beam's centroid at a screen (tools/beam_centroid.py), the click-weighted mean of the strips' coordinate from the engine's counts per detector, exact, with the shift against a twin and its verdict within the band; the well's clocks (tools/well_clocks.py), the wavelength, the period and the cycle from the GameBoard readings' sign changes, exact; and the one-click look (examples/events/experiments/bending_look.py), five lines from the outputs read without the runner; the rule's look (rule_redshift_look.py) reads the clocks' ratio along the run in ten spans and its drift per interval, the stepping Gamma's reading. The made-up readings: the level along the axis with the wavelength 4 in the first window and 6 in the second, the levels at two Nodes of periods 8 and 6, the clocks' cycle starts every 9 and every 8 with the cycle's length on every line; the made-up world: three strips at y = 10, 11, 12 on x = 5, its expectation (the centroid's shift and band, the well's readings' names) and its output (the counts and whatever else is given). COMPUTATION on made-up outputs; no pin of nature."""

import json
import sys
from fractions import Fraction
from pathlib import Path

sys.path[:0] = [str(Path(__file__).parents[1] / d) for d in ("tools", "examples/events/experiments")]

import bending_look  # noqa: E402
import rule_redshift_look  # noqa: E402
import well_clocks  # noqa: E402
from beam_centroid import centroid, main, report  # noqa: E402

ROW = dict(before_the_axis_pace_term=1, row_as_written=1.5, screen_distance=10, level_twice_over_once=2)
WELL = dict(rows="light_rows", levels=["deep", "out"], clocks=["near", "far"], axis_y=1, shift_ratio=4)
WELL.update(windows=[[0, 14], [15, 29]], shift_ratio_band=0.5, shift_ratio_before_the_conformal_term=2)
PINS = [{"kind": "reversible", "verdict": "MATCH"}, {"kind": "centre", "verdict": "MATCH"}]
STRIPS = [{"name": f"screen_{y}", "positions": [[5, y, 0]]} for y in (10, 11, 12)]


def lines(name: str, key: str, values: list, **more: int) -> dict:
    return {"name": name, "lines": [{"interval": t, key: v, **more} for t, v in enumerate(values)]}


def readings() -> list[dict]:
    row = [1 - 2 * ((i // (6 if i < 45 else 9)) % 2) if i % 3 == 1 else 0 for i in range(90)]
    deep = lines("deep", "level", [1 if (t // 4) % 2 == 0 else -1 for t in range(40)])
    out = lines("out", "level", [1 if (t // 3) % 2 == 0 else -1 for t in range(42)])
    near = lines("near", "cycle_start", [9 * (t // 9) for t in range(27)], cycle_length=9)
    far = lines("far", "cycle_start", [8 * (t // 8) for t in range(200)], cycle_length=8)
    return [lines("light_rows", "rows", [row]), deep, out, near, far]


def screen(directory: Path, name: str, counts: dict, shift: int | None, **output) -> tuple[Path, Path]:
    world, out = {"shape": [30, 3, 1], "detectors": STRIPS}, {"counts": counts, **output}
    row = {"CENTROID": dict(ROW, strips="screen_", twin="twin", shift=shift, band=1), "WELL": WELL}
    for suffix, document in (("", world), (".expectation", row), (".output", out)):
        (directory / f"{name}{suffix}.json").write_text(json.dumps(document), encoding="utf-8")
    return directory / f"{name}.json", directory / f"{name}.output.json"


def test_the_centroid_the_wells_clocks_and_the_one_click_look_on_made_up_outputs(tmp_path: Path):
    """Counts 1, 2, 5 at y = 10, 11, 12 give the centroid (10 + 22 + 60) / 8 exactly, with the face's and other clicks in the books; the twin at 4, 0, 0 sits at 10, so the shift is 11.5 - 10 = 3/2: MATCH within one Node of an expected 2 and MISS against 4; with no expected shift the verdict is a first look, and the command writes the report beside the output. The well's clocks: the periods 8 and 6 at the two Nodes and their ratio 4/3; along the axis the wavelengths 4 inside the window and 6 in the other; the cycle starts every 9 and every 8 give the mean cycles 9 and 8, so the light's relative shift 6 / 4 - 1 over the clock's 9 / 8 - 1 is 4; a zero between signs breaks no count and fewer than two changes give None. Then the one-click look on the same readings beside the strips, the outputs read without the runner: five lines, DETECTOR on the centroid's shift (3/2, MATCH within 1 of 2) and GAMEBOARD on the rest (the ratio 4 MATCH within 1/2 of 4, the angle 3/2 over 10, the reversible and centre pins as written, the books). The rule's look on a near clock of cycle 9 that steps to 11 from interval 99 against a far clock of 8 over 200 intervals: the ratio 9/8 in the first five spans of 20, none in the span holding one start, 11/8 in the last four, so the drift is (11/8 - 9/8) over the span centres 10 to 190 = 1/720."""
    counts = {"screen_10": 1, "screen_11": 2, "screen_12": 5, "face": 3, "other": 1}
    world, output = screen(tmp_path, "beam", counts, 2)
    found = centroid(json.loads(world.read_text()), json.loads(output.read_text()), "screen_")
    assert Fraction(*found["centroid"]) == Fraction(1 * 10 + 2 * 11 + 5 * 12, 8) and found["axis"] == "y"
    assert [found[f"clicks_{k}"] for k in ("in_strips", "at_the_face", "elsewhere")] == [8, 3, 1]
    twin = screen(tmp_path, "twin", {"screen_10": 4}, None)
    assert [report([(world, output), twin])[k] for k in ("shift", "verdict")] == [[3, 2], "MATCH"]
    assert report([screen(tmp_path, "far", counts, 4), twin])["verdict"] == "MISS"
    assert report([screen(tmp_path, "look", counts, None), twin])["verdict"].startswith("FIRST LOOK")
    assert main([str(world), str(output), str(twin[0]), str(twin[1])]) == 0
    assert json.loads((tmp_path / "beam.centroid.json").read_text())["shift"] == [3, 2]
    assert (changes := well_clocks.mean_between_sign_changes)([1, 1, -1]) is None
    assert changes([1, 1, 0, -1, -1, 1, 1, -1]) == 2 * (7 - 3) / 2
    f = well_clocks.report(*screen(tmp_path, "well", {}, None, readings=readings()))
    assert [w["wavelength"] for w in f["wavelengths"]] == [[4, 1], [6, 1]]
    assert f["light_periods"] == [[8, 1], [6, 1]] and f["light_period_ratio"] == [4, 3]
    assert (f["clock_cycles"], f["clock_ratio"], f["shift_ratio"]) == ([[9, 1], [8, 1]], [9, 8], [4, 1])
    assert (f["light_wave_number_shift"], f["clock_cycle_shift"]) == ([1, 2], [1, 8])  # 6/4 - 1, 9/8 - 1
    for name, count in zip(("bending", "bending_twin"), (counts, {"screen_10": 4}), strict=True):
        screen(tmp_path, name, count, 2, readings=readings(), pins=PINS)
    assert bending_look.main(["--out", str(tmp_path), "--look", "--worlds", str(tmp_path)]) == 0
    five = json.loads((tmp_path / "bending.look.json").read_text(encoding="utf-8"))["lines"]
    assert len(five) == 5 and five[0].startswith("1. DETECTOR") and "1.50 Links" in five[0]
    assert all("GAMEBOARD" in x for x in five[1:]) and "['MATCH']" in five[3] and "8 clicks" in five[4]
    assert "-- MATCH" in five[0] and "4.00" in five[1] and "-- MATCH" in five[1] and "0.150" in five[2]
    a = lines("near", "cycle_start", [t - t % (9 if t < 99 else 11) for t in range(200)], cycle_length=9)
    along = rule_redshift_look.ratio_along({"readings": [a, readings()[4]]}, ["near", "far"])
    assert along["drift_per_interval"] == [1, 720] and along["spans"][5]["ratio"] is None
