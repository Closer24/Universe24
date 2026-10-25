"""Hand K2: two 128-bit forms of the clock against the engine's exact clock (core/paces.clock_alone, the power (Gamma - 1)^c over Gamma^(c - 1) rounded once).
(1) The plain iterated rounding p(c + 1) = rounded(p(c) (Gamma - 1), Gamma): it freezes where p / Gamma falls under a half, at p about Gamma div 2, and never reaches the frozen content (measured: the fixed point and the content it is reached at).
(2) The carried form, the division act with its remainder kept: p(c + 1) Gamma + r(c + 1) = p(c) (Gamma - 1) + r(c), every integer below Gamma^2 + Gamma; measured against the exact clock at every content to the frozen one at Gamma 1,000 (the differing contents, the largest difference, the frozen content by both, the deepest pace by both, the volume's deepest level by both) and on the first 400 contents and the deepest alone at Gamma 6,000. Integers only.

Run: PYTHONPATH=<worktree>/src python tools/derivations/open_items/H-Constants-Of-The-Universe-2/k2_iterated_clock.py > tools/derivations/open_items/H-Constants-Of-The-Universe-2/k2_iterated_clock.txt
"""

from __future__ import annotations

import json

from event_universe.core import paces
from event_universe.core.rule3 import division_forward
from event_universe.features import volume


def rounded(n: int, w: int) -> int:
    return int(division_forward(n + n, w + w, w)[0])


def volume_level(gamma: int, pace: int) -> int:
    e = volume.EXPONENT
    return int(division_forward(gamma ** (e + 1) + pace**e - 1, pace**e, 0)[0])


def plain_fixed_point(gamma: int) -> tuple[int, int]:
    p, c = gamma, 0
    while True:
        q = rounded(p * (gamma - 1), gamma)
        if q == p:
            return p, c
        p, c = q, c + 1


def carried(gamma: int, limit: int) -> tuple[list[int], int]:
    """The carried clock to the content `limit` or to its frozen content (rounded(p^2, Gamma) = 0), whichever first; the frozen content or -1."""
    p, r, found = gamma, 0, []
    frozen = -1
    for c in range(limit + 1):
        found.append(p)
        if rounded(p * p, gamma) == 0 and frozen < 0:
            frozen = c
            break
        q, r = division_forward(p * (gamma - 1), gamma, r)
        p = int(q)
        r = int(r)
    return found, frozen


def main() -> None:
    out = {}
    for gamma, reach in ((1000, None), (6000, 400)):
        frozen = paces.frozen_content(gamma)
        fixed, at = plain_fixed_point(gamma)
        out[str(gamma)] = {"plain_iterated_fixed_point_p": fixed, "reached_at_content": at, "Gamma_div_2": gamma // 2, "frozen_engine": frozen}
        limit = frozen + 200 if reach is None else reach
        found, frozen_carried = carried(gamma, limit)
        compare = min(len(found), frozen if reach is None else reach)
        exact = [paces.clock_alone(gamma, c) for c in range(compare)]
        diffs = [a - b for a, b in zip(exact, found[:compare], strict=True)]
        out[str(gamma)].update(
            {
                "carried_contents_compared": compare,
                "carried_differing_contents": sum(1 for d in diffs if d),
                "carried_largest_difference_units": max(abs(d) for d in diffs),
                "carried_first_differing_content": next((k for k, d in enumerate(diffs) if d), None),
                "carried_frozen_content": frozen_carried,
                "carried_p_before_frozen": found[frozen_carried - 1] if frozen_carried > 0 else None,
                "engine_p_before_frozen": paces.clock_alone(gamma, frozen - 1),
                "X_carried": volume_level(gamma, found[frozen_carried - 1]) if frozen_carried > 0 else None,
                "X_engine": volume_level(gamma, paces.clock_alone(gamma, frozen - 1)),
                "exact_fraction_bits_at_deepest": (2 * gamma * (gamma - 1) ** (frozen - 1) + gamma ** (frozen - 1)).bit_length(),
                "carried_largest_integer_bits": (gamma * (gamma - 1) + gamma).bit_length(),
                "p0_at_content_Gamma_engine": paces.clock_alone(gamma, gamma),
                "p0_at_content_Gamma_carried": found[gamma] if len(found) > gamma else None,
            }
        )
        print(json.dumps({gamma: out[str(gamma)]}), flush=True)
    print(json.dumps(out, indent=1))


if __name__ == "__main__":
    main()
