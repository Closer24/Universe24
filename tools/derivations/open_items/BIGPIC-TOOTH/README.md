# The 24 and the mirror on a moving clock: the centred tooth

Big Pic, 2026-10-30. This is the solution from above that the Boss asked for (#2187 6524720383, item 2; 6524739654,
mend 1). His page on the 24's symmetry (derive/boss/sym24, local) is NOT PASSED by its hostile mathematician. On a
moving clock, the turns that flip a sign depart by whole turns of the count from the second round, and the departure
spreads through the Meshes. The Boss's question: where does it belong, G2, a law or the act? It touches term 13, the
mirror's own condition and term 11's odd key.

The probe is tooth.py, its output tooth.txt beside it, in whole numbers alone (Rule3's carry for every division, no
float, root, circular call, random draw or fraction): `python3 tools/derivations/open_items/BIGPIC-TOOTH/tooth.py`, a
few seconds.
- Part A runs the act as main holds it (engine/step.py).
- Part B runs the same world with the centred tooth, in the probe alone. Solution24's step 8: a local run, never pushed
  as code.

**Status: DRAFTED,** for a hostile mathematician and a hostile physicist.

## The answer

- **It belongs to the act.** The cause is one representation, how a fine tooth is kept. G2 carries one condition,
  and no law changes. Law line 94 (the step commutes with each of the 24 turns, bit for bit) is broken by the act's
  tooth, not by the law, and the centred tooth restores it.
- **The cause.** The act keeps each fine tooth from 0 up, r in [0, W). A sign flip reflects it about its teeth's
  middle, W - 1 - r: the mirror's flip, and every turn that sends a row to minus a row. That middle moves with the teeth.
  - On a moving clock a tooth kept at one round's teeth is read at the next round's teeth.
  - The reflected tooth then sits off the reflection of the read one by the teeth's change.
  - A carry that lands near its edge comes out a whole count apart, and the Meshes carry the difference on.
  - Measured (part A): on a still clock all 24 turned runs are the run turned. Drifting by 1 or 2 a round, only the 3
    turns that flip no sign hold, and the others part from the first round.
- **The solution from above: the centred tooth.**
  - Keep each fine tooth counted in half teeth from its teeth's middle, s = 2 r + 1 - W, and store s itself.
  - Carry the round as 2 (W (a - b) + push) + s = 2 q W + s+, one carry at 2 W.
  - Every sign flip is then a plain negation, s -> -s, which reads no teeth.
  - On a still clock it is the act as built, state for state: 401 of 401 rounds (part B).
- **The condition, G2's: the teeth keep their parity as the clock moves.** The 00 slot's read moves W by even steps.
  - With the centred tooth, drifting by 2, all 24 turned runs hold (part B).
  - Drifting by 1, the teeth change parity every round, a remainder lands on its window's edge, and 21 turns part from
    round 8.
- **What it carries along:**
  - **the mirror's own condition** ("its own inverse only where the clock stands still"): mirrored twice is the state
    itself at every teeth, and the run back is exact on a rising clock, 400 of 400 rounds at either drift (part C). A
    falling clock's promise stands as before: no kept tooth outgrows the teeth that read it;
  - **term 11's odd key:** the same fact for the click tooth. A centred tooth that a negation keeps (s = 0) exists only
    at odd teeth (part D), which is why the books close for an odd key with one birth;
  - **term 13, the frozen clock:** the teeth grow where a clock freezes, and the parity condition holds there too;
  - **"the odd tooth":** decision 40 (h) reads it as the odd kind A2 or the odd den. Here is a third reading. The
    board's rest teeth, 6 den Gamma^2, are even for every den (part D), so every centred tooth is odd, and no state of a
    negated row is kept by its turn. The act keeps the 24, and the state's odd tooth breaks them at the grain: the law's
    "if the 24 breaks, it breaks by the state". Which reading the owner meant is his.

## 1. In clocks

- **A fine tooth** is the part of a count the dial has not yet carried. The act counts it from one end of the dial.
- **A sign flip turns the dial round,** so a tooth counted from one end is counted from the other: it reflects the
  tooth about the dial's middle.
- **When the dial grows between two rounds, its middle moves.** The reflected tooth then no longer sits where the
  turned gear's own tooth would, and once a carry is near, they part by a whole count.
- **Counted from the middle,** a turned gear's tooth is the same tooth with its sign changed, whatever the dial's size.
  This holds as long as the middle stays on the same kind of mark as the dial grows: a whole tooth for an odd dial, a
  half tooth for an even one.

## 2. In the algebra

- **The act as built:** q, r+ = carry(W (a - b) + push, W, r). Write s = 2 r + 1 - W.
  - Multiplying by 2 and taking W - 1 away gives 2 (W (a - b) + push) + s = 2 q W + s+, with s and s+ about the same W.
  - On a moving clock, the tooth kept at W_b is read at W_a, so the act's s is re-read as s + (W_b - W_a).
  - A turned row's tooth, flipped about W_b, reads -s + (W_b - W_a) where the negated one is -s - (W_b - W_a): two
    teeth apart for every tooth the clock moved.
- **The centred tooth:** store s, odd or even as W - 1 is, and carry x = 2 (W (a - b) + push) + s as
  (q, rem) = carry(x + W, 2 W, 0), s+ = rem - W, in [-W, W).
- **Negation commutes with that carry** wherever x has the parity of W - 1:
  - from x = 2 q W + s+ comes -x = 2 (-q) W + (-s+);
  - -s+ lies in [-W, W) unless s+ = -W, and s+ has the parity of W - 1, so it is never -W;
  - so the carry of -x is (-q, -s+), with no condition on x's size.
  - x keeps s's parity, so the condition is that s's parity, set when the tooth was kept, matches the reading teeth:
    the teeth keep their parity.
- **The mirror,** (a, b, s) -> (b, a, -s):
  - the tick on the mirrored state reads the same now slot, so the same W;
  - from 2 (W (a - b) + P) + s = 2 q W + s+ comes 2 (W (a - a+) + P) - s+ = 2 W (b - a) + (-s);
  - so the round runs back to (a, b, s) exactly, and mirrored twice is the identity at any W;
  - a falling clock still asks that -s lie within the reading teeth: the promise.

## 3. On the board (tooth.txt)

- **The world:** one Node-clock with no Mesh pull. Row 0 is the clock's own count c (kind A1), drifting by v a round
  with no spring, so rows 1 to 3 read W = 6 + c and their teeth move with it. Rows 1 to 3 are a family of kind T1 with
  the spring V = X . X, laid at (5, -3, 2). The small rest teeth let a remainder land on its edge often.
- **A, the act as built:**
  - at v = 0, 24 of 24 turned runs are the run turned, over 400 rounds;
  - at v = 1 and at v = 2, 3 of 24 hold (the turns with no sign), and the rest part from round 1.
- **B, the centred tooth:**
  - at v = 0 and at v = 2, 24 of 24;
  - at v = 1, 3 of 24, parting from round 8;
  - on a still clock it is the act as built in 401 of 401 rounds.
- **C, the mirror with the centred tooth:** at v = 2 and at v = 1, 400 of 400 rounds run back to their way out's
  state by the act on the mirrored state.
- **D:** a centred tooth that a negation keeps exists at the odd teeth 1, 3, 5, 7, 9 and 11, and at no even teeth. The
  example's rest teeth, 6 den Gamma^2 = 90,977,140,554,674,334,000,000, are even.

## 4. In the clicks

- **The click carries tau,** the area the push turns into a hand, which a turn keeps exactly whenever the act commutes
  with it.
  - With the act as built, on a moving clock, a turned board's clicks can part from the board's clicks turned once a
    departure reaches a carry. The 24 frames would then read different clicks, a symmetry broken by the grain and not by
    the law.
  - With the centred tooth and the parity kept, every frame reads the same clicks.
- **The vacuum's odd tooth** at even teeth breaks the 24 only at the grain, below any click: no click reads a fine tooth
  alone.

## 5. Where it belongs, and what is owed

- **The act,** for the Boss to route: the fine tooth stored centred, and the carry at 2 W. The run back and the 24 on
  a moving clock follow, and on a still clock nothing changes, state for state. It is DRAFTED until both readers pass,
  then READY for the code writer.
- **G2's condition:** the teeth keep their parity as the clock moves (the 00 slot's read moves W by even steps), with
  the law's line 94 and the mirror kept whole. OPEN: whether G2's push gives it, or the read lands at a factor of 2.
- **No law changes.** Line 94 holds once the act's tooth is centred.
- **The owner's:** which reading of "the odd tooth" he meant (decision 40 (h)).
