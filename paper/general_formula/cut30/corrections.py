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
    # The owner's word of 2026-09-22 in the writer's session: the covariant
    # rule's entry into the law is in hand (the Boss orders the route: the
    # Highlights line superseding record 270's, the three-tests verdict, the
    # directional drive, the off-axis runs); the paper says so in the
    # distance table's row and claims nothing until the readings land.
    (
        "the covariant rule in hand (the owner's word of 2026-09-22)",
        "the covariant readings (a body's energy as an exact square, its counts gated by $E_0/E$; series S's face clicks inside their pins on one axis) against the same pins \\\\",
        "the covariant readings (Eq.~\\eqref{eq:square}; series S's face clicks inside their pins on one axis) against the same pins; their entry into the law is in hand on the owner's word of 2026-09-22, the runs off the one axis pending, and this text claims nothing of it until they land \\\\",
    ),
    # Issues #553 and #544 against the merged cut (the Boss's word of 02:12Z,
    # record 651): the antiphase pair 1 + x^(N/2) is zero in the declared
    # quotient, so its "support 32" is the full DFT of an unreduced
    # representative and leaves the enumeration; the discussion's Born
    # clause reads the ledger's bound (a cell within 1 / N, the cumulative
    # within 1 / (2N)), not 1 / (2N) per cell.
    (
        "#553 the antiphase pair out of the support enumeration",
        "(one phase gives all $64$ roots, the antiphase pair $32$, a comb of every eighth phase $8$, the equality case)",
        "(one phase gives all $64$ roots, a comb of every eighth phase $8$, the equality case)",
    ),
    (
        "#544 the discussion's Born clause",
        "Born's rule to $1/(2\\Nphi)$ per cell, Tsirelson's bound",
        "Born's rule to $1/\\Nphi$ per cell and the cumulative rungs to $1/(2\\Nphi)$, Tsirelson's bound",
    ),
    # Newton after a detector, series D3 (PR #718; the physics-rule
    # reviewer's ADMISSIBLE WITH CORRECTIONS; the Boss's order of 02:24Z): the
    # equivalence principle measured after a detector, the 1 / r force's scale
    # symmetry read consistent on loops that are not similar figures, not
    # closed; G's value not read; the circle's pins outside as registered.
    # With it, four trims that hold the body at 25 pages: the second
    # departure's test-fixture clause (not a registered world), the "own
    # geometries" clause of the positioning paragraph, one sentence of the
    # ledger's caption, the distance line.
    (
        "D3 the checks table's Newton row",
        "$1.909 \\pm 0.05$; replicated \\\\",
        "$1.909 \\pm 0.05$; replicated \\\\\nThe equivalence principle after a detector; the $1/r$ force's scale symmetry & D3, a probe carrying a lamp on series D's plane at $r = 12$ and $24$, its births read at a line of one-Node detectors; the held mass four times at $r = 24$; two controls & the same $x$ on $138$ of $139$ common birth ticks (one Node the largest difference) and the same escape tick at four times the mass; $T(24)/T(12) = 1.997$ from one recurrence per radius on loops that are not similar figures; the controls at $x = 60 + r$ on every click; the circle's period, amplitude and $\\omega^2$ outside their pins & one birth interval and one Node; $2.00 \\pm 0.18$; $60 + r$, the escape $278 \\pm 6$ \\\\",
    ),
    (
        "D3 the distance table's Newton line",
        "Newton's and Poisson's laws measured after a detector & a body carrying a lamp beside a source, its births' Doppler read at a detector over time; a face detector's count of the escape against the release; the clock's form at more distances (series T's method) \\\\",
        "Newton's inverse square closed after a detector (the equivalence measured, series D3; the $1/r$ form's scale symmetry consistent, $1.997$ for $2.00 \\pm 0.18$, on loops that are not similar figures; $G$ not read), and Poisson's law measured & a closed orbit's period at two radii under the directional drive (form B, not built); a face detector's count of the escape against the release; the clock's form at more distances (series T's method) \\\\",
    ),
    (
        "D3 the ground paragraph of Section 4",
        "No detector reading of these laws is registered; their measurement after a detector is a run not made (Section~\\ref{sec:discussion}).",
        "After a detector the equivalence principle is measured (series D3, Table~\\ref{tab:checks}) and the $1/r$ force's scale symmetry reads consistent, $1.997$ for $2.00 \\pm 0.18$, on loops that are not similar figures: the inverse square is not closed after a detector and $G$'s value is not read; Coulomb's and Poisson's runs are not made (Section~\\ref{sec:discussion}).",
    ),
    (
        "D3 the introduction's open list",
        "Open, with the check that decides each: the measurement of Newton's and Poisson's laws after a detector, the clock",
        "Open, with the check that decides each: the closing of Newton's inverse square after a detector (the equivalence measured, series D3) and Poisson's law, the clock",
    ),
    (
        "D3 the page count: the second departure's fixture",
        "so a body can outrun its own field's rows on the drive as built on main (shown by the test fixture of the derivation's Doppler section, a body at $0.75$ Links per interval, not by a registered world).",
        "so a body can outrun its own field's rows on the drive as built on main.",
    ),
    (
        "D3 the page count: the own-geometries clause",
        "both sides of Tsirelson's bound \\cite{tsirelson1980,pr1994}; the experiments the checks are named for \\cite{tonomura1989,grangier1986,ghsz1990,ev1993} are reproduced in none of their own geometries. The earlier testbed",
        "both sides of Tsirelson's bound \\cite{tsirelson1980,pr1994}. The earlier testbed",
    ),
    (
        "D3 the page count: the ledger's caption",
        "Every row is derived from the update rules implemented in the simulator; what is added beside the rules, with its kind (an axiom of the apparatus, an input, a definition, a hypothesis), is the third column, and a result that rests on a hypothesis beside the law has no row.",
        "Every row is derived from the update rules implemented in the simulator; the third column names what is added beside them with its kind; a result resting on a hypothesis beside the law has no row.",
    ),
    (
        "D3 the page count: the octahedron figure",
        "\\includegraphics[width=0.34\\textwidth]{figures/octahedron.pdf}",
        "\\includegraphics[width=0.27\\textwidth]{figures/octahedron.pdf}",
    ),
    (
        "D3 the page count: the figure's caption",
        "The Nodes one interval from a Node. The six neighbours at the ends of the six Links (the Ports $\\pm x$, $\\pm y$, $\\pm z$) are the vertices of the octahedron $|x| + |y| + |z| \\le 1$, the causal front of one interval. Its inscribed sphere, of radius $1/\\sqrt3$, touches the eight faces on the cube diagonals at $(\\pm1, \\pm1, \\pm1)/3$ and is the rows' pace $c$, the largest isotropic pace under one Link per interval (Proposition~\\ref{prop:pace}); a row's mean pace lies within $1/T_D$ of the sphere and never at a vertex. The faint cube shares the octahedron's symmetry, the $48$ signed permutations of the axes, $3! \\times 2^3$, $24$ rotations and $24$ reflections told apart by the determinant, the GameBoard's stand-in for the rotation group. Drawn by \\texttt{octahedron.py} from the definitions; no run.}",
        "The Nodes one interval from a Node: the six neighbours are the vertices of the octahedron $|x| + |y| + |z| \\le 1$, the causal front of one interval; its inscribed sphere, of radius $1/\\sqrt3$, touches the eight faces on the cube diagonals and is the rows' pace $c$ (Proposition~\\ref{prop:pace}); the faint cube shares the $48$ signed permutations of the axes. Drawn by \\texttt{octahedron.py} from the definitions; no run.}",
    ),
    (
        "D3 the page count: the symmetries' parenthesis",
        "up to the law's two declared ties, the digital line's axis order and the collision's Port order (\\cite{beamlaw}, note 39 and section 4; the apportioning's tie, by the row's age, breaks no axis symmetry; this paper meets the first, Section~\\ref{sec:measurement}); under the circle",
        "up to the law's two declared ties, the digital line's axis order and the collision's Port order (\\cite{beamlaw}, note 39 and section 4); under the circle",
    ),
    (
        "D3 the page count: the code paragraph",
        "the readings at each Node (the presence, the age moment and the first moment of the arriving rows), the collision,",
        "the readings at each Node, the collision,",
    ),
    (
        "the ledger's no-dispersion row: the flight's blindness to the phase is put in (P9), not forced (the owner's word of 02:50Z)",
        "No dispersion & the flight table indexed by direction and age & none & exact & \\ref{sec:geometry} \\\\",
        "No dispersion, the constancy of $c$ & the flight table indexed by direction and age & the rate in transit constant, the flight blind to the phase (P9, a rule chosen among few); whether the six operations force it is open & exact & \\ref{sec:geometry} \\\\",
    ),
    (
        "GRB 090510: the constancy of c by the postulate meets the photon-dispersion bound (the Boss's word of 02:53Z; NUMBERS.md rows 97 to 99, a computation)",
        "free of dispersion by construction, as a classical corpuscle is.",
        "free of dispersion by construction, as a classical corpuscle is. By the postulate P9 the pace has no dispersion at any phase rate, so the model meets the bound on an energy-dependent speed of light from GRB 090510, a difference below $2.6 \\times 10^{-18}$ between $31$ GeV and the keV band \\cite{abdo2009}, a computation \\cite{checks}, not a run, and a consequence of the postulate until the six operations are shown to force it.",
    ),
    (
        "GRB 090510: the reference",
        "\\bibitem{nagel2015} M. Nagel,",
        "\\bibitem{abdo2009} A. A. Abdo et al. (Fermi LAT and Fermi GBM Collaborations), Nature 462, 331 (2009).\n\\bibitem{nagel2015} M. Nagel,",
    ),
    # The page count with the GRB sentence and the honest ledger row: seven
    # trims of duplicated sentences and asides, no claim and no table number.
    (
        "page count: the anisotropy bound said twice in Section 3",
        "same age $29$. Nature's bound on the anisotropy of $c$, below $10^{-18}$ \\cite{nagel2015}, is a bound on the grain, $N_l$ at or above $5.8 \\times 10^{17}$ (Section~\\ref{sec:checks}, row 5a).",
        "same age $29$.",
    ),
    (
        "page count: the delay section's operations list (the ledger's row carries it)",
        "its push reads the flow of the same rows. The operations: the release and the walk (translations), the reading (the zeroth moment, the age moment, the first moment: bilinear forms), the owed count (the Euclidean division), the coupling (a bilinear form).",
        "its push reads the flow of the same rows.",
    ),
    (
        "page count: the theorem's parenthetical repeated in the next paragraph",
        "2.828125$ at every power of two from $512$ through $8192$ (run at $512$ and $4096$, computed exactly at $2048$ and $8192$; $5793/2048$ at $16384$ and $32768$, the closed form of the derivation's 24.4) \\cite{checks}.",
        "2.828125$ at every power of two from $512$ through $8192$ \\cite{checks}.",
    ),
    (
        "page count: the harmonic's aside in the limit paragraph",
        "the fundamental is what the register reads and what the phase means (one step per declared rate; a detector at the harmonic $j$ is a detector reading the wavelength $\\Lambda/j$).",
        "the fundamental is what the register reads and what the phase means.",
    ),
    (
        "page count: the symbol table without Lambda",
        "$\\Lambda$, $\\lambda$, $\\psi_r$, $\\theta$ & scalars, an element & a wavelength in Links and in the continuum, the state of the record $r$ in the group ring, an angle",
        "$\\lambda$, $\\psi_r$, $\\theta$ & scalars, an element & a wavelength, the state of the record $r$ in the group ring, an angle",
    ),
    (
        "page count: the read-out's aside",
        "The click reads one comparison and nothing else leaves the rows (a detector's other readings, the counts, the flow and the moments of the rows at its Node, read and delete nothing): for a record",
        "The click reads one comparison and nothing else leaves the rows: for a record",
    ),
    (
        "page count: the introduction's window",
        "which pinned the power of the click's weight to a window containing $2$ and excluding $1$ and $3$ before the form was proved;",
        "which pinned the power of the click's weight to a window containing $2$ before the form was proved;",
    ),
    # The constancy of c is the declared postulate P9 and not a theorem of the
    # six operations (DERIVATIONS_BEAM section 27: a dispersive flight passes
    # the three tests, the books, the isometry, the injectivity, the isotropy
    # and the direction-only requirement); the Boss's word of 03:08Z.
    (
        "c a postulate: the ledger's no-dispersion row closed",
        "the rate in transit constant, the flight blind to the phase (P9, a rule chosen among few); whether the six operations force it is open & exact",
        "the rate in transit constant, the flight blind to the phase (P9, a rule chosen among few), not forced by the six operations: a dispersive flight passes every requirement (the derivation's 27) & exact",
    ),
    (
        "c a postulate: the GRB sentence",
        "a computation \\cite{checks}, not a run, and a consequence of the postulate until the six operations are shown to force it.",
        "a computation \\cite{checks}, not a run, and a consequence of the postulate.",
    ),
    # The owner's review of the 30 pages (2026-09-22; his word "go"): the
    # writer's part of the five must-fix items. (1) The Gleason theorem is
    # about the ideal reading; the built click violates hypothesis (a) by the
    # tables' rounding (C[1]^2 + S[1]^2 = 65650 at N = 64, a part in 276), the
    # sentence the generator's cut dropped restored with the norm range as the
    # error bound; and the power's window read from the click cells is a
    # read-back of an engine that carries the square, an implementation check
    # and not evidence about nature. (3) Tsirelson's bound with the tables'
    # term. (4) hbar under the paper's own dictionary. The age bounded.
    (
        "review (1): the power's window an implementation check; the tables' violation of (a) restored",
        "its upper from $\\Nphi = 128$, containing $2$ and excluding $1$ and $3$. The two-slit clicks",
        "its upper from $\\Nphi = 128$, containing $2$ and excluding $1$ and $3$. These windows are read back from the built click, which carries the square: a check that the implementation is the form of Theorem~\\ref{th:gleason}, no evidence about nature's power (Table~\\ref{tab:nature}, row 2c). The theorem is about the ideal reading; the built click is this form to the tables' rounding, a record's total over the $64$ birth phases from $65448/65536$ to $65773/65536$, the tables' violation of hypothesis (a) (at $\\Nphi = 64$, $C[1]^2 + S[1]^2 = 65650$; the extreme a part in $276$), the norm range of Appendix~\\ref{app:technical} the error bound. The two-slit clicks",
    ),
    (
        "review (1): the k = 1 and k = 3 aside out (an implementation check needs no counterfactual)",
        "both windows contain $2$ and exclude $1$ and $3$ ($k = 1$ gives $56/8$ and $23, 9, 9, 23$; $k = 3$ gives $64/0$ and $30, 2, 2, 30$).",
        "both windows contain $2$ and exclude $1$ and $3$.",
    ),
    (
        "review (1): the introduction's window sentence",
        "which pinned the power of the click's weight to a window containing $2$ before the form was proved;",
        "whose window for the click's power, containing $2$, was read back from the built click before the form was proved, a check of the implementation;",
    ),
    (
        "review (1): what excludes the phase-blind detector is interference, not the register alone",
        "The algebra admits the phase-blind detector; what excludes it is the register.",
        "The algebra admits the phase-blind detector; what excludes it is interference, nature's (Table~\\ref{tab:nature}, row 2a) and, for the implementation, the built click's.",
    ),
    (
        "review (2): Theorem 3 on the quotient that forgets the age, for the fixed event history (the derivation mathematician's wording, 2026-09-22)",
        "For an interval without a click, an end at a face or the border, or a collision, $M \\circ R \\circ S \\circ F$ is an injective $\\Z$-linear map from $\\bigoplus_r M_r$ to $\\bigoplus_r M_r$ on the rows' weights, multiplicities and phases, the GameBoard's state alone: no rule of the interval deletes them, and the state at any interval between two clicks determines them at the birth. A row's age is its count of intervals since its last event (Definition~\\ref{def:rules}), so a split, an event, restarts it at $0$ by that definition; the age before the event is read by no rule and is no part of the state after it. The click is the one deletion.",
        "Let $Q$ be the quotient of $\\bigoplus_r M_r$ that forgets the age (rows differing only in their age identified), and fix the event history of the record, the intervals and Nodes of its births, splits, rotations and re-emissions, which the record keeps. For an interval without a click, an end at a face or the border, or a collision, $M \\circ R \\circ S \\circ F$ induces an injective $\\Z$-linear map of $Q$ into itself: no rule of the interval deletes a weight, a multiplicity or a phase, and the state at any interval between two clicks, with the history, determines them at the birth. The age is not a coordinate of $Q$ but a function of the history, the current interval less the interval of the row's last event; a split restarts it at $0$ by the definition of age (Definition~\\ref{def:rules}) and forgets nothing, since the interval of the split is in the history; the click is the one deletion.",
    ),
    (
        "review (3): Tsirelson's bound with the tables' term in the discussion",
        "Tsirelson's bound to $8/\\Nphi$, Young's spacing, the attained value of $c$,",
        "Tsirelson's bound to $8/\\Nphi$ plus the tables' $0.0444$ ($2\\sqrt2$ in the joint limit of $\\Nphi$ and $N_t$), Young's spacing, the attained value of $c$,",
    ),
    (
        "review (4): hbar under the dictionary h = h_q N",
        "with $\\hbar = h\\Nphi/(2\\pi)$",
        "with $\\hbar = h/(2\\pi) = h_q\\Nphi/(2\\pi)$",
    ),
    (
        "review (7): the age bounded",
        "a row's age (the rate $1$, no wall)",
        "a row's age (the rate $1$, no wall; bounded by the family's lifetime and the run)",
    ),
    # The page count: six trims of duplicated or narrative text, no claim.
    (
        "page count: the Courant sentence repeated in the positioning paragraph",
        "the pace $1/\\sqrt3$ is the cubic lattice's Courant bound \\cite{cfl1928} and the lattice Boltzmann sound speed \\cite{qian1992}; the transport",
        "the transport",
    ),
    (
        "page count: the visibility clause of the limit paragraph",
        "the Born kernel $\\cos\\theta$ is the first of them, and the visibility of two rows is $\\mathcal K(\\theta)/\\mathcal K(0)$.",
        "the Born kernel $\\cos\\theta$ is the first of them.",
    ),
    (
        "page count: the clock's word as its fact",
        "The owner's word of 2026-09-21 (record 394 \\cite{log}) chose the age moment as the clock's word, entered as an assumption of the law (P9) and not as a derivation, where the law as built counts the presence by default and the age moment on an entry that reads the age, the default to follow the word; the presence word stays in the record as the alternative refuted on the form.",
        "The age moment is the clock's word, an assumption of the law (P9; record 394 \\cite{log}), not a derivation; the law as built counts the presence by default and the age moment on an entry that reads the age; the presence word is the alternative refuted on the form.",
    ),
    (
        "page count: G's makeup said twice in Section 4",
        "Derived from the update rules in the shell mean, $G$ named; $G$ is a formula of the release rate, the fan and the width, and the width $N_w$ is an input, a choice of units (Table~\\ref{tab:ledger}).",
        "Derived from the update rules in the shell mean, $G$ named, the width $N_w$ an input, a choice of units (Table~\\ref{tab:ledger}).",
    ),
    (
        "page count: series K's numbers repeated outside Table 2",
        "blind to the crowd (series K, registered: the mean age $89.40$ in every world, the difference $0.00$).",
        "blind to the crowd (series K, Table~\\ref{tab:checks}).",
    ),
    (
        "page count: the cone example of the introduction",
        "explained through $8192$ and beyond; the pace $c = 1/\\sqrt3$ came from a cone world in which two rows on different digital lines reached their counters at the same age.",
        "explained through $8192$ and beyond.",
    ),
    (
        "page count: the limits paragraph's repeats",
        "Tsirelson's value is a limit of the two terms of Theorem~\\ref{th:bell}; the light cone is the octahedron scaled by the age, isotropic within $1/T_D$; the content and $\\sum w^2/\\mathtt m$ are conserved exactly, the offered norm only within the tables' rounding.",
        "The content and $\\sum w^2/\\mathtt m$ are conserved exactly, the offered norm only within the tables' rounding.",
    ),
    (
        "page count and review (1): what the runs support, without the power's window",
        "After a detector the simulator reads the pace and its isotropy, the click's cells and the power's window, $S$ at four grains, the interference of one record, GHZ's triples, Malus's law and the clock's form at two distances, each inside an expectation written before the run (Table~\\ref{tab:checks}); nothing of the GameBoard's state is read as a measurement.",
        "After a detector the simulator reads what Table~\\ref{tab:checks} lists, each inside an expectation written before the run; nothing of the GameBoard's state is read as a measurement.",
    ),
    (
        "review (1): the introduction's map of results without the power's window",
        "the click's cells and the power's window, $S$ at four grains,",
        "the click's cells, $S$ at four grains,",
    ),
    (
        "page count: the crossing rule's counts are the ledger's",
        "the crossing rule's tests read $k + 55/32$ rows per $k$ intervals toward a moving source, $k - 55/32$ away and $k$ at rest. These are",
        "the crossing rule's tests read their pinned counts. These are",
    ),
    (
        "page count: the two loophole-free experiments the model cannot compare",
        "the loophole-free \\cite{hensen2015} excludes no $\\Nphi$; \\cite{giustina2015,shalm2015} report a quantity whose comparison needs a detector efficiency the model lacks.",
        "the loophole-free \\cite{hensen2015} excludes no $\\Nphi$.",
    ),
    (
        "page count: Section 7's opening repeats the click's definition",
        "For a record with arms at two rotated sets $A$ and $B$ the cells are the joint outcomes, the weights are Eq.~\\eqref{eq:joint}, the rungs Eq.~\\eqref{eq:rung}, and the record is gathered once when the rows at both arms have ended. The correlation",
        "The correlation",
    ),
    # Theorem 3 restated on the quotient that forgets the age (the derivation
    # mathematician's wording): the proof, the introduction, the ledger and
    # the discussion say the same. Table 3's rows 2a, 2b and 2c carry the
    # register's criterion (the chief physicist's lines); 2c's verdict is
    # NOT COMPARED, the power's window an implementation gate; the tallies
    # follow (three PASS, a fourth under the clock's word, one NOT COMPARED).
    (
        "review (2): the proof's F on Q",
        "$F$ maps a basis element to a basis element and is injective because the age is kept whole: $(D, \\tau) \\mapsto (D, \\tau+1)$ is injective and the Node offset is a function of $(D, \\tau)$.",
        "$F$ maps a basis element of $Q$ to a basis element, the Node moved by an offset that is a function of $D$ and of the age, the history's; with the history fixed it is injective on the basis.",
    ),
    (
        "review (2): the proof's S on Q and the record as the history",
        "on the weights, multiplicities and phases it is injective by Theorem~\\ref{th:isometry} (the conjugate transpose inverts it), and the age it restarts is, by definition, the count since this event. (The engine's record of the event, a host diagnostic read by no rule and compared with nothing, keeps the age the row arrived with for the books and the replay; the statement does not use it.)",
        "on $Q$ it is injective by Theorem~\\ref{th:isometry} (the conjugate transpose inverts it on the weights, multiplicities and phases); on $Q$ there are no two rows differing only in age, and their ages are the history's, the count since this event. (The engine's record of the event, a host diagnostic read by no rule and compared with nothing, is the history the statement fixes; it keeps the age the row arrived with for the books and the replay.)",
    ),
    (
        "review (2): the introduction's sentence on the injective interval",
        "every step of the linear block is injective on the rows' weights, multiplicities and phases, the GameBoard's state alone (Theorem~\\ref{th:bijection}); the click is the one deletion.",
        "every step of the linear block is injective on the rows' weights, multiplicities and phases for the event history the record keeps (Theorem~\\ref{th:bijection}); the click is the one deletion.",
    ),
    (
        "review (2): the ledger's row",
        "The split an isometry; the interval injective on the amplitudes & the six operations & none & exact &",
        "The split an isometry; the interval injective on the amplitudes for a fixed event history & the six operations & none & exact &",
    ),
    (
        "review (2): the discussion's list of what is proved",
        "the split's isometry and the injectivity of the interval on the rows' weights, multiplicities and phases; the pace of every direction",
        "the split's isometry and the injectivity of the interval on the rows' weights, multiplicities and phases for a fixed event history; the pace of every direction",
    ),
    (
        "review (5): Table 3's row 2a with the register's criterion",
        "2a & Two-slit visibility of one quantum at a time: $0.98$ \\cite{grangier1986} & $0.966$ in the clicks under the birth wheel, $4096$ births (L2b) & FAIL by $0.014$; the cause named, the fan's grain \\\\",
        "2a & Two-slit visibility of one quantum at a time: $0.98$ \\cite{grangier1986}, the ideal $1$; the criterion the clicks' visibility $(I_{\\max} - I_{\\min})/(I_{\\max} + I_{\\min})$, no apparatus model & $0.966$ in the clicks of \\texttt{slits\\_huygens} (the golden-rate wheel, $4096$ births under the exact phase; L2b), $0.954$ in the record's weights & FAIL: $0.014$ below the measured, $0.034$ below the ideal; the cause named, the screen's fan's grain (the pin derived for the screen's fan, not this world's) \\\\",
    ),
    (
        "review (5): Table 3's row 2b with the register's criterion",
        "2b & Mach-Zehnder visibility: $0.98$ & the clicks $64/0$ over $64$ births, the dark port $0$ & PASS: the visibility $1.000$ in the clicks, above $0.98$ \\\\",
        "2b & Mach-Zehnder visibility: $0.98$; the criterion the offers' visibility $(D_1 - D_2)/(D_1 + D_2)$ of \\texttt{mz\\_equal}, no apparatus model & the offers $1681/1682$ and $1/1682$; the clicks $64/0$ over $64$ births & PASS: $0.9988$, above $0.98$ \\\\",
    ),
    (
        "review (5): Table 3's row 2c not compared",
        "& the power's window $[1.917, 2.012)$ from the click cells & PASS on the power: the window contains $2$; $\\kappa$ an observable the law does not compute here \\\\",
        "& the power's window $[1.917, 2.012)$ from the click cells, a read-back of the built click, which carries the square & NOT COMPARED ($\\kappa$ not computed): the window a gate on the implementation, no evidence about nature; no three-opening world is registered \\\\",
    ),
    (
        "review (5): the verdict words",
        "BOUND where the comparison bounds a free parameter.",
        "BOUND where the comparison bounds a free parameter, NOT COMPARED where the law does not compute the observable.",
    ),
    (
        "review (5): Table 3's tally",
        "Four PASS (each replicated by the second runner \\cite{replications}) and a fifth under the clock's assumed word (row 12); twelve FAIL: seven in a registered run, four by a pin without its run (not in this table), one a declared input refuted by nature (8c); two BOUND (5a; 7a on a declared input).",
        "Three PASS (each replicated by the second runner \\cite{replications}) and a fourth under the clock's assumed word (row 12); twelve FAIL: seven in a registered run, four by a pin without its run (not in this table), one a declared input refuted by nature (8c); two BOUND (5a; 7a on a declared input); one NOT COMPARED (2c).",
    ),
    (
        "review (5): the abstract's tally",
        "nature four readings pass, a fifth under the clock's assumed word, and twelve fail, the failures the law's own.",
        "nature three readings pass, a fourth under the clock's assumed word, twelve fail and one is not compared, the failures the law's own.",
    ),
    (
        "review (5): the discussion's tally",
        "Against nature four readings pass, a fifth under the clock's assumed word, and twelve fail",
        "Against nature three readings pass, a fourth under the clock's assumed word, twelve fail and one is not compared",
    ),
    (
        "review (5) and the page count: the three-slit sentence of Section 6 is Table 3's row 2c",
        "Theorem~\\ref{th:bell}. Sinha et al.'s three-slit test read the third-order term $\\kappa = 0.0064 \\pm 0.0119$ \\cite{sinha2010}; the click's form, a quadratic, gives $\\kappa = 0$ exactly, and its power's window contains $2$ (Table~\\ref{tab:nature}, row 2c).",
        "Theorem~\\ref{th:bell}.",
    ),
    # The page count after the owner's five: four asides whose numbers Table 2
    # carries, no claim moved.
    (
        "page count: series S's numbers are Table 2's",
        "(series S: the muon's $64$th self-creation at $70$ and $124$ intervals against $64$ at rest, the face clicks $369$ and $345$ against $392$, inside their pins)",
        "(series S, Table~\\ref{tab:checks}, inside their pins)",
    ),
    (
        "page count: the Lorentz row's in-hand clause",
        "their entry into the law is in hand on the owner's word of 2026-09-22, the runs off the one axis pending, and this text claims nothing of it until they land",
        "their entry into the law in hand (the owner's word of 2026-09-22), the runs off the one axis pending, nothing claimed until they land",
    ),
    (
        "page count: the Newton row's numbers are Table 2's",
        "Newton's inverse square closed after a detector (the equivalence measured, series D3; the $1/r$ form's scale symmetry consistent, $1.997$ for $2.00 \\pm 0.18$, on loops that are not similar figures; $G$ not read), and Poisson's law measured",
        "Newton's inverse square closed after a detector (the equivalence measured and the $1/r$ form's scale symmetry consistent, series D3, Table~\\ref{tab:checks}; $G$ not read), and Poisson's law measured",
    ),
    (
        "page count: row 3's aside",
        "(series G2, the pointer's $z$; reproduced at head as a verdict with the digits moved, $-0.104$, record 408 \\cite{log})",
        "(series G2, the pointer's $z$; $-0.104$ at head, record 408 \\cite{log})",
    ),
    (
        "page count: the masses row",
        "every equal split is a fixed point and none is selected; the law gives floors only",
        "every equal split is a fixed point; the law gives floors only",
    ),
    (
        "page count: the hypotheses' sentence",
        "the hypotheses under their identities with what would close and what would refute each, is on the tree",
        "the hypotheses under their identities, is on the tree",
    ),
    (
        "page count: the earlier testbed",
        "The earlier testbed of this program \\cite{paper1}, with its draw and its return, is history: no rule of it survives here.",
        "The earlier testbed of this program \\cite{paper1} is history: no rule of it survives here.",
    ),
    (
        "page count: row 4b's aside",
        "(series G2, read before the crossing rule; not reproduced at head, the re-run pending under the age word)",
        "(series G2, before the crossing rule; the re-run at head pending)",
    ),
    (
        "page count: the three decisive failures are named once, in the prediction paragraph",
        "twelve fail and one is not compared (Table~\\ref{tab:nature}), and the three decisive failures, the unslowed clock in motion, light unbent beside a mass and the coasting deceleration, each refute the law as declared.",
        "twelve fail and one is not compared (Table~\\ref{tab:nature}); each failure refutes the law as declared.",
    ),
    (
        "page count: Table 4's Newton cell",
        "Newton's inverse square closed after a detector (the equivalence measured and the $1/r$ form's scale symmetry consistent, series D3, Table~\\ref{tab:checks}; $G$ not read), and Poisson's law measured &",
        "Newton's inverse square closed after a detector (the equivalence measured, the scale symmetry consistent, series D3, Table~\\ref{tab:checks}; $G$ not read), and Poisson's law measured &",
    ),
    (
        "page count: Table 4's Lorentz cell",
        "against the same pins; their entry into the law in hand (the owner's word of 2026-09-22), the runs off the one axis pending, nothing claimed until they land \\\\",
        "against the same pins, their entry into the law in hand (the owner's word of 2026-09-22), the off-axis runs pending \\\\",
    ),
    (
        "page count: Table 4's masses cell",
        "The values of the masses: every rule is linear in the content, so every equal split is a fixed point; the law gives floors only &",
        "The masses' values: every rule is linear in the content, so every equal split is a fixed point; the law gives floors only &",
    ),
    (
        "page count: Table 4's harmonic cell",
        "The harmonic constants of the click (the axioms admit every Galois conjugate); the circle read as position, its transform as momentum (a hypothesis, Section~\\ref{sec:measurement}) &",
        "The click's harmonic constants (the axioms admit every Galois conjugate); the circle as position, its transform as momentum (a hypothesis, Section~\\ref{sec:measurement}) &",
    ),
    (
        "page count: Table 4's Newton cell, the detail in Section 4 and Table 2",
        "Newton's inverse square closed after a detector (the equivalence measured, the scale symmetry consistent, series D3, Table~\\ref{tab:checks}; $G$ not read), and Poisson's law measured &",
        "Newton's inverse square and Poisson's law closed after a detector ($G$ not read; series D3, Table~\\ref{tab:checks}) &",
    ),
    (
        "page count: Table 4's masses cell, shorter",
        "The masses' values: every rule is linear in the content, so every equal split is a fixed point; the law gives floors only &",
        "The masses' values: every rule is linear in the content, every equal split a fixed point; floors only &",
    ),
    (
        "page count: Table 4's harmonic cell, shorter",
        "The click's harmonic constants (the axioms admit every Galois conjugate); the circle as position, its transform as momentum (a hypothesis, Section~\\ref{sec:measurement}) &",
        "The click's harmonic constants (the axioms admit every Galois conjugate); the circle as position (a hypothesis, Section~\\ref{sec:measurement}) &",
    ),
    # The owner's word on the title (2026-09-22, through the Boss: "A, go"):
    # the word that separates the law, local, from its read-out, the click,
    # non-local, goes into candidate 3's frame; the abstract's first sentence
    # says the same. With it, the writer's re-read of the five: the ports'
    # offers without the direction's letter, the birth wheel named as the
    # paper names it, Q in the symbols table, the Gleason sentence whole.
    (
        "the title: the law local, its read-out non-local",
        "\\title{Universe24: a local integer law of nature and what follows from it}",
        "\\title{Universe24: a local integer law of nature with a non-local read-out, and what follows from it}",
    ),
    (
        "the abstract's first sentence with the title",
        "and one comparison, the click, is its only read-out.",
        "and one comparison, the click, the one non-local step, is its only read-out.",
    ),
    (
        "row 2b: the ports' offers, not the direction's letter",
        "the criterion the offers' visibility $(D_1 - D_2)/(D_1 + D_2)$ of \\texttt{mz\\_equal}, no apparatus model",
        "the criterion the visibility $(b - d)/(b + d)$ of the bright and dark ports' offers of \\texttt{mz\\_equal}, no apparatus model",
    ),
    (
        "row 2a: the birth wheel as the paper names it",
        "(the golden-rate wheel, $4096$ births under the exact phase; L2b)",
        "(the birth wheel, $4096$ births; L2b)",
    ),
    (
        "the symbols table: Q",
        "$\\lambda$, $\\psi_r$, $\\theta$ & scalars, an element & a wavelength, the state of the record $r$ in the group ring, an angle \\\\",
        "$\\lambda$, $\\psi_r$, $Q$, $\\theta$ & scalars, an element, a module & a wavelength, the state of the record $r$ in the group ring, the quotient of the rows' module that forgets the age (Theorem~\\ref{th:bijection}), an angle \\\\",
    ),
    (
        "the Gleason sentence whole",
        "the extreme a part in $276$), the norm range of Appendix~\\ref{app:technical} the error bound.",
        "the extreme a part in $276$), and the norm range of Appendix~\\ref{app:technical} is the error bound between the two.",
    ),
    # The owner's word (2026-09-22): the big formula in a frame.
    (
        "the covariant square in a frame",
        "W = E_0^2 + 3\\,\\mathbf p\\cdot\\mathbf p, \\qquad E_0 = N_l N_w M, \\qquad c^2 = 1/3,",
        "\\boxed{\\,W = E_0^2 + 3\\,\\mathbf p\\cdot\\mathbf p, \\qquad E_0 = N_l N_w M, \\qquad c^2 = 1/3\\,}",
    ),
    # The Bell runs on main (PR #759 at b34fe114; the owner's word "B, go"):
    # N = 2048, 8192 and 16384 measured after a detector, the S(N) figure at
    # half the width beside Table 2, the page count paid by duplicated text.
    (
        "Bell measured: Theorem 6's last sentence",
        "and equals $181/64 = 2.828125$ at every power of two from $512$ through $8192$ \\cite{checks}.",
        "and equals $181/64 = 2.828125$ at every power of two from $512$ through $8192$ and $5793/2048 = 2.828613$ at $16384$ \\cite{checks}; measured after a detector at $512$, $1024$, $2048$, $4096$, $8192$ and $16384$ \\cite{register} (Figure~\\ref{fig:sofn}).",
    ),
    (
        "Bell measured: the proof's 16384",
        "$5793/2048 = 2.828613$ at $16384$ and $32768$, where the second pair of settings rounds to $2893/4096$",
        "$5793/2048 = 2.828613$ at $16384$ and $32768$ (measured at $16384$: $S\\Nphi = 46344$ \\cite{register}), where the second pair of settings rounds to $2893/4096$",
    ),
    (
        "Bell measured: the prediction paragraph",
        "It was computed in advance, run at $\\Nphi = 512$ and $4096$ under the click and the wheel with every pin met (the register's block of the derivation's 24.4), and re-run by the second runner \\cite{replications}.",
        "It was computed in advance and measured after a detector at $\\Nphi = 512$, $2048$, $4096$, $8192$ and, the plateau's end, $16384$ (Table~\\ref{tab:checks}, the last three on main at \\texttt{b34fe114}; Figure~\\ref{fig:sofn}), under the click and the wheel with every pin met (the register's block of the derivation's 24.4); $512$ and $4096$ were re-run by the second runner \\cite{replications}.",
    ),
    (
        "Bell measured: Table 2's row",
        "$S(\\Nphi)$ & L, the pair at $\\Nphi = 64$, $512$, $1024$, $4096$ & $176/64$; $1448/512$; $2896/1024$; $11584/4096$ & the same, Theorem~\\ref{th:bell} and its closed form \\\\",
        "$S(\\Nphi)$ & L and L6, the pair at $\\Nphi = 64$, $512$, $1024$, $2048$, $4096$, $8192$, $16384$ (the last three on main at \\texttt{b34fe114}) & $176/64$; $1448/512$; $2896/1024$; $5792/2048$; $11584/4096$; $23168/8192$; $46344/16384$ & the same, Theorem~\\ref{th:bell} and its closed form: the plateau $181/64$ and its end $5793/2048$ \\\\",
    ),
    (
        "the S(N) figure at half width beside Table 2",
        "\\end{longtable}} \\paragraph{The comparison with nature.}",
        "\\end{longtable}}\n\n\\begin{figure}[!tb]\n\\begin{minipage}[c]{0.5\\linewidth}\\centering\\includegraphics[width=\\linewidth]{figures/s_of_n.pdf}\\end{minipage}\\hfill\n\\begin{minipage}[c]{0.47\\linewidth}\\caption{\\label{fig:sofn}$S(\\Nphi)$ at the CHSH labels. The curve is the closed form $S(\\Nphi) = 8(c_1 + c_1')/\\Nphi - 4$ computed from the rule at every multiple of $8$ with the tables at $N_t = 256$, a computation \\cite{checks}; the circles are detector readings (DETECTOR) at $\\Nphi = 64$, $512$, $1024$, $2048$, $4096$, $8192$ and $16384$ (series L, L6 and the register's block of the derivation's 24.4, the last three on main at \\texttt{b34fe114}); the inset marks the plateau $181/64$ from $512$ through $8192$ and its end $5793/2048$ at $16384$; the dashed line is $2\\sqrt2$.}\\end{minipage}\n\\end{figure}\n\n\\paragraph{The comparison with nature.}",
    ),
    (
        "Bell measured: the map of results",
        "the click's cells, $S$ at four grains,",
        "the click's cells, $S$ at seven grains,",
    ),
    (
        "Bell measured: the introduction's narrative",
        "whose pattern the closed form then explained through $8192$ and beyond.",
        "whose pattern the closed form then explained; the runs at $2048$, $8192$ and $16384$ met it (Figure~\\ref{fig:sofn}).",
    ),
    # The page count: duplicated text, no claim, no table number.
    (
        "page count: the host layer's sentence",
        "so no Node ever holds both rows, and the coherent sum exists only in the record's ledger \\cite{log}; the GameBoard never reads it, and it is no measurement.",
        "so no Node ever holds both rows \\cite{log}; it is no measurement.",
    ),
    (
        "page count: the reviewer's recomputation is NUMBERS.md's",
        "\\cite{log}); the reviewer also recomputed the marginals from the rows of one registered world at $\\Nphi = 64$ for all 4096 setting pairs, $32/64$ in every pair \\cite{log}.",
        "\\cite{log}).",
    ),
    (
        "page count: the second runner is said in Section 8",
        "its world file and its source fingerprint; a second runner re-ran each registered world from the register and compared bit by bit; and each registered number was then traced back",
        "its world file and its source fingerprint, and each registered number was then traced back",
    ),
    (
        "page count: the lemma's parenthesis",
        "(with $C_K > 0$: for a record born with a nonzero row whose every end is an offer, the offers summed over all its ends are the born row's norm up to the tables' rounding, Theorem~\\ref{th:isometry}; at $C_K = 0$ the engine gathers nowhere, the auditor's rounds 4 and 4b, record 363 \\cite{log})",
        "(with $C_K > 0$, the born row's norm up to the tables' rounding, Theorem~\\ref{th:isometry}; at $C_K = 0$ the engine gathers nowhere, record 363 \\cite{log})",
    ),
    (
        "page count: the introduction's Gleason narrative",
        "came from a click count, $63$ of $64$ births in one channel of an unbalanced splitter, whose window for the click's power, containing $2$, was read back from the built click before the form was proved, a check of the implementation; the exact CHSH function",
        "came from a click count, $63$ of $64$ births in one channel of an unbalanced splitter; the exact CHSH function",
    ),
    (
        "page count: the pace readings are Table 2's",
        "Two registered runs read the pace after a detector. Series Q \\cite{register}: a lamp releasing one row on each of the $290$ primitive directions with $|a| + |b| + |c| \\le 6$, with detectors on the six faces; $290$ of $290$ face clicks landed at the derived interval, Node and face, and the pace read from the clicks is $0.5718$ to $0.5893$ Links per interval (mean $0.5810$; the table's asymptotic $0.5774$ to $0.5818$). Series L7, the cone: a row of $17$ Links on an axis and a row of $24$ Links on the plane diagonal, at the same Euclidean distance to one percent, reached their counters at the same age $29$.",
        "Two registered runs read the pace after a detector (Table~\\ref{tab:checks}): series Q, a lamp releasing one row on each of the $290$ primitive directions with $|a| + |b| + |c| \\le 6$ toward detectors on the six faces, every click at the derived interval, Node and face, the pace $0.5718$ to $0.5893$ Links per interval at finite ages against the table's asymptotic $0.5774$ to $0.5818$; and series L7, the cone, a row of $17$ Links on an axis and a row of $24$ on the plane diagonal, the same Euclidean distance to one percent, at their counters at the same age.",
    ),
    (
        "page count: the ground paragraph repeats the ledger's caption",
        "no single reading of the GameBoard's state is the inverse square; the condition is part of the claim, and a detector run, when made, establishes a lattice-exact claim about the world at hand whose agreement with the continuum's form within the ripple is evidence for the inverse square and not its proof.",
        "no single reading of the GameBoard's state is the inverse square; the condition is part of the claim (the ledger's caption).",
    ),
    (
        "page count: the derived-not-derived summary is the ledger's",
        "the fundamental is what the register reads and what the phase means. Derived: the form, the power and the multiplicity rule; not derived: the harmonic constants; Tsirelson's value as a limit is Theorem~\\ref{th:bell}.",
        "the fundamental is what the register reads and what the phase means.",
    ),
    (
        "page count: Section 8's opening",
        "Three things are kept apart: the checks that the code implements the law, which are computations; the numerical checks of the formulas after a detector, which are measurements of the simulator; and the comparisons with measurements of nature.",
        "Three things are kept apart: the gates on the code, the formulas' checks after a detector, and the comparisons with nature.",
    ),
    (
        "page count: the reading rule's last clause is Section 8's",
        "never compared with nature and never pinned, and none appears in this paper as a check.",
        "never compared with nature and never pinned.",
    ),
    (
        "terminology: the GameBoard, not the board",
        "a number of the board appears nowhere.",
        "a number of the GameBoard's state appears nowhere.",
    ),
    (
        "row 5a: the flight table's pace, series Q's reading at finite ages in Table 2",
        "the pace $0.5774$ to $0.5818$ at $N_l = 64$ (series Q)",
        "the flight table's pace $0.5774$ to $0.5818$ at $N_l = 64$ (series Q within it at finite ages, Table~\\ref{tab:checks})",
    ),
    (
        "page count: the gate review's parenthesis is the log's",
        "(computed from the rule, \\cite{checks}; the gate review found none at $64$, $256$, $1024$ and at $4096$ for $a = 0, 1024$, \\cite{log}).",
        "(computed from the rule \\cite{checks}).",
    ),
    (
        "page count: the gathered record's afterthought",
        "A row of a gathered record that reached a set afterwards would offer nothing; no reported world has one, since completion needs every row ended. A set that reads",
        "A set that reads",
    ),
    (
        "page count: the hypotheses' sentence, shorter",
        "Everything the program stated beside the law, the hypotheses under their identities, is on the tree \\cite{hypotheses} and claimed nowhere here.",
        "The hypotheses beside the law are on the tree \\cite{hypotheses}, claimed nowhere here.",
    ),
    (
        "page count: the read-out paragraph is Definition 3's",
        "sums the rows' integer phasors per cell through the tables, squares the sums (the one quadratic step of the law, where the Born rule enters, forced in form by Theorem~\\ref{th:gleason} and free in its constants), lays the cells on a ladder by those squared sums, and compares the record's coordinate $u$, the wheel's, with the ladder's rungs; the cell whose rung $u$ falls under is the click, and the record is done.",
        "sums the rows' integer phasors per cell through the tables, squares the sums (the one quadratic step, forced in form by Theorem~\\ref{th:gleason}), lays the cells on a ladder and compares the record's coordinate $u$ with the rungs; the cell whose rung $u$ falls under is the click.",
    ),
    (
        "page count: the single opening's sentence is Section 8's",
        "The single opening (row 10 of the register) carries no number here (Section~\\ref{sec:checks}).",
        "",
    ),
    (
        "page count: the enumeration's parenthesis",
        "records (one phase gives all $64$ roots, a comb of every eighth phase $8$, the equality case). The entropic bound:",
        "records. The entropic bound:",
    ),
    (
        "page count: Planck's row references are the ledger's",
        "relations are identities of the update rules (the derivation's 21.2, rows 51 and 52), with one constant, $h = h_q\\Nphi = h_A$, a constraint on the inputs whose value is an input (24.1, row 25).",
        "relations are identities of the update rules, with one constant, $h = h_q\\Nphi = h_A$, a constraint on the inputs whose value is an input (Table~\\ref{tab:ledger}).",
    ),
    (
        "page count: the choosers' parenthesis",
        "(periods $3$ and $5$ against $\\Nphi = 64$, every bin one birth per $u$, every marginal $32/64$)",
        "(periods $3$ and $5$ against $\\Nphi = 64$)",
    ),
    (
        "page count: the rounding pins are Table 2's",
        "the rounding pins were met before the run ($63/1$ at $\\Nphi = 64$, $31/1$ at $32$, $125/3$ at $128$ for the $(3, 4)$ split);",
        "the rounding pins of the $(3, 4)$ split were met (Table~\\ref{tab:checks});",
    ),
    (
        "page count: the second runner's sentence, shorter",
        "a second runner re-ran the worlds of series L, T and fifteen more from the register at main and compared every field bit by bit \\cite{replications};",
        "a second runner re-ran series L, T and fifteen more worlds bit by bit \\cite{replications};",
    ),
    (
        "page count: the sequential-instrument sentence, shorter",
        "A read, then a rotation of the labels, then a second read, taken as two outcomes in time (a sequential-instrument test), is not modelled: the first read's selector, keyed by the labels at the read, is applied at the gather to the labels as the rotation left them, once (\\cite{engine}, the readings by type).",
        "A read, then a rotation of the labels, then a second read, taken as two outcomes in time, is not modelled: the first read's selector is applied once, at the gather, to the labels as the rotation left them \\cite{engine}.",
    ),
    (
        "page count: the lemma's delay sentence",
        "Every record of the worlds below is of this kind. The world's row carries the completion interval and the last arrival's interval; the delay between them is a delay of the record, not of the GameBoard.",
        "Every record of the worlds below is of this kind; the delay between a record's last arrival and its completion is the record's, not the GameBoard's.",
    ),
    (
        "page count: the norm range is the appendix's",
        "($-351/65536$ to $+361/65536$ per row for the powers of two through $65536$; Appendix~\\ref{app:technical})",
        "(Appendix~\\ref{app:technical})",
    ),
    (
        "page count: the failures' list names Table 3's rows once",
        "The failures are the law's own results: the unslowed clock (4b, and 4a by its pin), the deceleration (3), light unbent (Section~\\ref{sec:delay}, against $1.75$ arcseconds), the weak forms (8a, 8b), the strong ratio (7b), the two-slit visibility by the fan's grain (2a), the phase-form window (1b), the massless neutrino (8c); each refutes the law as declared on its own, and no count of passes weighs against them.",
        "The failures are the law's own results (Table~\\ref{tab:nature}; light unbent is Section~\\ref{sec:delay}'s, against $1.75$ arcseconds): the unslowed clock, the deceleration, light unbent, the weak forms, the strong ratio, the two-slit visibility, the phase-form window, the massless neutrino; each refutes the law as declared on its own, and no count of passes weighs against them.",
    ),
    (
        "page count: the distance paragraph's opening",
        "What is established now is an explicit model with the exact and conditional results above and their numerical checks after a detector. What the broad claim still needs, and the check that would decide each:",
        "What is established is an explicit model with the results above and their checks after a detector; what the broad claim still needs, and the check that decides each:",
    ),
    (
        "page count: Table 4's bending cell",
        "a rule under which a row's wall reads the crowd's age moment (built as a hypothesis with a coefficient that is an input, the six operations giving Newton's half) run against nature's $1.75$ arcseconds",
        "a rule under which a row's wall reads the crowd's age moment (a hypothesis, its coefficient an input, the six operations giving Newton's half) against nature's $1.75$ arcseconds",
    ),
    (
        "page count: Table 4's harmonic cell, the Galois clause in Section 6",
        "The click's harmonic constants (the axioms admit every Galois conjugate); the circle as position (a hypothesis, Section~\\ref{sec:measurement}) &",
        "The click's harmonic constants; the circle as position (a hypothesis, Section~\\ref{sec:measurement}) &",
    ),
    (
        "page count: Table 4's masses cell, shorter still",
        "The masses' values: every rule is linear in the content, every equal split a fixed point; floors only &",
        "The masses' values: every rule linear in the content, every equal split a fixed point; floors only &",
    ),
    (
        "page count: the runs paragraph's last clause is the prediction paragraph's",
        "twelve fail and one is not compared (Table~\\ref{tab:nature}); each failure refutes the law as declared.",
        "twelve fail and one is not compared (Table~\\ref{tab:nature}).",
    ),
    (
        "page count: Table 4's Newton check cell",
        "a face detector's count of the escape against the release; the clock's form at more distances (series T's method) \\\\",
        "a face detector's count of the escape against the release; the clock's form at more distances \\\\",
    ),
    (
        "page count: the positioning paragraph's asides",
        "no-signalling is Theorem~\\ref{th:marginals}, as it is a theorem of quantum mechanics \\cite{grw1980}.",
        "no-signalling is Theorem~\\ref{th:marginals} \\cite{grw1980}.",
    ),
    (
        "page count: the lattice gas clause",
        "\\cite{hpp1976,fhp1986} with the click's reading of one record added, a walker",
        "\\cite{hpp1976,fhp1986}, a walker",
    ),
    (
        "page count: the earlier testbed, one clause",
        "The earlier testbed of this program \\cite{paper1} is history: no rule of it survives here.",
        "The earlier testbed \\cite{paper1} is history: no rule of it survives here.",
    ),
    (
        "page count: the closed form clause of the proved list",
        "the CHSH sum as an exact function of the grain and the tables, with its closed form;",
        "the CHSH sum as an exact function of the grain and the tables;",
    ),
    # The framing (the owner's records 762, 768 and 773, 2026-09-22): Inside
    # and Outside, the read-out the frame's assumption (P11), the clicks
    # recovering known forms, the click theorem's three sentences (the
    # derivation mathematician's, section 0 of the click frame at its merge)
    # and the writer's paragraph; the limits paragraph's first two sentences
    # and Table 4's Lorentz row replaced; the page count paid by duplicated
    # text carrying no claim and no table number.
    (
        "framing: the title",
        "\\title{Universe24: a local integer law of nature with a non-local read-out, and what follows from it}",
        "\\title{Universe24: a local integer law inside the GameBoard, a non-local read-out above it, and what the clicks recover of nature}",
    ),
    (
        "framing: the abstract's first sentences",
        "One update law of bounded integers, applied at every Node of a cubic GameBoard at every interval, is stated as one map with a rate and a wall per component; its rates and walls are made of six integer operations, and one comparison, the click, the one non-local step, is its only read-out. The paper asks how much of physics that map forces with few assumptions, and answers in one ledger, result by result.",
        "Inside a cubic GameBoard one update law of bounded integers propagates records as a beam by algebraic formulas at every Node and interval: one map with a rate and a wall per component, its rates and walls made of six integer operations. Outside, the game above the board, there are detectors and their clicks only, and the beam passes to them with amplitudes at one comparison, the click, the one non-local step and the only read-out; the paper assumes the GameBoard is read in no other way (P11). Inside, the law's consequences are derived and need no experiment; Outside, the clicks recover known forms and are compared with known experiments, result by result, in one ledger, and the paper shows how far Outside represents reality.",
    ),
    (
        "framing: the abstract's Lorentz factor",
        "What no rule forces is said in the same ledger: the Lorentz factor, the bending of light,",
        "What no rule forces is said in the same ledger: the Lorentz factor (how the clicks arrive at it is the frame), the bending of light,",
    ),
    (
        "framing: P11 after P10",
        "and the harmonic constants are not derived. Nothing outside this list is assumed.",
        "and the harmonic constants are not derived. One assumption of the frame (P11): the GameBoard, Inside, is read only through its emitters and detectors, Outside; every result Outside is a click, a number of the board's state is never a reading, and every comparison with experiment is a comparison of clicks with readings; a measurement is itself an event of the board, an emitter putting a record on it and a detector ending the record at the click, the one step that deletes Inside and the one row that Outside gains. Nothing outside this list is assumed.",
    ),
    (
        "framing: the reading rule names P11 and the physics names",
        "Only a detector's reading is a measurement: a click, a record's moments or an external thing's reading, as the world file declares.",
        "Only a detector's reading is a measurement (the frame's assumption, P11): a click, a record's moments or an external thing's reading, as the world file declares. Every physics name in this paper (Gauss's, Newton's, Coulomb's, Born's, Planck's, Tsirelson's) names the known form that the law's result recovers, Inside by derivation or Outside at a detector.",
    ),
    (
        "framing: the claim paragraph, produced -> recovered",
        "several different physical phenomena are produced from this one discrete update law and a small number of assumptions:",
        "the forms of several different physical phenomena are recovered from this one discrete update law and a small number of assumptions, Inside by derivation and Outside at the clicks:",
    ),
    (
        "framing: the claim paragraph, describes -> represents, and the frame's last sentence",
        "What can be established now is an explicit model, a set of exact and conditional mathematical results, and numerical checks after a detector; the broad claim that the model describes nature still needs the completions Section~\\ref{sec:discussion} names, and the paper is built around the precise distance between the two.",
        "What can be established now is an explicit model, exact and conditional results and checks after a detector; the broad claim that Outside represents nature still needs the completions Section~\\ref{sec:discussion} names, and the paper is built around the distance between the two.",
    ),
    (
        "framing: Definition 3 recovers the Born rule's form",
        "Definition~\\ref{def:click} \\emph{is} the Born rule: the weight is",
        "Definition~\\ref{def:click} recovers the Born rule's form: the weight is",
    ),
    (
        "framing: Section 8's opening states the rule",
        "Three things are kept apart: the gates on the code, the formulas' checks after a detector, and the comparisons with nature.",
        "Three things are kept apart: the gates on the code; what is shown Inside by algebra under named assumptions, which needs no experiment; and what is measured, a run Inside read Outside, compared with known experiments.",
    ),
    (
        "framing: the proved paragraph opens on the spine",
        "\\paragraph{What is proved.} Exact on the GameBoard:",
        "\\paragraph{What is proved.} A packet moved Inside, from place to place, and what it says Outside: every formula below is the answer for one packet. Derived Inside, exact on the GameBoard, no experiment needed:",
    ),
    (
        "framing: recovered in the limit",
        "In the limit of the grain, with a rate: Born's rule",
        "Recovered in the limit of the grain, with a rate: Born's rule",
    ),
    (
        "framing: recovered under the average",
        "In the limit under an average that covers the shell, with the condition in the claim: Newton's",
        "Recovered under an average that covers the shell, with the condition in the claim: Newton's",
    ),
    (
        "framing: the boost sentence of Section 3",
        "Lorentz's symmetry is not a symmetry of the GameBoard but of the limit of its linear block, the wave equation at $c$ (Section~\\ref{sec:discussion}).",
        "Lorentz's symmetry is not a symmetry of the GameBoard but of its clicks Outside, to second order in the velocity, the lattice's corrections from the fourth (Section~\\ref{sec:discussion}).",
    ),
    (
        "framing: the c-postulate row and (A1)",
        "not forced by the six operations: a dispersive flight passes every requirement (the derivation's 27)",
        "not forced by the six operations: a dispersive flight passes every requirement (the derivation's 27); (A1) of the frame asks the same of the clicks",
    ),
    (
        "framing: row 4b's verdict",
        "for the pinned $0.369 \\pm 0.003$ (series S), the law's row stays FAIL \\\\",
        "for the pinned $0.369 \\pm 0.003$ (series S), the law's row stays FAIL; the two one-way factors apart by $1 - v^2$ (the frame) \\\\",
    ),
    (
        "framing: the frame's paragraph before the limits paragraph",
        "\\end{longtable}} \\paragraph{The limits, and what does not return.}",
        "\\end{longtable}}\n\n\\paragraph{Inside and Outside, and how a click arrives at Lorentz.} A packet moved Inside, from place to place, and the question what it says Outside: inside the GameBoard the law propagates records as a beam by the algebraic formulas of Section~\\ref{sec:law}, on Nodes, integer rows and the interval's count, where no one measures; Outside, the game above the board, there are detectors and their clicks only, and the beam passes to them with amplitudes at the click (P11). A detector's clock is what it emits and receives back, on its own record (a detector at rest receives its row back at its own Node); no Node holds a detector's time; a detector without a body, an open face, has no clock of its own, its tick the record's ordering, a GameBoard diagnostic; a velocity is Nodes apart over counts apart between neighbouring detectors, never a reading of the interval, and the read-out of Definition~\\ref{def:click} is the click. The frame's three sentences, the derivation's \\cite{clickframe}: ``To convert the lattice and the momentum inside it into motion Outside, the game above the board, one uses clicks that pass information, a click being the passage of information from Node to Node at most one Node per interval (A1) and its content an amplitude with a phase that splits each interval between staying and hopping, the mass the staying share (A2); Lorentz of the world is assumed, and what is shown is that this conversion brings it. The symmetry of the conversion, the transformations between click families that preserve (A1) and (A2), is the Lorentz group up to scale, acting on the amplitudes of the passing packet as the Dirac walk's covariance, so that the passage of clicks is Lorentz up to corrections of order $m^2 v^2$, exact in the continuum limit, a detector's own rate $\\sqrt{1 - v^2}\\,(1 - \\kappa^2/6)$ with the mass angle $m$ the spacing over the reduced Compton wavelength; in three dimensions the lattice's anisotropy begins at the fourth order. The conversion is made exactly with the amplitudes, converting the packet that passes, and it comes out from there; the law as built satisfies (A1) and not (A2).'' (A1) and the one line, the relativity of the two directions ($k_{AB} = k_{BA}$), are special relativity's two postulates in the click language, so what is arrived at is Einstein's road walked on clicks, and what the board adds is (A2), the amplitudes that carry $\\sqrt{1 - v^2}$ into a detector's own rate, up to corrections of order $m^2 v^2$. The law as built meets (A1), one Node per interval with the flight blind to the phase (P9), and not (A2), its hop a whole-record schedule with no staying amplitude; so its clicks carry the group and its counter runs at the rest rate at every speed, the Doppler $1 + \\beta$ without the clock's factor (rows 4a, 4b): read through records, the two one-way Doppler factors are $r/(1 - v)$ and $(1 + v)/r$, alike only at $r^2 = 1 - v^2$, and the law's $r = 1$ leaves them apart by $1 - v^2$, the measurable that decides. No wall of the law and no declared identity enter the reading; Eq.~\\eqref{eq:square} is an Inside formula on the record, read by no detector, whose Outside formulas the conversion gives. What the system gives is a computation Inside whose passage Outside is the clicks, at the quantum level as well: the equations Inside are the law's, the equation of the passage is the click theorem's, and how far Outside represents reality is what Tables~\\ref{tab:checks} and~\\ref{tab:nature} show, result by result.\n\n\\paragraph{The limits, and what does not return.}",
    ),
    (
        "framing: the limits paragraph's first two sentences replaced",
        "The GameBoard and its interval are a rest frame, and Lorentz invariance is not a limit of the model but a property it must show or lack: the law as declared predicts a body's counter at the rest rate at every speed and the Doppler $1 + \\beta$ without the clock's factor, falsifiable rows (4a, 4b); the owner's decision (record 270 \\cite{log}) keeps that prediction and builds the covariant readings beside it as a hypothesis against the same pins, in its one-axis domain: a body's record carries the exact square of its energy,",
        "The covariant readings (record 270 \\cite{log}) read one Inside formula Outside on one axis, series S against its pins: a body's record carries the exact square of its energy,",
    ),
    (
        "framing: Table 4's Lorentz row on the frame's measurable",
        "The Lorentz factor: no rule of the six reads a body's momentum into its clock, and a boost is not among the $48$ & the muon in flight under the law (row 4a, a pin: the counter at the rest rate); beside the law, the covariant readings (Eq.~\\eqref{eq:square}; series S's face clicks inside their pins on one axis) against the same pins, their entry into the law in hand (the owner's word of 2026-09-22), the off-axis runs pending \\\\",
        "The Lorentz factor: the law meets (A1) and not (A2) & the ratio of the two one-way Doppler factors read at the ground through records: $1 - v^2$ under the law, $1$ under Lorentz; the split of a row between staying and hopping (A2) as a hypothesis under its own identity, not opened \\\\",
    ),
    (
        "framing: the click frame's bibitem",
        "\\bibitem{derivations} The derivations of the beam law, \\texttt{docs/DERIVATIONS\\_BEAM.md} of the archived code \\cite{zenodo}.",
        "\\bibitem{derivations} The derivations of the beam law, \\texttt{docs/DERIVATIONS\\_BEAM.md} of the archived code \\cite{zenodo}.\n\\bibitem{clickframe} Lorentz from the clicks: the click frame, its section 0 the click theorem, \\texttt{docs/designs/click\\_frame/DERIVATION.md} of the archived code \\cite{zenodo}, at 1dd81fef (PR \\#769, pending merge).",
    ),
    # The page count: duplicated text, no claim, no table number.
    (
        "framing, page count: the introduction's narrative to its rule",
        "The lattice Gleason theorem (Section~\\ref{sec:measurement}) came from a click count, $63$ of $64$ births in one channel of an unbalanced splitter; the exact CHSH function $S(\\Nphi)$ (Section~\\ref{sec:bell}) came from three registered values, $176/64$, $2896/1024$ and $11584/4096$, whose pattern the closed form then explained; the runs at $2048$, $8192$ and $16384$ met it (Figure~\\ref{fig:sofn}). Where a derivation closed,",
        "Where a derivation closed,",
    ),
    (
        "framing, page count: the mixture sentence",
        "a mixture is a different law, the flat mixture being the phase-blind detector $R(f) = \\sum_{p < \\Nphi/2} f_p^2$ on the reduced basis $1, x, \\dots, x^{\\Nphi/2-1}$, which satisfies (a), (b), (c) exactly. The algebra admits the phase-blind detector; what excludes it",
        "a mixture is a different law, the flat mixture being the phase-blind detector, which satisfies (a), (b), (c) exactly; what excludes it",
    ),
    (
        "framing, page count: Section 8's gate clauses",
        "the engine's inverse interval returns a world without a measured event to its birth; the rounding pins",
        "the rounding pins",
    ),
    (
        "framing, page count: the optical-v1 sentence is Table 4's",
        "A rule under which the rows read the crowd's age moment (optical-v1) is a hypothesis beside the law, designed and reviewed, not built; the equivalence principle holds",
        "The equivalence principle holds",
    ),
    (
        "framing, page count: the preferred party is Definition 3's",
        "Which party is first is the world file's declaration of the arms' order, not a property of the GameBoard: the model has a preferred party by declaration, and swapping the arms moves outcomes between the parties while the counts stay \\cite{log}.",
        "",
    ),
    (
        "framing, page count: the positioning paragraph's Bohm and psi-ontic clauses",
        "the uniform $u$ and the ruler do the work of quantum equilibrium in Bohm's theory \\cite{bohm1952,dgz1992}; the model is $\\psi$-ontic in the classification of \\cite{spekkens2007,hs2010}; Theorem",
        "the uniform $u$ does the work of quantum equilibrium \\cite{bohm1952,dgz1992}; the model is $\\psi$-ontic \\cite{spekkens2007,hs2010}; Theorem",
    ),
    (
        "framing, page count: the claim paragraph's middle",
        "The three things work together: the formula defines the mechanism, the derivations show what follows and under what conditions, the simulator and the comparison with experiment check the results and their limits. What can be established",
        "What can be established",
    ),
    (
        "framing, page count: the code paragraph's last sentence",
        "A world file declares the parameters and the initial conditions and nothing of the rules; the same engine runs every world of this paper.",
        "The same engine runs every world of this paper from its world file.",
    ),
    (
        "framing, page count: the host paragraph's last clause",
        "so no Node ever holds both rows \\cite{log}; it is no measurement.",
        "so no Node ever holds both rows \\cite{log}.",
    ),
    (
        "framing, page count: Kennard's sentence",
        "Kennard's variance form $\\Delta x\\,\\Delta p \\ge \\hbar/2$ \\cite{kennard1927,robertson1929} follows, as is well known, by the Cauchy--Schwarz argument on the Gram form of Theorem~\\ref{th:gleason} in the limit $\\Nphi \\to \\infty$ of a record spread over many phases, with $\\hbar = h/(2\\pi) = h_q\\Nphi/(2\\pi)$; at finite $\\Nphi$ the bound is the finite group's and the Gaussian equality case does not exist on $\\Z_{\\Nphi}$.",
        "Kennard's variance form $\\Delta x\\,\\Delta p \\ge \\hbar/2$ \\cite{kennard1927,robertson1929} follows by Cauchy--Schwarz on the Gram form of Theorem~\\ref{th:gleason} in the limit $\\Nphi \\to \\infty$, with $\\hbar = h/(2\\pi) = h_q\\Nphi/(2\\pi)$; at finite $\\Nphi$ the bound is the finite group's.",
    ),
    (
        "framing, page count: the uncertainty's last sentence",
        "What makes it an uncertainty and not a spread is the one read-out: a record read at a Node gives its position and erases its phase vector, a record read on the fan's angle gives its momentum's direction and not the Node it came from, and the two are not jointly readable for the same reason the law has no joint distribution for Bell (Theorem~\\ref{th:bell}).",
        "What makes it an uncertainty and not a spread is the one read-out: read at a Node a record gives its position and loses its phase, read on the fan's angle it gives its momentum's direction and not its Node, and the two are not jointly readable, as the law has no joint distribution for Bell (Theorem~\\ref{th:bell}).",
    ),
    (
        "framing, page count: Planck's paragraph",
        "Under the declared dictionary the release's cost rule reads as $E = h_q s = (h_q\\Nphi) f$ and the turn rule as $\\lambda = h_A/p$: Planck's and de Broglie's relations are identities of the update rules, with one constant, $h = h_q\\Nphi = h_A$, a constraint on the inputs whose value is an input (Table~\\ref{tab:ledger}). No detector reading of them is registered; the electron's click on a face reads where an orbit ended, not $E = hf$.",
        "Under the declared dictionary the release's cost rule reads as $E = h_q s = (h_q\\Nphi) f$ and the turn rule as $\\lambda = h_A/p$: Planck's and de Broglie's relations are identities of the update rules with one constant, $h = h_q\\Nphi = h_A$, an input (Table~\\ref{tab:ledger}); no detector reading of them is registered.",
    ),
    (
        "framing, page count: the Bell scope sentences",
        "Where the two settings meet is explicit in Definition~\\ref{def:click}: $B$'s rung is computed from $R(o_A, o_B)$ with $a$ and $o_A$ supplied by the layer. That the marginal at $B$ is nevertheless $\\Nphi/2$ for every $a$ is the content of the theorem; the joint counts are not local, and the model does not claim they are.",
        "That the marginal at $B$ is $\\Nphi/2$ for every $a$ although $B$'s rung is computed from $R(o_A, o_B)$ with $a$ and $o_A$ supplied by the layer (Definition~\\ref{def:click}) is the content of the theorem; the joint counts are not local, and the model does not claim they are.",
    ),
    (
        "framing, page count: Theorem 6's proof, the values beyond the tables",
        "(\\cite{checks}; the derivation's 24.4, \\texttt{bell\\_plateau.py}, the same values): $11585/4096 = 2.828369$ at $65536$, $46341/16384 = 2.828430$ at $131072$ and $370727/131072 = 2.828423$ at $2^{20}$, two-sided about the bound; with the",
        "(\\cite{checks}; the derivation's 24.4, the same values): $11585/4096 = 2.828369$ at $65536$ and $370727/131072 = 2.828423$ at $2^{20}$, two-sided about the bound; with the",
    ),
    (
        "framing, page count: the uniform birth phase's run clause",
        "which is how every run below is made (one birth per $u$), and its independence of the settings",
        "(one birth per $u$ in every run below), and its independence of the settings",
    ),
    (
        "framing, page count: the marginals theorem's list of grains",
        "No tie occurs for any setting pair at $\\Nphi = 8, 16, 24, 32, 48, 64, 96, 128, 192, 256, 512, 1024$, nor at the CHSH labels for any multiple of $8$ up to $4096$ (computed from the rule \\cite{checks}).",
        "No tie occurs for any setting pair at the twelve grains from $8$ to $1024$ of \\cite{checks}, nor at the CHSH labels for any multiple of $8$ up to $4096$.",
    ),
    (
        "framing, page count: the strict-crossing sentence",
        "The strict-crossing rung $\\Nphi C_k > uC_K$ gives the second party $33/64$ in $3944$ of the $4096$ setting pairs at $\\Nphi = 64$, a signalling of $1/\\Nphi$ made by the rounding \\cite{design}; the nearest rung of \\eqref{eq:rung} is what Theorem~\\ref{th:marginals} needs.",
        "The strict-crossing rung $\\Nphi C_k > uC_K$ would give the second party $33/64$ in $3944$ of the $4096$ setting pairs at $\\Nphi = 64$, a signalling of $1/\\Nphi$ made by the rounding \\cite{design}; the nearest rung is what the theorem needs.",
    ),
    (
        "framing, page count: Table 3's caption",
        "Three PASS (each replicated by the second runner \\cite{replications}) and a fourth under the clock's assumed word (row 12); twelve FAIL: seven in a registered run, four by a pin without its run (not in this table), one a declared input refuted by nature (8c); two BOUND (5a; 7a on a declared input); one NOT COMPARED (2c).",
        "Three PASS (replicated \\cite{replications}), a fourth under the clock's assumed word (12); twelve FAIL (seven in a registered run, four by a pin without its run and not in this table, one a declared input refuted, 8c); two BOUND (5a, 7a); one NOT COMPARED (2c).",
    ),
    (
        "framing, page count: row 4b's verdict, shorter",
        "FAIL: $0.315$ expected, $17$ grains below; under covariant-readings-v1 the same star reads $0.3674$ for the pinned $0.369 \\pm 0.003$ (series S), the law's row stays FAIL; the two one-way factors apart by $1 - v^2$ (the frame) \\\\",
        "FAIL: $0.315$ expected, $17$ grains below; under covariant-readings-v1 $0.3674$ for the pinned $0.369 \\pm 0.003$ (series S), the law's row FAIL; the frame: the two one-way factors apart by $1 - v^2$ \\\\",
    ),
    (
        "framing, page count: row 12's limit clause is Table 2's",
        "the presence clock $1.000$; the continuum's $1/r$ a limit under the shell's average &",
        "the presence clock $1.000$ &",
    ),
    (
        "framing, page count: the spine said once, in the frame's paragraph",
        "\\paragraph{What is proved.} A packet moved Inside, from place to place, and what it says Outside: every formula below is the answer for one packet. Derived Inside, exact on the GameBoard, no experiment needed:",
        "\\paragraph{What is proved.} Derived Inside, exact on the GameBoard, no experiment needed, each the answer for one packet moved from place to place:",
    ),
    (
        "framing, page count: the frame paragraph's closing sentence",
        "What the system gives is a computation Inside whose passage Outside is the clicks, at the quantum level as well: the equations Inside are the law's, the equation of the passage is the click theorem's, and how far Outside represents reality is what Tables~\\ref{tab:checks} and~\\ref{tab:nature} show, result by result.",
        "What the system gives is a computation Inside whose passage Outside is the clicks, at the quantum level as well, the equations Inside the law's and the equation of the passage the click theorem's; how far Outside represents reality is what Tables~\\ref{tab:checks} and~\\ref{tab:nature} show, result by result.",
    ),
    (
        "framing, page count: the detector at rest, a parenthesis",
        "A detector's clock is what it emits and receives back, on its own record (a detector at rest receives its row back at its own Node); no Node holds",
        "A detector's clock is what it emits and receives back, on its own record; no Node holds",
    ),
    (
        "framing, page count: the earlier testbed in five words",
        "The earlier testbed \\cite{paper1} is history: no rule of it survives here.",
        "The earlier testbed \\cite{paper1} is history.",
    ),
    (
        "framing, page count: row 2c, shorter",
        "from the click cells, a read-back of the built click, which carries the square & NOT COMPARED ($\\kappa$ not computed): the window a gate on the implementation, no evidence about nature; no three-opening world is registered \\\\",
        "from the click cells, a read-back of the built click & NOT COMPARED ($\\kappa$ not computed): the window an implementation gate, no evidence about nature; no three-opening world is registered \\\\",
    ),
    (
        "framing, page count: the proximity sentence",
        "The proximity is a compatibility, not an advantage over quantum mechanics, whose bound the law approaches from below on this range; what refutes it",
        "The proximity is a compatibility, not an advantage over quantum mechanics; what refutes it",
    ),
    (
        "framing, page count: the proved list's two clauses",
        "the split's isometry and the injectivity of the interval on the rows' weights, multiplicities and phases for a fixed event history; the pace of every direction, isotropic within $1/T_D$, with its Manhattan bound;",
        "the split's isometry and the injectivity of the interval on the amplitudes for a fixed event history; the pace of every direction, isotropic within $1/T_D$;",
    ),
    (
        "framing, page count: the runs paragraph in one sentence",
        "each inside an expectation written before the run; nothing of the GameBoard's state is read as a measurement. Against nature three readings pass,",
        "each inside an expectation written before the run, nothing of the GameBoard's state among them; against nature three readings pass,",
    ),
    (
        "framing, page count: Table 4's Newton check, shorter",
        "a face detector's count of the escape against the release; the clock's form at more distances \\\\",
        "the escape's count at a face detector; the clock's form at more distances \\\\",
    ),
    (
        "framing, page count: the limits paragraph's E' clause",
        "compared and never rooted, with $E'$ the largest integer whose square is at most $W$, kept by comparisons, and every count of the body gated by $E_0/E'$; multiplied by $c^4$ it is the energy--momentum relation of special relativity, and the identity's own content is the integer form (series S, Table~\\ref{tab:checks}, inside their pins).",
        "compared and never rooted, with $E'$ the largest integer whose square is at most $W$ and every count of the body gated by $E_0/E'$; multiplied by $c^4$ it is the energy--momentum relation of special relativity (series S, Table~\\ref{tab:checks}, inside their pins).",
    ),
    (
        "framing, page count: the frame paragraph's velocity clause",
        "a velocity is Nodes apart over counts apart between neighbouring detectors, never a reading of the interval, and the read-out of Definition~\\ref{def:click} is the click. The frame's three sentences, the derivation's \\cite{clickframe}:",
        "a velocity is Nodes apart over counts apart between neighbouring detectors, and the read-out of Definition~\\ref{def:click} is the click. The frame \\cite{clickframe}:",
    ),
    (
        "framing, page count: the rest rate clause",
        "so its clicks carry the group and its counter runs at the rest rate at every speed, the Doppler $1 + \\beta$ without the clock's factor (rows 4a, 4b): read through records,",
        "so its clicks carry the group and its counter runs at the rest rate at every speed (rows 4a, 4b): read through records,",
    ),
    (
        "framing, page count: the proved paragraph's opening, shorter",
        "\\paragraph{What is proved.} Derived Inside, exact on the GameBoard, no experiment needed, each the answer for one packet moved from place to place:",
        "\\paragraph{What is proved.} Derived Inside, exact on the GameBoard, no experiment needed:",
    ),
    (
        "framing, page count: Table 4's harmonic check, shorter",
        "the least-rank click, an axiom of the apparatus, pinned by the two-slit period and Malus at $22.5$ degrees, not derived; the identification by the single opening against its pin (row 10) \\\\",
        "the least-rank click, an axiom of the apparatus pinned by the two-slit period and Malus at $22.5$ degrees; the single opening against its pin (row 10) \\\\",
    ),
    (
        "framing, page count: row 12's verdict, shorter",
        "PASS under the age word, the clock's word by assumption (P9), nature's $2.00$ $4.6$ percent away; FAIL under the presence word",
        "PASS under the age word (P9), nature's $2.00$ $4.6$ percent away; FAIL under the presence word",
    ),
    (
        "framing, page count: row 4b's reading, shorter",
        "(series G2, before the crossing rule; the re-run at head pending)",
        "(series G2; the re-run at head pending)",
    ),
    (
        "framing, page count: the prediction's three assumptions in fewer words",
        "(that nature's pairs are this model's pairs at some $\\Nphi$, that fair sampling holds, and that the experiment's four settings are the model's labels)",
        "(nature's pairs this model's pairs at some $\\Nphi$, fair sampling, the four settings the model's labels)",
    ),
    (
        "framing, page count: Table 4's masses cell in two lines",
        "The masses' values: every rule linear in the content, every equal split a fixed point; floors only &",
        "The masses' values: every rule linear in the content, every equal split a fixed point &",
    ),
    (
        "framing, page count: the open face in fewer words",
        "a detector without a body, an open face, has no clock of its own, its tick the record's ordering, a GameBoard diagnostic;",
        "an open face, without a body, has no clock, its tick the record's ordering (a GameBoard diagnostic);",
    ),
    (
        "framing, page count: Table 4's Lorentz check in two lines",
        "the ratio of the two one-way Doppler factors read at the ground through records: $1 - v^2$ under the law, $1$ under Lorentz; the split of a row between staying and hopping (A2) as a hypothesis under its own identity, not opened \\\\",
        "the ratio of the two one-way Doppler factors through records: $1 - v^2$ under the law, $1$ under Lorentz; the split of a row between staying and hopping (A2), a hypothesis not opened \\\\",
    ),
    (
        "framing, page count: the runs paragraph in two lines",
        "After a detector the simulator reads what Table~\\ref{tab:checks} lists, each inside an expectation written before the run, nothing of the GameBoard's state among them; against nature",
        "After a detector the simulator reads Table~\\ref{tab:checks}'s list, each inside an expectation written before the run; against nature",
    ),
    (
        "framing, page count: Planck's clause in the proved list",
        "Planck's and de Broglie's relations as identities under the declared dictionary, an input.",
        "Planck's and de Broglie's relations as identities under the declared dictionary.",
    ),
    (
        "framing, page count: the frame paragraph's first clause",
        "and the question what it says Outside: inside the GameBoard the law propagates records as a beam",
        "and the question what it says Outside: Inside, the law propagates records as a beam",
    ),
    (
        "framing, page count: Table 4's Newton cell in two lines",
        "Newton's inverse square and Poisson's law closed after a detector ($G$ not read; series D3, Table~\\ref{tab:checks}) &",
        "Newton's inverse square and Poisson's law closed after a detector ($G$ not read; D3) &",
    ),
    (
        "framing, page count: the positioning paragraph's transport clause",
        "the transport is a lattice gas's exact integer dynamics \\cite{hpp1976,fhp1986}, a walker free of dispersion where the lattice automata of",
        "the transport a lattice gas's exact integer dynamics \\cite{hpp1976,fhp1986}, free of dispersion where the lattice automata of",
    ),
    (
        "framing, page count: the axioms clause of the proved list",
        "the click's weight a positive quadratic form of power $2$ under the axioms (a) to (e); the exact marginals",
        "the click's weight a positive quadratic form of power $2$; the exact marginals",
    ),
    (
        "framing, page count: the beam clause of the frame paragraph",
        "there are detectors and their clicks only, and the beam passes to them with amplitudes at the click (P11).",
        "there are detectors and their clicks only, the beam passing to them with amplitudes at the click (P11).",
    ),
    (
        "framing, page count: the hypotheses' sentence in five words",
        "The hypotheses beside the law are on the tree \\cite{hypotheses}, claimed nowhere here.",
        "The hypotheses beside the law are on the tree \\cite{hypotheses}.",
    ),
    (
        "framing, page count: the frame paragraph's opening clause",
        "and the question what it says Outside: Inside, the law propagates records as a beam by the algebraic formulas of Section~\\ref{sec:law}, on Nodes, integer rows and the interval's count, where no one measures;",
        "and what it says Outside: Inside, the law propagates records as a beam by the algebraic formulas of Section~\\ref{sec:law}, where no one measures;",
    ),
    (
        "framing, page count: the Doppler factors' clause",
        "the two one-way Doppler factors are $r/(1 - v)$ and $(1 + v)/r$, alike only at $r^2 = 1 - v^2$,",
        "the two one-way Doppler factors $r/(1 - v)$ and $(1 + v)/r$ are alike only at $r^2 = 1 - v^2$,",
    ),
    (
        "framing, page count: the distance paragraph's first clause is the introduction's",
        "What is established is an explicit model with the results above and their checks after a detector; what the broad claim still needs, and the check that decides each:",
        "What the broad claim still needs, and the check that decides each:",
    ),
    (
        "framing, page count: the field equation's sentence is Table 4's scope",
        "(series S, Table~\\ref{tab:checks}, inside their pins). Einstein's field equation is not reached.",
        "(series S, Table~\\ref{tab:checks}, inside their pins).",
    ),
    (
        "framing, page count: the bending row's parenthesis",
        "(a hypothesis, its coefficient an input, the six operations giving Newton's half) against nature's $1.75$ arcseconds",
        "(a hypothesis, its coefficient an input) against nature's $1.75$ arcseconds",
    ),
    (
        "framing, page count: the closing sentence's middle clause",
        "at the quantum level as well, the equations Inside the law's and the equation of the passage the click theorem's; how far Outside represents reality",
        "at the quantum level as well; how far Outside represents reality",
    ),
    (
        "framing, page count: the order clause said once, in the quote",
        "the amplitudes that carry $\\sqrt{1 - v^2}$ into a detector's own rate, up to corrections of order $m^2 v^2$. The law as built meets (A1)",
        "the amplitudes that carry $\\sqrt{1 - v^2}$ into a detector's own rate. The law as built meets (A1)",
    ),
    # Plan B, the reshaping (the owner's GO through the Boss, 08:15Z): the argument, the road, the transition, the step beneath and above, the smallest thing, Newton, the conversion table, the phenomena by formulas, the seven confirmations to Appendix C.
    (
        "the abstract: why, in one clause",
        "the GameBoard is read in no other way (P11).",
        "the GameBoard is read in no other way (P11). Physics above the board is arithmetic on counts and the law beneath it is modern algebra, and the paper says why: the rules put into the cells are, written down, a cyclic group, a group ring, integer matrices, an evaluation at the roots of unity and a shift, and every result is an identity of that algebra, exact on the board or in a named limit, compared with the register's readings by kind.",
    ),
    (
        "the introduction: why physics behaves like modern algebra, five steps",
        "\\paragraph{The claim and the question.} The claim of the paper is that the forms of several different physical phenomena are recovered from this one discrete update law and a small number of assumptions, Inside by derivation and Outside at the clicks: the geometry of propagation, the flux and the forces, and further the measurement and its correlations. The decisive question is how much of that the law really forces. If every phenomenon needed a rule that puts its result in beforehand, the law would explain nothing; if the same rules force several results with little freedom, that is the contribution. So the paper keeps one ledger (Table~\\ref{tab:ledger}): for every result, the rules of Eq.~\\eqref{eq:map} it starts from, the assumptions added beside them with their kind, the freedom left, and the ground on which the derivation stands, exact on the GameBoard, a limit of the grain, or a limit under a spatial condition. What can be established now is an explicit model, exact and conditional results and checks after a detector; the broad claim that Outside represents nature still needs the completions Section~\\ref{sec:discussion} names, and the paper is built around the distance between the two.",
        "\\paragraph{Why physics behaves like modern algebra.} The claim of the paper is that the forms of several different physical phenomena are recovered from this one discrete update law and a small number of assumptions, Inside by derivation and Outside at the clicks, and the reason is stated in five steps that the paper then follows. First, Outside is arithmetic in $\\mathbb Q$: every measured quantity is a count at a click or a ratio of two counts (a velocity is Nodes apart over counts apart; a visibility, a correlation and a redshift are ratios of counts), and nothing measured is a real number. Second, Inside is integer and local: six operations on bounded integers at a Node and its six neighbours, each rule generic, vector and local; written down, the rules put into the cells are the cyclic group of the phase, the group ring of the arrivals, the integer matrices of the split and the rotation, the evaluation at the roots of unity and the translation group's shift, so the state is a free $\\Z$-module and the interval a $\\Z$-linear map on it (Section~\\ref{sec:law}). Third, the couplings are tables, the circle's $C$ and $S$, the split's and the rotation's integer matrices, the family table, and Born's rule is a coupling computed from $\\Nphi$, the rungs of Eq.~\\eqref{eq:rung}, so a click is a comparison of integers. Fourth, the transformations between click families that preserve the passage of information are the Lorentz group up to scale (Section~\\ref{sec:discussion}), so the symmetry Outside has is the algebra's and not a metric put in. Fifth, every result of the paper is therefore an identity of that algebra, checked against the register's readings by kind and not chosen to fit a reading; where a form was declared, the paper says so. The decisive question is how much of that the law really forces: if every phenomenon needed a rule that puts its result in beforehand, the law would explain nothing; if the same rules force several results with little freedom, that is the contribution. So the paper keeps one ledger (Table~\\ref{tab:ledger}): for every result, the rules of Eq.~\\eqref{eq:map} it starts from, the assumptions added beside them with their kind, the freedom left, and the ground on which the derivation stands. What can be established now is an explicit model, exact and conditional results and checks after a detector; the broad claim that Outside represents nature still needs the completions Section~\\ref{sec:discussion} names, and the paper is built around the distance between the two.",
    ),
    (
        "Section 2 opens with the GameBoard as a system of information transfer and the road from the cells to the algebra",
        "\\section{The law and its implementation}\\label{sec:law} \\paragraph{Rules, parameters, initial conditions.}",
        "\\section{The law and its implementation}\\label{sec:law}  \\paragraph{The GameBoard as a system of information transfer.} The GameBoard is a system of information transfer, and its only objects are messages, the rows: a row is a tuple (Node, direction, age, phase, emitter, content per unit, record, label, amount, multiplicity), and a Link is a channel that carries at most one step of a row per interval in each direction. Nothing else exists Inside: no field at a Node, no register, no memory beyond the rows present. Each interval does six things to messages and nothing else: it moves a row one Link along its digital line (the translation), turns its phase (the translation on the circle), splits it at a splitter into rows with integer weights (the multiplication by a declared table), rotates a labelled pair (an integer matrix), merges the rows that meet at a Node with equal words, opposite phases cancelling (the addition), and, at a detector, reads a record once by one comparison and deletes it (the evaluation and the count). The books say that no message is lost or made in transit: released equals in transit plus absorbed plus escaped plus cancelled at every interval. Two messages of this paper: a row on the heading $+x$ crosses its Links at the intervals $1, 3, 5, 7, 8$ (the hand-worked update below), its whole history the closed form of its accumulator and nothing kept at a Node; and at a balanced splitter one row of amount $1$ becomes two of amount $1$ and multiplicity $2$ on two arms, which meet again at a second splitter, at one port with equal phases (the words add) and at the other $\\Nphi/2$ apart (an equal pair is no row, the message cancels), so the detector at the first port reads the record, $64$ of $64$ births, and the dark port is the cancelled message (series L, Section~\\ref{sec:checks}). Written down, a message is a basis element of a free $\\Z$-module, the passage is the translation group's shift, the split and the rotation are integer matrices, the merge is the group ring's addition and the read-out is one bilinear form: the passage from physics to modern algebra is the passage from messages with attributes to vectors with coordinates. The lattice gases \\cite{hpp1976,fhp1986} carry particles as bits on links with collision tables, the cellular automata machines of \\cite{toffoli1987} are lattices of local rules on bits, the quantum cellular automata of \\cite{arrighi2019} are local unitaries on cells, and Shannon's channel \\cite{shannon1948} is the message and its capacity; the GameBoard is of that family, with two differences the paper states: its messages carry a phase on a bounded circle and an integer amount, and its only read-out is the click.  \\paragraph{The road from the cells to the algebra.} How the things of physics entered: the amount $w$ of a row is a positive integer, translated and merged; the phase $p$ is an element of $\\Z_{\\Nphi}$, turned per Link, added in the group ring, evaluated at the roots of unity; the multiplicity $\\mathtt m$ is a positive integer, $A = \\sum a_i^2$ at a split; the age $\\tau$ is a count at the rate $1$; mass is the content $M$, a count of units per family and an input of the family table, which sets the drive's wall $N_l N_w M + |p_a|$ (the division), scales the push's bilinear form and the release rate, and is the rest energy $E_0 = N_l N_w M$; charge is $\\rho$, the declared charge per unit of content, entering only the coupling matrix $\\rho_A\\rho_B$ of the push; momentum is an integer vector, translated by the push, read by the drive as a rate against a wall, its square compared and never rooted; the field a body reads is the label flow $\\mathbf a = \\sum \\mathrm{amount} \\times \\mathbf u_D$, bilinear in the arrivals; the family table (content, cost per phase step, charge, the strong column, lifetime, phase rate, hand) is read and never computed; and the couplings, the circle's tables at $1/256$, the split and rotation tables and the click's Gram matrix, are integer matrices and one bilinear form. So mass is a count that sets a wall and scales a form, charge a declared integer in one matrix, momentum a translated vector whose square is compared, and the six operations are the only operations on them.  \\paragraph{Rules, parameters, initial conditions.}",
    ),
    (
        "the state paragraph's row attributes are the tuple's",
        "A row carries its Node, its direction (a primitive integer vector on whose digital line it walks), its age, its phase on the circle $\\Z_{\\Nphi}$, its number (its family), its amount, its content per unit, and under a record its identity, label, multiplicity and birth phase.",
        "",
    ),
    (
        "the identities of the six operations",
        "loses nothing either, so there is still no third place.",
        "loses nothing either, so there is still no third place. Written as algebra, the six are: the carry a bijection $s \\mapsto (e, s - ed)$; the linear block's closed form $\\lfloor s_0 + rt \\rfloor$, the flight the translation group's shift along the digital line; the split's table with $A = \\sum a_i^2$ inverted by its conjugate transpose (Theorem~\\ref{th:isometry}); the rotation an integer matrix with $U_s^{\\mathsf T}U_s = n_s I$; the merge the addition in $\\Z[\\Z_{\\Nphi}]$, its cancel the quotient by $x^{\\Nphi/2} + 1$, which for $\\Nphi$ a power of two is the ring of cyclotomic integers $\\Z[\\zeta_{\\Nphi}]$, a free $\\Z$-module of rank $\\Nphi/2$; and the click one bilinear form $\\mathbf f^{\\mathsf T}\\mathbf G\\mathbf f$ with $\\mathbf G$ the tables' Gram matrix, then one comparison. Modern algebra is not assumed here; it is what the cell rules are when written down, and every theorem below is a property of these six maps.",
    ),
    (
        "when the transition was made, before the ledger",
        "\\paragraph{The ledger.} Table~\\ref{tab:ledger} is the paper's spine:",
        "\\paragraph{When the transition was made.} The road from ordinary physics to this algebra was walked in twenty-four dated steps, each a thing of physics becoming an object of the law, recorded with the reading that showed it \\cite{history} (Appendix~\\ref{app:reproduction} lists them): on 2026-09-17 the shared quantum resource was deleted and locality held without exception, the amplitude became a phase with a conserved content and Born's rule a declared table; on 09-18 the Born table was computed from $\\Nphi$ and a Node became its six Ports; on 09-19 a quantum became an integer row on a record, the click the one one-way border, the push one bilinear form and charge a rational per unit of content, and $E = hf$ the cost of a release; on 09-20 every force became a column with a sign, the readings became two kinds, the masses the initialisation, every count an accumulator on its reader's own record, the Doppler the count of rows a mover crosses; on 09-21 the whole law became one vector operation of six verbs under three tests, the record an element of $\\Z[\\Z_{\\Nphi}]$ with the weight one bilinear form, the lattice the translation group and $c$ the norm of the flight operator, and the Lorentz factor, a root, was refused as a seventh verb; on 09-22 a detector's clock became a member of the age wall, the click theorem placed the Lorentz group Outside, and the paper's framing, Inside and Outside, was set. \\paragraph{The ledger.} Table~\\ref{tab:ledger} is the paper's spine:",
    ),
    (
        "the ledger's caption: what the algebra shows and what a run measures",
        "\\caption{\\label{tab:ledger}The forcing ledger. Ground:",
        "\\caption{\\label{tab:ledger}The forcing ledger: what the algebra shows, its ground word the rung; what a run measures is Table~\\ref{tab:checks}'s. Ground:",
    ),
    (
        "Section 6: interference by formulas, before the limit",
        "\\paragraph{The limit.} As $\\Nphi = 2^k$ grows",
        "\\paragraph{Interference, by the formulas alone.} Every phenomenon of this paper is read the same way: Outside, what a detector counts; down to Inside, the rows, their phases, the merge and the evaluation; back Outside, the click's counts over the births against the reading. Two slits: one record is born with two rows of amount $1$, one per opening, $\\mathtt m = 2$; each row's phase advances one turn per Link; at pixel $x$ the two arrive with phases $p_1(x)$, $p_2(x)$, their difference $\\Delta(x)$ the path difference times the turn; the merge adds them and an equal pair with $\\Delta = \\Nphi/2$ cancels to no row; the click evaluates the sum and squares it, the offer $R(x) = 512\\,[(C[p_1] + C[p_2])^2 + (S[p_1] + S[p_2])^2] = 1024\\,(65536 + C[p_1]C[p_2] + S[p_1]S[p_2])$ up to the tables' rounding, proportional to $1 + \\cos\\Delta(x)$; the rungs $\\rung_x$ of Eq.~\\eqref{eq:rung} lay the pixels on the ladder, the click is the pixel under which $u$ falls, and over $\\Nphi$ births the count at $x$ is $\\rung_x - \\rung_{x-1}$, Born's to $1/\\Nphi$. What passes: the pixels with $\\Delta$ near $0$, a wide rung. What does not: the pixels with $\\Delta = \\Nphi/2$, the rows cancelled, the offer $0$, a rung of width $0$ where no click can land. One slit: one row per pixel, no pair, nothing cancels, a flat count within the fan's grain, no dark pixel. Mach-Zehnder: the balanced splitter, two arms, the mirrors' turn $\\Nphi/4$, the second splitter; at one port the two phasors add and at the other they are $\\Nphi/2$ apart and cancel; with the tables at $\\Nphi = 64$ the offers are $1681/1682$ and $1/1682$, the rounding and not $1$ and $0$, and the rungs give the bright port $64$ of $64$ clicks and the dark port $0$ (row 2b); the half turn and the quarter turn, $0/64$ and $32/32$, follow by the same lines. The pair (Section~\\ref{sec:bell}), Malus's $219/256$ at $22.5$ degrees from the rotation table, and GHZ's zeros from the joint weights are the same three lines each; the register's runs confirm them (Section~\\ref{sec:checks}). \\paragraph{The limit.} As $\\Nphi = 2^k$ grows",
    ),
    (
        "Section 8: the seven confirmations in one sentence",
        "a number of the GameBoard's state appears nowhere.",
        "a number of the GameBoard's state appears nowhere. Seven formulas shown Inside were confirmed by their runs, each number pinned before the run, and are listed in Appendix~\\ref{app:reproduction} with their series and fingerprints: the pace of every direction (series Q, $290$ of $290$ face clicks; L7), the click's power (the $(3, 4)$ split, $63/1$, $31/1$, $125/3$), the Mach-Zehnder interference ($64/0$, $0/64$, $32/32$), the exact marginals ($32/64$ in every bin), GHZ's triples ($16$ each, the others $0$), Malus's law ($128$, $0$, $219$ of $256$) and light beside a mass (series K, $0.000$); Table~\\ref{tab:checks} keeps the readings that no formula gives.",
    ),
    (
        "the discussion: the step beneath and the step above, the smallest thing, Newton from the small step, the Inside | Outside table",
        "show, result by result. \\paragraph{The limits, and what does not return.}",
        "show, result by result.  \\paragraph{The step beneath and the step above.} The paper's centre is the step beneath the lattice, Eq.~\\eqref{eq:square} in its frame, the six operations on the record with $W$ its invariant; the direction is one way: the step beneath is the axiom, the conversion of (A1) and (A2) is the map, and the step above is its image, a theorem named as what Einstein wrote. From $W$, by the conversion, the step above follows: $W c^4$ is $E^2 = E_0^2 + p^2c^2$, the gate $E_0/E'$ is $1/\\gamma$, a detector's own rate, the drive's fraction is the click's velocity, and the two Doppler factors are the step above read at two detectors. The click frame's section 7 \\cite{clickframe} shows the chain with no square declared: the walk's exact invariant $\\cos\\omega = \\cos m\\cos\\kappa$ gives $\\omega^2 = m^2 + \\kappa^2 - m^2\\kappa^2/3 + O(6)$; the law's own Planck map ($E = h_q n/d = h_A f$, $p = \\hbar\\kappa$ per Link, $E_0 = \\hbar m$, the load identity $3hn = QSd$) gives $E^2 = E_0^2 + c^2p^2$; the whole unit $E' = E/c^2$ gives $W = E_0'^2 + 3\\,\\mathbf p\\cdot\\mathbf p$ with $3 = 1/c^2 = d$ exactly on the body diagonal ($2.954$, $2.971$, $3.000$ by direction, the root's rounding), the corrections of relative order $m^2\\beta^2$, exact in the continuum limit. So $W$ is shown to that order as the conversion's identity under (A1) and (A2), and Einstein's relation follows from the Inside alone; for the rows' dynamics, which hop whole and lack (A2), $W$ remains the declared identity of record 270 \\cite{log}, the reading's identity and not yet the rows'. The same road serves Newton (below) and, in the same font, what it does not reach: length contraction, the perihelion's second order, the bending of light, waves, horizons and the field equations \\cite{einsteinoutside}.  \\paragraph{The smallest thing above.} What the Outside step is made of follows from (A1) and the click's definition with no run: a click is a Node, a detector's own count and what arrived, and the counts of a family add, so their ratios lie in $\\mathbb Q$ \\cite{clickframe}. Hence the least distance a click can report is one Link, Nodes apart being an integer; the least time a detector times is one count, a pulse and its return two; the least step of a velocity at $k$ counts is one Node per $k$ counts; $c$ is one Link per the least count; and the amount $w$ of a row is the unit that arrives. Every reading Outside is a whole number of these, which is why the world above the board is quantized: physics above cannot take this from its own formulas, and the Inside gives it. The speed of light Outside is then the arrival count over the Euclidean distance, $c_D = N_l|D|/T_D$ by a row's age or by a pulse and its return, its anisotropy $1/c_D^2 = 2.954$, $2.971$, $3.000$ on the heading, the face diagonal and the body diagonal and $1/\\sqrt3$ in the limit \\cite{lightoutside}.  \\paragraph{Newton from the small step.} The same way, with five assumptions on \\texttt{main} today and no (A2) (the crowd read as the age moment, the age wall at coefficient $1$, the push, the flight blind, the reading a pulse and its return) and the spreading of $K$ beams over a shell of $N(r)$ Nodes, which is arithmetic and not a law, the fall, the equivalence principle, Kepler's ratio and the clock in a crowd come out Outside, the inverse square at the shell mean's rung and the equivalence exactly, $M_A$ cancelling record by record; the register's D3, T and X are their confirmation, and the inverse square's decisive reading is not made \\cite{clickframe}. Every result Outside is thus the image of one Inside formula under the conversion, and Table~\\ref{tab:conversion} lists the map row by row with the reading that sits on the Outside side.  {\\scriptsize\\setlength{\\tabcolsep}{3pt} \\begin{longtable}{p{1.7in}p{1.7in}p{1.6in}p{1.4in}} \\caption{\\label{tab:conversion}Inside formulas and Outside formulas, the conversion between them with its order, and the register's reading on the Outside side (the click frame's section 7 \\cite{clickframe}; SHOWN is algebra under the named assumptions, MEASURED a run Inside read Outside).}\\\\ \\toprule Inside (from the six operations) & Outside (a detector reading) & The conversion; its order & The reading (kind) \\\\ \\midrule \\endfirsthead \\toprule Inside & Outside & The conversion & The reading \\\\ \\midrule \\endhead \\bottomrule \\endlastfoot $W = E_0'^2 + 3\\,\\mathbf p\\cdot\\mathbf p$ on the record, $E'$ the whole root by comparisons; on the law no square, the wall linear & the energy a click reads, $\\gamma$, the rate $r = E_0'/E'$ (the identity) or $1$ (the law) & (A1), (A2), the Planck map; shown to order $m^2\\beta^2$; the law's $r = 1$ exact & series S: the 64th self-creation at $70$ and $124$ (GAMEBOARD); $r$ not read \\\\ the pace $|p_a|/(N_lN_wM + |p_a|)$ per axis; under the identity $p/E'$ & the velocity: Nodes apart over counts apart between neighbouring detectors & (A1); exact within $1/T_D$ & D3's controls at their pace on every click (DETECTOR) \\\\ the phase per age $n/d$, $E = h_qn/d = h_Af$, $\\lambda = h_A/p$ & the frequency a detector counts, $1 + z$; $k_{BA} = (1+v)/r$, $k_{AB} = r/(1-v)$, the round trip $(1+v)/(1-v)$ & (A1) and the count, rung 1 & row 4b $0.2636$ (FAIL); series S $0.3674$ (MET in its domain); $k_{AB}$ not read \\\\ the age wall, the crowd $a_\\tau$ at coefficient $1$, the rate $1/(1 + a_\\tau n/d)$ & the clock rate in a crowd by a pulse and its return, the ratio of two lamps' $1 + z$ & (A1) and the count, rung 1 & series T $1.907$ for $1.909 \\pm 0.05$; series X $1.0000$ (DETECTOR) \\\\ the flight table $T_D$, the pace $N_l|D|/T_D$ & the arrival count at a detector $L$ Links away; $c$ one Link per the least count & (A1); rung 1 in the count, rung 2 in the isotropy & series Q $290$ of $290$; series S $369$, $345$ (DETECTOR) \\\\ the click's bilinear form $\\mathbf f^{\\mathsf T}\\mathbf G\\mathbf f$ & Born's form, the count of clicks over many records & (A2) at the click; rung 1 & the two-slit fringes, Malus (DETECTOR); the amount and the phase of one record never pass singly \\\\ the spreading, the presence $q\\tau_L/(4\\pi r^2)$ and the age moment $q\\tau_L/(4\\pi cr)$ in the shell mean & the clock's field, the ratio of two shifts $2.00$; a shell's flat interior & rung 2, the shell mean; the ripple MEASURED ONLY & series T $1.907$; series X $1.0029$ for $1.0039$ (DETECTOR) \\\\ the push $-M_A\\mathbf a$ and the drive & the fall, $a = -GM_B/r^2$, $G = K\\eta/(4\\pi N_w)$; the equivalence & (A1) and the count; the equivalence rung 1, the inverse square rung 2 & D3: $138$ of $139$ common birth ticks (DETECTOR); the inverse square's reading not made \\\\ the circular momentum under the push, $v^2/r = GM_B/r^2$ & Kepler's period, $T(24)/T(12) = 2$ on the plane & rung 2, $v \\ll c$ & D3: $1.997$ in $[1.82, 2.18]$ (DETECTOR) \\\\ \\end{longtable}}  \\paragraph{The limits, and what does not return.}",
    ),
    (
        "what is proved: known and ours",
        "Newton's and Coulomb's inverse square, the retarded potential and Poisson's equation, the clock's $1/r$ form.",
        "Newton's and Coulomb's inverse square, the retarded potential and Poisson's equation, the clock's $1/r$ form. Each names the known form the algebra recovers (Gauss's, Newton's, Coulomb's, Born's, Tsirelson's, Planck's, Einstein's); the paper's own are the integer road, the finite-$\\Nphi$ values (Born's bound $1/\\Nphi$, the plateau $181/64$, the fixed-table limit), the lattice Gleason on $\\Z_{\\Nphi}$, the measurable $1 - v^2$ and the entropy identity of the click; the value $1/\\sqrt3$, Tsirelson's limit and the dictionary's identities claim no novelty.",
    ),
    (
        "Appendix C: the seven confirmations and the twenty-four transitions",
        "\\paragraph{Use of AI tools.}",
        "\\paragraph{The seven confirmations.} {\\footnotesize The pace: series Q, $290$ primitive directions with $|a| + |b| + |c| \\le 6$, $290$ of $290$ face clicks at the derived interval, Node and face, the pace $0.5718$ to $0.5893$ at finite ages; L7, the cone, two rows at the same counter age. The click's power: series L, the $(3, 4)$ split, $63/1$ at $\\Nphi = 64$, $31/1$ at $32$, $125/3$ at $128$, the far pair's cells $27, 5, 5, 27$. The interference of one record: Mach-Zehnder, $64/0$ equal arms, $0/64$ half turn, $32/32$ quarter turn over $64$ births. The exact marginals: the pair at $\\Nphi = 64$, $32/64$ for each party in every bin. GHZ: the four allowed triples $16$ each, the products $+1$ and $-1$, the others $0$. Malus: A12, $128$ of $256$ at $45$ degrees, $0$ of $256$ crossed, $219$ of $256$ at $22.5$. Light beside a mass: series K, three worlds, the deflection $0.000$ pixel, the delay $0.00$ interval. Series L's fingerprint \\texttt{ff5c382d672f}, L7's \\texttt{4bf55a62e6fd} \\cite{register,replications}.} \\paragraph{The transition from ordinary physics to modern algebra, dated.} {\\footnotesize The twenty-four steps of \\cite{history}, each a thing of physics becoming an object of the law: (1) 2026-09-17, the shared quantum resource deleted, locality without exception; (2) 09-17, the amplitude a phase and a conserved content, Born's rule a declared table; (3) 09-17, a force a catalog entry read at a meeting; (4) 09-18, the Born table computed from $\\Nphi$, a clock content, a Node its six Ports; (5) 09-19, the law of events, everything from vector operations; (6) 09-19, a quantum an integer row on the record, the collision a permutation, the click the one one-way border, an open face a detector; (7) 09-19, the tables from the keys, a detector's reading the moments of order $0$, $1$, $2$, the push one bilinear form, charge a rational per unit of content; (8) 09-19, $E = hf$ the cost of a release; (9) 09-20, a force a column with a sign and a lifetime, the coupling a signed inner product; (10) 09-20, two kinds of readings, an emitter in and a detector out; (11) 09-20, the masses and charges the initialisation, the compact quantised, the scale free; (12) 09-20, the amplitude law, a quantum a record, the click chosen by the wheel, the wave the histogram of clicks; (13) 09-20, every count an accumulator on its reader's own record; (14) 09-20 to 21, the Doppler the count of rows a mover crosses; (15) 09-20, the fan a width of the law, the exact phase at the click, the pins detector readings only; (16) 09-21, the whole law one vector operation, the six verbs, the three tests; (17) 09-21, the record an element of $\\Z[\\Z_{\\Nphi}]$, the weight one bilinear form, Born's rule the unique positive quadratic form, the complex numbers leave; (18) 09-21, the lattice the translation group, the $48$ with the hand, $c$ the norm of the flight operator; (19) 09-21, the readings by type, a formula gives and a run proves, the dictionary; (20) 09-21, the Lorentz factor a root refused as a seventh verb, the covariant readings kept beside the law; (21) 09-21 to 22, the clock's word the age moment, Newton and Poisson after a detector; (22) 09-22, a detector's clock a member of the age wall at coefficient $1$; (23) 09-22, the click theorem, a click the passage of information Node to Node, the click families' transformations the Lorentz group up to scale; (24) 09-22, the framing, Inside and Outside, matches nature and never is nature.} \\paragraph{Use of AI tools.}",
    ),
    (
        "the bibitems of the four sources",
        "\\bibitem{clickframe} Lorentz from the clicks: the click frame, its section 0 the click theorem,",
        "\\bibitem{lightoutside} Light Outside from the board: every equation of light Inside carried Outside by its own transformation, \\texttt{docs/designs/light\\_outside/DERIVATION.md} of the archived code \\cite{zenodo}, at 8bd4f811 (PR \\#791, pending merge). \\bibitem{einsteinoutside} Einstein Outside: the formulas of the special and the general theory brought from inside the GameBoard to above it, \\texttt{docs/designs/einstein\\_outside/DERIVATION.md} of the archived code \\cite{zenodo}, at c25efd01 (PR \\#792, pending merge). \\bibitem{history} The transition from ordinary physics to modern algebra: a dated, cited history, \\texttt{docs/designs/algebra\\_transition/HISTORY.md} of the archived code \\cite{zenodo}, at 8eaaf61a (PR \\#793, pending merge). \\bibitem{toffoli1987} T. Toffoli and N. Margolus, Cellular Automata Machines (MIT Press, Cambridge, 1987). \\bibitem{shannon1948} C. E. Shannon, Bell Syst. Tech. J. 27, 379 (1948). \\bibitem{clickframe} Lorentz from the clicks: the click frame, its section 0 the click theorem,",
    ),
    (
        "Table 2: shown row 1 to Appendix C",
        "$c = 1/\\sqrt3$, isotropic within $1/T_D$ & Q, the $290$ directions; L7, the cone & $290$ of $290$ face clicks at the derived interval, Node and face, the pace $0.5718$ to $0.5893$; the two rows' counters at the age $29$ & the flight table's ticks; the same age \\\\",
        "",
    ),
    (
        "Table 2: shown row 2 to Appendix C",
        "The click's weight, power $2$ & L, the $(3, 4)$ split at $\\Nphi = 64$, $32$, $128$; the far pair & $63/1$; $31/1$; $125/3$; the cells $27, 5, 5, 27$ & the same, pinned; the power's window $[1.917, 2.012)$ \\\\",
        "",
    ),
    (
        "Table 2: shown row 3 to Appendix C",
        "Interference of one record & L, Mach-Zehnder, equal arms; half turn; quarter turn & $64/0$; $0/64$; $32/32$ over $64$ births & the same \\\\",
        "",
    ),
    (
        "Table 2: shown row 4 to Appendix C",
        "Exact marginals & L, the pair at $\\Nphi = 64$, all setting bins & $32/64$ for each party in every registered bin & Theorem~\\ref{th:marginals} \\\\",
        "",
    ),
    (
        "Table 2: shown row 5 to Appendix C",
        "GHZ & L, XXX and XYY, YXY, YYX & the four allowed triples $16$ each, the products $+1$ and $-1$; the others $0$ & the same \\\\",
        "",
    ),
    (
        "Table 2: shown row 6 to Appendix C",
        "Malus's law & A12, one polariser at $45$ degrees; two crossed; $22.5$ degrees & $128$ of $256$; $0$ of $256$; $219$ of $256$ & the same, from the tables \\\\",
        "",
    ),
    (
        "Table 2: shown row 7 to Appendix C",
        "Light beside a mass & K, three worlds, the screen's clicks & the deflection $0.000$ pixel, the delay $0.00$ interval & the same: the flight blind to the crowd \\\\",
        "",
    ),
    # The trims after plan B's first compile (35 pages): B.7's named cuts, two defects.
    (
        "the duplicate bibitem shannon1948 removed",
        "\\bibitem{shannon1948} C. E. Shannon, Bell Syst. Tech. J. 27, 379 (1948).",
        "",
    ),
    (
        "the conversion table's columns within the text width",
        "\\begin{longtable}{p{1.7in}p{1.7in}p{1.6in}p{1.4in}}",
        "\\begin{longtable}{p{1.6in}p{1.6in}p{1.5in}p{1.4in}}",
    ),
    (
        "Section 6: the registered integers in four lines, the L2b narrative out (B.7)",
        "\\paragraph{Against the registered integers.} The power: the $(3, 4)$ split's $63/1$ (Section~\\ref{sec:checks}) holds if and only if $7^k$ lies in $[125/3, 127)$, $k \\in [1.917, 2.489)$; the far pair's cells $27, 5, 5, 27$ if and only if $k \\in [1.784, 2.054)$; both windows contain $2$ and exclude $1$ and $3$. The same split scaled to $\\Nphi = 32$ and $\\Nphi = 128$, pinned from the engine's tables and ladder before the run and met exactly ($31/1$ and $125/3$; the amplitude register's \\texttt{mz\\_345\\_n} block, record 363 \\cite{log}), gives $k \\in [1.548, 2.129)$ and $k \\in [1.835, 2.012)$, so the intersection over the registered $\\Nphi$ is $[1.917, 2.012)$, its lower end from $\\Nphi = 64$ and its upper from $\\Nphi = 128$, containing $2$ and excluding $1$ and $3$. These windows are read back from the built click, which carries the square: a check that the implementation is the form of Theorem~\\ref{th:gleason}, no evidence about nature's power (Table~\\ref{tab:nature}, row 2c). The theorem is about the ideal reading; the built click is this form to the tables' rounding, a record's total over the $64$ birth phases from $65448/65536$ to $65773/65536$, the tables' violation of hypothesis (a) (at $\\Nphi = 64$, $C[1]^2 + S[1]^2 = 65650$; the extreme a part in $276$), and the norm range of Appendix~\\ref{app:technical} is the error bound between the two. The two-slit clicks under the birth wheel (series L2b) correlate $0.891$ with the two-source cosine, the kernel of the fundamental $j = 1$; a harmonic $j$ would give a fringe of period $23.5/j$ pixels where $23.5$ is read, and Malus at $22.5$ degrees ($219/256$ and $187/256$ exact) admits $j = \\pm 1 \\bmod 8$ and excludes every mixture: the register pins the fundamental, and the least-rank click (P10) stores it.",
        "\\paragraph{Against the registered integers.} The built click carries the square: the $(3, 4)$ split's $63/1$, $31/1$ and $125/3$ at $\\Nphi = 64$, $32$ and $128$ (record 363 \\cite{log}) hold if and only if the power $k$ lies in $[1.917, 2.012)$, containing $2$ and excluding $1$ and $3$, a check that the implementation is the form of Theorem~\\ref{th:gleason} and no evidence about nature's power (Table~\\ref{tab:nature}, row 2c); the norm range of Appendix~\\ref{app:technical} is the error bound between the ideal reading and the tables. The two-slit period $23.5$ pixels and Malus at $22.5$ degrees ($219/256$ exact) admit the harmonic $j = \\pm 1 \\bmod 8$ and exclude every mixture: the register pins the fundamental, and the least-rank click (P10) stores it.",
    ),
    (
        "Section 3: the anisotropy in one sentence, the bound on the grain to Table 3 (B.7)",
        "The pace is $64/110 = 0.5818$ on a heading, $0.77$ percent above $1/\\sqrt3$, $0.49$ percent above on the plane diagonal, exact on the cube diagonal; the anisotropy is the table's rounding, below $1/T_D$ in every direction and so of order $1/(\\sqrt3 N_l)$; a measured bound on the anisotropy of $c$ in the GameBoard's frame puts $N_l$ at or above its inverse, of order $5.8 \\times 10^{17}$ for $10^{-18}$ \\cite{nagel2015} (what the law says of a laboratory in motion is Section~\\ref{sec:discussion}). Nothing measured enters the value.",
        "The anisotropy is the table's rounding, below $1/T_D$ in every direction and so of order $1/(\\sqrt3 N_l)$ (Table~\\ref{tab:nature}, row 5a, the bound on $N_l$); nothing measured enters the value.",
    ),
    (
        "Section 3: the ground sentence without the registered count (B.7)",
        "Stated with its ground: the pace of a direction, $N_l|D|/T_D$, isotropic within $1/T_D$, and the Manhattan bound $S_1 N_l \\le T_D$ are exact in integers; the isotropic bound $1/\\sqrt3$ is a theorem about a pace that would be the same in every direction, while the GameBoard's Euclidean pace per direction is above $1/\\sqrt3$ on $282$ of the $290$ registered directions, $0.5818$ on every heading, and exactly at it, $0.5774$, on the eight diagonals; the value $c = 1/\\sqrt3$ attained is a limit of the grain $N_l$.",
        "Stated with its ground: the pace of a direction, $N_l|D|/T_D$, isotropic within $1/T_D$, and the Manhattan bound $S_1 N_l \\le T_D$ are exact in integers; the isotropic bound $1/\\sqrt3$ is a theorem about a pace the same in every direction, attained on the eight diagonals, above on every other registered direction, and a limit of the grain $N_l$.",
    ),
    (
        "Section 3: the GRB bound in one clause",
        "By the postulate P9 the pace has no dispersion at any phase rate, so the model meets the bound on an energy-dependent speed of light from GRB 090510, a difference below $2.6 \\times 10^{-18}$ between $31$ GeV and the keV band \\cite{abdo2009}, a computation \\cite{checks}, not a run, and a consequence of the postulate.",
        "By P9 the pace has no dispersion at any phase rate, so the bound on an energy-dependent speed of light from GRB 090510 \\cite{abdo2009} is met, a consequence of the postulate and not a run.",
    ),
    (
        "Section 8: the seven unrun rows by number",
        "seven rows of the register rest on a pin whose run is not made (the muon's lifetime in flight under the law, 4a; the two-arm anisotropy, 5b; Bohr's ratio, 6; the single opening, 10; the far lamp's brightness, stretch and surface brightness, 11a to 11c) and carry no number here.",
        "seven rows of the register (4a, 5b, 6, 10, 11a to 11c) rest on a pin whose run is not made and carry no number here.",
    ),
    (
        "Section 8: the excluded grains in one clause",
        "the law's $181/64$ stands $1.05$ standard errors above, $16384$ and $32768$ at $2.0$, $65536$ and beyond at $1.5$ to $1.65$; $\\Nphi = 64$ ($152$ standard deviations) and $256$ ($30$) are excluded; the loophole-free \\cite{hensen2015} excludes no $\\Nphi$.",
        "the law's $181/64$ stands $1.05$ standard errors above, $16384$ and beyond at $1.5$ to $2.0$; $\\Nphi = 64$ and $256$ are excluded; the loophole-free \\cite{hensen2015} excludes no $\\Nphi$.",
    ),
    (
        "Section 8: the seven confirmations named once, their numbers in Appendix C (B.7)",
        "Seven formulas shown Inside were confirmed by their runs, each number pinned before the run, and are listed in Appendix~\\ref{app:reproduction} with their series and fingerprints: the pace of every direction (series Q, $290$ of $290$ face clicks; L7), the click's power (the $(3, 4)$ split, $63/1$, $31/1$, $125/3$), the Mach-Zehnder interference ($64/0$, $0/64$, $32/32$), the exact marginals ($32/64$ in every bin), GHZ's triples ($16$ each, the others $0$), Malus's law ($128$, $0$, $219$ of $256$) and light beside a mass (series K, $0.000$); Table~\\ref{tab:checks} keeps the readings that no formula gives.",
        "Seven formulas shown Inside (the pace, the click's power, Mach-Zehnder, the marginals, GHZ, Malus, light beside a mass) were confirmed by their runs, each number pinned before the run, and are listed in Appendix~\\ref{app:reproduction} with their series and fingerprints; Table~\\ref{tab:checks} keeps the readings that no formula gives.",
    ),
    (
        "Section 2: the two messages, shorter",
        "Two messages of this paper: a row on the heading $+x$ crosses its Links at the intervals $1, 3, 5, 7, 8$ (the hand-worked update below), its whole history the closed form of its accumulator and nothing kept at a Node; and at a balanced splitter one row of amount $1$ becomes two of amount $1$ and multiplicity $2$ on two arms, which meet again at a second splitter, at one port with equal phases (the words add) and at the other $\\Nphi/2$ apart (an equal pair is no row, the message cancels), so the detector at the first port reads the record, $64$ of $64$ births, and the dark port is the cancelled message (series L, Section~\\ref{sec:checks}).",
        "Two messages of this paper: a row on the heading $+x$ crosses its Links at the intervals $1, 3, 5, 7, 8$ (the hand-worked update below), nothing kept at a Node; and at a balanced splitter one row of amount $1$ becomes two of amount $1$ and multiplicity $2$, which meet again at a second splitter, at one port with equal phases (the words add) and at the other $\\Nphi/2$ apart (the message cancels), so one detector reads the record, $64$ of $64$ births, and the dark port is the cancelled message (series L, Section~\\ref{sec:checks}).",
    ),
    (
        "Section 2: the family of models, shorter",
        "The lattice gases \\cite{hpp1976,fhp1986} carry particles as bits on links with collision tables, the cellular automata machines of \\cite{toffoli1987} are lattices of local rules on bits, the quantum cellular automata of \\cite{arrighi2019} are local unitaries on cells, and Shannon's channel \\cite{shannon1948} is the message and its capacity; the GameBoard is of that family, with two differences the paper states: its messages carry a phase on a bounded circle and an integer amount, and its only read-out is the click.",
        "The lattice gases \\cite{hpp1976,fhp1986} carry bits on links with collision tables, the cellular automata machines of \\cite{toffoli1987} and the quantum cellular automata of \\cite{arrighi2019} are local rules on cells, and Shannon's channel \\cite{shannon1948} is the message and its capacity; the GameBoard is of that family, with two differences: its messages carry a phase on a bounded circle and an integer amount, and its only read-out is the click.",
    ),
    (
        "Section 2: the road's summary sentence out",
        " So mass is a count that sets a wall and scales a form, charge a declared integer in one matrix, momentum a translated vector whose square is compared, and the six operations are the only operations on them.",
        "",
    ),
    (
        "Appendix B: the single-use letters out of the D row (B.7)",
        "$D$, $\\mathbf u_D$, $T_D$, $S_1$, $c_h$, $K$, $\\mathcal F$ & an integer vector written plain, a vector, scalars, a set & a direction, its unit vector at the scale $N_l$, its resolution, its Manhattan length, its Manhattan pace ($c_h = 32/55$ on a heading; not Born's constant $c_1$), the number of directions of a fan (the ladder's $K$, the count of a record's cells in $C_K$ and $\\rung_K$, is Section~\\ref{sec:measurement}'s), the fan of primitive directions within $N_D$ \\\\",
        "$D$, $\\mathbf u_D$, $T_D$, $S_1$, $K$ & an integer vector written plain, a vector, scalars & a direction, its unit vector at the scale $N_l$, its resolution, its Manhattan length, the number of directions of a fan (the ladder's $K$, the count of a record's cells in $C_K$ and $\\rung_K$, is Section~\\ref{sec:measurement}'s) \\\\",
    ),
    (
        "Appendix B: the single-use letter out of the lambda row (B.7)",
        "$\\lambda$, $\\psi_r$, $Q$, $\\theta$ & scalars, an element, a module & a wavelength, the state of the record $r$ in the group ring, the quotient of the rows' module that forgets the age (Theorem~\\ref{th:bijection}), an angle \\\\",
        "$\\lambda$, $Q$, $\\theta$ & scalars, a module & a wavelength, the quotient of the rows' module that forgets the age (Theorem~\\ref{th:bijection}), an angle \\\\",
    ),
    (
        "Appendix B: the single-use letter out of the z row (B.7)",
        "$z$, $q_0$, $G$, $\\rho$ & scalars & the redshift, the deceleration parameter (Table~\\ref{tab:nature}, row 3), Newton's constant, a family's charge per unit of content \\\\",
        "$z$, $G$, $\\rho$ & scalars & the redshift, Newton's constant, a family's charge per unit of content \\\\",
    ),
    (
        "Table 2: the weak forms' row, already Table 3's rows 8a and 8b",
        "The weak forms & J1, the neutron's decay clicks; J2, the second detector & the width over the median $0.036$ and $0.038$ over $64$ clicks; $16$ of $1024$ with $0$ behind & a step; a window \\\\",
        "",
    ),
    (
        "Table 2: the covariant readings' row, now the conversion table's",
        "The covariant readings (a hypothesis beside the law) & S, the muon at rest, at $0.43c$, at $0.86c$; the coasting star & the electron's face clicks at $392$, $369$, $345$; $z = 0.3674$ (arithmetic on the click ticks) & $391$, $367$, $345$ within two; $0.369 \\pm 0.003$ \\\\",
        "",
    ),
    (
        "the limits paragraph cites series S in the conversion table",
        "(series S, Table~\\ref{tab:checks}, inside their pins)",
        "(series S, Table~\\ref{tab:conversion}, inside their pins)",
    ),
    (
        "row 5a cites series Q in Appendix C",
        "(series Q within it at finite ages, Table~\\ref{tab:checks})",
        "(series Q within it at finite ages, Appendix~\\ref{app:reproduction})",
    ),
    # Round 2 of the trims: the run narratives of Sections 3, 5 and 7 and Appendix C, shorter.
    (
        "Section 5: series T in one sentence",
        "Which of the two words the clock counts, the presence or the age moment, was put to the GameBoard as series T of the register, the physicist's pins written before the run \\cite{register,clockage}: a lamp at rest, two sources of $F = 4915$ units per interval each at $3$ and then at $6$ Links, the detector at $x = 110$; under the presence word the detector reads $1 + z = 1.3000$ at both distances, the presence clock unable to tell them apart; under the age word $2.6517$ at $3$ and $4.1500$ at $6$, the ratio of the two $a_\\tau$ being $1.907$ for the lines' pin $1.909$, nature's $2.00$ being $4.6$ percent away; every pin met; measured and replicated (\\cite{replications}, the block of series T).",
        "Which word the clock counts, the presence or the age moment, was put to the GameBoard as series T, the physicist's pins written before the run \\cite{register,clockage}: a lamp at rest, two sources at $3$ and at $6$ Links, the detector at $x = 110$; under the presence word the detector reads $1 + z = 1.3000$ at both distances; under the age word $2.6517$ and $4.1500$, the ratio of the two $a_\\tau$ being $1.907$ for the lines' pin $1.909$, nature's $2.00$ being $4.6$ percent away; every pin met, measured and replicated \\cite{replications}.",
    ),
    (
        "Section 5: the GPS term is Table 3's row 12",
        " Under the age word the clock's shift follows the potential's form, the physicist's map putting the GPS ground-to-orbit shift at $45.7$ microseconds per day against Ashby's $45.7$ \\cite{ashby2003}, where the presence word gives $28.3$.",
        "",
    ),
    (
        "Section 7: the tables' bound in one clause",
        "(measured at $16384$: $S\\Nphi = 46344$ \\cite{register}), where the second pair of settings rounds to $2893/4096$ (\\cite{checks}, \\texttt{s\\_powers\\_of\\_two}; the tables' bound $2\\Nphi \\le 65536$ stops the tables' computation there).",
        "(measured at $16384$, Table~\\ref{tab:checks}), where the second pair of settings rounds to $2893/4096$ and the tables' bound $2\\Nphi \\le 65536$ stops their computation (\\cite{checks}, \\texttt{s\\_powers\\_of\\_two})",
    ),
    (
        "Appendix C: the fingerprints and the tag, shorter",
        "The register's runs carry the fingerprint \\texttt{ff5c382d672f} (the gate worlds re-run after the gate's fix with the same integers); the figures' runs carry \\texttt{731d0f56c9f9}, the fingerprint of \\texttt{figures/summary.json} \\cite{checks} on the paper's tree; every integer is equal. The two cone worlds of L7 carry \\texttt{4bf55a62e6fd}, the tree of the one click. The archived version cited at submission is the tag \\texttt{paper-2026-09-22} on the merge commit of the pull request that carries this cut, one tree whose history holds the three trees named above and the log records this paper cites; it replaces the concept DOI below, and its code no longer has the world key.",
        "The register's runs carry the fingerprint \\texttt{ff5c382d672f}, the figures' runs \\texttt{731d0f56c9f9} (\\texttt{figures/summary.json} \\cite{checks}), the two cone worlds of L7 \\texttt{4bf55a62e6fd}. The archived version cited at submission is the tag \\texttt{paper-2026-09-22} on the merge commit of the pull request that carries this cut, one tree whose history holds the trees named above and the log records this paper cites; it replaces the concept DOI below.",
    ),
    (
        "Section 3: the Courant bound and the lattice Boltzmann sound speed in one sentence",
        "The number is, as is well known, the bound of the Courant condition of the standard second-order scheme for the wave equation, $c\\,\\Delta t/\\Delta x \\le 1/\\sqrt n$ \\cite{cfl1928}, whose necessity is this same argument (the sphere of radius $c\\,\\Delta t$ inside the stencil's octahedron), and the lattice Boltzmann sound speed $c_s^2 = 1/3$, from the isotropy of the lattice tensor \\cite{qian1992}. What the paper adds is the exact integer table sitting at the bound, its rounding's anisotropy as a bound on the grain, and the program's intent of one operator for rows and bodies; it claims no novelty for the number.",
        "The number is the bound of the Courant condition for the wave equation, $c\\,\\Delta t/\\Delta x \\le 1/\\sqrt n$ \\cite{cfl1928}, by this same argument, and the lattice Boltzmann sound speed $c_s^2 = 1/3$ \\cite{qian1992}; the paper adds the exact integer table at the bound and its rounding's anisotropy as a bound on the grain, and claims no novelty for the number.",
    ),
    # Round 3 of the trims: Appendix C's reproduction paragraphs, shorter.
    (
        "Appendix C: the long form in one sentence",
        "The long form of this manuscript, with the derivation record of every formula, the families' tables, the dark sector, the inventory of flow and heat and the table of every computable difference, is the tree's paper at the commit \\texttt{c15c1174}; this paper is its cut to what is proved, measured after a detector or replicated, built around the general formula; the forty-page cut before it is at the commit \\texttt{b0d1ebf7}; the tree cited for the rest.",
        "The long form of this manuscript, with the derivation record of every formula, is the tree's paper at the commit \\texttt{c15c1174}, the forty-page cut before it at \\texttt{b0d1ebf7}; this paper is the cut to what is proved, measured after a detector or replicated, built around the general formula.",
    ),
    (
        "Appendix C: the interpreter in one clause",
        "The project's declared interpreter is Python 3.14; no floating point is in any physical module; the runs take seconds each (the register's durations).",
        "The interpreter is Python 3.14, no floating point in any physical module, the runs seconds each.",
    ),
    (
        "Appendix C: the fingerprints named once",
        "the delay $0.00$ interval. Series L's fingerprint \\texttt{ff5c382d672f}, L7's \\texttt{4bf55a62e6fd} \\cite{register,replications}.}",
        "the delay $0.00$ interval \\cite{register,replications}.}",
    ),
    # Round 4 of the trims: Appendices B and C, a few lines.
    (
        "Appendix B: the norm's extremes in one clause",
        "(the extremes $65185$ and $65897$, the latter at $\\Nphi = 4096$, $p = 503$ and $3593$: $C = 184$, $|S| = 179$; at $\\Nphi = 64$ the range is $-88$ to $+237$)",
        "(at $\\Nphi = 64$ the range is $-88$ to $+237$)",
    ),
    (
        "Appendix B: the Mach-Zehnder total in one clause",
        "The integer Mach-Zehnder's record total over the $64$ birth phases, a number of the apparatus layer computed from the tables and not a reading, takes eight values from $65448/65536$ to $65773/65536$, the same eight on every one of its ten worlds \\cite{register};",
        "The Mach-Zehnder record's total over the $64$ birth phases, computed from the tables and not a reading, takes eight values from $65448/65536$ to $65773/65536$ \\cite{register};",
    ),
    (
        "Appendix B: the cap's row, shorter",
        "$a$, $\\varrho$ & scalars & the cap of Eq.~(\\ref{eq:map}); where the text says so, an acceleration ($a = -GM/r^2$), a party's setting or a Link's length; the tables' radius $N_t - \\sqrt2/2$ (Theorem~\\ref{th:bell}) \\\\",
        "$a$, $\\varrho$ & scalars & the cap of Eq.~(\\ref{eq:map}), or, where the text says so, an acceleration or a party's setting; the tables' radius $N_t - \\sqrt2/2$ (Theorem~\\ref{th:bell}) \\\\",
    ),
    (
        "Appendix C: the AI statement, shorter",
        "\\paragraph{Use of AI tools.} The simulator's code, the design documents, the check scripts and the drafts of this manuscript were produced with AI coding agents working under the author's direction and review; the author verified every number against the archived runs and is responsible for the whole text. No AI system is an author. [The tool and version are named here at submission.]",
        "\\paragraph{Use of AI tools.} The code, the design documents, the check scripts and the drafts of this manuscript were produced with AI coding agents under the author's direction and review; the author verified every number against the archived runs and is responsible for the whole text; no AI system is an author. [The tool and version are named at submission.]",
    ),
    (
        "Appendix C: the pace's confirmation, shorter",
        "The pace: series Q, $290$ primitive directions with $|a| + |b| + |c| \\le 6$, $290$ of $290$ face clicks at the derived interval, Node and face, the pace $0.5718$ to $0.5893$ at finite ages; L7, the cone, two rows at the same counter age.",
        "The pace: series Q, $290$ of $290$ primitive directions ($|a| + |b| + |c| \\le 6$) clicking at the derived interval, Node and face, the pace $0.5718$ to $0.5893$ at finite ages; L7, the cone.",
    ),
    (
        "Appendix C: the far lamp's rows are Section 8's",
        "; the far lamp's rows 11a to 11c rest on a pin whose run is not made.",
        ".",
    ),
    # Series X's clock reading: the registered k at r = 4 (docs/EXPERIMENTS.md, series X; record 661).
    (
        "the conversion table's clock row: series X's registered reading",
        "series T $1.907$ for $1.909 \\pm 0.05$; series X $1.0000$ (DETECTOR)",
        "series T $1.907$ for $1.909 \\pm 0.05$; series X $k = 0.9089$ at $r = 4$ for the pin $0.9108$ (DETECTOR)",
    ),
    # Commit C, the owner's words of records 817 and 822: the roads shown and checked, the families in the algebra, the new formulas; the citations at the merged and current heads.
    (
        "the click frame cited on main at its merge (PR #769 merged at 70e9781a; the file identical to 1dd81fef)",
        "at 1dd81fef (PR \\#769, pending merge).",
        "on \\texttt{main} at 70e9781a (PR \\#769, merged; the file identical to its head 1dd81fef).",
    ),
    (
        "light-outside at its current head",
        "at 8bd4f811 (PR \\#791, pending merge)",
        "at ceb6e066 (PR \\#791, pending merge)",
    ),
    (
        "einstein-outside at its current head",
        "at c25efd01 (PR \\#792, pending merge)",
        "at d1b4af84 (PR \\#792, pending merge)",
    ),
    (
        "the algebra transition at its current head",
        "at 8eaaf61a (PR \\#793, pending merge)",
        "at 928f056d (PR \\#793, pending merge)",
    ),
    (
        "the bibitem clickframe2 (the W phrase, pending its PR)",
        "\\bibitem{toffoli1987}",
        "\\bibitem{clickframe2} The click frame, part 2 (``no square is declared anywhere in the chain''), \\texttt{docs/designs/click\\_frame/DERIVATION.md} of the archived code \\cite{zenodo} on the branch click-frame-2 at 097b2006, pending its PR. \\bibitem{toffoli1987}",
    ),
    (
        "the step paragraph cites the W phrase",
        "So $W$ is shown to that order as the conversion's identity under (A1) and (A2), and Einstein's relation follows from the Inside alone;",
        "So $W$ is shown to that order as the conversion's identity under (A1) and (A2), no square declared anywhere in the chain \\cite{clickframe2}, and Einstein's relation follows from the Inside alone;",
    ),
    (
        "row 2b quotes Grangier (PR #797 merged at 01660cbb)",
        "Mach-Zehnder visibility: $0.98$;",
        "Mach-Zehnder visibility: $0.98$ \\cite{grangier1986};",
    ),
    (
        "the discussion: the road to each and the check; what the Inside gives Outside that the continuum cannot state (records 817 and 822)",
        "\\paragraph{The limits, and what does not return.} The content and",
        "\\paragraph{The road to each, and the check that nothing was derived from them.} Three roads are shown, each from the Inside step, the six verbs, (A1) and, where it enters, (A2), with (A3), locality Outside (nothing Outside passes faster than a chain of clicks or jumps a Node), a definition of Outside and not a law \\cite{einsteinoutside}. To Lorentz: two legs at one Node per interval, the two directions alike ($k_{AB} = k_{BA}$), give the boost with $v = (k^2 - 1)/(k^2 + 1)$, the scale $r$ left free, the click frame's section 2; (A2) is what fixes $r$ at $\\sqrt{1 - v^2}$. To Einstein: the place-to-place factor $k_{XY}$ from (A1) and the counts, the radar map, the rate $1/\\gamma$ as $r$ read from two factors, the composition of velocities $r$-free, and $E^2 = E_0^2 + c^2p^2$ as the line of the rate with $W$ shown to second order (Section 7 of the frame), Theorems 1 and 2 and rows II.1, II.3 and II.6 of \\cite{einsteinoutside}. To the step above itself: the Outside step, place apart and count apart of a detector between two clicks, is the image of the Inside step under the conversion, Einstein's step its most general form where $r$ is supplied, its quantum a theorem of (A1), (A3) and the drive's one Link per self-creation, and Newton's step its limit at $v \\ll c$ (section 3 of \\cite{einsteinoutside}). Einstein's, Lorentz's and the Outside step's formulas appear in these chains only as the thing compared with; no chain takes them as an input, and the Outside step is never a second formula set beside the Inside step. The word is ``follows'' or ``recovered'' where a known form is arrived at, ``shown to second order'' for $W$ under (A1) and (A2), ``declared'' for $W$ on the rows' dynamics and for the unit $E_0 = m c^2$; ``derived'' stands nowhere in the three roads. Table~\\ref{tab:roads} (Appendix~\\ref{app:families}) lists the check row by row: the inputs each chain used, the file and line where it starts, and the word; the check was made by reading each chain against the certification tables of the two sources, and the physics-rule reviewer audits the same in the sources.  \\paragraph{What the Inside step gives Outside that the continuum cannot state.} Formulas of the six verbs taken Outside by the conversion, each with the click that reads it and its kind; none of them is a formula of the continuum. (i) The quantum of the Outside step: one Link, a pulse and its return, a velocity $1/k$ in the mean with its quantum $1/(k(k + 1))$ at the pace $1/k$ (Theorem 3 of \\cite{einsteinoutside}); read as a least step in series S's face clicks $369$ and $345$ within two of the flight table's and D3's $138$ of $139$ births at the same Node (DETECTOR); the velocity's quantum and the pulse's two counts not read as such. (ii) The pair's sum at the CHSH labels is the exact rational the rung gives, $|S(\\Nphi) - 2\\sqrt2| \\le 8/\\Nphi + 0.0444$, above the bound at $\\Nphi = 16$ and $32$ ($S = 3$), the plateau $181/64$ from $512$ through $8192$ below it by $3.02 \\times 10^{-4}$ and $5793/2048$ above at $16384$ (Theorem~\\ref{th:bell}; the frame's section 10); measured at seven $\\Nphi$ (Table~\\ref{tab:checks}, DETECTOR). (iii) The perihelion: the drive's pace departs from $p/m_i$ at first order per axis, so a bound orbit's apsides move per revolution by an angle of order $\\beta$ with the lattice's symmetry, where Einstein has $6\\pi\\beta^2$ isotropic, about $300$ times nature's at Mercury's pace and of the wrong symmetry: FAIL on the law, stated as a difference; under the identity $\\pi\\beta^2$, one sixth; the deciding reading, the apsides of a lamp's orbit at two orientations to the axes, NOT MADE, its pin written before any run, an apsidal motion of order $\\beta$ that changes with the orientation and not with the mass held (\\cite{einsteinoutside}, II.12). (iv) The grain: the radial residence factor times the pace, $\\tau_L c = 0.993$ on a heading, multiplies every constant read at a finite grain and is $1$ in the limit of every direction. (v) The anisotropy of $c$ by direction, $1/c_D^2 = 2.954$, $2.971$, $3.000$ (series Q, $290$ of $290$, DETECTOR; \\cite{lightoutside}). (vi) The equivalence's constant: the clock in a crowd and the accelerated detector read one shift, $\\delta k = (nS/d)\\,(gY/c^2)$, Einstein's $gY/c^2$ exactly when $nS = d$, a condition on an Inside declaration and not a result; the register's clock and crowd worlds declare $nS/d = 16$ (GAMEBOARD, the world files), so the condition is not met by them, the form's readings are series T's $1.907$ and series X's $k$ (DETECTOR), and the constant's reading is NOT MADE (\\cite{einsteinoutside}, II.10). (vii) Light's bending: on the law $0$, the flight blind to the crowd (series K, $0.000$ pixel, DETECTOR; FAIL against $1.75$ arcseconds); under the key \\texttt{optical}, the flight in the age wall's set with a declared $c_f$, the delay $c_f (nS/d)(GM/c^3)\\ln(4r_1r_2/b^2)$ and the bending $\\alpha = 2c_f(nS/d)\\,GM/(c^2 b)$, Einstein's at $nS = d$ and $c_f = 2$, NOT COMPARED, the route the owner's decision (\\cite{einsteinoutside}, II.11). The families of the register, each with its declared integers, its algebraic object and the click that reads it, are Table~\\ref{tab:families}.  \\paragraph{The limits, and what does not return.} The content and",
    ),
    (
        "Section 2: the families in the algebra (record 822)",
        "\\paragraph{Rules, parameters, initial conditions.} The law is stated as rules,",
        "\\paragraph{The families in the algebra.} Every family of the register is one row of declared integers (P8) and nothing else: the quantum $h$ ($1$ on a free family, whose rows carry their energy as turns, $0$ on a paid family, whose content is the mass), the charge per unit of content as a rational pair, the columns with their signs, the lifetime, whether the phase turns, the hand; the content $M$ of a body is the world's declaration. Written down, a family is where its quantities live: the content on $\\Z$, the non-compact scale, free; the phase on $\\Z_{\\Nphi}$, quantised; the charge and a column's coefficient as entries of the coupling matrix; the hand a pseudoscalar under the $48$; a family's rows on the fan under the $48$; a pair's arms in $\\Z^2 \\otimes \\Z^2$ under the settings' integer matrices; and the six verbs are the only operations on them. The mass angle $m$ of the frame is the rest pair's turn, $2\\pi n/d$ per interval, a world's declaration and not the family's. Table~\\ref{tab:families} (Appendix~\\ref{app:families}) lists every family of the register with its declared integers, its object, when it entered, the verbs that act on it and the click that reads it; a cell the tree does not name says so.  \\paragraph{Rules, parameters, initial conditions.} The law is stated as rules,",
    ),
    (
        "Appendix D: the families table and the roads' check table",
        "[The tool and version are named at submission.]",
        "[The tool and version are named at submission.]  \\section{The families in the algebra, and the check of the roads}\\label{app:families}  {\\scriptsize\\setlength{\\tabcolsep}{3pt} \\begin{longtable}{p{0.7in}p{1.25in}p{1.25in}p{0.9in}p{0.6in}p{1.15in}} \\caption{\\label{tab:families}Every family of the register \\cite{familiesaudit}: its declared integers ($h$, the charge $\\rho$, the columns, the lifetime $L$, the circle, the hand; the content $M$ on the measured worlds), its algebraic object (the frame's section 9 \\cite{clickframe}; \\cite{history}), when it entered (the record), the verbs that act on it (1 translation, 2 bilinear form, 3 group-ring addition, 4 permutation, 5 evaluation, 6 division) and the click that reads it, by kind. ``Not named'' is a cell the tree does not fill.}\\\\ \\toprule Family & The declared integers & The algebraic object & When it entered & The verbs & The click that reads it \\\\ \\midrule \\endfirsthead \\toprule Family & The declared integers & The object & When & Verbs & The click \\\\ \\midrule \\endhead \\bottomrule \\endlastfoot \\texttt{light} (the photon) & $h = 1$; no charge; the circle turns; $M$ per unit $1$; the amplitude worlds' births $2^{20}$ to $2^{33}$ & a free row, an element of $\\Z[\\Z_{\\Nphi}]$ born at the lamp, its amount the coefficient, its direction on the fan under the $48$; its phase per Link the declared turn & the amplitude a phase and a content, 2026-09-17 (entry 2); $E = hf$, 09-19 (entry 8) & 1, 2, 3, 5 & the two-slit pixels (L2b), the Mach-Zehnder ports $64/0$, series Q's $290$ of $290$ face clicks (DETECTOR) \\\\ \\texttt{e} (the electron) & $h = 0$; $\\rho = -15$; the circle turns; $M = 1836$ (atoms, bohr), $1$ (gallery) & the content on $\\Z$; the charge one entry of the coupling matrix; the momentum an integer $3$-vector; the phase on $\\Z_{\\Nphi}$ & the charge a rational per unit, 09-19 (entry 7); the masses the initialisation, 09-20 (entry 11) & 1, 2, 6 & series S's face clicks $369$, $345$ (DETECTOR); Bohr's ratio (row 6) not run \\\\ \\texttt{beta}, \\texttt{w} (the decay's electron and boson) & $h = 1$; a whole charge $-7344$ per unit of amount; \\texttt{w}'s lifetime $1$, no circle; \\texttt{beta}'s circle turns, its hand $-1$ on \\texttt{hand/wu} & a free row pushing by its label; the lifetime an integer wall; the hand a pseudoscalar in $\\Z_2$ & the catalog, record 30; one definition per family, record 113 (09-20) & 1, 2, 6 & the neutron's decay clicks, series J1, $64$ clicks, width over median $0.036$ (DETECTOR, row 8a) \\\\ \\texttt{p} (the proton) & $h = 0$; $\\rho = [1, 1]$ (a winding), $4$ on the atoms and binding worlds; no circle; $M = 1834$, $1836$ & the content on $\\Z$; the charge a rational pair in the coupling matrix; clicks by no phase & the catalog, record 30; one definition per family, record 113 (09-20) & 1, 2, 6 & series N's border clicks: the deuteron's held bond $0.109$ percent, the alpha's $2.0$ (DETECTOR, rows 7a, 7b) \\\\ \\texttt{n} (the neutron) & $h = 0$; no charge; no circle; $M = 1837$, $1839$ & the content on $\\Z$; the momentum an integer $3$-vector & as above & 1, 2, 6 & series J1's decay clicks (row 8a); series N (row 7a) (DETECTOR) \\\\ \\texttt{nuclear}, \\texttt{glue}, \\texttt{bond} (the strong column and the bond) & $h = 0, 0, 1$; the column \\texttt{strong} $\\sigma = 10000$ with the sign $-1$ ($7000$ on one nucleus world); the lifetime $3$; no circle & the column's signed scalar per unit, one entry of the coupling matrix; the lifetime an integer wall & a force a column with a sign and a lifetime, 09-20 (entry 9) & 2, 6 & series N's border clicks (DETECTOR, rows 7a, 7b) \\\\ \\texttt{u} (the up quark) & $h = 0$; $\\rho = 1224$; no circle & the content on $\\Z$, the charge on $\\Z$ & the catalog, record 30 (09-20) & 1, 2, 6 & no detector reading registered (the quarks worlds) \\\\ \\texttt{nu}, \\texttt{nubar} (the neutrino) & $h = 0$; no charge; no content per unit (row 8c); the circle turns; the hand $+1$ (\\texttt{nubar}), $-1$ (\\texttt{nu} on \\texttt{hand/nu\\_hand}); $M = 4096$ on the weak worlds & the hand a pseudoscalar in $\\Z_2$ under the $48$, kept by the rotations and negated by the reflections; the phase on $\\Z_{\\Nphi}$ & the hand, \\texttt{hand-v1} \\cite{history} & 1, 4, 5 & series J2, $16$ of $1024$ with $0$ behind (DETECTOR, row 8b); the massless input refuted (row 8c) \\\\ \\texttt{m}, \\texttt{mass}, \\texttt{probe}, \\texttt{neutron} (the massive bodies) & $h = 0$; $\\rho = 0$; no circle; $M$ from $1$ to $2^{26}$ as declared per world & the held content on $\\Z$; a body's momentum an integer $3$-vector; its counts accumulators $(s, r, d)$; the age wall's member & the content, record 15 of 09-19; the masses the initialisation, 09-20 (entry 11); the clock's word, 09-21 to 22 (entry 21) & 1, 2, 6 & D3's births at the line, $138$ of $139$, $T(24)/T(12) = 1.997$; series T's $1.907$; series X's $k = 0.9089$; series G2's $z = 0.2636$ (DETECTOR) \\\\ \\texttt{q} (the test charge) & $h = 0$; $\\rho = [0, 1]$, $[-1, 2]$ on the coupling worlds; the circle turns; $M = 2^{24}$ & the charge a rational pair in the coupling matrix & the charge a rational per unit, 09-19 (entry 7) & 2, 6 & no detector reading registered (the coupling worlds) \\\\ \\texttt{sa}, \\texttt{sb} (the pair's choosers) & $h = 0$; no charge; the circle turns & a setting's integer matrix $U_s$ in $M_2(\\Z)$ acting on the arms' label pair; the pair's record in $\\Z[\\Z_{\\Nphi}] \\otimes \\Z^2 \\otimes \\Z^2$ & the record an element of $\\Z[\\Z_{\\Nphi}]$, 09-21 (entry 17) & 2, 3, 5 & the pair's clicks, $S = 2.75$ at $\\Nphi = 64$, the marginals $32/64$ (DETECTOR, row 1a) \\\\ the apparatus materials (\\texttt{wall}, \\texttt{screen}, \\texttt{counter}, \\texttt{apparatus}, \\texttt{carrier}, \\texttt{detector}, \\texttt{d}) & $h = 1$; no charge; the circle turns (\\texttt{d} no) & the click's readers: a detector's set of Nodes, its own count the age wall's member at coefficient $1$, its reading the moments of order $0$, $1$, $2$ & the readings the moments, 09-19 (entry 7); a detector's clock, 09-22 (entry 22) & 5, 6 & every DETECTOR row: they are the clicks \\\\ the sources (\\texttt{s}, the $24$ \\texttt{thrown\\_sources}, the $24$ \\texttt{hubble\\_stars}) & $h = 0$ or $1$; no charge; the circle turns; $M = 64$, $1024$, $4096$, $8192$ & a lamp's counts table on $\\Z_W$ (the birth wheel); a throw's direction on the fan & the amplitude law, the wheel, 09-20 (entry 12) & 1, 6 & series G2's $z = 0.2636$ (row 4b); series T's lamp; the hubble worlds' $q_0 = -0.108$ (row 3) (DETECTOR) \\\\ \\texttt{mu} (the muon, the covariant worlds) & inline: $h = 0$; $M = 13248$ (series S) & the record's $W = E'^2 + 3\\,\\mathbf p\\cdot\\mathbf p$ with $E'$ the whole root by comparisons (the identity, a hypothesis beside the law) & the covariant readings, 09-21 (entry 20) & 1, 2, 6 & the 64th self-creation at $70$ and $124$ (GAMEBOARD); its products' face clicks (DETECTOR, series S) \\\\ \\texttt{matter} (the massive rows) & inline: $h = 0$; the rows' content per unit & a paid row, its content per unit on $\\Z$, its momentum content $\\times\\,\\mathbf u_D$ & the massive rows, series W (09-21) & 1, 6 & series W's first-click ages $815$ and $876$ at the pixels (DETECTOR) \\\\ \\end{longtable}}  {\\scriptsize\\setlength{\\tabcolsep}{3pt} \\begin{longtable}{p{1.5in}p{1.7in}p{1.5in}p{1.4in}} \\caption{\\label{tab:roads}The check of the roads (record 817): one row per formula the paper arrives at, the inputs its chain used, the file and line where the chain starts, and the word used. No row lists Einstein's or Lorentz's formula among its inputs; ``derived'' stands in no row. The sources: the click frame on \\texttt{main} at 70e9781a \\cite{clickframe} and Einstein Outside at d1b4af84 \\cite{einsteinoutside}, whose section III is the same check made in the source.}\\\\ \\toprule The formula arrived at & The inputs its chain used & Where the chain starts & The word \\\\ \\midrule \\endfirsthead \\toprule The formula & The inputs & Where & The word \\\\ \\midrule \\endhead \\bottomrule \\endlastfoot $W = E_0'^2 + 3\\,\\mathbf p\\cdot\\mathbf p$ to second order & (A1), (A2); the walk's invariant $\\cos\\omega = \\cos m\\cos\\kappa$; the Planck map on \\texttt{main}; the unit $E' = E/c^2$ & the click frame, section 7 (the invariant :748, the unit :795); \\cite{clickframe2} & shown to second order (the conversion's identity); declared for the rows' dynamics (record 270) \\\\ the boost, Lorentz's form & (A1); two legs at one Node per interval; $k_{AB} = k_{BA}$ & the click frame, section 2 (b) :278--297; section 0 :84--132 (the group up to scale) & follows; Lorentz's form recovered, the scale $r$ free; (A2) fixes $r$ at $\\sqrt{1 - v^2}$ \\\\ the place-to-place factor $k_{XY} = (r_Y/r_X)(1 - \\mathbf s\\cdot\\mathbf v_X)/(1 - \\mathbf s\\cdot\\mathbf v_Y)$ & (A1), (A3), the counts; $r$ a free symbol & Einstein Outside, Theorem 1 :349 & follows (a theorem of A1) \\\\ $1/\\gamma$, the rate $r$ & Theorems 1, 2; $r$ read from two factors & Einstein Outside, II.1 :636 & follows in $r$; $\\sqrt{1 - v^2}$ recovered under the line, shown to second order under (A2), declared under the identity, $1$ on the law \\\\ the composition $w = (v_R - v)/(1 - v v_R)$ & Theorems 1, 2, (A3) & Einstein Outside, II.3 :716 & follows, $r$-free (Einstein's form recovered) \\\\ $E^2 = E_0^2 + c^2p^2$ & $E = E_0/r$, $p = Ev$, the line of II.1; the frame's section 7 for $W$ & Einstein Outside, II.6 :870 & follows as the line; $W$ shown to second order; exact by declaration under the identity; $E_0 = mc^2$ a declared unit \\\\ the Outside step, place apart and count apart of a detector, Einstein's step its most general form & (A1), (A3), the Inside step, Theorems 1, 2 & Einstein Outside, section 3 (a) :470 (Einstein's form named at :486 as the comparison) & follows; Einstein's form recovered where $r$ is supplied, never an input \\\\ the quantum of the step above & (A1), (A3), the drive's one Link per self-creation, Theorem 2 (a) & Einstein Outside, section 3 (b) :499 & follows (a theorem; no run) \\\\ Newton's step as the limit & Theorem 4, the shell mean, $v \\ll c$ & Einstein Outside, section 3 (c) :543 & recovered (the limit) \\\\ \\end{longtable}}  ",
    ),
    # The families table's cells that overflowed their columns.
    (
        "the families table: the sources' names break in the column",
        "the sources (\\texttt{s}, the $24$ \\texttt{thrown\\_sources}, the $24$ \\texttt{hubble\\_stars})",
        "the sources (\\texttt{s}; the $24$ thrown sources; the $24$ star sources)",
    ),
    (
        "the families table: the neutrino's world named without the path",
        "$-1$ (\\texttt{nu} on \\texttt{hand/nu\\_hand})",
        "$-1$ (\\texttt{nu} on the world \\texttt{nu\\_hand})",
    ),
    (
        "the families table: the decay's world named without the path",
        "its hand $-1$ on \\texttt{hand/wu}",
        "its hand $-1$ on the world \\texttt{wu}",
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
