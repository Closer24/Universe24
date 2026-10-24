"""The cube's 48 on a turned plane (ALGEBRA.md, The cube's symmetry; features/phase `orbit_moves`, `signed_read`, 2026-10-21): a Link's phase pair stands at the size of the Link's count on the one orbit from the seed and is read with the count's sign, the pair at -n the conjugate of the pair at +n, so that a reflection of a turned world maps every line's levels AND remainders onto the image's bit for bit, the scalars equal and the reversed axis's odd line negated with its remainder complemented (`records.complement`, wall - 1 - r, the law's complement under a symmetry that negates a component; the odd lines seeded at the half wall stand one unit off it, a finding of 2026-10-21 not closed), and the inverse act exact, every array of the state back bit for bit. Posed on the small torus with the universe file (tests/laws_universe.atom_world): the proton's pixel on the clump's x line and the electron's plane one Node along +x, against the x-mirror image with the electron one Node along -x (the flip x -> 2 - x about the clump on the 3-cube torus, a symmetry of the board, the clump, the light and the proton), the two stepped side by side; then the world stepped back. The former board, the shipped hydrogen 1s cut to the 5-cube about its centre (2 intervals side by side and 1 back; the lay even in x, the world its own image, the remainders' two's complement w - r read there), left with the atom folder on 2026-10-24, every world but Universe24 cancelled."""

import time
from pathlib import Path

import numpy as np

from event_universe import records, world_files
from event_universe.core.rule3 import wall_of
from event_universe.lattice import Lattice
from event_universe.world_files import load_world
from tests.laws import LINE_KEYS, arrays
from tests.laws_universe import CUBE, atom_world

INTERVALS, BACK = 2, 1  # side by side; the last one stepped back
PROTON, ELECTRON, MIRRORED = (
    [1, 2, 0],
    [2, 2, 0],
    [0, 2, 0],
)  # on the clump's x line (x = 1 fixed under the flip)


def partings(world: Lattice, image: Lattice) -> list[tuple[str, int, str, int, int]]:
    """Every line of every family of the image run against the x-flip of the world's, the law's map of the cube's symmetry: a scalar line equal; a held row's x odd line (the line 1 of each row of 1 + 3 lines) negated with its remainder the law's complement, wall - 1 - r (records.complement; the plain wall w of the line, and 3 w (X1 + X0) of the row's time line at the Node on a tension line carried as the shear's momentum, the swap's reading); returns (the family, the line, the array, the entries unequal, the largest difference), the unequal ones alone."""
    found = []
    for index, (family, state, other) in enumerate(
        zip(world.families, world.states, image.states, strict=True)
    ):
        wall = wall_of(family.pair[1], world.world.node_clock, world.unit)
        time_line = state.lines[0] if family.held else None
        for number, (line, mirrored) in enumerate(zip(state.lines, other.lines, strict=True)):
            odd = family.held and family.axes and number % family.width == 1
            tension = (
                odd and index not in world.turning and family.motion_volume and time_line is not None
            )
            for key in LINE_KEYS:
                a = np.asarray(getattr(line, key), dtype=object)
                b = np.asarray(getattr(mirrored, key), dtype=object)[::-1]
                if odd and key == LINE_KEYS[2]:
                    own = (
                        3
                        * wall
                        * (
                            np.asarray(time_line.now, dtype=object)
                            + np.asarray(time_line.before, dtype=object)
                        )
                        if tension
                        else wall
                    )
                    b = records.complement(b, own)
                elif odd:
                    b = -b
                unequal = int((a != b).sum())
                if unequal:
                    found.append((family.name, number, key, unequal, int(np.abs(a - b).max())))
    return found


def test_the_x_mirror_of_the_turned_world_is_the_world_bit_for_bit_and_the_inverse_is_exact(
    tmp_path: Path, monkeypatch
) -> None:  # type: ignore[no-untyped-def]
    """The small torus's atom and its x-mirror image stepped 2 intervals side by side: the world stepped back the last interval returns every array of its state at the snapshot, the lines, the write remainders, the phase lines and the count lines, bit for bit (the inverse exact); and at every interval every level and every remainder of every line of every family (the sign holder's rows, the proton's and the electron's planes, the clump, the light, the holder of the content) of the image run is the law's image of the world's bit for bit (`partings`), the first parting's interval, the entries and the largest difference the assertion's message, the levels' partings and the remainders' listed apart."""
    started = time.perf_counter()
    (tmp_path / "world").mkdir(), (tmp_path / "image").mkdir()
    monkeypatch.setattr(world_files, "REPOSITORY_ROOT", tmp_path / "world")
    world = Lattice(load_world(atom_world(tmp_path / "world", ELECTRON, PROTON)))
    monkeypatch.setattr(world_files, "REPOSITORY_ROOT", tmp_path / "image")
    image = Lattice(load_world(atom_world(tmp_path / "image", MIRRORED, PROTON)))
    world.output = image.output = lambda line: None
    assert world.shape == image.shape == (CUBE,) * 3
    electron = [f.name for f in world.families].index("electron")
    assert world.families[electron].plane and world.world.bodies[3].nodes[0] == tuple(ELECTRON)
    assert image.world.bodies[3].nodes[0] == tuple(MIRRORED)
    found, kept = {0: partings(world, image)}, None
    for interval in range(1, INTERVALS + 1):
        world.step()
        image.step()
        if interval == INTERVALS - BACK:
            kept = arrays(world)
        found[interval] = partings(world, image)
    for _ in range(BACK):
        world.step_inverse()
    assert kept is not None and world.interval == INTERVALS - BACK
    assert all(
        np.array_equal(a, b) for a, b in zip(kept, arrays(world), strict=True)
    )  # the inverse exact
    levels = {t: [p for p in parts if p[2] != LINE_KEYS[2]] for t, parts in found.items()}
    remainders = {t: [p for p in parts if p[2] == LINE_KEYS[2]] for t, parts in found.items()}
    print(
        f"the {CUBE}-cube torus's atom and its x-mirror image over {INTERVALS} intervals, the fifth act's fires "
        f"{world.swaps}; the levels' partings {levels}; the remainders' partings {remainders}; "
        f"{time.perf_counter() - started:.1f} s"
    )
    assert not any(levels.values()) and not any(remainders.values()), (
        "the x-mirror image parts from the world: (the interval, (family, line, array, entries unequal, "
        f"largest difference)) the levels {[(t, p[:3]) for t, parts in levels.items() for p in parts[:3]]}; "
        f"the remainders {[(t, p[:3]) for t, parts in remainders.items() for p in parts[:3]]}"
    )
