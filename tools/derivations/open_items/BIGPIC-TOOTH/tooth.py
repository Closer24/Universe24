"""The 24 and the mirror on a moving clock: where a sign flip departs, why, and the centred tooth that keeps it.

Big Pic, 2026-10-30, the solution from above that the Boss asked for (#2187 6524720383 item 2): his page on the 24's
symmetry is NOT PASSED by its hostile mathematician, since on a moving clock the turns that flip a sign depart by whole
turns from the second round. README.md beside it reads it. Every division is Rule3's carry; nothing here holds a float,
a root, a circular call, a random draw or a fraction.

The world: one Node-clock whose neighbours are itself, so no Mesh pulls. Row 0 is the clock's own count c (kind A1),
laid drifting by v counts a round with no spring, so the teeth of rows 1 to 3 read W = T + c and move with it. Rows 1
to 3 are a family of kind T1 with a spring F: V = F (X . X).

Part A runs the act as main holds it (engine/step.py), each fine tooth kept from 0 up and flipped about its teeth's
middle, w - 1 - r. Part B runs the same world with each fine tooth kept centred, s = 2 r + 1 - W, stored as such and
flipped by negation, the carry 2 (W (a - b) + push) + s = 2 q W + s+. On a still clock the two are one act, state for
state.

Run: python3 tools/derivations/open_items/BIGPIC-TOOTH/tooth.py (a few seconds); its output is tooth.txt.
"""

import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(ROOT / "src"))

from tensor24.algebra.carry import carry, flip  # noqa: E402
from tensor24.engine import step  # noqa: E402
from tensor24.engine.state import Gearing, Layout, Plan, Read, State  # noqa: E402
from tensor24.main import made  # noqa: E402
from tensor24.runner import load as loading  # noqa: E402

KINDS, _, _ = made(loading.star(3))
ON = [g for g in range(KINDS.a1.shape[0]) if KINDS.a1[g, 0, 0] == 1]  # the 24, weighed 1 by Rule3
TURNS = [[[int(v) for v in row] for row in KINDS.t1[g]] for g in ON]
ROWS, X = 4, [1, 2, 3]
PLANES = 1 + 3 + 1
ROUNDS = 400


def layout(teeth: int, spring: int) -> Layout:
    """One Node-clock: the clock's count at row 0, its teeth at rest; rows 1 to 3 read W = T + c; the spring on X."""
    nb = np.zeros((6, 1), dtype=np.intp)
    spokes = np.array([s * axis for axis in np.eye(3, dtype=int) for s in (1, -1)], dtype=object)
    meshes, _ = carry(np.arange(6), 2, 0)
    unit = PLANES * ROWS
    # V = spring (X . X): each X row pushed by -2 spring X, as two legs of one monomial
    first = np.array(X + X, dtype=np.intp)
    second = np.array([unit] * 6, dtype=np.intp)
    third = np.array([unit] * 6, dtype=np.intp)
    plan = Plan(
        first, second, third, np.array([-spring] * 6, dtype=object), np.array(X + X, dtype=np.intp)
    )
    clock = Read(np.zeros(3, dtype=np.intp), np.ones(3, dtype=object), np.array(X, dtype=np.intp))
    none = np.zeros(0, dtype=np.intp)
    ones = np.ones((1, 1), dtype=object)
    return Layout(
        nb,
        spokes,
        meshes[:, None],
        ones.repeat(3, axis=1),
        Gearing(teeth * ones, 1, 1, 1),
        plan,
        clock,
        Read(none, none.astype(object), none),
    )


def lay(c0: int, v: int, x: tuple[int, int, int]) -> State:
    a = np.array([[c0 + v], [x[0]], [x[1]], [x[2]]], dtype=object)
    b = np.array([[c0], [x[0]], [x[1]], [x[2]]], dtype=object)
    return State(a, b, 0 * a, 0 * a)


def teeth_at(lay_out: Layout, a: object) -> list[int]:
    """Every row's teeth at a slot: the rest, and for X the clock's count read there."""
    rest = int(lay_out.gearing.rest[0, 0])
    return [rest] + [rest + int(a[0, 0])] * 3


def turned_r(s: State, m: list[list[int]], lay_out: Layout) -> State:
    """A turn on X in the act as built: a row sent to minus a row has its tooth flipped in the teeth it was kept at,
    the before slot's, as the act's own mirror flips it."""
    a, b, r = s.a.copy(), s.b.copy(), s.r.copy()
    kept = teeth_at(lay_out, s.b)
    for i in range(3):
        j = next(c for c in range(3) if m[i][c] != 0)
        sign = m[i][j]
        a[X[i], 0], b[X[i], 0] = sign * s.a[X[j], 0], sign * s.b[X[j], 0]
        r[X[i], 0] = s.r[X[j], 0] if sign > 0 else flip(s.r[X[j], 0], kept[X[j]])
    return State(a, b, r, s.rd)


def same(x: State, y: State) -> bool:
    return all(np.array_equal(u, w) for u, w in zip(x, y, strict=True))


def run_r(lay_out: Layout, start: State, rounds: int) -> list[State]:
    states, s = [start], start
    for _ in range(rounds):
        s = step.tick(lay_out, s)
        states.append(s)
    return states


# The centred tooth: a state is (a, b, s), s the fine tooth counted in half teeth about its teeth's middle.
def tick_s(
    lay_out: Layout, a: list[int], b: list[int], s: list[int], spring: int
) -> tuple[list[int], ...]:
    w = teeth_at(lay_out, np.array([[a[0]]], dtype=object))
    push = [0] + [-2 * spring * a[x] for x in X]
    out_a, out_s = [], []
    for row in range(ROWS):
        x = 2 * (w[row] * (a[row] - b[row]) + push[row]) + s[row]
        q, rem = carry(x + w[row], 2 * w[row], 0)
        out_a.append(a[row] + q)
        out_s.append(rem - w[row])
    return out_a, list(a), out_s


def run_s(
    lay_out: Layout, start: tuple[list[int], ...], rounds: int, spring: int
) -> list[tuple[list[int], ...]]:
    states, s = [start], start
    for _ in range(rounds):
        s = tick_s(lay_out, *s, spring)
        states.append(s)
    return states


def turned_s(state: tuple[list[int], ...], m: list[list[int]]) -> tuple[list[int], ...]:
    """A turn on X with the centred tooth: a row sent to minus a row has its tooth negated, with no teeth read."""
    a, b, s = (list(part) for part in state)
    na, nb_, ns = list(a), list(b), list(s)
    for i in range(3):
        j = next(c for c in range(3) if m[i][c] != 0)
        sign = m[i][j]
        na[X[i]], nb_[X[i]], ns[X[i]] = sign * a[X[j]], sign * b[X[j]], sign * s[X[j]]
    return na, nb_, ns


def centred_lay(lay_out: Layout, start: State) -> tuple[list[int], ...]:
    """The same lay with each tooth centred about the teeth it is read at: s = 2 r + 1 - W."""
    w = teeth_at(lay_out, start.a)
    a = [int(v) for v in start.a[:, 0]]
    b = [int(v) for v in start.b[:, 0]]
    return a, b, [2 * int(r) + 1 - w[row] for row, r in enumerate(start.r[:, 0])]


def part_a(rest: int, spring: int) -> None:
    print("A. The act as main holds it: each tooth kept from 0 up and flipped about its teeth's middle.")
    for v in (0, 1, 2):
        lay_out = layout(rest, spring)
        start = lay(0, v, (5, -3, 2))
        base = run_r(lay_out, start, ROUNDS)
        kept, first = 0, []
        for m in TURNS:
            other = run_r(lay_out, turned_r(start, m, lay_out), ROUNDS)
            parted = [
                t
                for t, (x, y) in enumerate(zip(other, base, strict=True))
                if not same(x, turned_r(y, m, lay_out))
            ]
            kept += not parted
            if parted:
                first.append(parted[0])
        print(
            f"   the clock drifting by {v} a round (rest teeth {rest}): turns whose turned run is the run turned, "
            f"state for state, over {ROUNDS} rounds: {kept} of {len(TURNS)}; the first round a turned run parts, "
            f"at the earliest: {min(first) if first else 'none'}"
        )


def part_b(rest: int, spring: int) -> None:
    print(
        "\nB. The centred tooth: each tooth stored as s = 2 r + 1 - W and flipped by negation, with no teeth read."
    )
    for v in (0, 2, 1):
        lay_out = layout(rest, spring)
        start = lay(0, v, (5, -3, 2))
        base = run_s(lay_out, centred_lay(lay_out, start), ROUNDS, spring)
        kept, first = 0, []
        for m in TURNS:
            other = run_s(lay_out, turned_s(centred_lay(lay_out, start), m), ROUNDS, spring)
            parted = [t for t, (x, y) in enumerate(zip(other, base, strict=True)) if x != turned_s(y, m)]
            kept += not parted
            if parted:
                first.append(parted[0])
        print(
            f"   the clock drifting by {v} a round: turns whose turned run is the run turned, state for state, over "
            f"{ROUNDS} rounds: {kept} of {len(TURNS)}; the first round a turned run parts, at the earliest: "
            f"{min(first) if first else 'none'}"
        )
    lay_out = layout(rest, spring)
    start = lay(0, 0, (5, -3, 2))
    r_run = run_r(lay_out, start, ROUNDS)
    s_run = run_s(lay_out, centred_lay(lay_out, start), ROUNDS, spring)
    alike = sum(
        1
        for x, (a, b, s) in zip(r_run, s_run, strict=True)
        if [int(u) for u in x.a[:, 0]] == a
        and [int(u) for u in x.b[:, 0]] == b
        and [2 * int(r) + 1 - w for r, w in zip(x.r[:, 0], teeth_at(lay_out, x.a), strict=True)] == s
    )
    print(
        f"   on a still clock the two acts are one, state for state (s = 2 r + 1 - W): {alike} of {ROUNDS + 1} rounds"
    )


def part_c(rest: int, spring: int) -> None:
    print(
        "\nC. The mirror with the centred tooth, (a, b, s) -> (b, a, -s): the run back on a moving clock."
    )
    for v in (2, 1):
        lay_out = layout(rest, spring)
        start = centred_lay(lay_out, lay(0, v, (5, -3, 2)))
        states = run_s(lay_out, start, ROUNDS, spring)
        s = states[-1]
        back = 0
        for t in range(ROUNDS - 1, -1, -1):
            a, b, sv = s
            ma, mb, ms = tick_s(lay_out, b, a, [-x for x in sv], spring)
            s = (mb, ma, [-x for x in ms])
            back += s == states[t]
        print(
            f"   the clock drifting by {v} a round: rounds run back to their way out's state by the act on the "
            f"mirrored state: {back} of {ROUNDS}; mirrored twice is the state itself at every teeth: True by -(-s) = s"
        )


def part_d() -> None:
    print("\nD. Where a tooth can stand still under a sign flip, by the teeth's parity.")
    fixed = [
        w for w in range(1, 13) if 0 in range(-w + 1, w, 2)
    ]  # the centred teeth: -(w - 1), -(w - 3), ..., w - 1
    print(
        f"   teeth from 1 to 12 with a centred tooth that a negation keeps (s = 0, so 2 r + 1 = W): {fixed}; at even "
        f"teeth every centred tooth is odd, so no state of a negated row is kept by its turn"
    )
    rest = 6 * 15162856759112389 * 1000 * 1000
    _, parity = carry(rest, 2, 0)
    print(f"   the example's rest teeth, 6 den Gamma^2 = {rest}: odd: {parity == 1}")


def main() -> None:
    rest, spring = 6, 1  # small teeth, so that a remainder lands on the edge often
    part_a(rest, spring)
    part_b(rest, spring)
    part_c(rest, spring)
    part_d()


if __name__ == "__main__":
    main()
