"""Term 9, the volume's notch, measured on the act in whole numbers (the Boss's code writer, 2026-10-30; a local
draft): the example universe (light, A1 of two parts; the metric family) on a cube of 3, the notch's strength
CHOSEN here as the probe's own, no file's; David's page (DAVID-TENSOR24-TERM9-NOTCH.md) followed.

Clock: each Node-clock's 00 slot and its ii trace on a spring of their own, so the board's mean swings and returns;
the polarizations, the E part and the shears, get none.
Algebra: V9 = 2 h c00^2 + h tr^2 as monomials of the vertex law, the 00 slot pushed back by -4 h c00 and each ii slot
by -2 h tr; the beat 4 sin^2 (omega / 2) = 4 h / W about the rest J_total / (4 h).
Board: 12 rows at 27 sites; a source pinned by a gliding hand (term 5's push, a steady J00), with and without the notch.
Clicks: n/a: the probe reads the board from outside.

Run: .venv/bin/python tools/derivations/open_items/derive/boss/term9_edge/probe.py; its output is probe.txt beside it.
"""

import json
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[6]
sys.path.insert(0, str(ROOT / "src"))

from tensor24 import main  # noqa: E402
from tensor24.algebra.carry import carry  # noqa: E402
from tensor24.engine import step  # noqa: E402
from tensor24.engine.state import State  # noqa: E402
from tensor24.runner import load as loading  # noqa: E402
from tensor24.runner.files import sites_of  # noqa: E402

SHAPE = [3, 3, 3]
ROUNDS = 400
UNIVERSE = json.loads((ROOT / "examples" / "tensor24" / "universe.json").read_text(encoding="utf-8"))
GRIP = (
    UNIVERSE["integers"]["den"] * UNIVERSE["integers"]["full_rate"] * UNIVERSE["integers"]["full_rate"]
)
REST = 6 * GRIP
PUSH, _ = carry(GRIP, 1000, 0)  # the push's strength, the probe's own, as term 5's probe has it
NOTCH, _ = carry(
    REST, 40000, 0
)  # the notch's strength h: 4 h / W = 1 / 10000, a beat of about 630 rounds
# the square train's components: 00; 0x 0y 0z; xx yy zz; yz zx xy
PARTS = {
    "the 00 slot": {0: 1},
    "the ii trace": {4: 1, 5: 1, 6: 1},
    "the E part, xx - yy": {4: 1, 5: -1},
    "the T2 part, yz": {7: 1},
}
READ = {"the 00 slot": 0, "the ii trace": 4, "the E part, xx - yy": 4, "the T2 part, yz": 7}


def world(push, notch, lay):
    universe = json.loads(json.dumps(UNIVERSE))
    universe["chosen"]["push"], universe["chosen"]["notch"] = push, notch
    sites = sites_of(SHAPE)
    made = main.made(loading.star(len(SHAPE)))
    empty, _ = loading.load(universe, {"version": 1, "gears": []}, sites, *made)
    gears = []
    for t in range(len(empty.trains)):
        train = empty.trains[t]
        for component in range(train.rows()):
            for x in range(sites):
                a, b, r = lay(train, component, x)
                gears.append([t, component, x, a, b, r])
    held, laid = loading.load(universe, {"version": 1, "gears": gears}, sites, *made)
    assert not laid, laid
    return held, main.layout(universe, SHAPE, held), State(*held.state)


def gliding(train, component, x):
    """A hand gliding alike at every site, a steady source: the light's first component at a stride of 30 a round."""
    return (10**6, 10**6 - 30, 0) if (not train.square and component == 0) else (0, 0, 0)


def laid(value, parts):
    """The square train's components laid uniform at the value times each part's sign, every other row at rest."""

    def lay(train, component, x):
        sign = parts.get(component, 0) if train.square else 0
        return (sign * value, sign * value, 0)

    return lay


def same(s, t):
    return all(bool(np.array_equal(x, y)) for x, y in zip(s, t, strict=True))


def square_first(held):
    return next(int(held.trains[t].first) for t in range(len(held.trains)) if held.trains[t].square)


def report():
    out = []

    def say(line):
        print(line)
        out.append(line)

    say(
        "Term 9 on the edge (step.act), whole numbers: the example universe on a cube of 3, 12 rows at 27 sites"
    )
    say(
        f"the rest teeth {REST}; the push's strength {PUSH}, the notch's h {NOTCH} (4 h / W = 1 / 10000)"
    )
    # (a) and (b): the mean under a steady source, no notch and with the notch
    for name, notch in (("no notch", 0), ("the notch", NOTCH)):
        held, layout, s = world(PUSH, notch, gliding)
        s00 = square_first(held)
        marks, sums = [], []
        for t in range(1, ROUNDS + 1):
            s = step.tick(layout, s)
            total = int(s.a[s00].sum())
            sums.append(total)
            if t in (100, 200, 300, 400):
                marks.append(f"round {t}: {total}")
        say(
            f"(a/b) a steady source (the gliding hand), {name}: the 00 slot's board sum at "
            + "; ".join(marks)
            + f"; its least {min(sums)}, its most {max(sums)}"
        )
    # (c) which slots the notch holds: each laid uniform, no source: the slot's swing over the rounds
    for name, parts in PARTS.items():
        held, layout, s = world(0, NOTCH, laid(10**9, parts))
        row = square_first(held) + READ[name]
        start = int(s.a[row, 0])
        changes, last, seen = 0, start, [start]
        for _ in range(ROUNDS):
            s = step.tick(layout, s)
            now = int(s.a[row, 0])
            seen.append(now)
            changes += int(now * last < 0)
            last = now if now else last
        alike = all(int(v) == seen[-1] for v in s.a[row])
        say(
            f"(c) {name} laid uniform at 10^9, no source, {ROUNDS} rounds: the read row's count from {start} to {seen[-1]}"
            f" (least {min(seen)}, most {max(seen)}, {changes} sign changes; alike at every site: {alike})"
        )
    # (d) the run back with the notch and the source
    held, layout, s0 = world(PUSH, NOTCH, gliding)
    s = s0
    for _ in range(ROUNDS):
        s = step.tick(layout, s)
    for _ in range(ROUNDS):
        s = step.untick(layout, s)
    say(
        f"(d) {ROUNDS} rounds out and {ROUNDS} back with the notch and the source: the lay returns bit for bit: {same(s, s0)}"
    )
    Path(__file__).with_name("probe.txt").write_text("\n".join(out) + "\n", encoding="utf-8")


if __name__ == "__main__":
    report()
