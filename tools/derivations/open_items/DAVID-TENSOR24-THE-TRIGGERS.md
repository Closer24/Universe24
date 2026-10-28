# Law 4's top and bottom from the clock, and why a bang repeats under the exact time reversal

David, 2026-10-28, 15:0x UTC, for the Boss (Sofer and Animate copied). This page answers three questions the plan holds open:
- **(a)** "the rate 0 gives nothing": what BH-S1's restore does, and whether the clock gives it with no mask;
- **(b)** the bottom with no typed floor: the weak minimum of section 30, item 10, or another;
- **(c)** the many bangs: does the board swing between its two ends by itself, and does each bang show more (law 10; rows 1c and 46)?

It overlaps the board's item H (the Boss's helper), so either can be the other's second hand. A helper drafted it, and I reran its probes by its own exact commands (58 runs). Of the 71 outputs, 47 are byte for byte identical. The other 23 differ only by what the harness and course.py gained after they were written: two switches printed at their defaults (which reproduce the earlier runs), the run times, and two summary lines. They are the same once those are dropped. One output (p3_edge_nofine.txt) came from an earlier version of its probe and is not rerun. They are in DAVID-TENSOR24-THE-TRIGGERS_CHECKS.txt, with the draft's proofs in full. The probes run the head's own acts with each variant assigned at run time (no file of the repository edited), on toys-5's src (last changed at 834cfd72e); the harness reads the head bit for bit (11 of 11). The law is quoted at scribe-5 f32b67cc3 (lines 132, 1608 and 1909). This page covers protocol steps 1 to 4. A second hand follows, then Sofer's check and my sign-off. No src is pushed.

## 1. (a) The rate 0 gives nothing

1. **In the clock.** A clock whose Link rate reads 0 should not tick. The one formula as it stands does not give that: at the rate 0 only the grips vanish, and the time gear coasts on its own inertia, spring and push. The discarded step is 517,114,983 at 5,000,000 quanta and 160,335,814 at 500,000 (PROVED; CHECKED).
2. **The formula, in the three operations:** weight the time gear's step by the clock's own tick count at its Link rate,
   - n = (p_m + Gamma - 1) div Gamma, which is Rule3 on a dial one tooth short of its turn: 1 at every Link rate from 1 to Gamma, and 0 at 0;
   - the time gear's output = held + n (stepped - held).
3. **The top then comes by itself** (Theorem A1, PROVED). From a live setting, a clock can reach the stop only rising (X0 < X1). So with X2 = X1, law 4's own weak maximum turns every stopped clock at its stopped tick. No ceiling is typed: X_c = 4,268,834,097 is the rate chain's own zero.
4. **BH-S1's restore of the other gears is never reached,** since the turnover rewrites every gear of a turned clock. CHECKED, bit for bit with the head:
   - 251 of 251 states at 5,000,000 quanta;
   - 301 of 301 at 500,000;
   - 901 of 901 on the hole over 900 ticks.

   Stopped clock-ticks: 320, 128 and 397, every one rising and turned. The rewind is 20 of 20 through the top. 6 of 6 mutants are caught. The time gear's hold is the load-bearing part of BH-S1; the rest of its restore is not.
5. **OPEN:**
   - n is BH-S1's own mask read as a coefficient. Its other uses stay as n's products (the wall, the dial's rest, the click's skips). Striking the wall moves the hole from tick 476 (425 of 901 states differ, births 35 both).
   - Whether n, an indicator spelt as Rule3's quotient, passes law 11 is Sofer's to read. He reads it as one of five names for one operation (6471863755, item 4): BH-S1's mask, the rate 0, the charge's held Meshes (QR4), H's cone lapse and F5's dial are all a Mesh's rate as a dial whose whole turn is "no tick this tick". It is to be written once.
   - Its form with the remainder kept is the asynchronous dial of DAVID-TENSOR24-THE-LOCAL-TICK.md.

## 2. (b) The bottom

1. **The weak minimum is REFUTED** (Theorem B1, PROVED; CHECKED).
   - Beside the weak maximum, it holds every time gear at rest for ever: a clock at rest turns the first tick it moves either way, and the turnover returns it to rest.
   - Every world starts at rest, so every world freezes at tick 1. On all six charts, the node and the threshold route, every clock turns every tick, with 0 births.
   - It contradicts law 4's own "the one big bang's rest at the full rate ... does not turn".
2. **No trigger on the shape of the three notches alone keeps X in the reading's domain** (Theorem B2, PROVED). A fall from X1 > 0 to X2 <= 0 within one tick is no minimum. With the strict minimum, or with no bottom trigger at all, the hole falls through X = 0 and is refused at tick 6.
3. **The full rate is the step's own edge** (Theorem B3, PROVED; CHECKED).
   - The light's checkerboard steps as a+ + a- = (2 - 4 (p_m / Gamma)^2) a.
   - It is bounded for p_m < Gamma, grows linearly at p_m = Gamma (the vacuum, on the edge), and grows exponentially above.
   - The rates' table puts p_m <= Gamma exactly at the loads c >= 0. So X >= Gamma is the stable side, and X = Gamma is derived, not typed.
   - CHECKED on the head's own integers over 2,000 ticks: 8,702 cases, 0 failures, 4 of 4 mutants caught. One more mutant, the carry's fine tooth reset, is not caught, as it should not be: the edge is the linear map's, not the rounding's.
4. **As law 4's bottom,** no time-gear slot then falls below Gamma on any chart, so F5's clamp and the typed hill depth never act.
   - The typed X_f = 19 acts only on the hole (160 turned clock-ticks).
   - X = Gamma moves the five structured charts from tick 3 to 10 (births: hole 28 to 30, nature 3 to 2, chiral 5 to 6, ga2 32 to 48). The bang and the threshold route stay bit for bit.
5. **In law 11's words:** X = Gamma is the dial's zero in Sofer's carry shape (6469988450): the borrow below the vacuum, q = -1. It is the step's own edge, not a floor value. Sofer reads it.

## 3. (c) The many bangs

1. **The 00-equation route (R) does not swing between the two ends.** On the bang's calibre with the heavy sea it swings every 13 ticks between X of about Gamma and 1.15 Gamma, far from the stop. So (a) never acts.
2. **R's differing tops are an artifact.** Its bottoms drift down and its rewind fails (0 of 20), both for one cause: the velocity term X'^2 / 2X read at the tick's start breaks T S T = S^-1 (1,216 of 4,864 integers).
3. **Written exactly in the Link's length L** (X = L L div Gamma; Theorem C1: the 00 equation is then a pure brake, L'' = -L ((d+1) K - (d-1) V) / (2 Gamma key)):
   - T S^4 T = S^-4 holds to the last integer (4,864 of 4,864);
   - the rewind is 20 of 20 through the turnovers;
   - every swing repeats the one before (29 of 29 on 4^3). Every gear returns every two swings; only the dial and the click counter do not.
4. **Draft C's threshold route (V) with (a) does swing between both ends:** its top is the Link rate's zero, and its bottom the full rate at rest, where the push turns the course out with no trigger. Its rewind is exact through the top.
5. **But the head's turnover is not the exact time reversal.** The regulator's three flow gears are odd under T: their source negates at the retracing step (192 of 192). The turnover mirrors them as even gears, so their drive fine teeth miss by 2N (192 of 192).
   - With the flows odd under T, T S^m T = S^-m holds to the last integer on V, on the head's own bang and on RL (4,864 of 4,864 each). The rewind stays 20 of 20.
6. **Under that exact time reversal every one-clock (A1) bang is a copy:**
   - births 0 at 5,000,000 quanta (against 96) and at 500,000 (against 64);
   - births 0 on the head's own bang (against 64);
   - every swing equals the one before, and all tops are one number.

   The structured worlds keep their clicks (hole 30, nature 2), because their clocks turn over at different ticks.
7. **Why** (Theorem C3, PROVED). Where T S T = S^-1, a whole-board turnover makes the next swing retrace the last, so nothing the clicks wrote is new. A bang can show more only where the board leaves the one clock (local turnovers at different ticks), or where a click breaks the time reversal bang after bang and does not die out. Both second hostile reviews reach the same palindrome (the plan at deaa899b9, item 11 (o)).

## 4. What it means for the plan, and a big law above

1. **Law 10 against the exact time reversal.** "Every bang shows more" fails on every one-clock course once the turnover is the exact T, if the reversed run undoes the clicks too. The clicks measured after the first top on those courses came from the turnover's flaw. This joins draft F's finding (law 10 at the closing bang, a conflict).
   - **The owner ruled at 14:37 UTC** (item 11 (o), way 2, approved with (s); the plan at 8f012b9b2): the reversed run leaves the clicks undone. What a click wrote runs on with the gears into the next bang, its quotient in the record, and the exact rewind stays as the check that reads the log.
   - So Theorem C3's copies hold for the gears alone: time is a circle for the gears, the clicks carry the arrow, and every bang shows more by what they wrote.
   - His direction for the missing part of law 10 is "the solution is in the detector's click" (draft K).
2. **A big law above, approved by the owner at 14:37 UTC (item 11 (s)): the turnover is the kind's own phase reversal T on every gear,** each gear even or odd as T makes it. It is one sentence for three findings:
   - the flows here;
   - draft E's T = i sigma_y K on the twins, where the head's K breaks the 24;
   - the charge's QR2 (DAVID-TENSOR24-THE-CHARGE.md), where the head's turnover reverses every charge.

   It contradicts law 4's mirror, so it goes to the owner. On his word of 14:48 ("I meant generic for the clocks' reversal") it went to the Boss as one law 4 (6472218585): the turnover is T = J K on every gear, at the clock's own top, as a carry, each gear's sign its source's.
3. **The top and the bottom,** read in the clock: the top is the clock that stops ticking (n = 0), and the bottom is the step's own edge at the full rate. Neither is a typed value.

## 5. What it replaces, and what stays OPEN

1. **Replaces:**
   - BH-S1's restore (line 132; tick.py:285-287), by the time gear's step times n: the state is bit for bit;
   - FR-S1's trigger "on the restored line", by law 4's weak maximum on X2 = X1, with no restore under it;
   - law 4's second trigger X_f = 19 and the typed hill depth (line 1608), by the step's edge at the full rate;
   - the weak minimum of section 30, item 10, REFUTED;
   - draft C's 00-equation closure with "each top different", which is the velocity term's artifact. Its exact form RL is given, with an exact rewind and equal swings.
2. **OPEN:**
   - Sofer's readings of n and of the full rate under law 11;
   - the wall without a mask (the grip read from both ends' rates);
   - the click that makes a bang show more with the rewind exact;
   - the flows odd under T, as a change of law 4's mirror (the offset's three odd gears and the twin hands not read for their sign under T);
   - RL on the structured charts;
   - a 5^3 bang.
