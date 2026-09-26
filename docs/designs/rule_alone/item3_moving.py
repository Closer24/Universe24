"""ITEM 3 of record 2134: a bound record put in motion (the mode times the character of K,
9.94 (6)) keeps its shape and its speed, and its clock slows. The rule alone with the one seam.

The board [240, 32, 32], periodic on every axis (no face). One body of s = 2000 on a well of
side 5 at the kind [800, 850], its record the bound mode times the character at the group pace
v along x (both levels split about the standing start, 9.98 (9) (b)). The content is the hold
alone, s on the well's Nodes, moving with the well (a first run stepped the gravity time part on
this fully periodic board: with no face to sink it the content floods the board, the pace falls
and the record blows up at t = 1050; not read; the flooding is the board's, not the rule's). The
well hops to the Node nearest the envelope's centroid over its support (the box of half-width 5
about the well, 9.98 (8); the envelope read with the pair's own cosine at each Node; a first run
took the centroid over the whole board, which the mode's tail pulls, and the well wandered even
at rest: not read). Read every 50 intervals: the centroid (the speed), the width along x and
across (the shape), and the pair's phase at the well's centre Node (its unwrapped advance per
interval is the clock's rate). The same run at v = 0 is the control (the rest clock). HOST.

    PYTHONPATH=src python docs/designs/rule_alone/item3_moving.py [v] [intervals] [free]

With the third argument `free` the same record runs with no well and no content (the kind
everywhere): the control that shows whether the character K moves a record when nothing pins it.
"""

from __future__ import annotations

import json
import math
import sys
import time
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import bodies as B  # noqa: E402
import rule_alone as R  # noqa: E402

SHAPE = (240, 32, 32)
WRAP = (True, True, True)
AMOUNT = 2000
EVERY = 50
HALF = 5  # the support's window about the well, the seam's tally (9.98 (8))


def phase_of(now: int, before: int, cos_omega: float) -> float:
    """The pair's phase: now = A cos(phi), before = A cos(phi - omega)."""
    sin_omega = math.sqrt(max(1.0 - cos_omega * cos_omega, 1e-12))
    # before = A (cos phi cos omega + sin phi sin omega) -> sin phi = (before - now cos omega) / sin omega
    return math.atan2(before - now * cos_omega, now * sin_omega)


def run(speed: float, intervals: int, free: bool = False, seam: str = "centroid") -> dict:
    middle = SHAPE[1] // 2
    body = B.Body([60, middle, middle], AMOUNT)
    t0 = time.time()
    profile, clock = B.bound_mode(SHAPE, WRAP, body)
    if speed != 0.0:
        now, before, numbers = B.moving_record(profile, body, SHAPE, WRAP, 0, speed, clock)
    else:
        now, before, numbers = profile.copy(), profile.copy(), {}
    rem = np.zeros(SHAPE, dtype=R.INT)
    seeding = time.time() - t0
    readings = []
    phases = []  # the pair's phase at the well's centre Node, every interval
    hops = 0
    carried = [0.0, 0.0, 0.0]
    paces = []
    t0 = time.time()
    for t in range(intervals + 1):
        content = np.zeros(SHAPE, dtype=R.INT)
        if free:
            num = np.full(SHAPE, body.kind[0], dtype=R.INT)
            den = np.full(SHAPE, body.kind[1], dtype=R.INT)
        else:
            content[body.mask(SHAPE)] = body.amount  # the hold alone
            num, den = body.pairs(SHAPE)
        read, own, wall = R.coefficients(num, den, content)
        cos_omega = B.pair_cosine(num, den)
        c = tuple(body.centre)
        phases.append(phase_of(int(now[c]), int(before[c]), clock[0] / (2.0 * clock[1])))
        if t % EVERY == 0:
            e2 = R.envelope_squared(now, before, cos_omega)
            cx, cy, cz = B.window_centroid(e2, body.centre, HALF, SHAPE, WRAP)
            xs = np.arange(SHAPE[0]).reshape(-1, 1, 1)
            ys = np.arange(SHAPE[1]).reshape(1, -1, 1)
            dx = ((xs - cx + SHAPE[0] / 2) % SHAPE[0]) - SHAPE[0] / 2
            width_x = float(np.sqrt((e2 * dx**2).sum() / e2.sum()))
            width_y = float(np.sqrt((e2 * (ys - cy) ** 2).sum() / e2.sum()))
            readings.append(
                {
                    "t": t,
                    "x": cx,
                    "well_x": body.centre[0],
                    "width_x": width_x,
                    "width_y": width_y,
                    "peak": int(np.abs(now).max()),
                    "hops": hops,
                }
            )
        if t == intervals:
            break
        now, before, rem = R.step(now, before, rem, read, own, wall, WRAP)
        e2 = R.envelope_squared(now, before, cos_omega)
        if seam == "current":
            pace = B.current_pace(now, before, num, den, cos_omega, body.centre, HALF, SHAPE, WRAP)
            paces.append(pace[0])
            if B.hop_by_pace(body, carried, pace, SHAPE, WRAP):
                hops += 1
        elif B.hop(body, B.window_centroid(e2, body.centre, HALF, SHAPE, WRAP), SHAPE, WRAP):
            hops += 1  # free: the window follows the packet; nothing else changes
    # the clock's rate: the phase's total advance over the run (unwrapped), per interval
    unwrapped = np.unwrap(np.array(phases))
    rate = float((unwrapped[-1] - unwrapped[0]) / (len(unwrapped) - 1))
    return {
        "speed": speed,
        "free": free,
        "seam": seam,
        "pace_read_mean": float(np.mean(paces)) if paces else None,
        "shape": SHAPE,
        "amount": AMOUNT,
        "clock": clock,
        "moving_numbers": numbers,
        "phase_rate_per_interval": abs(rate),
        "seeding_seconds": seeding,
        "host_seconds": time.time() - t0,
        "readings": readings,
    }


def main() -> None:
    speed = float(sys.argv[1]) if len(sys.argv) > 1 else 0.1
    intervals = int(sys.argv[2]) if len(sys.argv) > 2 else 1500
    free = len(sys.argv) > 3 and sys.argv[3] == "free"
    seam = "current" if "current" in sys.argv[3:] else "centroid"
    result = run(speed, intervals, free, seam)
    out = (
        Path(__file__).resolve().parent
        / f"item3_moving_v{speed}{'_free' if free else ''}{'_current' if seam == 'current' else ''}.json"
    )
    out.write_text(json.dumps(result, indent=1) + "\n", encoding="utf-8")
    for r in result["readings"]:
        print(
            f"t {r['t']:5d}  x {r['x']:9.3f}  well {r['well_x']:3d}  width_x {r['width_x']:6.2f}  width_y {r['width_y']:6.2f}  peak {r['peak']}  hops {r['hops']}"
        )
    print(
        "moving numbers (HOST, the dispersion's):",
        {k: round(v, 5) for k, v in result["moving_numbers"].items()},
    )
    print("seam:", result["seam"], "; the pace read from the current, mean:", result["pace_read_mean"])
    print(
        f"the pair's phase rate at the well's centre: {result['phase_rate_per_interval']:.5f} per interval; clock {result['clock']}"
    )
    print(
        f"HOST seeding {result['seeding_seconds']:.1f} s, run {result['host_seconds']:.1f} s; written {out.name}"
    )


if __name__ == "__main__":
    main()
