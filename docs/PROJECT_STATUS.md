# Project status and restart guide

## Where the project stands on 2026-09-20 (read this first)

**Update of 2026-09-24, 11:58Z (the Boss, record 1806 of docs/LOG_2026-09-20.md).** On the
model owner's word every agent session is stopped and closed until a plan is reached with the
physicist and presented to him: one list of the experiments we want to support, one engine on
main, no building of worlds, the engine stabilised until a freeze on one commit, no pin runs
until then, one GO on his word, the paper submitted only when everything is stable. The live
state (open pull requests, the branches with unmerged work, the declaration defects found and
not yet fixed, the three idle sessions holding unpushed engine work) is record 1806; the owner's
decisions of the day are in docs/HIGHLIGHTS.md section 5.4 and the GO status page is
docs/designs/detector_law/GO_STATUS_2026-09-24.md.

This is a snapshot of `claude/universe24-new-3ytqde` at the pull request
that carries the day's work to `main`; read current Git, the linked issues
and pull requests, and [Highlights 5.4](HIGHLIGHTS.md#54-the-detector) (the
record "The day of 2026-09-20 in summary") before treating it as live status.

1. **One law, one engine, one name per thing.** The Beam Law (`beam-v1`,
   [BEAM_LAW.md](BEAM_LAW.md), a world selected by `"law": "beam"`) runs in
   `src/event_universe/events/`; the record in transit is `NatureBeam`, the
   lattice is the GameBoard everywhere, the glossary of Highlights 5.6 names
   each thing once. Every reading is a moment of the events that reach a
   set in one interval; every rate is the whole part off an age (`by_clock`);
   the collision is a table permutation; the click is the one one-way border.
2. **The four forces on the GameBoard as one mechanism.** The push is one
   signed inner product over declared columns per unit of content (gravity
   the universal column, `charge`, `strong`), the range of a column its
   family's lifetime `L` (an escape click at L), the contact through the
   table at one Link. Series I (the nucleus) is registered; the weak force
   (`become`, `phase_width`, D-1) is in flight in its own pull request.
3. **The detector is all there is to measure.** A `DetectorSet` with one
   record, a threshold on the coherent pointer's square under `wave`, a
   phase window, the two kinds of readings (detector / GameBoard) on every
   registered line, the experimenter's skill (`skills/experimenter/SKILL.md`:
   a human measures nothing on the GameBoard; an emitter in, a detector out).
4. **What the law predicts and where it fails, measured:** Newton's
   identities, Gauss, the third law, the clock's redshift (E), the Hubble
   diagram coasting (G), Bohr's orbit closed under the step drive but not
   quantised (H: the orbit at r = 8 stable for the run, the phase's turn
   per orbit 0.75 to 0.83 against 0 and C(4) = 1.01 against 2.0), light
   neither bent nor delayed (K; the meeting `meeting-v1` in flight makes it
   bend as a report),
   the nucleus (I), Heisenberg in the record (A10), no single-click build-up
   (A10 at a low rate), Bell S = 2 with no-signalling exact (A2; #363 in
   flight reads the settings from distant events). Each is stated in
   [HYPOTHESES.md](HYPOTHESES.md) so that it can fail and registered in
   [EXPERIMENTS.md](EXPERIMENTS.md) with the expectation before the run.
5. **Decided and recorded (Highlights 5.4):** an event is a number at one
   place with a phase (option 1); no draw, no register, no memory at the
   detector; the click the only one-way border; the meeting as a report;
   the old-engine issues mapped to their live targets.

## Where the project stood on 2026-09-19 (history)

**One engine: the Beam Law.** This description is a snapshot of the
branch `claude/universe24-new-3ytqde` at the commits that implemented
[the Beam Law](BEAM_LAW.md) on the base `ce0b22af`. Read current Git and
the linked Issue/PR before treating it as live status.

1. **The Beam Law** (Highlights 5.4, "DECIDED: the law of the ray",
   the model owner, 2026-09-19; the design published in
   [BEAM_LAW.md](BEAM_LAW.md) before the engine changed): the Node holds no
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
   one engine, `src/event_universe/events/` (`beam-v1`) on the substrate of
   `core/`, a world selected by `"law": "beam"`, with the ten `tests/test_nature_beam_*.py`
   modules and the worlds under `examples/events/`
   ([the engine's bookkeeping](ENGINE.md), [coverage](HIGHLIGHTS_IMPLEMENTATION.md),
   [expectations](TEST_EXPECTATIONS.md)).
2. **The engines before it are deleted, on 2026-09-19:** the law of the bit
   in the morning, the law of the shadow (`field-only-v1`) in the evening,
   and the law of events (`events-v1`, with the coherent sum at the Node,
   the sides, the scatter, the suspension of a bundle and the
   `reversible-detector-v1` candidate) in the night; see the
   [migration notes](MIGRATION.md#the-law-of-the-ray-on-2026-09-19-rays-v1).
   Every rule the Beam Law keeps (the clock, the tables, the phase window,
   the release priced by the turn, the face detectors, the refused step,
   the one reading set, the count off the clock) is re-pinned in the new
   modules. Any state before a deletion can be checked out from git.

**What the engine gave on its first worlds** (`test_nature_beam_worlds`, and the
re-registered runs in [EXPERIMENTS.md](EXPERIMENTS.md)): the content of a
measured event at rest constant at every tick; six ballistic beams with
Gauss's flux through every cube equal to the emission exactly once the front
has passed; the two slits fringing in the record at lambda = period / sqrt 3
(the correlation with the two-source cosine 0.893) and not in the count;
Bell S = 2 and S' = 3/2 exactly with no-signalling exact; the equivalence and
the superposition identities exact, the third law to the grain of the whole
apportioning (5.9e-6), the front at the flight table's tick with the whole
amount; the far-field ring means following the GameBoard ring's Node count
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
  GameBoard ring's count); the orbit series D under the step drive
  (2026-09-20, record 117: the S = 32 probe at r = 24 closes by the
  criterion, T 623 against the derived 687, the mean radius 23.63, C 1.37
  against the ring mean's 1; its second turn returns (-14, +1); r = 12
  closes the angle twice and not by the criterion): whether to release
  the field continuously rather than in shells (the precession), to widen
  the push further, or to pre-fill the field; 'to read the count off the
  clock as well' is settled by the drive (record 108)
  ([D, the orbit](EXPERIMENTS.md#d-the-orbit-under-the-beam-law-on-the-plane-2026-09-19)).
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
BEAM_LAW.md, its bookkeeping in ENGINE.md and its coverage in
HIGHLIGHTS_IMPLEMENTATION.md; every deletion in MIGRATION.md.

**Everything is in git.** The history is merge commits only; `git log
--first-parent main` reads the days by PRs. Any earlier state can be checked
out, the engines before this one among them.

## What this checkout contains

| Scope | Implemented owner | Contract and limits |
| --- | --- | --- |
| The world file and its refusals | `src/event_universe/events/world.py` | [BEAM_LAW.md](BEAM_LAW.md), section 2; [ENGINE.md](ENGINE.md), "The world" |
| The law: the record, the reading, the tables, the store, the interval | `src/event_universe/events/nature_beam.py` | [BEAM_LAW.md](BEAM_LAW.md), sections 3 to 5; [TEST_EXPECTATIONS.md](TEST_EXPECTATIONS.md) |
| The frame: the clocks, the steps, the books, the readings, the inverse | `src/event_universe/events/engine.py`, `measured.py` | [ENGINE.md](ENGINE.md), "The frame", "The books" |
| The record of a run | `src/event_universe/events/run.py`, `snapshot_writer.py`, `runner.py` | [ENGINE.md](ENGINE.md), "The record" |
| The substrate | `src/event_universe/core/` | Bounded integers (`by_clock`, `apportion_whole`, `integer_root`), the GameBoard's addresses and headings, the phase tables; the integer audit |
| The preflight | `configuration_validation.py` | [ENGINE.md](ENGINE.md), "Preflight" |
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
minimal GameBoard, not that the law holds in nature; that is the work of the
research runs registered in [EXPERIMENTS.md](EXPERIMENTS.md).

## Resume without a conversation

1. Read [AGENTS.md](../AGENTS.md), inspect local changes, fetch main and record the
   actual base. Use a separate branch/worktree for the task.
2. Use [README installation instructions](../README.md#install-and-run) and the
   interpreter in [.python-version](../.python-version). The minimum package version
   in [pyproject.toml](../pyproject.toml) does not select the shell interpreter.
3. Select an explicit initialization and an unused output directory.
   Visualization is opt-in. Registered outputs expire under [retention](RETENTION.md);
   idle cleanup needs the existing watcher or a scheduled invocation.
4. Follow [CONTRIBUTING.md](../CONTRIBUTING.md), inspect the affected selection from
   `python tools/check.py`, and attach actual results for the submitted tree.
   Use `--full` only for an explicitly justified complete audit.
5. Hand off the scope, validation, limits and integration state through the PR and
   [shared workflow](../skills/workflow.md). A Git rename changes the source fingerprint;
   retain older fingerprints as historical evidence rather than relabeling old runs.
