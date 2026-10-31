# SPLIT3: the takers' swap on the four-tooth palindrome (for Big Pic's stage 2 and THIRD6)

The Boss's deriver of SPLIT, 2026-10-31, 04:3x to 05:1x UTC. **Status: PASSED by both readers, minors folded** (with
SPLIT2b; scratchpad/split2_math/REPORT2.md and scratchpad/split2_phys/REPORT2.md; section 6). It reads the THIRD
deriver's palindrome against SPLIT2's premise P2, the takers' swap, on SPLIT2's probe part (b). The palindrome is in
scratchpad/third/toy6/mirror6.py and palin4.py, copied unchanged into split/toy6/ with SHA-256 equal to the originals.

**Files** (scratchpad/split/), each run twice from this folder, the two outputs byte-identical (cmp):
- split3_probe.py: split3_run1.txt = split3_run2.txt;
- split3b_probe.py: split3b_run1.txt = split3b_run2.txt;
- the THIRD deriver's search: toy6/palin4_run1.txt = toy6/palin4_run2.txt.

mirror6.py's definitions run as written, and none of its loops run. The probe's round equals its step4 at 20,000 of
20,000 rounds. The lay is a **stand-in** (a 64-bit carry sequence). The passings 16 k, 9 k and 16 k, with k = D div
1,250 and D = 50,811,429, and 9 and 16 times D div 50 for the memory reading, are the toys' stand-ins. Every number
here is a board toy's reading, not a share in the click world.

## Verdict

1. **The THIRD palindrome does not commute with the swap draw by draw, and does hold in frequency.**
   - DERIVED: its five shears, t1 += g1, g1 -= t1, t2 += g2, g2 += t1, g1 += t2, have no swap image of g1 -= t1. So
     P H P^-1 != H, both for the swap P (g1 with g2, t1 with t2) and for P' (the same with the hidden teeth negated).
   - MEASURED: the swapped state parts from the original's swap at round 1 in 10 of 10 lays, and its totals are swapped
     exactly in 0 of 10.
   - In frequency, at 16 k and 16 k over 20 lays of 100,000 rounds: pooled 25,418 : 25,542, z^2 0.301.
2. **A palindrome on the same classes that does commute exists, built from the structure alone.** The building rule:
   each block is a pair of shears the swap exchanges, which commute because each writes one class and reads the other,
   and the blocks alternate the classes. Each block is then mapped to itself by the swap, so the whole half-turn is.
   - 144 such palindromes of 2 to 4 blocks keep no direction and are hyperbolic on both the swap's even and odd parts.
   - 48 of them split into one pair of teeth per taker, and those remember: after two takes in a row, 2,129 of 12,824
     against 2,298 independent, and 12,091 of 41,023 against 13,140.
   - 96 join all four teeth. The shortest, 4 blocks and 8 shears, is t1 += g1 and t2 += g2; g1 -= t1 and g2 -= t2;
     t1 -= g1 and t2 -= g2; g1 += t2 and g2 += t1. It reads:
     - the swap: 500,000 of 500,000 rounds draw by draw, totals swapped exactly in 10 of 10;
     - the run back by the same act on the mirrored state: 0 fails, the window exact, the flip 0 fails;
     - R2: 200 of 200; an empty taker: 0 clicks; the share 367 thousandths against 360;
     - no memory: 2,191 of 12,583 against 2,251, and 13,126 of 41,090 against 13,177.
   - **P2, as relabelling-covariance under the swap P, is DERIVED on the toy's round.** A lay and its swap give exactly
     swapped takes. The qualifications:
     - it holds for P, not for P';
     - it holds on mirror6.py's definitions, and on the engine's act only once THIRD6 builds the member;
     - under a relabelling of universe.json it holds only if the lay relabels with the trains, which the birth rule's
       equal teeth make automatic.
   - Covariance relates two worlds, a lay and its swap. Equal counts in one world need a lay the swap keeps, or a
     record that mixes (P1's reading (i)): equal squares get equal shares wherever the lay's spread carries no label.
   - Of the 144 forms only two were run with carries: the split form at 16 k : 16 k and at 9 k : 16 k, and the coupled
     form at 9 k : 16 k, each at 500,000 of 500,000 rounds. The other 142 meet P2 at the matrix level only.
   - Named and passed: the member is chosen by the rule "fewest shears, smallest entries", not by a number. Whether the
     structure fixes it further (the 24 on a negated giver row; P' if the structure's swap complements the hidden
     teeth) is THIRD6's.
3. **The within-lay correlation belongs to Big Pic's triangle and leaves with it.** The lays' z^2 summed over 20 lays,
   against chance's 20:
   - the triangle: 8.089;
   - the THIRD palindrome: 17.023;
   - the 48's first, split per taker: 18.428;
   - the coupled symmetric palindrome: 15.228.

   The chi-square on 20 has its lower 5 per cent point near 10.851, a cited reference value. Only the triangle falls
   below it.

## 1. Why P H P^-1 != H for the THIRD palindrome (DERIVED)

The swap P acts on u = (g1, g2, t1, t2) as (g2, g1, t2, t1). A shear "x += s y" goes to "P(x) += s P(y)". The THIRD
half-turn's shears go to t2 += g2, g2 -= t2, t1 += g1, g1 += t2 and g2 += t1. The set holds no g2 -= t2, so the image
differs as a set, and the matrices differ:
- H = [[0, 1, -1, 1], [1, 1, 1, 0], [1, 0, 1, 0], [0, 1, 0, 1]];
- P H P^-1 = [[1, 1, 0, 1], [1, 0, 1, -1], [1, 0, 1, 0], [0, 1, 0, 1]].

Under P' every image shear changes its sign, and P' H P'^-1 != H too. The carries commute with both swaps once the
passings are exchanged, so the round commutes exactly where the half-turn does.

## 2. The swap-symmetric palindromes (DERIVED, then MEASURED)

**The blocks.** A t-block is (t1 += s g1, t2 += s g2) or (t1 += s g2, t2 += s g1). A g-block is (g1 += s t1, g2 += s t2)
or (g1 += s t2, g2 += s t1). Here s is plus or minus 1. Each block's two shears commute: they write the two teeth of one
class and read the other class. P exchanges them, so P maps each block to itself, and a half-turn built of blocks
satisfies P H P^-1 = H.

**The mirror holds for any palindrome of shears between the classes.** The mirror keeps g and negates t, so it turns
each such shear into its inverse: mir s mir = s^-1. With the carries' rule (teeth kept, passings negated), the mirrored
round is the round's inverse. This is the THIRD deriver's own law, unchanged.

**The swap splits L.** L commutes with P, so it splits into its even part (g1 + g2, t1 + t2) and its odd part
(g1 - g2, t1 - t2), each a 2 x 2 block of determinant 1.
- It keeps no direction where neither block's trace is 2 or -2.
- It mixes where both traces exceed 2 in size.
- The coupled form's traces are 6 and -10, with L = [[-1, 4, 4, -2], [4, -1, -2, 4], [4, 0, -1, 4], [0, 4, 4, -1]].

**Why the coupling counts.** Every 2-block and 3-block member of the family splits into one pair of teeth per taker: each
taker then draws from two teeth of its own, and two teeth remember, as Big Pic's item 2 (c) found and (iv) measures. The
shortest coupled member has 4 blocks.

## 3. The readings

| Reading | THIRD palindrome | symmetric, split per taker | symmetric, coupled | Big Pic's triangle |
|---|---|---|---|---|
| the swap draw by draw (10 lays of 50,000) | 0 of 500,000; totals 0 of 10 | - | 500,000 of 500,000; totals 10 of 10 | (SPLIT2) parts within 1 to 64 rounds |
| the split form against the swap (split3_run1.txt) | - | 500,000 of 500,000; totals 10 of 10 | - | - |
| equal squares, pooled (20 lays of 100,000) | 25,418 : 25,542, z^2 0.301 | 25,644 : 25,762, z^2 0.270 | 25,587 : 25,686, z^2 0.191 | 25,675 : 25,479, z^2 0.750 |
| the lays' z^2 summed, against 20 | 17.023 | 18.428 | 15.228 | 8.089 |
| a take after two in a row, the first taker | 2,301 of 12,853 (2,307) | 2,129 of 12,824 (2,298) | 2,191 of 12,583 (2,251) | - |
| the same, the second taker | 12,902 of 40,476 (12,899) | 12,091 of 41,023 (13,140) | 13,126 of 41,090 (13,177) | - |
| run back by the same act on the mirrored state; window; flip | 0; exact; 0 (the THIRD deriver's mirror6.txt) | 0; exact; 0 | 0; exact; 0 | fails at 2,000 of 2,000; only its own back() is exact (mirror6.txt) |
| R2 (one hidden unit apart); an empty taker | 200 of 200; 0 (mirror6.txt) | 200 of 200; 0 | 200 of 200; 0 | - |

In the memory rows, the brackets hold the count expected of independent takes, from each taker's own rate.

## 4. Statuses

- **DERIVED:**
  - the THIRD palindrome's half-turn is not swap-invariant;
  - a half-turn of swap-exchanged commuting blocks is swap-invariant;
  - every palindrome of shears between the classes keeps the mirror law;
  - L splits on the swap's even and odd parts;
  - P2, as relabelling-covariance under P, holds draw by draw on the toy's round for the swap-symmetric family. Equal
    counts in one world need, beyond it, a swap-kept lay or mixing within the record.
- **MEASURED on the stand-in toy:** every number above, two runs alike.
- **Named and passed:**
  - the family member, chosen by the rule "fewest shears, smallest entries", for THIRD6 to fix by the structure;
  - the swap P' that complements the hidden teeth, which neither form commutes with, for THIRD6 if the structure's
    swap is P';
  - the 24 on a negated giver row, for THIRD6.

## 5. R3 read again on the palindromes (SPLIT2's physicist's B3, the Boss's 04:5x item 4)

The probe is split3c_probe.py, run twice from this folder: split3c_run1.txt = split3c_run2.txt. It uses the
physicist's measures (split2_phys/fano.py):
- each taker's Fano factor, its counts' variance over their mean (about 1,000 thousandths for independent takes);
- the two takers' covariance, given as r^2 = cov^2 / (var a var b) with cov's sign, so that no root is taken.

It reads them two ways:
- (a) across SPLIT2's 20 stand-in lays of 100,000 rounds, the physicist's own window, where each value is good to
  about a third;
- (b) within one record of 2,000,000 rounds cut into 200 blocks of 10,000, read twice, on blocks 1 to 100 and 101 to
  200.

| Form | (a) Fano a, b; r^2 (sign) | (a) difference spread | (b) Fano a, b; r^2 (sign) | (b) difference spread | (b) halves: Fano a, b; r^2 (sign) |
|---|---|---|---|---|---|
| Big Pic's triangle | 584, 581; 133 (+) | 369 | 907, 970; 16 (+) | 819 | 837, 978; 18 (+) and 972, 960; 14 (+) |
| the THIRD palindrome | 556, 1,289; 10 (+) | 835 | 831, 1,039; 0 (+) | 932 | 874, 1,059; 1 (+) and 789, 1,009; 1 (-) |
| symmetric, split per taker | 706, 1,179; 1 (+) | 905 | 905, 897; 12 (+) | 801 | 885, 746; 2 (+) and 876, 1,040; 21 (+) |
| symmetric, coupled | 1,018, 349; 12 (-) | 749 | 972, 1,093; 7 (-) | 1,124 | 969, 1,196; 39 (-) and 965, 978; 0 (+) |

All values are in thousandths.
- The difference spread is var(a - b) over independent takes', var a + var b, by the carry's floor; the physicist's
  rounding gives 370, 835, 906, 749 and 820, 932, 802, 1,125.
- The bands, from the physicist's REPORT2 (Wilson-Hilferty, cited): 20 lays 469 to 1,729; 200 blocks 813 to 1,206;
  100 blocks 741 to 1,297.

**Read:**
- **The triangle: R3 NOT MET on the stand-in across the 20 lays, a board ensemble, as the physicist measured.** It
  reproduces his numbers exactly: Fano 584 and 581; r^2 133 with cov positive, so r is about +0.37, which is 1.6
  standard errors; difference spread 369.
  - Within one record the triangle is not settled: Fano 907 and 970, r^2 16 (r about +0.13), and difference spread 819,
    inside the band.
- **The palindromes' co-movement:** r^2 at most 12 thousandths in the two main readings. The halves reach 21 (+, the
  split form, blocks 101 to 200) and 39 (-, the coupled form, blocks 1 to 100, about two standard errors), and there
  the coupled form's difference spread is 1,296, at the band's edge.
- **The split per taker form: R3 shown FAILED on the stand-in.**
  - Its memory row (section 3) is a take after two in a row at 12,091 of 41,023 against 13,140, about 11 standard
    errors low.
  - Its difference spread within one record is 801, below the band's 813.
  - Two teeth remember. **Road 3, one two-tooth palindrome per triangle edge, is in this split family.** It must be
    read for memory (a take after two in a row against independent) on Big Pic's world before THIRD6 takes it.
- **The coupled form and the THIRD palindrome: regularity not settled.** Across the 20 lays it scatters from 349 to
  1,289. That is about the
  spread 20 samples give, though the coupled form's 349 sits below that band's lower 2.5 per cent point, near 470.
  Within one record it lies from 831 to 1,093; the THIRD palindrome's first taker, at 831, is about 1.7 standard errors
  low.
- **So R3 is shown failed on the split form, and neither met nor failed on the coupled form and the THIRD
  palindrome.** It is owed in the click world. The next
  reading is the Fano factor against the window's length within one record: a carried form's regularity grows with
  the window, and independent takes stay at 1,000.

## 6. The readers' minors, folded (with SPLIT2b; one line each, no third read)

**The mathematician:**
1. P2 is relabelling-covariance under P (not P') on the toy's round. It reaches the engine's act once THIRD6 builds
   the member, and a relabelling of universe.json only where the lay relabels with the trains (the verdict,
   item 2; section 4).
2. A sense-free turn gives covariance, not equal counts. Equal counts in one world need a swap-kept lay or mixing within
   the record (verdict, item 2).

**The physicist:**
1. R3 is shown FAILED on the split per taker form: its memory row is about 11 standard errors low, and its difference
   spread is 801 against the band's 813. Section 5 adds the difference-spread column. Road 3, THIRD6's candidate, is
   in that family and is named so.
2. The halves' r^2 reach 21 and 39; "at most 12" holds in the main readings only (section 5).
3. The triangle's R3 NOT MET holds across 20 lays only; within one record it is not settled (section 5).
4. Every number is the stand-in toy's, and the coupled form's share is 367 against 360 (verdict, item 2).
5. Only two of the 144 forms were run with carries (verdict, item 2).
