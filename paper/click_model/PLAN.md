# Paper 3, the click model: the plan

Written 2026-09-20 by the paper coordinator (a separate session, by the
model owner's decision recorded in
[Highlights 5.4](../../docs/HIGHLIGHTS.md#54-the-detector), "DECIDED: the
paper is coordinated by a separate agent"). Base: `072fd8bd` on the branch
`claude/universe24-new-3ytqde`, the commit that added the `amplitude-v1`
design and its check outputs to `docs/designs/amplitude-v1/`. Nothing of
`amplitude-v1` is on `main` at this writing: the implementation, its
acceptance tests and its Bell runs land later, and the draft (`main.tex`,
section 11) is written only after they are in the
[experiments register](../../docs/EXPERIMENTS.md). This plan cites
three kinds of numbers and names each: the register (papers 1 and 2, A2, A2
with the choosers, A10 at a low rate); the design's check outputs
(`docs/designs/amplitude-v1/*.txt`, the design's own evidence, not runs);
and this plan's one computation (`checks/s_of_n.py`, its output
`checks/s_of_n.txt`), which reproduces the design's Bell numbers from the
design's formulas with the repository's own tables (`core/phase.py`) and
extends them to every N. A computation from a formula is not a run of the
engine and is labelled so wherever it is used.

## 1. The one claim

### 1.1 The claim as recommended

The orchestrator's recommendation, recorded in Highlights 5.4 for the owner
to confirm: a local integer lattice with a one-way click reading a record's
sum gives Born, interference, Bell with exact marginals and GHZ, with
S = 2 sqrt 2 - epsilon(N), epsilon <= 4/N, so the best measured
S = 2.8276 +- 0.0008 bounds nature's N >= about 4000 and excludes N = 64;
the weak force and the other series stay out of the claim.

### 1.2 What the evidence supports, checked line by line

The mechanism half of the claim stands on the design's checks and is what
the paper's tables will measure once the runs exist. The Bell-value half
does not survive the check, on four points.

**(a) The experiment.** The number 2.8276 +- 0.0008 is not in the
register. The register's million-pair value is 2.8269 +- 0.0010
(paper 1, Table 3; VALIDATION: mean 2.8269, predicted error 0.0007,
spread 0.0021), and it is a measurement of paper 1's configured registry
(expectation 724/256 on the table), not of nature; it can bound nothing
about nature's N. The number the recommendation had in mind is the
photon-pair experiment of Poh, Joshi, Cere, Cabello and Kurtsiefer,
Phys. Rev. Lett. 115, 180408 (2015): S = 2.82759 +- 0.00051, with
2 sqrt 2 - S = 0.00084 +- 0.00051 (the 0.0008 is the distance to
Tsirelson, not the error). That experiment assumes fair sampling and
is not loophole-free; the loophole-free experiments give S = 2.42 +- 0.20
(Hensen et al., Nature 526, 682 (2015); 2.38 +- 0.14 over both runs,
Sci. Rep. 6, 30289 (2016)), which constrain N not at all. The paper cites
Poh et al. for the value and says what it assumes.

**(b) S(N) is not below Tsirelson at every N.** The design checked
N = 64, 256, 1024 (S = 176/64, 720/256, 2896/1024) and wrote "at or below
Tsirelson at every N". `checks/s_of_n.py` reproduces those three values
and the cells (27, 5, 5, 27) and the exact marginals at N = 64 integer by
integer, then computes S(N) at the CHSH labels (0, N/8, N/4, 3N/8) for
every N with 8 | N up to 2048 (the pair's rotation uses the half-angle
tables at 2N, and `phase_cosines` is bounded at 4096 steps, so N = 4096
is not reachable by the design as written; the "Bell at N = 4096" of the
schedule needs that bound raised or is N = 2048). The result: 126 of the
256 values of N give S(N) above 2 sqrt 2 (N = 16 and 32 give 3, N = 128
gives 23/8 = 2.875, N = 96, 192, 384 and 768 give 17/6 = 2.8333); the
powers of two from 512 give exactly 181/64 = 2.828125, the tables'
cosine of the eighth turn; between them S(N) scatters on both sides
(2.82443 to 2.83212 for N >= 1024). The deficit bound epsilon <= 4/N is
false: N x |S(N) - 2 sqrt 2| reaches 7.76 (at N = 48). What holds, and is
the theorem to prove (section 4, T4): the four E's are nearest-integer
counts, so each is within 2/N of the tables' cosine plus the tables'
own rounding, and |S(N) - 2 sqrt 2| <= 8/N + c_T, two-sided, with c_T the
tables' 1/256 term that does not shrink with N (measured: max |E - cos|
over all setting pairs is 2.27/N at N = 64 and 0.0115 = 5.9/N at
N = 512, where the tables' term dominates). "S = 2 sqrt 2 - epsilon(N)
from below" is true of the three N the design checked and false in
general; the physics is more interesting than the recommendation: at
finite N the click's rounding puts the model's Bell value above
Tsirelson's bound with the marginals still exactly 1/2, a no-signalling
box beyond quantum mechanics at those N, and a Bell measurement of nature
tests it.

**(c) The bound on N.** Since S(N) is not monotone, a measurement selects
a set of N, not a half-line. Against Poh et al.: N = 64 is excluded at
152 standard deviations and N = 256 at 30; the smallest N within three
standard deviations is 184; 94 of the 256 values up to 2048 are within
three, 116 are excluded at five, the largest excluded being 2032; the
powers of two from 512 sit one standard deviation above the measurement.
"N >= about 4000" does not follow from anything; "N = 64 is excluded" does
follow, given the experiment and given that nature's pairs are this
model's pairs at some N. The paper states the set.

**(d) The tables' ceiling.** With the 1/256 tables the eighth turn is
181/256 at every N (`tables.txt`), so at the CHSH labels the model never
exceeds 181/64 = 2.828125 at a power of two; 2 sqrt 2 - 181/64 = 0.0003,
below the best experiment's resolution. The table's scale is untested by
any Bell measurement and the paper says so.

### 1.3 The claim proposed for the owner's confirmation

One sentence, as the evidence supports it:

> On a local integer GameBoard whose only one-way step is a click that reads
> the accumulated sum of one record's rows and chooses by the record's birth
> phase u on nearest-integer rungs, the world's list of clicks reads Born
> (the click histogram over u equals the record's weights), single-quantum
> interference (the integer Mach-Zehnder, 64/0, 0/64, 32/32), Bell pairs
> with marginals exactly 1/2 at every setting and every N (no-signalling
> exact, proved), GHZ's exact zeros, and a CHSH value S(N) that is an exact
> rational function of the circle's N, two-sided within 8/N plus the
> tables' term of 2 sqrt 2 and above Tsirelson's bound for about half the
> N; a Bell measurement of nature therefore selects the admissible N, and
> the photon-pair value 2.82759 +- 0.00051 excludes N = 64 and N = 256 and
> admits N = 512, 1024 and 2048 among others. The click is a non-local
> step, owned by the apparatus and forced by Bell's theorem; the lattice is
> local and a bijection between clicks.

Outside the claim, by the owner's decision: the weak force's registered
disagreements (series J), the redshift (paper 2), the meeting (series K),
the nucleus, Bohr, the Hubble diagram. Not claimed: a derivation of
quantum mechanics; a continuum limit; spin, polarization, bosons, fermions;
Lorentz; the norm's exact conservation on the lattice (section 10).

The two alternatives the owner may prefer instead (ranked with the rest in
1.4): (A) the mechanism alone,
without the comparison with nature's S (Born, interference, exact
marginals, GHZ, the finite-N bound as a theorem), a shorter and safer
paper that predicts nothing; (B) the recommendation as recorded, which
this plan cannot support on points (b) and (c) and would not write.

### 1.4 The candidate claims ranked by safety and by ease (the owner's request of 2026-09-20, relayed by the Boss session)

Safety: what is proved or measured today and defensible against a hostile
referee. Ease: what already exists in the register and in the two
submitted papers, the least new work. Ranked 1 (best) to 4.

| Claim | Proved or measured today | New work | The referee's attack | Safety | Ease |
| --- | --- | --- | --- | --- | --- |
| C4 "Bell's assumption is a measurement in the model": a local integer engine with the settings chosen by GameBoard events gives S = 2 exactly, every E on the triangle, the marginals 1/2, no superdeterministic correlation (A2, A2 with the choosers, control 3 seeing a built-in one), with the law's registered limits beside it (no single-click build-up under the amount reading, light not bent without the meeting) | everything: registered runs with fingerprints, exact integers, the causal anatomy of paper 1 | none on the engine; the writing, the figures from existing runs | "a negative result about a model no one else uses; paper 1 already has S = 2 for the local candidates"; answer: the choosers on the GameBoard and the measured superdeterminism control are new, and the limits are stated so they can fail | 1 | 1 |
| C3 (alternative A of 1.3) the click model's mechanism alone: Born from the uniform u, the integer Mach-Zehnder, exact marginals and no-signalling (T3), GHZ's exact zeros, T1, T2, and T4's two-sided bound with S(N) tabulated, no comparison with nature's S | the theorems are provable now (T3's tie case and T4's constant to finish); the integers are the design's checks, becoming measured when `amplitude-v1`'s runs are registered | the runs of the acceptance table (in flight), the proofs, the draft | "a non-local click is Bohm with extra steps; the tables' unitarity is only approximate; nothing is predicted"; answer: the non-locality is stated as forced by Bell, the residual is measured, and the prediction is left to C2 | 2 | 3 |
| C2 (the claim of 1.3) C3 plus the finite-N Bell value as a prediction: S(N) above Tsirelson for about half the N, and the set of admissible N from Poh et al. | as C3, plus `checks/s_of_n.txt` (a computation, exact) | as C3, plus the run points at N = 64, 1024, 2048, the exact c_T, the comparison written with its assumptions | "why would nature's pairs be this model's pairs at any N; a no-signalling box beyond quantum mechanics is refuted in advance by every precision Bell test unless N is a power of two, which is a tuning"; answer: the claim is falsifiable and the excluded N are stated, but the referee's point stands as a risk | 3 | 4 |
| C1 the recommendation as recorded (S below Tsirelson at every N, epsilon <= 4/N, N >= about 4000) | contradicted by the computation (1.2 (b), (c)) | none that could rescue it | "false on the model's own numbers" | 4 | not applicable |

The judgement, stated plainly. The safest claim and the easiest claim are
the same, C4: it needs no run that does not exist, every number in it is
registered, and no sentence in it can be shown false; its weakness is
that it is small, a measurement of an assumption and a list of limits,
and a referee may call it a note. Among the claims that need
`amplitude-v1`, the safest is C3 and the one with the physics is C2; the
distance between them is one section (the comparison with Poh et al.) and
one risk (the referee's attack on C2, which cannot be argued away, only
stated). This plan recommends C2 written so that C3 survives if the
comparison is struck out by a referee, and C4 folded into it as the
"before" (the result of the amount reading that the click's reading
replaces); if the owner wants the paper out before `amplitude-v1`'s runs
exist, C4 is the paper that can be written today. The structure that
makes any of these safe is section 12: one claim as the result, everything
else a hypothesis with its status.

## 2. A new paper 3, not a revision of paper 1

Recommended: a new paper. Reasons. Paper 1 is submitted and its claim is a
testbed: the Bell value there lives in a declared shared registry, and its
"What is not claimed" says in so many words "not a derivation of the Born
rule" and "not a local explanation of the Bell value". Paper 3 removes the
registry, reads one record's sum at the click, and derives Born from the
uniform birth phase; its candidate set, its worlds, its theorems and its
comparison with nature are new, and its relation to paper 1 is that of a
result to the framework that measured its absence (paper 1's S = 2 for the
local candidates, A2, and #363's S = 2 with the choosers on the GameBoard
are paper 3's "before"). A revision would reverse paper 1's disclaimers
inside a paper whose tables it does not change, and an arXiv v2 would bury
the new result under the old title. Paper 3 cites paper 1 for the causal
anatomy (parameter dependence at fixed hidden variable, which applies to
the click unchanged) and for the framework, and paper 2 not at all.

## 3. The formal definition (the two pages of the paper)

From [BEAM_LAW](../../docs/BEAM_LAW.md) sections 2, 3 and 5 with notes 24,
33 and 34, and the [design](../../docs/designs/amplitude-v1/DESIGN.md)
sections 1 to 5. The paper states these as definitions; the engine's names
appear once each in a footnote.

**3.1 The GameBoard and the circle.** Nodes are the points of a box in
Z^3 (an axis may be periodic); each Node has six Links. Time is the
interval t in Z. The circle is Z_N, N even, 4 | N. The tables: for
p in Z_N, C_N[p] = round(256 cos(2 pi p / N)) (the rounding of
`phase_cosines`: no entry is a half-integer), S_N[p] = C_N[p - N/4]; the
identities C_N[p + N/2] = -C_N[p] and S_N[p + N/4] = C_N[p] are exact; the
norm C_N^2 + S_N^2 is 65536 +- 315 for every N (`tables.txt`). The
half-angle tables C'_N = C_{2N}, S'_N = S_{2N}. Directions D: the six
headings and the declared primitive integer vectors; the flight table
gives, per direction d and age tau, the Node offset pos_d(tau) on the
digital line of d with at most one Link per interval and Euclidean speed
1/sqrt 3 for every direction (BEAM_LAW section 3).

**3.2 The state space.** A row is
(node, d, tau, p, number, content, r, l, w, m): its Node, direction, age,
phase p in Z_N, emitter, content per unit, record r, branch label l, amount
w >= 1 and multiplicity m >= 1. Its amplitude is
z = (w / sqrt m) (C_N[p] + i S_N[p]) / 256, so |z|^2 = w^2 / m up to the
tables' norm. Two rows equal in every identity field are one row with the
amounts added; two rows of one record and label equal in every field but a
phase difference of N/2 are one row with the amounts subtracted (an equal
pair is no row). The state of record r is a vector psi_r in the free
Z-module M_r on the basis (node, d, tau, p mod N/2, number, content, l, m)
with |p + N/2> = -|p>, modulo the scaling (w, m) ~ (k w, k^2 m); the
GameBoard's state is the multiset of rows, one normal form per element of
the direct sum over r of M_r. The norm is <psi, psi> = sum over rows of
w^2 / m. Host state, not on any Node (the apparatus's layer): per live
record the birth phase u in Z_N, the count of live rows, the accumulated
pointer (X, Y) per (set, label), and the gathered flag.

**3.3 The update rules, one interval, in this order (each a formula on the
row's own fields).**

- Flight F: (node, d, tau, p) -> (node + pos_d(tau + 1) - pos_d(tau), d,
  tau + 1, p + phi_family), phi_family the family's phase per Link, applied
  when the step is a Link, the phase turned only then. Injective: the age is
  whole.
- Collision and meeting C: a permutation of the directions of the rows at a
  Node by the eight-slot table (and, under `meeting`, the arc permutation),
  record, label and m unchanged. A bijection.
- Split S at a measured event with `split` {(d_i, a_i, t_i)}: the row
  (w, m, p) is absorbed and re-emitted as the rows (w a_i, m A, p + t_i) on
  d_i, A = sum a_i^2, age 0. Norm sum (w a_i)^2 / (m A) = w^2 / m, exact
  for any integers. An equal k-way split is a_i = 1; the balanced splitter
  is (1, 1) with A = 2; a Pythagorean pair (a, b) has A = c^2; the
  reflection's quarter turn is t = N/4.
- Rotation R at a set with `rotate` {s, t} on a label pair (0, 1):
  U_s = [[C'[s], S'[s]], [-S'[s], C'[s]]], the rows (w, m, p) of label 0
  becoming (w C'[s], 65536 m, p) on 0 and (w S'[s], 65536 m, p + t) on 1,
  and of label 1 (w S'[s], 65536 m, p + N/2) on 0 and (w C'[s], 65536 m,
  p + t) on 1. U_s^T U_s = (C'[s]^2 + S'[s]^2) I exactly.
- Normal form M: merge and cancel as in 3.2. The identity on M_r.
- Birth B: a lamp's self-creation at interval t releases record r with
  u = t mod N (the lamp's clock; the lamp's declared turn), rows of amount
  1 on its k directions with m = k, and, for a pair, the declared branches
  (the labels with integer weights) on `arms` directions. The birth is the
  one operation that adds combinations.

**3.4 The click rule.** At a set with `reading: "sum"`, the rows of record
r and label l that arrive are absorbed (the GameBoard's click line) and the
layer accumulates their pointer,
X += sum 32 w C_N[p + f(tau, t)], Y += sum 32 w S_N[p + f(tau, t)], with
f = floor(t n / d) - floor((t - tau) n / d) the family's frequency [n, d]
(the age phase read whole by the external thing). The offer of (set, l) is
W = (X^2 + Y^2) / m, all rows at a set sharing m (refused otherwise). When
the record's live count reaches 0 (every row clicked, escaped through a
face or the border), Total = sum of the offers, the cumulative sums
C_1 <= ... <= C_K = Total in the declared order of the sets and labels, the
rungs b_k = floor((2 N C_k + Total) / (2 Total)) (b_0 = 0, b_K = N), and the
click is the k with b_{k-1} <= u < b_k: the world's row
(t, node or set, detector, family, r, u, channel, W, Total, combinations
before, after). For a record with arms at two sets (a pair) the first set
in the order takes the coarse rung over its outcomes, the second the fine
rung within the first's cell with the same u; the rows of the record not
chosen are deleted lazily (absorbed at their next set, offering nothing).
The click removes combinations and adds one row to the world's list; no
other operation does either.

**3.5 The world's list.** The world is the sequence of clicks. Over births
with u uniform on Z_N (the lamp's clock over N consecutive intervals), the
count of clicks in channel k is b_k - b_{k-1}, the nearest integer to
N W_k / Total: Born with the resolution 1/N.

**3.6 What is lattice and what is host.** The rules F, C, S, R, M, B act
on rows at one Node with Link-delivered inputs and fixed local work per
row. The layer's table and the rung are the apparatus's (principle 5): the
completion is known through the apparatus's Ports, the deletion of the
other arm's rows is the non-local step, and the lattice never reads the
layer. The paper says this in one paragraph and does not soften it.

## 4. The four theorems, as they should be stated

**T1 (the interval is a bijection between clicks).** For an interval
without a click, the composition M o R o S o C o F is an injective
Z-linear map on the direct sum of the M_r; F and C are permutations of the
basis, S and R are isometries (T2), M is the identity on the module. Hence
the GameBoard's state between two clicks determines the state at the birth
(the engine's `inverse_step` is the witness on worlds without a measured
event, BEAM_LAW note 6; with splitters the proof is the mathematical one).
Needs: the age whole (note 25) so that F is injective; the collision a
permutation inside its invariant classes (note 18).

**T2 (the split is an isometry with the transposed inverse).** The map
(w, m) -> ((w a_i)_i, m A) preserves sum w^2 / m; applied to two inputs at
one splitter, the transposed table on the output rows followed by the
normal form returns each input up to the scaling (k w, k^2 m) with k = A
(checked in `mz.txt`: (20, 21) returns (841, 2 x 841^2, 5) for the input
(1, 2, 5), the amplitude 1/sqrt 2 both; the same for (3, 4, 5) and
(119, 120, 169) and for unequal inputs). R likewise: U_s^T U_s is a scalar
on the integers. Corollary: a record's norm is conserved by S and R exactly
and by the tables only within +- 315/65536 per row (`tables.txt`; the
Mach-Zehnder's total 1.000000, 1.001808, 0.999893 over the arm phase,
`mz.txt`), which is why the ladder normalises by Total at completion and
not by the birth norm (design 2.5): the theorem states the exact part and
the measured residual.

**T3 (the marginals are exactly 1/2; no-signalling).** For the pair with
labels [[0, 1], [1, 1]] and settings a, b, the joint weights
W(o_A, o_B) = J^2 with J = sum over l of U_a[o_A][l] U_b[o_B][l]. Since the
rows of U_b are orthogonal on the integers, sum over o_B of J^2 = n_a n_b
for each o_A, so the coarse cumulative is exactly Total / 2 and the rung
is N/2 for every (a, b): A's marginal is N/2 exactly. B's marginal is N/2
by the mirror symmetry W(o_A, o_B) = W(-o_A, -o_B) and the identity
floor(N/2 - x + 1/2) = N/2 - floor(x + 1/2) away from a tie; the proof
must treat the tie (2 N C_1 + Total divisible by 2 Total) or show it
cannot occur; the computation shows the marginals exact for every setting
pair at N = 8, 16, 24, 32, 48, 64, 96, 128, 192, 256 and 512
(`checks/s_of_n.txt`). Hence P(o_B | a, b) = P(o_B | b) = 1/2 exactly in the
counts: no-signalling at every N, in the sense Ghirardi, Rimini and Weber
proved for quantum mechanics (Lett. Nuovo Cimento 27, 293 (1980)). The
strict-crossing rungs break it by 1/N (33/64 in 3944 of 4096 pairs,
design 3.3), which the paper reports as the reason for the nearest rungs.

**T4 (the finite-N Bell value), replacing "S <= 2 sqrt 2 at every N with
|E - cos| <= 1/N".** With the cells at the nearest rungs and A's rung at
N/2, the count of (+, +) is c = round(N W(+, +) / Total) and
E = 4 c / N - 1, so |E_N(a, b) - 4 W(+, +) / Total + 1| <= 2/N, and
4 W(+, +) / Total - 1 differs from cos(2 pi (a - b) / N) by the tables'
rounding term c_T, to be bounded exactly from the +- 1/2 rounding of C'
and S' (measured over all setting pairs: |E - cos| at most 2.27/N at
N = 64, 5.9/N = 0.0115 at N = 512, the tables' term about 0.012 and not
shrinking with N). Hence |S(N) - 2 sqrt 2| <= 8/N + 4 c_T at the CHSH
labels, two-sided; S(N) is an exact rational of N, tabulated
(`checks/s_of_n.txt`), above 2 sqrt 2 for 126 of the 256 admissible N up
to 2048 and equal to 181/64 at every power of two from 512. The paper
proves the bound, prints the table, and states the comparison with
Poh et al. as the set of admissible N (section 1.2 (c)). The claim
"at or below Tsirelson at every N" is withdrawn as false; the claim
"|E - cos| <= 1/N" is withdrawn as contradicted by the design's own
`bell.txt` (0.03516 at N = 64).

## 5. The literature and the positioning (references verified 2026-09-20)

The sentence the paper says plainly: the click is a non-local step, forced
by Bell's theorem because the marginals are exact and S > 2 (Bell 1964;
CHSH 1969); it is parameter-dependent at fixed u in the sense of paper 1's
causal anatomy (Jarrett 1984, Shimony 1986); no-signalling is proved (T3),
as it holds in quantum mechanics (GRW 1980). Positioning, one paragraph
each:

- 't Hooft, The Cellular Automaton Interpretation of Quantum Mechanics
  (Springer, 2016): deterministic ontological states with quantum
  mechanics as a description; the Bell value there is met by
  superdeterminism. Here the model is deterministic given u, the settings
  are GameBoard events measured not to correlate with the pair (#363, A2
  with the choosers), and the Bell value is met by an explicit non-local
  click, not by a correlation of the settings.
- Wolfram, Complex Systems 29(2), 107-536 (2020), and Gorard, Complex
  Systems 29(2), 537-598 (2020): hypergraph rewriting with a multiway
  system whose branches are the superposition and whose completion is the
  collapse. Here one lattice, one record with rows, one click with an
  exact integer rule, and finite tables whose consequences are computed.
- Lattice gases, Hardy, Pomeau and de Pazzis, Phys. Rev. A 13, 1949 (1976),
  and Frisch, Hasslacher and Pomeau, Phys. Rev. Lett. 56, 1505 (1986):
  exact integer dynamics with the continuum law in the limit. The
  GameBoard is of that kind; what is added is the click's reading of one
  record.
- Quantum cellular automata and quantum lattice gases, Bialynicki-Birula,
  Phys. Rev. D 49, 6920 (1994); Meyer, J. Stat. Phys. 85, 551 (1996);
  Arrighi, Natural Computing 18, 885 (2019): local unitary rules on
  complex amplitudes. Here no complex number is on the lattice; the rows
  carry an integer phase and the split is an exact integer isometry; the
  unitarity of the tables holds within 315/65536 and is measured, not
  assumed.
- Bohm, Phys. Rev. 85, 166 and 180 (1952), and Duerr, Goldstein and
  Zanghi, J. Stat. Phys. 67, 843 (1992): Born from a uniform distribution
  of the hidden variable over the ensemble (quantum equilibrium). The
  ladder over u is the same logical move: u uniform over births, the map
  from u to the outcome the inverse of the cumulative weights, Born as
  ignorance of u. Like Bohm's, the pair is non-local (the second outcome
  depends on the first setting through the record); unlike Bohm's, the
  hidden variable is one integer per record and the guidance is a table.
- Nelson, Phys. Rev. 150, 1079 (1966): stochastic mechanics; here nothing
  is stochastic once u is fixed, and the paper says which randomness it
  assumes (the lamp's clock).
- GRW, Phys. Rev. D 34, 470 (1986), and Bassi et al., Rev. Mod. Phys. 85,
  471 (2013): objective collapse as a real discrete event. The click is
  such an event, but triggered by the apparatus at the record's completion
  and without a free rate or length; the paper states this difference and
  that no spontaneous collapse exists here (a pair stays entangled without
  maintenance, acceptance test 9).
- Spekkens, Phys. Rev. A 75, 032110 (2007), and Harrigan and Spekkens,
  Found. Phys. 40, 125 (2010): ontological models and the psi-ontic /
  psi-epistemic classification. The rows' amplitudes and u are ontic, so
  the model is psi-ontic in their sense and, as their argument requires of
  such a model, non-local; the paper places it there in one sentence.
- Tsirelson, Lett. Math. Phys. 4, 93 (1980); Popescu and Rohrlich, Found.
  Phys. 24, 379 (1994); Buniy, Hsu and Zee, Phys. Lett. B 630, 68 (2005)
  (discrete Hilbert space); Meyer, Phys. Rev. Lett. 83, 3751 (1999), and
  Kent, Phys. Rev. Lett. 83, 3755 (1999) (finite precision). The model's
  S(N) beyond Tsirelson at about half the N with exact marginals is a
  no-signalling box of the Popescu-Rohrlich kind at finite N, of a size
  8/N + 4 c_T that a Bell measurement of precision 0.0005 already
  constrains; the paper says this is a prediction that can fail and states
  the N it excludes.
- The experiments cited: Poh et al., Phys. Rev. Lett. 115, 180408 (2015);
  Hensen et al., Nature 526, 682 (2015); Giustina et al., Phys. Rev. Lett.
  115, 250401 (2015); Shalm et al., Phys. Rev. Lett. 115, 250402 (2015);
  Pan et al., Nature 403, 515 (2000) (GHZ); Tonomura et al., Am. J. Phys.
  57, 117 (1989), and Grangier, Roger and Aspect, Europhys. Lett. 1, 173
  (1986) (single-quantum build-up, where the register's A10 at a low rate
  is the model's registered failure under the amount reading and the
  single-record weights of the design are what the new reading must
  measure); Elitzur and Vaidman, Found. Phys. 23, 987 (1993); GHSZ, Am. J.
  Phys. 58, 1131 (1990), and Mermin, Phys. Rev. Lett. 65, 1838 (1990).

Every reference above was checked against its journal record on
2026-09-20; none is cited from memory. References added to the draft
later are checked the same way before they enter `main.tex`.

## 6. The figures, each from a registered run

None can be drawn today. Each is listed with the world it needs, what u
does in it, and the tool that reads it; the names of the worlds and of the
reading tool are the implementation's (the design names
`tools/amplitude_path.py` and `examples/events/amplitude/`; the draft uses
the names as landed). `paper/click_model/figures.py` draws from the runs'
summaries only, as `paper/figures.py` does, and its command line is
recorded in `paper/README.md`.

| Figure | Run (register entry) | u | Reading | Shows |
| --- | --- | --- | --- | --- |
| 1 The integer Mach-Zehnder | acceptance test 1's world at the arm phases 0, N/4, N/2 and the unequal arms at frequency 0, 8, 16 | 64 births, u = 0 .. 63 | the world list's channel per birth | D1/D2 counts 64/0, 0/64, 32/32 against the offers; one gather per birth; Total within +- 0.0019 |
| 2 One quantum at a time | test 2's two-slit world with the openings' neighbours freed, 64 births | u = 0 .. 63 | per-pixel weights and the click histogram | the single record's weights against the 64-birth histogram (design: correlation 0.963) and against the incoherent sum; the register's A10 at a low rate beside it as the amount reading's failure |
| 3 The pair at N = 64 | test 4's four CHSH worlds and the choosers' world | u = 0 .. 63 per setting pair | the world list binned by setting | the cells 27, 5, 5, 27; E against a - b over all 4096 pairs with the table cosine; the marginals 32/64 everywhere; #363's triangle (S = 2) in grey |
| 4 S(N) | the exact table (`checks/s_of_n.txt`, a computation) with the run points at N = 64, 1024 and 2048 | all u | the tool at each N | S(N) against N on both sides of 2 sqrt 2, the 8/N + 4 c_T band, Poh et al.'s band, the excluded N marked |
| 5 GHZ | test 5's world at XXX, XYY, YXY, YYX | all u | the world list | the four allowed triples per basis and the exact zeros; a table if a figure adds nothing |
| 6 Which-path | test 6's world | all u | the world list | S = 88/64 and the product form; the two-slit world with a measure at one opening: the incoherent weights |

Every number in the paper's tables carries a row in a table
"number, register entry, file, fingerprint" kept in `paper/click_model/`
beside the draft, so a referee can follow each one to its run.

## 7. Reproducibility

- **A tagged release.** The last tag on the remote is `v0.3.0`
  (2026-09-14, the GitHub release with the endorser's message; Zenodo
  version DOI 10.5281/zenodo.22749342 under the concept DOI
  10.5281/zenodo.22738746). `CITATION.cff` and `paper/release_notes_0.3.1.md`
  name 0.3.1, but no `v0.3.1` tag or release exists on GitHub: papers 1 and
  2 cite the concept DOI. Before paper 3 the owner decides whether to tag
  the commit the earlier papers used as `v0.3.1` (so their reproducibility
  sections resolve to a version) and tags the commit that carries
  `amplitude-v1` and its runs as the next version; paper 3 cites that
  version's DOI and the concept DOI.
- **Zenodo.** A new version under the concept DOI, uploaded from the
  release, as for the previous papers.
- **The worlds and expectations.** The acceptance worlds with their
  `expectations.json` pinned before the runs (the design's table, section
  7), the runs' `run.json` and `events.jsonl` fingerprints in
  `docs/VALIDATION.md`, the register entries with the date and the
  fingerprint, Python and numpy versions, `python tools/check.py --full`
  green at the tagged commit.
- **The reading tool.** The offline rebuild of the world's list from
  `events.jsonl` (the design's test 10) equal to the run's list, so a reader
  regenerates every table from the archived events without the engine.
- **The exact tables.** `checks/s_of_n.py` and the paper's own scripts for
  T4's table run from the repository's `core/phase.py`; their outputs are
  committed beside them.

## 8. The disclosure of AI assistance

- arXiv's policy for authors' use of generative AI language tools
  (info.arxiv.org/help/policies): such tools are not authors; the authors
  take full responsibility for every part of the contents however
  generated; use is reported in the paper.
- Springer Nature's editorial policy (Foundations of Physics follows it):
  large language models do not satisfy authorship criteria; their use is
  documented in the Methods section or, absent one, a suitable part of the
  manuscript; AI-assisted copy editing alone need not be declared.
- What paper 3 must disclose, since it exceeds copy editing: the
  simulator's code, the design documents, the check scripts and the drafts
  of the manuscript were produced with AI coding agents working under the
  author's direction and review, the author verified every number against
  the archived runs, and no AI system is an author. The draft carries this
  as a paragraph "Use of AI tools" before the acknowledgements, with the
  tool named as the venue requires; the repository's rule against model
  identifiers in artifacts leaves the tool's name and version for the
  owner to insert at submission, and the plan flags this so it is not
  forgotten. Papers 1 and 2 carry no such paragraph; whether to add one in
  a revision is the owner's call and is outside this plan.

## 9. The venue

arXiv quant-ph first, cross-listed to physics.comp-ph as paper 1 was (the
endorsement path of the v0.3.0 release). Then Foundations of Physics
(Springer): the literature the paper positions against ('t Hooft's book,
Harrigan and Spekkens, Elitzur and Vaidman, Popescu and Rohrlich) is
there, it takes long formal papers with proofs, and it has no page charge.
Alternatives, in order: Quantum Studies: Mathematics and Foundations
(Springer) if the editors of the first find the model too far from
quantum theory; Physical Review A (fundamental concepts) only if the owner
makes the finite-N departure from Tsirelson the headline, which would
need the run points at every N and a sharper c_T. Not recommended: a
journal with an article processing charge.

## 10. The honest ledger of the paper

- **Measured** (after the merge, from the register only): the acceptance
  integers of the design's table (the Mach-Zehnder counts, the two-slit
  correlations, the Bell cells at N = 64, S at N = 1024 and 2048 if run,
  the marginals in every setting pair, GHZ's zeros, which-path 88/64,
  byte-identity of the registered worlds without the key, the reading
  tool's equality with the run).
- **Proved**: T1 to T4 as restated in section 4, with the tie case of T3
  and the exact constant c_T of T4 to be worked out in the draft.
- **Assumed**: the tables at 1/256 and their rounding; the flight table's
  one speed; u uniform over births (the lamp's clock over N intervals); the
  ladder read at completion and normalised by Total (the owner's decision
  (a)); the nearest rungs; the layer as the apparatus's (form A); the
  frequency read at the click; the CHSH labels as the settings; that
  nature's pairs are this model's pairs at some N when the comparison with
  Poh et al. is made.
- **Open**, stated in the paper's last section: the continuum limit (no
  Schroedinger or Dirac equation is derived; the flight table's speed and
  the tables' rounding have no limit taken); spin and polarization (the
  labels are abstract; Malus is not in the model); bosons and fermions (no
  statistics; the meeting sums identical rows); the norm on the lattice
  (+- 315/65536 per row from the tables and the 5.10 of the shipped
  two-slit geometry when paths re-meet non-unitarily, design 2.5); Lorentz
  (one speed for every direction, no boost); the classical limit as click
  density (test 11, proposed and not decided); matter's push of a branched
  row (the sum over branches, the stated limit); the cost 2^n per
  entangled record and the register's exact depth as the ceiling
  (principle 9, the design's section 12); the single-quantum build-up,
  which the register today records as the model's failure under the amount
  reading (A10 at a low rate) and which the new reading must show on a
  changed world before the paper says it is closed.

## 11. The order of work

1. This plan committed; the owner's answer to one question: does he
   confirm the claim of section 1.3, or which claim (A, B, or his own).
2. On the Boss session's message that `amplitude-v1` is on `main` with its
   runs: read the merged design revisions, the acceptance tests, the
   register entries and VALIDATION; check every landed integer against the
   design's table and this plan's computation; note every departure.
3. Write `paper/click_model/main.tex` in the style and macros of
   `paper/main.tex` (article, 11pt, the same packages and hypersetup,
   `thebibliography`) and in the structure of section 12: abstract within
   arXiv's 1920 characters; introduction; the model (section 3 of this
   plan as two pages); the theorems with proofs (section 4); the
   measurements (the tables from the register, each row with its entry);
   the comparison with the Bell experiments (the set of admissible N); the
   literature (section 5); what is new; what is not claimed (section 10);
   the hypotheses of the program with their status (section 12);
   reproducibility; the AI paragraph; the bibliography. `figures.py` and the figures from the
   summaries. The number-to-register table beside the draft.
4. The hostile referee: the physics-rule reviewer skill
   (`skills/physics-rule-validation/SKILL.md`) reads the draft against the
   register, the design and BEAM_LAW, as a referee who wants to reject it:
   every number to its run, every theorem's proof, every "proved" and
   "measured" label, the locality claims, the non-local step stated
   plainly, the comparison with nature's data. Its findings fixed or
   answered in the draft; the report to the owner with the draft's path and
   the findings.
5. The owner's review; `paper/arxiv_metadata.md` gains paper 3's title,
   abstract and categories; the release tag and Zenodo version; the arXiv
   submission by the owner.

## 12. The structure of the paper: one claim as the result, everything else a hypothesis with its status (the owner's instruction of 2026-09-20)

The paper has two parts. Part I is the result: the one claim the owner
confirms (section 1), with its definition, theorems, measurements and
comparison; nothing enters Part I that is not proved or registered.
Part II is "The hypotheses of the program": everything else the
repository holds, from the ten principles of `amplitude-v1` and the day's
decisions in Highlights 5.4 to the series' verdicts on gravity, the
nucleus, the weak force and the meeting, each stated as a falsifiable
hypothesis with its status and asserted nowhere as a result. The status
values: **registered run** (in the experiments register with a
fingerprint and a date, the verdict quoted), **design only** (a check
script's integers, no engine run), **not run** (stated on the hypotheses
page or in Highlights, no design and no run), **published** (papers 1
and 2). The table below is the section's draft; the draft quotes each
verdict's own words and links each row to its entry.

| Hypothesis, stated so that it can fail | Status | What the record says | Where |
| --- | --- | --- | --- |
| The world is the list of clicks; the GameBoard computes every continuation between clicks (principles 1 to 4, 7) | design only, becoming registered with `amplitude-v1` | the integer Mach-Zehnder, Born over u, one gather per birth | design sections 2 to 3, `mz.txt` |
| The detector layer is the only non-local operation and is the apparatus's (principle 5, form A) | design only | the layer's table, lazy deletion, form B kept as the local alternative | design sections 5, 9, 11 |
| Entanglement is a record with rows in two places, no further rule; S = 2.83 with no-signalling (principle 6) | design only (the prototype's 2.875 was a rounding); Part I once registered | 176/64 at N = 64, marginals exact | `bell.txt`, Part I |
| Matter is structure that closes records; classical where clicks are dense, quantum where none (principle 8); the classical limit as click density (test 11) | not run | proposed after the ten acceptance tests, not decided | Highlights 5.4 "DECIDED: amplitude-v1 is built" |
| The price 2^n per entangled record; a finite host predicts a ceiling, a description does not (principle 9) | design only | rows n x 2^n; the register's exact depth (62 balanced splits; Grover's six rotations exceed it on the lattice) | design sections 10, 12, `gate.txt` |
| The two-record gate: CNOT as a joint label permutation; CNOT twice the identity; GHZ from two CNOTs; Grover clicks the marked row for every u | design only, acceptance tests after the merge | all four checked on the host's integers | `gate.txt` |
| In the continuum limit Dirac and Lorentz (principle 10) | not run, not derived | stated; DERIVATIONS covers the earlier engines, not the Beam Law | Highlights 5.4; DERIVATIONS sections 51 to 56 |
| Polarization, bosons, two sources of mass, gravity of the click model (principle 10's open list) | not run | open | Highlights 5.4 |
| Bell under the amount reading: S = 2 exactly, the triangle 1 - 4k/N, no-signalling exact (the law's limit) | registered run (2026-09-19) | measured = expected, 326 criteria, the model's limit against the 2015 data | A2 under the Beam Law |
| The law does not correlate the settings with the pair through their common past (no superdeterminism) | registered run (2026-09-20) | every E on the triangle, S = 2 on the quadruple, marginals 1/2 in 15 bins; the one-clock control sees the built-in correlation | A2 with the choosers; HYPOTHESES 11 |
| Heisenberg in the record: the `wave` record narrows with the opening, the count does not; w x FWHM = 0.886 lambda | registered run (2026-09-20) | within 22 % at w = 27; not read at smaller widths (the fan's limit) | A10 |
| Fringes do not build up one click at a time under the amount reading | registered run (2026-09-20) | the narrowing 0.31 at six rays per pixel per interval, gone at 0.14: a plain disagreement with nature, the law's limit; the `sum` reading's single-record weights are the design's answer, to be measured | A10 at a low rate; design test 2 |
| The couplings on the plane: the identities, books and timing of the Beam Law hold; the far field of a six-beam source follows the Node count | registered run (2026-09-19) | exact identities; the ring means outside the +- 10 % expectation for six beams | C under the Beam Law |
| The orbit under the Beam Law | registered run (2026-09-19) | registered; the verdict quoted in the draft from its entry | D |
| The clock's redshift in space: M / r on the age clock and M / r^2 on the push from the same rays; no horizon | registered run (2026-09-20) | the 1 / r form holds; the pinned 15 % criterion missed at three radii by the shell ripple | E; PREDICTIONS 1 |
| The Hubble diagram behind the detector: linear near, coasting far, nothing accelerates | registered run (2026-09-20) | z = v/c to 0.003, H t_0 = 1.03; q not told apart at this precision | G |
| Bohr's lines behind the detector | registered run (2026-09-20) | no orbit closes under whole kicks; the lines not read, neither for nor against | H |
| The nucleus: the strong reading a cut 1 / r^2 with the opposite sign, no Yukawa tail; the deuteron bound at one Link; the alpha a line, not a square | registered run (2026-09-20) | integer by integer as designed; the order of the bodies a declared tie | I |
| Light beside a mass: neither bent nor delayed without a rule that reads the crowd | registered run (2026-09-20) | 0.000 pixel, 0.00 interval: a plain disagreement with nature | K; PREDICTIONS 2 |
| Under the meeting light bends toward a mass with the sign and the M / b form, not delayed, not redshifted; an interferometric Shapiro phase per path | registered run (2026-09-20) | the sign in every world, the form inside its brackets, the grain 10^4 times nature's angle, so the value is not claimed; the mass absorbs the light it bends most | K under the meeting; HYPOTHESES 20 |
| The weak force: the neutrino's admitted fraction w / N exactly, flat in energy; the neutron's decay a step with a line spectrum; a bound neutron later or never under the crowd gate | registered run (2026-09-20) | plain disagreements with nature (the exponential survival, the continuous spectrum, the stable bound neutron), registered as the law's limits, nothing tuned | J; PREDICTIONS 7, 8, 10, 18 |
| A moving body's clock ticks at one rate at every speed; nature's gamma a limit | not run (series J4 defined) | the engine's finding; stated so that it can fail | HYPOTHESES 21 |
| Redshift from delay growth on a closed GameBoard; the supernova test | published | paper 2: behind flat LambdaCDM by delta chi^2 = 9 to 106; the Tolman exponent against it | paper 2 |
| Dark matter is a closed dimension; G = hbar c / (N m_0)^2; one mass ladder; confinement from the quark's field rays; the lottery as the only door | not run | forms, not values; the hypotheses page | HYPOTHESES 6, 12, 13, 14, 1 |
| The 23 predictions of the law's own list | mixed: 1, 2, 5, 7, 8, 10, 18 registered; the rest not run | the five strongest quoted in Highlights 5.4 (the retarded field's aberration, the Nordtvedt-like flux, no radiation from accelerated charges, bodies outrunning light, no mass defect) | PREDICTIONS.md |

Two rules for Part II. A hypothesis that a registered run contradicts is
written as the model's limit in the register's words, never softened;
a hypothesis without a run is written in one sentence with no number.
Nothing in Part II is cited by Part I, and the abstract names Part II in
one clause ("the hypotheses of the program are listed with their status
and claimed nowhere").
