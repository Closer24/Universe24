"""Tensor24's half-speed trains in the runner: the files' eight kinds and the two trains they admit, refused in a file run."""

import json
import subprocess
import sys
from pathlib import Path

from tensor24 import main
from tensor24.runner import load as loading
from tensor24.runner.files import NAMES, entries, held_departures, star, vocabulary

ROOT = Path(__file__).resolve().parents[1]
PATHS = [ROOT / "examples" / "tensor24" / f"{name}.json" for name in NAMES]
AXES = len(json.loads(PATHS[1].read_text(encoding="utf-8"))["shape"])  # the piece's board
MADE = main.made(star(AXES))
COSETS, CLASSES = (
    (["G3/2"], 2),
    (["E1/2", "E5/2", "G3/2", "G3/2"], 2),
)  # the two half-speed trains: kinds, part
UNIT = "no family couples a half-speed train in this build"
CLICKS = [  # the click world's clocks: a scalar clock at part 2, the square, the held hand and two tied hands
    {"name": "scalar", "kinds": ["A1"], "part": 2},
    {"name": "metric", "kinds": ["A1", "T1", "A1", "E", "T2"], "part": 1},
    {"name": "held", "kinds": ["A1", "A2"], "part": 1},
    {"name": "giver", "kinds": ["T1", "T2"], "part": 1},
    {"name": "taker", "kinds": ["T1", "T2"], "part": 1},
]


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


def test_a_half_speed_train_is_no_square_nor_held_untied_gripped_and_driven_on_the_force_path():
    """Yes: each half-speed train beside the click world's clocks no square, not the held hand, untied, gripped, its rows its
    gears, its drive's teeth 1 (the force's path); the click world's clocks read as they were.
    No: the twist keeps both trains' characters, so they are untied by their speed; a mix wrapping onto the held hand's is no hand."""
    labels, dims, reads = vocabulary(MADE[0], *MADE[-2:])
    lifts, spins = reads[-1], [{"name": "spin", "kinds": k, "part": p} for k, p in (COSETS, CLASSES)]
    trains = loading.trains_of(*entries([*CLICKS, *spins], labels), dims, reads)
    flags = [getattr(trains, flag).tolist() for flag in ("square", "held", "tied", "gripped", "half")]
    assert flags == [
        [0, 1, 0, 0, 0, 0, 0],
        [0, 0, 1, 0, 0, 0, 0],
        [0, 0, 0, 1, 1, 0, 0],
        [1, 1, 0, 1, 1, 1, 1],
        [0, 0, 0, 0, 0, 1, 1],
    ]
    assert trains.size[-len(spins) :].tolist() == list(lifts.gears)  # each one's rows its gears
    universe = json.loads(PATHS[0].read_text(encoding="utf-8"))
    (*_, drive, _), *_ = loading.geared(universe, trains, star(AXES))
    spun = range(trains.first[-len(spins)], trains.size.sum())
    assert set(drive[list(spun), 0].tolist()) == {1}  # T_d = 1 on the half-speed rows
    a2 = lifts.characters[labels.index("A2"), ..., :1]  # the sign kind's character on the 48
    for kinds, part in (COSETS, CLASSES):
        character = part * lifts.characters[[labels.index(k) for k in kinds]].sum(axis=0)
        assert (character * a2 == character).all()  # kept under the twist
    (hand,) = loading.trains_of(
        *entries([{"name": "x", "kinds": ["E1/2", "E5/2"], "part": 1}], labels), dims, reads
    ).held
    assert hand == 0  # its kinds wrap onto A1 and A2, at the factor 0


def test_a_half_speed_trains_rows_are_its_cosets_each_gear_on_its_cosets_row():
    """Yes: a gear at each component of each half-speed train laid on its coset's row, the train's first and that index, the
    last coset's within the train's rows and every other train's rows untouched.
    No: a component one past the last coset is refused by name, off the train's rows, and laid nowhere."""
    labels, dims, reads = vocabulary(MADE[0], *MADE[-2:])
    spins = [{"name": f"spin {n}", "kinds": k, "part": p} for n, (k, p) in enumerate((COSETS, CLASSES))]
    trains, sites = loading.trains_of(*entries([*CLICKS, *spins], labels), dims, reads), 1
    for t, gears in zip(range(len(CLICKS), len(CLICKS) + len(spins)), reads[-1].gears, strict=True):
        laid = [
            [t, c, 0, c + 1, -c - 1, 0] for c in range(gears)
        ]  # each coset's gear, its counts its index's
        (a, b, *_), found = loading.lay(laid, trains, sites, 0)
        rows = range(trains.first[t], trains.first[t] + gears)
        assert found == [] and a[list(rows), 0].tolist() == [c + 1 for c in range(gears)]
        assert not a.sum() - a[list(rows)].sum() and (b[list(rows), 0] == -a[list(rows), 0]).all()
        universe = {"trains": [*CLICKS, *spins]}
        (line,) = held_departures(universe, {"gears": [[t, gears, 0, 0, 0, 0]]}, (labels, dims, reads))[
            -1:
        ]
        assert line == f"setting.gears[0]: component {gears} off train {t}'s {gears} rows"
