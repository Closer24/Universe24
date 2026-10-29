# Draft D2, verified by the Boss (2026-10-29, 05:0x UTC)

The second hand, the Boss, who did not write the draft. What was checked:

- **The five probes run again** on the engine at tensor24-review (src unchanged since 298bec5d8), each output equal
  byte for byte to the drafter's: q2_compose (0.6 s), q2_dial, q2_board, q3_wait (67 s) and q3_rest.
- **The lemmas read by hand:**
  - L1, a carry keeps a uniform remainder: for a fixed n, r -> r' is a bijection of [0, d). PROVED.
  - L2, the mixed radix is a bijection onto [0, the product). PROVED.
  - L3, the sum through the carry is uniform where one read is uniform and independent of the rest. PROVED.
  - L4, the sort maps the tuples to multisets: C(b + m - 1, m) values, 220 of 1,000 at (10, 10, 10) and 126 of 1,296
    at (6, 6, 6, 6), the plan's 0.875 and 0.9375. PROVED.
  - L5, Born's pick within one count of room, exact where the sum of the sizes divides it. PROVED.
- **The dial at a beat lies in [0, rate):** the beat's carry is ph + rate = k Gamma + ph', so where k = 1,
  ph' = ph + rate - Gamma < rate. PROVED from step.beat.

What stands as the draft says:

- **CHECKED:** the draw's bias is the sorted composition's, not the reads'. The sum through the carry is exactly
  uniform, keeps the 24's permutations of the Meshes (0 changes of 17,496), and needs no sort, no if and no bound.
- **CHECKED:** a fresh uniform draw at each beat gives geometric waiting times exactly. The dial's draws follow the
  three-gap theorem, so the decay read from the dial is periodic, not exponential.
- **OPEN:** that the fine teeth stay uniform after the first tick. This is measured (site 0 of a ring of four: 267 to 399
  against 343 at tick 13), not derived, so the draw's fairness rests on it, and a distribution test on every record is
  what reads it.
- **OPEN:** the sign flips (r -> w - 1 - r under a reflection or a half turn), which the sum does not keep.
- **OPEN:** whether c is independent of the sizes, whose gears are the ones read.
- **OPEN:** a quantum near rest. Its whether persists, so its decay is not exponential on its own reads.

For David (item 11 of DAVID-TENSOR24-THE-CLOCK-READING.md), the verdicts against his item stand as the draft's table
gives them. It confirms the residues at a coprime rate. It contradicts the dial as the draw's source: read at a beat
its room is the rate, and its successive reads are a rotation.
