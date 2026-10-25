"""pl2's flagged copy of the engine (engine-5.0-test 10c04fb31), written by this script and never by hand: src_pl2/event_universe
is src/event_universe with three files changed by exact text replacements (each must match once, else the script refuses); every
flag absent is David's path bit for bit (check_flag_absent.py).
  CS7_EQ=n   (bodies.py): cs7's letter of EQ-S1 on the NET current: where the taken row's six currents at the Node sum to 0 at the
             interval's start, the body's take is laid back on the taken line by the one lay act in the same close, the credit
             written with laid_back = levels and dP_take 0 (cs7's make_copy_cs7.py, this head's sites);
  PL2_CHARGE=kick (interval.py): the shape-4 row's time line is written the records' charge read at the kick, the Wronskian of
             the level now against the kick's odd velocities in and out, SUM over the records with a gap of
             -(re u_im,in - im u_re,in) - (re u_im,out - im u_re,out), u the odd rounding of 2 P + 1 over 2 w X (interval.kicks),
             the same integers forward and backward and its own mirror under the exchange (pl2's derivation, section 1);
  PL2_CHARGE=ends (interval.py): the time line written W_start + W_after (the level Wronskian at the interval's two ends) forward;
             backward the unwrite has no W_start (the pre state's before is not known before the carrier's inverse), so it
             unwrites 2 W_after: the run back is expected to FAIL where W varies (the law's refusal of this letter, measured);
  PL2_SIGN_ODD=1 (node.py): the shape-4 row's time line negated at the exchange (letter (a), a pseudoscalar), its rotation
             remainder mirrored twice (the identity) and its write remainder twice, by the one rule of the remainder.
Run: python make_src_pl2.py (writes src_pl2/ beside this file)."""
import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
WORKTREE = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
SRC = os.path.join(WORKTREE, "src", "event_universe")
ROOT = os.path.join(HERE, "src_pl2")
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


# bodies.py: cs7's net reading of EQ-S1 (CS7_EQ=n), eq2's reading b and the control c beside it
p = os.path.join(DST, "bodies.py")
replace_once(p, "import numpy as np\n", "import numpy as np\nimport os\n")
replace_once(p, "from event_universe.core.ports import PORT_SIDES\n",
             "from event_universe.core.ports import PORT_SIDES, PORTS\nfrom event_universe.links import row_current\n")
replace_once(p, "from event_universe.take import frame_nodes, take_at\n",
             "from event_universe.take import frame_nodes, lay, take_at\n")
replace_once(p, """    for rec, row in enumerate(node.records()):
        if row.gap == 0:
            continue
        standing_now = np.vectorize(""", """    rec0 = node.records().index(node.row(PLANE, gap=0))
    eq = os.environ.get("CS7_EQ", "")  # cs7: n (the net current), b (eq2's letter), c (every click); absent David's path
    arriving = (
        [row_current(plane_starts[rec0], port) for port in range(PORTS)] if eq else []
    )  # the taken row's current across the Node's six Links at the interval's start, as close.meet reads it
    for rec, row in enumerate(node.records()):
        if row.gap == 0:
            continue
        standing_now = np.vectorize(""")
replace_once(p, """            got = take_at(node, at, node.units[rec], r_gap0, 1)
            node.standing[rec][at] = 0
            if got is None:
                continue
            levels, fall, now, before = got
            node.counts["body_clicks"] += 1
            node.log.append(credit(node, rec, at, plane_starts, fall, levels, now, before))
""", """            currents = [int(c[at]) for c in arriving]
            quiet = (
                eq == "c"
                or (eq == "b" and all(v == 0 for v in currents))
                or (eq == "n" and sum(currents) == 0)
            )  # nothing arrives at the Node by the reading named
            got = take_at(node, at, node.units[rec], r_gap0, 1)
            node.standing[rec][at] = 0
            if got is None:
                continue
            levels, fall, now, before = got
            node.counts["body_clicks"] += 1
            entry = credit(node, rec, at, plane_starts, fall, levels, now, before)
            if eq:
                entry["arrivals"] = currents
            if eq and quiet:  # EQ-S1: the taken levels laid back on the taken line by the one lay act in the same close
                z = node.records()[rec0].lines[0]
                lay(node, rec0, at, (now - int(z.now[at]),) + (0,) * (2 * node.records()[rec0].shape - 1))
                entry["laid_back"] = levels
                entry["dP_take"] = [0, 0, 0]
                node.counts["laid_back"] = node.counts.get("laid_back", 0) + 1
            node.log.append(entry)
""")

# interval.py: the charge's write form (PL2_CHARGE)
p = os.path.join(DST, "interval.py")
replace_once(p, "import numpy as np\n", "import numpy as np\nimport os\n")
replace_once(p, """        for line, n in zip(self.lines(self.potential), [2 * self.w_end, *self.current], strict=True):
            node.write(line, n, -1)
""", """        for line, n in zip(self.lines(self.potential), [self.charge_numerator(), *self.current], strict=True):
            node.write(line, n, -1)
""")
replace_once(p, """        for line, n in zip(
            self.out[self.where[id(self.potential)]], [2 * self.w_after, *self.current], strict=True
        ):
            node.write(line, n, 1)
""", """        for line, n in zip(
            self.out[self.where[id(self.potential)]], [self.charge_numerator(), *self.current], strict=True
        ):
            node.write(line, n, 1)
""")
replace_once(p, """    def mean_wall(self) -> Any:""", """    def velocities(self, r: Row) -> tuple[list[Any], list[Any]]:
        \"\"\"pl2: a riding row's odd velocities in and out at the kick, as interval.kicks reads them: u = the odd rounding of 2 P + 1
        over 2 w X_now at the row's scale, P_in = W (a_now - a_before) + r - W div 2 at the mean wall as the rows hold them, P_out =
        P_in + direction X_now F; the same integers forward (from the pre state) and backward (from the post state).\"\"\"
        k = self.where[id(r)]
        ws, ds = self.scales[k] * self.mean_wall(), self.scales[k] * 2 * self.node.w * self.x_now
        p_side = [ws * (line.now - line.before) + line.rem - half(ws) for line in self.rows[k]]
        p_other = [p + self.direction * self.x_now * f for p, f in zip(p_side, self.force[k], strict=True)]
        return [paces.odd_rounded(2 * p + 1, ds) for p in p_side], [paces.odd_rounded(2 * p + 1, ds) for p in p_other]

    def charge_numerator(self) -> Any:
        \"\"\"pl2: the shape-4 row's time line's write numerator. David's path (the flag absent): 2 W of the records after the step
        (forward w_after; backward w_end, the post state's charge). PL2_CHARGE=kick: the charge read at the kick, SUM over the
        records with a gap and over their planes of -(re u_im,in - im u_re,in) - (re u_im,out - im u_re,out), re and im the
        plane's levels at the interval's start (self.at) and u the kick's odd velocities (velocities): the same integers in either
        direction and its own mirror under the exchange and the conjugation. PL2_CHARGE=ends: W_start + W_after forward
        (w_end + w_after); backward 2 w_end (no W_start before the carrier's inverse: the run back is expected to fail).\"\"\"
        flag = os.environ.get("PL2_CHARGE", "")
        if flag == "kick":
            found = zeros(self.node.shape)
            for r in self.gapped:
                u_in, u_out = self.velocities(r)
                levels = [self.at(line) for line in self.lines(r)]
                for re, im, uri, uii, uro, uio in zip(
                    levels[0::2], levels[1::2], u_in[0::2], u_in[1::2], u_out[0::2], u_out[1::2], strict=True
                ):
                    found = found - (re * uii - im * uri) - (re * uio - im * uro)
            return found
        if flag == "ends":
            return self.w_end + self.w_after if self.direction == 1 else 2 * self.w_end
        return 2 * self.w_after if self.direction == 1 else 2 * self.w_end

    def mean_wall(self) -> Any:""")

# node.py: the time line of the shape-4 row negated at the exchange (PL2_SIGN_ODD=1)
p = os.path.join(DST, "node.py")
replace_once(p, "import numpy as np\n", "import numpy as np\nimport os\n")
replace_once(p, """        for r, row, hrow in zip(self.rows_, self.rows(), held, strict=True):
            k = gram.conjugation(r.shape)
            nows, befores = (""", """        for r, row, hrow in zip(self.rows_, self.rows(), held, strict=True):
            k = gram.conjugation(r.shape)
            if os.environ.get("PL2_SIGN_ODD", "") == "1" and r.shape == POTENTIAL and r.wall is None:
                k = [list(x) for x in k]
                k[0][0] = -1  # pl2's letter (a): the time line a pseudoscalar, negated at the exchange
            nows, befores = (""")
replace_once(p, """                if line.wr is not None:
                    line.wr = np.where(top, mirrored(h.wr, line.wwall, 1), line.wr)
""", """                if line.wr is not None:
                    line.wr = np.where(top, mirrored(h.wr, line.wwall, 1 + (k[i][i] < 0)), line.wr)
""")
replace_once(p, "from event_universe.rows import (\n    CARRIER,\n", "from event_universe.rows import (\n    CARRIER,\n    POTENTIAL,\n")
print("src_pl2 written:", DST, "flags: CS7_EQ (bodies.py), PL2_CHARGE (interval.py), PL2_SIGN_ODD (node.py); every flag absent = David's path")
