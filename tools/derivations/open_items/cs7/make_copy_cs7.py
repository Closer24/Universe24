"""cs7's flagged copy of the engine for this head (engine-5.0-test 57220fc0a, detached; SL-S2 built, EM-S2's sense, no CK-S1), src untouched: src/event_universe copied whole to src_cs7/event_universe with cs6's chain of flags rebuilt word for word (cs5's and cs4's, each unset bit for bit David's path) and eq2's EQ-S1 stacked on them at this head's sites, each unset bit for bit David's path:
  CK1_CROSS=1 (bodies.bodies): the re line's zero crossing read in either direction (CK-S1; a control here);
  CS4_LIGHT_NO_BODY=1 (bodies.bodies): the plane at the gap 0 never credited as a body (cs4's word);
  CS4_NO_BIRTH=1 (close.refuse): a reader's control, every lay refused by name;
  CS5_BIRTHS_UNTIL=<i> (close.refuse): a reader's control, no birth after the interval i;
  CS5_CROWD_OFF=1 (close.refuse): the crowd refusal lifted (a control);
  CS4_TAKE_FARTHEST=1 (take.take_at, close.merger_take, close.unclick): the take moves the line of the taken record whose level now stands farthest from its before (the largest now^2 - before^2; the first where equal), the line kept PER TAKE in node.taken_lines and logged on every birth, merger take and credit, unclick restoring that line (CS4-S2 as cs5 mended it);
  CS6_SL_S3=1, CS6_LIGHT_ON_LIGHT=1 (close.refuse): cs6's two readings of SL-S3 (controls here);
  CS7_EQ=b (bodies.bodies): EQ-S1 as eq2 wrote it: where nothing arrives at the Node (the taken row's current 0 across every one of its six Links at the interval's start, links.row_current as close.meet reads it) the take is laid back on the TAKEN LINE (the line the take moved: the first line on David's path, the far line under CS4_TAKE_FARTHEST) by the one lay act in the same close, the credit written with laid_back = levels and its momentum booked 0;
  CS7_EQ=n (bodies.bodies): the same with "nothing arrives" read on the NET current, the six currents summed 0 (the lattice divergence: what flows in flows out; a candidate reading, this hand's);
  CS7_EQ=c (bodies.bodies): the take laid back at every click (eq2's reading (c); a control and a candidate);
  under any CS7_EQ the six currents at the Node are logged on every credit under `arrivals` (a reader).
The reader's mend (clicks.lengthening): the start value (0, None) replaced by (0, []) (cs5's finding (b), cs6's one line).
Usage: python make_copy_cs7.py (writes src_cs7/ beside this file)."""
import os
import shutil

here = os.path.dirname(os.path.abspath(__file__))
src = os.path.join(here, "..", "..", "..", "src", "event_universe")
root = os.path.join(here, "src_cs7")
dst = os.path.join(root, "event_universe")
if os.path.exists(root):
    shutil.rmtree(root)
shutil.copytree(src, dst, ignore=shutil.ignore_patterns("__pycache__"))


def replace_once(path, old, new):
    s = open(path).read()
    assert s.count(old) == 1, ("the site is not unique", path, old[:70], s.count(old))
    open(path, "w").write(s.replace(old, new))


# bodies.py: the crossing, the light no body, the credit's taken line, EQ-S1
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
        standing_now = np.vectorize(""", """    rec0 = node.records().index(node.row(PLANE, gap=0))
    eq = os.environ.get("CS7_EQ", "")  # cs7: EQ-S1's reading b (eq2's letter), n (the net current), c (every click); absent David's path
    arriving = (
        [row_current(plane_starts[rec0], port) for port in range(PORTS)] if eq else []
    )  # the taken row's current across the Node's six Links at the interval's start, as close.meet reads it
    for rec, row in enumerate(node.records()):
        if os.environ.get("CS4_LIGHT_NO_BODY", "") == "1" and row.gap == 0:  # cs4's flag: the light at the gap 0 is no body
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
            )  # cs7: nothing arrives at the Node by the reading named
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
                k = getattr(node, "taken_lines", {}).get((at, rec0), 0)
                line = node.records()[rec0].lines[k]
                lay(
                    node,
                    rec0,
                    at,
                    tuple((now - int(line.now[at])) if j == 2 * k else 0 for j in range(2 * node.records()[rec0].shape)),
                )
                entry["laid_back"] = levels
                entry["dP_take"] = [0, 0, 0]
                node.counts["laid_back"] = node.counts.get("laid_back", 0) + 1
            node.log.append(entry)
""")
replace_once(p, """        "taker": [taken_was, taken_before, levels],
        "dP_take": node.last_dp,""", """        "taker": [taken_was, taken_before, levels],
        "taken_line": getattr(node, "taken_lines", {}).get((at, node.records().index(node.row(PLANE, gap=0))), 0),
        "dP_take": node.last_dp,""")
replace_once(p, "import numpy as np\n", "import numpy as np\nimport os\n")
replace_once(p, "from event_universe.core.ports import PORT_SIDES\n", "from event_universe.core.ports import PORT_SIDES, PORTS\nfrom event_universe.links import row_current\n")
replace_once(p, "from event_universe.take import frame_nodes, take_at\n", "from event_universe.take import frame_nodes, lay, take_at\n")

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

# clicks.py: the reader's mend (cs5's finding (b)), one shape for the compared tuples
p = os.path.join(dst, "clicks.py")
replace_once(p, "    longest: tuple[int, Any] = (0, None)\n", "    longest: tuple[int, Any] = (0, [])  # cs6: one shape with the compared tuples (the reader's mend)\n")
print("copy written:", dst, "flags: CK1_CROSS, CS4_LIGHT_NO_BODY, CS7_EQ (bodies.py); CS4_NO_BIRTH, CS5_BIRTHS_UNTIL, CS5_CROWD_OFF, CS6_SL_S3, CS6_LIGHT_ON_LIGHT (close.py); CS4_TAKE_FARTHEST (take.py, close.py); the gates reader's mend; unset = David's path")
