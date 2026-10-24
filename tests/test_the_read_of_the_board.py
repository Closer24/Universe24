"""The click's read of the board (ALGEBRA.md, The click's read of the board; the owner's words: the board is deterministic and the click is the only instrument that reads it, the new draw built from the remainders and Rule3 only): the digits' number and the one division act per draw (`features/click.read_number`, `drawn_from`), the residue's and the quotient's independence, the digits' lattice at the exact vacuum paces and at the shipped content, the loader's refusal of a generator's keys and the read's refusals by name (`digits.read_of`), and the read at work on three shipped worlds re-declared beside tmp_path (`tests.laws.world_beside`): the singlet's two sides (the first side blind to the later side's basis bit for bit, the read writing nothing), the one photon's two bodies (the arriving record's digits and the body's own in the mixed radix of their walls) and the two slits' many-draw close (the digits spent by name at the shipped window, the close run at a shorter one)."""

import random
from collections import Counter

import numpy as np
import pytest

from event_universe import digits, node, node_detector
from event_universe.core import paces
from event_universe.core.rule3 import rule_integers, wall_of
from event_universe.features.click import bias_bound, drawn_from, read_number
from event_universe.features.front import ball
from event_universe.lattice import Lattice
from event_universe.loader.draw import DIGIT_ORDER
from tests.laws import family

GAMMA, UNIT = 6000, 16  # the shipped universes' Gamma and Link unit G
LIGHT, ATOM = wall_of(6000, GAMMA, UNIT), wall_of(1299, GAMMA, UNIT)  # the walls w = 6 den Gamma^2 G^2


def placed(residue: int, weights: list[int]) -> int:
    """The residue placed on the cumulative weights, the first index whose cumulative weight exceeds it."""
    return next(i for i in range(len(weights)) if residue < sum(weights[: i + 1]))


def body_reads(board: Lattice, families: list[int], at: np.ndarray) -> list[tuple[int, np.ndarray]]:
    """What a body reads by the test's own arithmetic (the reader's G2): each family at the body's Nodes `at` and at the Nodes within one Link of them (the ball of radius 1, `features/front.ball`) where a line of its record holds a remainder other than w // 2."""
    centres = [tuple(int(k) for k in where) for where in np.argwhere(at)]
    near = ball(board.shape, centres, 1, board.world.periodic)
    found = []
    for index in families:
        off = np.zeros(board.shape, dtype=bool)
        for line in board.lines_of(index, 0):
            off |= np.asarray(line.remainder) != board.half_wall(index)
        found.append((index, at | (near & off)))
    return found


def digits_now(
    board: Lattice, reads: list[tuple[int, np.ndarray]], distinct: bool = True
) -> tuple[list[int], list[int]]:
    """The digits and their bases by the test's own arithmetic of the declared order: the families in their order, each at its own Nodes (`reads`, a side's region or a body's `body_reads`), every line of each family's record in the declared order, each line's remainder at the Nodes in the lattice's index order (`np.argwhere`), the digit the remainder's index on the Node's lattice, r // F (`digits.lattice_of` on the rule's integers there), its base w // F + 1; with `distinct` a remainder equal to an earlier line's at the same Node, or w less it, is a copy and left out (the reader's D2), without it every line's digit."""
    found, bases = [], []
    for index, at in reads:
        family, gamma = board.families[index], board.world.node_clock
        wall = wall_of(family.pair[1], gamma, board.unit)
        lattice = digits.lattice_of(
            node.rule_of(family, gamma, *board.read(index, 1, 0), board.unit), at
        )
        earlier: dict[int, list[int]] = {}  # per Node, the earlier lines' remainders
        for line in board.lines_of(index, 0):
            for k, (where, step) in enumerate(zip(np.argwhere(at), lattice, strict=True)):
                remainder, seen = int(line.remainder[tuple(where)]), earlier.setdefault(k, [])
                copied = distinct and any(remainder in (e, wall - e) for e in seen)
                seen.append(remainder)
                if not copied:
                    found.append(remainder // step)
                    bases.append(wall // step + 1)
    return found, bases


def spied(monkeypatch, board_of, distinct=True):  # type: ignore[no-untyped-def]
    """Every draw of the run recorded as the engine makes it (`node_detector.drawn_from` spied): the label, the number read or left, the weights, the pick, the number left after, and the test's own digits of the records the label names at the Nodes it names, read from the board at that moment (each Node's distinct digits, or with `distinct` False every line's)."""
    seen: list[dict] = []  # type: ignore[type-arg]
    real = node_detector.drawn_from

    def spy(number, weights, label, *moduli):  # type: ignore[no-untyped-def]
        board = board_of()
        words = label.split("'")
        if label.startswith("the side "):
            name = words[1]
            reads = [
                (family(board, words[3]), next(d.nodes for d in board.node_detectors if d.name == name))
            ]
        elif label.startswith("the regions "):
            reads = [(family(board, words[1]), node_detector.node_detector_nodes(board))]
        else:
            books = board.credit.bodies[int(label.split()[2])]
            drives = list(dict.fromkeys(t.drive for t in books.declared.transitions))
            reads = body_reads(board, [*drives, books.index], board.mask(books.nodes))
        own, walls = digits_now(board, reads, distinct)
        pick, left = real(number, weights, label, *moduli)
        drawn = dict(label=label, number=number, weights=list(weights), pick=pick, left=left)
        seen.append(dict(drawn, digits=own, walls=walls))
        return pick, left

    monkeypatch.setattr(node_detector, "drawn_from", spy)
    return seen


def test_the_read_is_the_digits_number_and_each_draw_one_division_act():
    """The number is the digits in base w, the first the most significant (`read_number`, multiply and add, equal to the plain sum and to Horner's form with the base reduced); each draw one division act by the weights' total (`drawn_from`): the quotient the number left, the remainder placed on the cumulative weights (the lower index on a tie, a weight of 0 never drawn); the mixed radix of two walls; one weight above 0 is a certain draw and consumes nothing (a weight of 0 never drawn); a total at or below 0 and a number below the total refused by name in the two texts (the number left, a quotient's draw; the number read, the interval's first), the texts apart from the write's bound refusal."""
    chance = random.Random(24)  # the test's own vectors; the engine draws by nothing of the kind
    for _ in range(60):
        count = chance.randint(1, 12)
        found = [chance.randrange(LIGHT) for _ in range(count)]
        x = read_number(found, [LIGHT] * count)
        assert x == sum(d * LIGHT ** (count - 1 - i) for i, d in enumerate(found))
        weights = [chance.randint(0, 10**9) for _ in range(chance.randint(2, 6))]
        weights[0] = max(weights[0], 1)
        total = sum(weights)
        pick, left = drawn_from(x, weights, "the test")
        residue = x % total
        assert (pick, left) == (placed(residue, weights), x // total) and weights[pick] > 0
        horner = 0
        for d in found:
            horner = (horner * (LIGHT % total) + d) % total
        assert horner == residue
    assert read_number([5, 7], [LIGHT, ATOM]) == 5 * ATOM + 7  # the mixed radix: each digit its own base
    assert drawn_from(12345, [9], "the test") == (0, 12345)  # one weight consumes nothing
    assert drawn_from(12345, [0, 3, 0], "the test") == (1, 12345)  # one weight above 0: certain, whole
    assert drawn_from(12345, [0, 3, 4], "the test") == (placed(12345 % 7, [0, 3, 4]), 12345 // 7)
    with pytest.raises(ValueError, match="weights whose total is above 0"):
        drawn_from(12345, [0, 0], "the test")
    with pytest.raises(
        RuntimeError, match="at the test has the number 5 left, below the draw's total 7"
    ):
        drawn_from(5, [3, 4], "the test")
    spent = str(pytest.raises(RuntimeError, drawn_from, 5, [3, 4], "the test").value)
    assert spent.startswith("the click's read of the board") and "amplitude bound" not in spent
    with pytest.raises(RuntimeError, match="has the number 5 read, below the draw's total 7"):
        drawn_from(5, [3, 4], "the test", (1, 2))  # the interval's read itself below the total


def test_the_residue_and_the_quotient_of_one_number_are_independent():
    """Two draws of one close are one division act each on the number left: over a full period of T1 T2 the pairs (the first pick's residue, the second's) are each hit alike (60 pairs of 60 at T1 = 6 and T2 = 10, 7 times each over 7 periods), where the same residue read twice would lock the picks (30 pairs of 60 at gcd 2: the refused form, the test's own arithmetic)."""
    first, second = [2, 4], [7, 3]  # T1 = 6, T2 = 10
    counts: Counter[tuple[int, int]] = Counter()
    base = 7 * 60  # above both totals at every draw: the number left stays above T2
    for x in range(base, base + 7 * 60):
        pick, left = drawn_from(x, first, "the test")
        again, _rest = drawn_from(left, second, "the test")
        counts[(x % 6, left % 10)] += 1
        assert (pick, again) == (placed(x % 6, first), placed(left % 10, second))
    assert len(counts) == 60 and set(counts.values()) == {7}
    assert len({(x % 6, x % 10) for x in range(60)}) == 30  # the same residue twice: locked pairs


def test_a_total_sharing_a_factor_with_the_bases_books_its_bias_bound_and_is_refused_only_as_the_whole_total():
    """The reader's F of 2026-10-20 (`bias_bound`, `drawn_from` with the read's moduli, `digits.read_of`; CHANGED the same day from D's refusal where the product of the two gcds reached the smallest weight, a model's worst case taken for a measure): at the shipped content the base is B = w div F + 1 = 108,000,001 = 31 x 1069 x 3259 and B - 1 = 108,000,000 = 2^8 3^3 5^6, so the residue modulo a factor of B - 1 is the distinct digits' sum and modulo a factor of B the last digit alone, and g / T, g the product of the two gcds, bounds a port's move where the digits cycle: the bound is booked, [g_sum, g_last, T], and the one draw refused is g = T with two weights above 0, the digits' sum modulo the total alone (the conversion's total 30 at the weight 1, and the base's prime 31 at the weight 1), named so; the screens' class (the total 66,120,000 at the smallest weight 24,000, g = 120,000), a small factor (194 = 2 x 97), a total coprime to both (97) are drawn as before, the residue placed on the weights, and a certain draw (one weight above 0, g = T = 5) consumes nothing; the quotient's draws carry no moduli."""
    moduli, number = (108_000_000, 108_000_001), 10**30 + 12345
    assert bias_bound(66_120_000, moduli) == [
        120_000,
        1,
        66_120_000,
    ]  # the two slits' bound 0.18 percent
    assert bias_bound(30, moduli) == [30, 1, 30] and bias_bound(31, moduli) == [1, 31, 31]
    for weights in ([1, 29], [1, 30]):
        with pytest.raises(RuntimeError, match="the draw is the digits' sum modulo the total alone"):
            drawn_from(number, weights, "the test", moduli)
        total = sum(weights)
        assert drawn_from(number, weights, "the test") == (
            placed(number % total, weights),
            number // total,
        )
    for weights in ([24_000, 66_096_000], [97, 97], [48, 49]):
        total = sum(weights)
        found = drawn_from(number, weights, "the test", moduli)
        assert found == (placed(number % total, weights), number // total)
    for weights in ([5, 0], [1, 0]):  # a certain draw: nothing read, nothing consumed, g = T no refusal
        assert drawn_from(number, weights, "the test", moduli) == (0, number)


def test_the_digits_lattice_at_the_exact_vacuum_is_three_valued():
    """The digits' lattice F = gcd(w, D_i, R_ij) (`digits.lattice_of`): at the exact vacuum paces, p_0 = p_i = Gamma with no tension, light's digits lie on w div 2 + (w div 3) Z, three values each (the read refused there), the massive pair [4000, 6000] on nine; at the shipped universes' content 60 (the paces 5940 and 5881) F = 3,072,000 = 2 num G^2 and a digit takes 108,000,000 values; the atom [1, 1299] at the exact vacuum 3,897."""
    at = np.ones((2, 1, 1), dtype=bool)
    light = rule_integers(6000, 6000, GAMMA, GAMMA, GAMMA, None, UNIT)
    found = digits.lattice_of(light, at)
    assert found == [LIGHT // 3] * 2 and all(3 * f >= LIGHT for f in found)
    matter = rule_integers(4000, 6000, GAMMA, GAMMA, GAMMA, None, UNIT)
    assert digits.lattice_of(matter, at) == [LIGHT // 9] * 2
    atom = rule_integers(1, 1299, GAMMA, GAMMA, GAMMA, None, UNIT)
    assert [ATOM // f for f in digits.lattice_of(atom, at)] == [3897] * 2
    clock, pace = paces.node_paces(GAMMA, 60)
    assert (clock, pace) == (5940, 5881)
    content = rule_integers(6000, 6000, GAMMA, clock, pace, None, UNIT)
    lattice = digits.lattice_of(content, at)
    assert lattice == [3_072_000] * 2 and LIGHT // lattice[0] == 108_000_000
    assert lattice[0] == 2 * 6000 * UNIT * UNIT and all(3 * f < LIGHT for f in lattice)
    assert (
        "most significant" in DIGIT_ORDER and "index order" in DIGIT_ORDER and "r div F" in DIGIT_ORDER
    )
