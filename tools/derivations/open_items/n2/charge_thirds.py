"""Hand N2: the charge's unit T div 2 under thirds on the lay's integers (item c). The quarter-turn lay of one plane at the count carries A^2 = isqrt(T div 2)^2 as its Wronskian, the charge unit; three planes at T div 6 each would carry a third; the tightest split of T div 2 into three squares (ALGEBRA.md, The conversion: 5450 + 5458 + 5476 = 16384 at T 32,768). Measured at T 36,000 (the record's), 32,768 (the paper's) and 35,574 = 6 x 77^2 (the least T near them whose sixth is a square). Integers only.

Run: PYTHONPATH=<worktree>/src TMPDIR=/dev/shm/tmp /home/user/Universe24/venv314/bin/python tools/derivations/n2/charge_thirds.py
"""

from __future__ import annotations

import json
import sys
from math import gcd
from pathlib import Path

from event_universe.core.rule3 import largest_below

OUT = Path(__file__).with_name("out")
ACTIONS = (36000, 32768, 35574)


def tightest_three_squares(w: int) -> tuple[int, int, int] | None:
    """a^2 + b^2 + c^2 = w with a >= b >= c >= 0 and the spread a - c least (the lay's exact split)."""
    best: tuple[int, int, int] | None = None
    a = largest_below(w)
    while a >= 0 and 3 * a * a >= w:
        rest = w - a * a
        b = min(a, largest_below(rest))
        while b >= 0 and 2 * b * b >= rest:
            c2 = rest - b * b
            c = largest_below(c2)
            if c * c == c2 and c <= b:
                if best is None or (a - c) < (best[0] - best[2]):
                    best = (a, b, c)
            b -= 1
        a -= 1
    return best


def reduced(n: int, d: int) -> list[int]:
    g = gcd(n, d)
    return [n // g, d // g]


def report(action: int) -> dict:
    unit = action // 2  # the charge's unit, the Wronskian of one quantum, T div 2
    a = largest_below(unit)  # the quarter-turn lay's amplitude isqrt(T div 2)
    third = action // 6
    t = largest_below(third)
    split = tightest_three_squares(unit)
    found = {
        "T": action,
        "unit_T_div_2": unit,
        "lay_amplitude_isqrt": a,
        "lay_wronskian_A2": a * a,
        "lay_short_of_unit": unit - a * a,
        "unit_exact_square": a * a == unit,
        "T_div_6": third,
        "T_div_6_times_3_equals_unit": 3 * third == unit,
        "third_isqrt": t,
        "third_square": t * t,
        "third_exact_square": t * t == third,
        "three_planes_at_isqrt_T_div_6_sum": 3 * t * t,
        "three_planes_short_of_unit": unit - 3 * t * t,
        "integer_thirds_exact_iff_6_divides_T": action % 6 == 0,
        "integer_thirds_of_unit": [unit // 3 + (1 if i < unit % 3 else 0) for i in range(3)],
        "nature_fractions_two_thirds_one_third_of_unit": [(2 * unit) // 3, unit // 3, (2 * unit) % 3, unit % 3],
    }
    if split is not None:
        found["tightest_split_of_unit"] = list(split)
        found["tightest_split_fractions_of_unit"] = [reduced(x * x, unit) for x in split]
        found["tightest_split_spread"] = split[0] - split[2]
        found["tightest_split_thirds_exact"] = all(3 * x * x == unit for x in split)
    return found


def main() -> None:
    OUT.mkdir(exist_ok=True)
    rows = [report(action) for action in ACTIONS]
    # the theorem on the integers: the unit T div 2 a square and T div 6 a square cannot both hold
    both = [action for action in range(2, 100000) if largest_below(action // 2) ** 2 == action // 2 and action % 6 == 0 and largest_below(action // 6) ** 2 == action // 6]
    summary = {
        "rows": rows,
        "T_below_100000_with_unit_square_and_sixth_square": both,
        "T_below_100000_with_unit_square": sum(1 for action in range(2, 100000) if largest_below(action // 2) ** 2 == action // 2),
        "T_below_100000_with_sixth_square": sum(1 for action in range(2, 100000) if action % 6 == 0 and largest_below(action // 6) ** 2 == action // 6),
    }
    (OUT / "charge_thirds.json").write_text(json.dumps(summary, indent=1), encoding="utf-8")
    lines = []
    for r in rows:
        lines.append(
            f"T {r['T']}: unit T div 2 = {r['unit_T_div_2']}; the lay's A = {r['lay_amplitude_isqrt']}, A^2 = {r['lay_wronskian_A2']} (short {r['lay_short_of_unit']}; exact {r['unit_exact_square']});"
            f" T div 6 = {r['T_div_6']}, isqrt {r['third_isqrt']}, square {r['third_square']} (exact {r['third_exact_square']}); three planes at it {r['three_planes_at_isqrt_T_div_6_sum']} (short {r['three_planes_short_of_unit']})"
        )
        lines.append(f"  integer thirds of the unit (any Wronskians): {r['integer_thirds_of_unit']} exact iff 6 | T: {r['integer_thirds_exact_iff_6_divides_T']}; nature's 2/3 and 1/3 of the unit [q2, q1, r2, r1]: {r['nature_fractions_two_thirds_one_third_of_unit']}")
        if "tightest_split_of_unit" in r:
            lines.append(f"  tightest split of the unit into three squares {r['tightest_split_of_unit']} fractions {r['tightest_split_fractions_of_unit']} spread {r['tightest_split_spread']} thirds exact {r['tightest_split_thirds_exact']}")
    lines.append(f"T below 100000 with the unit a square: {summary['T_below_100000_with_unit_square']}; with the sixth a square: {summary['T_below_100000_with_sixth_square']}; with both: {summary['T_below_100000_with_unit_square_and_sixth_square']}")
    text = "\n".join(lines) + "\n"
    (OUT / "charge_thirds.txt").write_text(text, encoding="utf-8")
    sys.stdout.write(text)


if __name__ == "__main__":
    main()
