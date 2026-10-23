"""The chain world as a test (the owner's word of 2026-10-19, "write it as a test"; the click's plan, the conservation section's blinds B1 to B5 and B7 with C1's and C5's lines; the folder examples/events/chain holds the declaration and the lays as the test's fixtures, its blinds asserted here on every run of tools/check.py and never read from a run's table): one law-quantum of light at k = pi / 4 on two bodies of three Nodes along a chain of 96 with receding faces, each body taking the light into e over a window of 48 from the first lit interval and giving it back as a source in time at the lifetime 48; the six worlds the chain under the six signed permutations that carry a chain to a chain; the seventh the detuned packet of the window's length. Rule3 plus the one act conserve the count, the form, the momentum, the inverse and the 48, with no world-specific code and nothing at the Node. The first run's findings are named in the folder's document."""

import json
import time

import numpy as np

from event_universe.lattice import Lattice
from event_universe.world_files import load_world
from tests.laws import BACK, EVENTS
from tests.laws_content import TWO_ATOMS, content_copy
from tests.laws_read import load_shipped

CHAIN = EVENTS / "chain"
DESIGN = json.loads((CHAIN / "design.json").read_text(encoding="utf-8"))
AXES = "xyz"
RUNS: dict[str, tuple[list[dict], dict[tuple[int, int], tuple[np.ndarray, ...]]]] = {}


def copied(folder, name: str):  # type: ignore[no-untyped-def]
    """The chain world `name` as its content copy beside `folder`: the shipped world's run is refused by name at the body 0 of 'atom' at the interval 122 (the law's third refusal of the click's read, ALGEBRA.md The digits' budget: the room 2^45.8 of the digits read, the photon's five at three values each on the universe two_atoms.json, which declares no content, and the atom's three at the lay's origin, below the absorption draw's total 2^51.5; the former course took at 74 by the same number read, the rest weight's booking centred on 2026-10-23 moving the residue to the cell none takes), so the claim is read on the content copy (tests/laws_content.content_world, the born universe's holders prepended), which carries every draw."""
    return content_copy(folder / name, CHAIN / f"{name}.json", TWO_ATOMS)


def test_the_chain_runs_back_through_its_absorption_and_emission():
    """B4, the inverse: tools/back_in_time.py's verdict on chain_x_minus over the first 100 intervals, through the first absorption (74) and the emission that follows (91), MATCH bit for bit: every array returns through the click's two writes, the fold and the lay lines."""
    found = BACK.verdict(Lattice(load_shipped(CHAIN / "chain_x_minus.json")), 100)
    assert found["verdict"] == "MATCH" and found["intervals"] == 100, found


def carried(board: Lattice, array: np.ndarray, axis: str, toward: str) -> np.ndarray:
    """An image world's array brought back to the original's frame: the chain's axis moved to x and, for the light toward the upper side, the coordinate mirrored."""
    moved = np.moveaxis(array, AXES.index(axis), 0)
    return moved[::-1] if toward == "plus" else moved


def image(folder, name: str) -> tuple[list[dict], dict[tuple[int, int], tuple[np.ndarray, ...]]]:  # type: ignore[no-untyped-def]
    """A world run over the design's intervals and carried back to the original's frame: its credit lines with the vector keys' chain component moved to x and signed, and every line's now, before and remainder per family and line; run once per process (`RUNS`)."""
    if name not in RUNS:
        axis, toward = DESIGN["worlds"][name]
        board = Lattice(load_world(copied(folder, name)), (lines := []).append)
        for _ in range(DESIGN["intervals"]):
            board.step()
        a, sign = AXES.index(axis), -1 if toward == "plus" else 1
        clicks = []
        for c in lines:
            if c["event"] != "credit":
                continue
            line = dict(c)
            for key in ("momentum", "fan", "recoil"):
                if isinstance(line[key], list):
                    vector = line[key]
                    line[key] = [sign * vector[a], *(v for k, v in enumerate(vector) if k != a)]
            clicks.append(line)
        arrays = {
            (f, j): tuple(
                carried(board, x, axis, toward) for x in (line.now, line.before, line.remainder)
            )
            for f, state in enumerate(board.states)
            for j, line in enumerate(state.lines)
        }
        RUNS[name] = (clicks, arrays)
    return RUNS[name]


def one_world(folder, names: list[str], original: str) -> int:  # type: ignore[no-untyped-def]
    """Every world of `names` equal to `original` in every click line and every cell of every line, brought back to one frame; the click lines' count."""
    clicks0, arrays0 = image(folder, original)
    for name in names:
        clicks, arrays = image(folder, name)
        apart = [
            (c["interval"], key)
            for c, c0 in zip(clicks, clicks0, strict=False)
            for key in c
            if c[key] != c0[key]
        ]
        assert len(clicks) == len(clicks0) and not apart, (name, len(clicks), len(clicks0), apart)
        assert arrays.keys() == arrays0.keys(), name
        for key, cells in arrays.items():
            for x, x0 in zip(cells, arrays0[key], strict=True):
                assert x.shape == x0.shape and np.array_equal(x, x0), (name, key)
    return len(clicks0)


def test_the_two_pure_permutations_are_the_original_bit_for_bit(tmp_path):
    """B5, the 48, the pure permutations: the chain along y and along z with the light toward the lower side, run over the design's 400 intervals and brought back by the inverse permutation, equal to chain_x_minus in every click line, every level and every remainder of every family, the draw's order the one named exception (the bodies' Node lists the images in the original's order, L812 untouched). The runs' seconds printed."""
    started = time.perf_counter()
    count = one_world(tmp_path, ["chain_y_minus", "chain_z_minus"], "chain_x_minus")
    print(
        f"B5: the two pure permutations exact over {DESIGN['intervals']} intervals, {count} click lines; {time.perf_counter() - started:.1f} s"
    )
