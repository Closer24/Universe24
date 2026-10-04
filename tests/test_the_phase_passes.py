"""The phase passes with the quantum (B1 of the law-engine alignment audit, #1793 comments 5982140872 and 5982171035 (3), the mathematician's of 17:14 UTC; ALGEBRA.md, The two-mode line, row 16, and The click writes on the GameBoard (j), the giving): the entered part's direction is the leaving part's turned by the arriving record's phase at the Node, atan2(Y', X) of the window's two sums, and the born light's source begins at the phase phi_e - phi_g read from the two parts' directions at the Node."""

import math
import random

from event_universe import meeting
from event_universe.core.rule3 import division_forward
from event_universe.features.click import SCALE_OF
from event_universe.game_board import GameBoard
from event_universe.giving import increments_of, radiated_total, start_of
from event_universe.resonance import turned_direction
from event_universe.world_files import load_world
from tests.laws import EVENTS


def float_turn(re: int, im: int, x: int, y: int) -> tuple[float, float]:
    """The float rotation of (re, im) by the angle of (x, y), the reference the integer act is held against."""
    angle = math.atan2(y, x)
    return re * math.cos(angle) - im * math.sin(angle), re * math.sin(angle) + im * math.cos(angle)


def test_the_entered_part_is_laid_in_the_leaving_parts_direction_turned_by_the_arrivals_phase(
    monkeypatch,
):
    """`resonance.turned_direction` on exact cases, against the float rotation within one level where the size isqrt(X^2 + Y'^2) is exact (a Pythagorean arrival) or large (the engine's arrivals stand at the scale R, about 10^7), the division act's floor; then on the Zeno world (examples/events/zeno/zeno_2.json) at its first taking, `relaid` spied: the entered part's (re, im) is the leaving part's direction turned by the (X, Y') the close held, not the bare leaving direction (Y' is not 0), the leaving part laid at 0 in its own direction, the sense passed unchanged."""
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
    turned_labels, relaid, leaving_phase = meeting.turned_labels, meeting.relaid, meeting.leaving_phase

    def held(board, books):
        pairs = zip(books.declared.transitions, books.references, strict=True)
        arrivals[board.tick] = [(t.leaves, t.enters, r.in_phase, r.quadrature) for t, r in pairs]
        turned_labels(board, books)

    def spied(board, books, part, count, phase, sense):
        laid.append((board.tick, part, count, phase, sense))
        relaid(board, books, part, count, phase, sense)

    def read(board, item):
        found = leaving_phase(board, item)
        left.append((board.tick, item.part, found))
        return found

    monkeypatch.setattr(meeting, "turned_labels", held)
    monkeypatch.setattr(meeting, "relaid", spied)
    monkeypatch.setattr(meeting, "leaving_phase", read)
    board = GameBoard(load_world(EVENTS / "zeno" / "zeno_2.json"), (lines := []).append)
    taken: list[dict] = []
    while not taken and board.tick < 96:
        board.step()
        taken = [
            c for c in lines if c["event"] == "credit" and c["label"] == "NODEREADER" and c["taken"]
        ]
    tick = board.tick
    assert taken and taken[0]["tick"] == tick
    leaves, ((re, im), sense) = next((part, found) for t, part, found in left if t == tick)
    enters = 1 - leaves
    x, y = next((x, y) for low, up, x, y in arrivals[tick] if (low, up) == (leaves, enters))
    entered = next((c, phase, s) for t, p, c, phase, s in laid if t == tick and p == enters)
    print(
        f"the Zeno world's first taking at {tick}: the leaving part {leaves} stands at {(re, im)}, the arrival "
        f"(X, Y') = {(x, y)}, atan2 = {math.degrees(math.atan2(y, x)):.3f} degrees, the entered part laid at {entered[1]}"
    )
    assert y != 0 and entered == (1, turned_direction(re, im, x, y), sense) and entered[1] != (re, im)
    assert all(abs(f - e) <= 1 for f, e in zip(entered[1], float_turn(re, im, x, y), strict=True))
    assert next((c, phase, s) for t, p, c, phase, s in laid if t == tick and p == leaves) == (
        0,
        (re, im),
        sense,
    )


def test_the_born_lights_source_begins_at_the_phase_from_the_ground_parts_direction_to_the_excited_parts():
    """`giving.start_of` and `giving.increments_of` with the two parts' directions: e parallel to g, a part at 0 or no parts named reproduce the old start bit for bit, (R, R num div den rounded half up); at phi = +90 degrees (e = (0, A), g = (A, 0)) r_0 = 0 and r_(-1) = R sin Omega within one level of the float; at 180 degrees r_0 = -R; at 270 degrees r_(-1) = -R sin Omega; the first increment A_0 cos phi; the amplitudes, which carry the quantum, identical at every phase with their squares summing to S within the carry, and the increments' squares, the cosine's half of them, within two percent of that half at every phase (the span 48 holds 6.4 periods of [2, 3])."""
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
