"""Hand N2: the record's den as three primes 1 mod 4 and what a fourth would have to be (items b and e). For every prime p of the record's den (examples/events/universe24/universe_universe24.json) the two squares p = a^2 + b^2 (loader/circle.two_squares), the lift's leg s = den x 2ab / p (checked against lift_points) and the sine 2ab/p as a quotient per 10^12; the lift steps as quotients (the mass ratios: nature's p/e 1836.153 and n/p 1.0013784); the condition for two heavy lifts near each other, sin(2 theta_p2) / sin(2 theta_p1) = m_n / m_p, read on the integers; and the neutrino: the prime q = c^2 + d^2 a den would need for a lift lighter than the electron's by m_e / m_nu at 1 eV, 0.1 eV and 0.01 eV (d = 1, c the least even number at or above the target with c^2 + 1 prime), its bits and the bits den x q would have against the law's 128. The lightest point of the record's den is read too (it is the electron's lift: no lighter point exists at this den). Integers only.

Run: PYTHONPATH=<worktree>/src TMPDIR=/dev/shm/tmp /home/user/Universe24/venv314/bin/python tools/derivations/n2/neutrino_prime.py
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

from event_universe.loader.circle import factors, is_prime, lift_points, lightest_point, two_squares

OUT = Path(__file__).with_name("out")
RECORD = json.loads((Path(__file__).resolve().parents[3] / "examples/events/universe24/universe_universe24.json").read_text(encoding="utf-8"))
DEN = int(RECORD["integers"]["den"])
T = int(RECORD["integers"]["quantum_action"])
M_E_OVER_M_NU = {"1 eV": 510999, "0.1 eV": 5109990, "0.01 eV": 51099895}  # m_e = 510,998.95 eV
NATURE = {"p_over_e_per_million": 1836152673, "n_over_p_per_million": 1001378}  # 1836.152673 and 1.0013784


def quotient(numerator: int, denominator: int, scale: int) -> list[int]:
    q, r = divmod(numerator * scale, denominator)
    return [int(q), int(r)]


def main() -> None:
    OUT.mkdir(exist_ok=True)
    primes = sorted(factors(DEN))
    lifts = {s: (list(v), n) for v, n, s in lift_points(DEN)}
    rows = []
    for p in primes:
        a, b = two_squares(p)
        a, b = max(a, b), min(a, b)
        leg = DEN * 2 * a * b // p
        rows.append(
            {
                "prime": p,
                "bits": p.bit_length(),
                "a": a,
                "b": b,
                "a_squared_plus_b_squared_is_prime": a * a + b * b == p,
                "sine_2ab_over_p_per_10_12": quotient(2 * a * b, p, 10**12),
                "lift_leg_den_2ab_div_p": leg,
                "lift_leg_exact": (DEN * 2 * a * b) % p == 0,
                "leg_is_a_lift_of_circle": leg in lifts,
                "lift_vector": lifts.get(leg, (None, None))[0],
                "lift_num": lifts.get(leg, (None, None))[1],
                "gap_den_minus_num": None if leg not in lifts else DEN - lifts[leg][1],
            }
        )
    rows.sort(key=lambda r: r["lift_leg_den_2ab_div_p"])
    e, p, n = rows
    steps = {
        "p_over_e_per_million": quotient(p["lift_leg_den_2ab_div_p"], e["lift_leg_den_2ab_div_p"], 10**6),
        "n_over_p_per_million": quotient(n["lift_leg_den_2ab_div_p"], p["lift_leg_den_2ab_div_p"], 10**6),
        "n_over_e_per_million": quotient(n["lift_leg_den_2ab_div_p"], e["lift_leg_den_2ab_div_p"], 10**6),
        "nature": NATURE,
        "two_heavy_lifts_condition": "sin(2 theta_n) / sin(2 theta_p) = (2 a_n b_n / p_n) / (2 a_p b_p / p_p) = m_n / m_p, two primes of den with their Gaussian angles' sines in nature's ratio",
        "sines_ratio_n_over_p_per_million": quotient(2 * n["a"] * n["b"] * p["prime"], 2 * p["a"] * p["b"] * n["prime"], 10**6),
    }
    num_min, s_min = lightest_point(DEN)
    lightest = {
        "s": s_min,
        "num": num_min,
        "gap": DEN - num_min,
        "is_the_electron_lift": s_min == e["lift_leg_den_2ab_div_p"],
        "g_per_10_24": quotient(DEN - num_min, DEN, 10**24),
    }
    # the neutrino's prime: a lift lighter than the electron's by m_e / m_nu needs 2cd/q = (2ab/p)_e / ratio; with d = 1 and c >> 1, 2/c ~ that, so c ~ ratio x p_e / (a_e b_e)
    neutrino = []
    for name, ratio in M_E_OVER_M_NU.items():
        c = (ratio * e["prime"]) // (e["a"] * e["b"])
        if c % 2:
            c += 1
        tried = 0
        while not is_prime(c * c + 1):
            c += 2
            tried += 1
        q = c * c + 1
        new_den = DEN * q
        leg_nu = new_den * 2 * c // q  # d = 1
        leg_e_new = new_den * 2 * e["a"] * e["b"] // e["prime"]
        neutrino.append(
            {
                "m_e_over_m_nu": name,
                "ratio": ratio,
                "c": c,
                "d": 1,
                "q_c2_plus_1": q,
                "q_bits": q.bit_length(),
                "evens_tried_before_a_prime": tried,
                "den_times_q_bits": new_den.bit_length(),
                "W_c_3_den_T_bits_at_new_den": (3 * new_den * T).bit_length(),
                "electron_over_neutrino_leg_per_million": quotient(leg_e_new, leg_nu, 10**6),
                "ratio_asked_per_million": ratio * 10**6,
            }
        )
    found = {
        "den": DEN,
        "den_bits": DEN.bit_length(),
        "T": T,
        "W_c_bits": (3 * DEN * T).bit_length(),
        "primes": rows,
        "lift_steps": steps,
        "lightest_point": lightest,
        "neutrino_prime": neutrino,
    }
    (OUT / "neutrino_prime.json").write_text(json.dumps(found, indent=1), encoding="utf-8")
    lines = [f"record den {DEN} ({DEN.bit_length()} bits), T {T}, W_c bits {found['W_c_bits']}"]
    for r in rows:
        lines.append(f"  prime {r['prime']} ({r['bits']} bits) = {r['a']}^2 + {r['b']}^2 ({r['a_squared_plus_b_squared_is_prime']}); sine 2ab/p {r['sine_2ab_over_p_per_10_12'][0]}/10^12; lift leg {r['lift_leg_den_2ab_div_p']} exact {r['lift_leg_exact']} lift {r['lift_vector']} num {r['lift_num']} gap {r['gap_den_minus_num']}")
    lines.append(f"  lift steps: p/e {steps['p_over_e_per_million']} /10^6 (nature {NATURE['p_over_e_per_million']} /10^6); n/p {steps['n_over_p_per_million']} /10^6 (nature {NATURE['n_over_p_per_million']}); n/e {steps['n_over_e_per_million']}; sines ratio n/p {steps['sines_ratio_n_over_p_per_million']}")
    lines.append(f"  lightest point s {lightest['s']} gap {lightest['gap']} g {lightest['g_per_10_24'][0]}/10^24: the electron's lift {lightest['is_the_electron_lift']}")
    for row in neutrino:
        lines.append(f"  neutrino at m_e/m_nu {row['m_e_over_m_nu']} ({row['ratio']}): c {row['c']} (tried {row['evens_tried_before_a_prime']}), q = c^2 + 1 ({row['q_bits']} bits); den x q {row['den_times_q_bits']} bits, W_c there {row['W_c_3_den_T_bits_at_new_den']} bits; e/nu leg {row['electron_over_neutrino_leg_per_million'][0]}/10^6 against {row['ratio_asked_per_million']}/10^6")
    text = "\n".join(lines) + "\n"
    (OUT / "neutrino_prime.txt").write_text(text, encoding="utf-8")
    sys.stdout.write(text)


if __name__ == "__main__":
    main()
