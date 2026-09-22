# Series X: Poisson after a detector, the source term at both of its sides

The chief physicist's design of 2026-09-22 ([record 574](../../../docs/LOG_2026-09-20.md),
part 2, POISSON AFTER A DETECTOR) under the model owner's word of that day
("build them", records 574 and 581). Series E read the clock's `1 / r` off
the probes' registers, a GameBoard reading of a world with no detector, and
the owner struck such readings from the paper (records 562, 564 and 575);
series T reads a clock's rate after a detector at two distances from a point
crowd ([NATURE row 12](../../../docs/NATURE.md), REPLICATED), which is
Laplace's part, the field outside its source. THIS SERIES READS THE SOURCE
TERM AFTER A DETECTOR: inside a shell of sources the potential is flat (the
shell theorem) and outside it falls as `C / r`, so the field equation is
read after a detector at both of its sides.

The register's entry is [docs/EXPERIMENTS.md, "X, Poisson after a
detector"](../../../docs/EXPERIMENTS.md#x-poisson-after-a-detector-2026-09-22);
the pins with their `derivations` map are `expectations.json` (written by
`make_worlds.py` before any run); the readings tool is `read_runs.py`.

## The kind of every reading

Every number of this series is a DETECTOR reading, and the tool opens
nothing else: `read_runs.py` reads the `click` lines of the detector in
`events.jsonl` and no other line, no store, no `state.json`, no replay of a
world (the owner's word of 2026-09-22, records 562 and 564: no experiment
reads the GameBoard; a GameBoard reading serves diagnostics and bug fixing
alone). The host's cost below is a GAMEBOARD number and is reported apart
from the readings, as the host's cost always is.

## The question

`1 / r^2` and `1 / r` are two readings of one stream
([DERIVATIONS_BEAM 5.1](../../../docs/DERIVATIONS_BEAM.md#51-the-two-fields-of-one-stream-and-the-equation-they-obey)):
the presence is the retarded flux, which obeys Gauss's law, and the age
moment `A = q dwell / (4 pi c r)` per source is the retarded potential,
which obeys Poisson's equation with the sources' release as the density.
Outside a source the two cannot be told apart by their form alone at one
distance, and series T tells them apart at two. INSIDE A SHELL OF SOURCES
THEY DIFFER AS FAR AS TWO FIELDS CAN: the potential is flat, the flux is
not. Under the age word (the law's default since clock-age-v1,
[record 394](../../../docs/HIGHLIGHTS.md#54-the-detector)) a body's clock
counts the age moment and its rate is `1 / (1 + k_a)`, so a lamp's births
per interval, read at a detector, read the field the sources make.

## The worlds

Series T's geometry with the crowd's point source replaced by a shell
(`make_worlds.py` imports series T's generator for the speeds and series E's
for the one copy of the fan of 290; series T's registered worlds are
untouched, byte for byte):

- the lamp `s_px1` at rest at x = 103 (2^20 units, one unit per
  self-creation on -x, the wheel [1, 64]), the detector fixed at x = 3
  measuring `s_px1` with `reads: "age"`: series T's flight of 100 Links and
  series T's windows, 200 to 350 and 350 to 500 of 500 intervals;
- a shell of 450 fixed `mass` sources of radius R = 6 about a centre r Links
  from the lamp on +x, away from the detector, so the lamp's light never
  crosses the shell when the lamp is outside it; the shell's Nodes are those
  at `|distance - R| < 1/2` (series E's selection), each releasing on the
  full fan of 290, named by the indices of the world's direction table;
- the release: series T's crowd's total release pair, 2 F with F = 4915
  units per direction per interval, spread over the shell's Nodes, so
  `amount` = 1431597 at `release` [1, 2^16], 21.8444 units per source per
  direction per interval;
- `suspension` [1, 2^16] as series T, the bar 110 + r x 15 x 15.

| World | the lamp's `mass` entry | r | where | pinned k | pinned 1 + z (DETECTOR) |
| --- | --- | --- | --- | --- | --- |
| `age_2.json` | `{"rule": "pass", "reads": "age"}` | 2 | inside | 0.914351 | 1.914351 |
| `age_4.json` | `{"rule": "pass", "reads": "age"}` | 4 | inside | 0.910783 | 1.910783 |
| `age_12.json` | `{"rule": "pass", "reads": "age"}` | 12 | outside | 0.563110 | 1.563110 |
| `presence_2.json` | `{"rule": "pass", "reads": "presence"}` | 2 | inside | 0.089647 | 1.089647 |
| `presence_4.json` | `{"rule": "pass", "reads": "presence"}` | 4 | inside | 0.106724 | 1.106724 |
| `presence_12.json` | `{"rule": "pass", "reads": "presence"}` | 12 | outside | 0.029271 | 1.029271 |
| `control_2.json`, `control_4.json`, `control_12.json` | none (the lamp alone) | 2, 4, 12 | -- | 0 | 1.000000 |

The six worlds of the design's point (2) are the three under the age word
with their controls; the three under the presence word are the design's
point (3), run beside them as series T ran the two words, and expected to
FAIL inside.

## The pins, written before any run

All of them are the map's: section E of
[docs/designs/clock_age/clock_age_map.py](../../../docs/designs/clock_age/clock_age_map.py),
its numbers in [clock_age_map.out](../../../docs/designs/clock_age/clock_age_map.out)
beside it. The map walks every source's lines on the engine's own flight
table and states, per unit of the release, what the whole shell leaves at
each lamp's Node.

**The interior by the map:** the map's interior on the axis runs 5009 to 5246 with uniform sources (the age moment at r = 0 to 5: 5162, 5009, 5086, 5130, 5086, 5246; with the sources' own clocks k = 0.932, 0.898, 0.914, 0.919, 0.911, 0.943), a lattice ripple of about +-2.4 percent about the shell theorem's flat interior; the equality 5086 at r = 2 and at r = 4 is a coincidence of the lattice at the two Nodes the design named before the map (record 574); at r = 12 the age moment is 3144; the
presence is 499, 596 and 163, rising toward the shell as a flux does and
not flat inside.

**The sources' own clocks, the one thing the design did not foresee.** The
shell's sources stand in one another's rows, so each source's own clock
counts the age moment of its neighbours by the law's default word and a
source releases only at its self-creations: its release per interval is its
declared rate over 1 + its own count. The map iterates that fixed point to
convergence: the sources' own k runs 0.787 to 0.932 (mean 0.866), so each
keeps 11.31 to 12.22 of its declared 21.84 units, 0.536 of the rate. This
is the law's own nonlinearity, not a rule added here: a dense shell slows
its own clocks and so releases less. At the two Nodes the design named the
uniform sources give one integer, and the spread of the sources' own clocks
over the lattice shell is what moves the inside pin off 1 there; the
lattice interior's own ripple, +-2.4 percent by the map, is not read at two
Nodes.

| The reading (DETECTOR, k = 1 + z - 1 from the detector's click lines) | Pinned | Refuted if |
| --- | --- | --- |
| inside, the age word: `k(2) / k(4)` | 1.003917 (the continuum's 1: the shell theorem, Poisson's source term); the ripple 0.0039 is the sources' own clocks and nothing else | outside 1 by more than 0.02, five times the ripple: no Poisson |
| inside, the presence word: `k(2) / k(4)` | 0.839989, forty-one ripples from 1: the FAIL expected, `1 / r^2` obeying the flux and not the potential | the pin missed by more than 0.02; it is the one reading that tells the two words apart at a source term |
| outside, the age word: `k(12) / k(4)` | 0.618270; the continuum's `R / 12` = 0.5, the lattice above it by the grain of the map's section C, where the age moment times r rises with r (series E's shell means read the same grain) | the pin missed by more than 0.02: series T's `1 / r` refuted |
| every world: `1 + z` | the table above, k within a tenth of itself | outside it; the bracket is what the map's fixed point does not model, the bursts of a slowed source's release |
| the controls: `1 + z` | 1.0000 exactly (no crowd, nothing owed) | any departure |

The two ratios are what decides, and they are robust to the shell's overall
release: a common factor cancels in them exactly.

## Run and read

```bash
PYTHONPATH=src python examples/events/shell_clock/make_worlds.py
PYTHONPATH=src python tools/run_series.py --jobs 1 --out artifacts/shell_clock/<world> \
    examples/events/shell_clock/<world>.json     # one world at a time: see the host's cost
PYTHONPATH=src python examples/events/shell_clock/read_runs.py artifacts/shell_clock
```

A shell world writes about 24 MB of record per interval (450 sources on the
fan of 290: the rows leaving through the faces and the sources reading one
another), so 500 intervals are about 12 GB and about 24 minutes of host time
per world. The worlds are therefore run one at a time and each record is
read for the detector's clicks and then reclaimed, the runner's own digests
kept from its summary first; the readings and the digests are what the
register carries, as the [retention policy](../../../docs/RETENTION.md) has
it for every run's evidence.

**Measured (2026-09-22, one run each, `readings.json` beside the worlds,
written by `read_runs.py` from the detector's click lines alone; measured
once, awaiting replication).** DETECTOR, `1 + z` in the windows 200 to 350
and 350 to 500: the age word 1.9056 / 1.9176 at r = 2 (k read 0.9116, the
pin 0.914351), 1.9061 / 1.9118 at r = 4 (0.9089, the pin 0.910783), 1.5782 /
1.5643 at r = 12 (0.5712, the pin 0.563110); the presence word 1.0891 /
1.0893 at r = 2 (0.0892, the pin 0.089647), 1.1063 / 1.1063 at r = 4
(0.1063, the pin 0.106724), 1.0297 / 1.0291 at r = 12 (0.0294, the pin
0.029271); the three controls 1.0000 / 1.0000. Every world MET, the
absolute k within 1.5 percent of the map's fixed point everywhere and within
half a percent inside; no ordinal missing in any world (the light escapes
whole, through the shell's Nodes when the lamp is inside it); the age read
172 in every world, the flight of 100 Links. THE RATIOS THAT DECIDE: inside
under the age word `k(2) / k(4)` = 1.0029 (the pin 1.003917, MET; flat
within the tolerance: YES), inside under the presence word 0.8390 (the pin
0.839989, MET; flat: NO, the FAIL expected), outside under the age word
`k(12) / k(4)` = 0.6285 (the pin 0.618270, MET; the continuum's 0.5 outside
the tolerance, as the map said before the run). Per window the three ratios read inside under the age word 0.9994 / 1.0063, inside under the presence word 0.8379 / 0.8401, outside under the age word 0.6381 / 0.6189, and k drifts from the first window to the second by +1.3, +0.6 and -2.4 percent (the presence word +0.3, 0.0 and -2.0), so the outside MET is met at the reading's resolution (the windows 0.638 and 0.619 against the tolerance 0.02). The inside reading is the
same age moment within 0.02 at the two Nodes the design named (the windows
0.9994 and 1.0063); the lattice interior's own ripple, +-2.4 percent by the
map, is not resolved by this run. Host cost
(GAMEBOARD, apart from the readings): 1396 to 1465 s and 1284 to 1349 MB
peak per shell world, about a second per control; the events' fingerprints
5a228c2c398f, 63335a44c98c, 2e6f934ce491 (age), 0b76092af867, e8cf7b0e15d9,
1518bec744b7 (presence), bb1df5874c84 (the three controls, the same light);
the full sha256 in `readings.json`.

`tests/test_shell_clock.py` pins the shipped worlds to the generator, the
algebra of the pin, the readings tool on a hand-made click list, and the
rule the whole reading rests on: a detector whose own clock is slowed by a
crowd at its Node clicks on the same lattice ticks as one with no crowd, so
the shell's rows reaching the detector cannot move `1 + z`; only the lamp's
clock does. The reading's denominator is the host tick, the detector's own clock only at k_D = 0 (record 569); the map gives k_D = 0.0945, 0.0927 and 0.1357 at x = 3 (the detector in the shell's on-axis rows); in the strict form (records 678 and 709) the inside ratio is 0.9994, the outside 0.5134 and the presence word's k near zero or negative; the convention is the owner's (the clock audit's uncertainty (a)), the same as series T's.
