"""The delay-growth distance-redshift law against the supernova Hubble diagram.

The closed-row sweep (`redshift_sweep.py`) measures 1 + z = exp(alpha D) for
light crossing D links while the computation load grows linearly with age:
the hop time k rises linearly, so D = (1 / alpha) ln(1 + z). What a distant
source looks like then follows from two further readings of the model, both
stated rather than derived: bodies arrive at a rate reduced by 1 + z, and the
field of a source dilutes as 1 / D^2 in three open dimensions (the isotropy
probe). If each body keeps its amount (reading A) the flux is
L / (4 pi D^2 (1 + z)) and the luminosity distance is D sqrt(1 + z); if a
body's amount is also read down by 1 + z, as a wave's frequency would be
(reading B), it is D (1 + z). The Hubble diagram then has one free scale,
alpha in links per unit distance, which is degenerate with the absolute
magnitude, so only the shape of m(z) is tested.

This script fits the shape of each reading, of flat LambdaCDM and of the
Einstein-de Sitter universe to the Pantheon+ supernova sample (Hubble-flow
objects) with one free offset each, with the diagonal errors and, given
--covariance, with the release's full statistical-plus-systematic covariance
restricted to the kept objects, and reports chi-square, the low-redshift
deceleration parameter of each luminosity-distance shape and the binned
residuals. Nothing here runs the lattice; the lattice's law is the
input, taken from the sweep's summary if given.

usage: python redshift_hubble.py --pantheon Pantheon+SH0ES.dat --output DIR [--sweep summary.json] [--covariance Pantheon+SH0ES_STAT+SYS.cov]
"""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path

OMEGA_M = 0.334  # flat LambdaCDM, the Pantheon+ best fit
BINS = ((0.01, 0.1), (0.1, 0.3), (0.3, 0.6), (0.6, 1.0), (1.0, 2.3))


def comoving_integral(z: float, omega_m: float, steps: int = 400) -> float:
    """int_0^z dz' / E(z') for flat LambdaCDM by Simpson's rule."""
    if z <= 0:
        return 0.0
    h = z / steps

    def e(x: float) -> float:
        return 1 / math.sqrt(omega_m * (1 + x) ** 3 + 1 - omega_m)

    total = e(0) + e(z)
    for i in range(1, steps):
        total += (4 if i % 2 else 2) * e(i * h)
    return total * h / 3


def lattice_distance(z: float, n: float) -> float:
    """D(z) in units of 1 / alpha for a hop time growing as the n-th power of age.

    1 + z = (t_o / t_e)^n and D = int dt / k, so D is proportional to
    (1 + z)^((n - 1) / n) - 1 for n > 1 and to ln(1 + z) for n = 1 (the linear
    load of constant emission); n = 2 is the load of an emission growing
    linearly with age. The hop time plays the part of the scale factor,
    a(t) ~ t^n, so the low-redshift deceleration parameter is -(n - 1) / n.
    """
    if abs(n - 1) < 1e-9:
        return math.log(1 + z)
    return ((1 + z) ** ((n - 1) / n) - 1) * n / (n - 1)


def shape(n: float, reading: str):
    """The luminosity-distance shape of the lattice law under reading A or B."""
    power = 0.5 if reading == "A" else 1.0
    return lambda z: lattice_distance(z, n) * (1 + z) ** power


SHAPES = {
    "linear load (n = 1), rate loss only (A)": shape(1, "A"),
    "linear load (n = 1), rate and amount loss (B)": shape(1, "B"),
    "quadratic load (n = 2), rate loss only (A)": shape(2, "A"),
    "quadratic load (n = 2), rate and amount loss (B)": shape(2, "B"),
    "flat LambdaCDM, Omega_m 0.334": lambda z: (1 + z) * comoving_integral(z, OMEGA_M),
    "Einstein-de Sitter": lambda z: 2 * (1 + z) * (1 - 1 / math.sqrt(1 + z)),
}
# The low-redshift deceleration parameter of each shape, from d(z) = z + (1 - q0) z^2 / 2 + ...
DECELERATION = {
    "linear load (n = 1), rate loss only (A)": 1.0,
    "linear load (n = 1), rate and amount loss (B)": 0.0,
    "quadratic load (n = 2), rate loss only (A)": 0.5,
    "quadratic load (n = 2), rate and amount loss (B)": -0.5,
    "flat LambdaCDM, Omega_m 0.334": OMEGA_M / 2 - (1 - OMEGA_M),
    "Einstein-de Sitter": 0.5,
}


def deceleration_numeric(shape, h: float = 1e-3) -> float:
    """q0 = 1 - d''(0) / d'(0) from finite differences of the shape."""
    d1 = (shape(2 * h) - shape(h)) / h  # one-sided, the shape is defined for z > 0 only
    d2 = (shape(3 * h) - 2 * shape(2 * h) + shape(h)) / (h * h)
    return 1 - d2 / d1


def read_pantheon(path: Path, with_index: bool = False):
    """(z, m_b_corr, error) for Hubble-flow supernovae: not calibrators, z above 0.01.

    With `with_index`, also the row numbers kept, for the covariance.
    """
    rows = []
    keep = []
    header = None
    index = 0
    for line in path.read_text(encoding="utf-8").splitlines():
        parts = line.split()
        if not parts:
            continue
        if header is None:
            header = {name: i for i, name in enumerate(parts)}
            continue
        z = float(parts[header["zHD"]])
        if not (int(parts[header["IS_CALIBRATOR"]]) == 1 or z < 0.01):
            rows.append((z, float(parts[header["m_b_corr"]]), float(parts[header["m_b_corr_err_DIAG"]])))
            keep.append(index)
        index += 1
    return (rows, keep) if with_index else rows


def read_covariance(path: Path, keep: list[int]) -> list[list[float]]:
    """The Pantheon+ statistical-plus-systematic covariance, restricted to the kept rows."""
    values = path.read_text(encoding="utf-8").split()
    size = int(values[0])
    flat = [float(v) for v in values[1:]]
    return [[flat[i * size + j] for j in keep] for i in keep]


def fit_with_covariance(shape, sample, covariance) -> dict:
    """One free offset, weighted by the inverse of the full covariance (numpy)."""
    import numpy as np

    z = np.array([s[0] for s in sample])
    m = np.array([s[1] for s in sample])
    model = np.array([5 * math.log10(shape(v)) for v in z])
    c = np.array(covariance)
    for i, s in enumerate(sample):
        c[i, i] = s[2] ** 2 if c[i, i] == 0 else c[i, i]
    inverse = np.linalg.inv(c)
    ones = np.ones(len(sample))
    residual = m - model
    offset = float(ones @ inverse @ residual / (ones @ inverse @ ones))
    r = model + offset - m
    return {"offset": round(offset, 4), "chi2": round(float(r @ inverse @ r), 2)}


def fit(shape, sample: list[tuple[float, float, float]]) -> dict:
    """One free offset (absolute magnitude and scale together), weighted least squares."""
    model = [5 * math.log10(shape(z)) for z, _, _ in sample]
    weights = [1 / (s * s) for _, _, s in sample]
    offset = sum(w * (m - mod) for w, (_, m, _), mod in zip(weights, sample, model, strict=True)) / sum(
        weights
    )
    residuals = [mod + offset - m for (_, m, _), mod in zip(sample, model, strict=True)]
    chi2 = sum(w * r * r for w, r in zip(weights, residuals, strict=True))
    binned = []
    for low, high in BINS:
        picked = [
            (r, w) for (z, _, _), r, w in zip(sample, residuals, weights, strict=True) if low <= z < high
        ]
        if picked:
            total = sum(w for _, w in picked)
            mean = sum(r * w for r, w in picked) / total
            binned.append(
                {
                    "z_low": low,
                    "z_high": high,
                    "count": len(picked),
                    "mean_residual_mag": round(mean, 4),
                    "error_of_mean_mag": round(1 / math.sqrt(total), 4),
                }
            )
    return {
        "offset": round(offset, 4),
        "chi2": round(chi2, 2),
        "count": len(sample),
        "chi2_per_dof": round(chi2 / (len(sample) - 1), 4),
        "binned_residuals_model_minus_data": binned,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--pantheon", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--sweep", type=Path, help="summary.json of redshift_sweep.py, for alpha")
    parser.add_argument(
        "--covariance", type=Path, help="Pantheon+SH0ES_STAT+SYS.cov, for the full-covariance fit"
    )
    args = parser.parse_args()
    args.output.mkdir(parents=True, exist_ok=True)
    sample, keep = read_pantheon(args.pantheon, with_index=True)
    results = {name: fit(shape, sample) for name, shape in SHAPES.items()}
    reference = results["flat LambdaCDM, Omega_m 0.334"]["chi2"]
    covariance = read_covariance(args.covariance, keep) if args.covariance else None
    full_reference = None
    for name, row in results.items():
        row["delta_chi2_against_LambdaCDM"] = round(row["chi2"] - reference, 2)
        row["deceleration_q0"] = DECELERATION[name]
        row["deceleration_q0_numeric"] = round(deceleration_numeric(SHAPES[name]), 3)
        if covariance is not None:
            full = fit_with_covariance(SHAPES[name], sample, covariance)
            row["full_covariance"] = full
    if covariance is not None:
        full_reference = results["flat LambdaCDM, Omega_m 0.334"]["full_covariance"]["chi2"]
        for row in results.values():
            row["full_covariance"]["delta_chi2_against_LambdaCDM"] = round(
                row["full_covariance"]["chi2"] - full_reference, 2
            )
    # The exponent of the load's growth as a free parameter, each reading: the best n.
    best = {}
    for reading in ("A", "B"):
        grid = [
            (round(1 + i * 0.05, 2), fit(shape(1 + i * 0.05, reading), sample)["chi2"])
            for i in range(0, 81)
        ]
        n, chi2 = min(grid, key=lambda row: row[1])
        full_best = (
            fit_with_covariance(shape(n, reading), sample, covariance)
            if covariance is not None
            else None
        )
        best[f"reading {reading}"] = {
            **(
                {
                    "full_covariance_chi2": full_best["chi2"],
                    "full_covariance_delta_chi2_against_LambdaCDM": round(
                        full_best["chi2"] - full_reference, 2
                    ),
                }
                if full_best
                else {}
            ),
            "best_n": n,
            "chi2": round(chi2, 2),
            "delta_chi2_against_LambdaCDM": round(chi2 - reference, 2),
            # The deceleration parameter of the luminosity-distance shape itself, which in
            # reading A differs from the scale factor's -(n - 1) / n.
            "deceleration_q0": round(deceleration_numeric(shape(n, reading)), 3),
            "scale_factor_q0": round(-(n - 1) / n, 3),
            "chi2_by_n": {str(k): round(v, 1) for k, v in grid[::10]},
        }
    alpha = None
    if args.sweep:
        runs = json.loads(args.sweep.read_text(encoding="utf-8"))["runs"]
        alpha = next((r["alpha"] for r in runs if r["label"] == "reference"), None)
    report = {
        "sample": "Pantheon+SH0ES.dat, IS_CALIBRATOR = 0, zHD >= 0.01, diagonal errors"
        + (", and the full statistical-plus-systematic covariance" if covariance is not None else ""),
        "count": len(sample),
        "alpha_reference_run": alpha,
        "note": "alpha is degenerate with the absolute magnitude; only the shape of m(z) is fitted",
        "fits": results,
        "free_exponent": best,
        "tests": {
            "time_dilation": "durations stretch by 1 + z with the spacing (sweep: duration ratio equals 1 + z); consistent with supernova light-curve dilation",
            "tolman_surface_brightness_exponent": {"reading A": 1, "reading B": 2, "expansion": 4},
            "cmb_temperature_scaling": "not applicable: the model has no blackbody spectrum",
        },
    }
    (args.output / "hubble.json").write_text(json.dumps(report, indent=2) + "\n")
    print(f"{len(sample)} Hubble-flow supernovae, diagonal errors")
    for name, row in results.items():
        print(
            f"{name}: chi2 {row['chi2']} ({row['chi2_per_dof']} per dof), delta against LambdaCDM"
            f" {row['delta_chi2_against_LambdaCDM']}, q0 {row['deceleration_q0']}"
            f" (numeric {row['deceleration_q0_numeric']})"
            + (
                f"; full covariance: chi2 {row['full_covariance']['chi2']}, delta"
                f" {row['full_covariance']['delta_chi2_against_LambdaCDM']}"
                if "full_covariance" in row
                else ""
            )
        )
        for b in row["binned_residuals_model_minus_data"]:
            print(
                f"   z {b['z_low']}-{b['z_high']}: {b['count']} SNe, model - data"
                f" {b['mean_residual_mag']:+.3f} +- {b['error_of_mean_mag']:.3f} mag"
            )
    for reading, row in best.items():
        print(
            f"free exponent, {reading}: best n {row['best_n']}, chi2 {row['chi2']}, delta against"
            f" LambdaCDM {row['delta_chi2_against_LambdaCDM']}, q0 of the shape"
            f" {row['deceleration_q0']} (scale factor {row['scale_factor_q0']})"
            + (
                f"; full covariance: chi2 {row['full_covariance_chi2']}, delta"
                f" {row['full_covariance_delta_chi2_against_LambdaCDM']}"
                if "full_covariance_chi2" in row
                else ""
            )
        )
    print("Wrote report: " + str(args.output / "hubble.json"))


if __name__ == "__main__":
    main()
