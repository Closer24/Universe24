"""The resonant read of a record declared a NodeDetector at one Node, the two-quadrature form (ALGEBRA.md #what-is-open, item 50; The click writes on the lattice (b), the share at resonance; the mathematician's and the advisor's hands with their precisions, two hands): the taker keeps per transition two reference records at its declared resonance pair [num_d, den_d], r_t = R cos(Omega_d t) and r'_t = R sin(Omega_d t), advanced every interval by the one recurrence the emission's phasor uses (`emission.advanced`, Chebyshev's recurrence, one rounding half up), the sine record begun at (0, (the largest x with x^2 <= R^2 (den_d^2 - num_d^2)) div den_d), one root at the declaration as the node_detector's wall's is; over the window the arriving level a_t at the Node is summed against both, X = SUM a_t r_t and Y' = SUM a_t r'_t, so that X^2 + Y'^2 = R^2 |SUM a_t e^(i Omega_d t)|^2, and at the window's close the turn of the labels is theta_W = k (the largest x with x^2 <= X^2 + Y'^2) div R, the plane's size over the scale at the transition's declared weight k, applied at the window's close as one hop of the labels by the phase line's pair at the window's angle, one carried division per label with the remainders kept in the books (`window_pair`, `hopped`, `meeting.turned_labels`; Part C, the local trial), nothing reading the labels inside the window; the first-order change of the labels over a window is k |SUM a_t e^(i Omega_d t)|, A W / 2 at resonance at every arrival phase and A W sinc(delta W / 2) / 2 detuned by delta, the counter-rotating residue below 2 / W, where the magnitude form the engine ran before accumulated (2 / pi) k A W at every frequency and read no resonance. The scale R is derived from the file's amplitude bound, the record's window and the width and never declared; no s_d anywhere; the root once per window is the NodeDetector's own act as the lay's root is and no act of Rule3, which takes none. The engine holds no number and no family name; the records stand in the books and at no Node."""

from __future__ import annotations

from dataclasses import dataclass

from event_universe.core.rule3 import division_forward, largest_below
from event_universe.emission import advanced
from event_universe.features import phase
from event_universe.loader.node_detector_declaration import Transition


@dataclass
class Reference:
    """A transition's two reference records at the taker's Node and its window's two sums: the transition's resonance pair (num, den), the scale R (`scale_of`), the cosine record (r_t, r_(t-1)) begun at (R, R num div den), so that r_t = R cos(Omega_d t), the sine record (r'_t, r'_(t-1)) begun at r'_0 = 0 and r'_1 = (the largest x with x^2 <= R^2 (den^2 - num^2)) div den, the one root at the declaration, so that r'_t = R sin(Omega_d t), both advanced by `emission.advanced`, the window's two sums over the arriving level a_t at the Node, X = SUM a_t r_t and Y' = SUM a_t r'_t, and the arrival, the two sums as the close read them, held past their reset for the absorption's lay (ALGEBRA.md, The two-mode line, row 16: the phase passes with the quantum); the books' and at no Node."""

    resonance: tuple[int, int]
    scale: int
    cosine: tuple[int, int]
    sine: tuple[int, int]
    in_phase: int
    quadrature: int
    arrival: tuple[int, int] = (0, 0)

    def closed(self) -> None:
        """The window's close: the two sums held as the arrival for this interval's absorption lay and reset for the next window."""
        self.arrival, self.in_phase, self.quadrature = (self.in_phase, self.quadrature), 0, 0


def scale_of(room: int, bound: int, window: int) -> int:
    """The reference records' scale R, derived from the file's numbers and never declared (the mathematician's hand, the advisor's second): |X| and |Y'| stay at or below R A W with A the file's amplitude bound and W the record's window, so R is the largest power of two at which the plane's size squared X^2 + Y'^2, at most 2 (R A W)^2, stays inside the width's largest integer `room` (R A W below 2^31 at the width 63, at every pair, [1, 1299] included)."""
    scale = 1
    while 2 * (2 * scale * bound * window) ** 2 <= room:
        scale *= 2
    return scale


def references_of(scale: int, transitions: tuple[Transition, ...]) -> list[Reference]:
    """One `Reference` per transition at the scale: the cosine record at (R, R num div den rounded half up, the emission's own start), the sine record at (0, -r'_1) with r'_1 = (the largest x with x^2 <= R^2 (den^2 - num^2)) div den, the one root at the declaration, and the window's sums at 0."""
    found = []
    for transition in transitions:
        num, den = transition.resonance
        cosine = int(division_forward(scale * num, den, division_forward(den, 2, 0)[0])[0])
        square = scale * scale * (den * den - num * num)
        sine = int(division_forward(largest_below(square), den, 0)[0])
        found.append(Reference(transition.resonance, scale, (scale, cosine), (0, -sine), 0, 0))
    return found


def gathered(
    references: list[Reference], transitions: tuple[Transition, ...], levels: dict[int, int]
) -> None:
    """One interval of the taker's read inside its window, a read and no write, no root and no draw: for every transition the arriving family's level a_t at the Node (`levels`, per drive family) times each reference record is added to the window's two sums, X += a_t r_t and Y' += a_t r'_t, and both records advance by the transition's resonance (`emission.advanced`); nothing reads the labels inside the window."""
    for transition, reference in zip(transitions, references, strict=True):
        level = levels[transition.drive]
        reference.in_phase += level * reference.cosine[0]
        reference.quadrature += level * reference.sine[0]
        reference.cosine = advanced(*reference.cosine, reference.resonance)
        reference.sine = advanced(*reference.sine, reference.resonance)


def arrival_of(
    transitions: tuple[Transition, ...], references: list[Reference], key: tuple[int, int, int | None]
) -> tuple[int, int] | None:
    """The arriving record's phase (X, Y') held at the close for the transition `key` names by (leaves, enters, drive), None where none matches, the emission's items among them (no drive)."""
    pairs = zip(transitions, references, strict=True)
    return next((r.arrival for t, r in pairs if (t.leaves, t.enters, t.drive) == key), None)


def turned_direction(re: int, im: int, x: int, y: int) -> tuple[int, int]:
    """A part's direction (re, im) turned by the angle of (x, y), the arriving record's phase at the Node atan2(Y', X) (ALGEBRA.md, The two-mode line, row 16: the entering part's direction is the leaving part's turned by the arrival's, the product's phase phi_part = phi_left + phi_L): (re x - im y, re y + im x) over (the largest x with x^2 <= x^2 + y^2) by the division act, its floor; unturned where no arrival stands, the size 0."""
    size = largest_below(x * x + y * y)
    if size == 0:
        return re, im
    return int(division_forward(re * x - im * y, size, 0)[0]), int(
        division_forward(re * y + im * x, size, 0)[0]
    )


def window_turn(reference: Reference, weight: int) -> int:
    """The window's turn in the labels' numerator, theta_W = k (the largest x with x^2 <= X^2 + Y'^2) div R, the plane's size over the scale at the transition's declared weight k (the advisor's derivation: the first-order change of the labels over a window is k |SUM a_t e^(i Omega_d t)|, A W / 2 at resonance at every arrival phase and A W sinc(delta W / 2) / 2 detuned); the root once per window is the NodeDetector's own act, as the lay's root is (`features/click.amplitude`), and no act of Rule3, which takes none (the advisor's precision (iii))."""
    size = largest_below(reference.in_phase**2 + reference.quadrature**2)
    return int(division_forward(weight * size, reference.scale, 0)[0])


PAIRS: dict[
    tuple[int, int], dict[int, phase.Pair]
] = {}  # the phase pairs read this run per (Gamma, X), by angle


def clear_memo() -> None:
    """The memo cleared at a run's start (`Lattice.__init__`, with `paces.clear_memo`): the phase pairs at the windows' angles are computed again within the run from the seed and nothing is kept between runs."""
    PAIRS.clear()


def window_pair(turn: int, gamma: int, amplitude: int) -> tuple[int, int, int]:
    """The hop pair (C, S) at the window's angle theta_W = turn x theta_0, theta_0 = 1 / Gamma the phase line's fixed angle (features/phase; the mathematician's and the advisor's word on the first build: the labels are Python integers in the books, no width cost, so the turn is the hop and no shear): the phase line seeded at the amplitude X the width derives (`Lattice.amplitude` by `phase.amplitude`, here `amplitude`; `phase.seed`, a multiple of Gamma) and iterated `turn` acts from the seed in the turn's sign (`phase.iterate`), read as the hop's two integers (C, S) = (X cos theta_W, X sin theta_W) to the walk's bound (`phase.read`, within 1.42 |turn| + 2.3 Gamma levels of X in magnitude); the integer `turn` is theta_W in units of theta_0, resonance's own integers by one division act (`window_turn`, the plane's size over the scale at the declared weight k), the angle 48 x 2 arctan(9,408 / (12,000 x 48)) = 1.5680 of the first build's sub-turns now 9,408 / 6,000 = 1.5680 exactly to the angle's rounding, where the one shear of a whole window compressed it to 1.330. Returns (C, S, X), X the pair's magnitude and the hop's wall. The pairs read within a run are kept by angle (`PAIRS`, cleared at the run's start by `clear_memo`) and a new angle's pair is iterated from the nearest one kept, bit for bit the pair iterated from the seed, since the acts compose exactly forward and inverse: the cost per window the difference of the angles and not theta_W / theta_0 acts."""
    found = PAIRS.setdefault((gamma, amplitude), {0: phase.seed(amplitude, gamma)})
    nearest = min(found, key=lambda angle: abs(angle - turn))  # the memo: the acts compose exactly
    pair = found.setdefault(turn, phase.iterate(found[nearest], turn - nearest, gamma))
    cosine, sine = phase.read(pair)
    return int(cosine), int(sine), amplitude


def hopped(
    u: int,
    v: int,
    cosine: int,
    sine: int,
    amplitude: int,
    carried: tuple[int, int] = (0, 0),
    direction: int = 1,
) -> tuple[int, int, int, int]:
    """The labels (u, v) hopped by the pair (C, S) at the magnitude X with one carried division per label (ALGEBRA.md #the-four-acts, the division act, kind R, a carried division on levels): (u', v') = ((C u - S v + r_u) div X, (S u + C v + r_v) div X), the remainders r_u, r_v in [0, X) kept in the books between turns (`NodeBooks.carried`), so that each label's floor is carried to the next window and not lost; counterclockwise for a positive angle, as the three shears turned. Direction -1 hops by the conjugate pair (C, -S), the angle's opposite, with the same carried division: the back-turn to the labels' floor and not bit for bit (the two labels are divided by X, not multiplied, so the remainders before the hop are not recoverable from the remainders after it; tests/test_part_c2_window.py states the reading). Returns (u', v', r_u', r_v')."""
    if direction not in (1, -1):
        raise ValueError(f"the hop's direction is 1 or -1, not {direction}")
    sine = direction * sine
    real, carried_real = division_forward(cosine * u - sine * v, amplitude, carried[0])
    imaginary, carried_imaginary = division_forward(sine * u + cosine * v, amplitude, carried[1])
    return int(real), int(imaginary), int(carried_real), int(carried_imaginary)
