"""Read-only diagnostics; continuum equations never supply a simulation update."""

import itertools
import math

import numpy as np
from configuration import AMPLITUDE_SCALE, DIRECTIONS, NAMES


def cross(a, b):
    return (a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0])


def moments(frame):
    """Full integer-tick frames have completed every one-tick field transfer."""
    if frame.get("spatial_transfers"):
        raise ValueError("moment sampling requires a completed-link frame")
    result = {}
    norm = 0
    for node in frame["spatial_fields"]:
        electric, magnetic = [0, 0, 0], [0, 0, 0]
        for direction, name in zip(DIRECTIONS, NAMES, strict=True):
            value = node["fields"][name]["value"]
            assert sum(a * b for a, b in zip(direction, value, strict=True)) == 0
            rotated = cross(direction, value)
            norm += sum(v * v for v in value)
            for j in range(3):
                electric[j] += value[j]
                magnetic[j] += rotated[j]
        result[tuple(node["position"])] = (tuple(electric), tuple(magnetic))
    return result, norm


def centered_divergence(values, shape, component):
    """Unscaled centered difference; zero is tested exactly with integer arithmetic."""
    maximum = 0
    # Divergence can be nonzero at an empty node adjacent to occupied stock.
    for point in itertools.product(*(range(extent) for extent in shape)):
        total = 0
        for axis in range(3):
            plus, minus = list(point), list(point)
            plus[axis] = (plus[axis] + 1) % shape[axis]
            minus[axis] = (minus[axis] - 1) % shape[axis]
            total += values.get(tuple(plus), ((0, 0, 0), (0, 0, 0)))[component][axis]
            total -= values.get(tuple(minus), ((0, 0, 0), (0, 0, 0)))[component][axis]
        maximum = max(maximum, abs(total))
    return maximum


def frequency(samples):
    """Fit a second-order temporal recurrence after removing a static offset.

    Even samples alias the reflection's fast branch onto its slow counterpart.
    This read-only estimator is defined before the engine run and cannot tune it.
    """
    even = np.asarray(samples, dtype=float)[::2]
    differences = np.diff(even)
    center = differences[1:-1]
    neighbors = differences[:-2] + differences[2:]
    denominator = 2 * float(center @ center)
    if denominator < 1e-24:
        return {"status": "static or insufficient signal"}
    q = float(center @ neighbors) / denominator
    if not -1 <= q <= 1:
        return {"status": "not an oscillatory recurrence", "coefficient": q}
    residual = float(np.linalg.norm(neighbors - 2 * q * center) / np.linalg.norm(neighbors))
    return {"status": "measured", "omega": math.acos(q) / 2, "recurrence_residual": residual}


def analyze(case, recording):
    raw = case["input"]
    shape = raw["shape"]
    k = [2 * math.pi * m / n for m, n in zip(case.get("mode", (0, 0, 0)), shape, strict=True)]
    polarization = case.get("polarization", (0, 1, 0))
    rows = []
    initial_norm = None
    initial_totals = None
    for frame in recording["frames"]:
        values, norm = moments(frame)
        if initial_norm is None:
            initial_norm = norm
        assert norm == initial_norm, (frame["tick"], norm, initial_norm)
        totals = [
            [sum(pair[owner][axis] for pair in values.values()) for axis in range(3)]
            for owner in range(2)
        ]
        if initial_totals is None:
            initial_totals = totals
        assert totals == initial_totals, (frame["tick"], totals, initial_totals)
        electric_squared = sum(v * v for e, _ in values.values() for v in e)
        magnetic_squared = sum(v * v for _, b in values.values() for v in b)
        assert electric_squared + magnetic_squared <= 4 * norm
        mode_e = np.zeros(3, dtype=complex)
        mode_b = np.zeros(3, dtype=complex)
        for position, (electric, magnetic) in values.items():
            phase = np.exp(-1j * sum(a * x for a, x in zip(k, position, strict=True)))
            mode_e += phase * np.asarray(electric) / AMPLITUDE_SCALE
            mode_b += phase * np.asarray(magnetic) / AMPLITUDE_SCALE
        k_norm = float(np.linalg.norm(k))
        mode_norm = float(np.linalg.norm(mode_e))
        longitudinal = abs(np.dot(k, mode_e)) / (k_norm * mode_norm) if k_norm * mode_norm > 1e-9 else 0
        rows.append(
            {
                "tick": frame["tick"],
                "population_norm": norm,
                "electric_magnetic_totals": totals,
                "electric_squared": electric_squared,
                "magnetic_squared": magnetic_squared,
                "macro_energy_fraction": (electric_squared + magnetic_squared) / (4 * norm)
                if norm
                else 0,
                "electric_mode": [[float(v.real), float(v.imag)] for v in mode_e],
                "magnetic_mode": [[float(v.real), float(v.imag)] for v in mode_b],
                "polarized_electric_mode": float(np.dot(mode_e, polarization).real),
                "continuum_longitudinal_fraction": float(longitudinal),
                "centered_div_e_max": centered_divergence(values, shape, 0),
                "centered_div_b_max": centered_divergence(values, shape, 1),
            }
        )
    estimate = (
        frequency([r["polarized_electric_mode"] for r in rows])
        if len(rows) >= 9
        else {"status": "short pulse"}
    )
    if estimate["status"] == "measured" and any(k):
        estimate["phase_speed"] = estimate["omega"] / float(np.linalg.norm(k))
        estimate["relative_error_from_half_link_speed"] = abs(estimate["phase_speed"] - 0.5) / 0.5
    return {"rows": rows, "frequency": estimate, "shape": shape, "kind": case["kind"]}
