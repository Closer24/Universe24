"""The register's verification map carried through a regeneration
(`event_universe.register_map.carry_replicated`; docs/TEST_EXPECTATIONS.md,
"The register's verification map", the owner's rule of 2026-09-21, record
353). The expected results, written down first: (a) a register file
absent, or present without the map, leaves the regenerated register as it
is; (b) a file with the map gives the regenerated register that map,
equal entry by entry and detached from the file's object; (c) a block
regenerated with new numbers keeps its `replicated` entry beside the new
numbers, and an entry of a block the generator no longer writes is kept
too (the replicator's, never the generator's to drop); (d) the shipped
amplitude register equals its generator's output, the map included;
(e) a generator of another register (`two_stars/make_worlds.py`) writing
into a folder that holds a register with the map carries it, and into a
folder without one leaves the register as it is.
"""

from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path

import pytest

from event_universe.register_map import carry_replicated

ROOT = Path(__file__).resolve().parents[1]
AMPLITUDE = ROOT / "examples" / "events" / "amplitude"
TWO_STARS = ROOT / "examples" / "events" / "two_stars"


def test_an_absent_file_or_map_leaves_the_register_as_it_is(tmp_path: Path):
    """(a)."""
    register = {"format": "x-v1", "block": {"n": 1}, "derivations": {"block": "measured"}}
    assert carry_replicated(tmp_path / "missing.json", dict(register)) == register
    (tmp_path / "bare.json").write_text(json.dumps({"format": "x-v1", "block": {"n": 0}}))
    assert carry_replicated(tmp_path / "bare.json", dict(register)) == register


def test_a_file_with_the_map_gives_it_to_the_register(tmp_path: Path):
    """(b)."""
    on_disk = {
        "format": "x-v1",
        "block": {"n": 0},
        "replicated": {"block": "docs/REPLICATIONS.md#block"},
    }
    (tmp_path / "expectations.json").write_text(json.dumps(on_disk))
    register = carry_replicated(tmp_path / "expectations.json", {"format": "x-v1", "block": {"n": 1}})
    assert register["replicated"] == {"block": "docs/REPLICATIONS.md#block"}
    assert register["block"] == {"n": 1}


def test_a_regenerated_block_keeps_its_entry(tmp_path: Path):
    """(c)."""
    on_disk = {
        "format": "x-v1",
        "block": {"n": 0},
        "gone": {"n": 9},
        "replicated": {"block": "docs/REPLICATIONS.md#block", "gone": "docs/REPLICATIONS.md#gone"},
    }
    path = tmp_path / "expectations.json"
    path.write_text(json.dumps(on_disk))
    regenerated = carry_replicated(path, {"format": "x-v1", "block": {"n": 2}})
    assert regenerated == {
        "format": "x-v1",
        "block": {"n": 2},
        "replicated": {"block": "docs/REPLICATIONS.md#block", "gone": "docs/REPLICATIONS.md#gone"},
    }
    path.write_text(json.dumps(regenerated))
    assert json.loads(path.read_text())["replicated"]["block"] == "docs/REPLICATIONS.md#block"


def test_the_shipped_amplitude_register_is_the_generators_with_the_map():
    """(d)."""
    spec = importlib.util.spec_from_file_location("amplitude_make_worlds", AMPLITUDE / "make_worlds.py")
    module = importlib.util.module_from_spec(spec)
    sys.modules["amplitude_make_worlds"] = module
    spec.loader.exec_module(module)
    shipped = json.loads((AMPLITUDE / "expectations.json").read_text(encoding="utf-8"))
    generated = module.expectations()
    assert generated == shipped
    assert ("replicated" in generated) == ("replicated" in shipped)


def test_another_generator_carries_the_map_and_leaves_a_bare_register_as_it_is(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """(e)."""
    spec = importlib.util.spec_from_file_location("two_stars_make_worlds", TWO_STARS / "make_worlds.py")
    module = importlib.util.module_from_spec(spec)
    sys.modules["two_stars_make_worlds"] = module
    spec.loader.exec_module(module)
    monkeypatch.setattr(module, "HERE", tmp_path)
    monkeypatch.setattr(module, "ROOT", tmp_path)
    shipped = json.loads((TWO_STARS / "expectations.json").read_text(encoding="utf-8"))
    on_disk = dict(shipped)
    on_disk["replicated"] = {"worlds": "docs/REPLICATIONS.md#two-stars"}
    (tmp_path / "expectations.json").write_text(json.dumps(on_disk, indent=1) + "\n", encoding="utf-8")
    module.main()
    written = json.loads((tmp_path / "expectations.json").read_text(encoding="utf-8"))
    assert written["replicated"] == {"worlds": "docs/REPLICATIONS.md#two-stars"}
    assert {k: v for k, v in written.items() if k != "replicated"} == shipped
    (tmp_path / "expectations.json").unlink()
    module.main()
    assert json.loads((tmp_path / "expectations.json").read_text(encoding="utf-8")) == shipped
