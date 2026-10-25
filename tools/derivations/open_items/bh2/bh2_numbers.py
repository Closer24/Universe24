"""bh2: the integers of the frozen Node at Gamma 1,000 (ALGEBRA.md The paces, The line, The bound): the frozen content (the Link's pace 0), the clock there, the clock's last pace and its content, X at each, Rule3's integers at the frozen content per row (R = 0, D, S, w), the one-Node rotation 2 cos omega per row as a rational and its period in intervals, the write's numerator at the clock's zero, and the width budget: bits(w) at the three dens and the largest X and content that keep w X within 128 bits. Integers only. Usage: python bh2_numbers.py"""
import json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, 'src_e5', 'src'))
import numpy as np
from event_universe.core import paces, rule3
from event_universe.features import volume
from event_universe.rows import TRACE

sys.set_int_max_str_digits(0)
G = 1000
out = {}
fc = paces.frozen_content(G)
out['frozen content (the Link pace 0)'] = fc
out['clock p_0 at the frozen content, one above, one below'] = [paces.clock(G, fc), paces.clock(G, fc + 1), paces.clock(G, fc - 1)]
out['Link pace at fc - 1, fc'] = [paces.link_pace(G, fc - 1), paces.link_pace(G, fc)]
cz = volume.clock_zero(G)
out['clock zero (first content with p_0 = 0), the clock at cz - 1'] = [cz, paces.clock(G, cz - 1), paces.clock(G, cz)]
first_one = next(c for c in range(fc, cz) if paces.clock(G, c) == 1)
out['first content with the clock 1 (the last pace), and its span'] = [first_one, cz - 1]
xv = lambda c: int(volume.volume_of(G, np.array([c], dtype=object))[0])
out['X at the vacuum, at fc, at the first clock 1, at cz - 1 (value, bits)'] = [[xv(c), xv(c).bit_length()] for c in (0, fc, first_one, cz - 1)]
out['the level read back from X(fc), X(cz-1)'] = [int(volume.level_of(G, np.array([xv(fc)], dtype=object))[0]), int(volume.level_of(G, np.array([xv(cz - 1)], dtype=object))[0])]
out['the level read at X = 2^60, 2^80 (the reading rests at the last pace)'] = [int(volume.level_of(G, np.array([2 ** 60], dtype=object))[0]), int(volume.level_of(G, np.array([2 ** 80], dtype=object))[0])]
dens = {'54-bit (universe_toy)': 15162856759112389, 'middle (universe_middle)': 1655909141, 'record (owner, HIGHLIGHTS)': 3311818282, 'cheap (owner)': 697786}
unit = rule3.link_unit_of(G)
out['G derived'] = unit
budget = {}
for name, den in dens.items():
    w = rule3.wall_of(den, G, unit)
    # Rule3's total at a Node is at least w X on the carrier's line (the -w a_before term): the largest X with bits(w X) <= 128 is X < 2^128 / w
    xmax = (2 ** 128) // w
    # the content at which X(c) first exceeds xmax
    c = 0
    while c < cz - 1 and xv(c) <= xmax:
        c += 1
    budget[name] = {'den bits': den.bit_length(), 'w bits': w.bit_length(), 'largest X with w X within 128 bits (bits)': xmax.bit_length(), 'first content whose X breaks 128 bits on w X (None: never, the last pace within)': (c if xv(c) > xmax else None), 'X(fc) bits + w bits': xv(fc).bit_length() + w.bit_length(), 'X(cz-1) bits + w bits': xv(cz - 1).bit_length() + w.bit_length()}
out['the width budget'] = budget
# Rule3's integers at the frozen content per row of the 54-bit universe
uni = json.load(open(os.path.join(HERE, 'worlds', 'universe_toy.json')))
den = uni['integers']['den']
rows = {}
for c in (fc, first_one, cz - 1):
    clock, pace = paces.clock(G, c), paces.link_pace(G, c)
    for r in uni['rows']:
        if 'pair' not in r:
            continue
        num = r['pair'][0]
        rl = rule3.rule_integers(num, den, G, clock, pace, None, unit)
        D, w = rl.mass, rl.wall
        # 2 cos omega = (2 w - D) / w; the period: the least integer n with n omega >= 2 pi, read as the integer part of 2 pi / omega with omega from 1 - cos omega = D / (2 w): omega^2 ~ D / w for small omega: period ~ 2 pi sqrt(w / D): computed as the integer root of 4 pi^2 w / D with pi^2 as 9,870 / 1,000 (an integer reading)
        period = None if D == 0 else rule3.largest_below((4 * 9870 * w) // (1000 * D))
        rows[f'content {c}, row shape {r["shape"]} gap {den - num}'] = {'p_0': clock, 'p_i': pace, 'R per Port': int(rl.reaches[0]), 'D bits': D.bit_length(), 'D over w in parts per 10^9': (D * 10 ** 9) // w, 'S equals 2 w - D': rl.self_coefficient == 2 * w - D, 'period of the one-Node rotation (intervals, integer root)': period}
out['Rule3 at the frozen Node per row (R = 0 everywhere; D the clock twice)'] = rows
# the write's numerator: 4 X (forms 54 den Gamma^2 - trace p_0^2) p_0: 0 iff p_0 = 0 (never read: the last pace is 1); at the last pace the factor X p_0 against the vacuum's X p_0
out['write factor X p_0: vacuum, fc, last pace (bits)'] = [(xv(0) * paces.clock(G, 0)).bit_length(), (xv(fc) * paces.clock(G, fc)).bit_length(), (xv(cz - 1) * 1).bit_length()]
out['write numerator at p_0 = 0 with X = 2^60 and forms = 10^6'] = rule3.held_numerator(TRACE, 2 ** 60, 10 ** 6, 0, 0, den, G)
json.dump(out, open(os.path.join(HERE, 'out', 'bh2_numbers.json'), 'w'), indent=1)
for k, v in out.items():
    print(k, ':', v)
