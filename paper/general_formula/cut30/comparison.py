"""The comparison section of the storyline (the Boss's PLAN.md section 8,
items 4 and 5; the owner's words of 2026-09-23 and 2026-09-24): the method
(an experiment a world file, a result clicks, the pin before the run, three
checks per row), the table of the paper's list with three columns per row
and a visible blank for every reading not yet made and merged, the bounds
and the derivations final, and the rows that left the list. The sources:
docs/designs/detector_law/APPROVALS.md (the three checks and their state),
ALGEBRAIC_CLOSURE.md (the closed rows), SCHEDULE.md (the pins by kind) and
DECLARATIONS.md. Every number here is a COMPUTATION declared before its
run or an exploratory reading labelled so; nothing from an unmerged reading.
"""

BLANK = "\\underline{\\hspace{0.45in}}"

METHOD = r"""\paragraph{The method.} An experiment is a world file: the GameBoard's extents, the blocks placed on it as the bodies of the experiment, the lamps and the detectors, every one a declared object of Section~\ref{sec:massive}; a result is clicks, a count between clicks on a detector's own record or a ratio of such counts; the pin, the number the algebra gives, is written before the run and no pin moves after a reading. Every row of the paper's list passes three checks in order \cite{approvals}: approved in the algebra, its number following from the one law before any run and closed on the closure page \cite{closure}; approved on the GameBoard without pins, an exploratory run reading beside the algebra's number within the band the physicist declared, labelled exploratory and never a result; approved with pins, the pin written before the run \cite{declarations,schedule}, one run at the owner's word, the clicks read by the reader of record and the reading by kind inside the pin. A row is (K), a known-formula row whose algebraic identity is a textbook formula and whose engine reading is the control of the engine against the algebra, or (P), a prediction row, a number the algebra gives and no known formula gives; a prediction is not a pass. A reading that falls outside its pin is written as a miss, in this table, by kind; every number of the law is stated as matching nature or not, never as how nature is. Table~\ref{tab:list} is the paper's list at this version: every pinned reading is a blank, since no row of the list has yet been read on the engine as it stands, and the blanks fill as each run is read and merged; the old comparison of the engine before 2026-09-23, its rows, its readings and its figures, is history in the records file \cite{records}, never carried into this table.

"""

TABLE = r"""{\scriptsize\setlength{\tabcolsep}{3pt}
\begin{longtable}{L{0.3in}L{1.25in}L{0.25in}L{1.85in}L{1.2in}L{1.0in}}
\caption{\label{tab:list}The paper's list, closed in the algebra before any run \cite{closure,approvals}: one line per row with its three checks. Kind: (K) a known formula as the thing compared with, (P) a prediction of the algebra with no known formula. Column 1, the algebra's number, a COMPUTATION declared before the run, with nature's number beside it for a (K) row; column 2, the GameBoard without pins, an exploratory reading labelled so, or not yet; column 3, the pinned reading by kind, a blank until its run is read and merged, then DETECTOR (a click, a count between clicks) or the word miss. Sources for nature's numbers as the register cites them \cite{nature}.}\\
\toprule
Row & Experiment & Kind & 1. The algebra (COMPUTATION) & 2. The GameBoard, no pins & 3. Pinned (by kind) \\
\midrule
\endfirsthead
\toprule
Row & Experiment & Kind & 1. The algebra (COMPUTATION) & 2. The GameBoard, no pins & 3. Pinned (by kind) \\
\midrule
\endhead
\bottomrule
\endlastfoot
1a & Bell's CHSH sum $S$ of a pair, two polariser tables reading the record's phase & K & the table's $\cos^2$ law on a shared record summed at the four settings, $S = 181/64 = 2.828$ at $\Nphi = 2048$, exact; nature $2.42 \pm 0.20$ \cite{hensen2015} and $2.82759 \pm 0.00051$ \cite{poh2015} & not yet: the phase-reading component and the tables & BLANK \\
1b & The CHSH sum under the phase-form window & K & $2$, a control & not yet & BLANK \\
1c & The order channel & K & on its declaration: not predicted until the order form is declared under the rule & not yet & BLANK \\
1d & No-signalling of the marginals & K & $0$ exactly by the table's symmetry, each party's $+$ fraction $32$ of $64$ at every setting & not yet & BLANK \\
2a & The two slits, one quantum at a time, the visibility & K & at or above the train's coherence value, $0.99$ at $128$ periods, the lattice's band $0.01$ ($0.959$, $0.958$, $0.958$ at $12$, $16$, $24$ Links for $32$ periods); nature $0.94$ \cite{jacques2005} & partial: the slits' exploratory page & BLANK \\
2b & The Mach-Zehnder visibility & K & $1.00 - 0.02$, the dark port $0$ of $64$ at $128$ periods; nature $0.98$ \cite{grangier1986} & not yet: the pair's two arms and the splitter's table & BLANK \\
2c & Born's exponent, the three-opening sum & K & the exponent $2$ exactly, the click a quadratic form; the sum $0$ to the remainder's grain; nature $0.0064 \pm 0.0119$ \cite{sinha2010} & not yet & BLANK \\
9 & Malus at $45$ degrees and at $11.25$, $28.125$, $33.75$ degrees & K & $128$ of $256$ at $45$ degrees, $0$ crossed, $64$ with a third between; the table's counts of $256$ at the three settings; nature $\cos^2$ & not yet on the engine as it stands & BLANK \\
10 & The single opening's spread, two halves & K & (a) $0.842$ at $w = 2\lambda$, $F = 0.16$, the Rayleigh--Sommerfeld sum on the board; (b) $0.886$ in the far field & not yet & BLANK \\
7 & The atom's lines at the coupled modes & P & the lines at the modes' own frequencies, $0.0995$ and $0.1432$ & exploratory: the coupled mode $0.09948$ within $0.3$ percent & BLANK \\
4a & The muon in flight, the moving clock at $k = 3$ & K & $0.8116$ by the one formula at the exact cone on the declared layer ($\mu = 0.15$, $s = 14$), $0.8108$ at $c_m$ and $0.8132$ at $c$ beside as controls; nature's form $1/\gamma$ \cite{bailey1977} & at rest: the period $42.364$ against $42.36$, no beat; in motion partial, the ramp redeclared & BLANK \\
4b & The moving lamp's redshift & K & $1 + z = 1.9889$ on the declared world, the free limit $1.9339$ beside; nature's form $\gamma(1 + \beta)$ \cite{botermann2014} & not yet: the redeclared geometry & BLANK \\
4c & The round-trip Doppler off a receding transponder & K & $(1 + \beta_c)/(1 - \beta_c) = 3.732$ at $k = 3$ exactly, the hop's sidebands named beside; nature the two-way form of every radar & not yet & BLANK \\
5a & The anisotropy of $c$ by direction & K & the pace by direction within $0.8$, $0.4$, $0.2$ percent of $c$ at $12$, $16$, $24$ Links, falling as the inverse square of the wavelength; nature below $10^{-17}$ \cite{nagel2015}, a bound met at the lattice's grain & not yet on the engine as it stands & BLANK \\
R2 & The Sagnac ratio on two pushed blocks & K & $\beta = v_c/c = 0.5774$ at $k = 3$ exactly, a count between clicks independent of the clock's factor; nature's coefficient $0.975 \pm 0.021$ (Michelson, Gale and Pearson 1925, to verify) & not yet & BLANK \\
LC & The light clock of two bodies & K, P & $N_0 = 218 \pm 2$ in A's clicks at $W = 64$, $2L/c = 207.85$ beside as the (K) form, (P) in the two ring-ups & not yet & BLANK \\
v & The index of a medium block at rest & K & $n^2 = 1 + Gg/(\omega_0^2 - \omega^2)$ in closed form, a control of the coupling; the cavity's mode sum beside it, the $4$ percent between them open in size & exploratory at rest: $0.01$ to $0.03$ percent from the closed form & BLANK \\
v-m & The index in motion & P & the scheme's own number on the declared geometry; Fizeau's form the declared non-match & partial: head-on $0.498$ beside & BLANK \\
ii & The moving block's clock on $64^3$, two worlds & P & $0.7814$ and $0.8032$, the controls beside & exploratory: $0.7833$ and $0.8055$ by the peak, the three gammas indistinguishable at this board & BLANK \\
M1 & Matter waves through two openings & K & the side lobe's count centroid at $y = 64 + 27.79$ for $\lambda_{\mathrm{dB}} = 12$ Links, the two-source sum with the band's $k$, the band one Node; nature's form de Broglie's & not yet & BLANK \\
M2 & The energy of a moving mass, $E = mc^2$ its rest limit & K & the first click $169 \pm 2$ intervals after the lamp's birth at the declared rung, the group transit $167.1$ beside as the form; $m = k/v_g = 1.0417$ the band's number in the form of a moving mass & not yet & BLANK \\
A & The two-pace bound on the one scale & P & the deficit $\omega_0^2/4$ of $c_m$ below $c$; with the electron's $c$ coefficient $2 \times 10^{-14}$ one interval is at most $3.6 \times 10^{-28}$ s, with the one-direction Crab bound at most $6.3 \times 10^{-31}$ s; a bound, no run & n/a & n/a, a bound \\
A2 & Light against itself, the quadratic dispersion by wavelength and direction & P & the coefficient $3\sum_i n_i^4 - 1$ in $[0, 2]$ on the sky, Eq.~\eqref{eq:dispersion}, a prediction of the form; the bound on the one scale from the burst bound on quadratic photon dispersion, about $2 \times 10^{-35}$ s, the published number recalled and not yet verified \cite{lightdispersion} & n/a & n/a, a form and a bound \\
B & The bound clock's second term & P & $\epsilon(\gamma_m^2 - 1)/2$ below $1/\gamma_m$, printed on every massive world; a bound, no run & n/a & n/a, a bound \\
\end{longtable}}

\paragraph{The derivations, final.} Four numbers of the list are the algebra's identities and stand whatever the runs read: Born's exponent $2$ exactly, the click a quadratic form (row 2c); Tsirelson's value $2\sqrt2$ as the limit of the finite-grain Bell value, the local bound beside it (row 1a); $c^2 = 1/3$, the pace of light as the norm of the flight operator, one Link per interval on every line and $1/\sqrt3$ in the Euclidean mean (row 5a); and the rest energy of a massive kind, $h\omega_0$ with $\omega_0 = mc^2$ in the law's units at the massive cone, de Broglie's internal clock as the thing compared with (row M2).

\paragraph{Under the hypothesis, after the pins and on the owner's word.} Three rows enter only under the pair-field hypothesis, a third record kind sourced by every block's content and read by every Node as its own pair, outside the law under its own identity and never in the list's place: the clock in a field at $r$ and $2r$, the ratio $2.00$ (row 12, Newton's potential from the lattice Green's function); the delay of a light pulse through a medium block sitting in the field, Shapiro's form with the same $1 + \gamma$, one declared input (in place of row 13's bending); and Newton's fall, a prediction of the form and not a pinned row (in place of row 14's orbit).

\paragraph{The rows that left the list.} Under the law as it stands the following rows of the register are not predicted, each with its missing piece named on the schedule \cite{schedule}, and their earlier readings are history in the records file \cite{records}: the far lamp (rows 3 and 11a to 11c, a crowd's field from the rule), the nuclear bindings (7a and 7b, a binding energy from the rule), the decays and the neutrino (8a to 8c, a lifetime and a mass ratio from the rule), the two arms in motion (5b, kept as the prediction page of the light-bound arms), complementarity and aberration (R5 and R6, their declarations), Bohr's ladder (6, replaced by the atom's lines), the bending (13, replaced by the delay under the hypothesis) and the period ratio (14, replaced by the fall under the hypothesis). No row is removed from the register; a row not predicted says so.

""".replace("BLANK", BLANK)

PREDICTION = r"""\paragraph{The prediction rows.} The (P) rows of Table~\ref{tab:list} are the algebra's own numbers with no known formula behind them: the atom's lines at the coupled modes, the index in motion, the moving block's clock on the two $64^3$ worlds, the ring-ups of the light clock, the two-pace bound, light's anisotropic dispersion on the sky and the bound clock's second term; each has its falsifier written before any run \cite[8.9]{algebra}, and a prediction is not a pass. The rows read on the engine before 2026-09-23, with their agreements and their disagreements, are history \cite{records}; what this version claims is the algebra's numbers before the runs, and the blanks of the table say so.

"""
