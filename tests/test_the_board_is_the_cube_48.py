"""The board is the cube's 48 (the Boss's covariance test, 2026-10-24, on the bound-click hand's measurement; ALGEBRA.md, The cube's symmetry, the direction: Rule3 commutes with the cube's 48, the reflections included; The click's read of the board, the owner's rule that the click reads the Node and its six neighbours only and nothing of the board's labels): every act of the interval, the step, the held writes, the swap, the board's own close and its draw by the digits, carries the 48 rotations and reflections of the cube about the origin, so (a) a seed invariant under the 48 runs invariant under the 48 at every interval, every level, remainder, write remainder and phase line (the orbits whole), and (b) a seed transformed by one rotation and one reflection before the run gives the transformed run, interval by interval, bit for bit. The 48 are the signed permutation matrices generated from two of them found by the closure, no table declared (`cube_48`); a state is carried by a signed permutation as the law's lines are: a scalar line permuted over the Nodes about the origin, a holder's axis lines permuted over the axes, the sign holder's odd lines with the axis's sign and the complement w - r of their remainders (the carried division's symmetry under negation, as the swap complements), the phase lines of the Node's +a Link carried to the image Link, read from the Node it points back from where the axis flips, the sine kept and the count negated (`carried`; every rule the one under which the hole seed's run stands invariant through its nine intervals before any draw, measured 2026-10-24). On the engine with the ordered two-Link read of the digits (the mixed-radix number in the fixed Port order) the test FAILS by name, measured 2026-10-24 on the tests' small universe (den 1,021) under the hole the Node's own level before: (a) the hole-seed 3-cube stands invariant through 20 intervals (its draws fall at the origin alone, a trivial orbit); the sea plus one quantum at the origin on the 3-cube stands invariant through 3 and breaks at 4 under 40 of the 47 elements, the whether drawn at the corners' orbit of 8 and met at 4 of them, (1, 1, 1), (1, 1, 2), (2, 2, 1), (2, 2, 2); the hole-seed 5-cube breaks at 4 under 40 of 47, the edges' orbit of 12 born at 8; (b) the sea plus one at (1, 0, 0) against its image under the 90-degree rotation about z and under the reflection x -> -x: equal through 3, apart at 4 at the births by the draw. It passes once the digits' read is one-Link and symmetric (the builder's sentence); it is not to be skipped or weakened."""

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
from event_universe.world_files import load_world
from tests.laws_universe import sea_plus_one, small_universe

Matrix = np.ndarray


def signed_permutations() -> list[Matrix]:
    """Every signed permutation of the three axes, e_a -> s_a e_pi(a)."""
    found = []
    for perm in itertools.permutations(range(AXES)):
        for signs in itertools.product((1, -1), repeat=AXES):
            m = np.zeros((AXES, AXES), dtype=int)
            for a in range(AXES):
                m[perm[a], a] = signs[a]
            found.append(m)
    return found


def closure(generators: list[Matrix]) -> list[Matrix]:
    """The group the generators make under the product, from the identity."""
    identity = np.eye(AXES, dtype=int)
    found, frontier = {identity.tobytes(): identity}, [identity]
    while frontier:
        new = []
        for g in frontier:
            for h in generators:
                m = h @ g
                if m.tobytes() not in found:
                    found[m.tobytes()] = m
                    new.append(m)
        frontier = new
    return list(found.values())


def cube_48() -> list[Matrix]:
    """The cube's 48 from the first two signed permutations whose closure is the whole, found and not declared."""
    everything = signed_permutations()
    for first, second in itertools.product(everything, everything):
        group = closure([first, second])
        if len(group) == 48:
            return group
    raise AssertionError("no two signed permutations generate the 48")


def axis_map(m: Matrix) -> tuple[list[int], list[int]]:
    """e_a -> s_a e_pi(a): pi and s per axis."""
    pi, s = [], []
    for a in range(AXES):
        b = int(np.nonzero(m[:, a])[0][0])
        pi.append(b)
        s.append(int(m[b, a]))
    return pi, s


def carried(board: Lattice, m: Matrix) -> list[Any]:
    """Every family's state carried by the signed permutation `m` about the origin (the module's sentence): per family its lines as (now, before, remainder), its write remainders and its phase rows."""
    shape, side = board.shape, board.shape[0]
    nodes = np.array(list(np.ndindex(*shape)))
    images = np.mod(nodes @ m.T, side)
    pi, s = axis_map(m)

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

    def complemented(remainder: Any, wall: Any) -> np.ndarray:
        r = np.asarray(remainder, dtype=object)
        return np.where(r == 0, 0, np.asarray(wall, dtype=object) - r)

    found = []
    for index, state in enumerate(board.states):
        family = board.families[index]
        lines: list[Any] = [None] * len(state.lines)
        writes: list[Any] = [None] * len(state.write_remainders)
        if not family.held:  # a family of quanta: scalar lines
            for k, line in enumerate(state.lines):
                lines[k] = tuple(moved(v) for v in (line.now, line.before, line.remainder))
        else:  # a holder: per row the time line, then the axis lines in triples
            rows, per_row = (
                registry.records_of(family, state.lines),
                family.width,
            )  # the live rows (the point rows born at the first birth, 2026-10-24)
            wall = wall_of(family.pair[1], board.world.node_clock, board.unit)
            divided = records.divided_walls(family, board.fixed_walls[index], board.world.node_clock)
            for row in range(rows):
                base = row * per_row
                lines[base] = tuple(moved(v) for v in records_of(state.lines[base]))
                writes[base] = moved(state.write_remainders[base])
                for triple in range((per_row - 1) // AXES):
                    for a in range(AXES):
                        k, target = base + 1 + triple * AXES + a, base + 1 + triple * AXES + pi[a]
                        now, before, remainder = (moved(v) for v in records_of(state.lines[k]))
                        write = moved(state.write_remainders[k])
                        if family.wronskian and s[a] < 0:  # an odd line: a vector's component
                            now, before = -now, -before
                            remainder = complemented(remainder, wall)
                            write = complemented(write, divided[k])
                        lines[target], writes[target] = (now, before, remainder), write
        phases = []
        for row in state.phases:
            out: list[Any] = [None] * len(row)
            if not row:  # the free row carries no phase line
                phases.append(out)
                continue
            for a in range(AXES):
                b, shift = pi[a], None if s[a] > 0 else pi[a]
                cosine, sine, count = row[2 * a], row[2 * a + 1], row[2 * AXES + a]
                out[2 * b] = tuple(moved(v, shift) for v in records_of(cosine))
                out[2 * b + 1] = tuple(moved(v, shift) for v in records_of(sine))
                now, before, remainder = (moved(v, shift) for v in records_of(count))
                out[2 * AXES + b] = (-now, -before, remainder) if s[a] < 0 else (now, before, remainder)
            out[-1] = tuple(moved(v) for v in records_of(row[-1]))
            phases.append(out)
        found.append((lines, writes, phases))
    return found


def records_of(line: records.Record) -> tuple[Any, Any, Any]:
    return line.now, line.before, line.remainder


def plain(board: Lattice) -> list[Any]:
    return [
        (
            [tuple(np.asarray(v, dtype=object) for v in records_of(line)) for line in state.lines],
            [np.asarray(w, dtype=object) for w in state.write_remainders],
            [
                [tuple(np.asarray(v, dtype=object) for v in records_of(line)) for line in row]
                for row in state.phases
            ],
        )
        for state in board.states
    ]


def same(a: list[Any], b: list[Any]) -> bool:
    """Two carried states equal in every line, write remainder and phase line, bit for bit."""
    for (la, wa, pa), (lb, wb, pb) in zip(a, b, strict=True):
        if not all(
            np.array_equal(u, v) for x, y in zip(la, lb, strict=True) for u, v in zip(x, y, strict=True)
        ):
            return False
        if not all(np.array_equal(u, v) for u, v in zip(wa, wb, strict=True)):
            return False
        for ra, rb in zip(pa, pb, strict=True):
            if not all(
                np.array_equal(u, v)
                for x, y in zip(ra, rb, strict=True)
                for u, v in zip(x, y, strict=True)
            ):
                return False
    return True


def board_of(tmp_path, monkeypatch, side, intervals, seeder):  # type: ignore[no-untyped-def]
    """The tests' small universe on the bare cube of `side`, seeded by the engine's own hole seed or by `seeder` in its place."""
    monkeypatch.setattr(world_files, "REPOSITORY_ROOT", tmp_path)
    small_universe(tmp_path)
    (tmp_path / "w.json").write_text(
        json.dumps({"universe": "u.json", "shape": [side] * 3, "intervals": intervals})
    )
    if seeder is not None:
        monkeypatch.setattr(seed, "uniform_seed", seeder)
    lines: list[dict[str, Any]] = []
    return Lattice(load_world(tmp_path / "w.json"), output=lines.append), lines


def test_two_signed_permutations_generate_the_48_and_every_element_is_one() -> None:
    """The closure of the two found generators is the 48 signed permutation matrices of the three axes, each orthogonal with the determinant 1 or -1, 24 of each."""
    group = cube_48()
    assert len(group) == 48 and len({m.tobytes() for m in group}) == 48
    assert all(np.array_equal(m @ m.T, np.eye(AXES, dtype=int)) for m in group)
    assert sorted(int(round(np.linalg.det(m))) for m in group) == [-1] * 24 + [1] * 24


@pytest.mark.parametrize(
    ("side", "seeder", "intervals"), [(3, None, 20), (3, sea_plus_one((0, 0, 0)), 8), (5, None, 6)]
)
def test_a_seed_invariant_under_the_48_runs_invariant_under_the_48(
    tmp_path, monkeypatch, side, seeder, intervals
):  # type: ignore[no-untyped-def]
    """(a) The hole seed on the 3-cube and the 5-cube and the sea plus one quantum at the origin on the 3-cube, every one invariant under the 48 about the origin, run invariant under every one of the 47 non-trivial elements at every interval: the orbits whole in every level, remainder, write remainder and phase line (the module's sentence names where the ordered read breaks it)."""
    board, lines = board_of(tmp_path, monkeypatch, side, intervals, seeder)
    group = [m for m in cube_48() if not np.array_equal(m, np.eye(AXES, dtype=int))]
    for _ in range(intervals):
        board.step()
        state = plain(board)
        broken = [m.tolist() for m in group if not same(carried(board, m), state)]
        births = [
            tuple(line["nodes"][0])
            for line in lines
            if line.get("event") == "birth" and line["interval"] == board.interval
        ]
        assert broken == [], (board.interval, len(broken), births)
    assert any(
        line.get("event") in ("birth", "refused") for line in lines
    )  # a close reached: born, or refused by the take


@pytest.mark.parametrize(
    "m",
    [np.array([[0, -1, 0], [1, 0, 0], [0, 0, 1]]), np.diag([-1, 1, 1])],
    ids=["rotation", "reflection"],
)
def test_a_seed_transformed_before_the_run_gives_the_transformed_run(tmp_path, monkeypatch, m):  # type: ignore[no-untyped-def]
    """(b) The sea plus one quantum at (1, 0, 0) and the same seed carried by the 90-degree rotation about z, then by the reflection x -> -x, before the run: the run of the carried seed is the carried run of the other, interval by interval, bit for bit, through eight intervals."""
    at = (1, 0, 0)
    image = tuple(int(v) for v in np.mod(m @ np.array(at), 3))
    assert image != at
    board, lines = board_of(tmp_path, monkeypatch, 3, 8, sea_plus_one(at))
    (tmp_path / "other").mkdir()
    other, _ = board_of(tmp_path / "other", monkeypatch, 3, 8, sea_plus_one(image))
    assert same(carried(board, m), plain(other)) is True
    for _ in range(8):
        board.step()
        other.step()
        births = [
            tuple(line["nodes"][0])
            for line in lines
            if line.get("event") == "birth" and line["interval"] == board.interval
        ]
        equal = same(carried(board, m), plain(other))
        assert equal, (board.interval, births)
    assert any(
        line.get("event") in ("birth", "refused") for line in lines
    )  # a close reached: born, or refused by the take
