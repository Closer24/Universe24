"""Exploration probe (not committed): the field the prefill gives on a 25^3 cube
from a star body, read through the Simulation API: whole quanta arriving per
Node per interval (what a thing there would read) along the +Y axis, the (0,1,1)
diagonal and the path line y = 12 + b, over the run's ticks; the parked ninths;
the totals. Prints one table per case."""

import json
import sys
import time
from pathlib import Path

import numpy as np

sys.path.insert(0, "/tmp/claude-0/-home-user-Universe24/0b03033a-a270-572b-b3b6-f528960b6109/scratchpad/wt-runs-a6/examples/nature/a6_law")
from make_worlds import bending_world  # noqa: E402

from event_universe import Simulation  # noqa: E402
from event_universe.initialization import parse_initial_state  # noqa: E402


def probe(x_per_heading, fill, ticks, shape=(25, 25, 25), amount=1 << 20, wait=1):
    star = (shape[0] // 2, shape[1] // 2, shape[2] // 2)
    release = [1, amount // x_per_heading]
    doc = bending_world(
        f"probe_x{x_per_heading}_t{fill}",
        shape=shape,
        star=star,
        b=-11,
        z_offsets=(11,),
        amount=amount,
        release=release,
        fill=fill,
        wait=wait,
        ticks=ticks,
    )
    # No lights: the star alone (its family list must still hold light).
    started = time.perf_counter()
    sim = Simulation(parse_initial_state(doc))
    built = time.perf_counter() - started
    dense = sim._spatial.dense
    fam = dense.families[0]
    cx, cy, cz = star
    rs = list(range(1, shape[0] // 2))
    axis_nodes = [(cx, cy + r, cz) for r in rs]
    diag_nodes = [(cx, cy + d, cz + d) for d in range(1, shape[0] // 2)]

    def arrivals():
        # whole quanta arrived this interval at each Node: sum over owner, flow, sign, port, layer
        return fam.arr_amt.sum(axis=(3, 4, 5, 6, 7))

    def parked():
        return fam.reg.sum(axis=(3, 4, 5, 6)) / 9.0

    a0 = arrivals()
    p0 = parked()
    print(f"case X={x_per_heading} fill={fill} build {built:.1f}s total arrived {a0.sum()} parked {p0.sum():.1f} fly {fam.fly_amt.sum()}")
    series_axis = []
    series_diag = []
    series_line = []
    totals = []
    t0 = time.perf_counter()
    for t in range(1, ticks + 1):
        sim.step()
        a = arrivals()
        series_axis.append([int(a[n]) for n in axis_nodes])
        series_diag.append([int(a[n]) for n in diag_nodes])
        series_line.append([int(a[(x, cy + 4, cz)]) for x in range(shape[0])])
        totals.append((int(a.sum()), float(parked().sum()), int(fam.fly_amt.sum())))
    dt = time.perf_counter() - t0
    axis = np.array(series_axis)
    diag = np.array(series_diag)
    print(f"  {ticks} ticks in {dt:.1f}s ({dt/ticks:.2f} s/tick); totals first/mid/last {totals[0]} {totals[len(totals)//2]} {totals[-1]}")
    print("  r     : " + " ".join(f"{r:6d}" for r in rs))
    print("  n(r)  : " + " ".join(f"{v:6.3f}" for v in axis.mean(axis=0)))
    print("  n first half: " + " ".join(f"{v:6.3f}" for v in axis[: ticks // 2].mean(axis=0)))
    print("  n second half: " + " ".join(f"{v:6.3f}" for v in axis[ticks // 2 :].mean(axis=0)))
    print("  r*n(r): " + " ".join(f"{r*v:6.3f}" for r, v in zip(rs, axis.mean(axis=0))))
    print("  diag d: " + " ".join(f"{d:6d}" for d in range(1, shape[0] // 2)))
    print("  n(diag): " + " ".join(f"{v:6.3f}" for v in diag.mean(axis=0)))
    line = np.array(series_line)
    print("  line b=4, per-x mean: " + " ".join(f"{v:5.2f}" for v in line.mean(axis=0)))
    print(f"  line b=4, sum over x per tick, mean {line.sum(axis=1).mean():.2f} (first 10 ticks {line[:10].sum(axis=1).mean():.2f}, last 10 {line[-10:].sum(axis=1).mean():.2f})")
    # the parked profile on the axis
    p = parked()
    print("  parked(r): " + " ".join(f"{p[n]:6.2f}" for n in axis_nodes))
    audit = sim.audit()
    print(f"  balanced {audit['balanced']}")
    return {"X": x_per_heading, "fill": fill, "axis": axis.tolist(), "diag": diag.tolist(), "totals": totals}


if __name__ == "__main__":
    out = []
    for X, fill in [(1, 30), (1, 40), (4, 25), (16, 15)]:
        try:
            out.append(probe(X, fill, 60))
        except ValueError as e:
            print(f"case X={X} fill={fill}: {e}")
    Path("/tmp/claude-0/-home-user-Universe24/0b03033a-a270-572b-b3b6-f528960b6109/scratchpad/a6law_probe.json").write_text(json.dumps(out))
