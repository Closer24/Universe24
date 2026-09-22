"""The reviewer's corrections folded into the thirty-page assembly (2026-09-22).

The verdict on the cut at 5c6c4576 was ADMISSIBLE WITH CORRECTIONS (the
reviewer's report to the Boss, 01:31Z; the owner's word of 01:24Z made the
reviewer the paper's writer). Each correction below is one exact replacement
in the assembled text, applied exactly once by `assemble.py` after the four
parts are joined; a miss stops the build (`cut30_lib.sub` asserts the count).
The labels are the report's: M for must-fix, S for should-fix. The
editing seams of M7 are fixed at their source (`cut30_lib.cutp`, `part2.py`,
`part3.py`, `part4.py`), not here.

The grounds: the owner's thirty-page instruction (record 573 of
docs/LOG_2026-09-20.md), his guiding statement (record 595), the two checks
of the derivation's ground (records 607, 609) and the measurement rule
(records 281, 562, 575). No number is moved; a number's label is added where
its kind was not named.
"""

from cut30_lib import sub

CORRECTIONS = [
    # M1, M2, M3, S1: the abstract reads the ledger's ground column, and counts
    # the fifth PASS under the clock's assumed word.
    (
        "M1-M3, S1 abstract",
        "Exact on the GameBoard: the conservation of the books and a continuity equation, the pace bound $1/\\sqrt3$, the click's weight a positive quadratic form of power $2$ under one axiom of the apparatus, the exact marginals of a pair, and the CHSH sum as an exact function of the grain, $181/64$ at the powers of two from $512$ to $8192$. In the limit of the grain: Born's rule, Tsirelson's bound, Young's spacing, Planck's and de Broglie's identities. In the limit over a dense fan of directions: Gauss's law, Newton's and Coulomb's inverse square, the retarded potential and Poisson's equation.",
        "Exact on the GameBoard: the conservation of the books and the lattice form of the continuity equation, Gauss's law of a free family's flux under its world condition, the pace of every direction with its Manhattan bound, the click's weight a positive quadratic form of power $2$ under one axiom of the apparatus, the exact marginals of a pair, the CHSH sum as an exact function of the grain, $181/64$ at the powers of two from $512$ to $8192$, and Planck's and de Broglie's relations as identities under the declared dictionary. In the limit of the grain: the value $c = 1/\\sqrt3$, Born's rule, Tsirelson's bound, Young's spacing. In the limit under an average that covers the shell, the condition part of the claim: Newton's and Coulomb's inverse square, the retarded potential and Poisson's equation.",
    ),
    (
        "S1 abstract, the fifth PASS",
        "nature four readings pass and twelve fail, the failures the law's own.",
        "nature four readings pass, a fifth under the clock's assumed word, and twelve fail, the failures the law's own.",
    ),
    # M1, M2, M3: the discussion's three lists read the ledger's column.
    (
        "M1-M3 discussion",
        "Exact on the GameBoard: the group of the six Ports and its $24$ rotations; the books' conservation and the continuity equation; the split's isometry and the injectivity of the interval on the rows' weights, multiplicities and phases; the pace bound $1/\\sqrt3$; the click's weight a positive quadratic form of power $2$ under the axioms (a) to (e); the exact marginals of a pair; the CHSH sum as an exact function of the grain and the tables, with its closed form. In the limit of the grain, with a rate: Born's rule to $1/(2\\Nphi)$ per cell, Tsirelson's bound to $8/\\Nphi$, Young's spacing, the attained value of $c$, Planck's and de Broglie's identities. In the limit over a dense fan, with the condition in the claim: Gauss's law of the field, Newton's and Coulomb's inverse square, the retarded potential and Poisson's equation, the clock's $1/r$ form.",
        "Exact on the GameBoard: the group of the six Ports and its $24$ rotations; the books' conservation and the lattice form of the continuity equation; Gauss's law of a free family's flux under its world condition; the split's isometry and the injectivity of the interval on the rows' weights, multiplicities and phases; the pace of every direction, isotropic within $1/T_D$, with its Manhattan bound; the click's weight a positive quadratic form of power $2$ under the axioms (a) to (e); the exact marginals of a pair; the CHSH sum as an exact function of the grain and the tables, with its closed form; Planck's and de Broglie's relations as identities under the declared dictionary, an input. In the limit of the grain, with a rate: Born's rule to $1/(2\\Nphi)$ per cell, Tsirelson's bound to $8/\\Nphi$, Young's spacing, the attained value of $c$, the continuity equation's differential form. In the limit under an average that covers the shell, with the condition in the claim: Newton's and Coulomb's inverse square, the retarded potential and Poisson's equation, the clock's $1/r$ form.",
    ),
    (
        "S1 discussion, the fifth PASS; S5 the GameBoard's state",
        "nothing of the board is read as a measurement. Against nature four readings pass, twelve fail",
        "nothing of the GameBoard's state is read as a measurement. Against nature four readings pass, a fifth under the clock's assumed word, and twelve fail",
    ),
    # M4: row 2b's verdict rests on the clicks, not on the offers (a number of
    # the apparatus layer; records 281, 562).
    (
        "M4 row 2b",
        "2b & Mach-Zehnder visibility: $0.98$ & the clicks $64/0$ & PASS: $0.9988$ \\\\",
        "2b & Mach-Zehnder visibility: $0.98$ & the clicks $64/0$ over $64$ births, the dark port $0$ & PASS: the visibility $1.000$ in the clicks, above $0.98$ \\\\",
    ),
    # S1: the confrontation table's caption counts its own rows.
    (
        "S1 caption of the confrontation table",
        "Four PASS (each replicated by the second runner \\cite{replications}), twelve FAIL (eight in a registered run, four by a pin without its run, the latter not in this table), one BOUND, one declared input against nature, one row under an assumed word of the clock.",
        "Four PASS (each replicated by the second runner \\cite{replications}) and a fifth under the clock's assumed word (row 12); twelve FAIL: seven in a registered run, four by a pin without its run (not in this table), one a declared input refuted by nature (8c); two BOUND (5a; 7a on a declared input).",
    ),
    # M5: the owner's status word (record 573) on every central formula; the
    # derivation document's "reached" leaves the paper, and Coulomb's "in form"
    # (a status record 595 excludes) becomes what DERIVATIONS 21.2 row 7 says.
    (
        "M5 ledger caption",
        "The section is this paper's; the derivation's section is \\cite{derivations}'s.}",
        "Every row is derived from the update rules implemented in the simulator; what is added beside the rules, with its kind (an axiom of the apparatus, an input, a definition, a hypothesis), is the third column, and a result that rests on a hypothesis beside the law has no row. The section is this paper's; the derivation's section is \\cite{derivations}'s.}",
    ),
    (
        "M5 the shell mean",
        "ring, a number of the derivation and not a reading. Reached in the shell mean, with the ripple named;",
        "ring, a number of the derivation and not a reading. Derived from the update rules implemented in the simulator, in the shell mean, with the ripple named;",
    ),
    (
        "M5 Newton",
        "interval, not by a registered world). Reached in the shell mean, $G$ named;",
        "interval, not by a registered world). Derived from the update rules in the shell mean, $G$ named;",
    ),
    (
        "M5 Coulomb",
        "Reached in form; no detector reading of it is registered.",
        "Derived under the same average as Newton's, the ratio $-\\rho_A\\rho_B$ exact at every $r$; no detector reading of it is registered.",
    ),
    (
        "M5 the two fields",
        "Reached: in the limit of every direction the age moment is the retarded potential of the release and obeys the wave equation there.",
        "Derived from the update rules, in the limit of every direction: the age moment is the retarded potential of the release and obeys the wave equation there.",
    ),
    (
        "M5 the redshift",
        "is the $1/r$ law. Reached at first order.",
        "is the $1/r$ law. Derived at first order, the calibration an input.",
    ),
    (
        "M5 the lattice Gleason",
        "\\paragraph{What is reached and what is not.} Reached: the reading is a",
        "\\paragraph{What is derived and what is not.} Derived from the update rules and the axiom (b): the reading is a",
    ),
    (
        "M5 the limit of the click's form",
        "Reached for the form, the power and the multiplicity rule; not reached for the harmonic constants;",
        "Derived: the form, the power and the multiplicity rule; not derived: the harmonic constants;",
    ),
    # S3: the row that rests on a hypothesis beside the law leaves the ledger
    # (the covariant readings stay in the checks table and the distance table).
    (
        "S3 the muon's row",
        "The muon's decay tick under covariant-readings-v1 & the identity's owed count & the identity, a hypothesis beside the law & exact under the identity & 18.1 (a) \\\\",
        "",
    ),
    # M6: the defined version is the owner's tag (records 606, 616); the tree
    # of this cut named, the stale merge out.
    (
        "M6 the defined version",
        "The archived version cited at submission is the tagged release after the merge, one tree whose history holds the three trees named above and the log records this paper cites; it replaces the concept DOI below, and its code no longer has the world key. Every record, note, design and register row this text cites is on the tree it was written on (main merged at \\texttt{b6ab1bb3}); the far lamp's rows 11a to 11c rest on a pin whose run is not made.",
        "The archived version cited at submission is the tag \\texttt{paper-2026-09-22} on the merge commit of the pull request that carries this cut, one tree whose history holds the three trees named above and the log records this paper cites; it replaces the concept DOI below, and its code no longer has the world key. Every record, note, design and register row this text cites is on the tree of this cut (main merged into it at \\texttt{87c7ec6b}); the far lamp's rows 11a to 11c rest on a pin whose run is not made.",
    ),
    # S2: the 282 of 290 against Proposition prop:pace (equality on the
    # diagonals); S5: the GameBoard, not the board.
    (
        "S2 the 282 of 290",
        "while the board's Euclidean pace per direction is at or above $1/\\sqrt3$ on $282$ of the $290$ registered directions, $0.5818$ on every heading and $0.5774$ on the eight diagonals;",
        "while the GameBoard's Euclidean pace per direction is above $1/\\sqrt3$ on $282$ of the $290$ registered directions, $0.5818$ on every heading, and exactly at it, $0.5774$, on the eight diagonals;",
    ),
    # S4: a run not registered is not cited.
    (
        "S4 the crowd-clock pages",
        "The clock alone, without the field's push, is read on the crowd-clock pages of the tree (a lamp inside a crowd, a cluster of crowds, a reader inside a crowd; their register entries drafted \\cite{crowdclock,clusterclock,readerclock}), every reading inside its pin, measured once.",
        "",
    ),
    # S5: every symbol named at its first use; the GameBoard's state, never
    # the board; HYPOTHESES 27 cited once, in the discussion; the pinned row
    # named once, in Section 8.
    (
        "S5 eta named at first use",
        "releases at each self-creation the carry of the count of rate $M_B\\eta$ against the wall $1$",
        "releases at each self-creation the carry of the count of rate $M_B\\eta$, $\\eta$ the release rate per unit of content per direction, against the wall $1$",
    ),
    (
        "S5 beta named at first use",
        "$z = 0.2636$ at $\\beta = 0.2674$",
        "$z = 0.2636$ at $\\beta = v/c = 0.2674$",
    ),
    (
        "S5 the ledger paragraph",
        "whose derivation is not closed, or whose only reading is of the board, is not in the table; the hypotheses beside the law are on the tree \\cite{hypotheses}.",
        "whose derivation is not closed, or whose only reading is of the GameBoard's state, is not in the table; the hypotheses beside the law are on the tree (Section~\\ref{sec:discussion}).",
    ),
    (
        "S5 the comb of beams",
        "no single reading of the board is the inverse square;",
        "no single reading of the GameBoard's state is the inverse square;",
    ),
    (
        "S5 the distance table's caption",
        "What no rule of the law forces, and the check that decides each; the hypotheses beside the law are listed on the tree under their identities \\cite{hypotheses}.}",
        "What no rule of the law forces, and the check that decides each.}",
    ),
    (
        "S5 the single opening",
        "The single opening (Table~\\ref{tab:nature}, row 10) is pinned and not run under the one click; no number of it is carried here.",
        "The single opening (row 10 of the register) carries no number here (Section~\\ref{sec:checks}).",
    ),
    # S6: the apparatus layer's number labelled; the symbol table pruned to
    # the symbols this paper uses.
    (
        "S6 the Mach-Zehnder total",
        "The integer Mach-Zehnder's total over the $64$ birth phases takes eight values",
        "The integer Mach-Zehnder's record total over the $64$ birth phases, a number of the apparatus layer computed from the tables and not a reading, takes eight values",
    ),
    (
        "S6 symbols: the energy row",
        "$E$, $E_0$, $m$, $\\mathbf p$, $c$, $v$, $\\gamma$, $\\beta$ & scalars, one vector & the energy, the rest energy $E_0 = mc^2$, the mass $m = N_l N_w M$ in label units, the momentum, the limit speed $c = 1/\\sqrt3$ Links per interval, the speed, the Lorentz factor, $v/c$ \\\\",
        "$E$, $E_0$, $m$, $\\mathbf p$, $c$, $v$, $\\beta$ & scalars, one vector & the energy, the rest energy $E_0 = mc^2$, the mass $m = N_l N_w M$ in label units, the momentum, the limit speed $c = 1/\\sqrt3$ Links per interval, the speed, $v/c$ \\\\",
    ),
    (
        "S6 symbols: the exact square row",
        "$E^2/c^4$, $\\Eint$ & scalars & the exact square $m^2 + 3\\,\\mathbf p\\cdot\\mathbf p$ carried as an integer and never rooted; its integer root, kept by comparisons \\\\",
        "",
    ),
    (
        "S6 symbols: the quantum of action row",
        "$h$, $f$, $s_h$ & scalars & the quantum of action ($E = hf$), the frequency, a lamp's turn per self-creation \\\\",
        "$h$, $f$ & scalars & the quantum of action ($E = hf$), the frequency \\\\",
    ),
    (
        "S6 symbols: the coupling row",
        "$\\mathbf C$, $\\mathbf a$, $\\sigma_s$ & matrix, vector, scalar & the coupling matrix, the label flow read at a Node, the strong coupling per unit \\\\",
        "$\\mathbf a$ & vector & the label flow read at a Node \\\\",
    ),
    (
        "S6 symbols: the Gram matrix row",
        "$\\mathbf G$, $\\mathbf E$, $U_s$, $R(f)$, $R_k$ & matrices, a matrix written plain, a form, scalars & the click's Gram matrix, the tables' matrix, the label rotation (Section~\\ref{sec:measurement}'s matrix, written plain there), the click's reading (weight), a cell's weight \\\\",
        "$\\mathbf G$, $U_s$, $R(f)$, $R(o_A, o_B)$ & a matrix, a matrix written plain, a form, a scalar & the click's Gram matrix, the label rotation (Section~\\ref{sec:measurement}'s matrix, written plain there), the click's reading (weight), a cell's weight \\\\",
    ),
    (
        "S6 symbols: the wave row",
        "$\\mathbf k$, $k$, $\\Lambda$, $\\lambda$, $\\psi$, $\\theta$, $\\omega$ & a vector, scalars, a field & the wave vector and the wavenumber, a wavelength in Links and in the continuum, the wave function of the limit, an angle, the angular frequency \\\\",
        "$\\Lambda$, $\\lambda$, $\\psi_r$, $\\theta$ & scalars, an element & a wavelength in Links and in the continuum, the state of the record $r$ in the group ring, an angle \\\\",
    ),
    (
        "S6 symbols: the redshift row",
        "$z$, $H$, $q$, $G$, $\\rho$ & scalars & the redshift, the growing wall's rate, the deceleration parameter, Newton's constant, a family's charge per unit of content \\\\",
        "$z$, $q_0$, $G$, $\\rho$ & scalars & the redshift, the deceleration parameter (Table~\\ref{tab:nature}, row 3), Newton's constant, a family's charge per unit of content \\\\",
    ),
    (
        "S6 symbols: the multiplicity row",
        "$\\mathtt m$, $\\mathtt m(\\tau)$ & a row's attributes, in code font & a row's multiplicity; the Links a row has made by its age \\\\",
        "$\\mathtt m$ & a row's attribute, in code font & a row's multiplicity \\\\",
    ),
    (
        "S6 symbols: the second-meaning row",
        "$q$, $\\mathbf E$, $\\rho$, $f$, $s$, $e$, $r$, $d$, $H$, $S$, $W$, $a$ & letters with a second meaning, named where the text uses it & a source's release $q$ (Sections~\\ref{sec:forces} and~\\ref{sec:delay}) beside the deceleration parameter; Maxwell's field $\\mathbf E$ (the derivation's 25) beside the tables' matrix; a density $\\rho$ beside the charge per unit; a record's count vector $f$ in $R(f)$ beside the frequency; the turn's steps $s$ in $E = hs$ beside the accumulator; Euler's $e$ beside the event count; the radius $r$ beside the rate; the pair's denominator, a phase difference in steps and the derivation's density $d$ beside the wall; Shannon's $H$ beside the wall's rate; the CHSH sum $S$, and Boltzmann's $S$ and $W$; the wall's scale $a(t)$ beside the cap \\\\",
        "$q$, $f$, $s$, $e$, $r$, $d$, $H$, $S$, $W$ & letters with a second meaning, named where the text uses it & a source's release $q$ (Sections~\\ref{sec:forces} and~\\ref{sec:delay}) beside the deceleration parameter; a record's count vector $f$ in $R(f)$ beside the frequency; the turn's steps $s$ in $E = hs$ beside the accumulator; Euler's $e$ beside the event count; the radius $r$ beside the rate; the pair's denominator, a phase difference in steps and the derivation's density $d$ beside the wall; Shannon's $H$ of the entropy identity; the CHSH sum $S$, and Boltzmann's $S$ and $W$ \\\\",
    ),
    # S8: the distance table names the identification of position and
    # momentum beside the harmonic constants (PLAN.md section 5, item 4).
    (
        "S8 the harmonic constants' row",
        "The harmonic constants of the click: the axioms admit every Galois conjugate & the least-rank click, an axiom of the apparatus, pinned by the two-slit period and Malus at $22.5$ degrees; not derived \\\\",
        "The harmonic constants of the click (the axioms admit every Galois conjugate); the circle read as position, its transform as momentum (a hypothesis, Section~\\ref{sec:measurement}) & the least-rank click, an axiom of the apparatus, pinned by the two-slit period and Malus at $22.5$ degrees, not derived; the identification by the single opening against its pin (row 10) \\\\",
    ),
    # The page count: the displayed exact square (498b6f31) and the fold
    # together ran the body four lines onto page 26; the sentence on the
    # tables' precedents in signal processing leaves the positioning
    # paragraph (a precedent, not a claim; its four references with it), so
    # the body ends on page 25 as the owner approved.
    (
        "the page count: the signal-processing precedents",
        "of their own geometries. The declared rounding of the circle's tables has its precedents in the fixed-point transforms of signal processing \\cite{malvar2003,welch1969,mathews1963,goodman1970}. The earlier testbed",
        "of their own geometries. The earlier testbed",
    ),
]


def apply(text: str) -> str:
    """Apply every correction once, in order; a miss raises."""
    for label, old, new in CORRECTIONS:
        try:
            text = sub(text, old, new)
        except AssertionError as error:
            raise AssertionError(f"correction {label!r} did not match once: {error}") from None
    return text
