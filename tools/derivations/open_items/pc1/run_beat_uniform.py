"""pc1, item 3: the beat of a body in a UNIFORM held content (the toy's control well with a radius past the board, held), so that the clock's effect on the beat stands apart from the self-made well: four worlds at the contents 0, 500, 1000, 2000 on the 7-cube with the sea and one body of 125 quanta of the heavy lift, 120 intervals; the records' credits' beats against the law's rest line at that content (pc1_beat.py).
Usage: python run_beat_uniform.py <out_dir>"""
import sys, os, json, subprocess
HERE = os.path.dirname(os.path.abspath(__file__)); TOY = os.path.join(HERE, 'toy_pc1')
out_dir = sys.argv[1]; os.makedirs(out_dir, exist_ok=True)
found = {}
for c in (0, 500, 1000, 2000):
    world = {"universe": "universe_middle.json", "shape": [7, 7, 7], "intervals": 120, "seed": [{"lay": "sea", "row": 0}, {"lay": "at", "row": 2, "centre": [3, 3, 3], "width": 2, "quanta": 125}], "control": {"well": {"at": [3, 3, 3], "levels": c, "radius": 100, "held": True}}}
    path = os.path.join(TOY, 'pc1_uniform_%d.json' % c); json.dump(world, open(path, 'w'))
    rec = os.path.join(out_dir, 'uniform_%d.json' % c)
    r = subprocess.run([sys.executable, os.path.join(TOY, 'lean_full.py'), path, rec, 'back', '5'], capture_output=True, text=True, env=dict(os.environ, PC1_CLOCK='memo'))
    if r.returncode != 0: print(r.stderr[-1500:]); continue
    b = subprocess.run([sys.executable, os.path.join(HERE, 'pc1_beat.py'), rec, rec[:-5] + '.beat.json'], capture_output=True, text=True)
    R = json.load(open(rec)); B = json.load(open(rec[:-5] + '.beat.json'))
    found[c] = {'counts': R['counts'], 'run_back': R['run_back'], 'contents at the credits': B['contents at the credits (min, max)'], 'beats measured': B['beats measured (beat: count)'], 'measured among predicted': [B['credits with the measured beat among the law line predicted spacings'], B['credits with the measured beat outside them']], 'factor table': B['the beat factor against the clock factor at the credits contents'][:3]}
    print(json.dumps({c: found[c]}), flush=True)
json.dump(found, open(os.path.join(out_dir, 'uniform_summary.json'), 'w'), indent=1)
