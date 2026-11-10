"""Shared helpers of the EM demos (builder B1-EM). Builds systems ONLY through the package API (layers/, prepare/,
observe/, core.Engine); predictions are floats computed from the package's own parameters (analysis only)."""
from __future__ import annotations

import json
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import numpy as np

from research.metric_variant_v1.core import Engine, State, compose
from research.metric_variant_v1.core.engine import OBJ
from research.metric_variant_v1.layers.em import A_NAMES, PHI, build_current_driver, build_em
from research.metric_variant_v1.layers.matter import algebra, build_matter, build_static_lapse_mechanism
from research.metric_variant_v1.observe import em as oem
from research.metric_variant_v1.prepare import vacuum_state
from research.metric_variant_v1.prepare import em as pem

OUT = Path(__file__).resolve().parent / "results"
Q0 = 2 ** 29 + 1
HOP0 = (Q0 - 1) // 4
MASS0 = 3 * Q0


def stamp() -> str:
    return subprocess.run(["date", "-u"], capture_output=True, text=True).stdout.strip()


def save(name: str, data: dict) -> None:
    OUT.mkdir(exist_ok=True)
    data = dict(data, demo=name, written=stamp())
    (OUT / f"{name}.json").write_text(json.dumps(data, indent=1, default=float))


def em_system(Q=Q0, hop=HOP0, mass=MASS0, wilson=0, g_phi=4, g_A=1, sigma=2 ** 14, extra=(), **kw):
    m = build_matter(Q=Q, hop=hop, mass=mass, wilson=wilson)
    e = build_em(Q=Q, matter=m, g_phi=g_phi, g_A=g_A, sigma=sigma, **kw)
    blocks = [m, e] + [f(m, e) for f in extra]
    T = compose(*blocks)
    return blocks, T, Engine(T, Q)


def kgrid(L):
    return pem.kgrid(L)


def band_stats(params, L, width, kc=(0.0, 0.0, 0.0), axis=0):
    """<E''_axis> and <cos E> over the packet's |amplitude|^2 k-weight exp(-width^2 (k - kc)^2) (float analysis),
    sin E = sqrt(mass^2 + 4 hop^2 sum sin^2 k) / D (wilson 0)."""
    D = 6 * params["Q"]
    K = kgrid(L)
    kk = ((K - np.asarray(kc) + np.pi) % (2 * np.pi)) - np.pi
    Z2 = np.exp(-width ** 2 * (kk ** 2).sum(-1))
    kabs = kk + np.asarray(kc)
    m, h = float(params["mass"]), float(params["hop"])

    def Ek(k):
        return np.arcsin(np.sqrt(m ** 2 + 4 * h ** 2 * (np.sin(k[..., 0]) ** 2 + np.sin(k[..., 1]) ** 2 +
                                                       np.sin(k[..., 2]) ** 2)) / D)
    hh = 1e-3
    e = np.zeros(3)
    e[axis] = hh
    Epp = (Ek(kabs + e) - 2 * Ek(kabs) + Ek(kabs - e)) / hh ** 2
    Ev = (Ek(kabs + e) - Ek(kabs - e)) / (2 * hh)
    w = Z2 / Z2.sum()
    return float((w * Epp).sum()), float((w * np.cos(Ek(kabs))).sum()), float((w * Ev).sum())


def phi_of(rho, em_params):
    """Float torus potential of rho in the E1 normalisation: -2 g (Q-1) Lap Phi = sigma rho."""
    return pem.torus_poisson_float(np.asarray(rho, float) * em_params["sigma"], 2.0 * em_params["g"] * (em_params["Q"] - 1))


def gx(f, axis=0):
    return (np.roll(f, -1, axis) - np.roll(f, 1, axis)) / 2


def accel(series, t0=0):
    s = np.asarray(series, float)
    tt = np.arange(len(s)) + t0
    return float(2 * np.polyfit(tt, s, 2)[0])


def rewind_ok(eng, final, steps, s0) -> bool:
    return eng.rewind(final, steps).same_as(s0)


def spin_projectors(params):
    us = pem.spin_spinors(params, +1)
    return [2 * np.real(np.outer(u, u.conj())) for u in us]
