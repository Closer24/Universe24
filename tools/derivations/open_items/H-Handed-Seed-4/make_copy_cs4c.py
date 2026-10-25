"""cs4's third copy (src_cs4c, from src_cs4b: the three flags kept), the mended take behind the flag CS4_TAKE_FARTHEST=1: take.take_at moves the taken record's line with the largest now^2 - before^2 at the Node (the fall's own sign; the first such line where equal; the first form of this flag, |now - before|, tied on the pattern and chose the re line at every class, measured on l4_q5_nb_far: 32 + 32 births at i 1 and 2 by the first line alone; the first line unflagged, David's path bit for bit), logs the taken line in the birth and the credit, and close.unclick restores that line; so the take is covariant under the record's quarter turn (the re and im lines exchanged) and the classes whose re line holds 0 can pay with their im line at the same interval.
Usage: python make_copy_cs4c.py"""
import os
import shutil

here = os.path.dirname(os.path.abspath(__file__))
src = os.path.join(here, "src_cs4b", "event_universe")
root = os.path.join(here, "src_cs4c")
dst = os.path.join(root, "event_universe")
if os.path.exists(root):
    shutil.rmtree(root)
shutil.copytree(src, dst, ignore=shutil.ignore_patterns("__pycache__"))
p = os.path.join(dst, "take.py")
s = open(p).read()
old = """    row = node.records()[taken]
    z = row.lines[0]
    levels, fall = fall_of(node, at, walls, rule, z)
"""
new = """    row = node.records()[taken]
    k = 0
    if os.environ.get("CS4_TAKE_FARTHEST", "") == "1":  # cs4's flag: the line whose level now stands farthest from its before
        gaps = [int(line.now[at]) ** 2 - int(line.before[at]) ** 2 for line in row.lines]  # the fall's own sign: positive where the move toward before lowers now^2
        k = gaps.index(max(gaps))
    node.last_line = k
    z = row.lines[k]
    levels, fall = fall_of(node, at, walls, rule, z)
"""
assert s.count(old) == 1
s = s.replace(old, new)
old2 = """    lay(node, taken, at, (toward * levels,) + (0,) * (2 * row.shape - 1))
"""
new2 = """    lay(node, taken, at, tuple(toward * levels if j == 2 * k else 0 for j in range(2 * row.shape)))
"""
assert s.count(old2) == 1
s = s.replace(old2, new2)
s = s.replace("import numpy as np\n", "import numpy as np\nimport os\n", 1)
open(p, "w").write(s)
p = os.path.join(dst, "close.py")
s = open(p).read()
old3 = """                "taken_row": rec,
                "proper": int(node.proper[at]),"""
new3 = """                "taken_row": rec,
                "taken_line": getattr(node, "last_line", 0),
                "proper": int(node.proper[at]),"""
assert s.count(old3) == 1
s = s.replace(old3, new3)
old4 = """        "taker": [taken_was, taken_before, levels],
        "dP_take": node.last_dp,"""
new4 = """        "taker": [taken_was, taken_before, levels],
        "taken_line": getattr(node, "last_line", 0),
        "dP_take": node.last_dp,"""
assert s.count(old4) == 1
s = s.replace(old4, new4)
old5 = """            row = entry.get("taken_row", rec0)
            line = node.records()[row].lines[0]
            lay(
                node,
                row,
                at,
                (entry["taken_now_was"] - int(line.now[at]),)
                + (0,) * (2 * node.records()[row].shape - 1),
            )"""
new5 = """            row = entry.get("taken_row", rec0)
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
            )"""
assert s.count(old5) == 1
s = s.replace(old5, new5)
open(p, "w").write(s)
print("copy written:", dst, "flag: CS4_TAKE_FARTHEST (take.py, close.py)")
