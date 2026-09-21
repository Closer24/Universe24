"""The click without amplitudes (2026-09-21; the model owner's decision,
record 188 of docs/LOG_2026-09-20.md; BEAM_LAW note 37 (xii); the derivation
mathematician's section 6.7 with `click_gram.py`): the record's cell is the
phase-count vector **f** (the amount per phase step), the click's weight the
one bilinear form f^T G f with the Gram matrix **G** = **E**^T **E** of the
tables, for one arm evaluated explicitly and for several arms through the
matrix's rank-2 factorisation, the pointer **E f**. The expected integers of
docs/TEST_EXPECTATIONS.md ("The click without amplitudes"), written down
first:

(a) the Gram matrix at N = 64: G_jk = C_j C_k + S_j S_k over the rounded
    tables C and S themselves (never the cosine of j - k), symmetric; its
    diagonal the eight values 65448, 65501, 65522, 65533, 65536, 65650,
    65717, 65773 (the eight totals over the births of series L); not
    circulant, G_(j+1)(k+1) differing from G_jk on 3696 of the 4096
    entries (G_11 = 65650, G_01 = 65280, G_12 = 65255); of rank 2 (the
    3 x 3 minors on the phases (0, 1, 2) and (0, 5, 17) are 0); killing
    every antipodal pair e_p + e_(p+32) exactly; stored through N = 512
    (`phase_gram`; N = 1024 refused as not stored, a float and a boolean
    refused) and formed from the tables beyond it (a layer at N = 4096
    holds no matrix and forms the entries, the same identity);
(b) the identity f^T G f = X^2 + Y^2 with (X, Y) = E f: on 200 random
    sparse integer vectors of Z^64 (entries -5 .. 5, a phase present with
    probability 0.3), on 50 at N = 4096 through the formed entries, and on
    the registered shape of `mz_equal`'s record at every u (41 rows of
    amount 1 at u + 16 and the cancel's 1 at u + 32, the amplitude scale
    32 and the identity 256^2, the multiplicity 1682): the weights 1681 x
    2^42 x q[u + 16] and 2^42 x q[u + 32] with q[p] = C[p]^2 + S[p]^2,
    the ladder's cell 0 at all 64 u (the registered 64 / 0);
(c) the layer's `cells` against the click as it was, on synthetic records
    fed through `end`: one arm at two Nodes with two labels (a plain set),
    one arm with a which-path read factor (four cells, the read's two
    channels by the end's two), a rotated set at the settings
    (8, 0) and (8, 16) with the bits 0 and 1, two arms at rotated sets
    (the pair's form) and three arms (GHZ's): every cell's every Node
    tuple weighs exactly what the former evaluation gave (the pointer
    32 w (C[p], S[p]) per row, the residual the rotation's complex entry
    times the pointer, the labels' products summed, the square);
(d) the turn as a shift: the residual of the bit 1 at a turn t is the
    count at p + t with the scalar S' x 256, the same pointer as the
    former product (C_t, S_t)(C_p, S_p) at every phase for t in {0, 16,
    32, 48} (the register's turns 0 and 16) and not at t = 3 (the entry
    181 at the phase 1 with the weight 7: formerly (76811875, 31668665),
    now (76871424, 31786496), one rounding in place of two);
(e) the several-arm product is not the ring convolution: E(e_1)^2 =
    (64400, 12750) against 256 E(e_2) = (64256, 12800); the tensor form
    is exact: the product of two arms' pointers equals the sum over the
    phase pairs of f_p g_q times the product of the tables' entries, on
    100 random pairs of vectors;
(f) the ring product: the read's factor 256^2 e_0 times f is 256^2 f, e_5
    times e_60 is e_1 at N = 64, and a vector with two rows at one phase
    is one count.
"""

from __future__ import annotations

import itertools
import random

import pytest

from event_universe.core.phase import (
    GRAM_STORED_STEPS,
    PHASE_COSINE_SCALE,
    phase_cosines,
    phase_gram,
    phase_sines,
)
from event_universe.events.amplitude import (
    AMPLITUDE_SCALE,
    NO_NODE,
    ROTATION_IDENTITY,
    Layer,
    branch_of,
    cell_of,
    cmul,
    half_angle,
    ring_product,
)

N = 64
C = phase_cosines(N)
S = phase_sines(N)
NAMES = ["a", "b", "c", "face:+x"]
KEYS = [("set", 0), ("set", 1), ("set", 2), ("face", 0)]


def layer_of(steps: int = N) -> Layer:
    return Layer(list(NAMES), list(KEYS), [], ["light"], steps)


def det3(m: list[list[int]]) -> int:
    return (
        m[0][0] * (m[1][1] * m[2][2] - m[1][2] * m[2][1])
        - m[0][1] * (m[1][0] * m[2][2] - m[1][2] * m[2][0])
        + m[0][2] * (m[1][0] * m[2][1] - m[1][1] * m[2][0])
    )


def test_the_gram_matrix_is_the_tables_own():
    """(a)."""
    gram = phase_gram(N)
    assert all(gram[j][k] == C[j] * C[k] + S[j] * S[k] for j in range(N) for k in range(N))
    assert all(gram[j][k] == gram[k][j] for j in range(N) for k in range(N))
    assert sorted({gram[j][j] for j in range(N)}) == [
        65448,
        65501,
        65522,
        65533,
        65536,
        65650,
        65717,
        65773,
    ]
    moved = sum(1 for j in range(N) for k in range(N) if gram[j][k] != gram[(j + 1) % N][(k + 1) % N])
    assert moved == 3696
    assert (gram[1][1], gram[0][1], gram[1][2]) == (65650, 65280, 65255)
    for phases in ((0, 1, 2), (0, 5, 17)):
        assert det3([[gram[j][k] for k in phases] for j in phases]) == 0
    layer = layer_of()
    assert all(layer.gram_form({p: 3, (p + 32) % N: 3}) == 0 for p in range(N))
    assert layer.gram is gram
    assert phase_gram(GRAM_STORED_STEPS)[0][0] == PHASE_COSINE_SCALE**2
    with pytest.raises(ValueError, match="stored for phase_steps"):
        phase_gram(1024)
    with pytest.raises(ValueError, match="stored for phase_steps"):
        phase_gram(64.0)
    with pytest.raises(ValueError, match="stored for phase_steps"):
        phase_gram(True)
    big = layer_of(4096)
    assert big.gram is None
    assert big.gram_entry(5, 1000) == phase_cosines(4096)[5] * phase_cosines(4096)[1000] + (
        phase_sines(4096)[5] * phase_sines(4096)[1000]
    )


def random_vector(draw: random.Random, steps: int, phases: int | None = None) -> dict[int, int]:
    if phases is None:
        return {p: draw.randint(-5, 5) for p in range(steps) if draw.random() < 0.3}
    return {draw.randrange(steps): draw.randint(-1000, 1000) for _ in range(phases)}


def test_the_form_equals_the_pointers_inner_product():
    """(b)."""
    draw = random.Random(1)
    layer = layer_of()
    for _ in range(200):
        counts = random_vector(draw, N)
        x, y = layer.evaluate(counts)
        assert layer.gram_form(counts) == x * x + y * y
    big = layer_of(4096)
    for _ in range(50):
        counts = random_vector(draw, 4096, 6)
        x, y = big.evaluate(counts)
        assert big.gram_form(counts) == x * x + y * y
    unit = AMPLITUDE_SCALE * ROTATION_IDENTITY
    for u in range(N):
        first = {(u + 16) % N: 41 * unit}
        second = {(u + 32) % N: unit}
        weights = [(layer.gram_form(first), 1682), (layer.gram_form(second), 1682)]
        assert weights[0][0] == 1681 * (1 << 42) * (C[(u + 16) % N] ** 2 + S[(u + 16) % N] ** 2)
        assert weights[1][0] == (1 << 42) * (C[(u + 32) % N] ** 2 + S[(u + 32) % N] ** 2)
        assert cell_of(weights, N, u) == 0


# -- (c): the click as it was, computed beside the layer ---------------------------

Row = tuple[int, int, int, int, int, tuple[int, int, int] | None, tuple[int, int] | None, bool]
# (set index, arm, label, amount, phase, Node, rotation, absorbed)


def former_entries(rotation: tuple[int, int], bit: int) -> tuple[tuple[int, int], tuple[int, int]]:
    """The rotation's entries as the click formed them until 2026-09-21:
    complex integers in 1/256^2, the turn evaluated and multiplied."""
    s, t = rotation
    c, sn = half_angle(s, N)
    turn = (C[t % N], S[t % N])
    if bit == 0:
        return (c * PHASE_COSINE_SCALE, 0), (-sn * PHASE_COSINE_SCALE, 0)
    return cmul((sn, 0), turn), cmul((c, 0), turn)


def former_residuals(
    rows: list[Row],
) -> dict[tuple[int, int, int], dict[tuple[object, int], tuple[int, int]]]:
    """Per (set, arm, channel) the former complex residual per (Node, label)."""
    found: dict[tuple[int, int, int], dict[tuple[object, int], tuple[int, int]]] = {}
    for set_index, arm, label, amount, phase, node, rotation, absorbed in rows:
        if not absorbed:
            found.setdefault((set_index, arm, label), {})[(NO_NODE, label)] = (ROTATION_IDENTITY, 0)
            continue
        weight = AMPLITUDE_SCALE * amount
        pointer = (weight * C[phase], weight * S[phase])
        at = NO_NODE if node is None else node
        if rotation is None:
            entries = [(label, (ROTATION_IDENTITY, 0))]
        else:
            entries = list(enumerate(former_entries(rotation, (label >> arm) & 1)))
        for channel, entry in entries:
            held = found.setdefault((set_index, arm, channel), {})
            value = cmul(entry, pointer)
            x, y = held.get((at, label), (0, 0))
            held[(at, label)] = (x + value[0], y + value[1])
    return found


def feed(layer: Layer, rows: list[Row], labels: dict[int, int], arms: int) -> None:
    layer.birth(1, 1, 0, 0, labels, arms, sum(a for _, _, _, a, _, _, _, absorbed in rows if absorbed))
    for set_index, arm, label, amount, phase, node, rotation, absorbed in rows:
        layer.end(
            2,
            set_index,
            1,
            branch_of(arm, label),
            1,
            amount,
            phase,
            absorbed=absorbed,
            rotation=rotation,
            node=node,
        )


def check_against_the_former_click(rows: list[Row], labels: dict[int, int], arms: int) -> int:
    layer = layer_of()
    feed(layer, rows, labels, arms)
    record = layer.records[1]
    former = former_residuals(rows)
    present = sorted(labels)
    cells = layer.cells(record)
    assert cells
    for factors, numerator, _, tuples in cells:
        total = 0
        for nodes, weight in tuples:
            ends = [(o, c) for o, c in factors if not o.read]
            real, imaginary = 0, 0
            for label in present:
                product = (1, 0)
                for offer, channel in factors:
                    node = NO_NODE if offer.read else nodes[ends.index((offer, channel))]
                    residual = former.get((offer.set_index, offer.arm, channel), {}).get(
                        (node, label), (0, 0)
                    )
                    product = cmul(product, residual)
                real += product[0]
                imaginary += product[1]
            assert weight == real * real + imaginary * imaginary
            total += weight
        assert numerator == total
    return len(cells)


def test_one_arm_cells_weigh_what_the_former_click_gave():
    """(c), the plain set at two Nodes with two labels and a face."""
    rows: list[Row] = [
        (0, 0, 0, 3, 5, (1, 0, 0), None, True),
        (0, 0, 0, 2, 21, (1, 0, 0), None, True),
        (0, 0, 1, 1, 40, (1, 0, 0), None, True),
        (0, 0, 0, 4, 63, (1, 1, 0), None, True),
        (3, 0, 1, 2, 9, (0, 3, 0), None, True),
    ]
    assert check_against_the_former_click(rows, {0: 1, 1: 1}, 1) == 3


def test_a_read_factor_selects_the_label_as_before():
    """(c), the which-path read at the set b, the ends at a."""
    rows: list[Row] = [
        (1, 0, 0, 1, 0, None, None, False),
        (1, 0, 1, 1, 0, None, None, False),
        (0, 0, 0, 1, 12, (2, 0, 0), None, True),
        (0, 0, 1, 1, 44, (2, 0, 0), None, True),
        (0, 0, 1, 1, 45, (2, 1, 0), None, True),
    ]
    assert check_against_the_former_click(rows, {0: 1, 1: 1}, 1) == 4


@pytest.mark.parametrize("turn", [0, 16])
def test_rotated_cells_weigh_what_the_former_click_gave(turn):
    """(c), the rotated set at the settings (8, t) with both bits."""
    rows: list[Row] = [
        (0, 0, 0, 1, 7, (1, 0, 0), (8, turn), True),
        (0, 0, 1, 1, 7, (1, 0, 0), (8, turn), True),
        (0, 0, 0, 1, 39, (1, 0, 0), (8, turn), True),
        (0, 0, 1, 2, 20, (1, 2, 0), (8, turn), True),
    ]
    assert check_against_the_former_click(rows, {0: 1, 1: 1}, 1) == 2


@pytest.mark.parametrize("turn", [0, 16])
def test_the_pairs_cells_weigh_what_the_former_click_gave(turn):
    """(c), two arms at two rotated sets (the pair's form)."""
    rows: list[Row] = [
        (0, 0, 0, 1, 3, (0, 1, 0), (0, 0), True),
        (0, 0, 3, 1, 3, (0, 1, 0), (0, 0), True),
        (1, 1, 0, 1, 3, (4, 1, 0), (8, turn), True),
        (1, 1, 3, 1, 3, (4, 1, 0), (8, turn), True),
    ]
    assert check_against_the_former_click(rows, {0: 1, 3: 1}, 2) == 4


def test_ghzs_cells_weigh_what_the_former_click_gave():
    """(c), three arms (GHZ's form) with a turn of 16 on two of them."""
    rows: list[Row] = [
        (0, 0, 0, 1, 11, (0, 1, 0), (16, 0), True),
        (0, 0, 7, 1, 11, (0, 1, 0), (16, 0), True),
        (1, 1, 0, 1, 11, (4, 1, 0), (16, 16), True),
        (1, 1, 7, 1, 11, (4, 1, 0), (16, 16), True),
        (2, 2, 0, 1, 11, (2, 3, 0), (16, 16), True),
        (2, 2, 7, 1, 11, (2, 3, 0), (16, 16), True),
    ]
    assert check_against_the_former_click(rows, {0: 1, 7: 1}, 3) == 8


def test_the_turn_is_a_shift_where_the_tables_turn_exactly():
    """(d)."""
    layer = layer_of()
    for t in (0, 16, 32, 48, 3):
        (scalar, shift), _ = layer.rotation((8, t), 1)
        assert (scalar, shift) == (half_angle(8, N)[1] * PHASE_COSINE_SCALE, t)
        same = all(
            cmul(cmul((entry, 0), (C[t], S[t])), (7 * C[p], 7 * S[p]))
            == layer.evaluate({(p + t) % N: entry * PHASE_COSINE_SCALE * 7})
            for p in range(N)
            for entry in (1, 181, -255)
        )
        assert same == (t % 16 == 0), t
    former = cmul(cmul((181, 0), (C[3], S[3])), (7 * C[1], 7 * S[1]))
    assert former == (76811875, 31668665)
    assert layer.evaluate({4: 181 * PHASE_COSINE_SCALE * 7}) == (76871424, 31786496)


def test_several_arms_are_the_tensor_form_and_not_the_convolution():
    """(e)."""
    layer = layer_of()
    assert cmul(layer.evaluate({1: 1}), layer.evaluate({1: 1})) == (64400, 12750)
    assert tuple(256 * v for v in layer.evaluate({2: 1})) == (64256, 12800)
    draw = random.Random(2)
    for _ in range(100):
        f, g = random_vector(draw, N), random_vector(draw, N)
        product = cmul(layer.evaluate(f), layer.evaluate(g))
        tensor = (
            sum(
                a * b * (C[p] * C[q] - S[p] * S[q])
                for (p, a), (q, b) in itertools.product(f.items(), g.items())
            ),
            sum(
                a * b * (C[p] * S[q] + S[p] * C[q])
                for (p, a), (q, b) in itertools.product(f.items(), g.items())
            ),
        )
        assert product == tensor


def test_the_ring_product():
    """(f)."""
    f = {3: 5, 10: -2}
    assert ring_product({0: ROTATION_IDENTITY}, f, N) == {
        3: 5 * ROTATION_IDENTITY,
        10: -2 * ROTATION_IDENTITY,
    }
    assert ring_product({5: 1}, {60: 1}, N) == {1: 1}
    layer = layer_of()
    layer.birth(1, 1, 0, 0, {0: 1}, 1, 2)
    layer.end(2, 0, 1, 0, 1, 1, 9, node=(1, 0, 0))
    layer.end(2, 0, 1, 0, 1, 1, 9, node=(1, 0, 0))
    offer = layer.records[1].offers[(0, 0)]
    assert offer.counts[((1, 0, 0), 0)] == {9: 2 * AMPLITUDE_SCALE}
    assert offer.residuals[0][((1, 0, 0), 0)] == {9: 2 * AMPLITUDE_SCALE * ROTATION_IDENTITY}
