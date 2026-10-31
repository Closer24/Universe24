"""Tensor24's shipped worlds beside our bang, each run its first rounds out and back (the click world's to its first click):
the run back exact, the digest and the click lines the run tool wrote in tensor24_prefixes.jsonl (prefixes/write.py),
never typed here; its no, the world's setting changed by one count."""

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


def ran(written, rounds, change, tmp_path):
    """The world's own three files at the rounds, its first gear's count moved by the change: departures, end, clicks."""
    *paths, setting = [ROOT / "examples" / written["world"] / f"{name}.json" for name in NAMES]
    held, record = json.loads(setting.read_text(encoding="utf-8")), tmp_path / f"{rounds}.{change}.jsonl"
    held["ticks"], held["gears"][0][3] = rounds, held["gears"][0][3] + change
    (tmp_path / f"{rounds}.{change}.json").write_text(json.dumps(held), encoding="utf-8")
    found = main.ran([*paths, tmp_path / f"{rounds}.{change}.json"], record)
    lines = [json.loads(x) for x in record.read_text("utf-8").splitlines()]
    return found, lines[-1], sum(x["kind"] == "click" for x in lines)


@pytest.mark.parametrize("written", WRITTEN, ids=[x["world"] for x in WRITTEN])
def test_each_world_runs_its_first_rounds_out_and_back_to_the_digest_the_run_wrote(written, tmp_path):
    """Yes: the world's own three files at the written rounds run out and back exact to the written digest and clicks.
    No: its setting with its first gear's count one more runs out and back exact to another digest than its own."""
    folders = sorted(f.name for f in (ROOT / "examples").glob("*/") if f.name != "tensor24")
    assert [x["world"] for x in WRITTEN] == folders  # every world but our bang's is written
    found, end, clicks = ran(written, written["rounds"], 0, tmp_path)
    assert found == [] and end == {
        k: v for k, v in written.items() if k not in ("world", "clicks", "no")
    }
    assert clicks == written["clicks"]
    (same, own, _), (other, moved, _) = (
        ran(written, written["no"], change, tmp_path) for change in (0, 1)
    )
    assert same == other == [] and moved["exact"] == 1 and moved["digest"] != own["digest"]
