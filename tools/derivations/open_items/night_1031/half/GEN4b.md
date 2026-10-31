# GEN4b: three doublets of the half-speed hand on the board (Big Pic's generations owed to the click world)

This is the Boss's deriver of the half-speed gear, 2026-10-31, 03:1x UTC, for the same pair. It folds GEN4's two
readers:
- the mathematician, PASSED with eight minors (hf_math/REPORT_GEN4.md);
- the physicist, NOT PASSED on B1 and B2 with seven minors (hf_phys/gen4/REPORT.md).

The Boss ruled that both readers pass the board facts, and that B1 and B2 are click-world reading specs. GEN4 is kept
frozen.

Big Pic's own words are in bigpic_6537793603.txt, items 5 to 8.

**Probes.** Two are reused, both frozen: probe_gen3.py and probe_gen4.py. One is new: probe_gen4b.py, with
probe_gen4b.txt and probe_gen4b_run2.txt, byte-identical. It holds three small checks: R(h) + R(h^-1) squared, the
quarter-turn characters, and the W = 10^6 row relabelled. The rules: whole numbers, Rule3's carry the one division,
and Z[r2] and Z[w] as exact pairs.

Every MEASURED below is a clock fact on the board.

## 0. What changed

**Phys B1: reading 6 is now each doublet's quarter-turn character, not the 4 pi return.** Every half-speed kind is
-dim on the full turn, so the 4 pi return reads only "half-speed".
- The board's prediction (probe_gen4b part 2): chi(g) / dim on a quarter turn's lift h = (1 + i) / r2 is:
  - +r2 / 2 for E1/2, and -r2 / 2 for E5/2 (each sign flips on -h);
  - 0 for G3/2, so 2' and 2'' read 0;
  - 1/3 for T1 and 1 for A1, the whole-speed controls.
- Readings 1 and 2 now add "and by reading 6".

**Phys B2: reading 2's control is now broken by the world, not by the act.** The world is either a laid state moving
along one axis, or a piece with unequal sides, and the act stays kept by the 24, so the share must leave 1/3. The
reading needs the tie, the gradient-leg table half x T1 -> half, which is OPEN.

**The mathematician's minors:**
- 1: the Krylov count is a lower bound. The commutant gives the upper bound: 1 + 1 + 2 = 4 under the 48, and
  2 + 4 = 6 under the 24 alone. The two meet.
- 2: "two on the G3/2 pair", not "one per copy".
- 3: the trace identity is a proof by Newton's identities. k = 0 to 8 suffice on the 8-dimensional parts.
- 4: "twice the hand's real form" holds under the 24 only.
- 5: "cannot be split": the Galois twist forces only E5/2; the partner's G3/2 is forced only on signed permutations.
- 6: probe_hm5's attribution is corrected.
- 7: the W = 10^6 row is labelled EMPTY.
- 8: (R(h) + R(h^-1))^2 = senses x I, so its rates are +-r2.

**The physicist's minors:**
- m1: as math 4.
- m2: a spring kept by the 24 alone is no lawful board spring.
- m3: the no is a curl push, not a spring.
- m4: "Zeeman" is struck.
- m5: the pair is split about each copy's unparted rate, with w+ w- = W0^2 in the continuous limit.
- m6: "doublet-rate" replaces "species-rate".
- m7: "First to stand" now needs reading 6.

## 1. On the board (clock facts, MEASURED twice)

**1.1 Units and kinds** (GEN3 parts 1 and 2):
- the 24 whole units are Q8, w Q8 and w^2 Q8;
- w's turn takes i to k, k to j and j to i;
- the seven kinds of the 24 are exactly orthonormal in Z[w] pairs.

**1.2 The hand and the train, by characters.**
- E1/2 x T1, the half-speed hand on the three axes, is 2 + 2' + 2'' under the 24, each once.
- Under the 48 it is E1/2 + G3/2: "the cube alone shows 1 + 2" (Big Pic).
- **Under the 48**, HALF2's 24-gear train is (E1/2 + G3/2) + (E5/2 + G3/2), 12 + 12 real: the hand's real form plus
  its Galois partner's. That partner is HALF2's company.
- **Under the 24** the two halves have one character, so the train is twice the hand's real form (24 = 2 x 12). It
  holds each doublet 4 times.
- **The company:** the Galois twist forces E5/2 beside E1/2 in any whole basis. The partner's G3/2 is forced only on
  signed permutations: in whole numbers the hand's real form fits on 16 gears, Lambda's 8 plus the 8-gear train.

**1.3 The whole projectors and the class difference Q** (GEN3 part 4).
- Pi_2 and Pi_c are whole, with Pi_2 + Pi_c = 12 I.
- Q, the sum over w's class less the sum over w^2's class, is whole, antisymmetric, and a sum of L(g). That it is
  central in the 24 is a separate fact.
- Q Pi_2 = 0 and Q Q = -Pi_c, and each r2 lift sends Q to -Q.

**1.4 The count of rates, and 2' = 2'' at every rate** (probe_gen4 parts A and B; probe_gen4b part 1).

The table gives distinct rates of a real symmetric spring C. The measured number is the Krylov rank of a drawn start,
a lower bound. The derived number is the commutant's upper bound.

| spring | kept by | measured: train / 2 / 2' + 2'' | the commutant's bound |
| --- | --- | --- | --- |
| drawn, two draws (17 and 29) | all 48 | 4 / 2 / 2 | 1 (E1/2, one quaternion block) + 1 (E5/2) + 2 (the G3/2 pair, a 2 x 2 quaternion block) = 4 |
| R(h) + R(h^-1), h = (1 + i) / r2 | all 48 | 2 / 2 / 2 | its square is senses x I exactly, so its rates are +r2 and -r2: one sign on E1/2, the other on E5/2, both on the G3/2 pair |
| drawn (draw 17) | the 24 alone, no lawful board spring | 6 / 2 / 4 | 2 (M_2(H) on 2) + 4 (M_4(C) on 2' + 2'') = 6 |

Where the measured count meets the bound, both are stated. The physicist's probe_rates reads the same per-part
counts. The mathematician's probe_hm5 read 4 and 4 (all 48, two draws) and 6 and 6 (the 24 alone), on the whole
train only.

**The two clock facts:**
- (i) **A lawful board spring, kept by all 48, gives the train at most 4 distinct rates, and drawn ones reach 4.**
  - Two are on 2: E1/2 and its Galois partner E5/2. E5/2 is a fourth kind by rate, a board name (the Boss's ruling).
  - Two are on the G3/2 pair.
- (ii) **A real spring never parts 2' from 2''. They share every rate, with its multiplicity.**
  - This is a proof per spring. Each spring here is kept by the 24, so
    tr(C^k B) = (12 / (i r3)) [p_k(2') - p_k(2'')], with p_k the power sums.
  - The 2' and 2'' parts are each 8-dimensional, so equal p_k for k = 0 to 8 fix one characteristic polynomial by
    Newton's identities. The probe checks k = 0 to 24, and every trace is 0.
  - Derived for every real spring: C commutes with every L(g), so with Q.
  - No spring can be the no: that is the clock fact itself. The probe's no, R(h) + R(h^-1) + Q, is a curl push, not a
    spring. It reads tr(Q B) = -384, from Q = -+r12 i on the two 8-dimensional parts.

What needs a term odd in Q is the third doublet-rate, 2' against 2'', not a third rate. Whether Big Pic's "three
rates" means three doublet-rates or three rates of any kind is put to him; nothing is chosen here.

**1.5 By the act's own steps, under R(h) + R(h^-1)** (probe_gen4 part C; labels from probe_gen4b part 3).
- **Where W divides every push:** the other part reads 0 at every round.
- **Where the carry rounds** (W = 3, 5, 6): the spring moved a count at nearly every gear in every round (9,584 to
  9,600 of 9,600 in 400 rounds).
  - The leak is 6 to 15 counts, against the hand's own part of 8,906 to 150,473.
  - It grows with the rounds (7 and 6 at 100 rounds, 14 and 8 at 400, at W = 3) and stays flat in the amplitude.
  - This is a board reading.
- **At W = 10^6 the row is EMPTY:** the spring moved no count. probe_gen4's frozen label "(the carry rounds)" on
  that row is wrong; probe_gen4b part 3 labels it EMPTY.

**1.6 The share per axis row:** 1/3 exactly for 2 and for 2' + 2'' (GEN3 part 6). w's cycle forces it for every kind
on three axes (DERIVED). It is a control of the axes' symmetry, not a reading of the generations.

**1.7 Each kind's quarter-turn character** (probe_gen4b part 2). chi(g) / dim on the lift h = (1 + i) / r2 and on -h:

| kind | on h | on -h |
| --- | --- | --- |
| A1 | 1 | 1 |
| T1 | 1/3 | 1/3 |
| E1/2 | r2 / 2 | -r2 / 2 |
| E5/2 | -r2 / 2 | r2 / 2 |
| G3/2 | 0 | 0 |

On the full turn all three half-speed kinds read -1 per dimension (HALF2 1.1), so only a quarter turn tells them
apart.

## 2. The parting coupling (OPEN)

**Its shape.** A term that parts 2' from 2'' must be odd in Q:
- as a push on the now slot it is a curl force, with complex rates, not a clock;
- as a conservative term it acts on the rates: sigma Q (a - b), with sigma the held hand's winding
  a_A1 a_A2' - a_A2 a_A1'.

The term is kept by every symmetry of the board, since sigma, Q and (a - b) each flip where needed.

**What it does** (a clock fact, DERIVED to first order; its click-world reading is owed). It splits each G3/2 copy's
pair symmetrically about that copy's unparted rate. In the continuous limit w+ w- = W0^2 exactly; the sum is twice
W0 only to first order. It does this only in a world with sigma not 0. Such a world is kept neither by the quarter
turns nor by the run back: the mirrored world has -sigma, with the rates swapped. The term itself is kept by both.

**Is it lawful?**
- No sign test and no INDICATOR: yes.
- The orientation is the sign of a CHOSEN strength.
- **From the families: NO, so it is OPEN.** Three causes:
  - (i) The push reads the now slot alone (hypothesis (d)). A rate leg breaks the run back unless the step is
    implicit.
  - (ii) sigma is time-odd, while the families' tables lay value legs only.
  - (iii) Tonight's rule: a value is lawful only when it comes out of the families and their coupling.
- GEN5 weighs Big Pic's turning-frame form of the same term.

## 3. The road to the click readings (each read twice in the click world, by Big Pic's methods)

**Common to all six:**
- HALF2's 24-gear train laid, in test worlds only;
- a click channel from a half-speed table of the families;
- a clock's own clicks.

The record holds the meetings, their order, each clock's own count, light's clicks and its echo, and no board row.

| reading | what it needs, in click terms | status |
| --- | --- | --- |
| 1. the doublets' own clocks at rest | each rate read as its clock's own count, and by reading 6 to say which rates are 2's. Without the parting coupling, 2' = 2'' at every rate | OPEN |
| 2. each doublet's landings, share 1/3 on each axis | a landing's axis read as the direction of the meeting between two clocks, by light's echo; the doublets told apart by each clock's own count and by reading 6; the tie (half x T1 -> half, OPEN). Control: the axes' symmetry broken by the world (a laid state moving along one axis, or unequal sides), the act kept by the 24, where the share must leave 1/3 | OPEN; a symmetry control, not a generation reading |
| 3. a heavier doublet's line ending in lighter ones | distinct rates (reading 1), and a channel between the doublets | OPEN |
| 4. Koide's Q from the three rates, within the calibre | reading 1, and the calibre condition. Big Pic: no three whole masses meet 2/3 | OPEN |
| 5. the Michelson reading with the held hand turning | the held hand in its window, sigma on the board, and a two-arm world | OPEN |
| 6. each doublet's quarter-turn character | a quarter turn made by the act's own coupling on one path, with the tie (half x T1 -> half) and a whole-speed control through the same turn. The board's prediction is 1.7: 2 reads +-r2 / 2 (E1/2 and E5/2 opposite), 2' and 2'' read 0, T1 reads 1/3, A1 reads 1. The 4 pi return reads half-speed only | proposed, owed, put to Big Pic |

**First to stand: reading 6, then reading 1.**
- Once the common prerequisites and the tie stand, reading 6 can tell 2 from 2' + 2'' by the quarter-turn character.
- Reading 1 needs reading 6 to say which of the four rates are 2's.
- A drawn spring kept by all 48 separates 2 from the G3/2 pair. R(h) + R(h^-1) does not: its two rates +-r2 are
  shared.
- Nothing tells 2' from 2'' until the parting coupling stands.

## 4. Tonight

**Can be built,** as in-memory tests on writer A's items 1 and 2, each with its no:
- the cosets of the 24 and the whole characters;
- Pi_2, Pi_c and Q, with their identities;
- the count of rates, with its bound;
- 2' = 2'' by tr(C^k B) = 0 for k = 0 to 8;
- the quarter-turn characters of 1.7;
- the modes kept by the act.

**Cannot be built:**
- the parting coupling;
- the tie half x T1 -> half;
- any half-speed click;
- the meeting's direction by light's echo on half-speed quanta;
- a clock's own clicks;
- all six readings;
- generations, masses or Koide's Q as physics.

The board shows a central class difference Q, whose odd coupling would part 2' from 2''. No lawful term carries that
coupling yet.
