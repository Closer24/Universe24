"""EVERY SHIPPED WORLD BIT FOR BIT (the model owner's short procedure, record 2214 point 7: "the
most important test: with the new feature off, all the old runs come out identical to the bit";
the Boss's records 2216 (2) and 2230; issue #1155). `tests/shipped_worlds.json` holds, for every
world file under examples/events/ that the engine loads, the stamp of its file, the number of
intervals recorded and the SHA-256 digest of the engine's whole state after them, written by
`tools/record_shipped_worlds.py`. This test replays exactly those intervals and compares the
digest; it is selected by `tools/check.py` on every pull request, whatever the change. A moved
digest is a changed run: the change re-records it on purpose, in the same commit, with the reason
in the commit's message. HOST readings only; nothing here is a measurement."""

from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
RECORD = ROOT / "tests" / "shipped_worlds.json"


def recorder():  # type: ignore[no-untyped-def]
    spec = importlib.util.spec_from_file_location(
        "record_shipped_worlds", ROOT / "tools" / "record_shipped_worlds.py"
    )
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    sys.modules["record_shipped_worlds"] = module
    spec.loader.exec_module(module)
    return module


RECORDED = json.loads(RECORD.read_text(encoding="utf-8"))
WORLDS = sorted(RECORDED["worlds"])


def test_the_record_names_every_shipped_world_and_nothing_else():
    module = recorder()
    shipped = sorted(path.relative_to(ROOT).as_posix() for path in module.shipped_worlds())
    assert shipped == WORLDS, "a world was added or removed: record it (tools/record_shipped_worlds.py)"
    assert RECORDED["format"] == module.FORMAT
    for entry in RECORDED["worlds"].values():
        assert 1 <= entry["intervals"] <= entry["ticks"]
        assert len(entry["digest"]) == 64


@pytest.mark.parametrize("world", WORLDS)
def test_a_shipped_world_runs_bit_for_bit_as_recorded(world: str):
    module = recorder()
    expected = RECORDED["worlds"][world]
    actual = module.run(ROOT / world, expected["intervals"])
    assert actual["stamp"] == expected["stamp"], f"{world}: the world file changed; re-record it"
    assert actual["digest"] == expected["digest"], (
        f"{world}: the run moved after {expected['intervals']} intervals "
        f"(records {expected['records']} -> {actual['records']}, clicks {expected['clicks']} -> "
        f"{actual['clicks']}, lines {expected['lines']} -> {actual['lines']}); "
        "an intended change re-records it in the same commit"
    )


def test_the_digest_does_not_move_under_a_rename_of_the_engines_attributes():
    """The digest is of what the run is, never of how the code holds it (the Boss's word on
    PR #1172): for every attribute of the engine object, renaming it either leaves the digest
    where it is (the reading does not name it) or breaks the reader aloud (the reading or the
    engine's own state stream reads it by that name, and follows a rename by hand); it never
    moves the digest. The keys of the reading are the world's family names, the records'
    identities and the ledger's words, never an attribute's name."""
    import json

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
    assert set(reading) == {
        "lines",
        "state",
        "records",
        "held families",
        "read remainders",
        "clicks",
        "books",
    }
