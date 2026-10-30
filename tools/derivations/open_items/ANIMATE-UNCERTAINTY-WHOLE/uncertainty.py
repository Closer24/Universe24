"""Uncertainty on Tensor24's board, each step checked, in whole numbers alone and with no draw: a place is a
Node-clock, a motion a step along a Mesh, and their trade-off counted.

Animate, 2026-10-30: the re-run, on the owner's word "Delete" and Sofer's 6523506996 and 6523641446, of the probe that
left the tree (ANIMATE-UNCERTAINTY, held in git at scribe-5 6183738b1). The old probe drew 3,000 waves at random on
each board; this one counts every wave of a class instead. Every division is Rule3's carry; nothing here holds a float,
a root, a circular call, a random draw or a fraction. A motion's turn-sum is held as a polynomial in the board's turn
and read as 0 or not by its exact remainder on the cyclotomic polynomial.

Run: python3 tools/derivations/open_items/ANIMATE-UNCERTAINTY-WHOLE/uncertainty.py (about a minute); its output is
uncertainty.txt. README.md beside it reads it.
"""

import json
import sys
from itertools import combinations, product
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(ROOT / "src"))

import numpy as np  # noqa: E402

from tensor24.algebra.carry import carry  # noqa: E402
from tensor24.engine import step  # noqa: E402
from tensor24.main import ENGINE, made  # noqa: E402
from tensor24.main import layout as laid  # noqa: E402
from tensor24.runner.board import board  # noqa: E402
from tensor24.runner.files import sites_of  # noqa: E402
from tensor24.runner.load import load, star  # noqa: E402

EXAMPLES = ROOT / "examples" / "tensor24"
ROUNDS = 60  # the rounds the engine is run, forward and back


def quotient(poly: list[int], modulus: list[int]) -> list[int]:
    """The exact quotient of an integer polynomial by a monic one, coefficients from degree 0 up; a remainder is refused."""
    rest, top = list(poly), len(modulus) - 1
    out = [0] * (len(rest) - top)
    for at in range(len(rest) - 1, top - 1, -1):
        lead = rest[at]
        out[at - top] = lead
        for k, c in enumerate(modulus):
            rest[at - top + k] -= lead * c
    assert not any(rest), "the division is not exact"
    return out


def remainder(poly: list[int], modulus: list[int]) -> list[int]:
    """The remainder of an integer polynomial by a monic one: 0 exactly where the polynomial vanishes at every root of it."""
    rest, top = list(poly), len(modulus) - 1
    for at in range(len(rest) - 1, top - 1, -1):
        lead = rest[at]
        for k, c in enumerate(modulus):
            rest[at - top + k] -= lead * c
    return rest[:top]


def divides(d: int, n: int) -> bool:
    return carry(n, d, 0)[1] == 0


def cyclotomic(n: int) -> list[int]:
    """The polynomial whose roots are the n-th turns of a full circle that no smaller count of steps closes."""
    poly = [-1] + [0] * (n - 1) + [1]
    for d in range(1, n):
        if divides(d, n):
            poly = quotient(poly, cyclotomic(d))
    return poly


def common(sides: tuple[int, ...]) -> int:
    """The least whole number every side divides: the turns a step along any side is counted in."""
    m = 1
    for s in sides:
        a, b = m, s
        while b:
            a, b = b, carry(a, b, 0)[1]
        m = carry(m * s, a, 0)[0]
    return m


def motions(
    wave: dict[tuple[int, ...], int], shape: tuple[int, ...], turns: int, circle: list[int]
) -> int:
    """How many of the board's motions a wave holds: a motion's turn-sum over the nodes, exact, kept where it is not 0."""
    steps = [carry(turns, s, 0)[0] for s in shape]
    held = 0
    for k in product(*(range(s) for s in shape)):
        poly = [0] * turns
        for x, v in wave.items():
            _, at = carry(sum(u * kk * xx for u, kk, xx in zip(steps, k, x, strict=True)), turns, 0)
            poly[at] += v
        held += any(remainder(poly, circle))
    return held


def counted(wave: dict[tuple[int, ...], int], shape: tuple[int, ...]) -> tuple[int, int, int]:
    """A wave's nodes, its motions and the board's nodes."""
    turns = common(shape)
    return len(wave), motions(wave, shape, turns, cyclotomic(turns)), int(np.prod(shape))


def engine() -> None:
    """Part 1: the board's facts, read on the engine itself from the example files."""
    universe, piece, setting = (
        json.loads((EXAMPLES / n).read_text(encoding="utf-8"))
        for n in ("universe.json", "piece.json", "setting.json")
    )
    shape = tuple(piece["shape"])
    kinds, tables, square = made(star(len(shape)))
    loaded, found = load(universe, setting, sites_of(list(shape)), kinds, tables, square)
    assert not found, found
    layout, start = laid(universe, list(shape), loaded), ENGINE.state(*loaded.state)
    nb = board(shape)
    n = nb.shape[1]
    sy, sz = shape[1], shape[2]

    def at(i: int) -> tuple[int, int, int]:
        x, rest = carry(i, sy * sz, 0)
        y, z = carry(rest, sz, 0)
        return x, y, z

    def apart(i: int, j: int) -> int:
        return sum(
            min(carry(p - q, s, 0)[1], carry(q - p, s, 0)[1])
            for p, q, s in zip(at(i), at(j), shape, strict=True)
        )

    pairs = [
        (2 * a, 2 * a + 1) for a in range(3)
    ]  # each Spoke beside its opposite: +x, -x, +y, -y, +z, -z
    opposite = all(
        int(nb[o, nb[p, i]]) == i and int(nb[p, nb[o, i]]) == i for p, o in pairs for i in range(n)
    )
    six = all(len(set(int(q) for q in nb[:, i])) == 6 for i in range(n))
    wraps = all(apart(i, int(nb[k, i])) == 1 for k in range(6) for i in range(n))
    print(
        f"  1. The Meshes: {n} Node-clocks on a board {shape[0]} by {sy} by {sz} that wraps; each reads six neighbours,"
    )
    print(
        f"     all different: {six}; each Mesh read both ways: {opposite}; every neighbour one Mesh away, across the wrap too: {wraps}"
    )
    row, site = (int(v[0]) for v in np.nonzero(start.a))
    print(
        f"  2. One gear laid on the example board: row {row} at Node-clock {site}, its now slot 1 and its before slot 0."
    )
    s, far, beat, twice = start, 0, [], True
    for r in range(1, ROUNDS + 1):
        before = s
        s = step.tick(layout, s)
        twice &= bool((s.b == before.a).all())
        touched = set()
        for part in s:
            touched |= set(int(i) for i in np.nonzero(np.asarray(part != 0).any(axis=0))[0])
        far = max(far, max(apart(site, i) for i in touched) - r)
        beat.append(int(s.a[row, site]))
        if r == 1:
            ends = sorted(set(int(q) for q in nb[:, site]))
            print(
                f"     round 1 touches Node-clocks {sorted(touched)}: the gear's own and its six neighbours {ends};"
            )
            teeth = {int(s.r[row, q]) for q in ends}
            print(
                f"     the six neighbours' fine teeth all one value: {len(teeth) == 1} (every direction alike)"
            )
    print(f"     over {ROUNDS} rounds, no Node-clock touched farther than one Mesh a round: {far <= 0}")
    print(
        f"  3. Two moments: every round's before slot is the last round's now slot: {twice}; a motion is their difference"
    )
    back = s
    for _ in range(ROUNDS):
        back = step.untick(layout, back)
    whole = all(bool((x == y).all()) for x, y in zip(back, start, strict=True))
    print(f"  4. The run back: {ROUNDS} rounds run back to the laid start, slot for slot: {whole}")
    period = next(p for p in range(1, ROUNDS) if beat[p:] == beat[:-p])
    print(
        f"  5. The laid gear's own beat, its now slot round by round: {beat[:period]}, repeating every {period} rounds"
    )
    shown = {(t,): v for t, v in enumerate(beat[:period]) if v}
    print(
        f"     on the ring of its {period} rounds: rounds held {counted(shown, (period,))[0]}, beats held {counted(shown, (period,))[1]};"
    )
    print(
        f"     a click at one round: rounds held 1, beats held {counted({(0,): 1}, (period,))[1]} of {period}"
    )


def rings() -> None:
    """Part 2: every wave of -1, 0 and 1 on a ring of 2 to 10 Node-clocks, its nodes times its motions against the ring's nodes."""
    for n in range(2, 11):
        turns = common((n,))
        circle = cyclotomic(turns)
        least, equal, total = None, 0, 0
        for values in product((-1, 0, 1), repeat=n):
            wave = {(x,): v for x, v in enumerate(values) if v}
            if not wave:
                continue
            made_up = len(wave) * motions(wave, (n,), turns, circle)
            least = made_up if least is None else min(least, made_up)
            equal += made_up == n
            total += 1
        print(
            f"  ring of {n:2}: {total:5} waves, the least of nodes times motions {least} (the ring's nodes {n}), {equal} waves at it"
        )


def sweep(shape: tuple[int, ...], most: int, values: tuple[int, ...]) -> tuple[int, int, int]:
    """Every wave on 1 to `most` Node-clocks of the board, each value from `values`: how many, the least of nodes times
    motions, and how many sit at it."""
    nodes = list(product(*(range(s) for s in shape)))
    turns = common(shape)
    circle = cyclotomic(turns)
    least, equal, total = None, 0, 0
    for size in range(1, most + 1):
        for picked in combinations(nodes, size):
            for vals in product(values, repeat=size):
                wave = dict(zip(picked, vals, strict=True))
                made_up = size * motions(wave, shape, turns, circle)
                least = made_up if least is None else min(least, made_up)
                equal += made_up == len(nodes)
                total += 1
    return total, least, equal


def boards() -> None:
    """Part 3: whole classes of waves on three boards, the example's among them, and the waves that sit at the bound."""
    for shape, most, values in (
        ((2, 2, 2), 8, (-1, 1)),
        ((2, 3, 4), 3, (-1, 1)),
        ((4, 4, 4), 2, (-2, -1, 1, 2)),
    ):
        total, least, equal = sweep(shape, most, values)
        print(
            f"  board {shape}: every wave on 1 to {most} Node-clocks with values {values}, {total} waves; the least of "
            f"nodes times motions {least} (the board's nodes {int(np.prod(shape))}), {equal} at it"
        )
    shape = (4, 4, 4)
    for name, wave in (
        ("one Node-clock", {(0, 0, 0): 1}),
        ("every other Node-clock on one line", {(0, 0, 0): 1, (0, 0, 2): 1}),
        ("one line", {(0, 0, z): 1 for z in range(4)}),
        ("one plane", {(0, y, z): 1 for y in range(4) for z in range(4)}),
        (
            "a wave along z, 1 0 -1 0, on the whole board",
            {(x, y, z): 1 - z for x in range(4) for y in range(4) for z in (0, 2)},
        ),
        ("the whole board alike", {x: 1 for x in product(range(4), repeat=3)}),
    ):
        held, moving, n = counted(wave, shape)
        print(
            f"  {name}: nodes {held}, motions {moving}, nodes times motions {held * moving} (the board's {n})"
        )


if __name__ == "__main__":
    print(
        "Uncertainty on Tensor24's board: a place is a Node-clock, a motion a step along a Mesh; exact, whole numbers "
        "only, no draw\n"
    )
    print("Part 1: the board's facts, on the engine at main (examples/tensor24)")
    engine()
    print("\nPart 2: on a ring, every wave of -1, 0 and 1; a motion's turn-sum is 0 or not, exactly")
    rings()
    print("\nPart 3: whole classes of waves on three boards, the example's among them")
    boards()
