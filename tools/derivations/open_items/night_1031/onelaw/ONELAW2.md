# ONELAW2: the fold of the FRAME16 readers into ONELAW

Status: DERIVED as a reading on static frames; the act not built; both readers' items folded, 02:3x UTC
(physicist B1, B2, M1-M6; mathematician B1, B2, M1-M7, re-counted on p_onelaw2b.py). Folds f16_math/REPORT.md and
f16_phys/REPORT.md (both NOT PASSED on FRAME16) into ONELAW.md. New probe: onelaw/p_onelaw2.py with
p_onelaw2.txt. p_onelaw.py's acts now read spring = o det S (o = +1 laid), with p_onelaw.txt unchanged (diffed
identical). Whole numbers; Rule3's carry the one division (Bareiss's exact steps by carry, remainder checked 0);
no sign test in any act offered here.
The owner's word of 02:0x: no physics on a board reading. gamma, redshift, light, the cone, the delay and the
bending are owed to the click world, read there by Big Pic's methods (the meetings, their order, each clock's own
count of its events, light's echo between clocks). On the board the law is a clock fact: the dial, the grips and
the spring, measured on the board. "The board's wave" is the train's wave, c_w^2 = grip / W: a clock fact.

WHAT CHANGED (the ONELAW lines it replaces)
- 1.1 l.13-14 "(the inverse metric)": the slots are the act's DENSITIZED coefficients, read through the
  frame (item 3).
- 1.2 l.19, 2.2 l.47-48 "spring = |det S| m^2", "q = carry(det S, det(S)^2 + 1, 0)": withdrawn from the act;
  spring = o det S m^2, o laid and held (item 5).
- 2.2 l.49-50 "W(a+) needs the 0-row's four gears given first": named as an act change (item 6).
- 2.5 l.57-60 "(1, 3) (A): ... MEASURED": DERIVED, a code check (item 1).
- 3.1 l.76-78 units: rest / grip = 6 named as a cost (item 7).
- 3.3 l.82-92 (tip, bound, det S): replaced by the run from the flat with margin (section 0, items 2 and 9).
- Part A's start S = 4 I everywhere: replaced by S0 = diag(L0, +-l0, +-l0, +-l0), L0^2 > 3 l0^2 (item 2).
- 4: the first arrival added (item 10). The rest of ONELAW holds as DERIVED readings on static frames: 1.3-1.5,
  2.3, 2.4, 2.5's two halves (on an S00-only well), 4, 5; 5's "ONE LAW" is a reading, the act not built.
- Any ONELAW sentence naming a cone, gamma or light (3.3 l.83 "the cone tipping", 4.2's "(1 + gamma)") is
  owed to the click world; on the board it reads "the tip": W <= 0 or the space block not definite.

## 0. The measurement (p_onelaw2 A2): the ten slot gears, ten free waves on the fixed dial 18 (as p_gauge2)

From S0 = diag(L0, s l0, s l0, s l0) plus a spread on all ten slots, 27 Node-clocks x 41 rounds = 1107 per run;
stride +-1 (ONELAW's seeds) or 0 (released at rest). 3 l^2 = L^2 has no whole solution, so the flat's bound is
strict. "Spokes" = the six Spokes' bound spelt for any grips P: s^T P s <= W at s = (1, +-1, +-1) (diagonal
P: 3 grip <= W; it ignores the 0i slots, see item 2). Crossings: a sign change of det S between consecutive
nonzero rounds at a Node-clock (as the code counts; a passage through a landing counts there too, at most 16).

    flat (L0, s l0)  spread stride | W<=0 (start) | Spokes failed (start) | det S land / cross | chart cross
    (12, +4)            1     1    |   414 (0)    |      865 (0)          |      0 / 234       |    304
    (12, +4)            1     0    |     0 (0)    |      117 (0)          |      1 / 84        |     84
    (12, +4)            3     1    |     0 (0)    |      987 (18)         |      1 / 150       |    291
    (12, +4)            3     0    |     0 (0)    |      492 (15)         |      5 / 375       |    417
    (12, +4)            6     1    |   137 (4)    |     1017 (21)         |      0 / 243       |    453
    (12, +4)            6     0    |    43 (3)    |      806 (24)         |      0 / 409       |    498
    (12, -4)            1     1    |     0 (0)    |      121 (0)          |      2 / 224       |    364
    (12, -4)            1     0    |     0 (0)    |       55 (1)          |      1 / 14        |     14
    (12, -4)            3     1    |   105 (0)    |      633 (15)         |      0 / 209       |    312
    (12, -4)            3     0    |     1 (0)    |      613 (16)         |      4 / 324       |    340
    (12, -4)            6     1    |   457 (3)    |     1072 (24)         |      1 / 282       |    349
    (12, -4)            6     0    |    85 (4)    |      848 (23)         |      0 / 416       |    464
    (30, +10)           1     1    |     0 (0)    |       10 (0)          |      0 / 63        |    168
    (30, +10)           1     0    |     0 (0)    |        0 (0)          |      0 / 0         |      0
    (30, +10)           3     1    |     0 (0)    |      646 (0)          |      1 / 114       |    212
    (30, +10)           3     0    |     0 (0)    |       39 (0)          |      0 / 2         |      2
    (30, +10)           6     1    |     0 (0)    |      571 (13)         |      0 / 241       |    276
    (30, +10)           6     0    |     0 (0)    |      199 (11)         |      0 / 135       |    135

MEASURED: W <= 0 in 1242 of 19,926 Node-clock-rounds, none at the wide flat (30, 10) (the W half only); the
unshifted Spokes' test failed in 9091 (it understates), held throughout in one run of 18 ((30, 10), spread 1, at
rest). Read again (p_onelaw2b.py, the mathematician's counts reproduced): the shifted bound (item 2) fails at
12,500; P not definite (the tip's other half: the act reads no 0i, so (W, -P) is hyperbolic only if P is
definite) at 9264, 3533 of them passing the unshifted test with W > 0; at the wide flat 1636 of 6642. det S
crossed 0 3519 times against 16 landings; the chart's singular set (item 2) crossed 4683 times against the same
16 landings (those include det S's; the i < j factor alone 2385, math M3). The run back: 0 of 810 missed in
all 18 runs, on the free act at the fixed dial 18, not the joined act. (1, 3) at every invertible round in all
18 (a code check, item 1).

## The eleven items

1.  (1, 3): DERIVED, Sylvester's for every invertible S (44,868 of 44,868 over 3^10, math B2); ONELAW's
    1100/1100, 1101/1101, 1106/1106 and section 0's counts are code checks and cannot fail. Nothing holds det S
    off 0: section 0's 3519 crossings against 16 landings (math B2: 286 against 6); on a definite flat
    det(S0 + t V) = det S0 prod (1 + t mu_i) with every mu_i real, so a zero comes forward or on the run back
    (not so for the indefinite (12, -4) flat, math M2). DERIVED.
2.  W <= 0: ONELAW's tip counts 934, 964, 1023 are mostly this fact (p_gauge2: 835 of 1100, 807 of 1101, math
    B1, phys B3). At W = 0 a dial that reads W is 0 and Rule3's carry has no divisor. W >= 1 and the Spokes'
    bound are laws still owed; Sylvester gives neither. Spelt whole, with no root (math B2): W >= 1;
    s^T P s + 2 s . beta <= W for all eight s in {+-1}^3, beta_i = G0i (the unshifted s^T P s <= W passes 38 of
    119 of his frames whose cone leaves the board's reach); P's three leading minors > 0. The margin only delays
    a failure, in proportion to L0: from diag(30, 10, 10, 10) a uniform stride +1 on S01 gives W = 59, 0, -61 at
    rounds 29, 30, 31 (det S = -60,000) (math M1).
    ONELAW's start S = 4 I had W = grip, was outside the bound, and sat at the gauge's degenerate point (rank 7
    of 10, math B3, phys B4): replaced (section 0). The
    reading's singular set: prod over i <= j of (lam_i + lam_j) = 0, lam the eigenvalues of S C; it is the
    determinant of the chart's own map dS -> dS C S + S C dS (DERIVED), and det S = 0 is only its i = j part.
3.  On the board the slots are the act's densitized coefficients, read through the frame: the act's divergence
    form d_t(W d_t a) = d_i(grip d_i a) is identified with it (phys B2 (a)), not derived; recovering g^mn from G
    would need a root, which the act does not use. Its density is det S: in 4-D such coefficients
    have det G = -(density)^2, and G = S C S gives det S (its sign: item 5). Read as plain inverse coefficients,
    the density would be 1/det S, a division. The metric that clocks and echoes see is owed to the click world.
    DERIVED.
4.  The spring road is the one the physicist measured on the board (phys B2, p_phys E: spring = S00 at 64
    against 81, 1001 per mille, the board's wave slowing as the beat squared; a fixed spring, 1000, as the beat).
    ONELAW's D1, D2 and E are the same road on two more boards (one well: clock 2001, the board's wave 3985
    permille; fixed spring: clock 3995 against the wave's 3979). MEASURED on the board, clock facts only, ON A WELL
    THAT DEEPENS S00 ALONE (the spatial legs laid flat; all four boards were laid so): the clock's beat slows by
    N, the board's wave by N^2. DERIVED: on S = diag(L, l, l, l) with spring = o det S m^2, beat^2 ~ l^3 / L and
    wave^2 ~ l^2 / L^2, so the wave is the beat squared only while l stays fixed: the N^2 needs the OPEN law
    "the slots' own law leaving the grips". And beat^2 = o det S m^2 / W is the uniform mode's beat; with 0i
    slots a clock held at one board site beats at another rate; which board clock is the click world's clock
    is owed. No physics is read from it: gamma, the delay and the
    bending are owed to the click world, by Big Pic's methods (light's echo between two clocks against each
    clock's own count: the echo delay over the clock deficit, 1 + gamma, read twice there).
5.  The sign: ONELAW's |det S| = det S (1 + q + q), q = carry(det S, det(S)^2 + 1, 0), is the gate's INDICATOR
    (the sign test x div (x x + 1): a bound spelt as a quotient, an if; the Node-clock has none). Withdrawn from
    the act. The option: o = +1 or -1, ONE global orientation, a CHOSEN lay orientation fixed by how the start is
    built (the Boss's ruling), never read from det S0 at each site (that is a sign test at load); spring =
    o det S m^2, the density only on det S's laid sign. MEASURED twice (p_onelaw2b and the mathematician's):
    o det S < 0, an anti-spring and a runaway, at 8477 of 19,926 Node-clock-rounds with one o per flat (7270 with
    one o per site, which the ruling forbids); det S0 already has the other sign at 133 of 486 site-starts. No
    free act holds the sign (item 1); exact: the wide flat with a stride -1 on S11 gives det S = 3000, 0, -3000
    at rounds 9, 10, 11. OPEN (put to Big Pic). D2' (2001 permille, unchanged) cannot fail: det S = f > 0 on its
    static, hand-laid well. DERIVED, not a measurement of the spring; the joined act is not built.
6.  W(a+): not one synchronous pass. The engine already gives the 00 row's own carry first (on its own teeth at
    rest) and then the rows whose D_out = W(a) + W(a+) reads it: a second sub-step. The joined law widens that
    sub-step from one row to the 0-row's four (S00, S01, S02, S03), each of which must keep a dial that does not
    read W: an act change, named as such. Every gear still reads only now and before, plus the given-first
    counts. A one-pass D_out = 2 W(a) would break the edge's dial shared by the run back. DERIVED, not built.
7.  Units: the flat S0 = diag(r, g, g, g) needs rest / grip = (r / g)^2. The shipped rest / grip = 6 is no square
    of a ratio, so the shipped files do not fit the frame law; stronger (math M7): no whole frame at all reads
    rest / grip = 6, since -det G = 6 k^4 is never a square. Cost: the loader re-laid (9, the physicist's,
    r = 3 g, also keeps the Spokes' bound with margin 3), and every reading calibrated at 6 (FWDBACK3's 1000,
    2252, 3999, 9047, the window) re-measured. The toy's 36,864,000 / 9000 = 64^2 fits.
8.  The tie (math B4: kept only on D = 2 mod 4 with constant teeth) is moot for the ten-gear S: S is symmetric
    by construction, there is no tie to hold. It bears only on FRAME16's 16-gear frame.
9.  The tip's cause (phys Q2), right for W <= 0 only: the ten slots' free modes, chiefly the uniform ones, with
    no restoring force on a periodic board, from random seeds that meet no constraint; no source: nothing in
    the act sources anything. Section 0 agrees with it but does not prove it. Released at rest, W <= 0 falls
    from 551 to 43 and from 562 to 86; at the wide flat it is 0 in all six runs. The Spokes' bound and det S
    fail at rest too (bound 1415, 1516, 238; det S crossings 868, 754, 137, the three flats). At the wide flat
    at rest the bound's failures grow with the spread (0, 39, 199): the seeded waves' amplitude against the
    margin. Only the margin (a) reaches that; (b), (c) and (d) do not. The proposals are DERIVED, not built,
    OPEN:
    (a) the flat with margin (section 0 uses it);
    (b) the de Donder sums d_m G^mn = 0, four whole, linear, local sums;
    (c) seeds that meet the constraints;
    (d) a non-periodic flat boundary.
10. No light on the board. The board's wave's first arrival is octahedral and depends on strength (phys B5: a kick
    on 33^3 first moves axis distance d in round d, the diagonal (d, d, d) in round 3d, at K = 10^12; at
    K = 10^3, d = 7 in round 14). On ONELAW's well (D2'), the first whole-count motion crosses 100 flat sites in
    185 rounds and 100 deep in 754, against the peak's 200 and 797 (ONELAW read the peak). MEASURED: the board's
    wave's first motion depends on its threshold. A click-world light must define its front in clicks, with a
    threshold, and be tested for isotropy and for independence from strength. Owed.
11. Big Pic's L: the refusal stands. Reading L as the frame's 00 leg with W = det(P) L^4 gives one slot two W's,
    equal in 2 of 216 cases. What his L would need: it is no frame leg. As a gear, W = det(P) L^4 makes the ten
    slots no frame's reading: (1, 3) is not free (P definite and L /= 0 become laws), and his density det(P) L^2
    holds only at 0i = 0. As a name, L^2 = S00 at unit grips (S00 = L^2 l1 l2 l3 in general), N = 1/L is a
    reading of the clock, and S is the only gear.

## What is DERIVED, what stays OPEN

DERIVED as a reading; the act is not built; the spring equals the density only on det S's laid sign; OPEN. One
law as a reading: the slots are the act's densitized coefficients, read through the frame: W = Re(s0 s0), grips
-Re(s_i s_j), spring = o det S m^2, o one chosen lay orientation. Big Pic's products are its static diagonal case
(DERIVED; the 216 an identity check, S00 chosen to match). The 24 by conjugation (DERIVED; 7200 identity
checks). The run back exact on the free act at the fixed dial 18 and on static frames (21 runs), not on the joined
act. The clock's beat slowed by N and the board's wave by N^2 on a well that deepens S00 alone (clock facts,
MEASURED on four boards with the physicist's; the N^2 needs the slots' own law leaving the grips, OPEN below).
OPEN:
- W >= 1;
- the Spokes' bound with the shift (eight whole sums) and P definite (three leading minors);
- det S of the laid sign o (one global, chosen at the lay); no free act holds it;
- the joined act itself (not built);
- the chart's singular set;
- the slots' own law leaving the grips (r = 0, term 6): the law the board's wave's N^2 needs;
- the act reading 0i;
- the widened given-first sub-step (an act change);
- the units re-laid;
- the four proposals of item 9;
- every physics reading (gamma, redshift, light, the cone, the delay, the bending, the front): owed to the click
  world, read there by Big Pic's methods. Owed there too, by the owner's 01:0x requirement:
  (a) a clock that travels counts less between two meetings: at several speeds, along an axis and along the
      body diagonal (the board's lattice is a candidate preferred frame);
  (b) light's two-way speed the same in every direction for a lab moving against the board, not only the
      front's isotropy;
  (c) the same slowing for every clock at one depth, for every m and every train (on the board m cancels in
      spring / W, a clock fact only);
  (d) the second order, beta (the density road is first order only);
  (e) a well made by the act from its matter's clicks, not laid by hand.
