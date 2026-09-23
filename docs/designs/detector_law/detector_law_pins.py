"""The pins of the local detector law before any build (DESIGN.md section
6): the owner's rule run offline, in its own integers, on the pilot's
worlds scaled to the wavelength the lattice carries, and read as the law
reads a detector; a COMPUTATION, no engine run, no pin moved.

The rule (DESIGN.md section 2): a record's row at a Node holds two
integers, its amplitude now a_t and its amplitude one interval ago
a_(t-1), and a remainder r; every interval the Node re-emits to its six
neighbours what arrived from them less what it emitted the interval
before, at the world's pair c^2 = [1, 3]:

    3 a_(t+1) + r' = (sum of a_t over the six neighbours) - 3 a_(t-1) + r,
    0 <= r' < 3

(the group-ring addition over the six neighbours, verb G, and the
Euclidean division by 3 with the remainder kept on the record's row,
verb D; in a z-periodic world of one layer the two z-neighbours are the
row itself). A source Node (the lamp, or an opening's Node reached by the
lamp's rows in phase) is driven by the record's clock for the record's
emission train: a_t = A cos(2 pi t / T) with T the period in intervals,
lambda = c T Links at c = 1 / sqrt 3. A detector Node reads the offer
a_t^2 arriving at it and accumulates it; the record's clicks fall on the
detector cells in proportion to the accumulated offer (the counting
trigger on the pointer per set, DESIGN.md section 5), so the pattern of
the clicks over 4096 births is the accumulated offer per pixel, read
here as such. No wall or edge reflects into the reading: the read window
ends before the first return from the far edges (the domain is wider than
the window's light cone), and the wall's Nodes absorb (a click at the
wall, its amplitude 0).

Sections: A the rule's pace and dispersion on the lattice (a plane wave
along an axis and along a diagonal, the phase pace against c); B the
single opening at the pilot's two Fresnel numbers (w = 27 and w = 9 at
L = 108 and lambda = 4.654, scaled by lambda / 4.654), w x FWHM / lambda
against the Euclidean exact sum at the same geometry and 22.2's bands;
C the two slits scaled, the visibility over the two-source cosine's bright
and dark pixels; D the detector at rest (the light clock's N_0: the
round trip of the record's train to a reflector and back, the cycle time
read as the offer's return), at the same wavelengths. Every number is
printed with its kind.

    PYTHONPATH=src python docs/designs/detector_law/detector_law_pins.py > docs/designs/detector_law/detector_law_pins.out
"""

from __future__ import annotations

import math
import sys
import time

import numpy as np

C = 1.0 / math.sqrt(3.0)  # Links per interval, the pair [1, 3]
SCALE = 1 << 20  # the amplitude unit (the wheel's resolution; an integer)
REGISTERED_LAMBDA = 64.0 / 110.0 * 7.99870  # the pilot's 4.654 Links
BANDS = {
    27: (0.92, 0.03, 0.916),
    9: (0.886, 0.03, 0.891),
}  # 22.2's band and the exact sum at the pilot's geometry


class Board:
    """The record's rows on a 2D z-periodic world: a_t, a_(t-1), r as int64."""

    def __init__(self, width: int, height: int) -> None:
        self.width, self.height = width, height
        self.now = np.zeros((width, height), dtype=np.int64)
        self.before = np.zeros((width, height), dtype=np.int64)
        self.remainder = np.zeros((width, height), dtype=np.int64)
        self.absorbing = np.zeros((width, height), dtype=bool)

    damped: np.ndarray | None = None  # the Nodes of a lossy body (a wall that takes the offer), or None

    def step(self) -> None:
        a = self.now
        total = np.zeros_like(a)
        total[1:, :] += a[:-1, :]
        total[:-1, :] += a[1:, :]
        total[:, 1:] += a[:, :-1]
        total[:, :-1] += a[:, 1:]
        total += 2 * a  # the two z-neighbours of a one-layer world are the row itself
        total -= 3 * self.before
        total += self.remainder
        nxt = np.floor_divide(total, 3)
        self.remainder = total - 3 * nxt
        nxt[self.absorbing] = 0
        if self.damped is not None:
            # The lossy body: a Node of the wall keeps three quarters of what it would emit (the
            # rest is the offer it books), the Euclidean division by 4 with the remainder dropped.
            nxt[self.damped] = np.floor_divide(3 * nxt[self.damped], 4)
        self.before = a
        self.now = nxt


def drive(
    board: Board, nodes: list[tuple[int, int]], t: int, period: float, train: int, amplitude: int
) -> None:
    """The source's train: the record's clock on the source Nodes for `train` intervals."""
    if t < train:
        value = int(round(amplitude * math.cos(2 * math.pi * t / period)))
        for x, y in nodes:
            board.now[x, y] = value
            board.before[x, y] = (
                int(round(amplitude * math.cos(2 * math.pi * (t - 1) / period))) if t else 0
            )
    else:
        for x, y in nodes:
            board.now[x, y] = 0


def fwhm_in_s(counts: np.ndarray, distance: float, centre: float) -> tuple[float, float, float]:
    """The half-maximum crossings in s = sin(theta) by linear interpolation, as run_10_pins reads them."""
    peak = int(np.argmax(counts))
    half = counts[peak] / 2.0
    left = peak
    while left > 0 and counts[left] > half:
        left -= 1
    right = peak
    while right < len(counts) - 1 and counts[right] > half:
        right += 1

    def cross(i: int, j: int) -> float:
        if counts[i] == counts[j]:
            return float(i)
        return i + (half - counts[i]) / (counts[j] - counts[i]) * (j - i)

    yl = cross(left, left + 1)
    yr = cross(right, right - 1)

    def s_of(y: float) -> float:
        dy = y - centre
        return dy / math.sqrt(dy * dy + distance * distance)

    return s_of(yl), s_of(yr), s_of(yr) - s_of(yl)


def exact_sum(
    w: int, distance: int, height: int, centre: int, wavelength: float, obliquity: bool = False
) -> np.ndarray:
    """The Euclidean exact sum over w in-phase emitters at the opening on the screen's pixels
    (COMPUTATION): isotropic emitters (the pilot's pin, RUN_10.md), or with the obliquity cos theta
    of an aperture in a screen of amplitude 0 (Rayleigh-Sommerfeld's first solution), which is what a
    wave through a hard opening carries."""
    ys = np.arange(height)
    emitters = np.arange(centre - w // 2, centre - w // 2 + w)
    amp = np.zeros(height, dtype=complex)
    for e in emitters:
        r = np.sqrt(distance * distance + (ys - e) ** 2)
        factor = (distance / r) if obliquity else 1.0
        amp += factor * np.exp(2j * math.pi * r / wavelength) / np.sqrt(r)
    return np.abs(amp) ** 2


def section_a(period: float) -> None:
    print(
        f"\nA. THE RULE'S PACE ON THE LATTICE at T = {period:.3f} intervals (lambda = c T = {C * period:.3f} Links), COMPUTATION:"
    )
    for name, (dx, dy) in {"the axis (1, 0)": (1, 0), "the diagonal (1, 1)": (1, 1)}.items():
        # A plane wave along the heading: the phase pace by the dispersion relation of the rule,
        # 3 (2 cos(w) - 2) = sum over the six neighbours of (2 cos(k . e) - 2), solved for k at the given w.
        omega = 2 * math.pi / period
        lhs = 3 * (2 * math.cos(omega) - 2)
        norm = math.hypot(dx, dy)

        def rhs(k: float, dx: float = dx, dy: float = dy, norm: float = norm) -> float:
            kx, ky = k * dx / norm, k * dy / norm
            return (2 * math.cos(kx) - 2) + (2 * math.cos(ky) - 2)

        lo, hi = 0.0, math.pi
        for _ in range(200):
            mid = (lo + hi) / 2
            if rhs(mid) > lhs:
                lo = mid
            else:
                hi = mid
        k = (lo + hi) / 2
        pace = omega / k
        print(
            f"   along {name}: k = {k:.5f} per Link, the phase pace omega / k = {pace:.5f} Links per interval, c = {C:.5f}, the ratio {pace / C:.5f}"
        )


def section_b(wavelength: float, w0: int, train: int, wall: str = "zero") -> dict:
    scale = wavelength / REGISTERED_LAMBDA
    w = max(1, int(round(w0 * scale)))
    distance = int(round(108 * scale))
    period = wavelength / C
    height = int(round(161 * scale)) | 1
    centre = height // 2
    # The read window: from the train's first arrival at the screen until the train has passed the
    # farthest pixel (the screen's corner, at sqrt(L^2 + (h / 2)^2) Links); the far edges of the
    # world lie beyond the window's light cone, so nothing reflected enters the reading.
    farthest = math.hypot(distance, height / 2)
    arrive = int(distance / C)
    end = int(farthest / C) + train + int(period) + 2
    margin = int(round(C * end - distance)) // 2 + 8
    width = 4 + distance + margin
    board = Board(width, height + 2 * margin)
    wall_x = 2
    depth = 6 if wall == "lossy" else 1
    if wall == "lossy":
        # The wall a lossy body of `depth` Nodes on the source's side of the opening's line,
        # the opening's line itself free: the wave through the opening meets no Node of amplitude 0.
        board = Board(width + depth, height + 2 * margin)
        board.damped = np.zeros_like(board.absorbing)
        board.damped[wall_x : wall_x + depth, :] = True
        wall_x = wall_x + depth
        board.damped[
            wall_x - depth : wall_x, margin + centre - w // 2 : margin + centre - w // 2 + w
        ] = False
        board.absorbing[wall_x - depth : wall_x, :] = False
    else:
        board.absorbing[wall_x, :] = True
    opening = [(wall_x, margin + centre - w // 2 + i) for i in range(w)]
    board.absorbing[wall_x, [y for _, y in opening]] = False
    screen_x = wall_x + distance
    offer = np.zeros(height, dtype=np.float64)
    t0 = time.time()
    for t in range(end):
        drive(board, opening, t, period, train, SCALE)
        board.step()
        if t >= arrive - int(period):
            line = board.now[screen_x, margin : margin + height].astype(np.float64)
            offer += line * line
    counts = offer
    sl, sr, width_s = fwhm_in_s(counts, distance, centre)
    product = w * width_s / wavelength
    ref = exact_sum(w, distance, height, centre, wavelength)
    rl, rr, ref_s = fwhm_in_s(ref, distance, centre)
    ref_product = w * ref_s / wavelength
    oblique = exact_sum(w, distance, height, centre, wavelength, obliquity=True)
    ol, orr, obl_s = fwhm_in_s(oblique, distance, centre)
    oblique_product = w * obl_s / wavelength
    fresnel = w * w / (wavelength * distance)
    band, tol, pilot_exact = BANDS[w0]
    inside = abs(product - band) <= tol
    print(
        f"\nB. THE SINGLE OPENING w0 = {w0} scaled by {scale:.3f}, the wall {wall} (zero: a reflecting wall of amplitude 0;"
        f" lossy: a body of {depth} Nodes losing a quarter per interval): w = {w} Nodes, L = {distance} Links, lambda = {wavelength:.3f} Links"
        f" (T = {period:.3f} intervals), the Fresnel number {fresnel:.3f}, the train {train} intervals, the screen {height} pixels,"
        f" {end} intervals, {time.time() - t0:.1f} s HOST"
    )
    print(
        f"   the rule's reading (COMPUTATION on the accumulated offer per pixel): the half-maximum crossings at s = {sl:.4f} and"
        f" {sr:.4f}, FWHM(sin theta) = {width_s:.4f}, w x FWHM / lambda = {product:.3f}; the Euclidean exact sum at the same"
        f" geometry {ref_product:.3f} isotropic (the pilot's {pilot_exact}) and {oblique_product:.3f} with the obliquity cos theta"
        f" (Rayleigh-Sommerfeld, a hard screen); 22.2's band {band} +- {tol}: {'inside' if inside else 'OUTSIDE'};"
        f" the refuting bound 0.85: {'above' if product >= 0.85 else 'BELOW'}"
    )
    peak = int(np.argmax(counts))
    rough = float(np.mean(np.abs(np.diff(counts[max(0, peak - 20) : peak + 21])) / counts[peak]))
    print(
        f"   the peak at y = {peak} (centre {centre}); the pixel-to-pixel roughness near the peak {rough:.4f}"
    )
    return {"w": w, "product": product, "reference": ref_product, "inside": inside}


def section_c(wavelength: float, train: int) -> dict:
    scale = wavelength / REGISTERED_LAMBDA
    period = wavelength / C
    separation = int(round(10 * scale))
    slit = max(1, int(round(1 * scale)))
    distance = int(round(44 * scale))
    height = int(round(121 * scale)) | 1
    centre = height // 2
    farthest = math.hypot(distance, height / 2)
    arrive = int(distance / C)
    end = int(farthest / C) + train + int(period) + 2
    margin = int(round(C * end - distance)) // 2 + 8
    width = 4 + distance + margin
    board = Board(width, height + 2 * margin)
    wall_x = 2
    board.absorbing[wall_x, :] = True
    nodes = []
    for sy in (centre - separation // 2, centre + separation // 2):
        for i in range(slit):
            nodes.append((wall_x, margin + sy - slit // 2 + i))
    for _, y in nodes:
        board.absorbing[wall_x, y] = False
    screen_x = wall_x + distance
    offer = np.zeros(height, dtype=np.float64)
    t0 = time.time()
    for t in range(end):
        drive(board, nodes, t, period, train, SCALE)
        board.step()
        if t >= arrive - int(period):
            line = board.now[screen_x, margin : margin + height].astype(np.float64)
            offer += line * line
    # The two-source cosine's bright and dark pixels at this geometry (the fringe by the path difference).
    ys = np.arange(height)
    r1 = np.sqrt(distance**2 + (ys - (centre - separation // 2)) ** 2)
    r2 = np.sqrt(distance**2 + (ys - (centre + separation // 2)) ** 2)
    cosine = np.cos(2 * math.pi * (r1 - r2) / wavelength)
    bright = [
        y
        for y in range(height)
        if cosine[y] > 0.95 and abs(y - centre) < 3.2 * wavelength * distance / separation
    ]
    dark = [
        y
        for y in range(height)
        if cosine[y] < -0.95 and abs(y - centre) < 3.2 * wavelength * distance / separation
    ]
    b = float(np.mean(offer[bright])) if bright else float("nan")
    d = float(np.mean(offer[dark])) if dark else float("nan")
    visibility = (b - d) / (b + d) if b + d else float("nan")
    pearson = float(
        np.corrcoef(
            offer[abs(ys - centre) < 3.2 * wavelength * distance / separation],
            cosine[abs(ys - centre) < 3.2 * wavelength * distance / separation],
        )[0, 1]
    )
    print(
        f"\nC. THE TWO SLITS scaled by {scale:.3f}: the separation {separation}, each slit {slit} Node(s), L = {distance}, lambda ="
        f" {wavelength:.3f}, the fringe spacing lambda L / d = {wavelength * distance / separation:.1f} pixels, the train {train},"
        f" {end} intervals, {time.time() - t0:.1f} s HOST"
    )
    print(
        f"   the rule's reading (COMPUTATION on the accumulated offer): the visibility over the cosine's bright ({len(bright)}) and dark"
        f" ({len(dark)}) pixels {visibility:.4f} (the registered ray law's 0.966 at the fan's grain; nature's 0.98; the ideal 1);"
        f" Pearson with the two-source cosine over the central fringes {pearson:.3f}"
    )
    return {"visibility": visibility, "pearson": pearson}


def section_d(wavelength: float, arm: int = 60, periods: int = 2) -> dict:
    """The detector at rest, the light clock's world (320 x 3 x 3, y and z periodic, so every
    y and z neighbour of a row is the row itself and the rule is the one-dimensional chain
    3 a_(t+1) + r' = a_E + a_W + 4 a_t - 3 a_(t-1) + r): a short train (`periods` periods of the
    record's clock) sent along +x from the detector's Node to a mirror (a Node of amplitude 0, the
    sign reversed on return) `arm` Links away and back; the cycle time N_0 read as the centre of the
    returning offer (a^2 at the detector's Node, its first moment over the return's window) less the
    emitted train's centre (COMPUTATION), against the ray law's pin 206 +- 2 at L = 60, the
    continuum's 2 L / c = 207.8 and the chain's group pace 2 L / v_g at the record's clock."""
    period = wavelength / C
    train = int(round(periods * period))
    length = arm + 4
    now = np.zeros(length, dtype=np.int64)
    before = np.zeros(length, dtype=np.int64)
    remainder = np.zeros(length, dtype=np.int64)
    x0 = 1
    mirror_x = x0 + arm + 1
    end = int(3.2 * arm / C) + train
    arrivals = []
    t0 = time.time()
    for t in range(end):
        if t < train:
            now[x0] = int(round(SCALE * math.cos(2 * math.pi * t / period)))
        total = np.zeros_like(now)
        total[1:] += now[:-1]
        total[:-1] += now[1:]
        total += 4 * now - 3 * before + remainder
        nxt = np.floor_divide(total, 3)
        remainder = total - 3 * nxt
        nxt[mirror_x:] = 0
        nxt[0] = 0
        before, now = now, nxt
        arrivals.append(float(now[x0]) ** 2)
    rate = np.array(arrivals)
    lo = train + int(period)
    hi = min(end, int(3 * arm / C) + train)
    window = rate[lo:hi]
    ts = np.arange(lo, hi)
    centre = float(np.sum(ts * window) / np.sum(window)) if np.sum(window) else float("nan")
    n0 = centre - train / 2
    # The counting trigger's click: the interval at which the returning offer's accumulation crosses
    # a rung, read at the fractions 1 / 4096 (the wheel's first rung), 1 / 16 and 1 / 2 of the return.
    cumulative = np.cumsum(window)
    crossings = {
        name: int(ts[int(np.searchsorted(cumulative, fraction * cumulative[-1]))]) - train / 2
        for name, fraction in (("1 / 4096", 1 / 4096), ("1 / 16", 1 / 16), ("1 / 2", 0.5))
    }
    # The chain's group pace at the record's clock: 3 (2 cos w - 2) = 2 cos k - 2, v_g = sin k / (3 sin w).
    omega = 2 * math.pi / period
    k = math.acos(1 + 3 * (math.cos(omega) - 1))
    group = math.sin(k) / (3 * math.sin(omega))
    print(
        f"\nD. THE DETECTOR AT REST (the light clock's chain), the arm {arm} Links, lambda = {wavelength:.3f}, the train {train}"
        f" intervals ({periods} periods): the returning offer's centre at the interval {centre:.1f}, less the train's centre"
        f" {train / 2:.1f}: N_0 = {n0:.1f} intervals (COMPUTATION; the ray law's pin 206 +- 2 at L = 60; the continuum's 2 L / c ="
        f" {2 * arm / C:.1f}; the chain's group pace at this clock {group:.4f} Links per interval, 2 L / v_g = {2 * arm / group:.1f});"
        f" the counting trigger's click at the rung crossings of the returning offer, less the train's centre:"
        f" {', '.join(f'{k}: {v:.1f}' for k, v in crossings.items())}; the mirror's zero Node one Link beyond the arm;"
        f" {time.time() - t0:.1f} s HOST"
    )
    return {"n0": n0}


def section_e(wavelength: float, arm: int = 60, k: int = 3, periods: int = 2) -> dict:
    """The moving detector along its motion (the light clock's par world at k = 3): the detector's
    body and its mirror advance one Node every k intervals along +x (the drive's pace 1 / k Links
    per interval, beta = 1 / (k c) = 0.577 at k = 3); the record's train is emitted from the body's
    Node as it moves and the return is read at the body's Node where it is now, by the first rung of
    the returning offer (COMPUTATION), against the ray law's whole-tick pin N_par = 307 +- 10 at
    k = 3 and the classical medium clock's 2 L gamma^2 / c = 309.6."""
    period = wavelength / C
    train = int(round(periods * period))
    end = int(4.0 * arm / C) + train
    length = arm + end // k + 8
    now = np.zeros(length, dtype=np.int64)
    before = np.zeros(length, dtype=np.int64)
    remainder = np.zeros(length, dtype=np.int64)
    arrivals = []
    t0 = time.time()
    for t in range(end):
        body = 1 + t // k
        mirror = body + arm + 1
        if t < train:
            now[body] = int(round(SCALE * math.cos(2 * math.pi * t / period)))
        total = np.zeros_like(now)
        total[1:] += now[:-1]
        total[:-1] += now[1:]
        total += 4 * now - 3 * before + remainder
        nxt = np.floor_divide(total, 3)
        remainder = total - 3 * nxt
        nxt[mirror:] = 0
        nxt[:body] = 0  # the body's own Node the last free one behind the train; nothing behind it
        before, now = now, nxt
        body_next = 1 + (t + 1) // k
        arrivals.append(float(now[body_next]) ** 2)
    rate = np.array(arrivals)
    lo = train + int(period)
    window = rate[lo:]
    cumulative = np.cumsum(window)
    first = lo + int(np.searchsorted(cumulative, cumulative[-1] / 4096)) if cumulative[-1] else -1
    beta = 1 / (k * C)
    gamma2 = 1 / (1 - beta * beta)
    print(
        f"\nE. THE MOVING DETECTOR along its motion, the arm {arm} Links, k = {k} (beta = {beta:.4f}), lambda = {wavelength:.3f},"
        f" the train {train} intervals ({periods} periods): the counting trigger's first rung of the returning offer at the body's"
        f" Node at the interval N_par = {first} (COMPUTATION; the ray law's whole-tick pin 307 +- 10 at k = 3; the classical"
        f" medium clock's 2 L gamma^2 / c = {2 * arm * gamma2 / C:.1f}; the ratio to the resting 206: {first / 206:.4f}, the pin's 307 / 206"
        f" = 1.4903, gamma^2 = {gamma2:.4f}); {time.time() - t0:.1f} s HOST"
    )
    return {"n_par": first}


PERIODS = 32  # the record's emission train in periods of its clock (the lamp's declaration, kind 1)


def main() -> None:
    wavelengths = [float(a) for a in sys.argv[1:]] or [8.0, 12.0, 16.0]
    print(
        "THE LOCAL DETECTOR LAW, the pins before any build (COMPUTATION, the rule run offline in its own integers; no engine run);"
        f" the amplitude unit {SCALE}, the train {PERIODS} periods of the record's clock, c = 1 / sqrt 3 = {C:.5f} Links per interval"
    )
    for wavelength in wavelengths:
        train = int(round(PERIODS * wavelength / C))
        print(f"\n===== lambda = {wavelength:.3f} Links, the train {train} intervals =====")
        section_a(wavelength / C)
        for w0 in (27, 9):
            section_b(wavelength, w0, train)
        section_b(wavelength, 9, train, wall="lossy")
        section_c(wavelength, train)
        section_d(wavelength)
        section_e(wavelength)


if __name__ == "__main__":
    main()
