"""The resonant read of a record declared an instrument at one Node, the two-quadrature form (ALGEBRA.md #what-is-open, item 50; The click writes on the GameBoard (b), the share at resonance; the mathematician's 223 (c) and 224 (2)(c), #1572 comments 5965727937 and 5966081562; the advisor's seconds, 5965918924 and 5966129376 with #1563 comment 5966129628, and the hands' precisions of the morning, #1572 comments 5966338551 and 5966387795; two hands): the taker keeps per transition two reference records at its declared resonance pair [num_d, den_d], r_t = R cos(Omega_d t) and r'_t = R sin(Omega_d t), advanced every interval by the one recurrence the giving's phasor uses (`giving.advanced`, Chebyshev's recurrence, one rounding half up), the sine record begun at (0, isqrt(R^2 (den_d^2 - num_d^2)) div den_d), one root at the declaration as the detector's wall's is; over the window the arriving level a_t at the Node is summed against both, X = SUM a_t r_t and Y' = SUM a_t r'_t, so that X^2 + Y'^2 = R^2 |SUM a_t e^(i Omega_d t)|^2, and at the window's close the turn of the labels is theta_W = k isqrt(X^2 + Y'^2) div R, the plane's size over the scale at the transition's declared weight k, applied once per window (`meeting.turned_labels`), nothing reading the labels inside the window; the first-order change of the labels over a window is k |SUM a_t e^(i Omega_d t)|, A W / 2 at resonance at every arrival phase and A W sinc(delta W / 2) / 2 detuned by delta, the counter-rotating residue below 2 / W, where the magnitude form the engine ran before accumulated (2 / pi) k A W at every frequency and read no resonance. The scale R is derived from the file's amplitude bound, the record's window and the width and never declared; no s_d anywhere; the root once per window is the instrument's own act as the lay's root is and no act of Rule3, which takes none. The engine holds no number and no family name; the records stand in the books and at no Node."""

from __future__ import annotations

from dataclasses import dataclass

from event_universe.core.rule3 import division_fixed_point, division_forward
from event_universe.giving import advanced
from event_universe.loader.instrument import Transition


@dataclass
class Reference:
    """A transition's two reference records at the taker's Node and its window's two sums: the transition's resonance pair (num, den), the scale R (`scale_of`), the cosine record (r_t, r_(t-1)) begun at (R, R num div den), so that r_t = R cos(Omega_d t), the sine record (r'_t, r'_(t-1)) begun at r'_0 = 0 and r'_1 = isqrt(R^2 (den^2 - num^2)) div den, the one root at the declaration, so that r'_t = R sin(Omega_d t), both advanced by `giving.advanced`, and the window's two sums over the arriving level a_t at the Node, X = SUM a_t r_t and Y' = SUM a_t r'_t; the books' and at no Node."""

    resonance: tuple[int, int]
    scale: int
    cosine: tuple[int, int]
    sine: tuple[int, int]
    in_phase: int
    quadrature: int


def scale_of(room: int, bound: int, window: int) -> int:
    """The reference records' scale R, derived from the file's numbers and never declared (the mathematician's 224 (2)(c), the advisor's second): |X| and |Y'| stay at or below R A W with A the file's amplitude bound and W the record's window, so R is the largest power of two at which the plane's size squared X^2 + Y'^2, at most 2 (R A W)^2, stays inside the width's largest integer `room` (R A W below 2^31 at the width 63, at every pair, [1, 1299] included)."""
    scale = 1
    while 2 * (2 * scale * bound * window) ** 2 <= room:
        scale *= 2
    return scale


def references_of(scale: int, transitions: tuple[Transition, ...]) -> list[Reference]:
    """One `Reference` per transition at the scale: the cosine record at (R, R num div den rounded half up, the giving's own start), the sine record at (0, -r'_1) with r'_1 = isqrt(R^2 (den^2 - num^2)) div den, the one root at the declaration, and the window's sums at 0."""
    found = []
    for transition in transitions:
        num, den = transition.resonance
        cosine = int(division_forward(scale * num, den, division_forward(den, 2, 0)[0])[0])
        square = scale * scale * (den * den - num * num)
        sine = int(division_forward(division_fixed_point(square), den, 0)[0])
        found.append(Reference(transition.resonance, scale, (scale, cosine), (0, -sine), 0, 0))
    return found


def gathered(
    references: list[Reference], transitions: tuple[Transition, ...], levels: dict[int, int]
) -> None:
    """One interval of the taker's read inside its window, a read and no write, no root and no draw: for every transition the arriving family's level a_t at the Node (`levels`, per drive family) times each reference record is added to the window's two sums, X += a_t r_t and Y' += a_t r'_t, and both records advance by the transition's resonance (`giving.advanced`); nothing reads the labels inside the window."""
    for transition, reference in zip(transitions, references, strict=True):
        level = levels[transition.drive]
        reference.in_phase += level * reference.cosine[0]
        reference.quadrature += level * reference.sine[0]
        reference.cosine = advanced(*reference.cosine, reference.resonance)
        reference.sine = advanced(*reference.sine, reference.resonance)


def window_turn(reference: Reference, weight: int) -> int:
    """The window's turn in the labels' numerator, theta_W = k isqrt(X^2 + Y'^2) div R, the plane's size over the scale at the transition's declared weight k (the advisor's derivation, #1572 comment 5966387795: the first-order change of the labels over a window is k |SUM a_t e^(i Omega_d t)|, A W / 2 at resonance at every arrival phase and A W sinc(delta W / 2) / 2 detuned); the root once per window is the instrument's own act, as the lay's root is (`features/click.amplitude`), and no act of Rule3, which takes none (the advisor's precision (iii), #1572 comment 5965918924)."""
    size = division_fixed_point(reference.in_phase**2 + reference.quadrature**2)
    return int(division_forward(weight * size, reference.scale, 0)[0])
