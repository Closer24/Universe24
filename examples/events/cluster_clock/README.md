# Series V: a cluster of crowds read by one detector, at rest and moving as one

The model owner's question (2026-09-21, in conversation after series U,
translated): "so is it possible that this is the matter with galaxy
clusters that look as if at a constant speed when they should have flown
apart?", then "start the additional test you proposed". The design with the
expectation pinned before any run is
[docs/designs/cluster_clock/DESIGN.md](../../../docs/designs/cluster_clock/DESIGN.md);
this folder holds the two worlds it declares, written by `make_worlds.py`
(which imports series U's generator, `../crowd_clock/make_worlds.py`, for
the fan, the speeds and the pinned k), and `expectations.json`. Nothing is
registered.

## The worlds

Five members before one fixed detector (x = 3, `reads: "age"`), each a lamp
of `s_px1` (2^20 units, one unit per self-creation toward the detector)
inside its own crowd of two `mass` sources (series U's fan, F per source
per interval) at k = 4 F / 2^16 = 0, 0.1, 0.3, 0.6, 1, the lamps at
x = 40, 60, 80, 100, 120 on a bar of 201 x 9 x 9.

| World | the members | pinned 1 + z of the five |
| --- | --- | --- |
| `cluster_rest.json` | every body fixed | 1.000, 1.100, 1.300, 1.600, 2.000: a "velocity dispersion" of 0.36 c around 0.4 c with nothing moving, one-sided |
| `cluster_moving.json` | the lamps at 0.2 c away from the detector, each member's sources at 0.2 c / (1 + k), the pace of their waiting lamp (the crowd slowed alike, emulated by momentum) | 1.200, 1.300, 1.500, 1.800, 2.200: every member shifted by 0.200, the dispersion unchanged (the product form would read 1.32, 1.56, 1.92, 2.40) |

## Run and read

```bash
PYTHONPATH=src python examples/events/cluster_clock/make_worlds.py
PYTHONPATH=src python tools/run_series.py --jobs 2 --out artifacts/cluster_clock examples/events/cluster_clock/cluster_rest.json examples/events/cluster_clock/cluster_moving.json
```

`tests/test_cluster_clock.py` pins the shipped worlds to the generator, the
presence 4 F at every lamp, the emulated pace and the algebra.

## The register entry, drafted (not registered until the model owner says so)

- **Confronts.** The owner's question of 2026-09-21: a cluster's velocity
  dispersion as a spread of the members' clocks. Five members of different
  crowd densities before one detector, at rest and moving as one.
- **Model prediction, pinned before the run** (the design's section 3): at
  rest 1 + z_i = 1 + k_i (a dispersion of 0.36 c with nothing moving, never
  below the bare member's 1.000); moving as one 1 + z_i = 1 + k_i + v / c,
  the terms adding, every member shifted by 0.200 and the spread untouched.
- **Run.** 2026-09-21 on main d8cb46e (the design's section 7): all ten
  readings inside the tolerance; at rest 1 + z = 1.0000, 1.0999, 1.3001,
  1.6000, 2.0000 (a dispersion of 0.363 with nothing moving, none below the
  bare member); moving as one 1.2007, 1.3022, 1.5066, 1.8092, 2.2147 for the
  pinned 1.2, 1.3, 1.5, 1.8, 2.2 (the product form, 2.4 at k = 1, refuted),
  the dispersion 0.368; every lamp within one Link of its emulated sources;
  no light lost.
- **Re-read under `clock-age-v1` (2026-09-21; record 394: a clock counts
  the age moment by default).** The two worlds run again on the head of
  branch `clock-age-v1` (`tools/run_series.py --jobs 2`, 500 intervals) and
  read by the same method in the window 250 to 500 per lamp number (the
  reader reproduced the registered readings on `main` first). DETECTOR, at
  rest 1 + z = 1.0000, 1.5510, 2.6502, 4.2992, 6.4990 for the age word's
  pins 1, 1.55, 2.65, 4.3, 6.5 (the register's block `clock_age_v1`, each
  k 5.5 times the presence word's; the presence word read 1.0000, 1.0999,
  1.3001, 1.6000, 2.0000 for 1, 1.1, 1.3, 1.6, 2): every member inside the
  tolerance of 0.02, the k read from the lamps' births 0, 0.543, 1.660,
  3.310, 5.579; the z mean 2.1999 (was 0.4000), the dispersion 1.9977 (was
  0.3633), the minimum 0.0000; every ordinal arrived. Moving as one, a
  research reading: the members' sources were emulated at 0.2 c / (1 + k)
  for the presence word's k, so under the age word every slowed lamp but
  the bare one falls behind its crowd: 1.2007, 1.4717, 1.5585, 2.0127,
  3.3219 (was 1.2007, 1.3022, 1.5066, 1.8092, 2.2147), the k read from
  the lamps' births 0, 0.250, 0.437, 0.969, 2.049 against the age word's
  0, 0.55, 1.65, 3.3, 5.5 at rest; the z mean 0.9131 (was 0.6067), the
  dispersion 0.7514 (was 0.3683). The sum form is not re-decided by this
  run: the emulation holds for the presence word's k alone, and its
  re-declaration is the design's.
- **Re-read on `main` and the moving members re-declared at the age word's
  k (2026-09-21, the Replicator; Far 2's flag, record 463 (ii)).** The two
  worlds run again on `main` at e531de5c (`tools/run_series.py --jobs 3`,
  500 intervals, 2.9 and 3.3 s) and read by the same method: every reading
  above digit for digit (DETECTOR: at rest 1.0000, 1.5510, 2.6502, 4.2992,
  6.4990, the z mean 2.1999 and the dispersion 1.9977; moving as one
  1.2007, 1.4717, 1.5585, 2.0127, 3.3219, the z mean 0.9131 and the
  dispersion 0.7514; every ordinal arrived). The register's block
  `clock_age_v1` now carries, per moving member, k under the age word
  (5.5 times the presence word's) beside `k_presence_word` and the
  statement that the shipped world paces every member's sources at
  0.2 c / (1 + k) for the presence word's k (the world file unchanged),
  so the additive pin 1 + k + v / c is readable in this world for the
  bare member alone (`pin_readable_in_the_shipped_world`); the others
  stand for a world whose sources pace the age word's k, the design's
  re-declaration. The map `replicated` points at the Replicator's line
  ([REPLICATIONS](../../../docs/REPLICATIONS.md)).
