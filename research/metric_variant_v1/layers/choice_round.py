"""ROUND-CONE F7 (post-freeze file; the frozen layers/choice.py is reused unchanged).

The frozen ``build_f7(carrier="light")`` drives the headroom light u = (Q-1) Sum_6 b + 6b with u_P += gamma b_F. In the
plane-wave geometry that source leaves a persistent zero-frequency plateau after the abrupt switch-on (TC.17-long).
``build_f7_round`` adds ONE designated term per front component, u_P += -gamma a_F, so the source is the time
difference gamma (b_F - a_F): no DC content, the same |response| at 60 degrees, phase +60 degrees. Bob is one-shot
(bob_gate=True). The extra terms are a separate Block (no gears) composed after the frozen block.
"""
from __future__ import annotations

import math

from ..core.tensor import Block
from .choice import build_f7

EMIT_DIFF = ("choice-front emission (F7, round cone): the time-difference half of the one-way source gamma (b_F - a_F) "
             "into the headroom light (no DC content); the far side reads the front without back-action")


def round_gamma(Q: int, rho0: float = 0.9) -> int:
    """gamma for a CW plane-wave amplitude rho0 x (Alice's clock amplitude) at 60 degrees: |G| = gamma A / (2 (Q-1) sin k),
    cos k = 1 - 3Q / (2 (Q-1)) (the time-difference factor |1 - e^{-i 60 deg}| = 1)."""
    cosk = 1 - 3 * Q / (2 * (Q - 1))
    return round(rho0 * 2 * (Q - 1) * math.sqrt(1 - cosk * cosk))


def build_f7_round(*, Q: int, kappa: int, gamma: int, name: str = "f7"):
    """Returns (base, extra): the frozen F7 block (light carrier, one-shot Bob) and the extra source block."""
    base = build_f7(Q=Q, kappa=kappa, name=name, bob_gate=True, carrier="light", gamma=gamma)
    terms = tuple((f"{name}.P{j}", -gamma, ((f"{name}.F{j}", (0, 0, 0), "a"),), {"designated_one_way": EMIT_DIFF})
                  for j in range(3))
    extra = Block((), terms, name=None, Q=Q, params={"Q": Q, "gamma": gamma}, doc="time-difference source half")
    return base, extra


__all__ = ["round_gamma", "build_f7_round", "EMIT_DIFF"]
