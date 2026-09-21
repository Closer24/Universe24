# The click model paper: the plan (two pages)

2026-09-20, the paper coordinator's session; base `072fd8bd`. The long
form with every argument, table and number is [RECORD.md](RECORD.md);
this page holds the decisions and the work. Every number cited here is
one of three kinds and is named: the register, the design's check outputs
(`docs/designs/amplitude-v1/*.txt`), or this directory's own computations
(`checks/`), which are computations from the design's formulas with the
repository's tables and not runs of the engine.

## Decided by the owner (2026-09-20)

1. **A new paper 3, on the click model only** (the owner, in order: "stay
   with one new paper", then "a completely new paper", then "paper 3, new;
   update the plan: only the new engine"). The paper is about the model,
   the law of the click (Definitions 1 to 3 and the theorems); the engine
   is not its subject and appears only as the instrument that produced
   each registered number and in the reproducibility section. One law:
   every number in the paper is a registered run of the finished
   implementation of the click after `amplitude-v1` is on `main` ("run
   after everything closes with the new implementation"), at N = 64, 1024
   and 4096; after
   `amplitude-v1` the key is removed ("the one click"), so the paper
   describes one law and no keyed alternative. Papers 1 and 2 are not
   changed and not resubmitted; paper 1 is cited in one paragraph as the
   "before" (the local candidates at S = 2, the shared registry at 2.83,
   the choosers' run) and none of its tables is reproduced, since its
   engine was deleted on 2026-09-17. The manuscript is
   `paper/click_model/main.tex` with its own `figures/`; a new arXiv
   submission (quant-ph, cross-list physics.comp-ph), a new Zenodo version
   under the concept DOI, a new tag.
2. **The claim** ("the amplitude runs, because they unify everything"): on
   a local integer GameBoard whose only one-way step is a click that reads
   the accumulated sum of one record's rows and chooses by the birth phase
   u on nearest-integer rungs (the Born rule as the one measurement rule,
   put in, not derived), the world's list of clicks reads single-quantum
   interference, Bell pairs with marginals exactly 1/2 at every setting
   and every N (no-signalling proved for the equal-weight pair), GHZ's
   exact zeros, and a CHSH value S(N) that is an exact rational of N,
   two-sided within 8/N + 0.044 of 2 sqrt 2 and above Tsirelson's bound
   for about half the N; the photon-pair value 2.82759 +- 0.00051 (Poh et
   al. 2015) constrains N under stated assumptions (64 and 256 out, the
   powers of two from 512 in) and validates nothing. The click is
   non-local (the second click reads the first's setting and outcome, then
   deletes), the apparatus's, forced by Bell's theorem; the lattice is
   injective between clicks given the apparatus's record. Not claimed: a
   derivation of the square, a continuum limit, spin, statistics, Lorentz,
   exact unitarity on the lattice.
3. **The structure**: Part I the result (the one claim, its definition,
   theorems, measurements, comparison); Part II every other statement of
   the program as a hypothesis with its status (registered run, design
   only, not run, published), split into consequences of the click model,
   each with the rule it follows from, and conjectures of the same
   GameBoard that the click does not imply (the forces, the nucleus, the
   weak force, the meeting, the redshifts, Bohr, dark matter, G), asserted
   nowhere as results.
4. **The phase circle's bound** raised to 65536 on this branch ("raise the
   bound"), so the pair's half-angle tables exist at N = 4096; the engine's
   branch carries it before that run.

## What the checks changed in the recommendation

The recorded recommendation said S <= 2 sqrt 2 at every N, |E - cos| <= 1/N,
epsilon <= 4/N and N >= 4000 from "S = 2.8276 +- 0.0008". The computation
`checks/s_of_n.py`, which reproduces the design's Bell numbers exactly,
shows: 252 of 512 N up to 4096 above 2 sqrt 2 (N = 16, 32: S = 3; N = 128:
2.875); N |epsilon| up to 7.76; the per-E bound is 2/N plus the tables'
term 0.011, which does not shrink with N; the measured value is Poh et al.'s
2.82759 +- 0.00051 (the 0.0008 is its distance to Tsirelson), it selects a
set of N and not a half-line (smallest admitted 184; 64 and 256 excluded;
the powers of two from 512 one sigma above). `checks/which_path_window.py`
shows that a partial which-path window on one arm gives neither the
linear nor the quadratic duality relation and makes the absorber's count
depend on the arm phase and the window's centre, because the window and
the ladder read the same u. The owner's ruling (2026-09-20): no partial
case is needed. The paper measures only the design's own worlds on the
finished engine, and a which-path device in this model is a `measure`
without a window, all or nothing; a windowed entry on an arm is a
different apparatus and therefore a different world, since placing a
detector or an emitter on the GameBoard changes the record's offers and
the ladder's rungs (principle 8: the structure is the program; design test
8: the same u falls elsewhere when a detector moves), not a weaker
measurement of the same world. The partial computation stays in `checks/`
as a note to the design owner only (whether a phase window on a branched
record is meant to be lawful), out of the paper. Rule for every number:
the new engine after it is finished, from the register; the checks are
the plan's evidence and never a substitute for a run.

## The four theorems, as the draft states them (`main.tex`, section 2)

T1 the interval without a click is an injective Z-linear map on the
records' modules; T2 the split is an isometry whose transpose inverts it
up to the scaling (kw, k^2 m), and U_s^T U_s is a scalar in integers; T3
the first party's rung is exactly N/2 for every setting pair and N, and
the second party's marginal is N/2 except at a rung tie (none for N <=
512, every pair; a tie rule is asked of the design); T4 |E_N - cos| <= 2/N
+ 4 arcsin(sqrt 2 / 512), hence |S(N) - 2 sqrt 2| <= 8/N + 0.044, two-sided,
with S(N) tabulated; the statements "S <= 2 sqrt 2 at every N" and
"|E - cos| <= 1/N" are withdrawn as false.

## The work, in order

1. Done: the plan, the checks, the draft's formal part.
2. Done (2026-09-20, after PR #370 merged at `d2064195`): main merged into
   this branch; the 46 worlds of series L run again on the merged tree
   (`tools/run_series.py`, fingerprint `731d0f56c9f9`; the register's
   `ff5c382d672f`), every run's register replayed equal to its world by
   `tools/amplitude_path.py --check` (45 of 45 keyed runs), every integer
   equal to the register's and to the expectations file
   (`summarize_runs.py` -> `figures/summary.json`); the four figures drawn
   by `figures.py`; `NUMBERS.md` maps every number of the paper to its
   source.
3. Done: `main.tex` completed as paper 3 (the abstract within 1920 characters, the
   introduction with the plain description and paper 1 as the before, the
   model, the theorems, the measurements from the register, the finite-N
   comparison, the causal anatomy, what is new, what is not claimed, the
   hypotheses of the program, reproducibility, the AI paragraph, the
   bibliography). Compiled by the owner's local agent before the merge;
   to be compiled again after these edits (no TeX in this session).
4. Next: the hostile referee (the physics-rule reviewer skill) on the
   completed draft; findings fixed or answered; the report to the owner.
5. The owner's review; `arxiv_metadata.md` gains a third entry; the
   release tag and Zenodo version (no `v0.3.1` tag exists on GitHub though
   CITATION names it: to resolve); the new arXiv submission by the owner;
   venue after arXiv, Foundations of Physics.

## Reproducibility and disclosure, in one paragraph each

A tagged release after the merge, archived as a new Zenodo version under
the concept DOI 10.5281/zenodo.22738746; the acceptance worlds with their
`expectations.json` pinned before the runs; the runs' fingerprints in
VALIDATION; the reading tool that rebuilds the world's list from
`events.jsonl`; the `checks/` scripts with their outputs; Python and numpy
versions; `python tools/check.py --full` green at the tag. The AI
paragraph, required by arXiv (tools are not authors; authors responsible
for every part; use reported) and by Springer Nature (LLM use documented
in Methods or an equivalent part): the simulator's code, design documents,
check scripts and manuscript drafts were produced with AI coding agents
under the author's direction and review, every number verified against the
archived runs, no AI system an author; the tool's name is inserted by the
owner at submission.

## Referee round 0: the owner's reading of the compiled draft (2026-09-20)

Seven pages read cold. Each point, with what the draft now does:

1. Born is inside the click's definition, not derived; u uniform is an
   assumption. Accepted: the title no longer says "without a configured
   law"; a paragraph after Definition 3 names the three inputs (the
   square, u uniform from a lamp at N consecutive intervals and
   independent of the settings, the tables) and what is derived from them.
2. The non-locality is more than deletion: B's rung is computed from
   W(o_A, o_B) with A's setting and outcome. Accepted: stated in
   Definition 3, in the plain description ("the second click reads what
   the first wrote") and after Theorem 3.
3. The tables' norm: not +-315; 65897 at N = 4096, p = 503. Confirmed by
   computation: the range is -351 to +361 for every power of two through
   65536; the draft says so. The rotation is not an isometry: confirmed
   (65705/65536 at N = 64, s = 1); Theorem 2 and Theorem 1's proof say
   "injective, an isometry only up to the tables' rounding".
4. Reversibility: the split resets the age. Accepted: Theorem 1 is
   restated as injective given the apparatus's record of absorbed rows,
   and says the split forgets the age without it. No-signalling's scope
   (equal weights, two labels, the rung tie) is stated; unequal weights
   are open. One click per record and the click's timing: a lemma.
5. The results are placeholders. Yes, by design: filled from the register
   after the runs (step 2).
6. The departures from quantum mechanics: N is not fixed by the model, so
   the comparison with Poh et al. constrains N under stated assumptions
   and validates nothing; the draft says so, with noise and inefficiency
   named as not modelled.

Not done, and not attempted: an independent derivation of the square.
The paper claims the model, its theorems and its computed departures,
which is the claim the reader said can be supported.

## The Highlights read on 2026-09-20 (records 89 to 100 of the dated log), and the sharpest claim

What changed for the paper: **record 96** decides that interference is
coherent within one Node only (a set of Nodes is one cell whose weight is
the sum over its Nodes of the per-Node squared pointer); Definition 3 of
the draft says so now. **Record 94** reports the single quantum on the
engine (the Mach-Zehnder and Elitzur-Vaidman integers as designed; the two
slits with two measured departures: the tables' rounding makes the
weights depend on u by parts in a thousand and moves one rung, and the
acceptance world's geometry changed); cited only once registered.
**Record 97** proposes, the owner's decision pending, that u is the
record's own field unread by the lattice and that a row pushes matter
with its share of the record's label; the draft already says no rule
reads u, and the meeting's reading of the path phase enters Definition 2
when decided. **Records 89 and 93** carry the statement this plan's
computation refuted ("S = 2 sqrt 2 - epsilon(N), epsilon <= 4/N, never
above Tsirelson; N >= about 4000; 12 bits"): the Highlights' owner should
mark them superseded by the computation (`checks/s_of_n.txt`: 252 of 512
N above 2 sqrt 2; the bound 8/N + 0.044 two-sided; the set of admissible N
from Poh et al. starting at 184); the bits-per-click bound of record 93
(at most log2 N per click) stands on its own and does not need the Bell
bound. **Record 95** asked for the formal part now: done.

The sharpest claim, in the Highlights' own words and the draft's terms:
"The world is the list of clicks" made exact. One measurement rule, the
click that reads one record's squared sum and lets the birth phase choose
on nearest-integer rungs, put in once; from it and the lattice's
invertible rules, four theorems (injective between clicks given the
apparatus's record; the split an exact isometry; the marginals exactly
1/2, no-signalling; the finite-N Bell value within 8/N + 0.044 of
2 sqrt 2, two-sided) and one table of exact rationals S(N); and the
measurements of the finished engine (the Mach-Zehnder 64/0, 0/64, 32/32;
Elitzur-Vaidman 32/17/15; the pair's cells 27/5/5/27 at N = 64 and 181/64
at 1024 and 4096; GHZ's zeros). Everything else is a hypothesis with its
status. What makes it sharp is what it refuses: no derivation of the
square, no fixed N, no claim below Tsirelson, no number before the
register.

## Referee round 1: the physics-rule reviewer as a hostile referee (2026-09-20)

Verdict: major revision; every number confirmed, the definitions and two
theorems not the model that produced them. Twenty-eight findings, all
applied to the draft the same day:

- Blocking, fixed: the rotation's matrix (the turn on the label-1 column,
  as the engine has it, without which Y = X and GHZ is impossible); the
  pair's "second click" narrative replaced by the engine's one gather at
  completion from both settings (nothing is deleted; the near party's row
  is written at the far tick); Theorem 1 restricted to F, S, R, M with the
  collision named a nonlinear bijection that acts in no reported world;
  E(N/4, N/8) = 46452/65773; the CNOT rows' provenance stated (re-run after
  the gate's fix, reproduced on the paper's tree, now in summary.json).
- Should fix, fixed: the figures' tree attributed to the paper branch's
  merge 4ccf65c7 (fingerprint 731d0f56c9f9; main's is 48a9d1c91661); u is
  every row's starting phase (the "read by no rule" qualified; the eight
  totals explained); the pair form of the phase turn on the row, the click
  reading p as is; Theorem 2's inverse the conjugate transpose; the tie
  evidence cited as computation and the review's re-read; Theorem 4 "off
  a tie"; the tables' norm script added (`checks/tables_norm.py`); Lemma 1
  scoped to records whose rows all end; the two-slit re-pin disclosed and
  Figure 2's 0.931 attributed to the generator's reading (the run's 15
  clicks: 0.655); the preferred party by declaration stated; Hong-Ou-Mandel
  marked as needing a rule the model lacks; the windowed which-path result
  reported as a computed departure; the reading tool named a consistency
  check, not an independent implementation; the registry's 2.83 attributed
  to paper 1's own archive; the 12 gate and far worlds added to the summary.
- Minor, fixed: the meeting noted as absent from the paper's worlds; the
  abstract's injectivity qualified; "allows" for "must"; the module's
  quotient narrowed to one m per set; live units; Figure 3's curve named
  E(d, 0); Hensen "no N at three sigma"; the fair-sampling assumption; W
  defined in Definition 3; the missing v0.3.1 tag already in step 5.

## The information-transfer report (2026-09-20, the owner's request)

`INFORMATION_TRANSFER.md` lists the formulas that follow from "everything
on the GameBoard is a transfer of information" under the paper's rules,
each with its label and its real-world reading, and the numbers are in
`checks/information_transfer.txt`: the L1 causal cone (one Link per
interval; the front an octahedron, 42 percent slower on the body diagonal),
the wavelength `N d / n` Links and the bound `a <= lambda_min / 2`, the
click's precision `1 / (2 N)`, no amplification at a split (Theorem 2 as
no-cloning), at most `log2 (cells)` bits per click, the joint law of the
pair from `u`, the distance independence (the far worlds), reversibility
between clicks with a Landauer reading as a conjecture, and the two-slit
path difference under the L1 count (constant beyond the slit separation,
no Young fringes; the register's Pearson 0.368 with the cosine). The
sharpest open item is the metric: which length a row's phase counts, and how
the L1 count becomes Euclidean at scale. Sent to the Boss as issue #376; the
half-page for Part I waits on the Boss's answer to its questions 1 and 2.

## The Boss's answers and the cone test, L7 (2026-09-20)

The Boss answered on issue #376: the phase counts the Links stepped (the
integer form); the proposition is acceptable with the layer the
apparatus's and every lamp's rows records; Landauer out of Part II; the
isotropy question to the physicist as record 140. The approved one-world
test became two worlds of one geometry (`cone_links`, `cone_intervals`,
series L7, prepared on a local worktree from the one click's head, no src
change): the flight table moves every direction at 1 / sqrt 3, so both
rows click at the age 29; the integer form of `phase_per_link` gives the
path phases 51 and 8 (17 and 24 Links), the pair form 23 and 23 (29
intervals). Every pin met. The report's rows 1, 2 and 9 corrected (the
octahedral front was wrong; the phase's metric is the declared form's).
The registration (the register's L7 item, the README, a test, the
changelog) waits on the owner's word for a branch and a pull request, and
on PR #395's landing for the run on main.

## L7 landed; one fact for Part II (2026-09-20, evening)

The Boss cherry-picked the two registration commits onto main (82cf8cc7,
049cb233) and merged them as PR #399 at 272b715b; record 144 stands as
the record. The paper directory stays on this branch for the owner's
word. For Part II, from the Boss's message and the fraction-free work
(record 147 on main, record 148 to follow): the count of a clock whose
rate changes is the whole part of the integral of its rate (the
accumulator on the record), and the Bell S = 176/64 is independent of
the tick alignment when read by the birth ordinal; the fraction-free
unification re-pins the register's ticks once, so the paper's registered
integers are to be re-checked against the register after it lands
(`summarize_runs.py` on the re-run, every integer expected equal).

## The owner's direction and the continuum limits (2026-09-20, night)

The owner: focus on the transition between classical and quantum physics
(the model's advantage); take the computation on the Nodes to infinity and
the known formulas must return, Einstein's included, special and general,
as Fourier returns pi. Done: `checks/limits.py` and the new section
"Continuum limits" of the draft: Tsirelson's value as the limit of S(N, Q)
(the bound's two terms vanish), the isotropic cone and the plane wave
(omega = c k, L7), Young under the fan's discreteness (the true residual:
27 of 75 pixels see both openings; 0.45 at 91 directions, 0.90 from 721;
the flight's rounding alone 0.07, so the earlier diagnosis "the rounding
at lambda = 8 is the killer" was wrong and is withdrawn), the continuity
equation from the books. Not returned and said so: Lorentz invariance (the
lattice is a rest frame) and the field equations (no mass in this model).
The classical limit as one row per record, and the cost of a quantum as
its rows (86 units per Mach-Zehnder record, 729 per GHZ-by-gate record, 3
bits out), noted for Part II. Sent to the Boss for the mathematician: the
click as the evaluation of Z[Z_N] at zeta_N, the accumulator's exact phase
and exact u, and now the limit's symmetry (a moving body's c) and the
field equation of the delay rule.

## The law as one piecewise-linear map (2026-09-21, the owner's framing, sent to the Boss and the derivation mathematician)

The state is an integer vector on a torus; every interval translates it by
a rate, thresholds, subtracts; the events are what crossed. Where the rate
is constant (the rows between clicks) the map has a closed form, the floor
of a linear function: the quantum part is computed without runs (the
paper's checks do so). Where the rate depends on the state (the push, the
collision, the crowd) the map is a difference equation whose solution is
the iteration or the continuum limit: the classical part. The boundary is
the property of the rate. Proposed sentence for the model section, pending
the owner's wording: "the model is one piecewise-linear map on an integer
torus; the measurement is the one threshold that is read out." Also
pending: a `checks/formula_run.py` that recomputes every integer of the
measurements table from the formulas (a run without runs), offered to the
owner. The mathematician's two-slit answer (records 156, 160): the wheel
W = 2^12, the exact phase and the fan's width P wait for the owner's word;
`slits_huygens` ordered on main; the paper's numbers re-pinned once after
the fraction-free batch.

## The click's square, sent to the Boss for resolution (2026-09-21)

The one-sentence paragraph names the click's fourth operation, the square
(commit ae450bfd). Three placements sent to the Boss on the owner's word
("send it all to the Boss for a solution"): (1) keep it and prove it
forced (Theorem 2's conservation admits only k = 2; a lattice Gleason, for
the derivation mathematician); (2) the square as the return (Cramer's
transactional form, the owner's postulate 24, retired on 2026-09-19),
which makes the click local but is constrained by two experiments: a
real-time return puts the click at 3 L / c against time-tagged detections
at L / c, standing returns fail delayed choice; (3) the apparatus's ledger
as today, the one atemporal step. The owner inclined to reopen 2026-09-19
and, on the two experiments, sent the whole for resolution. The paper
keeps (3) with (1) beside it until the answer.

## The main course, to the skills (2026-09-21)

The owner: "add it to skills, ask the Boss to add it to their skills; this
is the main course". Drafted as a section for skills/workflow.md with one
line per role (equations first, runs as confirmation; class 1 constant
rate, closed form, the formula pinned before any run; class 2
state-dependent rate, the difference equation, the iteration or the limit;
every formula meets known physics twice; the classical-quantum boundary as
the property of the rate), sent to the Boss by trigger and posted on issue
#376 for the owner. The Boss edits the skills on main; nothing in skills/
is touched on this branch.

## Referee round 2 (2026-09-21): the material added since round 1

Verdict: major revision; every integer of the measurements table, the
four theorems and the S(N) table confirmed. Twenty-two findings, all
applied the same day: the abstract no longer promises fringes; the
one-sentence paragraph claims the counts of the table computed before
their runs (not "every number"), names the collision table and the push by
share as engine operations that act in none of these worlds, and says
"releases" for the gathered record; Figure 3's caption corrected (18 of 19
registered E on the step curve; the choosers' bin (51, 8) reads -28/64
where E(43, 0) is -32/64); the bound at Q = 2^20 corrected (0.125, 0.031,
0.0078; the Q = 256 values 0.169, 0.075, 0.052); the flight's speed stated
as within 0.8 percent of 1 / sqrt 3 at the flight scale Q_f = 64, the
sphere only as Q_f grows, the two scales named apart; u defined by the
birth ordinal, uniform over N consecutive births; the Young paragraph
names the wheel first (the click set periodic in u, record 156), the fan's
angular measure (record 160) and the rounding's 0.02 on the world; the
continuity paragraph reduced to the two exact conservations with the
offered norm's departures (the eight totals, 1.136 on the two slits); the
world-key sentences dated to the tree of the runs, L7's tree and
fingerprint stated, the version DOI to replace the concept DOI at
submission; the multiplicity rule as built; the tie evidence cited to the
gate review; the reviewer's recomputation of the marginals worded as such;
the proof's delta with the least table length (0.0443 everywhere); the
choosers' world cited for measurement independence; "computed" for the
tables' unitarity; the lattice defined once as the GameBoard; the layer's
necessity argued (18 intervals apart). Left for the owner: the title, the
arXiv identifiers of papers 1 and 2, confirmation of the two experimental
values against the PDFs, the release tag and version DOI.

## Referee round 3 (2026-09-21): the round-2 fixes verified, three majors

Verdict: major revision, narrow; every registered integer, the proofs, the
definitions against the engine and the story's consistency confirmed; the
22 round-2 fixes verified. Three majors, all applied: (1) the exclusion of
N = 256 (and the admitted set from 184) holds at the CHSH labels only,
since E depends on (a, b) beyond a - b: at N = 256 the maximum of S over
all quadruples is 91/32 and 181,152 quadruples lie within three sigma of
Poh; at N = 64 the maximum is 11/4, so its exclusion stands; a third
assumption stated in the Bell section and the abstract qualified "at the
CHSH labels"; (2) the plane-wave "limit" was a tautology of the check's
own definition of k (omega = c k by construction) and is withdrawn, the
record's interference wavelength c N d / n kept; three limits and two
conservations now; (3) measurement independence "by construction" was
false: u and a chooser are both clocks, independent when the chooser's
period is coprime to N and the run covers the common period (the
registered world's periods 3 and 5), and a period sharing a factor with N
would correlate by construction ('t Hooft's case). Minors applied: the
bound 0.0444 and 0.045 with rho = 256 - sqrt 2 / 2 (0.0443 was rounded
down); the eq. (ebound) middle term as proved; the archived engine's N a
power of two disclosed; the tie evidence computed and printed (the CHSH
labels to 4096, every pair at 1024) and record 105 cited as it reads; the
loophole-free comparison restricted to Hensen's CHSH value (the CH-Eberhard
experiments need the detector efficiency); Bohm's |psi|^2 distribution
stated correctly; Meyer and Kent cited for finite precision, not for
Tsirelson; psi-ontic wording; the labels' weights in eq. (joint); the
Young plateau at 0.90 named with its cause; the count of limits; the
checks bibitem completed; the two-slit figure labelled; the roadmap names
the limits section; "lattice" wording; u on the row in the archived code
noted; the one re-pin noted beside "computed before its run"; Figure 3's
caption counts distinct pairs (17 of 18). Left for the owner: the title,
the arXiv identifiers, the two experimental values against the PDFs, the
release tag and version DOI.

## Referee round 4 (2026-09-21): minor revision; the round-3 fixes verified

Verdict: minor revision; every round-3 fix verified (the quadruple maxima
and the 181,152 recomputed independently; the bound's constants; the
wavelength algebra; the periods 3 and 5 and the 960 births; the tie
evidence; every integer of the table and the figures). Nineteen findings,
all applied: the method claim excepts the two slits (its expectation is
the generator's reading of the reference world slits_one on the engine,
not a check script's closed form), in the thesis paragraph and the
table's caption; the archived version named as the tagged release after
the merge (one tree holding the three trees and the cited records), the
log bibitem extended to records 144, 156 and 160; the class sentence of
the causal section made consistent with the coprime-periods statement;
"wave" dropped from the roadmap's list; u on the tree of the runs (the
lamp's phase at the birth) stated beside the archived code's (b - 1) mod
N; "is done with the record" for the tree of the runs; the 512/2048 cited
to the checks; the light cone's source named (information_transfer.txt);
the plateau's cause withdrawn as not computed; the sphere sentence made
precise (each direction's speed; the front's shape the fan's); the
powers-of-two qualifier on the tables' norm in two places; 19 bins and 18
distinct pairs; U^T U diagonal; Theorem 1 excludes an end at a face or the
border; the Q term as proved; superdeterminism wording; the packet's
bookkeeping; the interpreter as the project's declared one and the
duration claim dropped; NUMBERS.md rows for every number of the Young
paragraph and the withdrawn plane-wave row marked. The referee: once
findings 1 to 3 are applied no major finding remains and the manuscript
is stable in its physics, numbers and proofs. Round 5 confirms.

## Referee round 5 (2026-09-21): the round-4 fixes verified; twelve items, none a proof or a registered integer

Verdict: minor revision; every round-4 fix verified; the proofs, the
integers and the literature attributions confirmed once more; LaTeX
checked by script (references, citations, braces, figure files). Twelve
findings, all applied: the bound at N = 256 with rho reads 0.076 (0.075
was the nominal Q); the 0.96 prediction credited to the screen's fan of
record 156 (one direction per pixel, equal multiplicity), the angular fan's
own pin (fringes in the weights, none in the clicks until the wheel)
stated beside it; the Young limit counted as partial (two limits, a
partial third, two conservations) and "not a continuum limit" qualified
"of the model as a whole"; NUMBERS.md declares the map as a fourth kind
and gains rows for every remaining number (the sigma distances, 3944 and
33/64, 0.655, -88 to +237, the offers, the fan's 91/75/27, the ceiling's
62/13/6/3, the periods and the 960 births, the 80 sets);
information_transfer.txt section 2 relabelled to intervals and c N d / n
Links; the multiplicity rule dated to the two trees; R's injectivity
argued through diag(1, v(t)); the CNOT-GHZ triples worded as the two sets
exchanged; the phase window named a rule outside Definition 2 that reads
u; eq. (joint) shortened and the labels' weights moved to the sentence;
the measurements table set in p-columns at footnotesize; the double
citation merged. Round 6 is the confirmation.

## Referee round 6 (2026-09-21): stable

Verdict: minor revision; the referee's line: "stable in its physics,
integers and proofs; no finding changes a registered integer, a claim's
truth on the paper's own tree, or a proof". Every round-5 fix verified,
the E of all eighteen registered pairs, the bounds, the tables' extremes
and the CNOT-GHZ triples recomputed once more. Nine residual items, all
applied: the table's column separation (the width was 0.26 in over the
text); the count of worlds (46 of series L, 45 under the key in the
summary, slits_one read by the generator); two scope qualifiers (the phase
window on the model as defined, where the row's phase starts at u, not
the archived code's path phase; the rotation's row form exact for t a
multiple of N/4, the only turns used); NUMBERS.md's ceiling row relabelled
and the 27 sourced to record 156; "the first N births, one per u" in
three places; the equal-weight fan "has not converged by the width 64"
with its three values; information_transfer.txt section 7's units marked
illustrative. The referee rounds stop here: the manuscript is stable;
what remains is the owner's (the title, the arXiv identifiers, the two
experimental values against the PDFs, the release tag and version DOI,
the compile), and the register's re-pin when the fraction-free batch and
the wheel land, after which the summary is re-run and the numbers
re-checked in one pass.
