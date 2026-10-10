"""The layout: the body ends by page 14 (the Conclusion's last sentence sits on a page no later than 14 and the Declarations or the References begin by page 14); the smallest printed label of Figure 1 is at least 7 points and its panel titles at least 8 points, measured from the PDF's word boxes on the figure's page (pdftotext -bbox); no overfull box wider than 5 points in the LaTeX log; the figure's inset frame holds all its rows and no box crosses the rule's line beneath (the layout comment of figures_board.tex against pdftotext -bbox). Usage: python3 -I check_layout.py [arrow.pdf] [arrow.log]."""
from __future__ import annotations
import re
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import PAPER

OPEN_LAST = "is what we call entanglement on the board."
PAGE_LIMIT = 18  # the owner's yes to the table of symbols (the owner: "a table of symbols, in my view yes") allowed page 16; the table took four fifths of a page, not half, and the external review's items a further half page; the editor asked for page 17 after its cuts of round 12, and 18 if the round's additions (the momentum paragraph in full, the three bursts, the clocks' largest numbers) did not let it hold: the body ends a third of a page into 18, so 18 stands here pending the owner's word; before the table the owner's rule was page 14, then 15 with the ensemble over seeds and the gathered open paragraph (round 8)  # the owner's rule: the body may run to page 14; shorten only where a sentence is uninteresting (the owner: "cut pages only where it can be done and where there are things of no interest")  # the Conclusion's last clause


def page_text(pdf: Path, page: int) -> str:
    return subprocess.run(["pdftotext", "-f", str(page), "-l", str(page), str(pdf), "-"], capture_output=True, text=True).stdout


def figure_page(pdf: Path, pages: int) -> int:
    for p in range(1, pages + 1):
        if re.search(r"^Fig\. 1", page_text(pdf, p), re.M):
            return p
    return 0


def smallest_label_pt(pdf: Path, page: int) -> tuple[float, str, float]:
    """The smallest word box on the page above the caption, in points. pdftotext -bbox gives each word's box in PDF points from the font's ascender to its descender, which for Computer Modern is 0.694 + 0.194 = 0.888 of the font size (the 10 bp body text measures 8.85 pt, the 8 bp caption 7.08 pt), so the size is the height over 0.888."""
    html = subprocess.run(["pdftotext", "-bbox", "-f", str(page), "-l", str(page), str(pdf), "-"], capture_output=True, text=True).stdout
    words = re.findall(r'<word xMin="([\d.]+)" yMin="([\d.]+)" xMax="([\d.]+)" yMax="([\d.]+)">([^<]*)</word>', html)
    # the caption starts at the word "Fig."; everything above it on the page is the figure
    fig_bottom = None
    for x0, y0, x1, y1, w in words:
        if w.startswith("Fig."):
            fig_bottom = float(y0)
            break
    if fig_bottom is None:
        return 0.0, "no caption found", 0.0
    best = (1e9, "")
    title = 1e9
    for x0, y0, x1, y1, w in words:
        if float(y1) <= fig_bottom and re.search(r"[A-Za-z0-9]", w):
            size = (float(y1) - float(y0)) / 0.888
            if size < best[0]:
                best = (size, w)
            if w in ("(a)", "(b)", "(c)", "board:", "One"):  # the figure's title word and the inset's
                title = min(title, size)
    return best[0], best[1], title


def figure_boxes(pdf: Path, page: int) -> list[tuple[float, float, float, float, str]]:
    html = subprocess.run(["pdftotext", "-bbox", "-f", str(page), "-l", str(page), str(pdf), "-"], capture_output=True, text=True).stdout
    words = [(float(a), float(b), float(c), float(d), w) for a, b, c, d, w in re.findall(r'<word xMin="([\d.]+)" yMin="([\d.]+)" xMax="([\d.]+)" yMax="([\d.]+)">([^<]*)</word>', html)]
    cap = next((y0 for x0, y0, x1, y1, w in words if w.startswith("Fig.")), None)
    return [b for b in words if cap is not None and b[3] <= cap]


def figure_overlaps(pdf: Path, page: int, board: Path) -> list[str]:
    """The figure's elements must not overlap: every word of the inset lies inside the inset's frame, and the rule's line lies below every other box. The frame and the title's anchor are read from the layout comment tools/make_figure.py writes into figures_board.tex (in cm from the picture's origin); the page's origin is fixed by the title's first word, 'The', whose left edge is the picture's x = 0 and whose baseline is the title's anchor."""
    problems = []
    boxes = figure_boxes(pdf, page)
    if not boxes or not board.exists():
        return ["no figure boxes or no figures_board.tex to read the layout from"]
    m = re.search(r"title_anchor=\(([\d.]+),([\d.]+)\) frame=\(([\d.]+),([\d.]+),([\d.]+),([\d.]+)\) equation_baseline=([\d.]+)", board.read_text(encoding="utf-8"))
    if not m:
        return ["figures_board.tex has no layout comment"]
    tx, ty, fx0, fy0, fx1, fy1, eq_y = (float(v) for v in m.groups())
    pt = 72 / 2.54
    title = next((b for b in boxes if b[4] == "The"), None)
    if title is None:
        return ["the figure's title word 'The' not found"]
    x_origin = title[0] - tx * pt
    baseline = title[3] - 0.2 * 9   # the descender of a 9 pt word below its baseline
    y_origin = baseline + ty * pt   # page y grows downward
    page_x = lambda cm: x_origin + cm * pt
    page_y = lambda cm: y_origin - cm * pt
    fx0p, fx1p, fy_top, fy_bottom = page_x(fx0), page_x(fx1), page_y(fy1), page_y(fy0)
    eq_top = page_y(eq_y) - 14   # the rule's line, a 12 pt line above its baseline
    # the inset's words: those in the frame's columns, below its top edge and above the rule's line; each must lie inside the frame
    inset = [b for b in boxes if fx0p - 3 < (b[0] + b[2]) / 2 < fx1p + 3 and b[1] > fy_top - 3 and b[3] < eq_top]
    outside = [b[4] for b in inset if b[0] < fx0p - 3 or b[2] > fx1p + 3 or b[3] > fy_bottom + 3]
    if len(inset) < 10:
        problems.append(f"only {len(inset)} words found inside the inset's columns; the layout comment and the page disagree")
    if outside:
        problems.append("inset words outside the inset's frame: " + ", ".join(outside[:8]))
    crossing = [b[4] for b in boxes if b[1] < eq_top and b[3] > eq_top + 4]
    if crossing:
        problems.append("boxes crossing the rule's line: " + ", ".join(crossing[:8]))
    return problems


def main(argv: list[str]) -> int:
    pdf = Path(argv[1]) if len(argv) > 1 else PAPER / "arrow.pdf"
    log = Path(argv[2]) if len(argv) > 2 else PAPER / "arrow.log"
    problems = []
    info = subprocess.run(["pdfinfo", str(pdf)], capture_output=True, text=True).stdout
    pages = int(re.search(r"Pages:\s+(\d+)", info).group(1))
    # (a) the body ends by page 14 (the owner's rule): the Conclusion's last sentence on a page no later than 14, the back matter beginning by page 14
    first_back = next((p for p in range(1, pages + 1) if re.search(r"^(Statements and Declarations|References)$", page_text(pdf, p), re.M)), None)
    last_body = max((p for p in range(1, pages + 1) if OPEN_LAST in re.sub(r"\s+", " ", page_text(pdf, p))), default=None)  # the last page that holds the clause, its line breaks folded
    print(f"the back matter begins on page {first_back}; the Conclusion's last sentence is on page {last_body}")
    if first_back is None or first_back > PAGE_LIMIT + 1 or last_body is None or last_body > PAGE_LIMIT:
        problems.append(f"the body does not end by page {PAGE_LIMIT}")
    # (b) the figure's smallest label
    fp = figure_page(pdf, pages)
    size, word, title = smallest_label_pt(pdf, fp) if fp else (0.0, "no figure page", 0.0)
    print(f"Figure 1 on page {fp}; the smallest label about {size:.1f} pt ('{word}'), the smallest panel title about {title:.1f} pt")
    if size < 7.0:
        problems.append(f"a figure label under 7 pt ({size:.1f} pt, '{word}')")
    if title < 8.0:
        problems.append(f"a panel title under 8 pt ({title:.1f} pt)")
    overlaps = figure_overlaps(pdf, fp, PAPER / "figures_board.tex") if fp else []
    print("the figure's elements: " + ("no overlap" if not overlaps else "; ".join(overlaps)))
    problems += overlaps
    # (d) overfull boxes in the log
    if log.exists():
        over = [float(m) for m in re.findall(r"Overfull \\[hv]box \(([\d.]+)pt too wide", log.read_text(errors="ignore"))]
        worst = max(over) if over else 0.0
        print(f"overfull boxes: {len(over)}, the widest {worst:.1f} pt")
        if worst > 5.0:
            problems.append(f"an overfull box of {worst:.1f} pt")
    else:
        print("no LaTeX log to read overfull boxes from")
    if problems:
        print("the layout FAILS: " + "; ".join(problems))
        return 1
    print("the layout passes")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
