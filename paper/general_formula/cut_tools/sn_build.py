"""Build a TeX source of the paper in Springer's sn-jnl class and print where every section starts.

Usage: python sn_build.py main.tex [supplement.tex] [--out DIR]. The class and the style are read from
paper/general_formula/sn/; the figures folder beside the source is copied into DIR. A source already in
sn-jnl is built as it is; an article-class source is converted: the packages it loads are kept but geometry,
the section spacing and the line spread, the theorem environments take sn-jnl's styles, and the front
matter (title, author, abstract, keywords) is rewritten in sn-jnl's commands. pdflatex runs three times;
the page count and, when PyMuPDF is installed, the page of every numbered section are printed.
"""

import re
import shutil
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
SN = HERE.parent / "sn"
PREAMBLE = """\\documentclass[sn-mathphys-num]{sn-jnl}
\\usepackage{amsmath,amssymb}
\\usepackage{booktabs,graphicx,caption,float,multicol,enumitem,array,microtype,longtable}
\\setlength{\\columnsep}{14pt}\\setlist{nosep}
\\renewcommand{\\figurename}{Fig.}
"""
KEPT = re.compile(
    r"\\(newcommand|renewcommand\{\\the|newcounter|newenvironment|newcolumntype|hypersetup|newif|ifsubmission)"
)


def convert(source: str) -> str:
    """Rewrite an article-class source for sn-jnl; return a source already in sn-jnl unchanged."""
    preamble_end = source.index("\\begin{document}")
    if "sn-jnl" in source[:preamble_end]:
        return source
    kept = [line for line in source[:preamble_end].split("\n") if KEPT.match(line)]
    theorems = [line for line in source[:preamble_end].split("\n") if line.startswith("\\newtheorem")]
    body = source[preamble_end + len("\\begin{document}") :]
    title = re.search(r"\\title\{(.*)\}", source)
    abstract = re.search(r"\\begin\{abstract\}(.*?)\\end\{abstract\}", body, re.S)
    keywords = re.search(r"\\noindent\\textbf\{Keywords:\} (.*)", body)
    front = "\\begin{document}\n"
    if title and abstract:
        body = body[: abstract.start()] + body[abstract.end() :]
        body = re.sub(r"\\maketitle\s*", "", body, count=1)
        if keywords:
            body = body.replace(keywords.group(0), "", 1)
        front += f"\\title{{{title.group(1)}}}\n\\author*{{\\fnm{{Alon}} \\sur{{Gonen}}}}\\email{{alon@defounder.ai}}\n"
        front += "\\affil{\\orgname{Independent researcher}, \\orgaddress{\\city{Haifa}, \\country{Israel}}}\n"
        front += f"\\abstract{{{abstract.group(1).strip()}}}\n"
        if keywords:
            front += f"\\keywords{{{keywords.group(1).strip()}}}\n"
        front += "\\maketitle\n"
    elif title:
        body = re.sub(r"\\maketitle\s*", "", body, count=1)
        front += f"\\title{{{title.group(1)}}}\n\\author*{{\\fnm{{Alon}} \\sur{{Gonen}}}}\\email{{alon@defounder.ai}}\n"
        front += "\\affil{\\orgname{Independent researcher}, \\orgaddress{\\city{Haifa}, \\country{Israel}}}\n\\maketitle\n"
    styled = "\\theoremstyle{thmstyleone}\n" + "\n".join(theorems) + "\n" if theorems else ""
    return PREAMBLE + styled + "\n".join(kept) + "\n" + front + body


def section_pages(pdf: Path, count: int) -> list[tuple[int, int, str]]:
    try:
        import fitz  # PyMuPDF
    except ImportError:
        return []
    starts: dict[int, tuple[int, str]] = {}
    for number, page in enumerate(fitz.open(pdf), 1):
        for match in re.finditer(r"(?m)^(\d{1,2}) ([A-Z][a-z][^\n]{3,70})$", page.get_text()):
            section = int(match.group(1))
            if section == len(starts) + 1 and section <= count:
                starts[section] = (number, match.group(2)[:45])
    return [(section, *starts[section]) for section in sorted(starts)]


def main() -> None:
    args = sys.argv[1:]
    out = Path(args[args.index("--out") + 1]) if "--out" in args else Path("/tmp/sn_build")
    sources = [Path(name) for name in args if name.endswith(".tex")]
    out.mkdir(parents=True, exist_ok=True)
    for file in SN.iterdir():
        shutil.copy(file, out / file.name)
    for source in sources:
        figures = source.parent / "figures"
        if figures.is_dir() and not (out / "figures").exists():
            shutil.copytree(figures, out / "figures")
        target = out / (source.stem + "_sn.tex")
        target.write_text(convert(source.read_text(encoding="utf-8")), encoding="utf-8")
        for _ in range(3):
            subprocess.run(
                ["pdflatex", "-interaction=nonstopmode", target.name], cwd=out, capture_output=True
            )
        log = (out / (target.stem + ".log")).read_text(encoding="utf-8", errors="ignore")
        errors = log.count("\n!")
        pages = re.search(r"Output written on [^ ]* \((\d+) pages", log)
        print(f"{target.name}: {errors} errors, {pages.group(1) if pages else '?'} pages")
        count = len(re.findall(r"(?m)^\\section\{", source.read_text(encoding="utf-8")))
        for section, page, heading in section_pages(out / (target.stem + ".pdf"), count):
            print(f"  {section:>2} {heading:<45} page {page}")


if __name__ == "__main__":
    main()
