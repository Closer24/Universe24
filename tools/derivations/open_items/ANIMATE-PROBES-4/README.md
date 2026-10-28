# Animate's toys for the clocks' roots (the owner's word of 2026-10-28, 15:2x UTC)

The page is ANIMATE-CLOCK-ROOTS.md. These are toys that check whether a law would work in an engine. Nothing here is engine code, and nothing was pushed to an engine branch. Both run with no engine: `python -I local_tick.py` and `python -I kind_kept.py` (the second reads ANIMATE-PROBES-2/kinds_ladder.py and ANIMATE-PROBES-3/ladder_pauli.py).

## local_tick.py: law A, a clock's time is the carry of its own dial

- **The board:** a ring of 60 clocks in exact rationals, each a hand of two slots stepped by the one formula with the coupling c d^2, d its own tick. A patch of 20 clocks asks for c = 27/25, past the light cone at c = 1.
- **The reads:** every clock reads its neighbours where they stand at its own moment.
- **Four runs of one pulse:** one tick for all; the clamp; the local tick (the patch's clocks tick twice per great tick); every clock at half a tick (the reference).
- **The output (local_tick.txt):**
  - one tick for all grows past 10^6 by tick 48;
  - the clamp holds, with the patch's light held to the full rate;
  - the local tick holds, its front reaches the probe a tick sooner, and the rewind is exact over 9,600 events.

## kind_kept.py: law C, every carry keeps the kind, and the ladder by the light's family

- **The lays under the 24's lifts** (24 classes closed from three generators): the head's (the up twin at one end, the down at the other), the singlet and the vector lay along the Mesh.
- **The children's own states.**
- **The ladder per bang** from four calibres: the light A1 or T1, each with and without the twin hands.
- **The output (kind_kept.txt):**
  - the head's lay keeps the 24 at 12 of 72 cases, the singlet and the vector at 72 of 72;
  - a child is S = (0, 0, 1) under the head's lay and S = 0 under the other two;
  - the light A1 alone stays at A1, and the light T1 alone reaches the 24's five kinds by bang 3;
  - with the twin hands all eight kinds stand at bang 4 (A1 light) or 3 (T1 light).

---
Animate, reader-5.
