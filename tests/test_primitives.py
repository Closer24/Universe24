"""The primitives: the tables are exact Pythagorean identities; the helicity is the sign of the spin against the momentum. HOST computations."""

from __future__ import annotations

from pathlib import Path

import pytest

from event_universe.events import primitives as P
from tests.laws import load_file

ROOT = Path(__file__).resolve().parents[1]
TWIST_FINE_COUNT = (
    1 << 10
)  # the shipped table's fine count, the test's own number (the loader takes the file's)

# a hand table: the angles are the host's, the identities exact; the fine table filled with (3, 4, 5) beyond its first entries so that its length is 2^10
FINE = ((1, 0, 1), (3, 4, 5), (5, 12, 13), (8, 15, 17)) + ((3, 4, 5),) * (TWIST_FINE_COUNT - 4)
COARSE = ((1, 0, 1), (7, 24, 25), (20, 21, 29))
TABLE = P.TwistTable(FINE, COARSE)


def test_the_identities_and_the_exact_product_of_rotations():
    assert P.is_triple((3, 4, 5)) and not P.is_triple((3, 4, 6)) and not P.is_triple((3, 4, -5))
    assert P.is_quadruple((1, 2, 2, 4, 5)) and not P.is_quadruple((1, 2, 2, 4, 6))
    TABLE.check()
    assert TABLE.bound == 3 * TWIST_FINE_COUNT - 1
    assert (
        TABLE.triple(0) == (1, 0, 1) and TABLE.triple(1) == (3, 4, 5) and TABLE.triple(-1) == (3, -4, 5)
    )
    # k = 2^10 + 2: the coarse (7, 24, 25) times the fine (5, 12, 13): the angles add, the norm 325
    composed = TABLE.triple(TWIST_FINE_COUNT + 2)
    assert composed == P.compose_triples((5, 12, 13), (7, 24, 25)) and P.is_triple(composed)
    assert composed[2] == 13 * 25
    with pytest.raises(ValueError, match="beyond the table's bound"):
        TABLE.triple(3 * TWIST_FINE_COUNT)
    with pytest.raises(ValueError, match="no Pythagorean triple"):
        P.TwistTable(((1, 0, 1), (3, 4, 6)) + FINE[2:], COARSE).check()
    with pytest.raises(ValueError, match="not the identity"):
        P.TwistTable(((3, 4, 5),) + FINE[1:], COARSE).check()
    assert P.link_angle(-1, 1, 3, 5, 7) == -36 and P.link_angle(1, -1, 3, 5, 7) == -36


def test_the_helicity_is_the_sign_of_the_spin_against_the_momentum():
    assert P.helicity((0, 0, 5), (0, 0, 3)) == 1 and P.helicity((0, 0, 5), (0, 0, -3)) == -1
    assert P.helicity((0, 0, 5), (3, 0, 0)) == 0  # the spin across the motion
    assert P.helicity((0, 0, 0), (3, 0, 0)) == 0 and P.helicity((0, 0, 5), (0, 0, 0)) == 0
    assert P.helicity_admits(0, (0, 0, 5), (0, 0, -3))
    admits = P.helicity_admits
    assert admits(-1, (0, 0, 5), (0, 0, -3)) and not admits(1, (0, 0, 5), (0, 0, -3))


def test_the_hosts_table_generator_writes_exact_triples_within_their_angles():
    tool = load_file("twist_table", ROOT / "tools/twist_table.py")
    table = tool.build(coarse=4)
    table.check()  # every identity exact (the module's check)
    largest = tool.check_angles(table)  # every angle within the representable floor (the host's check)
    assert table.fine[0] == (1, 0, 1) and table.coarse[0] == (1, 0, 1)
    assert max(t[2] for t in table.fine + table.coarse) <= tool.DENOMINATOR_BOUND
    assert table.bound == 4 * TWIST_FINE_COUNT - 1
    # the unit: 1 / (4 Gamma 2^16) radians per unit of k (ALGEBRA.md #the-primitives)
    assert tool.theta_unit() == 1.0 / (4 * 10_000 * 65536)
    # THE FINDING (the tool's docstring): the asked precision theta_unit / 2^10 cannot be met with d at most 10^9; every fine angle lies below the floor and its triple is the identity's
    assert 0 < largest <= tool.SMALLEST_ANGLE and all(triple == (1, 0, 1) for triple in table.fine)
    with pytest.raises(ValueError, match="misses its angle"):
        tool.check_angles(table, tolerance=tool.theta_unit() / TWIST_FINE_COUNT)
