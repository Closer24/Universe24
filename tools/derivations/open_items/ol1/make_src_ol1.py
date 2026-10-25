"""ol1's flagged copy of the engine (engine-5.0-test bb9deff70: EQ-S1 in cs7's letter, the take by the fall's sign and the light
no body built; PL-S1 not built), written by this script and never by hand: src_ol1/event_universe is src/event_universe with
three files changed by exact text replacements (each must match once, else the script refuses); every flag absent is David's
path bit for bit (check_flag_absent.py).
  OL1_PL=kick   (interval.py): PL-S1 as pl2 wrote it (make_src_pl2b.py): the shape-4 row's TIME line's write is the records'
                charge read at the kick, SUM over the records with a gap of -(re u_im,in - im u_re,in) - (re u_im,out - im u_re,out),
                u the kick's odd velocities, landing as a momentum kick P_out = P_in + X F + w X_now q before the line's division
                (q the carried quotient at the wall T, the write remainder carried as before); no level written after the division.
  OL1_ODD=exch  (gram.py, node.py): letter A, the three odd lines of the shape-4 row NEGATED at the exchange (the row's
                conjugation K = diag(1, -1, -1, -1): the time line a scalar, the odd lines a vector odd under time's reversal as
                the plane's im line is), their rotation and write remainders mirrored twice by the one rule (left); the current J
                at the start written as David writes it.
  OL1_ODD=exchkick (gram.py, node.py, interval.py): OL-S1, letter A with the current J at the start (David's numerator)
                landing as a momentum kick on each odd line at the kick's unit w X_now before its division (as PL-S1 lands the
                charge), no level written after: the interval its own mirror in every integer on a board with a current.
  OL1_ODD=kick  (interval.py): letter B (the Boss's letter beside PL-S1), the odd lines' source read at the kick from the odd
                velocities, per axis a the sum over the records with a gap and over the velocities in and out of
                dN_a.GJ.U + dU_a.GJ.N (dN_a, dU_a the centred differences of the neighbours' levels and velocities read in the
                Node's frame, N the levels at the start, U the own velocities), its own mirror under the exchange and the
                conjugation; landing as a momentum kick on each odd line before its division; no level written after.
Run: python make_src_ol1.py (writes src_ol1/ beside this file)."""
import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
WORKTREE = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
SRC = os.path.join(WORKTREE, "src", "event_universe")
ROOT = os.path.join(HERE, "src_ol1")
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


# interval.py: PL-S1 (OL1_PL=kick) and letter B (OL1_ODD=kick)
p = os.path.join(DST, "interval.py")
replace_once(p, "import numpy as np\n", "import numpy as np\nimport os\n")
replace_once(p, "from event_universe.core.rule3 import division_forward, half, held_numerator, quotient\n",
             "from event_universe.core.rule3 import carried_division, division_forward, half, held_numerator, quotient\n")
replace_once(p, """        for line, n in zip(self.lines(self.potential), [2 * self.w_end, *self.current], strict=True):
            node.write(line, n, -1)
""", """        for line, n in zip(self.lines(self.potential), self.sign_numerators(2 * self.w_end), strict=True):
            if n is not None:
                node.write(line, n, -1)
""")
replace_once(p, """        for line, n in zip(
            self.out[self.where[id(self.potential)]], [2 * self.w_after, *self.current], strict=True
        ):
            node.write(line, n, 1)
""", """        for line, n in zip(
            self.out[self.where[id(self.potential)]], self.sign_numerators(2 * self.w_after), strict=True
        ):
            if n is not None:
                node.write(line, n, 1)
""")
replace_once(p, """            u_in = [paces.odd_rounded(2 * p + 1, ds) for p in p_side]
            u_out = [paces.odd_rounded(2 * p + 1, ds) for p in p_other]
""", """            if r is self.potential and os.environ.get("OL1_PL", "") == "kick":
                # PL-S1 (pl2's form): the charge's write as a momentum kick at the unit w X_now before the time line's division
                line = self.rows[k][0]
                q, line.wr = carried_division(self.charge_at_kick(), line.wwall, line.wr, self.direction)
                p_other[0] = p_other[0] + self.direction * node.w * self.x_now * q
            if r is self.potential and os.environ.get("OL1_ODD", "") in ("kick", "exchkick"):
                # ol1's letter B (kick): the current read at the kick; OL-S1 (exchkick): the current J at the start as David
                # reads it; either landing as a momentum kick on each odd line at the unit w X_now before its division
                source = self.current_at_kick() if os.environ.get("OL1_ODD", "") == "kick" else self.current
                for a, numerator in enumerate(source):
                    line = self.rows[k][1 + a]
                    q, line.wr = carried_division(numerator, line.wwall, line.wr, self.direction)
                    p_other[1 + a] = p_other[1 + a] + self.direction * node.w * self.x_now * q
            u_in = [paces.odd_rounded(2 * p + 1, ds) for p in p_side]
            u_out = [paces.odd_rounded(2 * p + 1, ds) for p in p_other]
            self.velocities[k] = (u_in, u_out)
""")
replace_once(p, """        self.forms = zeros(node.shape)
        self.kicked: dict[int, list[Any]] = {}
""", """        self.forms = zeros(node.shape)
        self.kicked: dict[int, list[Any]] = {}
        self.velocities: dict[int, tuple[list[Any], list[Any]]] = {}
""")
replace_once(p, """    def mean_wall(self) -> Any:""", """    def sign_numerators(self, charge: Any) -> list[Any]:
        \"\"\"ol1: the shape-4 row's four write numerators after the division: David's path [2 W, J_x, J_y, J_z]; under OL1_PL=kick
        the time line None (its write landed at the kick); under OL1_ODD=kick the three odd lines None (the same).\"\"\"
        time_line = None if os.environ.get("OL1_PL", "") == "kick" else charge
        odd = [None] * AXES if os.environ.get("OL1_ODD", "") in ("kick", "exchkick") else list(self.current)
        return [time_line, *odd]

    def charge_at_kick(self) -> Any:
        \"\"\"PL-S1 (pl2's spelling): SUM over the records with a gap and over their planes of
        -(re u_im,in - im u_re,in) - (re u_im,out - im u_re,out), re and im the plane's levels at the interval's start and u the
        kick's odd velocities (the records come before the shape-4 row in the riders' order): the same integers in either direction
        and its own mirror under the exchange and the conjugation.\"\"\"
        found = zeros(self.node.shape)
        for r in self.gapped:
            k = self.where[id(r)]
            u_in, u_out = self.velocities[k]
            levels = self.starts[k]
            for re, im, uri, uii, uro, uio in zip(
                levels[0::2], levels[1::2], u_in[0::2], u_in[1::2], u_out[0::2], u_out[1::2], strict=True
            ):
                found = found - (re * uii - im * uri) - (re * uio - im * uro)
        return found

    def current_at_kick(self) -> list[Any]:
        \"\"\"ol1's letter B: the current read at the kick, per axis a the SUM over the records with a gap and over the velocities in
        and out of dN_a.GJ.U + dU_a.GJ.N, dN_a and dU_a the centred differences of the neighbours' levels and velocities read in the
        Node's frame (gram.conjugated), N the levels at the start and U the own velocities; the time derivative of the sign's
        current J_a = dN_a.GJ.N at the kick, even under the exchange and the conjugation (N -> K N, U -> -K U with in and out
        exchanged).\"\"\"
        found = [zeros(self.node.shape) for _ in range(AXES)]
        for r in self.gapped:
            k = self.where[id(r)]
            gj = gram.matmul(gram.gram(r.shape), gram.rotation(r.shape))
            levels = self.starts[k]
            for u in self.velocities[k]:
                for a in range(AXES):
                    up_n = gram.conjugated(r.shape, [across(n, 2 * a) for n in levels], self.frames[2 * a])
                    down_n = gram.conjugated(r.shape, [across(n, 2 * a + 1) for n in levels], self.frames[2 * a + 1])
                    up_u = gram.conjugated(r.shape, [across(x, 2 * a) for x in u], self.frames[2 * a])
                    down_u = gram.conjugated(r.shape, [across(x, 2 * a + 1) for x in u], self.frames[2 * a + 1])
                    dn = [x - y for x, y in zip(up_n, down_n, strict=True)]
                    du = [x - y for x, y in zip(up_u, down_u, strict=True)]
                    found[a] = found[a] + gram.form(gj, dn, u) + gram.form(gj, du, levels)
        return found

    def mean_wall(self) -> Any:""")

# gram.py: letter A, the shape-4 row's conjugation K = diag(1, -1, -1, -1) under OL1_ODD=exch
p = os.path.join(DST, "gram.py")
replace_once(p, "import numpy as np\n", "import numpy as np\nimport os\n")
replace_once(p, "from event_universe.rows import PLANE, QUARTET, Line, zeros\n",
             "from event_universe.rows import PLANE, " + "POTENTIAL, " + "QUARTET, Line, zeros\n")
replace_once(p, """    found = identity(shape)
    if shape == PLANE:
        found[1][1] = -1
    return found
""", """    found = identity(shape)
    if shape == PLANE:
        found[1][1] = -1
    if shape == POTENTIAL and os.environ.get("OL1_ODD", "") in ("exch", "exchkick"):
        for a in range(1, shape):  # ol1's letter A: the three odd lines a vector odd under time's reversal
            found[a][a] = -1
    return found
""")

# node.py: the write remainder mirrored once per reversal of its line, as the rotation remainder is (the one rule)
p = os.path.join(DST, "node.py")
replace_once(p, "import numpy as np\n", "import numpy as np\nimport os\n")
replace_once(p, """                if line.wr is not None:
                    line.wr = np.where(top, mirrored(h.wr, line.wwall, 1), line.wr)
""", """                if line.wr is not None:
                    reversals = 1 + (k[i][i] < 0) if os.environ.get("OL1_ODD", "") in ("exch", "exchkick") else 1
                    line.wr = np.where(top, mirrored(h.wr, line.wwall, reversals), line.wr)
""")
print("src_ol1 written:", DST, "flags: OL1_PL=kick (interval.py), OL1_ODD=exch (gram.py, node.py), OL1_ODD=kick (interval.py); every flag absent = David's path")
