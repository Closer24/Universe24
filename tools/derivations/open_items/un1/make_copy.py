"""un1's flagged COPY of src/event_universe (engine-5.0-test 4468c0970), written by this script and never by hand, under
tools/derivations/un1/src_un1/event_universe. The flag: the environment variable UN1_FREE=1, read once in rows.py (FREE); absent,
every act runs David's text bit for bit (the replacements add functions and route the picks through them, the off path David's).
Under the flag every branch on the gap in the acts is read as the VALUE of one function of the pair or of the rows' list:
  (a) the emitter: the plane whose pair is the potential's (rows.emitter_of), in place of row(PLANE, gap=0) at nine sites;
  (b) the unit: unit_of(leg_of(num, den), T), leg_of the pair's sine where above 0 and den where the pair has no leg, as one
      arithmetic s + den (1 - min(s, 1)) (row 12's two cases as one function's two values);
  (c) the coupling c(pair) = min(den - num, 1) in {0, 1} (Row.coupling): the turn of every plane by the six Links' records at the
      coupling c (Interval.coupled: frame 1 + c (f - 1), cos X + c (cos - X), sin c sin, odd c n; c = 0 the identity by arithmetic);
      the order key (1, shape, 1 - c) compared, not tested;
  (d) the sums over the planes (the Wronskian, the current, the emission, the Wronskian after) over EVERY plane, the emitter among
      them (its im line is 0 at every interval, so its terms are 0 by arithmetic);
  (e) the loader's refusals by the pairs (a duplicate pair refused; one plane at the potential's pair; two planes at least), the
      sea's and the hole's row the emitter, the reader's skip the emitter.
Every replacement must match the source text exactly once, else the script refuses. Run: python make_copy.py"""

import os
import shutil

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "..", "..", "..", "src", "event_universe")
DST_ROOT = os.path.join(HERE, "src_un1")
DST = os.path.join(DST_ROOT, "event_universe")

if os.path.isdir(DST_ROOT):
    shutil.rmtree(DST_ROOT)
shutil.copytree(SRC, DST, ignore=shutil.ignore_patterns("__pycache__"))

REPLACEMENTS = {
    "rows.py": [
        (
            "from __future__ import annotations\n\nfrom typing import Any\n",
            "from __future__ import annotations\n\nimport os\nfrom typing import Any\n",
        ),
        (
            "from event_universe.core.rule3 import half, held_wall, quotient\n",
            "from event_universe.core.paces import sine_den\nfrom event_universe.core.rule3 import half, held_wall, quotient\n\nFREE = os.environ.get(\"UN1_FREE\") == \"1\"  # un1's flag: the branches on the gap read as values of one function; off, David's path\n",
        ),
        (
            "        return None if self.pair is None else self.pair[1] - self.pair[0]\n",
            "        return None if self.pair is None else self.pair[1] - self.pair[0]\n\n    @property\n    def coupling(self) -> int | None:\n        \"\"\"un1: the coupling c(pair) = min(den - num, 1): 1 for a pair with a gap, 0 at (den, den), None for the row with its own wall.\"\"\"\n        return None if self.pair is None else min(self.pair[1] - self.pair[0], 1)\n",
        ),
        (
            "def order_of(row: Row) -> int:\n    \"\"\"The acts' order: a row whose write reads other rows comes after them: the row with its own wall, the planes with a gap, the plane at the gap 0 (its lay reads the planes' Wronskian), the shape-4 row, the carrier.\"\"\"\n    if row.wall is not None:\n",
            "def order_of(row: Row) -> Any:\n    \"\"\"The acts' order: a row whose write reads other rows comes after them: the row with its own wall, the planes with a gap, the plane at the gap 0 (its lay reads the planes' Wronskian), the shape-4 row, the carrier. un1: a tuple compared, (0, 0, 0) for the walled row, (1, shape, 1 - c) for a pair row, c the coupling: the coupled planes before the uncoupled one, the shapes rising.\"\"\"\n    if FREE:\n        return (0, 0, 0) if row.wall is not None else (1, row.shape, 1 - row.coupling)\n    if row.wall is not None:\n",
        ),
        (
            "    rows = sorted(by_index, key=order_of)\n    walled = [r for r in rows if r.wall is not None]\n    gap0 = [r for r in rows if r.shape == PLANE and r.gap == 0]\n    carriers = [r for r in rows if r.shape == CARRIER]\n    potentials = [r for r in rows if r.shape == POTENTIAL]\n",
            "    rows = sorted(by_index, key=order_of)\n    walled = [r for r in rows if r.wall is not None]\n    carriers = [r for r in rows if r.shape == CARRIER]\n    potentials = [r for r in rows if r.shape == POTENTIAL]\n    if FREE:\n        planes = [r for r in rows if r.shape == PLANE]\n        if len({r.pair for r in planes}) != len(planes):\n            raise ValueError(\"two planes at one pair: the same row twice\")\n        gap0 = [r for r in planes if len(potentials) == 1 and r.pair == potentials[0].pair]\n    else:\n        gap0 = [r for r in rows if r.shape == PLANE and r.gap == 0]\n",
        ),
        (
            "    if not any(r.shape == PLANE and r.gap is not None and r.gap > 0 for r in rows):\n        raise ValueError(\"the universe names no plane row with a gap\")\n    return rows, by_index\n",
            "    if FREE:\n        if sum(1 for r in rows if r.shape == PLANE) < 2:\n            raise ValueError(\"the universe names no plane beside the emitter's\")\n    elif not any(r.shape == PLANE and r.gap is not None and r.gap > 0 for r in rows):\n        raise ValueError(\"the universe names no plane row with a gap\")\n    return rows, by_index\n\n\ndef emitter_of(rows: list[Row]) -> Row:\n    \"\"\"un1: the emitter, the plane whose pair is the potential's (the row the potential's write lights, the row the Links' meeting takes, the sea's row), found by the pairs' equality and no gap.\"\"\"\n    potential = row_of(rows, POTENTIAL)\n    return next(r for r in rows if r.shape == PLANE and r.pair == potential.pair)\n\n\ndef leg_of(num: int, den: int) -> int:\n    \"\"\"un1: the leg a row's unit is read at (row 12 of The conventions and the units as one function): the pair's sine s = largest_below(den^2 - num^2) where it is above 0, den where the pair has no leg (the massless case, the law's clause by number), as one arithmetic s + den (1 - min(s, 1)); equal to sine_den(num mod den, den) on 0 <= num <= den.\"\"\"\n    s = sine_den(num, den)\n    return s + den * (1 - min(s, 1))\n",
        ),
    ],
    "node.py": [
        (
            "from event_universe.rows import (\n    CARRIER,\n    HALF_WIDTH,\n    PLANE,\n    Line,\n    Row,\n    records_of,\n    row_of,\n    rows_of,\n    walled_of,\n    zeros,\n)\n",
            "from event_universe.rows import (\n    CARRIER,\n    FREE,\n    HALF_WIDTH,\n    PLANE,\n    Line,\n    Row,\n    emitter_of,\n    leg_of,\n    records_of,\n    row_of,\n    rows_of,\n    walled_of,\n    zeros,\n)\n",
        ),
        (
            "            unit_of(sine_den(r.pair[0], self.den) if r.gap else self.den, self.T)\n",
            "            unit_of(\n                leg_of(r.pair[0], self.den) if FREE else (sine_den(r.pair[0], self.den) if r.gap else self.den),\n                self.T,\n            )\n",
        ),
        (
            "        self.unit_gap0 = self.units[self.records().index(self.row(PLANE, gap=0))]\n",
            "        self.unit_gap0 = self.units[self.records().index(self.emitter())]\n",
        ),
        (
            "    def walled(self) -> Row:\n",
            "    def emitter(self) -> Row:\n        \"\"\"un1: the emitter (the taken row, the sea's row, W-S1's row): the plane of the potential's pair under the flag; David's pick by the gap 0 off.\"\"\"\n        return emitter_of(self.rows_) if FREE else self.row(PLANE, gap=0)\n\n    def walled(self) -> Row:\n",
        ),
    ],
    "interval.py": [
        (
            "from event_universe.links import links_of, plane_current, stress_parts, tensor_parts, wronskian\nfrom event_universe.rows import CARRIER, PLANE, POTENTIAL, TRACE, Line, Row, zeros\n",
            "from event_universe.links import Link, links_of, plane_current, stress_parts, tensor_parts, wronskian\nfrom event_universe.rows import CARRIER, FREE, PLANE, POTENTIAL, TRACE, Line, Row, zeros\n",
        ),
        (
            "        self.potential, self.gap0 = node.row(POTENTIAL), node.row(PLANE, gap=0)\n        self.riders = [r for r in node.rows_ if r.wall is None and r is not self.carrier]\n        self.gap_planes = [r for r in self.riders if r.shape == PLANE and r.gap]\n",
            "        self.potential, self.gap0 = node.row(POTENTIAL), node.emitter()\n        self.riders = [r for r in node.rows_ if r.wall is None and r is not self.carrier]\n        self.gap_planes = [r for r in self.riders if r.shape == PLANE and (FREE or r.gap)]\n",
        ),
        (
            "            turn = self.links if r.shape == PLANE and r.gap else None\n",
            "            turn = (self.coupled(r.coupling) if FREE else (self.links if r.gap else None)) if r.shape == PLANE else None\n",
        ),
        (
            "    def mean_wall(self) -> Any:\n",
            "    def coupled(self, c: int) -> list[Link]:\n        \"\"\"un1: the six Links' records at a plane's coupling c in {0, 1}: (frame, cos, sin, odd) -> (1 + c (f - 1), X + c (cos - X), c sin, c n); at c = 1 the Links as read, at c = 0 the identity turn by arithmetic (the frame 1, the pair (X, 0) over X, the odd part 0).\"\"\"\n        x = self.node.X\n        return [\n            Link(k.factor, 1 + c * (k.frame - 1), x + c * (k.cosine - x), c * k.sine, c * k.odd)\n            for k in self.links\n        ]\n\n    def mean_wall(self) -> Any:\n",
        ),
        (
            "                if r.gap:\n                    self.w_after = self.w_after + wronskian(*after)\n",
            "                if FREE or r.gap:\n                    self.w_after = self.w_after + wronskian(*after)\n",
        ),
    ],
    "close.py": [
        (
            "    gap0 = node.row(PLANE, gap=0)\n    r_gap0 = node.rule_of(gap0, c, factors)\n",
            "    gap0 = node.emitter()\n    r_gap0 = node.rule_of(gap0, c, factors)\n",
        ),
        (
            "    gap0 = node.row(PLANE, gap=0)\n    rec0 = node.records().index(gap0)\n",
            "    gap0 = node.emitter()\n    rec0 = node.records().index(gap0)\n",
        ),
    ],
    "take.py": [
        (
            "    gap0 = node.row(PLANE, gap=0)\n    z = gap0.lines[0]\n",
            "    gap0 = node.emitter()\n    z = gap0.lines[0]\n",
        ),
    ],
    "run.py": [
        (
            "from event_universe.rows import CARRIER, PLANE, POTENTIAL, zeros\n",
            "from event_universe.rows import CARRIER, FREE, PLANE, POTENTIAL, zeros\n",
        ),
        (
            "        if row.gap == 0:\n            continue\n",
            "        if (row is node.emitter()) if FREE else (row.gap == 0):\n            continue\n",
        ),
        (
            "    metric, potential, gap0 = node.row(CARRIER), node.row(POTENTIAL), node.row(PLANE, gap=0).lines[0]\n",
            "    metric, potential, gap0 = node.row(CARRIER), node.row(POTENTIAL), node.emitter().lines[0]\n",
        ),
        (
            "        \"gap-0 W abs max\": max(abs(x) for x in ints(wronskian(*node.row(PLANE, gap=0).lines))),\n",
            "        \"gap-0 W abs max\": max(abs(x) for x in ints(wronskian(*node.emitter().lines))),\n",
        ),
        (
            "    gap0 = node.row(PLANE, gap=0).lines[0]\n    return {\n",
            "    gap0 = node.emitter().lines[0]\n    return {\n",
        ),
    ],
    "seed.py": [
        (
            "from event_universe.rows import PLANE, Line, Row, zeros\n",
            "from event_universe.rows import FREE, PLANE, Line, Row, zeros\n",
        ),
        (
            "            if row is None or row.gap != 0:\n                raise ValueError(\"a sea is the plane at the gap 0 alone: the drift is its double root\")\n",
            "            if row is None or ((row is not node.emitter()) if FREE else (row.gap != 0)):\n                raise ValueError(\"a sea is the plane at the gap 0 alone: the drift is its double root\")\n",
        ),
        (
            "            node.lay(node.records().index(node.row(PLANE, gap=0)), at, (-node.drift, 0, 0, 0))\n",
            "            node.lay(node.records().index(node.emitter()), at, (-node.drift, 0, 0, 0))\n",
        ),
        (
            "            if row.gap == 0:\n                node.lay(node.records().index(row), at, (n * node.drift, 0, 0, 0))\n",
            "            if (row is node.emitter()) if FREE else (row.gap == 0):\n                node.lay(node.records().index(row), at, (n * node.drift, 0, 0, 0))\n",
        ),
    ],
}

count = 0
for name, pairs in REPLACEMENTS.items():
    path = os.path.join(DST, name)
    text = open(path, encoding="utf-8").read()
    for old, new in pairs:
        if text.count(old) != 1:
            raise SystemExit(f"{name}: the text to replace matches {text.count(old)} times, not once:\n{old}")
        text = text.replace(old, new)
        count += 1
    open(path, "w", encoding="utf-8").write(text)
print(f"the copy written under {DST}: {count} replacements, each matched once")
