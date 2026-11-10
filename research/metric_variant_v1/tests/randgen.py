"""Random B3-local translation-invariant tensors and random exact states for the Stage-0 tests (seeded, data only)."""
from __future__ import annotations

import random

import numpy as np

from research.metric_variant_v1.core.engine import OBJ, State
from research.metric_variant_v1.core.lattice import DIRECTIONS, OFFSETS, ZERO, lattice
from research.metric_variant_v1.core.tensor import Block, GearType

NEG = {d: tuple(-v for v in d) for d in OFFSETS}


def _local_offsets(rng: random.Random, k: int, onsite_p: float = 0.35) -> list[tuple]:
    """k factor offsets on one node or one face link (B3): all in {0, e} for a single random e."""
    if rng.random() < onsite_p:
        return [ZERO] * k
    e = rng.choice(DIRECTIONS)
    offs = [rng.choice((ZERO, e)) for _ in range(k)]
    if all(o == ZERO for o in offs):
        offs[rng.randrange(k)] = e
    return offs


def symmetric_linear_terms(rng, names, scale, rowsum, pairs):
    """Linear part u = grad of a random quadratic potential Phi2 = sum m*scale*b_i(x)*b_j(x+o): symmetric operator,
    absolute row sums <= rowsum*scale (bounded leapfrog for rowsum <= 6)."""
    load = {n: 0 for n in names}
    terms = []
    for _ in range(pairs):
        i, j = rng.choice(names), rng.choice(names)
        o = rng.choice(OFFSETS)
        m = rng.choice((-1, 1))
        if i == j and o == ZERO:
            cost = {i: 2}
            new = [(i, 2 * m * scale, ((i, ZERO, "b"),))]
        elif i == j:
            cost = {i: 2}
            new = [(i, m * scale, ((i, o, "b"),)), (i, m * scale, ((i, NEG[o], "b"),))]
        else:
            cost = {i: 1, j: 1}
            new = [(i, m * scale, ((j, o, "b"),)), (j, m * scale, ((i, NEG[o], "b"),))]
        if all(load[g] + c <= rowsum for g, c in cost.items()):
            for g, c in cost.items():
                load[g] += c
            terms.extend(new)
    return terms


def random_tensor_block(seed: int, G: int = 6, Q: int = 10 ** 6, a_reads: bool = False, max_degree: int = 3,
                        nonlinear=(2, 4), small: int = 5, constants: bool = True, prefix: str = "g",
                        rowsum: int = 6, labels=("official", "audit")) -> Block:
    """T0.3/T0.4 family: symmetric Q-weighted linear part + small nonlinear terms (+ constants) (+ acyclic a-reads)."""
    rng = random.Random(seed)
    names = [f"{prefix}{i}" for i in range(G)]
    gears = tuple(GearType(n, labels[i % len(labels)]) for i, n in enumerate(names))
    terms = symmetric_linear_terms(rng, names, Q, rowsum, pairs=2 * G)
    order = names[:]
    rng.shuffle(order)
    pos = {n: p for p, n in enumerate(order)}
    for t in names:
        for _ in range(rng.randint(*nonlinear)):
            k = rng.randint(2, max_degree) if max_degree >= 2 else 1
            offs = _local_offsets(rng, k)
            facs = tuple((rng.choice(names), o, "b") for o in offs)
            c = rng.choice([v for v in range(-small, small + 1) if v])
            terms.append((t, c, facs))
        if constants and rng.random() < 0.5:
            terms.append((t, rng.choice([v for v in range(-7, 8) if v]), ()))
        if a_reads and pos[t] > 0:
            earlier = order[:pos[t]]
            # linear two-time read of an earlier gear
            o = _local_offsets(rng, 1)[0]
            terms.append((t, rng.choice([v for v in range(-9, 10) if v]), ((rng.choice(earlier), o, "a"),)))
            # nonlinear read mixing a (earlier gears) and b (any gear)
            k = rng.randint(2, max_degree) if max_degree >= 2 else 1
            offs = _local_offsets(rng, k)
            facs = [(rng.choice(earlier), offs[0], "a")]
            facs += [(rng.choice(names), o, "b") for o in offs[1:]]
            if k >= 3 and rng.random() < 0.5:
                facs[-1] = (rng.choice(earlier), offs[-1], "a")
            terms.append((t, rng.choice([v for v in range(-3, 4) if v]), tuple(facs)))
    return Block(gears, tuple(terms), Q=Q)


def random_state(seed: int, G: int, L: int, D: int, lo: int, hi: int) -> State:
    rng = random.Random(seed)
    N = lattice(L).N
    a = np.array([[rng.randint(lo, hi) for _ in range(N)] for _ in range(G)], dtype=OBJ)
    b = np.array([[rng.randint(lo, hi) for _ in range(N)] for _ in range(G)], dtype=OBJ)
    r = np.array([[rng.randrange(D) for _ in range(N)] for _ in range(G)], dtype=OBJ)
    return State(L, a, b, r)


def coupled_new_block(seed: int, ref_names, n_new: int = 32, max_degree: int = 3, deviation: bool = True,
                      back: int = 24, a_reads: bool = True, prefix: str = "n") -> tuple[Block, list]:
    """T0.6: new gears coupled to the reference, NO constants.
    deviation=True: every term targeting a new gear contains >= 1 new-gear factor; back-coupling terms into the
    reference always contain >= 1 new-gear factor. Returns (block of the new gears, back-coupling terms)."""
    rng = random.Random(seed)
    names = [f"{prefix}{i:02d}" for i in range(n_new)]
    gears = tuple(GearType(n, "audit" if i % 2 else "official") for i, n in enumerate(names))
    order = names[:]
    rng.shuffle(order)
    pos = {n: p for p, n in enumerate(order)}
    every = list(ref_names) + names
    terms = []

    def factor_list(k, must_new, t):
        offs = _local_offsets(rng, k)
        facs = []
        for i, o in enumerate(offs):
            pool = names if (must_new and i == 0) else every
            g = rng.choice(pool)
            field = "b"
            if a_reads and t is not None and g in pos and pos[g] < pos[t] and rng.random() < 0.3:
                field = "a"
            facs.append((g, o, field))
        rng.shuffle(facs)
        return tuple(facs)

    for t in names:
        for _ in range(rng.randint(3, 6)):
            k = rng.randint(1, max_degree)
            terms.append((t, rng.choice([v for v in range(-9, 10) if v]), factor_list(k, deviation, t)))
    back_terms = []
    for _ in range(back):
        t = rng.choice(list(ref_names))
        k = rng.randint(1, max_degree)
        back_terms.append((t, rng.choice([v for v in range(-9, 10) if v]), factor_list(k, True, None)))
    return Block(gears, tuple(terms)), back_terms


def perf_new_block(seed: int, ref_names, n_new: int = 32, Q: int = 7, prefix: str = "p") -> Block:
    """T0.7: a random rank-3 (degree <= 2) block for 32 new gears, reading the reference and each other.
    Linear new-new couplings are symmetric and Q-weighted (bounded); quadratic terms read reference b's and at most
    one new gear that comes earlier in a random order (no quadratic feedback loop), so the values stay in int64."""
    rng = random.Random(seed)
    names = [f"{prefix}{i:02d}" for i in range(n_new)]
    gears = tuple(GearType(n, "audit" if i % 2 else "official") for i, n in enumerate(names))
    terms = symmetric_linear_terms(rng, names, Q, 6, pairs=2 * n_new)
    order = names[:]
    rng.shuffle(order)
    pos = {n: p for p, n in enumerate(order)}
    for t in names:
        for _ in range(3):                                   # linear reads of the reference
            o = _local_offsets(rng, 1)[0]
            terms.append((t, rng.choice((-3, -2, -1, 1, 2, 3)), ((rng.choice(ref_names), o, "b"),)))
        for _ in range(4):                                   # quadratic terms
            offs = _local_offsets(rng, 2)
            f1 = (rng.choice(ref_names), offs[0], "b")
            earlier = order[:pos[t]]
            if earlier and rng.random() < 0.5:
                f2 = (rng.choice(earlier), offs[1], "b")
            else:
                f2 = (rng.choice(ref_names), offs[1], "b")
            terms.append((t, rng.choice((-2, -1, 1, 2)), (f1, f2)))
    return Block(gears, tuple(terms), Q=Q)
