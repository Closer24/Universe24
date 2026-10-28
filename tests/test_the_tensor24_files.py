"""Tensor24's three files: the examples hold, and each rule of the checker refuses its own broken file."""

import json
from pathlib import Path

import pytest

from tensor24.runner.files import departures


def edits():
    """One broken file per rule, each a single change the checker must refuse."""
    return {
        "a float": ("universe", lambda u: u["integers"].update(den=0.5)),
        "a divisor at 0": ("universe", lambda u: u["integers"].update(full_rate=0)),
        "a truth value": ("universe", lambda u: u["trains"][0].update(part=True)),
        "a key off the format": ("universe", lambda u: u.update(colour=1)),
        "a rim that is not den": ("universe", lambda u: u["trains"][0]["pair"].__setitem__(1, 7)),
        "a coupling to no train": ("universe", lambda u: u["couplings"].append([0, 0, 1, 0, 0, 1])),
        "a side at 0": ("piece", lambda p: p["shape"].__setitem__(0, 0)),
        "a gear off the board": ("setting", lambda s: s["gears"].append([0, 0, 64, 1, 0, 0])),
        "another version": ("setting", lambda s: s.update(version=2)),
    }


@pytest.mark.parametrize("rule", sorted(edits()))
def test_the_examples_hold_and_each_rule_refuses_its_broken_file(rule, tmp_path):
    names, (name, edit) = ("universe", "piece", "setting"), edits()[rule]
    paths = [Path(__file__).resolve().parents[1] / "examples" / "tensor24" / f"{n}.json" for n in names]
    assert departures(*paths) == []
    held = json.loads(paths[names.index(name)].read_text(encoding="utf-8"))
    edit(held)
    paths[names.index(name)] = tmp_path / f"{name}.json"
    paths[names.index(name)].write_text(json.dumps(held), encoding="utf-8")
    assert departures(*paths)
