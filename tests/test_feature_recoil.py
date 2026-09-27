"""THE RECOIL, its own folder (ALGEBRA.md 9.117 item 2, the row "the recoil"; 9.117 item 5;
9.84 (2); 9.91 (4); 9.111 items 1 and 2; the Boss's record 2224): the line's integers on the
moving row's numbers, the store carried so the sum over clicks is the exact floor, also across
clicks of different divisors and across a taking and a giving, the direction of travel and the
giver's opposite sign, a symmetric emitter's cancellation, the refusals by name, the trace's
hand identity on the emitter's run (the givings' four-vectors), and the folder's declaration
the ledger's row."""

from __future__ import annotations

from fractions import Fraction

import pytest

from event_universe.core.register import folder_of
from event_universe.events.detector_law import DetectorLawSimulation
from event_universe.features.recoil import (
    DECLARATION,
    GIVING,
    NO_STORE,
    TAKING,
    THE_WORD,
    RecoilOwn,
    RecoilStart,
    RecoilTerm,
    apply,
    sign_of,
)
from event_universe.world_files import parse_nature_beam_world
from tests.test_emitter import emitter_world

# the moving row's body (issue #1156): W = 12480 at M = 65 (Q = 64), its period 21, the
# given light's wavelength 4 Links
TERM = RecoilTerm(period=21, quanta=65, wavelength=4, sense=TAKING)
START = RecoilStart(tally=(+9, 0, -4), wall=12_480)
NONE = (NO_STORE, NO_STORE, NO_STORE)


def exact_floor(clicks: list[tuple[int, int, int, int, int]]) -> int:
    """The hand check: the floor of the sum over the clicks of sense x sigma x W P / (M
    lambda), each click's integers as the trace's line shows them."""
    total = sum(
        Fraction(sense * sigma * wall * period, quanta * wavelength)
        for sense, sigma, wall, period, quanta, wavelength in clicks
    )
    return total.numerator // total.denominator


def run_clicks(clicks: list[tuple[int, int, int, int, int, int]]) -> RecoilOwn:
    own = RecoilOwn((0, 0, 0), NONE)
    for sense, sigma, wall, period, quanta, wavelength in clicks:
        writes = apply(
            RecoilTerm(period, quanta, wavelength, sense), RecoilStart((sigma, 0, 0), wall), own
        )
        own = RecoilOwn(writes.momentum, writes.remainders)
    return own


def test_the_line_on_the_moving_rows_numbers():
    """n_a += sigma_a x (W x P_body) div (M x lambda_q): 12480 x 21 = 262080 over 65 x 4 =
    260 gives 1008 exactly on x (the tally positive, toward +x) and -1008 on z (the tally
    negative), nothing on y (no tally); the stores empty."""
    writes = apply(TERM, START, RecoilOwn((100, 200, 300), NONE))
    assert writes.momentum == (1108, 200, -708)
    assert writes.remainders == NONE


def test_the_store_is_carried_so_the_sum_over_clicks_is_the_exact_floor():
    """The store stays on the body's record between clicks, so the sum of the whole parts
    over k clicks is the exact floor of k x (W x P_body) / (M x lambda_q): 52 exact clicks at
    260; 576 exact at 455; at 462 (M = 66, lambda 7) the fraction 126 / 462 = 3 / 11 per click
    adds three whole units over eleven clicks and the store returns to none."""
    fifty_two = [(TAKING, 1, 12_480, 21, 65, 4)] * 52
    assert run_clicks(fifty_two) == RecoilOwn((52 * 1008, 0, 0), NONE)
    three = [(TAKING, 1, 12_480, 21, 65, 7)] * 3
    assert run_clicks(three).momentum == (3 * (262_080 // 455), 0, 0) == (3 * 576, 0, 0)
    eleven = [(TAKING, 1, 12_480, 21, 66, 7)] * 11
    for count in range(1, 12):
        own = run_clicks(eleven[:count])
        assert own.momentum[0] == exact_floor(eleven[:count]) == (count * 262_080) // 462
        assert own.remainders[0] == (Fraction(count * 126, 462) % 1).as_integer_ratio()
    assert own.momentum[0] == 11 * 567 + 3 and own.remainders[0] == NO_STORE


def test_clicks_of_different_divisors_add_exactly_the_reviewers_case_and_a_mixed_run():
    """Q = 64, M = 65 (W = 12480), P = 20: a click of lambda 7 (249600 / 455 = 548 + 4 / 7) then
    one of lambda 4 (249600 / 260 = 960) give 1508, the exact floor of 1508.571 (a remainder
    carried as a bare integer across the change of divisor gave 1509); over a mixed run of
    wavelengths and quanta, takings and givings, the momentum after every click is the exact
    floor of the sum of the fractions, and the store's divisor divides the least common
    multiple of the wavelengths (the fraction 3 Q P / lambda once W = 3 Q M)."""
    reviewer = [(TAKING, 1, 12_480, 20, 65, 7), (TAKING, 1, 12_480, 20, 65, 4)]
    first = run_clicks(reviewer[:1])
    assert first.momentum == (548, 0, 0) and first.remainders[0] == (4, 7)
    both = run_clicks(reviewer)
    assert both.momentum == (1508, 0, 0) and both.remainders[0] == (4, 7)
    assert exact_floor(reviewer) == 1508
    mixed = []
    quanta = 65
    for step, (sense, sigma, wavelength) in enumerate(
        [
            (TAKING, 1, 7),
            (TAKING, -1, 4),
            (GIVING, 1, 9),
            (TAKING, 1, 7),
            (TAKING, 1, 9),
            (GIVING, -1, 4),
        ]
        * 4
    ):
        quanta += 1 if sense == TAKING else -1
        mixed.append((sense, sigma, 3 * 64 * quanta, 20 + step % 3, quanta, wavelength))
    for count in range(1, len(mixed) + 1):
        own = run_clicks(mixed[:count])
        assert own.momentum[0] == exact_floor(mixed[:count])
        assert 252 % own.remainders[0][1] == 0  # lcm(7, 4, 9) = 252


def test_a_taking_and_a_giving_of_the_same_quantum_cancel_through_a_negative_remainder():
    """A giving is the same line with the opposite sign: a taking of 3840 / 7 (548, the store
    4 / 7) then a giving of the same undo each other exactly (n back to 0, the store none);
    a giving first floors to -549 with the store 3 / 7 (the exact floor of -548.571), and the
    taking after it returns n to 0."""
    take, give = (TAKING, 1, 12_480, 20, 65, 7), (GIVING, 1, 12_480, 20, 65, 7)
    assert run_clicks([take, give]) == RecoilOwn((0, 0, 0), NONE)
    given = run_clicks([give])
    assert given.momentum == (-549, 0, 0) and given.remainders[0] == (3, 7)
    assert exact_floor([give]) == -549
    assert run_clicks([give, take]) == RecoilOwn((0, 0, 0), NONE)


def test_the_direction_of_travel_and_the_givers_opposite_sign():
    """sigma is the tally's sign, never its size: a tally of +1 and of +10^6 recoil the same;
    a giving with the same tally recoils the other way; a symmetric emitter (the tallies
    0) recoils by nothing and keeps its stores (9.84 (2))."""
    small = apply(TERM, RecoilStart((1, 0, 0), 12_480), RecoilOwn((0, 0, 0), NONE))
    large = apply(TERM, RecoilStart((10**6, 0, 0), 12_480), RecoilOwn((0, 0, 0), NONE))
    assert small.momentum == large.momentum == (1008, 0, 0)
    giving = apply(
        RecoilTerm(21, 65, 4, GIVING), RecoilStart((1, 0, 0), 12_480), RecoilOwn((0, 0, 0), NONE)
    )
    assert giving.momentum == (-1008, 0, 0) and giving.remainders == NONE
    kept = ((1, 2), (2, 3), (3, 5))
    symmetric = apply(TERM, RecoilStart((0, 0, 0), 12_480), RecoilOwn((7, 8, 9), kept))
    assert symmetric.momentum == (7, 8, 9) and symmetric.remainders == kept
    assert [sign_of(v) for v in (-3, 0, 5)] == [-1, 0, 1] and TAKING == 1


def test_the_bounds_and_the_terms_are_refused_by_name():
    """The two products at most 10^9 (9.91 (4)); the period, the quanta, the wavelength and the
    wall from 1; the sense +1 or -1; a store a remainder below its divisor in lowest terms;
    a store's divisor beyond the bound."""
    with pytest.raises(ValueError, match="products exceed the bound: W x P_body = 12480000000"):
        apply(RecoilTerm(1_000_000, 65, 4, TAKING), START, RecoilOwn((0, 0, 0), NONE))
    with pytest.raises(ValueError, match="M x lambda_q = 6500000000"):
        apply(RecoilTerm(21, 65, 100_000_000, TAKING), START, RecoilOwn((0, 0, 0), NONE))
    with pytest.raises(ValueError, match="from 1, got P_body = 0"):
        apply(RecoilTerm(0, 65, 4, TAKING), START, RecoilOwn((0, 0, 0), NONE))
    with pytest.raises(ValueError, match="needs a wall from 1, got W = 0"):
        apply(TERM, RecoilStart((1, 0, 0), 0), RecoilOwn((0, 0, 0), NONE))
    with pytest.raises(ValueError, match=r"sense is \+1 \(a taking\) or -1 \(a giving\), got 2"):
        apply(RecoilTerm(21, 65, 4, 2), START, RecoilOwn((0, 0, 0), NONE))
    with pytest.raises(ValueError, match="store on axis 1 is 2 / 4: a remainder below its divisor"):
        apply(TERM, START, RecoilOwn((0, 0, 0), (NO_STORE, (2, 4), NO_STORE)))
    with pytest.raises(ValueError, match="store on axis 2 is 7 / 7"):
        apply(TERM, START, RecoilOwn((0, 0, 0), (NO_STORE, NO_STORE, (7, 7))))
    with pytest.raises(
        ValueError, match=r"would need the divisor 999999937000000000 .* beyond the bound"
    ):
        apply(
            RecoilTerm(1, 1, 999_999_937, TAKING),
            RecoilStart((1, 0, 0), 1),
            RecoilOwn((0, 0, 0), ((1, 10**9), NO_STORE, NO_STORE)),
        )


def test_the_trace_hand_identity_on_the_emitters_run():
    """On the emitter's unit world (the body of Q = 64 giving four quanta of light of the
    wavelength 4 along +x through its window), every giving line carries the given
    quantum's four-vector (its momentum the sign per axis of the outward flux); the folder,
    fed the line's integers (the direction, the body's wall and quanta as the loop reads
    them, its period, the wavelength) with the giver's sense, moves the body's n by the whole
    part and keeps the store, and after every giving n equals the hand check, the exact
    floor of the sum of the fractions from the same integers (ALGEBRA.md 9.112 item 5, the
    click's writes; 9.84 (2)). No body's momentum moves in the run itself (the binding is
    the main loop's cut): the run is read, never adjusted."""
    document = emitter_world(stock=4, ticks=1200)
    period = document["measured"][0]["emitter"]["period"]
    wavelength = 2 * document["N"] // document["universe"][0]["clock"][0]  # k = pi / 2: 4
    assert wavelength == 4 and period > 0
    lines: list[dict] = []
    simulation = DetectorLawSimulation(parse_nature_beam_world(document), observer=lines.append)
    for _ in range(document["ticks"]):
        simulation.step()
    givings = [line for line in lines if line["event"] == "giving" and "momentum" in line]
    assert len(givings) == 4 and all(line["momentum"] == [1, 0, 0] for line in givings)
    body = simulation.block_by_number[0]
    assert body.momentum == [0, 0, 0]  # the run's own n untouched
    clicks = []
    own = RecoilOwn((0, 0, 0), NONE)
    for line in givings:
        wall, quanta = simulation.wall_of(body), sum(simulation.held[line["measured"]])
        assert wall == 3 * document["momentum_unit"] * quanta
        writes = apply(
            RecoilTerm(period, quanta, wavelength, GIVING),
            RecoilStart(tuple(line["momentum"]), wall),
            own,
        )
        own = RecoilOwn(writes.momentum, writes.remainders)
        clicks.append((GIVING, line["momentum"][0], wall, period, quanta, wavelength))
        assert own.momentum[0] == exact_floor(clicks) < 0 and own.momentum[1:] == (0, 0)


def test_the_declaration_is_the_ledgers_row():
    """The folder declares the row of ALGEBRA.md 9.117: "the recoil" at (iv), writing a
    body's momentum n and its remainders, order 2 after the giving's bulk share, its
    function `apply`, and its section with the word of 9.117 item 5, from the rule."""
    assert DECLARATION.name == "the recoil" and DECLARATION.place == "(iv)"
    assert DECLARATION.writes == ("a body's momentum n", "a body's remainders")
    assert DECLARATION.function is apply and DECLARATION.built
    assert DECLARATION.word == "after the step" and folder_of(DECLARATION.name) == "recoil"
    assert DECLARATION.section.startswith(THE_WORD)
    # the engine's register finds this folder among the twenty-four, with its apply
    simulation = DetectorLawSimulation(parse_nature_beam_world(emitter_world(stock=1, ticks=2)))
    registered = simulation.register.declarations["the recoil"]
    assert registered.reads == DECLARATION.reads and registered.function is apply
    assert registered.place_of("a body's momentum n") == "(iv)"
    assert THE_WORD.startswith("from the rule") and "beyond" not in THE_WORD
    assert "9.117" in DECLARATION.section and "9.84 (2)" in DECLARATION.section
