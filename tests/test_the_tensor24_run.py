"""Tensor24's run (stage 10): the three files to a record and a ledger the decoder reads, every train's counts at
every Node-clock and round, the run back checked, and a departure named before anything is written."""

import dataclasses
import hashlib
import json
import subprocess
import sys
from pathlib import Path

from tensor24 import main
from tensor24.decoder import records
from tensor24.engine import step
from tensor24.engine.state import State
from tensor24.record import schema
from tensor24.runner import run
from tensor24.runner.files import NAMES, sites_of, whole
from tensor24.runner.load import load, star

ROOT = Path(__file__).resolve().parents[1]
EXAMPLES = ROOT / "examples" / "tensor24"
PATHS = [EXAMPLES / f"{name}.json" for name in NAMES]
TOOTH = 1 << 127  # a fine tooth within the files' width and past light's teeth, 2 T


def read(path):
    """A file of JSON, or a record's lines, each a JSON object."""
    text = path.read_text(encoding="utf-8")
    return (
        [json.loads(line) for line in text.splitlines()] if path.suffix == ".jsonl" else json.loads(text)
    )


def test_the_example_files_run_to_a_record_the_decoder_reads_with_its_run_back_exact(tmp_path):
    record = tmp_path / "run.jsonl"
    assert main.ran(PATHS, record) == []
    held, cause = records.read(str(record))
    assert cause == "" and held is not None
    universe, piece, setting = (read(path) for path in PATHS)
    texts = [path.read_text(encoding="utf-8") for path in PATHS]
    assert [(f["name"], f["text"], f["digest"]) for f in held.header["files"]] == [
        (path.name, text, hashlib.sha256(text.encode("utf-8")).hexdigest())
        for path, text in zip(PATHS, texts, strict=True)
    ]
    assert held.header["sides"] == piece["shape"] and held.header["runner"] == "synchronous"
    ticks = setting["ticks"]
    end = dict(kind="end", rounds=ticks, digest=held.end["digest"], undone=ticks, exact=1)
    # no rate line: every Node-clock steps in every round, and light alone never clicks
    assert held.end == end and held.events == []
    # the file's trains alone, the metric family among them, each winding 1 until G3
    cards = held.header["trains"]
    assert [t["label"] for t in cards] == [t["name"] for t in universe["trains"]]
    assert {t["winding"] for t in cards} == {1}


def test_the_end_holds_the_digest_of_the_state_the_rounds_reach_and_reads_0_where_the_run_back_misses(
    tmp_path,
):
    record, missed = tmp_path / "run.jsonl", tmp_path / "missed.jsonl"
    reached = {}

    def kept(layout, s):
        reached.setdefault("end", s)  # the first state the run back reads is the rounds' last
        return s  # a run back that undoes nothing

    assert run.run(main.ENGINE._replace(untick=kept), PATHS, missed) == []
    assert main.ran(PATHS, record) == []
    end = read(record)[-1]
    assert end["exact"] == 1 and end["digest"] == run.digest(run.stated(reached["end"]))
    assert read(missed)[-1]["exact"] == 0 and read(missed)[-1]["digest"] == end["digest"]


def test_the_ledger_holds_every_trains_counts_at_every_node_clock_after_every_round(tmp_path):
    """Beside the record, one Count line per round, Node-clock and train, in that order, schema.Count's fields of their
    shapes, and the decoder reads them: the train's now counts there, row by row, as the engine's own rounds reach
    them; the metric family stands at rest in every line."""
    record = tmp_path / "run.jsonl"
    assert main.ran(PATHS, record) == []
    universe, piece, setting = (read(path) for path in PATHS)
    held, _ = load(universe, setting, sites_of(piece["shape"]), *main.made(star(len(piece["shape"]))))
    laid, s, wanted = main.layout(universe, piece["shape"], held), State(*held.state), []
    for at in range(1, setting["ticks"] + 1):
        s = step.tick(laid, s)
        wanted += [
            {
                "round": at,
                "at": "step",
                "site": site,
                "train": n,
                "count": s.a[t.first : t.first + t.rows(), site].tolist(),
            }
            for site in range(sites_of(piece["shape"]))
            for n, t in enumerate(held.trains)
        ]
    lines, fields = (
        read(run.ledger_of(record)),
        [field.name for field in dataclasses.fields(schema.Count)],
    )
    shaped = [
        list(x) == fields and all(map(whole, (x["round"], x["site"], x["train"], *x["count"])))
        for x in lines
    ]
    assert (
        lines == wanted
        and all(shaped)
        and records.read_ledger(str(run.ledger_of(record))) == (lines, "")
    )
    rest = {x["train"]: x["count"] for x in lines if held.trains[x["train"]].square}
    assert set(rest) and all(not any(count) for count in rest.values())


def test_a_departing_file_or_a_broken_promise_is_named_and_no_record_is_written(tmp_path):
    universe, piece, setting = (read(path) for path in PATHS)
    universe["version"] = 1 + 1
    setting["gears"][0][-1] = TOOTH
    edits = (
        ("universe", universe, "universe.version: 1, not 2"),
        ("setting", setting, "round 1: row 0, site 0: the fine tooth"),
    )
    for name, held, named in edits:
        paths = list(PATHS)
        paths[NAMES.index(name)] = tmp_path / f"{name}.json"
        paths[NAMES.index(name)].write_text(json.dumps(held), encoding="utf-8")
        record = tmp_path / f"{name}.jsonl"
        found = main.ran(paths, record)
        assert len(found) == 1 and found[0].startswith(named), found
        assert not record.exists() and not run.ledger_of(record).exists()


def test_the_tool_runs_the_files_and_names_a_departure(tmp_path):
    tool, record = ROOT / "tools" / "tensor24_run.py", tmp_path / "run.jsonl"
    done = subprocess.run(
        [sys.executable, "-I", str(tool), *map(str, PATHS), str(record)], capture_output=True, text=True
    )
    assert (
        done.returncode == 0
        and done.stdout == f"{record}: written\n"
        and records.read(str(record))[1] == ""
    )
    missing, none = tmp_path / "missing.json", tmp_path / "none.jsonl"
    done = subprocess.run(
        [sys.executable, "-I", str(tool), str(missing), *map(str, PATHS[1:]), str(none)],
        capture_output=True,
        text=True,
    )
    assert done.returncode == 1 and "missing.json: not read" in done.stdout and not none.exists()
