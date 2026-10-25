"""mv1 (c): the control. David's toy (toy/lean_full.py, untouched) against the flagged copy on the same world without `wave`, and the copy's wave [0, 0, 0] in the plain and the exact form: the state's hash at the lay and after 20 intervals, bit for bit or the count of Node-lines apart."""
import sys, os, json, hashlib
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'toy'))
sys.set_int_max_str_digits(0)
import numpy as np
import lean_full, lean_mv1
HERE = os.path.dirname(os.path.abspath(__file__))
UNI = json.load(open(os.path.join(HERE, 'toy', 'universe_middle.json')))
base = {"universe": "universe_middle.json", "shape": [9, 9, 9], "intervals": 20, "seed": [{"lay": "sea", "row": 0}, {"lay": "at", "row": 1, "centre": [2, 4, 4], "width": 2, "quanta": 125}]}
def with_wave(w):
    w2 = json.loads(json.dumps(base)); w2['seed'][1]['wave'] = [0, 0, 0]; return w2
def apart(a, b):
    n = 0
    for la, lb in zip(a.all_lines(), b.all_lines()):
        for x, y in ((la.now, lb.now), (la.before, lb.before), (la.rem, lb.rem)):
            n += int(sum(1 for u, v in zip(x.reshape(-1), y.reshape(-1)) if int(u) != int(v)))
    return n
david = lean_full.Lean(UNI, base); copy_nowave = lean_mv1.Lean(UNI, base)
lean_mv1.PLAIN_LAY = True; copy_w0_plain = lean_mv1.Lean(UNI, with_wave(base))
lean_mv1.PLAIN_LAY = False; copy_w0_exact = lean_mv1.Lean(UNI, with_wave(base))
out = {'at the lay': {'david': david.state_hash(), 'copy no wave': copy_nowave.state_hash(), 'copy wave0 plain': copy_w0_plain.state_hash(), 'copy wave0 exact': copy_w0_exact.state_hash(),
       'node-lines apart (david vs copy no wave)': apart(david, copy_nowave), 'apart (david vs wave0 plain)': apart(david, copy_w0_plain), 'apart (david vs wave0 exact)': apart(david, copy_w0_exact)}}
for b in (david, copy_nowave, copy_w0_plain, copy_w0_exact):
    for _ in range(20): b.step()
out['after 20'] = {'david': david.state_hash(), 'copy no wave': copy_nowave.state_hash(), 'copy wave0 plain': copy_w0_plain.state_hash(), 'copy wave0 exact': copy_w0_exact.state_hash(),
       'node-lines apart (david vs copy no wave)': apart(david, copy_nowave), 'apart (david vs wave0 plain)': apart(david, copy_w0_plain), 'apart (david vs wave0 exact)': apart(david, copy_w0_exact),
       'david counts': dict(david.counts), 'wave0 exact counts': dict(copy_w0_exact.counts)}
out['lays'] = {'david': [e for e in david.log if e['event'] == 'lay'], 'wave0 plain': [e for e in copy_w0_plain.log if e['event'] == 'lay'], 'wave0 exact': [e for e in copy_w0_exact.log if e['event'] == 'lay']}
json.dump(out, open(os.path.join(HERE, 'out', 'control_hash.json'), 'w'), default=str); print(json.dumps(out, default=str))
