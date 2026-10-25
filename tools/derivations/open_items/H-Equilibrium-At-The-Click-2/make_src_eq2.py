"""eq2's FLAGGED COPY of the engine (toys-5 3177921fb), written by this script and never by hand: src_eq2/event_universe is
David's src/event_universe with ONE file changed, bodies.py, by the exact text replacements below (each must match once, else the
script refuses); the flag EQ2_CLICK in the environment, absent = David's path bit for bit (the state hash equal, checked by
check_flag_absent.py). The three readings of the body's click where nothing arrives (the taken row's current across every one of the
Node's six Links 0 at the interval's start, the meeting's own reading, links.row_current as close.meet reads it):
  EQ2_CLICK=a  the click refused by name `arrival` (no take, no credit; the standing reset as after a click);
  EQ2_CLICK=b  the equilibrium: the exact take as the head, then the taken levels laid back on the gap-0 line by the one lay act in
               the same close, the credit written with `laid_back` = levels and its momentum booked 0 (the light's state unchanged);
  EQ2_CLICK=c  the lay back at every click, arrivals or none (the click a reading that takes nothing).
  EQ2_CROSS=up the crossing read upward alone (the head before CK-S1, e3cfce303), to reproduce the 992 / 966 and 981 / 952 bottoms.
Run: python make_src_eq2.py  (copies src/event_universe to src_eq2/ and rewrites bodies.py there)."""
import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
WORKTREE = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
SRC = os.path.join(WORKTREE, "src", "event_universe")
DST_PKG = os.path.join(HERE, "src_eq2")
DST = os.path.join(DST_PKG, "event_universe")

if os.path.isdir(DST):
    shutil.rmtree(DST)
os.makedirs(DST_PKG, exist_ok=True)
shutil.copytree(SRC, DST, ignore=shutil.ignore_patterns("__pycache__"))

path = os.path.join(DST, "bodies.py")
text = open(path, encoding="utf-8").read()

replacements = [
    (
        '"""The bodies\' closing, the close\'s last act',
        '"""eq2\'s FLAGGED COPY (2026-10-25, make_src_eq2.py names every delta; the flag EQ2_CLICK absent is David\'s path bit for bit).\nThe bodies\' closing, the close\'s last act',
    ),
    (
        "from __future__ import annotations\n\nfrom typing",
        "from __future__ import annotations\n\nimport os\n\nfrom typing",
    ),
    (
        "from event_universe.core.ports import PORT_SIDES\n",
        "from event_universe.core.ports import PORT_SIDES, PORTS\nfrom event_universe.links import row_current\n",
    ),
    (
        "from event_universe.take import frame_nodes, take_at\n",
        "from event_universe.take import frame_nodes, lay, take_at\n\nEQ2_FLAG = os.environ.get(\"EQ2_CLICK\")  # eq2: a, b, c or absent (David's path)\n",
    ),
    (
        "    for rec, row in enumerate(node.records()):\n        standing_now = np.vectorize(",
        "    rec0 = node.records().index(node.row(PLANE, gap=0))\n    z = node.records()[rec0].lines[0]\n    arriving = (\n        [row_current(plane_starts[rec0], port) for port in range(PORTS)] if EQ2_FLAG else []\n    )  # eq2: the taken row's current across the Node's six Links at the interval's start, as close.meet reads it\n    for rec, row in enumerate(node.records()):\n        standing_now = np.vectorize(",
    ),
    (
        """            if at in born_nodes or frozen[at]:
                continue
            got = take_at(node, at, node.units[rec], r_gap0, 1)
            node.standing[rec][at] = 0
            if got is None:
                continue
            levels, fall, now, before = got
            node.counts["body_clicks"] += 1
            node.log.append(credit(node, rec, at, plane_starts, fall, levels, now, before))
""",
        """            if at in born_nodes or frozen[at]:
                continue
            quiet = EQ2_FLAG is not None and (
                EQ2_FLAG == "c" or all(int(c[at]) == 0 for c in arriving)
            )  # eq2: nothing arrives at the Node (every one of its six Links' currents 0)
            if EQ2_FLAG == "a" and quiet:
                node.standing[rec][at] = 0
                node.counts["refused_arrival"] = node.counts.get("refused_arrival", 0) + 1
                node.log.append(
                    {"event": "refused", "i": node.interval, "node": list(at), "cause": "arrival", "row": rec}
                )
                continue
            got = take_at(node, at, node.units[rec], r_gap0, 1)
            node.standing[rec][at] = 0
            if got is None:
                continue
            levels, fall, now, before = got
            node.counts["body_clicks"] += 1
            entry = credit(node, rec, at, plane_starts, fall, levels, now, before)
            if EQ2_FLAG in ("b", "c") and quiet:
                lay(node, rec0, at, (now - int(z.now[at]),) + (0,) * (2 * node.records()[rec0].shape - 1))
                entry["laid_back"] = levels
                entry["dP_take"] = [0, 0, 0]
                node.counts["laid_back"] = node.counts.get("laid_back", 0) + 1
            node.log.append(entry)
""",
    ),
    (
        "                lambda b, n: 1 if (int(b) < 0 <= int(n) or int(n) < 0 <= int(b)) else 0,",
        "                lambda b, n: 1 if (int(b) < 0 <= int(n) or (EQ2_CROSS != \"up\" and int(n) < 0 <= int(b))) else 0,  # eq2: EQ2_CROSS=up the former upward crossing alone (pre CK-S1), absent CK-S1's",
    ),
    (
        "EQ2_FLAG = os.environ.get(\"EQ2_CLICK\")  # eq2: a, b, c or absent (David's path)\n",
        "EQ2_FLAG = os.environ.get(\"EQ2_CLICK\")  # eq2: a, b, c or absent (David's path)\nEQ2_CROSS = os.environ.get(\"EQ2_CROSS\")  # eq2: up = the former upward crossing alone (the head before CK-S1), absent = CK-S1\n",
    ),
]
for old, new in replacements:
    if text.count(old) != 1:
        sys.exit(f"the replacement does not match once: {old[:60]!r} ({text.count(old)})")
    text = text.replace(old, new)
open(path, "w", encoding="utf-8").write(text)
print("src_eq2 written:", path, "replacements:", len(replacements))
