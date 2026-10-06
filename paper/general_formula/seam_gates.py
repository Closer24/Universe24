"""The seam gates of the short version: four reports on the joins between the main text and Online Resource 1.

Every finding of the closing round that was not a number's arithmetic sat at a seam: a pointer that resolves to a
derivation which does not hold the sentence's number, a status word in the main stronger than the cited derivation's
Status line or a condition of that line dropped, a sentence of Section 2 stating an act of the law in words the law's
document does not carry, and a free noun or a symbol used before it is named. Each class is one report here, run over
both documents at a commit and printed as rows; the ratchets come after the one push that fixes the first list.

Usage: python seam_gates.py [--main main.tex] [--supplement supplement.tex] [--law ../../docs/ALGEBRA.md] [--quiet]
Exit 0 always: the gates are reports until their ratchets are set in tests/test_paper_gates.py.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

from claims_table import DERIVATION, KEY_WORDS, plain_marks, sentences

HERE = Path(__file__).resolve().parent
MAIN = HERE / "main.tex"
SUPPLEMENT = HERE / "supplement.tex"
LAW = HERE.parent.parent / "docs" / "ALGEBRA.md"

# 1. the pointer holds: the numbers and the subscripted symbols of a marked sentence against the cited derivation
NUMBER = re.compile(r"(?<![A-Za-z\\^_{])(\d+(?:\{,\}\d{3})*(?:\.\d+)?(?:\s*\\times\s*10\^\{-?\d+\})?)")
SUBSCRIPTED = re.compile(r"(\\[a-zA-Z]+|(?<![\\a-zA-Z])[A-Za-z])_(\{[^{}]*\}|[A-Za-z0-9])")
OPERATORS = (
    "\\sum",
    "\\prod",
    "\\int",
    "\\max",
    "\\min",
    "\\lim",
    "\\sup",
    "\\inf",
    "\\bigcup",
    "\\bigcap",
)
LONG_VERSION = re.compile(
    r"S\.\d+(?: \([^)]*\))?(?:,? ?\(?row \d+\)?)?(?: to \([^)]*\))? of the long version"
)
CITED = re.compile(r"S\.(\d+)((?:\s*\([a-z]\))*)")
SMALL = 10  # an integer below it is a count of things, not a number of the paper


def derivations(supplement: str) -> dict[int, tuple[str, str]]:
    """S.n to its title and its body."""
    return {n: (m.group(1), m.group(2)) for n, m in enumerate(DERIVATION.finditer(supplement), 1)}


def digits_of(token: str) -> str:
    """The printed digits of a number token, the thousands' separator and the exponent's dressing removed."""
    token = token.replace("{,}", "").replace(" ", "")
    token = re.sub(r"\\times10\^\{(-?\d+)\}", r"e\1", token)
    return token


def numbers_of(sentence: str) -> list[str]:
    """The numbers a sentence prints, the pointers, citations, references, years and small counts left out."""
    text = re.sub(r"\\(cite|ref|eqref|label)(\[[^\]]*\])?\{[^}]*\}", " ", sentence)
    text = re.sub(r"\bS\.\d+(?:\s*\([a-z]\))*", " ", text)
    text = re.sub(
        r"\b(Section|Sections|Theorem|Theorems|Eq\.|Eqs\.|Figure|Table|Lemma)~?\s*\(?\d+(\.\d+)*\)?",
        " ",
        text,
    )
    text = re.sub(r"\b(19|20)\d\d\b", " ", text)
    text = re.sub(r"\\num_b|\\den_b", " ", text)
    found: list[str] = []
    for token in NUMBER.findall(text):
        value = digits_of(token)
        if "." not in value and "e" not in value and int(value) < SMALL:
            continue
        if value not in found:
            found.append(value)
    return found


def symbols_of(sentence: str) -> list[str]:
    """The subscripted symbols a sentence names, as written."""
    found: list[str] = []
    for base, sub in SUBSCRIPTED.findall(sentence):
        if base in OPERATORS:
            continue
        symbol = base + "_" + sub
        if symbol not in found:
            found.append(symbol)
    return found


def holds(value: str, body: str) -> bool:
    """A number holds in a derivation when its printed digits open a number printed there (3.37 against 3.3713)."""
    body_values = {digits_of(t) for t in NUMBER.findall(body)}
    if value in body_values:
        return True
    if "e" in value:
        mantissa, exponent = value.split("e")
        return any(v.endswith("e" + exponent) and v.startswith(mantissa) for v in body_values)
    return any(v.startswith(value) and (len(v) == len(value) or "." in value) for v in body_values)


def gate_pointer_holds(main: str, supplement: str) -> list[str]:
    """The rows: a marked sentence's number or symbol in none of the derivations it cites; a marked sentence that
    cites a section and no derivation is listed after them, not failed."""
    rows: list[str] = []
    listed: list[str] = []
    bodies = derivations(supplement)
    for line, sentence in sentences(main):
        marks, _, inside = plain_marks(sentence)
        if not marks:
            continue
        cleaned = LONG_VERSION.sub(" ", sentence)
        cited = sorted({int(n) for n, _ in CITED.findall(cleaned)} & set(bodies))
        if not cited:
            if re.search(r"\\ref\{sec:", inside):
                listed.append(
                    f"main.tex:{line}: section-cited, no derivation to hold its numbers: {inside[:90]}"
                )
            continue
        held = " ".join(bodies[n][1] for n in cited)
        for value in numbers_of(sentence):
            if not holds(value, held):
                rows.append(
                    f"main.tex:{line}: the number {value} is in none of {', '.join('S.' + str(n) for n in cited)}: "
                    f"{inside[:80]}"
                )
        for symbol in symbols_of(re.sub(r"\\\(.*?\\\)|\(.*?\)", "", sentence)):
            if symbol not in held:
                rows.append(
                    f"main.tex:{line}: the symbol {symbol} is in none of {', '.join('S.' + str(n) for n in cited)}: "
                    f"{inside[:80]}"
                )
    return rows + listed


# 2. the status not stronger: the key's own order of its three claim words; the provenance words equal in kind; the
# Status line's conditions required in the citing sentence
RANK = {"theorem": 3, "derived": 2, "computed": 1}
PROVENANCE = tuple(w for w in KEY_WORDS if w not in RANK)
STATUS = re.compile(r"\\emph\{Status:\}(.*?)(?:\\end\{derivation\}|$)", re.S)
SEGMENT_LETTERS = re.compile(r"\(([a-z])\)(?:\s*(?:to|--|–|-)\s*\(([a-z])\))?")
CONDITION = re.compile(
    r"\b(under [^;,.()]+|to (?:the )?first order[^;,.()]*|to (?:the )?second order[^;,.()]*|at static paces"
    r"|at the small gap|at long wavelength|at the vacuum's paces|in form|an upper estimate"
    r"|conditional on [^;,.()]+)"
)


def status_line(body: str) -> str:
    found = STATUS.search(body)
    return re.sub(r"\\(fence|claimmark)\{([^}]*)\}", r"\2", found.group(1)).strip() if found else ""


def segments_of(status: str) -> list[tuple[set[str], str]]:
    """The Status line split at its semicolons, each segment with the letters it names."""
    segments: list[tuple[set[str], str]] = []
    for part in status.split(";"):
        letters: set[str] = set()
        for first, last in SEGMENT_LETTERS.findall(part):
            if last:
                letters.update(chr(c) for c in range(ord(first), ord(last) + 1))
            else:
                letters.add(first)
        segments.append((letters, part.strip()))
    return segments


def status_for(status: str, letters: set[str]) -> str:
    """The segments a mark cites by their letters, or the whole line when no segment is named."""
    if not letters:
        return status
    chosen = [text for named, text in segments_of(status) if named & letters]
    return "; ".join(chosen) if chosen else status


def words_of(text: str) -> list[str]:
    return [w for w in re.findall(r"[a-z]+", text.lower()) if w in KEY_WORDS]


def gate_status_rank(main: str, supplement: str) -> list[str]:
    """The rows: a mark's claim word above every cited Status line's; a provenance word of the mark absent from every
    cited Status line; a condition of a cited Status line absent from the sentence."""
    rows: list[str] = []
    bodies = derivations(supplement)
    for line, sentence in sentences(main):
        marks, _, inside = plain_marks(sentence)
        if not marks:
            continue
        cleaned = LONG_VERSION.sub(" ", inside)
        cited: list[tuple[int, set[str]]] = []
        for number, letters in CITED.findall(cleaned):
            if int(number) in bodies:
                cited.append((int(number), set(re.findall(r"\(([a-z])\)", letters))))
        if not cited:
            continue
        statuses = [(n, status_for(status_line(bodies[n][1]), letters)) for n, letters in cited]
        status_words = {w for _, s in statuses for w in words_of(s)}
        mark_rank = max((RANK[w] for w in marks if w in RANK), default=0)
        status_rank = max((RANK[w] for w in status_words if w in RANK), default=0)
        where = ", ".join(
            "S." + str(n) + ("".join(f" ({c})" for c in sorted(ls)) if ls else "") for n, ls in cited
        )
        if mark_rank > status_rank and status_rank:
            rows.append(
                f"main.tex:{line}: the mark says {', '.join(w for w in marks if w in RANK)} where {where} says "
                f"{', '.join(sorted(status_words & set(RANK))) or 'no claim word'}: {inside[:80]}"
            )
        for word in marks:
            if word in PROVENANCE and word not in status_words and status_words:
                rows.append(
                    f"main.tex:{line}: the mark's {word} is in no Status line of {where}: {inside[:80]}"
                )
        lowered = sentence.lower()
        for n, status in statuses:
            for condition in CONDITION.findall(status):
                head = " ".join(condition.lower().split()[:3])
                if head not in lowered:
                    rows.append(
                        f"main.tex:{line}: S.{n}'s condition '{condition.strip()}' is not in the sentence"
                    )
    return rows


# 3. the law: the sentences of the model's sections against the law's document, by their longest common run of words
LAW_SECTIONS = ("sec:lattice", "sec:rule3", "sec:paces", "sec:interval", "sec:click", "sec:spread")
LAW_WORDS = re.compile(
    r"\b(Rule3|the interval|the four acts|the click|the write|the read|the draw|the window|the report|the counting"
    r" rule|the credit|the emission|the dead time|the rate|the paces|the pace|the remainder|the beyond|the guard)\b"
)
RUN = 5  # the shortest run of words that counts as the law's line quoted


def section_bounds(main: str) -> dict[str, tuple[int, int]]:
    """A section label to the line span it heads, up to the next sectioning command."""
    lines = main.split("\n")
    heads = [
        (i + 1, m.group(1))
        for i, line in enumerate(lines)
        if (m := re.search(r"\\(?:sub)*section\{[^}]*\}\\label\{([^}]*)\}", line))
    ]
    bounds: dict[str, tuple[int, int]] = {}
    for index, (start, label) in enumerate(heads):
        end = heads[index + 1][0] - 1 if index + 1 < len(heads) else len(lines)
        bounds[label] = (start, end)
    return bounds


def word_list(text: str) -> list[str]:
    text = re.sub(r"\$[^$]*\$", " ", text)
    text = re.sub(r"\\[a-zA-Z]+(\[[^\]]*\])?(\{[^}]*\})?", " ", text)
    return re.findall(r"[a-z0-9']+", text.lower())


def runs_of(words: list[str], run: int) -> set[tuple[str, ...]]:
    return {tuple(words[i : i + run]) for i in range(len(words) - run + 1)}


def gate_law(main: str, law: str) -> list[str]:
    """The rows: a sentence of the model's sections that names an act of the law and shares no run of five words
    with the law's document."""
    rows: list[str] = []
    bounds = section_bounds(main)
    spans = [bounds[label] for label in LAW_SECTIONS if label in bounds]
    law_runs = runs_of(word_list(law), RUN)
    for line, sentence in sentences(main):
        if not any(start <= line <= end for start, end in spans):
            continue
        if not LAW_WORDS.search(sentence) or "&" in sentence or "\\qquad" in sentence:
            continue
        words = word_list(sentence)
        if len(words) < RUN:
            continue
        if not runs_of(words, RUN) & law_runs:
            rows.append(
                f"main.tex:{line}: no run of {RUN} words of the law's document: {sentence[:100]}"
            )
    return rows


# 4. the words: the free nouns on their word boundary; a Nomenclature symbol used in the main before its naming
FREE_NOUNS = re.compile(
    r"(?<!Node)\b(detector|detectors|instrument|instruments|emitter|emitters|absorber|absorbers|observer|observers"
    r"|measurer|measurers|grid|grids|site|sites)\b"
)
NOM = re.compile(r"\\nom\{\$([^$]*)\$\}\{([^{}]*(?:\{[^{}]*\}[^{}]*)*)\}")


def outside_citations(text: str) -> str:
    """The text with the bibliography and the cited titles blanked, where a free noun may be another author's."""
    end = text.find("\\begin{thebibliography}")
    text = text[:end] if end > 0 else text
    return re.sub(r"\\cite\[[^\]]*\]", " ", text)


def gate_words(main: str, supplement: str) -> list[str]:
    rows: list[str] = []
    for name, text in (("main.tex", main), ("supplement.tex", supplement)):
        body = outside_citations(text)
        for match in FREE_NOUNS.finditer(body):
            before = body[max(0, match.start() - 30) : match.start()]
            if re.search(r"\\texttt\{[^}]*$|\\label\{[^}]*$", before):
                continue
            line = body.count("\n", 0, match.start()) + 1
            rows.append(
                f"{name}:{line}: the free noun '{match.group(1)}': {body[max(0, match.start() - 40) : match.end() + 20]!r}"
            )
    for symbol, description in NOM.findall(supplement):
        bare = symbol.split(",")[0].strip()
        if len(bare) < 2 or "\\" not in bare and "_" not in bare:
            continue
        at = main.find(bare)
        if at < 0:
            continue
        line_start = main.rfind("\n", 0, at) + 1
        line_end = main.find("\n", at)
        first_line = main[line_start : line_end if line_end > 0 else len(main)].lower()
        gloss = [w for w in re.findall(r"[a-z]{4,}", description.lower())[:4]]
        if gloss and not any(w in first_line for w in gloss):
            line = main.count("\n", 0, at) + 1
            rows.append(f"main.tex:{line}: ${bare}$ first used without its name ({' '.join(gloss)})")
    return rows


def main_entry(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("--main", default=str(MAIN))
    parser.add_argument("--supplement", default=str(SUPPLEMENT))
    parser.add_argument("--law", default=str(LAW))
    parser.add_argument("--quiet", action="store_true", help="print the counts alone")
    args = parser.parse_args(argv)
    main_text = Path(args.main).read_text(encoding="utf-8")
    supplement = Path(args.supplement).read_text(encoding="utf-8")
    law = Path(args.law).read_text(encoding="utf-8")
    for name, rows in (
        ("the pointer holds", gate_pointer_holds(main_text, supplement)),
        ("the status not stronger", gate_status_rank(main_text, supplement)),
        ("the law's lines in Section 2", gate_law(main_text, law)),
        ("the words", gate_words(main_text, supplement)),
    ):
        print(f"{name}: {len(rows)} row{'s' if len(rows) != 1 else ''}")
        if not args.quiet:
            for row in rows:
                print("  " + row)
    return 0


if __name__ == "__main__":
    sys.exit(main_entry())
