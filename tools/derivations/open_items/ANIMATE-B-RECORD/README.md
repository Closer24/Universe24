# B's record, and the decoder's readings on it (Animate)

The Boss's asks of 2026-10-29, 09:39 and 10:06 UTC (#2187 6493239195 item 4, and 6493783603), set in order in Animate's 6494185513 item 5: "a record written by B's draw, with the Split line at the source, for many pairs and late settings. On it, from the record's lines alone: S, the joint clicks, each party's marginal against the others' settings, and g2."

Beside the engine: the decoder's code waits with the build (decision 32). `python -I b_record.py` writes six records and reads each, in about 11 seconds; its output is b_record.txt.

## The answer

1. **The record holds every reading.** The decoder's own reader (src/tensor24/decoder/records.py) reads all six records under schema 1.1's guards. The 1.2 fields stand in them as fields the schema does not name, whole numbers and labels.
2. **On B's record, all nine readings hold:**
   - S = -2.775 +- 0.064, against nature's -82/29 = -2.828 at these frames, and 12 standard errors past the bound 2;
   - Mermin's M = 4 exactly, nature's 4;
   - the joint clicks at nature's law, chi-square 47.8 on 52 degrees;
   - no signal: each party's marginal against the other parties' settings, the least tail 0.26 over 10 tests;
   - each of 2,048 quanta taken exactly once, so g2 = 0 at every pair of absorbers;
   - every setting chosen spacelike to its birth and to the other takes.
3. **Each reading can fail.** Five other writers, each breaking one thing, are read the same way (part 2).
4. **So, for schema 1.2:** the lines of part 3. The source's split click carries the joint parts, sigma_f, sigma_b (G6) and the frames brought back. Each take names its birth (G5) and holds 1.1's detector and written readings. The header names no switch (decision 33).

## 1. What the toy writes

- **The board:** 32 x 32 x 32, in the runner's order (the site (x sy + y) sz + z). Light runs one Mesh a tick.
- **Three sources, 2,048 births each,** one birth every 18 rounds; each detector is 8 Meshes from its source:
  - **a pair:** the shared hand e1 x e2 - e2 x e1 (the 24 forces it, David's shared_hand.py); the frames are draft D's, a = z and a' = x at one end, b = (20, 0, 21) / 29 and b' = (-20, 0, 21) / 29 at the other;
  - **a triple:** the hand e1 x e1 x e1 + e2 x e2 x e2, put in by hand; each party's frames are x and y;
  - **one quantum spread over three absorbers,** its sizes 5, 3 and 2.
- **The settings, late:** each detector's setting is a split click of its own light over its two frames, 7 rounds after the birth and 1 round before the take. So it is spacelike to the birth (7 rounds, 8 Meshes) and to the other takes (1 round, 16 Meshes).
- **B's draw:** at the birth, the frames the detectors choose are brought back, and one law-9 draw is made over sigma_f sigma_b.
  - sigma_f is the Gaussian norm of the hand's whole-number overlap with the frames' spinors. For the pair it gives David's sizes (4, 25, 25, 4), (9, 49, 49, 9) and (49, 9, 9, 49).
  - sigma_b is 1 at every part, since each detector takes whatever comes: the future past the frames is silent.
  - Each twin carries its own outcome out, and each detector's take writes it.

## 2. The readings, and the writers that break them

| reading | B | F | signal | stale | early | off |
| --- | --- | --- | --- | --- | --- | --- |
| 1. S, two parties | holds | fails | holds | fails | holds | holds |
| 2. M, three parties | holds | fails | holds | holds | holds | holds |
| 3. the joint clicks | holds | fails | fails | fails | holds | holds |
| 4. the draw, line by line | holds | holds | holds | holds | holds | fails |
| 5. the sizes at the source | holds | not read | fails | holds | holds | holds |
| 6. no signal | holds | holds | fails | holds | holds | holds |
| 7. one quantum written once | holds | fails | holds | holds | holds | holds |
| 8. the handshake | holds | not read | holds | fails | holds | holds |
| 9. late settings | holds | holds | holds | holds | fails | holds |

**The readings,** each from the record's lines alone:
1. **S:** the two parties' correlations from the takes (each take's frame and the part it wrote, paired through the birth it names). It holds where S is past 2 by 4 standard errors and within 4 of nature's S at those frames.
2. **M:** Mermin's combination for three parties, read the same way.
3. **The joint clicks:** per setting pair or triple, the joint outcomes' counts against nature's law at those frames. It fails on a click nature never makes, or where the chi-square's tail is below a normal's at 4 standard deviations.
4. **The draw:** at every split click, room is the sum of sigma_f sigma_b, c lies below it, and drawn is the rank count of c (law 9).
5. **The sizes:** at every source, sigma_f sigma_b over room is nature's law at the frames brought back, exactly; for one quantum, sigma_b is alike at every part (Born).
6. **No signal:** each party's marginal, per own setting, against the other parties' settings; 10 tests, failing where any one departs.
7. **One quantum written once:** the takes per birth of a quantum with no frame, and g2 per pair of absorbers.
8. **The handshake:** the frames brought back are the frames the takes took in, and the drawn part is what each take wrote.
9. **Late:** each take's frame is its detector's last setting, and that setting is spacelike to the birth and to every other take of the birth.

**The writers:**
- **F, one forward board, the history kept:** the twins' direction, the triple's answers and each absorber's draw are made forward alone, with no frames brought back and no sigma_b (a 1.1 record of one board). S = -0.857 +- 0.086 and M = 0.08 +- 0.13, both within 2; 488 joint clicks nature never makes; of 2,048 quanta, 567 are never taken and 532 are taken two or three times, so g2 = 1.02, 0.97 and 1.04.
- **signal:** the pair's sizes moved by 4 toward the second twin's + where the first detector chose a', and toward its - where it chose a. S stays at nature's (-2.807), since the move leaves every correlation as it was. But the second twin's marginal moves with the first detector's setting (the least tail 1.6e-10), and 2,048 sources are off nature's law.
- **stale:** in every fourth pair, the second frame brought back is the one its detector did not choose. 512 sources disagree with their takes, and S falls to -2.090 +- 0.074, no longer past 2 by 4 standard errors.
- **early:** every setting is chosen 8 rounds before its birth, on the birth's past light cone. Every other reading holds; this one names all 10,240 takes.
- **off:** the drawn part is the rank count of the digit after c. Every count keeps its law, so the readings of the counts hold; the line-by-line check finds 1,479 split clicks off law 9.

## 3. The lines, for schema 1.2

B's first pair, as the record writes it (b_record.txt shows the first births of all three sources):

```
{"kind": "whole", "round": 9, "site": 16912, "count": 9, "train": 0, "q": 1}
{"kind": "split", "round": 9, "site": 16912, "count": 9, "train": 0, "sizes": [4, 25, 25, 4], "back": [1, 1, 1, 1], "c": 5, "room": 58, "drawn": 1, "parts": [[1, 1], [1, -1], [-1, 1], [-1, -1]], "frames": [{"site": 8720, "rho": 1, "spin": [0, 0, 1]}, {"site": 25104, "rho": 29, "spin": [20, 0, 21]}]}
{"kind": "split", "round": 16, "site": 8720, "count": 16, "train": 3, "sizes": [1, 1], "back": [1, 1], "c": 0, "room": 2, "drawn": 0, "axes": [{"rho": 1, "spin": [0, 0, 1]}, {"rho": 2, "spin": [2, 0, 0]}]}
{"kind": "whole", "round": 17, "site": 8720, "count": 17, "train": 0, "q": 1, "birth": [9, 16912], "detector": {"train": 0, "rho": 1, "spin": [0, 0, 1]}, "written": {"train": 0, "rho": 1, "spin": [0, 0, 1]}}
```

The lines, each with the field it adds to 1.1:
- **The lay:** a whole click at the source, with no birth.
- **The split click at the source:**
  - **parts:** the joint outcomes, a sign per party, or for one quantum 1 at the absorber that takes it;
  - **back:** sigma_b per part (G6), beside sizes (sigma_f);
  - **frames:** the frames brought back, each with its detector's site, in 1.1's axis form (rho and spin), or the absorber's site alone.
- **A setting:** a split click of the detector's own light, with the frames it chooses among (axes).
- **The take:** a whole click with birth (G5), the round and site of the lay it takes from. It holds 1.1's detector and written readings, which move from the split click to the take.
- **The header:** no switch (decision 33). F's record, with no back and no frames, is the 1.1 record of one board: the decoder reads it with back 1, and readings 5 and 8 read NOT READ, the cause named.

## 4. What does not follow

- **The engine's own record:** this writer stands in for stage 9's two clicks and the runner's passes. Its frames brought back are its own copy of each setting, not the backward half's carry.
- **The scheduler on a full board:** each birth here has its settings before its draw, by the writer's order of work.
- **The hands:** the singlet's is forced by the 24 (David); GHZ's is put in by hand.
- **Nature's laws in the decoder:** the singlet's and GHZ's on the equator, held by the decoder as its comparison with nature.
- **The bound of 4 standard errors:** the toy's, named.

## Method: addressed

- **(a) Which clock or gear makes each term:**
  - the split click at the source is law 9's draw over sigma_f sigma_b, at the Node-clock where the parts were one;
  - each take is a whole click at its detector, and each setting a split click of the detector's own light.

  No term is declared but the frames and the hands.
- **(b) What the clicks show, the books first:**
  - under B, every quantum laid is taken exactly once, so the books close at every birth;
  - under F, 567 of 2,048 quanta are never taken and 532 are taken more than once;
  - S and M stand past the bound 2 and at nature's.
- **(c) What does not follow, asked of the clicks:** the engine's own record, the scheduler on a full board, and GHZ's hand.

---
Animate, reader-5.
