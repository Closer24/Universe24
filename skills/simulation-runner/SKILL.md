---
name: simulation-runner
description: Execute reproducible Universe24 scenarios and inspect runtime outcomes, traces and HTML without changing the physical laws.
---

# Simulator execution

Read [the shared workflow](../workflow.md), current
[run instructions](../../README.md) and the output/failure contract in
[definitions](../../SIMULATOR_DEFINITIONS.md). This skill can run independently
or receive a scenario from Boss, tests or a field owner.

**Input:** source tree, model, initial state, parameters, duration and acceptance
conditions. **Output:** the exact invocation/setup, completion/failure metadata,
events and an inspected HTML replay. Use the existing Python runner and renderer;
an API-only candidate must retain its actual identity in recorded evidence.

Verify the runtime and select an existing scenario or explicit initial conditions
that exercise the requested behavior. Use an isolated checkout and unique output
directory. Do not run a large parameter sweep when one bounded case resolves the
current question. Reuse a matching test run instead of duplicating it.

Check actual completion, requested tick count, source fingerprint/model, integer
and occupancy checks, per-tick momentum and relevant isolated-motion acceptance.
Frame stride changes recording only, never the physical update interval. On a
failure retain the trace, failure frame and FAILED RUN report; do not smooth the
trajectory or silently rerun with weaker parameters.

Inspect the existing standalone HTML and relevant frames. A successful process
does not prove the candidate is physically accepted. Route runtime errors to the
component owner, visual ambiguity to visualization-check, and a reproducible
behavior difference to regression-check/physics-rule-validation. Do not edit
laws or use diagnostic results to repair the world while running an experiment.
