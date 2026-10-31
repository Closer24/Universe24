"""Tensor24's shipped worlds, each run its first rounds out and back (to its first click, if any): the run
back exact, the digest, the click lines and their digest the run tool wrote in tensor24_prefixes.jsonl (prefixes/write.py),
never typed here, every edge's books at 0, the record read by the decoder's reader; its no, the setting moved by one count."""

import dataclasses
import hashlib
import json
from pathlib import Path

import pytest

from tensor24 import main
from tensor24.decoder import records
from tensor24.engine import step
from tensor24.record import schema
from tensor24.runner import run
from tensor24.runner.files import NAMES
from tests import frame

ROOT = Path(__file__).resolve().parents[1]
WRITTEN = [
    json.loads(x)
    for x in ROOT.joinpath("tests", "tensor24_prefixes.jsonl").read_text("utf-8").splitlines()
]


def ran(written, rounds, change, tmp_path):
    """The world's own files at the rounds, its first gear's count moved by the change: its departures, the end line, its click
    lines' count and digest (SHA-256, a line feed between two), the reader's cause; each line schema.Click's fields, its q its sides'
    sum, Mesh sides too (writer C's pin), each side beside its mirror at the partner's place, q negated; the run's own end teeth paired."""
    *paths, setting = [ROOT / "examples" / written["world"] / f"{name}.json" for name in NAMES]
    held, record = json.loads(setting.read_text(encoding="utf-8")), tmp_path / f"{rounds}.{change}.jsonl"
    held["ticks"], held["gears"][0][3] = rounds, held["gears"][0][3] + change
    (short := tmp_path / f"{rounds}.{change}.json").write_text(json.dumps(held), encoding="utf-8")
    read = []  # every state the run back reads, the first the runner's own end state: the teeth are the board's
    back = main.ENGINE._replace(untick=lambda laid, s: step.untick(laid, read.append(s) or s))
    found = run.run(back, [*paths, short], record)
    text = record.read_text("utf-8").splitlines()
    clicks = [x for x in text if json.loads(x)["kind"] == "click"]
    lines = hashlib.sha256("\n".join(clicks).encode("utf-8")).hexdigest()
    fields = ["kind", *(f.name for f in dataclasses.fields(schema.Click))]
    lined, head = [json.loads(x) for x in clicks], json.loads(text[0])
    key, trains = head["dial"], len(head["trains"])  # the edge dial, every card's key
    assert {t["key"] for t in head["trains"]} == {key}
    # q the sum over a line's own Node-clock's sides and its Mesh sides; each side beside its mirror at the partner's place
    assert all([*x] == fields and x["q"] == sum(s[-1] for s in x["sides"] + x["across"]) for x in lined)
    met = {
        (x["round"], x["site"], x["train"], s[0], [*s[1:-1], x["site"]][0]): s[-1]
        for x in lined
        for s in x["sides"] + x["across"]
    }
    assert all(met.get((r, p, u, t, x)) == -q for (r, x, t, u, p), q in met.items())
    # every own side's tooth and its mirror's summing to key - 1 at the run's end, read on the board's own end state
    assert frame.opposed(0 * read[0].k, read[0].k, key, trains)
    return found, json.loads(text[-1]), len(clicks), lines, records.read(str(record))[1]


@pytest.mark.parametrize("written", WRITTEN, ids=[x["world"] for x in WRITTEN])
def test_each_world_runs_its_first_rounds_out_and_back_to_the_digest_the_run_wrote(written, tmp_path):
    """Yes: the world's own three files at the written rounds run out and back exact to the written digest and click
    lines, the record read with no cause. No: its setting with its first gear's count one more runs out and back exact,
    at the written no rounds, to another digest than the world's own there, which is written too."""
    folders = sorted(f.name for f in (ROOT / "examples").glob("*/"))
    assert [x["world"] for x in WRITTEN] == folders  # every world is written
    found, end, clicks, lines, cause = ran(written, written["rounds"], 0, tmp_path)
    assert found == [] and cause == "" and end == {k: written[k] for k in end}
    assert (clicks, lines) == (written["clicks"], written["lines"])
    (same, own, *_), (other, moved, *_) = (
        ran(written, written["no"], change, tmp_path) for change in (0, 1)
    )
    assert same == other == [] and own["digest"] == written["own"]
    assert moved["exact"] == 1 and moved["digest"] != own["digest"]
