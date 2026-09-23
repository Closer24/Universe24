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

## The c judgement, the Lorentz section and the octahedron (2026-09-21, the owner's directions through the Boss, records 217, 219, 220, 226, 230)

The owner: "go in the direction of c in the paper if it is a breakthrough";
"summarise the decision to be made on Lorentz; put it in the paper";
"the octahedron is needed, a picture of it in the paper"; the architect's
four abstractions to be used after a referee round. The Boss's three
conditions for "a breakthrough": (i) the value of c in Links per interval
follows from locality and straightness alone with no measured input; (ii)
a prediction absent from physics that a measurement can refute (the
finite-grain anisotropy); (iii) it survives the known lattice bounds.

The judgement, after referee round 7: **not a breakthrough by the three
conditions; c is a section** (a proposition with the figure in the model
section, and a sentence each in "what is not claimed" and the
positioning). (i) Fails as posed: the two rules give the supremum
1 / sqrt 3 of isotropic paces (Cauchy-Schwarz, the proof in the paper),
and the flight table's sitting at the supremum is a third statement of
the design, not a consequence (a slower isotropic pace obeys both rules;
DERIVATIONS_BEAM 13.2 (a) says the same: isotropy at the diagonal's pace
is a second axiom beside the causal bound); no measured input enters, but
the value rests on three statements, not two. (ii) Holds in kind and not
in novelty: the anisotropy is the rounding's, below 1 / T_d, of order
1 / (sqrt 3 Q_f) (0.77 percent on a heading at Q_f = 64), and an isotropy
bound of 1e-18 puts Q_f at or above 5.8e17 in order; but a lattice
anisotropy of c bounded by the isotropy experiments is what every lattice
model of light predicts in kind, so the prediction is a bound on the
grain, not a number physics lacks; and, worse for the law, its own bond
clock (the derivation's 12.3, gamma^2 along and gamma across, nothing to
contract) predicts the classical ether's two-way anisotropy of order
beta^2 / 2, 1e-8 at the Earth's orbital speed and reversing over the
year, which the same 1e-18 refutes for route (A) whatever the lattice's
frame. (iii) Fails: 1 / sqrt 3 in lattice units is the Courant bound of
the discretised wave equation on the cubic grid (1 / sqrt n), whose
necessity half is this very argument (the sphere of radius c dt inside
the stencil's octahedron), and the lattice Boltzmann sound speed c_s^2 =
1 / 3, whose models also stream every population with one operator; what
the paper adds is the exact integer table at the bound, its rounding's
anisotropy as a bound on the grain, and the intent of one operator for
rows and bodies (form B: decided, in build, not on main), a design intent
and not a result. A finding for the design: FORM.md section 1 says the 2072
equalities are "the cube diagonals"; 8 are, and 2064 are directions near
them where isqrt's floor closes a gap below 1 / Q_f (the shortest
(22, 21, 21)); the bound and the pace's interval are unaffected.

Written: the paragraph "The pace of the rows, and the octahedron" with
Proposition 1 (the pace) and Figure 1 (`octahedron.py`,
`figures/octahedron.pdf`) after the flight table's sentence in the model
section; the architect's "Four abstractions" paragraph was drafted after
"In one sentence" and cut on the referee's finding (M8 below); the
section "Lorentz: an open question of the theory" before the literature
(what the operations give, what they do not, where nature measured
gamma, the three routes A, B, C); the check `checks/light_speed.py`;
seven references (CFL 1928, Qian 1992, Nagel 2015, Bailey 1977, Bertozzi
1964, Botermann 2014; the design's FORM.md and the derivation as
repository sources); NUMBERS.md rows. The title and the abstract are
unchanged (the abstract has ten characters of room; a sentence on c would
need the owner's cut elsewhere).

## Referee round 7 (2026-09-21): the c material and the Lorentz section, major revision, applied

Verdict: major revision; nine majors and eleven minors, every one verified
against main at 88d843ef (FORM.md, the map's output, LAW.md, the
derivation's sections 4, 12, 12b, 13, the log's records 186 to 228, the
engine's `_bresenham`), the check re-run byte-identical and the figure
re-rendered. Applied the same day. M1: the isotropy measurement does not
merely bound the grain; by the law's own bond clock (12.3) a moving
laboratory's two-way light clock shows the classical ether's anisotropy
of order beta^2 / 2 (1e-8 at the Earth's orbital speed, annual), which
1e-18 refutes for route (A): rewritten in "Where nature has measured" and
in route (A). M2: "Michelson-Morley null two-way" was the crossing count
of an isotropic crowd at equal density below the rows' pace on the axis,
not a light clock: (iii) rewritten with the apparatus and the condition,
and "a two-way light clock is not null, (vi)". M3: the dispersion's 0.632
against 0.864 is the map's row p = m in label units (Newton's pace one
Link per interval), not p = m c: relabelled in the text and NUMBERS.md.
M4: the muon world J4 is defined and not run: "would read", with the
source. M5: route (C)'s 1 + beta^2 / 3 is the sphere mean of the relative
speed |n - beta| (the mean of the crossing factor 1 - n . beta is 1):
the quantity named, and record 230 no longer cited (not yet in any log;
"the item of 2026-09-21 that ordered section 12c"). M6: "a bound no row
reaches" was false (2072 directions cross one Link per interval; the
(1, 1, 1) row rides the front at every period): rewritten in terms of the
mean pace within 1 / T_d of the inscribed sphere, the vertex's pace
reached by no row's mean pace; caption likewise. M7: "reached by another
road" was not accurate, the Courant condition's necessity being the same
domain-of-dependence argument: the text, "what is not claimed", the
positioning sentence, the check's section 5 and the judgement above say
so, and "the road" is no longer claimed. M8: the "Four abstractions"
paragraph asserted a Noether-type claim the paper does not have (the
split's isometry is not an invariant of a group action; no collision
acts in these worlds) and used six symbols before their definitions: cut.
M9: Bertozzi's speed against kinetic energy is not "predicted
differently" but not reached (the law has no energy of motion, 4.5).
Minors: the proof's missing step v <= |d| / S_1 added; the map's
description of the 2072 as cube diagonals said to be corrected here; the
grain bound "of order", with the fixed two-arm null on headings and the
rotating resonators' cubic pattern; "the crossing rule's factor"; the
1e-15 as the classical identity's check; (ii) "asserted there"; the tie
"for half of the 48"; the angular-momentum clause cut (none is defined
here); the caption's vertices as the six neighbours at the Ports' ends
and the label overlap moved; "beta" written at first use; "the standard
second-order scheme"; NUMBERS.md's rows for J4 and record 230 corrected;
the check's "the mathematician's map" made "the design's map". The
literature coordinates (CFL 1928, Qian 1992, Bailey 1977, Bertozzi 1964,
Botermann 2014, Nagel 2015) confirmed by the referee. Not applied: none.
Two findings go to the Boss: FORM.md section 1's "2072 cube diagonals"
(8 are; 2064 are near ones where isqrt's floor closes a gap below
1 / Q_f), and the Lorentz section's reading that the law's bond clock
predicts a Michelson-Morley signal a moving laboratory does not see.

## The Lorentz decision in the manuscript (2026-09-21, the Boss's message of 04:24Z; records 245 and 249)

The owner decided routes (A) and (B) together (record 249, a Highlights
5.4 line): the law stays the six verbs and states its prediction that a
body's own counter does not slow with speed as a falsifiable row against
the muon in flight; lorentz-v1 is built beside the law under its own
identity as a comparison hypothesis, both run against the same pins, the
paper stating both. Route (C) is closed by section 12c (record 245, PR
#437): the crossing rule's count of a mover through an isotropic crowd at
rest has the sphere mean exactly 1, the owed count and the counter's rate
are the rest ones, the sweep's 1 + beta^2 / 3 is not the rule and the
registered transverse count refutes it, the mover's rate is never below
one half of the rest rate. Applied: the section retitled "Lorentz: what
the law predicts, and the decision taken"; its opening states the
decision; the last paragraph is "The three routes, and the decision"
with route (C) closed on 12c's numbers and the decision (A) and (B) with
the two readings to come; the limits section's cross-reference; the log
bibitem cites 230, 245 and 249 (245 and 249 land on main with the Boss's
next records pull request; 230 is on main since PR #433); the
derivations bibitem names 12c; NUMBERS.md's route-C row replaced by 12c's
three numbers. The verdict on c and the direction "a paper on everything"
are recorded by the Boss (records 253 and 255); no action on the latter. A short referee check on
the change (the same day): pass on substance, every closure claim traced
to 12c; applied its wording fixes (the count's excess odd in the
component; the owed count's mean; the decision named the author's, a
choice and not a derivation's result; the redshift z, the pace v, the
momentum p and the mass m named at first use in the section); its caveat
stands: the citations of records 245 and 249 dangle until the Boss's
records pull request lands, so the manuscript is not merged before it.

## The claim on c a referee cannot call taken (2026-09-21, the owner's request after the verdict; superseded by referee round 8 below: the text described here was rewritten, Proposition 2 became Remark 1, the universal claim on lattice waves and the "2e4 times" comparison were withdrawn)

The owner (translated): "try something a referee will not say you took
or derived from elsewhere; a founded claim". The candidate, written into
the model section after the pace paragraph as Proposition 2 ("The pace
is the direction's") with its consequence, a bullet in "What is new" and
a sentence in the positioning: the pace of a row depends on its
direction alone, at every phase rate up to the alias bound, so the
model's light has one speed at every wavelength (no dispersion), where
every discretised wave equation and lattice Boltzmann model is dispersive
with a band edge. Consequences with numbers (`checks/light_speed.txt`
section 6): the Link is bounded only by the shortest wavelength seen
(LHAASO's 1.4 PeV photon: a <= 7.7e-22 m under the pair form, 4.4e-22 m
under the integer form) and by nothing of the time-of-flight tests; one
GRB photon (GRB 090510, 31 GeV within 0.83 s at z = 0.903) bounds a
lattice wave's Link below 3.6e-26 m, 2e4 times lower; the prediction: no
energy dependence of c at any precision (as in special relativity), the
lattice left only in the frequency-independent anisotropy; one measured
energy dependence refutes the flight. Stated as a property of the
definitions (the row a walker on a digital line, not a wave), not a
limit: referee round 3 withdrew a "plane-wave limit" built on the same
fact, and this entry claims the consequence, not a limit. Referee round
8 before it stays.

## Referee round 8 (2026-09-21): the no-dispersion claim, major revision, applied

Verdict: major revision, twelve findings, every one verified (the
archived walk and collision, the scheme's dispersion relation recomputed
in closed form, the literature numbers recomputed). Applied the same
day. (1) The universal "every lattice wave equation with a Link above
1e-25 m is already refuted" was false: the same second-order scheme is
exactly dispersionless on the cube diagonal at this Courant number, and
a fourth-order scheme's bound from the same photon is 8e-22 m, above the
LHAASO bound; the text now bounds "the standard second-order scheme on
an axis" and gives the fourth-order number, and says a lattice wave
obeys both bounds. (2) "Energy" is undefined in the model: the reading
of a photon of energy E as a family turning E tau / h per interval is
now stated and labelled assumed, and the prediction "no energy
dependence" carries it. (3) Proposition 2 was a definition's pointer:
demoted to Remark 1, widened to every rule of the interval (the archived
collision table reads no phase), and the fact named for what it is, the
pure-shift case of a lattice automaton (Meyer 1996), a ballistic walker
with a passenger phase; the claim is the pair with Proposition 1
(isotropic within 1 / T_d and dispersion-free in every direction while
the carried phase interferes), which no local linear wave scheme on the
lattice can be, with the one-line reason (a trigonometric polynomial
against c |k|). (4) The integer form's bound is lambda / sqrt 2 (two
Links span sqrt 2 a on a cube diagonal's line), 6.3e-22 m, not lambda /
2. (5) The wavelength's symbol clashed with Bell's lambda: the photon's
wavelength is now Lambda; v_g, a, omega, k named at first use. (6) The
cosmology named (H_0 = 71, Omega_m = 0.27, the comoving distance 9.47e25
m, Abdo et al. 2009), the weighting's direction stated; the LHAASO
bound dated ("moves with the record"; the referee notes later LHAASO
photons to 2.5 PeV, to be verified against the source before
submission). (7) "This model's bound" corrected: the shortest-wavelength
bound is every lattice's; the "2e4 times" comparison dropped; the
positioning sentence restricted to the discretised wave equation and
the cited three-dimensional automata (no claim about lattice Boltzmann
carrying light); "the flight as defined". The referee's answer to the
owner's question, recorded: the bare no-dispersion fact can be
dismissed as the trivial shift; the pair with the isotropy cannot, and
its weakest point is its price, no wave on the lattice and the energy
entering by an assumed reading. The "What is new" bullet states the pair
and the price. The re-verification at eef31b7c
(the same referee): minor, eight residuals, applied: the interval's
length written Delta t (tau is the age), the reading as the fraction
E Delta t / h of the circle with the alias bound E Delta t / h < 1/2;
the reason in Remark 1 restated as a polynomial equation in
e^{i omega Delta t} and e^{i k_j a} (omega(k) periodic up to 2 pi /
Delta t); the automata cited by key; the redshift z named; the
fourth-order term marked an order of magnitude; NUMBERS.md's symbol
Lambda; this entry's predecessor marked superseded; the birth added to
Remark 1's rule list.

## One paper, on the general formula (DECIDED by the owner, 2026-09-21, about 05:02Z)

The owner, after the assessment of the record (his words, translated):
"No, no, we take one paper, a paper on the general formula, that is it."
So: one manuscript on the map **F** of the integer torus (the state vector,
the six verbs, the click as the one threshold), every result as its
consequence, and the click-model manuscript folded in as the measurement
chapter; no separate submission of the click-model paper. The directory
`paper/click_model` was renamed `paper/general_formula` with its
consumers (`paper/README.md`, the manuscript's own paths; the log's
historical mentions untouched).

The structure: Part I, the formula (DERIVATIONS_BEAM.md section 0 and 9.1,
with the two precisions of section 0: the rates of the feedback block are
bilinear, and the threshold read out is one comparison against the norm
of the linear evaluation). Part II, what follows from the formula: one
table in four rows, each entry with its derivation's section and its
registered check or its pin: REACHED (Newton, Coulomb, Gauss and the
third law, 3.1 to 3.4, series C; Doppler on the axis under the crossing
rule, 2.2, record 158; c as the largest uniform pace, this paper's
Proposition 1; Born as the lattice Gleason and Tsirelson as a limit, 6.2
and 6.5, series L; Young's spacing in the limit of every direction, 7.1,
record 156; Bohr's condition and radii in form, 7.2, series H; Poisson
and the retarded delay field, the first-order redshift, Newton's retarded
geodesics, 5.1 to 5.3, series E; the information cost and the boundary,
6.1 and 6.3); INPUT, NOT DERIVED (G as the width S, 3.3; the masses M,
PREDICTIONS 26; the family table, record 189); NOT REACHED (Einstein's
equation, 5.5 and 5.6; E = m c^2 and velocity addition, 4.5; Bohr's
energies and the Rydberg lines, 7.3; the harmonic constants of the click,
6.5); DIFFERENT LAW, stated as a falsifiable row (Lorentz: the counter
at 1, the dispersion, the push one factor short, decision A and B; the
transverse Doppler exactly 1, 2.3; the second-order redshift, 5.2). Then
the derivation sections of Part II written one by one from
DERIVATIONS_BEAM with the register's checks, each after a hostile
referee round. Part III, the click model, the measurement chapter: the
present sections unchanged in content. Part IV, the pace (Proposition 1,
Remark 1, the octahedron), Lorentz and the decision, what is not reached,
the literature, the reproducibility.

The conditions before the results are written as results, per the main
course: the three builds and form B on main (the code the formula,
record 221 (2)); each reached formula with its confirming run cited from
the register (form B's cone, the thrown orbit, J4 and 12c's probe are
pins, not runs); the derivation's sections 12c to 16 on main; a referee
round per section. Until then a section states its formula with its
source and its check's status. The click chapter's numbers are re-run
over the 48 worlds after the fraction-free and wheel re-pin, as planned.
Asked of the Boss: the record and the 5.4 line; the derivation
mathematician informed; the builds' and runs' timeline; the re-pin's
timing. The title is proposed to the owner with the skeleton.

## Referee round 9 (2026-09-21): the one paper's frame, major revision, applied

The frame (the title, the abstract, the introduction, Part I "The law",
Part II "The table", the part markers) went to a hostile referee before
its first commit. Verdict: major revision, twenty-four findings, every
one verified against the derivation's verdict tables, HIGHLIGHTS 5.7, the
register and the code; all applied the same day. The substance: (1)
Born's rule was claimed three incompatible ways (derived in the abstract,
put in in Part I, disclaimed in Part III): the abstract now says "the
click's weight forced to a positive quadratic form of power 2", the
table's row adds "not reached from the algebra: the harmonic constants".
(2) to (5), (11), (12) four "reached" rows had no confirming run of the
law on the archived code (Doppler under the crossing rule, decided and
not built; Young's fringes in the weights and a host map, the wheel not
built; Bohr's j = 4.01 the derivation's arithmetic with no closing
orbit; the geodesics with series D closing none; the redshift's
weak-field run pinned): each row now says pin or names the true check,
and the abstract separates "against recorded runs" from "in the limit
only, their runs pinned". (6), (7) Part I described form B's drive and
the wheel W as the law run: now main's per-axis drive saturating at one
Link per interval above c, form B and W = 4096 stated as decided and not
built. (8) the isotropy row hid the bond clock's refutation: now a
different-law row, named in the abstract. (9) the bending of light given
its own row; Einstein's check cell empty. (10) G "reached in form, with
the width an input". (13) the click chapter's sentences that said "this
paper" where the one-paper frame made them false ("of this chapter",
"series L"; the hypotheses section as the chapter's history where an
item became a table row; the roadmap rewritten; "In one sentence" tied
to Part I's six operations). (14) the introduction's roadmap corrected
(the pace is in Part III; the table's rows to be written out one by one,
no promise of sections that do not exist). (15) the legend maps the
table's statuses onto the four labels and adds "new"; the c row "the
bound proved; the value assumed". (16) the register, derivations and
predictions bibitems widened to what the table cites; the caption names
the log's records. (17), (18) the six operations and the inputs cited to
HIGHLIGHTS 5.7 with the quotation marked, "or a rounding declared at
load", the fan's grain G and the wheel's rounding added, "no fourth"
dropped. (19) the balance (I5) with the cancelled and the free/paid
distinction. (20) "the one read-out that deletes". (21) the wall's
letter b (the direction keeps d), the pair form's rate nu in Part I, the
width S told from the CHSH S. (22) Gauss's check as the square's
half-widths; the transverse Doppler's check a host script. (23) the
table's widths 1.5 / 1.25 / 1.1 / 2.25 in at 3 pt. (24) the title
without "piecewise-linear" (the derivation's own precision: bilinear
rates in the bodies); British spelling throughout. The referee's closing
line, recorded: the frame is defensible in principle; the measurement
chapter is the only part yet confirmed end to end, and the table must say
so row by row, which it now does.

## The second wave (2026-09-21): the symmetries, the table's new rows, the confrontation table, Lorentz on section 17

Read from main at 2f6a44c5: records 259 to 265 (the owner: "maybe
Lorentz is not needed here"; "everything in one paper"; the GO for one
paper on the big formula broken into the small formulas; "not a paper
about a simulator"; the three failures under one logic), section 16
(the numbers of nature: c reached; G the width, a choice of units, no
rule for the hierarchy in sight; the smallest mass per kind a theorem of
the charge line, the floors 1 and 3, the counts inputs), section 17 (the
theorem of covariant readings: the linear block's limit carries
Lorentz's symmetry; a body inherits it as far as its four readings are
covariant; the covariant forms within the six verbs; E = m c^2 forced,
the muon 70.9 and 125.2; covariant-readings-v1 on paper, not built), and
NATURE.md (the confrontation register, seventeen rows, 3 PASS, 9 FAIL, 2
BOUND, 3 NOT YET). Written: the paragraph "The symmetries" in Part I
(the translations, the 48 with the hand, Z_N, the families; a boost not
among the 48, record 231; conserved up to the lattice, record 225); the
table's rows for entropy (14), the growing wall (15), the smallest mass
per kind (16.2 (d)), G with 16.2 (e), Heisenberg's spread (NATURE row
10, A10), the Lorentz row with the covariant readings; the section "The
confrontation with nature" with the seventeen rows; the Lorentz section
rewritten on section 17 (the theorem, built on Newton, tried on Lorentz,
the covariant readings, the decision: A and B as recorded in 249, the
derivation's hypothesis named, the choice between the root and the
readings recorded as the program's next decision, since the owner's word
on replacing B is not yet in the log). The c row waits for series Q's
register entry (263: 290 of 290 face clicks at the derived interval).
Referee round 10 on this wave before it stays.

## Referee round 10 (2026-09-21): the second wave, major revision, applied

Twenty-four findings, all verified; the numbers of the seventeen rows,
the tally, the muon's 70.9 and 125.2, the floors, the hierarchy and the
48 checked out; what did not: (1) the sources cited (NATURE.md, sections
16 and 17, records 259 to 265) were not on the branch's tree: main
merged again (a6a18c2d, 970a81d5), "at the tree of this paper" replaced
by the register's own commit 88d843ef; (2) to (4) the Lorentz section's
opening and decision paragraph had written the recommended replacement
of B as if decided and attributed the recommendation to the derivation:
now the decided hypothesis is the seventh operation (record 249), the
covariant readings the derivation's second candidate, the program's
recommendation cited (records 259, 260, 264), the choice pending; the
root's content stated as the record has it (the clock and the
contraction by declaration, no energy of motion); (5), (6) the table and
the section agree: three of the four readings in the lattice's frame,
the E = m c^2 row "not reached as declared; reached under the covariant
readings"; the abstract carries the hypothesis and the confrontation's
tally; (7) series D not cited as confirming G M / r^2; (8), (9) "only
under them" deleted, the invariant "kept to 1e-12 in a host integration,
the exact closure open", the contraction "by Lorentz's 1904 argument,
not integrated"; (10) the one set's qualifier (eight worlds with another
clock pair, no verdict depending on it); (11), (12) seven published
sources added to the bibliography (Sinha 2010, Planck 2018, Riess 1998,
Perlmutter 1999, AME2020, Gonzalez 2021, Nairz 2002), the Sorkin
parameter attributed to Sinha's measurement, the register's "to verify
against the source" carried; (13), (14) rows 4a and 5b: the covariant
readings' entries marked as this paper's additions, "nine orders", the
lattice-frame qualifier, the register's own route wording noted; (15)
row 3's crowds named, the two pinned failures counted as NOT YET for the
run; (16) the growing-wall row owns nature's q_0 as not reached and
names G2's re-read at rest a host reading; (17) to (19) the quark
design's quarks, alpha and alpha_G named with alpha_G = alpha / rho_p^2,
w, theta and Lambda named; (20) the symmetries paragraph: the three ties
named, the interval's translation, the families with their columns,
"angular momentum only up to the lattice; no Noether theorem for the map
claimed"; (21) the wave-equation hedge restored; (22) E, E_0, m, nu
named, gamma = 29.33 once, Q_f written Q in the register; (23) the
lattice-frame qualifier in "Tried on Lorentz", route C's closure in one
clause; (24) the two role words of the click chapter replaced. The
abstract re-fitted under 1920 characters.

## The Lorentz decision closed (2026-09-21, record 270): the covariant readings in place of the seventh operation

The owner told the paper session "it is no longer A plus B, it is
closed"; the derivation mathematician's note (his branch at 129fbd87,
17.5 and 18.1) cites record 270: covariant-readings-v1 is built beside
the law in place of lorentz-v1; main's log at 3ae2ac92 ends at 266, so
the record lands with the Boss's next pull request. Applied: the Lorentz
section's opening and "The decision" (the law kept with its prediction
as a row that can fail; the comparison hypothesis first the root, now
the covariant readings, decided in its place; both run against the same
pins; route C closed), the table's Lorentz and E = m c^2 rows ("the
comparison hypothesis decided for the build, on paper, not built"), row
5b's parenthetical, the abstract ("the hypothesis built beside it"), the
log bibitem (270). The derivation's sections 19 (the masses generically)
and 20 (the periodic universe) are new on his branch and not yet read
for the table; 13.2 (a) corrected per record 262; 12c.1 names its two
sphere means. The referee's check on this
change (the same agent, read-only): minor, five items, applied: the
derivation's grounds detached from the decision's sentence; the pins of
18.1 named; "the first decision: A and B" in the log bibitem; row 4a
"decided for the build" and the isotropy row's clause for uniformity; a
caveat in the manuscript's submission note that record 270 and its
decision line are not yet in the archive's log (PLAN.md is not read by a
referee), and 18.1 added to the derivations bibitem.

## Referee round 11 (2026-09-21): the Newton and Coulomb section, major revision, applied

The first written-out row group of Part II ("Newton and Coulomb from the
bilinear coupling", from the derivation's section 3 and series C).
Eighteen findings, every registered number confirmed and every statement
around them tightened: Newton's equation displayed in the plane form
beside the space form (the registered check is the plane's 1 / r, the
1 / r^2 unrun); the outrunning body named a test fixture, not a
registered world; six operations of three kinds, not "five"; the release
as a count against a wall with the carry; the release rate given its own
symbol eta = n / d (nu stays the phase rate) and named, the table's G row
in the same symbol; Gauss's conditions stated (a free unit, no periodic
axis crossing the surface, no absorbing reader, within the lifetime) and
the periodic axis's home-and-release mechanism that makes q = 6 x 2^17;
the world's two sources of the third-law world and the probes' contents
per radius; the fingerprint whose integers are quoted named, the unit-
vector re-read's factor 64; the register's flow defined as the label
flow over Q_f; the misses of item 5 attributed per criterion (the flow
at 12, 16, 20; the count at 16 and in the ripple; the ring counts 68,
112, 112); the equivalence identity for m = 4, 16 against the probe of
1; the speed formula per interval for a clock owing nothing, with |p_a|;
the front's arrival as the flight table's first age; u_d, S, theta, e,
epsilon_0, m_p named, Huxley 2003 cited; which body owns which
coefficient; the accumulator on the branch labelled; the delay-field
pointer to the table's row; "in form, the ratio exact at r = 12".

## Referee round 12 (2026-09-21): the delay field, the lattice Gleason and the click's two questions, major revision, applied

Three pieces read together: the delay-field section (the derivation's
section 5, series E and K), the lattice Gleason (6.5) and the paragraph
on the owner's two hypotheses. Eighteen findings, all applied. Symbols:
the clock pair n_c / d_c, the dwell tau_L (delta was the map's error
term), the presence Pi (P is the phase wall), the age moment in
calligraphic A (A was the click's constant), C_a and C_Sigma for the
redshift fit's two constants, Delta for the meeting key's offset and
calligraphic K for the general flux (K is the coupling); the redshift
fit's second list and its C = 33.12 quoted from the register, not from
memory. The meeting key named with the registered centroids; G2's two
readings named with their world. Gleason's title without "unique"
(uniqueness is up to the odd constants c_j, which are not reached);
hypothesis (b) stated as a hypothesis on the reading, not as a seventh
operation; the two-slit bands attributed to record 156's host map,
"consistent with c_j = 0 for j not 1, no bound stated, pinned by no run".
The table: the click-weight row, the redshift row ("named, not pinned"),
Einstein's row with "no cosmological term", the intro sentence. Part I's
read-out paragraph: where the Born rule enters, "forced in form, free in
its constants"; the "what is not claimed" Born bullet in the same words.
The two hypotheses moved out of the history section into a new paragraph
"Two questions of the click, open", placed before it: the detector
question with nothing claimed, the click as a choice among futures with
the record's injectivity "given the apparatus's record (the bijection
theorem)" and the entropy of section 14 named as "the only computed
quantity near that reading". Two bibitems: Gleason 1957, Jordan, von
Neumann and Wigner 1935. Not applied: nothing; the round closed with no
residual.

## The owner's two hypotheses on the click (2026-09-21, about 05:50Z to 06:00Z), what enters and what stays out

The owner (translated): "one hypothesis, entirely a hypothesis: what a
detector is and why one cannot touch the GameBoard; whether the Sun
clicks at all, or clicks arise only on Earth"; then, correcting himself:
"not only a living being makes a click; I would say the clicks are
somehow connected to life, that clicks arise from life; a hypothesis to
be checked, and I am not going into it now". And: "beyond the click all
possibilities exist, the click chooses one, and the number of paths to
the future changes; put it in the paper as a hypothesis and nothing
else; the paper is formulas, how we reached them, and the proofs, as is
customary". In the manuscript (the hypotheses section of the click
chapter, under referee round 12): the law's two kinds of reading and the
open question which physical systems are detectors, with nothing
claimed; and the click as a choice among futures as a hypothesis, the
computed quantity behind it named (the derivation's section 14). Not in
the manuscript, by the owner's word: "clicks arise from life" (no
formula, no test in the model; kept here as his hypothesis for the
record, to be put to the Boss).

## Sources announced for later citation (2026-09-21, from the architect and the derivation mathematician; not yet on main)

BEAM_LAW note 47, the crowd audit (record 276; the architect's branch at
5bd58241): one table of the 23 rules in force with what each reads of its
own record and of the crowd, 13 reading the crowd and 10 only their own
record (the walk, the escape, the click's choice, the re-emission, the
rotation, the turn, the birth, the release, the border lifetime, the
decay's timing), with the hypotheses under which the crowd would enter
(decay-by-crowd-v1, covariant-readings-v1, the meeting): the source for
one sentence of Part I's "two blocks" (which rules read the crowd and
which only their record), cited by title until the note numbers are
reconciled with the click branch's. BEAM_LAW notes 43 and 44 (the bound
set's mass; the parity of the bipartite lattice): the sources for the
masses row with 19.1 and 19.3. Sections 18 to 20 with 16.2 (f), (g),
18.2's addendum and 19.5: the rows drafted in the scratchpad enter when
they are on main and merged into the branch.

## The title decided, the closure declared (2026-09-21, the Boss's consolidated message of about 06:00Z; records 272 to 275, in the Boss's open pull request)

The owner's decision (record 275, translated: "3, only that it explains
how 24 follows from the group"): the title is "Universe24: a local
integer law of nature and what follows from it"; the descriptive line
became the abstract's first sentence in its short form. The condition
is met by Theorem th:group in Part I's symmetries paragraph, with its
proof in one paragraph: the maps of the six Ports keeping opposite Ports
opposite are the signed permutations of the three axes, 2^3 x 3! = 48
(the hyperoctahedral group B_3, record 226, the derivation's 16.3); the
determinant is onto {+1, -1}, its kernel the 24 rotations of the cube
(the symmetric group on the four body diagonals), its other coset the 24
reflections; the hand is that determinant on a row (BEAM_LAW's parity
passage: the image differs under exactly the 24 improper elements). What
24 is exactly: the orientation-preserving symmetries of the octahedron
of the six Ports, the rotation group of the cube. No further title
candidates.

The closure (record 275, "we are closed on everything"): the paper
carries the quarks by the design's pins (QUARKS.md on the tree; series R
not yet), the masses (section 19, notes 43 and 44), every formula with
how and why it is derived and its registered run beside it, and names
the GameBoard as the instrument of every table entry and not the
subject (one sentence in the Method paragraph). A FAIL row stays FAIL.

## Wave 3 applied (2026-09-21, after the merge of main at d870fedb)

The drafted rows entered once their sources were on the tree: the
masses row (19.1 to 19.5; notes 43, 44; the quarks design's pins; the
colour sentence "in the law the quarks compose the nucleons' charge and
binding, not their mass", colour-v1 a hypothesis to be tried, record 270
(1)); the weak forms row (18.2 with its addendum, decay-by-crowd-v1
pinned); the strong ratio row (18.3: 4.0, 6.0 with the diagonals,
against 12.72); the periodic universe row (20.2, 20.3: open, a
convention; the deciding number L / (2 chi_rec) measured above 0.97,
Planck 2015 XVIII); the three-failures paragraph after the confrontation
table (18.5). The c row gains series Q (merged at 3be07117: 290 of 290
face clicks at the derived interval, Node and face; the pace 0.5718 to
0.5893, mean 0.5810). Part I's two-blocks paragraph gains the crowd
audit's sentence (note 47: 23 rules, 13 read the crowd, 10 only their
own record). The confrontation section: the detector rule in one
sentence (the register's rules; the owner's record 281), eighteen rows at
d1fe2712 (three PASS, ten FAIL of which two pinned and one a refutation
of a declared input, two BOUND, three NOT YET), row 8c (the massless
neutrino, refuted; PDG 2024 and KATRIN 2022 as the register cites them)
and row 3b, the far lamp's brightness through a detector (records 280
and 282; the note docs/designs/far_lamp/BRIGHTNESS.md with its pull
request open): q_eff = +1 from the luminosity distance ln(1 + z)
sqrt(1 + z) (checked here: the z^2 coefficient vanishes, so (1 - q) / 2
= 0), the shape residual 0.339 mag rms against flat Lambda-CDM (Milne
0.055), the stretch 1 + z passing exactly against (1 + z)^(0.97 +- 0.10)
(Blondin 2008), the surface brightness (1 + z)^-1 against Tolman's
(1 + z)^-4. Row 3b is the one place this text cites a source not on
its tree; it is marked as this paper's addition, cited by title, and
named in the submission caveat with the instruction to re-read its
numbers at the merge (the rule of referee round 10 kept visible, not
broken silently). The Lorentz section's host integration is now called
what the derivation's corrected 17.1 calls it: a floating-point
consistency check, not the discrete proof.

## Referee round 13 (2026-09-21): the title, the theorem of the 24, wave 3 and the far lamp, major revision, applied

Sixteen findings, all applied. MAJOR: the theorem's last sentence and
its proof claimed the hand as "the one datum" telling the 24 from the
24 and attributed the parity reading to "the derivation's" worlds;
BEAM_LAW's parity passage (series P's worlds of tests/test_hand.py)
reads exactly the 24 improper elements only on worlds with an axis, an
axial vector tells them apart too, and a hand without an axis is
mirror-equal under all 48: the statement now says "the one pseudoscalar
column ... as does an axial vector", the proof names series P and the
axis. MINOR: the faithfulness of the rotations' action on the four body
diagonals shown in one clause (the identity and the central inversion
alone fix all four, the inversion improper); Lambda-CDM written in words
(Lambda is the wavelength here); the symbols of row 3b and the periodic
row renamed (r for the distance, L_lamp, L_box; H and c_0 named at first
use in the expansion row); the neutrino family in typewriter (nu is the
turn rate); q_0 = -0.53 +- 0.01 as in row 3, Riess and Perlmutter for the
discovery only; the one clause on why the power of (1 + z) is one (each
click delivers the row's birth content, 6.4; read at the arrival rate
the power would be two and q_eff = 0, this paper's remark); the caveat
names the two numbers of row 3b unverified against any file of the tree
(0.339 / 0.055 mag rms; 0.97 +- 0.10) and adds records 271, 273 and 276;
row 3 described as the thrown stars' Doppler z; the weak forms row in
the addendum's words (the rung the family's own b / W, the wheel
advanced by the arriving rows, failing only in an empty world); the
masses row's pins attributed to 19.4 and the seven worlds' own, colour-
v1 named for confinement and failing the vector and local tests; the
register cited by its base 88d843ef with row 8c added at d1fe2712; the
preamble's rule with its exception (a pin marked so); the abstract's
mass "in form". Verified without change by the referee: the 48 / 24 / 24
and record 226; note 47's 23 / 13 / 10; series Q's numbers; the tally;
row 8c; the strong ratio; the periodic row; the host check's 10^-12;
the column counts; the four theorems of the measurement chapter.

## The far lamp on the tree, the records on the tree (2026-09-21, after the merge of main at 01bb782a)

PR #455 (records 267 to 282 and the 5.4 lines) and PR #464 (the far
lamp's note BRIGHTNESS.md with far_lamp_map.out, DARK_SECTOR.md, the
register's rows 11a to 11c) are on main and merged into the branch. The
paper's row 3b is replaced by the register's own rows 11a (q_eff = +1,
FAIL pinned), 11b (the stretch 1 + z, PASS pinned: 400 rows over 400
intervals arrive over 1452 at 300 Links, 3.639 against 3.629) and 11c
(the surface brightness (1 + z)^-1 against Tolman's -4, FAIL pinned; at
z = 1 the ratio 0.500 against 0.062); the two numbers previously marked
unverified (0.339 / 0.055 mag rms; 0.97 +- 0.10) are now read from the
note's lines 114, 116 and 146 and the register, Blondin 2008 and Lubin
and Sandage 2001 carried with the register's "to verify" flag (eight
values now). The register: twenty-one rows, four PASS, twelve FAIL (four
pinned, one a refutation of a declared input), two BOUND, three NOT YET.
The submission caveat reduces to one sentence: every source cited is on
the tree; the far lamp's rows rest on a pin, series R is not registered.
The log bibitem cites records 270 to 282 by number, no longer "in the
Boss's open pull request". Abstract 1880 characters.

## Referee round 14 (2026-09-21): the far lamp's rows 11a to 11c, minor revision, applied

Nine findings, all applied: the log bibitem's records corrected (281 is
the owner's rule, not the far lamp; 270 "in place of the build of
lorentz-v1"; 271 the addendum ordered, 278 the addendum delivered); nine
values marked "to verify" (Gonzalez 2021 was undercounted before this
round); rows 11a to 11c added at 8b13ceeb, merged at 01bb782a; row 11a's
parenthetical no longer contradicts its own row ("were the content to
follow the frequency in flight, the power would be two and q_eff = 0, a
rule 6.4 finds not among the six"); the stretch exponent renamed beta_s
(b is the rung); the post-table sentence separates the Hubble diagram's
widening gap (11a) from the surface brightness's three powers (11c);
row 5b marked "this paper's addition" as row 4a is. Verified without
change: every number of rows 11a to 11c against NATURE.md and
BRIGHTNESS.md (0.339 / 0.055; 3.639 / 3.629; 1452; 0.500 / 0.062; "no
such rule among the six"); the tally; the caveat's series R; the 5.4
lines of records 277 and 281.

## Series R on the tree (2026-09-21, after the merge of main at aa4cabf0)

The quarks' run (PR #463, EXPERIMENTS entry R, the seven worlds of
examples/events/quarks/ with expectations.json written before the run,
tools/quarks_readings.py, 16 derive-and-compare tests) is on main and
merged. The masses row's check column cites it: the push on every body
the design's integer exactly; the lines hold 3000 intervals, the
triangle and the rectangle shear (27 and 176 against the toy's 25 and
161); the read mass the exact sum in every world (20, 25, 20, 45, 45,
20, 1836); the kicked u leaves at tick 63 (the pin 70 to 90, outside by
seven, reported and not moved) and its pair breaks at about 1190 (the
pin "a bound pair", outside): the law binds and does not confine. The
caveat's "series R not registered" sentence is gone; the register
bibitem adds R, the log bibitem record 279. Records 283 to 288 (the dark
sector's three routes refuted, the far system read before any click
refuted) are on the tree and not cited: the paper carries no dark-sector
claim, and the register's row for it is not a reading.

## Referee round 15 (2026-09-21): the series R cell, minor revision, applied

Eight findings, all applied: the log bibitem cited record 279 for "the
quarks' six verdicts", which it is not (no log record carries the run's
verdicts; the register's entry R does), now records 267, 273 and 275
(the design delivered, the run ordered and registered); the dressed
world's one accumulator unit qualifies "exactly"; "the toy" named as the
design's integer replay; the kicked u "leaves through the face with its
2/3 e" and "the pair it leaves behind breaks"; 19.4's pins reported as
met (a chain and never a triangle; m_n - m_p the held difference, 25 - 20
units; the F pin is not read by the register); LaTeX quotes; the
compositions spaced as the source writes them. Verified: every number of
the cell against the register's entry R and the worlds' README.

## The crossing rule on the tree (2026-09-21, after the merge of main at 562fb736 and a9acbd67)

BEAM_LAW note 48 (PR #468): the crossing rule is built; the key doppler,
the grain G, weighted_flow, flux_pair, frame_momentum, the doppler worlds
and tests/test_doppler.py are deleted, note 38 a tombstone. The paper
cited none of the deleted names (checked: no hit for doppler as a key,
weighted flow, flux pair, frame momentum, note 38, the grain G). Two
rows change: the receiver's Doppler from "pin, decided and not built" to
"reached under the crossing rule, built", with the rule's counts (toward
k + 55/32 per k intervals, 45 in 32 and 58 in 48; away 19 and 38; 183
and 311 over a period exact; c = 32/55) and the G2 run under the rule
still pinned, not made; the transverse Doppler's check names the rule's
transverse stream at exactly the rest rate (32 in 32). The delay-field
section's "a key since deleted" was already right. Records 274 to 289
(PR #470) are on the tree; 289 is the closure record. The beamlaw
bibitem adds note 48.

## Referee round 16 (2026-09-21): the Doppler rows under note 48, applied

Seven findings, all applied: no pin exists for the G2 run under the rule
(EXPERIMENTS: the pinning is laid on that session), so the cell says
"not yet made, its expectations to be pinned first"; the derivation's
2.7 on the tree still reads "on main not reached" (written before the
build), stated in the row and reported to the Boss for the derivation's
own fix; the streams are record 151's, the counts record 158's design,
the pins the rule's tests; "built" without "on the archived code" until
the archive's version is confirmed; note 48's own caveat carried (a
reader faster than one Link per two intervals counted, not proved;
exact over whole Links, within one row otherwise); the period named (32
Links at k = 4, 8); the bibitem's gloss left as a gloss.

## The dark sector section (2026-09-21, the owner's word, record 298 pending on main; the physicist's structure approved by the owner, relayed by the Boss at about 08:10Z)

The owner (translated): "Yes, you can pass it to him for the paper: only
what we tried to do there with dark matter. And you say also a detector
does not help, a limited number of clicks does not help, nothing; at the
moment there is no explanation for it." One short section, a sharp
negative result with the missing content located, never an explanation
of dark matter: (a) the statement with its one-line reason (Gauss exact,
the push bilinear and homogeneous of degree 1 in the rows, every
division keeps its remainder: no rule of the six strengthens a weak
field, none gives an acceleration below which the field departs from
1 / r^2); (b) the falsifiable rows in one font (11a FAIL, 11b PASS, 11c
FAIL, the rotation curve Keplerian with the visible content FAIL as
stated, not a register row); (c) one table of six routes with the sign
and the shape each gives and what refutes it (the detector's shift;
the finite clicks and the read-before-any-click; the short periodic
dimension; S derived; the rounding floor; the fixed computation at the
edge); (d) where the missing content sits (an input family with a
charge column 0 and no lamp; dark energy nowhere; the Bullet Cluster's
bending needs unseen content); (e) the open question in one line (a
root of the state and a declared a_0, not one of the six). Placed after
the delay field, before the lattice Gleason. Sources on the tree:
DARK_SECTOR.md, S_AND_A0.md (sections A to E), BRIGHTNESS.md, NATURE
rows 11a to 11c; published: Milgrom 1983, McGaugh 2012, McGaugh, Lelli
and Schombert 2016, Clowe 2006, Hofmann and Muller 2018. Not written,
by the Boss's instruction: "the model explains dark matter", "no dark
energy is needed".

## Referee round 17 (2026-09-21): the dark sector section, major revision, applied

Twelve findings, all applied. MAJOR: the opening was called a theorem
and said "Newton's exactly"; the sources reach Newton in the shell mean
with Gauss exact, and the claim that no rule of the six strengthens a
weak field is argued in the notes, not proved as a theorem: now "The
statement, with its one-line reason", "Newton's in the shell mean, with
Gauss's law exact", the push's homogeneity named as a reading of its
form, the gravity column's divisor 1 and the charge column's remainder
kept by the accumulator, and "as the notes argue and no source proves
as a theorem". MINOR: the Doppler departures are parts in 10^4 of the
shift, not 10^6 (the note's own arithmetic slip, reported to the Boss);
the slab's exponents quoted in full (-0.7 to -1.0 against -1.8 to
-2.1); the caption separates the law's numbers (the host map's) from
nature's pins; n and beta named at first use; the slab's thickness
written ell_slab (ell_p reads as the Planck length); K_c tied to the
derivation's section 13 constant; alpha_G named as nature's coupling of
the proton, not redefined; the planets' bound "of order a part in 10^5"
(the 1 m/s precision unverified in the note); the slope "about 4" with
McGaugh 2012 and Lelli 2019 both cited; the open question's logic (a
root fails the vector test, so it enters outside the law); the budget
reading S = K_budget / 26 listed with what refutes it, the factors 900
and 2800 both; the fixed-computation row's three forms labelled with
their three refutations; "a finite number of clicks" dropped (no such
route in the note); the rotation curve "this paper's own reading, no
register row"; "in one list".

## The owner's direction: the derivation record per formula (2026-09-21, about 08:05Z)

The owner (translated): "For every formula you reach, you also write how
we reached it: by the pin method, then from the limit in the simulator,
then in the simulator what the method was by which we derived it, and
see that it does not depend on the formula itself. All the formulas of
all the greats, of course." Applied as: three sentences in the Method
paragraph (the three steps and the independence), and an appendix
"How every formula was reached" before the Reproducibility section: an
opening paragraph (the pin from the closed form alone, committed before
the run; the limit with the order and the error term where stated; the
run of a world that declares families, grain and initial state and no
formula, under the architecture's contract; the independence structural;
the one caveat where the rule is the closed form, the flight table) and
two tables of the derivation map's rows (the field, gravity, the
expansion, the masses; the click, the information, the body in motion),
five columns: the formula, the operations and the premise, the limit
and the closed form, the pin before the run, the run and its reading
with the status. Referee round 18 pending on it.

## Referee round 18 (2026-09-21): the derivation record, major revision, applied

Thirteen findings, seven major, all applied; the round did exactly what
the owner asked the appendix to show. (a) The engine is not free of
every classical formula: the flight table T_d is the rule itself, and
the phase circle's cosine table (cos(2 pi d / P) rounded to 1 / 256,
computed at load as immutable law data) is the rotation of Part III;
both caveats now stated, "no classical formula" dropped; the collision
table generated from its class rule holds none. (b) The pin column
carried post-run readings on ten rows (the third law's momenta,
Newton's flux and rings, Poisson's 36.1 and 41.5, the plane wave's
89.40, the bending's 0.000, Bohr's j = 4.01, the wall's re-read, the
information cost, the entropy, the weak forms' readings, the Gleason
window): every row now carries the register's expectation from before
the run in the pin column and the reading in the reading column, or
says "no pin; a host reading". (c) The labels reduced to the four with
the caption's rule (a pin without its run, or a number read after the
run, is assumed or open, never measured); Doppler assumed until the G2
run under the rule. (d) Newton: the ring means outside the design's
+-10 percent at r = 12, 16, 20, reported. (e) The redshift: the 15
percent criterion missed at three radii, open; the shells 6 to 14. (f)
The wall: -0.108 under a key since deleted, inside Milne's +-0.25,
nature's -0.53 FAIL, the rms 0.0044 a host reading with no run, the
form assumed until run. (g) The tables' widths reduced to fit 6.5 in
(6.18 in with 2 pt columns). (h) chi_rec named; d unbolded; the
expectation "file or the register's paragraph"; the Gleason window
named as the intersection and the splitter's conservation restored; the
far lamp's verdicts on the pins stated; "the push in space unrun".

The verification pass on the corrected appendix (the same day): seven
minor findings, applied: the ring means' attribution (the count's mean
outside at r = 16 and by its ripple; the flow's at r = 12, 16, 20);
Coulomb's pin as the register states it (-Qq / (Mm) exactly) with -1
and -1/4 as the readings; J1's 0.036 moved to the reading column; the
Gleason window "derived from the measured counts after the runs", not
"measured"; series N's registered pin (the ratio 2.0, stated to fail)
in the pin column with the pair give as the unrun crowd form; the
cosine table's arguments named (d the phase difference, N the circle's
phases); Born's P named. The pin/reading separation holds on every row.

## Wave 4 (2026-09-21, after the merge of main at 42b3d470: PRs #472, #474, #475, #476, #477, #479, #481, #482)

Applied from the tree: (1) the Lorentz section and its rows per the
derivation's 17.6 (the nine must-fixes of the physics-rule review,
record 297): the self-creation gated by a proper-time owed count, the
exact square W = E'_0^2 + 3 p.p carried and E' by comparisons, c^2 =
[1, 3], the pace p / E', the identity 3 h n = Q S d checked at load;
the contraction NOT derived (the gradient of the age moment alone; the
magnetic part needs source-velocity-v1, named and not designed); the
pins restated on declared integers as detector readings (the muon's
products' face clicks at 367 and 345 against 391 at rest, the decay at
70.9 and 125.2 derived back; z = 0.369 +- 0.003 at the declared
momentum; the 5b pin withdrawn). (2) Section 22, the uncertainty
relation: a paragraph after the lattice Gleason (the support and
entropic bounds exact on Z_N, the Weyl relation, Kennard's form as the
limit with hbar = h N / (2 pi), the one read-out as the reason), a row
in Table 1, the Heisenberg row with the pin 0.92 +- 0.03 at w = 27 and
0.886 +- 0.03 at w = 9, the crowd form's 1.08 explained by its sparse
fan; the abstract names it. (3) The greats under the six-point standard
(record 300; 21.2 rows 47 to 57 with the order of the expansion and the
error term; 21.5): Gauss and continuity, Faraday and Ampere-Maxwell
with the Lorentz force and Biot-Savart (H under source-velocity-v1),
Planck and de Broglie (identities), Boltzmann and Shannon (R) with
Landauer (D), Hubble (R for the form), the aberration (R at first
order, D at second), Schrodinger (not reached): rows in Table 1 and a
third appendix table with the two new columns. (4) Item F, optical-v1
(record 302, the design and its review, admissible with eight
must-fixes; the go to the build after review, record 303): the bending
row and one sentence in the delay-field section naming where the rule
lives (record 294). (5) The Method paragraph in record 305's words and
the standard's three sources. (6) The dark row's planets sourced (HARPS
1 m/s, Mayor 2003). (7) The log bibitem: records 291 to 305 as cited, a
punctuation glitch fixed. Referee round 19 pending.

## Referee round 19 (2026-09-21): wave 4, major revision small in extent, applied

Fifteen findings, five major, all applied: the proper-time gate stated
as the accumulator it is (gaining E' - E'_0 against the wall E'_0 with
the remainder kept), not a floor of the ratio, which would owe nothing
at both J4 momenta; the supports of 22.1 are 64, 32, 8, 57 for 1, 2, 8,
8 phases (the products 64, 64, 64, 456), not "products 64, 64, 64, 57";
two stale sentences outside the diff that said the readings remove row
5b (the isotropy row; the three-failures paragraph) now say the
contraction is withdrawn from the identity; the Method's "every derived
formula" reduced to the rows added in this revision, the earlier rows
carrying the order and the error term where the derivation states
them; the invariant stated as W_E - 3 p.p = E'_0^2 with E' the integer
root (the exact square renamed W_E, since W is the wheel's width); E',
E'_0, gamma, beta, the age moment, g, rho, j named at first use in
their rows; the third appendix table narrowed by 0.02 in; record 306
and section 22 added to the bibitems (record 312, the optical review,
not on the tree, so not cited); optical-v1 reads the rows at the row's
own Node, and 21.4 calls the same rule flight-in-field-v1; Maassen and
Uffink's inequality "of the same form as" the entropy row's identity;
the count per self-creation per direction on the lattice; the
abstract's list re-ordered. The navigation gate: main's boss skill
routes paper-coordinator and not paper-writer; the route row restored.

## Wave 5 (2026-09-21, after the merge of main at 9958214e): Eq. (1) first, the exact square, the second round

The owner's word (record 320, pending on main; relayed by the Boss at
about 09:55Z, translated): "at the beginning of the paper there should
be our big formula, and what is derived from it, if it is zero and
times it is zero, and all these things ... exactly in the same form,
where everyone always puts it." Applied in the standard place: the
abstract states the law in words; the introduction ends by announcing
Eq. (1); the first section after the introduction states it once as
the first numbered displayed equation, every symbol named at first
use, the six operations as a numbered list under it, then "The special
cases that follow at once" (seven, each a rate, wall or content at zero
or a wall times a factor, one line each with its place: the row as the
body of zero content; the free family at zero cost; the pair at zero
turning a rule off; the bilinear push at zero flow and zero content;
the wall times a factor, the growing wall and the optical wall; the
phase-less family; the remainder kept at every division), then "What
follows from Eq. (1), in order" with the sections; the old "The map"
paragraph becomes "The components of Eq. (1)" without its duplicates.
The exact-square page the mathematician sent at the owner's order ("it
is beautiful") entered as a boxed figure in the Lorentz section, with
its integers re-checked (14 671^2 <= 215 258 304 < 14 672^2; 25 910^2
<= 671 339 712) and one correction: S is the world's width, not the
GameBoard's size. The second round of the covariant readings' review
(record 314, buildable with must-fixes; 17.6's N1 to N6, PR #485 at
135f80a1) entered the Lorentz section: the domain of the pace, the push
ceiling and three comparisons, the crossing count's sum, the release
per lattice interval, the load-time identity a diagnostic, the books'
balance withdrawn, the J4 shape [201, 1, 1] with the re-derived ticks.
The appendix says the map now carries the pin column (PR #489). The
log bibitem: records 312, 314, 316, 317, 318. A bibitem for the vector
form of the law (LAW.md). Referee round 20 pending.

## Referee round 20 (2026-09-21): wave 5, major revision, applied

Fifteen findings, three major, all applied: the zero-content case is
form B's (the drive on the momentum's direction, decided and not
built), stated so, with the built per-axis drive's case beside it and
the flight's ratio S_1 Q_f / T_d, not "the wall 2 T_d"; the push named
on the gravity column with the charge column's term, and "no inertia at
zero content" replaced by the content cancelling in the ratio (the
equivalence principle); N1's count is gamma times the moving reader's
count 1 - n.beta per direction, not the rest count. Minor: the free
family as a declaration at h = 0 with the table's reading; the
suspension pair n_s / d_s, a and H named at first use; the phase-less
family as the family without a circle; the remainder kept at every
division but the click's, the charge column under its accumulator;
section 9 for the law of information; N5's exception (a world that
declares the books); E' set at load by the integer root then kept by
comparisons; the caption's algebra (division by 9, E' the root to the
remainder); the figure's table narrowed; Q_f, S, M, T_d, S_1, N named
at first use in the reordered section; "among them" for the roundings
with the click's rung added; the log bibitem's punctuation.

## The quantum-mechanics section (2026-09-21, the owner's direction of about 08:50Z)

The owner (translated): "Let us look at what the very first paper on
quantum mechanics was. We need somehow to put this in, because the one
who gives me the endorsement is also from quantum mechanics ... how we
see it, how it connects ... some formula, Schrodinger or something."
Applied as one section before the confrontation, "Quantum mechanics in
the law: the founding formulas, one by one": how the law sees it in one
sentence (the record's vector in Z[Z_N] where the wavefunction sits,
the evaluation the Fourier transform, the click the measurement); then
Planck 1900 (E = h f an identity of the release, R), Einstein 1905 (the
row is the quantum, the law's definition), Bohr 1913 (in form), de
Broglie 1924 (the turn by momentum, an identity), Heisenberg 1925 (the
law's kinematics a matrix mechanics on Z_N: the Weyl relation exact,
the Gram form; Weyl 1931 and Schwinger 1960 the cousins), Schrodinger
1926 (NOT reached, stated plainly: omega = c k, a body one record, the
dispersion named), Born 1926 (a limit, forced in form), Heisenberg 1927
(exact on the circle, Kennard the limit), Dirac 1928 (not reached: no
spin), Bell 1964 and Tsirelson 1980 (measured and proved); a closing
paragraph; Weyl and Schwinger in the literature; the founding papers'
bibitems. No claim that the law is quantum mechanics. Referee round 21
(a quantum physicist's reading) pending.

## Referee round 21 (2026-09-21): the quantum-mechanics section, a quantum physicist's reading, major revision, applied

Twelve findings, six major, all applied: the rung's bound cited to
Definition def:click and 6.2, not to the isometry theorem, with the
paper's own rung symbol; the single opening's pin placed in the Gleason
section and row 10 named as not yet run with its last registered 1.08;
"the one founding formula the law gives a different answer to" replaced
by "the one equation of motion the law does not reach" (Dirac and
Bohr's levels are not reached either; row 57 is not reached, not a
different answer); Heisenberg 1925 restated honestly: the arrays
between levels are not reached (no stationary states), what is reached
is the kinematics in Weyl's form, the commutator credited to Born and
Jordan, the continuum commutator as the contraction of the Weyl
relation; the Bell paragraph: a deterministic rule whose value is not a
LOCAL hidden-variable value, the joint Gram weight and no-signalling,
the unproved "same Fourier fact" dropped; Einstein 1905 with 6.4's
caveat (content and turn part at a re-emission; the relation at the
absorber not derived). Minor: "closes no orbit on the base"; the
digital-circle numbers as the derivation's arithmetic; the symbols
(f the record vector and f the frequency separated by s_h; zeta for the
root, omega and k named; W_k, T, the rung named); note 39 in the
beamlaw bibitem; Weyl's edition and Schrodinger's fourth communication;
the closing list with Einstein and Born as a limit; the introduction
names the section, not table rows; the harmonic constants pinned by a
host map.

## Wave 6 (2026-09-21, after the merge of main at 5fdf38e5: the click at 7e523c55, PR #492, PR #486, #489, the records to 325)

The click landed (record 324; BEAM_LAW notes 45 and 46): Part I's
components name the birth wheel as a lamp's declared rate (u = ordinal
x r_w mod W, one row of the counts table, 4096 at the golden rate on the
registered two-slit world) and the exact phase at the click (one
Euclidean division from the row's two counts), both built; "decided,
not built" removed for the wheel everywhere. The two-slit world
re-registered at 4096 births under the wheel and the exact phase (L2b):
the dark pixels 0 to 3 as pinned, the counts' correlation with the
cosine 0.891 against the weights' 0.895, the visibility 0.966 against
0.954, every cell within 2 of its rung; the bright pixels 19 to 51
against the map's 28 to 29, the map's fan the screen's and not this
world's (reported as outside): Young's row, the Gleason paragraph, the
nature table's row 2a (the register's row predates the re-registration:
0.966 against 0.98, FAIL by 0.014 in the clicks, reported to the Boss
for the physicist's update of NATURE.md), Part III's Young paragraph
and the appendix's Young row. The Doppler row cites 2.7 again (restated
by PR #492); 21.4 names optical-v1 (the parenthesis dropped); the
bending row and the delay-field sentence: reviewed twice, buildable
after form B, not yet built (record 323, REVIEW_ROUND2.md). The log
bibitem: 320, 322, 323, 324; the beamlaw bibitem: notes 45, 46. The
paper-writer skill folded into paper-coordinator on the Boss's word
(record 309): the file deleted, the route removed, one MIGRATION line.
Referee round 22 pending.

## Referee round 22 (2026-09-21): wave 6, major revision, applied

Nine findings, four major, all applied: the two-slit pin before the run
was the counts' correlation about 0.96, not a visibility, and it was
missed (0.891), the register's reason being that the pin was the
screen's fan's and not this world's: stated so in Part III, in Young's
row and in the appendix (the pin column now the three pins, the reading
column the misses and the reason); the Gleason paragraph no longer says
no registered click pattern tests the kernel; row 2a's clicks marked as
this paper's addition and its FAIL by 0.014 as this paper's reading
(NATURE.md still reads NOT YET; reported to the Boss); the appendix's
Young row names slits_huygens (L2b), not slits_low (L2); the wheel
written as the rate r_w per birth against the wall W with u, r_w and
the ordinal named and [2531, 4096] given; the exact phase as the
click's one division with its remainder kept; the read-out sentence
compares the wheel's coordinate; "within 2 where the pin said within
one, the rungs per record"; the beamlaw bibitem's notes in order.

## Wave 7 (2026-09-21, after the merge of main at b09fbc24): the glossary, Fine 1982, record 326

The glossary audit landed (record 321, PR #494 at e6b76725): the
paper's glossary and symbols table are taken from TERMINOLOGY.md at
that commit, as its top sentence orders, into an appendix before the
Reproducibility section: the terms in one paragraph (Node, GameBoard,
Link, Port, row, body, record, click, family, crowd, pin; "lattice" in
this paper the mathematical Z^3, the lattice gases and the lattice
Gleason, the physical board being the GameBoard), and a table of the
paper's symbols with name, kind under the notation rule and place,
the glossary's spelling given where the paper's differs (Q_f for Q,
T_d for T_D, d for D). The Bell paragraph of the quantum-mechanics
section cites Fine 1982 as 22.3 restated (PR #498 at 31cb7926): a
joint distribution over the four outcomes exists exactly when the CHSH
inequalities hold, so the registered 176 / 64 has none; the withdrawn
phrase is not repeated. The highlights bibitem names 5.4's "Decisions
of 2026-09-21"; the log bibitem adds 326. The exact circle of record
327 ("go with the beautiful solution") was withdrawn by the owner's
correction, record 328: the existing tables at 1/256 stay and are
declared an input of the law; the paper's one sentence follows in
wave 8. Referee round 23 pending.

## Referee round 23 (2026-09-21): the glossary appendix, major revision, applied

Nineteen findings, four major, all applied: Delta is the Gleason
kernel's argument (the phase difference of two rows), not "the meeting
key's offset"; J is the pair's joint sum with W = J^2 the weight; the
paper's K (a fan's direction count) named as not the glossary's K (the
clock's pair, the world key), and eta = n / d as that pair; the fan's
grain G named as the archived code's, distinct from the retired grain
of the doppler key; every duplicated letter given its "not the ..."
(q, a, b, r, S, H, m, w, s, k, f, rho, N, Q, Lambda and lambda, E);
the prose follows the glossary's own words for the row, the click (the
record's read-out being Part III's click by Definition def:click), the
crowd (the six neighbours the crowd audit's, not the glossary's crowd);
"board" removed as a retired word; the word "lattice" kept only for Z^3
as a mathematical object, the cubic and bipartite lattice of the
derivation, the lattice gases and schemes of the literature and the
lattice Gleason, and about forty uses as the noun for the physical
thing renamed to the GameBoard (the GameBoard's frame, on the
GameBoard, through the GameBoard, the GameBoard's stand-in for the
rotation group, ...); the notation rule's exceptions stated (U, V, d, f
written plain; s, r one component of the glossary's vectors); Fine's
theorem stated as a joint distribution of the four observables
returning the pair distributions as marginals; the highlights bibitem
with 5.4's title and subsection; the log bibitem's 326 wording and a
missing comma; the table narrowed to 6.15 in; the Where cells.

## Wave 8 (2026-09-21): the circle's rounding declared an input, record 328

Part I's "What is put in" gains one sentence: the tables of cos and sin
of every phase step, scaled by 256 and rounded to the nearest integer,
computed once at load from integer series, law data and not a register
at a Node, read at the click through the Gram matrix G = E^T E and,
at 2N, at the label rotation (the half-angle tables), are declared an
input of the law with the standing of N and Q_f and kept (record 328),
as signal processing takes a rounding of the circle as the definition
and keeps it, with the four precedents the Boss found, each checked
by the coordinator for journal, volume, first page and year against
the publisher's record: Malvar, Hallapuro, Karczewicz and Kerofsky 2003 (IEEE Trans.
Circuits Syst. Video Technol. 13, 598; the H.264/AVC integer
transform), Welch 1969 (IEEE Trans. Audio Electroacoust. 17, 151; the
fixed-point FFT), Mathews 1963 (Science 142, 553; the stored waveform
table) and Goodman and Silvestri 1970 (IBM J. Res. Dev. 14, 478; the
phase quantized to N levels). The appendix's caveat on the cosine table
names it a declared input. The log bibitem adds 327 and 328. A
duplicated bibitem (fhp1986, entered twice) removed. The exact circle
(PR #501, exact-circle-v1) is closed unmerged and is not cited.
Referee round 24 pending.

## Referee round 24 (2026-09-21): the circle's rounding declared, major revision, applied

Eleven findings, two major, all applied: the tables are read not only
at the click but also, at 2N, at the label rotation (the half-angle
tables of Part III), as the paper's own appendix caveat says, so "read
only at the click" (record 328's phrase) is replaced by the tree's
fact; the bold E and G named at their first appearance (E the 2 x N
matrix of the tables, G the click's Gram matrix, not the fan's grain
G of the same paragraph); "beside Q_f, S and N" replaced by "with the
standing of N and Q_f" (S is a physical input in the paragraph's own
taxonomy); the precedents' wording tightened (Malvar's cosines
replaced by small integers, not rounded; Welch bounds the error, not
the factors; "the first digital instrument" dropped; Goodman's N is
theirs); "fixed-point transforms" narrowed to "signal processing"; the
sentence split in two; Part III's "third input" tied to its own list
of three and to Part I's declaration; PLAN.md's "reverted" corrected
to "closed unmerged" and the verification claim made concrete.

## Wave 9 (2026-09-21): main at 8c4a9754 taken (row 2a restated, the fan's grain G in the glossary)

Main merged (PRs #502 and #503). NATURE row 2a is restated to the
clicks under the birth wheel (d66ac8b6): FAIL, 0.966 against 0.98,
0.014 below the measured and 0.034 below the ideal, the cause named
(the fan's grain); the paper's row 2a drops "this paper's reading" and
the register-predates-it note, and the count of this paper's additions
to the register falls from three cells to two (rows 4a and 5b). The
glossary's symbols table gains the fan's grain G as a constant of the
law beside N, Q, P, W and K, distinct from the retired grain of
doppler-v1 (6d57c7a2); the paper's glossary appendix, its caption and
the terminology bibitem now cite 6d57c7a2, and the G row's wording
follows the glossary's. The reproducibility caveat names main at
8c4a9754. Records 329 to 332 (Kepler, Compton and Malus ordered; the
Schrodinger question and the owner's yes to massive-rows-v1, PR #500)
and the derivation's rows 58 and 59 (PR #504) are not on main yet and
are not cited; the paper keeps Schrodinger "not reached" until the
derivation is on the tree. Referee round 25 pending.

## Referee round 25 (2026-09-21): wave 9, minor revision, applied

Four findings, all applied: the register's provenance in the paragraph
and in the caption names row 2a's restatement at d66ac8b6, as
NUMBERS.md does; the change-history sentence on row 2a replaced by
"the register's own reading"; the G row's list of constants says whose
letters they are (the glossary's N, Q, P, W and K, this paper's N, Q_f,
P, W and eta); row 2a's verdict cell carries the register's correlation
miss (0.96 pinned, 0.891 read, the pin the screen's fan's). Verified by
the referee: every number of row 2a against NATURE.md, 0.026 the
register's own prose, the tally unchanged, the G row in the symbols
table at 6d57c7a2 (53 rows), nothing of records 329 to 332 cited.

## Wave 10 (2026-09-21): from the Node to the 48, the 24 and the pace; the order of the laws; Kepler, Compton and Malus pinned

The owner's order through the Visualiser, relayed by the Boss (the
record in PR #500, not yet on main, so not cited): one place that
explains, from the six-Port Node, the 48 signed permutations, the
determinant's 24 rotations and 24 improper maps, the hand as that
determinant, the octahedron of the six Ports and its inscribed sphere
c = 1 / sqrt 3, and then every law of the paper from Eq. (1) in order
with how each was reached. Part I gains the paragraph "From the Node
to the group, the octahedron and the pace" (records 142, 226 and 231
cited; Theorem th:group, Proposition prop:pace and Figure
fig:octahedron referenced, nothing re-proved) and the paragraph "What
follows from Eq. (1), in order" becomes a numbered list in the Boss's
order (Gauss, Newton and Coulomb, Doppler, the delay field, Born and
the uncertainty relation, Young, Bohr, the information law, the
redshift, then the masses, Kepler and Compton), each with its operation
and how it was reached (limit, pin, run), the derivation record
appendix holding the numbers. Main at 10f00c94 taken: the derivation's
rows 58 (Kepler) and 59 (Compton), pinned and not run, enter the table
of consequences and the derivation record; the Malus note
(docs/designs/malus/NOTE.md, 70a39d6b) enters as a design from the
entries in force with the pin 128, 0, 64 of 256 exact, NATURE row 9
kept NOT YET with the pin named; the introduction's "in the limit only"
list adds Kepler's laws; the derivations bibitem names 21.5's rows 58
and 59; a malus bibitem; the log bibitem adds 142. The Visualiser's
page 10 is not on the tree and is not cited. Referee round 26 pending.

## Referee round 26 (2026-09-21): wave 10, major revision, applied

Fifteen findings, three major, all applied: the pace stated as a bound
(the value c = 1/sqrt 3 the design's third statement, assumed, as
tab:recorda says), 48 and 24 counts of the figure and 1/sqrt 3 its
bound, the constants listed with the fan's grain G and the roundings;
the Kepler pin said to stand on form B, decided and not built (under the
drive as built the host's period 687), with s32_r12_lamp named; the
Compton row saying the law as built gives a different law (the released
row takes the re-emitter's turn, no shift, the derivation's D on main);
the parity worlds' qualifier "with an axis"; the duplicated sentence on
the stand-in cut and "before any rate" corrected; Gauss from the release
(operation 6) and the walk (operation 1); the source's Doppler read on
G2 added; Bohr's levels open; Milne's q = 0 read inside; the masses'
runs not called "not run"; "pin:" prefixed on the three new status
cells; NATURE row 9's reading cell back to "no polariser built", the pin
in the verdict cell, the caption naming it with the register's row
unchanged; the read at a sum set with its cells clicked; the derivations
bibitem's locator 21.2 with the blocks in 21.5; the log bibitem's 142 in
order; the introduction's Kepler "(pinned, not run)".

## The owner's review of abdf1115 (2026-09-21), handled

The owner's own review of main at abdf1115 (the paper at 411667c5),
relayed in conversation: the Doppler of a moving detector along an axis
built (the crossing rule in the engine, 1 +- v/c, the relativistic
factor missing); the discrete design of the energy and the clock
complete, the condition E'^2 <= W < (E'+1)^2 checked by him over 40 000
small momentum changes (an arithmetic check of the design, not an
engine run; his check is not on the tree and is not cited); still open:
(1) the design and the drive with the cap at c not in the main engine,
(2) the domain, about 0.866 c along an axis, (3) the contraction and the
energy balance at emission and absorption, (4) no demonstration that a
moving detector reads the same c in every direction. The paper carried
(1) and (3) already (not built, not run; the contraction not derived;
the books' balance withdrawn); the Lorentz section now states the four
in one sentence at the end of the covariant-readings passage and adds
beta at most 0.866 to the domain; the integer form of the invariant was
already in the section (the open item of the floating-point check
closed) and in Figure fig:square.

## Referee round 27 (2026-09-21): the Lorentz open list, rewritten

Seven findings, three major, all applied: form B is "decided and in
build, not on main" (HIGHLIGHTS 5.4, record 301), not "not built", at
every place the paper said so (Part I's special case, the state, the
Newton section, the Kepler rows); the domain parenthesis once, "gamma at
most 2, beta at most 0.866, on a heading"; the books "withdrawn until
derived" in the source's words, not renamed "the energy balance"; a
moving detector's c stated by the three quantities the derivation keeps
apart (the one-way count 1 -+ beta, the two-way count of an isotropic
crowd the rest count exactly, the round-trip time gamma^2 along and
gamma across, row 5b FAIL (pinned)), the wrong "its pin withdrawn"
removed; the floating-point sentence dropped as a duplicate of the
section's own sentence and the figure's caption; the passage reduced to
one sentence so that nothing in the section is said twice.

## Wave 11 (2026-09-21): Schrodinger reached only in part (section 23), records 329 to 336

Main at 5cc43ae7 merged (PR #500's records 329 to 336; PR #507's
section 23). Schrodinger's equation for a free particle: on the law as
built not reached (every row at c); under massive-rows-v1, a hypothesis
named and not built, the time-independent free equation reached in
form (the massive row's wall E' = isqrt(E'_0^2 + 3 p . p), the photon
its E'_0 = 0 case; de Broglie's turn per Link; the phase (N / h) p . x
on the Nodes; the Helmholtz limit with k = 2 pi p / h, the
time-independent Klein-Gordon form exactly, Schrodinger's at second
order in p / E'_0; Born's |psi|^2 the click's Gram form), the
time-dependent form not reached (no frequency in flight, forced by the
click; one momentum per record); the pin slits_matter before any run
(the bands at 36.5, 60, 83.5 within one; Pearson 0.96 +- 0.02; the
centre's first click at 1 + 828 within 2), the confrontation Jonsson
1961 and Tonomura 1989; the price stated (a massive quantum in flight a
record of rows, matter a body after the click; record 332). Changed:
the QM section's Schrodinger paragraph and its sum, the table of
consequences, the derivation record, the hypotheses section's one
sentence (massive-rows-v1 named once), the jonsson1961 bibitem, the
derivations bibitem (23; row 60; E19), the log bibitem (330 to 336),
the citations of 334 and 335 in Part I and the tables. Referee round
28 pending.

## Referee round 28 (2026-09-21): Schrodinger in part, applied

Thirteen findings, two major, all applied: the derivation record's row
restored to six cells (the order and the error term in their own
columns; the label "the limit proved under massive-rows-v1, the pin
assumed"); the consequences row's status prefixed "pin:" as the legend
binds; "not replicating in flight" in 23.5's words (the birth over the
fan the one apportioning); the phase exact to the accumulator's
remainder; Born's |psi|^2 the Gram form at the click and nowhere
between clicks; the wall E' by comparisons at the birth, no root in
flight; the QM section's status list gains "under a hypothesis named
beside it"; the hypotheses section says the design is ordered and not
delivered (record 336), not run; two commas in the bibitems; record
333's gloss with the atoms; record 334 cited as the owner's direction,
not as evidence. Reported, pre-existing: the abstract at 1944 characters
between its LaTeX markers (the plain-text count for arXiv's 1920 is
taken at submission, arxiv_metadata.md); the Heisenberg single-opening
row's status without "pin:".

## Record 337 (2026-09-21): the paper as a theory, four parts

The owner's order through the Boss (record 337): the physics must come
out of the law and not go in as input; a few postulates, one local
update law, the known phenomena; the referee's question whether the
physics comes from F or hides in r, b, the family tables, the bilinear
forms, the matrices and the click rule; the strongest test a
prediction computed in advance. Four parts, each its own push (on one
branch, successive heads): (1) paper/README.md: the archived v0.3.1
manuscripts named historical, general_formula/main.tex the one paper.
(2) The postulates P1 to P10 at the head of Section sec:law, before
Eq. (1), from the derivation's inputs ledger (24.1): the bounded
integers, the GameBoard, the six operations, locality, one Link per
interval, the click, the grains, the physical inputs, the rules chosen
among few (the flight blind to the crowd, form B's drive, the
collision's shift), Born's member c_1 = 1 the one imported law; the
bilinear rate of a body's reading derived (24.2). With it the owner's
finding on the lattice Gleason: hypothesis (d), the empty record reads
zero and R is not identically zero, without which the constant reading
satisfies (a) to (c); the derivation's 6.5 has the same gap (reported
to the Boss). (3) The standing column of Table tab:consequences, one
word per row: DERIVED, HYPOTHESIS, POSTULATE, INPUT, DIFFERENT, NOT
REACHED, OPEN, the words after the ledger; c = 1/sqrt 3 DERIVED given
the flight's declared wall (24.1 row 9), the expansion rows HYPOTHESIS
(expansion-v1 a declared assumption, record 279), the different-law
rows DIFFERENT. (4) The section "Where the law differs, by how much,
and what bounds it" from 24.3 (twenty differences with the bounding
experiment and the verdict on main) and 24.4 (the one prediction: S =
181/64 = 2.828125 for N a power of two at or above 512, three parts in
ten thousand below Tsirelson's bound, inside Poh et al. 2015 at 1.1
standard errors, what refutes it, the run at N = 512 and 4096 pending);
the twelve failures stay in the abstract. Referee round 29 (eleven
findings, four major: P4's invented phrases, P6 too narrow, the
expansion rows, the table's width; the README's leftovers) applied;
"What is put in" shortened to what P7 and P8 do not say (the circle's
rounding with its precedents, the program's quotation). Referee round
30 on P9, P10, the relabelling of c and the differing section pending.
The references of 24.3 verified against the publishers' records before
citing: Poh et al. 2015 (PRL 115, 180408), Herrmann et al. 2009 (PRD
80, 105011), Botermann et al. 2014 (PRL 113, 120405), Bucherer 1909
(Ann. Phys. 333, 513), Kostelecky and Russell 2011 (Rev. Mod. Phys. 83,
11), Delva et al. 2018 (PRL 121, 231101), Vessot et al. 1980 (PRL 45,
2081), Clemence 1947 (Rev. Mod. Phys. 19, 361), Dyson, Eddington and
Davidson 1920 (Phil. Trans. R. Soc. A 220, 291), Shapiro et al. 2004
(PRL 92, 121101).

## Wave 12 (2026-09-21): the 48 figure attached, record 334

The Visualiser's page 10 (PR #508, on main at 807b1be7) and its tool
tools/gallery_pages.py --figures write octahedron.png and the_48.png
for the paper: the 48 signed axis permutations, each the octahedron of
the six Ports after g with its matrix and determinant, the 24 rotations
above (the identity 1, half turns about the Port axes 3, quarter turns
6, half turns about the edge axes 6, third turns about the diagonals
8) and the 24 improper below (reflections in the Port planes 3, the
inversion 1, reflections in the diagonal planes 6, quarter turns with a
reflection 6, sixth turns with a reflection 8); the test pins the
counts; no run, nothing pinned by the page. Part I gains Figure
fig:the48 after the group paragraph; the paper's own octahedron.pdf
stays; the gallery bibitem; paper/README.md names the two files and
the command. Referee round 31 pending.

## Referee round 31 (2026-09-21): the 48 figure, applied

Eight findings, two major, all applied (in the commit after the
figure's, which went out before the findings were in): the figure set
by height (0.72 of the text height) so the block with its caption fits
one page under [H]; the caption says the matrices and indices are
legible on the page, not in print; the builder's order named;
"checks", not "pins", for the test; the hand as a row's pseudoscalar
column with record 142; the duplicated sentence folded into the
paragraph; the README and the bibitem say the paper uses the_48.png
only (octahedron.png written and not used, not committed); the bibitem
quotes the page's own words. Main merged at bd74c49a (records 338 and
339; the log bibitem adds them).

## Record 340 (2026-09-21): the owner's second review, from main at 119fd9b8

Eq. (1) written as the count primitive implements it (the derivation's
section 0 restated, PR #525): e = sign(s) min(floor(|s|/b), a) with
the signed rate and the remainder kept, the cap a = 1 the drive's
alone, every other count firing the whole part (the owner's high-rate
series 0, 2, 5, 7, 10), and one sentence on where the 0/1 form holds
(the flight, the drive by its cap, the wheel, a slow clock). The
lattice Gleason's hypotheses (d) the empty reads zero and (e) some
input reads, as 6.5 states them (record 340). The abstract's pace
qualified: the rows' pace c, the largest uniform one, a body's pace
not bounded by it under the law as declared. The axis preference and a
body's pace above the rows' stated where the drive is stated (the
owner's eight runs: 26 Nodes on x and none on y; 0.925 against 0.582;
the cap one Link per interval, 1.72 c, the engine's rule that one axis
steps per interval) and as rows 21 and 22 of the differing table (24.3),
both refuted on main as declared and closed under form B's directional
drive, in build (PR #526 in review). A duplicated ame2020 bibitem
removed. Referee round 32 pending.

## Referee round 32 (2026-09-21): record 340's round, applied

Twelve findings, four major, all applied: under the cap the residual
above the wall is kept and fires one event at each following interval
(not a Euclidean remainder); the cap and the sign named as operation
6's comparison, the capped carry an injection that loses nothing, so
still no third non-linear place; the abstract's and the introduction's
summaries in the count form ("count the walls it holds, capped at one
for the drive; every wall counted is an event"), the glossary's e the
event count with a its cap; a = infinity where no cap is declared; the
drive's form with the sign; the axis preference in the engine's words
(the first axis whose rule fires, x before y before z when two fire in
one interval); a body's cap one Link per interval in all, T_d / Q_f =
1.72 times the rows' pace on a heading (sqrt 3 c), not "up to sqrt 3
Nodes per interval, 3 c" as 24.3 row 22 has it (the tree's error,
reported: the engine's _move steps one axis per interval; FORM.md's
1.72 c agrees); row 22 closed also under the covariant readings; the
Cohen-Glashow bound named as the neutrinos', the charged bodies' the
vacuum Cherenkov one; (d) excludes the constant reading and (e) the
zero detector, said so; "form B in build" in the abstract. The
abstract at 1921 plain characters after the measurement-chapter
sentence was cut for the prediction's.

## Wave 13 (2026-09-21): the formulas of flow, heat and temperature (section 25, round 1)

Main at c61d2117 merged (PR #529, the derivation's section 25). A
short section before the confrontation with nature with
Table tab:continuum: the twenty-three formulas of the continuum, what
the GameBoard has of each and its standing in the paper's words
(three exact: the continuity equation, Boltzmann's count, the second
law at the click; six in form on the six-heading gas with the cubic
lattice's obstacle; three identities of readings; two by reference;
nine not reached, five of them falling to elastic-contact-v1, named
and not designed); one row of the table of consequences pointing to
it; the derivations bibitem adds 25. Records 341 to 343 are not on the
log at c61d2117 and are not cited. Referee round 33 pending.

## Referee round 33 (2026-09-21): the continuum section, applied

Eleven findings, four major, all applied: four rows fall to
elastic-contact-v1 (9, 10, 19, 21), not five, the isotropic
Navier-Stokes to fan-collision-v1 (25.3's "five" is the source's own
slip against 25.2's "one identity named for four rows", reported); the
entropy count cross-referenced to the table's entropy row and the
derivation's 14, the bijection to its theorem; rows 7 and 15 in the
legend's words; the bundle row split into DERIVED (fourteen) and NOT
REACHED (nine), placed before the DIFFERENT block, the overlap with
existing rows said; the FCHC projection cited to d'Humieres, Lallemand
and Frisch 1986, not to FHP; D_diff named; row 12 in form at the click;
row 23's two reasons; "the HPP obstacle of the cubic lattice gas" on
"the six-Link GameBoard"; the paper's phrase "torus points"; the
bibitem's commas. Reported as the tree's: section 25's header cites
record 343, which is on no log at HEAD.

## Wave 14 (2026-09-21): every formula with its route; where the law's form stands above (record 352)

The owner's order through the Boss (record 352): for every formula of
nature the paper carries, the route from the law or one line on how it
is reached, never a bare "derived"; where the law's form stands above
the known one, one sentence with what the law adds and what the
derivation holds; formulas not needed leave; formulas wanted and
lacking listed to the Boss. Done: the table's legend names the record
appendix as the route of every DERIVED row; the appendix gains the two
rows it lacked (the source's Doppler, 2.5 with series G2's coasting
stars; Newton's geodesics, 5.3, the form proved and open for the run);
a paragraph at the end of the table section, "Where the law's form
stands above the known one", six places each with the derivation's
section: the exact square above Einstein's E^2 = E_0^2 + p^2 c^2 (17's
theorem: true of the linear block and of what is built from it, for a
body as far as its readings are covariant; the covariant readings a
hypothesis, not built), the CHSH value at finite N above the bound
(6.2), Born's rule to the rung (6.2), the uncertainty relation exact on
Z_N (22), the entropy's accounting at the click (14), Gauss exact at
every instant (5.5). Removed: no formula (every row of the tables is
either routed, one-lined or marked not reached; the candidates for the
owner's word are the continuum rows not reached, Hooke, Ohm, Stokes,
which the inventory he ordered carries). Wanted and lacking, sent to
the Boss: the time-dependent Schrodinger equation, the Lorentz
contraction and the books' balance, Kepler's precession on the
GameBoard, the isotropic Navier-Stokes, Planck's spectrum, Dirac,
Bohr's levels, Einstein's field equation, the strong ratio's remainder,
the weak forms' memorylessness. Referee round 34 pending.

Folded into wave 14 after main at 6a59ee04 and e0282b6a: the Bell run
of 24.4 (S = 1448 / 512 and 11584 / 4096, both 181 / 64 exactly, the
marginals W / 2, PASS on eight worlds) as "pinned and run, once,
awaiting its replication"; section 25's round 2 (rows 2, 3, 5 and 22 of
Table tab:continuum at round 2's standing: the Galilean factor and the
sound speed in closed form, the one-axis Navier-Stokes with the shear
frozen, diffusion as one tensor law anisotropic along the cube's
diagonal, round 1's isotropy withdrawn); the law's two declared ties
named as BEAM_LAW note 39 has them (the digital line's axis order, the
collision's Port order), the apportioning's the derivation's; the log
bibitem adds 341 to 348; records 349 to 357 not yet on main, the
owner's replication rule cited by date until 353 lands.

## Referee round 34 (2026-09-21): wave 14, applied

Thirteen findings, six major, all applied: the nature section's tally
to five PASS (each measured once), two NOT YET, row 9's restatement at
71e15626 named; nine worlds with another clock pair (row 9 flagged
since 71e15626); the owner's rule cited by date until its record is on
the log, the replications file named as being written; the exact
square's integer condition filed as the covariant readings' (a
hypothesis, not built), not the law's; quantum mechanics gives one
value and the bound; 181/64 at every power of two from 512; the
source's Doppler row's pin the register's (Milne's q = 0 +- 0.25), the
per-star form a host reading after the run; the entropy item without
"beyond Boltzmann", the click as the one read-out with the cancel and
the leaks beside it; Gauss "after the front" with the two Gauss rows;
the legend's route sentence with its three exceptions; "run once, met
exactly" in the abstract; the plane's "measured once (awaiting
replication)". The abstract at 1902 plain characters.

## Referee round 35 (2026-09-21): the late additions, applied

Fifteen findings, four major, all applied: the register pointer to the
Bell 24.4 block and its test named; the replication parenthesis
sourced to the paper's own convention (the caption) until the record
lands; the N = 512 worlds written by the generator for the run,
1448/512 in the registered list; rows 4, 6 and 8 of Table
tab:continuum brought to round 2 (Bernoulli's factor g(1 - c_s^2),
Fourier as one tensor law with row 5, the ideal gas law's identity
exact in the mean with the drive's saturation -v_a as the error), the
caption "rows 2 to 6, 8 and 22"; d the density per heading and d_p the
parked pair's; the ideal gas law and equipartition's half in the prose;
the ties cited to note 39 and section 4, the apportioning's tie said
to break no axis symmetry; a comma in the log bibitem. Reported as the
tree's: 24.4 still says the run at N = 4096 "is the pin's run" in the
future tense after the run was made.

## Wave 15 (2026-09-21): records 349, 352, 353 and 356 cited by number

Main merged at e2259ef6 (PRs #541, #543, #545 and #546 among others; records 349 to 357
on the log). The paper's citations by date or by "its record to be
cited once it is on the log" become citations by number: the record
appendix's caption (the replication rule, record 353; the replications
document named as record 353 orders it, no line on the tree yet), the
prediction paragraph (record 353), the stands-above paragraph (the
owner's order, record 352), the symmetries paragraph (the first tie as
record 349 read it on the GameBoard: the label, the momentum and the
hand covariant under all 48, the Nodes crossed and the exit face only
under the 8 that keep the axis order), the log bibitem (349, 352, 353,
356 and three missing commas), the Reproducibility caveat's main commit.
No number changes. Referee round 36 (four findings, all applied): the
record-349 sentence had severed the invariance list, now placed after
it; the readings are the faces' detectors', not a GameBoard reading;
"the momentum" is the row's momentum by the auditor's verdict, the
mapped-back escaped momentum equal to the base under the 8 alone; the
comma after 336's gloss. The referee's caution kept: the run's five
directions carry no heading, so "exact on the headings" is the pin's
host analysis and series P's test, not this run; the paper says "exact
on every untied direction" for the run.

## Wave 16 (2026-09-21): the families' appendix (record 358), record 359's readings, the crowd's clock, the replicated map

The owner's word through the physicist's session (record 358): the
tables of the masses, the groups, the sets and the vectors of all the
families in the paper; the mathematician's audit (PR #547) found the
schema carried and the rows never. Done: a new appendix before the
glossary, "the families, the sets, the groups and the vectors", with
F1 (the 75 families in their 28 entities, every declared key; the 24
thrown sources and the 24 Hubble stars one row each), F1b (the 21
declarations of the worlds that differ from the definitions, said once
to be the register's declared variants and not a second law), F2 (the
content every family carries on the worlds' measured events, per
series; the held content), F3 (the group per declared quantity, per
family of the physics, PREDICTIONS 26's rule) and F4 (the state vector
per kind, the six verbs); every number an input of the register, none
a measurement; the tables generated from the tree's script over the
one source (families.json and the worlds) by a scratch script, so the
crowd-clock worlds landed since the audit are in F2. Pointers: P8, the
masses row of Table 1 (F1, F2), "The state" (F4), the symmetries (F3).
The audit's answers: all the families (question 1); the variants said
once (2); the masses row cites F2 (3); F3 in the appendix with a
pointer beside the symmetries (4). Record 359: the second tie's
reading beside the first's (16 of 48, the difference reaching the
detector); the pace bound read again on all 290 directions in the c
row of the record appendix; the crowd's clock in the clock's-redshift
paragraph (the tree's worlds, pinned before the run, run twice on
main 119fd9b, the entry drafted and not registered; series Q landed
on main at 33330d59 during the wave and is cited beside it, the
cluster at rest and thrown as one, the sum against the product, its
entry drafted and not registered), measured once. Series R
re-registered under the crossing rule (PR #554): the masses row and
the record appendix give the kicked u's exit at 63 in the registered
3000-interval run before the rule and at 64 in the replay under it. Record 360: the register's
replicated map in the record appendix's caption. The log bibitem to
360; two bibitems (the audit, the crowd's clock). Reported to the Boss
as the tree's: the audit's prose says 27 entities and 23 inline
declarations where its output counts 28 and 21; TERMINOLOGY gives the
lifetime in intervals and the audit in Links (the paper says the age);
the quarks' README table and its prose disagree on the kicked u's exit
before the crossing rule (the table's 3000-interval run: reaches the
face at 62, leaves at 63; the prose and MIGRATION: clicked at 69).
Referee round 37 (four findings, all applied): the unset circle is the
engine's default, a circle, and the caption names every difference
(m, the coupling p, the Hubble mass, e in the gallery, beta's hand);
the crowd-clock content is s_px1's alone in F2; at k = 0.005 the
reading 1.000/1.006 is inside the pin by its tolerance, not exact, the
four higher rungs exact; a comma in the log bibitem. The referee's
notes kept: the second window's 1.271 not printed; the test pins the
presence 4F on a short run, not the series' readings. Referee round 38
on the additions after main moved to 33330d59 (series Q, series R's
replay): no FAIL; his wording note applied (a cluster's dispersion a
spread of clocks); his note kept for the Boss: the quarks' README run
row says the kicked u left at 63 before the crossing rule and the
README's prose and MIGRATION say 69.

## Wave 17 (2026-09-21): the precedents study's five verdict lines (record 356; PRECEDENTS.md on main)

The Boss's relay of the study's PART D, applied with a referee round:
(1) KEEP the ledger, the standing column, the one prediction, the
not-claimed list (nothing changed). (2) CHANGE fig:square: the
energy-momentum relation of special relativity in place of "Einstein,
1905" (in neither 1905 paper), and the caption in the greats' form
("gives ... exactly; the relation is not new"); the stands-above
paragraph's "Einstein's" likewise. (3) CHANGE the abstract: the twelve
FAIL with their cause in one clause (seven the law's as declared in a
run made, four from a pin whose run is not made, one a declared input
refuted), the abstract cut elsewhere to stay under 1920 plain
characters. (4) ADOPT a closing sentence in the greats' form at the end
of sec:newton (no number of nature met, the reason), sec:delay (Delva
et al. 2.5e-5, Vessot et al.; the second order below reach), sec:gleason
(Sinha et al.'s kappa; the harmonic constants the gap) and sec:qm
(Hensen et al.'s 2.42 +- 0.20; Bohr's ratio awaiting its line); one
sentence in the Introduction in the author's voice ("what is new here,
it seems"); "as is well known" at the Courant condition and Kennard's
form. (5) ADOPT: the commit SHAs out of tab:nature's caption, the
nature prose, series C's fingerprint and the crowd-clock commits in Part
II, into Reproducibility; one-line bibitems for Shannon 1948, Landauer
1961, Bresenham 1965 and Jefimenko 1966, cited at the eponyms. Also:
the auditor's round 4b, the four words "with T > 0 by Theorem
th:isometry" in Lemma lem:one; the reader inside a crowd (PR #558, one
run on main d8cb46e, drafted and not registered) beside the cluster;
PRECEDENTS.md cited by path. Not yet on main, so not cited: records
361 to 366 (PR #559) and the (3, 4) split at N = 32 and 128 (PR #563).
Reported to the Boss as the tree's: examples/events/reader_clock/README.md
calls itself "Series R", the quarks' letter. Referee round 39 (four
findings, all applied): main merged at 3fa35e09 before the commit (the
study and the reader's worlds on the tree); the lemma's T > 0 stated
with its reason (the offers summed over all ends the born row's norm
up to rounding) rather than by a bare reference; the reader's formula
the sum form as pinned; the glossary caption's commit to
Reproducibility. His notes applied: "Galileo" and "loophole-free" not
on the tree, dropped; sec:newton "confronts no number of nature (the
protons' ratio enters as an input)"; the Courant sentence's grammar.
His caveat kept: the abstract folds the hypothesis rows (3; 8a, 8b)
into "the law's as declared", the finer sorting in sec:nature.

## Wave 18 (2026-09-21): records 361 to 366 by number, the split at N = 32 and 128, the derivation's section 26, the clock's word

Main merged at d17af9b9, PR #566 merged (the Boss's merge of main into this branch for
PR #566's CI taken as a merge commit; PRs #552, #559, #562, #563, #567).
The log bibitem to 366; the precedents by records 356 and 366; series
R's replay by record 364; the lemma's T = 0 by record 363. The (3, 4)
split at N = 32 and 128 (PR #563, the register's mz_345_n block): the
power window sharpened to [1.917, 2.012) in the "Against the registered
integers" paragraph, the click's-weight row of Table 1, the record
appendix and the Gleason section's closing sentence; Table tab:nature's
row 2c left as the register's row (the physicist restates it). The
derivation's section 26 (the ten formulas the paper wants and the
derivation lacks, record 352) cited at the end of the stands-above
paragraph, none claimed. Record 365 and the mathematician's note on the
clock's word: the crowd-clock worlds' k is the presence (M / r^2), the
series E clock the age moment (M / r); the presence's clock mapped to
nature fails in form (0.058 against 0.24) and in scale (1e-5 against
1e-3); the owner's decision pending; one sentence in the clock's
paragraph, a bibitem for the note. The notation (record 362,
docs/designs/notation/NOTATION.md, the mathematician's proposal): no
rename in the paper until the Boss's decision is in TERMINOLOGY; then
one wave with a notation table at the paper's head. Referee round 40:
one finding (a comma in the log bibitem), applied; his soft points
applied (the lemma cites rounds 4 and 4b, not 4b alone).

## Wave 19 (2026-09-21): the notation wave (record 362; the Boss's decision on NOTATION.md)

The Boss's decision (his message of 12:45Z under record 362, on the
mathematician's docs/designs/notation/NOTATION.md): every formula in
physics' letters (E^2 = E_0^2 + p^2 c^2 with c^2 = 1/3, v = p c^2 / E,
E_0 = m c^2); the integer form (E / c^2)^2 = m^2 + 3 p . p kept as the
exact square, never rooted, its integer root written floor(E / c^2)
(the macro \Eint); the prime of E' dropped; the grain family as the
one rule (N_phi the circle, N_l the label's scale, N_w the width, N_D
the direction bound, N_theta the fan's grain, N_u the wheel; this
paper adds N_t for the cosine tables' scale, 256, on the same rule),
the definition line m = N_l N_w M with the one note that the law's
documents write Q, S and N; the cheap renames: the four W's to
E^2/c^4, R(f) and R_k, d_p and N_u; bold F to bold Phi; the fan's G to
N_theta; P to N_D; the ladder's T to C_K; the presence k to a_r and
the age moment's k_a to a_tau; bold V to bold a; c_1 the heading's
pace; the direction D with T_D and u_D and Eq. (1)'s wall d (the
ladder's rungs b_k unchanged); the multiplicity and the Links made by
the age in code font (\mathtt m); Young's D and s to z_s and a_s
(the direction's letter taken). A notation table at the paper's head
(Table tab:notation, after the Method paragraph) and the glossary
appendix restated to it; a bibitem for the proposal and the decision.
Also under the Boss's order of 12:45Z: the clock's-word sentence and
its bibitem removed (nothing of it cited until the owner's word and
the run); the crowd paragraph keeps one clause that its k is the
presence, from the worlds' own README. Done by one scratch script
(notation.py) with exact anchors, then the leftovers checked by grep.
Referee round 41 before the commit.

## Wave 20 (2026-09-21): the replications round 1 into the labels; NATURE row 2c restated

docs/REPLICATIONS.md on main (PR #580, the Replicator's round 1): the
blocks of L1 (the Mach-Zehnder set), L3 (the pair), L6 (the pair at
N = 512 to 4096), the run of 24.4 and A12 REPLICATED, every registered
reading equal bit-exact and the four checks met; NATURE 11b
INCONCLUSIVE (a pin without a run). The paper: the abstract's five
PASS as "four re-run and checked by a second runner, one a pin without
its run"; the nature prose names rows 1a, 2b, 2c and 9 as re-run; the
prediction paragraph "pinned, run and re-run by the second runner";
the record appendix's rows of Born's rule, the lattice Gleason,
Tsirelson's bound and Malus "measured and replicated" with the block
named; the caption's rule restated (a run with its line reads
"measured and replicated"); a bibitem for the document; Reproducibility
names the re-runs' tree. NATURE row 2c restated on main (PR #578): the
paper's row 2c carries [1.917, 2.012) with the split at N = 32 and 128.
The other "measured once" labels (series C, E, K, G2, L7, H, R, the
crowd worlds) stay until round 2. Referee round 42, the cleanliness
round over the whole paper (the Boss's seven items): ten findings,
all applied: the abstract's "run and replicated"; the Method's "every
registered run" with the three crowd runs named as drafted; Kepler's
row 58 restated to its amended pin (784 in [714, 855], 392 in [357,
428], 24.8 and 12.4, -81 +- 15 under form B's pace; record 347); the
30 against 31 standard errors of N = 256 stated with both sources (a
tree disagreement between checks/s_of_n.txt and 24.3/24.4, reported);
Bohr's energy row to 26.5's standing (an identity of readings, the
transition not reached); the not-claimed list's "not a prediction of
nature's S" qualified by the one prediction at a power of two; the
abstract's "(pinned, not run)" on Kepler alone; the figures'
fingerprint 731d0f56c9f9 named as figures/summary.json's; the unused
POSTULATE standing said so; the letters with a second meaning named
in the head table. PASS on the labels (every replicated label in a
round-1 block, every "measured once" outside), the commits (19 hexes,
every one an ancestor of HEAD or a register fingerprint), 60 numbers
traced, the counts (44 rows of Table 1; 22 differences; 21 nature
rows; P1 to P10; six places) and section 26 (none of the ten claimed).

## Wave 21 (2026-09-21): series T, the clock's word, both readings and no choice; the series letters; row 3 of the differences

The Boss's orders of 13:25Z to 13:35Z: (b) series T (PR #587, merged
at afb533a8, the register's entry "T, the clock's word", the physicist's
pins before the run): one passage in the clock's-redshift paragraph in
the greats' form and one row (23) in the differences table, labelled
measured once, both readings and no choice (the presence clock 1.3000
at 3 and at 6 Links alike; the age clock 2.6517 and 4.1500, the ratio
1.907 for the pinned 1.909, the continuum's 2.000; the GPS
ground-to-orbit shift 45.7 us per day against Ashby's 45.7 under the
age word, 28.3 under the presence word); the clock_age note's bibitem
back, Ashby 2003 added, the register bibitem names series T. The series
letters as the Boss fixed them: the reader S, the clock worlds T, the
lamp in a crowd U and the cluster V (U and V pending their retitling
PR, said so). Row 3 of the differences reworded as the auditor's round
6 found (the theorem's own N = 16, 32 and 128 with S = 3, 3 and 23/8;
the escape "a power of two at or above 512, or 64 or 256"); the round
itself is not on the tree's log, so it is not cited, and the row cites
Theorem th:bell. Main moved to 12ff2fb1 during the wave (PR #591):
NATURE row 12, the clock's field at two distances (series T, both
words), is the register's row now, so the paper's confrontation table
carries it as row 12 (PASS under the age word, FAIL under the presence
word, the law's default; the word the owner's choice), the tallies
read twenty-two, the abstract carries the row in one clause, and the
differences' row 23 written first is withdrawn; Pound and Rebka 1960
added. Referee round 43: one finding (U and V are the clock note's
letters, not the register's), applied; his note applied ("at first
order" dropped from the series T passage); everything else PASS; his
word for the PR body after the fix: CLEAN.

## Wave 22 (2026-09-21): the owner's word on the clock, entered as an assumption

The owner to the coordinator (about 14:00Z, translated): "I said the
age moment, but this is added to the paper as an assumption, right?"
Yes: P9 (the rules chosen among few) gains the clock's word, the age
moment, the potential's form M / r, with the alternative (the presence,
M / r^2) named and what refutes it on the form (series T on the
GameBoard; nature's clocks between two heights follow the potential);
the series T passage says the word was chosen and entered as an
assumption, not a derivation; row 12's verdict cell reads PASS under
the age word "by the owner's word (an assumption, P9)", the presence
word the alternative's FAIL; the abstract's clause "under the clock's
word assumed, the age moment"; the nature prose and the differences'
sentence likewise. The record number is cited when it lands; the
register's row 12 is the physicist's to restate. Referee round 44
(four findings, all applied): P9 and the series T passage say what the
law as built counts today (the presence by default, the age moment per
table entry, BEAM_LAW section 3) and that the owner's word makes the
age moment the law's word with the engine's default to follow; the
"What departs" and "What is delayed" passages reconciled to it; P9's
heading says the ledger does not yet carry the clock's word; the notes
applied (I4's wording, the comma series). His word after the fixes:
CLEAN.

## Wave 23 (2026-09-21): the external reviewer's findings (batch #577, F01 to F18; issues #544, #548, #549, #553, #555, #556, #557, #565, #586)

The owner's independent testing agent reviewed main.tex at d17af9b9 (issue #577's comment of 13:21Z, F01 to F18) and the focused issues. The Boss's order of 14:12Z: each finding gets one disposition, FIXED at a commit, NOT ACCEPTED with the reason, or STATED AS A HYPOTHESIS. The verified findings and their dispositions (the commit is this wave's):

| Finding | Issue | Disposition | What the paper now says |
| --- | --- | --- | --- |
| F01 the universal 181/64 | #548 | FIXED | verified with the repository's tables (checks/s_powers_of_two.py): 181/64 at 512 to 8192, 5793/2048 at 16384 and 32768, the fixed-table limit 186034/65773; the prediction restated as the exact function of N_phi and N_t with its value on the registered range; the abstract, the stands-above item, the Bell section, the not-claimed list, the differences' row 2 and the prediction paragraph; the per-setting deficits given (725/1024 and 723/1024 at 4096); "five times the precision"; the non-powers of two not excluded by experiment but by declaration; Poh's optimized settings named |
| F02 the 1/(2N) bound | #544 | FIXED | a cell within 1/N (two cumulative rungs each within 1/(2N)); the counts 21, 22, 21 at three equal weights; "nearest integer" withdrawn; the Born paragraph, the ledger, the stands-above item, the differences' row 20, the record appendix |
| F03 the non-local gather | #577 | FIXED | P6 names the pair's click as the law's one non-local operation with its state in the apparatus's list |
| F04 Gauss at every instant | #549 | FIXED (restricted) | exact at every instant for a steady source after the front; the varying source carries the transit term (25.4's continuity with the row amount as density); the stands-above item, Table 1's row, the continuum's row 1, the record appendix |
| F05 the dwell T_D/Q | #565 | FIXED | tau_L the radial residence factor T_D/(N_l |D|) = 1/v_D (1.72 on a heading, sqrt 3 in the limit); the per-Link dwell T_D/(S_1 N_l) named apart; the shell's coefficient depends on its geometry; the glossary |
| F06 the wave/Poincare limit of the block | #577 | STATED AS A HYPOTHESIS | the continuum table's row 16: DERIVED for a plane-wave stream (4.1), a hypothesis for arbitrary row data (17.1 conditional) |
| F07 the uncertainty's identification | #553 | STATED AS A HYPOTHESIS | Table 1's row: the transform's identities on the phase circle are exact; the reading of the circle as position and its transform as momentum is an identification assumed (22), Kennard's form its limit under it |
| F08 the h against hN dictionary | #553 | OPEN to the derivation mathematician | the paper's E = hs = (h N_phi) f, hbar = h N_phi / (2 pi) and lambda = h/p need one calibration; not changed here without the mathematician's dictionary (24.1's row for h) |
| F09 the quadratic form "forced" | #577 | STATED AS A HYPOTHESIS | the theorem under the added measurement axiom (the balanced splitter's conservation for every pair); the built tables break phase invariance by their rounding, the theorem the exact form's; the abstract's "forced" softened |
| F10 the PASS tally | #555 | FIXED (labels) | row 2c: PASS on the power, Sinha's kappa a different observable not computed (compatible, not the same observable); row 11b a compatibility from a pin, not a measurement; the abstract already sorts the five |
| F11 Poh's settings and the precision | #577 | FIXED | five times the precision, the optimized settings and the detection model named, the identification assumed |
| F12 the neutrino's quantities | #556 | FIXED | row 8c: the heavier state of the atmospheric splitting at least 1e-7 (the lightest unbounded below), the effective beta-decay mass at most 1.6e-6; the verdict FAIL on the splittings stands; the differences' row 16 likewise; the physicist re-reads NATURE row 8c |
| F13 the division and the unwrapped count | #557 | FIXED | the division toward zero with the signed remainder (Euclidean for a non-negative accumulator); the bijection stated; the closed form named the unwrapped count |
| F14 bounded torus, unbounded counts | #577 | FIXED (stated) | P1: a world whose counts would exceed the declared bounds is refused at load; no overflow rule inside a run |
| F15 the entropy and the second law | #577, #586 | FIXED (restricted) | the identity is the outcome's coarse graining: bits read plus bits not read of u, u kept in the world's list as a GameBoard diagnostic; no second law claimed (an identity, no ensemble); Table 1's rows, the stands-above item, the continuum's rows 12 and 23, the record appendix |
| F16 the derived couplings' supplied physics | #577 | FIXED (stated) | the redshift's calibration a_tau = GM/(r c^2) assumed, the clock's pair and the width not fixing it |
| F17 the gas's closure | #577 | FIXED (stated) | the continuum table's caption: every "in form" row of the gas rests on the product-measure closure of 25.5, whose error is not bounded |
| F18 novelty | #577 | FIXED (stated) | the Introduction's sentence names the supplied structures stored as integers (the tables, the pair's joint contraction, the energy's square) |
| the isometry's zero vector, T > 0 (#557) | #557 | FIXED earlier | the lemma states C_K > 0 (wave 17); the split theorem's vector: "every integer vector" now read with A > 0, stated in this wave if the referee asks |
| the submission metadata (#557) | #557 | OPEN, the owner's | the AI-tool line, the release tag and the arXiv identifiers are the owner's at submission (the Reproducibility section says so) |

The check checks/s_powers_of_two.py is added with its output; NUMBERS.md carries the new numbers. Referee round 45 (six findings, all applied: the differences' row 20's departure per cell; the entropy row's one standing; P1's overflow rule as the engine has it, refused at load where the static budget covers it and loudly at the step otherwise; the abstract's "at the powers of two"; row 3's 136 of 512 excluded under the identification, the rest surviving, the power of two a declaration; the Bell section's phrase bounded through 8192; his notes applied: the continuity identity holds for every source, the flux-equals-release form for a steady one; the energy's square the covariant readings'; Poh's angles not on the tree, dropped). His word after the fixes: CLEAN WITH NOTES. Then one reply per focused issue with the disposition and the commit.

## Wave 24 (2026-09-21): the Boss's three messages that crossed wave 23 (14:16Z, 14:22Z, 14:26Z)

(1) The click definition says what a non-absorbing read is (a deferred
offer keyed by the labels, gathered at the record's one click) and that
a read, a rotation and a second read taken as two outcomes in time is
not modelled (issue 584, the architect's disposition). (2) The Bohr
paragraph says a transition is one-shot (`become`, once, no product
change of its own) and that an excited state that relaxes has no hook
(issue 585). (3) The orbit's inward push: the physicist's note
(docs/designs/orbit_read/NOTE.md, on the tree at 75efe7b5) in Kepler's
row of the table, the differences' prose list and the record appendix,
with its bibitem: the fan's Manhattan mean 1.287 (4 / pi uniform), series
C's C = 1 on the six headings, the same form and a different constant.
(4) The mathematician's exact numbers for F01 (PR 594, pending on main):
the check extended with the closed form on the fixed correlations beyond
the tables' bound, 11585/4096 at 65536, 46341/16384 at 131072,
370727/131072 at 2^20, the distances from Poh (+1.05 on the plateau,
+2.01 at 16384 and 32768, +1.5 to +1.65 beyond), the same values the
mathematician reports; the prediction paragraph and the Bell section
carry them. Not done, waiting on the tree: "record 394" for the owner's
word on the clock (cited by date until PR 581 lands, per the rule);
NATURE row 8c's 9.8e-8 (PR 598); Malus at 22.5 degrees run (A12's
registration and 24.3 row 4's turn to "run"). Referee round 46 before
the commit.
Referee round 46: FAIL on three lines, fixed: the closed form cited to
the check alone (24.4 on the tree lacks it); the distance from Poh one
number, 1.05 standard errors, in the abstract, the 24.4 paragraph, the
prediction paragraph and NUMBERS (the Bell section keeps its local
"standard deviations" beside the 152 and 30, a pre-existing mix of the
two words across sections, noted); the orbit note's 1.29 labelled host
arithmetic, no run, "registered" kept for the orbits alone. His notes
applied: the auditor's pin 1.00 +- 0.15 apart from the register's
C = 1.00 +- 0.10 on a fan (the refuted one); the push constant as the
register's letter in typewriter (plain C is the cosine table's entry);
the ring means 1.13 to 1.43 at r = 8 to 28; the read's selector keyed
by the labels at the read and applied at the gather to the labels as
the rotation left them; `become` turns the event into the `into`
family, its products released, the key consumed. CLEAN WITH NOTES.

## Wave 25 (2026-09-21): main be194aca merged; what it landed taken into the paper

Merged after wave 24's push: PR 594 (24.4's closed form and the plateau's
domain, bell_plateau.py, now cited beside the paper's check; 24.3 row 1's
29.6, so N = 256 is 30 by both), PR 598 (NATURE row 8c: the heaviest
mass state at least 9.8e-8, the lightest not bounded below; the paper's
row 8c and the differences' row 16 follow it), PR 592 (ENGINE's readings
by type: the non-absorbing read a deferred offer, cited in the click
definition; the three Malus worlds at 22.5 degrees registered under A12
extended, the tables' rungs met exactly: the consequences' Malus row,
NATURE row 9, the differences' row 4 and the record appendix say run,
measured once), PR 600 (wave 23). Reproducibility: main merged at
be194aca. Still waiting on the tree: record 394 (PR 581; the owner's word
cited by date), wave 22's PR 596, the replicator's round 2, the
retitling of series U and V. Referee round 47 before the commit.
Referee round 47: FAIL on one stale row, fixed: the differences' row 1
(N = 256: 30 standard errors, 29.6, by the check and the derivation's
24.3 row 1 and 24.4; the 31 the deficit from the bound over the error).
His notes applied: NATURE row 9 and 24.3 row 4 on the tree not yet
restated for the 22.5-degree run, said in the paper's row 9; the Malus
note's bibitem says run since as A12 and A12 extended; "standard errors"
at N = 256 in the Bell section. CLEAN WITH NOTES.

## Wave 26 (2026-09-21): main e2faf65c merged; replications round 2 (part 1) and the series letters

PR 601: series T, the cone (L7), the (3, 4) split at N = 32 and 128, the
two slits (L2, L2b) and the click's gate set REPLICATED (19 worlds, no
FAIL): the clock sentence, NATURE row 12, the register paragraph, the
flight row and Young's row say measured and replicated; the
replications bibitem and Reproducibility name round 2's trees, 5fbd0c7
and afb533a for series T. PR
595: a lamp inside a crowd is series U and a cluster of crowds series V
in the register's documents; "its retitling pending" dropped. A slip on
the tree, reported to the Boss and not edited here: the same PR
retitled examples/events/README.md's hand series from P to U and c
measured from Q to V, while docs/EXPERIMENTS.md keeps "P, the hand" and
"Q, c measured", so the README now carries two series U and two series
V; the paper keeps P and Q for the hand and c measured as the
experiments register has them. Reproducibility: main merged at
e2faf65c. Referee round 48 before the commit.
Referee round 48: FAIL on two lines, fixed: round 2 ran on two trees
(5fbd0c7; afb533a for series T alone), said in the bibitem and in
Reproducibility; a NUMBERS row for round 2 as a whole. His notes
applied: row 12's replication moved out of the five PASS's parenthesis;
the 48 images not run on slits_huygens, said in Young's row and the
bibitem; the clock's word register's map pending; main b7ddf93f (the
open-problems note on Lorentz, docs only) merged, Reproducibility
follows. CLOSURE.md, the closure list for the arXiv cut, added on the
Boss's order of 14:47Z (referee round 49). CLEAN WITH NOTES.

## Wave 27 (2026-09-21): the figures in black and white (the owner's word, "regenerate")

The owner's word: colour figures are not wanted, black and white only.
The five drawn figures (the Mach-Zehnder counts, the two slits, the pair
at N = 64, S(N), the octahedron) are regenerated by figures.py and
octahedron.py from the same summary.json and the same checks, every
series told apart by its fill (black, white with a hatch, grey), its
marker (a filled circle, an open square, an open circle) or its line
style (solid, dashed), never by hue; the Poh band pale grey; the links
of the PDF black (hyperref's allcolors). The 48-permutations figure was
already black and white (0.9 percent coloured pixels, the gallery's
markers). No number moved: the scripts' data paths are unchanged (the
diff is colours, hatches, markers and a --png preview option). The PDF
compiled here with pdflatex (three passes, clean) is 80 pages, not the
105 of the word-count estimate; the Boss told.

## Wave 28 (2026-09-21): the one non-local operation and no-signalling's scope in the abstract (the reviewer's point 3, the owner's "make sure it is resolved")

The reviewer: P6 and the causal section state the pair's gather from
both settings (transparent), the title should reflect the exception,
and no-signalling is proved for equal weights only. In the paper: P6
names the one non-local operation (wave 23); the theorem's scope
paragraph and the "What is not claimed" item say no-signalling is
proved for the equal-weight pair and open beyond it; the abstract now
says both in one sentence ("Local at every Node, the law has one
non-local operation, the click of a pair, a gather of one record from
both settings; no-signalling is proved for equal weights, open
beyond"), with cuts to stay under 1920 plain characters (1917): the
pace's parenthesis, "run and replicated at 512 and 4096" (the
replication stays in "four replicated"), the closing "every claim is
measured, proved, assumed or open", two shortenings. The title is the
owner's decision (record 275) and is not changed by the writer; the
question is put to him with a variant. Referee round 50.
Referee round 50: CLEAN WITH NOTES; applied: "on paper" restored for the
covariant readings, "the rule gives" for 5793/2048, "From this law"; the
abstract at 1917 plain characters. His reading of the title: the
abstract's fourth sentence states the exception, so title and abstract
together do not mislead; alone, the title lacks the qualifier, and the
title is the owner's (record 275).
Wave 28 extended on the owner's issue 621 (the first-reader review of the
compiled PDF, six points) and the Boss's order of 16:10Z: (1) a paragraph
and Table tab:assumptions after the postulates, what Eq. (1) determines
and what its rates and tables supply, per main recovery the assumptions
that force it and the freedom left, identities apart from predictions;
(2) the scope table's four rows carried in that table (c a bound and a
chosen wall; Born the splitter axiom and the harmonic freedom; Newton a
shell mean, the spatial run unrun; the uncertainty relation conditional
on the identification); (3) the abstract's sentence (above); (4) after
the register paragraph: every verdict the law's beam-v1 at the merge
commit unless a hypothesis's identity is named, a hypothesis's PASS
never changing the law's FAIL, incompatible predictions apart from
capabilities not reached, PASS counts no evidence against a decisive
FAIL; covariant-readings-v1 built and run (series S) in rows 4a, 4b,
the Lorentz section and the consequences' rows, the law's rows FAIL,
the identity's PASS on its domain; (5) the prediction paragraph's
domain at its first occurrence with the grains, the settings and the
prepared state, the allowed family, the compatibility not an advantage,
a rejection criterion at five standard errors, no new physical data;
(6) every table a longtable with repeated headers (16 tables): the
compiled PDF 94 pages, no overfull vertical box (the 80-page build lost
6051 points of the consequences table and the foot of the register).
Also P10 restated by the Boss's decision (record 435; the Born note's
line), series G2's status by date (record 408 to follow). The title is
the owner's; put to him. Referee round 51.

## Wave 29 (2026-09-21): the cut to 40 pages (the owner's word, "shorten the paper to 40 pages; keep what is certain"; no referee)

The owner's word supersedes record 373's arXiv-first full paper and
cancels the referee rounds. The manuscript is cut from the long form
(commit c15c1174, 97 pages) to what is proved, measured and, where the
second runner's line exists, replicated: Part I the law (the postulates,
the assumptions table, Eq. (1) and its operations, the group, the
state, the components, the two blocks, the read-out, the five
statements, the inputs, the symmetries and the theorem of the 24);
Part II the table of consequences in short (standing, formula,
derivation, check; the status column left to the long form), Newton and
Coulomb, the delay field (Poisson, the retarded wave equation, the
clock's redshift with series T replicated, the crowd worlds in one
passage, light in one paragraph), the lattice Gleason and the
confrontation register; Part III the click model (without the
plain-words and history paragraphs and the time-of-flight bounds), the
four theorems, the measurements (the table, the two-slit and S(N)
figures), the Bell value, the causal anatomy, what is new, what is not
claimed, the hypotheses in one paragraph; Part IV the one prediction
(the differences' table left to the derivation's 24.3), the limits
(without Young's fan paragraph), Lorentz (the theorem, Newton, the
built hypothesis with series S, the figure, the decision), the
literature, Reproducibility (naming the long form's commit), the AI
line. Dropped to the tree: the special cases, "what follows in order",
the figure of the 48, "where the law's form stands above", the dark
sector, the founding formulas one by one, flow and heat, the
differences' table, the record appendix, the families' appendix, the
glossary; the repository bibitems shortened to one line and the uncited
ones removed. Compiled: 40 pages at 11pt, no overflow, no undefined
reference; every number kept is one the long form carries with its
source in NUMBERS.md. The full text stays in git at c15c1174.
The Boss's procedure for the same word (record 454): the referee retired
in skills/paper-coordinator/SKILL.md in one paragraph; the cut by one
criterion, (a) a rule of the law as the repository states it, (b) a
derivation closed in DERIVATIONS_BEAM with its row cited, (c) a
registered run with its fingerprint and detector readings, (d) a
declared hypothesis or a stated non-claim; three further cuts under it:
the Lorentz decision paragraph (a decision under review), the causal
anatomy section (an interpretation), the literature essay to one
paragraph; the uncited bibitems removed (72 remain). Where the cut
departs from the Boss's first reading: the confrontation register is
kept in full (its FAIL rows are registered detector readings, criterion
(c), and the owner's "certain" includes the failures); the one
prediction is kept (a derivation, 24.4, with registered and replicated
runs at 512 and 4096); the founding formulas one by one are not kept as
a section (their closed rows are in the table and the Gleason section);
the glossary is not kept (the notation table stands). 40 pages.

## Wave 30 (2026-09-21): the Boss's twelve items on the cut, from the chief physicist's and the mathematician's certainty lists (record 457's order)

The criterion of the cut (record 454, on the owner's "keep what is
certain"): a passage stays only as (a) a rule of the law as the
repository states it, (b) a derivation closed in DERIVATIONS_BEAM with
its row cited, (c) a registered run with its fingerprint and detector
readings, or (d) a declared hypothesis or a stated non-claim. Done on
the cut: (1) no conditional derivation remains (the flow rows to one
NOT REACHED line; Compton and E = mc^2 one line each under
covariant-readings-v1; the built identity stays as (d) with series S's
readings and its one-axis domain, an orbit refused); (2) form B out
everywhere (P9 states the drive as built on main, per axis; the
table's legend, the Newton paragraph, the click model's parenthetical,
the Lorentz domain); (3) optical-v1 one line, designed and reviewed,
not built; the bending keeps the registered 0.000 against nature's
1.75 arcseconds, cited to the derivation's 24.3 row 14 (the cut's
"the register's row 14" was the long form's table row: a citation
slip, fixed); (4) the table of consequences: every pinned or
unchecked row is one non-claim line without a number (Bohr's
condition, Kepler, Compton, Newton's geodesics, Bradley, Schroedinger,
the single-opening spread, the periodic universe), the HYPOTHESIS rows
one line with the identity's name and status (source-velocity-v1,
expansion-v1, optical-v1, covariant-readings-v1, massive-rows-v1),
Heisenberg's arrays and Dirac's spin added as NOT REACHED; (5) the
register's pinned rows (4a's law reading, 5b, 6, 10, 11a to 11c)
carry "not run" in the reading column and no number, every FAIL a
FAIL, the BOUND rows and 4b's 0.2636 unchanged; (6) Planck and de
Broglie cite 24.1 row 25 (one constant h = h_q N = h_A); Bohr's
energies, Heisenberg's arrays, Schroedinger and Dirac one non-claim
line in "What is not claimed"; Born, Young (L2b) and Tsirelson stay
with their fingerprints; (7) the uncertainty relation: the circle as
position and its transform as momentum a stated identification, the
finite-Fourier bounds mathematics on Z_N, the Weyl relation an
identity, the single opening's 0.886 out (a pin, not run); the row
HYPOTHESIS; (8) Lorentz: the theorem restricted to the plane-wave
stream (a hypothesis for arbitrary row data), the decision in one
sentence (record 270), the law's three rows stated (4a a pin, not
run; 4b registered; the pace on main), the seventh-operation narrative
and the round-trip pins out, the contraction one line; (9) no general
push constant is stated (C = 1 only as series C's reading in the long
form; the cut states none); (10) no trace of the dark sector's
"missing content"; (11) "What is new" item 4 kept, restated to what
Remark rem:nodispersion proves (the periodicity of a local linear
scheme's dispersion relation), the coordinator's call for the
mathematician; (12) the optical-metric limit sentence and the Young
"partial third" out. The families' tables and the glossary stay on
the tree, cited by path (the families' audit; TERMINOLOGY through the
notation table). The Boss's "J4's registered numbers" for the law's
FAIL rows: the register's J4 worlds are series S's, run under the key;
under the law the muon in flight is a pin (row 4a), so the row carries
no number; the dispersion the Boss wrote, v = p / (m + p / c), is form
B's, and the law on main reads |p_a| / (N_l N_w M + |p_a|) per axis.
The Boss's "Young's fringes (series L2, 36.5 / 60 / 83.5)": those
integers are the slits_matter pin under massive-rows-v1, not L2's
readings; L2b's registered fringes stay (the bright pixels 19 to 51,
the dark 0 to 3). Main b6ab1bb3 merged (records 367 to 453 on the
tree: the owner's clock word cited as record 394, series G2's
replication FAIL as record 408). The PDF: 38 pages.

### Wave 30, addenda 1 and 2 (records 458 and 459): the physicist's five and the mathematician's five

(13) Series T stays "replicated": REPLICATIONS.md on main at b6ab1bb3
carries the Replicator's block for series T (afb533a, every world
bit-exact); NATURE row 12's own label ("measured once, the replicator's
round pending") lags the block. (14) The crowd-clock worlds are cited
by their pages' titles (Series U: a lamp inside a crowd, still and
moving; Series V: a cluster of crowds read by one detector; Series S:
a reader inside a crowd), their register entries drafted and not
registered; the covariant readings by the register's entry "S, the
covariant readings" everywhere (the letter alone nowhere). (15) The
S(N) figure shows the powers of two 64 to 8192 only (figures.py; the
runs at 64, 1024, 4096 as open circles); the Bell section and the
prediction lose the multiples-of-8 statements (91/32, 181,152, 184,
136 of 512, 3016, S = 3 at 16 and 32); Theorem th:bell keeps its
exact count of the multiples of 8, a proved statement. (16) The
assumptions table checked row by row: every row's "assumptions that
force it" is a postulate, a declared input, a theorem of the paper or
a section of the derivation (P1, P4, P9; P3, P5; 24.2, P8; th:gleason,
P10; N_t and the labels; 22's identification, assumed; P8, P9, 24.1
row 25; the calibration assumed; the coarse graining); the five
statements are the law's rules (I1 to I5); both kept. (17) fig:square's
caption names covariant-readings-v1 and says "a hypothesis beside the
law". (g1) meeting-v1 one line in the hypotheses paragraph as a
registered hypothesis (K under the meeting: the centroid -1.790,
-4.359, -2.301 pixel, DETECTOR), not coupled to optical-v1. (g2) The
rows' pace untouched. (g3) The DERIVED rows keep their series and
keys; the FAIL rows their registered readings. (g4) The notation
table kept; the glossary cited by path (docs/TERMINOLOGY.md). The
families: P8 says every world's families are the shipped definitions
(75 families in 27 entities, examples/events/entities/families.json)
plus the 23 inline declarations (the audit's count; the Boss's
addendum said 21), cited to the audit with family_table.out. (18) The
three labels: Kepler and Bohr's condition OPEN, the single-opening
spread OPEN without the 0.886, Compton one line without numbers (as in
the wave). (19) Form B's last two mentions in Part I out (the
components paragraph, the cap sentence). (20) th:bell's statement
"through 8192" with the run and computed N named. (21) Row 4a's
reading keeps J4's registered rest reading (the 64th self-creation at
64, j4_muon_rest); in flight a pin. (22) "What is new" item 4 claims
only the first half of rem:nodispersion (no rule reads a phase into a
step); the remark attributes "no local linear wave scheme is both" to
Meyer's theorem. The PDF: 38 pages.

### Wave 30, the physicist's four corrections on 6abe65ce (record 477; the mathematician agreed with none)

(1) The differs head counts the eight registered FAILs (1b, 2a, 3, 4b,
7b, 8a, 8b, 8c), the four by a pin without its run (4a, 5b, 11a, 11c;
the physicist's line named three, 11a is the fourth "FAIL (pinned)"
row) and the one under the presence word (12). (2) Row 11b's verdict
reads "not run; the pin's exponent within the measured", no PASS; the
tallies follow: four PASS (all replicated), twelve FAIL, two BOUND, two
NOT YET, one pin without its run (the abstract and the register
paragraph). (3) P8: the 23 inline declarations, 21 of them differing
from the shipped definitions or naming a family the definitions lack.
(4) The assumptions table's uncertainty row: "an identity on the
circle; the physical identification a stated hypothesis (22, assumed)".

### After the merge (2026-09-21, about 23:30Z): the conditional derivations the cut removed are hypotheses on the tree

The Boss's assignment under the owner's GO (its record to follow): every
conditional derivation the cut removed (record 454's criterion) has one
status on the tree, a declared hypothesis outside the law, docs/HYPOTHESES.md
entry 27, each with its condition, what closes it and what refutes it;
DERIVATIONS_BEAM 24.5 links to it. The paper is unchanged: it carries
them as HYPOTHESIS or OPEN rows without a number since wave 30.

### The bijection theorem restated on the GameBoard alone (the owner's word, 2026-09-21, about 23:50Z)

The owner's question: why lean on the apparatus's record if only a
detector measures? Theorem th:bijection and its proof no longer lean on
the engine's event record (a host diagnostic read by no rule): the
interval is injective on the rows' weights, multiplicities and phases,
the GameBoard's state alone; a row's age is its count since its last
event by Definition def:rules, so a split, an event, restarts it at 0
by definition and loses nothing; the click is the one deletion. The
read-out paragraph of Part I says the same. No number moved; 38 pages.

### Newton and Poisson are checked on GameBoard readings, labelled so (the owner's word, 2026-09-22, about 00:30Z)

The owner: "Make sure the law is clear. Newton and Poisson measured after
a detector. Nobody measures the board. Make sure the law is clear in the
Highlights." The Highlights carry the rule (records 277 and 281); the
paper applied it to the register's rows but not to the checks of series
C and E, which are probe readings of the GameBoard (no detector in those
worlds). Every such check now says so: the consequences table's rows for
Gauss, Newton, Coulomb, Poisson, the field's Gauss law and the redshift;
the Newton and delay sections' "registered" sentences; the rings table's
caption; the table's legend. Newton's and Poisson's measurement after a
detector is a run not made, named as such; the owner's word sent to the
Boss for Highlights 5.4 and the register's labels.

### No probe reading of the GameBoard in the paper (the owner's word, 2026-09-22, about 00:50Z)

The owner: "No probe reading that samples the board in the paper at all;
it has no meaning without a detector." Every series C and E number left
the paper: the rings table, the Gauss, Newton, Coulomb, Poisson, field
and redshift checks (now "no detector reading registered; the run after
a detector not made"), the equivalence principle's, the third law's and
the retardation's integers, the Coulomb coefficients, the two fields'
constants and the strong-field rate ratios; the derivations stand as
derivations, and series T (a detector's reading of the clock's field at
two distances) is the field's one measurement. Reproducibility no longer
names series C's fingerprint.

## The thirty-page plan (the owner's instruction of 2026-09-22, its record 573; step 1 of the Boss's order, 2026-09-22, 00:25Z)

The owner's instruction (translated by the Boss): thirty pages in all,
twenty-three of body, four of references, three of appendices; the title
and the abstract counted, no title page; the paper built around the
general formula, its implementation in the simulator and the physical
formulas derived from the model's rules; the introduction says how the
work with the simulator led to the results and the derivations; the
general formula on the first page with a short explanation, its full
definition in the next chapter; every central derivation states its
relation to the law. This section is the plan only (step 1); the cut
(step 2) waits on the Boss's word after the mathematician's and the
physicist's checks of the statuses below. The base is head b684ba0b
(37 pages after the removal of every probe reading; the Boss's order
named 9e1dbbef's 39). The measurement rule throughout: records 281, 562
and 564 (only a detector's reading is a measurement; no GameBoard number
stands as one; every external entity is a detector or an emitter).

### 1. The page map: today's 37 pages onto the owner's 30

| Pages | The owner's content | From today's paper (its pages) | What unites, what is cut, what moves | Expected |
| --- | --- | --- | --- | --- |
| 1-2 | abstract and introduction: the general formula, the physical idea, the simulator's role, the new contribution; the map of results (proved, shown numerically, open) | the abstract and the introduction (p1-3: "One law", "What this paper carries", "Method", the notation table) | the abstract to about 1200 characters; Eq. (1) printed on page 1 with four lines of meaning (section 4 below); one new paragraph, "How the simulator led to the results" (the runs registered before the text, the pins, the second runner, the derivation record: the path from a run to a derivation, from PLAN.md's history); the map of results as one short list (proved: the theorems; numerically: the detector readings of pages 19-21; open: Newton's and Poisson's detector runs, the muon under the law, the harmonic constants); "What this paper carries" cut; the notation table to appendix B | 2 |
| 3-5 | the law and its implementation: variables, operations, rates, walls, neighbourhood, time; rules apart from parameters and initial conditions; a hand-worked update; its realisation in the code | Part I (p4-10): the postulates P1-P10, the assumptions table, Eq. (1) and the six operations, the state, the components, the two blocks, the read-out, the five statements, the inputs | the postulates and the five statements united into one definition list (the Node and its six Ports, the interval, the row and the body as the two kinds, the accumulators with rate and wall, the six operations, the click as the one read-out, the least-rank click P10 as an axiom of the apparatus); the assumptions table cut (each row's content returns in its formula's five-step path); "the inputs" becomes "rules, parameters, initial conditions": the world file's families, widths and apparatus as parameters and initial conditions, the law as rules; NEW: the hand-worked update, a row on a heading: rate 2 S_1 N_l = 128 against the wall 2 T_D = 220 (T_D = floor(sqrt(3) x 64) = 110), the accumulator 128, 256 (an event, 36), 164, 292 (an event, 72), 200, 328 (an event, 108), 236 (an event, 16): Links at the intervals 2, 4, 6, 7, the pace 128/220 = 0.5818 Links per interval, the heading's pace the paper already carries; and how the code realises it (the step of an interval in docs/ENGINE.md, the accumulator per component, the carry as the event; the module and function ENGINE.md names) | 3 |
| 6-7 | geometry and symmetries: the directions, c = 1/sqrt 3, the geometric bound, the implementation's choice, what a detector measures | the group paragraph and th:group (p9-10); prop:pace and rem:nodispersion with the octahedron figure (p22-23) | united here: the 48 signed permutations and the 24 rotations (th:group, statement and the two-line proof), the fan of directions and the flight table (D, tau), the wall T_D as the implementation's choice among few (P9), the Courant bound and the lattice Boltzmann sound speed as the geometric bound (the literature in one sentence), no dispersion by construction (the remark's first half); what a detector measures: series Q's 290 of 290 face clicks at the derived interval, Node and face, the pace 0.5718 to 0.5893 (DETECTOR), series L7's cone, two rows at the same age 29 (DETECTOR); the isotropy bound on N_l from nature's 10^-18 (row 5a); the octahedron figure kept small | 2 |
| 8-10 | conservation and the forces: conservation to flux to Gauss to 1/r^2; the coupling assumptions, the shell mean, the constants' standing | the books (I5), the Newton and Coulomb section (p14-15), the INPUT rows of the table | the chain in five steps: the books exact at every operation (P3, P5), the walk as a translation, Gauss exact for a closed surface, the shell mean over the fan and Gauss's circle problem, the bilinear push, Newton's inverse square with G = K eta / (4 pi N_w), the equivalence principle and the third law from the step rule, Coulomb with the same constant and the charge as a declared rho; the coupling assumptions stated (two additivities, 24.2); the constants' standing (G a formula of the release rate, the fan and the width, the width an input; rho an input, the hierarchy not the law's); the retardation and the saturation as the two departures; no detector reading of any of it, said once; the drive as built on main (per axis) | 3 |
| 11-12 | the delay field: the age field, the delayed potential, Poisson, the boundary assumptions, the relation to clocks | the delay section (p15-17) and the light paragraph | the two fields of one stream and the retarded wave equation (5.1) with the assumptions named (the dense fan P >> r, the open box, the shell mean); the clock's redshift at first order under the calibration a_tau = G M / (r c^2), assumed, and the second-order difference (no horizon); the relation to clocks measured after a detector: series T (the form at two distances, 1.907 for the pinned 1.909 against nature's 2.00, replicated; row 12) and the crowd-clock pages (measured once, entries drafted); light in two sentences (no optical metric; series K's 0.000 DETECTOR against nature's 1.75; optical-v1 a hypothesis with gamma an input) | 2 |
| 13-16 | measurement and the quadratic form: the click, the splitter assumption, the central proof; Planck, de Broglie, the uncertainty relations, with what is derived and what is defined | the click model (p21-25 less the pace parts), the lattice Gleason (p17-19), the Planck and uncertainty rows | the record as an element of the group ring, the split, the rotation, the merge, the evaluation at the roots of unity, the ladder and the click (def:row, def:rules, def:click, in one page); the splitter's conservation as the measurement axiom beyond the six operations, stated as an assumption; th:gleason and its proof (the central proof, one page); the harmonic constants not derived and the least-rank click P10 as the apparatus's axiom (definition); Planck's E = h f and de Broglie's lambda = h / p as identities under the declared dictionary, h an input (24.1 row 25: definition or input); the uncertainty relation: the support, entropic and Weyl statements as mathematics on Z_N, the identification of the circle as position and its transform as momentum a hypothesis (F07); the isometry and bijection theorems stated in one line each, their proofs to appendix A; the "in one sentence" and "GameBoard and circle" paragraphs compressed; the tables' rounding (N_t = 256, the norm's window) to appendix B | 4 |
| 17-18 | Bell and CHSH: from weights to counts and correlations, the finite-resolution result, its limit, no-signalling | th:marginals and th:bell (p26-27), the Bell section (p29), the one prediction (p31-32), fig:sofn | the pair's joint weights, the rungs and the counts (eq:joint, eq:rung), E(a, b) and S; th:marginals (exact marginals, the one gather) and th:bell (S(N) exact, 181/64 at the powers of two 512 to 8192, 5793/2048 at 16384 and 32768, the limit 2 sqrt 2 with the bound eq:ebound), with the proofs' decisive steps; the prediction stated here as the law's number (eq:prediction) with its criterion; the comparison with Poh et al. (1.05 standard errors) and the loophole-free experiments moves to page 21; fig:sofn kept at half width or cut (the numbers are in the text) | 2 |
| 19-21 | the simulator's checks and the comparison with nature, separately: (a) the code implements the law, (b) the numerical checks of the formulas, (c) the comparisons with measurements; predictions, results, deviations, failures | the measurements (p27-29), the confrontation with nature (p19-21), the differs section's comparison, the replications | (a) one paragraph: the second runner's bit-exact replications (record 353's rule; series L, T and 15 more worlds REPLICATED), the books balanced at every interval, the engine's inverse interval on worlds without a measured event, the rule's tests (the crossing rule, the rounding at 63/1, 31/1, 125/3 pinned before the run): computations that the code implements the law, not measurements; (b) the representative detector checks of the formulas (section 3 below), one compact table; (c) the confrontation register as one table of the detector rows with their verdicts (section 3 below), the pinned rows in one line ("not run"), the prediction against Poh et al., the twelve failures named as the law's results | 3 |
| 22-23 | discussion and conclusions: what is proved, what the runs support, what the observations support; the limits and the next decisive checks | What is new, What is not claimed, the hypotheses paragraph, the continuum limits, Lorentz, the literature (p29-34) | united: proved (the theorems and the exact identities), supported by runs (the detector readings of pages 19-21, each measured or replicated), supported or refuted by observations (four PASS, twelve FAIL, the decisive three: the unslowed clock, the bending, the deceleration); the limits in one paragraph (Tsirelson as a limit, the cone, the two conservations; not a limit: Lorentz invariance, Einstein's equation); Lorentz in one paragraph (the law's falsifiable row, record 270's decision, covariant-readings-v1 as a hypothesis with series S's face clicks 369 and 345 and z = 0.3674 DETECTOR, its one-axis domain); the hypotheses named in one sentence with HYPOTHESES 27 on the tree; the next checks that decide: Newton's and Poisson's detector runs, the muon in flight under the law, a CHSH measurement at 1e-4, the bending under optical-v1's key against its pins; the literature in one paragraph (the finite kinematics, the lattice gas, the automata, Bohm, PR boxes); fig:square cut (its one equation line stays) | 2 |
| 24-27 | references: the derivations' literature, the methods, the experimental data | the bibliography (p35-37, 92 items) | the literature items kept (about 60: Bell, CHSH, Tsirelson, Gleason, Weyl, Schwinger, Courant, the lattice gas and automata, Bohm, Spekkens, the experiments Hensen, Giustina, Shalm, Poh, Grangier, Sinha, Tonomura, Bailey, Botermann, Nagel, Nairz, AME 2020, PDG, KATRIN, Ashby, Pound and Rebka, Delva, Planck 2018, Riess, Perlmutter, Blondin, Lubin, Tolman, Huxley, Donoho, Maassen, Kennard, Robertson, Shannon, Landauer, Meyer, Bialynicki-Birula, Arrighi, HPP, FHP, Qian, Jarrett, Shimony, GRW, Fine, PR); the repository items (the derivation, the registers, the notes, the designs, the checks) move to appendix C as the reproduction list with paths and the commit; four pages at the class's size (a full page each for three groups, one for the data) | 4 |
| 28-30 | appendices and reproduction: essential auxiliary proofs, technical details, reproduction instructions with a defined code version and the runs' parameters | the theorems' proofs, the notation table, Reproducibility, the AI line, the check scripts | A (1 page): the proofs of th:isometry, th:bijection (as restated on the GameBoard alone) and prop:pace, compressed; B (1 page): the notation table compact, the tables' rounding and the norm's window, the click's rung formula, the tie rule; C (1 page): the archived version (the tagged release after the merge; the commit named), the worlds and their fingerprints (ff5c382d672f, 731d0f56c9f9, 4bf55a62e6fd, series S's 24e0c1ba, series T's afb533a), the check scripts with their outputs, NUMBERS.md as the one source per number, the register's replications, the runners' commands; the AI line | 3 |

Sum: 2 + 3 + 2 + 3 + 2 + 4 + 2 + 3 + 2 = 23 pages of body, 4 of references, 3 of appendices: 30. The figures kept: the octahedron (small, pages 6-7), the two-slit clicks (small, page 20) and S(N) at half width (page 18) if the count allows; fig:square cut. The tables kept: the compact consequences table folds into the five-step statuses of section 2 (one short table on page 2, the map of results) and into the checks tables of pages 19-21; the assumptions table cut; the notation table to appendix B.

### 2. The central formulas, each on the five-step path, with its status and the section of DERIVATIONS_BEAM that proves it

Status words, the owner's: "derived from the update rules implemented in the simulator" (a proof exists), "numerical finding" (a relation found in runs alone), "hypothesis" (a relation under a condition or an identity beside the law), "definition or input" (a relation defined in advance in the model). The five steps per formula: (1) the update rules it starts from, (2) the assumptions and approximations, (3) the decisive steps, (4) the domain and the free parameters, (5) the comparison with the simulator's detector readings and with nature.

| Formula | Status on the path | Proved in | The rules it starts from; the assumptions; the free parameters | Compared with (DETECTOR only) |
| --- | --- | --- | --- | --- |
| Eq. (1), the map per component | definition (the law) | section 0; LAW.md | the accumulator, the rate, the wall, the cap, the carry as the event; the six operations | none: a definition |
| c = 1 / sqrt 3 Links per interval, isotropic within 1 / T_D | derived from the update rules | 13.2, 11.1; prop:pace | the flight table (D, tau) with the wall T_D = floor(sqrt(3 abs(D)^2 N_l^2)); the fan declared; N_l free (a grain) | series Q's face clicks (290 of 290 at the derived interval; the pace 0.5718 to 0.5893), series L7's cone (the age 29 on both rows); nature: the isotropy bound on N_l (row 5a, BOUND) |
| The 24 rotations and the 48 with the hand | derived (a theorem) | this paper, th:group | the six Ports and the hand bit | none: mathematics |
| Gauss's law of a free family's flux | derived from the update rules | 3.1 | the walk as a translation, the books; a closed surface no periodic axis crosses, no absorber inside | no detector reading; the run after a detector not made |
| The shell mean and Newton's inverse square; G = K eta / (4 pi N_w); the equivalence principle; the third law | derived from the update rules (in the shell mean) | 3.2, 3.3; 24.2 | the bilinear push on the arriving rows' first moment; two additivities; the shell mean over the fan; N_w an input (units), eta the release rate | no detector reading; the run after a detector not made (a body carrying a lamp beside a source, its births' Doppler read at a detector) |
| Coulomb's law, k_C = G, the sign | derived from the update rules (in form) | 3.4 | the charge column; rho an input (the hierarchy not the law's) | no detector reading |
| The two fields of one stream, the retarded wave equation, Poisson's equation | derived from the update rules, in the limit of every direction | 5.1, 5.5 | the release, the flight, the presence and the age moment as moments; the dense fan (P >> r), the open box; the coefficient tau_L | no detector reading of the fields; the clock's form at two distances: series T (row 12, 1.907 for 2.00, PASS under the age word, replicated) |
| The clock's redshift, first order; the second-order difference | derived under a calibration (a_tau = G M / (r c^2), assumed) | 5.2 | the owed count; the calibration free; the clock's word P9 (the age moment, an assumption) | series T (as above); the strong field not measured after a detector |
| The click's weight, a positive quadratic form of power 2 (Born's form) | derived from the update rules plus one axiom of the apparatus (the balanced splitter's conservation) | 6.5, 6.6; th:gleason | the phase rotation, the splitter's conservation for every pair, non-negativity; the harmonic constants c_j not derived; the least-rank click P10 a definition | series L's cells 63/1 and 27, 5, 5, 27 at N = 64, 31/1 at 32 and 125/3 at 128 (clicks, pinned before the run; the power's window [1.917, 2.012)); nature: row 2c (Sorkin's kappa, compatible), rows 2a, 2b (the visibilities, FAIL by 0.014 and PASS) |
| Planck's E = h f and de Broglie's lambda = h / p | definition or input (identities under the declared dictionary; one constant h = h_q N = h_A, its value an input) | 6.4, 7.2; 24.1 row 25 | the release's cost per phase step and the turn per Link | series H's closure on the digital circle (2.041 to 2.000; the entry's reading kind to be confirmed by the register's audit) |
| The uncertainty relation | mathematics on Z_N (derived); the physical identification a hypothesis | 22 | the evaluation at the roots of unity; the identification of the circle as position and the transform as momentum | none after a detector (row 10 not run) |
| Young's spacing | derived from the update rules (the limit) | 7.1 | the two paths' phase difference, the fan's grain | series L2b's clicks under the wheel: the bright pixels 19 to 51, the dark 0 to 3, the visibility 0.966; nature: row 2a (0.98; FAIL by 0.014, the fan's grain named) |
| Malus's law, cos^2 theta | derived from the tables (the declared rounding at 1 / 256) | the Malus note; A12 | the tables' entries in force; the rounding an input (record 328) | A12's clicks: 128 of 256 at 45 degrees exactly, 0 crossed, 64 with the third between; 219 of 256 at 22.5 degrees; nature: row 9 PASS |
| The pair: exact marginals, no-signalling | derived (a theorem) | 6.2; th:marginals | the one gather of a record from both settings; equal weights; open beyond | series L: 32 of 64 in all setting pairs (clicks) |
| S(N, N_t) exact; 181/64 at 512 to 8192; 5793/2048 beyond; 2 sqrt 2 the limit | derived from the update rules (a theorem with its closed form) | 6.2; 24.4; th:bell | the rungs of the ladder, the tables at N_t = 256, the settings (0, N/8, N/4, 3N/8) | series L's clicks: 176/64 at 64, 1448/512, 2896/1024, 11584/4096 (the 24.4 block, replicated); nature: Poh et al. (1.05 standard errors; row 1a Hensen PASS, row 1b the phase form FAIL) |
| The information cost per record; the entropy identity (bits read plus bits not read = log_2 N) | derived (identities) | 6.1, 6.3, 14 | the click's one deletion; the coarse graining | the identity needs no reading; series L's units per bit only if the register labels them DETECTOR (to confirm), else the identity alone |
| The masses: a bound set's mass as its total content; the nucleon a chain | derived in form | 19.1 to 19.5 | the strong column, the give at contact; the families' contents inputs | series R: the kicked u through the face at 63 (a face reading; the entry's kind to confirm), nature: rows 7a, 7b (series N; the register's kind to confirm), 8c (a declared input refuted) |
| The smallest mass per kind | a theorem given the input P8 (definition or input) | 16.2 (d) | nature's whole charge, an input | none |
| The receiver's and the source's Doppler | derived from the update rules | 2.2, 2.5, 2.7 | the crossing rule (division) | the rule's tests (a computation); series G2's z (the pointer's reading; the second runner's FAIL at head, record 408: to be restated before it is cited) |
| The Lorentz factor absent: the counter at the rest rate, the Doppler 1 + beta, the pace per axis | derived from the update rules; a falsifiable difference from nature | 4.3, 4.4, 12, 17; the Lorentz section | the drive per axis on main, the owed count | row 4b (G2's 0.2636 against 0.315, FAIL); row 4a a pin, not run; the hypothesis covariant-readings-v1 beside it: series S's face clicks 369 and 345 against 392, z = 0.3674 (PASS in its domain) |
| Light beside a mass: no bending, no delay | derived from the update rules (the flight blind to the crowd) | 5.4 | no rule reads the crowd into a row | series K: 0.000 pixel and 0.00 interval at the screen; nature: 1.75 arcseconds, REFUTED (24.3 row 14); optical-v1 a hypothesis with gamma an input (HYPOTHESES 27) |
| The deceleration parameter q; the expansion | the law's coasting q = -0.108 a numerical finding of series G2; the growing wall a hypothesis (expansion-v1) | 15, 20.4 | the thrown stars; H an input under the hypothesis | row 3 (FAIL against -0.53); rows 11a to 11c pins, not run |
| The weak forms: a step and a window | derived from the update rules; a difference from nature | 18.2 | the lifetime column, the click's filter | series J1, J2: rows 8a, 8b (FAIL) |
| Kepler, Bohr's condition, Bradley, Newton's geodesics, Compton, E = m c^2, Schrodinger, Faraday-Maxwell, Einstein's equation, the flow inventory | open, hypothesis or not reached, one line each in the discussion; the hypotheses in HYPOTHESES 27 | 3.3, 7.2, 12.2, 5.3, 17.6, 23, 12.1, 5.5, 25 | as the tree states | none after a detector |

Two register kinds to confirm before step 2, by the physicist's audit of record 562: series H (Bohr's lines behind the detector: the closure 2.041 to 2.000), series R's face reading and the read mass, series N's binding (rows 7a, 7b), series L's information-cost units, series G2's z after the replication's FAIL; any of them not a detector's reading leaves the checks tables and the register's row, per the rule.

### 3. The representative checks kept for pages 19-21 (DETECTOR readings only)

(a) The code implements the law (computations, not measurements): the second runner's replications bit-exact from the register's worlds at main (series L, T and the round-2 worlds; docs/REPLICATIONS.md); the books balanced at every interval in every run; the engine's inverse interval on worlds without a measured event; the rounding pins met (63/1 at 64, 31/1 at 32, 125/3 at 128; the (3, 4) split); the crossing rule's tests (toward k + 55/32 rows per k intervals, away k - 55/32, at rest k).
(b) The numerical checks of the formulas after a detector: series Q (the pace on the six headings and the 290 directions, face clicks); series L7 (the cone, the counters' age 29); series L (the CHSH S at 64, 512, 1024, 4096; the marginals 32 of 64; the Mach-Zehnder 64/0; the (3, 4) split's cells; the two-slit clicks under the wheel); A12 (Malus at 45 and 22.5 degrees); series T (the clock's form at two distances); series S (the covariant readings' face clicks and z, under the identity); series K (light beside a mass: 0.000, 0.00); series J1, J2 (the weak forms); series G2 (z of the coasting stars, once restated after record 408).
(c) The comparisons with nature (the confrontation register's rows with a detector reading): 1a, 1b, 2a (the clicks), 2b, 2c, 3, 4b, 8a, 8b, 8c, 9, 12 with their verdicts; 5a BOUND; the pinned rows 4a, 5b, 6, 10, 11a, 11b, 11c in one line, "not run"; rows 7a, 7b after the audit's word on series N; the prediction 181/64 against Poh et al.; the twelve failures named as the law's own results, the three decisive ones first (the unslowed clock, the bending, the deceleration).

### 4. What the first page says of the general formula

Page 1 carries Eq. (1) as it stands, s <- s + r; e <- sign(s) min(floor(abs(s) / d), a); s <- s - e d, with four lines: one map at every Node of a cubic GameBoard at every interval; each component of the state is a bounded integer accumulator with a declared rate r and a declared wall d, translated by its rate, counted in walls (capped at one for the drive), reduced by the walls it holds; every wall counted is an event (a Link crossed, a phase step, a count completed, a birth, a push), and nothing else happens; the rates and walls are made of six integer operations (translation, a declared integer matrix or bilinear form, the group-ring sum, a permutation, the evaluation at the roots of unity with its norm, the division with the remainder kept and the comparison); one comparison, the click, is the only read-out, and only a detector's reading is a measurement. The full definition (the state, the components, the two blocks, the read-out, the rules apart from the parameters and the initial conditions) is chapter 2 (pages 3-5); every derivation of the paper names which of these rules it starts from.

### 5. The guiding statement for the cut (the owner, 2026-09-22, about 00:50Z, in Hebrew; translated; its record to follow)

The owner's words: "Use only the things that are closed with us, that
have a clear claim and a clear proof; throw out what is not clear; you
know from the reviews what is clear and proved, use that. In my view the
central thing in the paper is the claim that several different physical
phenomena can be produced from one shared discrete update law and a
small number of assumptions. The general formula is the starting point.
The possible novelty lies in showing how the same mechanism leads to the
geometry of propagation, to the flux and the forces, and further to
measurement and to correlations. The decisive question is how many of
the results the law really forces. If for every phenomenon a rule must
be added that puts the desired result in beforehand, the law's
explanatory power shrinks; if the same rules force several different
results with little freedom of choice, that is the strong scientific
contribution. So the three things must work together: the general
formula defines the mechanism; the derivations show what follows from
it and under what conditions; the simulator and the comparison with
experiment check the results and their limits. In the version I read,
the contribution that can be established now is an explicit model with
several conditional mathematical results and numerical checks; the
broad claim that it describes nature still needs completions. I would
build the paper around a precise statement of the distance between
these two."

What this fixes for step 2, on top of sections 1 to 4:

1. **The spine is the forcing ledger.** Every result the paper keeps
   carries three columns in its five-step path: the rules of Eq. (1)
   it starts from (nothing added), the assumptions added beside the
   rules (each named once, with its kind: an axiom of the apparatus,
   a calibration, a limit, an input), and the freedom left (the
   parameters). The paper's central table is this ledger, one row per
   result, so that a reader counts what the law forces and what was
   put in: the flight table forces c = 1/sqrt 3 and the isotropy bound;
   the walk and the books force Gauss's flux exactly; the bilinear push
   forces the inverse square in the shell mean under the dense fan; the
   same rows' moments force the retarded potential and Poisson under
   the same fan; the evaluation at the roots of unity plus one axiom
   (the balanced splitter's conservation) forces the quadratic form of
   power 2; the one gather forces exact marginals; the rungs force
   S(N) exactly with its limit 2 sqrt 2; no rule of the law forces the
   Lorentz factor, the bending, the masses' values or the harmonic
   constants, and the paper says so in the same table.
2. **What stays: the closed results only.** The derivation
   mathematician's closure (record 398, CLOSED) and this paper's
   theorems: the click rule and the rung rounding (6.2); the split
   identities and the norm rule (6.5); the group count and the second
   law at the click as a count (14); the pace bound and c = 1/sqrt 3
   (FORM.md 1; prop:pace); S(N) exact with the plateau 512 to 8192
   (24.4; th:bell); the quadratic-form classification under its axioms
   (6.5; th:gleason); the continuity equation from the books (25.4);
   the 24 rotations (th:group); the isometry and the bijection on the
   GameBoard alone (th:isometry, th:bijection); exact marginals
   (th:marginals); Gauss's flux (3.1); the shell mean and Newton's
   inverse square, and the retarded potential and Poisson, each with
   its stated condition (the dense fan, the shell mean: 3.3, 5.1),
   since a result with its condition written is a clear claim.
3. **What leaves: everything without a clear claim and proof.** Every
   "in form", "pinned, not run", "not reached" and hypothesis row
   (Kepler, Bohr's condition, Bradley, the geodesics, Compton,
   E = m c^2, Schrodinger, Faraday-Maxwell, the masses in form, the
   expansion under a wall, the smallest mass's theorem given an input)
   leaves the body; the hypotheses stay on the tree (HYPOTHESES 27)
   and the discussion names them in one sentence as the completions
   the broad claim needs. The DIFFERENT rows stay, because a
   difference from nature with the law's number and nature's is a
   clear claim (the unslowed clock, the Doppler without the factor,
   light unbent, the weak forms' step and window, the coasting q):
   they are the measured distance the owner asks for.
4. **The distance, stated precisely.** The discussion (pages 22-23)
   states in one table what is established now (an explicit model; the
   theorems above; the numerical checks after a detector that agree
   with the theorems: the pace, the cells, S at four N, Malus, the
   clock's form at two distances) and what the broad claim still
   needs, item by item with the check that would decide it: the
   detector runs of Newton's and Poisson's laws; the muon in flight
   under the law (row 4a, a pin); the bending under a rule that reads
   the crowd (optical-v1's pins); the Lorentz factor (the FAIL rows and
   the covariant readings beside them); the harmonic constants and the
   identification of position and momentum; the masses' values; a CHSH
   measurement at 1e-4. Nothing in between: no "reached in form", no
   number of the board.
5. **The abstract says the two things and the distance**: what the
   law forces (the list of item 1), what was assumed beside it (the
   splitter axiom, the least-rank click, the calibration of the clock,
   the dense fan, the inputs), and that the description of nature is
   a program with named completions, with the twelve failures counted.

### 6. The two checks of the plan folded in (records 588 and 590; the Boss's word of 01:05Z, 2026-09-22)

The mathematician, section 2 (AGREED with five words and four rows):
(a) c = 1/sqrt 3 is proved in DERIVATIONS_BEAM 13.2 (a) with 1.4 and
FORM.md 1 (not 11.1, the linear block's shift operator). (b) Planck and
de Broglie: derived from the update rules as identities (21.2 rows 51
and 52: E = h_q s = (h_q N) f the release's cost rule read as an
identity, lambda = h_A / p the turn rule's), with the constant h and
the dictionary h = h_q N = h_A an input (24.1 row 25); the "compared
with" column reads "none after a detector" (series H's closure is a
GameBoard reading, below). (c) The masses split: a bound set's mass as
its total content, derived (19.1); the nucleon as a chain of three and
the strong ratio, in form with the strong column an input (21.5 rows
41 to 43), so hypothesis or input there. (d) The smallest mass per
kind: derived, a theorem (16.2 (d)), its premise P8 an input. (e) The
clock's redshift: derived with the calibration an input, sharper than
"assumed": by 5.1 and 3.3 the clock's constant and Newton's G have the
exact ratio (n / d)_susp x S, so a_tau = G M / (r c^2) with 3.3's G
holds iff the suspension pair is [1, S] (a constraint on the inputs,
F16). The open list's words: Newton's retarded geodesics "derived (5.3),
unconfirmed by any registered orbit, the run after a detector not
made"; Bradley's aberration "derived at first order (12.2), pinned,
not run"; the deceleration "the law's coasting q = 0 derived (15.4,
Milne, the thrown stars); G2's -0.108 its reading, a numerical finding
inside the coasting bracket; the growing wall a hypothesis". Four
central formulas added to section 2's table, all derived from the
update rules: Born's rule as a limit with the 1/N bound per cell (6.2;
21.2 row 12), distinct from the form's row; the continuity equation
from the books (25.4; record 398 CLOSED); the Lienard-Wiechert retarded
potential of a moving source at first order (12.1; 21.2 row 21);
Boltzmann's S = k log W as the count of torus points (14, 16.1; 21.2
row 53). Two more, closed and small, at the coordinator's call within
thirty pages: Newton's cooling as the release's exponential (25.9); the
muon's decay tick under the identity (18.1 (a)); the cut takes the
first if a line is free, and neither if not.

The physicist, section 3 (the checks' kinds): (a) the replications, the
books, the inverse interval, the rounding pins and the crossing rule's
tests are gates and computations, under (a) only. (b) DETECTOR, stay:
series Q's 290 face clicks and the pace; L7's cone and the counters'
age 29; L's S at 64 to 4096, the marginals 32 of 64, the Mach-Zehnder
64/0, the (3, 4) split's cells 63/1, 31/1, 125/3, the two-slit clicks;
A12's 128 of 256 and 219 of 256; T's ratio 1.907 at 6 and 3 Links (the
lamp's births at the detector; the clock series' k, a replay, never
cited); S's face clicks 369 and 345 and z = 0.3674 (the body's own
record), "under the identity" said as arithmetic on the click ticks
(S's E' at load, the pace and the invariant out); K's 0.000 pixel and
0.00 interval (the screen's clicks; the crowd at b out); J1's widths
0.036 and 0.038 over the 64 beta clicks and J2's 16 of 1024 with 0
behind (the weak's "the pair holds" out). (c) Rows 1a, 1b, 2a, 2b, 2c,
8a, 8b, 9, 12 DETECTOR, stay; 5a stays as a bound; 8c a declared input
against nature, labelled an input, not a measurement; row 3 (q =
-0.108) DETECTOR in kind, reproduced at head as a verdict with the
digits moved (-0.104 at t_0 = 350, the pins met, record 408), cited
with that status; the pinned rows in the one "not run" line. (i)
Series H: the closure 2.041 to 2.000 and the closing ratio are the
orbit's r, p and T from the step records, GAMEBOARD: the closure
leaves; what H reads after a detector is the electron's click on a
face with its phase, which reads where the orbit ended and not E = h f.
Series R: the kicked u through the -x face at tick 63 with its 2/3 e (a
face click) and the read mass (the border's glue rows, the lifetime
border a detector) DETECTOR, stay; the separations, "no step" and the
first step's tick GAMEBOARD, leave. Series N (rows 7a, 7b): the bond
clicks on the lifetime border, the escaped content 4 and 8 and the mass
a detector reads (3673) DETECTOR, stay, with the pushes, reads, hands
and kicks; "no step" and "the pair separates" GAMEBOARD, not the
binding's evidence. Series L's information-cost units (82, 4, 6, 185
per 1, 2, 3, 6.3 bits): DETECTOR click amounts summed by the host, the
bits a definition of the coarse graining; they may stay in section 2's
row as arithmetic on registered click amounts with each amount's
register key, and they leave (b) and (c); the entropy identity stays as
a theorem. (ii) G2's z = 0.2636 (row 4b and the coasting q): DETECTOR
in kind but read before the crossing rule and unreproducible at head
(record 408, INCONCLUSIVE): out of (b); restated once in the "not
reproduced at head, re-run pending under the age word" line; row 4b's
FAIL kept in (c) with that status and no other citation. (iii) The one
formula-against-formula item is series H's closure (out); S's z from
the click ticks, 2c's exponent window from the click cells and T's
ratio against the derivation's pin are arithmetic on clicks and fine
when the sentence says so; the prediction 181/64 against Poh et al. is
the law's number, not a simulator measurement. Nothing of the board as
a measurement anywhere (records 281, 562, 564, 575); the base is
b684ba0b's text. Step 2, the cut, starts on this word.

### 7. The sixth column, the derivation's ground: three rungs (the proposal of record 605; the mathematician's and the physicist's checks, records 607 and 609, AGREED with corrections; the Boss's word of 01:45Z)

The five-step path gains a sixth column, the ground on which the
derivation stands, so that "how much the law forces" is counted at
three levels and never at one: rung 1, exact on the GameBoard (no limit,
no average); rung 2, a limit of the grain taken on paper with its rate;
rung 3, a limit under a spatial condition, an average that covers the
shell, the condition part of the claim.

The head rule (both checkers): a rung-3 claim is stated with its
condition in the sentence and compared with nature only after a
detector (record 575), never with a probe's reading; a detector reading
never lifts a rung-3 claim to rung 1: what a detector run establishes is
a sharper lattice-exact claim about the world at hand (rung 1 or 2
arithmetic, pinned from the lattice's lines or the orbit's sweep,
DETECTOR in its reading), whose agreement with the continuum's form
within the named ripple is the evidence for rung 3 and never its proof.

Rung 3's condition (the physicist): not "P >> r" alone but an average
that covers the shell, in three admissible forms, each with its own
error: (a) over the shell's Nodes, the shell mean, the ripple
O(r^(theta - 1)) with theta <= 131/208 (3.2), at any declared fan; (b)
over the directions at one Node, the dense fan K to infinity at fixed
r, and then only for a fan declared in a ball |D| <= P (a cube's fan
keeps a cubic anisotropy of 3^(3/2) in the limit); (c) over the path of
a body that sweeps the fan's lines, one closed turn of an orbit, whose
mean push per turn is the ring mean exactly, the only one of the three
readable after a detector. For Poisson and the retarded potential (5.1)
the same average plus the dwell direction-blind (T_D / (|D| Q) within
the label's 1.35 percent). Newton's and Coulomb's inverse square,
Poisson, the retarded potential (12.1 at first order, the fan's grain)
and the retarded wave equation (5.1) are rung 3.

The placements (both): (1) c: rung 1 holds the identity "the pace of a
direction is Q |D| / T_D, isotropic within 1 / T_D" and the Manhattan
bound S_1 Q <= T_D (13.2 (a), exact in integers); "c <= 1 / sqrt 3" is
not exact on the board (the Euclidean pace is at or above 1 / sqrt 3 on
282 of the 290 directions, 0.5818 on every heading, 0.5774 on the eight
diagonals; record 262); the value c = 1 / sqrt 3 attained is rung 2;
series Q's DETECTOR 0.5718 to 0.5893 is the reading of the
whole-interval grain of arrival, a third thing, labelled so. (2) The
books' conservation rung 1; the continuity equation splits: the lattice
identity from the books rung 1 (25.4), its differential form rung 2.
(3) Gauss's law of a free family's flux (3.1) rung 1 by name, under
the declared world condition (a closed surface no periodic axis
crosses, no absorber inside). (4) S(N): the exact rational at each N
with the tables at N_t = 256 rung 1; 2 sqrt 2 rung 2. (5) Born: the
bound itself (a cell within 1 / N, the cumulative within 1 / (2 N))
exact for every N, rung 1; Born's rule as the equality of probability
and weight its limit, rung 2. (6) Planck and de Broglie: identities
under the declared dictionary, the dictionary an input (24.1 row 25):
rung 1 as identities (Planck's E = h_q s exact at every birth, 6.4; de
Broglie's circle exact to the floor per Link, 21.5 row 52); not rung 2.
(7) The redshift row splits in three grounds: the clock's rate
1 / (1 + a_tau) and its never reaching 0 at a finite count (no horizon;
the second order 1 - k + k^2) exact on the state, rung 1; the 1 / r
form of a_tau rung 3; the calibration a_tau = G M / (r c^2) an input of
the dictionary (5.2), not an average; series T's row says "the form
measured at a detector at two Nodes (1.907 against the lines' pin
1.909, nature's 2.00 4.6 percent away), the continuum's 1 / r a rung-3
limit", never "the 1 / r law measured". (8) Newton's row splits: the
equivalence principle (push_m = m x push_1 record by record) and the
third law at rest (exact to the apportioning's grain) rung 1; the
inverse square rung 3. (9) "The second law as a count" worded as 14's:
the entropy produced only at the click, the cancel and the leaks, a
count of torus points; no second law claimed. (10) CLOSED items named
with their rungs: the muon's decay tick (18.1 (a), rung 1 under
covariant-readings-v1's identity); Newton's cooling within one birth's
cost (25.9, rung 1, an exact bound); a body's dispersion (4.4, rung 1);
the moving clock's rate 1 (4.3, rung 1); the Doppler on the axis by the
crossing rule (2.2, 2.7: rung 1 for the count per Link with its
boundary row, rung 2 for the ratio 1 +- v / c); Boltzmann's S = k log W
(14, 16.1, rung 1); the Lienard-Wiechert retarded potential at first
order (12.1, rung 3); the retarded wave equation (5.1, rung 3). The
rest of rungs 1 and 2 as placed in record 605 (the marginals and
no-signalling, the entropy identity, the 24 and the 48, the isometry
and the bijection, the click's quadratic form under its two axioms,
Tsirelson to 8 / N, Young's spacing). Detector readings today: none of
rung 3's claims has one that lifts it; series T's is the only detector
reading of a rung-3 form; Newton's and Poisson's runs enter pages 19 to
21 as one row each only if they land before the cut's PR, else the rows
say "not made". The owner's word of record 606 stands over all: only
what the paper needs.

## The thirty-page form, step 2 done (2026-09-22, the Boss's word of 01:45Z)

The cut written as the plan's sections 1 to 7 say: nine sections in the
owner's order with Eq. (1) on page 1, the forcing ledger (Table 1,
twenty-six rows with the ground column in three rungs), the hand-worked
update and the code path, the detector checks table and the
confrontation table's detector rows, the distance table; three
appendices (proofs; the tables' rounding and the symbol table;
reproduction). Out of the body: every "in form", "pinned, not run",
"not reached" and hypothesis row (HYPOTHESES 27 and one sentence of the
discussion), the tables of consequences and of assumptions, the What is
new, What is not claimed and hypotheses sections, Part IV's limits and
Lorentz sections (their kept content in the discussion), the two-slit
and S(N) figures (their numbers in the checks table), the literature
essay (one positioning paragraph). No number moved; three numbers added
with their source in NUMBERS.md (the hand-worked update, the 282 of
290, the 4.6 percent). The PDF: 30 pages (the body through 25, the
references 26 to 27, the appendices 28 to 30; the owner's 23 + 4 + 3
met in the total, the body two pages longer and the references two
shorter).


## The reviewer's corrections folded (2026-09-22, the owner's word of 01:24Z: the reviewer the paper's writer)

The verdict on the cut at 5c6c4576 was ADMISSIBLE WITH CORRECTIONS (the
reviewer's report to the Boss, 01:31Z; seven must-fix, eight should-fix;
the split 25 / 2 / 3 approved by the owner). The corrections are folded
by `cut30/corrections.py`, one exact replacement each, applied by the
assembler after the four parts are joined, so that main.tex stays the
assembler's output (`tests/test_paper_cut30.py` holds it to that). What
changed, by the report's labels:

- M1 to M3: the abstract and the discussion read the ledger's ground
  column: exact, the pace of every direction with its Manhattan bound,
  Gauss's law of a free family's flux under its world condition, and
  Planck's and de Broglie's relations as identities under the dictionary;
  a limit of the grain, the value c = 1/sqrt 3; a limit under the average
  that covers the shell, Newton, Coulomb, the retarded potential and
  Poisson (records 607, 609; section 7 above).
- M4: row 2b's verdict rests on the clicks (64/0 over 64 births, the
  visibility 1.000 above 0.98), not on the offers' 0.9988, a number of the
  apparatus layer (records 281, 562). The register's row 2b still carries
  the offers' number; its restatement is the register's own order.
- M5: the owner's status word (record 573) on every central formula: the
  ledger's caption says every row is derived from the update rules
  implemented in the simulator, with what is added beside them in the
  third column; the sections say "derived" where they said "reached";
  Coulomb's "in form" (a status record 595 excludes; DERIVATIONS 21.2 row
  7 has it R) reads "derived under the same average as Newton's, the
  ratio exact".
- M6: Appendix C names the defined version, the tag paper-2026-09-22 on
  the merge commit of the cut's pull request (records 606, 616), and the
  cut's tree (main merged at 87c7ec6b); the stale b6ab1bb3 out.
- M7: the editing seams. Their source was `cut30_lib.cutp` with a
  blank-line end anchor, which matched the empty string and removed the
  start phrase only, leaving the rest of the sentence; a blank-line end
  now means the end of the paragraph and the pattern is asserted
  non-empty; the two conditional patches of part3 (the Gleason
  parenthesis, which restores the citation of Gleason 1957) and part4
  ("by definition. That the") apply unconditionally; the cut of "The 48
  are the GameBoard's stand-in" in part2 is withdrawn (the reviewed text
  kept the sentence). With the fix, the crowd-audit sentence (23 rules,
  13 and 10), the constants sentence with the gallery's citation, the
  world-key history, the "Theorem 2" aside and the second Sinha
  sentence leave, as the parts intended.
- S1: the confrontation table's caption counts its rows (four PASS and a
  fifth under the clock's assumed word; twelve FAIL as seven in a run,
  four by a pin, one a declared input refuted; two BOUND); the abstract
  and the discussion say "four readings pass, a fifth under the clock's
  assumed word".
- S2: "above 1/sqrt 3 on 282 of the 290 and exactly at it on the eight
  diagonals" (Proposition prop:pace); NUMBERS.md's row reworded.
- S3: the muon's row under covariant-readings-v1 leaves the ledger (a
  result on a hypothesis beside the law; the covariant readings stay in
  the checks table and the distance table); the ledger has 25 rows.
- S4: the crowd-clock sentence (runs measured once, not registered)
  leaves; the three drafted entries leave the references with it.
- S5: eta and beta named at first use; "the board" reads "the
  GameBoard's state"; HYPOTHESES 27 cited once, in the discussion; the
  single opening named once as a row without a run.
- S6: the Mach-Zehnder record total labelled a number of the apparatus
  layer; the symbol table pruned to the symbols the paper uses.
- S7: Gleason 1957 back in the references (through M7's fix).
- S8: the distance table's harmonic-constants row names the identification
  of the circle as position and its transform as momentum, a hypothesis,
  with the single opening as its deciding check.

The references open a page of their own (a `\clearpage` in the
assembler), so the approved split is read from the page numbers: the
body through page 25, the references 26 to 27, the appendices 28 to 30;
30 pages, no overfull vbox, no undefined reference. No number moved; two
labels added (S2, S6). The 11 overfull hboxes of 2 to 16 points stand as
cosmetic. The coordinator's last content commit (498b6f31, the exact
square displayed in the discussion's Lorentz paragraph) and the fold
together ran the body four lines onto page 26; the sentence on the
tables' precedents in signal processing (a precedent, not a claim; its
four references with it) left the positioning paragraph and S8's row was
shortened, so the body ends on page 25 as approved. The owner's word of
01:48Z made the reviewer the paper's only writer; the coordinator's
HANDOFF.md and cut30/notes stand as he left them.

## The covariant rule in hand (2026-09-22, the owner's word in the writer's session)

The owner asked how W = E_0^2 + 3 p.p, a hypothesis beside the law
(covariant-readings-v1), becomes a law with us; the writer answered in
three steps (the three tests, with E' kept by comparisons and no root;
the same pins read after a detector off the one axis; the Highlights
line superseding record 270's) and the owner said "go for it", then:
the Boss handles the implementation, the paper says it is being
handled. One correction added to cut30/corrections.py: the distance
table's Lorentz row cites the displayed exact square (Eq. eq:square)
instead of restating it and says the rule's entry into the law is in
hand on the owner's word of 2026-09-22, the runs off the one axis
pending, the text claiming nothing of it until they land. One finding
passed to the Boss: the engine refuses a momentum on more than one axis
until form B's directional drive lands (examples/events/covariant/README.md,
17.6 N2), so the off-axis runs wait on the Architect's build. 30 pages,
the split 25 / 2 / 3 held.

## The Newton row (2026-09-22, series D3 on main; the Boss's order of 02:24Z)

Newton after a detector landed as series D3 (PR #718, the physics-rule
reviewer's ADMISSIBLE WITH CORRECTIONS). What the paper carries, and no
further: the equivalence principle measured after a detector (the held
mass four times, the same clicks to the Node on 138 of 139 common birth
ticks and the same escape tick, rung 1 on the detector); the controls'
pace to the tick; the 1 / r force's scale symmetry consistent, T(24) /
T(12) = 1.997 against 2.00 +- 0.18, from one recurrence per radius on
loops that are not similar figures, not closed; G's value not read; the
circle's period, amplitude and omega^2 outside their pins as registered.
Four places changed through cut30/corrections.py: the checks table's new
row, the distance table's Newton line, Section 4's ground paragraph (the
"run not made" now Coulomb's and Poisson's), the introduction's open
list. The row cost about 27 lines of body; the body is held at 25 pages
by trims that carry no claim: the octahedron figure smaller with its
caption cut to its facts (Theorem 1 states the rest), the second
departure's clause on a test fixture (not a registered world), the
positioning paragraph's "own geometries" clause (three references with
it), the symmetries' parenthesis on the ties, the code paragraph's list
of readings, one sentence of the ledger's caption. 30 pages, the split
25 / 2 / 3 held.

Added in the same commit on the Boss's words of 02:53Z: the ledger's
no-dispersion row names what is put in (the rate in transit constant, the
flight blind to the phase, P9; whether the six operations force it is
open, the mathematician's assignment on the owner's word "go for the proof
of c"); one sentence in the no-dispersion remark that the constancy of c,
by the postulate, meets GRB 090510's bound on an energy-dependent speed of
light (Abdo et al. 2009; a computation of NUMBERS.md rows 97 to 99, not a
run, not a derived result). Seven further trims of duplicated sentences
and asides held the body at 25 pages: the anisotropy bound said twice in
Section 3, the delay section's operations list (Table 1's row carries it),
Theorem 6's parenthetical repeated in the paragraph after it, the
harmonic's aside in the limit paragraph (and Lambda from the symbol
table), the read-out's aside, the introduction's "excluding 1 and 3", the
GRB sentence itself kept to three lines.

## The constancy of c a postulate (2026-09-22, the mathematician's verdict, DERIVATIONS_BEAM 27)

On the owner's word "go for the proof of c" the derivation mathematician
asked whether the six operations with locality force a phase-blind
flight, and refuted it: a dispersive flight (the rate N_l |D|_1 (N - f)
against the wall T_D N) passes the three tests, the books, the split's
isometry, the interval's injectivity, the isotropy within 1 / T_D and
the direction-only requirement, and disperses frequencies in the mean
for gcd(r, N) > 1. So the constancy of c is the declared postulate P9,
and what the verbs force is what the paper already carries: given a
direction-only flight, the pace at every phase and rate, isotropic
within 1 / T_D, c = 1 / sqrt 3 its limit. Two corrections through
cut30/corrections.py: the ledger's no-dispersion row closes its third
column on the fact (P9, not forced, the derivation's 27), and the GRB
sentence stays a consequence of the postulate without the "until"
clause. No number moved; 30 pages held.

## The owner's review of the thirty pages (2026-09-22, his five must-fix items, his word "go")

The owner read the thirty pages and sent seven points; the Boss relayed
his word: the five that are the paper's own errors go without waiting
(record 629), the two decisions he keeps (the title; the S(N) figure at
half width) move on nothing but his word, and stay as they are. The five,
each one entry of cut30/corrections.py, none by hand in main.tex:

1. The Gleason theorem and the tables. The theorem is about the ideal
   reading; the built click is that form to the tables' rounding, the
   record's total over the 64 birth phases from 65448/65536 to
   65773/65536, the tables' violation of hypothesis (a) (at N = 64,
   C[1]^2 + S[1]^2 = 65650; the extreme a part in 276), the norm range of
   the appendix the error bound: the sentence the generator's cut had
   dropped, restored. The power's windows read from the click cells are a
   read-back of the built click, which carries the square: a check that
   the implementation is the theorem's form, no evidence about nature's
   power. The introduction's window sentence, the map of results and the
   discussion's "what the runs support" say the same; the k = 1, k = 3
   counterfactual goes (an implementation check needs none); what
   excludes the phase-blind detector is interference, nature's (row 2a)
   and the built click's.
2. Theorem 3 (th:bijection), false as printed because the age sat in the
   basis and a split resets it: restated in the derivation mathematician's
   wording on the quotient Q that forgets the age, for the fixed event
   history the record keeps, the age a function of the history; rung 1.
   The proof follows (F and S on Q, the engine's record the history the
   statement fixes), and the introduction, the ledger's row and the
   discussion's list say "for a fixed event history".
3. Tsirelson in the discussion: 8/N plus the tables' 0.0444, 2 sqrt 2 in
   the joint limit of N and N_t, no longer "8/N" against the fixed-table
   limit 186034/65773 of Theorem 6.
4. hbar = h / (2 pi) = h_q N / (2 pi) under the paper's own dictionary
   h = h_q N; the age bounded by the family's lifetime and the run.
5. Table 3's rows 2a, 2b, 2c in the chief physicist's lines, the
   register's criterion named on each (the clicks' visibility of
   slits_huygens against 0.98 and the ideal 1; the offers' visibility of
   mz_equal, 0.9988; no apparatus model), and 2c's verdict NOT COMPARED
   (kappa not computed): the window an implementation gate, no evidence
   about nature, no three-opening world registered. The verdict words
   gain NOT COMPARED; the tally is three PASS, a fourth under the clock's
   word, twelve FAIL, two BOUND, one NOT COMPARED, in the caption, the
   abstract and the discussion; Section 6's three-slit sentence is the
   row.

The page count: 30 held (the body through 25, the references 26 to 27,
the appendices 28 to 30) by trims of text whose numbers Table 2 carries
(series S's and D3's numbers in Section 9, Table 4's cells, rows 3 and 4b's
asides), of the repeated list of the three decisive failures, and of the
Courant, visibility, clock's-word, cone, crossing-count and Section 7
repeats; no claim moved. NUMBERS.md carries the new numbers with their
kinds. The Highlights line, NATURE.md and DERIVATIONS_BEAM are the
Boss's, the physicist's and the mathematician's commits; the paper
follows them.

## The title (2026-09-22, the owner's word "A, go", through the Boss)

The owner keeps candidate 3's frame and adds the word that separates the
law from its read-out: the law is local (the six operations at a Node and
its six neighbours), the click is one gather from both detectors,
non-local. The title is "Universe24: a local integer law of nature with a
non-local read-out, and what follows from it", and the abstract's first
sentence names the click "the one non-local step"; no other change on
the title. With it, the writer's re-read of the five: row 2b's criterion
written on the bright and dark ports' offers, (b - d) / (b + d), without
the direction's letter D; row 2a's wheel named "the birth wheel" as the
paper names it everywhere; Q, the quotient of Theorem 3, in the symbols
table; the Gleason sentence's end whole ("the norm range of Appendix B is
the error bound between the two"). No number moved; 30 pages held (the
body through 25, the references 26 to 27, the appendices 28 to 30). The
S(N) figure at half width waits for the Bell runner's rows on main, one
commit after the Boss's SHA.
The owner's word of the same day on the formulas' places: every central
formula is a numbered display (the map, the shell, Newton, Coulomb, the
fields, the wave, the rung, the joint weight, Gleason's form, the bound,
the prediction, the covariant square), and the covariant square, Eq. 14,
his "big formula", is set in a frame; 30 pages held.

## The Bell runs measured and the S(N) figure (2026-09-22, the owner's "B, go"; PR #759 on main at b34fe114)

The Bell runner's rows are on main: S x N = 5792 at N = 2048 and 23168
at 8192 (181/64 exactly, the plateau) and 46344 at 16384 (5793/2048, the
plateau's end where the closed form put it), DETECTOR readings of the
register's block bell_24_4 / run_2048_8192_16384, the replication
byte-identical, no pin changed. The paper: Theorem 6's last sentence,
the proof's 16384, the prediction paragraph, Table 2's S(N) row (with
b34fe114 as the source of the last three), the introduction's map ("S at
seven grains") and its narrative say "measured"; the S(N) figure returns
at half the width beside Table 2 with its caption at its side: the
closed form at every multiple of 8 as the curve (a computation), the
seven detector readings as circles, the inset with the plateau 181/64
and its end 5793/2048, 2 sqrt 2 dashed; every point named by its kind
in the caption. figures.py's figure_s_of_n is rewritten for it (the
readings from the runs' summary and the amplitude register's expectation
file) and figures/s_of_n.pdf regenerated. The page count, 30 held, is
paid by duplicated text carrying no claim and no table number: the pace
readings and the rounding pins said once in Table 2, the ledger's caption
not repeated in Section 4, the read-out paragraph of Section 2 shortened
to what Definition 3 does not say, the reviewer's and the gate review's
recomputations left to NUMBERS.md and the log, and small parentheses.
One word of terminology fixed on the way ("a number of the board" to
"of the GameBoard's state"); row 5a names the flight table's pace as the
formula's, series Q's reading at finite ages in Table 2. The Lorentz
sentences and the click frame are untouched, as ordered.

## Prepared, not applied (2026-09-22): the framing commit and the reshaping commit, one canonical plan each

The owner's word for every agent (through the Boss, 06:50Z): what a
later word replaced is cut from what one looks at; everything gets
shorter. This block is the one plan; the cut list at its end names what
was removed and why. The paper's text is untouched by all of it; the
scratch scripts of the writer (framing_patch.py and its rounds) carry
the framing commit's corrections and compile on a trial at 30 pages.

### A. The framing commit (goes on PR #769's merge SHA; records 745, 749, 753, 762, 768, 773, 777, 793)

1. The title, the writer's call (record 773: not critical): "Universe24:
   a local integer law inside the GameBoard, a non-local read-out above
   it, and what the clicks recover of nature".
2. The abstract's first sentences: Inside a cubic GameBoard one update
   law of bounded integers propagates records as a beam by algebraic
   formulas at every Node and interval (one map, a rate and a wall per
   component, six integer operations); Outside, the game above the
   board, detectors and their clicks only, the beam passing to them with
   amplitudes at the click, the one non-local step and the only read-out,
   the GameBoard read in no other way (P11); Inside the consequences are
   derived and need no experiment, Outside the clicks recover known forms
   and are compared with known experiments, result by result, and the
   paper shows how far Outside represents reality. The Lorentz factor in
   the ledger's list "(how the clicks arrive at it is the frame)".
3. P11 after P10, one sentence: the GameBoard, Inside, is read only
   through its emitters and detectors, Outside; every result Outside is
   a click, a number of the board's state is never a reading, every
   comparison with experiment is a comparison of clicks with readings;
   a measurement is itself an event of the board, an emitter putting a
   record on it and a detector ending the record at the click, the one
   step that deletes Inside and the one row that Outside gains (the
   owner's half sentence to the writer).
4. The reading rule names P11 and adds: every physics name in the paper
   names the known form the law's result recovers, Inside by derivation
   or Outside at a detector.
5. The sweep, five places: the title; the abstract; the claim
   paragraph ("the forms of several physical phenomena are recovered
   ... Inside by derivation and Outside at the clicks"; "the broad claim
   that Outside represents nature"); "Definition 3 recovers the Born
   rule's form". Two ordering sentences: Section 8's opening (the gates
   on the code; what is shown Inside by algebra under named assumptions,
   needing no experiment; what is measured, a run Inside read Outside);
   "What is proved" opens "Derived Inside, exact on the GameBoard, no
   experiment needed", its limits "Recovered ...".
6. The frame paragraph of the discussion, "Inside and Outside, and how a
   click arrives at Lorentz", before "The limits", replacing that
   paragraph's first two sentences: a packet moved Inside and what it
   says Outside; Inside the beam by Section 2's formulas where no one
   measures, Outside detectors and clicks only (P11); a detector's clock
   what it emits and receives back on its own record, no Node holding a
   detector's time, an open face without a clock, its tick the record's
   ordering (a GameBoard diagnostic), a velocity Nodes apart over counts
   apart, Definition 3's read-out the click; the three sentences of the
   click frame's section 0 verbatim at the merge, with "Outside, the game
   above the board" for "our real world" (record 768), cited
   \cite{clickframe} (a new bibitem with the merge SHA); the sentence:
   (A1) and the one line k_AB = k_BA are special relativity's two
   postulates in the click language, so what is arrived at is Einstein's
   road walked on clicks, and what the board adds is (A2), the amplitudes
   that carry sqrt(1 - v^2) into a detector's own rate; the fact: the
   law meets (A1) and not (A2), its clicks carry the group, its counter
   runs at the rest rate (rows 4a, 4b), the two one-way Doppler factors
   r / (1 - v) and (1 + v) / r alike only at r^2 = 1 - v^2, the law's
   r = 1 leaving 1 - v^2, the measurable; no wall and no declared
   identity enter the reading, Eq. 14 an Inside formula on the record,
   read by no detector, whose Outside formulas the conversion gives; the
   closing: a computation Inside whose passage Outside is the clicks, at
   the quantum level as well, how far Outside represents reality what
   Tables 2 and 3 show. The limits paragraph then opens "The covariant
   readings (record 270) read one Inside formula Outside on one axis,
   series S against its pins: a body's record carries ..." with Eq. 14
   in its frame. Table 4's Lorentz row: "the law meets (A1) and not
   (A2)" and the frame's measurable (1 - v^2 under the law, 1 under
   Lorentz; the split of a row between staying and hopping, a hypothesis
   not opened). Section 3's boost sentence: Lorentz's symmetry is that
   of the clicks Outside, to second order, the corrections from the
   fourth. The c-postulate row: "(A1) of the frame asks the same of the
   clicks". Row 4b: "the frame: the two one-way factors apart by 1 - v^2".
7. The page count: 30, the split 25 / 2 / 3, held on the trial by nine
   rounds of trims of duplicated or narrative text carrying no claim and
   no table number (the scripts list them); the S(N) figure and the
   framed square stay.
Blocker: PR #769's merge SHA (the mathematician's fold and the reviewer,
about 06:30Z). Then: the scripts with the SHA, the three sentences
checked against the merged section 0, main.tex regenerated, the pinning
test, check.py, one commit, one push, the report.

### B. The reshaping commit (goes on the owner's GO, after parts 6 to 9 of the click frame, the derivations light-outside and einstein-outside, and docs/designs/algebra_transition/HISTORY.md merge; records 772, 777, 787, 793, 799, 802 and the owner's words to the writer)

0. THE ORDER, the owner's word (through the Boss, 07:35Z), binding on
   this plan: the paper begins with the step beneath and everything
   follows from it, in this order, before the phenomena:
   (1) THE STEP BENEATH: the Inside step, the six verbs on the record,
       Eq. 1 with its components, W = E'^2 + 3 p.p its invariant (Eq.
       14 in its frame), the basis; nothing else is assumed (the road
       from the cells to the algebra and the quantities' table sit here,
       B.2).
   (2) THE STEP ABOVE THAT FOLLOWS FROM IT: Einstein's, the most
       general, E^2 = E_0^2 + p^2 c^2, the clock's rate 1 / gamma, the
       composition of velocities, the Doppler factors; the conversion
       the map (B.3); and Lorentz follows the same way, from (A1) and the
       one line, per the click theorem. The words, per the audit:
       "follows", "recovered", "arrived at", never "derived" where the
       form was put in, and "declared" for Eq. 14 until part 6 is on
       main; the sentence that nothing of Einstein's was put into the
       formulas, only the Inside was used.
   (3) THE SMALLEST THING ABOVE, the quantum of the Outside step: a
       theorem of (A1) and the conversion with no run: one Link between
       two places read is the least distance a click can report; a pulse
       and its return is the least time a detector times; one Node per k
       counts is the least step of a velocity; c is one Link per the
       least count; every reading Outside is a whole number of these,
       so the world above is quantized, and the click's amount w is the
       unit that arrives. The sentence: this is what physics above
       cannot get from its own formulas and ours give, why the world
       above is quantized. The theorem's statement is taken from the
       merged texts (the click frame's parts 8 and 9, light-outside
       8bd4f811 / PR #791, einstein-outside at its final head); the
       paper names it and shows the four smallest things in four lines.
   (4) NEWTON FROM THE SMALL STEP: the limit, the shell mean, the
       equivalence, already shown (Sections 4 and 5; Newton Outside when
       part 7 lands); the register's D3, T and X the confirmation.
   (5) THE PHENOMENA BY FORMULAS (B.4), the register by kind (B.5, B.6),
       the no-circularity words (C).
   The sources are the merged texts only: the click frame (PR #769),
   light-outside (8bd4f811, PR #791), einstein-outside (its final head),
   HISTORY.md; nothing applied until the owner's GO. The items B.1 to
   B.7 below are the same plan in this order: B.2 and B.3 are steps (1)
   and (2), the smallest thing is a new paragraph of about six lines
   after B.3's "The step beneath and the step above", B.4 to B.6 are
   step (5); the cost joins B.7 (plus six, within the budget's margin
   or the compile's word).

1. The opening argument, WHY physics behaves like modern algebra
   (record 793), the introduction's claim paragraph rewritten in five
   steps (twelve lines): Outside is arithmetic in Q, counts at clicks and
   their ratios; Inside is integer and local, the six verbs, the three
   tests; the couplings are tables and the Born rule a coupling computed
   from N, the rungs; the maps between click families are the Lorentz
   group up to scale; therefore every result is an identity of the
   algebra checked by kind, the declared forms named. The abstract's
   second sentence gains "so that physics above the board is arithmetic
   on counts and the law beneath it is modern algebra". WHEN: one
   paragraph closing Section 2, "When the transition was made", the dated
   steps from HISTORY.md (the Transition Historian's merged text, the
   only source), the full history in Appendix C.
2. The road from the cells to the algebra opening Section 2 (the
   skill's last section) with the table of the physical quantities and
   their algebra: the amount, the phase in Z_N, the multiplicity, the
   age; mass the content M setting the drive's wall (verb 6) and scaling
   the push's bilinear form (verb 2), the release rate, E_0; charge rho
   in the one coupling matrix; momentum an integer vector translated by
   the push and compared as a square in W; the label flow; the family
   table; the couplings as integer matrices, the Born rule the rungs'
   comparison. Then the six verbs' identities in one paragraph (the carry
   a bijection, floor(s_0 + r t), the shift, the conjugate transpose,
   the group ring's addition, the click one bilinear form).
3. The three formulas as the algebra part's frame (records 787 and the
   owner's word; the direction one way, the Boss's correction of 07:15Z:
   the basis is Inside and everything is derived from Inside, the two
   steps never meet): THE INSIDE STEP is the axiom (Eq. 1 with its
   components, the six verbs; W = E'^2 + 3 p.p its invariant, Eq. 14 in
   its frame, the paper's centre); THE CONVERSION is the map (the
   emitter-to-click map, a detector at every place read, the click
   theorem its symmetry); THE OUTSIDE STEP is the image, a theorem,
   named as what Einstein and Newton wrote and shown to be the image to
   the stated order.
   The two-column table Inside | Outside with the map in each row (the
   mathematician's recast of the click frame's section 7 table; part 7
   follows it): the interval to a detector's count, the Node to a click's
   place, the momentum to a velocity of clicks, W to the energy at a
   click, gamma, the rate sqrt(1 - v^2), the two Doppler factors, the
   phase to a frequency; the register's readings on the Outside side
   only. Under the frame the paragraph "The step beneath and the step
   above", one way: from the step beneath, by the conversion, the step
   above is derived: W times c^4 is E^2 = E_0^2 + p^2 c^2, the gate
   E_0 / E' is 1 / gamma, the drive's fraction is the click's velocity,
   the two Doppler factors are the step above read at two detectors;
   each named as what Einstein wrote and shown to be the image to
   second order (the click frame's section 7 at its merge: the walk's
   invariant, the Planck map, E' = E / c^2, the 3 as 1 / c^2 = d on the
   body diagonal, the corrections m^2 beta^2), with the caveat beside it
   that the rows as built hop whole and lack (A2), so for the rows'
   dynamics W stays the declared identity of record 270; never two
   formulas side by side, never a meeting; Eq. 14 then "the Inside identity of the conversion,
   shown to second order", the rows still hopping whole beside it (the
   reading's identity, not yet the rows' dynamics), one ledger row
   "shown (second order)". Newton Outside after Section 4's ground
   paragraph when part 7 lands (ten lines, the ground stays fan).
4. Every result placed as Outside = the image of Inside under the
   conversion, and the pattern Outside -> Inside -> Outside written per
   phenomenon with formulas alone (the owner's word): the two slits
   (two rows, m = 2, the phases per Link, the merge with the cancel at
   Delta = N / 2, R(x) = 512 ((C[p_1] + C[p_2])^2 + (S[p_1] +
   S[p_2])^2) proportional to 1 + cos Delta, the rungs, the count
   b_x - b_(x-1); the dark pixels' rung of width 0 "does not pass"), one
   slit (no pair, flat within the fan's grain), Mach-Zehnder (the two
   phasors adding at one port and cancelling at the other, the tables'
   1681 / 1682 and 1 / 1682, the clicks 64 / 0), the pair, Malus, GHZ,
   the clock in a crowd, each in about six lines; the visibility clause
   K(Delta) / K(0) restored in Section 6.
5. Table 2: the seven rows that only confirm a shown formula (the pace,
   the click's power, Mach-Zehnder, the marginals, GHZ, Malus, light
   beside a mass) become one sentence of Section 8 and a list in
   Appendix C with series and fingerprints; the six that no formula
   gives stay (D3, series T's 1.907, J1 and J2, series S, Young's 0.966,
   S(N)'s seven grains, shown and measured). Table 3 stays whole.
6. The wording rule on every result: SHOWN (algebra under the
   assumptions the ledger's third column names; "Theorem" and "proved on
   the GameBoard" for Theorems 1 to 6, about the board), MEASURED (a run
   Inside read Outside), or both; everything Outside "shown", "arrives
   at", "comes out under the named assumptions", never "proves"; every
   result sentence names the KNOWN form it recovers with its citation
   and, in the same sentence, what is OURS; "new" only where the audit
   says it, "not new" said plainly.
7. The cost: about thirty-five lines in beyond the framing (the argument
   net plus four, the quantities' table and the identities eight, the
   Inside | Outside table fifteen, the step paragraph eight, Newton
   Outside ten, the four worked phenomena twenty), about forty out
   (Table 2's seven rows, Section 6's L2b narrative, two paragraphs of
   Sections 3 and 8, the symbols table's single-use letters to page 30's
   free lines); net about plus twelve in the body; 30 pages or, if parts
   6 and 7 exceed twenty-five lines together, 31 or the S(N) figure back
   to a row, the compile deciding and the count reported before any push.
8. For the record, not yet the paper's: the owner's foundational
   assumption (records 799, 802): in the real world we are built of
   clicks; to move a click from place to place one puts it into the board
   and takes it out; that is motion in the real world, and the
   transformation must be done there; the basis is Inside, and we are
   operated Outside, by emitters and clicks. A mathematician checks that
   it holds; it enters the paper only from the merged texts.

### B'. Two words folded into plan B (2026-09-22, the Boss at 08:00Z and the owner to the writer)

1. THE 24 TRANSITIONS MUST ENTER THE PAPER (the owner's word, binding).
   B.1's "when" is not optional: the abstract's second sentence one
   clause; the introduction's five steps (the argument in order reaches
   the group in its fourth paragraph); Section 2 opening with the road
   from the cells to the algebra and closing with "When the transition
   was made"; Appendix C the dated history in full, given the room it
   needs (the owner's "everything gets shorter" applies to what is
   superseded, not to this history). The framing for the text, the
   Boss's two clarifications: the 24 entries are the road (each physical
   thing, the algebraic object it became, when, where in the code, the
   reading that showed it), not the group; the group is where the road
   arrives, at entry 17 (the click without amplitudes: the group ring
   Z[Z_N], the cyclotomic integers, the complex numbers leave) and entry
   23 (the click theorem: the structure-preserving maps between click
   families are the Lorentz group up to scale). Source:
   docs/designs/algebra_transition/HISTORY.md at 8eaaf61a (PR #793),
   plus the re-pointing commit of record 788 if it lands before the
   merge; the paper takes the entries only from the merged text. The
   cost: Appendix C grows by the 24 entries at one line each (about
   twenty-six lines), on page 30's free lines and, if they do not
   suffice, the symbols table's single-use letters go; the body's cost
   is B.1's.

2. THE GAMEBOARD AS A SYSTEM OF INFORMATION TRANSFER (the owner's word
   to the writer: "something very, very important for the paper: the
   paper as information transfer; Inside, the GameBoard, is a system of
   information transfer, how messages pass, rows, attributes; explain it
   very cleanly, with an example or two; that is the explanation of the
   passage from physics to modern algebra; see how other papers do it").
   The place: the opening of Section 2, before the road from the cells
   to the algebra (B.2), so that the road starts from messages. The
   draft, in the paper's voice, about twelve lines:

   "The GameBoard is a system of information transfer. Its only objects
   are messages, the rows: a row is a tuple (Node, direction, age,
   phase, emitter, content per unit, record, label, amount,
   multiplicity), and a Link is a channel that carries at most one step
   of a row per interval in each direction. Nothing else exists Inside:
   no field at a Node, no register, no memory beyond the rows present.
   Each interval does six things to messages and nothing else: it moves
   a row one Link along its digital line (the translation), turns its
   phase (the translation on the circle), splits it at a splitter into
   rows with integer weights (the multiplication by a declared table),
   rotates a labelled pair (an integer matrix), merges the rows that
   meet at a Node with equal words, opposite phases cancelling (the
   addition), and, at a detector, reads a record once by one comparison
   and deletes it (the evaluation and the count). The books say that no
   message is lost or made in transit: released equals in transit plus
   absorbed plus escaped plus cancelled at every interval. Written down,
   a message is a basis element of a free Z-module, the passage is the
   translation group's shift, the split and the rotation are integer
   matrices, the merge is the group ring's addition, and the read-out is
   one bilinear form: the passage from physics to modern algebra is the
   passage from messages with attributes to vectors with coordinates,
   and the six things an interval does are six linear maps and one
   comparison."

   Two examples, about eight lines, from the paper's own numbers:
   (a) one message in flight, the hand-worked update already in Section
   2: a row on +x with the accumulator's rate 128 against the wall 220
   crosses Links at the intervals 1, 3, 5, 7, 8, five Links in eight
   intervals, its phase turning at each Link; the message's whole
   history is the closed form floor(s_0 + r t), nothing kept at a Node.
   (b) one message split and merged: at the balanced splitter one row
   of amount 1 becomes two rows of amount 1 and multiplicity 2 on two
   arms; at the second splitter the two meet at each port, at one port
   with equal phases (the words add, amount 2) and at the other N / 2
   apart (an equal pair is no row, the message cancels); the detector
   at the first port reads the record and deletes it: the dark port is
   the cancelled message, the bright port the click, 64 of 64 births
   (series L, Mach-Zehnder). The pair adds a third example in one line
   if room allows: two labelled messages of one record, gathered once.

   How other papers do it, for the positioning sentence: the lattice
   gases of Hardy, de Pazzis and Pomeau and of Frisch, Hasslacher and
   Pomeau carry particles as bits on links with collision tables and
   recover the Navier-Stokes equations in the limit; Toffoli and
   Margolus's cellular automata machines are lattices of local update
   rules on bits; the quantum cellular automata surveyed by Arrighi are
   local unitaries on a lattice of cells; Shannon's channel is the
   message and its capacity. The GameBoard is of that family, a lattice
   of message channels with one message step per interval per
   direction, with two differences the paper states: the messages carry
   a phase on a bounded circle and an integer amount, and the only
   read-out is the click. Cost: the twelve lines plus the eight, minus
   the six of Section 2's present "The state" paragraph, which the
   message tuple replaces, and the "In the code" paragraph's four,
   folded into the six things; net about ten, in section B.7's budget
   or the compile's word. Nothing applied until the owner's GO.

### C. The circularity audit (the check of skills/paper-coordinator/SKILL.md; the owner's word to the writer)

For each formula: the inputs, the road, whether the form was put in;
KNOWN and OURS; the paper's word.
- Eq. 1, the map: a DEFINITION. Known: none. Ours: the map, a rate and
  a wall per component. New as a definition.
- The 48 and the 24: DERIVED from the six Ports.
- The books, continuity: DERIVED (the carry a bijection, the conjugate
  transposes; P3, P5). Known: conservation laws. Ours: the exact integer
  identity.
- The pace bound 1 / sqrt 3: DERIVED (Cauchy-Schwarz); the value attained
  carried by the wall T_D, a choice among few (P9). Known: the lattice
  Boltzmann sound speed, the Courant bound (cited). Not new.
- No dispersion: a POSTULATE (P9), not forced (the derivation's 27).
- Gauss: DERIVED under the world condition. Newton, Coulomb, the
  retarded potential, Poisson: RECOVERED under the shell average from
  the walk and the bilinear push, no 1 / r^2 among the inputs; G named,
  N_w an input. Known: physics' forms. Ours: the integer road and the
  named condition.
- The clock's 1 / (1 + a_tau) and 1 / r: RECOVERED; the age moment P9;
  the calibration a DICTIONARY INPUT. Known: gravitational redshift.
- The click's quadratic form (Theorem 4): DERIVED from (a) to (e), the
  square carried by (b), the balanced splitter's conservation; the
  cosine carried by the tables (P7, a declared input); the harmonic
  constants free; P10. Known: Born, Gleason. Ours: the lattice Gleason
  on Z_N without dimension, the multiplicity rule. New as a theorem.
- Born's bound 1 / N: DERIVED from the rung with the uniform birth phase.
  New (finite N).
- The exact marginals (Theorem 5): DERIVED from the rotation rows'
  orthogonality. Known: no-signalling. New in the finite form.
- S(N), Tsirelson (Theorem 6): DERIVED from the rungs and the tables;
  the cos(a - b) correlation carried by the rotation tables, so 2 sqrt 2
  is RECOVERED as the standard consequence of cosine correlations under
  a quadratic weight, not a new bound; the finite-N rational, the
  plateau 181 / 64 (measured at seven grains) and the fixed-table limit
  186034 / 65773 ours and new.
- Planck, de Broglie: IDENTITIES UNDER THE DICTIONARY h = h_q N, an
  input; circular by construction, said so; not new.
- The uncertainty bounds: ALGEBRA on Z_N under a HYPOTHESIS (the circle
  as position); known (Donoho-Stark, Maassen-Uffink); not new.
- Young's spacing: RECOVERED in the fan's limit.
- Eq. 14, W = E_0^2 + 3 p.p: two uses, two words (the Boss's word of
  08:05Z on the click frame's section 7 at 1dd81fef, the reviewer
  AGREED, yes to second order). As the conversion's identity under (A1)
  and (A2): SHOWN to second order, no square declared in the chain: the
  walk's exact invariant cos omega = cos m cos kappa gives omega^2 =
  m^2 + kappa^2 - m^2 kappa^2 / 3 + O(6); the law's own Planck map (the
  dictionary's identities, an input: E = h_q n / d = h_A f, omega =
  2 pi n / (d N), p = hbar kappa per Link, E_0 = hbar m; the load
  identity 3 h n = Q S d) gives E^2 = E_0^2 + c^2 p^2; the whole unit
  E' = E / c^2 gives W = E'_0^2 + 3 p.p with 3 = 1 / c^2 = d exactly on
  the body diagonal (2.954 / 2.971 / 3.000 by direction, the root's
  rounding); the order: relative corrections m^2 beta^2 (m^2 beta^2 / 3
  on W, / 6 on E' and r), exact in the continuum limit; Lorentz enters
  only through (A1) and (A2). The inputs the audit names: (A1), (A2),
  the walk's invariant, the dictionary (Planck, de Broglie, the load
  identity), the tables' rounding. For the rows' dynamics: DECLARED
  (record 270), because the rows as built hop whole and lack (A2). The
  paper's word per use: "shown to second order (the conversion's
  identity, section 7)" where the step above is read from clicks under
  (A2); "declared (record 270)" where the rows' hop is meant; never
  "derived". Known: E^2 = E_0^2 + p^2 c^2. Ours: the integer W compared
  and never rooted, the gate E_0 / E', the factor 3 as 1 / c^2 = d, the
  order named. Plan A's line stays "an Inside formula on the record";
  plan B says the two words at their places.
- Lorentz, the click theorem: ARRIVED AT from (A1) and the one line
  k_AB = k_BA, special relativity's two postulates in the click
  language (Einstein 1905; Alexandrov-Zeeman); not circular, no
  transformation declared. Known: the group. Ours: the click language,
  (A2), the detector's own rate, the fact that the law lacks (A2). The
  sentence saying so is in the framing commit.
- The two Doppler factors: DERIVED on the counts (rung 1). Known:
  Bondi's k-calculus. Ours: the law's r = 1, the measurable 1 - v^2, new.
- The equivalence principle: DERIVED at rest (the step rule divides by
  the content); the scale symmetry MEASURED (D3). Known: Galileo.
- The entropy identity: a DEFINITION of the coarse graining with the
  click's one deletion. Known: Boltzmann. Ours: the count of torus
  points at the click, new as an identity of the click.

### Cut on 2026-09-22 (one line each: what, and why)

- The first frame paragraph draft and its "two notes" (the old sections
  3 and 5a): its "our reality" and "the real world" replaced by "Outside,
  the game above the board" (record 768); its detector count "advancing
  once per packet" and then "the count of intervals stretched by what
  arrives" replaced by the owner's sentence (a detector's clock is what
  it emits and receives back on its own record); its first sentence
  replaced by record 753's shape and then by the packet moved Inside
  (record 773). The canonical paragraph is A.6.
- The first three sentences (the old section 2, the pre-753 wording) and
  their 149c4dc6 copy: the paper takes the merged section 0's at PR
  #769's SHA; the copy is not the source.
- "Eq. 14 is not needed for the reading and stays a hypothesis under
  its own identity" and "a hypothesis beside the law that the frame does
  not need": replaced by "an Inside formula on the record, read by no
  detector, whose Outside formulas the conversion gives" (record 777),
  and by "shown to second order" in the reshaping.
- The old section 4 ("what it replaces or retires") and the old sections
  5, 6, 7(6), 8(3), 10 (the cost counts and trim lists): superseded by
  the trial's compile at 30 (A.7) and the reshaping's one budget (B.7);
  the trims live in the writer's scripts.
- The first framing list (the old section 7) with "no claim that nature
  is so" and "our reality": replaced by Inside and Outside and the
  gentler tone (record 768, the owner's words to the writer); its title
  candidate with capitalized Inside / Outside replaced by the lowercase
  one (section 9's decision, now A.1).
- "The Lorentz-road sentence goes into the reshaping commit": moved to
  the framing commit by the Boss's word of 06:20Z (A.6).
- Table 2's rows described as measurements that the algebra shows (the
  pace, the click's power, Mach-Zehnder, the marginals, GHZ, Malus, light
  beside a mass): reclassified SHOWN with the run as the confirmation
  (B.5); "measured" stays only where no formula gives the number.
- The old 8, 8a, 8b, 8c, 8d, 8e as separate sections: merged into B;
  the audit's first form merged with its known / ours columns into C.
- The old section 9's reasons for the title: kept in one line (A.1).

## Applied (2026-09-22, the owner's GO through the Boss at 08:15Z): commit A, the framing

Plan A applied as written, one commit through cut30/corrections.py
(the writer's ten rounds folded into the table): the title, the
abstract's first sentences, P11, the reading rule, the sweep, the two
ordering sentences, the frame paragraph with the click frame's three
sentences at 1dd81fef (PR #769, pending merge; "Outside, the game above
the board" for "our real world", record 768) and the Lorentz-road
sentence, the limits paragraph's and Table 4's replacements, the boost
sentence, the c-postulate row, row 4b, the bibitem clickframe; 30 pages,
the split 25 / 2 / 3; the pinning test and tools/check.py pass. Commit B,
the reshaping, follows on the same branch. The citation swap to the
merge SHAs is one small commit when they land.

## Applied (2026-09-22, the owner's GO through the Boss): commit B, the reshaping

Plan B applied as written through cut30/corrections.py, one commit: the
abstract's why clause; "Why physics behaves like modern algebra" (five
steps) in place of the claim paragraph; Section 2's opening, "The
GameBoard as a system of information transfer" (the message tuple, the
six things an interval does to messages, the books, two messages of the
paper, the passage to the algebra, the family of lattice gases,
cellular automata machines, quantum cellular automata and Shannon) and
"The road from the cells to the algebra" (how mass, charge, momentum,
the phase, the amount, the multiplicity, the age, the field and the
tables entered); the identities; "When the transition was made"; the
ledger's caption; "Interference, by the formulas alone" (two slits, one
slit, Mach-Zehnder, what passes and what does not); Section 8's seven
confirmations named once; the discussion's "The step beneath and the
step above" (W the axiom, the conversion the map, Einstein's relation
its image, shown to order m^2 beta^2 as the conversion's identity
under A1 and A2, declared for the rows' dynamics, record 270), "The
smallest thing above" (the quantum of the Outside step from A1 and the
click's definition), "Newton from the small step" and the Inside |
Outside conversion table of nine rows with the reading's kind on each;
the known / ours sentence at the end of "What is proved"; Appendix C's
seven confirmations and the 24 dated transitions; the four sources at
their branch heads, "PR #NNN, pending merge" (click frame 1dd81fef
#769, light-outside 8bd4f811 #791, einstein-outside c25efd01 #792,
HISTORY.md 8eaaf61a #793); Table 2's seven shown rows out.

The count: the first compile was 35 pages; B.7's named cuts (Section
6's L2b narrative to four lines, Section 3's registered count and the
grain's bound to Table 3's row 5a, the symbols table's single-use
letters, Table 2's rows now carried by Table 3 and the conversion
table) and four rounds of trims of run narratives (series T in one
sentence, the GPS term to row 12, the excluded grains, the seven unrun
rows by number, the Courant sentence, the fingerprints named once,
Appendix C's reproduction paragraphs) bring it to 34 pages, the body
through 28, the references 29 to 31, the appendices to 34; no overfull
vbox, no undefined reference. The plan's budget (30 or 31) is not met:
the "in" items came in about three pages longer than B.7's thirty-five
lines, the owner's content (the information-transfer opening, the road,
the five steps, the step paragraphs, the table, the phenomena, the 24
transitions) being most of it. The count is reported as the order
allows. What a further cut could take, each on the owner's word and
none taken here: the abstract to about 1200 characters (six lines); the
page break before the references (about twenty lines of page 28); the
remark on dispersion (Section 3, eleven lines); Table 3's cells (about
eight lines); the ledger's rows already shown in the conversion table.

Two defects found at the compile and fixed before the commit: the new
bibitem shannon1948 duplicated the existing one (removed); the
conversion table's columns were 17 pt wider than the text (narrowed).
One number corrected: the conversion table's clock row named "series X
1.0000", a reading the register does not hold; it now carries series
X's registered k = 0.9089 at r = 4 for the pin 0.9108 (docs/EXPERIMENTS.md,
series X, on main at 7ef735c8; record 661). NUMBERS.md carries the
plan-B numbers (the count, 1/c^2 by direction, the click frame's chain,
the 24 transitions, series X). The citation swap to the merge SHAs is
one small commit when the four PRs land.

## Applied (2026-09-22, the owner's words of records 817 and 822 through the Boss): commit C, the roads, the families, the new formulas

Three things folded, one commit through cut30/corrections.py, on top of
commit B: (1) record 817, "show how we arrived at Einstein, at Lorentz
and at the step-above formula, without deriving from them": the
discussion's paragraph "The road to each, and the check that nothing
was derived from them" (the three roads, A3 named, the words, the
sentence that Einstein's, Lorentz's and the Outside step's formulas
appear only as the thing compared with) and Table 8, the check of the
roads, in the new Appendix D: one row per formula arrived at (W to
second order, the boost, the factor, 1 / gamma, the composition, the
energy-momentum relation, the Outside step, its quantum, Newton's step
as the limit) with the inputs used, the file and line where the chain
starts (the click frame on main at 70e9781a; Einstein Outside at
d1b4af84, whose section III is the same check made in the source) and
the word; how the check was made: each chain read against the two
sources' certification tables. (2) record 822, the mass families in
the algebra: Section 2's paragraph "The families in the algebra" and
Table 7 in Appendix D, every family of the register (the shipped
definitions and the inline ones, the mathematician's audit) with its
declared integers, its algebraic object (the frame's section 9, the
history's table), when it entered (the record), the verbs that act on
it and the click that reads it by kind; "not named" and "no detector
reading registered" where the tree does not fill the cell; the mass
angle a world's declaration (the rest pair), not the family's. (3)
record 822, the new formulas: the discussion's paragraph "What the
Inside step gives Outside that the continuum cannot state", seven
items, each with its click and kind (the quantum of the Outside step
and the velocity's 1 / (k (k + 1)); Bell's rounding term and the
plateau; the perihelion's order-beta term, FAIL and NOT MADE with its
pin; the grain tau_L c = 0.993; the anisotropy of c; the equivalence's
constant with n S = d as the condition and the register's n S / d = 16
stated; light's bending, 0 on the law and the key's form NOT COMPARED,
the route the owner's decision). The citations: the click frame on
main at 70e9781a (PR #769 merged, the file identical to 1dd81fef);
click-frame-2 at 097b2006 cited for the W phrase, pending its PR;
light-outside at ceb6e066, einstein-outside at d1b4af84,
algebra-transition at 928f056d, each "pending merge"; Grangier quoted
on row 2b (PR #797 merged). The count: 38 pages, the body through 30,
Appendix D two pages; the tables in the appendix and one paragraph
each in the body, as the Boss allowed; nothing else cut. NUMBERS.md
carries the new numbers.

## Applied (2026-09-22): the citation swap for the three merged sources

Click-frame-2 (PR #801 at af051aaf), Einstein Outside (PR #792 at
e8432e6c) and the algebra transition (PR #793 at 412f5c61) cited on
main; the click frame's lines stay at 70e9781a (a commit on main whose
lines Table 8 cites). Table 8's Einstein Outside lines re-checked
against the merged file's own check table (Theorem 1 :355, II.1 :647,
II.3 :733, II.6 :887, section 3 :481, :497, :510, :554; the words
unchanged on the cited rows); the five places the later commits
changed were read: the composition pin, series G's grains and II.2's
E = h_q s are not cited by the paper; Theorem 1's order is stated in
its statement, not in the paper's row; the perihelion's wording is
taken over ("larger than nature's by 1 / (6 pi beta), about 330 times
at Mercury's pace if its coefficient is of order one; FAIL pinned in
order and symmetry, the coefficient NOT MADE"). Light Outside's swap
waits for its merge SHA, as the Boss ordered.

## Applied (2026-09-22): the last citation swap, Light Outside merged

Light Outside cited on main at a62441fb (PR #791 merged; its verdict
rows unchanged since 186f0030 but the luminosity pin's label). The
paper cites no line of it, only its verdict row on the speed of light
by direction (2.954 / 2.971 / 3.000), which is unchanged in the merged
file; the words unchanged. In the same commit one record fix of the
writer's own: NUMBERS.md's parenthetical for tau_L c = 0.993 said "1.72
times the heading's pace 0.5818", whose product is exactly 1; the
factor is 1.72 = 110 / 64 times c = 1 / sqrt 3. Every source of the
paper is now on main; nothing else changes without the owner's word.

## Applied (2026-09-22, the owner's word to the writer): from an Inside formula to an Outside formula, family by family

The owner, in the writer's session: "it must be shown how from the
Inside formulas one gets the Outside formulas, with the families and
the attributes." One commit: the discussion's paragraph "From an
Inside formula to an Outside formula, family by family", three chains
written in full with the row tuple's attributes named at each step
(light through two slits: the family light, the two rows' direction,
age and phase, the merge in the group ring, the evaluation and the
rung, Outside the count per pixel and Young's spacing, L2b 23.5 for
23.3; a massive body's clock and fall: m and mass, the content, the
momentum and the counts table, the crowd's rows' age and amount, the
drive's pace and the age wall, the lamp's births counted at a detector
at rest, Outside 1 + z and the ratio of two shifts and the birth's Node
per count, series T 1.907 and D3 138 of 139; the pair: sa and sb, the
labels on two arms, U_a on the label pair, J and R = J^2, the one
gather and the rung, Outside c_++ and S(N), 2.75 and 32/64), and the
closing sentence that Outside holds counts and Nodes and none of the
attributes themselves. The conversion table's Inside cells open with
the family and the attributes each formula reads; its caption says so.
No new number; 39 pages, the count reported. The Boss was told before
the commit (the writer's line of 07:52Z).

## Applied (2026-09-22, the Boss's condition on the owner's GO): the eighth formula

The Boss's GO of 08:20Z on the family-by-family paragraph (already at
8f2ce077) carried one condition: keep the eighth formula honest, the
two-slit spacing lambda = c N d / n, either said absent or added as one
line if its reading is registered by kind. Its reading is registered
(L2b: the bands' centres 23.5 pixels apart for the exact two-path law's
23.3, DETECTOR; Light Outside II.6 on main), so it is one line in
Section 6's "Interference, by the formulas alone", after Born's rule,
with Young's lambda D / s named on the comparison side only. 39 pages.
QUANTA.md and LIGHT.md (PRs #805, #810) are cited when the new-formulas
section is next touched, as the Boss ordered, not here.

## Applied (2026-09-22, the owner's word to the writer): dark energy's shape, derived from the model's own computations

The owner: "make sure the dark energy formula, derived from our own
computations, is in the paper." It was not (only row 3's q_0 = -0.108
FAIL). One commit: item (viii) of the discussion's "What the Inside
step gives Outside that the continuum cannot state": the apparent
acceleration q_eff = -2 g_1 / (1 + g_1) from the emitters' clock stretch
over the detector's own, a property of the conversion with nothing
accelerating on the board (DARK_ENERGY.md on main at c8ac2ffb, SHOWN in
form, rung 2), the shape read by series G (DETECTOR) and the coasting
throw's q = -0.108 (G2, MET; FAIL against -0.53), and in the same font
what the law does not give: the size an input, the sign from its own
accumulation the opposite, the brightness one factor short (row 11a
FAIL); the model has no cosmological constant and states the supernova
diagram as a failure, not a resolution. Since the section was touched,
QUANTA.md (477daa1d) and LIGHT.md (7370d524) are cited on main as the
full lists, as the Boss ordered. 39 pages, the count reported.

## Applied (2026-09-22, the owner's word to the writer): the platform for formulas, and the discussion in one order

The owner: "the important part is to explain how one arrives at the
formulas from our basis, from Inside to Outside algebraically and also
through the simulator, detectors in motion or a detector at a Node;
give them a platform for formulas; make sure the paper is coherent
like other papers." One commit: (1) the discussion's second paragraph,
"The platform: how a formula is arrived at, by the algebra and by the
simulator": the algebraic road's three steps (the Inside step on the
family's attributes, the conversion, the Outside form with its rung
and order, the known form on the comparison side only) and the
simulator's road (the world file, the pin before the run; a detector
at a Node, series L, Q, T, X; a lamp in motion read at a detector at
rest, G, G2, S, the moving detector's own one-way ratio a reading not
yet made; a lamp on a body and a line at rest, D3, T; the kind), the
rule that a formula enters with both roads and nature on the
comparison side, and the recipe for a reader's further formula; one
sentence each in the abstract and in the introduction's "How the
simulator led to the results". (2) Coherence: the discussion reordered
into one argument, the frame, the platform, the step beneath and
above, the smallest thing, Newton, the road to each and the check,
family by family with the conversion table, what the Inside gives that
the continuum cannot, then what is proved, what the runs support, the
distance, the limits, positioning; text moved, not rewritten; the
duplicated statements of the Outside step's quantum and of c's
anisotropy in the new-formulas items reduced to pointers; the light
chain cites Section 6's formulas. No number moved, no claim changed;
39 pages. The Boss was told before the commit (08:05Z).

## Applied (2026-09-22): the Boss's conditions on the platform paragraph

The Boss's GO (08:35Z) on the platform and the coherence pass reached
the writer after the commit 38d569d9; its conditions are met in one
small commit: every reading the simulator's road cites carries its
kind (L, Q, T, X, G, G2, D3 DETECTOR; series S the face clicks DETECTOR
and the self-creations' ticks GAMEBOARD), a number of the board's
state named a GAMEBOARD diagnostic, and the moving detector's own
one-way ratio "a reading NOT MADE" until the physicist's step 4 and
the transponder worlds land. The count 39, reported; no cut.

## Step A (2026-09-22, the owner's word of record 852 through the Boss, 08:45Z): the claims table and the cut table, PLAN.md only

The owner: "make sure the paper is shortened to 35 pages and claims
only established things that will not bring us down." Step A is this
record; step B, the cut, waits on the Boss's word after the
physics-rule reviewer's adversarial read of the claims table. The
paper at 53e07e4c is 39 pages; nothing in it changes here.

### A.1 The claims table

Every claim a hostile referee could test, one row each. Support:
PROVED (a theorem in the paper or in a cited derivation on main),
READ (a detector's click in the register, DETECTOR), SHOWN IN FORM
(an algebraic form with a declared input, rung 2, not read), DECLARED
(an input of the law or a world file), NOT COMPARED / NOT MADE / FAIL.
Verdict: KEEP AS IS / KEEP WITH THE STATUS WORD (the word in the same
sentence) / CUT. The words: "follows", "recovered" where a form was
put in; "derived" only where none was (record 817); "matches nature",
never "is nature".

| # | The claim, in the paper's words (section) | Support | Verdict |
| --- | --- | --- | --- |
| 1 | One update law of bounded integers propagates records; written down, the rules are a cyclic group, a group ring, integer matrices, an evaluation at the roots of unity and a shift (abstract; Section 2) | PROVED (the definitions of Section 2; the ledger) | KEEP AS IS |
| 2 | Physics above the board is arithmetic on counts; every measured quantity a count or a ratio of counts (abstract; intro's five steps) | SHOWN (the click's definition, P11; Theorem 3 of Einstein Outside on main) | KEEP WITH THE STATUS WORD ("a theorem of A1 and the definition of Outside") |
| 3 | The group of the six Ports and its 24 rotations (Section 3, Theorem 1) | PROVED (Appendix A) | KEEP AS IS (the proof cited to DERIVATIONS_BEAM on main, Appendix A's text cut, A.2 row 14) |
| 4 | The books' conservation; the lattice continuity equation (Section 4) | PROVED (the books, exact); the continuity equation's differential form a limit | KEEP WITH THE STATUS WORD ("its differential form in the limit") |
| 5 | Gauss's law of a free family's flux under its world condition (Section 4) | PROVED (exact on the GameBoard) | KEEP AS IS |
| 6 | The split's isometry; the injectivity of the interval between clicks (Section 6, Theorems 2, 3) | PROVED (Appendix A) | KEEP AS IS |
| 7 | The pace of every direction isotropic within 1/T_D; c = 1/sqrt 3 the largest isotropic pace the two rules allow; the value attained a limit of the grain (Section 3, Proposition) | PROVED (the Proposition) + READ (series Q, 290 of 290, DETECTOR) | KEEP AS IS |
| 8 | The table sits at the supremum: T_D = floor(sqrt(3 |D|^2 N_l^2)) (Section 3) | DECLARED (P9, a rule chosen among few) | KEEP WITH THE STATUS WORD (already "a rule chosen among few, not a consequence") |
| 9 | No dispersion at any phase rate; the GRB 090510 bound met (Section 3, the remark) | a consequence of the postulate P9, no run | CUT (the remark to one clause of Positioning: the pure-shift automaton, Meyer's theorem cited) |
| 10 | The click's weight is a positive quadratic form of power 2; the lattice Gleason (Section 6, Theorem 4) | PROVED (a sketch in the paper; the full steps DERIVATIONS_BEAM 6.5 on main) | KEEP WITH THE STATUS WORD ("sketch; the steps in full in the derivation on main") |
| 11 | The power window [1.917, 2.012) from the registered cells: an implementation gate, no evidence about nature (Section 6; Table 3 row 2c) | READ (the cells) | KEEP AS IS (the status already in the sentence) |
| 12 | The harmonic constants c_j are not derived; the least-rank click is an axiom of the apparatus (P10) | DECLARED | KEEP AS IS |
| 13 | Born's rule as a frequency to 1/N (the rung); the cumulative to 1/(2N) (Section 6) | PROVED (an integer identity of the floor) | KEEP AS IS |
| 14 | Interference by the formulas alone: two slits, one slit, Mach-Zehnder 1681/1682 and 1/1682, 64/0 (Section 6) | PROVED (identities of the tables) + READ (L, mz_equal 64/0, DETECTOR) | KEEP AS IS |
| 15 | The two-slit spacing lambda = c N d / n; Young's lambda D / s in the paraxial limit (Section 6) | SHOWN IN FORM, rung 2 (the fan) + READ (L2b, 23.5 for 23.3, DETECTOR) | KEEP WITH THE STATUS WORD ("rung 2, the fan; Young's on the comparison side") |
| 16 | Planck's and de Broglie's relations as identities under the declared dictionary (Section 6) | DECLARED (identities of the release) | KEEP AS IS (already "as identities") |
| 17 | The uncertainty relation from the same evaluation: the support bound, the entropic bound, Kennard's form in the limit (Section 6) | mathematics of Z_N on a stated identification that is a hypothesis (the circle as position); nothing read | CUT to a pointer of three lines (the identification a hypothesis, the bounds the transform's, DERIVATIONS_BEAM 22 on main) |
| 18 | The exact marginals; no-signalling as an identity of the integers (Section 7, Theorem 5) | PROVED + READ (32/64 in every bin, DETECTOR) | KEEP AS IS |
| 19 | S(N) an exact rational; abs(S(N) - 2 sqrt 2) <= 8/N + 0.0444; the plateau 181/64; above the bound at 16 and 32 (Theorem 6) | PROVED (the proof in the text, its constant proven) + READ (seven N, DETECTOR) | KEEP AS IS |
| 20 | One prediction: S = 181/64, inside Poh et al. at 1.05 standard errors, under three assumptions stated (Section 8) | READ + a comparison under three assumptions | KEEP WITH THE STATUS WORD (the three assumptions in the same sentence, as now; "a compatibility, not an advantage") |
| 21 | The inverse square as a shell mean; Newton's law with G = K eta / (4 pi N_w); the equivalence (Section 4) | SHOWN IN FORM, rung 2 (the shell mean) + READ (D3 138 of 139, 1.997, DETECTOR); G not read | KEEP WITH THE STATUS WORD ("the shell mean; the inverse square's decisive reading NOT MADE") |
| 22 | Coulomb's law and the one constant (Section 4) | SHOWN IN FORM; no detector reading registered (the coupling worlds) | KEEP WITH THE STATUS WORD ("no detector reading registered"), the paragraph condensed |
| 23 | The retarded potential and Poisson's equation from the two fields of one stream (Section 5) | SHOWN IN FORM, rung 2 (the limit of every direction) + READ (series X, k(2)/k(4) = 1.0029 for 1.0039, DETECTOR) | KEEP WITH THE STATUS WORD ("in the limit of every direction; the interior flat within the tolerance after a detector") |
| 24 | The clock's redshift: first order agrees with general relativity under the calibration a_tau = G M / (r c^2); at second order a different law, no horizon (Section 5) | SHOWN IN FORM (the calibration an input) + READ (series T, 1.907 for 1.909, the form at two Nodes, DETECTOR); the strong-field reading not registered | KEEP WITH THE STATUS WORD ("the calibration an input; the strong-field form not read") |
| 25 | Light: no optical metric; the flight blind; the bending 0.000 (Section 5; item vii) | READ (series K, DETECTOR); FAIL against 1.75 arcseconds | KEEP AS IS (a FAIL stated) |
| 26 | The click theorem: the transformations between click families preserving A1 and A2 are the Lorentz group up to scale; Lorentz up to corrections of order m^2 v^2 (the frame paragraph, quoted) | PROVED in the cited derivation (the click frame section 0 on main); assumed of the world, shown of the conversion | KEEP WITH THE STATUS WORD (the quote shortened to its theorem sentence; "Lorentz of the world is assumed, what is shown is that the conversion brings it") |
| 27 | The law as built meets A1 and not A2; its counter runs at the rest rate; the two one-way factors apart by 1 - v^2 (the frame; Table 3 row 4b) | SHOWN IN FORM + READ (row 4b, 0.2636 FAIL, DETECTOR); the one-way ratio NOT MADE | KEEP AS IS (the FAIL and NOT MADE stated) |
| 28 | W = E_0'^2 + 3 p.p shown to second order as the conversion's identity under A1 and A2, no square declared in the chain; declared for the rows' dynamics (record 270) (the step paragraph) | PROVED to second order (the click frame section 7 on main); DECLARED for the rows | KEEP WITH THE STATUS WORD (both words, as now) |
| 29 | Einstein's relation follows from the Inside alone; 1/gamma, the composition, the Doppler factors (the step paragraph; Table 8) | SHOWN (Einstein Outside on main, its section III) | KEEP WITH THE STATUS WORD ("follows to second order under A1 and A2; Einstein's on the comparison side") |
| 30 | The quantum of the Outside step; why the world above is quantized (the smallest thing) | PROVED (Theorem 3 of Einstein Outside on main; no run); the velocity's quantum NOT READ | KEEP WITH THE STATUS WORD ("a theorem of A1, A3 and the conversion; not read as such") |
| 31 | 1/c_D^2 = 2.954, 2.971, 3.000 by direction (the smallest thing) | a computation on the flight table + READ (Q) | KEEP AS IS |
| 32 | Newton from the small step: the fall, the equivalence, Kepler's ratio, the clock in a crowd come out Outside (the Newton paragraph) | SHOWN IN FORM, rung 2 + READ (D3, T, X) | KEEP WITH THE STATUS WORD ("the shell mean; the inverse square's reading NOT MADE") |
| 33 | Nothing was derived from Einstein's, Lorentz's or the Outside step's formulas (the roads paragraph; Table 8) | the check table against the sources' certification tables | KEEP AS IS |
| 34 | The three chains, family by family (light, a body, the pair) | PROVED (the identities) + READ (L2b, T, D3, L) | KEEP AS IS |
| 35 | Item (ii): Bell's rounding term and the plateau | PROVED + READ | KEEP AS IS |
| 36 | Item (iii): the perihelion's order-beta term, FAIL on the law, pi beta^2 under the identity, the coefficient NOT MADE | SHOWN IN FORM (its order and symmetry); FAIL; NOT MADE | KEEP AS IS (a FAIL stated as a difference) |
| 37 | Item (iv): tau_L c = 0.993 on a heading | a computation | KEEP AS IS (folded into item vi's sentence) |
| 38 | Item (vi): the equivalence's constant (n S / d)(g Y / c^2), Einstein's when n S = d; the register's n S / d = 16; the reading NOT MADE | DECLARED; NOT MADE | KEEP AS IS |
| 39 | Item (vii): the bending under the key optical, 2 c_f (n S / d) G M / (c^2 b), NOT COMPARED | SHOWN IN FORM under a hypothesis; NOT COMPARED (the generic entry in work, records 847 and 851) | KEEP AS IS (NOT COMPARED until the entry lands) |
| 40 | Item (viii): dark energy's shape q_eff = -2 g_1 / (1 + g_1) a property of the conversion; the size an input; the sign from the law's accumulation opposite; the brightness a FAIL | SHOWN IN FORM, rung 2 + READ (series G's shape; G2 -0.108, DETECTOR); FAIL (rows 3, 11a) | KEEP AS IS (the FAILs stated; "not a resolution") |
| 41 | Table 3: PASS 1a (S = 2.75 for 2.42 +- 0.20), 2b (0.9988), 9 (Malus exact at 45 and 90); 12 under the age word (1.907, 4.6 percent away) | READ | KEEP AS IS |
| 42 | Table 3: FAIL 1b, 2a (0.966 for 0.98), 3 (-0.108 for -0.53), 4b (0.2636 for 0.315), 7b (factor 6.4), 8a (factor 88), 8b, 8c (the massless input refuted) | READ; FAIL | KEEP AS IS (a FAIL stays in the paper's words) |
| 43 | Table 3: BOUND 5a (N_l >= 5.8e17), 7a (the deuteron's 0.109 percent); NOT COMPARED 2c | READ | KEEP AS IS |
| 44 | Row 2a's cause named, "the screen's fan's grain" (Table 3) | a diagnosis, not read | KEEP WITH THE STATUS WORD ("a diagnosis; the pin derived for the screen's fan, not this world's"); the physicist's open item |
| 45 | Table 2's four rows (Young's spacing, S(N), the clock's field, the equivalence) | READ | CUT the table: every row is in Table 4, Figure 1 or Table 3; the fingerprints to Appendix C |
| 46 | The covariant readings: a hypothesis beside the law; series S 369, 345 within two; z = 0.3674 for 0.369 (Table 4; the families table) | READ under a hypothesis | KEEP WITH THE STATUS WORD ("a hypothesis beside the law", as now) |
| 47 | The families table: every family's declared integers, object, verbs, click; "no detector reading registered" (u, q); "not named" | DECLARED (the register's inputs) + READ per family | KEEP AS IS (the owner's, record 822) |
| 48 | The 24 dated transitions (Appendix C) | history (HISTORY.md on main) | KEEP AS IS (the owner's) |
| 49 | The seven confirmations (Appendix C; Section 8's sentence) | READ | KEEP AS IS |
| 50 | The GameBoard as a system of information transfer; of the family of lattice gases, cellular automata machines, quantum cellular automata, Shannon's channel (Section 2) | definitions and positioning, with citations | KEEP AS IS |
| 51 | Why physics behaves like modern algebra, five steps; the fourth: the click families' transformations are the Lorentz group up to scale (intro) | the click theorem (cited) | KEEP WITH THE STATUS WORD ("the click theorem's, Section 9") |
| 52 | Positioning: the click is a non-local step forced by Bell's theorem because the marginals are exact and S > 2; the model psi-ontic; the uniform u does the work of quantum equilibrium | PROVED (Theorems 5, 6) for the first; classifications with citations for the rest | KEEP AS IS |
| 53 | The entropy identity of the click, H(u | K) = log_2 N per record ("What is proved"; the uncertainty paragraph) | an identity of the wheel (a definition) | KEEP WITH THE STATUS WORD ("an identity of the wheel"), one clause after row 17's cut |
| 54 | Bohr's ratio, the muon's lifetime in flight, the single opening, the far lamp's rows 11a to 11c, the two-way c after a detector, the inverse square at two radii | NOT MADE | KEEP AS IS (named as not made) |
| 55 | The platform: a formula enters the paper with both roads and nature on the comparison side (the platform paragraph) | the paper's rule | KEEP AS IS |
| 56 | The abstract: "against nature three readings pass, a fourth under the clock's assumed word, twelve fail and one is not compared, the failures the law's own" | READ (Table 3) | KEEP AS IS |
| 57 | The intro's "map of results" (proved, shown numerically, open) | a summary of rows 3 to 54 | CUT (duplicated by "What is proved" and Table 3; A.2 row 10) |

Rows: 57. Rows with the verdict CUT: 9, 17, 45, 57 (four); KEEP WITH
THE STATUS WORD: 2, 4, 8, 10, 15, 20, 21, 22, 23, 24, 26, 28, 29, 30,
32, 44, 46, 51, 53 (nineteen, of which every status word but rows 2,
4, 10, 15, 21, 22, 23, 24, 29, 30, 32, 51 and 53 is already in the
sentence); the rest KEEP AS IS.

### A.2 The cut table: 39 pages to 35 or fewer

What goes, in order, each with its page estimate (a page is about 45
lines of the body, 55 of the appendices); the sum at least four pages.
What stays and is condensed, never cut: the owner's ordered items (the
inputs table of 817, the families table of 822, the three chains of
843, the dark energy item of 849, the platform of 850), the click
theorem and the Bell plateau, the ledger of readings by kind (Table
3), the conversion table.

| # | What goes or is condensed | Why | Pages |
| --- | --- | --- | --- |
| 1 | Section 3's remark on dispersion (the GRB bound, the corpuscle) to one clause in Positioning | a postulate's consequence, not a reading (A.1 row 9) | 0.25 |
| 2 | Section 3's octahedron figure to one sentence; "The pace of the rows, and the octahedron" condensed | a sentence says it (the inscribed sphere) | 0.25 |
| 3 | Section 4's "The operations" and "The ground of these derivations" condensed to half | the ledger and Table 4 carry the ground | 0.3 |
| 4 | Section 4's Coulomb paragraph to three sentences with "no detector reading registered" | A.1 row 22 | 0.15 |
| 5 | Section 5's "Light: no optical metric" to a pointer at item (vii) | duplicated | 0.1 |
| 6 | Section 6's uncertainty paragraph to a three-line pointer | A.1 row 17 | 0.35 |
| 7 | Section 6's "What is derived and what is not" condensed to half; "The limit" merged into the Gleason paragraph | duplicated statements of the constants c_j | 0.2 |
| 8 | Section 7's "What Theorem 6 does not say" condensed to its two facts (above the bound at half the N; the tables' term fixed) | the rest is in the figure's caption and the checks file | 0.2 |
| 9 | Section 8: Table 2 cut; its fingerprints to Appendix C; "The formulas after a detector" and "The comparison with nature" condensed | A.1 row 45 | 0.5 |
| 10 | The intro's "The map of results" cut; "How the simulator led to the results" condensed | A.1 row 57 | 0.2 |
| 11 | The frame paragraph: the click frame's quotation cut to its theorem sentence with the citation; the detector's clock sentences kept | the quote's three sentences are the theorem, its proof sketch's words and the law's verdict, the last two said again in the step paragraph | 0.35 |
| 12 | The new-formulas paragraph: items (i), (iv), (v) folded into one line each; (ii), (iii), (vi), (vii), (viii) kept in full | duplicates and pointers | 0.3 |
| 13 | Section 2: "The road from the cells to the algebra" and "The families in the algebra" made one paragraph; "When the transition was made" to a pointer at Appendix C's 24 entries | duplicated with the families table and Appendix C | 0.35 |
| 14 | Appendix A: the proofs of Theorems 1 and 3 cited to DERIVATIONS_BEAM on main; Theorem 2's two lines kept | a derivation on main | 0.55 |
| 15 | Appendix B: the symbols table to the letters used in more than one section; the rounding paragraph kept | the single-section letters are named at their first use | 0.3 |
| 16 | Appendix C: the reproduction paragraphs condensed (the tag and the three trees in two sentences) | said in NUMBERS.md and the register | 0.1 |
| 17 | The abstract to about 1500 characters (the platform sentence and the prediction kept) | a paper's abstract | 0.2 |
| 18 | The discussion's "What is proved" kept as the list of theorems; "What the runs support" merged into it | duplicated by Table 3's caption | 0.1 |
| | Sum | | 4.7 |

Rows: 18, summing to about 4.7 pages, from 39 to about 34; the compile
decides and the count is reported. Nothing is added in step B; the
register and every file outside the paper's sources untouched.

## Step B applied (2026-09-22, the Boss's GO of 09:15Z on the owner's word of record 852): the cut, 36 pages

One commit through cut30/corrections.py and one line of cut30/assemble.py
(the page break before the references removed; the references follow
the body on its last page, as in most papers). Applied from A.2, in
order: the abstract to about 1900 characters; the intro's map of
results cut and the simulator paragraph condensed; the road and the
families one paragraph, the transition paragraph a pointer; the
dispersion remark and the octahedron figure cut (the octahedron said
in words); the ground paragraph condensed with the inverse square's
reading NOT MADE; Coulomb condensed with "no detector reading
registered"; light's paragraph a pointer with its FAIL; the
uncertainty paragraph a pointer with the identification named a
hypothesis and the entropy identity "an identity of the wheel"; "What
is derived" condensed with "The limit" folded in; Young's spacing
"rung 2, the fan"; "What Theorem 6 does not say" condensed; Table 2
cut, its fingerprints in "The formulas after a detector", its rows
pointed at Table 4 and Figure 1; "The comparison with nature"
condensed; every reference to Table 2 re-pointed (Appendix C, Table 3,
Table 4, Figure 1); the frame's quotation cut to the theorem's two
sentences; Einstein's relation "to second order under A1 and A2"; the
quantization "a theorem of A1, A3 and the conversion, not read as
such"; item (iv) folded into the equivalence's constant and the items
renumbered (i) to (vii), dark energy now (vii); "What the runs
support" merged into "What is proved" with nature's count; the proofs
of Theorems 1, 2 and 3 condensed; the symbols table to the letters
not named at their first use; the reproduction paragraphs condensed;
the six Ports paragraph without the duplicated octahedron; the
operations and the five steps' close condensed; Appendix B's
directions sentence out; Appendix D's captions shorter and the two
inline families one row; the AI statement shorter. Also folded, from
A.1: Poisson's interior read after a detector (series X) in place of
the stale "no detector reading of the two fields is registered"; the
fourth of the five steps names the click theorem. Nothing added;
no number moved; every FAIL kept; the register untouched. The count:
36 pages.

## The owner's referee read of the 39-page version (2026-09-22): six points, what was verified and changed

The owner read the paper as a referee and sent six points with "check
what is relevant and correct; change only what you verify." Verified
and changed, one commit: (1) the Born-to-1/N statement holds for the
exact tables; with the declared tables the weights vary with the birth
phase within the rounding, and the owner's worked pair (two equal
offers at u and u + 1824, N = 8192) reproduces exactly, 4104 / 4088 for
4096 each, 8 / N: the interference paragraph and "What is proved" now
say so, the theorem untouched. (2) Theorem 5 covers the outcomes'
counts; the pair's gather at the completion interval (P6) makes the
near outcome's readable time depend on the far arm's length: the paper
now says no-signalling in the times is not claimed and that the
availability of a local outcome before the completion is a definition
it does not give. (3) Einstein's relation "follows from the Inside step
under (A1) and (A2), to second order, an extension the law as built
does not meet"; the abstract's Lorentz clause says "under an amplitude
split the law as built lacks". (4) The prediction's parameters named
(N_t = 256, the grains 512 to 8192, why nature's grain would lie there
not said) and the five-sigma separation 6e-5 added to the refutation
sentence; the paper had no five-sigma criterion of its own, so the
owner's premise there was not the paper's, and the number is stated as
arithmetic. (5) The orbit's mean equals the ring mean only under a
uniform dwell, "a sampling the paper does not prove" (no source on
main names a proof). (6) Table 3's criterion per row stated in its
caption; row 2b's PASS as a bound met with the clicks' 1.000 (the
register's DETECTOR number; the offers' 0.9988 was the apparatus
layer's diagnostic, wrongly the paper's number) and row 12's PASS as
the lattice-exact form (the dwelling ages 5, 6 and 10, 11 pinning
1.909). Not changed, and why: the presentation remarks (shorten the
history and the Inside/Outside repetitions) touch the owner's ordered
items and are not a verification; the referee's wish for a full
operational definition of the click beyond P6 is a design question for
the tree, not a sentence the writer can verify. The count: 36 pages.

## Applied (2026-09-22, the Boss's order of 10:15Z on the owner's decision of record 865): the crowd worlds' status word; the cuts (a) and (c)

Under the generic entry of the bending the crowd worlds at a pair with
n > 0 are opaque to light (records 861, 865); the physicist's list of
the paper's readings in them (record 866): series T (the ratio 1.907,
the clock's word), G and G2 (the diagram's shape, q = -0.108, z =
0.2636) and X (Poisson's interior); the crowd's clock, the cluster and
the reader inside a crowd are NUMBERS.md rows only, not the paper's.
Every sentence carrying one of those readings now says, in the same
sentence, "read under the law before the generic entry of 2026-09-22,
not readable under the law as it stands" (nineteen places: Section 5's
series T and Poisson sentences and its opening, Table 3's rows 3, 4b
and 12 with their verdicts "of the law before the entry", the chains
paragraph, Table 4's three rows, item (v), the dark energy item with
the deceleration parameter's verdict, the platform's simulator road,
the ground paragraph, the families table's two rows, the abstract's
fourth reading); the readings and their kinds unchanged; D3's fall
worlds and the optical worlds untouched (suspension 0). The cuts (a)
(Appendix B's Mach-Zehnder-total sentence) and (c) (the roads table's
W row, "the click frame, section 7") applied; not (b). The count:
37 pages; the status words cost about fifteen lines, more than the
two cuts saved; the count is reported and the paper holds still.

## Applied (2026-09-22, the Boss's correction of 10:40Z, record 868): the status word on series T only

The physicist's relevance check against main.tex: of the crowd worlds
at n > 0 the paper cites only series T (clock_word's four worlds);
NATURE rows 3 and 4b rest on coasting_none, the S row on the muon at
rest and the coasting star, K and D3 on suspension 0, X's shell worlds
not in the list. So the status word of the previous commit is removed
from G, G2 and X's places (rows 3 and 4b and their verdicts, Table 4's
light row, the dark energy item, the platform's stars, the ground
paragraph, Section 5's Poisson sentence) and kept on series T's, with
the owner's decision (a) in it: "read under the law before the generic
entry of 2026-09-22; not readable under the law as it stands; the four
worlds are being redeclared in the weak field (the pair [1, 16384], the
crowd's age moment at most 1024 per Node on the light's path) and
re-read, the new numbers to replace these" in Section 5's series T
sentence and Table 3's row 12, a short form ("read before the generic
entry of 2026-09-22, not readable under the law as it stands, being
re-read in the weak field") where 1.907 is quoted elsewhere (Section
5's opening, the chains paragraph, Table 4's two rows, item (v), the
platform, the families table). The cuts (a) and (c) stand. The count:
36 pages.

## Applied (2026-09-22, the Boss's delta of 09:10Z, record 873): the cuts (i) and (iii); NUMBERS.md's series T rows marked

The delta's part (1) and (2) were already at aec5c32f (the status word
on series T only, with the weak-field words). Now: (i) the short form
"(before the entry of 2026-09-22)" in Table 4's two rows and the
families table's two rows, the full words kept in Section 5 and Table
3's row 12, the medium form in the prose; (iii) the 24 transitions
with the date once per group; not (ii). NUMBERS.md's rows 147, 157 and
169 (series T) carry the status word. The count: 36 pages.

## Applied (2026-09-22, the owner's two words on his referee points 2 and 4)

(2) "The click does not signal; everything is local; verify and put
definitions accordingly." Verified against the engine
(amplitude.py, LiveRecord and Layer.complete: a record is gathered once
when its live count reaches 0; the rows' content is placed at their
arrival; the flight is blind, P9) and against Theorem 5's proof (the
coarse rung of the first-declared party sits at N/2 for every setting,
so its outcome is a function of u alone). The definition of the click
now names the click's two parts, the arrival (local, at the arm's own
interval, independent of the other arm's setting and length) and the
outcome (the first party's fixed at its arrival by u, the second's at
the completion by the joint weights), with the near outcome's writing
at the far tick a bookkeeping of the host; the sentence after Theorem 5
now states no-signalling in the times as well as in the counts, with
the one non-local step named as the assignment of the second outcome
on the labels, not on the times; Positioning says the same. The
earlier sentence ("no-signalling in the times is not claimed") is
replaced, since the claim is now verified and stated. (4) "The paper
can check algebraically": the prediction paragraph now says the
dependence on the grain and the tables is algebraic, the family of
exact rationals (181/64 from 512 to 8192, 5793/2048 to the tables'
bound), and that a measurement below 2.828125 or above 2.828613 by five
standard deviations refutes every grain from 512 up at once. The count:
37 pages.

## The owner's referee points 5 and 6, handed to the Boss (2026-09-22, the owner's word to the writer: "5 to the Boss for handling; 6 ask that what is needed be re-run; handle everything")

Point 5, the orbit's mean and the ring mean: the paper says (Section
4, the ground paragraph) that the mean push over one closed turn of an
orbit equals the ring mean "only where the body's dwell is uniform in
angle, a sampling the paper does not prove". Handed to the Boss for a
mathematician: prove the equality under the body's dwell weighting, or
give the error bound in terms of the orbit's eccentricity and the
lattice's grain, with series D3's loops (not similar figures, one
recurrence per radius, T(24)/T(12) = 1.997) as the registered case;
the paper takes the theorem or the bound on the Boss's SHA, the
sentence then "proved" or "bounded by ...".

Point 6, Table 3's criteria: the paper's caption states the criterion
per row and rows 2b and 12 carry theirs; the owner asks that every row
get, from the register's side, what exactly is measured (the click
line), whether the number is an ideal prediction or one for a given
instrument, and the rejection criterion, and that whatever the criteria
need be re-run. Handed to the Boss with the list of what the paper
names as pending or not made: row 2a's two-slit visibility with the pin
derived for this world's fan (the physicist's open item, the screen's
fan's grain); row 4b's re-run at head (pending); row 3's -0.104 at head
against the paper's -0.108 (record 408), which is the register's
number; row 12 in the weak field (ordered, record 865); rows 11a to 11c
(the far lamp) not run; rows 8a and 8b (J1, J2) if the criterion needs
more than 64 clicks; the two-way c after a detector, the inverse
square's decisive reading (form B), the moving detector's one-way ratio
and the velocity's quantum, all NOT MADE. The paper takes each new
number by kind on the Boss's SHA, one commit per batch; a PASS or FAIL
that changes under a stated criterion changes in the paper's words.

## Applied (2026-09-22, the Boss's word of 09:35Z under record 852): the two condensations for the last page

From the two places the Boss named and no other: (1) the platform's
simulator road, the series named once each (L, Q, X, T; G, G2, S; D3),
T's four worlds' status kept, no sentence of claim removed; (2) the
frame paragraph's detector-clock sentences condensed to their claim,
the click theorem's sentence and the owner's framing sentence kept word
for word. No reading, kind, number, verdict, citation or claim removed;
the seven confirmations and the GHZ clause as they are. The count:
37 pages (the owner's words on his points 2 and 4 had added the
click's two parts and the algebraic family at f7ac7856, one page's
last lines, before this); stopped here as ordered.

## Applied (2026-09-22, the owner's word to the writer): the one chain from the board to Einstein's step through Lorentz

The owner (in English, by voice): make sure the step that connects the
GameBoard to Einstein's equation is there, through Lorentz, both shown
as the step above, Einstein being the step on the outside of the board.
Verified against Einstein Outside section 3 (a) on main (e8432e6c) and
written into "The step beneath and the step above" as one chain: the
Inside step (Eq. 1 with W its invariant), the conversion (A1, A2), the
symmetry of the conversion (the Lorentz group up to scale, the click
theorem), its image the Outside step, whose most general form is
Einstein's step as physics writes it (dp/dt = F with p = gamma m v,
E^2 = E_0^2 + c^2 p^2, d tau/dt = sqrt(1 - v^2), the geodesic's first
terms); Lorentz the symmetry of that one step and Einstein's equations
its form, both one step above and neither put in; the r-free lines
Einstein's exactly from A1, A3 and the conversion, the scaled lines
Einstein's iff r^2 = 1 - v^2, which A2 gives to order m^2 v^2 and the
law as built (r = 1) does not. The count: 37 pages.

## Applied (2026-09-22, the owner's "go for it", record 886): the four content cuts, in the order of least loss

The cut table's four new rows: (i) the five steps of "Why physics
behaves like modern algebra" to three, the claims merged (the couplings
into the second step, the identity of every result into the third), no
claim dropped; (ii) Table 5, the distance, folded into "What is proved"
as one sentence with every needed item and its deciding check, the
numbers and kinds kept (G not read, form B not built, 1 - v^2 against 1,
1.75 arcseconds, 22.5 degrees, row 10, 10^-4, 181/64 against 2 sqrt 2);
(iii) the 24 transitions to Appendix C's lines with the citation
(HISTORY.md on main at 412f5c61) and the dates once, one clause per
date; (iv) the roads table's nine rows to six: the place-to-place
factor's row out (a lemma of the boost and the rate rows, Theorem 1 of
Einstein Outside cited there), the composition's row out (named in the
roads paragraph as r-free, II.3), the quantum's row out (Theorem 3 cited
in "The smallest thing above"); the six kept: W to second order, the
boost, 1/gamma, E^2 = E_0^2 + c^2 p^2, the Outside step with Einstein's
step, Newton's step as the limit. No reading, kind, number, verdict or
citation removed; the seven confirmations and the GHZ clause as they
are; the framing sentence and the click theorem's sentences word for
word. The count: 36 pages.

## The last page's candidates, named and not cut (2026-09-22, the Boss's word of 11:20Z under record 852; the owner decides)

From 36 pages (the last page full) to 35 needs about fifty lines. The
three candidates, in the order of least loss, each with what it loses;
together they reach 35, none is cut until the owner's word:

| # | The candidate | What it loses | Lines |
| --- | --- | --- | --- |
| A | The discussion's "The road to each, and the check that nothing was derived from them" condensed to eight lines pointing at the one chain (now in "The step beneath and the step above") and at Table 8 | the prose of the three roads (Lorentz, Einstein, the Outside step) told a second time; no claim, no number, no citation (Table 8 keeps the check, the chain keeps the roads) | about 10 |
| B | The duplicated sentences: the frame paragraph's close (the two one-way Doppler factors and 1 - v^2, now in the chain sentence); Section 6's "Interference, by the formulas alone" without the Mach-Zehnder and one-slit sentences the light chain of Section 9 repeats (the formula R(x), the spacing and the readings stay); Section 3's "The pace of the rows, and the octahedron" to three lines (the six Ports paragraph and the Proposition say it) | no claim, no reading, no number: each statement stays in its other place | about 18 |
| C | The families table's "when it entered" and "the verbs" columns merged into one, its object cells shortened; the abstract from twenty lines to fourteen (the platform sentence and the prediction kept) | the families table's readability (one column fewer), six lines of the abstract's list of exact results (the list stays in "What is proved") | about 21 |

The writer's recommendation: all three. The owner was shown the same
list in six items (the three above split); the simulator and the code
stay named in the introduction, the platform, Section 8 and Appendix
C; Table 7 stays. Also noted from the Boss (record 891): NUMBERS.md's
rows 130 to 134 (the crowd's clock, the cluster, the reader in a crowd)
cite worlds main.tex no longer carries; on the Register Architect's
merge SHA they are marked "world removed from the register, record
871, SHA ..." and not deleted; shell_clock's six worlds (series X) stay
in the register, cited by the paper.

## Applied (2026-09-22, the owner's word to the writer, after the hold of record 895): the groups and rings of the six verbs in the symbols table

The owner asked whether the paper names the operations of the group,
the groups' symbols and how everything is computed. The body does: the
six verbs named in Section 2 and written as algebra in Section 2's
"Written as algebra" sentence (the carry a bijection, the flight the
translation group's shift, the split's table with its conjugate
transpose, the rotation an integer matrix, the merge the addition in
Z[Z_Nphi] with its cancel the quotient by x^{Nphi/2} + 1, the click one
bilinear form); the map of Eq. (map) with the 5-against-2 example and
the hand-worked update (238, 146, 274, ...; Links at 1, 3, 5, 7, 8;
128/220 = 0.5818); the 48 and its 24 rotations in Theorem 1 and its
proof (Appendix A). The one gap was Appendix B's symbols table, which
carried physics' letters, the grains and the map but no group symbol.
On the owner's word one row was added to Table B (the symbols):
Z_Nphi, Z[Z_Nphi], Z[zeta_Nphi], Z^2 (x) Z^2 and B_3, each with its
kind and its name, pointing at Theorem 1 and Section 2. No number
moved; 48 and 24 are Theorem 1's. 36 pages; the PDF rebuilt. The hold
of record 895 on the last page's candidates A, B and C stands.

## Applied (2026-09-22, the Boss's order of 10:03Z, record 883 closed): the ring mean sentence on PR #840's merge SHA ab96e7e8

Section 4's ground paragraph: the clause "which equals the ring mean
only where the body's dwell is uniform in angle, a sampling the paper
does not prove" was not the true statement and goes. In its place the
Ring Mean Mathematician's sentence in its two forms from
docs/designs/ring_mean/PROOF.md section 6 (on main at ab96e7e8):
"proved" for the continuum claim (the orbit's mean over one closed turn
equals the ring mean at r_* = <r^2>_theta / <r>_theta on the plane and
sqrt(<r^2>_theta) in space, by the area rule of a radial push, Kepler's
second law the comparison; against the angle-mean radius the factor
r_bar^2 / <r^2>_theta between 1 - e^2 and 1; on the lattice up to four
grain terms, three numbers and one Node's dwell per crossing, GAMEBOARD
by formula) and "bounded by" beside D3's reading (the turn's e not on
record, bounded by 0.96 and 0.70, the floors 0.07 and 0.51, deciding
nothing; the ratio T(24)/T(12) resting on the 1/r push's scale symmetry,
not on the equality). The reference `ringmean` added. NUMBERS.md rows
for every number, by kind.

The page: the sentence pushed the roads table's last three rows onto a
37th page. Trimmed within the same paragraph only, as ordered ("in one
of three forms", the factor clause, the grain terms and the D3 clause
compacted; every number kept): the paragraph fell from 24 to 21 lines,
the spill needs about six more, and the paragraph cannot give them
without dropping the numbers the order named. Delivered at 37 pages with
the sentence whole; the choice is the Boss's or the owner's: (i) 37
pages; (ii) the grain terms' numbers moved to the citation (about two
lines, not enough alone); (iii) the owner's "cut" on the last page's
candidates A, B, C (record 895). No cut made.

## Applied (2026-09-22, the owner's word "fix or sharpen them"): the second referee read, points 1 to 6, in the paper's words

The owner brought a second referee read of the 36-page paper (seven
points); each was checked against the text, the world files and a
computation, reported to him, and on his word the verified ones were
folded:

1. The intro's "every result of the paper is therefore an identity of
   that algebra" narrowed to the results the paper calls exact, under
   the declared tables, matrices and family table, named as inputs
   (Table 1).
2. The Bell section states what Theorem 5 does not cover: the
   registered wheel [1, 64] runs one birth per u in order, so the first
   party's outcome sequence is a square wave with serial correlation
   1 - 4/N_phi (0.9990 at 4096), a prediction in time no run reads and no
   row compares; and the marginal holds for settings independent of the
   wheel (a = 0 for u < N_phi/2, a = N_phi/2 after gives the second party
   + at all 64 births at 64), the settings' independence an assumption
   of the frame, added as the fourth assumption of the prediction
   paragraph. A run of the outcome sequence is the Criteria Runner's if
   the owner wants it.
3. "Exclude every mixture" narrowed to the mixtures the readings
   resolve, the weight bound not computed; the norm range of Appendix B
   said to bound one phasor and not a near-cancelling sum, with the
   example 256 x^8 - 181 (1 + x^16) at 64: (0, 0) under the tables,
   (0, 14) after a common turn of eight steps, the exact 0.0007. The
   error theorem for the tables is the Ring Mean Mathematician's if the
   Boss assigns it.
4. Section 3's Lorentz sentence carries the (A2) caveat the abstract
   and Section 9 carry.
5. "Why nature's grain would lie there" adds the table scale N_t = 256.
6. Table 3 row 2a: the register's source (Grangier, Roger and Aspect
   1986) named as a Mach-Zehnder reading, a two-slit source not yet
   registered (the register's own note "to verify against the source");
   the verdict and the number unchanged, the criteria the Criteria
   Runner's. The clock row's count (a fourth PASS under the caveat, or
   historical only) is with the Criteria Runner's re-read of series T.
7. The development history in the body: not changed, the owner's own
   items (the 24 transitions, the families table's "when it entered").

Figure 1's legend was moved clear of the inset at 21b4ac0a. Numbers by
kind in NUMBERS.md. 37 pages (the ring mean sentence of 0c6a4f2d had
reached 37; the page is with the Boss).

## Applied (2026-09-22, the owner's "cut", record 922, relayed by the Boss at 10:42Z): the last page's candidates A, B and C together

A: the discussion's "The road to each, and the check that nothing was
derived from them" condensed to the three roads in one sentence each,
pointing at the one chain above and at Table 8; the no-input sentence,
the words ("follows", "recovered", "shown to second order",
"declared"; "derived" nowhere) and the Table 8 pointer kept. B: the
frame paragraph's close to the measurable once (the two one-way Doppler
factors apart by 1 - v^2); the interference paragraph's what-passes,
one-slit and Mach-Zehnder sentences to one clause (the one-slit claim
"no dark pixel" and the Mach-Zehnder reading 64/0 kept, row 2b and
Appendix C carry the rest); Section 3's pace paragraph to its two
rules, the causal front and the Proposition. C: the families table's
"when it entered" and "the verbs" columns merged into "when it entered;
the verbs" (widths 0.7, 1.3, 1.3, 1.1, 1.45 in), three object cells
shortened (light, the apparatus materials, mu/matter); the abstract's
list of results shortened to one sentence, its "every result is an
identity" narrowed to the results the paper calls exact under the
declared tables, as the intro was (the second referee read, point 1).
No claim, number, verdict or citation removed.

The count: 37 pages, not 36. Before the cuts page 37 carried 33 lines
of the roads table; after them 25 (five rows). The body's savings
(about 25 lines in Sections 3, 6 and 9 and the abstract) moved the
page breaks before the references and Table 3 and were absorbed: the
body ends on page 30 at 600 of 650 points before and after (the log's
pagetotal at the bibliography's start), the references still begin on
page 31. The appendix side gained the families table's 8 lines only.
What would give the remaining 25 lines without loss is not on the
owner's list; the Boss decides.

## Applied (2026-09-22, the Boss's order of 11:05Z under the owner's "cut", record 922): the lossless appendix-side candidates D, E, F

D: the families table to 0.7, 1.35, 1.35, 1.15, 1.5 in and the roads
table to 1.5, 1.75, 1.5, 1.4 in (the text width less the column
separations). E: Appendix C's "seven confirmations" in one sentence
pointing at Tables 3 and 7, every number kept (the far pair's cells
27, 5, 5, 27, the half-turn 0/64, GHZ's 16 each, Malus's 0 of 256
crossed and series K's 0.000 pixel and 0.00 interval stand nowhere
else). F: the symbols caption shortened; the grains, directions and
groups rows tightened; the notation table's third column 3.3 to 3.25
in, which ends its 3.5 pt overfull. G untouched. No claim, number,
verdict or citation removed.

The count: 37 pages, unchanged; the roads table's last five rows (25
lines) still on page 37. The appendix-side savings of D, E, F are a
few lines on pages 34 and 35, below one row of the families table
(its rows 4 to 8 lines tall and unbreakable), so no row moved and page
36 is as it was. Next lossless candidates, measured in a trial build
and not applied: (H) the references at footnotesize instead of small;
(I) the notation table at scriptsize. The owner decides.

## Applied (2026-09-22, the Boss's order of 11:30Z under the owner's "cut", record 922): H, the references at footnotesize

One line of cut30/assemble.py: the bibliography's wrapper "{\small"
to "{\footnotesize". No word, claim, number, verdict or citation of
the paper changed. The count: 36 pages, measured in the real build
(the references end on page 33, Appendix A follows them there, the
roads table closes on page 36). I (the notation table at scriptsize)
not applied. If the owner wants H undone, one revert commit.

## Applied (2026-09-22, the owner's word "go on all of it"): the third referee read, six points, in the paper's words

1. The drive on three axes and P5: Section 2's P9 sentence states the
   engine's rule (each axis's count advances every interval, the first
   axis whose count fires steps, a later axis's coincident fire is lost,
   its wall subtracted, x before y before z), so a body crosses one Link
   per interval and the per-axis fraction is its pace only where the
   fires do not coincide; three equal momenta N_l N_w M give 1/2 per
   axis, 3/2 in all, and the built body moves on x alone at 1/2, the sum
   of the paces at most 1; form B not built. The ledger's row and the
   conversion table's cell say the same. Whether the lost step is the
   law's intent is the physicist's (record 342).
2. No-signalling of the counts: Theorem 5 renamed "Exact marginals;
   no-signalling of the counts"; the Bell section states the channel in
   the order of the outcomes (B = A at a = b, B = -A at a = b + N/2;
   15/16 against -5/16 over 192 births at 64, the marginal 96/96, at
   every shift), a computation, a FAIL of any claim beyond the counts,
   open until the wheel is other than a counter (P4 forbids a draw) or
   the claim is kept to the counts; the ledger's row and the discussion's
   positioning sentence say the same. The law's fix is the owner's and
   the physicist's, not the paper's.
3. The exact evaluation and the tables' are two maps with different
   zeros, the cancel's zero (an equal pair at N/2) a zero of both; said
   once in Section 2's "Written as algebra" sentence.
4. Definition 1: the scaling (w, m) -> (kw, k^2 m) an identification at
   the read-out and not a relation of the module (the quotient would not
   be free); the multiplicity's bound named, the engine's 2^63 - 1, a run
   passing it refused.
5. Gauss's law: the crossing claim to net signed crossings (a non-convex
   surface left, re-entered, left again; the sum one).
6. The sign: a body's acceleration is +(N_l c / tau_L) grad A, toward the
   source, from the flow a = -(N_l c / tau_L) grad A and the gravity
   column -M_A a; the sentence's "minus the gradient" was wrong.

No number, verdict or citation removed; every new number by kind in
NUMBERS.md. The count: 37 pages (the body grew by about twenty lines,
the references moved with it, the roads table's last five rows on page
37); the page is the Boss's.

## Applied (2026-09-22, the owner's decisions of record 941, the Boss's order of 11:27Z): Table 3 row 8a kept as history

(1) Row 8a (J1, the FAIL by a factor 88): one sentence beside the
number and the verdict, both unchanged: the registered J1 run predates
the one flight wall, under which the weak register's become blocks move
(the physicist's derivation, records 931 to 933), so the row is a
reading of the law before it, kept as history, J1's redeclaration in
the weak field after the paper. (2) The referee's point 7: the history
stays in the body; nothing needed. (3) Row 12 (series T) reads "read
under the law before the generic entry of 2026-09-22; not readable
under the law as it stands; ... PASS, of the law before the entry,
under the age word ...; FAIL under the presence word": historical in
those words, unchanged. (4) The merge waits for the three SHAs. (5) The
third referee read's six points were folded at b3e12fae on the owner's
word to the writer, "go on all of it and come back to me when it is
resolved to give the referee a PDF", given after the writer's report
of the six points; the Boss's order of 11:27Z, written before that
commit's report, holds them not yet authorized: the crossing is
reported, nothing reverted without a word.

## Applied (2026-09-22, the owner's words): the title; Inside a beam, Outside a wave; the page stays at 37

The title, the owner's: "Universe24: Physical Relations from a Common
Discrete Update Rule" (the writer's variant, "Physical Laws Recovered
from a Single Discrete Update Rule", offered and not taken; one line
if the owner wants it). The small explanation the owner asked for,
placed after the frame paragraph's opening in the discussion: a thing
propagates Inside as a beam, rows on digital lines at one Link per
interval, and shows Outside as a wave, the click's weight being the
squared sum of the rows' amplitudes, which adds and cancels as
amplitudes do (Young's bands, the Mach-Zehnder's ports), the wave the
read-out of the beam and not a second thing on the board. Written from
the paper's own statements (the abstract's "as a beam", Definition 3's
click, Section 6's interference by the formulas alone); its wording
sent to the Boss for the chief physicist's confirmation, to be
adjusted on his word. The page: the owner's word "leave it as it is,
no need to cut": 37 pages stand.

## Applied (2026-09-22, the owner's word "put them in unequivocally, in the body of the paper"): the five items of the comparison with other papers

1. The run line in Appendix C: the install and the run command of the
   README, the world files of the pair, the two slits and the
   Mach-Zehnder, and the runs' fingerprints named once there.
2. "The words of this paper" after the introduction's first paragraph:
   GameBoard, Inside and Outside, row and record, the click, a rung,
   the kinds DETECTOR and GAMEBOARD, each in one sentence from its
   definition.
3. The longest sentences of the introduction and the discussion split
   (the first paragraph, "Second", "Third", "So the paper keeps one
   ledger", "What no rule of the law forces", the platform's simulator
   sentence, "The same way", "So 1 + z"); the same words, full stops
   for semicolons; the click theorem's quotation, the chain sentence
   and the frame's opening untouched.
4. The project's references as citation notes: "record N \cite{log}"
   to "\cite[record N]{log}" throughout the body; the roles ("the
   model owner's finding", "the owner's word", "the physicist's
   derivation", "the physics-rule reviewer", "the physicist's pins")
   out of the body, the citations kept; the commit b34fe114 and the
   runs' fingerprints as citation notes and in Appendix C.
5. Four figures in the body: Figure 1, the mechanism (a new drawing
   from the definitions, figures.py figure_mechanism, no run: the
   board, an emitter, two rows on their digital lines, a detector's
   Nodes; the click as the ladder of rungs over u); Figure 2, the
   two-slit weights and clicks beside the Mach-Zehnder worlds' clicks
   (the figures' runs, series L, both kinds named); Figure 3, the
   pair's E(a, b) computed from the rule against the tables' cosine
   with the registered worlds; Figure 4, S(N) as before.

No claim, number, verdict or citation removed. 39 pages (the owner's
word on the page: leave it).

## Applied (2026-09-22, the owner's word: the tables correct, telling, and good to look at)

Checked: Table 2's caption counts against its rows (three PASS, 1a, 2b,
9, and 12 under the caveat; seven FAIL in a run, 1b, 2a, 3, 4b, 7b, 8a,
8b, plus 8c the refuted input and four pins not in the table; BOUND 5a,
7a; NOT COMPARED 2c), every row cited in the text either in the table
or named by the caption as a pin outside it (4a, 6, 10, 11a); the
ledger's rows against their sections; the conversion table's readings
each with a kind. Changed, formatting only: every longtable column set
ragged right (a column type L in the preamble), which ends the
stretched word spacing of justified narrow cells; the families table's
first column widened to 0.95 in so the family names no longer break
letter by letter. No word changed. 39 pages.

## Applied (2026-09-22, the Boss's order of 11:51Z): Table 3 on the criteria file at the merge SHA f5fe8004 (PR #851)

Every row's reading carries its kind (DETECTOR, GAMEBOARD, COMPUTATION)
as the file states it; the re-runs at head stand beside the registered
numbers, none in their place (row 3 -0.104, row 4b 0.2647, rows 7a and
7b every pin met, row 8a's width 0.08 to 0.13 at the cap in the
lattice's clock, GAMEBOARD, row 8b the pin met bit for bit); row 2a
carries the pin derived for this world's fan (0.9659, COMPUTATION, met
bit for bit) and the two-slit source (Jacques 2005, a biprism's central
fringe, 0.94 as reported, to verify, NOT COMPARED until then, bound
against bound), the 0.954 of the weights named as history; row 3's
criterion in the file's words (0.42 away, the coasting ideal q = 0, no
term carrying q toward -0.5); row 12 unchanged, the caption calling the
fourth PASS historical; item (a): the register's settings declared per
world or balanced over every u, the freedom-of-choice loophole's
counterpart in the wheel, the reading that would test it; the criteria
file cited in Appendix C and the caption at its merge SHA; two
references added (criteria, jacques2005). No number, verdict or
citation invented. 39 pages.

## Applied (2026-09-22, the chief physicist's verdict, the Boss's order of 11:54Z): the beam-and-wave sentence in his words

RIGHT WITH ONE CHANGE: the law as built forms no amplitude per row and
squares nothing as a step of its own (records 173 and 188; amplitude.py's
gram_form, f^T G f with the declared Gram matrix); Definition 3's X and
Y are the paper's writing of that integer. So "the squared sum of the
rows' amplitudes" became "the quadratic form of the rows' phase counts
(Definition 3's X^2 + Y^2, the same integer as the square of a phased
sum)" and "as amplitudes do" became "as a phased sum at the roots of
unity does" ((A2) not built). His caution, no change: "shows Outside as
a wave" is right for the count over many clicks; one click is one Node.

## Applied (2026-09-22, the owner's three corrections of record 951 and the form B sentence; the Boss's orders of 12:01Z and 12:08Z)

1. The pace clause, "per axis where the axes' fires do not coincide;
   one Link per interval in all", added where a body's speed appeared
   without it: the conversion list of Section 2 ("whose speed
   p / (N_l N_w M + p) saturates ...") and the Newton paragraph ("the
   speed the push builds saturates ..."); the notation table's drive
   row names no pace, unchanged. No number changed.
2. The click's zero: "the GameBoard's cancel and the click's zero are
   one relation, exactly" became "the GameBoard's cancel and the ideal
   click's zero, the evaluation on Z[zeta_Nphi], are one relation,
   exactly", the odd-factor parenthesis kept, and one sentence added:
   the table click is a different map, an ideal zero a table zero (the
   merge cancels before the tables), and whether the tables add zeros of
   their own, beyond the one instance Section 6 shows, and in what
   measure, is a computation (the Gleason bound's note), not a relation
   of the module. The one instance is the paper's own computation of
   the third referee read's point 3 (256 x^8 - 181 (1 + x^16) at 64
   reading (0, 0) under the tables), kept as a shown case, the measure
   left to BOUND.md.
3. The multiplicity's bound: "bounded with every integer of the run by
   the engine's 2^63 - 1" became the law's bound 2^62 - 1 of an amount,
   a multiplicity and a momentum component (events/world.py) inside the
   host's working bound 2^63 - 1 (core/integer.py), a run passing either
   refused; the ledger and the notation table name no bound, unchanged;
   NUMBERS.md one row by kind.
4. Form B: beside Section 2's drive rule, the physicist's sentence (form
   B exists as a declared identity off by default, the world key drive_b,
   series Y, no coincident fire lost, read inside its pins on six
   registered worlds; the default on the model owner's word; until then
   a diagonal body is the per-axis walk); the discussion's "form B, not
   built" to "built off by default, series Y". Record 938's "not built"
   was wrong (PR #813 at e0761893).

## Applied (2026-09-22, the owner's word "be critical and fix what is needed"): the fourth referee read, points 1 to 9; point 10 not

1. The body's acceleration in the age moment's field: the sentence of
   the third read's sign fix carried the flow's coefficient; the body's
   acceleration is the push over N_l N_w M_A (the drive's conversion,
   as Eq. coulomb's a_e), so +(c / (N_w tau_L)) grad A, verified
   against Section 4's push and a_e. Corrected.
2. Theorem 5 renamed "Exact count marginals"; after the channel, the
   plain statement that the law as built with its sequential wheel does
   not meet operational no-signalling, its counts blind to the other
   setting and its order not, the pair's construction a model of a Bell
   experiment in its counts only; the ledger's row the same.
3. "The one prediction" became "The finite-grain value, and what would
   make it a prediction": a prediction of the law once the wheel meets
   no-signalling in the order of the outcomes, until then the exact
   consequence of the declared construction at its grain; the abstract
   the same.
4. Tsirelson's value 2 sqrt 2 named a limit and not a bound of the
   construction at finite grain (S on both sides of it), in the abstract;
   the Bell section already said so.
5. The conditional extension named at the head of the frame paragraph:
   the click frame under (A1) and (A2), where (A2) enters not a
   consequence of the law as built, the r-free lines from (A1), (A3) and
   the conversion alone; the owner's framing sentence and the chain
   sentence untouched.
6. Beside Eq. (square): a declared identity of the record's
   representation in the law as built, not derived from the rows'
   dynamics; under (A2) shown to second order.
7. The depth of successive rotations against the bound: in the row form
   a rotation multiplies m by 65536, four would pass 2^62 - 1; the
   engine keeps the label set and applies the tables once at the click
   (amplitude.py, rotate; the cells' weight reduced by its gcd), so the
   depth is not limited; where the bound binds, a limit of the
   implementation's domain, never a prediction.
8. "The lattice Gleason" renamed "The quadratic read-out on the phase
   lattice, a Gleason-like characterization", the paragraph and the
   discussion's list with it.
9. The abstract carries the limitation: the law as built meets (A1) and
   not (A2), recovers no relativistic dynamics, and its sequential wheel
   signals in the order of the pair's outcomes though not in their
   counts. The abstract's structure is the owner's and stays.
10. The length (25 to 30 pages, the history and the tables to a
    supplement): not applied; the owner's items and his word on the
    page.

No number, verdict or citation removed; 40 pages.

## Applied (2026-09-22, the Boss's order of 12:27Z, record 958): the register's consolidation cited pending merge; the paper does not wait for the Gleason bound

PR #860's head b12dd253 (register-paper-sources) cited in Appendix C
and in the register's reference as pending merge, the merge commit to
replace it; verified on that head: every world the paper cites stands
(amplitude, bell, c_measured, hubble_stars, binding, weak, clock_word,
orbit_lamp, shell_clock, covariant), and the worlds it removes are
cited by no row. NUMBERS.md rows 130 to 134 marked: 130, 133, 134 the
crowd's clock, the cluster and the reader, cited by the paper no longer
(record 871), their directories standing on b12dd253; 131 series Q's
fan world, cited, standing; 132 the collision's tie, the gallery worlds
removed on b12dd253, the row history. The Gleason bound's number: not
waited for; the sentence stands (the instance shown, the measure a
computation), one line takes the number if BOUND.md lands. The atom is
out of the paper. The one thing waited for: the order channel's NATURE
row (the Order Channel Runner, the pins 15/16 and -5/16 against
nature's 0), into Table 2 on its merge SHA.

## Applied (2026-09-22, the owner's question "why did you take the octahedron out of the PDF?")

The figure had been cut at 8f7408eb (Step B, the cut to 35 pages under
record 852, A.2 row 2), with its words kept in Section 3. Returned as
Figure 2 in Section 3 with its caption as it was (drawn by
octahedron.py from the definitions, no run), the paragraph pointing at
it. 41 pages.

## Applied (2026-09-22, the owner's word): the GameBoard in space, a new Figure 1; the folds verified; the figures checked

The owner asked for a picture of the Nodes in space, six by six, how
they are arranged: Figure 1, a 6 x 6 x 6 cubic array of Nodes joined
by Links through the six Ports, one Node and its six neighbours marked
(figures.py, figure_lattice, from the definitions, no run), placed
after "The words of this paper" with the mechanism as Figure 2 and the
octahedron as Figure 3. Verified in the PDF at dbcf1c93: every fold of
the fourth referee read's nine points is in (the acceleration's
coefficient, the theorem's name, the operational statement, the
finite-grain value, Tsirelson's value, the conditional extension, W
declared, the rotations' depth, the read-out characterization, the
abstract's limitation); the figures' pages and captions checked one by
one (the mechanism, the octahedron at 0.3 of the width, the two slits
with the Mach-Zehnder, the pair, S(N)). 41 pages.

## Applied (2026-09-22, the Boss's orders of 12:47Z and 12:54Z, records 962 and 964): three readings from their branch heads pending merge; rows 13 and 14 PENDING

One commit, the three readings cited at their branch heads with the
merge SHA to be swapped in when each lands: (1) the order channel
(order-channel-run at 389dc5d10c83): Table 2 row 1c after 1b, the
second party's serial correlation 15/16 under a = 0 and -1/16 under the
period-3 cycle 0, 21, 42 (DETECTOR), the marginals 96/96, the algebra
at 16 of 16 checks, nature 0, FAIL; the Bell section's plain statement
and the discussion's positioning sentence cite the row. (2) The atom
(atom-give-momentum at 686673f785f6; CAUSE.md on main at 8ee973d6, PR
#867): row 6 by kind (C1 PASS, no escape in 7500 intervals, 23 quarter
crossings; 12 to 7 Links; the period 1431 to 1040; C2, C3 FAIL as
declared; the baseline's escape at 3407) and the paragraph (viii) of
Section 9. (3) The Gleason bound (gleason-bound at 1f0ea47b417b):
w* = 1/1516 on j = +-3 mod 8, about 0.02 on j = +-1 mod 8; the error
bound A sqrt(2 R*) + A^2/2 replacing "no theorem is given"; the table
click's zeros at N_phi = 8192 and none at N_phi = 64. Rows 13 (the
bending's ring re-run, pin 0.731 +- 0.025 at b = 6, gamma = 1) and 14
(Newton's D3 rows under the one constant, pins 384 and 768, against
2.00 +- 0.18) PENDING their run of 2026-09-22, the ledger's bending and
Newton rows keeping their words; the caption's counts updated; six
bibitems (orderchannel, atomcentred, atomcause, gleasonbound, dyson1920,
nist). Every new number a NUMBERS.md row by kind. 43 pages. Held next:
the ring's SHA (row 13) and Newton's SHA (row 14), each folded on its
head the same way; the merge SHAs swapped in when order-channel-run,
atom-give-momentum, gleason-bound and PR #860 land.

## Applied (2026-09-22, the owner's word): what the law names and has not computed

The owner asked that the paper state, somewhere, the things the law
could compute and this paper has not computed. One paragraph in
Section 9 before Positioning, "What the law names and has not
computed": the atom's lines (row 6), third-order interference (row 2c),
the single opening and the rows pinned without their run (10; 4a, 5b,
11), the quarks and the nucleon's binding with colour designed and not
built (records 248, 270), the unseen content (the dark sector note on
main at aa243019: Newton's field in the shell mean, the short periodic
dimension failing the Tully-Fisher slope, unseen content admitted only
as an input family; no rotation curve read after a detector), the
crowd's stretch g_1 and the periodic against the open GameBoard, the
detector's constants c_j, and rows 13 and 14 pending; apart from these
the inputs for which the law has no formula (rho_p, h, the content per
unit, N_phi). No number added. 43 pages.

## Applied (2026-09-22, the Boss's consolidated order of 14:23Z, commit 1): rows 13 and 14 read, the algebra beside the runs, the merge SHAs

Row 14 (newton-one-constant at f44a69e5, PR #879, pending merge): by
formula first (F_plane = 1.2871, n = 8, 384 / 768, the ratio 2.00), then
the run of 2026-09-22 (the controls inside, the orbits outside, the ratio
1.677 against 1.82 to 2.18, 4 inside, 7 outside, none moved), FAIL as
read; the registered D3 row (n = 9) history beside it. Row 13
(flow-link-build at a3be9ba1, PR #854, pending merge): the law's FAIL
(series K, 0.000 pixel) carried in the row as the physicist reviewer's
finding 4 asks; the algebra first (STEP_ALGEBRA.md: C_ring = 5.12 as
built, the M / b form recovered; flow_weight/ALGEBRA.md: 3.65 / 3.82 /
3.92 against 4, 2 c_f within two factors, gamma an input); the run: b = 6
gamma 0 inside its four pins, C_ring 1.806 against 1.929 +- 0.085 (the
README pins it, OUTSIDE by 0.038, 1.45 grains, as the algebra's own
1.46; written by the source, COMPUTATION from the clicks), b = 6 gamma 1
refused by the working bound, NOT DECIDED. Row 6 and Section 9 (viii):
the atom's algebra first (atom_algebra/ALGEBRA.md, NEEDS A NEW RULE),
the law's FAIL (the escape at 3407) beside the key's C1 PASS, the lines
NOT COMPUTABLE by any run of the law as built (the physicist's finding
5). Section 5's bending paragraph and Section 9 (vi): the algebra's
number first, the run's reading after. Merge SHAs swapped: the order
channel (main 804a8da0, PR #874), the centred step (a4794cc6, PR #876),
the Gleason bound (e6809713, PR #875); PR #860 (b12dd253), #879 and #854
still pending. Five bibitems added (stepalgebra, flowalgebra,
atomalgebra, ringrun, newtonrun). No figure. 46 pages.

## Applied (2026-09-22, the Boss's consolidated order of 14:23Z, commit 2): the eleven MUST-FIX findings of the two whole-paper reviews (record 974)

PHYSICS_REVIEW.md (main fdc96079) findings 1 to 7 and MATH_REVIEW.md
(main 5550a2d1) findings 1 to 4, each in the paper's manner: (a) one
verdict count computed from the rows, written in the caption and
repeated verbatim in the abstract and "What is proved", the failures
paragraph listing every FAIL row by number, 1c and 8b among them, row 12
HISTORY and not a pass (the lattice pin a gate on the code; 4.6 percent
off nature with no uncertainty stated; the weak-field re-read pending),
the sentence naming rows the table does not carry corrected; (b) no
GAMEBOARD number in a verdict: row 7a from the DETECTOR mass, row 8a
from the DETECTOR width 0 with the factors 88 and 25 to 40 a labelled
aside, the redshift rows 3, 4b and 12 with their time base named (births
DETECTOR per tick of the open-face detector, the host's interval,
GAMEBOARD, record 768; the detector's own clock NOT READ) and the
platform paragraph qualified the same way; (c) the Lorentz sentence
after the owner's chain sentence now says once that Lorentz of the world
is assumed through (A1) and k_AB = k_BA and that the conversion brings
it, nothing deriving the group from the six verbs, "nothing of
Einstein's put in" read as no factor of Einstein's entering the steps;
(d) the chain's Inside step named as the click frame's walk with its
invariant cos omega = cos m cos kappa, Eq. (1) carrying W only as the
declared identity of Eq. (14), the paragraph opened with that sentence;
(e) E_0' = E_0 / c^2 = N_l N_w M the rest energy in whole units in Eq.
(14), Section 2 and the symbol table; (f) the fan's Manhattan factor F
= <S_1 / |D|> in Eqs. (2), (3), (4), the ledger's and the roads table's
Newton rows, with its values and where the presence absorbs it, the
orbit read note cited by SHA. Also the cross-reference of this hour's
not-computed paragraph made unambiguous. The SHOULD-FIX and NIT items
and "what is missing" wait for the owner's word. 48 pages.

## Applied (2026-09-22, the owner's word): the central formulas boxed; the independent read's issues #882 and #883 answered in the text

The owner asked whether the paper's central formulas, the ones unique
to it, are boxed: only W (Eq. 14) was. Boxed now: Eq. (1) the map of
one accumulator, Eq. (9) the rung and the click, Eq. (11) the quadratic
read-out on the phase lattice, Eq. (13) the finite-grain value 181/64.
The recovered forms (Newton, Coulomb, the fields, the wave equation)
stay unboxed, being nature's known forms. The independent read of the
manuscript on main (batch #877, issues #882 and #883, the comment on
#872) answered on GitHub with the head's SHA and, where the paper was
short, in the text: Gauss's law with the crossing's sign, no splitter,
absorber or cancelling pair inside, a constant release per interval and
a varying release by the retarded intervals, the crossings' kind named
(GAMEBOARD on an interior surface, DETECTOR at a face); the injectivity
theorem's scope, the rows' linear block, a body's drive with its lost
coincident fire outside it. 48 pages.

## Applied (2026-09-22, the owner's word through the Boss's order of 15:11Z): the bending and the atom as conjectures from the algebra

The owner: last attempts on the light bending and the atom so that
they are in the paper; algebraic formulas thought derived may enter as
conjectured. (A) The bending: in Section 5, Section 9 (vi), row 13 and
the ledger, the coefficient 2 (1 + gamma) on the one constant stated as
a conjecture, labelled "conjectured from the algebra, not read", from
flow_weight/ALGEBRA.md's ring (3.65 / 3.82 / 3.92 against 4, closing to
2 c_f within the two stated factors); what is read stays: series K's
0.000 pixel (FAIL), the gamma 0 ring inside its pins, the gamma 1 ring
NOT READ; the verdict word NOT DECIDED. (B) The atom: in Section 9
(viii), row 6 and the ledger, the ladder a_j = j^2 h^2 / (4 pi^2 kappa
m), (j / i)^2, (j / i)^3, the virial form E_j = -j h / (2 T_j)
proportional to 1 / j^2, two lines in (1 / i^2 - 1 / j^2), 27 / 20, as
a conjecture in the shell mean's limit, from ALGEBRA.md and LEVELS.md
(atom-levels at cd0c2029, PR #891, pending merge); what is read stays
(the r = 12 loop's staying and tightening); the reviewer's read (record
991, pending merge) that the three-rung ratio at the lattice's grain
cannot decide (1.280, 1.373, 1.431, the band +- 0.13 to 0.29); row 6
NOT YET on the line. (C) One sentence in the abstract and one in "What
is proved" naming the two conjectures and distinguishing them from what
is read; in the not-computed paragraph the two moved to "conjectured,
not computed". Never "recovered", never "matches nature". (D) No SHA
swapped; the citations as they stand. 49 pages.

## Applied (2026-09-22, the Boss's order of 15:26Z): the generic entry cited at its merge

PR #855 (the generic entry of the bending: the flight in the age wall's
set at 1 + gamma, gamma an input; the one form of the last Link's time;
the square ladder in place of the root) merged to main at 5b855791. The
paper cited the entry by its date only, never by a branch head or as
pending, so no SHA was swapped; the entry is given its reference
(genericentry, main at 5b855791) at the first mention (Section 5, the
clock's form) and in row 12. The paper's "the law as built" for the
flight (series K's 0.000 pixel, row 13) is the law before the entry;
no reading of the bending under the entry is in the paper until the
Boss names one. 49 pages.

## Applied (2026-09-22, the independent read's issue #896): the six-heading check's factor 1

Issue #896 (batch #893) asks what the paper's MUST-FIX (f) fold
already gives (the unit-width shell, the incidence count S_1 / |D| per
beam, the fan's mean F in Eqs. (2) to (4) and the ledger, the presence
absorbing it, flow-link-v1 dividing by the same mean) and, its item 5,
that the six-heading check (series C) has the factor 1 and does not
test the coefficient: one clause added after Eq. (2). Its item 6 (the
three-dimensional shell count's error source) is the mathematician's
SHOULD-FIX 11 and waits on the owner's word. Answered on the issue with
the head's SHA. No number added. 49 pages.

## Applied (2026-09-22, the Boss's order of 15:37Z): the atom by the algebra alone with the scale statement; the ring read on the split ladder

(1) The owner's word (record 997): the atom's levels cannot be read on
any lattice that can be run (the orbit's radius sixty thousand times the
nucleus's; the lattice's r = 3 to 12; the fan's grain the named limit;
a lattice of order fifty thousand on a side not run). Section 9
(viii), row 6 and the ledger's atom row: the conjecture's label kept,
the scale statement added, "computed from the algebra, not read on the
board; a lattice able to hold the scale is not run"; the three-rung
sentence removed (a side track, no run of the levels cited as a
reading); row 6 NOT YET on the line; what is read stays as read. (2)
The ring's run on the split ladder (flow-link-build at de4f4410, PR
#854, pending merge): the reviewer's sentence by kind carried word for
word in row 13; the verdict DOES NOT CLOSE within the grain by the
README's rule (its headline CLOSES on the deciding pin, the pin inside,
said in the row); Section 5 says the law as built is the law before
the generic entry (main at 5b855791) and the readings under the entry
are the ring's alone; Section 9 (vi), the abstract, "What is proved",
the not-computed paragraph and the ledger's bending row updated the
same way; the ringrun reference at de4f4410. Series K's FAIL stays;
"matches nature" nowhere. 49 pages.

## Applied (2026-09-22, the owner's word "go"): the submission form

The owner asked what could reject the paper at an editor's desk and
where to submit; the answer (arXiv first, then Foundations of Physics,
International Journal of Theoretical Physics second) and the five
changes he approved: (1) the declaration of the use of artificial
intelligence, in a Declarations section before the references, with
funding, competing interests, ethics, data and code availability (the
Zenodo concept DOI, the commit of Appendix C, the ledger) and author
contributions; (2) the abstract at journal length, the long abstract
kept as the introduction's first paragraph "The paper in one page";
(3) a paragraph "What this paper contributes, and what it does not
claim" at the end of the introduction; (4) the project's jargon out:
"the author" for "the model owner", the log cited by its record
number, the pull request numbers out of the references (the merged
ones by their main commit, the pending ones by branch and head, the
merge commits still to be swapped in); (5) COVER_LETTER.md, a draft
for the author's hand with five suggested reviewers from the cited
literature, affiliations to be confirmed by the author. No physics and
no number changed. 50 pages.

## Applied (2026-09-22, the Boss's order of 16:43Z): the final build

The owner's word (record 993): the paper closes. The swaps: Newton's
run at its merge on main, 7682c57d (the reading's files unchanged by
the merge); the ring's run at flow-link-build's head b094c53b pending
merge (the run's numbers de4f4410's; the README's own headline now
DOES NOT CLOSE by its rule with the deciding pin inside, so the
parenthesis on the headline is dropped, the row's word unchanged); the
atom's levels at atom-levels' head 83b1bf2e pending merge; the register
(b12dd253) and records 991 and 997 pending as they are. The PDF rebuilt
and committed as the closing build; one small swap commit follows when
the two branches merge. 50 pages.

## Applied (2026-09-22, the Boss's order of 16:51Z): issue #905, the paper's law identity, option 2

The independent read's batch #900 (issue #905): the pinned runtime on
main carries the generic entry of the bending as the law, while the
paper defines and evaluates the flight blind to the crowd. Frozen as
option 2 under the owner's standing words (record 951, the reader's
corrections orderly; record 997, the paper closes as it is): the
paper's law is the runtime before the generic entry, the runs' own
commits on main's first-parent line up to 3a9a7109 (the last commit
before the entry's merge 5b855791); the generic entry is a later rule
of the law, and the ring's run (row 13) is the paper's one reading
under it. Said in one sentence at P9 and one in Appendix C, and in one
clause each where a reader would otherwise take the pinned runtime for
the paper's law: the delay section, the ledger's constancy-of-c row,
the failures' tally (13), Section 9 (vi); Section 5 carried it
already. No number, verdict or physics changed; no re-read. Option 1,
the paper about the runtime with the entry (P9, the ledger, the delay
and light sections, the tally and the provenance rewritten and every
affected comparison re-read under the entry), is a later version's
work, the owner's to order, not this paper's. 50 pages.

Correction (the same day): the build of 58a65a93 is 51 pages, not 50;
NUMBERS.md carries the correcting row.

## Applied (2026-09-22, the owner's word of record 1014 through the Boss's order of 17:22Z): the declaration in the customary form; the reviewers verified

The declaration of the use of artificial intelligence rewritten short
and in the journals' customary form: the model named as a tool (code,
computation, the drafting of the text) under the author's direction,
the author responsible for every claim, and the author's statement in
his own words: every postulate and hypothesis laid down by him, nothing
external brought in, the forms of Newton, Kepler, Einstein, Lorentz,
Bohr and Balmer the things compared with, not inputs (record 817). The
cover letter's five suggested reviewers kept, each with an affiliation
checked on the institution's or a public research page on 2026-09-22
(Arrighi, Université Paris-Saclay; Meyer, UC San Diego; Spekkens,
Perimeter Institute; Kurtsiefer, CQT Singapore; Elze, Università di
Pisa); the letter's own AI statement matched to the declaration. No
physics, no number. 51 pages.

## Applied (2026-09-22, the Boss's order of 19:03Z): the swap's first commit on a fresh branch from main

On `paper-swap-2026-09-22` off main at ee3d34f6, one commit through the
generator's sources, nothing else in the paper. (1) The ring's run cited
at PR #854's merge on main, 23b0e630, the files unchanged from the branch
head b094c53b; the atom's levels left at the branch head 83b1bf2e with
"merge pending" in the generator's source, a one-line commit to swap it
when PR #891 merges. (2) Row 14 per issue #927 and the diagnosis merged at
5ce4eb06: the noun corrected (the periods of two closed loops in the
nature cell; the run's readings the means of the recurrences of x before
the escape), the escapes at 1208 (r12_flow, the face +y) and 2452
(r24_flow, the face -x) as face clicks, DETECTOR, no loop closed, the
ratio 1.677 a computation from two such means and not a reading of the
force's exponent, the loops not similar figures (mean radii 24.3 and
37.6); the verdict FAIL as read stays, the law's, the row among the FAIL
rows, the ratio not compared with nature; a bibitem for the diagnosis.
(3) The third law at rest per the reviewer's read T on issue #920 (record
1042, option 1): the ledger's row, one sentence after the paid messages'
sentence (the free family's third law a symmetry of two readers, not a
balance per message; the momentum lines a report of the GameBoard), the
Section 4 sentence (to the apportioning's grain, six parts in 10^6, a
GameBoard reading, a diagnostic) and the ground paragraph (Gauss's law
and the equivalence principle exact; the third law the two readers'
symmetry to the grain); the paid sentence stays; DERIVATIONS_BEAM
untouched. (4) Row 5a's bound with the clause proposed on issue #555,
verbatim. (5) Theorem 3 with the joint-table condition B^H B = A I and
Appendix A's sentence with the zero-turn table as the witness (issue
#557); the proof's line names the condition; no claim about the paper's
worlds changes. No physics changed, no pin moved. 51 pages.

## Applied (2026-09-22, the Boss's order of 19:20Z): the reviewer's look X of PR #930, one line and two words

Row 14's verdict cell: the FAIL's ground named as the reviewer gave it,
the law's at the launch pace 0.34 c, the probes left a confining push
and no loop closed, the face clicks the reading; the ratio not compared
with nature. The mean radii 24.3 and 37.6 labelled CONVERSION (a length
made from the clicks' places, the diagnosis's 3.3), not DETECTOR; the
ledger's page-count rows HOST from here on. Nothing else; the #891 merge
SHA and the orbitread bibitem rename wait for the later one-line commit.
No physics, no pin moved. 51 pages.

## Applied (2026-09-22, the Boss's order of 20:26Z): the follow-up, three items, on a fresh branch from main

On `paper-followup-891` off main at d8afc87c, one commit. (1) The atom's
levels cited at PR #891's merge on main, d8afc87c, LEVELS.md unchanged
from the branch head. (2) The first of the two references keyed
orbitread renamed orbitlegs; it is cited nowhere, and the generator keeps
only cited references, so it leaves the list (88 references); the one
citation, the fan's Manhattan mean 1.287, keeps the second entry. (3) The
CHSH refutation sentence restricted to the proved subset (issue #938,
option 1): the registered grains, the powers of two from 512 to 32768;
17/6 at 768; the scan 2.82443 to 2.83212 over 1024 to 4096 as the check's
scan, not a bound beyond it; the kind named. Found on the way and fixed
in the same commit: the three merge citations carried "PR #NNN", and the
character # does not compile; rewritten without the number (the
submission form's rule). Found and recorded: the PDFs of PR #930's two
commits were compiled from a stale copy of main.tex (f82e73d1) left in
the compile directory, so the committed PDF on main is f82e73d1's text;
this commit's PDF is compiled from the true source and read back. 52
pages, not 51: the true count of the text since PR #930.

## Applied (2026-09-22, the Boss's order of 21:08Z): issue #941, the two sentences of the timing claim, option 1

On `paper-941` off main at d7c0ddc0, one commit, words only, no number.
Definition 8: the first party's outcome "determined at its arrival by u
alone, computable there from the record's own wheel, and written only at
the completion" in place of "fixed at its arrival". After Theorem 6:
"No-signalling in the arrival intervals and in the counts" in place of
"in the times as well as in the counts", with the clause that neither
party's recorded outcome exists as a row before the completion, whose
interval is the last arm's, so the availability of the record, unlike
the arrival, waits on the far arm's length, and the paper claims no
independence for that latency. The count theorem and the
sequential-order FAIL unchanged; no engine change. The PDF compiled from
the true source (no copy of main.tex in the compile directory) and read
back. 52 pages.

## Applied (2026-09-22, the Boss's order of 21:16Z): the reviewer's read AA of paper-941, three lines

A second commit on `paper-941`, words only. The reviewer's reason: u is
fixed at the record's birth (amplitude.py, the wheel reading u = ordinal
x r mod W; LiveRecord.birth), not at the arrival, so "at its arrival" was
the overreach even with "determined"; and the arrival interval is the
host's tick at the arm's set, GAMEBOARD, which the two sentences did not
say. (i) Definition 8: u the record's wheel reading fixed at its birth,
so determined before either arrival and known at the first party's
arrival from the record's own wheel under the hypotheses of Theorem 6,
computed by nothing at that arm and written only at the completion. (ii)
After Theorem 6: the first party's outcome determined by u at the
record's birth and the second's at the completion, both written at the
completion; the non-local step on the labels, its interval, the record's,
the last arm's. (iii) The arrival interval the host's tick at the arm's
set, GAMEBOARD (record 768); the arm's own count read only under the
later key clock_stamp, outside this paper's law. No number moved. The PDF
compiled from the true source and read back. 52 pages.

## Applied (2026-09-22, the Boss's order of 21:22Z): the Positioning paragraph's phrase, paper-941's third commit

The one remaining "not on the times" (the Positioning paragraph: the
click's assignment of the second outcome a non-local step on the labels)
brought to the clause after the marginals theorem (Theorem 5 in the
PDF's numbering, label th:marginals; the sentence follows its proof):
"its interval the last arm's (as after Theorem 5)". Nothing else; words only; the PDF compiled from the
true source and read back. 52 pages.

## Applied (2026-09-22, the Boss's order of 22:10Z): issue #953, the multiplicity's symbol in Definition 7's equation

On `paper-953` off main at 5757c6b9, one commit, notation only. The one
occurrence changed: the displayed equation of Definition 7, the square's
denominator, `\frac{w^2}{m}` to `\frac{w^2}{\mathtt m}` (main.tex line
539 on main). The search over the whole paper for a plain m meant as the
multiplicity found no other: every other multiplicity is `\mathtt m`
(the tuple, the split's `\mathtt m A`, Theorem 2 and its proof, the five
`w^2/\mathtt m`); the plain `m` at Sections 2 and 9 is the mass angle
and the symbol list's `m` the mass; `\texttt{m}` in the tables is a
family's name. None of those touched; no plain m of doubtful meaning. No
number moved. The PDF compiled from the true source and read back. 52
pages.

## Applied (2026-09-22, the owner's word through the Boss's order of 23:00Z): the opening, the algebraic object first

On `paper-opening` off main at 067b2472, one commit, words only. (a) A
new first paragraph of the Introduction, "The algebra first", before
"The paper in one page": the object (the integer group ring of the
cyclic group of the phase grain on the cubic lattice whose symmetry is
the cube's rotation group of order 24, Theorem 1), the six integer
operations, what is exact as identities under declared tables (Theorems
2 to 6, the books, Gauss's law, the pace), and what is reached from the
same object under (A1) and (A2): Lorentz's factors' form, the
equivalence principle, Einstein's step, and in a limit under a shell
average Newton's inverse square; "reached from the algebra, not derived
from nothing"; the law as built meets (A1) and not (A2); Table 2 row by
row; the closing sentence, the owner's own word, that the algebra first
and the comparison after is the order in which the model was found. (b)
The abstract's first sentence turned to the object; the sentence traded
is the third ("The rules are a cyclic group, a group ring, integer
matrices and an evaluation at the roots of unity"), folded into the
first; the abstract 246 words (mathematics counted one token each). No
number moved, no claim changed, no row touched; "derived" nowhere. The
PDF compiled from the true source and read back. 52 pages.

## Applied (2026-09-22, the Boss's order of 23:45Z): the reviewer's read AC on the opening, and the owner's third word

A second commit on `paper-opening`, words only. (a) The chain sentence
with the hypotheses named line by line: under (A1) with (A3), locality
Outside, the r-free lines of Lorentz's factors; under (A2) their scale
and Einstein's step; under (A1) and five assumptions of the law as
built, with no (A2), the equivalence principle and, in a limit under a
shell average, Newton's inverse square; "reached from the algebra, not
derived from nothing" kept; "an identity of it under declared tables and
world conditions". (b) The lattice's symmetries are the 48 signed
permutations of the axes, their rotations the group of the cube of order
24, in the paragraph and in the abstract. (c) The paragraph's closing
sentence ("That order ... is the order in which the model was found")
dropped: the beginning states, it does not narrate (the owner's word).
The abstract at 250 words (mathematics counted one token each) after
four words traded for read AC's: "finite-grain" (One value), "named"
(Recovered in a limit), "and" for a comma (the one non-local step, the
only read-out), "conservation" (the books). No number moved, no claim
changed. The PDF compiled from the true source and read back. 52 pages.

## Applied (2026-09-22, the owner's word of records 1104 and 1108 through the Boss's order of 00:00Z): the central idea visible

A third commit on `paper-opening`, words only. (a) The abstract carries
the sentence "Everything the paper compares with nature is a count
between clicks at a detector, or a ratio of such counts; nothing
measured inside the board is compared", joined to the tally sentence in
place of "Every reading is compared with nature by kind"; kept at or
under 250 by trades inside the abstract: "the GameBoard" (named in the
text), "one rule of ... bounded, acts" to "six bounded integer
operations ... act", "there are" to "are", "the only read-out", "as" twice
(the click's weight a positive quadratic form; the CHSH sum an exact
rational), "count" before marginals, "enter as labelled conjectures from
the algebra ... neither is established" to "are conjectures, not
established", "and ... though" to "; ... ,". 248 words (mathematics one
token each). (b) The opening paragraph, after the sentence on the exact
identities: "Every quantity compared with nature is a count between
clicks at a detector or a ratio of such counts; a reading of the board
itself is a diagnostic and is compared with nothing (the reading rule
below; Section 8; Table 2)". No number moved, no claim changed. The PDF
compiled from the true source and read back. 52 pages.

## Applied (2026-09-23, the owner's choice): the title from the group of order 24

The owner chose candidate B of the four put to him: "Universe24:
Physical Relations from the Group Ring of a Cyclic Group under the
Octahedral Group of Order 24", in place of "Universe24: Physical
Relations from a Common Discrete Update Rule". The lattice leaves the
title and stays in the abstract as the way. A fourth commit on
`paper-opening`; nothing else changed; the PDF compiled from the true
source and read back. 52 pages.

## Applied (2026-09-23, the owner's word through the Boss's order of 00:25Z): "the group of order 24", the name everywhere

A fifth commit on `paper-opening`, words only. The group is named "the
group of order 24" wherever the paper names it in words; "the rotation
group of the cube" and "the symmetric group S_4" follow in apposition
once each, in Theorem 1 and in its proof, where the isomorphism is
stated; the 48 signed permutations stay where read AC put them. Every
occurrence, before and after:
- the abstract: "their rotations the cube's group of order 24" to
  "their rotations the group of order 24";
- the opening paragraph: "their rotations the group of the cube of
  order 24 (Theorem 1)" to "their rotations the group of order 24
  (Theorem 1)";
- Theorem 1's statement: "its kernel, the rotations of the cube, has
  index 2 and order 24, and is the group of the permutations of the
  cube's four body diagonals" to "its kernel, the group of order 24
  (the rotation group of the cube), has index 2 and is the group of the
  permutations of the cube's four body diagonals, the symmetric group
  S_4"; the sentence "tells the 24 rotations from the 24 reflections"
  stays (a count of elements, not the name);
- the ledger's row: "The group of the six Ports, 48 and 24" to "The
  group of the six Ports, 48, and within it the group of order 24";
- Section 9, "What is proved": "the group of the six Ports and its 24
  rotations" to "the group of the six Ports and, within it, the group
  of order 24";
- Appendix A, the proof: "its kernel, the rotations, has index 2 and
  order 24, and it acts faithfully on the cube's four body diagonals, so
  it is the symmetric group on them" to "its kernel, the group of order
  24, has index 2 and acts faithfully on the cube's four body diagonals,
  so it is the symmetric group S_4 on them" (B_3 and the 48 kept);
- Appendix C, the symbols: "48 signed permutations, 24 rotations" to
  "48 signed permutations, their rotations the group of order 24";
- left as they are: Section 3's "48 in all, the symmetry group of the
  cube" (the 48, not the 24); "the GameBoard's stand-in for the rotation
  group" (the continuum's rotation group, not the model's); Theorem 1's
  title "the 24 of the name"; the title's "the Octahedral Group of
  Order 24" (the owner's choice, the name with its apposition).
The abstract 247 words. No number moved. The PDF compiled from the true
source and read back. 52 pages.

## Applied (2026-09-23, the owner's word through the Boss's order of 00:55Z): Newton, Lorentz and Einstein named in the abstract

On `paper-abstract-names` off main at dd0c111c, one commit, the
abstract only. Newton named where the inverse square already stood
("under a shell average Newton's inverse square and Poisson's
equation"); one new sentence after the limits: "Under two named
hypotheses on the click, Lorentz's factors, the equivalence principle
and Einstein's step are reached, not derived from nothing; the law as
built meets the first only."; the CHSH value folded into the exact
results' sentence ("181/64 from 512 to 8192, 1.05 standard errors from
the measured CHSH value"); "It has no relativistic dynamics; its
sequential wheel signals in a pair's order, not in its counts." Paid for
inside the abstract, no claim lost: "of a free family's flux" after
Gauss's law, "the lattice" after Outside, "positive" before quadratic
form, "not established" after conjectures, the tally's verbs, "the forms
of", "above the board", "hypothesis". The owner's central sentence
untouched. 248 words (mathematics one token each). Accepted usage:
"recovered in a limit", "reached under named hypotheses" are the forms
abstracts use for Newton's, Lorentz's and Einstein's laws; "derived
from" without a qualifier is what desk rejections cite. The PDF from
the true source, read back. 52 pages.

## Applied (2026-09-23, the owner's word through the Boss's order of 01:30Z): the abstract for a reader of quantum mechanics

A second commit on `paper-abstract-names`, the abstract only. The
bridge is the postulate P1 (bounded integers; the phase on the circle
Z_N): "the phase discrete in N steps" in the first sentence in place of
"the phase grain"; after the Outside sentence: "An amplitude is an
integer sum of N-th roots of unity and the Born rule its square at the
click, under one axiom of the apparatus; interference, marginals and
CHSH are then exact rationals of N." Paid for inside the abstract: the
click's weight and the pair's marginals moved into that sentence out of
the exact-results sentence; "Born's rule" and "Young's spacing" out of
the recovered list (the Born rule and interference now stated as
exact); "of the axes", "coefficient", "CHSH" before "value", "Recovered
in limits", "their clicks" to "clicks", "passes to a detector" to
"ends", "It has" dropped before "no relativistic dynamics". Newton,
Lorentz, Einstein, the owner's central sentence, the tally, the
conjectures and the two limitations kept. 250 words (mathematics one
token each), the journal's limit. The PDF from the true source, read
back. 52 pages.

## Applied (2026-09-23, the reviewer's read AD through the Boss's order of 02:00Z): two word changes in the abstract

A third commit on `paper-abstract-names`, the abstract only. (a) The
Lorentz sentence: "Under two named hypotheses on the click, Lorentz's
factors and Einstein's step are reached, the equivalence principle
under the first alone, not derived from nothing; the law as built
meets the first only." (the equivalence principle needs (A1) and the
law as built, not (A2); a reader took the old order as needing (A2)).
(b) The close with the law as its subject: "The law as built has no
relativistic dynamics; its sequential wheel signals in a pair's order,
not its counts." The eight words these cost, traded inside the
abstract, none in the owner's central sentence and no name: "begins
with" to "has"; "discrete in N steps" to "discrete, N steps"; "on that
ring" to "on it"; "and the Born rule" to ", the Born rule" and "then"
dropped; "the pace of every direction, and" to "every direction's
pace,"; "the measured value" to "the measurement". The optional
condition after the CHSH value ("a prediction once the wheel meets
no-signalling in the order") not added: no words left under 250. 250
words (mathematics one token each). The PDF from the true source, read
back. 52 pages.

## Applied (2026-09-23, the reviewer's whole read through the Boss's order of 00:50Z): Born's form exact, Born's rule its limit

A fourth commit on `paper-abstract-names`, the abstract only. The one
claim beyond the body, "the Born rule its square at the click", is
brought to the ledger's word (row 276, the click's square Born's form
exact; Born's rule its limit with a rate 1/N per cell): "An amplitude
is an integer sum of N-th roots of unity, Born's form its square at the
click under one axiom of the apparatus, Born's rule its limit;
interference counts, marginals and CHSH are exact rationals." The two
words this cost are taken from the central sentence, the same claim:
"Everything compared with nature is a count between clicks at a
detector or a ratio of such counts". The optional "from the measured
CHSH value" not added: no words left. 250 words (mathematics one token
each). The PDF from the true source, read back. 52 pages.

## Step 1 of the reordering (2026-09-23, the Boss's order of 23:10Z, the owner's go and his approval): the plan, docs only

On `paper-algebra-first` off main after the abstract's four commits merged
(PR #967, merge c324434d6f7ee52811c86ef622eef5c618c0da06; the paper file last changed at d2a58a7d). The sources
cited by the plan, all merged: docs/GROUP_STRUCTURE.md (PR #968, merge 7739bbbea5846ec5efccc83ca3e24bf695d5b9a5),
docs/designs/fail_rows/WHAT_IS_MISSING.md (PR #964, merge c66de8718357beae6114590a1f86c21c59a84299), RUN_8BC.md
(PR #975, merge 907f339d08eaa64c29acab190e106b74f06e67ee). Nothing of the paper's text changes in this commit; step 2,
the reordering itself through the generator, starts only on the Boss's go
after this plan is read. The plan follows, in the order it was drafted through
the evening of 2026-09-22, each of the owner's words folded in where it came.

## Planned (2026-09-22, the owner's word through the Boss's order of 23:10Z): the paper in the algebra's order, step 1, the plan

The owner's word: the paper begins with the algebraic object and says
all of it first (the group of the six Ports, the 24, the cyclic group
of the phase and its ring, the families of the ring and how the
operations act on their members), then says that not all the physical
rules were put into the algebra but part of them, and then what that
part gave. This is a reordering of the present text; no claim, no
number, no row and no verdict changes; every sentence moved keeps its
words, and the only new prose is the section's opening lines and the
paragraph in the owner's words. Step 2 (the reordering itself, through
the generator) starts only on the Boss's go after this plan is read.

### The new order of the sections

1. Introduction (as now; its first paragraph "The algebra first"
   stays, and its "The words of this paper" paragraph moves to the new
   Section 2).
2. **The algebra: the group, the ring and the families** (new; made of
   moved text). In this order:
   - The six Ports and their group: the paragraph "The six Ports, the
     group and the front" and Theorem 1 (th:group) with its proof
     reference, from Section 3 (lines 294 to 322 now); the hand as the
     pseudoscalar column; the 24 rotations and the 24 reflections.
   - The cyclic group of the phase and its ring: the record as an
     element f = sum f_p x^p of Z[Z_N], the pointer ev(f) at the roots
     of unity, and the pair's record in Z[Z_N] x Z^2 x Z^2 (the
     paragraph "The objects", line 704 now, from Section 6), with
     Definition "Row and record" (def:row, line 536) and its amplitude
     equation.
   - The six operations on those objects: the paragraph "The road from
     the cells to the algebra" (Section 2 now) and Definition "The
     update rules of one interval" (def:rules, line 563, from Section
     6): the translation, the split (the table), the merge (the ring's
     addition), the rotation (the integer matrix), the evaluation (the
     click) and the accumulator (the division with the remainder kept).
   - The families as declared integers on the objects: Appendix D's
     table tab:families brought forward whole (its caption and the
     three columns "the declared integers", "the algebraic object",
     "the verbs that act on it"), with the paragraph "The words of this
     paper" (Section 1 now) as its introduction; the column "the click
     that reads it" stays in the table (it names the rows of Table 2).
   - **The paragraph in the owner's words** (new prose): not all the
     rules of physics were put into the algebra; what was put in is the
     six operations and the declared tables, and what was not: the
     atom's rule (no operation quantises a body's loop), the hypothesis
     (A2) (the amplitude's split between staying and hopping; the law
     as built meets (A1) only), the recoil at a free release (the free
     family's third law a symmetry of two readers, not a balance per
     message), the collision (Rule C acts in no world of this paper),
     the tables at 1/256 (a declared input, P7), the masses and the
     coupling matrix's entries (initialisation and declared integers,
     not results), the shell average (a limit taken Outside, not an
     operation Inside), and the generic entry of the bending (a later
     rule, outside this paper's law identity). "We put part of the
     rules in, and saw what they gave."
   - What the part put in gave, in one paragraph: the exact identities
     (Theorems 2 to 6; the books; Gauss's law; the pace with its
     Manhattan bound), the limits recovered (c = 1/sqrt 3, Born,
     Tsirelson, Young, the inverse square and Poisson under a shell
     average), the chain to Lorentz's factors, the equivalence principle
     and Einstein's step under (A1) and (A2) and to Newton in a limit
     (Section 9's chain, cited, not moved), and the comparison by kind
     (Table 2).
3. The law and its implementation (Section 2 now, minus the two
   paragraphs moved up; its map Eq. (1), the state, the components, the
   two blocks, the read-out, the hand-worked update, the code, the
   ledger stay).
4. Geometry and symmetries (Section 3 now, minus the Ports paragraph
   and Theorem 1; the symmetries, the octahedron, Proposition 1 and
   "What a detector measures" stay).
5. Conservation, the flux and the forces (unchanged).
6. The delay field (unchanged).
7. Measurement and the quadratic form (Section 6 now, minus def:row,
   def:rules and "The objects"; Definition "The click" (def:click), the
   rungs, the lemma, Theorems 2 to 4 and the rest stay; a one-line
   pointer to Section 2 where the definitions were).
8. Bell and CHSH (unchanged).
9. The simulator's checks and the comparison with nature (unchanged).
10. Discussion and conclusions (unchanged; its chain stays where it is
    and is cited from Section 2).
Declarations, References, Appendices A to C unchanged; Appendix D keeps
the roads table (tab:roads) and its dated transition paragraph, and
loses the families table (moved up) or keeps a one-line pointer.

### What moves, by label

- th:group (4 references), def:row (1), def:rules (2), tab:families
  (5): move to Section 2; every \ref follows the label, so no
  cross-reference is rewritten by hand; the generator's assembler
  moves the text blocks and the numbers renumber themselves.
- The shared theorem counter: Theorem 1 stays Theorem 1 (first in the
  new Section 2); the two definitions moved up become Definitions 2
  and 3 in order of appearance and the click's definition follows
  later; the theorems 2 to 6 keep their numbers (they stay in order
  after Theorem 1). The reviewers' issue comments cite "Definition 7"
  and "Definition 8" by the old numbers; the labels are what the paper
  cites, and the NUMBERS.md row of step 2 will list the old and the
  new numbers side by side.
- sec:law, sec:geometry, sec:measurement keep their labels; their
  section numbers move by one (2 to 3, 3 to 4, 6 to 7); every
  Section~\ref follows.
- No equation label moves except the amplitude equation inside def:row
  (unlabelled) and none is renumbered out of order: Eq. (1), the map,
  stays first because Section 3 (the law) still precedes every other
  numbered equation; the amplitude equation in the new Section 2 is
  unnumbered now and stays so.
- Figures: none move. Tables: tab:families moves before tab:ledger, so
  the table numbers renumber (the families table becomes Table 1, the
  ledger Table 2, the confrontation table Table 3, the conversion
  table Table 4); every Table~\ref follows; the prose that says "Table
  2" in words (none: the paper cites tables by \ref only, checked by
  grep) needs no hand edit; the NUMBERS.md and PLAN.md notes that say
  "Table 2" for the confrontation table are history and stay.

### What stays as it is

Every sentence of physics, every number, every verdict, the abstract
(its first sentence already turned), the chain sentence "In one chain,
with nothing of Einstein's put in", the Declarations, the references.

### The expected page count

The moved text is the same text; the new prose is the section's opening
(about 60 words), the owner's paragraph (about 130 words) and the
"what it gave" paragraph (about 90 words): about half a page. Expected
52 or 53 pages; reported at step 2.

### How step 2 is done

Through the generator: the assembler gains one step that cuts the named
blocks (by their paragraph headings and labels, matched exactly once
each) and places them under the new section heading, before the present
Section 2; the new prose enters as corrections with their own labels;
the tests of the generator (test_paper_cut30) gain one check that every
label of the paper is defined once and referenced as before (the same
\ref counts). One or two commits on paper-algebra-first; the PDF from
the true source, read back; check.py; then the physics-rule reviewer's
full read and the mathematician's check of the group's details.

### The owner's third word (23:10Z), folded into this plan

- The beginning states and does not narrate: the opening paragraph's
  closing sentence ("That order ... is the order in which the model was
  found") is dropped; the object is stated as found ("the paper has one
  algebraic object"), in the form other papers use.
- The paper is a paper on modern algebra: the new Section 2 is its
  subject; the lattice is the way the object is computed with, named in
  the abstract and in Section 3 as the tool, not in the title.
- The failures with their cause: where a FAIL's cause is a rule absent
  from the algebra (3, 4b, 6, 13; the pinned 4a, 5b), the verdict cell
  says so in one word beside FAIL, "a rule absent"; the hypotheses
  refuted (7b, 8a, 8b, 8c) and the failures of grain or apparatus (1b,
  1c, 2a, 14) named as such in the tally sentence; the verdict words the
  register's to confirm. What was found and why: the families table
  (what) and Table 2's cause cells (why) are that table; no new table
  unless the register defines a column.
- The title from the group: the rotation group of the cube, order 24,
  the octahedral rotation group (isomorphic to S4), Theorem 1; the
  candidates put to the owner; the chosen title enters at step 2.

### The owner's fourth word (23:15Z): the organisation, in the form of the great papers

The order of the paper is the order of Wigner (1939, the group first,
the particles as its representations after), Yang and Mills (1954, the
gauge group and its field first, the physics read from it), Gell-Mann
(1961, the Lie algebra first, the hadrons as its multiplets) and of a
mathematics paper (definitions, theorem, proof, then the application):

1. The algebra (the new Section 2): the group of the six Ports (48 and
   24, Theorem 1); the cyclic group of the phase and its integer group
   ring Z[Z_N]; the record as an element; the six operations written as
   maps on the ring in the algebra's own notation (the translation
   f -> x^phi f carried one Link; the split f -> (a_i x^{t_i} f)_i; the
   merge, the ring's addition; the rotation, the integer matrix U_s on
   the label pair; the click, the evaluation ev: Z[Z_N] -> Z[zeta] with
   its norm; the accumulator, the division with the remainder kept);
   the central formula, Eq. (1), boxed, read as the composition of
   those maps; the families as declared integers on the objects (the
   families table). "These are the operations of the algebra that
   nature's readings are compared with."
2. What follows from the algebra, in its own symbols: the exact
   identities (Theorems 2 to 6, the books, Gauss, the pace), and the
   forms reached under (A1) and (A2): Lorentz's factors, the
   equivalence principle, Einstein's step, Newton's inverse square in a
   limit; "reached", the hypotheses named.
3. The way: the lattice, the GameBoard and the simulator, as the way
   the algebra is computed with (the present Sections 2 to 8, reordered
   under this heading, each keeping its text).
4. How the group was reached through physics (a chapter gathered from
   what exists: "The road from the cells to the algebra", "How the
   simulator led to the results", "The transition from ordinary physics
   to modern algebra, dated", Section 9's "The platform" and "The road
   to each"): the dated entries, the six verbs found one by one, and
   what was not put in.
5. The comparison with nature by kind, the failures by cause, the
   discussion, the declarations.

Where the text can shorten under this order (the owner asks; his word on
each): the Introduction's "The paper in one page" repeats what the new
Section 2 says (about half a page); "The hand-worked update" and "In the
code" of Section 3 can go to Appendix C (about a page); Section 9's
"The platform" and "The road to each" fold into the chapter on how the
group was reached (about half a page saved by the merge); the register's
paragraphs of Section 9 ("The simulator's checks") shorten by their
duplicates of Table 2's cells (about half a page). Nothing physical is
cut; every number and verdict stays; about two to three pages in all if
every one is taken.

### The owner's fifth word (23:25Z): the cuts are allowed; where "how we reached the algebra" goes

The owner allows the shortenings listed above (his word: "if you think
it can be cut and shortened, yes"), and asks where the chapter "how we
reached this algebra" goes, since readers will ask how the group was
found. The answer of the great papers: a short motivation in the
Introduction and one section of its own before the comparison with
nature (Wigner's and Gell-Mann's papers motivate in the introduction and
keep the construction's origin to a section; a mathematics paper puts
it in "Background" or at the end). Here: five lines in the Introduction
("where the object came from") and a section of its own, the fourth in
the new order, "How the algebra was reached: from one Node and its six
neighbours to the group", between the way (the lattice and the
simulator) and the comparison with nature. Its content exists and is
gathered, not written anew: a Node and its six neighbours, the seven
Nodes of the causal front (the octahedron, Figure 3), one message per
Link per interval; the GameBoard as the way of computing between Nodes;
the twenty-four dated steps of the transition (Appendix C's paragraph,
HISTORY.md): 09-17 the amplitude a phase with a content; 09-18 the Born
table from N and a Node its six Ports; 09-19 the quantum an integer row,
the click the one border, the push one bilinear form; 09-20 the readings
by kind, every count an accumulator; 09-21 the six verbs, the record in
Z[Z_N], the lattice the translation group, the Lorentz factor refused as
a seventh verb; 09-22 the detector's clock and the click theorem. The
sentence in the owner's words: the GameBoard showed that everything
converged to this group and this ring; what did not converge was not
put in. The dated paragraph leaves Appendix C for this section; the
Introduction's "How the simulator led to the results" moves here whole.

### The owner's sixth word (23:55Z and 00:00Z): the click-to-click algebra, and the reverse direction

- Part 2 of the new order opens with a named subsection, "The algebra
  from click to click": the click as the one measured event (the
  one-way border); everything measured a count between clicks or a
  ratio of such counts (the detector's own count, the interval between
  two clicks, the smallest distance between clicks 1/(k(k+1)) on the
  k-ladder, the count ratio k_a(b) of the moving detector); the map
  from the ring's elements to those counts (the record as an element,
  its ordinal on the released rows the detector's own count, the click
  theorem as the statement about count ratios); the sources the click
  frame's section 0 and NEWTON_FROM_CLICKS.md sections 1.1 and 1.2;
  every reading of Table 2 then named as such a count or ratio, or
  marked as not one (a GameBoard reading a diagnostic, never compared).
  The central idea (records 1104 and 1108): everything is measured
  between click and click, nothing inside the board; it is in the
  abstract and in the opening paragraph from the paper-opening branch
  on, and in Highlights 5.4 by the Boss.
- Part 5 (the comparison and the failures by cause) is framed in the
  reverse direction: from the algebra to what the experiments lack;
  each FAIL a READING not yet made, a DECLARATION, a RULE the algebra
  has a place for and the law does not fill (the owner's "perhaps
  another physical force"), or NOTHING; the FAIL Rows Algebraist's file
  (branch fail-rows) the source, cited as pending until it merges; the
  paper claims no force it has not shown.

### The owner's seventh word (00:40Z): the definitions in the new order, and the names

The new Section 2 opens with the definitions in this order, each one
line of mathematics before its words: (1) the GameBoard, the cubic
lattice Z^3 of Nodes with six Ports each and one Link per interval; (2)
the group of order 24, the rotations of the cube acting on the six
Ports, inside the 48 signed permutations (Theorem 1; isomorphic to the
symmetric group S_4, which is not written "S_24": S_24 would name the
symmetric group on 24 letters, of order 24!, a different group); (3) the
cyclic group Z_N of the phase and its integer group ring Z[Z_N]; the
record as an element f = sum f_p x^p at a Node with a direction; (4) the
six operations, maps on the records (the law's step Inside); (5) the
click, the evaluation ev: Z[Z_N] -> Z[zeta] with its norm at a detector,
and the Outside: counts between clicks and ratios of counts, the only
things compared with nature. So the correct sentence is: the group of
order 24 is the symmetry of the GameBoard (what maps its directions to
directions keeping opposites), not the GameBoard itself; the six
operations act Inside on the ring's elements; the Outside is not an
operation on the group but the read-out, the click and its counts.
The words of the world, kept as the paper uses them: "exact" for an
identity of the algebra; "recovered in a limit" for a known law
re-obtained in a named limit (c = 1/sqrt 3, Born, Tsirelson, Young, the
inverse square and Poisson under a shell average); "reached under
hypotheses" for the chain to Lorentz's factors, the equivalence
principle, Einstein's step and Newton (under (A1), (A3), (A2) as named);
"conjectured" for the bending's coefficient and the atom's ladder;
"compared" for Table 2's readings; "derived" nowhere for a law of
nature.

### The owner's eighth word (00:50Z): the paper is how the algebra and the physics connect; where the route goes

The great papers place the route in two places and nowhere else: a
paragraph of motivation in the Introduction (Dirac 1928, Yang and
Mills 1954, Gell-Mann 1961 all begin from the physics that called for
the mathematics, in a page), and a section of its own once the
mathematics and its consequences are on the table (Gell-Mann's closing
sections; Wigner's physical sections after the group). The reordered
paper follows that, and its five parts read as the two directions of
the connection: Part 1 the algebra; Part 2 the algebra to the physics
(what follows, the click-to-click algebra, the forms reached); Part 3
the GameBoard, the way the algebra is computed with; Part 4 the physics
to the algebra: "How the algebra was reached from the GameBoard" (the
route, the twenty-four dated steps, what did not converge and was not
put in); Part 5 the comparison with nature by kind and the failures by
cause. The Introduction carries the route in five lines and points to
Part 4; Part 4 comes after Part 3 because the GameBoard must be defined
before the paper says how it led to the group.

### The owner's ninth word (00:58Z): from the physics to the mathematics by the postulates, and back

Part 4 is written as a table, one row per postulate of the law, the
physical assumption on the left and the mathematical object it forces
on the right (the objects already in the paper; the table is new):
- P2, space a cubic array of Nodes with six Ports -> the lattice Z^3,
  the six directions, and their symmetries: the 48 signed permutations,
  their rotations the group of order 24 (Theorem 1);
- P5, one Link per interval; P4, a rule reads its own record and the
  six neighbours and keeps nothing at a Node -> the translation group's
  shift, the causal front (the octahedron), the Manhattan bound and the
  pace c = 1/sqrt 3 in the limit (Proposition 1);
- P1, every quantity a bounded integer; the phase on a bounded circle
  -> the cyclic group Z_N and the free Z-module of the rows; the amount
  an integer coefficient;
- messages that meet and add, opposite phases cancelling -> the group
  ring Z[Z_N] and its addition (the merge);
- P7, P8, the declared tables and the families as rows of integers ->
  the integer matrices (the split, the rotation) and the coupling
  matrix; the record of a pair in Z[Z_N] x Z^2 x Z^2;
- P3, the rates and walls made of the six operations; the bounded
  accumulator -> Eq. (1), the division with the remainder kept, the
  comparison that is the event;
- P6 and P11, a record read out once by one comparison, the GameBoard
  read in no other way; P10, one axiom of the apparatus -> the
  evaluation at the roots of unity with its norm, the click's weight the
  positive quadratic form (Theorem 4), and the Outside: counts between
  clicks and their ratios;
- P9, the flight blind to the phase and the crowd -> no dispersion, the
  constancy of c; a rule chosen among few, so named.
Then the way back, mathematics to physics, in the same table's last
column or a second table: what each object gives that is compared with
nature (the books and Gauss's law exact; c, Born, Tsirelson, Young, the
inverse square and Poisson recovered in limits; Lorentz's factors, the
equivalence principle, Einstein's step and Newton reached under (A1),
(A3), (A2); the CHSH value 181/64 and Table 2's rows), each with its
word. The two tables are the paper's two directions in one page.

### The owner's tenth word (01:05Z): the postulates get names, not only numbers

"P9" is not a name. In the new Section 2 every postulate keeps its
number and gets its name, used in the text from then on: P1 bounded
integers; P2 the cubic lattice (six Ports); P3 the six operations; P4
locality (a rule reads its own record and the six neighbours, nothing
kept at a Node); P5 one Link per interval; P6 one read-out (a record
read once by one comparison); P7 the declared tables; P8 the families
as integers; P9 the blind flight (a row in transit moves at its declared
rate whatever its phase and whatever the crowd; no dispersion); P10 the
click axiom (the click's weight the one positive quadratic form); P11
clicks only (the GameBoard read in no other way). The numbers stay for
the cross-references already in the paper and the ledger.

### The Boss's note (00:55Z): the group's definitions are the physicist's file

docs/GROUP_STRUCTURE.md (the physicist, branch group-structure, on the
owner's word: the four objects, the group of order 24, the 48; nothing
renamed) is the one definition; the reordered paper's Section 2 cites
it once it merges and writes no second definition of the group.

### The owner's go (2026-09-23 ~00:20Z his clock): the order is good; reorder the whole paper; the length

The owner: "Yes, this order is good, and reorder the whole paper with
the things we talked about; and say whether there is a way to shorten
it, perhaps to 24 pages, still including all our important things; if
not 24, then at least 48; and see how many pages Einstein and the
greatest submitted."

The lengths of the great papers, as printed: Einstein 1905 (special
relativity) 31 pages; Einstein 1905 (the light quantum) 17; Einstein
1916 (general relativity) 54; Heisenberg 1925, 15; Schroedinger 1926
(first communication) 16; Dirac 1928, 15; Wigner 1939, 56; Feynman
1948, 21; Yang and Mills 1954, 5; Gell-Mann 1962 (Phys. Rev.) 18; Bell
1964, 6. The foundational ones with a new mathematics (Einstein 1916,
Wigner 1939) are the long ones, about 55; the rest 5 to 31.

What the reordered paper can be, from the present 52 (42 of main text,
3 of declarations and references, 6 of appendices; about 34,000
words): (i) about 48 pages as one paper: the reordering, the cuts
already listed (2 to 3 pages), the reproduction appendix and the roads
table to a supplement (2 pages); every claim, number and row kept.
(ii) About 24 pages of main text with a supplement (a form Foundations
of Physics accepts as electronic supplementary material): the main
text keeps the algebra (4 pages), what follows with the theorems stated
and the proofs in the supplement (6), the GameBoard (3), the route (2),
the comparison with Table 2 compact (4), the discussion (3), references
(2); the supplement carries the proofs, the technical details, the
reproduction, the families and roads tables, the ledger's long rows and
the register's paragraphs. Nothing is lost; it moves. The generator can
emit both from one source. The recommendation: (i) for the submission
(the journal has no page limit and the paper's evidence is its
tables), (ii) ready if the editor asks for a short main text.

### The owner's word of record 1129 (the Boss's order of ~01:10Z): "The steps between two clicks", stated exactly

A numbered subsection at the head of Part 2 (before the click-to-click
algebra, which it introduces): the chain every comparison in the paper
walks, one line per step with its kind.
1. The birth of a record's rows at a declared source: a declaration
   (the family's row of integers, the world file's source and its rate
   [r, W]); the wheel reading u fixed here.
2. The flight: the six operations on Z[Z_N] and the lattice, the phase
   turning per Link, the split and the rotation by the declared tables,
   the merge in the ring; the law (P3, P4, P5, P9).
3. The arrival at a detector's Node and the click: the one measured
   event, the evaluation of the record at the roots of unity and the
   comparison (DETECTOR; P6, P10, P11).
4. The detector's own count between two clicks, read under the key
   clock_stamp (DETECTOR; outside this paper's law identity, named as
   such).
5. A ratio of two such counts, k_a(b), or a count itself (COMPUTATION
   on clicks; nothing of the board enters).
6. The identity the algebra states between the ratios, the form of
   nature compared with. The proposed sentence: "Step (6) is the only
   place where a formula meets a measurement: the click theorem gives
   the ratios' identity from the ring, Lorentz's factors under (A1) to
   (A3), Einstein's step and, in the limit under a shell average,
   Newton's form; a row of Table 2 compares the ratio of step (5) with
   that identity, and with nothing else."
And the closing line: anything read from the board itself (a tick, a
presence mean, a body's own record, a shell mean) is a GameBoard
diagnostic and enters no comparison (the central idea, record 1104).
Part 5's failures-by-cause table then names, for each FAIL row, which
of the six steps its earlier reading broke (WHAT_IS_MISSING.md's four
words, READING, DECLARATION, RULE, NOTHING, and its modes A to E; on
branch fail-rows, cited as pending until it merges). The owner's aim:
the FAIL rows are to be turned by runs whose steps the algebra confirms
to be exactly these six, and the paper must let a reader see the six
steps exactly.

### The owner's word (~00:00Z UTC): the abstract for a reader of quantum mechanics, through the discrete

The bridge is the postulate P1 (bounded integers; the phase on the
circle Z_N, the grain N declared, P7): an amplitude is an integer sum
of N-th roots of unity, the Born rule its square at the click under one
axiom of the apparatus (P10), and interference, the marginals and CHSH
are then exact rationals of N. A draft abstract at 250 words carries it
(scratchpad/abstract_draft_QM.txt); in the reordered paper the same
bridge opens the new Section 2 in one sentence after the definitions,
and the postulate P1 is named "bounded integers" beside its number.

### The physicist's six items for Section 2, "how the group was reached through physics" (record 1136; docs/GROUP_STRUCTURE.md, branch group-structure at e99a1afa, its section 3; cited, not rewritten)

The outline of the new Section 2's road back, in the physicist's order:
1. The operations came first as acts on the board (the flight one Link
   per interval, the collision, the step by an accumulator, the turn,
   the merge, the click), each then one of the six operations on a
   state vector (record 191).
2. The group is the answer to which maps preserve what the operations
   act on: a Node of six Ports and its Links, a cone of one Link per
   interval; the bijections of the Ports keeping opposites opposite are
   the 48 signed permutations, over the integers the only
   cone-preserving bijections; a boost is not Z-linear, so Lorentz is
   reached Outside from the clicks, not as a lattice symmetry.
3. The 48 first appeared in the code as the collision table's
   invariance (BEAM_LAW note 42): the invariance of one operation, then
   recognised as the symmetry of all.
4. The 24 came from the hand: spin and polarisation needed a
   pseudoscalar (record 128); det(g) splits the 48 into the 24 rotations
   keeping the hand and the 24 reflections.
5. The other objects the same way: the shifts the translation group,
   the turn modulo N the circle Z_N and the merge Z[Z_N], the collision
   a cyclic action; c not chosen but the flight operator's norm
   1/sqrt 3 (record 186).
6. What the group does back: a rule reading the local state must
   commute with the 48, so the admissible forms are forced (Theorem 3 of
   the Lorentz note: the only isotropic even reading of the momentum
   within the six operations is c p . p; "generic" in the three tests
   means this).
In one sentence, the physicist's: the operations did not deduce a
group; defined on a Node of six Ports, the 48 are everything that
preserves that Node and its cone, and requiring every rule to commute
with them chooses the admissible forms, the group of order 24 the part
under which the hand is kept too. Section 2 cites GROUP_STRUCTURE.md
for the definitions and writes no second one.

The abstract and the road back (the Boss's judgement, agreed): at 250
words the abstract holds the objects and the results; the road back is
the Introduction's five lines and Section 2's; no clause of it enters
the abstract, since every word there now carries something the owner
asked for (the object, the discrete phase, the Born bridge, the exact
results, the limits, Newton, Lorentz, Einstein, the central sentence,
the tally, the conjectures, the limitations).

### The owner's word (~00:15Z UTC): the system of information transfer

The paper's paragraph "The GameBoard as a system of information
transfer" (Section 2 now: the rows the only objects, a Link a channel
carrying one step of a row per interval each way, the six things an
interval does to messages, the books saying no message is lost or made
in transit, the lattice gases and Shannon's channel as the family it
belongs to) opens the definition of the GameBoard in the new Section 2,
moved whole: the GameBoard is defined as a system of information
transfer whose messages are the rows with their attributes, whose
channels are the Links, whose symmetry is the group of order 24 inside
the 48, and whose only read-out is the click. The algebra is then what
the messages are (elements of Z[Z_N]) and what the six operations do to
them; the owner's sentence, "in all, a system for transferring
information", closes that definition.

### The owner's word (~00:20Z UTC): "we see it as reality, but one can also see it as a system of information transfer with costs; define it correctly"

The definition proposed for the new Section 2 (the two readings of one
object): "Definition (The GameBoard). A system of information transfer
with costs. Its messages are the rows, each a tuple of bounded integers
(a Node, a direction, an age, a phase in Z_N, an emitter, a content per
unit, a record, a label, an amount, a multiplicity). Its channels are
the Links, each carrying at most one step of a message per interval in
each direction. Every step is paid: a message advances only by its own
accumulator, a rate against a wall (Eq. (1)), and turns its phase by
its declared turn per Link; a message is created only at a source that
pays its content (a release's cost, E = hf); a split and a rotation
re-emit it by declared integer tables; a merge adds messages that meet
and cancels opposite phases; nothing is kept at a Node beyond the
messages present (locality, P4); and the only reading is the click,
which consumes the message it reads and pays nothing back (the one
read-out, P6, P11). The books are the audit: at every interval released
equals in transit plus absorbed plus escaped plus cancelled. Read as
physics, the same objects are Nodes, Links and records and the costs
are contents and phases; read as a channel, they are Shannon's messages
and capacity with a budget per message, and the lattice gases' bits on
links with a phase and an amount added."

### The owner's words of record 1139 (the Boss's order of ~01:45Z): the click an action; locality and discreteness Outside

1. "The detector does not only read; when it reads it performs an
   action; that is what explains that a detector changes the outcome."
   In the subsection "The steps between two clicks", step (3) reads:
   "the arrival at a detector's Node and the click: the record ends
   there, its content enters the detector's own record and its count
   advances; the click is an action of the law on the state, not a
   passive read (P11)". The reading rule's paragraph (now "Only a
   detector's reading is a measurement") is reworded: "Only a
   detector's click is a measurement, and a click is an action of the
   law on the state: the one step that deletes Inside and the one row
   that Outside gains." The repository's rule wording is corrected the
   same way by the physicist (branch measurement-acts), so the paper
   and the law files say one thing; the paper cites it once it merges.
2. "Check whether one can say that above the board too there is
   locality and discreteness; whether it follows from all the things."
   It follows, and it is proved in the click frame; the plan states
   both as theorems beside P11, in Part 1 (after the definitions), one
   line each, "not an added assumption":
   - "Locality Outside (a theorem of (A1) with the definition of
     Outside; the click frame's section 0 and its closing theorem,
     DERIVATION.md lines 53 to 73 and 1452 to 1456): every Outside
     passage is a chain of clicks between neighbouring places, so
     Outside inherits Inside's locality through the map, one Node per
     interval of the tick, 1/r_D Nodes per the detector's own count;
     the one exception is the pair's gather, P6, the law's one
     non-local operation."
   - "Discreteness Outside (a theorem of the click's definition, M3):
     the counts form a free abelian monoid and their ratios lie in Q;
     every Outside quantity is an integer count or a ratio of counts;
     nothing continuous enters above the board."
   And the line between the theorem and the assumption, stated as what
   it is: "What is more than (A1) is not a theorem: that the apparatus
   is itself inside the law, that we are built of clicks (DERIVATION.md
   lines 74 to 92), is an assumption about the world, or a programme for
   the law; the paper marks it so."

### The owner's word of record 1141 (the Boss's order of ~02:30Z): the uncertainty relation and Bell by the click, "the one fact and its two faces"

One paragraph in the section on the click (P11), every claim the
derivation's (DERIVATIONS_BEAM section 22) or the entanglement page's
(docs/designs/click_frame/ENTANGLEMENT_PAGE.md), cited, none new; then
one citation each in the uncertainty row (row 10, A10) and the Bell row
(row 1a) with the click frame's section 10.
- The one fact: a record is read once; the click reads one cell of one
  record and ends it; the two results are that fact from two sides.
- The uncertainty relation: a record is a vector f in Z[Z_N]; its
  position the Node its rows ended at, its momentum the turn per Link
  |p| N / h (de Broglie as the declared turn); the click evaluates f at
  the N-th roots of unity, the discrete Fourier transform on Z_N, so
  position and phase are the two sides of one transform. Exact, no
  limit: the support bound |supp f| x |supp f^| >= N (checked by
  enumeration at N = 64: one phase gives all 64 roots, the antiphase
  pair 32, the comb of every eighth phase 8, the equality case) and the
  Weyl relation VU = omega UV, from which [x, p] = i hbar follows as
  N -> infinity with hbar = hN / 2 pi; Kennard's Delta x Delta p >=
  hbar / 2 as that limit; at finite N the entropic bound, the two
  entropies summing to at least log2 N ("bits read plus bits erased =
  log2 N per record"). What makes it an uncertainty and not a spread:
  the click reads one cell; read at a Node the record gives its
  position and its phase vector is erased; read on the fan's angle its
  momentum's direction and not the Node; not jointly readable because
  there is one read-out; the reading is what is uncertain, not the
  board (the detector acts, record 1139). The pin: w x FWHM(sin theta)
  / lambda = 0.886 far field, 0.92 +- 0.03 at the registered geometry
  (row 10).
- Entanglement: a lamp releases one record with two arms, the joint
  labels 00 and 11 of weight 1, psi = (00) + (11) in Z^2 (x) Z^2
  tensored with its phase in Z[Z_N], its coefficient matrix of rank 2,
  no u (x) v = psi: entangled by construction; in flight each arm
  local, nothing of one arm written on the other; a setting an integer
  rotation U_s with U_s^T U_s = n_s I; the pair's click one gather of
  the one record from both settings at the completion, J(o_A, o_B) =
  sum_l U_a[o_A][l] U_b[o_B][l], the cell's weight J^2, the birth wheel
  selecting one of four cells through the ladder; the rows local, the
  read-out not: the non-locality in one object, a record of rank 2 read
  by one gather at two clicks; no signal between the arms; E(a, b) =
  cos(2 pi (a - b) / N) within the rounding, the marginals exactly 1/2
  (no-signalling an identity of the integers), S = 2 sqrt 2 before
  rounding and 176/64 = 2.75 at N = 64 (row 1a, against Hensen 2015's
  2.42 +- 0.20), the plateau 181/64; Tsirelson's bound a theorem of the
  operator algebra on the labels; not a hidden-variable value because
  the pair's weight is one quadratic form with cross terms where a
  mixture is linear (Fine's theorem).
- What links them: the same one read-out per record makes the support
  bound an uncertainty and denies Bell a hidden joint distribution.
  Not proven, and said so (section 22.3): that Bell's excess is "the
  same Fourier fact" as the support bound.
The owner's question, whether these are the terms: the paper uses the
standard names as the things compared with, per record 817: the
support uncertainty principle on Z_N (Donoho and Stark), Kennard's
relation as its limit, the Weyl relation, the entropic uncertainty
bound, Tsirelson's bound, Fine's theorem; the model's own words (the
click, the record, the gather, the wheel) name the mechanism.

### The owner's approval (2026-09-23 ~00:35Z UTC)

After the check of the structure against Einstein 1916, Dirac 1928 and
Gell-Mann 1962 (the object; the physics from the mathematics; the
comparison with nature; the route in the introduction and, here, in a
section of its own; the failures table ours alone; the click-to-click
head ours alone): "This is the best structure, an excellent structure
for the paper; only make sure the others are built with this structure
too." And: "Okay, approved." The structure of the reordered paper is
the owner's decision; part 6 (the failures by cause) is the Boss's and
the algebraist's work, cited as pending.

### The Boss's word of 00:50Z: part 6's sources merged, and the runs' verdicts for the plan's honesty

WHAT_IS_MISSING.md is merged to main at c66de871
(docs/designs/fail_rows/WHAT_IS_MISSING.md, PR #964); Part 5/6 cites
it merged, its four words (READING, DECLARATION, RULE, NOTHING) and its
modes A to E, and counts its rows in three classes (the Boss's count to
the owner, record 1144): at most two rows turned by a click; three by
a declaration that puts the compared form in, counted apart from the
measured passes; the rest stay FAIL. The runs so far: row 8b run, the
row stays FAIL by the law's design of the path phase (the beat at
h/p = 4.65 Links read at a click for the first time; RUN_8BC.md on
fail-run-8bc, its PR opening); row 4a outside the identity's domain
under either drive (a factor 14.8); row 2a's comparison figure
verified at the abstract's level, 0.94 (Jacques et al. 2005), the
law's 0.966 above it, a bound met and not a number matched; row 13's
continuum coefficient read on the lattice only within the fan's comb
(10 to 20 percent), so "matches 1.75 in the limit" is not written.

### Addendum to step 1 (2026-09-23, the Boss's word of 01:05Z): two verdicts and the owner's decision on the weight pair

- Row 2a: an honest bound met under the paper's own caption criterion
  ("where the model's value lies above the apparatus-limited
  measurement (a bound met)", the criterion row 2b passes by): 0.966 in
  the clicks against the biprism's 0.94; two caveats in the cell (the
  figure at the abstract's level, the body unread; the central fringe's
  visibility against the pattern's). The verdict word: "BOUND MET (a
  bound, not a match)" in the reordered paper, with the caveats; NOT
  COMPARED only if the body is required, and the plan does not require
  it since 2b passes by the same criterion (RUN_13_2A, the reviewer's
  gate of 00:44Z).
- Row 13 under gamma_PPN = 1: the coefficient 2(1 + gamma_PPN) is a
  declared input equal to nature's, read within the fan's comb (the
  mean over rings within 9 percent, single rings up to 23 percent off),
  never within the grain; not a pass against nature, the coefficient
  being the input; the law's own row, 0.000, FAIL (series K).
- Row 8b's run merged (RUN_8BC.md, PR #975, 907f339d): FAIL by the
  law's design of the path phase, the beat h/p = 4.65 Links read at a
  click; its step 3 (the re-emitter world) ordered, pins first.
- The owner's decision on the weight pair (record 1150, B): the paper
  states the weight rule once, as a declaration by gamma_PPN; rows 13
  and 14 read "under the declaration"; no per-test choice, and the
  options A, B, C are not in the paper.

## Applied (2026-09-23, the Boss's order of 01:05Z, step 2, commit 1): the reordering into the six heads, nothing cut, nothing rewritten beyond the joins

The generator gained one step, `cut30/reorder.py`, applied after the
corrections: every block is matched exactly once by its heading or
label, cut whole and placed whole; the tests hold each block verbatim
and once in main.tex, every label defined once, every reference
resolved, and every moved reference in its new place.

The order now (the owner's approval of the six heads):

1. Introduction: as before, less "The words of this paper" (to
   Section 2) and "How the simulator led to the results" (to Section
   6); in the latter's place one pointer paragraph, "Where the object
   came from", to Sections 6 and 5.
2. The algebra: the group, the ring and the families (`sec:algebra`):
   the opening join; "The words of this paper"; "The six Ports, the
   group and the front" with Theorem 1 and its proof reference (from
   the geometry section); "The objects" (from the quadratic form's
   part); Definitions 1 to 3 (row and record, the update rules, the
   click), the host's layer paragraph, Lemma 1 and the "three things
   put in" paragraph (from the measurement section); the families'
   sentences of the law section's first paragraph under the new
   heading "The families as declared integers" (its "(Appendix D)"
   now "(below)"); the families table, Table 1, brought forward whole
   from Appendix D.
3. From click to click (`sec:click`): the opening join; "Inside and
   Outside, and how a click arrives at Lorentz"; "The step beneath and
   the step above", "The smallest thing above", "Newton from the small
   step"; "From an Inside formula to an Outside formula, family by
   family" with the conversion table (Table 2) and "What the Inside
   step gives Outside that the continuum cannot state"; "The limits,
   and what does not return" with Eq. W (all from the discussion).
4. From the algebra, the physics (`sec:physics`): the opening join;
   "What is proved" (from the discussion); then, demoted to
   subsections with their labels, 4.1 Geometry and symmetries (with a
   pointer to Theorem 1), 4.2 Conservation, the flux and the forces,
   4.3 The delay field, 4.4 Measurement and the quadratic form (with a
   pointer to Definitions 1 to 3 and, where "The objects" stood, to
   Section 2), 4.5 Bell and CHSH.
5. The GameBoard: the way the algebra is computed with
   (`sec:gameboard`): the opening join; 5.1 The law and its
   implementation (the whole law section, its first paragraph "The
   GameBoard as a system of information transfer" kept, the road
   paragraph and the families' sentences out of it; "The code
   implements the law" from the checks section placed before "When the
   transition was made" and the forcing ledger, Table 3).
6. How the algebra was reached: from the GameBoard to the group
   (`sec:route`): the opening join; "How the simulator led to the
   results"; "The road from the cells to the algebra"; "The transition
   from ordinary physics to modern algebra, dated" (from Appendix C);
   "The platform" and "The road to each" (from the discussion).
7. The comparison with nature, and the failures by cause
   (`sec:comparison`): the opening join; 7.1 The simulator's checks and
   the comparison with nature (`sec:checks`, less the code paragraph;
   the confrontation register Table 4); 7.2 Discussion and conclusions
   (`sec:discussion`: a pointer line, then "What the law names and has
   not computed").
Declarations, references, Appendices A to C as before (C less the dated
paragraph); Appendix D now "The check of the roads" (its label kept,
the roads table).

The joins, all the new text: seven section headings and their opening
sentences (one to three each), five pointer lines, one paragraph
heading. Fifteen cross-references whose targets moved follow them
(`reorder.REFS`): nine that pointed at the discussion (the click
theorem, the second-order W, the lattice's corrections, the detector in
motion, the bending under the key, the hypotheses on the tree, the
platform, the tally, the centred step) now point at Sections 3, 4 or
"below"; five that pointed at the measurement section for the
definitions' objects (n/d, the rungs, the rotation matrix, the ladder's
K, the tables' zeros) now point at Section 2; the ledger's row on the
group points at Section 2. No sentence of physics, number or verdict
changed. 53 pages (NUMBERS.md). Not in this commit: the six operations
as maps (commit 2), the route chapter's tables and the postulates'
names (3), the click subsections (4), the failures-by-cause table (5),
the cuts and the length (the owner's word).

## Applied (2026-09-23, the Boss's order of 01:05Z, step 2, commit 2): the six operations as maps on Z[Z_N] in symbols, and the definitions in order with the names

Two passages, both in Section 2, through corrections:

- "The definitions, in order." at the head of Section 2, before "The
  words of this paper" (the reorder's first block now starts at this
  heading): five items, each one line of mathematics before its words,
  the owner's seventh word. (1) The GameBoard: Z^3, the six Ports P
  with the involution e -> -e, one Link per interval. (2) The group of
  order 24: G_48 the bijections of P with g(-e) = -g(e), the 48 signed
  permutations; det a homomorphism onto {+1, -1}; G_24 = ker det, the
  rotations, index 2, "the group of order 24, the name used
  throughout"; the isomorphism to the symmetric group is stated in
  Theorem 1 alone, the list points to it and does not repeat S_4 (the
  proof in Appendix A restates it as the proof must). The hand h ->
  det(g) h tells the cosets. (3) Z_N = Z/NZ and Z[Z_N] = {sum f_p x^p},
  the addition by components, x^p x^q = x^{p+q}; the record's rows one
  element (the objects; Definition 1). (4) The six operations as maps,
  one symbol each, (T) (B) (G) (P) (E) (D). (5) The click, ev(f) with
  its norm, the one read-out (Definition 3); the Outside, the counts
  between clicks and their ratios (Section 3).
- "The six operations as maps, in symbols." between Definition 2 (the
  update rules) and Definition 3 (the click), about a page, the
  statements of docs/ALGEBRA.md chapter 2 on algebra-one at 93033d54
  (the mathematics reader's sound chapter), condensed, with the letters
  of the derivation record: (T) s -> s + r, the closed form floor(s_0 +
  rt), the flight's m_D(tau) and tau_k, the phase's turn, the
  translation group of the box; (B) u^T C v, the push, the split and
  the rotation, the click's weight f^T G f with G = E^T E; (G) f + g
  in Z[Z_N], the cancel as the quotient by (x^{N/2} + 1), Z[zeta_N] for
  N a power of two, the pair's product; (P) the collision, the gate,
  the apportioning's tie, never of contents; (E) ev a surjective ring
  homomorphism with kernel (x^{N/2} + 1), the first isomorphism theorem
  exact, a *-homomorphism carrying f*f to |ev f|^2; the built tables
  E a Z-linear map to Z^2, not a ring homomorphism (the two pointers
  at N = 64, COMPUTATION, NUMBERS.md), the exact map the algebra and
  the tables the declared rounding (P7); (D) the signed truncating
  division with the remainder kept, the Euclidean division on an
  unsigned count, the comparison part of the map (the ladder's cell,
  a key, a window, a threshold). The closing lines: the order of the
  six at one interval, Eq. (1) their composition; what is not one of
  the six (a run-time root: the pair under the key optical, a later
  rule; Lorentz's factor on a body's own counter; a rounded constant
  beyond the tables at load; a float, a true division, a draw). The
  meeting's norm under its key, in ALGEBRA.md's list, is not named:
  the paper names no meeting rule.
- The letters (T) (B) (G) (P) (E) (D) are new to the paper; the
  Introduction's list of the six in words and "The map" paragraph's
  numbered list stay as they are (the cuts are the owner's word).
- Straight double quotes in the two passages were replaced by TeX's
  quote pairs after the first read-back showed a wrong opening mark.
- The maps paragraph cites the algebra document (a new reference,
  docs/ALGEBRA.md on the branch algebra-one at 93033d54, its merge
  pending at submission) beside the derivation record.
54 pages (NUMBERS.md). The mathematician's check of the two passages
follows, per the Boss's order.

## Applied (2026-09-23, the Boss's order of 01:05Z, step 2, commit 3): the route chapter gathered with the postulate table and the two-direction table; the postulates named beside their numbers

- Section 2, after the definitions list: "The postulates, by name",
  the owner's tenth word: P1 bounded integers; P2 the cubic lattice,
  six Ports; P3 the six operations; P4 locality; P5 one Link per
  interval; P6 one read-out; P7 the declared tables; P8 the families as
  integers; P9 the blind flight; P10 the click axiom; P11 clicks only.
  The numbers stay where the paper already cites them (the law
  section states each; the ledger and the text cite by number); the
  names are used beside the numbers in the new tables.
- Section 6 opens with the two directions as two tables, the owner's
  ninth word: Table 4, "From the physics to the mathematics", one row
  per postulate (P2; P5 with P4; P1; P3 the merge; P7 with P8; P3 the
  accumulator; P6 with P11 and P10; P9), the physical assumption and
  the object it forces (the lattice and the group of order 24; the
  translation group's shift, the causal front, the Manhattan bound,
  the pace; Z_N and the free Z-module; Z[Z_N] and (G); the integer
  matrices and (B), the pair's record; Eq. (1) with (T) and (D); (E),
  Theorem 4 and the Outside; no dispersion, a rule chosen among few).
  Table 5, "From the mathematics back to the physics", nine rows, the
  object, what it gives, the word: the books and the walk (exact); the
  Ports and the group (exact; c recovered in the limit of the grain);
  Z[Z_N] and ev (Born's form and the counts exact; the rule and Young's
  spacing recovered in a limit); the pair's record (the rational exact;
  Tsirelson recovered in a limit); the push under a shell average
  (recovered in a limit under a shell average); the step rule (exact;
  the third law to the apportioning's grain); the clicks under the
  named hypotheses, in the opening paragraph's words (reached under
  named hypotheses); the flow per Euclidean Link and the closure
  congruence (conjectured); the detector's counts (compared). Every
  word is the ledger's ground word for that row.
- Then "From the operations to the group", the physicist's six items
  of GROUP_STRUCTURE.md section 3 in one paragraph, cited at its merge
  on main (7739bbbe, a new reference), the paper writing no second
  definition; then the road as it was recorded (the five blocks of
  commit 1, unchanged).
- The Introduction's pointer "Where the object came from" is now the
  five lines of the owner's fifth word: the object not chosen first;
  the simulator's assumptions; the rules turned out to be six maps on
  one ring and the maps preserving a Node and its cone the 48; what did
  not converge was not put in; the road is Section 6.
- The route section's opening join says the two tables come first.
56 pages, 90 references (NUMBERS.md).

## Applied (2026-09-23, the Boss's order of 01:05Z, step 2, commit 4): the click subsections

Section 3 (from click to click) opens with three passages, through
corrections (the chain's cut now starts at the first heading):
- "The steps between two clicks", the owner's record 1129 stated
  exactly: six numbered steps, each with its kind; step (3) the click
  an action of the law in POSTULATES.md section 10's wording at
  536edefb (the record ends at the detector, its content moves into
  the detector's own record, the click stamped with the detector's own
  count, the flight of every other row untouched, no back-action),
  cited at the postulates file's existing reference; the closing lines
  (step (6) the only place a formula meets a measurement; anything read
  from the board a diagnostic; the failures named by the step their
  reading broke, Section 7).
- "Locality and discreteness Outside, two theorems beside P11":
  Theorem 2 (Locality Outside) and Theorem 3 (Discreteness Outside),
  the plan's one-line statements written out from ALGEBRA.md 3.4 (the
  click frame's section 0 and closing theorem; Einstein Outside's
  Theorem 3, both cited); the line after them that what is more than
  (A1), the apparatus itself inside the law, is an assumption or a
  programme, marked so and not used. The later theorems renumber
  (NUMBERS.md); every citation by \ref.
- "The one fact and its two faces", the owner's record 1141: the one
  read-out; the first face the uncertainty relation (the support bound
  with its equality cases at N = 64, Weyl's relation, Kennard's form as
  the limit, the entropic bound as the click's identity; the
  identification of the circle as position kept as the hypothesis the
  measurement section names); the second face the pair (the record of
  rank 2, entangled by construction, the arms local, the one gather,
  E(a, b), the marginals, S at N = 64 and on the plateau, Tsirelson's
  bound, Fine's theorem); what links them; "not proven, and said so"
  (the derivation's 22.3). The standard names are the things compared
  with. Fine 1982 a new reference.
- The reading rule's paragraph (Introduction) reworded as record 1139
  says: "Only a detector's click is a measurement, and a click is an
  action of the law on the state, the one step that deletes Inside and
  the one row that Outside gains".
- Row 1a's cell and the uncertainty paragraph of Section 4.4 each cite
  the click frame's section 10 and point to the one fact. The plan's
  "row 10" (the uncertainty row of the register) is not a row of the
  paper's table, so the citation went to the paragraph that carries the
  reading.
- The assembler's citation regex now accepts an optional argument, so
  \cite[section 10]{postulates} keeps its entry (the first build dropped
  it and the PDF showed an undefined citation, caught on the read-back;
  a second, duplicate entry of my own was then removed in favour of the
  existing one).
58 pages, 92 references (NUMBERS.md).

## Applied (2026-09-23, the Boss's order of 01:05Z, step 2, commit 5): the failures by cause, in three classes; the runs' verdicts as merged only

- Section 7.1 gains, after "The prediction, and the failures", the
  paragraph "The failures by cause" and Table 7: every row of the
  register's table and the four pinned rows in three classes (the
  measured passes and the bounds; the passes under a declaration
  named, counted apart; the failures, each with its cause), the cause
  in the algebra's words (WHAT_IS_MISSING.md's four words READING,
  DECLARATION, RULE, NOTHING, and its modes A to G, cited at its merge
  c66de871), and the step of Section 3 the earlier reading broke
  (modes A and C step (4), B, D and E step (3), F and G step (1); a
  rule absent at the step where it would act). The honest count in the
  paragraph: three measured passes and three bounds; four under a
  declaration named (4b, 4a, 13, 8c); eleven FAIL with their cause,
  eight in the table and three by their pins.
- The runs' verdicts as merged only: RUN_4AB.md at 0a7b5db2 (PR #977,
  merged 01:15Z) for rows 4b and 4a; RUN_8BC.md at 907f339d for rows
  8b and 8c; three new references. No pin moved; no verdict of the
  law's row changed: 4b, 8b, 13, 14 stay FAIL as the law's.
- Row 2a's verdict word: "BOUND MET (a bound, not a match)", the
  Boss's word of 01:05Z under the caption's own criterion (a visibility
  above the apparatus-limited measurement, the one row 2b passes by),
  with the two caveats (the biprism's figure read at its source's
  abstract, the body unread; a central fringe's visibility against the
  pattern's) and the Mach-Zehnder numbers kept. The file RUN_13_2A is
  not on main; the ground is the Boss's word and the caption's
  criterion, as reported. The tally follows in its four places (the
  abstract, unchanged at 249 words; the caption; Section 4's "What is
  proved"; the checks' paragraph) and 2a leaves the FAIL list of "The
  prediction, and the failures".
- Row 13's cell: under the declaration gamma_PPN = 1 the coefficient
  a declared input equal to nature's, read within the fan's comb and
  never within the grain, a pass in form and not a pass against
  nature; row 14's cell "read under the declaration of the weight
  rule". The weight rule stated once, in the paragraph: the pair
  declared as gamma_PPN > 0's rule, at gamma_PPN = 0 a body weighs M
  (the owner's decision B, record 1150, cited at the log); the options
  A, B, C are not in the paper.
- Row 4b's cell cites the merged run (the click read over the
  detector's own count; the two one-way factors read on the k-ladder);
  row 8b's cell carries the merged run's verdict (FAIL by the law's
  design of the path phase, the beat 4.65 Links read at a click for
  the first time).
61 pages, 95 references (NUMBERS.md). Step 2's five commits are done;
not touched: the cuts and the length (the owner's word). The
physics-rule reviewer's full read follows, per the Boss's order.

## Applied (2026-09-23, the owner's GO of record 1166 and his three kinds of record 1173, through the Boss's orders of 02:0xZ to 02:5xZ, read after commit 5 had gone out): commit 6, the one table with three statuses; the mathematics reader's six lines; the algebra document at its merge

- Commit 5's "The failures by cause" paragraph and Table 7 are
  withdrawn (one correction replaces that block), so nothing is written
  twice: Part 7 has the one table, the register's every row (the six
  pinned rows 4a, 5b, 10, 11a, 11b, 11c brought in with the law's own
  number by kind and their sources), and a status column of three
  values: agrees (a bound met marked so), disagrees with the number,
  not predicted by construction with the missing piece and its kind
  ((1) the instrument missing in the model, (2) nature's number a bound
  or a fitted parameter, (3) no click definition yet), a row carrying
  two kinds where it does (3: 1 and 2; 11a: 1 and 3; 11c: 1 and 2).
  Four rows keep their words: 12 history, 2c not compared, 10 not yet,
  11b a pin. The form can take a "beside" row (the same claim, two rows,
  one status each); none added.
- The placement, record 1166 with the Boss's 02:5xZ: agrees 1a, 2b, 9,
  and 5a, 7a as bounds met; disagrees 1b (a control, the note kept),
  1c, 6, 7b, 8a (the crowd's history named beside for a width), 8b (the
  registered 16 and 0 behind; the declaration's 0, 0, 1013 of 1013;
  beside it the re-emitter reading of RUN_8BC section 6.3, merged at
  f852e50d, 1.000 exactly, 16 and 16, 683 of 705, an arrangement of the
  law and not a pass against nature; the merge SHA written directly
  since the merge landed, no "PR" in the text), 13 (0.000 pixel
  against 1.75 arcseconds; the gamma_PPN = 1 reading beside it as a
  declared input, kind (3) for the ring's position), 14 its present
  word (FAIL as read, pending its run); not predicted 2a (kind 2, the
  declared fan width; NOT COMPARED against a two-slit source until the
  figure is verified; 0.966 printed), 3 (kinds 1 and 2), 4a and 4b
  (kind 1, the identity's readings beside as a declared hypothesis),
  5b (kind 1), 8c (kind 2), 11a (kinds 1 and 3), 11c (kinds 1 and 2).
- Before the table: the comparison paragraph rewritten for the three
  statuses (the earlier verdict words PASS, FAIL, BOUND gone from the
  paragraph, kept in the four rows that keep their words), and the
  new paragraph "The limitations, stated before the comparison": the
  third status from the structure (no relativistic dynamics, r = 1 and
  no contraction; no term of the crowd's history; a declared input not
  a prediction), the referee's test (a row sits in the same class had
  it agreed), the weight rule once (record 1150, decision B), and the
  count sentence. The count sentence replaces the tally in its four
  places (the caption, Section 4's "What is proved", the checks'
  paragraph, the abstract at 249 words); the prediction paragraph's
  list is in the three statuses' words.
- The mathematics reader's six lines on commit 2, folded: zeta_N and
  Z[zeta_N] named at their first use in the definitions list; S_1 and
  N_l named in (T); bold f the coordinate vector of f on the basis x^p;
  the two closing quotation marks (they had not closed in the pushed
  text); the two run-time roots of ALGEBRA.md 2.7 named (the meeting's
  norm under its key and the pushed row's pair under the key optical);
  \bibitem{algebra} at the merge of algebra-one on main, 863cf5fd,
  "pending" dropped.
- The status column's header "Status" and the law column "The law's
  reading, by kind"; the moved caption reference in reorder.REFS
  follows the new caption text.
61 pages, 100 references, the abstract 249 words (NUMBERS.md). Length
48 still the target, no cut taken (the owner's word). The physics-rule
reviewer's full read of the whole head follows on the Boss's order.

## Applied (2026-09-23, the Boss's order of 03:1xZ, read after commit 6): commit 7, 1b a control and not counted

The Boss's placement of record 1166 with his word of 03:1xZ matches
commit 6 in every row but one: 1b, the phase-form window, is a control
and not counted (Bell's bound a theorem of every local read-out; the
law's answer to nature row 1a). Its status cell says so; the count in
its four places and the abstract reads twelve observables predicted,
five agree, seven disagree (1c, 6, 7b, 8a, 8b, 13, 14 as read), eight
not predicted, with "1b a control, not counted" beside the four rows
that keep their words; the old tally's remainder ("one is not compared
(2c)") that had trailed the count in three places is folded into it;
the prediction paragraph and the comparison paragraph name 1b the
control. 8c "not predicted, kind (2)" as the Boss settled it, already
so in commit 6. 61 pages, 100 references, the abstract 249 words.

## Applied (2026-09-23, the Boss's order of 03:5xZ): commit 8, row 14 not yet read against nature; the count of eleven; the fan's comb

- Row 14's status cell "not yet read against nature", the physics-rule
  reviewer's ruling on RUN_14's step 2: the conditional pins were the
  law's shell-mean form on an input no click read, the run refuted that
  premise and not a number of the law as built, and nature's period was
  not compared (the D3 2.00 +- 0.18 a host-tick period); the cell prints
  the law's numbers (1.677 and 1.512, COMPUTATION on the host's tick of
  unclosed loops) and the reviewer's sentence (the rung confirmed by the
  control, 979 then 980; the conditional pins FAIL on this fan by the
  comb, 2.5 to 4 times; nature's period not compared); RUN_14 cited at
  the branch head f30f2b0a, the merge SHA to be swapped at the
  reviewer's full read.
- The count in its four places and the abstract: eleven observables
  predicted (twelve once row 14 is read), five agree, six disagree (1c,
  6, 7b, 8a, 8b, 13), eight not predicted, five rows keep their words
  (12, 2c, 10, 11b, 14), 1b a control not counted; the prediction and
  comparison paragraphs follow.
- One sentence in the limitations paragraph, the reviewer's principle
  under rows 6, 10, 13 and 14, stated as the register's finding (the
  owner's Highlights line pending): a fan bounded in Manhattan length is
  not a fan of every direction; the isotropic mean holds only where the
  fan is declared uniform in angle at a grain finer than the reading or
  where a click read the crowd; otherwise the law's own number is the
  integral on the comb.
Nothing else moved. 61 pages, 101 references, the abstract 249 words.

## Applied (2026-09-23, the physics-rule reviewer's full read of the head 286993c4, through the Boss's order of 02:29Z): commit 9, the five MUST lines and the SHOULD lines (a) to (e)

- MUST (i): rows 3, 4b and 12 and the platform paragraph of Section 6
  no longer say the time base is the host's interval with the
  detector's clock not read; they say, in the reviewer's words, that
  the count is read at head in the detector's own clock (its count of
  self-creations under the age wall, r = 1.0000, no crowd at the
  detector, CRITERIA.md's re-run), equal to the host's interval to the
  integer, DETECTOR, the registered run's time base superseded, a
  two-way light clock at the detector reading the same count in no
  crowd (series X); row 12's clause is the ratio of the two records'
  rates over the same intervals, in which the interval cancels; the
  status cells of 3 and 4b read "(DETECTOR, the detector's own clock)".
- MUST (ii): row 8a's bracket says a width would need a decay fired by
  a met row of a declared bath (the fail-rows file's 1.8), none of the
  three pieces, the lattice-clock width a diagnostic beside it; row
  13's bracket says the ring's shift and the ratio read the declared
  gamma_PPN back (DETECTOR readings of a declared input).
- MUST (iii): row 2a's cause is the kind audit's: the fan's grain at
  most 0.004 of the 0.034 shortfall on finer fans, the residual in the
  record's phases at the click; the status the register's, pending the
  owner's word on whether a fan width that does not set the number is
  a declared input; KIND_AUDIT.md cited at the branch head 568c4e4d,
  its merge pending.
- MUST (iv): one word per row outside the table: the conversion
  table's row 4b "not predicted, Table 6" and series S "inside its
  pins in its domain"; paragraph (vii) "G2, inside its pin; row 3, not
  predicted, the crowd's history missing" and "row 11a, not
  predicted"; FAIL and MET kept only where a row's status is disagrees
  or a pin's own verdict is meant.
- MUST (v): the weight pair's gamma_L and gamma_PPN named; the walk's
  invariant's omega and kappa named at their first use (the step
  beneath); row 14's omega squared named the angular rate squared; the
  Sorkin parameter written kappa_S in its three places.
- SHOULD (a) to (e): row 4a's become line "a body's own record,
  DETECTOR; its interval GAMEBOARD"; row 8b's re-emitter counts "16 of
  1024 and 16 of 1007"; the caption says the count is repeated in the
  abstract (not "verbatim"); row 12's history clause once (the
  caption's), dropped from "The paper in one page" and "What is
  proved"; the appendix's second "Use of AI tools" paragraph with its
  placeholder removed, the declaration's kept (the reorder's dated
  block now ends at the appendix heading).
- NOT now, the owner's word: row 7a's move to not predicted and 2a's
  move to NOT COMPARED; the count sentence stands in its five places.
  Held as a prepared change, not applied.
62 pages, 102 references, the abstract 249 words.

## Applied (2026-09-23, the owner's word "what the Boss says about the moves in the table"): commit 10, row 7a not predicted and row 2a NOT COMPARED

- Row 7a's status: not predicted, the model's own number a declared
  input (the limitations paragraph's third clause): the give once per
  body is an integer of the family table, so the mass read 3673 against
  the declared 3677 reads that input back; nature's 4.35 units a bound
  on the input, not a prediction. The kinds' sentence in the count
  gains a fourth clause for it, "the model's own number a declared
  input".
- Row 2a's status: NOT COMPARED, as it is, a kept word beside 2c:
  nature's two-slit figure unverified, so no comparison stands until
  it is; the law's 0.966 printed with the kind audit's grain bound; the
  fan's width and the slits' grain declared inputs; once the figure is
  verified, bound against bound.
- The count in its four places and the abstract: ten observables
  predicted (eleven once row 14 is read), four agree (5a as a bound
  met), six disagree, eight not predicted (3, 4a, 4b, 5b, 7a, 8c, 11a,
  11c), six rows keep their words (12, 2c, 2a, 10, 11b, 14), 1b a
  control; the comparison and prediction paragraphs follow.
62 pages, 102 references, the abstract 249 words. The owner also asked
that the table be checked against the conventions of papers; the
check's findings go to him and to the Boss, not applied here (they are
the owner's and the Boss's to decide): the table's length (eight pages,
cells of prose), the status column's mixed vocabulary, the internal
kinds as jargon, and the citations of unmerged branches.

## Applied (2026-09-23, the Boss's order of 02:40Z, the owner's "go for it", record 1204, read after commit 10): commit 11, the two placements in the Boss's wording

Commit 10 had applied the owner's word as I read it from him directly;
the Boss's order with the exact wording arrived after it. Commit 11
aligns: row 7a "not predicted: the give per nucleon a declared input
read back (record 106); the escaped 4 of 3677 (DETECTOR) brackets
nature's 4.35 between the whole gives 4 and 5; the missing piece a rule
that derives the binding", the law's number kept; row 2a "NOT COMPARED
until the two-slit source is verified; the law's number 0.966 a
prediction under every fan (the grain's share at most 12 percent of the
shortfall, the kind audit's section 3); a bound met against the
biprism's 0.94 at the abstract's level; against the Mach-Zehnder's 0.98
another geometry", no kind bracket; the count in its four places and the
comparison paragraph carry "2a NOT COMPARED until its source is
verified"; the structure line on declared inputs names 7a's give, 8c's
content and 13's gamma; one sentence in the limitations paragraph says
the two placements are the owner's word of 2026-09-23 after the kind
audit, nothing else moved. The abstract's short form unchanged from
commit 10 (ten predicted, four agree, six disagree, eight not
predicted), 249 words. 62 pages, 102 references.

## Applied (2026-09-23, the Boss's order of 02:53Z on the owner's word of record 1207, the six findings on the table against the conventions of papers): commit 12 on the branch paper-summary-table, off paper-algebra-first's head 4c4cd42d

- Part 7 gets the comparison in one page: Table 6 "The comparison with
  nature in one page", one line per observable in the count (eighteen
  rows: four agree, six disagree, eight not predicted), the columns
  observable; nature's value with its source, "unverified" where the
  register has not checked the figure against the source (twelve
  rows); the law's own value with its kind; the distance in units of
  the source's standard uncertainty where one is stated (1a, 3, 11a;
  a factor where the number is a factor, 7b and 4a; a dash with the
  table's note otherwise); the status in one vocabulary. Table 7 "The
  rows that keep their earlier words" beneath it (1b a control, 2a and
  2c NOT COMPARED, 10 NOT YET, 11b a pin, 12 history, 14 not yet read
  against nature); the register's rows 1d and 4c the Boss named are not
  in docs/NATURE.md on main, so no line for them.
- The full record (the former Table 6, now Table 8) becomes Appendix D,
  "The confrontation register, the full record", unchanged in content,
  its caption with a one-line legend of the kinds; the reorder module
  moves it (move_register_table) and the generator's test holds the
  order (the summary in Part 7, the full record after its appendix
  heading). The check of the roads is Appendix E. About two pages
  moved, none cut; the count sentence unchanged in its five places.
- The reviewer's open SHOULD: the full record's caption names row 12's
  history clause once.
- At submission every citation of a branch head ("its merge pending":
  RUN_14 on fail-run-14, the kind audit on kind-audit, and any later
  one) is replaced by the archived record, one DOI, and none remains;
  the same for the commit SHAs of the live tree named in the
  references.
- Not in this commit: the three-levels paragraph (the owner's question,
  Einstein's four sources), which enters only on the owner's own go as
  a separate commit in the place proposed.
63 pages, 102 references, the abstract 249 words.

## Applied (2026-09-23, the owner's word "you need to shorten the paper, 48 pages"): commit 13 on paper-summary-table, the Supplementary Material

The owner's word lifts his earlier "not now" on the length; the form is
the one he approved on 01:40Z, the paper as one document with the
records a reader needs only to reproduce or to audit in a supplement.
The generator (cut30/supplement.py, called by assemble.build_all) cuts
six blocks whole from the reordered text and writes them as
supplement.tex, generated from the same source and held by the same
test: S1 the confrontation register's full record (Table S1); S2 the
check of the roads (Table S2); S3 the reproduction appendix's seven
confirmations; S4 the symbols table (Table S3); S5 the auxiliary
proofs of Theorems 1, 4 and 5; S6 the hand-worked update and "In the
code". The paper keeps a one-line pointer at each place and rewrites
its references to them (Table S1, Table S2, Table S3; S1 to S6 of the
Supplementary Material); the supplement resolves its references to the
paper's labels through xr-hyper (\externaldocument[main-]{main}, its
own references prefixed), has its own reference list, and is compiled
after the paper in the same directory. Nothing physical cut, every
claim, number and row kept; the paper 53 pages (63 before), the
supplement 13. The remaining five pages to 48 are commit 14: the
prose cuts of the owner's fifth word (about two to three pages) and,
for his word, two more pages from the ledger, the conversion table or
the families table moved to the supplement, none cut.

## Applied (2026-09-23, the owner's word "48 pages"): commit 14 on paper-summary-table, the prose cuts

The first part of the owner's fifth word (the repetitions), started on
my word as told to the Boss. Three repetitions cut, 408 words, nothing
physical and no claim: the one-page paragraph's first part, the list
of what is exact, recovered and not forced, which `What is proved'
(Section 4) carries in full, replaced by two sentences and a pointer;
the platform's list of series and detectors, which Table 2 carries,
replaced by one clause pointing there (the time-base sentence of rows
3, 4b and 12 kept whole); the prediction paragraph's list of the rows
that disagree and of the rows not predicted, which Table 6 carries
row by row, replaced by the pointer, the words on 1b and 14 kept.
The count sentence stands in every place it stood. The paper 53 pages
with nine lines on the last, so 52 full pages; the remaining four to
48 are the second part, for the Boss's or the owner's word: the
conversion table (Table 2, about two pages) to the supplement as S7,
and the ledger (Table 3) or the families table as the next, moved
whole, none cut.
