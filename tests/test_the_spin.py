"""The spin branch (2026-10-19, stacked on the click branch; ALGEBRA.md, Spin, closed for the paper as a route, and the derivation of the same day: under the 48 every line Rule3 steps is a scalar, no record carries a spinor, and the half angle is the detector's read of two planes under a basis it declares): a quantum of spin one half is a record of two planes as two parts of one record (the family's shape [2, 2], the parts laid as one event and never summed at a Node), and a detector declaring its `axis`, the half-angle pair (c, s) with the Bloch axis (2 c s, c^2 - s^2) / (c^2 + s^2) in the x-z plane, credits the quantum to one of its two ports, up or down the axis, by the joint credit's one form on the parts' plane sums; nothing at the Node. The worlds are the tests' own (`tests.laws.spin_world`), no run beyond them."""

import itertools
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
SINGLET = [
    [0, 1],
    [-1, 0],
]  # the partner's pattern in the singlet: its + port reads (s, -c), its - port (c, s)
BELL = (
    (1, 0),
    (1, 1),
    (12, 5),
    (5, 12),
)  # a, a', b, b' as half-angle pairs: 0 and 90 degrees, and cos = 119 / 169
PORT = {"plus": 0, "minus": 1}
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


def joint_shares(
    lines: list[dict], sides: dict[str, tuple[tuple[int, int], list[list[int]]]]
) -> dict[tuple[int, ...], int]:  # type: ignore[type-arg]
    """The joint credit's shares per combination of the sides' ports (0 the plus port, 1 the minus) from the `parts` lines of the regions in `sides` ({name: (axis, pattern)}), the reader's own arithmetic beside the engine's (`credit.joined`): per interval and member of the level pair the amplitude SUM_k PROD_sides e^s_k(port) psi^s_k with psi^s_k the part's (re, im) sums at side s, the product over the sides of one interval, its norm squared summed over the window; one side gives the two shares of Stern and Gerlach."""
    names = list(sides)
    ports = {
        n: ports_of(axis, tuple(tuple(pair) for pair in pattern)) for n, (axis, pattern) in sides.items()
    }
    intervals: dict[int, dict[str, list[list[int]]]] = {}
    for row in lines:
        if row["event"] == "parts" and row["node_detector"] in sides:
            intervals.setdefault(row["interval"], {})[row["node_detector"]] = row["levels"]
    found = {}
    for key in itertools.product(range(2), repeat=len(names)):
        total = 0
        for levels in intervals.values():
            for member in range(2):
                re_sum, im_sum = 0, 0
                for k in range(2):
                    product = (1, 0)
                    for name, port in zip(names, key, strict=True):
                        sums = levels.get(
                            name, [[0, 0]] * 4
                        )  # per line [now, before]: re_1, im_1, re_2, im_2
                        e = ports[name][port][k]
                        re, im = e * sums[2 * k][member], e * sums[2 * k + 1][member]
                        product = (product[0] * re - product[1] * im, product[0] * im + product[1] * re)
                    re_sum, im_sum = re_sum + product[0], im_sum + product[1]
                total += re_sum * re_sum + im_sum * im_sum
        found[key] = total
    return found


def correlation(a: tuple[int, int], b: tuple[int, int]) -> Fraction:
    """The singlet's E(a, b) = -cos(theta_a - theta_b) from the half-angle pairs, exact: -((c_a c_b + s_a s_b)^2 - (c_a s_b - s_a c_b)^2) / ((c_a^2 + s_a^2) (c_b^2 + s_b^2))."""
    (ca, sa), (cb, sb) = a, b
    same, different = (ca * sb - sa * cb) ** 2, (ca * cb + sa * sb) ** 2
    return Fraction(same - different, (ca * ca + sa * sa) * (cb * cb + sb * sb))


def test_a_two_plane_quantum_goes_up_or_down_the_declared_axis_by_the_half_angle(tmp_path, monkeypatch):
    """Stern and Gerlach on the board: one quantum of the two-plane family (the amplitude 90, the lay 75, the share 0.9994 of the record's unit, the count 1) laid in the equal-parts state (psi_1 = psi_2, the Bloch vector along +x), one region at the chain's lower end declaring its axis as the half-angle pair (c, s) with the identity pattern; at the window's close the whole quantum is credited to the plus port or the minus port, two beams and never a smear (one credit line, count 1, nothing left, the parts kept those the port reads with a coefficient other than 0), with the share (c + s)^2 / (2 (c^2 + s^2)) = cos^2 of the half angle between the axis and the state, exact in the integers' rationals: 1 / 2 at the z axis (1, 0), 1 at the x axis (1, 1), 0 at -x (1, -1), 4 / 5 at (3, 1) and 9 / 10 at (2, 1); the shares read from the engine's `parts` lines by the reader's own arithmetic equal the formula exactly, every run's port is one the share allows, and the engine's own draw over the shares (`node_detector.credit_draw`, the states hashed as the trials tool hashes them) gives the plus port within three binomial scatters of the share over 400 draws, exactly all or none along the state."""
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
            up, down = (shares := joint_shares(lines, {"left": (axis, IDENTITY)}))[(0,)], shares[(1,)]
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


def test_the_singlet_reads_minus_the_cosine_of_the_axes_angle_and_breaks_the_bound_at_two_root_two(
    tmp_path, monkeypatch
):
    """The singlet on the board (the Boss's item (d), 2026-10-19): two packets of the two-plane family from the centre toward the two ends, half a quantum each, the two parts laid alike on both, the left region's pattern the identity and the right region's the singlet's [[0, 1], [-1, 0]] (the partner reads the parts crossed with one sign turned, the antisymmetric pair), each region its own `axis`; the joint credit over the window gives E(a, b) = -cos(theta_a - theta_b) exact in the integers' rationals from the engine's `parts` lines at the four Bell settings, -119 / 169, 119 / 169, -120 / 169, -120 / 169, so |S| = 478 / 169 (the photons' S with (a - b) in the place of 2 (a - b)); each side's marginal 1 / 2 whatever the partner's axis; at equal axes the shares of (+, +) and (-, -) are 0 exactly, the anticorrelation, and the combination realised is one of the two the shares allow; the pair is one quantum of the record, each packet half of it (the amplitude 64, the lay 54, the two shares 1.0134 of the record's unit together), and every run credits both sides with the one combination drawn (two credit lines, one per side, count 1, nothing left; `lists.region`); the engine's own draw over the four shares at (a, b) (`node_detector.credit_draw`, 400 hashed states) within three binomial scatters of each share."""
    found = {}
    for a in BELL[:2]:
        for b in BELL[2:]:
            sides = {"left": (a, IDENTITY), "right": (b, SINGLET)}
            path = spin_world(
                tmp_path / f"{a[0]}_{a[1]}_{b[0]}_{b[1]}", monkeypatch, sides, both=True, amplitude=64
            )
            board, lines = trial(path, 1, 40)
            clicks = [c for c in lines if c["event"] == "credit"]
            assert [c["node_detector"] for c in clicks] == ["left", "right"], clicks
            assert all(c["count"] == 1 and c["left"] == 0 for c in clicks), clicks
            shares = joint_shares(lines, sides)
            total = sum(shares.values())
            same, different = shares[0, 0] + shares[1, 1], shares[0, 1] + shares[1, 0]
            assert Fraction(same - different, total) == correlation(a, b), (a, b, shares)
            assert Fraction(shares[0, 0] + shares[0, 1], total) == Fraction(1, 2)  # the left marginal
            assert Fraction(shares[0, 0] + shares[1, 0], total) == Fraction(1, 2)  # the right marginal
            assert shares[tuple(PORT[c["realised"]] for c in clicks)] > 0, clicks
            found[a, b] = correlation(a, b)
            print(f"singlet: the axes {a} and {b} read E = {found[a, b]}, the shares {shares}")
    a, a2, b, b2 = BELL
    assert [found[a, b], found[a, b2], found[a2, b], found[a2, b2]] == [
        Fraction(-119, 169),
        Fraction(119, 169),
        Fraction(-120, 169),
        Fraction(-120, 169),
    ]
    assert abs(found[a, b] - found[a, b2] + found[a2, b] + found[a2, b2]) == Fraction(478, 169)
    sides = {"left": ((3, 1), IDENTITY), "right": ((3, 1), SINGLET)}
    board, lines = trial(
        spin_world(tmp_path / "equal", monkeypatch, sides, both=True, amplitude=64), 1, 40
    )
    shares = joint_shares(lines, sides)
    assert shares[0, 0] == shares[1, 1] == 0 and shares[0, 1] == shares[1, 0] > 0, shares
    clicks = [c for c in lines if c["event"] == "credit"]
    assert tuple(PORT[c["realised"]] for c in clicks) in {(0, 1), (1, 0)}, clicks
    keys, counts = sorted(shares), [0] * 4
    for state in range(DRAWS):
        board.credit.state = TRIALS.hashed_state(state, board.world.width)
        counts[credit_draw(board, [shares[key] for key in keys])] += 1
    assert counts[keys.index((0, 0))] == counts[keys.index((1, 1))] == 0
    sides = {"left": (a, IDENTITY), "right": (b, SINGLET)}
    board, lines = trial(
        spin_world(tmp_path / "draws", monkeypatch, sides, both=True, amplitude=64), 2, 40
    )
    shares, counts = joint_shares(lines, sides), [0] * 4
    keys, total = sorted(shares), sum(shares.values())
    for state in range(DRAWS):
        board.credit.state = TRIALS.hashed_state(state, board.world.width)
        counts[credit_draw(board, [shares[key] for key in keys])] += 1
    for key, count in zip(keys, counts, strict=True):
        p = shares[key] / total
        assert abs(count - DRAWS * p) <= 3 * (DRAWS * p * (1 - p)) ** 0.5, (key, count, p)
    print(f"singlet: the draw at {a}, {b} gives {dict(zip(keys, counts, strict=True))} of {DRAWS}")
