"""Figure 1 of arrow.tex, drawn as TikZ into figures_board.tex: a block of cube Nodes, six by six by six, each with a dot on every face the eye sees and short rods to its six neighbours; an inset with one Node, its six arrows (one step per tick each, no digit on them) and a small list of its whole numbers by name, no value of any board; the title and the subtitle in the paper's words; the rule, equation (1), beneath. Deterministic, numpy only, python3 -I. The cubes are three parallelograms each, drawn from the back to the front (the painter's order: the larger x + y first, the lower z first), the rods between a cube and its neighbours drawn after the neighbour behind and before the cube in front. Usage: python3 -I make_figure.py [figures_board.tex]."""
from __future__ import annotations
import sys
from pathlib import Path

import numpy as np

N = 6            # Nodes along each axis
PITCH = 1.5      # the distance between the centres of neighbouring cubes, in cube sides
K = 0.40         # cm per cube side on the page
WIDTH_CM = 13.1  # the text width
OUT = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).resolve().parent.parent / "figures_board.tex"


def proj(x: float, y: float, z: float, k: float = K, ox: float = 0.0, oy: float = 0.0) -> str:
    """A point of the block on the page: x to the right and back, y to the left and back, z up (a view from the front and above)."""
    px = 0.866 * (x - y) * k + ox
    py = (0.45 * (x + y) + 0.95 * z) * k + oy
    return f"({px:.3f},{py:.3f})"


def cube(x: float, y: float, z: float, k: float, ox: float, oy: float, side: float = 1.0, dots: bool = True) -> list[str]:
    """The three faces the eye sees (the top, the face at smaller x on the left, the face at smaller y on the right) and a dot on each."""
    p = lambda a, b, c: proj(a, b, c, k, ox, oy)
    s = side
    out = [
        f"\\fill[gray!12] {p(x,y,z+s)} -- {p(x+s,y,z+s)} -- {p(x+s,y+s,z+s)} -- {p(x,y+s,z+s)} -- cycle;",
        f"\\fill[gray!34] {p(x,y,z)} -- {p(x,y+s,z)} -- {p(x,y+s,z+s)} -- {p(x,y,z+s)} -- cycle;",
        f"\\fill[gray!52] {p(x,y,z)} -- {p(x+s,y,z)} -- {p(x+s,y,z+s)} -- {p(x,y,z+s)} -- cycle;",
        f"\\draw[gray!65, line width=0.3pt] {p(x,y,z+s)} -- {p(x+s,y,z+s)} -- {p(x+s,y+s,z+s)} -- {p(x,y+s,z+s)} -- cycle {p(x,y,z)} -- {p(x,y+s,z)} -- {p(x,y+s,z+s)} {p(x,y,z)} -- {p(x+s,y,z)} -- {p(x+s,y,z+s)} {p(x,y,z)} -- {p(x,y,z+s)};",
    ]
    if dots:
        r = 0.045 * k / 0.57
        for c in ((x + s / 2, y + s / 2, z + s), (x, y + s / 2, z + s / 2), (x + s / 2, y, z + s / 2)):
            out.append(f"\\fill[black!75] {p(*c)} circle[radius={r:.3f}];")
    return out


def block(ox: float, oy: float) -> list[str]:
    out = []
    order = sorted(((x, y, z) for x in range(N) for y in range(N) for z in range(N)), key=lambda t: (-(t[0] + t[1]), t[2]))
    p = lambda a, b, c: proj(a, b, c, K, ox, oy)
    for i, j, l in order:
        x, y, z = i * PITCH, j * PITCH, l * PITCH
        rods = []
        if i + 1 < N:  # the neighbour behind to the right, already drawn
            rods.append((p(x + 1, y + 0.5, z + 0.5), p(x + PITCH, y + 0.5, z + 0.5)))
        if j + 1 < N:  # the neighbour behind to the left
            rods.append((p(x + 0.5, y + 1, z + 0.5), p(x + 0.5, y + PITCH, z + 0.5)))
        if l > 0:      # the neighbour below
            rods.append((p(x + 0.5, y + 0.5, z), p(x + 0.5, y + 0.5, z - (PITCH - 1))))
        for a, b in rods:
            out.append(f"\\draw[gray!70, line width=0.9pt] {a} -- {b};")
        out += cube(x, y, z, K, ox, oy)
    return out


ROWS = [("gravity, content $n$", ""), ("the Node's rate", ""), ("light, now", ""), ("light, before", ""), ("light, remainder", ""), ("matter, now", ""), ("matter, before", ""), ("matter, remainder", "")]  # the Node's whole numbers by name, no value of any board
ROW_CM = 9.5 * 0.9 / 72 * 2.54   # one table row: the 8 pt font's 9.5 pt line times the array stretch, in cm
TABLE_TOP = 3.45                  # the table's top below the inset's top edge, in cm (the title, the cube with its arrows and the note above it)


def inset_height() -> float:
    """The inset's frame is as tall as its contents: the table's rows (the header and one per row) plus a margin."""
    return TABLE_TOP + (len(ROWS) + 1) * ROW_CM + 0.12


def inset(ox: float, oy: float, height: float) -> list[str]:
    """One Node: a cube with six arrows, one per neighbour, each one step per tick, and the table of its whole numbers; laid out from the box's top edge down, the frame drawn around the whole of it."""
    k = 0.8
    top = oy + height
    cx, cy = ox + 2.0, top - 2.0  # the cube's centre
    out = [f"\\draw[black!80, line width=0.5pt] ({ox:.2f},{oy:.2f}) rectangle ({ox + 4.0:.2f},{top:.2f});",
           f"\\node[font=\\small\\bfseries, anchor=north] at ({ox + 2.0:.2f},{top - 0.12:.2f}) {{One Node}};"]
    far = [((1, 0.5, 0.5), (1.9, 0.5, 0.5)), ((0.5, 1, 0.5), (0.5, 1.9, 0.5)), ((0.5, 0.5, 0), (0.5, 0.5, -0.9))]
    near = [((0, 0.5, 0.5), (-0.9, 0.5, 0.5)), ((0.5, 0, 0.5), (0.5, -0.9, 0.5)), ((0.5, 0.5, 1), (0.5, 0.5, 1.9))]
    p = lambda a, b, d: proj(a - 0.5, b - 0.5, d - 0.5, k, cx, cy)
    lab = lambda a, b: p(b[0] + (b[0] - a[0]) * 0.3, b[1] + (b[1] - a[1]) * 0.3, b[2] + (b[2] - a[2]) * 0.3)
    for a, b in far:  # the arrows out of the faces the eye does not see, grey, behind the cube
        out.append(f"\\draw[-latex, gray!60, line width=0.8pt] {p(*a)} -- {p(*b)};")
    out += cube(-0.5, -0.5, -0.5, k, cx, cy)
    for a, b in near:
        out.append(f"\\draw[-latex, black, line width=0.9pt] {p(*a)} -- {p(*b)};")
    out.append(f"\\node[font=\\FigLabel, anchor=north, align=center, text width=3.7cm, inner sep=0pt] at ({ox + 2.0:.2f},{top - 2.6:.2f}) {{six arrows, one per neighbour, each one step per tick}};")
    table = "\\\\ ".join(a for a, b in ROWS)
    out.append(f"\\node[font=\\FigLabel, anchor=north west, inner sep=0pt] at ({ox + 0.2:.2f},{top - TABLE_TOP:.2f}) {{\\setlength{{\\tabcolsep}}{{2pt}}\\renewcommand{{\\arraystretch}}{{0.9}}\\begin{{tabular}}{{l}}its whole numbers:\\\\[1pt] {table}\\end{{tabular}}}};")
    return out


def main() -> int:
    lines = ["% Figure 1, written by tools/make_figure.py; do not edit by hand.", "\\newcommand{\\FigureBoard}{%", "\\begin{tikzpicture}[x=1cm, y=1cm]"]
    # the block: its page extent
    w_units = (N - 1) * PITCH + 1
    half_w = 0.866 * w_units * K
    block_h = (0.45 * 2 * w_units + 0.95 * w_units) * K
    ox = half_w + 0.1           # the block's left edge at 0.1 cm
    ins_h = inset_height()
    extra = max(0.0, ins_h - block_h + 0.1)   # the inset taller than the block: the block is lifted so that both clear the rule beneath
    oy = 1.45 + extra            # the block's bottom, above the equation
    lines += block(ox, oy)
    top = oy + block_h + 0.15
    ins_x, ins_y = WIDTH_CM - 4.1, oy + 0.1 - extra
    lines += inset(ins_x, ins_y, ins_h)
    title_y = top + 0.95
    lines.insert(1, f"% layout in cm from the picture's origin: title_anchor=(0.00,{title_y:.2f}) frame=({ins_x:.2f},{ins_y:.2f},{ins_x + 4.0:.2f},{ins_y + ins_h:.2f}) equation_baseline=0.75 (the inset's frame around all its rows, the rule below the block and the inset)")
    # the title and the subtitle
    lines.append(f"\\node[font=\\small\\bfseries, anchor=south west, inner sep=0pt] at (0,{title_y:.2f}) {{The board: Nodes of whole numbers, six neighbours each, one bound}};")
    lines.append(f"\\node[font=\\FigLabel, anchor=north west, text width={WIDTH_CM - 0.3:.1f}cm, inner sep=0pt] at (0,{top + 0.8:.2f}) {{Each tick, every Node reads its six neighbours and writes only itself; nothing moves more than one step per tick; a long pattern of light moves at $c$, about 0.58 Node per tick.}};")
    # the rule beneath, equation (1) in the paper's notation, and one line of words
    lines.append(f"\\node[font=\\large, anchor=south, inner sep=0pt] at ({WIDTH_CM / 2:.2f},0.75) {{$w\\,a_{{\\mathrm{{next}}}} + r' = \\sum_{{\\text{{six}}}} R_j\\,a_j + S\\,a_{{\\mathrm{{now}}}} - w\\,a_{{\\mathrm{{before}}}} + r, \\quad 0 \\le r' < w$}};")
    lines.append(f"\\node[font=\\FigLabel, anchor=north, align=center, text width={WIDTH_CM - 0.4:.1f}cm, inner sep=0pt] at ({WIDTH_CM / 2:.2f},0.55) {{the one rule at every Node, every tick, the remainder kept; every step can be undone.}};")
    lines += ["\\end{tikzpicture}}", ""]
    OUT.write_text("\n".join(lines), encoding="utf-8")
    print(f"make_figure: {len(lines)} lines of TikZ, the block {2 * half_w:.1f} by {block_h:.1f} cm, the inset {ins_h:.1f} cm tall, written to {OUT.name}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
