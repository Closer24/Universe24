"""The discrete chain rule of the time gear's push per notch, exact in fractions on random whole-number fields.

usage: python -I chain_rule.py <runs> <seed>   (the recorded run: 40 20261029, chain_rule.txt)

The push per notch of a field Y on the torus, by the six neighbours' second difference D and the three centred
differences G (the act's own readings): n = 0: p(Y) = sum over the axes of D Y / Y - (G Y / Y)^2, the Y lap(ln Y) / Y
of Postulate 6; the head's law: q(Y) = sum over the axes of D Y / Y + 3 (G Y / Y)^2. For a product P = Y1 Y2 of two
fields, with a = D Y1 / Y1, u = G Y1 / Y1 and b, v the same for Y2, per axis:

    p(P) = p(Y1) + p(Y2) + E,      E = sum of  a b / 2 - (u + v) c - c^2 / 4,
    q(P) = q(Y1) + q(Y2) + H,      H = sum of  8 u v + a b / 2 + 3 (u + v) c + 3 c^2 / 4,        c = u b + v a

both exact (each neighbour is the value plus or minus the centred difference plus half the second difference, exactly),
so the composition test needs no lattice spacing, no bound and no smooth field. Two mutants of E must fail at every site.
"""

import random
import sys
from fractions import Fraction

SHAPE = (3, 4, 5)
AXES = range(3)


def sites():
    return [(x, y, z) for x in range(SHAPE[0]) for y in range(SHAPE[1]) for z in range(SHAPE[2])]


def step(site, axis, move):
    moved = list(site)
    moved[axis] = (moved[axis] + move) % SHAPE[axis]
    return tuple(moved)


def second(field, site, axis):
    return field[step(site, axis, 1)] + field[step(site, axis, -1)] - 2 * field[site]


def centred(field, site, axis):
    return Fraction(field[step(site, axis, 1)] - field[step(site, axis, -1)], 2)


def push(field, site, weight):
    """The sum over the axes of D Y / Y + weight (G Y / Y)^2: weight -1 is n = 0, weight 3 the head's law."""
    y = field[site]
    return sum(Fraction(second(field, site, k), y) + weight * (centred(field, site, k) / y) ** 2 for k in AXES)


def readings(one, two, site, k):
    a, u = Fraction(second(one, site, k), one[site]), centred(one, site, k) / one[site]
    b, v = Fraction(second(two, site, k), two[site]), centred(two, site, k) / two[site]
    return a, u, b, v, u * b + v * a


def remainders(one, two, site):
    """E, the first mutant (the c^2 / 4 term dropped) and the second (the sign of the middle term turned), and H."""
    exact = dropped = turned = head = Fraction(0)
    for k in AXES:
        a, u, b, v, c = readings(one, two, site, k)
        exact += a * b / 2 - (u + v) * c - c * c / 4
        dropped += a * b / 2 - (u + v) * c
        turned += a * b / 2 + (u + v) * c - c * c / 4
        head += 8 * u * v + a * b / 2 + 3 * (u + v) * c + 3 * c * c / 4
    return exact, dropped, turned, head


def main(runs: int, seed: int) -> None:
    rng = random.Random(seed)
    read = held = parted_head = caught_dropped = caught_turned = 0
    for _ in range(runs):
        one = {s: rng.randrange(2, 10**6) for s in sites()}
        two = {s: rng.randrange(2, 10**6) for s in sites()}
        product = {s: one[s] * two[s] for s in sites()}
        for site in sites():
            miss0 = push(product, site, -1) - push(one, site, -1) - push(two, site, -1)
            miss4 = push(product, site, 3) - push(one, site, 3) - push(two, site, 3)
            exact, dropped, turned, head = remainders(one, two, site)
            read += 1
            held += miss0 == exact
            parted_head += miss4 == head
            caught_dropped += miss0 != dropped
            caught_turned += miss0 != turned
    print(f"n = 0: the product's push equals the sum of the factors' pushes plus E exactly at {held} of {read} sites")
    print(f"the head's law: its miss equals H exactly at {parted_head} of {read} sites")
    print(f"the mutants of E (a term dropped, a sign turned) fail at {caught_dropped} and {caught_turned} of {read} sites")


if __name__ == "__main__":
    main(int(sys.argv[1]), int(sys.argv[2]))
