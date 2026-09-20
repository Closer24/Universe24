"""The numbers behind INFORMATION_TRANSFER.md: what follows, as a formula,
from "everything on the GameBoard is a transfer of information" under the
rules of amplitude-v1 (one Link per interval, the phase as a counter on N
steps, the split an isometry, the click reading one record's squared sum),
and how each formula reads against the real world.

    python paper/click_model/checks/information_transfer.py

Nothing here is an engine run: the formulas are evaluated from the
design's rules and the repository's tables, and the registered numbers
they are compared with are read from figures/summary.json.
"""

from __future__ import annotations

import json
import math
from fractions import Fraction
from pathlib import Path

HERE = Path(__file__).resolve().parent
SUMMARY = HERE.parent / "figures" / "summary.json"

# physical constants (CODATA 2018), for the readings only
PLANCK = 6.62607015e-34  # J s
LIGHT = 299792458.0  # m/s
BOLTZMANN = 1.380649e-23  # J/K
ELECTRON_VOLT = 1.602176634e-19  # J
PLANCK_LENGTH = 1.616255e-35  # m


def section(title: str) -> None:
    print(f"\n== {title}")


def causal_cone() -> None:
    """One Link per interval: the front of any information is the L1 ball.
    The Euclidean speed of the front in the direction (cos, sin) is
    1 / (|cos| + |sin|) in two dimensions and 1 / (|x| + |y| + |z|) on the
    unit sphere in three."""
    section("1. The causal cone: one Link per interval, an L1 front")
    for degrees in (0, 15, 30, 45):
        angle = math.radians(degrees)
        speed = 1 / (abs(math.cos(angle)) + abs(math.sin(angle)))
        print(
            f"  two dimensions, {degrees:2d} degrees off an axis: front speed {speed:.4f} Links per interval"
        )
    print(
        f"  three dimensions, the body diagonal: {1 / math.sqrt(3):.4f}; the slowest direction of the front"
    )
    print(
        "  reading: c = a / tau along an axis; the front is an octahedron, not a sphere (an anisotropy of 42 percent)"
    )


def wavelengths() -> None:
    """A row's phase counts n / d steps of the N-circle per interval of its
    age (the pair form), or an integer per Link crossed. Its wavelength is
    N d / n Links; the shortest is 2 Links (n / d = N / 2, the alias
    bound); the resolution of the phase is 2 pi / N whatever the rate."""
    section("2. Wavelength and the Link: lambda = N d / n Links; lambda >= 2 Links")
    for n_steps, n, d in (
        (64, 8, 1),
        (64, 8591334592, 1073741824),
        (4096, 1, 1),
        (4096, 2048, 1),
        (65536, 1, 3),
    ):
        print(
            f"  N = {n_steps:5d}, rate {n}/{d} steps per interval: lambda = {n_steps * d / n:.4f} Links"
        )
    print(
        "  the register's Mach-Zehnder with unequal arms (phase per Link 8 at N = 64): lambda = 8 Links"
    )
    energies = {"visible 500 nm": 2.48, "the 1.4 PeV photon of LHAASO (2021)": 1.4e15}
    for name, ev in energies.items():
        wavelength = PLANCK * LIGHT / (ev * ELECTRON_VOLT)
        print(f"  {name}: lambda = {wavelength:.3e} m, so a <= lambda / 2 = {wavelength / 2:.3e} m")
    print(
        f"  the Planck length {PLANCK_LENGTH:.3e} m is {PLANCK * LIGHT / (1.4e15 * ELECTRON_VOLT) / 2 / PLANCK_LENGTH:.2e} times below that bound"
    )
    print(
        "  reading: the Link is at most half the shortest wavelength ever seen; no lower bound on a from this"
    )


def born_precision() -> None:
    """The ladder b_k = (2 N C_k + T) // (2 T) puts the click's probability
    of a cell within 1 / (2 N) of W_k / T; a measured departure delta from
    a squared-sum law bounds N >= 1 / (2 delta)."""
    section("3. The click's precision: |P(o) - W_o / T| <= 1 / (2 N)")
    for n_steps in (64, 184, 1024, 4096, 65536):
        print(
            f"  N = {n_steps:5d}: the probabilities are multiples of 1/N, each within {1 / (2 * n_steps):.2e} of the squared sum"
        )
    for delta in (1e-2, 1e-3, 1e-4):
        print(
            f"  a squared-sum law confirmed to delta = {delta:.0e} needs N >= {math.ceil(1 / (2 * delta))}"
        )
    print(
        "  the pair's S at N = 64 .. 4096 against Poh et al. 2015 is the sharper bound (N >= 184, s_of_n.txt)"
    )


def isometry() -> None:
    """The split (w, m) -> (w a_i, m A), A = sum a_i^2, preserves the sum of
    w^2 / m: nothing is amplified; a copy of a row at its own norm cannot
    be made (the no-cloning reading)."""
    section("4. No amplification at a split: sum w_i^2 / m_i = w^2 / m")
    for shares in ((1, 1), (3, 4), (1, 2, 2), (5, 12)):
        a_sq = sum(a * a for a in shares)
        total = sum(Fraction(a * a, a_sq) for a in shares)
        print(f"  shares {shares}: A = {a_sq}, sum (w a_i)^2 / (m A) = {total} x w^2 / m")
    print("  two rows of the full norm would need the sum 2: refused by the identity above")


def bits_per_click(summary: dict) -> None:
    """A click reports one cell of a record: at most log2 (cells) bits leave
    the rows per click, whatever the rows carried (the Holevo reading)."""
    section("5. Bits per click: at most log2 (cells) per record")
    worlds = {
        "Mach-Zehnder (2 counters)": 2,
        "Elitzur-Vaidman (absorber, D1, D2)": 3,
        "the pair (4 cells)": 4,
        "GHZ (8 triples)": 8,
        "two slits (80 sets)": 80,
    }
    for name, cells in worlds.items():
        print(f"  {name}: <= {math.log2(cells):.2f} bits per click")
    ghz = summary["ghz"]["ghz_xxx"]["triples"]
    print(
        f"  GHZ XXX in the register: {ghz} = 4 of 8 triples, 2 bits, the product fixed (1 bit of the 3 is the law's)"
    )


def landauer() -> None:
    """A click deletes the record's rows and keeps one cell: the bits erased
    are at least the rows' bits less the cell's. Landauer's bound turns
    that into a least heat per click at temperature T. A conjecture: the
    rows' minimal bits are the model's, not the engine's representation."""
    section(
        "6. The heat of a click (a conjecture): Q >= k T ln 2 x (bits of the rows - bits of the cell)"
    )
    for n_steps in (64, 4096):
        bits_per_row = math.log2(6) + math.log2(n_steps)
        for name, rows, cells in (("Mach-Zehnder", 2, 2), ("the pair", 4, 4)):
            erased = rows * bits_per_row - math.log2(cells)
            for temperature in (300.0, 1.0):
                heat = BOLTZMANN * temperature * math.log(2) * erased
                print(
                    f"  N = {n_steps:4d}, {name:13s}: {erased:5.1f} bits erased; at {temperature:5.0f} K "
                    f"Q >= {heat:.2e} J = {heat / ELECTRON_VOLT:.3f} eV"
                )
    print(
        "  reading: a detector's least dissipation per click; only a lower bound, far below any real detector's"
    )


def young_fringes() -> None:
    """Two slits at (0, +-s/2), a screen at distance D. If the phase counts
    Links crossed on a staircase path, the path difference is the L1 one,
    |y - s/2| - |y + s/2|, constant (= -s) beyond |y| >= s/2: no periodic
    fringes. If it counts Euclidean length, the difference is ~ y s / D and
    the fringes are spaced lambda D / s."""
    section(
        "7. Two slits: the L1 path difference against the Euclidean one (s = 6, D = 44, lambda = 8 Links)"
    )
    s, distance, wavelength = 6, 44, 8.0
    print("   y   L1 diff  Euclid diff   I_L1   I_Euclid")
    for y in range(0, 25, 4):
        l1 = abs(y - s / 2) - abs(y + s / 2)
        euclid = math.hypot(distance, y - s / 2) - math.hypot(distance, y + s / 2)
        i_l1 = 2 + 2 * math.cos(2 * math.pi * l1 / wavelength)
        i_eu = 2 + 2 * math.cos(2 * math.pi * euclid / wavelength)
        print(f"  {y:2d}   {l1:6.2f}   {euclid:8.3f}   {i_l1:5.2f}   {i_eu:5.2f}")
    print(
        f"  Euclidean fringe spacing lambda D / s = {wavelength * distance / s:.1f} Links; the L1 pattern has none beyond |y| = s / 2"
    )
    print(
        "  the register's two-slit run: Pearson 0.368 with the cosine pattern, 0.744 with the incoherent sum (expectations.json)"
    )


def distance(summary: dict) -> None:
    section("8. The correlation does not depend on the distance: the far worlds")
    far = summary["far"]["bell_16_24_far"]
    near = summary["pair"]["64"]["worlds"]["bell_16_24"]
    print(
        f"  bell_16_24: cells {near['cells']}, E = {near['E']}; Bob 116 Links farther: cells {far['cells']}, E = {far['E']}"
    )
    print(
        "  the joint distribution is fixed at the birth (u with the record); the click adds nothing that travels"
    )


def main() -> None:
    summary = json.loads(SUMMARY.read_text(encoding="utf-8"))
    causal_cone()
    wavelengths()
    born_precision()
    isometry()
    bits_per_click(summary)
    landauer()
    young_fringes()
    distance(summary)


if __name__ == "__main__":
    main()
