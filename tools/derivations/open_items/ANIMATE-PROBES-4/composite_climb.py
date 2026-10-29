"""Toy: does the chosen path help build ever more complex clocks? (Animate; the owner's word of 2026-10-28, 15:57 UTC:
"Does this help build more and more complex clocks?")

1. T, each kind's time reversal, keeps every kind (read by this count; no act applies T, decision 27). T commutes
   with every turn, so it sends each kind to the kind of the conjugate characters; it keeps every kind exactly where
   every turn is conjugate to its own reverse. Counted exactly on the 24 turns and on their 48 lifts to the twins
   (Gaussian rationals up to a positive scalar, as in kind_kept.py), and on the mutant, the 12 turns of the
   tetrahedron and their 24 lifts.
2. The kinds built from the twins, each a meeting of a composite with one more twin (the 24's projections by the
   characters, checked against the built kinds' traces): each kind's rung (the fewest twins that hold it), its T T, and
   whether it can hold a direction (T1 in K x K*, by the characters, and the largest |<S_z>| it shows).
3. One composite clock over many bangs, in the plan's item (t): every meeting is one shared dial, the 24 decompose it
   into kinds, and the click draws a kind with shares the projections' norms; the composite is then a clock of the kind
   drawn, its components that kind's own (line 98's count stays fixed). Each bang:
     - no act at the top (decision 27): the composite goes on as its gears hold it; with --former, the former
       turnover, T = J K by the kind, for comparison;
     - the fitting lays one new twin: along the composite's standing direction, by S . J at the coupling's strength,
       where the composite holds one; along the bang's own lead axis with a fair sign where it holds none;
     - the composite and the twin meet, and the click draws the kind.
   The rules for what crosses into the next bang:
     rewound   nothing: the exact rewind undoes the click, so each bang's composite is one meeting of two fresh twins;
     axis      the composite stands, and the twin is laid on its line with a fair sign (no bending);
     half      the twin laid half along the composite's direction (its sign along it three times in four);
     choice    the twin laid wholly along it;
     against   wholly against it: the coupling's other sign.
   The composite's direction is its T1 reading, the sum of its parts' spins read in its kind; a kind reached by more
   than one route is read through its first route. The draws come from a fixed stream of fair digits, SHA-256 of the
   seed and a counter (the vernier's stand-in; the former linear congruential bit repeated every 2^17 bits, so a rule's
   2,048 runs replayed part of it), each rule on its own stream; the states are complex doubles. --seed N sets the seed.
Read per bang over many runs: the kinds' shares, the share holding a direction, and the share that has held all eight.
"""

import hashlib
import sys
from fractions import Fraction as Q
from itertools import permutations, product

import numpy as np

BANGS, RUNS = 24, 2048
FORMER = "--former" in sys.argv  # the former turnover at the top, which decision 27 cancelled
SEED = int(sys.argv[sys.argv.index("--seed") + 1]) if "--seed" in sys.argv else 2026


# 1. Exact: Gaussian rationals as pairs (re, im) of Fractions.
def gr(a, b=0):
    return (Q(a), Q(b))


ZERO = gr(0)


def gmul(x, y):
    return (x[0] * y[0] - x[1] * y[1], x[0] * y[1] + x[1] * y[0])


def gadd(x, y):
    return (x[0] + y[0], x[1] + y[1])


def gneg(x):
    return (-x[0], -x[1])


def gconj(x):
    return (x[0], -x[1])


def gdiv(x, y):
    n = y[0] * y[0] + y[1] * y[1]
    return ((x[0] * y[0] + x[1] * y[1]) / n, (x[1] * y[0] - x[0] * y[1]) / n)


def mmul(a, b):
    return [[gadd(gmul(a[i][0], b[0][j]), gmul(a[i][1], b[1][j])) for j in range(2)] for i in range(2)]


def adjugate(m):
    return [[m[1][1], gneg(m[0][1])], [gneg(m[1][0]), m[0][0]]]


def det(m):
    return gadd(gmul(m[0][0], m[1][1]), gneg(gmul(m[0][1], m[1][0])))


def dagger(m):
    return [[gconj(m[0][0]), gconj(m[1][0])], [gconj(m[0][1]), gconj(m[1][1])]]


def key(m):
    """The matrix up to a positive real scalar: its entries over the first nonzero one, and that entry's ray."""
    flat = [x for row in m for x in row]
    e = next(x for x in flat if x != ZERO)
    ray = (1 if e[0] > 0 else -1, e[1] / e[0]) if e[0] != 0 else (0, 1 if e[1] > 0 else -1)
    return tuple(gdiv(x, e) for x in flat), ray


GENERATORS = [
    [[gr(1, -1), ZERO], [ZERO, gr(1, 1)]],  # a quarter turn about z
    [[gr(1), gr(0, -1)], [gr(0, -1), gr(1)]],  # a quarter turn about x
    [[gr(1, -1), gr(-1, -1)], [gr(1, -1), gr(1, 1)]],  # a third of a turn about (1, 1, 1)
]
PAULI = [
    [[ZERO, gr(1)], [gr(1), ZERO]],
    [[ZERO, gr(0, -1)], [gr(0, 1), ZERO]],
    [[gr(1), ZERO], [ZERO, gr(-1)]],
]


def lifts():
    """The 24 turns' lifts to the twins, closed from the generators up to a positive real scalar."""
    found = {key(g): g for g in GENERATORS}
    frontier = list(found.values())
    while frontier:
        nxt = []
        for m in frontier:
            for g in GENERATORS:
                p = mmul(m, g)
                if key(p) not in found:
                    found[key(p)] = p
                    nxt.append(p)
        frontier = nxt
    return list(found.values())


def rotation(m):
    """The turn a lift makes: R_ab = Tr(sigma_a M sigma_b M^dagger) / (2 det M), integers."""
    d = det(m)[0]
    rows = []
    for a in range(3):
        row = []
        for b in range(3):
            p = mmul(mmul(PAULI[a], m), mmul(PAULI[b], dagger(m)))
            row.append((p[0][0][0] + p[1][1][0]) / (2 * d))
        rows.append(tuple(row))
    return tuple(rows)


def even(r):
    """Whether the turn permutes the three axes evenly (the tetrahedron's 12 turns)."""
    perm = [next(j for j in range(3) if r[i][j] != 0) for i in range(3)]
    return sum(perm[i] > perm[j] for i in range(3) for j in range(i + 1, 3)) % 2 == 0


def turns():
    found = []
    for perm in permutations(range(3)):
        for signs in product((1, -1), repeat=3):
            m = np.zeros((3, 3), dtype=int)
            for i, j in enumerate(perm):
                m[i][j] = signs[i]
            if round(np.linalg.det(m)) == 1:
                found.append(m)
    return found


def classes_turns(group):
    keys = [tuple(map(tuple, g)) for g in group]
    seen, count, real = set(), 0, 0
    for g in group:
        cls = frozenset(tuple(map(tuple, h @ g @ h.T)) for h in group)
        if cls & seen:
            continue
        seen |= cls
        count += 1
        real += tuple(map(tuple, g.T)) in cls
    assert len(seen) == len(keys)
    return count, real


def classes_lifts(group):
    seen, count, real = set(), 0, 0
    for g in group:
        cls = frozenset(key(mmul(mmul(h, g), adjugate(h))) for h in group)
        if cls & seen:
            continue
        seen |= cls
        count += 1
        real += key(adjugate(g)) in cls
    return count, real


# 2 and 3. The kinds, in complex doubles.
SQ2 = np.sqrt(2.0)
CHARACTERS = {  # on E, -E, C3, -C3, C4, -C4, the axes' half turns, the diagonals' half turns
    "A1": (1, 1, 1, 1, 1, 1, 1, 1),
    "A2": (1, 1, 1, 1, -1, -1, 1, -1),
    "E": (2, 2, -1, -1, 0, 0, 2, 0),
    "T1": (3, 3, 0, 0, 1, 1, -1, -1),
    "T2": (3, 3, 0, 0, -1, -1, -1, 1),
    "E1/2": (2, -2, 1, -1, SQ2, -SQ2, 0, 0),
    "E5/2": (2, -2, 1, -1, -SQ2, SQ2, 0, 0),
    "G3/2": (4, -4, -1, 1, 0, 0, 0, 0),
}
SIZES = (1, 1, 8, 8, 6, 6, 6, 12)
SIGMA = [np.array([[0, 1], [1, 0]], complex), np.array([[0, -1j], [1j, 0]]), np.diag([1.0 + 0j, -1.0])]
J_TWIN = np.array([[0, -1], [1, 0]], complex)


def class_of(m):
    """The class of a lift, exactly: its trace squared over its determinant, the trace's sign, and the turn."""
    t, d = gadd(m[0][0], m[1][1]), det(m)
    assert t[1] == 0 and d[1] == 0 and d[0] > 0
    ratio = t[0] * t[0] / d[0]
    if ratio == 0:
        r = rotation(m)
        return 6 if all(r[i][j] == 0 for i in range(3) for j in range(3) if i != j) else 7
    return {4: 0, 1: 2, 2: 4}[ratio] + (t[0] < 0)


def build(group):
    """Every kind built from the twins by meeting one more twin; returns the kinds and the meetings' maps."""
    labels = [class_of(m) for m in group]
    assert tuple(labels.count(c) for c in range(8)) == SIZES
    twins = [
        np.array([[complex(*x) for x in row] for row in m]) / np.sqrt(float(det(m)[0])) for m in group
    ]
    for u, c in zip(twins, labels, strict=True):
        assert abs(np.trace(u) - CHARACTERS["E1/2"][c]) < 1e-12

    def project(rep, kind):
        chi = CHARACTERS[kind]
        return chi[0] / 48 * sum(chi[c] * d for d, c in zip(rep, labels, strict=True))

    kinds = {"E1/2": {"rep": twins, "J": J_TWIN, "S": [s / 2 for s in SIGMA], "rung": 1}}
    meets, queue = {}, ["E1/2"]
    while queue:
        k = queue.pop(0)
        kd = kinds[k]
        size = kd["rep"][0].shape[0]
        rep = [np.kron(d, u) for d, u in zip(kd["rep"], twins, strict=True)]
        for k2 in CHARACTERS:
            p = project(rep, k2)
            if np.linalg.norm(p) < 1e-9:
                continue
            if k2 not in kinds:
                w, vecs = np.linalg.eigh(p)
                phi = vecs[:, w > 0.5]
                kinds[k2] = {
                    "rep": [phi.conj().T @ d @ phi for d in rep],
                    "J": phi.conj().T @ np.kron(kd["J"], J_TWIN) @ phi.conj(),
                    "S": [
                        phi.conj().T @ (np.kron(s, np.eye(2)) + np.kron(np.eye(size), t / 2)) @ phi
                        for s, t in zip(kd["S"], SIGMA, strict=True)
                    ],
                    "rung": kd["rung"] + 1,
                }
                queue.append(k2)
            else:
                d2 = kinds[k2]["rep"]
                a = (np.arange(2 * size * d2[0].shape[0]).reshape(2 * size, -1) + 1) * (1 + 0.5j)
                phi = sum(r @ a @ d.conj().T for r, d in zip(rep, d2, strict=True)) / 48
                gram = phi.conj().T @ phi
                assert gram[0, 0].real > 1e-9 and np.allclose(gram, gram[0, 0] * np.eye(len(gram)))
                phi = phi / np.sqrt(gram[0, 0].real)
            meets[(k, k2)] = phi
    for k, kd in kinds.items():
        for d, c in zip(kd["rep"], labels, strict=True):
            assert abs(np.trace(d) - CHARACTERS[k][c]) < 1e-9
            assert np.allclose(kd["J"] @ d.conj(), d @ kd["J"])
        for s in kd["S"]:
            assert np.allclose(kd["J"] @ s.conj(), -s @ kd["J"])
    return kinds, meets


def digits():
    """A fixed stream of fair bits: SHA-256 of the seed and a counter, 256 bits a block (the vernier's stand-in)."""
    count = 0
    while True:
        block = hashlib.sha256(f"{SEED}:{count}".encode()).digest()
        count += 1
        for byte in block:
            for i in range(8):
                yield (byte >> i) & 1


def uniforms():
    bits = digits()
    while True:
        yield sum(next(bits) << i for i in range(30)) / (1 << 30)


def twin(n, up):
    w, vecs = np.linalg.eigh(sum(c * s for c, s in zip(n, SIGMA, strict=True)))
    return vecs[:, 1] if up else vecs[:, 0]


KAPPA = {"axis": 0.0, "half": 0.5, "choice": 1.0, "against": -1.0}


def climb(rule, kinds, meets, draws):
    """One composite over the bangs: the kind after each bang and whether it holds a direction."""

    def fresh():
        axis = np.eye(3)[min(int(3 * next(draws)), 2)]
        return twin(axis, next(draws) < 0.5)

    def reading(kind, v):
        return np.array([np.vdot(v, s @ v).real for s in kinds[kind]["S"]])

    kind, v = "E1/2", fresh()
    path = [(kind, True)]
    for _ in range(2, BANGS + 1):
        if rule == "rewound":
            kind, v = "E1/2", fresh()
        elif FORMER:
            v = kinds[kind]["J"] @ v.conj()  # the former turnover; no act at the top (decision 27)
        s = reading(kind, v)
        if np.linalg.norm(s) > 1e-9:
            line, kappa = s / np.linalg.norm(s), KAPPA.get(rule, 0.0)
        else:
            line, kappa = np.eye(3)[min(int(3 * next(draws)), 2)], 0.0
        x = np.kron(v, twin(line, next(draws) < (1 + kappa) / 2))
        outcomes = [(k2, phi) for (k1, k2), phi in meets.items() if k1 == kind]
        parts = [phi.conj().T @ x for _, phi in outcomes]
        shares = [np.vdot(p, p).real for p in parts]
        assert abs(sum(shares) - 1) < 1e-9
        u, acc = next(draws), 0.0
        for (k2, _), p, share in zip(outcomes, parts, shares, strict=True):
            acc += share
            if u < acc or k2 == outcomes[-1][0]:
                kind, v = k2, p / np.sqrt(share)
                break
        path.append((kind, np.linalg.norm(reading(kind, v)) > 1e-9))
    return path


def main():
    rot = turns()
    tet = [g for g in rot if even(g)]
    group = lifts()
    assert len(group) == 48
    tet_lifts = [m for m in group if even(rotation(m))]
    print(
        "1. T, each kind's time reversal, keeps a kind exactly where every turn is conjugate to its own reverse"
        " (counted exactly)"
    )
    for name, (count, real) in (
        ("the 24 turns", classes_turns(rot)),
        ("their 48 lifts to the twins", classes_lifts(group)),
        ("the mutant: the tetrahedron's 12 turns", classes_turns(tet)),
        ("their 24 lifts", classes_lifts(tet_lifts)),
    ):
        print(f"   {name}: {count} kinds, {real} kept by T, {count - real} sent to another kind")
    for a in CHARACTERS.values():
        for b in CHARACTERS.values():
            dot = sum(n * x * y for n, x, y in zip(SIZES, a, b, strict=True))
            assert abs(dot - (48 if a is b else 0)) < 1e-9
    kinds, meets = build(group)
    print(
        "2. the kinds built from the twins, each by meeting one more twin (the traces match the characters)"
    )
    t1 = CHARACTERS["T1"]
    for k, kd in sorted(kinds.items(), key=lambda item: item[1]["rung"]):
        tt = np.real(kd["J"] @ kd["J"].conj())[0, 0]
        mult = sum(n * x * y * y for n, x, y in zip(SIZES, t1, CHARACTERS[k], strict=True)) / 48
        largest = max(abs(np.linalg.eigvalsh(kd["S"][2])))
        into = [k2 for (k1, k2) in meets if k1 == k]
        print(
            f"   {k:5s} rung {kd['rung']}, T T = {tt:+.0f}, T1 in K x K* {round(mult)} times, "
            f"largest |<S_z>| {largest:.3f}; with one more twin: {' or '.join(into)}"
        )
    print(
        f"3. one composite over {BANGS} bangs, {RUNS} runs per rule, seed {SEED}, "
        + ("the former turnover at the top" if FORMER else "no act at the top (decision 27)")
        + "; per bang: the share at the bang's new rung"
    )
    print(
        "   (bangs 1 to 6), the mean rung, the share holding a direction, and the share that has reached the top"
    )
    print("   kind (A2, rung 6) at least once")
    for rule in ("rewound", "against", "axis", "half", "choice"):
        draws = uniforms()
        paths = [climb(rule, kinds, meets, draws) for _ in range(RUNS)]
        top, mean, held, reached = [], [], [], []
        for b in range(BANGS):
            rungs = [kinds[p[b][0]]["rung"] for p in paths]
            if b < 6:
                top.append(sum(r == b + 1 for r in rungs) / RUNS)
            mean.append(sum(rungs) / RUNS)
            held.append(sum(p[b][1] for p in paths) / RUNS)
            reached.append(sum(any(k == "A2" for k, _ in p[: b + 1]) for p in paths) / RUNS)
        print(f"   {rule}:")
        print(f"     new rung    {' '.join(f'{x:.2f}' for x in top)}")
        print(f"     mean rung   {' '.join(f'{x:.2f}' for x in mean)}")
        print(f"     direction   {' '.join(f'{x:.2f}' for x in held)}")
        print(f"     reached A2  {' '.join(f'{x:.2f}' for x in reached)}")
        last = {k: sum(p[-1][0] == k for p in paths) / RUNS for k in CHARACTERS}
        print(
            f"     the kinds at bang {BANGS}: " + ", ".join(f"{k} {x:.2f}" for k, x in last.items() if x)
        )


if __name__ == "__main__":
    main()
