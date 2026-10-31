<!-- Boss note, 2026-10-31 ~09:3x UTC: written by the Boss from the reader's hand-back (the harness refuses report files from readers); the text below is the reader's, whole. Reader of VARY5 (frozen 747442ca), the hostile physicist (the VARY pair's physicist). -->

# The hostile physicist (THIRD pair) on VARY5 (the varied lay, fifth text), 2026-10-31, 09:0x to 09:3x UTC

This harness refuses report-file writes from a subagent, so the whole report is below and S/vary5_phys/REPORT.md was not written. What I ran is in S/vary5_phys/.

**What I read:**
- VARY5.md whole: 443 lines, sha256 747442ca...7dde, which matches; every sum in FROZEN.sha256 checks.
- VARY5's three probes and its r/ outputs.
- My VARY4 report as the Boss wrote it.
- The brief's 08:1x, 08:3x, 08:4x and 08:5x sections.
- MIRACLE_A section 7.
- MIRACLE_B's physicist's report, B1 and B2.
- I did not open the other reader's folder.

**What I ran** (whole numbers, Python 3.14.6 and numpy 2.5.4 from the live venv, python -I -B, nice 19, one process at a time, the load read before each run, from a copy of the frozen folder in vary5_phys/copy):
- **The amp outputs.** VARY5's r/amp_nohold_L1_400.json, r/amp_nohold_L0_400.json and r/amp_tieon_L1_400.json are each byte for byte my vary4_phys/rr/ (checked by cmp).
- **probe_ref.py on L1.** rr/ref_L1_200.txt is line for line VARY5's r/ref_L1_200.txt.
- **My amp_nohold.py on world/ setting_shipped.json** (L0, tie on), 400 rounds: rr/amp_tieon_L0_400.json. This is new.

VERDICT on VARY5: NOT PASSED

What is met:
- My VARY4 B2 and all six of my VARY4 minors.
- My VARY4 B1, in my own words. But those words were incomplete, and VARY5's own section 1 shows it.

Two items block:
- **B1:** the text says road B removes the residual. MIRACLE_B's physicist and the 08:5x ruling say otherwise.
- **B2:** the open book in the clicks is named as wholly the act's own, against VARY5's own section 1 and the 08:3x ruling.

Each fix is one paragraph.

## BLOCKING

**B1. Road B is said to remove the residual. Its clicks still carry it.**

Where:
- section 2, "What moves it": "Only a change of the step on the quartic removes it: road A or road B, each under its pair";
- section 6, "Weighed": "By its derivation the tie's residual at the place is 0 there ... it goes only when the step on the quartic changes";
- section 8: "removed only by a different step: road A or road B ..., or David's split where it arises";
- the status row "miracle road B: cited, under its pair, not leaned on". Sections 2 and 8 do lean on it.

What MIRACLE_B's physicist found (his B1 (a) to (d)):
- **The clicks are today's passing.** bedge()'s clicks are step.passing, the act's two-leg passing, carried at the key. The exact exchange P is computed only in booked(), which is a reading.
- **So the residual stays in road B's clicks:** 225 keys at one clock on the pair world, and 2,545 keys on click1 over 5,000 rounds.
- **The 0-miss column is a check by construction.**
- **The stored share passes the teeth from round 1:** 457 and 3,930 keys at the held clock.
- **The form read is node-live's per-train tooth.** node-all's sides are never read.

What the 08:5x ruling says:
- "B-edge's clicks still carry the act's two-leg passing, so the residual is gone in the probe's books, not in the clicks, until term 11's passing is P; the books are read on node-all's edge form (the sides) or named OWED there."
- After the exact step, the reading that can fail on road B is "the physicist's walk of the held counts (MEASURED, no bound)".

What VARY5 does instead:
- It calls the 0 misses "MEASURED there".
- It cites MIRACLE_B's "the click world's counts within 7 bits over 5,000 rounds", and leaves out the walk:
  - the held |k|^2 is 8 to 49 times today's act's, reaching 900 by round 5,000;
  - the held clock's whole clicks per 250 rounds drift about 5,000-fold, so any within-record reading reads a drifting rate;
  - energy arrives at the held clock as the teeth's share, which no click books.

The physics:
- The clicks show what term 11's passing reads. Changing the step is not enough. With road B's step and today's passing, the record still books the explicit form's class, now on road B's counts.
- "David's split where it arises" is a booking. The 08:4x ruling says booking never means putting the residual into a store. The 08:3x ruling says only a different step can make the work an exact difference. So it is no removal road.

**Fix:**
- "The residual leaves the clicks only when the step on the quartic is exact and term 11's passing reads that step's own exchange."
- "On road B as built (B-edge) the clicks still carry the act's two-leg passing. So the residual is gone from its probe's books only, and 225 and 2,545 keys stay in its clicks (MIRACLE_B's physicist; 08:5x). Its 0 misses are a check by construction. Its books on node-all's sides are OWED."
- "After its step, the reading that can fail is the energy's bound. On road B that is the held counts' walk, with no bound, read beside today's act's walk."
- Drop "or David's split where it arises".

**B2. The open book in the clicks is named as wholly the act's own.**

Where:
- section 2, "What it is": "the act's four-leg residual seen in the head's record";
- section 2, "Whose it is": "the act's own: the class of its explicit work on the tie ..., DERIVED identical to the head's form";
- section 2, "What moves it": "no booking makes it or removes it";
- section 2, "booked": "a drift that runs to 18,870 keys";
- the status row "the open book in the clicks".

What VARY5's own section 1 says:
- The head's place miss is the sum of D_i under VARY4's reference G, term by term (1.5).
- Under G, D's first-order part for the tie is -dG: a difference of a function of the counts (1.2).
- "VARY3's head numbers swing first with the tie's form at the counts, and only D's class is no difference" (1.5).
- At site 17, round 170 on L1, the place's residual is 10,023,720,000 under G and 1,879,980,000 under G'. My rerun with Python 3.14 gives the same, line for line.
- The 08:3x ruling: read against G', "the residual's first-order part, a function of the counts, then goes to the state part".

DERIVED (mine; two lines):
- For the tie, k = 4, so G' = G/2 and 2dG' = dG.
- So D_G = 2W - 2dG = D' - 2dG' at every term.
- Summed over the rounds, the head's miss is SUM D' - 2(G'(now) - G'(start)).

So the open book in the head's record has two parts:
- **(i) The head's reference part, -2 delta G'.**
  - It is twice the tie's normalized form's change since the start: a function of the counts.
  - The head's two-window term 11 books it as quanta that no clock gave, because its built-in reference counts the tie's form twice.
  - At the L1 peak place it is 8,143,740,000 of 10,023,720,000, about four fifths.
  - It is a state part, booked as an open book.
- **(ii) The act's own class, SUM D'.** It is second order, and no reference removes it.

What follows:
- Only (ii) is the act's own.
- "No booking makes it or removes it" holds for (ii) only.
- "A drift that runs to 18,870 keys" is the head's number under G. How much of it is (ii) has not been reread: VARY5's own OPEN in 1.5.

**My own correction.** My VARY4 B1 fix words, which VARY5 adopts, named the whole open book the act's own. With the reference (VARY4's mathematician's B1, folded in VARY5 section 1), they hold for its class only. So my two earlier lines were each half right:
- VARY3 m1, "the miss belongs to the booking form", was wrong for the class and right for the first-order part.
- VARY4 B1 was the reverse.

**Fix** (section 2 and its status row):
- "The open book in the clicks is the head's record of the act's work on the tie, booked against the head's own two-window reference."
- "At first order it is the change of the tie's coupling form at the counts, about four fifths of the place's miss at the L1 peak place: a state part by the 08:3x ruling."
- "Beyond first order it is D's class, the act's own, which no reference or booking removes."
- "The clicks show both as quanta that no clock gave. Their split over the 5,000 ticks is OPEN (1.5)."
- Restate the 18,870 keys as the head's number under G.

## MINOR

- **m1. The record's teeth, 08:5x (section 3, "The click world's book of a clock is its own lines").** VARY5 quotes my VARY4 sentence "key_e N_t + the change of its teeth = B_t". The 08:5x ruling corrects it: the teeth are board fields, and the click world reads the lines and sides alone. So B_t recovered through the teeth is a board check. Restate: the click world's book of a clock is its sides' quanta, N_t. (This is my correction too.)
- **m2. A store offered (section 3, "Meeting it ... or a store for the coupling's form (a new element, the owner's batch)").** The 08:4x ruling says the stored form is the edge's, "with no store and no new element". Drop it.
- **m3. The ticks not named.** The 08:5x ruling says "every text that cites the click world's ticks names it". Sections 2 and 8 cite 5,000 ticks and round ends, but never name that the shipped click world runs 3,751 of its 5,000. Name it, and say the 5,000 are L1's: the varied lay, on the head, within the width.
- **m4. "The confined world" (1.4, 2, 3).**
  - For L0, MEASURED here over 400 rounds with the tie on: the giver stays within 30 to 40, the taker rises to 77 and falls back to 10, and the held hand sits at 0 or 1. So L0's counts are bounded in the window that is read. But L0 passes the width at round 3,752 (08:5x).
  - L1's bound is likewise only 400 rounds': its held count wanders from 1 to 12.
  - Write "bounded in the window read".
- **m5. The interpreter.** VARY5 ran Python 3.13.17, against 08:5x's rule of 3.14. My reruns with 3.14.6 reproduce probe_ref line for line and amp byte for byte, so it is harmless here. Name it.
- **m6.** MIRACLE_B's 0 misses are called "MEASURED there". By 08:5x they are a check by construction. This goes with B1's fix.

## My VARY4 items: met or not

- **B1 (the open book named wrongly): MET in my words** (section 2, the status row). The words were incomplete; see the new B2.
- **B2 (2.5 read on a runaway): MET.**
  - Section 4 names hold 0 the open direction's world (STOP1's) and cites its numbers for nothing.
  - It reruns my probe byte for byte (verified).
  - It draws "bounded is not within the teeth" from L1 with the tie on.
  - It adds the mathematician's point: kappa is 2 at hold 0, so the 40 and 37 edge keys are 13 and 12 in the world's key.
- **n1: MET.** The remaining "energy" words are the Boss's names, flagged as such in the header.
- **n2 to n6: MET.**
  - n2: the board check is named so.
  - n3: the place identity.
  - n4: the clocks are named by train index.
  - n5: DERIVED, MEASURED at the peaks.
  - n6: withdrawn along with m5.
- **My weighing of "(b) with (c)": folded as ruled at 08:4x.**
  - The residual is stated at the place.
  - "Booked" means removed or read by name.
  - The stored form is the edge's.
  - (c) is (a) under an exact step; (c) is renamed and gates no turn.
  - The exception is the store offer (m2).

## SOUND

- **The reference split reproduces** (my rerun, 3.14):
  - D is 10,023,720,000 against D' 1,879,980,000 at site 17, round 170;
  - D' is largest at 3,294,480,000, 21 edge keys;
  - Res'/4 is largest at 6,588,960,000, 43 edge keys;
  - St'/4 is largest at -16,287,480,000, 106 edge keys;
  - 2M = St + Res holds, 0 off.
- **1.2 checks:** Euler's sum x_i d_iV = kV; 2W = -4 v.gradV, 2dG = -2k v.gradV, so D = 2(k - 2) v.gradV; and D' is second order.
- **1.3 (ii) checks:**
  - setting a+ = b makes F symmetric;
  - so g(x, a) - g(a, x) = c(a) - c(x);
  - on the diagonal this needs x a^(k-1) = a x^(k-1), which is false for k >= 3.
- **probe_mono:** 6 two-leg and 24 four-leg monomials; the two-leg sums are 0 at every place and round; the two runs agree.
- **The rulings folded:** section 4's runaway table is mine; "booked" is restated; (c) is renamed; after an exact step, the reading that can fail is the energy's bound.

## DERIVED / MEASURED / OVERCLAIMED

- **DERIVED:**
  - 1.2 and 1.3;
  - (mine) D_G = D' - 2dG' for k = 4, at every term;
  - (mine) the open book's two parts.
- **MEASURED:**
  - VARY5's tables;
  - (mine) the 3.14 rerun;
  - (mine) L0 with the tie on, bounded over 400 rounds.
- **OVERCLAIMED:**
  - "road A or road B" removes it; "the residual is 0 there"; "or David's split where it arises" (B1);
  - "the open book ... is the act's own: the class"; "a drift that runs to 18,870 keys" (B2);
  - the 0 misses as "MEASURED" (m6).

## Questions for the Boss

1. Should the open book in the clicks be reported in two parts: the head's reference's first-order part (a state part, by 08:3x) and the act's class? And should the 5,000-tick split under G' be read before the open book is cited as no conservation in the clicks?
2. Road B: does "removed" need both conditions, the step exact and term 11's passing reading that step's exchange? And are its books OWED on node-all's sides until then?
3. On a bounded world, should the class's running sum at a place be read by name for growth over the world's own ticks? That is what tells a secular drift from a bounded wander; a class that is not 0 says neither.

## Solution24 (the reader's line)

VARY5 folds the runaway and the minors cleanly. Its reference shows what the open book is: the head's two-window term 11 books the tie's coupling form at the counts as quanta that no clock gave, and only a second-order class is the act's own. That class leaves the clicks only when the step is exact and term 11 reads that step's own exchange. Road B, so far, removes it from its probe's books, not from its clicks.
