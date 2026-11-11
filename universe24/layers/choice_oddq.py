"""ODD-Q helpers for the CHOICE layer (post-freeze file; the frozen layers/choice.py is unchanged).

At an odd system Q an exact (efficiency-1) two-exit Born router on the polarization identity is impossible (parity:
K+ - K- = 4 kappa (|X1|^2 + |X2|^2) = 0 mod 4 while D = 6Q = 2 mod 4; NOTES_choice.md TC.13). The router is then
NEAR-MATCHED: exclusive, Born-exact conditional on a click, with the predicted per-readout non-detection (D - S)/D.
"""
from __future__ import annotations

from fractions import Fraction

from .choice import build_born_router


def near_matched_kappa(Q: int, A: int = 1) -> int:
    """Largest kappa with S = 16 kappa A^2 <= D = 6Q (two 3-gear rings of amplitude A, opposite or mirror form)."""
    if type(Q) is not int or Q < 1 or type(A) is not int or A < 1:
        raise ValueError("Q and A must be positive ints")
    k = (6 * Q) // (16 * A * A)
    if k < 1:
        raise ValueError("D = 6Q is too small for amplitude A")
    return k


def predicted_non_detection(Q: int, A: int = 1) -> Fraction:
    """Uniform fresh shared-remainder ensemble: P(no click)=(D-S)/D per
    one-shot readout (>=2/D for odd Q). Not an unconditional probability for a
    deterministic seed or a continuously exposed detector."""
    D = 6 * Q
    return Fraction(D - 16 * near_matched_kappa(Q, A) * A * A, D)


def build_odd_q_router(*, Q: int, A: int, arm1, arm2, form: str = "opposite", name: str | None = "router"):
    """build_born_router with kappa = near_matched_kappa(Q, A); same API otherwise. Readers must be ONE-SHOT
    (exposed once from fresh equal remainders): a continuously exposed pair at odd Q loses its lock (TC.15)."""
    return build_born_router(Q=Q, kappa=near_matched_kappa(Q, A), arm1=arm1, arm2=arm2, form=form, name=name)


__all__ = ["near_matched_kappa", "predicted_non_detection", "build_odd_q_router"]
