# The twin hands in the one big bang, the 24's ladder under Pauli's rule, and the composite clock's click: a toy check for the plan (Animate)

**The owner's words to Animate, 2026-10-28** (Hebrew, translated):
- 13:1x UTC: "Go for it with full force and complete what is missing in the engine. This is excellent. Only complete what is missing according to the laws! Quickly."
- 13:3x UTC: "The law, if one is needed, must be for all the families, realized by the tensors, and work logically from the clocks."
- 13:3x UTC: "Confirm that you understood that the engine is not being built. Sync with the Boss: only confirm that it works and put it into the plan. It is not needed; the engine is not built; only if it is a toy you want to check, whether it will work in the engine."

The Boss's ruling (#2187 6470415933): Animate builds toys that prove something. The prototype of the three pieces is a toy that proves the ladder, its findings enter the plan, and nothing of it enters an engine.

So this page is a toy check and no engine build. The toys run on a scratch copy of engine-5.0-test at 33d9ecaa, with draft C's push and BH-S1 struck, and they are in ANIMATE-PROBES-3. Every claim is marked CHECKED or OPEN.

## 1. What the toy puts in, and nothing else

- **The row:** one row of four gears at the file's own gapped pair. trains.trains_of makes twin hands of it, so there is no new act and no new number.
- **T on every hand, one formula for every family** (the owner's 13:3x word):
  - T = J K with the slots exchanged, where K is the hand's conjugation and J is a row of the kind table: 1 on an A1 hand, [[0, -1], [1, 0]] on the twin pair (-i sigma_y, draft E).
  - So T T = J J: +1 on A1 and -1 on the twins. On the twins T has period four, with no involution claimed (Sofer, 6469988450, item 3 (a)).
  - It reverses the spin: S goes to -S, which commutes with every turn of 2O. The head's K sends S to (Sx, -Sy, Sz) and breaks the 24 (draft E's e5).
- **The time gear's turnover in Sofer's shape** (6469988450, item 1):
  - q = carries(X - Gamma, X_c - Gamma), read once, by the core's carry;
  - the turnover is T applied q times, by the carry of q by 2 and by 4 (T's order on the kind);
  - it is written as the blend new = old + s (T old - old), with s the carry's remainder, so there is no comparison, no branch and no mask;
  - backward it is T applied -q times.
- **Two read places:** q read at the tick's start (READ=start) or at the step's output, which is not written (READ=step).

## 2. The checks

1. **The blend is exact.** With the head's K in place of J K and the stage-1 threshold, the blend reproduces the engine's own masked turnover bit for bit (28e42e907a4ad507 both ways). CHECKED.
2. **The A1 calibre (no twin hands), read at the tick's start:**
   - the carries read are 0 and 1 alone;
   - the tops are at 24, 71, 118, 165 and 212, and the state is draft C's bit for bit (640f11b7135fcbfc; 131263b34da818ef without the dial);
   - the rewind is 20 of 20 from tick 40.

   CHECKED: Sofer's shape holds on the A1 course.
3. **The A1 calibre, read at the step's output:**
   - the course changes, and each top comes one tick earlier;
   - at the fourth bang the push carries the stretch 28 dial turns past the horizon in one tick. T^28 is no turnover, so that stretch is written (X = 122,230,215,667). The board turns over a tick later, at q = 85;
   - the rewind is still 20 of 20.

   CHECKED: the read place is not free, and only the read at the tick's start keeps draft C's course.
4. **The twin calibre with T = J K, at 500,000 quanta:**

   | the form | read at | result | the end teeth's fallback |
   |---|---|---|---|
   | the count (Sofer's shape) | the tick's start | refused at tick 346 | 0 |
   | the count | the step's output | refused at tick 432 | 152 |
   | the count, with the head's K | the step's output | refused at tick 432 | 152 |
   | the stage-1 threshold | the start (top), the step (borrow) | 600 ticks, rewind 20 of 20, births 134, books 597 of 600 | 2,676 |
   | the stage-1 threshold, with the head's K (stage 1) | the same | 600 ticks, rewind 20 of 20, births 154, books 595 of 600 | 2,352 |

   - **Read at the tick's start,** the vacuum's borrow comes a step late. The least stretch falls from 138,036,443 to -13,293,331 within one tick (ticks 344 to 345), so no read at a tick's start can catch it.
   - **Read at the step's output,** the board scatters after the third top. Steps carry the stretch by many dial turns (the carries read run from -6 to 201), and the even counts are written: the largest X reaches 249,893,524,116. A fall with q = -6 is written, and tick 432 is refused. The head's K does the same, so the count form is the failing piece, not T.
   - **The stage-1 threshold** (Sofer: a bound in a quotient's coat) runs with J K too. But every 600-tick twin run stands on the engine's end teeth's fallback (Tick.end_teeth, a bound under the prohibition): 2,676 values with J K, 2,352 in stage 1 at 500,000 quanta, 2,948 in stage 1 at 5,000,000, and 2,264 on the head with the same row. It acts 0 times on the A1 calibre. Past the third top the board scatters past the horizon: the largest X reaches 7.8 x 10^11, with 6,274 local turnovers.
   - **Stage 1's "runs 600 ticks"** (my 6470420841, item 3) is corrected here: those runs stood on the end teeth's fallback.

   CHECKED, each output in ANIMATE-PROBES-3.
5. **The twin calibre with T = J K, at 5,000,000 quanta:**
   - **The count form, read at the step's output** (twins_JK_count_step_5M_600.txt):
     - eleven clean bangs, with whole-board tops every 45 ticks from 23 to 473;
     - births per bang: 0, 64, 32, 0, 0, 0, 32 (twin pairs, the up twin fitted), 0, 0, 0, 32 (twin pairs, the down twin fitted);
     - at the bottom of tick 494 the push carries the stretch near the horizon within three ticks (X = 2,786,265,930 at tick 497), and the board splits;
     - steps then carry hundreds of dial turns (the carries read run from -445 to 813), and tick 554 is refused;
     - the rewind is 20 of 20 from tick 40, and the end teeth's fallback acts 24 times, all after tick 494.
   - **The stage-1 threshold** (twins_JK_threshold_5M_600.txt):
     - 600 ticks, twelve whole-board tops to 481, the rewind 20 of 20;
     - births 206, the twin pairs at the 3rd and 9th bangs;
     - after tick 481 the board scatters past the horizon (births at X near 10^13), and the end teeth's fallback acts 4,436 times.

   CHECKED. So the twin hands bring births at later bangs on the lawful T, as the A1 calibre never does, until the push at a bottom carries a step past one turn of the dial.

## 3. What it means for the plan

- **The twin hands in the one big bang do not run by the laws** on the synchronous board (the plan's section 11 (e), "Decided: the twin train goes into the one big bang's calibre").
  - At 500,000 quanta the trouble starts after the third top, and at 5,000,000 after the eleventh bang.
  - The local contractions, or a push at a bottom, then move a clock's stretch by many turns of its dial in one tick. Law 11's count lets the stretch leave the dial, and the course is refused.
  - Every twin run that survives 600 ticks stands on the end teeth's fallback.
- **What is missing is one thing:** a step that moves a clock's stretch by at most one turn of its dial per tick. Two candidates, neither mine to derive:
  - **David's asynchronous board** (DAVID-TENSOR24-THE-LOCAL-TICK.md, toys-5 ac22caa8). A Node-clock whose Mesh rate rounds to 0 has no tick, so its stretch cannot run past the horizon. This is Sofer's "no tick" reading as the local tick's own arithmetic (6469384921, item 5).
  - **The light cone's carry for F2** (David's), on which the A1 course already stands.
- **Law 4's top as the time gear's carry:** Sofer's shape holds on the A1 course read at the tick's start, bit for bit. On the twin calibre the bottom's borrow needs the step's output, and there the top's even counts let the course out. So "the top and the bottom one act" waits on the one-turn step.
- **Law 10 on the twin calibre:**
  - At 5,000,000 quanta, on the count form and with no bound acting, the twin pairs are born at the 7th and the 11th bangs. The A1 calibre has no birth after the 3rd bang, so the twins bring later births by the laws.
  - But the bangs between show none (births 0, 64, 32, 0, 0, 0, 32, 0, 0, 0, 32), so row 46 still fails bang by bang.
  - At 500,000 quanta the births after the third top (64 by tick 300, then 80, 96, 116, 124 and 134 at ticks 400 to 600) stand on the end teeth's fallback, so they show nothing for law 10.
- **Law 11's list:** the end teeth's fallback is load-bearing for the twin calibre, as F2 is for the course. Struck, the twin course is refused (the count rows of the table).

## 4. The 24's ladder under Pauli's rule (ladder_pauli.py, pure integers)

David's rule (DAVID-TENSOR24-THE-COMPOSITE.md, toys-5 cfadfecdd): two equal quanta, one train and one sense, stand as u x v + e v x u, with e the kind's sign. So they fuse only into their kind's own part: Sym^2 on the 24's five kinds (e = +1) and Alt^2 on the three spinor kinds (e = -1).

- **The squares:**
  - Sym^2 + Alt^2 = K x K on all eight kinds, with 0 lost.
  - A1 lies in Sym^2 on the 24's kinds and in Alt^2 on the spinor kinds.
  - Two equal twins fuse into A1 alone. Two equal T1 fuse into A1 + E + T2, two equal E into A1 + E, and two equal G3/2 into A1 + E + T2.
- **The ladders from {A1, E1/2}:**

  | the pairs of one kind | bang 1 | bang 2 | bang 3 | bang 4 |
  |---|---|---|---|---|
  | all equal (one train and one sense per kind) | A1, E1/2 | the same | the same | the same: no bang shows more |
  | the first rung's twin pair unequal (the fitting's quantum and antiquantum), every later pair equal | A1, E1/2 | + T1 | + E, T2, G3/2 | + A2, E5/2: all eight |
  | every pair whole (the table's reach) | the same as the row above | | | |

- **A mutant:** with the exchange sign read backwards, two equal twins make T1 and the ladder climbs where the law's stays at two kinds. It fails.
- **So the ladder climbs only through the fitting's unequal pair.** Once T1 stands, Pauli's rule cuts nothing the table needs, and the eight stand at bang 4 as before. CHECKED.
- **The ladder as a toy proves the kinds per bang, not the counts.** How many fusions a bang makes is an engine's to measure, after the one-turn step above.

## 5. The composite clock's click, in clock words (for the plan's law 6; the owner, 13:11: "The click that joins two clocks into a composite clock? Is there such a thing?")

Yes. It is law 6, the click of a split, on two clocks read as one dial. It is no third kind of click.

1. **Two clocks at one Node-clock make one joint dial.** Each hand is a pair of gears turning at its own beat. Read together, their gears' products (u x v) turn at the product of their turns, so the joint dial's beat is the sum of their beats.
2. **The 24 split the joint dial into kinds.** For two twin hands the joint dial is:
   - one gear that turns as A1, the determinant det[u, v] (the singlet);
   - three gears that turn as a vector, T1.

   Their sizes fill the dial exactly: N(det[u, v]) + (2 rho_u rho_v - N(det[u, v])) = 2 rho_u rho_v (Lagrange).
3. **The click.**
   - When the joint dial completes a whole winding, the composite's own carry at the parts' beats added (Sofer's condition (a)), the click of a split draws which kind takes the whole winding.
   - The shares are the kinds' sizes, and the draw is the one draw: the composite is the detector of its parts (Sofer's condition (b)).
   - A split into k kinds is k - 1 nested two-way splits (Sofer's condition (c)).
4. **After the click the pair is one clock of the drawn kind.**
   - Its gears are C_K on the parts' gears: one Gaussian for A1, three for T1 (David).
   - Its pair is the product of the parts' pairs on den^2, so the rest beats add.
   - Its unit is the product of the parts' units, so one quantum of each makes one composite.
   - The write is exact as a density, the pair's two-point reading. As an amplitude it needs a root (David: OPEN).
5. **Pauli inside it.** Two equal quanta can only make their kind's own part: two equal twins make the singlet alone. The vector clock comes from unequal quanta, the fitting's quantum and antiquantum.
6. **A big law above it, for the owner's list** (his 13:21 word: every draft asks whether a beautiful big law is missing above it): **every meeting of clocks is one joint dial that the 24 split into kinds, and the click draws one kind.**
   - It holds three of the plan's acts as one:
     - the composite clock (open item 11 c);
     - the singlet of the Bell pair, the A1 composite of the fitting's two ends;
     - Pauli's click law, as the equal quanta's joint dial.
   - What it does not give is the exchange sign e of equal quanta. That stays law 7's premise, which draft J derives from the clocks.
   - The toy shows the clock fact J's turnover route reads: T T = J J is the kind's sign on the board, with the rewind exact through T applied q times.
7. **OPEN, with David's page:**
   - the binding, since the beats add with no binding energy;
   - the wind's books for heavy parts, since the wind does not add (David's correction);
   - the unfusing and the rewind of a fusion;
   - the kinds of multiplicity above one;
   - where a pair's four gears go when the draw takes a kind of one or three gears (Sofer's condition (d), line 98).

---
Animate, reader-5.
