# Run 14: Newton's periods re-read by the moving detector with mass. The steps between click and click, the pins before the run, the checks before the run (FAIL Runner D, 2026-09-23)

The order (the Boss, 2026-09-23, record 1128 (a) item 4 of
[the log](../../LOG_2026-09-20.md); the model owner's words, records
1043, 1046, 1098 and 1128: Newton read at a moving detector with mass,
from clicks; the FAIL rows turned by the algebra; before any run the
algebra must confirm that the run's steps are exactly the steps between
click and click). The row: 14 of the paper's confrontation table, Newton's
periods, FAIL (T(24) / T(12) = 1.677 under the one constant and 1.512
under the line drive against the pin 2.00 +- 0.18; the verdict word
READING in `docs/designs/fail_rows/WHAT_IS_MISSING.md` section 1.13, on
the branch `fail-rows` (PR #964) until it merges). The design, reviewed (read AD, record 1117) and merged:
[NEWTON_ON_THE_SIDE.md](../newton_clicks/NEWTON_ON_THE_SIDE.md) on
`main` at da86e383, Side A (sections 3 and 4.1, 4.3), with
[NEWTON_FROM_CLICKS.md](../newton_clicks/NEWTON_FROM_CLICKS.md) section 3
beside it. Base commit `e404baa19fe28d978a775862bcbea699ff52c40b`
(`origin/main`, "Merge pull request #965"). This file is step 1: the
chain of steps, the pins, the checks and the side's files, before any
run; section 9 holds the readings after the owner's go (step 2). No law
change, no engine line, no key, no default; nothing enters the paper from
here.

**The kinds of every number** (AGENTS.md, the measurement rule):
DETECTOR, a detector's click or count, the only kind pinned or compared;
GAMEBOARD, the host's view (a tick, a body's record, a presence, an age
moment at a Node, the books), a diagnostic, never pinned or compared;
COMPUTATION, arithmetic on readings or the algebra's closed forms, no
run; HOST, a cost or a time of the machine; CONVERSION, an Outside number
made from counts by a named reading. Every result is stated as matching a
form, never as being it; Newton's, Einstein's and Shapiro's forms appear
only as the things compared with.

**The symbols, named once.** Q the label's scale, 64; S the width of the
push (the world key `width`), 1; M_row the massive row's content per row
(the family key `quantum`), 21; p the magnitude of the row's label (the
lamp key `momentum_magnitude`), 71; E'_0 = Q S M_row the row's rest
energy in whole units, 1344; E'_D = isqrt(E'_0^2 + 3 p^2) its pace wall,
1349; k the rung of the ladder of velocities (counts per Link), 19; v the
row's pace in Links per count, p / E'_D = 1 / 19 on the rung; c the pace
of a light row, 1 / sqrt 3 Links per interval (c_h = 32 / 55 on a
heading); tau the age of a row; m(tau) the row's Links by the age tau;
n / d the suspension pair (the world key `suspension`), [1, 4096]; a_tau
the age moment a wall or a clock reads (amount times age summed over the
rows of other numbers at a Node); k_a(b) = (n / d) a_tau(b) the crowd's
stretch at the impact distance b, 6.95 x 10^-4 at the held mass 2^10
(0.0445 at 2^16); b the impact distance, 6; L the Links from the mass's
plane to the receivers, 26 = r_1 = r_2; L_line the Links from the lamp to
the receivers, 52; n_A the lamp's own count and the ordinal the row
carries (`record` mod 2^32); n_B the receiver's own count (`clock`);
T the arrival count of a click, n_B less the ordinal; gamma_PPN the
world's `optical`, 1 declared; c_f = 1 + gamma_PPN the flight's
coefficient in the age wall's set, 2; alpha the deflection angle; **P**
a pushed row's whole momentum and **W** its push accumulator; **V** the
label flow of the crowd's arrivals at a Node; ln the natural logarithm,
ln(4 r_1 r_2 / b^2) = 4.319; W a window's length in counts; u / c the
name of the ratio of two count ratios, 0.0912 on the rung.

## 0. What step 1 found, at the top

1. **The run's steps are the steps between click and click**, restated
   in section 1: one click at each end (the lamp's release at its own
   count; the receiver's click at its own count), and between them only
   declarations of the world file and computations on the law's integers.
   Every pin of the design re-derived from the integers (section 2)
   returns the design's numbers: the control 979 exactly, the advance
   -40.5 (the wall +0.68, the push -41.19), the centroid 4.39 (4.46 under
   the crossing count), the light row's lever-arm centroid 4.63 against
   5.47 toward the mass, its read delay +3.0 (the wall's +3.96 less the
   two clocks' stretch at 26.7 Links from 2^16), the mark (c / v)^2 of
   Newton's form 60.2 (the massive row's push advance over its own wall's
   delay). The physics-rule reviewer's GO of 2026-09-23 (the Boss's word
   of 01:30Z) is subject to three lines, folded here before the run: the
   light delay pin +3.0 (step 13), the mark named as the row's own (step
   10) with the clause on the presence read (step 5), and Side B's drive
   (section 7).
2. **Two steps the design did not list, found by the algebra before the
   run, both on the receiver's own count, neither a number of the chain:**
   (a) *The birth's convention, one count* (step 6; the design's own edge
   case): a lamp at the content K births at its first self-creation,
   skips the second once (its turn accumulator at K - M_row is below the
   wall K for one count) and births at every one after, so the ordinal
   lags the lamp's own count by one from the third self-creation on, and
   every click after the first reads the flight's count plus one (979 on
   the first click, 980 on the rest; read on a bar of six Links in the
   tool's test: 105 then 106; the light lamp 10 then 11). The advance and
   the delay are differences of two such counts and carry no convention.
   (b) *The receiver's count is stretched by the rows it receives* (step
   5): a body's clock counts the age moment of the other numbers' rows at
   its Node on every table entry unless the entry reads `presence`
   (clock-age-v1, `measured.count_component`), and the arriving row is
   such a row at the receiver's Node for the interval it ends there.
   Under the design's `reads: "age"` every click stretches the receiver's
   count by the row's age over d, 979 / 4096 = 0.239 of a count, so n_B
   less the ordinal falls by one every four clicks and no click of the
   control can read 979 (read on the bar: the count one behind the tick
   from the 41st click, 105 / 4096 per click). **The one declaration
   changed on the side, named and nothing else moved:** the receivers'
   entry for the lamp's family reads the presence (`{"rule": "measure",
   "reads": "presence"}`), under which the stretch is 1 / 4096 per click
   (0.1 of a count over the window of 400 clicks) and every pin of the
   design stands; the row's age is then not on the click line and is in
   no pin (the arrival count is n_B less the ordinal, the design's
   reading). The physics-rule reviewer reads this change against the
   design before the Boss's go.
3. **The checks of the design's section 6** (section 4): the receiver
   plane of 1681 bodies with tables costs 37 to 50 ms per interval at the
   start on this host (HOST; series K's plane of the same 1681 bodies
   16 to 25 ms per interval on the registered machine), so the three
   worlds of 1400 intervals are minutes each and the declared plane
   stays; the pair [1, 4096]'s bound at the declared p, M_row and d holds,
   by an arithmetic that differs from the design's line (iv): the wall's
   square X = R^2 + 3 abs(**P**)^2 of a pushed row must stay under 2^63,
   and the rest term R = Q d M_row E'_0 = 2^32.8 alone would put R^2 at
   2^65.6 at a gcd of 1; the gcd the push leaves is at least 16 (Q d M_row
   = 2^18 x 3 x 7 and the unit weight 1360 = 2^4 x 5 x 17 share 2^4), so X
   is at most 2^57.7, under the bound by 2^5.3; the light world's X at most
   2^51.2.
4. **The side's files** (sections 5 to 7): the three worlds of Side A
   under `examples/events/newton_side/` with their generator and the
   register of pins; the readings tool `tools/newton_side_readings.py`
   with its test on hand-written click lines and a bar run; Side B's two
   numbers (the width 404, the launch momentum 4 x 404 x M) in
   `examples/events/orbit_lamp/make_worlds.py` writing the k17 pair and
   its controls, the registered worlds untouched. No engine line.
5. **Step 2, run on the GO of 2026-09-23** (section 9): the control
   PASSES every pin (979 then 980 on every click, the line's end, no
   face click, the ratio 1.000: the rung whole on the board); the mass
   and light worlds FAIL every conditional pin by 2.5 to 4 (the advance
   -115 against -40.5, the centroid 11.0 against 4.39, the light row's
   18.9 against 4.63 and 5.47, its delay +21 against +3.0), the deciding
   pin answering with its fourth line; the cause by the primitive, read
   as a GAMEBOARD diagnostic and never pinned: the crowd's age moment
   along the row's line and at the two clocks is the comb of the
   Manhattan fan, densest near the mass's x axis where the line's ends
   and both clocks sit, 2 to 35 times the isotropic shell mean the
   conditional pins assumed. No pin moved; Newton's advance and bending
   stay unread at the shell mean's value.
6. **Open, the owner's or the reviewer's** (section 8): the deciding pin
   is the light row's, a run on the go; the word "a read at a body is a
   click" is not needed by Side A (the row's push reads the arrivals at
   its Node as coded, whichever way the word goes); k_a(b) at 2^10 is a
   linear scaling of a GAMEBOARD age moment until a lamp at b reads it.

## 1. THE STEPS BETWEEN CLICKS

The chain of the design's section 1 written as the run's steps, from the
lamp's release to the receiver's click and its own count, the control's
count, the difference and the ratio. Each step is tagged **click** (a
detector's own line: a Node, an ordinal, a count), **declaration** (an
integer of the world file, no run) or **computation** (arithmetic on
those, in closed form, before the run). The run does these steps and no
other; a run that differs refutes a step or finds a rule the chain
forgot.

1. **[declaration] The world.** Series K's open box of 57 x 41 x 41 Nodes;
   the lamp A, a fixed body of the massive family `matter` at (2, 26, 20);
   the held mass, a fixed body of the free phase-less family `m` at (28,
   20, 20), content 2^10, releasing on series E's fan of 290 directions
   under the release [1, 4096] (one row per direction per four
   self-creations, `by_clock(age, 2^10, 2^12)`); the receivers, 1681
   fixed bodies of the paid family `wall` on the plane x = 54, each
   measuring `matter` (the presence read, step 5) and passing `m`; the
   world keys `massive_rows` true, `width` S = 1, `action` 1024,
   `age_bound` 2048, `suspension` [1, 4096], `optical` 1 (c_f = 2, never
   a default), `flow_link` false, `clock_stamp` true, `K` 2^30, `N` 64;
   the family's `quantum` M_row = 21 and `massive` true; the lamp's
   `momentum_magnitude` p = 71, `rate` [1, 1], `wheel` [2531, 4096],
   `directions` [[1, 0, 0]], its content the world's K. The control: the
   same without the held mass. The geometry: b = 6, L = 26 = r_1 = r_2,
   L_line = 52.
2. **[computation] The rung.** E'_0 = Q S M_row = 64 x 1 x 21 = 1344;
   E'_D = isqrt(1344^2 + 3 x 71^2) = isqrt(1806336 + 15123) =
   isqrt(1821459) = 1349 (1349^2 = 1819801 <= 1821459 < 1350^2 =
   1822500); 1349 = 19 x 71: the row sits on the rung k = 19 exactly. The
   ladder's quantum at k = 19 is 1 / (19 x 20) = 1 / 380 Links per count.
   u / c = (1 / 19) / (1 / sqrt 3) = 0.0912, a name for the ratio of two
   count ratios, no input.
3. **[click] The release.** At the lamp's self-creation with its own
   count n_A, its turn 1 (the content K over the wall K: exactly 1 at the
   first birth; step 6 for the rest), the lamp births one row of `matter`
   on the heading [1, 0, 0]: the row carries the ordinal n_A on its record
   (`record` = the lamp's number x 2^32 + the ordinal, from 1), the label
   **p**_D = (71, 0, 0), the content 21 and the age 0. Each birth costs
   the lamp M_row = 21 of its content.
4. **[computation] The flight.** One accumulator at the rate 2 abs(**p**_D)_1
   = 142 against the wall 2 E'_D = 2698, started at E'_D = 1349 (the
   half-wall start): the row's Links by the age tau are m(tau) =
   floor((142 tau + 1349) / 2698) = floor((2 tau + 19) / 38), one Link per
   19 counts with no remainder (2698 = 19 x 142). The L-th Link at tau =
   19 L - 9: the 52nd at 979, the 51st at 960 (the difference 19 exactly,
   the least step of record 1050 (iii)). Each Link is one Node along the
   digital line of the heading; the path is straight, 52 Links on a
   57-Link box, so no row reaches a face (a face click of the row is the
   control's FAIL).
5. **[declaration] What acts on the row and on the clocks between the
   ends.** In the control nothing: no crowd at any Node, the wall's
   stretch (d + c_f n a_tau) = d and the push **V** = 0, the row walks
   integer for integer, and every clock counts one per interval (the
   receiver's clock counts the presence of the rows it receives, 1 per
   click over d = 4096: 0.1 of a count over the window; under the
   design's `reads: "age"` it would count their age moment, 979 per click
   over 4096, a quarter of a count per click, the step of section 0 (2)
   (b); the key `reads` selects the component the receiver's clock
   counts, a reading aid of the external thing (`count_component`); it
   touches neither the row's push, which reads the crowd's arrivals at
   its Node under either setting, nor the owner's open word on a body's
   push). In the mass world two rules of the law act on the row, both the
   law's own since the generic entry (record 847), at the pair [1, 4096]:
   the flight in the age wall's set at c_f = 2 (the wall stretched by the
   crowd's age moment at the row's Node) and the push on a paid row by the
   crowd's arrival flow (**W** -= n x weight x **V**(x) at every Node x
   it visits, the weight per unit (E'_D^2 + 3 gamma_PPN p^2) // E'_D =
   1360, the label following the line of **P** = Q d M_row **p**_D + **W**
   by Bresenham, the pace wall re-formed as E'(**P**) by the split
   ladder); and on the two clocks at the ends the age moment of the mass's
   rows at their Nodes (the lamp at 26.7 Links, the receivers at 26.0 to
   26.7 Links from the mass), k_A and k_B of order 1.6 x 10^-4 per
   interval at 2^10.
6. **[click] The receiver's click and its own count.** The row's 52nd
   Link lands at the receiver body B whose Node is the line's end (54,
   26, 20 in the control); B's table measures `matter`: the click line
   carries B's number and Node, the row's ordinal, B's own count n_B
   (`clock`, its self-creations to that interval) and the entry's
   reading. The birth's convention (section 0 (2) (a)): the lamp's turn
   accumulator at the rate content against the wall K is at K at the first
   self-creation (a birth, the content falls to K - 21), at K - 21 at the
   second (no birth), at 2 K - 42 at the third (a birth, the surplus K -
   42 kept) and above K at every one after within any run of this length
   (the deficit reaches K after about 2^30 / 21 births), so the ordinal
   lags the lamp's own count by exactly one from the third self-creation
   on, and n_B less the ordinal reads the flight's count on the first
   click and the flight's count plus one on every later click; the same
   in every world of the series, so the differences below carry no
   convention. The window of the reading: the clicks whose n_B is at or
   after 919 (the design's control count less 60), about 400 clicks.
7. **[computation] The control's count.** T = n_B - ordinal = 979 on the
   first click, 980 on every click after it, every one alike (the rung
   whole, no remainder); the pace over the window, L_line over that count,
   52 / 979 = 0.05311 against 1 / 19 = 0.05263 within the one band rule's
   2 / W = 2 / 979 = 0.00204 (the difference 0.00048); the arrival Node
   the line's end, the centroid (26, 20) exactly; the count ratio of
   consecutive clicks at B, B's counts apart over the ordinals apart,
   1.000 (1 - 1 / 4096 by the presence read).
8. **[computation] The wall's delay in the mass world.** At the Node x the
   row's accumulator gains 142 d per interval against 2698 (d + c_f n
   a_tau(x)), so it spends per Link (E'_D / p) (1 + c_f k_a(x)) counts in
   the mean with k_a(x) = (n / d) a_tau(x), the remainder kept on the row;
   the excess over the control from the wall alone is c_f (1 / v) times
   the sum of k_a(x) over the path's Links, and in the shell mean along the
   straight path (k_a(x) = k_a(b) b / r, r_1, r_2 >> b) c_f (b k_a(b) / v)
   ln(4 r_1 r_2 / b^2) = 2 x (6 x 6.95 x 10^-4 / 0.05263) x 4.319 = 2 x
   0.07927 x 4.319 = +0.68 counts. Shapiro's form is the thing compared
   with, with c_f (n S / d) in place of nature's 1 + gamma_PPN. The wall
   reads a presence and carries no velocity term under either count of the
   deciding question.
9. **[computation] The push's advance in the mass world.** The push's
   radial part raises abs(**P**) and with it the pace v = p / E'(**P**)
   (d v / d p = E'_0^2 / E'^3, 1 / E'_0 for a slow row, 0 for a light
   row); in the shell mean at first order in k_a the row's fall has the
   constant G_row = (n S / d) (1 - v^2 / c^2) (1 + gamma_PPN v^2 / c^2) G
   and the arrival is earlier by (1 - v^2 / c^2) (1 + gamma_PPN v^2 / c^2)
   (b k_a(b) / v) (c^2 / v^2) ln(4 r_1 r_2 / b^2) = 0.99169 x 1.00831 x
   0.07927 x 120.33 x 4.319 = 41.19 counts (v^2 / c^2 = 0.00831, (c /
   v)^2 = 120.33). Newton's advance of a slow particle in a 1 / r
   potential, -(G M / v^3) ln(4 r_1 r_2 / b^2), is the thing compared
   with. The row's push reads the arrivals at its Node (the presence
   class) as coded, so this step carries no velocity term whichever way
   the deciding question goes.
10. **[computation] The difference and the ratio.** T_mass - T_control =
    +0.68 - 41.19 = -40.5 counts on the control's 979: the ratio -0.0414.
    The mark of Newton's form: the massive row's push advance over its OWN
    wall's delay in its world, 41.19 / 0.68 = (c / v)^2 (1 - v^2 / c^2)
    (1 + gamma_PPN v^2 / c^2) / c_f = 120.33 x 0.99993 / 2 = 60.2, a
    COMPUTATION of two closed forms the run reads only as their sum
    (-40.5); the row fell as a slow particle, whose push outweighs its wall
    by (c / v)^2 (the light row's push, at v = c, adds nothing to its
    wall). It is not the advance over the light row's delay of the light
    world: that row is read at 2^16 and this one at 2^10, and at equal
    k_a(b) the advance over the light row's delay would be (c / v)^3 /
    c_f, about 660. The two clocks at the ends, the lamp and the receiver,
    both at 26.7 Links from the held mass, count at 1 / (1 + k_a(b) b /
    26.7) = 0.99985 of the tick at 2^10, which moves the massive pins by
    0.15 of a count, inside the bracket 3.5. The first-order margin:
    8 per cent of the advance, 3.3 counts, with the held mass's grain at
    2^10 (one row per direction per four self-creations, the crowd's shell
    every four intervals) inside it: the bracket 3.5.
11. **[computation] The bending in the mass world.** Per Link the turn is
    (n / d) ((E'_D^2 + 3 gamma_PPN p^2) / p^2) q sin(theta) / (4 pi r^2)
    with the path's integral of sin(theta) / r^2 equal to 2 / b, so alpha
    = 2 k_a(b) (c^2 / v^2) (1 + gamma_PPN v^2 / c^2) = 2 x 6.95 x 10^-4 x
    120.33 x 1.00831 = 0.1687 radians and the centroid of the arrival
    Nodes on the plane moves alpha L = 4.39 pixels toward the mass
    (Newton's 2 G M / (b v^2) for a slow particle the thing compared with,
    the PPN form (1 + gamma_PPN v^2 / c^2) between it and Einstein's light
    form). Under the crossing count the mean place of the turn moves before
    the mass by (pi b / 4) (v / c) = 0.43 Links and the centroid grows by
    alpha x 0.43 = 0.07 pixel to 4.46: inside the bracket 0.5, so the
    massive row cannot separate the two counts at this grain.
12. **[click and computation] The count ratio of consecutive clicks at
    B.** B's counts apart over the ordinals apart of consecutive clicks at
    one receiver: the ratio of B's rate to A's, both clocks in the same
    crowd at 26 to 27 Links from the mass (r_1 = r_2, the symmetric
    geometry), 1.000 within 0.1 per cent in every world (at 2^16 the two
    rates differ by k(26.04) - k(26.68) = 2.4 x 10^-4 per count). The
    design's 0.990 for the light world (the gr_rows design's count ratio
    at 26.7 Links from 2^16) is B's rate against the tick, GAMEBOARD,
    printed by the tool as the receiver's count behind the tick. The line
    of the arrival counts against the ordinals over the window (its
    intercept the flight's count where both clocks were 0, its slope the
    difference of the two rates) is Einstein's step in the middle, the
    count ratio in a crowd, separated from the flight's count.
13. **[click and computation] The light row of the same world.** The
    lamp's family series K's `light` (no `massive`, no
    `momentum_magnitude`), the held mass 2^16 (k_a(b) = 0.0445, the gr_rows
    pin world's), everything else the same. The flight table's first age
    at 52 Links on the heading, ceil((2 x 52 - 1) x 110 / 128) = 89 (55 for
    32 Links); the wall's delay c_f (b k_a(b) / c_h) ln(4 r_1 r_2 / b^2) = 2
    x (6 x 0.0445 / 0.5818) x 4.319 = +3.96 counts (the design's 3.97),
    no advance (E'_0 = 0, the pace fixed by the square's own cap). The
    READ delay is smaller, since both clocks at the ends sit in the crowd
    of 2^16: the lamp and the receiver at sqrt(26^2 + 6^2) = 26.7 Links
    from the held mass, where the stretch is k = k_a(b) b / r = 0.0445 x 6
    / 26.7 = 0.0100 per interval, so the lamp's ordinals and the
    receiver's count both run at 1 / (1 + k) = 0.990 of the tick and T =
    n_B - ordinal reads 0.990 x (89 + 3.96) = 92.0 in the mass world
    against 89 in the control: the pin +3.0 +- 1, not +3.96 (the wall's
    +3.96 at c_f = 2 less the two clocks' stretch; step 5 counted the same
    stretch for the massive worlds at 2^10, where it is 64 times smaller,
    0.15 of a count, inside 3.5); the
    centroid 2 (1 + gamma_PPN) k_a(b) L = 4 x 0.0445 x 26 = 4.63 pixels
    toward the mass under the arrivals count, and under the crossing count
    the lever arm (pi b / 4) (v / c) = 4.712 Links moves it to 4.63 + 0.178
    x 4.712 = 5.47 (the design's -4.63 against -5.47 in series K's sign,
    negative toward the mass); the bracket 0.5, the design's back-reaction
    range 4.73 to 4.81 inside it.
14. **[computation] The chain's identity, restated.** Newton's form is the
    chain's value at r = 1 (the mover's own count against the tick, the
    whole-record hop) and at u / c below the band (the click count's term
    where the declaration puts it, on a BODY's push, note 48, and on no
    row's push and no wall); the side arranges both: the rung k = 19
    (u / c = 0.0912, the term 0.07 pixel on the row's centroid) and the
    reading a ratio of counts on a detector's own record. Nothing in
    steps 1 to 13 expands in v / c.

## 2. The pins, restated by kind with their arithmetic

Every number COMPUTATION before the run; the conditional ones hang on the
one click reading k_a(b) = 6.95 x 10^-4 at 2^10 (0.0445 at 2^16), taken
by the linear scaling of the gr_rows pin world's GAMEBOARD age moment,
DETECTOR only when a lamp at b reads it against a control (series T's
method); a read k_a(b) re-derives every conditional number by the same
forms and refutes nothing. The register beside the worlds:
[expectations.json](../../../examples/events/newton_side/expectations.json).

| The reading | The control | The mass world | The light world | Kind | PASS | FAIL |
| --- | --- | --- | --- | --- | --- | --- |
| the arrival count T = n_B - ordinal, per click, averaged over the window | 979 on the first click, 980 on every later one (step 6), the mean within 1 of 979; every click after the first alike | the advance T_mass - T_control = -40.5 +- 3.5 (the wall +0.68, the push -41.19; steps 8 to 10), the ratio -0.0414; the count itself about 939.5; conditional | the read delay +3.0 +- 1 on the heading's 89 (+ the convention's one): the wall's +3.96 at c_f = 2 less the two clocks' stretch, the lamp and the receiver both at 26.7 Links from 2^16 counting at 0.990 of the tick, so T_mass = 0.990 x (89 + 3.96) = 92.0 against the control's 89; no advance (step 13); conditional | DETECTOR (n_B under `clock_stamp`, the ordinal); the tick GAMEBOARD beside | inside; the mass world earlier than the control | a control off 979 by more than one, or two control clicks after the first differing (the rung not whole): the run stops; the mass world later than the control (the wall without the push: no fall); an advance off by more than the margin; a light row sped up |
| the pace over the window, L_line over T | 52 / 979 within 2 / 979 of 1 / 19 (the one band rule) | the same to first order (the push's radial part raises v by 4 per cent along the path in the mean: reported, not pinned) | 52 / 89 against c_h = 32 / 55 (reported) | DETECTOR (a ratio of counts) | inside the band | outside it in the control |
| the arrival Node: the centroid on the plane, pixels toward the mass | 0.00 exactly, the line's end (26, 20) | 4.39 +- 0.5 (4.46 under the crossing count: not separable) (step 11); conditional | 4.63 +- 0.5 under the arrivals count against 5.47 +- 0.5 under the crossing count (step 13): the deciding pin; conditional | DETECTOR (the click's Node) | inside; the light row inside one and outside the other | off both counts by more than the bracket (the straight-path form or the read k_a(b), not the count); a control off its Node |
| no click of the family on a face | none | none | none | DETECTOR (a face click) | none | any: the row left the board (the control's FAIL; a capture or a turn in the others) |
| the count ratio of consecutive clicks at one receiver | 1.000 (1 - 1 / 4096) | 1.000 within 0.1 per cent | 1.000 within 0.1 per cent (both clocks in the same crowd; 0.990 against the tick, GAMEBOARD) | DETECTOR | within 1 per cent | off by more than 1 per cent |
| the line of T against the ordinal: the intercept, the slope | 979 + 1 - (the first click's share), 0 | the intercept the count, the slope k_A - k_B of order 10^-5 | the slope about -2.4 x 10^-4 per ordinal | COMPUTATION on DETECTOR counts | reported | |
| k_a(b), the one reading the numbers hang on | 1.0000 | 1 + 6.95 x 10^-4 | 1.0445 | DETECTOR when read (not by these three worlds) | a read k_a(b) re-derives the conditional pins | none |

What PASS means: the reading matches Newton's form for a slow particle
(the advance's (c / v)^2 and the bending's 2 G M / (b v^2)) beside
Einstein's light forms in the same world, with the constant n S / d in
front; not a comparison with nature's G. What FAIL means: the law's
massive row does not fall as a slow particle, or the flight's rung is not
whole, or the wall acts without the push.

## 3. The deciding pin, and what each outcome means

The deciding question (NEWTON_FROM_CLICKS.md section 2; the design's 3
(a) and 3 (c)): which count a ROW's push takes, the arrivals at its Node
(the presence class, the law as coded, no velocity term at first order)
or the crossings of world lines (the click count's term (1 + u / c), as
note 48 puts it on a BODY's push). The massive row cannot separate them
(4.39 against 4.46, inside the bracket 0.5); the light row of the same
world can: its lever-arm centroid 4.63 pixels toward the mass under the
arrivals count against 5.47 under the crossing count, the bracket 0.5.

| The light row's centroid reads | The answer | What follows |
| --- | --- | --- |
| inside 4.63 +- 0.5 and outside 5.47 +- 0.5 | the row's push reads the arrivals at its Node: the law as coded; the click count's term sits on a body's push (note 48) and on no row's | Newton's advance and bending of the massive row are the presence class's, as pinned; the term on a BODY stays Side B's question (the advance per turn on the ordinals) |
| inside 5.47 +- 0.5 and outside 4.63 +- 0.5 | the row's push counts the crossings: the term (1 + u / c) is on a row's push too | the row's forms carry the term; the massive pins move by 0.07 pixel (inside their bracket) and the lever arm is the term's signature on a row; a finding against BEAM_LAW note 48's reading of the code, for the reviewer |
| inside both | the bracket does not separate them at this grain (the back-reaction's range 4.73 to 4.81 and the fan's whole steps) | no verdict on the count; a larger b or L, on a later order |
| outside both | the straight-path form at r_1 = r_2 = 26 (the 0.6 per cent), or the read k_a(b) at 2^16, is refuted, not the count | re-derive with the lamp-at-b reading; no verdict on the count |

The control's own FAIL, before any of this: a control off 979 (by more
than the birth's one count), or two control clicks after the first
differing, refutes the rung and the run stops and reports (the order).

## 4. The checks of the design's section 6, done before the run

**The receiver plane's HOST cost at the declared size.** Series K's
plane, the same 1681 bodies of `wall` with tables on x = 54, ran 400
intervals in 6.5 to 9.9 s on the registered machine
([VALIDATION.md](../../VALIDATION.md), series K), 16 to 25 ms per
interval. On this host, the three worlds loaded and stepped through the
API for 40 intervals (HOST, no reading, no run of the pins; the rows in
flight at the end in brackets): the control 36.7 ms per interval [39
rows of `matter`], the mass world 39.7 ms [39 `matter`, 2896 `m`], the
light world 50.3 ms [39 `light`, 11424 `m`]. The steady state holds about
979 massive rows in flight (one per interval, each 979 intervals) and the
crowd's rows, and the push on a pushed row is a Python loop per row per
interval (`momentum_pair`), so the estimate is 50 to 150 ms per interval,
1 to 4 minutes per world of 1400 intervals: within the host, the declared
plane stays, nothing moved.

**The pair [1, 4096]'s bound at the declared p, M_row and d** (the price
note's line (i), [GENERIC_BENDING_PRICE.md](../one_wall/GENERIC_BENDING_PRICE.md);
the engine's `momentum_pair`: **P** = Q d M_row **p**_D + **W** and R =
Q d M_row E'_0, both over their gcd, X = R^2 + 3 abs(**P**)^2 tested
against the working bound 2^63 by division before each term is formed,
T = isqrt(X Q^2) by the split ladder, then 2 T <= 2^63 / d). At **W** =
0 the gcd is Q d M_row = 5505024 itself and the pair is the family's
triple, (71, 0, 0) and 1344, X = 1821459. Under a push **W** is a
multiple of the unit weight 1360 = 2^4 x 5 x 17 (times n = 1 and the
integer flow **V**; 28560 = 2^4 x 3 x 5 x 7 x 17 with the content's 21
in it), and Q d M_row = 2^18 x 3 x 7, so every component of **P** and R
is a multiple of 2^4: the gcd is at least 16, R over it at most
7398752256 / 16 = 2^28.8, R^2 at most 2^57.6, and with 3 abs(**P**)^2 at
most 2^54.2 (a push of the order of the label's own term, abs(**P**)
under 2 x 390856704 / 16 = 2^25.5 per component) X is at most 2^57.7,
under the bound by 2^5.3 (a gcd of 1, which the weight's factor forbids,
would put R^2 alone at 2^65.6 and refuse: the design's line (iv) bounded
Q d M_row = 5.5 x 10^6 against 2^24.7 and not the rest term, so the
conclusion stands by a different arithmetic, stated here for the
reviewer). 2 T = 2 isqrt(X Q^2) at most 2^35.9 against 2^63 / 4096 =
2^51.
The light world (content 1, R = 0): **P** = 2^24 on the heading, 3
abs(**P**)^2 at most 2^51.2, the price note's refusal at d = 65536 not
reached at 4096. Both checked by arithmetic on the declared integers
(COMPUTATION), the massive world's push also exercised on the bar of the
tool's test (balanced, no refusal).

**The load condition (DESIGN.md's M3).** The lamp's content is the
world's K, the turn exactly 1 at the first birth; a massive birth at a
turn other than 1 is refused at the birth naming the lamp; each birth
costs 21, the turn falls to 0 once at the second self-creation and never
again within 1400 intervals (step 6); the preflight of the three worlds
(`validate_configuration`) is valid with no issue, 1682 to 1683 measured
events, 1400 ticks, and the record's hypotheses are `amplitude-v1`,
`massive-rows-v1` and `bohr-v1` (the last the turn by momentum the key
`action` names, required with `massive_rows`; no key of a hypothesis
beyond the identity the design declares).

## 5. The world files of Side A

`examples/events/newton_side/` ([README.md](../../../examples/events/newton_side/README.md)):
`control.json`, `mass.json`, `light.json`, written by `make_worlds.py`
from series K's generator (the box, the fan, the definitions the
families come from) with the design's section 4.3 keys, and byte-checked
against the generator by the test (a) of `tests/test_newton_side_readings.py`
(the shipped document equals the generator's, key by key; the rung's
integers 1344, 1349 = 19 x 71, 979 and 89; the lamp on the rung; the
held mass at 2^10 and 2^16; the receivers' table; every pin of the
register equal to the closed form). The keys as declared, one line each:

| Key | Declared | The design's section 4.3 |
| --- | --- | --- |
| `shape`, `boundary` | [57, 41, 41], open | the same |
| `ticks` | 1400 (the control's 979, then a window of about 400 clicks) | not stated; chosen here |
| `K`, `N` | 2^30, 64 | the same |
| `release`, `suspension` | [1, 4096], [1, 4096] | the same |
| `width`, `action`, `age_bound`, `massive_rows` | 1, 1024, 2048, true | the same |
| `optical`, `flow_link`, `clock_stamp` | 1, false, true | the same (`flow_link` stated either way) |
| the families | `matter` {21, massive}, `wall` {1}, `m` {0, charge 0, no phase}; `light` {1} in the light world | the same |
| the lamp | (2, 26, 20), fixed, content K, `rate` [1, 1], `wheel` [2531, 4096], `directions` [[1, 0, 0]], `momentum_magnitude` 71 (none on `light`), `table` {m: pass} | the same |
| the held mass | (28, 20, 20), fixed, 2^10 (2^16 in the light world), the fan of 290 | the same |
| the receivers | 1681 bodies of `wall` on x = 54, fixed, `table` {the lamp's family: {measure, reads: presence}, m: pass}, no `detectors` list | `reads: "age"`: the one departure, section 0 (2) (b) |
| `directions` | the fan's 284 non-headings | the same |
| the model ids | `beam-newton-side-<name>-v1` | not stated |

## 6. The readings tool and its test

`tools/newton_side_readings.py`: Outside arithmetic on the receivers'
click lines alone (the receiver's number and Node, `clock`, `record` mod
2^32, the reading), nothing of the engine: per world the arrival count
per click (clock less the ordinal), its mean, the first ordinal's, the
least and greatest of the rest and the spread over the window; the pace
L_line over that count with the band 2 / W; the centroid of the arrival
Nodes in y and z and its shift toward the mass against the control's read
centroid (or the line's end where no control run is read); the count
ratio of consecutive clicks at the receiver that clicked most; the faces'
clicks of the family; the line of the counts against the ordinals (the
intercept and the slope); the control's count derived from the world's
own integers before it is read (the massive triple; the flight table);
the tick and the receiver's count behind it printed as GAMEBOARD; every
verdict against the register's pins, PASS or FAIL, none moved; and the
deciding pin's answer in the light world as one of the four lines of
section 3. The test (`tests/test_newton_side_readings.py`): (a) the
worlds and the register against the generator; (b) hand-written click
lines (400 control clicks at 979 on the line's end read the pin, every
click alike, the pace inside the band, the centroid exact, the ratio 1;
400 mass clicks 40 counts earlier on the Nodes 4 and 5 pixels toward the
mass read the advance and the centroid; 400 light clicks 5.25 pixels
toward the mass read the crossing count's pin and not the arrivals'; a
pass, a click of another family, a line without a record and a face
click are left out or counted where they belong); (c) a bar of six Links
run in-process for 160 intervals, the receivers reading the presence:
every click carries `clock` and `record`, the count 105 = 19 x 6 - 9 on
the first click and 106 on every later one (the birth's convention), the
light lamp's 10 then 11, the pace inside the band, no face click; and the
same bar under `reads: "age"`, the receiver's count one behind the tick
from the 41st click (the step of section 0 (2) (b)).

## 7. Side B: the two numbers in orbit_lamp's generator

`examples/events/orbit_lamp/make_worlds.py`: the width S = 404 and the
launch momentum p = 4 x 404 x M in label units (n = p / (Q M) = 25.25),
the rung k = 17 exact under the per-axis drive of `main` today (the pace
abs(p_a) / (Q S M + abs(p_a)) = 1616 / (25856 + 1616) = 1 / 17 exactly;
S = A k (k - 1) = 1.4838 x 272 = 403.6 under the key `flow_link`, the
balance 404 / 272 = 1.485, 0.1 per cent off A), writing the pair
`r12_k17.json`, `r24_k17.json` and their controls `r12_k17_control.json`,
`r24_k17_control.json` with `flow_link` and `clock_stamp` true and the
detector line at y = 2 (58 Links below the source; the reviewer's line
(iii) of read AD); the registered worlds and both registers byte
identical (the generator re-run; only the four new files appear). The
pins of the design's section 4.2 stand as written and enter no register
here (the ratio of the first turns on the ordinals 2.00 +- 0.20; T_1 =
1282 and 2564 REPORTED, not pinned; the advance per turn above 1 by the
term, its falsifier equal turns; the controls' escape at the 61st Link,
1037 +- 6 on the probe's own count; the least step one Node per 17
counts); the re-read of `tools/orbit_lamp_readings.py` on the ordinals
and the runs are the later order's. The line drive of PR #907 is not on
`main`; the pins are the per-axis drive's, the drive of `main` today, as
the Boss's note says: the rung k = 17 is the per-axis drive's; when the
line drive is `main`'s default the four k17 files declare
`per_axis_drive` (the moving detector's practice) or the rung is
re-derived from the line drive's wall before any pin.

## 8. What is not done here, and what stays open

- The runs: step 2, on the Boss's go after the physics-rule reviewer's
  read of sections 1 and 5 against the design (the control first; a
  control off 979 or two control clicks after the first differing refutes
  the rung and stops the run).
- The one declaration changed (the receivers read the presence) is for
  the reviewer's word; under the design's `age` the control cannot read
  979 by the law's own count (section 0 (2) (b)), so the run would refute
  the side and not the rung.
- k_a(b) at 2^10 and at 2^16: a linear scaling of a GAMEBOARD age
  moment; the lamp-at-b world that reads it is not among the three (the
  design's section 6) and every conditional pin waits on it.
- Whether a free row's read at a body is a click: the owner's word; Side
  A reads Newton under either answer (the row's push reads the arrivals
  at its Node as coded).
- The exact factor of the crossing count off the axis on the lattice:
  read by no click; the light row's pin is the continuum straight-path
  integral's.
- The window's mean of the light row's count against the fit's intercept:
  both printed; the pin on the mean (+3.0, the read delay), the slope of
  order 2.4 x 10^-4 per ordinal (0.3 of a count over the window) reported.
- Side B's run and its tool's re-read on the ordinals: a later order.
- The value of G and the condition n S = d: declarations; the side
  carries n S / d = 1 / 4096 in front of every form.

## 9. Step 2: the readings (2026-09-23, on the Boss's GO of 01:30Z, the reviewer's three lines folded first)

The three runs, headless, the control first, through `tools/run_series.py`
(the runner's record; `artifacts/newton_side/`, under the 24-hour
retention): every world completed its 1400 intervals with the books
balanced at every tick; no click of the lamp's family on any face; every
number below a DETECTOR reading off the receivers' click lines, a
COMPUTATION on them, a GAMEBOARD diagnostic labelled so, or a HOST time;
no pin moved after the run; every FAIL written as FAIL with its cause by
the primitive.

| World | HOST | Digests (state, ledger, events) | The receivers that clicked |
| --- | --- | --- | --- |
| `control` | 78.8 s | 22fdb6c655bd, b7c6c3a77211, e08a77b4bf48 | (54, 26, 20) alone, 420 clicks |
| `mass` | 117.5 s | a5568f812dfe, 7b9ff2da5331, 6d4c87ba1a13 | (54, 15, 20) 490, (54, 16, 20) 22, (54, 14, 20) 18, (54, 17, 20) 5, (54, 13, 20) 1 |
| `light` | 139.2 s | bf5f5fb00ab6, e568c6ae5e08, 753d02881330 | (54, 7, 20) 716, (54, 8, 20) 257, (54, 6, 20) 109, (54, 9, 20) 7, (54, 5, 20) 1 |

### 9.1 The verdicts against section 2's pins

| The reading | The control (DETECTOR) | The mass world (DETECTOR) | The light world (DETECTOR) |
| --- | --- | --- | --- |
| the arrival count T = n_B - ordinal | 979 on the first click, 980 on every later one (420 clicks, least 980, greatest 980, spread 0.05); mean 980.0 against 979 +- 1: **PASS**; every click after the first alike: **PASS** (the rung whole, the birth's convention as step 6 says) | mean 864.7 over 525 clicks in the window, the first ordinal's 963, least 844, greatest 965, spread 19.2; the advance against the control's read mean -115.3 counts (the ratio -0.118) against -40.5 +- 3.5: **FAIL** (2.85 times the pin); earlier than the control: **PASS** (a fall, not the wall alone) | mean 111.1 over 1089 clicks, the first ordinal's 113, least 20, greatest 310, spread 79.2; the read delay against the heading's 89 + 1: +21.1 against +3.0 +- 1: **FAIL**; the reading is not a flight count at all but the difference of two clocks' rates (9.2 below) |
| the pace over the window | 52 / 980 = 0.05306 against 1 / 19 = 0.05263 within 2 / W = 0.00204: **PASS** | 0.0601 (reported, not pinned: the push's radial part and the comb) | 0.468 (reported) |
| the arrival Node | the centroid (26.000, 20.000), the line's end exactly: **PASS** | 11.01 pixels toward the mass against 4.39 +- 0.5 (4.46 under the crossing count): **FAIL** (2.5 times the pin) | 18.85 pixels toward the mass against 4.63 +- 0.5 (the arrivals count) and against 5.47 +- 0.5 (the crossing count): **FAIL** both; the deciding pin's answer, the fourth line of section 3: off both, the straight-path form or the read k_a(b) is refuted, not the count (9.2 says which) |
| no click on a face | none: **PASS** | none: **PASS** | none: **PASS** |
| the count ratio of consecutive clicks at one receiver | 1.0000 over 418 counts, every pair 1.000: **PASS** | 0.852 over 444 counts at (54, 15, 20), the pairs from -14 to 23: **FAIL** against 1.000 +- 0.01; not the clocks' (the receiver's count behind the tick 5.4 on average, the lamp's ordinals behind it 5 over the run) but the scatter of the arrival counts themselves (844 to 965) at a receiver whose ordinals are not consecutive (four receivers share the clicks): the grain of the crowd, 9.2 | 0.923 over 982 counts at (54, 7, 20), the pairs 0 to 3: **FAIL** against 1.000 +- 0.01; the two clocks' rates: the lamp's ordinals behind the tick by 207 at the end (0.15 per interval), the receiver at (54, 7, 20) by 286 (0.21 per interval) |
| the line of T against the ordinal (COMPUTATION) | the intercept 980.0, the slope 0.00000 | the intercept 883.0, the slope -0.067 per ordinal (the early ordinals' higher counts and the scatter, not a rate) | the intercept 108.3, the slope +0.005 (the receivers in no crowd at (54, 6, 20) and (54, 8, 20), owed 0, read T = 198 to 281, the lamp's lag alone, while (54, 7, 20) reads T falling from 113 to 21 through the window) |
| the tick (GAMEBOARD) | the first click's tick 980; the receiver's count behind the tick 0.00 | the first click's tick 847; the receiver's count behind the tick 5.4 on average | the first click's tick 114; the receiver's count behind the tick 100 on average |

The tool's verdict line: 0 record checks failed; 9 readings inside, 7
outside, none moved. The control PASSES every pin: the rung k = 19 is
whole on the board (979 then 980 on every click, one Node per 19 counts,
the arrival Node the line's end), which is the run's own confirmation of
steps 2 to 7. The two conditional worlds FAIL every conditional pin by a
factor of 2.5 to 4, and the deciding pin answers with its fourth line.

### 9.2 The cause by the primitive (one GAMEBOARD diagnostic, never pinned)

The conditional pins all hang on one input, the crowd's stretch along
the row's path and at the two clocks taken as the shell mean k_a(x) =
k_a(b) b / r (the design's rung 2, which it marks "a GAMEBOARD limit and
not an input"; the click reading that replaces it, a lamp at b against a
control by series T's method, was not among the three worlds). The
primitive the wall and the push read is the crowd's age moment a_tau at
the Node the row is at, and the primitive the two clocks read is a_tau
at their own Nodes. Both worlds replayed through the API for 300
intervals, a_tau averaged over the intervals 201 to 300 (the crowd steady
from about the 60th interval: 3523 to 3575 rows of `m` in flight through
the mass world's run), against the shell mean d k_a(b) b / r:

| Node (x, y, z) | r from the mass | `mass`: a_tau read, shell mean, ratio | `light`: a_tau read, shell mean, ratio |
| --- | --- | --- | --- |
| (2, 26, 20), the lamp | 26.7 | 12.0, 0.64, 18.7 | 736, 41.0, 18.0 |
| (6, 26, 20) | 22.8 | 20.2, 0.75, 27.0 | 640, 48.0, 13.3 |
| (10, 26, 20) | 19.0 | 26.2, 0.90, 29.1 | 528, 57.6, 9.2 |
| (14, 26, 20) | 15.2 | 0.0, 1.12, 0.0 | 0, 71.8, 0.0 |
| (18, 26, 20) | 11.7 | 8.7, 1.47, 5.9 | 320, 93.8, 3.4 |
| (22, 26, 20) | 8.5 | 3.8, 2.01, 1.9 | 240, 128.9, 1.9 |
| (26, 26, 20) and (30, 26, 20) | 6.3 | 8.5, 2.70, 3.1 | 544, 172.9, 3.1 |
| (28, 26, 20), above the mass, b = 6 | 6.0 | 5.2, 2.85, 1.8 | 336, 182.3, 1.8 |
| (34, 26, 20) | 8.5 | 3.8, 2.01, 1.9 | 240, 128.9, 1.9 |
| (38, 26, 20) | 11.7 | 5.0, 1.47, 3.4 | 320, 93.8, 3.4 |
| (42, 26, 20) | 15.2 | 0.0, 1.12, 0.0 | 0, 71.8, 0.0 |
| (46, 26, 20) | 19.0 | 8.2, 0.90, 9.2 | 528, 57.6, 9.2 |
| (50, 26, 20) | 22.8 | 10.0, 0.75, 13.3 | 640, 48.0, 13.3 |
| (54, 26, 20), the control's receiver | 26.7 | 22.8, 0.64, 35.5 | 736, 41.0, 18.0 |
| (54, 15, 20), the mass world's receiver | 26.5 | 22.8, 0.65, 35.2 (the clock's k = 0.0056 per interval) | 736, 41.3, 17.8 |
| (54, 7, 20), the light world's receiver | 29.1 | 12.5, 0.59, 21.3 | 1152, 37.6, 30.6 (the clock's k = 0.28 per interval) |

The mean ratio along the line is 12.7 in the mass world and 8.2 in the
light world; 1.8 to 3.1 within 6 Links of the mass's plane, where the
advance's and the bending's kernels weigh most, and 9 to 35 at the ends,
where the two clocks sit. So by the primitive: **the crowd of a fan
bounded in Manhattan length is not isotropic**; the 290 directions of
series E's fan are densest in angle near the axes (the Manhattan ball is
an octahedron), and the row's straight line at b = 6 runs parallel to the
mass's x axis, 13 degrees off it at its ends, where the age moment is
tens of times the isotropic shell mean, and 1.8 to 3 times above the
mass; the comb's teeth (the zeros at x = 14 and 42, the peaks at the
ends) are the fan's digital lines (COMB_NOTE: "the field at a Node a
comb, the ring the instrument"; the light bending note's "the beam's
plane is the fan's comb: 3.5 times the shell-mean pins"). What follows,
reading by reading:

- The advance (2.85 times the pin) and the massive bending (2.5 times):
  the path integrals of k_a(x) with the kernels cos(theta) / r^2 and
  sin(theta) / r^2 over a comb whose teeth near the mass are 1.9 to 3.1
  times the shell mean; the factor read is the comb's, not the count's
  (the two counts differ by 0.07 pixel on the massive row, section 2).
  The straight-path condition k_a(b) << v^2 / c^2 is also weaker than
  the design's 8 per cent: at the read k_a it is about 0.2, and the
  first-order margin no longer covers the second order.
- The light row's centroid (4.1 times the pin, alpha read 0.72 radians):
  the same comb at the held mass 2^16, where the deflection is beyond
  alpha << 1 (the straight-path form's own condition), so the fourth
  line: the straight-path form and the read k_a(b) are refuted together,
  the count not separated at this grain; a lever arm of 0.8 pixel cannot
  be read on a centroid moved 18.9 pixels by a comb.
- The light row's delay (+21 against +3.0): the two clocks' rates are
  not the pin's 0.990 but 0.85 (the lamp, k = 0.15 to 0.18 per interval)
  and 0.79 (the receiver at (54, 7, 20), k = 0.21 to 0.28), so T = n_B -
  ordinal is the difference of two clocks running 7 per cent apart and
  falls by 0.09 per ordinal through the window; the receivers off the
  comb's teeth ((54, 6, 20) and (54, 8, 20), owed 0) read the lamp's lag
  alone (198 to 281). Einstein's step in the middle, the count ratio in
  a crowd, is what the light world reads: the ratio 0.923, DETECTOR, is
  the two clocks' k_A and k_B at their Nodes, by the comb.
- The mass world's count ratio 0.852 and its spread of 19 counts: the
  held mass at 2^10 releases one row per direction per four
  self-creations, so the crowd on the line pulses with the period 4 and
  a row born at one phase of the pulse crosses different teeth than a
  row born at the next; the scatter 844 to 965 is that grain, the
  design's own caution ("the crowd's shell is every four intervals and
  its grain is larger than the design's at 2^16"), forty times the 3.5
  the first-order margin allowed.

What this run decided and did not: the rung is whole and the arrival
click reads the flight's count exactly (the control, PASS, the run's
confirmation of the click algebra's steps 2 to 7); the massive row falls
(earlier than the control, PASS) and is bent toward the mass with the
sign of gravity; the size of both is the comb's and not the shell
mean's, so the conditional pins FAIL as written and Newton's advance and
bending remain UNREAD at the shell mean's value; the deciding pin does
not decide the count on this line. Nothing moved; the pins stand as
written for a world whose crowd is read by a click (the lamp at b) or
whose line does not run along the fan's densest angle; which world, if
any, is the owner's word and the physicist's design, not this file's.

### 9.3 The tool's output, verbatim (the record of the run)

```
control (artifacts/newton_side/control/run): 1400 intervals, HOST 78.8 s; the hypotheses ['bohr-v1', 'amplitude-v1', 'massive-rows-v1']
  record check passed: completed
  record check passed: the books balanced at every tick
  COMPUTATION the control's arrival count derived before the read: 979 (the massive triple (M_row 21, S 1, p 71) at 52 Links); the window opens at the receiver count 919
  DETECTOR clicks of `matter` at the receivers in the window: 420 on 1 receiver(s) (420 over the run); the arrival count (clock less the ordinal): mean 980.00, the first ordinal's 979, then least 980, greatest 980, spread 0.05; the pace 52 Links over that count 0.05306 (the band 2 / W = 0.00204); the centroid y 26.000 z 20.000; the faces' clicks of the family none
  COMPUTATION the line of the arrival counts against the ordinals over the window: the intercept 980.00 (the flight's count where both clocks were 0), the slope 0.00000 per ordinal (the receiver's rate less the lamp's: the count ratio in the crowd, Einstein's step)
  DETECTOR the count ratio of consecutive clicks at receiver 1088 (counts apart over ordinals apart, 418 counts): 1.0000; the consecutive pairs from 1.000 to 1.000
  GAMEBOARD the first click's tick 980; the receiver's count behind the tick 0.00 on average (what it owes the crowd; a diagnostic, never pinned)
  PASS the arrival count (DETECTOR): 979.998 against the pin 979 +- 1 (the birth's convention, one count)
  PASS every click after the first the same count (the rung whole): the first ordinal's 979, then least 980, greatest 980
  PASS the pace over the window (DETECTOR) against 1 / 19: 0.053 against the pin 0.0526316 +- 0.00204082 (the one band rule)
  PASS the arrival Node the line's end (the centroid on the lamp's y and z): centroid (26.000, 20.000) against the lamp's (26, 20)
  PASS no click of the family on a face: none
  PASS the count ratio of consecutive clicks (DETECTOR): 1.000 against the pin 1 +- 0.01
mass (artifacts/newton_side/mass/run): 1400 intervals, HOST 117.5 s; the hypotheses ['bohr-v1', 'amplitude-v1', 'massive-rows-v1']
  record check passed: completed
  record check passed: the books balanced at every tick
  COMPUTATION the control's arrival count derived before the read: 979 (the massive triple (M_row 21, S 1, p 71) at 52 Links); the window opens at the receiver count 919
  DETECTOR clicks of `matter` at the receivers in the window: 525 on 4 receiver(s) (536 over the run); the arrival count (clock less the ordinal): mean 864.66, the first ordinal's 963, then least 844, greatest 965, spread 19.16; the pace 52 Links over that count 0.06014 (the band 2 / W = 0.00231); the centroid y 14.994 z 20.000; the faces' clicks of the family none
  COMPUTATION the line of the arrival counts against the ordinals over the window: the intercept 882.96 (the flight's count where both clocks were 0), the slope -0.06736 per ordinal (the receiver's rate less the lamp's: the count ratio in the crowd, Einstein's step)
  DETECTOR the count ratio of consecutive clicks at receiver 638 (counts apart over ordinals apart, 444 counts): 0.8522; the consecutive pairs from -14.000 to 23.000
  GAMEBOARD the first click's tick 847; the receiver's count behind the tick 5.43 on average (what it owes the crowd; a diagnostic, never pinned)
  COMPUTATION the arrival count less the control's (the control's read mean 980.00): -115.34 counts (the ratio -0.1177); the centroid's shift toward the mass 11.01 pixels against the control's read centroid
  FAIL the advance, the arrival count less the control's (DETECTOR), conditional on k_a(b): -115.342 against the pin -40.5 +- 3.5 (the wall 0.68, the push -41.19; the count itself 864.66)
  PASS the mass world earlier than the control (a fall, not the wall alone): -115.34 counts
  FAIL the centroid toward the mass (DETECTOR), conditional on k_a(b): 11.006 against the pin 4.39 +- 0.5 (4.46 under the crossing count: not separable on the massive row)
  FAIL the count ratio of consecutive clicks (DETECTOR): 0.852 against the pin 1 +- 0.01
  PASS no click of the family on a face: none
light (artifacts/newton_side/light/run): 1400 intervals, HOST 139.2 s; the hypotheses ['bohr-v1', 'amplitude-v1', 'massive-rows-v1']
  record check passed: completed
  record check passed: the books balanced at every tick
  COMPUTATION the control's arrival count derived before the read: 89 (the flight table on the heading at 52 Links); the window opens at the receiver count 110
  DETECTOR clicks of `light` at the receivers in the window: 1089 on 5 receiver(s) (1090 over the run); the arrival count (clock less the ordinal): mean 111.14, the first ordinal's 113, then least 20, greatest 310, spread 79.22; the pace 52 Links over that count 0.46786 (the band 2 / W = 0.01799); the centroid y 7.147 z 20.000; the faces' clicks of the family none
  COMPUTATION the line of the arrival counts against the ordinals over the window: the intercept 108.27 (the flight's count where both clocks were 0), the slope 0.00525 per ordinal (the receiver's rate less the lamp's: the count ratio in the crowd, Einstein's step)
  DETECTOR the count ratio of consecutive clicks at receiver 310 (counts apart over ordinals apart, 982 counts): 0.9229; the consecutive pairs from 0.000 to 3.000
  GAMEBOARD the first click's tick 114; the receiver's count behind the tick 100.24 on average (what it owes the crowd; a diagnostic, never pinned)
  COMPUTATION the arrival count less the control's (the derived 89 plus the birth's convention's one count (no control run of this family read)): 21.14 counts (the ratio 0.2349); the centroid's shift toward the mass 18.85 pixels against the control's read centroid
  FAIL the light row's arrival count less its control (DETECTOR): the read delay, no advance: 21.144 against the pin 3 +- 1 (the wall's 3.96 less the two clocks' stretch at 0.9901 of the tick; a light row sped up refutes)
  FAIL the lever-arm centroid toward the mass (DETECTOR) under the arrivals count: 18.853 against the pin 4.63 +- 0.5
  FAIL the lever-arm centroid toward the mass (DETECTOR) under the crossing count: 18.853 against the pin 5.47 +- 0.5
  the deciding pin's answer: off both: the straight-path form or the read k_a(b) is refuted, not the count
  FAIL the count ratio of consecutive clicks (DETECTOR): 0.923 against the pin 1 +- 0.01
  PASS no click of the family on a face: none
0 record check(s) failed; 9 reading(s) inside, 7 outside, none moved
```

## 10. Links

- [NEWTON_ON_THE_SIDE.md](../newton_clicks/NEWTON_ON_THE_SIDE.md)
  (sections 0, 1, 3, 4.1, 4.3, 5 and 6) and
  [NEWTON_FROM_CLICKS.md](../newton_clicks/NEWTON_FROM_CLICKS.md)
  (sections 2, 3 and 6); [MASSIVE_RELEASE_INVENTORY.md](../newton_clicks/MASSIVE_RELEASE_INVENTORY.md)
  (the load condition, the shortest list of declarations).
- `docs/designs/fail_rows/WHAT_IS_MISSING.md` section 1.13 (row 14; on
  the branch `fail-rows`, PR #964, until it merges);
  [DIAGNOSIS.md](../newton_diagnosis/DIAGNOSIS.md) sections 0, 2 and 6.
- [The moving detector's design](../moving_detector/DESIGN.md) section 7
  (`clock_stamp`) and [PREREGISTRATION_V2.md](../moving_detector/PREREGISTRATION_V2.md)
  section 5 (the one band rule); [the gr_rows design](../gr_rows/DESIGN.md)
  section 4 (k_a(b) at the pin world); [the price note](../one_wall/GENERIC_BENDING_PRICE.md)
  line (i).
- [ENGINE.md](../../ENGINE.md), the massive rows, the clock stamp and the
  readings by type; [TERMINOLOGY.md](../../TERMINOLOGY.md), the readings
  (a detector's clock, Inside and Outside); `src/event_universe/events/measured.py`,
  `count_component` (what a clock counts by its entry's `reads`).
- The worlds [examples/events/newton_side/](../../../examples/events/newton_side/README.md);
  the tool `tools/newton_side_readings.py`; the test
  `tests/test_newton_side_readings.py`; Side B's generator
  `examples/events/orbit_lamp/make_worlds.py`.
- The log: records 768, 1043, 1044, 1046, 1047, 1050, 1053, 1095, 1098,
  1113, 1117, 1122 and 1128.
