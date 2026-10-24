"""The digits' lattice of the click's read (digits.lattice_of; ALGEBRA.md, The click's read of the board): F = gcd(w, D_i, R_ij) from Rule3's integers at a Node, three values for light at the exact vacuum paces and 2 num G^2 at a content, integers alone."""

from event_universe import digits
from event_universe.core import paces
from event_universe.core.rule3 import rule_integers, wall_of

GAMMA, UNIT = 6000, 16  # the shipped universes' Gamma and Link unit G
LIGHT, ATOM = wall_of(6000, GAMMA, UNIT), wall_of(1299, GAMMA, UNIT)  # the walls w = 6 den Gamma^2 G^2


def test_the_digits_lattice_at_the_exact_vacuum_is_three_valued():
    """The digits' lattice F = gcd(w, D_i, R_ij) (`digits.lattice_of`): at the exact vacuum paces, p_0 = p_i = Gamma with no tension, light's digits lie on w div 2 + (w div 3) Z, three values each (the read refused there), the massive pair [4000, 6000] on nine; at the shipped universes' content 60 (the paces 5940 and 5881) F = 3,072,000 = 2 num G^2 and a digit takes 108,000,000 values; the atom [1, 1299] at the exact vacuum 3,897."""
    at = [
        (0, 0, 0),
        (1, 0, 0),
    ]  # a Node and its neighbour beyond the Port +x, the Link's lattice from the neighbour's reach back
    light = rule_integers(6000, 6000, GAMMA, GAMMA, GAMMA, None, UNIT)
    found = digits.lattice_of(light, at, None, [0])
    assert found == [LIGHT // 3] * 2 and all(3 * f >= LIGHT for f in found)
    matter = rule_integers(4000, 6000, GAMMA, GAMMA, GAMMA, None, UNIT)
    assert digits.lattice_of(matter, at, None, [0]) == [LIGHT // 9] * 2
    atom = rule_integers(1, 1299, GAMMA, GAMMA, GAMMA, None, UNIT)
    assert [ATOM // f for f in digits.lattice_of(atom, at, None, [0])] == [3897] * 2
    clock, pace = paces.node_paces(GAMMA, 60)
    assert (clock, pace) == (5940, 5881)
    content = rule_integers(6000, 6000, GAMMA, clock, pace, None, UNIT)
    lattice = digits.lattice_of(content, at, None, [0])
    assert lattice == [3_072_000] * 2 and LIGHT // lattice[0] == 108_000_000
    assert lattice[0] == 2 * 6000 * UNIT * UNIT and all(3 * f < LIGHT for f in lattice)
