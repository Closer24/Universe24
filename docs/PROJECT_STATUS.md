# Project status and restart guide

## Where the project stands on 2026-09-19 (read this first)

**One law, one engine.** Everything below is on `main`; nothing is in a branch
or a machine.

**The law of events (2026-09-19, after the one engine; recorded, not implemented).**
The model owner's definitions, in Highlights 5.4 after "One speed, and what is
seen": there are no fields, no matter and no registers; there are events, in
transit or measured; a Node keeps nothing and handles every entering event by one
generic computation; a single event leaves whole in one direction and does not
spread; the wait is a Port's exit suspended by what is present. The engine below
is the engine of the law of the shadow, which parks, counts and carries what this
law removes ([Highlights coverage](HIGHLIGHTS_IMPLEMENTATION.md)); its rewrite is
the next task, with tests of the code only.

1. **The law of the shadow** (Highlights 5.4, the paragraph "The law of the shadow: only
   shadows and events", the model owner's words of the evening of 2026-09-18; the
   whole document annotated to it on the same day, the consistency table at the end of
   5.4): "No real and shadow. There is only shadow. There are events, which are a whole
   quantum. That is all. The shadow spreads like a ray from the event." Matter is
   content held at Nodes; every ray in flight is a whole quantum spreading by the
   Node's mixing; an event is a whole quantum at held content. It is derived in
   [DERIVATIONS.md](DERIVATIONS.md) round 8 (sections 51 to 56: the law in points S1
   to S10, stability, the step and the speed, inertia, the tests one by one, the
   verdict table, the Node rule in pseudo-code) on round 7's fixed point (sections 45
   to 50). Its engine is the one engine, `src/event_universe/shadow/` (feature 20,
   `field-only-v1`, PR #327) on the substrate of `core/` (bounded integers, the
   board's addresses and headings, the phase tables), a world selected by
   `"law": "shadow"`, with `tests/test_field_only.py`, `tests/test_node_mixing.py` and
   the worlds under `examples/shadow/`. The readings of the day (Highlights 5.4, the
   status line and "One speed, and what is seen"): a quantum passes, like everything,
   at the speed of light between Nodes, all slowness a stay at a Node; the wait is
   the delayed clock and `wait_per_quantum` a declared width like ρ, K and N; the
   three decisions of the morning (`transmitted_number`, the wait's unit, ε_g) are
   not needed and the gate of feature 20b is not written; "the field is, in fact, a
   field of events". The declared widths of "what can be put as a
   parameter, put": `phase_turn` and `quantum` per family (features 21 to 23); light
   turns by its message, uniformly, by default ("constant frequency for light? Yes,
   make it the default for light. That is, per family."), so a world that wants
   light with a frequency declares the family's `quantum`, the photon.
2. **The old engine of the law of the bit was deleted on 2026-09-19** by the model
   owner's decision of the evening ("No confrontations are needed. Only tests that
   everything is as designed."): `core/` but its substrate, `fields/`,
   `dense_field.py`, `prefill.py`, the initialization schema, the catalog, every world
   under `examples/nature/`, the ray viewer and about 1,000 tests; see the
   [migration note](MIGRATION.md#one-engine-on-2026-09-19-the-old-engine-deleted).
   The law of the bit stays recorded in Highlights 5.4 (points 1 to 25 with their
   glossary) with the dated sentences saying how each point reads under the law of
   the shadow, and its confrontation runs of 2026-09-18 stay registered in
   [EXPERIMENTS.md](EXPERIMENTS.md) as measurements on a field that never settles
   (DERIVATIONS.md round 7, Theorem 1), which is what forced the emission and the
   open board. Any state before the deletion can be checked out from git.

**What the new engine already gave on its first worlds** (test_field_only, pinned before
the runs): Gauss's flux through every shell equal to the emission within 2 %, the count
falling as r^-2.00 and the size as r^-1.05, the third law within 2.1 %, the product law,
two slits giving fringes in the counts event by event (ratio 3.2, the one-slit control
monotone), the wait falling as r^-0.9.

**What is open, by whose hand:**

- The model owner's decisions (round 8's verdict table, PR #327's "Needs a decision",
  Highlights 5.4's status line): the law in points S1 to S10 point by point; T2 (an
  event takes its interval); what a matter shadow rotates by, since 2026-09-19 a declared
  rule of the family (`phase_turn`: none for matter, by the quantum for light);
  hypothesis 19 or a per-family w (the bending of light: half of Einstein with one w,
  whole if light pays twice); the Compton table; the parked share's phase (1.5 % of the
  emission stands still); a lamp's recoil; the plain or matched edge. Settled on
  2026-09-19 ("We do not need these three things at all"): the number a transmitted
  quantum carries is the last emitter's, the wait is the delayed clock and
  `wait_per_quantum` stays a declared width of the world like ρ, K and N ("there is
  only a delayed clock"), and there is no gravity multiplier ε_g; the hierarchy of
  section 55 (x) stays an open question of the model, not a parameter.
- Derived and not solved by either law: no inertia for a co-moving pair at first order
  in v (section 54: the lattice's preferred frame for composite matter); no mass ladder
  under the law of the shadow (bound contents give Kepler's continuum; the law of the
  bit had one from loop-binding, hypothesis 12); Bell at most 2 (both laws, section 55
  (ix)); the field of a small content is a haze, not a wave (sections 47 (iii), 52 (v)).
- Research runs to make on the engine when wanted, each with a page, registered in
  EXPERIMENTS.md and not a condition of anything (the owner, 2026-09-19): E11 (one
  held content), A5s (two), A6 (the four tests on an open 33³ board), A1 (a lamp with
  q_γ ≥ 2·10⁶ per quantum), E9. DERIVATIONS.md section 56 gives the worlds and the
  numbers that decide. The GIF renderer went with the old engine.

**How the work is done** ([AGENTS.md](../AGENTS.md)): every model decision is recorded in
Highlights the same day in the owner's words, elaborations flagged; one feature per
branch and PR with one isolated test module; `PYTHONPATH=src python tools/check.py
--base origin/main` locally (the whole suite in CI); merge commits, never a rebase;
experiments registered in EXPERIMENTS.md with their digests; hypotheses numbered in
HYPOTHESES.md; the engine documented in SPATIAL_FIELDS.md (its last section) and its
features in HIGHLIGHTS_IMPLEMENTATION.md; every deletion in MIGRATION.md.

**Everything is in git.** The history is merge commits only; `git log --first-parent
main` reads the day by PRs (#278 to #331 on 2026-09-18 and 19). Any earlier state can be
checked out, the old engine among them at any commit before its deletion.

## What this checkout contains

| Scope | Implemented owner | Contract and limits |
| --- | --- | --- |
| The world file | [world.py](../src/event_universe/shadow/world.py) | `"law": "shadow"`, an open board, K, N, the release, the wait's unit, the families, the held contents with their tables and lamps, the initial shadows; every refusal names its key |
| The engine | [engine.py](../src/event_universe/shadow/engine.py) | `ShadowSimulation(world)`: the held contents, the interval's steps (the events at held content, the wait, the mixing, the releases and the clocks, the steps), the books per family exact at every tick, the readings (`shell_readings`, `cube_flux`, `snapshot_stream`) |
| The layer of one family | [layer.py](../src/event_universe/shadow/layer.py) | Arrivals, parked shares and departures per Node and number as integer arrays; the walk one Link per interval; the wait a hold per Node (`charge_wait`); the escapes booked |
| The Node's mixing | [mixing.py](../src/event_universe/shadow/mixing.py) | `node-mixing-v1`, the remainder rule and the momentum carried, as kernels over the layer's arrays |
| The substrate | [integer.py](../src/event_universe/core/integer.py), [lattice.py](../src/event_universe/core/lattice.py), [phase.py](../src/event_universe/core/phase.py) | Bounded integer primitives; the board's addresses, the six Port headings and the cell bound; the phase circle's tables; integer-only, audited |
| A run and its record | [run.py](../src/event_universe/shadow/run.py), [runner.py](../src/event_universe/runner.py) | `python -m event_universe --init WORLD --output OUT [--ticks N]`, headless; `run.json` with `law` "field-only-v1" |
| Preflight and the workspace | [configuration_validation.py](../src/event_universe/configuration_validation.py), [ui.py](../src/event_universe/ui.py) | A world file checked without a run; the local workspace with the worlds of `examples/shadow/` as templates |
| Standalone vector laboratory | [laboratory guide](../tools/generic_vector_lab/README.md) | Separate research/reference process, not the engine |

The active package lives only in `src/event_universe/`. The old engine's
`Simulation` and `InitialState` were deleted on 2026-09-19 with it; the
historical scalar scheduler, its named research APIs, notebook facade and
frozen archive had been deleted on 2026-09-17; see
[migration](MIGRATION.md#one-engine-on-2026-09-19-the-old-engine-deleted).

## Specifications and gaps

[docs/HIGHLIGHTS.md](HIGHLIGHTS.md) is the high-level specification, edited
directly since 2026-09-17 by the model owner's decision; it is not automatic
evidence of implementation. The Google Doc
[Universe 24 Highlights](https://docs.google.com/document/d/1IkhSyqZZMBSgbJV-PMMwcXG0D_Rlfg4FrLy2jXBMUSs/edit)
is its historical source up to the revision of 2026-09-16 and is neither
edited nor resynced. What the repository implements of it is in
[Highlights coverage](HIGHLIGHTS_IMPLEMENTATION.md), section by section with
the tests; what is open is at the end of that table and in Highlights 5.4 and
5.5. A passing test establishes that the code does what the law says on a
minimal board, not that the law holds in nature; that is the work of the
research runs registered in [EXPERIMENTS.md](EXPERIMENTS.md).

## Resume without a conversation

1. Read [AGENTS.md](../AGENTS.md), inspect local changes, fetch main and record the
   actual base. Use a separate branch/worktree for the task.
2. Use [README installation instructions](../README.md#install-and-run) and the
   interpreter in [.python-version](../.python-version). The minimum package version
   in [pyproject.toml](../pyproject.toml) does not select the shell interpreter.
3. Select an explicit initialization and an unused output directory. The
   [workspace](WORKSPACE.md) changes runtime JSON without rebuilding the engine.
   Visualization is opt-in. Registered outputs expire under [retention](RETENTION.md);
   idle cleanup needs the existing watcher or a scheduled invocation.
4. Follow [CONTRIBUTING.md](../CONTRIBUTING.md), inspect the affected selection from
   `python tools/check.py`, and attach actual results for the submitted tree.
   Use `--full` only for an explicitly justified complete audit.
5. Hand off the scope, validation, limits and integration state through the PR and
   [shared workflow](../skills/workflow.md). A Git rename changes the source fingerprint;
   retain older fingerprints as historical evidence rather than relabeling old runs.

