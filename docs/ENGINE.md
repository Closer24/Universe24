# The engine

This document describes the engine as the code holds it on `main`. It is one of the three current documents of the project, beside [ALGEBRA.md](ALGEBRA.md) (the law, one algebraic line per primitive) and [HIGHLIGHTS.md](HIGHLIGHTS.md) (the decisions in force). Sections 8 and 9 are rendered from the tree by `tools/render_documents.py`, never written by hand: the run's files key by key, and the state of the engine (the primitives, the step file's acts, the expected failures, the owners and the shipped worlds). Anyone who enters the project should understand the whole engine from this page, the algebra and the code.

The engine is an integer simulator of a lattice of Nodes. A run reads three files, steps the lattice a declared number of intervals by one rule, and writes one output file. Nothing physical is written in the code: the families, their attributes and their integers come from the run's files, and every primitive is one folder found by its name.

## 1. The words

- **Node**: one place of the lattice. Its whole local information is its **NodeState**: the levels of every family at that Node, with the remainders of every division made there.
- **Link** and **Port**: a Node has six neighbours, one through each of its six Ports. A level moves from a Node to a neighbour only through a Port.
- **GameBoard**: the lattice of Nodes, a box of three sides. Each axis is closed (a wall) or periodic (a ring), as the world file says.
- **Family**: one kind of field. A family has parts (1, 3 or 6 components), a phase (1 or 2), a pair of integers, and its declared attributes. The families are the universe file's, never the code's.
- **Record**: one wave of one family on the GameBoard: two integer arrays, the level now and the level before, and an array of remainders. The engine steps a record with **Rule3**.
- **Body**: a bounded thing of one family on some Nodes, with a count of quanta per Node and a momentum. A body's own record is the standing wave at its Nodes. A body may hold other families' levels at its Nodes (the hold), may give a record (the giving) and may take one (the taking).
- **Detector**: a named set of Nodes that reads the records passing through its Ports and clicks when a record's booking reaches its threshold. A detector's click (the engine's `gather` line, the only line the output reads) is a **measurement**; everything else the engine writes is a GameBoard reading, a diagnostic. A body has a clock too: a cycle is counted when its own record's sum crosses zero, and the loop writes that cycle as an event line named `click`, which is the body's cycle and not a detector's click.
- **Click**: a whole quantum moving from a record to a detector or from a body to a new record. Quanta never split.
- **Primitive** (the owner's "feature"): one kind of attribute the engine can apply to any family, written once in its own folder and applied by the files' declarations, never by a family's name.
- **Interval**: one step of the whole GameBoard. The run's `ticks` is the number of intervals.

The core's integer modules under the engine: `core/integer.py` holds the working bound 2^63 - 1 with its check, the body's count step `by_drive` (the hop) and `by_clock`; `core/game_board.py` holds the Ports' fixed order (+X, -X, +Y, -Y, +Z, -Z; Port k on axis k div 2), the extent bound 1 through 4096, the self-Link of a periodic axis of extent one, and `MAX_VALUE` = 2^30 - 1, the bound on a family's quantum, a charge per unit and every pair's two integers; `core/phase.py` holds the bound of the world's phase circle, N a power of two from 2 through 65536, read by the loader alone; `core/ports.py` holds the six Ports of every Node (the arrival of an array through one Port, the six arrivals once per array per interval, the outward Ports of a set of Nodes), the one shift across Nodes of the package; `core/main_loop.py` holds the main loop.

## 2. The main loop

![The engine's modules and the data on every arrow](ENGINE.svg)

The drawing: one box per module, an arrow for what one hands to the next, the gates under them; it is redrawn when a module moves. One responsibility per module:

| Module | Holds | Hands on |
| --- | --- | --- |
| `tools/run_inputs.py` | one process per input; the verdict `LAWFUL`, `REFUSED` or `LEAK`; the pins compared | the output file |
| `src/event_universe/world_files.py` | the three files read at the world's paths, the step file from the repository root, the stamp's digest | the documents to the loader |
| `src/event_universe/loader/frame.py` with `core/schema.py` and `loader/cards.py` | the schemas of the files' keys; a family's entry is the frame's `name` and `clock` with the keys the folders' cards declare | the checked values |
| `src/event_universe/loader/world.py` | the loop's classes built from the checked values, and the rules between keys | the loaded world |
| `src/event_universe/events/detector_law.py` | the engine: the stages, the state and the readings, built from the loaded world | `step()`, the main loop's `run` |
| `src/event_universe/core/main_loop.py` | the plan of the step file's acts and the walk of one interval under its guards | each act's stage or `apply` |
| `src/event_universe/core/register.py` with `core/step.py` | the folders' cards and the step file; `at(name, place)` | the act's function |
| `src/event_universe/features/<name>/` | one primitive each: its card and its `apply` or `bind` | its writes |
| `src/event_universe/core/rule3.py` with `core/ports.py` | the one arithmetic; the six arrivals, the one shift across Nodes | the next level and the remainder |
| `src/event_universe/core/readings.py` | the declared readings by kind, the clicks from the `gather` lines | the output's `readings` and `clicks` |

The main loop is `core/main_loop.py`: `MainLoop.plan` binds the step file's built acts to the engine's stages at load, and `MainLoop.run` walks them one interval at a time through the register, freezes the interval's start, thaws each act's arrays as its card grants, audits the ledger's words after every act and applies a (ii) card's deferred writes before the first (iv) act after (ii). The engine, `DetectorLawSimulation` in `src/event_universe/events/detector_law.py`, holds the stages, the state and the readings, is built from a loaded world and is handed to the main loop; its `step()` is the main loop's `run`. The Node's six Ports are `core/ports.py`.

The law's interval has five places, and every card declares one of them (the table below). The interval's order lives in one data file shared by every world, `law/step.json` (`src/event_universe/core/step.py` reads it): an ordered list of acts, each `[place, name]` or `[place, name, words]`, a primitive's name at its declared place with the words of its call; a name has one place and may have several acts, told apart by their words (the hold has two: `{"advance": false}` after the hop, `{"advance": true}` after the records). The loop's `step()` walks the file: the clock, then each built act in the file's order through `register.at(name, place)`, bound at load to the loop's stage of that name (the hop per body; the hold's first act; the records' pass under "the operation", the bodies' own records with the excitation rung and then every light record's fused step with its booking and its click inline, so (ii) is interleaved per record inside (i); the giving after the windows' close; the hold's second act, carrying the held families' records, the hold and the pace guard; the spin's step per body), then the interval's closing, which is the loop's own frame and no folder's: the bodies' clocks, the clicked records deleted, the readings. The ten (i) names and the clicks are listed acts: the register is asked for them where the file lists them, and their calls sit inside the records' pass. The recoil is a generic act: a card with a function of its own and no stage of the loop is called once per term of the files naming it, `apply(term, start, own)`, its writes taken by the loop (no term names the recoil today, so nothing is called). Four acts are nested inside the whole-board ones and audited under their own card: the clicks and the giving's window write inside each record's step, the held families' step under the operation's words at (iii), the pace guard under the signed read's. A built name without a stage, an act with words its stage does not take, or a file ordering the record's fused chain otherwise is refused at load by name, never run silently. Every run's output carries the file's digest (`step.hash`); to reorder the whole-board acts, edit the file. The five places, as the cards declare them:

| Place | What happens | The cards declaring it |
| --- | --- | --- |
| (i) | The clicking families' records step by Rule3, every component, with the transport through the Ports. | the operation, the send, the receive, the wait, the degree, the pair, the phase, the self-source, the signed read, the internal representation |
| (ii) | The bookings at the detectors' Ports, the ladder, the takings and the givings. A click writes the body's count at once; only the count's write into the held level waits for the hold at (iv) of the same interval, and there is no queue. | the clicks, the clicks list, the giving, the hand, the lifetime |
| (iii) | The held families' records step by Rule3. | the operation |
| (iv) | The holds are written: each body's count, momentum and spin written into the held families' levels at its Nodes. The hold writes here, then the source: the folder's `apply` on every sourced family, its argument the record family's counts D_i = now^2 - next x before summed at the records' step, the count's write added into the family's level after its own step, the remainder per Node the folder's own; the recoil's act is walked with no term of the files naming it, so no body's momentum changes at a click. | the hold, the source, the recoil |
| (v) | The bodies on one Node: the hop and the spin's step run today; the feed, the induction and the recoil's accumulator are rows not built. | the hop, the spin's step, the feed, the induction, the recoil's accumulator |

The loop is built with the register: it discovers the folders, binds every card that has a binder to one of its own methods or to Rule3, checks the step file against the cards (a primitive the register lacks, one listed at a place it does not declare, or a built one left out is refused), checks the writers and checks every term of the files against the built names. Every whole-board, listed and generic act goes through the register by name and place, `register.at(name, place)`; a call at another place, or at one the file does not list, is refused. The main loop's guards, at run time: every array of the interval's start (the records', the bodies' own records' and masks, the held families', the pair arrays, the detector map, the spans, the paces' carries and the held levels) is read-only for the whole walk (an array an act rebinds, a record's stepped level, is frozen after that act for the acts after it), and an act writes in place only into the arrays its card grants (the hop the pair arrays and the detector map, the hold the held families' arrays, the operation the remainders); a write elsewhere is refused under the act's name; after every act the changed ledger words (a body's content, momentum, spin, position and remainders, the records' and the held families' levels by identity, the tallies, the paces, the records alive) must be among the act's card's writes, else the act is refused by word and target; two writers of one value and target in one interval must follow the file's order of the writers, else refused; a write of a body's value a card makes at (ii) is deferred and applied before the first (iv) act after (ii). A read leaves no trace, so the reading side is the law's words: a right-side card reads the start, a step card writes now, an after-the-step card's writes enter later; the primitives' bookkeeping (a body's wait, its window, the record's residue, wheel, age and box) has no ledger word yet and is listed, not audited. The audit stamps an array by its identity, so an in-place write into a thawed array passes it and the freeze alone guards it: the giving's window write adds the emitter's levels into the record's own stepped array inside the operation's act, under the giving's card, and its audit stamps that record's words. The giving's three acts are the folder's `apply` (features/giving) through the function the walk looked up for the interval: the open's count of the given family at the body, the write's level at the body's Nodes and the close's decision on the outward norm summed over the window; the loop keeps the record's birth, its giving line and the writes on the GameBoard, and the share of the body's momentum the open returns is not applied until the shipped worlds' re-record is decided. The signed read stays the loop's own read (`content_of` of features/signed_read) until the owner's word on the guard's upper side: the folder's `apply` refuses seventeen of the twenty-two shipped worlds, whose matter family reads a content one to seven units below zero beside the bodies (the pace above the edge P = Gamma of the pair [1, 1]). No act is named in the main loop: the loop's stage of the giving declares that it creates records (the records alive change under it; the law's named values of a card do not include them), and the chain check exempts the one whole-board act whose stage carries the chain's names. Two primitives that write the same value at the same place are ordered by the file (a body's value a click writes at (ii) is ordered among the writers of (iv), the write deferred from (ii) first); a card carries no order; a remainder is the writer's own and never collides.

The step is a bijection but for the click: `step_inverse` returns the state to the interval before, bit for bit, by Rule3's own backward line, for an interval with no click, no giving and no hop; it refuses a body that has hopped; it keeps the joint inverse's fixed order (the bodies' step back, every family at the interval's start levels, the held families and their hold last), its stage calls through the register; the main loop's guards cover the forward interval alone. There is no click journal; a test steps a click's interval back by hand.

The six Ports (`core/ports.py`): `arrival` gives the level arriving through one Port on the neighbours' addresses (the wrap on a periodic axis, a fill beyond an open face, the Node itself on a folded axis of extent one); `Ports.arrivals` takes the six arrivals of an array once per interval and hands the same six to every reader (the transport's arrival sums, the flux at the detectors' and the bodies' Ports, the shell of a body), the cache cleared at the interval's start and at the two in-place writers of exchanged arrays (the hold and the pair region); `Ports.outward` gives per Port the Nodes of a mask whose Link leaves it. The loop holds no shift of its own; the reads by coordinate that remain (the curls and the gradient of the spin's step, the giving line's read clocks, the moving set's frame, the click's gather, the dipole's write at the six neighbours) are listed here and bind with their folders.

### Rule3

Rule3 is the function `rule3` in `src/event_universe/core/rule3.py`, the only place in the code that holds the rule's arithmetic; beside it the module holds `coefficients` (the rule's integers at a Node), `form_term` (the conserved form's term), `rule_total_bound` (the load-time bound of the line inside int64) and `rungs` (the ladder's rungs). At every Node `rule3` it forms the next level from the level now, the level before, the six neighbours' arrivals and the remainder:

```
w a_next + r' = SUM_axis R_axis (arrival_+ + arrival_-) + S a_now - w a_before + r,  0 <= r' < w
```

The coefficients `R` (one per axis), `S` and `w` come from the family's pair, the Node clock `Gamma` and the paces at the Node. The content at a Node is the sum over the family's `reads` of weight times the read level (by plain) or minus q times weight times the read level (by sign), q the body's sign; the pace is `Gamma` minus the content, and the axis pace is the pace minus the axis content, so a body's count lowers the pace of what it reads and bends the wave. `coefficients` has two forms: the weak-field rule (`R_a = 2 num p_a^2`, `S` from the paces, `w = 6 den Gamma^2`) and the plain first-order rule (`R = num p`, `S = 6 den c`, `w = 3 den Gamma`); the loop steps a held family's record plain and every other record weak-field, and the loader chooses the weak-field bound where `Gamma > 1`. One floor division per Node per step; the remainder stays at the Node. After the hold the loop's guard ends the run when a reading family's content, or content plus an axis content, reaches `Gamma`. The step backward is `rule3` with `direction=-1`: the two levels exchanged and the sum negated, the remainder after carried in and the remainder before given out.

### The state a run keeps

The records, one dict by identity: each keeps its family, now, before, remainder, its residue u, wheel W and running total C, its pace, its first rung per detector, its ladder (the click at (2u + 1) norm against 2 W pace C), its support box, its window flag, count and outward norm, its momentum tally, its pair, its part marks, the second level of a phase-2 family and its twist. Per held family: one record per component, the time part and one silent record per further part, all stepped alike. Per body: its count per family in the loop's held table; its block keeps its own record, its drive, its spin before the step, `fixed`, its clock (count, previous sum, cycle start and length), its hop, its stepped count and the giving's counters. Per detector: its name, its measured body, its face flag, its set name and channel, a map of the Nodes it sits on, the set tables and the one face receiver; the ladder is the record's, and no click count is kept per detector (the runner derives the counts from the `gather` lines). The books: the conserved forms per family, computed in `books()` under `massive_record` and read by the tests alone, never by the step or the runner. Per-Node state beyond the records: the pace remainder per reading family, read family and axis; the dense pair arrays per family and pair; the detector map.

## 3. The folders, their cards and the register

Every primitive is one folder `src/event_universe/features/<name>/__init__.py`. The register (`src/event_universe/core/register.py`) finds the folders at load and reads each folder's card, its `DECLARATION`:

| Field | Meaning |
| --- | --- |
| `name` | the primitive's unique English name, "the hold"; the folder is the name without "the ", the apostrophe dropped, a space or a hyphen an underscore ("the spin's step" is `spins_step`, "the self-source" is `self_source`) |
| `place` | one of the five places, or "any" for a read-only line |
| `reads` | the values it reads, in the ledger's words |
| `writes` | the values it writes |
| `function` | its function where its code lives in the folder (the recoil's and the source's `apply`), or None; a card with both a function and a binder runs the binder's method today (the signed read, the giving) |
| `section` | its line in ALGEBRA.md |
| `word` | the mathematician's reading of its moment: the right side, the step, after the step, or any (the trace); optional, and only a word outside the four is refused |
| `binder` | `bind(loop)`, which gives the loop's method that implements it today while the code still sits in the loop; the operation's binder gives Rule3 itself |

A folder's function has one signature, `apply(term, start, own) -> writes`, declared in `src/event_universe/core/primitive.py`: the term is one line of the files (the primitive's name, its target value, the family or body it acts on, its degree, its weight, its table, and the line's label for a refusal); the start is the interval's read-only state (levels now and before, paces, counts, walls, momenta, the Ports' accumulators); the own is the primitive's own record at the Nodes it acts on, where every remainder of its divisions lives; the writes are whole integers into declared values, now or deferred to the next interval. The loop and `core/main_loop.py` import the declared types for the generic act; each built folder still defines its own term, start, own and writes classes in that shape.

The folders today: the operation (Rule3 itself), the send, the receive, the wait, the hold, the clicks, the clicks list, the count's line, the giving, the recoil, the recoil's accumulator, the source, the signed read, the self-source, the feed, the induction, the spin's step, the degree, the pair, the phase, the hop, the hand, the lifetime, the internal representation, the trace. Nine folders have neither a function nor a binder on main (the clicks list, the count's line, the feed, the hand, the induction, the internal representation, the lifetime, the recoil's accumulator, the trace): a line of the law not built. Section 9 lists every folder with its place, its word, how it runs and its keys of the files, rendered from the cards. The loop's constructor, not the loader, refuses a term of the files naming one, through the register's check of the terms.

The register refuses, at load and by name: a folder without a card or whose folder name is not its declared name's; a dict-form card with an unknown or missing key; a `bind` that is not a function; a name declared twice; a place outside the six or a word outside the four; a step file naming an unknown primitive, listing one at a place it does not declare or leaving out a built one; a term naming a primitive the register does not hold, or one not built; and a call from the loop at a place other than the declared one. There is no version anywhere: a primitive that changes behaviour keeps every shipped world bit for bit or takes a new name.

## 4. The loader and the files

The loader is `src/event_universe/loader/` (`frame.py` the schemas, `world.py` the loop's classes built from the checked values), entered through `src/event_universe/world_files.py` (`parse_nature_beam_world`, `load_world`). The host module reads the three files and hands them to `parse_world_document`, which parses the world's document, checks every key by name and refuses an unknown key, a missing key or an out-of-bound value with a message naming it. The three files are read by `loader/frame.py` against schemas (`core/schema.py` holds the kinds, `loader/cards.py` collects the cards): the world file's own keys by the frame's schema (`WORLD`: an unknown key, a missing key and a wrong kind refused by name, the wording "the world has unknown keys: ..." and "the world lacks keys: ..."), with the universe, the bodies, the detectors, the readings and an inline twist table handed on as written to their readers in `loader/world.py`; the universe's integers by the frame's own, each family's entry by the folders' cards (each key of an entry beyond the frame's `name`, `quantum`, `clock` and `spins_step` is one folder's; section 8 lists every key with the card that declares it); the start file's mode by the frame's. `world.py` then translates the checked entries to its families list and keeps the rules the cards do not state (the three forms of `parts`, the self-source's unit, held or clicking; a key admitted only with another, as `face_depth` on an open face or `probes` under `massive_record`). The bodies and the detectors are read by the frame's schemas of today's form (`BODY`, `EMITTER`, `DETECTOR`) with the families known; `world.py` keeps the rules between keys (its lines are the loop's classes, the translation of the checked entries to them and those rules; the ray law's parse of lamps, tables, transformations, trains, columns, apertures and the covariant readings, its prose, its retired keys and the one engine's flag are deleted) and still writes defaults there: a detector's threshold is 1 (no longer a key), a body that is no well has no `margin` (None, no margin reading); every boundary axis is declared; `fixed`, `age_bound` and a body's `q`, `spin`, `moment` and `twist` are required, no default; a body without `ramp` or `start` has none (0). The acceptance tests for no default and no family name in the loader are green since #1236; the body of 9.120 alone, the word `sourced` and the source world wait on the loop's reads. What remains of `world.py` leaves with the loop's reads of the old form's keys.

### The world file

One experiment is one world file, a JSON object under `examples/events/`. Its keys:

- `shape`: the GameBoard's three sides. `boundary`: the word `open`, or an object with `x`, `y`, `z` each `open`, `periodic` or `closed`, a missing axis open; an open axis requires `face_depth`. `ticks`: the intervals to run, from 0.
- `universe`: the repository path of the universe file (a unit test may write the families inline instead, in the same form, checked against the same cards, the world then carrying the universe's integers itself; with a path those keys are refused). `engine`: the repository path of the start file.
- `measured`: the bodies. Every entry needs `position`, `family`, `amount` (the quanta), `momentum` and `stocks` (the other families it can give); a block also `ramp`, `start`, `pair`, `q`, `spin`, `moment` and `twist`, with `extents` for a box; `kind` only where the family's pair is `"body"`; `seed` on a well and refused on a barrier or on light's kind; `margin` on a well; `clock` beside a profile and under `body_record`; `stock` when the `emitter` (the given family, the receivers, the weight, the twist) gives the body's own family. The keys are the frame's schema `BODY` (`loader/frame.py`, with `EMITTER` for the nested object), checked with the families known: an unknown key is refused by name, the ray law's `phase`, `directions`, `table`, `lamp` and `become` among them; the rules between keys (a block's ramp and start, a well's seed and margin, the emitter's stock) stay `world.py`'s. The law's form of a body is its family, its Nodes, its count per Node and its momentum, and nothing else: the frame's schema `COUNTED` reads it (`family`, `nodes` as one line per Node with its `node` and its `count`, `momentum`, and `spin` and `moment` where declared; at least one Node, no Node twice), a body is written in one of the two forms (by `position` or by `nodes`), and `world.py` refuses the law's form by name until the count's line is bound to the loop.
- `detectors`: each with `name` (required), `positions` and `block`, the index of the body it belongs to in `measured` (the frame's schema `DETECTOR`; the ray law's `threshold` and `reading` are no keys of the file); with `block` the positions are optional (the free Nodes beside the body), without it they are required and may not sit on a body's centre. The face names, the lifetime's name and the reserved prefix are refused as names.
- `readings`: what the run writes beyond its verdict, a list of named entries read by `src/event_universe/core/readings.py`. Each has a `name`, a `kind` and the kind's own keys: `clicks` of a `detector` (labelled DETECTOR); `level` of a `family` at a `node`, `support` (the Nodes whose level is nonzero) and `total` (the sum of absolute levels) of a `family`, `centre` of a `body` (GAMEBOARD); `alive`, the records alive (HOST). A periodic kind takes `every`, its stride from 1: read at the interval 0 and at every multiple of the stride. A reading writes nothing into the run. The refusals name the reading and the key: an unknown or missing key, an unknown kind, an empty or repeated name, a stride below 1, a detector, family or body the world lacks, a Node outside the shape.
- `stamp`: an object with the SHA-256 `hash` of the canonical JSON without the stamp key. It is compared only when a body's `seed` is a profile; a world without a profile needs no stamp, and a wrong one is not refused.
- The loader also requires `N`, `age_bound`, `clock_stamp`, `massive_record`, `body_record`, `engine` and `detectors`, `face_depth` on an open face and `fixed` on every body; `K`, `release` and `width` left the file with the last loader PR (#1236), with the direction table and the flight bound the loop no longer reads; the ray law's `suspension`, `directions`, `direction_bound`, `action`, `meeting`, `massive_rows`, `optical`, `drive_b`, `flow_link`, `centred_step`, `atom_level`, `in_transit` and `covariant_readings` are no keys of the file (refused as unknown). `N` is the phase steps, a power of two from 2 through 65536, read as the emitter's period. The thirteen check-mode worlds and the source worlds do not load on main for these keys (they are AHEAD in the regression record).

### The universe file

One file, `examples/events/universe.json`, names every family and every integer of the universe. Every world names it, and every family is on in every run; a world cannot turn a family off.

- `integers`: `node_clock` (Gamma, the pace of an empty Node), `amplitude_bound` (the largest level), `Lambda` (the weight of a read by sign), `momentum_unit`, and the `twist_table`: exactly `unit` (4 x node_clock x 2^16), `fine` (2^10 triples) and `coarse` (1 to 2^15 triples), each triple [c, s, d] with c^2 + s^2 = d^2 and d up to 10^9, the first [1, 0, 1], the angles rising, every product inside int64.
- `families`: one entry per family, at most twenty. Each has `name`, `sign` (the sign on its quantum, -1, 0 or 1, the signed read's card), `parts` (`[1]`, `[1, 3]` or `[1, 3, 6]`), `phase` (1 or 2), `pair` (two integers, or `"body"` for the family of bodies), `quantum` (an integer from 1, the family's quantum, the weight of its quanta in a body's count; the clicks card's copy agrees with it), `clock` where the family declares one (the pair form `[p, q]` of its phase per interval of age, the frame's key; a held family declares none), `spins_step` (`curl` and `tidal`, two pairs, the spin's step's weights; the frame's key, required on a family that holds the spin's dipole and read by the spin's step's folder; the leapfrog's span is core's one name, never a key), `reads` (each exactly `family`, `weight` an integer or the name of one of the universe's integers, `twist` an integer from 0 or `"own"`, `by` 1 or `"q"`), `self_source` (`unit` 0 for off, else at least 24 x amplitude_bound), and `held` (`count` content or sign, its `factors` per part, and its `dipole` with `dipole_div`, the divisor required with the dipole) or `clicks` (`gives`, `takes`, `quantum`) or `sourced` (the source folder's card: `of` a record family, `weight`, `scale`, `cap` where a table caps it; carried to the loop as the family's source term), at least one of the three. `sourced` passes the frame (the source folder's card declares it) and the loop reads it nowhere yet; its fragment in `examples/events/source/universe_entries.json` shows the form. The loop's families are built from the checked entries in `world.py` (`_families_of`: the rules between keys, a held family's shape, the reads by name to indices); no translation stands between the file and the loop.

### The start file

`examples/events/engine_start.json` holds the run's parameters, today one key, `mode`, `check` or `pin`: under `check` the runner refuses a pins file, under `pin` it requires one; the shipped file says `check`.

### The output

`tools/run_inputs.py` writes one file per world, `<name>.output.json`: its `format`, the input's name and stamp, the verdict (`LAWFUL`; `REFUSED` with the reason, written only for an exception at load or at the loop's construction; or `LEAK` when a family with no source moved), the ticks, the mode, the records alive, every click with its detector, interval, record and giving, the count per detector, the comparison per registered pin (its kind, the pin, the band, the value read, `MATCH` or `MISS`), and `readings`, the declared readings in their order, each with its name, kind, label, target, stride and lines. `REFUSED` and `LEAK` carry no clicks, counts or pins. A refusal during the run (the pace guard, a body off the GameBoard, the amplitude bound, a twist beyond the table) is raised from the step and aborts the command with a traceback, with no verdict written. The engine's event lines (giving, the body's clock, block, gather, probe, mode) go to an optional observer; the runner passes none and builds the clicks from the `gather` lines alone. A click is a measurement. The engine's state stream (`snapshot_stream`: the interval, the bodies' contents, the held families' levels, the records' integers, under the files' names) and the books are GameBoard readings, diagnostics for the tests and the record; they are never compared with nature.

## 5. The gates

Every pull request runs `python tools/check.py --base <the base commit>` (the one CI file, `.github/workflows/check.yml`). The tool selects the changed files and their consumers, runs `ruff`, `ruff format --check`, `mypy` on the typed modules and `pytest` on the selected tests, and adds four gates on every change:

| Gate | Test | What it holds |
| --- | --- | --- |
| Regression | `tests/test_shipped_worlds.py` | Every shipped world under `examples/events/` (a file with a shape, ticks and a universe, the AHEAD folders check_mode and source left out: 22 worlds) is replayed for its recorded intervals (its ticks where the run projects within 12 seconds, else the smaller of the ticks and 200) and compared bit for bit with `tests/shipped_worlds.json`, a digest of what the run is under the files' names. A moved digest is a changed run, and a world added, removed or changed without a re-record fails; an intended change re-records in the same commit with `tools/record_shipped_worlds.py` and says why. Until the one generator builds the worlds from zero, this record guards the code against unintended change only; it is no physical reference. |
| Genericity | `tests/test_genericity.py` | A seeded generator draws one to twenty families with random English names and random admitted attributes; every draw loads and runs, and five properties hold: renaming the families leaves the run bit for bit, reordering them leaves it bit for bit, a family with no source stays exactly zero, Rule3's conserved form holds where no click and no load acts, and the backward run returns the start. |
| Code shape | `tests/test_code_shape.py` | The ratchet against the merge base, read from git (no baseline file): a file of `src/` within the limits (every docstring one line, no record reference, under 400 lines, no Rule3 arithmetic outside `core/rule3.py` and no shift across Nodes anywhere) passes; a file beyond them grows no count, and a new one stays within them. No new copied function, and an internal of the loop imported by no more files than at the merge base. A feature folder imports `core/` or its own package and never another feature; `core/` imports the standard library alone, handles the arrays by their own methods, and imports nothing of the package outside itself; the one shift across Nodes is `core/ports.py`'s `arrival`, and the three tokens of a shift (`np.roll(`, `._shift(`, `.take(`) are counted in every other file. |
| Language | `tests/test_repository_language.py` | Every file of the repository is written in Latin script: the gate rejects Hebrew and six other scripts, ASCII paths and identifiers included; it detects scripts, not language, so a reviewer still reads the English. The hygiene and navigation tests beside it keep one canonical copy of each file and every link and anchor of the entry documents live. |
| Ownership | `tests/test_ownership.py` | One owner per area (`tools/owners.json`, `tools/ownership.py`): a pull request that touches another owner's area fails unless its body carries that owner's line `HANDED BY <owner>: <files>`, or the Boss's, which covers any area; the author is the owner whose session link is the body's last one, and a path in no area is free. |
| Documents | `tests/test_documents.py` | Only the three, the skills and the entry files exist; each of the three stays under its line cap with no history marker; sections 8 and 9 of this page equal what `tools/render_documents.py` renders from the tree; every path a document or a skill cites in backticks exists, and a decision line naming an absent path says "ahead of the tree". |
| The tests' shape | `tests/test_tests_shape.py` | `tests/` holds no more lines than at the merge base; no test imports a test; the copied setups, the docstrings beyond three lines, the history markers and the retired skips stay at or below the merge base's counts (`tools/tests_shape.py`). |
| Engine gates | `tests/test_engine_gates.py` | No new number, no family name and no unapproved module of `core/` in `src/` (`tools/engine_gates.py`). |
| The step and the cards | `tests/test_step_drives_the_loop.py`, `tests/test_folder_cards.py` | In one interval of a shipped world every built act of `law/step.json` is looked up once, in the file's order, and no built primitive runs outside an act; every card loads with the step file, and no card is built by position beyond the merge base. |
| Runtime guards | `tests/test_runtime_guards.py` | No assert as a runtime guard and no unused module-level name in `src/` and `tools/`. |

The acceptance tests state what the finished engine must satisfy: `tests/test_engine_acceptance.py`, no family name, no integer of the universe, no default, no flag and no version in the code, the rule as one function; `tests/test_loader_acceptance.py`, the same three on the loader alone, a body loaded by its four attributes alone, the words `sourced` and `readings` loading, an unknown key refused by name, and every key of a family's entry declared on one folder's card and written nowhere in the loader. A test the code fails today is marked xfail strict, with the reason; it turns green when the cut lands and then loses its mark.

`python tools/check.py --full` runs everything. CI (`.github/workflows/check.yml`) runs a plan job, `check.py --plan`, then one job per shard, `check.py --shard`: the selected suite in three parts and, where a world runs, the three heaviest shipped worlds each alone and the rest in two parts; a draft's pushes run nothing. Only the Boss merges into `main`, on green.

## 6. How to run a world

1. Write or pick a world file under `examples/events/`, naming the shipped universe and the start file. A generator writes the file and its stamp; a world with a profile body is refused at a wrong stamp.
2. Run it headless, one output file per world:

```
PYTHONPATH=src python tools/run_inputs.py --out runs/inputs --jobs 4 examples/events/<folder>/<world>.json
```

`--out` and `--jobs` are required. The command prints one JSON summary line per input and exits 0 only when every input is `LAWFUL`.

3. Read the output file: the verdict first. `REFUSED` names the key or value the loader refused. `LEAK` names the family that moved without a source. `LAWFUL` carries the clicks and the counts.
4. A pin (an expected count, first click or mean interval at a detector, with its band) is written in a pins file before the run, an object keyed by the input's file stem, and passed with `--pins`; the output then says `MATCH` or `MISS` per pin, and a detector with no click reads None and is `MISS`. A run is compared with a pin only on the owner's Go.
5. To record a world into the regression record, run `PYTHONPATH=src python tools/record_shipped_worlds.py` and commit the record with the world.

The engine never draws or renders in a run; a display reads the output afterwards.

## 7. How to add a feature

1. Read the primitive's line in ALGEBRA.md. The mathematician writes it; a primitive without a line is not built.
2. Make one folder, `src/event_universe/features/<name>/__init__.py`, on a short branch from `main`. Write its card, `DECLARATION`, with the name, the place, the reads, the writes, the section and the word; its act in the interval is one line of `law/step.json`, the core's, at its place. Write `apply(term, start, own) -> writes` with whole integers and its own remainders in `own`; write `check` for its refusals by name. Touch no shared file: the register finds the folder.
3. Keep the shape: every docstring one line (what it does and its ALGEBRA.md line), no record number, under 400 lines, no Rule3 arithmetic outside `core/rule3.py`, no shift of a level across Nodes outside the transport. Import `core/` alone.
4. Write its small test beside it, `tests/test_feature_<name>.py`: the line on the run files' numbers, the refusals, the inverse bit for bit, the hand identity of one Node.
5. Write its run files: a world under `examples/events/<name>/` with its stamp, the universe's fragment as a separate file if it adds a family word (appending to `universe.json` moves every recorded digest), and the blind expectations in the folder's `expectations.json`, beside the world, before any run. While the loader lacks the word, the folder is listed AHEAD in `tools/record_shipped_worlds.py` and in `tests/test_families_file.py`.
6. Run `python tools/check.py --base origin/main`. With the new primitive undeclared in the files, every shipped world must come out bit for bit; the regression gate says so.
7. Open the pull request. The mathematician approves the line with `APPROVED-MATH` on the pull request; the Boss merges on green. The loop's call of the new primitive at its place is the core's cut, Main Loop's, in its own pull request.

<!-- generated: the run's files -->
## 8. The run's files, key by key

Rendered by `tools/render_documents.py` from the frame's schemas (`src/event_universe/loader/frame.py`), the folders' cards and the shipped output; a hand edit fails the documents gate. A key the frame does not name and no card declares is refused by name; the rules between keys (a key admitted only with another) stay in section 4.

### The world file

| key | required | kind |
| --- | --- | --- |
| `shape` | required | a list of 3, each an integer from 1 |
| `boundary` | required | one of `open` or an object with `x` (one of `open`, `periodic`, `closed`), `y` (one of `open`, `periodic`, `closed`), `z` (one of `open`, `periodic`, `closed`) |
| `ticks` | required | an integer from 0 |
| `engine` | required | a word |
| `stamp` | optional | an object with `hash` (a word) |
| `face_depth` | optional | an integer from 1 |
| `age_bound` | required | an integer from 1 |
| `probes` | optional | a list, each a list of 3, each an integer from 0 |
| `mode_axis` | optional | one of `x`, `y`, `z` |
| `amplitude_bound` | optional | an integer from 1 |
| `node_clock` | optional | an integer from 1 |
| `momentum_unit` | optional | an integer from 1 |
| `N` | required | an integer from 2 |
| `clock_stamp` | required | true or false |
| `massive_record` | required | true or false |
| `body_record` | required | true or false |


Handed on as written to their readers, once the world's own keys are checked:

| key | required | what it holds |
| --- | --- | --- |
| `universe` | required | the repository path of the universe file |
| `measured` | required | the bodies, each in one of the two forms below |
| `detectors` | required | the detectors, below |
| `readings` | optional | the readings, below |
| `twist_table` | optional | an inline world's twist table, the universe file's form |


#### A body by its position (today's form)

| key | required | kind |
| --- | --- | --- |
| `position` | required | a list of 3, each an integer from 0 |
| `family` | required | a family's name |
| `amount` | required | an integer from 1 |
| `momentum` | required | a list of 3, each an integer |
| `stocks` | required | an object mapping a family's name to an integer from 1 |
| `fixed` | required | true or false |
| `kind` | optional | a list of 2, each an integer from 1 |
| `q` | optional | an integer |
| `spin` | optional | a list of 3, each an integer |
| `moment` | optional | a list of 3, each an integer |
| `twist` | optional | an integer from 0 |
| `side` | optional | an integer from 1 |
| `extents` | optional | a list of 3, each an integer from 1 |
| `pair` | optional | a list of 2, each an integer from 1 |
| `seed` | optional | an integer from 0 or a list, each an integer |
| `clock` | optional | a list of 2, each an integer from 1 |
| `proper_clock` | optional | a list, each a list of 2, each an integer from 1 |
| `ramp` | optional | an integer from 0 |
| `start` | optional | an integer from 0 |
| `margin` | optional | a word |
| `emitter` | optional | an object with `family` (a family's name), `receiver` (a word or a list, each a word, optional), `period` (an integer from 1, optional), `norm` (an integer from 1, optional), `weight` (an integer from 1, optional), `norm_denominator` (an integer from 1, optional), `window_read` (an integer, optional), `clock` (an integer from 1 or a list of 2, each an integer from 1, optional), `pair` (an integer from 1 or a list of 2, each an integer from 1, optional), `twist` (an integer from 0) |
| `receiver` | optional | a word |
| `stock` | optional | an integer from 1 |


#### A body's emitter

| key | required | kind |
| --- | --- | --- |
| `family` | required | a family's name |
| `receiver` | optional | a word or a list, each a word |
| `period` | optional | an integer from 1 |
| `norm` | optional | an integer from 1 |
| `weight` | optional | an integer from 1 |
| `norm_denominator` | optional | an integer from 1 |
| `window_read` | optional | an integer |
| `clock` | optional | an integer from 1 or a list of 2, each an integer from 1 |
| `pair` | optional | an integer from 1 or a list of 2, each an integer from 1 |
| `twist` | required | an integer from 0 |


#### A body by its Nodes (the law's form)

| key | required | kind |
| --- | --- | --- |
| `family` | required | a family's name |
| `nodes` | required | a list, each an object with `node` (a list of 3, each an integer from 0), `count` (an integer from 1) |
| `momentum` | required | a list of 3, each an integer |
| `spin` | optional | a list of 3, each an integer |
| `moment` | optional | a list of 3, each an integer |


#### A detector

| key | required | kind |
| --- | --- | --- |
| `name` | required | a word |
| `positions` | optional | a list, each a list of 3, each an integer from 0 |
| `block` | optional | an integer from 0 |


#### A reading

Every reading has a `name` and a `kind`; the kind takes its own keys (`src/event_universe/core/readings.py`).

| kind | label | its keys |
| --- | --- | --- |
| `clicks` | DETECTOR | `detector` |
| `level` | GAMEBOARD | `family`, `node`, `every` |
| `support` | GAMEBOARD | `family`, `every` |
| `total` | GAMEBOARD | `family`, `every` |
| `centre` | GAMEBOARD | `body`, `every` |
| `alive` | HOST | `every` |


### The universe file

Two keys: `integers`, `families`.


#### The integers

| key | required | kind |
| --- | --- | --- |
| `node_clock` | required | an integer from 1 |
| `amplitude_bound` | required | an integer from 1 |
| `Lambda` | required | an integer from 1 |
| `momentum_unit` | required | an integer from 1 |
| `twist_table` | required | an object with `unit` (an integer from 1), `fine` (a list, each a list of 3, each an integer), `coarse` (a list, each a list of 3, each an integer) |


#### A family's entry

Each key beyond the frame's is one folder's, declared on its card.

| key | required | kind | declared by |
| --- | --- | --- | --- |
| `name` | required | a word | the frame |
| `quantum` | required | an integer from 1 | the frame |
| `clock` | optional | a list of 2, each an integer from 0 | the frame |
| `spins_step` | optional | an object with `curl` (a list of 2, each an integer from 1), `tidal` (a list of 2, each an integer from 1) | the spin's step |
| `clicks` | optional | an object with `gives` (true or false), `takes` (true or false), `quantum` (an integer from 1) | the clicks |
| `parts` | required | a list, each an integer from 1 | the degree |
| `held` | optional | an object with `count` (one of `content`, `sign`), `factors` (a list, each an integer from 1), `dipole` (one of `spin`, `moment`, optional), `dipole_div` (an integer from 1, optional) | the hold |
| `pair` | required | a list of 2, each an integer from 1 or one of `body` | the pair |
| `phase` | required | one of `1`, `2` | the phase |
| `self_source` | required | an object with `unit` (an integer from 0) | the self-source |
| `sign` | required | one of `-1`, `0`, `1` | the signed read |
| `reads` | required | a list, each an object with `family` (a family's name), `weight` (an integer from 1 or the name of one of the universe's integers), `twist` (an integer from 0 or one of `own`), `by` (one of `1`, `q`) | the signed read |
| `sourced` | optional | an object with `of` (a family's name), `weight` (an integer), `scale` (an integer from 1), `cap` (an integer from 1, optional) | the source |


### The start file

| key | required | kind |
| --- | --- | --- |
| `mode` | required | one of `check`, `pin` |


### The step file

`law/step.json`: an object with the one key `interval`, a list of acts, each `[place, name]` or `[place, name, words]`, a primitive's name at its declared place with the words of its call; a name has one place; no act twice. The acts as the file lists them today are in section 9.


### The pins file

An object keyed by the input's file stem; each pin has a `detector`, one of `count`, `first_click` or `mean_interval`, and a `band`; passed to `tools/run_inputs.py` with `--pins`, refused under the mode `check`, required under `pin`.


### The output file

One file per world, `<name>.output.json`, as `examples/events/massive_record/light_clock.output.json` shows it (4800 intervals, the verdict `LAWFUL`).

| key | in the shipped output |
| --- | --- |
| `clicks` | a list of 167 |
| `counts` | an object with `at_well` |
| `format` | `one-command-output-v1` |
| `input` | `light_clock.json` |
| `mode` | `check` |
| `name` | `light_clock` |
| `pins` | an empty list |
| `readings` | an empty list |
| `records_alive` | the integer 18 |
| `stamp` | an object with `hash` |
| `step` | an object with `hash` |
| `ticks` | the integer 4800 |
| `verdict` | `LAWFUL` |

Each click:

| key | in the first click |
| --- | --- |
| `detector` | `at_well` |
| `giving` | the integer 27 |
| `interval` | the integer 268 |
| `record` | the integer 2 |
<!-- end -->

<!-- generated: the state of the engine -->
## 9. The state of the engine

Rendered by `tools/render_documents.py` from the register, `law/step.json`, the tests' marks, `tools/owners.json` and `tests/shipped_worlds.json`; a hand edit fails the documents gate.

### The primitives

25 folders under `src/event_universe/features/`: 16 built, 7 of them running their own code; 9 not built. The register reads every card at load; a term of the files naming an unbuilt primitive is refused.

| primitive | place | word | how it runs | its keys of the files | its line in ALGEBRA.md |
| --- | --- | --- | --- | --- | --- |
| **the clicks** | (ii) | after the step | bound through the loop's `bind` | `clicks` (a family's entry) | 9.25 (2), (3); 9.111 items 1, 2 and 6; 9.117 items 2 and 3 |
| **the clicks list** | (ii) | after the step | not built |  | 9.88 (4) |
| **the count's line** | (ii) | after the step | not built |  | 9.121 item 3; 9.119 item 1; 9.57 (1) |
| **the degree** | (i) | the step | bound through the loop's `bind` | `parts` (a family's entry) | 9.86 (2); 9.91 (2) |
| **the feed** | (v) | after the step | not built |  | 9.117 item 2; 9.78 (4); 9.91 (8) (v) |
| **the giving** | (ii) | after the step | its own `apply` |  | the close of the count the click's inverse, the bulk share from the rule 9.57 (1), the window's write beyond (H) (9.117 item 5); 9.117 item 2, the row 'the giving'; 9.107; 9.71 (1); 9.116 item 5; 9.86 (1) |
| **the hand** | (ii) | after the step | not built |  | 9.88 (5) |
| **the hold** | (iv) | the right side | its own `apply` | `held` (a family's entry) | 9.45 (2); 9.91 (3); 9.111 item 3; 9.117 item 3; 9.119 item 2, the row 'the hold' |
| **the hop** | (v) | after the step | bound through the loop's `bind` |  | 9.117 item 2; 9.52; 9.104 item 6 |
| **the induction** | (v) | after the step | not built |  | 9.117 item 2; 9.78 (4); 9.91 (8) (v) |
| **the internal representation** | (i) | the right side | not built |  | 9.88 (7) (i); 9.101; 9.117 item 3 |
| **the lifetime** | (ii) | after the step | not built |  | 9.88 (3); 9.117 item 3 |
| **the operation** | (i) | the step | bound through the loop's `bind` |  | 9.57 (1); 9.112 items 1 and 2 |
| **the pair** | (i) | the step | bound through the loop's `bind` | `pair` (a family's entry) | 9.57 (1); 9.111 item 7 row 1 |
| **the phase** | (i) | the step | bound through the loop's `bind` | `phase` (a family's entry) | 9.91 (2) |
| **the receive** | (i) | the step | its own `apply` |  | 9.112 item 1; 9.96 (2) (e); 9.117 item 3; 9.119 item 2, the row 'the receive' |
| **the recoil** | (iv) | after the step | its own `apply` |  | from the rule 9.57 (1) and the click, the store a remainder of the division on the record (9.117 item 5); 9.117 item 2, the row 'the recoil'; 9.84 (2); 9.91 (4); 9.111 items 1 and 2 |
| **the recoil's accumulator** | (v) | after the step | not built |  | 9.117 item 2; 9.109 item 2 (b); 9.96 (2) (e) |
| **the self-source** | (i) | the right side | its own `apply` | `self_source` (a family's entry) | 9.78 (3); 9.88 (2); 9.91 (5); 9.119 item 2, the row 'the self-source' |
| **the send** | (i) | the step | bound through the loop's `bind` |  | 9.112 item 1 |
| **the signed read** | (i) | the right side | bound through the loop's `bind`; its own `apply` waits | `sign` (a family's entry), `reads` (a family's entry) | from the rule 9.57 (1) and the click (9.117 item 5); 9.117 item 2, the first row; 9.78 (4); 9.108 items 8, 11, 12, 13; 9.116 items 4a and 4c |
| **the source** | (iv) | the right side | its own `apply` | `sourced` (a family's entry) | the field's shape from the rule 9.57 (1), the write beyond (H) (9.113 item 2; 9.117 item 5); 9.117 item 2; 9.108 items 3, 10, 11, 13; 9.116 item 4b |
| **the spin's step** | (v) | after the step | its own `apply` | `spins_step` (a family's entry) | 9.117 item 2, the row 'the spin's step'; 9.78 (5); 9.104 (2); 9.119 item 2 |
| **the trace** | any | any | not built |  | 9.112 item 5; 9.117 item 2 |
| **the wait** | (i) | the step | bound through the loop's `bind` |  | 9.112 item 1 |


### The step file's acts

`law/step.json`, digest `777bbb80bd0456a004e4f3d8260dc2e6c3f28d0d82ce51ae8540cabd9c81c275` (written into every output as `step.hash`): 25 acts, of which 17 are built and walked.

| # | place | primitive | words | built |
| --- | --- | --- | --- | --- |
| 0 | (v) | the hop |  | yes |
| 1 | (iv) | the hold | {"advance": false} | yes |
| 2 | (i) | the pair |  | yes |
| 3 | (i) | the degree |  | yes |
| 4 | (i) | the signed read |  | yes |
| 5 | (i) | the send |  | yes |
| 6 | (i) | the wait |  | yes |
| 7 | (i) | the receive |  | yes |
| 8 | (i) | the internal representation |  | no |
| 9 | (i) | the self-source |  | yes |
| 10 | (i) | the phase |  | yes |
| 11 | (i) | the operation |  | yes |
| 12 | (ii) | the clicks |  | yes |
| 13 | (ii) | the lifetime |  | no |
| 14 | (ii) | the giving |  | yes |
| 15 | (ii) | the clicks list |  | no |
| 16 | (ii) | the hand |  | no |
| 17 | (iv) | the hold | {"advance": true} | yes |
| 18 | (iv) | the source |  | yes |
| 19 | (iv) | the recoil |  | yes |
| 20 | (v) | the feed |  | no |
| 21 | (v) | the induction |  | no |
| 22 | (v) | the spin's step |  | yes |
| 23 | (v) | the recoil's accumulator |  | no |
| 24 | any | the trace |  | no |


### The expected failures

Each mark names what the tree does not do yet; it comes off when the cut lands.

| test | reason |
| --- | --- |
| `tests/test_engine_acceptance.py:166` | the ledger's item 'a signed read weight' (ALGEBRA.md 9.108 (8)): the loader bounds the weight from 1; when the support lands this passes and the mark comes off |
| `tests/test_engine_acceptance.py:267` | the loader still writes defaults for keys of the files; the review after the merge |
| `tests/test_genericity.py:139` |  |
| `tests/test_ledger_items.py:94` | the loader admits `reads`, not the term form [kind, target, of, degree, weight, table] |
| `tests/test_ledger_items.py:123` | the step's four declarations (send, receive, wait, operation) are not read from universe.json |
| `tests/test_ledger_items.py:187` | the guard is the load's alone, from below; a pace above Gamma at run time is not refused |
| `tests/test_ledger_items.py:210` | the recoil is not built; a body's held momentum does not move at a click |
| `tests/test_ledger_items.py:237` | the trace that shows the interval's order is not built |
| `tests/test_ledger_items.py:279` | the start file's `trace` is not read; nothing is traced |
| `tests/test_ledger_items.py:308` | no parallel or active path; the start file's keys are refused |
| `tests/test_loader_acceptance.py:113` | the frame reads the body's form (#1221) and the loop still reads N, age_bound, clock_stamp and the flags massive_record and body_record, which the world of 9... |
| `tests/test_loader_acceptance.py:133` | the frame reads `sourced` from the source folder's card (#1206) and `world.py` carries it as the family's source term (#1236); the fragment's `control` famil... |
| `tests/test_loader_acceptance.py:155` | K, release and width are gone (#1236); the source worlds still carry none of N, age_bound, clock_stamp, massive_record and body_record, which the loader requ... |
| `tests/test_loader_acceptance.py:191` | every key of a shipped family's entry is one folder's card (#1206, #1236) but `spins_step`, the frame's until #1203's card lands; `world.py` still builds the... |
| `tests/test_source_worlds.py:187` | the ledger's source row); LAWFUL when they land |
| `tests/test_toward_nature.py:109` | a giving lowers the live M in the wall W = 3 Q M while n stays, so the moving emitter speeds up and the mirror hops one interval before it from interval 51 (... |


### The owners

One owner per area (`tools/owners.json`); the arbiter is Boss.

| owner | areas |
| --- | --- |
| Nature24 | `src/event_universe/loader/`, `docs/ENGINE.md` |
| Main Loop | `src/event_universe/core/`, `src/event_universe/events/detector_law.py`, `law/step.json`, `src/event_universe/retention.py`, `tools/run_inputs.py`, `tools/record_shipped_worlds.py` |
| Mathematician | `docs/ALGEBRA.md`, `tools/body_generator.py`, `src/event_universe/features/feed/`, `src/event_universe/features/induction/`, `src/event_universe/features/recoil/` |
| Mathematician 2 | `src/event_universe/features/counts_line/`, `src/event_universe/features/hold/`, `src/event_universe/features/spins_step/`, `src/event_universe/features/receive/`, `src/event_universe/features/self_source/` |
| Paper Writer | `paper/`, `tools/check.py`, `tools/every_pull_request.txt`, `tools/engine_gates.py`, `tools/merge_base.py`, `tools/owners.json`, `tools/ownership.py`, `tools/record_code_shape.py`, `tools/tests_shape.py`, `tests/bodies.py`, `tests/running.py`, `tests/worlds.py`, `tests/shipped_worlds.json` |
| Boss | `docs/HIGHLIGHTS.md`, `skills/`, `AGENTS.md`, `README.md`, `CONTRIBUTING.md` |


### The shipped worlds

22 worlds under `examples/events/`, each replayed bit for bit on every pull request that runs a world (`tests/shipped_worlds.json`).

| world | ticks | intervals recorded |
| --- | --- | --- |
| `examples/events/dark_body/bright.json` | 15156 | 200 |
| `examples/events/dark_body/dark.json` | 2400 | 200 |
| `examples/events/massive_record/boxed_clock_side_20_at_rest.json` | 3000 | 200 |
| `examples/events/massive_record/boxed_clock_side_20_moving.json` | 9500 | 200 |
| `examples/events/massive_record/boxed_clock_side_28_at_rest.json` | 3000 | 200 |
| `examples/events/massive_record/boxed_clock_side_28_moving.json` | 9500 | 200 |
| `examples/events/massive_record/deep_well_clock_at_rest_40.json` | 3500 | 200 |
| `examples/events/massive_record/deep_well_clock_speed_third_40.json` | 9500 | 200 |
| `examples/events/massive_record/light_clock.json` | 4800 | 1500 |
| `examples/events/massive_record/muon_moving_clock_at_rest_14.json` | 20500 | 200 |
| `examples/events/massive_record/muon_moving_clock_speed_third_14.json` | 20500 | 200 |
| `examples/events/point_emitter/point_chain.json` | 70992 | 200 |
| `examples/events/point_emitter/point_light_clock.json` | 35304 | 3000 |
| `examples/events/toward_nature/bending.json` | 5600 | 200 |
| `examples/events/toward_nature/lorentz_moving.json` | 3600 | 200 |
| `examples/events/toward_nature/lorentz_moving_long.json` | 5966 | 200 |
| `examples/events/toward_nature/lorentz_rest.json` | 3600 | 1500 |
| `examples/events/toward_nature/lorentz_rest_long.json` | 8206 | 200 |
| `examples/events/toward_nature/redshift_bottom.json` | 6534 | 200 |
| `examples/events/toward_nature/redshift_bottom_long.json` | 10558 | 200 |
| `examples/events/toward_nature/redshift_top.json` | 6150 | 200 |
| `examples/events/toward_nature/redshift_top_long.json` | 9598 | 200 |
<!-- end -->
