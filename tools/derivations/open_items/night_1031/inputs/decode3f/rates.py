"""DECODE3e's side probe: the long-run rate of each verdict on fair stand-ins, 1,000 draws a case (decode3e.py's own
definitions, executed up to its stand-in cases). Whole numbers; Rule3's carry the one division. argv: the output name."""
import sys
from pathlib import Path
HERE = Path(__file__).resolve().parent
text = HERE.joinpath("decode3e.py").read_text(encoding="utf-8")
space = {"__file__": str(HERE.joinpath("decode3e.py"))}
exec(compile(text.split("# ---- the stand-in cases")[0], "decode3e.py", "exec"), space)
g = space
lines = []
seed = 31337
for name, xs, n in (("fair, 190 a round, halves of 1,000", g["steady"](190, 1000), 1000),
                    ("fair, 175 a round, halves of 2,000", g["steady"](175, 2000), 1000),
                    ("fair moving, swing, halves of 2,000", g["swing"](2000), 1000)):
    t3b, t3d, half3b, half3d = {}, {}, {}, {}
    for _ in range(n):
        q, seed = g["fair_side"](seed, xs)
        v, hv = g["b3_given"](q, xs, g["D"], 20)
        g["tally"](t3b, v)
        for h in hv:
            g["tally"](half3b, h[0])
        v, hv = g["d3_given"](q, xs, g["D"], 20)
        g["tally"](t3d, v)
        for h in hv:
            g["tally"](half3d, h[0] if h[0] != "NOT SHOWN" or isinstance(h[1], int) else "NOT SHOWN by two values")
    lines.append(f"{name}, {n} draws: (3b) {dict(sorted(t3b.items()))}, by half {dict(sorted(half3b.items()))};"
                 f" (3d) {dict(sorted(t3d.items()))}, by half {dict(sorted(half3d.items()))}")
HERE.joinpath(sys.argv[1]).write_text("\n".join(lines) + "\n", encoding="utf-8")
