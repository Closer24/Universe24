"""pc2, item 3: the beat of a standing record at a Node of content c from the law's own line (Rule3's one-Node step at the pair's coefficients and the Node's paces, the neighbours equal: a_next + a_before = (2 - D / w) a_now with D = 12 (den - num) p_0^2 G^2 and w = 6 den Gamma^2 G^2, so 1 - cos omega_c = (1 - num / den) (p_0 / Gamma)^2), run in integers with the carried remainder, the beat read as intervals per upward crossing over a long run (the law's own reading, no acos): B(c) in thousandths of an interval; in proper time B(c) p_0(c) / Gamma against B(0) (the clocks shift alike to first order; the second order the term); the beat's dilation factor B(c) / B(0) against the clock's Gamma / p_0(c) (G-S3's gap); then the measured beats of the bodies' record by content (the credit's 'beat' and 'content'), and the light lift's beat at the 54-bit den (11,705).
Usage: PYTHONPATH=src python beat_law.py <bodies record.json> > out. Integers only."""
import sys, os, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.set_int_max_str_digits(0)
from collections import defaultdict
import pc2_paces as P
from event_universe.core import paces as E
from event_universe.core.rule3 import wall_of, mass as mass_of, largest_below

MIL = 1000


def standing_beat(num, den, gamma, G, c, intervals, carried=False):
    """Intervals per upward crossing of the one-Node line at the content c, in thousandths: the law's beat B(c), and the count of crossings."""
    p0 = P.carried_clock(gamma, c) if carried else E.clock(gamma, c)
    w = wall_of(den, gamma, G); D = mass_of(num, den, p0, G)
    A = largest_below(36000 // 2)  # the lay's amplitude (the toy's A), the start at the rest rotation of the vacuum: any start gives the same count to one crossing
    now, before, r = A, (A * num) // den, w // 2
    crossings = 0; first = None; last = None
    for t in range(intervals):
        total = (2 * w - D) * now - w * before + r
        nxt = total // w; r = total - w * nxt
        if now < 0 <= nxt:
            crossings += 1
            if first is None: first = t
            last = t
        before, now = now, nxt
    span = (last - first) if crossings > 1 else None
    return (span * MIL // (crossings - 1) if span else None), crossings, p0


def first_beats(num, den, gamma, G, c, intervals, n=6):
    """The first n crossing intervals (the integer beats as the toy counts them) at a content: the staircase of the rounding."""
    p0 = E.clock(gamma, c); w = wall_of(den, gamma, G); D = mass_of(num, den, p0, G)
    A = largest_below(36000 // 2); now, before, r = A, (A * num) // den, w // 2
    found = []; last = None
    for t in range(intervals):
        total = (2 * w - D) * now - w * before + r; nxt = total // w; r = total - w * nxt
        if now < 0 <= nxt:
            if last is not None: found.append(t - last)
            last = t
            if len(found) >= n: break
        before, now = now, nxt
    return found


out = {}
rec = json.load(open(sys.argv[1])); gamma, G, den = int(rec['gamma']), int(rec['G']), int(rec['den'])
planes = [int(x) for x in rec['planes']]
lifts = [n for n in planes if n != den]
heavy = min(lifts); light = max(lifts)
out['record: den, Gamma, G, the lifts (num), heavy, light'] = [den, gamma, G, lifts, heavy, light]
for name, num in (('heavy', heavy), ('light', light)):
    rows = []
    B0 = None
    for c in (0, 100, 200, 300, 500, 800, 1000, 1500, 2000, 2500, 3000):
        b, cr, p0 = standing_beat(num, den, gamma, G, c, 200000 if num == heavy else 400000)
        if c == 0: B0 = b
        if b is None: rows.append([c, p0, None]); continue
        proper_beat = b * p0 // gamma  # B(c) p_0 / Gamma in thousandths: the beat in the Node's proper intervals (Gamma = one interval at the vacuum)
        beat_factor = b * MIL // B0  # B(c) / B(0) in thousandths
        clock_factor = gamma * MIL // p0  # Gamma / p_0 in thousandths
        rows.append({'content': c, 'p0': p0, 'B(c) thousandths of an interval': b, 'crossings': cr, 'B(c) p0 / Gamma (proper beat) thousandths': proper_beat, 'B(c)/B(0) thousandths': beat_factor, 'Gamma/p0 thousandths': clock_factor, 'first integer beats (the staircase)': first_beats(num, den, gamma, G, c, 20000)})
    out['law: standing beat of the %s lift (num %d) by content' % (name, num)] = rows
# the measured beats of the record's credits by content
by_c = defaultdict(list); by_i = []
for e in rec['log']:
    if e['event'] == 'credit' and e['beat'] > 0:
        by_c[(e['content'] // 250) * 250].append((e['beat'], e['line'])); by_i.append((e['i'], tuple(e['node']), e['line'], e['content'], e['beat'], e.get('sign_level'), e['proper']))
bins = {}
for k in sorted(by_c):
    bs = [b for b, _l in by_c[k]]
    bins[k] = {'credits': len(bs), 'beats min/max': [min(bs), max(bs)], 'mean beat thousandths': sum(bs) * MIL // len(bs), 'law standing beat at the bin (thousandths)': standing_beat(heavy, den, gamma, G, k, 100000)[0], 'law standing beat at the bin + 250': standing_beat(heavy, den, gamma, G, k + 250, 100000)[0]}
out['measured: the credits\' beats by content bin (250 wide), against the law\'s standing beat of the heavy lift'] = bins
out['measured: the first 24 credits (interval, node, line, content, beat, sign level, proper)'] = by_i[:24]
out['measured: the last 12 credits'] = by_i[-12:]
# the proper spacing of successive credits of one line at one Node: the beat in proper units (proper per credit) against the interval spacing
tracks = defaultdict(list)
for e in rec['log']:
    if e['event'] == 'credit': tracks[(tuple(e['node']), e['line'])].append((e['i'], e['proper'], e['content'], e['beat']))
spac = []
for key, cs in tracks.items():
    cs.sort()
    for (i1, p1, c1, b1), (i2, p2, c2, b2) in zip(cs, cs[1:]):
        if i2 > i1: spac.append((i2 - i1, p2 - p1, c2, b2))
if spac:
    out['tracks: successive credits of one line at one Node: count; interval spacing min/middle/max; proper spacing min/middle/max; proper per interval over all (thousandths); the clock p0 at the middle content'] = [len(spac), [min(s[0] for s in spac), sorted(s[0] for s in spac)[len(spac) // 2], max(s[0] for s in spac)], [min(s[1] for s in spac), sorted(s[1] for s in spac)[len(spac) // 2], max(s[1] for s in spac)], sum(s[1] for s in spac) * MIL // sum(s[0] for s in spac), E.clock(gamma, sorted(s[2] for s in spac)[len(spac) // 2])]
# the light lift at the 54-bit den (universe_toy): the beat at the vacuum, 11,705, and at contents 100 and 1000
den54 = 15162856759112389; lifts54 = [15162854575528411, 2458210083751875, 2580388913625285]
for num in lifts54:
    b0, cr0, _ = standing_beat(num, den54, gamma, G, 0, 2000000 if num == lifts54[0] else 100000)
    out['54-bit den lift num %d: B(0) thousandths, crossings' % num] = [b0, cr0]
b1, _, p1 = standing_beat(lifts54[0], den54, gamma, G, 1000, 4000000)
out['54-bit den light lift at content 1000: B thousandths, p0, B p0 / Gamma, B(1000)/B(0) against Gamma/p0 (thousandths)'] = [b1, p1, b1 * p1 // gamma, [b1 * MIL // out['54-bit den lift num %d: B(0) thousandths, crossings' % lifts54[0]][0], gamma * MIL // p1]]
# the carried clock against the memo on the beat: at the contents where the two differ (584, 1267 at Gamma 1000), the standing beat on each
for c in (584, 1267):
    out['beat at content %d on the memo clock and on the carried clock (thousandths), the clocks' % c] = [standing_beat(heavy, den, gamma, G, c, 100000)[0], standing_beat(heavy, den, gamma, G, c, 100000, carried=True)[0], E.clock(gamma, c), P.carried_clock(gamma, c)]
for k, v in out.items(): print(json.dumps({k: v}))
