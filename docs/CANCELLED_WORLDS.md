# Cancelled worlds and paths: deleted

The ray law's paths were marked cancelled on 2026-09-26 (the model owner's records 1875 and
2095; the Boss's records 2102, 2107 and 2133) and deleted the same day on the owner's word
(the Boss's record 2220: "few lines of code for the whole project"). Git history keeps every
file: the last commit of `main` that holds them all is `fbfed39f`, and one path comes back with

    git checkout fbfed39f -- <path>

## 1. What was deleted (the Boss's record 2220; Nature24, branch feature/remove-cancelled-code)

| Kind | Count | Where they were | Python lines |
| --- | --- | --- | --- |
| world folders (worlds, generators, registers, readers, notes) | 29 | `examples/events/amplitude`, `atoms`, `bell`, `binding`, `bohr`, `c_measured`, `clock_word`, `coupling`, `covariant`, `detector`, `drive_b`, `entities`, `flow_link`, `heisenberg`, `hubble`, `hubble_stars`, `lamp_shell`, `lensing`, `massive_rows`, `moving_detector`, `newton_side`, `nucleus`, `optical`, `orbit`, `orbit_lamp`, `quarks`, `redshift`, `shell_clock`, `weak` | 14,862 |
| test files | 85 | `tests/test_amplitude_*.py`, `tests/test_nature_beam_*.py`, the readings tests, `tests/test_algebra_visualizer.py`, `tests/test_locality.py`, `tests/test_run_series_guard.py`, `tests/test_register_map.py`, `tests/test_run_series.py` and the rest of the list of the cancel | 30,755 |
| modules and tools | 42 | `src/event_universe/events/engine.py`, `nature_beam.py`, `meeting.py`, `run.py`; `src/event_universe/__main__.py`, `configuration_validation.py`, `json_documents.py`, `register_map.py`, `runner.py`, `snapshot_writer.py`, `trimmed_record.py`, `world_loading.py`, `diagnostics/shell_readings.py`; `tools/click_readings/*.py` but `detector_law_bell.py`; `tools/amplitude_path.py`, `amplitude_probe.py`, `moving_detector_readings.py`, `newton_side_readings.py`, `profile_run.py`, `run_series.py` | 24,098 |
| the gate's cancelled-paths machinery | 3 | `tools/cancelled_paths.py`, `tests/test_cancelled_paths.py`, `tests/test_gate_configuration.py`, with the `collect_ignore` of `tests/conftest.py`, the selector's filter in `tools/check.py`, the type checker's override and the script entry `event-universe` in `pyproject.toml` | 214 |

In all 515 files and 69,929 Python lines: `main` at `fbfed39f` held 157,545 Python lines, the
branch holds 87,527 (36,049 of them the design folders' scripts, records).

Every markdown link to a deleted path was turned into its text with the path in code font and
the word "deleted 2026-09-26". Nothing of the design folders under `docs/designs/` or of the
dated logs was deleted; the design scripts that imported the deleted modules are records and
do not run.

## 2. Listed whole, kept for now (the Boss's approval asked, record 2220)

| Path | Why it stays today |
| --- | --- |
| `src/event_universe/events/measured.py` | imported by `src/event_universe/events/amplitude.py` (a living file with a cancelled half, Main Loop's cut), so its deletion would break the type check of a file that is not this branch's to touch; it is the one module under the type checker's `ignore_errors` override. `amplitude.py` itself is imported by nothing living since `rungs` moved to `events/rule.py`, so it is proposed whole in section 4 |
| `docs/BEAM_LAW.md`, `docs/DERIVATIONS_BEAM.md` | the ray law's two documents, linked from about 460 places of the living documentation and Highlights; history, not code (0 Python lines) |

## 3. The cancelled halves in living files (Main Loop's cut; formerly section 9)

These stay imported by the living path; only the part named is cancelled, and it goes with
Main Loop's cut (record 2220), never in this deletion.

| Path | What is cancelled, what stays |
| --- | --- |
| `src/event_universe/__init__.py`, `src/event_universe/events/__init__.py` | the `__getattr__` that names the deleted engine's exports |
| `src/event_universe/events/amplitude.py` | the whole module reads nothing living; `rungs` lives in `events/rule.py` |
| `src/event_universe/events/world.py` | the ray law's half: `BEAM_LAW`, `LAW_VALUE`, `OLD_LAW_VALUE` (the law's name and version, 9.90 (1)); the seventeen rule constants (`BECOME_RULE` to `MASSIVE_ROWS_RULE`) and the parses keyed on them; `GRAVITY_COLUMN`, `CHARGE_COLUMN`, `COLUMN_SIGNS`, `COLUMN_KEYS`, `COLUMN_LIMIT`; `CHARGE_KEY`, `NO_CHARGE`; `LAMP_KEYS`, `TABLE_ENTRY_KEYS`, `SPLIT_KEYS`, `TRANSFORM_KEYS`, `BECOME_KEYS`, `CLOCK_ONLY_KEYS`, `WINDOW_READING_KEYS`, `TRANSIT_KEYS`; the detector law's parses stay |
| `src/event_universe/events/detector_law.py` | the unreachable giving branches (record 2220) |
| `tools/check.py` | its resource map is empty since the deletion; the check itself stays |
| `tools/preflight_worlds.py` | only its ray-law part; its detector-law part stays |

## 4. Code that nothing living reads (proposed; the Boss approves each item before deletion)

| Path | Python lines | Why it is dead |
| --- | --- | --- |
| `src/event_universe/events/amplitude.py` | 1025 | imported by the deleted `nature_beam.py`, `engine.py`, `amplitude_path.py` and `amplitude_probe.py` alone; `rungs` is `events/rule.py`'s |
| `src/event_universe/events/measured.py` | 1118 | listed whole; imported by `amplitude.py` alone |
| `examples/events/make_worlds.py` | 140 | the generator of the deleted root worlds (the old entities' families); it imports the deleted `world_loading.py` and no longer runs |
| `tools/click_readings/detector_law_bell.py` | 183 | the reader of the deleted Bell series' register; it imports the deleted `world_loading.py` and no longer runs |
| `tools/algebra_visualizer/` (5 files) | 5171 | its test `tests/test_algebra_visualizer.py` was cancelled and deleted; it renders the deleted runner's runs |
| `tests/support/hand_worlds.py` | 184 | used by no living test |
| `examples/events/one_slit.json`, `two_contents.json`, `two_slits.json`, `gate_set.json` | 0 (JSON) | the ray law's root worlds and its gate register, named by `examples/events/README.md` alone (`two_slits.json` as a path string in `tests/test_check_scope.py`); `one_content.json` stays as the preflight test's refused example, `expectations.json` and `pins.json` are read by living tests |
