"""The series runner's list and its replay verdict (`tools/run_series.py
--list` and `--compare`; the gate set of the model owner's decision of
2026-09-20, Highlights 5.4). The expectations, written down first:

(a) `--list FILE` runs the worlds the file names, each path resolved relative
    to the file and each run at its listed `ticks` (a world with `entity_definitions`
    resolves its own reference beside its copy), and the summary gains the
    digest of `events.jsonl`; `--fast` runs each world to its listed `cap`;
(b) two runs of the same list on the same tree compared with `--compare` are
    identical world by world and the tool exits 0; a run in which one world
    ran longer (the detector world at its declared 4 intervals instead of 2,
    a click at the 4th) is reported as changed on that world's three digests
    and the tool exits 1; a world missing on either side is reported and
    fails; an earlier summary without the events digest (the tool before
    2026-09-20) is compared on the digests it recorded, one without any is
    reported;
(c) a list that names no world, an entry without a path, and `--fast` without
    `--list` are refused, and a series without any world too.
"""

from __future__ import annotations

import importlib.util
import json
import shutil
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("run_series", ROOT / "tools/run_series.py")
RUN_SERIES = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(RUN_SERIES)

WORLDS = ROOT / "examples" / "events"
ONE = "one_content.json"
DETECTOR = "detector/grouped_12_nodes.json"


def write_list(
    tmp_path: Path, name: str, ticks: dict[str, int], caps: dict[str, int] | None = None
) -> Path:
    """The two tiny worlds copied once beside the list files, listed at the given ticks."""
    folder = tmp_path / "worlds"
    if not folder.exists():
        folder.mkdir()
        shutil.copy(WORLDS / ONE, folder / ONE)
        (folder / "detector").mkdir()
        shutil.copy(WORLDS / DETECTOR, folder / DETECTOR)
        shutil.copytree(WORLDS / "detector" / "entities", folder / "detector" / "entities")
    entries = []
    for world, duration in ticks.items():
        entry: dict[str, object] = {"path": f"worlds/{world}", "ticks": duration, "covers": world}
        if caps and world in caps:
            entry["cap"] = caps[world]
        entries.append(entry)
    listing = tmp_path / f"{name}.json"
    listing.write_text(json.dumps({"format": "gate-set-v1", "worlds": entries}), encoding="utf-8")
    return listing


def run_main(monkeypatch, *arguments: str) -> int:
    monkeypatch.setattr(sys, "argv", ["run_series.py", *arguments])
    try:
        RUN_SERIES.main()
    except SystemExit as stop:
        return int(stop.code or 0)
    return 0


def summary(out: Path) -> list[dict[str, object]]:
    return json.loads((out / "summary.json").read_text(encoding="utf-8"))


def test_the_list_runs_each_world_at_its_listed_ticks_and_the_fast_pass_at_its_cap(
    tmp_path, monkeypatch, capsys
):
    """(a)."""
    listing = write_list(tmp_path, "list", {ONE: 2, DETECTOR: 3}, caps={DETECTOR: 1})
    worlds, durations = RUN_SERIES.read_list(listing)
    assert worlds == [(tmp_path / "worlds" / ONE).resolve(), (tmp_path / "worlds" / DETECTOR).resolve()]
    assert durations == {worlds[0]: 2, worlds[1]: 3}
    _, fast = RUN_SERIES.read_list(listing, fast=True)
    assert fast == {worlds[0]: 2, worlds[1]: 1}
    plain = tmp_path / "plain"
    assert run_main(monkeypatch, "--list", str(listing), "--jobs", "2", "--out", str(plain)) == 0
    rows = summary(plain)
    assert [(row["world"], row["status"], row["ticks"]) for row in rows] == [
        ("one_content", "completed", 2),
        ("grouped_12_nodes", "completed", 3),
    ]
    for row in rows:
        events = plain / str(row["world"]) / "run" / "events.jsonl"
        assert row["events_sha256"] == RUN_SERIES._digest(events.read_bytes())
    assert "events_sha256" in capsys.readouterr().out.splitlines()[0]
    fast_out = tmp_path / "fast"
    assert (
        run_main(monkeypatch, "--list", str(listing), "--fast", "--jobs", "2", "--out", str(fast_out))
        == 0
    )
    assert [row["ticks"] for row in summary(fast_out)] == [2, 1]


def test_the_compare_verdict_is_identical_on_a_replay_and_changed_on_a_longer_run(
    tmp_path, monkeypatch, capsys
):
    """(b)."""
    listing = write_list(tmp_path, "list", {ONE: 2, DETECTOR: 2})
    base = tmp_path / "base"
    assert run_main(monkeypatch, "--list", str(listing), "--jobs", "2", "--out", str(base)) == 0
    capsys.readouterr()
    earlier = summary(base)
    compare = ("--compare", str(base / "summary.json"))
    again = tmp_path / "again"
    assert (
        run_main(monkeypatch, "--list", str(listing), "--jobs", "2", "--out", str(again), *compare) == 0
    )
    assert capsys.readouterr().out.splitlines()[-2:] == [
        "one_content: identical",
        "grouped_12_nodes: identical",
    ]
    longer = write_list(tmp_path, "longer", {ONE: 2, DETECTOR: 4})
    out = tmp_path / "longer"
    assert run_main(monkeypatch, "--list", str(longer), "--jobs", "2", "--out", str(out), *compare) == 1
    assert capsys.readouterr().out.splitlines()[-2:] == [
        "one_content: identical",
        "grouped_12_nodes: changed: state_sha256, audit_sha256, events_sha256",
    ]
    rows = summary(out)
    assert RUN_SERIES.compare(rows[1:], earlier) == [
        ("grouped_12_nodes", "changed: state_sha256, audit_sha256, events_sha256"),
        ("one_content", "missing from this run"),
    ]
    assert RUN_SERIES.compare(rows, earlier[1:]) == [
        ("one_content", "missing from the earlier summary"),
        ("grouped_12_nodes", "changed: state_sha256, audit_sha256, events_sha256"),
    ]
    without_events = [{k: v for k, v in row.items() if k != "events_sha256"} for row in earlier]
    assert RUN_SERIES.compare(summary(again), without_events) == [
        ("one_content", "identical"),
        ("grouped_12_nodes", "identical"),
    ]
    without_digests = [{k: v for k, v in row.items() if not k.endswith("sha256")} for row in earlier]
    assert RUN_SERIES.compare(summary(again), without_digests)[0] == (
        "one_content",
        "no digests in the earlier summary",
    )


@pytest.mark.parametrize(
    "document,message",
    [
        ({"format": "gate-set-v1", "worlds": []}, "names no worlds"),
        ({"worlds": [{"ticks": 2}]}, "names no path"),
    ],
)
def test_a_list_without_worlds_or_paths_is_refused(tmp_path, monkeypatch, capsys, document, message):
    """(c)."""
    listing = tmp_path / "list.json"
    listing.write_text(json.dumps(document), encoding="utf-8")
    with pytest.raises(ValueError, match=message):
        RUN_SERIES.read_list(listing)
    assert run_main(monkeypatch, "--list", str(listing), "--out", str(tmp_path / "out")) == 1
    assert "Series refused" in capsys.readouterr().err
    assert not (tmp_path / "out").exists()


def test_fast_without_a_list_and_a_series_without_worlds_are_refused(tmp_path, monkeypatch, capsys):
    """(c)."""
    out = str(tmp_path / "out")
    assert run_main(monkeypatch, "--fast", "--out", out, str(WORLDS / ONE)) == 2
    assert "--fast needs --list" in capsys.readouterr().err
    assert run_main(monkeypatch, "--out", out) == 1
    assert "no worlds" in capsys.readouterr().err
    assert not (tmp_path / "out").exists()
