"""Toy: two boards on one Node-clock, one forward and one backward (decision 28), tested on one pair with two late
choosers (Animate; the owner's word to Animate of 2026-10-29, 08:4x UTC, in Hebrew, in translation: "Go with the
proposal, check it, and understand why it is two boards that help, and not a bang that keeps history: the swings, and
what the clicks do between the boards, by kind").

The pair is born at one Node-clock (the birth) as a singlet. Its twins ride a chain to two detectors, each choosing its
axis late, from its own digits, after the twins have left the birth. The axes are draft D's: a = z, a' = x,
b = (20, 0, 21) / 29 and b' = (-20, 0, 21) / 29, so the singlet gives S = -82/29. Every draw is law 9's: each part's
weight an integer, the digit d over [0, L), L the weights' sum, the part the rank count of d over the running sums.
Each law below is exact: every digit of every draw is enumerated, so each part is drawn exactly its weight's times.

The forms of the board:
  F  one forward board, the history kept: the twins carry a direction from the birth (law 6's twin pair with a
     definite direction), drawn by the birth's digits or carried from the last bang's record (the chosen path); each
     detector draws alone, its shares (1 +- s . m) / 2;
  O  two boards, ordered by the board's tick (David's 6491076850): the first click draws with a silent future, its
     outcome rides the backward board back along its twin to the birth and the forward board out along the other
     twin, where the second click draws over the products, sigma_b the Fierz sizes against -s a;
  U  two boards, no order: each click's sigma_b from the other's outcome, the history to agree with itself at both
     ends; the consistent histories counted at every pair of digits, and the sweeps from a silent future;
  B  two boards, the draw at the birth: the backward board carries both settings back along the twins to the birth,
     one draw there over the four parts (draft D's split, sigma_st proportional to 1 - s t a . b), and the forward
     board carries each twin's outcome out to its detector.
Then a loop (the second detector's setting chosen by the first's outcome), and one quantum spread over three
absorbers (Grangier's g2), each read under the forms.

usage: python -I two_boards.py
"""

import hashlib
import math
from fractions import Fraction as Q
from itertools import product

A_AXES = {"a": (0, 0, 1), "a'": (1, 0, 0)}
B_AXES = {"b": (20, 0, 21), "b'": (-20, 0, 21)}
PAIRS = [("a", "b"), ("a", "b'"), ("a'", "b"), ("a'", "b'")]  # S = E(a,b) + E(a,b') + E(a',b) - E(a',b')
SIGNS = (1, -1)  # the part along the axis, then the part against it
DIRECTIONS = [tuple(s * e for e in axis) for axis in ((1, 0, 0), (0, 1, 0), (0, 0, 1)) for s in (1, -1)]


def dot(u, v):
    return sum(p * q for p, q in zip(u, v, strict=True))


def norm(v):
    """The axis's length, a whole number: every axis here is Pythagorean."""
    n = math.isqrt(dot(v, v))
    assert n * n == dot(v, v)
    return n


def draw(weights, d):
    """Law 9: the part at digit d, the rank count of d over the weights' running sums."""
    total = 0
    for part, w in enumerate(weights):
        total += w
        if d < total:
            return part
    raise ValueError("a digit past the weights' sum")


def shares(weights):
    """Each part's share, by enumerating every digit of the draw: exactly its weight over the sum."""
    counts = [0] * len(weights)
    for d in range(sum(weights)):
        counts[draw(weights, d)] += 1
    return [Q(c, sum(weights)) for c in counts]


def correlation(law):
    return sum(s * t * p for (s, t), p in law.items())


def bell(laws):
    e = [correlation(laws[pair]) for pair in PAIRS]
    return e[0] + e[1] + e[2] - e[3], e


def marginals(law):
    """Each end's share of +."""
    return sum(p for (s, _), p in law.items() if s == 1), sum(p for (_, t), p in law.items() if t == 1)


def settings(pair):
    a, b = A_AXES[pair[0]], B_AXES[pair[1]]
    return a, b, norm(a) * norm(b), dot(a, b)


# F: one forward board, the history kept


def law_forward(pair):
    """The twins carry +-lambda from the birth, lambda one of the 24's six axis directions alike; each end draws alone."""
    a, b = A_AXES[pair[0]], B_AXES[pair[1]]
    law = {k: Q(0) for k in product(SIGNS, SIGNS)}
    for lam in DIRECTIONS:
        pa = shares([norm(a) + dot(lam, a), norm(a) - dot(lam, a)])
        pb = shares([norm(b) - dot(lam, b), norm(b) + dot(lam, b)])  # the other twin carries -lambda
        for (i, s), (j, t) in product(enumerate(SIGNS), enumerate(SIGNS)):
            law[(s, t)] += Q(1, len(DIRECTIONS)) * pa[i] * pb[j]
    return law


def local_bound():
    """Every forward-only history is a mixture of fixed answers per setting, chosen before the late settings."""
    best = 0
    for sa, sa2, tb, tb2 in product(SIGNS, repeat=4):
        best = max(best, abs(sa * tb + sa * tb2 + sa2 * tb - sa2 * tb2))
    return best


def stream(label):
    """A fixed stream of fair digits, SHA-256 of a label and a counter (the vernier's stand-in)."""
    count = 0
    while True:
        block = hashlib.sha256(f"{label}:{count}".encode()).digest()
        count += 1
        yield from block


def digit(source, below):
    """A digit below the bound, from 4 bytes of the stream, by rejection so that it stays fair."""
    span = 1 << 32
    while True:
        x = int.from_bytes(bytes(next(source) for _ in range(4)), "big")
        if x < span - span % below:
            return x % below


def bangs_with_history(count):
    """Bang after bang, each pair's lambda the last bang's record at A (the chosen path); the settings late and alone."""
    birth, at_a, at_b, pick_a, pick_b = (
        stream(name) for name in ("birth", "A", "B", "choose A", "choose B")
    )
    lam = DIRECTIONS[digit(birth, len(DIRECTIONS))]
    tally = {pair: {k: 0 for k in product(SIGNS, SIGNS)} for pair in PAIRS}
    for _ in range(count):
        pa_name, pb_name = ("a", "a'")[digit(pick_a, 2)], ("b", "b'")[digit(pick_b, 2)]
        a, b = A_AXES[pa_name], B_AXES[pb_name]
        wa = [norm(a) + dot(lam, a), norm(a) - dot(lam, a)]
        wb = [norm(b) - dot(lam, b), norm(b) + dot(lam, b)]
        s = SIGNS[draw(wa, digit(at_a, sum(wa)))]
        t = SIGNS[draw(wb, digit(at_b, sum(wb)))]
        tally[(pa_name, pb_name)][(s, t)] += 1
        lam = tuple(s * e for e in a)  # the record A's click wrote: the next bang's twin direction
    laws = {pair: {k: Q(n, sum(t.values())) for k, n in t.items()} for pair, t in tally.items()}
    return laws


# O: two boards, ordered by the board's tick


def law_ordered(pair, first="A"):
    """The first click draws with a silent future; the second over the products, sigma_b against -s times the first axis."""
    _, _, n, ab = settings(pair)
    law = {}
    for i, s in enumerate(SIGNS):
        p_first = shares([1, 1])[i]  # sigma_f alike (the singlet's twin) times a silent sigma_b
        second = shares(
            [n - s * ab, n + s * ab]
        )  # the Fierz sizes of the second detector against -s (first axis)
        for j, t in enumerate(SIGNS):
            law[(s, t) if first == "A" else (t, s)] = p_first * second[j]
    return law


# U: two boards, no order


def unordered(pair):
    """Every pair of digits: the consistent histories, the sweeps from a silent future, and the law under a fair choice."""
    _, _, n, ab = settings(pair)
    given = {
        r: [n - r * ab, n + r * ab] for r in SIGNS
    }  # an end's weights given the other end's outcome r
    silent, size = [n, n], 2 * n
    count = {0: 0, 1: 0, 2: 0}
    jacobi = {"settles": 0, "cycles": 0}
    law = {k: Q(0) for k in product(SIGNS, SIGNS)}
    for da, db in product(range(size), range(size)):
        found = [
            (s, t)
            for s, t in product(SIGNS, SIGNS)
            if SIGNS[draw(given[t], da)] == s and SIGNS[draw(given[s], db)] == t
        ]
        count[len(found)] += 1
        for k in found:
            law[k] += Q(1, len(found) * size * size)
        s, t = SIGNS[draw(silent, da)], SIGNS[draw(silent, db)]
        seen = []
        while (s, t) not in seen:
            seen.append((s, t))
            s, t = SIGNS[draw(given[t], da)], SIGNS[draw(given[s], db)]
        jacobi["settles" if seen[-1] == (s, t) else "cycles"] += 1
    return count, jacobi, law, size * size


# B: two boards, the draw at the birth


def law_birth(pair, order=((1, 1), (1, -1), (-1, 1), (-1, -1))):
    """One draw at the birth over the four parts, each weight n - s t (a . b), the settings carried back to it."""
    _, _, n, ab = settings(pair)
    weights = [n - s * t * ab for s, t in order]
    return dict(zip(order, shares(weights), strict=True))


CAUSAL = ((1, 1), (1, -1), (-1, 1), (-1, -1))  # the four parts, the first end's outcome outer
CROSSED = ((1, 1), (-1, 1), (1, -1), (-1, -1))  # the second end's outcome outer


def loop(first_setting="a'", order=CAUSAL):
    """The second detector's setting chosen by the first's outcome: b' after +, b after -. Under B, a history must
    agree with itself: the draw at the birth under the setting its own outcome chooses. Counted at every digit, with
    the law of the histories where one agrees; and the same loop under O, the first click first."""
    chosen = {1: "b'", -1: "b"}
    tables = {}
    for s in SIGNS:
        _, _, n, ab = settings((first_setting, chosen[s]))
        tables[s] = [n - x * y * ab for x, y in order]
    assert sum(tables[1]) == sum(tables[-1])
    size = sum(tables[1])
    count = {0: 0, 1: 0, 2: 0}
    law = {k: Q(0) for k in product(SIGNS, SIGNS)}
    for d in range(size):
        found = [order[draw(tables[s], d)] for s in SIGNS if order[draw(tables[s], d)][0] == s]
        count[len(found)] += 1
        for k in found:
            law[k] += Q(1, size) if len(found) == 1 else 0
    ordered = {}
    for i, s in enumerate(SIGNS):
        _, _, n, ab = settings((first_setting, chosen[s]))
        second = shares([n - s * ab, n + s * ab])
        for j, t in enumerate(SIGNS):
            ordered[(s, t)] = shares([1, 1])[i] * second[j]
    return count, size, law, ordered


# one quantum over three absorbers (Grangier)


def grangier(sizes=(5, 3, 2)):
    """F: each absorber clicks alone at its own share; B: one draw at the source over the absorbers' sizes, carried back."""
    total = sum(sizes)
    alone = [Q(w, total) for w in sizes]
    none = math.prod(1 - p for p in alone)
    one = sum(p * math.prod(1 - q for k, q in enumerate(alone) if k != i) for i, p in enumerate(alone))
    two_or_more = 1 - none - one
    at_source = shares(list(sizes))
    return alone, two_or_more, at_source


def fmt(law):
    return ", ".join(f"({s:+d},{t:+d}) {p}" for (s, t), p in sorted(law.items(), reverse=True))


def show(name, law):
    s, e = bell(law)
    print(f"  {name}: S = {s} = {float(s):.4f}; E = {', '.join(str(x) for x in e)}")


def main():
    print(
        "one pair born at one Node-clock, two detectors choosing late; draft D's axes; every draw enumerated whole"
    )
    print()
    print("F, one forward board, the history kept")
    show("the twins' direction drawn at the birth", {pair: law_forward(pair) for pair in PAIRS})
    print(
        f"  every forward-only history, at most: |S| = {local_bound()} (the 16 fixed answers per setting, exhausted)"
    )
    for count in (4096, 65536):
        s, _ = bell(bangs_with_history(count))
        print(
            f"  the twins' direction the last bang's record (the chosen path), {count} bangs: S = {float(s):.4f}"
        )
    print()
    print("O, two boards, ordered by the board's tick")
    a_first = {pair: law_ordered(pair, "A") for pair in PAIRS}
    show("A first", a_first)
    print(f"  B first gives the same law: {a_first == {pair: law_ordered(pair, 'B') for pair in PAIRS}}")
    print(
        "  the marginals, every setting: "
        + "; ".join(
            f"{p[0]},{p[1]}: {marginals(a_first[p])[0]}, {marginals(a_first[p])[1]}" for p in PAIRS
        )
    )
    print(
        "  one history at every digit; the second twin holds the first outcome from the first click's tick on"
    )
    print()
    print("U, two boards, no order: the consistent histories at every pair of digits")
    laws = {}
    for pair in PAIRS:
        count, jacobi, law, size = unordered(pair)
        laws[pair] = law
        x = Q(settings(pair)[3], settings(pair)[2])
        print(
            f"  {pair[0]},{pair[1]} (a . b = {x}): of {size} digit pairs, {count[0]} with none, {count[1]} with one, "
            f"{count[2]} with two ({Q(count[2], size)}, (a . b)^2 = {x * x}); the sweeps from a silent future settle "
            f"at {jacobi['settles']} and cycle at {jacobi['cycles']}"
        )
    show("a fair choice where two agree", laws)
    print(
        "  the marginals: "
        + "; ".join(f"{p[0]},{p[1]}: {marginals(laws[p])[0]}, {marginals(laws[p])[1]}" for p in PAIRS)
    )
    print(f"  Tsirelson's bound, nature's largest: |S| at most 2 sqrt 2 = {2 * math.sqrt(2):.4f}")
    print()
    print("B, two boards, the draw at the birth (the settings carried back, the outcomes carried out)")
    births = {pair: law_birth(pair) for pair in PAIRS}
    show("one draw over the four parts", births)
    reordered = {pair: law_birth(pair, ((-1, -1), (-1, 1), (1, -1), (1, 1))) for pair in PAIRS}
    print(
        f"  the four parts in another order give the same law: {births == reordered}; equal to O's: {births == a_first}"
    )
    print(
        "  the marginals: "
        + "; ".join(
            f"{p[0]},{p[1]}: {marginals(births[p])[0]}, {marginals(births[p])[1]}" for p in PAIRS
        )
    )
    print("  one history at every digit; each twin carries only its own outcome, out from the birth")
    print()
    print(
        "a loop: the second setting chosen by the first outcome (b' after +, b after -), the first setting a'"
    )
    for name, order in (
        ("the first end's outcome outer (the cause's order)", CAUSAL),
        ("the second's outer", CROSSED),
    ):
        count, size, law, ordered = loop(order=order)
        print(
            f"  under B, the four parts with {name}: of {size} digits at the birth, {count[0]} with no consistent "
            f"history, {count[1]} with one, {count[2]} with two"
        )
        if count[1] == size:
            print(f"    its law {fmt(law)}, equal to O's: {law == ordered}")
    print(f"  under O, the first click first: one history at every digit, the law {fmt(ordered)}")
    print()
    print("one quantum over three absorbers, sizes 5, 3 and 2 (Grangier)")
    alone, two_or_more, at_source = grangier()
    print(
        f"  F, each absorber alone at its share {', '.join(str(p) for p in alone)}: two or more click at once with "
        f"odds {two_or_more} = {float(two_or_more):.3f} (g2 above 0)"
    )
    print(
        f"  B, one draw at the source over the sizes carried back: each absorber's odds "
        f"{', '.join(str(p) for p in at_source)}, and two never click at once (g2 = 0)"
    )


if __name__ == "__main__":
    main()
