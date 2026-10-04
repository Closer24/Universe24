"""The resonant read of a record declared a NodeReader at one Node, the two-quadrature form (ALGEBRA.md #what-is-open, item 50; The click writes on the lattice (b), the share at resonance; the mathematician's and the advisor's hands with their precisions, two hands): the taker keeps per transition two reference records at its declared resonance pair [num_d, den_d], r_t = R cos(Omega_d t) and r'_t = R sin(Omega_d t), advanced every interval by the one recurrence the giving's phasor uses (`giving.advanced`, Chebyshev's recurrence, one rounding half up), the sine record begun at (0, isqrt(R^2 (den_d^2 - num_d^2)) div den_d), one root at the declaration as the node_reader's wall's is; over the window the arriving level a_t at the Node is summed against both, X = SUM a_t r_t and Y' = SUM a_t r'_t, so that X^2 + Y'^2 = R^2 |SUM a_t e^(i Omega_d t)|^2, and at the window's close the turn of the labels is theta_W = k isqrt(X^2 + Y'^2) div R, the plane's size over the scale at the transition's declared weight k, applied at the window's close as W equal sub-turns with the carry (`sheared`, `meeting.turned_labels`), nothing reading the labels inside the window; the first-order change of the labels over a window is k |SUM a_t e^(i Omega_d t)|, A W / 2 at resonance at every arrival phase and A W sinc(delta W / 2) / 2 detuned by delta, the counter-rotating residue below 2 / W, where the magnitude form the engine ran before accumulated (2 / pi) k A W at every frequency and read no resonance. The scale R is derived from the file's amplitude bound, the record's window and the width and never declared; no s_d anywhere; the root once per window is the NodeReader's own act as the lay's root is and no act of Rule3, which takes none. The engine holds no number and no family name; the records stand in the books and at no Node."""

from __future__ import annotations

from dataclasses import dataclass

from event_universe.core.rule3 import division_fixed_point, division_forward
from event_universe.features import rotation
from event_universe.giving import advanced
from event_universe.loader.node_reader_declaration import Transition


@dataclass
class Reference:
    """A transition's two reference records at the taker's Node and its window's two sums: the transition's resonance pair (num, den), the scale R (`scale_of`), the cosine record (r_t, r_(t-1)) begun at (R, R num div den), so that r_t = R cos(Omega_d t), the sine record (r'_t, r'_(t-1)) begun at r'_0 = 0 and r'_1 = isqrt(R^2 (den^2 - num^2)) div den, the one root at the declaration, so that r'_t = R sin(Omega_d t), both advanced by `giving.advanced`, the window's two sums over the arriving level a_t at the Node, X = SUM a_t r_t and Y' = SUM a_t r'_t, and the arrival, the two sums as the close read them, held past their reset for the taking's lay (ALGEBRA.md, The two-mode line, row 16: the phase passes with the quantum); the books' and at no Node."""

    resonance: tuple[int, int]
    scale: int
    cosine: tuple[int, int]
    sine: tuple[int, int]
    in_phase: int
    quadrature: int
    arrival: tuple[int, int] = (0, 0)

    def closed(self) -> None:
        """The window's close: the two sums held as the arrival for this interval's taking lay and reset for the next window."""
        self.arrival, self.in_phase, self.quadrature = (self.in_phase, self.quadrature), 0, 0


def scale_of(room: int, bound: int, window: int) -> int:
    """The reference records' scale R, derived from the file's numbers and never declared (the mathematician's hand, the advisor's second): |X| and |Y'| stay at or below R A W with A the file's amplitude bound and W the record's window, so R is the largest power of two at which the plane's size squared X^2 + Y'^2, at most 2 (R A W)^2, stays inside the width's largest integer `room` (R A W below 2^31 at the width 63, at every pair, [1, 1299] included)."""
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


def arrival_of(
    transitions: tuple[Transition, ...], references: list[Reference], key: tuple[int, int, int | None]
) -> tuple[int, int] | None:
    """The arriving record's phase (X, Y') held at the close for the transition `key` names by (leaves, enters, drive), None where none matches, the giving's items among them (no drive)."""
    pairs = zip(transitions, references, strict=True)
    return next((r.arrival for t, r in pairs if (t.leaves, t.enters, t.drive) == key), None)


def turned_direction(re: int, im: int, x: int, y: int) -> tuple[int, int]:
    """A part's direction (re, im) turned by the angle of (x, y), the arriving record's phase at the Node atan2(Y', X) (ALGEBRA.md, The two-mode line, row 16: the entering part's direction is the leaving part's turned by the arrival's, the product's phase phi_part = phi_left + phi_L): (re x - im y, re y + im x) over isqrt(x^2 + y^2) by the division act, its floor; unturned where no arrival stands, the size 0."""
    size = division_fixed_point(x * x + y * y)
    if size == 0:
        return re, im
    return int(division_forward(re * x - im * y, size, 0)[0]), int(
        division_forward(re * y + im * x, size, 0)[0]
    )


def window_turn(reference: Reference, weight: int) -> int:
    """The window's turn in the labels' numerator, theta_W = k isqrt(X^2 + Y'^2) div R, the plane's size over the scale at the transition's declared weight k (the advisor's derivation: the first-order change of the labels over a window is k |SUM a_t e^(i Omega_d t)|, A W / 2 at resonance at every arrival phase and A W sinc(delta W / 2) / 2 detuned); the root once per window is the NodeReader's own act, as the lay's root is (`features/click.amplitude`), and no act of Rule3, which takes none (the advisor's precision (iii))."""
    size = division_fixed_point(reference.in_phase**2 + reference.quadrature**2)
    return int(division_forward(weight * size, reference.scale, 0)[0])


def sheared(u: int, v: int, turn: int, pieces: int, gamma: int) -> tuple[int, int]:
    """The window's turn applied as `pieces` equal sub-turns, the window's intervals (the advisor's second on the first build): the engine's turn is a tangent half-angle (features/rotation, tan(theta / 2) = the numerator over 2 Gamma), under which one shear of a whole window's sum compresses a large turn (2 arctan(9,408 / 12,000) = 1.330 against 1.568 at the Zeno world's n = 1), so each sub-turn's numerator is (turn + carry) div pieces with the remainder carried across the shears (the carried division, the write's own act), the sub-turns summing to the turn exactly and the angles adding as the proper intervals' did (48 x 2 arctan(9,408 / (12,000 x 48)) = 1.5680 at n = 1); the labels untouched inside the window, the resonance read by the plane's size, the root once per window."""
    carry = 0
    for _ in range(pieces):
        piece, carry = division_forward(turn, pieces, carry)
        u, v = rotation.turned(u, v, int(piece), 2 * gamma)
    return int(u), int(v)
