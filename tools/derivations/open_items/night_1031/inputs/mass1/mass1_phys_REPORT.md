# MASS1, read by the hostile physicist (2026-10-31)

(Written by the Boss from the reader's hand-back at 08:4x UTC, the reader's harness refusing the write; the text is
the reader's, word for word.)

VERDICT on MASS1: NOT PASSED

Four items block: three in the text's own physics, and one board claim that my measurement overturns. Its strong parts stand:
- The group theory and the triangle's numbers are correct.
- No probe types a number of nature.
- No strength, key or lay is picked toward 1,836.

The four blocks:
- **B1:** sentences read board quantities as masses.
- **B2:** the mass reading's definition cannot tell a mass from a depth.
- **B3:** "there is no beat to read" is overturned on the board.
- **B4:** "a lone member stays bound at every size" does not follow from what it cites.

Both the text and my reading are of node-all 9d75a4904, the frozen tree.

**My files**, in S/mass1_phys/ (the harness refuses REPORT.md writes, so the Boss writes this report):
- `copy/` is a copy of the frozen folder's tree/src, tree/examples, probes and out. It checks against FROZEN.sha256.
- `p_beat_long.py` runs the click world's lay on one Node-clock (every site is laid alike). It reproduces beat.py's 400 rounds to the count: 238/292, 161/162, 99/150, and the same three FAILS.
- `p_beat_long.run1.txt` and `run2.txt` are its 3,700-round runs, byte-identical, sha256 c5e7df89f520bc58.
- At one point I started a 5-second run at load 8.75; every later run waited for the load to be at most 8.

## BLOCKING

**B1. Board quantities are read as masses (press 1).** The text's own 1.2 says a click-world mass ratio is N_X/N_Y, own lines between light links. It also says lines per beat read the key and the amplitude, so a beat ratio is a mass ratio only in a fit click form whose lines per beat come from the structure. That form is OPEN. Yet these sentences read the board directly:
- Verdict, bullet 4: "the board's mass walks with it".
- 3.2(b): "The board's mass is thus universal, like one Yukawa for every fermion".
- 1.3: "The board's 'mass' sits at the rounding scale".
- 4.3: "no steady mass", read from the tied curvature's growth.
- 2.4: "m(2')/m(2'') = 1, and nature refuses it". This is a Schur equality of board beats, read as a mass equality.
- Verdict bullet 2, 3.2(c) and 3.3 set the board's tied/held beat ratio (about 245) against 1,836.15 ("to meet 1,836.15 that product would have to be about 3.37 million"; "nothing like 1,836"). The tied/held pair is not even either named design (2.2).
- Section 3's title, "Which mass ratios the structure alone could fix", analyses board beats.
- 1.3 quotes the code's docstring without flagging it: plans.py line 4, "the tied hand's beat, 2 hold f |k|^2 / W ... is what the clicks read as its mass". That is a claim of physics in the code, standing on a board quantity the clicks have never read.

Fix:
- Restate section 3 and the verdict as clock facts: what the structure fixes about beats.
- Carry "only in a fit click form (OPEN)" in every sentence that meets 1,836.
- Strike "the board's mass" and the Yukawa analogy.
- Name plans.py line 4 for the documentation clean-up.

**B2. The definition (1.2, labelled DERIVED) cannot tell a mass ratio from a depth.**
- X and Y need only be "at rest relative to each other", at any depth.
- For static clocks at two depths, N_X/N_Y = (m_X/m_Y) x (the ratio of their proper rates). The owner's law says a deeper clock counts less.
- None of the four checks fails for that factor:
  - M1: a static factor is the same in both windows.
  - M2: in a static world the factor does not depend on the source.
  - M3: it tests motion only.
  - M4: depth factors multiply, so the products agree.
- Also, "each [quantum] is taken by X and by Y": a quantum is one passing from one clock to another, so it cannot be taken twice.

Fix:
- Require X and Y side by side (one Node-clock), or add M5, a swap: each design laid at the other's place reads the same ratio, and the check fails if the ratio carries a depth.
- S lays one quantum per taker.
- MASS2 builds this definition, so it must be right first.

**B3. "There is no beat to read" (4.3) and "the held count stands at 0 or 1" are overturned on the board.** These read 400 rounds as the present act. MEASURED with p_beat_long, twice alike, over 3,700 rounds, on a copy:

| rounds | held |k|^2 (most, per 250 rounds) | tied pair's half-beats (rounds) |
|---|---|---|
| 1 to 500 | 1 | |
| 501 to 750 | 4 | |
| 653 to 1627 | at most 1 (751 to 1750) | 184 to 207, mean about 195: steady to about 5% over about 2.5 beats |
| 1751 to 2500 | 9 | about 88 |
| 2501 to 2750 | 36 | about 59 |
| 2751 to 3000 | 16 | |
| 3001 to 3500 | 4 | |
| 3501 to 3700 | 49 (count 7) | |

- The held count is 0 in 16 to 81 of every 250 rounds.
- The giver and the taker swing in phase: their sign changes are 5 to 15 rounds apart.
- So the tied gears integrate the held hand's fast round-by-round flicker and beat at its mean. The beat is real, and it walks with the held count's excursions.
- The present act's held hand wanders to count 7 by round 3,700. 4.3 credits that walk to B-edge alone ("1 to about 30 in 5,000"). The comparison needs the present act's own walk.

M1 at 1,000-round windows still fails, by 2.2 to 8.6 times the calibre:
- held : giver 7,186/3,224 and 8,656/3,616;
- held : taker 25,278/3,223 and 31,142/3,634;
- giver : taker 9,386/2,201 and 20,430/2,466.

So 1.3's conclusion stands: no steady own-count ratio. But its "about ten times" belongs to 200-round windows, about one half-beat each, where any beating pair fails by phase alone.

Fix:
- 4.3 and 1.2 should say: a beat steady to about 5% while the held count stays at 0 or 1, walking when it walks; no beat steady enough for a mass.
- Read M1 over whole beats.

**B4. "A lone member tied to the held hand stays bound at every size" does not follow from what it cites.** The derivation (4.4) is "from the signs: V = s |k|^2 + c |k|^2 |x|^2 is positive definite". This sentence carries the verdict's sorting of the designs.
- V is only semi-definite: it is 0 at k = 0 for every x, so the energy bounds no x. At |k| = 0 the member has no restoring force at any size, and the held count is 0 in 16 to 81 rounds of 250 (MEASURED).
- So the lone member's binding is the held hand's state, as the triangle's is. The designs differ by a threshold on one held count:
  - the lone member needs |k|^2 > 0;
  - the pair needs 2c|k|^2 > tie.
- The text's other side, the pair's V_T indefinite where 2c|k|^2 < tie (|k|^2 < 0.8), is right.

Fix: restate the sorting, and what it says about the families, on those two thresholds.

## MINOR

- **m1 (verdict bullet 3; 3.4 to 3.5; triangle.py).** triangle.py prints "48 x 38 = 1824" and "(3 + r10)^4". These are products picked for nearness to 1,836, so 1,836 is used as a selection target. Keep the chance estimate as a control, move it out of the verdict, and print no product picked for its nearness.
- **m2 (verdict bullet 2; 3.3).** "Which no whole lay meets exactly" and "not whole" cannot fail, and they mislead. den Gamma |k|^2 = 561,909 gives root(3,371,454) = 1,836.1520, 4 parts in 10^7 from nature's ratio and inside 5.1's own calibre of 3 x 10^-6. Only the fake rule forbids it; say so.
- **m3 (1.3; beat.py).** The "own lines" are sides with a quotient not 0 at the clock's own Node-clock, with the Mesh sides left out. They are not the record's lines that name the clock (FACE2's own count). Name them sides, or count lines.
- **m4 (2.2 to 2.3; Statuses; press 2). The designs are named, not derived.**
  - "Spin 1/2 is a half-speed kind" and "The proton is an E1/2, in the two ways three spins make 1/2" read physics onto board kinds.
  - The Statuses list "'never seen alone' as L4" under DERIVED. The fact B C = 0 is derived; the confinement reading is the owner's picture, OPEN.
  - The proton's design is two different things: 2.2's triangle of unlike whole-kind members, and 2.3's three half-speed members. Say which one, and label the mapping OPEN throughout.
- **m5 (5.1).** The size estimate assumes the outcome: a quarter turn over 1,836, at least 7,344 rounds a beat, 6.6 x 10^8 lines. That is fine as a condition a world meets; say it is no lay.
- **m6 (1.1).** The Compton phase is not observed alone, only its differences. Name it as the FACE2 frame's reading.

## SOUND

- **Press 3.** No probe types a number of nature. No strength, key or lay is picked toward 1,836: the probes read the shipped click world's files, and "every strength read as 1" is labelled a reading, no world.
- **families.py's counts**, which match SU(2)'s 2x2x2 = 2+2+4:
  - dimensions 1, 1, 2, 3, 3 and 2, 2, 4; squares summing to 24 and 48; orthonormal characters;
  - E1/2^3 = 2 E1/2 + G3/2 and E1/2 x T1 = E1/2 + G3/2;
  - the trains as 2 G3/2 and 2 E1/2 + 2 E5/2 + 4 G3/2;
  - the generations' a, b, b under the 48.
- **triangle.py:**
  - B C = 0; K = 3; spectra {0, 3, 3} and {2, -1, -1}; B^T B + C C^T = 3I;
  - L = [[19, 6], [60, 19]], hyperbolic;
  - 9K = 457,302,861 = 3^3 x 16,937,143, with L's order 528,480 checked by L^N = I and by L^(N/p) not I;
  - the lay's numbers: W 6 x 10^8; f 60,000; held curvature 392 x 10^6, 163 per mille of 4W; tied curvature 120,000, split into 216,000 and 24,000 (ratio 9).
- **The physics that is right:**
  - nature's numbers: 1,836.15267343; muon over tau 0.059; 6 pi^5 within 2 in 10^5;
  - the law of beats: 2 - 2cos theta = kappa/W, the window kappa < 4W, and cos theta = W/(W+s) for the polarized step;
  - M3's 2pq/(p^2 + q^2);
  - "a rest mass reads no state, so a law of the least orbit is needed" (4.2).

## DERIVED / MEASURED / OVERCLAIMED

- **DERIVED, sound:** the counts; Schur's equalities as clock facts; the triangle's algebra; the pair's indefinite V_T.
- **MEASURED:** the text's probes, which I confirmed on a copy; mine, B3.
- **OVERCLAIMED:**
  - section 3 and the verdict's mass ratios, which are board beats (B1);
  - the definition as DERIVED (B2);
  - "no beat to read" (B3);
  - "bound at every size" (B4);
  - "'never seen alone' as L4" as DERIVED (m4).

## Questions for the Boss

1. Is plans.py line 4's docstring, "what the clicks read as its mass", to go to the documentation clean-up?
2. Should MASS2's reading require one Node-clock for the two clocks, or the swap check M5?
3. Should the held hand's walk in the present act (to count 7 in 3,700 rounds) go to the miracle texts beside B-edge's heating?

## Solution24

Keep MASS1's negative verdict: no mass can be read today, and the structure fixes only equalities and counts. Restate it as clock facts with the bridge to masses OPEN. Fix the reading's definition for depth before MASS2 builds it. Read the board's beat as it is: steady at the held flicker's mean, walking with the held count.
