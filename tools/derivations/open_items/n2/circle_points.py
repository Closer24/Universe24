"""Hand N2: den's circle at the dens the brief names (3,311,818,282 and 697,786) and at G-S1's dens (1,655,909,141 and 348,893) and the toy's 1,021: the primes 1 mod 4, every point of the open quadrant, the lifts with their legs, their gaps as integer quotients, the mass ratios of the lifts' legs, the neutron-like step nearest nature's 1.0013784 among every pair of points, the lifts' walls against two light quanta, the lightest point (the neutrino-like candidate) and the bit widths. Integers only (quotients with remainders, bit lengths); no float. Reads src/ and writes nothing into it.

Run: PYTHONPATH=<worktree>/src TMPDIR=/dev/shm/tmp /home/user/Universe24/venv314/bin/python tools/derivations/n2/circle_points.py
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

from event_universe.core.rule3 import largest_below
from event_universe.loader.circle import circle_points, factors, lift_points, lightest_point

GAMMA, T, G = 1000, 36000, 16  # the toy's clock, action and Link unit (tests/laws_universe.py, the record's files)
DENS = (3311818282, 697786, 1655909141, 348893, 1021, 21397363965165989151899244775347635252768274397)  # the last the record's den (examples/events/universe24), three primes
NATURE_N_OVER_P_PER_MILLION = 1001378  # m_n / m_p = 1.0013784, the brief's 1.00138
NATURE_P_OVER_E_PER_THOUSAND = 1836153  # m_p / m_e = 1836.153
OUT = Path(__file__).with_name("out")


def quotient(numerator: int, denominator: int, scale: int) -> list[int]:
    """numerator / denominator at the scale as [quotient, remainder] of (numerator x scale) div denominator: an integer reading."""
    q, r = divmod(numerator * scale, denominator)
    return [int(q), int(r)]


def wall_of(s: int) -> int:
    """One quantum's wall of a Pythagorean point: 3 T s (count_wall at a Pythagorean pair, exact)."""
    return 3 * T * s


def report(den: int) -> dict:
    primes = factors(den)
    points = circle_points(den)
    lifts = lift_points(den)
    light_quantum = 3 * den * T  # W_c, the massless quantum's measure
    found: dict = {
        "den": den,
        "den_bits": den.bit_length(),
        "primes": {str(p): e for p, e in sorted(primes.items())},
        "primes_1_mod_4": [p for p in sorted(primes) if p % 4 == 1],
        "points_in_the_open_quadrant": len(points),
        "wall_w_bits": (6 * den * GAMMA * GAMMA * G * G).bit_length(),
        "W_c_bits": light_quantum.bit_length(),
        "half_wall_bits_at_two_light_quanta": (2 * light_quantum).bit_length(),
    }
    rows = []
    for vector, num, s in lifts:
        gap = den - num
        rows.append(
            {
                "vector": list(vector),
                "num": num,
                "s": s,
                "gap_den_minus_num": gap,
                "g_milli": quotient(gap, den, 1000),
                "s_over_den_micro": quotient(s, den, 1_000_000),
                "compton_milli_links_isqrt_den2_over_3s2": largest_below((den * den * 1_000_000) // (3 * s * s)),
                "wall_3Ts": wall_of(s),
                "pair_walls_fit_two_light_quanta": 2 * wall_of(s) <= 2 * light_quantum,
                "pair_walls_over_two_quanta_milli": quotient(2 * wall_of(s), 2 * light_quantum, 1000),
            }
        )
    rows.sort(key=lambda r: r["s"])
    found["lifts_by_rising_leg"] = rows
    if len(rows) >= 2:
        light, heavy = rows[0], rows[-1]
        found["mass_ratio_heaviest_lift_over_lightest_milli"] = quotient(heavy["s"], light["s"], 1000)
        found["nature_p_over_e_milli"] = NATURE_P_OVER_E_PER_THOUSAND
        steps = []
        for i in range(len(rows) - 1):
            steps.append(
                {
                    "from_vector": rows[i]["vector"],
                    "to_vector": rows[i + 1]["vector"],
                    "leg_ratio_per_million": quotient(rows[i + 1]["s"], rows[i]["s"], 1_000_000),
                }
            )
        found["lift_steps"] = steps
    # the neutron-like step: among every pair of points the leg ratio nearest nature's 1.0013784 (per million)
    legs = sorted({s for _v, _n, s in points})
    best = None
    for i, a in enumerate(legs):
        for b in legs[i + 1 :]:
            ratio = (b * 1_000_000) // a
            if ratio > 1_100_000:
                break
            miss = abs(ratio - NATURE_N_OVER_P_PER_MILLION)
            if best is None or miss < best[0]:
                best = (miss, a, b, ratio)
    if best is not None:
        miss, a, b, ratio = best
        who = {s: (list(v), n) for v, n, s in points}
        found["neutron_like_step_nearest_nature"] = {
            "light_leg": a,
            "light_point": who[a],
            "heavy_leg": b,
            "heavy_point": who[b],
            "leg_ratio_per_million": ratio,
            "nature_per_million": NATURE_N_OVER_P_PER_MILLION,
            "miss_per_million": miss,
            "heavy_is_a_lift": any(s == b for _v, _n, s in lifts),
            "light_is_a_lift": any(s == a for _v, _n, s in lifts),
        }
    num_min, s_min = lightest_point(den)
    found["lightest_point"] = {
        "num": num_min,
        "s": s_min,
        "gap": den - num_min,
        "g_micro": quotient(den - num_min, den, 1_000_000),
        "den_over_s_milli": quotient(den, s_min, 1000),
        "is_a_lift": any(s == s_min for _v, _n, s in lifts),
    }
    return found


def main() -> None:
    OUT.mkdir(exist_ok=True)
    results = [report(den) for den in DENS]
    (OUT / "circle_points.json").write_text(json.dumps(results, indent=1), encoding="utf-8")
    lines = []
    for r in results:
        lines.append(f"den {r['den']} ({r['den_bits']} bits) = {r['primes']}; points {r['points_in_the_open_quadrant']}; w bits {r['wall_w_bits']}; W_c bits {r['W_c_bits']}")
        for row in r["lifts_by_rising_leg"]:
            lines.append(
                f"  lift {row['vector']}: num {row['num']} s {row['s']} g {row['g_milli'][0]}/1000 r{row['g_milli'][1]}"
                f" s/den {row['s_over_den_micro'][0]}/10^6; Compton {row['compton_milli_links_isqrt_den2_over_3s2']} milli-Links;"
                f" wall 3Ts {row['wall_3Ts']}; pair walls / 2 W_c {row['pair_walls_over_two_quanta_milli'][0]}/1000"
            )
        if "mass_ratio_heaviest_lift_over_lightest_milli" in r:
            lines.append(f"  heaviest lift / lightest lift {r['mass_ratio_heaviest_lift_over_lightest_milli']} /1000 (nature p/e 1836153)")
            for st in r["lift_steps"]:
                lines.append(f"  lift step {st['from_vector']} -> {st['to_vector']}: {st['leg_ratio_per_million']} /10^6")
        if "neutron_like_step_nearest_nature" in r:
            n = r["neutron_like_step_nearest_nature"]
            lines.append(
                f"  neutron-like step nearest nature: legs {n['light_leg']} -> {n['heavy_leg']} ratio {n['leg_ratio_per_million']}/10^6"
                f" (nature {n['nature_per_million']}, miss {n['miss_per_million']}); heavy is a lift: {n['heavy_is_a_lift']}, light is a lift: {n['light_is_a_lift']}"
            )
        lp = r["lightest_point"]
        lines.append(f"  lightest point num {lp['num']} s {lp['s']} gap {lp['gap']} g {lp['g_micro'][0]}/10^6 den/s {lp['den_over_s_milli'][0]}/1000 lift: {lp['is_a_lift']}")
    text = "\n".join(lines) + "\n"
    (OUT / "circle_points.txt").write_text(text, encoding="utf-8")
    sys.stdout.write(text)


if __name__ == "__main__":
    main()
