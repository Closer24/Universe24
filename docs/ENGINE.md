# The engine

This document describes the engine as the code holds it on `main`. It is one of the three current documents of the project, beside [ALGEBRA.md](ALGEBRA.md) (the law, one algebraic line per primitive) and the day's log. Anyone who enters the project should understand the whole engine from this page, the algebra and the code.

The engine is an integer simulator of a lattice of Nodes. A run reads three files, steps the lattice a declared number of intervals by one rule, and writes one output file. Nothing physical is written in the code: the families, their attributes and their integers come from the run's files, and every primitive is one folder found by its name.

## 1. The words

- **Node**: one place of the lattice. Its whole local information is its **NodeState**: the levels of every family at that Node, with the remainders of every division made there.
- **Link** and **Port**: a Node has six neighbours, one through each of its six Ports. A level moves from a Node to a neighbour only through a Port.
- **GameBoard**: the lattice of Nodes, a box of three sides. Each axis is closed (a wall) or periodic (a ring), as the world file says.
- **Family**: one kind of field. A family has parts (1, 3 or 6 components), a phase (1 or 2), a pair of integers, and its declared attributes. The families are the universe file's, never the code's.
- **Record**: one wave of one family on the GameBoard: two integer arrays, the level now and the level before, and an array of remainders. The engine steps a record with **Rule3**.
- **Body**: a bounded thing of one family on some Nodes, with a count of quanta per Node and a momentum. A body's own record is the standing wave at its Nodes. A body may hold other families' levels at its Nodes (the hold), may give a record (the giving) and may take one (the taking).
- **Detector**: a named set of Nodes that reads the records passing through its Ports and clicks when a record's booking reaches its threshold. A click is a **measurement**; everything else the engine writes is a GameBoard reading, a diagnostic.
- **Click**: a whole quantum moving from a record to a detector or from a body to a new record. Quanta never split.
- **Primitive** (the owner's "feature"): one kind of attribute the engine can apply to any family, written once in its own folder and applied by the files' declarations, never by a family's name.
- **Interval**: one step of the whole GameBoard. The run's `ticks` is the number of intervals.

## 2. The main loop

The main loop is the class `DetectorLawSimulation` in `src/event_universe/events/detector_law.py`. It is built from a loaded world, steps it one interval at a time, and reports its state. The planned shape splits it into `core/main_loop.py` (take the input, run the step, write the output), with the step, the Node and the register each in its own file under `core/`; today the loop and the step share one file, and the register is already `core/register.py`.

One interval has five places, in this order:

| Place | What happens | Who writes |
| --- | --- | --- |
| (i) | The clicking families' records step by Rule3, every component, with the transport through the Ports. | the operation, the send, the receive, the wait |
| (ii) | The bookings at the detectors' Ports, the ladder, the takings and the givings. A click's writes are deferred to the next interval. | the clicks, the giving, the recoil |
| (iii) | The held families' records step by Rule3. | the operation |
| (iv) | The holds are written: each body's count, momentum and spin written into the held families' levels at its Nodes; the deferred writes of the interval's clicks enter. | the hold, the source |
| (v) | The bodies on one Node: the feed, the induction, the spin's step, the recoil's accumulator. | the spin's step, the feed, the induction |

The loop calls a primitive through the register by its name and its place, `register.at("the hold", "(iv)")`, and never by a family's name. The order of two primitives that write the same value at the same place is declared by each, and the register refuses two writers with no order.

Every step is reversible: `step_inverse` returns the whole state to the interval before, bit for bit, by Rule3's own backward line and the click journal.

### Rule3

Rule3 is one function in `src/event_universe/core/rule3.py`, the only place in the code that holds the rule's arithmetic. At every Node it forms the next level from the level now, the level before, the six neighbours' arrivals and the remainder:

```
w a_next + r' = SUM_axis R_axis (arrival_+ + arrival_-) + S a_now - w a_before + r,  0 <= r' < w
```

The coefficients `R` (one per axis), `S` and `w` come from the family's pair, the Node clock and the paces read at the Node. The paces are `Gamma` minus the weighted sum of the levels the family reads (its `reads`), so a body's count lowers the pace of what it reads and bends the wave. One floor division per Node per step; the remainder stays at the Node. The same line with the two levels exchanged is the step backward.

### The state a run keeps

Per family with records: the records (identity, family, now, before, remainder, the record's norm and its bookings at the detectors). Per held family: one record over the GameBoard. Per body: its Nodes, its count per family, its momentum, its spin, its remainders, its window if it is giving. Per detector: the ladder and the count of clicks. The books: the conserved forms per family, checked balanced at every interval. Nothing else is kept at a Node beyond the events there.

## 3. The folders, their cards and the register

Every primitive is one folder `src/event_universe/features/<name>/__init__.py`. The register (`src/event_universe/core/register.py`) finds the folders at load and reads each folder's card, its `DECLARATION`:

| Field | Meaning |
| --- | --- |
| `name` | the primitive's unique English name, "the hold"; the folder is the name without "the", with underscores |
| `place` | one of the five places, or "any" for a read-only line |
| `reads` | the values it reads, in the ledger's words |
| `writes` | the values it writes |
| `order` | its order among the writers of the same value at the same place, or None when alone |
| `function` | its function once its code lives in the folder, or None |
| `section` | its line in ALGEBRA.md |
| `word` | the mathematician's reading of its moment: the right side, the step, after the step |
| `binder` | `bind(loop)`, which gives the loop's method that implements it today while the code still sits in the loop |

A folder's function has one signature, `apply(term, start, own) -> writes` (`src/event_universe/core/primitive.py`): the term is one line of the files (the primitive's name, its target value, the family or body it acts on, its degree, its weight, its table); the start is the interval's read-only state (levels now and before, paces, counts, walls, momenta); the own is the primitive's own record at the Nodes it acts on, where every remainder of its divisions lives; the writes are whole integers into declared values, now or deferred to the next interval.

The folders today: the operation (Rule3 itself), the send, the receive, the wait, the hold, the clicks, the clicks list, the giving, the recoil, the recoil's accumulator, the source, the signed read, the self-source, the feed, the induction, the spin's step, the degree, the pair, the phase, the hop, the hand, the lifetime, the internal representation, the trace. A folder whose card has neither a function nor a binder is a row of the law not built: the loader refuses a term naming it.

The register refuses, at load and by name: a folder without a card or whose folder name is not its declared name's; a name declared twice; a place or a word outside the five and the three; two writers of one value at one place with no order; and a call from the loop at a place other than the declared one. There is no version anywhere: a primitive that changes behaviour keeps every shipped world bit for bit or takes a new name.

## 4. The loader and the files

The loader is `src/event_universe/events/world.py`, entered through `src/event_universe/world_files.py` (`parse_nature_beam_world`, `load_world`). It reads three files, checks every key by name and refuses an unknown key, a missing key or an out-of-bound value with a message naming it. It writes no default. The planned shape is one small generic loader that checks each declared term against the schema of the folder it names.

### The world file

One experiment is one world file, a JSON object under `examples/events/`. Its keys:

- `shape`: the GameBoard's three sides. `boundary`: per axis, `closed` or `periodic`. `ticks`: the intervals to run.
- `universe`: the path of the universe file. `engine`: the path of the start file. Both are repository paths.
- `measured`: the bodies. Each names its `family`, its place on the GameBoard (`position`, and `extents` for a box), its `amount` of quanta, its `stocks` of other families it can give, its `momentum`, `spin` and `moment`, and, for a giver, its `emitter` (the given family, the receivers, the weight, the twist). Today's loader also asks a body for its `pair`, `kind` and `seed`; the law's form of a body is its family, its Nodes, its count per Node and its momentum, and nothing else.
- `detectors`: the named sets of Nodes, each with its `positions` and the body it belongs to.
- `readings`: what the run writes, a list of named entries, each with a `name`, a `kind` (`clicks`, `level`, `support`, `total`, `centre`) and the kind's keys (a detector, a family and a Node, a family, a body) and `every`, the interval between readings. The source worlds carry this key; today's loader does not read it yet.
- `stamp`: the digest of the file as its generator wrote it. A file whose stamp does not match is refused.
- Today's loader also requires `K`, `N` and `release`, integers of the old form kept until the loader's cut.

### The universe file

One file, `examples/events/universe.json`, names every family and every integer of the universe. Every world names it, and every family is on in every run; a world cannot turn a family off.

- `integers`: `node_clock` (Gamma, the pace of an empty Node), `amplitude_bound` (the largest level), `Lambda` (the weight of a read by sign), `momentum_unit`, and the `twist_table` (the unit and the fine table of the twist).
- `families`: one entry per family, at most twenty. Each has `name`, `parts` (`[1]`, `[1, 3]` or `[1, 3, 6]`), `phase` (1 or 2), `pair` (two integers, or `"body"` for the family of bodies), `reads` (the families it reads, each with a `weight`, a `by` of 1 or `"q"` and a `twist`), `self_source` (a unit, 0 for off), and optionally `held` (`count` content or sign, its `factors` per part, its `dipole`) and `clicks` (`gives`, `takes`, `quantum`). A family declared `sourced` gains a record family's count into its level; the source's fragment in `examples/events/source/universe_entries.json` shows the form.

### The start file

`examples/events/engine_start.json` holds the run's parameters, today one key, `mode`. Every key the engine needs is in this file; the code holds no default.

### The output

`tools/run_inputs.py` writes one file per world, `<name>.output.json`: the input's name and stamp, the verdict (`LAWFUL`, `REFUSED` with the reason, or `LEAK` when a family with no source moved), the ticks, the mode, every click with its detector and its interval, the count per detector, and the comparison per registered pin (`MATCH` within the band or `MISS`). A click is a measurement. The engine's state stream (`snapshot_stream`: the interval, the bodies' contents, the held families' levels, the records' integers, under the files' names) and the books are GameBoard readings, diagnostics for the tests and the record; they are never compared with nature.

## 5. The gates

Every pull request runs `python tools/check.py --base <the base commit>` (the one CI file, `.github/workflows/check.yml`). The tool selects the changed files and their consumers, runs `ruff`, `ruff format --check`, `mypy` on the typed modules and `pytest` on the selected tests, and adds four gates on every change:

| Gate | Test | What it holds |
| --- | --- | --- |
| Regression | `tests/test_shipped_worlds.py` | Every shipped world under `examples/events/` is replayed for its recorded intervals and compared bit for bit with `tests/shipped_worlds.json`, a digest of what the run is under the files' names. A moved digest is a changed run; an intended change re-records in the same commit with `tools/record_shipped_worlds.py` and says why. Until the one generator builds the worlds from zero, this record guards the code against unintended change only; it is no physical reference. |
| Genericity | `tests/test_genericity.py` | A seeded generator draws one to twenty families with random English names and random admitted attributes; every draw loads and runs, and five properties hold: renaming the families leaves the run bit for bit, reordering them leaves it bit for bit, a family with no source stays exactly zero, Rule3's conserved form holds where no click and no load acts, and the backward run returns the start. |
| Code shape | `tests/test_code_shape.py` | The ratchet: a file of `src/` within the limits (every docstring one line, no record reference, under 400 lines, no Rule3 arithmetic and no shift across Nodes outside their homes) passes; a file beyond them may not grow any count against `tests/code_shape_baseline.json` or against the merge base's copy of it, and a lowered count is re-recorded in the same commit with `tools/record_code_shape.py`. Two functions with one abstracted body fail. A feature folder imports `core/` alone and never another feature; `core/` imports nothing outside itself; nothing outside `core/` imports the loop's internals. |
| Language | `tests/test_repository_language.py` | Every file of the repository is English: no Hebrew or other non-Latin script in any text. The hygiene and navigation tests beside it keep one canonical copy of each file and every link and anchor of the entry documents live. |

The acceptance tests (`tests/test_engine_acceptance.py`, `tests/test_loader_acceptance.py`) state what the finished engine must satisfy: no family name, no integer of the universe, no default, no flag and no version in the code; the rule as one function; a body loaded by its four attributes alone; every folder's schema its own. A test the code fails today is marked xfail strict, with the reason; it turns green when the cut lands and then loses its mark.

`python tools/check.py --full` runs everything; CI runs the affected scope. Only the Boss merges into `main`, on green.

## 6. How to run a world

1. Write or pick a world file under `examples/events/`, naming the shipped universe and the start file. A generator writes the file and its stamp; a file edited by hand is refused at its stamp.
2. Run it headless, one output file per world:

```
PYTHONPATH=src python tools/run_inputs.py --out runs/inputs --jobs 4 examples/events/<folder>/<world>.json
```

3. Read the output file: the verdict first. `REFUSED` names the key or value the loader refused. `LEAK` names the family that moved without a source. `LAWFUL` carries the clicks and the counts.
4. A pin (an expected count, first click or mean interval per detector, with its band) is written in a pins file before the run and passed with `--pins`; the output then says `MATCH` or `MISS` per pin. A run is compared with a pin only on the owner's Go.
5. To record a world into the regression record, run `PYTHONPATH=src python tools/record_shipped_worlds.py` and commit the record with the world.

The engine never draws or renders in a run; a display reads the output afterwards.

## 7. How to add a feature

1. Read the primitive's line in ALGEBRA.md. The mathematician writes it; a primitive without a line is not built.
2. Make one folder, `src/event_universe/features/<name>/__init__.py`, on a short branch from `main`. Write its card, `DECLARATION`, with the name, the place, the reads, the writes, the order among the writers of its values, the section and the word. Write `apply(term, start, own) -> writes` with whole integers and its own remainders in `own`; write `check` for its refusals by name. Touch no shared file: the register finds the folder.
3. Keep the shape: every docstring one line (what it does and its ALGEBRA.md line), no record number, under 400 lines, no Rule3 arithmetic outside `core/rule3.py`, no shift of a level across Nodes outside the transport. Import `core/` alone.
4. Write its small test beside it, `tests/test_feature_<name>.py`: the line on the run files' numbers, the refusals, the inverse bit for bit, the hand identity of one Node.
5. Write its run files: a world under `examples/events/<name>/` with its stamp, the universe's fragment if it adds a family word, and the blind expectations in the folder's README before any run.
6. Run `python tools/check.py --base origin/main`. With the new primitive undeclared in the files, every shipped world must come out bit for bit; the regression gate says so.
7. Open the pull request. The mathematician approves the line with `APPROVED-MATH` on the pull request; the Boss merges on green. The loop's call of the new primitive at its place is the core's cut, Main Loop's, in its own pull request.
