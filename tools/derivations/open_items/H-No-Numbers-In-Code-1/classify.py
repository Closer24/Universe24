"""Group every literal site beyond 0, 1, -1 of literals_all.txt by the form of its expression.

Reads the table literals.py printed; writes literals_classified.txt (one row per site with its
group code and class) and prints the counts per group. The rules are by file, line and literal,
tuned by reading each site in its file; a site no rule catches is printed as UNPLACED.
"""
import re
import sys
from collections import Counter, OrderedDict

RULES = [
    # code, class, description, predicate(file, line, lit, src); the first rule that fits places the site
    ("D-TRACE", "D", "TRACE = 54, a number of the universe under derivation by two hands (rows.py)",
     lambda f, n, v, s: v == 54),
    ("A-PORTS-DEF", "A", "ports.py: AXES = 3 and SIDES = 2, the two definitions the lattice's names rest on",
     lambda f, n, v, s: f.endswith("ports.py")),
    ("A-ROWS-SHAPES", "A", "rows.py: the rows' shapes CARRIER 10, POTENTIAL 4, PLANE 2, QUARTET 8 and the acts' order (3, 4 in order_of)",
     lambda f, n, v, s: f.endswith("rows.py") and n in (11, 12, 13, 14, 112)),
    ("A-HELD-POWERS", "A", "rows.py:74, the held walls' powers: 4 the time line's, 2 the axis lines' (held_wall)",
     lambda f, n, v, s: f.endswith("rows.py") and n == 74),
    ("B-WIDTH", "B", "128 the law's width (decoder.WIDTH); 64 = WIDTH div 2 (rows.HALF_WIDTH), derived and typed",
     lambda f, n, v, s: v in (128, 64)),
    ("C-UNITS", "C", "the readers' units named once with their meaning: the million MIL, the hundred HUNDRED, the thousand THOUSAND, the fewest credits FEW and the fewest spans SPANS (decoder.py), the marks MARKS and EARLY and the thousand (run.py)",
     lambda f, n, v, s: (f.endswith("decoder.py") and n in (13, 14, 15, 17, 18)) or (f.endswith("run.py") and n in (22, 23, 24))),
    ("A-PORTS6", "A", "6 = PORTS in wall_of, w = 6 den Gamma^2 G^2 (ports.py names PORTS the one definition of Rule3's 6)",
     lambda f, n, v, s: v == 6 and f.endswith("rule3.py")),
    ("A-SIDESPORTS12", "A", "12 = SIDES x PORTS, twice the six: the mass D_i (rule3.mass) and the decoder's re-typed weight 12 p0^2 G^2 (decoder.solve)",
     lambda f, n, v, s: v == 12 and (f.endswith("rule3.py") or f.endswith("decoder.py"))),
    ("B-QUADRATIC", "B", "rule3.least_root: the quadratic's own 4 a c, 2 a, and the root's second neighbour s + 2",
     lambda f, n, v, s: f.endswith("rule3.py") and n in (173, 177, 178)),
    ("B-UNIT-3TS", "B", "3 T s the plane's unit (rule3.unit_of, the conventions' row 12)",
     lambda f, n, v, s: v == 3 and f.endswith("rule3.py") and n == 131),
    ("B-HELD-WRITE-4", "B", "4 X (forms 54 den Gamma^2 - trace p0^2) p0 the held write (rule3.held_numerator); 4 Gamma^3 G^2 the share's wall (gram.py:160)",
     lambda f, n, v, s: v == 4 and (f.endswith("rule3.py") and n == 126 or f.endswith("gram.py") and n == 160)),
    ("B-LINK-WALL-4G", "B", "W = 4 Gamma the Link's wall of the tangent triple, typed twice (links.turned, decoder.solve)",
     lambda f, n, v, s: v == 4 and "4 * gamma" in s),
    ("A-POWER-WRITTEN", "A", "x ** 2, x ** 3 (den**2, gamma**2, gamma**3 the paces' N_0, 2 Gamma^3 G^2 the take's weight): the square and the cube by the operator's literal where the code's convention is the product (gamma * gamma * gamma in gram.py:160)",
     lambda f, n, v, s: v in (2, 3) and re.search(r"\*\* ?%d\b" % v, s) is not None and "2 **" not in s.replace("2**", "2 **")),
    ("A-POW2", "A", "2 ** e, 2 ** width: a power of two (the lattice's halves, the width's room): 1 << e",
     lambda f, n, v, s: v == 2 and "2 **" in s.replace("2**", "2 **")),
    ("A-CYC-INDEX", "A", "quartet.py: the slot of a Cyc (a[2], a[3], a[4] the power of two) or a Gauss (g[2] the denominator) read by index; g[:2] the Gaussian's two parts, a[:4] the four coordinates (HALF)",
     lambda f, n, v, s: f.endswith("quartet.py") and v in (2, 3, 4) and (re.search(r"\[%d\]" % v, s) is not None or "[:2]" in s or "[:4]" in s)),
    ("A-HALF-UP", "A", "quartet.nearest: (2 x + n) div 2 n, the half-up rounding (paces.rounded's own form, numerator + numerator over wall + wall)",
     lambda f, n, v, s: f.endswith("quartet.py") and n == 150),
    ("C-CIRCLE", "C", "circle.py (a reader by the law's letter, den's circle from den alone): primality's 2, Pollard's start and doubling, the Gaussian exponent's range 2 e + 1, the primes 1 mod 4",
     lambda f, n, v, s: f.endswith("circle.py")),
    ("C-RECORD-SLOT", "C", "a reader's field read by index: lines[falls[0] - 2], rows[0][2], [\"content min/mean/max\"][2], credited[-2], legs[-2], found[2], argv[2]",
     lambda f, n, v, s: re.search(r"(decoder|clicks|gates|board|predicates|events|run)\.py", f) is not None and v in (2, 3)
        and (re.search(r"\[-?%d\]" % v, s) is not None or re.search(r"\[falls\[0\] - 2\]", s) is not None or "argv[2]" in s)),
    ("C-THREE-LEVELS", "C", "decoder.carrier_levels: the three carrier levels (i - 3, i - 2, i - 1), the reader's own count",
     lambda f, n, v, s: f.endswith("decoder.py") and n == 91),
    ("B-LAW-THIRD", "B", "T div 6 a third of the charge, no third alone (predicates.confinement, row 27)",
     lambda f, n, v, s: v == 6 and f.endswith("predicates.py")),
    ("A-TUPLE-SLOT", "A", "an act's tuple read by index: the Birth's k[2], k[3], kid[2] (close.py), act(...)[2] the write's return (node.py), link(...)[2] the frame sign (readings.py)",
     lambda f, n, v, s: v in (2, 3) and ((f.endswith("close.py") and ("k[" in s or "kid[" in s)) or (f.endswith("node.py") and n == 255) or (f.endswith("readings.py") and n == 70))),
    ("E-REFUSAL-HEAD", "E", "paces.certified: the refusal's message lists undecided[:3], a count no act reads (a message's head)",
     lambda f, n, v, s: f.endswith("paces.py") and n == 81),
    ("A-HALF", "A", "the halving: x // 2, quotient(x, 2), division_forward(x, 2, 0), (low + high) div 2 the bisection's middle, w // 2 the mean wall, rounded(summed, 2) the tension's mean, the readers' middles and means (clicks, decoder.middle, events, predicates T div 2)",
     lambda f, n, v, s: v == 2 and (re.search(r"// 2\b", s) is not None or re.search(r", 2\)", s) is not None
        or re.search(r", 2, 0\)", s) is not None or "rounded(summed, 2)" in s or (f.endswith("decoder.py") and n == 145))),
    ("A-PARITY", "A", "the parity: remainder(x, 2), x % 2, k % 2, reversals % 2 (circle apart)",
     lambda f, n, v, s: v == 2 and (re.search(r"% 2\b", s) is not None or re.search(r"remainder\([^,]+, 2\)", s) is not None)),
    ("C-LISTED", "C", "the readers' list heads and samples typed inline: [:8], [:6], [-6:], [:4], // 8 every eighth, // 3 the last third, words[:2]/[:3], and paces' refusal undecided[:3]",
     lambda f, n, v, s: v in (2, 3, 4, 6, 8) and (re.search(r"\[:%d\]" % v, s) is not None or re.search(r"\[-%d:\]" % v, s) is not None
        or re.search(r"// %d\b" % v, s) is not None or ("words[" in s))),
    ("C-THRESHOLD", "C", "the readers' counts typed inline: fewer than two (len < 2, >= 2), three lifts born (>= 3), the majority (x * 2 > n), the first half and the last quarter (min * 2 <= n, max * 4 >= 3 n), range(2) over the pair's parts",
     lambda f, n, v, s: v in (2, 3, 4) and re.search(r"(decoder|clicks|gates|board|predicates|events|run)\.py", f) is not None
        and ("len(" in s or "* 2 >" in s or "* 2 <=" in s or "range(2)" in s or "< 2" in s or ">= 2" in s)),
    ("B-READER-PULL", "B", "board.lift_of: the pull 2 largest_below(X div Gamma) and the lift over 3 x (LC-S1's forms re-typed by the reader)",
     lambda f, n, v, s: f.endswith("board.py") and n in (132, 133)),
    ("A-AXES3", "A", "3 = AXES: range(3) over the axes (gates, node), the mean over the three axes 3 den (seed.running_rotation), lines[1:4] the three axis lines (readings), parts[0] + parts[1] + parts[2] (links)",
     lambda f, n, v, s: (v == 3 and ("range(3)" in s or "3 * den" in s or "range(nr)] for _ in range(3)" in s or (f.endswith("links.py") and "parts[2]" in s)))
        or (v == 4 and f.endswith("readings.py") and "lines[1:4]" in s) or (v == 2 and f.endswith("links.py") and "parts[2]" in s)),
    ("A-AXES-CYCLIC", "A", "wrap(axis + 2, AXES): the third axis of the cyclic triple, equal to wrap(axis - 1, AXES) (links.row_twist, links.twist, gram.curl)",
     lambda f, n, v, s: v == 2 and "wrap(a" in s),
    ("A-PORT-OF-AXIS", "A", "2 * axis, 2 * a (+1): the Port of an axis and side, SIDES * axis + side (close, gram, links, run, take)",
     lambda f, n, v, s: v == 2 and re.search(r"2 \* (axis|a)\b", s) is not None and not f.endswith("quartet.py")),
    ("A-PLANE-LINES", "A", "the plane's two lines (re, im): xs[0::2], 2 * p (+1), found[2 * p], m[2 * r], quotient(shape, 2), 2 * shape - 1, 2 * PLANE - 1, quotient(QUARTET, 2) = HALF, range(2) over the pair's parts (decoder.solve)",
     lambda f, n, v, s: v == 2 and (re.search(r"\[[01]::2\]", s) is not None or re.search(r"2 \* [prc]\b", s) is not None
        or "quotient(shape, 2)" in s or "2 * node.records()[row].shape" in s or "2 * row.shape" in s or "2 * PLANE" in s or "quotient(QUARTET, 2)" in s
        or (f.endswith("decoder.py") and n == 112)) and not (f.endswith("decoder.py") and n == 145)),
    ("B-SIGN", "B", "rule3.signed_quotient: the sign (x >= 0) * 2 - 1",
     lambda f, n, v, s: f.endswith("rule3.py") and n == 141),
    ("B-RAISED-COSINE", "B", "seed.raised_cosine: the half-widths 2 or 3 (the law's envelope), the doubled cosine 2 cos 0 = 2 and w_k = 2 + 2 cos (Chebyshev's recurrence)",
     lambda f, n, v, s: f.endswith("seed.py") and n in (85, 87, 89, 90)),
    ("B-SECOND-BEAT", "B", "gram.period: k = 2, the search from the second multiple of the count",
     lambda f, n, v, s: f.endswith("gram.py") and n == 222),
    ("B-TWICE", "B", "the law's twice, 2 * x: the reach 2 num p^2 Q (rule3), K-S1's 2 G^2 (2 Gamma - 1), the phase line's 2 Gamma and 2 Gamma^2 and 2 K_0 and 2 D, the count 2 (Phi_now - Phi_before) + c, the own weight 2 w, the mean wall's 2 w X, 2 cphi, 2 w_end, the tangent triple's 2 W n, the circle point's 2 h^2 and 2 h s, the momentum's 2 num, the quartet's scale 2 PORTS Gamma, the decoder's 2 pi^2 Q and the floor's 2 w^2",
     lambda f, n, v, s: v == 2 and re.search(r"\b2 \* ", s) is not None),
]


def main(path):
    rows = []
    for line in open(path, encoding="utf-8"):
        m = re.match(r"^(event_universe/\S+):(\d+) \| (-?\d+) \| int \| (.*)$", line.rstrip("\n"))
        if not m:
            continue
        f, n, v, s = m.group(1), int(m.group(2)), int(m.group(3)), m.group(4)
        if v in (0, 1, -1):
            continue
        rows.append((f, n, v, s))
    counts = Counter()
    by_group = OrderedDict((code, []) for code, *_ in RULES)
    out = []
    for f, n, v, s in rows:
        placed = None
        for code, cls, _desc, pred in RULES:
            if pred(f, n, v, s):
                placed = (code, cls)
                break
        code, cls = placed if placed else ("UNPLACED", "?")
        counts[code] += 1
        if placed:
            by_group[code].append((f, n, v, s))
        out.append(f"{f}:{n} | {v} | {cls} | {code} | {s}")
    with open(path.replace("literals_all.txt", "literals_classified.txt"), "w", encoding="utf-8") as fh:
        fh.write("file:line | literal | class | group | source line\n")
        fh.write("\n".join(out) + "\n")
        fh.write("\n\ngroups:\n")
        for code, cls, desc, _p in RULES:
            fh.write(f"\n[{code}] class {cls}, {counts[code]} sites: {desc}\n")
            for f, n, v, s in by_group[code]:
                fh.write(f"  {f}:{n} | {v} | {s}\n")
    print(f"sites beyond 0, 1, -1: {len(rows)}")
    for code, cls, desc, _p in RULES:
        print(f"{cls} {code:18s} {counts[code]:4d}  {desc[:110]}")
    print(f"? UNPLACED           {counts['UNPLACED']:4d}")
    for f, n, v, s in rows:
        if not any(p(f, n, v, s) for *_a, p in RULES):
            print("  UNPLACED", f, n, v, s[:120])
    by_class = Counter()
    for code, cls, _d, _p in RULES:
        by_class[cls] += counts[code]
    print("by class:", dict(by_class))


if __name__ == "__main__":
    main(sys.argv[1])
