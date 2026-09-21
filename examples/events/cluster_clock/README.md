# Series Q: a cluster of crowds read by one detector, at rest and moving as one

The model owner's question (2026-09-21, in conversation after series P,
translated): "so is it possible that this is the matter with galaxy
clusters that look as if at a constant speed when they should have flown
apart?", then "start the additional test you proposed". The design with the
expectation pinned before any run is
[docs/designs/cluster_clock/DESIGN.md](../../../docs/designs/cluster_clock/DESIGN.md);
this folder holds the two worlds it declares, written by `make_worlds.py`
(which imports series P's generator, `../crowd_clock/make_worlds.py`, for
the fan, the speeds and the pinned k), and `expectations.json`. Nothing is
registered.

## The worlds

Five members before one fixed detector (x = 3, `reads: "age"`), each a lamp
of `s_px1` (2^20 units, one unit per self-creation toward the detector)
inside its own crowd of two `mass` sources (series P's fan, F per source
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
- **Run.** Section 7 of the design, when done.
