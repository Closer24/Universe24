# Animate's probes, kept with their outputs (the derivation protocol's step 3)

Every probe runs on the head's engine code (834cfd72e; src unchanged through 55a3483e) or on a scratch copy of it with one line changed, named below. Nothing here is engine code, and nothing was pushed to an engine branch.

## 1. The one big bang's course and the cap F1 (ANIMATE-TENSOR24-READINGS.md, part A)

- **The worlds:** tests/worlds/world_bang.json with its universe_bang.json, the side 4; the lay's quanta varied (5,000,000 the setting's; 500,000; 50,000; 5,000; 2,000; 1,000; 800; 760; 700; 500; 50), and once with one quantum laid at [0, 0, 0] on row 1 beside 500.
- **The one-line change** for "F1 removed", in a scratch copy of src/event_universe/tick.py, line 255:

      numerators = [np.minimum(np.maximum(drive, -hold), hold)]   # the head
      numerators = [drive]                                        # the probe

- **The command:** `PYTHONPATH=<src> python -m event_universe.run <world.json> <out.json> back 20`.
- **The output:** bang_course.txt, per run: the turnovers (tick, Node-clocks), the births, the rewind, the mean stretch and its spread per tick.

## 2. The draw's composition (the mathematician's item 4)

- **draw_count.py** wraps draw.vernier from outside (bobs.vernier and click.vernier rebound to a counting wrapper) and runs a world: `PYTHONPATH=<src> python draw_count.py <world.json> <out.json> <label>`. It prints the draws, the count with c below half the room, the octiles of c over the room, and the rooms' bit lengths.
- **The one-line change** for "unsorted", in a scratch copy of src/event_universe/draw.py, line 50:

      for d, b in sorted(digits):   # the head
      for d, b in digits:           # the probe: the digits in their read order

- **The output:** draw_counts.txt (the hole and the chiral at 120 ticks, the one big bang at 250, each sorted and unsorted).
- **compare_rows.py** compares the sixteen records' readings of two runs: `python compare_rows.py <old dir> <new dir> [record ...]`. Its output for the head against the unsorted draw is rows_moved_unsorted.txt.

## 3. The teeth counts' parity (the owner's word of 2026-10-28, 10:5x UTC: teeth with no restriction of even or odd)

- **parity.py,** pure integers with no engine: `python parity.py`. For every teeth count from 8 to 15 it checks four things:
  - the engine's one mirror (acts.mirror: the fine tooth r to (mid + mid - r) mod w, the carry dropped, with the two slots exchanged) as an involution, and whether it turns the stride P = w (now - before) + r - mid to -P;
  - Rule3's rounding at the mid tooth, q(p) = (p + mid) div w, against q(-p) = -q(p);
  - two candidates that hold at any teeth count: the mirror with its carry kept in the stride (the slots exchanged, the stride -d + c), and the rounding with an exact tie sent to the even quotient.
- **The output:** parity.txt.
  - At every even count the mirror misses -P at the fine tooth 0, by w, and the rounding breaks at the ties: 10 of 101 at w = 10.
  - At every odd count both hold.
  - The two candidates hold at every count, even and odd.

---
Animate, reader-5.
