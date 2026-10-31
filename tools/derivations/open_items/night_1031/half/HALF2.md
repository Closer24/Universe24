# HALF2: the half-speed gear on the act as built, the second text

Status: PASSED by both readers, 02:1x UTC (seven minors folded, each marked "02:1x" where it stands).

The Boss's deriver of the half-speed gear, 2026-10-31, 01:5x UTC. It folds the hostile mathematician's report
(hf_math/REPORT.md: PASSED, eight MINOR) and the hostile physicist's (hf_phys/REPORT.md: NOT PASSED, B1 to B3 BLOCKING,
M1 to M11 MINOR) under the Boss's five rulings. HALF.md and its probes stand frozen. New probes, each run twice and
byte-identical, with scratchpad/live/.venv/bin/python -I on live 7dcb31607:
- probe_half2.py, a copy of probe_half.py with two changes: the exact check, and the count of tooth moves;
- probe_half_board2.py, the board with the control widened;
- probe_half_candidates.py, the 48 as weighed candidates; probe_half_candidates2.py, the structural weight (02:1x).
All use whole numbers, with Rule3's carry as the one division. Statuses are DERIVED, MEASURED (on the board) and
OPEN. No claim of physics stands here.

## 0. What changed

- Ruling 1, B3: a half-speed train is admitted in a test world only (2, item 5). No family couples it in this build,
  so an uncoupled train would be a declared particle.
- Ruling 2, B1: the word "light" is struck from the board. The doublet's mixing is the board's whole-speed wave under
  FAMILIES4's probe table, a board reading. Whether light mixes them is NOT READ (1.5).
- Ruling 3, B2: the clicks' owed lines now begin with the gate. Owed first: a click channel from a half-speed table of
  the families, and a turn made by the act's own coupling, checked against a whole-speed control (3).
- Ruling 4: the (p, q) pairs are lawful. They are the exact ring Z[x] / (x^2 - senses): pairs compared only for
  equality, no order, no root computed or approximated. This is as the mathematician reads it; Sofer and Big Pic to
  confirm.
- Ruling 5, math 7: the wall's divisor is stated (1.5).
- Math 1: the orthogonality is now checked whole. All 8 diagonal sums read quotient 1, remainder 0, r2 part 0; all 56
  off-diagonal sums read 0, 0, 0 (probe_half2).
- Math 2: 2 Re g is the trace of g as an SU(2) matrix. That classical fact makes it E1/2's character (1.1).
- Math 3: "at any size" is struck. What is proved: every orbit is one of the two trains, under the premise that the
  full turn is -I. Sums of orbits make the rest (16 = 8 + 8, 32 = 8 + 24).
- Math 4: "W = 1 only" is now "wherever W divides every push", which is where the split never rounds.
- Math 5: the rows where nothing rounds are now marked EMPTY: the 8-gear rows at W = 1 and 2, and the 24-gear row at
  W = 1. The tooth moved 0 times in those rows, and 105 times at W = 3, as the mathematician also counted.
- Math 6: the "only if" half of H1 is the carry's lemma (FAMILIES 208; ONE_ALGEBRA 1 (i)), now cited.
- Math 8 and phys M9: C6 is now the powers of (1 + i + j + k) / 2. The lifts' order and the coset representatives are
  fixed by rule (2, item 2). The 48 can also come as weighed candidates, with no closure search.
- Phys M1: "E1/2" now stands where "spin 1/2" stood. The kinds are the 48's own: E1/2 also comes from j = 7/2 and
  9/2, and G3/2 from j = 5/2. Phys M2 and M8: the sign is an inner Z2 of the train (1.4). Phys M3: "half-speed" is
  defined once (1.0).
- Phys M4, M5, M6, M10 and M11 are folded as worded (1.3, and 2 item 6). Phys M7: the electron's list now ends with
  "among others" (4).

## 1. The clock (on the board)

**1.0 Half-speed** means: the full turn, the unit -1, acts on the train as -I. Its speed against the board's turn is
OPEN (1.3).

**1.1 The eight kinds (MEASURED, twice).** The 48 units close from the lifts (1 + i) / r2 and (1 + i + j + k) / 2.
Each kind's character is read from the unit g:
- A1 = 1;
- T1 = the trace of the sandwich pi(g), which is a whole signed permutation of the axes;
- A2 = the determinant of pi(g)'s squared entries;
- E = the trace of that permutation, less 1;
- T2 = A2 T1;
- E1/2 = 2 Re g, the trace of g as an SU(2) matrix;
- E5/2 = A2 x 2 Re g;
- G3/2 = 2 Re g x E.

The degrees are 1, 1, 2, 3, 3, 2, 2, 4, and their squares sum to 48. The characters are orthonormal exactly (math 1).
Frobenius-Schur reads +48 on the five whole-speed kinds and -48 on the three half-speed kinds. The full turn is +1 on
the five and -1 on the three. This agrees with MIRACLES row 6.

**1.2 The half-speed signed-permutation trains (DERIVED, MEASURED twice).**

Hypotheses:
- (H1) The carry works per gear: step.split gives n = q 4W + s with s in [-2W, 2W) on a standing dial
  (D = 2 W). A gear negated by a turn takes the tooth's flip s -> -1 - s, so n -> -n - 1 and
  split(-n - 1) = (-q, -1 - s); the drive's tooth flips the same way. So the carry turns with a whole matrix on the
  gears if and only if that matrix is a signed permutation. The "only if" half is the carry's lemma (FAMILIES 208;
  ONE_ALGEBRA 1 (i)).
- (H2) J is linear in the now slot and turns with the 48.
- (H3) The train has one dial W. The clock's read is kind-blind.

Derivation (the monomial theorem). Each orbit of the 48 on the gears' lines is Ind_H(lam): H is the subgroup that
keeps a line, and lam: H -> {+1, -1} is its sign there. The premise that the full turn is -I puts -1 in H with
lam(-1) = -1, which needs -1 outside the squares of H. Only two subgroups qualify:
- H = {+1, -1};
- H = C6, the powers of (1 + i + j + k) / 2, with lam +1 on the squares of C6 and -1 elsewhere on C6 (02:1x).

In every other subgroup holding -1, -1 is a square: x^2 in C4, x^4 in C8, y^2 in Q8, Dic3, Q16, 2T and 2O.

Measured by enumeration: 35 subgroups, 5 pairs (H, lam) and 2 trains. Both readers re-derived these, the physicist by
hand.
- **The 8-gear train**, the cosets of C6, is 2 G3/2: the real form of G3/2.
- **The 24-gear train**, the units mod sign, is 2 E1/2 + 2 E5/2 + 4 G3/2. In real dimensions that is E1/2 (4) +
  E5/2 (4) + G3/2 (8) + G3/2 (8).

So G3/2 rides alone. E1/2 rides only inside the 24-gear orbit, with E5/2 and two G3/2 (FAMILIES3's doublers); E5/2
likewise. The company has two reasons (02:1x): the Galois twist forces E5/2 beside E1/2 in any whole basis (on
Lambda's 8 gears, whole but not signed permutations, E1/2 + E5/2 rides with no G3/2); the orbit, by the monomial
theorem on signed permutations, forces the two G3/2. Every other half-speed signed-permutation train is a sum of
these orbits.

Where each kind rides on the per-gear carry:

| kind | gears | W (DERIVED on H1 to H3; measured at the W of 1.3) |
| --- | --- | --- |
| A1, A2 | 1 | every W |
| T1, T2 | 3 | every W |
| E | 3, inside A1 + E (the axes' permutation; the square's ii slots) | every W |
| G3/2 | 8, the cosets of C6 | every W |
| E1/2, E5/2 | 24, the units mod sign, with two G3/2 | every W |
| E1/2 alone | 4 (Hurwitz) or 8 (Lambda) | only where W divides every push (no rounding); else the wall (1.5) |

**1.3 On the act's own gear (MEASURED, twice).** The setup:
- one Node-clock, with step.gear and step.split as built;
- the push J = (C - 2 W) a, with C = SUM_g L(g) M L(g)^T for a drawn whole M. M is not symmetric, so this push is no
  -dH/da: it is a probe coupling, linear and equivariant, which is all H2 needs (phys M5);
- the 48 act by (P a, P b, P s), with the tooth flipped on every negated gear.

Results:
- **8-gear train.** The turned run equals the run turned, 144 of 144 (48 lifts x 3 starts, 6 rounds each), at 10
  dials: W = 1, 2, 3, 5, 6, 9, 12, 42, the click world file's rest dial 6 x 10^8 (a board dial), and the example
  universe's 6 den Gamma^2. The rows at W = 1 and 2 are EMPTY (the tooth never moved); elsewhere it moved 93 to 144
  times. The run back by (b, a, -1 - s) is exact, 3 of 3, at each dial.
- **24-gear train.** 96 of 96 at 6 dials: W = 1, 5, 6, 9, 42 and 6 x 10^8. W = 1 is EMPTY; elsewhere the tooth moved
  126 to 192 times. The run back is exact, 2 of 2.
- **The no.** A signed permutation that is no lift holds 0 of 144 and 0 of 96 at W = 6. E1/2 alone on Hurwitz's 4
  gears, with a spring of 1, holds 5 to 14 of 120 at W = 2 to 42.
- **The scope (phys M6).** "Every W" is DERIVED. The measurement covers these dials.
- **On a 3 x 3 x 3 board** (probe_half_board2), with the Mesh pull and the sites turned: 48 of 48 on both trains, and
  the run back exact. A lift's gears with any turn's sites holds too: 1152 of 1152 (all 48 x 24, phys M10) on the
  8-gear train at W = 6, my widened control; the 24-gear train's 1152 of 1152 and the W = 9 runs are the
  physicist's (probe_phys Q1) (02:1x). The train's lifts and the board's turns are separate symmetries. Nothing ties the
  gear's turn to the board's until a gradient-leg table, half x T1 -> half (the hopping), does that (OPEN).

**1.4 The full turn (DERIVED).** Every table the 48 keep has an even count of half-speed legs, since an odd count
sums to 0 over g and -g. So the act commutes with -I on the half-speed rows (teeth flipped) and with I on every other
row. This sign is an inner Z2 of the train, not a turn of the board (phys M2). Pairing a board turn with one lift is a
choice until the hopping table ties the two. The mirror commutes with every L(g): on a negated gear both orders give
(-b, -a, s). So the run back is the act's own, for any push read from the now slot (math). Kramers' T = R(i) after
the mirror (02:1x) exists only by a choice of coupling that no family derives tonight: it holds 3 of 3 under a
coupling that keeps R(i) and 0 of 3 under the drawn C (phys M8).

**1.5 The pick, and the wall.**
- **The pick.** G3/2 on the 8-gear train: alone, every W, no new carry, no compare, no if. The 24-gear train also
  rides every W, but only with its company: two G3/2. Under FAMILIES4's probe table, which this build does not lay, a
  whole-speed board wave mixes that company with the doublet: the leak reads 758, 457 and 367 thousandths, a board
  reading. Light lives in the click world, and whether light mixes them is NOT READ (B1). The owner's "No price is
  allowed" stands against laying the 24-gear train as the electron.
- **The wall's divisor (ruling 5).**
  - On the split's own divisor 4 W, no fixed-dial carry turns with its lifts at any W >= 2 (gcd(4 W, 6) >= 2); on
    Hurwitz's 4 gears the lifts are the 24 Hurwitz units (02:1x).
  - On the reduced tooth, the act keeps each tooth's residue mod senses^2 = 4 at a standing dial
    (n = 4 W (a - b) + 4 J + s). There ONE_ALGEBRA's gcd(W, 6) reading holds. But the mirror -1 - s moves the
    residue class, so such a carry would need its own mirror.
  - Both readings put every loaded dial on the wall: W = 6 den Gamma^2 + k0 c00, with k0 = 12, is divisible by 6.
  - The quotient-dependent carry turns at every W, but it compares 24 images (MIRACLES 11).
  - A compare-free, table-free rule is OPEN.

## 2. The loader and the files (the list kept; no code here)

Every item keeps these laws: no number beyond 0 and 1 in src (48, 24, 8 come from the counts of the lifts and the
cosets, and 2 is senses), no typed table, no train declared in code, Rule3's carry as the one division, paths by
joinpath.

1. **engine/kinds.py, the lifts.** Weigh candidates, as kinds.turns weighs the 216. Each doubled coordinate is 0, +-1
   or +-2 (sums of two of the star's entries), or +-r2. Weight 1 goes where the doubled norm is senses^2 with r2 part
   0 and the lift's sandwich takes every Spoke to a Spoke, that is, its turn is one of the 24 (02:1x, the structural
   weight, replacing the typed "all rational or all r2"): 48 of the 144 of norm senses^2 kept, the closure's set
   exactly (probe_half_candidates2; the mathematician's probe_hm3 finds 144, then 48, on 390,625 candidates too).
   The weight gives each lift's turn in the same step and derives the 48 as the lifts of the board's 24. The no: the
   norm alone keeps 144. The product is read by its index.
2. **engine/kinds.py, the half-speed kinds.**
   - Their characters go on the 48 as (p, q) pairs.
   - The two trains are signed permutations built from cosets: the 8-gear train on the cosets of C6, the powers of
     (1 + i + j + k) / 2, with lam +1 on the squares of C6 (the diagonal of the product table) and -1 elsewhere on
     C6 (02:1x); the 24-gear train on the classes +-h, with L(g) e_[h] = sign x e_[gh].
   - The lifts' order is the candidates' order, with no sort. A coset's representative is its first lift in that
     order, found by load.first's trick, with no compare.
   - The five whole-speed kinds go on the 48 through each lift's turn.
   - The fields are e1_2, e5_2, g3_2, labelled "E1/2", "E5/2", "G3/2".
3. **main.made** passes the lifts and the half-speed kinds. The five kinds' tables stay as built on the 24.
4. **runner/files.py.**
   - There are eight labels.
   - A half-speed kind is admitted only in the 8-gear train (["G3/2"], part 2) or the 24-gear train (["E1/2",
     "E5/2", "G3/2", "G3/2"], part 2). The train's character must have no r2 part and must be -I on the full turn.
   - Every other mix is refused by name.
5. **The universe file (B3, ruling 1): test worlds only.**
   - held_departures refuses every file-run universe naming a half-speed kind, by name: "no family couples a
     half-speed train in this build".
   - A test lays such a world in memory, through load.load and the act.
   - The refusal goes when a half-speed table from the families is built.
   - No new key. A half-speed gear's component is its coset's index.
6. **runner/load.py, trains_of.** A half-speed train is not the square, not the held hand, and untied (NOT_CLOSED 8).
   It is gripped by the Mesh, and its rows lie on the force's path (T_d = 1). It sources the metric's push as the
   matter train does on the board: the tooth's flip sends -m - 1 to -sigma.
7. **runner/load.py, lay.** The train's rows are its cosets: 8 or 24.
8. **runner/plans.py, pairs_of.** The train's form onto A1 is its kept form, SUM L^T L, whose primitive row is the
   dot. There is no half-speed table in this build. Meshing gives 0, since an odd count of half-speed legs has no A1
   channel.
9. **record/schema.py, 1.4.** One ADDED entry: the lifts with their turn indices, and the three half-speed kind
   cards, their characters as (p, q) pairs. The decoder must accept 1.4; the writer checks the minor rule.
10. **Tests**, in memory, each with its no:
   - the two trains, and only those;
   - the 48 turning the run at a W that rounds, including 6 den Gamma^2, with a non-lift as the no;
   - the run back through step.act;
   - the board with the sites turned;
   - item 4's refusals, and item 5's refusal of a file-run world.

## 3. The clicks (B2, ruling 3)

**The gate.** After section 2 is built, a half-speed train still cannot click: it is untied and takes no half-speed
table, and the passing reads the value legs alone. For any own push that is -dH/da the passing X is 0: the physicist
measured X = 0 at 20 of 20 draws on both trains with step.passing. On top of that, the board's turns do not reach the
gears: 1152 of 1152 on the 8-gear train at W = 6 (probe_half_board2), and on the 24-gear train and at W = 9 by the
physicist's probe_phys Q1 (02:1x). So a two-path flip laid by hand cannot fail, since lam(-1) = -1 by construction.

- **(a) Interference: OPEN, NOT READ.** Owed:
  - a half-speed table from the families, as the click channel;
  - the tie (half x T1 -> half);
  - a turn made on one path by the act's own coupling, on every kind at once;
  - a whole-speed control through the same device;
  - the clicks at the screen, read twice in the click world.
- **(b) Like clicks: OPEN, NOT READ.** Owed:
  - the same click channel;
  - two quanta, a hand per quantum (FRAMES 12);
  - the like-click weighing (term 12's draw);
  - the coincidence clicks, read twice, never two at one place, against the whole-speed control's bunching.

## 4. OPEN

- The compare-free, table-free carry for E1/2 alone on 4 or 8 gears.
- The electron. It needs, among others: its company gone, the tie, the exclusion, a click channel with the click
  world's light, the particle and the antiparticle, and Kramers' T^2 = -1 from a family's coupling.
- A refusal that acts: only with a second hand (FAMILIES4).
- The hopping table half x T1 -> half, and whether it rides the carry.
- The half-speed tables from the families, the tie to the held hand, and with them the end of item 5's test-only
  rule.
