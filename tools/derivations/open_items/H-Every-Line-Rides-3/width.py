"""Hand R3 (2026-10-25), item (b): the width of the riding line, w X within 128 bits, integer readings only.

The riding line's wall at a Node is w X_now with w = 6 den Gamma^2 G^2 and X = Gamma (Gamma / p_0)^(d + 1), d + 1 = 4
(features/volume, the engine's X; the brief writes e^(3U) Gamma, V1 named the slip: X / Gamma = e^(4U) to the paces'
rounding). The state's integer is the remainder r in [0, w X): its bit length is the state's width. The transient is
the numerator w X_now a_now + w X_before (a_now - a_before) + X_now F + r, at most X w (5 A + 1) at levels within A
(F at most 6 R A with R = 2 den p^2 G^2 <= w / 3). Read at den 1,021, at the 54-bit candidate 15,162,856,759,112,389,
at a den of about 40 bits (the least prime 1 mod 4 above 2^40) and at the top tier's 22-digit den, with G = 16 and G = 1:
the bits of w X at the record's U = 2.5 (the content level whose e^U = Gamma / p_0 is 12.18, a = 2500 at Gamma 1,000
to the clock's rounding), the largest X whose w X stays below 2^127 and its level and e^U, and the transient's room at
A = 4,096 (the levels within 12 bits, ENGINE.md section 10) and at the loader's amplitude bound of den 1,021.
Command: PYTHONPATH=src TMPDIR=/dev/shm/tmp /home/user/Universe24/venv314/bin/python tools/derivations/open_items/H-Every-Line-Rides-3/width.py
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve()
ROOT = HERE.parents[3]
for path in (ROOT / "src", ROOT):
    if str(path) not in sys.path:
        sys.path.insert(0, str(path))

from event_universe.core import paces  # noqa: E402
from event_universe.core.rule3 import division_forward, wall_of  # noqa: E402
from event_universe.features import volume  # noqa: E402

GAMMA = 1000
SCALE = 10**6
BITS = 128
SIGNED = 2**127  # the signed 128-bit range's half: an integer within 128 bits lies below it
LEVEL_RECORD = 2500  # the content level whose e^U is 12.18 at Gamma 1,000 (U = 2.5, the record's U's)
AMPLITUDES = (4096, 3696726972)  # the levels within 12 bits; the loader's amplitude bound at den 1,021


def is_prime(n: int) -> bool:
    """Deterministic Miller-Rabin for n below 3.3 x 10^24 (the bases to 41)."""
    if n < 2:
        return False
    small = (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41)
    for p in small:
        if n % p == 0:
            return n == p
    d, s = n - 1, 0
    while d % 2 == 0:
        d //= 2
        s += 1
    for a in small:
        x = pow(a, d, n)
        if x in (1, n - 1):
            continue
        for _ in range(s - 1):
            x = x * x % n
            if x == n - 1:
                break
        else:
            return False
    return True


def den_40_bits() -> int:
    """The least prime 1 mod 4 above 2^40."""
    n = 2**40 + 1
    while not (n % 4 == 1 and is_prime(n)):
        n += 1
    return n


def volume_at(level: int) -> int:
    return int(np.asarray(volume.volume_of(GAMMA, np.array([level], dtype=object)), dtype=object).reshape(-1)[0])


def level_at(x: int) -> int:
    return int(np.asarray(volume.level_of(GAMMA, np.array([x], dtype=object)), dtype=object).reshape(-1)[0])


def reading(den: int, unit: int) -> dict:
    w = wall_of(den, GAMMA, unit)
    x_record = volume_at(LEVEL_RECORD)
    p_0 = int(paces.clock(GAMMA, LEVEL_RECORD))
    x_max = int(division_forward(SIGNED - 1, w, 0)[0])  # the largest X with w X < 2^127 (the state's remainder)
    top = volume.clock_zero(GAMMA)  # the clock's last pace: the level reading rests there
    level_max = level_at(min(x_max, volume_at(top - 1))) if x_max >= GAMMA else None
    found = {
        "den": den,
        "den_bits": den.bit_length(),
        "G": unit,
        "w": w,
        "w_bits": w.bit_length(),
        "X_at_U_2_5": x_record,
        "p_0_at_U_2_5": p_0,
        "e_U_scaled_at_level_2500": int(division_forward(GAMMA * SCALE, p_0, 0)[0]),
        "wX_bits_at_U_2_5": (w * x_record).bit_length(),
        "state_within_128_at_U_2_5": (w * x_record) < SIGNED,
        "X_max_state": x_max,
        "level_max_state": level_max,
        "e_U_max_state_scaled": (
            int(division_forward(GAMMA * SCALE, int(paces.clock(GAMMA, level_max)), 0)[0])
            if level_max is not None and int(paces.clock(GAMMA, level_max)) > 0
            else None
        ),
        "level_reading_rests_at": top,
        "transients": [],
    }
    for amplitude in AMPLITUDES:
        room = w * (5 * amplitude + 1)
        x_t = int(division_forward(SIGNED - 1, room, 0)[0])
        level_t = level_at(min(x_t, volume_at(top - 1))) if x_t >= GAMMA else None
        found["transients"].append(
            {
                "A": amplitude,
                "numerator_bits_at_U_2_5": (x_record * room).bit_length(),
                "within_128_at_U_2_5": x_record * room < SIGNED,
                "X_max_transient": x_t,
                "level_max_transient": level_t,
                "e_U_max_transient_scaled": (
                    int(division_forward(GAMMA * SCALE, int(paces.clock(GAMMA, level_t)), 0)[0])
                    if level_t is not None and int(paces.clock(GAMMA, level_t)) > 0
                    else None
                ),
            }
        )
    return found


def main() -> None:
    dens = {
        "toy": 1021,
        "candidate_54_bits": 15162856759112389,
        "about_40_bits": den_40_bits(),
        "top_tier_22_digits": 1166991900949580266237,
    }
    rows = []
    for name, den in dens.items():
        for unit in (16, 1):
            row = {"name": name, **reading(den, unit)}
            rows.append(row)
            t = row["transients"]
            print(
                f"{name:22s} den bits {row['den_bits']:3d} G {unit:2d} w bits {row['w_bits']:3d} | X(U 2.5) {row['X_at_U_2_5']:12d} "
                f"wX bits {row['wX_bits_at_U_2_5']:3d} state within 128: {row['state_within_128_at_U_2_5']} | "
                f"X_max(state) {row['X_max_state']} level {row['level_max_state']} e^U x1e6 {row['e_U_max_state_scaled']} | "
                f"transient A 4096: bits {t[0]['numerator_bits_at_U_2_5']} within {t[0]['within_128_at_U_2_5']} "
                f"X_max {t[0]['X_max_transient']} level {t[0]['level_max_transient']} e^U x1e6 {t[0]['e_U_max_transient_scaled']} | "
                f"A loader: bits {t[1]['numerator_bits_at_U_2_5']} within {t[1]['within_128_at_U_2_5']} level {t[1]['level_max_transient']}"
            )
    (HERE.parent / "width.json").write_text(json.dumps(rows, indent=1, default=str), encoding="utf-8")
    print("written", HERE.parent / "width.json")


if __name__ == "__main__":
    main()
