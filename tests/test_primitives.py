"""The primitives: the internal representation's tables are exact Pythagorean identities and the transport turns, composes and inverts exactly per Node; the clicks list balances every declared conserved integer or refuses; the helicity is the sign of the spin against the momentum. HOST computations."""

from __future__ import annotations

from pathlib import Path

import pytest

from event_universe.events import primitives as P
from tests.worlds import load_file

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


def test_a_plane_rotation_keeps_the_norm_before_the_division_and_inverts_exactly():
    levels, triple = (1000, -300), (3, 4, 5)
    exact_re, exact_im = 3 * 1000 - 4 * -300, 4 * 1000 + 3 * -300
    assert exact_re**2 + exact_im**2 == (1000**2 + 300**2) * 25  # the norm times d^2, exact
    for remainders in ((0, 0), (2, 4), (4, 1)):
        rotated, after = P.rotate_plane(levels, triple, remainders)
        assert all(0 <= rho < 5 for rho in after)
        assert rotated[0] * 5 + after[0] == exact_re + remainders[0]
        assert rotated[1] * 5 + after[1] == exact_im + remainders[1]
        back, before = P.rotate_plane_inverse(levels, triple, after)
        assert back == rotated and before == remainders  # ALGEBRA.md #the-transport
    # the quaternion's block, the same identities with four remainders
    quadruple = (1, 2, 2, 4, 5)
    block = (11, -7, 5, 3)
    for remainders in ((0, 0, 0, 0), (1, 2, 3, 4)):
        rotated, after = P.rotate_quaternion(block, quadruple, remainders)
        assert all(0 <= rho < 5 for rho in after)
        back, before = P.rotate_quaternion_inverse(block, quadruple, after)
        assert back == rotated and before == remainders
    # the unit quaternion keeps the norm times e^2 before the division
    a, b, c, d, e = quadruple
    w, x, y, z = block
    products = (
        a * w - b * x - c * y - d * z,
        a * x + b * w + c * z - d * y,
        a * y - b * z + c * w + d * x,
        a * z + b * y - c * x + d * w,
    )
    assert sum(p * p for p in products) == (w * w + x * x + y * y + z * z) * e * e


def test_the_transport_composes_the_generators_and_inverts_per_node():
    quadruples = P.QuadrupleTable(((1, 0, 0, 0, 1), (1, 2, 2, 4, 5), (2, 3, 6, 0, 7)))
    representation = P.InternalRepresentation(
        3,
        (
            P.PlaneGenerator(((0, 1), (2, 3), (4, 5)), TABLE),  # the common phase of the three pairs
            P.PlaneGenerator(((0, 2), (1, 3)), TABLE),  # a rotation between pairs 0 and 1
            P.QuaternionGenerator((2, 3, 4, 5), quadruples),  # pairs 1 and 2 as a quaternion
        ),
    )
    representation.check()
    assert representation.levels == 6 and representation.remainder_count == 6 + 4 + 4
    arrived = (120, -45, 300, 7, -88, 61)
    angles = (2, -1, 1)
    remainders = tuple(range(14))
    remainders = tuple(r % 5 for r in remainders)
    levels, after = representation.transport(arrived, angles, remainders)
    assert len(levels) == 6 and len(after) == 14 and all(0 <= rho < 13 for rho in after)
    back, before = representation.transport_inverse(arrived, angles, after)
    assert back == levels and before == remainders
    # the angle 0 with zero remainders is the identity
    identity, zeros = representation.transport(arrived, (0, 0, 0), (0,) * 14)
    assert identity == arrived and zeros == (0,) * 14
    with pytest.raises(ValueError, match="levels arrived"):
        representation.transport(arrived[:4], angles, remainders)
    with pytest.raises(ValueError, match="angles for"):
        representation.transport(arrived, angles[:2], remainders)
    with pytest.raises(ValueError, match="not distinct indices"):
        P.InternalRepresentation(2, (P.PlaneGenerator(((0, 0),), TABLE),)).check()
    with pytest.raises(ValueError, match="not distinct indices"):
        P.InternalRepresentation(1, (P.PlaneGenerator(((0, 2),), TABLE),)).check()


def test_the_loaders_hook_reads_the_internal_object_and_refuses_the_rest():
    obj = {
        "pairs": 2,
        "generators": [
            {"planes": [[0, 1], [2, 3]]},
            {"quaternion": [0, 1, 2, 3], "table": [[1, 0, 0, 0, 1], [1, 2, 2, 4, 5]]},
        ],
    }
    representation = P.internal(obj, TABLE)
    assert representation.pairs == 2 and len(representation.generators) == 2
    with pytest.raises(ValueError, match="pairs"):
        P.internal({"pairs": 0, "generators": []}, TABLE)
    with pytest.raises(ValueError, match='"planes", or "quaternion"'):
        P.internal({"pairs": 1, "generators": [{"twist": 1}]}, TABLE)
    with pytest.raises(ValueError, match="no Pythagorean quadruple"):
        P.internal(
            {
                "pairs": 2,
                "generators": [
                    {"quaternion": [0, 1, 2, 3], "table": [[1, 0, 0, 0, 1], [1, 1, 1, 1, 3]]}
                ],
            },
            TABLE,
        )


def test_the_clicks_list_balances_the_conserved_integers_or_refuses():
    obj = {
        "takes": {"family": "a", "labels": {"q": 0, "colour": 0}},
        "gives": [
            {"family": "b", "count": 1, "labels": {"q": -1, "colour": 0}},
            {"family": "c", "count": 1, "labels": {"q": 1, "colour": 0}},
        ],
        "helicity": -1,
    }
    clicks = P.clicks_list(obj)
    assert clicks.products == 2 and clicks.helicity == -1 and clicks.takes == "a"
    bad = dict(obj)
    bad["gives"] = [{"family": "b", "count": 2, "labels": {"q": -1}}]
    with pytest.raises(ValueError, match="'q' is 0 taken and -2 given"):
        P.clicks_list(bad)
    bad["gives"] = [{"family": "b", "count": 1, "labels": {"q": 0, "spin": 1}}]
    with pytest.raises(ValueError, match="names 'spin'"):
        P.clicks_list(bad)
    bad["gives"] = obj["gives"]
    bad["helicity"] = 2
    with pytest.raises(ValueError, match="helicity"):
        P.clicks_list(bad)
    with pytest.raises(ValueError, match="at least 1"):
        P.ClicksList("a", {}, (P.Giving("b", 0, {}),)).check()


@pytest.mark.parametrize("products", [1, 2, 3, 5])
@pytest.mark.parametrize("residue", [0, 1, 17, 63])
def test_the_momenta_are_shared_whole_with_the_sum_exact(products, residue):
    total = (100, -37, 0)
    shares = P.share_momenta(total, products, residue, 64)
    assert len(shares) == products
    assert tuple(sum(share[axis] for share in shares) for axis in range(3)) == total
    assert all(share[0] >= 0 and share[1] <= 0 and share[2] == 0 for share in shares)
    assert shares == P.share_momenta(total, products, residue, 64)  # the same residue, the same shares
    if products == 1:
        assert shares == (total,)


def test_the_share_refuses_a_residue_off_the_wheel_and_no_product():
    with pytest.raises(ValueError, match="not on the wheel"):
        P.share_momenta((1, 0, 0), 2, 64, 64)
    with pytest.raises(ValueError, match="at least one product"):
        P.share_momenta((1, 0, 0), 0, 0, 64)
    # two products: the one cut is the rung (residue + W / 2) mod W scaled to the whole
    assert P.share_momenta((10, 0, 0), 2, 0, 64) == ((5, 0, 0), (5, 0, 0))
    assert P.share_momenta((10, 0, 0), 2, 32, 64) == ((0, 0, 0), (10, 0, 0))
    assert P.share_momenta((10, 0, 0), 2, 16, 64) == ((7, 0, 0), (3, 0, 0))


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
