"""Tensor24's three files: the examples hold, each rule of the checker refuses its own broken file by name, its edge holds."""

import json
from pathlib import Path

import pytest

from tensor24.runner.files import COUPLING, NAMES, OPERANDS, departures

EXAMPLES = Path(__file__).resolve().parents[1] / "examples" / "tensor24"
DEN = 15162856759112389  # the example's den, as its file holds it: the widest of its integers, 54 bits


def edits():
    """One edited file per rule: the file, its one change (or its text), the departure named, or None at a rule's edge."""
    train = "universe.trains[0]"

    def coupling(named, **fields):
        row = dict(zip(COUPLING, [0] * (len(COUPLING) - 1) + [1], strict=True)) | fields
        return (
            "universe",
            lambda u: u["couplings"].append(list(row.values())),
            named and f"universe.couplings[0]: {named}",
        )

    def light(**fields):
        return lambda u: u["trains"][0].update(fields)

    def gear(row, named):
        return "setting", lambda s: s["gears"].append(row), named and f"setting.gears[1]: {named}"

    def at(name, *path, null=False):
        """The file's key at the path taken away, or given as null where a file may leave it out."""

        def edit(held):
            for key in path[:-1]:
                held = held[key]
            held.update({path[-1]: None}) if null else held.pop(path[-1])

        return name, edit

    whole = "a whole number of at least 1, not None"
    gone = {  # every key the format requires, each named where it stands when it is absent
        ("universe", "version"): "universe.version: 1, not None",
        ("universe", "integers"): "universe.integers: a mapping, not NoneType",
        ("universe", "trains"): "universe.trains: a list of one train or more",
        **{
            ("universe", "integers", k): f"universe.integers.{k}: {whole}"
            for k in ("den", "full_rate", "key")
        },
        ("universe", "trains", 0, "name"): f"{train}.name: a label, not None",
        ("universe", "trains", 0, "kinds"): f"{train}.kinds: a list of the kinds' labels, not None",
        ("universe", "trains", 0, "part"): f"{train}.part: {whole}",
        (
            "universe",
            "trains",
            0,
            "pinion",
        ): f"{train}.pinion: den, the seed's (masses are measured only in clicks), not None",
        ("piece", "version"): "piece.version: 1, not None",
        (
            "piece",
            "shape",
        ): "piece.shape: one side per axis, each a whole number of at least 1, not None",
        ("setting", "version"): "setting.version: 1, not None",
        ("setting", "ticks"): "setting.ticks: a whole number of at least 0, not None",
    }
    nulls = {  # a key a file may leave out is not left out by a null
        ("universe", "couplings"): "universe.couplings: a list of rows, not NoneType",
        ("setting", "gears"): "setting.gears: a list of rows, not NoneType",
    }
    return {
        **{f"no {'.'.join(map(str, path))}": (*at(*path), named) for path, named in gone.items()},
        **{
            f"a null {'.'.join(map(str, path))}": (*at(*path, null=True), named)
            for path, named in nulls.items()
        },
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
            f"universe.integers.den: the integer {DEN} takes more bits than the width, 8",
        ),
        "the width one bit short": (
            "universe",
            lambda u: u["integers"].update(width=53),
            f"universe.trains[0].pinion: the integer {DEN} takes more bits than the width, 53",
        ),
        "the width at the widest integer": ("universe", lambda u: u["integers"].update(width=54), None),
        "an integer too wide in the setting": (
            "setting",
            lambda s: s["gears"].append([0, 0, 1, 1 << 200, 0, 0]),
            f"setting.gears[1][3]: the integer {1 << 200} takes more bits than the width, 128",
        ),
        "a key off the format": (
            "universe",
            lambda u: u.update(colour=1),
            "universe: the key 'colour' is not",
        ),
        "a key off the format among the integers": (
            "universe",
            lambda u: u["integers"].update(colour=1),
            "universe.integers: the key 'colour' is not",
        ),
        "a key off the format in the piece": (
            "piece",
            lambda p: p.update(colour=1),
            "piece: the key 'colour' is not",
        ),
        "a key off the format in the setting": (
            "setting",
            lambda s: s.update(colour=1),
            "setting: the key 'colour' is not",
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
        "an empty label": (
            "universe",
            lambda u: u["trains"][0].update(name=""),
            f"{train}.name: a label, not ''",
        ),
        "two trains of one label": (
            "universe",
            lambda u: u["trains"].append(dict(u["trains"][0])),
            "universe.trains: the label 'light' names two trains or more",
        ),
        "two trains of one label that is no text": (
            "universe",
            lambda u: u["trains"].extend([dict(u["trains"][0], name=[7]) for _ in range(2)]),
            "universe.trains[2].name: a label, not [7]",
        ),
        "no kind": (
            "universe",
            lambda u: u["trains"][0].update(kinds=[]),
            f"{train}.kinds: a list of the kinds' labels",
        ),
        "a kind that is no text": (
            "universe",
            lambda u: u["trains"][0].update(kinds=[7]),
            f"{train}.kinds: a list of the kinds' labels, not [7]",
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
        "a pinion past den": (
            "universe",
            light(pinion=DEN + 1),
            f"{train}.pinion: den, the seed's (masses are measured only in clicks), not {DEN + 1}",
        ),
        "a pinion below den, a mass by hand": (
            "universe",
            light(pinion=DEN - 1),
            f"{train}.pinion: den, the seed's (masses are measured only in clicks), not {DEN - 1}",
        ),
        "a pinion of a list": (
            "universe",
            light(pinion=[DEN]),
            f"{train}.pinion: den, the seed's (masses are measured only in clicks), not [{DEN}]",
        ),
        "a sine, read by no act": (
            "universe",
            light(sine=0),
            f"{train}: the key 'sine' is not in the format",
        ),
        "a weight, read by no act": (
            "universe",
            light(weight=1),
            f"{train}: the key 'weight' is not in the format",
        ),
        "a trace, read by no act": (
            "universe",
            lambda u: u["integers"].update(trace=1),
            "universe.integers: the key 'trace' is not in the format",
        ),
        "a coupling to no train": coupling("a train off the trains' rows", with_train=1),
        "a coupling on the time gear": coupling("a train off the trains' rows", train=1),
        "a coupling's first train below 0": coupling("a train off the trains' rows", train=-1),
        "a coupling's second train below 0": coupling("a train off the trains' rows", with_train=-1),
        "a coupling's target beyond": coupling("a train off the trains' rows", target=1),
        "a coupling's target below 0": coupling("a train off the trains' rows", target=-1),
        "a coupling's strength that is a float": coupling(
            "a row of whole numbers, one per field", strength=0.5
        ),
        "a coupling's kind beyond": coupling("a kind off its train's", kind=1),
        "a coupling's kind below 0": coupling("a kind off its train's", kind=-1),
        "a coupling's second kind beyond": coupling("a kind off its train's", with_kind=1),
        "a coupling's target kind beyond": coupling("a kind off its train's", target_kind=1),
        "a coupling's target kind below 0": coupling("a kind off its train's", target_kind=-1),
        "a coupling's part beyond": coupling("a part off its train's", part=2),
        "a coupling's part below 0": coupling("a part off its train's", part=-1),
        "a coupling's second part beyond": coupling("a part off its train's", with_part=2),
        "a coupling's second part below 0": coupling("a part off its train's", with_part=-1),
        "a coupling's target part beyond": coupling("a part off its train's", target_part=2),
        "a coupling's target part below 0": coupling("a part off its train's", target_part=-1),
        "a coupling's operand beyond": coupling("an operand off the readings", operand=len(OPERANDS)),
        "a coupling's operand below 0": coupling("an operand off the readings", operand=-1),
        "a coupling's second operand beyond": coupling(
            "an operand off the readings", with_operand=len(OPERANDS)
        ),
        "a coupling's second operand below 0": coupling("an operand off the readings", with_operand=-1),
        "a coupling at the last parts and operands": coupling(
            None,
            part=1,
            with_part=1,
            target_part=1,
            operand=len(OPERANDS) - 1,
            with_operand=len(OPERANDS) - 1,
        ),
        "a side at 0": (
            "piece",
            lambda p: p["shape"].__setitem__(0, 0),
            "piece.shape: one side per axis",
        ),
        "a side that is a float": (
            "piece",
            lambda p: p["shape"].__setitem__(0, 4.0),
            "piece.shape: one side per axis, each a whole number of at least 1, not [4.0, 4, 4]",
        ),
        "two axes": ("piece", lambda p: p.update(shape=[4, 4]), "piece.shape: one side per axis"),
        "ticks below 0": (
            "setting",
            lambda s: s.update(ticks=-1),
            "setting.ticks: a whole number of at least 0",
        ),
        "ticks that are a float": (
            "setting",
            lambda s: s.update(ticks=1.5),
            "setting.ticks: a whole number of at least 0, not 1.5",
        ),
        "ticks at 0": ("setting", lambda s: s.update(ticks=0), None),
        "a gear off the board": gear([0, 0, 64, 1, 0, 0], "train 0 or site 64 off the files"),
        "a gear at the last site": gear([0, 0, 63, 1, 0, 0], None),
        "a gear's site below 0": gear([0, 0, -1, 1, 0, 0], "train 0 or site -1 off the files"),
        "a gear on the time gear": gear([1, 0, 0, 1, 0, 0], "train 1 or site 0 off the files"),
        "a gear's train below 0": gear([-1, 0, 1, 1, 0, 0], "train -1 or site 1 off the files"),
        "a gear's notch that is a float": gear(
            [0, 0, 1, 0.5, 0, 0], "a row of whole numbers, one per field"
        ),
        "a fine tooth below 0": gear([0, 0, 1, 1, 0, -1], "component 0 or fine tooth -1 below 0"),
        "a component below 0": gear([0, -1, 1, 1, 0, 0], "component -1 or fine tooth 0 below 0"),
        "a gear given twice": gear([0, 0, 0, 1, 1, 0], "the gear (0, 0, 0) given twice"),
        "a key doubled": (
            "piece",
            lambda p: '{"version": 1, "shape": [0, 4, 4], "shape": [4, 4, 4]}',
            "piece.json: not read: a key doubled",
        ),
        "a nesting too deep to read": (
            "piece",
            lambda p: "[" * 100000 + "]" * 100000,
            "piece.json: not read:",
        ),
        "no JSON": ("setting", lambda s: "{", "setting.json: not read:"),
        "a part of 1": ("universe", light(part=1), None),
        "an integer of 1": ("universe", lambda u: u["integers"].update(full_rate=1), None),
        "a side of 1": ("piece", lambda p: p["shape"].__setitem__(0, 1), None),
        "a coupling at the first parts": coupling(None),
        "a version 0": ("setting", lambda s: s.update(version=0), "setting.version: 1, not 0"),
        "four axes": ("piece", lambda p: p.update(shape=[4, 4, 4, 4]), "piece.shape: one side per axis"),
        "a gear row of seven": gear([0, 0, 1, 1, 0, 0, 0], "a row of whole numbers, one per field"),
        "a gear row of five": gear([0, 0, 1, 1, 0], "a row of whole numbers, one per field"),
        "a coupling row of a field more": (
            "universe",
            lambda u: u["couplings"].append([0] * (len(COUPLING) + 1)),
            "universe.couplings[0]: a row of whole numbers, one per field",
        ),
        "a coupling row of a field less": (
            "universe",
            lambda u: u["couplings"].append([0] * (len(COUPLING) - 1)),
            "universe.couplings[0]: a row of whole numbers, one per field",
        ),
    }


@pytest.mark.parametrize("rule", sorted(edits()))
def test_the_examples_hold_each_rule_refuses_its_own_broken_file_by_name_and_its_edge_holds(
    rule, tmp_path
):
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
    assert any(named in line for line in found) if named else found == [], found


def test_two_departures_of_one_file_are_each_named_once(tmp_path):
    paths = [EXAMPLES / f"{name}.json" for name in NAMES]
    held = json.loads(paths[0].read_text(encoding="utf-8"))
    held["version"], held["integers"]["key"] = 1 + 1, 0
    paths[0] = tmp_path / "universe.json"
    paths[0].write_text(json.dumps(held), encoding="utf-8")
    assert sorted(departures(*paths)) == [
        "universe.integers.key: a whole number of at least 1, not 0",
        "universe.version: 1, not 2",
    ]
