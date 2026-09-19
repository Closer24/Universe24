# Project status and restart guide

## Where the project stands on 2026-09-19 (read this first)

**One law, one engine.** Everything below is on `main`; nothing is in a branch
or a machine.

1. **The law of events** (Highlights 5.4, the paragraphs "The law of events"
   and "The principles of the law of events", the model owner's words of
   2026-09-19; the whole document annotated to it the same day, a reading note
   at its head): "There is no shadow, no real. There are only events on the
   event board. There are detectors by sensitivity. That is it. Everything must
   be generic in the engine, without registers. There are no draws. There are
   only opening events that spread by the physics of the engine." One thing,
   the event, with its record (amount, phase, number, momentum from birth,
   heading, its counts); at every interval every event is created at its next
   place, one of seven, a neighbour or here; a measured event is created here
   without end and its clock is the count of its self-creations ("every clock
   tick there is self-creation, that is, no transfer to the next Port"); a
   single quantum goes whole in one direction, by its momentum ("By the
   momentum"), and does not turn ("Correct, an event does not turn"); the
   suspension is a count the event carries ("The event carries it; note that
   the next event is delayed"); no return to the source; a detector states its
   sensitivity, "and that is exactly the uncertainty principle". Its engine is
   the one engine, `src/event_universe/events/` (`events-v1`) on the substrate
   of `core/`, a world selected by `"law": "events"`, with the tests
   `test_node_mixing`, `test_node_mixing_numbers`, `test_event_transit`,
   `test_event_suspension`,
   `test_event_clock` and `test_event_worlds` and the worlds under
   `examples/events/` ([the engine](ENGINE.md), [coverage](HIGHLIGHTS_IMPLEMENTATION.md)).
2. **The engines before it are deleted, on 2026-09-19:** the old engine of the
   law of the bit in the morning ("No confrontations are needed. Only tests that
   everything is as designed.") and the engine of the law of the shadow
   (`field-only-v1`, 2026-09-18 to 2026-09-19) in the evening, with what it
   kept that the law of events removes: the parked ninths, the wait as a hold,
   the remainders, the register of `quantum`, the phase turn in flight; see the
   [migration notes](MIGRATION.md). The law of the bit and the law of the
   shadow stay recorded in Highlights 5.4 with the dated sentences saying how
   each rule reads under the law of events. Any state before a deletion can be
   checked out from git.

**What the engine gave on its first worlds** (`test_event_worlds`, pinned from
the first readings): the content of a measured event at rest constant at every
tick, Gauss's flux through every closed surface equal to the emission within
1 %, the escape 0.989 of the emission (nothing stands), the count falling as
r^-2.03 and the size as r^-0.95, the third law within 5 %, the product law within
6 %, two openings giving a minimum and a maximum on the detector with the
one-opening control monotone.

**What is open, by whose hand:**

- The model owner's: a decay as a table on a measured event; the mass ladder
  under this law; the value of ρ and of the suspension's width. Decided the
  same day: a detector's threshold gates every response of its Nodes,
  receivers and re-emitters alike (`test_detector_sensitivity`); `phase_window`
  approved as a declared width of a detector and of a lamp, the setting of the
  Bell run (Highlights 5.4), its feature with its isolated test and the run of
  A2 on a small board pending, the run designed by the physicist and the
  mathematician.
- Derived and not solved: no inertia for a co-moving pair at first order in v
  (DERIVATIONS.md section 54); Bell at most 2; a single quantum does not
  interfere with itself, interference being of many of one number.
- Research runs to make on the engine when wanted, each with a page, registered
  in [EXPERIMENTS.md](EXPERIMENTS.md) and not a condition of anything.

**How the work is done** ([AGENTS.md](../AGENTS.md)): every model decision is
recorded in Highlights the same day in the owner's words, elaborations flagged;
one feature per branch and PR with one isolated test module; `PYTHONPATH=src
python tools/check.py --base origin/main` locally (the whole suite in CI); merge
commits, never a rebase; experiments registered in EXPERIMENTS.md with their
digests; hypotheses numbered in HYPOTHESES.md; the engine documented in
ENGINE.md and its coverage in HIGHLIGHTS_IMPLEMENTATION.md; every deletion in
MIGRATION.md.

**Everything is in git.** The history is merge commits only; `git log
--first-parent main` reads the days by PRs. Any earlier state can be checked
out, the engines before this one among them.

## What this checkout contains

| Scope | Implemented owner | Contract and limits |
| --- | --- | --- |
| The world file and its refusals | `src/event_universe/events/world.py` | [ENGINE.md](ENGINE.md), "The world" |
| The interval, the measured events, the books | `src/event_universe/events/engine.py` | [ENGINE.md](ENGINE.md), "The interval", "The push", "The books" |
| The events in transit and the sides | `src/event_universe/events/transit.py`, `mixing.py` | [ENGINE.md](ENGINE.md); [TEST_EXPECTATIONS.md](TEST_EXPECTATIONS.md) |
| The record of a run | `src/event_universe/events/run.py`, `snapshot_writer.py`, `runner.py` | [ENGINE.md](ENGINE.md), "The record" |
| The substrate | `src/event_universe/core/` | Bounded integers, the board's addresses and headings, the phase tables; the integer audit |
| The preflight and the workspace | `configuration_validation.py`, `ui.py` | [ENGINE.md](ENGINE.md), "Preflight"; [WORKSPACE.md](WORKSPACE.md) |
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

