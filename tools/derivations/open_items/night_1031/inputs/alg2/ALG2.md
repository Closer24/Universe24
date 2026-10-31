# ALG2: ALG1 corrected: the fourth click as a law of the build, the books in the rulings' terms (node-all 9d75a4904)

ALG2, for the Boss, 2026-10-31, 08:4x to 09:1x UTC. S is
S.

**What this text is.** It replaces only the lines of ALG1 it names, and every other line of ALG1 stands as written.
- ALG1 is S/alg1_frozen/ALG1.md: 634 lines, sha256 e9deeed71dbeaf0169c226aad95c9d8c76eb26b0618f0785e3b3dbb761a56d50.
- Line numbers below are that file's.
- Section 0 lists every replacement. Each section after it gives the text that replaces those lines, and the
  measurements behind it.

**What was read.**
- Both readers' reports: S/alg1_math/REPORT.md and S/alg1_phys/REPORT.md.
- The Boss's rulings of 07:5x (second part), 08:1x, 08:3x and 08:4x in S/BRIEF_PAIRS.md.
- VARY4.md section 2, for its D_i and G. MIN2.md section 3.4, for its counting rule.
- node-all 9d75a4904 and node-fold's head, 86201c4d8, extracted by git archive into S/alg2/all and S/alg2/fold.

**The head.** `git diff 4ce1aa9d7 9d75a4904` over src/tensor24/engine, runner and algebra is empty. So the act ALG1
measured is the act ALG2 measures: only the decoder and the record's schema moved. Every run below was redone on
9d75a4904.

**Conduct.**
- Nothing in /home/user/Universe24 or in any worktree was edited, committed or pushed. I wrote only in S/alg2/.
- Probes are in S/alg2/probes and their outputs in S/alg2/out:
  - cochain2.py: ALG1's cochain.py, extended with the place identity, MIN2's counting rule and the kinetic mode;
  - hodge2.py: new;
  - unitlay.py, twinD.py and twinD_back.py: ALG1's.
- Whole numbers only, with Rule3's carry the one division (Euclid's gcd in hodge2.py runs by it too).
- python3 -I (Python 3.13.17, numpy 2.5.3), the extracted tree's src first on sys.path, one process at a time under
  nice 19.
- The load was read before each run; it ranged from 4.7 to 7.98 and never reached 8.

Every claim is marked DERIVED, MEASURED or OPEN. MEASURED is said only of what a probe here moved.

## 0. What ALG2 replaces

| ALG1 lines | what they held | replaced by |
|---|---|---|
| 25-66 | the answer to the owner | section 1 |
| 75, 76, 78-82, 84 | standings rows: work, (c), the books, the 3-cell | section 8 |
| 102-105, 415, 422, 427, 502 | "meeting" for a cell | 6.6: a cell is an edge |
| 109-110, 282, 297 | the place | section 4 |
| 132-135, 157-158, 165-166, 219, 235, 259-260, 273, 284-285, 365, 389, 394-395, 407, 422 | the letters K and B | 6.2 |
| 138 | "on a coupling's own cell: its stored energy" | 3.3 |
| 196-206 | the strength-0 cells as the ruling's (c) | 6.3 |
| 271-275 | the odd dial | 6.5 |
| 281-287 | what closes by construction | 3.1 |
| 289-309 | the reading that can fail | 3.2 |
| 320-334 | the two-leg books | 3.3 and 3.4 |
| 336-356 | the degree theorem's scope | section 5 |
| 365-378 | the tie's table | 3.2 and 3.6 (the numbers kept, the frame changed) |
| 380-411 | the tie's own cell | 2.5 and 3.5 |
| 415-445 | 4.1 and 4.2: three clicks, the generations | section 2 |
| 483-485, 494-497 | the 3-cell, and a coupling of four trains | 2.4 |
| 517 | "the books: d d = 0" | 6.1 |
| 554-567 | the products | 7.5 |
| 569-571, 577-589, 593-618, 620-634 | 5.3, OPEN, the lists, the files | sections 7, 9, 10 and 11 |

ALG1's other lines stand, and none of their measurements is withdrawn. The cone's numbers (ALG1 3.5) stay as
measurements of a reading; the cone itself is withdrawn as a record item (2.5).

## 1. The answer to the owner (replaces 25-66)

The algebra that orders the world of clocks is the clocks' coupling complex, with whole-number cochains on it, augmented
by the place: Z^F --C--> Z^E --B--> Z^V --eps--> Z. Both readers call it the right algebra for the books.

**Its cells.**
- A clock (a train at a Node-clock) is a 0-cell.
- An edge (two clocks a coupling joins, at one Node-clock or across one Mesh) is a 1-cell.
- A triangle (three clocks of one Node-clock, pairwise joined) is a 2-cell.
- An edge or a triangle is the place's structure. A meeting is read from what passes (the 07:5x ruling).

**Its teeth.**
- A tooth is a cochain: one whole number per oriented cell, born at the middle, which is the cell's zero.
- Read from the other end it is its negation, which in the engine's digits is D - 1 - k.
- A passing is a 1-chain, and a clock's line is its boundary.
- MIN1's doubles cannot be written in this algebra. node-all's runs come back from it byte for byte on all five shipped
  worlds and on the two variants. On node-fold's head they come back byte for byte on the click and mesh worlds
  (section 7).

**Its two laws of d d = 0.** eps B = 0 and B C = 0, and only these two (6.1).
- eps B = 0 is each connected part's books.
- B C = 0 is why the third click is never seen in a line.

**The clicks: three, and no fourth, by a law of the build** (section 2).
- Teeth sit only on edges between two clocks and on triangles of three clocks at one place.
- Under that law the record holds two kinds of quanta, the edges' and the triangles', with the split as the map between
  them.
- Nothing above dimension 2 could be shown in any case (C d_3 = 0).
- The cycles no laid triangle fills keep their quanta as first clicks, edge by edge.

**The books** (section 3).
- The residual is the act's own, stated at the place as the sum of D_i over each monomial.
- No edge or triangle can carry it: that is a theorem.
- A two-leg coupling's stored form is the pair's, read off the counts, and its closure is a check by construction.
- The four-leg tie's residual has no stored form of its own in free window counts. Only a step that makes the
  quartic's work an exact difference removes it, and after that step the reading that can fail is the energy's bound,
  a board fact.
- Measured on today's act, the clocks' kinetic term cannot separate the teeth's term from the tie's residual. The two
  parts are each larger than the residual and cancel to it (3.6).

## 2. The fourth click: off the table as a law of the build (replaces 49-53, 84, 406-407, 415-445, 483-485, 494-497)

### 2.1 The law (the 08:4x ruling, and the ruling for ALG2)

1. Teeth sit only on edges between two clocks, and on triangles of three clocks at one Node-clock.
2. No tooth sits on any cell joined to something that is not a clock.
3. No tooth sits on a cycle that no laid triangle fills (an H_1 cycle). Its quanta are carried edge by edge as first
   clicks, as today's act carries them.
4. The potential's forms join at most two trains.
5. The record has two levels: lines on clocks, and sides on edges.

### 2.2 What is DERIVED under it

- **Three kinds of click, no fourth, for every lay the files allow.** By 1 to 3, a tooth lives on an edge or on a
  triangle and nowhere else. By 5, an edge's wraps are written in its two sides and its two clocks' lines (the first
  click), and a triangle's wraps are written as +w, +w, -w on its three edges' sides, never in a line (the third click,
  B C = 0). The split is the map C between them: it holds no tooth and writes no quantum of its own. So the record holds
  two kinds of quanta and three clicks, and there is no other tooth to make a fourth.
- **That every lay is covered:** by 4, a plan joins at most two trains in any one form. The physicist checked the forms
  in plans.py one by one: notch and spring on one train; the tie on one tied train's two rows with the held hand; the
  hands' tie on two tied trains; the gradient vertex on two trains across a Mesh. No file declares a coupling (load.py,
  line 184).
- **What the algebra itself gives, without the law:** nothing above dimension 2 can be shown, since a 3-cell's quanta
  reach the sides through C d_3 = 0. Everything else in "no fourth" is the law's, not the algebra's alone (the 08:4x
  ruling).

### 2.3 The H_1 family, with its conditions and its numbers (OPEN 7 of ALG1, moved here)

**Why it is a family.** A record of lines and sides can show any 1-chain. Over the rationals C_1 is the sum of three
parts:
- im B^T, seen in lines;
- im C, the laid triangles' circulations, the third click;
- H_1 = ker B / im C, the 1-cycles that no laid triangle bounds (the mathematician's item 3).

A form that turned a tooth on an H_1 cycle would write a whole circulation on the cycle's sides in one round, with no
line moving. Rule 3 of the law keeps such a tooth off the table.

**Where H_1 cycles arise** (the conditions):
- (a) chordless rings of four clocks or more, at one place or across Meshes;
- (b) three clocks pairwise joined across one Mesh: two clocks of one Node-clock joined by an own edge, each joined by
  a Mesh edge to one clock at a neighbour. X_2 does not hold these, since they do not lie at one Node-clock;
- (c) loops round the board.

**MEASURED** (probes/hodge2.py, on the complex laid from the structure; rank C by exact row reduction):

| complex | clocks, edges, triangles | parts | rank B | H_1 | H_2 | triangles across one Mesh |
|---|---|---|---|---|---|---|
| the click board, its 12 Mesh cells per Node-clock laid (idle at mesh 0) | 135, 405, 27 | 28 (the 108 coupled clocks one part; 27 metric clocks alone) | 107 | 271 | 0 | 162; once filled, H_1 109 and H_2 0 |
| the mesh ring (live) | 540, 540, 0 | 2 (the ring's two strands) | 538 | 2 | 0 | 0 |
| each Node-clock's own part, on every shipped world | at most 5, 3, 1 | - | - | 0 | 0 | - |
| bang, live and well | no edge | every clock alone | 0 | 0 | 0 | 0 |

- The readers' hodge8 gave 271 and 2. These are measured again here, by another probe.
- On the click board, the 162 cross-Mesh triangles are 27 Node-clocks x 3 + Spokes x 2 kinds: the wave here with the
  giver and taker there, and the giver and taker here with the wave there. Their boundaries are independent (rank 189
  with the 27 laid triangles).
- The 109 left once they are filled are rings of four or more clocks across Meshes, and loops round the board; they are
  not separated further here. One such ring, by hand: (x, wave), (x + e1, giver), (x + e1 + e2, wave), (x + e2, giver).
  It is chordless, since no edge joins two waves or two givers.
- On the shipped click world all of these sit on Mesh cells that mesh 0 leaves idle, so no shipped world moves a
  quantum on an H_1 cycle. On the mesh ring the two strands do carry, as first clicks, edge by edge.
- For a tooth on such a cycle, the dial would decide its lawfulness (the mathematician): a 4-ring has G = 4, so its dial
  4D is even and is refused; a cross-Mesh triangle has G = 3 and an odd dial, and its member would read one Mesh away,
  which locality allows. That case is the owner's question (2.6).

### 2.4 A 3-cell, and four pairwise-joined clocks (replaces 483-485 and 494-497)

- **"A 3-cell holds no tooth" is MIN1's minimality rule, not a consequence of invisibility** (the mathematician's MINOR
  6; the physicist's OVERCLAIMED). A 3-cell tooth's own quanta would be invisible, since C d_3 = 0. But a tooth turned
  with the triangles' pairs could steer their landings, so invisibility alone does not exclude it. The law (rule 1)
  excludes it, and so does MIN1's rule.
- **Its boundary is THIRD7's kept direction.** k = (-1, 1, -1, 1) is Z_2 = ker C for four clocks pairwise joined. The
  triangles' pairs there belong on C_2 / Z_2, so that direction is a double by MIN1's rule (ALG1 4.4's DERIVED lines
  stand).
- **Such a place reads its third click NOT READ by name**, beyond the scope C^T C = 3 I (the 08:4x ruling). The
  physicist laid one in a test world (taker2, no strength touched): the cochain act there stays byte for byte, and the
  four triangles' landings read from the sides only up to k.
- **No plan can lay a coupling of four distinct trains**, not merely "no shipped plan lays one" (rule 4, and the
  physicist's check of plans.py). If one were laid, its four-leg weight would make the edge dial even, which KEY3's
  ruling has the load refuse by name.

### 2.5 The tie's own cell is withdrawn as a record item (replaces 380-411 as a proposal; the numbers stay)

- ALG1 3.5's cone would put teeth on edges from a clock to a cell that is not a clock. Each wrap there would be a
  quantum given by one clock and taken by no clock: a fourth kind of event.
- On L0 that reads -18 quanta at every place over 200 rounds, with no clock as partner (the physicist, from ALG1's own
  run).
- Rule 2 of the law excludes it, so it is withdrawn as a record item and no longer offered to the owner's batch.
- Its measured numbers (each clock's quanta, and its run back) stay as a reading of the board, not as a record element.
- "Booked" means only removed, by an exact step (then a check by construction), or read by name. It never means put
  into a store (the 08:4x ruling).

### 2.6 To the owner's batch

Are three clocks pairwise joined across one Mesh a triangle, with a third click there? Or are they an H_1 cycle,
carried as first clicks as today?
- On the click board there are 162 of them, laid by the structure and idle at mesh 0.
- C^T C = 3 there, so the dial 3D would be odd.
- The member would read one Mesh away, which locality allows.
- Nothing is built until the owner rules.

### 2.7 The table of 4.1, corrected (replaces 417-435)

| dimension | cell | holds | its quanta seen in | the click |
|---|---|---|---|---|
| 0 | a clock (a train at a Node-clock) | its gears: the board | its line, B q | none |
| 1 | an edge (two clocks a coupling joins) | one tooth in Z/D | lines and sides | the first click |
| between 2 and 1 | the map C (the Hodge split 3 x = (3 x - C C^T x) + C C^T x) | none | none | the split click |
| 2 | a triangle of one Node-clock | (tau, eta) | sides alone, since B C = 0 | the third click |
| H_1 cycles | no cell | no tooth (rule 3) | their quanta are first clicks, edge by edge | none of their own |
| 3 | a tetrahedron | no tooth (rule 1; MIN1's rule) | nowhere, since C d_3 = 0 | none |

- An edge's stored form, its coupling's energy, is read off its two clocks' counts. It is the edge's and holds no tooth
  (3.3).
- An event is one wrap of a tooth: one quantum given at one end of an edge and taken at the other. The record holds two
  kinds of quanta, the edges' and the triangles'.

## 3. The books, in the 08:3x and 08:4x rulings' terms (replaces 55-61, 281-334, 365-378, 401-411)

### 3.1 The checks by construction, named so (replaces 281-287)

| check | what it is | d d = 0? |
|---|---|---|
| each edge: q at one end, -q at the other | the orientation | no |
| each connected part: SUM of its clocks' lines = 0 | eps B = 0, the part's conservation | yes |
| each clock's line unmoved by the third click | B C = 0 | yes |
| D x (a clock's booked total) - (its swept passing) = B (c_0 - c_N), within the clock's degree times h | David's identity: the carry's telescoping | no |
| a two-leg coupling's work = - the change of its staggered energy | 3.3 | no |

None of these can fail on the act; each reads the record's faithfulness to it.
- MEASURED: David's identity reads 150,089,166 on L0, against 2h = 152,434,286.
- The books against the board's work are board checks beside a click reading, by the 07:5x ruling (the physicist's
  M5). That holds for every reading in sections 3.2 to 3.6.

### 3.2 The residual is the act's own, stated at the place (replaces 289-309)

**The residual** (VARY4 2.2). For every term i, T_i(x; y) = J_i(y) x_target, and
    D_i = [T_i(a+; a) - T_i(a; a+)] + [T_i(a; b) - T_i(b; a)],   2 W_i = 2 G_i(n) - 2 G_i(n - 1) + D_i.
The residual at the place is SUM_i D_i over each monomial's terms. It is not stated as a clock's share: the split by
legs, l_t / L, is David's convention, and only the place's total is the act's (the 08:4x ruling). ALG1's lines
308-309 are withdrawn as a statement of the act.

**MEASURED** (cochain2.py kinetic mode, from VARY4's definition, on the cochain act, 200 rounds). The place's SUM D,
in kappa 1 units:
- L0: 708,840,000 at its largest, round 150 (every Node-clock alike);
- L1: 10,023,720,000 at site 17, round 170.

These are VARY4's numbers to the unit. On every two-leg and one-clock monomial SUM D = 0, at every place and round.

**The theorem stands, restated at the place (DERIVED; ALG1's proof).** No 1-chain and no 2-chain books eps(omega),
because eps B = 0 and B C = 0. It is read per connected part (section 4). It holds for every edge form, every split
and every turn on edges or triangles.

**The tie's numbers that stay** (ALG1's table, 369 to 373, MEASURED there): own minus swept at a clock reaches 82 edge
keys on L1 and 19 on L0. Under the 08:1x ruling that is not a reading of the residual: it books stored energy as
unbooked work.

### 3.3 The stored form is the pair's, read off the counts (replaces 138 and 320-327)

- **For two legs, f x y:** R = -(E(after) - E(before)), with E(a, b) = f (x_a y_b + x_b y_a) (DERIVED). A squared leg
  gives E = 2 f x_a x_b. E is the pair's, the edge's, read off the two clocks' counts. It sits in no tooth and no store,
  and it is no new element.
- **The two-leg closure is a check by construction, named so** (the physicist's B2), not a reading that can fail.
  MEASURED as a check: kappa 1 SUM R + the change of E = 0 at every place and round. That covers the held spring (one
  clock) on L0 and L1, and the hands' tie (two clocks) on L0; on L1 the hands' tie does not work.
- **For the tie,** the reference is VARY4's potential-normalized G' = (2/k) G = -E', where
  E' = (f/4) [SUM_i a_i PROD_(j != i) b_j + SUM_i b_i PROD_(j != i) a_j], so E'(a, a) = 2 V(a) (the 08:3x ruling). No
  stored form of the tie's own holds its work (section 5).

### 3.4 The record's legibility of the coupling's energy at the key's grain (replaces 329-334)

The old per-clock "stored share within the teeth" is renamed (the 08:3x ruling): the record's legibility of the
coupling's energy at the key's grain. It is no gate for turns, and it goes to the owner with the key.

**MEASURED** (L0, 200 rounds):
- The pair's (the hands' tie's) stored energy at a place moves by up to 443,520,000 in kappa 1 units. That is
  2,661,120,000, or 17 edge keys, in the act's units (kappa 6), at site 26, round 156; every Node-clock is alike.
- Shared half and half, as David's convention does, a clock's half is about 8.7 edge keys, against the 2h = 152,434,286
  (under one key) that its two teeth hold. This is the physicist's NOT SHOWN, now under its new name.

### 3.5 After an exact step (replaces 409-411)

- An exact step makes the quartic's work an exact difference. Then SUM D = 0 identically, a check by construction.
- The reading that can fail is then the energy's bound, a board fact (STOP1's).
- No record-side form and no extra slot of today's step does this (section 5).
- Claims that the shares pass the teeth are cited only from a confined world with the tie on: L0 and L1, 200 rounds.
  Hold 0 is the open direction's world, STOP1's (the 08:4x ruling).
- On L1 the residual's share passes the teeth at 27 of 54 clocks within 200 rounds (VARY4's mathematician, cited):
  OPEN.

### 3.6 The kinetic term, tried (the mathematician's question 2; the ruling's item 6)

**The identity (DERIVED from step.gear; MEASURED as a check).** On every row, at constant teeth W:

    4 push (a+ - b) = 4 W (v+^2 - v^2) + (r+ - r)(a+ - b),   v = a - b, v+ = a+ - a, r the edge tooth.

Summed over a place's rows, the push's work is the Mesh pull's work Fw (the board's wave) plus every coupling's R.
With the two-leg identity and the tie's reference E' this gives, exactly at every place and round:

    Res' := SUM R_tie + (E'_tie now - E'_tie at the start) = dH' + Teeth - Fw,

where:
- dH' is the change of the place's whole two-slot energy: SUM W v^2 plus E of every two-leg and one-clock coupling,
  plus E'_tie;
- Teeth is SUM (r+ - r)(a+ - b) / 4, the teeth's term;
- Fw is the board's wave's work at the place.

Over the board, Fw closes into the Mesh pull's staggered energy, SUM over the Meshes of grip u(a) u(b).

The momentum form is a second kinetic term, with p = 4 W v + r and p+ = p + 4 push:

    16 W push (a+ - b) = (p+^2 - p^2) - 4 push (r + r+).

**Checks** (cochain2.py kinetic mode, 200 rounds on L0 and on L1). Every one is 0 off:
- W is the rest, 600,000,000, on every row, place and round;
- the grips never move;
- the identity holds per row;
- the kicks' work equals the J terms' work;
- Res' = dH' + Teeth - Fw at every place and round;
- the board's SUM Fw equals minus the change of the Mesh energy;
- p+ = p + 4 push, and the momentum form's identity, per row.

**What it reads (MEASURED).** In kappa 1 units, with D = 152,434,287 one edge key:

| reading | L0, a place (every Node-clock alike, Fw = 0) | L1, a place | L1, the whole board |
|---|---|---|---|
| Res' at its largest | 546,330,000: 3.6 keys (round 151) | 1,647,240,000: 10.8 keys (site 17, round 163) | 4,788,510,000: 31.4 keys (round 200) |
| dH', counts' form | 1,990,370,000: 13.1 keys (round 151) | 65,156,770,000: 427 keys (site 10, round 190) | 307,683,030,000: 2,018 keys, with the Mesh energy (round 200) |
| the teeth's term | -1,444,040,000: -9.5 keys (round 151) | -27,035,400,000: -177 keys (site 7, round 200) | -302,894,520,000: -1,987 keys (round 200) |
| the board's wave at the place, Fw | 0 | 44,600,000,000: 292.6 keys (site 10, round 190) | closes into the Mesh energy |
| momentum form: dH'_p, and its remainder | 6.3 keys and -6.2 keys (round 148) | 404 and -173 keys | 1,977 and -1,946 keys (round 200) |
| at round 200, site 0: Res', dH', teeth | -1.9, +1.2 and -3.1 keys | - | - |

**Findings.**
- **The split is exact, but it does not isolate a small "tie's own residual".** On every lay the teeth's term is as
  large as the energy change and of the opposite sign, and the residual is their small difference. On L0 at round 151,
  13.1 - 9.5 = 3.6 keys. On L1's board at round 200, 2,018 - 1,987 = 31 keys.
- **Why (DERIVED).** W (v+^2 - v^2) = W (v+ - v)(v+ + v) is a whole multiple of W = 600,000,000, which is 3.9 edge keys.
  So the counts' kinetic term reads a place's energy only at the grain W, coarser than the residual it would separate.
  The teeth's term carries the rest.
- **The momentum form does no better.** Its remainder, 4 push (r + r+), is as large as its energy change: -6.2 against
  6.3 keys on L0, and -1,946 against 1,977 on L1's board.
- **So, on today's act, the kinetic term cannot separate the teeth's term from the tie's residual at the key's grain
  (MEASURED, both forms).** The residual stays as the 08:3x ruling reads it, against G', and stays OPEN.

## 4. The place (replaces 109-110, 282 and 297)

- **The place, X_-1,** is a connected part of the laid complex, by structure (DERIVED).
- **MEASURED** (hodge2.py):
  - with its 12 Mesh cells per Node-clock laid (the 97, lawful by the 08:1x ruling), the click world's 108 coupled
    clocks are one part over the whole board (rank B = 107), and its 27 metric clocks stand alone;
  - the mesh ring is two parts, its two strands.
- **The per-site reading.** Reading each Node-clock's held, giver and taker as a place holds only because mesh = 0
  makes the Mesh passings vanish. That is a strength's value, and it is named so.
- **The per-site identity** is the site star's coboundary: a site's sum of lines is its across net, the Mesh cells held
  there less those held one Mesh away whose far end is there.
  - MEASURED (compare mode, every world, every round): 0 site-rounds off, and own sides not cancelling at 0.
  - The across net is not 0 at 7,371 site-rounds of the mesh world (125 rounds) and at 1,526 of its key-7 variant (60).
    It is 0 on the click world, at mesh 0.
- **Causality is per clock** (the 07:5x ruling), so X_-1 is no causal unit. The part's conservation, eps B = 0, is a
  check, not a law of causes.

## 5. The degree theorem, narrowed (replaces 63-66, 80 and 338-356)

**What it excludes.** A step-free energy of the coupling itself, in free window counts. In ALG1's statement, read
"telescopes through a polynomial of a finite window of free counts". The proof (ALG1 341-347) stands for that case, and
both readers re-derived it. The 08:3x ruling has the same for three legs or more (VARY4's mathematician).

**What it does not exclude: the board's trajectories.**
- Along a trajectory the step binds the window.
- There the identity of 3.6 makes the tie's work exactly a two-slot difference of the rest of the board's energy, plus
  the teeth's term, less the wave's inflow (MEASURED, 0 off).
- So "no polynomial of any number of slots can hold the tie's work" (ALG1 63) is withdrawn. Whether a function of the
  board's state can hold it along trajectories is Theorem A's case: drafted, unread, and nothing here leans on it
  (the 08:1x ruling).

## 6. The rest

### 6.1 d d = 0 (replaces 45-47 and 517)

Only eps B = 0 and B C = 0 are d d = 0. The orientation (each edge's q and -q), David's identity (the carry's
telescoping) and the two-leg closure are checks by construction of other kinds (3.1).

### 6.2 The letters (replaces the uses of K and B in 132-135, 157-158, 165-166, 219, 235, 259-260, 273, 284-285, 365, 389, 394-395, 407 and 422)

- **D** is the edge dial: 152,434,287 on the click world, ALG1's K. It is odd.
- **h = (D - 1) div 2** is its middle, the birth, ALG1's B where B meant the middle. PICTURE.md's L5 uses the same h.
- **B** stays d_1, the incidence of edges on clocks.
- **The key** is KEY3's: key = 2 x middle + 1, with D = 3 x key.
- The triangles' matrix is written C^T C, never K.
- So ALG1's 157 reads n + c = q D + c', carry(n, D, c + h), c' = r' - h, and carry(n, D, k).
- ALG1's 273 reads "the key = 2 middle + 1 is odd by its form, and so are D = 3 x key and 3D = 9 x key".
- ALG1's 284-285 read "D x (booked) - (swept) = B (c_0 - c_N), within the clock's degree times h; 150,089,166 against
  2h = 152,434,286".
- ALG1's 395 reads "(degree + 1) h = 228,651,429".

### 6.3 The strength-0 cells (replaces 196-206)

The 08:1x ruling made MIN1's case (c) unlawful: a chosen 0 enters only as a factor, and multiplies its terms to exact
zeros. So these are structure, laid at their factor 0, and the click world's lawful state is 97 per Node-clock:
- the 12 Mesh cells (24 sides) per Node-clock;
- the notch's 7 couplings;
- term 5's 178 terms.

On those cells the cochain act does about 650 of its 2,849 products (MIN2's rule, 7.5) (MEASURED: the term counts).

### 6.4 node-fold (the mathematician's MINOR 5)

- The structural edging move has not landed on node-fold's head: plans.py:75 still reads lit(factor), at 86201c4d8.
- MEASURED on that head: the compare is byte for byte on the click world (100 rounds) and the mesh world (125), with
  the run back exact. The only change to the click world's files there is the square train's name, "square".
- When the move lands, the click world's end line gains the 24 Mesh sides at their birth. The cochain read-back already
  writes every idle Mesh cell's two sides at the birth, so the end line should stay equal (DERIVED).
- The rerun is OWED when the move lands.

### 6.5 The odd dial (replaces 271-275)

- The odd dial is needed by the balanced cochain form, where a reversal is a negation only on an odd dial, and by
  KEY3's ruling. It is not needed by the act.
- The physicist measured this (evendial.txt): on the dials 2, 4, 8 and 24, and on 3, 9 and 15, over every tooth and
  every passing in [-3D, 3D], the side pair closes and the run back is exact in the engine's digits.
- A dial that comes out even is refused by name at the load (KEY3), or its weights are read anew (OPEN).

### 6.6 A cell is an edge, not a meeting (replaces 32, 102-105, 415, 422, 427 and 502)

- Read "the edges, X_1" for ALG1's "the meetings, X_1", and "a click names an edge, never a kind" in 502.
- A meeting is read from what passes: one give and one take of a quantum on a side (the 07:5x ruling).

### 6.7 The two missing worlds (the mathematician's MINOR 7)

They are now in S/alg2/worlds/, each a byte-for-byte copy of its source:
- vary3_L1: VARY3's world/ (universe 2a2aa411e193a88a..., piece 85c72a56b6fcc85c..., setting 3f2d426e44c532f0...);
- mesh_key7: MIN1's variant, the mesh world with file key 7 (universe 2376dd6c90bae54c...; piece and setting byte
  for byte the shipped mesh world's).

## 7. MEASURED on node-all 9d75a4904 (ALG2's runs)

### 7.1 Byte for byte, with the place identity (compare mode)

Each run is compared round by round:
- a, b, r, rd, every tooth read back, every click, and the record's click lines;
- at the end, the end line's teeth and the digest of the state read back;
- then the run back from the cochain end alone, with nothing saved;
- and at every site and round, the place identity of section 4.

| world (rounds) | entries off: a, b, r, rd, k, clicks, lines | click entries not 0 | click lines | end teeth, digest | run back | place identity off; sites with across net != 0 |
|---|---|---|---|---|---|---|
| bang (10) | 0 each | 0 | 0 | equal, equal | exact | 0; 0 |
| click (100) | 0 each | 4,050 | 5,508 | equal, equal | exact | 0; 0 |
| click (300) | 0 each | 22,950 | 19,521 | equal, equal | exact | 0; 0 |
| live (20) | 0 each | 0 | 0 | equal, equal | exact | 0; 0 |
| mesh (125) | 0 each | 36,192 | 21,589 | equal, equal | exact | 0; 7,371 |
| well (10) | 0 each | 0 | 0 | equal, equal | exact | 0; 0 |
| mesh at file key 7 (60) | 0 each | 6,824 | 4,204 | equal, equal | exact | 0; 1,526 |
| VARY3's L1 (200), new | 0 each | 6,328 | 9,492 | equal, equal | exact | 0; 0 |

- Apart from the two new lines, every output is line for line ALG1's on 4ce1aa9d7; for key 7, only the world folder's
  name differs.
- On node-fold's head, 86201c4d8: the click world (100) and the mesh world (125) give the same rows (6.4).

### 7.2 The 24, again (turn mode)

On the mesh world at file key 7, 60 rounds, the Mesh teeth off their birth in 2,366 cell-rounds. For the turns
diag(-1, -1, 1) and diag(-1, 1, -1), each part of the test is 0 rounds off:
- the engine's act(g s) against g act(s);
- the cellular map with its sign against the engine's turn read back;
- act(g c) against g act(c) on the complex.

### 7.3 The homology

As in 2.3 (probes/hodge2.py, out/hodge_*.txt).

### 7.4 The books and the kinetic term

As in 3.2 to 3.6 (out/kinetic_click_L0_200.txt and out/kinetic_vary3_L1_200.txt).

### 7.5 State and work per Node-clock per round (replaces 554-567)

**The counting rule.** It is MIN2's (MIN2 3.4), on 9d75a4904:
- 3 per term of J, the Mesh plan and the push;
- 4 + T per passing term in node-all; 4 + its edges per edge term on the complex;
- 5 per clock-read term;
- 1 per grips'-read term;
- 3 per crossing entry (node-all's at both ends, the complex's at the + end);
- 45 R for the board's per-row work.

| world | state, node-all -> cochain | products, node-all (MIN2's rule) -> cochain |
|---|---|---|
| bang, live | 76 -> 40 | 23,928 -> 889 |
| click | 279 -> 97 | 144,884 -> 2,849 |
| mesh | 103 -> 33 | 19,248 -> 888 |
| well | 115 -> 43 | 30,221 -> 966 |

**MEASURED.** node-all's four numbers are MIN2's to the unit.

**ALG1's 144,984** (on 4ce1aa9d7, the same act) used another rule. The difference of 100 is:
- +1,300: the clock read counted at 3 per term, not 1;
- -1,170: the per-row work left out;
- -30: the grips' read left out.

**The click world's terms,** structural against laid: J 126 of 9,664; Mesh plan 12 of 4,056; push 178 of 910; clock
25 of 130; passing 108 of 9,664; crossing 12 of 4,056; teeth carries 15 of 175, of which 3 are live.
- The complex counts all 30 grips'-read terms, and MIN2's (a)+(b) counts 6. The complex computes the passing on its 108
  edge terms only, and the crossing at the + end.
- So its 2,849 is below MIN2's form count of 3,455, by exactly 594 + 36 - 24 = 606.

## 8. The standings (replaces ALG1's rows 75, 76, 78-82 and 84)

| claim | standing | section |
|---|---|---|
| state per Node-clock 76 -> 40, 279 -> 97, 103 -> 33, 115 -> 43; products (MIN2's rule) 23,928 -> 889, 144,884 -> 2,849, 19,248 -> 888, 30,221 -> 966 | MEASURED on 9d75a4904 | 7.5 |
| the click world's 12 Mesh cells, notch and term 5 laid at their factor 0: the lawful 97 | the 08:1x ruling; MEASURED | 6.3 |
| three kinds of click, no fourth, for every lay the files allow | DERIVED under the law of the build | 2.1, 2.2 |
| nothing above dimension 2 can be shown | DERIVED (C d_3 = 0) | 2.2 |
| the H_1 family: 271 on the click board (109 once its 162 cross-Mesh triangles are filled), 2 on the mesh ring, 0 at every place | MEASURED | 2.3 |
| a 3-cell holds no tooth | MIN1's rule and the law, not invisibility | 2.4 |
| the tie's own cell as a record item | withdrawn: a fourth kind of event | 2.5 |
| the residual at the place, SUM D, VARY4's to the unit; 0 on every two-leg and one-clock monomial | MEASURED | 3.2 |
| no 1-chain or 2-chain books the place's coupling work | DERIVED, per connected part | 3.2, 4 |
| the two-leg closure | a check by construction (MEASURED as one) | 3.3 |
| the record's legibility of the pair's energy at the key's grain: 17 edge keys at a place on L0 | MEASURED, named so; no gate | 3.4 |
| Res' = dH' + Teeth - Fw, exact; the kinetic term does not isolate the residual at the key's grain | DERIVED; MEASURED (both forms) | 3.6 |
| the degree theorem: no step-free energy of the coupling in free window counts | DERIVED; the trajectory case Theorem A's | 5 |
| the place: a connected part by structure; the per-site reading at mesh 0 only | DERIVED; MEASURED | 4 |

## 9. OPEN (replaces 577-589)

1. The twin on the dial D: measured on toy dials only. The mathematician read it at the file's key in his THIRD8
   reading: 0 landings apart, the run back exact.
2. The hidden pairs on a place of four pairwise-joined clocks: on C_2 / Z_2, with no pick, through im C. Read NOT READ
   until then (2.4).
3. A dial that comes out even: refused by name, or its weights read anew (6.5).
4. The tie's residual: only a step removes it (3.5, 5). After the step the reading is the energy's bound, STOP1's.
5. The metric's push J5, a coupling with no edge (ALG1 361-363).
6. The owner's question on the cross-Mesh triangles (2.6). Separating the 109 cycles left on the click board.
7. The rerun on node-fold when the structural edging lands (6.4).
8. The generations, Koide's 2/3 and the three heights (ALG1 4.2's last item, standing).
9. The dynamics (ALG1 4.6's list, standing).

## 10. DERIVED, MEASURED, and where my measurement overturned my derivation (replaces 593-618)

**DERIVED here:**
- the law of the build's consequence, three clicks and no fourth;
- the three-part sum of C_1 and the H_1 family's conditions;
- the place as a connected part, and the per-site identity as the star's coboundary;
- the books restated at the place;
- the identity Res' = dH' + Teeth - Fw, and the kinetic term's grain W;
- the narrowed degree theorem;
- the letters, the odd dial's need, and the counting difference.

**MEASURED here, on 9d75a4904:**
- the compare on five worlds and two variants (and on node-fold's head), with the place identity;
- the 24 on two turns;
- H_1 and H_2 on every shipped complex;
- VARY4's SUM D to the unit;
- the two-leg check;
- the legibility numbers;
- the kinetic split and its checks;
- MIN2's counts.

**Where my measurement overturned my derivation:**
1. I expected the clocks' kinetic term to show the tie's residual as a small energy defect, with a smaller teeth's
   term beside it. It shows the teeth's term as large as the energy change and of opposite sign, in both kinetic forms;
   the residual is their small difference. I then derived why: the counts' kinetic term moves in whole multiples of W,
   3.9 edge keys.
2. I expected node-fold's head to carry the structural edging. It does not yet (plans.py:75).

ALG1's three overturned items (612-618) stand, with the third read under 3.4's name.

## 11. Files (all under S/alg2/; ALG1's stay in S/alg1_frozen/)

- ALG2.md: this text.
- probes/cochain2.py: the compare, kinetic, turn and books modes.
- probes/hodge2.py: the homology.
- probes/unitlay.py, twinD.py and twinD_back.py: ALG1's.
- out/:
  - compare_*.txt for the five worlds, mesh_key7, vary3_L1 and click at 100 and 300 rounds;
  - fold_compare_*.txt;
  - kinetic_click_L0_200.txt and kinetic_vary3_L1_200.txt;
  - hodge_*.txt;
  - turn_mesh_key7_60.txt.
- worlds/vary3_L1/ and worlds/mesh_key7/: the two missing worlds.
- unit/ and unitfold/: the unit-strength lays the structure is read from.
- all/: node-all 9d75a4904's src and examples. fold/: node-fold 86201c4d8's.
