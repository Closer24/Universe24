<!-- The read-only review of 2026-09-21 of docs/DERIVATIONS_BEAM.md at c181ab74 on claude/derivations-beam (the derivation mathematician's round 9, first pass; docs/LOG_2026-09-20.md record 172); copied from the scratchpad unchanged for the derivation session to apply. Verdict: MERGEABLE AFTER 16 must-fix (8 wrong formulas, false verdicts or dishonest registered comparisons; 5 wrong citations; 3 method and inventory) and 2 should-fix. -->

# Review of docs/DERIVATIONS_BEAM.md (origin/claude/derivations-beam at c181ab74)

Read-only, 2026-09-21. The branch adds three files over its merge base
f89884f0 (DERIVATIONS_BEAM.md, a pointer in DERIVATIONS.md, an index row in
docs/README.md); `src/` is byte-identical between f89884f0 and origin/main
d36f4382, so every `file:line` was checked against the tree the document
names. Every registered integer was looked up in docs/EXPERIMENTS.md, the
world READMEs, docs/LOG_2026-09-20.md (records 102, 105, 123, 131, 138, 144,
148, 153-159), FORM.md, GRAIN.md, HYPOTHESES.md, BEAM_LAW.md and the paper
branch's `paper/click_model/checks/limits.txt`. Every formula and limit that
could be recomputed was (`checks.py`, `checks2.py` beside this file: numpy
only; no engine run). Method checked against DERIVATIONS.md section 0.

## Verdict: MERGEABLE AFTER the must-fix list below (16 items: 8 of class A, 5 of class B, 3 of class C)

No derivation is wrong in a way a fix cannot save. The core results hold and
were reproduced: the encounter counts and their formula table (2.2), the
bar's rates and the doppler-v1 weight, the `|D|^2 / (a S_1)` ratios (2.4),
the nine ring counts N(r) = 32, 40, 48, 68, 112, 112, 144, 200, 264 with
`r / N(r)` and `2 pi r / N(r)` equal to the register's two columns to every
printed digit and the slopes -0.944 / +0.056 (3.2), the arrival ticks 8 ..
69 (3.3), G and k_C (3.3, 3.4), the delay field's constants and the ratio
`sqrt 3 / 2` (5.1), the second-order clock terms (5.2), the deflection
integral `q / (4 N b c)` (5.4), the Born, tables and Tsirelson numbers (6.2),
the Bohr README's j column times `pi / 2` (1.49 .. 5.10, exact) and the
action sum on digital circles (2.03, 2.01, 2.002, 2.000 x pi p r at r = 8 ..
256), the flight accumulator equal to m(tau) on seven directions over 600
intervals with at most one step per interval (1.4).

## A. Wrong formula, false verdict, or a registered comparison not made honestly (must-fix)

**A1. Section 7.1, Young's spacing against record 156.** "delta_y = 4.654 x
44 / 10 = 20.5 pixels, the spacing record 156 pins with the screen's fan
(bright at y = 35 .. 38, 59 .. 61, 82 .. 85 ...)". The pinned bright pixels
are centred at 36.5, 60, 83.5: a spacing of 23.5, not 20.5. The document's
formula is the paraxial one ("to first order in s / D and y / D") and the
pinned fringes sit at y / D = 0.53, where it fails by 13 %. The exact
two-path condition `L_1 - L_2 = +-lambda` with D = 44, s = 10, lambda =
4.654 gives |y| = 23.3, pixels 36.7 and 83.3: the register pins the exact
two-path law, which IS Young's interference; the paraxial `lambda D / s`
is its limit s, y << D. Record 156's own "spacing 20.5 pixels" is the
paraxial number beside a pixel list that shows the exact one. Correct
statement: the verdict "reached in the limit of every direction" stands
for the two-path law; the check must compare the pixels with `L_1 - L_2 =
j lambda` (23.3) and name `lambda D / s` as the paraxial limit only.

**A2. Section 6.1, the cost formula contradicts its own table.** The formula
"cost (units of content h s) = sum over the ends of the rows' amounts = k x
product over the path's splits of (sum_i a_i)" gives 2 x 41 = 82 for the
Mach-Zehnder and 2 x 91 (+ 3 wall rows) = 185 for the two slits; the table
says "2 + 2 + 2 x 41 = 86" and "5 + 2 x 91 = 187", a cumulative count of
every row ever created (born, re-emitted, split), not the amounts at the
ends. One definition must be chosen and the "units per bit" column (86, 30)
recomputed. None of these numbers is a registered integer (the document
says so for GHZ's 729); see C1 for the verdict word.

**A3. Section 4.4, the outrunning threshold is inverted.** "a body of `p >
0.73 Q S M` outruns its own family's rows". `v = p / (m + p) > 1 / sqrt 3`
requires `p > m / (sqrt 3 - 1) = 1.366 m` (1.391 m with the table's `c =
32 / 55`); at p = 0.73 m the speed is 0.42 < 0.577. (0.73 = sqrt 3 - 1 is
the reciprocal of the right threshold.) The bar's outrunning body at 0.75
Links per interval has p = 3 m and is unaffected.

**A4. Section 2.5, a tool validation quoted as the registered fit.** "the
crowd fits the Milne form with `q = 0.000`, `H (t_0 + T_0) = 1.000` (record
138 and the README)". The register's `coasting_none` reads q = -0.108
(inside the pin -0.25 .. +0.25), H (t_0 + T_0) = 1.026, rms 0.0019
(hubble_stars README lines 317 and 556; EXPERIMENTS 2277). "q = 0.000, H
(t_0 + T_0) = 1.0000, rms 0" is the tool's self-validation on the exact
Milne form (README lines 138-144: "the tool's validation prints this"), not
a run. Section 5.5 cites -0.108 correctly; 2.5 must say the same.

**A5. Section 7.2, a registered reading claimed as explained.** "the phase's
turn per orbit at r = 8 read 0.75 to 0.83 of a circle beyond whole circles,
which is what `j = 3.14` on an eccentric loop gives sooner than the
design's 0". j = pi gives 0.14 beyond whole circles; nothing in the
document derives 0.75 .. 0.83, and "sooner" is not a derivation. Correct
statement: the registered fraction (bohr README line 165) matches neither
the design's 0 nor pi's 0.14 and is not explained here. The pi / 2
correction of the README's j column itself is right (verified: 0.946,
1.463, 1.725, 2.000, 2.555, 2.873, 3.248 x pi / 2 = 1.49, 2.30, 2.71, 3.14,
4.01, 4.51, 5.10), as is the action sum `sum |p_axis| = 2 pi p r`.

**A6. Section 1, an omitted run-time discard: `norm //= denominator`,
meeting.py:358.** The target is formed over the common denominator D
(`t = sum n (D / d) V`, lines 324-333) and its norm is `isqrt(t . t) // D`:
a second floor per interval on |t|, distinct from the isqrt of item 10 (the
fractional part of `isqrt(t . t) / D` is dropped every interval, up to one
unit of |t| per interval, so `adv` under-reads the crowd met on any world
whose kappas have a denominator above 1). The document never mentions it
(its only "denominator" is amplitude's square test, line 204). Add it to
1.2 step 3 and to 1.3 as a remainder discarded at run time outside by_drive
(the torus form: keep `t . t` and D^2 and compare, or carry `isqrt(t . t)
mod D` on the row).

**A7. Sections 2.5 and 4.3, the grain arithmetic.** "the register reads
0.2636 against the classical 0.2674, within the grain 0.003 and fifty
grains from the relativistic value" and 2.5's "every star within the grain
of the digital step (0.003 in z)". |0.2636 - 0.2674| = 0.0038 > 0.003, and
s_px1's 0.0611 against 0.0573 is 0.0038 too; (0.315 - 0.2636) / 0.003 = 17
grains, not fifty. The conclusion (no gamma) stands; write "within 0.004"
and "seventeen grains".

**A8. Section 6.3, a registered quadruple misquoted.** "where the unread
pair reads `44, 44, 44, 44` and `S = 176 / 64`". The register reads `E x 64
= 44, -44, 44, 44` (EXPERIMENTS 3725, the CHSH sign at -b); S = 176 / 64 is
right.

## B. Wrong citations (must-fix)

**B1. Section 2.4:** "a row's y-step is a self-Link (`game_board.py:48-49`)".
Lines 48-49 are `raise ValueError("adjacency requires three-tuples ...")`.
The self-Link of `adjacent_node` is the docstring at 35-36 and lines 60-63,
and the walk never calls it: a row's self-Link on an axis of extent 1 is
`coordinates[:, axis] %= extents[axis]` at nature_beam.py:2404. Cite 2404
(the finding that follows, 2399 and 2412 marking a self-Link as an arrival,
is correct as cited).

**B2. Section 1.2:** "the apportioning ... `core/integer.py:88-113`".
`apportion_whole` is at 100-116; 88-98 is the body of `by_drive` (70-98).

**B3. Section 5.4:** "the phase offset per pixel sharp (the resultant 0.92
to 0.98 at the lit pixels of `mass`)". The lensing README says "0.9 to 1.0
at the lit pixels of `mass` and `near`" (line 281); the table's resultants
0.09, 0.21, 0.31 are per world. Quote the README's words.

**B4. Section 1.4:** "two independent axis accumulators at the rate 64 / 156
fire at the same intervals (2, 4, 7, 9, ...), two Links in one interval,
and the sum of the per-axis floors at age 29 is 22, not 24". The fires 2, 4,
7, 9 are the half-rounded form's, whose per-axis sum at 29 is 24 (equal to
m(29)); the sum 22 belongs to the plain floor `tau x 64 // 156`, which fires
at 3, 5, 8, 10. Either form makes two Links in one interval (the conclusion
holds); state one form and its numbers.

**B5. Section 5.4:** "its phase gains the crowd met, `integral of abs(V) dt
/ Q`, which is `q / (4 N b c)` too". That integral is `q / (4 b c)` phase
steps; `q / (4 N b c)` is the same in turns of the circle. Say "turns".

## C. Method and wording (must-fix C1-C3)

**C1. The verdict words.** DERIVATIONS.md section 0 has four: reached,
different law, not reached, and **New** ("a formula the GameBoard gives that
has no counterpart in known physics"). The document announces "three words"
and then uses **stated** (6.5 row 1), **stated as a quantity** (6.5 row 6)
and **not a formula of the law** (6.5 row 8), none of which is in section 0.
By section 0 the cost per record and the classical-quantum quantity are
"new"; Landauer is "not reached". Section 8's table inherits the fix.

**C2. The `//` inventory's classes are incomplete.** Every run-time discard
the task names is in the document except A6 (by_drive; m(tau) 553;
`share_of` 853; `apportion_whole` 108; the turn under `action` engine 644;
`adv` meeting 232/239; the push floor 2219; the doppler floors 2057/2142;
the lamp's cap 3774/3789/3799; the give 800). Record 155 (b) asks for
"every remaining `//` with its class"; the document names no class for:
the ~25 guards (`MOMENTUM_BOUND // x`: nature_beam 838, 841, 868, 950, 964,
1808, 1871, 2034, 2056, 2118, 2140, 2213, 2216, 3634, 3645; meeting 194,
336; measured 112; world 474, 1303-1304, 1528, 1698, 1767, 2485, 2648, 2668,
2682, all at load or tested before a product); the addressing divisions
(nature_beam 1082, 1084; game_board 59; amplitude 132, 139; `modulus // 2`
at 1125, 1221, 1883, 2599, world 1324, 1656; the lamp's `ways // arms` 3784
and `way // paths` 3828, exact by the load guard world.py:1735); the periods
(nature_beam 610-612, exact at load); the exact reductions (amplitude 153,
167, 184, 194, 650, 697; meeting 328, 333; integer 45); the isqrt's own
Newton iteration (integer 34, 36); and the fixed-point series behind C and
S (phase.py 28-49, named only by 62-90). One paragraph with these classes
and lines closes record 155 (b).

**C3. Section 1.2, the flight table's class.** m(tau) at nature_beam 553 is
classed "a torus operation (the exact cache)". As built it is a floor at
run time whose remainder is dropped; the document's true point is that the
dropped remainder is a function of the age (verified: the accumulator
started at T_d, gaining 2 S_1 Q, carrying at 2 T_d, equals m(tau) on
(1,0,0), (1,1,0), (1,1,1), (3,1,0), (2,1,0), (5,-3,2), (44,7,0) over 600
intervals). Say both, so that record 155's "no division at run time
discards a remainder" reads honestly: as built it discards, nothing is lost.

**C4 (should-fix).** Section 7.2: "the whole values fall at r = 12 (j = 4)
and near r = 2 (j = 1.5, between)": 1.5 is not whole; r = 12 (4.01) is the
one registered radius with a whole j. Section 3.2's cube-fan "3.5 at P =
16" reads 3.3 in my count of primitive vectors within 11.5 degrees (3.04 at
P = 8 agrees with the document's 3.0); state the counting rule. Section
7.2's digital-circle numbers (2.010, 2.003, 2.0004, 2.0001) depend on the
circle walked (mine: 2.034, 2.010, 2.002, 2.000); the limit 2 is what
matters and holds.

**C5 (not verified, stated as such).** The Bell lamps "stall once at tick
4" (6.4; the bell README says only that K + 2 hides the stall for 160
ticks, record 148); "TERMINOLOGY corrected" (4.3). Everything else quoted
from records 153-159, series C, E, G2, H, K, L, FORM.md, GRAIN.md,
HYPOTHESES 21, BEAM_LAW's 1.35 % and notes 24-40, and limits.txt (0.454,
0.842, 0.897; 0.932, 0.995; 0.0442; the bound `8 / N + 16 arcsin`) was
found as cited.

## Section-by-section (a) citations, (b) register, (c) mathematics, (d) verdict, (e) inventory

**1. The inventory.** (a) All cited lines checked hold except B1, B2; the
coincident-fire finding (engine 552-568: `axis_steps` raised and D
subtracted on the later axis with no Link, line 563) and the refused-step
finding (630-634, `_contact` 735-739 `else: continue`) are correct readings
of the code. (b) Notes 33, 37, 41 and records 148, 154-158 as cited. (c)
The accumulator identity verified (C3); B4. (d) "Reached for the audit"
is justified once A6 is added. (e) A6 is the one omission of a run-time
discard; C2 the missing classes.

**2. Doppler.** (a) 2741, 2399, 2412, engine 378-401, 418-451, 85-116 hold;
B1. (b) Record 158's 45, 58, 19, 38, 48, 183, 311; record 153's 374784 /
262144; test_doppler's 96.9, 45.3, 303.1, 0, 57.8 and 6204 / 64; G2's
per-star z (0.0573/0.0611, 0.1146/0.1146, 0.2483/0.2478, 0.2674/0.2636)
found; A4, A7. (c) Every number in 2.1-2.4 and 2.6 recomputed and right
(45.75, 58.31, 18.25, 37.69, 183, 311; 96.875, 45.31, 303.125, 57.81;
5/6, 5/3, 5/2, 1985/2244; 156/64, 156/128; 1.516, 2.065, 1.769). (d) The
verdicts are honest about what is built (main: not reached, k per k) and
what is a design (record 158); the bar-of-extent-1 reading of record 158's
2.44 is an interpretation, plausible and marked as such.

**3. Newton and Coulomb.** (a) 3546-3566, 2147-2221, 2973, engine 1120-1143
(`abs(distance - radius) < 0.5`) hold. (b) Series C item 5's two columns,
the slopes, N(16) = N(20) = 112, the flux 1.0000, P_A / P_B, item 7's -1
and -1/4, series 7's six coefficients, item 4's arrival ticks: all found and
reproduced. (c) G = K (n / d) / (4 pi S) follows (Q cancels); Huxley's
131/208 right; the hierarchy 1.1e18 / 2.0e21 right. (d) Justified.

**4. Special relativity.** (a) 444-447 (the age advances before the step),
world 447-456 hold. (b) HYPOTHESES 21 exists; record 144's cone (17, 24 at
age 29) reproduced by m(29). (c) The table 4.4 right; A3, A7. (d) The
Lorentz-covariance row is carefully limited to the equation the rows
converge to; justified.

**5. General relativity.** (a) 475-485, engine 119-131 hold; B3, B5. (b)
Series E's 41.5, 36.1, 0.870, the rate ratios and the law's column (C =
33.12 fitted at r = 14, as the README says), series K's 89.40, 0.000, the
centroids and ages, 122, 2.4 degrees, G2's +0.345 / +0.922 / -0.108 found.
(c) The retarded potential, Poisson's equation, `V = -(Q c / dwell) grad
A`, `1 - k + k^2` against `1 - k - k^2 / 2`, and the deflection integral
verified. (d) Justified, including "different law" for the Shapiro form.

**6. The information cost.** (a) 3762, 3665, 3844-3847, amplitude 192,
524-527, 749 hold. (b) 1/1682, 63/1, 65448-65773, 237, 176/64, 88/64, 44 /
-44 / 0 / 0, 2896/1024, 11584/4096, 252 of 512 (record 102), rotations_4
found; A8. (c) 64/1682 = 0.038, 65536/237 = 276, 0.0442, 1/2N bounds,
log2 80 = 6.32, 362 right; A2. (d) C1: three verdict words outside the
method; Born and Tsirelson "as a limit" honest.

**7. Young and Bohr.** (a) engine 637-645 (`links = axis_steps - 1`,
`by_clock(links, magnitude x N, action)`) holds. (b) Record 156's 0.963,
0.96, 0.904, 27 of 75, the comb 68/115/68, "15 screen clicks on 14 pixels"
(TWO_SLITS.md line 14: two at 61), limits.txt's correlations; the bohr
README's j column, r = 8 four and r = 12 five closings, C(4) = 1.01,
0.75-0.83, 40 600 / 39 660, 84 lumps, the signed drive's twice / none: all
found. A1, A5. (c) The action sum right; A1. (d) Bohr's condition
"reached" is a limit derivation with no registered closure confirming it
(the document says so); A5 overclaims the register.

**8. The table** inherits A1-A5 and C1; otherwise consistent with the
sections.

## The `//` inventory against the grep (every runtime `//` in events/ and core/)

| Line | Class | In the document |
| --- | --- | --- |
| integer.py 67 (`by_clock`), 108 (`apportion_whole`); by_drive 70-98 | primitive / floor off the clock / exact apportioning | yes (1.2, 1.3 items 1-3, 12) |
| nature_beam 492, 553, 508, 575, 608-612 | by_clock_rows; m(tau); the window; u_d; T_d and the periods (load) | yes, except the periods (C2); C3 |
| nature_beam 853, 2057, 2142, 2219, 3774, 3789, 3799 | share_of; the doppler grain and floor; the push floor; the lamp's cap | yes (items 4, 5, 12, 13) |
| engine 644 (`by_clock` on k0), 800 (`held // h`) | the turn under `action`; the give | yes (item 6; step 4) |
| meeting 232, 239-240 | `adv`, the register and its inverse | yes (item 9) |
| meeting 358 `norm //= denominator` | a floor per interval on abs(t) | **no (A6)** |
| meeting 328, 333; amplitude 153, 167, 184, 194, 650, 697; integer 45 | exact (lcm, gcd reductions) | partly (204); C2 |
| amplitude 192, 215 | the rungs (nearest) | yes (item 14) |
| amplitude 132, 139; nature_beam 1082, 1084, 1125, 1221, 1883, 2599, 3784, 3828; game_board 59; world 1324, 1656 | addressing / N over 2 / the lamp's arms | no class named (C2) |
| nature_beam 838, 841, 868, 950, 964, 1808, 1871, 2034, 2056, 2118, 2140, 2213, 2216, 3634, 3645; meeting 194, 336; measured 112; world 474, 1303-1304, 1528, 1698, 1767, 2485, 2648, 2668, 2682 | guards and load-time bounds | no class named (C2) |
| phase.py 28-49, 63, 66, 83, 88; integer 34, 36 | the fixed-point series for C, S (load); the isqrt's Newton | C, S yes (62-90); the rest C2 |

Files: `checks.py`, `checks2.py` (the arithmetic), `DERIVATIONS_BEAM.md`
(the copy reviewed) beside this file. No repository file was touched.
