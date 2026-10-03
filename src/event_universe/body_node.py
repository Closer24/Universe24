"""The one-Node detector on a bound body, the exact solve on the reference sequences (ALGEBRA.md, The emitter/detector is one declaration kind for every experiment, line 1; the mathematician's 235, #1572 comment 5966769056, with the advisor's second, 5966780505, two hands): at one Node x_0 of a body of levels g and e the record is c_g phi_g(x_0) cos(omega_g t + alpha) + c_e phi_e(x_0) cos(omega_e t + beta), two rotations in time, and the detector reads the level sequence z_t at its Node over its window and solves exactly for the four quadrature amplitudes of the reference sequences R cos(omega_g t), R sin(omega_g t), R cos(omega_e t), R sin(omega_e t) through their Gram matrix by Cramer's rule, every determinant an integer of Python's (the Gram determinants of the order (R^2 W)^4, beyond the width and exact), no root before the squares and no float; the two separate projections of the resonant act would leave the other level's cross term at 1 / (W delta), phase-dependent, where the solve is exact in exact arithmetic for W at or above 4 and within the rounding's amplification once W is of the order of 2 pi / (omega_e - omega_g). The share of a level is Q_n = (a_n^2 + b_n^2) w sin^2(omega_n) / phi_n(x_0)^2 with phi_n(x_0)^2 / (phi_n . phi_n) the level's declared weight at the Node, and p_n = Q_n / Q(z) its probability, the common factors cancelling: the draw's weights are the Q_n brought to one denominator in integers (`shares`). The window resolves the beat when the beat's sine, R^2 sin((omega_e - omega_g) t) = r'_e r_g - r_e r'_g over the window, has crossed 0 twice, the beat phase at or past 2 pi (`resolves_the_beat`, the loader's refusal "the window does not resolve the beat"); a level whose weight at the Node is 0 is unreadable there (the loader's refusal "the Node is a node of a read mode"). The reference sequences advance by the giving's recurrence at the scale R derived from the width alone (`scale_of_the_width`: the largest power of two whose square is inside the width's largest integer, so that one product of two references fits the width and the sums and the determinants stand exact in Python's integers beyond it, the hands' word); the engine holds no number and no name, every pair and weight the file's."""

from __future__ import annotations

from event_universe.core.rule3 import division_fixed_point, division_forward
from event_universe.giving import advanced

Pair = tuple[int, int]  # a rotation as the file declares it, cos omega = num / den
Sequences = list[list[int]]  # per level its cosine then its sine reference sequence over the window


def scale_of_the_width(room: int) -> int:
    """The reference sequences' scale R, derived from the width and never declared: the largest power of two whose square is at or below `room`, the width's largest integer (2^31 at the width 63), so that a product of two references fits the width while the window's sums and the Gram determinants, of the order (R^2 W)^4, stand exact in Python's integers beyond it (the advisor's word on 235, #1572 comment 5966780505)."""
    scale = 1
    while (2 * scale) * (2 * scale) <= room:
        scale *= 2
    return scale


def references_over(scale: int, pairs: tuple[Pair, ...], length: int) -> Sequences:
    """Per level its two reference sequences of `length` values from t = 0 at the scale R, r_t = R cos(omega_n t) begun at (R, R num div den) and r'_t = R sin(omega_n t) begun at (0, -isqrt(R^2 (den^2 - num^2)) div den), the one root at the declaration, each advanced by the giving's recurrence (`giving.advanced`), as the resonant act's references are."""
    found = []
    for num, den in pairs:
        cosine = int(division_forward(scale * num, den, division_forward(den, 2, 0)[0])[0])
        square = scale * scale * (den * den - num * num)
        sine = int(division_forward(division_fixed_point(square), den, 0)[0])
        for record in ((scale, cosine), (0, -sine)):
            sequence = []
            for _ in range(length):
                sequence.append(record[0])
                record = advanced(record[0], record[1], (num, den))
            found.append(sequence)
    return found


def resolves_the_beat(lower: Sequences, upper: Sequences) -> bool:
    """Whether a window resolves the beat of two levels (the uncertainty rule's form in time, a beat at one Node): the beat's sine R^2 sin((omega_e - omega_g) t) = r'_e r_g - r_e r'_g formed from the two levels' reference sequences over the window, resolved where it has crossed 0 twice, the beat phase at or past 2 pi within the window."""
    beat = [
        e_sine * g_cosine - e_cosine * g_sine
        for g_cosine, g_sine, e_cosine, e_sine in zip(
            lower[0], lower[1], upper[0], upper[1], strict=True
        )
    ]
    crossings, previous = 0, 0
    for value in beat[1:]:
        if (previous > 0 and value <= 0) or (previous < 0 and value >= 0):
            crossings += 1
        previous = value
    return crossings >= 2


def gram_of(references: Sequences) -> list[list[int]]:
    """The Gram matrix of the reference sequences, G_ij = SUM_t r_i(t) r_j(t), integers."""
    return [
        [sum(a * b for a, b in zip(row, column, strict=True)) for column in references]
        for row in references
    ]


def sums_of(references: Sequences, levels: list[int]) -> list[int]:
    """The four sums of the record's level sequence with the references, s_i = SUM_t z_t r_i(t)."""
    return [sum(r * z for r, z in zip(row, levels, strict=True)) for row in references]


def determinant(matrix: list[list[int]]) -> int:
    """The determinant of an integer matrix by the fraction-free elimination (Bareiss), every intermediate an integer and every division exact, the division act's quotient; a row swap turns the sign; 0 where no pivot stands."""
    rows = [list(row) for row in matrix]
    size, sign, previous = len(rows), 1, 1
    for k in range(size - 1):
        if rows[k][k] == 0:
            swap = next((i for i in range(k + 1, size) if rows[i][k] != 0), None)
            if swap is None:
                return 0
            rows[k], rows[swap], sign = rows[swap], rows[k], -sign
        for i in range(k + 1, size):
            for j in range(k + 1, size):
                numerator = rows[i][j] * rows[k][k] - rows[i][k] * rows[k][j]
                rows[i][j] = int(division_forward(numerator, previous, 0)[0])
        previous = rows[k][k]
    return sign * rows[size - 1][size - 1]


def solved(references: Sequences, levels: list[int]) -> tuple[int, list[int]]:
    """Cramer's rule on the Gram matrix: the Gram determinant D and per reference the determinant D_i of the matrix with its column i replaced by the sums, so that the amplitude of the reference i is D_i / D exactly; D is 0 where the window is too short for the references to be independent (below 4 values for two levels)."""
    gram, sums = gram_of(references), sums_of(references, levels)
    found = []
    for i in range(len(references)):
        replaced = [
            [sums[r] if c == i else gram[r][c] for c in range(len(references))]
            for r in range(len(references))
        ]
        found.append(determinant(replaced))
    return determinant(gram), found


def shares(solution: list[int], pairs: tuple[Pair, ...], weights: tuple[Pair, ...]) -> list[int]:
    """The levels' shares as the draw's integer weights, per level Q_n = (D_cos^2 + D_sin^2) sin^2(omega_n) / weight_n up to the factors common to every level (D^2, w, the family's own), with sin^2(omega_n) = (den_n^2 - num_n^2) / den_n^2 and the weight phi_n(x_0)^2 / (phi_n . phi_n) = [w_num, w_den]: every level's share multiplied by the other levels' den_m^2 w_num_m, so the ratios are exact and p_n = Q_n / SUM Q."""
    found = []
    for n, ((num, den), (_w_num, w_den)) in enumerate(zip(pairs, weights, strict=True)):
        own = (solution[2 * n] ** 2 + solution[2 * n + 1] ** 2) * (den * den - num * num) * w_den
        for m, ((_num_m, den_m), (w_num_m, _w_den_m)) in enumerate(zip(pairs, weights, strict=True)):
            if m != n:
                own *= den_m * den_m * w_num_m
        found.append(own)
    return found
