# G5, the split click's draw: two clocks parting a winding, read by where their hands sit between teeth

David, 2026-10-30 (the third text, 16:2x UTC). It answers Sofer's ask (#2187 6518975579, item 3: "the build has held
no beat count since G1b ... so the draw needs a source for c on the act. Which gear's tooth or sum is c is yours and
David's to name"). It follows the owner's words:
- of 11:1x UTC: derive what the Node-clock needs to close, everything to stand with a hostile mathematician and a
  hostile physicist;
- of 17:3x UTC, through the Boss (6525992153, item 6): read the split click as two clocks parting a winding;
- of 16:4x UTC: energy and momentum are read in the clicks' spacetime, not on the board.

It reads the act as built on main (0df0e8385), in the law's four layers (Postulate 4, item (10)). The second text
(toys-5 dc795bc94) went to a new pair. The physicist refused it with nine items and the mathematician with fourteen.
Refused twice, it went to Big Pic first, and he found every blocking item standing (6526641319, item 3), with two
rulings folded here: the click writes nothing, and the parts are read in their own order. Asked through the Boss, he
named the draw's form (6527540022, item 8): the fold, in the parts' own order, with c struck. Section 8 lists how each
item is folded, and section 9 how the text checked itself (the owner's word of 16:2x UTC, 6527238774). The probe,
derive/david_open/node/g5_draw.py, is rebuilt for this text. Its output, g5_draw.txt, sits beside it: whole numbers
alone, with no root, about 100 s. G3's probe g3_held_hand.py (f) supplies the moving hands.

**The finding in one line:** the draw's pointer is the escapement's phase at the meeting. It is where the hand of every
A1 clock at the Node-clock and its six neighbours sits between its teeth, counted from the middle, read as the round
takes it in and as it gives it out, summed, and folded to a half turn.
- The mirror turns that sum's sign wherever the engine's promise holds. So the backward act reads the same pointer:
  64,800 of 64,800 draws, against a control at chance.
- The parts are read in their own order, with no rank (Big Pic). Each part is drawn by its size within its run's own
  spread: D_N from 1,969 to 4,779 ppm on six lays, 8,724 on the cold packet.
- The draw is fair only where the A1 hands it reads move by a sizeable part of a turn between draws. On the probe's
  board that is matter's rows, laid as A1. The held count at rest freezes it (86,400 of 86,400 draws to one part), and
  so does a merge where light alone crossed.
- G3's held hand, turning round at every Node-clock, never rests: its fine teeth move about 0.31 of a turn every round
  in vacuum. With the plan's strengths dividing W the pointer takes 8 values. A spring one count off that lattice still
  clusters it (the tenths at 9,406 on 9). A spring off it by about kappa over 10^6, its offset times the hand's swing a
  step of the lattice, passes the tenths, D_N and two of three splits, the third at z^2 4.063. So the moving hands
  exist, and the fair draw asks G3's strengths for a pitch fine at the hand's swing.
- The click writes nothing: the coupling passes the turns and the click counts them (Big Pic; term 11). A write the act
  cannot undo fails the run back, as the law's take does (0 of 300 rounds).
- OPEN: the strengths' pitch; the held hand read two ways, its fine teeth by the draw and its norm by G3's anchor (Big
  Pic, 6527540022 item 8); and the split click itself.

## 1. In clocks

- **Two clocks parting a winding** (the owner's word of 17:3x). A spread quantum is clocks joined: one winding shared by
  hands at several places, none holding it whole. The split click is where they come apart, and the winding goes whole
  with one of them. Under form B (decision 28's two boards) the parting is decided at the birth and at every merge of
  the backward pass, not at the click (CLICKS-CLOSED, section 13; TENSOR24_NODE.md 4.5).
- **The escapement** (Big Pic, 6526070842). Between two ticks a clock's hand sits between two teeth. The tick is whole
  and the hand is not: each gear keeps the part of a tooth its turn did not complete, its fine tooth, for the next turn.
- **The pointer.** The Node-clock reads where its A1 clocks' hands sit between their teeth, counted from the middle of
  the tooth. It reads them twice, as the round takes them in and as it gives them out, and sums over itself and its six
  neighbours, so a Mesh carries a hand's position as well as its counts. Folded onto a half turn, that sum is the
  pointer.
- **Both ways of time.** Run backward, the round takes in what it gave out, and each hand counted from the middle turns
  its sign. The sum turns its sign and the folded pointer stands where it stood: the backward act parts the same clocks
  the same way. This holds while every kept tooth stands below the teeth of the round that reads it, the engine's own
  promise, which only a falling clock breaks.
- **The share.** The parting clocks share the half turn by their sizes, in their own order, and the one whose share
  holds the pointer takes the winding. Nothing is ranked (Big Pic: a rank is a sort, which the law refuses).
- **The draw needs hands that move.** If the hands the pointer reads stand still between two partings, the pointer
  stands, and the same clock takes every winding.
  - On the probe's board matter's hands move, laid as A1.
  - The held count of the old reading, standing at rest, barely moves: its fine tooth moves about 10^16 a round against
    teeth near 9 x 10^22, so read alone it freezes the pointer.
  - Light's hands are not read (light is a vector, T1), and nature's matter is a half-speed clock (Big Pic's piece 1),
    not A1 either.
  - G3's held hand never rests: one winding at every Node-clock, turning round, so its fine teeth move at every merge,
    vacuum included. That is Big Pic's cure from above, measured below with its one condition.
- **The click writes nothing** (Big Pic). The coupling passes the turns between the clocks that part, and the click
  counts them (term 11; line 35 (4) as completed by the owner's word: the click counts where the two runs part). A write
  into the board that the same act cannot undo would break the run back.

## 2. In the algebra

**The rule.** At a drawing Node-clock x, for the round from s_in to s_out = tick(s_in), with T_row the teeth that
round's carry used at each row (read at s_in's now slot) and H = T_f div 2, T_f the fold's teeth (below):

    c(r) = 2 r + 1 - T_row, a fine tooth counted from the middle of its row's turn
    P = the sum, over x, its six neighbours and every A1 row, of c(r_in) + c(r_out)
    u, from carry(P, T_f, 0): u = P - T_f (P div T_f);  e = u + nonneg(u - H - 1) (T_f - 2 u), within [0, H]
    C_i the sizes of parts 0 to i in their own order, L the total
    part i is drawn when C_(i-1) H <= e L < C_i H; at the edge e = H, the last part of nonzero size in that order

- **Cost:** one carry for u, one sign bit for the fold, and one comparison of two products per part.
- **What it holds:** one sum, SUM c(r_in) over the seven Node-clocks' A1 rows, taken before their tick and closed with
  SUM c(r_out) after it, inside the one pass. Nothing else is held across rounds: no count, no dial, no gcd, no rank.
- **A1 rows alone:** an A1 row's fine tooth is the same under all 24 turns, so P is.
- **Sizes of 0:** a part of size 0 owns an empty interval and is never drawn, at the edge included (probe (r)).
- **The fold's teeth T_f:** the teeth of the row the lemma reads (below), at the round's now slot. On the probe's board
  every row carries at one W, so T_f = W.

**The mirror** (DERIVED; CHECKED on the act, probe (e)).
- The mirror swaps the two slots and flips each fine tooth in the teeth it was kept at, the before slot's. The backward
  act's round runs from m = mirror(s_t) to m_out = tick(m).
- Every row's round teeth are read at m's now slot, which is s_t's before slot, a_(t-1): the same teeth T_row as the
  forward round, read at s_(t-1)'s now slot.
- So r_in' = T_row - 1 - r_t. By the run back, s_(t-1) = mirror(m_out), so r_out' = T_row - 1 - r_(t-1).
- Since c(T_row - 1 - r) = -c(r) at the same teeth, P' = -P, u' = T_f - u (or 0 at u = 0), and e' = e.
- The sizes are read in the input's now slot both ways, the same count a_(t-1), and the parts' order is the same both
  ways. So the backward act draws the same part.
- **The condition** is the engine's promise at the round: r_(t-1) < T_row at every row read (step.py, the comment above
  weight()). Then r_out' stands within [0, T_row).
  - One W is not needed: rows at W, W, 2 W, 2 W and 3 W keep P' = -P, e' = e and the part at every draw (the second
    reading's mathematician, his M1, 25,920 of 25,920).
  - One W is not enough either: a moving clock that breaks the promise loses the identity at the rounds where it breaks
    (his M2).
- So the mirror's departure is the falling clock (G2's moving-clock condition), named. The fold needs nothing more than
  the promise, and the N2 board's item is struck from the mirror; it stays for the lemma's row, carried at the fold's
  teeth.

**The lemma** (DERIVED). Let X = c(r_out) for the lemma's row at x, carried at T_f, and p its pitch: the gcd of every
teeth the row carried at and every move its fine tooth made, so r_out stands on a progression of step p in [0, T_f).
Write Y = P - X. Suppose that, given Y and the sizes, r_out is spread evenly over its progression. Then for every part,
however large L is,

    | P(part i | Y, sizes) - s_i / L | <= 4 p / T_f when T_f / p is even, and 2 p / T_f when T_f / p is odd.

- **Proof, T_f / p even.**
  - Given Y, 2 r_out mod T_f is spread evenly over a progression of step 2 p, and u over a shifted copy of it:
    T_f / (2 p) points.
  - Part i is drawn when e falls in an interval of [0, H] of length s_i H / L. That is, when u falls in that interval or
    in its reflection about H: two intervals of [0, T_f), of total length s_i T_f / L.
  - A progression of step 2 p holds within 1 of (the length) / (2 p) of its points in each interval, so within 2 of
    s_i T_f / (2 p L) in the pair, out of T_f / (2 p) points. That is within 4 p / T_f of s_i / L.
  - Averaging over Y and the sizes keeps the bound.
- **T_f / p odd:** 2 is prime to T_f / p, so 2 r_out mod T_f runs over the whole progression of step p, T_f / p points,
  and the same count gives 2 p / T_f.
- **Checked exhaustively** for even teeth up to 32 (the second reading's mathematician, A3): the worst departure is
  3.000 p / T_f at T_f / p even and 1.428 p / T_f at T_f / p odd, inside both bounds.
- **What the lemma does not limit:** L. A share below 4 p / T_f has no guarantee, so the fold resolves the shares to
  4 p / T_f, where decision 29's digits had a limit on L instead.
- **The hypothesis** carries the physics: the analogue of quantum equilibrium (Durr, Goldstein and Zanghi, J. Stat.
  Phys. 67, 843 (1992)).
  - No finite record can show it, so 4 p / T_f is the fold's resolution under it, not a measurement.
  - It asks the row's fine tooth to move, given everything else, over its whole progression between draws. A row whose
    tooth moves by 10^-6 of a turn a round cannot meet it, and neither can a row whose teeth sit on a lattice of a few
    points (G3's probe (f)).

**What a finite record shows.** For fixed sizes, with D_N the star discrepancy of e / H over the N draws:
- |freq(part i) - s_i / L| <= 2 D_N for any number of parts, and <= D_N for two, since part i's draws are those with
  e / H in an interval of length s_i / L.
- This is a theorem, so a check of it cannot fail. What a record measures is D_N itself, run by run, against the
  Kolmogorov law for independent draws.
- With no root (ALGEBRA.md line 100): N D_N^2 has the mean pi^2 / 12, near 0.822, under the Kolmogorov law, and the
  5 per cent point 1.844, the square of 1.358, both written as whole thousandths in the probe.

**The draw's form** (Big Pic's answer through the Boss, 6527540022 item 8). His ruling read "one carry, d = (c + V) mod
L, read against the parts in their own order". Asked which form, he answered: one carry and no sort, not decision 29's
digits, which probe (c) breaks past V's top. So the form is this text's fold (u = P mod T_f, e against the cumulative
sizes in their own order), and c stays struck, since the pointer is the held hand's fine teeth, moved every round. The
record of why decision 29's form gives way:
- **Decision 29's form** (d = (c + V) mod L, V the sum of the seven Node-clocks' digits r div p, part = SUM_i
  nonneg(d - S_i)) has a span: V stays below 35 W / p, p the finest pitch. A size as a norm of counts, squared on two
  boards, reaches 10^28 at swings of 10^7, and when L is past V's top, d = V and every draw falls in the first parts: at
  10^30 : 3 x 10^30 its digits draw part 0 in 86,400 of 86,400 (probe (c)). The fold has no limit on L.
- **Its dial.** With c a beat count and V standing still, a part is drawn exactly its size's times over L beats running
  at one Node-clock: an alternation, a partition noise below the binomial. G1b struck c (the node holds no count), and
  Big Pic keeps it struck: the held hand's fine teeth move the pointer every round, so no dial is needed.
- **On the probe's lays decision 29's own digits do not stand still:** on the plan-empty lay V takes 86 values from 44
  to 130, at no Node-clock still, and the dial gives part 0 between 490 and 512 times of 1,000. Only on the vacuum lay
  does V stand, at one value, and there the dial gives exactly 500 (probe (l)).
- **Read raw**, as probe (i) reads it, the sum fails by the pitch: with the plan empty every tooth is a whole number of
  grips, so V mod 1,000 is 0 by arithmetic. That is the raw sum's failure, not decision 29's, and (i) is labelled so.

**The parts in their own order** (Big Pic's ruling).
- **No rank, no tie rule.** The parts keep the order they come in; a balanced split is no special case.
- **The 24 in the frequencies, not draw by draw.** A turn that reverses the split axis reverses the parts' order, so for
  the same e it draws the other part. Under the 12 turns keeping the split axis's sense the draw is covariant at 1,080
  of 1,080; under the 12 reversing it, at 658, and at 0 for equal sizes (probe (f)). Wherever the pointer is fair, each
  part is drawn at its share in either order, so the 24 hold in the clicks' frequencies. Ranked by size, the refused
  rule, the draw was covariant at 1,080 under every turn, and it picks a different part than the parts' own order in
  57,754 of 86,400 draws at 1:2 (probe (r)): the order changes which draw, not how often.
- **Contextual.** The part a given e picks depends on all the sizes and their order, so the pointer is a contextual
  hidden variable. Kochen and Specker's theorem (J. Math. Mech. 17, 59 (1967)) makes that necessary for a deterministic
  draw over three or more parts that reproduces quantum statistics. For two parts, noncontextual models exist (Bell,
  Rev. Mod. Phys. 38, 447 (1966)), and every split on the probe's board has two parts.

**The motion the draw needs.** The lemma's hypothesis asks the row's fine tooth to run over its progression between
draws.
- **The pitch is the strengths'.** With the plan empty every push is a multiple of the grip, and a fine tooth takes 6
  values. Term 6's strengths make the pitch small: on G3's probe numbers, 4 on matter and 2 on the held count.
- **A small pitch is not enough** (the second reading's physicist, item 1). The held count has pitch 2, yet at rest its
  fine tooth moves about 10^16 a round against W near 9 x 10^22. Read alone, it freezes the pointer (probe (j)).
- **Motion is not enough either** (G3's probe (f)). The held hand of G3's seventh text turns round at every Node-clock
  and moves its fine teeth by a median 0.312 of a turn each round. With the plan's strengths dividing W (kappa = W div
  16, the grip W div 6), the teeth sit on a lattice of 16 points and the pointer takes 8 values, the 3:7 split failing.
  The turning itself is not what moves the teeth: any A1 hand off its rest moves them as much, but the held hand is the
  one that never rests.
- **Off the lattice is not enough unless it is off by a step at the hand's swing** (G3's probe (f), at one phase). A
  spring kappa + delta moves a fine tooth by -kappa x - delta x each round: the first term stays on the 16 points, and
  the second moves it off them by delta x, x the part's count, at most the swing A = n = 10^6.
  - At delta = 1 the teeth stay within 10^-17 of a turn of the lattice: 10,797 distinct e of 10,800, yet the tenths at
    9,406 on 9 and the 3:7 split at z^2 293.6.
  - At delta near kappa over 10^6, delta A is a step of the lattice, W over 16: the tenths 11.753 on 9, D_N 11,213 ppm,
    z^2 2.739 and 2.216 at 1:1 and 1:3, and 4.063 at 3:7, between the 5 and the 1 per cent points.
- **So the condition the draw puts on the theory is motion on a fine pitch:** the A1 hands read must move by a
  sizeable part of a turn between draws, and the strengths must leave W's coarse lattices by a step of them at the
  hand's swing (delta A at least W over q, for a lattice of q points). G3's held hand supplies the motion at every
  merge; G3's strengths owe the pitch.
- **Term 5's push of the 00 slot by rho + 3 p** (TENSOR24_NODE.md section 3; light twice, decision 30) is another A1
  row a merge reads where light crossed; at gravity's strength it is not expected to move the 00 slot's tooth by a
  sizeable part of a turn.

**The click writes nothing** (Big Pic's ruling). The draw chooses a part. A write of the outcome into the board must be
undone by the same act on the mirrored state, with no list outside the state. Probe (k) measures each write:
- a whole count into the taker's now slot, or a record tooth that the mirror flips, comes back: the next round reads the
  count as the velocity's +k, mirrored it stands in the before slot as -k, and the same write cancels it;
- shrinking both slots of light's row along themselves (decision 29 (2), the law's take) leaves the velocity and moves
  the position, and mirrored the same write shrinks them again: 0 of 300 rounds come back.

So the click writes nothing: the coupling passes the turns between the parting clocks and the click counts them (term
11; line 35 (4) completed). The outcome is on the board as the coupling's passing, which the act runs back as itself.

## 3. On the board

What the event board's counts do (g5_draw.txt). The board: 6 by 6 by 6 Node-clocks; light, matter (two parts each)
and the held count, all A1 on this board; W = 6 grip. Term 6 at G3's probe strengths: g = 227442851386684,
kappa = 5686071284667145875000, lam = 4548860, the least whole multiple of 4 with 2 kappa lam >= g^2. Rounds 21 to 420
read, 86,400 draws. Every number below is the pointer at every Node-clock in every round, a stand-in for the draws a
split click would make. No split click is built on the act, and the draws fall only at births and merges; probes (p)
and (q) read the pointer where such draws would fall.

- **The pitch** (probe (a)): with the plan empty, the grip on all three trains (6 values); with term 6, light the grip,
  matter 4 and the held count 2.
- **The pointer** (probe (b)):
  - 86,400 distinct values of e in 86,400 draws.
  - Every e is 2 more than a multiple of 4, since P is 70 plus twice a sum of moves, each a multiple of 2, 4 or the
    grip. So e is never 0 or H.
  - The chi-square of e's tenths is 8.096 on 9.
  - In one half two rounds running: 497 per mille, z^2 2.541. One Mesh apart: 498, z^2 0.758. Both are below 3.84;
    independent draws give 500.
  - The star discrepancy D_N of e / H is 3,521 ppm, and N D_N^2 = 1.071, against the Kolmogorov law's mean 0.822 and
    its 5 per cent point 1.844.
- **Born at five splits** (probe (c)), part 0's count, z^2 against the binomial:

  | S1 : S2 (expected) | (i) the pointer e, own order | (ii) the raw sum mod L | (iii) decision 29's digits | (iv) its digits and dial |
  |---|---|---|---|---|
  | 1 : 1 (43,200) | 43,122, z^2 0.281 | 86,400, z^2 86,400 | 43,371, z^2 1.353 | 43,103, z^2 0.435 |
  | 1 : 2 (28,800) | 28,829, z^2 0.043 | 28,657, z^2 1.065 | 28,983, z^2 1.744 | 28,791, z^2 0.004 |
  | 3 : 7 (25,920) | 25,951, z^2 0.052 | 34,391, z^2 3,954.907 | 25,932, z^2 0.007 | 26,035, z^2 0.728 |
  | 10^6 : 3 x 10^6 (21,600) | 21,559, z^2 0.103 | 21,611, z^2 0.007 | 21,767, z^2 1.721 | 21,770, z^2 1.783 |
  | 10^30 : 3 x 10^30 (21,600) | 21,559, z^2 0.103 | 86,400, z^2 259,200 | 86,400, z^2 259,200 | 86,400, z^2 259,200 |

  - **Column (i):** every z^2 is below 3.84. The largest |freq - share| is 902 ppm, against D_N = 3,521 ppm. The
    binomial's standard error is 1,701 ppm at 1:1 and 1,473 at 1:3, so the splits resolve the shares to about
    5 x 10^-3: a departure below about 4,100 to 4,800 ppm would go unseen one time in five.
  - **The two largest splits** draw alike, since both put part 0 in the same first quarter of the half turn.
  - **With the sizes read from the state** (S1 = m_re^2 + 1, S2 = m_im^2 + 1 at x in s_in's now slot): 42,744 against
    42,802 expected, z^2 0.309.
- **The theory's pointer, light outside** (beside (b) to (d)):
  - the chi-square of the tenths 11.764, 11.747, 4.694, 6.751, 14.532 and 4.354 over the six lays, mean 8.973;
  - D_N from 2,345 to 4,193 ppm, and N D_N^2 = 0.475 on the first lay;
  - z^2 at 1:1 0.806, 4.111, 2.180, 0.044, 0.000 and 0.246, the second between the 5 and 1 per cent points;
  - at the five splits z^2 from 0.020 to 0.806, and at the state's sizes 0.301;
  - e still always 2 more than a multiple of 4.
  The conclusions stand with light out of the pointer, as the theory has it (light a vector).
- **Six lays** (probe (d)):
  - The chi-square of e's tenths is 8.096, 12.572, 6.304, 5.974, 16.203 and 4.112, mean 8.876, against the null's
    mean 9 with variance 18 for one lay and 3 for the mean of six.
  - Each lay's own D_N is 3,521, 3,698, 2,493, 2,496, 4,779 and 1,969 ppm, and its largest |freq - share| over the five
    splits 902, 2,627, 1,307, 949, 4,398 and 1,145 ppm, each inside its own D_N.
  - z^2 at 1:1: 0.281, 0.655, 0.020, 0.311, 6.685 and 0.125. The fifth lay's 6.685 lies just past the 1 per cent point
    of one degree of freedom, 6.635; one lay in six that far out has a chance near 6 per cent (1 - 0.99^6).
  - That 6.685 is exactly the halves' one-degree part of the lay's tenths chi-square 16.203; the remainder is 9.518 on
    8. It is one fluctuation, not two.
- **The run back inside the act** (probe (e)): 300 rounds out from the old lay with a draw at every Node-clock, then
  for t = 300 down to 1, m = mirror(s_t), m_out = tick(m), the same draw from (m, m_out).
  - The pointer is equal at 64,800 of 64,800 draws, and so is the part, at 1:1 and at the state's sizes.
  - The control, the first text's d = V mod W on the raw teeth after the tick, read the same way: 32,358 of 64,800
    equal, z^2 0.108, chance.
  - That is the test. What cannot fail is named as such: s_(t-1) recovered at 300 of 300 and equal to the engine's
    untick is the same computation as untick; the lay returning is the engine's bijection, since this draw writes
    nothing; the books ending at 0 follow from the parts being equal.
- **The click that writes, one act both ways** (probe (k)): 300 rounds out and back, a draw at each of the 216
  Node-clocks every round, each write made by the act on the state with no list read:

  | Write | Pointer equal (of 64,800) | Part equal | Rounds recovered (of 300) |
  |---|---|---|---|
  | a record tooth on the hand, flipped by the mirror (term 11's design) | 64,800 | 64,800 | 300 |
  | a whole count into the taker's now slot, matter's row | 64,800 | 64,800 | 300 |
  | a whole count into the taker's now slot, light's row | 64,800 | 64,800 | 300 |
  | both slots of light's row, the law's take | 64,800 | 64,800 | 0 |
  | both slots of matter's row | 0 | 48,274 | 0 |
  | a fine tooth moved by a grip, its quotient into the now slot | 39 | 48,282 | 0 |

  So the same pointer is necessary for the run back, not sufficient, and the click writes nothing (section 2).
- **The 24** (probe (f)): every turn of the cube, rounds 1 to 5, 1,080 draws a turn; the split is between x's +x and -x
  neighbours, with sizes m_re^2 + 1 there.
  - The act turns with the board in 5 of 5 rounds, and e is equal at the image.
  - The rule, the parts in their own order: covariant at 1,080 under the 12 turns taking +x to a + direction, and at
    658 under the 12 taking it to a - direction; at sizes 1 and 1, at 1,080 and at 0.
  - Ranked by size (refused, a sort): covariant at 1,080 under every turn.
- **The rows the pointer reads** (probe (j); the second reading's physicist, item 1), part 0's count at 1:1 and 1:3:

  | Lay | All five rows | Matter and the held count, no light | The held count alone |
  |---|---|---|---|
  | the old lay | D_N 3,521 ppm; 43,122 | D_N 2,345; 43,332 and 21,582 | D_N 2,202; 43,138 and 21,505 |
  | the hot board, matter to 10 counts | D_N 3,285; 43,299 | D_N 3,567; 43,017 and 21,491 | D_N 996,866; 86,400 and 86,400 |
  | the cold packet, its 27 Node-clocks | D_N 8,724; 5,309 | D_N 8,724; 5,309 and 2,662 | D_N 872,212; 10,800 and 10,800 |

  - Light dropped from the pointer changes nothing that matters.
  - The held count alone is at the edge on the old lay (lag-1 103.296 on 81, the 5 per cent point 103.0, where its
    swings reach 10^5). It is frozen on the hot board and on the cold packet, below a quarter of the half turn, so the
    first part takes every draw.
  - So on this board the fairness comes from matter's rows read as scalars.
- **The vacuum** (probe (g)): term 6, light laid moving at every Node-clock, matter at rest at 0 and the held count at
  rest at n, 400 rounds.
  - With light read as T1, outside the pointer: e is frozen at 42 at every Node-clock in every round, and a 1:1 split
    draws part 0 in 86,400 of 86,400. At e = 42, e / H = 9.2 x 10^-22.
  - With light's rows counted in the pointer (this board's A1 trains): e takes at most 3 values, and part 0 is drawn in
    28,757 of 86,400.
- **The held hand in vacuum** (G3's probe (f), a ring of 128, the merge at one Node-clock and its two neighbours on the
  ring, 10,800 draws):
  - the turning hand moves its fine teeth by a median 0.312 of a turn each round;
  - on the plan's strengths (kappa = W div 16, the grip W div 6) its teeth sit on a lattice, W / gcd(W, kappa) = 16, and
    the pointer takes 8 values, the 3:7 split at z^2 286;
  - with the held spring one count off it, kappa + 1: 10,797 distinct values, clustered on the lattice, the tenths
    9,406.448 on 9 and the 3:7 split at z^2 293.587;
  - with the held spring off it by about kappa over 10^6, kappa + 5,686,071,284,667,146, at one phase: 10,797 distinct
    values, the tenths 11.753 on 9, D_N 11,213 ppm, the joint tenths one round apart 69.554 on 81, and z^2 2.739, 2.216
    and 4.063 at 1:1, 1:3 and 3:7;
  - the standing count near rest, moved by a tied row at 10 (its tooth's move near this board's 10^16 a round), read
    alone, freezes it: 10,800 of 10,800 to one part.
- **The frozen merges' weight** (probe (o), form B's backward pass on a tree toward the source, CLICKS-CLOSED section
  13, rebuilt in whole numbers): the deciding merges where only light crossed the seven Node-clocks the pointer reads:
  - spread_quantum's own board: 1 of 3;
  - two detectors 10 Meshes out along +x and -x, or along +x and +y: 0 of 1 (the merge falls at the source);
  - two detectors at +z and at +6 x +4 z: 1 of 1;
  - a full screen: 0 of 399;
  - one pixel in four: 6 of 85;
  - sparse absorbers, one in about 100 Node-clocks: 50 of 66.
  With matter read as A1, which draws are fair turns with the apparatus's bearing to the board's axes. With the held
  hand at every Node-clock no merge is frozen, on the pitch's condition.
- **The two hardest lays** (probe (h)), the held count laid at n:
  - a hot board, matter laid to 10 counts, all 216 Node-clocks: 86,400 distinct e of 86,400; the chi-square of the
    tenths 12.523 on 9; the joint tenths one round apart 81.334 on 81, two apart 74.049; at 1:1 43,299 (expected
    43,200), z^2 0.453; D_N 3,285 ppm and the largest gap 1,909 ppm.
  - a cold board, one packet near 100 counts, its 27 Node-clocks: 10,800 distinct e of 10,800; 14.979 on 9; one round
    apart 96.609 on 81, two apart 88.443; at 1:1 5,309 (expected 5,400), z^2 3.067; D_N 8,724 ppm and the largest gap
    8,425 ppm.
  Each lies on the high side, none past its 5 per cent point (16.92 on 9, 103.0 on 81, 3.84 on 1); the 27 Node-clocks'
  sums share Meshes.
- **The partition noise** (probe (m)): the Fano factor of part 0's count over windows of 10 to 400 rounds at one
  Node-clock, 1:1 / 1:3 (1 for independent draws):
  - the old lay, 0.999 to 1.080 / 0.897 to 1.019;
  - the hot board, 1.008 to 1.086 / 0.918 to 0.999;
  - the cold packet, 0.854 to 1.094 / 0.709 to 1.050, on 27 to 1,080 windows.
  Every z^2 against the factor's own binomial spread is below 3.84: binomial within its error.
- **The draw where a click would fall** (probe (p), the first text's conditional test): the pointer read only at the
  rounds where a Node-clock's swept area crosses the key (10^10 W): 14,333 crossings; the chi-square of the tenths 5.580
  on 9; D_N 8,029 ppm; at 1:1 part 0 in 7,249 of 14,333 (expected 7,166), z^2 1.899; at the state's sizes z^2 0.728.
  With light outside: 8.031 on 9, D_N 6,869 ppm, z^2 0.242 and 0.109.
- **One Mesh and one round apart** (probe (q), the backward pass's step): the joint tenths of e at (x, t) and at
  (x + one Mesh, t + 1), along +x 74.281 on 81 (61.012 with light outside), over all six Spokes 93.450 (87.319); the
  same half one Mesh and one round on, z^2 1.710 and 0.193. On seed 4, the lay already high in its halves (6.685): along
  +x 87.964 (98.779), with the same half at z^2 4.402 (4.066), and 5.881 over the six Spokes, between the 5 and the 1
  per cent points.
- **Decision 29's dial** (probe (i), the raw sum, labelled so): the plan empty, 1,000 rounds, L = 1,000, sizes 500 and
  500. The raw V mod 1,000 is 0 at every Node-clock in every round, by arithmetic: every tooth a whole number of grips.
  The dial gives part 0 exactly 500 times at each of the 216 Node-clocks; with c struck, part 0 in 216,000 of 216,000.
  **On decision 29's own digits** (probe (l)): on the plan-empty lay D mod 1,000 takes 86 values, 44 to 130, and no
  Node-clock's D stands still; the dial gives part 0 from 490 to 512 times of 1,000. On the vacuum of (g), D takes one
  value at every Node-clock; the dial gives exactly 500 of 1,000 by alternation, and with c struck part 0 every time.
- **The rule's own checks** (probe (r)): the edge, e = H, goes to the last part of nonzero size in the parts' own order,
  and on size lists with zeros each part takes exactly its share on an even grid of pointers.

## 4. In the clicks

The physics is read after the clicks, on the record, never on the board. Energy and momentum are read in the clicks'
spacetime (the owner's word of 16:4x). The draw reaches the record only as which part took the quantum. No split click
is built on the act, so what follows is what its records must read; it is owed with the split click itself (G5's code,
beside term 11's click tooth). The board's numbers above are the stand-in, not the clicks.

- **Born's rule, half of it, under a condition.**
  - Over many splits part i takes the quantum with frequency s_i / L within each run's spread, wherever the A1 hands
    read move by a sizeable part of a turn between draws on a fine pitch.
  - On the probe's board those hands are matter's, laid as A1: five splits agree (z^2 0.043 to 0.281), to a resolution
    near 5 x 10^-3 at 86,400 draws.
  - In nature matter is a half-speed clock, not A1; G3's held hand supplies the motion at every merge, and the pitch is
    G3's strengths' to owe.
  - The other half, that the sizes are the amplitudes squared, is the sizes' item (section 7), with the bound on
    higher-order interference as its test (Sinha and others, Science 329, 418 (2010)).
- **Independent trials, in scope.** Binomial partition is what nature shows for single quanta entering by one port: the
  shot noise 2 e I (1 - T) of a quantum point contact (Reznikov and others, PRL 75, 3340 (1995); Kumar and others, PRL
  76, 2778 (1996)).
  - The board's partition noise is binomial within its error (probe (m)).
  - The board's tests (the tenths, the halves, the joint tenths one and two rounds apart, one Mesh and one round apart,
    six lays) are consistent with independent draws; no standard battery was run.
  - Two indistinguishable quanta entering by two ports are one draw over two-quantum outcomes, with the Hong-Ou-Mandel
    dip as its test (Hong, Ou and Mandel, PRL 59, 2044 (1987)): OPEN.
- **No signal, as far as the pointer is fair.** The part drawn is a function of e and the sizes, and the sizes carry
  both settings back to the birth (decisions 28 and 29). So a far setting moves no click only while the pointer is
  spread.
  - Pilot waves keep signal-locality only in equilibrium (Valentini, Phys. Lett. A 158, 1 (1991), Part II), and every
    deterministic hidden-variable theory does too (Valentini, Phys. Lett. A 297, 273 (2002)).
  - Measured (probe (n)), with Bob's analyser fixed and Alice's at 30 or 60 degrees from it: with e frozen at 3/10 of
    the half turn, the polarization singlet gives Bob - at 30 degrees and + at 60, so the far setting moves Bob's click,
    a signal; with e spread evenly, Bob + in 3,120 of 6,240 at both angles, and in 43,063 and 43,126 of 86,400 (z^2
    0.868 and 0.253) as the act spreads e.
  - For the spin singlet Bob draws - at 30 and at 60 degrees and + at 120: the second text's sentence holds for the
    polarization singlet, or for spin at 60 and 120 degrees, and is corrected so.
  - The frozen pointer is a no-signal item as well as a Born item.
- **The split is nonlocal.** One particle split across two places is nonlocal too (Guerreiro and others, Phys. Lett. A
  376, 2174 (2012); Fuwa and others, Nat. Commun. 6, 6665 (2015)), and contextuality is tested for three or more
  outcomes (Kirchmair and others, Nature 460, 494 (2009); Lapkiewicz and others, Nature 474, 490 (2011)). Every split
  whose parts are apart, one particle or two, stands on the two boards (decision 28), not on the pointer alone. A merge
  geometry like Guerreiro's (two detectors, one particle) is where the frozen merges must be read (probe (o)).
- **Gravity follows the outcome** (Page and Geilker, PRL 47, 979 (1981)). In their test the click set the lead masses
  and the balance followed them. The click writes nothing, so the outcome acts on the board only through the coupling's
  passing of the turns to the taker; whether the losing shares gather with it is a condition (CLICKS-CLOSED, section
  13), OPEN with term 11.
- **Departures, named:**
  - the draw unfair where the A1 hands read stand still, or sit on a coarse lattice: the held count at rest, the merges
    where light alone crossed (50 of 66 deciding merges with sparse absorbers, with matter read as A1), and the held
    hand on strengths on W's coarse lattice or within less than a step of it at the hand's swing;
  - the 24 kept in the frequencies, not draw by draw, under the turns that reverse the parts' order;
  - the resolution 4 p / T_f (2 p / T_f at odd T_f / p) under the lemma's hypothesis;
  - the falling clock, where the engine's promise and the mirror's identity break.

## 5. Measured (g5_draw.txt; G3's g3_held_hand.txt (f))

| Check | Result |
|---|---|
| (a) the pitch, plan empty and term 6 | the grip three times; the grip, 4 and 2 |
| (b) the pointer, 86,400 draws | all distinct; chi-square 8.096 on 9; D_N 3,521 ppm, N D_N^2 1.071 against 0.822 and 1.844 |
| (c) Born, the pointer in the parts' own order, five splits | z^2 0.281, 0.043, 0.052, 0.103, 0.103; the largest gap 902 ppm |
| (c) the raw sum, decision 29's digits, with its dial | the pitch fails the raw sum at 1 : 1 and 3 : 7; the span fails all three at 10^30 : 3 x 10^30 |
| (d) six lays, and light outside the pointer | mean chi-square 8.876 against 9; D_N 1,969 to 4,779 ppm; light outside: D_N 2,345 to 4,193 |
| (e) the run back, the test | e and the part equal at 64,800 of 64,800; the control 32,358 of 64,800 |
| (f) the 24, the parts in their own order | 1,080 under the 12 turns keeping the split axis's sense; 658 under the other 12 |
| (g) the vacuum, light as T1 | e frozen at 42; a 1:1 split draws part 0 every time |
| (h) the hot and the cold board | lag 1: 81.334 and 96.609 on 81; z^2 0.453 and 3.067; D_N 3,285 and 8,724 ppm |
| (i) the raw sum's dial, plan empty | exactly 500 of 1,000 at every Node-clock, by arithmetic |
| (j) the rows read | the held count alone frozen on the hot board (86,400 of 86,400) and the cold packet |
| (k) the click that writes | the record tooth and a whole count into the now slot: 300 of 300 rounds; the law's take: 0 of 300 |
| (l) decision 29's own digits | 86 values, the dial 490 to 512; the vacuum one value, exactly 500 |
| (m) the Fano factor | 0.709 to 1.094 over every lay, split and window; every z^2 below 3.84 |
| (n) no signal, frozen and spread | frozen: Bob's sign moves with Alice's angle; spread: 3,120 of 6,240 at both |
| (o) the frozen merges | 50 of 66 deciding merges with sparse absorbers; 0 of 399 on a full screen |
| (p) the conditional draw | 14,333 crossings; 5.580 on 9; z^2 1.899 and 0.728 |
| (q) one Mesh and one round apart | 74.281 and 93.450 on 81; on seed 4 the same half at z^2 4.402 and 5.881 |
| (r) the edge, and the refused rank | the edge never draws a part of size 0; the rank and the own order part at 57,754 of 86,400 draws at 1:2 |
| G3's (f), the held hand in vacuum | moves 0.312 of a turn a round; 8 values on W's lattice; one count off it, tenths 9,406 on 9; off it by a step at the swing, 11.753 on 9 and D_N 11,213 ppm |

## 6. What stands (term 12's row for the architecture document)

- **Clock:** two clocks part a winding where the escapement's phase at the meeting says. The Node-clock reads where its
  A1 clocks' hands sit between their teeth, going in and coming out, each from the middle, summed over itself and its
  six neighbours and folded to a half turn. The parting clocks share the half turn by size, in their own order, and the
  one whose share holds the pointer takes the winding. The click writes nothing; the coupling passes the turns.
- **Board:** c(r) = 2 r + 1 - T_row; P the sum of c(r_in) + c(r_out) over the seven Node-clocks' A1 rows; e the fold of
  P at T_f; the part the one whose interval, in the parts' own order, holds e L, the edge to the last nonzero part; one
  sum held in the pass.
- **Algebra:** the mirror negates P under the engine's promise, so the backward act reads the same e (DERIVED); the
  lemma's 4 p / T_f (2 p / T_f at odd T_f / p) under its hypothesis; D_N for a finite record of two parts.
- **Clicks:** Born's frequencies by the sizes within each run's spread where the A1 hands read move between draws on a
  fine pitch; binomial partition for single quanta at one port; no signal as far as the pointer is fair; the 24 in the
  frequencies.
- **Home:** owed in code at G5, beside term 11's click tooth. **Status:** DERIVED, and CHECKED on the act on one board
  with term 6 at G3's probe strengths, with matter laid as A1, and on a ring with G3's held hand. The draw's form is the
  fold, by Big Pic's word. OPEN: G3's strengths' pitch, the held hand read two ways (the draw its fine teeth, the anchor
  its norm), and the split click itself.

## 7. OPEN

- **The pitch** (the heaviest): G3's strengths, derived, leaving W's coarse lattices by a step of them at the hand's
  swing, so that the held hand's moving teeth spread the pointer at every merge; checked at one phase only.
- **The held hand read two ways** (Big Pic, 6527540022 item 8): the draw needs its turn, read in its fine teeth, and
  G3's anchor must not see the turn, so it ties through the norm (four squares). The two read different parts of one
  hand; that one hand serves both is OPEN with G3's anchor.
- **The split click on the act**, with its record; Born and the partition noise read from its records, not from the
  pointer at every Node-clock.
- **The coupling's passing of the turns** (term 11), and the gathering of the losing shares (Page and Geilker).
- **The falling clock:** the mirror's identity at the rounds where the promise breaks (G2's moving-clock condition).
- **The sizes** (G5): the forward norm and the backward share, decision 28's form on the act; the sizes as the
  amplitudes squared; the pointer's independence of the sizes at form B's sizes, untested.
- **Two quanta at two ports** (Hong-Ou-Mandel).
- **The owner's word:** decision 29's d = (c + V) mod L becomes this pointer, c struck, and decision 29 (2)'s take gives
  way to "the click writes nothing". The law's wording follows his word (Sofer's 6518975579).

## 8. What changed, by the second reading's items and Big Pic's word

**Big Pic's word** (6526641319, item 3): every blocking item stands. The frozen pointer has one root, no A1 row moving
between draws, and the held hand is its cure, measured here with the pitch's condition (2, 3). The click writes nothing
(1, 2). The parts are read in their own order, with no rank (1, 2, 3). His answer through the Boss (6527540022, item
8): the draw's form is the fold, c struck; the held hand is read two ways, its fine teeth by the draw and its norm by
the anchor (2, 7).

**The hostile physicist's nine:**

1. Fairness rests on the A1 hands read moving between draws on a fine pitch; matter laid as A1 is named as the board's
   source of it; the held count at rest is measured frozen (probe (j)); the held hand measured as the cure (G3's (f))
   (1, 2, 4, 6).
2. The frozen merges' weight is measured (probe (o)); the bearing dependence named; the board-fixed tie is gone with the
   rank, the parts read in their own order; term 5's push named (2, 3, 4).
3. The run back with a write, one act both ways (probe (k)); the click writes nothing (1, 2, 4).
4. Valentini's Part II and the 2002 paper; the polarization singlet; the frozen-pointer case rebuilt in whole numbers
   (probe (n)) (4).
5. Kochen and Specker for three or more parts; Bell 1966 for two (2).
6. Born's resolution near 5 x 10^-3; the 2 D_N check named as a theorem; the stand-in labelled; the two boards named
   unbuilt (2, 3, 4).
7. The partition noise measured as a variance (probe (m)) (3, 4).
8. Probe (i) labelled the raw sum; decision 29's own digits measured (probe (l)) (2, 3).
9. The missing probes rebuilt in whole numbers: no signal (n), the frozen merges (o); no root (3).

**The hostile mathematician's fourteen:**

1. The mirror's condition is the engine's promise at the round; s_(t-1) = mirror(m_out) and r_out' = T_row - 1 -
   r_(t-1); the N2 board's item struck for the mirror; the falling clock named (2, 4, 7).
2. Probe (i) relabelled; decision 29's digits on the plan-empty lay and on the vacuum (probe (l)) (2, 3).
3. "Below 3 x 10^-3" dropped; each run's D_N printed (3).
4. No rank: the parts in their own order (Big Pic), so no sort and no tie rule; the 24 in the frequencies, with the
   refused rank's count for the record (probe (r)) (2, 3).
5. "No scalar gear moves" scoped to the act as built; term 5's push of the 00 slot named (2).
6. The edge goes to the last part of nonzero size; checked in the probe (2, 3).
7. The tests that cannot fail named as such; e' = e against the control is the test (2, 3).
8. The conditional test (probe (p)) and the backward pass's step (probe (q)) added (3).
9. The odds printed; seed 4's halves component split from its tenths (3).
10. The lemma at odd T_f / p, 2 p / T_f; "no limit on L, the shares resolved to 4 p / T_f" (2).
11. What the pass holds, one sum, and where the draw is read (2).
12. No root: N D_N^2 against the Kolmogorov law's mean of the square and its 5 per cent point (2, 3).
13. Kochen and Specker for three or more parts (2).
14. The theory's pointer, light outside, printed beside the probe's (3).

The first reading's items stay folded as the second text had them (toys-5 dc795bc94, its section 8), with the second
reading's corrections above: the mirror's condition (its 1 and 5), the dial over a full turn (its 4), the 3 x 10^-3
(its 8), and Kochen and Specker's scope (its 5).

## 9. How this text checked itself (the owner's word of 16:2x UTC, 6527238774)

- **The probe rerun:** g5_draw.py run again on main's src at 0df0e8385, in 102 s; its output equal to
  g5_draw.txt byte for byte; no root, isqrt or sqrt in its code.
- **Every number** in sections 3 to 5 read against that output line by line, and G3's (f) against g3_held_hand.txt.
- **Each step derived again:** the mirror's c(T_row - 1 - r) = -c(r), so P' = -P, e' = e and the same part (section 2);
  the lemma's count at T_f / p even and odd; the 2 D_N bound for a finite record.
- **Cases built to pass the text's own words, and what broke:**
  - The second reading's condition, "a pitch that does not divide W", holds at kappa + 1, and the draw still fails there
    (the tenths 9,406 on 9, G3's (f)). The condition is sharpened to a step of the lattice at the hand's swing (section
    2), and the same correction goes to the Boss for my 16:1x line.
  - "Passes every test" broke on the 3:7 split at z^2 4.063, between the 5 and the 1 per cent points, and is worded so.
  - The vacuum's light-counted line read "e at most 3" where the probe prints at most 3 values; corrected.
  - The off-lattice spring is measured at one phase of the hand; at the 37-wave's phases on the plan's lattice the
    pointer takes 24 values (G3's (f)), so the off-lattice spring at other phases is unmeasured, said in section 7.
