# The shared way of working

The team is the Boss, the advisor, the mathematician, the reviewer, the writer
and the experimenter, each with its issue, and the owner decides (the owner,
2026-09-30 and 2026-10-04). The Boss leads, decides within the owner's words,
records his decisions and runs the workers; its card is
[the Boss's card](boss-orchestrator/SKILL.md). The advisor answers from the
current documents, judges every line by its status, computes the blind numbers
and writes nothing to the law, the engine, the paper or HIGHLIGHTS.md; at the
owner's word of 2026-10-04 it builds tests and tools on a branch from `main` for
the Boss's HANDED BY pull request, nothing of src/event_universe/; its card is
[the advisor's card](advisor/SKILL.md). The mathematician is the second hand on
every derivation and at every sha, and the first hand where the Boss routes it
(#1836). The reviewer reads the paper, the supplement and the law whole and
keeps the ledger (#1793). The writer holds the paper (#1538). The experimenter
runs the shipped worlds against their blinds and keeps each folder's reading
(#1827).
This file is what the team shares. A skill is an instruction, not a grant of
permission: the user's scope binds every session.

## Repository knowledge and restart

Start from the current checkout, never from a previous conversation. Read
[AGENTS.md](../AGENTS.md) first, then only the part of the three documents the
task needs. One definition per concept: a skill links to the law and never copies
it. Temporary state (the task in hand, a blocked check, the next action) lives on
the GitHub issue or the pull request, never in a skill.

## The three documents and the two records (the owner, 2026-09-26, 2026-09-30 and 2026-10-04)

The project keeps three current documents, two records, the skills and the
entry files, and nothing else:

| Document | What it holds |
| --- | --- |
| [docs/ALGEBRA.md](../docs/ALGEBRA.md), the law | One algebraic line per rule, the families, the bodies, the clicks, every experiment's formula and blind expectation, every hypothesis under its own name |
| [docs/ENGINE.md](../docs/ENGINE.md), the engine | The engine as the code holds it on `main`: the words, the interval, the folders, the loader, the output, the gates, how to run a world |
| [docs/HIGHLIGHTS.md](../docs/HIGHLIGHTS.md), the decisions | The decisions in force, one line each; a decision of the owner replaces the line it changes |

The two records are not documents of the law; they are the files the one method
needs (the owner's word of 2026-10-04: one method that brings zero bugs, with
all the project's documents synchronized):

| Record | What it holds |
| --- | --- |
| docs/REVIEW_LEDGER.md, the reviewer's ledger | Every finding with its state, one row each: its place, its station, its hand and the hash it was checked at; changed by the pull request that prints |
| docs/PROVENANCE.md, the provenance | Who said what and when, under the law's line names: the hands' comments, the owner's dated words, the pull requests; the law's lines give it up in part 4 of the fill and keep the statement |

The skills are this file and the two role cards that exist, the Boss's
(`skills/boss-orchestrator/SKILL.md`) and the advisor's (`skills/advisor/SKILL.md`);
the other four hands, the mathematician, the reviewer, the writer and the
experimenter, have their issues as their cards until their cards are written.
The entry files are README.md, AGENTS.md and CONTRIBUTING.md. No log and no
status page: the two records are the only files beside the three documents, and
HIGHLIGHTS.md holds the decisions only, one line each, no diary.

## The documents rule (the owner, 2026-09-30 and 2026-10-04)

HIGHLIGHTS.md is updated at once, with the owner's word, and holds the decisions
in force, one line each: not a diary, and not the state of the findings, which
is the ledger's. ALGEBRA.md is updated when the law or its numbers change.
Every hypothesis is declared under its own name, outside the law, until it passes
the three tests or the owner admits it. A change to a document replaces what it
touches and deletes what no longer holds in the same pull request; the body names
what was deleted. No history note, record number or superseded line stays: git
keeps the history. Nothing is a decision until it is in HIGHLIGHTS.md.

## The one method (the owner, 2026-10-04)

The owner's word of 2026-10-04, about 03:35 Israel: converge on one method that
simply brings zero bugs, in the paper, in the algebra and in the supplement, with
all the project's documents synchronized. The method is five lines, the
advisor's, adopted by the Boss (#1793 comments 5975048351 and 5975055409).

1. **One source per fact.** The engine's behaviour is its tests. The law's
   statements are docs/ALGEBRA.md. Signs and units are the law's conventions and
   units table. Every shared number is a row of tools/numbers.json with its
   script under tools/derivations/. Who said what and when is docs/PROVENANCE.md.
   A run's reading is its folder's blind_and_reading.md. The paper, the
   supplement and docs/ENGINE.md cite these and restate none of them.
2. **One loop per finding, in the repository's ledger.** Every finding is one
   row of docs/REVIEW_LEDGER.md (its place, its station, its hand, the hash) and
   goes through one loop: found by a whole read; the first hand's answer from the
   quoted definitions, with a script where there is a number; a blind confirm by
   a second method; printed, the law first and the paper in the same batch; the
   gates; re-checked at the hash; closed. A station held over an hour (a first
   hand owed, a confirm owed, a print owed, a re-check owed) is a finding of the
   method, named with its station and its hand.
3. **One gate set on every pull request.** The language; the documents (stale
   phrases, numbers, derivations, headings and paths); the paper's marks checker;
   the readings gate for the runs (the gate worlds re-run and compared bit for
   bit with their folders' blind_and_reading.md); the shapes and the ownership.
   `python tools/check.py` runs the set locally and CI runs it on the pull
   request. Nothing merges red; nothing is ticked by memory.
4. **Whole reads until silence.** After each batch a hand who did not write
   reads each document whole. A whole read that finds nothing closes it. Zero is
   read from the ledger file and never declared.
5. **One pace.** Prints per batch, distributions per round. No restructuring
   while a fill is open; the structural work (the split of the law's statements
   from their provenance, the statements' rewrite) is its own numbered part, with
   both hands and the gates green at every push.

The rules of the hands under the method (the owner's word of 2026-10-04, #1793
comment 5974938542):

- The second hand writes its own number from the quoted definitions before
  reading the first hand's.
- A number takes two methods where two exist (an analytic form against a
  numeric one).
- Every derived or computed claim has a Python derivation script, and a test
  compares the script's output with the printed number; every such mark names
  its script. A theorem's proof stays in words beside its mark.

## The three tests of every rule: generic, vector, local (the owner, 2026-09-21)

A rule enters the law only if it passes all three. The hands apply them: the
advisor and the mathematician when judging a line, the Boss when briefing a
build.

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

Only a NodeReader's click is a measurement. Every number reported is labelled
NODEREADER or LATTICE; a lattice reading is a diagnostic, never compared with
nature and never a result on its own.

## The method of derivation (the owner, 2026-10-01)

Every row of nature is derived from the law by one method, in six steps, and
the paper explains it as its own:

1. Start from Rule3's line alone: a reader's band at the paces the row gives
   it, the clock once and the Link twice. No structure is written before its
   band is computed.
2. The source is a row's static rest: the six Ports' Green's function at the
   row's pair, a body's well the one number.
3. The bridge to nature is a body's clicks and nothing else: a bound body's
   rotation reading the content once is the clock; its click rate against
   nature's identifies the law's level with nature's potential. The source is a
   body's well, the clock a body, the NodeReader a body, an orbit a body's chain
   of clicks. The body enters through its clicks, never through its generator's
   equations.
4. Every observable is a click formula: the NodeReader's form over the
   quantum's measure on the forward orbit, or a ratio of two such. Every other
   formula is of the lattice, a diagnostic, and is labelled so beside its
   status (the fence: lattice or clicks).
5. Re-derive every row whenever a line changes and look for the problems: a
   row that does not come out, a sign that turns, a band that is not real. Each
   is a finding by name, never smoothed. Two hands derive before a line is
   written, and the blind numbers are written before any build.
6. Every result carries its status: theorem, derived, computed from the law,
   the owner's declaration (the model's postulate in the paper), hypothesis, or
   to be determined by an experiment, the experiment named.

## Names with meaning, never codes (the owner, 2026-09-24 and 2026-09-25)

Every experiment, rule, folder and file is called by its plain name: "the two
slits", "the moving lamp's redshift", "the signed read". No code letter or
number stands for a thing, not even in parentheses after its name. A block is
named by what it is on the lattice (a source, a body, a NodeReader, a clock);
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
Lattice, with the reading that would show it and the reading that would refute
it; (4) why do this at all: what it buys the law or a measurement, and what stays
unread or wrong if it is not done; (5) the decisions: which lines of
docs/HIGHLIGHTS.md the item keeps, and whether one should now change, a change
being a proposal made on the owner's word; (6) the implementation: what changes
in the tree, the time end to end, and what it can break. The evidence follows the
six lines. Every number in them is labelled NODEREADER or LATTICE.

## Writing to the owner (the owner, 2026-09-30)

The Boss and the advisor write to the owner in simple images: a plain picture
for every term (a well, a tail, a bucket filling to a wall), then a short
explanation, and the essence in bold, so that he reads the point first and the
reason after. A number stands on its own line or in a short table, never buried
in a sentence. Hebrew to the owner, one sentence per line, no blank lines between
them, no bullets and no full stop at the end of a line; English in the
repository.

## Checks proportional to the change

A test exercises one generic rule alone on a minimal lattice, with its expected
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

The Boss reads every diff of the engine's rounds and of `core/` before the merge,
against the law's lines: the changed files against the brief, the dedicated test,
the three verdicts where a rule changes, the sentences deleted from the documents,
no number and no name in the engine, English and sentence case, and `main` merged
in. A documents, tests or paper pull request carries the hands' final paragraphs,
pasted by the documents worker or the writer from the closures' comments; the Boss
checks each paste against its comment id, a diff of two texts, and does not read
the whole fill; it merges by auto-merge on green CI, the branch rule enforcing an
up-to-date base, the Boss arming it after the check (the owner's decision 234 of 2026-10-03, #1572 comment 5966659068, proposals 3 and 5). The engine's branches merge one
at a time; documents, paper and engine branches on disjoint file sets merge
independently (234, proposal 6). A green check on an old base is no evidence
about the merged tree. The Boss's check is a diff; the whole read is the hands',
after each batch, by a hand who did not write (the one method).

## The language

Every repository file, commit and pull request body is in English, simple and
precise; every message to the owner is in Hebrew (AGENTS.md, the language rule).
Every heading and every name is in sentence case: a capital first letter, never
all caps (the owner, 2026-09-30). The words of the engine are the words of
docs/ENGINE.md: a Node, a Link, a Port, an Event, the lattice, a Family, a
Record, a Body, a NodeReader, a Click, a Primitive, an Interval, and no other noun
for them. The old nouns detector, instrument, emitter, absorber, observer and
measurer have left (the owner's word of 2026-10-03, "no field, only events"): a
NodeReader with Nodes alone or with a record of its own is the one declaration
kind, and none of them returns.

## The short procedure: from the owner's word to the merge

1. The owner speaks, in any session. The hand that hears him relays his words
   verbatim on its issue; the Boss records them.
2. The Boss records a decision at once as one line in docs/HIGHLIGHTS.md,
   replacing the line it changes, and in docs/ALGEBRA.md when the law or its
   numbers change; a hypothesis under its own name. A hand's answer is its
   comment on its issue, cited by its id; the Boss writes no relay comments, and
   HIGHLIGHTS.md takes the decision's line only (the owner's decision 234 of 2026-10-03, #1572 comment 5966659068, proposal 2; the owner, 2026-10-04).
3. The Boss asks both hands at once, in one comment on one thread (the hand's
   issue: the mathematician's for a derivation, the reviewer's for a finding),
   and fires their triggers the moment the ask is posted; while any ask is open
   each hand's cadence is 15 minutes, the second hand writing its own number
   from the quoted definitions before reading the first's text and then
   seconding or differing in the same thread, the 45-minute check-in the
   fallback only. Every closure's comment ends with its final paragraph for
   docs/ALGEBRA.md in the law's words and, where the paper is touched, the
   paper's sentence (234, proposals 1 to 3). The advisor computes the blind
   number from the engine's own lines and states the three verdicts; the Boss
   writes them in the brief.
4. A fix enters as the code on one short branch from `main`, its one unit test,
   two hands at the sha and the Boss's merge at CI green, nothing around it (the
   owner, 2026-10-04, #1793 comments 5979384796 and 5979394836: "we fix, make a
   unit test, and merge after two hands; the new method", "if the function is
   generic there is no need to keep anything, just a unit test"); a physics change
   keeps the law's line first (steps 2 and 3). The worker writes no number in the
   engine and reports the numbers and the sentences it removed; the brief grants
   the tests' ratchet's room for the round, "this round adds N test lines" (234,
   proposal 7). Workers run on parallel branches by disjoint file set; the
   engine's branches one at a time (234, proposal 6).
5. The gates: the one gate set, `python tools/check.py` locally, then CI on the
   pull request; nothing merges red.
6. The Boss opens the pull request; its body carries "HANDED BY Boss: ..." and
   the Boss's session link, the problem, the change, the validation and what was
   deleted from the documents. The fills are batched: one documents pull request
   and one paper pull request per hour or per three closures, the law's and the
   paper's two-hands passes in parallel in the same batch, the documents worker
   and the writer pasting the hands' final paragraphs (234, proposals 3 and 4).
7. The Boss, the only merger, merges the engine's rounds and `core/` on green CI
   with `main` merged in, one at a time, after reading the diff against the law's
   lines; a documents, tests or paper pull request merges by auto-merge on green
   CI, the branch rule enforcing an up-to-date base, after the Boss's check of the
   pastes against their comment ids (234, proposal 5); the branch is deleted.
   `main` is the one version that works; no one pushes to it directly; there are
   no tags.
8. The Boss reports to the owner in Hebrew: the numbers, the list of removed or
   rewritten sentences, and what stands with him.

Propose and proceed (the owner, 2026-09-27): whoever needs another's word states
his own proposed answer, builds on it, and the other confirms or corrects; nobody
waits idle on a question he can answer himself.

## The channels

The team discusses on the GitHub issues, where the owner reads: the writer's
#1538 (the paper), the reviewer's #1793 (the findings on the paper, the
supplement and the law, and the advisor's answers to what is asked there), the
experimenter's #1827 (the shipped worlds against their blinds) and the
mathematician's #1836 (the second hand on the law and the paper). The state of
every finding is its row in the ledger, docs/REVIEW_LEDGER.md, and no issue. A
finding or approval of one pull request is a comment on it; a list across pull
requests is one issue with a checklist. A hand calls another by a Routine bound
to the receiver's session (create_trigger with the receiver's session, then
fire_trigger with the text), only to say that a comment is waiting. The Boss's
workers report inside the Boss's session. A decision given in any session is
relayed to the Boss verbatim and recorded by him.

## Tools and authority

The owner's standing authorization covers the Boss's commits, pushes, pull
requests and merges of requested work on the branches of its tasks; it is not
permission for unrelated changes, force pushes, a push to `main`, a bypassed gate
or a message to another person. The advisor reads, computes and answers; it
writes nothing to the law, the engine, the paper or HIGHLIGHTS.md, opens no pull
request and grants no permission; at the owner's word of 2026-10-04 its tests
and tools go on a branch from `main` for the Boss's HANDED BY pull request,
nothing of src/event_universe/. A skill supplies no authorization that the
owner's word does not.
