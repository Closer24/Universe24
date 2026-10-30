# G5, the split click's draw: a pointer the act reads alike both ways of time

David, 2026-10-30 (the second text 14:xx UTC), on Sofer's ask (#2187 6518975579, item 3: "the build has held no beat
count since G1b ... so the draw needs a source for c on the act. Which gear's tooth or sum is c is yours and David's
to name") and the owner's word of 11:1x UTC (derive what the Node-clock needs to close; everything to stand with a
hostile mathematician and a hostile physicist). It reads the act as built on main (0df0e8385), in the law's four
layers (Postulate 4, item (10)). The first text (toys-5 19b341c9b) went to a hostile mathematician and a hostile
physicist, who refused it with eight items and nine, folded here (section 8). The probe,
derive/david_open/node/g5_draw.py, is rebuilt for this text; its output g5_draw.txt is beside it, whole numbers alone,
about 35 s.

**The finding in one line:** the draw's pointer is the round's own fine teeth, each counted from the middle of its
turn, read as the round takes them in and as it gives them out, summed over the Node-clock and its six neighbours and
folded to a half turn. The mirror turns that sum's sign, so the backward act reads the same pointer and undoes the same
draw (64,800 of 64,800 draws on the act). Ranked by size, the parts are drawn by their sizes within the pointer's
measured spread, below 3 x 10^-3 here. The pointer moves only where a scalar gear moves: at a merge where light alone
crossed it stands still, and there the draw is not fair (OPEN, the heaviest item).

## 1. In clocks

- **The dust.** Every gear's turn leaves the part of a tooth that did not make a whole one: its fine tooth, kept for the
  next turn. The pushes move it every round, the Meshes' pull by whole sixths of a turn (the teeth are six grips), the
  coupling by finer steps.
- **The split.** Two twins share a winding that completes, and neither holds it whole. The Node-clock must say which
  twin takes it. Under form B (decision 28's two boards) that is said at the birth and at every merge of the backward
  pass, not at the click (CLICKS-CLOSED, section 13; TENSOR24_NODE.md 4.5).
- **The pointer.** The Node-clock reads the fine teeth of its scalar gears twice, as the round takes them in and as it
  gives them out, each counted from the middle of its turn, and sums them over itself and its six neighbours (so a Mesh
  carries fine teeth as well as counts). Where that sum stands within one turn, folded onto a half turn, is the
  pointer.
- **Both ways of time.** Run backward, the round takes in what it gave out, and every tooth counted from the middle
  turns its sign. So the sum turns its sign, and the folded pointer stands where it stood: the backward act draws the
  same twin and takes back the same record.
- **The share.** The twins share the half turn by their sizes, the larger first, and the twin whose share holds the
  pointer takes the whole winding.
- **No dial.** The node holds no count (G1b): no round, no beat, no time. Where the scalar gears move, the dust moves
  more than a dial would.
- **Where nothing moves.** At a merge where light alone crossed, no scalar gear moves: light is a vector train, whose
  teeth the pointer does not read, and matter and the held count stand still there. The pointer stands still, and the
  same twin takes every winding. The draw is not fair there (OPEN).

## 2. In the algebra

**The rule.** At a drawing Node-clock x, for the round from s_in to s_out = tick(s_in), with W the teeth that round's
carry used at every row the pointer reads (one W, asserted by the probe) and H = W div 2:

    c(r) = 2 r + 1 - W, a fine tooth counted from the middle of its turn
    P = the sum, over x, its six neighbours and every A1 row, of c(r_in) + c(r_out)
    u, from carry(P, W, 0): u = P - W (P div W);  e = min(u, W - u), within [0, H]
    the parts ranked by size, the larger first, ties in their given order; C_j the cumulative size, L the total
    the part drawn: the first ranked j with e L < C_j H; the last ranked part at e = H

One carry for u, and one comparison of two products per part. No count, no dial, no gcd, nothing held. A1 rows alone:
an A1 row's fine tooth is the same under all 24 turns, so P is.

**The mirror** (DERIVED; CHECKED on the act, probe (e)). The mirror swaps the two slots and flips each fine tooth to
W - 1 - r, and c(W - 1 - r) = -c(r). The backward act's round runs from m = mirror(s_t) to m_out = tick(m) =
mirror(s_(t-1)), so it reads r_in' = W - 1 - r_t and r_out' = W - 1 - r_(t-1): P' = -P, u' = W - u (or 0 at u = 0),
and e' = e. The sizes are read in the input's now slot both ways: s_(t-1)'s forward, and m's backward, which is s_t's
before slot, the same slot by the leapfrog (b+ = a). So the backward act draws the same part. Conditions: one W at
every row the pointer reads, as on the probe's board. On N2's board the rows carry at different teeth; the negation
still holds row by row, each tooth counted at its own row's teeth, and the fold needs one modulus both directions read
alike (OPEN there).

**The lemma** (DERIVED). Let X = c(r_out) for one A1 row at x, and p its pitch: the gcd of every teeth the row carried
at and every move its fine tooth made, so r_out stands on a progression of step p in [0, W), with W / p even. Write
Y = P - X. Suppose that, given Y and the sizes, r_out is spread evenly over its progression. Then for every part,
however large L is,

    | P(part i | Y, sizes) - sigma_i / L | <= 4 p / W.

Proof. Given Y, 2 r_out mod W is spread evenly over a progression of step 2 p, and u over a shifted copy of it,
W / (2 p) points. Part i is drawn when e falls in an interval of [0, H] of length sigma_i H / L, that is, when u
falls in that interval or in its reflection about H: two intervals of [0, W), of total length sigma_i W / L. A
progression of step 2 p holds within 1 of (the length) / (2 p) of its points in each, so within 2 of
sigma_i W / (2 p L) in the pair, out of W / (2 p): within 4 p / W of sigma_i / L. Averaging over Y and the sizes
keeps the bound.

The hypothesis carries the physics (the analogue of quantum equilibrium; Durr, Goldstein and Zanghi, J. Stat. Phys. 67,
843 (1992)), and no finite record can show it: 4 p / W is the fold's resolution under it, not a measurement.

**What a finite record shows.** For fixed sizes, with D_N the star discrepancy of e / H over the N draws,
|freq(part i) - sigma_i / L| <= 2 D_N, with no hypothesis: part i's draws are those with e / H in an interval of length
sigma_i / L.

**Why decision 29's form falls short** (d = (c + V) mod L with V the sum of the seven Node-clocks' digits r div p,
part = SUM_i nonneg(d - S_i)):

- **The span.** V stays below 35 W / p, p the finest pitch. A size as a norm of counts, squared on two boards,
  reaches 10^28 at swings of 10^7; when L is past V's top, d = V and every draw falls in the first parts.
- **The dial.** With c a beat count and V standing still, a part is drawn exactly its size's times over L beats
  running at one Node-clock: an alternation, a partition noise below the binomial. The reason to strike c is G1b,
  not nature: the dial shows only where V stands still, and there it was the only pointer that moved.
- **Read raw**, as the first text read it, the sum also fails by the pitch (every pitch here even, so V is even); that
  is the raw sum's failure, not decision 29's.
- The fold gains: no pitch read at load (a gcd that G3's strengths change), no span limit, no dial.

**Ranked by size, and the tie.** The cumulative sizes need an order of the parts, alike on every turned board. Ranked
by size it is. At a tie the given order decides, and on a state that a turn fixes while exchanging the parts no draw
built from A1 teeth alone is covariant: the tie breaks the 24 (named; OPEN). The part a given e picks depends on all the
sizes and their order: the pointer is a contextual hidden variable, as every deterministic draw must be (Kochen and
Specker, J. Math. Mech. 17, 59 (1967)).

**The pitch is the strengths'.** With the plan empty every push is a multiple of the grip, and every fine tooth takes
6 values. Term 6's strengths make the pitch small: on G3's probe numbers, 4 on matter and 2 on the held count. So G3's
strengths owe one condition to the draw: a pitch small against W at the rows the pointer reads.

## 3. On the board

What the event board's counts do (g5_draw.txt). The board: 6 by 6 by 6 Node-clocks; light, matter (two parts each)
and the held count, all A1 on this board; W = 6 grip. Term 6 at G3's probe strengths: g = 227442851386684,
kappa = 5686071284667145875000, lam = 4548860, the least whole multiple of 4 with 2 kappa lam >= g^2. Rounds 21 to 420
read, 86,400 draws. Every number below is the pointer at every Node-clock in every round, a stand-in for the draws a
split click would make: no split click is built on the act.

- **The pitch** (probe (a)): with the plan empty, the grip on all three trains (6 values); with term 6, light the grip,
  matter 4 and the held count 2.
- **The pointer** (probe (b)): 86,400 distinct values of e in 86,400 draws. Every e is 2 more than a multiple of 4 (P is
  70 plus twice a sum of moves, each a multiple of 2, 4 or the grip), so e is never 0 or H. The chi-square of e's
  tenths is 8.096 on 9; in one half two rounds running 497 per mille, one Mesh apart 498 (500 for independent draws).
  The star discrepancy D_N of e / H is 3,521 ppm, so 2 D_N = 7,042 ppm; root(N) D_N = 1.035, against the Kolmogorov
  law's mean 0.869 and its 5 per cent point 1.358 for independent uniform draws.
- **Born at five splits** (probe (c)), part 0's count, z^2 against the binomial:

  | S1 : S2 (expected) | (i) the pointer e, ranked | (ii) the raw sum mod L | (iii) decision 29's digits | (iv) its digits and dial |
  |---|---|---|---|---|
  | 1 : 1 (43,200) | 43,122, z^2 0.281 | 86,400, z^2 86,400 | 43,371, z^2 1.353 | 43,103, z^2 0.435 |
  | 1 : 2 (28,800) | 28,925, z^2 0.813 | 28,657, z^2 1.065 | 28,983, z^2 1.744 | 28,791, z^2 0.004 |
  | 3 : 7 (25,920) | 26,021, z^2 0.562 | 34,391, z^2 3,954.907 | 25,932, z^2 0.007 | 26,035, z^2 0.728 |
  | 10^6 : 3 x 10^6 (21,600) | 21,809, z^2 2.696 | 21,611, z^2 0.007 | 21,767, z^2 1.721 | 21,770, z^2 1.783 |
  | 10^30 : 3 x 10^30 (21,600) | 21,809, z^2 2.696 | 86,400, z^2 259,200 | 86,400, z^2 259,200 | 86,400, z^2 259,200 |

  The largest |freq - share| of column (i) is 2,418 ppm, within 2 D_N at every split. The two largest splits draw
  alike under (i), since ranking puts part 0 in the same upper quarter of the half turn for both. With the sizes read
  from the state (S1 = m_re^2 + 1, S2 = m_im^2 + 1 at x in s_in's now slot): 42,774 against 42,802 expected, z^2 0.073,
  4 ties.
- **Six lays** (probe (d)): the chi-square of e's tenths 8.096, 12.572, 6.304, 5.974, 16.203 and 4.112, mean 8.876,
  against the null's mean 9 with a spread of 4.242 for one lay and 1.732 for the mean of six; z^2 at 1:1 0.281, 0.655,
  0.020, 0.311, 6.685 and 0.125. The fifth lay's 6.685 lies just past the 1 per cent point of one degree of freedom,
  6.635; one lay in six that far out has a chance near 6 per cent (1 - 0.99^6).
- **The run back inside the act** (probe (e)): 300 rounds out from the old lay with a draw at every Node-clock, each
  adding 1 to its books; then, for t = 300 down to 1, m = mirror(s_t), m_out = tick(m), the same draw from (m, m_out),
  taking 1 from the books. The pointer is equal at 64,800 of 64,800 draws; the part at 64,800 of 64,800 at 1:1 and at
  64,800 of 64,800 at the state's sizes (2 ties); the books end all 0 under both; s_(t-1) is recovered bit for bit at
  300 of 300 rounds, equal to the engine's untick at 300 of 300; the lay returns bit for bit. The control, the first
  text's d = V mod W on the raw teeth after the tick, read the same way: 32,358 of 64,800 equal, chance, with 424 of its
  432 book entries not 0.
- **The 24** (probe (f)): every turn of the cube, rounds 1 to 5 (1,080 draws a turn), the split between x's +x and -x
  neighbours with sizes m_re^2 + 1 there. The act turns with the board in 5 of 5 rounds, and e is equal at the image.
  Ranked by size the draw is covariant at 1,080 of 1,080 under all 24 turns, with no ties. In the given order (+ side
  first, not ranked) it is covariant at 1,080 under the 12 turns taking +x to a + direction and at 658 under the 12
  taking it to a - direction; with sizes 1 and 1, all ties broken in the given order, at 1,080 and at 0.
- **The vacuum** (probe (g); the first reading's hostile physicist's lay): term 6, light laid moving at every
  Node-clock, matter at rest at 0 and the held count at rest at n, 400 rounds. Matter and the held count are still at
  rest at the end. With light read as T1, as in the theory, so outside the pointer: e is frozen at 42 at every
  Node-clock in every round, and a 1:1 split draws part 0 in 86,400 of 86,400. With light's rows counted in the pointer,
  as this board's A1 trains: light's fine teeth take 6 values on the grip's lattice, e at most 3, and a 1:1 split draws
  part 0 in 28,757 of 86,400, about a third.
- **The two hardest lays** (probe (h)), the held count laid at n:
  - a hot board, matter laid to 10 counts, all 216 Node-clocks: 86,400 distinct e of 86,400; the chi-square of the
    tenths 12.523 on 9; the joint tenths one round apart 81.334 on 81, two apart 74.049 on 81; at 1:1 43,299 (expected
    43,200), z^2 0.453. (The first reading's physicist found 259.870 on 81 one round apart for the first text's d on
    this lay: the pointer read in and out removes that dependence at this test.)
  - a cold board, one packet near 100 counts, its 27 Node-clocks: 10,800 distinct e of 10,800; 14.979 on 9; one round
    apart 96.609 on 81, two apart 88.443 on 81; at 1:1 5,309 (expected 5,400), z^2 3.067. Each lies on the high side,
    none past its 5 per cent point (16.92 on 9, 103.0 on 81, 3.84 on 1); the 27 Node-clocks' sums share Meshes.
- **Decision 29's dial over a full turn** (probe (i)): the plan empty, 1,000 rounds, L = 1,000, sizes 500 and 500. V mod
  1,000 is 0 at every Node-clock in every round. The dial, d = (t + V) mod 1,000, draws part 0 exactly 500 times at
  each of the 216 Node-clocks; with c struck, part 0 in 216,000 of 216,000. Where V stands still the dial gives Born by
  alternation, and the struck rule gives the same part every time.

## 4. In the clicks

The physics is read after the clicks, on the record, never on the board. The draw reaches the record only as which part
took the quantum. No split click is built on the act, so what follows is what its records must read; it is owed with
the split click itself (G5's code, beside term 11's click tooth).

- **Born's rule, half of it.** Over many splits, part i takes the quantum with frequency sigma_i / L, within the
  pointer's spread, wherever a scalar gear near the draw moves. On one board no departure is seen above 3 x 10^-3 (the
  largest 2,418 ppm, against 2 D_N = 7,042 ppm at 86,400 draws). The other half, that the sizes are the amplitudes
  squared, is the sizes' item (section 7), with the bound on higher-order interference as its test (Sinha and others,
  Science 329, 418 (2010)).
- **Independent trials, in scope.** Binomial partition is what nature shows for single quanta entering by one port: the
  shot noise 2 e I (1 - T) of a quantum point contact (Reznikov and others, PRL 75, 3340 (1995); Kumar and others, PRL
  76, 2778 (1996)). The board's tests (the tenths, the halves one round apart, the joint tenths one and two rounds
  apart, six lays) are consistent with independent draws at those tests; no standard battery was run. Two
  indistinguishable quanta entering by two ports are one draw over two-quantum outcomes, with the Hong-Ou-Mandel dip as
  its test (Hong, Ou and Mandel, PRL 59, 2044 (1987)): OPEN.
- **No signal, as far as the pointer is fair.** The part drawn is a function of e and the sizes, and the sizes carry
  both settings back to the birth (decisions 28 and 29). So a far setting moves no click only while the pointer is
  spread: a deterministic draw that reproduces nonlocal correlations keeps no signal only in equilibrium (Valentini,
  Phys. Lett. A 156, 5 (1991)). With the pointer frozen at 3/10 of the turn, the singlet gives Bob's click one sign at
  30 degrees and the other at 60 (the first reading's physicist's g5_signal). The frozen pointer at vacuum merges is a
  no-signal item as well as a Born item.
- **The split is nonlocal.** One particle split across two places is nonlocal too (Guerreiro and others, Phys. Lett. A
  376, 2174 (2012); Fuwa and others, Nat. Commun. 6, 6665 (2015)), and Kochen and Specker's contextuality is tested
  (Kirchmair and others, Nature 460, 494 (2009); Lapkiewicz and others, Nature 474, 490 (2011)). Every split whose parts
  are apart, one particle or two, stands on the two boards (decision 28), not on the pointer alone.
- **Gravity follows the outcome** (Page and Geilker, PRL 47, 979 (1981)). The draw writes no fine tooth r and no drive
  tooth r_d. If the losing parts' shares stay on the board, term 5 sources the 00 slot from their strides and gravity
  follows the spread wave, which Page and Geilker refute. The gathering of the losing shares is a condition of this
  page, OPEN (CLICKS-CLOSED, section 13).
- **Departures, named:** the frozen pointer at merges where light alone crossed (Born and no signal fail there); the
  tie (the 24 broken there); the draw's resolution 4 p / W under the lemma's hypothesis; the run back on N2's board, its
  rows at different teeth.

## 5. Measured (g5_draw.txt)

| Check | Result |
|---|---|
| (a) the pitch, plan empty and term 6 | the grip three times; the grip, 4 and 2 |
| (b) the pointer, 86,400 draws | all distinct; chi-square 8.096 on 9; 497 and 498 per mille; D_N 3,521 ppm, root(N) D_N 1.035 |
| (c) Born, the pointer ranked by size, five splits | z^2 0.281, 0.813, 0.562, 2.696, 2.696; the largest gap 2,418 ppm, within 2 D_N |
| (c) the raw sum, decision 29's digits, with its dial | the pitch fails the raw sum at 1 : 1 and 3 : 7; the span fails all three at 10^30 : 3 x 10^30 |
| (d) six lays | mean chi-square 8.876 against 9; z^2 at 1:1 from 0.020 to 6.685 |
| (e) the run back inside the act, 300 rounds | e and the part equal at 64,800 of 64,800; the books 0; the lay returns; the control at chance |
| (f) the 24, ranked by size | covariant at 1,080 of 1,080 under every turn; a tie in the given order at 0 under 12 turns |
| (g) the vacuum, light as T1 | e frozen at 42; a 1:1 split draws part 0 every time |
| (h) the hot and the cold board | lag 1: 81.334 and 96.609 on 81; z^2 0.453 and 3.067 |
| (i) the dial over a full turn, plan empty | exactly 500 of 1,000 at every Node-clock; c struck: part 0 every time |

## 6. What stands (term 12's row for the architecture document)

- **Clock:** the Node-clock reads its scalar gears' fine teeth going in and coming out, each from the middle of its
  turn, summed over itself and its six neighbours and folded to a half turn; the twins share the half turn by size, the
  larger first, and the twin whose share holds the pointer takes the winding. No count, no dial.
- **Board:** c(r) = 2 r + 1 - W; P the sum of c(r_in) + c(r_out) over the seven Node-clocks' A1 rows; e =
  min(P mod W, W - P mod W); the part the first ranked j with e L < C_j H; nothing written in r or r_d.
- **Algebra:** the mirror negates P, so the backward act reads the same e (DERIVED, under one W at the rows read); the
  lemma's 4 p / W under its hypothesis; 2 D_N for a finite record.
- **Clicks:** Born's frequencies by the sizes within the pointer's spread where scalar gears move; binomial partition
  for single quanta at one port; no signal as far as the pointer is fair.
- **Home:** owed in code at G5, beside term 11's click tooth. **Status:** DERIVED, and CHECKED on the act on one board
  with term 6 at G3's probe strengths; the frozen pointer at vacuum merges, the tie and the split click itself OPEN.

## 7. OPEN

- **The frozen pointer at vacuum merges** (the heaviest): a pointer that radiation moves by a sizeable part of a turn
  between two draws there, or the draws moved to where matter moves, keeping form B's product law. A candidate named by
  the first reading's mathematician: the crossing phase of term 11's click tooth (k+ L against S_i |tau|), owed under
  the mirror.
- **The tie:** a pointer that turns with the parts, such as the split axis's centred T1 teeth.
- **The split click on the act**, with its record; Born and the partition noise read from its records, not from the
  pointer at every Node-clock.
- **The gathering of the losing shares** (Page and Geilker).
- **The run back on N2's board**, its rows at different teeth.
- **The sizes** (G5): the forward norm and the backward share, decision 28's form on the act; the sizes as the
  amplitudes squared.
- **Two quanta at two ports** (Hong-Ou-Mandel).
- **G3's strengths** set the pitch p.
- **The owner's word:** decision 29's d = (c + V) mod L becomes this pointer, c struck. The law's wording follows his
  word (Sofer's 6518975579).

## 8. What changed, by the first reading's items

**The hostile mathematician's eight:**

1. The lemma's hypothesis is completed (given Y and the sizes), the pitch counts every teeth the row carried at, and
   the probe asserts one W at the rows read (2).
2. 4 p / W is the fold's resolution under the hypothesis, not a measurement; the finite record's 2 D_N is stated and
   measured (2, 3, 4).
3. Decision 29's digits fall short by the span and the dial, not by the pitch; the raw sum's column is named as such;
   the fold's gains are named (2, 3).
4. The dial is read over a full turn (probe (i)); c is struck on G1b's ground; the frozen case is named in the clocks
   and the algebra (1, 2, 3).
5. The run back is the act on the mirrored state: the pointer from centred teeth in and out, which the mirror negates;
   the sizes read in the same slot; a draw with books; "writes no fine tooth r and no drive tooth r_d" (1, 2, 3).
6. The parts are ranked by size; the tie is named as a breach of the 24 (2, 3).
7. "No tooth is needed" holds where a scalar gear near the draw moves; the crossing phase of term 11's tooth is named
   for the frozen case (1, 7).
8. The statistics are read over six lays with the null's spread; "consistent with independent trials at these tests";
   "bounds" is dropped (3, 4).

**The hostile physicist's nine:**

1. Where the draw falls is named (form B's birth and merges); the frozen pointer at vacuum merges is measured on the
   act (probe (g)) and OPEN, the heaviest; "nothing is drawn" and "every motion moves the pointer" are struck (1, 3, 7).
2. No signal holds as far as the pointer is fair (Valentini) (4).
3. Section 3 is the board's; the split click and its records are owed (3, 4, 7).
4. The run back is read inside the act; the gathering and Page and Geilker are named as conditions (2, 3, 4).
5. The pointer is a contextual hidden variable; the parts are ranked by size; every split whose parts are apart stands
   on the two boards (2, 4).
6. Born holds within the pointer's measured spread, not to 4 x 10^-23 (2, 4).
7. Independent trials are scoped to one port, with Hong-Ou-Mandel OPEN; the dependence one round apart is measured
   (3, 4).
8. The citations: the quantum point contacts' shot noise; the random number generators are dropped (4).
9. c is struck on G1b's ground, and its cost at the vacuum merges is named (2, 7).
