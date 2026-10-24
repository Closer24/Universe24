"""The cube's 48 on a turned plane (ALGEBRA.md, The cube's symmetry; features/phase `orbit_moves`, `signed_read`, 2026-10-21): a Link's phase pair stands at the size of the Link's count on the one orbit from the seed and is read with the count's sign, the pair at -n the conjugate of the pair at +n, so that a reflection of a turned world maps every line's levels AND remainders onto the image's bit for bit, the scalars equal and the reversed axis's odd line negated with its remainder complemented, where a negative count iterated by the inverse act from the seed (the engine before this date) parted the remainders of mirror-image worlds from the interval 2 (one Link unit of the fold at 7 percent of the angles above the count 183, the levels untouched over 73 intervals); and the inverse act exact as before, every array of the state back bit for bit. The world: the repository's hydrogen 1s (examples/events/atom/hydrogen_1s.json: the proton's pixel at the centre, the electron's 1s record declared one Node along +x) cut to the 7-cube about its centre, the lay's arrays truncated (the levels beyond the cube below 0.02 of the centre's), and its x-mirror image, the electron declared one Node along -x and the arrays flipped along x; the phase act's cost is its rounds (the centre's Links count 3,000 acts per interval) and not the Nodes, so the test runs 4 intervals side by side and 2 back, cut from 8 and 4 on 2026-10-21 for the suite's 30-second bound (25 seconds on a quiet core at 8 and 4, 36 on a loaded one at 5 and 2): the parting falls at the interval 4 on the cut lay, and the engine before the fix fails the cut test at 4 with the same 18 entries, measured."""

import json
import time
from pathlib import Path

import numpy as np

from event_universe import world_files
from event_universe.core.rule3 import wall_of
from event_universe.lattice import Lattice
from event_universe.world_files import input_digest, load_world
from tests.laws import LINE_KEYS, arrays

ATOM = Path(world_files.REPOSITORY_ROOT) / "examples" / "events" / "atom" / "hydrogen_1s.json"
WHOLE, CUBE, CUT = (
    11,
    5,
    3,
)  # the 5-cube about the 11-cube's centre: the file's x, y, z from 3 through 7 (the 7-cube over 4 intervals, 30 s on the suite's clock, left on 2026-10-24)
INTERVALS, BACK = 2, 1  # side by side; the last one stepped back


def cut(flat: list[int], mirror: bool) -> list[int]:
    """A level array of the 11-cube in x-major order cut to the 7-cube about the centre, flipped along x for the mirror image."""
    block = np.asarray(flat, dtype=np.int64).reshape((WHOLE,) * 3)
    block = block[CUT : CUT + CUBE, CUT : CUT + CUBE, CUT : CUT + CUBE]
    if mirror:
        block = block[::-1]
    return [int(v) for v in block.ravel()]


def cube_world(folder: Path, mirror: bool) -> Path:
    """The 7-cube world written beside its mode file: the bodies' Nodes moved into the cube, the electron's reflected for the mirror image, every level array cut and flipped with it (the 1s lay's arrays are even in x: the flip changes no array), the mode's digest the cut world's."""
    doc = json.loads(ATOM.read_text(encoding="utf-8"))
    mode = json.loads(ATOM.with_suffix(".mode.json").read_text(encoding="utf-8"))
    doc["shape"], doc["intervals"] = [CUBE] * 3, INTERVALS
    for body in doc["bodies"]:
        for line in body["nodes"]:
            x, y, z = (int(c) - CUT for c in line["node"])
            line["node"] = [CUBE - 1 - x if mirror else x, y, z]
    for body in mode["bodies"]:
        assert all(cut(value, True) == cut(value, False) for value in body["moving"].values())
        body["moving"] = {key: cut(value, mirror) for key, value in body["moving"].items()}
    mode["world_digest"] = input_digest(doc)
    path = folder / ("mirror" if mirror else "cube") / "hydrogen_1s_cube.json"
    path.parent.mkdir(parents=True)
    path.write_text(json.dumps(doc), encoding="utf-8")
    path.with_suffix(".mode.json").write_text(json.dumps(mode), encoding="utf-8")
    return path


def partings(world: Lattice, image: Lattice) -> list[tuple[str, int, str, int, int]]:
    """Every line of every family of the image run against the x-flip of the world's, the law's map of the cube's symmetry: a scalar line equal, a held row's x odd line (a vector's component, the line 1 of each row) negated with its remainder the two's complement w - r (the lines seeded at the half wall and walked by opposite numerators; the law's complement w - 1 - r stands one unit off it, a finding of 2026-10-21 not closed here); returns (the family, the line, the array, the entries unequal, the largest difference), the unequal ones alone."""
    found = []
    for family, state, other in zip(world.families, world.states, image.states, strict=True):
        wall = wall_of(family.pair[1], world.world.node_clock, world.unit)
        for number, (line, mirrored) in enumerate(zip(state.lines, other.lines, strict=True)):
            odd = family.held and family.axes and number % family.width == 1
            for key in LINE_KEYS:
                a = np.asarray(getattr(line, key), dtype=object)
                b = np.asarray(getattr(mirrored, key), dtype=object)[::-1]
                if odd:
                    b = np.where(b == 0, 0, wall - b) if key == LINE_KEYS[2] else -b
                unequal = int((a != b).sum())
                if unequal:
                    found.append((family.name, number, key, unequal, int(np.abs(a - b).max())))
    return found


def test_the_x_mirror_of_the_turned_1s_world_is_the_world_bit_for_bit_and_the_inverse_is_exact(tmp_path):
    """The 5-cube 1s world and its x-mirror image stepped 2 intervals side by side: at every interval every level and every remainder of every line of every family (the sign holder's rows, the proton's and the electron's planes) of the image run is the law's image of the world's bit for bit (`partings`), and the world is its own image alike (the lay even in x; the step reads no declared Node); the engine before 2026-10-21 kept the levels and parted the electron's remainders from the interval 2 by multiples of p_0^2 at the Nodes whose -x Port reads a Link above the count 183, and the first parting's interval, the entries and the largest difference are the assertion's message; then the world stepped back the last 2 intervals returns every array of its state at the snapshot, the lines, the write remainders, the phase lines and the count lines, bit for bit."""
    started = time.perf_counter()
    world = Lattice(load_world(cube_world(tmp_path, False)))
    image = Lattice(load_world(cube_world(tmp_path, True)))
    assert world.shape == image.shape == (CUBE,) * 3
    electron = [f.name for f in world.families].index("electron")
    assert world.families[electron].plane and world.world.bodies[1].nodes[0] == (3, 2, 2)
    assert image.world.bodies[1].nodes[0] == (1, 2, 2)
    first, kept = None, None
    for interval in range(1, INTERVALS + 1):
        world.step()
        image.step()
        if interval == INTERVALS - BACK:
            kept = arrays(world)
        found = partings(world, image) + partings(world, world)
        if found and first is None:
            first = (interval, found)
    assert first is None, (
        f"the x-mirror image parts from the world at the interval {first[0]}: (family, line, array, entries "  # type: ignore[index]
        f"unequal, largest difference) {first[1][:6]}"  # type: ignore[index]
    )
    for _ in range(BACK):
        world.step_inverse()
    assert kept is not None and world.interval == INTERVALS - BACK
    assert all(np.array_equal(a, b) for a, b in zip(kept, arrays(world), strict=True))
    print(
        f"the {CUBE}-cube 1s world and its x-mirror image: {INTERVALS} intervals bit for bit in levels and "
        f"remainders of {sum(len(s.lines) for s in world.states)} lines, {len(kept)} arrays back bit for bit "
        f"over {BACK} intervals; {time.perf_counter() - started:.1f} s"
    )
