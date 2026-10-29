# The eleventh hostile review: stage 7a, the one act on every gear at its coefficients (9e5233d7f)

Verdict: approve with changes, at 9e5233d7f (a fresh reader, 01:5x UTC 2026-10-29). No defect of the code was found.
One change of the tests is asked, so that they show what Sofer said he would read for. Each claim stands on a probe the
reader ran.

## Required, and where it went

1. **The run back with every divisor row away from 1.** varied() drew W and W+ from [1, 20) and T_d from [1, 9), and
   back() ran on those layouts, so W was 1 at 6 to 15 of the 240 entries of each layout and a T_d row was 1 in 4 of
   the 6: a swap of W and W+ or of T_k and T_d could hide there. The code holds it (run_back.py, case (a): 200 of 200
   single rounds exact with every W, W+ and T_d at least 2, W apart from W+, |s| and T_k at least 2, random masks and
   stopped clocks). Now varied() takes the least divisor, and back() runs at 2.

## Follow-ups, and where each went

- **W+ across rounds:** one layout runs back over several rounds only where W+ <= W; with W+ above W it ran back in
  1 of 60 cases (run_back.out, case (b)), the promise that a fine tooth lies within [0, W) broken from the second
  round. When each round's W is the last round's W+, as the lapse makes it, 60 of 60 run back (case (c)). It goes to
  7b with the promise: each tick's W is the gear's last W+, at its own ticks.
- **Broken promises fail silently** (run_back_broken.out): r = W, r = -1, r_d = T_d, r_d = -1 or tn = c + 1 at the
  start, and the run back is wrong in most cases with no error; T_d = 0 and W+ = 0 raise. 7b's load calls promises()
  on the gearing (every teeth count at least 1, the drive's tooth within [0, T_d)), as Sofer's read-for 1 asks.
- **Stage 8:** the 24's map on the state must mirror r_d to T_d - 1 - r_d on the rows it negates; with that mirror the
  whole act, not the sources alone, commutes with all 24 turns in 12 of 12 worlds (images_full_act_all.py, .out).
  Recorded for stage 8.
- **Coefficients per row:** the Gearing and the grip are stored per gear row, and the 24 hold only if a train's rows
  share theirs; the room's reason said "a grip per train". The reason and state.py's comment now say a grip per gear
  row, alike on a train's rows from 7b's load, which 7b tests.
- **The run back's order at 7b and 7c** (a lapse gear's run back needs the regulator's): a probe when the two stages
  land.
- **U_j:** the gradient, like the pull, reads the neighbour without the Mesh's turn; when U_j comes (7c, David's
  6485049535), J's gradient takes it too.
- **Wording:** load.py's two refusals now name stage 7c, and state.py, files.py and tools/tensor24_files.py name 7b.
  tests/frame.py imports the engine's records for plain() alone.
- **The records' names unpinned** (its survivors r4 and r5, two fields' names swapped): a test now pins every field of
  State, Gearing, Layout, Plan and Out in order, and both die (mutants_s12_survivors_after.out).

With the review, David's two notes of 6485049535 went in: the hand's charge Q* moves by Rule3's torques alone over
rounds whose teeth change, with J off and the hand's rows alike in W, W+, s, D and the grip (the thirteenth review
adds the kick's term with J on), its mutants a grip per end, an s that moves and the push off its stretch (OPEN 13);
and the lay makes the dial, the count and the time three arrays of their own.

## What holds

- The formula is the plan's and David's: the push s (F + T_k q), that is s F + K with K = T_k s q; (q, r_d+) =
  carry(J, T_d, r_d); p = W (a - b) + (r - home(W)), carried at W+ with home(W+).
- J's planes are side()'s: the value at 0, the gradient's three axes at 1 to 3, the force at 4; every mutant that
  breaks the order on either side dies. The gradient a(x + e) - a(x - e) as seen turns as T1 under the 24. The operand
  pull reads F = pull - D a, the plan's section 2.
- The run back: one round 200 of 200; rounds with W+ = W or below it, and rounds re-geared from the last W+, 60 of 60
  each (run_back.out). The order test with J on, every T_d at least 2 and one clock stopped: 32 of 32 schedules equal
  the synchronous pass, and all 32 run back (order_full_act.py, .out).
- Stage 4 is unchanged: 300 random worlds give the same digests at 610fef782 and 9e5233d7f under plain()'s neutral
  gearing, r_d staying 0 and every rewind exact (stage4_alike.py, .out).
- Locality and purity hold forward and backward at 240 of 240 sites with J on; a control that counts one neighbour as
  far fails at 5 to 9 of 60 (local_pure.py, local_pure_control.py).
- The gate gives refusals 0, notes 2; every fast check passes; 267 Tensor24 tests pass.
- 47 of the reader's 51 source mutants die (mutants_s12.py, its output at 9e5233d7f); of the 4 that lived, r4 and r5
  die now, and d1 (the drive's carry with r_d folded into J) and s12 (J landing on zeros of the gears' shape from b)
  are equivalent.

The probes run as `PYTHONPATH=<worktree>/src:<worktree> python -P <probe>`, mutants_s12.py as `python -I
mutants_s12.py <a worktree> <a scratch folder> [names]`; their outputs stand beside them.
