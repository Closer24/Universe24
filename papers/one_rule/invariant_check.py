"""The adiabatic invariant of the one-Node line, S.14's check (Section 7.4, R227): the recurrence
a_next + a_before = 2 cos(omega_t) a_now stepped over 20,000 intervals with omega lowered linearly from 0.841
to 0.600 keeps D / sin(omega) = A^2 sin(omega), D = a_t^2 - a_{t+1} a_{t-1}, within 4 x 10^-5 of its start while
D itself falls by a quarter. Floating point, one Node, no run of the engine.

    python paper/invariant_check.py
"""

from __future__ import annotations

import math

INTERVALS = 20_000
OMEGA_START, OMEGA_END = 0.841, 0.600
PHASES = (0.0, 0.3, 1.0, 1.7, 2.5)


def worst_drift(phase: float) -> tuple[float, float]:
    """The largest relative departure of D / sin(omega) from its start, and D's end over its start."""
    a_before = math.cos(phase - OMEGA_START)
    a_now = math.cos(phase)
    start = None
    worst = 0.0
    ratio = 1.0
    for t in range(INTERVALS):
        omega = OMEGA_START + (OMEGA_END - OMEGA_START) * t / (INTERVALS - 1)
        a_next = 2.0 * math.cos(omega) * a_now - a_before
        d = a_now * a_now - a_next * a_before
        invariant = d / math.sin(omega)
        if start is None:
            start = (invariant, d)
        worst = max(worst, abs(invariant / start[0] - 1.0))
        ratio = d / start[1]
        a_before, a_now = a_now, a_next
    return worst, ratio


def main() -> None:
    print(f"omega lowered from {OMEGA_START} to {OMEGA_END} over {INTERVALS} intervals")
    overall = 0.0
    for phase in PHASES:
        worst, ratio = worst_drift(phase)
        overall = max(overall, worst)
        print(
            f"  phase {phase}: D / sin(omega) within {worst:.1e} of its start; D's end over its start {ratio:.3f}"
        )
    print(
        f"the worst drift over the phases: {overall:.1e} (the paper's bound 4e-5); sin(0.600) / sin(0.841) = {math.sin(0.600) / math.sin(0.841):.3f}"
    )


if __name__ == "__main__":
    main()
