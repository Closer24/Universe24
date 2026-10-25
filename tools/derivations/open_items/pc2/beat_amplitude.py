"""pc2, item 3: the integers' floor on the beat: the one-Node line's period (intervals per upward crossing, thousandths) at the lay's amplitude A against the law's rotation, for the light lift (the electron: 1,076 intervals at den 1,655,909,141; 11,705 at the 54-bit den) and the heavy lift, at A = 14 (one quantum of the electron at T 36,000), 134 (the toy's A = root of T / 2), 10^4, 10^6, 10^9; the rational period from the law, 2 pi / omega with 1 - cos omega = (1 - num / den) (p_0 / Gamma)^2, given as the integer count the line converges to. Integers only."""
import sys, os, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.set_int_max_str_digits(0)
from event_universe.core.rule3 import wall_of, mass as mass_of
from event_universe.core import paces as E
MIL = 1000


def period(num, den, gamma, G, c, A, intervals):
    p0 = E.clock(gamma, c); w = wall_of(den, gamma, G); D = mass_of(num, den, p0, G)
    now, before, r = A, (A * num) // den, w // 2
    crossings = 0; first = last = None
    for t in range(intervals):
        total = (2 * w - D) * now - w * before + r; nxt = total // w; r = total - w * nxt
        if now < 0 <= nxt:
            crossings += 1
            if first is None: first = t
            last = t
        before, now = now, nxt
    return (last - first) * MIL // (crossings - 1) if crossings > 1 else None, crossings


out = {}
for den, lifts, tag in ((1655909141, (1655880909, 506298091), 'den 1,655,909,141'), (15162856759112389, (15162854575528411, 2458210083751875), 'den 54-bit')):
    for num in lifts:
        light = (den - num) * 100 < den
        for c in (0, 1000):
            row = {}
            for A in (14, 134, 10 ** 4, 10 ** 6, 10 ** 9):
                n = 3000000 if light else 60000
                row['A %d' % A] = period(num, den, 1000, 16, c, A, n)
            out['%s num %d content %d: period thousandths and crossings by amplitude' % (tag, num, c)] = row
for k, v in out.items(): print(json.dumps({k: v}))
