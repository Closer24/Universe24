"""bb1's probe of the spread's growth from the least inhomogeneity: the sea plus A levels at the centre, run N intervals
in-process; per interval the carrier's X (min, max at the centre), the gap-0 line's level now and velocity (now - before)
at the centre and at a far Node, the forms' min and max, the write's min and max, the Link factors' min, the turns.
Usage: probe_growth.py <world.json> <A> <N>"""
import json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "..", "src"))
import numpy as np
from event_universe import interval as interval_module
from event_universe.core.rule3 import held_numerator, quotient
from event_universe.loader.world import load_world
from event_universe.node import Node
from event_universe.rows import PLANE, TRACE, CARRIER

sys.set_int_max_str_digits(0)
universe, world = load_world(sys.argv[1])
amp, n = int(sys.argv[2]), int(sys.argv[3])
node = Node(universe, world)
rec = node.records().index(node.row(PLANE, gap=0))
centre = (node.cube // 2,) * 3
far = (0, 0, 0)
if amp:
    node.lay(rec, centre, (amp, 0, 0, 0))
probe = {}
class P(interval_module.Interval):
    def carrier_act(self):
        if self.direction == 1:
            x = self.x_now
            line = self.rows[self.where[id(self.carrier)]][0]
            numerator = held_numerator(TRACE, x, self.forms, self.trace, self.p0, node.den, node.gamma)
            write = (numerator + line.wr) // line.wwall
            f = self.forms
            probe.update(forms_min=int(f.min()), forms_max=int(f.max()), forms_centre=int(f[centre]), forms_far=int(f[far]),
                         write_min=int(write.min()), write_max=int(write.max()), q_min=int(min(int(v) for fa in self.factors for v in fa.reshape(-1))),
                         trace_max=int(self.trace.max()))
        super().carrier_act()
interval_module.Interval = P
print("i | X centre, min, max | gap0 now centre, far | v centre, far | forms min, max | write min, max | Q min | trace max | turned")
for i in range(n):
    node.step()
    X = node.row(CARRIER).lines[0].now
    z = node.row(PLANE, gap=0).lines[0]
    v = z.now - z.before
    print(node.interval, "|", int(X[centre]), int(X.min()), int(X.max()), "|", int(z.now[centre]), int(z.now[far]), "|", int(v[centre]), int(v[far]), "|",
          probe["forms_min"], probe["forms_max"], "|", probe["write_min"], probe["write_max"], "|", probe["q_min"], "|", probe["trace_max"], "|", int(node.turned.sum()))
