# The many bangs from the clocks (Animate's draft, under derive/PROTOCOL.md, steps 1 to 4)

The owner's words to Animate, 2026-10-28 (Hebrew, translated):
- 11:5x UTC: "Many bangs must follow from the board, the tensors and the system as one clock. Think what brings it about. The Links that stretch and then shorten: what is it at a Node-clock, and what is it for the whole system, which actually produces the bang. It must be solved at the high level."
- 12:1x UTC: "Derive it yourself, through the logic of the clocks and the tensors, and sync with everyone."
- 12:4x UTC: "Note that floors and bounds are no longer allowed. Get updated from the Boss."

It stands under three laws not to be crossed:
- law 10: time on the board is a circle, and every bang shows more;
- law 11: every bound is a clock's carry;
- "no bound and no floor": no clamp, no floor value, no range and no mask (#2187, 6468487676 and 6468668551; scribe-5 d4ef8db4, "A floor or a bound is an if, and the Node-clock has none").

It builds on draft C (derive/C: the derived push, the theorems C1 to C6, the rate chain's zero) and its verifier (derive/C_verify). The probes are in ANIMATE-PROBES-2 (README there): many_bangs.py on the engine, and tst_time_gear.py in pure integers. Every claim is marked PROVED, CHECKED or OPEN.

## 0. The answer

- **The course is one swing of the great clock per bang, with no bound, no floor and no mask in its own acts.** In order:
  - **The push drives it out.** It is draft C's: general relativity's A1 volume equation in the board's integers, with no clamp. The Links stretch, and every Node-clock slows.
  - **The horizon is a dial's whole turn (law 11).** Each clock's load counts its slowing from the vacuum (load 0, the full rate) up to the stopped load L_c, where its Mesh rate rounds to 0. That is Rule3's own zero: 3,793 at Gamma = 1,000, X_c = 4,268,834,097.
  - **The top.** The load is a dial of L_c teeth. Its whole turn leaves as an event, the turnover: law 4's top as law 11 has it at the time gear. There is no ceiling, no hold and no mask, and BH-S1 is struck everywhere: its hold, its restore, its mask on the Meshes and on the dial, and the click's skip.
  - **The run back.** The turnover reverses time, and the run back retraces the rise exactly, as T S T = S^-1 for the time gear's step.
  - **The bang.** The run back arrives at the seed's stretch (load 0) at rest and passes no turn there, so no event comes. The push turns it out again, and the births come there.
- **CHECKED against draft C's run** (64 Node-clocks, 5,000,000 quanta). With law 11's top, no floor and BH-S1 struck everywhere, every integer of the state but the dial is draft C's bit for bit:
  - at 250 ticks, 131263b34da818ef with the dial left out;
  - at 1,000 ticks, 1bc59fa2b92b6617;
  - the dial now counts each clock's own rate past the horizon too.

  Over the 250 ticks:
  - tops at 24, 71, 118, 165 and 212;
  - every bottom at X = 1,000 at rest;
  - the rewind 20 of 20 from ticks 15, 40 and 60, through a top and a bottom;
  - the books closed at 250 of 250 click phases.
- **The engine under the course still holds three bounds that act** (the audit, part 4):
  - **The Mesh tension's clamp into [0, Gamma] (F2)** acts at 91,776 values in 250 ticks, and it is load-bearing. With it struck, the course runs away: X = 27,218,198,742,186 at tick 7, below 0 at tick 14, and refused by name at tick 15.
  - **The draw's room capped at the modulus** acts at 1,652,896 draws.
  - **The coupling min(spring, 1)** acts on the three sprung hands.

  So the course's top and bottom hold no bound, but the course stands on F2. Law 11's carry for the tension is owed (part 6).
- **The bottom must carry no trigger.** Law 4's bottom as the top's mirror, the weak minimum (written in the law's "The floor" as the candidate, scribe-5 line 1608), was run in place of the floor:
  - as the full mirror (X0 >= X1 <= X2, one strict), it fires at the seed itself, at rest with the push about to raise it. The board turns over at every tick and never leaves the seed: no bang and no birth;
  - entered from above only (X0 > X1 <= X2), it turns the board over at every bang. Every bang replays the first, with the same top, 4,638,548,302, every time, and no birth.
- **Law 10, "every bang shows more", is not met on this world.**
  - The births come only at the bangs: +64 at tick 47 and +32 at tick 94, at X = 1,000.
  - From the fourth bang on, no new birth comes, and the stretch's course is a palindrome about every top.
  - What every bang needs is a source of new clicks: OPEN (part 6).

## 1. At a Node-clock and for the whole system (the owner's question)

- **A Link's length is its clock's stretch,** the notch X of the clock's time gear. X = ceil(Gamma^5 / p0^4), so a slower clock (a smaller rate p0) has longer Links. The Links stretch exactly when the clocks slow.
- **At a Node-clock** the time gear steps by X+ = 2 X - X- + q.
  - The push q comes from the clock's own wind: its light's and its springs' (draft C, section 4).
  - The first difference of X never falls on the A1 course (draft C, C2).
- **The horizon, as a dial.** The clock's load counts its slowing in hollows, each multiplying the rate by Gamma - 1 over Gamma.
  - Its Mesh rate p_m = rounded(p0^2, Gamma) is the count of whole Mesh turns its Links make in a tick. That count reaches 0 at the stopped load L_c, where 2 p0^2 < Gamma: L_c = 3,793 at Gamma = 1,000, the rate 22.
  - Past it no Mesh of the clock completes a turn, so nothing crosses its Links.
  - Under law 11 the load's range is a dial of L_c teeth from the vacuum, and its whole turn is an event.
- **For the whole system.** Where every clock steps alike (the A1 course), the board is one clock, and its stretch is the universe's scale.
  - The load rises together on every clock to the dial's whole turn: the turnover. Then the run back, and the bang at the dial's zero: one swing per bang.
  - The bang is where the Links are shortest and the light densest. The top is where the Links are longest.
  - The maximal scale per bang is a_c = Gamma / p_c, about the square root of 2 Gamma (about 45 at Gamma = 1,000). It is set by the clock's fineness Gamma alone.
- **Locally the same.** Off the A1 course, a region whose clocks complete the dial's turn alone turns over alone: the local turnovers, the black holes' stopped clocks. A bang is that turnover done by the whole board at once.

## 2. The formula (step 1)

- **The time gear's step:** X+ = 2 X - X- + q, with q, r_d' = carry(N + r_d, T_d) and N = X ((d + 1) G + 2 d V), draft C's derived push. It has no typed form and no clamp.
- **Law 4's top as law 11's carry.** The turnover comes at the clocks whose load at the tick's start has completed the horizon dial's turn: the quotient load(X) div L_c is 1.
  - L_c is the first load whose Mesh rate is 0, from Gamma alone.
  - The quotient is the event, as the winding's quotient is the click of a whole (law 5).
  - The state is kept whole, the two slots exchanged, so nothing is lost and everything runs back.
- **The turnover T:** the time gear's two slots exchanged, every fine tooth turned as the engine turns it. Proposed: the drive's fine tooth flipped, r to T_d - 1 - r (P3).
- **No bottom trigger.** The load's other end, 0, is the vacuum. The A1 course comes to it at rest and passes no turn, so no event comes there.
- **Struck:**
  - law 4's floor clause (X_f);
  - BH-S1 everywhere: the hold, the restore, the Meshes' and the dial's masks, the click's skip;
  - the drive's clamp at the hold (F1, with bound (3), the owner's word of 11:5x);
  - any ceiling.

  On the A1 course the weak-maximum comparison never fires below the horizon (C2), so the top needs none.
- **What it holds:** Rule3's carries, sums and products, and law 11's quotient as the event. No typed number: L_c comes from Gamma, and the push's counts d + 1 and 2 d are the lattice's (draft C).

## 3. The proofs (step 2)

- **P1, the horizon is Rule3's own zero.** The rates' table steps the hollows by Gamma - 1 over Gamma per load. It reads p0 = rounded(N, Gamma^2) and p_m = rounded(p0^2, Gamma), half up (core/rates.py, Side.fill_to). The first load whose p_m is 0 is L_c (rates.stopped_load).
  - No number enters but Gamma, the universe file's integer.
  - PROVED by the table's construction. CHECKED: 3,793, rate 22, X_c = 4,268,834,097 (derive/C_verify/rate_zero.txt).
- **P2, the top as the dial's turn.** On the A1 course the load rises with X (C2), so it completes the dial's turn at the first tick whose start has X at or past X_c.
  - There the quotient is 1 and the turnover comes. Below it the quotient is 0 and nothing comes.
  - It is the same tick at which BH-S1's frozen time gear made law 4's weak maximum on the head, so the course is the same.
  - PROVED. CHECKED: the same five tops (24, 71, 118, 165, 212) and every integer but the dial the same, at 250 and 1,000 ticks.
- **P3, the run back: T S T = S^-1 for the time gear's step.** Let s+ = S(s), with q = (N + r) div T_d and r' = (N + r) mod T_d.
  - The turned state T(s+) holds (X+, X) and the flipped tooth T_d - 1 - r'.
  - The forms are their own image under the exchange (the engine's symmetric form), so the push read there is the same N.
  - Then (N + T_d - 1 - r') div T_d = q + (T_d - 1 - r) div T_d = q, since 0 <= T_d - 1 - r < T_d. The new tooth is T_d - 1 - r.
  - So S(T(s+)) = T(s) at every teeth count, odd or even. PROVED.
  - CHECKED (tst_time_gear.txt), at every teeth count from 8 to 15, every tooth and every push in [-3 T_d, 3 T_d]:
    - the flip: 0 failures;
    - the mirror (2 mid - r), which the engine applies to the drive's tooth: it fails at the even counts exactly where r = 0 or r' = 0;
    - the mutant that keeps the tooth: it fails everywhere.
  - CHECKED on the engine:
    - X at top + k equals X at top - 2 - k for 23, 24, 24, 71 and 118 ticks after the first five tops, to the bottom or further back to the last births;
    - the rewind 20 of 20 from ticks 15, 40, 60, 180 (5,000,000 quanta) and 140 (500,000, through a tick with births).
  - The driven gears' strides at even teeth are the parity item (ANIMATE-PROBES-1/parity.txt). They held on every run here.
- **P4, the bottom with no trigger.** The forward course leaves the seed at rest (both slots at Gamma, load 0). By P3 the run back arrives at T(seed): load 0, at rest. The push there is at least 0 (C2), so the course rises again, and the load never passes below 0.
  - PROVED. CHECKED: the floor's trigger true at 0 Node-clock ticks in every run.
  - A trigger at the bottom does harm (CHECKED, part 0). The seed at rest is itself a weak minimum, so the full mirror freezes the board there. A turnover at a bottom entered from above reverses the light at the bang, so the next rise replays the last and the births never come.
- **P5, BH-S1 is not load-bearing for the course.** By P2 a clock turns over at the tick it completes the dial's turn, and the turnover sets its whole state from the tick's start. So BH-S1's acts at that tick never reach the gears. CHECKED, every gear's notch and fine tooth the same with BH-S1 struck everywhere. What moves:
  - **The dial,** which now counts the clocks' own rate past the horizon.
  - **At 500,000 quanta, the click's counter.** From the second top on, the click reads the clocks at the top's tick, which BH-S1's mask skipped: 64 more chimes credited that take nothing, and 576 more refusals by tick 300. It is checked at ticks 160, 300, 450, 700 and 900: only the dial and the clicks counter differ.
- **P6, the births at the bang.** Every birth comes at a bottom, at X = 1,000:
  - at 5,000,000 quanta, +64 at tick 47 and +32 at tick 94;
  - at 500,000 quanta, +32 at ticks 147, 441 and 882.

  The fittings come where the light is densest. CHECKED.

## 4. The bounds the engine still holds, audited in the runs (CHECKED)

Counted with law 11's top and BH-S1 struck, at 5,000,000 quanta and 250 ticks: each count is the values the bound changed.

| bound (the law's list, scribe-5 line 106) | values it changed | load-bearing for the course |
|---|---|---|
| a load below 0 read at 0 (rates_of, F5) | 0 | no |
| the end teeth's fallback (Tick.end_teeth) | 0 | no |
| a tension below 0 read at 0 (meshes.factors, F2 lower) | 61,184 | yes, with F2 upper |
| a tension above Gamma read at Gamma (F2 upper) | 30,592 | with F2 struck the course runs away and is refused at tick 15 |
| the draw's room capped at the modulus (draw.py) | 1,652,896 draws | it shapes the births, not the course; owed with the draw's fairness |
| the coupling min(spring, 1) (meshes.coupling_of) | the three sprung hands (springs 2,183,583,978 and about 1.26 and 1.27 x 10^16) | not measured |
| BH-S1's Mesh mask and dial hold | 1,280 and 320 on draft C's run; 0 here, struck | no (P5) |

Over 1,000 ticks F2 acts at 367,488 values (5,000,000 quanta) and 379,008 (500,000), and the room's cap at 6,603,424 and 6,532,960 draws.

## 5. Law 10 on the course (CHECKED)

| quanta, ticks | tops | births per bang | bottoms' states distinct | the course after the last births |
|---|---|---|---|---|
| 5,000,000, 1,000 | 21, every 47 ticks | 0, 64, 32, then 0 for 18 bangs | 22 of 22 | X a palindrome about every top, back to tick 94 |
| 500,000, 1,000 | 7, every 147 ticks | 0, 32, 0, 32, 0, 0, 32 | 7 of 7 | the retrace broken at each tick with births |

- **Row 1c,** "each bang carries the last; no bang a copy": holds on every run. Each bottom's state is distinct, because the births of the earlier bangs stay.
- **Row 46,** "each later bang shows more", read as the click counts per bang rising: fails, at 5,000,000 quanta from the third bang (64, then 32, then none). Where no click comes, the course is time-symmetric about each top and the history replays mirrored.
- **The bang's length** follows the light laid: a tenth of the light lengthens it by 3.13, against Friedmann's square root of 10, 3.16.

## 6. Owed, by name (OPEN)

- **(a) The law's sentences** (Sofer):
  - law 4's top as law 11's carry at the horizon dial, L_c from Gamma;
  - "The floor" (line 1608) with no bottom trigger, in place of the weak minimum, which parts 0 and 3 refute;
  - BH-S1 (line 132) struck;
  - the horizon (line 1610) read as the Mesh rate's zero.
- **(b) F2 as a carry.** The Mesh tension into [0, Gamma] is load-bearing (part 4). Its law-11 form, the tension's dial with its turn as an event, is David's: the light cone, kept by construction.
- **(c) The draw's room** as a carry, with the draw's fairness (the mathematician's finding); and the coupling's cap.
- **(d) The drive's fine tooth at the turnover:** the flip in place of the mirror (P3), one line. The driven gears' strides at even teeth go with the parity candidates.
- **(e) New clicks at every bang (law 10).** Candidates:
  - twin hands in the calibre, whose splits draw at every bang; the one big bang has none (open item 11 e);
  - the late settings carried back by the turnover to the next birth (89d4d2a9e);
  - a lay whose light outlasts the fittings.
- **(f) Local contractions.** Six charts send clocks below the vacuum's stretch (draft B). Under law 11 the load's zero is the same dial's other end: a load that passes below 0 would leave a borrow, whose event is a turnover at the full rate. On the A1 course the load comes to 0 at rest and never passes it.
- **(g) The asynchronous runner's tick,** with the lapse counted once: David's formula (section 31). The A1 course here is the same sequence of states under any schedule that steps the clocks alike.
- **(h) The other closure, by general relativity's 00 equation** (draft C's verifier). The seed's breach acts as k > 0.
  - On a sprung hand it gives tops and bottoms with no horizon: tops at 40, 118, 193, 266 and 337 with 20 quanta, each different.
  - On the plan's light seed it is static.
  - Its exact rewind is owed. In nature a recollapse is curvature's, not a horizon's; the top here is a property of the integers. For David to weigh.

## 7. What it replaces (step 4)

- **BH-S1, R10:** struck everywhere, with law 11's turn of the horizon dial as law 4's top (P2, P5).
- **Law 4's floor clause** (X_f = 19, stretch LOW = -1, readings.bottom): struck, with no bottom trigger in its place (P4). The six charts are (f).
- **F1 and bound (3):** gone with the derived push (draft C), on the owner's word of 11:5x.
- **The ceiling:** never typed. The top is law 11's event at the horizon dial.
- **The rows:**
  - row 1 reads the tops (21 in 1,000 ticks at 5,000,000 quanta);
  - row 1c reads the bottoms' distinct states;
  - row 46 reads the click counts per bang, which fail from the third bang here (part 5).
- **Section 18, root VI, and law 10's sentence:** the closure stands on law 11's horizon dial with no declared number. Its course stands on F2 until (b), and law 10's "every bang shows more" waits on (e).

---
Animate, reader-5.
