# The engine

This document describes the engine as the code holds it on `main`, beside [ALGEBRA.md](ALGEBRA.md) (the law) and [HIGHLIGHTS.md](HIGHLIGHTS.md) (the decisions in force). The engine is the law's implementation and nothing else (the owner's decision (c) of 2026-09-29 on #1495): a GameBoard of Nodes, every family's NodeState at every Node, and one interval of five acts, each a call of Rule3 (`src/event_universe/core/rule3.py`) on whole-board arrays, every neighbour read through a Port (`src/event_universe/core/ports.py`). The engine holds no number, no formula, no family's name and no flag: every physical value comes from the run's files.

## 1. The words

- **Node**: one place of the GameBoard. Its whole local information is its **NodeState**, the law's own numbers and nothing else (section 2).
- **Port** and **Link**: a Node has six Ports, +x, -x, +y, -y, +z, -z; a Link is the pair of Ports between two neighbours. A level reaches a neighbour only through a Port (`arrival`). An axis is periodic (it wraps), closed (a wall, read as 0) or open (a wall read as 0 whose outer layer of `face_depth` Nodes is told to report); an axis of one layer folds, its two Ports returning the Node itself.
- **GameBoard**: the box of Nodes, `shape` [X, Y, Z]; in code `GameBoard` (`src/event_universe/game_board.py`).
- **Family**: one kind of physical value, a row of the universe file: its name, its pair [num, den] and what it holds (`held`: the content or the sign, at the divisor E_s). The rule derives the rest ([ALGEBRA.md, the families from the rule](ALGEBRA.md#a-familys-declaration), `src/event_universe/loader/derived.py`): a family that does not hold the content carries quanta (two levels, a count, a current); a held family has its parts, 1, 1 + 3 or 1 + 3 + 6 components; a family of quanta reads every holder of the content plainly and every holder of the sign of a higher rank by its sign q (0: the files declare no sign); a family gives into the one holder of the sign it reads.
- **Record**: a line of the books, never a level of its own: a family's level at a Node is one number.
- **Body**: a ledger and no state of the law: its family, its Nodes (where its family's count stands, followed each interval within one Link), its declared count and its clock (its family's level now summed over its Nodes). A crossing of the clock from at most 0 to above 0 is the body's **click**.
- **Detector**: a Node told to report. Its **report** of a quantum the count's line brought it is the one measurement; every other number (a level, a count, the books) is a GameBoard reading, a diagnostic.
- **Interval**: one step of the whole GameBoard; `ticks` intervals make a run.

## 2. The NodeState

`src/event_universe/node.py`, `NodeState`, one per family, every array over the GameBoard in 64-bit integers:

| Part | Held by | What it is |
| --- | --- | --- |
| `levels` (`now`, `before`, `remainder`) | a family of quanta | its two levels and Rule3's remainder |
| `count`, `count_remainder` | a family of quanta | its count and the count's line's remainder, laid at the first act |
| `well_remainder` | a family of quanta | the remainder of its well, (D_i + r) div T |
| `parts` | a held family | each component's two levels and remainder |
| `carry` | a held family | the hold's carry at its time part |

## 3. The interval

Before the first interval every held family's time part stands at its rest (`features/start`): the division act iterated from nothing until the levels repeat, 6 den b = num S_6(b) + 3 den sigma at a fine unit from the file's width, the sources the bodies' declared counts at the weight with which their family reads the held family; the same iteration serves the generator. `GameBoard.step()` walks the five acts in order, each one loop over the families (or the bodies and the detectors) with no case for any of them (ALGEBRA.md #the-interval):

1. **The signed read** (`node.signed_read`, `features/signed_read`): for every family of quanta the content c = SUM over its reads of (weight x by x the read family's time part) and the axis contents t_a from the tensor's parts, (weight x by x the aa part + 1) div 2; no floor and no clamp; the guard 0 < p <= P on p_0 = isqrt((Gamma - c)^2 + c^2) and on every Link's pace Gamma - 2 c - t_a, P = isqrt(2 den Gamma^2 div (den + num)), ends the run by name.
2. **Rule3 on the levels** (`node.step`): every family of quanta by `coefficients(num, den, Gamma, c, t)`, every held family's parts by the plain rule (the pace 1, the wall 3 den), forward `rule3` with the direction +1; a level beyond the amplitude bound A refuses the run by name. The well of every family of quanta is formed here, D_i = now^2 - next x before, (D_i + r) div T (`node.well`).
3. **The count's line** (`node.count_line`, `features/counts_line`): at the first act every family's count is laid from its levels, W_c c + r = 3 den (now^2 + before^2) - num now S_6(before) + W_c div 2, W_c = 3 den T (`node.lay`), the quanta a body `holds` of other families added at its Nodes, and each body's declared count is checked within 2 isqrt(c) + 1 of the count laid at its Nodes, refused by name beyond; then every interval the six currents num (now_i before_j - before_i now_j) move each family's count, no block and no clamp (a hole of -1 is conserved and filled). The bodies' Nodes follow their counts, and every detector (a detector's Nodes, the Nodes of the body it names, the open faces' layer) reports per family the rise of the family's count summed over its Nodes by the line this interval, the net inflow across its boundary (a move between its own Nodes cancels), one `gather` line per unit of rise; nothing is handed over.
4. **The hold** (`node.held_step`, `features/hold`): every held family's time part gains (w x n_i + r) div E_s at every Node by the write's carried division (`features/write`), n_i the wells of every family of quanta at the weight with which it reads the held family (whoever reads with w sources with w).
5. **The clocks and the givings** (`GameBoard.clock`, `GameBoard.give`): each body's clock; at its click the quantum leaves through an outer Port, from the shell Node where its family's count stands highest (ties in x-major order) and only where that count is at least 1: -1 of its family and +1 of the family it gives there, and the given family's two levels at that Node gain the body's family's two levels there scaled so that the form the write adds lays exactly one count over the board (`node.one_quantum`: the scale bracketed by halving and doubling, then bisected; refused by name where no scale does). A write at the whole shell of a symmetric body lays 0 or 2 counts, never 1, so the write is the read Node's.

`GameBoard.step_inverse()` runs the acts back in reverse order with Rule3's direction -1: the hold back (its increment recomputed from the wells of the levels stepped back), the count's line back, the levels back. An interval with no giving returns every level, remainder, count and carry bit for bit; the givings and the bodies' Nodes are not taken back, and the lay is not undone. The readings: `books()` per family of quanta (the count's sum, the remainders' sum, SUM (W_c c + r) against its laid value moved by the givings alone, the givings, the reports) and `contents()` per body (each family's count at its Nodes).

## 4. The loader and the files

`src/event_universe/world_files.py` (`load_world`) reads the world file, the universe and engine start files it names by their repository paths and the generator's mode file beside it, and `src/event_universe/loader/world.py` (`parse_world`) checks every key and refuses every other key as unknown by name; no default is written.

| File | Keys |
| --- | --- |
| world | `shape` [X, Y, Z]; `boundary` {`x`, `y`, `z`: `open`, `periodic` or `closed`}; `face_depth` (from 1, required with an open axis); `ticks`; `universe` and `engine` (repository paths); `measured`, a list of bodies, each `family` (a family of quanta), `nodes` [{`node` [x, y, z], `count` from 1}] (no Node shared) and optionally `holds` {family name: count}, the quanta of other families of quanta laid over its Nodes in proportion to its counts by the carried division; `detectors`, each `name` (not `face`) with `positions` (its Nodes) or `block` (the number of a body, whose Nodes report each interval) |
| universe | `integers`: `node_clock` (Gamma), `quantum_action` (T) and `width` (the integers' bits, at most the host's); `families`: each `name`, `pair` [num, den] (den from 1, |num| below den or num = den) and optionally `held` {`count`: `content` or `sign`, `divisor` from 1} |
| engine start | `mode` |
| mode (`<world>.mode.json`, `tools/pixel_mode.py`) | `world_digest` (the world's digest, `input_digest`) and `bodies`, one per body: `family`, `pair` and `moving` {`now`, `before`} (the two levels, one per Node in x-major order), with the generator's readings `profile`, `count`, `seed`, `carried`, `period`, `amplitude`, `clock` |

The amplitude bound A is derived from the file's width, never written (`derived.amplitude_bound`): the largest level at which Rule3's total 6 A R + A |S| + w (A + 1) at the levels 0, Gamma div 2 and Gamma - 1 of every pair and the count's line's total 12 num A^2 + W_c (most + 2) of every family of quanta stay inside the width. The shipped files are `examples/events/universe.json` (the universe of record), `examples/events/planck.json` (Gamma 24), `examples/events/planck_6000.json` (Gamma 6000) and `examples/events/engine_start.json`.

## 5. The output

The observer handed to `GameBoard` receives one dictionary per line: `click` (`tick`, `measured`, `family`, `node` the body's lower corner), `giving` (`tick`, `measured`, `family` the given one, `node` the Node it gave from, `count` the body's count after), `gather` (`tick`, `family`, `detector`, `count` the detector's count after, `taker` the body a detector names or None; the measurement) and `block` (`tick`, `measured`, `corner`, `sum` the clock's total; a reading). `tools/run_inputs.py` writes one `<name>.output.json` per world with the verdict (`LAWFUL`, or `REFUSED` with the reason), the intervals run, the `click`, `giving` and `gather` lines and the books.

## 6. How to run a world

1. Write a world file with its bodies declared on their Nodes, naming a universe file and `examples/events/engine_start.json`.
2. Lay its bodies: `PYTHONPATH=src python tools/pixel_mode.py --input <world>.json` rewrites the bodies' Nodes and counts and writes `<world>.mode.json` beside it.
3. Run it headless: `PYTHONPATH=src python tools/run_inputs.py --out runs/first --jobs 4 <world>.json`, one output file per world, one summary line printed per world.
4. Read the verdict first: `REFUSED` names the key, the value or the guard that refused; `LAWFUL` carries the lines and the books.

## 7. How to add a family

A family is a row of the universe file, never a line of the engine: its `name`, its `pair` and, for a held family, `held` {`count`, `divisor`}. The rule derives its parts, its reads and the family it gives; the engine steps it, counts it, holds it and reads it with the code it already has. A new act of the law starts from its line in ALGEBRA.md (CONTRIBUTING.md), is a pure function of arrays that calls Rule3 alone, and comes with its test.

## 8. The gates

`python tools/check.py` selects the changed files and their consumers and runs `ruff`, `ruff format --check`, `mypy` (strict) and `pytest` on them with the tests of `tools/every_pull_request.txt`; `--full` runs everything, and CI runs the suite in shards. `tests/test_rule3.py` holds the rule's arithmetic to `core/rule3.py` and every shift of a level across a Link to `core/ports.py`; `tests/test_integer_algebra.py` holds every module of the package to integers alone; `tests/test_the_node.py` checks the acts against Rule3 by hand, the interval on a closed cube (the count conserved, the 48 symmetries, the inverse bit for bit) and the giving on the chain.
