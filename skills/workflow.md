# The shared way of working

The team is two sessions and the owner (the owner, 2026-09-30). The Boss leads,
decides within the owner's words, records his decisions and runs the workers;
its card is [the Boss's card](boss-orchestrator/SKILL.md). The advisor answers
from the current documents, judges every line by its status, computes the blind
numbers and writes nothing; its card is [the advisor's card](advisor/SKILL.md).
The owner decides. This file is what the two sessions share. A skill is an
instruction, not a grant of permission: the user's scope binds every session.

## Repository knowledge and restart

Start from the current checkout, never from a previous conversation. Read
[AGENTS.md](../AGENTS.md) first, then only the part of the three documents the
task needs. One definition per concept: a skill links to the law and never copies
it. Temporary state (the task in hand, a blocked check, the next action) lives on
the GitHub issue or the pull request, never in a skill.

## The three documents only (the owner, 2026-09-26 and 2026-09-30)

The project keeps three current documents, the skills and the entry files, and
nothing else:

| Document | What it holds |
| --- | --- |
| [docs/ALGEBRA.md](../docs/ALGEBRA.md), the law | One algebraic line per rule, the families, the bodies, the clicks, every experiment's formula and blind expectation, every hypothesis under its own name |
| [docs/ENGINE.md](../docs/ENGINE.md), the engine | The engine as the code holds it on `main`: the words, the interval, the folders, the loader, the output, the gates, how to run a world |
| [docs/HIGHLIGHTS.md](../docs/HIGHLIGHTS.md), the decisions | The decisions in force, one line each; a decision of the owner replaces the line it changes |

The skills are this file and the two role cards. The entry files are README.md,
AGENTS.md and CONTRIBUTING.md. No log, no status page and no fourth document.

## The documents rule (the owner, 2026-09-30)

HIGHLIGHTS.md is updated at once, with the owner's word, so that it always states
where the project is. ALGEBRA.md is updated when the law or its numbers change.
Every hypothesis is declared under its own name, outside the law, until it passes
the three tests or the owner admits it. A change to a document replaces what it
touches and deletes what no longer holds in the same pull request; the body names
what was deleted. No history note, record number or superseded line stays: git
keeps the history. Nothing is a decision until it is in HIGHLIGHTS.md.

## The three tests of every rule: generic, vector, local (the owner, 2026-09-21)

A rule enters the law only if it passes all three. Both sessions apply them: the
advisor when judging a line, the Boss when briefing a build.

1. **Generic.** One primitive with declared integers and no family name or kind;
   the same primitive serves every family; its special cases are values, not
   branches; the engine branches on no name.
2. **Vector.** One of the six verbs on the state vector; its rate at most
   bilinear in the state; no root, no float, no rounding at run time beyond the
   ones declared at load.
3. **Local.** It reads only its own record and the six neighbouring Nodes; fixed
   work and storage; nothing kept at a Node beyond the law's own numbers.

A rule that fails one test does not enter the law. A hypothesis that needs more
is stated under its own name, outside the law. The three verdicts are stated,
one line each, in every brief, answer and pull request. Every new rule is sought
first in its generic vector form, dimension-free and world-free, and only then in
its integer form and its declaration per world (the owner, 2026-09-21).

## The six verbs

Every integer of the law is made of six operations only: the translation of an
accumulator by its rate, the bilinear form with a declared matrix, the group-ring
addition, the permutation, the evaluation at the primitive root of unity, and the
Euclidean division with the remainder kept. A root, a true division or a draw is
outside the law.

## No number in the engine or the generator (the owner, 2026-09-26 to 2026-09-28)

The engine and the generator hold no number, no formula, no family name and no
flag. Every physical value comes from the run's files; a scale that is no physics
is derived from the integer width, never written. Every primitive is one folder
found by its name. A gate counts the numeric literals and the family names in the
code, and the count may only fall.

## The blind number first (the owner, 2026-09-21 and 2026-09-28)

Whatever can be computed algebraically is computed algebraically. Before any run
the advisor computes the expected number from the engine's own lines, with its
band, and the Boss writes it in the brief. The run's reading is compared with
that number. A difference is a defect of the engine and never a finding: the
engine implements the law and nothing else, so what differs is fixed. A number
outside its band with no defect found names the missing law, as a hypothesis
under its own name. No expectation is rewritten after a look, and no body's
number is tuned to a result.

Only a detector's click is a measurement. Every number reported is labelled
DETECTOR or GAMEBOARD; a GameBoard reading is a diagnostic, never compared with
nature and never a result on its own.

## Names with meaning, never codes (the owner, 2026-09-24 and 2026-09-25)

Every experiment, rule, folder and file is called by its plain name: "the two
slits", "the moving lamp's redshift", "the signed read". No code letter or
number stands for a thing, not even in parentheses after its name. A block is
named by what it is on the GameBoard (an emitter, a body, a detector, a clock);
the laboratory's word for it may be said once to explain what it models. A new
word enters the words of docs/ENGINE.md with its one definition before it is
used; a word already taken is not reused.

## Notation: every symbol named, its kind shown (the owner, 2026-09-21)

Every symbol is named in English at its first use, so that the owner can type
and search it: "gamma (the Lorentz factor)", "c (the level of the family of
clicks)". A Greek letter never stands alone. The kind of a quantity is shown by
its type: a scalar plain (`c`, `Gamma`), a vector in bold lowercase (**p** the
momentum vector), a matrix, a tensor or an operator in bold uppercase (**C** the
coupling matrix). A component of a vector is a scalar and is written plain with
its index (`p_x`). In code the identifier's name says the kind where it matters.

## Short sentences, one idea each (the owner, 2026-09-25)

Every message, answer, brief and report is written in short sentences, one idea
each, the central ideas first. Short lists where there are several items. A
question, if there is one, on its own line at the end. The repository's documents
keep their own form.

## The six lines of every report (the owner, 2026-09-21)

Every report of a worker to the Boss, every answer of the advisor on a proposal
and every item the Boss brings the owner opens with six short lines, one each:
(1) the information: what the item moves between which records or Nodes, through
which Link and Port, at what rate, what is kept and what is lost; (2) the generic
solution: the one primitive, for every family alike, from which the number
follows, never a patch beside it; (3) why it will work: the mechanism on the
GameBoard, with the reading that would show it and the reading that would refute
it; (4) why do this at all: what it buys the law or a measurement, and what stays
unread or wrong if it is not done; (5) the decisions: which lines of
docs/HIGHLIGHTS.md the item keeps, and whether one should now change, a change
being a proposal made on the owner's word; (6) the implementation: what changes
in the tree, the time end to end, and what it can break. The evidence follows the
six lines. Every number in them is labelled DETECTOR or GAMEBOARD.

## Writing to the owner (the owner, 2026-09-30)

The Boss and the advisor write to the owner in simple images: a plain picture
for every term (a well, a tail, a bucket filling to a wall), then a short
explanation, and the essence in bold, so that he reads the point first and the
reason after. A number stands on its own line or in a short table, never buried
in a sentence. Hebrew to the owner, one sentence per line, no blank lines between
them, no bullets and no full stop at the end of a line; English in the
repository.

## Checks proportional to the change

A test exercises one generic rule alone on a minimal GameBoard, with its expected
integers derived from the law inside the test, with an edge case, and finishes in
seconds; no test pins the numbers of an example world (the owner, 2026-09-17 and
2026-09-19). A behaviour change needs a dedicated test; a bug is fixed with a
test that fails before and passes after. `python tools/check.py` runs before
every delivery: it selects the changed files, their consumers and the tests of
every pull request, with lint, formatting, strict types and the gates; `--full`
is explicit. CI runs the whole suite on every pull request, so the full local
check is run only to find a red shard. Never drop a failing test, weaken a gate
or turn a failure into an expected pass. Runs and tests are headless.

## How to run a world

A world is laid and run from its files alone, as
[docs/ENGINE.md](../docs/ENGINE.md#6-how-to-run-a-world) says:
`PYTHONPATH=src python tools/pixel_mode.py --input <world>.json` lays its bodies,
`PYTHONPATH=src python tools/run_inputs.py --out runs/first --jobs 4 <world>.json`
runs it headless, and the output file's verdict is read first (`REFUSED` names
the key or the guard; `LAWFUL` carries the clicks and the books). Every run names
the `main` commit it ran on. A run before its blind number is a first look and
says so.

## The review before a merge

The Boss reads every diff before the merge: the changed files against the brief,
the dedicated test, the three verdicts where a rule changes, the sentences
deleted from the documents, no number and no name in the engine, English and
sentence case, and `main` merged in. A change to the law or to `core/` is read
against the law's lines; everything else merges on green CI. A green check on an
old base is no evidence about the merged tree: merge one pull request at a time.

## The language

Every repository file, commit and pull request body is in English, simple and
precise; every message to the owner is in Hebrew (AGENTS.md, the language rule).
Every heading and every name is in sentence case: a capital first letter, never
all caps (the owner, 2026-09-30). The words of the engine are the words of
docs/ENGINE.md: a Node, a Link, a Port, an Event, the GameBoard, a Family, a
Record, a Body, a Detector, a Click, a Primitive, an Interval, and no other noun
for them.

## The short procedure: from the owner's word to the merge

1. The owner speaks, in either session. The session that hears him relays his
   words verbatim to the other; the Boss records them.
2. The Boss records a decision at once as one line in docs/HIGHLIGHTS.md,
   replacing the line it changes, and in docs/ALGEBRA.md when the law or its
   numbers change; a hypothesis under its own name.
3. The advisor computes the blind number from the engine's own lines and states
   the three verdicts; the Boss writes them in the brief.
4. The Boss's worker builds on one short branch from `main`, with a dedicated
   test, no number in the engine, and reports the numbers and the sentences it
   removed.
5. The gates: `python tools/check.py`, then CI on the pull request.
6. The Boss opens the pull request; its body carries "HANDED BY Boss: ..." and
   the Boss's session link, the problem, the change, the validation and what was
   deleted from the documents.
7. The Boss merges on green CI with `main` merged in, one pull request at a time,
   and deletes the branch. `main` is the one version that works; no one pushes to
   it directly; there are no tags.
8. The Boss reports to the owner in Hebrew: the numbers, the list of removed or
   rewritten sentences, and what stands with him.

Propose and proceed (the owner, 2026-09-27): whoever needs another's word states
his own proposed answer, builds on it, and the other confirms or corrects; nobody
waits idle on a question he can answer himself.

## The channels

The two sessions discuss on the GitHub issues, where the owner reads: #1509
holds the relayed decisions and their discussion, #1495 the findings and the
advisor's answers with numbers. A finding or approval of one pull request is a
comment on it; a list across pull requests is one issue with a checklist. A
session calls the other by a Routine bound to the receiver's session
(create_trigger with the receiver's session, then fire_trigger with the text),
only to say that a comment is waiting. The Boss's workers report inside the
Boss's session. A decision given in one session is relayed to the other and
recorded by the Boss.

## Tools and authority

The owner's standing authorization covers the Boss's commits, pushes, pull
requests and merges of requested work on the branches of its tasks; it is not
permission for unrelated changes, force pushes, a push to `main`, a bypassed gate
or a message to another person. The advisor reads, computes and answers; it
writes nothing to the repository and grants no permission. A skill supplies no
authorization that the owner's word does not.
