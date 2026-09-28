"""The reader of worlds (a) and (b) of the rule's own universe (ALGEBRA.md THE COLOURS ARE THE THREE AXES; the Closer's assignment of 2026-09-28, 13:52 Israel): from a world and its runner output, the clicks at the pixel's detector and their tallies per axis: the net tally (the sum of the components) and the raw (the sum of the magnitudes) per axis, the net per interval at the peak interval, the net and the raw over the three axes, the first click's interval, against the expectation file's `axes` section (Cheshbon's blind numbers before the run): the net 0 on every axis reads white, the net leaning along one axis reads the pull; and with `--run`, the world run headless through the engine's own functions and the count's line's moves read per axis from the pixel's count and its six neighbours' every interval (a quantum that leaves through a Port arrives at that neighbour: the change at the +a neighbour less the change at the -a one is the net move along the axis, the two magnitudes the raw), with the pixel's own count along the run (GAMEBOARD); a reader of the clicks and the counts, no law."""

from __future__ import annotations

import json
import sys
from collections import defaultdict
from fractions import Fraction
from pathlib import Path
from typing import Any


def clicks_at(output: dict[str, Any], detector: str) -> list[dict[str, Any]]:
    """The clicks at the detector in the order of their intervals, those with a tally."""
    found = [c for c in output.get("clicks", []) if c.get("detector") == detector and c.get("tally")]
    return sorted(found, key=lambda c: int(c["interval"]))


def over_axes(values: list[int]) -> list[list[int]]:
    """The three values over the largest magnitude among them as exact rationals [numerator, denominator]; 0 : 0 : 0 where all vanish."""
    largest = max((abs(v) for v in values), default=0)
    return [
        [Fraction(v, largest).numerator, Fraction(v, largest).denominator] if largest else [0, 1]
        for v in values
    ]


def tally_rows(output: dict[str, Any], axes: dict[str, Any]) -> dict[str, Any]:
    """THE COLOURS ARE THE THREE AXES: per axis the net tally and the raw over all clicks at the detector, the net per interval at the interval where the net along the leaning axis peaks, the net and the raw over the axes, the first click's interval; MATCH when the peak's net lies within `band` of `net_per_interval` on every axis, else MISS, or the reading alone while no band is written; `white` where the net vanishes on every axis."""
    clicks = clicks_at(output, str(axes["detector"]))
    tallies = [[int(t) for t in c["tally"]] for c in clicks]
    net = [sum(t[a] for t in tallies) for a in range(3)]
    raw = [sum(abs(t[a]) for t in tallies) for a in range(3)]
    per_interval: dict[int, list[int]] = defaultdict(lambda: [0, 0, 0])
    for click, tally in zip(clicks, tallies, strict=True):
        for a in range(3):
            per_interval[int(click["interval"])][a] += tally[a]
    expected, band = axes.get("net_per_interval"), axes.get("band")
    leaning = max(range(3), key=lambda a: abs(expected[a]) if expected else 0)
    peak_interval = max(per_interval, key=lambda t: abs(per_interval[t][leaning]), default=None)
    peak = per_interval[peak_interval] if peak_interval is not None else None
    if not clicks:
        verdict = "no click at the detector"
    elif expected is None or band is None:
        verdict = "no band yet"
    else:
        within = all(abs(peak[a] - int(expected[a])) <= float(band) for a in range(3))
        verdict = "MATCH" if within else "MISS"
    return {
        "kind": "axes",
        "detector": axes["detector"],
        "clicks": len(clicks),
        "first_click": int(clicks[0]["interval"]) if clicks else None,
        "net": net,
        "raw": raw,
        "net_over_axes": over_axes(net),
        "raw_over_axes": over_axes(raw),
        "peak_interval": peak_interval,
        "net_per_interval_at_peak": peak,
        "white": bool(clicks) and all(v == 0 for v in net),
        "expected": {"net_per_interval": expected, "first_click": axes.get("first_click"), "band": band},
        "verdict": verdict,
    }


def moves_per_axis(series: list[list[int]]) -> dict[str, Any]:
    """The count's line's moves per axis from the counts at the pixel's Node and its six neighbours (+x, -x, +y, -y, +z, -z) interval by interval: per interval the net along each axis (the change at the + neighbour less the change at the - one) and the raw (the two magnitudes), summed over the run, the peak interval by the largest net, the ratios over the axes."""
    per_interval = []
    for before, after in zip(series, series[1:], strict=False):
        delta = [a - b for a, b in zip(after, before, strict=True)]
        net = [delta[1 + 2 * a] - delta[2 + 2 * a] for a in range(3)]
        raw = [abs(delta[1 + 2 * a]) + abs(delta[2 + 2 * a]) for a in range(3)]
        per_interval.append((net, raw))
    net = [sum(n[a] for n, _ in per_interval) for a in range(3)]
    raw = [sum(r[a] for _, r in per_interval) for a in range(3)]
    peak = max(
        range(len(per_interval)), key=lambda t: max(abs(v) for v in per_interval[t][0]), default=None
    )
    return {
        "kind": "moves",
        "label": "GAMEBOARD",
        "intervals": len(per_interval),
        "net": net,
        "raw": raw,
        "net_over_axes": over_axes(net),
        "raw_over_axes": over_axes(raw),
        "peak_interval": None if peak is None else peak + 1,
        "net_per_interval_at_peak": None if peak is None else per_interval[peak][0],
        "first_move": next((t + 1 for t, (_, r) in enumerate(per_interval) if any(r)), None),
        "pixel_count": {"start": series[0][0], "end": series[-1][0], "least": min(s[0] for s in series)},
        "white": bool(per_interval) and all(v == 0 for v in net),
    }


def period_of(levels: list[int]) -> float | None:
    """The period in intervals from the sign changes of the level at the Node (two changes per period); None under two changes."""
    signs = [(v > 0) - (v < 0) for v in levels if v != 0]
    changes = sum(1 for a, b in zip(signs, signs[1:], strict=False) if a != b)
    return None if changes < 2 else round(2 * (len(levels) - 1) / changes, 2)


def record_reading(
    levels: list[int], counts: list[int], record: dict[str, Any] | None
) -> dict[str, Any]:
    """THE RECORD (GAMEBOARD): the pixel's record at its Node over the run: the period from the level's sign changes, the amplitude b = max|level| over the last period, the count over the last period (the mean of the held counts at the Node, else the last ten intervals); against Cheshbon's table from the generator run as Rule3 in integers (15:43 Israel: b and the period per count) within one quantum and one interval, or the reading alone."""
    period = period_of(levels)
    window = int(round(period)) if period else 10
    recent, amplitude = counts[-window:], max((abs(v) for v in levels[-window:]), default=None)
    read: dict[str, Any] = {
        "label": "GAMEBOARD",
        "period_intervals": period,
        "amplitude_b": amplitude,
        "count_over_the_last_period": round(sum(recent) / len(recent), 2) if recent else None,
        "expected": record,
    }
    if record and record.get("b") is not None and amplitude is not None:
        read["b_verdict"] = "MATCH" if abs(amplitude - int(record["b"])) <= 1 else "MISS"
    if record and record.get("period") is not None:
        read["period_verdict"] = (
            "MISS"
            if period is None
            else ("MATCH" if abs(period - float(record["period"])) <= 1 else "MISS")
        )
    return read


def run_moves(
    world_path: Path, axes: dict[str, Any], record: dict[str, Any] | None = None
) -> dict[str, Any]:
    """The world run headless with the engine's own functions, the counts at the pixel's Node and its six neighbours read from the loop's block after every interval (GAMEBOARD), the moves per axis from them, the record's level at the Node every interval and its reading (the period, b, the count over the last period) against the blind `record`; a refusal in the run is named with its interval."""
    from event_universe.events.detector_law import DetectorLawSimulation
    from event_universe.world_files import load_world

    world = load_world(world_path)
    document = json.loads(world_path.read_text(encoding="utf-8"))
    shape, node = document["shape"], document["measured"][0]["nodes"][0]["node"]
    around = [list(node)] + [
        [(node[0] + dx) % shape[0], (node[1] + dy) % shape[1], (node[2] + dz) % shape[2]]
        for dx, dy, dz in ((1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, 1), (0, 0, -1))
    ]
    simulation = DetectorLawSimulation(world)
    block = simulation.blocks[0]
    series, support, levels, refusal = [], [], [], None
    for _ in range(world.ticks):
        try:
            simulation.step()
        except (RuntimeError, ValueError) as stop:
            refusal = f"at interval {simulation.tick + 1}: {stop}"
            break
        series.append([int(block.counts[x, y, z]) for x, y, z in around])
        if block.own is not None:
            levels.append(int(block.own.now[node[0], node[1], node[2]]))
        if (simulation.tick % 10 == 0 or simulation.tick < 10) and block.own is not None:
            level = int(
                block.own.now[node[0], node[1], node[2]]
            )  # the record's support, its level at the Node
            support.append((simulation.tick, int((block.own.now != 0).sum()), level))
    rows = moves_per_axis(series) if len(series) > 1 else {"kind": "moves", "intervals": len(series)}
    return {
        "refusal": refusal,
        "ticks_run": simulation.tick,
        "expected": axes.get("net_per_interval"),
        "records_alive": len(simulation.records),
        "record_support": support,
        "record": record_reading(levels, [row[0] for row in series], record),
        **rows,
    }


def report(world: Path, output: Path) -> dict[str, Any]:
    """The reading of one world and its output: the `axes` row where the expectation declares it, MATCH or MISS or the reading alone."""
    expectation = json.loads(world.with_suffix(".expectation.json").read_text(encoding="utf-8"))
    found = json.loads(output.read_text(encoding="utf-8"))
    rows: dict[str, Any] = {"world": world.name, "output": output.name, "verdict": found.get("verdict")}
    if "axes" in expectation:
        rows["axes"] = tally_rows(found, expectation["axes"])
    return rows


def main() -> None:
    if len(sys.argv) > 2 and sys.argv[1] == "--run":
        for argument in sys.argv[2:]:
            world = Path(argument).resolve()
            blind = json.loads(world.with_suffix(".expectation.json").read_text(encoding="utf-8"))
            axes = blind.get("axes", {})
            record = blind.get("blind", {}).get("record")
            text = json.dumps({"world": world.name, **run_moves(world, axes, record)}, indent=1)
            print(text)
            world.with_name(f"{world.stem}.moves.json").write_text(text + "\n", encoding="utf-8")
        return
    arguments = [Path(a).resolve() for a in sys.argv[1:]]
    worlds, outputs = arguments[0::2], arguments[1::2]
    if not worlds or len(worlds) != len(outputs):
        raise SystemExit(
            "usage: axis_tallies.py <world.json> <output.json> [...] | --run <world.json> [...]"
        )
    for world, output in zip(worlds, outputs, strict=True):
        text = json.dumps(report(world, output), indent=1)
        print(text)
        output.with_suffix(".axes.json").write_text(text + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
