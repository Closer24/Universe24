# The rule alone: the hard question's runs

Can the engine be built from the rule 9.57 (1) alone (ALGEBRA.md 9.98)? The owner's hard
question (the Boss's records 2134 to 2137 of 2026-09-26): Nature24 answers each item from his
own runs of the rule, in integers with the remainders kept and no motion rule of any kind, with
one verdict, WORKS, FAILS (with what fails) or NEEDS (the one missing thing); the algebra's
number beside the run's, the run written before the algebra's number is looked at (record 2137).
Every number is HOST (the runner's own computation) or GAMEBOARD (a reading of the runner's
board). Nothing here is engine code: the runner is checking code (record 2135).

PARKED (the model owner's word of 2026-09-26, 12:50Z, in Nature24's session): the eighth
question of record 2140 (its sixth engine world was stopped unfinished; the five finished
outputs and the click rates of section 5 stand as read), the hard question's open items and
the well's study runs wait until a generic engine stands; until then the physicist works on the
generic engine alone with Coder 3, and writes no code. Nothing here is a result; every number
is a GAMEBOARD reading of the runner unless labelled otherwise.

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

## 7. The four runs of ALGEBRA.md 9.98 (11): the binding as a family (record 2157)

The mathematician's generic line (c): every record writes its local count s_i = F_i div E_s
into the t part of gravity and of a binding family; every matter record reads gravity with the
weight 1 and the binding family with the weight K_m; the binding family is held, of degree 0,
with its own pair below [1, 1] (a range of a few Links); no pair well, no hop, no tally.
`binding_family.py`, the readings as JSON beside it (the runs of 2026-09-26, 09:30Z).

1. **As run (HOST choices, stated once).** F_i = now^2 + before^2 - 2 now before cos omega_i
   from the record's pair alone, cos omega_i the Node's rest rotation at the content read there
   in the interval before. The binding pair [54, 55]: the held level's static equation is
   SUM_neighbours a = 6 (den / num) a, so kappa^2 = 6 (den / num - 1) = 1 / 9, the range 3 Links
   asked. The hold after the held families' plain step (9.85 (2)); the pace p_0,i = Gamma - g_i -
   K_m b_i; the guard p > 0 ends a run. The board 48^3 with open faces; the record a standing
   Gaussian of sigma = side / 2 at 2^17 (a start, not the mode). Three readings of E_s, the
   source's scale: `level`, E_s = F_peak(0) div s (the peak reads s = 2000 at the start, the
   level the mathematician's table of 9.98 (10) (h) binds with, K_m s at the Nodes); `count`,
   E_s = SUM F_i(0) div s (one count's form, the counts summing to s); `cap`, `level` with s_i
   cut at s (a saturation, not the line: what the cut does).
2. **The algebra's numbers beside.** The table of 9.98 (10) (h) at [800, 850]: a uniform
   content binds from c near 3500 at side 5 (the tail 12 Links at 4000) and from c near 2000 at
   side 9 (the tail 6 Links at 3000); K_m s = 4000 at K_m = 2. The fall of two bodies of s =
   2000 from rest at 20 Links: meeting at 249 (item 2's Newton integration). The moving body:
   x = x_0 + v t.

| Run | Reading (GAMEBOARD of the runner) | Verdict |
| --- | --- | --- |
| (1) `level`, the line as written, side 5 and 9, K_m = 1, 2, 3 | THE GUARD at interval 18 to 61 in all six runs: the record concentrates, its form at the peak grows, the count at the peak passes s (3261 at interval 25 for side 5, K_m = 2; 4538 for side 9, K_m = 1), and the content reaches Gamma (10002 to 16676) | FAILS: a runaway. A source that follows the record's own form deepens the well as the record concentrates, and the rule in three dimensions has no stop before the guard |
| (1) `count`, the counts summing to s | the content at the peak 66 (side 5) and 12 (side 9) at the start, then the counts flicker to 0 as the packet spreads (rms 1.8 to 9.4 at 500); the guard at 746 and 878 from the held families' waves piling up on the runner's reflecting faces, not from a binding | FAILS to bind: with s conserved as a count over the Nodes, the level at a Node is s times the Node's share of the form, far below the table's 3500 |
| (1) `cap`, the level cut at s | side 5, K_m = 2: rms 1.8, 3.7, 7.2, 9.9, 11.9 at 0, 25, 500, 1000, 1500, the peak's count 2000 to 98, the bound share within 12 Links 1.00 to 0.11: disperses. Side 9, K_m = 2: rms 3.2, 3.8, 5.4, 6.2, 6.0; the peak's count 2000 throughout, the content 6000; the tail 3 to 5 Links; the bound share 0.76 to 0.85; the rotation measure 2 SUM now before / SUM (now^2 + before^2) gives omega 0.42 to 0.48 against the vacuum's 0.345 (a trapped packet that sloshes, not a mode below the band). Side 9, K_m = 3: the guard at 189 | binds at side 9 with K_m = 2, at rms 6 with a tail of 3 to 5 Links, beside the table's tail of 6 at 3000; not at side 5. The cut is a new operation, not the line |
| (2) `moving`, `cap` side 9 K_m = 2, v = 0.05 and 0.1 | the centroid 16.0 to 21.5 (250), 21.8 (500), then 16.8 to 19.0 against x_0 + v t = 91; at v = 0.1: 16.0 to 24.7 (500), 25.6 (750), then 21.8 to 23.0 against 166; the width 6 to 8; the `level` moving run hits the guard at 39 | FAILS: the body moves 6 to 9 Links and stops, pinned |
| (3) the leak, in every run | the rule's form at the current coefficients over its start swings 0.65 to 1.20 over 1500 intervals in the bound runs; the count sum 400,000 to 1,000,000 | the form is not conserved under a pace the record itself changes; a norm for the self-sourced record is owed by the algebra |
| (4) `pair`, `cap` side 9 K_m = 2, 20 Links apart | the separation 20.0, 12.9 (250), 5.85 (500); at 532 the two sources overlap and the guard fires (content 12000) | the attraction WORKS at about half the pace of item 2's algebra (meeting at 249); a moving one keeps its shape (rms 6 to 8) but not its motion (row 2) |

3. **The sum.** The line as written runs away in three dimensions at every K_m tried; with the
   counts conserved it binds nothing at s = 2000; with a cut at s it binds at side 9 and pins the
   body. What the runs ask of the algebra: the source's scale E_s with a stop (the count's cap
   or another), the norm of a self-sourced record, and the moving self-bound body's pinning
   against the free record's motion (item 1 and 9.98 (7)).

## 8. The click that keeps the momentum (the Boss's record 2160) and the wide self-bound body

1. **The click that keeps the momentum, as run** (`item9_pair.py ... keep`, `Record.
   recreate_with_momentum`): at a click the record is re-created at the click's Node as a
   packet of rms 3 carrying its momentum K and its norm. K is CARRIED as a label: set from the
   record's start, changed between clicks by what the rule did (the reading now less the
   reading just after the last re-creation; the reading itself, sin K = sin omega_K SUM J / I
   with I the rule's invariant, is biased low on a narrow packet, 0.069 read on a packet of
   rms 3 carrying 0.1006, and re-imposing the reading alone lost the momentum in 50 clicks).
   The click's Node by Born's rule on the record's form (`density`) or on the inward flux
   (`flux`, the engine's). The displacement to the click's Node is the detector's share.
2. **A finding on the flux rule in a bath of Node detectors.** A Link's flux is booked to the
   Node it enters, so the click samples a moving packet half a Link ahead of its density: the
   mean share along the motion +0.48 Link per click over the first 50 clicks (GAMEBOARD), and
   the body at v = 0.1 went 38 to 450 in 1500 intervals, 2.7 times its speed. For the engine's
   cube detectors the bias is the cube's wall against its side; for Node detectors it is the
   whole Link. The `density` runs below sample the form.

| Run | Reading (GAMEBOARD of the runner) | Algebra beside | Verdict |
| --- | --- | --- | --- |
| `moving keep density`, v = 0.1 | the peak 38, 42, 64, 99, 108, 134, 142 at 0 to 1500: a speed of 0.069 Link per interval over 364 clicks; the carried K 0.1006 to 0.1005 | v t: 188 at 1500 (the plane wave's 0.1); a FREE packet of rms 3 moves at 0.083 to 0.086 in its first 100 intervals and one of rms 12 at 0.098 (the calibration `packet_speed`, HOST): a narrow packet is slower than its K's group pace under the rule | WORKS: the body keeps a speed, the narrow packet's own, 0.7 of the plane wave's |
| `still keep density`, v = 0 | the peak 38, 27, 30, 46, 29, 24, 44: a walk of 10 to 15 Links, no drift; 317 clicks | the walk of one record re-created at a Born Node: about (w / 2) sqrt(N) (9.98 (10) (i)) = 1.5 x 18 = 27 | the walk as the algebra says; no motion from nothing |
| `pair keep density`, 20 Links apart, eight residue seeds | the separation at 1500: 5, 16, 31, 29, 34, 16, 3, 13 (the mean 18.4, the spread 11, the error of the mean 4); at 250: -1 to 58 (a body crossing the periodic seam flips the reading) | item 2's algebra: meeting at 249 | NOT READABLE in the one-record form: the two bodies' walks (20 to 30 Links each) hide a 20-Link approach; the mean shows no approach. The form of M records (the walk over sqrt M, 9.98 (10) (i)) would decide: owed, a heavier build |
| `binding_family` `cap`, side 13, K_m = 2 (the owner's question of 09:40Z: a wider body) | at rest: rms 4.6, 4.7, 10.1, 5.2, 6.5, 5.9 at 0, 25, 250, 500, 1000, 1500, the peak's count 2000 throughout, bound; moving at v = 0.05: the centroid 16.0, 24.6 (250), 24.4 (500), 25.9 (1000), 25.7 (1500) against 91: pinned after 9 Links, as side 9. Side 17 on the 48-board reaches the faces and the guard (a run not read) | | the pinning is not the narrow body's alone |

3. **The sum for record 2160.** A click that carries the momentum lets a body keep its speed
   (0.7 of the plane wave's, the narrow packet's own) and does not move a body at rest. Whether
   two such bodies fall together is hidden by the whole body's Born walk in the one-record
   form; the many-record form is owed. The engine's flux rule, in a bath of Node detectors,
   adds half a Link forward per click.

## 9. The runs of ALGEBRA.md 9.108 (the Boss's record 2163): the saturating table and the two families

The mathematician's two corrected forms of the binding line after section 7's collapse:
the source as a saturating table, s_i = s_cap F_i div (s_cap E_s + F_i) (9.108 (3)), and two
families with no table, a hollow of range 3 Links read +K_m and a hill of range 1 Link read
-K_r (9.108 (7)). `binding_family.py` with `source=table|core`; the pairs [1000, 1019] and
[1000, 1181]; the readings as JSON beside it (the runs of 2026-09-26, 10:15Z). The table's
numbers hold at the start: side 9, K_m = 2, s_cap = 4000 gives K_m T = 2666 at the peak, as
9.108 (3) says. For the two families the floor 2666 at the peak needs K_r = 2 / 3 at K_m = 2;
the runs take integer weights and the core's source scaled by 3 / 2 (K_m = 2, K_r = 1, E_core
= 3 E_s / 2, the floor 2666 + gravity), and beside it (3, 2), (2, 1), (2, 2), (2, 3), (3, 4).

| Run | Reading (GAMEBOARD of the runner) | Algebra beside | Verdict |
| --- | --- | --- | --- |
| (1) table, side 9, K_m = 2, s_cap = 4000, at rest | no guard over 1500; the content at the peak climbs to 9500 to 9800 (the ceiling 8000 plus gravity's own share); rms 3.2, 3.7, 12.7, 7.0, 8.4, 9.5 at 0, 25, 250, 500, 1000, 1500; the bound share within 12 Links 1.00, 0.95, 0.08, 0.77, 0.62, 0.45; the rotation measure 0.46 to 0.53 against the vacuum's 0.345 | bound at a finite width, no guard | the runaway is stopped; the record sloshes out to the board and back, half of it stays bound at 1500 |
| (1) table, side 5, K_m = 3, s_cap = 3000 | the guard at 686 (content 10800): the ceiling 9000 plus gravity's 1800 passes Gamma; the record disperses first (the bound share 0.08 at 250) | below the guard | FAILS: gravity's weight 1 was left out of "K_m s_cap below Gamma" |
| (2) table, side 9, moving, v = 0.05 and 0.1 | v = 0.05: the centroid 16.0, 21.8 (250), 25.6 (500), 21.8 (1000) against 28.5, 41, 66, then the guard at 1145; v = 0.1: the guard at 156 | x_0 + v t; the speed ratio v / (K / m_rec) | FAILS: it moves 10 Links and wanders; the content reaches Gamma as it concentrates |
| (3) table, the form's means over windows of 300 | at rest: 0.92, 0.97, 1.19, 1.36, 1.67; moving: 1.34, 1.65, 1.94; the pair: 0.92, 0.96, 1.03, 1.06, 1.13 | no drift; the field's form in antiphase | FAILS: a secular drift of 13 to 94 percent in 1500 intervals; the binding family's form falls 3.6e7 to 1.7e7 and rises to 2.9e7 with no clear antiphase |
| (4) table, the pair 20 Links apart, the fields at the pace and plain | the separation 20.0, 4.4 (250), -10.6 (500), 7.6 (1000), -1.3 (1500): the bodies meet before 250 and pass through each other; the two pace forms give the same record readings to four figures (the hold rewrites the field at the support every interval, so the field's pace changes nothing for the record) | item 2's meeting at 249 | WORKS: the meeting at the algebra's time |
| (1) two families, K_m > K_r (2 and 1 with the core scaled 3 / 2; 3 and 2; 2 and 1) | the guard at 31 to 76 at rest, 39 to 58 moving, 76 in the pair: the record concentrates as in section 7 | bound at a finite size where the hill and the hollow balance | FAILS: a runaway |
| (1) two families, K_m <= K_r (2 and 2; 2 and 3; 3 and 4) | the content at the peak 2000 (gravity alone) or 0; the record disperses: rms 3.2 to 13 by 1500, the bound share 0.10 | | FAILS: nothing binds |

1. **Why the two families give no size.** The engine's held family is written to the source's
   level at the source's Nodes whatever its pair; the range shapes only the tail outside the
   support. So at the record's own Nodes the hollow and the hill are K_m s_i and K_r s_i, and
   their difference has one sign everywhere: attraction that runs away or repulsion that
   disperses, nothing between. A balance by range needs fields whose value at the source
   grows with the range, a sourced field (Poisson's), not a held level. This is a property of
   the hold, the engine's primitive, not of the weights.
2. **The sum for record 2163.** The saturating table is the one form that stops the runaway,
   and two such bodies fall together at the algebra's 249. But the body it makes sloshes to
   the board's edge and back, keeps about half its form within 12 Links, drifts in its form
   by tens of percent, does not move freely, and reaches the guard when gravity's share is
   added to the ceiling. The two-family stop does not work with held fields. A gap in these
   is the mathematician's (9.108 (6)).

## 10. The sourced two families (ALGEBRA.md 9.108 item 10 (a) to (d); the Boss's record 2171)

The binding [1000, 1019] read +K_m = 2 and the core [1000, 1181] read -K_r = 4, SOURCED: each
interval the record's count s_i is added into each family's now level at its Nodes and each
steps by the rule at the Node's pace (`pace=1`) or plain (`pace=0`); gravity the hold as built;
the fields start at the static response to the start's source ((2 - M) a = s by relaxation,
HOST; at the pace, two passes); E_s set by that response so that K_m b - K_r h at the start's
peak is the floor asked (`floor=`); the board 64^3 periodic (`wrap=1`), the start a Gaussian
of sigma 4.5 (the runs of 2026-09-26, 10:50Z). `binding_family.py ... source=sourced`.

| Run | Reading (GAMEBOARD of the runner) | Algebra beside | Verdict |
| --- | --- | --- | --- |
| the static start | the plain response gives the floor asked within the counts' rounding (1480 for 1500, 2484 for 2500, 3482 for 3500); at the pace the response is larger and grows with the depth: 1924 for 1500, 6944 for 3500, 23804 for 6000 (the guard at interval 0) | K_m b - K_r h = 1500 at the peak, with gravity's 2000 the pace lowered 3500 | the peak's count is 157 at the floor 1500 (the response per count is 9.5), so gravity's hold there is 157, not 2000; the paced response feeds on its own depth |
| (1) at rest, side 9, the floor 1500, fields at the pace | rms 3.2, 4.1, 5.9, 8.1, 10.6, 13.0, 15.1, 16.8 at 0 to 175; the count at the peak 157, 98, 26, 9, 3, 1; the content at the peak 2117, 850, 542, 283, 159, 81; the bound share 1.00 to 0.06; then the guard at 198 | bound at a finite width for 3000 intervals | FAILS: disperses within 100 intervals; the well flickers and fades with the counts |
| (1) at rest, plain fields, the floors 1500, 2500, 3500 | the same dispersal (rms 3.2 to 15 by 150 to 200); the content at the peak flickers (3853, 1083, 1949, 993, 527 at 0, 25, 50, 75, 100 for the floor 3500); then the guard at 155 to 213 with contents of 3e7 to 3e12 | | FAILS, and the guard is the rule's instability, below |
| (2), (3), (4) moving and the pair, the floor 1500, at the pace | the guard at 176 to 191, the same dispersal first | | not reached |

1. **Why it fails, two findings for the algebra.** (a) A sourced massive field rings: the
   injected count balances the static level only while the source is constant; when the record
   spreads or moves, the fields oscillate at their own rest rotations (the binding's period 33
   intervals, the core's 11) with no damping and no propagation of the K = 0 part, so the net
   well, a small difference of two ringing fields, flickers (3853 to 1083 to 1949 in 50
   intervals) and the record is not held. (b) A hill can drive the pace above Gamma. Where the
   core's level exceeds the binding's and gravity's, the content is negative (-44 at 50, -227 at
   145, -3149 at 155 in the plain run) and the pace exceeds Gamma; the rule's step is stable
   only while the pace stays below about 1.25 Gamma (the K = pi mode's factor (S - 6 R) / w
   against -2), so at -3149 the record grows exponentially (its level 9139 to 17,889,190 in 20
   intervals), its counts and the fields with it, and the guard fires on the overflow. The
   engine's guard is one-sided (p > 0); a repulsive read needs the other side too (p <= Gamma),
   and with it the hill can only lessen a hollow, never exceed it.

## 11. The pair in the many-record form (the Boss's record 2167)

`item9_many.py`: two bodies of M = 100 records each (one per quantum), 20 Links apart on [96, 48,
48] periodic, each record on its own box of side 25 with the click that keeps the momentum (the
label carried, the re-creation at rms 3.5 by Born's rule on the form); each record reads the
other body's content, item 2's cube of side 5 at level 2000 about the other body's centroid (a
one-Node source, the first run, is 125 times weaker and its fall is unreadable in 1500
intervals). `null`: the same with no content. The runs of 2026-09-26, 10:33Z (27 minutes each).

| Reading (GAMEBOARD of the runner) | Algebra beside | Verdict |
| --- | --- | --- |
| the mean momentum label of each body's records along x: +0.041 and -0.028 at 250, +0.055 and -0.018 at 500 (the bodies fall toward each other), then mixed as the clouds pass; in `null` exactly 0 throughout | item 2's meeting at 249; 9.109 (3): the fall accrues in the phase between clicks and is re-read at each click | the FALL is read in the momentum: WORKS |
| the clouds: each body's records walk apart from one another (the walk of one record 20 to 30 Links by 1500, 9.98 (10) (i)), so a body's records spread over the board and the centroid read about one record wraps (the separations 20, 11.5, 29.5, -23, -3, 23, 1.3 and, in `null`, 20, 17, 54, -4, 20, 19, 56 are the wrap's, not a motion); 28,000 clicks per body, the leak 5e-4 | the centroid's walk over sqrt M; the cloud's size the walk itself | the MEETING is not readable: the clicks hold each record's phase and position, not the records together; without a binding the body is a cloud of the walk's size by 1500 |

## 12. The sourced form run again with the four corrections (ALGEBRA.md 9.108 item 12; the Boss's record 2188, the study run of the well)

The mathematician's four corrections, each an option of `binding_family.py` so the earlier runs
stand: (i) the pace bounded on both sides, 0 < p <= Gamma (a content below 0 is cut at 0 and
the cut Nodes counted, `hill_excess`; a content at Gamma ends the run); (ii) the stationary
start at the pace, `passes=8`: the record's ground mode (the eigenvector of the step operator
M(content) with the largest 2 cos omega, a shifted power iteration, HOST floats) and the fields'
static levels iterated together, the fields at the pace of the content of the pass before; (iii)
absorbing faces as a sponge of 8 Nodes on an open board of 64^3 (`sponge=8 n=64`, the damping
0.12 ((8 - d) / 8)^2 per interval on every stepping level, the record's tails included); (iv)
v = 0.05 (v / w = 0.011 against the fields' rotations 0.19 and 0.56). Side 9, K_m = 2, K_r = 4,
the floor 1500 at the Gaussian (E_s 12,454,244); the fallback the hold with the table, s_cap
3000, the ceiling (K_m + 1) s_cap = 9000 (E_s 980,857). The runs of 2026-09-26, 12:00Z to 12:30Z.
The deciding reading, the mathematician's: the ringing amplitude of each field at the start's
peak Node over windows of 300 intervals, (max - min) / (2 |mean|), under 0.05.

The stationary start converged in both forms (the content's change at the peak per pass: 1637,
1355, 524, 213, 103, 15, 23, 12 for the sourced; 3600, 801, 447, 24, 15, 9, 3, 3 for the table;
the mode's omega 0.3372 and 0.3396 against the vacuum's 0.3447; the peak content 2553 and 3003).

| Run (GAMEBOARD of the runner) | Reading | Algebra beside | Verdict |
| --- | --- | --- | --- |
| (1) sourced, at rest, 1500 intervals | the record disperses: rms 5.65, 6.07, 10.6, 11.0, 9.6, 11.1, 10.6 at 0, 250, 500, 750, 1000, 1250, 1500; the bound share 0.80, 0.74, 0.24, 0.21, 0.32, 0.20, 0.23; the content at the peak 2591, 1450, 228, 36, 102, 16, 340; the ringing of the binding per 300: 0.41, 1.35, 0.96, 0.89, 2.01; of the core: 0.79, 2.47, 3.42, 2.07, 8.51; the hill's excess (the content cut at 0) at 2136 Nodes (max 2) at 0, 89,919 (78) at 250, 169,507 (185) at 1000; the record's form means per 300: 0.955, 0.931, 0.631, 0.471, 0.333 (the sponge takes what leaves) | the ringing under 0.05 decides | FAILS: 0.41 in the first window and growing; the body is not held |
| (2) sourced, moving v = 0.05 | the guard at 294 (the content 10808 at Gamma); at 250 the centroid 10.5 Links on (12.5 expected), rms 5.6 to 4.5, the content at the peak 2584 to 4346: the record concentrates and the fields run away | v t = 12.5 at 250 | FAILS |
| (3) the fallback, the hold with the table, at rest, 1500 intervals | the record collapses onto the table's ceiling: rms 5.76, 5.77, 6.80, 3.33, 2.87, 2.30, 1.98; the count at the peak 1001, 2820, 2883, 2895, 2882, 2888, 2909 (the cap 3000); the content at the peak 3003, 8460, 8649, 8685, 8646, 8664, 8727; the bound share 0.79 to 0.99; the ringing of the binding per 300: 0.44, 0.024, 0.010, 0.008, 0.008; the record's form means 0.67, 0.29, 0.31, 0.40, 0.50 | the ringing under 0.05; 9.108 item 12: "the stable size is where the net well per quantum is deepest, finite" | BOUND, at the ceiling: the ringing under 0.05 after the first window; the size is the table's (rms 2), not the mode's; half the record radiated into the sponge |
| (4) the fallback, moving v = 0.05, ceiling 9000 | the guard at 340 (the content 10673 at Gamma); 7 Links in 250 intervals against 12.5 (0.55 of v); the form 0.65 at 250 | v t | FAILS: the held fields at the pace overshoot the ceiling 9000 near Gamma when the body moves |

1. **Findings for the algebra (record 2137: a gap is the algebra's, the run is not adjusted).**
   (a) With the stationary start, the sponge and the bounded pace, the sourced form still
   disperses at rest, and the two fields' ringing GROWS (0.41 to 2.0 and 0.79 to 8.5 relative
   over 1500 intervals): it is not a transient of the start that the faces would carry away; the
   source moves as the record spreads, the fields follow with their own rotations, and the
   coupled system runs away in integers at this floor. (b) The hill's excess is not a rounding
   of the tails: the core's ringing exceeds the binding's over 10^5 Nodes far from the record,
   where both are small; the bound at Gamma acts on a large region, so "a hill lessens a hollow
   and never exceeds it" is not what the integer fields do once they ring. (c) The fallback
   holds the body by collapsing it onto the table's ceiling; the ceiling 9000 at 0.9 Gamma is
   unstable under the paced held fields when the body moves (the guard at 340), and at rest the
   record radiates half its form while it collapses. (d) On a board with a sponge the record's
   form means are not a leak test; the leak reading is the sponge's.
2. **The runner's changes (checking code, record 2135):** the two-sided bound with the count of
   the cut Nodes; the stationary start's passes with their report; the ground mode by a shifted
   power iteration; the sponge; the ringing reading; `n=` for the board's side. Outputs
   `binding_*_n64_sponge8_passes8_*.json`.

## 13. The send on fewer than six Ports (the Boss's record 2197; the model owner: "motion is the replication of events at the Nodes")

`send_ports.py`: a free packet of the kind [800, 850] (rms 4.2, amplitude 2^11) at rest and
moving at the group pace 0.1 along +x, on [160, 48, 48] periodic, 200 intervals, with THE SEND
DECLARED ON A SET OF PORTS (the step's send, the ledger's primitive 13): the arrival at a Node
through its Port -a is the neighbour's send through its Port +a, and a neighbour that does not
send there delivers nothing; the own term and the wall are the six-Port rule's. Readings every
25 intervals (GAMEBOARD of the runner): the envelope's centroid, its rms, the total norm over
its start, the level's maximum. A first run of 600 intervals showed the free packet filling the
periodic board by 200 intervals (rms 24 at 200, 30 after), so the readings stop at 200.

| The send | At rest | Moving (0.1 expected) | Verdict |
| --- | --- | --- | --- |
| all six Ports (the law's own) | the centroid at 40.0 through 75 intervals, then the board's filling moves it (43.3, 47.1, 51.7 at 150 to 200 as the rms passes 18); rms 3.0 to 13.4 at 100; the level's maximum 236 | the centroid 40.0, 41.2, 43.4, 46.3, 48.4, ... 59.6: the speed 0.098 over 200 | the control: the packet moves at the group pace and disperses, nothing grows |
| five Ports, no send toward +x | the centroid drifts toward -x, 40.0, 37.3, 33.0, 27.8, 22.5 at 0 to 100 (-0.17 per interval) while the norm grows 3.7, 540, 5.7e5, 2.5e9 times its start; by 125 the board is full at a level of 1.8e7 everywhere | the same drift and the same growth, the declared momentum makes no difference | UNSTABLE and asymmetric: a one-sided send is a gain, the rule's step amplifies without bound and the pattern runs toward the side it does not send to |
| four Ports, no send along x | the centroid exactly 40.0 at every reading; rms grows in y and z only (3.0 to 10.0 at 200); the norm 0.43 to 0.77 of its start (the standing pair's oscillation); the level's maximum 485 | the centroid 40.0 to 40.3 and back to 40.0: the speed -0.0001 against 0.1 expected; the momentum along x does nothing | STABLE and STILL: with no replication along x there is no motion along x, whatever the phases declare |
| three Ports, +x, +y, +z only | the centroid runs toward +x, 40.0, 43.3, 47.5, 55.2, 66.6 at 0 to 100 (+0.27 per interval) while the norm grows 64, 3.4e9, 9.2e9, 1.3e10 times its start | the same | UNSTABLE and asymmetric, the run toward the side that is sent to |

1. **The reading for the owner's word (record 2197).** Motion is the replication of events
   through the Ports and nothing else: with the sends along an axis removed the packet does not
   move along it even when its phases carry the momentum (the four-Port run), and the six-Port
   rule moves the moving packet at the group pace (the control). A send that is not symmetric
   (five Ports, three Ports) is not a slower or a one-sided motion: the rule's step loses its
   conserved form and amplifies without bound, the pattern running toward the side of the
   missing or the present sends. So the law's own send is all six Ports, symmetric, and the
   step's send declaration admits a symmetric set (an axis on or off) and refuses a one-sided
   one, or the guard ends the run. The mathematician's line on the asymmetric operator's
   spectrum is owed; the run is the reading. Output `send_ports.json`.

## 14. The commands

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
    PYTHONPATH=src python docs/designs/rule_alone/item9_pair.py pair|moving|moving_control|still 1500 [keep] [flux|density] [seed N]
    PYTHONPATH=src python docs/designs/rule_alone/binding_family.py rest side=9 km=2 source=level|count|cap
    PYTHONPATH=src python docs/designs/rule_alone/binding_family.py rest side=9 km=2 source=table scap=4000
    PYTHONPATH=src python docs/designs/rule_alone/binding_family.py moving side=9 km=2 v=0.05 source=table scap=4000
    PYTHONPATH=src python docs/designs/rule_alone/binding_family.py pair side=9 km=2 source=table scap=4000 pace=1
    PYTHONPATH=src python docs/designs/rule_alone/binding_family.py rest side=9 km=2 kr=1 source=core corescale=3/2
    PYTHONPATH=src python docs/designs/rule_alone/item9_pair.py moving 1500 keep density width 1
    PYTHONPATH=src python docs/designs/rule_alone/binding_family.py rest side=9 km=2 kr=4 source=sourced pace=1 wrap=1 t=3000 floor=1500
    PYTHONPATH=src python docs/designs/rule_alone/item9_many.py pair|null 100 1500

The readings are written beside the scripts as JSON (the runs of 2026-09-26).

> The scripts of this folder (`binding_family.py`, `bodies.py`, `item1_fall.py`, `item2_algebra.py`, `item2_pair.py`, `item3_moving.py`, `item5_winding.py`, `item6_recoil_write.py`, `item7_local_source.py`, `item8_dense.py`, `item8_rate_read.py`, `item8_rate_worlds.py`, `item8_spectrum.py`, `item9_clicks.py`, `item9_many.py`, `item9_pair.py`, `packet_speed.py`, `send_ports.py`) were deleted on 2026-09-26 (the model owner's word, record 2229: code not in use goes); git history keeps them at `6d2a92e2` (`git checkout 6d2a92e2 -- docs/designs/rule_alone/<script>`).
