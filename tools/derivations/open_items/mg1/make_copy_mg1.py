"""mg1's flagged copy of the engine for this head (engine-5.0-test bb9deff70, detached; EQ-S1 in cs7's letter built, the light no body, CK-S1 even, SL-S2, the fourth form), src untouched: src/event_universe copied whole to src_mg1/event_universe with cs7's and cs8's flags rebuilt at this head's sites and this hand's stacked on them, each unset bit for bit David's path:
  CS4_TAKE_FARTHEST=1 (take.take_at, close.merger_take, close.unclick, bodies.bodies): the take moves the line of the taken record whose level now stands farthest from its before, the line kept PER TAKE in node.taken_lines and logged, unclick and EQ-S1's laying back restoring that line (CS4-S2 as cs5 mended it);
  CS5_CROWD_OFF=1 (close.refuse): the crowd refusal lifted (cs5's control);
  CS8_REST=1 (close.meet): the merger at rest: where a record with a gap meets across a Link with its current 0 and the two ends' charges of opposite sign, the + end is the end whose charge is positive, the twist not consulted, the one number read at the + end (cs8's candidate, word for word);
  CS8_MERGER_LAY=1 (close.refuse): the merger's children (a gapped row taken, the light born) are the take's inverse and are not read by the lay's refusals (cs8's);
  MG1_WALL=own (close.walls_of): CS8-S2: a child's wall is its own quantum, the share its levels alone hold on an empty board at the Node under the row's rule at the board's content (the same two integers A, B for every row), not the board's increment where its plane already stands;
  MG1_LOG_WALLS=1 (close.births): every kept birth's walls logged with both readings (the board's increment and the own quantum) as `walls` lines, a reader's hook, the state untouched;
  MG1_TAKE=two (close.merger_take): CS8-S1 as cs8 wrote it: the exact take continued on the record's second line where the first line's full move falls short, one take per line under `takes`, unclick restoring each by its taken_line;
  MG1_TAKE=whole (close.merger_take): the merger's take as the birth's lay read at -1 on what stands: the taken record's four levels at the end taken whole by the one lay act at -1, the fall the record's share the board loses (read before either end is written), refused by name `stop` where the fall is below the child's wall; the take logged with `taken_levels`, unclick laying them back.
Usage: python make_copy_mg1.py (writes src_mg1/ beside this file)."""
import os
import shutil

here = os.path.dirname(os.path.abspath(__file__))
src = os.path.join(here, "..", "..", "..", "src", "event_universe")
root = os.path.join(here, "src_mg1")
dst = os.path.join(root, "event_universe")
if os.path.exists(root):
    shutil.rmtree(root)
shutil.copytree(src, dst, ignore=shutil.ignore_patterns("__pycache__"))


def replace_once(path, old, new):
    s = open(path).read()
    assert s.count(old) == 1, ("the site is not unique", path, old[:70], s.count(old))
    open(path, "w").write(s.replace(old, new))


# take.py: the take's line by the fall's sign, kept per take (cs7's rebuild of CS4-S2)
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

# bodies.py: EQ-S1's laying back on the taken line, the credit's taken line (cs7's sites at this head)
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

# close.py
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
            rest = (
                os.environ.get("CS8_REST", "") == "1"
                and flow == 0
                and charges is not None
                and int(charges[at]) * int(charges[j]) < 0
            )  # cs8: the pair at rest, nothing flows and the two ends' charges opposite: the merger's premise met
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
        if int(owns[s][minus]) > 0 or int(owns[s][plus]) > 0:""")
replace_once(p, """    crowded = [k for k in kept if landing[(k[1], k[2])] > 1 or landing[(k[1], k[3])] > 1]
""", """    crowded = [k for k in kept if landing[(k[1], k[2])] > 1 or landing[(k[1], k[3])] > 1]
    if os.environ.get("CS5_CROWD_OFF", "") == "1":  # cs5's control: the crowd refusal lifted
        crowded = []
""")
replace_once(p, """    return [k for k in kept if k not in crowded]
""", """    return [k for k in kept if k not in crowded] + inverse
""")
# births: the walls logged with both readings (a reader's hook)
replace_once(p, """    walls = {k: walls_of(node, k[1], k[2], k[3], c, factors) for k in kept}
""", """    walls = {k: walls_of(node, k[1], k[2], k[3], c, factors) for k in kept}
    if os.environ.get("MG1_LOG_WALLS", "") == "1":  # mg1: every kept birth's walls under both readings, the state untouched
        ow = owns_now(node, c, factors)
        for k in kept:
            inc = walls_increment(node, k[1], k[2], k[3], c, factors)
            own = walls_own(node, k[1], k[2], k[3], c, factors)
            node.log.append({"event": "walls", "i": node.interval, "node": list(k[0]), "line_pair": k[1], "taken_row": k[5], "minus": list(k[2]), "plus": list(k[3]), "increment": list(inc), "own": list(own), "standing": [int(ow[k[1]][k[2]]), int(ow[k[1]][k[3]])]})
""")
# the birth's taken line in the log
replace_once(p, """                "taken_row": rec,
                "proper": int(node.proper[at]),""", """                "taken_row": rec,
                "taken_line": getattr(node, "taken_lines", {}).get((at, rec), 0),
                "proper": int(node.proper[at]),""")
# merger_take: per-end line (CS4), the two-line take (MG1_TAKE=two), the whole take (MG1_TAKE=whole)
replace_once(p, """    line = node.records()[rec].lines[0]
    for where, wall in zip((minus, plus), walls, strict=True):
        levels, fall = fall_of(node, where, wall, rule, line)
        if levels is None:
            node.counts["refused_stop"] += 1
            node.log.append(
                {
                    "event": "refused",
                    "i": node.interval,
                    "node": list(where),
                    "cause": "stop",
                    "fall": fall,
                    "walls": wall,
                    "row": rec,
                }
            )
            return None
    takes: list[dict[str, Any]] = []
    for where, wall in zip((minus, plus), walls, strict=True):
        got = take_at(node, where, wall, rule, 1, rec)
        assert got is not None
        levels, fall, now, before = got
        node.closes[where] -= 1
        takes.append({"node": list(where), **take_line(fall, wall, levels, now, before, node.last_dp)})
""", """    mode = os.environ.get("MG1_TAKE", "")
    if mode == "whole":
        return merger_take_whole(node, minus, plus, walls, rule, rec)
    row = node.records()[rec]
    plan: list[list[tuple[int, int]]] = []  # per end: the lines taken with the walls each pays
    for where, wall in zip((minus, plus), walls, strict=True):
        k = line_index(node, row, where)
        levels, fall = fall_of(node, where, wall, rule, row.lines[k])
        if levels is not None:
            plan.append([(k, wall)])
            continue
        if mode == "two" and row.shape > 1:  # CS8-S1: the exact take continued on the second line where the first falls short
            other = 1 - k
            levels2, fall2 = fall_of(node, where, wall - fall, rule, row.lines[other])
            if levels2 is not None:
                plan.append([(k, fall), (other, wall - fall)])
                continue
            fall = fall + fall2
        node.counts["refused_stop"] += 1
        node.log.append(
            {
                "event": "refused",
                "i": node.interval,
                "node": list(where),
                "cause": "stop",
                "fall": fall,
                "walls": wall,
                "row": rec,
            }
        )
        return None
    takes: list[dict[str, Any]] = []
    for where, wall, lines_plan in zip((minus, plus), walls, plan, strict=True):
        for k, part in lines_plan:
            got = take_on_line(node, where, part, rule, rec, k)
            assert got is not None
            levels, fall, now, before = got
            node.closes[where] -= 1
            takes.append({"node": list(where), "taken_line": k, **take_line(fall, part, levels, now, before, node.last_dp)})
""")
replace_once(p, """def walls_of(
    node: Node, s: int, minus: tuple[int, ...], plus: tuple[int, ...], c: Any, factors: tuple[Any, ...]
) -> tuple[int, int]:
    \"\"\"Each child's wall (MS-S1): the share its lay adds to its plane on the board in the carrier's unit, read by laying the - child, then the + child, reading after each and taking both back; the birth's walls their sum.\"\"\"
    row = node.records()[s]
""", """def take_on_line(
    node: Node, at: tuple[int, ...], walls: int, rule: rule3.Rule, rec: int, k: int
) -> tuple[int, int, int, int] | None:
    \"\"\"mg1: one exact take at a Node on the named line k of the taken record (take.take_at's act with the line given), the line kept per take.\"\"\"
    row = node.records()[rec]
    z = row.lines[k]
    levels, fall = fall_of(node, at, walls, rule, z)
    if levels is None:
        return None
    if not hasattr(node, "taken_lines"):
        node.taken_lines = {}
    node.taken_lines[(at, rec)] = k
    now, before = int(z.now[at]), int(z.before[at])
    toward = 1 if before > now else -1
    lay(node, rec, at, tuple(toward * levels if j == 2 * k else 0 for j in range(2 * row.shape)))
    node.closes[at] += 1
    assert row.pair is not None
    node.last_dp = momentum_of(node, z.now, z.before, at, d_now=toward * levels, num=row.pair[0])
    return levels, fall, now, before


def merger_take_whole(
    node: Node,
    minus: tuple[int, ...],
    plus: tuple[int, ...],
    walls: tuple[int, int],
    rule: rule3.Rule,
    rec: int,
) -> dict[str, Any] | None:
    \"\"\"mg1: the merger's take as the birth's lay read at -1 on what stands: at each end the taken record's levels at the Node taken whole by the one lay act at -1, the fall the record's share the board loses (both ends read before either is written), refused by name `stop` where an end's fall is below the child's wall; one take per end under `takes`, each carrying `taken_levels` for unclick.\"\"\"
    row = node.records()[rec]
    assert row.pair is not None

    def total() -> int:
        return int(sum(int(x) for x in node.share(row.lines, rule).reshape(-1)))

    stood = []
    falls = []
    base = total()
    for where in (minus, plus):
        levels = [int(v) for line in row.lines for v in (line.now[where], line.before[where])]
        lay(node, rec, where, tuple(levels), -1)
        after = total()
        lay(node, rec, where, tuple(levels), 1)
        stood.append(levels)
        falls.append(base - after)
    for where, wall, fall in zip((minus, plus), walls, falls, strict=True):
        if fall < wall:
            node.counts["refused_stop"] += 1
            node.log.append(
                {
                    "event": "refused",
                    "i": node.interval,
                    "node": list(where),
                    "cause": "stop",
                    "fall": fall,
                    "walls": wall,
                    "row": rec,
                    "whole": 1,
                }
            )
            return None
    takes: list[dict[str, Any]] = []
    for where, wall, fall, levels in zip((minus, plus), walls, falls, stood, strict=True):
        dp = [0, 0, 0]
        for k, line in enumerate(row.lines):
            part = momentum_of(node, line.now, line.before, where, d_now=-levels[2 * k], d_before=-levels[2 * k + 1], num=row.pair[0])
            dp = [a + b for a, b in zip(dp, part, strict=True)]
        lay(node, rec, where, tuple(levels), -1)
        node.last_dp = dp
        takes.append(
            {
                "node": list(where),
                "taken_levels": levels,
                **take_line(fall, wall, sum(abs(v) for v in levels), levels[0], levels[1], dp),
            }
        )
    return {
        "taken": takes[0]["taken"] + takes[1]["taken"],
        "booked": takes[0]["booked"] + takes[1]["booked"],
        "levels": takes[0]["levels"] + takes[1]["levels"],
        "taken_now_was": [t["taken_now_was"] for t in takes],
        "taker": [t["taker"] for t in takes],
        "dP_take": [a + b for a, b in zip(takes[0]["dP_take"], takes[1]["dP_take"], strict=True)],
        "takes": takes,
    }


def owns_now(node: Node, c: Any, factors: tuple[Any, ...]) -> list[Any]:
    \"\"\"mg1 (a reader's hook): every record's share on the live board.\"\"\"
    found = []
    for r in node.records():
        assert r.pair is not None
        found.append(node.share(r.lines, node.rule(r.pair, c, factors)))
    return found


def walls_own(
    node: Node, s: int, minus: tuple[int, ...], plus: tuple[int, ...], c: Any, factors: tuple[Any, ...]
) -> tuple[int, int]:
    \"\"\"mg1, CS8-S2: each child's wall as its own quantum: the share the child's levels alone hold at the Node on empty lines of the row's shape under the row's rule at the board's content (the same two integers A, B for every row).\"\"\"
    row = node.records()[s]
    assert row.pair is not None
    rule = node.rule(row.pair, c, factors)
    found = []
    for where, sense in ((minus, -1), (plus, 1)):
        lines = [Line(zeros(node.shape), zeros(node.shape), None, line.wall) for line in row.lines]
        lines[0].now[where] = node.A
        lines[1].before[where] = sense * node.B
        found.append(int(sum(int(x) for x in node.share(lines, rule).reshape(-1))))
    return found[0], found[1]


def walls_of(
    node: Node, s: int, minus: tuple[int, ...], plus: tuple[int, ...], c: Any, factors: tuple[Any, ...]
) -> tuple[int, int]:
    \"\"\"Each child's wall: David's path the board's increment (`walls_increment`); under MG1_WALL=own the child's own quantum (`walls_own`, CS8-S2).\"\"\"
    if os.environ.get("MG1_WALL", "") == "own":
        return walls_own(node, s, minus, plus, c, factors)
    return walls_increment(node, s, minus, plus, c, factors)


def walls_increment(
    node: Node, s: int, minus: tuple[int, ...], plus: tuple[int, ...], c: Any, factors: tuple[Any, ...]
) -> tuple[int, int]:
    \"\"\"Each child's wall (MS-S1): the share its lay adds to its plane on the board in the carrier's unit, read by laying the - child, then the + child, reading after each and taking both back; the birth's walls their sum.\"\"\"
    row = node.records()[s]
""")
# unclick: per taken_line, and the whole take's levels laid back
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
                if "taken_levels" in take:  # mg1: the whole take undone, the levels laid back
                    lay(node, row, where, tuple(int(v) for v in take["taken_levels"]), 1)
                    continue
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
replace_once(p, "from event_universe.rows import PLANE, Line\n", "from event_universe.rows import PLANE, Line, zeros\n")
replace_once(p, "import numpy as np\n", "import numpy as np\nimport os\n")
# the light laid as the exact take at -1 (MG1_LAY=exact): on the taken row's line at the end, now moved away from before by the least count of levels at which the share rises by the child's wall; the child's lay where the line has no direction
replace_once(p, """    touched = {at}
    for s, minus, plus, room in kids:
        dp_lay, w_children, stood = child_laid(node, s, minus, plus)
""", """    touched = {at}
    for s, minus, plus, room in kids:
        exact_lay = None
        if os.environ.get("MG1_LAY", "") == "exact" and node.records()[rec].gap and "takes" in take:
            dp_lay, w_children, stood, exact_lay = child_laid_exact(node, s, minus, plus, [t["booked"] for t in take["takes"]])
        else:
            dp_lay, w_children, stood = child_laid(node, s, minus, plus)
""")
replace_once(p, """                "dP_lay": dp_lay,
                **({"takes": take["takes"]} if "takes" in take else {}),
""", """                "dP_lay": dp_lay,
                **({"takes": take["takes"]} if "takes" in take else {}),
                **({"exact_lay": exact_lay} if exact_lay is not None else {}),
""")
replace_once(p, """def child_laid(
    node: Node, s: int, minus: tuple[int, ...], plus: tuple[int, ...]
) -> tuple[list[int], list[int], list[list[int]]]:""", """def rise_of(
    node: Node, at: tuple[int, ...], walls: int, r: rule3.Rule, line: Line, away: int
) -> tuple[int | None, int]:
    \"\"\"mg1: the exact take at -1 (fall_of's form mirrored): the least count of levels s by which the line's now, moved away from its before in the direction `away`, raises the Node's share by the walls, found by doubling and bisection; (None, the rise at the bound) where no count within 2^80 levels does.\"\"\"
    now, before = int(line.now[at]), int(line.before[at])
    own, w, reached = int(np.asarray(r.self_coefficient)[at]), int(r.wall), 0
    for port, reach in enumerate(r.reaches):
        reached += int(np.asarray(reach)[at]) * int(line.before[neighbour(node, at, port)])
    pull = own * before + reached
    x, weight = int(node.start_x[at]), 2 * node.gamma**3 * node.G * node.G

    def rise(s: int) -> int:
        d = away * s
        return int(quotient(x * (w * ((now + d) ** 2 - now * now) + d * pull), weight))

    high = 1
    while rise(high) < walls:
        high = high + high
        if high > 1 << 80:
            return None, rise(high)
    low = 0
    while high - low > 1:
        middle = int(quotient(low + high, 2))
        if rise(middle) < walls:
            low = middle
        else:
            high = middle
    return high, rise(high)


def child_laid_exact(
    node: Node, s: int, minus: tuple[int, ...], plus: tuple[int, ...], walls: list[int]
) -> tuple[list[int], list[int], list[list[int]], list[Any]]:
    \"\"\"mg1: the merger's light laid at each end as the exact take at -1 on the light's line the take would move (line_index), now moved away from before by the least count of levels at which the share rises by the child's wall (rise_of); the child's lay (child_at) where the line has no direction or no count pays. Returns the lays' momentum, each end's charge, the four levels before and the lays [line, d, rise] or None per end.\"\"\"
    row = node.records()[s]
    assert row.pair is not None
    re, im = row.lines
    stood = [[int(a[w_]) for a in (re.now, re.before, im.now, im.before)] for w_ in (minus, plus)]
    rule = node.rule(row.pair, node.start_content, node.link_factors(None, readings.frozen_of(node, node.start_content)))
    dp_lay = [0, 0, 0]
    laid: list[Any] = []
    for (where, sense), wall in zip(((minus, -1), (plus, 1)), walls, strict=True):
        k = line_index(node, row, where)
        line = row.lines[k]
        now, before = int(line.now[where]), int(line.before[where])
        got = (None, 0) if now == before else rise_of(node, where, wall, rule, line, 1 if now > before else -1)
        if got[0] is None:
            for a, d in enumerate(child_at(node, s, where, sense)):
                dp_lay[a] += d
            laid.append(None)
            continue
        d = (1 if now > before else -1) * got[0]
        for a, v in enumerate(momentum_of(node, line.now, line.before, where, d_now=d, num=row.pair[0])):
            dp_lay[a] += v
        lay(node, s, where, tuple(d if j == 2 * k else 0 for j in range(2 * row.shape)))
        laid.append([k, d, got[1]])
    senses = [int(cross(re.now[w_], im.now[w_], re.before[w_], im.before[w_])) for w_ in (minus, plus)]
    return dp_lay, senses, stood, laid


def child_laid(
    node: Node, s: int, minus: tuple[int, ...], plus: tuple[int, ...]
) -> tuple[list[int], list[int], list[list[int]]]:""")
replace_once(p, """        if entry["event"] == "birth":
            s, (a, b) = entry["line_pair"], entry["amplitude"]
            lay(node, s, tuple(entry["minus"]), (a, 0, 0, -b), -1)
            lay(node, s, tuple(entry["plus"]), (a, 0, 0, b), -1)
""", """        if entry["event"] == "birth":
            s, (a, b) = entry["line_pair"], entry["amplitude"]
            exact = entry.get("exact_lay", [None, None])
            for end, sense, one in zip(("minus", "plus"), (-1, 1), exact, strict=True):
                if one is None:
                    lay(node, s, tuple(entry[end]), (a, 0, 0, sense * b), -1)
                else:
                    k, d, _rise = one
                    lay(node, s, tuple(entry[end]), tuple(int(d) if j == 2 * int(k) else 0 for j in range(2 * node.records()[s].shape)), -1)
""")
print("copy written:", dst, "flags: CS4_TAKE_FARTHEST, CS5_CROWD_OFF, CS8_REST, CS8_MERGER_LAY, MG1_WALL, MG1_LOG_WALLS, MG1_TAKE; unset = David's path")
