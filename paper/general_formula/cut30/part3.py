"""Part 3 of the thirty-page assembly; see assemble.py."""

from pathlib import Path

from cut30_lib import B, cutp, sub

HERE = Path(__file__).resolve().parent
out = []
# ---- Section 6: measurement and the quadratic form
out.append(r"""\section{Measurement and the quadratic form}\label{sec:measurement}

The worlds of this section have no body: the law of Section~\ref{sec:law}
on rows alone, and the measurement is the one threshold that is read
out. Every interval applies three of the six operations to the state,
the translation (the flight, the phase, every count and the birth), the
multiplication by a declared integer matrix (the split and the
rotation) and the sum in the group ring (the merge, where opposite
phases cancel); between clicks the rates are constant, so the map has a
closed form and every count of Section~\ref{sec:checks} was computed
from it before its run. The click is the one place with a fourth
operation: the apparatus sums a record's rows through the tables and
squares the sum, the norm, and only then applies its threshold to the
birth phase $u$.

""")
dr = B("\\begin{definition}[Row and record]", "The host, not any Node, keeps per live record")
out.append(dr)
host = B(
    "The host, not any Node, keeps per live record",
    "\\begin{definition}[The update rules of one interval]",
)
host = sub(
    host,
    "in the record's ledger \\cite{log}.",
    "in the record's ledger \\cite{log}; the GameBoard never reads it, and it is no measurement.",
)
out.append(host)
rules = B("\\begin{definition}[The update rules of one interval]", "\\begin{definition}[The click]")
out.append(rules)
click = B("\\begin{definition}[The click]", "\\begin{lemma}[One click per record]")
click = sub(
    click,
    "(the which-path read of the polariser, Table~\\ref{tab:consequences})",
    "(the which-path read of the polariser)",
)
out.append(click)
lem = B("\\begin{lemma}[One click per record]", "Three things are put in here and not derived")
out.append(lem)
three = B("Three things are put in here and not derived", "\\section{Four theorems}")
three = sub(
    three,
    "(the record's total over $u$ takes eight values,\nSection~\\ref{sec:measure})",
    "(the record's total over $u$ takes eight values, Appendix~\\ref{app:technical})",
)
three = sub(
    three,
    "a declared input of\nthe law (Part~I, ``What is put in'').",
    "a declared input of the law (Section~\\ref{sec:law}, P7).",
)
three = cutp(three, "At the tree of the runs reported here the law was selected by a world", "\n\n")
three = cutp(three, "a chooser\nwhose period shares a factor with", "The earlier engine's run")
three = sub(
    three,
    "every marginal $32/64$); The earlier engine's run \\cite{paper1}\nis history.",
    "every marginal $32/64$).",
)
three = cutp(three, "$u$ is also the phase every row of", "The\ntables at $1/256$ are the third")
out.append(three.rstrip() + "\n\n")
out.append(r"""\paragraph{The two theorems of the interval.} Two theorems of the
linear block are stated here and proved in Appendix~\ref{app:proofs}.

""")
iso = B("\\begin{theorem}[The split is an isometry", "\\begin{proof}")
out.append(iso)
bij = B("\\begin{theorem}[The interval is injective between clicks]", "\\begin{proof}")
out.append(bij)
norm = B(
    "So a record's norm is conserved exactly by $S$ and by the flight",
    "\\begin{theorem}[Exact marginals; no-signalling]",
)
norm = sub(
    norm,
    "$65536$); the integer\nMach-Zehnder's total over the 64 birth phases takes eight values from\n$65448/65536$ to $65773/65536$, the same eight on every one of its ten\nworlds \\cite{register}.",
    "$65536$; Appendix~\\ref{app:technical}).",
)
out.append(norm)
# the lattice Gleason
gl = B("\\section{The click's square as a positive quadratic form", "\\paragraph{The objects.}")
gl = sub(
    gl,
    "\\section{The click's square as a positive quadratic form forced by the splitter: a lattice Gleason}\\label{sec:gleason}",
    "\\paragraph{The click's square as a positive quadratic form: a lattice Gleason.}",
)
gl = sub(
    gl,
    "The row of Table~\\ref{tab:consequences} on the click's weight is written\nout here from the derivation's section 6.5 \\cite{derivations}; the\nregister's checks are the click chapter's own (series L, Part~III). The\nclick's square,",
    "The row of Table~\\ref{tab:ledger} on the click's weight is written out here from the derivation's section 6.5 \\cite{derivations}; the register's checks are series L's clicks (Section~\\ref{sec:checks}). The click's square,",
)
gl = cutp(gl, "(The derivation's ``Theorem\n2'' of the click paper", "\n\n")
out.append(gl.rstrip() + "\n\n")
obj = B("\\paragraph{The objects.}", "\\paragraph{The hypotheses.}")
out.append(obj)
hyp = B("\\paragraph{The hypotheses.}", "\\begin{theorem}[The lattice Gleason]")
hyp = sub(
    hyp,
    "(the totals $64/0$ and $32/32$ of Part~III)",
    "(the totals $64/0$ and $32/32$ of Section~\\ref{sec:checks})",
)
out.append(hyp)
thm = B(
    "\\begin{theorem}[The lattice Gleason]",
    "\\paragraph{The uncertainty relation, from the same evaluation.}",
)
thm = sub(
    thm,
    "$C'$ and $S'$ the half-angle\ntables of Part~III.",
    "$C'$ and $S'$ the half-angle\ntables of Definition~\\ref{def:rules}.",
)
out.append(thm)
reached = B(
    "\\paragraph{What is reached and what is not.}", "\\paragraph{Against the registered integers.}"
)
reached = cutp(reached, "(Gleason's theorem \\cite{gleason1957} needs", "The multiplicity rule")
reached = sub(
    reached,
    "continuity and no dimension The multiplicity rule",
    "continuity and no dimension (Gleason's theorem \\cite{gleason1957} needs dimension three; the lattice version does not, because (b) holds for every two inputs, the parallelogram law, a stronger hypothesis the balanced splitter grants). The multiplicity rule",
)
out.append(reached)
against = B("\\paragraph{Against the registered integers.}", "\\paragraph{The limit.}")
against = sub(
    against, "split's $63/1$ (Part~III) holds", "split's $63/1$ (Section~\\ref{sec:checks}) holds"
)
against = cutp(
    against, "The harmonics: every registered Mach-Zehnder world", "The\ntables: the built click"
)
against = sub(
    against,
    "(Part~III), the tables' violation of hypothesis (a), a part in $276$.",
    "(Appendix~\\ref{app:technical}), the tables' violation of hypothesis (a), a part in $276$. The two-slit clicks under the birth wheel (series L2b) correlate $0.891$ with the two-source cosine, the kernel of the fundamental $j = 1$; a harmonic $j$ would give a fringe of period $23.5/j$ pixels where $23.5$ is read, and Malus at $22.5$ degrees ($219/256$ and $187/256$ exact) admits $j = \\pm 1 \\bmod 8$ and excludes every mixture: the register pins the fundamental, and the least-rank click (P10) stores it.",
)
against = cutp(
    against,
    "The\ntables: the built click is this form to the tables' rounding",
    "The two-slit clicks under the birth wheel",
)
out.append(against)
lim = B("\\paragraph{The limit.}", "\\section{The confrontation with nature}")
lim = sub(
    lim,
    "Tsirelson's value as a limit is Part~III's\nTheorem~\\ref{th:bell}.",
    "Tsirelson's value as a limit is Theorem~\\ref{th:bell}.",
)
lim = cutp(lim, "In the precedents' form of words: Sinha et al.'s", "\n\n")
lim = (
    lim.rstrip()
    + " Sinha et al.'s three-slit test read the third-order term $\\kappa = 0.0064 \\pm 0.0119$ \\cite{sinha2010}; the click's form, a quadratic, gives $\\kappa = 0$ exactly, and its power's window contains $2$ (Table~\\ref{tab:nature}, row 2c).\n\n"
)
out.append(lim)
out.append(r"""\paragraph{Planck and de Broglie, as identities.} Under the declared
dictionary the release's cost rule reads as $E = h_q s = (h_q\Nphi) f$
and the turn rule as $\lambda = h_A/p$: Planck's and de Broglie's
relations are identities of the update rules (the derivation's 21.2,
rows 51 and 52), with one constant, $h = h_q\Nphi = h_A$, a constraint
on the inputs whose value is an input (24.1, row 25). No detector
reading of them is registered; the electron's click on a face reads
where an orbit ended, not $E = hf$.

""")
unc = B(
    "\\paragraph{The uncertainty relation, from the same evaluation.}",
    "\\paragraph{What is reached and what is not.}",
)
unc = sub(
    unc,
    "of the same form as the identity of Section~\\ref{sec:table}'s entropy\nrow, bits read plus bits not read of $u$",
    "of the same form as the entropy identity of the ledger, bits read plus bits not read of $u$",
)
out.append(unc)

# ---- Section 7: Bell and CHSH
out.append(r"""\section{Bell and CHSH: from weights to counts}\label{sec:bell}

For a record with arms at two rotated sets $A$ and $B$ the cells are the
joint outcomes, the weights are Eq.~\eqref{eq:joint}, the rungs
Eq.~\eqref{eq:rung}, and the record is gathered once when the rows at
both arms have ended. The correlation at the settings $(a, b)$ is $E =
(c_{++} + c_{--} - c_{+-} - c_{-+})/\Nphi$ over $\Nphi$ births, one per $u$, and
the CHSH sum is $S = E(a, b) - E(a, b') + E(a', b) + E(a', b')$ at the
labels $(0, \Nphi/8, \Nphi/4, 3\Nphi/8)$. Two theorems follow from the
definitions, exact on the GameBoard.

""")
marg = B("\\begin{theorem}[Exact marginals; no-signalling]", "The strict-crossing rung")
out.append(marg)
after_marg = B("The strict-crossing rung", "\\begin{theorem}[The finite-$\\Nphi$ Bell value]")
out.append(after_marg)
bell = B("\\begin{theorem}[The finite-$\\Nphi$ Bell value]", "What Theorem~\\ref{th:bell} does not say:")
out.append(bell)
after_bell = B("What Theorem~\\ref{th:bell} does not say:", "\\section{The measurements}")
after_bell = sub(
    after_bell,
    "Against \\cite{poh2015} the plateau stands\n$1.05$ standard errors above, $16384$ and $32768$ stand $2.0$\nabove, $65536$ and beyond $1.5$ to $1.65$ above.",
    "",
)
out.append(after_bell)
out.append(r"""\paragraph{The one prediction.} The law's number is
\begin{equation}\label{eq:prediction}
S_{\mathrm{U24}} = \frac{181}{64} = 2.828125 \ \text{exactly}, \qquad
\Delta S = S_{\mathrm{U24}} - 2\sqrt2 = -3.02 \times 10^{-4},
\end{equation}
at every power of two from $512$ through $8192$, with the tables at
$N_t = 256$, the wheel at $N_u = \Nphi$, the settings $(0, \Nphi/8, \Nphi/4,
3\Nphi/8)$ and a pair of two labels with equal weights; the marginals
exactly $1/2$; the correlations at the two pairs of settings
$725/1024$ and $723/1024$ at $\Nphi = 4096$, above and below $1/\sqrt2$;
$5793/2048$ at $16384$ and $32768$. It was computed in advance, run at
$\Nphi = 512$ and $4096$ under the click and the wheel with every pin met
(the register's block of the derivation's 24.4), and re-run by the
second runner \cite{replications}. The criterion: the law at a grain
is rejected when a measured $S$ differs from $S(\Nphi)$ by more than
five standard errors, under the identification of the experiment's
settings and detection with the labels and the ideal read-out, which
the model does not model; the comparison with nature is
Section~\ref{sec:checks}.

""")
open(str(HERE / "part3.tex"), "w").write("".join(out))
print("part3 ok", sum(len(x) for x in out))
