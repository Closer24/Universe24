"""The generator by Rule3 alone (tools/body_generator.py): the read and division acts iterated to the first repeat give the bound mode at rest and in motion, the held field at rest under its family's pair is the well the mode sits on; a pair that binds nothing is refused."""

from __future__ import annotations

import json
import math
from fractions import Fraction

import numpy as np
import pytest
import scipy.sparse as sparse
import scipy.sparse.linalg as sparse_linalg

from event_universe.core.integer import MAX_WORK_INT
from event_universe.core.rule3 import coefficients, rule_total_bound
from event_universe.features.start import rest as start_rest
from tools.body_generator import (
    AT_REST,
    PERIODIC,
    amplitude_unit,
    arrivals,
    bound_mode,
    clock_pair,
    conserved_form,
    generate,
    moving_body,
    moving_mode,
    packet_current,
    period_by_the_rule,
    read_act,
    rule_integers,
    scaled_to_norm,
    to_amplitude,
    triple_of,
    two_levels,
)

GAMMA = 10_000
KIND = (800, 1200)
OPEN = (False, False, False)


def counted_cube(box: int, side: int, count: int) -> np.ndarray:
    counts = np.zeros((box, box, box), dtype=np.int64)
    low = (box - side) // 2
    counts[low : low + side, low : low + side, low : low + side] = count
    return counts


def float_top_mode(counts: np.ndarray, pair: tuple[int, int]) -> tuple[float, np.ndarray]:
    """The check's oracle in floats: the top eigenvector of the symmetric form on the periodic box, as the level a_i = phi_i p_i."""
    num, den = pair
    shape = counts.shape
    idx = np.arange(counts.size).reshape(shape)
    p = (GAMMA - counts).astype(float)
    u = (p / GAMMA) ** 2
    on_site = 2 - (1 + u) * (den - num) / den - 2 * num * u / den
    rows, cols, vals = [], [], []
    for axis in range(3):
        j = np.roll(idx, -1, axis=axis)
        bond = num * p * np.roll(p, -1, axis=axis) / (3 * den * GAMMA**2)
        rows += [idx.ravel(), j.ravel()]
        cols += [j.ravel(), idx.ravel()]
        vals += [bond.ravel(), bond.ravel()]
    rows.append(idx.ravel())
    cols.append(idx.ravel())
    vals.append(on_site.ravel())
    matrix = sparse.csr_matrix(
        (np.concatenate(vals), (np.concatenate(rows), np.concatenate(cols))),
        shape=(counts.size, counts.size),
    )
    value, vector = sparse_linalg.eigsh(matrix, k=1, which="LA")
    level = np.abs(vector[:, 0].reshape(shape)) * p
    return float(value[0]), level / np.linalg.norm(level)


def test_the_iteration_stops_at_the_first_repeat_and_gives_the_bound_mode():
    """A cube of side 4 at 3000 per Node on [800, 1200]: a fixed point at iteration 198, the float mode's rotation and profile to 10^-6, 0.76 inside the cube, the clock's period 8."""
    counts = counted_cube(12, 4, 3000)
    mode = bound_mode(counts, KIND, GAMMA)
    assert (mode.iterations, mode.cycle) == (198, 1)
    assert mode.rotation > Fraction(2 * KIND[0], KIND[1])
    value, level = float_top_mode(counts, KIND)
    assert abs(float(mode.rotation) - value) < 1e-6
    profile = mode.profile.astype(float)
    profile /= np.linalg.norm(profile)
    assert abs(float(np.sum(profile * level)) - 1) < 1e-6
    assert Fraction(75, 100) < mode.share_inside < Fraction(77, 100)
    assert int(np.abs(mode.profile).max()) == mode.amplitude
    clock = clock_pair(mode.rotation, mode.amplitude)
    assert clock[1] == mode.amplitude and period_by_the_rule(*clock) == round(
        2 * math.pi / math.acos(value / 2)
    )


def test_the_amplitude_unit_is_derived_from_the_width_and_the_fixed_point_stands_beyond_it():
    """A is the largest amplitude keeping Rule3's total inside int64 (between 2^22 and 2^23 here); the profile divided to A / 2 is a fixed point of the iteration at A / 2 within one unit."""
    counts = counted_cube(12, 4, 3000)
    amplitude = amplitude_unit(KIND, GAMMA, counts)
    reads, self_coefficient, wall = coefficients(KIND[0], KIND[1], GAMMA, 3000)
    assert amplitude == (MAX_WORK_INT - wall) // (6 * abs(reads[0]) + abs(self_coefficient) + wall)
    assert (1 << 22) < amplitude < (1 << 23)
    for content in (0, 3000):
        assert rule_total_bound(KIND[0], KIND[1], GAMMA, content, amplitude, True) <= MAX_WORK_INT
    assert rule_total_bound(KIND[0], KIND[1], GAMMA, 3000, amplitude + 1, True) > MAX_WORK_INT
    mode = bound_mode(counts, KIND, GAMMA)
    assert mode.amplitude == amplitude
    # the fixed point at the coarser grain A / 2: the profile divided to A / 2 by the division
    # act, then one read act and one division act at A / 2, returns within one unit of itself
    read, self_coefficient, wall = rule_integers(KIND, GAMMA, counts)
    (coarse,) = to_amplitude((mode.profile,), amplitude // 2)
    (again,) = to_amplitude(
        read_act((coarse,), (arrivals(coarse, PERIODIC),), read, self_coefficient, wall), amplitude // 2
    )
    assert int(np.abs(again - coarse).max()) <= 1
    with pytest.raises(ValueError, match="beyond int64"):
        to_amplitude((mode.profile,), 1 << 41)


def test_the_period_is_the_nearest_integer_to_two_pi_over_omega_with_no_pi():
    """The period is round(2 pi / acos(a / 2 b)) in integers: 9 for the light clock, 45 for the dark body."""
    assert period_by_the_rule(1651150, 1048576) == 9
    assert period_by_the_rule(2076636, 1048576) == 45
    b = 1 << 20
    for a in range(-2 * b + 1, 2 * b, 20_101):
        assert period_by_the_rule(a, b) == round(2 * math.pi / math.acos(a / (2 * b))), (a, b)
    assert period_by_the_rule(0, 1) == 4 and period_by_the_rule(1, 1) == 6


def test_the_two_levels_and_the_amplitude_from_the_count_and_the_norm():
    """The second level is the read act halved; the levels scaled to c T give the form within 10^-3."""
    counts = counted_cube(12, 4, 3000)
    mode = bound_mode(counts, KIND, GAMMA)
    read, self_coefficient, wall = rule_integers(KIND, GAMMA, counts)
    now, before = two_levels(mode.profile, read, self_coefficient, wall, PERIODIC)
    ratio = float(before[6, 6, 6]) / float(now[6, 6, 6])
    assert abs(ratio - float(mode.rotation) / 2) < 1e-4
    paces = GAMMA - counts
    form = conserved_form(now, before, self_coefficient, wall, KIND[0], paces, PERIODIC)
    assert form > 0
    doubled = conserved_form(2 * now, 2 * before, self_coefficient, wall, KIND[0], paces, PERIODIC)
    assert doubled == 4 * form
    norm = Fraction(int(np.sum(counts)) * 34026417078243063, 24990001)  # c T, the emitter's T of today
    scaled_now, scaled_before = scaled_to_norm(now, before, form, norm, mode.amplitude)
    reached = conserved_form(scaled_now, scaled_before, self_coefficient, wall, KIND[0], paces, PERIODIC)
    assert abs(reached / norm - 1) < Fraction(1, 1000)  # the rounding of levels a few tens in size
    assert 10 < int(np.abs(scaled_now).max()) < mode.amplitude
    assert scaled_now.dtype == np.int64 and scaled_before.dtype == np.int64


def test_the_moving_body_is_the_same_iteration_with_the_rotation_per_link():
    """At (1, 0, 1) the twisted iteration is the resting mode bit for bit and at (99, 20, 101) its rotation within the rest's (the gauge); the moving body of (e): the packet's velocity bisected to the named one, both senses."""
    counts = counted_cube(12, 4, 3000)
    rest = bound_mode(counts, KIND, GAMMA)
    still = moving_mode(counts, KIND, GAMMA, AT_REST)
    assert np.array_equal(still.re, rest.profile) and not still.im.any()
    assert still.rotation == rest.rotation and still.iterations == rest.iterations
    long_counts = np.zeros((24, 12, 12), dtype=np.int64)
    long_counts[10:14, 4:8, 4:8] = 3000
    long_rest = bound_mode(long_counts, KIND, GAMMA)
    triple = (99, 20, 101)
    moving = moving_mode(long_counts, KIND, GAMMA, triple)
    assert Fraction(2 * KIND[0], KIND[1]) < moving.rotation < long_rest.rotation
    # the stop is a two-cycle of the rounding: one more iteration returns a profile one unit away at most
    assert moving.cycle == 2
    # (e): the moving body is the rest mode with the phase k per Link; its velocity (the current over the form)
    # rises with j, the bisection finds the named one within the pair's resolution, the sense the momentum's sign
    quanta, unit = int(long_counts.sum()), 64
    moved = moving_body(long_counts, KIND, GAMMA, 3 * unit * quanta // 20, unit, 1024, rest=long_rest)
    assert moved.named == Fraction(1, 20) and moved.pair[0] == 1024 and 0 < moved.pair[1] < 1024
    assert abs(moved.velocity - moved.named) < Fraction(1, 1000) and moved.triple == triple_of(
        moved.pair
    )
    assert packet_current(moved.now, moved.before, KIND[0], PERIODIC) > 0
    back = moving_body(long_counts, KIND, GAMMA, -3 * unit * quanta // 20, unit, 1024, rest=long_rest)
    assert back.triple[1] < 0 and abs(back.velocity + moved.named) < Fraction(1, 1000)
    still_body = moving_body(long_counts, KIND, GAMMA, 0, unit, 1024, rest=long_rest)
    assert still_body.pair == (1024, 0) and np.array_equal(still_body.now, long_rest.profile)
    with pytest.raises(ValueError, match="beyond the packet's"):
        moving_body(long_counts, KIND, GAMMA, 3 * unit * quanta, unit, 1024, rest=long_rest)
    with pytest.raises(ValueError, match="no Pythagorean triple"):
        moving_mode(counts, KIND, GAMMA, (3, 3, 5))
    asymmetric = counted_cube(12, 4, 3000)
    asymmetric[1, 5, 5] = 100
    with pytest.raises(ValueError, match="mirrored along x"):
        moving_mode(asymmetric, KIND, GAMMA, triple)


def test_the_generator_reads_its_input_file_in_the_laws_form_and_refuses_by_name(tmp_path):
    """THE INPUT IS A FILE (the owner's word): a world file in the law's form (the GameBoard, the Node clock, the universe it names, one body by its Nodes and counts) gives the mode on the held fields the family reads plainly (a read by the sign skipped, a weight named in the integers); the refusals by name, [800, 809]'s shallow well."""

    def row(name, pair, held, reads):
        return {"name": name, "pair": pair, "held": held, "reads": reads}

    reads = [
        {"family": "gravity", "weight": "one", "by": 1},
        {"family": "charge", "weight": 1, "by": "q"},
    ]
    families = [
        row("gravity", [1, 4], {"count": "content"}, []),
        row("charge", [1, 1], {"count": "sign"}, []),
    ]
    families += [row("matter", list(KIND), None, reads), row("light", "body", None, [])]
    (tmp_path / "universe.json").write_text(
        json.dumps({"families": families, "integers": {"one": 1, "momentum_unit": 64}})
    )
    nodes = [{"node": [x, y, z], "count": 3000} for x in (3, 4) for y in (3, 4) for z in (3, 4)]
    body = {"family": "matter", "nodes": nodes, "momentum": [0, 0, 0], "momentum_before": [0, 0, 0]}
    body["phase_denominator"] = 64  # one form: every body carries the phase's m
    faces = {"x": "periodic", "y": "periodic", "z": "periodic"}
    world = {"shape": [8, 8, 8], "boundary": faces, "node_clock": GAMMA, "measured": [body]}
    world["universe"] = str(tmp_path / "universe.json")
    readings, box = generate(world), counted_cube(8, 2, 3000)
    reading = readings["bodies"][0]
    rest = start_rest(box, (1, 4))
    mode = bound_mode(box, KIND, GAMMA, content=rest.levels)
    assert reading["rotation"] == [mode.rotation.numerator, mode.rotation.denominator]
    assert reading["period"] == 8 and np.array_equal(reading["profile"], mode.profile)
    assert readings["rest"]["gravity"] == {
        "pair": [1, 4],
        "iterations": rest.iterations,
        "cycle": 1,
        "at_bodies": 3000,
        "at_corner": 0,
    }
    assert np.array_equal(reading["content"], rest.levels)
    still = reading["moving"]  # one path: at the momentum 0 the pair (m, 0) and the mode's levels
    assert still["phase_pair"] == [64, 0] and still["triple"] == [1, 0, 1]
    assert still["velocity_named"] == [0, 1] and np.array_equal(still["now"], mode.profile)
    moving = {**body, "momentum": [0, 3 * 64 * 24000 // 40, 0]}
    moved = generate({**world, "measured": [moving]})["bodies"][0]["moving"]
    assert moved["axis"] == 1 and moved["velocity_named"] == [1, 40] and moved["phase_pair"][0] == 64
    assert moved["now"].shape == (8, 8, 8) and abs(
        Fraction(*moved["velocity"]) - Fraction(1, 40)
    ) < Fraction(1, 100)

    def refused(entry: dict) -> str:
        return generate({**world, "measured": [entry]})["bodies"][0]["refused"]

    assert "moves along one axis" in refused({**body, "momentum": [1, 1, 0]})
    without = {k: v for k, v in body.items() if k != "phase_denominator"}
    assert "declares its phase_denominator" in refused(without)
    assert "the row's pair is 'body', not [num, den]" in refused({**body, "family": "light"})
    two = generate({**world, "measured": [body, {**body, "family": "light"}]})["bodies"]
    deeper = Fraction(
        *two[0]["in_the_worlds_well"]["rotation"]
    )  # a second body deepens the world's well:
    assert deeper != Fraction(*two[0]["rotation"]) and "refused" in two[1]  # the clock's rotation moves
    with pytest.raises(ValueError, match=r"the count binds no mode of the family \[800, 809\]"):
        bound_mode(counted_cube(8, 4, 3000), (800, 809), GAMMA)
    with pytest.raises(ValueError, match=r"the clock \[2, 1\] is no rotation"):
        period_by_the_rule(2, 1)
    with pytest.raises(ValueError, match="the counts stay in \\[0, Gamma\\)"):
        bound_mode(counted_cube(4, 2, GAMMA), KIND, GAMMA)
    with pytest.raises(ValueError, match="zero everywhere"):
        bound_mode(np.zeros((4, 4, 4), dtype=np.int64), KIND, GAMMA)
    with pytest.raises(ValueError, match="int64"):
        bound_mode(np.ones((4, 4, 4), dtype=np.int32), KIND, GAMMA)
