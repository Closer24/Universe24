"""Reorder the manuscript into the six heads of the owner's approved structure.

The owner's decision (2026-09-23, his approval "okay, approved" of the
six-head structure; PLAN.md, "Step 1 of the reordering"): the paper opens
with the algebraic object, then the click-to-click chain, then what follows
from the algebra, then the GameBoard as the way the algebra is computed with,
then how the algebra was reached, then the comparison with nature and the
failures by cause. This module moves the existing text blocks into that
order. Nothing is cut and nothing is rewritten beyond the joins: every block
is matched exactly once by its heading or label, cut whole and placed whole;
the joins (JOINS) are the new section headings and one or two sentences
each, so a reader sees where a block went. `reorder(s)` returns the moved
text; BLOCKS names every cut so the tests can hold each block verbatim in
the output.
"""

# The cut blocks: name -> (start marker, end marker). A block runs from its
# start marker (inclusive) to its end marker (exclusive); both must occur
# exactly once in the text, the end after the start.
import massive

BLOCKS = {
    "words": (
        "\\paragraph{The definitions, in order.}",
        "\\begin{figure}[!tb]\\centering\\includegraphics[width=0.36\\linewidth]{figures/lattice.pdf}",
    ),
    "simulator_led": (
        "\\paragraph{From the physics to the mathematics: the postulates and what each forces.}",
        "\\paragraph{The reading rule and the notation.}",
    ),
    "road": (
        "\\paragraph{The road from the cells to the algebra.}",
        "Every family of the register is one row of declared integers (P8)",
    ),
    "families_intro": (
        "Every family of the register is one row of declared integers (P8)",
        "\\paragraph{Rules, parameters, initial conditions.}",
    ),
    "law": (
        "\\section{The law and its implementation}\\label{sec:law}",
        "\\section{Geometry and symmetries: the directions and $c = 1/\\sqrt3$}\\label{sec:geometry}",
    ),
    "code": (
        "\\paragraph{The code implements the law.}",
        "\\paragraph{The formulas after a detector.}",
    ),
    "ports": (
        "\\paragraph{The six Ports, the group and the front.}",
        "\\paragraph{The symmetries.}",
    ),
    "definitions": (
        "\\begin{definition}[Row and record]\\label{def:row}",
        "\\paragraph{The two theorems of the interval.}",
    ),
    "objects": (
        "\\paragraph{The objects.}",
        "\\paragraph{The hypotheses.}",
    ),
    "chain_click": (
        "\\paragraph{The steps between two clicks.}",
        "\\paragraph{The platform: how a formula is arrived at, by the algebra and by the simulator.}",
    ),
    "platform": (
        "\\paragraph{The platform: how a formula is arrived at, by the algebra and by the simulator.}",
        "\\paragraph{The step beneath and the step above.}",
    ),
    "chain_steps": (
        "\\paragraph{The step beneath and the step above.}",
        "\\paragraph{The road to each, and the check that nothing was derived from them.}",
    ),
    "road_to_each": (
        "\\paragraph{The road to each, and the check that nothing was derived from them.}",
        "\\paragraph{From an Inside formula to an Outside formula, family by family.}",
    ),
    "chain_conversion": (
        "\\paragraph{From an Inside formula to an Outside formula, family by family.}",
        "\\paragraph{What is proved.}",
    ),
    "proved": (
        "\\paragraph{What is proved.}",
        "\\paragraph{The limits, and what does not return.}",
    ),
    "limits": (
        "\\paragraph{The limits, and what does not return.}",
        "\\paragraph{What the law names and has not computed.}",
    ),
    "dated": (
        "\\paragraph{The transition from ordinary physics to the algebra, dated.}",
        "\\section{The families in the algebra, and the check of the roads}\\label{app:families}",
    ),
    "families_table": (
        "\\section{The families in the algebra, and the check of the roads}\\label{app:families}",
        "{\\scriptsize\\setlength{\\tabcolsep}{3pt} \\begin{longtable}{L{1.5in}L{1.75in}L{1.5in}L{1.4in}}",
    ),
}

FAMILIES_HEADING = (
    "\\section{The families in the algebra, and the check of the roads}\\label{app:families}"
)
ROADS_HEADING = "\\section{The check of the roads}\\label{app:families}"
CHECKS_HEADING = "\\section{The simulator's checks and the comparison with nature}\\label{sec:checks}"
DISCUSSION_HEADING = "\\section{Discussion and conclusions}\\label{sec:discussion}"
GEOMETRY_HEADING = (
    "\\section{Geometry and symmetries: the directions and $c = 1/\\sqrt3$}\\label{sec:geometry}"
)
TRANSITION_HEADING = "\\paragraph{When the transition was made.}"
FAMILIES_APPENDIX_REF = "Table~\\ref{tab:families} (Appendix~\\ref{app:families}) lists"
FAMILIES_BELOW_REF = "Table~\\ref{tab:families} (below) lists"

# The headings of the sections that become subsections under a head.
DEMOTED = [
    GEOMETRY_HEADING,
    "\\section{Conservation, the flux and the forces}\\label{sec:forces}",
    "\\section{The delay field: the retarded potential, Poisson's equation and the clock}\\label{sec:delay}",
    "\\section{Measurement and the quadratic form}\\label{sec:measurement}",
    "\\section{Bell and CHSH: from weights to counts}\\label{sec:bell}",
    CHECKS_HEADING,
    DISCUSSION_HEADING,
]

# The joins: the new headings and the sentences that show where a block went.
JOINS = {
    "intro_pointer": (
        "\\paragraph{Where the object came from.} The object was not chosen first. One Node with six Ports, one Link per interval and bounded integers were the assumptions of a simulator; its rules, written one by one as operations on a state vector, turned out to be six maps on one ring, and the maps that preserve a Node and its causal cone turned out to be the $48$ signed permutations, their rotations the group of order $24$ (Theorem~\\ref{th:group}); what did not converge to that group and that ring was not put in. The road, from the postulates to the objects they force and back, with the simulator running first and the derivations following it, is Section~\\ref{sec:route}; the GameBoard the object is computed with is Section~\\ref{sec:gameboard}.\n\n"
    ),
    "algebra_head": (
        "\\section{The algebra: the group, the ring and the families}\\label{sec:algebra}\n\n"
        "This section states the object and nothing else: the words of the board, the group of the six Ports, the ring of the phase and the record as its element, the rules of one interval, the click that reads a record once, and the families as declared integers on those objects. The definitions are gathered here from the sections that used them; every later section cites them by number.\n\n"
    ),
    "families_paragraph": "\\paragraph{The families as declared integers.} ",
    "click_head": (
        "\\section{From click to click}\\label{sec:click}\n\n"
        "Everything compared with nature is a count between clicks at a detector or a ratio of such counts; nothing inside the board is compared. This section reads forward: its clicks are those of Definition~\\ref{def:click} and its postulates are stated in Section~\\ref{sec:law}. This section is the chain from the ring's element read at a click to those counts and to the forms they take, the click frame under the hypotheses (A1) to (A3), each named where it enters; it uses the objects of Sections~\\ref{sec:physics} and~\\ref{sec:gameboard} by the names defined there. It opens with the six steps between two clicks, the two theorems of the Outside, and the one fact behind the uncertainty relation and Bell's excess; then the chain.\n\n"
    ),
    "physics_head": (
        "\\section{From the algebra, the physics}\\label{sec:physics}\n\n"
        "What follows from the algebra is stated first in one paragraph, each item with its word (exact; recovered in a limit; reached under named hypotheses; conjectured), and then subsection by subsection with the proofs, the runs that read each form after a detector, and the words kept apart.\n\n"
    ),
    "geometry_pointer": (
        "The six Ports and their group are Theorem~\\ref{th:group} of Section~\\ref{sec:algebra}; the symmetries of the law and the pace follow from them.\n\n"
    ),
    "measurement_pointer": (
        "The row and the record, the update rules of one interval and the click are Definitions~\\ref{def:row}, \\ref{def:rules} and~\\ref{def:click} of Section~\\ref{sec:algebra}, one click per record by that Definition.\n\n"
    ),
    "objects_pointer": (
        "The objects are those of Section~\\ref{sec:algebra}: the record's element $f$ of $\\Z[\\Z_{\\Nphi}]$, its pointer $\\mathrm{ev}(f)$ and the function $R$ of a cell's element.\n\n"
    ),
    "gameboard_head": (
        "\\section{The GameBoard: the way the algebra is computed with}\\label{sec:gameboard}\n\n"
        "The GameBoard is the way the algebra is computed with, not the object: a system of information transfer with costs, read in two ways, the detector's click a measurement and the host's view a diagnostic. This section states the law as one map, its state and its components, its read-out and its code, and the ledger of what the algebra shows on it.\n\n"
        "\\subsection{The law and its implementation}\\label{sec:law}"
    ),
    "route_head": (
        "\\section{How the algebra was reached: from the GameBoard to the group}\\label{sec:route}\n\n"
        "The order of this paper is not the order of the finding. The object of Section~\\ref{sec:algebra} was reached from the GameBoard: from one Node and its six neighbours, one message per Link per interval, through the simulator's runs, in dated steps; what did not converge to the group and the ring was not put in. This section states the one choice and what it forces (the algebra document's chapter 7 \\cite{algebra}), the road from the operations to the group, the dated steps, the platform on which a formula is arrived at by two roads, and the check of the roads; the two direction tables, the simulator's part and the dictionary of the rows that hop, as the paper carried them, are its record \\cite{records}.\n\n"
    ),
    "comparison_head": (
        "\\section{The comparison with nature, and the failures by cause}\\label{sec:comparison}\n\n"
        "Everything compared here is a detector's count or a ratio of counts (Section~\\ref{sec:click}); the readings are compared by kind, and each failure is named with its cause.\n\n"
    ),
    "discussion_pointer": (
        "The chain from the click to Lorentz's factors, Einstein's step and Newton's form is Section~\\ref{sec:click}; the two roads and their check are Section~\\ref{sec:route}; what is proved opens Section~\\ref{sec:physics}.\n\n"
    ),
}

# The cross-references whose target moved: each old string occurs once, with
# enough context to name it; the new string points where the text now stands.
REFS = [
    (
        "the click theorem's \\cite{clickframe} (Section~\\ref{sec:discussion})",
        "the click theorem's \\cite{clickframe} (Section~\\ref{sec:click})",
    ),
    (
        "$W$ is shown to second order (Section~\\ref{sec:discussion})",
        "$W$ is shown to second order (the step above, this section)",
    ),
    (
        "the GameBoard's corrections from the fourth (Section~\\ref{sec:discussion})",
        "the GameBoard's corrections from the fourth (Section~\\ref{sec:click})",
    ),
    (
        "are not derived here (Section~\\ref{sec:discussion})",
        "are not derived here (Section~\\ref{sec:click})",
    ),
    (
        "no verb reads the space part (Section~\\ref{sec:discussion}, the bending under the key)",
        "no verb reads the space part (Section~\\ref{sec:click}, the bending under the key)",
    ),
    (
        "the hypotheses beside the law are on the tree (Section~\\ref{sec:discussion})",
        "the hypotheses beside the law are on the tree (Section~\\ref{sec:click})",
    ),
    (
        "are one platform, stated in Section~\\ref{sec:discussion} so that",
        "are one platform, stated below so that",
    ),
    (
        "repeated in the abstract and in Section~\\ref{sec:discussion}: the paper's list",
        "repeated in the abstract and in Section~\\ref{sec:physics}: the paper's list",
    ),
    (
        "off by default; Section~\\ref{sec:discussion}): the loop stays",
        "off by default; Section~\\ref{sec:click}): the loop stays",
    ),
    ("written $n/d$ in Section~\\ref{sec:measurement}", "written $n/d$ in Section~\\ref{sec:algebra}"),
    (
        "The ladder's rungs $\\rung_k$ of Section~\\ref{sec:measurement} are walls",
        "The ladder's rungs $\\rung_k$ of Section~\\ref{sec:algebra} are walls",
    ),
    (
        "the label rotation (Section~\\ref{sec:measurement}'s matrix",
        "the label rotation (Section~\\ref{sec:algebra}'s matrix",
    ),
    ("$\\rung_K$ is Section~\\ref{sec:measurement}'s)", "$\\rung_K$ is Section~\\ref{sec:algebra}'s)"),
    (
        "the click's other zeros are the tables' own (Section~\\ref{sec:measurement})",
        "the click's other zeros are the tables' own (Section~\\ref{sec:algebra})",
    ),
    (
        "the six Ports, the hand bit & none & exact & \\ref{sec:geometry}",
        "the six Ports, the hand bit & none & exact & \\ref{sec:algebra}",
    ),
]


def _once(s: str, marker: str, name: str) -> int:
    n = s.count(marker)
    if n != 1:
        raise ValueError(f"reorder: the marker of {name} occurs {n} times, not once: {marker[:60]!r}")
    return s.index(marker)


def cut(s: str, name: str) -> tuple[str, str]:
    """Cut the block `name` out of `s`; return (the block, the text without it)."""
    start, end = BLOCKS[name]
    i = _once(s, start, name + " (start)")
    j = _once(s, end, name + " (end)")
    if j <= i:
        raise ValueError(f"reorder: the end of {name} precedes its start")
    return s[i:j], s[:i] + s[j:]


def _replace_once(s: str, old: str, new: str, name: str) -> str:
    _once(s, old, name)
    return s.replace(old, new)


def reorder(s: str) -> str:
    """The manuscript in the six heads' order (see the module docstring)."""
    blocks = {}
    for name in BLOCKS:
        blocks[name], s = cut(s, name)
    # The pointer where the simulator's paragraph stood in the Introduction.
    s = _replace_once(
        s,
        BLOCKS["simulator_led"][1],
        JOINS["intro_pointer"] + BLOCKS["simulator_led"][1],
        "intro pointer",
    )
    # The law's section, cut whole: its road paragraph and its families sentences
    # were cut out of it above (they stood inside its first line); the gates on
    # the code join it before the ledger's paragraph; the heading is demoted.
    law = blocks["law"]
    law = law[len(BLOCKS["law"][0]) :]
    law = _replace_once(
        law, TRANSITION_HEADING, blocks["code"] + TRANSITION_HEADING, "code before the ledger"
    )
    # The families table without its appendix heading; the appendix keeps the
    # roads table under its own heading and its label.
    families_table = blocks["families_table"][len(FAMILIES_HEADING) :]
    s = _replace_once(
        s,
        BLOCKS["families_table"][1],
        ROADS_HEADING + "  " + BLOCKS["families_table"][1],
        "roads heading",
    )
    families_intro = _replace_once(
        blocks["families_intro"], FAMILIES_APPENDIX_REF, FAMILIES_BELOW_REF, "families reference"
    )
    # Head 1, the object; head 2, click to click; head 3, from the algebra the
    # physics: all three enter before the geometry section, which is demoted.
    algebra = (
        JOINS["algebra_head"]
        + blocks["words"]
        + blocks["ports"]
        + blocks["objects"]
        + blocks["definitions"]
        + JOINS["families_paragraph"]
        + families_intro
        + families_table
        + "\n\n"
    )
    click = (
        JOINS["click_head"]
        + blocks["chain_click"]
        + blocks["chain_steps"]
        + blocks["chain_conversion"]
        + blocks["limits"]
    )
    physics = JOINS["physics_head"] + blocks["proved"]
    s = _replace_once(
        s,
        GEOMETRY_HEADING,
        algebra
        + massive.SECTION  # the massive record kind (ALGEBRA.md chapter 8; the owner's "everything starts from the algebra")
        + click
        + physics
        + GEOMETRY_HEADING.replace("\\section", "\\subsection")
        + "\n\n"
        + JOINS["geometry_pointer"],
        "the three heads before the geometry",
    )
    s = _replace_once(
        s,
        BLOCKS["definitions"][1],
        JOINS["measurement_pointer"] + BLOCKS["definitions"][1],
        "measurement pointer",
    )
    s = _replace_once(
        s, BLOCKS["objects"][1], JOINS["objects_pointer"] + BLOCKS["objects"][1], "objects pointer"
    )
    # Head 4, the GameBoard; head 5, the route; head 6, the comparison: all three
    # enter where the checks section stood, which is demoted under head 6.
    route = (
        JOINS["route_head"]
        + blocks["simulator_led"]
        + blocks["road"]
        + "\n\n"
        + blocks["dated"]
        + "\n\n"
        + blocks["platform"]
        + blocks["road_to_each"]
    )
    s = _replace_once(
        s,
        CHECKS_HEADING,
        JOINS["gameboard_head"]
        + law
        + route
        + JOINS["comparison_head"]
        + CHECKS_HEADING.replace("\\section", "\\subsection"),
        "the three heads before the checks",
    )
    s = _replace_once(
        s,
        DISCUSSION_HEADING,
        DISCUSSION_HEADING.replace("\\section", "\\subsection") + "\n\n" + JOINS["discussion_pointer"],
        "discussion pointer",
    )
    for heading in DEMOTED:
        if heading in (GEOMETRY_HEADING, CHECKS_HEADING, DISCUSSION_HEADING):
            continue  # demoted above, with their joins
        s = _replace_once(s, heading, heading.replace("\\section", "\\subsection"), "demotion")
    for old, new in REFS:
        s = _replace_once(s, old, new, "a reference whose target moved")
    return move_register_table(s)


REGISTER_START = (
    "{\\scriptsize\\setlength{\\tabcolsep}{3pt}\n\\begin{longtable}{L{0.3in}L{2.0in}L{1.5in}L{2.2in}}"
)
REGISTER_END = "\\end{longtable}}"
REGISTER_HEADING = "\\section{The confrontation register, the full record}\\label{app:register}\n\n"


def move_register_table(s: str) -> str:
    """The full confrontation register (tab:nature) becomes an appendix, the
    one-page summary staying in Part 7 (the Boss's order of 2026-09-23,
    02:53Z, on the owner's word of record 1207): the table is cut from its
    start marker to the first table end after it and placed, whole, under its
    own appendix heading before the check of the roads."""
    i = _once(s, REGISTER_START, "the register table (start)")
    j = s.index(REGISTER_END, i) + len(REGISTER_END)
    table, s = s[i:j], s[:i] + s[j:]
    return _replace_once(
        s, ROADS_HEADING, REGISTER_HEADING + table + "\n\n" + ROADS_HEADING, "the register's appendix"
    )
