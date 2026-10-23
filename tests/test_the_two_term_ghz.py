"""The two-term plane GHZ (the reader's design verdict of 2026-10-20, Part B; ALGEBRA.md, The meeting's identity, the Gram theorem's identity case; The click is the meeting of the future with the past): the Gaussian clause of the write, a side's quarter turn on a plane record, and the record of two terms of planes read at three sides; and first the byte-for-byte test of every real-port world the branch ships, recorded by this test at the eighth commit as pushed (5efd3b4d7), the real path before the Gaussian pairs (the eighth's own tests pin none of them; the reader's run at that commit confirms every one), so that the real path's identity is a test and no claim."""

import hashlib
import json
from fractions import Fraction

import numpy as np
import pytest

from event_universe import meeting_back, world_files
from event_universe.lattice import Lattice
from event_universe.loader.draw import UNITS, Gauss, norm, ports_of, setting_of, times
from event_universe.world_files import load_world
from tests.laws import EVENTS, ROOT, TOOL
from tests.laws_read import load_shipped
from tests.laws_spin import (
    IDENTITY,
    PORT,
    SINGLET,
    SPIN,
    digest,
    joint_shares,
    marginal_of,
    sided,
    spin_world,
)

X, Y = (
    0,
    3,
)  # the x basis the axis [1, 1] at the turn 0, the y basis the same axis at the turn 3 (u = -i)
COUNT = (
    6151  # the two-term record's count on the board at the close, 6,149 at the lay, the step's walk of 2
)
SETTINGS = {
    "x_x_x": ((X, X, X), 1),
    "x_y_y": ((X, Y, Y), -1),
    "y_x_y": ((Y, X, Y), -1),
    "y_y_x": ((Y, Y, X), -1),
}

REAL_PORT_DIGESTS: dict[
    str, tuple[str, str, int]
] = {  # the lines' digest, the arrays' digest at the end, the lines; the lines' digests re-recorded 2026-10-20 under the twist's deletion, the credit line without twist and shortfall, the arrays' digests and the counts as at the ninth; the entries marked `former` re-recorded 2026-10-23 under two acts of the law's reading on the owner's decisions of 2026-10-23, the count centred (the phase hand's run on the documents tree, the arrays' digest named `centred` where its table has the world) and the window derived and never declared (the windows hand's run on the branch windows, every click at its derived close): each names the former lines' digest, arrays' digest and count; the entries marked `former` re-recorded 2026-10-23 under two acts of the law's reading on the owner's decisions of 2026-10-23, the count centred (the phase hand's run on the documents tree, the arrays' digest named `centred` where its table has the world) and the window derived and never declared (the windows hand's run on the branch windows, every click at its derived close): each names the former lines' digest, arrays' digest and count
    "singlet_a_b": (
        "bfcbdf59a9085e84",
        "2aed7082f74bdfd3",
        421,
    ),  # former bfcbdf59a9085e84, 2aed7082f74bdfd3, 421; centred f58fefcc86e2ece1; the clicks 2: left:plus@30, right:minus@30; former 1b4de9a3ecd0fbe3, 29c984886c98a340, 152; centred f58fefcc86e2ece1; the clicks 2: left:plus@30, right:minus@30
    "singlet_a_b_prime": (
        "4da72e5cd021809f",
        "2aed7082f74bdfd3",
        421,
    ),  # former 4da72e5cd021809f, 2aed7082f74bdfd3, 421; centred f58fefcc86e2ece1; the clicks 2: left:plus@30, right:plus@30; former 3fb0cfd3c2d4f761, 29c984886c98a340, 152; centred f58fefcc86e2ece1; the clicks 2: left:plus@30, right:plus@30
    "singlet_a_prime_b": (
        "9a8e8c76a96a3f79",
        "0daa86151311d32c",
        456,
    ),  # former 9a8e8c76a96a3f79, 0daa86151311d32c, 456; centred 4fa2bf3b04c65a88; the clicks 2: left:minus@30, right:plus@30; former cf3ee118d5d5a591, 355f34162a2096bc, 165; centred 4fa2bf3b04c65a88; the clicks 2: left:minus@30, right:plus@30
    "singlet_a_prime_b_prime": (
        "3ca88a811ea9f2b8",
        "0444781a43c9f9bb",
        456,
    ),  # former 3ca88a811ea9f2b8, 0444781a43c9f9bb, 456; centred 6cd440151409074a; the clicks 2: left:minus@30, right:plus@30; former 3a3fa16fd3151ccc, de0951aaad4762b0, 165; centred 6cd440151409074a; the clicks 2: left:minus@30, right:plus@30
    "ghz_x_x_x": (
        "9dfa6215e84a9a46",
        "5b61d065da2b1cca",
        2153,
    ),  # former e3907b49e7107747, d6a774f9d5346e84, 2162; centred 38daaff3c4ff1649; the clicks 3: left:minus@35, right:plus@35, top:minus@35
    "ghz_x_y_y": (
        "0c77d3edf4217284",
        "fff22e30e4d65c26",
        1613,
    ),  # former df89005705555bb6, 03f76ace05e501e9, 1593; centred fff22e30e4d65c26; the clicks left:minus@35, right:plus@35, top:plus@35
    "ghz_y_x_y": (
        "db9e9f42462ef52a",
        "ebae12a7ee683613",
        3337,
    ),  # former d37726d4ad3db38b, 21422c4532c84b95, 3300; the clicks left:minus@35, right:plus@35, top:plus@35
    "ghz_y_y_x": (
        "8584dce0162e8560",
        "e9dfe0e14fd490da",
        3328,
    ),  # former 3b9802f5a46e3e74, befdc50e632d240e, 5007; this hand's run of the shipped world under the derived window 35 (2026-10-23)
}
REFUSED: dict[
    str, str
] = {}  # nothing refused on the landing: the two slits draw at the window 1 and run whole
REAL_PORT_DIGESTS.update(  # the born four at the seventh, 2026-10-20: the atom reads within one Link (G2)
    {
        "two_slits": (
            "c065a075ed83c487",
            "7742549762b6ec9d",
            2683,
        ),  # 2026-10-21, the floor and the remainder's draw: every window's remainder drawn, N 546 (the landing's 874668d0a958235f, be63d2ce99f6604a, 2696 lines, N 500, under the half-up rounding)
        "born_a_b": (
            "f5a43513a239cd68",
            "0177773313ecd712",
            385,
        ),  # former f5a43513a239cd68, 0177773313ecd712, 385; centred a63e69a3e05dddbf; the clicks 3: body 0:g@24, left:minus@72, right:plus@120; former bb97f5dcda1fb8b5, c192784fb41509b1, 290; centred a63e69a3e05dddbf; the clicks 3: body 0:g@24, left:minus@72, right:plus@120
        "born_a_b_prime": (
            "dc672678350bfb01",
            "0177773313ecd712",
            385,
        ),  # former dc672678350bfb01, 0177773313ecd712, 385; centred a63e69a3e05dddbf; the clicks 3: body 0:g@24, left:minus@72, right:minus@120; former 0ea65e583fec7beb, c192784fb41509b1, 290; centred a63e69a3e05dddbf; the clicks 3: body 0:g@24, left:minus@72, right:minus@120
        "born_a_prime_b": (
            "e94a77708718fdab",
            "d3a04b353df0b81e",
            383,
        ),  # former e94a77708718fdab, d3a04b353df0b81e, 383; centred 7b9ceaae0d0a84c6; the clicks 3: body 0:g@24, left:plus@72, right:minus@120; former 19285640497e35f7, b23542a6b2c460fd, 290; centred 7b9ceaae0d0a84c6; the clicks 3: body 0:g@24, left:plus@72, right:minus@120
        "born_a_prime_b_prime": (
            "59b7fdaa84013cb8",
            "d72fae91ad520fda",
            383,
        ),  # former 59b7fdaa84013cb8, d72fae91ad520fda, 383; centred 9cf860847a1ef469; the clicks 3: body 0:g@24, left:plus@72, right:minus@120; former 1a001543d9083ac1, 26aa22f2998f8cd6, 290; centred 9cf860847a1ef469; the clicks 3: body 0:g@24, left:plus@72, right:minus@120
    }
)


def run_digest(folder: str, name: str) -> tuple[str, str, int]:
    """One shipped world run through its intervals: the sha256 (16 hex digits) of its output lines in order (each line's JSON with sorted keys), the hash of every array of the board at the end (`laws_spin.digest`) and the count of lines."""
    lines: list[dict] = []  # type: ignore[type-arg]
    board = Lattice(load_shipped(EVENTS / folder / f"{name}.json"), lines.append)
    for _ in range(board.world.intervals):
        board.step()
    found = hashlib.sha256()
    for line in lines:  # the sixth's bias booking aside, the line the ninth wrote
        kept = {k: v for k, v in line.items() if k != "bias_bound"}
        found.update(json.dumps(kept, sort_keys=True, default=str).encode())
    return found.hexdigest()[:16], digest(board)[:16], len(lines)


def worlds_read(monkeypatch, folder: str, names: tuple[str, ...]) -> None:  # type: ignore[no-untyped-def]
    """Every real-port world the branch ships (the four singlet, the four GHZ of four real parts, the four born, the two slits), run whole: its output lines and its board at the end equal, digest for digest, this test's own recording at the ninth's head before the tenth's merge (4c16df037, the click's read of the board), or refused by name as the ninth refuses it (the born four at 85, the two slits at 130: the digits spent at a second draw); a coefficient with the imaginary part 0 is the integer of the ninth's formulas, so the path is the same path."""
    monkeypatch.setattr(world_files, "REPOSITORY_ROOT", ROOT)
    for name in names:
        if name in REFUSED:  # refused by name as the ninth's read refuses it, the same with the tenth
            with pytest.raises(RuntimeError, match=REFUSED[name]):
                run_digest(folder, name)
            continue
        found = run_digest(folder, name)
        print(f"{folder}/{name}: {found}")
        assert found == REAL_PORT_DIGESTS[name], name


def test_the_four_singlet_worlds_run_byte_for_byte_as_at_the_ninth(monkeypatch):  # type: ignore[no-untyped-def]
    """The four shipped singlet worlds of bell_singlet, digest for digest the recording at the ninth before the merge, 4c16df037 (`worlds_read`; the clock gives each folder its own test)."""
    worlds_read(
        monkeypatch,
        "bell_singlet",
        ("singlet_a_b", "singlet_a_b_prime", "singlet_a_prime_b", "singlet_a_prime_b_prime"),
    )


def test_the_four_born_worlds_run_byte_for_byte_as_at_the_ninth(monkeypatch):  # type: ignore[no-untyped-def]
    """The four shipped born-pair worlds of bell_singlet, digest for digest the recording at the ninth's seventh commit (what a body reads, the reader's G2 of 2026-10-20: the atom's absorption draws at 85 and 110 read the pair's wake within one Link and carry their totals; `worlds_read`)."""
    worlds_read(
        monkeypatch,
        "bell_singlet",
        ("born_a_b", "born_a_b_prime", "born_a_prime_b", "born_a_prime_b_prime"),
    )


def test_the_two_slits_world_runs_byte_for_byte_at_the_window_1(monkeypatch):  # type: ignore[no-untyped-def]
    """The shipped two slits world at the draw's window of one interval with the screens two columns deep (the landing of 2026-10-20), run whole, digest for digest the recording of 2026-10-21 under the floor and the remainder's draw (`credit.whether`: 88 closes drew their remainder, 30 of them a quantum, N 546 where the half-up rounding's carry gave 500; `worlds_read`); at the ninth's window 130 the same world was refused by name at its close, the digits spent by the many-draw close (the ninth's test_the_two_slits_many_draw_close_spends_the_digits_at_the_window_130 keeps that reading)."""
    worlds_read(monkeypatch, "two_slits", ("two_slits",))


def test_the_ghz_worlds_x_x_x_and_x_y_y_run_byte_for_byte_as_at_the_ninth(monkeypatch):  # type: ignore[no-untyped-def]
    """Two of the four shipped GHZ worlds of four real parts, x x x and x y y, digest for digest the recording at the ninth before the merge, 4c16df037 (`worlds_read`; two per test for the clock)."""
    worlds_read(monkeypatch, "ghz", ("ghz_x_x_x", "ghz_x_y_y"))


def test_the_ghz_worlds_y_x_y_and_y_y_x_run_byte_for_byte_as_at_the_ninth(monkeypatch):  # type: ignore[no-untyped-def]
    """The other two shipped GHZ worlds, y x y and y y x, digest for digest the recording at the ninth before the merge, 4c16df037 (`worlds_read`); with the first pair every real-port world the branch ships is run."""
    worlds_read(monkeypatch, "ghz", ("ghz_y_x_y", "ghz_y_y_x"))


def conj_times(a: Gauss, b: Gauss) -> Gauss:
    """conj(a) b on Gaussian integers, the Hermitian product of two coefficients."""
    return times((a[0], -a[1]), b)


def test_the_quarter_turn_makes_the_hermitian_ports_and_the_loader_refuses_it_by_name(
    tmp_path, monkeypatch
):  # type: ignore[no-untyped-def]
    """The key `turn` (B2 of the reader's design): at the turn 0 the ports are the eighth's integers with 0 behind them; at the turn 3 the identity pattern at `axis` [1, 1] reads (1, -i) and (-i, 1), orthogonal in the Hermitian form with equal norms; every quarter turn's ports orthogonal with equal norms on the identity and on a general pattern; the loader refuses by name `turn` beside `basis`, `turn` without `axis` and a turn outside 0 to 3, and admits the key on a plane side (the singlet chain's sides at the turn 3 load and run)."""
    identity = tuple(tuple(pair) for pair in IDENTITY)
    plus, minus = ports_of((1, 1), identity)
    assert (plus, minus) == (
        ((1, 0), (1, 0)),
        ((-1, 0), (1, 0)),
    )  # the eighth's (1, 1) and (-1, 1) as pairs
    plus, minus = ports_of((1, 1), identity, 3)
    assert (plus, minus) == (((1, 0), (0, -1)), ((0, -1), (1, 0)))  # (1, -i) and (-i, 1)
    for turn in range(4):
        for setting, pattern in (
            ((1, 1), identity),
            ((3, 5), tuple(tuple(pair) for pair in SINGLET)),
            ((12, 5), identity),
        ):
            plus, minus = ports_of(setting, pattern, turn)
            crossed = (0, 0)
            for a, b in zip(plus, minus, strict=True):
                product = conj_times(a, b)
                crossed = (crossed[0] + product[0], crossed[1] + product[1])
            assert crossed == (0, 0) and sum(map(norm, plus)) == sum(map(norm, minus)), (
                turn,
                setting,
                pattern,
            )
    assert UNITS == ((1, 0), (0, 1), (-1, 0), (0, -1))
    sides = {"left": ((1, 1), IDENTITY), "right": ((1, 1), IDENTITY)}
    path = spin_world(tmp_path / "turned", monkeypatch, sides, both=True, amplitude=64)
    world = json.loads(path.read_text(encoding="utf-8"))
    for turned, text in (
        ({"turn": 3, "basis": [1, 1]}, "beside its `axis`"),
        ({"turn": 5}, "from 0 through 3"),
        ({"turn": -1}, "from 0 through 3"),
    ):
        row = {**world["node_detectors"][0], **turned}
        if "basis" in row:
            row.pop("axis")
        with pytest.raises(ValueError, match=text):  # the loader's reading of the row's setting
            setting_of(row, "node_detectors[0]")
    world["node_detectors"][1]["turn"] = 3
    (good := tmp_path / "turned" / "spin_turned.json").write_text(
        json.dumps(world) + "\n", encoding="utf-8"
    )
    TOOL.main(["--input", str(good)])
    board = Lattice(load_world(good))
    assert board.world.node_detectors[1].turn == 3 and board.credit.sides[1][1] == ports_of(
        (1, 1), identity, 3
    )


def test_the_patterns_gram_is_real_for_every_quarter_turn():
    """The plan's algebra, asserted: for a side's two ports (c, u s) and (-conj(u) s, c) with |u| = 1 the Hermitian sum over the ports, SUM_p conj(e_k(p)) e_m(p), is (p^2 + q^2)(alpha_k alpha_m + beta_k beta_m) for every quarter turn, the azimuth's cross terms cancelling, so `gram_of` reads the pattern alone and stays real (B1's identity case: G = I on the identity pattern, no pattern of another side entering a read)."""
    for turn in range(4):
        for (p, q), pattern in (
            ((1, 1), ((1, 0), (0, 1))),
            ((3, 5), tuple(tuple(pair) for pair in SINGLET)),
            ((12, 5), ((1, 0), (0, 1))),
        ):
            ports = ports_of((p, q), pattern, turn)
            gram = meeting_back.gram_of([pattern], 2)
            for k in range(2):
                for m in range(2):
                    total = (0, 0)
                    for port in ports:
                        product = conj_times(port[k], port[m])
                        total = (total[0] + product[0], total[1] + product[1])
                    assert total == ((p * p + q * q) * gram[k][m], 0), (turn, p, q, k, m)


def test_a_unit_coefficient_turns_a_planes_two_lines_bit_for_bit_and_a_global_unit_writes_nothing(
    tmp_path, monkeypatch
):  # type: ignore[no-untyped-def]
    """The write on planes (B2 iii): a plane part whose port coefficient is the unit i carries the overlap conj(i) = -i, its two lines moved together, re' = im and im' = -re, bit for bit through the one lay act, the other part untouched; a global unit on every surviving part, (i, i), is the identity and writes nothing (`credit.reduced` on pairs); the written coefficients and the scale read the pairs' norms."""
    sides = {"left": ((1, 1), IDENTITY), "right": ((1, 1), IDENTITY)}
    board = Lattice(
        load_world(spin_world(tmp_path / "unit", monkeypatch, sides, both=True, amplitude=64))
    )
    spin = [f.name for f in board.families].index("spin")  # the write at the birth, the lay's interval 0
    before = [np.asarray(line.now).copy() for line in board.states[spin].lines]
    befores = [np.asarray(line.before).copy() for line in board.states[spin].lines]
    meeting_back.realised(board, spin, [(1, 0), (0, 1)])
    lines = board.states[spin].lines
    assert (np.asarray(lines[0].now) == before[0]).all() and (
        np.asarray(lines[1].now) == before[1]
    ).all()
    assert (np.asarray(lines[2].now) == before[3]).all() and (
        np.asarray(lines[3].now) == -before[2]
    ).all()
    assert (np.asarray(lines[2].before) == befores[3]).all() and (
        np.asarray(lines[3].before) == -befores[2]
    ).all()
    assert board.credit.written[spin] == [(1, 0), (0, -1)] and board.credit.scale[spin] == 2
    turned = [np.asarray(line.now).copy() for line in lines]
    meeting_back.realised(board, spin, [(0, 1), (0, 1)])  # a global unit: the identity, nothing written
    assert all(
        (np.asarray(line.now) == was).all()
        for line, was in zip(board.states[spin].lines, turned, strict=True)
    )
    assert board.credit.written[spin] == [(1, 0), (0, -1)] and board.credit.scale[spin] == 2


def ghz_plane_world(  # type: ignore[no-untyped-def]
    folder,
    monkeypatch,
    turns,
    amplitude=1328,
    intervals=60,
    across=4,
    along=6,
    centres=(16, 16, 16),
):
    """The two-term plane GHZ declared here (B3 of the reader's design): the spin family [2, 2] (two planes, no sign) on a 33 x 33 board open on x and y with receding faces, three packets from the centre toward -x, +x and +y at the shipped GHZ's amplitude 1328 (6,149 quanta at the lay: a one-quantum lay, amplitude 20, reads 3 at the close, the integer step's share noise in two dimensions being about 2.4 quanta over 60 intervals at both amplitudes tried, 20 and 1,328), both terms laid alike, three regions at the three ends (the four-real-parts GHZ's beams and regions), each side the identity pattern at `axis` [1, 1] with its `turn`, 0 the x basis and 3 the y basis; the draw's window the run."""
    folder.mkdir(parents=True, exist_ok=True)
    universe = json.loads((EVENTS / "pair.json").read_text(encoding="utf-8"))
    universe["families"].append(json.loads(json.dumps(SPIN)))
    (folder / "u.json").write_text(json.dumps(universe), encoding="utf-8")
    monkeypatch.setattr(world_files, "REPOSITORY_ROOT", folder)
    wide = {"x": [13, 19], "y": [13, 19], "z": [0, 0]}
    packets = [
        {
            "family": "spin",
            "along": axis,
            "wave": [sign, 4],
            "phase": [0, 1],
            "amplitude": amplitude,
            "top": {**wide, axis: [centre, centre]},
            "edge": {"x": across, "y": across, "z": 0, axis: along},
        }
        for (axis, sign), centre in zip((("x", -1), ("x", 1), ("y", 1)), centres, strict=True)
    ]
    regions = {
        "left": [[x, y, 0] for x in range(4) for y in range(13, 20)],
        "right": [[x, y, 0] for x in range(29, 33) for y in range(13, 20)],
        "top": [[x, y, 0] for x in range(13, 20) for y in range(29, 33)],
    }
    detectors = [
        {"name": name, "positions": regions[name], "axis": [1, 1], "turn": turn, "pattern": IDENTITY}
        for name, turn in zip(("left", "right", "top"), turns, strict=True)
    ]
    receding = {"sides": ["low", "high"], "largest": 400, "layers": 16}
    world = {
        "shape": [33, 33, 1],
        "boundary": {"x": "open", "y": "open", "z": "periodic"},
        "face_depth": 1,
        "intervals": intervals,
        "universe": "u.json",
        "bodies": [],
        "packets": packets,
        "node_detectors": detectors,
        "receding": {"x": receding, "y": receding},
        "draw": {},
    }
    (path := folder / "ghz2.json").write_text(json.dumps(world) + "\n", encoding="utf-8")
    TOOL.main(["--input", str(path)])
    return path


def ghz_plane_read(tmp_path, monkeypatch, name, amplitude=1328):  # type: ignore[no-untyped-def]
    """One setting of the two-term plane GHZ run under the cone (the default): the board, its lines, the credit lines in the declared order and the realised ports."""
    turns, _sign = SETTINGS[name]
    path = ghz_plane_world(tmp_path / f"{name}_{amplitude}", monkeypatch, turns, amplitude=amplitude)
    lines: list[dict] = []  # type: ignore[type-arg]
    board = Lattice(load_world(path), lines.append)
    for _ in range(board.world.intervals):
        board.step()
    clicks = [c for c in lines if c["event"] == "credit" and c.get("order") is not None]
    return board, lines, clicks, [PORT[c["realised"]] for c in clicks]


def setting_read(name: str, tmp_path, monkeypatch) -> None:  # type: ignore[no-untyped-def]
    """The two-term plane GHZ (B3): at the four settings x x x, x y y, y x y, y y x the eight shares of the three sides' ports are 0 or 1 / 4 of the whole, E_3 = +1, -1, -1, -1 exactly, every marginal 1 / 2 and every pairwise correlation 0, the gate's blind; the engine's weights at every side the chain rule's (`sided`): the first side's its own parts' shares, 1 / 2 at either port, the second's the same (G = I, B1), the third's coherent, one port 0; the realised triple's parity the setting's sign; three credit lines with `order` 1, 2, 3, the scale 2 after every write (the coefficients Gaussian units, the norm the parts' count) and the count on the board 6,151 at every side's close (6,149 at the lay: the step's walk of 2 in 6,000, the shipped GHZ's); the cone's assertions holding over seven passes, the tick at the close."""
    turns, sign = SETTINGS[name]
    board, lines, clicks, realised = ghz_plane_read(tmp_path, monkeypatch, name)
    spin = [f.name for f in board.families].index("spin")
    sides = {
        n: ((1, 1), IDENTITY, turn) for n, turn in zip(("left", "right", "top"), turns, strict=True)
    }
    shares = joint_shares(lines, sides, 0, close=clicks[-1]["interval"])  # to the close (2026-10-23)
    total = sum(shares.values())
    assert total > 0 and all(share in (0, Fraction(total, 4)) for share in shares.values()), shares
    e_3 = sum(Fraction((-1) ** sum(key), 1) * share for key, share in shares.items()) / total
    assert e_3 == sign, (name, e_3)
    for side in range(3):
        assert Fraction(marginal_of(shares, side)[0], total) == Fraction(1, 2)
    for a, b in ((0, 1), (0, 2), (1, 2)):
        pair = sum(Fraction((-1) ** (key[a] + key[b]), 1) * share for key, share in shares.items())
        assert pair == 0
    sided(board, spin, shares, realised)
    assert [
        (c["node_detector"], c["order"], c["scale"], c["board_count"], c["count"]) for c in clicks
    ] == [
        ("left", 1, 2, COUNT, 1),
        ("right", 2, 2, COUNT, 1),
        ("top", 3, 2, COUNT, 1),
    ]
    assert (-1) ** sum(realised) == sign and board.passes == 7 and board.tick == board.world.intervals
    weights = [board.credit.weights[(spin, n)] for n in ("left", "right", "top")]
    assert weights[0][0] == weights[0][1] > 0 and weights[1][0] == weights[1][1] > 0 and 0 in weights[2]
    print(
        f"the two-term plane GHZ {name}: E_3 = {e_3}, the realised triple {realised}, the weights {weights}"
    )


def test_the_two_term_plane_ghz_at_x_x_x_reads_e_3_plus_one(tmp_path, monkeypatch):  # type: ignore[no-untyped-def]
    """The two-term plane GHZ at x x x (the clock gives each setting its own test): E_3 = +1 exactly with the eight shares 0 or 1 / 4, the marginals 1 / 2, the pairwise correlations 0, the weights the chain rule's, the three credit lines (`setting_read`)."""
    setting_read("x_x_x", tmp_path, monkeypatch)


def test_the_two_term_plane_ghz_at_x_y_y_reads_e_3_minus_one(tmp_path, monkeypatch):  # type: ignore[no-untyped-def]
    """The two-term plane GHZ at x y y: E_3 = -1 exactly, the same reading (`setting_read`)."""
    setting_read("x_y_y", tmp_path, monkeypatch)


def test_the_two_term_plane_ghz_at_y_x_y_reads_e_3_minus_one(tmp_path, monkeypatch):  # type: ignore[no-untyped-def]
    """The two-term plane GHZ at y x y: E_3 = -1 exactly, the same reading (`setting_read`)."""
    setting_read("y_x_y", tmp_path, monkeypatch)


def test_the_two_term_plane_ghz_at_y_y_x_reads_e_3_minus_one(tmp_path, monkeypatch):  # type: ignore[no-untyped-def]
    """The two-term plane GHZ at y y x: E_3 = -1 exactly, the same reading (`setting_read`); over the four settings M = 1 - (-1) - (-1) - (-1) = 4 in magnitude, the gate's signs."""
    setting_read("y_y_x", tmp_path, monkeypatch)


def test_the_two_term_plane_ghz_is_exact_at_another_amplitude(tmp_path, monkeypatch):  # type: ignore[no-untyped-def]
    """The writes Gaussian units and the two terms standing unit for unit bit for bit at every side's read on this family (the third side's one port exactly 0 in the engine's own read), so the numbers are exact at every read: x y y at the amplitude 1300, another board for the click's read, reads E_3 = -1 with the parity odd, the shares 0 or 1 / 4."""
    board, lines, clicks, realised = ghz_plane_read(tmp_path, monkeypatch, "x_y_y", amplitude=1300)
    turns, sign = SETTINGS["x_y_y"]
    shares = joint_shares(
        lines,
        {n: ((1, 1), IDENTITY, t) for n, t in zip(("left", "right", "top"), turns, strict=True)},
        0,
        close=clicks[-1]["interval"],
    )
    total = sum(shares.values())
    e_3 = sum(Fraction((-1) ** sum(key), 1) * share for key, share in shares.items()) / total
    assert e_3 == sign and (-1) ** sum(realised) == sign and len(clicks) == 3
