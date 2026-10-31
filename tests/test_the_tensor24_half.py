"""Tensor24's half-speed trains in the runner: the files' eight kinds and the two trains they admit, refused in a file run."""

import json
import subprocess
import sys
from pathlib import Path

from tensor24 import main
from tensor24.runner.files import NAMES, held_departures, star, vocabulary

ROOT = Path(__file__).resolve().parents[1]
PATHS = [ROOT / "examples" / "tensor24" / f"{name}.json" for name in NAMES]
MADE = main.made(star(len(json.loads(PATHS[1].read_text(encoding="utf-8"))["shape"])))
COSETS, CLASSES = (
    (["G3/2"], 2),
    (["E1/2", "E5/2", "G3/2", "G3/2"], 2),
)  # the two half-speed trains: kinds, part
UNIT = "no family couples a half-speed train in this build"


def held(kinds, part):
    """A universe of one train of these kinds and part, held against the engine's eight kinds: its departures."""
    universe = {"trains": [{"name": "spin", "kinds": kinds, "part": part}]}
    return held_departures(universe, {"gears": []}, vocabulary(MADE[0], *MADE[-2:]))


def test_the_files_admit_the_two_half_speed_trains_alone_and_refuse_both_in_a_file_run(tmp_path):
    """Yes: eight labels, the three half-speed ones E1/2, E5/2, G3/2, the dimensions' squares summing to the 48; the 8-gear and
    24-gear trains admitted in any order of their kinds, then refused by name in a file run, by the run (nothing written) and the files tool.
    No: every other mix of a half-speed kind refused by name: with an r2 part, not -I on the full turn, neither train's."""
    labels, dims, read = vocabulary(MADE[0], *MADE[-2:])
    lifts = read[-1]
    assert labels[-len(lifts.dims) :] == ("E1/2", "E5/2", "G3/2")
    one = lifts.characters[:, 0, 0, 0]  # every kind's character at the lift 1, the + sense's first word
    senses, classes = MADE[-1].lift.shape[:2]
    assert list(dims) == one.tolist() and sum(d * d for d in dims) == senses * classes  # the 48
    rows = [part * sum(dims[labels.index(k)] for k in kinds) for kinds, part in (COSETS, CLASSES)]
    assert rows == list(lifts.gears)  # each train's rows its gears
    for kinds, part in (COSETS, CLASSES, (CLASSES[0][::-1], CLASSES[1])):
        assert held(kinds, part) == [f"universe.trains[0].kinds: {kinds} at part {part}: {UNIT}"]
    for kinds, part, reasons in (
        (["E1/2"], 1, "has an r2 part, is neither train's"),
        (["T1", "G3/2"], 1, "is not -I on the full turn, is neither train's"),
        (["G3/2"], 1, "is neither train's"),
        (["G3/2"], 4, "is neither train's"),
        (["E1/2", "E5/2"], 1, "is neither train's"),
    ):
        (line,) = held(kinds, part)
        assert line.endswith(f"this character {reasons}") and ": no half-speed train: " in line, line
    # the square's kinds with a half-speed kind are no square: E then has no whole basis there
    lines = held(["A1", "T1", "A1", "E", "T2", "G3/2"], 1)
    assert [": no half-speed train: " in x for x in lines] == [
        False,
        True,
    ] and "no whole basis" in lines[0]
    universe = json.loads(PATHS[0].read_text(encoding="utf-8"))
    (kinds, part), den = COSETS, universe["integers"]["den"]  # the pinion den, the seed's
    universe["trains"].append({"name": "spin", "kinds": kinds, "part": part, "pinion": den})
    paths, record = [tmp_path / "universe.json", *PATHS[1:]], tmp_path / "spin.jsonl"
    paths[0].write_text(json.dumps(universe), encoding="utf-8")
    at = len(universe["trains"]) - 1
    assert main.ran(paths, record) == [f"universe.trains[{at}].kinds: {kinds} at part {part}: {UNIT}"]
    assert not record.exists()
    tool = [sys.executable, "-I", str(ROOT / "tools" / "tensor24_files.py"), *map(str, paths)]
    done = subprocess.run(tool, capture_output=True, text=True)
    assert done.returncode == 1 and UNIT in done.stdout, done.stdout + done.stderr
