# Series U: a lamp inside a crowd, still and moving

The model owner's remark (2026-09-21, in conversation after the two-stars
run, translated): "this could explain something about distant galaxies and
why they look as if at high speed", then "check it yourself and report to
the Boss". The design with the expectation pinned before any run is
[docs/designs/crowd_clock/DESIGN.md](../../../docs/designs/crowd_clock/DESIGN.md);
this folder holds the eight worlds it declares, written by `make_worlds.py`,
and `expectations.json`, the generator's derivation. Nothing is registered.

## The worlds

A lamp (`s_px1`, series G2's light family, one unit per self-creation, the
wheel [1, 64]) inside a crowd of two free `mass` sources three Links away on
+y and +z, each sending F units per interval on a fan of nine directions
across the lamp's line (the lamp lets them `pass`; its clock counts them),
read by a fixed detector with `reads: "age"`; the world's `suspension` is
[1, 2^16]. Five worlds hold the crowd still, F chosen for the pinned
k = 4 F / 2^16 at 0.005, 0.08, 0.3, 1 and 2; three throw the lamp and its
crowd together at 0.2 c away from the detector at k = 0.08, 0.3 and 1.

| World | F | pinned k | pinned 1 + z at the detector |
| --- | --- | --- | --- |
| `still_005.json` | 82 | 0.005 | 1.005 |
| `still_08.json` | 1311 | 0.08 | 1.08 |
| `still_3.json` | 4915 | 0.3 | 1.3 |
| `still_1.json` | 16384 | 1 | 2.0 |
| `still_2.json` | 32768 | 2 | 3.0 |
| `moving_08.json` | 1311 | 0.08 | 1.224 .. 1.296 in both windows (the lamp inside its crowd) |
| `moving_3.json` | 4915 | 0.3 | 1.2 .. 1.56, falling between the windows |
| `moving_1.json` | 16384 | 1 | 1.2 .. 2.4 then 1.2 (the lamp left behind by its crowd) |

## The expectation, pinned (the design's section 3)

Under the law as built a detector reads a crowd's lamp at
1 + z = (1 + k)(1 + v / c): the Doppler of its speed and the slowing of its
clock by the crowd, k the presence of the crowd's rows at its Node times
the suspension's width. The still lamp births once per 1 + k intervals and
the detector reads 1 + k, so z = 1 and z = 2 are read from a lamp at rest;
every birth reaches the detector (the crowd slows the clock, it takes no
light). A lamp that waits does not step, so a slowed lamp moves at
v / (1 + k) while its unslowed crowd moves at v: it falls behind and, past
the fan's reach of four Links, is out of its crowd and reads the Doppler
alone. The brackets, the refutation lines and what the run cannot decide
are the design's sections 3 to 5.

## Run and read

```bash
PYTHONPATH=src python examples/events/crowd_clock/make_worlds.py
PYTHONPATH=src python tools/run_series.py --jobs 3 --out artifacts/crowd_clock examples/events/crowd_clock/still_005.json examples/events/crowd_clock/still_08.json examples/events/crowd_clock/still_3.json examples/events/crowd_clock/still_1.json examples/events/crowd_clock/still_2.json examples/events/crowd_clock/moving_08.json examples/events/crowd_clock/moving_3.json examples/events/crowd_clock/moving_1.json
```

`tests/test_crowd_clock.py` pins the shipped worlds to the generator, the
presence 4 F at the lamp's Node once the rows arrive, and the algebra.

## The register entry, drafted (not registered until the model owner says so)

- **Confronts.** The owner's remark of 2026-09-21: a distant galaxy's
  redshift as a slowed clock. A lamp inside a crowd of gravity rows, still
  and moving, read by a detector at rest.
- **Model prediction, pinned before the run** (the design's section 3): the
  still lamp reads 1 + k with k = 4 F / 2^16 up to 2 (z = 2 at rest), the
  light escapes whole, the moving lamp reads (1 + k)(1 + v / c) inside its
  crowd and falls behind it at v / (1 + k).
- **Run.** 2026-09-21 on main 119fd9b, two runs (the design's section 7):
  the first, with a lamp of 8192 units, inside the pins in the first window
  at every rung and outside in the second at six, by the lamp's own
  spending (its wheel by its content over K), not the crowd; the second,
  with the reservoir raised to 2^20 units, all 32 readings inside: the still
  lamp reads 1 + z = 1.000/1.006, 1.080, 1.300, 2.000, 3.000 for the pinned
  1.005, 1.08, 1.3, 2, 3 (k = 4 F / 2^16 exact to the rung, z = 1 and 2 from
  a lamp at rest); every birth reaches the detector; the moving lamp reads
  1.283 inside its crowd, between the sum 1 + k + v / c (1.279) and the
  product (1.295), and falls behind it,
  leaving the fan at ticks 181 and 86 within the pinned brackets and reading
  the Doppler alone thereafter (1.85 then 1.21).
- **Re-read under `clock-age-v1` (2026-09-21; the model owner's word of
  record 394: a clock counts the age moment by default).** The eight worlds
  run again through `tools/run_series.py --jobs 2` (500 intervals) on the
  head of branch `clock-age-v1` and read by the same method (the birth
  ordinal against the click's tick in the windows, the lamp's k from its
  births one flight earlier; the reader reproduced every registered reading
  on `main` first, 1.3000 at `still_3`, 2.0000 at `still_1`). The pins
  under the age word are the register's block `clock_age_v1` (k = 22 F /
  2^16, the age moment of the two sources' rows dwelling at the ages 5 and
  6, 5.5 times the presence word's 4 F / 2^16; series T's map). DETECTOR,
  1 + z in the two windows, the presence word's registered reading beside
  it: `still_005` 1.0284, 1.0283 (pinned 1.0275; was 1.0000, 1.0064 for
  1.005); `still_08` 1.4400, 1.4401 (1.4401; was 1.0802, 1.0800 for 1.08);
  `still_3` 2.6517, 2.6514 (2.65; was 1.3000, 1.3000 for 1.3); `still_1`
  6.5002, 6.5002 (6.5; was 2.0000, 2.0000 for 2); `still_2` 12.0000,
  12.0000 (12; was 3.0000, 3.0000 for 3): every still reading inside 0.02
  of the age word's pin, the k read from the lamp's births 0.027, 0.442,
  1.63 to 1.68, 5.25 to 5.52, 10.5 to 11.5, the light escaping whole (319,
  229, 127, 55, 32 ordinals, none missing). The moving worlds, a research
  reading: their sources' pace 0.2 c / (1 + k) was emulated for the
  presence word's k, so under the age word the slowed lamp falls behind
  its crowd sooner and reads the Doppler alone after: `moving_08` 1.6145,
  1.2822 (was 1.2827, 1.2714), the exit at tick 138 (was none before 464);
  `moving_3` 1.6871, 1.1978 (was 1.4152, 1.4768), the exit at 69 (was
  181); `moving_1` 1.3540, 1.1981 (was 1.8514, 1.2058), the exit at 52
  (was 86); the lag 8 Links at the end in all three, every ordinal
  arrived. What the re-read decides: a still lamp's clock reads the age
  moment, linear in F over the same factor of 400; the moving worlds
  decide nothing until their emulation is re-declared for the age word's
  k, which is the design's to do, not the run's.
- **Re-read on `main` and the moving worlds re-declared at the age word's
  k (2026-09-21, the Replicator; Far 2's flag, record 463 (ii)).** The
  eight worlds run again on `main` at e531de5c (`tools/run_series.py
  --jobs 3`, 500 intervals, 1.4 to 1.9 s each) and read by the same
  method: every reading above digit for digit (DETECTOR: 1.0284 / 1.0283,
  1.4400 / 1.4401, 2.6517 / 2.6514, 6.5002 / 6.5002, 12.0000 / 12.0000;
  1.6145 / 1.2822, 1.6871 / 1.1978, 1.3540 / 1.1981; the exits at 138, 69,
  52; the lag 8 Links; every ordinal arrived). The register's block
  `clock_age_v1` now carries the three moving worlds under
  `moving_worlds`, each at the age word's k (5.5 times the presence
  word's, the old k beside it as `k_presence_word`) with the brackets by
  the presence block's own rule at that k (`make_worlds.moving_entry`,
  one helper for both blocks): the exit brackets [112, 347], [55, 118]
  and [41, 59] hold the read exits 138, 69 and 52, and the windows'
  brackets [1.332, 1.728] and [1.2, 1.728] (`moving_08`), [1.2, 3.18] and
  [1.2, 1.2] (`moving_3`), [1.2, 7.8] and [1.2, 1.2] (`moving_1`) hold
  every reading (the second windows of `moving_3` and `moving_1` within
  0.02 of the Doppler alone). The entry says what the worlds declare: the
  sources' pace 0.2 c / (1 + k) is for the presence word's k (the world
  files unchanged), so under the age word the lamp leaves its crowd
  within the bracket; a re-declaration of the emulation for the age
  word's k stays the design's. The map `replicated` points at the
  Replicator's line ([REPLICATIONS](../../../docs/REPLICATIONS.md)).
