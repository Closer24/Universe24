# Two boards on one Node-clock, tested on one pair (Animate)

The owner's word to Animate, 2026-10-29, 08:4x UTC (in Hebrew; in translation): "Go with the proposal, check it, and understand why it is two boards that help, and not a bang that keeps history: the swings, and what the clicks do between the boards, by kind." The proposal was Animate's answer to his question of 08:3x UTC: a small board, one pair, two detectors that choose late; count the consistent histories, check whether the sweeps settle on one without a choice, then Bell's S, the marginals and a loop.

- **The toy:** two_boards.py, in exact integers; two_boards.txt is its run (about one second).
- **The pair:** born at one Node-clock as a singlet; its twins ride to two detectors that choose their axes late, each from its own digits.
- **The axes:** draft D's (a = z, a' = x, b = (20, 0, 21) / 29, b' = (-20, 0, 21) / 29), where the singlet gives S = -82/29.
- **The draws:** every draw is law 9's, each part's weight an integer, and every digit of every draw is enumerated. So each law below is exact, not sampled (but for one line, marked).

## 1. The results

| the form | S at draft D's axes | the marginals | histories per digit |
| --- | --- | --- | --- |
| **F**, one forward board: the twins carry a direction drawn at the birth (law 6's definite pair), each detector draws alone | -82/87 = -0.94 | 1/2 | one |
| **F**, the history kept: the twins' direction is the last bang's record (the chosen path) | -1.47 over 4,096 bangs, -1.41 over 65,536 (sampled) | | one |
| **F**, any forward-only history at all (the 16 fixed answers per setting, exhausted) | at most 2 in size | | |
| **O**, two boards ordered by the board's tick (David's): the first click draws with a silent future, the second over the products | -82/29 = -2.83, nature's | 1/2 at every setting | one |
| **U**, two boards with no order: each click's backward sizes from the other's outcome | two histories at (a . b)^2 of the digits; the sweeps cycle at 26 and 24 percent; a fair choice gives -106/29 = -3.66, past nature's bound of 2.83 | 1/2 | none 0, one or two |
| **B**, two boards with the draw at the birth: the settings carried back along the twins, one draw there over the four parts, each outcome carried out | -82/29, nature's, the four parts in any order, equal to O's law | 1/2 at every setting | one |

**A loop** (the second setting chosen by the first outcome: b' after +, b after -; the first setting a'):
- **B, with the four parts ordered by cause** (the first end's outcome outer): one consistent history at all 116 digits, and its law equals O's, which is sequential quantum mechanics.
- **B, in the other order:** 40 digits have no consistent history, 36 have one, and 40 have two.
- **O:** one history at every digit.

**One quantum over three absorbers** (sizes 5, 3 and 2; Grangier):
- **F**, each absorber drawing alone at its own share: two or more click at once with odds 1/4. That is g2 above 0, where nature gives 0.
- **B**, one draw at the source over the absorbers' sizes carried back: odds 1/2, 3/10 and 1/5, and two never click at once (g2 = 0).

## 2. Why two boards help, and a bang that keeps history does not

- **A kept history carries information forward only.** The records pass the bottom into the next bang, and the chosen path's record becomes the next twin's direction. All of it is decided before the late settings.
- **So every forward-only history is a mix of fixed answers set before the choice.** Its S is at most 2: the 16 fixed answers are exhausted, and the kept history reads -1.41.
- **Nature's -2.83 needs the late setting to reach the pair's source.** That is information from the future. The second board adds that one direction, from a click back to the birth, and nothing else. With it, the toy reaches:
  - nature's S at -82/29;
  - g2 = 0;
  - marginals of 1/2, so no signal.
- **The two do different jobs.** The kept history is the arrow and the ratchet: each bang starts richer, and the chosen path builds composites (ANIMATE-LAW-CHOSEN-PATH.md). The backward board is the reach into the past that the correlations of pairs and of one spread quantum need. It writes no record.

## 3. Which two-board form

- **B, the draw at the birth, is the cleanest.**
  - **One draw, local:** the draw is made at the Node-clock where the twins were one, reading both settings carried back. This is draft D's local split at one Mesh (L = 1), moved to the birth.
  - **Nothing crosses space:** each twin carries only its own outcome out, at its own speed, so in the board's time nothing crosses space.
  - **One history, no order needed:** while no setting depends on the pair's own outcomes, there is one history at every digit and no order is needed. The runner needs one pass forward to the settings, one back along the twins to the birth, and one forward with the outcomes (on paper; the toy has one pair). Each pass reads neighbours only, and nothing is selected. That meets Sofer's reading 7 (6491095182): a schedule that verifies, not a search that selects.
  - **A causal loop** (a later setting that depends on an earlier outcome, the clicks in each other's light cone): B needs the parts ordered by cause, and then equals O. The cause's order is physical, carried along the forward board, not a frame chosen.
- **O, ordered at the detectors (David's),** gives the same law. But in the engine's order of work, the far twin learns the near outcome at the tick of the near click: an update at a distance, the zigzag being its path in spacetime. For clicks outside each other's cones it needs an order across the board, a frame.
- **U, no order at the detectors, is out:**
  - two histories at (a . b)^2 of the digits;
  - the sweeps cycle in about a quarter of them;
  - a fair choice between two gives |S| = 3.66, past nature's bound.

## 4. The swings, and the clicks between the boards, by kind

- **The swing** is the same on both boards. The act is symmetric in time (T S T = S^-1) and the source rho + 3p is even, so the backward board sees the load's swing run back, with the same tops and bottoms. The boards agree on the pendulum and part only at the escapement, the clicks.
- **The whole click (how much):**
  - the forward board decides it (q at least 1) and writes the record;
  - the backward board carries only the confirmation back to the source, so the giver and the taker close one handshake;
  - the books close at both ends.
- **The split click (which):**
  - the draw is made at the source, where the parts were one (the birth of a pair, or the emitter of one spread quantum), over the parts' sizes;
  - the backward board carries the future's settings and absorbers there;
  - the forward board carries each outcome out, and the detector's click writes the record;
  - for a lone quantum with a silent future, this is Born.
- **The silence:** nothing passes.
- **The records:** forward only. The backward board writes none and erases none, so the arrow stays the records' growth.

## 5. Open, each with its probe

- **The scheduler on a full board:** many pairs, chains and composites, each split click's settings found before its source's draw, by local passes and with no selection. The toy has one pair.
- **Loops beyond one step:** a machine whose choice depends on its own outcome through many clicks, with the cause's order read along the forward board.
- **The cost:** the backward board's integers per Node-clock and the passes; the record's G5 (the birth) and G6 (the backward sizes; under B, the settings carried back).
- **The probe on the engine as built** (the Boss's), with B's rule: S, g2, Born, three parties with no signal, and a loop.

## Method: addressed

- **(a) Which clock or gear makes each term:**
  - the forward board is the act as built;
  - the backward board is the act run back, carrying settings and sizes, and writing nothing;
  - the draw is law 9's, at the Node-clock where the parts were one.

  No term is declared.
- **(b) What the clicks show, the books first:**
  - every law is exact, each draw enumerated whole;
  - each part is drawn its weight's times;
  - the marginals are 1/2 at every setting;
  - one quantum is written once (g2 = 0).
- **(c) What does not follow, asked of the clicks:**
  - the scheduler on a full board;
  - loops beyond one step;
  - the probe on the engine.

---
Animate, reader-5.
