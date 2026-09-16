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
5. Assess finite-size, boundary, lattice-direction and encoding effects relevant
   to the claim. Sensitivity/convergence controls must represent the same physical
   case with fixed hypotheses. Do not assume that shrinking a fundamental lattice
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
or correction is requested; reuse catalog entities and explicit experiment
profiles where appropriate. Unsupported format or composition means a capability
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

## Checks proportional to the change

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

Pure documentation/skill changes need skill/link/language and packaging validation,
not newly invented physical tests. The repository's existing submission and CI
gate still applies. Ordinary runs and tests are headless; render only when the
user explicitly requests visualization or visual checks. Diagnostics may reject
a run but may not repair physical state. Consult
[the active disturbance contract](../docs/DISTURBANCES.md) before applying old
scalar/particle assumptions to the primary Simulation API.

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
or lower resolution without saying so. Keep historical renderer benchmarks on
`event_universe.legacy_runner`; active runs require initialization data.

When live display validation is explicitly requested, verify that an image is
available before final output and distinguish simulation-time preview from
export progress. Record time to first
visible output separately from total duration. Keep preview queues bounded,
preserve all canonical frames and physical failure evidence, and verify worker
cleanup plus the final replay handoff. Disclose unverified browser behavior.

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
