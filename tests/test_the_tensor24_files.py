"""Tensor24's three files: the examples hold, and each rule of the checker refuses its own broken file by name."""

import json
from pathlib import Path

import pytest

from tensor24.runner.files import departures

EXAMPLES = Path(__file__).resolve().parents[1] / "examples" / "tensor24"
NAMES = ("universe", "piece", "setting")
DEN = 15162856759112389  # the example's den, as its file holds it


def edits():
    """One broken file per rule: the file, its one change (or its text), and the departure the checker must name."""
    train = "universe.trains[0]"
    return {
        "a version that is a float": (
            "universe",
            lambda u: u.update(version=1.0),
            "universe.version: 1, not 1.0",
        ),
        "a version that is a truth value": (
            "piece",
            lambda p: p.update(version=True),
            "piece.version: 1, not True",
        ),
        "another version": ("setting", lambda s: s.update(version=2), "setting.version: 1, not 2"),
        "a float of at least 1": (
            "universe",
            lambda u: u["integers"].update(den=2.5),
            "universe.integers.den: a whole number of at least 1, not 2.5",
        ),
        "an integer at 0": (
            "universe",
            lambda u: u["integers"].update(full_rate=0),
            "universe.integers.full_rate: a whole number of at least 1, not 0",
        ),
        "no width": (
            "universe",
            lambda u: u["integers"].pop("width"),
            "universe.integers.width: a whole number of at least 1, not None",
        ),
        "an integer past the width": (
            "universe",
            lambda u: u["integers"].update(width=8),
            f"the integer {DEN} takes more bits than the width, 8",
        ),
        "a key off the format": (
            "universe",
            lambda u: u.update(colour=1),
            "universe: the key 'colour' is not",
        ),
        "a train's key off the format": (
            "universe",
            lambda u: u["trains"][0].update(colour=1),
            f"{train}: the key",
        ),
        "no train": (
            "universe",
            lambda u: u.update(trains=[]),
            "universe.trains: a list of one train or more",
        ),
        "a label that is no text": (
            "universe",
            lambda u: u["trains"][0].update(name=7),
            f"{train}.name: a label, not 7",
        ),
        "two trains of one label": (
            "universe",
            lambda u: u["trains"].append(dict(u["trains"][0])),
            "universe.trains: the label 'light' names two trains or more",
        ),
        "no kind": (
            "universe",
            lambda u: u["trains"][0].update(kinds=[]),
            f"{train}.kinds: a list of the kinds' labels",
        ),
        "a part at 0": (
            "universe",
            lambda u: u["trains"][0].update(part=0),
            f"{train}.part: a whole number of at least 1",
        ),
        "a part that is a truth value": (
            "universe",
            lambda u: u["trains"][0].update(part=True),
            f"{train}.part: a whole number of at least 1, not True",
        ),
        "a rim that is not den": (
            "universe",
            lambda u: u["trains"][0].update(pair=[DEN, DEN + 1]),
            f"{train}.pair: the rim is den, not {DEN + 1}",
        ),
        "a pinion past the rim": (
            "universe",
            lambda u: u["trains"][0].update(pair=[DEN + 1, DEN]),
            f"{train}.pair: the pinion within [0, den], not {DEN + 1}",
        ),
        "a weight that is a float": (
            "universe",
            lambda u: u["trains"][0].update(weight=0.5),
            f"{train}.weight: a whole number, not 0.5",
        ),
        "a coupling to no train": (
            "universe",
            lambda u: u["couplings"].append([0, 0, 1, 0, 0, 1]),
            "universe.couplings[0]: a train beyond the trains' rows",
        ),
        "a coupling's first train beyond": (
            "universe",
            lambda u: u["couplings"].append([1, 0, 0, 0, 0, 1]),
            "universe.couplings[0]: a train beyond the trains' rows",
        ),
        "a coupling's strength that is a float": (
            "universe",
            lambda u: u["couplings"].append([0, 0, 0, 0, 0, 0.5]),
            "universe.couplings[0]: a row of whole numbers, one per field",
        ),
        "a coupling's target beyond": (
            "universe",
            lambda u: u["couplings"].append([0, 0, 0, 0, 1, 1]),
            "universe.couplings[0]: a train beyond the trains' rows",
        ),
        "a coupling's part beyond": (
            "universe",
            lambda u: u["couplings"].append([0, 2, 0, 0, 0, 1]),
            "universe.couplings[0]: a part beyond its train's",
        ),
        "a side at 0": (
            "piece",
            lambda p: p["shape"].__setitem__(0, 0),
            "piece.shape: one side per axis",
        ),
        "two axes": ("piece", lambda p: p.update(shape=[4, 4]), "piece.shape: one side per axis"),
        "ticks below 0": (
            "setting",
            lambda s: s.update(ticks=-1),
            "setting.ticks: a whole number of at least 0",
        ),
        "a gear off the board": (
            "setting",
            lambda s: s["gears"].append([0, 0, 64, 1, 0, 0]),
            "setting.gears[1]: train 0 or site 64 off the files",
        ),
        "a gear's notch that is a float": (
            "setting",
            lambda s: s["gears"].append([0, 0, 1, 0.5, 0, 0]),
            "setting.gears[1]: a row of whole numbers, one per field",
        ),
        "a gear on no train": (
            "setting",
            lambda s: s["gears"].append([1, 0, 0, 1, 0, 0]),
            "setting.gears[1]: train 1 or site 0 off the files",
        ),
        "a fine tooth below 0": (
            "setting",
            lambda s: s["gears"].append([0, 0, 1, 1, 0, -1]),
            "setting.gears[1]: component 0 or fine tooth -1 below 0",
        ),
        "a gear given twice": (
            "setting",
            lambda s: s["gears"].append([0, 0, 0, 1, 1, 0]),
            "setting.gears[1]: the gear (0, 0, 0) given twice",
        ),
        "a key doubled": (
            "piece",
            lambda p: '{"version": 1, "shape": [0, 4, 4], "shape": [4, 4, 4]}',
            "piece.json: not read: a key doubled",
        ),
        "no JSON": ("setting", lambda s: "{", "setting.json: not read:"),
    }


@pytest.mark.parametrize("rule", sorted(edits()))
def test_the_examples_hold_and_each_rule_refuses_its_own_broken_file_by_name(rule, tmp_path):
    paths = [EXAMPLES / f"{name}.json" for name in NAMES]
    assert departures(*paths) == []
    name, edit, named = edits()[rule]
    held = json.loads(paths[NAMES.index(name)].read_text(encoding="utf-8"))
    text = edit(held)
    paths[NAMES.index(name)] = tmp_path / f"{name}.json"
    paths[NAMES.index(name)].write_text(
        text if isinstance(text, str) else json.dumps(held), encoding="utf-8"
    )
    found = departures(*paths)
    assert any(named in line for line in found), found
