"""The map of atom-level-v1 (docs/designs/atom_levels/LEVELS.md): every
number of that file printed from the declared integers of the registered
world `examples/events/atoms/hydrogen_r12_centred.json` and from the
readings RUN_CENTRED.md made on it, each labelled with its kind. A host
computation: no engine import, no run. Run it from the repository root:

    python docs/designs/atom_levels/levels_map.py

Bohr's, Balmer's and Kepler's forms appear only as the thing compared
with (record 817 of docs/LOG_2026-09-20.md)."""

from __future__ import annotations

from fractions import Fraction
from math import floor

# The declared integers of the centred world (kind 1 and 2; the electron's
# momentum kind 3), read from the world file, not derived here.
N = 64  # the phase circle's steps
Q = 64  # the label's scale
S = 45120  # the width
M = 1836  # the electron's content
H = 5536242544  # the world's action, h = 16 p(8) under form B (PINS.md)
P4 = 293783192  # the electron's declared momentum at r = 12 (the rung j = 4)
T4 = 1462  # the registered period at r = 12 on main's drive (series H)
M_I = Q * S * M  # the inertial constant of the drive's limit (Theorem 4)

# The readings of RUN_CENTRED.md on the same world without the key.
RETURNS = [1341, 2772, 4272, 5422, 6462]  # DETECTOR: the +x returns' counts
PERIODS = [1431, 1500, 1150, 1040]  # DETECTOR: the counts between them
CIRCLES = [4.125, 4.094, 3.750, 3.500]  # DETECTOR: the circles per return (C5)
# GAMEBOARD (a diagnostic): the momentum's length at the step lines nearest
# the +x crossings, in millions of label units, the birth's first.
MOMENTA_MILLION = [293.783192, 295.0, 342.9, 392.6, 398.1, 437.4]
PAIRS = [(3, 2), (4, 2), (5, 2), (2, 1)]  # (j, i): the released pairs


def wall(n_l: int, d_l: int) -> int:
    """The rule's wall W_l = floor(2 Q S M h d_l / (N n_l)), formed at load."""
    return (2 * M_I * H * d_l) // (N * n_l)


def level_steps(delta_e: Fraction, n_l: int, d_l: int) -> int:
    """The turn s = floor(N n_l Delta E / (h d_l)) of a released row."""
    return floor(Fraction(N * n_l) * delta_e / (H * d_l))


def main() -> None:
    p1 = 4 * P4
    e1 = Fraction(p1 * p1, 2 * M_I)
    print("[COMPUTATION] section 1: the ladder from the rung j = 4 (the declared integers)")
    print(f"  m_i = Q S M = {M_I}; p_1 = 4 p_4 = {p1}; E_1 = p_1^2 / (2 m_i) = {e1} = {float(e1):.2f}")
    print(
        f"  N E_1 / h = {float(Fraction(N) * e1 / H):.4f} steps (the whole spectrum at the dictionary)"
    )
    for j in range(1, 6):
        p_j = Fraction(p1, j)
        a_j = Fraction(12 * j * j, 16)
        t_j = Fraction(T4 * j**3, 64)
        e_j = e1 / (j * j)
        print(
            f"  j = {j}: Delta A_j = j N h = {j * N * H}; p_j = {p_j} ({float(p_j):.1f}); "
            f"a_j = {a_j} ({float(a_j):.4f}) Links; T_j = {t_j} ({float(t_j):.2f}); "
            f"E_j = -{e_j} (-{float(e_j):.2f}); N E_j / h = {float(Fraction(N) * e_j / H):.4f} steps"
        )
    print("[COMPUTATION] section 3 (a), (b): the four pairs under both forms")
    for j, i in PAIRS:
        delta_e = e1 * (Fraction(1, i * i) - Fraction(1, j * j))
        s_1 = Fraction(N) * delta_e / H
        print(
            f"  ({j}, {i}): action form g = j - i = {j - i}, f = {Fraction(j - i, N)}; "
            f"momentum form Delta E = {delta_e} = {float(delta_e):.2f}; "
            f"s at [1, 1] = {floor(s_1)} ({float(s_1):.4f}); at [64, 1] = {level_steps(delta_e, 64, 1)} "
            f"({float(64 * s_1):.2f}); at [4096, 1] = {level_steps(delta_e, 4096, 1)}"
        )
    print(
        "  the action form: nu(4 to 2) / nu(3 to 2) = 2, nu(5 to 2) / nu(3 to 2) = 3, nu(2 to 1) / nu(3 to 2) = 1"
    )
    r42 = (Fraction(1, 4) - Fraction(1, 16)) / (Fraction(1, 4) - Fraction(1, 9))
    r52 = (Fraction(1, 4) - Fraction(1, 25)) / (Fraction(1, 4) - Fraction(1, 9))
    r21 = (1 - Fraction(1, 4)) / (Fraction(1, 4) - Fraction(1, 9))
    print(
        f"  the momentum form, exact in the limit: {r42} = {float(r42)}, {r52} = {float(r52):.3f}, {r21} = {float(r21)}"
    )
    print("  on the comparison side only: Balmer's 27 / 20 = 1.35 (NATURE row 6)")
    print("[COMPUTATION] section 3 (d): the grain")
    for n_l in (64, 4096):
        s32 = level_steps(e1 * (Fraction(1, 4) - Fraction(1, 9)), n_l, 1)
        s42 = level_steps(e1 * (Fraction(1, 4) - Fraction(1, 16)), n_l, 1)
        print(
            f"  at [{n_l}, 1]: s(3 to 2) = {s32}, s(4 to 2) = {s42}, the ratio {Fraction(s42, s32)} = {s42 / s32:.4f}, the band 1 / {s32}"
        )
    alpha = e1 * (Fraction(1, 4) - Fraction(1, 9))
    for steps in (1, 10, 100):
        need = Fraction(steps) * H / (Fraction(N) * alpha)
        print(f"  the pair n_l / d_l for s(3 to 2) >= {steps}: {float(need):.2f}")
    print("[COMPUTATION] section 2 (c): the walls")
    for n_l in (1, 64):
        w = wall(n_l, 1)
        print(f"  W_l at [{n_l}, 1] = {w} ({w:.3e}); below 2^60: {w < 2**60}")
    print(f"  3 x (2^30)^2 = {3 * (2**30) ** 2} < 2^62 = {2**62}: {3 * (2**30) ** 2 < 2**62}")
    print("[COMPUTATION from GAMEBOARD] section 5: the gives on the centred world's returns at [64, 1]")
    w = wall(64, 1)
    level = 0
    total = 0
    squares = [int(round(p * p * 10**12)) for p in MOMENTA_MILLION]
    for k in range(1, len(squares)):
        rate = squares[k] - squares[k - 1]
        level += rate
        s = level // w if level >= w else 0
        level -= s * w
        total += s
        print(
            f"  return {k} at {RETURNS[k - 1]}: rate {rate:.3e} ({rate / w:.3f} W_l at [64, 1], "
            f"{rate / wall(1, 1):.4f} at [1, 1]), give {s}, remainder {level / w:.2f} W_l"
        )
    print(
        f"  the sum of the gives {total}; the sum of the rates over W_l {sum(squares[k] - squares[k - 1] for k in range(1, len(squares))) / w:.2f}"
    )
    print(
        "[GAMEBOARD, a diagnostic] section 5 (i): the level at each return from the momentum, p . p / W_l at [64, 1]"
    )
    print("  " + ", ".join(f"{squares[k] / w:.2f}" for k in range(1, len(squares))))
    print("[COMPUTATION from DETECTOR] section 5 (i): the level from the virial form, N n_l j / (2 T)")
    print("  " + ", ".join(f"{N * 64 * j / (2 * t):.2f}" for j, t in zip(CIRCLES, PERIODS, strict=True)))
    print(
        "[COMPUTATION from DETECTOR] section 5 (ii): the ladder's gives from the read j alone at [64, 1]"
    )
    steps_e1 = float(Fraction(N * 64) * e1 / H)
    print(
        "  "
        + ", ".join(
            f"{steps_e1 * (1 / CIRCLES[k + 1] ** 2 - 1 / CIRCLES[k] ** 2):.2f}"
            for k in range(len(CIRCLES) - 1)
        )
    )
    print("[COMPUTATION from DETECTOR] section 5, L3: T_k / T_(k+1) against (j_k / j_(k+1))^3")
    for k in range(len(PERIODS) - 1):
        ratio_t = PERIODS[k] / PERIODS[k + 1]
        ratio_j = (CIRCLES[k] / CIRCLES[k + 1]) ** 3
        print(
            f"  returns {k + 1} to {k + 2}: T ratio {ratio_t:.3f}, (j / i)^3 {ratio_j:.3f}, off by {abs(ratio_t / ratio_j - 1) * 100:.1f} percent"
        )
    print("[COMPUTATION] section 6 (2): the rungs at whole Links by j = 4 sqrt(r / 12) (the shell mean)")
    print(
        "  "
        + ", ".join(f"r = {r}: {4 * (r / 12) ** 0.5:.2f}" for r in (2, 3, 4, 6, 7, 8, 12, 15, 16, 19))
    )


if __name__ == "__main__":
    main()
