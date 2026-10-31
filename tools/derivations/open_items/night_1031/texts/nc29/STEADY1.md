# STEADY1: the push-back for term 11's passing, and the held hand's runaway (node-live 1919dd64c)

## Verdict first

- **Term 11's push-back is not built.** The exact form, "the hands take the booked quanta", is not lawful in the
  act's operations: delivering the booked quanta as work into a hand needs a quotient by that hand's own motion.
  DERIVED, OPEN as an act.
- **It cannot stop the held hand's runaway as a bounded correction.** On unturned edge teeth the push-back moves less
  than one key per edge per round, and less than one key over the whole run (DERIVED). The runaway is a row leaving
  the act's own stability window: the held rows first leave it at round 740, and once both kinds of row are outside,
  the counts grow from 7 bits to 223 bits in 5 rounds (MEASURED, a clock fact). No push-back bounded by one key
  can hold that, and holding a row inside its window would be a bound, which the act may not hold.
- **One quantum per meeting is not brought nearer** (DERIVED). Before any push-back could act, the pair and click
  worlds already pass 5 keys at a place in round 1, and the mesh world 80000 at its first click, round 21.
- **No rate was made steady.** No push-back was built, so none was measured.
- **The runaway's road** stays writer B's NOT_CLOSED 37: the lay's held pair inside the window by the structure,
  never by a chosen strength.

## 1. The push-back for term 11, derived in the engine's terms

- **On each edge e = (a, b)** the act carries the passing P_e at the key K on the edge's two complementary teeth:
  q_e, r_e+ = carry(P_e, K, r_e). So q_e K = P_e + (r_e - r_e+) exactly (the carry's law). The booked quanta and the
  swept area P_e differ by the tooth's change, d_e = r_e - r_e+, with |d_e| < K.
  - Summed over a run this telescopes: K SUM q_e = SUM P_e + r_e(0) - r_e(end). So the booked quanta track the swept
    area within one key over the whole run, on every edge (DERIVED).
- **What leaves one side enters the other.** For the hands to answer to the booked quanta instead of the swept area,
  side a's hands must take d_e more work this round and side b's hands give d_e. That is zero-sum on the edge. The
  push-back moves gears only, no tooth, so the books on the edge teeth stay closed (DERIVED, from NC29b's carry law).
- **Which gears and by how much.** In the work form, a push p_i on leg i over the window does the work
  p_i (a+_i - b_i).
  - To deliver d_e exactly, the pushes on the edge's legs must satisfy SUM p_i (a+_i - b_i) = d_e. Any form solves it
    only by a quotient by the legs' own window displacement or push, e.g. p_i = d_e (a+_i - b_i) / SUM (a+ - b)^2.
    Where the legs stand still, that is a quotient by 0.
  - Kept whole, it is a quotient by a state-dependent number (an INDICATOR quotient, or carry(x, x x + 1, 0) in
    disguise), or a pick among the solutions of a linear Diophantine equation. All of these are refused by the laws.
  - The same holds for delivering the quanta into a momentum: an energy step of d on a hand moving at v needs a
    momentum step of d / v.
  - So no gear move of exactly the booked quanta exists in the act's operations: DERIVED (an obstruction). The lawful
    push-back is OPEN, and I built none rather than pick one.
- **What a lawful push-back must keep, if one is found:**
  - zero-sum on every edge;
  - odd under the window's reversal, so that the mirror, with the click tooth kept, undoes it;
  - the 24: a row's negation complements that edge's teeth, so the push-back must flip with the passing;
  - every number from the structure, and no new strength (the owner's 03:5x word).

## 2. Checks (what stands without a built push-back)

- **The run back:** exact on the edge form with no push-back: pair 764 of 764, mesh 125 of 125, click window 200 of
  200 (NC29b). It was not run with a push-back, since none was built.
- **The books on the edge teeth:** closed at every place (NC29b). A zero-sum push-back on gears moves no tooth, so
  they would stay closed (DERIVED).
- **The 24:** not run.

## 3. Measured: the runaway's cause (the board's clock facts, no click reading)

The probes window.py and energy.py run the engine's own act; the passing moves no gear, so these are the board's own.

- **Each row's stiffness against the act's window.** kappa = d2V/dx2 at the now slot, from J's potential's live
  monomials. The act's step obeys a+ - 2a + b = push / W, so a row is stable only while kappa < 4 W, the docstring's
  window 0 < 2 spring < 4 W.
- **The pair world (the run test's own world, 1260 ticks):**
  - at the lay the held rows' stiffness reads 181 permille of 4 W and the tied rows' 0;
  - through round 739 every row stays inside the window. The held rows read 128 to 460 permille at the rounds
    sampled every 50, the counts stay within 3 to 6 bits, and 4E stays within 8.7 10^6 to 7.4 10^7 through round 700;
  - the first crossing is the held rows at round 740 (1019 permille), outside through round 744 (1131 at round 743).
    By round 750, 4E is 2.5 10^10. The tied rows reach 2592 at round 760, and the held rows 43293 at round 761;
  - the counts then go from 7 bits at round 760 to 223 bits at round 765, and the run tool names round 766;
  - so the runaway is the act's step outside its window. The stiffness grows with the counts' squares, so it feeds
    itself;
  - two runs each of window.py and energy.py, byte for byte alike.
- **The click world:** the held rows read 163 permille of 4 W at the lay and 187 at round 100, inside the window (100
  rounds read, two runs alike). Its runaway round is writer B's 3752. My earlier length run reached round 2854 with
  no departure (NC29b).
- **The bound against the runaway.** Between rounds 760 and 765 the pair world's counts gain about 40 bits a round.
  Term 11's push-back moves less than one key a round, and the pair world's key is 1,843,203. So once a row leaves
  the window, no bounded push-back can stop it. Before that it could only keep the rows inside the window by holding
  a bound on the hands, which the act may not hold (DERIVED, from the measured growth).

## 4. One quantum per meeting, and a steady rate

- **One quantum:** the edge passes |q| = 5 at round 1 on the pair and click worlds, and 80000 on the mesh world at its
  first click, round 21 (NC29b). That is before any push-back can act, so the passing's size at the lay is P / K. A
  push-back of under one key cannot make a place's passing one quantum: DERIVED, not nearer.
- **A steady rate:** no world's rate is steady without a push-back (NC29b), and no push-back was built to measure.

## 5. Where term 11's push-back and THIRD6's must agree

- **The same teeth.** Term 11 carries the edge teeth unturned, and the third click turns them (Big Pic, 6538736766
  item 2 (b)). The push-back must read the booked quanta on those same teeth, so that both sit on one carry law.
- **The same delivery.** Both push the booked quanta back into hands. The obstruction in section 1, a quotient by
  the hand's own motion, applies to THIRD6's push-back too, if it moves the board's gears.
  - If THIRD6's "pair's hand" is a dial of teeth of its own, "pushed back to the first outcome", then it moves teeth,
    not gears. The board's hands and the clicks then still drift apart: G5's open part, item 5 (5).
  - The two must agree on which of these the push-back moves.
- **Zero-sum per edge, odd under reversal, and complemented under a row's negation,** for both.
- **The size.** Under the turned tooth the quanta wander from the swept area (item 3 (7)), so d_e is no longer
  bounded by one key per run. The bound used in section 3 holds for term 11 alone.

## Statuses

- **DERIVED:**
  - the push-back's size, d_e = r_e - r_e+, under one key a round and under one key over the run;
  - it is zero-sum on each edge, and the edge books stay closed under it;
  - the obstruction: no lawful exact delivery into the gears;
  - it cannot reach one quantum per meeting;
  - no bounded push-back holds a row past the window.
- **MEASURED (board clock facts):**
  - the window crossings at rounds 744, 760 and 761, and the counts from 7 to 223 bits in rounds 760 to 765 on the
    pair world;
  - the click world inside its window through round 100;
  - every probe run twice, byte for byte alike.
- **OPEN:**
  - a lawful push-back form;
  - the runaway's road (NOT_CLOSED 37);
  - the 24 with a push-back;
  - a steady rate.

Files: STEADY1.md, window.py, window_tail.py, energy.py, rec3/ (pair_window_1/2, pair_energy_1/2, click_window_1/2).
