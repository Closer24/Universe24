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
- The index (v, v-m): light's phase at the probe by projection on the window (the
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
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
ARTIFACTS = ROOT / "artifacts" / "massive_record"
C = 1.0 / math.sqrt(3.0)
N_PHASE = 64
REST_WINDOW = (200, 3000)
HOLD = (1500, 9500)
# the layer pin worlds (4a): the hold after the ramp 10000 (DECLARATIONS.md section 8), read
# at rest and at k = 3 over the same window
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


def run_lines(run: Path, event: str) -> list[dict]:
    """The lines of one event kind from a run directory's `events.jsonl` (a run of
    `python -m event_universe --output <run>`, or a tracked copy); none when the file
    is missing or empty."""
    path = run / "events.jsonl"
    if not path.exists():
        return []
    found = []
    with path.open(encoding="utf-8") as stream:
        for line in stream:
            if line.strip():
                record = json.loads(line)
                if record.get("event") == event:
                    found.append(record)
    return found


def click_stamps(run: Path) -> dict[str, list[int]]:
    """The clicks of the ray law's detectors (DETECTOR), a reader of clicks only: per
    detector set, the click stamps of the records whose chosen cell is that set (the
    `gather` line's `click`, the interval its pointer crossed the first rung), sorted;
    a record escaped or taken by a face or a body outside every set is no click of a
    set. An empty train (no gather line) reads no click, no exception."""
    stamps: dict[str, list[int]] = {}
    for line in run_lines(run, "gather"):
        chosen = line.get("chosen")
        if not chosen:
            continue
        name = str(chosen[0][0])
        if name.startswith("measured:") or name.startswith("face:"):
            continue
        stamps.setdefault(name, []).append(int(line["click"]))
    return {name: sorted(found) for name, found in stamps.items()}


def screen_clicks(run: Path, prefix: str = "screen") -> dict[str, int]:
    """The ray law's screen (rows 2a, 2c, 10, M1; DETECTOR): the click count per
    detector set whose name starts with `prefix`, keyed by the set's name; a screen
    of one set per Node (`screen_<y>`) reads its clicks per Node. Zero sets on an
    empty train."""
    return {name: len(found) for name, found in click_stamps(run).items() if name.startswith(prefix)}


def light_clicks(run: Path, detector: str) -> list[int]:
    """A light detector's train (rows 4b, R2, the light clock; DETECTOR): the sorted
    click stamps at the named detector set; an empty list on an empty train."""
    return click_stamps(run).get(detector, [])


def mean_interval(stamps: list[int], window: tuple[int, int] | None = None) -> float | None:
    """The mean interval between consecutive clicks inside the window (both ends
    included), the reader of record of a received line's period; None below two
    clicks."""
    inside = [s for s in stamps if window is None or window[0] <= s <= window[1]]
    if len(inside) < 2:
        return None
    return float(np.mean(np.diff(np.array(inside, dtype=np.int64))))


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
    reading = {
        "window": list(window),
        "count": count,
        "rate_per_interval": count / span if span else math.nan,
        "click_mean_interval": (clicks[-1] - clicks[0]) / (len(clicks) - 1)
        if len(clicks) > 1
        else math.nan,
        "spectral_peak_omega": spectral_peak(sums),
        "centre_peak_omega": spectral_peak(centres) if np.any(centres) else math.nan,
        "steps": block[-1].get("steps", 0),
    }
    return reading


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
    # (i-L), (ii-L) the layer pin worlds of row 4a: the clicks' mean interval over the hold
    # [10200, 18200] at k = 3 over the rest world's over the same window (DETECTOR), the peaks
    # GAMEBOARD beside
    layer_hold = clock("layer_pin_k3_14", LAYER_HOLD)
    layer_rest = clock("layer_pin_rest_14", LAYER_HOLD)
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
    # (4b) the redshift of the moving lamp (RUN_LIST.md step 2), when its worlds exist: B's
    # clicks over the hold in the receding world over the control's (DETECTOR, `light_clicks`)
    receding = mean_interval(light_clicks(ARTIFACTS / "redshift_k3", "B"), HOLD)
    at_rest = mean_interval(light_clicks(ARTIFACTS / "redshift_control", "B"), HOLD)
    if receding is not None and at_rest is not None:
        reading = {
            "kind": "DETECTOR (B's clicks)",
            "receding_mean_interval": receding,
            "control_mean_interval": at_rest,
            "one_plus_z": receding / at_rest,
            "clicks": [
                len(light_clicks(ARTIFACTS / name, "B")) for name in ("redshift_k3", "redshift_control")
            ],
        }
        if "redshift_k3" in pins:
            reading["pin_one_plus_z"] = pins["redshift_k3"]["pin"]["one_plus_z"]
            reading["one_plus_z_over_pin"] = reading["one_plus_z"] / reading["pin_one_plus_z"]
        readings["redshift_k3"] = reading
    # (v) the index at rest
    for name in ("index_50", "index_20", "index_10"):
        pin = pins[name]["pin"]
        reading = index_reading(name, "index_reference", pin["omega"], INDEX_CELLS, INDEX_WINDOW)
        if reading:
            reading["pin_n"] = pin["n"]
            reading["n_over_pin"] = reading["n"] / pin["n"]
            reading["excess_over_pin"] = (reading["n"] - 1.0) / (pin["n"] - 1.0)
            readings[name] = {"kind": "GAMEBOARD", **reading}
    # (v-m) the index in motion
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
