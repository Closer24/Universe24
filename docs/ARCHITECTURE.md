# Tensor24: the architecture

The owner's words, through David, Animate and the Boss (2026-10-30, in Hebrew, in translation): "Pass to the writer that everything must be gathered under an architecture document, and to work by it." (09:5x UTC, to David, his 6519867280); "Sofer is preparing an architecture document for the whole system, including the page you and Animate built. Make sure he does it well and clearly, and from there everything is derived. And in the architecture document, every section must be explained: how it works in the clock, how it is in physics in the clicks, how it is on the event board, and what its algebra is." (10:1x UTC, to David, his 6520218195); "Pass it to Sofer, and he embeds it in the architecture document he is building." (10:0x UTC, to Animate, her 6520283599, of the decoder's page); "Find out in the world how architecture documents work for small physical systems like ours, pass it to Sofer, and close together on how he should do it." (10:1x UTC, to David, his 6520277889). This is that document.

**What it is.** The one place the whole system is told as a structure: its parts in the order of the flow, what each part does, what it reads and writes, where it lives in the code, what verifies it and what state it is in. The law ([docs/ALGEBRA.md](ALGEBRA.md)) governs it and the owner decides it; every other page of the system derives its part's place and its layers from here (TENSOR24_NODE.md, TENSOR24_PLAN.md, the decoder's page, [docs/BIG_PICTURE.md](BIG_PICTURE.md), the engine's document [docs/ENGINE.md](ENGINE.md)), and a sentence of one of them that disagrees with this document is that page's to mend, or comes to the writer with the reason. The writer keeps it as he keeps the law: a change of a part, of a wall between folders or of a status is entered here first, and with the owner's word where it touches a line of the law.

**The four layers.** Every section tells its part in four paragraphs, in the order where the part is simplest and each closing the others (the law's principle, line 35, item (10)):

- **Clock:** how it works as clock parts, gears and Meshes.
- **Clicks:** what the clicks read of it, the physics; the physics is after the clicks, never the board's numbers, and the step from the board to the clicks is the delicate one and is named.
- **Event board:** what stands and moves at each Node-clock, Mesh and round.
- **Algebra:** its tensor algebra, whole numbers and Rule3's carry.

Each part then gives its **home** in the code, what it **reads and writes**, its **verification** (the law and the mutant that fails it) and its **status**: BUILT, DERIVED (owed in code only), CHECKED (a probe shows it), OPEN (owed a derivation, by name) or owed (not written). The shape follows arc42 (goals, constraints, context, strategy, building blocks, runtime, concepts, decisions, quality, risks, glossary) with the verification and validation ladder of ASME V&V 10 as the ground of the fourth layers (David's survey, 6520277889): the clock is the conceptual model, the algebra the mathematical model, the event board the computational model, and the clicks what is read against nature.

## A. The whole

**A.1 Purpose and quality goals.** A world that shows what nature shows, in whole numbers, with nothing typed that the clicks must show. The goals, each a line of the law: whole numbers only (line 100); locality, a Node-clock reads itself and its six Meshes and nothing else (line 92); the run back exact, the step on the mirrored state (Postulates 2 and 4); no number beyond 0 and 1 in the code, the numbers standing in the three files; nothing declared, no file names a particle, a mass or a coupling (decision 35); one act at every Node-clock, no special code for a clock or a link (line 90); nature is in the clicks, not in the board (the owner's word of 05:0x UTC, the decoder's page).

**A.2 Constraints.** The law's rules (lines 90 to 106); the gate, which refuses a push that raises a count of any rule ([SCRIBE-GATE-1.md](../tools/derivations/open_items/SCRIBE-GATE-1.md)); the documents' gates; the architect's table of who may import whom (below); only the Boss writes engine code and only Animate the decoder's (decision 40), David derives, the writer keeps the law and the documents, the owner decides.

**A.3 Context.** In: three files of whole numbers (the universe, the piece, the setting). Out: a record of the schema and a ledger beside it. Read: the record by the decoder, and by the visualizer (owed). Beside the run: the law, the gate, the census, the documents' gates, the tests and `tools/check.py`.

**A.4 Strategy.** One act at every Node-clock, the same code at every place; the 24 turns of the cube derived once from the Node-clock's own star; the clicks the only physics.

**A.5 The whole, in four layers.**

- **Clock:** a board of clocks, a torus of Node-clocks, each a train of gears that mesh with its six neighbours through six Meshes, one through each Spoke; time is each Node-clock's own gear rate and no count stands inside it (line 92, item (4)).
- **Clicks:** the great clock reads itself, and a click is the one measurement: a whole click credits a train's whole winding, a split click draws a part by the sizes of the parts, and there is no third kind; nature is read from the clicks alone.
- **Event board:** every round, at every Node-clock, every gear of every row steps once in one pass at its now slot; the state per gear row is the notch now and before and two fine teeth, a and b, r and r_d; nothing is queued or sent between Node-clocks.
- **Algebra:** one tensor operation on arrays: the gather of the neighbours' counts (mesh.pull), the contraction of the readings through the plan and the 24's tables (contract), and Rule3's carry elementwise (step.gear): q, r+ = carry(W (a - b) + s F + K, W, r), a+ = a + q, b+ = a.

```
 world        loader          Node-clock       runner          record       decoder     visualizer
 3 files  ->  runner/files, -> engine/,    ->  runner/run, ->  record/  ->  decoder/ -> (owed)
              board, load      algebra/        rounds, rewind  schema
                                  ^                |
                                  +---- main.py ---+   the one joint between the Node-clock and the runner
```

## B. The parts

### B.1 The world: three files

- **Clock:** the files lay the clocks. The universe: the families (a name, its kinds, its part, its pinion) and the integers den, full_rate and width. The piece: the board's three sides. The setting: the gears laid, a row each, and the number of ticks.
- **Clicks:** nothing physical. A file declares no particle, no mass and no coupling (the law's clause **Nothing is declared**, decision 35, line 35): every particle appears by itself in the clicks, a mass is measured only there (decision 37).
- **Event board:** universe.json (version, integers, trains), piece.json (version, shape), setting.json (version, ticks, gears: rows of train, component, site, a, b, r). No fourth file is a world.
- **Algebra:** whole numbers alone; a side, a part and an integer that counts at least 1; every train, kind, part and site a row refers to is named in the files; the teeth and the grips come from den and full_rate by one formula (the teeth 6 den Gamma^2 and the grip den Gamma^2 per Mesh, Gamma the full rate).
- **Home:** `examples/tensor24/`. **Reads and writes:** read by the loader; written by hand. **Verification:** tests/test_the_tensor24_files.py (the examples hold; each rule refuses its own broken file, by name). **Status:** BUILT.

### B.2 The loader

- **Clock:** it lays the clocks on the board: every site with its six neighbours through six Spokes, the wrap on every axis, and the gears on their rows; it is the Node-clock's initialization from the outside.
- **Clicks:** the record's header names each train's kinds and part as the files lay them, so a click names a train and never a row (schema 1.2); no number of the loader reaches the clicks except through the act.
- **Event board:** the board from the piece's sides (each site's six neighbours, the wrap by Rule3 on each coordinate), the teeth and grips from the universe's integers, the gears laid from the setting, the 24's tables made once at the start.
- **Algebra:** arrays of Python integers; the 24 by Rule3's weight over every matrix of three Spokes; each channel's group sum c u u^T, one invariant line, read in closed form with no seed, no search and no loop (David's tb_seed.py, checked by the writer, 6520003245); the tables' unit stays with the strength, which G3 derives (the writer's three conditions, 6520003245).
- **Home:** `src/tensor24/runner/files.py`, `board.py`, `load.py`; `main.made`; the tool `tools/tensor24_files.py` checks the three files alone. **Reads and writes:** reads the three files, writes the layout and the state's arrays; every departure of the files is named and no record is written past one. **Verification:** tests/test_the_tensor24_load.py, tests/test_the_tensor24_files.py, tests/test_the_tensor24_kinds.py. **Status:** BUILT; the strengths OPEN (G3).

### B.3 The Node-clock

- **Clock:** the one act, every round, at every Node-clock alike: it reads itself and its six Meshes and nothing else (lines 90 and 92); no special code and no specific law for a slowing, a grip, a sending, a receiving, a lengthening, a shortening or a freezing, which are the act's own results (line 90). A gear is a dial, a coarse wheel and a fine tooth; a train is a tensor whose kind is a way the 24 turns act; a held hand with a hairspring in its own Node-clock is what makes a clock of a hand, and its rest beat is its mass.
- **Clicks:** the clicks are the act's outputs: a whole click is the drive's carry of the swept area (term 11, DERIVED, G5), a split click the draw by a rank count over the parts' sizes (term 12, OPEN, G5); the engine writes no click before G5. What the clicks read of the act: the rest beat as a mass, proper time as a clock's own count.
- **Event board:** at every Node-clock and every round the state per gear row is (a, b, r, r_d); the teeth W are the rest plus the metric's 00 slots (decision 41's slot form), each Spoke's grip the rest plus the ii slots at both ends of its Mesh; the round reads the now slot alone, in one pass, with no queue and no send.
- **Algebra:** q, r+ = carry(W (a - b) + s F + K, W, r), with the pull F the sum over the six Spokes of grip times (neighbour minus own), the source J through the plan (the vertex law: each vertex pushes all its legs), the drive (q_d, r_d+) = carry(J, T_d, r_d) and the kick K = T_k s q_d; the run back is the same act on the mirrored state. The thirteen terms, one by one: TENSOR24_NODE.md, section 3.
- **Home:** `src/tensor24/engine/` (contract.py, kinds.py, mesh.py, state.py, step.py) and `src/tensor24/algebra/` (carry.py, ring.py); `src/tensor24/main.py` passes its functions into the runner. **Reads and writes:** reads its own gears and its six Meshes' at the now slot; writes its own state. **Verification:** tests/test_the_tensor24_engine.py (each generic part once with its mutants, then the whole node), test_the_tensor24_generic.py (the whole node as the files lay it), test_the_tensor24_algebra.py, test_the_tensor24_kinds.py, test_the_tensor24_frame.py (the generic properties any engine is read by). **Status:** terms 1 to 4 and 8 BUILT; term 6 the contraction BUILT, its strengths and plan OPEN (G3); term 7 DERIVED (G3); terms 5, 9 and 13 OPEN (G2; the first-order form of term 5 is the Boss's draft N2, f3cbebe0c, for David's reading), term 10 OPEN (G4), term 11 DERIVED and term 12 OPEN (G5).

### B.4 The runner

- **Clock:** it counts the rounds from outside, since no Node-clock holds one; it gives every Node-clock its turn in every round and runs the whole back to see that it returns.
- **Clicks:** none; it writes what the act wrote.
- **Event board:** rounds one after another to the setting's ticks, each a full pass of every Node-clock; the promise (the teeth stand at least 1 and the fine teeth within their teeth) read from outside before each round (line 92); the rewind runs the rounds back by the engine's run back alone, with no log read.
- **Algebra:** the engine's tick, passed in and iterated; the run back the mirrored tick; the start must return bit for bit.
- **Home:** `src/tensor24/runner/run.py`, `rounds.py`, `rewind.py`; the tool `tools/tensor24_run.py` runs the three files to a record and a ledger. **Reads and writes:** reads the loader's layout and state, writes the record and its ledger. **Verification:** tests/test_the_tensor24_run.py (the whole run: the three files to a record the decoder reads). **Status:** BUILT.

### B.5 The record

- **Clock:** the boundary between the board and the clicks: the runner writes it, the decoder reads it, no act reads it (line 92: only the readers read the record).
- **Clicks:** the record is the clicks' only source: its header names each train's kinds and part; its click lines (none before G5) name a train, a Node-clock and a tick; the ledger carries each train's counts.
- **Event board:** JSON Lines, one line per record, its kind its record's name in lower case; for the example world a header, an end and one Count line per round, Node-clock and train (1,280 on the example).
- **Algebra:** whole numbers and labels, nothing computed in it; its width is whole numbers of any size.
- **Home:** `src/tensor24/record/schema.py`, schema 1.2. **Reads and writes:** written by the runner, read by the decoder. **Verification:** the decoder's tests read it under the schema's rules and refuse each broken record by its cause. **Status:** BUILT; the couplings stand empty in the header until schema 1.3 retires them (Animate, 6520283599).

### B.6 The decoder (the decoder's page, embedded)

Animate's page, `tools/derivations/open_items/Decoder4D2Clicks3D.md`, holds the decoder's plan and the mass in full, from the board's events to the clicks and from the clicks to what nature shows; this section is its four layers in the architecture's order, and the page stays the derivation underneath (its parts 1 to 5 and 8). The decoder reads only what the new engine writes.

- **Clock (page part 1):** each reading is a clock's own count or a light link; the clock family's 00 slot is each Node-clock's own teeth; the two clicks told in a clock; the mass, the three hands and uncertainty told in clock parts (1.7 to 1.11).
- **Clicks (page part 2, 1.3, 4.4):** the facts of nature to meet, each read by the clicks and no number of the board: proper time and the twins, the cone checked by click, the books at the click (the conservation, row 15), each later bang showing more (row 46), the mass as the rest beat read through energy differences.
- **Event board (page 4.1, 4.2, 4.5, and the step in 4.3 and 4.6):** the board's space is no fixed space (the Meshes lengthen); the board's numbers cannot be read as nature's; they reach the clicks only as ratios at first order, and as departures of order omega0^2 beyond, and the board holds no unit for the round; the step from the board to the clicks is the delicate one.
- **Algebra (page part 3):** from the star to the metric family, the act in the algebra, what a click carries in kinds, the invariants, four to three in kinds, uncertainty (checked in whole numbers), families standing only in the files, mass on the board as a spring with a coupling (3.7, 3.8).
- **Home:** `src/tensor24/decoder/` (records.py, books.py, bangs.py, measure.py; clocks.py goes with the rate lines no run writes, and family.py, the clock family by the loader's own derivation called read only, is the first to build); the tool `tools/tensor24_decode.py`. **Reads and writes:** reads a record and its ledger, prints each row's verdict (shown, not shown or not read, with its cause); writes nothing. **Verification:** tests/test_the_tensor24_decoder.py, test_the_tensor24_decoder_bangs.py, test_the_tensor24_decoder_cases.py, test_the_tensor24_decoder_measure.py (one per generic part with its mutant). **Status:** the decoder as built reads the record and the ledger whole; every row reads NOT READ until G5 (no click line); the decoder's code is built after the page's approval, from the Boss's head once his cut is whole (the owner's word to Animate, 10:0x UTC: "Wait until he finishes everything, and then work from the branch of the whole system. Bring the decoder's page for approval.").

### B.7 The readings

- **Clock:** the reads of the clicks that the engine's folders share, taken once where they are alike.
- **Clicks:** the same reads, kept out of both the engine and the decoder.
- **Event board:** none.
- **Algebra:** none.
- **Home:** `src/tensor24/readings/`, an empty package; it may import the algebra and the record. **Status:** owed.

### B.8 The visualizer

- **Clock:** the board's clocks drawn as they turn.
- **Clicks:** the clicks drawn where they land, with the decoder's verdicts beside them.
- **Event board:** the Node-clocks, the Meshes and the rounds as the record has them.
- **Algebra:** none: it draws what the decoder reads and computes nothing.
- **Home:** Animate's; the old engine's pages (tools/page.py and tools/bangs_page.py read its record) left with it. **Status:** owed; the new record's visualizer waits on the click lines (G5).

### B.9 The tools

- **Clock:** none; the tools run the parts, they are no part of the clock.
- **Clicks:** `tools/tensor24_decode.py` reads a record's clicks and prints each row's verdict.
- **Event board:** `tools/tensor24_files.py` checks the three files and the load's refusals by name; `tools/tensor24_run.py` runs them to a record and a ledger; each puts `src/` on its path and calls the package.
- **Algebra:** none; no tool holds a formula.
- **Home:** `tools/`. **Verification:** the tests of the parts they call. **Status:** BUILT.

### B.10 The guards, beside the run

- **Clock:** the law's clause **The system is a system of clocks, and it is always checked** (line 106): the guards read every push and every line.
- **Clicks:** the decoder's rows are the validation: what the clicks read is set against what nature shows (part F).
- **Event board:** the tests run worlds on boards (tests/test_the_tensor24_*.py: each generic part once with its mutant, then one test of the whole node on a board, the owner's word to the Boss of 2026-10-30, 09:2x UTC), and `tools/check.py` runs the gates and the tests together.
- **Algebra:** the gate (`tools/derivations/open_items/scribe_scan.py`) is the algebra's law in a script: it refuses a push that raises a count of a number beyond 0 and 1, a float, a root, a loop, a branch, a comparison, a clamp, a mask, an enumeration or a probe with a float, and it enforces the table of who may import whom; the census (`scribe_code_census.py`) counts per file what the whole-number rules forbid; the law's own check (`scribe_law_check.py`, with `--docs`) finds a contradiction between two lines of the law and between the law and a document; the documents' gates (`tools/documents_gates.py`) hold the documents to the tree.
- **Home:** the law, the gate, the census, the checks, the tests. **Status:** BUILT; the tests' cut to one per generic part is the Boss's, and the gate's counts follow it.

## C. One round

**Clock.** A Node-clock reads its six neighbours' counts through its six Meshes, each Mesh read once from both ends; it steps every gear once; it writes only its own state. **Clicks.** Where the carry of the drive completes a whole winding a click leaves, a whole click at the Node-clock that holds the winding, or a split click where two parts share it and the great clock draws; the click is written as one line of the record and lasts one tick (owed from G5). **Event board.** One pass over every Node-clock and every gear row, in this order: the readings and the sources (the value, the gradient along each axis, the pull, the plan's terms: step.sources); the drive (step.drive); the push, the force and the kick (step.driven); the teeth (step.weight); the gear's carry (step.gear). **Algebra.** One tensor operation: the gather (mesh.pull), the contraction through the plan and the 24's tables (contract), the two carries in series, the drive's and the gear's, the only nonlinearity. The run back is the same act on the mirrored state, mirrored again (step.mirror, step.untick), exact where the fine teeth stand within their teeth and the teeth stand at least 1.

## D. The crosscutting concepts

- **Rule3's carry and whole numbers.** *Clock:* a dial turns and what it cannot hold stays at the Node-clock as its remainder. *Clicks:* the quotient leaves as the event, the remainder stays as the memory that makes the run back exact. *Event board:* n + r = q d + r' at every gear, every round. *Algebra:* `algebra/carry.py`, the one place a division is written, with the fine tooth's flip at the mirror.
- **The 24 and the kinds.** *Clock:* the cube's 24 turns exchange and reflect a train's gears; five kinds (A1 the scalar, A2 the pseudoscalar, E, T1 the vector, T2 the shears). *Clicks:* a click names a train and its kind, never a row. *Event board:* the same code at every site, the act alike under the 24's turns of sites and components. *Algebra:* the 24 by Rule3's weight over every matrix of three Spokes, the kinds' matrices, the tables' group sums (`engine/kinds.py`, `runner/load.py`).
- **Locality and no queue.** *Clock:* a Node-clock reads itself and its six Meshes (line 92); no Node-clock sends. *Clicks:* a click's effect travels one Mesh per tick; Bell at a distance stands on two boards. *Event board:* one pass, the order of work and no law (line 98). *Algebra:* the dependency radius of one tick is one Mesh, tested forward and backward.
- **The record's schema.** *Clock:* the boundary between the board and the clicks. *Clicks:* the only source of what nature shows. *Event board:* a header, the clicks, an end, and the ledger's counts. *Algebra:* whole numbers and labels (`record/schema.py`).
- **The promise, read from outside.** *Clock:* the Node-clock holds no round and no time; the promise that the teeth stand at least 1 and the fine teeth within their teeth is read before every round by the runner. *Clicks:* none. *Event board:* checked at the load and before every round. *Algebra:* `step.teeth`, the promise's measure.

## E. The decisions

The law stays the law; a decision is in force as [docs/HIGHLIGHTS.md](HIGHLIGHTS.md) and the law's clauses record it, and the plan's section 14 (TENSOR24_PLAN.md) numbers them. The ones that shape the parts, one line each (status, where): 27 the runner first, the act at the top cancelled, the doubler's hold (APPROVED, line 35); 28 Bell at a distance on two boards (APPROVED, line 35); 29 the product draw, the take by way (b) (APPROVED, line 35); 35 nothing declared (APPROVED, line 35); 36 the same clock and the same ruler for every act (APPROVED); 37 masses are measured only in clicks (APPROVED, line 35); 38 the Node-clock is one generic node (APPROVED); 39 the great clock is the whole metric (APPROVED); 40 the final picture approved and the build resumed, with (a) to (h) (APPROVED); 41 no root and no table in the code, now or later, the metric gears hold the tick's weight (APPROVED, line 35); 42 the Node-clock is independent and disconnected from the world, the 24's tables its own design (APPROVED, line 92); 43 the old engine frozen and the work run with no waiting (APPROVED; the old engine has since left the tree, 2026-10-30, 4cb5359ce).

## F. Verification and validation

- **Code verification:** each generic part is tested once with its mutant, then one test of the whole node on a board (the owner's word to the Boss, 09:2x UTC): the carry and the ring, the kinds and the 24's tables, the contraction with the vertex law, the pull through the Mesh, the run back, the files and the load's refusals, the record under the schema, the decoder's readers; the gate and the documents' gates beside them.
- **Each solution's verification:** the run back exact in its stated domain, the floor and the ceiling of the swing, the step's domain, the act alike under the 24's turns, the grip alike from both ends.
- **Validation:** the facts to meet (the decoder's page, part 2), each read by the clicks and never from the board's numbers, each with its status (shown, not shown or not read); no row can read SHOWN before the engine writes a click (G5).

## G. Risks and the open items

G2: the first-order form of term 5 (N2) and the notch and the frozen clock (terms 9 and 13); G3: the strengths per channel and the plan (the tables' unit, the four-leg form, which families tie to k, the held count's own potential, n's unit); G4: the shift and the shears (term 10); G5: the click as the act's output and the split's draw, with the draw's c (law decision 29 names the Node-clock's beat count, which the build holds none of since G1b); the visualizer and the readings; six counts hidden in label tuples (AXES and GEAR and ADDED in the Boss's code; WAYS, ENDS and a header and end pair in the decoder's) to be read from the star, the piece and the schema; the old spring of line 35, which waits on the owner's rule for the head's notch.

## H. The glossary

The clock words are defined once each in [docs/CLOCK_WORDS.md](CLOCK_WORDS.md) and in the law, each in its own place.

## The trace table

One row each; the gates can read it (the paths and the tests named here exist at the head).

| Part or term | Law line | Code | Test | Status |
|---|---|---|---|---|
| The world's three files | 35 (nothing declared) | examples/tensor24/ | test_the_tensor24_files.py | BUILT |
| The loader | 92 (2) | runner/files.py, board.py, load.py | test_the_tensor24_load.py | BUILT |
| The 24 and the kinds | 94 | engine/kinds.py | test_the_tensor24_kinds.py | BUILT |
| Term 1, the readings | 90 | engine/mesh.py, step.py | test_the_tensor24_engine.py | BUILT |
| Term 2, the teeth W | 35 (decision 41) | engine/step.py | test_the_tensor24_engine.py | BUILT |
| Term 3, the grips | 90 | engine/mesh.py | test_the_tensor24_engine.py | BUILT |
| Term 4, the pull F | 90 | engine/mesh.py | test_the_tensor24_engine.py | BUILT |
| Term 5, the metric's push | 35 (decision 40) | engine/contract.py | test_the_tensor24_engine.py | OPEN (G2) |
| Term 6, the vertex and the spring | 96 | engine/contract.py | test_the_tensor24_engine.py | BUILT the contraction, OPEN (G3) |
| Terms 7 and 8, the drive and the kick | 98 | engine/step.py | test_the_tensor24_engine.py | DERIVED at G3 and BUILT |
| Terms 9, 10 and 13 | 35, 90 | (none yet) | (none yet) | OPEN at G2 and G4 |
| Terms 11 and 12, the two clicks | 35 | (none yet) | (none yet) | DERIVED and OPEN at G5 |
| The whole node | 90 | engine/ and algebra/ | test_the_tensor24_generic.py | BUILT |
| Rule3's carry, the ring | 31 | algebra/carry.py, ring.py | test_the_tensor24_algebra.py | BUILT |
| The runner and the rewind | 92 (4) | runner/run.py, rounds.py, rewind.py | test_the_tensor24_run.py | BUILT |
| The record | 92 (5) | record/schema.py | test_the_tensor24_decoder.py | BUILT |
| The decoder | 35 (decision 37) | decoder/ | test_the_tensor24_decoder_measure.py | built, every row NOT READ until G5 |
| The readings and the visualizer | 106 | readings/ | (none yet) | owed |

## Who may import whom

The architect's table (section 4 of the design approved at eaf07f596); the gate's ISOLATE rule reads it, and the standard library is allowed everywhere, numpy in the engine and the runner alone.

| Folder | May import |
|---|---|
| algebra | algebra |
| record | record |
| engine | algebra, engine, record |
| readings | algebra, readings, record |
| runner | algebra, readings, record, runner |
| decoder | algebra, decoder, readings, record |
| main.py | engine, runner |

## The documents under it

| Document | What it holds | Kept by |
|---|---|---|
| [README.md](../README.md), `llms.txt` | the front page and the short map | Sofer |
| [docs/ARCHITECTURE.md](ARCHITECTURE.md) | this: the parts, the four layers, who may import whom, the trace | Sofer |
| [docs/ALGEBRA.md](ALGEBRA.md) | the law | Sofer, on the owner's word |
| [docs/HIGHLIGHTS.md](HIGHLIGHTS.md) | the decisions in force | Sofer |
| [docs/BIG_PICTURE.md](BIG_PICTURE.md) | the whole told by the clock, the algebra and the physics | Sofer |
| [docs/ENGINE.md](ENGINE.md) | the engine's document | Sofer |
| [docs/UNIVERSE24.md](UNIVERSE24.md) | what the one run must show, and the ledger | Sofer |
| [docs/CLOCK_WORDS.md](CLOCK_WORDS.md), [docs/FURTHER_RESEARCH.md](FURTHER_RESEARCH.md), [docs/FOLLOW_UP_PAPERS.md](FOLLOW_UP_PAPERS.md), [CHANGELOG.md](../CHANGELOG.md) | the clock words, what does not match nature, the papers proposed, what changed | Sofer |
| `tools/derivations/open_items/TENSOR24_NODE.md`, `TENSOR24_PLAN.md` | the Node-clock's terms, and the stages and decisions | the Boss |
| `tools/derivations/open_items/Decoder4D2Clicks3D.md` | the decoder's plan and the mass, derived under B.6 | Animate |
| `tools/derivations/open_items/SCRIBE-GATE-1.md`, `SCRIBE-LAW-AUDIT-2.md`, `SCRIBE-ROUTINE.md` | the gate, the law's check, the keeper's routine | Sofer |

## How each works by it

- **The Boss** builds the engine, the loader and the runner against lines 90 to 106 of the law and the Node-clock's terms, and asks this document where a new function belongs and which folder may import it; he updates the status words of B.1 to B.5 and the trace rows with each push, or says so and the writer does.
- **Animate** works the record, the decoder and the visualizer against the schema and the decoder's page; B.6 is hers to keep true to the page, the writer keeps its form.
- **David** derives: each derivation names the part it serves and tells it in the four layers; a derivation that needs a change of a part's wall or of the law goes to the writer first.
- **Sofer** keeps this document and the law, reads every push against both, and lets the gate hold the table; each push he reads moves the status words that it moves.
- **The owner** decides; no part changes its place or its wall without his word.

## What this document does not hold

The state of the build by the hour, the counts of tests and the numbers of the readings; they stand in `TENSOR24_PLAN.md`, in the ledger of [docs/UNIVERSE24.md](UNIVERSE24.md) and in the thread, and the status words here follow them. The old engine (`src/event_universe`, out of the working tree since 2026-10-30, the owner's word to the Boss, 09:3x UTC: "Yes, all of it now") stands in git's history alone.
