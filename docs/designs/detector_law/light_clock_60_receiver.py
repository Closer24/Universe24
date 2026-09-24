"""The light clock's pin re-derived under DECLARATIONS.md section 10 item 9's declared form
(2026-09-24, 09:55Z, on the owner's word of 09:50Z): COMPUTATION on the map with the SET IN THE
RECEIVER FORM (the map (h)'s Port with a ghost, DESIGN.md section 5; the engine's form),
light_clock_60's own geometry: the chain 673 closed at both ends, A at [600, 612), the set the one
Node 612 (free for the grace 140, then held at 0 with its Port toward 613, light's take pair
[-15, 56]), the mirror 672, A's cells taking their own record from age 70 (T = 0, item 10) with
Ports at 599 and 612 (the latter free during the grace, held after it). Inputs: the world file's
pairs, the amplitude 2^20, the declared train 70. Outputs: the set's first rung after the birth at
W = 64 (256, 1024 beside) with the rise, and the motion left on the board against the pointer by
age through the -x half's return (2078), the first age at which energy x W_c < pointer for W_c = 64
and 256. No run's number enters.
THE CLOSE PRINTED LAST IS THE MAP'S OWN AND NOT THE ENGINE'S (withdrawn as a prediction, 09:56Z):
the map's Port takes the +x half whole on its first pass, the engine's one-Node set takes a part
and reflects the rest, which stays trapped between the set and the mirror (the Preliminary Runner's
2600 probe); the first rung, the pin, is the same on both (213 on the map, 214 in the engine)."""

import math
import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import coupled_mode_pins as m  # noqa: E402

SAMPLE_AGES = (150, 220, 300, 400, 700, 1000, 1500, 1900, 2000, 2100, 2150, 2200, 2400, 2600, 2999)
LEVELS = (0.25, 0.5, 1.0, 1.5, 2.0)


def run(
    W=64,
    n=673,
    lo=600,
    s=12,
    set_node=612,
    G=140,
    E=70,
    steps=3000,
    ramp=300,
    g=1 / 50000,
    big_g=1.0,
    amp=2**20,
    train=70,
    a_take=True,
):
    """One record on the chain; returns A's mode, the norm, the pointer's crossings of the rung's
    fractions (ages), the pointer series in rungs, the map's close ages and the sampled rows."""
    reads = m.open_chain_reads(n)
    idx = np.arange(n)
    cells = (idx >= lo) & (idx < lo + s)
    d_node = m.well_d(cells, 800, 809, 800, 800)
    omega_b, prof = m.bare_mode(reads, np.where(cells, 1.0, 809 / 800))
    prof = prof / np.abs(prof).max() * amp
    if prof[lo + s // 2] < 0:
        prof = -prof
    m_now, m_bef = prof.copy(), prof * math.cos(omega_b)
    l_now, l_bef = np.zeros(n), np.zeros(n)
    ce = cells.astype(float)
    norm = 0.0
    pointer = 0.0
    taken = 0.0
    a_ports = {"lo": (lo, lo - 1), "hi": (lo + s - 1, lo + s)}  # (near cell, free neighbour)
    a_ghost = {}
    set_ghost = None
    set_near, set_free = set_node, set_node + 1
    birth = ramp
    crossings = {}
    closes = {}
    rows = []
    series = []
    for t in range(steps + ramp):
        age = t - birth
        a_taking = a_take and age >= E
        set_taking = age >= G
        if a_taking and age == E:
            for f, (near, _free) in a_ports.items():
                a_ghost[f] = l_now[near]
        if set_taking and age == G:
            set_ghost = l_now[set_near]
        in_train = ramp <= t < ramp + train
        source = big_g * ce * (m_now - m_bef) if in_train else 0.0
        m_next = (reads @ m_now) / d_node / 3 - m_bef + g * ce * (l_now - l_bef)
        l_next = (reads @ l_now) / 3 - l_bef - source
        if a_taking:
            for f, (near, free) in a_ports.items():
                # the +x Port's neighbour is held by the set after the grace
                if not (set_taking and free == set_node):
                    l_next[free] += (a_ghost[f] - l_now[near]) / 3
        if set_taking:
            l_next[set_free] += (set_ghost - l_now[set_near]) / 3
        l_next[0] = 0.0
        l_next[-1] = 0.0
        if in_train:
            norm += float(np.sum(source**2))
        if a_taking:
            l_next[cells] = 0.0
            for f, (_near, free) in a_ports.items():
                if set_taking and free == set_node:
                    continue
                new = l_now[free] + m.TAKE_K * (l_next[free] - a_ghost[f])
                taken += (new - a_ghost[f]) ** 2
                a_ghost[f] = new
        if set_taking:
            l_next[set_node] = 0.0
            new = l_now[set_free] + m.TAKE_K * (l_next[set_free] - set_ghost)
            pointer += (new - set_ghost) ** 2
            set_ghost = new
            r = pointer * W / norm
            series.append((age, r))
            for level in LEVELS:
                if level not in crossings and r >= level:
                    crossings[level] = age
        energy = float(np.sum((l_next - l_now) ** 2))
        for W_c in (64, 256):
            if W_c not in closes and age > train and pointer > 0 and energy * W_c < pointer:
                closes[W_c] = age
        if age in SAMPLE_AGES:
            left = float(np.sum((l_next[:lo] - l_now[:lo]) ** 2))
            cav = float(np.sum((l_next[set_node + 1 :] - l_now[set_node + 1 :]) ** 2))
            rows.append(
                (
                    age,
                    energy,
                    pointer,
                    taken,
                    left / energy if energy else 0,
                    cav / energy if energy else 0,
                )
            )
        m_bef, m_now = m_now, m_next
        l_bef, l_now = l_now, l_next
    return omega_b, norm, crossings, series, closes, rows


def main():
    omega_b, norm, _cr, series, closes, rows = run()
    print(
        f"A's bare mode omega {omega_b:.5f}, period {2 * math.pi / omega_b:.2f}; the norm {norm:.4e}; "
        f"the -x return {2 * 600 * math.sqrt(3):.0f}"
    )
    for W in (64, 256, 1024):
        _, _, c, s_, _, _ = run(W=W, steps=400)
        before = max((r for a, r in s_ if a < c.get(1.0, 10**9)), default=0.0)
        print(
            f"W = {W:4d}: FIRST RUNG at age {c.get(1.0)}; 1/4 at {c.get(0.25)}, 1/2 at {c.get(0.5)}, "
            f"3/2 at {c.get(1.5)}, 2 at {c.get(2.0)}; the largest reading before the rung {before:.3f} rung"
        )
    _, _, c0, _, _, _ = run(W=64, steps=400, a_take=False)
    print(
        f"beside, no take at A's cells (the earlier form, HISTORY): first rung {c0.get(1.0)} at W = 64"
    )
    print("the rise at W = 64:", ", ".join(f"{a}:{r:.3f}" for a, r in series if 205 <= a <= 226))
    print(
        "age | energy left | pointer | taken at A | share -x side | share beyond the set | "
        "energy x 64 / pointer | x 256"
    )
    for age, e, p, tk, left, cav in rows:
        r64 = e * 64 / p if p else float("inf")
        r256 = e * 256 / p if p else float("inf")
        print(
            f"{age:5d} | {e:.3e} | {p:.3e} | {tk:.3e} | {left:.3f} | {cav:.3f} | {r64:.2f} | {r256:.1f}"
        )
    print(
        "THE CLOSE on the map (the first age with energy x W_c < pointer), the map's own, "
        "not the engine's (see the docstring):",
        closes,
    )


if __name__ == "__main__":
    main()
