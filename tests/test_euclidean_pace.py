"""Euclidean pace probe: the front is round, the fringe follows Euclidean distance, worlds close."""

import importlib.util
import json
from pathlib import Path

from event_universe.runner import run_initialization

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "euclidean_pace_probe", ROOT / "examples/euclidean-pace/run_experiments.py"
)
PROBE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(PROBE)


def test_the_front_is_an_octahedron_on_links_and_round_on_the_euclidean_metric():
    links = PROBE.front(PROBE.front_document("links"))
    assert links["links"] == {"axis": [12], "face": [12], "body": [12]}
    assert links["spread"] == 1.732 and links["quanta_closed"]
    round_front = PROBE.front(PROBE.front_document("euclidean"))
    assert round_front["links"] == {"axis": [6], "face": [9], "body": [12]}
    assert round_front["spread"] < 1.2 and round_front["quanta_closed"]


def test_the_fringe_minima_move_from_manhattan_to_euclidean_path_difference():
    assert PROBE.predicted_minima("links") == [-1, 1]
    assert PROBE.predicted_minima("euclidean") == [-5, -4, 4, 5]
    links = PROBE.fringe(PROBE.fringe_document("links"))
    assert links["darkest"] == [-1, 1] and links["quanta_closed"]
    assert len({links["readings"][x] for x in range(2, PROBE.SCREEN_HALF - 2)}) == 1
    euclidean = PROBE.fringe(PROBE.fringe_document("euclidean"))
    assert euclidean["darkest"] == [-5, 5] and euclidean["quanta_closed"]
    assert euclidean["readings"][0] > 4 * euclidean["readings"][5]


def test_the_metric_is_identified_and_validated(tmp_path):
    raw = PROBE.front_document("euclidean", ticks=2)
    del raw["emissions"][0]["recoil_field"]
    path = tmp_path / "front.json"
    path.write_text(json.dumps(raw))
    run_initialization(path, tmp_path / "out", ticks=2)
    metadata = json.loads((tmp_path / "out" / "run.json").read_text())
    assert metadata["spatial_metric"] == "euclidean-ray-pace-v1"
    assert metadata["spatial_policy"] == "isotropic-ray-field-v1"
