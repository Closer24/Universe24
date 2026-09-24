"""Row 1c's order channel: the test of the hidden residue, PREPARED, NOT DECLARED (the model
owner's word of 2026-09-24, 03:14Z, "make preparations for the above test", on the answer to his
question "the algebra does not solve it; what does?"; DECLARATIONS.md section 2 item 8; his word
on the declaration pending). COMPUTATION on the declared ladder of `order_channel_pins.py`; no
run, no pin moved; nothing here enters a GO world.

(a) AS DECLARED (the counter family [1, 1]): the birth residue u is the birth index, so B's click
list in birth order is the list in residue order, and B reads A's setting from his own list alone
at b = 3 N / 8: the fraction of + among his first N / 4 births (0.293 at a = 0, 1.000 at a = N /
4), the whole list four runs; a decoder fixed before the run reads a with certainty.
(b) UNDER A SEED-SET ORDER (the births take the residues of Z_N in the order of a permutation
drawn from the world's seed by an integer hash: here a Fisher-Yates shuffle driven by a 64-bit
mixing hash of SplitMix64's form, plain integers, the engine's form the builder's on the owner's
word): the same decoders read about 1 / 2 for either setting of A over many seeds; the lists
still differ on E_N of the births for a reader who holds the residues (Inside, Bell's theorem),
and the counts are N / 2 exactly either way.
(c) THE THEOREM (exact for a uniformly random order; the seed-set shuffle its integer form,
closed to a reader without the seed): B's list at fixed b is a
balanced multiset (N / 2 pluses for either a) in a uniformly random order, so its distribution is
the uniform distribution over balanced strings for a and for a' alike; no decoder fixed before the
run, without the seed, does better than 1 / 2. (b) checks it on two decoders.

    PYTHONPATH=src python docs/designs/detector_law/order_channel_hidden_pins.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from order_channel_pins import o_b, table  # noqa: E402

MASK = (1 << 64) - 1


def mix64(state):
    """One output of a 64-bit mixing hash (SplitMix64's form: a Weyl step, then two xor-shift
    multiplies), plain integers; every bit of the output depends on every bit of the state, unlike
    a linear congruential generator, whose low bits cycle. Returns the new state and the output."""
    state = (state + 0x9E3779B97F4A7C15) & MASK
    z = state
    z = ((z ^ (z >> 30)) * 0xBF58476D1CE4E5B9) & MASK
    z = ((z ^ (z >> 27)) * 0x94D049BB133111EB) & MASK
    return state, z ^ (z >> 31)


def permutation(n, seed):
    """A Fisher-Yates shuffle of range(n) driven by the mixing hash seeded with the world's seed:
    the integer form of a uniformly random order, closed to a reader without the seed (the engine's
    form is the builder's under the same requirement, a keyed permutation indistinguishable from
    uniform without its key)."""
    order = list(range(n))
    state = seed & MASK
    for i in range(n - 1, 0, -1):
        state, out = mix64(state)
        j = out % (i + 1)
        order[i], order[j] = order[j], order[i]
    return order


def b_lists(n):
    """B's outcome per residue u at b = 3 N / 8 for a = 0 (key 0) and a = N / 4 (key 1)."""
    t = table(n)
    return {0: [o_b(c) for c in t[(0, 3)]], 1: [o_b(c) for c in t[(1, 3)]]}


def first_quarter(seq):
    q = len(seq) // 4
    return sum(x > 0 for x in seq[:q]) / q


def runs(seq):
    return 1 + sum(seq[i] != seq[i - 1] for i in range(1, len(seq)))


def lag_one(seq):
    """The fraction of neighbouring births with the same outcome (an autocorrelation decoder)."""
    return sum(seq[i] == seq[i - 1] for i in range(1, len(seq))) / (len(seq) - 1)


def halves(seq):
    """The + fraction of the first half less the second half's (a drift decoder)."""
    h = len(seq) // 2
    return (sum(x > 0 for x in seq[:h]) - sum(x > 0 for x in seq[h:])) / h


# The battery of decoders fixed before the run, each a statistic of B's list alone and a rule
# "guess a = N / 4 when the statistic is above its midpoint between the two declared-order values";
# under a seed-set order each is expected right on 1 / 2 of the trials.
DECODERS = {
    "first quarter": (first_quarter, 0.5),
    "threshold": (first_quarter, (0.293 + 1.0) / 2),
    "runs (few = the declared order)": (lambda s: -runs(s), -100.0),
    "lag-one sameness": (lag_one, 0.5),
    "halves' drift": (halves, 0.0),
}


if __name__ == "__main__":
    for n in (64, 256, 2048):
        lists = b_lists(n)
        flips = sum(x != y for x, y in zip(lists[0], lists[1], strict=True))
        counts = {a: sum(x > 0 for x in lists[a]) for a in (0, 1)}
        print(f"N = {n}: the counts of + at b = 3N/8 {counts[0]} and {counts[1]} of {n} (exact);")
        print(
            f"   with the residues known the two lists differ on {flips} of {n} births"
            f" = {flips / n:.5f} (E_N; Inside, Bell's theorem)"
        )
        # (a) as declared: the birth order is the residue order
        print("   (a) AS DECLARED, the counter family [1, 1] (the birth order the residue order):")
        for a in (0, 1):
            s = lists[a]
            print(
                f"       a = {'0' if a == 0 else 'N/4'}: the + fraction among B's first N/4 births"
                f" {first_quarter(s):.3f}; runs in the whole list {runs(s)}"
            )
        # (b) under a seed-set order: the decoders fixed before the run
        seeds = range(1, 201)
        hits = dict.fromkeys(DECODERS, 0)
        for seed in seeds:
            perm = permutation(n, seed)
            for a in (0, 1):
                s = [lists[a][u] for u in perm]
                for name, (stat, mid) in DECODERS.items():
                    hits[name] += int((stat(s) > mid) == (a == 1))
        trials = 2 * len(seeds)
        summary = "; ".join(f"{name} {h} of {trials} ({h / trials:.3f})" for name, h in hits.items())
        print(
            f"   (b) UNDER A SEED-SET ORDER (the mixing hash), {len(seeds)} seeds, the decoders fixed"
            f" before the run, each right on: {summary}; the runs about {n // 2} (the balanced"
            f" string's own)"
        )
    print(
        "(c) THE THEOREM: for a uniformly random permutation of the births, B's list at fixed b is"
        " a balanced multiset (N/2 pluses for either a) in uniformly random order, so its"
        " distribution is the uniform distribution over balanced strings for a and for a' alike;"
        " no decoder fixed before the run, without the seed, does better than 1/2: exact for a"
        " uniformly random order; the seed-set shuffle is its integer form, closed to a reader without"
        " the seed. The Inside dependence (E_N of the residues) is Bell's theorem and stays."
    )
