"""Two boards against one, on a toy of swings: does the backward board make the clocks grow more complex, or does the
past alone, through what passes each bang? Every weight a whole number; Fractions for the exact laws.

The toy: a ring of L sites, a bond between each pair of neighbours. Each swing: in its expansion every open bond is
laid by a split click of three outcomes, weak, medium or strong, at the forward sizes SF = (4, 2, 1); at its bang the
sieve breaks every weak bond, a medium bond on a coin, and no strong bond; what survives passes to the next swing
(the records). Complexity per swing: the largest composite (the longest run of bonds), and the composites of four or
more. Four runs:
  forward: the forward board alone (the old reading: the past drives);
  two boards: the backward board carries each bond's own future (survived or broken at the next bang) back, and the
    split click draws over the product SF x SB, SB the likelihood of that future: the history agreeing with itself;
  imposed: the backward board starting from a future set by hand, every bond surviving (a declared goal, refused by
    the law, run as the control that shows what a special future would do);
  reset: nothing passes the bang (the control with no ratchet).
"""

import sys
from fractions import Fraction

import numpy as np

SF = (4, 2, 1)  # weak, medium, strong
SURVIVE = (Fraction(0), Fraction(1, 2), Fraction(1))  # the sieve's odds per strength at the bang


def exact():
    """The laws in Fractions: each strength's odds and the survival per bond per swing, under each run."""
    total = sum(SF)
    sf = [Fraction(f, total) for f in SF]
    forward = sum(f * p for f, p in zip(sf, SURVIVE))
    # two boards: the future drawn by the process itself (P(survive) = forward), each strength drawn over
    # SF x P(future | strength); the history agrees with itself, so a bond survives where its future says it does
    odds = [Fraction(0)] * 3
    for future, p_future in ((1, forward), (0, 1 - forward)):
        w = [f * (p if future else 1 - p) for f, p in zip(sf, SURVIVE)]
        odds = [o + p_future * x / sum(w) for o, x in zip(odds, w)]
    w = [f * p for f, p in zip(sf, SURVIVE)]  # imposed: every bond's future set to survival by hand
    imposed_odds = [x / sum(w) for x in w]
    return sf, forward, odds, forward, imposed_odds, Fraction(1)


def swing(rng, bonds, run):
    """One swing: open bonds laid by the split click, then the bang's sieve; the bonds that pass, and the laid ones."""
    open_ = bonds == 0
    n = int(open_.sum())
    coins = rng.integers(0, 2, n)  # the bang's coin for a medium bond, drawn with the bond
    total = sum(SF)
    if run == "forward" or run == "reset":
        laid = rng.choice(3, size=n, p=[f / total for f in SF]) + 1
    elif run == "two boards":
        first = rng.choice(3, size=n, p=[f / total for f in SF]) + 1  # the forward board's history
        future = (first == 3) | ((first == 2) & (coins == 1))  # each bond's future, the backward board's start
        laid = np.empty(n, dtype=int)
        for fut in (True, False):
            sb = [float(p) if fut else 1 - float(p) for p in SURVIVE]
            w = np.array([f * b for f, b in zip(SF, sb)], dtype=float)
            idx = np.flatnonzero(future == fut)
            laid[idx] = rng.choice(3, size=len(idx), p=w / w.sum()) + 1
        # the history agrees with itself: each laid bond keeps the future it was drawn under
        coins = np.where(laid == 2, future.astype(int), coins)
    else:  # imposed
        w = np.array([f * float(p) for f, p in zip(SF, SURVIVE)])
        laid = rng.choice(3, size=n, p=w / w.sum()) + 1
        coins = np.ones(n, dtype=int)
    bonds = bonds.copy()
    bonds[open_] = laid
    survive = (bonds == 3) | ((bonds == 2) & np.isin(np.arange(len(bonds)), np.flatnonzero(open_)[coins == 1]))
    survive |= (bonds == 2) & ~open_  # a medium bond that passed an earlier bang stays: it passed its own sieve
    if run == "reset":
        survive[:] = False
    return np.where(survive, bonds, 0)


def runs_of(bonds):
    """The composites: the runs of bonds around the ring, each run of k bonds a composite of k + 1 units."""
    if bonds.all():
        return [len(bonds)]
    b = np.roll(bonds, -int(np.flatnonzero(bonds == 0)[0]))
    out, cur = [], 0
    for x in b:
        if x:
            cur += 1
        elif cur:
            out.append(cur)
            cur = 0
    if cur:
        out.append(cur)
    return out


def main(L=96, swings=12, seeds=400):
    sf, forward, odds, two, imposed_odds, imposed = exact()
    show = lambda xs: "(" + ", ".join(str(x) for x in xs) + ")"
    print(f"exact, each strength's odds (weak, medium, strong): forward {show(sf)}; two boards {show(odds)}; imposed {show(imposed_odds)}")
    print(f"exact, the survival per bond per swing: forward {forward}; two boards {two}; imposed {imposed} (set by hand)")
    for run in ("forward", "two boards", "imposed", "reset"):
        big = np.zeros(swings)
        four = np.zeros(swings)
        for seed in range(seeds):
            rng = np.random.default_rng(seed)
            bonds = np.zeros(L, dtype=int)
            for k in range(swings):
                bonds = swing(rng, bonds, run)
                r = runs_of(bonds)
                big[k] += max(r, default=0)
                four[k] += sum(1 for x in r if x + 1 >= 4)
        print(f"{run:>10}: the largest composite per swing (mean of {seeds} seeds): " + " ".join(f"{x / seeds:5.1f}" for x in big))
        print(f"{'':>10}  composites of 4 or more per swing:            " + " ".join(f"{x / seeds:5.1f}" for x in four))


if __name__ == "__main__":
    main(*map(int, sys.argv[1:]))
