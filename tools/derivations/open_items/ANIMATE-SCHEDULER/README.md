# Rule B's scheduler on a full board: one rule for every band (Animate)

The asks:
- the Boss's 6494549592, item 4 ("The scheduler on a full board has to be sized by the depth of its chains, not three passes fixed");
- Sofer's owed line (5) of 6494833685;
- Animate's own 10.5, item 6 (every band of agreeing histories must part at one Node-clock, and the probe must look for a band that does not);
- the owner's word to Animate of 2026-10-29, 11:5x UTC (in Hebrew; in translation): "The rule must be generic.";
- Sofer's 6496692228, item 6: two places in the code told weights by kind (a spread quantum's sigma_f against a hand's, and a free setting against a machine);
- decision 40 (b), the slot rule: "a full slot refuses after the split click's draw, and the refused quantum goes back to its giver by 5.1's books line"; the Boss's 6500777188, item 4: "(b) in the scheduler".

Beside the engine. `python -I scheduler.py` runs in about 9 seconds; its output is scheduler.txt. It reuses the hands, frames and sizes of ANIMATE-B-RECORD/b_record.py.

## The answer

1. **One rule draws every band, and one rule every slot.**
   - **The band:** the parts that share a hand (one birth's twins, or one spread quantum). A slot joins no band.
   - **The draw:** each band is decided by one law-9 draw over sigma_f of its joint histories, conditional on what is drawn, at its birth, in the pass in which its sizes come in.
   - **The slot** (one absorber at one tick), by decision 40 (b): once every part that may reach it is drawn, its own law-9 draw, on its own digit and over equal weights, picks which of its arrivals it takes, as many as it has free. It refuses the rest, each back to its giver (its birth), and the run's state holds the refusal.
   - **Nothing else is typed.** No slot weighs a history, and the place of every draw is where its parts are one: a band's at its birth, a refusal's at its slot. One function draws every band and one every slot, for pairs, triples, spread quanta, the one-slot tie and a chain of ties.
2. **Each part is drawn as its setting comes back.** Where only some of one birth's parts are in, those are drawn first, over the sizes summed over the rest.
   - **This is lawful by no signal:** a subset's sizes, summed over the other parts, are the same in every frame of those parts. Every such draw was checked against every frame the parts still out could take, exactly: 9,872 checks, all equal.
   - **A spacelike pair whose settings come back in one pass is drawn at once,** as reading 15 has it.
3. **The passes are 1 + 2 times the depth of the chains of settings,** a free setting counting 1 and a machine one more than the take it heard. This held on every one of 400 random boards, at depths 1 to 5 (3 to 11 passes).
4. **Drawing each birth whole (J) is no scheduler.** Pass by pass, it deadlocks wherever a birth's setting waits, through any chain, on that birth's own outcome: on 141 of the 400 boards, and on the crossed births always.
5. **The band that no Node-clock decides, found.** Taken as a history that agrees with itself, J needs the cause's order of the parts:
   - with the heard party's sign outermost: one history at every digit, and nature's law;
   - with that order reversed: of 53,824 free frames and digits, 3,200 have no history and 3,200 have two. The two differ at both births at once, so no single Node-clock parts them.

   The one rule never meets this band, because it never draws a part before that part's setting is in.
6. **Under decision 40 (b), two independent sources stay independent at a shared absorber** (Part 3).
   - **Two quanta reaching one absorber's one free slot at one tick:** each is drawn at its own birth, so the ends drawn are the Born product: x/y 6/25, x/z 4/25, z/y 9/25 and z/z 6/25. Where both reach z, the slot takes one and refuses the other, 3/25 each way.
   - **A chain of three quanta joined by two slots:** the ends drawn are the Born product, and each contested slot splits its history's share equally.
   - **At every digit,** every quantum is drawn once and either taken or refused at the end drawn; no slot takes past its free count, and a slot refuses only when full.
   - **Withdrawn with the weighing:** the slot bands' laws (the tie's 6/19, 4/19 and 9/19; the chain's 3/10, 1/5, 1/5 and 3/10), and the 216 of 900 digit pairs with two histories when each source drew alone against sigma_b. They stand at reader-5 84e77364.
7. **Nothing is told by kind in the code either** (Sofer's item 6). Parts 1 and 2 of scheduler.txt are equal byte for byte to the code that told them apart, and stay so under decision 40 (b).
   - **sigma_f is one formula for every hand:** the Gaussian norm of the hand's whole-number overlap with its parties' ends, each end a line of its party's frame, summed over the lines the hand carries untaken. A twin's frame is its two spinors along an axis. A spread quantum's frame is its absorbers' own lines, and its hand holds at each absorber its share as a Gaussian norm over two lines no absorber here resolves (any whole share is a sum of four squares).
   - **A setting is one law-9 draw over its frames:** its own light's sizes (1 each) times, at each take it heard, the sizes its rule gives that take's end. Hearing nothing, it is free; hearing a take, its rule's sizes leave one frame (a machine); a spread quantum's setting has one frame. The depth of a chain is one formula too: each setting one more than the deepest setting whose take it heard.
8. **The withdrawn weighing signalled, and (b) closes it** (part 5). With a full slot weighing 0, the far twin's law at its frame moved with the near twin's frame (11/29 against 107/174). Under (b) it reads 1/2 at every pair of frames, with the slot and without.
9. **The tie signalled too, with no hand, and (b) closes it** (part 5). With a full slot weighing 0, A's click at x read 2/5 with B not born and 10/19 with B born, B's birth spacelike to it. Under (b) both read 2/5.
10. **The cone check reads each click, never a party's whole outcome** (part 5). Under (b), whether A is taken or refused at z moves with B's birth: taken 3/5 with B not born; taken 12/25 and refused 3/25 with B born. That is lawful, since z lies on B's birth's light cone.
    - A check that binned A's whole outcome by B's birth would name it a signal.
    - The check that bins each click by the settings outside that click's past cone names none.

    This is the form of the decoder's cone check (D8).

## 1. The board

- **A line of Node-clocks;** light runs one site a tick.
- **Births:** a birth lays a pair (the shared hand e1 x e2 - e2 x e1), a triple (e1 x e1 x e1 + e2 x e2 x e2), or one quantum spread over absorbers.
- **Takes:** each twin rides one site a tick to its detector and waits there 0 to 3 ticks; its take is a whole click.
- **Settings:** each part's setting is a split click one tick before its take, one law-9 draw over its frames: its own light's sizes times the sizes its rule gives each take it heard by light, strictly inside its past light cone. A setting that hears nothing is free; one that hears a take is a machine.
- **Slots:** a slot is one absorber at one tick, with a free count. It draws once every part that may reach it is drawn, takes as many of its arrivals as it has free, and refuses the rest, back to their givers.
- **The sizes:** sigma_f is the Gaussian norm of the hand's whole-number overlap with its parties' ends (a twin's spinors along its frame; an absorber's own line), summed over the lines the hand carries untaken. sigma_b, an absorber's free slots, is alike in every history and weighs none: a slot's free count is the size of its own draw. Every draw is law 9's, the rank count of a digit over the running sums.

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

Parts 1 and 2 give the same numbers through the one rule's code as through the first, pair-only code (reader-5 325440ef), and through decision 40 (b)'s.

## 4. Part 3: quanta at absorbers' free slots, under decision 40 (b)

Every draw is the one rule's, by the same functions as Parts 1 and 2: each quantum at its own birth over sigma_f, and each slot, its arrivals all drawn, over equal weights.
- **A alone,** over x and z (sizes 2 and 3): its band is its own birth, so x 2/5 and z 3/5, Born.
- **A and B**, B over y and z (sizes 3 and 2), both reaching z at one tick, where one slot is free:
  - the ends drawn: A at x and B at y 6/25, A at x and B at z 4/25, A at z and B at y 9/25, both at z 6/25. This is the Born product;
  - where both reach z, the slot's own draw takes one: A taken and B refused 3/25, B taken and A refused 3/25.
- **A chain:** A over x and z (2 and 3), B over z and z2 (2 and 2), C over z2 and w (3 and 2), with one slot free at z and one at z2.
  - The ends drawn are the Born product: x/z/z2 3/25, x/z/w 2/25, x/z2/z2 3/25, x/z2/w 2/25, z/z/z2 9/50, z/z/w 3/25, z/z2/z2 9/50 and z/z2/w 3/25.
  - Each contested slot splits its history's share equally: x/z2/z2 into 3/50 and 3/50 at z2, z/z/z2 into 9/100 and 9/100 at z, z/z/w into 3/50 and 3/50 at z, and z/z2/z2 into 9/100 and 9/100 at z2.

At every digit, every quantum is drawn once and either taken or refused at the end drawn, no slot takes past its free count, and a slot refuses only when full.

**Withdrawn with the weighing** (they stand at reader-5 84e77364):
- with a full slot weighing 0, the one rule joined A and B into one band at z. Its law was 6/19, 4/19 and 9/19, both at z weighing 0;
- the chain was one band: 3/10, 1/5, 1/5 and 3/10;
- each source drawing alone against sigma_b left 216 of 900 digit pairs with two histories.

## 5. A band joined by a hand and a slot at once: the withdrawn weighing signalled, and (b) closes it (hand_slot.py)

The Boss's hunt of 13:55 UTC asks it of the record and the clicks. `python -I hand_slot.py` runs in under a second; its output is hand_slot.txt. It runs run() under (b), and computes the withdrawn weighing beside it from band_weights, as the contrast.

- **The board:**
  - a pair at site 50 (tick 5). Its near twin meets a two-way detector, + taken at site 45 and - at site 55, both at tick 10. Its far twin is taken at site 100 at tick 55, outside the near setting's future cone;
  - a spread quantum reaches x (site 75) or site 55 at tick 10, shares 1 and 1;
  - site 55 has one free slot at that tick.
- **Under the withdrawn weighing** (a full slot weighs 0), the hand and the slot joined the three parts into one band, drawn once at the slot. The far twin's + share at b moved with the near twin's frame a:
  - at b = (20, 0, 21)/29: 11/29 at a = z, and 67/174 at a = x;
  - at b = (-20, 0, 21)/29: 11/29 at a = z, and 107/174 at a = x.

  The near setting was read at the far take, outside its future cone: a signal. In closed form the far twin's + share is (3 - a.b)/6.
  - **The cause:** the zero weight removed the histories in which the near twin's - and the quantum share the slot, and the draw renormalized over the rest. That is a post-selection on a near event correlated with the near twin's sign, and through the hand it reached the far twin.
  - **Why the 9,872 checks missed it:** they check every band drawn at a birth, as its settings come in. A band joined by a slot was drawn at the slot, and the code checked none there. Part 3's slot bands held no hand, so no signal could show in them.
- **Under (b):** the pair is drawn at its birth and the quantum at its own; the slot then takes one of its two arrivals and refuses the other.
  - The far twin's + share is 1/2 at every pair of frames, with the slot and without; the near twin's drawn + share is 1/2.
  - The slot refuses the near twin 1/8 of the time and the quantum 1/8, at every pair of frames, and never takes past its free count.
  - No history is removed, so the hand's law is untouched and no signal can arise. Drawing the hand before the slot would also have closed it, but that tells a hand from a slot by kind, which decision 38 forbids; (b) needs no such telling.
- **The tie of Part 3, with no hand** (hand_slot.txt, its second part):
  - under the withdrawn weighing, A's click at x read 2/5 with B not born and 10/19 with B born at site 30. B's birth is spacelike to A's take at x (site 4, tick 6), so whether B's source emits was read at A's absorber;
  - under (b), A's click at x reads 2/5 either way;
  - A at z (site 20, tick 10) is taken 3/5 with B not born, and taken 12/25 and refused 3/25 with B born. This moves with B's birth lawfully, since z lies on B's birth's light cone (10 sites in 10 ticks). So the cone check reads each click by the settings outside that click's past cone (D8), never a party's whole outcome.

## 6. What does not follow

- **The engine:** stage 9's two clicks and the runner's passes on the act's own arrays; (b) on the act, where the run back tells a refusal from a take by the state, never by the log (the Boss's, at G5).
- **The way back to the giver** (5.1's books line): its path and its tick are the engine's. Here the run's state holds each refusal and names its giver.
- **Locality:** each carry rides its part's own path, one site a step, by construction here. The Boss's bpasses.py counts the reads (0 far).
- **A machine whose heard take a slot refused:** no board here holds one. A refused part makes no take, and a machine's rule gives sizes only at a take's two ends; its sizes where no take came are to state before a board holds one.
- **A loop through the backward run itself,** a setting that read the tag. The rule that every setting is a forward click, read only from takes in its past light cone, excludes it, and the probe makes none.

## Method: addressed

- **(a) Which clock or gear makes each term:**
  - each band's draw is law 9's over sigma_f, at its birth;
  - each slot's draw is law 9's over equal weights, at its slot, on its own digit;
  - each setting is a law-9 draw of the detector's own light, over its own sizes times its rule's at each take it heard by light;
  - the passes are the runner's order of work.

  No term is declared: no slot weighs a history, the place of a draw is where its parts are one, and sigma_f is one formula for every hand.
- **(b) What the clicks show, the books first:**
  - every part of every band is drawn once, and either taken or refused at the end drawn, on every board and at every digit; no slot takes past its free count;
  - the law is nature's at every layer, exactly, and the Born product over independent sources at a shared slot;
  - the far twin's click reads 1/2 at every near frame, the near twin's 1/2 at every far frame, and the slot's refusals 1/8 at every pair of frames; A's click at x reads 2/5 with B and without;
  - two histories that no single Node-clock parts appear only when a birth is drawn whole out of the cause's order.
- **(c) What does not follow, asked of the clicks:** the act's own run under (b), the way back to the giver, and a machine whose heard take a slot refused (part 6).

---
Animate, reader-5.
