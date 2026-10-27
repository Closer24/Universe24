# The spin doublet: two planes for matter, read from the numbers, verified in the clicks

David, 2026-10-27, 12:0x UTC, for the Boss (his tasks of 11:0x and 11:3x UTC), on the owner's words of 11:0x, 11:20 and 11:3x UTC.

## The words

- **11:0x UTC, relayed in the Boss's task, in translation:** "Spin as a pair of planes for matter ... the engine tells no family from another, only the universe file ... every row the same act ... are the 10, 4 and 2 in the code for families?"
- **11:20 UTC, to David, in translation:** "Tell the Boss what to do to verify that it is solved with 2 planes and with the clicks, because Pauli is in the clicks, and force carriers and matter are in the clicks."
- **11:3x UTC, relayed, in translation:** "A declaration is bad, no? There are no declarations."

Each claim carries one of five marks:

- **checked:** the integer algebra by exact fractions (DAVID-SPIN-DOUBLET_CHECKS.txt, item 1);
- **measured:** the engine head 9a5469453 on this box, by the scripts in the same file (items 2 to 5);
- **read:** read from the code;
- **derived:** derived here;
- **unknown:** none of the above settles it.

## 1. Is one doublet enough? (the Boss's item 1)

**In one line.** Two planes carry everything of spin one half that the clicks can read:

- Pauli's two states per Node;
- the two beats in a held field;
- Kramers' T^2 = -1;
- the full turn's sign.

On the cube's turns, two planes carry the half-turns exactly, the 120-degree turns on the even doublets, and the quarter turns up to a phase. The genuine double cover of all 24 turns needs eight lines, the struck row's count. Eight lines buy no click reading that two planes lack.

The facts:

- **The lines.** A doublet is four lines (re_up, im_up, re_dn, im_dn), psi_up = re_up + i im_up and psi_dn = re_dn + i im_dn.
- **The Pauli matrices are integer on the lines.** sigma_z negates the down plane, sigma_x swaps the two planes, and sigma_y = i sigma_x sigma_z. Each is symmetric and squares to I; they anticommute in pairs and commute with the plane's quarter turn J. So a field's coupling Phi . sigma is an integer numerator inside the one carried division. [checked]
- **The half-turns' lifts.** U_a = -i sigma_a is integer, U_a^2 = -I and U_x U_y = U_z; together they make the quaternion group (order 8, centre {I, -I}). Two half-turns about one axis give -I, which is the full turn's sign, exact on integers. [checked]
- **Kramers' T = (i sigma_y) K** maps (re_up, im_up, re_dn, im_dn) to (re_dn, -im_dn, -re_up, im_up).
  - It is integer and T^2 = -I.
  - It is antilinear: T J = -J T.
  - It commutes with every U_a.
  - It flips the spin: T sigma_a = -sigma_a T.

  This is the -1 a plane cannot give: on one plane every antilinear map squares to +I (DAVID-ONE-CLOCK_CHECKS.txt). [checked]
- **The share and the spin density.** N = |up|^2 + |dn|^2 and S_a = psi^dag sigma_a psi are the doublet's readings, with no line of their own.
  - |S| = N.
  - U_a turns S by the half-turn about the axis a.
  - U and -U give the same turn: the 2:1 cover.
  - T sends S to -S and keeps N.

  [checked on 200 random doublets]
- **The 120-degree turns about a body diagonal** are the axes' cycle, a relabelling in the 48.
  - Their lift (I + U_x + U_y + U_z) / 2 has entries +-1/2 and its cube is -I.
  - It is integer on the doublets whose four lines sum to an even number, and keeps that sum even.
  - With the U_a it makes the binary tetrahedral group (order 24).
  - It is exact in the rationals, and only to the floors on Rule3's lines: each line rounds on its own and does not keep the sum's parity.

  [checked; derived]
- **The quarter turns.** The genuine lift (I + U_a) / sqrt 2 holds sqrt 2, which no integer doublet holds. Times the phase e^(i pi / 4) the lift is integer:
  - diag(1, i) about z;
  - ((I + J) + (I - J) sigma_x) / 2 about x, on the even doublets.

  This phased lift turns N and S as the quarter turn does, and its fourth power is +I. So four quarter turns lose the sign with the phase, while two half-turns keep it. [checked]
- **The precession in a held field along z** turns the up hand by -theta / 2 and the down hand by +theta / 2, each a plane's rational turn by Rule3's own division.
  - At theta = 2 pi the doublet is -I; at 4 pi it is +I.
  - A precessed arm recombined with a free arm gives (1 + cos(theta / 2)) / 2, so the period is 4 pi.

  [checked; derived]
- **A correction to DAVID-ONE-CLOCK.md, section 1 (b).** There, "two planes for one axis" read one hand in Z[zeta_8] turning 45 degrees per quarter turn about one axis. The doublet (two hands in Z[i]) does more: all three axes' half-turns exactly, and the cube's 120-degree turns. The sentence "eight lines for all three axes" stands for the genuine lift alone.

What the owner gets in the clicks from each:

| reading | two planes | eight lines |
|---|---|---|
| Pauli: two states per Node, the two spins | yes | yes |
| the two beats in a held field (the Zeeman doublet, gate 41) | yes | yes |
| two spots along a gradient (Stern-Gerlach, gate 42) | yes, for quanta in definite planes | the same |
| Kramers: one beat with no field, T^2 = -1 | yes | yes |
| the full turn's sign (the 4 pi interference) | yes, by the precession's half angle | yes |
| the sign of four quarter turns of the lattice | no, lost with the phase | yes |
| the 48 on the lines | 8 exact, 16 to the floors, 24 up to a phase | 48 exact in the rationals, to the floors on the lines (SR-S2) |
| lines per matter family | 4 | 8 |

## 2. The generic form, from the numbers alone (the Boss's item 2 and his 11:3x consequences)

### The roles

- **Read (rows.py on the head).** The roles are read by the count of lines:
  - CARRIER = 1 + 3d (10) and POTENTIAL = d + 1 (4), both derived from d = AXES, and PLANE = 2;
  - the walled row by its wall.

  The loader also checks the carrier's pair (den - den div Gamma, den) and the potential's pair (den, den).
- **The owner's question.** 10, 4 and 2 are counts derived from d, and none is a family's number. 2 is every record's hand; 10 and 4 are the two field rows.
- **The collision.** A doublet of 4 lines meets the potential's 4 at d = 3 alone, since 2 x 2 = d + 1 only there. The pair tells them apart.

The roles from the count and the pair, no shape read as a role:

| the row's numbers | its role |
|---|---|
| a wall and no pair | the phase row |
| the pair (den - den div Gamma, den) | the clock's row (the regulator), its 1 + 3d lines checked |
| the gap 0, one plane | the light |
| the gap 0, d + 1 lines | the potential |
| a gap, whole planes | a family: one plane, or two (a doublet) |

No number is missing at d = 3, given one sentence of the law: **a doublet has a gap**. That is the one place where the count alone would not tell the potential from a family. Its natural form under either exchange below:

- under A: a gap-0 record is one plane;
- under B: a gap-0 row of two planes is the potential and no record.

[read; derived]

### The exchange, derived (the Boss's 11:3x item 1)

Two derivations, each from the numbers alone:

- **A, from the gap (the Boss's reading).** The gap 0 is symmetric, and a gap is antisymmetric.
  - On every shipped universe it equals DAVID-STEP-2.md's key row for row: the plane at (den, den) +1, every gapped plane -1. So step 2 re-cut with no key keeps its tables.
  - It forbids a massive symmetric family (nature's W, Z and Higgs) and a massless antisymmetric one.
- **B, from the count of planes (spin-statistics, nature's theorem).** One plane is symmetric (spin 0) and two planes are antisymmetric (spin one half), with the sentence that a doublet has a gap.
  - It admits a massive symmetric family: a gapped single plane.
  - It keeps every fermion massive, as nature's neutrinos are.

A and B agree on every universe whose families are doublets and whose light is one plane. They part on two rows:

- a gapped single plane: A antisymmetric, B symmetric (the shipped universes' lifts until they are laid as doublets);
- a gap-0 doublet: A symmetric, B none.

**My advice is B.** The owner's words tie the exchange to the pair of planes ("spin as a pair of planes for matter"; matter antisymmetric, light symmetric). Under B the exchange follows the spin, with no key and no gap read as a statistic. **The owner's word.**

**Does the close then choose by the numbers alone?** Yes. Every act of DAVID-STEP-2.md section 1 (the refusal, the lay, the take, the draw) reads the row's exchange, and under A or B it reads the derived sign instead of a key. The one role left in the close is the emitter, at three sites:

- close.list_of's records.index(node.emitter());
- the merger's read_ends and takes;
- bodies' rec0.

The emitter is the one symmetric record at the gap 0, so it too is read from the numbers. [read; derived]

### The doublet in the engine

- **The file.** The universe file names a matter family as one row of four lines at its pair: {"shape": 4, "pair": [num, den]} with num below den. This is the count and the pair, and no label.
- **The two planes.** The engine carries the row as two planes: up (lines 0 and 1) and down (lines 2 and 3).
  - Each plane is a record for the close and the click.
  - Each plane's partner is the other plane of its row.
  - Every act on a plane stays as on the head: Rule3's step, the share, the charge, the current, the beat and the click.
- **What reads the partner:**
  - the birth (section 5, G7);
  - the merger (G7);
  - the field's coupling (section 3);
  - the credit's frame (a reading).

## 3. What comes back, and its price (the Boss's item 3)

What comes back:

- **The coupling: SR-S3 on two planes.**
  - Phi . sigma enters inside the one carried division of each doublet line.
  - Phi is the one-Link curl of the potential's odd lines (gram.curl at 6501cd679).
  - The coefficient is nu = R / (2 Gamma), from g = 2.
  - sigma_a are the integer matrices of section 1: fixed permutations and signs of the four lines, so no matrix is derived at the load.
- **Kramers' T: no act.** The run back is Rule3's exact inverse on every line: the slots exchanged and the remainders mirrored. So T = (i sigma_y) K enters as a symmetry to read, not as an act: a doublet's mirrored run equals its T image. [derived]
- **The 45-degree turn per quarter turn of space: no act either.** The 48 relabel the Ports. The kit maps a doublet's lines by the lifts of section 1 and compares the phase-free readings (N, S, the charge, the credits by plane) on all 48:
  - exact on 8: the identity, the three half-turns about the axes, the inversion and the three coordinate reflections, with the inversion acting as I;
  - to the floors on 16: the 120-degree turns and their products with the inversion;
  - up to the phase on the other 24.

  [derived]
- **The seed's refusal by state, per plane (SR-S4 on two planes).** A matter lay is refused where its own plane stands at the Node. Its former form, which read the spinor's spin density, was struck at 36a98a8f9. [read]

The law's lines it touches (read in the head's docs/ALGEBRA.md):

- **The three shapes and U-S1, U-S2** ("a plane two lines"): the doublet as two planes, and the strike of SR-S1 to SR-S4, dated at 9a5469453 on scribe-5 (the Scribe's line of 11:2x UTC).
- **SR-S3:** the coupling, on two planes.
- **SR-S4:** the exclusion, per plane.
- **The click's parity:** "no record carries an axial vector" changes for a doublet, which carries S.
- **The cube's symmetry:** the 48 on a doublet.
- **SL-S1 and SL-S2:** the draw, and the conjugate pair's selector across the two planes.
- **MG-S1:** the merger, the birth read at -1, across the planes.
- **MS-S1:** "the charge is one e for every row", which G0 (section 5) keeps.
- **The table:** rows 39, 41, 42 and 43 and the Spin line.
- **Step 2's clauses:** the exchange derived, with no key.

**The price.** Measured on the head on the hole world over 60 intervals, without the field's coupling, by naming every gapped plane twice (the loader admits a repeated pair, CS5-S2):

| | as written | every gapped plane twice |
|---|---|---|
| planes | 4 | 7 |
| integers per Node | 99 | 126 |
| widest integer | 112 bits | 112 bits |
| seconds per interval | 0.296 and 0.289 | 0.525 and 0.496 |
| births | 18 | 25 |
| clicks | 2,262 | 4,497 |
| the run back | 20 of 20 exact | 20 of 20 exact |

- **Integers:** +9 per added plane (two lines of now, before and remainder, and the plane's three counters). So three doublet families cost +27 integers per Node.
- **Time:** about 1.7 to 1.8 times per interval, before the coupling's term.
- **Every record with a matter family moves.**

[measured]

## 4. What the head's clicks show (measured): the ground for the verification

**What a click is (read in bodies.py).** The click is per plane. A plane standing at a whole quantum of its own unit (its share div its unit at least 1) through one beat clicks; the light pays one quantum, and the credit names the plane (its `line`). So with two planes per family, every credit names its spin with no change to the click.

**What was measured.** At every click, the quanta standing in the clicking plane at its Node: the same count the click makes, on the three committed records.

| record | plane (its cos omega_0) | clicks | at 2 or more of its own quanta | most at a click | most at any Node, any interval |
|---|---|---|---|---|---|
| hole 60 | 0 (1 - 1.4e-7, the light lift) | 2,118 | 2,116 | 2,416 | 2,416 |
| hole 60 | 1 (0.162) | 71 | 9 | 2 | 3 |
| hole 60 | 2 (0.170) | 73 | 45 | 4 | 5 |
| chiral 60 | 0 (the light lift) | 2,916 | 2,910 | 2,443 | 2,443 |
| chiral 60 | 1 | 40 | 0 | 1 | 1 |
| chiral 60 | 2 | 47 | 5 | 2 | 2 |
| bodies 120 | 0 (0.99998, the light lift) | 17,173 | 15,586 | 236 | 243 |
| bodies 120 | 1 (0.306, the bodies' family) | 771 | 531 | 70 | 94 |

**At the light's side of the same clicks**, the light at the Node held up to:

- 12,865 of the body's quanta on the hole, 2 or more at 2,087 of 2,262 clicks;
- 20,666 on the chiral, 2 or more at 2,824 of 3,003;
- 1,849 on the bodies, 2 or more at 17,140 of 17,944.

[measured]

**The reading.**

- **Force carriers symmetric are in the clicks already:** the light stands at thousands of quanta where bodies click.
- **Pauli is not in the clicks:** every matter plane clicks with 2 or more of its own quanta standing. The doublet alone does not change that.

**The causes:**

1. **The child's lay.**
   - **Read:** merger.child_levels lays every child at the quarter turn, re_now = A and im_before = B with A B = T div 2, which is MS-S1's one e.
   - **Derived:** at the quarter turn a hand jumps 90 degrees in one tick. That is the rest form only of a clock whose omega_0 is 90 degrees. A child laid so holds den / s of its family's quanta, about 1 / sin(omega_0), with s the pair's sine.
   - **Computed:** den div s = 1,863 for the hole universe's light lift, 1 for its two heavy lifts (omega_0 near 81 degrees), and 171 for the bodies universe's light lift.
   - **Measured:** the hole's first light-lift child holds 1,863 at its - end. The 5 light-lift children hold 1,732 to 2,074, the 7 of plane 1 hold 1 (one holds 2), and the 6 of plane 2 hold 1 to 4 (the larger ones the later births).
2. **The seed.** The bodies are laid as packets of 125 quanta in one plane at width 2, up to 94 at one Node.
3. **The step.** Between lays a plane is a linear wave, and the head refuses only at the lay. Two quanta of one plane can meet at a Node, or the content's weight on the share can raise one quantum. Which of the two raises the heavy lifts' 2 to 5 is **unknown**.

## 5. The verification in the clicks (the owner's word of 11:20 UTC), in order

**G0. One quantum is one quantum.**

- **Build:**
  - the child is laid as the rest form of its own family at its Node's own rule: gram.rest at the row's pair, with the base found by comparisons (no root) so that |W| is one e. That keeps MS-S1, and its share is one quantum by the unit's own definition, PORTS s |W| (measured earlier to the ratio 1.000000000);
  - the quarter-turn form is struck;
  - the seed's matter lays stay at or below one quantum per plane per Node, refused by name above it.
- **Read:**
  - every child at 1 quantum at the lay, where the head's light lift reads 1,732 to 2,074;
  - the census of the quanta per matter plane per Node.
- **If a matter plane still piles to 2 at a Node between lays,** that is the finding, and an exclusion in the step is **the owner's word**.

**G1. The control.** A universe with no doublet runs as the head: the three records SAME but the milliseconds, and the run back 20 of 20.

**G2. Pauli in the clicks.**

- **Every doublet world:** no credit of a doublet plane shows 2 or more quanta standing in its plane at its Node. The credit carries that count (owns div unit, a reading). Two credits of opposite planes at one Node within one beat do occur.
- **The lay world:** one family, quanta laid at one Node in turn:
  - up;
  - up then up: the second is refused by name;
  - up then down: both are laid and both credited;
  - up, down, up: the third is refused.
- **The Reader:** gate 43 per plane.
- **The control:** the same family as one plane (symmetric under B): no refusal, and its credits stand at 2 and more.

**G3. Force carriers in the clicks.**

- The light's quanta at the credit's Node (a reading) stand at 2 and more, as on the head.
- N quanta of the body's unit laid as light at one Node by the account lay read N at the first credit there. They read N^2 under the head's lay (DAVID-STEP-3.md section 2).
- The light is never refused at a crowded lay.

**G4. The two spots (gate 42, Stern-Gerlach).**

- **The world:** the struck world (tools/derivations/toys/lean/records/world_stern_gerlach_on.json: the 9-cube, the held A_x = -(y - c)(B0 + b(z - c)), B0 = 200, b = 100), with an unpolarized beam of one doublet family: one quantum per plane per Node, half in each plane.
- **The reading:** from each credit, its plane and its Node. The up credits' centroid along z and the down credits' centroid stand on opposite sides by 150 milli each. The control (Phi . sigma off) stays within 150.
- **The struck row read NOT SHOWN at 60 intervals** (119 / -118 against 150, its control 112 / -51). So run to 120 intervals and report the split against the interval.
- **One plane and the light:** a one-plane family and the light give one spot.

**G5. The two beats and Kramers (gates 39 and 41).**

- **The world:** one quantum at rest in each plane of a doublet.
- **No field:** the two planes' credits read one beat (Kramers).
- **A held uniform Phi_z:** the two beats split oppositely. The one-interval shift per line stays within one level of num B0 x_now div (3 den Gamma), the struck test ported (tests/test_the_quartet.py at 70ac3b30c).
- **A held Phi_x:** a quantum's credits pass from its plane to its partner and back at the precession's period.

**G6. The full turn's sign (a new gate).**

- **The world:** up quanta on two arms, one arm through a held uniform Phi_z, recombined at a detector Node.
- **The reading:** in phase, the arms make a whole quantum there and a credit; out of phase they make none. The credits at the detector, against the precession angle theta, have the period 4 pi, with none at 2 pi.
- **The control:** Phi . sigma off, flat.

**G7. Spin kept at the close.**

- **The birth.** A light meeting's draw runs over the antisymmetric planes, two per family. It names the - child's plane, and the + child is laid in the partner, so S_z is kept and the light carries none (close.list_of, merger.children_laid, the Birth's two planes).
- **The merger.** Two quanta of one doublet meet as the conjugate pair across the two planes, opposite in charge and in spin (close.meet; merger.read_ends with a plane per end).
- **The reading:**
  - every birth's two children in opposite planes, read from the log;
  - every merger across opposite planes;
  - every pair the Reader finds credited at both ends reads opposite planes.

**G8. The big laws on every doublet world:**

- the run back exact, with every counter compared;
- the charge per plane;
- the momentum law and the flux;
- the reach one Link with the coupling on (the struck test T5 ported);
- the 48 by the lifts of section 1.

**One limit to name.** A quantum split between two planes or two places never stands at a whole quantum in one plane, so it never clicks.

- G4 to G6 read quanta in definite planes, or arms recombined in phase, never one quantum's split.
- **Bell on the spin pairs:** a child turned off its plane splits and never clicks, so only settings along the planes' axis read, with E = -1 for every pair.
- The children's planes are definite at the birth, so the pairs are a mixture of opposite spins: within the local bound, at most sqrt 2 for that mixture. Nature's -cos(a - b) needs the pair's two planes held as one state across the two Nodes, and no act makes one.
- **The split quantum's click** (the measurement's law) is open and is **the owner's word**.

**"Solved with two planes and in the clicks"** means: G0 to G8 pass, and the controls fail as stated.

## 6. The build order (the Boss's item 4)

1. **The toy on 9a5469453** (the toy line re-cut on the head, in the order of your 11:0x line): the carried paces, the exchange rule derived (A or B, no key), the account lay, the click direction.
   - Each step sits behind its flag.
   - With the flags off, the three records stay SAME.
2. **G0 behind a flag:** the child's lay at one quantum, and the seed's one quantum per plane per Node, measured on the three records and the bang world.
3. **The doublet behind a flag:** the roles from the numbers, the two planes, the birth and the merger across them, and the credit's readings. Gates G1, G2, G3, G7 and G8.
4. **The coupling behind a flag (SR-S3 on two planes):** gates G4, G5 and G6, and the 48 by the lifts.
5. **The Reader:**
   - gates 41 and 42 read a doublet: their condition "a shape-8 row" re-cut to "a row of two planes with a gap";
   - gate 43 per plane and in the credits;
   - Bell on the spin pairs, as the limit above allows.
6. **The code on the clocks branch:** after the rename's first stage, on the owner's word for the law's sentences.

**Mine, on your word:** the derivation of A against B, G0's lay (the rest form at one e at the Node's own rule), and any step you hand me in scratch.

## 7. The owner's word, by name

1. **The exchange:** A (the gap) or B (the count of planes, spin-statistics). My advice is B.
2. **G0:** the child's lay at one quantum of its own family, and the seed's bodies at one quantum per plane per Node.
3. **An exclusion in the step,** if G0's census shows a matter plane piling between lays.
4. **Pauli's state:**
   - per plane: two per family per Node, of either charge sense (the head's count);
   - or per plane and sense: four, nature's count with the antiparticle.
5. **SR-S3 on two planes.**
6. **The 48 on two planes:** 24 relabellings up to a phase, where eight lines carry all 48.
7. **The split quantum's click** (the measurement's law).

A document and its checks alone; no code and no test change.
