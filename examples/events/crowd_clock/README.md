# Series P: a lamp inside a crowd, still and moving

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
- **Run.** Section 7 of the design, when done.
