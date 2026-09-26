"""ITEM 2, THE ALGEBRA'S NUMBER beside the run's (record 2137): Newton's fall of the two bodies
by the algebra's own line, a = 2 (1 - 2U)^3 / (1 + (1 - 2U)^2) x (num / den) (dc/dx) / (6 Gamma)
(ALGEBRA.md 9.98 (7), 9.102 (2)), with dc/dx and U read from the static content of the two
bodies (the same relaxation the run starts from, GAMEBOARD of the runner), each body pulled by
the gradient at its centre, integrated in time from rest at the run's separation until the
centres are one side apart (the run's meeting). A COMPUTATION, written after the run and not
fed into it.

    PYTHONPATH=src python docs/designs/rule_alone/item2_algebra.py
"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import bodies as B  # noqa: E402
import item2_pair as I2  # noqa: E402

GAMMA = 10_000


def main() -> None:
    shape, wrap = I2.SHAPE, I2.WRAP
    middle = shape[1] // 2
    num, den = B.KIND
    # one body's static field alone (the fields add): its gradient along x on the axis
    lone = B.Body([shape[0] // 2, middle, middle], I2.AMOUNT)
    field = B.static_content(shape, wrap, [lone]).astype(np.float64)[:, middle, middle]
    x0 = shape[0] // 2

    def content_and_gradient(distance: float) -> tuple[float, float]:
        """The other body's content and its slope at a point `distance` Links from its centre."""
        r = x0 + distance
        i = int(np.floor(r))
        f = r - i
        c = (1 - f) * field[i] + f * field[i + 1]
        slope = field[i + 1] - field[i]
        return c, slope

    xa, xb = float(shape[0] // 2 - I2.SEPARATION // 2), float(shape[0] // 2 + I2.SEPARATION // 2)
    va = vb = 0.0
    t = 0
    rows = []
    while xb - xa > B.SIDE and t < 5000:
        # A reads B's field (and its own, uniform over its Nodes: no slope); U from the total
        c_other_a, slope_a = content_and_gradient(
            xa - xb
        )  # B's field at A: distance negative, slope toward B
        c_other_b, slope_b = content_and_gradient(xb - xa)
        u_a = (c_other_a + I2.AMOUNT) / (2 * GAMMA)
        u_b = (c_other_b + I2.AMOUNT) / (2 * GAMMA)
        factor_a = 2 * (1 - 2 * u_a) ** 3 / (1 + (1 - 2 * u_a) ** 2)
        factor_b = 2 * (1 - 2 * u_b) ** 3 / (1 + (1 - 2 * u_b) ** 2)
        # a falls toward higher content: d c / d x at A points toward B (positive), at B toward A
        aa = factor_a * (num / den) * slope_a / (6 * GAMMA)
        ab = factor_b * (num / den) * slope_b / (6 * GAMMA)
        va += aa
        vb += ab
        xa += va
        xb += vb
        t += 1
        if t % 50 == 0:
            rows.append((t, xa, xb, xb - xa, aa, u_a))
    print("the lone body's static content along the axis (GAMEBOARD of the runner), from its centre:")
    print("  r:", list(range(0, 24, 2)))
    print("  c:", [int(field[x0 + r]) for r in range(0, 24, 2)])
    for t_, a_, b_, s_, acc, u in rows:
        print(f"t {t_:4d}  A {a_:8.3f}  B {b_:8.3f}  separation {s_:7.3f}  a_A {acc:.3e}  U_A {u:.4f}")
    print(f"the algebra's meeting (centres one side apart): t = {t} intervals")


if __name__ == "__main__":
    main()
