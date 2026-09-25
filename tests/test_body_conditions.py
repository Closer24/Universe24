"""The body's algebraic conditions exact in the initial state, checked at load (the model
owner's word of 2026-09-24, 16:48Z, through the Boss; SIMULATOR_DEFINITIONS.md, the four
building blocks, the body's conditions): (a) a cube on a small board, a square on a layer
and a segment on a chain, each seeded with the margin module's own integer profile, load,
construct and pass the check bit for bit; (b) a body that does not fit the board is refused
at load, named with the axis, never cut; (c) a profile with one Node off is refused naming
the Node; (d) a flat seed is refused (the initial state is not the mode); (e) a pair not
lowered is the loader's own refusal; (f) a pushed body's ramp below ten relaxation times of
its own well is refused, at or above it admitted; (g) the run list's massive worlds under
the check: every bound body seeded on its own mode by the generators passes bit for bit,
the pushed ones with their ramp at or above ten relaxation times; the silent bodies and
the light-kind walls have no reading. Every number here is a
COMPUTATION of the declaration; nothing of the check is read by the state."""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pytest

from event_universe.diagnostics.massive_record_margin import (
    bound_mode,
    check_body_conditions,
    check_margins,
    relaxation_time,
)
from event_universe.events.detector_law import DetectorLawSimulation
from event_universe.events.world import parse_nature_beam_world
from tests.test_massive_record import block_world

PERIODIC = {"x": "periodic", "y": "periodic", "z": "periodic"}
KIND = [800, 809]
WELL = [
    800,
    801,
]  # the rich well (2403 remainder values, ALGEBRA.md 9.22 (4)), the fifteen's since item 15
AMPLITUDE = 1 << 20
WORLDS = Path(__file__).resolve().parents[1] / "examples" / "events"


def seeded(
    shape: list[int],
    corner: list[int],
    side: int,
    momentum: list[int] | None = None,
    ramp: int = 0,
    faces: dict[str, str] | None = None,
) -> dict:
    """A world of one body of the kind [800, 809] with the well [800, 801], a
    control world, its seed the margin module's own mode rounded at the amplitude 2^20 over
    the whole board (the generator's `mode_profile` form)."""
    document = block_world(
        shape,
        PERIODIC,
        KIND,
        [{"position": corner, "side": side, "pair": WELL, "margin": "control"}],
        faces=faces,
    )
    document["age_bound"] = 100000
    entry = document["measured"][0]
    entry["margin"] = "control"
    if momentum is not None:
        entry["momentum"] = momentum
        entry["ramp"] = ramp
    mode = bound_mode(parse_nature_beam_world(document), 0)
    entry["seed"] = [int(value) for value in np.rint(mode * AMPLITUDE).astype(np.int64).ravel()]
    return document


def checked(document: dict) -> list[str]:
    """The check as the runner and the preflight tool call it: the margins first, then the
    body's conditions on the engine as constructed."""
    world = parse_nature_beam_world(document)
    readings = check_margins(world)
    return check_body_conditions(world, DetectorLawSimulation(world), readings)


def test_a_cube_square_and_segment_seeded_on_the_mode_pass_bit_for_bit():
    """The cube of side 20 in 48^3, the square of side 8 on a 32 x 32 layer and the segment
    of side 8 on a chain of 64, each on its own board's mode: two COMPUTATION lines each
    (the family's composed operator below 2, ALGEBRA.md 9.19 (2); the initial state the
    profile at both levels bit for bit)."""
    for shape, corner, side in (
        ([48, 48, 48], [14, 14, 14], 20),
        ([32, 32, 1], [12, 12, 0], 8),
        ([64, 1, 1], [28, 0, 0], 8),
    ):
        lines = checked(seeded(shape, corner, side))
        assert len(lines) == 2 and "bit for bit" in lines[1], (shape, lines)
        assert lines[0].startswith("operator (COMPUTATION): the family 'matter'")
        assert f"amplitude {AMPLITUDE}" in lines[1]


def test_b_a_body_that_does_not_fit_is_refused_at_load_never_cut():
    """A body whose far vertex passes an open face is refused naming the axis and the
    vertex; a body wider than a periodic axis is refused as wrapped onto itself; a segment
    past the chain's end the same; the folded axis of extent 1 is no refusal (the square
    above). Before this line the engine cut the cube to the board silently."""
    off = block_world(
        [48, 48, 48],
        PERIODIC,
        KIND,
        [{"position": [40, 14, 14], "side": 20, "pair": WELL, "margin": "control"}],
        faces={"x": "open"},
    )
    off["age_bound"] = 100000
    with pytest.raises(
        ValueError, match=r"side 20 at 40 on the axis x reaches 59 beyond the face at 47"
    ):
        parse_nature_beam_world(off)
    wrapped = block_world(
        [16, 48, 48],
        PERIODIC,
        KIND,
        [{"position": [2, 14, 14], "side": 20, "pair": WELL, "margin": "control"}],
    )
    wrapped["age_bound"] = 100000
    with pytest.raises(ValueError, match=r"wraps onto itself on the periodic axis x of extent 16"):
        parse_nature_beam_world(wrapped)
    chain = block_world(
        [64, 1, 1],
        PERIODIC,
        KIND,
        [{"position": [60, 0, 0], "side": 8, "pair": WELL, "margin": "control"}],
        faces={"x": "open"},
    )
    chain["age_bound"] = 100000
    with pytest.raises(ValueError, match=r"reaches 67 beyond the face at 63"):
        parse_nature_beam_world(chain)
    # across the seam of a periodic axis the cube is whole: admitted
    seam = block_world(
        [48, 48, 48],
        PERIODIC,
        KIND,
        [{"position": [40, 14, 14], "side": 20, "pair": WELL, "margin": "control"}],
    )
    seam["age_bound"] = 100000
    assert parse_nature_beam_world(seam).measured[0].block is not None


def test_c_one_node_off_the_mode_is_refused_naming_the_node():
    document = seeded([48, 48, 48], [14, 14, 14], 20)
    index = (14 * 48 + 14) * 48 + 14
    document["measured"][0]["seed"][index] += 1
    with pytest.raises(ValueError, match=r"at the Node \(14, 14, 14\) the level `now` holds") as found:
        checked(document)
    assert "(1 Nodes differ" in str(found.value)


def test_d_a_flat_seed_is_not_the_mode_and_is_refused():
    """The flat seed of the first builds (the value on the cells, 0 outside) is not the bound
    mode's profile: refused at the first differing Node, the sentence naming the generator's
    `mode_profile` as the form the seed takes."""
    document = block_world(
        [48, 48, 48],
        PERIODIC,
        KIND,
        [{"position": [14, 14, 14], "side": 20, "pair": WELL, "margin": "control", "seed": AMPLITUDE}],
    )
    document["age_bound"] = 100000
    document["measured"][0]["seed"] = AMPLITUDE
    with pytest.raises(
        ValueError, match=r"is not the bound mode's integer profile at the amplitude 1048576"
    ):
        checked(document)


def test_e_a_pair_not_lowered_is_the_loaders_own_refusal():
    document = block_world(
        [48, 48, 48],
        PERIODIC,
        KIND,
        [{"position": [14, 14, 14], "side": 20, "pair": KIND, "margin": "control"}],
    )
    document["age_bound"] = 100000
    with pytest.raises(ValueError, match=r"is the kind's own pair"):
        parse_nature_beam_world(document)


def test_f_the_ramp_against_ten_relaxation_times():
    """The box of side 20 on the well [800, 801] (the relaxation about 33 intervals, the
    margin module's own omega_b; on [800, 800] it read 25.7, DECLARATIONS.md section 8's
    26): pushed with a ramp of 100 it is refused naming the ramp and the relaxation time;
    with 400 (above ten times) it is admitted with the ramp's line."""
    world = parse_nature_beam_world(seeded([48, 48, 48], [14, 14, 14], 20))
    relaxation = relaxation_time(check_margins(world)[0])
    assert 30.0 < relaxation < 36.0
    with pytest.raises(ValueError, match=r"the ramp 100 is below 10 relaxation times"):
        checked(seeded([48, 48, 48], [14, 14, 14], 20, momentum=[64, 0, 0], ramp=100))
    lines = checked(seeded([48, 48, 48], [14, 14, 14], 20, momentum=[64, 0, 0], ramp=400))
    assert len(lines) == 3 and lines[2].startswith("ramp (COMPUTATION): block 0: the ramp 400")


CLEAN = "bit for bit"
NONE = "no reading"


@pytest.mark.parametrize(
    ("name", "verdict"),
    [
        ("massive_record/layer_pin_rest_14.json", CLEAN),
        ("massive_record/layer_pin_k3_14.json", CLEAN),
        ("massive_record/deep_well_k3_40.json", CLEAN),
        ("massive_record/deep_well_rest_40.json", CLEAN),
        ("massive_record/moving_20.json", CLEAN),
        ("massive_record/rest_20.json", CLEAN),
        ("massive_record/light_clock_60.json", CLEAN),
        ("massive_record/sagnac_k3.json", CLEAN),
        ("massive_record/sagnac_rest.json", CLEAN),
        ("massive_record/redshift_k3.json", CLEAN),
        ("massive_record/redshift_control.json", CLEAN),
        ("massive_record/index_moving_long_k3_away.json", CLEAN),
        ("detector_law/two_slits.json", CLEAN),
    ],
)
def test_g_the_run_lists_massive_worlds_load_clean_under_the_check(name: str, verdict: str):
    """Every bound body of the run list's massive worlds is seeded on its own mode by the
    generators (`seed_on_the_mode`: the muon's layer pin worlds at rest and pushed, the deep
    well and its rest world, the boxes, the light clock, the Sagnac blocks and their rest
    world, the redshift emitter and its control) and passes the check bit for bit, a pushed
    body's ramp at or above ten relaxation times; the index's and the two slits' emitter
    bodies (BUILD.md section 26: a well of the source kind seeded on its mode) read clean too,
    the two slits' mirror line of light's kind having no reading. Before this branch the seven worlds other
    than the layer pin's carried a flat seed and were refused (the world line of
    DECLARATIONS.md section 15, the body's seed on its mode)."""
    document = json.loads((WORLDS / name).read_text(encoding="utf-8"))
    world = parse_nature_beam_world(document)
    readings = check_margins(world)
    lines = check_body_conditions(world, DetectorLawSimulation(world), readings)
    if verdict == NONE:
        assert readings == [] and lines == []
        return
    assert readings and lines
    assert all(CLEAN in line for line in lines if line.startswith("seed"))
    if any(int(component) != 0 for component in world.measured[readings[0].number].momentum):
        assert any(line.startswith("ramp (COMPUTATION)") for line in lines)
