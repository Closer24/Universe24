"""The bending's two reading tools: the beam's centroid at a screen (tools/beam_centroid.py), the click-weighted mean of the strips' coordinate from the engine's counts per detector, exact, with the shift against a twin and its verdict within the band; and the well's clocks (tools/well_clocks.py), the wavelength, the period and the cycle from the GameBoard readings' sign changes, exact. COMPUTATION on made-up outputs; no pin of nature."""

from __future__ import annotations

import json
import sys
from fractions import Fraction
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

import well_clocks  # noqa: E402
from beam_centroid import centroid, main, report  # noqa: E402


def screen(directory: Path, name: str, counts: dict[str, int], shift: int | None) -> tuple[Path, Path]:
    """A world of three strips at y = 10, 11, 12 on x = 5 with an expectation naming the twin, and an output carrying the counts; the paths of both."""
    world = {"detectors": [{"name": f"screen_{y}", "positions": [[5, y, 0]]} for y in (10, 11, 12)]}
    (directory / f"{name}.json").write_text(json.dumps(world), encoding="utf-8")
    expectation = {"CENTROID": {"strips": "screen_", "twin": "twin", "shift": shift, "band": 1}}
    (directory / f"{name}.expectation.json").write_text(json.dumps(expectation), encoding="utf-8")
    output = {"counts": counts, "records_alive": 0}
    (directory / f"{name}.output.json").write_text(json.dumps(output), encoding="utf-8")
    return directory / f"{name}.json", directory / f"{name}.output.json"


def test_the_centroid_is_the_click_weighted_mean_and_the_shift_is_read_against_the_twin(tmp_path: Path):
    """Counts 1, 2, 5 at y = 10, 11, 12 give the centroid (10 + 22 + 60) / 8 exactly, with the face's and other clicks in the books; the twin at 4, 0, 0 sits at 10, so the shift is 11.5 - 10 = 3/2: MATCH within one Node of an expected 2 and MISS against 4; with no expected shift the verdict is a first look, and the command writes the report beside the output."""
    counts = {"screen_10": 1, "screen_11": 2, "screen_12": 5, "face": 3, "other": 1}
    world, output = screen(tmp_path, "beam", counts, 2)
    found = centroid(json.loads(world.read_text()), json.loads(output.read_text()), "screen_")
    assert Fraction(*found["centroid"]) == Fraction(1 * 10 + 2 * 11 + 5 * 12, 8) and found["axis"] == "y"
    books = (found["clicks_in_strips"], found["clicks_at_the_face"], found["clicks_elsewhere"])
    assert books == (8, 3, 1)
    twin = screen(tmp_path, "twin", {"screen_10": 4}, None)
    assert report([(world, output), twin])["shift"] == [3, 2]
    assert report([(world, output), twin])["verdict"] == "MATCH"
    assert report([screen(tmp_path, "far", counts, 4), twin])["verdict"] == "MISS"
    assert report([screen(tmp_path, "look", counts, None), twin])["verdict"].startswith("FIRST LOOK")
    assert main([str(world), str(output), str(twin[0]), str(twin[1])]) == 0
    assert json.loads((tmp_path / "beam.centroid.json").read_text())["shift"] == [3, 2]


def test_the_wells_clocks_read_the_wavelength_the_period_and_the_cycle_from_sign_changes(tmp_path: Path):
    """A level of period 8 (four positive, four negative) at one Node and of period 6 at the other gives the periods 8 and 6 and the ratio 4/3; along the axis a row of wavelength 4 inside the window and 6 in the other gives those wavelengths; the clocks' cycle starts 0, 9, 18 and 0, 8, 16 give the mean cycles 9 and 8, so the light's relative shift 6 / 4 - 1 over the clock's 9 / 8 - 1 is 4; a zero between signs breaks no count and fewer than two changes give None. Then the one-click look (examples/events/experiments/bending_look.py) on the same readings beside the first test's strips, the outputs read without the runner: five lines, DETECTOR on the centroid's shift (3/2, MATCH within 1 of 2) and GAMEBOARD on the rest (the ratio 4 MATCH within 1/2 of 4, the angle 3/2 over 10, the reversible and centre pins as written, the books)."""
    changes = well_clocks.mean_between_sign_changes
    assert (
        changes([1, 1, 0, -1, -1, 1, 1, -1]) == Fraction(2 * (7 - 3), 2) and changes([1, 1, -1]) is None
    )
    row = [0] * 90
    for x in range(30):
        row[x * 3 + 1] = (1 if (x // 2) % 2 == 0 else -1) if x < 15 else (1 if (x // 3) % 2 == 0 else -1)
    wave = lambda period, n: [1 if (t // (period // 2)) % 2 == 0 else -1 for t in range(n)]  # noqa: E731

    def series(name: str, key: str, values: list) -> dict:
        return {"name": name, "lines": [{"interval": t, key: v} for t, v in enumerate(values)]}

    def cycles(name: str, c: int, n: int) -> dict:
        lines = [{"interval": t, "cycle_start": c * (t // c), "cycle_length": c} for t in range(n)]
        return {"name": name, "lines": lines}

    readings = [series("light_rows", "rows", [row]), series("deep", "level", wave(8, 40))]
    readings += [series("outside", "level", wave(6, 42)), cycles("near", 9, 27), cycles("far", 8, 24)]
    (tmp_path / "well.json").write_text(json.dumps({"shape": [30, 3, 1]}), encoding="utf-8")
    well = {"rows": "light_rows", "levels": ["deep", "outside"], "clocks": ["near", "far"], "axis_y": 1}
    well["windows"] = [[0, 14], [15, 29]]
    (tmp_path / "well.expectation.json").write_text(json.dumps({"WELL": well}), encoding="utf-8")
    (tmp_path / "well.output.json").write_text(json.dumps({"readings": readings}), encoding="utf-8")
    found = well_clocks.report(tmp_path / "well.json", tmp_path / "well.output.json")
    assert [w["wavelength"] for w in found["wavelengths"]] == [[4, 1], [6, 1]]
    assert found["light_periods"] == [[8, 1], [6, 1]] and found["light_period_ratio"] == [4, 3]
    assert found["clock_cycles"] == [[9, 1], [8, 1]] and found["clock_ratio"] == [9, 8]
    shifts = (found["light_wave_number_shift"], found["clock_cycle_shift"], found["shift_ratio"])
    assert shifts == ([1, 2], [1, 8], [4, 1])  # (6 / 4 - 1) over (9 / 8 - 1)
    sys.path.insert(0, str(ROOT / "examples" / "events" / "experiments"))
    import bending_look  # noqa: PLC0415

    well.update(shift_ratio=4, shift_ratio_band=0.5, shift_ratio_before_the_conformal_term=2)
    row = {"before_the_axis_pace_term": 1, "row_as_written": 1.5, "screen_distance": 10}
    pins = [{"kind": "reversible", "verdict": "MATCH"}, {"kind": "centre", "verdict": "MATCH"}]
    clicks = {"bending": {"screen_10": 1, "screen_11": 2, "screen_12": 5}}
    for name, counts in {**clicks, "bending_twin": {"screen_10": 4}}.items():
        world, output = screen(tmp_path, name, counts, 2)
        extras = ((world, {"shape": [30, 3, 1]}), (output, {"readings": readings, "pins": pins}))
        for path, extra in extras:
            path.write_text(json.dumps({**json.loads(path.read_text()), **extra}), encoding="utf-8")
        expectation = json.loads(world.with_suffix(".expectation.json").read_text())
        expectation["CENTROID"].update(row, level_twice_over_once=2)
        world.with_suffix(".expectation.json").write_text(json.dumps({**expectation, "WELL": well}))
    assert bending_look.main(["--out", str(tmp_path), "--look", "--worlds", str(tmp_path)]) == 0
    lines = json.loads((tmp_path / "bending.look.json").read_text(encoding="utf-8"))["lines"]
    assert len(lines) == 5 and lines[0].startswith("1. DETECTOR")
    assert all("GAMEBOARD" in line for line in lines[1:]) and "1.50 Links" in lines[0]
    assert lines[0].endswith("MATCH") and "4.00" in lines[1] and "-- MATCH" in lines[1]
    assert "0.15000" in lines[2] and "['MATCH']" in lines[3] and "8 clicks in the strips" in lines[4]
