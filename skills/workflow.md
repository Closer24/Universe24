# Shared agent workflow

These skills implement the project roles requested in issue #16. They are
repository instructions, not a background service or a grant of permissions.
Read [AGENTS.md](../AGENTS.md) from the current checkout first. Explicit user
instructions take precedence; the postulates, definitions and feature procedure
remain the authoritative physical contracts. Skills route work without copying
or weakening those contracts.

## Repository knowledge and restart

Use [monorepo ownership](../docs/ARCHITECTURE.md#monorepo-ownership) and the
[restart guide](../docs/PROJECT_STATUS.md) to recover context without chat history.
Read only affected contracts and Skills after the root entry point. Use one
authoritative definition per concept; Skills link to laws rather than copy them.
Since 2026-09-17 the Highlights specification is `docs/HIGHLIGHTS.md`, edited
directly; the Google Doc is not edited or resynced, and the documents that
restate a Highlights rule are synchronized from that file after each change
([Boss project reference](boss-orchestrator/SKILL.md#project-reference)).
Since 2026-09-20, by the model owner's decision of that day
([record 87](../docs/LOG_2026-09-20.md#87-decided-the-trimming-pull-request-after-amplitude-v1-lands)),
Highlights 5.4 holds the decisions only, one line each; every record of a day is
appended to `docs/LOG_<date>.md` with the next number, and a decision line links to
its record. A record is written once and linked from everywhere else.

Keep durable procedures in Skills and architectural decisions in their responsible
documents. Put temporary task state, assignments, blocked checks and next actions
in Issues/PRs. For permitted publishing, persist the handoff there rather than only
in chat. If publishing is unavailable or unauthorized, report the unsaved handoff.
Do not claim personal Skills were installed merely because repository files exist.

## Critical reasoning for every substantive claim

Boss and every specialist must independently assess the user's substantive claims
and proposals rather than agree automatically. Understanding a proposal is not
evidence that it is correct; do not object merely to appear critical either.

- Identify assumptions and examine internal consistency, mathematical/physical
  validity and available evidence. Where relevant, check locality, bounded integer
  state/work, remainders, conservation and separate model costs from host costs
  against the responsible contracts, without inventing exceptions.
- Distinguish user-chosen postulates and requirements from established physics,
  hypotheses from conclusions, and target architecture from implemented/verified
  behavior. A hypothesis needs a test and pass condition; a verified result needs
  an identified source tree and completed evidence, not merely a passing detector.
- Explain concrete conflicts, counterexamples and uncertainty, and correct the
  agent's own earlier errors explicitly. Never silently change a user-defined law
  or architecture to remove a contradiction. Explain concerns to the user in
  Hebrew under the conversation rule; authored project documentation stays English.
- Match scrutiny to the stakes and current scope. Small confirmations do not
  automatically require extended research. Critical review does not authorize
  new experiments, edits, scope expansion or bypassing approval requirements.

## Physics comparison method

Use this method for an authorized investigation of how the discrete model matches
known physics. Start from a primary experimental result or a clearly labeled
analytic reference, with its regime, units, uncertainty and source. Free
propagation, configured interference and conservation can be analytic or
engineering checks; they are empirical comparisons only when compared with
sourced experimental data.

1. Define the measured Detector observable and causal readout before running.
   An internal state, audit quantity or rendered marker is not automatically
   that observable. Record the mapping from the reference experiment to chosen
   generic local laws, integer encoding, physical scales, preparation and initial/
   boundary conditions; distinguish supplied laws from predicted consequences.
2. Fix independent expected results, uncertainty/error metric, controls and
   acceptance conditions in advance. Identify calibrated parameters and their
   calibration data, then freeze them when testing other conditions. Do not
   retune against the validation result or redefine acceptance after a failure.
3. The physicist owns empirical targets, applicable regime and observable mapping.
   The mathematician derives invariants, integer/remainder bounds and validity
   domains, and checks proposed macroscopic or continuum inferences. The
   computational experimental physicist executes reproducible comparisons through
   the runner and reports actual data, errors and limits. Each role may reject
   a hypothesis; no role's approval replaces the others' evidence.
4. Separate exact mathematical preservation, code verification, agreement with
   an analytic physics benchmark and agreement with experiment. Report source/
   configuration identity, quantitative discrepancy, uncertainty and failure
   cases. Preserve contrary evidence and omitted interactions. Several matching
   cases do not prove the theory; discreteness alone supplies no prediction.
5. Assess finite-size, boundary, GameBoard-direction and encoding effects relevant
   to the claim. Sensitivity/convergence controls must represent the same physical
   case with fixed hypotheses. Do not assume that shrinking the GameBoard's Link
   or tick is a harmless numerical refinement; it may change the physical model.
   Input representation error is distinct from forbidden loss of core remainders.
6. For these user-requested research comparisons, produce and inspect the
   standalone HTML alongside quantitative records under the user's standing
   output requirement; label the visual projection and do not use appearance as
   acceptance evidence. Automated tests remain headless. Record unavailable
   output honestly rather than claiming visual inspection.

Keep the comparison bounded to the authorized question. This method defines how
to investigate, not permission for a new sweep, implementation or changed law.
Use the current execution lane and retain declared ownership and causal limits.

## Implement from a published design

Before implementing or changing behavior, read the authoritative written design
for that scope and cite its exact repository path and commit in the assignment,
implementation handoff and PR. Chat context alone is not an implementation spec.
The design must state ownership, input/output and private-state boundaries,
allowed rules, routing/timing, activation/no-op conditions, bounded arithmetic and
errors, and independent acceptance criteria. Keep topology/counts explicit and
separate from channel packaging. Use the responsible architecture document to
find the bounded implementation contract; do not copy physical laws into Skills.

Developers implement only agreed behavior and interfaces in that design. Route
missing decisions or contradictions to the architect/design owner before adding
behavior; the owner records the resolution in the authoritative document and
sends its revision to affected developers before they continue. Do not fill gaps
with a familiar physics law, old evaluator or convenient routing default. Routine
implementation choices already covered by the design and user authorization
continue without repeated permission. This workflow neither expands scope nor
authorizes a new law, experiment or merge.

Boss supplies the written revision when dispatching work. Architecture owns
contract reconciliation; developers map their changes to it; test owners retain
independent expected results and report deviations rather than changing the
contract to fit code. On a design revision, assess affected work/evidence and
update the handoff before further behavior changes. Preserve historical results
with their original scope instead of relabeling them as the revised design.

## Configuration tasks and implementation scope

Checking a configuration uses the existing simulator and validator. It does not
require changing simulator source, validation code, schemas or test expectations.
Keep the requested operation explicit:

| Request | Work and result |
| --- | --- |
| Check an existing configuration | Read the supplied files and explicit dependencies, use the existing preflight, and report validity or concrete errors; preserve inputs and code, and do not run a world |
| Create or correct a configuration | Edit the requested configuration data using supported definitions and existing authoring adapters, preserve the intended experiment, then validate the resulting input |
| Run an experiment | Validate the explicit input first, use the existing runner for the requested run, and inspect its results against the stated acceptance target |
| Implement or fix simulator software | Treat this as implementation work only when the user's scope includes it; follow the responsible code owner's development and regression workflow |

A data error belongs to configuration authoring. A check-only request returns the
error and a proposed correction without applying it. An invalid result can complete
a check-only task: success is an accurate report, not making every input pass.
Correct data when authoring
or correction is requested; reuse [external entity definitions](../docs/ENTITY_DEFINITIONS.md)
and explicit placements through the canonical loader. Keep the complete portable
input when exporting or handing it to a runner. Unsupported format or composition means a capability
gap. A suspected validator/engine defect needs a minimal reproduction, expected
versus actual behavior and an identified owner. Report these findings separately;
a failed check or unexpected physical result does not open an implementation task.

Do not make an input pass by weakening a schema, capacity, assertion or physical
acceptance condition, adding a hidden law, or switching to a historical model.
Do not silently alter the experiment to fit the implementation. A passing preflight
permits the requested run; it does not prove the proposed physical behavior.
Use existing implementation authorization only when it still covers the current
task; later restrictions take precedence. When implementation is within scope,
continue without asking for the same permission again. Otherwise, return the
finding for a separate implementation request rather than modifying code during
configuration work.

## Defect ownership and closure

When the user authorizes remediation, every confirmed defect, capability gap or
unmet acceptance target needs an active owner and a durable Issue/PR handoff.
Attach related findings to the existing objective; use a separate Issue only for
an independently completable objective. Keep the temporary defect list out of Skills.

- Record the violated contract, affected model and source revision, reproduction,
  expected versus actual result, responsible role, dependencies and closure check.
- Route software defects to the component developer; configuration defects to
  configuration authoring; missing numerical laws to physics and mathematics;
  incompatible interfaces or ownership to architecture; display defects to the
  visualization owner; and long checks plus failure analysis to the test owner.
  Each implementation has one writer and an independent reviewer when required.
- A missing law is an open design task. The design owner specifies the unresolved
  operator, parameters, invariants and falsifiable acceptance before handing the
  published contract to a developer. Do not invent a physical law or substitute a
  different model to close a finding. Resolve routine implementation choices
  within existing authorization without repeatedly asking the user.
- The owner returns the correction and evidence, or a concrete blocker with the
  next responsible owner. Boss routes blockers onward; a report, task assignment,
  passing unrelated test or published branch is not a completed repair.
- Reproduce the original failure on the corrected source, check affected
  regressions and required review, and record the verified revision before
  closure. Preserve negative results and remaining physical limitations.

## Inputs and handoff

Give each owner a bounded task with the repository, base commit, candidate/model,
acceptance target and owned files. Include relevant earlier findings and the
current user's constraints. Use isolated branches/worktrees for concurrent edits;
one owner writes each shared interface until the coordinator reconciles changes.

Return a concise handoff with:

- status: pass, blocked or incomplete; distinguish code checks from physical acceptance;
- reviewed commit/tree, changed files, and any dependent branch;
- result and evidence: commands with outcomes, not-run checks, and relevant HTML/trace;
- violated or satisfied contract, remaining limitation, and next owner/action.

Generated run evidence, including previously retained failure traces, follows
the [24-hour retention policy](../docs/RETENTION.md). Record reproducible inputs
and concise acceptance results durably before registered output expires. Active
writer leases protect ongoing work; do not infer cleanup ownership from a folder
name or age. Use the cleanup watcher or a scheduled command when the UI and
runners are idle, and distinguish configured automation from verified execution.

Do not reuse a pass after its relevant inputs change without assessing the diff.
An unchanged tree can reuse its verified results; record that equality. Different
conversations do not synchronize automatically. Read current GitHub state before
integrating their work, and never overwrite unrelated edits.

## Publish corrections and share revisions

For requested maintained changes, each specialist owns Git publication as part
of the assignment. Promptly commit coherent corrections on the isolated task
branch and push or update the linked PR under the standing authorization. Keep
the PR draft while required validation or review is incomplete, and state what
remains. Publication shares work; it does not waive merge gates. This procedure
does not promote a research-only experiment into maintained code.

- If the specialist cannot publish, explicitly hand the exact local commit,
  owned files, base, dependencies and validation state to a named Git publishing
  owner. Boss assigns that owner and follows through; a local commit or an
  unaccepted handoff is not published work.
- The publishing owner reads back the remote branch head and changed content.
  Boss records the canonical Issue/PR, branch and verified remote SHA with the
  dependencies and review state, and notifies affected active agents whenever
  a correction or revised dependency is published or merged.
- Receiving agents fetch and inspect the stated revision in their own worktrees,
  preserve dirty work, and reconcile relevant changes before continuing dependent
  implementation or reusing evidence. Report the revision incorporated or a
  concrete conflict to Boss. Do not reset another owner's worktree or assume a
  pushed branch is already integrated into main.
- After required gates pass, the merge owner uses the PR workflow and verifies
  the resulting main revision. No direct-main bypass or force push is allowed.
  If publication fails, retain the local work and report the blocked owner and
  action rather than claiming the correction is shared.

A push does not update existing worktrees. Agent handoff messages reach the
available active team; repository records support later sessions. Do not promise
cross-chat notifications, automatic checkout updates or a background service.

## Checks proportional to the change

**Tests are short and run in parallel (model owner, 2026-09-19: "For every
test, run on a strong machine with several cores; they should be short, with
fixed arrays").** A test uses a fixed small GameBoard and fixed arrays, pins its
integers before the first run and finishes in seconds; the suite runs with
`pytest -n auto` on every core of the machine, never serially on one; a long
reading is a research run (section 6 of the experiments), not a test.

Select the project interpreter from [.python-version](../.python-version) and
[the run instructions](../README.md#install-and-run) before installing dependencies
or executing checks. Use one project virtual environment; record the actual
interpreter/version in the handoff. Use the declared project version, not an
arbitrary host `python` alias. Older-Python and historical API/frozen-v10 equality
checks are not required. Preserve independent physical invariants and useful
regression regimes when removing compatibility comparisons or duplicate worlds.

When reusing that environment across worktrees or benchmark snapshots, an editable
install can still resolve another checkout. Set `PYTHONPATH` to the intended `src`
directory and verify the imported package path and source fingerprint before the
run. Recheck the fingerprint afterward; interpreter identity alone does not
identify the simulated source.

For a physics-engine behavior change, completion requires physics-rule validation,
necessary tests, an affected simulator run, and regression comparison. Architecture
reviews interface/schema changes; visualization reviews changed output. Reuse the
same run as evidence for several checks when its inputs and assertions match.

Use independent numerical/behavioral expectations and retain boundary cases that
exercise distinct risks. Consolidate identical worlds rather than multiplying
tests. Do not remove a failing requirement, change a frozen source, or turn failure
into an expected pass to achieve a green gate. A candidate's passing tests do not
repair another model's failure or establish a real-world law.

Since 2026-09-17, by the model owner's decision in
[Highlights 5.5](../docs/HIGHLIGHTS.md#55-acceptance-tests-and-open-decisions),
a test exercises one generic rule in isolation on a minimal GameBoard and nothing
else: one test module per rule, one per feature of the ray-event model, with the
expected integers written down before the first run. No test pins the numbers of
an example world, compares two worlds or reproduces a known experiment; those are
research runs, made once and recorded with a fingerprint and a date in
[validation evidence](../docs/VALIDATION.md), never repeated as tests. A change is
checked only against the tests that depend on what it changed, selected by the
import graph (`python tools/check.py`); the whole suite runs together only when
the shared core changes (the Node and its Ports, the order of the cycle, the
bounded integers, the phase), and then once, in parallel (`pytest -n auto`). A
physical milestone, a phenomenon that several rules produce together, is one
fingerprinted, dated run of the engine, not a suite. The cost of checking is
proportional to the risk of the change, never constant.

Pure documentation/skill changes need skill/link/language and packaging validation,
not newly invented physical tests. The repository's existing submission and CI
gate still applies. Ordinary runs and tests are headless; render only when the
user explicitly requests visualization or visual checks. Diagnostics may reject
a run but may not repair physical state. Consult
[the Beam Law](../docs/BEAM_LAW.md) and [the engine's bookkeeping](../docs/ENGINE.md)
before applying old scalar/particle or disturbance assumptions to the primary
API (`NatureBeamSimulation`).

## The cost of an integration, kept short (the model owner, 2026-09-20)

The weak force's integration took two and a quarter hours, a third of it
documentation, a third re-checking, and a merge of eleven conflicting files
because three agents wrote the same documents at once. The owner's rules from
that day ("we said without 85 worlds"; "put it in the skill"):

- **Replay the gate set, not the register.** Byte-identity of the GameBoard
  under a new key is proved on a gate set of about fifteen example worlds,
  one per table rule, key and family kind, so that every engine code path is
  replayed once; the whole register (109 worlds on 2026-09-20) is replayed
  only under `--full` or on demand. The gate set is listed with what each
  world covers. The gate set is `examples/events/gate_set.json` (section 4 of
  the trimming plan chose it by measured coverage on 2026-09-20);
  `tools/run_series.py --list` replays it; a new key or rule adds the world
  that first uses it to the list, with the line it covers.
- **Check once at each stage, fully once at the end.** `python tools/check.py`
  scoped per stage; `--full` and the gate-set replay after the first
  behaviour-free commit and at the end, not after every commit.
- **One writer per document, and agents apart.** A code agent and a
  documentation agent may run in parallel only with a written split of the
  files; two implementation agents never run on the same sources or the same
  register at once, since each then pays the merge.
- **Small worlds.** An acceptance world is seconds: the Mach-Zehnder is
  5 x 5. A long reading is a research run, made once.
- **Pages apart.** The HTML pages with the frame player are made by a
  separate agent from the runs, in parallel with the reviews, never by the
  implementation agent.
- **Report at the half.** An implementation of several stages sends its
  measured integers after the first half, so the physics-rule review and the
  genericity probe of that half run in parallel with the second half.
- **Brief with the exact files.** An agent starts cold; the brief names the
  documents, the design and the commit to start from, and the design's
  evidence is committed under `docs/designs/<key>/` so every session can read
  it.
- **Write the record once.** The day's findings, readings and the owner's
  words go to `docs/LOG_<date>.md` as they happen, one record each with the
  next number; a decision of the owner is one line in Highlights 5.4 linked
  to its record; a run's entry is written beside its worlds. Nothing is
  restated in a second document; the reader follows the link.

## Performance work

Initialization configuration is runtime data. UI and configuration changes must
not introduce a compilation, package rebuild or server restart for each edit.
Reuse the canonical validator and runner; verify that edited values reach saved
run inputs/results and that in-flight runs retain their original configuration.
Keep frontend interaction checks distinct from HTTP/backend tests.
During a lecture, use the prepared simulator to create, save and rerun experiment
configurations. Do not rebuild for configuration edits. If the checkout is behind
the intended GitHub revision, update and prepare it before using it for the lecture.

Separate environment setup, physical stepping and diagnostic rendering before
optimizing. Reuse a verified checkout and installed environment for later runs.
Measure before and after with identical inputs, tick counts, frame sampling,
resolution and dependencies; report host timings separately from model cost.
Preserve every physical update, event and acceptance check. Compare traces and
metadata. Inspect saved frames when visual checks were requested; otherwise
report visual validation as not run. Do not claim a speedup from fewer frames
or lower resolution without saying so. Active runs require initialization data.

When live display validation is explicitly requested, verify that an image is
available before final output and distinguish simulation-time preview from
export progress. Record time to first
visible output separately from total duration. Keep preview queues bounded,
preserve all canonical frames and physical failure evidence, and verify worker
cleanup plus the final replay handoff. Disclose unverified browser behavior.

## The main course: equations first, runs as confirmation (the model owner, 2026-09-21)

The law is one piecewise-linear map on an integer torus: every interval
translates the state vector by a rate, thresholds it and subtracts (the
events are what crossed), multiplies by a declared integer matrix (a split,
a rotation) and adds (the merge). The measurement is the one threshold read
out; its weight is the inner product of the pointer with itself, through the
coupling's primitive (docs/LOG_2026-09-20.md records 167, 171, 173). Four
consequences govern how every role works.

1. Where the rate is constant (rows between clicks: the flight, the phase,
   the split, the merge) the map has a closed form, the floor of a linear
   function, and every number is computed from the formulas before any run.
   A run of such a world confirms a formula and is never the source of a
   number: the expectation is the formula's integer, pinned before the run,
   and a run that differs refutes the formula or finds a rule the formula
   forgot (the spread of a record's paths, the arrival's rounding). No world
   of this class is run without its formula.
2. Where the rate depends on the state (a body pushed by its crowd, a
   collision, bound bodies exchanging content, a windowed detector on a
   branched record) the map is a difference equation with no closed form.
   Its solutions are the iteration (the engine, the exact integers) and the
   continuum limit (many intervals, a small rate: the differential equation
   where Newton, Coulomb, Doppler and Bohr appear or fail to). The derivation
   gives the limit's formula; the register gives the integers; a run is
   needed for the integers and for what the lattice does that the continuum
   does not.
3. Every derived formula meets known physics twice: in the limit (the known
   formula returns, or the derivation says where the lattice differs: the L1
   count, the encounter comb, isqrt's anisotropy) and at finite resolution
   (the registered integer against the experiment). A paper, a design or a
   record with only the equations is mathematics; one with only runs is
   simulation; the work is the pairing, one formula per registered integer.
4. The boundary between the classical and the quantum is the property of
   the rate (constant or state-dependent), measured as rows per record and
   clicks per record; the program's advantage is there, and every design
   states on which side its world lies.

**Refined by the model owner on 2026-09-22 (record 762): whatever can be
computed algebraically is computed algebraically.** The GameBoard is a
finite, computable thing, so a phenomenon, a prediction or a reading, measured
or not yet, is first derived in closed form from the law's integer operations;
a run proves what the algebra cannot, and never discovers a number the algebra
could have given. Every result is stated as matching nature, never as how
nature is (the paper's framing, the same record).

**Refined by the model owner on 2026-09-21 (record 205): a formula gives, a
run proves; and after the detector, the vector.** (1) A register entry
carries the formula, or the derivation's section, beside its number, and
where a formula exists the test derives and compares rather than reads a
pinned number (`tests/test_amplitude_cone.py` is the template). (2) A run
without a derived expectation is a research run and says so in its page
and its record. (3) The derivation mathematician's targets
(DERIVATIONS_BEAM.md) are the source of every series' expectations; a
target not reached marks a quantity a run may only measure. (4) The
register's `expectations.json` entries carry a `derivation` field, and the
review of an experiment's pull request checks the derivation before the
numbers. (5) An experiment names, before the run, the vector or tensor it
will read after the detector and its form (the readings by type in
ENGINE.md): a scalar, an integer 3-vector in a declared unit (**p**, **f**),
the traceless second-moment tensor **T**, or the record's phase-count vector.

(6) The observed value is the reading, not the GameBoard's number (the owner,
2026-09-21, record 210): a distance, a time, a speed, a mass, an energy, a
force, an angle or a probability is produced from the GameBoard's Links,
intervals, contents, phase steps and weights only through a named reading
(HIGHLIGHTS 5.7's dictionary); an experiment's observable comes from a
detector declared in the world file, never from the host's state, and a
GameBoard quantity is never compared with nature directly.

(7) Only a detector's reading is a measurement (the owner, 2026-09-21,
record 281, translated: "many get confused and take results they measured,
but that is a measurement after a detector; it is only possible to measure
through a detector"): every number a role reports, registers, draws or
cites is labelled a detector reading or a GameBoard reading; only the first
is compared with nature or pinned; the second is a diagnostic of the host's
view of the state and never stands in for a measurement.

**A formula lives in three places (the model owner, 2026-09-21, [record 248](../docs/LOG_2026-09-20.md#248-the-owner-the-quarks-and-every-such-formula-must-be-in-the-paper-in-git-and-in-the-code-when-and-how-did-you-reach-it-the-owner-2026-09-21-about-0425z-translated-and-then-how-does-it-work-with-the-quarks-are-the-quarks-dividers-of-the-masses-or-a-group-that-composes-the-masses-they-too-have-masses-every-such-formula-you-must-put-in-the-paper-and-in-git-and-in-the-code-when-did-you-reach-the-formula-how-did-you-reach-the-formula-these-formulas-are-critical-the-bosss-answers-and-the-rule-1-the-quarks-today-not-modelled-the-nucleon-is-a-family-the-owners-decision-of-2026-09-20-entity_catalogmds-rows-on-the-six-quarks-the-proton-and-confinement-hypothesesmd-13-issue-169-if-they-enter-they-are-families-that-compose-a-nucleon-a-group-not-dividers-three-measured-events-bound-by-the-strong-column-at-adjacent-nodes-with-the-rational-charges-2-3-and--1-3-each-with-its-own-content-in-units-and-the-decisive-physical-fact-the-protons-measured-mass-is-about-one-percent-the-quarks-rest-masses-and-about-ninety-nine-percent-the-binding-the-strong-fields-energy-which-the-law-already-expresses-as-the-mass-a-detector-reads-of-a-bound-body-record-115-binding-v1-the-read-mass-of-a-bound-set-is-not-the-sum-of-its-parts-units-so-under-the-minimal-mass-reading-record-243-the-unit-is-at-most-the-lightest-quarks-content-and-a-composites-mass-is-the-bound-sets-reading-a-derivation-for-section-16-2-2-when-and-how-the-mass-formula-was-reached-mass--content-in-units-of-the-quantum-the-minimal-mass-one-unit-the-content-as-an-integer-amount-of-units-since-the-law-of-the-ray-the-code-era-code_to_formulas-1-the-drives-step-rule-with-the-mass-one-link-per-q-s-m--p-of-drive-the-label-along-the-unit-vector-at-q--64-with-the-physicists-corrections-2026-09-20-beam_laws-step-rule-the-coupling-and-the-charge-per-unit-of-content-the-one-mechanism-the-columns-2026-09-20-e--h-f-as-the-cost-of-a-release-per-unit-and-the-statement-that-the-minimal-mass-is-one-unit-and-not-free-reached-today-from-the-owners-question-record-243-its-theorem-status-and-the-mass-ratios-assigned-to-section-16-2-the-chronology-written-into-code_to_formulasmd-section-6-3-the-rule-the-owners-durable-every-formula-the-law-reaches-lives-in-three-places-and-code_to_formulasmd-records-when-and-how-it-was-reached-in-git-its-derivation-section-and-its-line-in-beam_law-or-formmdlawmd-in-the-code-the-docstring-of-the-function-that-computes-it-naming-the-section-and-a-derive-and-compare-test-or-a-derivations-entry-of-the-register-and-in-the-paper-the-paper-agent-adds-it-under-the-paper-writer-skill-when-the-section-lands-written-into-skillsworkflowmd-under-the-main-course-the-minimal-mass-and-the-mass-ratios-go-to-the-paper-with-section-16)).** Every formula the law reaches is written (1) in git, in its derivation section and its line of the law's document; (2) in the code, in the docstring of the function that computes it, naming the section, and in a derive-and-compare test or a `derivations` entry of the register; (3) in the paper, under the paper-writer skill, when its section lands. [docs/CODE_TO_FORMULAS.md](../docs/CODE_TO_FORMULAS.md) records for each formula when and how it was reached. A formula in one place only is not yet a result.

## The generic vector form first (the model owner's ask, 2026-09-21, record 177)

Every new rule of the law is sought and stated first in its generic vector
form, dimension-free and world-free: the set it acts on, the measure or map
it applies, the invariance it keeps; only then in its integer form per
dimension and its declaration per world. A rule that has no such form is a
world's declaration and not a law. The fan of directions is the case: three
per-world lists (91, 5, 290) each hid an equal-weights choice that the vector
form (the primitive directions within a width, each weighted by the measure
of its cell on the sphere) shows to be wrong by up to 5.4 on the sphere.

## Notation: every symbol named, its kind shown (the model owner, 2026-09-21, record 184)

Every symbol is named in English at its first use in a document, a message
or a record, so that the owner can type and search it: "gamma (the Lorentz
factor)", "c (the pace of a row)", "rho (the charge per unit of content)".
A Greek letter never stands alone: write its name in Latin letters and the
quantity's name beside it. The kind of a quantity is shown by its type,
in every document and every message to the owner: a scalar in plain text
(`c`, `M`, `N`, `gamma`); a vector in bold lowercase (`**p**` the momentum
vector, `**s**` the state vector on the torus, `**r**` the rate vector);
a tensor, a matrix or an operator in bold uppercase (`**C**` the coupling
matrix, `**G**` the click's Gram matrix, `**F**` the interval's map). A
component of a vector is a scalar and is written plain with its index
(`p_x`). In code the identifier's name says the kind where it matters
(`momentum` a vector of three integers, `count_table` a table). Every
role's skill points here; a review checks it as it checks the language.

## The three tests of every rule: generic, vector, local (the model owner, 2026-09-21, record 202)

A rule enters the law only if it passes all three, and every role applies
them: the implementer before writing it, the reviewer before admitting it,
the mathematician when stating its form, the Boss when ordering it.

1. **Generic.** One primitive with declared integers (a rate, a wall, a
   matrix, a table) and no family name or kind; the same primitive serves
   every family; its special cases are values, not branches (a row is a
   body of no content); the engine branches on no name.
2. **Vector.** One of the six verbs on the state vector: the translation of
   an accumulator by its rate, the bilinear form with a declared matrix, the
   group-ring addition, the permutation, the evaluation, the Euclidean
   division with the remainder kept; its rate at most bilinear in the
   state; no root, no float, no rounding at run time beyond the ones
   declared at load.
3. **Local.** It reads only its own record and the six neighbouring Nodes
   (LOCALITY-1); fixed work and storage for a fixed K; nothing kept at a
   Node; every host reading labelled host.

A rule that fails one test does not enter the law. A hypothesis that needs
more (a seventh verb, a root at a declared grain) is stated under its own
identity, outside the law, until it passes or the owner admits the verb.
State the three verdicts, one line each, in the design, the review and the
pull request.
Why the three tests give the least computation in the large system (the
owner's question, 2026-09-21, record 206): the cost of an exact run is the
number of events times a constant, with nothing that grows with the
GameBoard's size or the number of families; local bounds the work per Node
(six neighbours), vector makes each step a fixed number of bounded-integer
operations with no iteration inside it and gives the rows a closed form,
generic makes one primitive serve every family (one code path, one table,
one verification). The number of events is the floor of any exact
computation. And it follows that a generic system is ruled by small
conditions: the only free numbers are the family table's declared integers,
the width and the initial state; a large system has no rule of its own
scale, every known formula is the limit of the small local rule, and a
change of one small condition moves the registered integers everywhere,
exactly: a wrong small condition is caught by the large system's pins.
 Form B of the body's drive was the first rule read against
the three (record 201 of the log of 2026-09-20).

## The six lines of every report (the model owner, 2026-09-21, records 530, 533, 534, 535 and 536)

Every report, proposal, review finding or question a role sends to the Boss, and every one the Boss sends the owner, opens with six short lines, one each, never an essay: (1) the information: what the item moves between which records or Nodes, through which Link and Port, at what rate, what is kept and what is lost; (2) the generic solution: the one primitive, for every family alike, from which the number follows, never a patch beside it (record 421); (3) why it will work: the mechanism on the GameBoard, with the reading that would show it and the reading that would refute it; (4) why do this at all: what it buys the law or a measurement, and what stays unread or wrong if it is not done; (5) the Highlights: which decisions of docs/HIGHLIGHTS.md section 5.4 the item keeps and why they still hold, and whether one of them should now change, a change being an option proposed with its evidence and made on the owner's word as a new line naming the one it supersedes; (6) the implementation: what changes in the tree (engine, register, documents), which identities and registrations it touches, the time end to end (the build, the runs, the review) as a host estimate, and whether it is dangerous: what it can break, what re-run or read guards it, and whether the key stays off by default. The six lines are the report's head; the evidence follows them. Every number in them is labelled DETECTOR or GAMEBOARD.

## How the team works now (the model owner, 2026-09-21, record 309)

The owner's instruction: the Skills describe the team as he builds it now. The
roles, as they run today, one writer per document:

| Role | Writes | Does not write |
| --- | --- | --- |
| The Boss (the orchestrator) | the day's log, Highlights 5.4, the Skills, the records of every word of the owner; opens and merges the pull requests | any design, derivation or manuscript |
| The physicist | the designs under `docs/designs/` (a hypothesis, a candidate, a verdict on the dark sector, item by item), FULL_PICTURE, the far-lamp notes | DERIVATIONS_BEAM, BEAM_LAW, the paper |
| The derivation mathematician | DERIVATIONS_BEAM (every formula as a limit of one rule; the map 21.2 with its status, order and error term) | the designs, the law's text |
| The architect | BEAM_LAW's text, the genericity probe, the host-only unifications | the derivations, the designs |
| The paper coordinator | the manuscript, with its referee ([paper-coordinator](paper-coordinator/SKILL.md)) | the tree's documents; it reports what reaches the tree with its status |
| The Visualiser | no page (the gallery pages under `docs/pages/` were deleted on 2026-09-22, the owner's word of record 894; the Visual Checker's design folder `docs/designs/visual_check/` when it lands) | any number of the register |
| The physics-rule reviewer, the implementers, the experimenter | one bounded assignment each, as agents of the Boss: a review file, a branch, a registered run | the shared documents beyond their assignment |

The order and the report (the owner's rules of the day, in one place):

1. Every assignment is one bounded order sent as a direct message into the
   role's own session (the rule of messaging below): the question, the pins
   written BEFORE any number, the deliverable's file, the bound in time, the
   verdict as one of three (reached or derived; a hypothesis under its own
   identity naming what must be added; refuted or not reachable, with why).
   The report is one paragraph with the head SHA; the Boss opens the pull
   request when the writer's tool refuses, and merges on green. Nothing enters
   the law by an order alone.
2. No experiment for nothing: a run is ordered only with its expected number
   written first (record 205); a differing run refutes and never moves the
   number without its cause; every reported number is a detector reading or
   a GameBoard reading, named so (record 281).
3. The method (record 305, the six-point standard of record 300): the
   infinite limit derives the form, the run confirms the number, and the pin
   only orders that the first be written before the second; every derived
   formula carries its rule, the limit taken, the order of the expansion, the
   symmetry it needs, its error term and its check against a pinned value;
   a limit that differs from nature is a FAIL in the same font as a PASS.
4. The gate before a build: a design is read by the physics-rule reviewer
   (the three tests, LOCALITY-1, the measurement rule, bit-exactness with the
   identity off, the world-file declarations); the verdict is admissible,
   admissible with must-fixes (the writer amends, one bounded order) or not;
   the build starts on the verdict and the owner's go; the reviewer reads the
   head again before the merge when registered integers move.
5. An external review brought by the owner is checked point by point against
   the current main, with the commit each fixed point landed in; what is
   right and missing in the tree is added where it belongs, by its writer,
   and nothing else moves (records 293, 304).
6. Every word of the owner is recorded at once, translated and marked so, with
   the next record number; a decision of his is one line in Highlights 5.4;
   a question of his is answered from the tree, no run, and recorded with the
   answer. A deadline he sets is reported honestly at its hour: what landed,
   what did not, what stays with him (record 289).
7. The paper's referee: the coordinator activates a second reader who checks
   every round of the manuscript against the tree (each citation, integer,
   formula and status); its findings are applied in the manuscript or sent
   through the Boss to the file's writer as one bounded fix; the paper never
   changes the tree, and the tree's writers never write the paper.
8. Messaging between sessions (the model owner, 2026-09-24: "put it in your
   skills and the other agents' skills: always use SendMessage"): every
   order, report, question and answer between the Boss and a role's session,
   and between two sessions, is sent as a direct message with the SendMessage
   tool; the sender first lists its reachable agents (ListAgents) and checks
   that the receiver is on the list; the receiver replies by SendMessage to
   the sender's listed name. A Routine (create_trigger, send_later) is used
   only for what must happen at a later time (a check-in at an hour, a
   re-read after a run's expected end), never as a way to talk; a direct
   message creates no scheduled task. When the receiver is not on the list
   (its session stopped or unreachable), the sender says so in its report
   and does not fall back to a Routine as a message; the Boss decides.

## Tools and authority

The user has given standing authorization to publish requested Universe24 work
to Git: commit, push and open or update its PRs without another confirmation.
This also covers the requested project Skill updates and remediation handoffs.
Use existing authorization for a merge when it covers that change; do not require
a repeated approval merely because a Skill mentions approval. Keep scope and
required review/CI gates intact. This is not permission for unrelated changes,
force pushes, destructive repository operations or messages to other people.

Use the available local Git/Python tools and discover the connected GitHub tools
when needed. Read access does not imply merge authority. Use existing user
authorization for edits, publishing and merges; do not ask again for an already
authorized action. A skill never supplies otherwise missing authorization or
permits bypassing an access control or failed gate. Do not send messages to people
unless the user authorized that communication.

The PR owner records the tested head, current base and relevant results. The
coordinator is the final merge owner for a coordinated task. Skills do not claim
that GitHub enforces a branch protection rule unless it was actually verified.

## The shortened process for the engine's features (the owner, 2026-09-24, records 1812 and 1813)

The owner's words of 2026-09-24, 12:36Z to 14:12Z, in force for the
stabilisation of the engine and the freeze:

1. **One list, sixteen experiments** ([RUN_LIST.md](../docs/designs/detector_law/RUN_LIST.md); the sixteenth, a two-qubit quantum computer, added on 2026-09-25, record 1883);
   the seven others are OUT, not deferred ("there is no after the paper").
2. **One agent writes all the engine code, the worlds and the test-run lines**
   (Nature24, the physicist; the owner's word of 17:05Z: "only one writes the
   code, the worlds and the test world: for us Nature24"): the
   three features are one job, making the one operator, the click and the
   birth (which replaced the four building blocks on 2026-09-25, record 1875)
   one code for every body on the board;
   the experiments are compositions declared in the world file and defined
   in [SIMULATOR_DEFINITIONS.md](../SIMULATOR_DEFINITIONS.md); the engine
   knows no lamp, polariser or light clock by name. No builders, no World
   Generator, no world file before its row's feature is on `main`.
3. **Features are named, never numbered:** the receiver by name, the joint
   gather, the lamp's ladder.
4. **One branch, one merge** for the three features; a feature is pushed
   when its unit test (on a world that is none of the fifteen) passes; before
   a push only the docs gates and the changed modules' tests; the full gate
   once, at the freeze; the docs after the code; the reviewer reads once
   after the merge ([physics-rule-validation](physics-rule-validation/SKILL.md)).
5. **Every world has its test-run line, written by the world's writer before
   the run** (`docs/designs/detector_law/TEST_RUNS.md`, written by Nature24):
   what a clean preliminary run must show, with no pin and no target number;
   the Preliminary Runner runs each feature's experiments on the writer's
   branch as soon as it is pushed and reports clean or what broke; a defect in
   `src/` goes to the writer through the Boss.
6. **The Boss's status, three columns per experiment**
   ([ENGINE_STATUS.md](../docs/designs/detector_law/ENGINE_STATUS.md)): the
   engine features it needs and whether they are on `main`; its world file
   on `main`; its test run without a pin clean or not; a cell rewritten only
   on a merged record. The freeze is every row "yes" on one commit; then the
   owner's GO and every pin run in one go.
7. **Every block and every composition is tested alone before it is
   composed** (the owner, 2026-09-24, record 1823): the emitter, the body,
   the receiver, the clock, and each named composition (the polariser, the
   splitter, the mirror, the crystal) has its own unit tests on a small
   world that is none of the list, on every kind of input it can receive
   (every label, a superposition, an input from each Port). Only then is it
   composed into an experiment's world, which tests the composition. A
   block tested on one kind of input alone is a gap: the polariser's bug
   lived because it was tested on label 0 alone.
8. **Three levels: the one operator, the lab tools, the experiments**
   (the owner, 2026-09-24, record 1825; the engine's level made the one
   operator, the click and the birth on 2026-09-25, record 1875). The engine
   knows the one operator, the click, the birth and the six verbs. A lab tool
   (the polariser, the splitter, the mirror, the crystal, the well body) is a
   region of the operator with its material integers, defined once in the
   tool library (`examples/events/entities/apparatus.json`), with its own section of
   algebra and a unit test that checks that algebra exactly. An experiment
   is a world file that places tools by name at positions on the board,
   and its pin is computed from the tools' algebra. All the tools are specified in one
   file, `docs/designs/lab_tools/LAB_TOOLS.md` (one section per tool: its
   specification, algebra, timing, cost, engine lines and test values;
   existing design files cited, never copied), linked from ALGEBRA.md. The
   mathematician writes it; Nature24 checks every section and talks with the
   mathematician directly by Routine; a disagreement goes to the Boss for
   the owner. Nature24 writes each tool's code once its section is agreed
   (records 1830 to 1832). No Node carries a table: a tool is a body of
   material whose Nodes carry only material integers, and its action arises
   from the one rule (record 1838).
10. **The algebra, then the code, then the mathematician confirms** (the
   owner, 2026-09-24, record 1843). A tool is taken from the algebra, never
   invented: its section in ALGEBRA.md names its group element (of G_48, of
   the rotations G_24 = S4, or a rotation of the label module) and says
   whether it has a direction at all. Nature24 writes its code from that
   section; the code merges only after the mathematician confirms, line by
   line, that it performs exactly that group operation. Every operation in
   the cells is an operation of the group: a per-cell branch that is not one
   is forbidden. A tool
   declares its own orientation and never the directions of what leaves it.
   The specification goes into the tool file (LAB_TOOLS.md) from the
   algebra alone, the code is built from that file, and the experiments
   run only after every tool's algebra is closed and every tool merged; a
   well's seed is the bound mode of the composed world and never collides
   with another tool (the owner, 2026-09-25, record 1855).
   No tool acts on cells but through the law's advance and the click; momentum
   is conserved on the board's own values. Nature24 merges each tool to main
   on green CI with the mathematician's line-by-line confirmation, and tells
   the Boss for the record (the owner, 2026-09-25, record 1856).
   Everything is algebra (the owner, 2026-09-25, record 1875): a world
   declares only its extents, its operator as data, the births' data, the
   occupation and the receivers' names; a lab tool is a region of the
   operator with its material integers, never code; the initial state is
   derived and checked at load; an experiment's run checks only clicks.
9. **A physicist's validity report at the freeze** (the owner, 2026-09-24,
   record 1826): before the owner's GO, an independent physicist session,
   never the worlds' writer, writes one report on the list. For each
   experiment it states nature's experiment and what it tests, the tools
   the world places, the mechanism the world exercises, every declared
   input and why nature gives it, the pin and its provenance, and a
   verdict. The writer answers its questions through the Boss.

Unchanged, the law: one unit test per feature; no pin moved after a reading;
no world file by hand; LOCALITY-1, bounded integers, the measurement rule.

## The experimenter places the body exactly (the owner, 2026-09-24, record 1815)

The owner's word of 2026-09-24, 16:35Z: "in the code the experimenter must be
able to put the cube exactly where he wants it." A body is declared in the
world file by its place and its side (its corner and its edge, the cube's
vertices), a cube on a board, a square on a layer, a segment on a chain
(ALGEBRA.md 8.3); the loader places it exactly there and refuses a body that
does not fit the board rather than cutting it to fit; a refusal is a
declaration error, never a silent change of shape. Where the loader today
cuts a side to the board, that is a defect against this word, listed among the
body's conditions in [SIMULATOR_DEFINITIONS.md](../SIMULATOR_DEFINITIONS.md)
and fixed on the owner's word as an engine line with its test.

## Plain names, never codes alone (the owner, 2026-09-24, 16:55Z, record 1815)

The owner's word: "L and M are not clear; use only clear names." Every
experiment, world line, feature and file is called by its plain name first:
"the two slits, the second draft", "de Broglie's fringes", "the energy of a
moving mass", "the muon's form", "Sagnac", "the moving lamp's redshift", "the
receiver by name". A code (a row number such as 4a or R2, a line label such
as L-3, a family letter such as M1) may follow the name in parentheses as an
index into a table, never stand alone in a message, a heading, a report or a
commit; a new label is not coined. In any message the owner may read,
including an agent's replies in its own session, no code appears at all,
not even in parentheses: say what the thing is ("the declaration of the
muon's ramp", not "M1-8"; "the list of the world lines in the
declarations", not "section 15") (the owner, 2026-09-24, record 1828,
"still using unclear names").
No wave on the board: a record holds one integer amplitude per Node and
the one local rule is the split; "wave", "wavelength" and "phase
matching" name only the Outside reading of that rule and are said as such
(the owner, 2026-09-24, record 1833; docs/TERMINOLOGY.md). The features' rule of 14:00Z is the same
rule.

Our names, never the laboratory's, for a block (the owner, 2026-09-24,
record 1820): "use only our names; there is no pump, there is an emitter."
A block is called by what it is on the GameBoard: an emitter, a body, a
receiver, a clock, or a named composition of them (a crystal, a polariser, a
mirror). The laboratory's word for the same thing (a pump, a laser, a beam
splitter) may be said once to explain what it models, never as its name.
