# GEN4c: three doublets of the half-speed hand on the board (Big Pic's generations owed to the click world)

Status: PASSED by both readers, 03:3x UTC. Their minors are folded in place in section 5, each marked "(03:3x)": the
mathematician's one (hf_math/REPORT_GEN4c_GEN5b.md) and the physicist's three (hf_phys/gen5/REPORT_GEN4c_GEN5b.md).

This is the Boss's deriver of the half-speed gear, 2026-10-31, 03:2x UTC, for the same pair. GEN4b is kept frozen.
The verdicts on GEN4b were:
- the mathematician: PASSED, with two minors (hf_math/REPORT_GEN4b_GEN5.md);
- the physicist: NOT PASSED on B1, the owner's 03:1x word, which came after GEN4b was written, with two minors
  (hf_phys/gen5/REPORT.md).

**Probes.** Reused, all frozen: probe_gen3.py, probe_gen4.py and probe_gen4b.py. New: probe_gen4c.py, with
probe_gen4c.txt and probe_gen4c_run2.txt, byte-identical, holding the third-turn characters and the Koide circle on
the median. The rules: whole numbers, Rule3's carry the one division, and Z[r2] and Z[w] as exact pairs.

Big Pic's words are in bigpic_6537793603.txt and bigpic_6538128481.txt.

On the board there are only clocks (the owner's 03:2x word). The half-speed hand and its doublets are clocks. Light
and matter appear only in the click world's readings.

## 0. What changed

- **Phys B1, the owner's 03:1x word:** "Big Pic found exactly what was missing. He has the full picture. And it should
  include the three generations." Section 5, new, names how the doublets meet Big Pic's triangles (6538128481 items 2
  to 4), each link with its status, as the physicist lists them.
- **Math 1 and phys 1:** 1.7 now says that only the quarter turn tells E1/2 from E5/2, while a third turn tells 2 from
  the G3/2 pair (probe_gen4c part 1).
- **Math 2:** 1.5 quotes probe_gen4's range, 9,593 to 9,600, for the counts the spring moved.
- **Phys 2:** section 3 names the readings by species, told apart by their own counts and by reading 6. "Doublet" is
  kept for the board's prediction.
- **Kept consistent with GEN5b:** section 2's cause (i) is restated. The rate leg reads the rates of the rows it
  pushes, which hypothesis (d) forbids. Term 5's push, by contrast, reads momenta lawfully, because it lands on rows
  whose momenta it does not read.

## 1. On the board (clock facts, MEASURED twice)

**1.1 Units and kinds** (GEN3 parts 1 and 2):
- the 24 whole units are Q8, w Q8 and w^2 Q8;
- w's turn takes i to k, k to j and j to i;
- the seven kinds of the 24 are exactly orthonormal in Z[w] pairs.

**1.2 The hand and the train, by characters.**
- E1/2 x T1, the half-speed hand on the three axes, is 2 + 2' + 2'' under the 24, each once.
- Under the 48 it is E1/2 + G3/2: "the cube alone shows 1 + 2" (Big Pic).
- Under the 48, HALF2's 24-gear train is (E1/2 + G3/2) + (E5/2 + G3/2), 12 + 12: the hand's real form plus its
  Galois partner's, which is HALF2's company.
- Under the 24 the two halves have one character, and the train is twice the hand's real form.
- The Galois twist forces E5/2 in any whole basis. The partner's G3/2 is forced only on signed permutations: in whole
  numbers the hand's real form fits on 16 gears.

**1.3 The projectors and the class difference Q.**
- Pi_2 + Pi_c = 12 I.
- Q, the sum over w's class less the sum over w^2's class, is whole, antisymmetric and a sum of L(g). That it is
  central is a separate fact.
- Q Pi_2 = 0, Q Q = -Pi_c, and each r2 lift sends Q to -Q.

**1.4 The count of rates, and 2' = 2'' at every rate** (as GEN4b 1.4, unchanged).
- A spring kept by all 48 gives the train at most 4 distinct rates: 1 for E1/2, 1 for E5/2 and 2 on the G3/2 pair.
  Drawn springs reach 4.
- R(h) + R(h^-1) squares to senses x I, so it has 2 rates, +-r2.
- A spring kept by the 24 alone, which is no lawful board spring, gives 6.
- A real spring never parts 2' from 2''. The proof per spring is tr(C^k B) = 0 for k = 0 to 8, by Newton's identities
  on the 8-dimensional parts; the probe checks k = 0 to 24.

**1.5 By the act's own steps, under R(h) + R(h^-1).**
- Where W divides every push, the leak is 0 at every round.
- Where the carry rounds (W = 3, 5, 6): the spring moved 9,593 to 9,600 of 9,600 counts in 400 rounds (probe_gen4
  part C). The leak is 6 to 15 counts against the hand's own 8,906 to 150,473, growing with the rounds and flat in the
  amplitude.
- The W = 10^6 row is EMPTY: the spring moved no count (probe_gen4b part 3).

**1.6 The share per axis row:** 1/3 exactly for 2 and for 2' + 2''. w's cycle forces it for every kind on three axes
(DERIVED). Section 5 gives Big Pic's reading of it.

**1.7 Each kind's turn characters** (probe_gen4b part 2 and probe_gen4c part 1). chi(g) / dim on a quarter turn's
lift h = (1 + i) / r2 and on a third turn's lifts w (order 3) and -w (order 6):

| kind | h | -h | w, order 3 | -w, order 6 |
| --- | --- | --- | --- | --- |
| A1 | 1 | 1 | 1 | 1 |
| T1 | 1/3 | 1/3 | 0 | 0 |
| E1/2 | r2 / 2 | -r2 / 2 | -1/2 | 1/2 |
| E5/2 | -r2 / 2 | r2 / 2 | -1/2 | 1/2 |
| G3/2 | 0 | 0 | 1/4 | -1/4 |

- **The quarter turn** tells E1/2 from E5/2, and it alone does.
- **A third turn** tells the doublet 2 (E1/2 and E5/2 alike) from the G3/2 pair.
- **The full turn** reads -1 per dimension on all three half-speed kinds (HALF2 1.1).

## 2. The parting coupling (OPEN)

**Its shape.** A term that parts 2' from 2'' must be odd in Q. A conservative one acts on the rates:
sigma Q (a - b), with sigma the held hand's winding a_A1 a_A2' - a_A2 a_A1'. It is kept by every symmetry of the
board.

**What it does** (a clock fact, DERIVED to first order; its click-world reading is owed). It splits each G3/2 copy's
pair symmetrically about that copy's unparted rate. In the continuous limit w+ w- = W0^2; the sum is twice W0 only to
first order. It does so only in a world with sigma not 0, which is kept neither by the quarter turns nor by the run
back.

**Lawful? From the families: NO, so it is OPEN.** Three causes:
- (i) Q (a - b) reads the rates of the rows it pushes, which hypothesis (d) forbids. Term 5's push reads momenta
  lawfully, because it lands on rows whose momenta it does not read.
- (ii) No family's table yields sigma.
- (iii) Tonight's rule: a value is lawful only when it comes out of the families and their coupling.

GEN5b weighs the turning-frame form of the same term.

## 3. The road to the click readings (each read twice in the click world, by Big Pic's methods)

**Common to all six:**
- HALF2's 24-gear train laid, in test worlds only;
- a click channel from a half-speed table of the families;
- a clock's own clicks.

The record holds the meetings, their order, each clock's own count, light's clicks and its echo, and no board row
and no kind label.

| reading | what it needs, in click terms | status |
| --- | --- | --- |
| 1. the species' own clocks at rest | each species' rate read as its clocks' own count, the species told apart by those counts and by reading 6. The board's prediction: without the parting coupling the doublets 2' and 2'' share every rate | OPEN |
| 2. each species' landings, share 1/3 on each axis | a landing's axis read as the direction of the meeting between two clocks, by light's echo; the species told apart by their own counts and by reading 6; the tie (half x T1 -> half, OPEN). Control: the axes' symmetry broken by the world (a laid state moving along one axis, or unequal sides), the act kept by the 24, where the share must leave 1/3 | OPEN |
| 3. a heavier species' line ending in lighter ones | distinct rates (reading 1), and a channel between the species | OPEN |
| 4. Koide's Q from the three rates, within the calibre | reading 1, and the calibre condition; section 5's circle | OPEN |
| 5. the Michelson reading with the held hand turning | the held hand in its window, sigma on the board, and a two-arm world | OPEN |
| 6. each species' quarter-turn character | a quarter turn made by the act's own coupling on one path, with the tie and a whole-speed control through the same turn. The board's prediction is 1.7: the doublet 2 reads +-r2 / 2 (E1/2 and E5/2 opposite), the G3/2 pair 0, T1 1/3, A1 1. A third turn tells 2 from the G3/2 pair. The 4 pi return reads half-speed only | proposed, owed, put to Big Pic |

**First to stand: reading 6, then reading 1.** Nothing tells 2' from 2'' until the parting coupling stands.

## 4. Tonight

**Can be built,** as in-memory tests, each with its no:
- the cosets and the characters;
- Pi_2, Pi_c and Q;
- the count of rates with its bound;
- 2' = 2'' by tr(C^k B) = 0;
- the turn characters of 1.7;
- the modes kept by the act.

**Cannot be built:**
- the parting coupling;
- the tie;
- any half-speed click;
- a clock's own clicks;
- all six readings;
- generations, masses or Koide's Q as physics.

## 5. How the doublets meet Big Pic's triangles (the owner's 03:1x word)

Big Pic, 6538128481:
- item 3: "With three takers (the three families), the hand's three parts give three shares: a point's three heights
  in an equilateral triangle, over its whole height (Viviani)", and "Koide's 2/3 is a circle in the same triangle";
- item 4: "the shares of 1/3 per axis row, the first click reading of the three families";
- his method (c): the three families there are "a clock's counts and the takers' shares", not the kinds of click.

| link | status |
| --- | --- |
| Three takers' shares as a point's three heights. Shares p_i >= 0 with SUM p_i = 1 are a point's three heights over the whole height of an equilateral triangle (Viviani), so every split among three takers is a point of the triangle. For Big Pic's shares, the present squares' rule p_i = a_i^2 / SUM a^2: for three takers, Pythagoras in three dimensions (a vector's squared direction cosines sum to 1); Euclid's leg theorem is the two-taker case (03:3x) | DERIVED as algebra. OPEN in the act (the third click is not built; its law failed tonight) and in the clicks |
| Koide's 2/3 as a circle in the same triangle. With root shares s_i = r_i / SUM r (r_i the roots of the three rates), Q = SUM s_i^2 and \|s - centre\|^2 = Q - 1/3, so Q = 2/3 is the circle \|s - centre\|^2 = 1/3. Note: this is a different point of the triangle from the takers' p_i (first powers against squares) | DERIVED as algebra |
| The circle on tonight's board (03:3x). The clock fact is 2' = 2'' at every rate (1.4). Taken with one rate per doublet, it puts the point on the median s' = s''. Under a lawful spring, 2 carries two rates and the G3/2 pair two, and the median holds for every choice that pairs a rate of 2' with the same rate of 2''. Which three of the four rates belong to the triangle is OPEN, on Big Pic. The meeting points are algebra, checked in exact pairs (probe_gen4c part 2, rerun): s_2 = (1 + r2) / 3 with s' = s'' = (2 - r2) / 6, and s_2 = (1 - r2) / 3 with s' = s'' = (2 + r2) / 6, both with shares summing to 1, SUM s^2 = 2/3 and \|s - centre\|^2 = 1/3. Which lies in the triangle is an order claim, DERIVED on paper (Z[r2] pairs have no order): the first, with s_2 above the pair (a board ordering, its click reading owed); the second has s_2 < 0. The circle crosses all three edges, since its radius^2, 1/3, exceeds the inradius^2, 1/6; beyond an edge a root share is negative. Three distinct rates need the parting coupling (section 2) | the median a clock fact (1.4); the meeting points DERIVED as algebra; their order DERIVED on paper; which three rates OPEN; three distinct rates OPEN |
| The doublets as the three takers | OPEN, waiting on Big Pic: by his (c), the triangle's three families are a clock's counts and the takers' shares |
| The 1/3 share | w's cycle forces it for every kind on three axes (DERIVED, 1.6). Big Pic calls it "the first click reading of the three families"; how it reads the families is his (OPEN) |
