"""The series runner's host guards (`tools/run_series.py --wall-seconds` and
`--memory-mb`), both off by default. The expectations, written down first:

(a) under generous limits (600 s of wall clock, 8192 MB of address space) a
    tiny world completes and its summary row is unchanged against the run
    without guards: the status, the ticks and the three digests `--compare`
    reads, the verdict `identical`;
(b) under `--wall-seconds 0` every world of the series is killed at once and
    reported `not completed: wall 0 s` with no record of a run, the series
    goes on to the next world, the tool exits 1, and `--compare` reports the
    status in place of a verdict;
(c) under `--memory-mb 64`, too small for the interpreter's libraries, the
    world is reported `not completed: memory 64 MB` and the tool exits 1
    (Linux only: the address-space limit is enforced there); on a host without
    RLIMIT_AS the flag is refused before any world runs, and a negative wall
    or a non-positive memory limit is refused too.
"""

from __future__ import annotations

import importlib.util
import json
import resource
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("run_series", ROOT / "tools/run_series.py")
RUN_SERIES = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(RUN_SERIES)

WORLDS = ROOT / "examples" / "events"
ONE = str(WORLDS / "one_content.json")
TWO = str(WORLDS / "two_contents.json")
TICKS = ("--ticks", "2")

rlimit_as = pytest.mark.skipif(
    not hasattr(resource, "RLIMIT_AS") or not sys.platform.startswith("linux"),
    reason="RLIMIT_AS is enforced on Linux only",
)


def run_main(monkeypatch, *arguments: str) -> int:
    monkeypatch.setattr(sys, "argv", ["run_series.py", *arguments])
    try:
        RUN_SERIES.main()
    except SystemExit as stop:
        return int(stop.code or 0)
    return 0


def summary(out: Path) -> list[dict[str, object]]:
    return json.loads((out / "summary.json").read_text(encoding="utf-8"))


@rlimit_as
def test_generous_limits_leave_a_completed_world_and_its_summary_unchanged(
    tmp_path, monkeypatch, capsys
):
    """(a)."""
    plain = tmp_path / "plain"
    assert run_main(monkeypatch, "--jobs", "1", *TICKS, "--out", str(plain), ONE) == 0
    capsys.readouterr()
    guarded = tmp_path / "guarded"
    guards = ("--wall-seconds", "600", "--memory-mb", "8192")
    assert (
        run_main(
            monkeypatch,
            "--jobs",
            "1",
            *TICKS,
            *guards,
            "--out",
            str(guarded),
            "--compare",
            str(plain / "summary.json"),
            ONE,
        )
        == 0
    )
    assert capsys.readouterr().out.splitlines()[-1] == "one_content: identical"
    before, after = summary(plain)[0], summary(guarded)[0]
    assert (after["status"], after["ticks"], after["exit_code"]) == ("completed", 2, 0)
    assert [after[digest] for digest in RUN_SERIES.DIGESTS] == [
        before[digest] for digest in RUN_SERIES.DIGESTS
    ]
    assert (guarded / "one_content" / "run" / "run.json").exists()
    first_line = (guarded / "one_content" / "log.txt").read_text(encoding="utf-8").splitlines()[0]
    assert "RLIMIT_AS" in first_line and "8192 * 1024 * 1024" in first_line
    plain_first = (plain / "one_content" / "log.txt").read_text(encoding="utf-8").splitlines()[0]
    assert "RLIMIT_AS" not in plain_first and "-m event_universe" in plain_first


def test_a_wall_limit_of_zero_stops_every_world_and_the_series_goes_on(tmp_path, monkeypatch, capsys):
    """(b)."""
    plain = tmp_path / "plain"
    assert run_main(monkeypatch, "--jobs", "1", *TICKS, "--out", str(plain), ONE, TWO) == 0
    capsys.readouterr()
    out = tmp_path / "wall"
    assert (
        run_main(
            monkeypatch,
            "--jobs",
            "1",
            *TICKS,
            "--wall-seconds",
            "0",
            "--out",
            str(out),
            "--compare",
            str(plain / "summary.json"),
            ONE,
            TWO,
        )
        == 1
    )
    rows = summary(out)
    assert [(row["world"], row["status"], row["ticks"]) for row in rows] == [
        ("one_content", "not completed: wall 0 s", None),
        ("two_contents", "not completed: wall 0 s", None),
    ]
    assert all(row["exit_code"] < 0 and row["state_sha256"] is None for row in rows)
    for name in ("one_content", "two_contents"):
        assert (out / name / "log.txt").exists()
        assert not (out / name / "run" / "run.json").exists()
    printed = capsys.readouterr().out.splitlines()
    assert printed[-2:] == [
        "one_content: not completed: wall 0 s in this run",
        "two_contents: not completed: wall 0 s in this run",
    ]
    assert "| one_content | not completed: wall 0 s |" in printed[2]


@rlimit_as
def test_a_memory_limit_too_small_for_the_interpreter_is_reported(tmp_path, monkeypatch, capsys):
    """(c)."""
    out = tmp_path / "memory"
    assert run_main(monkeypatch, "--jobs", "1", *TICKS, "--memory-mb", "64", "--out", str(out), ONE) == 1
    (row,) = summary(out)
    assert (row["status"], row["ticks"], row["state_sha256"]) == (
        "not completed: memory 64 MB",
        None,
        None,
    )
    assert row["exit_code"] != 0
    log = (out / "one_content" / "log.txt").read_text(encoding="utf-8", errors="replace")
    assert any(mark in log for mark in RUN_SERIES.MEMORY_MARKS)
    assert not (out / "one_content" / "run" / "run.json").exists()
    assert "| one_content | not completed: memory 64 MB |" in capsys.readouterr().out


@pytest.mark.parametrize(
    "arguments,message",
    [
        (("--wall-seconds", "-1"), "must not be negative"),
        (("--memory-mb", "0"), "must be positive"),
    ],
)
def test_a_negative_wall_or_a_non_positive_memory_limit_is_refused(
    tmp_path, monkeypatch, capsys, arguments, message
):
    """(c)."""
    out = tmp_path / "out"
    assert run_main(monkeypatch, *arguments, "--out", str(out), ONE) == 1
    assert message in capsys.readouterr().err
    assert not out.exists()


def test_a_memory_limit_is_refused_on_a_host_without_rlimit_as(tmp_path, monkeypatch, capsys):
    """(c)."""
    monkeypatch.delattr(RUN_SERIES.resource, "RLIMIT_AS", raising=False)
    out = tmp_path / "out"
    assert run_main(monkeypatch, "--memory-mb", "64", "--out", str(out), ONE) == 1
    assert "RLIMIT_AS" in capsys.readouterr().err
    assert not out.exists()
