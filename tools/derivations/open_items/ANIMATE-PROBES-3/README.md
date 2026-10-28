# Animate's toys for the plan: the twin hands, the time gear's carry and the 24's ladder under Pauli's rule

The page is ANIMATE-TWIN-TOY.md. These are toys that check whether a piece would work in an engine (the owner's words of 2026-10-28, 13:3x UTC; the Boss's 6470415933). Nothing here is engine code, and nothing was pushed to an engine branch.

## many_bangs.py: the toy on a scratch engine

- **The tree:** engine-5.0-test at 33d9ecaa, with draft C's drives.py and course.py beside this harness, as in ANIMATE-PROBES-2. Run `python -I many_bangs.py <the tree> <variant> <quanta> <ticks> [<rewind n> <rewind from> ...]`.
- **The variant `dial`** is law 11 at the time gear in Sofer's shape (6469988450, item 1):
  - q = carries(X - Gamma, X_c - Gamma), read once by the core's carry;
  - the turnover is T applied q times, by the carry of q by 2 and by 4;
  - it is written as the blend new = old + s (T old - old), with s the carry's remainder, so there is no comparison, no branch and no mask;
  - backward it is T applied -q times;
  - BH-S1 is struck everywhere.
- **T on every hand is J K,** one formula for every family. J is a row of the kind table: 1 on an A1 hand, [[0, -1], [1, 0]] on the twin pair. T T = J J is the kind's sign.
- **Its settings, by environment variable:**
  - TWIN=k puts a row of twin hands in the calibre at the pair of the file's k-th row;
  - READ=step (the step's output, not written) or READ=start (the tick's start) is where q is read;
  - TWIN_T=K puts the head's K on the twins in place of J K;
  - FORM=hybrid is the stage-1 threshold, as a diagnosis only: the top's turn read at the tick's start at 1 or more, and the vacuum's borrow read at the step's output at -1 or less.
- **The tension's reading** (ANIMATE-F2-CARRY.md): with `dial_nof2`, TENSION=ratio reads the Mesh tension in the time gear's teeth, t = (Gamma t_abs) div X_ij (X_ij the two ends' mean stretch at the tick's start), unclipped. CONE=held reads it at 0 below 0, as a diagnosis only.
- **The earlier variants** (base, nofloor, notick, carry, carry_nof2, weakmin, fallmin) are ANIMATE-PROBES-2's, unchanged.

## tension_scale.py: the Mesh tension F2 clamps

- **Beside many_bangs.py:** `python -I tension_scale.py`. It runs the A1 course for 60 ticks (the `dial` variant read at the tick's start) and prints the stretch, the axis gears and their sum, every Spoke's tension, how many Mesh readings fall inside [0, Gamma], and t / X.
- **The output** is a1_tension_scale_60.txt: 0 of 384 inside at every tick.

## ladder_pauli.py: the 24's ladder under Pauli's rule

- **Pure integers, no engine:** `python ladder_pauli.py`. It reads the kinds of 2O from ANIMATE-PROBES-2/kinds_ladder.py.
- **It checks:**
  - the symmetric and antisymmetric squares of every kind;
  - where A1 lies;
  - three ladders from {A1, E1/2}: every pair of one kind equal; the fitting's first-rung pair unequal; every pair whole;
  - a mutant with the exchange sign read backwards.
- **The output** is ladder_pauli.txt.

## The outputs

Three outputs ran before the FORM setting was added, so their settings line names no FORM: a1_count_step_5M_250.txt, twins_JK_count_start_500k_600.txt and twins_JK_count_step_500k_600.txt. Their form is the count. a1_count_start_5M_250.txt is the rerun of the committed harness, bit for bit the first run's.

| file | the calibre | the form | read at | T on the twins | what it shows |
|---|---|---|---|---|---|
| a1_count_start_5M_250.txt | A1 | count | the start | none | draft C bit for bit (640f11b7135fcbfc); carries 0 and 1; rewind 20 of 20 |
| a1_count_step_5M_250.txt | A1 | count | the step | none | tops a tick earlier; a 28-turn step written at the fourth bang; rewind 20 of 20 |
| a1_tension_scale_60.txt | A1 | count | the start | none | the tension inside [0, Gamma] at 0 of 384 Mesh readings at every tick; t / X a few percent |
| a1_tension_ratio_nof2_5M_250.txt | A1 | count, the tension in the time gear's teeth, F2 struck | the start | none | the tension -42 to 83; refused at tick 87; rewind 20 of 20 |
| a1_tension_ratio_cone_5M_250.txt | A1 | the same, the lower side read at 0 (diagnosis) | the start | none | 6 tops every 39 ticks; books 250 of 250; rewind 20 of 20 |
| twins_JK_count_start_500k_600.txt | twins | count | the start | J K | refused at tick 346: the fall below the vacuum within one tick |
| twins_JK_count_step_500k_600.txt | twins | count | the step | J K | refused at tick 432: even counts let the stretch leave the dial |
| twins_K_count_step_500k_600.txt | twins | count | the step | K | refused at tick 432, as with J K |
| twins_JK_threshold_500k_600.txt | twins | threshold | the start and the step | J K | 600 ticks on the end teeth's fallback (2,676); births 134 |
| twins_K_threshold_500k_600.txt | twins | threshold | the start and the step | K | the stage-1 run bit for bit (28e42e907a4ad507): the blend is exact |
| twins_JK_count_step_5M_600.txt | twins | count | the step | J K | eleven clean bangs, twin births at the 7th and 11th bangs, refused at tick 554 |
| twins_JK_count_step_5M_494.txt | twins | count | the step | J K | the same run to tick 494: the end teeth's fallback 0, the books 494 of 494, eleven distinct bottoms |
| twins_JK_threshold_5M_600.txt | twins | threshold | the start and the step | J K | 600 ticks on the end teeth's fallback (4,436); births 206 |
| stage1_*.txt | | the `carry` variant (the stage-1 threshold) | | the engine's own K | the stage-1 runs, kept as run: the A1 threshold (640f11b7135fcbfc), the twins at 500,000 and 5,000,000 quanta, the head with the twin row, and the twins with the floor struck (refused at tick 345) |

---
Animate, reader-5.
