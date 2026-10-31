"""DECODE3e's side probe: where does (3b)'s carried bound bind by itself? It reads the passing alone, so each passing
shape is read once per half: the windows read by the two cells, and the bound's own z^2 against CUT. decode3e.py's
definitions executed up to its stand-in cases. Whole numbers; Rule3's carry the one division. argv: the output name."""
import sys
from pathlib import Path
HERE = Path(__file__).resolve().parent
text = HERE.joinpath("decode3e.py").read_text(encoding="utf-8")
space = {"__file__": str(HERE.joinpath("decode3e.py"))}
exec(compile(text.split("# ---- the stand-in cases")[0], "decode3e.py", "exec"), space)
g = space
carry, D, UNIT, CUT, FIVE = g["carry"], g["D"], g["UNIT"], g["CUT"], g["FIVE"]


def bound_half(x, kmin):
    H = len(x)
    w = g["ladder_top"](H, kmin)
    K, _ = carry(H, w, 0)
    V = B = Kr = 0
    for j in range(K):
        xs = x[j * w:j * w + w]
        X, Vk = sum(xs), sum(v * (D - v) for v in xs)
        if X < FIVE * D or w * D - X < FIVE * D or Vk == 0:
            continue
        W4 = sum(v * (D - v) * (D * D - 6 * v * (D - v)) for v in xs)
        V += 2 * UNIT + carry(UNIT * W4, Vk * Vk, 0)[0]
        B += g["up"](UNIT * D * D, Vk)
        Kr += 1
    if Kr < kmin:
        return "cells", Kr, None
    zb = None if B >= UNIT * Kr else carry((UNIT * Kr - B) * (UNIT * Kr - B), V, 0)[0]
    return ("bound" if zb is None or zb <= CUT else "read"), Kr, zb


lines = []
shapes = [(f"steady {p}, halves of {H}", g["steady"](p, H)) for p, H in
          ((40, 1000), (70, 2560), (100, 1000), (175, 2000), (190, 1000), (250, 2000), (300, 2000), (313, 240),
           (313, 480), (400, 2000), (500, 240), (500, 320), (688, 240), (800, 400), (950, 400))]
shapes += [("swing, halves of 2,000", g["swing"](2000)), ("wide, halves of 1,000", g["wide"](1000)),
           ("step, halves of 2,000", g["step"](2000))]
for name, xs in shapes:
    H, _ = carry(len(xs), 2, 0)
    row = []
    for kmin in (15, 20, 30):
        row.append(f"K_MIN {kmin}: " + ", ".join(str(bound_half(h, kmin)) for h in (xs[:H], xs[H:])))
    lines.append(f"{name}: " + "; ".join(row) + "  [(why, windows read, the bound's own z^2) per half]")
HERE.joinpath(sys.argv[1]).write_text("\n".join(lines) + "\n", encoding="utf-8")
