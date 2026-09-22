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

Still outside the package until the branches that touch them merge (PLAN.md
section D): `tools/lensing_readings.py` (K), `tools/drive_b_readings.py`
(the directional drive), `examples/events/clock_word/read_runs.py` (T),
`examples/events/shell_clock/read_runs.py` (X) and the cart's
`tools/moving_detector_readings.py`. `tools/amplitude_path.py` stays at its
path because the paper's RECORD.md cites it there.
