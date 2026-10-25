"""Hand k1, brief k, part (b)(ii) and (iii): Gamma and T as resolutions under the principle "the constants are the largest
the 128 bits allow", through the loader's own derivation of the width (loader/rooms.width_of: the least width at which the
amplitude bound holds the volume's level at the deepest admitted content) and the bound (loader/derived.amplitude_bound);
den's bits against the transients (Rule3's total at the bound, the wall, the held walls, the paces' exact fraction).

For each den of the window and the 54-bit control, at G 16 (the engine's) and at G 32 (the least power of two resolving one
level of tension at Gamma 1,000): the width, A and the transients at Gamma 1,000 / T 36,000; the largest T within 128 bits
at Gamma 1,000; the largest Gamma within 128 bits at T 36,000; the frontier T_max(Gamma) at Gamma 250, 500, 1,000, 2,000,
4,000, 8,000 (whether the principle fixes a point or leaves a ratio free). Integer readings only.

    PYTHONPATH=src python tools/derivations/k1/resolutions.py > tools/derivations/k1/resolutions.out
"""

from __future__ import annotations

import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "src"))

from event_universe.core import paces  # noqa: E402
from event_universe.core.rule3 import coefficients, mass, partial_rooms, wall_of  # noqa: E402
from event_universe.features.read import edge_of  # noqa: E402
from event_universe.loader import derived  # noqa: E402
from event_universe.loader.rooms import width_of  # noqa: E402
from event_universe.loader.universe import universe_of  # noqa: E402

BITS = 128
DENS = (1021, 348893, 1655909141, 4471099877, 15162856759112389)
GAMMA, ACTION = 1000, 36000


def families_at(den: int, gamma: int, action: int):
    return universe_of({"integers": {"den": den, "node_clock": gamma, "quantum_action": action}})[1]


def width_at(den: int, gamma: int, action: int, unit: int) -> int | None:
    try:
        return width_of(families_at(den, gamma, action), gamma, action, unit)
    except ValueError as refusal:
        print(f"   refused at den {den} Gamma {gamma} T {action} G {unit}: {str(refusal)[:160]}")
        return None


def transients(den: int, gamma: int, action: int, unit: int) -> dict:
    families = families_at(den, gamma, action)
    width = width_of(families, gamma, action, unit)
    bound = derived.amplitude_bound(families, gamma, action, width, unit)
    largest_total, largest_wall, largest_held = 0, 0, 0
    for family in families:
        num, d = family.pair
        edge = edge_of(family.pair, gamma)
        for clock, pace in ((gamma, gamma), (0, 0), (edge, edge)):
            reads, self_coefficient, wall = coefficients(num, d, gamma, clock, pace, None, unit)
            plain = sum(abs(r) for r in reads)
            own = mass(num, d, clock, unit)
            *_partials, total = partial_rooms(self_coefficient, wall, own, plain + plain, plain)
            largest_total = max(largest_total, total * bound + wall - 1)
        largest_wall = max(largest_wall, wall_of(d, gamma, unit))
        if family.held:
            write = derived.held_write_of(families, families.index(family), action)
            largest_held = max(largest_held, max(write.walls))
    c = paces.frozen_content(gamma) - 1
    fraction_bits = max(((gamma - 1) ** c).bit_length(), (gamma ** (c - 1)).bit_length())
    return {
        "families": len(families),
        "width": width,
        "A": bound,
        "A_bits": bound.bit_length(),
        "rule3_total_bits": largest_total.bit_length(),
        "wall_bits": largest_wall.bit_length(),
        "held_wall_bits": largest_held.bit_length(),
        "paces_fraction_bits": fraction_bits,
        "deepest_content": c,
    }


def largest_action(den: int, gamma: int, unit: int) -> int:
    """The largest T with the derived width within BITS at (den, Gamma, G): doubling then halving on T (the width grows with T)."""
    low, high = 1, 2
    while (w := width_at(den, gamma, high, unit)) is not None and w <= BITS:
        low, high = high, high * 2
        if high.bit_length() > 400:
            break
    while high - low > 1:
        middle = (low + high) // 2
        w = width_at(den, gamma, middle, unit)
        if w is not None and w <= BITS:
            low = middle
        else:
            high = middle
    return low


def largest_gamma(den: int, action: int, unit: int, cap: int = 1 << 22) -> int:
    """The largest Gamma with the derived width within BITS at (den, T, G): doubling then halving on Gamma from 2."""
    low, high = 2, 4
    while high <= cap and (w := width_at(den, high, action, unit)) is not None and w <= BITS:
        low, high = high, high * 2
    while high - low > 1:
        middle = (low + high) // 2
        w = width_at(den, middle, action, unit)
        if w is not None and w <= BITS:
            low = middle
        else:
            high = middle
    return low


def main() -> None:
    for unit in (16, 32):
        print(f"==== G = {unit} ====")
        for den in DENS:
            t0 = time.time()
            found = transients(den, GAMMA, ACTION, unit)
            print(f"den {den} ({den.bit_length()} bits) Gamma {GAMMA} T {ACTION} G {unit}: {found}; within {BITS}: width {found['width'] <= BITS}, Rule3 total {found['rule3_total_bits'] <= BITS}, paces' fraction {found['paces_fraction_bits'] <= BITS}")
            t_max = largest_action(den, GAMMA, unit)
            print(f"  largest T within {BITS} bits at Gamma {GAMMA}: {t_max} ({t_max.bit_length()} bits); A = isqrt(T div 2) = {paces.largest_below(t_max // 2)}; width there {width_at(den, GAMMA, t_max, unit)}, at T + 1: {width_at(den, GAMMA, t_max + 1, unit)}")
            g_max = largest_gamma(den, ACTION, unit)
            print(f"  largest Gamma within {BITS} bits at T {ACTION}: {g_max} ({g_max.bit_length()} bits); width there {width_at(den, g_max, ACTION, unit)}, at Gamma + 1: {width_at(den, g_max + 1, ACTION, unit)}; the clock's half-life about {g_max * 693 // 1000} levels")
            if den in (1021, 348893):
                frontier = []
                for gamma in (250, 500, 1000, 2000, 4000, 8000):
                    t_g = largest_action(den, gamma, unit)
                    frontier.append((gamma, t_g, t_g.bit_length()))
                print(f"  frontier T_max(Gamma): {frontier}")
                print(f"  Gamma^5 T_max bit lengths along the frontier: {[(g, (g ** 5 * t).bit_length()) for g, t, _b in frontier]}; Gamma^4 T_max: {[(g, (g ** 4 * t).bit_length()) for g, t, _b in frontier]}")
            print(f"  ({time.time() - t0:.1f} s)")
            sys.stdout.flush()


if __name__ == "__main__":
    main()
