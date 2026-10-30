"""Tensor24's three files and their one generic checker: the examples hold, each rule refuses its own broken file by
name, its edge holds, and the tool."""

import json
import subprocess
import sys
from pathlib import Path

from tensor24.runner.files import NAMES, departures

EXAMPLES = Path(__file__).resolve().parents[1] / "examples" / "tensor24"
DEN = 15162856759112389  # the example's den, as its file holds it: the widest of its integers, 54 bits


def edits():
    """One edited file per rule: the file, its one change (or its text), the departure named, or None at a rule's edge."""
    train = "universe.trains[0]"

    light = lambda **fields: lambda u: u["trains"][0].update(fields)  # noqa: E731

    def gear(row, named):
        return "setting", lambda s: s["gears"].append(row), named and f"setting.gears[1]: {named}"

    def at(name, *path, null=False):
        """The file's key at the path taken away, or given as null where a file may leave it out."""

        def edit(held):
            for key in path[:-1]:
                held = held[key]
            held.update({path[-1]: None}) if null else held.pop(path[-1])

        return name, edit

    whole, low = "a whole number of at least 1, not None", "a whole number of at least 0, not None"
    gone = {  # every key the format requires, each named where it stands when it is absent
        ("universe", "version"): "universe.version: 1, not None",
        ("universe", "integers"): "universe.integers: a mapping, not NoneType",
        ("universe", "trains"): "universe.trains: a list of one train or more",
        ("universe", "chosen"): "universe.chosen: a mapping, not NoneType",
        ("universe", "chosen", "key"): "universe.chosen.key: an odd whole number",
        ("universe", "chosen", "push"): "universe.chosen.push: 0 or 1",
        **{("universe", "chosen", k): f"chosen.{k}: {low}" for k in "notch hold tie mesh".split()},
        **{("universe", "integers", k): f"universe.integers.{k}: {whole}" for k in ("den", "full_rate")},
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
        ("setting", "ticks"): f"setting.ticks: {low}",
    }
    nulls = {("setting", "gears"): "setting.gears: a list of rows, not NoneType"}  # left out, not null
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
        "a push of 2": ("universe", lambda u: u["chosen"].update(push=2), "chosen.push: 0 or 1"),
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
            light(pinion=-1),
            f"{train}.pinion: den, the seed's (masses are measured only in clicks), not -1",
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
        "a key, read by no act": (
            "universe",
            lambda u: u["integers"].update(key=1),
            "universe.integers: the key 'key' is not in the format",
        ),
        "couplings, which no file declares": (
            "universe",
            lambda u: u.update(couplings=[]),
            "universe: the key 'couplings' is not in the format: no file declares a coupling",
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
        "a gear on a train past the file's": gear([2, 0, 0, 1, 0, 0], "train 2 or site 0 off the files"),
        "a gear's train below 0": gear([-1, 0, 1, 1, 0, 0], "train -1 or site 1 off the files"),
        "a gear's notch that is a float": gear(
            [0, 0, 1, 0.5, 0, 0], "a row of whole numbers, one per field"
        ),
        "a fine tooth below 0 holds, the edge's dial the run's promise": gear([0, 0, 1, 1, 0, -1], None),
        "a component below 0": gear([0, -1, 1, 1, 0, 0], "component -1 below 0"),
        "a gear given twice": gear([0, 0, 0, 1, 1, 0], "the gear (0, 0, 0) given twice"),
        "a key doubled": (
            "piece",
            lambda p: '{"version": 1, "shape": [0, 4, 4], "shape": [4, 4, 4]}',
            "piece.json: not read: a key doubled",
        ),
        "a nesting too deep to read": (
            "piece",
            # ten million deep, past any stack: 3.14.9 on CI reads a hundred thousand, 3.14.6 about forty thousand
            lambda p: "[" * 10**7 + "]" * 10**7,
            "piece.json: not read:",
        ),
        "no JSON": ("setting", lambda s: "{", "setting.json: not read:"),
        "a part of 1": ("universe", light(part=1), None),
        "an integer of 1": ("universe", lambda u: u["integers"].update(full_rate=1), None),
        "a side of 1": ("piece", lambda p: p["shape"].__setitem__(0, 1), None),
        "a version 0": ("setting", lambda s: s.update(version=0), "setting.version: 1, not 0"),
        "four axes": ("piece", lambda p: p.update(shape=[4, 4, 4, 4]), "piece.shape: one side per axis"),
        "a gear row of seven": gear([0, 0, 1, 1, 0, 0, 0], "a row of whole numbers, one per field"),
        "a gear row of five": gear([0, 0, 1, 1, 0], "a row of whole numbers, one per field"),
    }


def found(tmp_path, name, edit):
    """The departures of the three examples with one file edited, or its text given whole."""
    paths = [EXAMPLES / f"{n}.json" for n in NAMES]
    held = json.loads(paths[NAMES.index(name)].read_text(encoding="utf-8"))
    text = edit(held)
    tmp_path.mkdir(parents=True)
    paths[NAMES.index(name)] = tmp_path / f"{name}.json"
    paths[NAMES.index(name)].write_text(
        text if isinstance(text, str) else json.dumps(held), encoding="utf-8"
    )
    return departures(*paths)


def test_the_examples_hold_each_rule_refuses_its_own_broken_file_by_name_and_its_edge_holds(tmp_path):
    """Every rule of the one checker's format, two departures of one file each named once, and the tool: every example
    folder's three files hold, and the examples load, exit 0; given one file, argparse's usage error, exit 2."""
    assert not any(departures(*(f / f"{n}.json" for n in NAMES)) for f in EXAMPLES.parent.glob("*/"))
    for i, (rule, (name, edit, named)) in enumerate(sorted(edits().items())):
        lines = found(tmp_path / str(i), name, edit)
        assert any(named in line for line in lines) if named else lines == [], (rule, lines)

    def two(held):
        held["version"], held["integers"]["full_rate"] = 1 + 1, 0

    assert sorted(found(tmp_path / "two", "universe", two)) == [
        "universe.integers.full_rate: a whole number of at least 1, not 0",
        "universe.version: 1, not 2",
    ]
    tool = Path(__file__).resolve().parents[1] / "tools" / "tensor24_files.py"
    held, one = (
        subprocess.run([sys.executable, "-I", str(tool), *argv], capture_output=True, text=True)
        for argv in ([], ["universe.json"])
    )
    assert held.returncode == 0 and held.stdout.startswith("the three files hold and load"), held.stderr
    assert one.returncode == 1 + 1 and "the three files, or none for the examples" in one.stderr
