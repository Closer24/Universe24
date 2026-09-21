# Series S: a reader inside a crowd

The model owner's word (2026-09-21, in conversation): "start", on the
experimenter's proposal, after series P and Q, of a detector that sits
inside a crowd itself, as Earth sits inside the Milky Way. The design with
the expectation pinned before any run is
[docs/designs/reader_clock/DESIGN.md](../../../docs/designs/reader_clock/DESIGN.md);
this folder holds the five worlds it declares, written by `make_worlds.py`
(which imports series P's generator, `../crowd_clock/make_worlds.py`), and
`expectations.json`. Nothing is registered.

## The worlds

A reader (`s_px1`, fixed at x = 10, measuring `s_px1` with `reads: "age"`,
with a lamp of its own on -x so that its births are its own clock) and a
source (`s_px1` at x = 70, a lamp shining -x to the reader), each with or
without series P's crowd (two `mass` sources, the fan of nine directions,
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
