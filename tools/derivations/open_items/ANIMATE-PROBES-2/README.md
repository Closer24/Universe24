# Animate's probe of the 24's ladder (kinds_ladder.py)

Nothing here is engine code. ladder_pauli.py (ANIMATE-PROBES-3) reads its kinds from here.

## kinds_ladder.py: the 24's ladder, bang by bang

- **Pure integers, no engine:** `python kinds_ladder.py`. The eight kinds of 2O are given by their characters in Z[sqrt 2]; every multiplicity is the class sum over 48, an integer. It reads:
  - the table's orthonormality;
  - the ladder from the one big bang's calibre (all A1);
  - the ladder with the twin hands beside them, each bang fusing every pair of kinds present, and the slower one, each bang adding one twin hand;
  - the tensor powers of E1/2 to n = 8;
  - every kind's exchange sign;
  - two mutants.
- **The output:** kinds_ladder.txt.
  - The orthonormality fails at 0 pairs.
  - The ladder from A1 stays at A1.
  - With E1/2 the eight kinds stand at bang 4, or at bang 6 one twin hand at a time.
  - The exchange sign is +1 on the 24's own kinds and -1 on the spinor kinds.
  - The mutants fail.

---
Animate, reader-5.
