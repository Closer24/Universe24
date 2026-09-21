# Series S, a reader inside a crowd: the design, with the expectation pinned before any run

The G2 experimenter, 2026-09-21, on the model owner's word ("start", after
series U and Q, on the experimenter's proposal of a detector that sits
inside a crowd itself). Sections 1 to 6 are written before any run; section
7 after. Nothing here is registered in
[docs/EXPERIMENTS.md](../../EXPERIMENTS.md); the register entry is drafted
in the folder's [README](../../../examples/events/reader_clock/README.md)
for the owner's word.

Sources: [series U](../crowd_clock/DESIGN.md) (k = 4 F / 2^16 exact; a
lamp inside a crowd reads (1 + k)(1 + v / c) at a detector at rest with no
crowd), [series V](../cluster_clock/DESIGN.md) (a crowd slowed alike adds:
1 + k + v / c), [BEAM_LAW](../../BEAM_LAW.md) step 4 and notes 17, 41, 48.

## 1. The question, on the board

Series U and Q read a crowd's lamp at a detector with no crowd, and read it
by the lattice's tick. Earth is not such a reader: it sits inside the Milky
Way's crowd, and it reads by its own clock. Under the law as built the
reader's clock owes k_r intervals per self-creation exactly as the source's
owes k_s. What the reader counts in its own clock is the source's births
per its own births:

    1 + z = (1 + k_s)(1 + v / c) / (1 + k_r)      (a crowd behind an unslowed lamp)
    1 + z = (1 + k_s + v / c) / (1 + k_r)         (the source's crowd slowed alike)

Three consequences, pinned here: a reader denser than its source reads it
blue (k_r = 1, k_s = 0: 1 + z = 0.5); two bodies in crowds alike read no
shift (k_r = k_s: 1 + z = 1 at rest); the lattice's tick reads the source's
slowing alone, whatever the reader's crowd. For the owner's galaxies this
means the crowd's term is relative: what Earth reads of a galaxy is
(1 + k_galaxy) / (1 + k_here), and a galaxy in a crowd like ours reads no
clock term at all.

One question of the engine is answered by a probe before the pins (section
3): a reader that waits still clicks at every row that crosses it; the
click's tick is the lattice's. So the reading in the reader's clock is made
from the reader's own self-creations, which the design makes visible by a
lamp of the reader's own.

## 2. The worlds

`examples/events/reader_clock/make_worlds.py` (importing series U's
generator) writes five worlds on a bar of 121 x 9 x 9 Nodes (open),
`ticks` 500, `suspension` [1, 2^16], `release` [1, 2^16], `width` 2^20,
N = 64.

- **The reader**, number 1, `s_px1`, fixed at x = 10, 2^20 units, a lamp of
  one unit per self-creation on -x into the near face (its births are its
  own clock), measuring `s_px1` with `reads: "age"` and letting `mass` pass;
  its crowd, when it has one, is series U's pair of `mass` sources three
  Links up +y and +z with the fan of nine directions at F_r units per
  interval (k_r = 4 F_r / 2^16).
- **The source**, number 2, `s_px1`, at x = 70, the same lamp shining -x to
  the reader (a flight of 60 Links, 103 intervals), letting `mass` and
  `s_px1` pass; its crowd at F_s. In `alike_receding` the source is thrown
  at 0.2 c along +x and its sources at 0.2 c / (1 + k_s), the pace of the
  waiting lamp (series V's emulation of a crowd slowed alike).

| World | k_r | k_s | the source | model id |
| --- | --- | --- | --- | --- |
| `control.json` | 0 | 1 | at rest | `rays-reader-clock-control-v1` |
| `reader_dense.json` | 1 | 0 | at rest | `rays-reader-clock-reader-dense-v1` |
| `alike.json` | 1 | 1 | at rest | `rays-reader-clock-alike-v1` |
| `reader_half.json` | 0.5 | 1 | at rest | `rays-reader-clock-reader-half-v1` |
| `alike_receding.json` | 1 | 1 | 0.2 c away, its crowd at its pace | `rays-reader-clock-alike-receding-v1` |

## 3. What the run reads, pinned before it

**The probe.** A reader with k_r = 1 (two sources of F = 16384) and a
lamp of its own, reading a lamp at rest with no crowd 50 Links away for
300 intervals on the engine as merged (main d8cb46e): 213 clicks with and
without the reader's crowd, no birth ordinal missing, the clicks' ticks the
lattice's (the first at tick 87 in both); the reader's births 152 against
299, and in the window 150 to 300 exactly 2.000 clicks per reader birth. So
a waiting reader clicks at every crossing, and its own count is
(1 + k_r) / (1 + k_s) clicks per birth. The probe is calibration; the pins
follow.

The window is 250 to 500. Two readings per world, each the inverse slope
of the source's birth ordinal (`record & 0xFFFFFFFF` at the click)
against (i) the click's tick and (ii) the reader's own birth ordinal at
the click (the count of the reader's births up to that tick); the
tolerance 0.02.

| World | (i) in the lattice's clock | (ii) in the reader's clock | clicks per interval | clicks per reader birth |
| --- | --- | --- | --- | --- |
| `control` | 2.000 | 2.000 | 0.500 | 0.500 |
| `reader_dense` | 1.000 | **0.500** (blue) | 1.000 | 2.000 |
| `alike` | 2.000 | **1.000** (no shift) | 0.500 | 1.000 |
| `reader_half` | 2.000 | 1.333 | 0.500 | 0.750 |
| `alike_receding` | 2.200 | 1.100 | 0.455 | 0.909 |

Also pinned: no birth ordinal missing at the reader in any world (the
reader's crowd loses no light); the age read is the flight, 103 intervals
at rest and growing in `alike_receding`; the source of `alike_receding`
stays within one Link of its sources through the run.

## 4. What would refute the reading

- (ii) equal to (i) in `reader_dense` or `alike`: the reader's clock does
  not enter the reading; a body reads by the lattice's tick, not its own.
- (i) off 1 + k_s by more than 0.02 in any world: the reader's crowd changes
  what arrives, not only how the reader counts it.
- Clicks fewer than the source's births one flight earlier: a waiting
  reader misses rows (the probe says it does not).
- `alike_receding` reading other than 1.100 in the reader's clock: the sum
  of series V does not divide by the reader's clock as the product does.

## 5. What the run cannot decide, and what it is for

The worlds pin the law's arithmetic for a reader with a clock, not Earth's
clock. The run cannot say what k_here is, or whether any galaxy's z has a
clock term. It says what the law offers a reader inside a crowd: the crowd's
term is a ratio of the two crowds, so a reader reads its own kind of crowd
with no shift, reads denser crowds red and thinner ones blue, and reads the
lattice's tick nowhere (only through a body at rest with no crowd, which
Earth is not). It is for the owner's question of the galaxies and the
clusters (series U and Q): the clock term that Earth would read is
(1 + k_galaxy) / (1 + k_here) - 1, which is small for galaxies like ours
and large for crowds far denser, in either direction. It is also a reading
of the clock question raised for covariant-readings-v1 (record 344, "which
clock the click's tick belongs to"): here the click's tick is the
lattice's, and the reader's clock is a count of its own self-creations.

## 6. The run, when ordered

    PYTHONPATH=src python examples/events/reader_clock/make_worlds.py
    PYTHONPATH=src python tools/run_series.py --jobs 3 --out artifacts/reader_clock examples/events/reader_clock/control.json examples/events/reader_clock/reader_dense.json examples/events/reader_clock/alike.json examples/events/reader_clock/reader_half.json examples/events/reader_clock/alike_receding.json

The readings are the reader's `click` lines (the source's birth ordinal
and the tick, the `age`) and the reader's and the source's `birth` lines
(the two clocks), and in `alike_receding` the `step` lines of the source
and its sources (the lag). `tests/test_reader_clock.py` pins the shipped
worlds to the generator, the presence 4 F at the reader and the source,
and the algebra of the ratio.

## 7. Measured (2026-09-21, one run on main d8cb46e, after the pins above)

The run is `tools/run_series.py --jobs 3` over the five worlds (about two
seconds each, the books balanced, 500 intervals), read by the
experimenter's script in the window 250 to 500: the source's birth ordinal
at the reader's clicks against the click's tick (i) and against the reader's
own birth ordinal at the click (ii). Every one of the ten readings inside
the tolerance of 0.02, most to the fourth digit; no birth ordinal missing
in any world; the age 103 at rest, 117 to 139 in `alike_receding`; the
receding source within one Link of its emulated crowd through the run.

| World | k_r | k_s | (i) lattice 1 + z (pinned) | (ii) reader's clock 1 + z (pinned) | clicks per interval | clicks per reader birth (pinned) | reader births / source births |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `control` | 0 | 1 | 2.0000 (2.000) | 2.0000 (2.000) | 0.500 | 0.500 (0.500) | 499 / 252 |
| `reader_dense` | 1 | 0 | 1.0000 (1.000) | **0.5000** (0.500) | 1.000 | 2.000 (2.000) | 252 / 499 |
| `alike` | 1 | 1 | 2.0000 (2.000) | **1.0000** (1.000) | 0.500 | 1.000 (1.000) | 252 / 252 |
| `reader_half` | 0.5 | 1 | 2.0000 (2.000) | 1.3333 (1.333) | 0.500 | 0.749 (0.750) | 335 / 252 |
| `alike_receding` | 1 | 1 | 2.2111 (2.200) | 1.1054 (1.100) | 0.452 | 0.904 (0.909) | 252 / 251 |

**What the run decides.**

1. **The crowd's term is a ratio of the two crowds.** In the reader's own
   clock 1 + z = (1 + k_s) / (1 + k_r) to the fourth digit: a reader denser
   than its source reads it blue (0.5000), two bodies in crowds alike read
   no shift at all (1.0000) while the lattice's tick reads 2.0000 for both.
   The lattice's tick is read by no body inside a crowd; it is the reading
   of a body at rest with no crowd (`control`, where the two clocks agree).
2. **A waiting reader clicks at every crossing.** Clicks per lattice
   interval 1 / (1 + k_s) whatever the reader's crowd, no ordinal missing;
   the reader's waits change its own count of them, not their arrival.
3. **The sum divides as the product does.** `alike_receding` read 1.1054
   for the pinned (1 + k_s + v / c) / (1 + k_r) = 1.100, and 2.2111 in the
   lattice's tick (series V's 2.2147 for the same source); the excess of
   0.005 to 0.011 is series V's, the moving lamp's slightly higher k.
4. **The clock question.** The click's tick is the lattice's; the reader's
   clock is the count of its own self-creations, and a reading in it is a
   ratio of two counts. This is the form in which "which clock the click's
   tick belongs to" (record 344) has an answer on the engine as built.

**For the owner's galaxies.** What Earth would read of a galaxy under the
law as built is (1 + k_galaxy)(1 + v / c) / (1 + k_here) (the sum form over
1 + k_here when the galaxy's crowd is slowed alike): a galaxy in a crowd
like ours shows no clock term, a denser one shows red, a thinner one blue;
the cluster dispersion of series V is divided by 1 + k_here but not
removed; and the absolute k of series U is not what any reader inside a
crowd sees. The mapping of units is still missing (section 5).
