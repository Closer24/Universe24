"""cs5's second copy (src_cs5b from src_cs5, the four flags kept): the taken line logged PER TAKE and not as the close's last (cs4's copy logged node.last_line at the children's lay, after every take of the close had run, so a close whose takes used both lines logged the last take's line on every birth and close.unclick restored the wrong line; cs4's run back of 10 of 10 covered the last ten intervals, which held no birth, so the flaw was not measured). Under CS4_TAKE_FARTHEST=1 take.take_at keeps the line per (Node, taken record) in node.taken_lines and close.children logs that; unset, the line is 0 as David's path.
Usage: python make_copy_cs5b.py"""
import os
import shutil

here = os.path.dirname(os.path.abspath(__file__))
src = os.path.join(here, "src_cs5", "event_universe")
root = os.path.join(here, "src_cs5b")
dst = os.path.join(root, "event_universe")
if os.path.exists(root):
    shutil.rmtree(root)
shutil.copytree(src, dst, ignore=shutil.ignore_patterns("__pycache__"))


def replace_once(path, old, new):
    s = open(path).read()
    assert s.count(old) == 1, ("the site is not unique", path, old[:60])
    open(path, "w").write(s.replace(old, new))


p = os.path.join(dst, "take.py")
replace_once(p, """    node.last_line = k
    z = row.lines[k]
""", """    node.last_line = k
    if not hasattr(node, "taken_lines"):
        node.taken_lines = {}
    node.taken_lines[(at, taken)] = k
    z = row.lines[k]
""")
p = os.path.join(dst, "close.py")
replace_once(p, """                "taken_row": rec,
                "taken_line": getattr(node, "last_line", 0),
                "proper": int(node.proper[at]),""", """                "taken_row": rec,
                "taken_line": getattr(node, "taken_lines", {}).get((at, rec), 0),
                "proper": int(node.proper[at]),""")
print("copy written:", dst, "the taken line per take (take.py, close.py)")
