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

Keep model rules, hypotheses to test and verified results distinct. A hypothesis
needs a test and pass condition; a verified result needs an identified tree and
completed evidence. A high-level target or a passing detector is not proof that
the underlying physical law works.

Keep durable procedures in Skills and architectural decisions in their responsible
documents. Put temporary task state, assignments, blocked checks and next actions
in Issues/PRs. For permitted publishing, persist the handoff there rather than only
in chat. If publishing is unavailable or unauthorized, report the unsaved handoff.
Do not claim personal Skills were installed merely because repository files exist.

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
For within-world parallelism, compare complete per-tick state and ordered failure
prefixes, and report actual dispatched work and serial fallback. Include worker
startup, data transfer and shutdown in end-to-end timing; a worker count alone
does not establish acceleration. Verify cleanup after failed and interrupted runs.
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

Use the available local Git/Python tools and discover the connected GitHub tools
when needed. Read access does not imply merge authority. Use existing user
authorization for edits, publishing and merges; do not ask again for an already
authorized action. A skill never supplies otherwise missing authorization or
permits bypassing an access control or failed gate. Do not send messages to people
unless the user authorized that communication.

The PR owner records the tested head, current base and relevant results. The
coordinator is the final merge owner for a coordinated task. Skills do not claim
that GitHub enforces a branch protection rule unless it was actually verified.
