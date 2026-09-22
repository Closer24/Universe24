"""The kick map of the atom's loop at r = 12, by algebra: the Atom
Algebraist's body step (ALGEBRA.md section 3 (b): the per-axis count
`k = 1 + Q S M / abs(p_a)`, the two-valued gaps) driven by the shell mean
of the proton's push, steady or pulsed (CAUSE.md section 2 (v), the
chief physicist's candidate of record 937). No engine import, nothing
run on the engine: a host computation from the declared integers and the
algebra's shell mean (the fan's grain absent by construction), GAMEBOARD
by formula. Run: `python docs/designs/atom_give/cause_kicks.py`.

The step: the electron's centre Node moves by the law's count primitive
per axis (`by_drive`'s form: an accumulator gains the signed momentum
component every interval, a step fires when it reaches the wall
`Q S M + abs(p_a)`, the remainder stays), with `main`'s per-axis drive
(a coincident fire on a later axis is lost: only the first axis that
fires steps, the later count is consumed) or without the loss. The push:
the shell mean `E(r) = E_12 (12 / r)^k` entries per shell at the Node's
radius, each entry one label of size Q times the charge product 16 times
the content M, toward the proton's Node; STEADY: one tenth of a shell
every interval; PULSED: one whole shell every 10 intervals (the release
pair [1, 18360] of a content of 1836). A flow factor divides the push
(flow-link-v1's plane factor 1.2871). The proton at the origin, the
board's half-width 26: the loop leaves when a coordinate passes it.
"""

from __future__ import annotations

import math
from dataclasses import dataclass

Q = 64
S = 45120
M = 1836
QSM = Q * S * M
E_12 = 6.588
CHARGE_PRODUCT = 16
HALF_WIDTH = 26


@dataclass
class Case:
    name: str
    p0: int
    pulsed: bool
    lost_fires: bool
    exponent: float
    flow_factor: float = 1.0
    ticks: int = 7500
    at_fraction: bool = (
        False  # the control: the push read at the accumulated position, Node plus acc / wall
    )
    centred: bool = False  # the candidate cure: the accumulator starts at half the wall (the Node the nearest to the accumulated motion)


def run(case: Case) -> str:
    x, y = 12, 0
    px, py = 0, case.p0
    acc = [0, 0]
    period = 10 if case.pulsed else 1
    crossings: list[tuple[int, float, float, float]] = []
    last_angle = 0.0
    quarter = 0
    escape = None
    for t in range(1, case.ticks + 1):
        # the push at the Node's radius, toward the origin
        if t % period == 0:
            if case.at_fraction:
                fx = x + acc[0] / (QSM + abs(px)) if px else float(x)
                fy = y + acc[1] / (QSM + abs(py)) if py else float(y)
            else:
                fx, fy = float(x), float(y)
            r = math.hypot(fx, fy)
            entries = E_12 * (12.0 / r) ** case.exponent * (period / 10.0) / case.flow_factor
            kick = CHARGE_PRODUCT * M * Q * entries
            px -= int(round(kick * fx / r))
            py -= int(round(kick * fy / r))
        # the step, the count primitive per axis
        fired = None
        for axis, p in enumerate((px, py)):
            if p == 0:
                continue
            wall = QSM + abs(p)
            acc[axis] += p
            # the centred step: a step fires when the accumulated motion passes HALF a Link
            # beyond the Node (the Node is then the nearest to the accumulated motion) and the
            # whole wall is subtracted, so the accumulator runs in [-wall / 2, wall / 2)
            if abs(acc[axis]) >= (wall // 2 if case.centred else wall):
                sign = 1 if acc[axis] > 0 else -1
                acc[axis] -= sign * wall
                if fired is None:
                    fired = (axis, sign)
                elif not case.lost_fires:
                    if axis == 0:
                        x += sign
                    else:
                        y += sign
        if fired is not None:
            axis, sign = fired
            if axis == 0:
                x += sign
            else:
                y += sign
        if abs(x) > HALF_WIDTH or abs(y) > HALF_WIDTH:
            escape = t
            break
        angle = math.atan2(y, x)
        # a quarter crossing: the angle passes a multiple of pi / 2
        unwrapped = angle
        while unwrapped < last_angle - math.pi:
            unwrapped += 2 * math.pi
        if math.floor(unwrapped / (math.pi / 2) + 1e-9) > quarter:
            quarter = math.floor(unwrapped / (math.pi / 2) + 1e-9)
            r = math.hypot(x, y)
            p = math.hypot(px, py)
            energy = p * p / (2 * QSM) - kappa(case) / r
            crossings.append((t, r, p / 1e6, energy / 1e6))
        last_angle = unwrapped
    lines = [
        f"[GAMEBOARD by formula] {case.name}: p0 = {case.p0}, "
        f"{'pulsed (one shell per 10 intervals)' if case.pulsed else 'steady (a tenth of a shell every interval)'}, "
        f"{'lost coincident fires' if case.lost_fires else 'no fire lost'}, flux r^-{case.exponent:.2f}, "
        f"flow factor {case.flow_factor}"
        + (
            ", THE CONTROL: the push read at the Node plus the accumulator's fraction"
            if case.at_fraction
            else ""
        )
        + (
            ", THE CENTRED STEP: a step at half the wall, the whole wall subtracted"
            if case.centred
            else ""
        )
    ]
    for t, r, p, energy in crossings[:12]:
        lines.append(
            f"    quarter at {t:5d}: r = {r:6.2f} Links, abs(p) = {p:6.1f} million, E = {energy:7.2f} x 10^6"
        )
    if escape is not None:
        lines.append(f"    the loop leaves the board at {escape}")
    else:
        lines.append(
            f"    the loop stays for {case.ticks} intervals; {len(crossings)} quarter crossings, "
            f"r at the +x crossings {[round(c[1], 2) for c in crossings[3::4]]}"
        )
    return "\n".join(lines)


def kappa(case: Case) -> float:
    """The inverse-square constant of the balance, for E only (a label)."""
    return (CHARGE_PRODUCT * M * Q * E_12 / 10.0) * 144.0 / case.flow_factor


CASES = [
    Case("A. as the algebra: steady, no fire lost", 293783192, False, False, 2.0),
    Case("B. the pulse alone: pulsed, no fire lost", 293783192, True, False, 2.0),
    Case("C. the lost fires alone: steady, main's per-axis drive", 293783192, False, True, 2.0),
    Case("D. both: pulsed, main's per-axis drive", 293783192, True, True, 2.0),
    Case("E. the lattice's flux r^-1.83: steady, no fire lost", 293783192, False, False, 1.83),
    Case("F. the lattice's flux r^-1.83: pulsed, main's per-axis drive", 293783192, True, True, 1.83),
    Case(
        "G. the stationary crowd at the circle's momentum: steady, no fire lost",
        288249497,
        False,
        False,
        2.0,
    ),
    Case(
        "H. flow-link-v1 (1.2871), the declared momentum: steady, no fire lost",
        293783192,
        False,
        False,
        2.0,
        1.2871,
    ),
    Case(
        "I. flow-link-v1 (1.2871), the declared momentum: pulsed, main's per-axis drive",
        293783192,
        True,
        True,
        2.0,
        1.2871,
    ),
    Case(
        "J. flow-link-v1 (1.2871), the re-pinned momentum: steady, no fire lost",
        254075280,
        False,
        False,
        2.0,
        1.2871,
    ),
    Case(
        "K. flow-link-v1 (1.2871), the re-pinned momentum: pulsed, main's per-axis drive",
        254075280,
        True,
        True,
        2.0,
        1.2871,
    ),
    Case(
        "L. the control of the lag: steady, no fire lost, the push at the accumulated position",
        293783192,
        False,
        False,
        2.0,
        at_fraction=True,
    ),
    Case(
        "M. the control of the lag: pulsed, main's per-axis drive, the push at the accumulated position",
        293783192,
        True,
        True,
        2.0,
        at_fraction=True,
    ),
    Case(
        "N. the control at the circle's momentum: steady, no fire lost, the push at the accumulated position",
        288249497,
        False,
        False,
        2.0,
        at_fraction=True,
    ),
    Case(
        "O. the centred step: steady, no fire lost, the push at the Node",
        293783192,
        False,
        False,
        2.0,
        centred=True,
    ),
    Case(
        "P. the centred step: pulsed, main's per-axis drive, the push at the Node",
        293783192,
        True,
        True,
        2.0,
        centred=True,
    ),
    Case(
        "R. the centred step at the circle's momentum: pulsed, main's per-axis drive, the lattice's flux r^-1.83",
        288249497,
        True,
        True,
        1.83,
        centred=True,
    ),
    Case(
        "S. the centred step under flow-link-v1 at the re-pinned momentum: pulsed, main's per-axis drive",
        254075280,
        True,
        True,
        2.0,
        1.2871,
        centred=True,
    ),
]


def main() -> None:
    print(__doc__.strip().splitlines()[0])
    print(
        f"[GAMEBOARD] Q S M = {QSM}, E_12 = {E_12} entries per shell, the kick per shell "
        f"{CHARGE_PRODUCT * M * Q * E_12:.3e} label units ({math.degrees(CHARGE_PRODUCT * M * Q * E_12 / 293783192):.2f} degrees of the declared momentum)"
    )
    push_12 = CHARGE_PRODUCT * M * Q * E_12 / 10.0
    print(
        f"[GAMEBOARD by formula] the lag's pump: the Node lags the accumulated motion by half a Link in the mean, "
        f"so the push read at the Node has a part along the motion of 1 / (2 r) of its size (4.2 percent at r = 12), "
        f"and the work per turn is pi x F(r): {math.pi * push_12:.2e} at r = 12 against the bound value "
        f"{293783192**2 / (2 * QSM) - push_12 * 144 / 12:.2e}"
    )
    for case in CASES:
        print(run(case))


if __name__ == "__main__":
    main()
