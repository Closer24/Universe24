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
is what the pin or the run still waits on. Each experiment is called by its
name; the slug is its name in files, keys and tests (record 1925). No code
stands for an experiment.

| Experiment | Slug | Pin, in short | State |
| --- | --- | --- | --- |
| Bell's four settings | `bell_four_settings` | S = 2.80 +- 0.14 at 100 pair records per setting (the pin [2.38, 3.22], the falsifier S <= 2); no-signalling control: Alice's counts identical under Bob's two axes; the product-state control S = 1.40 +- 0.52 | waits on the polariser's axis and the crystal |
| Malus's four axes | `malus_four_axes` | at 256 records: 128 +- 24, 246 +- 9, 199 +- 20, 177 +- 22 | waits on the polariser's axis and the crystal |
| The two slits | `two_slits` | at 4096 records: the visibility 0.95 +- 0.13 at the spacing 53.2; the one-opening control is the single opening's spread | waits on the bodies with extents, the travelling born profile and the face slab |
| The pace fans | `pace_fans` | the axis's wave number above the diagonal's by k^2 / 48; no click pin | a diagnostic row, not compared with nature; waits on the bodies with extents, the travelling born profile and the face slab |
| The muon's moving clock | `muon_moving_clock` | at rest the mode's period 42.33 intervals; in motion the tick 0.8146 of the rest, band 0.3 percent | in motion waits on the packets with momentum and the moving name |
| The moving emitter's redshift | `moving_emitter_redshift` | 1 + z = 1.935 at v = 1 / 3, band 0.3 percent; the rest control 1 | waits on the packets with momentum and the moving name |
| The round trip off a receding mirror | `receding_mirror_round_trip` | (1 + beta) / (1 - beta) = 3.7373, band 0.3 percent | waits on the packets with momentum and the moving name |
| Sagnac's two-way light times | `sagnac_light_times` | at rest the first rung 108 +- 2; in motion scaled by 2.369 and 0.634 | the rungs owed on the flux form; waits on the packets with momentum and the moving name |
| De Broglie's fringes | `de_broglie_fringes` | at 2048 records: the visibility 0.92 +- 0.19; the lobes at 64.5 -+ 53.2 | waits on the bodies with extents, the travelling born profile and the face slab |
| The moving mass's energy | `moving_mass_energy` | the first rung 169 +- 2 | owed on the flux form |
| The boxed clocks, sides 20 and 28 | `boxed_clock_side_20`, `boxed_clock_side_28` | at rest the periods 52.67 and 63.56 intervals; in motion the tick 0.8146 | in motion waits on the packets with momentum and the moving name |
| The deep well's clock | `deep_well_clock` | at rest the period 86.25 intervals; in motion the tick 0.8146 | in motion waits on the packets with momentum and the moving name |
| The light clock | `light_clock` | at rest the first rung 214 +- 1 (211.98 plus the rung's offset); in motion a closed form only | a trial read before the freeze missed at 76 and 51 (records 1917 and 1923), a finding on the born pulse, not a failed experiment; waits on the travelling born profile |
| The receding index at one third of a Link per interval | `receding_index_speed_third` | the delay behind the medium; the index at rest n = 1.2519 as its control | the bound medium's number owed; waits on the packets with momentum and the moving name |
| The receding index at one quarter of a Link per interval | `receding_index_speed_quarter` | as the receding index at one third, with n = 1.2577 | as the receding index at one third |
| The two-qubit computer | `two_qubit_computer` | Grover 0 / 0 / 0 / 100 at 100 records; Deutsch-Jozsa 100 / 0 per oracle | waits on the polariser's axis and the crystal |
| Mach-Zehnder | `mach_zehnder` | at 100 records: bright 97 +- 5, dark 0 or 1, faces 3; the one-arm control 47 / 39 / 14 | waits on the bodies with extents, the travelling born profile and the face slab |
| Sorkin's three openings | `sorkin_three_openings` | the Sorkin sum of the seven worlds' screen totals, S = +80 +- 400 at 16384 records per world | waits on the bodies with extents, the travelling born profile and the face slab |

The engine's parts still to be built (record 1914) are named by what they
are: the bodies with extents per axis, the travelling born profile, the face
slab, the packets with momentum and the moving name, and the polariser's axis
and the crystal. The emitter's pace is the click rule of
[ALGEBRA.md 9.17 (7) (f)](ALGEBRA.md), adopted by record 1918 and in the
engine since record 1923. No experiment is run against its pin before the
model owner says the engine is stable (record 1924).

## The six algebraic experiments

Each one is computed from the algebra with no run. The mathematician writes
the section with the computation step by step, the model's number, nature's
number with its source, and the verdict (record 1915).

| Experiment | Slug | What the algebra gives | Against nature |
| --- | --- | --- | --- |
| The atom's lines | `atom_lines` | the lines at the modes' own frequencies, not at their differences | disagrees: nature's lines are at the differences; lines there would need a coupling outside the law |
| Light's dispersion by direction and wavelength | `light_dispersion` | the coefficient 3 sum n_i^4 - 1 in [0, 2] | against the bounds from astrophysical bursts |
| The bound on the interval's length | `interval_length_bound` | the length of one interval, bounded from the two paces | against the measured bounds |
| The bound clock's second term | `bound_clock_second_term` | a bound below 1 / gamma, printed on every massive world | a bound, no run |
| Born's exponent and Tsirelson's limit | `born_exponent_and_tsirelson_limit` | the exponent 2 exactly; Tsirelson's value as a limit | identities of the algebra |
| Gravity's forms under a shell average | `shell_averaged_gravity` | Newton's inverse square and Poisson's equation as limits | limits of the algebra, not a run |

## The way to the freeze

The steps are those of records 1918 and 1924:

1. Nature24 closes everything:
   - the mathematician's gate on emitter-click, then its merge;
   - the click rule;
   - the born profile;
   - the bodies with extents, the travelling born profile, the face slab, the
     packets with momentum and the moving name, the polariser's axis and the
     crystal;
   - the eighteen's input files, with their pins taken from main.
2. The model owner says the engine is stable; only then are the experiments
   run against their pins.
3. An independent checker checks each measured experiment locally with the
   one command:
   - the input is LAWFUL at load;
   - the same input gives the same output;
   - the clicks stand against the blind pin as stated.
4. The freeze.
