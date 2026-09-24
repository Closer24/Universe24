"""Cut the paper's records out of the manuscript into the records file (the
owner's words of 2026-09-23: "48 pages", "there is only one paper", "start
it").

`cut(s)` takes the reordered manuscript text (before the references are
filtered) and returns `(paper, records)`: the nine blocks below leave the
paper whole and verbatim for `paper/general_formula/records.tex`, a source
file of the archive and not a document (it is not compiled and is cited from
the paper as \\cite{records}); each block is replaced in the paper by a
one-line pointer or by the sentence that introduced it, and the paper's
references to the blocks are rewritten to name the records file. The blocks:
the full confrontation record (its table, tab:nature), the check of the
roads (tab:roads), the reproduction appendix's paths and fingerprints with
the seven confirmations, the auxiliary proofs, the
hand-worked update, the conversion table (tab:conversion), the forcing
ledger (tab:ledger), the families table (tab:families) and the symbol
table. The summary table and the kept-words table stay in the paper. No claim, no number and
no count is cut; the count sentence stands in every place.
"""

from reorder import REGISTER_HEADING, ROADS_HEADING

BIB_START = "\\begin{thebibliography}"
PROOFS_HEADING = "\\section{Auxiliary proofs}\\label{app:proofs}"
TECHNICAL_HEADING = "\\section{Technical details}\\label{app:technical}"
CONFIRMATIONS_START = "\\paragraph{The seven confirmations.}"
REPRODUCTION_HEADING = "\\section{Reproduction}\\label{app:reproduction}"
ARCHIVE_SENTENCE = "The archived version cited at submission is the tag"
HANDWORKED_START = "\\paragraph{A hand-worked update.}"
CODE_HEADING = "\\paragraph{The code implements the law.}"
LONGTABLE_END = "\\end{longtable}}"
TABLE_START = "{\\scriptsize\\setlength{\\tabcolsep}{3pt}"
CONVERSION_LABEL = "\\caption{\\label{tab:conversion}"
LEDGER_LABEL = "\\caption{\\label{tab:ledger}"
FAMILIES_LABEL = "\\caption{\\label{tab:families}"
SYMBOLS_START = "\\paragraph{The symbols.} {\\footnotesize"

RECORDS = "the paper's records file \\cite{records}"

# The pointers left in the paper where a block stood.
POINTERS = {
    "reproduction": (
        "Every registered run's world file, its expectation written before the run, its source fingerprint "
        "and its record, the check scripts with their outputs, the figures' runs and the seven confirmations "
        "(each a run's clicks against the formula shown Inside, with its numbers) are listed in "
        + RECORDS
        + " and in the registers \\cite{register,replications}; the code and the worlds are the archive "
        "\\cite{zenodo}. "
    ),
    "symbols": (
        "\\paragraph{The symbols.} The symbol table, every letter with its kind and its name, is in "
        + RECORDS
        + "; every symbol is named at its first use in the text.\n\n"
    ),
    "handworked": (
        "\\paragraph{A hand-worked update.} One row's update worked by hand, interval by interval, "
        "is in " + RECORDS + "; the engine's realisation of Eq.~\\eqref{eq:map} as one pass per "
        "interval is the code \\cite{zenodo}.\n\n"
    ),
}

# The paper's references to what moved, the specific forms first, then the general.
REFERENCES = [
    (
        "Tables~\\ref{tab:conversion} and~\\ref{tab:nature}",
        "the conversion table and the full record \\cite{records}",
    ),
    (
        "the full record, Table~\\ref{tab:nature} of Appendix~\\ref{app:register}, keyed",
        "the full record \\cite{nature,records}, keyed",
    ),
    (
        "Table~\\ref{tab:conversion} names, row by row,",
        "The conversion table, in " + RECORDS + ", names, row by row,",
    ),
    ("Table~\\ref{tab:conversion} lists the map", "The conversion table \\cite{records} lists the map"),
    ("Table~\\ref{tab:conversion}'s (", "the conversion table's \\cite{records} ("),
    ("Table~\\ref{tab:conversion}", "the conversion table \\cite{records}"),
    (
        "Table~\\ref{tab:ledger} is the paper's spine:",
        "The forcing ledger, in " + RECORDS + ", is the paper's spine:",
    ),
    ("Table~\\ref{tab:ledger}", "the forcing ledger \\cite{records}"),
    ("Table~\\ref{tab:nature}", "the full record \\cite{nature,records}"),
    ("Table~\\ref{tab:families} (below) lists", "The families table, in " + RECORDS + ", lists"),
    ("Table~\\ref{tab:families}", "the families table \\cite{records}"),
    (
        "the symbol table is\nAppendix~\\ref{app:technical},",
        "the symbol table is\nin " + RECORDS + ",",
    ),
    ("Table~\\ref{tab:roads}", "the roads table \\cite{records}"),
    ("Appendix~\\ref{app:register}", RECORDS),
    ("Appendix~\\ref{app:families}", RECORDS),
    ("The proof is Appendix~\\ref{app:proofs}.", "The proof is in " + RECORDS + "."),
    ("proved in Appendix~\\ref{app:proofs}.", "proved in " + RECORDS + "."),
]


def _once(s: str, marker: str, name: str) -> int:
    n = s.count(marker)
    if n != 1:
        raise ValueError(f"records: the marker of {name} occurs {n} times, not once: {marker[:60]!r}")
    return s.index(marker)


def _cut_between(s: str, start: str, end: str, name: str) -> tuple[str, str]:
    """Cut from the start marker (inclusive) to the end marker (exclusive), the end the first after the start."""
    i = _once(s, start, name)
    j = s.index(end, i)
    return s[i:j], s[:i] + s[j:]


def cut_table(s: str, label: str, name: str) -> tuple[str, str]:
    """Cut one longtable whole, from its size group to the group's end."""
    i = _once(s, label, name)
    start = s.rindex(TABLE_START, 0, i)
    end = s.index(LONGTABLE_END, i) + len(LONGTABLE_END)
    return s[start:end], s[:start] + s[end:]


def cut(s: str) -> tuple[str, str]:
    """(the paper without the nine blocks, the records file's body)."""
    register, s = _cut_between(s, REGISTER_HEADING, ROADS_HEADING, "the register")
    roads, s = _cut_between(s, ROADS_HEADING, BIB_START, "the roads")
    # The reproduction appendix: its paths and fingerprints and the seven
    # confirmations to the records file; the archive's own sentences stay.
    i = _once(s, REPRODUCTION_HEADING, "the reproduction appendix") + len(REPRODUCTION_HEADING) + 2
    j = s.index(ARCHIVE_SENTENCE, i)
    reproduction, s = s[i:j], s[:i] + POINTERS["reproduction"] + s[j:]
    confirmations, s = _cut_between(s, CONFIRMATIONS_START, BIB_START, "the confirmations")
    proofs, s = _cut_between(s, PROOFS_HEADING, TECHNICAL_HEADING, "the proofs")
    handworked, s = _cut_between(s, HANDWORKED_START, CODE_HEADING, "the hand-worked update")
    s = s.replace(CODE_HEADING, POINTERS["handworked"] + CODE_HEADING, 1)
    conversion, s = cut_table(s, CONVERSION_LABEL, "the conversion table")
    ledger, s = cut_table(s, LEDGER_LABEL, "the ledger")
    families, s = cut_table(s, FAMILIES_LABEL, "the families table")
    i = _once(s, SYMBOLS_START, "the symbols")
    j = s.index(LONGTABLE_END, i) + len(LONGTABLE_END)
    symbols, s = s[i:j], s[:i] + POINTERS["symbols"] + s[j:]
    for old, new in REFERENCES:
        if old not in s:
            raise ValueError(f"records: the paper's reference {old!r} is not there to rewrite")
        s = s.replace(old, new)
    records = (
        register
        + "\n\n"
        + roads
        + "\n\n\\section{Reproduction: the runs, the fingerprints and the seven confirmations}\\label{rec:reproduction}\n\n"
        + reproduction
        + "\n\n"
        + confirmations
        + "\n\n"
        + proofs
        + "\n\\section{A hand-worked update}\\label{rec:handworked}\n\n"
        + handworked
        + "\n\n\\section{The conversion, Inside formula to Outside formula}\\label{rec:conversion}\n\n"
        + conversion
        + "\n\n\\section{The forcing ledger}\\label{rec:ledger}\n\n"
        + ledger
        + "\n\n\\section{The families as declared integers}\\label{rec:families}\n\n"
        + families
        + "\n\n\\section{The symbols}\\label{rec:symbols}\n\n"
        + symbols
    )
    return s, records


def strip_block(body: str) -> str:
    """The cuts of `cut`, applied to one text block where their markers are
    present, for the test that holds every reordered block verbatim."""
    if REPRODUCTION_HEADING in body and ARCHIVE_SENTENCE in body:
        i = body.index(REPRODUCTION_HEADING) + len(REPRODUCTION_HEADING) + 2
        j = body.index(ARCHIVE_SENTENCE, i)
        body = body[:i] + POINTERS["reproduction"] + body[j:]
    if CONFIRMATIONS_START in body and BIB_START in body:
        i, j = body.index(CONFIRMATIONS_START), body.index(BIB_START)
        body = body[:i] + body[j:]
    if PROOFS_HEADING in body and TECHNICAL_HEADING in body:
        i, j = body.index(PROOFS_HEADING), body.index(TECHNICAL_HEADING)
        body = body[:i] + body[j:]
    if HANDWORKED_START in body and CODE_HEADING in body:
        i, j = body.index(HANDWORKED_START), body.index(CODE_HEADING)
        body = body[:i] + POINTERS["handworked"] + body[j:]
    for label in (CONVERSION_LABEL, LEDGER_LABEL, FAMILIES_LABEL):
        if label in body:
            _, body = cut_table(body, label, label)
    if SYMBOLS_START in body:
        i = body.index(SYMBOLS_START)
        j = body.index(LONGTABLE_END, i) + len(LONGTABLE_END)
        body = body[:i] + POINTERS["symbols"] + body[j:]
    for old, new in REFERENCES:
        body = body.replace(old, new)
    return body


RECORDS_HEADER = """% The paper's records: the blocks cut from main.tex at 48 pages (the owner's
% words of 2026-09-23, "48 pages" and "there is only one paper"), kept verbatim
% from the same source by cut30/assemble.py (cut30/records.py); edit the parts,
% not this file. This is a source file of the archive, cited from the paper as
% \\cite{records}; it is not a document and is not compiled on its own: its
% references (\\ref, \\eqref, \\cite) are the paper's.
"""
