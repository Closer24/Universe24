<!-- Boss note, 2026-10-31 09:23 UTC (first labelled ~10:0x, ahead of the clock): written by the Boss from the reader's hand-back (the harness refuses report files from readers); the text below is the reader's, whole. Reader of LIGHT3 (frozen e111cfcd), the hostile physicist (LIGHT2's physicist). -->

VERDICT on LIGHT3: PASSED

LIGHT3 meets all four of my LIGHT2 BLOCKING items and all seven of my MINORs. Every frozen output reruns identically from my copy. Its one conclusion that its own evidence did not carry, "the lay is the reflector" (5.4), turns out true: I measured it here on a single front, which LIGHT3 lacked. What remains is MINOR. Two of the MINORs (m7, m8) rest only on rulings made after the 08:41 freeze, and m5's batch ruling may also postdate it.

I did not write a REPORT.md (the harness refused the last one). My files are all in S/light2_phys/light3/:
- copy/: the frozen folder, which checks against FROZEN.sha256 (the frozen folder checks too).
- out/: every output.
- runs/ and worlds/: my two 250-round runs (a test's run length, laid by LIGHT3's own lay tool).
- p_onefront.py, p_turned.py, p_ab.py and p_prefix.py: my probes, each run twice with identical output.

How I ran it: python3 -I (the live venv's 3.14), nice -n 19, one process at a time, each start waiting until the load was below 8 (the starts read 7.4 to 8.0). Whole numbers only. I touched no repository or worktree and did not open the other reader's folder.

Reruns from my copy: all 11 outputs are identical to the frozen ones (tests; mesh with prefixes; mesh180h; ring60; ring60h; ring60k; ring180k; mesh180hk; click200; both diffs).

## BLOCKING

None.

## MINOR

m1 (5.2, 5.4, 0.5): the reflector's evidence. My own run supports the conclusion; add it to the text.
- LIGHT3's evidence, as it stands:
  - On the shipped ring, the lay changes no light line within 125 rounds.
  - ring60h is mixed from the start. On a ring of 60, the far side's wave reaches B's neighbour (site 41) by round 36 even at the board's own cone (one Mesh a round; 17 + 1 + 18). So ring60h never held a single front at B.
- My one-front test: the shipped ring and mesh180h, both run to 250 rounds. Both end lines read exact 1. LIGHT3's frozen 125-round records are exact prefixes of both, line for line.
  - 13,301 lines differ, 10,131 of them light lines (a different across field).
  - From round 44 to 142, only B's own lines differ (site 40).
  - At round 143, light lines differ at sites 39 and 41 at once.
  - From there the difference moves away from B both ways. On the lay's side: 39 at 143, 35 at 154, 28 at 170, down to site 0 by 250. On the far side: 41 at 143, 52 at 166, and on.
  - Before round 156, the far side's wave cannot reach B's neighbour even at the board's cone. Before then:
    - 64 light lines differ on the lay's side (rounds 143 to 155), with q differences up to 4,500,000 against light lines carrying up to 18,250,000 there;
    - 81 light lines differ on the far side.
- So the held hand laid unlike its neighbours turns a single front back. It does so about 100 rounds after B's own lines first differ, which the shipped 125 ticks cannot show.
- Fix:
  - put this board check (two records) in 5.2 and 5.4;
  - name the delay;
  - name ring60h as mixed from round 36.
  - 3.4 (ii) then leaves the owner's batch on this evidence.

m2 (1.4, 3.5, 0.3): at the test key, the echoes' A and B are matter only by their train's label.
- ring180k: all 8 echoes have an A and a B with no own meeting anywhere in the record. 84 of the 140 clocks of matter trains have none.
- ring60k: 2 of the 4 echoes are like that. In the other 2, A and B have 2 and 4 own meetings.
- U (case13) adds own meetings at round 100 to its tied clocks. The real record holds none for (16, 2) or (18, 2).
- Per clock, then, the relay's SHOWN survives only on ring60k, with 2 echoes. The yes stays OPEN.
- But an A with no own meeting has, by the FACE2 ruling, no count ever.
- Fix:
  - name these counts and the lines U adds;
  - require own meetings of A and B, or say that per train the rule admits observers with no count.

m3 (0.3): "Fronts round a closed board fail it" holds only for 3.3's idealized front. A real front exchanges both ways, which is the uniform relay, and that passes (3.5). Qualify the sentence.

m4 (3.5, and LIGHT3's Q2): why no order-only condition can single out B.
- DERIVED from 2.3: the medium meets only matter one Mesh away. So a chain of meetings to any B beyond A's second neighbour runs through a relay matter clock at every second site, and each relay takes and gives.
- Every echo found has B as A's second neighbour. By clock identity, all four links go through one single medium clock in 6 of the 8 on ring180k and 2 of the 4 on ring60k.
- So the condition 3.5 lacks cannot be about the order at B alone. It can only be about what passes (q, the 08:5x ruling's click content).
- m1 gives its stake: a laid B turns its quanta back about 100 rounds after it takes, while the relays turn at once.

m5 (1.1): everything rests on a Mesh side being a meeting.
- Rule L, the chains and the echo all read a Mesh side as a meeting of its two clocks. Whether it is one is in the owner's batch (08:4x: DECODE3f's "at neither place alone"; this may postdate the freeze).
- If the batch rules it no meeting, the mesh world holds no light line at all. Its meetings would then be the 4,442 held-tied ones, 122 islands of two clocks (DERIVED from 1.3).
- Name the dependency.

m6 (Q1, section 8): what to build now.
- The echo rule's yes fires on the uniform relay at the test key. If the key moves (KEY4), a built rule would print SHOWN for what is no echo off a laid B.
- Build rule L, the components and the cone now; each can fail (the click world's no, a forged meeting).
- Print the echo's yes as OPEN by name, never as SHOWN.

m7 (1.5; rests only on the 08:5x ruling, after the freeze): every text citing the click world's ticks must name that it runs 3,751 of its 5,000. 1.5 cites only the 200-round test cut.

m8 (Q3; rests only on the 08:5x ruling on P3, after the freeze): a held-hand lay chosen so that A and B become steady clocks is a number set for an outcome, unless it comes from the structure.

## My LIGHT2 items, met or not

- B1, chains through clocks: MET (2.1 to 2.5).
  - 3 components of 187, 91 and 91 clocks; 0 of 122 sites with all its clocks in one.
  - The cone is 120 / 62 / 187, and the 187 are one whole component.
  - The per-Node-clock order is named a board check, and H3 tests the hop between two clocks at one place.
- B2, the passing front and the place quiet: MET.
  - A's quiet is A's own; the turn follows the ruling.
  - The closed-board fronts read NOT SHOWN on the built records (H1, H1b, and my R4 and R6), and the turn removes ring60's two pass-throughs.
  - The uniform relay is named, and the yes is OPEN.
  - Residues: m2 and m3.
- B3, the face: MET (section 6).
  - The face and the strict variant are withdrawn.
  - A's count is 0 in every echo, and B's hold is 0.
  - The steady clock is owed, with C-a's check: not the round in disguise, repeated echoes, the earliest chain.
- B4, the held hand: MET, with a correction to myself.
  - My "from round 92" was ring60h's mixed case. With one front, the turn starts at round 143.
  - So my conclusion stands, but my evidence was confounded more than my own caveat said (m1).
- m1 to m7: all MET. (m1, per clock and the whole record: 1.3 and 1.4. m2, the key: section 7. m3, the square: 5.4. m4, the site index: dropped. m5, the file names: case01 to case13. m6, the freeze. m7: 6.1.)
- My questions:
  - Q1 and Q2 are ruled, and LIGHT3 uses both.
  - Q3, where a Mesh meeting is, went to the owner's batch at 08:4x (m5).
  - Q4 is LIGHT3's 3.5 and its own Q2.
  - Q5 is answered by section 6.

## SOUND

- 3.2's least quiet is derived correctly (b1 > g, b2 > b1, t > b2).
- 1.4's prefix caution is right: cut after round 20, the medium set reads {0, 2}.
- The lay is lawful (the ruling) and is named a test's lay.
- The text is honest throughout: the yes is OPEN, the uniform relay is named, and the reflector's NOT SHOWN in one record is given its reasons.
- The site quiet and the per-Node-clock order are named board checks.

## DERIVED / MEASURED / OVERCLAIMED

- DERIVED, and sound:
  - rule L and its prefixes;
  - the click world's no (mesh 0);
  - the least quiet;
  - the idealized front against the turn;
  - 2.3, the medium never meets its site's matter;
  - mine: m4's relay at every second site.
- MEASURED:
  - LIGHT3's section 4, 5.2, 5.3 and 6.2, reproduced;
  - mine, each twice: the one-front turn, the per-clock A and B, and the one-medium-clock echoes.
- OVERCLAIMED:
  - "the lay is the reflector" on mixed evidence (true, by m1);
  - 0.3's front sentence (m3);
  - "8 on ring180k" read as the relay of matter (m2).

## Questions for the Boss

1. LIGHT3's Q2: comparing what passes (q) at B against the relays is click content. Which comparison could tell B, with nothing picked?
2. May an observer A have no own meeting in the whole record (m2)?
3. In this plan light never meets light. So C-a's 2r beyond A's second neighbour includes the relays' holds, and light's speed would be a medium's. Is that intended, or does a world need an edge between two medium clocks (the owner's batch)?
4. Is a reflector whose turn leaves B about 100 rounds after its take, beyond the shipped ticks, fit for C-a, with the hold read in B's own count? And may a test's run length stand as that board check?

## Solution24 (the reader's line)

LIGHT3 reads light's lines, the chains and the cone per clock, and states its echo rule honestly with the yes OPEN. The held hand's lay is a lawful reflector of a single front on the board, about 100 rounds late. The click world's echo still waits on three things: A's quiet (the key), a steady clicking clock at A and at B, and a condition on what passes that tells a laid B from the relay.
