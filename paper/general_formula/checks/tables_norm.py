"""The norm of the phase tables, C_N^2 + S_N^2, for every power of two N through 65536.

The paper states the range of the norm about 65536 and the two identities the
click's proofs use (the half turn and the quarter turn exact). A computation
from the repository's tables (core/phase.py), not a run of the engine.
"""

from __future__ import annotations

import sys

sys.path.insert(0, "src")
from event_universe.core.phase import MAX_PHASE_STEPS, phase_cosines, phase_sines  # noqa: E402


def main() -> None:
    worst_low, worst_high = None, None
    n = 4
    while n <= MAX_PHASE_STEPS:
        c, s = phase_cosines(n), phase_sines(n)
        shifted = tuple(c[(p - n // 4) % n] for p in range(n))
        half = all(c[(p + n // 2) % n] == -c[p] for p in range(n))
        norms = [(c[p] ** 2 + s[p] ** 2, p) for p in range(n)]
        low, high = min(norms), max(norms)
        print(
            f"N={n:6d}: quarter turn exact {s == shifted}, half turn exact {half}, "
            f"norm - 65536 from {low[0] - 65536:+d} (p={low[1]}, C={c[low[1]]}, S={s[low[1]]}) "
            f"to {high[0] - 65536:+d} (p={high[1]}, C={c[high[1]]}, S={s[high[1]]})"
        )
        if worst_low is None or low[0] < worst_low[0]:
            worst_low = (low[0], n, low[1])
        if worst_high is None or high[0] > worst_high[0]:
            worst_high = (high[0], n, high[1])
        n *= 2
    assert worst_low is not None and worst_high is not None
    print(
        f"over the powers of two through {MAX_PHASE_STEPS}: the norm lies in "
        f"[{worst_low[0]}, {worst_high[0]}] = 65536 {worst_low[0] - 65536:+d} .. {worst_high[0] - 65536:+d} "
        f"(the minimum at N={worst_low[1]}, p={worst_low[2]}; the maximum at N={worst_high[1]}, p={worst_high[2]})"
    )
    c64 = phase_cosines(128)
    print(
        f"the rotation at N=64, s=1: C'={c64[1]}, S'={c64[(1 - 32) % 128]}, n_s={c64[1] ** 2 + c64[(1 - 32) % 128] ** 2}"
    )


if __name__ == "__main__":
    main()
