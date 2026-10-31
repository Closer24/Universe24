"""Tensor24's shipped worlds beside our bang, each run its first rounds out and back (to its first click, if any): the run
back exact, the digest, the click lines and their digest the run tool wrote in tensor24_prefixes.jsonl (prefixes/write.py),
never typed here, every edge's books at 0, the record read by the decoder's reader; its no, the setting moved by one count."""

import dataclasses
import hashlib
import json
from pathlib import Path

import pytest

from tensor24 import main
from tensor24.decoder import records
from tensor24.record import schema
from tensor24.runner.files import NAMES

ROOT = Path(__file__).resolve().parents[1]
WRITTEN = [
    json.loads(x)
    for x in ROOT.joinpath("tests", "tensor24_prefixes.jsonl").read_text("utf-8").splitlines()
]


def ran(written, rounds, change, tmp_path):
    """The world's own files at the rounds, its first gear's count moved by the change: its departures, the end line, its click
    lines' count and digest (SHA-256, a line feed between two), the reader's cause; each line schema.Click's fields but the 1.3 tooth,
    its q its sides' sum (writer C's pin), each side (t, u) beside (u, t) at its place, q negated, each tooth key - 1 less the other."""
    *paths, setting = [ROOT / "examples" / written["world"] / f"{name}.json" for name in NAMES]
    held, record = json.loads(setting.read_text(encoding="utf-8")), tmp_path / f"{rounds}.{change}.jsonl"
    held["ticks"], held["gears"][0][3] = rounds, held["gears"][0][3] + change
    (tmp_path / f"{rounds}.{change}.json").write_text(json.dumps(held), encoding="utf-8")
    found = main.ran([*paths, tmp_path / f"{rounds}.{change}.json"], record)
    text = record.read_text("utf-8").splitlines()
    clicks = [x for x in text if json.loads(x)["kind"] == "click"]
    lines = hashlib.sha256("\n".join(clicks).encode("utf-8")).hexdigest()
    fields = ["kind", *(f.name for f in dataclasses.fields(schema.Click) if f.name != "tooth")]
    assert all(
        list(line) == fields and line["q"] == sum(side[1] for side in line["sides"])
        for line in map(json.loads, clicks)
    )
    lined, (card, *_) = [json.loads(x) for x in clicks], json.loads(text[0])["trains"]
    sides = {
        (x["round"], x["site"], x["train"], u): (q, b, a) for x in lined for u, q, b, a in x["sides"]
    }
    k = card["key"] - 1  # every side's key, the edge key, less 1
    assert all(
        sides.get((r, x, u, t)) == (-q, k - b, k - a) for (r, x, t, u), (q, b, a) in sides.items()
    )
    return found, json.loads(text[-1]), len(clicks), lines, records.read(str(record))[1]


@pytest.mark.parametrize("written", WRITTEN, ids=[x["world"] for x in WRITTEN])
def test_each_world_runs_its_first_rounds_out_and_back_to_the_digest_the_run_wrote(written, tmp_path):
    """Yes: the world's own three files at the written rounds run out and back exact to the written digest and click
    lines, the record read with no cause. No: its setting with its first gear's count one more runs out and back exact,
    at the written no rounds, to another digest than the world's own there, which is written too."""
    folders = sorted(f.name for f in (ROOT / "examples").glob("*/") if f.name != "tensor24")
    assert [x["world"] for x in WRITTEN] == folders  # every world but our bang's is written
    found, end, clicks, lines, cause = ran(written, written["rounds"], 0, tmp_path)
    assert found == [] and cause == "" and end == {k: written[k] for k in end}
    assert (clicks, lines) == (written["clicks"], written["lines"])
    (same, own, *_), (other, moved, *_) = (
        ran(written, written["no"], change, tmp_path) for change in (0, 1)
    )
    assert same == other == [] and own["digest"] == written["own"]
    assert moved["exact"] == 1 and moved["digest"] != own["digest"]
