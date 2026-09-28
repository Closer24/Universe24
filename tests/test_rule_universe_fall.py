"""The reader of world (c) of the rule's universe (examples/events/experiments/rules_universe/fall_bias.py) on made-up outputs: the tail's ratio from the two neighbours' levels and the moves' bias from the body's centre against the blind numbers."""

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "examples" / "events" / "experiments" / "rules_universe"))

import fall_bias  # noqa: E402

BODY, WELL, FAR = [4, 1, 1], [5, 1, 1], [3, 1, 1]


def line(kind: str, key: str, values: list, **target: object) -> dict:
    """One reading of the runner's output: its kind and target, one line per interval with the value under `key`."""
    return {"kind": kind, **target, "lines": [{"interval": t, key: v} for t, v in enumerate(values)]}


def made_up(where: Path, well: list[int], far: list[int], centres: list[int], band: float | None):
    """A world's expectation with the `fall` section (the ratio 1.053, the bias 0.513) and a runner output with the level lines at both neighbours and the body's centre along x, written to `where`."""
    world, output = where / "made_up.json", where / "made_up.output.json"
    world.write_text("{}\n", encoding="utf-8")
    fall = {"body": BODY, "well_side": WELL, "far_side": FAR, "axis": 0}
    fall |= {"tail_ratio": 1.053, "bias": 0.513, "band": band}
    world.with_suffix(".expectation.json").write_text(json.dumps({"fall": fall}), encoding="utf-8")
    readings = [line("level", "level", well, node=WELL), line("level", "level", far, node=FAR)]
    readings.append(line("centre", "node", [[x, 1, 1] for x in centres], body=0))
    output.write_text(json.dumps({"verdict": "LAWFUL", "readings": readings}), encoding="utf-8")
    return world, output


def test_the_tails_ratio_and_the_moves_bias_on_made_up_outputs(tmp_path: Path):
    """Levels of 21 on the well's side against 20 on the far side read the ratio 21/20; a centre stepping toward the well 5 times and away 4 reads the bias 5/9 and the drift 1: MATCH within the band 0.05 of 1.053 and 0.513; no band reads alone; a centre that never moves reads no move."""
    rows = fall_bias.report(*made_up(tmp_path, [0, -21, 3], [0, 20, -2], [4, 5] * 5, 0.05))["fall"]
    assert rows["tail_ratio"] == [21, 20] and rows["bias"] == [5, 9] and rows["drift_along_axis"] == 1
    assert rows["moves"] == {"toward_well": 5, "away": 4, "all": 9} and rows["verdict"] == "MATCH"
    rows = fall_bias.report(*made_up(tmp_path, [1], [1], [4, 4, 4], None))["fall"]
    assert rows["verdict"] == "no move of the centre" and rows["tail_ratio"] == [1, 1]
    rows = fall_bias.report(*made_up(tmp_path, [9], [3], [4, 5], None))["fall"]
    assert rows["verdict"] == "no band yet" and rows["tail_ratio"] == [3, 1] and rows["bias"] == [1, 1]
