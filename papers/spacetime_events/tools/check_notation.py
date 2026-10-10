"""The paper's mathematical symbols: each symbol used in arrow.tex's mathematics (the equations and the inline mathematics; the figure's captions carry none) is defined in words at or before its first use, and the defining phrase for it occurs once, so that it has one meaning throughout. The table SYMBOLS below is maintained by hand: for each symbol its token inside mathematics, the words that define it, and its meaning. Fails when a first use precedes the definition, when a definition is missing, or when a symbol's defining phrase appears on more than one line. Usage: python3 -I check_notation.py."""
from __future__ import annotations
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import read_tex, strip_comments

# (symbol, its token inside mathematics, the words that define it, the one meaning)
SYMBOLS = [
    ("w", r"(?<![A-Za-z\\])w(?![A-Za-z])", r"divides the total by a fixed whole number \$w\$", "the divisor of the rule"),
    ("R_j", r"R_j", r"\$R_j\$ the weight of that neighbour", "the weight of the neighbour j"),
    ("a_j", r"a_j", r"\$a_j\$ the number arriving from the neighbour \$j\$", "the number arriving from the neighbour j"),
    ("j", r"(?<![A-Za-z\\_])j(?![A-Za-z])", r"the number arriving from the neighbour \$j\$", "a neighbour's index"),
    ("a_next", r"a_\{\\mathrm\{next\}\}", r"\$a_\{\\mathrm\{next\}\}\$ the next number", "the Node's next number"),
    ("a_now", r"a_\{\\mathrm\{now\}\}", r"\$a_\{\\mathrm\{now\}\}\$ and \$a_\{\\mathrm\{before\}\}\$ its two numbers", "the Node's number now"),
    ("a_before", r"a_\{\\mathrm\{before\}\}", r"\$a_\{\\mathrm\{now\}\}\$ and \$a_\{\\mathrm\{before\}\}\$ its two numbers", "the Node's number one tick before"),
    ("S", r"(?<![A-Za-z\\])S(?![A-Za-z])", r"\$S\$ the Node's own weight", "the Node's own weight"),
    ("r", r"(?<![A-Za-z\\])r(?![A-Za-z'])", r"\$r\$ the old remainder", "the old remainder"),
    ("r'", r"(?<![A-Za-z\\])r'", r"\$r'\$ the new one", "the new remainder"),
    ("top", r"\\mathrm\{top\}", r"a top and a bottom number", "the pair's top number"),
    ("bottom", r"\\mathrm\{bottom\}", r"a top and a bottom number", "the pair's bottom number"),
    ("q_0", r"q_0", r"\$q_0\$ at an empty Node", "the rate of an empty Node"),
    ("s", r"(?<![A-Za-z\\])s(?![A-Za-z])", r"the slope \$s = ", "the first-order slope of the swings in the content"),
    ("v_A, v_B", r"v_[AB]", r"A body at the speed \$v_A\$ that sends light to another, at \$v_B\$", "the speeds of the reading body and the read one, in the board's frame"),
    ("u", r"(?<![A-Za-z\\])u(?![A-Za-z])", r"reads the other's speed as \$u = \(v_B - v_A\)/\(1 - v_A v_B/c\^2\)\$, below \$c\$, exactly at every pair, for long flashes", "what one body reads of another's speed by its own clicks"),
    ("k", r"(?<![A-Za-z\\_])k(?![A-Za-z])", r"the two numbers of the Node \$k\$", "a Node's index"),
    ("a (axis)", r"(?<![A-Za-z\\_{])a(?![A-Za-z_])", r"along the axis \$a\$", "an axis of the board"),
    ("now_k, before_k, next_k", r"\\mathrm\{(now|before|next)\}_", r"Write \$\\mathrm\{now\}_k\$ and \$\\mathrm\{before\}_k\$ for the two numbers of the Node", "a Node's numbers by its index"),
    ("F", r"(?<![A-Za-z\\])F(?![A-Za-z])", r"\$F_\{kj\} = ", "the flow into a Node from a neighbour"),
    ("P_a", r"P_a", r"the board's momentum along \$a\$", "the board's momentum along an axis"),
    ("c(n)", r"c\(n\)", r"the speed \$c\(n\)\$ at a Node of content \$n\$", "light's speed at a Node of content n"),
    ("A (height)", r"(?<![A-Za-z\\_{])A(?![A-Za-z_])", r"a pattern of height \$A\$", "the height of a pattern, its largest number"),
    ("T (ticks)", r"(?<![A-Za-z\\_{])T(?![A-Za-z_])", r"\$T/A\$ over \$T\$ ticks", "a count of ticks"),
    ("Delta n", r"\\Delta n", r"the difference \$\\Delta n\$ of \$n\$ across the ray", "the difference of the content across a ray"),
    ("ell", r"\\ell(?!_)", r"a path of length \$\\ell\$", "the length along a path"),
    ("ell_0", r"\\ell_0", r"\$\\ell_0\$ the distance between neighbouring Nodes", "the distance between neighbouring Nodes"),
    ("d_a", r"\\mathbf d|d_a", r"the unit direction \$\\mathbf d\$ with \$d_a\$ its part on the axis \$a\$", "a unit direction and its parts along the axes"),
    ("E", r"(?<![A-Za-z\\])E(?![A-Za-z_])", r"seen up to the energy \$E = 1\$~TeV", "the light's energy"),
    ("E_QG2", r"E_\{\\mathrm\{QG\},2\}", r"with \$E_\{\\mathrm\{QG\},2\}\$ the scale in which such a slowing is written", "the measurement's scale for a quadratic dependence of light's speed on its energy"),
    ("lambda", r"\\lambda", r"\$\\lambda\$ the light's length from one crest to the next", "the light's wavelength"),
    ("hbar", r"\\hbar", r"\$\\hbar\$ is the constant that turns a rate of swinging into an energy", "the constant that turns a rate of swinging into an energy"),
    ("nu", r"\\nu", r"for \$\\nu\$ swings per second", "a rate of swinging, swings per second"),
    ("tau", r"\\tau", r"with \$\\tau\$ the tick's length in seconds", "the tick's length in seconds"),
    ("delta v", r"\\delta v", r"its speed \$v\$ changed by a part \$\|\\delta v/v\|\$", "the change of light's speed"),
    ("rate", r"\\mathrm\{rate\}", r"that sets the Node's rate, a whole number", "the Node's rate"),
    ("turn", r"\\mathrm\{turn\}(?![_])", r"is the detector's turn, an angle measured as a part of one full swing", "an angle as a part of one swing"),
    ("i", r"(?<![A-Za-z\\_])i(?![A-Za-z])", r"the detector \$i\$ adds up", "a detector's index"),
    ("X_i, Y_i", r"[XY]_i", r"two sums, \$X_i\$ and \$Y_i\$", "the detector's two sums over the stretch"),
    ("g", r"(?<![A-Za-z\\])g(?![A-Za-z])", r"a declared strength \$g\$", "the declared strength"),
    ("M", r"(?<![A-Za-z\\])M(?![A-Za-z])", r"a fixed scale \$M\$", "the fixed scale of the turn"),
    ("turn_i", r"\\mathrm\{turn\}_i", r"is the detector's turn, an angle measured", "the detector's turn"),
    ("W_i", r"W_i", r"the detector's weight \$W_i\$ in the toss", "the detector's weight in the toss"),
    ("W_0", r"W_0", r"The no-click weight \$W_0\$", "the no-click weight"),
    ("U", r"(?<![A-Za-z\\])U(?![A-Za-z])", r"what is left of one piece, \$U\$", "what is left of one piece"),
    ("P_i", r"P_i", r"chance \$P_i\$ is its weight over the sum", "the detector's chance"),
    ("t", r"(?<![A-Za-z\\])t(?![A-Za-z])", r"the Nodes at \$t\$ steps at its \$t\$-th tick", "the steps from the taker, the wiping's ticks"),
    ("N(t)", r"N\(t\)", r"the ball within \$t\$ steps holds", "the Nodes within t steps"),
    ("L", r"(?<![A-Za-z\\])L(?![A-Za-z])", r"\$L\$ Nodes wide", "the tube's width in Nodes"),
    ("p", r"(?<![A-Za-z\\])p(?![A-Za-z])", r"a fixed part \$p\$ of a swing", "the part of a swing between neighbouring Nodes of a moving pattern"),
    ("v", r"(?<![A-Za-z\\])v(?![A-Za-z_])", r"the middle's speed \$v\$", "the moving middle's speed"),
    ("turn_0", r"\\mathrm\{turn\}_0", r"\$\\mathrm\{turn\}_0\$ the turn at the empty rate", "the turn at the empty rate"),
    ("Phi", r"\\Phi", r"the potential \$\\Phi\$, the known measure", "the known potential of gravity"),
    ("c_m", r"c_m", r"with \$c_m\^2 = \\mathrm\{turn\}_0 \\cot", "the matter pattern's own long-pattern speed"),
    ("c", r"(?<![A-Za-z\\])c(?![A-Za-z])", r"We write \$c\$ for that speed", "the long-wave speed of light on the board"),
    ("n", r"(?<![A-Za-z\\])n(?![A-Za-z])", r"With \$n\$ units of gravity content at the Node", "the units of gravity content at a Node"),
    ("x", r"(?<![A-Za-z\\])x(?![A-Za-z])", r"\(\$x\$, \$y\$, \$z\$, counted in Nodes\)", "the coordinate along the board's long axis, in Nodes"),
    ("y", r"(?<![A-Za-z\\])y(?![A-Za-z])", r"\(\$x\$, \$y\$, \$z\$, counted in Nodes\)", "the second coordinate, in Nodes"),
    ("z", r"(?<![A-Za-z\\])z(?![A-Za-z])", r"\(\$x\$, \$y\$, \$z\$, counted in Nodes\)", "the third coordinate, in Nodes"),
]


def math_of(line: str) -> str:
    """The mathematics of one source line: the inline $...$ pieces, and the whole line inside an equation environment (tracked by the caller)."""
    return " ".join(re.findall(r"\$([^$]*)\$", line))


def main() -> int:
    lines = strip_comments(read_tex()).splitlines()
    start = next(i for i, l in enumerate(lines) if l.startswith("\\section{"))
    end = next(i for i, l in enumerate(lines) if l.startswith("\\section*{Statements"))
    in_eq = False
    in_table = False
    skipped: set[int] = set()  # the table of symbols collects the definitions; it defines nothing and is skipped
    math_lines: list[tuple[int, str]] = []
    for i in range(start, end):
        l = lines[i]
        if "\\label{tab:symbols}" in l:
            in_table = True
        if in_table:
            skipped.add(i)
            if l.startswith("\\end{table}"):
                in_table = False
            continue
        if "\\begin{equation}" in l:
            in_eq = True
            continue
        if "\\end{equation}" in l:
            in_eq = False
            continue
        m = l if in_eq else math_of(l)
        if m:
            math_lines.append((i + 1, m))
    problems = []
    print(f"{'symbol':9} {'defined':>8} {'first use':>10}  meaning")
    for name, token, definition, meaning in SYMBOLS:
        defs = [i + 1 for i in range(start, end) if i not in skipped and re.search(definition, lines[i])]
        uses = [n for n, m in math_lines if re.search(token, m)]
        d = defs[0] if defs else None
        u = uses[0] if uses else None
        print(f"{name:9} {str(d):>8} {str(u):>10}  {meaning}")
        if d is None:
            problems.append(f"{name}: no definition in words")
        elif u is None:
            problems.append(f"{name}: never used in mathematics (drop it from the table or the paper)")
        elif u < d:
            problems.append(f"{name}: first used in mathematics on line {u}, defined on line {d}")
        if len(defs) > 1:
            problems.append(f"{name}: defined on more than one line ({defs}); one meaning, one definition")
    if problems:
        print("the notation FAILS: " + "; ".join(problems))
        return 1
    print("the notation passes")
    return 0


if __name__ == "__main__":
    sys.exit(main())
