"""THE ONE RULE'S INTEGERS AT A NODE (ALGEBRA.md 9.57 (1), the law's rule with
Einstein's weak field, the model owner's decision of record 2024 through the
Boss, "switch"; 9.50 (13) the first-order rule, HISTORY as the law and kept as
the field families' plain step and as the check-mode runs' control; BUILD.md
section 26 item 44): the three integers every step, wheel, form and load bound
read from, (R, S, w), so that the rule at a Node is

    w a_next + r' = R S_6(a_now) + S a_now - w a_before + r,  0 <= r' < w,

with the Node's own pace p = Gamma - c (the effective content c, the family of
clicks' level less the charge's read, 9.48 (3)). THE WEAK FIELD (9.57 (1)):
R = 2 p^2 num, S = 12 den Gamma^2 - 6 (p^2 + Gamma^2)(den - num) - 12 num p^2,
w = 6 den Gamma^2; at c = 0 the vacuum's rule term for term (S = 0, the
levels bit for bit, the remainders 2 Gamma^2 times the plain rule's). THE
PLAIN RULE (the field families' own step, pace 1, and the first-order control):
R = p num, S = 6 den c, w = 3 den Gamma. Integers or integer arrays alike; no
float, no root (the three tests of every rule, skills/workflow.md).
"""

from __future__ import annotations

from typing import overload

import numpy as np

Integers = int | np.ndarray


@overload
def rule_coefficients(
    num: int, den: int, gamma: int, content: int, weak_field: bool
) -> tuple[int, int, int]: ...


@overload
def rule_coefficients(
    num: np.ndarray, den: np.ndarray, gamma: int, content: np.ndarray | int, weak_field: bool
) -> tuple[np.ndarray, np.ndarray, np.ndarray]: ...


def rule_coefficients(num, den, gamma, content, weak_field):  # type: ignore[no-untyped-def]
    """(R, S, w): the coefficient on the six reads' sum, the coefficient on the
    Node's own level and the wall, of the weak-field rule (9.57 (1)) or of
    the plain rule (9.50 (13))."""
    pace = gamma - content
    if not weak_field:
        return pace * num, 6 * den * content, 3 * den * gamma
    squares = pace * pace
    gamma_squared = gamma * gamma
    read = 2 * squares * num
    self_coefficient = (
        12 * den * gamma_squared - 6 * (squares + gamma_squared) * (den - num) - 12 * num * squares
    )
    return read, self_coefficient, 6 * den * gamma_squared


@overload
def axis_rule_coefficients(
    num: int, den: int, gamma: int, content: int, axis_contents: tuple[int, ...]
) -> tuple[tuple[int, int, int], int, int]: ...


@overload
def axis_rule_coefficients(
    num: np.ndarray,
    den: np.ndarray,
    gamma: int,
    content: np.ndarray | int,
    axis_contents: tuple[np.ndarray, ...],
) -> tuple[tuple[np.ndarray, np.ndarray, np.ndarray], np.ndarray, np.ndarray]: ...


def axis_rule_coefficients(num, den, gamma, content, axis_contents):  # type: ignore[no-untyped-def]
    """THE FOUR PACES (ALGEBRA.md 9.91 (2); the one stroke, commit 3): p_0 = Gamma -
    c (c the reads' time components) and p_a = p_0 - t_a (t_a the reads' aa
    components halved, `axis_contents`), and the rule's integers with them:
    R_a = 2 p_a^2 num on the two reads along the axis a, S = 12 den Gamma^2 - 6
    (p_0^2 + Gamma^2)(den - num) - 4 num (p_x^2 + p_y^2 + p_z^2), w = 6 den
    Gamma^2. At p_a = p_0 the isotropic rule term for term (`rule_coefficients`
    with the weak field). Returns ((R_x, R_y, R_z), S, w); integers or integer
    arrays alike."""
    pace = gamma - content
    paces = [pace - axis_contents[axis] for axis in range(3)]
    gamma_squared = gamma * gamma
    reads = (2 * paces[0] * paces[0] * num, 2 * paces[1] * paces[1] * num, 2 * paces[2] * paces[2] * num)
    squares = paces[0] * paces[0] + paces[1] * paces[1] + paces[2] * paces[2]
    self_coefficient = (
        12 * den * gamma_squared - 6 * (pace * pace + gamma_squared) * (den - num) - 4 * num * squares
    )
    return reads, self_coefficient, 6 * den * gamma_squared


def rule_total_bound(
    num: int, den: int, gamma: int, content: int, amplitude: int, weak_field: bool
) -> int:
    """The largest total the rule can reach at a Node whose six reads and own
    two levels stand at the amplitude bound A, in size: 6 A R + A |S| + w (A +
    1); the load bound's reading (9.57 (2), 9.61 (3)), below 2^63 or the world
    is refused."""
    read, self_coefficient, wall = rule_coefficients(num, den, gamma, content, weak_field)
    return 6 * amplitude * abs(read) + amplitude * abs(self_coefficient) + wall * (amplitude + 1)
