# ANIMATE-UNCERTAINTY: the uncertainty principle on Tensor24's board, with no law of its own

The owner's word to Animate (2026-10-30, 03:1x UTC, in Hebrew; in translation, his first person plural rendered
without a person): "Summarize, then, how it all connects, and how uncertainty follows from the board with no
specific law. Explain each step by its logic and check it." It closed his questions of the same hour: is a click
the meeting of the past and the future, a shadow; do two Node-clocks hold one event, the one as past and the
other as present, reversed; does the future exist.

Run: `python -I tools/derivations/open_items/ANIMATE-UNCERTAINTY/uncertainty.py` (a few seconds; the output is
uncertainty.txt). Whole numbers only: no root, no float, no table. A motion's turn-sum is held as a polynomial in
the board's turn and read as 0 or not by its exact remainder.

## 1. How it connects

- **The board:** Node-clocks on a board that wraps, each reading its six neighbours alone, each round once
  (decision 42). A gear holds two moments, now and before. The run is fixed by the files and the seeds, and it
  runs back exactly.
- **A click** (stage G5): one quantum laid at one Node-clock and taken at another. The books hold it twice,
  reversed: laid at the giver, taken at the taker. Run back, the taker gives and the giver takes. So a click lies
  on the Mesh between two Node-clocks: the two answers to "where", before the step and after it.
- **The decoder** reads clicks and counts, never a formula: a clock's own count is proper time, a lay and its take
  a light line, an echo a distance (6513794974).
- **Uncertainty** follows from the same three things, the Node-clock, the Mesh and the round, with nothing added.

## 2. The steps, each with its check

| Step | Its logic | Its check |
|---|---|---|
| 1. A place is a Node-clock | a click stands at one site | the click lines carry one site (record/schema.py: Whole and Split) |
| 2. A motion is a step | a gear's motion is its now less its before; its force is its neighbours' differences | part 1, item 3: every round's before slot is the last round's now slot; engine/step.py, gear and sources |
| 3. Six neighbours, a wrapped board, one Mesh a round | the board's own Meshes | part 1, items 1 and 2: 64 Node-clocks, six neighbours each, all different, each Mesh read both ways, every neighbour one Mesh away across the wrap; over 60 rounds nothing touched farther than one Mesh a round |
| 4. A step changes the place | a wave at one Node-clock, stepped, stands at a neighbour, never at itself | part 1, item 2: one laid gear touches its own Node-clock and its six neighbours in round 1, the six alike |
| 5. The board's motions | a motion is a pattern a step leaves as itself, turned alike at every Node-clock; a board has as many as it has Node-clocks, and every wave is made of them in one way | the exact turn-sums of parts 2 and 3 |
| 6. One Node-clock holds every motion | stepped, it is never itself, so no single motion makes it | part 3: one Node-clock holds 64 motions of 64 |
| 7. One motion fills the board | stepped, it is itself turned alike everywhere, so its size is alike at every Node-clock | part 3: the whole board alike holds 1 motion; the wave 1 0 -1 0 along z holds 32 Node-clocks and 2 motions (a wave of whole numbers holds a motion with its reverse) |
| 8. The trade-off, counted | the Node-clocks a wave holds times the motions it holds are never fewer than the board's Node-clocks | part 2: every wave of -1, 0 and 1 on rings of 2 to 10, the least exactly the ring; part 3: 3,000 drawn waves on each of two boards, the least exactly the board; a line, a plane and every other Node-clock of a line sit at the bound |
| 9. The click | the draw puts the place at one Node-clock; by step 6 every motion is then open, and the next step goes any of the six ways | part 1, item 2 (the six neighbours alike); the draw over sizes stands in ANIMATE-SCHEDULER, run again at this push and equal byte for byte (scheduler.txt, hand_slot.txt, cone_read.txt) |
| 10. The same in time | a beat is a motion in time; a click at one round holds every beat | part 1, item 5: the laid gear's beat repeats every 6 rounds; on its ring of 6 rounds it holds 4 rounds and 2 beats; a click at one round holds 6 beats of 6 |
| 11. The future stands, and is not read from inside | the run is fixed and runs back exactly; a Node-clock sees its neighbours as they were a round before, one Mesh a round | part 1, item 4: 60 rounds run back slot for slot; part 1, item 2 |

## 3. What follows

- **Uncertainty is two things, and neither is a law of its own:**
  - **in the wave** (steps 4 to 8): no wave is sharp both in its Node-clock and in its motion, since the step that
    is the motion moves the place. On a board of N Node-clocks the count is exact: the Node-clocks a wave holds
    times the motions it holds, at least N. This is the uncertainty principle in counts, with no constant and no
    formula: Donoho and Stark's theorem (1989) on any wrapped board, checked here exactly;
  - **in what is known from inside** (step 11): the next click is fixed, but no Node-clock holds it, and what decides
    it reaches a Node-clock one Mesh a round. From inside it is a draw with the rule's shares; on the record, from
    outside, the past and the future both stand.
- **The past is read exactly:** the two Node-clocks of a click hold where the quantum came from and where it went
  (Heisenberg's own remark: the uncertainty relation does not hold for the past). The next step is open until the
  next click.

## 4. What does not follow, and is not checked here

- **A travelling wave on the engine:** the example board's gear stays at its Node-clock; its neighbours' fine teeth
  move and never carry. The trade-off is checked on the board's own grid and on the engine's own start; a file that
  lays a travelling wave is the Boss's.
- **The click on the engine** (G5) **and the slit** (bodies, G6): the draw over sizes stands in the scheduler model
  alone. The slit is the reading on clicks: the narrower the slit, the wider the clicks on a far screen.
- **Planck's constant in the textbook's units:** the count needs none; the units would need a Mesh in metres, which
  the board does not hold.
