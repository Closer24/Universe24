"""EXPLORATORY, GAMEBOARD: a private host computation of the rule, no engine, no
world file, no pin, nothing registered (CLOSER24, 2026-09-24; kept beside the page
on the Boss's word of 04:50Z, item (c), as coupled_mode_pins.py is kept).

The rule of ALGEBRA.md 8.1 at
light's pair [1, 1] on a chain, integers with the remainder kept, driven by a
source that hops one Link per K intervals and oscillates at its own angle.
Read: the frequency and the amplitude of the level's first difference (the
field) behind and ahead, against the continuum's D = 1 / (1 + beta) behind
and 1 / (1 - beta) ahead (beta = v / c, c = 1 / sqrt 3). EXPLORATORY, GAMEBOARD
numbers of a private script: no engine, no world file, no pin, nothing registered.
"""

import math
import sys

L = int(sys.argv[1]) if len(sys.argv) > 1 else 7000
T = int(sys.argv[2]) if len(sys.argv) > 2 else 5200
K = int(sys.argv[3]) if len(sys.argv) > 3 else 3  # intervals per hop; 0 = at rest
OMEGA_S = 0.0895  # the source's own angle per interval (0.1129 x 0.7931, row 4b's world)
AMP = 1 << 20  # the source's amplitude at the level's unit
c = 1 / math.sqrt(3)
v = (1 / K) if K else 0.0
beta = v / c


def run(K):
    a_now = [0] * L
    a_before = [0] * L
    rem = [0] * L
    x_src = L // 2
    hop_acc = 0
    series_behind = []  # the level at a probe behind the source's start
    series_ahead = []
    probe_b = L // 2 - 1200
    probe_a = L // 2 + (T // K if K else 0) + 400  # ahead of the source's final Node
    assert probe_a < L - 10
    for t in range(T):
        # the source: the block's record a_m = AMP cos(omega_s t) at its cell; the
        # source term on light's row is the first difference of a_m (8.5)
        src = int(round(AMP * (math.cos(OMEGA_S * (t + 1)) - math.cos(OMEGA_S * t))))
        a_next = [0] * L
        for x in range(1, L - 1):
            s6 = a_now[x - 1] + a_now[x + 1] + 4 * a_now[x]
            n = s6 - 3 * a_before[x] + rem[x]
            if x == x_src:
                n += 3 * src
            a_next[x], rem[x] = divmod(n, 3)
        a_before, a_now = a_now, a_next
        series_behind.append(a_now[probe_b])
        series_ahead.append(a_now[probe_a])
        if K:
            hop_acc += 1
            if hop_acc == K:
                hop_acc = 0
                x_src += 1
    return series_behind, series_ahead, x_src


def measure(series, t0, t1):
    """The field's line: a discrete Fourier scan of the first difference over
    [t0, t1), the peak in the band [0.02, 0.4] (its angle and amplitude) and the
    amplitude at the hop's pump angle pi / 3 (8.5, prediction 4)."""
    seg = series[t0:t1]
    diffs = [b - a for a, b in zip(seg, seg[1:], strict=False)]
    n = len(diffs)
    mean = sum(diffs) / n
    diffs = [d - mean for d in diffs]

    def amp_at(w):
        re = sum(d * math.cos(w * i) for i, d in enumerate(diffs))
        im = sum(d * math.sin(w * i) for i, d in enumerate(diffs))
        return 2 * math.hypot(re, im) / n

    best = (0.0, 0.0)
    w = 0.02
    while w < 0.4:
        a = amp_at(w)
        if a > best[1]:
            best = (w, a)
        w += 0.0005
    # refine around the peak
    w = best[0] - 0.0005
    while w < best[0] + 0.0005:
        a = amp_at(w)
        if a > best[1]:
            best = (w, a)
        w += 0.00002
    return best[1], best[0], amp_at(math.pi / 3)


print(
    "EXPLORATORY, GAMEBOARD: a private host computation of the rule; no engine, no pin, nothing registered"
)
sb, sa, x_end = run(K)
w0, w1 = T - 1300, T - 100
amp_b, om_b, pump_b = measure(sb, w0, w1)
amp_a, om_a, pump_a = measure(sa, w0, w1)
print(f"K = {K}: beta = {beta:.4f}; the source moved from {L // 2} to {x_end}")
print(
    f"  behind: field amplitude {amp_b:.1f}, angle {om_b:.5f} (continuum omega_s D = {OMEGA_S / (1 + beta):.5f})"
)
print(
    f"  ahead:  field amplitude {amp_a:.1f}, angle {om_a:.5f} (continuum omega_s / (1 - beta) = {OMEGA_S / (1 - beta):.5f})"
)
print(
    f"  amplitude ratio behind / ahead = {amp_b / amp_a:.4f}; the continuum's D_b / D_a = (1 - beta) / (1 + beta) = {(1 - beta) / (1 + beta):.4f}"
)
print(
    f"  the hop's pump line at pi / 3: behind {pump_b:.1f}, ahead {pump_a:.1f} (against the Doppler line's amplitude)"
)
print(
    f"  energy share behind / ahead = {(amp_b / amp_a) ** 2:.4f}; the continuum's ((1 - beta) / (1 + beta))^2 = {((1 - beta) / (1 + beta)) ** 2:.4f}"
)
