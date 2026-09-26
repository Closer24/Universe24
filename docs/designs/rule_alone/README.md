# The rule alone: the hard question's runs

Can the engine be built from the rule 9.57 (1) alone (ALGEBRA.md 9.98)? The owner's hard
question (the Boss's records 2134 to 2137 of 2026-09-26): Nature24 answers each item from his
own runs of the rule, in integers with the remainders kept and no motion rule of any kind, with
one verdict, WORKS, FAILS (with what fails) or NEEDS (the one missing thing); the algebra's
number beside the run's, the run written before the algebra's number is looked at (record 2137).
Every number is HOST (the runner's own computation) or GAMEBOARD (a reading of the runner's
board). Nothing here is engine code: the runner is checking code (record 2135).

## 1. The runner

1. `rule_alone.py`: one integer rule, transcribed from ALGEBRA.md 9.91 (2) and 9.57 (1):
   w a_next + r' = SUM R a_neighbour + S a_now - w a_before + r, 0 <= r' < w, with p = Gamma -
   c, R = 2 p^2 num, S = 12 den Gamma^2 - 6 (p^2 + Gamma^2)(den - num) - 12 num p^2, w = 6 den
   Gamma^2; the six neighbours, a level 0 beyond an open face. Its one step is equal to the
   engine's `one_rule` on random arrays (a check of the transcription, not of a number).
2. `bodies.py`: a body is its record on a well (the lowered pair [800, 801] on a cube of side
   5, the kind [800, 850] elsewhere: the species that binds in three dimensions, 9.98 (9)
   (a)); its record starts as the well's bound mode by the shipped generator's own operator
   (HOST, a start value); the moving record is the mode times the character of K at the
   group pace v, both levels split about the standing start with the later sample as now
   (9.98 (9) (b)); the content is s on the well's Nodes and the static level around it; the one
   seam in two forms: the well to the Node nearest the envelope's centroid over its support,
   or the well moved one Node when the record's own current has carried one Link.
3. The envelope of the pair (now, before) at a Node: A^2 = (now^2 + before^2 - 2 now before
   cos omega) / sin^2 omega, omega the pair's own rotation at the Node (HOST floats, a reading).

## 2. The verdicts

| Item | Verdict | The run (HOST) | The algebra | Side by side |
| --- | --- | --- | --- | --- |
| 1. A matter record falls in a content gradient in 3D, on the envelope | WORKS | `item1_fall.py`: a free Gaussian packet of width 20 Links at 2^19 on [400, 64, 64] (periodic across, open along x, the packet at the middle), c = 1000 + g (x - 200), 2100 intervals. g = 1: the centroid 200.00 to 227.83; the acceleration in windows of 300: 1.257e-5, 1.299e-5, 1.221e-5, 1.249e-5, 1.327e-5, 1.148e-5 Links per interval^2 (mean 1.25e-5). g = 0: the centroid at 200.000 throughout, the acceleration below 2e-8 | 9.98 (7) with 9.102 (2)'s factor: 2 (1 - 2U)^3 / (1 + (1 - 2U)^2) x (num / den) g / (6 Gamma) = 0.8055 x 1.5686e-5 = 1.264e-5 at U = 0.05 | 1.25e-5 against 1.264e-5; the windows 0.91 to 1.05 of it. They meet |
| 2. Two bodies attract and move, each by the content alone, the well hopping with the centroid | FAILS | `item2_pair.py`: two bodies of s = 2000 on wells of side 5, 20 Links apart on [80, 32, 32]; the content the two static levels moving with the wells. Seam (i), the centroid over the support: no hop in 3000 intervals, the centroids 30.00 +- 0.2 and 50.00 +- 0.2, the separation 20.0 +- 0.3. Seam (ii), the current: no hop for 375 intervals, then the wells run apart (the separation 27 at t = 400, 76 at 450, 96 at 500) | `item2_algebra.py`: Newton's fall by 9.98 (7) on the static content's own gradient (the lone body's level 2000 on its Nodes, 1394 at r = 4, 695 at 10, 354 at 20), from rest: the separation 19.46 at t = 50, 15.13 at 150, 11.05 at 200; the meeting at t = 249 | The algebra meets at 249; the run never (i) or moves the wrong way (ii). What fails: the seam. The well pins the record (the polarization a fifth of a Link, below half); a seam that reads the record's current feeds its own displacement |
| 3. A bound record put in motion keeps its shape and speed; its clock slows | FAILS | `item3_moving.py`: the body on [240, 32, 32] periodic, its record the mode times the character at v = 0.1 (K = 0.1068, HOST). Seam (i): 2 hops then none in 1500 intervals, the centroid 60.00 +- 0.1, the width along x breathing 2.5 to 40; the pair's phase rate at the centre 0.3007 per interval at v = 0.1 and 0.3007 at v = 0. Seam (ii): the well at 3.5 v, the record dispersed to the board in 300 intervals; at v = 0 no hop (the pace read -2e-5). The free control (no well): the packet moves 60.0 to 71.2 in 200 intervals (0.06 to 0.09 per interval) and disperses | the speed v = 0.1; the clock's ratio omega_K - K v over omega_rest = 0.984 (the dispersion, 9.94 (6)); 1 / gamma = 0.985 at c_l^2 = 1 / 3 | the run's speed 0 and ratio 1.000 against 0.1 and 0.984. What fails: the seam; the rule carries the momentum in the record's phase (the free control moves), the declared well stops it |
| 4. The vector part: the dragging; the Lorentz force | NEEDS | not run: the vector part acts on a record through the transport's twist (9.81 (2), 9.91 (6)), a rotation by an exact triple of the twist table per Link; the table cannot hold the angles the rows need (tools/twist_table.py, the finding of 2026-09-26: the smallest triple angle with d at most 10^9 is 6.3e-5 radians, theta_unit is 3.8e-10), so an integer run of the transport does not exist yet | 9.77 (6) (b), 9.78 (9) (a) | the one missing thing: the twist table's form (the mathematician has it); a float rotation would not be the rule in integers |
| 5. A wound record keeps its winding and precesses | WORKS (the winding); the precession waits on item 4 | `item5_winding.py`: the standing mode times the winding m = 1 about z as a rotating pattern of the two levels, at rest in its well on [64, 64, 64] periodic. The well of side 5: the pattern is not bound, the width grows 12 to 34 Links and the angular momentum reading L swings between -3 and +1 of its start in 1500 intervals. The well of side 9: L holds at 0.84 to 0.92 of its start for 1500 intervals, the width 5 to 7 Links, the peak 7e4 to 8e4 steady; the pattern turns at 0.290 per interval (the mode's own rest rotation 0.252) | 9.98 (9) (c): the winding number m = S div M, the profile the bound mode in the sector of angular momentum m, vanishing on the axis; the precession under a field 9.78 (9) (e) | the winding holds in a well that binds the sector (side 9), within a tenth over 1500 intervals; a well of side 5 binds no wound state. The pattern's own rate 0.290 against the s-like mode's 0.252 is the sector's level, read; the precession needs the vector part (item 4) |
| 6. The recoil as a rotation of the pair at a click, a phase gradient near 1e-8 per Link | FAILS | `item6_recoil_write.py`: the pair (now, before) of the bound record rotated at every Node by k dx and rounded: at the amplitude 2^17 and at the bound 2^20, k = 1e-8 (the quoted gradient), k = 7.6e-8 (the recoil of one quantum, Delta v = 1 / (1000 s lambda_q) = 2.4e-8 at s = 2000, lambda_q = 21, K = 3 (den / num) Delta v), 1e-7 and 1e-6 change NO integer at any of the 245760 Nodes; the first changes come at k = 1e-5 (at 2^20: 9810 Nodes, 100 of the well's 125) and k = 1e-4 (at 2^17) | 9.98 (2): the recoil a rotation of the body's pair by the transport's primitive, a phase gradient of k_q / M | lost at the write: one click's rotation is below one integer at every Node, and the rule's remainders cannot recover a phase that was never written. What is needed: a store of the clicks' momentum beside the rule until it is writable (about 130 quanta at 2^20), the accumulator in another name |
| 7. A local source from the record's current and stress | WORKS as a reading | `item7_local_source.py`: on the moving mode at v = 0.05, 0.1, 0.2 the pace the local source implies at each Node, v_i = (num / den) J_a(i) / (3 F_i): the median on the well's 125 Nodes 0.0506, 0.1037, 0.2295 (min to max 0.036 to 0.064, 0.073 to 0.132, 0.157 to 0.284); on the support (about 15000 Nodes) the median 0.0497, 0.1019, 0.2173 with the quartiles a tenth either way; the local source's total over the support 4 s x 0.0504, 0.1028, 0.2189; at rest the current 0 at every Node exactly | 9.98 (4) as redesigned in 9.102 (3): 4 s J_a(i) div F_i at the Node alone, zero at rest; its sum 9.91 (3)'s 4 s v | the total within 1, 3 and 9 percent of 4 s v; the per-Node pace within a third of v. A source with the Node and its six neighbours alone exists |

## 3. What is needed beyond the rule and the click

0. **Summary of the seven.** WORKS: 1 (the fall), 5 (the winding holds), 7 (a local source
   reads). FAILS: 2 and 3 (a bound body does not move by a seam that reads it), 6 (one click's
   recoil is below an integer). NEEDS: 4 (the twist table's form). Three things beyond the
   rule and the click are needed and named below: a body that can move, a store of the
   clicks' momentum, and the transport's table.
1. **A body that can move.** A record bound in a declared pair-well is not moved by the rule
   alone through a seam that reads the record: the centroid seam pins it, the current seam is
   unstable. The rule moves a free record (item 1) and carries the momentum in the record's
   phase (the free control of item 3); the declared well stops it. Either the well is the
   record's own (matter's self-binding, P_2 not 0: 9.98 (8)'s big decision for three) or the
   body keeps a store of its motion beside the rule (the accumulator that 9.98 (5) (a) deletes).
   The mathematician has the question.
2. **A store of the clicks' momentum.** One click's recoil (item 6) changes no integer of the
   record at the bound 2^20; the rule's remainders carry only what was written. Until about a
   hundred quanta have been taken the momentum has nowhere to live but a per-body tally.
3. **The transport's table.** The vector part reaches a record only through the twist (item
   4), and the twist table of 9.96 (2) (c) cannot hold its angles in triples with d at most
   10^9; the form is the mathematician's.
4. **The bound mode's start.** The generator's bound mode is not stationary under the rule at
   rest in three dimensions: with the well fixed, the record's peak swings between 2e4 and
   1.6e5 and its width along x between 4 and 17 Links over 1500 intervals (GAMEBOARD of the
   runner, `item3_moving_v0.0.json`). The loader's residual bound admits a profile that sloshes.
   This is the mode, not the rule; it does not change the verdicts.

## 4. The runs not read, kept in the folder

1. Item 1's first run: a packet of width 8 on [200, 24, 24] spread to the board in 500
   intervals and its control drifted by the near face's reflection (the runner's open face
   reflects; the engine's absorbs). Fixed by the wider packet at the board's middle.
2. Item 2's first run: the centroid over the whole board, which the mode's tail pulls; the
   displaced wells pumped the record and the wells met at t = 287. Withdrawn: not evidence.
3. Item 3's first run: the gravity time part stepped by the rule on a fully periodic board
   floods it (no face to sink it), the pace falls and the record blows up at t = 1050. Fixed by
   the content as the hold alone.
4. Item 2's gravity time part stepped by the rule with the hold on this runner's reflecting
   faces rang by 15 percent for 1500 intervals (the midpoint content 1193 to 1557) and never
   settled; the static level moving with the wells replaced it.

## 5. The eighth question: the rate row against the well's multiplicities (record 2140; 9.103 (4))

Written before either number was read (record 2137); the readings are added below them.

1. **The algebra's number**: the multiplicity of the well's bound levels under the cube group,
   from the margin operator's spectrum on the well's own board (HOST). `item8_spectrum.py` is
   the Lanczos iteration named in 9.103 (4); its levels each count 1, and that count is the
   method's, not the well's: a Krylov space from one starting vector meets every eigenspace in
   one direction, so a Lanczos iteration from one vector cannot show a multiplicity. Its file
   is kept as a run not read (section 4). `item8_dense.py` reads the counts from the full
   symmetric eigendecomposition of the same operator on a 16^3 and a 20^3 periodic board and
   from the shift-invert eigensolver on 32^3; a level is a cluster of eigenvalues within 1e-6.
   The cube group's irreducible dimensions are 1, 1, 2, 3 and 3: a count of 3 is a p-like
   triplet.
2. **The run**: `item8_rate_worlds.py` writes six worlds in the loader's words of today and
   `item8_rate_read.py` reads the one command's outputs. The beam board [512, 21, 21] (x open
   with one-Node face slabs, y and z periodic); an emitter body of the matter family on the
   well [800, 801] of [32, 5, 5] holding 100 quanta of a second massive family `target` of
   the same kind [800, 850] (no reads) and giving them as trains along +x at the given clock
   [512, 1] on N = 1024 (the wavelength 4 Links, 8 periods, K = pi / 2, the shipped beam
   train; the slower trains were tried before any run: K = pi / 8 is a body of 128 Nodes
   whose mode the generator's iteration did not reach in 20 minutes, and K = pi / 4 at 8
   periods books 0.9802 of its norm through the plane 40 Links ahead, refused by the
   generator's passage check of 9.25 (11)); at x = 380 the
   receiver the emitter names, per side s in {5, 9, 13}: `well`, a body of the target family
   on the well [800, 801] of side s seeded on its bound mode and bound to the set by `block`,
   or `cube`, the same cube of free Nodes with no well (the control). The reading (DETECTOR):
   the clicks at the receiver per 100 givings and the wait from the giving; well less cube
   per side is what the well adds to the click.
3. **What the design already says.** A bound level's frequency lies below the kind's band
   (that is what bound means), so no train of the family carries a level's energy; the
   emitter feeds the well with rows of the continuum, and the click at the well reads the
   one-way flux into its cube (9.25 (2), (3)). The multiplicity can enter the rate only
   through what the well does to a passing row; the run measures that.

## 6. The ninth question: a body held by its clicks (records 2152, 2154, 2155)

No well and no self-binding: between clicks a body is a free record and the rule spreads it;
a click localises it again. `item9_clicks.py` and `item9_pair.py`; the readings as JSON beside
them (the runs of 2026-09-26, 09:00Z).

1. **The environment and the click (HOST, the runner's choices, stated once).** Every Node is a
   detector (the owner's picture of record 2154). The click is the engine's ladder: the
   record's one-way flux into every Node is booked at every interval, and the click fires when
   2 W C reaches (2 u + 1) T, T the record's norm (the rule's own conserved form of 9.57 (1),
   in the flux's units: a moving packet's passage through a plane books 0.9997 of it), W = 700,
   u a stated residue sequence. The click's Node is Born's: the point at a second residue's
   fraction of the interval's increment. The record is deleted whole and re-created at that
   Node with its norm (`whole`); or, the owner's picture, a click takes one quantum at one
   Node, and the 2000 quanta leave the shared profile one by one and each steps and clicks on
   its own (`quantum`). The kind [800, 850], the packet's rms 7.1 Links on 64^3 periodic.
2. **A finding on the ladder's order.** When one interval's increment exceeds the record's
   whole norm (a record at one Node in a bath of detectors: 0.30 of the norm at the first step
   after a click, 0.68 at the second), the ladder's declared order alone picks the Node and
   Born's rule is lost; the runner samples the increment by a residue instead. For the
   engine's cube detectors, whose increments are small against the norm, the order is Born's.

| Run | Reading (GAMEBOARD of the runner) | Algebra beside |
| --- | --- | --- |
| (a) `control`, the free packet | rms 7.1 to 16.6 in 250 intervals, then the 64-board is full (the readings 15.5, 7.6, 17.8, 14.1, 8.6 are the wrapped board's) | the free spread of item 1: 14.1 to 59.9 in 2100 intervals |
| (a) `whole` | the first click at 21; then one click per 1.73 intervals (856 in 1500); the width 0.0 to 0.2 for ever; the peak's distance from the start 9.3, 16.2, 17.0, 15.4, 12.2, 8.8 at 250 to 1500 (no walk beyond the first click's Node); the norm 1.0000 | a record of one Node is re-clicked at its own Node: the flux comes back to the centre at the second step |
| (a) `quantum`, 2000 quanta | all quanta out of the shared profile by interval 200 (1943 by 100); the pattern's rms 11.3, 11.9, 11.8, 11.4, 11.0, 11.5 at 250 to 1500, BOUNDED; the quanta's rms distance from the start 19.6 to 20.5, constant (= sqrt 3 x 11.4: no quantum moves after its first click); 1,693,277 clicks (one per 1.77 intervals per quantum); no leak from any box | the width the packet had when its quanta were all clicked; the mathematician's number (the click rate that holds a width w) is owed |
| (b) `pair`, two bodies 20 apart, each reading the other's content | the separation 20, 21, 29, 26, 28, 25, 22 at 0 to 1500; no approach; 857 and 855 clicks | item 2's algebra: two bodies of s = 2000 from rest at 20 Links meet at 249 intervals |
| (b) `moving`, v = 0.1 (K = 0.1096, omega_K = 0.3502) | the first click at 5; the peak 38, 36, 33, 33, 35, 36, 39 at 0 to 1500 against v t = 63 to 188: the body stops at its first click | `moving_control` with no click: the centroid 38 to 53 in 250 intervals (a packet of rms 4 is broadband; item 3's control moved at K's pace) |

3. **Verdicts.** (a) WORKS: the clicks keep the width bounded, in both forms; the free packet
   fills the board. (b) FAILS: the two bodies do not approach, and the moving body stops at its
   first click. The click that holds the body is the click that freezes it: the record
   re-created at a Node carries no phase gradient, so a click forgets the pace, and the fall
   between two clicks (1.7 intervals) is 10^-4 Link. What is needed is the same third thing as
   before: a click that keeps the record's momentum (the store of the clicks' momentum, 9.98
   (8)), or an environment that clicks far less often than every Node, at the price of the
   width. Both numbers are the mathematician's to set: the click rate that holds a width w and
   the rate that lets a body fall.

## 7. The commands

    PYTHONPATH=src python docs/designs/rule_alone/item1_fall.py 1 2100
    PYTHONPATH=src python docs/designs/rule_alone/item1_fall.py 0 2100
    PYTHONPATH=src python docs/designs/rule_alone/item2_pair.py 3000 [current]
    PYTHONPATH=src python docs/designs/rule_alone/item2_algebra.py
    PYTHONPATH=src python docs/designs/rule_alone/item3_moving.py 0.1 1500 [free] [current]
    PYTHONPATH=src python docs/designs/rule_alone/item7_local_source.py
    PYTHONPATH=src python docs/designs/rule_alone/item8_dense.py 9 16 dense
    PYTHONPATH=src python docs/designs/rule_alone/item8_dense.py 9 32 sparse
    PYTHONPATH=src python docs/designs/rule_alone/item8_rate_worlds.py
    PYTHONPATH=src python tools/run_inputs.py --out RUNS --jobs 3 docs/designs/rule_alone/worlds/*.json
    PYTHONPATH=src python docs/designs/rule_alone/item8_rate_read.py RUNS
    PYTHONPATH=src python docs/designs/rule_alone/item9_clicks.py check
    PYTHONPATH=src python docs/designs/rule_alone/item9_clicks.py whole|quantum|control 1500
    PYTHONPATH=src python docs/designs/rule_alone/item9_pair.py pair|moving|moving_control 1500

The readings are written beside the scripts as JSON (the runs of 2026-09-26).
