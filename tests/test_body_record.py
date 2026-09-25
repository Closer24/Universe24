"""THE BODY RECORD (the model owner's word of 2026-09-25 in the mathematician's session, "already
now, because it is generic; a body holds real parameters, and then it is a special Node in the
simulator; it can be checked that it is equivalent"; ALGEBRA.md 9.46 (1) to (3) and (9), 9.50 (8),
9.49 (3); BUILD.md section 26 item 37): under the world key `body_record` every seeded block is
held as one Node with a shape: its profile stored and never stepped, its own rows off the
GameBoard, and one rotation (a, b, r) stepped by the two-term rule on its clock pair [num_c,
den_c] at the pace of its Nodes, den_c Gamma a' + r' = (num_c p + 2 den_c (Gamma - p)) a -
den_c Gamma b + r, the remainder in [0, den_c Gamma); its residue its own remainder on its own
wheel, read at the click at the seat (the centre Node); its tick the count of intervals against
(2 u + 1) P / (2 W) as the lattice body's; the given rows the file's, set on the body's Nodes as
before. THE EQUIVALENCE (9.46 (4), the gate): (i) the ticks agree in distribution between the
two forms (the mean cycle length, the residues spread on the wheel, no runs of one-interval
cycles beyond a fair draw's); (ii) the rotation agrees as a rational with the lattice body's at
every content within the profile's rounding; (iii) the same given rows at each tick; (iv) the
block's count equal over the run; (v) the family of clicks' field identical where nothing is
given. Every number a COMPUTATION on the rule's integers; no pin."""

from __future__ import annotations

import json
import math
from fractions import Fraction

import numpy as np
import pytest

from event_universe.events.detector_law import UNIT, DetectorLawSimulation
from event_universe.events.rule import rule_coefficients
from event_universe.events.world import input_stamp, parse_nature_beam_world
from tests.test_emitter import emitter_world, massive_generator
from tests.test_flux_reading import planted
from tests.test_massive_record import block_world

PERIODIC = {"x": "periodic", "y": "periodic", "z": "periodic"}


def with_body_record(document: dict, on: bool) -> dict:
    """The document with `body_record` set and the input stamp renewed over the whole file
    (the generators build with the key off: the profile and the clock pair are written first,
    the loader's check under the key reads them)."""
    copy = json.loads(json.dumps(document))
    copy["body_record"] = on
    copy["input"] = input_stamp(copy)
    return copy


def cube_world(ticks: int = 400) -> dict:
    """A solitary body: the block of side 6 on the matter kind [800, 809] with the well [800,
    801] at the amplitude 2^20, seeded on its bound mode by the generator (its profile and its
    clock pair under the stamp), on a periodic 16^3 board; no emitter, nothing given."""
    document = block_world(
        [16, 16, 16],
        PERIODIC,
        [800, 809],
        [{"position": [5, 5, 5], "side": 6, "pair": [800, 801], "seed": 1 << 20, "margin": "control"}],
        ticks=ticks,
    )
    document["age_bound"] = 100000  # a periodic board keeps every ray: the store's bound
    massive_generator().seed_on_the_mode(document)
    return document


def rotation_of(levels: list[int]) -> Fraction | None:
    """2 cos omega read from three consecutive levels, (a_next + a_before) / a_now, where the
    middle level is not 0."""
    a_before, a_now, a_next = levels
    if a_now == 0:
        return None
    return Fraction(a_next + a_before, a_now)


def test_the_rotation_steps_by_the_two_term_rule_and_agrees_with_the_lattice_body():
    """(ii), (iv), (v) on the solitary cube: the body record's rotation satisfies den_c Gamma
    a_next + r' = K a_now - den_c Gamma a_before + r exactly at every interval with K = num_c p +
    2 den_c (Gamma - p) at the body's pace (the content 1 at its Nodes), its remainder in [0,
    den_c Gamma); its 2 cos omega' read from three consecutive levels is K / (den_c Gamma)
    within 2 x 10^-6 at the levels above half the amplitude (the remainder's jitter over the
    level), and the lattice body's, read the same way at its centre Node, agrees with it within
    10^-4 (the profile's rounding, 9.46 (9) (a): no bit-equal rational exists for a lattice
    body; the median 6 x 10^-6 and the worst 4.5 x 10^-5 over 400 intervals on this cube); the wheel in the vacuum's units is den_c /
    gcd(num_c, den_c) times Gamma / gcd(Gamma, ...) as the rule's gcd gives; the block's count
    (its cycles) over 400 intervals is the same on both forms within one; the body's invariant
    e = den_c Gamma (a^2 + b^2) - K a b jitters below 10^-4 of itself (2 x 10^-5 read); the family of clicks'
    field is identical on both forms at every interval (nothing given, the same hold). The edge
    case: the lattice body's own rows are on the GameBoard and the body record's are not."""
    document = cube_world()
    lattice = DetectorLawSimulation(parse_nature_beam_world(with_body_record(document, False)))
    seated = DetectorLawSimulation(parse_nature_beam_world(with_body_record(document, True)))
    lattice_block, seated_block = lattice.blocks[0], seated.blocks[0]
    assert lattice_block.own is not None and lattice_block.seat is None
    assert seated_block.seat is not None and seated_block.own is None
    assert seated_block.own is None and all(
        not seated.families[live.family].massive_kind for live in seated.records.values()
    )
    body = seated_block.seat
    centre = tuple(int(axis[0]) for axis in np.nonzero(seated.centre_mask(seated_block)))
    profile = np.array(document["measured"][0]["seed"], dtype=np.int64).reshape(seated.shape)
    assert (body.now, body.before, body.remainder) == (int(profile[centre]), int(profile[centre]), 0)
    # THE SEAT'S RULE (ALGEBRA.md 9.60 (2), 9.57 (1)): the one rule with the six reads returning
    # the seat, the pair [num_c, 2 den_c] and the seat's own level: its coefficient on a is 6 R
    # + S and its wall w, the weak-field rule's integers at that pair and level; asserted once
    num_c, den_c = seated_block.definition.clock
    pace, gamma = seated.node_clock_pair(centre, seated_block.family)
    assert (pace, gamma) == (gamma - 1, gamma)
    assert seated.seat_rule(seated_block) == (num_c, 2 * den_c, gamma, 1)
    coefficient, wall = seated.seat_coefficients(seated_block)
    read, self_coefficient, wall_rule = rule_coefficients(num_c, 2 * den_c, gamma, 1, True)
    assert wall == wall_rule == 12 * den_c * gamma**2
    assert coefficient == 6 * read + self_coefficient
    assert seated.one_rule(num_c, 2 * den_c, gamma, 1, 6 * body.now, body.now, body.before, 0) == (
        (coefficient * body.now - wall * body.before) // wall,
        (coefficient * body.now - wall * body.before) % wall,
    )
    forms = []
    seated_levels = [body.before, body.now]
    lattice_levels = [int(lattice_block.own.before[centre]), int(lattice_block.own.now[centre])]
    for _ in range(400):
        a_before, a_now, r = body.before, body.now, body.remainder
        seated.step()
        lattice.step()
        # the rule's identity, exact
        assert wall * body.now + body.remainder == coefficient * a_now - wall * a_before + r
        assert 0 <= body.remainder < wall and body.before == a_now
        seated_levels.append(body.now)
        lattice_levels.append(int(lattice_block.own.now[centre]))
        forms.append(seated.seat_form(seated_block))
        assert np.array_equal(seated.held_record("content").now, lattice.held_record("content").now)
        assert np.array_equal(
            seated.held_record("content").remainder, lattice.held_record("content").remainder
        )
    expected = Fraction(coefficient, wall)
    # the read at the levels above half the amplitude: (r' - r) / (wall a_now) below 2 x 10^-6
    # on the body record; the profile's rounding on the lattice body below 10^-4 (the median
    # 6 x 10^-6, the worst 4.5 x 10^-5 over 400 intervals on this cube, COMPUTATION)
    half = 1 << 19
    read = [rotation_of(seated_levels[i : i + 3]) for i in range(len(seated_levels) - 2)]
    read = [value for value in read if value is not None and abs(value.denominator) > half]
    assert len(read) > 100 and all(abs(value - expected) < Fraction(2, 10**6) for value in read)
    lattice_read = [rotation_of(lattice_levels[i : i + 3]) for i in range(len(lattice_levels) - 2)]
    lattice_read = [v for v in lattice_read if v is not None and abs(v.denominator) > half]
    assert len(lattice_read) > 100
    # under the weak field the lattice body's profile (the plain rule's eigenvector) is not
    # the rule's own at its level, so its read jitters at c / Gamma (the worst 4 x 10^-4,
    # the median 10^-6, COMPUTATION); the seat's within 2 x 10^-6
    assert all(abs(value - expected) < Fraction(1, 10**3) for value in lattice_read)
    assert abs(lattice_block.count - seated_block.count) <= 1 and seated_block.count >= 5
    # the invariant's jitter (a_next - a_before)(r - r') over e: 2 x 10^-5 read, below 10^-4
    assert max(forms) - min(forms) < max(forms) // 10**4
    step, wheel = seated.seat_wheel(seated_block)
    assert step * wheel == wall and step == math.gcd(wall, coefficient)
    # the wheel the rule's own gcd at the seat (9.60 (2), 9.57 (1))
    assert wheel == wall // math.gcd(wall, coefficient)


def cycles_of(
    document: dict, on: bool, ticks: int
) -> tuple[list[int], list[tuple[int, int]], list[dict]]:
    """The emitter world run on one form: the giving intervals' gaps (the cycle lengths), the
    residues with their wheels, and the giving lines."""
    lines: list[dict] = []
    simulation = DetectorLawSimulation(
        parse_nature_beam_world(with_body_record(document, on)), observer=lines.append
    )
    for _ in range(ticks):
        simulation.step()
        assert simulation.books()["balanced"], simulation.tick
    givings = [line for line in lines if line["event"] == "giving"]
    ticks_of = [line["tick"] for line in givings]
    gaps = [b - a for a, b in zip(ticks_of, ticks_of[1:], strict=False)]
    return gaps, [(line["u"], line["W"]) for line in givings], givings


def longest_run_of_ones(gaps: list[int]) -> int:
    longest = run = 0
    for gap in gaps:
        run = run + 1 if gap == 1 else 0
        longest = max(longest, run)
    return longest


def test_the_ticks_of_the_two_forms_agree_in_distribution():
    """(i) and (iii) on the emitter chain with the stock 600: on both forms the cycle lengths (the
    intervals between givings) have the mean within 5 percent of each other and of the fair
    draw's (P + 1) / 2 (the count ceil((2 u + 1) P / (2 W)) at a uniform residue; 47.7 and 48.2
    against 47.0 read, the standard error 2.3 percent; at 240 givings the body record read 42.4,
    a fluctuation of 2.7 standard errors, COMPUTATION), the residues
    u / W spread on the wheel (the chi-square over 12 bins below 19.7, the 5 percent bound at
    11 degrees of freedom), and no run of one-interval cycles beyond 3; every giving line's wheel
    is the form's own (the lattice body's at its first shell Node, the body record's the
    two-term rule's, another set of wheels); the given rows of the first giving are the file's train on the
    body's Nodes on both forms, bit for bit; the body record's read Node is its centre. The
    edge case: the two forms' givings differ in their intervals (different residues on different
    wheels: the law's claim is statistical, 9.46 (4))."""
    document = emitter_world(stock=600, ticks=1)
    period = document["measured"][0]["emitter"]["period"]
    train = document["measured"][0]["emitter"]["given"]
    results = {}
    for on in (False, True):
        gaps, residues, givings = cycles_of(document, on, 600 * period)
        assert len(givings) == 600, (on, len(givings))
        mean = sum(gaps) / len(gaps)
        fair = (period + 1) / 2
        # 600 givings: the standard error of the mean about 2.3 percent of it
        assert abs(mean - fair) < 0.05 * fair, (on, mean, fair)
        bins = [0] * 12
        for u, wheel in residues:
            assert 0 <= u < wheel
            bins[min(11, 12 * u // wheel)] += 1
        expected = len(residues) / 12
        chi = sum((count - expected) ** 2 / expected for count in bins)
        assert chi < 19.7, (on, chi, bins)
        assert longest_run_of_ones(gaps) <= 3, (on, gaps)
        first = givings[0]
        assert first["read_node"] == ([21, 0, 0] if on else [5, 0, 0])
        assert first["given_norm"] == train["norm"] and first["period"] == period
        results[on] = (mean, [line["tick"] for line in givings], [line["W"] for line in givings])
    assert abs(results[True][0] - results[False][0]) < 0.05 * results[False][0]
    assert results[True][1] != results[False][1]
    assert set(results[True][2]) != set(results[False][2])


def test_the_joint_inverse_is_exact_with_a_body_record():
    """THE BACKWARD RUN (ALGEBRA.md 9.50 (8): the body record's own backward run exact through
    its clicks): on the solitary cube under `body_record` with a light record of random rows
    registered, 60 intervals forward and 60 back return the rotation (a, b, r), the record's
    levels and remainders and both fields bit for bit; the body's pace is constant between
    clicks (its content held), so the two-term rule's coefficients are the same integers both
    ways. The edge case: the rotation did move (the state differs before the inverse)."""
    rng = np.random.default_rng(46)
    simulation = DetectorLawSimulation(parse_nature_beam_world(with_body_record(cube_world(), True)))
    block = simulation.blocks[0]
    assert block.seat is not None
    now = rng.integers(-UNIT, UNIT, size=simulation.shape, dtype=np.int64)
    before = rng.integers(-UNIT, UNIT, size=simulation.shape, dtype=np.int64)
    live = planted(simulation, 0, now, before, np.zeros(simulation.shape, dtype=np.int64))
    simulation.records[live.identity] = live
    start = (block.seat.now, block.seat.before, block.seat.remainder)
    field = simulation.held_record("content").now.copy()
    for _ in range(60):
        simulation.step()
    assert (block.seat.now, block.seat.before, block.seat.remainder) != start
    for _ in range(60):
        simulation.step_inverse()
    assert (block.seat.now, block.seat.before, block.seat.remainder) == start
    assert np.array_equal(live.now, now) and np.array_equal(live.before, before)
    assert not live.remainder.any() and simulation.tick == 0
    assert np.array_equal(simulation.held_record("content").now, field)


def test_the_loader_and_the_state_name_the_body_record():
    """`body_record` is true or false (another value refused), refused without `massive_record`,
    refused on a seeded block without its `clock` and profile (a flat scalar seed) naming the
    block; under it the state's block
    entry carries the rotation [a, b, r] and the form the two-term rule's invariant, and the
    block's click lines carry the body's identity; off, the block entry carries the rows and no
    rotation."""
    document = cube_world(ticks=4)
    bad = with_body_record(document, True)
    bad["body_record"] = "yes"
    bad["input"] = input_stamp(bad)
    with pytest.raises(ValueError, match="body_record must be true or false"):
        parse_nature_beam_world(bad)
    ray = json.loads(json.dumps(document))
    ray["massive_record"] = False
    ray["body_record"] = True
    with pytest.raises(ValueError, match="body_record needs massive_record"):
        parse_nature_beam_world(ray)
    # a flat scalar seed (no profile, no clock) is no body record: refused naming the block
    # (a profile always carries its clock, the loader's older check, record 1886)
    flat = block_world(
        [16, 16, 16],
        PERIODIC,
        [800, 809],
        [{"position": [5, 5, 5], "side": 6, "pair": [800, 801], "seed": 1 << 20, "margin": "control"}],
        ticks=4,
    )
    flat["age_bound"] = 100000
    flat["body_record"] = True
    with pytest.raises(ValueError, match=r"measured\[0\] under body_record declares no `clock`"):
        parse_nature_beam_world(flat)
    lines: list[dict] = []
    seated = DetectorLawSimulation(
        parse_nature_beam_world(with_body_record(document, True)), observer=lines.append
    )
    for _ in range(40):
        seated.step()
    state = dict(seated.snapshot_stream())
    entry = state["blocks"][0]
    body = seated.blocks[0].seat
    assert body is not None
    assert entry["rows"] is None and entry["seat"] == [body.now, body.before, body.remainder]
    assert entry["form"] == [seated.seat_form(seated.blocks[0]), 1]
    clicks = [line for line in lines if line["event"] == "click"]
    assert clicks and all(line["record"] == body.identity == 0 for line in clicks)
    lattice = DetectorLawSimulation(parse_nature_beam_world(with_body_record(document, False)))
    entry = dict(lattice.snapshot_stream())["blocks"][0]
    assert entry["seat"] is None and entry["rows"] is not None


def moving_world(ticks: int = 600, ramp: int = 200) -> dict:
    """The solitary body of `cube_world` pushed to speed one third along x (the momentum 64
    against the drive's wall 3 x 64 x 1 x 1 = 192: one Link every three intervals) over a ramp,
    seeded on its mode with its proper pairs by the generator (ALGEBRA.md 9.63 (3))."""
    document = block_world(
        [16, 16, 16],
        PERIODIC,
        [800, 809],
        [
            {
                "position": [5, 5, 5],
                "side": 6,
                "pair": [800, 801],
                "seed": 1 << 20,
                "margin": "control",
                "momentum": [64, 0, 0],
                "ramp": ramp,
            }
        ],
        ticks=ticks,
    )
    document["age_bound"] = 100000  # a periodic board keeps every ray: the store's bound
    massive_generator().seed_on_the_mode(document)
    return document


def test_the_moving_seat_rotates_at_the_proper_pair_of_its_momentum():
    """ALGEBRA.md 9.63 (3) (BUILD.md section 26 item 46). (1) THE GENERATOR'S LINE on a plane
    wave: the mode's quotient X is 2 num / (3 den) exactly and the moving rotation at v = 1 / 3
    and v = 1 / 5 on [800, 809] is the algebra's own (9.24 (2)): K = 0.18556 with the ratio
    0.81457 to the rest rotation, K = 0.09637 with 0.93757 (COMPUTATION). (2) THE TABLE: 65
    pairs for the momentum 64, the first the clock, the numerators never falling as the momentum
    grows (the proper rate slows), the last the rounding of b 2 cos(omega_K - K v) at v = 1 / 3
    from the mode's own dispersion. (3) THE SEAT reads the pair of the drive's momentum now: the
    clock before the ramp's first whole part, the table's entry at P t // ramp during it, the
    last after it, its rule at [num_m, 2 b]; the seat moved with its body. (4) THE LOADER under
    body_record refuses a moving seeded block without `proper_clock`, a table of the wrong
    length, a first entry other than the clock and the key on a body at rest, naming each; the
    generator refuses a momentum on two axes; the cube form loads the same file as before."""
    generator = massive_generator()
    # (1) the plane wave: every Node the kind's pair, the profile uniform
    plane = {
        "shape": [12, 3, 3],
        "boundary": PERIODIC,
        "families": [{"name": "matter", "pair": [800, 809]}],
        "measured": [
            {
                "family": "matter",
                "position": [0, 0, 0],
                "side": 12,
                "pair": [800, 809],
                "seed": [1000] * 108,
                "clock": [1600, 809],
            }
        ],
    }
    two_cos_rest, quotient = generator.mode_dispersion(plane, 0, 0)
    assert two_cos_rest == Fraction(1600, 809) and quotient == Fraction(1600, 3 * 809)
    rest_rotation = math.acos(800 / 809)
    for pace, wavenumber, ratio in ((1 / 3, 0.18556, 0.81457), (0.2, 0.09637, 0.93757)):
        k, rotation = generator.moving_rotation(float(two_cos_rest), float(quotient), pace)
        assert k == pytest.approx(wavenumber, abs=1e-5)
        assert rotation / rest_rotation == pytest.approx(ratio, abs=1e-5)
    # (2) the table of the moving world
    document = moving_world()
    entry = document["measured"][0]
    table = entry["proper_clock"]
    a, b = entry["clock"]
    assert len(table) == 65 and table[0] == [a, b]
    assert all(pair[1] == b for pair in table)
    assert all(table[m][0] >= table[m - 1][0] for m in range(1, 65))
    assert table[64][0] > table[0][0]
    two_cos_rest, quotient = generator.mode_dispersion(document, 0, 0)
    assert two_cos_rest == Fraction(a, b)
    _, rotation = generator.moving_rotation(float(two_cos_rest), float(quotient), 64 / 192)
    assert table[64] == [round(b * 2 * math.cos(rotation)), b]
    # (3) the seat's pair by the interval
    seated = DetectorLawSimulation(parse_nature_beam_world(with_body_record(document, True)))
    block = seated.blocks[0]
    assert block.seat is not None and block.definition.proper_clock is not None
    centre_at_rest = int(np.nonzero(seated.centre_mask(block))[0][0])
    assert seated.seat_clock(block) == (a, b)
    for tick in range(1, 301):
        seated.step()
        whole = 64 * tick // 200 if tick < 200 else 64
        assert seated.seat_clock(block) == tuple(table[whole]), tick
        num, den, _, _ = seated.seat_rule(block)
        assert (num, den) == (table[whole][0], 2 * b)
    assert block.stepped > 60 and int(np.nonzero(seated.centre_mask(block))[0][0]) != centre_at_rest
    # (4) the refusals, each named; the cube form loads the file as before
    parse_nature_beam_world(with_body_record(document, False))
    without = json.loads(json.dumps(document))
    del without["measured"][0]["proper_clock"]
    parse_nature_beam_world(with_body_record(without, False))
    with pytest.raises(ValueError, match=r"measured\[0\] under body_record moves and declares no"):
        parse_nature_beam_world(with_body_record(without, True))
    short = json.loads(json.dumps(document))
    short["measured"][0]["proper_clock"] = table[:-1]
    with pytest.raises(ValueError, match=r"proper_clock must be 65 pairs"):
        parse_nature_beam_world(with_body_record(short, True))
    other = json.loads(json.dumps(document))
    other["measured"][0]["proper_clock"] = [[a + 1, b]] + table[1:]
    with pytest.raises(ValueError, match=r"proper_clock\[0\] .* is not the clock"):
        parse_nature_beam_world(with_body_record(other, True))
    at_rest = cube_world(ticks=4)
    at_rest["measured"][0]["proper_clock"] = [list(at_rest["measured"][0]["clock"])]
    with pytest.raises(ValueError, match=r"proper_clock is admitted beside `clock` on a block whose"):
        parse_nature_beam_world(with_body_record(at_rest, True))
    two_axes = json.loads(json.dumps(document))
    two_axes["measured"][0]["momentum"] = [64, 64, 0]
    with pytest.raises(ValueError, match=r"the proper pair is read along one axis of motion"):
        generator.proper_clock(two_axes, 0)
