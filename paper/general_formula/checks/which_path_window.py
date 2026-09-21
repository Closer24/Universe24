"""A which-path window on one arm of the design's Mach-Zehnder: the duality relation.

The design's rules (docs/designs/amplitude-v1/DESIGN.md, sections 2 to 4): one record
of two rows, amplitude 1/sqrt 2 each, on a (1, 1) splitter with the quarter turn on the
reflected output; on arm 2 a measured event whose window admits the row when its phase
lies in the half circle centred on s (BEAM_LAW step 4: the window reads the row's own
phase) and absorbs it (its offer is the row's norm), or passes it whole; the record's
ladder at completion with the rungs at the nearest integer, the absorber first in the
declared order, then D1, D2. Counts over the N birth phases u at every arm phase phi.
A computation from the formulas with the repository's tables, not a run of the engine.
"""

from __future__ import annotations

import sys
from fractions import Fraction

sys.path.insert(0, "src")
from event_universe.core.phase import phase_cosines  # noqa: E402

N = 64
C = phase_cosines(N)
S = tuple(C[(k - N // 4) % N] for k in range(N))


def rung(cumulative: Fraction, total: Fraction) -> int:
    return int((2 * N * cumulative + total) // (2 * total))


def offers_interfering(phi: int) -> dict[str, Fraction]:
    # D1: arm 1 at u, arm 2 at u + phi + N/2 (two quarter turns); D2: both at u + N/4 + (0 or phi)
    def weight(delta: int) -> Fraction:
        x, y = 256 + C[delta % N], S[delta % N]
        return Fraction(x * x + y * y, 4 * 65536)  # |1 + e^{i delta}|^2 / 4 on the tables

    return {"D1": weight(phi + N // 2), "D2": weight(phi)}


def click(offers: dict[str, Fraction], u: int) -> str:
    total = sum(offers.values())
    cumulative = Fraction(0)
    for name, w in offers.items():
        cumulative += w
        if u < rung(cumulative, total):
            return name
    return name


def counts(phi: int, window: int | None, s: int = 0) -> dict[str, int]:
    out = {"absorber": 0, "D1": 0, "D2": 0}
    for u in range(N):
        arm2_phase = (u + N // 4 + phi) % N
        admitted = window is not None and (arm2_phase - s + window // 2) % N < window
        if admitted:
            offers = {"absorber": Fraction(1, 2), "D1": Fraction(1, 4), "D2": Fraction(1, 4)}
        else:
            offers = offers_interfering(phi)
        out[click(offers, u)] += 1
    return out


def visibility(series: list[int]) -> float:
    return (max(series) - min(series)) / (max(series) + min(series))


def main() -> None:
    for window, label in (
        (None, "no window on arm 2: the plain interferometer"),
        (N, "window the whole circle: the absorber always admits (Elitzur-Vaidman)"),
        (N // 2, "window the half circle centred on s = 0"),
        (N // 4, "window a quarter circle"),
    ):
        print(f"== {label}")
        d1, d2, ab = [], [], []
        for phi in range(0, N, 4):
            c = counts(phi, window)
            d1.append(c["D1"])
            d2.append(c["D2"])
            ab.append(c["absorber"])
        print(f"  phi = 0, 4, .., 60: D1 {d1}")
        print(f"                     D2 {d2}")
        print(f"                     absorber {ab}")
        surviving = [a + b for a, b in zip(d1, d2, strict=True)]
        print(
            f"  D1 visibility over phi: {visibility(d1):.3f}; absorber share {sum(ab) / (16 * N):.3f}; D1 among the surviving: {visibility([a / s_ for a, s_ in zip(d1, surviving, strict=True)]):.3f}"
        )
    # the same with the window's centre s varied: does the D1 count depend on s at fixed phi?
    print("== the half-circle window at phi = 16, the centre s = 0, 8, 16, 24, 32:")
    print("  ", [counts(16, N // 2, s) for s in (0, 8, 16, 24, 32)])
    # the model's duality: the fraction f of births the window admits (on the GameBoard) against the visibility
    print("== the fraction admitted by the window against the fringe visibility of D1, N = 64:")
    for window in (0, 8, 16, 24, 32, 40, 48, 56, 64):
        d1 = [counts(phi, window if window else None)["D1"] for phi in range(0, N, 4)]
        print(
            f"  window {window:2d}/64: admitted f = {window / N:.3f}; V(D1) = {visibility(d1):.3f}; V + f = {visibility(d1) + window / N:.3f}; V^2 + f^2 = {visibility(d1) ** 2 + (window / N) ** 2:.3f}"
        )


if __name__ == "__main__":
    main()
