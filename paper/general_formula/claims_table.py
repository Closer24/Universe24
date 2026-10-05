"""The paper's claims table, `paper/claims.md`, built from the paper's own text at every print (the method of
2026-10-04, #1538: the Boss's eight steps, the writer's counterexample sweep as the engine of steps 2 to 4 with the
advisor's four changes).

Every sentence of main.tex that carries a claim mark is one row: its place (the section's label and the line),
its marks and fence as printed, its kind, the source the sentence itself gives (a derivation of the supplement, a
script, a cited section of a document, a section of the paper), and the breaker: the smallest configuration that
could break it, written by hand in `paper/claims_breakers.json` and keyed by the sentence's opening words, so
that a sentence changed in the paper changes its row and a row's breaker survives a reprint. The kinds: (a)
derived from the law's line, with the line named; (b) computed by a named script, its output the number printed;
(c) read from a run at the frozen commit, labelled NodeDetector or lattice; (d) nature's measurement with its
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
KEY_WORDS = (
    "theorem",
    "derived",
    "computed",
    "assumption",
    "hypothesis",
    "experiment",
    "fitted",
    "inspiration",
    "calibration",
    "declaration",
    "definition",
    "untested",
)  # the key's eight words of Section 1 and the tables' four
PLAIN_MARK = re.compile(
    r"\\?\((" + "|".join(KEY_WORDS) + r")\b(?:[^()]|\([^()]*\))*\)"
)  # the short version's mark: a parenthesis opening with a key word, the fence after the first semicolon, then the pointers
FENCE_WORDS = ("lattice", "clicks")


def plain_marks(sentence: str) -> tuple[list[str], str, str]:
    """The short version's mark of a sentence: the key words of its last marking parenthesis, its fence and the
    parenthesis itself; the long version's \\claimmark macro is read beside it by the callers."""
    found = list(PLAIN_MARK.finditer(sentence))
    if not found:
        return [], "", ""
    inside = found[-1].group(0)
    words = [w for w in re.findall(r"[a-z]+", inside) if w in KEY_WORDS]
    marks: list[str] = []
    for word in words:
        if word not in marks:
            marks.append(word)
    fence = ",".join(w for w in FENCE_WORDS if re.search(r"\b" + w + r"\b", inside))
    return marks, fence, inside


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
    """The labels of the section, the subsection and the subsubsection each line stands in, joined by " > " from the
    outermost, so that a sentence answers to every level a table's "where" may name; a paragraph's title after
    " / "."""
    labels: dict[int, str] = {}
    stack = ["front matter"]
    paragraph = ""
    for number, line in enumerate(text.split("\n"), 1):
        section = re.search(
            r"\\(section|subsection|subsubsection)\*?\{([^}]*)\}(\\label\{([^}]*)\})?", line
        )
        if section:
            depth = {"section": 1, "subsection": 2, "subsubsection": 3}[section.group(1)]
            label = section.group(4) or section.group(2)[:40]
            stack = stack[: depth - 1] + [label] if len(stack) >= depth - 1 else [*stack, label]
            paragraph = ""
        title = re.search(r"\\paragraph\{([^}]*)\}", line)
        if title:
            paragraph = title.group(1)[:50]
        labels[number] = " > ".join(stack) + (" / " + paragraph if paragraph else "")
    return labels


def environments(text: str) -> dict[int, str]:
    """The key's word each line stands under by its environment: an assumption's text is marked assumption, a
    theorem's, a lemma's or a proposition's theorem, since the environment's name is the claim's mark."""
    marks: dict[int, str] = {}
    current = ""
    for number, line in enumerate(text.split("\n"), 1):
        begin = re.search(r"\\begin\{(assumption|theorem|lemma|proposition|corollary)\}", line)
        if begin:
            current = "assumption" if begin.group(1) == "assumption" else "theorem"
        if current:
            marks[number] = current
        if re.search(r"\\end\{(assumption|theorem|lemma|proposition|corollary)\}", line):
            current = ""
    return marks


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


TABLES = {
    "tab:claims": (1, 2, 3),
    "tab:results": (1, 2, None),
    "tab:clicks": (1, None, None),
    "tab:shared": (2, None, None),
    "tab:adds": (2, None, None),
}  # the status column, the fence column, the "where" column; the short version's labels and the long version's


def table_rows(text: str, supplement: str = "") -> list[dict[str, str]]:
    """The rows of the tables whose status column is a claim's kind (the claims, the formulas shared with nature and
    the formulas the paper adds, in the short version; the results, the clicks and the additions in the long);
    one row per table line between the rules. A table the main no longer holds is read from the supplement, where
    the short version keeps it whole (the claims list, push 2 of the short version)."""
    found: list[dict[str, str]] = []
    for label, (status_at, fence_at, where_at) in TABLES.items():
        text = main_text if (main_text := _text_holding(label, found_in=(text, supplement))) else ""
        start = text.find("\\label{" + label + "}")
        if start < 0:
            continue
        end = min(
            e
            for e in (
                text.find("\\end{longtable}", start),
                text.find("\\end{tabular}", start),
            )
            if e >= 0
        )
        foot = text.find("\\endfoot", start)
        head = foot + len("\\endfoot") if 0 <= foot < end else text.find("\\midrule", start)
        body = text[
            head:end
        ]  # a longtable's rows stand after its foot's definition, a tabular's after its rule
        first_line = text[:start].count("\n") + 1
        for offset, line in enumerate(body.split("\n")):
            if not line.rstrip().endswith("\\\\") or "&" not in line:
                continue
            cells = [cell.strip() for cell in line.rstrip()[:-2].split(" & ")]
            if len(cells) < 3:
                continue
            status = cells[status_at] if status_at < len(cells) else ""
            word = status.lower()
            kind = (
                "a"
                if word.startswith(("theorem", "derived"))
                else "b"
                if word.startswith("computed")
                else "d"
                if word.startswith("experiment")
                else "declaration"
            )
            found.append(
                {
                    "table": label,
                    "line": str(first_line + offset + body[: body.find(line)].count("\n") * 0),
                    "status": plain(status, 90),
                    "fence": plain(cells[fence_at], 30)
                    if fence_at is not None and fence_at < len(cells)
                    else "",
                    "kind": kind,
                    "text": plain(cells[0], 150),
                    "where": cells[where_at] if where_at is not None and where_at < len(cells) else "",
                    "key": label + ": " + key_of(cells[0]),
                }
            )
    return found


def _text_holding(label: str, found_in: tuple[str, ...]) -> str:
    """The first of the texts that holds the table's label, the main before the supplement."""
    for text in found_in:
        if "\\label{" + label + "}" in text:
            return text
    return ""


MARK_LIKE = re.compile(
    r"\(([a-z]+)[^()]*(?:;\s*(?:lattice|clicks)\b|\bS\.\d+)[^()]*\)"
)  # a parenthesis shaped like a mark, a fence or a derivation's pointer inside it, whatever its first word


def marks_outside_the_key(main: str) -> list[str]:
    """The plain marks whose first word is not the key's (the writer's gate 1 note of 2026-10-05): a parenthesis
    that carries a fence or an S.n pointer and opens with a word outside KEY_WORDS is a mark the reader would pass
    over in silence, so it is printed as a miss with its line and its word."""
    misses: list[str] = []
    for number, sentence in sentences(main):
        if sentence.startswith(("%", "\\bibitem")):
            continue
        for match in MARK_LIKE.finditer(sentence):
            if match.group(1) not in KEY_WORDS and match.group(1) not in ("the", "a", "an", "see", "cf"):
                misses.append(
                    f"line {number}: a mark outside the key, '{match.group(1)}': {match.group(0)[:70]}"
                )
    return misses


def misattached_breakers(supplement: str, breakers: dict[str, dict[str, str]]) -> list[str]:
    """The breakers keyed to a derivation by its number must name that derivation (the "derivation" field, the
    title's opening words written at the re-key of 2026-10-05): after a renumbering of the supplement a key that
    names another derivation's title is a silent reattachment, printed as a miss (the audit's ask, #2021)."""
    titles = [plain(match.group(1), 120) for match in DERIVATION.finditer(supplement)]
    misses: list[str] = []
    for key, row in breakers.items():
        if not key.startswith("S.") or "derivation" not in row:
            continue
        index = int(key[2:])
        if index > len(titles):
            misses.append(f"{key}: no such derivation in the supplement ({row['derivation'][:50]})")
        elif titles[index - 1][:40] != row["derivation"][:40]:
            misses.append(
                f"{key}: keyed to '{row['derivation'][:40]}' but the derivation is '{titles[index - 1][:40]}'"
            )
    return misses


def unmatched_rows(main: str, supplement: str = "") -> list[str]:
    """The gate of the claims table's move into the supplement (the advisor's word of 2026-10-05, 5996437774 (C)):
    every row of the claims table has a marked sentence in the main at the row's "where" (a section the sentence
    stands in, at any level) carrying the row's first status word, and, where the row names a derivation S.n, a
    marked sentence at that place names one of them; a sentence inside an assumption or theorem environment is
    marked by the environment. The unmatched rows are the misses, printed with the row's opening words."""
    labels = places(main)
    under = environments(main)
    marked: list[tuple[set[str], set[str], list[str]]] = []
    for number, sentence in sentences(main):
        if sentence.startswith(("%", "\\bibitem")):
            continue
        marks, _, _ = plain_marks(sentence)
        marks += re.findall(r"\\claimmark\{([a-z]*)\}", sentence)
        if number in under:
            marks.append(under[number])
        if not marks:
            continue
        here = set(labels.get(number, "").split(" / ")[0].split(" > "))
        marked.append((here, set(re.findall(r"S\.(\d+)", sentence)), marks))
    misses: list[str] = []
    for row in table_rows(main, supplement):
        if row["table"] != "tab:claims":
            continue
        sections = set(re.findall(r"\\ref\{(sec:[^}]*)\}", row["where"]))
        derivations = set(re.findall(r"S\.(\d+)", row["where"]))
        words = [w for w in re.findall(r"[a-z]+", row["status"].lower()) if w in KEY_WORDS]
        at_place = [
            (pointers, marks) for here, pointers, marks in marked if not sections or here & sections
        ]
        word_found = any(not words or words[0] in marks for _, marks in at_place)
        pointer_found = not derivations or any(pointers & derivations for pointers, _ in at_place)
        if not (word_found and pointer_found):
            why = (
                "no sentence marked " + (words[0] if words else "at all")
                if not word_found
                else "no S.n of the row"
            )
            misses.append(
                f"Table 1's row without a marked sentence at its place ({why}): {row['text'][:80]}"
            )
    return misses


DERIVATION = re.compile(r"\\begin\{derivation\}\[([^\]]*)\](.*?)\\end\{derivation\}", re.S)
INPUTS = re.compile(r"\\emph\{Inputs:\}(.*?)\\emph\{Steps:\}", re.S)
# the cycles of the Inputs graph known tonight, each named until its fix prints; the set may only shrink (the breakers'
# RED_ROWS rule): S.1 and S.63 (the budget clause borrowed forward; S.21 and S.22 ride in through S.22's body, which has
# no Inputs line), S.40 and S.51 (the parts' amplitudes borrowed forward; S.51 has no Inputs line)
KNOWN_CYCLES: frozenset[tuple[int, ...]] = frozenset({(1, 21, 22, 53), (38, 47)})
# a derivation of the long version at the tag paper-long-v1.1 that the short supplement does not carry is cited
# "S.n of the long version"; such a mention names no derivation of this supplement
LONG_VERSION_CITATION = re.compile(
    r"S\.\d+(?: \([^)]*\))?(?:(?: to \([^)]*\))|(?:,? ?\(?row \d+\)?))? of the long version"
)


def inputs_graph(supplement: str) -> dict[int, set[int]]:
    """S.i to the set of S.m its Inputs line names; where a derivation has no Inputs line, the mentions of its body."""
    graph: dict[int, set[int]] = {}
    for number, match in enumerate(DERIVATION.finditer(supplement), 1):
        body = match.group(2)
        inputs = LONG_VERSION_CITATION.sub("", " ".join(INPUTS.findall(body)) or body)
        graph[number] = {int(x) for x in re.findall(r"S\.(\d+)", inputs)} - {number}
    return {i: {m for m in rests if m in graph} for i, rests in graph.items()}


def cycles(graph: dict[int, set[int]]) -> list[tuple[int, ...]]:
    """The strongly connected components of two or more derivations (Tarjan), each sorted."""
    index: dict[int, int] = {}
    low: dict[int, int] = {}
    stack: list[int] = []
    on_stack: set[int] = set()
    found: list[tuple[int, ...]] = []
    counter = [0]

    def visit(node: int) -> None:
        index[node] = low[node] = counter[0]
        counter[0] += 1
        stack.append(node)
        on_stack.add(node)
        for other in graph.get(node, ()):
            if other not in index:
                visit(other)
                low[node] = min(low[node], low[other])
            elif other in on_stack:
                low[node] = min(low[node], index[other])
        if low[node] == index[node]:
            component = []
            while True:
                top = stack.pop()
                on_stack.discard(top)
                component.append(top)
                if top == node:
                    break
            if len(component) > 1:
                found.append(tuple(sorted(component)))

    for node in graph:
        if node not in index:
            visit(node)
    return sorted(found)


def gate_inputs_graph(supplement: str) -> list[str]:
    """The misses: every cycle of the derivations' Inputs graph not named in KNOWN_CYCLES."""
    return [
        "a cycle among the derivations' Inputs lines: " + " and ".join(f"S.{n}" for n in component)
        for component in cycles(inputs_graph(supplement))
        if component not in KNOWN_CYCLES
    ]


def build() -> str:
    main = MAIN.read_text(encoding="utf-8")
    supplement = SUPPLEMENT.read_text(encoding="utf-8")
    breakers: dict[str, dict[str, str]] = (
        json.loads(BREAKERS.read_text(encoding="utf-8")) if BREAKERS.exists() else {}
    )
    labels = places(main)
    rows = []
    for number, sentence in sentences(main):
        if sentence.startswith(("%", "\\bibitem")):
            continue
        marks = re.findall(r"\\claimmark\{([a-z]*)\}", sentence)
        fence = ",".join(re.findall(r"\\fence\{([A-Za-z]*)\}", sentence))
        if not marks:
            marks, fence, _ = plain_marks(sentence)
        if not marks:
            continue
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
        (
            number,
            labels.get(number, ""),
            STRONG.search(sentence).group(0),
            plain(sentence),
        )  # type: ignore[union-attr]
        for number, sentence in sentences(main)
        if "\\claimmark" not in sentence
        and not PLAIN_MARK.search(sentence)
        and STRONG.search(sentence)
        and not sentence.startswith(("%", "\\bibitem"))
        and len(sentence) > 40
    ]
    derivations = []
    for index, match in enumerate(
        re.finditer(
            r"\\begin\{derivation\}\[([^\]]*)\](.*?)\\end\{derivation\}",
            supplement,
            re.S,
        ),
        1,
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

    tables = table_rows(main, supplement)
    misses = unmatched_rows(main, supplement)
    outside = marks_outside_the_key(main)
    misattached = misattached_breakers(supplement, breakers)
    long_keys = sorted(key for key in breakers if key.startswith("long:"))
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
        " `green` (holds inside, breaks outside), `BROKE Rnnn` (the ledger's row). One rule stands over every row of"
        " kind (e), the owner's word of 2026-10-04: every act of the engine on a Node's levels is Rule3's one line or"
        " the division act with the half, as the law has them; logic found at a Node that is not of Rule3's form is a"
        " red row by itself and a finding shouted on the reviewer's ledger, whatever the sentence it stands under.",
        "",
        f"Rows with a claim mark: {len(rows)}, {filled} with a breaker written; rows of a derived, computed, run or"
        f" engine kind without a source pointer: {unsourced}; candidate sentences with a strong word and no mark:"
        f" {len(candidates)}; rows of the tables: {len(tables)}; rows of Table 1 without a marked sentence:"
        f" {len(misses)}; marks outside the key: {len(outside)}; breakers keyed to another derivation:"
        f" {len(misattached)}; breakers keyed to the long version at the tag: {len(long_keys)}; derivations of the"
        f" supplement: {len(derivations)}.",
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
    marked = {row["key"] for row in rows}
    named = [
        (number, labels.get(number, ""), key_of(sentence), plain(sentence))
        for number, sentence in sentences(main)
        if key_of(sentence) in breakers and key_of(sentence) not in marked
    ]
    lines += [
        "",
        "## E. Unmarked sentences named by hand as claims (the engine's own rule among them)",
        "",
        "| # | line | place | kind | the sentence | the breaker | state |",
        "|---|---|---|---|---|---|---|",
    ]
    for index, (number, place, key, sentence) in enumerate(named, 1):
        breaker = breakers[key]
        lines.append(
            f"| {index} | {number} | {place} | {breaker.get('kind', '')} | {sentence} | {breaker.get('breaker', '')} |"
            f" {breaker.get('state', '')} |"
        )
    lines += [
        "",
        "## D. The tables' rows, the status column their kind; the rows of Table 1 without a marked sentence first",
        "",
        *[f"- {miss}" for miss in misses],
        *[f"- {miss}" for miss in outside],
        *[f"- {miss}" for miss in misattached],
        "",
        "| # | table | status | fence | kind | the row | the breaker | state |",
        "|---|---|---|---|---|---|---|---|",
    ]
    for index, row in enumerate(tables, 1):
        breaker = breakers.get(row["key"], {})
        lines.append(
            f"| {index} | {row['table']} | {row['status']} | {row['fence']} | {breaker.get('kind', row['kind'])} |"
            f" {row['text']} | {breaker.get('breaker', '')} | {breaker.get('state', '')} |"
        )
    lines += [
        "",
        "## F. Breakers keyed to the long version at the tag (`long:`), their sentence or row not in the short version",
        "",
        "| key | kind | the breaker | state |",
        "|---|---|---|---|",
        *[
            f"| {key} | {breakers[key].get('kind', '')} | {breakers[key].get('breaker', '')[:120]} |"
            f" {breakers[key].get('state', '')} |"
            for key in long_keys
        ],
        "",
        "## C. The supplement's derivations and their Status lines (the key `S.n`)",
        "",
        "| S | line | title | status | kind | the breaker | state |",
        "|---|---|---|---|---|---|---|",
    ]
    for index, number, title, status in derivations:
        breaker = breakers.get(f"S.{index}", {})
        lines.append(
            f"| S.{index} | {number} | {title} | {status} | {breaker.get('kind', '')} |"
            f" {breaker.get('breaker', '')} | {breaker.get('state', '')} |"
        )
    return "\n".join(lines) + "\n"


if __name__ == "__main__":
    OUT.write_text(build(), encoding="utf-8")
    print(OUT)
