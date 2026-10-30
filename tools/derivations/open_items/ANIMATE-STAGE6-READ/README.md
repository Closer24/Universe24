# Stage 6 read independently (Animate)

The Boss's ask (#2187, 6484168578): Animate's word on af564daac, 54b9e6a63 and stage 6 (83a0b214a, 3fbbd1cd0,
91226e796, 927071a14, 0ff2ae0dc), read with fc8c810ff, the head the decoder's commit picks onto.

- **probe_stage6.py** takes from the head only what it checks. The 24 are made by closing two quarter turns; A2 is
  the sign of the permutation a turn makes of the cube's four body diagonals (S4's sign); the characters are checked
  against the octahedral group's table; the multiplicities come from the characters; each of the head's 125 tables is
  checked for equivariance at all 24, for being 0 exactly off the channels, primitive with its first entry positive,
  and, where no E enters, equal to the table made here by averaging every seed over the 24. The plan is contracted on
  300 random universes against a naive sum over the coupling rows, with strengths and readings past 64 bits.
- **probe_stage6.txt,** its run at fc8c810ff: the 24 the head's weight picks, 24 of 216; the five kinds
  representations with the table's characters; 43 channels; the 125 tables with no departure; the plan's contraction
  equal to the naive sum at every universe.

The naive sum lays the readings as runner/load.py does (the value, the gradient's three planes, the pull, before and
after): the plan names the operands' order, and stage 7's readings are to be built in that layout.

---
Animate, reader-5.
