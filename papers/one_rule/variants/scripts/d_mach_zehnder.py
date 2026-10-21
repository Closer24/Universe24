"""D. The delayed choice on the Mach-Zehnder in the law's algebra (README.md, section D; docs/ALGEBRA.md,
the rows against nature (l); The meeting's identity): the one-line form, the exits' shares 4 s (1 - s)
cos^2(Delta / 2) and one minus it at the arm difference Delta L Links at lambda = 8 (the row's 1, 0.854,
0.5, 0.146, 0), and the two-part form, the arms as the two parts of one record read at the exit side whose
basis is the second splitter's presence, (1, 1) in and (1, 0) out, the weights by
meeting_back.side_weights on the arms' second moments, exact in the integers; the Gram theorem's corollary
that the exit side's two weights are its own whatever a later side's basis (gram_of the identity for the
identity pattern).

    PYTHONPATH=src python papers/one_rule/variants/scripts/d_mach_zehnder.py
"""

from __future__ import annotations

import json
import math
import sys
from fractions import Fraction
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
sys.path.insert(0, str(ROOT / "src"))

from event_universe import meeting_back  # noqa: E402
from event_universe.loader.draw import ports_of  # noqa: E402

OUT = HERE.parent / "out"
IDENTITY = ((1, 0), (0, 1))
WAVELENGTH = 8  # the gates' wave, k = pi / 4
PERIODS = 4  # the window, in the band's periods
AMPLITUDE = 1000  # the arms' levels, integers


def one_line(s: Fraction, delta_links: int) -> tuple[float, float]:
    """The one-line form of row (l): the cross exit 4 s (1 - s) cos^2(Delta / 2), the straight exit one
    minus it."""
    delta = 2 * math.pi * delta_links / WAVELENGTH
    cross = 4 * float(s) * (1 - float(s)) * math.cos(delta / 2) ** 2
    return cross, 1 - cross


def arms_moments(delta_links: int) -> list[list[tuple[int, int]]]:
    """The two arms' second moments over a window of whole periods, as a side books them
    (credit.moments_booked: per interval the parts' level sums, now and before, M_kl = SUM sigma_k
    sigma_l): a plane wave of the rotation omega per interval at k = 2 pi / lambda on the lattice's band
    for light along an axis, cos omega = (2 + cos k) / 3, the second arm the first delayed by Delta L
    Links, the levels rounded to integers at the amplitude."""
    k = 2 * math.pi / WAVELENGTH
    omega = math.acos((2 + math.cos(k)) / 3)
    phase = k * delta_links
    steps = int(round(PERIODS * 2 * math.pi / omega))
    moments = [[0, 0], [0, 0]]
    for t in range(steps):
        for member in (0, 1):
            tau = t - member
            sigma = [
                int(round(AMPLITUDE * math.cos(omega * tau))),
                int(round(AMPLITUDE * math.cos(omega * tau - phase))),
            ]
            for a in range(2):
                for b in range(2):
                    moments[a][b] += sigma[a] * sigma[b]
    return [[(moments[a][b], 0) for b in range(2)] for a in range(2)]


def main() -> None:
    report: dict[str, object] = {}
    s = Fraction(1, 2)
    report["one_line_form_s_half"] = {
        f"Delta L = {d}": {"cross": round(one_line(s, d)[0], 4), "straight": round(one_line(s, d)[1], 4)}
        for d in range(5)
    }
    rows = {}
    all_ones = meeting_back.gram_of([], 2)
    identity_gram = meeting_back.gram_of([IDENTITY], 2)
    for d in range(5):
        moments = arms_moments(d)
        bs_in = [list(p) for p in ports_of((1, 1), IDENTITY)]  # in: the exit side mixes the arms
        bs_out = [list(p) for p in ports_of((1, 0), IDENTITY)]  # out: the exits read the arms
        w_in = meeting_back.side_weights(moments, bs_in, all_ones)
        w_out = meeting_back.side_weights(moments, bs_out, all_ones)
        # a later side leaves this side's weights its own: the identity pattern's Gram is the identity,
        # so the exit side's marginal with a side after it is M11 + M22 at either port of (1, 1)
        w_first = meeting_back.side_weights(moments, bs_in, identity_gram)
        rows[f"Delta L = {d}"] = {
            "BS2 in, (1, 1): P(cross), P(straight)": [
                round(w_in[0] / sum(w_in), 4),
                round(w_in[1] / sum(w_in), 4),
            ],
            "BS2 out, (1, 0): P(arm 1), P(arm 2)": [
                round(w_out[0] / sum(w_out), 4),
                round(w_out[1] / sum(w_out), 4),
            ],
            "sum of the exit side's weights, in and out": [sum(w_in), sum(w_out)],
            "the exit side with a side after it (Gram identity), either port": w_first,
        }
    report["two_part_form"] = rows
    report["splitter"] = {
        "the one-Node splitter's content for s = 1/2 at k = pi/4 (row (l))": (
            "U = 0.2294, 1,376 of Gamma = 6,000 under the linear Link pace; 0.3070 under the composed paces"
        ),
    }
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "d_mach_zehnder.json").write_text(json.dumps(report, indent=1), encoding="utf-8")
    print(json.dumps(report, indent=1))


if __name__ == "__main__":
    main()
