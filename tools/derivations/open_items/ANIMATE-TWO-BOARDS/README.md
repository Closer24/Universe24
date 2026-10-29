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

- **O, the product draw ordered by the board's tick (David's 6491076850), approved by decision 29** (the owner's word to the Boss of 08:3x UTC, tensor24-review 6e3cbbfe).
  - The first click draws with a silent future; the second draws over the products, with the first outcome carried along the zigzag.
  - The order, and a tie rule the 24 leave alike, are what make the history one: U below shows what happens without them.
  - David's probe (toys-5 f3661f52, derive/david_open/two_boards) shows:
    - A first, B first and a shared tick alike, at S = -82/29;
    - every carry one Mesh a step, and no read across space;
    - three parties with no two-party marginal moving with the third's setting;
    - a machine's feed-forward with one history per pair of digits.
- **B, the draw at the birth, is the same law seen at the source,** not a rival rule.
  - The draw is made at the Node-clock where the twins were one, reading both settings carried back. It is draft D's local split at one Mesh (L = 1), moved to the birth.
  - Each twin carries only its own outcome out.
  - **For a spacelike pair it needs no order and no tie rule:** the four parts in any order give one law, equal to O's.
  - **For a causal loop** (a later setting that depends on an earlier outcome) it needs the parts ordered by cause, and then equals O. The cause's order is physical, carried along the forward board.
  - The runner needs one pass forward to the settings, one back along the twins to the birth, and one forward with the outcomes (on paper; the toy has one pair).
- **Both re-run the twins' paths once a later event is known** (O, the first outcome; B, the settings), and neither reads across space. Each is a schedule that verifies a history, not a search that selects one: Sofer's reading 7 (6491095182).
- **U, no order at the detectors, is out, and it is why O needs its order:**
  - two histories at (a . b)^2 of the digits;
  - the sweeps cycle in about a quarter of them;
  - a fair choice between two gives |S| = 3.66, past nature's bound.

## 3b. Reading 15: which form the engine builds (Sofer's 6492798477)

**B, the product draw made where the dials meet at the source.**
- **The draw's place:**
  - the twins' shared hand stays one at the birth Node-clock (the Boss's 6493065300: the joint sizes are the norms of its whole-number overlaps with the two detectors' frames, nothing typed but the frames);
  - the backward board carries each detector's frame back along its own twin to the birth;
  - one law-9 draw is made there, over the overlaps' norms (the product of the two dials' sizes, decision 29);
  - the forward board carries each outcome out along its own twin, and the detector's click writes the record.
- **No Node-clock compares ticks at a distance:**
  - a spacelike pair needs no order: the four parts in any order give one law (part 1);
  - a causal chain takes its order from the forward signal that makes the later setting depend on the earlier outcome. The runner's passes meet that order by themselves: the later setting cannot be carried back before the earlier outcome is carried out.
- **The passes verify and do not select.** One history at every digit, in the spacelike case and, with the cause's order, in the loop (part 1).
- **O's law is the same,** so every reading of David's probe carries over (S, the marginals, three parties). Only the draw's place moves, from the second detector to the source.
- **The same rule for one spread quantum:** the draw at its emitter over the absorbers' sizes carried back, so one absorber clicks (g2 = 0); with a silent future, Born.
- **Open:** the scheduler on a full board (many pairs, nested chains), and the act at the birth giving the one shared hand (the Boss's open step).

## 4. The swings, and the clicks between the boards, by kind

- **The swing** is the same on both boards. The act is symmetric in time (T S T = S^-1) and the source rho + 3p is even, so the backward board sees the load's swing run back, with the same tops and bottoms. The boards agree on the pendulum and part only at the escapement, the clicks.
- **The whole click (how much):**
  - the forward board decides it (q at least 1) and writes the record;
  - the handshake between the giver and the taker is a check, not state: each quantum laid once and taken once, read on the forward record through G5. It adds nothing to the backward board's integers (Sofer's reading 12, 6492354773);
  - the books close at both ends.
- **The split click (which):**
  - the draw runs over the products of the two dials' sizes where they meet (decision 29);
  - for a pair, the second click reads the first outcome carried back to the birth and out along its own twin. Seen at the source, this is one draw at the birth over the four parts;
  - for one spread quantum, the word runs back to the source and out, so one absorber clicks (g2 = 0);
  - the detector's click writes the record;
  - with a silent future it is Born exactly.
- **The silence:** nothing passes.
- **The records:** forward only. The backward board writes none and erases none, so the arrow stays the records' growth.

## 5. Open, each with its probe

- **What the toy puts in by hand** (Sofer's reading of David's probe, 6492354773, holds here too): the joint sizes are the singlet's, n - s t (a . b). So S = -82/29 in O and B shows the bookkeeping and its exactness, not the act's own derivation of those sizes from the twins' frames, which is the engine probe's. What the toy finds on its own:
  - the bound of 2 on every forward-only history, exhausted;
  - U's two histories, its cycles and its S past nature's bound;
  - the loop's dependence on the order of the parts;
  - g2 above 0 when each absorber draws alone.
- **Complexity is not the two boards' work** (the Boss's swing probe and its argument, 6492236807): P(history) = P(future) P(history | future). So a history that agrees with itself draws by the forward law, Born, and leans no click toward composites; a lean needs a future set from outside, a declared goal. The growth is the forward board's ratchet, the bang that keeps history. This page's part 2 agrees: the two do different jobs.

- **The scheduler on a full board:** many pairs, chains and composites, each split click's settings found before its source's draw, by local passes and with no selection. The toy has one pair.
- **Loops beyond one step:** a machine whose choice depends on its own outcome through many clicks, with the cause's order read along the forward board.
- **The cost:** the backward board's integers per Node-clock and the passes; the record's G5 (the birth) and G6 (the backward sizes; under B, the settings carried back).
- **The probe on the engine as built** (the Boss's), with the product draw and the switch in the universe file (decision 29): S, g2, Born, three parties with no signal, and a loop. Born with the switch off.
- **The aim's lean** (David's probe, part 5): a split leaning toward a composite has two histories at some digits, and Born holds when the fewer is kept (his rule). Born's row 55 on the forward record reads whether the lean leaks.

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
