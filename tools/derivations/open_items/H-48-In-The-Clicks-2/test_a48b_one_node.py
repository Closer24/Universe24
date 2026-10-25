"""a48b's one-Node test: the carries of a reversed line's remainder and the digit that is even under them, in integers.

(1) The ones' complement commutes with the floor division (the law's theorem): floor((w - 1 - u) / w) = -floor(u / w).
(2) A remainder born at the half wall of an even wall is not its own ones' complement (w - 1 - w/2 = w/2 - 1) and is its own two's complement ((w - w/2) mod w = w/2): the lay's gauge.
(3) The riding division at the mean wall with the carry W div 2 sends p -> -p to rem -> (W - rem) mod W, except at the tie p + W div 2 = 0 mod W.
(4) The swap's ones' complement of a two's-complement image is w - 2 - (the swapped base): the turn-parity carry.
(5) On the lattice F | W with F | W div 2, a remainder's residue mod F stays in {0, F - 1} under the riding division (F | every force term) and flips under the swap; the lattice digit delta = (r + F - 1) div F folded by the two's complement, min(delta, W div F - delta), is equal at r and at its carry in both parities, where the ones' complement fold min(r, W - 1 - r) div F is not.
Run: python test_a48b_one_node.py  (exit 0 on pass; every check a count).
"""
import random
import sys

sys.set_int_max_str_digits(0)


def ones(r, w):
    return w - 1 - r


def twos(r, w):
    return (w - r) % w


def parity_carry(r, w, turns):
    return twos(r, w) if turns % 2 == 0 else (w - 2 - r) % w


def riding(p, W):
    """The riding division at the mean wall W with the carry W div 2: the quotient and the remainder."""
    u = p + W // 2
    return u // W, u % W


def fold_ones(r, w, F):
    return min(r, w - 1 - r) // F


def fold_lattice(r, w, F):
    values = w // F
    delta = (r + F - 1) // F
    return min(delta, values - delta)


def main():
    rng = random.Random(48)
    counts = {}
    # (1)
    n = 0
    for _ in range(20000):
        w = rng.randrange(2, 10**12)
        u = rng.randrange(-10**15, 10**15)
        n += (w - 1 - u) // w == -(u // w)
    counts["ones' complement commutes with the floor"] = (n, 20000)
    # (2)
    n2 = n3 = 0
    for _ in range(20000):
        w = 2 * rng.randrange(1, 10**12)
        h = w // 2
        n2 += ones(h, w) != h
        n3 += twos(h, w) == h
    counts["half wall not its own ones' complement"] = (n2, 20000)
    counts["half wall its own two's complement"] = (n3, 20000)
    # (3)
    n4 = ties = 0
    for _ in range(20000):
        W = 2 * rng.randrange(1, 10**12)
        p = rng.randrange(-10**14, 10**14)
        q, r = riding(p, W)
        q2, r2 = riding(-p, W)
        if (p + W // 2) % W == 0:
            ties += 1
            continue
        n4 += (r2 == twos(r, W)) and (q2 == -q)
    counts["riding division: p -> -p gives rem -> (W - rem) mod W and q -> -q off the tie"] = (n4, 20000 - ties)
    counts["ties met"] = (ties, 20000)
    # (4)
    n5 = 0
    for _ in range(20000):
        w = 2 * rng.randrange(2, 10**12)
        r = rng.randrange(1, w - 1)
        n5 += ones(twos(r, w), w) == (w - 2 - ones(r, w)) % w
    counts["swap after the two's carry is w - 2 - r"] = (n5, 20000)
    # (5) the residue and the folds on the lattice
    n6 = n7 = n8 = n9 = 0
    trials = 20000
    for _ in range(trials):
        F = rng.randrange(2, 10**6)
        values = 2 * rng.randrange(2, 10**6)  # W / F even so that F | W / 2
        W = F * values
        parity = rng.randrange(2)
        q = rng.randrange(0, values)
        r = q * F if parity == 0 else q * F + F - 1  # the residue by the turn parity
        # the riding division keeps the residue: the force a multiple of F
        p = W * rng.randrange(-3, 4) + r - W // 2 + F * rng.randrange(-10**6, 10**6)
        _q, r_next = riding(p, W)
        n6 += (r_next % F) == (r % F)
        rc = parity_carry(r, W, parity)
        n7 += (rc % F) == (r % F)
        n8 += fold_lattice(r, W, F) == fold_lattice(rc, W, F)
        n9 += fold_ones(r, W, F) == fold_ones(rc, W, F)
    counts["residue kept by the riding division"] = (n6, trials)
    counts["residue kept by the parity carry"] = (n7, trials)
    counts["lattice fold equal at r and its carry"] = (n8, trials)
    counts["ones' fold equal at r and its carry (not the mend)"] = (n9, trials)
    ok = True
    for k, (a, b) in counts.items():
        print(f"{k}: {a} of {b}")
    expect_full = ["ones' complement commutes with the floor", "half wall not its own ones' complement", "half wall its own two's complement",
                   "riding division: p -> -p gives rem -> (W - rem) mod W and q -> -q off the tie", "swap after the two's carry is w - 2 - r",
                   "residue kept by the riding division", "residue kept by the parity carry", "lattice fold equal at r and its carry"]
    for k in expect_full:
        ok = ok and counts[k][0] == counts[k][1]
    ok = ok and counts["ones' fold equal at r and its carry (not the mend)"][0] < counts["ones' fold equal at r and its carry (not the mend)"][1] // 2
    print("PASS" if ok else "FAIL")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
