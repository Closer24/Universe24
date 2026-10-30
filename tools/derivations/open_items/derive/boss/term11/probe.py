"""Term 11, the whole click, on the Node-clock's own act: the click tooth under the mirror, its birth at the one tooth
the flip leaves in place, and the books of a give and a take, in whole numbers (the Boss, 2026-10-30, for David's two
readers). The world is Animate's (ANIMATE-CLICK/click.py: one Node-clock, a giver and a taker, two parts each, term 6's
vertex between them); the click is her measured form, q_c, k+ = carry(tau, key, k), with nothing written into a, b, r
or r_d; what this probe adds is the run back by the act alone and the birth.

Run: python3 tools/derivations/open_items/derive/boss/term11/probe.py (about 20 seconds); its output is probe.txt.
"""

import importlib.util
import itertools
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[6]
sys.path.insert(0, str(ROOT / "src"))

from tensor24.algebra.carry import carry, flip  # noqa: E402
from tensor24.engine import step  # noqa: E402

SPEC = importlib.util.spec_from_file_location(
    "click", ROOT / "tools/derivations/open_items/ANIMATE-CLICK/click.py"
)
click = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(click)


def areas(layout, s):
    """The area the coupling moves into each hand in a round, read at the now slot: (the giver's, the taker's)."""
    _, j = step.sources(layout, s.a)
    pushed = list(j[:, 0])
    return click.moved(s, pushed, click.LRE), click.moved(s, pushed, click.MRE)


def tick(layout, s, teeth, key):
    """One round: the gears step as the act steps them, and each hand's area is carried at the key by its own tooth."""
    carried = [carry(tau, key, k) for tau, k in zip(areas(layout, s), teeth, strict=True)]
    return step.tick(layout, s), tuple(k for _, k in carried), tuple(q for q, _ in carried)


def mirror(layout, s, teeth, key):
    """Time's reversal: the act's own mirror on the gears, and each click tooth flipped in its key, as every fine tooth
    is flipped in its teeth."""
    return step.mirror(layout, s), tuple(flip(k, key) for k in teeth)


def untick(layout, s, teeth, key):
    """The round run back by the act alone: the tick on the mirrored state, mirrored; no click of the record is read."""
    m, mt = mirror(layout, s, teeth, key)
    n, nt, q = tick(layout, m, mt, key)
    back, bt = mirror(layout, n, nt, key)
    return back, bt, q


def books(key, birth, area):
    """The counts of a take of the area and of its give, each carried at the key from the birth."""
    taken, _ = carry(area, key, birth)
    given, _ = carry(-area, key, birth)
    return taken, given


def main():
    g, _ = carry(click.F, 10, 0)  # Animate's vertex
    layout = click.node(g)
    start = click.lay()
    held = click.swept(click.LRE, click.LIM, start.a[:, 0], click.stride(start))
    near, _ = carry(held, 7, 0)  # Animate's key, a seventh of the giver's area at the lay
    _, odd = carry(near, 2, 0)
    key = near + 1 - odd  # the odd key beside hers
    birth, _ = carry(key - 1, 2, 0)
    print(
        f"the giver's swept area at the lay {held}; the key {key} (odd); the birth (key - 1) div 2 = {birth}"
    )
    print(
        f"1. The birth is the one tooth the flip leaves in place: flip(birth, key) = birth: {flip(birth, key) == birth}"
    )

    states, teeth, clicks, moved = [start], [(birth, birth)], [], []
    s, k = start, (birth, birth)
    for _ in range(click.ROUNDS):
        moved.append(areas(layout, s))
        s, k, q = tick(layout, s, k, key)
        states.append(s)
        teeth.append(k)
        clicks.append(q)
    n = len(clicks)
    print(f"\n2. The forward run, {n} rounds, the clicks pushing nothing:")
    opposite = sum(1 for given, taken in moved if given + taken != 0)
    print(f"   rounds where the giver's area moved is not minus the taker's: {opposite} of {n}")
    unbalanced = sum(1 for q in clicks if q[0] + q[1] != 0)
    print(
        f"   rounds where the giver's click is not minus the taker's (the books, every round): {unbalanced} of {n}"
    )
    taken = [q[1] for q in clicks]
    counts = [0, *itertools.accumulate(taken)]
    print(
        f"   the taker's clicks: {sum(1 for q in taken if q > 0)} taken, {sum(1 for q in taken if q < 0)} given back; "
        f"its count from {min(counts)} to {max(counts)}"
    )
    total, count, missed = 0, 0, 0
    for t in range(n):
        total += moved[t][1]
        count += clicks[t][1]
        missed += key * count + (teeth[t + 1][1] - birth) != total
    print(
        f"   rounds where key x the taker's count + (its tooth - the birth) is not the area moved into it: {missed} of {n}"
    )

    print(
        "\n3. The run back by the act alone, the click teeth flipped in the key by the mirror, no log read:"
    )
    s, k = states[-1], teeth[-1]
    same, alike, quotients = 0, 0, 0
    for t in range(n - 1, -1, -1):
        s, k, q = untick(layout, s, k, key)
        same += click.same(s, states[t])
        alike += k == teeth[t]
        quotients += q == clicks[t]
    print(f"   rounds whose gears return to the way out's: {same} of {n}")
    print(
        f"   rounds whose click teeth return to the way out's: {alike} of {n}; at the start, both at the birth: {k == (birth, birth)}"
    )
    print(
        f"   rounds where the mirrored tick's quotients are the way out's (the area at the now slot the mirror keeps): {quotients} of {n}"
    )
    s, k = states[-1], teeth[-1]
    unflipped = 0
    for t in range(n - 1, -1, -1):
        m = step.mirror(layout, s)
        nxt, nk, _ = tick(layout, m, k, key)  # the mutant: the mirror leaves the click teeth as they are
        s, k = step.mirror(layout, nxt), nk
        unflipped += k == teeth[t]
    print(
        f"   the mutant, the click teeth not flipped by the mirror: rounds whose teeth return: {unflipped} of {n}"
    )

    print(
        "\n4. The birth, by every area from -3 keys to 3 keys at every key from 1 to 40 (a take and its give):"
    )
    for name, born in (
        ("(key - 1) div 2", lambda key: carry(key - 1, 2, 0)[0]),
        ("key div 2", lambda key: carry(key, 2, 0)[0]),
        ("0", lambda key: 0),
    ):
        odd_missed = even_missed = 0
        for small in range(1, 41):
            b = born(small)
            misses = sum(1 for area in range(-3 * small, 3 * small) if sum(books(small, b, area)) != 0)
            _, parity = carry(small, 2, 0)
            odd_missed += misses * parity
            even_missed += misses * (1 - parity)
        print(
            f"   born at {name}: areas whose take and give are not opposite clicks: odd keys {odd_missed}, even keys {even_missed}"
        )

    print(
        "\n5. Born at 0 on the act (Animate's mutant), the same run: the giver's and the taker's clicks"
    )
    s, k, unbalanced, count_give, count_take = start, (0, 0), 0, 0, 0
    for _ in range(click.ROUNDS):
        s, k, q = tick(layout, s, k, key)
        count_give += q[0]
        count_take += q[1]
        unbalanced += count_give + count_take != 0
    print(f"   rounds where the giver's count is not minus the taker's: {unbalanced} of {n}")


if __name__ == "__main__":
    main()
