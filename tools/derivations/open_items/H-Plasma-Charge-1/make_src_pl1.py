"""pl1's FLAGGED COPY of the engine (engine-5.0-test 57220fc0a), written by this script and never by hand: src_pl1/event_universe
is src/event_universe with three files changed by the exact text replacements below (each must match once, else the script refuses).
Every flag absent = the head's path bit for bit (check_flag_absent.py).
  PL1_SIGN=sym   the sign row's time line written from the charge BEFORE and AFTER the step, W_pre + W_after (the mean of the two
                 ends, doubled: the symmetric form), in place of 2 W_after; backward the pre charge is not known at the unwrite
                 (the records' inverse divisions come after it), so the unwrite uses 2 W_end: the run back is NOT exact by design
                 and its MATCH count is the measurement (the form is covariant under the exchange and not reversible).
  PL1_SIGN=pre   the sign row's time line written from 2 W_pre (the charge at the start); backward 2 W_end: not reversible (control).
  PL1_SIGN=none  the sign row's time line written 0 (no charge written; a control that isolates the cause, not a candidate).
  PL1_SIGN=odd   reading (a): the sign row conjugated at the exchange as a pseudoscalar (K = -I on the shape-4 row at the turned
                 Nodes; its rotation remainders mirrored twice by the one rule, the identity; the write remainders once).
  PL1_SIGN=kick  reading (c): the charge enters the sign row's time line as a KICK inside its one division (as the force enters
                 every riding line's kick, and as the walled row's write sits inside its division): at the kick, the momentum of the
                 time line gains (SUM over the records with a gap of a.GJ.P_in + a.GJ.P_out + the carried write remainder) div T, a
                 the record's levels at the start and P_in / P_out its momenta before and after the kick (the charge in momentum
                 form, symmetric in the step's two ends, the same integers read forward and backward), the carry kept in the time
                 line's write remainder at its wall T; no level write on the time line (the three odd lines as the head).
  EQ2_CLICK=a|b|c  eq2's three readings of the body's click where nothing arrives (The-Equilibrium-At-The-Click_COMPARISON.md; the Boss's EQ-S1 is b),
                 carried into this copy so that the plasma's return is read with the clicks refused (a) or laid back (b).
Run: python make_src_pl1.py"""
import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
WORKTREE = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
SRC = os.path.join(WORKTREE, "src", "event_universe")
DST_PKG = os.path.join(HERE, "src_pl1")
DST = os.path.join(DST_PKG, "event_universe")

if os.path.isdir(DST):
    shutil.rmtree(DST)
os.makedirs(DST_PKG, exist_ok=True)
shutil.copytree(SRC, DST, ignore=shutil.ignore_patterns("__pycache__"))


def rewrite(name, replacements):
    path = os.path.join(DST, name)
    text = open(path, encoding="utf-8").read()
    for old, new in replacements:
        if text.count(old) != 1:
            sys.exit(f"{name}: the replacement does not match once: {old[:70]!r} ({text.count(old)})")
        text = text.replace(old, new)
    open(path, "w", encoding="utf-8").write(text)
    print(name, "rewritten:", len(replacements), "replacements")


rewrite(
    "interval.py",
    [
        (
            "from __future__ import annotations\n\nfrom typing import TYPE_CHECKING, Any\n",
            "from __future__ import annotations\n\nimport os\n\nfrom typing import TYPE_CHECKING, Any\n",
        ),
        (
            "def laid_on(node: Node, line: Line, levels: Any) -> None:\n",
            '''PL1_SIGN = os.environ.get("PL1_SIGN")  # pl1: sym | pre | none | odd | absent (the head's path bit for bit)


def sign_source(w_pre: Any, w_after: Any) -> Any:
    """pl1's flag on the sign row's time line's write numerator: absent 2 W_after (the head); sym W_pre + W_after; pre 2 W_pre; none 0; odd as the head (the flag acts in node.exchange). Backward the caller passes the charge it holds for both."""
    if PL1_SIGN == "sym":
        return w_pre + w_after
    if PL1_SIGN == "pre":
        return 2 * w_pre
    if PL1_SIGN == "none":
        return 0 * w_after
    return 2 * w_after


def laid_on(node: Node, line: Line, levels: Any) -> None:
''',
        ),
        (
            "        for line, n in zip(self.lines(self.potential), [2 * self.w_end, *self.current], strict=True):\n            node.write(line, n, -1)\n",
            "        for line, n in zip(self.lines(self.potential), [sign_source(self.w_end, self.w_end), *self.current], strict=True):  # pl1: backward the pre charge is unknown here\n            node.write(line, n, -1)\n",
        ),
        (
            "        self.w_after = zeros(node.shape)\n        for r in self.riders:\n",
            "        self.w_after = zeros(node.shape)\n        self.w_pre = zeros(node.shape)  # pl1: the records' charge before the step\n        for r in self.riders:\n",
        ),
        (
            "                if r.gap:\n                    self.w_after = self.w_after + gram.charge(r.shape, after)\n",
            "                if r.gap:\n                    self.w_after = self.w_after + gram.charge(r.shape, after)\n                    self.w_pre = self.w_pre + gram.charge(r.shape, start)  # pl1\n",
        ),
        (
            "            self.out[self.where[id(self.potential)]], [2 * self.w_after, *self.current], strict=True\n",
            "            self.out[self.where[id(self.potential)]], [None if PL1_SIGN == \"kick\" else sign_source(self.w_pre, self.w_after), *self.current], strict=True  # pl1\n",
        ),
        (
            "        ):\n            node.write(line, n, 1)\n",
            "        ):\n            if n is not None:  # pl1: under kick the time line has no level write\n                node.write(line, n, 1)\n",
        ),
        (
            "        for line, n in zip(self.lines(self.potential), [sign_source(self.w_end, self.w_end), *self.current], strict=True):  # pl1: backward the pre charge is unknown here\n            node.write(line, n, -1)\n",
            "        for line, n in zip(self.lines(self.potential), [None if PL1_SIGN == \"kick\" else sign_source(self.w_end, self.w_end), *self.current], strict=True):  # pl1: backward the pre charge is unknown here\n            if n is not None:\n                node.write(line, n, -1)\n",
        ),
        (
            "        d = 2 * node.w * self.x_now\n        w_side = self.mean_wall()\n        for r in self.riders:\n",
            "        d = 2 * node.w * self.x_now\n        w_side = self.mean_wall()\n        source = zeros(node.shape)  # pl1 kick: the records' charge in momentum form, a.GJ.P_in + a.GJ.P_out, summed as the loop meets them\n        for r in self.riders:\n",
        ),
        (
            "            p_other = [\n                p + self.direction * self.x_now * f for p, f in zip(p_side, self.force[k], strict=True)\n            ]\n",
            "            p_other = [\n                p + self.direction * self.x_now * f for p, f in zip(p_side, self.force[k], strict=True)\n            ]\n            if PL1_SIGN == \"kick\" and r.gap:\n                gj = gram.matmul(g, gram.rotation(r.shape))\n                source = source + gram.form(gj, self.starts[k], p_side) + gram.form(gj, self.starts[k], p_other)\n            if PL1_SIGN == \"kick\" and r is self.potential:\n                line = self.rows[k][0]\n                q, line.wr = carried_division(source, line.wwall, line.wr, self.direction)\n                p_other[0] = p_other[0] + self.direction * q\n",
        ),
        (
            "from event_universe.core.rule3 import division_forward, half, held_numerator, quotient\n",
            "from event_universe.core.rule3 import carried_division, division_forward, half, held_numerator, quotient\n",
        ),
    ],
)

rewrite(
    "node.py",
    [
        (
            "import hashlib\nfrom typing import Any\n",
            "import hashlib\nimport os\nfrom typing import Any\n",
        ),
        (
            "from event_universe.rows import (\n    CARRIER,\n    HALF_WIDTH,\n    PLANE,\n",
            "from event_universe.rows import (\n    CARRIER,\n    HALF_WIDTH,\n    PLANE,\n    POTENTIAL,\n",
        ),
        (
            "COUNTS = {  # the run's counts, every one 0 at the start\n",
            '''PL1_SIGN = os.environ.get("PL1_SIGN")  # pl1: odd = reading (a), the shape-4 row conjugated at the exchange as a pseudoscalar


def pl1_conjugation(shape: int) -> list[list[int]]:
    """pl1's flag on the swap's conjugation: K = -I on the shape-4 row under PL1_SIGN=odd (reading (a)); gram.conjugation otherwise, bit for bit."""
    k = gram.conjugation(shape)
    if PL1_SIGN == "odd" and shape == POTENTIAL:
        return [[-x for x in row] for row in k]
    return k


COUNTS = {  # the run's counts, every one 0 at the start
''',
        ),
        (
            "        for r, row, hrow in zip(self.rows_, self.rows(), held, strict=True):\n            k = gram.conjugation(r.shape)\n",
            "        for r, row, hrow in zip(self.rows_, self.rows(), held, strict=True):\n            k = pl1_conjugation(r.shape)  # pl1\n",
        ),
    ],
)

rewrite(
    "bodies.py",
    [
        (
            "from __future__ import annotations\n\nfrom typing",
            "from __future__ import annotations\n\nimport os\n\nfrom typing",
        ),
        (
            "from event_universe.core.ports import PORT_SIDES\n",
            "from event_universe.core.ports import PORT_SIDES, PORTS\nfrom event_universe.links import row_current\n",
        ),
        (
            "from event_universe.take import frame_nodes, take_at\n",
            "from event_universe.take import frame_nodes, lay, take_at\n\nEQ2_FLAG = os.environ.get(\"EQ2_CLICK\")  # eq2's flag carried by pl1: a, b, c or absent (the head's path)\n",
        ),
        (
            "    for rec, row in enumerate(node.records()):\n        standing_now = np.vectorize(",
            "    rec0 = node.records().index(node.row(PLANE, gap=0))\n    z = node.records()[rec0].lines[0]\n    arriving = (\n        [row_current(plane_starts[rec0], port) for port in range(PORTS)] if EQ2_FLAG else []\n    )  # eq2: the taken row's current across the Node's six Links at the interval's start, as close.meet reads it\n    for rec, row in enumerate(node.records()):\n        standing_now = np.vectorize(",
        ),
        (
            """            if at in born_nodes or frozen[at]:
                continue
            got = take_at(node, at, node.units[rec], r_gap0, 1)
            node.standing[rec][at] = 0
            if got is None:
                continue
            levels, fall, now, before = got
            node.counts["body_clicks"] += 1
            node.log.append(credit(node, rec, at, plane_starts, fall, levels, now, before))
""",
            """            if at in born_nodes or frozen[at]:
                continue
            quiet = EQ2_FLAG is not None and (
                EQ2_FLAG == "c" or all(int(c[at]) == 0 for c in arriving)
            )  # eq2: nothing arrives at the Node (every one of its six Links' currents 0)
            if EQ2_FLAG == "a" and quiet:
                node.standing[rec][at] = 0
                node.counts["refused_arrival"] = node.counts.get("refused_arrival", 0) + 1
                node.log.append(
                    {"event": "refused", "i": node.interval, "node": list(at), "cause": "arrival", "row": rec}
                )
                continue
            got = take_at(node, at, node.units[rec], r_gap0, 1)
            node.standing[rec][at] = 0
            if got is None:
                continue
            levels, fall, now, before = got
            node.counts["body_clicks"] += 1
            entry = credit(node, rec, at, plane_starts, fall, levels, now, before)
            if EQ2_FLAG in ("b", "c") and quiet:
                lay(node, rec0, at, (now - int(z.now[at]),) + (0,) * (2 * node.records()[rec0].shape - 1))
                entry["laid_back"] = levels
                entry["dP_take"] = [0, 0, 0]
                node.counts["laid_back"] = node.counts.get("laid_back", 0) + 1
            node.log.append(entry)
""",
        ),
    ],
)
print("src_pl1 written:", DST)
