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

