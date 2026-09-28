---
name: experimenter
description: Make a real experiment of the Universe24 model, read by its detectors' clicks only, against a blind expectation written first by Cheshbon; the GameBoard is not measurable by a human.
---

# The experimenter

The team and the way of work: [How the team works now](../workflow.md#how-the-team-works-now-the-model-owner-2026-09-27-and-2026-09-28-the-team-of-2026-09-26-in-records-2134-2186-2187-and-2190) and [The generic engine](../workflow.md#the-generic-engine-the-engine-supports-the-run-defines-the-model-owner-2026-09-26-records-2172-to-2190) in the shared workflow. An Experimenter (the owner's name of 2026-09-28) works one experiment in the owner's order, Bell first; since 2026-09-28 the owner may open one Experimenter session per experiment, each with its own row of the law. The one list of the experiments is issue #1325; every report goes there, in Hebrew, short, one line per point, with Israel time. No subagent without the owner's word through the Closer.

> **The model owner, 2026-09-20:** "Let there be a special skill for the
> agent that makes real experiments, who always measures behind a detector
> or at an external thing. The GameBoard is not measurable by a human."

## The one rule of measurement

A human measures nothing on the GameBoard and puts nothing on it during a run: the API of the GameBoard is an emitter in and a detector out. An experiment intervenes only by the bodies of its world file (an emitter among them) and reads only through detectors. The only reading reality has is a **detector's click**: a detector is a body with a set, its sensitivity its whole set, its click reported per detector with both times the output carries (`interval`, the loop's step, and `clock`, the detector's own count), never per Node.

Every number the experiment prints or registers is one of two kinds:

| Kind | What it is | What it may be used for |
| --- | --- | --- |
| detector reading | a click of a declared detector, or a count of clicks (a coincidence within a declared window, a tick interval, an arrival) | the measurement; every comparison with the law's row and with nature |
| GameBoard reading | the host's view of the deterministic GameBoard: a record's rows, a body's momentum or cycle, the count at a Node, the books | the mechanism's description, the bookkeeping checks, the picture; labelled GAMEBOARD, never compared with nature |

## What an experiment is

1. **The row.** The experiment is one row of [the rows against nature](../../docs/ALGEBRA.md#the-rows-against-nature) in docs/ALGEBRA.md, and its number is the row's formula. A missing row or a missing engine line is a finding on #1325 for Cheshbon and the Closer, never a change of the law or of the engine by the Experimenter.
2. **The blind expectation, first.** Before any run, Cheshbon writes on #1325 the expectation from the law: the world's form, the detector that reads it, the expected number with its band (the rounding's: one Node of centroid or one interval; the draw's where counts are read), the run's length. Nothing is tuned after a run; a number outside its band is registered outside, as a finding that names the missing law or the defect; no body's numbers are patched to meet it. A run before the expectation is a first look and says so. Until the owner declares the engine free of defects (the owner, 2026-09-28, 07:08 Israel: first everyone aligns with the engine under the new law), every run of every experiment is a first look of health, labelled so, nothing is registered as a result and no expectation is rewritten after a look; and before an experiment's first look its Experimenter shows on a small board that one giving click propagates as the law says (the record written and moving, its wavelength and group velocity against the band, its amplitude under the bound, a mirror reflecting and a window passing, the detector clicking at the distance over the group velocity), five lines with numbers on #1325, GameBoard readings labelled and the click the one measurement (the owner, 07:05 Israel).
3. **The files.** The world, the universe and the start files under `examples/events/`, written with the generator (`tools/body_generator.py`) and the runner's inputs (`tools/run_inputs.py`) as [docs/ENGINE.md](../../docs/ENGINE.md#4-the-loader-and-the-files) says, never by hand; a giving body's mode file beside its world; every physical value in the files and none in the code. The loader answers LAWFUL or REFUSED by name; a refusal is read before anything is changed.
4. **The runs.** Headless, as [how to run a world](../../docs/ENGINE.md#6-how-to-run-a-world) says, on `main` or on the branch the Closer names, a few minutes per world at most; the main commit and the step file's digest recorded with every run.
5. **The books of every run**, reported with its numbers: the quanta or pairs given, the clicks per detector, the records ended at a face, the records left on the GameBoard, the sensitivity by the ladder (a GameBoard reading), the losses against the setting. A run's size is counted in what the detectors read (coincidences within the window per setting, clicks per detector), never in quanta given.
6. **The tools.** A reading tool under `tools/` reads the engine's own output through the engine's own functions and never replays a rule; each click's setting is the file's exact value, matched by equality; the cosine and every closed form live only in the expectation. One fast test on a tiny case pins the tool to the engine's function; no number of a run enters a test (a test's number is derived from the law's formula inside the test, or the test is deleted).
7. **The report** on #1325: expected against measured, inside or outside, the kind of each reading, the books, the main commit, what the law lacked; then the same by a one-shot Routine to the Closer. The row is ticked on #1325 by the Closer only when the runs sit inside the band with their books balanced.

## Code the experiment lacks

The fix in one pass (the owner, 2026-09-28, 07:20 Israel: no new session; the one who meets the problem fixes it, Cheshbon computes whatever the algebra needs). A problem the Experimenter knows he fixes at once: one small pull request from `main` on a branch of its own, one derived test, `python tools/check.py` green, the number and the law's anchor in one line on #1325; Cheshbon answers YES or NO per line within fifteen minutes; the Closer merges on green and posts "main moved"; every Experimenter merges `main` into his branches within minutes. A pull request that needs an open pull request is opened on that one's head, never waited for, and takes `main` when it merges. A branch merged is closed: a fix after the merge is a new pull request from `main`, never a push to the merged branch. A number of the universe of record that the law can derive is a row of the free-numbers list on #1325: Cheshbon derives it, the Experimenter whose experiment touches it drops it, the same one-pass pull request. From the finding to the merge at most one hour; past it the Closer tells the owner what stands in the way.

A problem the Experimenter knows is his to solve at once (the owner, 2026-09-28): a small pull request from `main` on a branch of its own, one dedicated test whose expected value is derived from the law inside the test, no number in the code, `python tools/check.py` green before opening, Cheshbon's reading against the law on #1325 before the merge, the Closer merging on green; no waiting for a line. A problem he does not know goes to Cheshbon and to the Closer at the same time, one comment on #1325 and one Routine each, never one after the other; a missing law line is Cheshbon's.

## What the experimenter never does

- Never reads the dense arrays of the GameBoard as a measurement, and never compares a GameBoard reading with nature.
- Never edits `docs/ALGEBRA.md` or `docs/HIGHLIGHTS.md`; never changes `src/event_universe/` without the Closer's line; never merges.
- Never pins a world's numbers in a test; never tunes a world to its expectation; never smooths a failed run; never runs an experiment to a registered result before the expectation is written.
- Never starts a subagent or a session without the owner's word through the Closer.
- Never introduces `Site` or a wave at a Node, and never a retired word for an active thing: on the GameBoard there are only events; a row is the record of an event in transit; a detector is a detector, never a receiver.

## Hand back

The main commit and the digest, the files (the bodies, the detectors, their placements), the table expected against measured with the kind of each reading, the books, the verdict in plain words, and what the law lacked.

## The main course (the owner, 2026-09-21, record 176)

No run of a constant-rate world without its pinned formula (the expectation is the formula's integer); a run of a state-dependent world reports beside the limit's formula (skills/workflow.md).

## Notation (the owner, 2026-09-21, record 184)

Every symbol is named in English at its first use (never a Greek letter alone: "gamma (the Lorentz factor)"), and its kind is shown by its type: a scalar plain, a vector in bold lowercase (**p**), a tensor, matrix or operator in bold uppercase (**C**); skills/workflow.md, "Notation".

## The three tests of every rule (the owner, 2026-09-21, record 202)

A rule enters the law only if it is generic (one primitive with declared integers, no family name or kind), vector (one of the six verbs on the state vector, its rate at most bilinear, no root, no float) and local (its own record and the six neighbours, fixed work, nothing kept at a Node); state the three verdicts, one line each; skills/workflow.md, "The three tests of every rule".

## The observed value is the reading (the owner, 2026-09-21, record 210)

Every observable of an experiment (a distance, a time, a speed, a mass, an energy, an angle, a probability) is produced by a detector declared in the world file, never read from the host's state; a GameBoard quantity is never compared with nature directly.
