"""READOUT LABELS (passive; OWNER decision 2, manager 11:2x). Read-only: classifies which gears' clicks are OFFICIAL
and which are AUDIT-ONLY. A label never changes a state; it is not a law.

Under the HANDED class (body_signs != (1, 1, 1)), L0 clicks are AUDIT-ONLY, the same label used for metric/potential
diagnostics. The default uses (1, -1, 1); +++ is an alternative with official L0 labels. The handed linear operator's
gap and Kramers structure motivate a proposed dark-sector interpretation; they do not establish physical mass,
neutrality or dark matter. Labels control observation only, not any interaction or physical detection efficiency.
"""
from __future__ import annotations

import math

import numpy as np

from ..core.tensor import Tensor

DARK_WHY = ("handed L0: proposed dark-sector interpretation of gap/Kramers algebra; clicks are AUDIT-ONLY "
            "by a passive observation convention, not a derived physical invisibility law")


def readout_class(tensor: Tensor, gear_name: str) -> str:
    """'official' or 'audit' for one qualified gear name: the TENSOR's own GearType label (ARCH F-R, RC2: the earlier
    namespace rule marked 220 gauge-link / EM-potential gears 'official' against their 'audit' tensor labels). Under the
    handed class the default builds L0 with label 'audit'; see dark_l0_violations."""
    return tensor.gears[tensor.gear_index(gear_name)].label


def readout_labels(system, tensor: Tensor) -> dict:
    """Per gear name: its readout class (= the tensor label)."""
    return {n: tensor.gears[i].label for i, n in enumerate(tensor.names)}


def dark_l0_violations(system, tensor: Tensor) -> list:
    """L0 gears that are NOT labelled 'audit' although the system is in the handed class (should be empty)."""
    if tuple(system.info.get("body_signs", (1, 1, 1))) == (1, 1, 1):
        return []
    return [n for i, n in enumerate(tensor.names) if n.startswith("ref.") and tensor.gears[i].label != "audit"]


def label_mismatches(system, tensor: Tensor) -> list:
    """Kept for callers: the declared dark-L0 rule vs the tensor labels (= dark_l0_violations)."""
    return dark_l0_violations(system, tensor)


def official_clicks(engine, before, after, step: int = 1):
    """The official click stream (Engine.clicks, stream 'official'): L0 is excluded under the handed class through the
    tensor label; nothing is computed differently."""
    return engine.clicks(before, after, step, stream="official").select("official")


# ------------------------------------------------------------------ R2: candidate clock ticks in the clock's OWN frame
OWN_FRAME_RULE = ("candidate clock tick = one sign cycle of the click sizes in the clock's OWN ROTATING FRAME: the fixed "
                  "carrier J (identified from the law, never from a species label) is removed by J^-t applied to the "
                  "consecutive click pair (l(t), l(t+1)); the raw sign-cycle reading is kept as contrast (manager R2)")


def carrier_from_law(tensor: Tensor, clock_gears, field: str, D: int) -> dict:
    """Identify a clock's fixed carrier from the TENSOR: fit the free k = 0 operator H0 (degree-1 b monomials among the
    clock gears, summed over offsets) as c 1 + kappa L where L is the k = 0 lapse-touched operator per unit field
    (degree-2 monomials with one ``field`` factor and one clock-gear b factor). The carrier is the part the lapse does
    not touch: theta = arccos(c/D), rounded to {0, pi/2, pi}. Returns c, kappa, theta, the rounded carrier and the
    relative fit residual."""
    idx = {tensor.gear_index(g): n for n, g in enumerate(clock_gears)}
    fi = tensor.gear_index(field)
    n = len(idx)
    H0 = np.zeros((n, n))
    Lop = np.zeros((n, n))
    for m in tensor.monomials:
        if m.target not in idx:
            continue
        fs = list(m.factors)
        if len(fs) == 1 and fs[0].field == "b" and fs[0].gear in idx:
            H0[idx[m.target], idx[fs[0].gear]] += m.coeff
        elif len(fs) == 2 and all(f.field == "b" for f in fs):
            g = [f.gear for f in fs]
            if g[0] == fi and g[1] in idx:
                Lop[idx[m.target], idx[g[1]]] += m.coeff
            elif g[1] == fi and g[0] in idx:
                Lop[idx[m.target], idx[g[0]]] += m.coeff
    A = np.stack([np.eye(n).ravel(), Lop.ravel()], axis=1)
    sol, *_ = np.linalg.lstsq(A, H0.ravel(), rcond=None)
    c, kappa = float(sol[0]), float(sol[1])
    res = float(np.linalg.norm(H0.ravel() - A @ sol) / max(np.linalg.norm(H0.ravel()), 1e-300))
    theta = math.acos(max(-1.0, min(1.0, c / D)))
    carrier = min((0.0, math.pi / 2, math.pi), key=lambda t: abs(t - theta))
    return {"c": c, "kappa": kappa, "theta": theta, "carrier": carrier, "residual": res}


def own_frame_series(clicks, carrier: float) -> list:
    """s(t) = [J^-t (l(t), l(t+1))]_0 with J = rotation by the carrier angle (0: identity; pi/2: (x, y) -> (y, -x),
    Rule3's zero-input map; pi: -1)."""
    if carrier not in (0.0, math.pi / 2, math.pi):
        raise ValueError("carrier must be 0, pi/2 or pi; no silent rounding in the decoder")
    out = []
    for t in range(len(clicks) - 1):
        x, y = clicks[t], clicks[t + 1]
        if carrier == 0.0:
            out.append(x)
        elif carrier == math.pi:
            out.append(x if t % 2 == 0 else -x)
        else:
            k = t % 4                                     # J^-t on (x, y): rotation by -t pi/2
            out.append((x, -y, -x, y)[k])
    return out


def tick_rate(series) -> float:
    """Angular tick rate from the sign cycles of a series (interpolated crossings; observe.gravity helpers)."""
    from .gravity import crossing_times, rate_from_crossings
    ts = [t for t, v in enumerate(series) if v != 0]
    qs = [v for v in series if v != 0]
    return rate_from_crossings(crossing_times(ts, qs))


__all__ = ["DARK_WHY", "readout_class", "readout_labels", "dark_l0_violations", "label_mismatches", "official_clicks",
           "OWN_FRAME_RULE",
           "carrier_from_law", "own_frame_series", "tick_rate"]
