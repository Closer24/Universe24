"""cs6's flagged copy of the engine for this head (d547dcef3, SL-S2 built: the bodies' closing in bodies.py, unclick restoring per take), src untouched: src/event_universe copied whole to src_cs6/event_universe with cs5's chain of flags rebuilt at this head's sites and two of this hand's, each unset bit for bit David's path:
  CK1_CROSS=1 (bodies.bodies): the re line's zero crossing read in either direction (CK-S1);
  CS4_LIGHT_NO_BODY=1 (bodies.bodies): the plane at the gap 0 never credited as a body;
  CS4_NO_BIRTH=1 (close.refuse): a reader's control, every lay refused by name;
  CS5_BIRTHS_UNTIL=<i> (close.refuse): a reader's control, no birth after the interval i;
  CS5_CROWD_OFF=1 (close.refuse): the crowd refusal lifted (a control);
  CS4_TAKE_FARTHEST=1 (take.take_at, close.merger_take, close.unclick): the take moves the line of the taken record whose level now stands farthest from its before (the largest now^2 - before^2; the first where equal), the line kept PER TAKE in node.taken_lines and logged on every birth, merger take and credit, unclick restoring that line (CS4-S2 mended as cs5 found);
  CS6_SL_S3=1 (close.refuse): SL-S3's letter, the lay refused where the child's plane stands at or above ONE QUANTUM of the child's unit (the former "above 0" kept by name as the unflagged path);
  CS6_LIGHT_ON_LIGHT=1 (close.refuse): a child of the plane at the gap 0 is never refused for the standing light (light laid into light: SL-S3's stated intent, a gap-0 child adds to standing light), a gapped child refused as the letter refuses it.
The reader's mend (clicks.lengthening): the start value (0, None) replaced by (0, []), one shape with the compared tuples (cs5's finding (b)); a reader, no act.
Usage: python make_copy_cs6.py (writes src_cs6/ beside this file)."""
import os
import shutil

here = os.path.dirname(os.path.abspath(__file__))
src = os.path.join(here, "..", "..", "..", "src", "event_universe")
root = os.path.join(here, "src_cs6")
dst = os.path.join(root, "event_universe")
if os.path.exists(root):
    shutil.rmtree(root)
shutil.copytree(src, dst, ignore=shutil.ignore_patterns("__pycache__"))


def replace_once(path, old, new):
    s = open(path).read()
    assert s.count(old) == 1, ("the site is not unique", path, old[:70], s.count(old))
    open(path, "w").write(s.replace(old, new))


# bodies.py: the crossing, the light no body, the credit's taken line
p = os.path.join(dst, "bodies.py")
replace_once(p, """            upward = np.vectorize(lambda b, n: 1 if (int(b) < 0 <= int(n)) else 0, otypes=[object])(
                re.before, re.now
            )
""", """            if os.environ.get("CK1_CROSS", "") == "1":  # ck1's flag: the zero crossing in either direction
                upward = np.vectorize(
                    lambda b, n: 1 if (int(b) < 0 <= int(n) or int(n) < 0 <= int(b)) else 0, otypes=[object]
                )(re.before, re.now)
            else:
                upward = np.vectorize(lambda b, n: 1 if (int(b) < 0 <= int(n)) else 0, otypes=[object])(
                    re.before, re.now
                )
""")
replace_once(p, """    for rec, row in enumerate(node.records()):
        standing_now = np.vectorize(""", """    for rec, row in enumerate(node.records()):
        if os.environ.get("CS4_LIGHT_NO_BODY", "") == "1" and row.gap == 0:  # cs4's flag: the light at the gap 0 is no body
            continue
        standing_now = np.vectorize(""")
replace_once(p, """        "taker": [taken_was, taken_before, levels],
        "dP_take": node.last_dp,""", """        "taker": [taken_was, taken_before, levels],
        "taken_line": getattr(node, "taken_lines", {}).get((at, node.records().index(node.row(PLANE, gap=0))), 0),
        "dP_take": node.last_dp,""")
replace_once(p, "import numpy as np\n", "import numpy as np\nimport os\n")

# close.py: the refusals' flags, the births' taken line, the merger's per-end line, the unclick per line
p = os.path.join(dst, "close.py")
replace_once(p, """    kept = []
    for at, s, minus, plus, room, rec in born:
        if int(owns[s][minus]) > 0 or int(owns[s][plus]) > 0:""", """    kept = []
    for at, s, minus, plus, room, rec in born:
        if os.environ.get("CS4_NO_BIRTH", "") == "1":  # cs4's control: no child on the board
            refused(node, at, "lay", control=1, row=rec)
            continue
        until = os.environ.get("CS5_BIRTHS_UNTIL", "")
        if until != "" and node.interval > int(until):  # cs5's control: no birth after the named interval
            refused(node, at, "lay", control=2, row=rec)
            continue
        above = 0  # the letter: refused where the child's plane stands above 0
        if os.environ.get("CS6_SL_S3", "") == "1":  # SL-S3's letter: refused at or above one quantum of the child's unit
            above = node.units[s] - 1
        if os.environ.get("CS6_LIGHT_ON_LIGHT", "") == "1" and node.records()[s].gap == 0:  # light laid into light
            above = None
        if above is not None and (int(owns[s][minus]) > above or int(owns[s][plus]) > above):""")
replace_once(p, """    crowded = [k for k in kept if landing[(k[1], k[2])] > 1 or landing[(k[1], k[3])] > 1]
""", """    crowded = [k for k in kept if landing[(k[1], k[2])] > 1 or landing[(k[1], k[3])] > 1]
    if os.environ.get("CS5_CROWD_OFF", "") == "1":  # cs5's control: the crowd refusal lifted
        crowded = []
""")
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

# gates.py: the reader's mend (cs5's finding (b)), one shape for the compared tuples
p = os.path.join(dst, "clicks.py")
replace_once(p, "    longest: tuple[int, Any] = (0, None)\n", "    longest: tuple[int, Any] = (0, [])  # cs6: one shape with the compared tuples (the reader's mend)\n")
print("copy written:", dst, "flags: CK1_CROSS, CS4_LIGHT_NO_BODY (bodies.py); CS4_NO_BIRTH, CS5_BIRTHS_UNTIL, CS5_CROWD_OFF, CS6_SL_S3, CS6_LIGHT_ON_LIGHT (close.py); CS4_TAKE_FARTHEST (take.py, close.py); the gates reader's mend; unset = David's path")
