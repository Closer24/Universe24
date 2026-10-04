"""The pion-gap holder at the law's coupling (ALGEBRA.md L176; the paper's S.38 (b), R184): a screened Coulomb well -g e^(-r / R) / r binds an s state only for mu g R / (hbar c)^2 >= 0.840; at g = alpha hbar c, R = 1.414 fm and the reduced mass 469.5 MeV the number, the threshold and the coupling the threshold needs in units of alpha.

Usage: `python tools/derivations/nuclear.py` prints them.
"""

from __future__ import annotations

HBAR_C = 197.327  # MeV fm
ALPHA = 1 / 137.036
THRESHOLD = 0.840  # the screened Coulomb well's first bound state, in mu g R / (hbar c)^2
RANGE_FM, REDUCED_MASS_MEV = 1.414, 469.5


def yukawa_threshold() -> list[float]:
    """[mu g R / (hbar c)^2 at g = alpha hbar c, the threshold, the coupling needed over alpha, the well's depth at r = R in MeV]."""
    number = REDUCED_MASS_MEV * ALPHA * RANGE_FM / HBAR_C
    needed = THRESHOLD * HBAR_C / (REDUCED_MASS_MEV * RANGE_FM)
    depth = ALPHA * HBAR_C * 2.718281828459045**-1 / RANGE_FM
    return [number, THRESHOLD, needed / ALPHA, depth]


if __name__ == "__main__":
    print("mu g R, threshold, needed / alpha, depth:", [round(v, 4) for v in yukawa_threshold()])
