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
