# HALF: the half-speed gear on the act as built (sections 1 and 2; 3 and 4 one line each)

The Boss's deriver of the half-speed gear, 2026-10-31, 01:2x UTC, under the owner's rule of 01:3x UTC (a derivation,
20 minutes at most). Probes beside it: probe_half.py (probe_half.txt, probe_half_run2.txt) and probe_half_board.py
(probe_half_board.txt, probe_half_board_run2.txt), each pair byte-identical, run with scratchpad/live/.venv/bin/python
-I on the package at live 7dcb31607 (step.gear and step.split identical to node-live 49e97c992; the board probe
imports probe_half by a path put first, as -I adds none). Whole numbers; Rule3's carry the one division (exact
halvings checked to remainder 0); no float, root, math, random, fractions, sine or cosine; nothing typed but the two
generator lifts. Statuses: DERIVED, MEASURED (on the board), OPEN. No claim of physics stands here: every MEASURED
is on the board.

## 1. The clock (on the board)

**1.1 The eight kinds, from the units alone (MEASURED, probe part 1, twice).** The 48 units close from the two lifts
(1 + i) / r2 and (1 + i + j + k) / 2 in Z[r2] (stored doubled as pairs p + q r2: r2 is a symbol of the ring, no root is
taken). Each kind's character on the 48 from the unit g alone: A1 = 1; T1 = trace of the sandwich pi(g) (whole, a
signed permutation of the axes); A2 = det of its squared entries (the axes' permutation sign); E = trace of that
permutation less 1; T2 = A2 T1; E1/2 = 2 Re g; E5/2 = A2 x 2 Re g; G3/2 = 2 Re g x E. Read: degrees 1, 1, 2, 3, 3, 2, 2,
4 (squares sum 48); <chi, chi> = 1 on all eight and <chi, psi> = 0 on all 56 ordered pairs, so they are the 48's eight
kinds; Frobenius-Schur SUM chi(g g) = +48 on the five whole-speed kinds and -48 on E1/2, E5/2, G3/2; the full turn
(the unit -1) is +1 on the five and -1 on the three. This repeats MIRACLES row 6 (p1) by another code: agreed.

**1.2 Which signed-permutation trains carry a half-speed kind (DERIVED, MEASURED twice).**
- Hypotheses. (H1) The act's carry is per gear (step.split: n = q 2D + s, s in [-D, D)); a gear negated by a turn
  takes the tooth's flip s -> -1 - s, so its momentum goes n -> -n - 1 and split(-n - 1) = (-q, -1 - s) exactly
  (SYM24's invariant box; the drive's tooth r_d -> T_d - 1 - r_d likewise). So the carry turns with a matrix on the
  train's gears exactly when it is a signed permutation (the families' lemma). (H2) The push J on the train is linear
  in the now slot and turns with the 48: J(L(g) a) = L(g) J(a). (H3) Every row of the train has one dial W (the
  clock's read is kind-blind: every row reads the square's 00 slot at k0 alike).
- Derivation. On a signed-permutation train the 48 permute the gears' lines; each orbit is Ind_H(lam), H the lifts
  keeping a line and lam: H -> {+1, -1} its sign there. The full turn -I on the train puts -1 in every H with
  lam(-1) = -1, which needs -1 outside the group of squares of H. In the 48 (subgroups: cyclic 1, 2, 3, 4, 6, 8, Q8,
  Dic3, Q16, 2T, 2O, each made by two elements) that leaves H = {+1, -1} and H = C6, the lifts of a third turn
  (lam = -1 on the order-6 lift): in every other subgroup holding -1, -1 is a square (x^2 in C4, x^4 in C8, y^2 in
  Q8, Dic3, Q16, 2T and 2O).
- Measured (part 2): 35 subgroups, every (H, lam) with lam(-1) = -1 enumerated: 5 pairs, 2 trains, each signed
  permutations 48 of 48 with the full turn -I:
  - **the 8-gear train**, the cosets of C6: the kinds 2 G3/2 (the real form of G3/2);
  - **the 24-gear train**, the units mod sign: 2 E1/2 + 2 E5/2 + 4 G3/2 (real: E1/2 4 + E5/2 4 + G3/2 8 + G3/2 8).
- Theorem (DERIVED on H1 to H3). G3/2 rides alone on 8 gears. Spin 1/2 (E1/2) rides a signed-permutation train only
  inside the 24-gear one, with E5/2 and two G3/2 (FAMILIES3's doublers, five doublet-equivalents), at any size and any
  W; never alone on 4 or 8 gears. E5/2 likewise. FAMILIES3 named the least forms and Big Pic's p4 lemma excluded 4
  and 8 gears by traces; new here is the whole list: no other half-speed signed-permutation train exists, at any size.
- Where each kind rides on the act as built (the per-gear carry):

  | kind | gears | W |
  | --- | --- | --- |
  | A1, A2 | 1 | every W |
  | T1, T2 | 3 | every W |
  | E | 3, inside A1 + E (the axes' permutation; the square's ii slots) | every W |
  | G3/2 | 8, the cosets of C6 | every W |
  | E1/2, E5/2 | 24, the units mod sign, with two G3/2 | every W |
  | E1/2 alone | 4 (Hurwitz) or 8 (Lambda) | W = 1 only (the split never rounds: n = 4 (a - b + J) + s); the wall |

**1.3 Both trains on the act's own gear, at every W (MEASURED, part 3, twice).** One Node-clock, step.gear and
step.split as built, the dial D = 2 W standing, the push J = (C - 2 W) a with C = SUM_g L(g) M L(g)^T for a drawn whole
M (a coupling that turns with the 48; a non-lift fails it, below), the 48 acting by (a, b, s) -> (P a, P b, P s,
flipped on a negated gear):
- 8-gear (G3/2): turned run = run turned 144 of 144 (48 lifts x 3 starts, 6 rounds each) at each W = 1, 2, 3, 5, 6, 9,
  12, 42, 600,000,000 (the click world's rest, 6 den Gamma^2 at den 1, Gamma 10^4) and 90,977,140,554,674,334,000,000
  (the example universe's rest); the run back by the mirror (b, a, -1 - s) exact 3 of 3 at each.
- 24-gear (E1/2 + E5/2 + 2 G3/2): 96 of 96 (48 lifts x 2 starts, 4 rounds each) at W = 1, 5, 6, 9, 42,
  600,000,000; run back 2 of 2.
- The no, on the same act: a signed permutation that is no lift (each lift with two gears swapped): 0 of 144 (8-gear)
  and 0 of 96 (24-gear) at W = 6. Spin 1/2 alone on Hurwitz's 4 gears (the 24 lifts that need no r2, whole matrices in
  the basis (1 + i + j + k) / 2, i, j, k, 2 of them signed permutations; a spring of 1; counts compared, tooth laid 0
  and not turned, a lenient test): 5, 10, 12, 6, 12, 14, 10 of 120 at W = 2, 3, 5, 6, 9, 12, 42, at most 2 of 24
  lifts holding at every start; 120 of 120 at W = 1 only, where the step n = -4 b is exact and nothing rounds.
- Where my measurement overturned my first run: the Hurwitz control first used the spring 2 W and held 120 of 120 at
  every W: at k = 2 W the quarter mode is exact (q+ = q j, ONE_ALGEBRA 0) and the carry never rounds, so the control was
  empty; with a spring of 1 it fails as above. Its W = 1 row is empty the same way.
- On a board (probe_half_board.py, twice, byte-identical): 3 x 3 x 3 Node-clocks, the Mesh pull at grip 1 on every
  gear, the push (C - (W + 1)) a plus the pull, the sites turned about the centre by the lift's turn (24 distinct
  site maps from the 48): turned run = run turned 48 of 48 for the 8-gear train at W = 5, 6, 9, 600,000,000
  (4 rounds) and for the 24-gear train at W = 6, 9 (3 rounds); the run back exact at each; the no, a signed
  permutation not a lift, fails at each.
- **Where my measurement overturned my expectation:** the second control, a lift's gears with ANOTHER turn's sites,
  HOLDS at every W. With the pull kind-blind and the coupling on-site, nothing ties the half-speed gear's turn to the
  board's: the train's lifts and the board's turns are separate symmetries, as for any train no gradient-leg table
  reads (tonight only the gradient vertex, FRAMES 7, ties a whole-speed train's rows to the axes). On the board the
  half-speed train is an inner hand until a table with a gradient leg, half x T1 -> half (the hopping), ties them:
  OPEN (section 4).
- Not measured: the engine's step.act with a loaded half-speed train (the loader cannot lay one: section 2).

**1.4 The full turn and the 48 on the board (DERIVED).** The board's sites and every whole-speed train turn by the
24 (the lift's turn pi(g)); a half-speed train turns by the lift L(g); g and -g turn the board alike and the half-speed
trains oppositely. Where every table is 48-invariant, a table with an odd count of half-speed legs sums to 0 over g and
-g, so the act commutes with the full turn: -I on the half-speed rows (teeth flipped), I elsewhere. The sign is the
board's: a superselection kept by the act, read by nothing (the physicist's item 10 stands). The mirror (b, a, -1 - s)
on the half-speed rows (even rows) commutes with every L(g) (checked by hand on a negated gear: both orders give
(-b, -a, s)), so the run back is the act's own (hypothesis (d)), no Kramers T in it.

**1.5 The pick, and the wall that stays.**
- Pick: **G3/2 on the 8-gear train** (cosets of C6): alone, no price, every W, no new carry, no compare, no if.
  **E1/2 + E5/2 on the 24-gear train** (units mod sign): every W likewise, at the named price of its company (two G3/2,
  which light mixes with the doublet: FAMILIES4's minors, the leak 758, 457, 367 thousandths under the train's table);
  the owner's "No price is allowed" (FAMILIES4, 18:1x) stands against laying it as the electron.
- The wall (OPEN): spin 1/2 alone on 4 or 8 gears. By 1.2 no signed-permutation form exists at any W, so the per-gear
  carry cannot carry it in any basis; a fixed-dial carry exists only at gcd(W, 6) = 1 and only as a table (ONE_ALGEBRA
  1, as RECHECK narrows it); the quotient-dependent carry turns at every W but compares 24 images (qa_math, 480 of
  480; MIRACLES row 11). Every dial the load makes, W = 6 den Gamma^2 + k0 c00 with k0 = Spokes x senses = 12, is
  divisible by 6, so every Node-clock tonight stands on the wall for any fixed dial. A compare-free, table-free rule:
  none known, none proved impossible.

## 2. The loader and the files: the changes for line 90's eight kinds (for the code writer; no code here)

Laws kept by every item: no number beyond 0 and 1 in src (48, 24, 8, 6 come from the closure and the coset counts, 2
is senses from the star), no table typed, no train declared in code, paths by joinpath, Rule3's carry the one division.

1. engine/kinds.py, the lifts: a new derivation from the star: the unit and the six Spokes as the six pure units; the
   two generators as the unit plus a Spoke (one r2 exponent, its norm senses) and the unit plus the three + Spokes
   halved by Rule3's carry at senses with remainder 0; closed under Hamilton's product (the 24's own T1 x T1 tables,
   FAMILIES3 CHECKED 20 of 20); each lift's turn found among the 24 by its sandwich (ONE_ALGEBRA 3: remainder 0, 24 of
   24). Out: the 48 as whole quaternions over Z[r2] (pairs), the product's index, each lift's turn index.
2. engine/kinds.py, the half-speed kinds: E1/2, E5/2, G3/2 as characters on the 48 in (p, q) pairs (q 0 but on the 12
   order-8 lifts of E1/2 and E5/2, +-1, opposite); the two trains' matrices as signed permutations built from cosets:
   the 8-gear on the cosets of C6 (the powers of a lift of order six: its cube -1, itself not -1), lam = (-1)^m on
   its m-th power; the 24-gear on the classes +-h, L(g) e_[h] = sign x e_[gh]. The five whole-speed kinds evaluated
   on the 48 through each lift's turn. Field names e1_2, e5_2, g3_2; the label rule reads the underscore as "/"
   ("E1/2", "E5/2", "G3/2").
3. main.made: passes the lifts and the half-speed kinds with the five; the five's tables c stay as built on the 24
   (were they summed over the 48, c would double and the primitive row u would not change).
4. runner/files.py, vocabulary and held_departures: eight labels; "none of the 24's kinds" becomes "none of the 48's";
   the whole-basis check moves from the kind to the train for a half-speed kind: a train holding a half-speed kind
   is admitted only if its character (part x the sum of its kinds' on the 48) has no r2 part, is -I on the full turn
   and equals the 8-gear train's (kinds ["G3/2"], part 2) or the 24-gear train's (kinds ["E1/2", "E5/2", "G3/2",
   "G3/2"], part 2); each other mix refused by name (a half-speed kind beside a whole-speed one in one train: its full
   turn is no sign; E1/2 without E5/2: "spin 1/2 rides only the 24-gear train, with its company").
5. The universe file names: such a train, by its labels and part 2, with its pinion at den; no new key; nothing else.
   The setting file's component of a half-speed gear is its coset's index in the lifts' order.
6. runner/load.py, trains_of: characters on the 48; a half-speed train is not the square, not the held hand, and
   **untied** in this build (the tie through the held hand's k shares k with whole-speed ties, NOT_CLOSED 8, g3_math
   item 4); gripped like any matter train (the Mesh pull), its rows on the force's path (T_d = 1), so it sources the
   metric's push as matter does (sigma_in sigma_out is kept by a flip: -m - 1 splits to -sigma).
7. runner/load.py, lay: the train's rows are its cosets (8 or 24), laid from item 2's matrices, not from kind
   components and parts.
8. runner/plans.py, pairs_of: a half-speed train's form onto A1 is its own kept form, the primitive row of
   SUM_g L(g)^T L(g) = the dot on its gears (FAMILIES3: the anchor's tie is the norm, kind-blind); so its passing
   (term 11) is SUM_i x_i J_i(y) - y_i J_i(x). No half-speed table in this build: half x half -> whole and
   whole x half -> half (the I-averaged table, FAMILIES3 item 3) are OPEN; meshing gives 0 by itself (an odd count of
   half-speed legs has no A1 channel).
9. runner/run.py and record/schema.py: schema 1.4 (one ADDED entry, a field no reader needs): the header's lifts (the
   48 with each one's turn index) and the three half-speed kind cards, their characters on the 48 as (p, q) pairs; the
   five cards unchanged on the 24. The decoder must accept 1.4 (its four readings use no kind card): the code writer
   checks the reader's minor rule.
10. Tests, each with its no: the classification (two trains only; part 2 of the probe); turned run = run turned for the
    48 at W including the loaded rest 6 den Gamma^2, and the no (a signed permutation not a lift); the run back exact
    on a world laid with a G3/2 train, on step.act through the loader; a board of several sites turned with the Mesh
    pull (owed: 1.3); the refusals of item 4 by name.

## 3. The clicks (one line each, as the Boss asks)

- (a) Interference (one half-speed quantum on two paths, one turned once: the fringes flip, and return after two
  turns): OPEN; decoder verdict NOT READ (decoder/shadow.py holds no two-path reading, and no record holds a
  half-speed train until section 2 is built); owed: two click-world readings of the flip and of the return.
- (b) Like clicks (the determinant for two like half-speed quanta, the permanent for whole-speed ones, a hand per
  quantum, FRAMES 12): OPEN; decoder verdict NOT READ (term 12's draw and the like-click weighing are not built; one
  train per quantum is what item 5 lets a file lay); owed: two click-world readings, never two at one place against
  bunching.

## 4. What stays OPEN (one line each)

- The compare-free, table-free carry for spin 1/2 alone on 4 or 8 gears: none known, none proved impossible (1.5).
- The electron: spin 1/2 lays only with its company (1.2), against the owner's "No price is allowed".
- A refusal that acts: only with a second hand (FAMILIES4's theorem); a hand per quantum is FRAMES 12's road.
- The tie of the half-speed turn to the board's (a half x T1 -> half table on the gradient, the hopping): without it
  the gear's 48 and the sites' 24 act apart (1.3, measured); its form and whether it rides the carry: not derived.
- The half-speed tables (the I-averaged vertex) and the half-speed tie to the held hand: not derived here.
