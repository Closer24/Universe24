"""The Lorentz form on the sign holder's four lines (the universe file's key `form`: `lorentz` on the holder of the sign under the rotation, `loader/universe.form_of`; ALGEBRA.md #the-hypotheses-under-their-own-names, The odd line's source is the sign's own current, the covector form declared on 2026-10-21): the time line and the three odd lines booked as one covector over one massless line, the odd line of the axis a owned by the Node at the -a end of its Link as the phase lines are (the +a Link of i), sourced by that Link's own flux of its record's step in the Link unit over the wall 2 den_s G^2 E_s T (`link_fluxes`, `loader/derived.held_write_of`) and read by that Link alone with the hop's sign of Peierls' p - q A (`FamilyRule.link_read` (-2, 0), `plane.link_levels`), so that the lattice Lorenz constraint 3 (L_0(t) - L_0(t - 1)) + SUM_a (L_a(i) - L_a(i - a)) = 0 (c^2 = 1 / 3, the massless line's R / w) is propagated by the law's exact continuity identity of the record's step (`residual`, the loader's gate at the lay, `gate`), and the time line's energy entering every reading of the holder's record with the negative sign, the covector's form SUM_a (odd line a) - 3 (time line) in thirds of the time line's unit (`weights`, `lines_total`; `readings.currents_of`, `share.family_share`, `credit.record_unit`); every function a reading of arrays, no state of its own, and nothing of it at the Node, which steps and divides every line alike."""

from __future__ import annotations

from collections.abc import Sequence
from typing import TYPE_CHECKING, Any

import numpy as np

from event_universe.core.ports import AXES, Wrap, arrival
from event_universe.core.rule3 import division_forward
from event_universe.loader.derived import FamilyRule
from event_universe.records import Record

if TYPE_CHECKING:
    from event_universe.lattice import Lattice

THIRDS = 3  # the covector's unit in the time line's: the odd lines enter the form at c^2 = 1 / 3 against the time line's 1, so the form L_0^2 - (1 / 3) SUM_a L_a^2 is read in thirds, 3 L_0^2 - SUM_a L_a^2
TIME_WEIGHT = -THIRDS  # the time line's entry, negative: the scalar and the longitudinal wave of a conserved source carry opposite energies and cancel, the two transverse lines carry Larmor's (the remedy)
Pairs = tuple[
    tuple[Any, ...], tuple[Any, ...]
]  # each Link's pair (R^c, R^s) in Port order, `plane.link_pairs`


def weights(family: FamilyRule) -> tuple[int, ...] | None:
    """The weight of each line of a holder's record in a reading of it under the Lorentz form, (-3, 1, 1, 1) over the time line and the three odd lines: the covector's form in thirds of the time line's unit, the time line's energy negative; None for every other family, every line at 1 (`readings.currents_of`, `share.family_share`)."""
    return (TIME_WEIGHT, 1, 1, 1) if family.lorentz else None


def lines_total(family: FamilyRule, lines: Sequence[Record]) -> list[Record]:
    """A holder's record under the Lorentz form as the board reads it whole: its four lines each summed over its rows at every Node, both levels (the time line as `records.rows_total` sums it, then the three odd lines alike; the light's record the free row 0 among them, ALGEBRA.md, No record reads its own write of the sign), the remainder the free row's; the row's own lines where it has one row, bit for bit."""
    found = []
    for line in range(family.width):
        rows = [lines[row * family.width + line] for row in range(family.records)]
        if len(rows) == 1:
            found.append(rows[0])
            continue
        now: Any = sum(row.now for row in rows)
        before: Any = sum(row.before for row in rows)
        found.append(Record(np.asarray(now), np.asarray(before), rows[0].remainder))
    return found


def link_fluxes(
    lines: Sequence[Record], pairs: Pairs, square: Any, wrap: Wrap
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """The flux of a two-part record's step through each of the Node's three +a Links in the Link unit, Phi_a(i) = Im(conj(z_i) (X^c_ij + i X^s_ij) z_(i+a)) = re_i (X^s re_j + X^c im_j) - im_i (X^c re_j - X^s im_j), every plane's added, read from the levels now at the interval's start and the Link's pair (X^c, X^s) the step reads through the +a Port (`flux.pairs_of`, which gives p_i^2 (X^c, X^s); `square` the p_i^2 of the record's read, divided out exactly), one Link's reach: the flux of the law's exact continuity identity of the record's own step, w (W_i(t) - W_i(t + 1)) = p_i^2 SUM_a (Phi_a(i) - Phi_a(i - a)) + Im(conj(z_i) (r - r')) at every Node bit for bit (multiply Rule3's step by the conjugate of the record and take the imaginary part; ALGEBRA.md, The odd line's source is the sign's own current, the identity with the Link's pair in the temporal gauge and the remainders' term as the tension's identity carries it), antisymmetric on the Link by direction since the far end reads the conjugate pair (X^c, -X^s) exactly (`plane.sign_pairs`, `features/phase.fold`); the source of the odd line a of the record's own row under the Lorentz form (`records.write_sources`, over the wall 2 den_s G^2 E_s T), where the plain current J_a / 2 of the two Links' mean was the source without it (`readings.sense_current_of`)."""
    evens, odds = pairs
    found: list[Any] = [0, 0, 0]
    for re_line, im_line in zip(lines[0::2], lines[1::2], strict=True):
        for axis in range(AXES):
            port = 2 * axis  # the +a Port, the Link the Node owns
            cosine = division_forward(evens[port], square, 0)[0]  # exact: the pair times p_i^2
            sine = division_forward(odds[port], square, 0)[0]
            re_j, im_j = arrival(re_line.now, axis, 1, wrap), arrival(im_line.now, axis, 1, wrap)
            found[axis] = (
                found[axis]
                + re_line.now * (sine * re_j + cosine * im_j)
                - im_line.now * (cosine * re_j - sine * im_j)
            )
    return np.asarray(found[0]), np.asarray(found[1]), np.asarray(found[2])


def residual(family: FamilyRule, lines: Sequence[Record], wrap: Wrap) -> list[np.ndarray]:
    """The lattice Lorenz constraint of each row of a holder under the Lorentz form at every Node, a reading: C = 3 (L_0(now) - L_0(before)) + SUM_a (L_a(i) - L_a(i - a)) at the levels the row holds, the time line's change per interval at the holder's c^2 = R / w = 1 / 3 plus the odd lines' divergence over the six Links, the +a Link's own line at i less the -a Link's at i - a (one Link's reach); 0 at the start (the rests static, the odd lines at 0) and kept within the roundings of the lines' steps and writes by the exact continuity identity of the sources (`link_fluxes`: with every row stepped by the one massless line, C obeys the same recurrence with the source 3 (s_0(t) - s_0(t - 1)) + SUM_a (s_a(i) - s_a(i - a)), the identity's remainders' term over Gamma^2)."""
    found = []
    for row in range(family.records):
        time = lines[row * family.width]
        total: Any = THIRDS * (time.now - time.before)
        for axis in range(AXES):
            odd = lines[row * family.width + 1 + axis].now
            total = total + (odd - arrival(odd, axis, -1, wrap))
        found.append(np.asarray(total))
    return found


def gate(board: Lattice) -> None:
    """The loader's gate at the lay, once: every row of every holder under the Lorentz form holds the lattice Lorenz constraint at every Node as laid (`residual` 0 everywhere: the rests static, the odd lines at 0, a packet laid with no divergence), refused by name otherwise with the holder, the row, the Node and the residual; the holder's form is indefinite off the constraint, so a light packet laid on the time line alone, which the form books at a negative energy, is refused."""
    for index in board.held:
        family = board.families[index]
        if not family.lorentz:
            continue
        for row, found in enumerate(residual(family, board.states[index].lines, board.wrap)):
            if found.any():
                at = np.unravel_index(int(np.abs(found).argmax()), found.shape)
                raise ValueError(
                    f"the lay breaks the lattice Lorenz constraint of {family.name!r} (held.form 'lorentz') on "
                    f"its row {row} at the Node {tuple(int(i) for i in at)}: 3 (L_0(now) - L_0(before)) + SUM_a "
                    f"(L_a(i) - L_a(i - a)) = {int(found[at])}, and the four lines booked as one covector keep it "
                    "0; a packet laid on the time line alone is refused: lay light on the odd lines with no "
                    "divergence (transverse), or lay its time line with 3 (L_0(now) - L_0(before)) = -SUM_a "
                    "(L_a(i) - L_a(i - a)) at every Node"
                )
