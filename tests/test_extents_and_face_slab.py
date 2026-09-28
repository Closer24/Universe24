"""Bodies with extents and the face slab: a block is the box of its extents per axis, and the face receiver at every open border is one detector of the world's face depth, last on every ladder. COMPUTATION on small worlds; no pin."""

import math
from fractions import Fraction

import numpy as np
import pytest

from event_universe.events.detector_law import DetectorLawSimulation
from event_universe.loader.world import body_node_indices
from event_universe.world_files import input_stamp, parse_nature_beam_world
from tests.running import planted
from tests.worlds import emitter_world, layer_world, seed_on_the_mode

# A, the amplitude unit of the planted rows: the worlds' amplitude_bound (ALGEBRA.md #the-line; the engine's constant UNIT retired by the model owner's record 2089, BUILD.md section 26 item 57)
UNIT = 1 << 20


def small_layer() -> dict:
    """The layer of 24 x 9 of the first form, empty (no emitter, no set): the detector-law layer's emitter body is the train's 32 Nodes since the given train (BUILD.md section 26 item 27), wider than this layer, so these tests place their bodies on the empty layer."""
    document = layer_world()
    document["shape"] = [24, 9, 1]
    document["measured"] = []
    document["detectors"] = []
    document.pop("stamp", None)
    return document


def wall(position, family="light", **keys):
    entry = {
        "position": position,
        "family": family,
        "amount": 1,
        "stocks": {},
        "momentum": [0, 0, 0],
        "momentum_before": [0, 0, 0],
        "pair": [1, 2],
        **keys,
    }
    if "extents" in entry or "side" in entry:
        # a block declares its drive's ramp and start (no default, item 57) and its numbers, q, spin and moment (ALGEBRA.md #the-interval; item 61; the word q, item 68)
        entry.setdefault("ramp", 0)
        entry.setdefault("start", 0)
        entry.setdefault("q", 0)
        entry.setdefault("spin", [0, 0, 0])
        entry.setdefault("spin_before", entry["spin"])
        entry.setdefault("moment", [0, 0, 0])
        entry.setdefault("twist", 0)  # the generator's number; 0 where no read by "own" (item 73)
    return entry


def test_a_box_of_extents_is_placed_whole_and_its_cells_are_the_box():
    """A light-kind wall slab with the extents [4, 3, 1] at (10, 2, 0) on the layer of 24 x 9: the loader carries the extents (the side the x extent) and the engine's Nodes are the box's 12 Nodes; `side` 3 is the extents (3, 3, 3) cut by the layer's thin axis; `body_node_indices` on a cube's side and on the box's extents agree with the box."""
    document = small_layer()
    document["measured"].append(wall([10, 2, 0], extents=[4, 3, 1]))
    world = parse_nature_beam_world(document)
    block = world.measured[-1].block
    assert block is not None and block.extents == (4, 3, 1) and block.side == 4
    simulation = DetectorLawSimulation(world)
    nodes = simulation.blocks[-1].mask
    assert int(nodes.sum()) == 12 and nodes[10:14, 2:5, 0].all()
    assert set(body_node_indices((24, 9, 1), (10, 2, 0), (4, 3, 1), (False, True, True))) == {
        x * 9 + y for x in range(10, 14) for y in range(2, 5)
    }
    assert body_node_indices((24, 9, 1), (10, 2, 0), 3, (False, True, True)) == body_node_indices(
        (24, 9, 1), (10, 2, 0), (3, 3, 3), (False, True, True)
    )
    cube = small_layer()
    cube["measured"].append(wall([10, 2, 0], side=3))
    assert parse_nature_beam_world(cube).measured[-1].block.extents == (3, 3, 3)


def test_the_extents_refusals_and_the_fit_per_axis():
    """Both `side` and `extents` refused; `extents` not three integers from 1 refused; a box reaching beyond a face is refused per axis naming its side on that axis (the extents [4, 3, 1] at x = 22 on the layer of 24: side 4 reaches 25 beyond the face at 23); a box wider than a periodic axis refused (extents [2, 12, 1] on the layer of 9 on y); a detector bound to a block of extents [12, 1, 1] on a chain is a cube cut by the chain and admitted, a bound block of extents [2, 1, 1] refused naming the extents."""
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
    document["stamp"] = input_stamp(document)  # the stamp over the whole file (item 28)
    parse_nature_beam_world(document)
    document["measured"][-1]["extents"] = [2, 1, 1]
    document["stamp"] = input_stamp(document)
    # SINCE COMMIT 7 a body is its own detector whatever its support (ALGEBRA.md #the-rows-against-nature, record 2109): the slab of two Nodes bound as its own set is admitted
    parse_nature_beam_world(document)


def test_a_slab_well_is_seeded_on_its_mode_and_checked_at_load():
    """A well [800, 801] of the matter kind with the extents [12, 5, 1] at (5, 2, 0) on the layer of 24 x 9 (a control world), seeded by the generator on its composed mode with its clock and stamp: LAWFUL at load, the residual within the bound at every Node, the mode's largest entry on the slab's Nodes; the slab's centre Node (5 + 6, 2 + 2)."""
    document = small_layer()
    document["measured"] = [
        {
            "position": [5, 2, 0],
            "family": "matter",
            "amount": 1,
            "stocks": {},
            "ramp": 0,
            "start": 0,
            "momentum": [0, 0, 0],
            "momentum_before": [0, 0, 0],
            "extents": [12, 5, 1],
            "q": 0,
            "spin": [0, 0, 0],
            "spin_before": [0, 0, 0],
            "twist": 0,
            "moment": [0, 0, 0],
            "pair": [800, 801],
            "seed": 4096,
            "margin": "control",
        }
    ]
    document["universe"][1]["pair"] = [800, 809]
    document["detectors"] = []
    seed_on_the_mode(document)
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
    """The world key `face_depth`, DECLARED on every board with an open face (no default, BUILD.md section 26 item 28): the chain of 80 opened on x without it is refused naming the axis; at depth 1 the face detector is the 2 border Nodes; at depth 4 it covers the 4 Nodes nearest each border (8 Nodes, the free ones); a depth above one that leaves no interior is refused; a periodic axis has no face whatever the depth (read on a chain without a body: the emitter's mode is the closed chain's, one border for every family). The stamp is rewritten for every changed key (the stamp over the whole file)."""
    document = emitter_world(stock=1)
    document["boundary"] = {"x": "open", "y": "periodic", "z": "periodic"}
    document["stamp"] = input_stamp(document)
    with pytest.raises(ValueError, match="face_depth is required on a GameBoard open on x"):
        parse_nature_beam_world(document)
    document["face_depth"] = 1
    document["stamp"] = input_stamp(document)
    simulation = DetectorLawSimulation(parse_nature_beam_world(document))
    face = simulation.detector_names.index("face")
    assert int((simulation.detector_at_node == face).sum()) == 2
    document["face_depth"] = 4
    document["stamp"] = input_stamp(document)
    simulation = DetectorLawSimulation(parse_nature_beam_world(document))
    face = simulation.detector_names.index("face")
    nodes = sorted(int(x) for x in np.nonzero(simulation.detector_at_node[:, 0, 0] == face)[0])
    assert nodes == [0, 1, 2, 3, 76, 77, 78, 79]
    document["face_depth"] = 40
    document["stamp"] = input_stamp(document)
    with pytest.raises(ValueError, match="face_depth 40 leaves no interior on the open axis x"):
        parse_nature_beam_world(document)
    # a periodic chain (no body: the emitter's mode is the closed chain's, one border for every family, and would not fit the periodic operator) has no face whatever the depth
    from tests.bodies import massive_world

    periodic = massive_world([80, 1, 1], {"x": "periodic", "y": "periodic", "z": "periodic"}, [800, 809])
    periodic["face_depth"] = 4
    assert "face" not in DetectorLawSimulation(parse_nature_beam_world(periodic)).detector_names


def test_a_deep_face_slab_books_a_packets_energy_and_a_shallow_one_a_part():
    """ALGEBRA.md #the-ladder, the mathematician's reading: a face one Node deep books a part of a packet and reflects the rest, a slab as deep as the packet books nearly all of it. On light's open chain of 300 a Gaussian packet of width 14 at k = 0.3 moving +x is planted at 150 with its norm set to 7/10 of its conserved form, so the face clicks only when it has taken most of the packet: after 600 intervals the face slab of depth 40 has clicked once (one gather line, chosen the face), the face of depth 1 not at all (the measurement is the click count on the gather lines; the reflected remainder returns along the chain)."""
    from tests.bodies import massive_world

    clicks = {}
    for depth in (1, 40):
        document = massive_world(
            [300, 1, 1], {"x": "open", "y": "periodic", "z": "periodic"}, [800, 809]
        )
        document["measured"] = []
        document["detectors"] = []
        document["face_depth"] = depth
        lines: list[dict] = []
        simulation = DetectorLawSimulation(parse_nature_beam_world(document), observer=lines.append)
        k = 0.3
        omega, x = math.acos((math.cos(k) + 2) / 3), np.arange(300)
        envelope = np.exp(-(((x - 150) / 14.0) ** 2))
        now = np.rint(UNIT * envelope * np.cos(k * (x - 150))).astype(np.int64).reshape(300, 1, 1)
        before = (
            np.rint(UNIT * envelope * np.cos(k * (x - 150) + omega)).astype(np.int64).reshape(300, 1, 1)
        )
        live = planted(simulation, 0, now, before, np.zeros((300, 1, 1), dtype=np.int64))
        live.norm = int(Fraction(*simulation.conserved_form(live)) * 7 / 10)
        simulation.records[live.identity] = live
        for _ in range(600):
            simulation.step()
        clicks[depth] = [line for line in lines if line["event"] == "gather"]
    assert len(clicks[40]) == 1 and clicks[40][0]["chosen"] == [["face", 0, "0"]] and clicks[1] == []
