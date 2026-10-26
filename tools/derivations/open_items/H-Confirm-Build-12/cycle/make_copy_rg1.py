"""rg1's flagged copy of the engine for this head (engine-5.0-test bb9deff70, detached; CK-S1 even, the light no body, EQ-S1 in cs7's net letter, SL-S2, the fourth form built), src untouched: src/event_universe copied whole to src_rg1/event_universe with ONE flag rebuilt at this head's sites (mg1's text, word for word), unset bit for bit David's path:
  CS4_TAKE_FARTHEST=1 (take.take_at, close.merger_take, close.unclick, bodies.bodies): the take moves the line of the taken record whose level now stands farthest from its before (the largest now^2 - before^2, the first where equal: CS4-S2, the take by the fall's sign), the line kept PER TAKE in node.taken_lines and logged on every birth, merger take and credit (`taken_line`), unclick and EQ-S1's laying back restoring that line.
Of cs7's chain (make_copy_cs7.py) the replacements CK1_CROSS, CS4_LIGHT_NO_BODY, CS7_EQ=n and the reader's mend of clicks.lengthening are NO-OPS at this head (built: bodies.py's crossing even, `if row.gap == 0: continue`, the net current summed and laid back on the taken line; clicks.py's (0, [])); CS4_NO_BIRTH, CS5_BIRTHS_UNTIL, CS5_CROWD_OFF, CS6_SL_S3, CS6_LIGHT_ON_LIGHT, CS7_EQ=b / c were controls not set on the ga2 record; CS4_TAKE_FARTHEST is the one replacement that still changes the act.
Usage: python make_copy_rg1.py (writes src_rg1/ beside this file)."""
import os
import shutil

here = os.path.dirname(os.path.abspath(__file__))
src = os.path.join(here, "..", "..", "..", "src", "event_universe")
root = os.path.join(here, "src_rg1")
dst = os.path.join(root, "event_universe")
if os.path.exists(root):
    shutil.rmtree(root)
shutil.copytree(src, dst, ignore=shutil.ignore_patterns("__pycache__"))


def replace_once(path, old, new):
    s = open(path).read()
    assert s.count(old) == 1, ("the site is not unique", path, old[:70], s.count(old))
    open(path, "w").write(s.replace(old, new))


# take.py: the take's line by the fall's sign, kept per take
p = os.path.join(dst, "take.py")
replace_once(p, """def take_at(
    node: Node, at: tuple[int, ...], walls: int, rule: rule3.Rule, cause: int, rec: int | None = None
) -> tuple[int, int, int, int] | None:""", """def line_index(node: Node, row: Any, at: tuple[int, ...]) -> int:
    \"\"\"The line the take moves: David's path the first line; under CS4_TAKE_FARTHEST=1 the line whose level now stands farthest from its before (the largest now^2 - before^2, the first where equal: CS4-S2).\"\"\"
    if os.environ.get("CS4_TAKE_FARTHEST", "") != "1":
        return 0
    gaps = [int(line.now[at]) ** 2 - int(line.before[at]) ** 2 for line in row.lines]
    return gaps.index(max(gaps))


def take_at(
    node: Node, at: tuple[int, ...], walls: int, rule: rule3.Rule, cause: int, rec: int | None = None
) -> tuple[int, int, int, int] | None:""")
replace_once(p, """    row = node.records()[taken]
    z = row.lines[0]
    levels, fall = fall_of(node, at, walls, rule, z)
""", """    row = node.records()[taken]
    k = line_index(node, row, at)
    if not hasattr(node, "taken_lines"):
        node.taken_lines = {}
    node.taken_lines[(at, taken)] = k
    z = row.lines[k]
    levels, fall = fall_of(node, at, walls, rule, z)
""")
replace_once(p, """    lay(node, taken, at, (toward * levels,) + (0,) * (2 * row.shape - 1))
""", """    lay(node, taken, at, tuple(toward * levels if j == 2 * k else 0 for j in range(2 * row.shape)))
""")
replace_once(p, "import numpy as np\n", "import numpy as np\nimport os\n")

# bodies.py: EQ-S1's laying back on the taken line, the credit's taken line
p = os.path.join(dst, "bodies.py")
replace_once(p, """            if int(net[at]) == 0:
                line = node.records()[rec0].lines[0]
                lay(node, rec0, at, (now - int(line.now[at]),) + (0,) * (2 * PLANE - 1))
""", """            if int(net[at]) == 0:
                k = getattr(node, "taken_lines", {}).get((at, rec0), 0)
                line = node.records()[rec0].lines[k]
                lay(node, rec0, at, tuple((now - int(line.now[at])) if j == 2 * k else 0 for j in range(2 * PLANE)))
""")
replace_once(p, """        "taker": [taken_was, taken_before, levels],
        "dP_take": node.last_dp,""", """        "taker": [taken_was, taken_before, levels],
        "taken_line": getattr(node, "taken_lines", {}).get((at, node.records().index(node.row(PLANE, gap=0))), 0),
        "dP_take": node.last_dp,""")

# close.py: the birth's taken line, the merger's per-end line, unclick per taken line
p = os.path.join(dst, "close.py")
replace_once(p, """                "taken_row": rec,
                "proper": int(node.proper[at]),""", """                "taken_row": rec,
                "taken_line": getattr(node, "taken_lines", {}).get((at, rec), 0),
                "proper": int(node.proper[at]),""")
replace_once(p, """    line = node.records()[rec].lines[0]
    for where, wall in zip((minus, plus), walls, strict=True):
        levels, fall = fall_of(node, where, wall, rule, line)
""", """    row = node.records()[rec]
    for where, wall in zip((minus, plus), walls, strict=True):
        line = row.lines[line_index(node, row, where)]
        levels, fall = fall_of(node, where, wall, rule, line)
""")
replace_once(p, """        takes.append({"node": list(where), **take_line(fall, wall, levels, now, before, node.last_dp)})
""", """        takes.append(
            {
                "node": list(where),
                "taken_line": getattr(node, "taken_lines", {}).get((where, rec), 0),
                **take_line(fall, wall, levels, now, before, node.last_dp),
            }
        )
""")
replace_once(p, """            row = entry.get("taken_row", rec0)
            line = node.records()[row].lines[0]
            for take in entry.get("takes", [entry]):
                where = tuple(take["node"])
                lay(
                    node,
                    row,
                    where,
                    (take["taken_now_was"] - int(line.now[where]),)
                    + (0,) * (2 * node.records()[row].shape - 1),
                )""", """            row = entry.get("taken_row", rec0)
            for take in entry.get("takes", [entry]):
                where = tuple(take["node"])
                k = int(take.get("taken_line", 0))
                line = node.records()[row].lines[k]
                lay(
                    node,
                    row,
                    where,
                    tuple(
                        (take["taken_now_was"] - int(line.now[where])) if j == 2 * k else 0
                        for j in range(2 * node.records()[row].shape)
                    ),
                )""")
replace_once(p, "from event_universe.take import fall_of, lay, momentum_of, neighbour, read_number, take_at\n",
             "from event_universe.take import fall_of, lay, line_index, momentum_of, neighbour, read_number, take_at\n")
replace_once(p, "import numpy as np\n", "import numpy as np\nimport os\n")
print("copy written:", dst, "flag: CS4_TAKE_FARTHEST (take.py, bodies.py, close.py); unset = David's path")
