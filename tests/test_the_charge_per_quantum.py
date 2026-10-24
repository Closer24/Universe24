"""The charge written is the Wronskian over T div 2 for every reader (ALGEBRA.md, The constants, the law's sentence of 2026-10-24 on the owner's word of that morning, the charge universal like nature; the former clause of the same day, each reader's Wronskian times 3 T den over its own count unit, kept by name as the defect: the electron's factor 1,822 times the proton's on the one universe file, one born electron written as 1,822 proton charges, the sign holder's row running away; the old "one ratio per holder, E_h T num / (Gamma den)" of 2026-10-23 kept by name too): the holder of the sign carries one alpha = E_h T / Gamma with any pairs under it (`loader/derived.alpha_of`), and each reader's Wronskian enters the holder's one write at the factor 1 over the one wall 2 E_s T Gamma (`loader/derived.held_write_of`, `loader/charge.charge_factors`), so that a quantum of every plane family, W = T div 2 at the birth's quarter-turn lay, writes the same charge; the register's scale and the lay's amplitude bound stay the loader's tool, a holder of the sign changing no neutral body's register."""

from __future__ import annotations

import json
from dataclasses import replace

import numpy as np

from event_universe import records, world_files
from event_universe.core.ports import LINK_UNIT
from event_universe.emission import laid_by_count
from event_universe.features.click import amplitude
from event_universe.lattice import Lattice
from event_universe.lay import laid
from event_universe.loader.circle import circle_points, lightest_point
from event_universe.loader.derived import amplitude_bound, count_wall, held_write_of
from event_universe.take import Item
from event_universe.world_files import load_world
from tests.laws import EVENTS, refused, resolved
from tests.laws_universe import SMALL, small_universe

GAMMA, T = 1000, 36_000
DEN = 53_567_765
SIGN = {
    "name": "charge",
    "pair": [GAMMA, GAMMA],
}  # the holder of the sign, the held massless row, by hand
SIGN_ROW = "sign"  # the loader's own name for it (loader/universe.SIGN)


def universe(proton: list[int], electron: list[int], gamma: int = GAMMA) -> tuple:  # type: ignore[type-arg]
    """The sign holder with two planes at the pairs given, rows by hand resolved at Gamma, T, the width 92 and G 16 (tests.laws.resolved; the files carry no row since 2026-10-24)."""
    return resolved(
        {**SIGN, "pair": [gamma, gamma]},
        {"name": "proton", "pair": proton, "dimension": 2},
        {"name": "electron", "pair": electron, "dimension": 2},
        node_clock=gamma,
        quantum_action=T,
    )


def test_the_one_world_at_natures_den_loads_with_the_proton_off_the_top():  # type: ignore[no-untyped-def]
    """The universe of $S/arrange/nature_den/universe_nature.json (2026-10-24): the pairs on the circle of den 53,567,765 = 5 x 17 x 73 x 89 x 97 with Gamma 1,000, the proton at (4,859,756, 53,346,867) off the top and the electron at (53,567,757, 29,276), both moving planes reading one holder: refused by name under the sentence of 2026-10-23, loaded under the charge's universality with alpha (36, 1), the write of a born quantum of either family 36 x 17,956 over 72,000 levels per interval."""
    families = resolved(
        {"name": "gravity", "pair": [53_529_741, DEN]},
        {"name": "charge", "pair": [DEN, DEN]},
        {"name": "matter", "pair": [32_140_659, DEN], "dimension": 1},
        {"name": "light", "pair": [DEN, DEN], "dimension": 1},
        {"name": "proton", "pair": [4_859_756, DEN], "dimension": 2},
        {"name": "electron", "pair": [53_567_757, DEN], "dimension": 2},
        node_clock=GAMMA,
        quantum_action=T,
    )  # the one world's six rows of the file to 2026-10-24, by hand (the file carries no row since; the rows derived from den stand in the loader's test)
    sign = next(f for f in families if f.name == "charge")
    assert (sign.write_weight, sign.write_wall) == (36, 1)
    write = held_write_of(families, families.index(sign), T)
    proton, electron = (families.index(f) for f in families if f.name in ("proton", "electron"))
    assert write.factors[proton] == write.factors[electron] == 1  # the charge the Wronskian itself
    assert write.walls[0] == 2 * T * sign.write_wall  # the one wall 2 E_s T Gamma, no count unit in it
    born = amplitude(1, T, (DEN, DEN), 1) ** 2  # the birth's quarter-turn lay, W = A^2 for either child
    assert T // 2 - born < 2 * amplitude(1, T, (DEN, DEN), 1)  # the largest square at or below T div 2
    assert (
        count_wall(families[proton], T) > 1800 * count_wall(families[electron], T)
    )  # the count units differ 1,822 times, and none of it enters the write (the former factor kept by name)


def test_the_register_reads_the_content_rooms_and_a_sign_holder_at_w_0_changes_no_neutral_body():
    """The register's scale and the lay's amplitude bound are the loader's tool and no line of the law, and a record laid at W = 0 writes nothing, so a holder of the sign may not change a neutral body's register (the Boss's word, 2026-10-24; the former rule, the min over every family's rooms with the sign holder's write room among them, kept by name, 2026-10-23): the amplitude bound of a universe whose planes read the sign holder (the charge factors standing) equals the bound of the same universe with the planes reading no sign (no charge factor, the holder written by no source), so the register (`node_detector.scale_of` from `World.amplitude_bound`) is the same; the sign holder's write room is gated apart in `bound_under_rooms`, refused by name where it leaves no level inside the width (no width of this universe reaches that gate before Rule3's own totals refuse, so the refusal is asserted by its sentence in the loader and by no world here)."""
    charged = universe([0, 6000], [3600, 6000])
    neutral = tuple(
        replace(family, reads=()) if family.plane else family for family in charged
    )  # the same planes reading no sign, by hand: every plane reads the sign since 2026-10-24, so no file states them
    bound_charged = amplitude_bound(charged, GAMMA, T, 92, LINK_UNIT)
    bound_neutral = amplitude_bound(neutral, GAMMA, T, 92, LINK_UNIT)
    assert bound_charged == bound_neutral  # the sign holder's write room enters no other family's bound


def bare_board(tmp_path, monkeypatch, output=None):  # type: ignore[no-untyped-def]
    """The tests' small universe on the bare 3-cube torus, the law's uniform seed of light and nothing else (tests.laws_universe.SMALL, den 1,021 with its two points)."""
    monkeypatch.setattr(world_files, "REPOSITORY_ROOT", tmp_path)
    small_universe(tmp_path)
    world = {"universe": "u.json", "shape": [3, 3, 3], "intervals": 40}
    (tmp_path / "bare.json").write_text(json.dumps(world), encoding="utf-8")
    return Lattice(load_world(tmp_path / "bare.json"), output=output)


def points_of(board: Lattice) -> list[str]:
    """The plane rows of the board's universe by name, the heavier point first (the larger s)."""
    planes = [f for f in board.families if f.plane]
    return [f.name for f in sorted(planes, key=lambda f: f.pair[0])]


def holder_rows(board: Lattice) -> list[int]:
    """The largest level of each row of the holder of the sign's time line (the free row 0, then one per charged family)."""
    charge = [f.name for f in board.families].index(SIGN_ROW)
    width, rows = board.families[charge].width, board.families[charge].records
    lines = board.states[charge].lines
    return [int(np.abs(np.asarray(lines[row * width].now, dtype=object)).max()) for row in range(rows)]


def test_equal_wronskians_of_two_families_write_equal_charge(tmp_path, monkeypatch):  # type: ignore[no-untyped-def]
    """The charge written is the Wronskian over T div 2 for every reader (ALGEBRA.md, The constants, 2026-10-24): one quantum of the proton and one of the electron, each laid at a Node in the birth's own form (the count's lay at the massless pair, one sense, W = -A^2 = -17,956), write the same level into the holder of the sign in one interval, 18 each on this file (the former factor wrote the electron's 1,822 times the proton's, 16,427 against 9 per interval)."""
    written = {}
    small = SMALL["integers"]["den"]
    for name in points_of(bare_board(tmp_path, monkeypatch)):
        board = bare_board(tmp_path, monkeypatch)
        names = [f.name for f in board.families]
        index, den = names.index(name), board.families[names.index(name)].pair[1]
        laid_by_count(board, Item(index, 1, ((1, 1, 1),), (den, den), sense=-1))
        wronskian = int(
            np.asarray(records.wronskian(board.lines_of(index, 0), True), dtype=object)[1, 1, 1]
        )
        board.step()
        written[name] = (wronskian, max(holder_rows(board)))
    heavier, lighter = points_of(board)
    assert written[heavier][0] == written[lighter][0] == -(amplitude(1, T, (small, small), 1) ** 2)
    assert written[heavier][1] == written[lighter][1] > 0


def test_the_holes_board_runs_25_intervals_with_the_sign_holder_bounded(tmp_path, monkeypatch):  # type: ignore[no-untyped-def]
    """The sea with a hole (the law's seed with the origin's light taken by the one lay act, the form the board's own close uses for the two quanta's hole) and one electron quantum laid in the birth's own form, 25 intervals: electron pairs are born by the draw and every level of the holder of the sign stays below the former factor's write of that one electron in one interval, 16,427 (the runaway hand's 3-cube, 2026-10-24: 18,861 at the interval 1 under the former factor, 18 under the sentence; the hole's board 4,401,616 at 40 before, 3,774 after). On this head a born pair's two items are both laid at the Node (every face read before any write), its Wronskian there 0, so the laid quantum is the holder's source."""
    births: list[dict] = []  # type: ignore[type-arg]
    board = bare_board(
        tmp_path, monkeypatch, lambda line: births.append(line) if line.get("event") == "birth" else None
    )
    light, here = board.world.seed, board.mask(((0, 0, 0),))
    span = records.record_slice(board.families[light], 0)
    for number in range(span.start, span.stop):
        line = board.states[light].lines[number]
        change = (np.where(here, -line.now, 0), np.where(here, -line.before, 0))
        laid(board, light, number, change, None, None, here)
    names = [f.name for f in board.families]
    lighter = points_of(board)[-1]  # the lighter point, the least leg of the small den
    electron, den = names.index(lighter), board.families[names.index(lighter)].pair[1]
    laid_by_count(board, Item(electron, 1, ((1, 1, 1),), (den, den), sense=-1))
    largest = []
    for _ in range(25):
        board.step()
        largest.append(max(holder_rows(board)))
    assert births and all(
        c in points_of(board) for b in births for c in b["children"]
    )  # lists of the den's points born, one record per child (2026-10-24)
    assert 0 < max(largest) < 16_427


def test_the_lightest_point_of_the_circle_is_the_electrons_pair():
    """The extremal sentence (the owner's word of 2026-10-24, 09:1x UTC: the charged plane family at rest is the lightest point of the circle; ALGEBRA.md, The lightest point is the electron): s_min(den) by `lightest_point`, the least leg among `circle_points`, at the former den and at the one universe's enlarged den, whose file holds den alone (the same day's later word: no family row), the point the pages caption electron."""
    num, s = lightest_point(DEN)
    assert (num, s) == (53_567_757, 29_276) and num * num + s * s == DEN * DEN
    den = json.loads((EVENTS / "universe24" / "universe_universe24.json").read_text(encoding="utf-8"))[
        "integers"
    ]["den"]
    assert (
        den == 13_586_597 * 132_260_701 * 649_421 and lightest_point(den)[1] == 633_202_287_062_780_012
    )
    for d in (DEN, den, 1000, 65):
        assert lightest_point(d) == min(((n, s) for _v, n, s in circle_points(d)), key=lambda p: p[1])
    assert [lightest_point(d) for d in (1000, 5, 65, 25)] == [(960, 280), (4, 3), (63, 16), (24, 7)]
    refused("no prime 1 mod 4 divides it", lightest_point, 9)
