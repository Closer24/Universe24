"""Configuration preflight without running a world: the report, the refusals
named by the engine's parser, and the read-only command line."""

import json
from pathlib import Path

import pytest

from event_universe.configuration_validation import main, validate_configuration

ROOT = Path(__file__).resolve().parents[1]
WORLDS = sorted(
    path
    for path in (ROOT / "examples" / "events").rglob("*.json")
    # A world declares `law` and never `format`: an entity definitions file
    # (`event-entities-v1`) and a readings tool's expectations file
    # (`weak-expectations-v1`) are not worlds.
    if "format" not in json.loads(path.read_text(encoding="utf-8"))
)


@pytest.mark.parametrize("path", WORLDS, ids=[path.stem for path in WORLDS])
def test_every_shipped_world_is_valid_and_summarized(path):
    report = validate_configuration(path.read_bytes(), base_dir=path.parent)
    assert report.valid and report.kind == "beam" and not report.issues, report
    document = json.loads(path.read_text(encoding="utf-8"))
    assert report.summary["model"] == document["model_id"]
    assert report.summary["shape"] == tuple(document["shape"])
    assert report.summary["ticks"] == document["ticks"]
    if "measured" in document:
        assert report.summary["measured"] == len(document["measured"])


def test_the_refusal_names_the_key_and_creates_nothing(tmp_path):
    path = ROOT / "examples" / "events" / "one_content.json"
    world = json.loads(path.read_text(encoding="utf-8"))
    # The shipped world references the family definitions beside it
    # (2026-09-20): its directory is the file context.
    for key in ("schema_version", "fields", "dense_field"):
        report = validate_configuration(json.dumps({**world, key: 1}), base_dir=path.parent)
        assert not report.valid and key in report.issues[0].message
        assert report.issues[0].code == "validation"
    report = validate_configuration(
        json.dumps({k: v for k, v in world.items() if k != "law"}), base_dir=path.parent
    )
    assert not report.valid and '"law": "beam"' in report.issues[0].message
    report = validate_configuration('{"law": "beam", "law": "beam"}')
    assert report.issues[0].code == "syntax" and "duplicate JSON key" in report.issues[0].message
    report = validate_configuration("{", kind="beam")
    assert report.issues[0].code == "syntax" and report.issues[0].line == 1
    report = validate_configuration("{}", kind="catalog")
    assert report.issues[0].code == "unsupported_kind"
    assert list(tmp_path.iterdir()) == []


def test_the_command_line_reports_and_never_writes(tmp_path, capsys):
    bad = tmp_path / "bad.json"
    bad.write_text('{"law": "beam"}', encoding="utf-8")
    assert main([str(WORLDS[0])]) == 0
    assert capsys.readouterr().out.startswith("VALID ")
    assert main([str(bad), "--json"]) == 1
    report = json.loads(capsys.readouterr().out)
    assert report["valid"] is False and report["results"][0]["issues"][0]["code"] == "validation"
    assert main([str(tmp_path / "missing.json")]) == 1
    assert "input:" in capsys.readouterr().out
    assert sorted(path.name for path in tmp_path.iterdir()) == ["bad.json"]
