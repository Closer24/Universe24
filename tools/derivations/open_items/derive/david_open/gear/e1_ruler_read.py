"""(e), the ruler's read exact and computed: the ruler carried as its own dial, (X, r), stepped with the load.

The loader walks the ruler once into a table (ruler_of): up one load is one carry, X Gamma + r = X+ (Gamma - 1) + r+,
the read at a load being X rounded at the resolution Gamma^2. Here the same carry is taken at the tick instead, up
one load where the time gear's count rises and its inverse, X (Gamma - 1) + r = X- Gamma + r-, where it falls.

Checks, all on integers:
  1. the dial walked up from the seed's start equals the loader's table entry by entry;
  2. it runs on past the table's last entry: no cap, no table;
  3. along any walk of the load at or above the start, with strides -1, 0 and +1, the dial at each load is the
     chain's, and the walk run back returns every state exactly;
  4. two descents below the start do not run back: the remainder of the first descent can be Gamma - 1, one
     past the next descent's range (the start is a floor unless the run never goes below it);
  5. a stride of two notches in one carry, at the ratio (Gamma + 2) / Gamma and its inverse, leaves the chain:
     the read follows the load only at a stride of at most one notch per tick;
  6. the step in the closed list, one carry with the multiplier Gamma - 1 + u and the teeth Gamma - 1 + d, where
     u = (q q + q) div 2 and d = (q q - q) div 2 are the bits of q = +1 and q = -1, equals the three carries
     (up, down, held) at every state of the chain and every stride -1, 0, +1.

Usage: python3 -I e1_ruler_read.py <src of tensor24-review>
"""

import random
import sys

sys.path.insert(0, sys.argv[1])
from tensor24.runner.load import rounded, ruler_of  # noqa: E402


def up(x, r, g):
    return divmod(x * g + r, g - 1)


def down(x, r, g):
    return divmod(x * (g - 1) + r, g)


def stepped(x, r, g, q):
    u, d = (q * q + q) // 2, (q * q - q) // 2
    return divmod(x * (g - 1 + u) + r, g - 1 + d)


def start(g):
    return g * g * g, (g - 1) // 2  # the loader's hill and hill tooth at the load 0


def main():
    g = 1000
    table = ruler_of(g)
    x, r = start(g)
    same = True
    for n, entry in enumerate(table):
        same = same and rounded(x, g * g) == entry
        x, r = up(x, r, g)
    print(f"1. Gamma {g}: the dial walked up equals the loader's table at all {len(table)} loads: {same}")
    for _ in range(4 * len(table)):
        x, r = up(x, r, g)
    print(f"2. past the table's last load, {5 * len(table)} loads up: Y = {rounded(x, g * g)}, "
          f"{x.bit_length()} bits; nothing stops the walk")

    rng = random.Random(29)
    for g in (7, 1000):
        chain = [start(g)]
        for _ in range(400):
            chain.append(up(*chain[-1], g))
        load, state, path = 0, chain[0], []
        on_chain = True
        for _ in range(20000):
            q = rng.choice((-1, 0, 1))
            if load + q < 0 or load + q >= len(chain):
                q = 0
            new = up(*state, g) if q == 1 else down(*state, g) if q == -1 else state
            path.append((q, state))
            load, state = load + q, new
            on_chain = on_chain and state == chain[load]
        back = state
        for q, before in reversed(path):
            back = down(*back, g) if q == 1 else up(*back, g) if q == -1 else back
            assert back == before
        print(f"3. Gamma {g}: 20,000 ticks at strides -1, 0, +1 above the start; the dial is the chain's at every "
              f"load: {on_chain}; run back to the start exactly: {back == chain[0]}")

    g = 7
    found = None
    for x0 in range(g * g * g, g * g * g + 200):
        for r0 in range(g - 1):
            once = down(x0, r0, g)
            twice = down(*once, g)
            if up(*twice, g) != once:
                found = (x0, r0, once, twice, up(*twice, g))
                break
        if found:
            break
    x0, r0, once, twice, back = found
    print(f"4. Gamma {g}: from the dial ({x0}, {r0}) one load down gives {once}, its remainder Gamma - 1; a "
          f"second load down gives {twice}, and up again gives {back}, not {once}")

    g = 1000
    x, r = start(g)
    one = up(*up(x, r, g), g)
    two = divmod(x * (g + 2) + r, g)
    print(f"5. Gamma {g}: two loads in two carries give X {one[0]}; in one carry at (Gamma + 2) / Gamma, "
          f"X {two[0]}: off the chain by {two[0] - one[0]}")

    same, cases = True, 0
    for g in (7, 1000):
        state = start(g)
        for _ in range(500):
            for q in (-1, 0, 1):
                three = up(*state, g) if q == 1 else down(*state, g) if q == -1 else state
                same = same and stepped(*state, g, q) == three
                cases += 1
            state = up(*state, g)
    print(f"6. the one carry with u and d from the stride equals the three carries in all {cases} cases: {same}")


if __name__ == "__main__":
    main()
