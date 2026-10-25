"""cs8's flagged copy of the engine for this head (engine-5.0-test 10c04fb31, detached; SL-S2, the fourth form, CK-S1 even, the light no body, EM-S2's sense built), src untouched: src/event_universe copied whole to src_cs8/event_universe with cs7's flags rebuilt at this head's sites (the light no body and the even crossing are built, so CS4_LIGHT_NO_BODY and CK1_CROSS fall away) and this hand's flag stacked on them, each unset bit for bit David's path:
  CS4_TAKE_FARTHEST=1 (take.take_at, close.merger_take, close.unclick): the take moves the line of the taken record whose level now stands farthest from its before, the line kept PER TAKE in node.taken_lines and logged, unclick restoring that line (CS4-S2 as cs5 mended it; cs7's rebuild word for word);
  CS7_EQ=n (bodies.bodies): EQ-S1 with "nothing arrives" read on the NET current (the six currents of the taken row summed 0 at the interval's start): the take laid back on the taken line by the one lay act in the same close, the credit with laid_back and dP_take 0 (cs7's; b and c kept as cs7 wrote them);
  CS5_CROWD_OFF=1 (close.refuse): the crowd refusal lifted (cs5's control);
  CS6_SL_S3=1 (close.refuse): the lay refused at or above one quantum of the child's unit (SL-S3's letter); CS6_LIGHT_ON_LIGHT=1: the gap-0 child never refused as standing (light laid into light);
  CS8_MERGER_LAY=1 (close.refuse): the merger's children (a gapped row taken, the light born) are the take's inverse and are not read by the lay's refusals (the standing, the crowd): light laid back into light, as unclick lays back;
  CS8_REST=2 (close.meet): the merger at rest admitted only where each end has stood whole through its beat (the pair's click, the bodies' closing reading at the interval's start);
  CS8_REST=1 (close.meet): the merger at rest, this hand's candidate: where a record with a gap meets across a Link with its current 0 (nothing flows) and the two ends' charges of opposite sign, the meeting is not refused by the orientation: the + end is the end whose charge is positive (the birth's orientation read at -1: the birth put the + child at the end the current flowed into, the merger reads which end holds it by what stands there), the twist not consulted (the handedness is written in the pair), the one number read at the + end; the candidate logged as `rest_meet` with the two ends' charges; every other reading unchanged (F 0 with equal charges or no charge: the orientation's refusal as before).
Usage: python make_copy_cs8.py (writes src_cs8/ beside this file)."""
import os
import shutil

here = os.path.dirname(os.path.abspath(__file__))
src = os.path.join(here, "..", "..", "..", "src", "event_universe")
root = os.path.join(here, "src_cs8")
dst = os.path.join(root, "event_universe")
if os.path.exists(root):
    shutil.rmtree(root)
shutil.copytree(src, dst, ignore=shutil.ignore_patterns("__pycache__"))


def replace_once(path, old, new):
    s = open(path).read()
    assert s.count(old) == 1, ("the site is not unique", path, old[:70], s.count(old))
    open(path, "w").write(s.replace(old, new))


# bodies.py: the credit's taken line, EQ-S1 (cs7's sites at this head)
p = os.path.join(dst, "bodies.py")
replace_once(p, """    for rec, row in enumerate(node.records()):
        if row.gap == 0:
            continue
        standing_now = np.vectorize(""", """    rec0 = node.records().index(node.row(PLANE, gap=0))
    eq = os.environ.get("CS7_EQ", "")  # cs7: EQ-S1's reading b (eq2's letter), n (the net current), c (every click); absent David's path
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

# close.py: the merger at rest (cs8), the refusals' flags, the births' taken line, the merger's per-end line, the unclick per line (cs7's)
p = os.path.join(dst, "close.py")
replace_once(p, """            flow = int(currents[axis][at])
            if flow == 0:
                refused(node, at, "orientation", link=list(j), row=rec)
                continue
            into, outof = (j, at) if flow > 0 else (at, j)
            h = int(twists[axis][at])
            if h == 0:
                refused(node, at, "twist", link=list(j), row=rec)
                continue
            if charges is not None and int(charges[at]) * int(charges[j]) >= 0:
                w = [int(charges[at]), int(charges[j])]
                refused(node, at, "sense", link=list(j), row=rec, charges=w)
                continue
            plus, minus = (into, outof) if h > 0 else (outof, into)
""", """            flow = int(currents[axis][at])
            mode = os.environ.get("CS8_REST", "")
            rest = (
                mode in ("1", "2")
                and flow == 0
                and charges is not None
                and int(charges[at]) * int(charges[j]) < 0
            )  # cs8: the pair at rest, nothing flows and the two ends' charges opposite: the merger's premise met
            if rest and mode == "2":  # cs8's second reading: the pair's click, each end having stood whole through its beat (bodies' closing reading at the start)
                rest = all(
                    int(node.beats[rec][w_]) > 0 and int(node.standing[rec][w_]) + 1 >= int(node.beats[rec][w_])
                    for w_ in (at, j)
                )
            if rest:
                w = [int(charges[at]), int(charges[j])]
                plus, minus = (at, j) if w[0] > 0 else (j, at)  # the + end the end whose charge is positive (the birth read at -1)
                into = plus
                node.counts["rest_met"] = node.counts.get("rest_met", 0) + 1
                node.log.append({"event": "rest_meet", "i": node.interval, "node": list(at), "link": list(j), "row": rec, "charges": w})
            else:
                if flow == 0:
                    refused(node, at, "orientation", link=list(j), row=rec)
                    continue
                into, outof = (j, at) if flow > 0 else (at, j)
                h = int(twists[axis][at])
                if h == 0:
                    refused(node, at, "twist", link=list(j), row=rec)
                    continue
                if charges is not None and int(charges[at]) * int(charges[j]) >= 0:
                    w = [int(charges[at]), int(charges[j])]
                    refused(node, at, "sense", link=list(j), row=rec, charges=w)
                    continue
                plus, minus = (into, outof) if h > 0 else (outof, into)
""")
replace_once(p, """    kept = []
    for at, s, minus, plus, room, rec in born:
        if int(owns[s][minus]) > 0 or int(owns[s][plus]) > 0:""", """    kept = []
    inverse = []  # cs8: the merger's children, the take's inverse, not read by the lay's refusals
    for at, s, minus, plus, room, rec in born:
        if os.environ.get("CS8_MERGER_LAY", "") == "1" and node.records()[rec].gap and node.records()[s].gap == 0:
            inverse.append((at, s, minus, plus, room, rec))
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

replace_once(p, """    return [k for k in kept if k not in crowded]
""", """    return [k for k in kept if k not in crowded] + inverse
""")
replace_once(p, "from event_universe.take import fall_of, lay, momentum_of, neighbour, read_number, take_at\n",
             "from event_universe.take import fall_of, lay, line_index, momentum_of, neighbour, read_number, take_at\n")
replace_once(p, "import numpy as np\n", "import numpy as np\nimport os\n")

# take.py: the take's line by the fall's sign, kept per take (cs7's)
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
print("copy written:", dst, "flags: CS7_EQ (bodies.py); CS8_REST, CS5_CROWD_OFF, CS6_SL_S3, CS6_LIGHT_ON_LIGHT (close.py); CS4_TAKE_FARTHEST (take.py, close.py); unset = David's path")
