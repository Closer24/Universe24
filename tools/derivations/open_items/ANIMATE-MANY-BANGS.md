# The many bangs from the clocks (Animate's draft, under derive/PROTOCOL.md, steps 1 to 4)

The owner's words to Animate, 2026-10-28 (Hebrew, translated):
- 11:5x UTC: "Many bangs must follow from the board, the tensors and the system as one clock. Think what brings it about. The Links that stretch and then shorten: what is it at a Node-clock, and what is it for the whole system, which actually produces the bang. It must be solved at the high level."
- 12:1x UTC: "Derive it yourself, through the logic of the clocks and the tensors, and sync with everyone."

It stands under law 10 (time on the board is a circle, and every bang shows more, the owner's word of 12:1x UTC) and under the Boss's "no bound and no floor" (#2187, 6468487676). It builds on draft C (derive/C: the derived push, the theorems C1 to C6, the rate chain's zero) and its verifier (derive/C_verify).

The probes are in ANIMATE-PROBES-2 (README there): many_bangs.py on the engine, and tst_time_gear.py in pure integers. Every claim is marked PROVED, CHECKED or OPEN.

## 0. The answer

- **The course is one swing of the great clock per bang.** Nothing is typed into it. In order:
  - **The push drives it out.** The push is draft C's, general relativity's A1 volume equation in the board's integers. The Links stretch, and every Node-clock slows.
  - **The horizon.** The clocks slow until their Mesh rate rounds to 0 (Rule3's own zero). Past that point no Mesh carries anything.
  - **The top.** At the horizon the great clock reads the stretch as held, so law 4's own top fires there, with no ceiling.
  - **The run back.** The turnover reverses time, and the run back retraces the rise exactly, as T S T = S^-1 for the time gear's step.
  - **The bang.** The run back arrives at the seed's stretch at rest. There the push turns it out again, with no floor. That bottom is the bang, and the births come there.
- **CHECKED on the one big bang** (64 Node-clocks, 5,000,000 quanta, 250 ticks). Law 4's floor clause was struck, and BH-S1's restore was struck, with law 4's reading of a clock with no tick as the only rule in their place. The run's integers are bit for bit draft C's (state hash 77e8684641d42469):
  - 5 tops, at ticks 24, 71, 118, 165 and 212;
  - every bottom at X = 1,000 at rest;
  - the floor's trigger true at 0 Node-clock ticks;
  - the rewind 20 of 20 from ticks 15, 40 and 60, through a top and a bottom;
  - the books closed at 250 of 250 click phases.
- **The bottom carries no trigger, and it must not.** The Boss's candidate, law 4's bottom as the top's mirror (the weak minimum), was run in place of the floor (CHECKED, 5,000,000 quanta, 250 ticks):
  - as the full mirror (X0 >= X1 <= X2, one strict), it fires at the seed itself, at rest with the push about to raise it. The board turns over at every tick and never leaves the seed: X = 1,000 throughout, no bang and no birth;
  - entered from above only (X0 > X1 <= X2), it turns the board over at every bang, the light reversed there. Every bang then replays the first: the same top 4,638,548,302 every time, and no birth in 250 ticks.

  With no trigger, the push turns the course at the bang and the births come there (96).
- **Over 1,000 ticks:**
  - 21 tops at 5,000,000 quanta, one every 47 ticks;
  - 7 tops at 500,000 quanta, one every 147 ticks, so a tenth of the light lengthens the bang by 3.13, against Friedmann's square root of 10, 3.16;
  - every bottom's state distinct from every other, 22 of 22 and 7 of 7, so no bang is a copy (row 1c).
- **Law 10, "every bang shows more", is not met on this world.**
  - The births come only at the bangs: +64 at tick 47 and +32 at tick 94 at 5,000,000 quanta, all at X = 1,000.
  - From the fourth bang on, no click comes, and the stretch's course runs as a palindrome about every top. Row 46's reading (the click counts per bang rising) fails from the third bang (64, then 32).
  - At 500,000 quanta the births come at the 2nd, 4th and 7th bangs (32 each) and at none between.
  - What every bang needs is a source of new clicks: OPEN (part 5).

## 1. At a Node-clock and for the whole system (the owner's question)

- **A Link's length is its clock's stretch,** the notch X of the clock's time gear. X = ceil(Gamma^5 / p0^4), so a slower clock (a smaller rate p0) has longer Links. The Links stretch exactly when the clocks slow.
- **At a Node-clock** the time gear steps by X+ = 2 X - X- + q.
  - The push q comes from the clock's own wind: its light's and its springs' (draft C, section 4).
  - The light pushes the clock to slow, and the first difference of X never falls (draft C, C2).
- **The horizon.** The clock's Mesh rate p_m = rounded(p0^2, Gamma) is the rate at which its Links carry. It rounds to 0 where 2 p0^2 < Gamma: at the stopped load 3,793 at Gamma = 1,000, the rate 22, X_c = 4,268,834,097 (about 4 Gamma^3).
  - Past it no Mesh of the clock carries anything, and the factors are 0 from both ends.
  - That is the slowest a clock on the integers can be read by its neighbours: the board's horizon.
  - Under law 11 (every bound is a clock's carry) it is no bound: the Mesh rate is a carry's quotient, and at the horizon the clock's Mesh dial completes no turn in a tick, so no event crosses its Links. The top's turnover is the event.
- **For the whole system.** Where every clock steps alike (the A1 course), the board is one clock, and its stretch is the universe's scale. It rises to the horizon, turns over, runs back and comes to the bang: one swing per bang.
  - The bang is where the Links are shortest and the light densest, at the seed's stretch, the full rate.
  - The top is where the Links are longest, at the horizon.
  - The maximal scale per bang is a_c = Gamma / p_c, about the square root of 2 Gamma (about 45 at Gamma = 1,000). It is set by the clock's fineness Gamma alone.
- **Locally the same.** Off the A1 course, a region whose clocks reach the horizon alone turns over alone: the local turnovers, the stopped clocks of the black holes. A bang is that turnover done by the whole board at once.

## 2. The formula (step 1)

- **The time gear's step:** X+ = 2 X - X- + q, with q, r_d' = carry(N + r_d, T_d) and N = X ((d + 1) G + 2 d V), draft C's derived push. It has no typed form and no clamp.
- **Law 4's top:** X0 <= X1 >= X2 with one of the two strict. X2 is the clock's notch after its tick. Where the clock has no tick (its Mesh rate 0 at the tick's start), X2 is X1.
- **The turnover T:** the time gear's two slots exchanged, and every fine tooth turned as the engine turns it. Proposed: the drive's fine tooth flipped, r to T_d - 1 - r (part 3, P3).
- **Struck:**
  - law 4's floor clause (X_f);
  - BH-S1's restore of a stopped clock's gears (R10);
  - the drive's clamp at the hold (F1, with bound (3), the owner's word of 11:5x);
  - any ceiling.
- **What it holds:** Rule3's carries, sums and products, and law 4's comparisons of three notches. No typed number: the push's counts d + 1 and 2 d are the lattice's (draft C).

## 3. The proofs (step 2)

- **P1, the horizon is Rule3's own zero.** The rates' table steps the hollows by Gamma - 1 over Gamma per load. It reads p0 = rounded(N, Gamma^2) and p_m = rounded(p0^2, Gamma), half up (core/rates.py, Side.fill_to). The first load whose p_m is 0 is the stopped load (rates.stopped_load).
  - No number enters but Gamma, the universe file's integer.
  - PROVED by the table's construction. CHECKED: 3,793, rate 22, X_c = 4,268,834,097 (derive/C_verify/rate_zero.txt).
- **P2, the top with no ceiling.** A clock that rises into the horizon has X0 < X1. It has no tick there, so X2 = X1, and law 4's weak maximum holds with one strict: the turnover.
  - A clock that reaches the horizon at rest (X0 = X1) would stay held. On the A1 course that never happens, because the first difference never falls (C2).
  - PROVED. CHECKED: every top at the first tick with every clock past the horizon (24, 71, 118, 165, 212).
- **P3, the run back: T S T = S^-1 for the time gear's step.** Let s+ = S(s), with q = (N + r) div T_d and r' = (N + r) mod T_d.
  - The turned state T(s+) holds (X+, X) and the flipped tooth T_d - 1 - r'.
  - The forms are their own image under the exchange (the engine's symmetric form), so the push read there is the same N.
  - Then (N + T_d - 1 - r') div T_d = q + (T_d - 1 - r) div T_d = q, since 0 <= T_d - 1 - r < T_d. The new tooth is T_d - 1 - r.
  - So S(T(s+)) = T(s) at every teeth count, odd or even. PROVED.
  - CHECKED (tst_time_gear.txt), at every teeth count from 8 to 15, every tooth and every push in [-3 T_d, 3 T_d]:
    - the flip: 0 failures;
    - the mirror (2 mid - r), which the engine applies to the drive's tooth: it fails at the even counts exactly where r = 0 or r' = 0 (the mathematician's finding);
    - the mutant that keeps the tooth: it fails everywhere.
  - CHECKED on the engine: X at top + k equals X at top - 2 - k for 23, 24, 24, 71 and 118 ticks after the first five tops. Each retrace runs to the bottom, or further back, to the last births. The rewind is 20 of 20 from ticks 15, 40, 60, 180 (5,000,000 quanta) and 140 (500,000, through a tick with births).
  - The driven gears' strides at even teeth are the parity item, owed with the two candidates (ANIMATE-PROBES-1/parity.txt). They held on every run here.
- **P4, the bottom with no floor.** The forward course leaves the seed at rest (both slots at Gamma, clock.start_state). By P3 the run back arrives at T(seed): X = Gamma, at rest. There the push is at least 0 (C2), so the course rises again: the bottom is a weak minimum at rest, with no trigger.
  - After the first bottom the course does not repeat the first bang: X at tick 48 is 20,000,876, against 20,001,000 at tick 1.
  - PROVED. CHECKED: the floor's trigger true at 0 Node-clock ticks in every run; with the floor clause struck, the same integers bit for bit.
  - A trigger at the bottom does harm (CHECKED, part 0). The seed at rest is itself a weak minimum, so the full mirror freezes the board there. A turnover at a bottom entered from above reverses the light at the bang, so the next rise replays the last and the births never come.
- **P5, BH-S1's restore is not load-bearing.** By P2 a clock turns over at its first tick past the horizon, and the turnover sets its whole state from the tick's start. So the restore of its other gears never reaches the course.
  - CHECKED: with no gear restored and law 4's reading alone, the same state hash.
  - In the asynchronous runner (the owner's word of 11:3x UTC: each Node-clock on its own tick), a clock whose Mesh rate is 0 takes no tick. Law 4's reading is then that runner's own fact: the great clock sees no change across the horizon. It is not a mask.
- **P6, the births at the bang.** Every birth comes at a bottom, at X = 1,000:
  - at 5,000,000 quanta, +64 at tick 47 and +32 at tick 94;
  - at 500,000 quanta, +32 at ticks 147, 441 and 882.

  The fittings come where the light is densest. CHECKED.

## 4. Law 10 on the course (CHECKED)

| quanta, ticks | tops | births per bang | bottoms' states distinct | the course after the last births |
|---|---|---|---|---|
| 5,000,000, 1,000 | 21, every 47 ticks | 0, 64, 32, then 0 for 18 bangs | 22 of 22 | X a palindrome about every top, back to tick 94 |
| 500,000, 1,000 | 7, every 147 ticks | 0, 32, 0, 32, 0, 0, 32 | 7 of 7 | the retrace broken at each tick with births |

- **Row 1c,** "each bang carries the last; no bang a copy": holds on every run. Each bottom's state is distinct, because the births of the earlier bangs stay.
- **Row 46,** "each later bang shows more", read as the click counts per bang rising: fails, at 5,000,000 quanta from the third bang. Where no click comes, the course is time-symmetric about each top and the history replays mirrored.
- **What law 10 needs on this course:** new clicks at every bang. This world's light is fitted in two or three bangs (96 births in all, at both settings), and then nothing new comes.

## 5. Owed, by name (OPEN)

- **(a) Law 4's reading at a clock with no tick.** The law's sentence, and the horizon's reading (line 1610: the Mesh factor at 0 from Gamma on), are Sofer's. In the synchronous probe the reading is spelt as a selection. In tensor24's asynchronous runner it is no tick.
- **(b) The asynchronous runner's tick,** with the lapse counted once: David's formula (section 31). The A1 course here is the same sequence of states under any schedule that steps the clocks alike.
- **(c) The drive's fine tooth at the turnover:** the flip in place of the mirror (P3), one line. The driven gears' strides at even teeth go with the parity candidates.
- **(d) New clicks at every bang (law 10).** Candidates:
  - twin hands in the calibre, whose splits draw at every bang; the one big bang has none (open item 11 e);
  - the late settings carried back by the turnover to the next birth (89d4d2a9e);
  - a lay whose light outlasts the fittings.
- **(e) Local contractions with no floor.** Six charts send clocks into the hills (draft B). The weak minimum cannot serve as their bottom: it freezes every clock that starts at rest and is pushed (part 0). Under law 11 (the owner's word of 12:5x UTC, "every bound is a clock's carry"), a clock's dial that would pass the full rate needs its own carry, to derive. On the A1 course here no clock falls below the seed's stretch.
- **(f) The other closure, by general relativity's 00 equation** (draft C's verifier). The seed's breach acts as k > 0.
  - On a sprung hand it gives natural tops and bottoms with no horizon: tops at 40, 118, 193, 266 and 337 with 20 quanta, each different.
  - On the plan's light seed it is static.
  - Its exact rewind is owed. On the area Y = a^2 its step would be a plain second difference.
  - In nature a recollapse is curvature's, not a horizon's. The horizon's top here is a property of the integers: draft C's "a horizon of the ruler". For David to weigh.

## 6. What it replaces (step 4)

- **R10, BH-S1's restore:** struck, in favour of law 4's reading of a clock with no tick (P2, P5).
- **Law 4's floor clause** (X_f = 19, stretch LOW = -1, readings.bottom): struck for the course, with no bottom trigger in its place (P4). The six charts' local contractions are (e).
- **F1 and bound (3):** gone with the derived push (draft C), on the owner's word of 11:5x.
- **The ceiling:** never typed. The top is law 4's own, at the horizon.
- **The rows:**
  - row 1 reads the tops (21 in 1,000 ticks at 5,000,000 quanta);
  - row 1c reads the bottoms' distinct states;
  - row 46 reads the click counts per bang, which fail from the third bang here (part 4).
- **Section 18, root VI, and law 10's sentence:** the closure stands on the horizon with no declared number. Law 10's "every bang shows more" waits on (d).

---
Animate, reader-5.
