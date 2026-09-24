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

import click
import law
import route
from reorder import REGISTER_HEADING, ROADS_HEADING

BIB_START = "\\begin{thebibliography}"
PROOFS_HEADING = "\\section{Auxiliary proofs}\\label{app:proofs}"
TECHNICAL_HEADING = "\\section{Technical details}\\label{app:technical}"
CONFIRMATIONS_START = "\\paragraph{The seven confirmations.}"
REPRODUCTION_HEADING = "\\section{Reproduction}\\label{app:reproduction}"
ARCHIVE_SENTENCE = "The archived version cited at submission is the tag"
HANDWORKED_START = "\\paragraph{A hand-worked update.}"
CODE_HEADING = "\\paragraph{The code implements the law.}"
# The law as the engine ran it before 2026-09-23 (the rows that hop): the whole
# section to the records file, cut30/law.py in its place, its ledger paragraph kept.
OLDLAW_START = "\\section{The GameBoard: the way the algebra is computed with}\\label{sec:gameboard}"
OLDLAW_END = "\\section{How the algebra was reached: from the GameBoard to the group}\\label{sec:route}"
LEDGER_START = "\\paragraph{The ledger.}"
LAW_BLOCK_START = "\\paragraph{The GameBoard as a system of information transfer.}"
# The road as the paper carried it before the algebra document: the two direction
# tables, the simulator's part and the old dictionary to the records file;
# cut30/route.py (ALGEBRA.md chapter 7) before the paragraph that stays.
FORWARD_START = "\\paragraph{From the physics to the mathematics: the postulates and what each forces.}"
OPERATIONS_START = "\\paragraph{From the operations to the group.}"
SIMULATOR_START = "\\paragraph{How the simulator led to the results.}"
OLDROAD_START = "\\paragraph{The road from the cells to the algebra.}"
DATED_START = "\\paragraph{The transition from ordinary physics to the algebra, dated.}"
# The readings of the engine before 2026-09-23 quoted as support, the old push's
# derivations and the delay field: to the records file (record 1459; ALGEBRA.md 2.11).
DETECTOR_START = "\\paragraph{What a detector measures.}"
FORCES_HEADING = "\\subsection{Conservation, the flux and the forces}\\label{sec:forces}"
OPERATIONS_PAR = "\\paragraph{The operations.}"
GAUSS_START = "\\paragraph{Gauss's law, exact.}"
SHELL_START = "\\paragraph{The inverse square as a shell mean.}"
DELAY_HEADING = "\\subsection{The delay field: the retarded potential, Poisson's equation and the clock}\\label{sec:delay}"
NEW_DELAY_HEADING = "\\subsection{Light past a held mass: the time part alone}\\label{sec:delay}"
LIGHT_START = "\\paragraph{Light: the time part alone, no optical metric.}"
REGISTERED_START = "\\paragraph{Against the registered integers.}"
INTERFERENCE_START = "\\paragraph{Interference, by the formulas alone.}"
# The click as the beam law defined it (the layer, the ladder, the lemma): to the
# records file; cut30/click.py (one click, the detector law's form) in its place.
OLDCLICK_START = "\\begin{definition}[The click]\\label{def:click}"
OLDCLICK_END = "\\end{lemma}\n"
# the beam law's flight table (S1 of the physicist's answers, 2026-09-24): the proof of
# the pace proposition and its ground go to the records file as history.
FLIGHT_PROOF_START = "\\begin{proof}\n$S_1^2 = (|D_x| + |D_y| + |D_z|)^2"
FLIGHT_PROOF_END = "\\end{proof}\n"
FLIGHT_GROUND_START = "The number is the bound of the Courant condition for the wave equation"
FLIGHT_GROUND_END = "and claims no novelty for the number. "
# the design's gate scripts (Section 6, "The code as the law's runtime"): to the records
# file with a one-sentence pointer (commit 50, the page count, the pointer rule).
CODE_RUNTIME_START = "\\paragraph{The code as the law's runtime.}"
CODE_RUNTIME_END = "\\paragraph{The ledger.}"
CODE_RUNTIME_POINTER = (
    "\\paragraph{The code as the law's runtime.} Every registered world is run from its world "
    "file with its pin written before the run and its source fingerprint "
    "(Appendix~\\ref{app:reproduction}); the books balance at every interval in every run; the "
    "design's scripts that gate the code, each printing its record beside the design and none an "
    "engine run, are listed in the records file \\cite{records}.\n\n"
)
# the beam law's weight rule of its rows 13 and 14 (the limitations paragraph): to the
# records file with a pointer (commit 50, the page count; the rows are not in the table).
WEIGHT_START = "The weight rule, stated once:"
WEIGHT_END = "is the declared input and not a result. "
WEIGHT_POINTER = (
    "The beam law's weight rule for its rows 13 and 14 ($\\gamma_{\\mathrm{PPN}}$, the declared "
    "space-curvature coefficient) is in the records file \\cite{records}, history. "
)
# the delay paragraph's head (the beam law's bending by the time part alone, history):
# to the records file with a pointer (commit 53, the page count, the pointer rule).
DELAY_HEAD_END = "\\subsection{Measurement and the quadratic form}"
DELAY_HEAD_POINTER = (
    "\\paragraph{Light: the time part alone, no optical metric.} The law at head bends a light "
    "row past a held mass by the time part alone, half of nature's, a reading of the engine of "
    "2026-09-22, history, NOT PREDICTED under the law as it stands; its readings, the ring's run "
    "and the delay's chain are in the records file \\cite{records} (row 13, history).\n\n"
)
# "The road to each, and the check that nothing was derived from them" (Section 7):
# to the records file with a pointer (commit 56, the page count, the pointer rule).
ROAD_START = "\\paragraph{The road to each, and the check that nothing was derived from them.}"
ROAD_END = "\\section{The comparison with nature"
ROAD_POINTER = (
    "\\paragraph{The road to each, and the check that nothing was derived from them.} The three "
    "roads are the one chain of Section~\\ref{sec:click}, each from the Inside step, the six verbs "
    "and the hypotheses named where they enter; the road to each formula and the check that no "
    "formula of nature was put in are in the records file \\cite{records}.\n\n"
)
FLIGHT_POINTER = (
    "The proof (Cauchy--Schwarz against $(1, 1, 1)$), the Courant and lattice Boltzmann "
    "comparisons and the ground of the bound are in the records file \\cite{records}, history.\n"
)


HISTORY_START = "\\paragraph{History: the beam law's flight table, the runtime before 3a9a7109.}"
HISTORY_END = "\\begin{proposition}[The pace]\\label{prop:pace}"
HISTORY_POINTER = (
    "\\paragraph{History.} The beam law's flight table, the runtime before 3a9a7109 (two rules, one Link per "
    "interval and the digital line of a direction, the octahedron of the six neighbours the causal front, the ground "
    "of Proposition~\\ref{prop:pace}), is in the records file \\cite{records}, history: under the law as it stands "
    "light is the record kind $[1, 1]$ whose band disperses at $k^2$ (row A2), and $c$ Outside is a bound "
    "(Theorem~\\ref{th:discreteness}).\n"
)
SIXOPS_START = "\\paragraph{The six operations as the engine runs them.}"
SIXOPS_END = "\\paragraph{The three tests, rule by rule.}"
SIXOPS_POINTER = (
    "\\paragraph{The six operations as the engine runs them.} The order of the six verbs within one interval, one "
    "line each in symbols \\cite[2.1 to 2.6, 2.11]{algebra}, and what is not one of them (a root of the state at run "
    "time, a float, a true division, a draw) are in the records file \\cite{records}.\n\n"
)


def cut_flight(s: str) -> tuple[str, str]:
    """The flight table's proof and its ground out of the paper, kept whole."""
    i = _once(s, FLIGHT_PROOF_START, "the flight proof")
    j = s.index(FLIGHT_PROOF_END, i) + len(FLIGHT_PROOF_END)
    proof, s = s[i:j], s[:i] + FLIGHT_POINTER + s[j:]
    i = _once(s, FLIGHT_GROUND_START, "the flight ground")
    j = s.index(FLIGHT_GROUND_END, i) + len(FLIGHT_GROUND_END)
    ground, s = s[i:j], s[:i] + s[j:]
    return s, proof + "\n\n" + ground + "\n"


# The three rows of the earlier beam law (the perihelion, the supernova diagram, the
# atom): out of the text entirely, whole in the records file (the owner's word of
# 2026-09-24, 03:30Z, through the Boss); the families' pointer sentence stays.
FAIL_CUTS = (
    (
        "(iii) The perihelion:",
        " (iv) ",
        "",
    ),
    (
        "(vii) Dark energy's shape:",
        " (viii) The atom.",
        "",
    ),
    (
        "(viii) The atom.",
        "\\paragraph{",
        "The families of the register, each with its declared integers, its algebraic object and the click that reads it, are the families table \\cite{records}.\n\n",
    ),
)


def cut_fail_rows(s: str) -> tuple[str, list[str]]:
    """The three FAIL rows' full statements out, one sentence each in their place."""
    spans = []
    for start, end, line in FAIL_CUTS:
        i = _once(s, start, start)
        j = s.index(end, i) if end in s[i:] else len(s)  # a block may end before the marker
        spans.append(s[i:j])
        s = s[:i] + line + s[j:]
    return s, spans


LONGTABLE_END = "\\end{longtable}}"
TABLE_START = "{\\scriptsize\\setlength{\\tabcolsep}{3pt}"
CONVERSION_LABEL = "\\caption{\\label{tab:conversion}"
LEDGER_LABEL = "\\caption{\\label{tab:ledger}"
FAMILIES_LABEL = "\\caption{\\label{tab:families}"
SYMBOLS_START = "\\paragraph{The symbols.} {\\footnotesize"
SUMMARY_LABEL = "\\caption{\\label{tab:summary}"
KEPT_LABEL = "\\caption{\\label{tab:kept}"
OLD_FIGURES = ("fig:mechanism", "fig:interference", "fig:pair", "fig:sofn")
FIGURE_START = "\\begin{figure}"
FIGURE_END = "\\end{figure}"

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
    (
        "Figure~\\ref{fig:sofn}'s ($S$ at seven grains)",
        "the $S(\\Nphi)$ figure's, history \\cite{records} ($S$ at seven grains)",
    ),
    (
        "Figure~\\ref{fig:sofn}",
        "the $S(\\Nphi)$ figure of the engine before 2026-09-23, history \\cite{records}",
    ),
    ("Table~\\ref{tab:families} (below) lists", "The families table, in " + RECORDS + ", lists"),
    ("Table~\\ref{tab:families}", "the families table \\cite{records}"),
    (
        "the symbol table is\nAppendix~\\ref{app:technical},",
        "the symbol table is\nin " + RECORDS + ",",
    ),
    ("Figure~\\ref{fig:mechanism}", "Figure~\\ref{fig:worlds}"),
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


def cut_figure(s: str, label: str) -> tuple[str, str]:
    """Cut one figure environment whole by the label it carries."""
    i = _once(s, "\\label{" + label + "}", label)
    start = s.rindex(FIGURE_START, 0, i)
    end = s.index(FIGURE_END, i) + len(FIGURE_END)
    return s[start:end], s[:start] + s[end:]


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
    # The old law's section, whole, to the records; the new section (cut30/law.py)
    # and the old ledger paragraph in its place; the hand-worked update as before.
    oldlaw, s = _cut_between(s, OLDLAW_START, OLDLAW_END, "the old law section")
    k = oldlaw.index(LEDGER_START)
    ledger_paragraph, oldlaw = oldlaw[k:], oldlaw[:k]
    s = s.replace(OLDLAW_END, law.SECTION + ledger_paragraph + OLDLAW_END, 1)
    handworked, oldlaw = _cut_between(oldlaw, HANDWORKED_START, CODE_HEADING, "the hand-worked update")
    # The route's old road: the two tables and the simulator's part to the records,
    # the algebra document's chapter 7 before the paragraph that stays.
    tables, s = _cut_between(s, FORWARD_START, OPERATIONS_START, "the two direction tables")
    oldroad, s = _cut_between(s, SIMULATOR_START, DATED_START, "the old road")
    s = s.replace(OPERATIONS_START, route.OPENING + OPERATIONS_START, 1)
    conversion, s = cut_table(s, CONVERSION_LABEL, "the conversion table")
    ledger, s = cut_table(s, LEDGER_LABEL, "the ledger")
    families, s = cut_table(s, FAMILIES_LABEL, "the families table")
    # The comparison of the engine before 2026-09-23 (the one-page summary, the
    # kept words) and the figures of its readings: history (record 1459).
    summary, s = cut_table(s, SUMMARY_LABEL, "the old summary table")
    kept, s = cut_table(s, KEPT_LABEL, "the old kept-words table")
    figures = []
    for label in OLD_FIGURES:
        figure, s = cut_figure(s, label)
        figures.append(figure)
    # (after the old figures, which sat inside these paragraphs) The old readings and derivations of the physics section: the pace's readings,
    # the push's operations, the old push's derivations (the shell mean, Newton,
    # Coulomb, their ground), the delay field, the registered integers of the click.
    detector, s = _cut_between(s, DETECTOR_START, FORCES_HEADING, "the pace's readings")
    operations, s = _cut_between(s, OPERATIONS_PAR, GAUSS_START, "the push's operations")
    push, s = _cut_between(s, SHELL_START, DELAY_HEADING, "the old push's derivations")
    i = _once(s, DELAY_HEADING, "the delay field") + len(DELAY_HEADING)
    j = s.index(LIGHT_START, i)
    delay, s = s[i:j], s[:i] + "\n\n" + s[j:]
    s = s.replace(DELAY_HEADING, NEW_DELAY_HEADING, 1)
    registered, s = _cut_between(s, REGISTERED_START, INTERFERENCE_START, "the registered integers")
    i = _once(s, OLDCLICK_START, "the old click")
    j = s.index(OLDCLICK_END, i) + len(OLDCLICK_END)
    oldclick, s = s[i:j], s[:i] + click.DEFINITION + s[j:]
    s, fail_rows = cut_fail_rows(s)
    s, flight = cut_flight(s)
    i = _once(s, CODE_RUNTIME_START, "the code's gates")
    j = s.index(CODE_RUNTIME_END, i)
    coderuntime, s = s[i:j], s[:i] + CODE_RUNTIME_POINTER + s[j:]
    i = _once(s, ROAD_START, "the roads' check")
    j = s.index(ROAD_END, i)
    roadcheck, s = s[i:j], s[:i] + ROAD_POINTER + s[j:]
    i = _once(s, HISTORY_START, "the flight table's history")
    j = s.index(HISTORY_END, i)
    flighthistory, s = s[i:j], s[:i] + HISTORY_POINTER + s[j:]
    i = _once(s, SIXOPS_START, "the six operations as run")
    j = s.index(SIXOPS_END, i)
    sixops, s = s[i:j], s[:i] + SIXOPS_POINTER + s[j:]
    i = _once(s, LIGHT_START, "the delay's head")
    j = s.index(DELAY_HEAD_END, i)
    delayhead, s = s[i:j], s[:i] + DELAY_HEAD_POINTER + s[j:]
    i = _once(s, WEIGHT_START, "the weight rule")
    j = s.index(WEIGHT_END, i) + len(WEIGHT_END)
    weightrule, s = s[i:j], s[:i] + WEIGHT_POINTER + s[j:]
    i = _once(s, SYMBOLS_START, "the symbols")
    j = s.index(LONGTABLE_END, i) + len(LONGTABLE_END)
    symbols, s = s[i:j], s[:i] + POINTERS["symbols"] + s[j:]
    for old, new in REFERENCES:
        s = s.replace(old, new)  # a reference the paper no longer carries is simply absent
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
        + "\n\\section{The law as the engine ran it before 2026-09-23: the rows that hop, history}\\label{rec:oldlaw}\n\n"
        + "The section of the GameBoard as the paper carried it until the algebra's chapter 8 replaced the rows that hop (the Boss's order of 2026-09-24): the postulates with their old parameters, the map's old components, the two blocks, the old read-out by the wheel and the rungs, the code's gates and the dated transition.\n\n"
        + oldlaw
        + "\n\\section{The road as the paper carried it before the algebra document, history}\\label{rec:oldroute}\n\n"
        + "The two direction tables (the postulates and what each forces; the objects and what each gives back), the simulator's part and the dictionary of the rows that hop, as the route's section carried them until the algebra document's chapter 7 took their place (the Boss's order of 2026-09-24).\n\n"
        + tables
        + "\n\n"
        + oldroad
        + "\n\\section{The readings and the derivations of the engine before 2026-09-23, history}\\label{rec:oldreadings}\n\n"
        + "The paragraphs of the physics section that quoted the readings of the engine before 2026-09-23 as support (the pace after a detector, the registered integers of the split), the derivations from the push of the rows that hop (the inverse square as a shell mean, Newton's law and the place of G, Coulomb's law, their ground) and the delay field (the retarded potential, Poisson's equation, the clock's redshift), as the paper carried them until the algebra document's chapters replaced the rows that hop (record 1459; ALGEBRA.md 2.11).\n\n"
        + detector
        + "\n\n"
        + operations
        + "\n\n"
        + push
        + "\n\n"
        + delay
        + "\n\n"
        + registered
        + "\n\\section{The click as the beam law defined it: the layer, the ladder and the lemma, history}\\label{rec:oldclick}\n\n"
        + "The Definition of the click and the lemma of one click per record as the paper carried them until the detector law's click took their place (the chief physicist's line of 2026-09-24, 01:08Z; the Boss's order of 02:00Z): the layer's X and Y per Node, the offer of a set, the ladder of rungs over the birth phase, the pair's joint weights and the deferred offer.\n\n"
        + oldclick
        + "\n\\section{The road to each formula, and the check that nothing was derived from them, as Section 7 carried it}\\label{rec:roadcheck}\n\n"
        + roadcheck
        + "\n\n\\section{The beam law's flight table, the runtime before 3a9a7109, as Section 5 carried it, history}\\label{rec:flighthistory}\n\n"
        + flighthistory
        + "\n\n\\section{The six operations as the engine runs them, as Section 6 carried them}\\label{rec:sixops}\n\n"
        + sixops
        + "\n\n\\section{Light past a held mass by the time part alone, the delay paragraph's head, history}\\label{rec:olddelayhead}\n\n"
        + delayhead
        + "\n\n\\section{The beam law's weight rule for its rows 13 and 14, history}\\label{rec:weightrule}\n\n"
        + weightrule
        + "\n\n\\section{The design's scripts that gate the code, as Section 6 listed them}\\label{rec:coderuntime}\n\n"
        + coderuntime
        + "\n\\section{The beam law's flight table: the proof of the pace proposition and its ground, history}\\label{rec:oldflight}\n\n"
        + flight
        + "\n\\section{The three FAIL rows in full: the perihelion, the supernova diagram and the atom, history}\\label{rec:failrows}\n\n"
        + "\n\n".join(fail_rows)
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
        + "\n\n\\section{The comparison of the engine before 2026-09-23, history}\\label{rec:oldcomparison}\n\n"
        + "The one-page summary and the kept words of the register as the paper carried them until the law changed from its foundation (record 1459): the readings of the engine before 2026-09-23, never carried into the paper's table.\n\n"
        + summary
        + "\n\n"
        + kept
        + "\n\n\\section{The figures of the readings of the engine before 2026-09-23, history}\\label{rec:oldfigures}\n\n"
        + "\n\n".join(figures)
    )
    return s, records


def strip_block(body: str) -> str:
    """The cuts of `cut`, applied to one text block where their markers are
    present, for the test that holds every reordered block verbatim."""
    if LAW_BLOCK_START in body:  # the old law's section, whole in the records file
        body = body[: body.index(LAW_BLOCK_START)]
    if body.lstrip().startswith(CODE_HEADING):  # its gates on the code, likewise
        return ""
    if FORWARD_START in body:  # the route's two tables, whole in the records file
        i = body.index(FORWARD_START)
        j = body.index(OPERATIONS_START) if OPERATIONS_START in body else len(body)
        body = body[:i] + body[j:]
    if SIMULATOR_START in body:  # the simulator's part, likewise
        i = body.index(SIMULATOR_START)
        j = body.index(DATED_START) if DATED_START in body else len(body)
        body = body[:i] + body[j:]
    if body.lstrip().startswith(OLDROAD_START):  # the old dictionary, likewise
        return ""
    if FAIL_CUTS[0][0] in body:  # the three FAIL rows, one sentence each
        body, _ = cut_fail_rows(body)
    if ROAD_START in body:  # the roads' check, likewise (its block ends before the section)
        i = body.index(ROAD_START)
        j = body.index(ROAD_END, i) if ROAD_END in body[i:] else len(body)
        body = body[:i] + ROAD_POINTER + body[j:]
    if HISTORY_START in body:  # the flight table's history, likewise
        i = body.index(HISTORY_START)
        j = body.index(HISTORY_END, i) if HISTORY_END in body[i:] else len(body)
        body = body[:i] + HISTORY_POINTER + body[j:]
    if SIXOPS_START in body:  # the six operations as run, likewise
        i = body.index(SIXOPS_START)
        j = body.index(SIXOPS_END, i) if SIXOPS_END in body[i:] else len(body)
        body = body[:i] + SIXOPS_POINTER + body[j:]
    if LIGHT_START in body and DELAY_HEAD_END in body:  # the delay's head, likewise
        i = body.index(LIGHT_START)
        j = body.index(DELAY_HEAD_END, i)
        body = body[:i] + DELAY_HEAD_POINTER + body[j:]
    if WEIGHT_START in body and WEIGHT_END in body:  # the weight rule, likewise
        i = body.index(WEIGHT_START)
        j = body.index(WEIGHT_END, i) + len(WEIGHT_END)
        body = body[:i] + WEIGHT_POINTER + body[j:]
    if CODE_RUNTIME_START in body and CODE_RUNTIME_END in body:  # the code's gates, likewise
        i = body.index(CODE_RUNTIME_START)
        j = body.index(CODE_RUNTIME_END, i)
        body = body[:i] + CODE_RUNTIME_POINTER + body[j:]
    if FLIGHT_PROOF_START in body:  # the flight table's proof and ground, likewise
        body, _ = cut_flight(body)
    if OLDCLICK_START in body:  # the beam law's click, whole in the records file
        i = body.index(OLDCLICK_START)
        j = body.index(OLDCLICK_END, i) + len(OLDCLICK_END)
        body = body[:i] + click.DEFINITION + body[j:]
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
    for label in (CONVERSION_LABEL, LEDGER_LABEL, FAMILIES_LABEL, SUMMARY_LABEL, KEPT_LABEL):
        if label in body:
            _, body = cut_table(body, label, label)
    for label in OLD_FIGURES:
        if "\\label{" + label + "}" in body and FIGURE_START in body:
            _, body = cut_figure(body, label)
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
