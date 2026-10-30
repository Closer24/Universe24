"""The drive tooth's mirror on an odd row, measured on the act in whole numbers (the Boss's code writer, 2026-10-30;
G2's mathematician's N3 on term 5's third text): the example universe (light, A1 of two parts; the metric family) on a
cube of 3, the drive's teeth T_d = 7 on the square's ten rows, the push at the probe's own strength, no file's.

Clock: on an odd row (the 0i slots) the mirror negates the counts, so the source J the drive carries is negated under
time's reversal; the carry's sign law then needs the drive's fine tooth kept, not flipped: n + r = q T + r' and
-n + r' = -q T + r, where the even rows' flip, T - 1 - r, undoes a carry of the same J.
Algebra: the drive alone, J = 8 at T_d = 5, over its five teeth: the tooth kept returns -q and r at every tooth, the
tooth flipped at 1 and 0 of 5.
Board: 12 rows at 27 sites; T_d = 7 on the square's rows, so the fine tooth moves wherever J is no multiple of 7; the
run back 12 rounds on all ten slots, on the even slots and on the odd, with the mirror as built and with the flip on
every row (the mutant); the 24 under the push with T_d = 7, a turn that negates a row flipping its fine tooth in its
teeth by the same sign law (the tests' turn, written for T_d = 1, leaves the tooth as it stands).
Clicks: n/a: the probe reads the board from outside.

Run: .venv/bin/python tools/derivations/open_items/derive/boss/drive_mirror/probe.py; its output is probe.txt beside it.
"""

import json
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[6]
sys.path.insert(0, str(ROOT / "src"))

from tensor24 import main  # noqa: E402
from tensor24.algebra.carry import carry, flip  # noqa: E402
from tensor24.engine import step  # noqa: E402
from tensor24.engine.state import State  # noqa: E402
from tensor24.runner import load as loading  # noqa: E402
from tensor24.runner.files import sites_of  # noqa: E402

SHAPE = [3, 3, 3]
ROUNDS = 12
TEETH = 7  # the drive's teeth on the square's rows
UNIVERSE = json.loads((ROOT / "examples" / "tensor24" / "universe.json").read_text(encoding="utf-8"))
GRIP = (
    UNIVERSE["integers"]["den"] * UNIVERSE["integers"]["full_rate"] * UNIVERSE["integers"]["full_rate"]
)
STRENGTH, _ = carry(GRIP, 1000, 0)  # the push's strength, the probe's own, as term 5's probe has it


def recurrence(seed):
    """Whole numbers from a fixed recurrence, each step one carry: no random module."""
    v = seed
    while True:
        _, v = carry(v * 6364136223846793005 + 1442695040888963407, 1 << 64, 0)
        yield v


def drawn(src, low, high):
    """A whole number in [low, high] from the recurrence's high bits, by two carries."""
    top, _ = carry(next(src), 1 << 33, 0)
    _, x = carry(top, high - low + 1, 0)
    return low + x


def world(strength, lay, seed=6):
    """The example universe at the strength given on the cube, its gears laid by `lay(train, component, site, src)`."""
    universe = json.loads(json.dumps(UNIVERSE))
    universe["chosen"]["push"] = strength
    sites = sites_of(SHAPE)
    made = main.made(loading.star(len(SHAPE)))
    empty, _ = loading.load(universe, {"version": 1, "gears": []}, sites, *made)
    src = recurrence(seed)
    gears = []
    for t in range(len(empty.trains)):
        train = empty.trains[t]
        for component in range(train.rows()):
            for x in range(sites):
                a, b, r = lay(train, component, x, src)
                gears.append([t, component, x, a, b, r])
    held, laid = loading.load(universe, {"version": 1, "gears": gears}, sites, *made)
    assert not laid, laid
    return held, main.layout(universe, SHAPE, held), State(*held.state)


def moving(train, component, x, src):
    """A hand moving: the light's components drawn with strides in [-30, 30] counts a round; the metric at 0."""
    if train.square:
        return 0, 0, 0
    a = drawn(src, -1000, 1000)
    return a, a - drawn(src, -30, 30), 0


def same(s, t, rows=None):
    """The states equal bit for bit, on every row or on the rows given (the click tooth per train, whole)."""
    if rows is None:
        return all(bool(np.array_equal(x, y)) for x, y in zip(s, t, strict=True))
    return all(
        bool(np.array_equal(x[rows], y[rows])) for x, y in zip(s[:-1], t[:-1], strict=True)
    ) and bool(np.array_equal(s.k, t.k))


def slots(held):
    """The square's rows: 00, the three 0i, the three ii, the three jk."""
    first = next(int(held.trains[t].first) for t in range(len(held.trains)) if held.trains[t].square)
    return (
        first,
        [first + 1 + i for i in range(3)],
        [first + 4 + i for i in range(3)],
        [first + 7 + i for i in range(3)],
    )


def geared(layout, rows, teeth):
    """The layout with the drive's teeth set on the rows given, every other row's as laid (1)."""
    drive = layout.gearing.drive * np.ones(layout.gearing.rest.shape, dtype=object)
    for row in rows:
        drive[row, 0] = teeth
    return layout._replace(gearing=layout.gearing._replace(drive=drive))


def flipping(layout, s):
    """The mutant mirror: the drive's tooth flipped on every row, the odd rows' too."""
    return step.mirror(layout, s)._replace(rd=flip(s.rd, layout.gearing.drive))


def unticked_flipping(layout, s):
    return flipping(layout, step.tick(layout, flipping(layout, s)))


def report():
    out = []

    def say(line):
        print(line)
        out.append(line)

    say(
        f"The drive tooth's mirror on an odd row: the example universe on a cube of 3, T_d = {TEETH} on the square's rows"
    )
    # 1. the drive alone: J = 8 at T_d = 5 over its five teeth, the run back with -J and the tooth kept or flipped
    j, d = 8, 5
    kept_q = kept_r = flipped_q = flipped_r = 0
    for r in range(d):
        q, r1 = carry(j, d, r)
        q2, r2 = carry(-j, d, r1)
        q3, r3 = carry(-j, d, flip(r1, d))
        kept_q, kept_r = kept_q + int(q2 == -q), kept_r + int(r2 == r)
        flipped_q, flipped_r = flipped_q + int(q3 == -q), flipped_r + int(r3 == r)
    say(
        f"1. the drive alone, J = {j} at T_d = {d}, the run back with -J: the tooth kept returns -q at {kept_q} of {d} teeth"
        f" and the tooth at {kept_r} of {d}; the tooth flipped returns -q at {flipped_q} of {d} and the tooth at {flipped_r} of {d}"
    )
    # 2. the board: T_d = TEETH on the square's rows, the hand moving under the push, 12 rounds out and back
    held, layout, s0 = world(STRENGTH, moving)
    s00, s0i, sii, sjk = slots(held)
    square = [s00, *s0i, *sii, *sjk]
    even_rows = [r for r in range(s0.a.shape[0]) if r not in s0i]
    layout = geared(layout, square, TEETH)
    states = [s0]
    for _ in range(ROUNDS):
        states.append(step.tick(layout, states[-1]))
    moved = int((states[1].rd[s0i] != states[0].rd[s0i]).sum())
    say(
        f"2. the hand moving under the push at the strength {STRENGTH}, T_d = {TEETH} on the square's rows: the odd rows'"
        f" fine tooth moved at {moved} of {3 * sites_of(SHAPE)} gears in round 1 (J no multiple of {TEETH} there)"
    )
    for name, untick in (
        ("the mirror as built, the odd rows' tooth kept", step.untick),
        ("the mutant, the tooth flipped on every row", unticked_flipping),
    ):
        backs = [untick(layout, states[n + 1]) for n in range(ROUNDS)]
        whole = sum(same(b, states[n]) for n, b in enumerate(backs))
        evens = sum(same(b, states[n], even_rows) for n, b in enumerate(backs))
        odds = sum(same(b, states[n], s0i) for n, b in enumerate(backs))
        end = states[-1]
        for _ in range(ROUNDS):
            end = untick(layout, end)
        say(
            f"   {name}: untick(tick s) = s on all ten slots and the light in {whole} of {ROUNDS} rounds, on the even rows"
            f" alone in {evens} of {ROUNDS}, on the odd 0i rows alone in {odds} of {ROUNDS}; the {ROUNDS} rounds rewound bit"
            f" for bit: {same(end, s0)}"
        )
    twice = sum(same(step.mirror(layout, step.mirror(layout, st)), st) for st in states)
    say(f"   mirror twice the identity at {twice} of {ROUNDS + 1} states")
    # 3. the 24 under the push with T_d = TEETH
    sys.path.insert(0, str(ROOT))
    from tests import frame
    from tests.test_the_tensor24_run import turned

    def turned_drive(m, st):
        """The state turned by m, the tests' turn with the drive's fine tooth turned too: a negated row's flipped in its teeth, T - 1 - r_d, as the carry's sign law has it."""
        there = turned(m, layout, held, st, SHAPE)
        moved = turned(
            m, layout, held, st._replace(r=st.rd), SHAPE
        ).r  # r_d on a kept row, -1 - r_d on a negated one
        negated = turned(
            m, layout, held, st._replace(r=0 * st.rd), SHAPE
        ).r  # 0 on a kept row, -1 on a negated one
        return there._replace(rd=moved - layout.gearing.drive * negated)

    held24, plain24 = [0] * 6, [0] * 6
    for m in frame.turns():
        t, u = turned_drive(m, s0), turned(m, layout, held, s0, SHAPE)
        for n in range(6):
            t, u = step.tick(layout, t), step.tick(layout, u)
            held24[n] += same(t, turned_drive(m, states[n + 1]))
            plain24[n] += same(u, turned(m, layout, held, states[n + 1], SHAPE))
    say(
        f"3. the 24 under the push with T_d = {TEETH}, rounds 1 to 6: {held24} with a negated row's fine tooth flipped in"
        f" its teeth by the turn (the carry's sign law), {plain24} with the fine tooth left as it stands"
    )
    Path(__file__).with_name("probe.txt").write_text("\n".join(out) + "\n", encoding="utf-8")


if __name__ == "__main__":
    report()
