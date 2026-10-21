"""B. The non-absorbing which-way marker and the quantum eraser in the law's algebra (README.md, section
B), on the shipped two slits' world by the law's real line (fields.py): the two paths' waves psi_L and
psi_U (the lower gap alone open, the upper gap alone open), the marker two local rotations of a two-part
record's parts at the two gaps by the half angles +theta/2 and -theta/2 (the act the engine lacks), the
screen's share per region the parts' currents summed (the bolometer, the parts never summed at a Node),
the marker side's ports by the one form, the eraser's conditional rows J(region | port), and the Gram
theorem checked in exact integers with the engine's own meeting_back.gram_of and
meeting_back.side_weights on integer moments. Englert's V^2 + D^2 = 1 exact in the rationals at the
Pythagorean half angle (2, 1).

    PYTHONPATH=src python papers/one_rule/variants/scripts/b_marker.py
"""

from __future__ import annotations

import json
import sys
from fractions import Fraction
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import fields  # noqa: E402

from event_universe import meeting_back  # noqa: E402
from event_universe.loader.draw import ports_of  # noqa: E402

OUT = HERE.parent / "out"
IDENTITY = ((1, 0), (0, 1))


def region_rows(board, line, a, b, window):  # type: ignore[no-untyped-def]
    """Per screen region the window sums of F[a], F[b] and the symmetrised cross current F[a, b]."""
    own_a, own_b, cross = [], [], []
    for name in board.screen:
        own_a.append(fields.windowed(fields.region_inflow(board, line, a, name), window))
        own_b.append(fields.windowed(fields.region_inflow(board, line, b, name), window))
        cross.append(fields.windowed(fields.region_cross_inflow(board, line, a, b, name), window))
    return np.array(own_a), np.array(own_b), np.array(cross)


def visibility(row, central=6, minima=(4, 8)):  # type: ignore[no-untyped-def]
    """The visibility at the blind central maximum against the blind first minima (tools/click_counts)."""
    most, low = row[central] * len(minima), sum(row[m] for m in minima)
    return (most - low) / (most + low)


def integer_moments(lower, upper, region, window, scale=1000):  # type: ignore[no-untyped-def]
    """The two paths' region-summed levels per interval and member as integers (the real line's levels
    scaled by `scale` and rounded), their second moments M_kl as a side books them."""
    xs = np.array([x for x, _y in region])
    ys = np.array([y for _x, y in region])
    moments = [[0, 0], [0, 0]]
    sums = 0
    for t in range(window[0] - 1, min(window[1], lower.now.shape[0])):
        for member in (0, 1):
            a_l = (lower.now if member == 0 else lower.before)[t][xs, ys].sum()
            a_u = (upper.now if member == 0 else upper.before)[t][xs, ys].sum()
            sigma = [int(round(scale * a_l)), int(round(scale * a_u))]
            for k in range(2):
                for m in range(2):
                    moments[k][m] += sigma[k] * sigma[m]
            sums += 1
    return moments, sums


def main() -> None:
    world, expected, board, line, wall = fields.loaded()
    window = (int(expected["window"][0]), int(expected["window"][1]))
    _w, _e, _b, _l, _wall, both, lower, upper = fields.three_fields()
    unit = wall  # W_c, the regions' unit in the blind
    f_both = (
        np.array(
            [fields.windowed(fields.region_inflow(board, line, both, n), window) for n in board.screen]
        )
        / unit
    )
    f_l, f_u, f_lu = (x / unit for x in region_rows(board, line, lower, upper, window))
    coherent = f_l + f_u + 2 * f_lu  # F[psi_L + psi_U], the one line through two gaps
    report: dict[str, object] = {}
    report["two_gaps_real_line"] = [round(v, 2) for v in f_both]
    report["lower_alone"] = [round(v, 2) for v in f_l]
    report["upper_alone"] = [round(v, 2) for v in f_u]
    report["cross_F[L,U]"] = [round(v, 2) for v in f_lu]
    report["sum_of_paths_coherent"] = [round(v, 2) for v in coherent]
    report["gap_coupling_two_gaps_minus_coherent_sum"] = [round(v, 2) for v in f_both - coherent]
    report["N_two_gaps"] = round(float(f_both.sum()), 2)
    report["N_coherent_sum"] = round(float(coherent.sum()), 2)
    report["N_incoherent_sum"] = round(float((f_l + f_u).sum()), 2)

    # the marker: two local rotations of the parts by the half angles +theta/2 at the lower gap and
    # -theta/2 at the upper gap; the parts H and V after the gaps: H = c (psi_L + psi_U), V = s (psi_L -
    # psi_U) with (c, s) the half angle's pair; the bolometer's row F[H] + F[V] = F[L] + F[U] + 2 cos theta
    # F[L, U] with cos theta = (c^2 - s^2) / (c^2 + s^2)
    rows = {}
    for label, cos_theta in (
        ("unmarked (theta 0)", Fraction(1)),
        ("half marked, half angle (2, 1): cos theta 3/5", Fraction(3, 5)),
        ("fully marked (theta 90): cos theta 0", Fraction(0)),
    ):
        row = f_l + f_u + 2 * float(cos_theta) * f_lu
        rows[label] = {
            "row": [round(v, 2) for v in row],
            "N": round(float(row.sum()), 2),
            "visibility_6_vs_4_8": round(visibility(row), 4),
            "visibility_of_the_cross_term": float(cos_theta),
        }
    report["marked_rows_bolometer"] = rows

    # Englert: the marker side (a side reading the record's two parts with the identity pattern) at the
    # basis (1, 1): the marker's states (c, s) for the lower path and (c, -s) for the upper, P(+ | L) =
    # (c + s)^2 / (2 (c^2 + s^2)), P(+ | U) = (c - s)^2 / (2 (c^2 + s^2)), D = |P(+|L) - P(+|U)| = 2 c s
    # / (c^2 + s^2) = sin theta; V = (c^2 - s^2) / (c^2 + s^2) = cos theta
    c, s = Fraction(2), Fraction(1)
    n2 = c * c + s * s
    plus, _minus = ports_of((1, 1), IDENTITY)  # e(+) = (1, 1), e(-) = (-1, 1)
    p_plus_l = Fraction((plus[0][0] * c + plus[1][0] * s) ** 2, 2 * n2)
    p_plus_u = Fraction((plus[0][0] * c + plus[1][0] * (-s)) ** 2, 2 * n2)
    distinguishability = abs(p_plus_l - p_plus_u)
    overlap = Fraction(c * c - s * s, n2)
    report["englert_exact"] = {
        "half_angle_pair": [2, 1],
        "marker_states_L_U": [[str(c), str(s)], [str(c), str(-s)]],
        "P(+|L)": str(p_plus_l),
        "P(+|U)": str(p_plus_u),
        "D": str(distinguishability),
        "V": str(overlap),
        "V^2+D^2": str(overlap * overlap + distinguishability * distinguishability),
    }

    # the eraser's two conditional rows in the form the law's J gives, F[psi_L + psi_U] (fringes) and
    # F[psi_L - psi_U] (anti-fringes), their sum twice the incoherent row
    fringes = f_l + f_u + 2 * f_lu
    anti = f_l + f_u - 2 * f_lu
    report["eraser_conditional_rows"] = {
        "port_plus_F[L+U]": [round(v, 2) for v in fringes],
        "port_minus_F[L-U]": [round(v, 2) for v in anti],
        "sum_over_ports": [round(v, 2) for v in fringes + anti],
        "twice_incoherent": [round(2 * v, 2) for v in f_l + f_u],
        "visibility_plus": round(visibility(fringes), 4),
        "visibility_minus": round(visibility(anti), 4),
        "visibility_sum": round(visibility(fringes + anti), 4),
    }

    # the Gram theorem in exact integers with the engine's helpers at the central region: the side weights
    # w(p) = SUM_kl c_k c_l G_kl M_kl (meeting_back.side_weights) for the eraser side at (1, 1) with no side
    # after it (the all-ones Gram) and for a side with the identity-pattern side after it (the identity
    # Gram): the marginal carries no cross term, the conditional does; exact integers
    moments, sums = integer_moments(lower, upper, board.regions[board.screen[6]], window)
    hermitian = [[(moments[k][m], 0) for m in range(2)] for k in range(2)]
    all_ones = meeting_back.gram_of([], 2)
    gram_identity = meeting_back.gram_of([IDENTITY], 2)
    eraser_ports = [list(p) for p in ports_of((1, 1), IDENTITY)]
    which_ports = [list(p) for p in ports_of((1, 0), IDENTITY)]
    last_eraser = meeting_back.side_weights(hermitian, eraser_ports, all_ones)
    last_which = meeting_back.side_weights(hermitian, which_ports, all_ones)
    first_any = meeting_back.side_weights(hermitian, eraser_ports, gram_identity)
    m11, m12, m22 = moments[0][0], moments[0][1], moments[1][1]
    report["gram_theorem_integers_central_region"] = {
        "intervals_and_members_summed": sums,
        "M": moments,
        "all_ones_gram": all_ones,
        "identity_pattern_gram": gram_identity,
        "last side at (1, 1): w(+), w(-) = M11 + M22 + 2 M12, M11 + M22 - 2 M12": last_eraser,
        "check": [m11 + m22 + 2 * m12, m11 + m22 - 2 * m12],
        "last side at (1, 0): w(+), w(-) = M11, M22": last_which,
        "a side with the identity-pattern side after it, at (1, 1): w(+), w(-) = M11 + M22 each": first_any,
        "the last side's two ports sum to twice the first side's one port": (
            sum(last_eraser) == 2 * (m11 + m22) == sum(first_any)
        ),
    }
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "b_marker.json").write_text(json.dumps(report, indent=1), encoding="utf-8")
    print(json.dumps(report, indent=1))


if __name__ == "__main__":
    main()
