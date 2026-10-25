"""bb1's flagged copy of the engine (David's src untouched): src/event_universe copied to engine_bb1/event_universe with ONE
exact text replacement in node.py, named: the swap's trigger reads the strict top X0 < X1 > X2 when the environment holds
BB1_STRICT=1, and the law's weak maximum (X0 <= X1 >= X2 with one strict) when it is absent, bit for bit David's path."""
import os, shutil
HERE = os.path.dirname(os.path.abspath(__file__))
src = os.path.join(HERE, "..", "..", "..", "src", "event_universe")
dst = os.path.join(HERE, "engine_bb1", "event_universe")
if os.path.exists(dst):
    shutil.rmtree(dst)
shutil.copytree(src, dst, ignore=shutil.ignore_patterns("__pycache__"))
p = os.path.join(dst, "node.py")
s = open(p, encoding="utf-8").read()
old = """        peak = np.vectorize(
            lambda a, b, c: (
                int(a) <= int(b) and int(c) <= int(b) and (int(a) < int(b) or int(c) < int(b))
            ),
            otypes=[bool],
        )"""
new = """        import os as _os  # bb1's flag: BB1_STRICT=1 reads the strict top; absent, the law's weak maximum
        if _os.environ.get("BB1_STRICT") == "1":
            peak = np.vectorize(lambda a, b, c: (int(a) < int(b) and int(c) < int(b)), otypes=[bool])
        else:
            peak = np.vectorize(
                lambda a, b, c: (
                    int(a) <= int(b) and int(c) <= int(b) and (int(a) < int(b) or int(c) < int(b))
                ),
                otypes=[bool],
            )"""
assert s.count(old) == 1
open(p, "w", encoding="utf-8").write(s.replace(old, new))
print("copied; one replacement in node.py (the swap's trigger under BB1_STRICT)")
