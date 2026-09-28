"""The beam's centroid at a screen (tools/beam_centroid.py): the click-weighted mean of the strips' coordinate from the engine's counts per detector, exact; the shift against a twin and its verdict within the band. COMPUTATION on a made-up output; no pin of nature."""

from __future__ import annotations

import json
import sys
from fractions import Fraction
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

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
