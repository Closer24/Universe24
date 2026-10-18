"""The spin branch (2026-10-19, stacked on the click branch; ALGEBRA.md, Spin, closed for the paper as a route, and the derivation of the same day: under the 48 every line Rule3 steps is a scalar, no record carries a spinor, and the half angle is the detector's read of two planes under a basis it declares): a quantum of spin one half is a record of two planes as two parts of one record (the family's shape [2, 2], the parts laid as one event and never summed at a Node), and a detector declaring its `axis`, the half-angle pair (c, s) with the Bloch axis (2 c s, c^2 - s^2) / (c^2 + s^2) in the x-z plane, credits the quantum to one of its two ports, up or down the axis, by the joint credit's one form on the parts' plane sums; nothing at the Node. The worlds are the tests' own (`tests.laws.spin_world`), no run beyond them."""

from fractions import Fraction
from pathlib import Path

from event_universe.lattice import Lattice
from event_universe.loader.draw import ports_of, settings_of_the_law
from event_universe.loader.universe import universe_of
from event_universe.loader.world import node_detectors_of
from event_universe.node_detector import credit_draw
from event_universe.world_files import input_digest, load_world
from tests.laws import ROOT, load_file, refused, spin_world

TRIALS = load_file("meeting_trials", ROOT / "tools" / "meeting_trials.py")
IDENTITY = [[1, 0], [0, 1]]  # the parts the spinor's two components: the + port reads (c, s)
SEEDS = (1, 2)  # the runs per axis; the draw's statistics are read from the engine's own draw below
DRAWS = 400


def trial(path: Path, seed: int, intervals: int) -> tuple[Lattice, list[dict]]:  # type: ignore[type-arg]
    """One run from the lay with the regions' draw at the trial's seed (`hashed_state`, the trials tool's), the board and its lines."""
    lines: list[dict] = []  # type: ignore[type-arg]
    board = Lattice(load_world(path), lines.append)
    board.credit.state = TRIALS.hashed_state(seed, board.world.width)
    for _ in range(intervals):
        board.step()
    return board, lines


def shares_of(lines: list[dict], name: str, axis: tuple[int, int], pattern) -> tuple[int, int]:  # type: ignore[no-untyped-def, type-arg]
    """The joint credit's two shares from the `parts` lines of one region, the reader's own arithmetic beside the engine's: per interval and member the spinor amplitude SUM_k e_k(port) psi_k with psi_k the part's (re, im) sums, its norm squared summed (the plus port first)."""
    ports = ports_of(axis, tuple(tuple(pair) for pair in pattern))
    found = []
    for coefficients in ports:
        total = 0
        for line in (row for row in lines if row["event"] == "parts" and row["node_detector"] == name):
            levels = line["levels"]  # per line [now, before]: re_1, im_1, re_2, im_2
            for member in range(2):
                re = sum(coefficients[k] * levels[2 * k][member] for k in range(2))
                im = sum(coefficients[k] * levels[2 * k + 1][member] for k in range(2))
                total += re * re + im * im
        found.append(total)
    return found[0], found[1]


def test_a_two_plane_quantum_goes_up_or_down_the_declared_axis_by_the_half_angle(tmp_path, monkeypatch):
    """Stern and Gerlach on the board: one quantum of the two-plane family (the generator's one count) laid in the equal-parts state (psi_1 = psi_2, the Bloch vector along +x), one region at the chain's lower end declaring its axis as the half-angle pair (c, s) with the identity pattern; at the window's close the whole quantum is credited to the plus port or the minus port, two beams and never a smear (one credit line, count 1, nothing left, the parts kept those the port reads with a coefficient other than 0), with the share (c + s)^2 / (2 (c^2 + s^2)) = cos^2 of the half angle between the axis and the state, exact in the integers' rationals: 1 / 2 at the z axis (1, 0), 1 at the x axis (1, 1), 0 at -x (1, -1), 4 / 5 at (3, 1) and 9 / 10 at (2, 1); the shares read from the engine's `parts` lines by the reader's own arithmetic equal the formula exactly, every run's port is one the share allows, and the engine's own draw over the shares (`node_detector.credit_draw`, the states hashed as the trials tool hashes them) gives the plus port within three binomial scatters of the share over 400 draws, exactly all or none along the state."""
    for axis, expected in (
        ((1, 0), Fraction(1, 2)),
        ((1, 1), Fraction(1)),
        ((1, -1), Fraction(0)),
        ((3, 1), Fraction(4, 5)),
        ((2, 1), Fraction(9, 10)),
    ):
        path = spin_world(
            tmp_path / f"axis_{axis[0]}_{axis[1]}", monkeypatch, {"left": (axis, IDENTITY)}
        )
        for seed in SEEDS:
            board, lines = trial(path, seed, 40)
            clicks = [c for c in lines if c["event"] == "credit"]
            assert len(clicks) == 1 and clicks[0]["node_detector"] == "left", clicks
            assert clicks[0]["count"] == 1 and clicks[0]["left"] == 0, clicks
            up, down = shares_of(lines, "left", axis, IDENTITY)
            assert Fraction(up, up + down) == expected, (axis, up, down)  # the half angle's share, exact
            allowed = {"plus"} if expected == 1 else {"minus"} if expected == 0 else {"plus", "minus"}
            port = clicks[0]["realised"]
            assert port in allowed, (axis, port)
            coefficients = ports_of(axis, ((1, 0), (0, 1)))[port == "minus"]
            assert clicks[0]["kept"] == [
                k for k, e in enumerate(coefficients) if e != 0
            ]  # the parts the port reads
        plus = 0
        for state in range(DRAWS):
            board.credit.state = TRIALS.hashed_state(state, board.world.width)
            plus += credit_draw(board, [up, down]) == 0
        n, p = DRAWS, float(expected)
        assert abs(plus - n * p) <= 3 * (n * p * (1 - p)) ** 0.5, (axis, plus)
        print(f"spin: the axis {axis} credits up {plus} of {n} against the share {expected}")


def test_the_axis_is_the_planes_setting_and_the_basis_the_real_lines(tmp_path, monkeypatch):
    """The settings' law (`loader/draw.settings_of_the_law`, `loader/world.node_detectors_of`): a side of a record of planes declares `axis` and a side of a record of real lines declares `basis`, each refused by name on the other kind, the two together refused, one pattern over laid records of both kinds refused, and a setting on a body's node_detector refused; the spin world loads with its axis, and the same world with `basis` in the axis's place (its mode file re-addressed to it) is refused by name."""
    import json

    path = spin_world(tmp_path, monkeypatch, {"left": ((1, 0), IDENTITY)})
    world = json.loads(path.read_text(encoding="utf-8"))
    universe = json.loads((tmp_path / "u.json").read_text(encoding="utf-8"))
    families = universe_of(universe)[1]
    spin, pair = ([f.name for f in families].index(n) for n in ("spin", "light_pair"))
    row, shape = world["node_detectors"][0], tuple(world["shape"])
    assert load_world(path).node_detectors[0].axis == (1, 0)
    refused("both `axis` and `basis`", node_detectors_of, [{**row, "basis": [1, 0]}], shape, 0, (), ())
    refused(
        "none is declared",
        node_detectors_of,
        [{k: v for k, v in row.items() if k != "axis"}],
        shape,
        0,
        (),
        (),
    )
    refused(
        "not on a body", node_detectors_of, [{"name": "d", "block": 0, "axis": [1, 0]}], shape, 1, (), ()
    )
    pattern = ((1, 0), (0, 1))
    refused(
        "declares `basis` for a record of planes",
        settings_of_the_law,
        [("left", (), (1, 0), pattern)],
        [spin],
        families,
    )
    refused(
        "declares `axis` for a record of real lines",
        settings_of_the_law,
        [("left", (1, 0), (), pattern)],
        [pair],
        families,
    )
    refused(
        "records of planes and of real lines",
        settings_of_the_law,
        [("left", (1, 0), (), pattern)],
        [spin, pair],
        families,
    )
    settings_of_the_law([("left", (1, 0), (), pattern)], [spin], families)  # the axis on planes stands
    settings_of_the_law(
        [("left", (), (1, 0), pattern)], [pair], families
    )  # the basis on real lines stands
    world["node_detectors"][0] = {**{k: v for k, v in row.items() if k != "axis"}, "basis": [1, 0]}
    (wrong := tmp_path / "wrong.json").write_text(json.dumps(world) + "\n", encoding="utf-8")
    mode = json.loads((tmp_path / "spin.mode.json").read_text(encoding="utf-8"))
    mode["world_digest"] = input_digest(world)
    (tmp_path / "wrong.mode.json").write_text(json.dumps(mode) + "\n", encoding="utf-8")
    refused("declares `basis` for a record of planes", load_world, wrong)
