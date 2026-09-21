"""The momentum label along the unit vector of the direction at the flight
table's scale (docs/BEAM_LAW.md, section 2 and section 10, note 23; the
model owner's decision of 2026-09-19 on the physics-rule reviewer's
verdict, Highlights 5.4): the label of one unit of a ray on the direction
D is u_d, the integer vector nearest Q D / |D| with Q = 64, computed once
in the world's direction table by the exact integer rule k(|a|) =
(isqrt((2 Q |a|)^2 // |D|^2) + 1) // 2 with the sign restored
(`nature_beam.unit_label`, the flight table's `labels`); the label of a
row is content x amount x u_d (a paid family) or amount x u_d (a free one),
so every direction's momentum per unit has one length within
sqrt 3 / (2 Q) = 1.35 % and a heading's is exactly Q e_d. The expected
integers of docs/TEST_EXPECTATIONS.md ("The label along the unit
vector"), written down first:

(a) the table: u_(1, 1, 0) = (45, 45, 0), u_(1, 1, 1) = (37, 37, 37),
    u_(2, 1, 0) = (57, 29, 0), u_(3, 1, 0) = (61, 20, 0), u_(7, 5, 0) =
    (52, 37, 0), u_(11, 1, 0) = (64, 6, 0), u_(1, 2, 3) = (17, 34, 51),
    u_(63, 46, 46) = (45, 33, 33); the six headings exactly 64 e_d; the
    rest vectors (0, 0, 0); 63^2 < |u_d|^2 < 65^2 for every direction of
    the table; u_{-D} = -u_D exactly; u_{gD} = g u_D for the 48 signed
    axis permutations; no exact tie (a half-integer Q |a| / |D| needs |D|
    a multiple of 256, beyond any direction bound below 147): over every
    primitive direction with components in -64 .. 64 the integer rule
    equals the float rounding (0 mismatches over 1780418), no component
    passes Q, no tie occurs, and |u_d| is within 1.35 % of Q;
(b) the labels on the GameBoard: a world of the six headings and the eight
    fan directions above with their negatives; a lamp of `light` (quantum
    1, content 3 x 2^18 at K 2^18: the turn 3 at every age of the run but
    tick 2, where the exact clock turns 2, the lamp paying 42 per birth
    (the fraction-free law of 2026-09-20; 3 at every tick until then),
    content c = 3 per unit) releasing one unit per interval on the six
    headings and the eight fan directions (14 rows per release, amount 1,
    content 3): every row's label 3 x u_d (`NatureBeamStore.labels`), |label|^2
    within (63 x 3)^2 .. (65 x 3)^2; the lamp's recoil after the first
    release exactly -(the labels born) = -3 x (378, 241, 121) = (-1134,
    -723, -363) (the six headings cancel), the transit line their sum;
    through 60 intervals with a screen at (21, 15, 15) measuring `light`
    (each click moves the ray's label 3 x u_d onto the screen: the +X rays
    give (192, 0, 0), the (11, 1, 0) rays (192, 18, 0)), a
    mirror at (22, 20, 15) on the line of (7, 5, 0) re-emitting on
    (-7, -5, 0) (its recoil exactly 2 x 3 x (52, 37, 0) = (312, 222, 0)
    per ray reflected, the label out being minus the label in) and the
    open faces (the escaped line the sum of the face clicks' momenta):
    measured + transit + escaped = (0, 0, 0) at every interval, the books
    balanced, the transit line equal to the recount;
(c) the bound: a declared ray of `light` (quantum 1) of amount 2^56 is
    refused by the parser naming 64 x 1 x 2^56 and the bound; amount
    2^56 - 1 is accepted; a free family's declared ray of amount 2^56 is
    refused and 2^56 - 1 accepted likewise; `momentum_labels` checks the
    product BEFORE it is formed, per row, the weight times the largest
    component of the row's unit vector (re-pinned on 2026-09-20, the
    architect's B1): a paid row of content 2^28 and amount 2^28 on a
    heading (64 e_d) is refused naming the amount, the Node and the
    product 2^56 x 64 = 2^62, and a free row of amount 2^56 likewise; the
    same rows on (1, 1, 0), u = (45, 45, 0), are accepted with the label
    2^56 x (45, 45, 0) (45 x 2^56 fits); `label_weights` refuses a row
    whose content x amount cannot be formed (content 2^31, amount 2^32)
    naming the amount and accepts 2^56 - 1 (the paid row of content
    2^28 - 1 and amount 2^28 + 1) and the free row of 2^56 - 1;
(d) the wrap that passed (the architect's B1, 2026-09-20; the probe: a
    row of 2^58 on (64, 1, 0) read a label of 0 for 2^64 with the books
    balanced): two declared rays of `light` of amount 2^55 at one Node on
    (1, 1, 0) merge at construction into one row of 2^56 and are
    accepted, the transit line 2^56 x (45, 45, 0) counted and running
    alike, the books balanced through three intervals; the same two rays
    on (1, 0, 0) are refused at construction (the recount forms the
    label) naming the Node [2, 2, 2], the amount 2^56 and the product
    2^56 x 64 = 2^62; a mirror of `wall` at (5, 5, 0) re-emitting on
    (64, 1, 0) what two rays of `light` (quantum 2^25: content 2^25 per
    unit) of amount 2^30 and of two other numbers bring it in one
    interval (from (4, 5, 0) on +X and from (5, 4, 0) on +Y; each group's
    label 2^55 x 64 = 2^61 within the reading's bound) is born as two
    rows of amount 2^30 (the weight 2^55, within the bound at its
    birth), merged into one row of amount 2^31 and weight 2^56 by the
    interval's merge, and the next label formed of that row (the
    recount) is refused naming the mirror's Node [5, 5, 0], the amount
    2^31, the content 2^25 and the product 2^56 x 64 = 2^62: no product
    of the law wraps, every refusal names the Node.
"""

from __future__ import annotations

import itertools

import numpy as np
import pytest

from event_universe.core.game_board import PORT_HEADINGS
from event_universe.events import NatureBeamSimulation, parse_nature_beam_world
from event_universe.events.nature_beam import (
    Q,
    direction_flight,
    label_weights,
    momentum_labels,
    unit_label,
)
from event_universe.events.world import LABEL_SCALE, MOMENTUM_BOUND

LIGHT, M = 0, 1
FAN = [(1, 1, 0), (1, 1, 1), (2, 1, 0), (3, 1, 0), (7, 5, 0), (11, 1, 0), (1, 2, 3), (63, 46, 46)]
PINNED = {
    (1, 1, 0): (45, 45, 0),
    (1, 1, 1): (37, 37, 37),
    (2, 1, 0): (57, 29, 0),
    (3, 1, 0): (61, 20, 0),
    (7, 5, 0): (52, 37, 0),
    (11, 1, 0): (64, 6, 0),
    (1, 2, 3): (17, 34, 51),
    (63, 46, 46): (45, 33, 33),
}
NEGATIVES = [tuple(-c for c in d) for d in FAN]
CONTENT = 3
CLOCK = 1 << 18
CENTRE = [15, 15, 15]
TICKS = 60


def cube_group() -> list[np.ndarray]:
    """The 48 signed axis permutations as integer matrices."""
    matrices = []
    for perm in itertools.permutations(range(3)):
        for signs in itertools.product((1, -1), repeat=3):
            matrix = np.zeros((3, 3), dtype=np.int64)
            for axis in range(3):
                matrix[perm[axis], axis] = signs[axis]
            matrices.append(matrix)
    return matrices


def test_the_table_is_the_nearest_integer_vector_at_the_scale_q_without_ties():
    """(a)."""
    assert Q == LABEL_SCALE == 64
    for direction, expected in PINNED.items():
        assert unit_label(direction) == expected, direction
    for port, heading in enumerate(PORT_HEADINGS):
        assert unit_label(heading) == tuple(64 * c for c in heading), port
    assert unit_label((0, 0, 0)) == (0, 0, 0)
    table = direction_flight(((0, 0, 0), (0, 0, 0), *PORT_HEADINGS, *FAN, *NEGATIVES))
    assert table.labels[:2].tolist() == [[0, 0, 0], [0, 0, 0]]
    for row, direction in zip(table.labels[2:], (*PORT_HEADINGS, *FAN, *NEGATIVES), strict=True):
        assert row.tolist() == list(unit_label(direction)), direction
        assert 63 * 63 < int(row @ row) < 65 * 65, direction
    group = cube_group()
    assert len({matrix.tobytes() for matrix in group}) == 48
    for direction in (*PORT_HEADINGS, *FAN):
        u = np.array(unit_label(direction), dtype=np.int64)
        assert unit_label(tuple(-c for c in direction)) == tuple((-u).tolist())
        for matrix in group:
            turned = tuple((matrix @ np.array(direction, dtype=np.int64)).tolist())
            assert unit_label(turned) == tuple((matrix @ u).tolist()), (direction, turned)
    # Every primitive direction with components in -64 .. 64, at once: the
    # integer rule against the float rounding, no component beyond Q, no
    # exact tie, and the length within sqrt 3 / (2 Q) of Q.
    span = np.arange(-64, 65, dtype=np.int64)
    a, b, c = (axis.reshape(-1) for axis in np.meshgrid(span, span, span, indexing="ij"))
    vectors = np.stack([a, b, c], axis=1)
    n = (vectors * vectors).sum(axis=1)
    primitive = (n > 0) & (np.gcd(np.gcd(np.abs(a), np.abs(b)), np.abs(c)) == 1)
    vectors, n = vectors[primitive], n[primitive]
    assert vectors.shape[0] == 1780418
    magnitude = np.abs(vectors)
    squares = (2 * Q * magnitude) ** 2 // n[:, None]
    roots = np.floor(np.sqrt(squares.astype(np.float64))).astype(np.int64)
    roots -= roots * roots > squares
    roots += (roots + 1) * (roots + 1) <= squares
    assert ((roots * roots <= squares) & ((roots + 1) * (roots + 1) > squares)).all()
    k = (roots + 1) // 2
    rounded = np.floor(Q * magnitude / np.sqrt(n.astype(np.float64))[:, None] + 0.5).astype(np.int64)
    assert (k == rounded).all()
    assert int(k.max()) == Q
    lengths = np.sqrt((k * k).sum(axis=1).astype(np.float64))
    assert float(np.abs(lengths - Q).max()) / Q < np.sqrt(3) / (2 * Q)
    # A tie: 2 Q |a| / |D| = m + 1/2 exactly, that is (2 m + 1)^2 n = (4 Q |a|)^2.
    ties = 4 * Q * magnitude
    tie_roots = np.floor(np.sqrt((ties * ties // n[:, None]).astype(np.float64))).astype(np.int64)
    for delta in (-1, 0, 1):
        candidate = tie_roots + delta
        assert not ((candidate % 2 == 1) & (candidate * candidate * n[:, None] == ties * ties)).any()


def world(measured: list[dict[str, object]], **keys: object) -> dict[str, object]:
    base: dict[str, object] = {
        "law": "beam",
        "model_id": "ray-label-test",
        "shape": [31, 31, 31],
        "boundary": "open",
        "ticks": TICKS,
        "K": CLOCK,
        "N": 64,
        "release": [0, 1],
        "suspension": 0,
        "directions": [list(d) for d in (*FAN, *NEGATIVES)],
        "families": [{"name": "light", "quantum": 1}, {"name": "m", "quantum": 0}],
        "measured": measured,
    }
    base.update(keys)
    return base


def test_every_label_is_content_times_the_unit_vector_and_the_books_close():
    """(b)."""
    lamp = {
        "position": CENTRE,
        "family": "light",
        "amount": CONTENT * CLOCK,
        "fixed": True,
        "lamp": {"rate": [1, 1], "directions": [list(d) for d in (*PORT_HEADINGS, *FAN)]},
    }
    screen = {"position": [21, 15, 15], "family": "m", "amount": 1, "fixed": True}
    mirror = {
        "position": [22, 20, 15],
        "family": "m",
        "amount": 1,
        "fixed": True,
        "directions": [[-7, -5, 0]],
        "table": {"light": "rerelease"},
    }
    records: list[dict[str, object]] = []
    simulation = NatureBeamSimulation(
        parse_nature_beam_world(world([lamp, screen, mirror])), records.append
    )
    lamp_entry, screen_entry, mirror_entry = (simulation.measured[n] for n in (1, 2, 3))
    store = simulation.stores[LIGHT]
    unit = simulation.tables.flight.labels
    born = np.array([unit_label(d) for d in (*PORT_HEADINGS, *FAN)], dtype=np.int64).sum(axis=0)
    assert born.tolist() == [378, 241, 121]
    simulation.step()
    assert lamp_entry.turn == CONTENT and store.size == 14
    assert (store.amount == 1).all() and (store.content == CONTENT).all()
    labels = store.labels(np.arange(store.size), unit, False)
    for i in range(store.size):
        assert labels[i].tolist() == (CONTENT * unit[store.direction[i]]).tolist()
        assert (63 * CONTENT) ** 2 < int(labels[i] @ labels[i]) < (65 * CONTENT) ** 2
    # The lamp's birth is one record of 14 rows (m 14): its recoil is the
    # rows' shares, label // 14 each, and the rest of the labels is on the
    # books' `remainder` line; the transit line carries the whole labels
    # (re-run under the one click (stage (vii) step 4); the verdict to be re-read; until stage (vii) step 3 the recoil was the whole labels,
    # [-1134, -723, -363] = -CONTENT x born).
    assert lamp_entry.momentum == [-77, -48, -24]
    assert simulation.books()["momentum"]["transit"] == (CONTENT * born).tolist()
    assert simulation.books()["momentum"]["remainder"] == [-1057, -675, -339]
    u_mirror = np.array(PINNED[(7, 5, 0)], dtype=np.int64)
    share = [int(np.sign(v)) * (CONTENT * abs(int(v)) // 14) for v in u_mirror]
    share_2 = [int(np.sign(v)) * (2 * abs(int(v)) // 14) for v in u_mirror]
    assert share == [11, 7, 0] and share_2 == [7, 5, 0]
    for tick in range(2, TICKS + 1):
        simulation.step()
        books = simulation.books(recount=True)
        assert books["balanced"], tick
        # The turn is the count of the lamp's accumulator (the fraction-
        # free law, 2026-09-20): the lamp pays 42 per birth, so at tick 2
        # its content 3K - 42 turns 2 and the remainder K - 42 carries; the
        # whole part of 3t - 21 t (t - 1) / K is 3t - 1 for every t of the
        # run (3 at every tick until then, the whole part off the clock at
        # the current content).
        assert lamp_entry.turn == (2 if tick == 2 else CONTENT), tick
        momentum = books["momentum"]
        assert [
            a + b + c + d
            for a, b, c, d in zip(
                momentum["measured"],
                momentum["transit"],
                momentum["escaped"],
                momentum["remainder"],
                strict=True,
            )
        ] == [0, 0, 0], tick
        assert books["momentum"]["transit"] == simulation.books()["momentum"]["transit"], tick
        reflected = mirror_entry.taken[LIGHT]["rerelease"]
        # The mirror takes each row's share and recoils by the re-created
        # row's: twice the share per reflection; the second row reflected,
        # born at tick 2 with the content 2, has the share 2 x |u| // 14 =
        # (7, 5, 0) in place of (11, 7, 0).
        second = 1 if reflected >= 2 else 0
        assert mirror_entry.momentum == [
            2 * (s * reflected - (s - t) * second) for s, t in zip(share, share_2, strict=True)
        ], tick
        if store.size:
            # Every label is the row's content times its unit vector; the
            # content of a release is the lamp's turn at its birth (the
            # free release's form, BEAM_LAW note 33), 3 on every row but the
            # 14 born at tick 2 with the content 2 (the fraction-free law,
            # 2026-09-20; 3 on every row until then).
            labels = store.labels(np.arange(store.size), unit, False)
            assert (labels == store.content[:, None] * unit[store.direction]).all(), tick
            assert set(store.content.tolist()) <= {2, CONTENT}, tick
    clicks = [r for r in records if r["event"] == "click"]
    at_screen = [r for r in clicks if r["measured"] == 2]
    # The +X rays and the (11, 1, 0) rays, whose line passes the screen's
    # Node too, each click with the label of their own direction.
    assert at_screen and all(r["amount"] == 1 for r in at_screen)
    # The two rays born at tick 2 carry the content 2: the labels (128, 0,
    # 0) and (128, 12, 0), the shares (9, 0, 0) twice.
    assert {tuple(r["push"]) for r in at_screen} == {
        (192, 0, 0),
        (192, 18, 0),
        (128, 0, 0),
        (128, 12, 0),
    }
    assert {tuple(r["share"]) for r in at_screen} == {(13, 0, 0), (13, 1, 0), (9, 0, 0)}
    assert sum(1 for r in at_screen if r["content"] == 2) == 2
    assert screen_entry.momentum == np.array([r["share"] for r in at_screen]).sum(axis=0).tolist()
    assert mirror_entry.taken[LIGHT]["rerelease"] >= 2
    escaped = [r for r in clicks if r["measured"] is None]
    assert escaped
    total = np.array([r["momentum"] for r in escaped], dtype=np.int64).sum(axis=0)
    assert simulation.books()["momentum"]["escaped"] == total.tolist()


def test_the_bound_refuses_a_label_of_two_to_the_fifty_six_and_accepts_one_less():
    """(c)."""
    lamp = {"position": CENTRE, "family": "light", "amount": 4, "fixed": True}
    holder = {"position": [1, 1, 1], "family": "m", "amount": 4, "fixed": True}

    def transit(family: str, amount: int) -> dict[str, object]:
        return {
            "position": [2, 2, 2],
            "family": family,
            "number": 1,
            "direction": [1, 0, 0],
            "amount": amount,
        }

    for family in ("light", "m"):
        with pytest.raises(ValueError, match=rf"64 x 1 x {1 << 56} = {64 << 56} .* exceeds"):
            parse_nature_beam_world(world([lamp, holder], in_transit=[transit(family, 1 << 56)]))
        parsed = parse_nature_beam_world(
            world([lamp, holder], in_transit=[transit(family, (1 << 56) - 1)])
        )
        assert parsed.in_transit[0].amount == (1 << 56) - 1
    assert MOMENTUM_BOUND // Q == (1 << 56) - 1
    labels = direction_flight(((0, 0, 0), (0, 0, 0), *PORT_HEADINGS, (1, 1, 0))).labels
    heading, diagonal = 2, 8
    node = np.array([[2, 2, 2]], dtype=np.int64)
    for amount, content, free in ((1 << 28, 1 << 28, False), (1 << 56, 0, True)):
        with pytest.raises(
            OverflowError,
            match=rf"amount {amount} and content {content} at Node \[2, 2, 2\] .* {1 << 56} times "
            rf"the largest component 64 = {64 << 56}, exceeds",
        ):
            momentum_labels(
                labels, np.array([heading]), np.array([amount]), np.array([content]), free, node
            )
        wide = momentum_labels(
            labels, np.array([diagonal]), np.array([amount]), np.array([content]), free, node
        )
        assert wide.tolist() == [[45 << 56, 45 << 56, 0]]
    with pytest.raises(OverflowError, match=rf"amount {1 << 32} and content {1 << 31}"):
        label_weights(np.array([1 << 32]), np.array([1 << 31]), False)
    accepted = label_weights(np.array([(1 << 28) + 1]), np.array([(1 << 28) - 1]), False)
    assert accepted.tolist() == [(1 << 56) - 1]
    assert label_weights(np.array([(1 << 56) - 1]), np.array([0]), True).tolist() == [(1 << 56) - 1]
    assert label_weights(np.array([1 << 56]), np.array([0]), True).tolist() == [1 << 56]


def test_a_merged_row_beyond_the_bound_is_refused_before_the_product_naming_the_node():
    """(d)."""
    holder = {"position": [1, 1, 1], "family": "m", "amount": 4, "fixed": True}

    def pair(direction: list[int]) -> list[dict[str, object]]:
        return [
            {
                "position": [2, 2, 2],
                "family": "light",
                "number": 1,
                "direction": direction,
                "amount": 1 << 55,
                "phase": 0,
            }
            for _ in range(2)
        ]

    lamp = {"position": CENTRE, "family": "light", "amount": 4, "fixed": True}
    simulation = NatureBeamSimulation(
        parse_nature_beam_world(world([lamp, holder], in_transit=pair([1, 1, 0])))
    )
    store = simulation.stores[LIGHT]
    assert store.size == 1 and store.amount.tolist() == [1 << 56]
    books = simulation.books(recount=True)
    assert books["momentum"]["transit"] == [45 << 56, 45 << 56, 0] == simulation.transit_momentum()
    for _ in range(3):
        simulation.step()
        assert simulation.books(recount=True)["balanced"]
        assert simulation.transit_momentum() == simulation.recount()["momentum"]
    with pytest.raises(
        OverflowError,
        match=rf"amount {1 << 56} and content 1 at Node \[2, 2, 2\] along \[64, 0, 0\], its weight "
        rf"{1 << 56} times the largest component 64 = {64 << 56}, exceeds",
    ):
        NatureBeamSimulation(parse_nature_beam_world(world([lamp, holder], in_transit=pair([1, 0, 0]))))

    mirror = {
        "position": [5, 5, 0],
        "family": "wall",
        "amount": 1,
        "fixed": True,
        "table": {"light": "rerelease"},
        "directions": [[64, 1, 0]],
    }
    others = [{"position": [10, y, 0], "family": "wall", "amount": 1, "fixed": True} for y in (9, 10)]
    arriving = [
        {
            "position": [4, 5, 0],
            "family": "light",
            "number": 2,
            "direction": [1, 0, 0],
            "amount": 1 << 30,
        },
        {
            "position": [5, 4, 0],
            "family": "light",
            "number": 3,
            "direction": [0, 1, 0],
            "amount": 1 << 30,
        },
    ]
    document = world(
        [mirror, *others],
        shape=[12, 12, 1],
        boundary={"z": "periodic"},
        directions=[[64, 1, 0]],
        families=[{"name": "light", "quantum": 1 << 25}, {"name": "wall", "quantum": 1}],
        in_transit=arriving,
        ticks=2,
    )
    records: list[dict[str, object]] = []
    simulation = NatureBeamSimulation(parse_nature_beam_world(document), records.append)
    simulation.step()
    re_emitted = [r for r in records if r["event"] == "rerelease"]
    assert [(r["number"], r["amount"], r["push"]) for r in re_emitted] == [
        (2, 1 << 30, [1 << 61, 0, 0]),
        (3, 1 << 30, [0, 1 << 61, 0]),
    ]
    store = simulation.stores[LIGHT]
    assert store.size == 1 and store.amount.tolist() == [1 << 31]
    assert store.node.tolist() == [store.flat((5, 5, 0))] and store.content.tolist() == [1 << 25]
    with pytest.raises(
        OverflowError,
        match=rf"amount {1 << 31} and content {1 << 25} at Node \[5, 5, 0\] along \[64, 1, 0\], "
        rf"its weight {1 << 56} times the largest component 64 = {64 << 56}, exceeds",
    ):
        simulation.books(recount=True)
