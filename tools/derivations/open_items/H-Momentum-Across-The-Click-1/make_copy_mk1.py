"""mk1's flagged copy of src: the recoil at the click (MK-S1) behind the flag MK1_RECOIL=1 in three files
(take.py: the act `recoil`; bodies.py: the kick on the credited row at the take's Node; close.py: the kick on the
children's row at a birth and the kick undone in `unclick` from the booked line). The flag absent is the head bit
for bit. With the argument `built`, the same copy with the flag removed (the act always on), the source of mk1.patch.
Run: python make_copy_mk1.py [built]."""
import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", "..", ".."))
SRC = os.path.join(ROOT, "src", "event_universe")
BUILT = len(sys.argv) > 1 and sys.argv[1] == "built"
OUT = os.path.join(HERE, "src_mk1_built" if BUILT else "src_mk1")
DST = os.path.join(OUT, "event_universe")
if os.path.isdir(OUT):
    shutil.rmtree(OUT)
os.makedirs(OUT)
shutil.copytree(SRC, DST, ignore=shutil.ignore_patterns("__pycache__"))

FLAG = "True" if BUILT else 'os.environ.get("MK1_RECOIL") == "1"'


def replace_once(path, old, new):
    text = open(path, encoding="utf-8").read()
    if text.count(old) != 1:
        sys.exit(f"the site is not unique in {path}: {old[:70]!r} ({text.count(old)})")
    open(path, "w", encoding="utf-8").write(text.replace(old, new))


# take.py: the act
p = os.path.join(DST, "take.py")
replace_once(
    p,
    "from event_universe.core.rule3 import half, lattice, mirrored, quotient, remainder\n",
    "from event_universe.core.rule3 import division_forward, half, lattice, mirrored, quotient, remainder\n",
)
replace_once(
    p,
    '''def take_at(''',
    '''def recoil(node: Node, rec: int, at: tuple[int, ...], dp_take: list[int]) -> tuple[int, list[int], int]:
    """MK-S1, the momentum across the click (Compton's recoil): the row the taken quantum passes into is kicked at the take's Node on its first line, as the take moved the taken row's first line there, by q levels of its level now (its velocity, the kick's momentum form: P_out = P_in + W q), q the nearest quotient of the kick's numerator -(dP_take . Gb) at the wall 2 num (Gb . Gb), Gb the line's before gradient at the Node per axis (the same reads `momentum_of` makes: before at the -a neighbour less before at the +a neighbour), so the row's lattice momentum changes by 2 num q Gb, the part of -dP_take along the line's own gradient to the nearest level; q 0 where the gradient is 0 (a flat line holds no momentum at the Node); the kick's lattice momentum booked (`momentum_of`), the inverse the same lay at -q from the booked line. Returns (q, dP_recoil, the wall)."""
    row = node.records()[rec]
    assert row.pair is not None
    line, num = row.lines[0], row.pair[0]
    gradient = []
    for a in range(AXES):
        up, down = neighbour(node, at, 2 * a), neighbour(node, at, 2 * a + 1)
        gradient.append(int(line.before[down]) - int(line.before[up]))
    wall = 2 * num * sum(g * g for g in gradient)
    if wall == 0:
        return 0, [0] * AXES, 0
    numerator = -sum(d * g for d, g in zip(dp_take, gradient, strict=True))
    q = int(division_forward(numerator, wall, half(wall))[0])
    dp = momentum_of(node, line.now, line.before, at, d_now=q, num=num)
    lay(node, rec, at, (q,) + (0,) * (2 * row.shape - 1))
    return q, dp, wall


def take_at(''',
)

# bodies.py: the kick on the credited row where the take stands
p = os.path.join(DST, "bodies.py")
replace_once(p, "from __future__ import annotations\n\n", "from __future__ import annotations\n\nimport os\n")
replace_once(
    p,
    "from event_universe.take import frame_nodes, lay, take_at\n",
    "from event_universe.take import frame_nodes, lay, recoil, take_at\n",
)
replace_once(
    p,
    """                entry["laid_back"], entry["dP_take"] = levels, [0] * AXES
                node.counts["laid_back"] += 1
            node.log.append(entry)""",
    """                entry["laid_back"], entry["dP_take"] = levels, [0] * AXES
                node.counts["laid_back"] += 1
            elif FLAG:
                kicked(node, entry, recoil(node, rec, at, node.last_dp))
            node.log.append(entry)


def kicked(node: Node, entry: dict[str, Any], got: tuple[int, list[int], int]) -> None:
    \"\"\"MK-S1: the kick's numbers booked on the click's line (the levels q, the lattice momentum it books, the wall) and counted (the kicks moved, the flat ones).\"\"\"
    q, dp, wall = got
    entry["kick"], entry["dP_recoil"], entry["kick_wall"] = q, dp, wall
    node.counts["recoil"] = node.counts.get("recoil", 0) + (q != 0)
    node.counts["recoil_flat"] = node.counts.get("recoil_flat", 0) + (wall == 0)""".replace("FLAG", FLAG),
)

# close.py: the kick on the children's row at a birth; the kick undone
p = os.path.join(DST, "close.py")
replace_once(p, "from __future__ import annotations\n\n", "from __future__ import annotations\n\nimport os\n")
replace_once(
    p,
    "from event_universe.bodies import bodies\n",
    "from event_universe.bodies import bodies, kicked\n",
)
replace_once(
    p,
    "from event_universe.take import fall_of, lay, momentum_of, neighbour, read_number, take_at\n",
    "from event_universe.take import fall_of, lay, momentum_of, neighbour, read_number, recoil, take_at\n",
)
replace_once(
    p,
    """        dp_lay, w_children, stood = child_laid(node, s, minus, plus)
        touched |= {minus, plus}
        node.counts["births"] += 1
        node.closes[at] += 1
        node.log.append(
            {""",
    """        dp_lay, w_children, stood = child_laid(node, s, minus, plus)
        touched |= {minus, plus}
        node.counts["births"] += 1
        node.closes[at] += 1
        entry: dict[str, Any] = {}
        if FLAG:
            kicked(node, entry, recoil(node, s, at, take["dP_take"]))
        node.log.append(
            {
                **entry,""".replace("FLAG", FLAG),
)
replace_once(
    p,
    """        at = tuple(entry["node"])
        if entry["event"] == "birth":
            s, (a, b) = entry["line_pair"], entry["amplitude"]""",
    """        at = tuple(entry["node"])
        if "kick" in entry:
            kicked_row = entry["line_pair"] if entry["event"] == "birth" else entry["line"]
            lay(node, kicked_row, at, (entry["kick"],) + (0,) * (2 * node.records()[kicked_row].shape - 1), -1)
        if entry["event"] == "birth":
            s, (a, b) = entry["line_pair"], entry["amplitude"]""",
)
if BUILT:  # the flag removed: the act's lines stand plain, no os import
    for name, olds in (
        ("bodies.py", (("import os\n", ""), ("            elif True:\n", "            else:\n"))),
        ("close.py", (("import os\n", ""), ("        if True:\n            kicked(", "        kicked("))),
    ):
        for old, new in olds:
            replace_once(os.path.join(DST, name), old, new)
print("written:", DST, "flag" if not BUILT else "built (the flag removed)")
