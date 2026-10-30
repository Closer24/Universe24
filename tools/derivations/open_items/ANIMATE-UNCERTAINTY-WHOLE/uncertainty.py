"""Fourier's support bound on Tensor24's board, in whole numbers alone and with no draw: a place is a Node-clock, a
motion a mode of the board, and their trade-off counted; what of the uncertainty principle follows from the board.

Big Pic (formerly Animate), 2026-10-30, the second text: the re-run, on the owner's word "Delete" and Sofer's
6523506996 and 6523641446, of the probe that left the tree (ANIMATE-UNCERTAINTY, held in git at scribe-5 6183738b1),
with its two readers' items folded. Every division is Rule3's carry; nothing here holds a float, a root, a circular
call, a random draw or a fraction. A motion's turn-sum is held as a polynomial in the board's turn and read as 0 or not
by its exact remainder on the cyclotomic polynomial; the waves at the bound are counted again, independently, as a
constant times a character on a coset of a subgroup (Smith's characterization), and the two counts must agree.

Run: python3 tools/derivations/open_items/ANIMATE-UNCERTAINTY-WHOLE/uncertainty.py (about two minutes); its output is
uncertainty.txt. README.md beside it reads it.
"""

import json
import sys
from itertools import combinations, combinations_with_replacement, product
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
    back_again = all(
        int(nb[o, nb[p, i]]) == i and int(nb[p, nb[o, i]]) == i for p, o in pairs for i in range(n)
    )
    six = all(len(set(int(q) for q in nb[:, i])) == 6 for i in range(n))
    wraps = all(apart(i, int(nb[k, i])) == 1 for k in range(6) for i in range(n))
    print(
        f"  1. The Meshes: {n} Node-clocks on a board {shape[0]} by {sy} by {sz} that wraps; each has six neighbours,"
    )
    print(
        f"     all different: {six}; each Spoke's opposite leads back: {back_again}; every neighbour one Mesh away, "
        f"across the wrap too: {wraps}"
    )
    row, site = (int(v[0]) for v in np.nonzero(start.a))
    print(
        f"  2. One gear laid on the example board: row {row} at Node-clock {site}, its now slot 1 and its before slot 0."
    )
    s, beat, twice = start, [], True
    away, teeth_moved, far = 0, 0, 0
    states = [start]
    for r in range(1, ROUNDS + 1):
        before = s
        s = step.tick(layout, s)
        states.append(s)
        twice &= bool((s.b == before.a).all())
        counts = set(int(i) for i in np.nonzero(np.asarray((s.a != 0) | (s.b != 0)).any(axis=0))[0])
        teeth = set(int(i) for i in np.nonzero(np.asarray(s.r != 0).any(axis=0))[0])
        away += bool(counts - {site})
        teeth_moved += bool(teeth - {site})
        far = max([far] + [apart(site, i) for i in counts | teeth])
        beat.append(int(s.a[row, site]))
        if r == 1:
            ends = sorted(set(int(q) for q in nb[:, site]))
            alike = len({int(s.r[row, q]) for q in ends}) == 1
            print(
                f"     round 1: its own now slot moves, and the fine teeth of its six neighbours {ends} move, all six "
                f"alike: {alike}"
            )
    print(
        f"     over {ROUNDS} rounds: rounds where a now or before slot stands off the laid Node-clock: {away}; rounds "
        f"where a neighbour's fine tooth stands off 0: {teeth_moved}; the farthest Node-clock any slot or tooth "
        f"reaches: {far} Mesh. So nothing travels on this example: the gear stays and its neighbours' teeth never "
        f"carry. That a round reaches one Mesh at most is the act's own (step.py reads its six Meshes, seen(a, nb)), "
        f"not this run's"
    )
    print(
        f"  3. Two moments: every round's before slot is the last round's now slot: {twice}; a gear's own rate is their "
        f"difference (not part 2's motion, a mode of the board)"
    )
    back = s
    for _ in range(ROUNDS):
        back = step.untick(layout, back)
    whole = all(bool((x == y).all()) for x, y in zip(back, start, strict=True))
    print(f"  4. The run back: {ROUNDS} rounds run back to the laid start, slot for slot: {whole}")
    period = next(
        p
        for p in range(1, ROUNDS + 1)
        if all(bool((x == y).all()) for x, y in zip(states[p], start, strict=True))
    )
    again = all(bool((x == y).all()) for x, y in zip(states[2 * period], start, strict=True))
    print(
        f"  5. The state at round {period} is the laid start, slot for slot, and again at round {2 * period}: {again}; "
        f"so the gear's beat repeats every {period} rounds exactly: its now slot {beat[:period]} (the example's "
        f"teeth are six grips, so the laid gear, with its neighbours silent, steps a+ = a - b)"
    )
    shown = {(t,): v for t, v in enumerate(beat[:period]) if v}
    held, beats, _ = counted(shown, (period,))
    print(
        f"     on the ring of its {period} rounds: rounds held {held}, beats held {beats}; one round alone holds every "
        f"beat of the ring, {counted({(0,): 1}, (period,))[1]} of {period} (a one-round wave's transform: an identity)"
    )


def subgroups(shape: tuple[int, ...], most: int) -> set[frozenset[tuple[int, ...]]]:
    """Every subgroup of the board's group of at most `most` elements, each generated by up to three of its elements."""
    nodes = list(product(*(range(s) for s in shape)))

    def add(x: tuple[int, ...], y: tuple[int, ...]) -> tuple[int, ...]:
        return tuple(carry(u + v, s, 0)[1] for u, v, s in zip(x, y, shape, strict=True))

    found: set[frozenset[tuple[int, ...]]] = set()
    zero = tuple(0 for _ in shape)
    for gens in combinations_with_replacement(nodes, 3):
        group, edge = {zero}, [zero]
        while edge and len(group) <= most:
            nxt = []
            for x in edge:
                for g in gens:
                    y = add(x, g)
                    if y not in group:
                        group.add(y)
                        nxt.append(y)
            edge = nxt
        if len(group) <= most:
            found.add(frozenset(group))
    found.add(frozenset({zero}))
    return found


def at_the_bound(shape: tuple[int, ...], most: int, values: tuple[int, ...]) -> set[frozenset]:
    """Smith's characterization, counted independently: every wave that is a constant (from `values`) times a character
    with values 1 and -1 on a coset of a subgroup of at most `most` elements, as a set of (Node-clock, value)."""
    nodes = list(product(*(range(s) for s in shape)))

    def add(x: tuple[int, ...], y: tuple[int, ...]) -> tuple[int, ...]:
        return tuple(carry(u + v, s, 0)[1] for u, v, s in zip(x, y, shape, strict=True))

    waves: set[frozenset] = set()
    for group in subgroups(shape, most):
        members = sorted(group)
        for signs in product((1, -1), repeat=len(members)):
            psi = dict(zip(members, signs, strict=True))
            if any(psi[add(x, y)] != psi[x] * psi[y] for x in members for y in members):
                continue
            for a in nodes:
                for c in values:
                    waves.add(frozenset((add(a, h), c * psi[h]) for h in members))
    return waves


def rings() -> None:
    """Part 2: every wave of -1, 0 and 1 on a ring of 2 to 10 Node-clocks, its nodes times its motions against the ring's
    nodes; the waves at the bound against Smith's characterization, counted independently."""
    for n in range(2, 11):
        turns = common((n,))
        circle = cyclotomic(turns)
        least, total, hit = None, 0, set()
        for values in product((-1, 0, 1), repeat=n):
            wave = {(x,): v for x, v in enumerate(values) if v}
            if not wave:
                continue
            made_up = len(wave) * motions(wave, (n,), turns, circle)
            least = made_up if least is None else min(least, made_up)
            if made_up == n:
                hit.add(frozenset(wave.items()))
            total += 1
        predicted = at_the_bound((n,), n, (1, -1))
        print(
            f"  ring of {n:2}: {total:5} waves, the least of nodes times motions {least} (the ring's nodes {n}); at it "
            f"{len(hit)} waves, the characterization's {len(predicted)}, the same waves: {hit == predicted}"
        )


def sweep(
    shape: tuple[int, ...], sizes: range, values: tuple[int, ...], origin: bool
) -> tuple[int, dict[int, int], set[frozenset]]:
    """Every wave on the given numbers of Node-clocks, each value from `values` (with `origin`, the board's first
    Node-clock always held at 1: a shift and a sign fixed): how many, the least of nodes times motions by size, and
    the waves at the bound."""
    nodes = list(product(*(range(s) for s in shape)))
    turns = common(shape)
    circle = cyclotomic(turns)
    zero = nodes[0]
    rest = nodes[1:] if origin else nodes
    least: dict[int, int] = {}
    hit: set[frozenset] = set()
    total = 0
    for size in sizes:
        for picked in combinations(rest, size - 1 if origin else size):
            for vals in product(values, repeat=len(picked)):
                wave = dict(zip(picked, vals, strict=True))
                if origin:
                    wave[zero] = 1
                made_up = size * motions(wave, shape, turns, circle)
                least[size] = min(least.get(size, made_up), made_up)
                if made_up == len(nodes):
                    hit.add(frozenset(wave.items()))
                total += 1
    return total, least, hit


def boards() -> None:
    """Part 3: whole classes of waves on three boards, the example's among them; the waves at the bound against Smith's
    characterization; and the waves that sit at the bound by their shape."""
    zero = (0, 0, 0)
    for shape, sizes, values, origin, name in (
        ((2, 2, 2), range(1, 9), (-1, 1), False, "every wave of -1, 0 and 1"),
        ((2, 3, 4), range(1, 4), (-1, 1), False, "every wave of -1 and 1 on 1 to 3 Node-clocks"),
        (
            (4, 4, 4),
            range(1, 5),
            (-1, 1),
            True,
            "every wave of -1 and 1 on 1 to 4 Node-clocks, the first Node-clock at 1",
        ),
    ):
        total, least, hit = sweep(shape, sizes, values, origin)
        predicted = {
            w
            for w in at_the_bound(shape, max(sizes), (1, -1))
            if len(w) in sizes and (not origin or (zero, 1) in w)
        }
        print(
            f"  board {shape}: {name}, {total} waves; the least of nodes times motions by size {least} (the board's "
            f"nodes {int(np.prod(shape))}); at it {len(hit)} waves, the characterization's {len(predicted)}, the same "
            f"waves: {hit == predicted}"
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
        "Fourier's support bound on Tensor24's board: a place is a Node-clock, a motion a mode of the board; exact, "
        "whole numbers only, no draw\n"
    )
    print("Part 1: the board's facts, on the engine at main (examples/tensor24)")
    engine()
    print(
        "\nPart 2: on a ring, every wave of -1, 0 and 1; a motion's turn-sum is 0 or not, exactly; the waves at the "
        "bound against the characterization"
    )
    rings()
    print("\nPart 3: whole classes of waves on three boards, the example's among them")
    boards()
