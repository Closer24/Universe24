"""cs5's flagged copy of the engine (rebuilt from cs4's three makers in one chain, src untouched): src/event_universe copied whole to src_cs5/event_universe with four flags, each unset bit for bit David's path:
  CK1_CROSS=1 (close.bodies): the re line's zero crossing read in either direction (CK-S1);
  CS4_LIGHT_NO_BODY=1 (close.bodies): the plane at the gap 0 never credited as a body;
  CS4_NO_BIRTH=1 (close.refuse): a reader's control, every lay refused by name;
  CS4_TAKE_FARTHEST=1 (take.take_at, close.unclick): the take moves the line of the taken record with the largest now^2 - before^2 (the fall's own sign; the first where equal), the taken line logged and restored (CS4-S2).
Usage: python make_copy_cs5.py (writes src_cs5/ beside this file)."""
import os
import shutil

here = os.path.dirname(os.path.abspath(__file__))
src = os.path.join(here, "..", "..", "..", "src", "event_universe")
root = os.path.join(here, "src_cs5")
dst = os.path.join(root, "event_universe")
if os.path.exists(root):
    shutil.rmtree(root)
shutil.copytree(src, dst, ignore=shutil.ignore_patterns("__pycache__"))


def replace_once(path, old, new):
    s = open(path).read()
    assert s.count(old) == 1, ("the site is not unique", path, old[:60])
    open(path, "w").write(s.replace(old, new))


p = os.path.join(dst, "close.py")
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
replace_once(p, """    kept = []
    for at, s, minus, plus, room, rec in born:
        if int(owns[s][minus]) > 0 or int(owns[s][plus]) > 0:""", """    kept = []
    for at, s, minus, plus, room, rec in born:
        if os.environ.get("CS4_NO_BIRTH", "") == "1":  # cs4's control: no child on the board
            refused(node, at, "lay", control=1, row=rec)
            continue
        if int(owns[s][minus]) > 0 or int(owns[s][plus]) > 0:""")
replace_once(p, """                "taken_row": rec,
                "proper": int(node.proper[at]),""", """                "taken_row": rec,
                "taken_line": getattr(node, "last_line", 0),
                "proper": int(node.proper[at]),""")
replace_once(p, """        "taker": [taken_was, taken_before, levels],
        "dP_take": node.last_dp,""", """        "taker": [taken_was, taken_before, levels],
        "taken_line": getattr(node, "last_line", 0),
        "dP_take": node.last_dp,""")
replace_once(p, """            row = entry.get("taken_row", rec0)
            line = node.records()[row].lines[0]
            lay(
                node,
                row,
                at,
                (entry["taken_now_was"] - int(line.now[at]),)
                + (0,) * (2 * node.records()[row].shape - 1),
            )""", """            row = entry.get("taken_row", rec0)
            k = int(entry.get("taken_line", 0))
            line = node.records()[row].lines[k]
            lay(
                node,
                row,
                at,
                tuple(
                    (entry["taken_now_was"] - int(line.now[at])) if j == 2 * k else 0
                    for j in range(2 * node.records()[row].shape)
                ),
            )""")
replace_once(p, "import numpy as np\n", "import numpy as np\nimport os\n")
p = os.path.join(dst, "take.py")
replace_once(p, """    row = node.records()[taken]
    z = row.lines[0]
    levels, fall = fall_of(node, at, walls, rule, z)
""", """    row = node.records()[taken]
    k = 0
    if os.environ.get("CS4_TAKE_FARTHEST", "") == "1":  # cs4's flag: the line whose level now stands farthest from its before
        gaps = [int(line.now[at]) ** 2 - int(line.before[at]) ** 2 for line in row.lines]
        k = gaps.index(max(gaps))
    node.last_line = k
    z = row.lines[k]
    levels, fall = fall_of(node, at, walls, rule, z)
""")
replace_once(p, """    lay(node, taken, at, (toward * levels,) + (0,) * (2 * row.shape - 1))
""", """    lay(node, taken, at, tuple(toward * levels if j == 2 * k else 0 for j in range(2 * row.shape)))
""")
replace_once(p, "import numpy as np\n", "import numpy as np\nimport os\n")
print("copy written:", dst, "flags: CK1_CROSS, CS4_LIGHT_NO_BODY, CS4_NO_BIRTH (close.py), CS4_TAKE_FARTHEST (take.py, close.py); unset = David's path")
