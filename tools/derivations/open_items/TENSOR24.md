# Tensor24: the node-clock as one act

The owner's words of 2026-10-28, 06:0x UTC (Hebrew, translated): "You be the owner of the plan, the node as one act." Then: "Call the plan Tenzor24. Write it for me here and for everyone in such a file, make sure it stands, divide the work. At its end the whole engine is tensor arithmetic only: say of which order. Explain how the clock enters here, what the node takes and what it gives, and what all the families are. For now only close the plans with everyone, implementing nothing. Make sure that at its end there are no numbers in the code and no circular proofs."

The plan's owner: the Boss. Its base: engine-5.0-test at 526a5666d. Its status: a plan, with nothing built under it. It takes in whole the Reader's proposal of 05:49 UTC (#2187, 6461767760) and the Scribe's SCRIBE-THE-NODE-AS-ONE-ACT-1.md (scribe-5 d2d78b945, #2187, 6461843937). It adds what the Boss's check found and names who does what.

## 1. The end state

- **One act.** Every node-clock does one act, the same for every family: one integer contraction of its own gears and its six neighbours' gears, then one division with a carried remainder (Rule3). The quotient leaves as a click; the remainder stays in the gear.
- **The order.** The engine is integer tensor arithmetic of the second order:
  - its tensors are of rank 0, 1 and 2, the highest being the metric and the stress;
  - every contraction is at most bilinear in the fields, and each is weighed by the clock's scalar;
  - the only steps that are not tensor arithmetic are Rule3's division and the gate's comparisons (a whole winding, the top of a dial, the draw).
- **The 24.** The cube's 24 turns hold by construction. The kinds come from the six spokes alone, so no act knows an axis.
- **No numbers, no circularity.** There is no number beyond 0 and 1 in src, no circular function, no root search, no angle and no closed form of a phenomenon. Every integer of a family stands in the universe, world and setting files.

## 2. What the node-clock takes and what it gives

- **It takes** the board as the tick starts, at itself and at its six neighbours one mesh away: a stencil of seven node-clocks. From each it reads every train's gears: each gear's notch now and before, its fine tooth and teeth, and its drive fine tooth. It reads nothing else: no index of the board, no read of the log, nothing beyond one mesh.
- **It does** one contraction per gear, then one carry (Rule3). The contraction is a sum of products of the stencil's gears, with integer weights fixed by the kinds' product table and the universe file.
- **It gives** three things:
  1. its own gears, written only after every read of the tick (the order-free phase, phase.py);
  2. its clicks, the quotients that leave. The turnover is the clock's own click; a fitting, a chime and a merger are each a few integers (the hand, the node-clock, the windings);
  3. its books: every winding taken is booked, and the remainder is signed.

## 3. The tensors and the families

- **Gears and trains.** A gear is a dial: an integer with a carried remainder. A train is a tensor. Its kind is the way the cube's 24 turns move its dials: they exchange dials (an axis for an axis, with its sign) and they reflect a dial about its mid tooth (the one mirror).
- **The five kinds** are the five irreducible representations of the cube's rotation group. Each is derived from the vector kind (the six spokes) by its products, so no table is typed. The Boss checked this on the 24 signed permutation matrices of determinant 1, by characters:
  - the vector V is T1;
  - its symmetric square is A1 + E + T2;
  - its antisymmetric square is T1;
  - the product xyz is A2;
  - 1 + 1 + 4 + 9 + 9 = 24.

| kind | dimension | what it is on the board |
| --- | --- | --- |
| scalar, A1 | 1 | the clock: the time gear, the rate, the load, the trace; also each of a hand's own two gears |
| pseudoscalar, A2 | 1 | xyz (none on the board on the head) |
| E | 2 | the tensions less their trace |
| vector, T1 | 3 | a gradient, a flow, the offset's odd gears, a curl |
| shear, T2 | 3 | the off-diagonal products (struck from the regulator at d09f1a8a5) |

- **Products** split by the group's product table:
  - the stress, a product of two gradients, is A1 + E + T2;
  - the regulator's seven gears are 2 A1 + E + T1;
  - the offset's four gears are A1 + T1.
- **A family** is a kind and its integers in the universe file (its pair, its spring, its couplings, its weight), nothing more. The engine knows kinds and integers, never a family's name:
  - the light: a hand at the spring 0 (the coupling 0), the null element;
  - matter: hands at a spring above 0, the mass by the pair;
  - the regulator: the metric (the clock's time gear, the tensions, the flows);
  - the offset: the potential (a time gear and three odd gears);
  - the held field: a scalar with a weight, the mediator;
  - the twins: two hands as one spinor, spin one half (see 7 a).

## 4. How the clock enters

- **The clock is the scalar,** the kind the 24 leave in place. At a node-clock that a turn of the cube fixes, only the scalar can be read. So the clock is what every image reads alike.
- **It enters the act in three ways:**
  1. as the weight of every contraction, the local rate of time. On the head these are: p + stretch pull, stretch cross, offset rate div full rate, and the drive's rate squared;
  2. as the dial: every gear's carry is a tick of a clock, and its quotient a turn;
  3. as the turnover: the time gear at its top or bottom is the node-clock's own click, and it mirrors every fine tooth there.
- **The hierarchy:**
  - the board is the great clock;
  - each node-clock has its own time gear;
  - each hand is a small clock;
  - a bound pair that becomes one larger clock is the next level (fusion, row 76; open, 7 c).

## 5. The head as it is (526a5666d)

- **The step.** The Scribe's table of 26 acts (SCRIBE-THE-NODE-AS-ONE-ACT-1.md, read on 97e5b3fd6) stands on 526a5666d by kind: 9 contractions, 8 pointwise maps of one gear, 5 acts of bookkeeping, 2 gates and 2 global reductions. Since 97e5b3fd6:
  - the stress's shear products are struck (d09f1a8a5);
  - the click's phase is order-free (phase.py, 42d5448b7);
  - the turnover mirrors (42d5448b7).
- **The Scribe's scan** (scribe_scan.py, scribe-5 abfbd6ee9) on 526a5666d, counting its blocking rules only:
  - the engine's modules: 95 hits (circular words in names 62, root searches 14, state beyond the node-clock 14, log reads 3, a typed table 1, a number 1);
  - the readers' modules: 57 hits (numbers 23, circular words 13, root searches 11, state 7, typed tables 2, a float 1).
- **The light** is read by identity at 18 places in 7 files (the Boss's count).

## 6. The cuts, and who does what

Every cut goes the same way:
1. David derives it and confirms it on toys-5 before it is built; he writes no engine code.
2. The Boss builds it in his toy and measures it.
3. The Reader benches it.
4. The Scribe's scan passes, with every count falling or equal.
5. The full check exits 0, and the Boss pushes.

The cuts, in order:

1. **The fair draw.** Built in the Boss's toy and measured: the 24 on nature and the hole, the rewind 20 of 20, the suite 118. Pushed on the owner's go.
2. **The gate.** The Scribe's scan goes into tools/check.py's ratchets and the push hook, so it holds every later cut.
3. **The pure contractions, bit for bit:** regulation.stress_of; the hands' products (dot, lead, sweep, products); the meshes' cross and gradient; the offset's curl; Pauli's numerator. They become one contraction act over the stencil, its weights from the kinds' product table.
4. **The pointwise maps:** the rate table and its inverse by search (stretch.load_of, readings.rates_of), the mesh factor, rest_rate_of, the clamps, rounded(p + p + 1, d) and the end teeth's selection. Each becomes a chain of Rule3 carries or integers in the universe file, by David's derivation.
   - With them, every sine, cosine and root search of src leaves for integer data: core/rates.sine_rim; assembly/setting.py's raised_cosine, rim_point, angle_of, angles_of and running_rotation; assembly/cycle.cycle_angles; readings.standard_angle; hands.cosine_count.
   - The three integers of each pair go into the universe file, and the setting's weights into the setting file.
5. **The gate as one act for every family:** the turnover and the click (engage, jam, unwinds, winds, the draw, the bobs, the merger's ends), read whole and then written whole. The light is known by its spring 0, never by identity.
6. **The state beyond the node-clock goes out:** the id() keys, the module-level containers and caches, and the log reads (tick.py, click.py, draw.py, features/).
7. **The two global reductions** (count_max, max_transient) leave the step for the readers.
8. **The end check** (section 8).

| who | the part |
| --- | --- |
| the Boss | owns the plan and this file; writes every line of code; builds each cut in his toy, measures it and pushes it |
| David | derives every cut before it is built (the contraction table from the spokes, the pointwise maps, the twins, the gate as one act) and confirms or refutes each build; writes no engine code |
| the Reader | benches each cut: the 77 rows on the 16 records and the 3 committed charts, the head against the cut, within the hour of each push; clears the readers' own modules under the scan; takes the reductions into the readers |
| the Scribe | the gate on every push; the law's sentence (proposed in his file, entered on the owner's word after the first measured cut); the documents after each cut; the ledger |
| the owner | the law's sentence; the 24 or the 48; the Bell click's form; the bang's seed |

## 7. Open, by name

- **(a) The twins.** A spinor is a representation of the cube's double cover, and its quarter turn needs the square root of 2: on the z axis it is the diagonal (1 - i, 1 + i) over the root of 2. Its half turn is a Gaussian integer. So the 24 cannot hold on the twins' own gears with integers. David derives which way stands:
  - an integer scale exponent carried with the twins; or
  - the twins read only through their bilinears (the density, a scalar, and the spin, a vector), with the 24 asked of those.

  Until then the 24 is asked of the five kinds and of the twins' bilinears.
- **(b) The 48.** With the reflections, every kind splits in two, giving ten kinds. This is the owner's word.
- **(c) The clock of clocks.** Fusion, a bound pair as one larger clock (row 76), after David's derivation, with no new number.
- **(d) The Bell click.** Its form is the owner's word: a detector hand's gear by Rule3's carry (the Scribe's recommendation), or another. The twins' state holds the correlation.

## 8. The end check

- **No numbers:** no number beyond 0 and 1 in src; every integer in the universe, world and setting files. The scan's number and table rules stand at 0.
- **No circularity:** no sine, cosine, root search, angle or closed form of a phenomenon in src, so the scan's circle, root, word and mix rules stand at 0. The Scribe's audit items E1 to E19 are cleared one by one. The click's draw by the parts' sizes is the one chance.
- **Locality:** no state beyond the node-clock, and no act reads the log. The state and log rules stand at 0.
- **No circular test:**
  - every test compares two runs or reads what the engine wrote;
  - no test asserts a number the code typed in;
  - the 24 is read by the images' test on every chart.
- **The step:** one contraction act and one carry; the gate is one act for every family.
- **The counts to bring to 0,** from 526a5666d: the engine's 95 hits (the Boss) and the readers' 57 (the Reader).

## 9. After every cut

- the Reader's per-row diff (77 rows, 16 records, 3 charts);
- the rewind 20 of 20;
- the books closed at every click;
- the 24 on nature and the hole, and the 48 on nature while the reflections hold;
- the suite under the 30 s bound;
- the scan with no count risen;
- the full check exiting 0 before any push.
