"""Tensor24's half-speed trains in the runner: the files' eight kinds and the two trains they admit, refused in a file run;
the load's reading of them, their rows their cosets, and a test world in memory turned by the lifts and the board's turns."""

import json
import subprocess
import sys
from pathlib import Path

import numpy as np

from tensor24 import main
from tensor24.engine import kinds as engine
from tensor24.engine import state, step
from tensor24.runner import load as loading
from tensor24.runner.files import NAMES, entries, held_departures, sites_of, star, vocabulary
from tests import frame

ROOT = Path(__file__).resolve().parents[1]
PATHS = [ROOT / "examples" / "tensor24" / f"{name}.json" for name in NAMES]
AXES = len(json.loads(PATHS[1].read_text(encoding="utf-8"))["shape"])  # the piece's board
MADE = main.made(star(AXES))
COSETS, CLASSES = (
    (["G3/2"], 2),
    (["E1/2", "E5/2", "G3/2", "G3/2"], 2),
)  # the two half-speed trains: kinds, part
UNIT = "no family couples a half-speed train in this build"
ROUNDS = 2  # the rounds a world in memory runs
LIFTS = MADE[-1].lift[..., 0, 0].size  # the 48
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


def laid(trains, chosen, integers=None, shape=(2, 1, 1)):
    """A test world in memory, laid through load.load as the run lays it, at the example universe's integers or others."""
    universe = json.loads(PATHS[0].read_text(encoding="utf-8"))
    integers = {**universe["integers"], **(integers or {})}
    universe = {
        **universe,
        "integers": integers,
        "trains": trains,
        "chosen": {**universe["chosen"], **chosen},
    }
    held, found = loading.load(universe, {"gears": []}, sites_of(list(shape)), *MADE)
    assert found == []
    return held, main.layout(universe, list(shape), held)


def drawn(held, layout, seed, reach):
    """A state on the layout, every gear below reach either side of 0 but the square's 00 slot, at 0 or past it below
    2**40, each tooth within its dial."""
    rng, rows, n = np.random.default_rng(seed), layout.gearing.rest.shape[0], layout.nb.shape[1]
    a, b = (frame.wide(rng, (rows, n)) % (reach + reach) - reach for _ in "ab")
    (clock,) = [t.first for t in held.trains if t.square]
    a[clock], b[clock] = (rng.integers(0, 1 << 40, n).astype(object) * (reach > 1 << 40) for _ in "ab")
    d = step.weight(layout.gearing, layout.clock, a) + step.weight(layout.gearing, layout.clock, b)
    return state.State(a, b, frame.wide(rng, (rows, n)) % (d + d) - d, 0 * a, 0 * a[: len(held.trains)])


def ran(layout, s, rounds):
    """The state the act reaches in so many rounds, and how many teeth moved on the way."""
    moved = 0
    for _ in range(rounds):
        out, _ = step.act(layout, s)
        moved, s = moved + int((out.r != s.r).sum()), out
    return s, moved


def turned(s, lifts, trains, flip=True):
    """The state turned by one lift on each half-speed train's rows, its own L(g), every other row kept: a negated gear's
    tooth flipped on its dial, -1 - s, as the mirror flips it (or, with flip off, negated: the no)."""
    turn = np.eye(len(s.a), dtype=object)
    for t, m in zip(trains, lifts, strict=True):
        turn[t.first : t.first + t.rows(), t.first : t.first + t.rows()] = m
    tooth = (turn @ (s.r + s.r + 1) - 1) // 2 if flip else turn @ s.r
    return state.State(turn @ s.a, turn @ s.b, tooth, s.rd, s.k)


def turning(layout, start, end, halves, flip=True):
    """How many of the 48 lifts turn the run alike: the turned start run to the end turned, each train by its own L(g)."""
    lifts, alike = MADE[-1], 0
    for g in zip(*(x.reshape(-1, *x.shape[-2:]) for x in (lifts.cosets, lifts.classes)), strict=True):
        moved, _ = ran(layout, turned(start, g, halves, flip), ROUNDS)
        alike += frame.same(moved, turned(end, g, halves, flip))
    return alike


def test_a_half_speed_world_laid_in_memory_turns_with_its_48_lifts_runs_back_and_pairs_by_the_dot():
    """Yes: the two half-speed trains beside the square, the push on, at the rest 6 den Gamma^2 and at 6: every lift turns the
    run (the teeth rounding), the run back exact; each passing pair a half-speed row with itself at 1; no gradient term on one.
    No: at the rest 6 a gear negated with its tooth negated and not flipped, the turned run and the run turned part."""
    spins = [{"name": f"spin {n}", "kinds": k, "part": p} for n, (k, p) in enumerate((COSETS, CLASSES))]
    for integers, reach in ((None, 1 << 300), ({"den": 1, "full_rate": 1}, 1 << 8)):
        held, layout = laid([CLICKS[1], *spins], {"push": 1}, integers)
        halves, start = [held.trains[n] for n in (1, 2)], drawn(held, layout, 7, reach)
        end, moved = ran(layout, start, ROUNDS)
        back = end
        for _ in range(ROUNDS):
            back = step.untick(layout, back)
        assert moved and turning(layout, start, end, halves) == LIFTS and frame.same(back, start)
        # the no, at the rest 6: a negated gear's tooth negated, not flipped
        assert integers is None or turning(layout, start, end, halves, False) < LIFTS
    one, two, entry, train, _ = held.click
    rows = {r for t in halves for r in range(t.first, t.first + t.rows())}
    pairs = {
        (int(x), int(y)): int(e) for x, y, e in zip(one, two, entry, strict=True) if e and int(x) in rows
    }
    assert pairs == {(r, r): 1 for r in rows}  # each half-speed row with itself, the dot
    held, layout = laid([CLICKS[0], CLICKS[3], *spins], {"mesh": 3})
    reads, *_, factor, target = held.mesh
    landed = {int(r) for r in target[factor != 0]} | {
        int(r) % len(held.state[0]) for r in reads[factor != 0]
    }
    halves = [held.trains[n] for n in (2, 3)]
    assert factor.any() and not landed & {r for t in halves for r in range(t.first, t.first + t.rows())}


def boarded(s, held, g, shape, flip=True):
    """The state turned by the lift g: the sites by its own turn, the square's slots by that turn's square, each half-speed
    train's gears by its own L(g), a negated gear's tooth flipped, -1 - s (or, with flip off, negated: the no)."""
    lifts = MADE[-1]
    m = lifts.turn.reshape(-1, AXES, AXES)[g]
    xyz, sides = np.indices(shape).reshape(AXES, -1), np.array(shape)[:, None]
    site = np.ravel_multi_index(tuple(((m @ xyz) % sides).astype(int)), shape)
    (square,) = [n for n in range(len(held.trains)) if held.trains[n].square]
    blocks = [(square, engine.square(engine.kinds(m[None]))[0])]
    blocks += [(n, x.reshape(-1, *x.shape[-2:])[g]) for n, x in ((1, lifts.cosets), (2, lifts.classes))]
    turn = np.eye(len(s.a), dtype=object)
    for n, block in blocks:
        first, rows = held.trains[n].first, held.trains[n].rows()
        turn[first : first + rows, first : first + rows] = block
    tooth = (turn @ (s.r + s.r + 1) - 1) // 2 if flip else turn @ s.r
    there = [np.empty_like(x) for x in s]
    for x, y in zip(there, (turn @ s.a, turn @ s.b, tooth, (turn * turn) @ s.rd, s.k), strict=True):
        x[:, site] = y
    return state.State(*there)


def board_turnings(layout, held, start, end, shape, flip=True):
    """For each of the 48 lifts, each with its own turn on the sites, whether it turns the run of a round alike."""
    for g in range(LIFTS):
        moved, _ = ran(layout, boarded(start, held, g, shape, flip), 1)
        yield frame.same(moved, boarded(end, held, g, shape, flip))


def test_the_board_with_its_sites_turned_by_each_lifts_own_turn_turns_the_run_alike():
    """Yes: on a cube of 2 x 2 x 2 sites, both half-speed trains beside the square, the push on, at the rest 6 den Gamma^2 and at
    6: each lift on its trains' gears with its own turn on the sites and the square's slots turns the run alike, the teeth rounding.
    No: at the rest 6 a negated gear's tooth negated and not flipped, the turned run and the run turned part."""
    spins = [{"name": f"spin {n}", "kinds": k, "part": p} for n, (k, p) in enumerate((COSETS, CLASSES))]
    shape = (2, 2, 2)
    for integers, reach in ((None, 1 << 300), ({"den": 1, "full_rate": 1}, 1 << 8)):
        held, layout = laid([CLICKS[1], *spins], {"push": 1}, integers, shape)
        start = drawn(held, layout, 11, reach)
        end, moved = ran(layout, start, 1)
        assert moved and all(board_turnings(layout, held, start, end, shape))
        # the no, at the rest 6: a negated gear's tooth negated, not flipped
        assert integers is None or not all(board_turnings(layout, held, start, end, shape, False))
