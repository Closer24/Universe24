"""ONELAW4 probe 3, a code check on F's tree (0ece4b19f): the shipped worlds laid by the files as the run lays them, and
the closure's act (as p2_closure.act4, copied: the pivot reading and the time-symmetric cross push on the new count u, laid
u = a - b) against F's act as built, the state (a, b, r, r_d, k) and the clicks compared at every round; the cross slots
counted at every round (every world lays its 0i rows at 0). argv[1] the tree, argv[2] the round cap per world, argv[3:]
the worlds (all five when none is named); the progress every 50 rounds to stderr, the result lines alone to stdout. Each
world runs the rounds the run itself runs: it stops where the run names its first departure (run.promised on the state
F's act reaches: every tooth within its dial, the wave's window, every count within the width), as the run does."""

import json
import re
import sys
from pathlib import Path

TREE = Path(sys.argv[1])
CAP = int(sys.argv[2])
sys.path.insert(0, str(TREE.joinpath("src")))
sys.path.insert(1, str(TREE))
from tensor24 import main as tensor24  # noqa: E402
from tensor24.engine import step  # noqa: E402
from tensor24.runner.files import held_departures, sites_of, star, vocabulary  # noqa: E402
from tensor24.runner.load import load  # noqa: E402
from tensor24.runner.run import promised, wide  # noqa: E402
from tests import frame  # noqa: E402

BUILT = step.momentum, step.crossing
HELD = {}


def pivot(layout, s, teeth, slots):
    a, b, tooth, _, _ = s
    return step.halves(layout) * teeth * (a - b) - (slots * step.gradient(layout, a)).sum(axis=0) + tooth


def crossing4(layout, s, slots):
    here, u = step.crossed(layout, s.a), HELD["u"]
    return step.halves(layout) * ((here * step.gradient(layout, u)).sum(axis=0) + step.divergence(layout, here * u))


def act4(layout, s, u):
    HELD["u"] = u
    step.momentum, step.crossing = pivot, crossing4
    try:
        s1, clicks = step.act(layout, s)
    finally:
        step.momentum, step.crossing = BUILT
    return s1, step.halves(layout) * (s1.a - s.a) - u, clicks


WORLDS = sys.argv[3:] or ["tensor24", "tensor24-live", "tensor24-mesh", "tensor24-well", "tensor24-click"]
for world in WORLDS:
    paths = [TREE.joinpath("examples", world, f"{name}.json") for name in ("universe", "piece", "setting")]
    universe, piece, setting = (json.loads(p.read_text(encoding="utf-8")) for p in paths)
    shape = piece["shape"]
    kinds, tables, square = tensor24.ENGINE.made(star(len(shape)))
    assert not held_departures(universe, setting, vocabulary(kinds, square))
    loaded, found = load(universe, setting, sites_of(shape), kinds, tables, square)
    assert not found
    layout = tensor24.ENGINE.layout(universe, shape, loaded)
    start = tensor24.ENGINE.state(*loaded.state)
    ticks, width = min(setting["ticks"], CAP), universe["integers"]["width"]
    x, y, u = start, start, start.a - start.b
    alike, crossed, clicked, ran, stop = True, 0, 0, 0, ""
    found = promised(tensor24.ENGINE, layout, start, width) if ticks else []
    stop = f" (the run names a departure at round 1: {found[0][:80]})" if found else ""
    for at in range(1, ticks + 1):
        if found:
            break
        x1, u, c1 = act4(layout, x, u)
        y1, c2 = step.act(layout, y)
        alike = alike and frame.same([*x1, c1], [*y1, c2])
        crossed += int(sum(1 for v in step.crossed(layout, y.a).flat if v != 0))
        clicked += int(sum(1 for v in c2.flat if v != 0))
        x, y, ran = x1, y1, at
        found = promised(tensor24.ENGINE, layout, y, width) if at < ticks else wide(y, width)
        first = re.sub(r"-?[0-9]{13,}", "<a count>", found[0]) if found else ""
        stop = f" (the run names a departure at round {at + 1}, {len(found)} of them, the first: {first})" if found else ""
        if at % 50 == 0:
            print(f"{world}: round {at} alike {alike}", file=sys.stderr, flush=True)
    print(f"{world}: {ran} of {setting['ticks']} rounds, the closure alike with F's act at every round {alike};"
          f" cross slots off 0 in all rounds {crossed}; clicks off 0 {clicked}{stop}")
