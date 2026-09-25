"""BODIES WITH EXTENTS AND THE FACE SLAB (ALGEBRA.md 9.22 (8) and 9.25 (10); BUILD.md
section 26 item 23): a block is the box of `extents` per axis (the cube of `side` the
shorthand), the slabs of the table's emitters, walls and receivers; the face receiver at
every open border is the slab of the world's `face_depth`, one cell, last on every ladder.
Every reading here is the engine's on small worlds (COMPUTATION); no pin.
"""

from __future__ import annotations

import math

import numpy as np
import pytest

from event_universe.events.detector_law import UNIT, DetectorLawSimulation
from event_universe.events.world import block_cell_indices, input_stamp, parse_nature_beam_world
from tests.test_detector_law import layer_world
from tests.test_emitter import emitter_world, massive_generator
from tests.test_flux_reading import planted


def small_layer() -> dict:
    """The layer of 24 x 9 of the first form, empty (no emitter, no set): the detector-law
    layer's emitter body is the train's 32 cells since the born train (BUILD.md section 26
    item 27), wider than this layer, so these tests place their bodies on the empty layer."""
    document = layer_world()
    document["shape"] = [24, 9, 1]
    document["measured"] = []
    document["detectors"] = []
    document.pop("input", None)
    return document


def wall(position, family="light", **keys):
    return {
        "position": position,
        "family": family,
        "amount": 1,
        "phase": 0,
        "momentum": [0, 0, 0],
        "fixed": True,
        "pair": [1, 2],
        **keys,
    }


def test_a_box_of_extents_is_placed_whole_and_its_cells_are_the_box():
    """A light-kind wall slab with the extents [4, 3, 1] at (10, 2, 0) on the layer of 24 x 9:
    the loader carries the extents (the side the x extent) and the engine's cells are the
    box's 12 Nodes; `side` 3 is the extents (3, 3, 3) cut by the layer's thin axis;
    `block_cell_indices` on a cube's side and on the box's extents agree with the box."""
    document = small_layer()
    document["measured"].append(wall([10, 2, 0], extents=[4, 3, 1]))
    world = parse_nature_beam_world(document)
    block = world.measured[-1].block
    assert block is not None and block.extents == (4, 3, 1) and block.side == 4
    simulation = DetectorLawSimulation(world)
    cells = simulation.blocks[-1].mask
    assert int(cells.sum()) == 12 and cells[10:14, 2:5, 0].all()
    assert set(block_cell_indices((24, 9, 1), (10, 2, 0), (4, 3, 1), (False, True, True))) == {
        x * 9 + y for x in range(10, 14) for y in range(2, 5)
    }
    assert block_cell_indices((24, 9, 1), (10, 2, 0), 3, (False, True, True)) == block_cell_indices(
        (24, 9, 1), (10, 2, 0), (3, 3, 3), (False, True, True)
    )
    cube = small_layer()
    cube["measured"].append(wall([10, 2, 0], side=3))
    assert parse_nature_beam_world(cube).measured[-1].block.extents == (3, 3, 3)


def test_the_extents_refusals_and_the_fit_per_axis():
    """Both `side` and `extents` refused; `extents` not three integers from 1 refused; a box
    reaching beyond a face is refused per axis naming its side on that axis (the extents
    [4, 3, 1] at x = 22 on the layer of 24: side 4 reaches 25 beyond the face at 23); a box
    wider than a periodic axis refused (extents [2, 12, 1] on the layer of 9 on y); a
    detector bound to a block of extents [12, 1, 1] on a chain is a cube cut by the chain
    and admitted, a bound block of extents [2, 1, 1] refused naming the extents."""
    both = small_layer()
    both["measured"].append(wall([10, 2, 0], side=3, extents=[3, 3, 1]))
    with pytest.raises(ValueError, match="declares both `side` and `extents`"):
        parse_nature_beam_world(both)
    for bad in ([3, 3], [3, 0, 1], "3", [3, 3, 1, 1]):
        document = small_layer()
        document["measured"].append(wall([10, 2, 0], extents=bad))
        with pytest.raises(ValueError, match=r"extents"):
            parse_nature_beam_world(document)
    beyond = small_layer()
    beyond["measured"].append(wall([22, 2, 0], extents=[4, 3, 1]))
    with pytest.raises(ValueError, match="side 4 at 22 on the axis x reaches 25 beyond the face at 23"):
        parse_nature_beam_world(beyond)
    wide = small_layer()
    wide["measured"].append(wall([10, 2, 0], extents=[2, 12, 1]))
    with pytest.raises(ValueError, match="side 12 wraps onto itself on the periodic axis y of extent 9"):
        parse_nature_beam_world(wide)
    document = emitter_world(stock=1)
    document["measured"].append(wall([40, 0, 0], extents=[12, 1, 1]))
    document["detectors"].append({"name": "slab", "block": len(document["measured"]) - 1})
    document["input"] = input_stamp(document)  # the stamp over the whole file (item 28)
    parse_nature_beam_world(document)
    document["measured"][-1]["extents"] = [2, 1, 1]
    document["input"] = input_stamp(document)
    with pytest.raises(ValueError, match=r"a block of extents \[2, 1, 1\]; a detector is one cube"):
        parse_nature_beam_world(document)


def test_a_slab_well_is_seeded_on_its_mode_and_checked_at_load():
    """A well [800, 801] of the matter kind with the extents [12, 5, 1] at (5, 2, 0) on the
    layer of 24 x 9 (a control world), seeded by the generator on its composed mode with its
    clock and stamp: LAWFUL at load, the residual within the bound at every Node, the mode's
    largest entry on the slab's cells; the slab's centre cell (5 + 6, 2 + 2)."""
    document = small_layer()
    document["measured"] = [
        {
            "position": [5, 2, 0],
            "family": "matter",
            "amount": 1,
            "phase": 0,
            "momentum": [0, 0, 0],
            "fixed": True,
            "extents": [12, 5, 1],
            "pair": [800, 801],
            "seed": 4096,
            "margin": "control",
        }
    ]
    document["families"][1]["pair"] = [800, 809]
    document["detectors"] = []
    massive_generator().seed_on_the_mode(document)
    world = parse_nature_beam_world(document)
    block = world.measured[0].block
    assert block is not None and block.extents == (12, 5, 1) and block.clock is not None
    profile = np.array(block.profile).reshape(24, 9, 1)
    peak = np.unravel_index(int(np.argmax(np.abs(profile))), profile.shape)
    assert 5 <= peak[0] < 17 and 2 <= peak[1] < 7
    simulation = DetectorLawSimulation(world)
    centre = simulation.centre_mask(simulation.blocks[0])
    assert centre[11, 4, 0] and int(centre.sum()) == 1


def test_the_face_slab_is_one_cell_of_the_depth_at_every_open_border():
    """The world key `face_depth`, DECLARED on every board with an open face (no default,
    BUILD.md section 26 item 28): the chain of 80 opened on x without it is refused naming
    the axis; at depth 1 the face cell is the 2 border Nodes; at depth 4 it covers the 4
    Nodes nearest each border (8 Nodes, the free ones); a depth above one that leaves no
    interior is refused; a periodic axis has no face whatever the depth (read on a chain
    without a body: the emitter's mode is the closed chain's, one border for every family).
    The stamp is rewritten for every changed key (the stamp over the whole file)."""
    document = emitter_world(stock=1)
    document["boundary"] = {"x": "open", "y": "periodic", "z": "periodic"}
    document["input"] = input_stamp(document)
    with pytest.raises(ValueError, match="face_depth is required on a GameBoard open on x"):
        parse_nature_beam_world(document)
    document["face_depth"] = 1
    document["input"] = input_stamp(document)
    simulation = DetectorLawSimulation(parse_nature_beam_world(document))
    face = simulation.cell_names.index("face")
    assert int((simulation.cell_index == face).sum()) == 2
    document["face_depth"] = 4
    document["input"] = input_stamp(document)
    simulation = DetectorLawSimulation(parse_nature_beam_world(document))
    face = simulation.cell_names.index("face")
    nodes = sorted(int(x) for x in np.nonzero(simulation.cell_index[:, 0, 0] == face)[0])
    assert nodes == [0, 1, 2, 3, 76, 77, 78, 79]
    document["face_depth"] = 40
    document["input"] = input_stamp(document)
    with pytest.raises(ValueError, match="face_depth 40 leaves no interior on the open axis x"):
        parse_nature_beam_world(document)
    # a periodic chain (no body: the emitter's mode is the closed chain's, one border for
    # every family, and would not fit the periodic operator) has no face whatever the depth
    from tests.test_flux_reading import massive_world

    periodic = massive_world([80, 1, 1], {"x": "periodic", "y": "periodic", "z": "periodic"}, [800, 809])
    periodic["face_depth"] = 4
    periodic["age_bound"] = 100000
    assert "face" not in DetectorLawSimulation(parse_nature_beam_world(periodic)).cell_names


def test_a_deep_face_slab_books_a_packets_energy_and_a_shallow_one_a_part():
    """ALGEBRA.md 9.25 (10), the mathematician's reading: a face one Node deep books a part of
    a packet and reflects the rest, a slab as deep as the packet books nearly all of it.
    On light's open chain of 300 a Gaussian packet of width 14 at k = 0.3 moving +x is
    planted at 150 and kept from clicking; after 600 intervals the face slab of depth 40 has
    booked more than 0.9 of the packet's conserved form I, the face of depth 1 less than
    0.5 (COMPUTATION; the reflected remainder returns along the chain)."""
    from tests.test_flux_reading import massive_world

    readings = {}
    for depth in (1, 40):
        document = massive_world(
            [300, 1, 1], {"x": "open", "y": "periodic", "z": "periodic"}, [800, 809]
        )
        document["age_bound"] = 100000
        document["measured"] = []
        document["detectors"] = []
        document["face_depth"] = depth
        simulation = DetectorLawSimulation(parse_nature_beam_world(document))
        face = simulation.cell_names.index("face")
        k = 0.3
        omega = math.acos((math.cos(k) + 2) / 3)
        x = np.arange(300)
        envelope = np.exp(-(((x - 150) / 14.0) ** 2))
        now = np.rint(UNIT * envelope * np.cos(k * (x - 150))).astype(np.int64).reshape(300, 1, 1)
        before = (
            np.rint(UNIT * envelope * np.cos(k * (x - 150) + omega)).astype(np.int64).reshape(300, 1, 1)
        )
        live = planted(simulation, 0, now, before, np.zeros((300, 1, 1), dtype=np.int64))
        live.norm = 10**30
        simulation.records[live.identity] = live
        energy = simulation.conserved_form(live)
        for _ in range(600):
            simulation.step()
        readings[depth] = live.pointers[face] / energy
    assert readings[40] > 0.9 and readings[1] < 0.5, readings
