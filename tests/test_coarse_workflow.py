"""Research orchestration preserves evidence and fails on unsuccessful saved runs."""

import importlib
import json

import pytest

workflow = importlib.import_module("examples.coarse-graining.run_experiments")


def test_eight_headless_runs_share_retention_ownership_and_match_the_report(tmp_path):
    output = tmp_path / "experiment"
    report_path = workflow.run(output)
    report = json.loads(report_path.read_text(encoding="utf-8"))
    assert len(report["runs"]) == 8
    for entry in report["runs"]:
        directory = output.parent / entry["directory"]
        metadata = json.loads((directory / "run.json").read_text(encoding="utf-8"))
        assert metadata == entry["metadata"]
        assert metadata["status"] == "completed" and metadata["display"] == "none"
        assert metadata["source_sha256"] == report["source_sha256"]
        assert metadata["accounting_balanced_at_every_completed_tick"]
        assert (directory / "events.jsonl").is_file() and (directory / "state.json").is_file()
    assert report["routing"]["counts"] == {"0": 20, "3": 8}
    assert report["closure_search"]["conflicts"]["direction_phase"] == 0
    assert not list(tmp_path.rglob("*.gif")) and not list(tmp_path.rglob("*.html"))
    before = report_path.read_bytes()
    with pytest.raises(ValueError, match="empty experiment"):
        workflow.run(output)
    assert report_path.read_bytes() == before


def test_failed_canonical_run_cannot_be_reported_as_a_completed_experiment(tmp_path, monkeypatch):
    def fail(initialization, output):
        output.mkdir(parents=True)
        (output / "run.json").write_text(
            json.dumps({"status": "failed", "completed_ticks": 0, "error": "injected run failure"}),
            encoding="utf-8",
        )

    monkeypatch.setattr(workflow, "run_initialization", fail)
    output = tmp_path / "experiment"
    with pytest.raises(AssertionError, match="injected run failure"):
        workflow.run(output)
    assert not (output / "report.json").exists()
    assert (output / "inputs/momentum-route.json").exists()
