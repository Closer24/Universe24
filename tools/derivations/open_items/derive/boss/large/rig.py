"""The rig: tiny boards built and ticked on tensor24-review's committed act (engine/step.tick and untick), no engine file changed.

Every board here is built through the engine's own loader (tensor24.main.made, runner/load.load, tensor24.main.layout)
from a universe dict holding only the file's integers (den, full_rate, key, trace, width) and the trains' pinions.
"""

import sys
from fractions import Fraction
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[6] / "src"))  # the worktree's committed act

from tensor24 import main as tensor24  # noqa: E402
from tensor24.engine import step  # noqa: E402
from tensor24.runner import load  # noqa: E402

DEN = 15162856759112389  # the example's den (examples/tensor24/universe.json), act_push's


def integers(gamma: int, den: int = DEN, key: int = 36000) -> dict:
    return {"den": den, "full_rate": gamma, "key": key, "trace": 6, "width": 128}


_TABLES: dict = {}


def built(ints: dict, trains: list, shape: list, gears: list):
    """Layout and state from the files' dicts, as run.run makes them; gears rows [train, component, site, now, before, tooth]."""
    universe = {"version": 1, "integers": ints, "trains": trains, "couplings": []}
    sites = shape[0] * shape[1] * shape[2]
    if tuple(shape) not in _TABLES:
        _TABLES[tuple(shape)] = tensor24.made(tuple(shape))
    kinds, tables = _TABLES[tuple(shape)]
    loaded, found = load.load(universe, {"version": 1, "ticks": 0, "gears": gears}, sites, kinds, tables)
    assert loaded is not None, found
    layout = tensor24.layout(universe, shape, loaded)
    return layout, tensor24.ENGINE.state(*loaded.state)


def matter_hand(
    gamma: int, quanta: Fraction, pinion_off: int = 50, den: int = DEN, key: int = 36000, shape=(1, 1, 1)
):
    """A uniform matter hand (part 2: re, im) at its rest rotation cos w = pinion/den, |L|^2 sin w = quanta key / 2
    per Node-clock (BIG_PICTURE 5.1: one quantum is one swept area, Q = |L|^2 sin w = key / 2)."""
    import math

    pinion = den - den // pinion_off
    cos_w = Fraction(pinion, den)
    sin_w = math.sqrt(1 - float(cos_w) ** 2)
    l2 = float(quanta) * key / (2 * sin_w)
    big = math.isqrt(int(l2 * 10**6)) / 1000.0  # |L|
    L = round(big)
    re_now, re_before = L, round(L * float(cos_w))
    im_now, im_before = 0, -round(L * sin_w)
    sites = shape[0] * shape[1] * shape[2]
    gears = []
    for site in range(sites):
        gears.append([0, 0, site, re_now, re_before, 0])
        gears.append([0, 1, site, im_now, im_before, 0])
    train = {"name": "matter", "kinds": ["A1"], "part": 2, "pinion": pinion}
    layout, s = built(integers(gamma, den, key), [train], list(shape), gears)
    w = math.acos(float(cos_w))
    n_actual = 2 * L * L * sin_w / key
    return layout, s, {"L": L, "w": w, "quanta_per_node": n_actual}


def count_mean(layout, s) -> Fraction:
    row = layout.ruler.row
    return Fraction(int(s.a[row].sum()), s.a.shape[1])


def run(layout, s, ticks: int, keep_outs: bool = False):
    """Tick the act, every due beat firing; the time gear's mean count per tick (and the outs for the run back)."""
    allowed = np.ones((1, s.c.shape[1]), dtype=object)
    counts = [count_mean(layout, s)]
    outs = []
    for _ in range(ticks):
        s, out = step.tick(layout, s, allowed)
        counts.append(count_mean(layout, s))
        if keep_outs:
            outs.append(out)
    return s, counts, outs


def rewound(layout, s, outs):
    for out in reversed(outs):
        s = step.untick(layout, s, out)
    return s


def same(s1, s2) -> bool:
    return all(
        np.array_equal(np.asarray(x, dtype=object), np.asarray(y, dtype=object))
        for x, y in zip(s1, s2, strict=True)
    )


def bits(s) -> int:
    return max(int(abs(int(v))).bit_length() for arr in s for v in np.asarray(arr, dtype=object).ravel())


def tops(counts):
    """The ticks where the mean count stops rising after rising (local tops), and bottoms likewise."""
    t, b = [], []
    for n in range(1, len(counts) - 1):
        if counts[n] > counts[n - 1] and counts[n + 1] <= counts[n]:
            t.append(n)
        if counts[n] < counts[n - 1] and counts[n + 1] >= counts[n]:
            b.append(n)
    return t, b
