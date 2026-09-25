"""The readings of the massive record kind's check worlds from their run artifacts
(`artifacts/massive_record/<world>/`), each against its pin in `expectations.json`, written
to `readings.json` beside it and printed: the engine's number reported against the
algebra's, never the algebra moved (BUILD.md section 5; the readings by kind of section
4: DETECTOR a click, GAMEBOARD a diagnostic of the rows, COMPUTATION a number of the
declaration; a reading "matches the algebra's number", never "is nature").

- The block's clock (i, ii, iii): its count (the `clock` of the last `block` line, the
  upward zero crossings of its record's sum across its cells) over the window, its rate
  per interval, the mean interval between its `click` lines, and the spectral peak of the
  `block` lines' `sum` over the window (a discrete Fourier transform of the co-moving
  sum, refined by a parabola on the peak's three bins): GAMEBOARD readings.
- The moving worlds (ii, iii-b): f / f_0 as the hold's rate over the rest world's rate on
  its own box (the rest world's box is 48^3, the moving world's 64^3: the rest mode
  differs by the periodic image, the ratio of the two boxes' omega_b printed), and as
  the hold's spectral peak over the rest world's; the pump's two signatures: light's
  energy drift per interval (the light family's `form` in the books, its first
  difference over the hold: mean and largest) and the content of the mode
  k = 2 pi / 3 along x (the `mode` lines: abs(S_0 + w S_1 + w^2 S_2)^2, w the cube root
  of unity, mean and largest over the hold).
- The clicks alone, for the ray law's screens and the light detectors' trains (RUN_LIST.md,
  the reader of record of the two slits, Sorkin's three openings, the one opening, de Broglie's fringes, the moving mass's energy, the moving emitter's redshift, Sagnac and the light clock): `clicks_of`
  turns a run's click lines into clicks (a `click` line's tick and Node; a `gather` line's
  chosen cell and its `click` interval, the Node the cell's one declared Node), `screen_clicks`
  counts them per Node of a detector row (the count centroid, the maxima's positions and the
  visibility as exact fractions), `light_clicks` reads one detector's train (the first click's
  interval from a declared birth stamp, the mean interval by the same reader as the block
  clocks above, the train's line 2 pi over it): DETECTOR readings, no value of the board read.
- The index at rest and in motion: light's phase at the probe by projection on the window (the
  design's `massive_moving_index.py`: phase = atan2(sum v cos omega t, sum v sin
  omega t)), the delay the reference's phase less the world's, n = 1 + delay / (k s)
  with k = omega / c at rest; in motion the ratio of the delay to the covariant
  expectation (n(omega') - 1) omega' gamma_m s / c with n(omega') read from the engine's
  own rest world at omega' against its reference.

Run from the repository root after the worlds have run:

    PYTHONPATH=src python examples/events/massive_record/read_runs.py
"""

from __future__ import annotations

import cmath
import json
import math
from collections import Counter
from collections.abc import Iterable
from dataclasses import dataclass
from fractions import Fraction
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
ARTIFACTS = ROOT / "artifacts" / "massive_record"
C = 1.0 / math.sqrt(3.0)
N_PHASE = 64
REST_WINDOW = (200, 3000)
HOLD = (1500, 9500)
# the muon's moving clock, the layer pin world pushed to k = 3: the hold after the ramp 10000 (DECLARATIONS.md
# section 8); the rest world (3500 intervals) is read over REST_WINDOW
LAYER_HOLD = (10200, 18200)
INDEX_WINDOW = (1000, 1800)
MOVING_WINDOW = (3400, 4300)
# the long chains regenerated on DECLARATIONS.md section 11's geometry: the window [3800, 5400]
LONG_WINDOW = (3800, 5400)
INDEX_CELLS = 12
MOVING_CELLS = 24


def lines(name: str, event: str) -> list[dict]:
    path = ARTIFACTS / name / "events.jsonl"
    if not path.exists():
        return []
    found = []
    with path.open(encoding="utf-8") as stream:
        for line in stream:
            record = json.loads(line)
            if record.get("event") == event:
                found.append(record)
    return found


def run_record(name: str) -> dict | None:
    path = ARTIFACTS / name / "run.json"
    return json.loads(path.read_text(encoding="utf-8")) if path.exists() else None


def spectral_peak(values: np.ndarray) -> float:
    """The frequency (radians per interval) of the largest bin of the transform of the
    series less its mean, refined by a parabola through the peak and its neighbours."""
    series = values - values.mean()
    if len(series) < 8:
        return math.nan
    power = np.abs(np.fft.rfft(series * np.hanning(len(series)))) ** 2
    power[0] = 0.0
    peak = int(np.argmax(power))
    if 0 < peak < len(power) - 1:
        left, mid, right = power[peak - 1], power[peak], power[peak + 1]
        shift = 0.5 * (left - right) / (left - 2 * mid + right) if (left - 2 * mid + right) else 0.0
    else:
        shift = 0.0
    return 2.0 * math.pi * (peak + shift) / len(series)


def click_mean_interval(ticks: list[int]) -> Fraction | None:
    """The mean interval between the clicks of one train, the span of the train over its
    intervals (the reader of the block clocks' click lines and of a light detector's train):
    None with fewer than two clicks."""
    if len(ticks) < 2:
        return None
    return Fraction(ticks[-1] - ticks[0], len(ticks) - 1)


def clock(name: str, window: tuple[int, int]) -> dict[str, float]:
    """The block's clock over a window: the count, its rate, the clicks' mean interval, the
    spectral peak of the summed record."""
    block = [line for line in lines(name, "block") if window[0] <= line["tick"] <= window[1]]
    clicks = [line["tick"] for line in lines(name, "click") if window[0] <= line["tick"] <= window[1]]
    if not block:
        return {}
    counts = [line["clock"] for line in block]
    sums = np.array([float(line["sum"]) for line in block])
    centres = np.array([float(line.get("centre", 0)) for line in block])
    count = counts[-1] - counts[0]
    span = block[-1]["tick"] - block[0]["tick"]
    mean_interval = click_mean_interval(clicks)
    reading = {
        "window": list(window),
        "count": count,
        "rate_per_interval": count / span if span else math.nan,
        "click_mean_interval": float(mean_interval) if mean_interval is not None else math.nan,
        "spectral_peak_omega": spectral_peak(sums),
        "centre_peak_omega": spectral_peak(centres) if np.any(centres) else math.nan,
        "steps": block[-1].get("steps", 0),
    }
    return reading


Node = tuple[int, int, int]


@dataclass(frozen=True)
class Click:
    """One click of a detector as its record line carries it: the interval of the click,
    the Node it was read at (None when the line names a set of several Nodes and no one
    Node), the cell's name, the record's birth stamp where the line carries one and the
    detector's own count (`clock`) where the world stamps it."""

    tick: int
    node: Node | None
    cell: str | None
    birth: int | None = None
    clock: int | None = None


def detector_nodes(world: dict) -> dict[str, list[Node]]:
    """The Nodes of every cell a click line can name, from the world file: each detector
    set by its name with its declared positions, each measured event as `measured:<n>`
    at its position (its span when it has one)."""
    cells: dict[str, list[Node]] = {}
    for number, entry in enumerate(world.get("measured", [])):
        origin = tuple(int(v) for v in entry["position"])
        span = entry.get("span")
        nodes: list[Node] = []
        if span is None:
            nodes.append((origin[0], origin[1], origin[2]))
        else:
            for dx in range(int(span[0]) or 1):
                for dy in range(int(span[1]) or 1):
                    for dz in range(int(span[2]) or 1):
                        nodes.append((origin[0] + dx, origin[1] + dy, origin[2] + dz))
        cells[f"measured:{number}"] = nodes
    for detector in world.get("detectors", []):
        cells[detector["name"]] = [
            (int(p[0]), int(p[1]), int(p[2])) for p in detector.get("positions", [])
        ]
    return cells


def clicks_of(records: Iterable[dict], cells: dict[str, list[Node]] | None = None) -> list[Click]:
    """The clicks among a run's record lines, in the order of their intervals: a `click`
    line is a click at its interval and its Node (the block's own clock line, the ray
    law's click at a face or a set); a `gather` line with a chosen cell is a light
    record's click under the detector law at its `click` interval (the first rung of the
    chosen cell), its Node the cell's one declared Node when `cells` (from
    `detector_nodes`) gives exactly one, else None; a gather with no chosen cell is an
    escape and not a click. Nothing else of a line is read."""
    found: list[Click] = []
    for line in records:
        event = line.get("event")
        if event == "click":
            node = line.get("node")
            found.append(
                Click(
                    tick=int(line["tick"]),
                    node=(int(node[0]), int(node[1]), int(node[2])) if node else None,
                    cell=line.get("detector"),
                    birth=None if line.get("birth") is None else int(line["birth"]),
                    clock=None if line.get("clock") is None else int(line["clock"]),
                )
            )
        elif event == "gather" and line.get("chosen"):
            cell = str(line["chosen"][0][0])
            nodes = (cells or {}).get(cell, [])
            found.append(
                Click(
                    tick=int(line["click"]),
                    node=nodes[0] if len(nodes) == 1 else None,
                    cell=cell,
                    birth=None if line.get("birth") is None else int(line["birth"]),
                    clock=None if line.get("clock") is None else int(line["clock"]),
                )
            )
    found.sort(key=lambda click: click.tick)
    return found


def _row_axis(nodes: list[Node]) -> int:
    """The axis along which a row's Nodes differ (x when they do not)."""
    for axis in range(3):
        if len({node[axis] for node in nodes}) > 1:
            return axis
    return 0


def screen_clicks(
    clicks: Iterable[Click],
    row: Iterable[Node] | None = None,
    axis: int | None = None,
    window: tuple[int, int] | None = None,
    fringe: tuple[int, int] | None = None,
) -> dict[str, object]:
    """The clicks per Node of a detector row (DETECTOR): the counts by Node (every Node of
    `row` present, a Node without a click at 0; without `row`, the clicked Nodes), the
    count centroid along the row's axis (an exact fraction; None with no click; over the
    whole row always), the positions of the maxima (each strict local maximum of the
    counts along the row, a plateau of equal counts at its middle as a fraction) and the
    visibility (max - min) / (max + min) of the counts (None when both are 0) over the
    declared fringe window `fringe`, the coordinates [low, high] along the row's axis
    inclusive, declared before the run on the row's page (an edge Node without a click
    outside it reads no visibility of 1); without one, over the whole row. A click
    without a Node (a set of several Nodes) is counted as `unplaced` and enters nothing
    else. An empty train reads zero clicks and raises nothing."""
    chosen = [click for click in clicks if window is None or window[0] <= click.tick <= window[1]]
    counts: Counter[Node] = Counter(click.node for click in chosen if click.node is not None)
    unplaced = sum(1 for click in chosen if click.node is None)
    nodes = [tuple(int(v) for v in node) for node in row] if row is not None else list(counts)
    if row is not None:
        counts = Counter({node: counts.get(node, 0) for node in nodes})
    if axis is None:
        axis = _row_axis(nodes)
    ordered = sorted(nodes, key=lambda node: node[axis])
    values = [counts[node] for node in ordered]
    total = sum(values)
    centroid = (
        Fraction(sum(count * node[axis] for node, count in zip(ordered, values, strict=True)), total)
        if total
        else None
    )
    maxima: list[Fraction] = []
    start = 0
    while start < len(values):
        end = start
        while end + 1 < len(values) and values[end + 1] == values[start]:
            end += 1
        above_left = start == 0 or values[start - 1] < values[start]
        above_right = end == len(values) - 1 or values[end + 1] < values[start]
        if values[start] > 0 and above_left and above_right and (start > 0 or end < len(values) - 1):
            maxima.append(Fraction(ordered[start][axis] + ordered[end][axis], 2))
        start = end + 1
    fringe_values = (
        [
            count
            for node, count in zip(ordered, values, strict=True)
            if fringe[0] <= node[axis] <= fringe[1]
        ]
        if fringe is not None
        else values
    )
    largest, smallest = (max(fringe_values), min(fringe_values)) if fringe_values else (0, 0)
    return {
        "kind": "DETECTOR",
        "axis": "xyz"[axis],
        "counts": {node: counts[node] for node in ordered},
        "total": total,
        "unplaced": unplaced,
        "centroid": centroid,
        "maxima": maxima,
        "fringe": list(fringe) if fringe is not None else None,
        "max": largest,
        "min": smallest,
        "visibility": Fraction(largest - smallest, largest + smallest) if largest + smallest else None,
    }


def light_clicks(
    clicks: Iterable[Click],
    birth: int | None = None,
    window: tuple[int, int] | None = None,
) -> dict[str, object]:
    """One light detector's click train (DETECTOR): the count, the first and the last
    click's interval, the first click's interval from the birth stamp (the declared
    `birth`; without one, the first click's own stamp where its line carries one), the
    interval of every click from its own record's birth stamp (`birth_intervals`, one
    per click whose line carries a stamp, in the train's order: a train of many records,
    the light clock's one record per period, reads each click against its own birth),
    the successive intervals, the mean interval by `click_mean_interval` (the reader of
    the tracked runs' block clocks, an exact fraction) and the train's line 2 pi over it
    in radians per interval (the host's conversion of that fraction). The window keeps a
    click with its own stamp. An empty train reads zero clicks, None for every interval,
    and raises nothing."""
    chosen = sorted(
        (click for click in clicks if window is None or window[0] <= click.tick <= window[1]),
        key=lambda click: click.tick,
    )
    ticks = [click.tick for click in chosen]
    own = [click.tick - click.birth for click in chosen if click.birth is not None]
    if birth is None and chosen and chosen[0].birth is not None:
        birth = chosen[0].birth
    mean_interval = click_mean_interval(ticks)
    return {
        "kind": "DETECTOR",
        "count": len(ticks),
        "first_tick": ticks[0] if ticks else None,
        "last_tick": ticks[-1] if ticks else None,
        "birth": birth,
        "first_interval": ticks[0] - birth if ticks and birth is not None else None,
        "birth_intervals": own,
        "intervals": [b - a for a, b in zip(ticks, ticks[1:], strict=False)],
        "mean_interval": mean_interval,
        "line_omega": 2.0 * math.pi / mean_interval if mean_interval else None,
    }


def pump(name: str, window: tuple[int, int]) -> dict[str, float]:
    """The pump's two signatures over a window: light's energy drift per interval (the
    books' `form` of the light family, first differences) and the mode k = 2 pi / 3."""
    record = run_record(name)
    reading: dict[str, float] = {}
    if record is not None:
        forms = [
            (entry["tick"], entry["families"]["light"]["form"])
            for entry in record.get("audit", [])
            if window[0] <= entry["tick"] <= window[1] and "light" in entry.get("families", {})
        ]
        if len(forms) > 1:
            drifts = [b[1] - a[1] for a, b in zip(forms, forms[1:], strict=False)]
            reading["light_form_first"] = forms[0][1]
            reading["light_form_last"] = forms[-1][1]
            reading["light_drift_mean_per_interval"] = sum(drifts) / len(drifts)
            reading["light_drift_largest"] = max(abs(d) for d in drifts)
    modes = [line for line in lines(name, "mode") if window[0] <= line["tick"] <= window[1]]
    if modes:
        w = cmath.exp(2j * math.pi / 3)
        contents = [abs(s[0] + w * s[1] + w * w * s[2]) ** 2 for s in (line["sums"] for line in modes)]
        reading["mode_content_mean"] = sum(contents) / len(contents)
        reading["mode_content_largest"] = max(contents)
    return reading


def probe_phase(name: str, omega: float, window: tuple[int, int]) -> tuple[float, float]:
    """The phase and the amplitude of light at the first probe over the window."""
    probes = [line for line in lines(name, "probe") if window[0] <= line["tick"] <= window[1]]
    if not probes:
        return math.nan, math.nan
    ticks = np.array([line["tick"] for line in probes], dtype=float)
    values = np.array([line["values"][0] for line in probes], dtype=float)
    phase = math.atan2(
        float(np.sum(values * np.cos(omega * ticks))), float(np.sum(values * np.sin(omega * ticks)))
    )
    return phase, float(np.max(np.abs(values)))


def wrap_angle(value: float) -> float:
    return (value + math.pi) % (2.0 * math.pi) - math.pi


def index_reading(
    world: str, reference: str, omega: float, cells: int, window: tuple[int, int]
) -> dict[str, float]:
    phase_ref, amp_ref = probe_phase(reference, omega, window)
    phase, amp = probe_phase(world, omega, window)
    if math.isnan(phase_ref) or math.isnan(phase):
        return {}
    delay = wrap_angle(phase_ref - phase)
    k = omega / C
    return {
        "window": list(window),
        "delay_rad": delay,
        "n": 1.0 + delay / (k * cells),
        "amplitude_ratio": amp / amp_ref if amp_ref else math.nan,
    }


def main() -> None:
    pins = json.loads((HERE / "expectations.json").read_text(encoding="utf-8"))["worlds"]
    # `format` names this file as a readings file and not a world (the repository's
    # convention: a world declares `law` and never `format`)
    readings: dict[str, object] = {
        "format": "massive-record-readings-v1",
        "identity": "massive-record-v1",
        "artifacts": "artifacts/massive_record/<world>/ (events.jsonl, run.json), each world run headless by python -m event_universe; the pins in expectations.json",
    }
    # (i) at rest
    for name in ("rest_20", "rest_28"):
        reading = clock(name, REST_WINDOW)
        if reading:
            pin = pins[name]["pin"]
            reading["pin_omega_b"] = pin["omega_b"]
            reading["peak_over_pin"] = reading["spectral_peak_omega"] / pin["omega_b"]
            reading["rate_over_pin"] = reading["rate_per_interval"] * 2.0 * math.pi / pin["omega_b"]
            readings[name] = {"kind": "GAMEBOARD", **reading}
    # (iii-a) the cavity
    reading = clock("cavity_24", REST_WINDOW)
    if reading:
        pin = pins["cavity_24"]["pin"]
        reading["pin_omega"] = pin["omega"]
        reading["peak_over_pin"] = reading["spectral_peak_omega"] / pin["omega"]
        reading["rate_over_pin"] = reading["rate_per_interval"] * 2.0 * math.pi / pin["omega"]
        readings["cavity_24"] = {"kind": "GAMEBOARD", **reading}
    # (ii) and (iii-b) in motion
    for name, rest in (
        ("moving_20", "rest_20"),
        ("moving_28", "rest_28"),
        ("cavity_24_moving", "cavity_24"),
    ):
        hold = clock(name, HOLD)
        base = clock(rest, REST_WINDOW)
        if hold and base:
            pin = pins[name]["pin"]
            expected = pin.get("pin_f_over_f0", pin.get("f_over_f0"))
            boxes = pin["omega_b_rest"] / pins[rest]["pin"]["omega_b"] if "omega_b_rest" in pin else 1.0
            reading = {
                "kind": "GAMEBOARD",
                "hold": hold,
                "rest": base,
                "f_over_f0_by_rate": hold["rate_per_interval"] / base["rate_per_interval"] / boxes,
                "f_over_f0_by_peak": hold["spectral_peak_omega"] / base["spectral_peak_omega"] / boxes,
                "rest_box_ratio_64_over_48": boxes,
                "pin_f_over_f0": expected,
                "pump": pump(name, HOLD),
            }
            reading["rate_over_pin"] = reading["f_over_f0_by_rate"] / expected
            reading["peak_over_pin"] = reading["f_over_f0_by_peak"] / expected
            readings[name] = reading
    # the layer pin worlds of the muon's moving clock: the clicks' mean interval over the hold
    # [10200, 18200] at k = 3 over the rest world's over [200, 3000] (DETECTOR), the peaks
    # GAMEBOARD beside
    layer_hold = clock("layer_pin_k3_14", LAYER_HOLD)
    layer_rest = clock("layer_pin_rest_14", REST_WINDOW)
    if layer_rest:
        pin = pins["layer_pin_rest_14"]["pin"]
        layer_rest["pin_omega_b"] = pin["omega_b"]
        layer_rest["peak_over_pin"] = layer_rest["spectral_peak_omega"] / pin["omega_b"]
        layer_rest["rate_over_pin"] = layer_rest["rate_per_interval"] * 2.0 * math.pi / pin["omega_b"]
        readings["layer_pin_rest_14"] = {
            "kind": "DETECTOR (the clicks); the peaks GAMEBOARD",
            **layer_rest,
        }
    if layer_hold and layer_rest:
        pin = pins["layer_pin_k3_14"]["pin"]
        expected = pin.get("pin_f_over_f0", pin.get("f_over_f0"))
        reading = {
            "kind": "DETECTOR (the clicks); the peaks GAMEBOARD",
            "hold": layer_hold,
            "rest": layer_rest,
            "f_over_f0_by_rate": layer_hold["rate_per_interval"] / layer_rest["rate_per_interval"],
            "f_over_f0_by_peak": layer_hold["spectral_peak_omega"] / layer_rest["spectral_peak_omega"],
            "pin_f_over_f0": expected,
            "pump": pump("layer_pin_k3_14", LAYER_HOLD),
        }
        reading["rate_over_pin"] = reading["f_over_f0_by_rate"] / expected
        reading["peak_over_pin"] = reading["f_over_f0_by_peak"] / expected
        readings["layer_pin_k3_14"] = reading
    # the deep well in motion (the cavity row's CONTROL, RUN_LIST.md step 3): the clicks'
    # mean interval over the hold at k = 3 over the rest world's (DETECTOR)
    deep_hold = clock("deep_well_k3_40", HOLD)
    deep_rest = clock("deep_well_rest_40", REST_WINDOW)
    if deep_rest:
        pin = pins["deep_well_rest_40"]["pin"]
        deep_rest["pin_omega_b"] = pin["omega_b"]
        deep_rest["rate_over_pin"] = deep_rest["rate_per_interval"] * 2.0 * math.pi / pin["omega_b"]
        readings["deep_well_rest_40"] = {
            "kind": "DETECTOR (the clicks); the peaks GAMEBOARD",
            **deep_rest,
        }
    if deep_hold and deep_rest:
        expected = pins["deep_well_k3_40"]["pin"]["pin_f_over_f0"]
        reading = {
            "kind": "DETECTOR (the clicks); the peaks GAMEBOARD",
            "hold": deep_hold,
            "rest": deep_rest,
            "f_over_f0_by_rate": deep_hold["rate_per_interval"] / deep_rest["rate_per_interval"],
            "f_over_f0_by_peak": deep_hold["spectral_peak_omega"] / deep_rest["spectral_peak_omega"],
            "pin_f_over_f0": expected,
            "pump": pump("deep_well_k3_40", HOLD),
        }
        reading["rate_over_pin"] = reading["f_over_f0_by_rate"] / expected
        reading["peak_over_pin"] = reading["f_over_f0_by_peak"] / expected
        readings["deep_well_k3_40"] = reading
    # (v) the index at rest
    for name in ("index_50", "index_20", "index_10"):
        pin = pins[name]["pin"]
        reading = index_reading(name, "index_reference", pin["omega"], INDEX_CELLS, INDEX_WINDOW)
        if reading:
            reading["pin_n"] = pin["n"]
            reading["n_over_pin"] = reading["n"] / pin["n"]
            reading["excess_over_pin"] = (reading["n"] - 1.0) / (pin["n"] - 1.0)
            readings[name] = {"kind": "GAMEBOARD", **reading}
    # the index in motion
    for k in (3, 4):
        for direction in ("toward", "away"):
            name = f"index_moving_k{k}_{direction}"
            pin = pins[name]["pin"]
            omega, omega_prime, gamma = pin["omega"], pin["omega_prime"], pin["gamma_m"]
            rest_prime = index_reading(
                f"index_moving_rest_k{k}_{direction}",
                f"index_moving_reference_k{k}_{direction}",
                omega_prime,
                MOVING_CELLS,
                MOVING_WINDOW,
            )
            rest_omega = index_reading(
                "index_moving_rest_omega",
                "index_moving_reference_omega",
                omega,
                MOVING_CELLS,
                MOVING_WINDOW,
            )
            moving = index_reading(
                name, "index_moving_reference_omega", omega, MOVING_CELLS, MOVING_WINDOW
            )
            if rest_prime and moving:
                expected = (rest_prime["n"] - 1.0) * omega_prime * gamma * MOVING_CELLS / C
                reading = {
                    "kind": "GAMEBOARD",
                    "rest_at_omega": rest_omega,
                    "rest_at_omega_prime": rest_prime,
                    "moving": moving,
                    "covariant_expected_delay_rad": expected,
                    "ratio_read_over_expected": moving["delay_rad"] / expected if expected else math.nan,
                    "pump": pump(name, MOVING_WINDOW),
                }
                reading["halves"] = [
                    index_reading(name, "index_moving_reference_omega", omega, MOVING_CELLS, half).get(
                        "delay_rad"
                    )
                    for half in (
                        (MOVING_WINDOW[0], (MOVING_WINDOW[0] + MOVING_WINDOW[1]) // 2),
                        ((MOVING_WINDOW[0] + MOVING_WINDOW[1]) // 2, MOVING_WINDOW[1]),
                    )
                ]
                if "ratio_read_over_expected" in pin:
                    reading["pin_ratio"] = pin["ratio_read_over_expected"]
                    reading["ratio_over_pin"] = (
                        reading["ratio_read_over_expected"] / pin["ratio_read_over_expected"]
                    )
                readings[name] = reading
        # the receding case on the longer chain
        name = f"index_moving_long_k{k}_away"
        pin = pins[name]["pin"]
        omega, omega_prime, gamma = pin["omega"], pin["omega_prime"], pin["gamma_m"]
        rest_prime = index_reading(
            f"index_moving_long_rest_k{k}_away",
            f"index_moving_long_reference_k{k}_away",
            omega_prime,
            MOVING_CELLS,
            LONG_WINDOW,
        )
        moving = index_reading(
            name, "index_moving_long_reference_omega", omega, MOVING_CELLS, LONG_WINDOW
        )
        if rest_prime and moving:
            expected = (rest_prime["n"] - 1.0) * omega_prime * gamma * MOVING_CELLS / C
            reading = {
                "kind": "GAMEBOARD",
                "rest_at_omega_prime": rest_prime,
                "moving": moving,
                "covariant_expected_delay_rad": expected,
                "ratio_read_over_expected": moving["delay_rad"] / expected if expected else math.nan,
                "halves": [
                    index_reading(
                        name, "index_moving_long_reference_omega", omega, MOVING_CELLS, half
                    ).get("delay_rad")
                    for half in (
                        (LONG_WINDOW[0], (LONG_WINDOW[0] + LONG_WINDOW[1]) // 2),
                        ((LONG_WINDOW[0] + LONG_WINDOW[1]) // 2, LONG_WINDOW[1]),
                    )
                ],
                "pump": pump(name, LONG_WINDOW),
            }
            if "ratio_read_over_expected" in pin:
                reading["pin_ratio"] = pin["ratio_read_over_expected"]
                reading["ratio_over_pin"] = (
                    reading["ratio_read_over_expected"] / pin["ratio_read_over_expected"]
                )
            readings[name] = reading
    (HERE / "readings.json").write_text(json.dumps(readings, indent=1) + "\n", encoding="utf-8")
    for name, reading in readings.items():
        if isinstance(reading, dict):
            print(name, json.dumps(reading)[:400])


if __name__ == "__main__":
    main()
