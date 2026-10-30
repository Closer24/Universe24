"""The great clock's push on stage 7b's act: rho + 3p read from the act's own arrays, and the time gear's swing under it.

usage: python3 -I act_push.py (the repository's interpreter, with numpy; about four minutes)

Beside the engine: the committed act of tensor24-review (engine/step.py and runner/load.py at 7b), driven tick by
tick on a 4 x 4 x 4 board, every due beat firing; no engine file is changed. One file train at a time beside the
time gear, which the load lays at every Node-clock:
  light, one gear, pinion = den (no spring): a standing wave along x, a = A (1, 0, -1, 0), at rest (b = a);
  matter, one gear, pinion = den - den div 50 (the mass term s D / 4 W = 1/100): a uniform mode a = A, at rest.
1. rho + 3p on the act: the time gear's source J (step.sources, the time gear's row, summed over the board), its
   mean over whole periods of the train, against the train's energy at the start, E = (1/2) SUM_meshes grip (a_i -
   a_j)^2 + (1/2) SUM_sites D a^2 (at rest the motion's part is 0). Light should read 2 and matter 1.
2. The swing under it: the time gear's count, its mean over the board, from the start at 0 to its top (the first
   tick where the mean stops rising), for light and matter at the same energy and for light at larger amplitudes.
"""

import sys
from fractions import Fraction
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[6] / "src"))  # the worktree's committed act

from tensor24 import main as tensor24  # noqa: E402
from tensor24.engine import step  # noqa: E402
from tensor24.runner import load  # noqa: E402

DEN = 15162856759112389
INTEGERS = {"den": DEN, "full_rate": 1000, "key": 36000, "trace": 6, "width": 128}
SHAPE = [4, 4, 4]
WAVE = (1, 0, -1, 0)  # cos(2 pi x / 4) at x = 0, 1, 2, 3, whole numbers


def built(train: dict, amplitude: int, pattern):
    """The layout and the state laid from the files' dicts, as run.run makes them."""
    universe = {"version": 1, "integers": INTEGERS, "trains": [train], "couplings": []}
    sites = SHAPE[0] * SHAPE[1] * SHAPE[2]
    gears = []
    for site in range(sites):
        x = site % SHAPE[0]  # the board's first axis runs fastest (runner/board.py)
        value = amplitude * pattern(x)
        if value:
            gears.append([0, 0, site, value, value, 0])
    setting = {"version": 1, "ticks": 0, "gears": gears}
    kinds, tables = tensor24.made(tuple(SHAPE))
    loaded, found = load.load(universe, setting, sites, kinds, tables)
    assert loaded is not None, found
    layout = tensor24.layout(universe, SHAPE, loaded)
    return layout, tensor24.ENGINE.state(*loaded.state)


def energy(layout, s) -> int:
    """The file train's energy at rest: half the grips' sum over the Meshes of the squared differences, plus half D a^2."""
    a = s.a[0]
    nb = layout.nb
    grip = layout.grip[0, 0]
    spring = layout.gearing.spring[0, 0]
    pairs = sum(
        int(((a[nb[k]] - a) ** 2).sum()) for k in (0, 2, 4)
    )  # each Mesh once: the +x, +y and +z Spokes
    return grip * pairs // 2 + spring * int((a * a).sum()) // 2


def source(layout, s) -> int:
    """The time gear's J summed over the board, from the act's own sources."""
    _, j = step.sources(layout, s)
    return int(j[layout.ruler.row].sum())


def run(layout, s, ticks: int):
    """Tick the act, every due beat firing; the board's summed J and the time gear's mean count each tick."""
    allowed = np.ones((1, s.c.shape[1]), dtype=object)
    js, counts = [], []
    for _ in range(ticks):
        js.append(source(layout, s))
        counts.append(Fraction(int(s.a[layout.ruler.row].sum()), s.a.shape[1]))
        s, _ = step.tick(layout, s, allowed)
    return js, counts


def top(counts):
    """The first tick where the mean count stops rising, after it has risen."""
    for n in range(1, len(counts) - 1):
        if counts[n] > 0 and counts[n + 1] <= counts[n]:
            return n, counts[n]
    return None, counts[-1]


LIGHT = {"name": "light", "kinds": ["A1"], "part": 1, "pinion": DEN}
MATTER = {"name": "matter", "kinds": ["A1"], "part": 1, "pinion": DEN - DEN // 50}


def main() -> None:
    lines = [
        "The great clock's push on stage 7b's act (the Boss, 2026-10-29); tensor24-review's committed act",
        "",
    ]
    lines.append(
        "1. rho + 3p on the act: the board's mean J over whole periods of the train, over its energy at the start"
    )
    small = (
        30  # small enough that the time gear's count stays at 0 and the ruler's read at the full rate
    )
    for name, train, pattern, ticks in (
        ("light", LIGHT, lambda x: WAVE[x], 128),
        ("matter", MATTER, lambda x: 1, 128),
    ):
        layout, s = built(train, small, pattern)
        e = energy(layout, s)
        js, counts = run(layout, s, ticks)
        ratio = Fraction(sum(js), len(js)) / e
        lines.append(
            f"   {name}: E = {e:.4e}, the mean J over {ticks} ticks = {float(Fraction(sum(js), len(js))):.4e}, "
            f"J / E = {float(ratio):.4f}; the time gear's count stayed at {max(counts)}"
        )
    lines.append("")
    lines.append(
        "2. The time gear's swing from 0 to its top under each source (the mean count over the board)"
    )
    for name, train, pattern, amplitude in (
        ("light, A = 600", LIGHT, lambda x: WAVE[x], 600),
        ("matter at light's energy", MATTER, lambda x: 1, None),
        ("light, A = 850", LIGHT, lambda x: WAVE[x], 850),
        ("light, A = 1200", LIGHT, lambda x: WAVE[x], 1200),
    ):
        if amplitude is None:  # matter's amplitude for the energy of light at A = 600
            ref_layout, ref_s = built(LIGHT, 600, lambda x: WAVE[x])
            target = energy(ref_layout, ref_s)
            amplitude = next(m for m in range(1, 10**6) if energy(*built(train, m, pattern)) >= target)
        layout, s = built(train, amplitude, pattern)
        e = energy(layout, s)
        js, counts = run(layout, s, 160)
        n, height = top(counts)
        first = Fraction(sum(js[:10]), 10)
        late = Fraction(sum(js[max(0, (n or 0) - 10) : (n or 0)]), 10) if n else None
        lines.append(
            f"   {name} (A = {amplitude}, E = {e:.3e}): the top at tick {n}, height {float(height):.1f}; "
            f"J over the first 10 ticks {float(first):.3e}, over the 10 before the top {float(late) if late else 0:.3e}"
        )
    print("\n".join(lines))


if __name__ == "__main__":
    main()
