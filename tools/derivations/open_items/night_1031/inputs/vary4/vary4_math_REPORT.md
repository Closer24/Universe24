# The hostile mathematician (THIRD pair) on VARY4 (the varied lay, fourth text), 2026-10-31

(Written by the Boss from the reader's hand-back at 08:3x UTC, the reader's harness refusing the write; the text is
the reader's, word for word.)

The harness refuses report files from this reader, as it did on VARY3, so the whole report is here.

**What I read**
- VARY4.md, whole: 542 lines, sha256 7847ffcd26c6a534...; all 16 files in FROZEN.sha256 check OK.
- probe_vary4.py, probe_split.py, and the frozen records r1/ and r2/.
- My VARY3 report as written (M1 to M6), and the physicist's VARY3 report with the Boss's answers 1 to 6.
- The last three sections of BRIEF_PAIRS.md.
- ALG1 3.2 to 3.5 and MIRACLE_A only where VARY4 cites them; I do not lean on either.

**What I ran** (in S/vary4_math/, one process at a time, nice 19, python3 -I -B, load read before each)
- S/vary4/all/src is 4ce1aa9d7's src and S/vary4/all4/src is 9d75a4904's: diff -r against my own git archives. Neither tree was written.
- copy/ holds both probes copied from the frozen folder. My rerun of probe_split.py on L1, 200 rounds, under Python 3.13 (the text ran 3.14.6), gives copy/r/split_L1_200.json byte for byte the frozen r1/split_L1_200.json. That includes the place residual 10,023,720,000 at site 17, round 170.
- probe_ref.py is mine. It recomputes VARY4's split beside one whose reference energy is normalized to the potential, G' = (2/k) G, on L1 for 200 rounds; output in ref_L1_200.txt.

## VERDICT on VARY4: NOT PASSED

There is one BLOCKING item. The split 2M = St + Res is exact, but the residual it names depends on the reference energy chosen, and VARY4's reference counts the four-leg tie's energy twice. So most of what VARY4 calls the residual's share at its peak is stored energy, a function of the counts.

Everything else is sound or a one-line minor:
- the floors;
- the head-miss equality;
- D = 0 for two legs, as a monomial's sum;
- the fold of VARY3's B1 and of every minor of both readers.

## BLOCKING

**B1. The split's residual depends on its reference, and VARY4's reference counts the quartic's energy twice.**

Places: the verdict's "New, MEASURED"; 2.2 "The split in two"; 2.4 ("the non-telescoping part of node-all's edged work at a place is the head's NC29 residual"); 2.6 and 2.7 ("the same up to a bounded difference"); section 5 (b); status rows 10 and 14.

**The identity carries no content of its own.**
- 2M = St + Res is exact and DERIVED, but it holds by definition:
  - D is defined as 2W - 2DeltaG;
  - Lmap is linear;
  - G telescopes, because round r+1's window (b, a) is round r's (a, a+).
- Its three checks, 0 off (I recomputed: 0 of 27,000 clock-rounds on L1), cannot fail except by a code slip.
- All the content lies in the choice of G.

**What VARY4's G does to a four-leg monomial.**
- VARY4's per-term 2G = T(a+; a) + T(a; a+). Summed over a k-leg monomial at rest, this is -2kH (Euler), so the potential is counted k/2 times relative to the work.
- To first order in the counts' step v (b = x - v, a+ = x + v):
  - 2W = -4 f v.P;
  - 2DeltaG = -2k f v.P;
  - so D = 2(k - 2) f v.P.
- For two legs that is 0, which is sound.
- For the tie (k = 4), D = -DeltaG at first order. That is a difference of a function of the counts, not "the part that is no difference".

**The reference that matches the work.** G' = (2/k) G matches the work at first order for every k:
- it is -2H at rest for every monomial;
- the two-leg staggered energy is unchanged;
- D' = O(v^2).

It is a reading's choice and puts no number into the act.

**MEASURED** (probe_ref.py, L1, 200 rounds; at the text's own peak these numbers are also exact from its frozen M and St):

| | VARY4's G | G' = (2/k) G |
| --- | --- | --- |
| the place's residual at kappa 1, largest | 10,023,720,000 (site 17, round 170; 65 edge keys) | 3,294,480,000 (site 17, round 163; 21) |
| the place's residual at site 17, round 170 | 10,023,720,000 | 1,879,980,000 |
| the residual's share at a clock, largest | 20,047,440,000: 131 edge keys (giver, site 17, round 170) | 6,588,960,000: 43 (giver, site 17, round 163) |
| the giver's residual share at site 17, round 170 | 20,047,440,000 | 3,759,960,000 |
| the state part at a clock, largest | -32,574,960,000: 213 (giver, site 17, round 170) | -16,287,480,000: 106 (same clock) |
| clocks whose residual's share passes 4 edge keys; first round | held 15, giver 27 (42 of 54); rounds 8 and 3 | held 7, giver 20 (27 of 54); rounds 21 and 9 |

**What this means.**
- At the text's own peak, four fifths of its residual's share is the tie's stored energy. Across all clocks the largest share falls from 131 to 43 edge keys.
- "Both parts pass the teeth on their own; they partly cancel in M" (2.4) is the symptom.
- What stands under either reference: the residual's share still passes the teeth within 200 rounds, at 27 of 54 clocks under G'.
- My own derivation was overturned in part: at first order D' vanishes, but on this lay the counts' steps are large, and D' keeps a third of D at its peak.

**What does not depend on the reference** (DERIVED here):
- **(i) Two legs:** the reference with D == 0 is unique up to a constant.
- **(ii) Three legs or more:** no function of the window's counts makes a monomial's work an exact difference.
  - Such an F would force g(a, b) - g(b, a) = c(b) - c(a), with g(a, c) = -f e1(c; a).
  - With every leg row at one value, this reads -f k (b a^(k-1) - a b^(k-1)) = c(b) - c(a).
  - Setting a = 0 makes c constant, which is false for k >= 3. The tie's repeated leg changes nothing.
- **(iii)** The place identity with the head (m3).

The residual's size, its clock counts and its first rounds all depend on the reference.

**The head's books inherit this.** VARY3's "the books' miss is the tie's four-leg residual" is the same D (m3). So the head's place miss swings first with the tie's energy at the counts, and only its second-order part is no difference.

**Fix:**
- name G as a choice for the tie;
- give the split under G' (the numbers above), or under both references;
- restate "the part that is no difference" and 2.4's "non-telescoping part" as D's class: no reference makes it 0, and its size depends on the reference;
- say that the head's miss carries the same first-order part.

## MINOR

**m1. The hold-0 numbers are in another key, and the text does not say so** (2.5 and its status row).
- With hold 0 the tie's monomials are dead, so kappa is 2 and the edge key is the file's 50,811,429. The frozen nohold records say so: "kappa" 2, "edged terms" 12, "edge key" 50,811,429.
- So "40 and 37 edge keys" are in that key. In the world's 152,434,287 they are 13 and 12, still past 4.
- A strength set to 0 moves the edge key, through edging's lit(factor) (MIN1's (c)).
- Fix: say so, and state the teeth there as 4 x 50,811,429.

**m2. "D is 0 for every two-leg monomial" holds for the monomial's sum, not per term** (2.2, 2.5).
- A two-leg term's own D_i is -f (a+_p a_q - a_p a+_q + a_p b_q - b_p a_q), which is not 0.
- The clocks' shares see only the monomial's total: Lmap gives each clock kappa (l_t / L) of it, by 2.2's own derivation. So the conclusion stands; fix the phrase.

**m3. The head-miss equality is DERIVED, with the measurement as its check** (2.4, "So the residual is one on both codes (MEASURED)").
- The head's place residual over the windows (a, b) and (a+, a) is SUM_i [T_i(a; b) - T_i(b; a)] + [T_i(a+; a) - T_i(a; a+)] = SUM_i D_i, term by term.
- So on the same board (the physicist's chained digest, cited) the two are equal to the unit by construction. It is one expression on both codes, carrying B1's first-order part.
- Reproduced: 10,023,720,000 in my rerun; 708,840,000 in the frozen L0 record against VARY3's world_L0.json.

**m4. 2.6 and section 5 (c) disagree on what can fail after an exact step.** 2.6 says "the energy's bound, a board fact"; 2.7 and (c) take MIRACLE_A's "each clock's stored share within its teeth". Reconcile them (see the ruling below).

**m5. "The same up to a bounded difference"** (2.6, 2.7) misses the text's own 2.5 lesson that bounded is not within the teeth. Here the bounded difference is most of the residual's share (B1).

## The four press points

1. **The identity 2M = St + Res:** DERIVED, exact, and true by definition (B1).
2. **D = 0 for two legs:** DERIVED for the monomial's sum, with its reference unique up to a constant (B1 (i)); not 0 per term (m2).
3. **The head-miss equality to the unit:** DERIVED as the same expression, and checked on both lays (m3). It pins one expression, not a non-telescoping part (B1).
4. **The floors: SOUND.**
   - **M1:** the floor (320 rounds, 200 landings) makes every 200-round NOT READ DERIVED, node-all's included. Only the 5,000-tick NOT READ is MEASURED (longest stretch 74 rounds with 2 landings; most landings 9 in 70 rounds).
   - **M2,** at L0's own rate p = 7/200:
     - five expected landings need w >= 143;
     - the gate takes w as the largest power of 2 with 20 windows a half, and 128 gives only 4.48 expected landings, so w = 256 and a half needs H >= 5,120;
     - so the record needs 10,240 rounds after T0 = 0, past the world's 5,000 ticks;
     - the other parts of the gate are weaker: 100 landings a half need about 2,858 rounds, and E2 >= 3,000 needs about 2,450;
     - this is DERIVED if the rate holds and the sides stay single and one-way (two-way sides are not read at all).

## The Boss's ruling, (b) with (c), weighed

**(a) withdrawn: SOUND.** M_t = St_t/2 + Res_t/2 exactly, so (a) cannot tell a residual from stored energy. At hold 0, Res == 0 (DERIVED: D_m = 0 on every two-leg monomial), and (a) still fails at 40 hold-0 edge keys.

**(b): SOUND as the books' requirement.**
- "Identically 0 under an exact step, a check by construction then, named so" is right: an exact step makes the work a difference of its own energy.
- Read on today's act, (b) must name its reference (B1). Under G' it fails at 27 of 54 clocks on L1 within 200 rounds, from round 9: still a failure, a third the size at the peak.

**(c): not sound as worded, as the books' reading that can fail.**
- Under an exact step Res == 0, so M_t = St_t/2, and (c) is (a) word for word.
- The ground given for withdrawing (a), "it books stored energy as unbooked work, and fails with no residual", then fits (c) too. MEASURED at hold 0, where Res == 0: (c) = (a) = 40 hold-0 edge keys at the giver, site 8, round 200.
- ALG1 3.3, cited as agreeing, actually says the two-leg books "hold exactly" once the coupling's energy E is read off the board, with no tooth and no new element. That treats the stored share as the coupling's energy, a function of the counts, not as something the teeth must hold.
- What (c) actually reads: whether the record's teeth, at the key's grain, can resolve each clock's share of the coupling's energy. That compares the file's key with the energy's swing at the lay's counts: an initialization fact. The key is the owner's, and no key moves.
- Meeting (c) would take either:
  - a coarser key or weaker strengths, which is a number picked for an outcome and forbidden; or
  - a store for the coupling's energy, a new element for the owner's batch (ALG1 3.5's tie cell, which ALG1 itself does not offer as a closure).
- So (c) cannot gate a turn.

**Proposed:**
- (b) is the books' reading, holding by construction under an exact step, and named so.
- The stored share is read as the coupling's energy at the counts (ALG1 3.3).
- After an exact step, the reading that can fail is the energy's bound, a board fact (STOP1's), as VARY4 2.6 says.
- (c) is renamed "the record's legibility of the coupling's energy at the key's grain" and goes to the owner with the key.

Beside all three: own work and stored energy are board quantities. Read against the record's teeth, they are board checks beside the record (the 07:5x second part), and should be named so.

## SOUND, with numbers

- **Frozen folder:** FROZEN.sha256 OK for all 16 files; the trees are their commits; my probe_split.py rerun on L1 is byte for byte.
- **VARY3's B1 folded honestly:**
  - "only the split's edge books close it" is withdrawn in both readers' words;
  - the checks by construction are named so, 0 off on both lays;
  - the reading that can fail is stated and fails: 82 edge keys on L1 (giver, site 17, round 170) and 19 on L0 (taker, site 0, round 155), as my VARY3 probe and the physicist's had.
- **The share by legs:**
  - Lmap[X]_t = kappa (l_t / L) X_m for a monomial on two trains, since kappa - w_t = w_u = kappa l_t / L (re-derived);
  - 2 M_held = M_giver at 5,400 of 5,400 places on L1 follows from it, the taker's counts being 0;
  - the end shares are 12,810,960,000 and 25,621,920,000 (84 and 168 edge keys);
  - kappa R at a Node-clock, -18,791,280,000, equals M_giver + M_held.
- **Round 1 on L0:** the giver's M = 4R = 768,000,000 with R = 192,000,000 (VARY3's round-1 S); that is 5 edge keys and 5,828,565.
- **9d75a4904:** its records are byte for byte 4ce1aa9d7's (equal frozen sums).
- **Minors folded:** my M3 to M6 and the physicist's m1 to m5, in the readers' words.
- **The edge key:** the act's units; no key moved within a world (but see m1).
- **The lay:** section 4 is honest about what remains.

## DERIVED / MEASURED / OVERCLAIMED

- **DERIVED:**
  - the identity (by definition);
  - the share by legs;
  - D_m = 0 for two legs, with its reference unique;
  - the place identity with the head;
  - the floors;
  - mine: D = 2(k - 2) f v.P at first order, and no exact reference for k >= 3.
- **MEASURED:**
  - the text's tables, with one rerun byte for byte;
  - mine: the split under G' (B1's table).
- **OVERCLAIMED:**
  - "D, the part over the two windows that is no difference", and "the non-telescoping part of node-all's edged work at a place is the head's NC29 residual" (B1);
  - the residual share's sizes and clock counts, read as if they did not depend on the reference (B1);
  - "the two codes carry one residual (MEASURED)": it is one expression, DERIVED (m3).

## Questions for the Boss

1. Should the books' readings take the reference normalized to the potential (G' = (2/k) G, -2H at rest for every monomial) as the residual's reference, so that the residual's first-order part, a function of the counts, goes to the state part?
2. Is (c) a gate for turns, or the record's legibility of the coupling's energy at the key's grain, which belongs to the owner with the key?
3. Should the head's 5,000-tick miss (18,870 keys at site 19; SUM q +63,945) be reread under G', to see how much of it is the tie's energy swing and how much drifts?

## Solution24 (the reader's line)

VARY4 folds VARY3's block honestly and finds a true identity, 2M = St + Res. But its reference counts the quartic's energy twice, so most of what it calls the residual at its peak is stored energy. Under the potential's normalization the residual is a third the size, and it still passes the teeth at 27 of 54 clocks. Only an exact step removes it; the stored share is the coupling's energy, to be read off the counts, not held in a clock's teeth.

**Files:** S/vary4_math/probe_ref.py, S/vary4_math/ref_L1_200.txt, S/vary4_math/copy/ (the probes copied, and r/split_L1_200.json, my rerun).
