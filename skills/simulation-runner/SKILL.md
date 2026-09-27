---
name: simulation-runner
description: Execute reproducible Universe24 runs and inspect outcomes and traces, with visualization only when requested, without changing the physical laws.
---

# Simulator execution

The team of 2026-09-26 and the generic engine's way of work: [How the team works now](../workflow.md#how-the-team-works-now-the-model-owner-2026-09-26-records-2134-2186-2187-and-2190) and [The generic engine](../workflow.md#the-generic-engine-the-engine-supports-the-run-defines-the-model-owner-2026-09-26-records-2172-to-2190) in the shared workflow (records 2186 to 2190). Every agent may run the engine locally and debug it with the trace; only the coder, Coder 3, changes it.

> **One engine (2026-09-19).** The runner takes `--init`, `--output` and `--ticks`
> only and runs a world of the Beam Law headless; `--visualize`,
> `--frame-stride`, `--observer`, `--node-workers`, `--dense-field` and
> `--standing-field` went with the old engine (migration).
> Where this Skill names them, read the history.

For creating or changing the input, use
simulation-configuration, including its
complete file map and runnable template. This skill executes the resulting input.

Read [the shared workflow](../workflow.md), current
[run instructions](../../README.md) and the output/failure contract in
definitions. This skill can run independently
or receive a scenario from Boss, tests or a field owner.

**Input:** source tree, model, initial state, parameters, duration and acceptance
conditions. A run's duration is declared from the world's own clocks (the
lamp's turn recurrence and the flight to the gather), derived before the run
and never a fixed margin; a first declaration that falls short is kept with
its readings and the re-declaration is derived, never chosen to meet a number
(the Bell runs of 2026-09-22, series L6). **Output:** the exact invocation/setup, completion/failure metadata
and events. Runs are headless by default: do not capture frames, import rendering
dependencies or create HTML/GIF unless visualization is explicitly requested.
Use the existing Python runner and optional renderer; an API-only candidate must
retain its actual identity in recorded evidence.
When visualization is requested, the deliverable is an HTML page that embeds
the GIF or the frames next to the run's readings (the world, the plane shown,
the scale of each region, the intervals per frame); a GIF is never delivered
on its own (model owner, 2026-09-19: "Always put a GIF inside HTML").

**Every experiment delivers its results page (model owner, 2026-09-20).** The
owner's words: "Add to every experiment that is made that it shows results in
HTML: the GameBoard with the detector as an icon and the star as an icon on
the GameBoard, so that one understands exactly what is tested; and it states why
it was tested and what the conclusion is." So every research run (a series or
a numbered run in EXPERIMENTS) delivers, beside
the register entry, one HTML page in the owner's page style (no document
skeleton, a `<title>`, colour tokens with dark mode, phone width) that carries,
in this order: (1) a drawing of the GameBoard of the world with an icon for
each thing on it: the detector (its set of Nodes), the star or source (a
measured event, its content), the lamps, the walls, the probes, each with its
name from the world file and a legend (the owner, the same day: "to show atoms
I do not need a detector": an atom is drawn as its proton and its electron's
set on the GameBoard; a detector appears only where the world declares one,
receiving what comes out of the thing, or a lamp that shoots a beam at it as
physicists do); (2) "Why it was tested", the question
in the owner's words and the expectation written before the run; (3) the
moving picture of the run when there is one, played inside the page with a
time control (a canvas player over the frames with play and pause, a slider
over the intervals and the interval shown, the GIF kept as a link; the model
owner, 2026-09-20: "the page does not run, one cannot see it move by time")
with the plane shown, the scale of each region and the intervals per frame; (4) the readings, measured against expected, inside or outside the
brackets, nothing moved; (5) "The conclusion", the verdict in plain words and
what the law lacked, if anything. The page is written to the scratchpad (not
the repository) and Boss publishes it as an artifact; the numbers stay in the
register.

**Two kinds of readings (model owner, 2026-09-20: "in reality there is no
such thing").** Label every registered number: a detector reading (the record
of a detector's set or of a measured event in the world; the only kind
reality has) or a GameBoard reading (the host's view of the GameBoard: positions,
counts per Node, shell means, the books; a picture or a bookkeeping check,
never the measurement). A comparison with nature uses detector readings
only; a readings tool prints which kind each line is.

For authorized physics comparisons, apply the shared
[physics comparison method](../workflow.md#physics-comparison-method).
Its standing HTML requirement counts as an explicit visualization request for
those research runs; ordinary automated tests remain headless. Execute the fixed
observable/expectation plan without retuning and retain quantitative discrepancies
alongside the inspected HTML. A visual match is not physical acceptance.

For primary runs, require the explicit world file and read its families,
measured events, tables and detectors; see the Beam Law
and [the engine's bookkeeping](../../docs/ENGINE.md) (the generic disturbance
contract, DISTURBANCES.md, was deleted on 2026-09-19). Missing input must not
select an implicit historical universe.

Follow the shared
[configuration task scope](../workflow.md#configuration-tasks-and-implementation-scope)
when a preflight or run fails. Return the diagnostic to the appropriate owner;
running an experiment does not authorize a simulator fix.

For configuration-only checks, use the read-only
preflight API/CLI and return its report;
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
output retention: generated output is registered for
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

## Notation (the owner, 2026-09-21, record 184)

Every symbol is named in English at its first use (never a Greek letter alone: "gamma (the Lorentz factor)"), and its kind is shown by its type: a scalar plain, a vector in bold lowercase (**p**), a tensor, matrix or operator in bold uppercase (**C**); skills/workflow.md, "Notation".

## The three tests of every rule (the owner, 2026-09-21, record 202)

A rule enters the law only if it is generic (one primitive with declared integers, no family name or kind), vector (one of the six verbs on the state vector, its rate at most bilinear, no root, no float) and local (its own record and the six neighbours, fixed work, nothing kept at a Node); state the three verdicts, one line each; skills/workflow.md, "The three tests of every rule".
