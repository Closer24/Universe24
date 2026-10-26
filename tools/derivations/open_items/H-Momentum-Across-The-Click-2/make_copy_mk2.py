"""mk2's flagged copy of src: the recoil as a lay across the click's Link (MK-S2) behind the flag MK2_RECOIL=1 in three
files (take.py: the act `recoil`, the taker's first line's before at the far end of the Link moved by the nearest
quotient of the take's momentum along the Link's axis at the wall one level books; bodies.py: at a credit the Link of the
taken row's largest current at the Node; close.py: at a birth the Link the children stand on, and the lay undone in
`unclick` from the booked line). The flag absent is the head bit for bit. With the argument `built`, the same copy
with the flag removed, the source of mk2.patch. Run: python make_copy_mk2.py [built]."""
import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", "..", ".."))
SRC = os.path.join(ROOT, "src", "event_universe")
BUILT = len(sys.argv) > 1 and sys.argv[1] == "built"
OUT = os.path.join(HERE, "src_mk2_built" if BUILT else "src_mk2")
DST = os.path.join(OUT, "event_universe")
if os.path.isdir(OUT):
    shutil.rmtree(OUT)
os.makedirs(OUT)
shutil.copytree(SRC, DST, ignore=shutil.ignore_patterns("__pycache__"))

FLAG = "True" if BUILT else 'os.environ.get("MK2_RECOIL") == "1"'


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
    '''def recoil(
    node: Node, rec: int, at: tuple[int, ...], far: tuple[int, ...], dp_take: list[int]
) -> tuple[int, list[int], int, int]:
    """MK-S2, the momentum across the click as a lay across the click's Link (the two-Node form, OB-S1's letter): the row the taken quantum passes into has its first line's level before at the far end of the Link moved by p levels, p the nearest quotient of the take's momentum along the Link's axis, negated, at the wall one level books there (`momentum_of` at one level of before: 2 num times the line's now gradient along the axis at the far end, one of its two reads the taker's own level at the take's Node), so the row's lattice momentum along the Link's axis changes by the take's, negated, to the remainder of that one division, and across the two transverse axes by 2 num p times the line's now gradient there (0 where the row stands at nothing around the far end: a two-Node lay onto nothing carries momentum along its Link's axis alone); p 0 where the wall is 0; the lay's lattice momentum booked, the inverse the same lay at -p from the booked line. Returns (p, dP_recoil, the wall, the axis)."""
    row = node.records()[rec]
    assert row.pair is not None
    line, num = row.lines[0], row.pair[0]
    axes = [a for a in range(AXES) if far[a] != at[a]]
    if not axes:
        return 0, [0] * AXES, 0, -1
    axis = axes[0]
    wall = momentum_of(node, line.now, line.before, far, d_before=1, num=num)[axis]
    if wall == 0:
        return 0, [0] * AXES, 0, axis
    sign = 1 if wall > 0 else -1
    p = int(division_forward(-dp_take[axis] * sign, sign * wall, half(sign * wall))[0])
    dp = momentum_of(node, line.now, line.before, far, d_before=p, num=num)
    lay(node, rec, far, (0, p) + (0,) * (2 * row.shape - 2))
    return p, dp, wall, axis


def take_at(''',
)

# bodies.py: the lay across the Link of the taken row's largest current at the credited Node
p = os.path.join(DST, "bodies.py")
replace_once(p, "from __future__ import annotations\n\n", "from __future__ import annotations\n\nimport os\n")
replace_once(
    p,
    "from event_universe.take import frame_nodes, lay, take_at\n",
    "from event_universe.take import frame_nodes, lay, neighbour, recoil, take_at\n",
)
replace_once(
    p,
    """                entry["laid_back"], entry["dP_take"] = levels, [0] * AXES
                node.counts["laid_back"] += 1
            node.log.append(entry)""",
    """                entry["laid_back"], entry["dP_take"] = levels, [0] * AXES
                node.counts["laid_back"] += 1
            elif FLAG:
                currents = [int(row_current(plane_starts[rec0], port)[at]) for port in range(PORTS)]
                port = max(range(PORTS), key=lambda k: (abs(currents[k]), -k))
                far = neighbour(node, at, port)
                recoiled(node, entry, recoil(node, rec, at, far, node.last_dp), far)
            node.log.append(entry)


def recoiled(node: Node, entry: dict[str, Any], got: tuple[int, list[int], int, int], far: tuple[int, ...]) -> None:
    \"\"\"MK-S2: the recoil's numbers booked on the click's line (the levels p, the lattice momentum it books, the wall, the axis, the far end) and counted (the recoils moved, the flat ones).\"\"\"
    p, dp, wall, axis = got
    entry["recoil"], entry["dP_recoil"], entry["recoil_wall"] = p, dp, wall
    entry["recoil_axis"], entry["recoil_at"] = axis, list(far)
    node.counts["recoil"] = node.counts.get("recoil", 0) + (p != 0)
    node.counts["recoil_flat"] = node.counts.get("recoil_flat", 0) + (wall == 0)""".replace("FLAG", FLAG),
)

# close.py: the lay across the children's Link at a birth; the lay undone
p = os.path.join(DST, "close.py")
replace_once(p, "from __future__ import annotations\n\n", "from __future__ import annotations\n\nimport os\n")
replace_once(
    p,
    "from event_universe.bodies import bodies\n",
    "from event_universe.bodies import bodies, recoiled\n",
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
            far = minus if plus == at else plus
            recoiled(node, entry, recoil(node, s, at, far, take["dP_take"]), far)
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
        if "recoil" in entry:
            row_ = entry["line_pair"] if entry["event"] == "birth" else entry["line"]
            zeros = (0,) * (2 * node.records()[row_].shape - 2)
            lay(node, row_, tuple(entry["recoil_at"]), (0, entry["recoil"]) + zeros, -1)
        if entry["event"] == "birth":
            s, (a, b) = entry["line_pair"], entry["amplitude"]""",
)
if BUILT:
    for name, olds in (
        ("bodies.py", (("import os\n", ""), ("            elif True:\n", "            else:\n"))),
        ("close.py", (("import os\n", ""), ("        if True:\n            far = minus if plus == at else plus\n            recoiled(", "        far = minus if plus == at else plus\n        recoiled("))),
    ):
        for old, new in olds:
            replace_once(os.path.join(DST, name), old, new)
print("written:", DST, "flag" if not BUILT else "built (the flag removed)")
