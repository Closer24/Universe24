"""Part 1 of the thirty-page assembly; see assemble.py."""
from pathlib import Path

from cut30_lib import B, cutp, sub

HERE = Path(__file__).resolve().parent
out = []
# ---- preamble and title (the base's, unchanged)
pre = B("\\documentclass", "\\begin{abstract}")
pre = pre.replace("\\usepackage{longtable}\n", "\\usepackage{longtable}\n\\usepackage{array}\n")
out.append(pre)
out.append(r"""\begin{abstract}
One update law of bounded integers, applied at every Node of a cubic
GameBoard at every interval, is stated as one map with a rate and a wall
per component; its rates and walls are made of six integer operations,
and one comparison, the click, is its only read-out. The paper asks how
much of physics that map forces with few assumptions, and answers in one
ledger, result by result. Exact on the GameBoard: the conservation of
the books and a continuity equation, the pace bound $1/\sqrt3$, the
click's weight a positive quadratic form of power $2$ under one axiom of
the apparatus, the exact marginals of a pair, and the CHSH sum as an
exact function of the grain, $181/64$ at the powers of two from $512$
to $8192$. In the limit of the grain: Born's rule, Tsirelson's bound,
Young's spacing, Planck's and de Broglie's identities. In the limit over
a dense fan of directions: Gauss's law, Newton's and Coulomb's inverse
square, the retarded potential and Poisson's equation. What no rule
forces is said in the same ledger: the Lorentz factor, the bending of
light, the values of the masses, the harmonic constants. After a
detector the simulator confirms the exact results and the pace; against
nature four readings pass and twelve fail, the failures the law's own.
One prediction: $S = 181/64$, inside Poh et al. at $1.05$ standard
errors.
\end{abstract}

\section{Introduction}\label{sec:intro}

\paragraph{The general formula.} The law is one map $\bPhi$ applied at
every Node of the GameBoard at every interval, per component $s$ of the
state, each with its own rate $r$ and wall $d$:
\begin{equation}\label{eq:map}
s \leftarrow s + r, \qquad e \leftarrow \operatorname{sign}(s)\,\min\!\left(\lfloor |s|/d \rfloor,\ a\right), \qquad s \leftarrow s - e\,d .
\end{equation}
Each component of the state is a bounded integer accumulator with a
declared rate and a declared wall: it is translated by its rate,
counted in walls (capped at $a = 1$ for the drive, uncapped elsewhere),
and reduced by the walls it holds; every wall counted is an event, a
Link crossed, a phase step taken, a count completed, a birth, a push,
and nothing else happens. The rates and walls are made of six integer
operations and nothing else: the translation, the multiplication by a
declared integer matrix or bilinear form, the sum in the group ring of
the phase circle, a permutation, the evaluation of a record at the
roots of unity with its norm, and the division with the remainder kept
together with the comparison that is the event. One comparison, the
click, is the only read-out, and only a detector's reading is a
measurement. Section~\ref{sec:law} gives the full definition; every
derivation of this paper names which of these rules it starts from.

\paragraph{The claim and the question.} The claim of the paper is that
several different physical phenomena are produced from this one
discrete update law and a small number of assumptions: the geometry of
propagation, the flux and the forces, and further the measurement and
its correlations. The decisive question is how much of that the law
really forces. If every phenomenon needed a rule that puts its result
in beforehand, the law would explain nothing; if the same rules force
several results with little freedom, that is the contribution. So the
paper keeps one ledger (Table~\ref{tab:ledger}): for every result, the
rules of Eq.~\eqref{eq:map} it starts from, the assumptions added beside
them with their kind, the freedom left, and the ground on which the
derivation stands, exact on the GameBoard, a limit of the grain, or a
limit under a spatial condition. The three things work together: the
formula defines the mechanism, the derivations show what follows and
under what conditions, the simulator and the comparison with experiment
check the results and their limits. What can be established now is an
explicit model, a set of exact and conditional mathematical results, and
numerical checks after a detector; the broad claim that the model
describes nature still needs the completions Section~\ref{sec:discussion}
names, and the paper is built around the precise distance between the two.

\paragraph{How the simulator led to the results.} The simulator ran
first and the derivations followed it. Every run was registered with
its expectation written before the run, its world file and its source
fingerprint; a second runner re-ran each registered world from the
register and compared bit by bit; and each registered number was then
traced back to the operations of the map until a derivation stood or the
number was marked a finding. The lattice Gleason theorem
(Section~\ref{sec:measurement}) came from a click count, $63$ of $64$
births in one channel of an unbalanced splitter, which pinned the power
of the click's weight to a window containing $2$ and excluding $1$ and
$3$ before the form was proved; the exact CHSH function $S(\Nphi)$
(Section~\ref{sec:bell}) came from three registered values, $176/64$,
$2896/1024$ and $11584/4096$, whose pattern the closed form then
explained through $8192$ and beyond; the pace $c = 1/\sqrt3$ came from
a cone world in which two rows on different digital lines reached their
counters at the same age. Where a derivation closed, the paper says
``derived from the update rules implemented in the simulator''; a
relation found in runs alone is a numerical finding; a relation defined
in advance is a definition or an input.

\paragraph{The map of results.} Proved: the theorems of
Sections~\ref{sec:geometry} to~\ref{sec:bell} (the group of the six
Ports, the pace bound, the lattice Gleason form, the isometry and the
injectivity of the interval, the exact marginals, the finite-$\Nphi$ Bell
value). Shown numerically after a detector: the pace and its
isotropy, the click's cells and the power's window, $S$ at four grains,
Malus's law, the clock's field at two distances
(Section~\ref{sec:checks}). Open, with the check that decides each: the
measurement of Newton's and Poisson's laws after a detector, the clock
of a body in flight, the bending of light, the values of the masses, the
harmonic constants (Section~\ref{sec:discussion}).

\paragraph{The reading rule and the notation.} Only a detector's reading
is a measurement: a click, a record's moments or an external thing's
reading, as the world file declares. A number of the GameBoard's state is
a diagnostic of the host, never compared with nature and never pinned,
and none appears in this paper as a check. Every symbol is named in
English at its first use, a scalar plain, a vector in bold lowercase,
a matrix or an operator in bold uppercase; the symbol table is
Appendix~\ref{app:technical}, the program's glossary is on the tree
\cite{terminology}, and every number has its one source \cite{checks}.
""")

# ---- Section 2: the law and its implementation
out.append(r"""\section{The law and its implementation}\label{sec:law}

\paragraph{Rules, parameters, initial conditions.} The law is stated as
rules, apart from the parameters and the initial conditions a world
supplies. The rules: (P1) every quantity of the state is a bounded
integer and every operation integer arithmetic, no real number, root or
floating point at run time; (P2) space is a cubic array of Nodes, each
joined to six neighbours by Links through directional Ports, a Node's
complete local information its NodeState, time a sequence of intervals;
(P3) the rates and walls of the map are made of the six operations of
Section~\ref{sec:intro} and nothing else; (P4) a rule reads its own
record and the arrivals at its Node and its six neighbours, already
delivered, and nothing kept at a Node beyond the events there, no
register, remainder or draw; (P5) no row or body crosses more than one
Link per interval; (P6) a record is read out once, by one comparison,
at the click, the one step that deletes, and the click of a pair is one
gather of one record from both settings, the law's one non-local
operation. The parameters (P7, P8): the grains, the circle $\Nphi$, the
pace's grain $N_l$, the sphere of directions, the birth wheel $N_u$, the
fan's grain, the clock's pair, and the roundings declared at load,
among them the circle's tables at $1/256$; and the physical inputs, the
family table (per family the content, the cost $h$ per phase step, the
charge per unit of content, the strong column, the lifetime, the phase
rate and the hand; its instance on the tree \cite{familiesaudit}) and
the world's width $N_w$, which carries what physics calls Newton's
constant. The initial conditions: the box and its boundaries, the
bodies with their momenta and contents, the lamps, the detectors, the
splitters and the gates of the world file. Four rules are chosen among
few (P9) and are assumptions, not derivations: the flight is blind to
the crowd, a row's rate in transit constant and its wall the direction's
$T_D$; a body's drive is the flight at the fraction its momentum earns,
$|p_a|/(N_l N_w M + |p_a|)$ per axis; the collision's permutation is
the cyclic shift; and a clock counts the age moment of the rows at its
Node (the potential's form, the owner's word of record 394 \cite{log})
rather than their presence. One axiom of the apparatus (P10): the click
stores one pointer per set, the least-rank member of the family
Theorem~\ref{th:gleason} forces, which is Born's form with the
fundamental harmonic; which harmonic is a relabelling of the declared
rate, and the harmonic constants are not derived. Nothing outside this
list is assumed.

""")
# the map's definition and the six operations, from the base
m = B("Here $s$ is one accumulator of the state", "\\paragraph{From the Node to the group")
out.append(r"""\paragraph{The map.} """ + m)
# the state, the components, the two blocks, the read-out
st = B("\\paragraph{The state.}", "\\paragraph{The components of")
st = sub(st, "(the fields per kind and the six verbs on them, F4 of the families' tables \\cite{familiesaudit}).", "(the fields per kind on the tree \\cite{familiesaudit}).")
out.append(st)
comp = B("\\paragraph{The components of", "\\paragraph{The two blocks.}")
comp = sub(comp, "The ladder's rungs $\\rung_k$ of Part~III are walls of this kind. The components", "The ladder's rungs $\\rung_k$ of Section~\\ref{sec:measurement} are walls of this kind. The components")
comp = sub(comp, "written $n/d$ in Part~III, its", "written $n/d$ in Section~\\ref{sec:measurement}, its")
comp = cutp(comp, "one row of the lamp's counts table, giving", "$[2531, 4096]$ on the registered")
comp = cutp(comp, ", the click's one Euclidean division with its remainder kept, from the row's two counts", "\\cite{beamlaw}; and")
out.append(comp)
blocks = B("\\paragraph{The two blocks.}", "\\paragraph{The read-out.}")
blocks = sub(blocks, "and the limits of Part~II are limits of that formula.", "and the limits of Sections~\\ref{sec:forces} and~\\ref{sec:delay} are limits of that formula.")
blocks = cutp(blocks, "What each rule reads is audited rule by rule", "\n\n")
blocks = blocks.rstrip() + "\n\n"
out.append(blocks)
ro = B("\\paragraph{The read-out.}", "\\paragraph{The law in five statements.}")
ro = sub(ro, "forced in form by Section~\\ref{sec:gleason} and free in its constants", "forced in form by Theorem~\\ref{th:gleason} and free in its constants")
out.append(ro)
out.append(r"""\paragraph{A hand-worked update.} A row on the heading $+x$ has the
flight accumulator's rate $2S_1N_l = 128$ ($S_1 = 1$, $N_l = 64$) against
the wall $2T_D$ with $T_D = \lfloor\sqrt{3 \cdot 64^2}\rfloor = 110$, so
$2T_D = 220$, started at $T_D = 110$. Interval by interval the
accumulator reads $238$ (one wall counted: a Link, the remainder $18$),
$146$ (none), $274$ (a Link, $54$), $182$ (none), $310$ (a Link, $90$),
$218$ (none), $346$ (a Link, $126$), $254$ (a Link, $34$): Links at the
intervals $1, 3, 5, 7, 8, \dots$, five Links in eight intervals, and in
the long run $128/220 = 0.5818$ Links per interval, the heading's pace
of Section~\ref{sec:geometry}. The same three lines of
Eq.~\eqref{eq:map} run the phase (the rate the family's turn, the wall
$\Nphi$), a body's owed count and every other component; only the rate and
the wall differ.

\paragraph{In the code.} The engine realises Eq.~\eqref{eq:map} as one
accumulator per component with its rate and wall read from the world
file, the carry as the event, in six steps per interval: departures
become arrivals (the walk), the readings at each Node (the presence,
the age moment and the first moment of the arriving rows), the
collision, the measured events' tables and the detectors, the
self-creations, and the border's lifetime with the merge of identical
rows \cite{beamlaw,engine}. A world file declares the parameters and
the initial conditions and nothing of the rules; the same engine runs
every world of this paper.

""")

out.append(r"""\paragraph{The ledger.} Table~\ref{tab:ledger} is the paper's spine:
for every result, the rules of Eq.~\eqref{eq:map} it starts from, the
assumptions added beside them with their kind, the freedom left, and
the ground of the derivation (the owner's decision of 2026-09-22
\cite{highlights}): exact on the GameBoard (no limit, no
average), a limit of the grain taken on paper with a rate, or a limit
under a spatial condition, an average that covers the shell (over the
shell's Nodes, over the directions of a fan declared in a ball, or over
the sweep of an orbit), the condition then part of the claim. A result
whose derivation is not closed, or whose only reading is of the board,
is not in the table; the hypotheses beside the law are on the tree
\cite{hypotheses}.

{\scriptsize\setlength{\tabcolsep}{3pt}
\begin{longtable}{p{1.3in}p{1.5in}p{1.45in}p{0.85in}p{0.85in}}
\caption{\label{tab:ledger}The forcing ledger. Ground: exact, on the GameBoard, no limit and no average; limit, of the grain, taken on paper with its rate; fan, a limit under an average that covers the shell, the condition part of the claim. A detector reading never lifts a claim from fan to exact: what a run establishes is a lattice-exact claim about the world at hand, whose agreement with the continuum's form within the named ripple is evidence for the fan claim, not its proof. The section is this paper's; the derivation's section is \cite{derivations}'s.}\\
\toprule
Result & Rules it starts from & Assumptions added (kind); freedom left & Ground & Section \\
\midrule
\endfirsthead
\toprule
Result & Rules & Assumptions; freedom & Ground & Section \\
\midrule
\endhead
\bottomrule
\endlastfoot
The books' conservation; the continuity equation & the carry (a bijection), the split and rotation matrices & none & exact (the lattice identity); limit (the differential form) & \ref{sec:forces}; 25.4 \\
The group of the six Ports, $48$ and $24$ & the six Ports, the hand bit & none & exact & \ref{sec:geometry} \\
The pace of a direction $N_l|D|/T_D$, isotropic within $1/T_D$; the Manhattan bound $S_1 N_l \le T_D$ & one Link per interval, the digital line & none; the wall $T_D$ a rule chosen among few (P9); $N_l$ free & exact & \ref{sec:geometry}; 13.2 (a) \\
The value $c = 1/\sqrt3$ attained & the same & none & limit (the grain $N_l$) & \ref{sec:geometry}; 1.4 \\
No dispersion & the flight table indexed by direction and age & none & exact & \ref{sec:geometry} \\
Gauss's law of a free family's flux & the walk, the books & a closed surface no periodic axis crosses, no absorber inside (a declared world condition) & exact & \ref{sec:forces}; 3.1 \\
The equivalence principle; the third law at rest & the step rule (divides by the content); the books & none & exact & \ref{sec:forces}; 3.3 \\
Newton's inverse square; $G = K\eta/(4\pi N_w)$ & the bilinear push on the arriving rows' first moment & two additivities (24.2); an average that covers the shell; $N_w$ an input & fan & \ref{sec:forces}; 3.2, 3.3 \\
Coulomb's law with $k_C = G$ & the charge column of the push & $\rho$ an input; the same average & fan & \ref{sec:forces}; 3.4 \\
The retarded potential and the retarded wave equation; Poisson's equation & the release, the flight, the age moment & the same average, the dwell direction-blind, the open box & fan & \ref{sec:delay}; 5.1, 5.5 \\
The Li\'enard--Wiechert potential of a moving source, first order & the same & the same, the fan's grain & fan & 12.1 \\
The clock's rate $1/(1 + a_\tau)$, never $0$ at a finite count (no horizon) & the owed count & the age moment as the clock's word (P9) & exact & \ref{sec:delay}; 5.2 \\
The clock's $1/r$ form; its calibration & the same & the $1/r$ form the same average; the calibration $a_\tau = GM/rc^2$ an input of the dictionary & fan (the form); input (the calibration) & \ref{sec:delay}; 5.2 \\
The click's weight a positive quadratic form of power $2$ & the evaluation at the roots of unity, the phase rotation & the balanced splitter's conservation (an axiom of the apparatus); the harmonic constants free; the least-rank click (P10) & exact & \ref{sec:measurement}; 6.5, 6.6 \\
Born's bound: a cell within $1/\Nphi$, the cumulative within $1/(2\Nphi)$; Born's rule as its limit & the ladder's rungs & the uniform birth phase (a fact of the source) & exact (the bound); limit (the rule) & \ref{sec:measurement}; 6.2 \\
The entropy identity; the entropy produced only at the click, the cancel and the leaks, a count of torus points; Boltzmann's $S = k\log W$ & the click's one deletion & the coarse graining (a definition); no second law claimed & exact & 14, 16.1 \\
The split an isometry; the interval injective on the amplitudes & the six operations & none & exact & \ref{sec:measurement} \\
Planck's $E = hf$; de Broglie's $\lambda = h/p$ & the release's cost rule, the turn rule & the dictionary $h = h_q\Nphi = h_A$, an input & exact (identities under the dictionary) & \ref{sec:measurement}; 6.4; 21.2 rows 51, 52; 24.1 row 25 \\
Young's spacing & two paths' phase difference & the fan's grain & limit & 7.1 \\
The uncertainty relation's bounds on $\Z_{\Nphi}$ & the evaluation & the circle as position, its transform as momentum: a hypothesis & exact (the bounds) & \ref{sec:measurement}; 22 \\
Exact marginals; no-signalling & the one gather, the nearest rung & equal weights; open beyond & exact & \ref{sec:bell} \\
$S(\Nphi)$ exact, $181/64$ on the plateau; $2\sqrt2$ the limit & the rungs, the tables & the tables at $N_t = 256$ (P7) & exact (the rational); limit (the bound) & \ref{sec:bell}; 24.4 \\
The Doppler on the axis by the crossing rule & the crossing count, its boundary row & none & exact (the count per Link); limit (the ratio $1 \pm v/c$) & 2.2, 2.7 \\
A body's dispersion, its momentum's fraction; the moving clock's rate $1$ & the drive per axis, the owed count & none: the law's own predictions & exact & 4.3, 4.4 \\
Newton's cooling within one birth's cost & the release & none & exact (a bound) & 25.9 \\
The muon's decay tick under covariant-readings-v1 & the identity's owed count & the identity, a hypothesis beside the law & exact under the identity & 18.1 (a) \\
\end{longtable}}

""")

open(str(HERE / 'part1.tex'), 'w').write(''.join(out))
print('part1 ok', sum(len(x) for x in out))
