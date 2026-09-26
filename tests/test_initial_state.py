"""THE INPUT CHECKED LAWFUL OR REFUSED IN INTEGERS (the model owner's record 1886 of
2026-09-25; ALGEBRA.md 9.22 (3) and (7); BUILD.md section 26 items 20 and 21): the
initial state is stored once in the world file (every seeded body's integer profile at
both levels, its mode's clock [a, b] and its given pair, the generator's, under the
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
    body_node_mask,
    integer_mode_iteration,
    iterated_mode,
)
from event_universe.events.world import (
    MOST_FAMILIES,
    mode_residual,
    six_neighbours_flat,
)
from event_universe.world_files import input_stamp, parse_nature_beam_world
from tests.test_emitter import emitter_world, massive_generator, reads
from tests.test_massive_record import light_clock_world, massive_world
from tests.test_receiver_by_name import CLOSED_CHAIN, emitter


def peak_of(profile: list[int]) -> int:
    return max(range(len(profile)), key=lambda index: abs(profile[index]))


def restamped(document: dict) -> dict:
    """The document with its `input` stamp rewritten for its integers as they stand, so
    that the check under test speaks and not the hash's."""
    document["stamp"] = input_stamp(document)
    return document


def test_a_generated_world_is_lawful_and_carries_its_clock_and_stamp():
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
        (light_clock_world("closed", False), 50 << 12),
    ):
        assert document["stamp"] == input_stamp(document)
        assert set(document["stamp"]) == {"hash"} and len(document["stamp"]["hash"]) == 64
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


def test_a_profile_off_the_mode_is_refused_and_one_unit_off_is_within_the_rounding():
    """The residual bound (9.22 (7) (ii), proved for the rounded profile of an exact mode):
    the profile with its peak doubled is refused naming the Node, its residual and the
    bound; the profile with its peak zeroed is refused; the profile with one unit added at
    the peak is ADMITTED (the edge case: a one-unit change is within the rounding the bound
    allows, so the check does not single it out; the same input then gives another output,
    the property test's test 8), read on a side-12 well [800, 801] seeded by the generator
    on the emitter world's chain (the 32-Node well of the given train's emitter sits at the
    bound's edge: the iteration's floor of 276 units leaves no unit of slack, and the peak
    plus one is refused there naming the Node). The stamp is rewritten for every changed
    profile so that the residual speaks (the hash's own refusal is test g)."""
    document = emitter_world(stock=2, on_mode=False)
    document["measured"] = [
        {
            "position": [5, 0, 0],
            "family": "matter",
            "amount": 1,
            "stocks": {},
            "ramp": 0,
            "start": 0,
            "momentum": [0, 0, 0],
            "side": 12,
            "q": 0,
            "spin": [0, 0, 0],
            "twist": 0,
            "moment": [0, 0, 0],
            "pair": [800, 801],
            "seed": 1 << 20,
            "margin": "control",
        }
    ]
    document["detectors"] = []
    massive_generator().seed_on_the_mode(document)
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


def test_the_clocks_refusals_name_the_rule():
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


def test_at_most_five_families():
    """Five families are admitted (the emitter world's four, the families of clicks and of
    charge among them, and a fifth), a sixth is refused naming the count and the bound (the
    owner's constant: record 1875's three, four since the family of clicks, record 1982,
    five since the family of charge, ALGEBRA.md 9.48; BUILD.md section 26 item 35)."""
    document = emitter_world(stock=2)
    assert len(document["universe"]) <= MOST_FAMILIES
    while len(document["universe"]) < MOST_FAMILIES:
        document["universe"].append(
            {
                "name": f"family_{len(document['universe'])}",
                "quantum": 1,
                "pair": [800, 809],
                "charge": 0,
                "reads": reads(),
            }
        )
    parse_nature_beam_world(restamped(document))
    document["universe"].append(
        {"name": "sixth", "quantum": 1, "pair": [800, 809], "charge": 0, "reads": reads()}
    )
    restamped(document)
    with pytest.raises(
        ValueError,
        match=f"families declares {MOST_FAMILIES + 1}; at most {MOST_FAMILIES} families",
    ):
        parse_nature_beam_world(document)


def test_bodies_are_whole_and_disjoint():
    """Two bodies whose Nodes overlap are refused naming both (a light-kind block of side 1
    inside A's Nodes on the light clock's chain); a block beyond a face of the board is
    refused by the fit check naming the axis and the vertex (a light-kind block of side 3 at
    x = 171 on the open chain of 173 reaches 173 beyond the face at 172); a block of side 3
    at x = 160, whole, is admitted."""

    def wall(x, side):
        return {
            "position": [x, 0, 0],
            "family": "light",
            "amount": 1,
            "stocks": {},
            "ramp": 0,
            "start": 0,
            "momentum": [0, 0, 0],
            "side": side,
            "q": 0,
            "spin": [0, 0, 0],
            "twist": 0,
            "moment": [0, 0, 0],
            "pair": [1, 2],
        }

    overlap = light_clock_world("open", False)
    overlap["measured"].append(wall(105, 1))
    with pytest.raises(ValueError, match=r"measured\[1\] and measured\[0\] overlap"):
        parse_nature_beam_world(restamped(overlap))
    cut = light_clock_world("open", False)
    cut["measured"].append(wall(171, 3))
    with pytest.raises(
        ValueError, match=r"side 3 at 171 on the axis x reaches 173 beyond the face at 172"
    ):
        parse_nature_beam_world(restamped(cut))
    whole = light_clock_world("open", False)
    whole["measured"].append(wall(160, 3))
    parse_nature_beam_world(restamped(whole))


def test_two_wells_of_one_family_may_stand_anywhere():
    """THE SEPARATION RULE OF 9.35 IS RETIRED (ALGEBRA.md 9.96 (4); the one stroke, commit 6;
    the tail check of BUILD.md section 26 item 28 HISTORY): two wells of the matter kind on
    the closed chain of 400, A at [100, 132) with its profile at 50 x 2^12 (its last nonzero
    Node 180, HOST) and B at [170, 202) inside A's tail, or at [232, 264) beyond it: both
    admitted, each body's record its own array meeting the other through the held
    families alone. A light-kind wall at B's place is another family, admitted as before."""
    for b_corner, admitted in ((170, True), (232, True)):  # the tail ends at 180 at the seed 50 x 2^12
        document = massive_world([400, 1, 1], CLOSED_CHAIN, [800, 809])
        document["ticks"] = 10
        document["measured"] = [emitter(100, None), emitter(b_corner, None, direction=[-1, 0, 0])]
        for entry in document["measured"]:
            del entry["emitter"]  # two wells, no giving: the loader's tail check alone
        profile = massive_generator().mode_profile(document, 0, amplitude=50 << 12)
        document["measured"][0]["seed"] = profile
        assert (
            max(x for x in range(400) if profile[x] != 0) == 180
        )  # at the seed 50 x 2^12 (194 at 50 x 2^20 HISTORY)
        restamped(document)
        if admitted:
            parse_nature_beam_world(document)
            continue
        with pytest.raises(
            ValueError,
            match=r"measured\[0\]\.seed is 8 at Node \[170, 0, 0\] of measured\[1\]: a body's mode "
            r"ends before another body of its family begins",
        ):
            parse_nature_beam_world(document)
    wall = light_clock_world("closed", False)
    wall["measured"].append(
        {
            "position": [160, 0, 0],
            "family": "light",
            "amount": 1,
            "stocks": {},
            "ramp": 0,
            "start": 0,
            "momentum": [0, 0, 0],
            "side": 3,
            "q": 0,
            "spin": [0, 0, 0],
            "twist": 0,
            "moment": [0, 0, 0],
            "pair": [1, 2],
        }
    )
    parse_nature_beam_world(restamped(wall))


def test_the_six_neighbour_read_in_integers():
    """`six_neighbours_flat` on a 3 x 1 x 1 chain: open on x, [1, 2, 3] reads [2, 4, 2];
    periodic on x, [5, 3, 1] with y and z of extent 1 periodic (the Node itself twice per
    folded axis): [3 + 1 + 4 x 5, 5 + 1 + 4 x 3, 3 + 5 + 4 x 1]."""
    assert six_neighbours_flat([1, 2, 3], (3, 1, 1), (False, False, False)) == [2, 4, 2]
    assert six_neighbours_flat([5, 3, 1], (3, 1, 1), (True, True, True)) == [24, 18, 12]


def test_the_input_stamp_the_law_and_the_hash():
    """THE FILE'S HASH (9.22 (7) (i); 9.90 (3) (c)): a seeded world without its `stamp` is
    refused naming the key; a stamp carrying a law's name is refused naming the key (no law
    identifier, 9.90 (1)); a stamp whose hash is not the digest of the whole file (the profile changed by
    one unit without restamping, the clock changed, the given pair changed, the ticks changed:
    the stamp covers every key, BUILD.md section 26 item 28) is refused as not the file the
    generator wrote; a world with no profile needs no stamp (the emitter
    world on its scalar seed, its emitter removed); the stamp is the same from the raw
    document and from the parsed integers (the generated world loads, test a)."""
    missing = emitter_world(stock=2)
    del missing["stamp"]
    with pytest.raises(ValueError, match="declares a seeded body and no `stamp`"):
        parse_nature_beam_world(missing)
    other = emitter_world(stock=2)
    other["stamp"]["law"] = "another law"
    with pytest.raises(ValueError, match="stamp has unknown keys: law"):
        parse_nature_beam_world(other)

    def unit(document):
        seed = document["measured"][0]["seed"]
        seed[peak_of(seed)] += 1

    def clock(document):
        document["measured"][0]["clock"][0] += 1

    def weight(document):
        # a unit on the window's weight (the loader admits it; the stamp's hash is what
        # refuses, ALGEBRA.md 9.22 (7) (i); the train's profile retired at commit 7)
        document["measured"][0]["emitter"]["weight"] += 1

    def ticks(document):
        document["ticks"] += 1

    for change in (unit, clock, weight, ticks):
        changed = emitter_world(stock=2)
        change(changed)
        with pytest.raises(ValueError, match="is not the digest of the file"):
            parse_nature_beam_world(changed)
    unseeded = emitter_world(stock=2, on_mode=False)
    assert "stamp" not in unseeded
    del unseeded["measured"][0]["emitter"]
    parse_nature_beam_world(unseeded)


def test_the_generator_as_the_operator_iterated_in_integers():
    """THE GENERATOR WITH THE STOP (the model owner's word of 2026-09-25, 04:10Z, closing
    record 1898; ALGEBRA.md 9.22 (7); BUILD.md section 26 item 25): on the emitter world's
    chain of 80 (the well [800, 801] in the kind [800, 809]) `iterated_mode` iterates the law's
    own operator 3 den v' = num S_6(v) + 6 den v + r from the Nodes' indicator at the working
    amplitude 2^28 (scaled to the declared 2^20), reads
    the clock as the operator's quotient over the board, and stops at the first iteration at which the
    scaled profile passes the loader's own residual bound with that clock (2487 iterations
    read on the 32-Node well of the given train's emitter on the closed chain, its border the
    world's (one border for every family, BUILD.md section 26 item 28; 1805 with the matter
    border periodic, HISTORY), COMPUTATION; 1653 on the side-12
    well, 1817 at the working amplitude 2^20, which left the muon layer's well hovering at
    1.5 times the bound, BUILD.md section 26 item 25 amended); the result is bit
    for bit the same on a second run; the profile it
    writes passes `mode_residual` (the stop's own condition, read again here) and agrees with
    the host's eigensolver (ARPACK, a diagnostic now) within 500 units at every Node (467
    read on the 32-Node well five Links from the closed chain's zero face, 276 with the matter
    border periodic, 204 on the side-12 well: the iteration's floor, the rounding noise of every step fed into the next mode and
    damped only by the gap, about 1 / gap units at the amplitude), its clock within 4 units of
    ARPACK's rounded 2 cos omega at the denominator 2^22 (0 read; 2 at 2^20). The fixed-count
    iteration
    (`integer_mode_iteration`, the same step 4000 times) lands within the same 300 units. The
    edge: a limit below the stop refuses, naming the last residual against the bound."""
    document = emitter_world(stock=1)
    world = parse_nature_beam_world(document)
    entry = world.measured[0]
    block = entry.block
    assert block is not None
    shape = (int(world.shape[0]), 1, 1)
    wrap = world.kind_periodic(entry.family)
    nodes = body_node_mask(shape, (int(entry.position[0]), 0, 0), block.extents, wrap)
    num = np.where(nodes, block.pair[0], 800)
    den = np.where(nodes, block.pair[1], 809)
    amplitude = 1 << 20
    profile, clock, iterations = iterated_mode(world, 0, amplitude)
    assert iterated_mode(world, 0, amplitude) == (profile, clock, iterations)
    assert 1000 < iterations < 4000 and clock[1] == 1 << 22
    num_flat = [int(v) for v in num.ravel()]
    den_flat = [int(v) for v in den.ravel()]
    residual, bound, _ = mode_residual(profile, num_flat, den_flat, clock, shape, wrap)
    assert residual <= bound
    assert max(profile) == amplitude and min(profile) >= 0
    lambda_max, mode = accurate_mode(world, 0)
    expected = np.rint(mode * amplitude).astype(np.int64).ravel()
    assert int(np.max(np.abs(np.array(profile) - expected))) <= 500
    assert abs(clock[0] - round(lambda_max * clock[1])) <= 4
    start = np.where(nodes, amplitude, 0).astype(np.int64)
    fixed = integer_mode_iteration(start, num, den, wrap, amplitude, 4000)
    scaled = np.rint(fixed.astype(np.float64) * amplitude / np.max(np.abs(fixed))).astype(np.int64)
    assert int(np.max(np.abs(scaled.ravel() - expected))) <= 300
    with pytest.raises(ValueError, match="did not stop within 100 iterations: the last residual"):
        iterated_mode(world, 0, amplitude, limit=100)
