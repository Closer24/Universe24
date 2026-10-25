"""un2's FLAGGED COPY of src/event_universe (engine-5.0-test 4468c0970), written by this script and never by hand:
src_un2/event_universe is src/event_universe with every branch on a row's gap in the Node's acts replaced by the VALUE of one
function of the pair or by a lookup of a row by its numbers, each replacement named below and asserted to match the text exactly once.
Every new form stands behind the environment flag UN2_GENERIC=1; with the flag absent the copy runs David's path bit for bit
(the replaced expressions keep David's text on the off branch). Run: python make_copy_un2.py  (writes src_un2/ beside it).

The forms (the derivation in un2_REPORT.md, section 1):
  U  the unit of a row, one function of the pair: 3 T (s + den (num div den)), s = largest_below(den^2 - num^2);
     num div den is 1 at the pair with no gap and 0 at every other pair of the file's range 0 <= num <= den (the 1 and the 0).
  E  the emitter: the plane whose pair is the potential's pair (gn2), a lookup by the pairs' values; every `row(PLANE, gap=0)` reads it.
  C  the coupling of a plane to the Links' phase, c(pair) = min(den - num, 1): the Link's count and odd part are multiplied by c
     (the turn at c = 0 the identity by arithmetic, the orbit's pair at the count 0 being (X, 0)); the sign's sources (the Wronskian,
     the current) and the emission are weighted by c: every plane in every loop, no plane left out by a test.
  O  the acts' order: a row that is written (a write wall on a line) comes after the rows of its shape that are not; by shape and write.
  T  the taken row's unit threads the close as an argument (meet, read_number): the unit of the row whose quanta meet.
  L  the loader (seed.py, rows_of): the hole's row is the sea's row (the last sea laid); the sea's and the packet's forms and the file's
     checks read the pair's value against the potential's pair, the word gap gone; these read the file and stay the loader's cases.
"""

import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "..", "..", "..", "src", "event_universe")
DST_ROOT = os.path.join(HERE, "src_un2")
DST = os.path.join(DST_ROOT, "event_universe")

if os.path.isdir(DST_ROOT):
    shutil.rmtree(DST_ROOT)
shutil.copytree(SRC, DST, ignore=shutil.ignore_patterns("__pycache__"))

count = 0


def replace(name: str, old: str, new: str) -> None:
    """One named replacement in the copy's file `name`, the old text matched exactly once."""
    global count
    path = os.path.join(DST, name)
    text = open(path, encoding="utf-8").read()
    if text.count(old) != 1:
        print("REFUSED", name, repr(old[:80]), "matches", text.count(old))
        sys.exit(1)
    open(path, "w", encoding="utf-8").write(text.replace(old, new))
    count += 1


# ---- rows.py: the flag, the write wall by the pair's value, the order by shape and write, plane_of, the checks

replace(
    "rows.py",
    "from event_universe.core.rule3 import half, held_wall, quotient\n",
    "import os\n\nfrom event_universe.core.rule3 import half, held_wall, quotient\n",
)
replace(
    "rows.py",
    "TRACE = 54  # the trace's weight of the held walls and the carrier's write, 2 x 27 (ALGEBRA.md, the held write)\n",
    "TRACE = 54  # the trace's weight of the held walls and the carrier's write, 2 x 27 (ALGEBRA.md, the held write)\n"
    'GENERIC = os.environ.get("UN2_GENERIC") == "1"  # un2: the branch-free forms on; off is David\'s path bit for bit\n',
)
# R1 the write wall: the plane at the universe's own pair (den, den), the potential's pair (E)
replace(
    "rows.py",
    "    if shape == PLANE and pair is not None and pair[0] == pair[1]:\n        return [action, None]\n",
    "    if shape == PLANE and pair is not None and (pair == (den, den) if GENERIC else pair[0] == pair[1]):\n        return [action, None]\n",
)
# R2 the order: a written row after the unwritten rows of its shape (O)
replace(
    "rows.py",
    "def order_of(row: Row) -> int:\n",
    "def order_key(row: Row) -> tuple[int, int, int]:\n"
    '    """un2 (O): the acts\' order as a tuple compared and never tested: the row with its own wall first (0, 0, 0); then every pair row by its shape, and within a shape the rows that are written (a write wall on a line: the plane the Wronskian is laid on) after the rows that are not, the written row reading the unwritten ones."""\n'
    "    if row.wall is not None:\n        return (0, 0, 0)\n"
    "    return (1, row.shape, sum(1 for line in row.lines if line.wwall is not None))\n\n\n"
    "def order_of(row: Row) -> int:\n",
)
replace(
    "rows.py",
    "    rows = sorted(by_index, key=order_of)\n",
    "    rows = sorted(by_index, key=order_key if GENERIC else order_of)\n",
)
# R3, R4 the file's checks by the pairs' values (L)
replace(
    "rows.py",
    "    walled = [r for r in rows if r.wall is not None]\n"
    "    gap0 = [r for r in rows if r.shape == PLANE and r.gap == 0]\n"
    "    carriers = [r for r in rows if r.shape == CARRIER]\n"
    "    potentials = [r for r in rows if r.shape == POTENTIAL]\n",
    "    walled = [r for r in rows if r.wall is not None]\n"
    "    carriers = [r for r in rows if r.shape == CARRIER]\n"
    "    potentials = [r for r in rows if r.shape == POTENTIAL]\n"
    "    if GENERIC:  # un2 (L): the plane at the universe's own pair (den, den), the potential's; a duplicate pair among the planes refused\n"
    "        gap0 = [r for r in rows if r.shape == PLANE and r.pair == (den, den)]\n"
    "    else:\n"
    "        gap0 = [r for r in rows if r.shape == PLANE and r.gap == 0]\n",
)
replace(
    "rows.py",
    "    if not any(r.shape == PLANE and r.gap is not None and r.gap > 0 for r in rows):\n",
    "    if GENERIC:\n"
    "        planes = [r.pair for r in rows if r.shape == PLANE]\n"
    "        if len(set(planes)) != len(planes):\n"
    '            raise ValueError("two planes at one pair: the universe names every pair once")\n'
    "    if not any(r.shape == PLANE and (r.pair != (den, den) if GENERIC else (r.gap is not None and r.gap > 0)) for r in rows):\n",
)
# R5 plane_of: the one plane at a pair (E)
replace(
    "rows.py",
    "def walled_of(rows: list[Row]) -> Row:\n",
    "def plane_of(rows: list[Row], pair: tuple[int, int]) -> Row:\n"
    '    """un2 (E): the one plane whose pair is the pair given, a lookup by the pairs\' values alone (the emitter: the plane of the potential\'s pair)."""\n'
    "    return next(r for r in rows if r.shape == PLANE and r.pair == pair)\n\n\n"
    "def coupling_of(row: Row) -> int:\n"
    '    """un2 (C): a plane\'s coupling to the Links\' phase as one function of its pair, min(den - num, 1): 0 at the pair with no gap (the turn the identity, the orbit\'s pair at the count 0), 1 at every other pair; the law\'s letter K = omega_0 Gamma over Gamma (Y-S1) is the function\'s general form, this engine\'s record its two values."""\n'
    "    assert row.gap is not None\n"
    "    return min(row.gap, 1)\n\n\n"
    "def walled_of(rows: list[Row]) -> Row:\n",
)

# ---- node.py: the emitter, the unit, the gapped list

replace(
    "node.py",
    "from event_universe.rows import (\n    CARRIER,\n    HALF_WIDTH,\n    PLANE,\n",
    "from event_universe.rows import (\n    CARRIER,\n    GENERIC,\n    HALF_WIDTH,\n    PLANE,\n    POTENTIAL,\n    plane_of,\n",
)
replace(
    "node.py",
    "        self.gapped = [r for r in self.records() if r.gap is not None and r.gap > 0]\n"
    "        self.units = [\n"
    "            unit_of(sine_den(r.pair[0], self.den) if r.gap else self.den, self.T)\n"
    "            for r in self.records()\n"
    "            if r.pair\n"
    "        ]\n"
    "        self.unit_gap0 = self.units[self.records().index(self.row(PLANE, gap=0))]\n",
    "        if GENERIC:  # un2 (U, E): the unit one function of the pair, the emitter a lookup by the pairs\n"
    "            self.gapped = [r for r in self.records() if r is not self.emitter()]\n"
    "            self.units = [\n"
    "                unit_of(sine_den(r.pair[0], self.den) + self.den * quotient(r.pair[0], self.den), self.T)\n"
    "                for r in self.records()\n"
    "                if r.pair\n"
    "            ]\n"
    "        else:\n"
    "            self.gapped = [r for r in self.records() if r.gap is not None and r.gap > 0]\n"
    "            self.units = [\n"
    "                unit_of(sine_den(r.pair[0], self.den) if r.gap else self.den, self.T)\n"
    "                for r in self.records()\n"
    "                if r.pair\n"
    "            ]\n"
    "        self.unit_gap0 = self.units[self.records().index(self.emitter())]\n",
)
replace(
    "node.py",
    "from event_universe.core.rule3 import carried_division, half, link_unit_of, mirrored, unit_of, wall_of\n",
    "from event_universe.core.rule3 import (\n    carried_division,\n    half,\n    link_unit_of,\n    mirrored,\n    quotient,\n    unit_of,\n    wall_of,\n)\n",
)
replace(
    "node.py",
    "    def walled(self) -> Row:\n",
    "    def emitter(self) -> Row:\n"
    '        """un2 (E): the plane the Wronskian\'s change is laid on and whose quanta the Link close takes, the plane of the potential\'s pair (gn2: the emitter is the plane of the writer\'s own pair); off the flag, David\'s pick by the gap 0."""\n'
    "        if GENERIC:\n"
    "            return plane_of(self.rows_, self.row(POTENTIAL).pair)\n"
    "        return self.row(PLANE, gap=0)\n\n"
    "    def walled(self) -> Row:\n",
)

# ---- close.py: the emitter, the taken row's unit as an argument (T)

replace(
    "close.py",
    "def meet(\n    node: Node, taken: Line, sh: Any, rules: list[tuple[Line, rule3.Rule]], frozen: Any\n) -> list[Birth]:\n",
    "def meet(\n    node: Node, taken: Line, sh: Any, rules: list[tuple[Line, rule3.Rule]], frozen: Any, unit: int\n) -> list[Birth]:\n",
)
replace(
    "close.py",
    "            if frozen[j] or int(sh[at]) < node.unit_gap0 or int(sh[j]) < node.unit_gap0:\n",
    "            if frozen[j] or int(sh[at]) < unit or int(sh[j]) < unit:\n",
)
replace(
    "close.py",
    "            drawn = read_number(node, into, rules)\n",
    "            drawn = read_number(node, into, rules, unit)\n",
)
replace(
    "close.py",
    "                    remainder(quotient(number, node.unit_gap0), len(node.records())),\n",
    "                    remainder(quotient(number, unit), len(node.records())),\n",
)
replace(
    "close.py",
    "    gap0 = node.row(PLANE, gap=0)\n    r_gap0 = node.rule_of(gap0, c, factors)\n",
    "    gap0 = node.emitter()\n    r_gap0 = node.rule_of(gap0, c, factors)\n",
)
replace(
    "close.py",
    "    sh = owns[node.records().index(gap0)]\n"
    "    born_nodes = births(\n"
    "        node, refuse(node, meet(node, gap0_start[0], sh, rules, frozen), owns), r_gap0, c, factors, pace\n    )\n",
    "    rec = node.records().index(gap0)\n"
    "    sh = owns[rec]\n"
    "    born_nodes = births(\n"
    "        node,\n"
    "        refuse(node, meet(node, gap0_start[0], sh, rules, frozen, node.units[rec]), owns),\n"
    "        r_gap0,\n"
    "        c,\n"
    "        factors,\n"
    "        pace,\n"
    "    )\n",
)
replace(
    "close.py",
    "    gap0 = node.row(PLANE, gap=0)\n    rec0 = node.records().index(gap0)\n",
    "    gap0 = node.emitter()\n    rec0 = node.records().index(gap0)\n",
)

# ---- take.py: the taken row's unit as an argument, the emitter

replace(
    "take.py",
    "def read_number(\n    node: Node, at: tuple[int, ...], rules: list[tuple[Line, rule3.Rule]]\n) -> tuple[int, int] | None:\n",
    "def read_number(\n    node: Node, at: tuple[int, ...], rules: list[tuple[Line, rule3.Rule]], unit: int\n) -> tuple[int, int] | None:\n",
)
replace(
    "take.py",
    "    modulus = node.unit_gap0 * len(node.records())\n",
    "    modulus = unit * len(node.records())\n",
)
replace(
    "take.py",
    "    gap0 = node.row(PLANE, gap=0)\n    z = gap0.lines[0]\n",
    "    gap0 = node.emitter()\n    z = gap0.lines[0]\n",
)

# ---- interval.py: the emitter, the coupling-weighted loops, the turn at the coupling

replace(
    "interval.py",
    "from event_universe.rows import CARRIER, PLANE, POTENTIAL, TRACE, Line, Row, zeros\n",
    "from event_universe.rows import CARRIER, GENERIC, " + "PLANE, POTENTIAL, TRACE, Line, Row, coupling_of, zeros\n",
)
replace(
    "interval.py",
    "        self.potential, self.gap0 = node.row(POTENTIAL), node.row(PLANE, gap=0)\n"
    "        self.riders = [r for r in node.rows_ if r.wall is None and r is not self.carrier]\n"
    "        self.gap_planes = [r for r in self.riders if r.shape == PLANE and r.gap]\n",
    "        self.potential, self.gap0 = node.row(POTENTIAL), node.emitter()\n"
    "        self.riders = [r for r in node.rows_ if r.wall is None and r is not self.carrier]\n"
    "        if GENERIC:  # un2 (C): every plane with its coupling, no plane left out by a test\n"
    "            self.planes = [(r, coupling_of(r)) for r in self.riders if r.shape == PLANE]\n"
    "        else:\n"
    "            self.planes = [(r, 1) for r in self.riders if r.shape == PLANE and r.gap]\n",
)
# the Links at every coupling value of the file's planes (count and odd part multiplied by c; one record per value)
replace(
    "interval.py",
    "        self.links = links_of(self.factors, self.frames, self.phases, self.odd)\n",
    "        self.links = links_of(self.factors, self.frames, self.phases, self.odd)\n"
    "        if GENERIC:  # un2 (C): the Link's record at each coupling value, the count and the odd part times c\n"
    "            self.links_at = {\n"
    "                c: (\n"
    "                    self.links\n"
    "                    if c == 1\n"
    "                    else links_of(\n"
    "                        self.factors,\n"
    "                        self.frames,\n"
    "                        readings.link_phases(node, self.frames, count * c),\n"
    "                        [o * c for o in self.odd],\n"
    "                    )\n"
    "                )\n"
    "                for c in sorted({c for _r, c in self.planes})\n"
    "            }\n",
)
replace(
    "interval.py",
    "        for r in self.gap_planes:\n"
    "            self.w_end = self.w_end + wronskian(*self.lines(r))\n"
    "            re_s, im_s = [Line(self.at(line), None, None, line.wall) for line in self.lines(r)]\n"
    "            for a, j_a in enumerate(plane_current(re_s, im_s, self.frames)):\n"
    "                self.current[a] = self.current[a] + j_a\n",
    "        for r, cpl in self.planes:\n"
    "            self.w_end = self.w_end + cpl * wronskian(*self.lines(r))\n"
    "            re_s, im_s = [Line(self.at(line), None, None, line.wall) for line in self.lines(r)]\n"
    "            for a, j_a in enumerate(plane_current(re_s, im_s, self.frames)):\n"
    "                self.current[a] = self.current[a] + cpl * j_a\n",
)
replace(
    "interval.py",
    "            turn = self.links if r.shape == PLANE and r.gap else None\n",
    "            if GENERIC:\n"
    "                turn = self.links_at[coupling_of(r)] if r.shape == PLANE else None\n"
    "            else:\n"
    "                turn = self.links if r.shape == PLANE and r.gap else None\n",
)
replace(
    "interval.py",
    "        for r in self.gap_planes:\n"
    "            (re_s, im_s), (f_re, f_im) = self.starts[self.where[id(r)]], self.force[self.where[id(r)]]\n"
    "            self.emission = self.emission + self.x_now * (re_s * f_im - im_s * f_re)\n",
    "        for r, cpl in self.planes:\n"
    "            (re_s, im_s), (f_re, f_im) = self.starts[self.where[id(r)]], self.force[self.where[id(r)]]\n"
    "            self.emission = self.emission + cpl * self.x_now * (re_s * f_im - im_s * f_re)\n",
)
replace(
    "interval.py",
    "                if r.gap:\n"
    "                    self.w_after = self.w_after + wronskian(*after)\n",
    "                cpl = coupling_of(r) if GENERIC else (1 if r.gap else 0)\n"
    "                self.w_after = self.w_after + cpl * wronskian(*after)\n",
)

# ---- seed.py: the loader's forms by the pair's value; the hole's row the sea's (L)

replace(
    "seed.py",
    "from event_universe.rows import PLANE, Line, Row, zeros\n",
    "from event_universe.rows import GENERIC, PLANE, Line, Row, zeros\n",
)
replace(
    "seed.py",
    "    packets = []\n    for lay in lays:\n",
    "    packets = []\n    sea_rows: list[Row] = []\n    for lay in lays:\n",
)
replace(
    "seed.py",
    "        if form == \"sea\":\n"
    "            if row is None or row.gap != 0:\n"
    "                raise ValueError(\"a sea is the plane at the gap 0 alone: the drift is its double root\")\n"
    "            node.lay(node.records().index(row), Ellipsis, (node.drift, 0, 0, 0))\n"
    "        elif form == \"hole\":\n"
    "            at = node.node_of(lay[\"at\"])\n"
    "            node.lay(node.records().index(node.row(PLANE, gap=0)), at, (-node.drift, 0, 0, 0))\n",
    "        if form == \"sea\":\n"
    "            if row is None or (row is not node.emitter() if GENERIC else row.gap != 0):\n"
    "                raise ValueError(\"a sea is the plane at the gap 0 alone: the drift is its double root\")\n"
    "            sea_rows.append(row)\n"
    "            node.lay(node.records().index(row), Ellipsis, (node.drift, 0, 0, 0))\n"
    "        elif form == \"hole\":\n"
    "            at = node.node_of(lay[\"at\"])\n"
    "            if GENERIC:  # un2 (L): a hole takes the sea back at one Node: its row is the sea's, the last sea laid\n"
    "                if not sea_rows:\n"
    "                    raise ValueError(\"a hole takes a sea back: no sea laid before it\")\n"
    "                node.lay(node.records().index(sea_rows[-1]), at, (-node.drift, 0, 0, 0))\n"
    "            else:\n"
    "                node.lay(node.records().index(node.row(PLANE, gap=0)), at, (-node.drift, 0, 0, 0))\n",
)
replace(
    "seed.py",
    "            if row.gap == 0:\n                node.lay(node.records().index(row), at, (n * node.drift, 0, 0, 0))\n",
    "            if row is node.emitter() if GENERIC else row.gap == 0:  # the pair with no rest: its packet N drifts (the loader's case)\n"
    "                node.lay(node.records().index(row), at, (n * node.drift, 0, 0, 0))\n",
)

# ---- run.py: the reader's picks of the emitter

replace(
    "run.py",
    "        if row.gap == 0:\n            continue\n",
    "        if row is node.emitter():\n            continue\n",
)
replace(
    "run.py",
    "    metric, potential, gap0 = node.row(CARRIER), node.row(POTENTIAL), node.row(PLANE, gap=0).lines[0]\n",
    "    metric, potential, gap0 = node.row(CARRIER), node.row(POTENTIAL), node.emitter().lines[0]\n",
)
replace(
    "run.py",
    "        \"gap-0 W abs max\": max(abs(x) for x in ints(wronskian(*node.row(PLANE, gap=0).lines))),\n",
    "        \"gap-0 W abs max\": max(abs(x) for x in ints(wronskian(*node.emitter().lines))),\n",
)
replace(
    "run.py",
    "    gap0 = node.row(PLANE, gap=0).lines[0]\n    return {\n",
    "    gap0 = node.emitter().lines[0]\n    return {\n",
)

print("written", DST, "replacements", count)
