# Rule B's scheduler on a full board (Animate)

The asks: the Boss's 6494549592, item 4 ("The scheduler on a full board has to be sized by the depth of its chains, not three passes fixed"); Sofer's owed line (5) of 6494833685; and Animate's own 10.5, item 6 (every band of agreeing histories must part at one Node-clock, and the probe must look for a band that does not).

Beside the engine. `python -I scheduler.py` runs in about 12 seconds; its output is scheduler.txt. It reuses the hands, frames and sizes of ANIMATE-B-RECORD/b_record.py.

## The answer

1. **Draw each part as its setting comes back.** At each backward pass, a birth draws, at once, the parts whose settings have come back, conditional on the parts it drew before. The frames of the parts still out are silent. This is the layered scheduler, L.
   - **The law is nature's:** a subset's sizes, summed over the other parts, are the same in every frame of those parts (no signal). Every layer's draw was checked against every frame the parts still out could take, exactly: 9,872 checks, all equal.
   - **A spacelike pair whose settings come back in one pass is drawn at once,** as reading 15 has it. Only parts whose settings come back at different passes are drawn in turn, and that turn is the passes' own, which the forward record's light cones set.
2. **The passes are 1 + 2 times the depth of the chains of settings,** a free setting counting 1 and a machine one more than the take it heard. This held on every one of 400 random boards, at depths 1 to 5 (3 to 11 passes).
3. **Drawing each birth whole (J) is no scheduler.** Pass by pass, it deadlocks wherever a birth's setting waits, through any chain, on an outcome of that same birth: on 141 of the 400 boards, and on the crossed births always.
4. **The band that no Node-clock decides, found.** Taken as a history that agrees with itself, J needs the cause's order of the parts:
   - with the heard party's sign outermost: one history at every digit, and nature's law;
   - with that order reversed: of 53,824 free frames and digits, 3,200 have no history and 3,200 have two. The two differ at both births at once, so no single Node-clock parts them.

   L never meets this band, because it never draws a part before that part's setting is in.
5. **One case is left: two quanta reaching one absorber's one free slot at one tick.**
   - With the slot as sigma_b and each source drawing alone, 216 of 900 digit pairs have two histories.
   - The two differ only in which quantum the absorber takes, so they part at the absorber, and its own click must decide.
   - One candidate is named: the absorber draws once over the joint histories' products, with the sizes reaching it along the quanta's own paths. The rule is David's open item (5.2: "two spread quanta ... take their passes in turn").

## 1. The board

- **A line of Node-clocks;** light runs one site a tick.
- **Births and takes:**
  - each birth lays a pair (the shared hand e1 x e2 - e2 x e1) or a triple (e1 x e1 x e1 + e2 x e2 x e2);
  - each twin rides one site a tick to its detector and waits there 0 to 3 ticks;
  - its take is a whole click.
- **Settings:** each detector's setting is a split click one tick before its take. It is either free (its own light's digit over its two frames) or a machine that sets its frame from an outcome it heard by light, a take strictly inside its past light cone.
- **The draws:** sigma_f is the Gaussian norm of the hand's whole-number overlap with the frames' spinors, and every sigma_b is 1. Every draw is law 9's, the rank count of a digit over the running sums.

## 2. Part 1: two crossed births

- **The births:** Q at site 50 and P at site 100, both at tick 0.
  - Q's first twin is taken at site 40 (tick 10) and its second at site 150 (tick 100).
  - P's first twin is taken at site 120 (tick 20) and its second at site 10 (tick 90).
- **The crossing:** Q's second frame is set by P's first outcome, heard by light (30 sites in 79 ticks), and P's second frame by Q's first outcome. Each birth's two takes are spacelike.
- **J as built pass by pass:** it deadlocks.
- **J as a history that agrees with itself** (guess both early outcomes, draw each birth whole, keep the guesses the draws return):
  - cause's order: one history at each of the 53,824 free frames and digits; nature's law;
  - order reversed: 3,200 with none, 47,424 with one, 3,200 with two.
- **L:** one history at each of the 215,296 digit sets, in 5 passes. Its law is nature's sequential law: each first outcome 1/2, and each second outcome its row given the first, at the frame then set.

## 3. Part 2: random full boards

400 boards on a line of 96 sites, each with 12 births (about a third of them triples), and 0, 30, 60 or 90 percent of the detectors machines:

| depth | boards | L: passes = 1 + 2 depth | L's passes | L: layer checks, equal | J deadlocks |
| --- | --- | --- | --- | --- | --- |
| 1 | 100 | 100 | 3 | 1,200, 1,200 | 0 |
| 2 | 76 | 76 | 5 | 1,706, 1,706 | 12 |
| 3 | 162 | 162 | 7 | 4,888, 4,888 | 84 |
| 4 | 57 | 57 | 9 | 1,900, 1,900 | 40 |
| 5 | 5 | 5 | 11 | 178, 178 | 5 |

## 4. Part 3: one free slot, two quanta

- **The quanta:** A is spread over absorbers x and z (sizes 2 and 3), and B over y and z (3 and 2). Both reach z at one tick, where one slot is free.
- **The slot as sigma_b, each source drawing alone:** of 900 digit pairs, 684 have one history that agrees with itself and 216 have two.
- **The candidate:** z draws once over the joint histories' products: xy 6/19, zy 9/19, xz 4/19. That gives one history at every digit, with each quantum taken once.

## 5. What does not follow

- **The engine:** stage 9's two clicks and the runner's passes on the act's own arrays.
- **Locality:** each carry rides its twin's own path, one site a step, by construction here. The Boss's bpasses.py counts the reads (0 far).
- **The tie's rule:** a candidate is named, not ruled.
- **A loop through the backward run itself:** a setting that read the tag. The rule that every setting is a forward click, read only from takes in its past light cone, excludes it, and the probe makes none.

## Method: addressed

- **(a) Which clock or gear makes each term:**
  - each draw is law 9's at the Node-clock where the parts were one, over sigma_f sigma_b;
  - each setting is a split click of the detector's own light, or a machine's frame from a take it heard by light;
  - the passes are the runner's order of work.

  No term is declared.
- **(b) What the clicks show, the books first:**
  - every part of every birth is drawn once and taken once, on every board;
  - L's law is nature's at every layer, exactly;
  - the band with two histories, which no single Node-clock decides, appears only when a birth is drawn whole with its parts out of the cause's order.
- **(c) What does not follow, asked of the clicks:** the act's own run, and the rule for the one slot.

---
Animate, reader-5.
