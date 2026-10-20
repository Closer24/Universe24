"""The atom's line read from a look file (tools/look/record.py's `<world>.look.json`), a lattice reading of a world of two s levels, or of one (the owner's order of 2026-10-20, the atom's own line; the design verdict of 2026-10-19, section 5, the line as the sum of two standing solutions): per interval, from the electron's two lines z = now + i second, the centre's |z| (the proton's Node), Q = SUM |z|^2, the overlap of |z| with the lay's |z| (the look's frame 0; the cosine of the two arrays, 1 at the start), the level at the centre and at r = 1 along +x over the first intervals (a lay that stands leaves them within a level), the centre's drift (its least and largest over the run against the lay's), and the spectrum of the centre's |z| over the run (the discrete transform of the trace about its mean, one bin 2 pi / (N every) per interval, every the look's stride, the peak bin's angle and amplitude): two s levels laid together beat at their difference, the line, since |z|^2 at the centre carries 2 A_1 A_2 phi_1 phi_2 cos((Omega_2 - Omega_1) t); the holder's row at the Nodes named by the blind along +x (the look's charge level, the sum of every row of the sign holder, the proton's and the electron's own) and the peaks of its spectrum beside the line, a reading and no fence; the proton's |z| at its Node. The checks against the blind (`expectation.json`, the world's entry): the spectrum's peak within the blind's bins of the line (`line_per_interval`, `line_tolerance_bins`), the overlap at the close at least the blind's (`overlap_with_the_lay_at_the_close_at_least`), the first steps' levels within the blind's levels (`first_steps_unchanged_within_levels`, over the first six intervals), the centre's drift within the blind's fraction (`centre_level_drift_at_most`). Written to `<world>.beat.json`; every number the look's, the script summing, transforming and comparing and inventing none."""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path
from typing import Any

import numpy as np

FIRST_STEPS = 6


def array_of(value: Any, shape: tuple[int, int, int]) -> np.ndarray:
    """A look's array (a nested list, or a sparse {at, values} over the flat x-major index) as the board's array in doubles."""
    if isinstance(value, dict):
        flat = np.zeros(int(np.prod(shape)), dtype=np.float64)
        flat[np.asarray(value["at"], dtype=np.int64)] = np.asarray(value["values"], dtype=np.float64)
        return flat.reshape(shape)
    return np.asarray(value, dtype=np.float64).reshape(shape)


def spectrum(trace: np.ndarray, every: int = 1) -> dict[str, Any]:
    """The discrete transform of a trace about its mean: the bins' angles per interval (2 pi k / (N every), every the look's stride in intervals), the amplitudes (2 |X_k| / N), the peak bin and the three largest."""
    n = len(trace)
    about = trace - trace.mean()
    amplitudes = 2 * np.abs(np.fft.rfft(about)) / n
    angles = 2 * math.pi * np.arange(len(amplitudes)) / (n * every)
    amplitudes[0] = 0.0
    order = np.argsort(amplitudes)[::-1][:3]
    return {
        "bin_per_interval": 2 * math.pi / (n * every),
        "peak_per_interval": float(angles[order[0]]),
        "peak_amplitude": float(amplitudes[order[0]]),
        "largest_three": [
            {"per_interval": float(angles[k]), "amplitude": float(amplitudes[k])} for k in order
        ],
    }


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("look", type=Path, help="the look file")
    parser.add_argument(
        "--expectation", type=Path, default=Path(__file__).resolve().parent / "expectation.json"
    )
    parser.add_argument("--record", default="electron", help="the record's family")
    parser.add_argument("--source", default="proton", help="the source's family")
    parser.add_argument("--holder", default="charge", help="the holder of the sign's family")
    parser.add_argument("--out", type=Path, default=None, help="the reading's file (<world>.beat.json)")
    args = parser.parse_args(argv)
    look = json.loads(args.look.read_text(encoding="utf-8"))
    stem = str(look["world"]).rsplit(".", 1)[0]
    shape = tuple(int(v) for v in look["shape"])
    centre = tuple(int(v) for v in look["bodies"][0]["nodes"][0])  # the proton's Node
    expectation = (
        json.loads(args.expectation.read_text(encoding="utf-8")) if args.expectation.exists() else {}
    )
    blind = (expectation.get("worlds") or {}).get(stem, {})
    frames = look["frames"]
    every = int(look.get("every") or 1)
    at_r = [int(v) for v in blind.get("holder_row_read_at", [3, 5])]
    row_nodes = [(centre[0] + d, centre[1], centre[2]) for d in at_r]
    neighbour = (centre[0] + 1, centre[1], centre[2])
    rows: list[dict[str, Any]] = []
    lay_abs = None
    for frame in frames:
        electron = frame["families"][args.record]
        z = array_of(electron["now"], shape) + 1j * array_of(electron["second"], shape)
        size = np.abs(z)
        if lay_abs is None:
            lay_abs = size.copy()
        overlap = float((size * lay_abs).sum() / (np.linalg.norm(size) * np.linalg.norm(lay_abs)))
        holder = array_of(frame["families"][args.holder]["now"], shape)
        proton = frame["families"].get(args.source)
        proton_size = None
        if proton is not None:
            pz = array_of(proton["now"], shape) + 1j * array_of(proton["second"], shape)
            proton_size = float(np.abs(pz)[centre])
        rows.append(
            {
                "interval": int(frame["interval"]),
                "Q": float((size**2).sum()),
                "centre_level": float(size[centre]),
                "neighbour_level": float(size[neighbour]),
                "overlap_with_the_lay": overlap,
                "holder_row": [float(holder[node]) for node in row_nodes],
                "proton_level": proton_size,
            }
        )
    n = len(rows)
    centre_trace = np.asarray([r["centre_level"] for r in rows])
    first = [
        {"interval": r["interval"], "centre": r["centre_level"], "r_1": r["neighbour_level"]}
        for r in rows[: FIRST_STEPS + 1]
    ]
    reading: dict[str, Any] = {
        "label": "LATTICE",
        "world": look["world"],
        "intervals": n - 1,
        "lay": {"centre_level": float(centre_trace[0]), "Q": rows[0]["Q"]},
        "overlap_with_the_lay": {
            "at_the_start": rows[0]["overlap_with_the_lay"],
            "at_the_close": rows[-1]["overlap_with_the_lay"],
            "least": min(r["overlap_with_the_lay"] for r in rows),
        },
        "first_steps": first,
        "first_steps_largest_change": {
            "centre": float(max(abs(r["centre"] - first[0]["centre"]) for r in first)),
            "r_1": float(max(abs(r["r_1"] - first[0]["r_1"]) for r in first)),
        },
        "centre_level": {
            "least": float(centre_trace.min()),
            "largest": float(centre_trace.max()),
            "drift_over_the_lay": float((centre_trace.max() - centre_trace.min()) / centre_trace[0]),
        },
        "Q_over_the_lay_at_the_close": rows[-1]["Q"] / rows[0]["Q"],
        "centre_spectrum": spectrum(centre_trace, every),
        "holder_row_at": at_r,
        "holder_row_spectra": [
            spectrum(np.asarray([r["holder_row"][k] for r in rows]), every) for k in range(len(at_r))
        ],
        "holder_row_range": [
            [float(min(r["holder_row"][k] for r in rows)), float(max(r["holder_row"][k] for r in rows))]
            for k in range(len(at_r))
        ],
        "proton_level": None
        if rows[0]["proton_level"] is None
        else {
            "least": min(r["proton_level"] for r in rows),
            "largest": max(r["proton_level"] for r in rows),
        },
        "rows": rows,
    }
    checks: dict[str, Any] = {}
    line = blind.get("line_per_interval")
    if line is not None:
        bins = float(blind.get("line_tolerance_bins", 1))
        peak = reading["centre_spectrum"]["peak_per_interval"]
        step = reading["centre_spectrum"]["bin_per_interval"]
        checks["centre_spectrum_peak_at_the_line"] = {
            "read": peak,
            "blind": line,
            "bins_off": abs(peak - line) / step,
            "within_bins": bins,
            "pass": abs(peak - line) <= bins * step,
        }
    if "overlap_with_the_lay_at_the_close_at_least" in blind:
        least = float(blind["overlap_with_the_lay_at_the_close_at_least"])
        checks["overlap_at_the_close"] = {
            "read": reading["overlap_with_the_lay"]["at_the_close"],
            "at_least": least,
            "pass": reading["overlap_with_the_lay"]["at_the_close"] >= least,
        }
    if "first_steps_unchanged_within_levels" in blind:
        within = float(blind["first_steps_unchanged_within_levels"])
        worst = max(reading["first_steps_largest_change"].values())
        checks["first_steps_within_levels"] = {"read": worst, "within": within, "pass": worst <= within}
    if "centre_level_drift_at_most" in blind:
        most = float(blind["centre_level_drift_at_most"])
        checks["centre_drift"] = {
            "read": reading["centre_level"]["drift_over_the_lay"],
            "at_most": most,
            "pass": reading["centre_level"]["drift_over_the_lay"] <= most,
        }
    reading["checks"] = checks
    reading["verdict"] = (
        "yes"
        if checks and all(c["pass"] for c in checks.values())
        else ("no" if checks else "no check named")
    )
    out = args.out or args.look.with_name(args.look.name.replace(".look.json", ".beat.json"))
    out.write_text(json.dumps(reading, indent=1) + "\n", encoding="utf-8")
    summary = {k: v for k, v in reading.items() if k != "rows"}
    print(
        json.dumps(
            {
                "reading": str(out),
                **{
                    k: summary[k]
                    for k in (
                        "overlap_with_the_lay",
                        "first_steps_largest_change",
                        "centre_level",
                        "Q_over_the_lay_at_the_close",
                        "centre_spectrum",
                        "checks",
                        "verdict",
                    )
                },
            }
        )
    )


if __name__ == "__main__":
    main()
