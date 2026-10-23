"""The phase passes with the quantum (B1 of the law-engine alignment audit, #1793 comments 5982140872 and 5982171035 (3), the mathematician's of 17:14 UTC; ALGEBRA.md, The two-mode line, row 16, and The click writes on the lattice (j), the emission): the entered part's direction is the leaving part's turned by the arriving record's phase at the Node, atan2(Y', X) of the window's two sums, and the born light's source begins at the phase phi_e - phi_g read from the two parts' directions at the Node."""

import math
import random

from event_universe import act, meeting
from event_universe.core.rule3 import division_forward
from event_universe.emission import increments_of, radiated_total, start_of
from event_universe.features.click import SCALE_OF
from event_universe.lattice import Lattice
from event_universe.resonance import turned_direction
from event_universe.world_files import load_world
from tests.laws import EVENTS
from tests.laws_content import TWO_ATOMS, content_copy
from tests.laws_read import load_shipped


def float_turn(re: int, im: int, x: int, y: int) -> tuple[float, float]:
    """The float rotation of (re, im) by the angle of (x, y), the reference the integer act is held against."""
    angle = math.atan2(y, x)
    return re * math.cos(angle) - im * math.sin(angle), re * math.sin(angle) + im * math.cos(angle)


def test_the_entered_part_is_laid_in_the_leaving_parts_direction_turned_by_the_arrivals_phase(
    tmp_path,
    monkeypatch,
):
    """`resonance.turned_direction` on exact cases, against the float rotation within one level where the size isqrt(X^2 + Y'^2) is exact (a Pythagorean arrival) or large (the engine's arrivals stand at the scale R, about 10^7), the division act's floor; then on the Zeno world (examples/events/zeno/zeno_2.json) at its first absorption, `relaid` spied: the entered part's (re, im) is the leaving part's direction turned by the (X, Y') the close held, not the bare leaving direction (Y' is not 0), the leaving part laid at 0 in its own direction, the sense passed unchanged."""
    assert turned_direction(1000, 0, 3, 4) == (600, 800)
    assert turned_direction(1000, 0, 1, 0) == (1000, 0)
    assert turned_direction(1000, 0, 0, 1) == (0, 1000)
    assert turned_direction(1000, 0, 0, 0) == (1000, 0)
    assert turned_direction(0, 1000, 0, 1) == (-1000, 0)
    assert turned_direction(600, 800, 3, -4) == (1000, 0)
    draw = random.Random(24)
    for _ in range(300):
        re, im, k = draw.randint(-1000, 1000), draw.randint(-1000, 1000), draw.randint(1, 200)
        for x, y in (
            (3 * k, 4 * k),
            (-8 * k, 15 * k),
            (draw.randint(-(10**8), 10**8), draw.randint(1, 10**8)),
        ):
            found, exact = turned_direction(re, im, x, y), float_turn(re, im, x, y)
            assert all(abs(f - e) <= 1 for f, e in zip(found, exact, strict=True)), (re, im, x, y)
    arrivals: dict[int, list[tuple[int, int, int, int]]] = {}
    laid: list[tuple[int, int, int, tuple[int, int], int]] = []
    left: list[tuple[int, int, tuple[tuple[int, int], int]]] = []
    turned_labels, relaid, leaving_phase = meeting.turned_labels, act.relaid, act.leaving_phase

    def held(board, books):
        pairs = zip(books.declared.transitions, books.references, strict=True)
        arrivals[board.interval] = [(t.leaves, t.enters, r.in_phase, r.quadrature) for t, r in pairs]
        turned_labels(board, books)

    def spied(board, books, part, count, phases):  # C3: one phase per Node of the body
        laid.append((board.interval, part, count, list(phases)))
        relaid(board, books, part, count, phases)

    def read(board, item):
        found = leaving_phase(board, item)
        left.append((board.interval, item.part, found))
        return found

    monkeypatch.setattr(meeting, "turned_labels", held)
    monkeypatch.setattr(act, "relaid", spied)
    monkeypatch.setattr(act, "leaving_phase", read)
    board = Lattice(
        load_world(content_copy(tmp_path, EVENTS / "chain" / "chain_x_minus.json", TWO_ATOMS)),
        (lines := []).append,
    )  # the content copy (re-pinned 2026-10-20 from zeno_2): the shipped world's run is refused by name at the body 0 of 'atom' at the interval 122 (the law's third refusal of the click's read, ALGEBRA.md The digits' budget: the room 2^45.8 of the digits read, the photon's five at three values each on the universe two_atoms.json, which declares no content, and the atom's three at the lay's origin, below the absorption draw's total 2^51.5; the former course took at 74 by the same number read, the rest weight's booking centred on 2026-10-23 moving the residue to the cell none takes), so the claim is read on the content copy (tests/laws_content.content_world, the born universe's holders prepended), which carries every draw
    taken: list[dict] = []
    while not taken and board.interval < 400:
        board.step()
        taken = [
            c for c in lines if c["event"] == "credit" and c["label"] == "NODEDETECTOR" and c["absorbed"]
        ]
    interval = board.interval
    assert taken and taken[0]["interval"] == interval
    leaves, own = next((part, found) for t, part, found in left if t == interval)
    ((re, im), sense), enters = own[0], 1 - leaves
    x, y = next((x, y) for low, up, x, y in arrivals[interval] if (low, up) == (leaves, enters))
    count, phases = next((c, p) for t, part, c, p in laid if t == interval and part == enters)
    entered = (count, phases[0][0], phases[0][1])
    assert phases == [(turned_direction(r, i, x, y), s) for (r, i), s in own]  # C3: each Node its own
    print(
        f"the chain world's first absorption at {interval}: the leaving part {leaves} stands at {(re, im)}, the arrival "
        f"(X, Y') = {(x, y)}, atan2 = {math.degrees(math.atan2(y, x)):.3f} degrees, the entered part laid at {entered[1]}"
    )
    assert y != 0 and entered == (1, turned_direction(re, im, x, y), sense) and entered[1] != (re, im)
    assert all(abs(f - e) <= 1 for f, e in zip(entered[1], float_turn(re, im, x, y), strict=True))
    assert next((c, p) for t, part, c, p in laid if t == interval and part == leaves) == (0, own)


def test_the_born_lights_source_begins_at_the_phase_from_the_ground_parts_direction_to_the_excited_parts():
    """`emission.start_of` and `emission.increments_of` with the two parts' directions: e parallel to g, a part at 0 or no parts named reproduce the plain start bit for bit, (R, R num div den rounded half up); at phi = +90 degrees (e = (0, A), g = (A, 0)) r_0 = 0 and r_(-1) = R sin Omega within one level of the float; at 180 degrees r_0 = -R; at 270 degrees r_(-1) = -R sin Omega; the first increment A_0 cos phi; the amplitudes, which carry the quantum, identical at every phase with their squares summing to S within the carry, and the increments' squares, the cosine's half of them, within two percent of that half at every phase (the span 48 holds 6.4 periods of [2, 3])."""
    scale, total, (num, den) = (3 * 6000 * 32768) ** SCALE_OF, radiated_total(32768, (2, 3)), (2, 3)
    old = (scale, int(division_forward(scale * num, den, division_forward(den, 2, 0)[0])[0]))
    assert start_of(scale, (num, den), None) == old
    for parallel in (((90, 0), (90, 0)), ((75, 51), (0, 0)), ((-30, 40), (-6, 8)), ((-30, 40), (-3, 4))):
        assert start_of(scale, (num, den), parallel) == old, parallel
    sine = math.sqrt(den * den - num * num) / den
    phases = {
        0: ((90, 0), (90, 0)),
        90: ((0, 90), (90, 0)),
        180: ((-90, 0), (90, 0)),
        270: ((0, -90), (90, 0)),
    }
    quarter, half, three = (start_of(scale, (num, den), phases[k]) for k in (90, 180, 270))
    assert quarter[0] == 0 and abs(quarter[1] - scale * sine) <= 1
    assert half == (-scale, -old[1])
    assert three[0] == 0 and abs(three[1] + scale * sine) <= 1
    base, amplitudes = increments_of(total, 48, (num, den), scale)
    assert increments_of(total, 48, (num, den), scale, phases[0]) == (base, amplitudes)
    squares = sum(a * a for a in amplitudes)
    assert 0 <= total - squares <= max(amplitudes) ** 2
    for degrees, levels in phases.items():
        increments, found = increments_of(total, 48, (num, den), scale, levels)
        start = start_of(scale, (num, den), levels)
        print(
            f"phi = {degrees} degrees: the start (r_0, r_(-1)) = {start}, the first increments {increments[:4]}, "
            f"SUM A_t^2 = {squares} against S = {total}, SUM increments^2 = {sum(d * d for d in increments)}"
        )
        assert found == amplitudes
        assert increments[0] == {0: amplitudes[0], 90: 0, 180: -amplitudes[0], 270: 0}[degrees]
        assert abs(2 * sum(d * d for d in increments) - squares) <= division_forward(squares, 50, 0)[0]
