"""Hand k1, brief k: the one transient of the paces beyond 128 bits (the memo's exact fraction (Gamma - 1)^c over Gamma^(c - 1), 37,785 bits at Gamma 1,000's deepest admitted content) and the form that mends it within the laws: the clock as one carried division per content at the fixed wall Gamma on a value scaled by 2^K (V_0 = Gamma 2^K; V_(c + 1) Gamma + r_(c + 1) = V_c (Gamma - 1) + r_c, the division act with its remainder carried), the pace p_0(c) = rounded(V_c, 2^K), every integer within K + Gamma's bits + 1; measured bit for bit against the oracle core/paces.clock_alone (the independent power rounded once) at every content from 0 to the Link's zero, and the Link's pace rounded(p_0^2, Gamma) likewise, at K = 64 and at K = 32 (where the carried error shows), for Gamma 1,000 and 6,000 and the hills (c < 0) to -3 Gamma by the turned fraction (Gamma over Gamma - 1).

    PYTHONPATH=src python tools/derivations/open_items/H-Constants-Of-The-Universe-1/paces_within_bits.py > tools/derivations/open_items/H-Constants-Of-The-Universe-1/paces_within_bits.out
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "src"))

from event_universe.core import paces  # noqa: E402
from event_universe.core.rule3 import division_forward  # noqa: E402


def carried_clocks(gamma: int, count: int, guard: int, hill: bool) -> tuple[list[int], int]:
    """The clocks at the contents 0 .. count (hollows) or 0 .. -count (hills) by the carried recurrence; the largest transient's bits."""
    scale = 1 << guard
    value, remainder, largest = gamma * scale, 0, 0
    up, down = ((gamma, gamma - 1) if hill else (gamma - 1, gamma))
    found = []
    for _c in range(count + 1):
        found.append(int(paces.rounded(value, scale)))
        numerator = value * up + remainder
        largest = max(largest, numerator.bit_length())
        value, remainder = (int(x) for x in division_forward(numerator, down, 0))
    return found, largest


def main() -> None:
    for gamma in (1000, 6000):
        frozen = paces.frozen_content(gamma)
        oracle = [paces.clock_alone(gamma, c) for c in range(frozen)]
        oracle_links = [int(paces.rounded(p * p, gamma)) for p in oracle]
        hills = [paces.clock_alone(gamma, -c) for c in range(3 * gamma + 1)]
        c = frozen - 1
        print(f"Gamma {gamma}: the Link's zero at content {frozen}; the memo's exact fraction at c = {c}: {((gamma - 1) ** c).bit_length()} bits over {(gamma ** (c - 1)).bit_length()} bits (beyond 128)")
        for guard in (32, 64, 96):
            clocks, largest = carried_clocks(gamma, frozen - 1, guard, False)
            misses = [k for k in range(frozen) if clocks[k] != oracle[k]]
            links = [int(paces.rounded(p * p, gamma)) for p in clocks]
            link_misses = [k for k in range(frozen) if links[k] != oracle_links[k]]
            hill_clocks, hill_largest = carried_clocks(gamma, 3 * gamma, guard, True)
            hill_misses = [k for k in range(3 * gamma + 1) if hill_clocks[k] != hills[k]]
            print(f"Gamma {gamma} K {guard}: hollows 0..{frozen - 1}: clock mismatches against clock_alone {len(misses)} (first {misses[:3]}), Link's pace mismatches {len(link_misses)} (first {link_misses[:3]}); hills 0..-{3 * gamma}: mismatches {len(hill_misses)} (first {hill_misses[:3]}); largest transient {max(largest, hill_largest)} bits (within 128: {max(largest, hill_largest) <= 128})")


if __name__ == "__main__":
    main()
