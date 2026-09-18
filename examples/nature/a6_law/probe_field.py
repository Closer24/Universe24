"""Exploration probe of the field the prefill gives on the closed board of
`make_worlds.py`, read through the Simulation API (a Renderer of the live
region, not of a record; a probe, not a run of the series): the whole quanta
arriving per Node per interval, what a thing there would read, along the +Y
axis, the (0, 1, 1) diagonal and the line y = 20 + b at z = 20, tick by tick;
the parked ninths on the axis; the totals; the seconds per tick; the standing
set's record (standing-field-v1). One table per case, and the series as JSON.

Run:  python examples/nature/a6_law/probe_field.py --x 16 --fill 14 --ticks 40 [--side 41] [--b 4] [--out probe.json]
"""

from __future__ import annotations

import argparse
import json
import time
from pathlib import Path

import make_worlds
import numpy as np

from event_universe import Simulation
from event_universe.initialization import parse_initial_state


def probe(x_per_heading, fill, ticks, *, side, b, out):
    make_worlds.SIDE = side
    make_worlds.SHAPE = (side, side, side)
    make_worlds.STAR = (side // 2, side // 2, side // 2)
    make_worlds.MASSES = {"probe": (x_per_heading, fill)}
    document = make_worlds.bending_world(
        "probe", mass="probe", wait_name="w1", reading="amount", impacts=(), ticks=ticks
    )
    # The star alone: one lamp type declared, nothing seeded, nothing emitted.
    document["disturbance_types"] = [make_worlds.lamp("lamp_0", (1, 0, 0))[0]]
    star = make_worlds.STAR
    started = time.perf_counter()
    try:
        simulation = Simulation(parse_initial_state(document))
    except ValueError as error:
        print(f"X = {x_per_heading} fill {fill} on {side}^3: refused: {error}")
        return {"X": x_per_heading, "fill": fill, "side": side, "refused": str(error)}
    built = time.perf_counter() - started
    dense = simulation._spatial.dense
    fam = dense.families[0]
    cx, cy, cz = star
    radii = list(range(1, side // 2))
    axis_nodes = [(cx, cy + r, cz) for r in radii]
    diag_nodes = [(cx, cy + d, cz + d) for d in radii]

    def arrivals():
        return fam.arr_amt.sum(axis=(3, 4, 5, 6, 7))

    def parked():
        return fam.reg.sum(axis=(3, 4, 5, 6)) / 9.0

    series_axis, series_diag, series_line, totals, seconds = [], [], [], [], []
    for _ in range(ticks):
        t0 = time.perf_counter()
        simulation.step()
        seconds.append(time.perf_counter() - t0)
        a = arrivals()
        series_axis.append([int(a[n]) for n in axis_nodes])
        series_diag.append([int(a[n]) for n in diag_nodes])
        series_line.append([int(a[(x, cy + b, cz)]) for x in range(side)])
        totals.append((int(a.sum()), float(parked().sum()), int(fam.fly_amt.sum())))
    axis = np.array(series_axis)
    diag = np.array(series_diag)
    line = np.array(series_line)
    half = ticks // 2
    report = dense.standing_report()
    print(
        f"X = {x_per_heading} fill {fill} on {side}^3: built in {built:.1f} s, "
        f"{ticks} ticks at {np.mean(seconds):.2f} s/tick (last {seconds[-1]:.2f}); "
        f"totals first/last (arrivals, parked, in flight) {totals[0]} {totals[-1]}; standing {report}"
    )
    print("  r            : " + " ".join(f"{r:6d}" for r in radii))
    print("  n(r) all     : " + " ".join(f"{v:6.3f}" for v in axis.mean(axis=0)))
    print("  n(r) 2nd half: " + " ".join(f"{v:6.3f}" for v in axis[half:].mean(axis=0)))
    print(
        "  r^2 n(r) 2nd : "
        + " ".join(f"{r * r * v:6.2f}" for r, v in zip(radii, axis[half:].mean(axis=0), strict=True))
    )
    print("  n(diag d) 2nd: " + " ".join(f"{v:6.3f}" for v in diag[half:].mean(axis=0)))
    print("  parked(r)    : " + " ".join(f"{parked()[n]:6.2f}" for n in axis_nodes))
    print(f"  line b = {b}, per x, 2nd half: " + " ".join(f"{v:4.2f}" for v in line[half:].mean(axis=0)))
    print(
        f"  line b = {b}, sum over x per tick: first half {line[:half].sum(axis=1).mean():.2f}, second half {line[half:].sum(axis=1).mean():.2f}"
    )
    result = {
        "X": x_per_heading,
        "fill": fill,
        "side": side,
        "built_seconds": built,
        "seconds_per_tick": seconds,
        "axis": axis.tolist(),
        "diag": diag.tolist(),
        "line": line.tolist(),
        "totals": totals,
        "standing": report,
    }
    if out:
        Path(out).write_text(json.dumps(result), encoding="utf-8")
    return result


def main():
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("--x", type=int, default=16)
    parser.add_argument("--fill", type=int, default=14)
    parser.add_argument("--ticks", type=int, default=40)
    parser.add_argument("--side", type=int, default=make_worlds.SIDE)
    parser.add_argument("--b", type=int, default=4)
    parser.add_argument("--out")
    args = parser.parse_args()
    probe(args.x, args.fill, args.ticks, side=args.side, b=args.b, out=args.out)


if __name__ == "__main__":
    main()
