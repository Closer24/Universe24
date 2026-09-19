---
name: simulation-runner
description: Execute reproducible Universe24 runs and inspect outcomes and traces, with visualization only when requested, without changing the physical laws.
---

# Simulator execution

> **One engine (2026-09-19).** The runner takes `--init`, `--output` and `--ticks`
> only and runs a world of the law of the shadow headless; `--visualize`,
> `--frame-stride`, `--observer`, `--node-workers`, `--dense-field` and
> `--standing-field` went with the old engine ([migration](../../docs/MIGRATION.md#one-engine-on-2026-09-19-the-old-engine-deleted)).
> Where this Skill names them, read the history.

For creating or changing the input, use
[simulation-configuration](../simulation-configuration/SKILL.md), including its
complete file map and runnable template. This skill executes the resulting input.

Read [the shared workflow](../workflow.md), current
[run instructions](../../README.md) and the output/failure contract in
[definitions](../../SIMULATOR_DEFINITIONS.md). This skill can run independently
or receive a scenario from Boss, tests or a field owner.

**Input:** source tree, model, initial state, parameters, duration and acceptance
conditions. **Output:** the exact invocation/setup, completion/failure metadata
and events. Runs are headless by default: do not capture frames, import rendering
dependencies or create HTML/GIF unless visualization is explicitly requested.
Use the existing Python runner and optional renderer; an API-only candidate must
retain its actual identity in recorded evidence.

For authorized physics comparisons, apply the shared
[physics comparison method](../workflow.md#physics-comparison-method).
Its standing HTML requirement counts as an explicit visualization request for
those research runs; ordinary automated tests remain headless. Execute the fixed
observable/expectation plan without retuning and retain quantitative discrepancies
alongside the inspected HTML. A visual match is not physical acceptance.

For primary runs, require the explicit initialization file and read its field,
disturbance, transport, coupling and cost definitions; see
[DISTURBANCES.md](../../docs/DISTURBANCES.md). Missing input must not select an
implicit historical universe.

Follow the shared
[configuration task scope](../workflow.md#configuration-tasks-and-implementation-scope)
when a preflight or run fails. Return the diagnostic to the appropriate owner;
running an experiment does not authorize a simulator fix.

For configuration-only checks, use the read-only
[preflight API/CLI](../../docs/CONFIGURATION_VALIDATION.md) and return its report;
do not launch a simulation. The active runner shares its initialization/observer
preparation with preflight. A valid report does not certify future capacities or
physical behavior; actual execution and acceptance remain separate evidence.

Verify the runtime and select explicit initialization or a named historical scenario
that exercises the requested behavior. Use an isolated checkout and unique output
directory. Do not run a large parameter sweep when one bounded case resolves the
current question. Reuse a matching test run instead of duplicating it.

For CPU-parallel active Simulation runs, pass `--node-workers N` with a bounded
value from 2 through 64. This is a host scheduling choice and must not be inserted
into the physical initialization JSON. Verify `run.json.execution`, and compare a
bounded serial control when accepting scheduler work: state, ordered events,
modeled costs and declared accounting must match exactly at every tick.
Include a `spatial_computation_delay` control when the shared field/carrier clock
is affected; both planning barriers must still lead to one joint Node commit.

Both runners require a new or empty output directory. Follow
[output retention](../../docs/RETENTION.md): generated output is registered for
24-hour cleanup after writing finishes, while active leases protect ongoing
writes. Keep original initialization outside the output and never register source
or templates as disposable artifacts. Inspect or save required acceptance evidence
before it expires; startup cleanup alone does not run while the simulator is idle.
Use the cleanup CLI's `--watch` or an authorized scheduled command when needed.

Check actual completion, requested tick count, source/configuration identity,
integer bounds, local capacity and declared per-tick conservation. Check momentum
and isolated-motion acceptance when the selected historical candidate requires them.
Frame stride changes recording only, never the physical update interval. On a
failure retain the trace and failed metadata for the retention period. If visualization was requested,
also retain the failure frame and FAILED RUN HTML report. Do not smooth the
trajectory or silently rerun with weaker parameters.

Inspect metadata and events for every run. Only when visualization was requested,
inspect the existing standalone HTML and relevant frames. Test-run rendering is
opt-in with `pytest --visualize-runs`; normal test runs remain headless and keep
their physical assertions. A successful process does not prove the candidate is
physically accepted. Route runtime errors to the component owner, visual ambiguity to visualization-check, and a reproducible
behavior difference to regression-check/physics-rule-validation. Do not edit
laws or use diagnostic results to repair the world while running an experiment.

For speed investigations, follow the shared workflow's
[performance procedure](../workflow.md#performance-work). Reuse the environment
once dependencies and source identity are verified; installing it again is setup
work, not a simulator benchmark. A performance investigation alone does not
request visualization or visual test execution.
