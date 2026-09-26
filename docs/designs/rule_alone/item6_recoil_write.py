"""ITEM 6 of record 2134: the recoil as a rotation of the body's pair at a click, a phase gradient
near 1e-8 per Link (9.98 (2), 9.84 (2), 9.96 (3)): does it survive in integers, or is it lost?
THE ARITHMETIC OF THE WRITE first (HOST, no run): the bound record (the well of side 5 at
[800, 850], amplitude 2^17 and the bound 2^20) has its pair (now, before) rotated at each Node by
the angle k dx, dx the Node's distance from the centre along x; the rotated levels are rounded to
integers; the count of Nodes whose integers change is read, at k = 1e-8 (the record's quoted
gradient), at the recoil of one quantum of 9.96 (3) (Delta v = 1 / (1000 s lambda_q) at s = 2000
and lambda_q = 21, K = 3 (den / num) Delta v), and at the k where the first Node changes. A write
that changes no integer is lost at the write; the rule's remainders cannot recover a phase that
was never written.

    PYTHONPATH=src python docs/designs/rule_alone/item6_recoil_write.py
"""

from __future__ import annotations

import json
import math
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import bodies as B  # noqa: E402

SHAPE = (240, 32, 32)
WRAP = (True, True, True)
AMOUNT = 2000
LAMBDA_Q = 21


def rotated(
    now: np.ndarray, before: np.ndarray, k: float, centre: int, cos_b: float, scale: float
) -> tuple[np.ndarray, np.ndarray]:
    """The pair as a rotating phasor A cos(phi), A cos(phi - omega): turn phi by k dx at every Node
    and round; `scale` multiplies the amplitude first (the bound 2^20 against the record's 2^17)."""
    sin_b = math.sqrt(1.0 - cos_b * cos_b)
    n = now.astype(np.float64) * scale
    b = before.astype(np.float64) * scale
    # the phasor: cos phi = n / A, sin phi = (b - n cos) / (A sin) with A^2 = (n^2 + b^2 - 2 n b cos) / sin^2
    amplitude = np.sqrt(np.maximum(n * n + b * b - 2.0 * n * b * cos_b, 0.0)) / sin_b
    with np.errstate(invalid="ignore", divide="ignore"):
        cos_phi = np.where(amplitude > 0, n / np.maximum(amplitude, 1e-300), 1.0)
        sin_phi = np.where(amplitude > 0, (b - n * cos_b) / np.maximum(amplitude * sin_b, 1e-300), 0.0)
    dx = (np.arange(SHAPE[0]) - centre).reshape(-1, 1, 1).astype(np.float64)
    theta = k * dx
    cos_t, sin_t = np.cos(theta), np.sin(theta)
    cos_new = cos_phi * cos_t - sin_phi * sin_t
    sin_new = sin_phi * cos_t + cos_phi * sin_t
    new_now = np.rint(amplitude * cos_new)
    new_before = np.rint(amplitude * (cos_new * cos_b + sin_new * sin_b))
    return new_now.astype(np.int64), new_before.astype(np.int64)


def main() -> None:
    body = B.Body([120, 16, 16], AMOUNT)
    profile, clock = B.bound_mode(SHAPE, WRAP, body)
    cos_b = clock[0] / (2.0 * clock[1])
    now, before = profile.copy(), profile.copy()  # the standing start, both levels the profile
    num, den = B.KIND
    delta_v = 1.0 / (1000 * AMOUNT * LAMBDA_Q)
    k_recoil = 3.0 * (den / num) * delta_v
    out = {
        "clock": clock,
        "amplitude": int(np.abs(profile).max()),
        "delta_v_one_quantum": delta_v,
        "K_one_quantum": k_recoil,
        "rows": [],
    }
    for scale, label in ((1.0, "2^17"), (8.0, "2^20 (the bound)")):
        base_now, base_before = rotated(now, before, 0.0, body.centre[0], cos_b, scale)
        for k in (1e-8, k_recoil, 1e-7, 1e-6, 1e-5, 1e-4):
            r_now, r_before = rotated(now, before, k, body.centre[0], cos_b, scale)
            changed = int(((r_now != base_now) | (r_before != base_before)).sum())
            on_well = body.mask(SHAPE)
            changed_well = int((((r_now != base_now) | (r_before != base_before)) & on_well).sum())
            out["rows"].append(
                {
                    "amplitude": label,
                    "k": k,
                    "nodes_changed": changed,
                    "well_nodes_changed": changed_well,
                }
            )
            print(
                f"amplitude {label}: k = {k:.2e} per Link: {changed} Nodes change of {SHAPE[0] * SHAPE[1] * SHAPE[2]}, {changed_well} of the well's 125"
            )
    print(
        f"the recoil of one quantum (9.96 (3)): Delta v = {delta_v:.2e} Links per interval, K = {k_recoil:.2e} per Link (COMPUTATION)"
    )
    (Path(__file__).resolve().parent / "item6_recoil_write.json").write_text(
        json.dumps(out, indent=1) + "\n", encoding="utf-8"
    )


if __name__ == "__main__":
    main()
