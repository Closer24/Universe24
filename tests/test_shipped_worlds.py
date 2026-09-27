"""Every shipped world bit for bit: each world of tests/shipped_worlds.json (written by tools/record_shipped_worlds.py) replayed for its recorded intervals and its state digest compared; selected when a pull request touches what runs a world. HOST readings only."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from tests.worlds import load_file

ROOT = Path(__file__).resolve().parents[1]
RECORD = ROOT / "tests" / "shipped_worlds.json"


def recorder():  # type: ignore[no-untyped-def]
    return load_file("record_shipped_worlds", ROOT / "tools" / "record_shipped_worlds.py")


RECORDED = json.loads(RECORD.read_text(encoding="utf-8"))
WORLDS = sorted(RECORDED["worlds"])


def test_the_record_names_every_shipped_world_and_nothing_else():
    module = recorder()
    shipped = sorted(path.relative_to(ROOT).as_posix() for path in module.shipped_worlds())
    assert shipped == WORLDS and RECORDED["format"] == module.FORMAT, "a world came or went: record it"
    for entry in RECORDED["worlds"].values():
        assert 1 <= entry["intervals"] <= entry["ticks"] and len(entry["digest"]) == 64


@pytest.mark.parametrize("world", WORLDS)
def test_a_shipped_world_runs_bit_for_bit_as_recorded(world: str):
    module = recorder()
    expected = RECORDED["worlds"][world]
    actual = module.run(ROOT / world, expected["intervals"], ROOT / "artifacts" / "record")
    assert actual["stamp"] == expected["stamp"], f"{world}: the world file changed; re-record it"
    assert actual["digest"] == expected["digest"], (
        f"{world}: the run moved after {expected['intervals']} intervals "
        f"(records {expected['records']} -> {actual['records']}, clicks {expected['clicks']} -> "
        f"{actual['clicks']}, lines {expected['lines']} -> {actual['lines']}); "
        "an intended change re-records it in the same commit"
    )


def test_the_digest_does_not_move_under_a_rename_of_the_engines_attributes():
    """Renaming any attribute of the engine leaves the digest where it is or breaks the reader aloud, never moves it: the reading's keys are the files' names and the ledger's words."""
    from event_universe.events.detector_law import DetectorLawSimulation
    from event_universe.world_files import parse_nature_beam_world

    module = recorder()
    world = ROOT / "examples/events/massive_record/light_clock.json"
    document = json.loads(world.read_text(encoding="utf-8"))
    simulation = DetectorLawSimulation(parse_nature_beam_world(document))
    lines: list[dict[str, object]] = []
    simulation.record = lines.append
    for _ in range(40):
        simulation.step()
    before = module.digest_of(module.run_reading(simulation, lines))
    unchanged, aloud = 0, 0
    for name in list(vars(simulation)):
        simulation.__dict__[f"renamed_{name.strip('_')}"] = simulation.__dict__.pop(name)
        try:
            after = module.digest_of(module.run_reading(simulation, lines))
        except AttributeError, KeyError, TypeError:
            aloud += 1
        else:
            assert after == before, f"renaming {name!r} moved the digest"
            unchanged += 1
        simulation.__dict__[name] = simulation.__dict__.pop(f"renamed_{name.strip('_')}")
    assert unchanged >= 10 and aloud >= 1
    assert module.digest_of(module.run_reading(simulation, lines)) == before
    reading = module.run_reading(simulation, lines)
    assert set(reading["held families"]) <= {family.name for family in simulation.families}
    assert all(key.isdigit() for key in reading["records"])
    keys = {"lines", "state", "records", "held families", "read remainders", "clicks", "books"}
    assert set(reading) == keys


def test_the_merge_replaces_the_named_worlds_and_keeps_the_rest(tmp_path, monkeypatch):
    """CI's merge on a tiny record: a world named by an uploaded entry takes it, a world named by none stays as recorded, and the commit is written."""
    module = recorder()
    kept = {"stamp": {"hash": "k" * 64}, "ticks": 9, "intervals": 9, "digest": "0" * 64}
    moved, added = {**kept, "digest": "2" * 64, "refused": "at the wall"}, {**kept, "intervals": 3}
    monkeypatch.setattr(module, "RECORD", tmp_path / "record.json")
    module.write_record({"a/kept.json": kept, "a/moved.json": {**kept, "digest": "1" * 64}}, "before")
    (tmp_path / "s" / "d").mkdir(parents=True)
    (tmp_path / "a__moved.record.json").write_text(json.dumps({"a/moved.json": moved}))
    (tmp_path / "s" / "d" / "b__added.record.json").write_text(json.dumps({"b/added.json": added}))
    assert module.merge(tmp_path, "abc1234") == ["a/moved.json", "b/added.json"]
    record = json.loads((tmp_path / "record.json").read_text())
    assert record["format"] == module.FORMAT and record["recorded_at"] == "abc1234"
    assert record["worlds"] == {"a/kept.json": kept, "a/moved.json": moved, "b/added.json": added}
