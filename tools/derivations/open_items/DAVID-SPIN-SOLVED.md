# Spin one half on two planes: built in scratch, measured on the board and in the clicks

David, 2026-10-27, 13:0x UTC, for the Boss, on the owner's words of 12:02 UTC.

## The words

The owner's words of 2026-10-27, 12:02 UTC, to David, in translation:

- "There is no former spin, right? Everything moves to the new spin, derived from the clocks, the board and the clicks, right?"
- "Only when spin and spin one half are solved completely, pass it to the Boss, and explain what it is in clocks, on the board and in the clicks."
- "The important law beyond Pauli: matter is symmetric and force carriers are not symmetric, and that brings Pauli; note that on the board it is something else, with the phase, and in the clicks it is something else."

Behind them:

- 11:20 UTC, to David: verify it with 2 planes and with the clicks;
- 11:0x UTC, relayed: spin as a pair of planes for matter;
- 11:3x UTC, relayed: no declarations.

**No former spin.** The shape-8 row is struck from the engine (4b5c3d834) and from the law (01d41264f). Everything below is new and is read from the universe's numbers.

Each claim carries one of four marks:

- **measured:** the scripts in DAVID-SPIN-SOLVED_CHECKS.txt, on the scratch build DAVID-SPIN-SOLVED_DIFF.txt (the engine head 900fc2f4a plus 6 files, +165 -36; the four patches in the checks file are its steps, the diff the whole);
- **checked:** exact fractions;
- **read:** read from the code;
- **derived:** derived here.

## 1. The answer

**Spin one half is built on two planes and runs in scratch on the engine head, with no number of a universe added.** Measured on the scratch build:

- a matter family is one row of four lines at its pair, carried as two planes;
- the field's curl turns the pair through the Pauli matrices, with the coefficient of g = 2;
- every birth and merger keeps the spin;
- the run back stays exact;
- the head's records stand bit for bit when no row is a pair.

Measured on the board:

- the spin's direction comes back after one full precession;
- the hands come back negated, the overlap with the free run at -1.01;
- they come back whole only after two full precessions, at +1.006.

Measured in the clicks:

- each plane holds at most one charge per Node at every click;
- the two planes beat as one with no field (Kramers) and apart in a held field (the Zeeman doublet);
- the boundary between a precessed half and a free half clicks at 2 pi and is silent at 4 pi, while the spin points the same way at both;
- the light stands at several quanta where bodies click.

The two spots of Stern-Gerlach show on the board and not in the clicks (section 2, item 5).

[measured]

## 2. What it is, in clocks, on the board and in the clicks

### In clocks

- **The matter family.** A matter family is **a pair of hands** at every Node: the up hand and the down hand, each a plane, each line a two-wheel clock turned by Rule3's carry. A force carrier (the light) is **one hand**.
- **The field is a gear between the two hands.** The curl Phi of the potential's odd lines enters each line's force as SUM_j R_j SUM_a Phi_a (sigma_a x), through one carried division at the wall 2 PORTS Gamma, with its remainder carried as one more fine wheel. So no remainder is thrown away and the run back is exact.
- **What the gear does:**
  - sigma_z speeds one hand and slows the other: the two beats;
  - sigma_x and sigma_y pass the motion from one hand to the other: the precession.
- **The gear's ratio is one half, and it is not put in.** The coupling's matrices are the Pauli matrices, which are the half-turns' lifts up to i (U_a = -i sigma_a, integer on the four lines). When the field has carried the pair's axis once around, each hand has turned half a turn against the free run, so the hands read -1. Two turns bring them home.
- **Kramers' T is the reverse gear.** It carries the up hand onto the down hand and back with a sign, and twice gives -1.
- **The light** has no partner to gear with: a turn is a turn, +1.

[checked; measured]

### On the board, with the phase

**The board holds the doublet's four lines per Node.** The spin S is a reading of the two hands: S_z = |up|^2 - |dn|^2, and S_x, S_y from the cross products.

**After one full precession** S is back, while every line of the doublet is the negation of the free run's. The sign lives in the phase of the hands, which no reading of one hand shows.

**Measured** on one mode (the heavy lift laid uniform, k = 0), with the curl held uniform along x (the control):

| precession | interval | S_z / N | overlap with the free run |
|---|---|---|---|
| pi | 7 | -0.95 | -0.15 |
| 2 pi | 15 | +0.94 | **-1.01** |
| 3 pi | 25 | -0.99 | +0.04 |
| 4 pi | 36 | +0.98 | **+1.006** |

So S_z = cos(theta) and the overlap = cos(theta / 2).

**A second world** confirms it (the curl held in one half of the board). At the moment the spin's x part is back at +0.87, the up plane's phase across the boundary is 180 degrees. [measured]

### In the clicks

**What a click is (read in bodies.py).** One plane stands at a whole quantum through one beat, and the light pays one quantum. The credit names the plane, so every click names its spin with no change to the click. [read]

1. **Pauli.** Counted by the charge, each plane holds at most **one** charge per Node at every click and at every Node at every interval, on every family and both planes. The check ran on the hole and the chiral as doublets.
   - Two planes per family give two quanta per Node, of opposite spin.
   - The charge is the count, because each child carries one e (MS-S1).
   - The energy count is no count of quanta (section 6). [measured]
2. **Kramers.** With no field, the two planes beat alike: up 625 clicks and down 625, every beat 2 ticks. [measured]
3. **The two beats (the Zeeman doublet).** In a held curl along z, the up plane beats slower and the down plane faster: up 375 clicks with beats 2 and 3 (mean 2.33), down 750 clicks with beats all 2.
   - The one-interval shift per line is +15 on the up plane and -15 on the down plane at B0 = 400, the derived num B0 x div (3 den Gamma) exactly.
   - This is the struck row's own test, passing on two planes. [measured]
4. **The full turn's sign.** Both planes are laid just below one quantum, so the bulk stands at no whole quantum, with the curl held in one half. The boundary Nodes stand when the halves' hands are opposite:

   | the halves' hands | precession | clicks at the boundary |
   |---|---|---|
   | opposite | around 2 pi (43 to 489 degrees) | **1,224** |
   | agreeing | around 4 pi (499 to 786 degrees) | **0** |

   The spin's x part reads +0.94 at 2 pi and +0.96 at 4 pi. The clicks tell apart two states whose spin is the same. [measured]
5. **The two spots (Stern-Gerlach): shown on the board, NOT SHOWN in the clicks.**
   - **On the board,** the spin's gradient pushes the two planes apart. The curl is held at 400 + 4000 (z - c) along z, with the orbital coupling off:
     - the up plane alone moves to +112 milli and the down plane alone to -100 at interval 30;
     - together they reach +52 and -94;
     - with the term off, 0.

     The force is small, because the heavy lift's packet is slow (R / w = num / (3 den), 0.054). [measured]
   - **In the clicks:**
     - **at the struck row's world:** the field's orbital pull drags both planes alike (up +369 and down +398 milli, the control +270 and +356, 60 intervals);
     - **with the spin force alone at the gradient 400:** the clicks' centroids carry about 150 milli of noise (up +137 and down +150, the control +54 and +208);
     - **at the gradient 4000:** the click rate itself follows the local beat, since a slowed plane clicks less (1,915 and 1,841 clicks against the control's 338 and 316). So the clicks' centroid is no reading of the packet's place: up -232 and down -32 milli, against the board's +52 and -94, with the control at -169 and +300.

     The struck row read NOT SHOWN as well (119 / -118 against 150). **Owed:** a reading of the place free of the beat, or a slower world. [measured]
6. **Force carriers symmetric.**
   - The light stands at many quanta where bodies click, up to 12,865, 20,666 and 1,849 of the body's quanta on the head's hole, chiral and bodies (DAVID-SPIN-DOUBLET.md section 4). It pays one quantum per click.
   - N quanta laid in its one plane at one Node hold N, not N^2 (DAVID-STEP-3.md section 2, the account lay).

   [measured]

## 3. The law the owner named

The owner's sentence: "matter is symmetric and force carriers are not, and that brings Pauli; on the board it is something else, with the phase, and in the clicks it is something else". Read in the two places he names:

- **On the board, with the phase:**
  - matter is a symmetric pair of planes: its two hands carry the same clock (one beat with no field), and T maps each onto the other with T^2 = -1. Its phase needs 4 pi.
  - A force carrier is one plane with no pair. Its phase is back at 2 pi.
- **In the clicks:**
  - matter is antisymmetric: one quantum per plane per Node. A second child is refused where its plane stands, which keeps the charge at one e per quantum, since n children in one plane at one Node would carry n^2 e. So a family holds two quanta per Node, one per spin plane.
  - The force carrier is symmetric: N quanta in its one plane at one Node, energy N.
- **So the pair brings Pauli.** The board's symmetric pair, with its T^2 = -1 and its 4 pi, is what gives a family two states per Node in the clicks. The one plane shares states. One number decides both: the count of planes (DAVID-SPIN-DOUBLET.md section 2, derivation B).

**Asked of the owner:** whether this reading of his sentence is his. [derived; measured]

## 4. The build (DAVID-SPIN-SOLVED_DIFF.txt, against the head 900fc2f4a)

**The diff's base.** The engine head moved to 67a7633d5 while this was measured: the rename's stage 1a, every identifier in clock words, the records SAME. The diff is against 900fc2f4a and uses the names from before the rename. The re-cut onto 67a7633d5's names, by DAVID-CLOCK-NAMES.md sections 3.1 to 3.6, is mine on your word.

1. **rows.py:**
   - a row of four lines at a gap that is not the clock's pair is carried as two planes, each the other's partner (no new shape, no key: the count and the pair);
   - the + child's plane is the partner of the drawn one (`plus_plane`).
2. **close.py:**
   - the refusal and the crowding read each child at its own plane;
   - a doublet meets across its two planes (the record at the Link's +a end, its partner at the other, opposite in charge), the two ends' planes passed to the take;
   - the undo lays each end back on its own plane.
3. **merger.py:**
   - the two children laid each in its own plane;
   - the merger's ends each read and written on its own plane.
4. **interval.py:** the coupling, SR-S3 on two planes, as in section 2.
5. **run.py:** a doublet birth's entry names the + child's plane.
6. **seed.py:** a lay names the plane of a doublet (`"plane": 0` or `1`).

**The test switches** (SPIN_TERM, HOLD_CURL, HOLD_CURL_GRAD_Z, HOLD_CURL_X_BELOW, SPIN_G0) are environment strings for the measurements, outside the law. The engine's build drops them.

**The engine's suite on the scratch build:** 103 of 106 passed and 3 failed:

- the numbers and names gate, on the switches and on the four lines' index literals;
- the refusal test of a shape-4 row off (den, den): refused still, but by the potential's absence, since a gapped row of four lines is now a family;
- the record test, which passes (19 of 19) once a doublet birth alone names its + plane, as the diff does.

## 5. Measured

| check | world | result |
|---|---|---|
| the control | the hole 20 and the chiral 30, no doublet | the state hash the head's own (2a2cf7426cf6a7d7, c2c11f072d6630db) |
| the spin kept at the close | the hole 60 as doublets | 38 births, every matter birth in opposite planes, born up 32 and born down 32; 6 mergers, every one across the two planes; S_z made by the close 0; the run back 20 of 20 |
| the spin kept at the close | the chiral 60 as doublets | 34 births, born up 32 and born down 32; 2 mergers, across the planes; S_z made by the close 0; the run back 20 of 20 |
| the run back with the coupling | a doublet pair in a field left to the engine, and in a held curl | 20 of 20 and 20 of 20 |
| the two beats' shift | one interval at B0 = 400 | +15 and -15 against the derived 15 |
| the record | the hole record, the scratch build | the engine's own bit for bit (the suite's record tests, 19 passed) |

The board and the clicks are as in section 2. [measured]

## 6. Corrections to DAVID-SPIN-DOUBLET.md

1. **Section 4's "Pauli is not in the clicks" read the energy count.** That count, share div unit, is no count of quanta:
   - a quantum held at one Node by a slow clock moves fast, about 1,863 of its own rest quanta for the light lift;
   - the content's weight raises the share.

   **The charge per sense counts quanta.** By it, the born matter holds at most one quantum per plane per Node at every click on the head:
   - the heavy lifts at most 1.13 per sense on the hole and 1.2 on the chiral;
   - |W| div e at most 1 at every click and Node, on all three records.

   The bodies' seeded packets do break it: both senses superposed, up to 25 quanta per sense at a click, the seed laying 125 quanta in one plane. [measured]
2. **G0 is withdrawn.** Laying a child at its own family's rest form at one e makes the light lift's child a one-Node spike of amplitude 6,000. Its wall is about 2,000 light quanta of hopping, so it is never born: 72 births kept by the refusal, all refused at the take. The head's lay is right: one e at the quarter turn, about one light quantum of energy for every family (1.010 measured). [measured]
3. **A slip in my merge.** a9ab14c64's message names 9a5469453. The head it merged was 900fc2f4a; the records are SAME on both, so the measurements stand.

## 7. Limits, by name

1. **The precession dephases** in a packet with a spread of frequencies. The second-order clock's rate is kappa Phi / omega per mode, so one mode or a slow packet precesses clean. A packet of width 2 or 3 settled at S_z near 0.6 with the field's orbital coupling, and near 0.2 without it. [measured; derived]
2. **The field's orbital pull on the charge** drags both planes alike and swamps the spin's force at the struck row's Stern-Gerlach parameters. The click rate follows the local beat, so the clicks' centroid is no place reading (section 2, item 5). [measured]
3. **The click's beat is a phase reading:** it reads the re line's zero crossings. Under the half-turn's lift, a quarter turn of each hand, the clicks move by a quarter beat. A beat read free of the phase is the owner's word. [read; derived]
4. **A split quantum never clicks.** A quantum split between the planes or between places never stands at a whole quantum in one plane. [read]
5. **The controls** (the held field or curl, the orbital coupling off) are no acts of the engine. [read]
6. **The 48 on the doublet's lines** is not built in the kit. The coupling's covariance under the half-turns is checked by the algebra (DAVID-SPIN-DOUBLET.md section 1). [checked]
7. **The seed has no exclusion:** it lays piles. [read]

## 8. For the Boss

1. **The build.** Apply DAVID-SPIN-SOLVED_DIFF.txt on the toy behind one flag (re-cut to the clock names first, mine on your word):
   - without G0;
   - the switches moved to the test harness;
   - the four index literals spelt from PLANE.
2. **The gates:** the scripts in the checks file, then the Reader's gates:
   - 41 and 42 read a row of two planes with a gap;
   - 43 per plane by the charge;
   - a new gate for the boundary's clicks at 2 pi against 4 pi.
3. **The owner's word, by name:**
   1. the count of planes as the exchange (B);
   2. the merger across the two planes;
   3. SR-S3 on two planes;
   4. the seed's exclusion per plane (the bodies' piles);
   5. the beat read free of the phase;
   6. the split quantum's click;
   7. the 48 on the lines up to the phase.

A document, its diff and its checks; no code of the engine head changed.
