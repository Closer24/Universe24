"""pl2's SECOND flagged copy, src_pl2b: src_pl2 (make_src_pl2.py's three files) with one more flag in interval.py,
  PL2_WRITE=kick: the shape-4 row's time line's write lands as a MOMENTUM kick inside interval.kicks, before the line's division
             (P_out = P_in + X F + w X_now q, q the write's carried quotient of the kick-form numerator at the wall T, the write
             remainder carried as before), and no level is written after the division; backward the inverse in the same place
             (q and the former remainder from the carried division at -1, P_in = P_out - X F - w X_now q). The kick-form numerator
             (PL2_CHARGE=kick) is implied. Prediction (section 1): the interval is then its own mirror under the exchange, so the
             plasma's fall retraces its rise bit for bit (no line parts at any k) and returns to Gamma exactly.
Every flag absent is David's path bit for bit (check_flag_absent.py with src_pl2b). Run: python make_src_pl2.py first, then this."""
import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "src_pl2", "event_universe")
ROOT = os.path.join(HERE, "src_pl2b")
DST = os.path.join(ROOT, "event_universe")
if os.path.isdir(ROOT):
    shutil.rmtree(ROOT)
os.makedirs(ROOT)
shutil.copytree(SRC, DST, ignore=shutil.ignore_patterns("__pycache__"))


def replace_once(path, old, new):
    text = open(path, encoding="utf-8").read()
    if text.count(old) != 1:
        sys.exit(f"the site is not unique in {path}: {old[:70]!r} ({text.count(old)})")
    open(path, "w", encoding="utf-8").write(text.replace(old, new))


p = os.path.join(DST, "interval.py")
replace_once(p, "from event_universe.core.rule3 import division_forward, half, held_numerator, quotient\n",
             "from event_universe.core.rule3 import carried_division, division_forward, half, held_numerator, quotient\n")
# the kick: the potential's time line kicked by the write's quotient
replace_once(p, """            p_other = [
                p + self.direction * self.x_now * f for p, f in zip(p_side, self.force[k], strict=True)
            ]
            u_in = [paces.odd_rounded(2 * p + 1, ds) for p in p_side]""", """            p_other = [
                p + self.direction * self.x_now * f for p, f in zip(p_side, self.force[k], strict=True)
            ]
            if r is self.potential and os.environ.get("PL2_WRITE", "") == "kick":
                # pl2: the charge's write as a momentum kick at the wall w X_now, the quotient of the kick-form numerator at T
                line = self.rows[k][0]
                q, wr = carried_division(self.charge_numerator(), line.wwall, line.wr, self.direction)
                line.wr = wr
                p_other[0] = p_other[0] + self.direction * node.w * self.x_now * q
            u_in = [paces.odd_rounded(2 * p + 1, ds) for p in p_side]""")
replace_once(p, """        for line, n in zip(self.lines(self.potential), [self.charge_numerator(), *self.current], strict=True):
            node.write(line, n, -1)
""", """        for line, n in zip(self.lines(self.potential), [self.charge_numerator(), *self.current], strict=True):
            if n is not None:
                node.write(line, n, -1)
""")
replace_once(p, """        for line, n in zip(
            self.out[self.where[id(self.potential)]], [self.charge_numerator(), *self.current], strict=True
        ):
            node.write(line, n, 1)
""", """        for line, n in zip(
            self.out[self.where[id(self.potential)]], [self.charge_numerator(), *self.current], strict=True
        ):
            if n is not None:
                node.write(line, n, 1)
""")
replace_once(p, """        flag = os.environ.get("PL2_CHARGE", "")
        if flag == "kick":""", """        flag = os.environ.get("PL2_CHARGE", "")
        if os.environ.get("PL2_WRITE", "") == "kick":
            if getattr(self, "kicking", False):
                flag = "kick"  # inside kicks: the numerator for the momentum kick
            else:
                return None  # no level written after the division
        if flag == "kick":""")
replace_once(p, """            if r is self.potential and os.environ.get("PL2_WRITE", "") == "kick":
                # pl2: the charge's write as a momentum kick at the wall w X_now, the quotient of the kick-form numerator at T
                line = self.rows[k][0]
                q, wr = carried_division(self.charge_numerator(), line.wwall, line.wr, self.direction)""", """            if r is self.potential and os.environ.get("PL2_WRITE", "") == "kick":
                # pl2: the charge's write as a momentum kick at the wall w X_now, the quotient of the kick-form numerator at T
                line = self.rows[k][0]
                self.kicking = True
                numerator = self.charge_numerator()
                self.kicking = False
                q, wr = carried_division(numerator, line.wwall, line.wr, self.direction)""")
print("src_pl2b written:", DST, "flag PL2_WRITE=kick added (interval.py); every flag absent = David's path")
