"""Series O (two stars, examples/events/two_stars) under covariant-readings-v1
as amended (17.6: M1, N1, N2, N4): the expected readings pinned before any
run (read-only, the derivation mathematician, 2026-09-21; DERIVATIONS_BEAM
18.6). Exact rationals from the declared momenta of the three world files;
decimal only for display. No run.

The identity's rules used: a body's self-creations come one per E / (m c^2)
= gamma lattice intervals (M1); the lamp's count is per self-creation, so a
moving lamp emits per proper time (N4); the drive's rate per self-creation
is Newton's p / (Q S M), so the pace per lattice interval is p c^2 / E (M1, on
the domain |p|_1 <= Q S M, N2); the crossing count is read per interval and
charged per self-creation (N1); c^2 = [1, 3] (M3), the rows on a heading at
c_h = 32 / 55 Links per interval (2.1).

Run from the repository root:

    python docs/designs/derivations_beam/series_o_identity.py > docs/designs/derivations_beam/series_o_identity.out
"""

from __future__ import annotations

import json
import math
from fractions import Fraction as Fr
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
WORLDS = ROOT / "examples" / "events" / "two_stars"
Q = 64
C_H = Fr(32, 55)  # the rows' pace on a heading
GAP = 60  # the stars' Links apart at the start (x = 70 and 130)


def dec(x: Fr | float, places: int = 4) -> str:
    return f"{float(x):.{places}f}"


class Star:
    def __init__(self, entry: dict, width: int) -> None:
        self.name = entry["family"]
        self.x = entry["position"][0]
        self.p = entry["momentum"][0]
        content = entry["amount"] + sum(entry["held"].values())
        self.qsm = Q * width * content
        self.v_law = Fr(abs(self.p), self.qsm + abs(self.p))  # the law's drive (4.4)
        w = self.qsm * self.qsm + 3 * self.p * self.p
        self.e = math.isqrt(w)  # E / c^2 (17.6 M3)
        self.gamma = Fr(self.e, self.qsm)
        self.v = Fr(abs(self.p), self.e)  # the identity's pace per lattice interval
        self.sign = 1 if self.p > 0 else -1 if self.p < 0 else 0
        assert abs(self.p) <= self.qsm  # N2's domain
        # nature's beta on the heading's c and the identity's own (c = 1 / sqrt 3)
        self.beta_h = self.v / C_H
        self.beta_id = float(self.v) * math.sqrt(3)


def reading(v_source_toward: Fr, gamma_s: Fr, v_reader_toward: Fr, gamma_r: Fr) -> tuple[Fr, Fr]:
    """A lamp moving at v_s toward its reader (negative: away), emitting one
    unit per gamma_s intervals, its units (c_h - v_s) gamma_s Links apart on
    the axis; a reader moving at v_r toward them meets (c_h + v_r) / ((c_h -
    v_s) gamma_s) per lattice interval. Returns (1 + z by the record's tool,
    the births per click tick against the lamp's declared rate of one per
    interval; 1 + z per the reader's own clock, the count per self-creation)."""
    per_interval = (C_H + v_reader_toward) / ((C_H - v_source_toward) * gamma_s)
    return 1 / per_interval, 1 / (per_interval * gamma_r)


def nature_mutual(beta_a: float, beta_b: float) -> float:
    beta = (beta_a + beta_b) / (1 + beta_a * beta_b)
    return math.sqrt((1 - beta) / (1 + beta))


def contact_tick(stars: list[Star]) -> int:
    """The first interval t at which the Links made would close the gap:
    floor(t v_A) + floor(t v_B) >= GAP (the step onto the occupant refused:
    the contact), with the identity's pace per interval in the mean."""
    t = 0
    while sum(math.floor(t * s.v) for s in stars) < GAP:
        t += 1
    return t


print("Series O under covariant-readings-v1: the expected readings from the declared momenta.")
for name in ("symmetric_pass", "symmetric", "rest_frame"):
    world = json.loads((WORLDS / f"{name}.json").read_text())
    width = world["width"]
    stars = {m["family"]: Star(m, width) for m in world["measured"] if m["family"].startswith("s_")}
    a, b = stars["s_px1"], stars["s_mx1"]
    print()
    print(
        f"[{name}]  Q S M = {a.qsm} (= 2^{math.log2(a.qsm):.4f}); the mass entry {world['measured'][2].get('table', {}).get('mass', {'rule': 'read'})['rule']}"
    )
    for s in (a, b):
        print(
            f"  {s.name} at x = {s.x}: p = {s.p:+d} ({dec(Fr(abs(s.p), s.qsm), 5)} of Q S M);"
            f" the law's pace {dec(s.v_law, 5)} Links per interval = {dec(s.v_law / C_H, 4)} c_h;"
            f" E / c^2 = {s.e}, gamma = E / (m c^2) = {dec(s.gamma, 5)};"
            f" the identity's pace p c^2 / E = {dec(s.v, 5)} = {dec(s.beta_h, 4)} c_h, beta = {s.beta_id:.4f} on c = 1 / sqrt 3"
        )
    # A moves toward +x (toward B), B toward -x (toward A) or at rest.
    va, vb = a.sign * a.v, -b.sign * b.v  # each star's speed TOWARD the other
    a_reads_b = reading(vb, b.gamma, va, a.gamma)
    b_reads_a = reading(va, a.gamma, vb, b.gamma)
    left_lab = reading(-va, a.gamma, Fr(0), Fr(1))  # A recedes from the left lab
    right_lab = reading(-vb, b.gamma, Fr(0), Fr(1))  # B recedes from the right lab
    nat_mut = nature_mutual(float(va / C_H), float(vb / C_H))
    print(
        "  A reads B: by the tool (per click tick) 1 + z = "
        + dec(a_reads_b[0])
        + ", per A's own clock "
        + dec(a_reads_b[1])
    )
    print("  B reads A: by the tool " + dec(b_reads_a[0]) + ", per B's own clock " + dec(b_reads_a[1]))
    print(
        "  the left lab reads A (receding): "
        + dec(left_lab[0])
        + "; the right lab reads B: "
        + dec(right_lab[0])
        + " (a lab at rest: the tool's and its own clock's readings are one)"
    )
    print(
        f"  nature at the same speeds (beta on c_h): the mutual {nat_mut:.4f} for both;"
        f" the labs (1 + beta) gamma: {(1 + float(va / C_H)) / math.sqrt(1 - float(va / C_H) ** 2):.4f} of A,"
        f" {(1 + float(vb / C_H)) / math.sqrt(1 - float(vb / C_H) ** 2):.4f} of B"
    )
    law_a = (1 - vb / C_H) / (1 + va / C_H)
    law_b = (1 - va / C_H) / (1 + vb / C_H)
    va_law, vb_law = a.sign * a.v_law, -b.sign * b.v_law
    print(
        f"  the law as built at the law's own pace ({dec(a.v_law / C_H, 3)} c_h, {dec(b.v_law / C_H, 3)} c_h):"
        f" A reads B {dec((1 - vb_law / C_H) / (1 + va_law / C_H))},"
        f" B reads A {dec((1 - va_law / C_H) / (1 + vb_law / C_H))},"
        f" the labs {dec(1 + va_law / C_H)} and {dec(1 + vb_law / C_H)}"
        f" (DESIGN.md section 3 at the declared momenta; under gravity the speeds grow)"
    )
    print(
        f"  the law's form at the identity's pace (no gamma anywhere): A reads B {dec(law_a)}, B reads A {dec(law_b)}"
    )
    t = contact_tick([a, b])
    t_law = 0
    while sum(math.floor(t_law * s.v_law) for s in (a, b)) < GAP:
        t_law += 1
    print(
        f"  the first contact without gravity: interval {t} under the identity (+-2, the two remainders),"
        f" {t_law} under the law (section 7 measured {258 if name == 'symmetric_pass' else '251 under gravity' if name == 'symmetric' else '254 under gravity'})"
    )

print()
print("The G2 session's 0.7794 for the mover of rest_frame, against the identity:")
world = json.loads((WORLDS / "rest_frame.json").read_text())
stars = {m["family"]: Star(m, world["width"]) for m in world["measured"] if m["family"].startswith("s_")}
a = stars["s_px1"]
law = 1 / (1 + a.v_law / C_H)
g_law = 1 / math.sqrt(1 - float(a.v_law / C_H) ** 2)
print(
    f"  the law's mover reading at its pace {dec(law)}; times gamma {law * g_law:.4f}; over gamma {law / g_law:.4f};"
)
print(
    f"  the identity's: by the tool {dec(1 / (1 + a.v / C_H))} (B at rest emits per interval; A's clicks per tick"
    f" the crossing rate), per A's own clock {dec(1 / ((1 + a.v / C_H) * a.gamma))}: none is 0.7794"
)

print()
print("The momenta that would keep the design's speeds under the identity (p c^2 / E = v, so")
print("p = Q S M v / sqrt(1 - 3 v^2), rounded), beside the declared ones (the pin is on the")
print("registered worlds, M2's rule):")
for v_c in (Fr(2, 10), Fr(4, 10)):
    v = v_c * C_H
    p_re = round(a.qsm * float(v) / math.sqrt(1 - 3 * float(v) ** 2))
    e_re = math.isqrt(a.qsm * a.qsm + 3 * p_re * p_re)
    print(
        f"  {dec(v_c, 1)} c_h: p = {p_re} (p c^2 / E = {dec(Fr(p_re, e_re), 5)} = {dec(Fr(p_re, e_re) / C_H, 4)} c_h)"
    )
