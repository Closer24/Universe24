<!-- Boss note, 2026-10-31 12:14 UTC: written by the Boss from the reader's hand-back (the harness refuses report files from readers); the text below is the reader's, whole. Reader of FLOOR1b (toys-5 4441901f5, frozen at S/floor1b_frozen), the hostile mathematician (the ALG pair's mathematician). -->

# The hostile mathematician on FLOOR1b (David's "The floor's balance: masses against bands", second text), 2026-10-31

(The harness refuses report files from subagents, so here is the whole report for S/floor1b_math/REPORT.md. ASCII only.)

**What I read**
- FLOOR1b whole, frozen at S/floor1b_frozen (toys-5 4441901f5): DAVID-FLOOR-BALANCE.md (380 lines, sha256 a47952b0...), floor_balance.py and .txt, ring_balance.py and .txt, README.md. All 6 sums check OK, before and after my runs.
- For comparison: my FLOOR1 report, the ALG physicist's FLOOR1 report, FLOOR1's freeze, and the brief to 12:12 UTC. The brief includes the Boss's 11:4x ruling on FLOOR1b's physicist; its Q3 asks me to confirm or correct, and I answer in Q3 below.
- To check the text's references: Big Pic's frozen bench S/bigpic_2a839f25f_frozen (miracle/split_bedge_x100_5000.txt, miracle/equil_5000.txt, miracle/equil.py with sum 0c4c936d), and G3's ninth text (DAVID-TENSOR24-G3.md, the copy at S/miracles/src/t5/) for its window.
- I did not open S/floor1b_phys or any folder of David's pair.

**How I ran** (in S/floor1b_math/; the live venv's Python 3.14.6, -I -B, nice 19, one process at a time, load 2 to 7)
- copy/ is a copy of the freeze.
- FLOOR1b's freeze lacks its probes' two inputs. inputs/ holds equil_9771a49a4.py (0c4c936d) and nodeall_9d75a4904_src.tar (0881d3f0), both from S/floor1_frozen; src/ is the tar extracted.
- Reruns:
  - every measured line of floor_balance.txt (rerun_fb.sh, output fb_rerun.txt);
  - ring_balance.py on rings 3 to 10, and on rings 3 to 24.
- FLOOR1b's own probe on further lays: the rows the text cites from other readers, and wide held lays above the edge.
- My probe checks.py loads Big Pic's World and round exactly as floor_balance.py does. It reports E32's walk, the held dial, the taker's tooth, and E32 at named states. Whole numbers only; the carry is the one division.

**VERDICT on FLOOR1b: PASSED.** There is no BLOCKING item.
- The algebra is right and complete.
- Every measured line reruns byte for byte.
- The rows the text cites from the ALG pair rerun exactly on its own probe.

There are nine MINOR items. The first three matter for the floor line:
- The hold above half is a property of the form. A wide held hand fells the board's run even at s = t (MEASURED).
- The statement's "half" is the pair's number, not the structure's in general.
- The steady rest is a local hold, and with S kept its rest needs 2 hat n > S + c(g^2 + u^2).

On the 11:4x Q3 I confirm that condition and correct the window (see Q3).

## BLOCKING

None.

## MINOR

**1. "Whatever the held hand does" (section 1, the more-than-half case) holds for the form, not for the board's run.**
- **DERIVED and right:** M(h) = M(0) + c h^2 I >= M(0) > 0 at every h.
- **On Big Pic's board** the run's hold needs section 3's own two conditions: every held dial >= 0, and 2(s + c h^2) + t < 4W. A wide held hand breaks them even at s = t.
- **MEASURED** with FLOOR1b's probe, pair lay at rest, 5,000 rounds unless named:

  | s | lam | held lays that hold | held lays that fall (round of the fall) |
  |---|---|---|---|
  | t (2/1 of t/2) | 100 | 20, 40, 60, 70, 80 (the giver's largest 42, 576, 1,265, 1,476 and 2,895 units, against its lay's 40) | 90 (1,080), 100 (50), 110 (2,141), 120 (11), 130 (14), 141 (4), 142 (4), 150 (6), 200 (5), 400 (4) |
  | t | 1 | 5 and 10, over 20,000 rounds | 20 (2,751), 40 (1,071), 60 (205) |
  | 11/10 of t/2 | 1 and 100 | - | 141 to 400 (rounds 4 to 6) |

  The identity holds to the fall in every row.
- **The mechanism** at a held lay of 141 (lam 1, s = t, checks.py):
  - 2(s + c h^2) + t is 0.994 of 4W;
  - in round 1 the giver steps from 40 to -119, and the held dial S + c x(b) x(a) falls to -185,600,000;
  - in round 2 the held count is 7,377.
- **Fix:** write "At every held value the pair's form holds by the masses alone (DERIVED). On the board the run holds within the step's law (section 3), MEASURED on the shipped held lay and with the hand at 0, over section 5's windows." The same words belong beside "more than half the hold" in the floor line.

**2. The floor statement's "half" is the pair's number.**
- Where: the statement quoted in section 0, which the text says it states "in that form ... and derives", and the floor line of 11:4x.
- It is right on one band (2.1), and for equal masses on complete groups, where lambda_min = -1 (2.3).
- On a general structure the edge sits at -lambda_min(A) t/2 (2.3), and under the square form Harary's balance decides (2.4).
- **Counterexample:** the plain ring of four with equal masses s = 3t/4, more than half the band.
  - s I + (t/2) A has the eigenvalue s - t = -t/4, so there is no floor at all.
  - Under the square form its masses are the whole band, t, and it sits at the edge with the alternating swing free, as 2.4 itself says of every even ring.
- **Fix:** scope the statement to one band (the click world's giver and taker), and give 2.3's and 2.4's rule for every other structure. Wording in Q1.

**3. The steady rest (2.5, the finding line, section 1) is right as a linear fact for a hand held fixed. In the click world it is a local hold, and its rest depends on S.**
- **(a) DERIVED and right.**
  - At h^2 = n the pair's form is [[s + cn, t/2], [t/2, s + cn]], with swings holding s + cn + t/2 and s + cn - t/2.
  - At s = t/2 the opposite swing's whole spring is cn.
  - The hold asks s > t/2 - cn; for unequal masses, (s1 + cn)(s2 + cn) > (t/2)^2 with each factor positive.
- **(b) Whether the hat replaces S.** In G3 the hat replaces the hand's own spring ("It replaces only the hand's own spring ... by a hat"). 2.5 does not say which holds here. With S beside the hat, as the 11:4x Q2 keeps it:
  - the hand's rest is h^2 = n - (S + c(g^2 + u^2)) / (2 hat);
  - that rest exists only while 2 hat n > S + c(g^2 + u^2), which confirms the physicist's condition;
  - otherwise h = 0 is the hand's minimum, since d^2V/dh^2 there is 2(S + c(g^2 + u^2)) - 4 hat n > 0, and at h = 0 the hand lends nothing;
  - the lend at the rest is c times that rest, not cn, and the pair's own swing presses it down.

  So "holds the hand still at every whole rest |k|^2 = n" and "the lend is steady at cn" hold only for a hat in place of S, and only while the pair is at rest.
- **(c) The hold is local (DERIVED here).**
  - At s = t/2, V is flat at the hat's height along h = 0, g = -u, for every size o of the opposite swing.
  - With the hat in place of S, minimizing over h: the swing's well is 2cn o^2 - c^2 o^4 / hat up to c o^2 = hat n, and hat n^2 beyond.
  - With S beside the hat, the height above the rest is (2 hat n - S)^2 / (4 hat).
  - So the rest holds the edge's free swing only while that swing's energy stays below this height. Past it the hand sits at 0 and the swing is free again.
  - Below half (t/2 - cn < s < t/2, hat in place of S) the well is metastable, of height hat (2cn - (t - 2s))^2 / (4c^2). At s = 0, n = 1 and the click world's c and t, that is hat/25, at o^2 = hat/300,000.
  - So "whether the pair's swing knocks it off" is not only a board check: its threshold can be derived now.
- **(d) "Even s = 0 would hold the pair for a still held hand" (n = 1) is a fact of a fixed hand.**
  - With a hat inside G3's window (20 hat n < 4W, so hat < 1.2 x 10^8 at n = 1), the shipped lay's potential at s = 0 is 9.6 x 10^7, above the barrier hat/25.
  - With S beside the hat, the lend at the rest exceeds t/2 only for hat > 2.5 (S + c(g^2 + u^2)), which lies outside that window.
- **(e) The hold rests on the file's two diagonal ties,** c h^2 g^2 + c h^2 u^2. Under David's cell h(g + u) (the 11:37 ruling), f (h(g + u))^2 lends f h^2 to the together swing only. The opposite swing then stays massless at every held size, and no rest lends it anything.
- **Fix:**
  - in 2.5, say whether the hat replaces S;
  - state the rest's condition, the local hold with its height, and the dependence on the ties;
  - make "held steadily by cn" (finding line and section 1) read "locally, below the hat's height".

**4. 2.5's "The pair is held exactly while that lend stays positive" is wrong.**
- While the hand swings, the lend c h^2 is positive in every round except isolated ones. Yet the edge falls.
- I reproduced E4's fall exactly with FLOOR1b's probe: at lam 100, s = t/2, held lay 1, pair lay opposite:100, the edge falls at round 106,411. At 11/10 the same lay holds over 110,000 rounds.
- At lam 10 with pair lay opposite:10 (E6c), the held swing drains:
  - the held square's window maximum is 61,504, then 10,404, then 0 in the window ending at 60,000;
  - the pair then drifts exactly 171 counts a round each;
  - |g - u| = 74,671,136 at round 240,000, exactly E6c's number.
- **Fix:** write "held only by the lend: while the hand swings, for a while (E4, E6c); with the hand at 0 it drifts". The 11:4x line, "held only while a held hand's swing lends", already says it right. Section 5 can print both rows from its own probe.

**5. The header's "The floor is a consequence of the structure (DERIVED)" is conditional.**
- DERIVED: the two cases as conditions on masses and bands (2.1), and, under the square form, which case holds (2.4).
- That the structure gives the masses rests on the square form, a candidate no pair has passed.
- The text names it so in the next paragraph, in 2.4 and in section 6, but not beside the DERIVED.
- On the click world as shipped, the giver's and the taker's own springs are 0 (the World's [0, 0, S]), so there is no floor, and the control falls.
- **Fix:** write "DERIVED given the masses; that the structure gives them rests on the square form, a candidate", both in the header and in the floor line's standing.

**6. Wording in 2.4 and the finding line.**
- "An odd loop, a triangle first, gives more than half" (the finding line and section 6's OPEN) should read "a frustrated loop: an odd loop of plain bands, a triangle first". An odd loop with one reversal sits at the edge, by 2.4's own ring rule.
- "A reversed odd loop sits at the edge, and a reversed even loop holds" is right for one band reversed, and wrong if every band is reversed: an even loop with all its bands reversed sits at the edge. Say "with one band reversed".
- "Two odd rings, each with one reversal, make an even ring with none": the joined ring carries two reversals, which a switch of one clock's sign makes none. This fits the physicist's ask that a clock fact replace the fermion sentence.

**7. Section 3's account of the fall, and whose "mathematician".**
- At round 818 the held count is 51.13 units. It is 371.27 at round 823 and 371.97 from round 824 on (checks.py trace). Read "from round 818 to round 824".
- The held dial a round steps on is first below 0 at round 793, and below 0 again at round 820, before it stays below 0 from round 823.
- The rest reruns:
  - 2,096.90 against -2,137.11 units at round 600, and 5,412.43 against -5,428.23 at round 700;
  - 2c h^2/W = 27.672;
  - the 25.6-fold growth a round, flipping sign each round;
  - 6.04e8 against -3.21e8.
- "The mathematician" in 2.2, 2.3 and section 3 is David's pair's reader; "the ALG pair's" is mine. Two mathematicians read FLOOR1, so name the pair each time.

**8. My FLOOR1 MINOR 6 is partly met.**
- Met:
  - The triangle is now named Big Pic's, and the control is "read on his triangle alone".
  - 2.3's scope makes the lend diagonal by definition.
- Still missing:
  - whether node-all's tied trains meet that scope (diagonal by Schur on the signed-permutation kinds; a kind-E train would lend off the diagonal);
  - node-all's own fall (its act, lam 1, round 3,752), named beside "the shipped fall" of 2.5 and section 4, which is the triangle's (827, 4,373, 1,371, 1,409 and 9,581).

**9. My FLOOR1 MINOR 7 is not met in this freeze.**
- FLOOR1b's freeze holds neither equil.py nor node-all's src, which both probes need, nor the control's reference.
- They stand in the Boss's other freezes, where I checked them:
  - S/floor1_frozen: equil_9771a49a4.py (0c4c936d) and the src tar (0881d3f0);
  - S/bigpic_2a839f25f_frozen/.../miracle/split_bedge_x100_5000.txt: "a count first past 32 bits at round 827", and the held squares 12,996, 8,464, 33,489, then 37,197^2;
  - in the same folder, equil_5000.txt: "2 of the 6 turns and flips".
- **Fix:** name these paths and sums in sections 5 and 7.

## SOUND (re-derived or rerun)

**The pair (2.1)**
- M(h) = (s + ch^2) I + (t/2) X, with parts s + ch^2 +- t/2.
- Bounded below exactly when M(0) >= 0. The form holds exactly when M(0) > 0 and S > 0.
- The kernel is (t/2, -s1). With S > 0, the stationary points are the kernel times {h = 0}, and they are exactly V's zeros.

**The drift (press point 4): DERIVED exact**
- On g = o, u = -o, the push -(2s - t) o is 0 (s = TIE2/2 exactly at every grain).
- The held hand at 0 stays at 0: its push is -(g_in + g_out) x 0.
- In every round, q = 1 and the tooth stays 0. So |g - u| = 8,000 + 2r holds at every round, not only at the end.
- It is the ALG physicist's E1 law. My A1 (lam 1, 80 + 2r) is the same law.
- At rest the opposite part stays put: g - u = 3,726 + 274 = 4,000 at round 40,000.

**2.2**
- 48,000 = 2^7 x 3 x 5^3, so (t/2)^2 has 315 divisors.
- 48,000 x 10^8 = 2^15 x 3 x 5^11, so the count is 31 x 3 x 23 = 2,139.

**2.3**
- The edge is at -lambda_min(A) t/2.
- lambda_min = -1 exactly when every connected group is complete and there is at least one band (an induced P3 sits at -sqrt 2; then interlacing).
- With a band to the held hand, V >= -(t - 2s)^2/(4c); the whole-number minimum is -36,000.
- The rungs: -3, -4, and -2 for L(K_4); the golden ratio for C_5; Niven for the odd rings; the triangle holds s + t and s - t/2.

**Harary under the square form (2.4, press point 3): SOUND**
- Q = (t/2) SUM (x_i + sigma x_j)^2 is 0 exactly when x_i = -sigma x_j on every band.
- On a connected group that fixes x up to one scale exactly when every loop's product of -sigma is 1: then there is one free swing, else Q > 0.
- ring_balance reruns byte for byte. All 44 rings from 3 to 24 meet the closed forms:
  - det(A + 2I) = 2 - 2(-1)^n sigma;
  - det(A + I) = (-1)^n (2 - 2 sigma) if 3 | n, else (-1)^n (-1 - 2 sigma).

**Section 3**
- E32 = H_held + 16W m'Km + 16W d'(W - K/4)d, with K = 2M(0) and H_held >= 0 wherever the dial g >= 0. At rest with h = 0, E32 = 32WV.
- The states: E32 = 3.87e22, -2.73e22 and -1.65e30 (dial -860,000), at s = t/2 and at s = t; the physicist's state gives -2.204e25.
- The walk:
  - E32(end)/E32(lay) = 94.101, 0.550, 0.830 and 1.009 at lam 1, 10, 100 and 1000;
  - |h| reaches 22 at lam 1;
  - the lam 1 taker's tooth reaches 0.608 of D at s = 2;
  - at lam 10, over 100,000 rounds, the mean held square per 12,500 rounds climbs from 0.94 to 68.2 units, with no fall.

**Section 5**
- All 58 measured lines (55 rows and 3 window lines) rerun byte for byte.
- The cited rows rerun on FLOOR1b's own probe:
  - E4's fall at round 106,411;
  - E6c's |g - u| = 74,671,136 at round 240,000;
  - over 40,000 rounds, held lay 5/4 falls at 20,578 and 13/10 at 6,118;
  - the lam 10 taker reaches 41 at 11/10 and 48 at 2.

## DERIVED / MEASURED / OVERCLAIMED

- **DERIVED** (re-derived): 2.1, 2.2, 2.3 with its citations, 2.4 under the square form, 2.5's linear form at a fixed rest, and section 3's decomposition. My additions:
  - the drift is exact round by round;
  - with S beside the hat, the hand's rest and its condition;
  - the barrier at the edge, (2 hat n - S)^2/(4 hat);
  - the metastable height below half;
  - h = 0 as the hand's minimum once the rest is gone.
- **MEASURED:** the 58 lines; the ring rule to 24; the cited rows on FLOOR1b's own probe; checks.py's walk, trace and states; the wide held lays.
- **OVERCLAIMED:**
  - "whatever the held hand does" (MINOR 1);
  - "half" read beyond one band (MINOR 2);
  - "exactly half holds when the held hand is held", "holds the hand still at every whole rest" and "steady at cn" in the click world (MINOR 3);
  - "held exactly while that lend stays positive" (MINOR 4);
  - the header's unconditional DERIVED (MINOR 5);
  - "an odd loop ... gives more than half" (MINOR 6);
  - "at round 818 ... 371.97 units" (MINOR 7).

## The six press points

1. **Both cases as facts:** met for the form (2.1, section 6). The run's hold above half is MEASURED only on the shipped held lay and with the hand at 0 (MINOR 1).
2. **The steady rest:** the linear form is right. Beyond it, "G3's hat holds the hand at n with a steady lend cn" fails with S beside the hat, and the hold is local with a barrier that can be derived (MINOR 3).
3. **Harary:** SOUND as the rule for the form under the square form; wording in MINOR 6.
4. **The drift:** DERIVED exact and MEASURED; the ALG pair's other edge rows also reproduce.
5. **The floor as a consequence:** it rests on the square form for the masses, and the square form is named a candidate, but not beside the header's DERIVED (MINOR 5). Its "half" is the pair's number (MINOR 2).
6. **My FLOOR1 items:**
   - B1: met.
   - MINOR 1, 2, 3 and 5: met.
   - MINOR 4: met as ruled (t and c are named interims, 10:34 quoted; W/S the structure's per 11:4x).
   - MINOR 6: partly met (MINOR 8).
   - MINOR 7: not met in this freeze (MINOR 9).
   - Q1 was answered at 11:10; Q2 is met.

## Questions for the Boss

1. **Should the floor line be scoped?** My wording: "The floor comes out of the structure's own masses and bands. On one band (the click world's giver and taker), exactly half the band gives the edge, and more than half the hold. On any structure the edge is at -lambda_min(A) t/2. Under the square form a connected group holds by its springs alone exactly when some loop is frustrated; otherwise it sits at the edge with one free swing, held only while a held hand's swing lends."
2. **Is "the hold" in that line the form's (DERIVED)?** If so, the board's runs above half should be named MEASURED, on their lays and windows (MINOR 1).
3. **The 11:4x Q3, which asks me to confirm or correct.**
   - **Confirmed:**
     - With the hat beside S, the rest needs 2 hat n > S + c(g^2 + u^2).
     - hat n, S and W scale alike, so this is grain-free.
     - W = 6 Gamma^2 and S = Gamma^2 match the files' numbers at Gamma 10^4.
   - **Corrected: the window.**
     - G3 states it as "20 hat R^2 below 4 W, strict, Mesh-less; with Meshes 2 SUM_6 g_held + 20 hat R^2 below 4 W; or the lays bounded". It does not say 20 hat n <= W.
     - 20 hat n <= W is the same as the size's beat squared, 8 hat n / W, being at most 2/5. That is four times stricter, and I cannot derive it from G3's text.
     - Under G3's own window, with W = 6S, the rest exists at the pair's rest for S/2 < hat n < 6S/5.
     - The window closes as the pair widens: at c(g^2 + u^2) = 7S/5 with the hat alone, or at c(g^2 + u^2) = S if the hand's own spring and lend are counted in the stiffness. On the click world's c and S that is about 48 or 41 units.
     - At the shipped lay it leaves 0.98 S < hat n < 1.2 S (or < 1.004 S).
     - The 20 hat n form is for a hand that rolls from the top. A hand held still meets at most 8 hat n.
     - G3's window is the explicit step's. On road B the held hand is dialed, and its polarized step over D + g is stable for every g >= 0. So which window binds a hat there is Big Pic's road-B form.
   - **So:** "excluded on every world of this structure" does not follow from W/S = 6. What follows is a narrow window, closing for pairs of about 41 to 48 units, that gives only a local hold (MINOR 3). Taking the clause out of the floor line still stands, on MINOR 3's grounds.

## Solution24 (the reader's line)

FLOOR1b gets the floor's algebra right, completely, for the pair and for networks:
- the potential is bounded below at s >= t/2;
- the masses hold at s > t/2, with S > 0;
- at the edge one swing is free and drifts exactly with the hand at 0;
- under the square form, Harary's balance decides which case holds.

But this is a consequence of the structure only through the square form, which is a candidate. The hold it derives is the form's: on the board a wide held hand fells even s = t. A hat's rest holds the edge only locally, below the hat's height.
