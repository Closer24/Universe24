"""The shear parts, three more held lines of a holder of the content (the owner's word of 2026-10-20, the held rows' own wave sector): the word `shear` in `held.sources` beside `tensions` gives the row three off-diagonal lines xy, yz, zx, sourced by the product of the Node's own two axis differences of its sources' records, D_a D_b at the same Node and the same interval (one Link's reach, no read at the reach sqrt 2), written by the same held write at the doubled wall 2 E_s W_c with one remainder per line and stepped by Rule3 as the tension lines are, read by no record (ALGEBRA.md, The tension, the off-diagonal booking G_ab met in the mean at the Link's two ends; The lattice's frame is read by gravity alone, and its carrier is a pair of Links, the three space pairs). Tested: the loader's refusals by name (the shear without the tensions, on the holder of the sign, a list the rule does not know), the lines and the walls the rule derives, the zero where the product is zero (a chain, every interval; a cube's mirror planes at the first write) with the sign of D_a D_b where it is written and the remainder identity, and the time line, the three tension lines, their remainders and every record unchanged bit for bit against the same world without the word (Newton's static sector untouched)."""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pytest

from event_universe import readings, records, world_files
from event_universe.lattice import Lattice
from event_universe.loader import universe
from event_universe.loader.derived import weight_of
from event_universe.records import Record
from event_universe.world_files import load_world
from tests.laws import UNIVERSE, refused

HELD = {"sources": ["form", "tensions"], "level_weight": 1, "write_weight": 1}


def shipped(shear: bool, level_weight: int = 1) -> dict:  # type: ignore[type-arg]
    """rule.json with gravity's sources ["form", "tensions"] and, with `shear`, the word beside them, at `level_weight`."""
    document = json.loads(UNIVERSE.read_text(encoding="utf-8"))
    gravity = next(row for row in document["families"] if row["name"] == "gravity")["held"]
    gravity["sources"] = ["form", "tensions"] + (["shear"] if shear else [])
    gravity["level_weight"] = level_weight
    return document


def board_of(
    folder: Path, shape: tuple[int, int, int], shear: bool, blob: np.ndarray
) -> tuple[Lattice, int, int]:
    """A world of no bodies on a board open on every axis of more than one Node, its universe beside it, the matter record laid by hand: now the blob, before now x num / den (a standing record at its band's rest rotation), the remainder as born."""
    name = f"u_{int(shear)}.json"
    (folder / name).write_text(json.dumps(shipped(shear)), encoding="utf-8")
    boundary = {
        axis: "periodic" if extent == 1 else "open" for axis, extent in zip("xyz", shape, strict=True)
    }
    world = dict(shape=list(shape), boundary=boundary, face_depth=1, intervals=10, universe=name)
    world.update(bodies=[], node_detectors=[])
    (path := folder / f"w_{int(shear)}_{len(shape)}.json").write_text(
        json.dumps(world), encoding="utf-8"
    )
    world_files.REPOSITORY_ROOT = folder
    board = Lattice(load_world(path))
    names = [family.name for family in board.families]
    matter, gravity = names.index("matter"), names.index("gravity")
    num, den = board.families[matter].pair
    line = board.states[matter].lines[0]
    now = blob.astype(line.now.dtype)
    board.states[matter].lines[0] = Record(
        now, ((blob * num) // den).astype(line.now.dtype), line.remainder
    )
    return board, matter, gravity


def blob_of(shape: tuple[int, int, int], amplitude: int = 2000, sigma: float = 1.3) -> np.ndarray:
    axes = [np.arange(n) - n // 2 for n in shape]
    x, y, z = np.meshgrid(*axes, indexing="ij")
    return np.rint(amplitude * np.exp(-(x * x + y * y + z * z) / (2 * sigma * sigma))).astype(np.int64)


def identical(a: Lattice, b: Lattice, index: int, lines: range) -> bool:
    """Whether the lines of one family stand bit for bit alike on two boards, with their write remainders where the family is held."""
    same = True
    for k in lines:
        x, y = a.states[index].lines[k], b.states[index].lines[k]
        same &= (
            np.array_equal(x.now, y.now)
            and np.array_equal(x.before, y.before)
            and np.array_equal(x.remainder, y.remainder)
        )
        if a.states[index].write_remainders:
            same &= np.array_equal(
                a.states[index].write_remainders[k], b.states[index].write_remainders[k]
            )
    return same


def test_the_shear_is_declared_beside_the_tensions_and_refused_by_name_elsewhere():
    """The loader: `shear` without `tensions` refused naming the row (the form alone, the Wronskian), a list the rule does not know refused as before, and the admitted lists give 1 + 3 + 3 lines (and 1 + 3 + 3 + 3 with the flux), the row's flag set and the shear lines the last three."""
    refused(
        "declares the shear without the tensions",
        universe.shape_of,
        {"held": {**HELD, "sources": ["form", "shear"]}},
        "r",
    )
    refused(
        "declares the shear without the tensions",
        universe.shape_of,
        {"held": {**HELD, "sources": ["wronskian", "shear"]}},
        "r",
    )
    refused(
        "held.sources is one of",
        universe.shape_of,
        {"held": {**HELD, "sources": ["shear", "form", "tensions"]}},
        "r",
    )
    assert universe.shape_of({"held": {**HELD, "sources": ["form", "tensions", "shear"]}}, "r") == (
        7,
        1,
        False,
        False,
        False,
    )
    assert universe.shape_of(
        {"held": {**HELD, "sources": ["form", "tensions", "flux", "shear"]}}, "r"
    ) == (10, 1, False, False, False)
    assert universe.shape_of({"held": HELD}, "r") == (4, 1, False, False, False)
    integers, families = universe.universe_of(shipped(True))
    gravity = next(family for family in families if family.name == "gravity")
    assert (
        gravity.off_diagonal
        and gravity.lines == 7
        and list(gravity.off_diagonal_lines) == [4, 5, 6]
        and gravity.axes
    )
    plain = next(
        family for family in universe.universe_of(shipped(False))[1] if family.name == "gravity"
    )
    assert not plain.off_diagonal and plain.lines == 4 and list(plain.off_diagonal_lines) == []
    with pytest.raises(ValueError, match="declares the shear without the tensions"):
        document = shipped(False)
        next(row for row in document["families"] if row["name"] == "binding")["held"]["sources"] = [
            "form",
            "shear",
        ]
        universe.universe_of(document)


def test_the_off_diagonal_lines_are_zero_where_the_product_is_zero_and_the_diagonal_stands_bit_for_bit(
    tmp_path,
):
    """On a chain every D_a D_b is 0 and the three shear lines stay 0 with their remainders at the half wall through ten intervals; on an open 7-cube the first write lands 0 on the blob's two mirror planes (the product 0 there), the sign of D_a D_b where it lands, and numerator + r_in = gain x wall + r_out at every Node with one remainder per line at the doubled wall 2 E_s W_c; and the time line, the three tension lines, their remainders, the matter record and every other family stand bit for bit as on the same board without the word."""
    for shape in ((16, 1, 1), (7, 7, 7)):
        blob = blob_of(shape)
        with_shear, matter, gravity = board_of(tmp_path, shape, True, blob)
        without, _matter, _gravity = board_of(tmp_path, shape, False, blob)
        family, walls = with_shear.families[gravity], with_shear.walls(gravity)
        assert family.lines == 7 and without.families[gravity].lines == 4
        assert walls[4:] == (2 * walls[1],) * 3 and len(with_shear.states[gravity].write_remainders) == 7
        weight = with_shear.families[matter].pair[0]
        parts = readings.off_diagonals_of(weight, with_shear.lines_of(matter, 0), with_shear.wrap)
        rulers, write, gamma = (
            with_shear.rulers(1),
            with_shear.writes[gravity],
            with_shear.world.node_clock,
        )
        numerators = []
        for k in range(3):
            total = 0
            for source in rulers:
                part = readings.off_diagonals_of(
                    with_shear.families[source[0]].pair[0], with_shear.lines_of(*source), with_shear.wrap
                )[k]
                scaled = records.rulers_write_factor(part, rulers[source], gamma, 2)
                total = (
                    total
                    + weight_of(gravity, with_shear.families[source[0]])
                    * write.factors[source[0]]
                    * scaled
                )
            numerators.append(np.asarray(family.write * total, dtype=object))
        carried = [r.copy().astype(object) for r in with_shear.states[gravity].write_remainders[4:]]
        for interval in range(1, 11):
            with_shear.step()
            without.step()
            state = with_shear.states[gravity]
            if interval == 1:
                for k in range(3):
                    level, wall = state.lines[4 + k].now, walls[4 + k]
                    after = state.write_remainders[4 + k].astype(object)
                    assert np.array_equal(
                        numerators[k] + carried[k], level.astype(object) * wall + after
                    )
                    assert int(after.min()) >= 0 and int(after.max()) < wall
                    zero = np.asarray(parts[k]) == 0
                    assert not level[zero].any()
                    written = level != 0
                    assert np.array_equal(
                        np.sign(level[written]), np.sign(np.asarray(parts[k])[written])
                    )
                    if (
                        shape[1] > 1
                    ):  # the pair's two mirror planes through the blob's centre: D_a or D_b is 0 there
                        assert written.any(), "the cube's blob writes the shear off its mirror planes"
                        centre = shape[0] // 2
                        for axis in ((0, 1), (1, 2), (2, 0))[k]:
                            assert not np.take(level, centre, axis=axis).any()
            if (
                shape[1] == 1
            ):  # the chain: every product 0, every shear line 0 and its remainder at the half wall
                for k in range(3):
                    assert not state.lines[4 + k].now.any() and not state.lines[4 + k].before.any()
                    assert bool((state.write_remainders[4 + k] == walls[4 + k] // 2).all())
            assert identical(with_shear, without, gravity, range(4))
            for index in range(len(with_shear.families)):
                if index != gravity:
                    assert identical(with_shear, without, index, range(len(without.states[index].lines)))
        if shape[1] > 1:
            assert any(with_shear.states[gravity].lines[k].now.any() for k in (4, 5, 6))
