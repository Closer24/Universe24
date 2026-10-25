"""pc2: the flagged COPY of David's toy (tools/derivations/open_items/H-Paces-Law-Closed-2/toy/lean_full.py, never edited) as tools/derivations/open_items/H-Paces-Law-Closed-2/lean_carried.py, and the decoder's copy decoder_carried.py; every change listed here and checked to apply exactly once.
The flag: the world file's key control.clock = "carried" reads the carried clock (pc2_paces) in every place the toy reads paces.clock_of, link_pace_of, clock, link_pace, frozen_content, volume_of and level_of; off the key the copy is David's toy bit for bit (the same engine functions through pc2_paces).
Readings added (no act changed): the row's shape at the largest Rule3 transient; the light's share in quanta and the massless im line's size in the reader's row."""
import os, sys
here = os.path.dirname(os.path.abspath(__file__))
src = open(os.path.join(here, 'toy', 'lean_full.py')).read()
changes = [
    ("sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..', '..', 'src'))  # tools/derivations/toys/lean -> src",
     "sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..', 'src'))  # tools/derivations/open_items/H-Paces-Law-Closed-2 -> src (pc2's copy)\nsys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))"),
    ("from event_universe.core import rule3, paces\n", "from event_universe.core import rule3\nimport pc2_paces as paces  # pc2's flag: the carried clock behind control.clock = 'carried', the engine's memo otherwise\n"),
    ("from event_universe.features import volume as volform, phase\n", "from event_universe.features import phase\nvolform = paces  # the volume's two readings on the chosen clock (pc2_paces.volume_of, level_of)\n"),
    ("        ints = universe['integers']\n", "        paces.CARRIED = (world.get('control', {}).get('clock') == 'carried'); paces.clear_memo()  # pc2's flag, read once from the world file\n        ints = universe['integers']\n"),
    ("            if direction == 1: self.max_transient = max(self.max_transient, int(np.max(np.vectorize(lambda v: abs(int(v)).bit_length(), otypes=[object])(t))))\n",
     "            if direction == 1:\n                bits_here = int(np.max(np.vectorize(lambda v: abs(int(v)).bit_length(), otypes=[object])(t)))\n                if bits_here > self.max_transient: self.max_transient_where = (bits_here, getattr(self, '_row_shape', None), self.interval)  # pc2's reading: the row whose Rule3 total is the largest transient\n                self.max_transient = max(self.max_transient, bits_here)\n"),
    ("        return rule3.Rule(tuple(0 for _ in AXES), 2 * r.wall, r.wall, 0) if r.wall is not None else self.rule(r.pair, c, factors)\n",
     "        self._row_shape = r.shape  # pc2's reading: the row the next act steps\n        return rule3.Rule(tuple(0 for _ in AXES), 2 * r.wall, r.wall, 0) if r.wall is not None else self.rule(r.pair, c, factors)\n"),
    ("'light velocity max': light_v}\n",
     "'light velocity max': light_v, 'light share quanta max': light_q_max, 'nodes with light at or above one quantum': light_q_nodes, 'massless im abs max': im_abs, 'transient where (bits, row shape, interval)': list(getattr(b, 'max_transient_where', (0, None, 0)))}\n"),
    ("    W = Z(b.shape)\n    for re, im in planes: W = W + wronskian(re, im)\n",
     "    W = Z(b.shape)\n    for re, im in planes: W = W + wronskian(re, im)\n    light_share = b.share(massless, b.rule_of(b.row(2, gap=0), c, b.link_factors()), vacuum=True)  # pc2's reading: the massless row's share at the vacuum's weight, in its quanta W_c\n    light_q = [int(x) // b.unit_gap0 for x in light_share.reshape(-1)]; light_q_max = max(light_q); light_q_nodes = sum(1 for q in light_q if q >= 1)\n    im_abs = max(abs(int(x)) for x in b.row(2, gap=0).lines[1].now.reshape(-1))\n"),
]
for old, new in changes:
    n = src.count(old)
    if n != 1: raise SystemExit('a change applies %d times, not once: %r' % (n, old[:80]))
    src = src.replace(old, new)
src = src.replace('"""David\'s local lean Node, complete', '"""pc2\'s flagged COPY of David\'s lean toy (made by make_copy.py; the changes listed there; David\'s file untouched).\nDavid\'s local lean Node, complete', 1)
open(os.path.join(here, 'lean_carried.py'), 'w').write(src)
dec = open(os.path.join(here, 'toy', 'decoder_full.py')).read()
dchanges = [
    ("sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..', '..', 'src'))\nfrom event_universe.core import paces, rule3\n",
     "sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..', 'src'))\nsys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))\nfrom event_universe.core import rule3\nimport pc2_paces as paces  # pc2's flag: the record's own clock (its world file's control.clock)\n"),
    ("        self.run = run; self.den = int(run['den']); self.gamma, self.G, self.T = run['gamma'], run['G'], run['T']\n",
     "        self.run = run; self.den = int(run['den']); self.gamma, self.G, self.T = run['gamma'], run['G'], run['T']\n        paces.CARRIED = (run.get('world', {}).get('control', {}).get('clock') == 'carried'); paces.clear_memo()  # pc2: the decoder reads the record on the clock the record ran with\n"),
]
for old, new in dchanges:
    n = dec.count(old)
    if n != 1: raise SystemExit('a decoder change applies %d times, not once: %r' % (n, old[:80]))
    dec = dec.replace(old, new)
open(os.path.join(here, 'decoder_carried.py'), 'w').write(dec)
for name in ('cube48_test.py', 'runback_test.py', 'one_node_test.py', 'reach_test.py'):
    t = open(os.path.join(here, 'toy', name)).read()
    n = t.count('from lean_full import')
    if n != 1: raise SystemExit('%s imports lean_full %d times' % (name, n))
    t = t.replace('from lean_full import', 'from lean_carried import')
    open(os.path.join(here, name.replace('_test.py', '_carried.py')), 'w').write('# pc2: David\'s test on the flagged copy lean_carried.py (the import the one change)\n' + t)
print('copies written')
