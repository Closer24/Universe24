<!-- Boss note, 2026-10-31 10:23 UTC: written by the Boss from the reader's hand-back (the harness refuses report files from readers); the text below is the reader's, whole. Reader of ALG3 (frozen 0e308f17), the hostile mathematician (the ALG pair's mathematician). -->

# The hostile mathematician on ALG3 (what is still open, read through the coupling complex), 2026-10-31

(The harness refuses report files from subagents, so here is the whole report for S/alg3_math/REPORT.md. ASCII only.)

**What I read**
- ALG3.md whole: 475 lines, sha256 0e308f17...; all 100 sums in FROZEN.sha256 check OK.
- Against: my ALG2 report, and the brief to its end (931 lines: 09:22 to 10:13 UTC, with the owner's words of 09:30 to 10:11 UTC).

**How I ran** (all in S/alg3_math/; the live venv's Python 3.14.6, -I, nice 19, one process at a time, the load 2.3 to 3.2 at every start; nothing in the repository touched beyond read-only git show and git archive):
- The tree: `git archive 9d75a4904 src examples` has sha256 91a5ebd6..., as stated. The frozen all/ equals that archive file for file, apart from __pycache__ folders.
- Reruns from copy/ (a copy of the frozen folder), all byte-identical to out/:
  - david_click_L0_200;
  - circ on L0, L1, the swap lay and the mesh ring;
  - compare on the swap lay;
  - member on L0 and L1, with Big Pic's circ.py from ed6a1f225 (by git show; sha256 a12ce8d9...) as the bench;
  - order3_40.
- order3 needs its arguments 40 12 (12 drawn lays plus 2 named). My first run, with 14 drawn lays, read 16 lays and differed; it agreed qualitatively.
- My own checks:
  - swapcheck.py: the test lay against the shipped files;
  - by hand: S_3's characters, the mod-3 identity, the cocycle, and Z_2's characters on the click world.

**VERDICT on ALG3: PASSED.** No BLOCKING item. My ALG2 items are all met, every output reruns byte for byte, and the derivations hold, with MINOR items.

## The press points

**1. Lead (a) overturned: SOUND.**
- David's fact 1 (david):
  - live monomials: 2 springs on the held clock, 12 tie monomials on (held, giver), 12 on (held, taker), and 6 two-leg monomials on (giver, taker); 0 join three clocks;
  - at round 1, D is -192,000,000 at the giver, all of it on the (2, 3) tie edge, the same at every Node-clock.
- Fact 2: SUM D over all monomials equals SUM D over the ties at 5,400 of 5,400 site-rounds, and eps B = 0. So no tooth booked through C or B moves the sum (eps B C = 0).
- The test lay (swapcheck):
  - the shipped universe (2a2aa411) and piece (85c72a56), with the setting's 54 gear entries kept and 27 added: the taker's row 0 laid as the giver's (40, 40, 0) at every site;
  - y = 0 at 5,400 of 5,400 site-rounds;
  - |SUM D| = 529,920,000, with -187,440,000 on each tie edge at site 0, round 200;
  - the compare is byte for byte, and the run back exact.
- The S_3 claim, checked by hand:
  - C^0 has character (3, 1, 0) = trivial + standard;
  - C^1 has (3, -1, 0) = sign + standard;
  - C^2 is the sign.
  - The residual is a sum at the Node-clock, so it is even.
  - Schur gives no equivariant map from trivial to sign; on the click world the swap's Z_2 alone gives the same.

**2. The miracle: SOUND.**
- An edge's work splits into its odd part (the passing, a 1-cochain) and its even part, the coupling's own, which no oriented cochain carries. With rule 2, "only the step can remove it" is DERIVED under the law of the build.
- Kicks commute and drifts commute, so today's simultaneous step is equivariant. An ordered step is not, unless its sub-steps commute.
- order3 (rerun byte-identical):
  - all at once commutes with all six relabellings on 14 of 14 lays, and SUM D is not 0 at 457 of 560 lay-rounds;
  - one clock after another: every sub-step is exact (0 of 1,680 off), but each non-identity relabelling commutes on 1 or 2 lays only.
- My 16-lay run reads the same: 16 of 16 commute all at once, and 0 of 1,920 sub-steps are off.

**3. The uncertainty: SOUND.**
- Complementarity, not a trade-off: q determines both im B^T (the lines) and im C (the circulations), so both are sharp in a record that writes q.
- The integer link, checked by hand: L_i = q_ij + q_ik and L_j = -q_ij + q_jk, so c . q = 3 q_ij + L_j - L_i. So the lines fix the circulation mod 3 = C^T C, and the third click adds 3w, which the lines never see.
- MEASURED 0 off at 5,400 on L0, L1 and the swap lay. That is a check by construction.

**4. The member's "four numbers": SOUND as ALG3 states it.**
- c^T p = 0, so c . g changes only by multiples of 3D, and with the births at the middle c . g = 0 mod 3D. One edge tooth is read back: g_ik = g_ij + g_jk.
- So the member is (two edge teeth, tau) on 3D plus the twin on D, which is (3D)^3 x D states. tau takes the read-back tooth's place, and the twin is the one number beyond the first click's three.
- member1 against Big Pic's Stepper: c . g off 0 at 0 of 5,400; 0 quanta and 0 landings apart; 3,915 landings and 7,938 side quanta on L0 (THIRD7's numbers), 2,695 and 5,487 on L1; the run back reaches the birth at 27 of 27.

**5. (C)'s end form: SOUND.**
- The act is a bijection, so an end law is the start law pulled back by T^-N.
- No cell carries it (rules 2 and 3), and no signal passes, since settings enter no act.
- The loop pairing's telescoping reads the end teeth, which answer 2 keeps out of the record.
- The mesh ring's loop pairings read 0 at every round (circ_mesh_125).

## Big Pic's 6541977181 item 3 against ALG3 5: do they agree?

His post is in no file I may read: not in the scratchpad, and 9771a49a4 is not in the local store. So I weigh it by the coordinator's quotation, "one tooth per triangle and no second number".

**They agree on tau:** one tooth per triangle carries the circulation.

**They disagree on the twin**, unless Big Pic's tooth does not turn.
- ALG3 5.4 derives that a turn mixing tau needs a second number of tau's character. Its premises: a linear turn, run back by the same act on the mirrored state, with tau kept. A kept tooth alone can only turn by an involution, and that makes two rounds a plain translation (THIRD8's argument).
- On an equilateral triangle no existing number has that character: the edges' sign part c . g is frozen at 0, and the standard and trivial parts are excluded by Schur.
- So "no second number" holds only for one of two forms:
  - a form that does not turn tau: a plain carry of the circulation, THIRD7's unturned control, whose path reads with a fixed order (lives 74,890 against 2,511 fresh), and whose choice could then sit only in the births by road (C)'s seeds' law;
  - a turn outside those premises, each of which ALG3 says breaks a law here.

**They also count the edges differently.**
- If Big Pic keeps three edge teeth beside tau, one of them is a double by ALG3 5.1 (c . g = 0 mod 3D).
- His count is then 3 + 1 with one redundant number; ALG3's is 2 + tau + the twin.
- The Boss's 10:13 summary ("tau, one number per triangle beyond the first click's three; the twin OPEN") reads the count Big Pic's way. In ALG3's count, the number beyond is the twin, not tau.

## MINOR

1. **The twin's necessity on the click world** (5.4, "no existing tooth can be the twin", by S_3's characters).
   - That argument holds on an equilateral triangle. On the click world as laid only the swap is a symmetry.
   - Under Z_2 the edges' gradient part has a swap-odd part, g_23 - g_24, which has tau's character; so does phi's phi_giver - phi_taker. Schur for Z_2 does not exclude them.
   - What does exclude them is THIRD7 section 5's line argument: a twin held in a tooth that a clock's carry reads would move the lines with the path.
   - Fix: say which argument holds where.
2. **Credit** (5.1, "THIRD9 saw this only mod 3"). THIRD7's OPEN 5 already reads "the edges' circulation c^T f is constant on the dial, since c^T p = 0", which is mod G D.
3. **The mod-3 link's condition** (section 4). c . q = L_j - L_i mod 3 needs each clock's sides to be its triangle's own edges only. That is true on the click world at mesh 0; with live Mesh sides at a clock, L_j - L_i carries them too. State the condition.
4. **The freeze.**
   - member1.py reads Big Pic's circ.py from a bench folder not in the freeze, named only as "circ.py ed6a1f225". Carry it, or its sha256 (a12ce8d9... by git show), as the 09:1x rule asks.
   - all/ also carries __pycache__ beside the archive's files.
5. **order3's arguments** (8.4). 40 rounds and 12 drawn lays are not stated; the output's name gives only the rounds.
6. **6's "So it is this lay's (DERIVED)".** The general expression is DERIVED not identically 0, but why this lay zeroes it is not derived. Fix: "MEASURED 0 on this lay; not an identity (DERIVED)".

## My ALG2 items, met or not

All nine are MET, by 1.2, items 1 to 9:
1. the odd dial, with the 09:4x ruling verbatim;
2. the law's sources, with 10:1x verbatim;
3. each edge on one triangle, with 2.6 answered by 10:1x;
4. and 5. the two wordings;
6. "the part's books, by construction";
7. 09:3x and 09:0x, verbatim;
8. the grain argument on L0 only;
9. Python 3.14.6.

My two questions are answered by the 10:1x ruling, which ALG3 cites.

## SOUND (re-derived or rerun)

- **DERIVED, re-derived:**
  - lead (a)'s failure;
  - the even part as the coupling's own;
  - commuting kicks and drifts, and an order breaking S_3;
  - complementarity and the mod-3 link;
  - the cocycle and the twin as the one new number (on an equilateral triangle);
  - no circulation on a lay a reversing relabelling fixes, which the toy's 10 symmetric lays confirm (y = 0, against 35 to 40 of 40 rounds on the 4 others);
  - the end form pulled back; the key, the stop and the strengths as non-values;
  - strengths per cell, not per clock, as a question for the owner.
- **MEASURED (rerun):** the nine byte-identical outputs above, and my swapcheck.
- **OVERCLAIMED:** "the twin cannot come from an existing tooth, by S_3's characters" read on the click world (MINOR 1); "it is this lay's (DERIVED)" (MINOR 6).

## Questions for the Boss

1. Which form does Big Pic build?
   - Three edge teeth and tau, with no turn: one edge tooth then a double by ALG3 5.1, and the path a plain carry.
   - Or a turn outside ALG3 5.4's premises.
   - And should the 10:13 summary read the member as ALG3 counts it (tau in the read-back tooth's place, the twin the one number beyond)?
2. On the click world, should the twin's necessity be cited from THIRD7 section 5's line argument rather than from S_3's characters?

## Solution24 (the reader's line)

ALG3 hands Big Pic exact facts:
- the residual is a miss in eps that no tooth can book;
- an exact step costs S_3 unless it is simultaneous;
- the lines see the circulation only mod 3;
- the member is two edge teeth, tau and one twin.

The open choice is now precise: either the triangle's tooth turns, and then a twin is forced, or it does not, and then the path is a plain carry.
