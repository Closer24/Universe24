# The hostile mathematician's fourth report: FAMILIES4.md against item A (spin 1/2's phase)

Reader as before, 2026-10-30, for the Boss. Read: FAMILIES4.md whole, the note added to FAMILIES.md (line 104), NOTES.md's
new tail, the revised probe_click.py, probe_pauli3.py, probe_induced.py with their outputs. Rerun into
fam_math/rerun/r4/ with the worktree's .venv/bin/python -I -B: probe_click and probe_pauli3 byte-identical (2 s, 23 s);
probe_induced see the last line. My checks: p8_fourth.py/.txt (whole numbers, the carry the one division), on top of
p7 (REPORT3).

## VERDICT on FAMILIES4, item A: CLOSED

The finding is confirmed in the text's own words and numbers (right-zeta the Galois twist, +zeta on E1/2 and -zeta on
E5/2; det(1, zeta) = 0 over the ring while D(1, zeta) is the whole room; the ring's line rank 4, the I-line rank 2), the
third text's "either way" and the first text's "phase zeta^k" are declared wrong as written, and the group is chosen
with its reason: U(1)_I. My numbers (p8_fourth.txt 1), on Lambda's Gaussian basis (1, j) Z[zeta_8]: of the right 48, 16
keep that lattice (the binary dihedral <zeta, j>; the other 32 send it off itself, as the left 32 do), all 16 signed
permutations; 8 commute with I = right i (the powers of zeta); 4 lie in the real span of 1 and I, the phases on both
Galois halves alike: +-1, +-i; 16 keep D (I's normalizer). So U(1)_I's lattice points among the hand's own turns are
+-1, +-i, zeta^odd commutes with I but is no phase, "one state" is the I-line (rank 2, p7: D = 0 exactly there), and D is
its reading. The reasons given (a phase on both halves alike; a signed permutation that rides the carry; the group the
contraction's rule names) are each true as stated. B (one state relative to the phase named; 16 of 48; forced for G3/2)
and C (the partner's key reaches an empty taker only; 1 key in 3,000 rounds; "two per orbital by a partner's giver"
struck) are folded with my numbers quoted exactly.

## New items

### a. MINOR. The correction is a note at the head; the corrected sentences still stand below it.

FAMILIES.md line 104 carries the note, and line 108 still reads "the hand's own phase, its winding, is right
multiplication by zeta^k, which commutes with the 48 on the left"; probe_spinor 3's printed gloss ("the hand's own phase
(its winding) is right multiplication by zeta^k") and probe_pair 2's docstring say the same, unchanged (their outputs are
unchanged, so nothing to rerun). A reader who skips the note reads the old claim. Fix: bracket or strike the sentence
itself and the two probes' lines (one line each).

### b. MINOR (the theorem of section 2, my glance): the algebra is right as far as it goes; its hypothesis H2 does not do the work the conclusion needs.

Right: under H1 "two quanta of one state" at a Node-clock is the lay 2 phi (one hand), so any click that is a function
of the Node-clock's state gives the same quotients on "two quanta" and on "double size" (they are one state), and a
refusal that acts (H3) is then a step function of the hand's size. Not right as written: H2 ("through Rule3's carries,
with no comparison and no register beyond the law's remainders") does not exclude such a step. A cap is one carry, the
engine's own lit (algebra/carry.py): for term 11's count q >= 0, min(q, 1) = lit(q), and the keys refused are q - lit(q)
(p8_fourth.txt 3: areas 0..150 at the key 21 give the counts 0, 0, 1, 1, 2, 2, 3, 4, 5, 6, 7 and the capped counts 0, 0,
1, 1, 1, 1, 1, 1, 1, 1, 1); the loader's sign test is carries too (load.tables). What forbids the cap is the declared
count in it (the cap's 1: a number in the code, line 35; the declared refusal of probe_act 4 that the first text named
the fake), not that a carry cannot compare: it compares by its teeth. Fix: the dichotomy should read "no click refuses a
second half-speed quantum on an occupied line without a second hand or a declared cap", and H2 should name the ban on a
declared count rather than on comparison. Also "the act evolves the two alike (exactly up to the rounding, probe_pauli3
2 and 3 ...)": the two lays are one lay, so exactly alike; the cited 21 and 0 thousandths are two separated lays
meeting, a different statement (N2 again). One line.

### Reproduction

probe_click and probe_pauli3 rerun byte-identical (the meeting form 4 to 5 thousandths at every count 1..7 for G3/2 and
light alike; part 3 relaid within the width: free act 20 / 995 / 451 with the part outside spin 1/2 at 1 to 5
thousandths, the train's table 689 / 941 / 851 with the leak 758 / 457 / 367). probe_induced: see below.

- probe_induced rerun: see the last line of the task output (identical / differs) appended below.
probe_induced exit 0
probe_induced: rerun identical
