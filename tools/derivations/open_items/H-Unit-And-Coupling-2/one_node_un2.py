"""un2's one-Node test (runnable; every reading an integer): (1) the unit as one function of the pair against David's two cases at the
three dens (the toy's, the middle's, 1,021); (2) the share of one laid quantum at a lone Node for every record, 6 den A^2 at the quarter
turn and at the rest, and the units as the share of one quantum of form T at the row's own rotation (the quarter turn where the pair has no
rest); (3) the identity turn at the coupling 0 by arithmetic (the orbit's pair at the count 0, turn_pair exact); (4) the order key against
David's order; (5) the phase pair's amplitude from the width 128: HALF_WIDTH = 128 div 2, the room 2 K_0 X + D within 63 bits.
Run with PYTHONPATH=<worktree>/src (David's src: the functions used stand there)."""

import json
import os
import sys

import numpy as np

from event_universe.core import rule3
from event_universe.core.paces import sine_den
from event_universe.core.rule3 import largest_below, quotient, unit_of
from event_universe.features import phase
from event_universe.links import turn_pair
from event_universe.node import Node
from event_universe.rows import HALF_WIDTH, PLANE, order_of

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
WORLDS = os.path.join(ROOT, "tests", "worlds")
sys.set_int_max_str_digits(0)


def unit_david(num: int, den: int, T: int) -> int:
    return unit_of(sine_den(num, den) if den - num else den, T)


def unit_one(num: int, den: int, T: int) -> int:
    """UN-S1: 3 T (s + den (num div den)), s the pair's sine; num div den is 1 at the pair with no gap and 0 at every other pair."""
    return unit_of(sine_den(num, den) + den * quotient(num, den), T)


def section_1() -> None:
    print("== (1) the unit, one function of the pair against the two cases")
    T = 36000
    universes = {
        "toy": json.load(open(os.path.join(WORLDS, "universe_toy.json"))),
        "middle": json.load(open(os.path.join(WORLDS, "universe_middle.json"))),
    }
    cases = []
    for name, u in universes.items():
        den = int(u["integers"]["den"])
        for r in u["rows"]:
            if r.get("pair") and int(r["shape"]) == PLANE:
                cases.append((name, int(r["pair"][0]), den))
    cases += [("den 1021", 779, 1021), ("den 1021", 1021, 1021), ("den 1021", 0, 1021)]
    for name, num, den in cases:
        a, b = unit_david(num, den, T), unit_one(num, den, T)
        print(
            f"{name} pair ({num}, {den}) gap {den - num}: david {a} one {b} equal {a == b} bits {b.bit_length()} num div den {quotient(num, den)} s {sine_den(num, den)}"
        )


def lone_node_share(node: Node, rec: int, levels: tuple[int, int, int, int]) -> int:
    """The conserved form's share summed over the 3-cube after one record's four levels are laid at one Node (the vacuum's weight)."""
    row = node.records()[rec]
    at = (1, 1, 1)
    node.lay(rec, at, levels)
    rule = node.rule_of(row, node.content(), node.link_factors())
    re, im = row.lines
    total = int(
        sum(
            int(x)
            for x in (node.share(re, rule, vacuum=True) + node.share(im, rule, vacuum=True)).reshape(-1)
        )
    )
    node.lay(rec, at, levels, -1)
    return total


def section_2() -> None:
    print("== (2) the share of one laid quantum at a lone Node, every record alike")
    universe = json.load(open(os.path.join(WORLDS, "universe_toy.json")))
    world = {"universe": "universe_toy.json", "shape": [3, 3, 3], "intervals": 1, "seed": []}
    node = Node(universe, world)
    den, T = node.den, node.T
    A = largest_below(quotient(T, 2))
    print(f"den {den} T {T} A = largest_below(T div 2) = {A} (A^2 = {A * A}, T div 2 = {quotient(T, 2)})")
    for rec, row in enumerate(node.records()):
        num = row.pair[0]
        s = sine_den(num, den)
        quarter = lone_node_share(node, rec, (A, 0, 0, A))
        rest = lone_node_share(node, rec, (A, quotient(A * num, den), 0, quotient(A * s, den)))
        unit = node.units[rec]
        q_u, q_r = divmod(quarter, unit)
        print(
            f"record {rec} pair ({num}, {den}) gap {den - num}: quarter-turn share {quarter} = 6 den A^2 {quarter == 6 * den * A * A}; "
            f"rest share {rest} (6 den A^2 {rest == 6 * den * A * A}); unit {unit}; quarter share in units {q_u} rem {q_r}; "
            f"2 A^2 against T: {2 * A * A} / {T}"
        )
    # the unit as the share of one quantum of form T at the row's own rotation: 6 den A^2 sin^2 omega with 2 A^2 sin omega = T
    # gives 3 T den sin omega: at the rest sin omega = s / den (a pair with a gap), at the quarter turn sin omega = 1 (the pair with none)
    for rec, row in enumerate(node.records()):
        num = row.pair[0]
        s = sine_den(num, den)
        sin_read = s + den * quotient(num, den)
        print(
            f"record {rec}: W_c sin(omega_read) = 3 T den x {sin_read} / den = {3 * T * sin_read} == unit {node.units[rec]}: {3 * T * sin_read == node.units[rec]}"
        )
    # the massless rest record over the envelope has no share at the uniform level: the double root has no rest quantum
    light = node.records().index(node.row(PLANE, gap=0))
    uniform = lone_node_share(node, light, (A, A, 0, 0))
    node.lay(light, Ellipsis, (A, A, 0, 0))
    row = node.records()[light]
    rule = node.rule_of(row, node.content(), node.link_factors())
    board = int(sum(int(x) for x in node.share(row.lines[0], rule, vacuum=True).reshape(-1)))
    node.lay(light, Ellipsis, (A, A, 0, 0), -1)
    print(f"the massless pair at rest (now = before = A): lone Node share {uniform}; the uniform level over the board: share {board} (the double root has no rest quantum: the lay by `fitted` has no solution)")


def section_3() -> None:
    print("== (3) the identity turn at the coupling 0 by arithmetic")
    gamma = 1000
    X = phase.amplitude(phase.unit(gamma), HALF_WIDTH - 1)
    seed_pair = phase.seed(X, gamma)
    c0, s0 = int(seed_pair[0][0]), int(seed_pair[1][0])
    print(f"Gamma {gamma} X {X} ({X.bit_length()} bits); the orbit's pair at the count 0: ({c0}, {s0}); equals (X, 0): {(c0, s0) == (X, 0)}")
    wl = 4 * gamma
    exact = 0
    trials = 0
    rng = np.random.default_rng(24)
    for _ in range(2000):
        re, im = int(rng.integers(-10**12, 10**12)), int(rng.integers(-10**12, 10**12))
        a = turn_pair(re, im, X, 0, X)
        b = turn_pair(a[0], a[1], wl * wl - 0, 0, wl * wl + 0)
        trials += 1
        exact += (int(a[0]), int(a[1])) == (re, im) and (int(b[0]), int(b[1])) == (re, im)
    print(f"turn_pair at (X, 0) over X then the odd triple at n = 0: identity on {exact} of {trials} random pairs within 2^40")


def section_4() -> None:
    print("== (4) the order key against David's order")
    universe = json.load(open(os.path.join(WORLDS, "universe_toy.json")))
    world = {"universe": "universe_toy.json", "shape": [3, 3, 3], "intervals": 1, "seed": []}
    node = Node(universe, world)

    def key(row):
        if row.wall is not None:
            return (0, 0, 0)
        return (1, row.shape, sum(1 for line in row.lines if line.wwall is not None))

    david = [order_of(r) for r in node.rows_]
    keys = [key(r) for r in node.rows_]
    print("David's order_of in the acts' order:", david)
    print("the key (wall, shape, written lines):", keys)
    print("the key sorts the file's rows into the same order:", sorted(node.by_index, key=key) == node.rows_)


def section_5() -> None:
    print("== (5) HALF_WIDTH from the width 128")
    for gamma in (1000, 6000):
        D = phase.D(gamma)
        K0 = phase.K0(gamma)
        X = phase.amplitude(phase.unit(gamma), HALF_WIDTH - 1)
        room = 2 * phase.K0(phase.unit(gamma)) * X + phase.D(phase.unit(gamma))
        print(
            f"Gamma {gamma}: HALF_WIDTH {HALF_WIDTH} = 128 div 2 {HALF_WIDTH == quotient(128, 2)}; width 63 = HALF_WIDTH - 1; X {X} ({X.bit_length()} bits), "
            f"the act's room 2 K_0 X + D at the line's Gamma 2 Gamma = {room} ({room.bit_length()} bits, within 63: {room.bit_length() <= 63}); "
            f"X times a level of 64 bits within 128: {(X * (2**64 - 1)).bit_length()} bits; D {D} K_0 {K0}"
        )


if __name__ == "__main__":
    section_1()
    section_2()
    section_3()
    section_4()
    section_5()
