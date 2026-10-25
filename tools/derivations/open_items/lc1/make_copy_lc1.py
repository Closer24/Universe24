"""lc1's FLAGGED COPY of the engine (engine-5.0-test 32b56254b, src/event_universe), written by this script and never by
hand: the whole package is copied to tools/derivations/lc1/src_lc1/event_universe and one file (node.py) gains a flag read
from the environment variable LC1_FLAG (the hand's control, no key of any file): absent or empty, every expression is
David's text and the run is bit for bit the default (checked by the state hash of the record); one letter selects a form
of the Link's reach, the one place the two ends of a Link may disagree:

  d  bg2's candidate (d): the reach symmetric in the two ends' paces, R_ij = 2 num p_i p_j Q_ij G^2, on EVERY row alike
     (the riding rows and the carrier's); the runaway of BG_COMPARISON to understand.
  g  the same symmetric reach p_i p_j on the carrier's row ALONE (the row of shape 10, the one row stepped at the fixed
     wall w); every riding row keeps the law's p_i^2: the instrument that parts the carrier's lift from the riders' pump.
  v  the carrier's row alone reads the vacuum's pace on its six Links, R_ij = 2 num Gamma^2 Q_ij G^2 (the pace-free
     current the clause Gravity's flux and the enclosed write names, R_ij / p_i^2 = R_ji / p_j^2); every riding row keeps
     the law's p_i^2 (their Link current X_i p_i^2 = Gamma^3 is pace-free already, section 1 of the report).

The flags g and v are instruments of measurement (a case on the row's shape inside the copy); the generic sentence they
test is written in the report (LC-S1: the reach read through the row's wall, R_ij = R_vac x W_vac / W_i, which on a
riding row is the law's p_i^2 to the rounding and on the row that holds the fixed wall is the vacuum's reach).
Every replacement must match the engine's text exactly once, else the script refuses. Run: python make_copy_lc1.py
"""
import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.normpath(os.path.join(HERE, "..", "..", "..", "src", "event_universe"))
DST = os.path.join(HERE, "src_lc1", "event_universe")

if os.path.exists(os.path.join(HERE, "src_lc1")):
    shutil.rmtree(os.path.join(HERE, "src_lc1"))
shutil.copytree(SRC, DST, ignore=shutil.ignore_patterns("__pycache__"))


def replace(path, pairs):
    text = open(path, encoding="utf-8").read()
    for old, new in pairs:
        if text.count(old) != 1:
            print("REFUSED: the text occurs", text.count(old), "times in", path, ":", old[:80])
            sys.exit(1)
        text = text.replace(old, new)
    open(path, "w", encoding="utf-8").write(text)


FLAG_HEAD = '''import os as _lc1_os

LC1_FLAG = _lc1_os.environ.get("LC1_FLAG", "")  # lc1's control: "" the default bit for bit; "d", "g", "v" the forms of the reach
'''

replace(os.path.join(DST, "node.py"), [
    ('from event_universe.core.rule3 import carried_division, half, link_unit_of, mirrored, unit_of, wall_of\n',
     'from event_universe.core.rule3 import carried_division, half, link_unit_of, mirrored, unit_of, wall_of\n' + FLAG_HEAD),
    ('''        assert r.pair is not None
        return self.rule(r.pair, c, factors)''',
     '''        assert r.pair is not None
        if LC1_FLAG in ("d", "g", "v") and (LC1_FLAG == "d" or r.shape == CARRIER):
            clock, pace = readings.paces_of(self, c)
            num, den = r.pair
            links = (self.G * self.G,) * PORTS if factors is None else factors
            if LC1_FLAG == "v":
                reaches = tuple(2 * self.gamma * self.gamma * f * num for f in links)
            elif np.ndim(pace):
                reaches = tuple(2 * pace * across(pace, port) * f * num for port, f in enumerate(links))
            else:
                reaches = tuple(2 * pace * pace * f * num for f in links)
            wall, own = rule3.wall_of(den, self.gamma, self.G), rule3.mass(num, den, clock, self.G)
            return rule3.Rule(reaches, wall + wall - own - sum(reaches), wall, own)
        return self.rule(r.pair, c, factors)'''),
])
print("written:", DST)
