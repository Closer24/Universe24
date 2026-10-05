"""The breaker's rows for the paper's theorems of the conserved form, the Wronskian, the share and the momentum flux (Theorem 3, Sections 4.2 to 4.4 and 5.5, S.5, S.6, S.9, S.32, S.48): each tried inside its stated condition (paces fixed in time, the Link's factor on the current, a closed or periodic board, |num| <= den) and outside it, on boards of 2x2x2 to 4x3x2 Nodes in exact rationals and integers. Every step is proofs_ground.py's line or rule3.py's integer step, every form proofs_form.py's or proofs_booking.py's; this module holds no arithmetic of the law of its own. The Row and the boards are counterexample_rows.py's; the registry is counterexamples.py's."""

from __future__ import annotations

import math
import random
import sys
from collections.abc import Callable, Sequence
from fractions import Fraction
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import rule3  # noqa: E402
from counterexample_rows import (  # noqa: E402
    PORTS,
    SHAPES,
    Board,
    Row,
    levels,
    uneven_board,
    weighted_currents,
)
from proofs_booking import (  # noqa: E402
    check_the_momentum_flux_identity_with_the_remainders,
    rational_share,
)
from proofs_form import plain_form, weighted_form  # noqa: E402
from proofs_ground import (  # noqa: E402
    SEED,
    box_arrivals,
    box_nodes,
    pairs,
    read,
    step_integer,
    step_line,
)

AXES = rule3.AXES


def exact_steps(
    draw: random.Random, board: Board, num: int, den: int, gamma: int, steps: int
) -> tuple[list[list[Fraction]], tuple]:
    """The line without its division over `steps` intervals from random integer levels on the board; returns the levels (before, now, next, ...) and the read (w, R, S, p)."""
    arrivals, clocks, factors = board
    coefficients = read(arrivals, clocks, factors, num, den, gamma)
    wall, reads, selves, _ = coefficients
    history = [
        [Fraction(v) for v in levels(draw, len(arrivals))],
        [Fraction(v) for v in levels(draw, len(arrivals))],
    ]
    for _ in range(steps):
        history.append(step_line(arrivals, reads, selves, wall, history[-1], history[-2]))
    return history, coefficients


def weighted_form_is_exact_at_static_paces() -> Row:
    """Theorem 3 (Section 4.2), S.32, 'The change is 0 at paces fixed in time, uniform or not, for the weighted form (for the plain form at fixed uniform paces alone)': on boards of 2x2x2 to 4x3x2 with uneven clocks and tensions the weighted form E is constant over ten steps of the line, exactly; the plain form (the Link factor dropped) moves there, and is constant where the paces are uniform; where the paces move in time (the clocks changed between steps) the weighted total moves, the work term."""
    draw = random.Random(SEED)
    weighted_holds, plain_at_uniform, plain_moves, moving_moves = True, True, False, False
    for (num, den), shape in zip(pairs(draw, 3), SHAPES, strict=True):
        gamma = draw.randint(2, 9)
        board = uneven_board(draw, shape, gamma)
        history, (wall, reads, selves, paces) = exact_steps(draw, board, num, den, gamma, 10)
        arrivals = board[0]
        totals = {
            weighted_form(reads, selves, wall, paces, arrivals, history[t], history[t - 1], num, gamma)
            for t in range(1, len(history))
        }
        weighted_holds &= len(totals) == 1
        plains = {
            plain_form(reads, selves, wall, paces, arrivals, history[t], history[t - 1], num)
            for t in range(1, 4)
        }
        plain_moves |= len(plains) > 1
        # the plain form at uniform paces and no tension: constant
        uniform = (arrivals, [gamma] * len(arrivals), [[gamma] * PORTS for _ in arrivals])
        flat, (wall_u, reads_u, selves_u, paces_u) = exact_steps(draw, uniform, num, den, gamma, 6)
        plain_at_uniform &= (
            len(
                {
                    plain_form(reads_u, selves_u, wall_u, paces_u, arrivals, flat[t], flat[t - 1], num)
                    for t in range(1, 7)
                }
            )
            == 1
        )
        # the paces moving in time: one Node's clock changed before the second step
        arrivals, clocks, factors = board
        wall, reads, selves, paces = read(arrivals, clocks, factors, num, den, gamma)
        first = step_line(arrivals, reads, selves, wall, history[1], history[0])
        deeper = list(clocks)
        deeper[0] = max(1, clocks[0] - gamma)
        wall_2, reads_2, selves_2, paces_2 = read(arrivals, deeper, factors, num, den, gamma)
        second = step_line(arrivals, reads_2, selves_2, wall_2, first, history[1])
        # E read at the new paces after the step against E read at the old paces before it: the work term
        moving_moves |= weighted_form(
            reads_2, selves_2, wall_2, paces_2, arrivals, second, first, num, gamma
        ) != weighted_form(reads, selves, wall, paces, arrivals, first, history[1], num, gamma)
    return Row(
        "The change is 0 at paces fixed in time uniform or not for th",
        weighted_holds and plain_at_uniform,
        plain_moves and moving_moves,
        f"weighted E one value over 10 steps on {len(SHAPES)} uneven boards; plain form moves under tension, constant at uniform paces; a moving clock moves E",
    )


def wronskian_total(
    re_now: Sequence[Fraction],
    im_now: Sequence[Fraction],
    re_before: Sequence[Fraction],
    im_before: Sequence[Fraction],
    weights: Sequence[Fraction] | None,
) -> Fraction:
    """SUM_i d_i (re_now_i im_before_i - im_now_i re_before_i), the Wronskian of a two-part record (S.9), d_i = 1 / p_i^2 or 1 for the plain total."""
    total = Fraction(0)
    for i in range(len(re_now)):
        d = Fraction(1) if weights is None else weights[i]
        total += d * (re_now[i] * im_before[i] - im_now[i] * re_before[i])
    return total


def two_part_steps(
    draw: random.Random,
    board: Board,
    num: int,
    den: int,
    gamma: int,
    steps: int,
    clocks_in_time: Callable[[int], list[int]] | None = None,
):
    """A two-part record (re, im) stepped by the line without its division, the paces read at each step from `clocks_in_time(t)` (the board's clocks when None); returns the two histories and the weights 1 / p_i^2 of each step's read."""
    arrivals, clocks, factors = board
    re = [[Fraction(v) for v in levels(draw, len(arrivals))] for _ in range(2)]
    im = [[Fraction(v) for v in levels(draw, len(arrivals))] for _ in range(2)]
    weights = []
    for t in range(steps):
        wall, reads, selves, paces = read(
            arrivals, clocks if clocks_in_time is None else clocks_in_time(t), factors, num, den, gamma
        )
        weights.append([1 / p**2 for p in paces])
        re.append(step_line(arrivals, reads, selves, wall, re[-1], re[-2]))
        im.append(step_line(arrivals, reads, selves, wall, im[-1], im[-2]))
    return re, im, weights


def wronskian_conserved_by_the_line_at_static_paces() -> Row:
    """Section 5.5, S.9: the weighted Wronskian SUM_i W_i / p_i^2 is constant over ten steps of the line on boards with uneven clocks and tensions; outside: the integer step's division moves W (S.9's counterexample at [2, 3]: the parts (1, 3) over zeros step to (1, 4), W from 0 to -1), and paces moving in time without the time-Link turn move the weighted total (the work term)."""
    draw = random.Random(SEED)
    holds, integer_moves, moving_moves = True, False, False
    for (num, den), shape in zip(pairs(draw, 3), SHAPES, strict=True):
        gamma = draw.randint(2, 9)
        board = uneven_board(draw, shape, gamma)
        re, im, weights = two_part_steps(draw, board, num, den, gamma, 10)
        totals = {wronskian_total(re[t], im[t], re[t - 1], im[t - 1], weights[0]) for t in range(1, 12)}
        holds &= len(totals) == 1
        clocks = board[1]

        def moving(t: int, clocks=clocks, gamma=gamma) -> list[int]:
            return [max(1, c - gamma * t) if i == 0 else c for i, c in enumerate(clocks)]

        re_m, im_m, weights_m = two_part_steps(draw, board, num, den, gamma, 3, moving)
        moving_moves |= wronskian_total(
            re_m[3], im_m[3], re_m[2], im_m[2], weights_m[2]
        ) != wronskian_total(re_m[2], im_m[2], re_m[1], im_m[1], weights_m[1])
    re_one = rule3.step(1, 0, [1] * PORTS, 2, 3, 0, 5)[0]
    im_one = rule3.step(3, 0, [3] * PORTS, 2, 3, 0, 5)[0]
    integer_moves = (re_one, im_one, re_one * 3 - im_one * 1) == (1, 4, -1)
    return Row(
        "The line without its division conserves it exactly with the",
        holds,
        integer_moves and moving_moves,
        f"weighted W one value over 10 steps on {len(SHAPES)} uneven boards; the integer step at [2, 3] moves W 0 -> {re_one * 3 - im_one}; a moving clock moves the total",
    )


def wronskian_total_under_a_change_of_paces() -> Row:
    """Section 5.5, 'Its total over the lattice is invariant under any change of the paces that keeps them uniform over the lattice, the weighted total exact at any paces fixed in time, and where the paces move it changes by SUM_i (d_i(t + 1) - d_i(t)) W_i(t + 1)': the plain total under uniform paces changing every step; the weighted total at static uneven paces; the weighted total's change under moving uneven paces against the formula, all exact; outside: a non-uniform change moves the plain total."""
    draw = random.Random(SEED)
    uniform_holds, static_holds, formula_holds, plain_moves = True, True, True, False
    for (num, den), shape in zip(pairs(draw, 3), SHAPES, strict=True):
        gamma = draw.randint(3, 9)
        arrivals = box_arrivals(shape)
        count = len(arrivals)
        no_tension = [[gamma] * PORTS for _ in arrivals]
        uniform_in_time = [draw.randint(1, gamma) for _ in range(6)]
        re, im, _ = two_part_steps(
            draw,
            (arrivals, [gamma] * count, no_tension),
            num,
            den,
            gamma,
            6,
            lambda t, paces=uniform_in_time, count=count: [paces[t]] * count,
        )
        uniform_holds &= (
            len({wronskian_total(re[t], im[t], re[t - 1], im[t - 1], None) for t in range(1, 8)}) == 1
        )
        board = uneven_board(draw, shape, gamma)
        re, im, weights = two_part_steps(draw, board, num, den, gamma, 6)
        static_holds &= (
            len({wronskian_total(re[t], im[t], re[t - 1], im[t - 1], weights[0]) for t in range(1, 8)})
            == 1
        )
        clocks = board[1]

        def moving(t: int, clocks=clocks, gamma=gamma) -> list[int]:
            return [max(1, c - gamma * (t % 2) * (i % 2)) for i, c in enumerate(clocks)]

        re, im, weights = two_part_steps(draw, board, num, den, gamma, 4, moving)
        for t in range(1, 4):  # weights[t] is the read of the step from (t, t - 1) to t + 1
            change = wronskian_total(re[t + 1], im[t + 1], re[t], im[t], weights[t]) - wronskian_total(
                re[t], im[t], re[t - 1], im[t - 1], weights[t - 1]
            )
            formula = sum(
                (weights[t][i] - weights[t - 1][i]) * (re[t + 1][i] * im[t][i] - im[t + 1][i] * re[t][i])
                for i in range(count)
            )
            formula_holds &= change == formula
            plain_moves |= wronskian_total(re[t + 1], im[t + 1], re[t], im[t], None) != wronskian_total(
                re[t], im[t], re[t - 1], im[t - 1], None
            )
    return Row(
        "Its total over the lattice is invariant under any change of",
        uniform_holds and static_holds and formula_holds,
        plain_moves,
        "plain W constant under uniform paces changing each step; weighted W constant at static uneven paces; moving uneven paces: change = SUM (d(t+1) - d(t)) W(t+1) exactly; the plain total moves there",
    )


def boards_conservations_are_the_form_and_the_wronskian() -> Row:
    """Section 3.5 ('In the clicks there are conservations other than the board's'): the board's conservations are theorems of the line, the weighted form and the weighted Wronskian constant at static paces (the two rows above, run here on one more board); no total energy: a family's form moves when its paces move (no theorem equates one family's loss with another's gain). The credit's conservation of the count is the engine's act (kind (e)) and is not tested here."""
    draw = random.Random(SEED + 1)
    num, den, gamma = 2, 3, 7
    board = uneven_board(draw, (3, 3, 2), gamma)
    history, (wall, reads, selves, paces) = exact_steps(draw, board, num, den, gamma, 8)
    arrivals = board[0]
    form_holds = (
        len(
            {
                weighted_form(
                    reads, selves, wall, paces, arrivals, history[t], history[t - 1], num, gamma
                )
                for t in range(1, 10)
            }
        )
        == 1
    )
    re, im, weights = two_part_steps(draw, board, num, den, gamma, 8)
    wronskian_holds = (
        len({wronskian_total(re[t], im[t], re[t - 1], im[t - 1], weights[0]) for t in range(1, 10)}) == 1
    )
    # the paces moving: the second step read at clocks one Gamma deeper on every Node
    clocks = board[1]
    deeper = [max(1, c - gamma) for c in clocks]
    re_m, _, _ = two_part_steps(draw, board, num, den, gamma, 2, lambda t: clocks if t == 0 else deeper)
    wall_d, reads_d, selves_d, paces_d = read(arrivals, deeper, board[2], num, den, gamma)
    moving_form = weighted_form(
        reads_d, selves_d, wall_d, paces_d, arrivals, re_m[3], re_m[2], num, gamma
    ) != weighted_form(reads, selves, wall, paces, arrivals, re_m[2], re_m[1], num, gamma)
    return Row(
        "In the clicks there are conservations other than the lattice",
        form_holds and wronskian_holds,
        moving_form,
        "weighted E and weighted W constant over 8 steps on a 3x3x2 uneven board; the form moves under moving paces (no total energy on the board); the credit's count is the engine's act, not tested here",
    )


def momentum(num: int, now: Sequence, before: Sequence, i: int, minus: int, plus: int) -> Fraction:
    """P_a(i) = (F_(i, i - a) - F_(i, i + a)) / num, the current per axis (Section 4.3, Eq. (7)), from rule3.link_current at the vacuum's factor."""
    return (
        rule3.link_current(num, now[i], before[i], now[minus], before[minus])
        - rule3.link_current(num, now[i], before[i], now[plus], before[plus])
    ) / num


def integer_step_subtracts_the_remainder_term() -> Row:
    """Eq. (7), S.48 ('the integer step subtracts the remainder term delta_i Delta_a(now)_i - now_i Delta_a(delta)_i with delta = r - r''): on a 3x3x3 periodic board at uniform coefficients, w [P_a(next, now) - P_a(next*, now)] equals -(delta_i Delta_a now_i - now_i Delta_a delta_i) at every Node and axis, next the integer step's level and next* the line's, Delta_a x_i = x_(i + a) - x_(i - a), in exact integers; the full identity with the stresses G_ab is proofs_booking's check; outside: the term dropped, the identity fails at some Node."""
    draw = random.Random(SEED)
    shape = (3, 3, 3)
    nodes, arrivals = box_nodes(shape), box_arrivals(shape)
    holds, dropped_fails = True, False
    for num, den in pairs(draw, 4):
        gamma = draw.randint(2, 9)
        clock, links = (
            draw.randint(1, gamma),
            (draw.randint(1, gamma), draw.randint(1, gamma), draw.randint(1, gamma)),
        )
        wall, _, _ = rule3.coefficients(num, den, gamma, clock, links)
        now, before = levels(draw, len(nodes)), levels(draw, len(nodes))
        remainders = [draw.randint(0, wall - 1) for _ in nodes]
        exact = [
            rule3.step_exact(
                now[i], before[i], [now[j] for j in arrivals[i]], num, den, gamma, clock, links
            )
            for i in range(len(nodes))
        ]
        stepped = [
            rule3.step(
                now[i],
                before[i],
                [now[j] for j in arrivals[i]],
                num,
                den,
                remainders[i],
                gamma,
                clock,
                links,
            )
            for i in range(len(nodes))
        ]
        integer, carried = [s[0] for s in stepped], [s[1] for s in stepped]
        delta = [r - r_out for r, r_out in zip(remainders, carried, strict=True)]
        for i in range(len(nodes)):
            for axis in range(AXES):
                plus, minus = arrivals[i][2 * axis], arrivals[i][2 * axis + 1]
                left = wall * (
                    momentum(num, integer, now, i, minus, plus)
                    - momentum(num, exact, now, i, minus, plus)
                )
                term = delta[i] * (now[plus] - now[minus]) - now[i] * (delta[plus] - delta[minus])
                holds &= left == -term
                dropped_fails |= left != 0
    full = check_the_momentum_flux_identity_with_the_remainders()[0]
    return Row(
        "The integer step subtracts the remainder term deltaiDeltaai",
        holds and full,
        dropped_fails,
        "w [P_a(next) - P_a(next*)] = -(delta_i Delta_a now_i - now_i Delta_a delta_i) at every Node and axis of a 3x3x3 board, 4 pairs; Eq. (7) with the stresses by proofs_booking; the term dropped fails",
    )


def share_change_on_a_board(
    draw: random.Random, shape: tuple[int, int, int], num: int, den: int, gamma: int
):
    """One integer step and one exact step on an uneven board; returns the board's read and (now, before, next*, next, r, r')."""
    arrivals, clocks, factors = uneven_board(draw, shape, gamma)
    wall, reads, selves, paces = read(arrivals, clocks, factors, num, den, gamma)
    now, before = levels(draw, len(arrivals)), levels(draw, len(arrivals))
    remainders = [draw.randint(0, int(wall) - 1) for _ in arrivals]
    exact = step_line(arrivals, reads, selves, wall, now, before)
    integer, carried = step_integer(arrivals, reads, selves, wall, now, before, remainders)
    return (arrivals, factors, wall, reads, selves, paces), (
        now,
        before,
        exact,
        integer,
        remainders,
        carried,
    )


def shares_change_is_the_six_weighted_currents() -> Row:
    """Eq. (10), S.5, 'Over one step of Rule3 the share's rational value, before its floor, changes by exactly the six currents into the Node, each weighted by its Link's factor, plus Rule3's own rounding': on 2x2x2 to 4x3x2 boards with uneven clocks and tensions, e_i(next*, now) - e_i(now, before) = SUM_j (q_ij / Gamma)^2 F_ij exactly, and the integer step's change is that plus -(next_i - before_i)(r'_i - r_i) / (2 p_i^2); the floored share's change differs from the rational by less than two units (the floors); outside: the plain currents, the Link factor dropped, fail where a tension stands."""
    draw = random.Random(SEED)
    holds, plain_fails, floors_small = True, False, True
    for (num, den), shape in zip(pairs(draw, 3), SHAPES, strict=True):
        gamma = draw.randint(2, 9)
        (
            (arrivals, factors, wall, reads, selves, paces),
            (now, before, exact, integer, remainders, carried),
        ) = share_change_on_a_board(draw, shape, num, den, gamma)
        for i in range(len(arrivals)):
            start = rational_share(wall, reads, selves, paces, arrivals, i, now, before)
            change = rational_share(wall, reads, selves, paces, arrivals, i, exact, now) - start
            currents = weighted_currents(factors, arrivals, i, now, before, num, gamma)
            holds &= change == currents
            plain = weighted_currents(
                [[gamma] * PORTS] * len(arrivals), arrivals, i, now, before, num, gamma
            )
            plain_fails |= change != plain
            integer_change = (
                rational_share(wall, reads, selves, paces, arrivals, i, integer, now) - start
            )
            term = -Fraction((integer[i] - before[i]) * (carried[i] - remainders[i])) / (
                2 * paces[i] ** 2
            )
            holds &= integer_change == currents + term
            floored = math.floor(
                rational_share(wall, reads, selves, paces, arrivals, i, integer, now)
            ) - math.floor(start)
            floors_small &= abs(floored - integer_change) < 2
    return Row(
        "Over one step of Rule3 the shares rational value before its",
        holds and floors_small,
        plain_fails,
        f"exact at every Node of {len(SHAPES)} uneven boards, with and without the division; the floored share within two units; the plain currents fail under tension",
    )


def boundary_currents(
    region: set[int],
    arrivals: Sequence[Sequence[int]],
    factors: Sequence[Sequence[int]],
    now: Sequence[int],
    before: Sequence[int],
    num: int,
    gamma: int,
) -> Fraction:
    """The weighted currents through the Ports leaving the region (rule3.link_current), the interior Links cancelling pairwise."""
    return sum(
        (
            rule3.link_current(num, now[i], before[i], now[j], before[j], factors[i][port], gamma)
            for i in region
            for port, j in enumerate(arrivals[i])
            if j not in region
        ),
        Fraction(0),
    )


def regions_share_changes_by_boundary_currents() -> Row:
    """Section 4.4 ('So over any region the total share changes only by the weighted currents through the region's boundary, the remainder terms and the readers' floors'): on uneven boards, for a random region, a one-Node region and the whole board, SUM_R [e_i(next, now) - e_i(now, before)] equals the weighted currents through the boundary Ports plus the remainder terms, the interior Links cancelling; outside the fence 'at standing paces': the clocks changed between the read and the next step, the region's change is not its boundary currents."""
    draw = random.Random(SEED)
    holds, moving_fails = True, False
    for (num, den), shape in zip(pairs(draw, 3), SHAPES, strict=True):
        gamma = draw.randint(2, 9)
        (
            (arrivals, factors, wall, reads, selves, paces),
            (now, before, exact, integer, remainders, carried),
        ) = share_change_on_a_board(draw, shape, num, den, gamma)
        count = len(arrivals)
        regions = [
            {draw.randrange(count)},
            set(range(count)),
            {i for i in range(count) if draw.random() < 0.5},
        ]
        for region in regions:
            change = sum(
                rational_share(wall, reads, selves, paces, arrivals, i, integer, now)
                - rational_share(wall, reads, selves, paces, arrivals, i, now, before)
                for i in region
            )
            terms = sum(
                -Fraction((integer[i] - before[i]) * (carried[i] - remainders[i])) / (2 * paces[i] ** 2)
                for i in region
            )
            holds &= (
                change == boundary_currents(region, arrivals, factors, now, before, num, gamma) + terms
            )
        # the paces moving: the shares after the step read at clocks other than the step's
        clocks = [max(1, gamma * draw.randint(1, 3)) for _ in arrivals]
        deeper = read(arrivals, [c - 1 for c in clocks], factors, num, den, gamma)
        region = regions[2]
        moved = sum(
            rational_share(deeper[0], deeper[1], deeper[2], deeper[3], arrivals, i, exact, now)
            - rational_share(wall, reads, selves, paces, arrivals, i, now, before)
            for i in region
        )
        moving_fails |= moved != boundary_currents(region, arrivals, factors, now, before, num, gamma)
    return Row(
        "So over any region the total share changes only by the weigh",
        holds,
        moving_fails,
        "a one-Node region, the whole board and a random region on 3 uneven boards: change = boundary currents + remainder terms exactly; a clock moved after the read breaks it",
    )


def vacuum_total_share(
    num: int,
    den: int,
    arrivals: Sequence[Sequence[int]],
    now: Sequence[int],
    before: Sequence[int],
    gamma: int = 1,
) -> Fraction:
    """SUM_i e_i at the vacuum's coefficients (rule3.coefficients at p_0 = p_a = Gamma), e_i the weighted share of proofs_booking; an arrival index equal to the Node count is an open face reading 0."""
    wall, reads, self_coefficient = rule3.coefficients(num, den, gamma)
    count = len(now)
    padded_now, padded_before = [*now, 0], [*before, 0]
    reads_table = [[Fraction(reads[port // 2]) for port in range(PORTS)] for _ in range(count)]
    selves = [Fraction(self_coefficient)] * count
    paces = [Fraction(gamma)] * count
    return sum(
        rational_share(
            Fraction(wall), reads_table, selves, paces, arrivals, i, padded_now, padded_before
        )
        for i in range(count)
    )


def total_share_nonnegative_inside_the_guard() -> Row:
    """Section 4.4, S.6, 'The total share of a closed or periodic lattice is non-negative for |num| <= den at the vacuum's coefficients, with equality for a static uniform level of light and, on an even periodic board, for its checkerboard': random integer levels on periodic boards and on a folded chain for pairs with |num| <= den, negative numerators included, 60 draws each; the two equalities at [1, 1]; outside: |num| > den gives a negative total (a uniform static level). A board with an open face reading 0 beyond is also tried: S_6 keeps its norm at or under 6 there and the total stays non-negative, so the fence's 'closed or periodic' is not what the sign needs (a note for the hands, the breaker's expectation and not the claim's)."""
    draw = random.Random(SEED)
    boards = {
        "2x2x2": box_arrivals((2, 2, 2)),
        "3x3x3": box_arrivals((3, 3, 3)),
        "4x2x2": box_arrivals((4, 2, 2)),
        "folded chain of 5": rule3.chain_arrivals(5),
    }
    open_face = [
        [j if j != 0 or i == 0 else 5 for j in ports] for i, ports in enumerate(rule3.chain_arrivals(5))
    ]
    open_face[0] = [1, 5, 0, 0, 0, 0]  # the Node 0's -x Port opens onto the face
    open_face[4] = [5, 3, 4, 4, 4, 4]  # the Node 4's +x Port opens onto the face
    inside, open_negative, beyond_negative = True, False, False
    for num, den in [*pairs(draw, 4), (-1, 2), (-3, 4), (-1, 1), (1, 1)]:
        for arrivals in boards.values():
            for _ in range(60):
                now, before = levels(draw, len(arrivals), 9), levels(draw, len(arrivals), 9)
                inside &= vacuum_total_share(num, den, arrivals, now, before) >= 0
        for _ in range(60):
            now, before = levels(draw, 5, 9), levels(draw, 5, 9)
            open_negative |= vacuum_total_share(num, den, open_face, now, before) < 0
        beyond_negative |= vacuum_total_share(abs(num) + den, den, boards["2x2x2"], [3] * 8, [3] * 8) < 0
    uniform_light = vacuum_total_share(1, 1, boards["3x3x3"], [5] * 27, [5] * 27) == 0
    checker = [(-1) ** sum(x) for x in box_nodes((2, 2, 2))]
    checkerboard = vacuum_total_share(1, 1, boards["2x2x2"], checker, [-c for c in checker]) == 0
    return Row(
        "The total share of any lattice whose Links read the same fro",
        inside and uniform_light and checkerboard,
        beyond_negative,
        f"non-negative over {len(boards)} boards x 8 pairs x 60 draws; equality at uniform light and at the checkerboard; |num| > den negative; an open face negative: {open_negative} (S_6's norm stays at or under 6 there)",
    )


def acts_form_no_product_of_levels() -> Row:
    """Theorem 2 (Section 4.1), 'The rule's acts form no product of levels': the line without its division is linear in the levels (now, before and the six arrivals) exactly, f(alpha x + beta y) = alpha f(x) + beta f(y), and the integer step lies within one unit of it; outside the acts: the share, a reading, is bilinear, e(2 x, 2 y) = 4 e(x, y)."""
    draw = random.Random(SEED)
    linear, within_one, share_quadratic = True, True, True
    for num, den in pairs(draw, 4):
        gamma = draw.randint(2, 9)
        clock, links = (
            draw.randint(1, gamma),
            (draw.randint(1, gamma), draw.randint(1, gamma), draw.randint(1, gamma)),
        )
        x = [Fraction(draw.randint(-30, 30)) for _ in range(PORTS + 2)]
        y = [Fraction(draw.randint(-30, 30)) for _ in range(PORTS + 2)]
        alpha, beta = (
            Fraction(draw.randint(-5, 5), draw.randint(1, 4)),
            Fraction(draw.randint(-5, 5), draw.randint(1, 4)),
        )

        def line(v: Sequence[Fraction], pair=(num, den), paces=(gamma, clock, links)) -> Fraction:
            return rule3.step_exact(v[0], v[1], v[2:], pair[0], pair[1], *paces)

        combined = [alpha * a + beta * b for a, b in zip(x, y, strict=True)]
        linear &= line(combined) == alpha * line(x) + beta * line(y)
        integer = [draw.randint(-30, 30) for _ in range(PORTS + 2)]
        wall, _, _ = rule3.coefficients(num, den, gamma, clock, links)
        remainder = draw.randint(0, wall - 1)
        stepped = rule3.step(
            integer[0], integer[1], integer[2:], num, den, remainder, gamma, clock, links
        )[0]
        within_one &= (
            abs(Fraction(stepped) - line([Fraction(v) for v in integer]) - Fraction(remainder, wall)) < 1
        )
        arrivals = box_arrivals((2, 2, 2))
        wall_f, reads, selves, paces = read(
            arrivals, [gamma] * 8, [[gamma] * PORTS] * 8, num, den, gamma
        )
        now, before = levels(draw, 8), levels(draw, 8)
        single = rational_share(wall_f, reads, selves, paces, arrivals, 0, now, before)
        doubled = rational_share(
            wall_f, reads, selves, paces, arrivals, 0, [2 * v for v in now], [2 * v for v in before]
        )
        share_quadratic &= doubled == 4 * single
    return Row(
        "tab:results: The rules acts form no product of levels on the infinite lat",
        linear and within_one,
        share_quadratic,
        "the line is linear in its eight inputs exactly at 4 pairs and random paces; the integer step within one unit of it; the share, a reading, scales as the square",
    )
