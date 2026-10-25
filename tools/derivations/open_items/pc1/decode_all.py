"""pc1: the toy's decoder run on every record (no shell loop), the gates kept beside each record as .gates.jsonl; the memo and the carried forms' gates compared line by line."""
import sys, os, subprocess, json, glob
HERE = os.path.dirname(os.path.abspath(__file__))
dec = os.path.join(HERE, 'toy_pc1', 'decoder_full.py')
found = {}
for rec in sorted(glob.glob(os.path.join(HERE, 'out', 'records*', '*.json'))):
    if rec.endswith('records_summary.json'): continue
    out = rec[:-5] + '.gates.jsonl'
    r = subprocess.run([sys.executable, dec, rec], capture_output=True, text=True)
    open(out, 'w').write(r.stdout + r.stderr)
    found[os.path.basename(rec)] = out
pairs = [('world_toy_60_memo', 'world_toy_60_scaled'), ('world_chiral_300_memo', 'world_chiral_300_scaled'), ('world_bodies_120_memo', 'world_bodies_120_scaled')]
for a, b in pairs:
    ga = open(os.path.join(HERE, 'out', 'records', a + '.gates.jsonl')).read(); gb = open(os.path.join(HERE, 'out', 'records', b + '.gates.jsonl')).read()
    print(json.dumps({'gates identical memo vs scaled': [a, ga == gb]}))
for a, b in [('world_toy_60_plain', 'world_toy_60_memo'), ('world_chiral_300_plain', 'world_chiral_300_memo'), ('world_bodies_120_plain', 'world_bodies_120_memo')]:
    ga = open(os.path.join(HERE, 'out', 'records_plain', a + '.gates.jsonl')).read().splitlines(); gb = open(os.path.join(HERE, 'out', 'records_plain', b + '.gates.jsonl')).read().splitlines()
    print(json.dumps({'gates differing plain vs memo': [a, sum(1 for x, y in zip(ga, gb) if x != y), len(ga)]}))
