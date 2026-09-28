"""THE WINDOW WRITES BOTH LEVELS and THE CLOSE RETURNS THE CURRENT (Cheshbon's lines of 2026-09-28, 12:23, 13:16 and 13:27 Israel; the Clock's rest world of 12 x 2,000 handed on #1325): the given record is a wave, not a step, and after the close the zero mode's weighted current stays within the division's remainders, so the level at the body's Node no longer grows linearly and the run is not refused above A."""

from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np

from event_universe.events.detector_law import DetectorLawSimulation
from event_universe.world_files import input_stamp, load_world

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

from body_generator import generate, input_digest, mode_document, split_levels  # noqa: E402

REST = ROOT / "tests" / "rest_giver.json"
BODY = (599, 0, 0)  # the giver's Node the Clock read (the 12 Nodes stand at x = 594..605)


def rest_world(tmp_path: Path) -> Path:
    """The Clock's rest world beside its mode file, both written by the generator into `tmp_path` (the universe of record by name)."""
    document = json.loads(REST.read_text(encoding="utf-8"))
    document.pop("stamp", None)
    document["stamp"] = input_stamp(document)
    reading = generate(document)
    reading["world_digest"] = input_digest(document)
    profiles, levels = split_levels(reading)
    (tmp_path / "rest.json").write_text(json.dumps(document), encoding="utf-8")
    (tmp_path / "rest.mode.json").write_text(json.dumps(mode_document(reading, profiles, levels)))
    return tmp_path / "rest.json"


def weighted_current(simulation: DetectorLawSimulation, live) -> tuple[int, int]:
    """The zero mode's weighted current SUM q_n (now_n - before_n) and the weights' sum over the record's support, q_n = (Gamma 2^8)^2 div p_n^2 at the Node's Link pace under the conformal pace, p_n = Gamma - 2 c_n - (the axis contents over the six Ports) div 6 (Cheshbon's line of 16:06 Israel; the close's own weights, without the carried remainder)."""
    gamma = int(simulation.node_clock)
    content = simulation._effective_content(live.family)
    axis = simulation._axis_contents(live.family)
    support = (live.now != 0) | (live.before != 0)
    unit = (gamma << 8) * (gamma << 8)
    current = total = 0
    for node in zip(*np.nonzero(support), strict=True):
        ports = 0 if axis is None else 2 * sum(int(t[node]) for t in axis)
        weight = unit // (gamma - 2 * int(content[node]) - ports // 6) ** 2
        current += weight * (int(live.now[node]) - int(live.before[node]))
        total += weight
    return current, total


def test_the_rest_world_runs_its_first_window_and_the_close_leaves_no_current(tmp_path):
    """The window opens, writes and closes within the first intervals (6 on the corrected giving alone, 16 under the conformal term: the light's pace at the giver is slower there, the outward flux per interval smaller); the giving line books the zero mode's velocity B; three intervals after the close the weighted current stays within (t - t_close + 1) weight sums (one division remainder per Node per interval); the given record stands under A at every interval, and the level's step at the body's Node shrinks from the close to the last interval: a wave passing, not a linear growth."""
    lines: list[dict] = []
    simulation = DetectorLawSimulation(load_world(rest_world(tmp_path)), observer=lines.append)
    light = [f.name for f in simulation.families].index("charge")
    levels: list[int] = []
    horizon = 40  # the first close within it, then three intervals more; a level above A ends the run: no refusal is the first assertion
    while simulation.tick < horizon and not [line for line in lines if line["event"] == "giving"]:
        simulation.step()
        records = [live for live in simulation.records.values() if live.family == light]
        levels.append(int(records[0].now[BODY]) if records else 0)
    for _ in range(3):
        simulation.step()
        records = [live for live in simulation.records.values() if live.family == light]
        levels.append(int(records[0].now[BODY]) if records else 0)
    givings = [line for line in lines if line["event"] == "giving"]
    assert len(givings) == 1 and givings[0]["window"] >= 1 and "zero_mode" in givings[0]
    close = int(givings[0]["tick"])
    given = simulation.records[int(givings[0]["record"])]
    assert given.zero_mode is not None and given.zero_mode[0] == givings[0]["zero_mode"]
    current, total = weighted_current(simulation, given)
    # the mean Link pace's weight is exact where the neighbours' counts are equal and leaves a remainder of the order (the spread of the contents) / (the Link pace) of the current taken off (Cheshbon's line of 16:06 Israel), beside one division remainder per Node per interval
    content = simulation._effective_content(given.family)[given.zero_mode[1]]
    spread, pace = (
        int(content.max() - content.min()),
        int(simulation.node_clock) - 2 * int(content.max()),
    )
    allowance = (simulation.tick - close + 1) * total + abs(given.zero_mode[0]) * total * spread // pace
    assert total > 0 and abs(current) <= allowance
    steps = [abs(levels[t] - levels[t - 1]) for t in range(close, len(levels))]  # from the close on
    assert (
        len(steps) >= 3 and steps[-1] < steps[0]
    )  # a wave passing the body's Node, not a linear growth
