"""The board is the cube's 48 (the Boss's covariance test, 2026-10-24, on the bound-click hand's measurement; ALGEBRA.md, The cube's symmetry, the direction: Rule3 commutes with the cube's 48, the reflections included; The click's read of the board, the owner's rule that the click reads the Node and its six neighbours only and nothing of the board's labels): every act of the interval, the step, the held writes, the swap, the board's own close and its draw by the digits, carries the 48 rotations and reflections of the cube about the origin, so (a) a seed invariant under the 48 runs invariant under the 48 at every interval, every level, remainder, write remainder and phase line (the orbits whole), and (b) a seed transformed by one rotation and one reflection before the run gives the transformed run, interval by interval, bit for bit. The 48 are the signed permutation matrices generated from two of them found by the closure, no table declared (`cube_48`); a state is carried by a signed permutation as the law's lines are: a scalar line permuted over the Nodes about the origin, a holder's axis lines permuted over the axes, the sign holder's odd lines with the axis's sign and their remainders reflected about their own lay, the phase lines of the Node's +a Link carried to the image Link, read from the Node it points back from where the axis flips, the sine kept and the count's sign by the Link's two frames (`carried`). The turned Node's gauge (2026-10-24, the mirror clause's next derivation, derived on paper and measured on the gapped board): the law's mirror of an odd line is records.complement, the levels negated and the remainder w - 1 - r, the exact symmetry of the carried division, and the swap at the top complements by the same; the test's carry reflects the remainder about the half wall w/2, (w - r) mod w, since the seed lays every odd line there and w - 1 - w/2 is w/2 - 1 at an even wall; two reflections half a unit apart compose to a translation by one unit, so at a turned Node the former reading, the test's carry at the lay's gauge alone, read the swap's one-unit move as two. The swap carries the gauge with it: after an odd count of a Node's turns since the row's birth the odd line's remainder is reflected about w/2 - 1, (w - 2 - r) mod w, the swap's conjugate of the lay's gauge, and after an even count about w/2; the gauge is a row's from its birth, every born row laid at the half wall after the interval's swap (`turns_of`). The count of a Link is K_i - s K_j with s the two ends' frame sign (node.phase_counts): under the exchange of its ends it goes to -s times itself, negated where both ends share one frame and kept where one end is turned and the other not; the former reading negated it on every Link. Measured 2026-10-24 on the tests' small universe (den 1,021) under the engine's own gapped pair: the hole-seed 3-cube turns at the origin at interval 1, its faces at 2, births at 4, and runs invariant under the 47 non-trivial elements through the births and the waves of turns; the sea plus one turns at 2 and births at 5; the two negative controls below assert the exact failure of each former reading. On the engine with the ordered two-Link read of the digits the test FAILS by name (measured 2026-10-24, the births by the draw at interval 4 under 40 of the 47 elements); it passes once the digits' read is one-Link and symmetric (the builder's sentence); it is not to be skipped or weakened."""

from __future__ import annotations

import itertools
import json
from typing import Any

import numpy as np
import pytest

from event_universe import records, registry, seed, world_files
from event_universe.core.ports import AXES
from event_universe.core.rule3 import wall_of
from event_universe.lattice import Lattice
from event_universe.loader import universe
from event_universe.world_files import load_world
from tests.laws_universe import sea_plus_one, small_universe

Matrix = np.ndarray
IDENTITY = np.eye(AXES, dtype=int)
Turns = dict[int, list[np.ndarray]]  # per held family the turn parity of every live row at every Node


def signed_permutations() -> list[Matrix]:
    """Every signed permutation of the three axes, e_a -> s_a e_pi(a)."""
    axes = range(AXES)
    return [
        np.array([[s[a] if pi[a] == b else 0 for a in axes] for b in axes])
        for pi in itertools.permutations(axes)
        for s in itertools.product((1, -1), repeat=AXES)
    ]


def closure(generators: list[Matrix]) -> list[Matrix]:
    """The group the generators make under the product, from the identity."""
    found, frontier = {IDENTITY.tobytes(): IDENTITY}, [IDENTITY]
    while frontier:
        frontier = [
            found.setdefault(m.tobytes(), m)
            for g in frontier
            for h in generators
            if (m := h @ g).tobytes() not in found
        ]
    return list(found.values())


def cube_48() -> list[Matrix]:
    """The cube's 48 from the first two signed permutations whose closure is the whole, found and not declared."""
    everything = signed_permutations()
    for first, second in itertools.product(everything, everything):
        group = closure([first, second])
        if len(group) == 48:
            return group
    raise AssertionError("no two signed permutations generate the 48")


def negating() -> list[Matrix]:
    """The 42 elements that negate an axis; the other 5 non-trivial ones are pure permutations and complement nothing."""
    return [m for m in cube_48() if any(x < 0 for x in axis_map(m)[1])]


def axis_map(m: Matrix) -> tuple[list[int], list[int]]:
    """e_a -> s_a e_pi(a): pi and s per axis."""
    pi = [int(np.nonzero(m[:, a])[0][0]) for a in range(AXES)]
    return pi, [int(m[pi[a], a]) for a in range(AXES)]


def turns_of(board: Lattice, before: Turns | None) -> Turns:
    """The turn parity of every held family's rows at every Node since the row's birth (the module's sentence: the gauge is a row's from its birth): per held family one mask per live row, flipped where the interval's swap turned the Node (`Lattice.turned`), a row born this interval entering even, its remainders laid at the half wall after the swap; `before` the parities at the interval's start, None at the start of the run, every row even."""
    found, turned = {}, np.asarray(board.turned, dtype=bool)
    for index, family in enumerate(board.families):
        if family.held:
            rows = registry.records_of(family, board.states[index].lines)
            kept = [] if before is None else [k ^ turned for k in before[index]]
            found[index] = kept + [np.zeros(board.shape, dtype=bool)] * (rows - len(kept))
    return found


def carried(board: Lattice, m: Matrix, turns: Turns | None = None, former: str = "") -> list[Any]:
    """Every family's state carried by the signed permutation `m` about the origin (the module's sentence): per family its lines as (now, before, remainder), its write remainders and its phase rows; `turns` the rows' turn parities (`turns_of`, every row even where None); `former` names a former reading for the negative controls, "node" the gauge per Node from the start (the free row's parity for every row), "link" the count negated on every Link."""
    shape, side = board.shape, board.shape[0]
    nodes = np.array(list(np.ndindex(*shape)))
    images = np.mod(nodes @ m.T, side)
    pi, s = axis_map(m)
    even = np.zeros(shape, dtype=bool)

    def moved(array: Any, shift: int | None = None) -> np.ndarray:
        a = np.asarray(array, dtype=object)
        target = images.copy()
        if (
            shift is not None
        ):  # the +a Link carried to a Link pointing back: the Node it points back from
            target[:, shift] = np.mod(target[:, shift] - 1, side)
        out = np.empty_like(a)
        out[tuple(target.T)] = a[tuple(nodes.T)]
        return out

    def complemented(remainder: Any, wall: Any, odd: np.ndarray) -> np.ndarray:
        """A negated line's remainder reflected about its own lay: about the half wall, (w - r) mod w, where the row's count of the Node's turns is even, and about w/2 - 1, (w - 2 - r) mod w, where odd (the module's sentence: the swap's conjugate of the lay's gauge)."""
        r, w = np.asarray(remainder, dtype=object), np.asarray(wall, dtype=object)
        return np.asarray(np.mod(w - 2 * np.asarray(odd, dtype=object) - r, w), dtype=object)

    found = []
    for index, state in enumerate(board.states):
        family = board.families[index]
        lines: list[Any] = [None] * len(state.lines)
        writes: list[Any] = [None] * len(state.write_remainders)
        if not family.held:  # a family of quanta: scalar lines
            for k, line in enumerate(state.lines):
                lines[k] = tuple(moved(v) for v in records_of(line))
        else:  # a holder: per row the time line, then the axis lines in triples
            rows, per_row = registry.records_of(family, state.lines), family.width
            wall = wall_of(family.pair[1], board.world.node_clock, board.unit)
            divided = records.divided_walls(family, board.fixed_walls[index], board.world.node_clock)
            for row in range(rows):
                base = row * per_row
                odd = turns[index][0 if former == "node" else row] if turns else even
                lines[base] = tuple(moved(v) for v in records_of(state.lines[base]))
                writes[base] = moved(state.write_remainders[base])
                for triple in range((per_row - 1) // AXES):
                    for a in range(AXES):
                        k, target = base + 1 + triple * AXES + a, base + 1 + triple * AXES + pi[a]
                        now, before, remainder = (moved(v) for v in records_of(state.lines[k]))
                        write = moved(state.write_remainders[k])
                        if family.wronskian and s[a] < 0:  # an odd line: a vector's component
                            now, before = -now, -before
                            remainder = moved(complemented(state.lines[k].remainder, wall, odd))
                            write = moved(complemented(state.write_remainders[k], divided[k], odd))
                        lines[target], writes[target] = (now, before, remainder), write
        phases = []
        for row in state.phases:
            out: list[Any] = [None] * len(row)
            if not row:  # the free row carries no phase line
                phases.append(out)
                continue
            frame = np.asarray(
                row[-1].remainder, dtype=object
            )  # the row's frame, the remainder at the wall 2
            for a in range(AXES):
                b, shift = pi[a], None if s[a] > 0 else pi[a]
                out[2 * b] = tuple(moved(v, shift) for v in records_of(row[2 * a]))
                out[2 * b + 1] = tuple(moved(v, shift) for v in records_of(row[2 * a + 1]))
                count, sign = row[2 * AXES + a], 1
                if (
                    s[a] < 0
                ):  # the count K_i - s K_(i+a) goes to -s times itself under the exchange of its ends
                    shared = (frame == np.roll(frame, -1, axis=a)) | (former == "link")
                    sign = np.where(shared, -1, 1).astype(object)
                levels = (
                    moved(np.asarray(v, dtype=object) * sign, shift) for v in (count.now, count.before)
                )
                out[2 * AXES + b] = (*levels, moved(count.remainder, shift))
            out[-1] = tuple(moved(v) for v in records_of(row[-1]))
            phases.append(out)
        found.append((lines, writes, phases))
    return found


def records_of(line: records.Record) -> tuple[Any, Any, Any]:
    return line.now, line.before, line.remainder


def apart(
    a: Any, b: Any, path: tuple[int, ...] = ()
) -> list[tuple[tuple[int, ...], tuple[int, ...], int]]:
    """Every entry where two carried states differ, bit for bit: the path (the family, 0 lines / 1 writes / 2 phases, the line, the part), the Node and the units, `a` less `b`; empty where the two are the same."""
    if isinstance(a, list | tuple):
        return [d for i, (x, y) in enumerate(zip(a, b, strict=True)) for d in apart(x, y, (*path, i))]
    u, v = np.asarray(a, dtype=object), np.asarray(b, dtype=object)
    return [
        (path, tuple(int(i) for i in at), int(u[tuple(at)] - v[tuple(at)])) for at in np.argwhere(u != v)
    ]


def births_at(lines: list[dict[str, Any]], at: int) -> list[tuple[int, ...]]:
    return [tuple(x["nodes"][0]) for x in lines if x.get("event") == "birth" and x["interval"] == at]


def board_of(tmp_path, monkeypatch, side, intervals, seeder, gapped=False):  # type: ignore[no-untyped-def]
    """The tests' small universe on the bare cube of `side`, seeded by the engine's own hole seed or by `seeder` in its place, under the engine's own gapped pair where `gapped` and the massless holder by name otherwise."""
    monkeypatch.setattr(world_files, "REPOSITORY_ROOT", tmp_path)
    if not gapped:
        monkeypatch.setattr(universe, "volume_pair", lambda den, gamma: (den, den))
    small_universe(tmp_path)
    world = {"universe": "u.json", "shape": [side] * 3, "intervals": intervals}
    (tmp_path / "w.json").write_text(json.dumps(world))
    if seeder is not None:
        monkeypatch.setattr(seed, "uniform_seed", seeder)
    lines: list[dict[str, Any]] = []
    return Lattice(load_world(tmp_path / "w.json"), output=lines.append), lines


def test_two_signed_permutations_generate_the_48_and_every_element_is_one() -> None:
    """The closure of the two found generators is the 48 signed permutation matrices of the three axes, each orthogonal with the determinant 1 or -1, 24 of each; 42 of them negate an axis."""
    group = cube_48()
    assert len(group) == 48 and len({m.tobytes() for m in group}) == 48
    assert all(np.array_equal(m @ m.T, IDENTITY) for m in group)
    assert sorted(int(round(np.linalg.det(m))) for m in group) == [-1] * 24 + [1] * 24
    assert len(negating()) == 42


@pytest.mark.parametrize(
    ("side", "seeder", "intervals", "gapped"),
    [
        (3, None, 20, False),
        (3, sea_plus_one((0, 0, 0)), 8, False),
        (5, None, 6, False),
        (3, None, 12, True),
        (3, sea_plus_one((0, 0, 0)), 8, True),
    ],
)
def test_a_seed_invariant_under_the_48_runs_invariant_under_the_48(
    tmp_path, monkeypatch, side, seeder, intervals, gapped
):  # type: ignore[no-untyped-def]
    """(a) The hole seed on the 3-cube and the 5-cube and the sea plus one quantum at the origin on the 3-cube, every one invariant under the 48 about the origin, run invariant under every one of the 47 non-trivial elements at every interval: the orbits whole in every level, remainder, write remainder and phase line; under the massless holder by name, and under the engine's own gapped pair through the first turn, the births and the waves of turns, the carry's gauge the row's own (the module's sentence names where the ordered read and the former carry break it)."""
    board, lines = board_of(tmp_path, monkeypatch, side, intervals, seeder, gapped)
    group, turns = [m for m in cube_48() if not np.array_equal(m, IDENTITY)], turns_of(board, None)
    for _ in range(intervals):
        board.step()
        turns = turns_of(board, turns)
        state = carried(board, IDENTITY)
        broken = [m.tolist() for m in group if apart(carried(board, m, turns), state)]
        assert broken == [], (board.interval, len(broken), births_at(lines, board.interval))
    assert any(line.get("event") in ("birth", "refused") for line in lines)  # a close reached
    assert bool(board.swaps) is gapped  # the gapped time line alone turns a board


@pytest.mark.parametrize("gapped", [False, True], ids=["massless", "gapped"])
@pytest.mark.parametrize(
    "m",
    [np.array([[0, -1, 0], [1, 0, 0], [0, 0, 1]]), np.diag([-1, 1, 1])],
    ids=["rotation", "reflection"],
)
def test_a_seed_transformed_before_the_run_gives_the_transformed_run(tmp_path, monkeypatch, m, gapped):  # type: ignore[no-untyped-def]
    """(b) The sea plus one quantum at (1, 0, 0) and the same seed carried by the 90-degree rotation about z, then by the reflection x -> -x, before the run: the run of the carried seed is the carried run of the other, interval by interval, bit for bit, through eight intervals, under the massless holder and under the engine's own gapped pair (the first turn at interval 2 at the quantum's Node, the births at 5), the turns' parities carried with the Nodes."""
    at = (1, 0, 0)
    image = tuple(int(v) for v in np.mod(m @ np.array(at), 3))
    assert image != at
    board, lines = board_of(tmp_path, monkeypatch, 3, 8, sea_plus_one(at), gapped)
    (tmp_path / "other").mkdir()
    other, _ = board_of(tmp_path / "other", monkeypatch, 3, 8, sea_plus_one(image), gapped)
    turns = turns_of(board, None)
    assert apart(carried(board, m, turns), carried(other, IDENTITY)) == []
    for _ in range(8):
        board.step()
        other.step()
        turns = turns_of(board, turns)
        found = apart(carried(board, m, turns), carried(other, IDENTITY))
        assert found == [], (board.interval, births_at(lines, board.interval), found[:3])
    assert any(line.get("event") in ("birth", "refused") for line in lines)  # a close reached
    assert bool(board.swaps) is gapped


def test_the_gauge_per_node_from_the_start_breaks_the_born_rows_at_their_birth_by_two_units(
    tmp_path, monkeypatch
):  # type: ignore[no-untyped-def]
    """The negative control of the first clause (2026-10-24): carried with the gauge per Node from the start in place of the row's from its birth, the hole seed under the gapped pair stands invariant until its first birth, where every one of the 42 negating elements parts from the run on the born rows' odd lines alone, their remainders and write remainders, by exactly two units, at exactly the Nodes the swap has turned an odd number of times: the births lay every born row at the half wall after the interval's swap, so a gauge older than the row reads the lay one unit off and the carry two."""
    board, lines = board_of(tmp_path, monkeypatch, 3, 6, None, True)
    sign = next(i for i, f in enumerate(board.families) if f.held and f.wronskian)
    turns = turns_of(board, None)
    for _ in range(6):
        board.step()
        turns = turns_of(board, turns)
        state = carried(board, IDENTITY)
        found = [apart(carried(board, m, turns, "node"), state) for m in negating()]
        if not births_at(lines, board.interval):
            assert all(not f for f in found), (
                board.interval
            )  # every row the free row's age: no difference
            continue
        odd = {tuple(int(i) for i in at) for at in np.argwhere(turns[sign][0])}
        for differences in found:
            assert differences and {node for _, node, _ in differences} == odd, (
                board.interval,
                len(odd),
            )
            assert all(
                path[0] == sign
                and path[1] < 2
                and path[2] >= board.families[sign].width
                and abs(units) == 2
                for path, _, units in differences
            ), differences[:3]
        return
    raise AssertionError("no birth within six intervals")


def test_the_count_negated_on_every_link_breaks_the_count_lines_where_a_turned_node_has_an_unturned_neighbour(
    tmp_path, monkeypatch
):  # type: ignore[no-untyped-def]
    """The negative control of the second clause (2026-10-24): carried with the former phase rule, the count negated on every Link, the hole seed under the gapped pair parts from the run under the 42 negating elements on the count lines alone, by twice the count (an even number of units and never 0), and only at intervals where some Link of a born row joins a turned Node to an unturned one (its two ends' frames apart); where every Link's ends share one frame the former rule and the law's agree, so the run is met broken and then whole again."""
    board, _ = board_of(tmp_path, monkeypatch, 3, 8, None, True)
    turns, broken = turns_of(board, None), []
    for _ in range(8):
        board.step()
        turns = turns_of(board, turns)
        state = carried(board, IDENTITY)
        frames = [
            np.asarray(row[-1].remainder, dtype=object) for s in board.states for row in s.phases if row
        ]
        mixed = any((f != np.roll(f, -1, axis=a)).any() for f in frames for a in range(AXES))
        found = [d for m in negating() for d in apart(carried(board, m, turns, "link"), state)]
        assert not found or mixed, (board.interval, found[:3])
        assert all(
            path[1] == 2 and 2 * AXES <= path[3] < 3 * AXES and units % 2 == 0 and units != 0
            for path, _, units in found
        ), found[:3]
        broken.append(bool(found))
    assert True in broken and broken.index(True) < broken.index(False, broken.index(True))
