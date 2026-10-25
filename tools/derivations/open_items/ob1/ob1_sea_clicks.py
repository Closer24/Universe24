"""Hand ob1: the sea's clicks on the engine's hole seed, read from the credit lines alone, in integers (2026-10-25).

Usage: ob1_sea_clicks.py <clicks.jsonl>   (the N1 record tools/derivations/open_items/n1/run300_697786.clicks.jsonl:
the engine's hole seed on the 3-cube at den 697,786, 300 intervals, the credits with the law's momentum key [sign, num, den]
per axis, the beat, the sense, the point, the take's numbers).
Read: the momentum signs summed per axis over every credit (the lattice momentum in the clicks, 0 on the 48-symmetric seed),
the running cosine's pairs per axis (the orbit of the 48 on them), the senses summed over the births (the charge), the take's
identity taken = walls + excess on every line, the light credits' beats against the Node's proper count (the beat per proper
interval, the energy in the clicks), and the body credits' beats (None on this engine, D-S2 the lack).
"""
import sys, json
from collections import Counter

sys.set_int_max_str_digits(0)
lines = [json.loads(l) for l in open(sys.argv[1]) if l.strip()]
credits = [l for l in lines if l.get('event') == 'credit']
births = [l for l in lines if l.get('event') == 'birth']
out = {'lines': len(lines), 'credits': len(credits), 'births': len(births), 'lays': sum(1 for l in lines if l.get('event') == 'lay'), 'refused': sum(1 for l in lines if l.get('event') == 'refused')}
signs = [0, 0, 0]; pairs = Counter(); senses = Counter(); kinds = Counter(); beats = Counter(); beat_none = 0; momentum_none = 0
for c in credits:
    m = c.get('momentum')
    if not m: momentum_none += 1
    else:
        for a in range(3):
            signs[a] += int(m[a][0]); pairs[str(m[a][1:])] += 1
    senses[c.get('sense')] += 1; kinds[str(c.get('kind'))] += 1
    b = c.get('beat')
    if b is None: beat_none += 1
    else: beats[int(b)] += 1
out['momentum signs summed per axis over the credits'] = signs
out['credits without a momentum key'] = momentum_none
out['running cosine pairs (the orbit of the 48: equal counts per orbit)'] = dict(pairs.most_common(12))
out['senses over the credits'] = dict(senses)
out['kinds'] = dict(kinds)
out['beats (W_c sin omega) with their counts'] = dict(beats.most_common(8))
out['credits with the beat None (a body credit without a beat: D-S2 the lack)'] = beat_none
# the births: the charge and the take
sense_sum = 0; identity = 0; exact = 0; walls_sum = 0; taken_sum = 0; excess_sum = 0
for b in births:
    sense_sum += sum(int(s) for s in b.get('senses', []))
    t, w, e = b.get('taken'), b.get('walls'), b.get('excess')
    if t is not None and w is not None and e is not None:
        tt = int(t) if not isinstance(t, list) else sum(int(x) for x in t)
        ww = int(w) if not isinstance(w, list) else sum(int(x) for x in w)
        ee = int(e) if not isinstance(e, list) else sum(int(x) for x in e)
        identity += (tt == ww + ee); exact += (ee == 0); walls_sum += ww; taken_sum += tt; excess_sum += ee
out['births: the senses summed'] = sense_sum
out['births: taken = walls + excess'] = [identity, len(births)]
out['births: exact (excess 0)'] = [exact, len(births)]
out['births: taken, walls, excess summed'] = [taken_sum, walls_sum, excess_sum]
# the energy in the clicks: the light credits' beat against the Node's proper count per interval (the beat per proper interval)
light = [c for c in credits if c.get('beat') is not None]
by_node = Counter(tuple(c['node_detector']) if isinstance(c.get('node_detector'), list) else c.get('node_detector') for c in light)
out['light credits with a beat'] = len(light)
out['light credits per Node (the first eight)'] = {str(k): v for k, v in by_node.most_common(8)}
# the proper counts at the light credits against the interval: the clock's reading per Node
props = sorted({(c['interval'], c.get('proper')) for c in light})
out['light credits (interval, proper) distinct pairs (the first twelve)'] = props[:12]
for k, v in out.items(): print(json.dumps({k: v}))
