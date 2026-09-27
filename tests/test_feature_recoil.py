"""THE RECOIL, its own folder (ALGEBRA.md #the-primitives, the row "the recoil"; 9.84 (2); 9.91 (4); 9.111
items 1 and 2; record 2224): the line's integers on the moving row's numbers, the store one remainder
on the universe's wall L so the sum over clicks of every wavelength is the exact floor (across a
taking and a giving too), the direction of travel, the refusals by name, the trace's hand identity on
the emitter's run, the declaration."""

from __future__ import annotations

from fractions import Fraction

import pytest

from event_universe.core.register import folder_of
from event_universe.events.detector_law import DetectorLawSimulation
from event_universe.features.recoil import (
    DECLARATION,
    GIVING,
    TAKING,
    THE_WORD,
    RecoilOwn,
    RecoilStart,
    RecoilTerm,
    apply,
    sign_of,
)
from event_universe.world_files import parse_nature_beam_world
from tests.worlds import emitter_world

# the moving row's body (issue #1156): Q = 64 (W = 12480 at M = 65), its period 21, the given
# light's wavelength 4 Links; the universe's wall L = 252, the least common multiple of 4, 7 and 9
UNIT = 64
WALL = 252
TERM = RecoilTerm(period=21, wavelength=4, sense=TAKING, wall=WALL, unit=UNIT)
START = RecoilStart(tally=(+9, 0, -4))
NONE = (0, 0, 0)


def exact_floor(clicks: list[tuple[int, int, int, int]]) -> int:
    """The hand check: the floor of the sum over the clicks of sense x sigma x 3 Q P / lambda."""
    total = sum(
        Fraction(sense * sigma * 3 * UNIT * period, wavelength)
        for sense, sigma, period, wavelength in clicks
    )
    return total.numerator // total.denominator


def run_clicks(clicks: list[tuple[int, int, int, int]], wall: int = WALL) -> RecoilOwn:
    own = RecoilOwn((0, 0, 0), NONE)
    for sense, sigma, period, wavelength in clicks:
        writes = apply(
            RecoilTerm(period, wavelength, sense, wall, UNIT), RecoilStart((sigma, 0, 0)), own
        )
        own = RecoilOwn(writes.momentum, writes.remainders)
    return own


def test_the_line_on_the_moving_rows_numbers():
    """n_a += sigma_a x 3 Q P_body (L div lambda_q) div L: 3 x 64 x 21 x 63 = 254016 over 252 gives
    1008 exactly on x (the tally positive, toward +x) and -1008 on z (the tally negative), nothing on
    y (no tally); the stores empty; the same as W x P_body div (M x lambda_q) = 262080 div 260."""
    writes = apply(TERM, START, RecoilOwn((100, 200, 300), NONE))
    assert writes.momentum == (1108, 200, -708) and writes.remainders == NONE
    assert 3 * UNIT * 21 * (WALL // 4) // WALL == 12_480 * 21 // (65 * 4) == 1008


def test_the_store_on_the_wall_makes_the_sum_over_clicks_the_exact_floor():
    """The store stays on the body between clicks as one remainder on L, so the sum of the whole parts
    over k clicks of any wavelengths is the exact floor of the sum of the fractions: 52 exact clicks
    at wavelength 4; at wavelength 7 the fraction 4032 / 7 = 576 exactly; at wavelength 9 (448 per
    click) 3 / 9 per click adds a unit every three; the reviewer's case, a click of lambda 7 then one
    of lambda 4 at P = 20, gives 1508, the exact floor of 1508.571; a mixed run of wavelengths,
    takings and givings, the momentum after every click the exact floor."""
    assert run_clicks([(TAKING, 1, 21, 4)] * 52) == RecoilOwn((52 * 1008, 0, 0), NONE)
    assert run_clicks([(TAKING, 1, 21, 7)] * 3).momentum == (3 * 576, 0, 0)
    for count in range(1, 10):
        own = run_clicks([(TAKING, 1, 21, 9)] * count)
        assert own.momentum[0] == exact_floor([(TAKING, 1, 21, 9)] * count) == (count * 4032) // 9
        assert own.remainders[0] == (count * 4032 * (WALL // 9)) % WALL
    reviewer = [(TAKING, 1, 20, 7), (TAKING, 1, 20, 4)]
    assert run_clicks(reviewer[:1]).momentum == (548, 0, 0)
    assert run_clicks(reviewer).momentum == (1508, 0, 0) and exact_floor(reviewer) == 1508
    mixed = [
        (sense, sigma, 20 + step % 3, wavelength)
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
        )
    ]
    for count in range(1, len(mixed) + 1):
        own = run_clicks(mixed[:count])
        assert own.momentum[0] == exact_floor(mixed[:count]) and 0 <= own.remainders[0] < WALL


def test_a_taking_and_a_giving_of_the_same_quantum_cancel_and_the_direction_of_travel():
    """A giving is the same line with the opposite sign: a taking of 3840 / 7 (548, the store 4 / 7 on
    L) then a giving of the same undo each other exactly; a giving first floors to -549 (the exact
    floor of -548.571) and the taking after it returns n to 0; sigma is the tally's sign, never its
    size (a tally of 1 and of 10^6 recoil the same); a symmetric emitter (the tallies 0) recoils by
    nothing and keeps its stores (9.84 (2))."""
    take, give = (TAKING, 1, 20, 7), (GIVING, 1, 20, 7)
    assert run_clicks([take, give]) == RecoilOwn((0, 0, 0), NONE)
    given = run_clicks([give])
    assert given.momentum == (-549, 0, 0) and given.remainders[0] == WALL - 4 * (WALL // 7)
    assert exact_floor([give]) == -549 and run_clicks([give, take]) == RecoilOwn((0, 0, 0), NONE)
    small = apply(TERM, RecoilStart((1, 0, 0)), RecoilOwn((0, 0, 0), NONE))
    large = apply(TERM, RecoilStart((10**6, 0, 0)), RecoilOwn((0, 0, 0), NONE))
    assert small.momentum == large.momentum == (1008, 0, 0)
    giving = apply(
        RecoilTerm(21, 4, GIVING, WALL, UNIT), RecoilStart((1, 0, 0)), RecoilOwn((0, 0, 0), NONE)
    )
    assert giving.momentum == (-1008, 0, 0) and giving.remainders == NONE
    symmetric = apply(TERM, RecoilStart((0, 0, 0)), RecoilOwn((7, 8, 9), (1, 2, 3)))
    assert symmetric.momentum == (7, 8, 9) and symmetric.remainders == (1, 2, 3)
    assert [sign_of(v) for v in (-3, 0, 5)] == [-1, 0, 1] and TAKING == 1


def test_the_bounds_and_the_terms_are_refused_by_name():
    """The period, the wavelength, the wall and the unit from 1; a wall at or beyond 2^63 (the row's
    refusal by name; 2^63 - 1 admitted as a wall, its click's amount then refused at the width); the
    sense +1 or -1; a wall that is no multiple of the wavelength; a store at or beyond the wall."""
    with pytest.raises(ValueError, match="from 1, got P_body = 0"):
        apply(RecoilTerm(0, 4, TAKING, WALL, UNIT), START, RecoilOwn((0, 0, 0), NONE))
    with pytest.raises(ValueError, match="L = 0, Q = 64"):
        apply(RecoilTerm(21, 4, TAKING, 0, UNIT), START, RecoilOwn((0, 0, 0), NONE))
    for wall in (1 << 63, (1 << 63) + 1, 1 << 64):
        with pytest.raises(ValueError, match=f"wall L = {wall} reaches the width"):
            apply(RecoilTerm(1, 1, TAKING, wall, 1), START, RecoilOwn((0, 0, 0), NONE))
    with pytest.raises(ValueError, match="amount 3 Q P_body .* reaches the width"):
        apply(RecoilTerm(1, 1, TAKING, (1 << 63) - 1, 1), START, RecoilOwn((0, 0, 0), NONE))
    with pytest.raises(ValueError, match=r"sense is \+1 \(a taking\) or -1 \(a giving\), got 2"):
        apply(RecoilTerm(21, 4, 2, WALL, UNIT), START, RecoilOwn((0, 0, 0), NONE))
    with pytest.raises(ValueError, match="L = 252 is not a multiple of the wavelength lambda_q = 5"):
        apply(RecoilTerm(21, 5, TAKING, WALL, UNIT), START, RecoilOwn((0, 0, 0), NONE))
    with pytest.raises(ValueError, match="reaches the width"):
        apply(RecoilTerm(10**12, 1, TAKING, 10**8, 10**5), START, RecoilOwn((0, 0, 0), NONE))
    with pytest.raises(ValueError, match="store on axis 1 is 252: a remainder below the wall L = 252"):
        apply(TERM, START, RecoilOwn((0, 0, 0), (0, WALL, 0)))


def test_the_trace_hand_identity_on_the_emitters_run():
    """The emitter's unit world (Q = 64 giving four quanta of light of wavelength 4 along +x, L = 4):
    fed every giving line's integers with the giver's sense, the folder moves n by the whole part and
    keeps the store, and after every giving n equals the exact floor of the sum of the fractions
    (ALGEBRA.md 9.112 item 5; 9.84 (2)); the run itself moves no momentum (the binding is the loop's)."""
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
    unit = document["momentum_unit"]
    own = RecoilOwn((0, 0, 0), NONE)
    total = Fraction(0)
    for line in givings:
        writes = apply(
            RecoilTerm(period, wavelength, GIVING, wavelength, unit),
            RecoilStart(tuple(line["momentum"])),
            own,
        )
        own = RecoilOwn(writes.momentum, writes.remainders)
        total -= Fraction(3 * unit * period, wavelength)
        assert own.momentum[0] == total.numerator // total.denominator < 0 and own.momentum[1:] == (0, 0)


def test_the_declaration_is_the_ledgers_row():
    """The folder declares the row of ALGEBRA.md 9.117: "the recoil" at (iv), writing a body's momentum
    n and its remainders, its function `apply`, its section; the engine's register finds it."""
    assert DECLARATION.name == "the recoil" and DECLARATION.place == "(iv)"
    assert DECLARATION.writes == ("a body's momentum n", "a body's remainders")
    assert DECLARATION.function is apply and DECLARATION.built
    assert DECLARATION.word == "after the step" and folder_of(DECLARATION.name) == "recoil"
    assert DECLARATION.section.startswith(THE_WORD) and "the universe's wall L" in DECLARATION.reads
    simulation = DetectorLawSimulation(parse_nature_beam_world(emitter_world(stock=1, ticks=2)))
    registered = simulation.register.declarations["the recoil"]
    assert registered.reads == DECLARATION.reads and registered.function is apply
    assert registered.place_of("a body's momentum n") == "(iv)"
