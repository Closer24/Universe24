# Rule B's scheduler on a full board: one rule for every band (Animate)

The asks:
- the Boss's 6494549592, item 4 ("The scheduler on a full board has to be sized by the depth of its chains, not three passes fixed");
- Sofer's owed line (5) of 6494833685;
- Animate's own 10.5, item 6 (every band of agreeing histories must part at one Node-clock, and the probe must look for a band that does not);
- the owner's word to Animate of 2026-10-29, 11:5x UTC (in Hebrew; in translation): "The rule must be generic."

Beside the engine. `python -I scheduler.py` runs in about 8 seconds; its output is scheduler.txt. It reuses the hands, frames and sizes of ANIMATE-B-RECORD/b_record.py.

## The answer

1. **One rule draws every band.**
   - **The band:** the parts that share a hand (one birth's twins) or a slot (one absorber at one tick, reachable by more parts than it has free).
   - **The draw:** each band is decided by one law-9 draw over the products sigma_f sigma_b of its joint histories, conditional on what is drawn, in the pass in which its products come in.
   - **The place:** the draw is made at the Node-clock where the band's parts are one: its birth, or the slots that join it, their digits summed.
   - **Nothing else is typed.** A full slot weighs 0 by sigma_b, and the place of a draw is where its parts are one. One function in the code does every draw, for pairs, triples, spread quanta, the one-slot tie and a chain of ties.
2. **Each part is drawn as its setting comes back.** Where only some of one birth's parts are in, those are drawn first, over the products summed over the rest.
   - **This is lawful by no signal:** a subset's sizes, summed over the other parts, are the same in every frame of those parts. Every such draw was checked against every frame the parts still out could take, exactly: 9,872 checks, all equal.
   - **A spacelike pair whose settings come back in one pass is drawn at once,** as reading 15 has it.
3. **The passes are 1 + 2 times the depth of the chains of settings,** a free setting counting 1 and a machine one more than the take it heard. This held on every one of 400 random boards, at depths 1 to 5 (3 to 11 passes).
4. **Drawing each birth whole (J) is no scheduler.** Pass by pass, it deadlocks wherever a birth's setting waits, through any chain, on that birth's own outcome: on 141 of the 400 boards, and on the crossed births always.
5. **The band that no Node-clock decides, found.** Taken as a history that agrees with itself, J needs the cause's order of the parts:
   - with the heard party's sign outermost: one history at every digit, and nature's law;
   - with that order reversed: of 53,824 free frames and digits, 3,200 have no history and 3,200 have two. The two differ at both births at once, so no single Node-clock parts them.

   The one rule never meets this band, because it never draws a part before that part's setting is in.
6. **The one-slot tie is the same rule, with nothing added.**
   - **Two quanta reaching one absorber's one free slot at one tick:** with each source drawing alone and the slot as sigma_b, 216 of 900 digit pairs have two histories.
   - **Under the one rule** the two quanta are one band, joined by the slot, and drawn once at the absorber where they are one. That gives one history at every digit, each quantum taken once, at the products over the band: 6/19, 4/19 and 9/19.
   - **A chain of three quanta joined by two slots** is one band, drawn once with the two slots' digits summed: 3/10, 1/5, 1/5 and 3/10, with every quantum taken once and no slot past its free count.

## 1. The board

- **A line of Node-clocks;** light runs one site a tick.
- **Births:** a birth lays a pair (the shared hand e1 x e2 - e2 x e1), a triple (e1 x e1 x e1 + e2 x e2 x e2), or one quantum spread over absorbers.
- **Takes:** each twin rides one site a tick to its detector and waits there 0 to 3 ticks; its take is a whole click.
- **Settings:** each detector's setting is a split click one tick before its take. It is either free (its own light's digit over its two frames) or a machine that sets its frame from an outcome it heard by light, a take strictly inside its past light cone.
- **The sizes:** sigma_f is the Gaussian norm of the hand's whole-number overlap with the frames' spinors, or a spread quantum's share at an absorber. sigma_b is an absorber's free slots. Every draw is law 9's, the rank count of a digit over the running sums.

## 2. Part 1: two crossed births

- **The births:** Q at site 50 and P at site 100, both at tick 0.
  - Q's first twin is taken at site 40 (tick 10) and its second at site 150 (tick 100).
  - P's first twin is taken at site 120 (tick 20) and its second at site 10 (tick 90).
- **The crossing:** Q's second frame is set by P's first outcome, heard by light (30 sites in 79 ticks), and P's second frame by Q's first outcome. Each birth's two takes are spacelike.
- **J as built pass by pass:** it deadlocks.
- **J as a history that agrees with itself** (guess both early outcomes, draw each birth whole, keep the guesses the draws return):
  - cause's order: one history at each of the 53,824 free frames and digits; nature's law;
  - order reversed: 3,200 with none, 47,424 with one, 3,200 with two.
- **The one rule:** one history at each of the 215,296 digit sets, in 5 passes. Its law is nature's sequential law: each first outcome 1/2, and each second outcome its row given the first, at the frame then set.

## 3. Part 2: random full boards

400 boards on a line of 96 sites, each with 12 births (about a third of them triples), and 0, 30, 60 or 90 percent of the detectors machines:

| depth | boards | passes = 1 + 2 depth | passes | layer checks, equal | J deadlocks |
| --- | --- | --- | --- | --- | --- |
| 1 | 100 | 100 | 3 | 1,200, 1,200 | 0 |
| 2 | 76 | 76 | 5 | 1,706, 1,706 | 12 |
| 3 | 162 | 162 | 7 | 4,888, 4,888 | 84 |
| 4 | 57 | 57 | 9 | 1,900, 1,900 | 40 |
| 5 | 5 | 5 | 11 | 178, 178 | 5 |

Parts 1 and 2 give the same numbers through the one rule's code as through the first, pair-only code (reader-5 325440ef).

## 4. Part 3: quanta at absorbers' free slots

Every draw is the one rule's, by the same function as Parts 1 and 2:
- **A alone,** over x and z (sizes 2 and 3): its band is its own birth, so x 2/5 and z 3/5, Born.
- **A and B**, B over y and z (sizes 3 and 2), both reaching z at one tick, where one slot is free:
  - each source drawing alone, the slot as sigma_b: of 900 digit pairs, 684 have one history that agrees with itself and 216 have two;
  - the one rule: their band is drawn at z, where they are one. The law is A at x and B at y 6/19, A at x and B at z 4/19, and A at z and B at y 9/19; A and B both at z weighs 0.
- **A chain:** A over x and z (2 and 3), B over z and z2 (2 and 2), C over z2 and w (3 and 2), with one slot free at z and one at z2.
  - The three quanta are one band, drawn once at z and z2 with their digits summed.
  - Its law is x/z/z2 3/10, x/z/w 1/5, x/z2/w 1/5 and z/z2/w 3/10.

At every digit, every quantum is taken exactly once, and no slot past its free count.

## 5. What does not follow

- **The engine:** stage 9's two clicks and the runner's passes on the act's own arrays.
- **Locality:** each carry rides its part's own path, one site a step, by construction here. The Boss's bpasses.py counts the reads (0 far).
- **A band joined both by a hand and by a slot,** a twin in a slot contest: the same rule (its parts are one at the birth and at the slot, the digits of both), not measured here.
- **A loop through the backward run itself,** a setting that read the tag. The rule that every setting is a forward click, read only from takes in its past light cone, excludes it, and the probe makes none.

## Method: addressed

- **(a) Which clock or gear makes each term:**
  - each draw is law 9's over sigma_f sigma_b, at the Node-clock where the band's parts are one;
  - each setting is a split click of the detector's own light, or a machine's frame from a take it heard by light;
  - the passes are the runner's order of work.

  No term is declared: a full slot weighs 0 by sigma_b, and the place of a draw is where its parts are one.
- **(b) What the clicks show, the books first:**
  - every part of every band is drawn once and taken once, on every board and at every digit;
  - the law is nature's at every layer, exactly, and the products over the band where a slot joins quanta;
  - two histories that no single Node-clock parts appear only when a birth is drawn whole out of the cause's order, or when two sources draw alone across a shared slot.
- **(c) What does not follow, asked of the clicks:** the act's own run, and a band joined by a hand and a slot at once.

---
Animate, reader-5.
