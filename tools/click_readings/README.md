# The readings of a click

The one boundary of the click code's reading side (the model owner's word of
2026-09-22, record 871 of docs/LOG_2026-09-20.md: "order the new code of the
clicks"; the table [docs/designs/register_paper_sources/PLAN.md](../../docs/designs/register_paper_sources/PLAN.md),
section C). Every module here reads a run's record (`run.json`,
`events.jsonl`, `state.json`) written by the runner or by
`tools/run_series.py`, and prints or registers the readings of one series
of [the register](../../docs/EXPERIMENTS.md): the clicks alone, labelled
DETECTOR, and the GameBoard's lines, labelled GAMEBOARD and never pinned
(the model owner, 2026-09-21, record 281). Nothing here runs a rule of the
law, reads a Node during a run or moves a pin: a tool compares a reading
with the pins of its series' `expectations.json`, written before the run,
and prints a reading outside its pin with its numbers.

One module per series, named by the series' subject; each is run as a
script with `PYTHONPATH=src python tools/click_readings/<module>.py ...`
(its usage line is in its docstring) and loaded by its path in its test:

| Module | Series | Test |
| --- | --- | --- |
| `bell.py` | A2, the Bell run (the CHSH reading) | `tests/test_nature_beam_worlds.py` |
| `bell_choosers.py` | A2 with the choosers on the GameBoard | `tests/test_bell_choosers.py` |
| `bohr.py` | H, Bohr's lines behind the detector | `tests/test_bohr_readings.py` |
| `c_measured.py` | Q, c measured behind a detector | `tests/test_c_measured.py` |
| `coupling.py` | C, the couplings on the plane | `tests/test_coupling_readings.py` |
| `covariant.py` | S, the covariant readings | `tests/test_covariant_readings.py` |
| `heisenberg.py` | A10, the width of an opening | `tests/test_heisenberg_readings.py` |
| `hubble.py` | G, the Hubble diagram behind the detector | `tests/test_hubble_readings.py` |
| `hubble_stars.py` | G2, the Hubble diagram with stars | `tests/test_hubble_stars_readings.py` |
| `massive_rows.py`, `massive_rows_replay.py` | W, the massive rows (the reading of a run; the replay block of the register) | `tests/test_massive_rows.py` |
| `nucleus.py` | I, the nucleus | `tests/test_nucleus_readings.py` |
| `orbit.py` | D, the orbit on the plane | `tests/test_orbit_readings.py` |
| `orbit_lamp.py` | D3, Newton after a detector | `tests/test_orbit_lamp_readings.py` |
| `quarks.py`, `quarks_replay.py` | R, the quarks (the readings; the replay block of the register) | `tests/test_quarks_expectations.py` |
| `redshift.py` | E, the clock's redshift in space | `tests/test_redshift_readings.py` |
| `weak.py` | J, the weak force | `tests/test_weak_readings.py` |
| `lensing.py` | K, light beside a mass (and the optical pin worlds under the key) | `tests/test_lensing_readings.py` |
| `drive_b.py` | the directional drive of a body, drive-b-v1 | `tests/test_drive_b.py` |
| `shell_clock.py` | X, Poisson after a detector | `tests/test_shell_clock.py` |
| `clock_word.py` | T, the clock's word (the presence or the age moment) | none: no test loads it; `tests/test_clock_word.py` reads the worlds and the register (moved here on 2026-09-23 from `examples/events/clock_word/read_runs.py`) |
| `flow_link.py` | the ring worlds of flow-link-v1 (the world key `flow_link`) | none: no test loads it; `tests/test_flow_link.py` reads the worlds and the register, not the tool (moved here on 2026-09-23 from `tools/flow_link_readings.py`, PR #855's) |

Still outside the package: the cart's `tools/moving_detector_readings.py` (a
file of `moving-detector-build`, PR #834, held; PLAN.md section D).
`tools/amplitude_path.py` stays at its path because the paper's RECORD.md
cites it there.

## The clicks' certificate (the Boss's order of 2026-09-22 on the owner's word, record 920)

One row per readings tool the paper reaches. "Reads" names the record files
the tool opens (the runner's `run.json`, `events.jsonl`, `state.json`,
`initialization.json`, the loader's `resolved_initialization.json`) and
the world files; every tool reads and prints, and writes back only where
the row says (its own series' register block under `--register`, a
register's `runs` or `replay` block, or a `readings.json` beside the
worlds; never a pin). "Floats" says what the tool's floating-point numbers
are: the host's conversions of integer readings for display (the display
contract of SIMULATOR_DEFINITIONS.md), or a derived quantity the tool
computes from the counts outside the engine, named by its function for the
reviewer. Every count a tool prints as a reading is an integer of the
record; no tool runs a rule of the law or reads a Node during a run.

| Tool | Reads | Writes back | Floats | Derived outside the engine (named for the reviewer) |
| --- | --- | --- | --- | --- |
| `bell.py` (A2) | run.json, events.jsonl, initialization.json | nothing | the correlation E and S as ratios of counts, display | none: the CHSH sum is a count ratio |
| `bell_choosers.py` | run.json, events.jsonl, initialization.json | nothing | E per bin as a count ratio, display | none |
| `bohr.py` (H) | run.json, events.jsonl, initialization.json | nothing | the fit's slope, display | `slope` (a least-squares line over the counts) |
| `c_measured.py` (Q) | run.json, events.jsonl, initialization.json | nothing | the pace as a ratio of Links to intervals, display | `verdict` (the comparison with the pin) |
| `coupling.py` (C) | run.json, events.jsonl, initialization.json | a JSON report of the shell means (host, no pin) | the shell means and slopes (`diagnostics/shell_readings.py`, floating point, GAMEBOARD) | `slope`; the shell means are GAMEBOARD readings, labelled |
| `covariant.py` (S) | run.json, events.jsonl, state.json, initialization.json, resolved_initialization.json | the register's `runs` block under `--register` (the source sha, the digests, the readings; the pins untouched) | gamma and z as ratios of integers, display | none: the 64th self-creation, the face clicks and z are counts and count ratios |
| `heisenberg.py` (A10) | run.json | nothing | the spread's rms and the product, display | `rms` (the width of the count histogram) |
| `hubble.py` (G) | run.json, events.jsonl, initialization.json | nothing | 1 + z per window as a count ratio; the fit | a host fit over DETECTOR counts: the counts DETECTOR, the slope a derivation (`fit_points`, `fit_window`, `milne`, `slope`, `rms`, `window_point`, the Hubble fit against the Milne shape) |
| `hubble_stars.py` (G2) | run.json, events.jsonl, initialization.json, resolved_initialization.json | the register's run block (the readings beside the pins) | 1 + z per window; q from the fit | a host fit over DETECTOR counts: the counts DETECTOR, q a derivation (`fit_q`, `fit_points`, `fit_window`, `milne`, `slope`, `rms`, `verdict`, `window_point`) |
| `massive_rows.py` (W) | run.json, events.jsonl, initialization.json | the register's run block | the Pearson correlation of the clicks with the weights, display | `pearson` |
| `massive_rows_replay.py` (W) | run.json, events.jsonl, state.json | the register's `replay` block (the engine's digests, no pin) | none | none |
| `nucleus.py` (I) | run.json, events.jsonl, initialization.json | nothing | one ratio, display | `deciding` (the comparison with the pin) |
| `orbit.py` (D) | run.json, events.jsonl | nothing | the shell means as ratios, display | none: the inward push read as count ratios |
| `orbit_lamp.py` (D3) | run.json, events.jsonl | nothing | the crossings' ticks interpolated between bracketing births, the periods their spacings (T reads 407.3 and 813.3, not a count), T(24) / T(12) | `crossings_of` (the interpolation), the period ratio and the exponent |
| `quarks.py` (R) | run.json, events.jsonl, state.json, initialization.json | nothing | none | `deciding` (the comparison with the pin) |
| `quarks_replay.py` (R) | the world files | the register's `replay` block | none | none |
| `redshift.py` (E) | run.json, initialization.json | nothing | k as a ratio of counts, display | none |
| `weak.py` (J) | run.json, events.jsonl, initialization.json | nothing | the width over the median, display | `width` (the 10th-to-90th-percentile width over the median of the click ticks, printed GAMEBOARD, the lattice's clock), `deciding` |
| `tools/amplitude_path.py` (L) | run.json, events.jsonl | a JSON list of the clicks (the replay's report, no pin) | none | none: the layer's replay through `events/amplitude.py`, integers |
| `lensing.py` (K) | run.json, events.jsonl, initialization.json | the register's block under `--register` | the deflection in pixels and the delay in intervals as ratios, display | `slope` (the beam's centroid line), `verdict` |
| `drive_b.py` (drive-b-v1) | run.json, events.jsonl, state.json | the register's run block under `--register` | the pace as a ratio, display | none |
| `clock_word.py` (T) | events.jsonl | `readings.json` beside the worlds (the readings, no pin) | k and 1 + z as ratios of counts, display | `slope` (the clock's field over distance) |
| `shell_clock.py` (X) | events.jsonl, state.json | `readings.json` beside the worlds | k(r) as ratios, display | `slope` |
| `flow_link.py` (flow-link-v1) | run.json, events.jsonl, state.json (its digest), log.txt | the register's `runs` blocks under `--register` (the source sha256, the digests, the readings, the verdicts; the pins untouched) | the arrival's mean shift and delay as ratios of counts, the radial and tangential shifts, rounded for display | `sd_radial` (a standard deviation over the starts, `math.sqrt`); the COMPUTATION lines C_nodes and C_ring (the Nodes' conversion and the lever-arm factor of the pin, floating point, labelled COMPUTATION) |

Three tools compute a fit outside the engine and say so on their lines
(`hubble.py` and `hubble_stars.py`, the Milne shape and q; `coupling.py`,
the shell means in floating point through `diagnostics/shell_readings.py`);
every other derived number is a ratio, an rms or a slope of integer
counts. Nothing here is pinned but by the comparison with a register's
pin written before the run. The engine side of the same word is
`tests/test_integer_algebra.py`, the algebra gate on the physical modules.
