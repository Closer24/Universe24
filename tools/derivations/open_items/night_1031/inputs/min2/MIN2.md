# MIN2: the Node-clock's minimality, one standing by cause (node-all 9d75a4904)

MIN2 answers the two hostile readers of MIN1:
- the mathematician, S/min1_math/REPORT.md;
- the physicist, S/min1_phys/REPORT.md.

It follows the Boss's rulings of 07:5x UTC, the last section of S/BRIEF_PAIRS.md. MIN1 stays frozen as it is.

The base is node-all 9d75a4904 (origin/node-all), read only.
- I extracted it whole into S/min2/nodeall by git archive. Nothing was checked out, edited, committed or pushed.
- From 48cd7fcf6 (MIN1's base) to 9d75a4904, src/tensor24/engine, runner, algebra and main.py are byte-identical
  (git diff --stat is empty there). Only the decoder (writer E's sides guard) and record/schema.py changed.
- So the act, the plans, the load and the runner are those MIN1 read. Every figure below is re-measured on
  9d75a4904 unless it is marked "MIN1, same act".

The probes are in S/min2/probes.
- cause.py is the split by cause and the three forms.
- mutants.py holds each build item's mutant.
- phase.py is mode 11's two phases.
- probe24_math.py is the mathematician's probe24.py, copied unchanged and rerun here.
- world.py is MIN1's loader.
- Each output sits beside its script (*.txt).

The rules I kept: whole numbers only, Rule3's carry the one division, python -I, nice -n 19, one process at a time,
and /proc/loadavg read before each run (6.1 to 7.3 throughout).

## VERDICT: NOT MINIMAL as laid; minimal in the gears

The gears hold no double, and the run back holds no second set of anything.
- **The gears are minimal.** a, b and r are each laid freely by the files (files.GEAR), so none is fixed by the
  others. r's need is MEASURED (MIN1, same act, the mesh world): dropped, the counts part at round 2. b's need is
  DERIVED (section 7.3).
- **No second set.** untick = mirror . tick . mirror on one layout and one state.

What is not minimal is every dead tooth and every dead term. They now take one standing, the load's existence test of
a coupling, split by cause:
- **(a) The act's form.**
  - The own diagonal teeth, T per Node-clock: P(t, t) = 0 by given - given^T on every layout.
  - Every J term that lands on the unit row, 2 per two-leg monomial: contract drops that row, and the passing reads
    va1 - vb = 1 - 1 = 0 there.
  - Both are dead for every layout, every factor and every state.
- **(b) The world's structure.** A tooth or term is dead by structure when it stays dead with every CHOSEN strength
  but the key set to 1. The loader's own load() is run again to read it. It covers the trains' characters, the 24's
  tables and the board's shape. These are counts from the structure, exact for every state.
- **(c) A chosen 0.** Dead only by a strength the file chose as 0.

**Lawful now** (the Boss, 07:5x):
- (a) and (b);
- D3;
- S1 as "combine like monomials at the load";
- the unit-row terms;
- with the record's digest taken on the state read back, so every record stays byte for byte.

**Waiting:**
- (c) waits on one ruling with edging's lit(factor).
- D1, the edge's pair held as one number, goes to the owner's batch before it is built. Its own-edge half is Big Pic's
  form (circ.py's gs[e]) and lands with his stage. Its Mesh half is node-all's.

The figures (MEASURED, cause.py, on 9d75a4904; the work per Node-clock per round by the count of section 3.4):

| world | state / Node-clock: as laid -> (a)+(b)+D3 -> and (c) -> and D1 | teeth: (a) / (b) / (c) / live | products: all; (a)+(b) | (c) | live work |
|---|---|---|---|---|---|
| click | 279 -> 112 -> 88 -> 85 | 5 / 140 / 24 / 6 | 144,884; 141,573 (977 per mille) | 702 (4 per mille) | 2,609 (18 per mille) |
| mesh | 103 -> 36 -> 36 -> 33 | 3 / 54 / 0 / 6 | 19,248; 18,276 (949 per mille) | 0 | 972 (50 per mille) |
| bang tensor24 | 76 -> 40 -> 40 -> 40 | 2 / 26 / 0 / 0 | 23,928; 23,027 (962 per mille) | 300 (12 per mille) | 601 |
| live | 76 -> 40 -> 40 -> 40 | 2 / 26 / 0 / 0 | 23,928; 23,027 (962 per mille) | 300 (12 per mille) | 601 |
| well | 115 -> 43 -> 43 -> 43 | 3 / 60 / 0 / 0 | 30,221; 29,249 (967 per mille) | 0 | 972 |

Notes on the table:
- "Live work" is the live terms plus the board's per-row work (45 R).
- The click world with (a)+(b) and D1 holds 97 per Node-clock (DERIVED from the counts: its 24 (c) sides and 6 live
  sides held as 12 + 3).

The forms' run against the engine's own act (MEASURED, cause.py) was byte for byte in every round and on every world.
Each form's run back from its own reduced end alone was exact. The details are in section 4.

## 1. What MIN2 changes from MIN1: each reader's item and where it is answered

| item | reader | answered in |
|---|---|---|
| B1: D2 and the pruning, one standing split by cause | both | VERDICT, sections 2, 3, 4, 8 |
| the unit-row terms, structural, proposed | math MINOR 1 | 2 (cause a), 3, 8 item 2 |
| the 24 on the reduced teeth, the train swap | math MINOR 2, phys m1 | 5.2 |
| S1 renamed "combine like monomials at the load" | math MINOR 3, phys m8 | 7.2, 8 item 1 |
| D1's hypothesis: the edge key odd | math MINOR 4 | 5.1 |
| a, b and r each needed; b's line | math MINOR 5 | 7.3 |
| the drop probe measures the state, not the work | math MINOR 6 | 3.4, 7.4 |
| mode 11's phase | math MINOR 7, phys m5 | 6 |
| D1 to the owner | math MINOR 8, phys m2 | 5, 9 |
| the digest, and the runner's memory | math MINOR 9, phys m3 | 7.5 |
| D3 stronger: the dial's range | math MINOR 10 | 7.6 |
| the header's birth and key | phys m3 | 7.5 |
| locality: no act reads another's tooth | phys m4 | 5.3 |
| HAT3 against the headline | phys m6 | 7.7 |
| words: the clock train | phys m7 | 7.8 |

## 2. One standing, three causes (DERIVED; the Boss's ruling of 07:5x)

The existence test of a coupling is one test, whether it is read for a tooth or for a term:
- edging's weight carries lit(factor) x lit(owners^2 - owners);
- across carries scale x apart x the coupling;
- run.joined reads weight != 0, and run.crossed reads across != 0.

D2's dead sides and the dead terms are read by the same test, so they take one standing. The cause splits them.

**Why (a) and (b) are exact for every state.**
- Every factor is a CHOSEN strength times a strength-free part laid from the structure:
  - notching's flag = square x notch;
  - holding's spring x held, and its tie hold x f x entry x tied x held (f = rest div Gamma, at least 6);
  - tying's tie x channel x the flags;
  - meshing's mesh x channel x the flags;
  - pushing's push x square x path;
  - the clocks' read and the grips' read carry no strength.
- So a factor 0 with every strength at 1 is 0 at every strength. The term adds 0 to J in contract (the factor
  multiplies first) and 0 to every passing P (the work carries the factor; the weight reads lit(factor)).
- The act is the same function on every state, so the run back and the 24 cannot move.
- A tooth whose side no monomial and no Mesh edge joins at the unit strengths carries P = 0 as a polynomial in the
  state, so it stays at its birth.
- MEASURED: as-laid live sides are a subset of strength-1 live sides on every world (cause.py asserts own0 <= own1
  and e0 <= e1).

**What (c) is.** A side or term live at the unit strengths and dead as laid is dead only because the file chose 0.
Whether the load may drop it is the same question as edging's lit(factor), whose kappa (the edge key's factor) a
chosen 0 also decides. It waits on that one ruling, after the ninth code reader weighs the 14 INDICATOR notes.

**Where each class stands on the shipped worlds:**
- **(a), per Node-clock:**
  - the own diagonal, T teeth;
  - the J terms on the unit row: 352 of 1,952 (bang, live), 1,504 of 9,664 (click), 280 of 1,440 (mesh), 424 of 2,252
    (well).
- **(b):**
  - the own pairs no monomial joins;
  - the Mesh reaches with no edge, including the Mesh diagonal (s, t, t);
  - every plan term whose strength-free part is 0.
  - The Mesh diagonal is (b), not (a): it is a real edge between two clocks of one train. It is dead on the shipped
    worlds only because no shipped train is both a gripped trivial row of the board's wave and tied (plans.meshing's
    train conditions).
  - DERIVED, not measured: a train of A1, A2, T1 and T2 at part 1 would be both. It has an A1 row for L and a T1 row
    for M's channel (T1 with T1 onto A1), and its character is kept under the twist, so it is tied.
- **(c), MEASURED:**
  - the click world: 24 Mesh sides per Node-clock (mesh 0), 20 J terms (notch 0), 12 Mesh-plan terms, 178 push terms
    (push 0) and 24 coupling entries;
  - bang and live: 20 J terms (the notch on the square's train) and 80 push terms;
  - mesh and well: none.

## 3. The figures by cause (MEASURED, cause.py; per Node-clock)

### 3.1 The click teeth by cause, and the state

| world | teeth laid (7 T^2) | (a) | (b) | (c) | live | rd rows held (T_d > 1) | state: as laid / (a)+(b)+D3 / and (c) / and D1 |
|---|---|---|---|---|---|---|---|
| bang tensor24 | 28 | 2 | 26 | 0 | 0 | 4 | 76 / 40 / 40 / 40 |
| click | 175 | 5 | 140 | 24 | 6 | 4 | 279 / 112 / 88 / 85 |
| live | 28 | 2 | 26 | 0 | 0 | 4 | 76 / 40 / 40 / 40 |
| mesh | 63 | 3 | 54 | 0 | 6 | 0 | 103 / 36 / 36 / 33 |
| well | 63 | 3 | 60 | 0 | 0 | 4 | 115 / 43 / 43 / 43 |

The state column counts 3 R for a, b and r, the rd rows, and the teeth held.

On click, (b) is 140: 14 own pairs no monomial joins, 96 Mesh off-diagonal reaches and 30 Mesh diagonals. (a) is the 5
own diagonals. That agrees with the mathematician's 164 layout zeros (14 + 120 + 30) less the physicist's 24 chosen-0
sides.

### 3.2 The terms by cause (the engine as laid)

| plan | click: (a) / (b) / (c) / live | mesh: (a) / (b) / (c) / live |
|---|---|---|
| J's terms (contract.pushes) | 1,504 / 8,028 / 20 / 112 | 280 / 1,108 / 0 / 52 |
| Mesh plan (term 6's gradient vertex) | - / 4,044 / 12 / 0 | - / 594 / 0 / 6 |
| push (term 5) | - / 732 / 178 / 0 | - / 210 / 0 / 0 |
| clocks' read | - / 105 / 0 / 25 | - / 30 / 0 / 0 |
| grips' read | - / 24 / 0 / 6 | - / 18 / 0 / 0 |
| Mesh coupling entries (across, 6 R^2) | - / 4,032 / 24 / 0 | - / 596 / 0 / 4 |

### 3.3 S1, like monomials combined at the load (MEASURED)

S1 combines like monomials by their legs alone: sort each monomial's legs, then sum the factors of like monomials over
every monomial. No factor is read.

| world | monomials | J terms | edge key |
|---|---|---|---|
| bang, live | 488 -> 240 | 1,952 -> 960 | unchanged |
| click | 2,416 -> 1,196 | 9,664 -> 4,784 | unchanged |
| mesh | 360 -> 170 | 1,440 -> 680 | unchanged |
| well | 563 -> 273 | 2,252 -> 1,092 | unchanged |

On well this includes the notch's 3 live doubles; the rest are dead copies with like legs.

### 3.4 The work per Node-clock per round, by cause

This is DERIVED from step.py, contract.py and mesh.py, applied to the measured counts. The count per term:
- J contract, the Mesh plan and the push: 3 products per term;
- the passing: 4 + T products per J term, classed by its weight row. A monomial whose value legs lie in one train
  passes nothing at any strength, so its passing work is (b) even where its J is live;
- the clocks' read: 5 calls x 1 per term;
- the grips' read: 1 per term;
- the crossing: 3 per coupling entry;
- the board's per-row work: 45 R, all live (pull 6, gradient 18, the two kicks and drives 6, the stress's momenta and
  splits 7, the two gears 8).

The board's carries are 6 R; the teeth carry one each.

| world | all | (a) | (b) | (c) | live terms | per-row | teeth carries: as laid -> (a)+(b) -> and (c) -> and D1 |
|---|---|---|---|---|---|---|---|
| click | 144,884 | 18,048 | 123,525 | 702 | 1,439 | 1,170 | 175 -> 30 -> 6 -> 3 |
| mesh | 19,248 | 2,800 | 15,476 | 0 | 522 | 450 | 63 -> 6 -> 6 -> 3 |
| bang, live | 23,928 | 3,168 | 19,859 | 300 | 61 | 540 | 28 -> 0 |
| well | 30,221 | 4,240 | 25,009 | 0 | 387 | 585 | 63 -> 0 |

**How my split differs from the readers'.** The physicist's split (140,901 by structure, 1,122 by a chosen 0, 1,661
live on click) differs from mine in two places:
- I class the unit-row terms of live monomials as (a), not live: 16 terms x 12 = 192.
- I class the passing of the notch's chosen-0 terms as (b), since they pass nothing at any strength.

Both splits agree that over 97 percent of the click world's products are dead by (a) or (b).

**The forms' work per Node-clock per round** (DERIVED from the measured term counts of section 4, with the crossing
laid as a list of its coupled entries):
- **click (a)+(b):** 126 J terms x 12 + 12 x 3 + 178 x 3 + 25 x 5 + 6 + 24 x 3 + 1,170 = 3,455, which is 23 per mille
  of 144,884.
- **click with (c) too:** 112 x 12 + 25 x 5 + 6 + 1,170 = 2,645.
- **mesh:** 52 x 10 + 6 x 3 + 4 x 3 + 450 = 1,000, which is 51 per mille of 19,248.

The probes measure the state's reduction, not the work's (math MINOR 6). cause.py computes every passing and every
crossing, then keeps the held ones, so these work figures and "the crossing at the + end only, half its products" are
DERIVED.

## 4. The forms against the engine's own act (MEASURED, cause.py, on 9d75a4904)

**The three forms:**
- **AB** drops (a) and (b) in teeth and terms, holds rd on the T_d > 1 rows alone (D3), and combines like monomials
  (S1). Both teeth of every kept pair are held.
- **ABC** also drops (c).
- **ABC+D1** also holds one tooth per live edge: own (t < u), and Mesh at the + Spoke's site. The partner is read back
  as key - 1 less it, with the negative quotient, the far end one Mesh away.

**What the read-back fills in.** Every dropped side reads back as the birth with q 0; rd reads back as 0 where T_d = 1.

**What is compared, in every round, entry by entry:** a, b, r, rd, every tooth (read back), every click (read back)
and run.clicked's lines (JSON text). At the end: run.teeth_of and the digest of the state read back. Then each form's
run back from its own reduced end alone, nothing saved, the same number of rounds, against its reduced start.

| world (rounds) | entries off (a, b, r, rd, k, clicks, lines), each form | click entries not 0 | record click lines | end teeth, digest read back | run back, each form |
|---|---|---|---|---|---|
| bang tensor24 (10, all its ticks) | 0, 0, 0, 0, 0, 0, 0 | 0 | 0 | equal, equal | exact |
| click (100 of 5,000) | 0, 0, 0, 0, 0, 0, 0 | 4,050 | 5,508 | equal, equal | exact |
| mesh (125, all its ticks) | 0, 0, 0, 0, 0, 0, 0 | 36,192 | 21,589 | equal, equal | exact |
| mesh at file key 7, variant (60) | 0, 0, 0, 0, 0, 0, 0 | 6,824 | 4,204 | equal, equal | exact |
| live (20 of 100) | 0, 0, 0, 0, 0, 0, 0 | 0 | 0 | equal, equal | exact |
| well (10 of 128) | 0, 0, 0, 0, 0, 0, 0 | 0 | 0 | equal, equal | exact |

The forms' plans, as laid:
- **click AB:** J 126, Mesh plan 12, push 178, clocks' read 25, grips' read 6; 30 teeth held.
- **click ABC:** J 112, the rest 0 but the reads; 6 teeth held.
- **click ABC+D1:** 3 teeth held.
- **mesh:** J 52 and Mesh plan 6 in every form; 6, 6 and 3 teeth held.

The mesh variant at file key 7 differs from the shipped mesh world in the key alone (diffed). Its teeth move:
- MIN1 measured 232 Mesh-reach and 112 own-reach entries off their birth in 60 rounds, on the same act.
- The shipped mesh world's teeth never move, since its key 3 divides every passing (the Boss, 07:5x).

## 5. D1, the edge's pair as one number: to the owner's batch before it is built

D1 keeps both teeth of every edge in every read and in the record. It holds them as one number because the carry's
law keeps the second tooth the first one's complement.

Its own-edge half is Big Pic's form already: circ.py's gs[e], one tooth per unordered pair, booked +q on the first
train and -q on the second. It lands with his stage, not as a second form of his part. Its Mesh half is node-all's.

The saving: the live teeth go 6 -> 3 per Node-clock on click and on mesh (section 3.1).

### 5.1 The pair law and its hypothesis (DERIVED; math MINOR 4)

**The pair law.** P(u, t) = -P(t, u) exactly. Across a Mesh, across[opp s] = across[s]^T, and nb[opp s, nb[s, x]] = x,
so the far end passes exactly -P.

Summing Rule3 for the two sides gives key - 1 = (q_tu + q_ut) key + (k'_tu + k'_ut), with the k' sum in
[0, 2 key - 2]. So q_ut = -q_tu and k'_ut = key - 1 - k'_tu, by induction from the birth.

**The hypothesis.** The two births, (key - 1) div senses each, must sum to key - 1, so the edge key must be odd.
- Today the edge key is the file's odd key times kappa div senses.
- kappa = 2 x (3 if a live edged monomial holds 3 counted legs) x (4 if one holds 4), by edging's product.
- MEASURED: kappa div senses is 1 on bang, live and well (no edged monomial; the edge key is the file's key) and 3 on
  click (152,434,287 = 3 x 50,811,429) and mesh (3 = 3 x 1).
- A live edged monomial of 4 counted legs would make it 4 or 12. The edge key is then even, and the births sum to
  key - 2. The pair law then fails at the lay, in the engine and in D1 alike.

Under KEY3 (D = (kappa div senses) K, K = 2 middle + 1 odd), D is odd exactly when kappa div senses is. The load shows
it by structure or refuses an even D by name (the Boss's KEY3 ruling). D1 keeps the hypothesis; KEY3 must keep it.

### 5.2 The 24 on the reduced teeth, and the train swap (MEASURED by both readers; rerun here)

**The move under a turn g.** Take a held Mesh side (s, t, u) at x.
- **Where g sends the + Spoke s to a + Spoke,** the tooth is transported to the image side at gx.
- **Where g sends it to a - Spoke,** the image side is (opp g(s), u, t), held at the image edge's + end, the site
  nb[g(s), gx] across the image Mesh. There the trains swap, (t, u) -> (u, t), the tooth becomes key - 1 - k and the
  quotient becomes -q.

This is not step.mirror's law for k, since the mirror keeps every k. It is a flip of the kind the mirror applies to r
(-1 - s) and to rd. The own teeth move with their site; the 24 permute no train.

**MEASURED: probe24_math.py**, the mathematician's script copied unchanged and rerun on 9d75a4904.
- The setting: the edges test's cube, 3 x 3 x 3, the test's key 1,000,003, edge key 3,000,009, birth 1,500,004.
- After 25 rounds, 162 of 162 held Mesh entries and 26 of 27 own entries are off their birth.
- Over the 24 turns, 21 of them reversing an axis:
  - the pair law is kept in 24 of 24;
  - the transport holds in 72 of 72 cases and the flip with the train swap in 72 of 72;
  - act and turn commute on the state in 24 of 24 and on the clicks in 24 of 24.
- The figures are identical to the reader's on 48cd7fcf6.

**MEASURED by the physicist (turn24.py), not rerun here:**
- the mesh line at file key 7: 8 of 8 turns;
- the cube: 24 of 24;
- the no-flip control misses on every turn that sends a carrying + Spoke to a - Spoke.

The orientation (the + Spoke's site holds the Mesh's tooth) is load.geometry's own and enters no number. The birth is
the flip's fixed point (key - 1 - birth = birth for an odd key).

### 5.3 Locality (phys m4)

In the reduced act no Node-clock reads another's tooth: each held tooth is read only by its own carry, at the Node-clock
that holds it. The + end's crossing of a Mesh edge reads its own gears and its + neighbour's before, now and next counts,
which are the reads the engine's crossing already makes. The - end's crossing of that edge is dropped.

The far side is read back only by the record's writer (run.clicked, run.teeth_of) and by the decoder's sides guard
(decoder/sides.py, mirrored: the two sides' q summing to 0 and their teeth to key - 1, before and after), one Mesh away.
The record is byte for byte, so the guard reads the same text.

## 6. Mode 11's phase (math MINOR 7, phys m5): MEASURED, phase.py, on Big Pic's Stepper (circ.py, ed6a1f225), D = 1601

The turn is the same; MIN1 and THIRD7 read it at two points of the round.
- **At the round's edge** (the stored state, y = 0: eta += 3 tau, tau += 3 eta, the carry, tau += 3 eta,
  eta += 3 tau), the map is [[19, 60], [6, 19]] on (eta, tau). Stepper.step at y = 0 agrees: (2, 5) -> (338, 107).
  In the half-sum basis n = (tau + eta) / 2, p = (tau - eta) / 2 (2's inverse on the odd dial 3D by Rule3's carry),
  this is p+ = -27 n - 14 p: 60 of 60 stated states, and +27 in 0 of 60. This is MIN1's phase.
- **Between carries** (tau += 3 eta, eta += 3 tau, the round's edge, eta += 3 tau, tau += 3 eta), the map is
  [[19, 6], [60, 19]], and p+ = 27 n - 14 p: 60 of 60, and -27 in 0 of 60. This is THIRD7's phase (its b' = 27 a - 14 b).

The two are conjugate, with det 1 and trace 38, so L^2 = 38 L - I at both. Both refute the gear's law b+ = a, which
held in 0 of 60 at either phase.

**The true content of Big Pic's naming.** The mirror (circ's flip of the twin, the tooth kept) swaps n and p exactly
as it swaps a gear's two slots: 60 of 60 (THIRD7's point).

So the triangle holds two new whole counts with a gear's mirror rule. It does not hold "its own now and before" in the
gear's law.

## 7. The other MINORs, answered

### 7.1 The unit-row terms (math MINOR 1)

They are cause (a), proposed in section 8, item 2. The figures are in section 2.

MEASURED, mutants.py unit, click world, 3 rounds: the pruning never parts. The mutant (one live value-leg term dropped
in place of a unit-row term) parts at round 1. The mathematician's prune.py A measured the pruning exact over 100
rounds on click and 60 on mesh at file key 7 (48cd7fcf6, same act).

### 7.2 S1 renamed, and its identity (math MINOR 3, phys m8)

**"Combine like monomials at the load":** sort each monomial's legs, then sum the factors of like monomials.

The 2 of the merged notch pair counts the two orderings of distinct legs, the cross coefficient of h tr^2. It is not
the senses of an axis.

The identity carries it on every state:
- h c_ii c_jj, laid at (i, j) and at (j, i), pushes c_ii by -2 h c_jj, the same as 2 h c_ii c_jj laid once;
- like legs give like weights, so P is linear in the summed factor.

The one hypothesis: like monomials whose factors cancel to 0 would leave J and P exact, but could drop a legs count
from kappa and so move the edge key. No shipped plan has such a pair, and the edge key is unchanged on every world
(MEASURED). A writer reads kappa before the combine, or shows that no pair cancels.

MEASURED:
- section 4's forms carry S1 on every world;
- mutants.py s1, well, 3 rounds: the sum never parts, and the mutant (the first factor kept, not the sum) parts at
  round 1.

### 7.3 a, b and r, each needed (math MINOR 5)

**None is fixed by the others.** All three are laid freely, field by field, by the setting (files.GEAR = train,
component, site, a, b, r; load.lay). Two lays apart in one field alone are lawful starts, and the run back is exact, so
the field carries information of its own (DERIVED).

**r's need is MEASURED** (MIN1, same act). With r dropped on the mesh world, the counts part at round 2 and the clicks
at round 20, and the run back fails.

**b's need is DERIVED.** The gear has two slots, its velocity is a - b and the mirror swaps them.

**The census lines** (MIN1, same act), beside each other:
- (row, a, b) took two values of r or more in 2 of 8 keys (click), 98 of 532 (mesh) and 1,151 of 4,290 (well);
- (row, a, r) took two values of b or more in 0 of 73 (click), 55 of 1,523 (mesh) and 3 of 20,627 (well).
- These lines show only that neither is a function of its row's two others. The lay's freedom is what shows each is
  no function of the whole state.

### 7.4 The probes measure the state, not the work (math MINOR 6)

Labelled in section 3.4: the work figures are DERIVED from the term counts.

### 7.5 The digest, the header and the runner's memory (math MINOR 9, phys m3)

**The digest** is taken on the state read back, E(state) (the Boss's ruling). MEASURED: it is equal on every form and
every world (section 4). MIN1 measured the digest of the reduced arrays themselves unequal on the same act.

**The header:**
- It reads its birth from loaded.state[-1][0, 0], which is the own diagonal (0, 0) at site 0, a cause-(a) tooth.
- It reads each train's key and the dial from the full Click.key array.
- With the state reduced, the writer takes the birth from the load's carry(key - 1, senses) and the key as one number.
- MEASURED (cause.py): the load's carry gives the header's birth on every world (0, 76,217,143, 1, 10, 0, 0), and the
  key holds 1 distinct value over the sides on every world.

**The runner's memory.** run.clicked reads only the listed sides (partners[train]) and the Mesh sides whose q is not
0. run.teeth_of reads only the partners and the crossed edges. All of these are live sides. So per round the writer
reads back only the live sides' partners. Only the end digest's text (stated over the full k) needs the full E, once
per run (DERIVED from run.py:140-198). The saving is in the act's state and carries. The runner keeps the reduced
state, and builds the full k only for the digest.

### 7.6 D3 is stronger than MIN1 said (math MINOR 10)

On a T_d = 1 row, rd lies in [0, 1) = {0} by its dial's range, whatever is laid. The files lay no rd, and load.lay lays
it at 0.

Likewise, on a world whose edge key is 1 (bang, live, well: birth 0), every tooth lies in [0, 1) = {0} by its dial's
range. Those three worlds have no live side in any case (section 3.1); they are the Boss's "NO CLICK by structure".

### 7.7 HAT3 against the headline (phys m6)

"The two-way node doubles nothing" is true of node-all as built. HAT3's third count and second tooth would be the one
element held for the run back alone: written forward, and read only by the mirror. On every state its round reaches,
it is fixed by the gear's now, before and tooth with the held family's slots, by A2 run backward (DERIVED from HAT3's
own text, sections 1 and 3b).

So it is exactly what the owner's note says a two-way node does not need. HAT4's road, an exact time-symmetric step
with no new element, is the answer to it. It waits there and is not built.

### 7.8 Words (phys m7)

The square's train is the clock train, the clock's name CLEAN's D2 gives it. Its 00 slot is the clock's count. The
file's label for it is the word that D2 retires; no sentence here uses that word. "Momentum" and "the force's path"
are the engine's own board names, and no physics is claimed from them. No sentence names light or matter.

## 8. The build list for a writer, now, in order (each with its test and its mutant)

Every item keeps the act's function. The run back, the 24, the books and the record's content stay byte for byte, the
record's digest on the state read back. Each item's test includes the existing ones:
- tests/tensor24_prefixes.jsonl;
- the run and world tests' digests;
- the seed test (i) on the five shipped worlds.

1. **S1, combine like monomials at the load** (runner/load.py, before contract.pushes: sort each monomial's legs, sum
   the factors of like monomials).
   - Test: every shipped world byte for byte against the engine. The monomial counts are 488 -> 240, 2,416 -> 1,196,
     360 -> 170 and 563 -> 273. The edge key is unchanged, read before the combine (section 7.2).
   - Mutant: the first factor kept in place of the sum. MEASURED: it parts at round 1 on well.
2. **The unit-row terms, cause (a)** (engine/contract.py, pushes): lay no term whose target is the unit row.
   - Test: byte for byte; J's terms on click go 9,664 -> 8,160, or 4,784 -> 4,082 after item 1.
   - Mutant: one live value-leg term dropped in place of a unit-row term. MEASURED: it parts at round 1 on click.
3. **The plans pruned by cause (b)** (runner/load.py and plans.py).
   - What it does: the load lays each plan twice, at the file's strengths (the factors) and at the unit strengths (the
     structure). It keeps J's terms with Click.weight and Click.train alike, the Mesh plan, the push, the clocks' read
     and the grips' read wherever the structure's factor is not 0. It lays the crossing as the list of its
     structurally coupled entries (Spoke, r, p, coupling, side) in place of the dense 6 R^2 array.
   - Test: (i) every shipped world byte for byte. (ii) The same pruned index set, on each world with every CHOSEN
     strength but the key at 1, against the engine there.
   - Mutant: the pruning taken from the as-laid factors. MEASURED (mutants.py laid, click): it passes test (i), not
     parting in 3 rounds on the world as laid. It fails test (ii), parting at round 3. So test (ii) is required.
4. **The teeth by causes (a) and (b), and D3** (engine/state.py, step.act and step.mirror, runner/load.py lay, and
   runner/run.py).
   - What it does:
     - State.k holds the sides live at the unit strengths alone: own pairs in both directions, Mesh sides at both
       ends.
     - The act computes and carries those alone; the mirror keeps them.
     - rd is held on the T_d > 1 rows alone.
     - The record's writer reads every other side back as the birth, with q 0.
     - The header takes the birth from carry(key - 1, senses) and the key as one number.
     - The end digest is taken on the state read back.
   - Test: every shipped world's record byte for byte (the click lines, the end teeth, the digest read back, the
     header's birth and dial). The run back from the reduced end alone is exact. The seed test (i) holds. The edges
     test's cube (moving Mesh teeth) is byte for byte too.
   - Mutant: one live side dropped. MEASURED: the teeth and the record's lines part at round 21, on mesh at file key 7.
   - Mutant: the digest taken on the reduced arrays. MEASURED in MIN1 on the same act: the digest is unequal.
5. **The work's doubles and the layout constants** (engine/step.py, mesh.py, runner/load.py).
   - What it does: W(a) and W(b) computed once per round (today twice: step.py:57 and :149); the six stretches once
     (mesh.pull and step.stress:62); the grips laid per row (R, 1) with the meshes gather dropped; Click.key as one
     number, with KEY3's scalar.
   - Test: byte for byte.
   - Mutant, for the writer to run (not measured here): W(b) read as W(a) in stress.

Waiting, not to build now:
- **(c)**, the teeth and terms dead only by a chosen 0, on the one ruling with edging's lit(factor). When it comes,
  item 3's test (ii) still applies, read at the file's strengths.
- **D1**, on the owner's batch (section 9). Its Mesh half is node-all's. Its own half lands with Big Pic's stage.
- **Its mutant**, already MEASURED (mutants.py flip, click): the read-back without the flip parts the teeth and the
  lines at round 1.

## 9. The owner's batch items from MIN2

1. **D1, the edge's pair held as one number.** Both teeth stay in every read and in the record. The record is byte for
   byte (MEASURED).
   - The owner's "one pair of teeth, born complementary" is held as one tooth and its complement.
   - The own-edge half is Big Pic's gs[e] and lands with his stage. The Mesh half is node-all's, held at the + Spoke's
     site.
   - Under the 24 the side goes to the image edge's far end with its trains swapped, at key - 1 - k (MEASURED,
     section 5.2).
   - Its hypothesis is the edge key odd, which KEY3 keeps.
   - The saving per Node-clock: 6 -> 3 live teeth on click and mesh, and with (c) laid live 30 -> 15 on click.
2. **Mode 11's triangle.** Name it as two new whole counts per triangle, the tooth and its twin, with a gear's mirror
   rule (the mirror swaps their half-sum and half-difference). It is not "its own now and before" in the gear's law,
   which holds at neither phase (section 6). This rewords the 07:1x item ("the triangle's tooth with its own now and
   before") and adds no element.
3. **HAT3's third count and second tooth.** A double of information, held for the run back alone. It waits on HAT4's
   miracle, and MIN2 asks for nothing to be added.
4. **The key.** A key finer than the passings' grain is the owner's initialization: the mesh world's key 3 divides every
   passing, so its teeth never move. That is already in the batch from AUDIT2 and LIGHT2. KEY3's D must be odd, by
   structure or refused, for the pair law (section 5.1).

For the Boss, not the owner: the one ruling on edging's lit(factor) settles (c), in teeth and in terms alike.

## 10. DERIVED, MEASURED, OPEN; conduct

**DERIVED:**
- the one standing (section 2);
- why (a) and (b) are exact for every state;
- the pair law and its odd-key hypothesis;
- the 24's move with the train swap;
- locality;
- S1's identity;
- the lay's freedom of a, b and r, and b's need;
- D3 by the dial's range;
- the runner reading back the live sides alone;
- the work counts;
- HAT3's element as a double of information.

**MEASURED here, on 9d75a4904:**
- the split by cause on all five worlds and the key-7 variant;
- the three forms byte for byte, with exact run backs;
- S1's counts;
- the 24 (probe24_math, 24 of 24);
- mode 11's two phases and the mirror's swap;
- five mutants caught.

**MEASURED by the readers or by MIN1 on the same act:**
- r's need;
- the census lines;
- the reduced arrays' digest unequal;
- the physicist's turn24 (8 of 8, 24 of 24, the control);
- the mathematician's prune.py A and B.

**OPEN:**
- (c), on the lit(factor) ruling;
- the work mutant of build item 5, for the writer;
- the writer's own measurement of the work saved (the figures here are DERIVED).

**Overturned by my own measurement:** combining like monomials "at the load" by their legs alone collapses far more
than the notch's 3 live doubles (click 2,416 -> 1,196). Most like legs are dead copies, which the combine sums with
their zeros.

**Conduct:**
- One process at a time, every probe under nice -n 19, with the load between 6.1 and 7.3 before each.
- The readers' scripts were read whole before being run. probe24_math.py was copied into my folder and run on my
  extract.
- I wrote only in S/min2. The frozen MIN1, the readers' folders and every worktree are untouched.
- Nothing was posted. ASCII only.
