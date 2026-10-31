"""Tensor24's shipped worlds beside our bang, each run its first rounds out and back: the run back exact and the state's
digest the one the run tool wrote for those rounds in tensor24_prefixes.jsonl (derive/boss/prefixes/write.py), never
typed here; its no, the world's setting changed by one count."""

import json
from pathlib import Path

import pytest

from tensor24 import main
from tensor24.runner.files import NAMES

ROOT = Path(__file__).resolve().parents[1]
WRITTEN = [
    json.loads(x)
    for x in ROOT.joinpath("tests", "tensor24_prefixes.jsonl").read_text("utf-8").splitlines()
]


@pytest.mark.parametrize("written", WRITTEN, ids=[x["world"] for x in WRITTEN])
def test_each_world_runs_its_first_rounds_out_and_back_to_the_digest_the_run_wrote(written, tmp_path):
    """Yes: the world's own three files at the written rounds run out and back exact to the written digest. No: its
    setting with its first gear's count one more runs out and back exact to another digest."""
    *paths, setting = [ROOT / "examples" / written["world"] / f"{name}.json" for name in NAMES]
    ends = []
    for change in (0, 1):
        held, record = json.loads(setting.read_text(encoding="utf-8")), tmp_path / f"{change}.jsonl"
        held["ticks"], held["gears"][0][3] = written["rounds"], held["gears"][0][3] + change
        (tmp_path / f"{change}.json").write_text(json.dumps(held), encoding="utf-8")
        found = main.ran([*paths, tmp_path / f"{change}.json"], record)
        ends.append((found, json.loads(record.read_text("utf-8").splitlines()[-1])))
    (found, end), (other, moved) = ends
    assert found == other == [] and end == {k: v for k, v in written.items() if k != "world"}
    assert moved["exact"] == 1 and moved["digest"] != end["digest"]
