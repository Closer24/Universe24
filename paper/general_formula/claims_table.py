"""The paper's claims table, `paper/claims.md`, built from the paper's own text at every print (the method of
2026-10-04, #1538: the Boss's eight steps, the writer's counterexample sweep as the engine of steps 2 to 4 with the
advisor's four changes).

Every sentence of main.tex that carries a claim mark is one row: its place (the section's label and the line),
its marks and fence as printed, its kind, the source the sentence itself gives (a derivation of the supplement, a
script, a cited section of a document, a section of the paper), and the breaker: the smallest configuration that
could break it, written by hand in `paper/claims_breakers.json` and keyed by the sentence's opening words, so
that a sentence changed in the paper changes its row and a row's breaker survives a reprint. The kinds: (a)
derived from the law's line, with the line named; (b) computed by a named script, its output the number printed;
(c) read from a run at the frozen commit, labelled NodeReader or GameBoard; (d) nature's measurement with its
citation; (e) what the engine does, sourced to the engine's document and a function; a declaration, hypothesis,
assumption or inspiration mark is a row of its own kind, with no breaker. A row with no source is marked NO
SOURCE, a finding for the hands. The unmarked sentences carrying a strong word are listed as candidates, and
the supplement's derivations with their Status lines.

    python paper/general_formula/claims_table.py      writes paper/claims.md from main.tex and supplement.tex
"""

from __future__ import annotations

import json
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent
MAIN = HERE / "main.tex"
SUPPLEMENT = HERE / "supplement.tex"
BREAKERS = HERE.parent / "claims_breakers.json"
OUT = HERE.parent / "claims.md"

STRONG = re.compile(
    r"\b(exactly|exact|bound|bounded|conserved|is kept|keeps|fixed point|for every|for any|never|at every Node|independent of)\b"
)
NO_BREAK = re.compile(r"(S|Eq|Fig|Sec|Section|Table|\d|vs|al)\.$")


def sentences(text: str) -> list[tuple[int, str]]:
    """The sentences of the text with their line numbers: a sentence ends at '. ' outside mathematics."""
    found: list[tuple[int, str]] = []
    for number, line in enumerate(text.split("\n"), 1):
        in_math = False
        start = 0
        for index, char in enumerate(line):
            if char == "$":
                in_math = not in_math
            if (
                not in_math
                and char == "."
                and index + 1 < len(line)
                and line[index + 1] == " "
                and not NO_BREAK.search(line[start : index + 1])
            ):
                found.append((number, line[start : index + 1].strip()))
                start = index + 1
        rest = line[start:].strip()
        if rest:
            found.append((number, rest))
    return found


def places(text: str) -> dict[int, str]:
    """The label of the nearest section, subsection or paragraph before each line."""
    labels: dict[int, str] = {}
    current = "front matter"
    for number, line in enumerate(text.split("\n"), 1):
        section = re.search(r"\\(section|subsection)\{([^}]*)\}(\\label\{([^}]*)\})?", line)
        if section:
            current = section.group(4) or section.group(2)[:40]
        paragraph = re.search(r"\\paragraph\{([^}]*)\}", line)
        if paragraph:
            current = current.split(" / ")[0] + " / " + paragraph.group(1)[:50]
        labels[number] = current
    return labels


def sources(sentence: str) -> list[str]:
    """The pointers the sentence itself gives."""
    found: list[str] = []
    found += ["S." + n for n in re.findall(r"S\.(\d+)", sentence)]
    found += [
        "script " + s.replace("\\_", "_") for s in re.findall(r"\\texttt\{([^}]*\.py)\}", sentence)
    ]
    for document in ("algebra", "engine", "decisions"):
        found += [
            f"{document}: {s}" for s in re.findall(r"\\cite\[([^\]]*)\]\{" + document + r"\}", sentence)
        ]
    found += ["Sec " + s for s in re.findall(r"\\ref\{(sec:[^}]*)\}", sentence)]
    found += ["Eq " + s for s in re.findall(r"\\eqref\{(eq:[^}]*)\}", sentence)]
    distinct: list[str] = []
    for item in found:
        if item not in distinct:
            distinct.append(item)
    return distinct


def plain(sentence: str, length: int = 170) -> str:
    """The sentence for the table: the marks in brackets, the fence in angles, the TeX commands unwrapped."""
    text = re.sub(r"\\claimmark\{([a-z]*)\}", r"[\1]", sentence)
    text = re.sub(r"\\fence\{([A-Za-z]*)\}", r"<\1>", text)
    text = re.sub(r"\\(texttt|emph|textsc|textbf)\{([^}]*)\}", r"\2", text)
    text = text.replace("\\\\", " ").replace("|", "/")
    return text[:length] + "..." if len(text) > length else text


def key_of(sentence: str) -> str:
    """The row's key, the sentence's opening words without TeX, stable across reprints that leave them."""
    text = re.sub(r"\\(emph|texttt|textsc|textbf)\{([^}]*)\}", r"\2", sentence)
    text = re.sub(r"\\[a-zA-Z]+(\[[^\]]*\])?\{[^}]*\}", "", text)
    text = re.sub(r"[^A-Za-z0-9 ]", "", text)
    return " ".join(text.split())[:60].strip()


def kind_of(marks: list[str]) -> str:
    if "theorem" in marks or "derived" in marks:
        return "a"
    if "computed" in marks:
        return "b"
    if "experiment" in marks:
        return "d"
    return "declaration"


def build() -> str:
    main = MAIN.read_text(encoding="utf-8")
    supplement = SUPPLEMENT.read_text(encoding="utf-8")
    breakers: dict[str, dict[str, str]] = (
        json.loads(BREAKERS.read_text(encoding="utf-8")) if BREAKERS.exists() else {}
    )
    labels = places(main)
    rows = []
    for number, sentence in sentences(main):
        marks = re.findall(r"\\claimmark\{([a-z]*)\}", sentence)
        if not marks:
            continue
        fence = ",".join(re.findall(r"\\fence\{([A-Za-z]*)\}", sentence))
        key = key_of(sentence)
        breaker = breakers.get(key, {})
        rows.append(
            {
                "line": number,
                "place": labels.get(number, ""),
                "marks": ",".join(marks),
                "fence": fence,
                "kind": breaker.get("kind", kind_of(marks)),
                "source": "; ".join(sources(sentence)) or "NO SOURCE",
                "sentence": plain(sentence),
                "breaker": breaker.get("breaker", ""),
                "state": breaker.get("state", ""),
                "key": key,
            }
        )
    candidates = [
        (number, labels.get(number, ""), STRONG.search(sentence).group(0), plain(sentence))  # type: ignore[union-attr]
        for number, sentence in sentences(main)
        if "\\claimmark" not in sentence
        and STRONG.search(sentence)
        and not sentence.startswith(("%", "\\bibitem"))
        and len(sentence) > 40
    ]
    derivations = []
    for index, match in enumerate(
        re.finditer(r"\\begin\{derivation\}\[([^\]]*)\](.*?)\\end\{derivation\}", supplement, re.S), 1
    ):
        status = re.search(r"\\emph\{Status:\}\s*(.*?)(\\end|$)", match.group(2), re.S)
        text = (
            re.sub(r"\s+", " ", status.group(1)).strip() if status else "the status in the paper's row"
        )
        derivations.append(
            (
                index,
                supplement[: match.start()].count("\n") + 1,
                plain(match.group(1), 90),
                plain(text, 200),
            )
        )

    filled = sum(1 for row in rows if row["breaker"])
    unsourced = sum(1 for row in rows if row["source"] == "NO SOURCE" and row["kind"] in "abce")
    lines = [
        "# The paper's claims",
        "",
        "Built from `paper/general_formula/main.tex` and `supplement.tex` by `paper/general_formula/claims_table.py`"
        " at every print; the breaker column is written by hand in `paper/claims_breakers.json` and keyed by the"
        " sentence's opening words. The kinds: (a) derived from the law's line; (b) computed by a named script;"
        " (c) read from a run at the frozen commit; (d) nature's measurement with its citation; (e) what the engine"
        " does, sourced to the engine's document and a function; a declaration, hypothesis, assumption or"
        " inspiration is a row of its own kind. The breaker is the smallest configuration that could break the"
        " claim, tried inside the claim's stated condition and outside it: the strong word stays only where the"
        " claim holds inside and breaks outside (a fence nothing breaks outside is struck too). The breakers run in"
        " `tools/derivations/counterexamples.py`, the law's, which the paper's gate imports; a break is narrowed and"
        " never reworded quietly, a theorem's or derived mark's narrowing at the mathematician's second, a"
        " computed number's re-run or a run reading's label at one hand's line. The state column: `to write`,"
        " `green` (holds inside, breaks outside), `BROKE Rnnn` (the ledger's row).",
        "",
        f"Rows with a claim mark: {len(rows)}, {filled} with a breaker written; rows of a derived, computed, run or"
        f" engine kind without a source pointer: {unsourced}; candidate sentences with a strong word and no mark:"
        f" {len(candidates)}; derivations of the supplement: {len(derivations)}.",
        "",
        "## A. The marked claims of main.tex",
        "",
        "| # | line | place | marks | fence | kind | source the sentence gives | the sentence | the breaker | state |",
        "|---|---|---|---|---|---|---|---|---|---|",
    ]
    for index, row in enumerate(rows, 1):
        lines.append(
            f"| {index} | {row['line']} | {row['place']} | {row['marks']} | {row['fence']} | {row['kind']} |"
            f" {row['source']} | {row['sentence']} | {row['breaker']} | {row['state']} |"
        )
    lines += [
        "",
        "## B. Unmarked sentences with a strong word, candidates for a row of kind (a) or (e)",
        "",
        "| # | line | place | word | the sentence |",
        "|---|---|---|---|---|",
    ]
    for index, (number, place, word, sentence) in enumerate(candidates, 1):
        lines.append(f"| {index} | {number} | {place} | {word} | {sentence} |")
    lines += [
        "",
        "## C. The supplement's derivations and their Status lines",
        "",
        "| S | line | title | status |",
        "|---|---|---|---|",
    ]
    for index, number, title, status in derivations:
        lines.append(f"| S.{index} | {number} | {title} | {status} |")
    return "\n".join(lines) + "\n"


if __name__ == "__main__":
    OUT.write_text(build(), encoding="utf-8")
    print(OUT)
