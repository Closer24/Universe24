"""THE TWIST TABLE'S GENERATOR AND CHECK, the host's floats (ALGEBRA.md #the-primitives, #the-transport): the fine table of 2^10 Pythagorean triples for the angles k_0 theta_unit and the
coarse table for the angles k_1 (2^10 theta_unit), theta_unit = 1 / (4 Gamma 2^16) radians,
each triple (m^2 - n^2, 2 m n, m^2 + n^2) from the n / m nearest tan(angle / 2) with d at most
10^9. The engine reads the integers alone (`event_universe.events.primitives.TwistTable`); the
identities are the module's check, the angles this tool's. HOST.

THE FINDING (HOST, 2026-09-26, Nature24 for the mathematician): every Pythagorean triple's
angle is 2 atan(n / m), so with d = m^2 + n^2 at most 10^9 the smallest nonzero angle is about
2 / sqrt(10^9) = 6.3 x 10^-5 radians. theta_unit = 1 / (4 Gamma 2^16) = 3.8 x 10^-10 radians,
and the fine table's angles k_0 theta_unit (k_0 below 2^10) are all below 3.9 x 10^-7: none of
them is representable but the identity, and the precision theta_unit / 2^10 of ALGEBRA.md #the-primitives
cannot be met by any triple under that bound (nor the 10^-6 radian of ALGEBRA.md #the-transport, by a
factor of about 60). `check_angles` reports the largest miss against the representable floor
`SMALLEST_ANGLE`; the table's form waits for the mathematician's line (a coarser unit, a
larger d, or the fine part folded into the coarse).

    PYTHONPATH=src python tools/twist_table.py OUT.json [--coarse N] [--gamma G]
"""

from __future__ import annotations

import argparse
import json
import math
import sys
from fractions import Fraction
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from event_universe.events.primitives import FINE_SIZE, Triple, TwistTable, is_triple  # noqa: E402

GAMMA = 10_000
UNIT_SCALE = 1 << 16
DENOMINATOR_BOUND = 10**9
COARSE_DEFAULT = 1 << 15  # at most 2^15 coarse entries (ALGEBRA.md #the-primitives)
SMALLEST_ANGLE = 2.0 * math.atan(
    1.0 / math.isqrt(DENOMINATOR_BOUND)
)  # the representable floor, about 6.3e-5


def theta_unit(gamma: int = GAMMA) -> float:
    return 1.0 / (4 * gamma * UNIT_SCALE)


def triple_for(angle: float) -> Triple:
    """The triple whose angle is nearest `angle`: n / m nearest tan(angle / 2) with m^2 + n^2
    at most 10^9, (m^2 - n^2, 2 m n, m^2 + n^2)."""
    if angle == 0.0:
        return (1, 0, 1)
    ratio = Fraction(math.tan(angle / 2.0)).limit_denominator(int(math.isqrt(DENOMINATOR_BOUND)))
    n, m = ratio.numerator, ratio.denominator
    return (m * m - n * n, 2 * m * n, m * m + n * n)


def angle_of(triple: Triple) -> float:
    c, s, _ = triple
    return math.atan2(s, c)


def build(coarse: int = COARSE_DEFAULT, gamma: int = GAMMA) -> TwistTable:
    unit = theta_unit(gamma)
    fine = tuple(triple_for(k * unit) for k in range(FINE_SIZE))
    coarse_entries = tuple(triple_for(k * FINE_SIZE * unit) for k in range(coarse))
    return TwistTable(fine, coarse_entries)


def check_angles(table: TwistTable, gamma: int = GAMMA, tolerance: float | None = None) -> float:
    """Every triple's angle within `tolerance` of its target (ALGEBRA.md #the-primitives asks theta_unit /
    2^10; the representable floor SMALLEST_ANGLE is the default here, the finding above);
    returns the largest miss (HOST)."""
    unit = theta_unit(gamma)
    allowed = SMALLEST_ANGLE if tolerance is None else tolerance
    largest = 0.0
    for name, entries, step in (("fine", table.fine, unit), ("coarse", table.coarse, FINE_SIZE * unit)):
        for index, triple in enumerate(entries):
            if not is_triple(triple):
                raise ValueError(f"the {name} triple {index} {triple} is no Pythagorean triple")
            miss = abs(angle_of(triple) - index * step)
            largest = max(largest, miss)
            if miss > allowed:
                raise ValueError(
                    f"the {name} triple {index} {triple} misses its angle {index * step} by {miss}"
                )
    return largest


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("out", type=Path)
    parser.add_argument("--coarse", type=int, default=COARSE_DEFAULT)
    parser.add_argument("--gamma", type=int, default=GAMMA)
    args = parser.parse_args()
    table = build(args.coarse, args.gamma)
    table.check()
    miss = check_angles(table, args.gamma)
    print(
        f"the largest miss of an angle {miss:.3e} radians against the asked theta_unit / 2^10 = "
        f"{theta_unit(args.gamma) / FINE_SIZE:.3e} (the finding in this tool's docstring)"
    )
    args.out.write_text(
        json.dumps({"fine": [list(t) for t in table.fine], "coarse": [list(t) for t in table.coarse]})
        + "\n",
        encoding="utf-8",
    )
    largest = max(t[2] for t in table.fine + table.coarse)
    print(
        f"{args.out}: {len(table.fine)} fine and {len(table.coarse)} coarse triples, the bound {table.bound}, the largest d {largest}"
    )


if __name__ == "__main__":
    main()
