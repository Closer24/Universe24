# Tensor24: the architecture

The owner's word of 2026-10-30, 09:5x UTC, to David (as David records it, his 6519867280; in Hebrew, in translation): "Pass to the writer that everything must be gathered under an architecture document, and to work by it." This is that document. The writer keeps it as he keeps the law: a change to the parts, to who may import whom, or to what a part may hold is entered here first, and with the owner's word where it changes a line of the law ([docs/ALGEBRA.md](ALGEBRA.md)).

**In one sentence.** Three files of whole numbers lay a world; a loader turns them into arrays; every Node-clock steps by one act in every round; a runner repeats the rounds and writes a record of whole numbers; a decoder reads the record into what nature shows. No part holds a float, a root, a table, a loop that makes a formula, or a division that is not Rule3's; no file names a particle, a mass or a coupling.

**How each part is told.** By the clock, the algebra and the physics, starting from the layer that is simplest for the part (the law's principle, line 35, item (10); the owner's words of 2026-10-30, 07:3x, 07:4x and 09:1x UTC). *In clocks* is what the gears and the Meshes do; *in algebra* is the whole-number operation that does it; *in physics* is what the clicks read of it, and the physics is after the clicks, the conversion from the board to them the hard and delicate step.

## The flow

```
 world        loader          Node-clock       runner          record       decoder     visualizer
 3 files  ->  runner/files, -> engine/,    ->  runner/run, ->  record/  ->  decoder/ -> (owed)
              board, load      algebra/        rounds, rewind  schema
                                  ^                |
                                  +---- main.py ---+   the one joint between the Node-clock and the runner

 beside the whole run: the law, the gate, the census, the documents' gates, the tests, tools/check.py
```

## The parts

### 1. The world: three files

- **Where:** `examples/tensor24/` (universe.json, piece.json, setting.json); no fourth file is a world.
- **In clocks:** the files lay the clocks: the universe the families (a name, its kinds, its part, its pinion) and the integers den, full_rate and width; the piece the board's three sides; the setting the gears laid (a row each: train, component, site, a, b, r) and the number of rounds.
- **In algebra:** whole numbers alone; a side, a part and an integer that counts at least 1; every train, kind, part and site a row refers to is named in the files.
- **In physics:** nothing. A file declares no particle, no mass and no coupling (the law's clause **Nothing is declared**, decision 35, line 35): every particle appears by itself in the clicks.

### 2. The loader

- **Where:** `src/tensor24/runner/files.py`, `board.py`, `load.py`; the tool `tools/tensor24_files.py` checks the three files alone.
- **In clocks:** it lays the board (every site, its six neighbours through six Spokes, the wrap on every axis) and the gears on it.
- **In algebra:** the files read and checked, then laid out as arrays of Python integers; the wrap by Rule3 on each coordinate; every coefficient one formula of the files' integers; the 24's tables derived once from the Node-clock's own star, as its initialization act (line 92, item (2)).
- **In physics:** none. Its voice is the refusal by name: every departure of the files is named, and no record is written past one.

### 3. The Node-clock

- **Where:** `src/tensor24/engine/` (contract.py, kinds.py, mesh.py, state.py, step.py) and `src/tensor24/algebra/` (carry.py, ring.py); `src/tensor24/main.py` passes its functions into the runner. The Boss builds it; its terms stand in `tools/derivations/open_items/TENSOR24_NODE.md`, its stages in `TENSOR24_PLAN.md`.
- **In clocks:** one act, every round, at every Node-clock alike: it reads itself and its six Meshes and nothing else (lines 90 and 92); no special code and no specific law for a slowing, a grip, a sending or a freezing (line 90).
- **In algebra:** one division with a carried remainder over one integer contraction of the Node-clock's own gears and its six Meshes' gears; every gear read before any is written; a gear a dial, an integer with a carried remainder; a train a tensor whose kind is a way the 24 turns act (five kinds); the group's action written once, in the table of the kinds, so the 24 holds by construction (lines 90 and 94). carry.py is the one place a division is written (Rule3); ring.py the Gaussian ring, products and sums alone.
- **In physics:** time is each Node-clock's own gear rate and no round or beat count stands inside it (line 92, item (4)); the clicks read what the act did, and nothing of nature is typed.

### 4. The runner

- **Where:** `src/tensor24/runner/run.py`, `rounds.py`, `rewind.py`; the tool `tools/tensor24_run.py` runs the three files to a record.
- **In clocks:** it counts the rounds from outside, since the Node-clock holds none; every Node-clock steps in every round to the setting's ticks.
- **In algebra:** the engine's tick, passed in, run round by round; the rewind runs the rounds back by the engine's run back alone, with no log read, and the start must come back bit for bit; the record and its ledger are written last.
- **In physics:** none.

### 5. The record

- **Where:** `src/tensor24/record/schema.py`, schema 1.2: JSON Lines of whole numbers and labels, each line's kind its record's name in lower case.
- **In clocks:** the boundary between the board and the clicks: the runner writes it and the decoder reads it, and no act reads it (line 92: only the readers read the record).
- **In algebra:** whole numbers and labels, nothing computed in it.
- **In physics:** none: it is the board's account, and the conversion from it to the clicks is the decoder's.

### 6. The decoder

- **Where:** `src/tensor24/decoder/` (records.py, clocks.py, books.py, measure.py, bangs.py); the tool `tools/tensor24_decode.py`; the page `tools/derivations/open_items/Decoder4D2Clicks3D.md`. Animate's.
- **In clocks:** the Node-clocks' ticks read from the rate lines, proper time with no count outside a Node-clock.
- **In algebra:** whole numbers and ratios of them; each reading made twice, from the clicks and from the ledger's clocks, and the two must agree.
- **In physics:** what the clicks show: proper time, the twins, the cone checked by click, the books at the click (the conservation), and each later bang showing more. The conversion from the board's numbers to the clicks is the delicate step.

### 7. The readings

`src/tensor24/readings/`, an empty package, owed: the reads of the clicks that the engine's folders may share. It may import the algebra and the record.

### 8. The visualizer

Animate's. The old engine's pages left with it (tools/page.py and tools/bangs_page.py read its record); the new record's visualizer is owed.

### 9. The tools

`tools/tensor24_files.py` checks the three files, `tools/tensor24_run.py` runs them to a record, `tools/tensor24_decode.py` reads a record. Each puts `src/` on its path and calls the package's functions; none holds a formula.

### 10. The guards, beside the run

- **The law**, [docs/ALGEBRA.md](ALGEBRA.md): the postulates (lines 29 to 35 and on), the Node-clock's lines (80 to 110) and the body; every change of it is the owner's word.
- **Sofer's gate**, `tools/derivations/open_items/scribe_scan.py` ([SCRIBE-GATE-1.md](../tools/derivations/open_items/SCRIBE-GATE-1.md)): refuses a push that raises a count of any rule (a number beyond 0 and 1, a float, a root, a loop, a branch, a comparison, a clamp, a mask, an enumeration, a probe with a float), and enforces the table of who may import whom below.
- **The census** (`scribe_code_census.py`) and **the law's own check** (`scribe_law_check.py`, with `--docs`): the first counts, per file, what the law's whole-number rules forbid; the second finds a contradiction between two lines of the law and between the law and a document.
- **The documents' gates** (`tools/documents_gates.py`), **the tests** (`tests/test_the_tensor24_*.py`: each generic part once with its mutant, then one test of the whole node on a board, the owner's word to the Boss of 2026-10-30, 09:2x) and **`tools/check.py`**, which runs them all, the tests every pull request runs named in `tools/every_pull_request.txt`.

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
| [docs/ARCHITECTURE.md](ARCHITECTURE.md) | this: the parts, who may import whom, who works on which | Sofer |
| [docs/ALGEBRA.md](ALGEBRA.md) | the law | Sofer, on the owner's word |
| [docs/HIGHLIGHTS.md](HIGHLIGHTS.md) | the decisions in force | Sofer |
| [docs/BIG_PICTURE.md](BIG_PICTURE.md) | the whole told by the clock, the algebra and the physics | Sofer |
| [docs/ENGINE.md](ENGINE.md) | the engine's document | Sofer |
| [docs/UNIVERSE24.md](UNIVERSE24.md) | what the one run must show, and the ledger | Sofer |
| [docs/CLOCK_WORDS.md](CLOCK_WORDS.md), [docs/FURTHER_RESEARCH.md](FURTHER_RESEARCH.md), [docs/FOLLOW_UP_PAPERS.md](FOLLOW_UP_PAPERS.md), [CHANGELOG.md](../CHANGELOG.md) | the clock words, what does not match nature, the papers proposed, what changed | Sofer |
| `tools/derivations/open_items/TENSOR24_NODE.md`, `TENSOR24_PLAN.md` | the Node-clock's terms, and the stages | the Boss |
| `tools/derivations/open_items/Decoder4D2Clicks3D.md` | the decoder and the mass | Animate |
| `tools/derivations/open_items/SCRIBE-GATE-1.md`, `SCRIBE-LAW-AUDIT-2.md`, `SCRIBE-ROUTINE.md` | the gate, the law's check, the keeper's routine | Sofer |

## How each works by it

- **The Boss** builds the engine, the loader and the runner against lines 90 to 106 of the law and the Node-clock's terms, and asks this document where a new function belongs and which folder may import it.
- **Animate** works the record, the decoder and the visualizer against the schema and the decoder's page.
- **David** derives: each derivation names the part it serves and tells it by the clock, the algebra and the physics; a derivation that needs a change of a part's wall or of the law goes to the keeper first.
- **Sofer** keeps this document and the law, reads every push against both, and lets the gate hold the table.
- **The owner** decides; no part changes its place or its wall without his word.

## What this document does not hold

The state of the build, the stage list, the counts of tests and the numbers of the readings change by the hour; they stand in `TENSOR24_PLAN.md`, in the ledger of [docs/UNIVERSE24.md](UNIVERSE24.md) and in the thread. The old engine (`src/event_universe`, left the working tree on 2026-10-30, the owner's word to the Boss, 09:3x UTC: "Yes, all of it now") stands in git's history alone.
