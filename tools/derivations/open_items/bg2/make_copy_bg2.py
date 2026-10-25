"""bg2's FLAGGED COPY of the engine (engine-5.0-test 5e94fd4b6, src/event_universe), written by this script and never by hand:
the whole package is copied to tools/derivations/bg2/src_bg2/event_universe and two files gain a flag read from the
environment variable BG2_FLAG (the hand's control, no key of any file): absent or empty, every expression is David's text
and the run is bit for bit the default (checked by the state hash and the record); "a", "b" or "c" selects one candidate:

  a  the write's source at the carrier's unit (PM-S1 carried into the carrier's write): the forms, the trace and the
     traceless stress each weighed by X_now div Gamma before the one carried division (the vacuum's weight 1 at X = Gamma).
  b  the riding wall's power a^2: the mean wall (w div 2)(X_before + X_now) replaced by w largest_below(Gamma (X_before + X_now) div 2),
     the conformal wall sqrt(Gamma X) in place of X, in the three places the wall is built (the riding lines' start,
     the mean wall of the interval, the carrier's wall at its end) and in the odd rounding's unit of the momenta.
  c  the swap at the top read on the Node's one-Link form: the weak maximum of the sum of the Node's level and its six
     neighbours' (X_i + SUM_j X_j, read through the six Links, no board sum) in place of the Node's level alone.

Every replacement must match the engine's text exactly once, else the script refuses. Run: python make_copy_bg2.py
"""
import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.normpath(os.path.join(HERE, "..", "..", "..", "src", "event_universe"))
DST = os.path.join(HERE, "src_bg2", "event_universe")

if os.path.exists(os.path.join(HERE, "src_bg2")):
    shutil.rmtree(os.path.join(HERE, "src_bg2"))
shutil.copytree(SRC, DST, ignore=shutil.ignore_patterns("__pycache__"))


def replace(path, pairs):
    text = open(path, encoding="utf-8").read()
    for old, new in pairs:
        if text.count(old) != 1:
            print("REFUSED: the text occurs", text.count(old), "times in", path, ":", old[:80])
            sys.exit(1)
        text = text.replace(old, new)
    open(path, "w", encoding="utf-8").write(text)


FLAG_HEAD = '''import os as _bg2_os

BG2_FLAG = _bg2_os.environ.get("BG2_FLAG", "")  # bg2's control: "" the default bit for bit; "a", "b", "c" the candidates
'''

# ---- interval.py: the candidates (a) and (b)
replace(os.path.join(DST, "interval.py"), [
    ('from event_universe.core.rule3 import division_forward, half, held_numerator, quotient\n',
     'from event_universe.core.rule3 import division_forward, half, held_numerator, largest_below, quotient\n' + FLAG_HEAD +
     '''

def bg2_root_wall(w, gamma, summed):
    """(b) the conformal wall: w largest_below(Gamma s) at every Node, s = (X_before + X_now) div 2; w Gamma at the vacuum, as the mean wall is."""
    return w * np.vectorize(lambda v: largest_below(int(gamma) * int(v)), otypes=[object])(np.asarray(summed, dtype=object))
'''),
    ('''        return self.w_half * (self.carrier.lines[0].before + self.carrier.lines[0].now)''',
     '''        if BG2_FLAG == "b":
            return bg2_root_wall(self.node.w, self.node.gamma, half(self.carrier.lines[0].before + self.carrier.lines[0].now))
        return self.w_half * (self.carrier.lines[0].before + self.carrier.lines[0].now)'''),
    ('''        d = 2 * node.w * self.x_now
        w_side = self.mean_wall()''',
     '''        d = 2 * bg2_root_wall(node.w, node.gamma, self.x_now) if BG2_FLAG == "b" else 2 * node.w * self.x_now
        w_side = self.mean_wall()'''),
    ('''        numerators = [
            held_numerator(TRACE, self.x_now, self.forms, self.trace, self.p0, node.den, node.gamma)
        ]
        numerators += [self.traceless[a] * p02 for a in range(AXES)] + [None] * (''',
     '''        if BG2_FLAG == "a":  # (a) every source of the carrier's write weighed by X_now div Gamma, the carrier's unit
            forms_c, trace_c = quotient(self.forms * self.x_now, node.gamma), quotient(self.trace * self.x_now, node.gamma)
            traceless_c = [quotient(self.traceless[a] * self.x_now, node.gamma) for a in range(AXES)]
        else:
            forms_c, trace_c, traceless_c = self.forms, self.trace, list(self.traceless)
        numerators = [
            held_numerator(TRACE, self.x_now, forms_c, trace_c, self.p0, node.den, node.gamma)
        ]
        numerators += [traceless_c[a] * p02 for a in range(AXES)] + [None] * ('''),
    ('''        xc = self.out[k][0]
        self.w_div = self.w_half * (xc.before + xc.now)''',
     '''        xc = self.out[k][0]
        if BG2_FLAG == "b":
            self.w_div = bg2_root_wall(node.w, node.gamma, half(xc.before + xc.now))
        else:
            self.w_div = self.w_half * (xc.before + xc.now)'''),
])

# ---- node.py: the riding walls at the start under (b), the swap's reading under (c)
replace(os.path.join(DST, "node.py"), [
    ('from event_universe.core.rule3 import carried_division, half, link_unit_of, mirrored, unit_of, wall_of\n',
     'from event_universe.core.rule3 import carried_division, half, link_unit_of, mirrored, unit_of, wall_of\n' + FLAG_HEAD),
    ('''        wall = half(self.w) * (carrier.before + carrier.now)
        for r in self.rows_:''',
     '''        wall = half(self.w) * (carrier.before + carrier.now)
        if BG2_FLAG == "b":
            wall = interval.bg2_root_wall(self.w, self.gamma, half(carrier.before + carrier.now))
        for r in self.rows_:'''),
    ('''        clock, pace = readings.paces_of(self, c)
        return rule3.rule_integers(pair[0], pair[1], self.gamma, clock, pace, factors, self.G)''',
     '''        clock, pace = readings.paces_of(self, c)
        if BG2_FLAG == "d" and np.ndim(pace):  # (d) the reach symmetric in the two ends: 2 num p_i p_j Q_ij G^2, every row alike
            links = (self.G * self.G,) * PORTS if factors is None else factors
            reaches = tuple(2 * pace * across(pace, port) * f * pair[0] for port, f in enumerate(links))
            wall, own = rule3.wall_of(pair[1], self.gamma, self.G), rule3.mass(pair[0], pair[1], clock, self.G)
            return rule3.Rule(reaches, wall + wall - own - sum(reaches), wall, own)
        return rule3.rule_integers(pair[0], pair[1], self.gamma, clock, pace, factors, self.G)'''),
    ('''        x0, x1, x2 = held[k][0].before, held[k][0].now, self.row(CARRIER).lines[0].now
        peak = np.vectorize(''',
     '''        x0, x1, x2 = held[k][0].before, held[k][0].now, self.row(CARRIER).lines[0].now
        if BG2_FLAG == "c":  # (c) the one-Link form: the Node's level and its six neighbours' summed, through the six Links
            x0, x1, x2 = (v + sum(across(v, port) for port in range(PORTS)) for v in (x0, x1, x2))
        peak = np.vectorize('''),
])
print("written:", DST)
