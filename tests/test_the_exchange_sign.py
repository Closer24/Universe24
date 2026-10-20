"""The family's sign under exchange (2026-10-19, the owner's word; ALGEBRA.md, Spin, closed for the paper as a route, The family's sign under exchange): a family of several parts may declare `exchange: antisymmetric` or `symmetric` in the universe file, a tri-state the loader reads into the family's row (`loader/universe.exchange_of`, `FamilyRule.exchange`, 0 undeclared) and the joint credit and the lists read, nothing at the Node: the first side's coefficients carry the determinant's lambdas for the antisymmetric record and the pattern's own integers for the symmetric and the undeclared (`meeting_back.coefficients_of`, `credit.terms_of`), the lists weigh an entry into a part by the sign's factor, 0 into a populated part for the antisymmetric record, n + 1 at a part holding n for the symmetric, 1 undeclared (`lists.exchange_factor`, beside `full`), and a family declaring the sign starts with its counts split over its parts, the one-part refusal kept for every other family (`loader/node_detector_declaration.parts_of`). The tests declare their own worlds through the helpers of tests/laws.py: the singlet under the sign with the identity pattern on both regions, equal to the crossed pattern's numbers by the determinant's identity at two parts; the symmetric control; the shell of two quanta at four parts with no capacity; the tri-state against the shipped worlds; the refusals by name."""

import json
from fractions import Fraction

from event_universe import lists
from event_universe.lattice import Lattice
from event_universe.loader.draw import patterns_of_the_law, ports_of
from event_universe.loader.node_detector_declaration import node_detector_of, parts_of
from event_universe.loader.universe import universe_of
from event_universe.world_files import load_world
from tests.laws import EVENTS, refused, world_beside
from tests.laws_spin import (
    BELL,
    IDENTITY,
    PORT,
    SINGLET,
    correlation,
    joint_shares,
    marginal_of,
    sided,
    spin_world,
    trial,
)

ANTISYMMETRIC, SYMMETRIC = "antisymmetric", "symmetric"  # the two words of the key `exchange`
SHELL = {
    "grounds": (("gu", 1), ("gd", 1)),
    "excited": ("eu", "ed"),
}  # the shell's four parts, one quantum in each ground part, the excited parts empty


def sign_singlet_read(tmp_path, monkeypatch, a, b) -> Fraction:  # type: ignore[no-untyped-def]
    """The singlet under the family's sign at one setting (the verdict's section 2, the determinant form): the spin world with `exchange: antisymmetric` on the family's row and the plain identity pattern on both regions; the joint credit's amplitude is SUM_{k != l} sign(l - k) e^L_k psi^L_k e^R_l psi^R_l, the determinant of the two sides' parts, and at two parts it is the symmetric form with the crossed pattern [[0, 1], [-1, 0]] on one side term by term (the crossed ports read e'_0 = e_1 and e'_1 = -e_0 at both ports, so the two terms are the determinant's two), the shares equal exactly; E(a, b) = -cos(theta_a - theta_b), both marginals 1 / 2, the engine's own weights at the draws (`sided`, the Gram read of the sides' own moments) equal to the reader's arithmetic with the sign's terms exactly. Returns the E read from the shares; two settings per test function, each under the suite's clock."""
    sides = {"left": (a, IDENTITY), "right": (b, IDENTITY)}
    path = spin_world(
        tmp_path / f"{a[0]}_{a[1]}_{b[0]}_{b[1]}",
        monkeypatch,
        sides,
        both=True,
        amplitude=64,
        exchange=ANTISYMMETRIC,
    )
    board, lines = trial(path, 40)
    assert board.families[[f.name for f in board.families].index("spin")].exchange == -1
    clicks = [c for c in lines if c["event"] == "credit"]
    assert [c["node_detector"] for c in clicks] == ["left", "right"], clicks
    assert all(c["count"] == 1 and c["left"] == 0 for c in clicks), clicks
    shares = joint_shares(lines, sides, -1)
    spin = [f.name for f in board.families].index("spin")
    sided(board, spin, shares, [PORT[c["realised"]] for c in clicks])  # the determinant's reads
    crossed = ports_of(b, tuple(tuple(p) for p in SINGLET))
    plain = ports_of(b, tuple(tuple(p) for p in IDENTITY))
    for port in range(2):  # the crossed pattern's ports are the determinant's signs on the parts
        assert tuple(crossed[port]) == (plain[port][1], (-plain[port][0][0], -plain[port][0][1]))
    assert shares == joint_shares(lines, {"left": (a, IDENTITY), "right": (b, SINGLET)}, 0)
    total = sum(shares.values())
    same, different = shares[0, 0] + shares[1, 1], shares[0, 1] + shares[1, 0]
    read = Fraction(same - different, total)
    assert read == correlation(a, b), (a, b, shares)
    assert Fraction(shares[0, 0] + shares[0, 1], total) == Fraction(1, 2)  # the left marginal
    assert Fraction(shares[0, 0] + shares[1, 0], total) == Fraction(1, 2)  # the right marginal
    assert shares[tuple(PORT[c["realised"]] for c in clicks)] > 0, clicks
    print(f"the sign's singlet: the axes {a} and {b} read E = {read}, the shares {shares}")
    return read


def test_the_singlet_under_the_familys_sign_at_a_b_and_a_b_prime_reads_the_crossed_patterns_numbers(
    tmp_path, monkeypatch
):
    """The first pair of Bell settings under the sign with the identity pattern on both sides: E = -119 / 169 at a, b and 119 / 169 at a, b', the crossed pattern's numbers."""
    a, _a2, b, b2 = BELL
    assert [sign_singlet_read(tmp_path, monkeypatch, a, x) for x in (b, b2)] == [
        Fraction(-119, 169),
        Fraction(119, 169),
    ]


def test_the_singlet_under_the_familys_sign_at_a_prime_b_and_a_prime_b_prime_breaks_the_bound(
    tmp_path, monkeypatch
):
    """The second pair of Bell settings under the sign: E = -120 / 169 at a', b and at a', b'; with the first pair's fractions (the law's correlation(a, b) and correlation(a, b'), read by the test above) |S| = |E(a, b) - E(a, b') + E(a', b) + E(a', b')| = 478 / 169, above 2."""
    a, a2, b, b2 = BELL
    found = {
        (a, b): correlation(a, b),
        (a, b2): correlation(a, b2),
    }  # the law's, read by the first pair's test
    found[a2, b] = sign_singlet_read(tmp_path, monkeypatch, a2, b)
    found[a2, b2] = sign_singlet_read(tmp_path, monkeypatch, a2, b2)
    assert [found[a2, b], found[a2, b2]] == [Fraction(-120, 169), Fraction(-120, 169)]
    assert abs(found[a, b] - found[a, b2] + found[a2, b] + found[a2, b2]) == Fraction(478, 169)


def test_the_singlet_under_the_familys_sign_at_equal_axes_realises_opposite_ports(tmp_path, monkeypatch):
    """At equal axes under the sign the shares of (+, +) and (-, -) are 0 exactly, the first side's weights the marginal's, and the realised pair opposite in the one read."""
    sides = {"left": ((3, 1), IDENTITY), "right": ((3, 1), IDENTITY)}
    path = spin_world(
        tmp_path / "equal", monkeypatch, sides, both=True, amplitude=64, exchange=ANTISYMMETRIC
    )
    board, lines = trial(path, 40)  # one world, one read of the board at the close
    shares = joint_shares(lines, sides, -1)
    spin, first = [f.name for f in board.families].index("spin"), board.credit.weights
    assert (
        first[(spin, "left")][0] * marginal_of(shares, 0)[1]
        == first[(spin, "left")][1] * marginal_of(shares, 0)[0]
    )
    assert shares[0, 0] == shares[1, 1] == 0 and shares[0, 1] == shares[1, 0] > 0, shares
    pair = tuple(PORT[c["realised"]] for c in lines if c["event"] == "credit")
    assert pair in {(0, 1), (1, 0)}, pair  # opposite ports at equal axes
    print(f"the sign's singlet at equal axes: the realised pair {pair}")


def test_the_symmetric_control_credits_the_same_port_at_equal_axes(tmp_path, monkeypatch):
    """The control: the same world with `exchange: symmetric`, the credit's form the one that stood (SUM_k over the same part at every side, the parts laid alike), so at equal axes the shares of (+, -) and (-, +) are 0 exactly and the realised pair is the same port over three seeds; the symmetric record's shares equal the undeclared reading of the same lines bit for bit (the tri-state's two readings of one form)."""
    sides = {"left": ((3, 1), IDENTITY), "right": ((3, 1), IDENTITY)}
    path = spin_world(
        tmp_path / "control", monkeypatch, sides, both=True, amplitude=64, exchange=SYMMETRIC
    )
    board, lines = trial(path, 40)  # one world, one read of the board at the close
    assert board.families[[f.name for f in board.families].index("spin")].exchange == 1
    shares = joint_shares(lines, sides, 1)
    assert shares == joint_shares(lines, sides, 0)
    spin, first = [f.name for f in board.families].index("spin"), board.credit.weights
    assert (
        first[(spin, "left")][0] * marginal_of(shares, 0)[1]
        == first[(spin, "left")][1] * marginal_of(shares, 0)[0]
    )
    assert shares[0, 1] == shares[1, 0] == 0 and shares[0, 0] == shares[1, 1] > 0, shares
    pair = tuple(PORT[c["realised"]] for c in lines if c["event"] == "credit")
    assert pair in {(0, 0), (1, 1)}, pair
    print(f"the symmetric control at equal axes: the realised pair {pair}")


def test_a_family_without_the_key_loads_and_steps_as_before(tmp_path, monkeypatch):
    """The tri-state: every family of the shipped universes carries the exchange 0, the lists' factor is 1 at every part of the shipped one-photon world's bodies (its lists and credit as they stand, the digest of its output the oracle's, tests/test_part_g_recoil.py), the one-part refusal stands for a family declaring no sign (`parts_of` without `split`) and the split start is admitted with it; the loader reads the key as any family key, refusing an unknown one beside it."""
    for universe in ("rule.json", "pair.json", "anticoincidence/two_atoms.json", "charged.json"):
        families = universe_of(json.loads((EVENTS / universe).read_text(encoding="utf-8")))[1]
        assert all(family.exchange == 0 for family in families), universe
    born = world_beside(
        tmp_path, EVENTS / "bell_singlet" / "born_a_b.json", lambda w: None
    )  # re-pinned 2026-10-20
    board = Lattice(load_world(born), lambda line: None)
    assert board.credit.bodies, "the born world declares its body"
    for books in board.credit.bodies:
        assert [lists.exchange_factor(board, books, part) for part in range(len(books.counts))] == [
            1
        ] * len(books.counts)
    rows = [
        {"part": k, "name": n, "count": c} for k, (n, c) in enumerate((("g", 1), ("e", 1), ("f", 0)))
    ]
    refused("stands in one part", parts_of, rows, "bodies[0].parts", 3, 2)
    assert parts_of(rows, "bodies[0].parts", 3, 2, True) == (
        ("g", "e", "f"),
        (1, 1, 0),
        (None, None, None),
    )


def test_the_refusals_by_name(tmp_path, monkeypatch):
    """The refusals: `exchange` on a family of one part (no second label to exchange), a value other than the two words, `exchange` beside a detector's `capacity` on the same family (one word for one thing), and the antisymmetric sign read by three sides or by one, at load (the determinant of two sides' parts, another count of sides a declaration the law has not made; the owner's word of 2026-10-19, N sides the general case otherwise)."""
    universe = json.loads((EVENTS / "anticoincidence" / "two_atoms.json").read_text(encoding="utf-8"))
    atom = universe["families"][0]
    refused(
        "one part",
        universe_of,
        {
            **universe,
            "families": [{**atom, "dimension": 2, "exchange": ANTISYMMETRIC}, *universe["families"][1:]],
        },
    )
    atom["dimension"] = [4, 2]
    refused(
        "is one of",
        universe_of,
        {**universe, "families": [{**atom, "exchange": "fermion"}, *universe["families"][1:]]},
    )
    refused(
        "is one of",
        universe_of,
        {**universe, "families": [{**atom, "exchange": -1}, *universe["families"][1:]]},
    )
    atom["exchange"] = ANTISYMMETRIC
    families = universe_of(universe)[1]
    quanta = {f.name: i for i, f in enumerate(families) if f.quanta}
    parts = [
        {"part": k, "name": n, "count": 1 if k < 2 else 0}
        for k, n in enumerate(("gu", "gd", "eu", "ed"))
    ]
    body = {"family": "atom", "parts": parts}
    node_detector_of(body, "bodies[0]", families, 0, quanta, 2)  # the split start admitted
    parts[2]["capacity"] = 1
    refused("one word for one thing", node_detector_of, body, "bodies[0]", families, 0, quanta, 2)
    sides = {"left": ((1, 0), IDENTITY), "right": ((12, 5), IDENTITY)}
    board = Lattice(
        load_world(
            spin_world(tmp_path, monkeypatch, sides, both=True, amplitude=64, exchange=ANTISYMMETRIC)
        ),
        None,
    )
    spin = [f.name for f in board.families].index("spin")
    pattern = tuple(tuple(pair) for pair in IDENTITY)
    three = [("left", pattern), ("right", pattern), ("third", pattern)]
    refused(
        "3 side", patterns_of_the_law, three, [spin], board.families
    )  # at load, the determinant two sides'
    refused("1 side", patterns_of_the_law, three[:1], [spin], board.families)
    patterns_of_the_law(three[:2], [spin], board.families)  # two sides admitted
    patterns_of_the_law([], [spin], board.families)  # read at no side: the shell's own world loads
