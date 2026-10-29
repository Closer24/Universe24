# Draft D1, verified by the Boss (2026-10-29, 05:3x UTC)

The second hand, the Boss, who did not write the draft. What was checked:

- **The nine probes run again** on a clean worktree at a64a60444, each output equal byte for byte to the drafter's:
  p1 (6 s), p2 (24 s), p3 (173 s), p4, p5, p6, p7, p8 and p9.
  - p5 runs at 16 worlds and 6,000 ticks by its own default. Its saved output is the run at `12 4000`, which repeats
    exactly. At the default the bound holds at 90,265 of 90,265 ticks, the wind reaches 3,039 per mille of its start,
    and seed 3 returns to its start after 5,936 ticks.
  - The probes read 7a's Layout of seven fields, so they run on the engine at a64a60444 and earlier.
- **The derivations read by hand:**
  - The wind's change, E(a+, a) - E(a, b) = (a+ - b) . (s T_k q - (r+ - r)), follows from the gear's carry at
    W = W+ in three lines, K being symmetric where each Mesh holds one grip. PROVED.
  - The local law, with the flux Phi(i -> j) = (s / 2) g (a_i - a_j) [(a+_i - b_i) + (a+_j - b_j)], is antisymmetric
    by its two factors. PROVED.
  - No polynomial invariant where s K is invertible mod W: the residues reach every fine tooth, so a kept polynomial is
    a function of a + r / W, which the step's linear part and its translations reduce to a constant. CHECKED by p2's
    exact nullspace; the step from "dense cosets" to one polynomial P is the argument's one compressed line, read as
    sound.
  - The drift bound, by the triangle inequality on the norm sqrt E where E is positive definite. PROVED.
  - At 7b's rest gearing (W = 2T, s = 2), the act is (T, 1) with the fine tooth's parity kept for ever. PROVED, by the
    common factor (p18's map), and CHECKED by p7.

What stands as the draft says:

- **PROVED and CHECKED:** the gear's and the drive's carries keep their wholes; the wind moves by exactly the click's
  work and the fine teeth's defect, locally with an antisymmetric flux through every Mesh.
- **PROVED:** no exact energy for W of 2 or more (with s K invertible mod W); the wind with its booked defect is the
  only kept form.
- **OPEN:** the asynchronous beat, W != W+, a bound uniform in time, a cubic coupling's energy books, and the wobble
  against one winding on the head's trains.

Question 1's notes are input to David's items 5 and 6, and David derives them (#2187 6488418223, item 5).
