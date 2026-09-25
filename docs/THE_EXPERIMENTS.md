# The twenty-four experiments

The model owner's decisions of 2026-09-25 (records 1911, 1915, 1916 and 1918
of the [log](LOG_2026-09-20.md); [Highlights](HIGHLIGHTS.md) 5.4, the rows
"Twenty-four experiments", "The click rule, one statement" and "The
convergence to the freeze") fix two groups of experiments, and both groups
are algebraic:

- **The eighteen measured experiments.** Each one runs on the GameBoard from
  its input file and is read in clicks against its blind pin. The pin is the
  algebra's prediction, written before the run, and the run checks the
  algebra in clicks.
- **The six algebraic experiments.** Each one's result is computed from the
  algebra with no run. The paper states how to compute it and gives the
  model's number beside nature's, with whether they agree. It is labelled
  COMPUTATION and is never a measurement.

This page is an index. The authority for every row is the
mathematician's table,
[ALGEBRA.md 9.22 (8)](ALGEBRA.md) ("The seventeen, each complete for its input
file", which includes the eighteenth), with its placements in
[LAB_TOOLS.md part B](designs/lab_tools/LAB_TOOLS.md). A number quoted here
that differs from that table is an error of this page. No pin moves after a
reading; a miss is a fault to find.

## The eighteen measured experiments

"Pin" is the blind pin in clicks as the table writes it, in short. "State"
is what the pin or the run still waits on.

| # | Experiment | Pin, in short | State |
| --- | --- | --- | --- |
| 1 | Bell, four settings | S = 2.80 +- 0.14 at 100 pair records per setting (the pin [2.38, 3.22], the falsifier S <= 2); no-signalling control: Alice's counts identical under Bob's two axes; the product-state control S = 1.40 +- 0.52 | waits on the polariser with an axis and the crystal (F4) |
| 2 | Malus, four settings | at 256 records: 128 +- 24, 246 +- 9, 199 +- 20, 177 +- 22 | waits on F4 |
| 3 | The two slits | at 4096 records: the visibility 0.95 +- 0.13 at the spacing 53.2; the one-opening control is the single opening's spread | waits on extents, the born profile and the face slabs (F0 to F2) |
| 4 | The pace fans | the axis's wave number above the diagonal's by k^2 / 48; no click pin | a diagnostic row, not compared with nature; waits on F0 to F2 |
| 5 | The muon's form | at rest the mode's period 42.33 intervals; in motion the tick 0.8146 of the rest, band 0.3 percent | in motion waits on packets and the moving name (F3) |
| 6 | The redshift | 1 + z = 1.935 at v = 1 / 3, band 0.3 percent; the rest control 1 | waits on F3 and the emitter's pace |
| 7 | The round trip | (1 + beta) / (1 - beta) = 3.7373, band 0.3 percent | waits on F3 and the emitter's pace |
| 8 | Sagnac | at rest the first rung 108 +- 2; in motion scaled by 2.369 and 0.634 | the rungs owed on the flux form; waits on the emitter's pace and F3 |
| 9 | de Broglie's fringes (M1) | at 2048 records: the visibility 0.92 +- 0.19; the lobes at 64.5 -+ 53.2 | waits on F0 to F2 |
| 10 | The moving mass's energy (M2) | the first rung 169 +- 2 | owed on the flux form; waits on the emitter's pace |
| 11 | The boxes (ii-a, ii-b) | at rest the periods 52.67 and 63.56 intervals; in motion the tick 0.8146 | in motion waits on F3 |
| 12 | The deep well | at rest the period 86.25 intervals; in motion the tick 0.8146 | in motion waits on F3 |
| 13 | The light clock | at rest the first rung 214 +- 1 (211.98 plus the rung's offset); in motion a closed form only | the first run MISSED at 76 (record 1917); waits on the born profile and the emitter's pace |
| 14 | The receding index at k = 3 | the delay behind the medium; the index at rest n = 1.2519 as its control | the bound medium's number owed; waits on F3 |
| 15 | The receding index at k = 4 | as row 14 with n = 1.2577 | as row 14 |
| 16 | The two-qubit computer | Grover 0 / 0 / 0 / 100 at 100 records; Deutsch-Jozsa 100 / 0 per oracle | waits on F4 |
| 17 | Mach-Zehnder | at 100 records: bright 97 +- 5, dark 0 or 1, faces 3; the one-arm control 47 / 39 / 14 | waits on F0 to F2 |
| 18 | Sorkin's three openings | the Sorkin sum of the seven worlds' screen totals, S = +80 +- 400 at 16384 records per world | waits on F0 to F2 |

F0 to F4 are Nature24's engine packages ([record 1914](LOG_2026-09-20.md)):
F0 bodies with extents per axis, F1 the born profile, F2 the face receiver as
a slab, F3 packets with their momentum and the moving name, and F4 the
polariser with an axis and the crystal. "The emitter's pace" is the click
rule of [ALGEBRA.md 9.17 (7) (f)](ALGEBRA.md), adopted by record 1918.

## The six algebraic experiments

Each one is computed from the algebra with no run. The mathematician writes
the section with the computation step by step, the model's number, nature's
number with its source, and the verdict (record 1915).

| # | Experiment | What the algebra gives | Against nature |
| --- | --- | --- | --- |
| A1 | The atom's lines | the lines at the modes' own frequencies, not at their differences | disagrees: nature's lines are at the differences; lines there would need a coupling outside the law |
| A2 | Light's dispersion by direction and wavelength | the coefficient 3 sum n_i^4 - 1 in [0, 2] | against the bounds from astrophysical bursts |
| A3 | The bound on the one scale | the length of one interval, bounded from the two paces | against the measured bounds |
| A4 | The bound clock's second term | a bound below 1 / gamma, printed on every massive world | a bound, no run |
| A5 | Born's exponent and Tsirelson's limit | the exponent 2 exactly; Tsirelson's value as a limit | identities of the algebra |
| A6 | Gravity's forms under a shell average | Newton's inverse square and Poisson's equation as limits | limits of the algebra, not a run |

## The way to the freeze

The steps are those of record 1918:

1. Nature24 closes everything:
   - the mathematician's gate on emitter-click, then its merge;
   - the click rule;
   - the born profile;
   - the packages F0 to F4;
   - the eighteen's input files, with their pins taken from main.
2. An independent checker checks each measured experiment locally with the
   one command:
   - the input is LAWFUL at load;
   - the same input gives the same output;
   - the clicks stand against the blind pin as stated.
3. The freeze.
