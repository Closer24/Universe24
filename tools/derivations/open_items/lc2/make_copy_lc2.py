"""lc2's flagged COPY of the engine (src/event_universe at 32b56254b), written by this script and never by hand, under tools/derivations/lc2/src_lc2/.
One act changes behind the flag LC2_REACH (an environment variable, absent = David's path bit for bit): Node.rule reads the Link's pace from the two ends.
Forms: 'harmonic' (the division at the Link's mean wall: p_ij^2 = rounded(2 p_i^2 p_j^2, p_i^2 + p_j^2), equal to Gamma^3 over the mean volume (X_i + X_j) div 2 to the rounding),
'product' (bg2's (d): p_i p_j), 'mean' (the mean pace rounded(p_i + p_j, 2) squared). Every replacement must match exactly once, else the script refuses."""
import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "..", "..", "..", "src", "event_universe")
DST_ROOT = os.path.join(HERE, sys.argv[1] if len(sys.argv) > 1 else "src_lc2")
DST = os.path.join(DST_ROOT, "event_universe")

if os.path.exists(DST_ROOT):
    shutil.rmtree(DST_ROOT)
shutil.copytree(SRC, DST, ignore=shutil.ignore_patterns("__pycache__"))

path = os.path.join(DST, "node.py")
text = open(path, encoding="utf-8").read()
replacements = []
replacements.append((
    "import hashlib\nfrom typing import Any\n",
    "import hashlib\nimport os\nfrom typing import Any\n",
))
replacements.append((
    '''        clock, pace = readings.paces_of(self, c)
        return rule3.rule_integers(pair[0], pair[1], self.gamma, clock, pace, factors, self.G)
''',
    '''        clock, pace = readings.paces_of(self, c)
        form = os.environ.get("LC2_REACH", "")
        if form:
            return lc2_rule(self, pair, clock, pace, factors, form)
        return rule3.rule_integers(pair[0], pair[1], self.gamma, clock, pace, factors, self.G)
''',
))
replacements.append((
    "class Node:\n",
    '''def lc2_link_pace_squared(pace: Any, port: int, form: str) -> Any:
    """lc2: the Link's pace squared read the same from both ends, one integer per Link (a coefficient of the interval, rounded once, no remainder, as the Link's factor Q_ij): 'harmonic' the division at the Link's mean wall, rounded(2 p_i^2 p_j^2, p_i^2 + p_j^2) = Gamma^3 over the two ends' mean volume to the rounding, 0 where both ends are frozen; 'product' p_i p_j; 'mean' rounded(p_i + p_j, 2) squared."""
    other = across(pace, port) if np.ndim(pace) else pace
    if form == "product":
        return pace * other
    if form == "mean":
        m = paces.rounded(pace + other, 2)
        return m * m
    if form == "harmonic":
        a, b = pace * pace, other * other
        wall = a + b
        if np.ndim(wall):
            wall = np.where(wall == 0, 1, wall)
        elif wall == 0:
            wall = 1
        return paces.rounded(2 * a * b, wall)
    raise ValueError(f"lc2: a reach form of no derivation: {form!r}")


def lc2_rule(node: Any, pair: tuple[int, int], clock: Any, pace: Any, factors: tuple[Any, ...], form: str) -> rule3.Rule:
    """lc2: Rule3's integers with the reach R_ij = 2 num P_ij Q_ij G^2, P_ij the Link's pace squared from the two ends (lc2_link_pace_squared), one number from both ends; w and D as written; S = 2 w - D - SUM R."""
    num, den = pair
    square = node.G * node.G
    links = (square,) * PORTS if factors is None else factors
    reaches = tuple(2 * lc2_link_pace_squared(pace, port, form) * factor * num for port, factor in enumerate(links))
    wall, own = rule3.wall_of(den, node.gamma, node.G), rule3.mass(num, den, clock, node.G)
    return rule3.Rule(reaches, wall + wall - own - sum(reaches), wall, own)


class Node:
''',
))
for old, new in replacements:
    if text.count(old) != 1:
        sys.exit(f"refused: the text occurs {text.count(old)} times: {old[:60]!r}")
    text = text.replace(old, new)
open(path, "w", encoding="utf-8").write(text)
if "b" in sys.argv[2:]:
    # the b copy adds ONE READING (no act, no state): the interval's forms kept on the Node for the course reader
    ip = os.path.join(DST, "interval.py")
    it = open(ip, encoding="utf-8").read()
    old = "            self.kicked[k] = p_other\n"
    new = "            self.kicked[k] = p_other\n        node.lc2_forms = self.forms  # lc2 b: a reading alone, the forms summed over the riding lines\n"
    if it.count(old) != 1:
        sys.exit("refused: kicks' tail not found once")
    open(ip, "w", encoding="utf-8").write(it.replace(old, new))
    print("b: the forms reading added to interval.py")
print("written", DST, "replacements", len(replacements))
