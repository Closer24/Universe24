"""The three components the quantum rows of the local detector law lack (the Boss's order of
2026-09-23 22:25Z; docs/designs/detector_law/declarations/DECLARATIONS.md, "what the engine
lacks"; BUILD.md section 11), one test each with its inputs, its expected integers and an edge
case: (a) the phase reading of a record at a Node, (c) the splitter's table under the rule,
(g, d4) the joint weights and the partial trace as integers. SINCE THE EMITTER AS A CLICKING
BODY (ALGEBRA.md 9.17; BUILD.md section 26) every source here is an emitter body (the chain
world's), and the two-arm lamp's tests (b, e, e2, f, h: the pair born at a lamp) are RETIRED
with the lamp: the pair is born at the crystal, and its tests return with the crystal's
branch (tests/test_crystal.py there). SINCE THE FLUX READING (9.19 (3); BUILD.md section 26
item 14) the polariser's tests (d, d2, d3: the table body of two cells at one Node and
Malus's counts) are HELD with the four Malus worlds: under the cumulative ladder as written
the entry's whole offer reaches the rung no later than the + share of it, so the two cells
at one Node give no distribution (the finding in tests/test_detector_law.py); the
polariser returns as a body with an axis and two receivers named (the mathematician's step
3) and its counts are re-derived on it."""

from __future__ import annotations

import math

import numpy as np
import pytest

from event_universe.core.integer import by_clock
from event_universe.core.phase import nearest_phase, phase_cosines, phase_sines
from event_universe.events.detector_law import UNIT, DetectorLawSimulation, LiveRecord
from event_universe.events.world import parse_nature_beam_world
from tests.test_detector_law import chain_world
from tests.test_emitter import massive_generator


def clock_phase(age: int, numerator: int, denominator: int, steps: int) -> int:
    """The engine's clock at an age (the zero 3 N / 4 advanced by the whole part of
    age x n / d)."""
    return (3 * steps // 4 + age * numerator // denominator) % steps


def test_a_the_phase_reading_reads_the_clocks_phase_back_at_every_age():
    """(a) The phase reading (DECLARATIONS.md's head): on the circle N = 64 with the clock
    [77, 25] (3.08 steps per interval) and with [1, 1], the pair (C[phi(t - 1)], C[phi(t)]) x
    A / 256 the lamp drives at age t reads back phi(t) with the residual 0 at every age of a
    train of 64 intervals (every phase of the wheel), at the amplitude A = UNIT and at 3 / 7
    of it (the amplitude the reading's third input, the declaration's A: without it a small
    pair at a zero crossing and a large one at the peak share one direction). The table's
    grain, named (BUILD.md section 11, the finding): on N = 128 the reading is exact where a
    level is at least 16 of 256 from the cosine's extrema, and on N = 2048 with the clock
    [3, 1] within one step where both levels are at least 32 from them; at N = 2048 with the
    clock [1, 1] consecutive entries of the 1 / 256 table repeat and the pair recurs along the
    wave, so the reading is not exact there (a design question for the Bell row's N). On the
    chain world the record's reading at a free Node 12 Links from the source, advancing by the
    clock's step between consecutive intervals: RETIRED with the lamp's drive (ALGEBRA.md 9.17;
    the emitter body's one-cell birth is broadband). The edge cases: the zero pair reads None; a zero circle, clock or
    amplitude is refused."""
    factor = UNIT // 256
    for steps, clock, band, within in (
        (64, (77, 25), 0, 0),
        (64, (1, 1), 0, 0),
        (128, (1, 1), 16, 0),
        (2048, (3, 1), 32, 1),
    ):
        table = phase_cosines(steps)
        checked = 0
        for age in range(1, steps + 1):
            phi = clock_phase(age, clock[0], clock[1], steps)
            previous = clock_phase(age - 1, clock[0], clock[1], steps)
            if not (
                band <= abs(table[phi]) <= 256 - band and band <= abs(table[previous]) <= 256 - band
            ):
                continue
            for scale in (factor, factor * 3 // 7):
                amplitude = scale * 256
                reading = nearest_phase(
                    table[previous] * scale, table[phi] * scale, amplitude, clock, steps
                )
                assert reading is not None
                error = min((reading[0] - phi) % steps, (phi - reading[0]) % steps)
                assert error <= within, (steps, clock, age, scale, reading, phi)
                if within == 0:
                    assert reading[1] == 0
                checked += 1
        assert checked >= steps // 2, (steps, checked)
    # (the chain part of this test, the reading's advance along a driven
    # train at a free Node, retired with the lamp's drive, ALGEBRA.md 9.17:
    # an emitter body's one-cell birth is broadband)
    assert nearest_phase(0, 0, UNIT, (77, 25), 64) is None
    with pytest.raises(ValueError):
        nearest_phase(1, 1, UNIT, (0, 1), 64)
    with pytest.raises(ValueError):
        nearest_phase(1, 1, UNIT, (1, 1), 0)
    with pytest.raises(ValueError):
        nearest_phase(1, 1, 0, (1, 1), 64)


def splitter_world(weights: list[list[int]], turns: list[list[int]], inputs: bool = True) -> dict:
    """A layer of 30 x 20 x 1 (z folded, x and y closed: mirrors, no face receiver), the
    emitter body at (2, 2, 0) (one excitation, one birth), one splitter of the TABLE form at
    (12, 2, 0) arriving from -x (the input direction +x) with its two outputs +x and +y, the
    split's weights and turns given; no detector set, so the born record's ladder is empty
    and it lives on."""
    document = chain_world(stock=1, wheel=(1, 1), on_mode=False)
    document["shape"] = [30, 20, 1]
    document["boundary"] = {"x": "closed", "y": "closed", "z": "periodic"}
    document["ticks"] = 120
    lamp = document["measured"][0]
    lamp["position"] = [2, 2, 0]
    table: dict = {"rule": "rerelease", "weights": weights, "turns": turns}
    if inputs:
        table["inputs"] = [[1, 0, 0]]
    else:
        # an opening's fan: one flat row of weights over the directions, no inputs
        table["weights"], table["turns"] = weights[0], turns[0]
    document["measured"] = [
        lamp,
        {
            "position": [12, 2, 0],
            "family": "light",
            "amount": 1,
            "phase": 0,
            "momentum": [0, 0, 0],
            "fixed": True,
            "directions": [[1, 0, 0], [0, 1, 0]],
            "table": {"light": table},
        },
    ]
    document["detectors"] = []
    massive_generator().seed_on_the_mode(document)
    return document


def planted_light(simulation: DetectorLawSimulation, age: int, identity: int = 1) -> LiveRecord:
    """A light record's rows given directly (no lamp): the clock [77, 25] on N = 64, at `age`."""
    return LiveRecord(
        identity,
        0,
        0,
        0,
        1,
        0,
        1,
        77,
        25,
        200,
        21,
        np.zeros(simulation.shape, dtype=np.int64),
        np.zeros(simulation.shape, dtype=np.int64),
        np.zeros(simulation.shape, dtype=np.int64),
        pointers=[0] * len(simulation.cell_names),
        first_rung=[None] * len(simulation.cell_names),
        ports=[np.zeros(simulation.shape, dtype=np.int64) for _ in simulation.take_masks],
        age=age,
    )


def test_c_the_splitters_table_acts_on_the_pair_by_the_linear_form():
    """(c) The splitter's table under DECLARATIONS.md section 14 (the linear form, the additive
    re-emission, the remainder carried): on the layer of `splitter_world` the splitter at
    (12, 2, 0) reads the input Node (11, 2, 0) and adds its terms at (13, 2, 0) and (12, 3, 0).
    (1) The integers: a planted pair (a_before, a_now) = (C[phi - k] UNIT / 256, C[phi] UNIT /
    256) at the input (the record's age 1, the clock's step k = by_clock(0, 77, 25) = 3) gives
    at the outputs, from 0, exactly floor(w_j (a_now S[k + t_j] - a_before S[t_j]) / (S[k] 29))
    with the remainder in [0, S[k] 29) kept on the splitter, w = [21, 20], t = [0, 16]; and each
    term is w_j UNIT cos(phi + t_j) / 29 within UNIT / 64 (the tables' 1 / 256 in the
    coefficients only). (2) The isometry: over the 64 phases the two outputs' squares sum to
    the input's squares within 2 percent (21^2 + 20^2 = 29^2). (3) A second call on the same
    pair adds the same term again (additive: the rule's value at the output is never
    overwritten). (4) The run of 90 intervals: the books balanced at every interval, the
    splitter's Node evolving under the rule like every Node (the take retired: nothing holds
    it at 0), no click at its cell (the record's ladder is empty: it lives on), the wave
    beyond both outputs nonzero, every remainder inside its wall. The edge cases: a split without
    inputs (an opening's fan) refused; a row whose norm is no square refused naming the norm;
    a clock whose step has a sine of 0 ([32, 1] on N = 64: the step 32, sin pi = 0; [1, 2]: a
    step of 0) refused at load naming the step. Light's worlds without a splitter are byte for
    byte as before (test (p) of test_massive_record.py)."""
    world = parse_nature_beam_world(splitter_world([[21, 20]], [[0, 16]]))
    simulation = DetectorLawSimulation(world)
    assert len(simulation.splitters) == 1
    splitter = simulation.splitters[0]
    assert splitter.inputs[0][0] == (11, 2, 0) and splitter.outputs == [(13, 2, 0), (12, 3, 0)]
    steps = world.phase_steps
    cosines = phase_cosines(steps)
    sines = phase_sines(steps)
    k = by_clock(0, 77, 25)
    assert k == 3
    unit_per_cell = UNIT // 256
    squares_in = squares_out = 0
    for phi in range(steps):
        live = planted_light(simulation, 1, identity=phi + 1)
        now = cosines[phi] * unit_per_cell
        before = cosines[(phi - k) % steps] * unit_per_cell
        live.now[11, 2, 0] = now
        live.before[11, 2, 0] = before
        simulation._split(live)
        assert live.age == 2
        remainders = splitter.remainders[live.identity]
        wall = sines[k] * 29
        for j, (weight, turn, output) in enumerate(
            zip((21, 20), (0, 16), splitter.outputs, strict=True)
        ):
            total = weight * (now * sines[(k + turn) % steps] - before * sines[turn])
            expected, remainder = divmod(total, wall)
            assert int(live.now[output]) == expected
            assert remainders[j] == remainder and 0 <= remainder < wall
            closed = weight * UNIT * math.cos(2 * math.pi * (phi + turn) / steps) / 29
            assert abs(expected - closed) < UNIT / 64, (phi, j, expected, closed)
            squares_out += expected * expected
        squares_in += now * now
        # additive: the same pair again adds the same term (up to the carried remainder)
        first = [int(live.now[output]) for output in splitter.outputs]
        simulation._split(live)
        for j, output in enumerate(splitter.outputs):
            assert abs(int(live.now[output]) - 2 * first[j]) <= 1
    assert abs(squares_out / squares_in - 1.0) < 0.02, squares_out / squares_in
    # the run
    lines: list[dict] = []
    simulation = DetectorLawSimulation(world, observer=lines.append)
    splitter = simulation.splitters[0]
    for _ in range(90):
        simulation.step()
        assert simulation.books()["balanced"], simulation.tick
        for remainders in splitter.remainders.values():
            assert all(0 <= r < sines[3] * 29 or 0 <= r < sines[4] * 29 for r in remainders)
    live = next(record for record in simulation.records.values() if record.family == 0)
    assert abs(int(live.now[14, 2, 0])) > 0 and abs(int(live.now[12, 4, 0])) > 0
    # the one `click` line is the emitter's excited record's (its birth); the
    # born record clicks nowhere (no gather line: its ladder is empty)
    assert not any(line["event"] == "gather" for line in lines)
    assert [line["family"] for line in lines if line["event"] == "click"] == ["matter"]
    assert not live.clicked and not simulation.dead
    with pytest.raises(ValueError, match="a splitter declares its inputs"):
        parse_nature_beam_world(splitter_world([[21, 20]], [[0, 16]], inputs=False))
    with pytest.raises(ValueError, match="no square"):
        DetectorLawSimulation(parse_nature_beam_world(splitter_world([[1, 1]], [[0, 16]])))
    for clock in ([32, 1], [1, 2]):
        zero_step = splitter_world([[21, 20]], [[0, 16]])
        zero_step["families"][0]["phase_per_link"] = clock
        with pytest.raises(ValueError, match="has a sine of 0"):
            parse_nature_beam_world(zero_step)


def test_g_the_joint_weights_are_the_declared_integers():
    """(g) The joint weights R = J^2 from planted tables (DECLARATIONS.md section 1 item 3): with
    psi = (00) + (11) (the labels 0 and 3 of weight 1, Alice reading the bit of arm 1 and Bob
    of arm 0) and the pairs (C', S') = (256, 0) and (181, 181), J(+, +) = 256 x 181, J(+, -) =
    -256 x 181, J(-, +) = 256 x 181, J(-, -) = 256 x 181 (the sign squared away); with (237,
    98) and (256, 0) (Bob's 22.5 degrees of N = 2048 against Alice's 0) the four weights
    (256 x 237)^2, (256 x 98)^2, (256 x 98)^2, (256 x 237)^2 and E = (237^2 - 98^2) / (237^2
    + 98^2) = 46565 / 65773 (COMPUTATION, the form's own number, for the generator's `bell.py`
    to compare with the pin 181 / 64); the singlet (01) - (10) at equal settings gives J(+,
    +) = 0; a one-body table gives the two weights C'^2 and S'^2 (Malus's form)."""
    labels = ((0, 1), (3, 1))
    cells = DetectorLawSimulation.joint_weights([(256, 0), (181, 181)], [1, 0], labels)
    assert [channels for channels, _ in cells] == [(0, 0), (0, 1), (1, 0), (1, 1)]
    assert [weight for _, weight in cells] == [(256 * 181) ** 2] * 4
    cells = DetectorLawSimulation.joint_weights([(256, 0), (237, 98)], [1, 0], labels)
    assert [weight for _, weight in cells] == [
        (256 * 237) ** 2,
        (256 * 98) ** 2,
        (256 * 98) ** 2,
        (256 * 237) ** 2,
    ]
    plus_plus, plus_minus, minus_plus, minus_minus = (weight for _, weight in cells)
    assert (plus_plus + minus_minus - plus_minus - minus_plus) * 65773 == 46565 * sum(
        weight for _, weight in cells
    )
    singlet = DetectorLawSimulation.joint_weights([(181, 181), (181, 181)], [1, 0], ((1, 1), (2, -1)))
    assert singlet[0][1] == 0 and singlet[3][1] == 0 and singlet[1][1] == singlet[2][1] > 0
    one = DetectorLawSimulation.joint_weights([(237, 98)], [0], ((0, 1),))
    assert one == [((0,), 237 * 237), ((1,), 98 * 98)]


def test_d4_an_arm_of_a_rank_2_record_is_split_by_the_partial_trace():
    """(d4) The mathematician's gate on the polariser's fix (ALGEBRA.md 9.11, defect (d)): for an
    arm of a rank-2 record the one-body weights are the PARTIAL TRACE over the other arm's
    bit, R(o) = SUM over the other bit b of (SUM over the labels l with that bit of w_l
    U_s[o][bit of l on this arm])^2, not the coherent sum over all labels. THE ALGEBRA'S
    INTEGERS on HV + VH (the branches [[1, 1], [2, 1]]), N = 2048: at s = 512 (C' = S' = 181)
    each arm's weights are (2 x 181^2, 2 x 181^2) = (65522, 65522), half on each channel,
    where the coherent sum would give (362^2, 0) and book the whole offer on +; at s = 0
    (C' = 256, S' = 0) the weights are (65536, 65536); at s = 256 (C' = 237, S' = 98) the
    weights are (237^2 + 98^2, 98^2 + 237^2) = (65773, 65773): an arm of the entangled pair
    is unpolarised at every setting. The other arm reads the same. A one-arm record keeps
    the coherent sum (test d2's superposition: at s = 512 the weights (362^2, 0)). The
    joint counts (tests e and f) do not move: the gather reads the whole offer."""
    from event_universe.events.amplitude import half_angle

    weights = DetectorLawSimulation.channel_weights
    pair = ((1, 1), (2, 1))
    for setting, expected in ((512, (65522, 65522)), (0, (65536, 65536)), (256, (65773, 65773))):
        cosine, sine = half_angle(setting, 2048)
        assert weights(cosine, sine, 0, pair) == expected, setting
        assert weights(cosine, sine, 1, pair) == expected, setting
    cosine, sine = half_angle(512, 2048)
    assert weights(cosine, sine, 0, ((0, 1), (1, 1))) == (362 * 362, 0)
