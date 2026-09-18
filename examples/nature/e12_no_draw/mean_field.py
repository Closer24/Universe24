"""The mean-field prediction for experiment E12 (docs/EXPERIMENTS.md), computed
before the runs: the intensity at every mark, which a counter (a mark at
setting [1, 1] that absorbs what it clicks) should count.

The split table [6, 1, 1, 1, 1, 1] over 11 as the linear map it is on average
(the remainder rule of `field-remainder-v1` realizes the split exactly on
average, A5s Run 2 measured the engine's integers against it to a part in a
thousand at release 4096 per heading), transported on the open board in
floating point with `spread` of `examples/nature/a5_static/mean_field_gauss.py`,
the one copy of the table's map. Per-heading amounts f[j, x, y, z] hold what
arrived at a Node on heading j this interval; every interval each heading's
content is split by the table relative to its heading and walks one Link; a
source's release lands on its six neighbours on the heading toward each; a
sink (a mark that absorbs, a body) takes everything that arrives at its Node;
the open boundary takes what walks out. The arrivals of tick t are what walked
into the Node during tick t, the engine's click of tick t.

Part 1, the E9 board: the ring's four corners release per interval, from the
cycle of tick 1, what the README of E9 computes (the two departing rays of a
corner, 1 on the five headings other than their own, merged per heading:
P1 sends 2 on +X along the axis, 1 on -X and +Z along the edges, 2 on the
rest), arriving at the neighbours at tick 2; the corners themselves are
ordinary Nodes for light and spread what reaches them. Two variants: the
seven marks absorbing (a click is an absorption, Highlights 5.4 of
2026-09-18, feature 2c) and transparent (the clicked quantum spreading on,
the rule before 2c). A drawn mark at [1, d] is the same sink for the
spreading field (a returned quantum walks back on its line and is not
spread), so its expected count is 1 / d of the counter's.

Part 2, the two-source board: two bodies releasing q per heading from the
cycle of tick 0, arriving at the neighbours at tick 1, the bodies and the
fifteen marks sinks. The amounts add whatever the phases (the coherent sum
sets the phase of the whole and never its amount, `spread_content`), so one
mean field serves the in-phase and the antiphase world; under
`born_steering` the transport itself changes and no mean field is claimed.
The phase difference the geometry gives a mark is r x dL mod N for an
emitter of rate r and the path difference dL: a body's release carries its
declared phase and light's rate is 0, so r = 0, the fringe period N / r is
infinite, and the only phase difference on the screen is the declared one
(0 in phase, 4 in antiphase) at every mark; the path differences are listed
for the record.

Run:  python examples/nature/e12_no_draw/mean_field.py [--out predictions.json]
"""

from __future__ import annotations

import argparse
import importlib.util
import json
import math
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[3]
HERE = Path(__file__).resolve().parent
HEADINGS = ((1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, 1), (0, 0, -1))
PHASE_STEPS = 8


def load(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


gauss = load("a5_static_mean_field_gauss", ROOT / "examples/nature/a5_static/mean_field_gauss.py")
worlds = load("e12_make_worlds", HERE / "make_worlds.py")
spread = gauss.spread
SPREAD = tuple(worlds.SPREAD)


class MeanField:
    """An open box. `sources` maps a Node to (six releases per heading, the first
    tick at which they arrive at the neighbours); `sinks` are the absorbing Nodes."""

    def __init__(self, shape, sources, sinks, table=SPREAD):
        self.shape = tuple(int(n) for n in shape)
        self.table = tuple(table)
        self.sinks = [tuple(s) for s in sinks]
        self.landings = []
        for node, (releases, start) in sources.items():
            for j, h in enumerate(HEADINGS):
                target = tuple(c + d for c, d in zip(node, h, strict=True))
                if any(target[a] < 0 or target[a] >= self.shape[a] for a in range(3)):
                    continue
                if releases[j]:
                    self.landings.append((j, target, float(releases[j]), int(start)))
        self._g = np.empty((6, *self.shape))

    def empty(self):
        return np.zeros((6, *self.shape))

    def walk(self, g, out):
        """Every heading's departures walk one Link; an open face loses what walks out."""
        for axis in range(3):
            jp, jm = 2 * axis, 2 * axis + 1
            lo = [slice(None)] * 3
            hi = [slice(None)] * 3
            lo[axis] = slice(None, -1)
            hi[axis] = slice(1, None)
            out[jp][tuple(hi)] = g[jp][tuple(lo)]
            out[jm][tuple(lo)] = g[jm][tuple(hi)]
            face0 = [slice(None)] * 3
            face0[axis] = 0
            last = [slice(None)] * 3
            last[axis] = -1
            out[jp][tuple(face0)] = 0.0
            out[jm][tuple(last)] = 0.0
        return out

    def arrivals(self, f, tick):
        """What arrives at tick `tick`: the spread and walk of what was on the board
        after the absorptions of tick - 1, plus the releases that land at this tick."""
        out = self.walk(spread(f, self.table, self._g), np.empty_like(f))
        for j, target, release, start in self.landings:
            if tick >= start:
                out[(j, *target)] += release
        return out

    def absorb(self, f):
        for sink in self.sinks:
            f[(slice(None), *sink)] = 0.0

    def run(self, ticks, marks, *, settle=4000, tolerance=1e-12):
        """The arrivals at each mark per tick for `ticks` ticks (a list per mark,
        index t the arrivals of tick t, t = 0 empty), then on to the steady state:
        the arrivals per interval at each mark once every mark's arrivals change
        by less than `tolerance` of themselves, and the tick that was reached."""
        f = self.empty()
        per_tick = {mark: [0.0] for mark in marks}
        last = None
        reached = None
        for tick in range(1, ticks + settle + 1):
            nxt = self.arrivals(f, tick)
            now = {mark: float(nxt[(slice(None), *mark)].sum()) for mark in marks}
            if tick <= ticks:
                for mark in marks:
                    per_tick[mark].append(now[mark])
            elif last is not None and all(
                abs(now[m] - last[m]) <= tolerance * max(now[m], 1e-300) for m in marks
            ):
                reached = tick
                break
            last = now
            self.absorb(nxt)
            f = nxt
        return per_tick, {mark: last[mark] for mark in marks}, reached


def ring_releases():
    """The release per corner and heading per interval of E9's ring (its README,
    "Computed before the run"): the R and L rays departing a corner each release 1
    on the five headings other than their own; per corner two rays, so 2 on every
    heading but the two departure headings, which get 1 each."""
    result = {}
    for k, corner in enumerate(worlds.CORNERS):
        departing = {worlds.R_PORTS[k], worlds.L_PORTS[k]}
        result[corner] = ([1 if j in departing else 2 for j in range(6)], 2)
    return result


def part1(ticks):
    marks = list(worlds.MARKS)
    out = {}
    for variant, sinks in (("absorbing", marks), ("transparent", [])):
        field = MeanField(worlds.SCREEN_SHAPE, ring_releases(), sinks)
        per_tick, steady, reached = field.run(ticks, marks)
        rows = {}
        for mark in marks:
            series = per_tick[mark]
            first = next((t for t, v in enumerate(series) if v > 0), None)
            rows[str(list(mark))] = {
                "first_tick": first,
                "steady_per_interval": steady[mark],
                "integrated": float(sum(series)),
                "integrated_by_tick": {
                    str(t): float(sum(series[: t + 1])) for t in (48, 96, 120, 240) if t <= ticks
                },
            }
        out[variant] = {"steady_state_reached_at_tick": reached, "marks": rows}
    return out


def part2(ticks, amount):
    q = amount * worlds.RELEASE[0] // worlds.RELEASE[1]
    marks = list(worlds.FRINGE_MARKS)
    sources = {source: ([q] * 6, 1) for source in worlds.SOURCES}
    field = MeanField(worlds.FRINGE_SHAPE, sources, list(worlds.SOURCES) + marks)
    per_tick, steady, reached = field.run(ticks, marks)
    rows = {}
    (x1, y1, z1), (x2, y2, z2) = worlds.SOURCES
    for mark in marks:
        series = per_tick[mark]
        x, y, z = mark
        euclid = math.dist(mark, (x1, y1, z1)) - math.dist(mark, (x2, y2, z2))
        manhattan = (abs(x - x1) + abs(y - y1) + abs(z - z1)) - (abs(x - x2) + abs(y - y2) + abs(z - z2))
        rows[str(list(mark))] = {
            "first_tick": next((t for t, v in enumerate(series) if v > 0), None),
            "steady_per_interval": steady[mark],
            "integrated": float(sum(series)),
            "integrated_by_tick": {
                str(t): float(sum(series[: t + 1])) for t in (48, 96, 240) if t <= ticks
            },
            "path_difference_links": {"euclidean": euclid, "lattice": manhattan},
            # r x dL mod N for the emitter's rate r = 0 (a body's declared phase, light's rate 0).
            "geometric_phase_difference": 0,
        }
    return {
        "release_per_heading": q,
        "steady_state_reached_at_tick": reached,
        "fringe_period_links": "infinite (emitter rate 0: N / r)",
        "declared_phase_difference": {"inphase": 0, "antiphase": worlds.ANTIPHASE},
        "marks": rows,
    }


def report(prediction):
    print("== Part 1, E9's board: the mean field at the seven marks (quanta)")
    for variant in ("absorbing", "transparent"):
        block = prediction["part1"][variant]
        print(
            f"   marks {variant}; steady state reached at tick {block['steady_state_reached_at_tick']}"
        )
        print(
            f"   {'mark':>12} {'first':>5} {'steady/interval':>15} {'240 ticks':>10} {'[1,2]':>7} {'[1,4]':>7}"
        )
        for mark, row in block["marks"].items():
            total = row["integrated"]
            print(
                f"   {mark:>12} {str(row['first_tick']):>5} {row['steady_per_interval']:>15.4f}"
                f" {total:>10.2f} {total / 2:>7.2f} {total / 4:>7.2f}"
            )
    block = prediction["part2"]
    print(
        f"\n== Part 2, two sources of {block['release_per_heading']} per heading: the mean field"
        f" at the fifteen counters (quanta); steady state at tick {block['steady_state_reached_at_tick']}"
    )
    print(
        f"   fringe period: {block['fringe_period_links']}; declared phase difference"
        f" {block['declared_phase_difference']}"
    )
    print(
        f"   {'mark':>12} {'first':>5} {'steady/interval':>15} {'240 ticks':>10} {'dL euclid':>10} {'dL lattice':>10}"
    )
    for mark, row in block["marks"].items():
        d = row["path_difference_links"]
        print(
            f"   {mark:>12} {str(row['first_tick']):>5} {row['steady_per_interval']:>15.4f}"
            f" {row['integrated']:>10.2f} {d['euclidean']:>10.3f} {d['lattice']:>10}"
        )


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("--ticks", type=int, default=worlds.TICKS)
    parser.add_argument("--amount", type=int, default=worlds.SOURCE_AMOUNT)
    parser.add_argument("--out", type=Path, default=HERE / "predictions.json")
    args = parser.parse_args(argv)
    prediction = {
        "table": list(SPREAD),
        "ticks": args.ticks,
        "part1": part1(args.ticks),
        "part2": part2(args.ticks, args.amount),
    }
    report(prediction)
    args.out.write_text(json.dumps(prediction, indent=1) + "\n", encoding="utf-8")
    print(f"\nwritten {args.out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
