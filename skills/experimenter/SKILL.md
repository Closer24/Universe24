---
name: experimenter
description: Make a real experiment of the Universe24 model, measured only behind a detector or at an external thing, registered against an expectation written first, and shown on a page; the GameBoard is not measurable by a human.
---

# The experimenter

> **The model owner, 2026-09-20:** "Let there be a special skill for the
> agent that makes real experiments, who always measures behind a detector
> or at an external thing. The GameBoard is not measurable by a human."

This skill is for an agent that asks the model a question it may answer
either way (a series or a numbered run of the
[experiments register](../../docs/EXPERIMENTS.md)). It is not the
[simulation runner](../simulation-runner/SKILL.md), which executes a given
world and inspects its outputs, and it is not a validator of the code: an
experiment changes no law and no source file. Read
[the shared workflow](../workflow.md) and its
[physics comparison method](../workflow.md#physics-comparison-method),
[the law of the ray](../../docs/RAY_LAW.md),
[the engine's bookkeeping](../../docs/ENGINE.md),
[the register's conventions](../../docs/EXPERIMENTS.md) and the records of
the model owner in [Highlights 5.4](../../docs/HIGHLIGHTS.md#54-the-detector).

## The one rule of measurement

A human measures nothing on the GameBoard. The only readings reality has are
the records of the things in the world:

- a **detector**, a set of Nodes with one record (`DetectorSet`; the keys
  `positions`, `threshold`, `reading` with `wave` by default or `beam`, a
  phase window): its clicks, its pointer, the phases and ages of what
  arrived; a face declared open is such a detector;
- an **external thing**, a measured event with a table (a probe with `pass`,
  a star or a source, a lamp, a mirror that re-releases): its `read` records,
  its owed count, its clock, its steps as a body.

A detector learns of a distant Node in two ways only, both the physicists'
own: it receives what the thing there releases by itself, or a lamp shoots
a beam at the thing and the detector reads what comes back or comes through.
A detector keeps nothing of the ray it sent; everything it learns is on the
returning event (its age is the flight time since the re-release, its phase
and number the mirror's). Looking is never free: a paid unit costs the
sender `quantum` x s, and when the thing measures it, its momentum pushes it.

Every number the experiment prints or registers is labelled one of two kinds
([the register](../../docs/EXPERIMENTS.md), "Two kinds of readings"):

| Kind | What it is | What it may be used for |
| --- | --- | --- |
| detector reading | a record of a detector's set or of a measured event in the world | the measurement; every comparison with nature |
| GameBoard reading | the host's view of the deterministic GameBoard: a ray's position, the count or flow at a Node, a body's steps, shell means, the books | the mechanism's description, the bookkeeping checks, the picture |

The readings tool of an experiment reads the engine's own functions
(`NatureBeamSimulation`, `parse_nature_beam_world`, `read_arrivals`, `unit_label`,
`flight_table`, `by_clock`, `DetectorSet`, `Measured.charge`); it never
replays a rule of the engine, and it prints the kind of every line.

## What an experiment is

1. **The question**, in the model owner's words, and the expectation written
   before any run: the numbers or the shape expected, the brackets, and
   what would count against the model. Nothing is tuned after the run; a
   number that falls outside its bracket is registered outside.
2. **The world**: a world file under `examples/events/<series>/` with a
   generator, declaring every thing the reading needs: the detectors (a
   set per reading), the probes (measured events with `pass` on whole
   shells where a field is read, since one Node reads its line's beam and
   the shell mean is the law's reading), the lamps, the stars. A missing
   feature of the law is a finding to register, never a change to `src/`.
3. **The runs**: headless, through `NatureBeamSimulation(parse_nature_beam_world(world),
   record)` or the runner, the books balanced at every interval, the source
   fingerprint recorded, a few minutes per world at most.
4. **The readings tool** under `tools/<series>_readings.py`, as above, with
   one fast test on a tiny case that pins the tool to the engine's function.
5. **The register entry** in [EXPERIMENTS](../../docs/EXPERIMENTS.md) and
   the [validation log](../../docs/VALIDATION.md): expected against measured,
   inside or outside, none moved, the kind of each reading, the fingerprint,
   what the law lacked; a README beside the worlds saying how to re-run.
6. **The page** for the model owner, in the scratchpad, per the page
   contract of the [simulation runner](../simulation-runner/SKILL.md): the
   GameBoard drawn with an icon and the world-file name for each thing on
   it (an atom is its proton and its electron's set; a detector appears
   only where the world declares one), "Why it was tested", the moving
   picture inside the page, the readings, "The conclusion". Boss publishes
   it.

## What the experimenter never does

- Never reads the dense arrays of the GameBoard as a measurement, and never
  compares a GameBoard reading with nature.
- Never edits `src/`, `docs/HIGHLIGHTS.md` or the law's documents; never
  pushes or opens a pull request; commits in its own worktree.
- Never pins an example world's numbers in a test; never tunes a world to
  its expectation; never smooths a failed run.
- Never introduces `Site` or a wave at a Node: on the GameBoard there are
  only events; what is called a ray is the record of an event in transit.

## Hand back

The commit hashes, the design choices (families, GameBoard, detectors, probes,
lamps), the table expected against measured with the kind of each reading,
the verdict in plain words, the path of the page and its GIF, and what the
law lacked.
