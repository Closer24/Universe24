"""eq1's FLAGGED COPY of the engine (toys-5 3177921fb, src/event_universe), written by this script and never by hand: the package copied whole to src_eq1/event_universe, then four exact text replacements, each matching once, else the script refuses. With no flag in the environment the copy is David's path bit for bit (the state hash equal; eq1_run.py prints it).

The flags (environment variables, read once at import):
  EQ1_CROSS=up   the former upward crossing alone (CK-S1 off), to reproduce the bottoms 992 and 966 of David's 6401809807.
  EQ1_LAW=a      the body's click refused by name `arrival` where nothing arrives: the taken row's current F_ij = now_i before_j - before_i now_j is 0 on every one of the Node's six Links at the interval's start (The click is the meeting: a detector receives two quanta, the arriving and its own; no click of one quantum alone).
  EQ1_LAW=b      the credited levels laid back on the taken line at the Node by the one lay act at every credit (nature's equilibrium: what a body takes at rest it lays back), the credit logged with `laid_back` and `dP_back`.
  EQ1_LAW=b0     the lay back where nothing arrives alone (the current 0 on every Link); where a current flows the take stands as the head's.
Run: python make_copy.py (writes src_eq1/)."""
import os, shutil, sys

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.normpath(os.path.join(HERE, '..', '..', '..', 'src', 'event_universe'))
DST = os.path.join(HERE, 'src_eq1', 'event_universe')
if os.path.isdir(os.path.join(HERE, 'src_eq1')):
    shutil.rmtree(os.path.join(HERE, 'src_eq1'))
shutil.copytree(SRC, DST, ignore=shutil.ignore_patterns('__pycache__'))


def replace_once(path, old, new):
    text = open(path, encoding='utf-8').read()
    if text.count(old) != 1:
        sys.exit('refused: the text to replace is not found exactly once in %s:\n%s' % (path, old))
    open(path, 'w', encoding='utf-8').write(text.replace(old, new))


B = os.path.join(DST, 'bodies.py')
N = os.path.join(DST, 'node.py')

# 1. the flags and the helpers (appended to bodies.py)
replace_once(B, 'from event_universe.take import frame_nodes, take_at\n',
'''from event_universe.take import frame_nodes, take_at
import os
from event_universe.core.ports import PORTS
from event_universe.take import lay, momentum_of, neighbour

EQ1_LAW = os.environ.get("EQ1_LAW", "")  # eq1's flag: "" David's path bit for bit; "a", "b", "b0" as make_copy.py names them
EQ1_CROSS = os.environ.get("EQ1_CROSS", "")  # eq1's flag: "up" the former upward crossing alone (CK-S1 off)


def eq1_arrival(node: Node, at: tuple[int, ...], plane_starts: list[list[Line]]) -> int:
    """eq1 (a): what arrives at the Node: the taken row's (the gap-0 line's) current across each of the Node's six Links at the interval's start, F_ij = now_i before_j - before_i now_j, summed in magnitude; 0 where nothing arrives (every Link's current 0, as on a board alike at every Node)."""
    rec0 = node.records().index(node.row(PLANE, gap=0))
    z = plane_starts[rec0][0]
    n, b = int(z.now[at]), int(z.before[at])
    total = 0
    for port in range(PORTS):
        j = neighbour(node, at, port)
        total += abs(n * int(z.before[j]) - b * int(z.now[j]))
    return total


def eq1_lay_back(node: Node, at: tuple[int, ...], taken_was: int) -> dict[str, Any]:
    """eq1 (b): the credited levels laid back on the taken line at the Node by the one lay act (the equilibrium: what a body takes at rest it lays back), the line's now as before the take; the momentum the lay books is the take's negation."""
    rec0 = node.records().index(node.row(PLANE, gap=0))
    row = node.records()[rec0]
    z = row.lines[0]
    back = taken_was - int(z.now[at])
    assert row.pair is not None
    dp = momentum_of(node, z.now, z.before, at, d_now=back, num=row.pair[0])
    lay(node, rec0, at, (back,) + (0,) * (2 * row.shape - 1))
    return {"laid_back": abs(back), "dP_back": dp}
''')

# 2. the crossing read upward alone under EQ1_CROSS=up (CK-S1 off)
replace_once(B, 'lambda b, n: 1 if (int(b) < 0 <= int(n) or int(n) < 0 <= int(b)) else 0,',
                'lambda b, n: 1 if (int(b) < 0 <= int(n) or (EQ1_CROSS != "up" and int(n) < 0 <= int(b))) else 0,')

# 3. the closing under the law's letter (a) or the equilibrium (b, b0)
replace_once(B, '''            if at in born_nodes or frozen[at]:
                continue
            got = take_at(node, at, node.units[rec], r_gap0, 1)
            node.standing[rec][at] = 0
            if got is None:
                continue
            levels, fall, now, before = got
            node.counts["body_clicks"] += 1
            node.log.append(credit(node, rec, at, plane_starts, fall, levels, now, before))
''', '''            if at in born_nodes or frozen[at]:
                continue
            arriving = eq1_arrival(node, at, plane_starts) if EQ1_LAW in ("a", "b0") else 1
            if EQ1_LAW == "a" and arriving == 0:
                node.counts["refused_arrival"] += 1
                node.log.append({"event": "refused", "i": node.interval, "node": list(at), "cause": "arrival", "row": rec})
                node.standing[rec][at] = 0
                continue
            got = take_at(node, at, node.units[rec], r_gap0, 1)
            node.standing[rec][at] = 0
            if got is None:
                continue
            levels, fall, now, before = got
            node.counts["body_clicks"] += 1
            line = credit(node, rec, at, plane_starts, fall, levels, now, before)
            if EQ1_LAW == "b" or (EQ1_LAW == "b0" and arriving == 0):
                line.update(eq1_lay_back(node, at, now))
            node.log.append(line)
''')

# 4. the refusal's count
replace_once(N, '    "refused_stop": 0,\n', '    "refused_stop": 0,\n    "refused_arrival": 0,  # eq1 (a): the closing refused where nothing arrives\n')
print('written', DST)
