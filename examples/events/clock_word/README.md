# Series S: the clock's word, the presence or the age moment

The Boss's order of 2026-09-21 (12:45Z) to the G2 experimenter, a rule-353
experiment (a second pair of hands on the physicist's pin; the replicator
runs it again later): build the four worlds exactly as the physicist's read
pins them in [docs/designs/clock_age/NOTE.md](../../../docs/designs/clock_age/NOTE.md)
section 6 (the numbers from `clock_age_map.py` beside it), register them
under the next free series letter with the pins before the run, run them
under beam-v1 as declared (no change under `src/`), and read them. The
register's entry is [docs/EXPERIMENTS.md, "S, the clock's word"](../../../docs/EXPERIMENTS.md#s-the-clocks-word-2026-09-21);
the expectations with the `derivations` map are `expectations.json`
(written by `make_worlds.py`; the `replicated` map absent: measured once,
awaiting replication); the readings tool is `read_runs.py`.

## The question

BEAM_LAW section 3 step 5: after each self-creation a body owes
`by_clock(age, k n, d)` intervals, k the presence of other numbers' rows at
its Node, or on a table entry that reads `age` the age moment
`sum amount x age`. Two crowds of the same release F at different distances
are the same push; only the age clock reads the distance. The presence
word gives the form `M / r^2`, the age word `M / r` (the potential, the form
nature's clocks measure at two heights).

## The worlds

Series P's geometry (`../crowd_clock/make_worlds.py` imported for the fan
and the speeds): the lamp `s_px1` at rest at x = 10 (2^20 units, one unit
per self-creation on +x, the wheel [1, 64]); two `mass` sources at 3 or at
6 Links on +y and +z, each releasing F = 4915 units per interval on the fan
of nine toward the lamp's line; `suspension` [1, 2^16]; the detector fixed
at x = 110 measuring `s_px1` with `reads: "age"`; the bar 121 x 9 x 9 at 3
Links and 121 x 15 x 15 at 6; 500 intervals.

| World | the lamp's `mass` entry | distance | pinned count per self-creation | pinned k | pinned 1 + z (DETECTOR) | the first row at the lamp |
| --- | --- | --- | --- | --- | --- | --- |
| `presence_3.json` | `pass` | 3 | 4 F (two headings' rows, two intervals each) | 0.300 | 1.300 +- 0.02 | tick 6 |
| `presence_6.json` | `pass` | 6 | 4 F | 0.300 (the presence clock cannot tell the distances apart) | 1.300 +- 0.02 | tick 11 |
| `age_3.json` | `{"rule": "pass", "reads": "age"}` | 3 | 22 F (the ages 5, 6 per source) | 1.650 | 2.650 +- 0.05 | tick 6 |
| `age_6.json` | `{"rule": "pass", "reads": "age"}` | 6 | 42 F (the ages 10, 11) | 3.150 | 4.150 +- 0.05; the ratio of the two k 1.909 +- 0.05 (the continuum's 2.000) | tick 11 |

## Run and read

```bash
PYTHONPATH=src python examples/events/clock_word/make_worlds.py
PYTHONPATH=src python tools/run_series.py --jobs 2 --out artifacts/clock_word examples/events/clock_word/presence_3.json examples/events/clock_word/presence_6.json examples/events/clock_word/age_3.json examples/events/clock_word/age_6.json
PYTHONPATH=src python examples/events/clock_word/read_runs.py artifacts/clock_word
```

`tests/test_clock_word.py` pins the shipped worlds to the generator, the
lamp's count under each word at each distance (4 F, 4 F, 22 F, 42 F; the
first counting tick 6 and 11) and the algebra of the pin.
