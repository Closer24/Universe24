"""THE TRANSPORT AND THE SECOND LEVEL (ALGEBRA.md 9.81 (2), 9.82 (3), 9.91 (1), (6), 9.96 (2);
the one stroke of record 2106, commit 4; BUILD.md section 26 item 64): the twist table's
triples are exact and the nearest; the loader writes every record's twist "own" and the given
light's component from the body's moment; a vector part on a slab rotates a matter record's
arriving pair on the Ports with the remainders kept, writes its second level, and one interval
back restores everything; the Ports along a record's own component book nothing of it; with
every vector part zero the step is the plain path bit for bit; the refusals by name. HOST; no
pin."""

from __future__ import annotations

import json
import math
from pathlib import Path

import numpy as np
import pytest

from event_universe.core.rule3 import coefficients, rule3
from event_universe.events.detector_law import DetectorLawSimulation
from event_universe.events.world import TWIST_FINE_BITS
from event_universe.generator_numbers import light_twist, rotation_twist, twist_triple
from event_universe.world_files import input_stamp, parse_nature_beam_world
from tests.bodies import PACES_SHAPE as SHAPE
from tests.bodies import paces_world, parts_of
from tests.running import refused
from tests.worlds import FILE, emitter_world, on_the_file

ROOT = Path(__file__).resolve().parents[1]
GAMMA = 10_000
UNIT = 4 * GAMMA * 65536


def table() -> dict:
    """The shipped twist table (the families file's integers block)."""
    return json.loads((ROOT / FILE).read_text(encoding="utf-8"))["integers"]["twist_table"]


def twisted_world() -> dict:
    """The paces world with the matter family's read on gravity twisted by "own" and the
    shipped twist table (an inline world declares it as a world key)."""
    document = paces_world()
    for family in document["universe"]:
        if family["name"] == "matter":
            family["reads"][0]["twist"] = "own"
        if family["name"] == "charge":
            # the charge with its vector part (the shipped file's entry on the inline list)
            family.update(
                {"parts": [1, 3], "held_factors": [1, 1], "held_dipole": "moment", "held_dipole_div": 2}
            )
    document["twist_table"] = table()
    document["stamp"] = input_stamp(document)
    return document


def composed(k: int, rows: dict) -> tuple[int, int, int]:
    """The transport's triple of k from the two tables, by hand (9.96 (2) (c))."""
    magnitude = abs(k)
    c0, s0, d0 = rows["fine"][magnitude & ((1 << TWIST_FINE_BITS) - 1)]
    c1, s1, d1 = rows["coarse"][magnitude >> TWIST_FINE_BITS]
    sign = 1 if k > 0 else -1 if k < 0 else 0
    return c1 * c0 - s1 * s0, sign * (s1 * c0 + c1 * s0), d1 * d0


def test_the_twist_tables_triples_are_exact_and_the_nearest_of_their_angles():
    rows = table()
    assert rows["unit"] == UNIT
    for k in (0, 1, 81 << 10, 200 << 10, 32767 << 10):
        c, s, d = twist_triple(k, UNIT)
        assert c * c + s * s == d * d and 1 <= d <= 10**9
        assert math.gcd(math.gcd(c, s), d) == 1
        # the angle within the triples' own resolution of its target (the nearest n / m with
        # m at most 31622: no triple below 2 / m, the fine angles all read 0)
        assert abs(math.atan2(s, c) - k / UNIT) <= 2 / 31622
    assert rows["fine"][0] == [1, 0, 1] and rows["coarse"][0] == [1, 0, 1]
    assert list(twist_triple(200 << 10, UNIT)) == rows["coarse"][200]
    c, s, d = rows["coarse"][200]
    assert abs(math.atan2(s, c) - (200 << 10) / UNIT) < 1e-8


def test_the_loader_writes_the_twist_own_and_the_given_lights_component():
    point = json.loads((ROOT / "examples/events/point_emitter/point_light_clock.json").read_text())
    world = parse_nature_beam_world(point)
    body = world.measured[0].block
    assert body is not None and body.emitter is not None
    # the body's own record turns at its mode's rotation, 2 cos omega = a / b
    a, b = body.clock if body.clock is not None else (0, 1)
    assert body.twist == rotation_twist(a, 2 * b) == round(65536 * math.acos(a / (2 * b)))
    # the window's light turns at the emitter's rotation (9.85 (5)); its component along z
    assert body.emitter.twist == body.twist and body.emitter.part == 3
    clock = json.loads((ROOT / "examples/events/massive_record/light_clock.json").read_text())
    beam = parse_nature_beam_world(clock).measured[0].block
    # SINCE COMMIT 7 the light clock's A gives by the window too (the train retired): its
    # light turns at its own rotation, the component along z
    assert beam is not None and beam.emitter is not None
    assert beam.emitter.twist == beam.twist == rotation_twist(beam.clock[0], 2 * beam.clock[1])
    assert beam.emitter.part == 3
    # the retired train's twist was its wavelength's on light's dispersion, cos omega = (cos k + 2) / 3
    assert light_twist(4) == round(65536 * math.acos(2 / 3))
    assert rotation_twist(800, 809) == round(65536 * math.acos(800 / 809))


def test_a_planted_vector_part_rotates_the_arriving_pair_and_the_inverse_restores_everything():
    """Gravity's x part set to 5 on a slab: a matter record with the twist "own" reads k =
    sigma x twist x (V_i + V_j) on its x Ports there, its arrivals are rotated by the table's
    triple to the nearest unit (T = (c re - s im) / d), its second level is written from
    the rotated arrivals, and one interval back restores the levels and the remainders
    exactly."""
    simulation = DetectorLawSimulation(parse_nature_beam_world(twisted_world()))
    gravity = parts_of(simulation, "clicks")
    matter = [family.name for family in simulation.families].index("matter")
    x_part = gravity[1]
    assert x_part.part == 1 and x_part.silent
    x_part.now[6:8, :, :] = 5
    x_part.before[6:8, :, :] = 5
    x_part.silent = False
    simulation._sourced_ever[(gravity[0].family, 1)] = True
    twist = rotation_twist(800, 809)
    rng = np.random.default_rng(7)
    now = rng.integers(-(1 << 16), 1 << 16, size=tuple(SHAPE), dtype=np.int64)
    before = rng.integers(-(1 << 16), 1 << 16, size=tuple(SHAPE), dtype=np.int64)
    live = simulation.planted_record(matter, now.copy(), before.copy(), twist=twist)
    twists = simulation._port_twists(live, False)
    assert twists is not None
    # the Port toward +x at a slab Node: k = +twist x (5 + 5); toward -x at its left edge: -twist x 5
    assert int(twists[0][6, 2, 2]) == twist * 10 and int(twists[1][6, 2, 2]) == -twist * 5
    assert int(twists[0][5, 2, 2]) == twist * 5 and int(twists[1][5, 2, 2]) == 0
    assert not twists[2].any() and not twists[3].any()  # no y or z twist: V_y = V_z = 0
    content = simulation._effective_content(matter).copy()
    num_all, den_all = simulation.pair_arrays(matter)
    simulation._advance(live)
    assert live.im_now is not None and live.im_now.any()
    rows = table()
    node = (6, 2, 2)
    reads = 0
    for axis in range(3):
        for side, sigma in enumerate((1, -1)):
            j = list(node)
            j[axis] = (j[axis] + sigma) % SHAPE[axis]
            k = int(twists[2 * axis + side][node])
            c, s, d = composed(k, rows)
            # the arriving pair (re_j, 0) rotated: T_re = c re_j / d to the nearest unit
            reads += (2 * c * int(now[tuple(j)]) + d) // (2 * d)

    (read, _, _), self_coefficient, wall = coefficients(
        int(num_all[node]), int(den_all[node]), GAMMA, int(content[node])
    )
    total = read * reads + self_coefficient * int(now[node]) - wall * int(before[node])
    assert int(live.now[node]) == total // wall
    assert live.im_now[node] != 0 or live.im_remainder is not None
    # one interval back: the levels and the remainders as before the step (the transport a
    # pure function of the arrivals, recomputed)
    simulation._advance_inverse(live)
    assert np.array_equal(live.now, now) and np.array_equal(live.before, before)
    assert not live.remainder.any()
    assert live.im_now is not None and live.im_before is not None and live.im_remainder is not None
    assert not live.im_now.any() and not live.im_before.any() and not live.im_remainder.any()


def test_with_every_vector_part_zero_the_step_is_the_plain_path_bit_for_bit():
    simulation = DetectorLawSimulation(parse_nature_beam_world(twisted_world()))
    matter = [family.name for family in simulation.families].index("matter")
    rng = np.random.default_rng(11)
    now = rng.integers(-(1 << 16), 1 << 16, size=tuple(SHAPE), dtype=np.int64)
    before = rng.integers(-(1 << 16), 1 << 16, size=tuple(SHAPE), dtype=np.int64)
    live = simulation.planted_record(matter, now.copy(), before.copy(), twist=rotation_twist(800, 809))
    assert simulation._port_twists(live, False) is None
    content = simulation._effective_content(matter)
    num, den = simulation.pair_arrays(matter)
    reads, self_coefficient, wall = coefficients(num, den, GAMMA, content)
    expected, remainder = rule3(
        reads, simulation._axis_sums(now), self_coefficient, wall, now, before, np.zeros_like(now)
    )
    simulation._advance(live)
    assert np.array_equal(live.now, expected) and np.array_equal(live.remainder, remainder)
    assert live.im_now is None


def test_the_ports_along_a_records_own_component_book_nothing_of_it():
    """A record in the vector component z (part 3) is booked through the x and y Ports of a
    set alone (9.82 (3) (b), (c)); the same levels as a time part are booked through all."""
    simulation = DetectorLawSimulation(parse_nature_beam_world(twisted_world()))
    charge = [family.name for family in simulation.families].index("charge")
    assert simulation.families[charge].parts == (1, 3)
    rng = np.random.default_rng(13)
    now = rng.integers(-(1 << 12), 1 << 12, size=tuple(SHAPE), dtype=np.int64)
    before = rng.integers(-(1 << 12), 1 << 12, size=tuple(SHAPE), dtype=np.int64)
    scalar = simulation.planted_record(charge, now.copy(), before.copy())
    mask = np.zeros(tuple(SHAPE), dtype=bool)
    mask[4:7, 1:4, 1:4] = True
    whole = simulation.inward_flux(scalar, mask)
    # the time part is booked through every Port
    assert simulation.booked_axis(scalar) is None
    # the record in z: the z Ports skipped; the sum over the x and y Ports by hand
    transverse = simulation.planted_record(charge, now.copy(), before.copy(), part=3)
    assert simulation.booked_axis(transverse) == 2
    wall = simulation.kind_wall(charge)
    expected = 0
    for axis in (0, 1):
        for side in (1, -1):
            outside = ~np.roll(mask, side, axis=axis)
            port = mask & outside
            now_j = np.roll(now, side, axis=axis)
            before_j = np.roll(before, side, axis=axis)
            flux = now.astype(object) * before_j - before.astype(object) * now_j
            expected += int(np.sum(np.where(port & (flux > 0), flux, 0)))
    assert 0 < simulation.inward_flux(transverse, mask) == expected * wall <= whole


def test_the_loader_refuses_a_light_emitter_without_one_moment_axis_and_a_bad_table():
    document = on_the_file(emitter_world(stock=1, ticks=10), [512, 1])
    flat = json.loads(json.dumps(document))
    flat["measured"][0]["moment"] = [0, 0, 0]
    flat["stamp"] = input_stamp(flat)
    refused(flat, "lies on 0 axes")
    diagonal = json.loads(json.dumps(document))
    diagonal["measured"][0]["moment"] = [1, 1, 0]
    diagonal["stamp"] = input_stamp(diagonal)
    refused(diagonal, "lies on 2 axes")
    # the table on an inline world: the unit, the identities and the angles' order checked (the
    # nearest triple the generator's, `generator_numbers.twist_triple`, item 73)
    good = twisted_world()
    parse_nature_beam_world(good)
    for change, match in (
        (lambda t: t.__setitem__("unit", 7), "is not 4 Gamma 2\\^16"),
        (lambda t: t["coarse"].__setitem__(200, [3, 4, 6]), "is no triple of the table"),
        # a triple planted out of order: the loader checks the angles' order in integers (item 73)
        (lambda t: t["coarse"].__setitem__(200, [3, 4, 5]), "turns back below the entry before it"),
        (lambda t: t["fine"].pop(), "must be a list of 1024 to 1024 triples"),
    ):
        broken = json.loads(json.dumps(good))
        change(broken["twist_table"])
        broken["stamp"] = input_stamp(broken)
        with pytest.raises(ValueError, match=match):
            parse_nature_beam_world(broken)


def test_a_twist_beyond_the_coarse_table_is_refused_naming_the_port():
    simulation = DetectorLawSimulation(parse_nature_beam_world(twisted_world()))
    gravity = parts_of(simulation, "clicks")
    matter = [family.name for family in simulation.families].index("matter")
    x_part = gravity[1]
    x_part.now[6:8, :, :] = 1 << 20
    x_part.before[6:8, :, :] = 1 << 20
    x_part.silent = False
    simulation._sourced_ever[(gravity[0].family, 1)] = True
    live = simulation.planted_record(
        matter,
        np.ones(tuple(SHAPE), dtype=np.int64),
        np.zeros(tuple(SHAPE), dtype=np.int64),
        twist=rotation_twist(800, 809),
    )
    with pytest.raises(RuntimeError, match=r"beyond the twist table .*32768 coarse triples"):
        simulation._advance(live)
