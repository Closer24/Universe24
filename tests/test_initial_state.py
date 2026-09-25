"""THE INPUT CHECKED LAWFUL OR REFUSED IN INTEGERS (the model owner's record 1886 of
2026-09-25; ALGEBRA.md 9.22 (3) and (7); BUILD.md section 26 items 20 and 21): the
initial state is stored once in the world file (every seeded body's integer profile at
both levels, its mode's clock [a, b] and its born pair, the generator's, under the
file's `input` stamp: the law identifier and the hash of those integers) and the loader
says at load whether it is lawful, with no float: the stamp's law and hash, the
eigen-equation's residual at every Node within its proved bound, the clock above the
band's top and below 2, the bodies disjoint, at most three families; and the generator
as the board's own operator iterated in integers (record 1898). Every reading here is
the loader's on the test worlds of the line (COMPUTATION); no pin.
"""

from __future__ import annotations

import json

import numpy as np
import pytest

from event_universe.diagnostics.massive_record_margin import (
    accurate_mode,
    block_cells,
    integer_mode_iteration,
)
from event_universe.events.world import (
    LAW_IDENTIFIER,
    MOST_FAMILIES,
    input_stamp,
    mode_residual,
    parse_nature_beam_world,
    six_neighbours_flat,
)
from tests.test_emitter import emitter_world
from tests.test_massive_record import light_clock_world


def peak_of(profile: list[int]) -> int:
    return max(range(len(profile)), key=lambda index: abs(profile[index]))


def restamped(document: dict) -> dict:
    """The document with its `input` stamp rewritten for its integers as they stand, so
    that the check under test speaks and not the hash's."""
    document["input"] = input_stamp(document)
    return document


def test_a_a_generated_world_is_lawful_and_carries_its_clock_and_stamp():
    """The emitter world (the well [800, 801] of side 12 on the chain of 80, the amplitude
    100) and the light clock's chain (the amplitude 50 x 2^20): each body's profile carries
    its clock [a, b] with b a power of two at least twice the amplitude and at least 2^20,
    a / b above the family's band top 2 x 800 / 809 and below 2, and the file its `input`
    stamp with this loader's law identifier and the hash of the integers; the loader
    admits the file and the definition carries the clock; the residual of the profile
    against the body's operator is within the bound at every Node (read through the
    loader's own function)."""
    for document, amplitude in (
        (emitter_world(stock=2), 100),
        (light_clock_world("closed", False), 50 << 20),
    ):
        assert document["input"] == input_stamp(document)
        assert document["input"]["law"] == LAW_IDENTIFIER and len(document["input"]["hash"]) == 64
        world = parse_nature_beam_world(document)
        block = world.measured[0].block
        assert block is not None and block.profile is not None and block.clock is not None
        a, b = block.clock
        assert document["measured"][0]["clock"] == [a, b]
        assert b >= 2 * amplitude and b >= 1 << 20 and b & (b - 1) == 0
        assert 2 * 800 * b < a * 809 and a < 2 * b
        shape = (int(world.shape[0]), int(world.shape[1]), int(world.shape[2]))
        count = shape[0] * shape[1] * shape[2]
        num, den = [800] * count, [809] * count
        corner = int(world.measured[0].position[0])
        for x in range(corner, corner + block.extents[0]):
            num[x], den[x] = 800, 801
        residual, bound, _ = mode_residual(
            block.profile, num, den, block.clock, shape, world.kind_periodic(1)
        )
        assert 0 <= residual <= bound


def test_b_a_profile_off_the_mode_is_refused_and_one_unit_off_is_within_the_rounding():
    """The residual bound (9.22 (7) (ii), proved for the rounded profile of an exact mode):
    the profile with its peak doubled is refused naming the Node, its residual and the
    bound; the profile with its peak zeroed is refused; the profile with one unit added at
    the peak is ADMITTED (the edge case: a one-unit change is within the rounding the bound
    allows, so the check does not single it out; the same input then gives another output,
    the property test's test 8). The stamp is rewritten for every changed profile so that
    the residual speaks (the hash's own refusal is test g)."""
    document = emitter_world(stock=2)
    profile = document["measured"][0]["seed"]
    peak = peak_of(profile)
    for change, refused in (
        (lambda p: p.__setitem__(peak, 2 * p[peak]), True),
        (lambda p: p.__setitem__(peak, 0), True),
        (lambda p: p.__setitem__(peak, p[peak] + 1), False),
    ):
        changed = json.loads(json.dumps(document))
        change(changed["measured"][0]["seed"])
        restamped(changed)
        if refused:
            with pytest.raises(
                ValueError,
                match=r"seed is not the mode of its family's operator.*at Node \[\d+, 0, 0\] the "
                r"eigen-equation's residual \d+ is above the bound \d+",
            ):
                parse_nature_beam_world(changed)
        else:
            parse_nature_beam_world(changed)


def test_c_the_clocks_refusals_name_the_rule():
    """The clock [a, b] beside a profile: absent, refused naming the key; not [a, b] of two
    positive integers, refused; b below the amplitude, refused; a / b at the band's top
    (a = floor(2 x 800 b / 809)), refused as no bound mode; a = 2 b, refused as a runaway;
    a clock beside a scalar seed, refused."""

    def refused(mutate, message):
        document = emitter_world(stock=2)
        mutate(document["measured"][0])
        restamped(document)
        with pytest.raises(ValueError, match=message):
            parse_nature_beam_world(document)

    a, b = emitter_world(stock=2)["measured"][0]["clock"]
    refused(lambda entry: entry.pop("clock"), "seed as a profile needs the mode's `clock`")
    refused(lambda entry: entry.__setitem__("clock", [a]), r"clock must be \[a, b\]")
    refused(lambda entry: entry.__setitem__("clock", [a, 0]), r"clock must be \[a, b\]")
    refused(
        lambda entry: entry.__setitem__("clock", [round(a * 64 / b), 64]),
        "b must be at least the profile's amplitude",
    )
    refused(
        lambda entry: entry.__setitem__("clock", [2 * 800 * b // 809, b]),
        "is not above the band's top 2 x 800 / 809",
    )
    refused(
        lambda entry: entry.__setitem__("clock", [2 * b, b]),
        "is at or above 2: the mode is a runaway",
    )

    def scalar(entry):
        entry["seed"] = 100
        entry.pop("emitter")

    refused(scalar, "clock is admitted only beside a profile")


def test_d_at_most_three_families():
    """Three families are admitted (the emitter world's two and a third), a fourth is
    refused naming the count and the bound (record 1875; 9.22 (2))."""
    document = emitter_world(stock=2)
    assert len(document["families"]) <= MOST_FAMILIES
    while len(document["families"]) < MOST_FAMILIES:
        document["families"].append(
            {"name": f"family_{len(document['families'])}", "quantum": 1, "pair": [800, 809]}
        )
    parse_nature_beam_world(document)
    document["families"].append({"name": "fourth", "quantum": 1, "pair": [800, 809]})
    with pytest.raises(
        ValueError,
        match=f"families declares {MOST_FAMILIES + 1}; at most {MOST_FAMILIES} families",
    ):
        parse_nature_beam_world(document)


def test_e_bodies_are_whole_and_disjoint():
    """Two bodies whose cells overlap are refused naming both (a light-kind block of side 1
    inside A's cells on the light clock's chain); a block beyond a face of the board is
    refused by the fit check naming the axis and the vertex (a light-kind block of side 3 at
    x = 171 on the open chain of 173 reaches 173 beyond the face at 172); a block of side 3
    at x = 160, whole, is admitted."""

    def wall(x, side):
        return {
            "position": [x, 0, 0],
            "family": "light",
            "amount": 1,
            "phase": 0,
            "momentum": [0, 0, 0],
            "fixed": True,
            "side": side,
            "pair": [1, 2],
        }

    overlap = light_clock_world("open", False)
    overlap["measured"].append(wall(105, 1))
    with pytest.raises(ValueError, match=r"measured\[1\] and measured\[0\] overlap"):
        parse_nature_beam_world(overlap)
    cut = light_clock_world("open", False)
    cut["measured"].append(wall(171, 3))
    with pytest.raises(
        ValueError, match=r"side 3 at 171 on the axis x reaches 173 beyond the face at 172"
    ):
        parse_nature_beam_world(cut)
    whole = light_clock_world("open", False)
    whole["measured"].append(wall(160, 3))
    parse_nature_beam_world(whole)


def test_f_the_six_neighbour_read_in_integers():
    """`six_neighbours_flat` on a 3 x 1 x 1 chain: open on x, [1, 2, 3] reads [2, 4, 2];
    periodic on x, [5, 3, 1] with y and z of extent 1 periodic (the Node itself twice per
    folded axis): [3 + 1 + 4 x 5, 5 + 1 + 4 x 3, 3 + 5 + 4 x 1]."""
    assert six_neighbours_flat([1, 2, 3], (3, 1, 1), (False, False, False)) == [2, 4, 2]
    assert six_neighbours_flat([5, 3, 1], (3, 1, 1), (True, True, True)) == [24, 18, 12]


def test_g_the_input_stamp_the_law_and_the_hash():
    """THE FILE'S HASH AND THE LAW IT WAS MADE UNDER (9.22 (7) (i)): a seeded world without
    its `input` stamp is refused naming the key; a stamp under another law is refused naming
    both laws; a stamp whose hash is not the digest of the integers (the profile changed by
    one unit without restamping, the clock changed, the born pair changed) is refused as
    not the ones the generator wrote; a world with no profile needs no stamp (the emitter
    world on its scalar seed, its emitter removed); the stamp is the same from the raw
    document and from the parsed integers (the generated world loads, test a)."""
    missing = emitter_world(stock=2)
    del missing["input"]
    with pytest.raises(ValueError, match="declares a seeded body and no `input` stamp"):
        parse_nature_beam_world(missing)
    other = emitter_world(stock=2)
    other["input"]["law"] = "another law"
    with pytest.raises(ValueError, match="input.law is 'another law'; this loader's law is"):
        parse_nature_beam_world(other)

    def unit(document):
        seed = document["measured"][0]["seed"]
        seed[peak_of(seed)] += 1

    def clock(document):
        document["measured"][0]["clock"][0] += 1

    def born(document):
        now = document["measured"][0]["emitter"]["born"][0] + 1
        document["measured"][0]["emitter"]["born"] = [now, -now]

    for change in (unit, clock, born):
        changed = emitter_world(stock=2)
        change(changed)
        with pytest.raises(ValueError, match="is not the digest of the initial state's integers"):
            parse_nature_beam_world(changed)
    unseeded = emitter_world(stock=2, on_mode=False)
    assert "input" not in unseeded
    del unseeded["measured"][0]["emitter"]
    parse_nature_beam_world(unseeded)


def test_h_the_generator_as_the_operator_iterated_in_integers():
    """RECORD 1898 (ALGEBRA.md 9.22 (7)): from the cells' indicator on the emitter world's
    chain of 80 (the well [800, 801] in the kind [800, 809]) the integer power iteration
    3 den v' = num S_6(v) + 6 den v with the remainder kept, renormalised by a power-of-two
    shift, converges to the bound mode: after 4000 iterations its levels, scaled to the
    amplitude 2^20, pass the loader's residual bound with the accurate clock and agree with
    ARPACK's rounded mode within 200 units at every Node (78 read, COMPUTATION: the
    iteration's floor, the rounding noise of every step fed into the next mode and damped
    only by the gap, about 1 / gap units at the amplitude; the float power iteration itself
    agrees with ARPACK to the unit), and are bit for bit the same on a second run (the same
    integers in, the same out)."""
    document = emitter_world(stock=1)
    world = parse_nature_beam_world(document)
    entry = world.measured[0]
    block = entry.block
    assert block is not None
    shape = (int(world.shape[0]), 1, 1)
    wrap = world.kind_periodic(entry.family)
    cells = block_cells(shape, (int(entry.position[0]), 0, 0), block.side, wrap)
    num = np.where(cells, block.pair[0], 800)
    den = np.where(cells, block.pair[1], 809)
    amplitude = 1 << 20
    start = np.where(cells, amplitude, 0).astype(np.int64)
    first = integer_mode_iteration(start, num, den, wrap, amplitude, 4000)
    second = integer_mode_iteration(start, num, den, wrap, amplitude, 4000)
    assert np.array_equal(first, second)
    lambda_max, mode = accurate_mode(world, 0)
    expected = np.rint(mode * amplitude).astype(np.int64)
    scaled = np.rint(first.astype(np.float64) * amplitude / np.max(np.abs(first))).astype(np.int64)
    assert int(np.max(np.abs(scaled - expected))) <= 200
    b = 1 << 22
    clock = (round(lambda_max * b), b)
    flat = [int(v) for v in scaled.ravel()]
    residual, bound, _ = mode_residual(
        flat, [int(v) for v in num.ravel()], [int(v) for v in den.ravel()], clock, shape, wrap
    )
    assert residual <= bound
