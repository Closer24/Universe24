"""The one rule of the remainder on the clock, measured on David's pre-fold toy: the paces' two functions of the content replaced, in the toy's own `paces` module at run time (no file of src edited), by the merged engine's K-S4 form (engine-5.0-test d752d586f, core/paces.py: one carried division per content from the half wall, the Link's pace the clock's square over Gamma rounded once), against David's exact power rounded once per content (a fresh half-wall birth each content). The two toys run side by side on one world; the state hash per interval, the first interval apart, the counts, the contents at which the two clocks differ.
Usage: python fd2_clock_rule.py <world.json>"""
import sys, os, json, importlib.util
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); sys.set_int_max_str_digits(0)
from event_universe.core import paces as P, rule3
from event_universe.core.paces import rounded, clock_alone

def carried_tables(gamma, top):
    clocks = []; links = []; p, r = gamma, gamma // 2
    for c in range(top + 1):
        clocks.append(p); links.append(int(rounded(p * p, gamma)))
        q, r = rule3.carried_division(p * (gamma - 1), gamma, r, 1); p = q
    return clocks, links

def load(name):
    spec = importlib.util.spec_from_file_location(name, os.path.join(HERE, 'toy_david', 'lean_full.py')); mod = importlib.util.module_from_spec(spec); spec.loader.exec_module(mod); return mod

world_path = sys.argv[1]
david = load('lean_david'); other = load('lean_clock')
universe, world = david.load_world(world_path); gamma = int(universe['integers']['node_clock'])
top = P.frozen_content(gamma) + 1
clocks, links = carried_tables(gamma, top)
exact = [clock_alone(gamma, c) for c in range(top + 1)]
diff_c = [c for c in range(top + 1) if clocks[c] != exact[c]]
def table_lookup(table):
    def f(g, contents):
        v = np.asarray(contents)
        if v.ndim == 0: return table[abs(int(v))] if int(v) >= 0 else int(P.clock_of(g, int(v)) if table is clocks else P.link_pace_of(g, int(v)))
        out = np.empty(v.shape, dtype=object)
        for idx in np.ndindex(*v.shape):
            c = int(v[idx]); out[idx] = (table[c] if c >= 0 else int((P.clock_of if table is clocks else P.link_pace_of)(g, c)))
        return out
    return f
# the patched module: the copy's `paces` name bound to a shim with the carried tables (the hills, c < 0, left as David's: no hill below 0 is a hollow's content)
class Shim:
    def __getattr__(self, k): return getattr(P, k)
shim = Shim(); shim.clock_of = table_lookup(clocks); shim.link_pace_of = table_lookup(links)
shim.clock = lambda g, c: clocks[c] if c >= 0 else P.clock(g, c); shim.link_pace = lambda g, c: links[c] if c >= 0 else P.link_pace(g, c)
other.paces = shim
n = int(world['intervals']); a = david.Lean(universe, world); b = other.Lean(universe, world)
equal = 0; first = None; contents_seen = set()
for t in range(n):
    a.step(); b.step()
    contents_seen |= set(int(x) for x in np.asarray(a.start_content).reshape(-1))
    if a.state_hash() == b.state_hash(): equal += 1
    elif first is None: first = t + 1
met = sorted(c for c in diff_c if c in contents_seen)
print(json.dumps({'world': os.path.basename(world_path), 'Gamma': gamma, 'contents where the carried clock parts from the exact power (clock)': diff_c, 'of them met on David\'s board in this run': met, 'intervals': n, 'state hash equal': [equal, n], 'first interval apart': first, 'counts David': {k: str(v) for k, v in a.counts.items()}, 'counts carried clock': {k: str(v) for k, v in b.counts.items()}, 'log equal': json.dumps(a.log, sort_keys=True) == json.dumps(b.log, sort_keys=True)}))
