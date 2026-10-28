# Draft B: the bounds of the head as thresholds or zeros, the held load in D, the release and its recoil

A draft for Tensor24's owed list (section 19: "the clamps' replacement", "the held field's load in D", "the release's advance and its recoil"), by a helper of the Boss's, for David's sign-off. It follows S/derive/PROTOCOL.md: steps 1 to 4 are here (the formula in the three operations, its proof, a probe that can fail, what it replaces and changes); step 5 (a second hand that did not write it) and step 6 (Sofer's law check, David's sign-off) are owed. Every claim is marked **PROVED** (with its proof), **CHECKED** (with the probe's count) or **OPEN** (with what blocks it).

- **Base.** The engine of the Boss's t24 tree: src at 834cfd72e (cut 1, the fair draw, on 526a5666d), the plan at 55a3483e1. David's rule for the bounds: #2187 6463668203 (read through the API): "(a) a threshold, where a quantity reaches a whole unit ... the next carry on the clocks' ladder (dial, winding, turnover, bang); the quotient leaves as an event, and the remainder stays; (b) a zero, where nothing is to move: a clock at rate 0, a link at grip 0 ... the formula itself gives nothing".
- **No file of the repository is edited.** Every variant is a wrapper installed at run time on the head's functions, or the head's own source of one function with one line changed and compiled inside the probe (inspect.getsource). Probes run as `python -I` with `sys.path[:0] = [S/t24/src, S/t24, S/derive/B]`, integers only.
- **The charts.** The 21 worlds of tests/worlds at their own ticks (the one big bang at the plan's 250), listed in bcommon.CHARTS; the committed charts are the hole (60), the chiral (world_nature, 60) and the bodies (120).

## 0. The verdicts

| the bound or term | the head | replaced by | its kind | status | what it changes |
| --- | --- | --- | --- | --- | --- |
| F5, a load below 0 read at 0 | readings.py:21 | the turnover's floor at the full rate, X_f = Gamma | threshold: the time gear's bottom | PROVED; CHECKED | where F5 acted (6 charts) the clock turns over at the full rate instead of entering a hill; the other 15 charts bit for bit |
| the end teeth kept above 0 | tick.end_teeth | no carry where the floor's turnover discards the output (law 4's floor clause); the divisor there the teeth the floor leaves | threshold: the time gear's bottom | PROVED; CHECKED (the state bit for bit on 21 of 21 charts, the log on every chart where the floor never fires) | no state; two face fields no reader reads, at the hole's floor-turned clocks (section 4) |
| F2, the tension above Gamma read at Gamma | meshes.py:74 | the tension's carry at the full rate: the Mesh engaged in its first winding only | threshold (the horizon) | PROVED as an identity for t >= 0; OPEN as a threshold (it books no event of its own) | nothing |
| F2, the tension below 0 read at 0 | meshes.py:74 | none | the lattice's light cone | OPEN | without it the step loses its energy (section 5.2) |
| F1, the drive at plus or minus the hold | tick.py:255 | none | neither | OPEN: the course's closure (draft C) | without it the bang spikes; the turnover past the hold freezes the great clock (section 6) |
| R10 and BH-S1, the stopped clock | tick.py:108, tick.carry's last restore, meshes.factors' mask, the click's skips | the clock's own grips: a zero; the rest: no zero | partly a zero | the own grips PROVED and CHECKED; the rest OPEN | with no mask and no restore the stopped clock coasts, sinks deeper and spreads the stop to its neighbours (section 7) |
| the held load in D | tick.py:106 | the load plus every train's calibre weight times its first gear | a contraction of every train alike | PROVED; CHECKED bit for bit | nothing |
| the held field's mass source | tick.py:229 | its weight times the masses' contraction over every train, read from the start board | J on every real gear alike | the head's order (R8) CHECKED to differ; OPEN: the source and the load's shift are not one coupling (a factor key div Gamma = 36) | the order-free source moves the bang after its fittings (section 8) |
| the release's advance and its recoil | tick.advances, unwind.push_of, unwind.recoil | every hand's first gear driven by the pinion's carry at the rim; the push from the start notches; the recoil inside the regulator's flow drive | K of every hand alike; a term of the regulator's drive | PROVED; CHECKED bit for bit, the rewind exact with no tally | nothing (R4's coupling stays the head's) |

**By label, and the rows to read again** (the readers were not run here; the rows are those the plan ties to each fake):

| item | what goes, by label | the law's clause it touches | rows to read again |
| --- | --- | --- | --- |
| the floor at the full rate | F5's reach through the load; A4's bound (2), "no Node-clock runs faster than the full rate", as a clamp; the hill's typed depth (stretch.LOW) | "The floor" (its X_f); "The great clock's bounds" (2) (scribe-5's ALGEBRA.md 1909, the plan's A4) | every row on the hole, the chiral, the bodies, node, ga2 and emission_one (their course moves); none on the bang |
| the end teeth | the bottom's fallback (section 16) | "The floor" (its letter: the output discarded); "The great clock's bounds", its 97e5b3fd6 sentence | none: no reader reads what moves |
| F2's upper side | F2's upper half, written as the Mesh's carry (E9's clamp, half) | "The horizon" | none |
| F2's lower side, F1 | nothing yet (OPEN) | "The great clock's bounds" (1) and (3) | F1 with the course's closure: rows 1, 1c and 46 |
| R10 and BH-S1 | the factors' mask at the stopped clock's own end (redundant); the rest OPEN | "BH-S1, the frozen Clock", FR-S1 | 14, 34 and 61, when the zero holds |
| the held field | R14's `weight is not None` (tick.py:71, 227); R8's order measured, not yet changed | "The nuclear holder", DAVID-MEDIATOR.md's "whoever reads with w sources with w" | 76 and 77; the bang's state from tick 11 under the order-free source |
| the release | R14's clock.unsprung() in tick.advances (two reads); the rewind note's tallies (state beyond the clock, cut 7); the second drive of the flow gears | EM-S1, LT-S1 | none |

## 1. The integers and their words

- A gear: (a, a-, r, w), its notch now and before, its fine tooth, its teeth count. Rule3, the carry: carry(n, d, r) = (q, r') with n + r = q d + r', 0 <= r' < d (acts.carry at +1; at -1 the same act conjugated by the flip of the fine tooth).
- The regulator's time gear, the stretch: X- (before), X (now, the tick's start), X+ (the step's output: the regulator's act, before any turnover or stop). The teeth count of every driven gear: T = 6 rim Gamma^2 G^2 (teeth_of). The mean teeth counts: W = (T div 2)(X- + X) at the tick's start, W+ = (T div 2)(X + X+) at its end (mean_teeth_of).
- The full rate Gamma (node_clock), the key (quantum_action), the trace t, the mesh unit G (mesh_unit_of). The load c = load_of(X), the largest c with Gamma^5 <= X p0(c)^4; the rate p0 = rate(c); the mesh rate p_i = p0^2 rounded at Gamma. load_of(Gamma) = 0 and the rate falls with the load, so **c >= 0 exactly where X >= Gamma** (PROVED: at c = 0 the condition reads Gamma^5 <= X Gamma^4; CHECKED at Gamma 1,000 and 6,000: X(0) = Gamma, load_of(Gamma - 1) = -1, load_of(Gamma) = 0).
- The turnover (law 4): its top, X- <= X >= X+ with one strict; its floor, X- < X_f or X+ < X_f. On the head X_f = X(-Gamma) = 19 at Gamma 1,000 (readings.bottom), and the floor reads X+ after the stop's restore.
- The light's hold S = 2w - D - SUM_j R_j, the grips R_j = 2 pinion p_i^2 Q_j and the spring D = 12 (rim - pinion) p0^2 G^2 (rule3.gearing). The step's edge: D + 2 SUM_j R_j <= 4 w, past which the conserved form is no energy (DAVID-LIGHT-CONE.md, toys-5).

## 2. Where each bound acts on the head (probe B1)

Counted at every forward tick of every chart, the head's code unchanged (b1_counts.py, b1_counts.txt). A tension is counted as the tick's factors read it, at each of the six Spokes of every clock, so each Mesh twice (the plan's "28 to 44 percent" is another count):

| chart, ticks | F1 above / below the hold (largest drive div hold) | F2 tensions below 0 | F2 above Gamma | F5 tick-start loads below 0 | the end-teeth fallback | stopped clock-ticks |
| --- | --- | --- | --- | --- | --- | --- |
| hole, 60 | 89 / 361 (3,003) | 21,842 of 45,000 (48%) | 8,884 (19%) | 112 of 7,500 | 19, all at turned clocks | 0 |
| chiral (nature), 60 | 0 | 21,440 (47%) | 0 | 96 | 0 | 0 |
| bodies, 120 | 0 | 159,012 of 246,960 (64%) | 0 | 8 | 0 | 0 |
| one big bang, 250 | 12,800 / 3,200 of 16,000 (6,666) | 38,400 of 96,000 (40%) | 19,200 (20%) | 0 | 0 | 0 |
| node, 20 | 0 | 1,172 of 3,240 (36%) | 0 | 33 of 540 | 0 | 0 |
| ga2, 230 | 0 | 61% | 0 | 32 | 0 | 0 |
| emission_one, 300 | 0 | 61% | 0 | 1 | 0 | 0 |
| polarization, packet, emission, the three collapses | 0 | 27% to 76% | 0 | 0 | 0 | 0 |
| sea, sea_3, plasma, plasma_3, universe, universe_3, pair_3, emission_none | 0 | 0 | 0 | 0 | 0 | 0 |

All 21: F1 at 16,450 clock-ticks (on two charts); F2 at 5,557,092 of 12,048,300 tensions below 0 and 28,084 above Gamma; F5 at 282 of 2,008,050 clock-ticks (on six charts), none in an end state; the fallback at 19 (the hole), 19 of them at turned clocks, 0 at a clock neither turned nor stopped; no stopped clock on any chart at its own ticks (CHECKED).

## 3. F5: the floor at the full rate (a threshold)

**The formula.** The turnover's floor is the full rate: X_f = Gamma, the calibre's node_clock, the stretch of the load 0. Nothing else changes: the trigger is law 4's (a whether of the gate, a quotient: for X > 0, X < Gamma exactly where X div Gamma = 0).

**In the clocks.** The great clock runs the small clocks: a small clock's time gear that would fall below the full rate turns over there, its own act, as it turns at its top. It never runs faster than the great clock, by its own turnover and by no clamp.

**In physics.** The law's own theorem refuses a vacuum load below 0 ("the guard", ALGEBRA.md line 432: at the wave number pi on every axis light has cos omega = 1 - 2 (p_a / Gamma)^2, and a load below 0 puts p_a above Gamma and cos omega below -1, the checkerboard mode growing). The floor keeps every clock off that load by the clock's own act.

**PROVED, the invariant.** Let P(t): at the start of tick t, at every clock, both notches of the time gear are at least X_f.
- P(0): the setting leaves the time gear at Gamma in both slots (clock.start_state), and X_f = Gamma.
- From P(t), forward: a clock the act turns over ends at its start's two notches exchanged, (X-, X), both at least X_f; a stopped clock not turned ends at (X, X-); any other clock ends at (X+, X) with X+ >= X_f, since X+ < X_f fires the floor and makes it a turned clock. So P(t + 1).
- The rewind runs through the same states. So at every tick's start c = load_of(X) >= 0, and rates_of's max(c, 0) is the identity: **the clamp is never reached and goes.**

**PROVED, bit for bit wherever F5 never acts.** Let a run of the head have no tick-start load below 0 and none in its end state. Then every now slot at every tick boundary is at least Gamma, and so is every before slot (a former now). The raised floor adds a trigger only where X- < Gamma (never, by this) or X+ < Gamma. At such a clock the head either turns it over too (the same act), or not; but then the next tick's start (or the end state) holds X+ < Gamma as its now, a load below 0, which the run does not have. So the turned clocks are the same at every tick, and the run is the same bit for bit.

**PROVED, the rewind and the books.** The floor's trigger is symmetric in X- and X+ (the reversed triple of law 4's floor clause), the turnover an involution, and the head's backward reads the rewind note's mask; nothing of that proof uses X_f's value but X_f > 0 and the start at or above it. The turnover is no click and books nothing (law 4); phase.books is untouched.

**CHECKED (probe B2, variant FLOOR, every chart; b2_floor.txt):**
- bit for bit (every tick's state and the whole log) on the 15 charts where F5 never acted;
- under the floor, F5 is reached at 0 tick starts and 0 end states on all 21 charts;
- the rewind 20 of 20 on all 21;
- on the 6 charts where F5 acted, the run moves from the first tick a clock would enter a hill:

| chart | first tick differing | turnovers head / floor | fittings head / floor |
| --- | --- | --- | --- |
| hole | 4 | 1,073 / 997 | 28 / 30 |
| chiral | 3 | 861 / 997 | 3 / 2 |
| bodies | 10 | 1,934 / 2,046 | 0 / 0 |
| node | 3 | 117 / 135 | 0 / 0 |
| ga2 | 196 | 64 / 96 | 32 / 48 |
| emission_one | 15 | 5,191 / 5,308 | 0 / 0 |

**What it replaces:** F5 (readings.rates_of's max at the tick's start, its one reach through the load); the floor's typed depth, a hill one Gamma deep (features/stretch LOW = -1, readings.bottom at the load -Gamma), so the hills' side of the rate table is read by no tick-start load. **What it changes:** the physics where a clock fell below the full rate: it bounces at the full rate (a local time reversal) instead of running a hill at the vacuum's rates; the six charts above. The one big bang is unchanged (its bottom stands at the full rate already).

**OPEN.** F5's second reach is the held load below 0 (the spring's rate past the full rate where a held field is negative). It is reached on no chart: 0 of 16,000 clock-ticks on the bang, the one calibre with a held field, whose notch stays in 0 to 42 (CHECKED, B4). Its replacement goes with section 8.

## 4. The end teeth: the floor's turnover, whose output the law discards (a threshold)

**The formula (ET3).** Law 4's floor clause discards the step's output where the floor fires: "it ends the tick at the state it started from ..., the step's and the drive's output discarded" (ALGEBRA.md, The floor). So at a clock whose floor fires (X- < X_f or X+ < X_f), or which the stop restores, no carry of a driven gear is taken: the turnover (or the stop) is the act there. The teeth every other carry divides by are the head's, W+ = (T div 2)(X + X+). In array code a divisor still stands at the discarded clocks, and it is the teeth the time gear holds as the floor leaves it, (T div 2)(X- + X):

    W+ = (T div 2) (X + X+ + f (X- - X+)),   f the floor's whether (law 4's, a quotient) or the stop's.

The fallback's own test of the teeth's sign, where(w > 0, w, start), goes.

**PROVED.**
1. Wherever the head's fallback acts, X + X+ <= 0, so X+ <= -X < 0 < X_f: the floor fires, or the clock is stopped and restored. So the fallback's clocks are inside the discarded ones, and there the head's fallback is the formula's divisor exactly.
2. W+ > 0 at every clock: at a discarded clock it is at least (T div 2)(2 X_f) by P(t) (section 3); elsewhere X+ >= X_f.
3. The tick's end state is a function of the start and of the carries at the clocks the act neither turns nor stops (the turnover sets every gear of every train from the held state, the stop's restore likewise). So **the state is bit for bit on every run**, the fallback's clock-ticks included, and **the log too wherever the floor never fires and no clock stops** (W+ is the head's at every clock that is not discarded).
4. The rewind is untouched: backward the end teeth are the forward's start teeth, as on the head.

**CHECKED (B2, variant ET3; b2_floor.txt):**
- the state bit for bit at every tick of all 21 charts, the hole's 19 fallbacks among them; the rewind 20 of 20 on all 21;
- the log bit for bit on every chart where the floor never fires (no chart stops a clock);
- on the hole, whose floor fires at 190 clock-ticks (19 of them the fallback's), 10 chime faces move, in their fields re_before_swap and im_before_swap alone (b2_faces.py: 10 and 8 entries). Those are the notches the turnover replaced (CL-S2), written by bobs.face_of and read by no reader in src, tools or tests;
- the counter 'laid' (the release's size, read by no reader) at floor-turned clocks: the hole's 4 notches go to 0. Both of the hole's advanced clock-ticks are turned clocks (b5_explore: 2 of 2), so on the hole the release never advanced a gear that stood.

| ET3 on | clock-ticks whose output the floor or the stop discards | of them the head's fallback | the state | the log |
| --- | --- | --- | --- | --- |
| the hole, 60 | 190 | 19 | bit for bit, 60 of 60 ticks | 10 entries: re_before_swap 10 times, im_before_swap 8 |
| the other 20 charts | 0 | 0 | bit for bit | bit for bit |

With the floor at the full rate as well (BOTH3, the hole, the chiral, node): the state is FLOOR's, tick for tick; the floor then discards 288, 134 and 22 clock-ticks. The raw output still falls through the bottom within a tick at 5 of the hole's (X+ <= -X even above the raised floor), so the end teeth's replacement is needed with section 3's floor too. F5 is reached at 0; the rewind is 20 of 20.

**The uniform spelling, ET, measured beside it.** W+ the teeth of the time gear as the act leaves it at every turned clock, the top's too.
- The state is bit for bit on all 21 charts as well.
- But the faces' before_swap move at every turned clock with a chime: 35 log entries on the hole, 44 on the chiral, 7 on the bodies, 1,651 on the packet, 16 on emission_one, 6,080 on the bang, 1 on collapse_500.
- ET3 is the narrower, and the law's floor clause is its letter.

**Against David's reading** (toys-5 95573578a, in the law's "The great clock's bounds"): he keeps the reading at the start's teeth, "exact wherever the turnover replaces the values and adding no rule and no number". ET3 is that reading with its test changed: the clocks it covers are the floor's (law 4's own trigger) and the stop's, not those whose end teeth fall to or below 0 (a test on the teeth's sign). The two agree on the state everywhere, and on the log wherever the floor never fires.

**What it replaces:** tick.end_teeth's fallback. **What it changes:** no state, and no reading any reader reads. **OPEN for the readers:** the face's before_swap at a turned clock records a carry the law discards. Tensor24's click record does not name it.

## 5. F2: the tension's two sides

### 5.1 The upper side: the tension's carry at the full rate (a threshold)

**The formula.** For a tension t >= 0 of a Mesh: k = t div Gamma, the tension's whole windings at the full rate (Rule3); e = 1 div (1 + k), 1 in the first winding and 0 at any whole one; the factor Q = e ((G^2 (Gamma - t)^2 + Gamma^2 div 2) div Gamma^2). In the clocks: the Mesh is engaged while its tension stays inside its first winding of the full rate, and disengaged when the tension's carry turns (the horizon, ALGEBRA.md's "The horizon": the Mesh read at the teeth count, the run going on decoupled, re-coupled the tick the tension falls back).

**PROVED (for t >= 0).** For 0 <= t < Gamma, k = 0 and e = 1: the head's factor. For t >= Gamma, k >= 1 and e = 0, and the head's factor at min(t, Gamma) = Gamma is (0 + Gamma^2 div 2) div Gamma^2 = 0. So Q is the head's factor for every t >= 0.

**CHECKED (B7 upper; b7_tension.txt):** every t in [0, 5 Gamma] at Gamma 1,000, 6,000 and 23,057 (5,001, 30,001 and 115,286 of them), and 20,000 random (Gamma, t >= 0): all equal.

**OPEN.** (a) The quotient k books nothing by itself: the event of the disengaged Mesh is the click's jam "disengaged" (8,059 of them on the hole's chart). Whether this spelling is a threshold or the clamp written as a quotient is for the second hand and Sofer's check. (b) It stands only on a lower side settled: below 0, 1 + k = 0 for t in [-Gamma, -1], and it is no factor.

### 5.2 The lower side: the lattice's light cone (OPEN)

**PROVED (the lemma).** At a clock at the full rate (p_i = Gamma), the light (pinion = rim, D = 0) has S = 2 rim G^2 (6 Gamma^2 - SUM_j (Gamma - t_j)^2), up to the factor's rounding. When each axis's two Meshes read the clock's own tension t_a and the three are traceless (their drive 3 T_aa - tr sums to 0 over the axes):

    SUM_j (Gamma - t_j)^2 = 2 SUM_a (Gamma - t_a)^2 = 6 Gamma^2 + 2 SUM_a t_a^2,

above 6 Gamma^2 at any tension other than 0. So S < 0: the light is past its edge and the conserved form is no energy. With the clamp, (Gamma - max(t, 0))^2 <= Gamma^2 term by term and S >= 0.

**So no zero and no threshold replaces it with the factor as written.** A tension below 0 reaches no whole unit (no threshold), and there the formula gives a factor above the vacuum's, not nothing (no zero). The clamp spelt with quotients (t times the indicator of t div M >= 0, M above every tension) is the clamp renamed.

**CHECKED (B7 cone and lockstep; b7_tension.txt):**
- with the head's factors, no clock past the light's edge or matter's (D + 2 SUM_j R_j <= 4 w) on any of six charts;
- with the lower side struck (the upper kept): past the edge at 19 clock-ticks on the chiral, 494 on the hole, 20 on the bodies and 2,304 of 3,840 on the bang (the light's grips up to 534,933 times the vacuum's); 0 on ga2 and collapse_500, whose tensions are small at loaded clocks;
- the tensions are traceless but for the carries where they are large: |n_x + n_y + n_z| at most 3 against |n_a| up to 3,988,069 on the bang, 156 against 33,131 on the hole (39 against 81 on the chiral, where the carries dominate);
- struck in lockstep: the hole's stretch at 808 bits by tick 60 (the head 20); the bang's integers past 4,300 decimal digits by tick 9, with no fitting; the chiral and the bodies move from tick 3 and 2 with mild courses (turnovers 853 against 861, 2,090 against 1,934); the rewind 20 of 20 where the run stands.

**What blocks it:** the metric's form. With the convex factor (Gamma - t)^2 and traceless tensions the cone cannot hold without a bound. It needs a factor that holds the cone by construction: the speed along each axis the lapse over that axis's metric, the cone their trace (section 24, item 4, the spatial metric the vector's whole symmetric square, with the lapse; section 25, item 3). David's two-ended cone (Q at most Gamma^2 G^2 div the faster end's mesh rate squared) is itself a bound, and was measured worse (245 bits on the bang). His DAVID-THREE-BOUNDS.md (toys-5 78b84f332) reads bounds (1) and (2) as one letter: the Mesh's own factor and the clock's rates each at most the full rate, so that the grip is at most the vacuum's at every clock and the edge holds rate by rate. That is the cone held by two bounds, not a zero or a threshold. Section 3 removes (2) by the floor; (1)'s lower half stands. It acts at 27% to 76% of the tensions of every chart with light or matter.

## 6. F1: the drive at plus or minus the hold (OPEN)

**PROVED, the algebra** (held_numerator and held_teeth). With N = 4 X (F t rim Gamma^2 - sigma p0^2) p0 and H = X t rim Gamma^4 key (F the forms, sigma the stress's trace):

    N / H = 4 F p0 / (Gamma^2 key) - 4 sigma p0^3 / (t rim Gamma^4 key).

X cancels. The push carries no t; the brake carries 1 / t. The clamp is the identity exactly where |N| <= H; at the full rate, where |F - sigma div (t rim)| <= Gamma key / 4.

**CHECKED, the cap (B3 cap; b3_drive.txt).** At the bang's setting of n quanta per clock:
- the forms at the first tick are n key (3 F div n = 3 key from 500 to 5,000,000 quanta);
- the first step is X1 - X0 = (4/3) n X0 div Gamma within one notch (665 against 666 at 500, 998 against 998 at 749), so the brake is two thirds of the push;
- so the clamp acts at the first tick exactly when (4/3) n >= Gamma: at 750 = (3/4) Gamma and above, not at 749;
- **but below the cap it acts later in the course, and not in order of the quanta:** from tick 21 at 700 quanta, not in 40 ticks at 740, from tick 39 at 749; at 500 not in 40 ticks, nor in 250 (CHECKED below).

**CHECKED, struck (B3 free).** Bit for bit where it never acts (PROVED: min(max(d, -h), h) = d exactly where -h <= d <= h; CHECKED: the chiral 60 of 60 ticks, the bang at 500 quanta 250 of 250). Where it acts:
- the bang at the head's setting: the stretch spikes to 23 bits at tick 1 and the whole board turns over 20 times in 60 ticks (about every 3 ticks), with no fitting (the head 64);
- the hole: 807 turnovers and 20 fittings against 1,073 and 28, its stretch 26 bits against 20;
- the bang at 700 quanta: the same to tick 20, then 136 fittings against 104 by tick 60.

The rewind is 20 of 20 in each.

**CHECKED, the threshold candidate rejected (B3 turn).** No clamp, and a clock whose drive passes the hold turns over (law 4's act with a third trigger, the "next carry" past the hold):
- on the bang at the head's setting the whole board turns at every tick and the stretch never leaves Gamma: 1,920 turnovers and no fitting in 30 ticks;
- on the hole: 2,732 turnovers and no fitting in 60 ticks against 1,073 and 28;
- at 700 quanta: the same to tick 20, then 256 turnovers against 64.

It freezes the great clock wherever the drive binds; and it would be a trigger written for the bang.

**David's reading agrees** (DAVID-THREE-BOUNDS.md): bound (3) "is no edge of Rule3's ... the tick's resolution of that drive ... the owner's to weigh".

**Verdict: OPEN.** The drive is not 0 where it binds (no zero). The hold is no whole unit of a gear: it is X teeth of the drive, a bound on the push per tick. Its one natural carry, the turnover, freezes the great clock (no threshold). F1 goes with the course's closure (draft C): the brake overtaking the push by the act itself, so that the drive stays inside its hold with no clamp. A setting below the cap keeps the clamp idle at the first tick, and not over the course (700 quanta: from tick 21).

## 7. R10 and BH-S1: the stopped clock (partly a zero; OPEN)

**Where.** No chart stops a clock at its own ticks (B1).
- The head's BH-S1 test world (tests/test_the_node.py: the 3-cube's centre fed to the stopped load's level, 4,268,834,097, both slots) stops it at 100 of 100 ticks. The stopped load is 3,793 at Gamma 1,000, where the rate is 22 and the mesh rate 0; the rate itself reaches 0 only at the load 7,598.
- The hole run to 900 ticks stops clocks at 397 clock-ticks from tick 476 (B6 chart).

**PROVED, the zero that holds.** The clock's own grips R_ij = 2 pinion p_i^2 Q_ij vanish at the mesh rate p_i = 0 whatever Q_ij is. So the factors' mask at the stopped clock's own end is redundant: the formula gives nothing there.

**CHECKED (B6 fed; b6_stopped.txt).** With no mask, 0 nonzero grips at the centre over its 100 stopped ticks (six trains, six Spokes each).

**What the zero does not give** (CHECKED, B6 fed, variant Z: readings.stopped_of reads no clock stopped, so the tick's mask, the restore, the dial's hold, the factors' mask and the click's skips all go):
1. **The neighbours' grips toward the stopped clock**, 2 pinion p_j^2 Q_ji at the neighbour's own rate, are not 0 without the mask: 3,600 of 3,600 on the head's run. The Mesh read from one end decouples that end only.
2. **The inertia and the drive.** With no restore the stopped clock's gears coast (p+ = p, the free linear growth): the centre's light gear goes from 189 to 16,949 in 100 ticks. Its time gear, fed at rest, climbs by its own drive (372,746 notches at the first tick and rising), from 4,268,834,097 to 6,008,523,804 in 100 ticks, with no top and so no turnover: the clock sinks deeper and is never released.
3. **The dial.** The rate at the stopped load is 22 (the mesh rate's zero, p0^2 below Gamma div 2, is not the rate's), and the dial advances 21 to 22 a tick where the head holds it.
4. **The course: the stop spreads.** Pulled through the one-ended Mesh toward the centre's stretch, the fed centre's six neighbours go from the load 0 to 3,556 in one tick and past the stopped load (3,793) by tick 4. Then their own grips toward the centre are 0 by the zero (144 of 3,600 left nonzero in the Z run). The fed 3-cube turns 5 times in 100 ticks against the head's 362.
5. **On the hole at 900 ticks** (B6 chart, Z in lockstep with the head): the state bit for bit to tick 475; from tick 476, the first stop, every tick differs (425 ticks). Turnovers 3,642 against 4,020, fittings 35 against 35, bob clicks 58,455 against 58,295, the stretch at 50 bits against 33. The rewind of 20 from tick 471, across the first stop, is exact (20 of 20).
6. **The rewind** stays exact without the restore (100 of 100 on the fed world): the restore is no part of the rewind.

**So the plan's R10 row ("a zero: the rate 0 gives nothing, with no restore") is false on the head's formula.** **OPEN, what blocks it:**
- **(a) the inertia.** The driven trains' teeth W grow with X, so they freeze only at the pole X -> infinity (the lapse 0), which no finite gear reaches (PROVED from the step: with F and K at 0, a+ - a = (p + mid W+) div W+, which is 0 only while p lies within half the teeth, and W+ is finite at every finite X). The regulator steps at its own fixed teeth, so its gears coast at any rate. A horizon from the lapse (section 25, item (e)) needs the lapse in every train's inertia, the regulator's own included.
- **(b) the one-ended Mesh.** A grip read from both ends (say the two ends' mesh rates in one product) decouples both ends at the zero, but it changes every chart where neighbouring rates differ, so it is no replacement bit for bit (PROVED: 2 pinion p_i p_j Q_ij differs from the head's 2 pinion p_i^2 Q_ij wherever p_j differs from p_i).
- **(c) the readings.** The dial is a reading: no act reads it, only run.py's entries and the readers (CHECKED by a search of src). Its hold, and the click's skips (bobs.py:51, click.engage, splits), are readings of the mask and go with the readers' rewrite (the dial read as the clock's chimes).

## 8. The held field's load in D and its mass source (no train known)

**The formula.** Every train r carries a calibre weight w_r, 0 where the file names none.
- **The held load:** c_held = c + SUM_r w_r a_r0, the contraction of the weights with each train's first gear at the tick's start. A weight stands only on a real gear, an A1 scalar: a hand's two gears are no invariant of its own phase, so the product table gives a hand no linear term. That is a check of the files outside the engine, not a branch.
- **Every train's spring:** D_r = 12 (rim - pinion_r) p0(c_held)^2 G^2, alike.
- **The masses' contraction:** M = SUM_r carries(D_r <a_r, a_r>, T), every train's spring times its own square in the teeth, read from the start board.
- **On every real gear g:** (q_g, r_g) = carry(w_g M + (the gear's other drive numerators), key, r_g), landing as K_g = T s q_g.
- For w_g = 0 the carry of 0 gives q = 0 and leaves r_g (0 <= r_g < key), at +1 and at -1. Two numerators in one drive equal two drives (identity I3, section 9).
- **In the clocks:** the held load is the clock's load plus each train's weight times its notch; the held field's drive carries its weight times the masses at the key.

**PROVED.** With the weights 0 but the held field's, c_held and the kick are the head's (tick.py:106 and 229), with no `weight is not None`.

**CHECKED (B4 head, the bang 250 ticks; b4_held.txt).** The generic held load against the head's: 0 mismatches of 16,000 clock-ticks.

**The order (R8).** The head's M sums only the trains met before the held field in the acts' order. The order-free M adds the held field's own mass density (the trains after it, the offset, have no spring).
- **CHECKED:** they differ at 7,680 of the bang's 16,000 clock-ticks, every one through the held field's own term (its notch reaches 42 after the fittings of tick 7).
- **CHECKED (B4 free), the order-free source in lockstep:** the bang's state moves from tick 11, at 96 of its 250 ticks; its turnovers, fittings and bob clicks stay the same (3,200, 64, 28,736). So R8's order is no fake of the counts on the bang, but it is one of the state: the held field does not source itself on the head.

**OPEN: the two couplings of one weight are not one coupling.** In the step T a'' = -D(c_held) a + ... (W ~ T X, s = X), so each hand's potential is (1/2) D(c + w phi) <a, a>.
- The reaction this implies on the held field, -(1/2) (dD / dphi) <a, a>, is w D <a, a> / Gamma to first order, since D falls by 2 w / Gamma per notch of phi.
- The head's source is T q = w D <a, a> / key.
- **CHECKED (B4 energy, from the head's own rate table):** the reaction over the source is 35.96 at the load 0 (key div Gamma = 36), 36.3 at 10, 39.7 at 100, 48.8 at 1,000. At 3,000 it is 0: the integer rate (50) does not resolve the shift, while the source stands.
- So the held field's action and reaction differ, and no energy over every train and the held field is kept by the step: the books cannot close on it.
- David's DAVID-MEDIATOR.md asks "whoever reads with w sources with w". The weight matches; the teeth (Gamma for the load's unit, key for the source) do not.
- The rate p0(c + w phi) is itself the typed exponential (E8, cut 4).

## 9. The release's advance and its recoil (every hand alike)

**The formula** (in place of tick.advances, forward and backward alike):
- **The coupling and the receiver:** u_h = pinion_h div rim_h, the hand's own Rule3 quotient, 1 where the pinion fills a whole rim and 0 at every gapped pair; c_h = 1 - u_h.
- **The release:** R = s SUM_h c_h (a_h3 F_h12 - a_h12 F_h3), the stretch times every hand's cross of its notches and its pull.
- **The advance on every hand's first gear:** rho = rounded(R, W+) (the head's odd rounding); (q_h, r_h) = carry(u_h rho, key, r_h); landing as the kick K_h0 = W+ q_h before the gear's own carry.
- **The push:** P_a = SUM_h 2 pinion_h q_h (a_h0(x - e_a) - a_h0(x + e_a)), with a_h0 the first gear's start notch.
- **The recoil:** the regulator's flow gear of axis a carries N_a = p0^2 (V_a - P_a), with V_a the hands' count flow, in its one drive: a term of the regulator's drive, J's metric half.
- **In the clocks:** the sprung hands' cross of notch and pull is wound into the first gear of the hand whose pinion fills its rim; what it moves there pushes back on the regulator's flow gear of each axis, weighed by the rate squared.
- It is K's form, not F's: K_h0 / s is no integer, and the advance is a whole count of the end teeth.

**PROVED.**
- **I1, the coupling:** c_h = min(rim - pinion, 1), the head's coupling_of, for every 0 <= pinion <= rim.
- **I2, the advance as a kick:** an advance of q notches after the carry at W+ is the kick W+ q before it, since (p + W+ q + mid W+) div W+ = (p + mid W+) div W+ + q, with the same remainder.
- **I3, the recoil merged:** two drives at one teeth count, the remainder carried, equal one drive of their sum, at +1 and at -1. So the head's second drive of the flow gears (unwind.recoil) is one drive.
- **The push:** the head's push reads the before slot after the carry, which is the start notch. Read from the start notches (tick.at), it is the same in both goings, so **the rewind needs no tally**.
- For u_h = 0 the carry of 0 leaves the drive remainder, so the gapped hands' first gears hold one more remainder each that never moves.
- R4 is untouched: c_h is the head's coupling, a step of the spring.

**CHECKED (B5; b5_release.txt):**
- I1 on 21,015 pairs (every calibre's rows and random ones), I2 on 100,000 random draws, I3 on 100,000: all hold;
- **the generic act in lockstep with the head:**
  - the charged packet (row 1 at 40 quanta, sense 1, wave den div 4, on the hole's 5-cube toy calibre; section 11), 60 ticks: the state bit for bit at every tick, the logs equal, laid 272 = 272 at 264 clock-ticks, 159 of them at clocks that stand (b5_explore: 105 at turned clocks); the rewind 20 of 20 with no tally;
  - the same packet at 4 quanta over 30 ticks (laid 6, all at clocks that stand), the hole 60 (laid 4, both at turned clocks), the polarization 12 (laid 33), the packet 150 (laid 6), collapse_1200 600 (laid 8), the one big bang 250 (laid 0): every tick's state bit for bit, the logs equal, the rewind exact with no tally (20 of 20, the polarization 12 of 12);
- the gapped hands' drive remainders moved: 0.

**What it replaces:** clock.unsprung() at tick.advances (and at the push's pinion), the release's tallies in the rewind note (state beyond the clock), and the second drive of the flow gears. **What it leaves:** R4 (every matter train coupled at 1; the plan's "the coupling the spring itself" would change every release) and E8's rounded rate, as on the head.

## 10. For the second hand: what to attack

1. Section 3's invariant: a setting that leaves a time gear below Gamma (none of the 21 does); the stop's restore under the raised floor; the backward trigger.
2. Section 4: a fallback at a clock neither turned nor stopped (B1 counts 0, and the proof says none can be); the faces that move.
3. Section 5.1's identity at t >= 0; 5.2's lemma (the traceless, two-ends-equal case), and whether any other factor holds the cone and is the head's on every chart.
4. Section 6: the cap (749 against 750), the later binding below it, and whether any threshold of the integers leaves the head's bang.
5. Section 7: the coasting, and whether the restore is needed for anything but the frozen chart.
6. Section 8: the factor 36 (the reaction read from the rate table); the self-source the order-free M adds.
7. Section 9: the start-notch push in both goings (the rewind with no tally), and the generic advance on the twin hands (u = 0).

## 11. The probes and their outputs (S/derive/B)

Each probe prints one JSON line per run. Its .txt holds every line of every run quoted in this draft, written out by bsummary.py (b1's by b1_table.py). All ran as `/home/user/Universe24/venv314/bin/python -I PROBE ...` with no file of the repository edited.

| probe | what it checks | output | the runs quoted |
| --- | --- | --- | --- |
| bcommon.py | the harness: the 21 charts (CHARTS), the clock from a world, the state as text, the counters of the five bounds | - | - |
| b1_counts.py, b1_table.py | where each bound acts | b1_counts.txt | `b1_counts.py --all`, tabulated |
| b2_floor.py, b2_faces.py | FLOOR, ET, ET3, BOTH, BOTH3 in lockstep with the head: the state at every tick, the log entry by entry, F5 under the variant, the rewind of 20; which face fields move | b2_floor.txt | every variant on every chart of CHARTS (BOTH3 on the hole, the chiral, node); faces: ET and ET3 on the hole and the chiral |
| b3_drive.py | F1: the cap at the bang's setting; the clamp struck; the turnover past the hold | b3_drive.txt | `cap 500 700 740 749 750 751 800 1000 5000000`; `free` on the chiral 60, the hole 60, the bang 60, the bang at 700 quanta 60, the bang at 500 quanta 250; `turn` on the hole 60, the bang 30, the bang at 700 quanta 60 |
| b4_held.py | the held load's generic form, R8's order, F5 through the held load; the order-free source in lockstep and its rewind; the two couplings | b4_held.txt | `head 250`, `free 250`, `freerewind 15 20`, `energy` |
| b5_explore.py, b5_release.py | where the head's release advances; the generic act in lockstep; I1 to I3 | b5_release.txt | explore: the hole 60, the charged packet (the seed below) at 40 quanta over 30 and 60 ticks and at 4 over 30; lockstep: the same packet at 40 over 60 and at 4 over 30, the hole 60, the polarization 12, the packet 150, collapse_1200 600, the bang 250; `identities` |
| b6_stopped.py, b6_spread.py | the fed stopped clock under the head and under Z; the stop spreading; the hole at 900 | b6_stopped.txt | `fed head 100`, `fed Z 100`, `chart Z world_hole.json 900`; `b6_spread.py 8` |
| b7_tension.py | F2: the cone with and without the lower side; the upper side's carry; the lower side struck in lockstep | b7_tension.txt | `cone` on the chiral 60, the hole 60, the bodies 120, the bang 60, ga2 230, collapse_500 600; `upper`; `lockstep` on the chiral 60, the hole 60, the bodies 120, the bang 30 |
| bsummary.py | the JSON lines written as text | - | - |

The charged packet: world_hole.json's piece with the seed `[{"lay": "sea", "row": 0}, {"lay": "at", "row": 1, "centre": [2, 2, 2], "width": 2, "quanta": 40, "sense": 1, "wave": [3790714189778097, 0, 0]}]`, the wave den div 4.
