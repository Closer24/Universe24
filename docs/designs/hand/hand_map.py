"""The hand on the message (hand-v1): the 48 symmetries of the GameBoard
acting on a signed heading (the axial record) and on a hand bit (a
pseudoscalar), and the sign of the right-hand rule under each (the
mathematician, 2026-09-20, read-only; standalone, exact integers). Output
beside this file: `hand_map.out`.
"""

from __future__ import annotations

import itertools

HEADINGS = ((1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, 1), (0, 0, -1))  # Port order


def apply(
    perm: tuple[int, int, int], signs: tuple[int, int, int], v: tuple[int, int, int]
) -> tuple[int, int, int]:
    """The signed axis permutation g: (g v)_i = signs_i x v_perm(i)."""
    return (signs[0] * v[perm[0]], signs[1] * v[perm[1]], signs[2] * v[perm[2]])


def parity(perm: tuple[int, int, int]) -> int:
    inversions = sum(1 for i in range(3) for j in range(i + 1, 3) if perm[i] > perm[j])
    return -1 if inversions % 2 else 1


def det(perm: tuple[int, int, int], signs: tuple[int, int, int]) -> int:
    return parity(perm) * signs[0] * signs[1] * signs[2]


group = [(p, s) for p in itertools.permutations(range(3)) for s in itertools.product((1, -1), repeat=3)]
assert len(group) == 48
proper = [g for g in group if det(*g) == 1]
print(
    "the 48 signed axis permutations: proper (det +1)",
    len(proper),
    "; improper (det -1)",
    48 - len(proper),
)
print()
print(
    "g = (perm, signs)          det | polar image of the six headings | axial image (det x g) | hand h -> det x h"
)
for perm, signs in group:
    d = det(perm, signs)
    polar = [HEADINGS.index(apply(perm, signs, e)) for e in HEADINGS]
    axial = [HEADINGS.index(tuple(d * c for c in apply(perm, signs, e))) for e in HEADINGS]
    print(f"{perm} {signs!s:14s} {d:+d} | {polar} | {axial} | h -> {d:+d} h")
print()
# The hemisphere rule of `become`: the product's direction d is admitted iff
# sign(a . d) = -h_product, a the parent's axial record. Under every g the
# axial record maps by det(g) g and the direction by g, so a . d maps to
# det(g) (a . d): kept by the 24 proper rotations, flipped by the 24 improper.
vectors = [v for v in itertools.product(range(-2, 3), repeat=3) if any(v)]
kept = flipped = 0
for perm, signs in group:
    d = det(perm, signs)
    for a in HEADINGS:
        for v in vectors:
            before = sum(x * y for x, y in zip(a, v, strict=True))
            a2 = tuple(d * c for c in apply(perm, signs, a))
            v2 = apply(perm, signs, v)
            after = sum(x * y for x, y in zip(a2, v2, strict=True))
            assert after == d * before
            if d == 1:
                kept += 1
            else:
                flipped += 1
print(
    f"the right-hand rule's sign a . d: kept under the 24 proper rotations ({kept} cases), negated under the 24 improper ({flipped} cases): exact"
)


# det is a homomorphism: the hand's representation composes.
def compose(g, h):
    (p1, s1), (p2, s2) = g, h
    # (g h) v = g (h v): perm and signs of the product
    perm = tuple(p2[p1[i]] for i in range(3))
    signs = tuple(s1[i] * s2[p1[i]] for i in range(3))
    return perm, signs


ok = all(det(*compose(g, h)) == det(*g) * det(*h) for g in group for h in group)
print(
    "det(g h) = det(g) det(h) on all 48 x 48 products:",
    ok,
    "(the hand's representation is a group action)",
)
closed = all(compose(g, h) in group for g in group for h in group)
print("the 48 close under composition:", closed)
