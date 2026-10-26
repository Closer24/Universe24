"""Hand ob1: the compact reading of an ob1_run.py output, integers only.
Usage: ob1_read.py <out.json> [every]
Prints per sampled interval each record's peak, centroid (milli Links), weight at the two centres and between, share (whole units),
W and P; then the credits' beats per record (counts), the running cosine pairs' counts, the summary (run back, bits, counts)."""
import sys, json
from collections import Counter, defaultdict

sys.set_int_max_str_digits(0)
run = json.load(open(sys.argv[1])); every = int(sys.argv[2]) if len(sys.argv) > 2 else 10
rows = run['rows']; s = run['summary']
print('WORLD', s['world'], 'singles', s['singles'], 'centres', s['centres'], 'between', s['between'])
marks = {0, 1, 2, 3, 5} | {k for k in range(0, len(rows), every)} | {len(rows) - 1}
for r in rows:
    if r['i'] not in marks: continue
    parts = []
    for k, v in sorted(r['records'].items()):
        parts.append('%s: peak %s cen %s wc %s wb %s share %s W %d P %s' % (k, v['peak'], v['centroid milli'], v['weight at centres'], v['weight between'], v['share (quotient, remainder) of unit'][0], v['W total'], v['P (lattice momentum)']))
    print('i %3d | light %s P %s | content %s | sign at centres %s | W board %d | %s' % (r['i'], r['light share (quotient, remainder) of W_c'][0], r['light P'], r['content min/max'], r['sign level at centres'], r['W board'], ' || '.join(parts)))
beats = defaultdict(Counter); cos = Counter(); nodes = defaultdict(Counter); n_cred = 0; sense_sum = 0
for c in run['credits']:
    n_cred += 1; sense_sum += c['sense']; beats[c['line']][c['beat']] += 1; nodes[c['line']][tuple(c['node'])] += 1
    cos[str([c['cos pair x2 axis %d (re)' % a] for a in range(3)])] += 1
print('CREDITS', n_cred, 'senses summed', sense_sum)
for line, cnt in sorted(beats.items()):
    print('  line %d beats (intervals per period: count) %s | credited Nodes %d, the most credited %s' % (line, dict(sorted(cnt.items())), len(nodes[line]), nodes[line].most_common(3)))
print('  running cosine pairs (re, x2) distinct', len(cos), 'the most common', cos.most_common(4))
births = [e for e in run['log'] if e['event'] == 'birth']
print('BIRTHS', len(births), 'senses summed', sum(x for b in births for x in b['senses']), 'taken >= booked', sum(1 for b in births if b['taken'] >= b['booked']), 'exact', sum(1 for b in births if b['taken'] == b['booked']))
print('SUMMARY run back %s | integers per Node %d | state bits %d | transient bits %d | counts %s' % (s['run back'], s['integers per Node'], s['max state bits'], s['max transient bits'], s['counts']))
