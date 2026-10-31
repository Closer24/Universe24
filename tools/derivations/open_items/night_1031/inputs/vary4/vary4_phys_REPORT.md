# The hostile physicist (THIRD pair) on VARY4 (the varied lay, fourth text), 2026-10-31, 08:1x to 08:5x UTC

(Written by the Boss from the reader's hand-back at 08:4x UTC, the reader's harness refusing the write; the text is
the reader's, word for word.)

The harness here refuses report-file writes from a subagent ("return findings as text"), so the whole report is below; S/vary4_phys/REPORT.md was not written. Everything I ran is in S/vary4_phys/.

What I read:
- VARY4.md whole: 542 lines. Its sha256 7847ffcd26c6a534... matches, and every sum in FROZEN.sha256 checks.
- probe_vary4.py's output and probe_split.py.
- My VARY3 report with the Boss's 07:2x answers.
- The mathematician's VARY3 report.
- The brief's last three sections (07:1x, 07:5x, 07:5x second part).
- MIRACLE_A section 7.

What I ran (one process at a time, nice 19, python -I -B, the load read before each run):
- **The rerun, from a copy only.** The frozen folder was copied to vary4_phys/copy. I reran its probe_split.py on L1 with S/vary4/all/src, read only, and no byte-code written. Output rr/split_L1_200.json, which is byte for byte r1/split_L1_200.json.
- **My own probe, amp_nohold.py.** It runs node-all's act and records each train's largest |count| every 25 rounds, over 400 rounds, on three lay-and-world pairs:
  - rr/amp_nohold_L1_400.json and rr/amp_nohold_L0_400.json (VARY3's world_nohold, read only);
  - rr/amp_tieon_L1_400.json (VARY3's world/).
- Whole numbers only.

VERDICT on VARY4: NOT PASSED

What is met:
- B1 of VARY3 is folded in both readers' words.
- The residual is measured on node-all and split exactly, 2M = St + Res, with 0 off.
- The minors are met.
- The varied lay stands as an initialization.

Two items block:
- **B1:** the open book in the clicks is not named as what it is. The folded m1 gives it to "the booking form", and VARY4's own section 2.4 shows otherwise. This sentence was mine in VARY3; I correct it here.
- **B2:** the new "bounded is not within the teeth" correction is drawn from a world whose counts run away.

Each fix is one paragraph.

## BLOCKING

**B1. The open book in the clicks is named wrongly.**

Where: section 3, m1; and the status row "the books in the click world".

What the text says:
- "So the miss belongs to the booking form, the act's two-train passing read on a four-leg monomial. It does not belong to the board's own energy."
- "The difference goes nowhere on the board."

VARY4's own section 2.4 contradicts this:
- **One residual under two bookings.** VARY4 states "the residual is one on both codes". The head's per-train passing and node-all's edge split are two different bookings, and they read one residual.
- **D is the act's own work.** D is the part of the act's own explicit work on the four-leg tie, J_i(a)(a+ - b), that is no difference of any function of the counts.
- **D is the head's form exactly (DERIVED, term by term).** I checked the algebra. Summing VARY4's D_i over a monomial's terms gives -f [e1(a+; a) - e1(a; a+) + e1(a; b) - e1(b; a)]. That is exactly the head's -f(e1 - e3) over the two windows (a, b) and (a+, a).
- **Only a change of the act's step removes it.** MIRACLE_A section 7 says the same: the residual goes only if the act's force changes to the polarized gradient (road A). No booking removes it.

So the miss is the act's, not the booking's. The bookings only show it (the head) or hide it in each clock's middle (node-all). My VARY3 m1 sentence was wrong, and VARY4's 2.4 overturns it.

The text's phrase "the record books quanta its teeth do not hold" is a board phrase. In the click world, the open book is this:
- The head's record holds more takes than gives: +63,945 at round 4932.
- At 4,821 of 5,000 round ends the excess is past the 134 quanta that any teeth could hold in flight.
- So it reads as quanta taken that no clock gave: no conservation of quanta on the head's record.

On node-all's record the same residual is in no click at all, since the record closes per edge by construction. Neither code's click world shows it as what it is.

**Fix.** Restate m1 and its status row:
- "The open book in the clicks is the act's four-leg residual seen in the head's record: quanta taken that no clock gave, past any 134 in flight at 4,821 of 5,000 round ends (peak +63,945)."
- "It is the act's own: the part of its explicit work on the tie that is no difference of the counts (2.4: DERIVED identical to the head's form; MEASURED at the peaks)."
- "The clicks push nothing back into the gears. No booking makes it or removes it; node-all's record hides it per edge; only a change of the step on the quartic removes it (road A, under its pair)."
- "Whether it is an energy's drift: Theorem A (cited, not passed) says no exact energy exists to drift."

**B2. Section 2.5's correction rests on a runaway.**

Where: section 2.5, "My own correction"; the headline "bounded by the counts is not within the teeth"; section 2.7, "the like shares pass the teeth at hold 0"; section 5 (c).

I measured node-all (VARY4's tree) on world_nohold, 400 rounds, both lays.

| round | L1 hold 0: giver, taker | L0 hold 0: giver, taker |
|---|---|---|
| 0 to 75 | 40, 0 | 40, 0 |
| 100 | 40, 22 | 40, 22 |
| 200 | 90, 122 | 83, 122 |
| 300 | 364, 395 | 351, 381 |
| 400 | 1,351, 1,324 | 1,310, 1,285 |

- From round 300 the pair grows by about 1.38 times every 25 rounds (1,351 / 981 = 1.377).
- This is the hands' tie's open direction with the held tie off. MIRACLE_A says V_d is indefinite where 2c|k|^2 < tie; that is STOP1's case.
- So "passes the teeth at every giver and taker clock from round 105, with no promise departure (the counts within the width)" reads the onset of the runaway. The taker leaves 0 at about round 100.
- A width of 128 bits is no bound on the swing.

The general point is true, and VARY4 already holds its evidence on a confined world.
- On L1 with the tie on, over 400 rounds (MEASURED here): the giver's largest count stays between 10 and 40, the taker stays at 0, and the held hand's wanders from 1 to 12.
- There the state part reaches 213 edge keys at the giver (VARY4's own 2.4).

**Fix:**
- Name hold 0 as the open direction's world.
- Draw "bounded is not within the teeth" from L1 with the tie on.
- Drop the hold-0 shares as evidence in 2.7 and in section 5 (c).

## MINOR

- **n1. Board quantities called energy and read as a clock's energy in the click world.**
  - Where: section 5 (b), "the state part booked by the energy"; (c), "each clock's stored share of the energy (road A's V_d) within its teeth"; line 53; 2.6, "less its share of the energy's change"; 2.5, "leaves half its energy's change at each end"; 2.2, "the polarized energy" and "staggered energy"; m1, "the board's own energy".
  - G and V_d are polarized forms of the counts, which are clock facts. A clock's share of them is David's convention.
  - Fix: name them so, and keep "energy" for what the decoder reads in the clicks. The header's own rule ("never as one clock's energy") asks for this.
- **n2. A board check that is not named as one.** The reading that can fail (own work against key_e N_t, read from a clock's lines) sets clicks against the board's work. By the 07:5x ruling that is "a board check beside a click reading until a click-only form exists". Name it so.
- **n3. "The place's books" on node-all.** By 07:5x this is the place identity (DERIVED): no reading of conservation, never printed beside the books. Rename it in m3 (ii) and in the 2.3 table.
- **n4. A giver named by its card in a click reading.** Section 2.3, round 1, says "the held hand books +5 quanta and the giver -5". That breaks the header's own rule and the Boss's answer 2. Use the train's index or the edge's side order.
- **n5. "So the residual is one on both codes (MEASURED)".** It is DERIVED as an identity term by term, on a shared board (my per-round digests, L1). It is MEASURED only at the two peaks. Say so.
- **n6. "The same up to a bounded difference (DERIVED)" in 2.6.** That difference is bounded only where the counts are (B2).

## Each item met

- **VARY3's B1 (both readers): MET.** Section 1, in the readers' words:
  - by construction, and not the residual booked;
  - the 1/3 and 2/3 share;
  - the reading that can fail, failing;
  - OPEN on the edge form, with two roads.
- **Phys m1:** met in the letter, wrong in one sentence (see B1).
- **Phys m2 to m5: MET.**
  - m2, "no choice": restated as M5.
  - m3, the two clocks: named apart.
  - m4: the 10,240-round floor.
  - m5: "metric" in node-all's file too.
- **Math M1 to M6: MET.**
- **The Boss's answers 1 to 6: folded.**

## SOUND

- **The rerun.** probe_split on L1, from my copy, is byte for byte r1. The identities hold at 0 off: 2W = 2G(n) - 2G(n-1) + D, Lmap[W] = O - B, and 2M = St + Res.
- **The 1 : 2 share.** It is exact on L1: 12,810,960,000 and 25,621,920,000, my VARY3 numbers.
- **The residual at a place equals the head's miss to the unit:**
  - L1: 10,023,720,000 at site 17, round 170;
  - L0: 708,840,000 at site 0, round 150.
- **Round 1 on L0.** The giver's own work is 0 at all 27 Node-clocks, yet its M is 768,000,000, which is the state part.
- **The giver's peak splits** as 213 edge keys of state part and 131 of residual share, of opposite signs.
- **The fourth merge** reads byte for byte on both lays.
- **Withdrawals.** "Only the split's edge books close it" and the hold-0 "reading that could fail passes" are both withdrawn.
- **The varied lay** stands as an initialization. Its six steps before a writer are an honest list; step 5, the 24 on node-all with the lay in the files, is owed and named.

## DERIVED / MEASURED / OVERCLAIMED

- **DERIVED:**
  - the share by legs;
  - 2W = 2dG + D;
  - D = 0 on two-leg monomials;
  - (mine) D is term by term the head's -f(e1 - e3).
- **MEASURED:**
  - sections 2.3, 2.4 and 2.5 as run;
  - (mine) the rerun, byte for byte;
  - (mine) the runaway at hold 0 on both lays;
  - (mine) bounded counts on L1 with the tie on.
- **OVERCLAIMED:**
  - "the miss belongs to the booking form"; "goes nowhere on the board" (B1);
  - "bounded by the counts", read on a runaway (B2);
  - "one residual (MEASURED)": DERIVED, with only the peaks measured (n5).

## The Boss's ruling, (b) with (c), weighed

You asked whether this is the right physics of the books in the click world, where each clock's booked total is read from its own lines.

**What the click world reads.** From a clock's own lines, plus its sides' teeth that the 1.4 record writes, the click world reads its swept passing exactly: key_e N_t + the change of its teeth = B_t (Rule3). That is the clock's book in the click world.
- It closes against its partners at every meeting by construction. That is a code check, the record's faithfulness (07:5x).
- A clock's own work and the coupling's form are board quantities. Any reading that sets them against the lines is a board check beside a click reading.

**(a) withdrawn: right.** M_t holds the coupling's stored form, which is held in the counts. Reading it against the teeth books stored as unbooked.

**(b): right, with two amendments.**
1. **Booking can only mean removal, or reading by name.** The residual is the act's own (B1). So "booked" can only mean removed (road A, then identically 0, a check by construction named so), or read by name. Putting it into any cell, tooth or store would hide a drift that runs to 18,870 keys at one Node-clock in 5,000 ticks. That is a check that cannot fail.
2. **State it free of convention.** State it as the residual at the place, Sum_i D_i per monomial, not as a clock's share. The share l_t/L is David's convention; only the place's total is the act's.

**(c): not the physics of the books.**
1. **Under the exact step, (c) is (a) to the unit.** With Res identically 0, VARY4's identity 2M = St + Res gives M_t = St_t / 2, the clock's running stored share. MIRACLE_A section 7 says the same: own work = booked + the change of its leg share of V_d. So the reason given for withdrawing (a) applies to (c) word for word. And today, |M| <= |St|/2 + |Res|/2: "(b) with (c)" is (a) split into two halves.
2. **The stored share is the pair's, not the clock's.** It is the coupling's form between the pair: the edge's, by the Boss's own answer 2. It is held in the counts, in no tooth. Only David's convention gives it to the clocks. VARY4's round 1 on L0 shows the consequence: the giver's counts stand, yet its stored share changes by 5 edge keys, past its teeth, because the held hand moved the pair's form. A reading that fails at a clock that did not move measures the convention, not the clock.
3. **Its size against the teeth is a resolution fact.** Its size against 4 edge keys is the key's grain against the coupling's swing. No number may be moved to make it pass, so it can be named but never acted on.
4. **It puts board energy into the click world.** It reads a board function, as energy, into a clock's click teeth: exactly the second press.

**Counting the stored share as stored** (MIRACLE_A's first OPEN, answered yes):
- Each clock's lines book its own work less its legs' share of the form's change.
- Under an exact step that is an identity, so the books can fail only through (b).
- An energy law in the click world must come from the clicks alone (OWED, 07:5x).

## Questions for the Boss

1. Under an exact step, (c) is (a) to the unit. Keep (c) as the reading that can fail? Or name it a resolution reading (the key's grain against the coupling's swing) with no verdict on the books, and answer MIRACLE_A's first OPEN (the stored share counted as stored)?
2. Is the coupling's form the pair's, held on the edge as a store? That would be an element for the owner's batch, like the per-triangle tooth with its own now and before. Or is it split between the clocks by David's legs? (c)'s verdict depends on that convention.
3. The hold-0 world runs away. Should "the like shares pass the teeth on today's act" be cited only from a confined world (the tie on), with hold 0 named STOP1's open direction?

## Solution24 (the reader's line)

VARY4 measures the residual exactly and shows it is one residual on both codes. That is the proof that the residual is the act's, not any booking's, so the text must name it so. A clock's book in the click world is its own lines. That book closes by construction. Its one law is that the residual must go, which only an exact step does. The stored share belongs to the pair, not to a clock's teeth.
