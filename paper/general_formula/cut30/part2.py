"""Part 2 of the thirty-page assembly; see assemble.py."""

from pathlib import Path

from cut30_lib import B, cutp, sub

HERE = Path(__file__).resolve().parent
out = []
# ---- Section 3: geometry and symmetries
g = B("\\paragraph{From the Node to the group", "\\paragraph{The state.}")
g = sub(
    g,
    "\\paragraph{From the Node to the group, the octahedron and the pace.}",
    "\\paragraph{The six Ports, the group and the front.}",
)
g = cutp(g, "(series P's parity", "The same six Ports bound")
g = g.replace("belongs to The same six Ports bound", "belongs to. The same six Ports bound")
g = g.replace(
    "(Proposition~\\ref{prop:pace}, Figure~\\ref{fig:octahedron})",
    "(Proposition~\\ref{prop:pace}, Figure~\\ref{fig:octahedron})",
)
g = cutp(g, "The group, the front and the bound are one figure:", "\n\n")
g = g.rstrip() + "\n\n"
out.append(
    "\\section{Geometry and symmetries: the directions and $c = 1/\\sqrt3$}\\label{sec:geometry}\n\n" + g
)
th = B("\\begin{theorem}[the $24$ of the name]", "\\begin{proof}")
out.append(th + "The proof is Appendix~\\ref{app:proofs}.\n\n")
sym = B("\\paragraph{The symmetries.}", "\\begin{theorem}[the $24$ of the name]")
sym = cutp(sym, "The two ties are read through the six faces' detectors", "A boost, which mixes")
sym = sub(
    sym,
    "the wave equation at $c$ (Section~\\ref{sec:lorentz}).",
    "the wave equation at $c$ (Section~\\ref{sec:discussion}).",
)
sym = sub(
    sym,
    "this paper meets the first, Section~\\ref{sec:model});",
    "this paper meets the first, Section~\\ref{sec:measurement});",
)
sym = sub(
    sym,
    "(the families' tables give, family by family, the group each declared quantity lives on \\cite{familiesaudit}).",
    "\\cite{familiesaudit}.",
)
sym = cutp(sym, "The $48$\nare the GameBoard's stand-in for the rotation group", "\n\n")
sym = sym.rstrip() + "\n\n"
out.append(sym)
pace = B("\\paragraph{The pace of the rows, and the octahedron.}", "\\begin{proposition}[The pace]")
out.append(pace)
prop = B("\\begin{proposition}[The pace]", "So $c = 1/\\sqrt3$ Links per interval is the largest")
out.append(prop)
after = B("So $c = 1/\\sqrt3$ Links per interval is the largest", "\\paragraph{No dispersion.}")
after = sub(
    after,
    "are not derived here (Section~\\ref{sec:lorentz}:\na one-way count of a stream reads $1 \\mp \\beta$, $\\beta$ (beta) the\ndetector's speed as a fraction of $c$).",
    "are not derived here (Section~\\ref{sec:discussion}).",
)
after = cutp(after, "Over the $1\\,780\\,418$ primitive", "The pace is $64/110 = 0.5818$ on a")
after = sub(
    after,
    "(a two-arm interferometer at rest with both\narms on headings sees nothing, the two paces being equal by the $48$; the\nrotating resonators of \\cite{nagel2015} would see the cubic pattern to the\nsame order; what the law says of a laboratory in motion is\nSection~\\ref{sec:lorentz}).",
    "(what the law says of a laboratory in motion is Section~\\ref{sec:discussion}).",
)
after = sub(
    after,
    "it\nclaims no novelty for the number\n(Section~\\ref{sec:lit}).",
    "it claims no novelty for the number.",
)
after = cutp(
    after,
    "The symmetry of the octahedron and of the flight\nis the group",
    "No body moves in the worlds of this chapter.",
)
after = sub(after, "No body moves in the worlds of this chapter.", "")
# the no-dispersion remark: the first half only, with the figure
rem = B("\\paragraph{No dispersion.}", "\\begin{figure}[H]\\centering")
rem = cutp(rem, "What is not trivial is the pair with Proposition", "\\end{remark}")
rem = rem.replace(
    "\\end{remark}",
    "That no local linear wave scheme on the GameBoard is both isotropic and free of dispersion is Meyer's theorem \\cite{meyer1996}, not this paper's.\n\\end{remark}",
    1,
)
fig = B(
    "\\begin{figure}[H]\\centering\n\\includegraphics[width=0.5\\textwidth]{figures/octahedron.pdf}",
    "\\end{figure}",
    include_end=True,
)
fig = fig.replace("width=0.5\\textwidth", "width=0.34\\textwidth")
after = (
    after.rstrip()
    + " Stated with its ground: the pace of a direction, $N_l|D|/T_D$, isotropic within $1/T_D$, and the Manhattan bound $S_1 N_l \\le T_D$ are exact in integers; the isotropic bound $1/\\sqrt3$ is a theorem about a pace that would be the same in every direction, while the board's Euclidean pace per direction is at or above $1/\\sqrt3$ on $282$ of the $290$ registered directions, $0.5818$ on every heading and $0.5774$ on the eight diagonals; the value $c = 1/\\sqrt3$ attained is a limit of the grain $N_l$.\n\n"
)
out.append(after + rem + fig + "\n")
out.append(r"""\paragraph{What a detector measures.} Two registered runs read the
pace after a detector. Series Q \cite{register}: a lamp releasing one
row on each of the $290$ primitive directions with $|a| + |b| + |c| \le
6$, with detectors on the six faces; $290$ of $290$ face clicks landed at
the derived interval, Node and face, and the pace read from the clicks
is $0.5718$ to $0.5893$ Links per interval (mean $0.5810$; the table's
asymptotic $0.5774$ to $0.5818$). Series L7, the cone: a row of $17$
Links on an axis and a row of $24$ Links on the plane diagonal, at the
same Euclidean distance to one percent, reached their counters at the
same age $29$. Nature's bound on the anisotropy of $c$, below $10^{-18}$
\cite{nagel2015}, is a bound on the grain, $N_l$ at or above $5.8
\times 10^{17}$ (Section~\ref{sec:checks}, row 5a).

""")

# ---- Section 4: conservation and the forces
out.append(r"""\section{Conservation, the flux and the forces}\label{sec:forces}

\paragraph{The books.} Every message released is on exactly one line of
the books at every interval, released equals in transit plus absorbed
plus escaped plus cancelled, per family, in amount and in content,
exact at every interval and at every operation (P3, P5): the carry is a
bijection $s \mapsto (e, s - ed)$ that loses nothing, and the split and
the rotation are integer matrices whose conjugate transposes invert them
(Theorem~\ref{th:isometry}). From the books the continuity equation of
the content follows exactly on the GameBoard (the derivation's 25.4
\cite{derivations}); it is the first row of the ledger. A paid message
carries its label out of its emitter at birth and into its reader at
its end, so for paid messages momentum is conserved and the third law
holds message by message; a free message, a field's row, takes no
recoil at birth and pushes its reader by its label times the reader's
content.

""")
ops = B(
    "\\paragraph{The operations.} Six operations, of three of Part~I's kinds",
    "\\paragraph{Gauss's law, exact.}",
)
ops = sub(
    ops,
    "Six operations, of three of Part~I's kinds",
    "Six operations, of three of Section~\\ref{sec:law}'s kinds",
)
out.append(ops)
gauss = B("\\paragraph{Gauss's law, exact.}", "\\paragraph{The inverse square as a shell mean.}")
out.append(gauss)
shell = B(
    "\\paragraph{The inverse square as a shell mean.}", "\\paragraph{Newton's law and the place of $G$.}"
)
out.append(shell)
newton = B(
    "\\paragraph{Newton's law and the place of $G$.}", "\\paragraph{Coulomb's law and the one constant.}"
)
newton = sub(newton, "(Table~\\ref{tab:consequences}).", "(Table~\\ref{tab:ledger}).")
out.append(newton)
coulomb = B("\\paragraph{Coulomb's law and the one constant.}", "\\section{The delay field")
out.append(coulomb)
out.append(r"""\paragraph{The ground of these derivations.} Gauss's law of the flux,
the equivalence principle and the third law at rest are exact on the
GameBoard. The inverse square, Newton's and Coulomb's, is a limit under
a spatial condition, an average that covers the shell, in one of three
admissible forms, each with its own error: over the shell's Nodes (the
shell mean, the ripple $O(r^{\theta - 1})$ with $\theta \le 131/208$, at
any declared fan); over the directions at one Node, the fan dense at
fixed $r$, and then only for a fan declared in a ball (a cube's fan
keeps a cubic anisotropy of $3^{3/2}$ in the limit); or over the path of
a body that sweeps the fan's lines, one closed turn of an orbit, whose
mean push per turn is the ring mean exactly, the only one of the three
readable after a detector. On one Node beside a source the field is a
comb of beams, and no single reading of the board is the inverse square;
the condition is part of the claim, and a detector run, when made,
establishes a lattice-exact claim about the world at hand whose
agreement with the continuum's form within the ripple is evidence for
the inverse square and not its proof. No detector reading of these laws
is registered; their measurement after a detector is a run not made
(Section~\ref{sec:discussion}).

""")

# ---- Section 5: the delay field
out.append(r"""\section{The delay field: the retarded potential, Poisson's equation and the clock}\label{sec:delay}

The rows of Table~\ref{tab:ledger} on the delay field are written out
here from the derivation's section 5 \cite{derivations}; the register's
series E reads probes on the GameBoard, diagnostics this paper does not
carry, and the field's one measurement after a detector is the clock's
form at two distances, series T (row 12 of Table~\ref{tab:nature}).

""")
wd = B("\\paragraph{What is delayed.}", "\\paragraph{The two fields of one stream.}")
wd = sub(
    wd,
    "(the clock's word by P9, the\nregistered clock worlds below reading it so)",
    "(the clock's word, P9)",
)
wd = sub(wd, "the clock's\npair of Part~I", "the clock's\npair of Section~\\ref{sec:law}")
out.append(wd)
tf = B("\\paragraph{The two fields of one stream.}", "\\paragraph{The clock's redshift.}")
tf = sub(
    tf,
    "(the limit of\nSection~\\ref{sec:newton}'s shell mean)",
    "(the limit of\nSection~\\ref{sec:forces}'s shell mean)",
)
out.append(tf)
rs = B("\\paragraph{The clock's redshift.}", "\\paragraph{Light: no optical metric.}")
rs = sub(
    rs,
    "Under the calibration $a_\\tau = GM/rc^2$, assumed (the clock's pair and the width do not fix it), the two agree at first order:",
    "Under the calibration $a_\\tau = GM/rc^2$, an input of the dictionary (by the derivation's 5.1 and 3.3 the clock's constant and Newton's $G$ have the exact ratio of the suspension pair times the width, so the calibration is a constraint on the inputs), the two agree at first order:",
)
rs = cutp(
    rs,
    "The clock alone, without the field's push, is read on the crowd-clock",
    "Which of the two words the clock counts",
)
rs = sub(
    rs,
    "the ratio of the two $a_\\tau$ being $1.907$\nfor the pinned $1.909$ (the continuum's potential $2.000$, outside the\npin as the lattice's dwelling ages say); every pin met; measured and\nreplicated (\\cite{replications}, the block of series T).",
    "the ratio of the two $a_\\tau$ being $1.907$ for the lines' pin $1.909$, nature's $2.00$ being $4.6$ percent away; every pin met; measured and replicated (\\cite{replications}, the block of series T). What the detector establishes is the form at two Nodes, a lattice-exact reading; the continuum's $1/r$ is its limit under the average that covers the shell, and the reading is evidence for it, not its proof.",
)
rs = sub(
    rs,
    "In the precedents' form of words: the law as declared reads either\nword per table entry; under the age word the clock's shift follows the\npotential's form, the physicist's map putting the GPS\nground-to-orbit shift at $45.7$ microseconds per day against Ashby's\n$45.7$ \\cite{ashby2003}, where the presence word gives $28.3$.",
    "Under the age word the clock's shift follows the potential's form, the physicist's map putting the GPS ground-to-orbit shift at $45.7$ microseconds per day against Ashby's $45.7$ \\cite{ashby2003}, where the presence word gives $28.3$.",
)
rs = cutp(rs, "the second runner's round is pending. What the runs cannot say is", "\n\n")
rs = sub(
    rs,
    "the presence word stays in the record as the alternative refuted on\nthe form; ",
    "the presence word stays in the record as the alternative refuted on\nthe form. The clock alone, without the field's push, is read on the crowd-clock pages of the tree (a lamp inside a crowd, a cluster of crowds, a reader inside a crowd; their register entries drafted \\cite{crowdclock,clusterclock,readerclock}), every reading inside its pin, measured once.",
)
out.append(rs.rstrip() + "\n\n")
light = B("\\paragraph{Light: no optical metric.}", "\\section{The click's square")
light = sub(
    light,
    "the derivation's 24.3, row 14, REFUTED\non main).",
    "the derivation's 24.3, row 14, REFUTED\non main; Table~\\ref{tab:nature}).",
)
out.append(light)
open(str(HERE / "part2.tex"), "w").write("".join(out))
print("part2 ok", sum(len(x) for x in out))
