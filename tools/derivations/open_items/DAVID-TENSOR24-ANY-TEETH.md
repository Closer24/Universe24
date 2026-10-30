# Every act at any teeth count: the retrace, the frame, and the balance at an odd count

David, 2026-10-28, 13:4x UTC, for the Boss (Sofer and Animate copied). This page answers:
- **the owner's ruling** (10:5x UTC, to Animate and to Sofer): teeth counts carry no parity restriction, and every act is derived to hold at any count;
- **Sofer's items owed to me** (6467734998): the formula of w at an odd count, T S T = S^-1 at any count, and the riders' mean teeth count at an odd w;
- **Animate's ask** (6467251813): (i) and (ii), or better, derived at any teeth count.

A helper drafted it, and I reran all six probes; their outputs are identical. The probes, their outputs and the draft's proofs in full are in DAVID-TENSOR24-ANY-TEETH_CHECKS.txt. The draft was read on toys-5 b56643b0e (src) and scribe-5 f32b67cc3 (the law). This page covers protocol steps 1 to 4; a second hand follows, then Sofer's check and my sign-off. No src is pushed.

## The findings

1. **Rule3's carry has one reflection, the flip u -> W - 1 - u.** PROVED (Lemma 1).
   - Read at the mid tooth, it sends the stride P to -P at an odd count, and to -P - 1 at an even count.
2. **At an even count, no carry with its remainder in [0, W) rounds oddly.** PROVED (Lemma 2): the fibre of the quotient 0 would be symmetric, so its size would be odd, but it has W elements.
   - So the exact reversal P -> -P is no symmetry of Rule3's carry at an even count. One more bit, a frame, is needed.
3. **The retrace has one solution** (Theorem A, PROVED). A turnover that exchanges the slots retraces, S T S = T for every time-even kick and every pair of counts of either parity, if and only if two things hold:
   - the stride is reversed, P -> c - P;
   - the two frames' mid teeth sum to V - 1 - c at every count V.

   With c = 0 that is **FRAME**:
   - the turnover's mirror is the flip r -> W - 1 - r;
   - the stride is read and carried at the frame's mid tooth, m_f(W) = mid(W) + f (W - 1 - mid(W) - mid(W));
   - f is the gear's count of reversals mod 2, toggled at each turnover.

   No branch and no parity test enter: f multiplies the count's own W - 1 - mid(W) - mid(W), which is 0 at an odd count.
4. **FRAME has a frame-free spelling, DOUBLED** (Theorem B, PROVED): the fine tooth at the doubled count 2W, whose mid tooth W is exact, the flip there, and the stride read as (P2 + 1) div 2. The frame rides in P2's parity.
   - DOUBLED and FRAME are one machine: 0 mismatches in 321,048.
5. **In frame 0, FRAME is the head's step bit for bit.** FRAME's turnover is an involution (T T = 1), and the whole run back returns the turned start through every turnover between.
6. **CHECKED at every w from 2 to 40, both parities, FRAME and DOUBLED, with 0 failures:**
   - one gear, exhaustive: 160,524 states, 641,312 changes of count, and 1,302,700 images of the mathematician's toy, none hit twice;
   - the circle: a time gear's weak top turning over a ring of five gears, 0 of 640 runs;
   - the head's own acts: 0 of 481,572;
   - the 24 on a 3^3 torus with a vector train: 0 of 7,200.

   All 8 mutants are caught.
7. **The law should state S T S = T with T T = 1.** T S T = S^-1 alone is not enough: Animate's carried mirror satisfies it (0 of 41,160) yet misses the run back at 1,960 states, because its T T is not 1.

## What the head fails at an even count, and why

1. **acts.mirror drops the carry of mid + mid - r.** At the fine tooth 0 the turned stride reads -P - W: 1,960 of 41,160 cases, every one an r = 0 state, and none at an odd count.
2. **The carry rounds a tie up in both directions,** so q(-P) = -q(P) + 1. The ties are exactly the r = 0 states.
3. **S T S = T fails exactly where exactly one of r and r+ is 0:**
   - 3,472 of 3,472 such states fail;
   - none of 37,688 others fail;
   - none fail at an odd count.

   It also fails at every change of count that meets an even count: 6,243 even to even, 3,822 even to odd and 4,743 odd to even. The mathematician's 25 images at w = 10 and 0 at w = 11 are reproduced.
4. **On the head's whole Tick** (node, nature and hole, with the fine tooth 0 seeded on hand gears):
   - 44 of 44 seeded three gears miss the turned start;
   - 0 of 44 seeded twelve gears miss it;
   - 0 of 44 miss it with acts.flip in acts.mirror's place.

   The head stays exact backward only through its stack.
5. **Two more failures:**
   - clock.reverse mirrors every drive fine tooth, which fails at even drive counts: 12,642 of 144,060, and 0 with the flip;
   - rule3.mean_teeth_of reads T div 2, which is wrong at an odd T: 7,600 of 7,600.

## Animate's two candidates

1. **(i), the carry kept in the stride, fails alone.** At r = 0, T T moves both notches by one, and the run back rounds the ties up again (1,960 each).
2. **(ii), ties to the even quotient, fails alone:** 1,838 and 1,830 failures. In the head's encoding it also loses the stride: 15,757 images hit twice.
3. **Together, in their closed letter, they are exact at every count** (Theorem C), so they are enough. They carry three costs:
   - at even counts the remainder reaches w, outside Rule3's range;
   - the rounding departs from the head's step at the ties;
   - "even" is not what works: any odd tie rule serves.
4. **Neither is needed.** FRAME and DOUBLED keep Rule3's floor and use the flip.

## The balance at an odd count

1. **The balance 2w = SUM R + D at the vacuum, for every pair, forces the factors (3k, k, 6k).** PROVED and CHECKED: among all triples up to (12, 12, 30), only these hold, and the mutants fail 78, 78 and 90 of 90 pairs.
2. **The least count (k = 1):**
   - w = AXES rim Gamma^2 G^2;
   - R_j = pinion p_i^2 Q_j;
   - D = SPOKES (rim - pinion) p0^2 G^2.

   It takes the calibre's parity, with no number but the piece's counts. The head's (6, 2, 12) is exactly its double: 0 failures in 10,395 pairs.
3. **The riders' mean teeth count (w / 2)(X0 + X1) becomes the doubled form w (X0 + X1), with the kick doubled.**
   - It is the exact rational letter: 0 of 15,600 against fractions.
   - At even w it is the head's step bit for bit: 0 of 3,937.
4. **The shear's (3w / 2)(X_ahead - X_behind)** is no integer at a mixed parity. Doubled, 3w (X_ahead - X_behind), it is exact: 0 of 9,947.
5. **The 24 at the odd gearing (w = 135):**
   - FRAME and DOUBLED: 0 failures of 2,880;
   - the head's mirror: 588 failures of 1,440, once the riders' count changes parity.

   The riders meet even counts at every calibre, since X0 + X1 is even at rest. So the even-count fix is needed whatever the calibre's parity.

## The other lines that lean on parity (one line each)

1. **w div 2 taken as exact** (ALGEBRA.md lines 100, 110, 130, 1600, 436 and 559): take the half of the whole product, or use the doubled form, and read P in the frame. Line 110's "Gamma odd" is struck.
2. **The setting at the half teeth count** (lines 1411, 344, 622, 352, 618 and 122): a gear is born at m_f(W), and line 622's complement is the frame-1 born tooth. The fold min(r, w - 1 - r) is the flip's invariant (0 failures of 819), not the head's mirror's (380).
3. **The count of quanta** (lines 110 and 142, where T is the key): count q = 2|W| div T, which is exact (0 of 23,439). The key's half misreads 8,963.

## What it replaces, and what stays OPEN

1. **Replaces:**
   - the one mirror at even counts (acts.mirror) by the flip with the frame;
   - the drive fine tooth's mirror at the turnover by the flip, where the numerator is time-even, and by the identity where it is time-odd;
   - mean_teeth_of's T div 2 by the doubled form;
   - every law line that leaned on parity, as above.

   The frame needs no new state at the turnover: it is the Node-clock's ratchet remainder (line 1602).
2. **OPEN:**
   - **a lone quantum at an odd key.** Setting it, A B = T / 2, is impossible there: the owner's call;
   - **FRAME or DOUBLED in the build:** a frame per gear, or a wider fine tooth;
   - **every reader of a driven stride must read in the frame** (the forms, the sweep, the stress, the winds, run.py and draw.py). Not probed;
   - **which drive numerators are time-even under K,** train by train;
   - **the regulator's three flow gears miss the turned start on the whole Tick** even with no tie: 14, 38 and 86 slots on node, nature and hole. It is no parity matter, and its cause is not read;
   - **the clicks and the draw** are not covered.

## For the Boss

1. **The cuts:**
   - the turnover's mirror is the flip, with the frame per gear (FRAME) or the doubled fine tooth (DOUBLED), so that S T S = T and T T = 1 at every count;
   - the drive's fine tooth takes the flip;
   - the balance takes the factors (3k, k, 6k), with k = 1 at an odd count;
   - the riders and the shear take the doubled form;
   - the count of quanta is q = 2|W| div T.
2. **For the law (Sofer):**
   - "S T S = T with T T = 1" replaces "T S T = S^-1";
   - the mirror's clause at even counts;
   - line 110's "Gamma odd" is struck.
