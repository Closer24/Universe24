"""The readings of rows (1) and (2) of ALGEBRA.md #the-rows-against-nature from the one command's outputs
(`tools/run_inputs.py`), every number labelled by kind; no pin, no verdict (ALGEBRA.md #the-rows-against-nature).

DETECTOR: for each world the intervals from a record's giving click to its click at the
clock's own set `at_well` (the light clock's tick, ALGEBRA.md #the-velocity), their count, mean, rms and
standard error of the mean; the clicks at the faces. COMPUTATION: the ratio of the means
between the two worlds of a row with its error, and the closed forms it is set beside: for
the redshift the continuum's 1 / sqrt(1 - c_1 / Gamma) (ALGEBRA.md #the-rows-against-nature) and the lattice's own at
the given train's wave number k = pi / 2 (the frequency conserved across the well's edge,
the wave number refracted: cos k' = (6 Gamma cos omega_0 - 6 c_1 - 4 (Gamma - c_1)) / (2
(Gamma - c_1)) with cos omega_0 = 2 / 3, the group velocity (Gamma - c_1) sin k' / (3 Gamma
sin omega_0) against sin k / (3 sin omega_0)); for Lorentz the longitudinal form's gamma^2
and nature's gamma at v over the board's own light speed c_l (ALGEBRA.md #the-velocity), c_l read from the
rest world's tick against the arm.

    PYTHONPATH=src python examples/events/toward_nature/read_runs.py <out dir>
"""

from __future__ import annotations

import json
import math
import sys
from pathlib import Path

GAMMA = 10_000
WELL_LEVEL = 2000
ARM_LINKS = 558  # the redshift's arm
LORENTZ_ARM = 58
HOP_EVERY = 4


def waits(path: Path, detector: str = "at_well") -> tuple[list[int], dict]:
    out = json.loads(path.read_text(encoding="utf-8"))
    found = sorted(
        line["interval"] - line["giving"]
        for line in out.get("clicks", [])
        if line.get("detector") == detector and "giving" in line
    )
    return found, out.get("counts", {})


def stats(values: list[int]) -> tuple[float, float, float]:
    n = len(values)
    mean = sum(values) / n
    rms = math.sqrt(sum((v - mean) ** 2 for v in values) / n)
    return mean, rms, rms / math.sqrt(n)


def report(name: str, values: list[int], counts: dict) -> tuple[float, float]:
    mean, rms, error = stats(values)
    print(f"DETECTOR {name}: {len(values)} clicks at at_well, counts {counts}")
    print(
        f"  wait since the giving: mean {mean:.1f}, rms {rms:.1f}, standard error {error:.1f}, least {min(values)}, most {max(values)}"
    )
    return mean, error


def ratio(a: tuple[float, float], b: tuple[float, float]) -> tuple[float, float]:
    value = a[0] / b[0]
    error = value * math.sqrt((a[1] / a[0]) ** 2 + (b[1] / b[0]) ** 2)
    return value, error


def redshift(out: Path, suffix: str = "") -> None:
    wave = "at the long wavelength 21 (k = 0.299)" if suffix else "at k = pi / 2"
    print(f"== ROW (1) THE REDSHIFT {wave}, Gamma 10^4, c_1 = 2000, the law as built")
    top, top_counts = waits(out / f"redshift_top{suffix}.output.json")
    bottom, bottom_counts = waits(out / f"redshift_bottom{suffix}.output.json")
    t = report("redshift_top (the arm at 0)", top, top_counts)
    b = report("redshift_bottom (the arm held at 2000)", bottom, bottom_counts)
    # the early clicks of the bottom world: records turned back at the well's edge before the
    # mirror (below the top world's least wait); stated, then the mirror's cluster alone
    early = [w for w in bottom if w < min(top)]
    late = [w for w in bottom if w >= min(top)]
    print(
        f"  DETECTOR bottom: {len(early)} clicks earlier than the top world's least wait {early} (the well's edge), {len(late)} the mirror's"
    )
    late_stats = report("redshift_bottom, the mirror's cluster", late, {})
    r_all = ratio(b, t)
    r_late = ratio(late_stats, t)
    print(
        f"COMPUTATION ratio bottom / top of the means: all clicks {r_all[0]:.3f} +- {r_all[1]:.3f}; the mirror's cluster {r_late[0]:.3f} +- {r_late[1]:.3f}"
    )
    u = WELL_LEVEL / (2 * GAMMA)
    continuum = 1 / math.sqrt(1 - 2 * u)
    cos_w0 = 2 / 3
    sin_w0 = math.sqrt(1 - cos_w0**2)
    p = GAMMA - WELL_LEVEL
    cos_k1 = (6 * GAMMA * cos_w0 - 6 * WELL_LEVEL - 4 * p) / (2 * p)
    sin_k1 = math.sqrt(1 - cos_k1**2)
    v0 = 1 / (3 * sin_w0)
    v1 = p * sin_k1 / (3 * GAMMA * sin_w0)
    print(
        f"COMPUTATION set beside: the continuum's 1 / sqrt(1 - 2 U_1) = {continuum:.3f} at U_1 = {u} (today's law, ALGEBRA.md #the-rows-against-nature); nature 1 + U_1 = {1 + u:.3f} at first order"
    )
    print(
        f"COMPUTATION on the Einstein form (ALGEBRA.md #the-rows-against-nature): a light clock with a declared arm reads the coordinate speed of light, 1 / (1 - 2 U_1) = {1 / (1 - 2 * u):.3f}; a clock body reads the redshift 1 / sqrt(1 - 2 U_1 + 2 U_1^2) = {1 / math.sqrt(1 - 2 * u + 2 * u * u):.3f}"
    )
    print(
        f"COMPUTATION the lattice's own at k = pi / 2: v_g at 0 = {v0:.4f}, in the well cos k' = {cos_k1:.3f}, v_g' = {v1:.4f}, the flight ratio {v0 / v1:.3f}"
    )
    print(
        "  the ratio of the means reads the whole tick (the arm both ways, the train's own Nodes at the emitter's level, the mirror's delay); the arm's share of the tick is the flight's"
    )


def lorentz(out: Path, suffix: str = "") -> None:
    long_wave = suffix == "_long"
    print(
        "== ROW (2) LORENTZ, the longitudinal clock"
        + (" at the long wave k = 0.299 with Doppler (item 49)" if long_wave else "")
        + (" under body_record" if suffix == "_seat" else "")
    )
    rest, rest_counts = waits(out / f"lorentz_rest{suffix}.output.json")
    moving, moving_counts = waits(out / f"lorentz_moving{suffix}.output.json")
    r = report("lorentz_rest", rest, rest_counts)
    m = report("lorentz_moving (one Link every 4 intervals along the arm)", moving, moving_counts)
    q = ratio(m, r)
    print(f"COMPUTATION ratio moving / rest of the means: {q[0]:.3f} +- {q[1]:.3f}")
    v = 1 / HOP_EVERY
    # c_l from the rest tick: the light clock's tick 2 D / c_l + the delay; the delay read from
    # the redshift's top world (D = 558) against the rest world (D = 58) where both exist
    k = 2 * math.pi / 21 if long_wave else math.pi / 2
    cos_omega = (math.cos(k) + 2) / 3
    c_l = math.sin(k) / (3 * math.sqrt(1 - cos_omega * cos_omega))
    gamma = 1 / math.sqrt(1 - (v / c_l) ** 2)
    print(
        f"COMPUTATION set beside: c_l = {c_l:.3f} at k = {k:.3f} (the plain rule's group velocity), v / c_l = {v / c_l:.3f}, nature's gamma = {gamma:.3f}, the longitudinal form's gamma^2 = {gamma**2:.3f} on the flight (ALGEBRA.md #the-velocity)"
    )


if __name__ == "__main__":
    folder = Path(sys.argv[1])
    if (folder / "redshift_top.output.json").exists():
        redshift(folder)
    if (folder / "redshift_top_long.output.json").exists():
        redshift(folder, "_long")
    if (folder / "lorentz_rest.output.json").exists():
        lorentz(folder)
    if (folder / "lorentz_rest_seat.output.json").exists():
        lorentz(folder, "_seat")
    if (folder / "lorentz_rest_long.output.json").exists():
        lorentz(folder, "_long")
