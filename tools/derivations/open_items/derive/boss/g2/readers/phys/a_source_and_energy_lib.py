"""The one-site integer replica of the first-order form under t13_probe's energy source, for checks A and B
(check A verifies it against n2b_lib.tick_first bit for bit).

Clock: one Node-clock: the hand, its 00 slot, its ii slots.
Algebra: Python integers and Rule3's carry.
Board: one site, no Meshes.
Clicks: n/a.
"""

import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE / "copy" / "n2_second"))

from n2b_lib import carry  # noqa: E402

REST, GRIP, G, TD = 3000, 500, 210, 1000


def tick1(x, exact=False):
    a5, p5, c00, p00, rd00, ii, pii, rdii = x
    w = REST + c00
    sb, _ = carry(p5, w, 0)
    q5 = -G * a5
    pa = p5 + q5
    sa, _ = carry(pa, w, 0)
    floor_part = 2 * w * (sb * sb + sa * sa)
    exact_part, _ = carry(2 * (p5 * p5 + pa * pa), w, 0)
    j00 = -2 * G * a5 * a5 + (exact_part if exact else floor_part)
    jii = 2 * G * a5 * a5
    q00, rd00n = carry(j00, TD, rd00)
    qii, rdiin = carry(jii, TD, rdii)
    p5n, p00n, piin = pa, p00 + q00, pii + qii
    a5n = a5 + carry(p5n, w, 0)[0]
    c00n = c00 + carry(p00n, REST, 0)[0]
    iin = ii + carry(piin, w, 0)[0]
    return (a5n, p5n, c00n, p00n, rd00n, iin, piin, rdiin), (j00, floor_part - exact_part, sb, sa, w)
