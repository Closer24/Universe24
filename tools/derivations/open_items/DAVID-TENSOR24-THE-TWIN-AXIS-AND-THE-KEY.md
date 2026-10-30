# The twin's axis step (OPEN 3) and Planck's key on swept area

David, 2026-10-29, for the Boss and Sofer. This closes two of the open steps of my 6488233005, by the owner's word of 04:1x UTC ("Close every open step. Let it enter the engine if corrections are needed, through the Boss"): step 7, the twin's axis step (OPEN 3), and step 8, Planck's key on swept area. Each claim is a reading of the law or a probe's line: twin_frame.py and planck_key.py in derive/david_open/twin/ with their outputs, run on the tensor24 src at 298bec5d8 (the engine's own carry, home, flip and tick). No src is pushed.

## 1. OPEN 3: what is open
- **The finding** (the plan's section 11, item 11; TENSOR24.md, line 1651; the ruling's (iv)): a twin hand's four integer rows carry the axis half turns' lifts as signed permutations, so the element-wise carries keep them. In no basis do the third turns' lifts act so, since 2T = SL(2,3) has no subgroup of index 2, and the quarter turns' lifts need the root of 2.
- **The consequence:** element-wise carries on the rows cannot keep the 24 on a twin hand, and no twin train loads before OPEN 3 closes (stage 6).
- **My route** (DAVID-TENSOR24-THE-CLOCK-READING.md, item 10): carry what the 24 permute. Its step is below.

## 2. The step: the 24 turn the twin's frame, and its rows take a sign
1. **The rows are the twin's amplitudes in its frame.** A twin hand's four rows are the quaternion A = a0 + a1 i + a2 j + a3 k, its two hands up and down. Its frame is one integer quaternion q, held once for the universe's twin trains and laid at q = 1 by the load. On the board the twin is q A / |q|.
2. **Each turn g of the 24 has an integer lift u,** with R(u) v = u v conj(u) / N(u):
   - the identity 1 and the three axis half turns i, j and k, of norm 1;
   - the six quarter turns 1 +- i, 1 +- j, 1 +- k and the six edge half turns i +- j, j +- k, i +- k, of norm 2;
   - the eight third turns 1 +- i +- j +- k, of norm 4.

   The lifts close under the product up to a whole factor at all 576 pairs.
3. **The image of a world under g:**
   - the Node-clocks and every kind's gears turn by g, as signed permutations;
   - the frame turns: u q = e q', with e the sign that puts q' in its canonical sign (its first coordinate that is not 0 above 0);
   - the twin's rows take the sign e alone: where e = -1, the now and before slots and the drive's fine tooth negate, and the fine tooth and the going flip, as at every negation.

   No row meets a matrix that is not a signed permutation, so the element-wise carries keep the image bit for bit. That is "carry what the 24 permute": the carried rows are signed, and the frame, which no carry touches, takes the product.
4. **The frame enters the act in one place:** where a twin meets a T1 reading (a field b, a gradient, another train's spin). There the coupling is the left product with the frame-relative field conj(q) b q, an integer pure quaternion, and the drive's teeth carry the frame's norm, T_d = T_d0 N(q). The pull through the Meshes, the spring, the twin's own split draw (S . m within one frame) and T read no frame.
5. **Where the lift's norm is 2 or 4,** the frame's norm, the coupling's numerator and the drive's teeth all grow by N(u). The image's act is then the same act by p18's common factor on the drive alone, with its fine tooth mapped r_d' = N(u) r_d.
6. **The axis on the board,** S = M(q) S_q / N(q) with S_q = A i conj(A) (so S . S = rho rho), turns by g exactly, and the density stays.
7. **The full turn:** four quarter turns about z bring the frame to 4 q, the same frame, and give the rows the sign -1; eight give +1. So the twin's full turn is -1 on its rows and +1 on the 24's kinds.
8. **T on the twin rows** is the right product by j: (up, down) to (-conj down, conj up), so T T = -1. A right product commutes with every frame turn, which is a left product.

## 3. Measured (twin_frame.py, exact integers)
- **The images test:** 12 worlds of 27 Node-clocks, 6 rounds each, every turn with both of its lifts (48): 576 of 576 bit for bit.
  - the identity, 24 of 24;
  - the axis half turns, 72 of 72;
  - the quarter turns, 144 of 144, with the drive's factor 2;
  - the edge half turns, 144 of 144, with the factor 2;
  - the third turns, 192 of 192, with the factor 4.
- **The run back:** 12 of 12 worlds return bit for bit after 6 rounds.
- **The axis on the board:** it turns by g, with the density kept, at 15,552 of 15,552 Node-clock readings.
- **T T = -1** at 324 of 324 twin hands.
- **The full turn:** on four frames, (1, 0, 0, 0), (2, 1, 0, 1), (3, -1, 2, 1) and (1, 1, 1, 1), four quarter turns give 4 q with the sign -1, and eight give 16 q with the sign +1.
- **Mutants:**
  - the field turned and the frame left unturned: it parts at every turn but the identity (24 of 24, 48 of 48, 48 of 48 and 64 of 64);
  - the drive's teeth without the frame's norm: it parts exactly where N(u) > 1 (48 of 48 quarter turns, 48 of 48 edge half turns, 64 of 64 third turns) and holds at the identity and the axis half turns;
  - the departure, the rows turned by the lift: the lift's product on the rows is a signed permutation for the identity and the axis half turns alone, and for every other turn its columns have norm 2 or 4, so no carry keeps it.
- **One reading that is no mutant:** the frame put in its canonical sign without handing the sign to the rows also holds 576 of 576, because the act is odd. The twin's overall sign is a symmetry of the act, as nature's spinor sign is never seen.

## 4. What enters the engine, through the Boss
- **Stage 6** (OPEN 3 before any twin train loads):
  - the layout holds the twin frame q, one integer quaternion, laid at 1 by the load;
  - a twin's coupling to a T1 reading is the left product with conj(q) b q through the ring's product, at the drive's teeth T_d0 N(q).
- **Stage 8** (the 24 on the state): the images test turns the twin frame by the lift and signs the twin rows, with the drive's fine tooth mapped by p18 where N(u) > 1.
- **Nothing else:** no new act and no new number, only products, sums and the carries that stand. At q = 1 the run is the act on the board's own frame; the frame is what makes the 24's images exact.

## 5. Planck's key on swept area (planck_key.py, on 7a's own tick)
1. **The law already counts a quantum by swept area:**
   - line 915: "Planck's relation holds on the lattice, wind = I sin omega with I = A^2 sin omega / T the adiabatic invariant and T for hbar";
   - line 1039 (rows 10 and 13 of **The conventions and the units**): one quantum is 2 A^2 sin omega = T, its energy T sin omega;
   - line 715: A^2 sin omega is "the adiabatic invariant of Rule3's area-preserving step".
2. **In clocks, A^2 sin omega is the swept area.**
   - A hand sweeps Im(conj(a) b) per tick between its now and its before, twice the triangle they span.
   - Per gear, the orbit in its own plane of now against before is the ellipse a^2 + b^2 - 2 a b cos omega = A^2 sin^2 omega, whose area is pi A^2 sin omega.
   - So one quantum is one fixed swept area, the key, whatever the train and its frequency. The count is n = 2 Q div key, one carry with its remainder kept, where Q = SUM Im(conj(a) b) is a whole number at every tick.
3. **Then the energy follows:** for a mode of the act, E = 2 W sin(omega) Q exactly, with E = W SUM (a - b)^2 - s SUM a F(b) the act's own conserved form. So E / n = W key sin omega: Planck's E = h nu on the lattice (sin omega for omega), with one constant, W key, for every train. The head's winding, 3 key s, reads the train's own sine; the count by swept area reads none.
4. **Measured:**
   - the setup: a ring of 24 Node-clocks, W = W+ = 1,536,000, s = 1, the grip W / 6, the key 36,000 and 4,000 quanta laid;
   - the hands: light, and a massive train with D = W / 40, each at k = pi / 12, pi / 6 and pi / 4, for three turns each;
   - E / (2 W Q sin omega) lies from 1.000000 to 1.000014;
   - the count runs from 3,997 to 4,002;
   - E / (n W key sin omega) lies in [1.00000, 1.00026] over both trains and all six waves;
   - Q drifts by at most 7.0 x 10^-4 over three turns: the remainders' walk, which the charge identity books exactly.
5. **What enters the engine:** the whole click's count on the swept area, n = 2 Q div key. That is the drive's carry at the teeth key (my 7b table's T_d = key for a hand's kicks), with Q the hand's own reading, the charge page's density over 2 W. No sine of a train is read. It belongs to stage 9's whole click, through the Boss.

## 6. What stays open
- **The twin's coupling as Pauli's sigma . B.** The left product conj(q) b q A is the probe's coupling, a source on the drive. That in the act's second-order form it gives the precession about B at 2 mu |B| is the derivation of the twin's own formula at stage 6. This page settles its covariance, not its physics.
- **Twin trains in two frames:** one frame serves every twin train of a universe. A universe with twins in two frames reads one through the other by the product of the two frames, by the same mechanism, which no probe here runs.
- **The key's value:** 36,000 is the example universe's. Whether it is nature's h in the lattice's units is the calibration of Gamma, den and the Mesh, which is not derived here.
- **Q's walk:** the count moves by a few quanta in 4,000 over three turns, the remainders' walk; a click's books close on it exactly through the charge identity (7a's charge test), and its size against nature's counts is the clicks' to show.
