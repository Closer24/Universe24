"""Part 4 of the thirty-page assembly; see assemble.py."""

from pathlib import Path

from cut30_lib import B, cutp, sub

HERE = Path(__file__).resolve().parent
out = []
# ---- Section 8: the checks and the comparison with nature
out.append(r"""\section{The simulator's checks and the comparison with nature}\label{sec:checks}

Three things are kept apart: the checks that the code implements the
law, which are computations; the numerical checks of the formulas after
a detector, which are measurements of the simulator; and the
comparisons with measurements of nature.

\paragraph{The code implements the law.} Every registered world is run
from its world file with its expectation written before the run and its
source fingerprint; a second runner re-ran the worlds of series L, T and
fifteen more from the register at main and compared every field bit by
bit \cite{replications}; the books balance at every interval in every
run; the engine's inverse interval returns a world without a measured
event to its birth; the rounding pins were met before the run ($63/1$
at $\Nphi = 64$, $31/1$ at $32$, $125/3$ at $128$ for the $(3, 4)$ split);
the crossing rule's tests read $k + 55/32$ rows per $k$ intervals
toward a moving source, $k - 55/32$ away and $k$ at rest. These are
gates on the code, not measurements.

\paragraph{The formulas after a detector.} Every number of
Table~\ref{tab:checks} is a count of clicks or a click's tick at a
declared detector, registered with its fingerprint; a number of the
board appears nowhere.

{\scriptsize\setlength{\tabcolsep}{3pt}
\begin{longtable}{p{1.25in}p{1.35in}p{1.65in}p{1.7in}}
\caption{\label{tab:checks}The representative detector checks of the formulas. Series L's runs carry the source fingerprint \texttt{ff5c382d672f}, L7's \texttt{4bf55a62e6fd}, series S's \texttt{24e0c1ba}, series T's \texttt{afb533a} \cite{register,replications}; each expectation was written before its run.}\\
\toprule
Formula & Run (series, world) & Detector reading & Expected before the run \\
\midrule
\endfirsthead
\toprule
Formula & Run & Detector reading & Expected \\
\midrule
\endhead
\bottomrule
\endlastfoot
$c = 1/\sqrt3$, isotropic within $1/T_D$ & Q, the $290$ directions; L7, the cone & $290$ of $290$ face clicks at the derived interval, Node and face, the pace $0.5718$ to $0.5893$; the two rows' counters at the age $29$ & the flight table's ticks; the same age \\
The click's weight, power $2$ & L, the $(3, 4)$ split at $\Nphi = 64$, $32$, $128$; the far pair & $63/1$; $31/1$; $125/3$; the cells $27, 5, 5, 27$ & the same, pinned; the power's window $[1.917, 2.012)$ \\
Interference of one record & L, Mach-Zehnder, equal arms; half turn; quarter turn & $64/0$; $0/64$; $32/32$ over $64$ births & the same \\
Young's spacing & L2b, two slits under the birth wheel, $4096$ births & the bright pixels $19$ to $51$, the dark $0$ to $3$, the visibility $0.966$ in the clicks & the dark pixels as pinned; the rungs within one \\
Exact marginals & L, the pair at $\Nphi = 64$, all setting bins & $32/64$ for each party in every registered bin & Theorem~\ref{th:marginals} \\
$S(\Nphi)$ & L, the pair at $\Nphi = 64$, $512$, $1024$, $4096$ & $176/64$; $1448/512$; $2896/1024$; $11584/4096$ & the same, Theorem~\ref{th:bell} and its closed form \\
GHZ & L, XXX and XYY, YXY, YYX & the four allowed triples $16$ each, the products $+1$ and $-1$; the others $0$ & the same \\
Malus's law & A12, one polariser at $45$ degrees; two crossed; $22.5$ degrees & $128$ of $256$; $0$ of $256$; $219$ of $256$ & the same, from the tables \\
The clock's field at two Nodes (the continuum's $1/r$ its limit) & T, a lamp's births at a detector, two sources at $3$ and at $6$ Links & the ratio of the two shifts $1.907$ (age word); $1.000$ (presence word) & the lines' pin $1.909 \pm 0.05$; replicated \\
The covariant readings (a hypothesis beside the law) & S, the muon at rest, at $0.43c$, at $0.86c$; the coasting star & the electron's face clicks at $392$, $369$, $345$; $z = 0.3674$ (arithmetic on the click ticks) & $391$, $367$, $345$ within two; $0.369 \pm 0.003$ \\
Light beside a mass & K, three worlds, the screen's clicks & the deflection $0.000$ pixel, the delay $0.00$ interval & the same: the flight blind to the crowd \\
The weak forms & J1, the neutron's decay clicks; J2, the second detector & the width over the median $0.036$ and $0.038$ over $64$ clicks; $16$ of $1024$ with $0$ behind & a step; a window \\
\end{longtable}}

\paragraph{The comparison with nature.} The confrontation register
\cite{nature} keeps one row per registered detector reading with a
dimensionless counterpart in nature, under one parameter set, one
published source per value and one verdict per row: PASS within the
stated uncertainty, FAIL with the number, BOUND where the comparison
bounds a free parameter. A FAIL is a result of the law and is stated
with the same care as a pass. Table~\ref{tab:nature} carries the rows
read after a detector; seven rows of the register rest on a pin whose
run is not made (the muon's lifetime in flight under the law, 4a; the
two-arm anisotropy, 5b; Bohr's ratio, 6; the single opening, 10; the
far lamp's brightness, stretch and surface brightness, 11a to 11c) and
carry no number here. Every verdict is the law's as built at the merge
commit named in Appendix~\ref{app:reproduction}; a hypothesis's PASS
beside the law never changes the law's FAIL.

{\scriptsize\setlength{\tabcolsep}{3pt}
\begin{longtable}{p{0.3in}p{2.0in}p{1.5in}p{2.2in}}
\caption{\label{tab:nature}The confrontation register's rows read after a detector \cite{nature}. Four PASS (each replicated by the second runner \cite{replications}), twelve FAIL (eight in a registered run, four by a pin without its run, the latter not in this table), one BOUND, one declared input against nature, one row under an assumed word of the clock.}\\
\toprule
Row & Observable and nature's value & The law's detector reading & Verdict \\
\midrule
\endfirsthead
\toprule
Row & Observable and nature's value & The law's detector reading & Verdict \\
\midrule
\endhead
\bottomrule
\endlastfoot
1a & The CHSH sum of a pair: $2.42 \pm 0.20$ \cite{hensen2015}; the quantum bound $2.828$ & $S = 2.75$ at $\Nphi = 64$, series L & PASS: $1.65$ standard errors above the measured, $0.078$ below the bound \\
1b & The same, the phase-form window & $S = 2$ exactly & FAIL: the local bound, $2.1$ standard errors below \\
2a & Two-slit visibility of one quantum at a time: $0.98$ \cite{grangier1986} & $0.966$ in the clicks under the birth wheel, $4096$ births (L2b) & FAIL by $0.014$; the cause named, the fan's grain \\
2b & Mach-Zehnder visibility: $0.98$ & the clicks $64/0$ & PASS: $0.9988$ \\
2c & The power of the click's form: the Sorkin parameter $\kappa = 0.0064 \pm 0.0119$ \cite{sinha2010} & the power's window $[1.917, 2.012)$ from the click cells & PASS on the power: the window contains $2$; $\kappa$ an observable the law does not compute here \\
3 & The deceleration parameter $q_0 = -0.53 \pm 0.01$ \cite{planck2018,riess1998,perlmutter1999} & $-0.108$ coasting (series G2, the pointer's $z$; reproduced at head as a verdict with the digits moved, $-0.104$, record 408 \cite{log}) & FAIL: no term with $q < 0$ \\
4b & A moving lamp's redshift with the clock's factor \cite{botermann2014} & $z = 0.2636$ at $\beta = 0.2674$ (series G2, read before the crossing rule; not reproduced at head, the re-run pending under the age word) & FAIL: $0.315$ expected, $17$ grains below; under covariant-readings-v1 the same star reads $0.3674$ for the pinned $0.369 \pm 0.003$ (series S), the law's row stays FAIL \\
5a & The anisotropy of $c$ by direction, below $10^{-18}$ \cite{nagel2015} & the pace $0.5774$ to $0.5818$ at $N_l = 64$ (series Q) & BOUND on $N_l$: of order $5.8 \times 10^{17}$ \\
7a & The deuteron's binding fraction $0.1185$ percent \cite{ame2020} & the escaped content and the mass a detector reads on the lifetime border (series N): the held bond $0.109$ percent & BOUND on a declared input \\
7b & The alpha's binding over the deuteron's, $12.72$ \cite{ame2020} & $2.0$ (series N, the border's clicks) & FAIL: a factor $6.4$; the give once per body \\
8a & The neutron's decay curve, exponential, width over median $3.17$ \cite{gonzalez2021} & $0.036$, a step (series J1, $64$ clicks) & FAIL: a factor $88$ \\
8b & The neutrino's passage through a second detector, about $1$ & $16$ of $1024$ with $0$ behind (series J2, a window) & FAIL \\
8c & The heaviest neutrino mass state over the electron's mass: at least $9.8 \times 10^{-8}$ \cite{pdg2024,katrin2022} & the \texttt{nu} family with no content, an input & a declared input refuted by nature: massless states cannot carry the observed splittings; a content above $0$ is an input the register does not declare \\
9 & Malus's law at $45$ degrees, $1/2$ & $128$ of $256$ exactly; $219$ of $256$ at $22.5$ degrees (A12) & PASS: exact at $45$ and $90$ degrees; $0.8555$ against $\cos^2 = 0.8536$ at $22.5$ \\
12 & The clock's field at two distances at the same push: the potential's form, $2.00$ (the GPS term $45.7$ microseconds per day \cite{ashby2003}; \cite{pound1960,delva2018}) & series T: the form measured at a detector at two Nodes, the age clock $1.907$ (the lines' pin $1.909 \pm 0.05$), the presence clock $1.000$; the continuum's $1/r$ a limit under the shell's average & PASS under the age word, the clock's word by assumption (P9), nature's $2.00$ $4.6$ percent away; FAIL under the presence word \\
\end{longtable}}

\paragraph{The prediction, and the failures.} Against the photon-pair
value $S = 2.82759 \pm 0.00051$ \cite{poh2015}, under three assumptions
the paper states and does not defend (that nature's pairs are this
model's pairs at some $\Nphi$, that fair sampling holds, and that the
experiment's four settings are the model's labels), the law's $181/64$
stands $1.05$ standard errors above, $16384$ and $32768$ at $2.0$,
$65536$ and beyond at $1.5$ to $1.65$; $\Nphi = 64$ ($152$ standard
deviations) and $256$ ($30$) are excluded; the loophole-free
\cite{hensen2015} excludes no $\Nphi$; \cite{giustina2015,shalm2015}
report a quantity whose comparison needs a detector efficiency the
model lacks. The proximity is a compatibility, not an advantage over
quantum mechanics, whose bound the law approaches from below on this
range; what refutes it is a CHSH measurement with an uncertainty below
$1 \times 10^{-4}$ reading a deficit below $2 \times 10^{-4}$ or above
$4 \times 10^{-4}$. The failures are the law's own results: the
unslowed clock (4b, and 4a by its pin), the deceleration (3), light
unbent (Section~\ref{sec:delay}, against $1.75$ arcseconds), the weak
forms (8a, 8b), the strong ratio (7b), the two-slit visibility by the
fan's grain (2a), the phase-form window (1b), the massless neutrino
(8c); each refutes the law as declared on its own, and no count of
passes weighs against them.

""")

# ---- Section 9: discussion
out.append(r"""\section{Discussion and conclusions}\label{sec:discussion}

\paragraph{What is proved.} Exact on the GameBoard: the group of the six
Ports and its $24$ rotations; the books' conservation and the continuity
equation; the split's isometry and the injectivity of the interval on
the rows' weights, multiplicities and phases; the pace bound $1/\sqrt3$;
the click's weight a positive quadratic form of power $2$ under the
axioms (a) to (e); the exact marginals of a pair; the CHSH sum as an
exact function of the grain and the tables, with its closed form. In
the limit of the grain, with a rate: Born's rule to $1/(2\Nphi)$ per
cell, Tsirelson's bound to $8/\Nphi$, Young's spacing, the attained
value of $c$, Planck's and de Broglie's identities. In the limit over a
dense fan, with the condition in the claim: Gauss's law of the field,
Newton's and Coulomb's inverse square, the retarded potential and
Poisson's equation, the clock's $1/r$ form.

\paragraph{What the runs support and what nature says.} After a
detector the simulator reads the pace and its isotropy, the click's
cells and the power's window, $S$ at four grains, the interference of
one record, GHZ's triples, Malus's law and the clock's form at two
distances, each inside an expectation written before the run
(Table~\ref{tab:checks}); nothing of the board is read as a
measurement. Against nature four readings pass, twelve fail
(Table~\ref{tab:nature}), and the three decisive failures, the unslowed
clock in motion, light unbent beside a mass and the coasting
deceleration, each refute the law as declared.

\paragraph{The distance, stated.} What is established now is an
explicit model with the exact and conditional results above and their
numerical checks after a detector. What the broad claim still needs,
and the check that would decide each:

{\small
\begin{longtable}{p{2.2in}p{4.0in}}
\caption{\label{tab:distance}What no rule of the law forces, and the check that decides each; the hypotheses beside the law are listed on the tree under their identities \cite{hypotheses}.}\\
\toprule
Needed & The deciding check \\
\midrule
\endfirsthead
\toprule
Needed & The deciding check \\
\midrule
\endhead
\bottomrule
\endlastfoot
Newton's and Poisson's laws measured after a detector & a body carrying a lamp beside a source, its births' Doppler read at a detector over time; a face detector's count of the escape against the release; the clock's form at more distances (series T's method) \\
The Lorentz factor: no rule of the six reads a body's momentum into its clock, and a boost is not among the $48$ & the muon in flight under the law (row 4a, a pin: the counter at the rest rate); beside the law, the covariant readings (a body's energy as an exact square, its counts gated by $E_0/E$; series S's face clicks inside their pins on one axis) against the same pins \\
The bending of light: the flight is blind to the crowd & a rule under which a row's wall reads the crowd's age moment (built as a hypothesis with a coefficient that is an input, the six operations giving Newton's half) run against nature's $1.75$ arcseconds \\
The values of the masses: every rule is linear in the content, so every equal split is a fixed point and none is selected; the law gives floors only & a nonlinear closure on the amounts under its own identity; until then the family table is an input \\
The harmonic constants of the click: the axioms admit every Galois conjugate & the least-rank click, an axiom of the apparatus, pinned by the two-slit period and Malus at $22.5$ degrees; not derived \\
A CHSH measurement at $10^{-4}$ & decides $181/64$ against $2\sqrt2$ \\
\end{longtable}}

\paragraph{The limits, and what does not return.} Tsirelson's value is
a limit of the two terms of Theorem~\ref{th:bell}; the light cone is the
octahedron scaled by the age, isotropic within $1/T_D$; the content and
$\sum w^2/\mathtt m$ are conserved exactly, the offered norm only within
the tables' rounding. The GameBoard and its interval are a rest frame,
and Lorentz invariance is not a limit of the model but a property it
must show or lack: the law as declared predicts a body's counter at the
rest rate at every speed and the Doppler $1 + \beta$ without the
clock's factor, falsifiable rows (4a, 4b); the owner's decision (record
270 \cite{log}) keeps that prediction and builds the covariant readings
beside it as a hypothesis against the same pins, in its one-axis domain.
Einstein's field equation is not reached. Everything the program
stated beside the law, the hypotheses under their identities with what
would close and what would refute each, is on the tree \cite{hypotheses}
and claimed nowhere here.

\paragraph{Positioning.} The click is a non-local step, forced by
Bell's theorem because the marginals are exact and $S > 2$
\cite{bell1964,chsh1969}; no-signalling is Theorem~\ref{th:marginals},
as it is a theorem of quantum mechanics \cite{grw1980}. The click's
finite kinematics is Weyl's and Schwinger's on $\Z_{\Nphi}$
\cite{weyl1931,schwinger1960}; the pace $1/\sqrt3$ is the cubic
lattice's Courant bound \cite{cfl1928} and the lattice Boltzmann sound
speed \cite{qian1992}; the transport is a lattice gas's exact integer
dynamics \cite{hpp1976,fhp1986} with the click's reading of one record
added, a walker free of dispersion where the lattice automata of
\cite{bialynicki1994,meyer1996,arrighi2019} disperse; the uniform $u$
and the ruler do the work of quantum equilibrium in Bohm's theory
\cite{bohm1952,dgz1992}; the model is $\psi$-ontic in the classification
of \cite{spekkens2007,hs2010}; Theorem~\ref{th:bell} puts $S(\Nphi)$ on
both sides of Tsirelson's bound \cite{tsirelson1980,pr1994}; the
experiments the checks are named for
\cite{tonomura1989,grangier1986,ghsz1990,ev1993} are reproduced in none
of their own geometries. The declared rounding of the circle's tables
has its precedents in the fixed-point transforms of signal processing
\cite{malvar2003,welch1969,mathews1963,goodman1970}. The earlier testbed of this program \cite{paper1}, with its draw and its
return, is history: no rule of it survives here.

""")

# ---- Appendices
out.append(r"""\appendix
\small

\section{Auxiliary proofs}\label{app:proofs}

\paragraph{Proof of Theorem~\ref{th:group}.}
""")
pg = B("A map of the six Ports that keeps opposite Ports opposite permutes the", "\\end{proof}")
pg = cutp(pg, "; series P's parity worlds with an", "That the\nsix operations commute")
pg = (
    sub(pg, "by definition. That the", "by definition. That the")
    if "by definition. That the" in pg
    else pg
)
out.append(pg.rstrip() + "\n\n\\paragraph{Proof of Theorem~\\ref{th:isometry}.}\n")
pi = B(
    "$\\sum_i (wa_i)^2/(\\mathtt m A) = w^2 \\sum_i a_i^2/(\\mathtt m A) = w^2/\\mathtt m$.",
    "\\end{proof}",
)
out.append(pi.rstrip() + "\n\n\\paragraph{Proof of Theorem~\\ref{th:bijection}.}\n")
pb = B("$F$ maps a basis element to a basis element and is injective because the", "\\end{proof}")
out.append(pb.rstrip() + "\n\n")

out.append(r"""\section{Technical details}\label{app:technical}

\paragraph{The tables and their rounding.} """)
tab = B(
    "The circle is $\\Z_{\\Nphi}$ with $4 \\mid \\Nphi$. The tables are",
    "\\paragraph{The pace of the rows, and the octahedron.}",
)
tab = tab.replace("Section~\\ref{sec:newton}", "Section~\\ref{sec:forces}")
out.append(
    tab.rstrip()
    + " The integer Mach-Zehnder's total over the $64$ birth phases takes eight values from $65448/65536$ to $65773/65536$, the same eight on every one of its ten worlds \\cite{register}; the normalisation by $C_K$ in Eq.~\\eqref{eq:rung} makes the click's probabilities sum to one at completion, and the paper claims exact unitarity nowhere.\n\n"
)
out.append(r"""\paragraph{The symbols.} """)
nt = B("{\\small\n\\begin{longtable}{p{1.9in}p{1.05in}p{3.5in}}", "\\part{The formula}")
nt = nt.replace("{\\small", "{\\footnotesize", 1).replace(
    "p{1.9in}p{1.05in}p{3.5in}", "p{1.75in}p{1.0in}p{3.3in}"
)
nt = nt.replace("Section~\\ref{sec:newton}", "Section~\\ref{sec:forces}")
out.append(nt.rstrip() + "\n\n")

out.append(r"""\section{Reproduction}\label{app:reproduction}

""")
rep = B(
    "The code, the worlds of series L with their expectation file written",
    "The long form of this manuscript",
)
rep = rep[: rep.index("The commits the body refers to here")].rstrip() + "\n"
rep = sub(
    rep,
    "the runs' summary and the two figure scripts are archived\n\\cite{zenodo}; the register entry of series L carries every run's world,\nduration and source fingerprint, and a table beside the manuscript maps\neach number of this paper to its source.",
    "the runs' summary and the two figure scripts are archived \\cite{zenodo}; the register entry of each series carries every run's world, duration and source fingerprint, and NUMBERS.md beside the manuscript maps each number of this paper to its source \\cite{checks}.",
)
out.append(rep.rstrip() + "\n\n")
long = B("The long form of this manuscript", "\\section*{Use of AI tools}")
long = sub(
    long,
    "this paper is its cut to what is\nproved, measured or replicated, and cites the tree for the rest.",
    "this paper is its cut to what is proved, measured after a detector or replicated, built around the general formula; the forty-page cut before it is at the commit \\texttt{b0d1ebf7}; the tree cited for the rest.",
)
out.append(long.rstrip() + "\n\n")
ai = B("\\section*{Use of AI tools}", "\\begin{thebibliography}{99}")
ai = ai.replace("\\section*{Use of AI tools}", "\\paragraph{Use of AI tools.}")
out.append(ai)
bib = B("\\begin{thebibliography}{99}")
bib = bib.replace(
    "\\bibitem{terminology} Canonical simulation terminology,",
    "\\bibitem{hypotheses} Hypotheses under test, entry 27, the conditional derivations as declared hypotheses, \\texttt{docs/HYPOTHESES.md} of the archived code \\cite{zenodo}.\n\\bibitem{terminology} Canonical simulation terminology,",
    1,
)
out.append(bib)
open(str(HERE / "part4.tex"), "w").write("".join(out))
print("part4 ok", sum(len(x) for x in out))
