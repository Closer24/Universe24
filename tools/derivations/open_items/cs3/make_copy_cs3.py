"""cs3's flagged copy of the engine (ck1's third replacement alone, the text ck1's make_copy_ck1.py verbatim): src/event_universe copied whole to src_cs3/event_universe; CK1_CROSS=1 reads the record's re line's zero crossing in either direction in close.bodies (even under the line's negation; the beat the half period); the flag unset is David's path bit for bit (measured: the first 50 intervals of cyc_c14_q2 equal in every Node's X and every count).
Usage: python make_copy_cs3.py (writes src_cs3/ beside this file)."""
import os
import shutil

here = os.path.dirname(os.path.abspath(__file__))
src = os.path.join(here, "..", "..", "..", "src", "event_universe")
root = os.path.join(here, "src_cs3")
dst = os.path.join(root, "event_universe")
if os.path.exists(root):
    shutil.rmtree(root)
shutil.copytree(src, dst, ignore=shutil.ignore_patterns("__pycache__"))
p = os.path.join(dst, "close.py")
s = open(p).read()
old_up = """        upward = np.vectorize(lambda b, n: 1 if (int(b) < 0 <= int(n)) else 0, otypes=[object])(
            re.before, re.now
        )
"""
new_up = """        if os.environ.get("CK1_CROSS", "") == "1":  # ck1's flag: the zero crossing in either direction, even under the line's negation
            upward = np.vectorize(
                lambda b, n: 1 if (int(b) < 0 <= int(n) or int(n) < 0 <= int(b)) else 0, otypes=[object]
            )(re.before, re.now)
        else:
            upward = np.vectorize(lambda b, n: 1 if (int(b) < 0 <= int(n)) else 0, otypes=[object])(
                re.before, re.now
            )
"""
assert s.count(old_up) == 1, "the crossing site is not unique (close.py)"
s = s.replace(old_up, new_up)
s = s.replace("import numpy as np\n", "import numpy as np\nimport os\n", 1)
open(p, "w").write(s)
print("copy written:", dst, "flag: CK1_CROSS (close.py); unset = David's path")
