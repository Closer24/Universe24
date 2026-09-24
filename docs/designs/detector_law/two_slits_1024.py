"""The two slits' COUNT pattern under the counting form (SIZING.md row 2a: the faces and the
mirror line sinks outside the ladder, the screen's sets the ladder, the lamp's wheel [1, 1024] with
each u once), computed BLIND before any screen reading exists (the Preliminary Runner's 10:45Z run
put every click at the open face and none on the screen). A COMPUTATION, no engine run.

The map is DESIGN.md 6.2's (the rule of `detector_law_pins.py`, the same integers) on the world's
own geometry: the lamp one driven Node behind the mirror line at x = 40 (a line of amplitude 0 with
the openings in it), the screen line read free as 6.2 reads it, the layer's open faces at x = 0 and
beyond the screen replaced by ideal sponges (a graded loss over 120 Nodes beyond each face; the
engine's open face is light's sponge, L-1), and the y boundary in three forms: "margin", 6.2's own
(the layer extended in y so that nothing returns from the y ends within the read window: the
two-source geometry itself); "periodic" (y periodic, the layer's images folded onto the screen);
"sponge" (y open with the faces as lossy bodies of three Nodes losing a quarter per interval, a
crude stand-in for the engine's face, which reflects less than this form and more than nothing).
The accumulated offer per screen Node over the record's life is the cell's share of the ladder; the
birth wheel's u chooses the cell whose cumulative interval of the shares holds (u + 1 / 2) / W
(the engine's `cell_of` over the ladder's own sum), and the counts over one wheel are the exact
click pattern the world writes if the engine's shares are the map's.

Two geometries are run. THE FIRST DRAFT of section 15 L-3 (the 128 x 128 layer, y periodic, d = 32,
L = 64, the openings of width 1): the record of why it is withdrawn, its visibility far below 6.2's
on its own map (the width-1 openings scatter into the lattice's short-wavelength modes, a floor at
the dark pixels; the periodic layer folds the images onto the screen). THE DECLARED WORLD (the
second draft, 2026-09-24): 6.2's own two-slit geometry, d = 26, L = 113, the openings of width 3,
on a 160 x 256 layer with x and y open, the lamp at [20, 128], the screen's sets over y in
[28, 228], the visibility's window y in [40, 216]; its margin form is the pin's derivation and its
sponge form the lower bound the engine's faces must beat. Printed per run: the visibility of the
accumulated offer over the two-source cosine's bright and dark pixels of the window (6.2's
statistic, the mean per pixel), the same visibility of the COUNTS (the reading of record), its grain
(one count moved), the per-Node counts, the dimmest CHOSEN cell's share (the rung wheel the screen's
sets need); then the 128-period train and the three-opening worlds of row 2c (a, b, c at the axis
and 13 Links to each side, the seven masks; the Sorkin sum of their offers and of their counts).

    PYTHONPATH=src python docs/designs/detector_law/two_slits_1024.py > docs/designs/detector_law/two_slits_1024.out
"""

from __future__ import annotations

import math
import os
import sys
import time
from dataclasses import dataclass

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from detector_law_pins import SCALE, Board, C  # noqa: E402

LIGHT = (1, 1)  # the free pair of the light kind on the six-neighbour term
LAMBDA = 12.0
X_LAMP, X_WALL = 20, 40
SPONGE = 120  # Nodes of graded loss beyond each open x face
BACK = SPONGE + 8  # the offset of the layer's x = 0 in the map's array
EDGE = 3  # the y sponge's Nodes at each face, losing a quarter per interval


@dataclass(frozen=True)
class Geometry:
    name: str
    height: int
    separation: int
    length: int
    width: int
    screen: tuple[int, int]
    window: tuple[int, int]

    @property
    def axis(self) -> int:
        return self.height // 2

    @property
    def x_screen(self) -> int:
        return X_WALL + self.length

    @property
    def x_face(self) -> int:
        return self.x_screen + 23

    def openings(self, centres: tuple[int, ...]) -> tuple[int, ...]:
        half = self.width // 2
        return tuple(y + i for y in centres for i in range(-half, half + 1))

    @property
    def two(self) -> tuple[int, int]:
        return (self.axis - self.separation // 2, self.axis + self.separation // 2)


FIRST_DRAFT = Geometry("the first draft of L-3", 128, 32, 64, 1, (4, 124), (20, 108))
DECLARED = Geometry("the declared world", 256, 26, 113, 3, (28, 228), (40, 216))


class Layer(Board):
    """The pins' rule on the layer: graded sponges beyond both x faces; the y boundary periodic,
    open with lossy faces ("sponge"), or extended by a margin ("margin"); the pair on the
    six-neighbour term in the index form (light, massless) or the well form (a massive kind:
    3 d a_next = sum6 - 3 d a_before with d = den / num, cos omega_0 = num / den at k = 0)."""

    def __init__(
        self, width: int, height: int, boundary: str, pair: tuple[int, int], well: bool = False
    ) -> None:
        super().__init__(width, height)
        self.boundary = boundary
        self.well = well
        self.num[:, :], self.den[:, :] = pair
        keep = np.ones(width, dtype=np.int64) * (4 * SPONGE * SPONGE)
        for i in range(SPONGE):
            loss = (SPONGE - i) * (SPONGE - i)  # from 1 at the sponge's start to 3 / 4 at its end
            keep[i] = 4 * SPONGE * SPONGE - loss
            keep[width - 1 - i] = 4 * SPONGE * SPONGE - loss
        self.keep = keep[:, None]
        self.keep_den = 4 * SPONGE * SPONGE
        if boundary == "sponge":
            damped = np.zeros((width, height), dtype=bool)
            damped[:, :EDGE] = True
            damped[:, height - EDGE :] = True
            self.damped = damped

    def step(self) -> None:
        a = self.now
        total = np.zeros_like(a)
        total[1:, :] += a[:-1, :]
        total[:-1, :] += a[1:, :]
        if self.boundary == "periodic":
            total += np.roll(a, 1, axis=1) + np.roll(a, -1, axis=1)
        else:
            total[:, 1:] += a[:, :-1]
            total[:, :-1] += a[:, 1:]
        total += 2 * a  # the two z-neighbours of a one-layer world are the row itself
        if self.well:
            total = self.num * total - 3 * self.den * self.before
        else:
            total = self.num * total + 6 * (self.den - self.num) * a - 3 * self.den * self.before
        total += self.remainder
        divisor = 3 * self.den
        nxt = np.floor_divide(total, divisor)
        self.remainder = total - divisor * nxt
        nxt = np.floor_divide(nxt * self.keep, self.keep_den)
        nxt[self.absorbing] = 0
        if self.damped is not None:
            nxt[self.damped] = np.floor_divide(3 * nxt[self.damped], 4)
        self.before = a
        self.now = nxt


def run_layer(
    g: Geometry,
    openings: tuple[int, ...],
    periods: float,
    boundary: str,
    pair: tuple[int, int] = LIGHT,
    period: float | None = None,
    well: bool = False,
) -> tuple[np.ndarray, int]:
    """One record: the offer accumulated per screen Node (y = 0 .. height - 1) over the record's
    life; returns it with the train's length."""
    period = LAMBDA / C if period is None else period
    train = int(round(periods * period))
    farthest = math.hypot(g.length, g.height / 2) + (X_WALL - X_LAMP)
    end = int(farthest / C) + train + int(period) + 2
    margin = (int(round(C * end - (g.x_screen - X_LAMP))) // 2 + 8) if boundary == "margin" else 0
    width = BACK + g.x_face + 1 + 8 + SPONGE
    layer = Layer(width, g.height + 2 * margin, boundary, pair, well)
    layer.absorbing[BACK + X_WALL, :] = True
    for y in openings:
        layer.absorbing[BACK + X_WALL, margin + y] = False
    offer = np.zeros(g.height, dtype=np.float64)
    for t in range(end):
        if t < train:
            layer.now[BACK + X_LAMP, margin + g.axis] = int(
                round(SCALE * math.cos(2 * math.pi * t / period))
            )
            layer.before[BACK + X_LAMP, margin + g.axis] = (
                int(round(SCALE * math.cos(2 * math.pi * (t - 1) / period))) if t else 0
            )
        layer.step()
        line = layer.now[BACK + g.x_screen, margin : margin + g.height].astype(np.float64)
        offer += line * line
    return offer, train


def counts_of(shares: np.ndarray, wheel: int) -> np.ndarray:
    """The clicks per cell over one wheel: u = 0 .. W - 1 once each, the cell the first whose
    cumulative share exceeds (u + 1 / 2) / W."""
    cumulative = np.cumsum(shares)
    counts = np.zeros(len(shares), dtype=np.int64)
    for u in range(wheel):
        cell = int(np.searchsorted(cumulative, (u + 0.5) / wheel, side="right"))
        counts[min(cell, len(shares) - 1)] += 1
    return counts


def rung_line(shares: np.ndarray, counts: np.ndarray, first_y: int) -> str:
    """The dimmest cell the wheel chooses and the rung wheel it needs, with the screen's share of
    the norm taken as 3 percent (the Runner's GAMEBOARD reading of the first draft: the faces 97)."""
    chosen = np.where(counts > 0)[0]
    dim = int(chosen[np.argmin(shares[chosen])])
    share_norm = float(shares[dim]) * 0.03
    rung = 1 << math.ceil(math.log2(4 / share_norm))
    return (
        f"the dimmest CHOSEN cell y = {first_y + dim} ({int(counts[dim])} click), its share of the screen"
        f" {shares[dim]:.3e}, of the norm {share_norm:.2e} at the screen's 3 percent, so the screen's rung"
        f" wheel must exceed {1 / share_norm:.2e}: with a margin of 4, 2^{rung.bit_length() - 1} = {rung};"
        f" the dimmest cell of all, y = {first_y + int(np.argmin(shares))}, {shares.min():.3e}, is chosen"
        f" by no u"
    )


def cosine_pixels(g: Geometry) -> tuple[list[int], list[int]]:
    ys = np.arange(g.height)
    r1 = np.hypot(g.length, ys - g.two[0])
    r2 = np.hypot(g.length, ys - g.two[1])
    cosine = np.cos(2 * math.pi * (r1 - r2) / LAMBDA)
    lo, hi = g.window
    bright = [int(y) for y in ys if lo <= y <= hi and cosine[y] > 0.95]
    dark = [int(y) for y in ys if lo <= y <= hi and cosine[y] < -0.95]
    return bright, dark


def visibility(values: np.ndarray, bright: list[int], dark: list[int]) -> float:
    b = float(np.mean(values[bright]))
    d = float(np.mean(values[dark]))
    return (b - d) / (b + d) if b + d else float("nan")


def screen_of(g: Geometry, offer: np.ndarray) -> np.ndarray:
    lo, hi = g.screen
    return offer[lo : hi + 1]


def two_slits(g: Geometry, periods: int, wheel: int, boundary: str) -> None:
    t0 = time.time()
    bright, dark = cosine_pixels(g)
    offer, train = run_layer(g, g.openings(g.two), periods, boundary)
    screen = screen_of(g, offer)
    shares = screen / screen.sum()
    counts = counts_of(shares, wheel)
    full = np.zeros(g.height)
    full[g.screen[0] : g.screen[1] + 1] = counts
    v_offer = visibility(offer, bright, dark)
    v_counts = visibility(full, bright, dark)
    moved = full.copy()
    moved[bright[len(bright) // 2]] -= 1
    moved[dark[len(dark) // 2]] += 1
    v_moved = visibility(moved, bright, dark)
    b_sum, d_sum = int(full[bright].sum()), int(full[dark].sum())
    lo, hi = g.window
    window = full[lo : hi + 1]
    print(
        f"\nTHE TWO SLITS on {g.name} ({g.height} tall, d = {g.separation}, L = {g.length}, the openings of"
        f" width {g.width}), the y boundary {boundary.upper()}, the train {periods} periods ({train}"
        f" intervals), the wheel [1, {wheel}] each u once; {time.time() - t0:.1f} s HOST"
    )
    print(
        f"   the window y in [{lo}, {hi}]: the bright pixels (the two-source cosine above 0.95) {bright};"
        f" the dark pixels (below -0.95) {dark}"
    )
    print(
        f"   the accumulated offer's visibility over the bright ({len(bright)}) and dark ({len(dark)})"
        f" pixels, the mean per pixel (6.2's statistic): {v_offer:.4f}"
    )
    print(
        f"   THE COUNTS' VISIBILITY, the same pixels, the mean count per pixel (the reading of record):"
        f" {v_counts:.4f}; the bright pixels' counts sum {b_sum}, the dark pixels' {d_sum}; one count"
        f" moved from a bright pixel to a dark one reads {v_moved:.4f} (the grain {abs(v_counts - v_moved):.4f});"
        f" the summed-count form (B - D) / (B + D) on unequal pixel numbers reads"
        f" {(b_sum - d_sum) / (b_sum + d_sum):.4f} and is not the statistic"
    )
    print(
        f"   per Node in the window: the largest count {int(window.max())} at y = {lo + int(window.argmax())},"
        f" the smallest {int(window.min())}; the per-Node visibility (max - min) / (max + min)"
        f" {(window.max() - window.min()) / (window.max() + window.min()):.4f}, its grain 2 / max ="
        f" {2 / window.max():.3f} (not the statistic)"
    )
    print("   " + rung_line(shares, counts, g.screen[0]))
    print(
        f"   the counts per Node, y = {g.screen[0]} .. {g.screen[1]}: "
        + " ".join(str(int(c)) for c in counts)
    )


def three_openings(g: Geometry, wheel: int, boundary: str) -> None:
    t0 = time.time()
    bright, _ = cosine_pixels(g)
    names = ["abc", "ab", "ac", "bc", "a", "b", "c"]
    where = {"a": g.two[0], "b": g.axis, "c": g.two[1]}
    offers = {}
    counts = {}
    for name in names:
        offer, _ = run_layer(g, g.openings(tuple(where[ch] for ch in name)), 32, boundary)
        offers[name] = screen_of(g, offer)
        counts[name] = counts_of(offers[name] / offers[name].sum(), wheel)
    sign = {"abc": 1, "ab": -1, "ac": -1, "bc": -1, "a": 1, "b": 1, "c": 1}
    s_offer = sum(sign[n] * offers[n] for n in names)
    s_count = sum(sign[n] * counts[n] for n in names)
    centre = g.axis - g.screen[0]
    lo, hi = g.window
    w = slice(lo - g.screen[0], hi - g.screen[0] + 1)
    cells = g.screen[1] - g.screen[0] + 1
    print(
        f"\nTHE THREE OPENINGS (row 2c) on {g.name}, the y boundary {boundary.upper()}: a, b, c at y ="
        f" {where['a']}, {where['b']}, {where['c']} (width {g.width}); the seven masks, the train 32"
        f" periods, one wheel [1, {wheel}] per world; {time.time() - t0:.1f} s HOST"
    )
    print(
        f"   the Sorkin sum of the accumulated OFFERS per Node, I_abc - I_ab - I_ac - I_bc + I_a + I_b"
        f" + I_c, against I_abc at the centre: the largest |S| over the {cells} cells"
        f" {np.abs(s_offer).max() / offers['abc'][centre]:.2e} (the remainders' grain; 0 for a quadratic"
        f" form, ALGEBRAIC_CLOSURE.md)"
    )
    print(
        f"   the Sorkin sum of the COUNTS per Node (each world its own wheel of {wheel}, each world's"
        f" counts normalised to its own ladder, so the seven patterns each sum to {wheel} and their"
        f" Sorkin sum over the {cells} cells is {wheel} by construction, not 0): the largest |S| over the"
        f" cells {int(np.abs(s_count).max())}, the sum over the window y in [{lo}, {hi}]"
        f" {int(s_count[w].sum())}; the three-opening centre's count {int(counts['abc'][centre])},"
        f" the bright pixels' mean count {np.mean([counts['abc'][y - g.screen[0]] for y in bright]):.1f}"
    )
    print(f"   the counts per Node of each world, y = {g.screen[0]} .. {g.screen[1]}:")
    for name in names:
        print(f"   {name:>3}: " + " ".join(str(int(c)) for c in counts[name]))


def main() -> None:
    print(
        f"lambda_0 = {LAMBDA} Links, the period {LAMBDA / C:.3f} intervals; the lamp at x = {X_LAMP} behind"
        f" the mirror line at x = {X_WALL}; the x faces as ideal sponges"
    )
    print("\n===== THE FIRST DRAFT OF L-3 (withdrawn on these numbers) =====")
    for boundary in ("margin", "periodic"):
        two_slits(FIRST_DRAFT, 32, 1024, boundary)
    print("\n===== THE DECLARED WORLD (the second draft) =====")
    for boundary in ("margin", "sponge"):
        two_slits(DECLARED, 32, 1024, boundary)
    two_slits(DECLARED, 128, 1024, "margin")
    three_openings(DECLARED, 1024, "margin")


if __name__ == "__main__":
    main()
