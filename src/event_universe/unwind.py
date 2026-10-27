"""The close's reads and writes at one Node: the exact take of the taken row's levels by the share's fall on the line the fall's sign chooses (`fall_of`; the take act at a list of ends is merger.takes, CR-S2), the one lay act (`lay`) and the take's move as the write's form (`move`, CR-S1), the lattice momentum a move books (`momentum_of`) and the refusal by name (`refused`)."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

import numpy as np

from event_universe.core import acts, rule3
from event_universe.core.rule3 import carries
from event_universe.core.spokes import AXES, SPOKE_SIDES, SPOKES, spoke_of, wrap
from event_universe.meshes import cross
from event_universe.trains import HAND, REGULATOR, Gear, Train, zeros

if TYPE_CHECKING:
    from event_universe.clock import Clock


def neighbour(node: Clock, at: tuple[int, ...], port: int) -> tuple[int, ...]:
    """The Node beyond the Port of the Node `at`, on the torus (fd2, U3): the one spelling of a neighbour's place, as `across` is the one read of a neighbour's array."""
    axis, side = SPOKE_SIDES[port]
    return tuple(wrap(at[a] + (side if a == axis else 0), node.cube) for a in range(AXES))


def window_clocks(node: Clock, at: tuple[int, ...]) -> list[tuple[int, ...]]:
    """The Node and its six neighbours in Port order."""
    return [at] + [neighbour(node, at, port) for port in range(SPOKES)]


def at_clock(x: Any, at: tuple[int, ...]) -> int:
    """A rule's integer at a Node (a walled row's reaches are the one integer 0)."""
    return int(np.asarray(x)[at]) if np.ndim(x) else int(x)


def fall_of(
    node: Clock, at: tuple[int, ...], walls: int, r: rule3.Gearing, row: Train, direction: int = 1
) -> tuple[int | None, int, int]:
    """The exact take at the Node in the carrier's unit (PM-S1) on the line the fall's sign chooses (CS4-S2, the owner's word of 2026-10-25 through the Boss: the taken record's line whose level now stands farthest from its before, the largest now^2 - before^2, the first line where equal, so the take is covariant under the record's quarter turn; the former first line kept by name): the taken line's now moved toward its before by the least count of levels at which the Node's share falls by the walls (0 where nothing is owed, EX-S1); the fall f(s) = s (price - X w s) over the share's weight 2 Gamma^3 G^2, the price X times Rule3's own numerator with the slots exchanged, -t (2 w now + pull); the count one carried division of the walls owed by the price, rounded up as the floor's mirror, and where the moved levels' own square leaves the fall short, the same division of the shortfall by the next level's price, price - 2 X w s, iterated from below to its fixed count (TC-S1, the owner's word of 2026-10-26, 08:3x UTC, "approved", both hands' one finding, H-Take-Count-As-Rule3-Division-1: the count Rule3's own kind of act, no root; the former least root by largest_below, least_root, kept by name); (None, the full fall) where no count within the full move pays, the division's fixed count passing the move or the next level's price falling to 0 before it; at -1 the exact take reversed, the merger's light (MG-S1; the former merger.rise_of kept by name, folded 2026-10-26 on the Boss's 6413888338): the line's now moved away from its before (the tie resolved as away at -1, cc1) by the least count at which the share rises by the walls, the rise the same quadratic with the direction's sign on the square term, s (price + X w s), convex, so the same division is iterated from above, the first quotient paying and each step the excess divided by the next level's price, to its fixed count, never refused (the former refusal read the fall at the full move alone, the parabola's far side, and refused a take a lesser count paid: the bug struck 2026-10-26 under the owner's priority, the Boss's 6411031946)."""
    gaps = [n * n - b * b for n, b in ((int(z.now[at]), int(z.before[at])) for z in row.gears)]
    k = gaps.index(max(gaps))
    line = row.gears[k]
    now, before = int(line.now[at]), int(line.before[at])
    if walls <= 0 and direction == 1:
        return 0, 0, k
    if now == before and direction == 1:
        return None, 0, k
    t = (1 if before > now else -1) if direction == 1 else (1 if now > before else -1)
    own, w, reached = int(np.asarray(r.hold)[at]), int(r.teeth), 0
    for port, reach in enumerate(r.grips):
        reached += int(np.asarray(reach)[at]) * int(line.before[neighbour(node, at, port)])
    pull = own * before + reached
    x, weight = int(node.start_stretch[at]), rule3.wind_weight(node.full_rate, node.G)

    def fall(s: int) -> int:
        moved = now + t * s
        return int(carries(direction * x * (w * (now * now - moved * moved) - t * s * pull), weight))

    price, dist = -t * direction * ((w + w) * now + pull) * x, abs(now - before)
    if direction == -1:
        s = (
            -carries(-walls * weight, price)
            if price > 0
            else -carries(price, x * w) - carries(-walls * weight, x * w)
        )
        while s > 1 and fall(s - 1) >= walls:
            s -= max(1, carries(s * (price + x * w * s) - walls * weight, price + x * w * (s + s)))
        return s, fall(s), k
    s = -carries(-walls * weight, price) if price > 0 else dist + 1
    while s <= dist and fall(s) < walls:
        slope = price - x * w * (s + s)
        s = s - carries(-(walls * weight - s * (price - x * w * s)), slope) if slope > 0 else dist + 1
    if s > dist:
        return None, fall(dist), k
    return s, fall(s), k


def advance(node: Clock, rec: int, where: Any, levels: Any, sign: int = 1) -> None:
    """The one lay act: a record's levels (now, before per line: re_now, re_before, im_now, im_before for a plane) added at the Node `where` (or over the board), taken back with sign -1 (the seed's forms, the children, a merger's ends taken whole and their undoing); the take's move on one line is `move` (CR-S1)."""
    lines = node.hands()[rec].gears
    for line_, now, before in zip(lines, levels[0::HAND], levels[1::HAND], strict=True):
        line_.now[where] = acts.advance(line_.now[where], now, sign)
        line_.before[where] = acts.advance(line_.before[where], before, sign)


def push_of(
    node: Clock, gears: list[Gear], at: tuple[int, ...], notches: Any, pinion: int, sign: int = 1
) -> list[int]:
    """The push a lay books at the clock `at`, the change of P_a = 2 pinion SUM_i (now_(i+a) . before_i - now_i . before_(i+a)), the dot over the hand's gears (Re conj(a) b of the Gaussian hand), when the gears' notches now and before move by the lay's `notches` (now, before per gear) times `sign`: 2 pinion SUM over the gears [d_now (before_(i-a) - before_(i+a)) + d_before (now_(i+a) - now_(i-a))] per axis; a one-gear lay is its gear with the before notch 0."""
    found = []
    for a in range(AXES):
        up, down = neighbour(node, at, spoke_of(a, 0)), neighbour(node, at, spoke_of(a, 1))
        dots = (
            cross(dn, db, int(g.now[down]) - int(g.now[up]), int(g.before[down]) - int(g.before[up]))
            for g, dn, db in zip(gears, notches[0::HAND], notches[1::HAND], strict=True)
        )
        found.append(sign * (pinion + pinion) * sum(dots))
    return found


def move(node: Clock, rec: int, k: int, at: tuple[int, ...], count: int) -> None:
    """The take's move, the Node's write act at one Node (CR-S1, the owner's word of 2026-10-26, 06:1x UTC): one carried division at the line's own wall of the exact numerator, the count times the wall, the quotient count laid on the line's level now by the one lay act and the remainder unmoved; the take forward, its lay-back and its undoing are this one act with the count's sign; not the interval's write act, whose wall is the line's write wall, which the taken line does not hold. The former take_at (one Node's take, EX-S1's remainder owed at it) is kept by name: its act is merger.takes."""
    lines = node.hands()[rec].gears
    wall = at_clock(lines[k].teeth, at)
    q, _unmoved = acts.carry(count * wall, wall, int(lines[k].fine[at]), 1)
    advance(node, rec, at, tuple(q if j == HAND * k else 0 for j in range(HAND * len(lines))))


def recoil(
    node: Clock, where: tuple[int, ...], dp: list[int], clock: int, direction: int
) -> dict[str, Any]:
    """The move's booking written on the Link's record the Node holds (LT-S1, the owner's word of 2026-10-26, 08:4x UTC, "approve"; H-Lay-As-The-Take-Reversed-1, the lay as the take reversed read on the Link's record): the momentum a move books at its Node (momentum_of, the change of the records' current on the Node's six Links) is written per axis on the carrier's flux line of that axis at that Node by the Node's one write act (one carried division at the line's write wall, the carry in its write remainder; Y-S3's line, whose source summed over the board is the records' momentum negated, so the line gains what the moved quantum lost, -dP, at the clock squared by the position of the reading, and the records' and the lattice's momentum sum to what they were: the Boss's correction of the sign under the delegation of 00:57, 2026-10-26, 10:18 UTC, the derivation's line 19 having carried the move's sign where the sentence means the book's), in the direction given, the same act at -1 undoing it from the log's numbers; so the momentum and the angular momentum at every click are an identity, -dP_a p_0^2 + wr_a - wr_a' = q_a K den Gamma^2 T. Returns the log's numbers: the clock, the levels laid per axis, the carry before and after."""
    lines = node.train(REGULATOR).gears[1 + AXES : 1 + AXES + AXES]
    was, laid = [int(line.dfine[where]) for line in lines], []
    for line, p in zip(lines, dp, strict=True):
        numerator = zeros(node.size)
        numerator[where] = -p * clock * clock
        level = int(line.now[where])
        node.drive(line, numerator, direction)
        laid.append(int(line.now[where]) - level)
    return {
        "clock": clock,
        "recoil": laid,
        "carry_was": was,
        "carry": [int(line.dfine[where]) for line in lines],
    }
