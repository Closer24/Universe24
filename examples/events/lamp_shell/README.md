# The k_a(b) lamp shell: the crowd's stretch at the impact distance read by clicks (row 13, STEP 2; 2026-09-23)

The world pair of STEP 2 of
[docs/designs/fail_rows/RUN_13_2A.md](../../../docs/designs/fail_rows/RUN_13_2A.md)
(sections 1, 2 (a) and 3), ordered by the Boss on 2026-09-23 at 01:00Z on
the physics-rule reviewer's read of that file at ba558c0e: the one number
of row 13's chain that is not between clicks, the crowd's stretch at the
impact distance b (the continuum's shell mean k_cont(6) = 0.01127 through
which the ring's 0.731 Links becomes a coefficient, GAMEBOARD), replaced
by a click. Written by `make_worlds.py` with the expectations BEFORE any
run (`expectations.json`, every pin from the step algebra's crowd,
[step_algebra_map.py](../../../docs/designs/light_bending/step_algebra_map.py)
imported, no number typed by hand). A research run, made once, never a
test; a reading outside its pin is reported with its numbers, never
moved. Every number is one of the kinds of
[the register](../../../docs/EXPERIMENTS.md) ("Two kinds of readings"):
DETECTOR (a lamp's count ratio from click lines), COMPUTATION (the shell
mean, the plane ring's mean and the deciding ratio, arithmetic on the
clicks), GAMEBOARD (the age moments the pins were computed from, the
lever-arm factor, the back-reaction, named so) or HOST.

## The worlds

The ring world `flow_link/ring_b6_g1` (series K's open box 57 x 41 x 41,
the mass of the free phase-less family `m` at the centre with content
2^16 releasing on the fan of 290 primitive directions within Manhattan 6,
the pair `suspension` [1, 16384] with `width` 16384, the keys `optical: 1`
and `flow_link: true`, the screen x = 54 of one-Node `wave` detectors
reading `age`) with the ring of 40 lamps on the plane x = 2 replaced by a
SHELL of lamps of the paid family `light`: one fixed measured event at
every Node with |sqrt(x^2 + y^2 + z^2) - 6| < 1 / 2 about the mass (450
Nodes; the 40 Nodes at x = 0 are the ring's plane), each with the entry
`{"m": {"rule": "pass", "reads": "age"}}` so that its own clock counts the
crowd's AGE MOMENT at its Node (the same A that stretches a light row's
wall under the key; `{"m": "pass"}` would count the presence), releasing
one unit per self-creation on the one heading of its largest coordinate
pointing away from the mass (ties to x, then y): no row meets the mass's
Node, every row reaches a face of the open box or the screen's plane,
both detectors; a row that crosses another shell lamp's Node is measured
there (the family's default rule at a measured event), a click like any
other. 1200 intervals. Every declaration is an existing world key.

| World | the mass | lamps | keys | intervals |
| --- | --- | --- | --- | --- |
| `shell_b6_g1` | 2^16 at the pin n S = d | 450 on the shell r = 6 | `optical: 1`, `flow_link: true` | 1200 |
| `shell_b6_control_g1` | none | the same | the same | 1200 |

## The reading and the pins, before the run (`expectations.json`)

The reading, DETECTOR: per lamp, the `click` lines that carry a `record`
(a face's, a screen pixel's, or another lamp's) grouped by `number` (the
emitter's measured number, the lamp), the birth ordinal (`record &
0xFFFFFFFF`) against the click's tick over the window [200, 1200), 1 + k
the inverse slope (series T's reading, `shell_clock/read_runs.py`'s
`slope`); `read_lamps.py` reads the click lines alone, no store, no
`state.json`, no replay.

| The reading | Kind | The pin | The bracket |
| --- | --- | --- | --- |
| k_shell, the mean over the 450 lamps of the count ratio less 1 | COMPUTATION on the DETECTOR readings | 0.011202 (the crowd's shell mean of the age moment at r = 6, 183.54, times 1 / 16384; 0.993 of k_cont = 0.01127; the README's 0.0445 of the gr_rows pin world is this number at [1, 4096], 0.0448) | 3.4 percent of itself (the ring's own, 0.025 / 0.731): 0.01082 to 0.01159; the reading's grain 0.04 percent |
| k_plane, the mean over the 40 lamps at x = 0 | COMPUTATION on the DETECTOR readings | 0.022852 (the comb of the coordinate plane, twice the shell's; not the chain's k_a(b), pinned beside it) | 0.00004 |
| each lamp's k | DETECTOR | A_i / 16384, A_i the crowd's age moment at its Node (GAMEBOARD until read), listed per lamp | 0.00004 (the reading's grain over the window) |
| each control lamp's count ratio | DETECTOR | 1.0000 exactly | none |
| the deciding ratio alpha_nodes / k_shell, alpha_nodes = 0.731 / 26 the registered ring run's mean radial shift over the half path (DETECTOR, `flow_link/expectations.json`) | COMPUTATION on two DETECTOR readings | 2.510; through the lever-arm factor 0.683 (the walk's, GAMEBOARD) 3.675 | 2.42 to 2.60; 2 c_f = 4 on the comparison side only |

**What refutes:** k_shell outside its bracket (the crowd's stretch at b
is not the algebra's shell mean; every number of row 13 conditional on
it moves by the ratio read over pinned, the cause to be found in the
lamps' own clicks before any number moves); a lamp off its A_i / 16384
by more than the grain; a control off 1.0000; the ratio outside its
bracket. A refusal by the working bound is a register's finding,
reported, no pin moved (the algebra puts every pushed row of these lamps
a factor 3 inside the split ladder's bound, RUN_13_2A.md section 2 (a)).

**The host's cost, estimated before the run (HOST):** the ring world (40
lamps, 400 intervals) ran 64 s and 157 MB on this class of host; the
shell's 450 rows per interval alive about 45 intervals are half the
crowd's rows in flight, so 2 to 3 times the cost per interval over 1200
intervals: 6 to 10 minutes and about 1 GB per world, the control less;
run.json's record of 540 000 records the larger file.

## Run and read

```bash
PYTHONPATH=src python examples/events/lamp_shell/make_worlds.py
PYTHONPATH=src python tools/run_series.py --jobs 2 --out artifacts/lamp_shell examples/events/lamp_shell/shell_b6_g1.json examples/events/lamp_shell/shell_b6_control_g1.json
PYTHONPATH=src python examples/events/lamp_shell/read_lamps.py artifacts/lamp_shell
```

## The one run (2026-09-23): every falsifier silent, the shell mean and the ratio inside, the per-lamp pin FAIL by its grain

`tools/run_series.py --jobs 2`, 1200 intervals, headless (Python
3.14.0rc2, numpy 2.5.3; this host 4 cores, 15 GB). The source sha256 of
the world files `bc994db7456a7907` (`shell_b6_g1`) and `23903c999eaed057`
(the control); both completed and conserved (the digests, the seconds
and the peak memory under `runs_2026_09_23` of `expectations.json`, from
the runner's `summary.json`). HOST: 496 s and 1908 MB (the mass world),
300 s and 1921 MB (the control), the estimate's time and twice its
memory. Read by `read_lamps.py`; the per-lamp readings in
`readings.json`; the verdicts under `runs_2026_09_23`; no pin moved.

| The reading | Kind | Read | The pin | Verdict |
| --- | --- | --- | --- | --- |
| k_shell | COMPUTATION on 450 DETECTOR readings | 0.011210 (by the lamps' own births 0.011199, beside) | 0.011202, the bracket 0.010819 to 0.011585 | PASS |
| k_plane | COMPUTATION on 40 DETECTOR readings | 0.022861 | 0.022852 +- 0.00004 | PASS |
| the ratio alpha_nodes / k_shell | COMPUTATION on two DETECTOR readings | 2.508 (through the lever arm 0.683: 3.672) | 2.510, the bracket 2.424 to 2.596 | PASS |
| the controls | DETECTOR | 1.0000 exactly at every lamp | 1.0000 | PASS |
| each lamp against A_i / 16384 | DETECTOR | 441 of 450 inside by the clicks (426 by the own births) | +- 0.00004 | FAIL as written: eight lamps one Link downstream of another lamp's beam count its arriving rows (990 clicks at age 1 each; +0.39 n / d by their births, +1.0 to +1.37 by the clicks), and the click ticks carry the flight's residue at birth, a grain the pin did not carry ((-6, 0, 0) at -0.67 n / d by the clicks, -0.17 by its births as its five axis partners); the cause the reading's, not the crowd's; the account in RUN_13_2A.md section 9 |

What the run establishes: the crowd's stretch at the impact distance
read by clicks is the algebra's shell mean to 0.07 percent, 0.993 of the
continuum's; row 13's one GameBoard input is a click. It establishes no
physical law: c_f = 2 an input, n S = d a declaration, 4 on the
comparison side.
