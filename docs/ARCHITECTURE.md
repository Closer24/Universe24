# Tensor24: the architecture

The one document that tells the system and how it is built, and the one the work runs from. The owner's words of 2026-10-30 (in Hebrew, in translation): "something not bloated that fits the Node-clock"; "one uniform document that is clear and clean and orderly, the big parts at the top, and below how each part is implemented and how it works together"; "a single document, with the decoder in it, no more splitting documents". The law ([docs/ALGEBRA.md](ALGEBRA.md)) governs it and the owner decides it.

Tensor24 is a purely algebraic engine: a board of clocks, each clock a train of gears that mesh with its six neighbours, and one act at every Node-clock every round, alike everywhere. Nothing of nature is typed; the physics is read from the clicks alone.

**Each part answers the same questions**, a few lines each, and one general flag, n/a, stands where a layer does not apply:

- **Clock:** what the clock actually does.
- **Board:** what the board does in terms of the clocks, the board taken as it stands in our event space, which has no time: time is each Node-clock's own count and nothing else.
- **Clicks:** what physics shows in the clicks, the board's shadow; the physics stands behind the clicks, and the step from the board to the clicks is the delicate one.
- **Algebra:** one line of its algebra, in whole numbers and Rule3's carry. Then its **home** in the code, its **test** and its **status**.

## 1. The parts

```
 world        loader           Node-clock        runner           record        decoder       visualizer
 3 files  ->  runner/files, -> engine/,     ->  runner/run,  ->  record/   ->  decoder/  ->  (owed)
              board, load      algebra/          rounds, rewind   schema
                                   ^                  |
                                   +----- main.py ----+    the one joint between the Node-clock and the runner
```

**The Node-clock is the most important part** (the owner's word of 2026-10-30, 11:2x UTC): every other part lays it, runs it or reads it, and it is told first below.

| Part | What it is | Home | Status |
|---|---|---|---|
| World | three files of whole numbers: the universe, the piece, the setting | examples/tensor24/ | BUILT |
| Loader | the Node-clock's initialization: lays the clocks from the three files | runner/files.py, board.py, load.py | BUILT |
| **Node-clock** | the one act at every Node-clock, every round: the core | engine/, algebra/carry.py | BUILT; terms OPEN at G2 to G5 |
| Runner | the rounds, counted from outside, and the run back | runner/run.py, rounds.py, rewind.py | BUILT |
| Record | the boundary between the board and the clicks | record/schema.py | BUILT at schema 1.2 |
| Decoder | reads the record's clicks against what nature shows (Animate's) | decoder/ | built; every row not read until G5 |
| Visualizer | draws what the decoder reads (Animate's) | owed | owed |
| Guards | the law, the gate, the tests, the documents' gates | docs/ALGEBRA.md, tools/, tests/ | BUILT |

## 2. How they work together: one round

The loader lays the board from the three files. The runner gives every Node-clock its turn in every round: each one reads itself and its six Meshes at the now slot, steps every gear once through Rule3's carry, and writes only its own state; nothing is queued or sent between Node-clocks, and the order of work is no law. Where the carry of the drive completes a whole winding a click leaves (none is written before G5). The runner writes the record and the decoder reads it. The run back is the same act on the mirrored state and returns the start bit for bit. main.py passes the Node-clock's functions to the runner, so the two never import each other.

## 3. The parts

### The Node-clock (the core)

- **Clock:** a clock of many hands, one gear per row. Every round every gear moves once: its six neighbours pull it through the Meshes and the coupling pushes it; it turns by what its teeth carry and keeps the rest as its fine tooth; the drive carries the coupling's push the same way. No gear waits, sends or is singled out, and there is no special code and no law of the Node-clock's for a slowing, a grip, a sending, a receiving, a lengthening, a shortening or a freezing: these are the act's own results (law, lines 90 and 92).
- **Board:** one pass at every Node-clock alike, reading only its own gears and its six Meshes at the now slot. The teeth W are the rest plus the metric family's 00 slots here; each Spoke's grip is the rest plus the ii slots at both ends of its Mesh. The run back is the same act on the mirrored state, exact while every fine tooth stands within its teeth.
- **Clicks:** none is written before G5. A whole click will be the drive's carry of a train's swept area; a split click will be the draw over the parts' sizes. The clicks read the rest beat as a mass, and a clock's own count as its proper time.
- **Algebra:** q, r+ = carry(W (a - b) + s (F + T_k q_d), W, r); a+ = a + q; b+ = a. F is the sum over the six Spokes of grip (neighbour - own); q_d, r_d+ = carry(J, T_d, r_d); J is the plan's contraction of up to three readings through the 24's tables, each monomial pushing all its legs.
- **Home:** engine/step.py, engine/mesh.py, engine/contract.py, engine/kinds.py, engine/state.py (the five modules of the engine), algebra/carry.py, main.py. **Test:** test_the_tensor24_engine.py (J; the act against its naive model; the run back), test_the_tensor24_algebra.py, test_the_tensor24_run.py (the whole once, on our bang). **Status:** by term, below.

**The metric family** (a train of the Node-clock, no row apart)

- **Clock:** the clock's own train: its 00 slot is every gear's teeth here, its ii slots are each Mesh's grip; it is found by its kinds' character.
- **Board:** it rides the act like every train; its push from the matter is owed (term 5).
- **Clicks:** a deeper 00 slot is a slower clock, read by its clicks as proper time; gravity reads massless.
- **Algebra:** the four-vector's symmetric square, a scalar, the vector, a scalar, E and the shears (the 00, 0i, trace, traceless diagonal and jk slots), with W = rest + the 00 slots, linear (decision 41). **Status:** the reads BUILT; its push is OPEN, owed at G2 (N2's first-order form).

**The thirteen terms** of the Node-clock's act

| # | Term | Clock | Board | Clicks | Algebra | Status |
|---|---|---|---|---|---|---|
| 1 | The readings | a gear looks at itself and at its six neighbours | its value, its difference along each axis and the pull, at the now slot | none of their own | the readings' rows: the value, three gradients, the force, then the unit | BUILT |
| 2 | The teeth W | how much a gear carries in one turn, so a deeper clock turns slower | the rest plus the 00 slots here | proper time | W = T + the sum of the 00 slots, linear | BUILT |
| 3 | The grips | how hard a Mesh holds its two gears | the rest grip plus its axis's ii slots, here and at the neighbour, alike from both ends | lengths and the speed of light, as the clicks read them | grip = den Gamma^2 + the ii slots at both ends | BUILT |
| 4 | The pull F | each neighbour tugs a gear toward its own count | the sum over the Spokes of grip (neighbour - own) | waves, and light travelling | F as above | BUILT |
| 5 | The metric's push | the matter's motion winds the clock's own train | each square slot pushed by its part of 2T + 2 eta V | gravity, read by the clocks' rates | T = sum of C[K x K -> A1] v (x) v onto the ten slots | OPEN (G2): N2's first-order form |
| 6 | The vertex and the spring | a hairspring ties a hand to a held hand in its own clock, and a vertex couples trains | J from the plan, every leg pushed | the rest beat as a mass | each monomial f x_a x_b x_c x_d pushes each leg by -f times the other three | the contraction BUILT; the strengths and the plan OPEN (G3) |
| 7 | The drive | one wheel carries the coupling's push for every row | q_d, r_d+ = carry(J, T_d, r_d) | where the clicks will come from | Rule3's carry at T_d | DERIVED (G3), in code at T_d = 1 |
| 8 | The kick | the drive's whole turns pushed into the gear | K = T_k s q_d | none of its own | as written | BUILT at T_k = 1 |
| 9 | The volume's notch | the board's mean count swings and returns | the metric family's own swing and its top | the universe's swing (Postulate 4), with gravity's polarizations massless | owed in the slot form | OPEN (G2) |
| 10 | The shift and the shears | the now leans toward a neighbour, and stretches by direction | the 0i and jk slots, read by the gradient's and the pull's contractions | frame dragging and waves | owed after G2 | OPEN (G4) |
| 11 | The whole click | when a train's swept area completes a whole key, the drive carries it once | the area summed over the train's rows through the A1 table, carried at the key, the rest kept in r_d | one quantum per mode, E = n h nu; a negative wind is a negative quotient, with no if | q, r_d+ = carry(the area moved, key, r_d) | DERIVED (G5), owed in code |
| 12 | The split click | when parts share a winding, the great clock draws which part takes it | a rank count over the parts' sizes after the carry; a full slot refuses after the draw, and the quantum returns to its giver | Born's rule; both clicks can fall in one round, on different trains | the draw | OPEN (G5): its fairness and the draw's c |
| 13 | The frozen clock | a clock whose teeth outgrow its drive never fires | where that holds is the horizon, with no hold and no restore | a horizon | derived on the slot form | OPEN (G2), on the act |

**The mass** (term 6; David's, with G3's results)

- **Clock:** a hairspring ties a hand to a held hand in its own clock, so it swings by itself.
- **Board:** a tied hand beats at its rest rate at every clock alike; light's hands have no hairspring and only travel from clock to clock.
- **Clicks:** the beat is read as a mass, through energy differences and through motion; light reads massless.
- **Algebra:** the spring g C n, 4 sin^2 (omega0 / 2) = g n / W. **Home:** engine/contract.py, term 6. **Status:** built; the strengths OPEN at G3.
- **G3's results** (David's DAVID-TENSOR24-G3.md, toys-5 1ae9a6c29): the bound holds for one tied family or one summed four-leg term, and with a term on each family the sum of g_f^2 / (2 kappa lam_f) is at most 1; the ceiling is the smaller of lam's excess scale and the held hand's own (x near kappa / g), never the held hand's sign; light and the metric stay off k (OPEN, no row apart); E is read through its form; an E held count's own potential of up to four legs stands where two of a T1 family's springs meet.

**The families and the three hands:** owed from David in the same form (his (e): the decoder's page 1.8 and 3.9 to 3.11).

### The world: the three files

- **Clock:** before the first round, the files say which trains every Node-clock carries (each a name, its kinds among the 24's five, its part and its pinion), how many Node-clocks stand on each axis, and which gears are set where.
- **Board:** at round 0 every gear stands at 0 except the ones the setting lays. Nothing else is laid: no coupling, strength, particle or mass (decision 35).
- **Clicks:** none come from the files; everything the clicks show comes out of the act (a mass is measured only there, decision 37).
- **Algebra:** whole numbers only; every side, part and integer is at least 1; no fourth file is a world.
- **Home:** examples/tensor24/ (universe.json, piece.json, setting.json), the one bang. **Test:** test_the_tensor24_files.py. **Status:** BUILT.

### The loader, the Node-clock's initialization

- **Clock:** it makes every Node-clock alike from its star of six Spokes: the 24 turns that leave the star the same, the five kinds by which a train's gears turn with them, and the tables that gear one kind into another. Then it sets every gear's teeth and every Mesh's grip, and lays the setting's gears.
- **Board:** each Node-clock's six neighbours, by the wrap on each axis. Every row's teeth rest at 6 den Gamma^2 (6 is the Spokes), and every Mesh's grip at den Gamma^2. The metric family is found by its kinds' character alone: its 00 slot is every row's teeth, its ii slots are each axis's grips. s, T_k and T_d stay at 1 until G3.
- **Clicks:** the record's header names each train's kinds and part, so a click names a train, never a row. No number of the loader reaches the clicks except through the act.
- **Algebra:** the 24 are the matrices of three Spokes that Rule3's weight keeps (24 of 216). A channel's group sum is c u u^T, and its table u is the primitive row, read where the diagonal entry divides every other, with the sign by Rule3's sign test; all 125 channels go in one einsum, with no loop, seed or search.
- **Home:** runner/files.py (reads the files and refuses by name), runner/board.py, runner/load.py, main.py (made); tools/tensor24_files.py (checks and loads the files). **Test:** test_the_tensor24_files.py, test_the_tensor24_load.py, test_the_tensor24_kinds.py. **Status:** BUILT; the strengths OPEN (G3).

### The runner

- **Clock:** it counts the rounds from outside, since no Node-clock holds a count. It gives every Node-clock its turn in every round, then runs all the rounds back to see the start return.
- **Board:** before each round it reads the promise, every fine tooth within its teeth (so the teeth are at least 1), and names where it breaks. After the rounds it rewinds by the act's run back alone. The end's digest is the state reached.
- **Clicks:** it writes what the act gives: the record's header and end, and the ledger beside them; click lines from G5.
- **Algebra:** the act iterated; the start returns bit for bit. **Home:** runner/run.py, runner/rounds.py, runner/rewind.py; tools/tensor24_run.py. **Test:** test_the_tensor24_run.py. **Status:** BUILT.

### The record

- **Clock:** the boundary between the board and the clicks; only the readers read it.
- **Board:** nothing of the board crosses it except what its lines name. The header: the files with their digests, the board's sides, and each train's kinds, part and winding. The end: the rounds, the digest, and whether the run back was exact. The ledger beside it: one count line per round, Node-clock and train (1,280 on the example).
- **Clicks:** its click lines, from G5, name a train, a Node-clock and a tick; nothing is computed in it.
- **Algebra:** whole numbers of any width, and labels. **Home:** record/schema.py. **Test:** test_the_tensor24_run.py and the decoder's tests. **Status:** BUILT at schema 1.2; schema 1.3, the Boss's next push, puts each kind's characters and each train's square flag in the header, retires the couplings and drops the classes and the draw.

### The decoder (Animate's)

- **Clock:** the watchmaker outside the case. It reads only what clocks count and how light links one clock's count to another's: a reading is a clock's own count between two of its clicks, never a round read as a duration and never a label's difference read as a length. Clock parts first: a click takes a whole train and never one of its gears, so a gear is read only through its clock's clicks, and only a clock is placed in spacetime.
- **Board:** the board reaches it only through the record and the ledger beside it, read from outside; it never steps the engine, never reads its arrays and never writes into a run. The step from the board to the clicks is the delicate one: the board is no fixed space (a Node-clock keeps its label while the Mesh between two labels lengthens and shortens), its round, teeth and grips are no observables, they reach the clicks only as ratios at first order and as departures of order omega0^2 beyond, and the board holds no unit for the round.
- **Clicks:** nature is read in the clicks, the board's shadow. Every reading says shown, not shown or not read, each with its cause, and raises nothing.
- **Algebra:** read a line and refuse a bad one by name; group, order by round, follow a link (a take to its lay, a clock to its clicks); count, add, subtract and multiply whole counts; compare fractions by cross products; Rule3's quotient with its remainder. Never a root, a float, a logarithm, a circular function, a physics formula or a number beyond 0 and 1 in the code; a spread for finite draws is an integer of the files.
- **Home:** decoder/ (it imports the record and the algebra alone) and tools/tensor24_decode.py. **Test:** test_the_tensor24_decoder.py, test_the_tensor24_decoder_bangs.py, test_the_tensor24_decoder_cases.py, test_the_tensor24_decoder_measure.py (Animate's five: the record, the ledger, the clock family, row 46's load, and the whole once on the example). **Status:** built on records made in memory; on the example's record every row not read until G5.

**What it reads.** The record's header (the files, the sides and the order of the sites, the kinds, the trains with their kinds, parts and windings; from schema 1.3 each kind's characters and each train's square flag), its click lines from G5 (a whole click: its train, Node-clock and round, its quotient, its takes with their lays; a split click: its parts' sizes, the frames it drew among and the one drawn), and its end (the rounds, the digest, the rounds run back, exact or not); the ledger's count lines, one per round, Node-clock and train, the train's counts there row by row. The clock family is the train flagged as the four-vector's square; its first row is the 00 slot, each Node-clock's own teeth.

**The readings** (what the clicks read; status):

1. **Row 15, the books:** at a whole click each train's taken equals its laid, at its own winding: conservation, both ways of time; built in memory, on the engine at G5.
2. **Row 46, each later bang shows more:** the load, the clock family's 00 slot summed over the board, falls to a bottom between bangs; each later bang's click kinds and deepest clock grow (ever more complex clocks); the load first, on the count lines, the rest at G5.
3. **D6, proper time:** a clock's own count between two of its clicks; built in memory, on the engine at G5, and from G2 where a clock moves.
4. **D7:** a difference of rounds read as a duration is refused by name; built.
5. **D8, the cone:** each click binned by the settings outside its past cone, so no signal; built on the board's cone, one Mesh a round; light's cone owed.
6. **The twins, the free path:** two clocks meet twice by two paths, and the free one counts more against nearby paths; equal counts on image paths are no fault; to mend.
7. **Light:** a light path is a lay and its take; a distance an echo in one clock's own count, two-way only; the redshift a one-way count ratio; time dilation read from both directions or over a closed path; proper time a second time by signals; a tide between free clocks; echoes growing or swinging; a horizon; owed (light.py).
8. **Mass:** the rest beat per species in its own ticks (decision 37), the width against the mean life, and where a species stands among a clock's parts: a gear never taken alone, a bound part freed by a click, a free quantum taken alone; owed (mass.py, G6).
9. **A probability:** the shares of split clicks over many lays alike, against the sizes, with their spread; at G5.
10. **A correlation at a distance:** the joint outcomes of one birth's two clicks by the two settings' frames, on two boards; at G5.

**What it needs from the engine** (the Boss's): the click lines (G5), with each take's lay, each clock's click with its clock and teeth, and each setting's frames and the one drawn; each train's windings and wind in the ledger with G5's click; composites that click (G6); a click's region where a reading uses one site (G6); a universe that lays a travelling wave (G2). **The build, in order:** family.py from schema 1.3's header (exactly one train flagged, else not read with the count); row 46's load on the count lines; clocks.py out (the rate lines no run writes); the five tests; the twins and the site refusal mended; light.py; mass.py; G5's clicks; G6's composites. **Open:** the spread for finite draws (the Boss's rule); light's cone read from the record; a click's region (G6); the draw's dial c (G5).

**Uncertainty**

- **Clock:** one tick holds every beat, and only many ticks tell a beat; one Node-clock holds every motion, and a sharp motion fills the whole board.
- **Board:** the Node-clocks a wave holds times the motions it holds are never fewer than the board's Node-clocks, a count with no law of its own (whole numbers, every ring of 2 to 10 and two boards: ANIMATE-UNCERTAINTY).
- **Clicks:** a click at one round holds every beat, so a mass is read only through many clicks of one clock; the draw puts a click's place in the detector's region, and within it the motion is open.
- **Algebra:** a wave's support times its transform's support is at least the board's size, by exact rank. **Status:** CHECKED.

### The algebra (algebra/carry.py)

- **Clock:** a dial turns, and what it cannot hold stays at the Node-clock as its remainder.
- **Board:** n + r = q d + r' at every gear, every round: the quotient leaves as the event, the remainder stays as the memory that makes the run back exact.
- **Clicks:** the quotient is the click; nothing else is measured.
- **Algebra:** n + r = q d + r' with 0 <= r' < d: the one place a division is written; the operations are three, on whole numbers: addition, multiplication and the carry; no float, no root, no exponential (lines 100 and 102). **Home:** algebra/carry.py. **Test:** test_the_tensor24_algebra.py. **Status:** BUILT.

### The visualizer (Animate's)

- **Clock:** the board's clocks drawn as they turn.
- **Board:** the Node-clocks, the Meshes and the rounds as the record has them.
- **Clicks:** the clicks drawn where they land, with the decoder's verdicts beside them.
- **Algebra:** n/a: it computes nothing. **Status:** owed; it waits for the click lines (G5).

### The guards, beside the run

- **Clock:** the law's clause "The system is a system of clocks, and it is always checked" (line 106): the guards read every push and every line.
- **Board:** the tests run on a board: each generic part has one small test and one test that nothing above it broke, the whole run once on our bang (line 106); tools/check.py runs the gates and the tests together.
- **Clicks:** the decoder's rows are the validation: what the clicks read is set against what nature shows.
- **Algebra:** the gate (tools/derivations/open_items/scribe_scan.py) is the algebra's law in a script: it refuses a push that raises a count of a number beyond 0 and 1, a float, a root, a loop, a branch, a comparison, a clamp, a mask, an enumeration, a probe with a float, or a module whose docstring lacks these four layers, and it keeps the table below.
- **Home:** docs/ALGEBRA.md, tools/, tests/. **Status:** BUILT.

## 4. Who may import whom

The architect's table; the gate's ISOLATE rule reads it. The standard library is allowed everywhere, numpy in the engine and the runner alone.

| Folder | May import |
|---|---|
| algebra | algebra |
| record | record |
| engine | algebra, engine, record |
| readings | algebra, readings, record |
| runner | algebra, readings, record, runner |
| decoder | algebra, decoder, readings, record |
| main.py | engine, runner |

## 5. What is open

**G2:** the first-order form of term 5 (N2, in David's reading) and the notch and the frozen clock (terms 9 and 13), and the exponential clock beside the slot form (Postulate 6), both kept written until the test. **G3:** the strengths per channel and the plan, the tables' unit, which families tie to k, the held count's own potential, n's unit. **G4:** the shift and the shears (term 10). **G5:** the clicks, the split's draw and its c, the visualizer. Beside them: the counts hidden in label tuples (len(GEAR), len(ADDED), WAYS, ENDS), to be read from the star, the piece and the schema with schema 1.3; the spring of line 35, which waits on the owner's rule for the head's notch.

## 6. The documents

One document tells the system: this one. Beside it stand the law ([docs/ALGEBRA.md](ALGEBRA.md)); the entry files ([README.md](../README.md), `llms.txt`); the project files (`LICENSE`, `CITATION.cff`, `pyproject.toml`, [CONTRIBUTING.md](../CONTRIBUTING.md), [CHANGELOG.md](../CHANGELOG.md)); and the work's records under tools/derivations (the Boss's derivation pages, David's derivations, the keeper's `SCRIBE-GATE-1.md`, `SCRIBE-LAW-AUDIT-2.md` and `SCRIBE-ROUTINE.md`), which no part depends on. The other documents of docs/ are records of the work, folded into this one: [ENGINE](ENGINE.md), [BIG_PICTURE](BIG_PICTURE.md), [CLOCK_WORDS](CLOCK_WORDS.md), [FURTHER_RESEARCH](FURTHER_RESEARCH.md), [FOLLOW_UP_PAPERS](FOLLOW_UP_PAPERS.md), [HIGHLIGHTS](HIGHLIGHTS.md) and [UNIVERSE24](UNIVERSE24.md). The old engine and its worlds stand in git's history alone.

**Who keeps what.** The Boss keeps the status lines of the world, the loader, the Node-clock, the runner and the record true at each push; Animate those of the decoder and the visualizer; David derives, each derivation telling its part in these questions and going to the writer as a section of this document; the writer keeps the form and the law and reads every push against both; the owner decides, and no part changes its place or its wall without his word.

## 7. The glossary

- **Node-clock:** a site of the board: a train of gears, one act per round. **Gear:** a dial with its count now and before and its fine teeth. **Mesh, Spoke:** the link between two neighbouring Node-clocks, one through each of a Node-clock's six Spokes.
- **Round:** one full pass of every Node-clock, counted by the runner. **Carry:** Rule3's division, a quotient that leaves and a remainder that stays. **Click:** the carry's quotient where a winding is whole: the one measurement.
- **The 24, the kinds:** the cube's turns and the five kinds that tie a train's gears. **Board:** the event board. **Bang:** the one run from the seed.
