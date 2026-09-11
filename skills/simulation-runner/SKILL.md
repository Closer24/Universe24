---
name: simulation-runner
description: Execute reproducible Universe24 runs and inspect outcomes and traces, with visualization only when requested, without changing the physical laws.
---

# Simulator execution

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

For primary runs, require the explicit initialization file and read its field,
disturbance, transport, coupling and cost definitions; see
[DISTURBANCES.md](../../docs/DISTURBANCES.md). Missing input must not select a
historical scalar universe. Historical scenarios belong to the separate
`event_universe.legacy_runner` entry point.

Verify the runtime and select explicit initialization or a named historical scenario
that exercises the requested behavior. Use an isolated checkout and unique output
directory. Do not run a large parameter sweep when one bounded case resolves the
current question. Reuse a matching test run instead of duplicating it.

Check actual completion, requested tick count, source/configuration identity,
integer bounds, local capacity and declared per-tick conservation. Check momentum
and isolated-motion acceptance when the selected historical candidate requires them.
Frame stride changes recording only, never the physical update interval. On a
failure retain the trace and failed metadata. If visualization was requested,
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
work, not a simulator benchmark.
Historical live previews require explicit `--live` or API `live=True`, which
also requests recorded visualization. A performance investigation alone does not request
visualization, a live preview or visual test execution.
