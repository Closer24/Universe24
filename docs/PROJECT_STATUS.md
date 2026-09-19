# Project status and restart guide

## Where the project stands on 2026-09-19 (read this first)

**One engine: the law of the ray.** This description is a snapshot of the
branch `claude/universe24-new-3ytqde` at the commits that implemented
[the law of the ray](RAY_LAW.md) on the base `ce0b22af`. Read current Git and
the linked Issue/PR before treating it as live status.

1. **The law of the ray** (Highlights 5.4, "DECIDED: the law of the ray",
   the model owner, 2026-09-19; the design published in
   [RAY_LAW.md](RAY_LAW.md) before the engine changed): the Node holds no
   wave; a unit is a ray with a record (`NatureBeam`: Node, direction, age,
   phase, number, amount, content) moving along the digital line of its
   momentum at one speed for every direction, 1 / sqrt 3 (the flight
   table); rays that meet at a Node are permuted by the eight-slot collision
   table, a bijection inside its invariant classes; the interval is a
   bijection and the click its only one-way border; the interference is the
   squared coherent record a detector reads of the rays it clicked; the
   ray's law is one generic function, `nature_beam`, and every piece of
   logic exists once (one reading of the Node, `read_arrivals`, its
   components selected by the coupling's declared key). Its engine is the
   one engine, `src/event_universe/events/` (`rays-v1`) on the substrate of
   `core/`, a world selected by `"law": "rays"`, with the ten `tests/test_ray_*.py`
   modules and the worlds under `examples/events/`
   ([the engine's bookkeeping](ENGINE.md), [coverage](HIGHLIGHTS_IMPLEMENTATION.md),
   [expectations](TEST_EXPECTATIONS.md)).
2. **The engines before it are deleted, on 2026-09-19:** the law of the bit
   in the morning, the law of the shadow (`field-only-v1`) in the evening,
   and the law of events (`events-v1`, with the coherent sum at the Node,
   the sides, the scatter, the suspension of a bundle and the
   `reversible-detector-v1` candidate) in the night; see the
   [migration notes](MIGRATION.md#the-law-of-the-ray-on-2026-09-19-rays-v1).
   Every rule the ray law keeps (the clock, the tables, the phase window,
   the release priced by the turn, the face detectors, the refused step,
   the one reading set, the count off the clock) is re-pinned in the new
   modules. Any state before a deletion can be checked out from git.

**What the engine gave on its first worlds** (`test_ray_worlds`, and the
re-registered runs in [EXPERIMENTS.md](EXPERIMENTS.md)): the content of a
measured event at rest constant at every tick; six ballistic beams with
Gauss's flux through every cube equal to the emission exactly once the front
has passed; the two slits fringing in the record at lambda = period / sqrt 3
(the correlation with the two-source cosine 0.893) and not in the count;
Bell S = 2 and S' = 3/2 exactly with no-signalling exact; the equivalence and
the superposition identities exact, the third law to the grain of the whole
apportioning (5.9e-6), the front at the flight table's tick with the whole
amount; the far-field ring means following the lattice ring's Node count
(registered outside the design's ±10 % expectation) and the clock on a
beam's axis frozen after the front (the design's accepted price). The
performance: 0.23 to 1.0 us per Node per interval on the registered worlds
(the design's budget 3.6 us).

**What is open, by whose hand:**

- The model owner's: a decay as a table on a measured event; the mass ladder
  under this law; the value of ρ and of the suspension's width; polarization
  as worlds and tables; whether the six-heading source of the coupling
  series should release on a fan of directions (the design's section 8
  expects the ring means of a fan, 0.31 to 0.33, and the six beams give the
  lattice ring's count); **the magnitude of a fan ray's label**: the
  label is content x amount x D with D the integer direction, so equal
  amounts on (1, 0, 0) and (7, 5, 0) carry the momenta 1 and sqrt 74 and
  a fan source pushes its mean |D| times harder than six headings
  ([RAY_LAW section 10](RAY_LAW.md#10-implementation-notes-2026-09-19-the-implementation),
  note 21; the orbit series D re-registered the night of 2026-09-19 under
  the one push form with p re-derived for the fan's mean |D| = 5.19: no
  orbit closes at any width), and whether the label should be along the
  unit vector of the direction at the flight table's scale Q = 64 (one
  table for the flight and the label), which the implementation
  recommends the owner rule on; after that, whether to pre-fill the field,
  to widen the push further or to read the count off the clock as well
  ([D, the orbit](EXPERIMENTS.md#d-the-orbit-under-the-law-of-the-ray-on-the-plane-2026-09-19)).
- Derived and not solved: no inertia for a co-moving pair at first order in v
  (DERIVATIONS.md section 54); Bell at most 2; a single ray does not
  interfere with itself, interference being the record of many of one
  number.
- Research runs to make on the engine when wanted, each with a page,
  registered in [EXPERIMENTS.md](EXPERIMENTS.md) and not a condition of
  anything.

**How the work is done** ([AGENTS.md](../AGENTS.md)): every model decision is
recorded in Highlights the same day in the owner's words, elaborations flagged;
one feature per branch and PR with one isolated test module; `PYTHONPATH=src
python tools/check.py --base origin/main` locally and the affected-check selector
in CI under current CONTRIBUTING.md; merge
commits, never a rebase; experiments registered in EXPERIMENTS.md with their
digests; hypotheses numbered in HYPOTHESES.md; the law documented in
RAY_LAW.md, its bookkeeping in ENGINE.md and its coverage in
HIGHLIGHTS_IMPLEMENTATION.md; every deletion in MIGRATION.md.

**Everything is in git.** The history is merge commits only; `git log
--first-parent main` reads the days by PRs. Any earlier state can be checked
out, the engines before this one among them.

## What this checkout contains

| Scope | Implemented owner | Contract and limits |
| --- | --- | --- |
| The world file and its refusals | `src/event_universe/events/world.py` | [RAY_LAW.md](RAY_LAW.md), section 2; [ENGINE.md](ENGINE.md), "The world" |
| The law: the record, the reading, the tables, the store, the interval | `src/event_universe/events/nature_beam.py` | [RAY_LAW.md](RAY_LAW.md), sections 3 to 5; [TEST_EXPECTATIONS.md](TEST_EXPECTATIONS.md) |
| The frame: the clocks, the steps, the books, the readings, the inverse | `src/event_universe/events/engine.py`, `measured.py` | [ENGINE.md](ENGINE.md), "The frame", "The books" |
| The record of a run | `src/event_universe/events/run.py`, `snapshot_writer.py`, `runner.py` | [ENGINE.md](ENGINE.md), "The record" |
| The substrate | `src/event_universe/core/` | Bounded integers (`by_clock`, `apportion_whole`, `integer_root`), the board's addresses and headings, the phase tables; the integer audit |
| The preflight and the workspace | `configuration_validation.py`, `ui.py` | [ENGINE.md](ENGINE.md), "Preflight"; [WORKSPACE.md](WORKSPACE.md) |
| The entity definitions | `world_loading.py` | [ENTITY_DEFINITIONS.md](ENTITY_DEFINITIONS.md) |
| Generated output | `retention.py` | [RETENTION.md](RETENTION.md) |
| The check | `tools/check.py` | [CONTRIBUTING.md](../CONTRIBUTING.md) |

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
