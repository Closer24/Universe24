"""(c) the control: David's lean_full.py and mv2's lean_mv2.py on one world with no wave number (and with wave [0, 0, 0]) compared bit for bit:
the state's bytes after the lay and after every interval, the lay lines' amplitude and share, the counts. Usage: python control_test.py <world_david.json> <world_wave0.json> <intervals>"""
import sys, os, json, hashlib
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, 'toy'))
import lean_full
sys.path.insert(0, HERE)
import lean_mv2

sys.set_int_max_str_digits(0)
n = int(sys.argv[3])
u1, w1 = lean_full.load_world(sys.argv[1]); u2, w2 = lean_mv2.load_world(sys.argv[2])
david = lean_full.Lean(u1, w1); mine0 = lean_mv2.Lean(u2, w1); mine = lean_mv2.Lean(u2, w2)


def h(b): return hashlib.sha256(b.state_bytes()).hexdigest()


same_lay = h(david) == h(mine0) == h(mine)
lays = [[{k: e[k] for k in ('amplitude', 'share', 'unit', 'nodes')} for e in b.log if e['event'] == 'lay'] for b in (david, mine0, mine)]
exact = 0
for t in range(n):
    david.step(); mine0.step(); mine.step()
    exact += (h(david) == h(mine0) == h(mine))
print(json.dumps({'state after the lay equal (david, mine with no wave key, mine with wave [0,0,0])': same_lay, 'lays': lays, 'intervals': n, 'states equal at every interval': exact, 'counts equal': david.counts == mine0.counts == mine.counts, 'counts': david.counts}))
