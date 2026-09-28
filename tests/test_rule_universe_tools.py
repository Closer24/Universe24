"""The reader of the rule's universe's first looks (examples/events/experiments/tube_clicks.py) on made-up outputs: the white pixel's three interval states and its quantum, the tube's clicks and their spacing against the blind number."""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "examples" / "events" / "experiments"))

import tube_clicks  # noqa: E402

NODE = [30, 2, 2]


def made_up(
    directory: Path, levels: list[int], clicks: list[int], tension: int | None
) -> tuple[Path, Path]:
    """A world's expectation with the `white` and `tube` sections and a runner output with the level lines at the pixel's Node and the clicks at the third, written to the directory."""
    world, output = directory / "made_up.json", directory / "made_up.output.json"
    world.write_text("{}\n", encoding="utf-8")
    white = {"node": NODE, "sum_ratio": 0, "period": 3, "band": 0, "row": "the three states"}
    tube = {"detector": "at_third", "axis": 0, "tension": tension, "band": 1, "row": "the tension"}
    world.with_suffix(".expectation.json").write_text(
        json.dumps({"white": white, "tube": tube}), encoding="utf-8"
    )
    lines = [{"interval": t, "level": v} for t, v in enumerate(levels)]
    found = [{"detector": "at_third", "interval": t, "tally": [1, 0, 0]} for t in clicks]
    readings = [{"kind": "level", "node": NODE, "lines": lines}]
    output.write_text(
        json.dumps({"verdict": "LAWFUL", "readings": readings, "clicks": found}), encoding="utf-8"
    )
    return world, output


def test_the_white_states_and_the_tubes_spacing_on_made_up_outputs(tmp_path: Path):
    """The period-3 rotation 6, -3, -3 sums to 0 at every interval (the ratio 0, the period 3, the quantum 27 constant: MATCH against the blind ratio 0 within the band 0); clicks every 10 intervals read the spacing 10 against the blind number 10 (MATCH) and no number reads the spacing alone; a rotation whose sum does not vanish reads its ratio and misses."""
    rows = tube_clicks.report(*made_up(tmp_path, [6, -3, -3] * 4, [10, 20, 30, 40], 10))
    assert rows["white"]["verdict"] == "MATCH" and rows["white"]["quantum"] == [27, 27]
    assert rows["white"]["sum_ratio"] == [0, 1] and rows["white"]["period"] == 3.0
    assert rows["tube"]["spacings"] == [10, 10, 10] and rows["tube"]["mean_spacing"] == [10, 1]
    assert rows["tube"]["sense_along_axis"] == {"forward": 4, "backward": 0, "none": 0}
    assert rows["tube"]["verdict"] == "MATCH"
    rows = tube_clicks.report(*made_up(tmp_path, [6, -3, -2, 6, -3, -2], [10, 25], None))
    assert rows["white"]["verdict"] == "MISS" and rows["white"]["sum_ratio"] == [1, 6]
    assert rows["tube"]["verdict"] == "no blind number yet" and rows["tube"]["mean_spacing"] == [15, 1]
