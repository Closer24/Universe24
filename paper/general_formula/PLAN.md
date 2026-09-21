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
