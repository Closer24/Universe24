"""The short version's checker: three checks of a short main text and a short supplement against the
frozen long version of the paper, one plain-text report, exit code 0 when every check passes.

1. The number audit. Every number written in the short files' text (integers, thousands groups,
   decimals, percentages, powers of ten in their TeX forms, scientific forms and simple fractions)
   is found in the long version's two files, after both are normalised to one form: a thousands
   group loses its separators, \\frac{a}{b}, \\tfrac ab, a / b and a/b are the fraction a/b, and
   10^{-21}, 10^-21, 2 \\times 10^{28}, 2 \\cdot 10^{28} and 1.3e11 are the power forms 1e-21, 2e28
   and 1.3e11. A composed number whose parts (the mantissa and the bare power, the numerator and the
   denominator) both stand in the long version is found by its parts and listed as such. TeX layout
   is not a number of the text and is ignored: the preamble, the comments and the bibliography; the
   pointer, URL, identity and layout macros; dimensions such as 8pt or 0.66\\textwidth; a digit run
   glued to a letter (a name such as Universe24, Rule3, GW170817 or a commit hash; a macro glued to
   digits is not a name, \\tfrac12 is the fraction 1/2); the number right after a pointer word
   (Section 3.4, Eq. (4), Theorem 2, line (1), S.12 (22)) and the number opening a sectioning
   command. Every miss is printed as MISS with its file, line, the number as written and its
   normalised form, under it the line (its 160 characters around the number when it is longer).
2. The pointer check. Every \\ref, \\eqref, \\autoref, \\cref and \\pageref of the short files resolves
   to a \\label of the short files together (or of an .aux file given with --xr-aux); every literal
   pointer S.n of the short files names a derivation the short supplement defines, the convention
   detected from the supplement and named in the report (its \\section*{S.n ...} headings, else the
   environment whose counter prints S.n, else its \\section commands); every \\cite key has its
   \\bibitem in the same document (or an entry of a BibTeX file given with --bib).
3. The labels of the long main text's theorems, propositions, assumptions and equations: a table
   saying whether the short main text or the short supplement still carries each label. This is
   information for the editor, not a failure.

    python paper/general_formula/short_checker.py --short-main PATH --short-supplement PATH
        [--long-ref COMMIT] [--long-main PATH --long-supplement PATH] [--xr-aux PATH] [--bib PATH]
        [--verbose]
    python paper/general_formula/short_checker.py --self-test [--verbose]

The self-test runs the long version against itself (short = long) and must report 0 misses and
0 unresolved pointers; with --verbose it prints the inventory of the numbers found and every ignored
token by rule, so that the ignore rules can be read off the long version itself.
"""

from __future__ import annotations

import argparse
import bisect
import re
import subprocess
import sys
from dataclasses import dataclass, field
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
LONG_REF = "441b2399953c40d9313431620fa85159cce3f805"
LONG_PATHS = {
    "long main": "paper/general_formula/main.tex",
    "long supplement": "paper/general_formula/supplement.tex",
}
WINDOW = 160

# --- the TeX forms that are not numbers of the text ------------------------------------------

# every table maps a macro to the number of its brace arguments
# the pointers, labels, citations and file names, dropped with their arguments
POINTER_MACROS = {
    "label": 1,
    "ref": 1,
    "eqref": 1,
    "pageref": 1,
    "autoref": 1,
    "cref": 1,
    "Cref": 1,
    "nameref": 1,
    "vref": 1,
    "labelcref": 1,
    "cite": 1,
    "citep": 1,
    "citet": 1,
    "citealp": 1,
    "citealt": 1,
    "citeauthor": 1,
    "citeyear": 1,
    "citeyearpar": 1,
    "nocite": 1,
    "bibitem": 1,
    "tag": 1,
    "hyperlink": 2,
    "hypertarget": 2,
    "url": 1,
    "nolinkurl": 1,
    "path": 1,
    "input": 1,
    "include": 1,
    "bibliography": 1,
    "bibliographystyle": 1,
}
# the authors' identity and the layout, dropped with their arguments
LAYOUT_MACROS = {
    "author": 1,
    "affil": 1,
    "affiliation": 1,
    "orgdiv": 1,
    "orgname": 1,
    "orgaddress": 1,
    "street": 1,
    "city": 1,
    "postcode": 1,
    "state": 1,
    "country": 1,
    "email": 1,
    "date": 1,
    "orcid": 1,
    "orcidlink": 1,
    "pacs": 1,
    "vspace": 1,
    "hspace": 1,
    "setlength": 2,
    "addtolength": 2,
    "setcounter": 2,
    "addtocounter": 2,
    "stepcounter": 1,
    "numberwithin": 2,
    "linespread": 1,
    "setstretch": 1,
    "fontsize": 2,
    "includegraphics": 1,
    "graphicspath": 1,
    "captionsetup": 1,
    "geometry": 1,
    "hypersetup": 1,
    "setlist": 1,
    "rule": 2,
    "cline": 1,
    "enlargethispage": 1,
    "footnotemark": 0,
    "newcommand": 2,
    "renewcommand": 2,
    "providecommand": 2,
    "newtheorem": 2,
    "newenvironment": 3,
    "renewenvironment": 3,
    "theoremstyle": 1,
    "DeclareMathOperator": 2,
    "newcolumntype": 2,
    "newcounter": 1,
    "usepackage": 1,
    "documentclass": 1,
    "pagestyle": 1,
    "thispagestyle": 1,
    "pagenumbering": 1,
    "phantom": 1,
    "hphantom": 1,
    "vphantom": 1,
    "color": 1,
    "definecolor": 3,
}
# the macros whose last brace argument is text and stays; the other arguments are layout
KEEP_LAST_MACROS = {
    "href": 2,
    "hyperref": 1,
    "raisebox": 2,
    "scalebox": 2,
    "resizebox": 3,
    "parbox": 2,
    "makebox": 1,
    "framebox": 1,
    "multicolumn": 3,
    "multirow": 3,
    "textcolor": 2,
    "rotatebox": 2,
    "footnotetext": 1,
    "footnote": 1,
}
# the environments whose options are layout and dropped (a title option of a theorem-like
# environment is text and stays)
OPTION_ENVIRONMENTS = (
    "figure",
    "figure*",
    "table",
    "table*",
    "enumerate",
    "itemize",
    "description",
    "minipage",
    "wrapfigure",
    "longtable",
    "tabular",
    "tabular*",
    "tabularx",
    "tabulary",
    "array",
    "multicols",
)
# the environments whose brace arguments are layout (column specifications, widths, counts)
ARGUMENT_ENVIRONMENTS = {
    "tabular": 1,
    "tabular*": 2,
    "tabularx": 2,
    "tabulary": 2,
    "longtable": 1,
    "array": 1,
    "minipage": 1,
    "wrapfigure": 2,
    "multicols": 1,
    "thebibliography": 1,
}
UNITS = r"(?:pt|pc|in|bp|cm|mm|dd|cc|sp|ex|em|mu|px)(?![A-Za-z])"
LENGTHS = (
    r"\\(?:textwidth|linewidth|columnwidth|textheight|hsize|vsize|baselineskip|paperwidth"
    r"|paperheight|columnsep|parindent|z@|p@|fill|fil)"
)
DIMENSION = re.compile(rf"[-+]?(?:\d+\.?\d*|\.\d+)(?:{UNITS}|\s*{LENGTHS})")
HEX_NAME = re.compile(r"(?<![A-Za-z0-9])(?=[0-9a-f]*[a-f])(?=[0-9a-f]*\d)[0-9a-f]{7,40}(?![A-Za-z0-9])")
# a macro glued to digits is not a name: \tfrac12 is the fraction 1/2 and \sqrt2 the root of 2
MACRO_BEFORE_DIGITS = re.compile(r"\\(?!(?:d|t|s|nice|c)?frac\d)[A-Za-z@]+(?=\d)")
# a digit run glued to a letter is a name (Universe24, Rule3, M87, GW170817, J1738+0333)
GLUED_DIGITS = re.compile(r"(\\?)[A-Za-z@]+(\d+(?:[-+]\d+)?)")
POINTER_WORDS = (
    "Section|Sections|Sec|Secs|Eq|Eqs|Equation|Equations|Fig|Figs|Figure|Figures|Table|Tables"
    "|Theorem|Theorems|Proposition|Propositions|Lemma|Lemmas|Corollary|Assumption|Assumptions"
    "|Hypothesis|Hypotheses|Definition|Remark|Step|Steps|Case|Item|Items|Row|Rows|Column|Columns"
    "|Line|Lines|Postulate|Postulates|Derivation|Derivations|Chapter|Appendix|Footnote|Page|Pages"
)
POINTER_NUMBER = r"\(?\s*\d+(?:\.\d+)*\s*\)?"
POINTER = re.compile(
    rf"(?<![A-Za-z])(?:{POINTER_WORDS})\b\.?~?\s*{POINTER_NUMBER}"
    rf"(?:\s*(?:,|;|and|or|to|--|-)\s*{POINTER_NUMBER})*",
    re.I,
)
# a supplement pointer S.n, with the numbered line or row it may name in a parenthesis
SUPPLEMENT_POINTER = re.compile(r"(?<![A-Za-z])S\.~?\s?(\d+)(?:\s*\((?:row\s+)?\d+\))?")
SECTION_NUMBER = re.compile(
    r"(\\(?:part|chapter|section|subsection|subsubsection|paragraph|subparagraph)\*?\{\s*)"
    r"((?:S\.)?\d+(?:\.\d+)*\.?)"
)
COMMENT = re.compile(r"(?<!\\)%[^\n]*")

# --- the numbers -----------------------------------------------------------------------------

SIGN = r"[-+\u2212]?"  # a hyphen-minus, a plus or the Unicode minus sign
SPACING = r"(?:\s|\\[,;!:]|~|\\quad|\\qquad)*"
TIMES = r"(?:\\times|\\cdot|\u00d7)"  # \times, \cdot or the Unicode multiplication sign
# the alternatives in the order tried at one position: a power of ten with its mantissa, a
# scientific form, a fraction a / b (not after an exponent's caret), a thousands group, a decimal,
# an integer; then the fraction macros, braced or glued
NUMBER = re.compile(
    r"(?<![A-Za-z0-9.])(?:"
    rf"(?P<power>(?:(?P<mantissa>\d+(?:\.\d+)?){SPACING}{TIMES}{SPACING})?"
    rf"10\^(?:\{{\s*(?P<exponent>{SIGN}\s*\d+)\s*\}}|(?P<digit>{SIGN}\d))(?![0-9.]))"
    r"|(?P<scientific>(?P<smantissa>\d+(?:\.\d+)?)[eE](?P<sexponent>[-+]?\d+)(?![A-Za-z0-9.]))"
    r"|(?P<fraction>(?<!\^)(?<!\^\{)(?P<numerator>\d+(?:\.\d+)?)\s*/\s*"
    r"(?P<denominator>\d+(?:\.\d+)?)(?![A-Za-z0-9.]))"
    r"|(?P<thousands>\d{1,3}(?:(?:,|\{,\}|\\,|~)\d{3})+(?:\.\d+)?(?!\d))"
    r"|(?P<decimal>\d+\.\d+(?!\.?\d))"
    r"|(?P<integer>\d+(?!\.?\d))"
    r")"
    r"|(?P<fracmacro>\\(?:d|t|s|nice|c)?frac\s*\{\s*(?P<mnumerator>\d+(?:\.\d+)?)\s*\}\s*"
    r"\{\s*(?P<mdenominator>\d+(?:\.\d+)?)\s*\})"
    r"|(?P<fracglued>\\(?:d|t|s|nice|c)?frac(?P<gnumerator>\d)(?P<gdenominator>\d)(?![0-9.]))"
)


@dataclass
class Token:
    """One number of a text: where it stands, how it is written, its normalised form and the parts
    of a composed form (a mantissa and a power of ten, a numerator and a denominator)."""

    start: int
    end: int
    written: str
    normalised: str
    parts: tuple[str, ...] = ()


@dataclass
class Cleaned:
    """A text with every non-number blanked to spaces (the offsets kept) and the blanked tokens by
    the rule that blanked them."""

    text: str
    ignored: dict[str, list[str]] = field(default_factory=dict)

    def blank(self, start: int, end: int, rule: str) -> None:
        """Blank the span, keeping newlines so that every offset still names its line."""
        removed = self.text[start:end]
        if re.search(r"\d", removed):
            self.ignored.setdefault(rule, []).append(" ".join(removed.split())[:80])
        self.text = self.text[:start] + re.sub(r"[^\n]", " ", removed) + self.text[end:]


def group_end(text: str, start: int) -> int:
    """The index after the brace group opening at `start`, escapes skipped; the text's end when
    the group never closes."""
    depth = 0
    i = start
    while i < len(text):
        c = text[i]
        if c == "\\":
            i += 2
            continue
        if c == "{":
            depth += 1
        elif c == "}":
            depth -= 1
            if depth == 0:
                return i + 1
        i += 1
    return len(text)


def macro_span(text: str, start: int, braced: int) -> tuple[int, list[tuple[int, int]]]:
    """From the end of a macro's name, the end of its invocation (the optional arguments before and
    between its `braced` brace groups included) and the spans of those brace groups."""
    i = start
    groups: list[tuple[int, int]] = []
    options = 0
    while True:
        j = i
        while j < len(text) and text[j] in " \t":
            j += 1
        if j < len(text) and text[j] == "[" and (len(groups) < braced or (braced == 0 and not options)):
            close = text.find("]", j)
            if close < 0:
                break
            options += 1
            i = close + 1
            continue
        if j < len(text) and text[j] == "{" and len(groups) < braced:
            end = group_end(text, j)
            groups.append((j, end))
            i = end
            continue
        break
    return i, groups


def drop_macros(cleaned: Cleaned, macros: dict[str, int], rule: str, keep_last: bool) -> None:
    """Blank every invocation of the macros with their arguments; with `keep_last` the last brace
    group is text and stays."""
    pattern = re.compile(r"\\(" + "|".join(macros) + r")\*?(?![A-Za-z@])")
    position = 0
    while True:
        m = pattern.search(cleaned.text, position)
        if m is None:
            return
        end, groups = macro_span(cleaned.text, m.end(), macros[m.group(1)])
        if keep_last and groups:
            last_start, last_end = groups[-1]
            cleaned.blank(m.start(), last_start + 1, rule)
            cleaned.blank(last_end - 1, last_end, rule)
            position = last_start + 1
        else:
            cleaned.blank(m.start(), end, rule)
            position = end


def drop_environment_arguments(cleaned: Cleaned) -> None:
    """Blank the options of the list and float environments and the brace arguments of the
    environments whose arguments are column specifications, widths or counts."""
    pattern = re.compile(r"\\begin\{([A-Za-z*]+)\}")
    position = 0
    while True:
        m = pattern.search(cleaned.text, position)
        if m is None:
            return
        name = m.group(1)
        braced = ARGUMENT_ENVIRONMENTS.get(name, 0)
        if name in OPTION_ENVIRONMENTS or braced:
            end, _groups = macro_span(cleaned.text, m.end(), braced)
            cleaned.blank(m.end(), end, "environment arguments")
        position = m.end()


def clean(text: str) -> Cleaned:
    """The text with everything that is not a number of the text blanked, offsets kept."""
    cleaned = Cleaned(text)
    for m in COMMENT.finditer(text):
        cleaned.blank(m.start(), m.end(), "comments")
    begin = cleaned.text.find("\\begin{document}")
    if begin >= 0:
        cleaned.blank(0, begin, "preamble")
    end = cleaned.text.find("\\end{document}")
    if end >= 0:
        cleaned.blank(end, len(cleaned.text), "after the document")
    begin = cleaned.text.find("\\begin{thebibliography}")
    if begin >= 0:
        end = cleaned.text.find("\\end{thebibliography}", begin)
        cleaned.blank(begin, len(cleaned.text) if end < 0 else end, "bibliography")
    for m in re.finditer(r"\\def\s*\\[A-Za-z@]+", cleaned.text):
        end, _ = macro_span(cleaned.text, m.end(), 1)
        cleaned.blank(m.start(), end, "layout macros")
    for m in re.finditer(r"\\cmidrule(?:\([^)]*\))?\s*\{[^}]*\}", cleaned.text):
        cleaned.blank(m.start(), m.end(), "layout macros")
    drop_macros(cleaned, POINTER_MACROS, "pointer macros", keep_last=False)
    drop_macros(cleaned, LAYOUT_MACROS, "layout macros", keep_last=False)
    drop_macros(cleaned, KEEP_LAST_MACROS, "layout macros", keep_last=True)
    drop_environment_arguments(cleaned)
    for m in re.finditer(r"\\\\\s*\[[^\]]*\]", cleaned.text):
        cleaned.blank(m.start(), m.end(), "layout macros")
    for m in SECTION_NUMBER.finditer(cleaned.text):
        cleaned.blank(m.start(2), m.end(2), "section numbers")
    for m in DIMENSION.finditer(cleaned.text):
        cleaned.blank(m.start(), m.end(), "dimensions")
    for m in HEX_NAME.finditer(cleaned.text):
        cleaned.blank(m.start(), m.end(), "names")
    for m in MACRO_BEFORE_DIGITS.finditer(cleaned.text):
        cleaned.blank(m.start(), m.end(), "names")
    for m in GLUED_DIGITS.finditer(cleaned.text):
        if not m.group(1):
            cleaned.blank(m.start(2), m.end(2), "names")
    for m in SUPPLEMENT_POINTER.finditer(cleaned.text):
        cleaned.blank(m.start(), m.end(), "pointers")
    for m in POINTER.finditer(cleaned.text):
        cleaned.blank(m.start(), m.end(), "pointers")
    return cleaned


def plain(number: str) -> str:
    """An integer or a decimal in its one form: separators and spaces out, leading zeros out,
    the digits after the point as written."""
    digits = re.sub(r"\{,\}|\\,|[,~\s]", "", number)
    whole, point, rest = digits.partition(".")
    whole = str(int(whole)) if whole else "0"
    return whole + point + rest


def exponent(text: str) -> int:
    return int(re.sub(r"\s", "", text).replace("\u2212", "-"))


def tokens(text: str | Cleaned) -> list[Token]:
    """Every number of a text, in the order written, the layout cleaned away first."""
    cleaned = text if isinstance(text, Cleaned) else clean(text)
    found = []
    for m in NUMBER.finditer(cleaned.text):
        kind = m.lastgroup
        parts: tuple[str, ...] = ()
        if m.group("power"):
            mantissa = plain(m.group("mantissa")) if m.group("mantissa") else "1"
            power = exponent(m.group("exponent") or m.group("digit"))
            normalised = f"{mantissa}e{power}"
            parts = (mantissa, f"1e{power}") if m.group("mantissa") else ()
        elif m.group("scientific"):
            mantissa = plain(m.group("smantissa"))
            power = exponent(m.group("sexponent"))
            normalised = f"{mantissa}e{power}"
            parts = (mantissa, f"1e{power}")
        elif m.group("fraction") or m.group("fracmacro") or m.group("fracglued"):
            numerator = plain(m.group("numerator") or m.group("mnumerator") or m.group("gnumerator"))
            denominator = plain(
                m.group("denominator") or m.group("mdenominator") or m.group("gdenominator")
            )
            normalised = f"{numerator}/{denominator}"
            parts = (numerator, denominator)
        else:
            normalised = plain(m.group(kind or "integer"))
        found.append(Token(m.start(), m.end(), m.group(0), normalised, parts))
    return found


# --- the lines of a text ---------------------------------------------------------------------


class Lines:
    """The line of every offset of a text and the window of a line around a span."""

    def __init__(self, text: str) -> None:
        self.text = text
        self.starts = [0] + [m.end() for m in re.finditer(r"\n", text)]

    def number(self, offset: int) -> int:
        return bisect.bisect_right(self.starts, offset)

    def window(self, start: int, end: int) -> str:
        """The line holding the span, or its WINDOW characters around the span when it is longer."""
        line = self.number(start) - 1
        line_start = self.starts[line]
        line_end = self.starts[line + 1] - 1 if line + 1 < len(self.starts) else len(self.text)
        if line_end - line_start <= WINDOW:
            return self.text[line_start:line_end].strip()
        left = max(line_start, min(start - WINDOW // 3, line_end - WINDOW))
        right = min(line_end, left + WINDOW)
        return (
            ("..." if left > line_start else "")
            + self.text[left:right]
            + ("..." if right < line_end else "")
        )


# --- check 1: the number audit ---------------------------------------------------------------


@dataclass
class Miss:
    file: str
    line: int
    written: str
    normalised: str
    context: str


@dataclass
class Audit:
    distinct: int = 0
    found: int = 0
    by_parts: int = 0
    misses: list[Miss] = field(default_factory=list)
    parts: list[Miss] = field(default_factory=list)
    inventory: dict[str, dict[str, tuple[str, int]]] = field(default_factory=dict)
    ignored: dict[str, dict[str, list[str]]] = field(default_factory=dict)


def audit_numbers(short: dict[str, str], long: dict[str, str]) -> Audit:
    """Every number of the short texts against the long texts' numbers and their parts."""
    known: set[str] = set()
    for text in long.values():
        for token in tokens(text):
            known.add(token.normalised)
            known.update(token.parts)
    audit = Audit()
    distinct: dict[str, bool] = {}
    for name, text in short.items():
        lines = Lines(text)
        cleaned = clean(text)
        audit.inventory[name] = {}
        audit.ignored[name] = cleaned.ignored
        for token in tokens(cleaned):
            audit.inventory[name].setdefault(
                token.normalised, (token.written, lines.number(token.start))
            )
            if token.normalised in known:
                distinct[token.normalised] = True
                continue
            by_parts = bool(token.parts) and all(part in known for part in token.parts)
            distinct[token.normalised] = by_parts
            listing = audit.parts if by_parts else audit.misses
            line = lines.number(token.start)
            if not any(
                m.file == name and m.line == line and m.normalised == token.normalised for m in listing
            ):
                listing.append(
                    Miss(
                        name,
                        line,
                        token.written,
                        token.normalised,
                        lines.window(token.start, token.end),
                    )
                )
    audit.distinct = len(distinct)
    audit.found = sum(distinct.values())
    audit.by_parts = len({m.normalised for m in audit.parts})
    return audit


# --- check 2: the pointer check --------------------------------------------------------------


@dataclass
class Pointers:
    checked: int = 0
    unresolved: list[str] = field(default_factory=list)
    notes: list[str] = field(default_factory=list)


def supplement_numbering(supplement: str) -> tuple[set[int] | None, int, str]:
    """How the supplement numbers its S.n: the numbers its headings write, else the count of the
    environment whose counter prints S.n, else the count of its \\section commands; with the
    convention's description."""
    headings = [int(n) for n in re.findall(r"\\(?:section|subsection)\*?\{\s*S\.(\d+)", supplement)]
    if headings:
        return (
            set(headings),
            max(headings),
            f"the \\section*{{S.n ...}} headings of the supplement ({len(headings)} headings, "
            f"the highest S.{max(headings)})",
        )
    counter = re.search(
        r"\\renewcommand\{\\the([A-Za-z]+)\}\{S\.\\(?:arabic|Roman|roman)\{\1\}\}", supplement
    )
    if counter:
        name = counter.group(1)
        count = len(re.findall(r"\\begin\{" + name + r"\}", supplement))
        return (
            None,
            count,
            f"the {name} environments, numbered S.n by \\the{name} ({count} environments)",
        )
    count = len(re.findall(r"\\section\*?\{", supplement))
    return (
        None,
        count,
        f"the \\section commands of the supplement ({count} sections, starred ones counted)",
    )


def check_pointers(
    short: dict[str, str], supplement_name: str, aux_labels: set[str], bib_keys: set[str]
) -> Pointers:
    """Every \\ref family pointer, literal S.n pointer and citation of the short files resolved."""
    result = Pointers()
    texts = {name: COMMENT.sub("", text) for name, text in short.items()}
    labels = set(aux_labels)
    for text in texts.values():
        labels.update(re.findall(r"\\label\{([^}]*)\}", text))
    numbers, count, convention = supplement_numbering(texts[supplement_name])
    result.notes.append(f"the S.n pointers are resolved against {convention}")
    for name, text in texts.items():
        lines = Lines(text)
        for m in re.finditer(
            r"\\(ref|eqref|pageref|autoref|cref|Cref|nameref|vref|labelcref|hyperref)\*?"
            r"(?:\[([^\]]*)\])?\{([^}]*)\}",
            text,
        ):
            targets = [m.group(2)] if m.group(1) == "hyperref" and m.group(2) else m.group(3).split(",")
            for target in (t.strip() for t in targets):
                result.checked += 1
                if target not in labels:
                    result.unresolved.append(
                        f"UNRESOLVED {name}:{lines.number(m.start())} \\{m.group(1)}{{{target}}} has no label"
                    )
        for m in SUPPLEMENT_POINTER.finditer(text):
            n = int(m.group(1))
            result.checked += 1
            if n == 0 or n > count or (numbers is not None and n not in numbers):
                result.unresolved.append(
                    f"UNRESOLVED {name}:{lines.number(m.start())} the pointer S.{n} names a derivation "
                    f"the supplement has not (the highest is S.{count})"
                )
        cites: dict[str, int] = {}
        for m in re.finditer(
            r"\\(?:cite|citep|citet|citealp|citealt|citeauthor|citeyear|citeyearpar|nocite)\*?"
            r"(?:\[[^\]]*\]){0,2}\{([^}]*)\}",
            text,
        ):
            for key in (k.strip() for k in m.group(1).split(",") if k.strip()):
                cites.setdefault(key, lines.number(m.start()))
        bibitems = set(re.findall(r"\\bibitem(?:\[[^\]]*\])?\{([^}]*)\}", text))
        bibtex = re.search(r"\\bibliography\{([^}]*)\}", text)
        if cites and not bibitems and bibtex is not None and not bib_keys:
            result.notes.append(
                f"{name} cites {len(cites)} keys against the BibTeX file {bibtex.group(1)!r}, which was "
                "not given (--bib PATH): those keys are not checked"
            )
            continue
        for key, line in cites.items():
            result.checked += 1
            if key not in bibitems and key not in bib_keys:
                result.unresolved.append(
                    f"UNRESOLVED {name}:{line} \\cite{{{key}}} has no bibitem in this document"
                )
    return result


# --- check 3: the labels of the long main text's theorems and equations ----------------------


@dataclass
class LabelRow:
    label: str
    environment: str
    line: int
    in_main: bool
    in_supplement: bool

    @property
    def verdict(self) -> str:
        if self.in_main:
            return "kept in the main text"
        if self.in_supplement:
            return "moved to the supplement"
        return "dropped"


def guard_labels(long_main: str, short_main: str, short_supplement: str) -> list[LabelRow]:
    """Every label inside a theorem-like or equation environment of the long main text, with the
    short file that still carries it."""
    text = COMMENT.sub("", long_main)
    lines = Lines(text)
    environments = {"theorem", "proposition", "lemma", "corollary"}
    environments.update(re.findall(r"\\newtheorem\*?\{([A-Za-z]+)\}", text))
    environments.update(("equation", "align", "gather", "multline", "flalign", "alignat", "eqnarray"))
    rows = []
    for name in sorted(environments):
        pattern = re.compile(
            rf"\\begin\{{{re.escape(name)}\*?\}}(.*?)\\end\{{{re.escape(name)}\*?\}}", re.S
        )
        for block in pattern.finditer(text):
            for label in re.finditer(r"\\label\{([^}]*)\}", block.group(1)):
                key = label.group(1)
                rows.append(
                    LabelRow(
                        key,
                        name,
                        lines.number(block.start() + label.start()),
                        f"\\label{{{key}}}" in short_main,
                        f"\\label{{{key}}}" in short_supplement,
                    )
                )
    return sorted(rows, key=lambda row: row.line)


# --- the report -------------------------------------------------------------------------------


def table(rows: list[list[str]]) -> list[str]:
    """The rows as aligned columns."""
    widths = [max(len(row[i]) for row in rows) for i in range(len(rows[0]))]
    return ["  ".join(cell.ljust(widths[i]) for i, cell in enumerate(row)).rstrip() for row in rows]


def report(
    audit: Audit,
    pointers: Pointers,
    rows: list[LabelRow],
    sources: dict[str, str],
    verbose: bool,
) -> str:
    """The plain-text report of the three checks."""
    out = ["The short version's checker"]
    out.extend(f"  {name}: {source}" for name, source in sources.items())
    out += ["", "1. The number audit"]
    for miss in audit.misses:
        out.append(f"MISS {miss.file}:{miss.line} {miss.written} | {miss.normalised}")
        out.append(f"    {miss.context}")
    for part in audit.parts:
        out.append(
            f"PARTS {part.file}:{part.line} {part.written} | {part.normalised}"
            " (its parts are in the long version, the composed number is not)"
        )
        out.append(f"    {part.context}")
    out.append(
        f"distinct numbers in the short files: {audit.distinct}; found in the long version: {audit.found}"
        f" ({audit.by_parts} by their parts); misses: {len(audit.misses)}"
        f" ({audit.distinct - audit.found} distinct numbers)"
    )
    for name, ignored in audit.ignored.items():
        counts = ", ".join(f"{rule} {len(items)}" for rule, items in sorted(ignored.items()))
        out.append(f"ignored in {name} (tokens with digits that are not numbers of the text): {counts}")
    if verbose:
        for name, inventory in audit.inventory.items():
            out += [
                "",
                f"The numbers of {name} ({len(inventory)} distinct), normalised <- as written (line)",
            ]
            for normalised, (written, line) in sorted(inventory.items(), key=lambda kv: kv[1][1]):
                out.append(f"  {normalised} <- {written} ({line})")
        for name, ignored in audit.ignored.items():
            out += ["", f"The tokens ignored in {name}, by rule (up to eight examples each)"]
            for rule, items in sorted(ignored.items()):
                out.append(f"  {rule} ({len(items)}): " + " | ".join(items[:8]))
    out += ["", "2. The pointer check"]
    out.extend(f"  {note}" for note in pointers.notes)
    out.extend(pointers.unresolved)
    out.append(f"pointers checked: {pointers.checked}; unresolved: {len(pointers.unresolved)}")
    out += [
        "",
        "3. The labels of the long main text's theorems, propositions, assumptions and equations",
    ]
    if rows:
        header = ["label", "environment", "long main line", "short main", "short supplement", "verdict"]
        body = [
            [
                row.label,
                row.environment,
                str(row.line),
                "yes" if row.in_main else "no",
                "yes" if row.in_supplement else "no",
                row.verdict,
            ]
            for row in rows
        ]
        out.extend(table([header, *body]))
        kept = sum(row.in_main for row in rows)
        moved = sum(row.verdict == "moved to the supplement" for row in rows)
        out.append(
            f"labels: {len(rows)}; kept in the main text {kept}; moved to the supplement {moved}; "
            f"dropped {len(rows) - kept - moved} (information, not a failure)"
        )
    else:
        out.append("  no labelled theorem, proposition, assumption or equation in the long main text")
    passed = not audit.misses and not pointers.unresolved
    out += [
        "",
        f"Result: {'PASS' if passed else 'FAIL'} ({len(audit.misses)} misses, "
        f"{len(pointers.unresolved)} unresolved pointers)",
    ]
    return "\n".join(out)


# --- the files --------------------------------------------------------------------------------


def git_show(ref: str, path: str) -> str:
    """A file's text at a commit, read from the repository that holds this script."""
    result = subprocess.run(
        ["git", "show", f"{ref}:{path}"], cwd=ROOT, capture_output=True, encoding="utf-8", check=False
    )
    if result.returncode != 0:
        raise FileNotFoundError(f"git show {ref}:{path} failed: {result.stderr.strip()}")
    return result.stdout


def long_version(
    ref: str, main_path: str | None, supplement_path: str | None
) -> tuple[dict[str, str], dict[str, str]]:
    """The long version's two texts and where each was read from: the two paths when both are
    given, else git at the commit."""
    if main_path and supplement_path:
        paths = {"long main": main_path, "long supplement": supplement_path}
        return {n: Path(p).read_text(encoding="utf-8") for n, p in paths.items()}, dict(paths)
    return (
        {name: git_show(ref, path) for name, path in LONG_PATHS.items()},
        {name: f"{ref[:12]}:{path}" for name, path in LONG_PATHS.items()},
    )


def aux_labels(paths: list[str]) -> set[str]:
    """The labels the .aux files define (\\newlabel{name}{...})."""
    found: set[str] = set()
    for path in paths:
        found.update(re.findall(r"\\newlabel\{([^}]*)\}", Path(path).read_text(encoding="utf-8")))
    return found


def bib_keys(paths: list[str]) -> set[str]:
    """The entry keys of the BibTeX files."""
    found: set[str] = set()
    for path in paths:
        found.update(
            re.findall(r"@[A-Za-z]+\s*\{\s*([^,\s]+)\s*,", Path(path).read_text(encoding="utf-8"))
        )
    return found


def run(
    short: dict[str, str],
    long: dict[str, str],
    main_name: str,
    supplement_name: str,
    labels: set[str],
    keys: set[str],
) -> tuple[Audit, Pointers, list[LabelRow]]:
    """The three checks on the given texts."""
    audit = audit_numbers(short, long)
    pointers = check_pointers(short, supplement_name, labels, keys)
    rows = guard_labels(long["long main"], short[main_name], short[supplement_name])
    return audit, pointers, rows


def self_test(
    ref: str = LONG_REF,
    main_path: str | None = None,
    supplement_path: str | None = None,
    verbose: bool = False,
) -> tuple[Audit, Pointers, str]:
    """The long version against itself: the audit, the pointers and the report."""
    long, sources = long_version(ref, main_path, supplement_path)
    short = {"short main": long["long main"], "short supplement": long["long supplement"]}
    audit, pointers, rows = run(short, long, "short main", "short supplement", set(), set())
    sources.update(
        {
            "short main": "the long main (self-test)",
            "short supplement": "the long supplement (self-test)",
        }
    )
    return audit, pointers, report(audit, pointers, rows, sources, verbose)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="The short version's checker against the frozen long version."
    )
    parser.add_argument("--short-main", help="the short main text (.tex)")
    parser.add_argument("--short-supplement", help="the short supplement (.tex)")
    parser.add_argument("--long-ref", default=LONG_REF, help="the commit holding the long version")
    parser.add_argument("--long-main", help="the long main text read from a path instead of git")
    parser.add_argument("--long-supplement", help="the long supplement read from a path instead of git")
    parser.add_argument(
        "--xr-aux", action="append", default=[], help="an .aux file whose labels resolve pointers"
    )
    parser.add_argument(
        "--bib", action="append", default=[], help="a BibTeX file whose keys resolve citations"
    )
    parser.add_argument(
        "--verbose", action="store_true", help="print the inventory and the ignored tokens"
    )
    parser.add_argument("--self-test", action="store_true", help="run the long version against itself")
    args = parser.parse_args(argv)
    if bool(args.long_main) != bool(args.long_supplement):
        parser.error("--long-main and --long-supplement go together")
    if not args.self_test and not (args.short_main and args.short_supplement):
        parser.error("--short-main and --short-supplement are required (or --self-test)")
    try:
        if args.self_test:
            audit, pointers, text = self_test(
                args.long_ref, args.long_main, args.long_supplement, args.verbose
            )
        else:
            long, sources = long_version(args.long_ref, args.long_main, args.long_supplement)
            short = {
                "short main": Path(args.short_main).read_text(encoding="utf-8"),
                "short supplement": Path(args.short_supplement).read_text(encoding="utf-8"),
            }
            sources.update({"short main": args.short_main, "short supplement": args.short_supplement})
            audit, pointers, rows = run(
                short,
                long,
                "short main",
                "short supplement",
                aux_labels(args.xr_aux),
                bib_keys(args.bib),
            )
            text = report(audit, pointers, rows, sources, args.verbose)
    except (OSError, UnicodeDecodeError) as error:
        print(f"the checker could not read its files: {error}", file=sys.stderr)
        return 2
    print(text)
    return 0 if not audit.misses and not pointers.unresolved else 1


if __name__ == "__main__":
    sys.exit(main())
