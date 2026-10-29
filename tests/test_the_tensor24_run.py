"""Tensor24's run (stage 10): the three files to a record the decoder reads, the run back checked, a departure named
before any record, and the run under masks the synchronous run at every count."""

import hashlib
import json
import subprocess
import sys
from pathlib import Path

import numpy as np

from tensor24 import main
from tensor24.decoder import records
from tensor24.runner import run
from tensor24.runner.files import NAMES, sites_of

ROOT = Path(__file__).resolve().parents[1]
EXAMPLES = ROOT / "examples" / "tensor24"
PATHS = [EXAMPLES / f"{name}.json" for name in NAMES]
SEED = 7  # the test's masks, drawn by numpy: the runner draws none
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
    _, piece, setting = (read(path) for path in PATHS)
    texts = [path.read_text(encoding="utf-8") for path in PATHS]
    assert [(f["name"], f["text"], f["digest"]) for f in held.header["files"]] == [
        (path.name, text, hashlib.sha256(text.encode("utf-8")).hexdigest())
        for path, text in zip(PATHS, texts, strict=True)
    ]
    assert held.header["sides"] == piece["shape"] and held.header["runner"] == "synchronous"
    ticks = setting["ticks"]
    assert held.end == {
        "kind": "end",
        "rounds": ticks,
        "digest": held.end["digest"],
        "undone": ticks,
        "exact": 1,
    }
    # every dial at the full rate: each Node-clock's k is written at its first beat alone, in the first round
    rates = [(e["round"], e["site"], e["count"], e["k"]) for e in held.of("rate")]
    assert rates == [(1, site, 1, 1) for site in range(sites_of(piece["shape"]))]
    *trains, time = held.header["trains"]
    assert time["label"] == run.TIME and time["winding"] > 1 and all(t["winding"] == 1 for t in trains)


def test_the_end_holds_the_digest_of_the_state_the_rounds_reach_and_reads_0_where_the_run_back_misses(
    tmp_path,
):
    record, missed = tmp_path / "run.jsonl", tmp_path / "missed.jsonl"
    reached = {}

    def kept(layout, s, out):
        reached.setdefault("end", s)  # the first state the run back reads is the rounds' last
        return s  # a run back that undoes nothing

    assert run.run(main.ENGINE._replace(untick=kept), PATHS, missed) == []
    assert main.ran(PATHS, record) == []
    end = read(record)[-1]
    assert end["exact"] == 1 and end["digest"] == run.digest(run.stated(reached["end"]))
    assert read(missed)[-1]["exact"] == 0 and read(missed)[-1]["digest"] == end["digest"]


def without_rounds(lines):
    """A record's events with their rounds taken out, in the order of their sites and counts, and its end without its rounds."""
    events = sorted((e["site"], e["count"], e["dial"], e["k"]) for e in lines[1:-1])
    return events, {key: value for key, value in lines[-1].items() if key not in ("rounds", "undone")}


def test_under_masks_the_run_is_the_synchronous_run_at_every_count(tmp_path):
    synchronous, masked = tmp_path / "synchronous.jsonl", tmp_path / "masked.jsonl"
    rng = np.random.default_rng(SEED)
    bits = lambda _, n: rng.integers(0, 1 + 1, n).tolist()  # noqa: E731
    assert main.ran(PATHS, synchronous) == [] and main.ran(PATHS, masked, bits) == []
    s, m = read(synchronous), read(masked)
    assert m[-1]["rounds"] > s[-1]["rounds"] and m[-1]["exact"] == 1  # the masks held beats back
    assert without_rounds(m) == without_rounds(s)
    named = ("record", "runner")  # the two fields that name the record and its runner
    assert {k: v for k, v in m[0].items() if k not in named} == {
        k: v for k, v in s[0].items() if k not in named
    }
    assert m[0]["runner"] == "under the caller's masks"


def test_a_node_clocks_k_is_written_at_its_first_beat_and_wherever_it_changes(tmp_path):
    def slowed(universe, shape, loaded):
        laid = main.layout(universe, shape, loaded)
        rate = laid.rate.copy()
        rate[0, 0] = laid.gamma // (
            1 + 1
        )  # one Node-clock at half the full rate: its k turns at every beat
        return laid._replace(rate=rate)

    record = tmp_path / "run.jsonl"
    assert run.run(main.ENGINE._replace(layout=slowed), PATHS, record) == []
    lines = read(record)
    slow = [(e["count"], e["k"]) for e in lines[1:-1] if e["site"] == 0]
    rest = [e["count"] for e in lines[1:-1] if e["site"] != 0]
    ticks = read(PATHS[-1])["ticks"]
    assert [count for count, _ in slow] == list(range(1, ticks + 1)) and set(rest) == {1}
    assert all(k != after for (_, k), (_, after) in zip(slow[:-1], slow[1:], strict=True))
    assert records.read(str(record))[1] == ""


def test_a_departing_file_or_a_broken_promise_is_named_and_no_record_is_written(tmp_path):
    universe, piece, setting = (read(path) for path in PATHS)
    universe["version"] = 1 + 1
    setting["gears"][0][-1] = TOOTH
    edits = (
        ("universe", universe, "universe.version: 1, not 2"),
        ("setting", setting, "row 0, site 0: the fine tooth"),
    )
    for name, held, named in edits:
        paths = list(PATHS)
        paths[NAMES.index(name)] = tmp_path / f"{name}.json"
        paths[NAMES.index(name)].write_text(json.dumps(held), encoding="utf-8")
        record = tmp_path / f"{name}.jsonl"
        found = main.ran(paths, record)
        assert len(found) == 1 and found[0].startswith(named) and not record.exists(), found


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
