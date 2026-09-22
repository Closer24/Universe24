# Series S: a reader inside a crowd

Since 2026-09-22 the law's drive of a body is the line drive (the model
owner, record 972; [docs/designs/drive_b/DEFAULT.md](../../../docs/designs/drive_b/DEFAULT.md)):
`alike_receding` declares `per_axis_drive`, the per-axis drive of history,
and keeps its readings as registered, because its source's mass of content
2^30 at width 2^20 has a line-drive wall Q^2 S M = 2^62, one past the law's
bound, and is refused at load under the law (the Boss's default until the
owner speaks).

The model owner's word (2026-09-21, in conversation): "start", on the
experimenter's proposal, after series U and V, of a detector that sits
inside a crowd itself, as Earth sits inside the Milky Way. The design with
the expectation pinned before any run is
[docs/designs/reader_clock/DESIGN.md](../../../docs/designs/reader_clock/DESIGN.md);
this folder holds the five worlds it declares, written by `make_worlds.py`
(which imports series U's generator, `../crowd_clock/make_worlds.py`), and
`expectations.json`. Nothing is registered.

## The worlds

A reader (`s_px1`, fixed at x = 10, measuring `s_px1` with `reads: "age"`,
with a lamp of its own on -x so that its births are its own clock) and a
source (`s_px1` at x = 70, a lamp shining -x to the reader), each with or
without series U's crowd (two `mass` sources, the fan of nine directions,
k = 4 F / 2^16), on a bar of 121 x 9 x 9.

| World | k_r | k_s | the source | pinned 1 + z in the reader's clock | in the lattice's |
| --- | --- | --- | --- | --- | --- |
| `control.json` | 0 | 1 | at rest | 2.000 | 2.000 |
| `reader_dense.json` | 1 | 0 | at rest | 0.500 (blue) | 1.000 |
| `alike.json` | 1 | 1 | at rest | 1.000 (no shift) | 2.000 |
| `reader_half.json` | 0.5 | 1 | at rest | 1.333 | 2.000 |
| `alike_receding.json` | 1 | 1 | 0.2 c away, its crowd at its pace | 1.100 | 2.200 |

## Run and read

```bash
PYTHONPATH=src python examples/events/reader_clock/make_worlds.py
PYTHONPATH=src python tools/run_series.py --jobs 3 --out artifacts/reader_clock examples/events/reader_clock/control.json examples/events/reader_clock/reader_dense.json examples/events/reader_clock/alike.json examples/events/reader_clock/reader_half.json examples/events/reader_clock/alike_receding.json
```

`tests/test_reader_clock.py` pins the shipped worlds to the generator, the
presence 4 F at the reader and the source, and the algebra of the ratio.

## The register entry, drafted (not registered until the model owner says so)

- **Confronts.** The reader's own clock: Earth inside its galaxy reading
  another. A detector inside a crowd of k_r, with a lamp of its own for its
  clock, reading a lamp inside a crowd of k_s, at rest and receding.
- **Model prediction, pinned before the run** (the design's section 3): in
  the reader's clock 1 + z = (1 + k_s)(1 + v / c) / (1 + k_r) (the sum form
  over 1 + k_r for a crowd slowed alike): a denser reader reads blue
  (0.500), crowds alike read no shift (1.000), the lattice's tick reads the
  source's slowing alone; a waiting reader clicks at every crossing.
- **Run.** 2026-09-21 on main d8cb46e (the design's section 7): all ten
  readings inside the tolerance, most to the fourth digit: in the reader's
  clock 2.0000, 0.5000, 1.0000, 1.3333, 1.1054 for the pinned 2, 0.5, 1,
  1.333, 1.1; in the lattice's 2.0000, 1.0000, 2.0000, 2.0000, 2.2111 for
  2, 1, 2, 2, 2.2; a waiting reader clicks at every crossing (no ordinal
  missing); the crowd's term is the ratio (1 + k_s) / (1 + k_r).
- **Re-read under `clock-age-v1` (2026-09-21; record 394: a clock counts
  the age moment by default).** The five worlds run again on the head of
  branch `clock-age-v1` (`tools/run_series.py --jobs 2`, 500 intervals) and
  read by the same method in the window 250 to 500 (the reader reproduced
  the registered readings on `main` first). DETECTOR, the lattice's 1 + z
  and the reader's clock's, the age word's pins from the register's block
  `clock_age_v1` (each k 5.5 times the presence word's) and the presence
  word's registered reading beside them: `control` 6.5011 and 6.5011 (6.5
  and 6.5; was 2.0000 and 2.0000); `reader_dense` 1.0000 and 0.1539 (1 and
  0.1538; was 1.0000 and 0.5000); `alike` 6.5011 and 1.0000 (6.5 and 1;
  was 2.0000 and 1.0000); `reader_half` 6.5011 and 1.7353 (6.5 and 1.7333;
  was 2.0000 and 1.3333): the eight readings at rest inside the tolerance,
  the crowd's term the ratio (1 + k_s) / (1 + k_r) under the age word as
  under the presence word (two bodies in crowds alike read no shift at
  k = 5.5 as at k = 1); the reader's births 499, 81, 81, 137 against the
  source's 81, 499, 81, 81; every ordinal arrived. `alike_receding`, a
  research reading: the receding source's crowd was emulated at 0.2 c /
  (1 + k) for the presence word's k, so under the age word the slowed
  source falls behind it and reads less of it: the lattice's 2.2239 and
  the reader's clock 0.3408 (was 2.2111 and 1.1054 for 2.2 and 1.1); the
  age word's pin (1 + k_s + v / c) / (1 + k_r) = 1.0308 is not read until
  the emulation is re-declared, the design's to do.
- **Re-read on `main` and the receding world re-declared at the age word's
  k (2026-09-21, the Replicator; Far 2's flag, record 463 (ii)).** The five
  worlds run again on `main` at e531de5c (`tools/run_series.py --jobs 3`,
  500 intervals, 1.6 to 2.2 s each) and read by the same method: every
  reading above digit for digit (DETECTOR: 6.5011 / 6.5011, 1.0000 /
  0.1539, 6.5011 / 1.0000, 6.5011 / 1.7353, and `alike_receding` 2.2239 /
  0.3408; the births 499 / 81, 81 / 499, 81 / 81, 137 / 81, 81 / 196; every
  ordinal arrived). The register's block `clock_age_v1` now carries, for
  `alike_receding`, the two k under the age word (5.5 times the presence
  word's) beside `k_reader_presence_word` and `k_source_presence_word`,
  and the statement that the shipped world paces the source's crowd at
  0.2 c / (1 + k) for the presence word's k (the world file unchanged), so
  the pin 1.0308 is not readable in this world
  (`pin_readable_in_the_shipped_world` false); it stands for a world whose
  crowd paces the age word's k, the design's re-declaration. The map
  `replicated` points at the Replicator's line
  ([REPLICATIONS](../../../docs/REPLICATIONS.md)).
