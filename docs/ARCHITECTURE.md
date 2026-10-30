# Tensor24: the architecture

The one document that tells the system and how it is built, and the one the work runs from (the owner's words of 2026-10-30, in Hebrew, in translation: "a single document, with the decoder in it, no more splitting documents"; "not bloated"; "clear and clean and orderly"). The law ([docs/ALGEBRA.md](ALGEBRA.md)) governs it and the owner decides it. The words it uses are in the glossary at the end.

Tensor24 is a purely algebraic engine: a board of Node-clocks, each a set of gears that mesh with its six neighbours' gears through six Meshes, and one act at every Node-clock, alike everywhere, which the runner repeats in rounds. Rule3's carry is its one division, with the remainder kept. Nothing of nature is typed; the physics is read from the clicks alone.

**Each part answers the same questions**, a few lines each, and one general flag, n/a, stands where a layer does not apply:

- **Clock:** what the clock actually does.
- **Board:** what the board does in terms of the clocks, the board taken as it stands in our event space, which has no time: time is each Node-clock's own count and nothing else (a round is the runner's pass and a gear's now and before are its two counts; none of them is a time of the board's).
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

The loader lays the board from the three files. The runner gives every Node-clock its turn in every round: each one reads itself and its six Meshes at the now slot, steps every gear once through Rule3's carry, and writes only its own state; nothing is queued or sent between Node-clocks, and the order of work is no law. Where a train's own click tooth carries its swept area to a whole key, a click leaves (none is written before G5). The runner writes the record and the decoder reads it. The run back is the same act on the mirrored state and returns the start bit for bit. main.py passes the Node-clock's functions to the runner, so the two never import each other.

## 3. The parts

### The Node-clock (the core)

The engine is five modules (engine/): step.py, mesh.py, contract.py, kinds.py and state.py.

- **Clock:** a clock of many hands, one gear per row. Every round every gear moves once: its six neighbours pull it through the Meshes and the coupling pushes it; it turns by what its teeth carry and keeps the rest as its fine tooth; the drive carries the coupling's push the same way. No gear waits, sends or is singled out. A Node-clock is independent: it reads itself and its six Meshes and nothing else (decision 42, line 92), and there is no special code and no law of its own for a slowing, a grip, a sending, a receiving, a lengthening, a shortening or a freezing: these are what the act gives on the metric's own gears (law, line 90), once the metric's push is built (G2).
- **Board:** one pass at every Node-clock alike, reading only its own gears and its six Meshes at the now slot. The teeth W are the rest plus the metric family's 00 slots here; each Spoke's grip is the rest plus the ii slots at both ends of its Mesh. The run back is the same act on the mirrored state, exact while every fine tooth stands within its teeth.
- **Clicks:** none is written before G5. A whole click will be the carry of a train's swept area by its own tooth; a split click will be the draw over the parts' sizes. The clicks read the rest beat as a mass, and a clock's own count as its proper time.
- **Algebra:** q, r+ = carry(W (a - b) + s (F + T_k q_d), W, r); a+ = a + q; b+ = a. F is the sum over the six Spokes of grip (neighbour - own); q_d, r_d+ = carry(J, T_d, r_d); J is the plan's contraction of up to three readings through the 24's tables, each monomial pushing all its legs.
- **Home:** engine/step.py, engine/mesh.py, engine/contract.py, engine/kinds.py, engine/state.py (the five modules of the engine), algebra/carry.py, main.py. **Test:** test_the_tensor24_engine.py (J; the act against its naive model, local, pure and turned by the 24; the run back; each law with the mutants that break it), frame.py (the property tests any engine of the Node-clock must pass, shared by the tests: locality, purity, rename, the 24's images, the run back), test_the_tensor24_algebra.py, test_the_tensor24_run.py (the whole once, on our bang). **Status:** by term, below.

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
| 7 | The drive | one wheel carries the coupling's push for every row | q_d, r_d+ = carry(J, T_d, r_d) | none of its own: the clicks do not come from the drive | Rule3's carry at T_d | DERIVED (G3), in code at T_d = 1 |
| 8 | The kick | the drive's whole turns pushed into the gear | K = T_k s q_d | none of its own | as written | BUILT at T_k = 1 |
| 9 | The volume's notch | the board's mean count swings and returns | the metric family's own swing and its top | the universe's swing (Postulate 4), with gravity's polarizations massless | owed in the slot form | OPEN (G2) |
| 10 | The shift and the shears | the now leans toward a neighbour, and stretches by direction | the 0i and jk slots, read by the gradient's and the pull's contractions | frame dragging and waves | owed after G2 | OPEN (G4) |
| 11 | The whole click | when a train's swept area completes a whole key, the train's own click tooth carries it once | the area summed over the train's rows through the A1 table, carried at the key by the train's own tooth k at each Node-clock, born at half the key; the click pushes nothing into a, b, r or r_d | one quantum per mode, E = n h nu; a negative wind is a negative quotient, with no if | q_c, k+ = carry(tau, key, k) | OPEN (G5): the Boss's derivation (derive/boss/term11) is with David's two readers: the area read at the now slot; the click tooth flipped in its key by the mirror, the run back exact with no log read; the birth (key - 1) div 2, the flip's fixed point, so that a give and a take are opposite clicks for an odd key; the key's value OPEN (G3) |
| 12 | The split click | when parts share a winding, the draw, a Node-clock's own from its fine teeth and its six neighbours' (decision 29), says which part takes it | a rank count over the parts' sizes after the carry; a full slot refuses after the draw, and the quantum returns to its giver | Born's rule; both clicks can fall in one round, on different trains | the draw | OPEN (G5): its fairness and the draw's c |
| 13 | The frozen clock | a clock whose teeth outgrow its drive never fires | where that holds is the horizon, with no hold and no restore | a horizon | derived on the slot form | OPEN (G2), on the act |

**The mass** (term 6; David's, with G3's results)

- **Clock:** a hairspring ties a hand to a held hand in its own clock, so it swings by itself.
- **Board:** a tied hand beats at its rest rate at every clock alike; light's hands have no hairspring and only travel from clock to clock.
- **Clicks:** the beat is read as a mass, through energy differences and through motion; light reads massless.
- **Algebra:** the spring g C n, 4 sin^2 (omega0 / 2) = g n / W. **Home:** engine/contract.py, term 6. **Status:** the vertex law BUILT and tested generically; the spring's beat and bound were checked at the tests' strengths and left the suite (git 2c87a07ed); no spring is laid in any world file yet; the strengths OPEN at G3.
- **G3's line, not yet agreed** (David's fourth text, toys-5 1ae9a6c29; his hostile mathematician's reading came back not agreed, eleven items; his fifth text replaces this line): the bound holds for the quadratic held spring with positive strengths; the step's limit is read through V's Hessian in (x, k); the held hand meets the gear's doubled beat at kappa = 4 g n, a resonance and no edge; the counts laid at swings of 2 x 10^7 and above are one sample of a wide spread and are reported as spreads; a five-leg term and the held count's cross terms also fix E's direction; the sum of g_f^2 / (2 kappa lam_f) at most 1 for a term on each family needs its signs and its proof step.

**The families and the three hands (the three generations)** (drawn by Animate from the decoder's page 1.6, 1.8 and 3.9 to 3.11, git 8c4f3ff59; David confirmed it with one mend, 6522837453)

- **Clock:** a family of kind T1 is a clock with three hands, one per axis. The cube's 24 turns swap them as they swap the axes, and the act drives all three alike: the same teeth, the same grip, the same wave. A held count beside them is a hairspring. Of kind A1 it ties all three alike, so one beat; of kind A2 it ties none, and only couples a T1 family to a T2 one. Three beats need a held count that points along the cube: E off its three lines, or T2 off the body diagonals, with an A1 part large enough that no hand runs away.
- **Board:** at every Node-clock the three rows step alike; with a held E or T2 count each row beats at its own rate. That count must not show the cube's axes to light: the kinds that split a triplet are the metric's own (E, T2), so a vertex pairing them with the metric's slots makes light's speed depend on direction, which cavities bound at parts in 10^18. An E count's own potential sits on its lines, where two beats meet, wherever its term in f to the first power is not 0 (a three-leg or five-leg term, or a cross term with the count's A1 part); only f^2, at six legs, moves it off.
- **Clicks:** a click takes the whole train and never a row, so unsplit the three hands are one species' gears: the law's confinement (line 1556), the colours as the three axes. Split, they are a candidate for three species alike but for mass, told apart only by a take resonant with one beat; then the rows are the generations and the colours stand elsewhere, since rows cannot be both. In nature the electron, the muon and the tau are one clock design at three beats: one charge and one spin, told apart by the beat (the mass), the life (the width) and the neutrino each pairs with, each heavier one decaying into lighter ones, all three taken alone. The quarks' generations are gears, read only through their hadrons, and the top through its own decay.
- **Algebra:** the 24's kinds have 1, 1, 2, 3 and 3 rows, and T1 x T1 -> A1 is the dot product. Three beats need held counts that cut the 24 to a group under which T1 has only one-dimensional pieces (D2 or the Klein group fix the basis; a half turn or nothing lets the counts set it). A1 + E (n0; e1, e2) gives n0 + e1, n0 - e1 + e2 and n0 - e2; T2 gives lambda^3 - |t|^2 lambda - 2 t1 t2 t3. Any three beats fit a + B cos (phi + 2 pi k / 3), so that form predicts nothing alone. Koide's 2/3 is a test, Animate's own, that David's readers have not read: never met on the diagonal A1 + E spring with whole counts (the Eisenstein norm's power of 2), met often with a T2 part. At most three alike, the board's axes, under four assumptions: a natural three, not a derived one.
- **Home:** none of its own: term 6's spring, and G5's take. **Status:** A1 or A2 held counts give one mass (DERIVED, CHECKED), which nature refuses as the generations' law. OPEN at G3: which held counts the one plan lays, against the metric's slots. OPEN at G5: the resonant take. OPEN: what keeps each row's count apart through a click (mu -> e gamma below 1.5 x 10^-13), what tells the electron's, the quarks' and the neutrinos' families apart, mixing, CP, and the neutrinos' masses.

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
- **Clicks:** its click lines, from G5, name a train, a Node-clock and a round, which orders the clicks and is never a duration; nothing is computed in it.
- **Algebra:** whole numbers of any width, and labels. **Home:** record/schema.py. **Test:** test_the_tensor24_run.py and the decoder's tests. **Status:** BUILT at schema 1.2; schema 1.3, the first task of the Boss's code writer, puts each kind's characters and each train's square flag in the header, retires the couplings and drops the classes and the draw.

### The decoder (Animate's)

- **Clock:** the watchmaker outside the case. It reads only what clocks count and how light links one clock's count to another's: a reading is a clock's own count between two of its clicks, never a round read as a duration and never a label's difference read as a length. Clock parts first: a click takes a whole train and never one of its gears, so a gear is read only through its clock's clicks, and only a clock is placed in spacetime.
- **Board:** the board reaches it only through the record and the ledger beside it, read from outside; it never steps the engine, never reads its arrays and never writes into a run. The step from the board to the clicks is the delicate one: the board is no fixed space (a Node-clock keeps its label while the Mesh between two labels lengthens and shortens), its round, teeth and grips are no observables, they reach the clicks only as ratios at first order and as departures of order omega0^2 beyond, and the board holds no unit for the round.
- **Clicks:** nature is read in the clicks, the board's shadow: proper time, no signal outside the cone, conservation at every click, ever more complex clocks bang by bang, masses as rest beats, Born's shares and Bell's correlations, each a count of clicks (the readings below). Every reading says shown, not shown or not read, each with its cause, and raises nothing.
- **Algebra:** read a line and refuse a bad one by name; group, order by round, follow a link (a take to its lay, a clock to its clicks); count, add, subtract and multiply whole counts; compare fractions by cross products; Rule3's quotient with its remainder. Never a root, a float, a logarithm, a circular function, a physics formula or a number beyond 0 and 1 in the code; a spread for finite draws is an integer of the files.
- **Home:** decoder/ (it imports the record and the algebra alone) and tools/tensor24_decode.py. **Test:** test_the_tensor24_decoder.py, test_the_tensor24_decoder_bangs.py, test_the_tensor24_decoder_cases.py, test_the_tensor24_decoder_measure.py (13 tests on records made in memory; after the cut from the Boss's head, five: the record, the ledger, the clock family, row 46's load, and the whole once on the example; the click readings' tests come back with G5). **Status:** built on records made in memory; on the example's record every row not read until G5.

**What it reads.** The record's header (the files, the sides and the order of the sites, the kinds, the trains with their kinds, parts and windings; from schema 1.3 each kind's characters and each train's square flag), its click lines from G5 (a whole click: its train, Node-clock and round, its quotient, its takes with their lays; a split click: its parts' sizes, the frames it drew among and the one drawn), and its end (the rounds, the digest, the rounds run back, exact or not); the ledger's count lines, one per round, Node-clock and train, the train's counts there row by row. The clock family is the train flagged as the four-vector's square; its first row is the 00 slot, each Node-clock's own teeth.

**The readings**, each in the three answers:

| # | Reading | Clock | Board | Clicks | Status |
|---|---|---|---|---|---|
| 1 | Row 15, the books | a click moves whole turns from a giver's dial to a taker's, and each remainder stays at its dial | the trains' counts before and after the click, at its Node-clocks | conservation: what one clock gives another takes, both ways of time | built in memory; at G5 |
| 2 | Row 46, each later bang shows more | the clocks' rate gears wind up and run down together, and each turn of the whole builds clocks of more parts | the clock family's 00 slot summed over the board, round by round; its bottoms part the bangs | ever more complex clocks, bang by bang: more kinds of click, deeper clocks laid | the load first, on the count lines; the rest at G5 |
| 3 | D6, proper time | a clock counts its own ticks between two of its clicks, and no Node-clock's rate line is read | the count it summed along its path | proper time, a clock's own age | built in memory; at G5, and from G2 where a clock moves |
| 4 | D7, no duration from rounds | the runner's pass is no tick of any clock | a round is an index from outside | a difference of rounds is refused by name | built |
| 5 | D8, the cone | a click's past is what could reach it, one Mesh a round | the board's cone round each click | no signal: no click's share shows a setting outside its cone | built on the board's cone; light's cone owed |
| 6 | The twins, the free path | two clocks part and meet again | the two paths between the meetings, each with its winding round the board | the free path counts more against nearby paths; equal counts on image paths are no fault | to mend |
| 7 | Light | one clock lays a quantum, another takes it | the lay's and the take's Node-clocks and rounds | distance by echo, the redshift, time dilation, a tide, a horizon | owed (light.py) |
| 8 | Mass | a clock's own beat, counted in its own ticks | the rest beat of a held hand | a species' mass and width, and where it stands among a clock's parts | owed (mass.py, G6) |
| 9 | A probability | many lays alike, each drawn by the sizes | the parts' sizes at each split click | Born's rule: the shares against the sizes, with their spread | at G5 |
| 10 | A correlation at a distance | one birth's two clicks at two clocks far apart, each drawn by its setting | the two settings' frames, on two boards | Bell: the joint outcomes against the two frames | at G5 |

**What it needs from the engine** (the Boss's): the click lines (G5), with each take's lay, each clock's click with its clock and teeth, and each setting's frames and the one drawn; each train's windings and wind in the ledger with G5's click; composites that click (G6); a click's region where a reading uses one site (G6); a universe that lays a travelling wave (G2). **The build, in order:** family.py from schema 1.3's header (exactly one train flagged, else not read with the count); row 46's load on the count lines; the five tests; the twins and the site refusal mended; light.py; mass.py; G5's clicks; G6's composites. **Open:** the spread for finite draws (the Boss's rule); light's cone read from the record; a click's region (G6); the draw's dial c (G5).

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
- **Board:** the Node-clocks, the Meshes and the rounds as the record has them; its board side can draw the count lines now.
- **Clicks:** the clicks drawn where they land, with the decoder's verdicts beside them.
- **Algebra:** n/a: it computes nothing. **Status:** owed; it waits for the click lines (G5).

### The guards, beside the run

- **Clock:** the law's clause "The system is a system of clocks, and it is always checked" (line 106): the guards read every push and every line.
- **Board:** the tests run on a board: each generic part has one small test and the whole runs once on our bang (line 106), the standard of the world and no more: no test is defined for nothing, no matrix of cases, no table of mutants (the owner's word of 12:4x UTC); tools/check.py runs the gates and the tests together.
- **Clicks:** the decoder's rows are the validation: what the clicks read is set against what nature shows.
- **Algebra:** the gate (tools/derivations/open_items/scribe_scan.py) is the algebra's law in a script: it refuses a push that raises a count of a number beyond 0 and 1, a float, a root, a loop, a branch, a comparison, a clamp, a mask, an enumeration, a probe with a float, or a module whose docstring lacks these four layers, and it keeps the table below.
- **Home:** docs/ALGEBRA.md; tools/check.py (runs the gates and the tests together, in CI on every pull request and on every push to main), tools/merge_base.py, tools/record_code_shape.py, tools/tests_shape.py, tools/documents_gates.py, tools/derivations/open_items/scribe_scan.py (the gate; its self-test beside it, scribe_scan_selftest.py, runs with it), tools/derivations/open_items/scribe_law_check.py (the law's own check and this document's mirror of the tree, `--arch`). **Status:** BUILT; the law check, the mirror and their self-test join tools/check.py's ratchets (the Boss's yes, 12:4x UTC); the tests are cut to that shape: the engine's by the Boss's code writer, the decoder's to five by Animate (the owner's word of 12:4x UTC).

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

**When the system is closed.** The owner's word of 2026-10-30, 12:4x UTC: once the Node-clock works well, that is it, the system is closed: its thirteen terms derived with both readers agreeing and the one whole run on our bang; every other part is simple, with one small test of itself and no more.

**G2:** the first-order form of term 5 (N2, in David's reading) and the notch and the frozen clock (terms 9 and 13), and the exponential clock beside the slot form (Postulate 6), both kept written until the test. **G3:** the strengths per channel and the plan, the tables' unit, which families tie to k, the held count's own potential, n's unit. **G4:** the shift and the shears (term 10). **G5:** the clicks (term 11 first, the Boss's derivation), the split's draw and its c (David's draft strikes the c), the visualizer. Beside them: the counts hidden in label tuples (len(GEAR), len(ADDED), WAYS, ENDS), to be read from the star, the piece and the schema with schema 1.3; the spring of line 35, which waits on the owner's rule for the head's notch.

## 6. The documents

Two documents tell the system: this one and the law ([docs/ALGEBRA.md](ALGEBRA.md)). [README.md](../README.md) is the front door (`llms.txt` its machine copy), [CONTRIBUTING.md](../CONTRIBUTING.md) the way in, [CHANGELOG.md](../CHANGELOG.md) what changed, and `LICENSE`, `CITATION.cff` and `pyproject.toml` the project's files. papers/ holds the two publications, their text and PDF (their scripts stand in git). The records of the work stand under tools/derivations (the derivations, the gate's `SCRIBE-GATE-1.md`, the keeper's `SCRIBE-LAW-AUDIT-2.md`, `SCRIBE-OWNER-WORDS.md` and `SCRIBE-ROUTINE.md`), and no part depends on them. The earlier documents (ENGINE, BIG_PICTURE, CLOCK_WORDS, FURTHER_RESEARCH, FOLLOW_UP_PAPERS, HIGHLIGHTS and UNIVERSE24) left the tree on 2026-10-30, the owner's word: one clean main, the architecture file and the algebra file; what of them is live stands here or in the law, and the rest in git at scribe-5 3b7fd1bd2. The decisions in force are the law's (line 35). The old engine and its worlds stand in git's history alone.

**Who keeps what.** The Boss keeps the status lines of the world, the loader, the Node-clock, the runner and the record true at each push; the code of the engine, the loader, the runner, the record and of his tools and tests is written by one code-writer subagent of his alone (the owner's word of 2026-10-30, 12:3x UTC: the Boss is free to manage everything, only the subagent writes code), briefed from this document, its work read by a hostile reader and reviewed and pushed by the Boss; Animate keeps those of the decoder and the visualizer, the decoder being hers; David derives, each derivation telling its part in these questions and going into its row or section of this document the moment both its readers agree (the owner's word of 12:3x UTC: "The moment the drafts are ready, they put them in."), the writer folding it in the document's form; the writer keeps the form and the law and reads every push against both; the owner decides, and no part changes its place or its wall without his word.

## 7. The glossary

- **Node-clock:** a site of the board: a set of gears, one for each row of each train, and one act per turn. **Gear:** a dial with its count now and before (the state's two slots) and its fine tooth, a remainder. **Train:** a tensor of gears across the board, the dials of one kind of thing (light, matter, the metric family).
- **Spoke, Mesh:** a Spoke is one of a Node-clock's six directions; a Mesh is the link through a Spoke between two neighbouring Node-clocks, read once from both ends.
- **Rule3, carry:** Rule3 is the one division, n + r = q d + r' with 0 <= r' < d: a quotient that leaves and a remainder that stays; the carry is the only place a division is written. **Winding:** the whole turn of a hand, the divisor at which a carry completes.
- **Click:** the carry's quotient where a winding is whole: the one measurement, whole or split. **Round:** one pass of the runner over every Node-clock, an index from outside and no time of the board's. **Now, before:** a gear's two counts, no clock time.
- **Mirrored state:** time's reversal at fixed teeth: now and before swapped and each fine tooth r flipped to W - 1 - r in its teeth W; the run back is the tick on the mirrored state, mirrored.
- **Metric family, 00 slot, ii slots:** the clock's own train: its 00 slot is every gear's teeth here (the clock's rate), its three ii slots are each axis's Mesh grip.
- **The 24, the kinds:** the cube's turns that leave a Node-clock's star the same, and the five kinds that tie a train's gears. **Board:** the event board, taken in our event space, which has no time. **Bang:** the one run from the seed.
- **G2 to G5:** the stages that close what the Node-clock lacks (the Boss's plan): G2 the metric's push, the notch and the frozen clock; G3 the strengths and the plan; G4 the shift and the shears; G5 the clicks. **Postulate 6:** the time gear's law, slowdowns composing by their product.
