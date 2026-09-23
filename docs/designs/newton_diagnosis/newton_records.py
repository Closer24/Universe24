"""GAMEBOARD diagnostic (never a measurement): the probe's path, momentum
and kicks read off a replay's record of series D3's worlds (the `step`,
`read`, `contact` and face `click` lines of events.jsonl), for
docs/designs/newton_diagnosis/DIAGNOSIS.md section 3. Usage:

    PYTHONPATH=src python docs/designs/newton_diagnosis/newton_records.py \\
        <run folder of r12_flow> <run folder of r24_flow> ...

Each folder is one of `tools/run_series.py`'s `<world>/run` folders. The
symbols: r the distance from the source's Node in Links; n the momentum in
n-units (p / (Q M_total)); H the invariant of the ring-mean push under the
per-axis drive, sum over the axes of |n_a| - S ln(1 + |n_a| / S) plus A ln
r (constant when the push is A / r and nothing else); L the angular
momentum x n_y - y n_x in Links times n-units; u the inward radial speed
over the rows' pace c = 64 / 110."""

from __future__ import annotations

import json
import math
import sys
from collections import Counter
from pathlib import Path

Q = 64
WIDTH = 32
C = 64 / 110
A = 1.4838  # the circular balance under the key (flow_weight/ALGEBRA.md 5)
WINDOW = 15  # the smoothing of r for the extrema
SPEED_WINDOW = 20  # the half-window of the radial speed


def analyse(folder: Path) -> None:
    run = json.loads((folder / "run.json").read_text())
    init = json.loads((folder / "initialization.json").read_text())
    number = next(int(k) for k, v in run["numbers"].items() if v["family"] == "probe")
    entry = next(m for m in init["measured"] if m.get("family") == "probe")
    source = next(m for m in init["measured"] if m.get("family") == "m")
    cx, cy = source["position"][:2]
    m_held = entry["held"]["m"]
    m_total = entry["amount"] + m_held
    n_unit = Q * m_total
    steps, reads, contacts, escape = [], [], [], None
    with (folder / "events.jsonl").open() as stream:
        for line in stream:
            e = json.loads(line)
            kind = e["event"]
            if kind == "step" and e["number"] == number:
                steps.append(e)
            elif kind == "read" and e.get("measured") == number:
                reads.append(e)
            elif kind == "contact" and e.get("number") == number:
                contacts.append(e)
            elif (
                kind == "click"
                and e.get("measured") == number
                and str(e.get("detector", "")).startswith("face")
            ):
                escape = (e["detector"], e["tick"], e["node"], e["momentum"])
    print(
        f"== {folder}: the probe number {number}, M_total {m_total}, M_held {m_held}, the source at ({cx}, {cy})"
    )
    print(f"  steps {len(steps)}, reads (kicks) {len(reads)}, contacts {len(contacts)}")
    print(f"  THE ESCAPE, a face click of the probe (DETECTOR): {escape}")
    for c in contacts:
        print(
            f"  the contact (GAMEBOARD): tick {c['tick']} from {c['node'][:2]} onto {c['to'][:2]}, the occupant {c['occupant']} "
            f"took the axis {c['axis']} component {c['component']} ({c['component'] / n_unit:.2f} n-units); "
            f"the momentum after {c['momentum']}"
        )
    last = escape[1] - 1 if escape else int(run["completed_ticks"])
    pos = [None] * (last + 1)
    mom = [None] * (last + 1)
    x = tuple(entry["position"][:2])
    p = list(entry["momentum"])
    pos[0], mom[0] = x, tuple(p)
    by_tick: dict[int, list] = {}
    for e in reads:
        by_tick.setdefault(e["tick"], []).append(e)
    si = 0
    for t in range(1, last + 1):
        while si < len(steps) and steps[si]["tick"] == t:
            x = tuple(steps[si]["to"][:2])
            si += 1
        pos[t] = x
        for e in by_tick.get(t, []):
            p = [a + b for a, b in zip(p, e["push"], strict=True)]
        for c in contacts:
            if c["tick"] == t:
                p = list(c["momentum"])
        mom[t] = tuple(p)
    print(
        f"  the momentum rebuilt from the reads and the contact at the end {mom[last][:2]}; the escape click's {escape[3][:2] if escape else None}"
    )
    kicks = []
    for e in reads:
        t = e["tick"]
        if t > last:
            continue
        dx, dy = pos[t][0] - cx, pos[t][1] - cy
        r = math.hypot(dx, dy)
        k = (e["push"][0] / n_unit, e["push"][1] / n_unit)
        radial = (k[0] * dx + k[1] * dy) / r if r else 0.0
        kicks.append((t, r, math.hypot(*k), radial, e["amount"]))
    print(
        f"  the kicks: {len(kicks)}; the mean |kick| {sum(k[2] for k in kicks) / len(kicks):.3f} n-units, "
        f"the mean radial part {sum(k[3] for k in kicks) / len(kicks):.3f} (negative toward the source); "
        f"rows per read {sorted(set(k[4] for k in kicks))}; the ticks mod 10 {sorted(Counter(k[0] % 10 for k in kicks).items())}"
    )
    r_t = [math.hypot(pos[t][0] - cx, pos[t][1] - cy) for t in range(last + 1)]
    n_t = [math.hypot(*mom[t][:2]) / n_unit for t in range(last + 1)]
    angle = [math.atan2(pos[t][1] - cy, pos[t][0] - cx) for t in range(last + 1)]
    turn = [angle[0]]
    for t in range(1, last + 1):
        d = angle[t] - angle[t - 1]
        while d > math.pi:
            d -= 2 * math.pi
        while d < -math.pi:
            d += 2 * math.pi
        turn.append(turn[-1] + d)

    def invariant(t: int) -> float:
        parts = [abs(c) / n_unit for c in mom[t][:2]]
        return sum(n - WIDTH * math.log(1 + n / WIDTH) for n in parts) + A * math.log(max(r_t[t], 0.5))

    def angular(t: int) -> float:
        return ((pos[t][0] - cx) * mom[t][1] - (pos[t][1] - cy) * mom[t][0]) / n_unit

    print(f"  turns about the source to the escape: {(turn[-1] - turn[0]) / (2 * math.pi):.2f}")
    whole_turns = []
    for t in range(1, last + 1):
        if (turn[t] - turn[0]) >= 2 * math.pi * (len(whole_turns) + 1):
            whole_turns.append(t)
    print(
        f"  the turns through 2 pi, 4 pi, 6 pi at the ticks {whole_turns[:3]} "
        f"(the spacings {[b - a for a, b in zip([0] + whole_turns[:3], whole_turns[:3], strict=False)]})"
    )
    smooth = [
        sum(r_t[max(0, t - WINDOW) : t + WINDOW + 1]) / len(r_t[max(0, t - WINDOW) : t + WINDOW + 1])
        for t in range(last + 1)
    ]
    extrema = []
    for t in range(WINDOW, last - WINDOW):
        segment = smooth[t - WINDOW : t + WINDOW + 1]
        if smooth[t] == min(segment) and smooth[t] < smooth[t - 1]:
            extrema.append(("peri", t))
        if smooth[t] == max(segment) and smooth[t] > smooth[t - 1]:
            extrema.append(("apo", t))
    print("  the radial extrema (the kind, the tick, r, n, H, L, the turns):")
    previous = None
    for kind, t in extrema:
        if previous == kind:
            continue
        previous = kind
        print(
            f"    {kind:4s} t = {t:5d}  r = {r_t[t]:6.2f}  n = {n_t[t]:5.2f}  H = {invariant(t):7.3f}  L = {angular(t):7.2f}  turns = {turn[t] / (2 * math.pi):6.3f}"
        )
    print("  every 400 intervals (the tick, r, n, H, L, the turns):")
    for t in range(0, last + 1, 400):
        print(
            f"    {t:5d}  r = {r_t[t]:6.2f}  n = {n_t[t]:5.2f}  H = {invariant(t):7.3f}  L = {angular(t):7.2f}  turns = {turn[t] / (2 * math.pi):6.3f}"
        )
    kick_ticks = Counter(k[0] for k in kicks)
    impulse: dict[int, float] = {}
    for k in kicks:
        impulse[k[0]] = impulse.get(k[0], 0.0) + k[2]
    bins: dict[float, list[float]] = {}
    for t in range(SPEED_WINDOW, last - SPEED_WINDOW):
        outward = (r_t[t + SPEED_WINDOW] - r_t[t - SPEED_WINDOW]) / (2 * SPEED_WINDOW)
        u = -outward / C
        b = round(u * 5) / 5
        d = bins.setdefault(b, [0, 0, 0.0, 0.0])
        d[0] += 1
        d[1] += kick_ticks.get(t, 0)
        d[2] += impulse.get(t, 0.0)
        d[3] += 1.0 / max(r_t[t], 1.0)
    print(
        "  the arrival rate against the inward radial speed u / c (bins of 0.2; bins under 60 intervals left out):"
    )
    print("    u / c   intervals  kicks   kicks x r per interval   impulse x r per interval (n-units)")
    for b in sorted(bins):
        count, n_kicks, imp, inverse_r = bins[b]
        if count < 60:
            continue
        print(
            f"    {b:+.1f}    {count:5d}     {n_kicks:4d}      {n_kicks / inverse_r:7.3f}                 {imp / inverse_r:7.3f}"
        )


def main(argv: list[str]) -> None:
    for folder in argv:
        analyse(Path(folder))


if __name__ == "__main__":
    main(sys.argv[1:])
