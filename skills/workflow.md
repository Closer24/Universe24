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

- **Replay the gate set, not the register.** Byte-identity of the lattice
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

(6) The observed value is the reading, not the board's number (the owner,
2026-09-21, record 210): a distance, a time, a speed, a mass, an energy, a
force, an angle or a probability is produced from the board's Links,
intervals, contents, phase steps and weights only through a named reading
(HIGHLIGHTS 5.7's dictionary); an experiment's observable comes from a
detector declared in the world file, never from the host's state, and a
board quantity is never compared with nature directly.

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
