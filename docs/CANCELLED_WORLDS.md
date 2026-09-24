# Cancelled worlds

This page marks as cancelled the world folders and files under `examples/events/`
that do not belong to the fifteen experiments. It follows the model owner's
question of 2026-09-25, "there are old worlds that no longer belong to us, are
they cancelled too?". See record 1869 of [the day's log](LOG_2026-09-20.md) and
the [cancelled branches](CANCELLED_BRANCHES.md).

A world listed here is cancelled. Nothing current cites it, no run of the
fifteen uses it, and no new work builds on it. It stays on disk as history:
its own old tests still load it until they are retired with it. Nothing is
deleted.

Kept, not listed:
- `detector_law/` and `massive_record/`, the fifteen's worlds (the older
  variants in `massive_record/` are listed below as cancelled).
- `moving_detector/`, the round trip's world (row 4c), current until the
  transponder replaces it.
- `entities/`, the tool library.
- The gate's configuration: `gate_set.json`, `expectations.json`, `README.md`.

## The fifteen's world files

Listed by Nature24 from RUN_LIST.md's file column. Each experiment is given with
its settings and controls, all under `examples/events/`.

| Experiment | World files |
| --- | --- |
| 2a, the two slits | `detector_law/two_slits.json` |
| 5a, the pace fans | `detector_law/pace_fan_12.json`, `pace_fan_16.json`, `pace_fan_24.json` |
| 4a, the muon's form | `massive_record/layer_pin_rest_14.json`, `layer_pin_k3_14.json` |
| 4b, the redshift | `massive_record/redshift_k3.json`, `redshift_control.json` |
| 4c, the transponder | `moving_detector/cart_k3.json`, until the transponder's world replaces it |
| R2, the Sagnac ratio | `massive_record/sagnac_k3.json`, `sagnac_rest.json` |
| M1, de Broglie's fringes | `massive_record/matter_waves_12.json` |
| M2, the energy of a moving mass | `massive_record/matter_front_12.json` |
| (ii-a), (ii-b), the bound clock's second term | `massive_record/moving_20.json`, `moving_28.json`, `rest_20.json`, `rest_28.json` |
| The deep well in motion and its cavity control | `massive_record/deep_well_k3_40.json`, `deep_well_rest_40.json` |
| The light clock of two bodies | `massive_record/light_clock_60.json` |
| (v-m), the receding index at k = 3 | `massive_record/index_moving_long_k3_away.json`, `index_moving_long_rest_k3_away.json`, `index_moving_long_reference_k3_away.json` |
| 1a to 1d, Bell's four settings | `detector_law/bell_a0b0.json`, `bell_a0b1.json`, `bell_a1b0.json`, `bell_a1b1.json` |
| 9, Malus and the three settings | `detector_law/malus_45.json`, `malus_11.25.json`, `malus_28.125.json`, `malus_33.75.json` |
| The receding index at k = 4 | `massive_record/index_moving_long_k4_away.json`, `index_moving_long_rest_k4_away.json`, `index_moving_long_reference_k4_away.json` |

Rows A, A2 and B have no world. `massive_record/expectations.json` and
`readings.json` are the generator's records, not worlds.

## Cancelled

| World | World files | Last change | Kind |
| --- | --- | --- | --- |
| `amplitude/` | 74 | 2026-09-23 | folder |
| `atoms/` | 7 | 2026-09-23 | folder |
| `bell/` | 20 | 2026-09-23 | folder |
| `binding/` | 3 | 2026-09-23 | folder |
| `bohr/` | 7 | 2026-09-23 | folder |
| `c_measured/` | 2 | 2026-09-23 | folder |
| `clock_word/` | 6 | 2026-09-23 | folder |
| `coupling/` | 21 | 2026-09-23 | folder |
| `covariant/` | 5 | 2026-09-23 | folder |
| `detector/` | 4 | 2026-09-23 | folder |
| `drive_b/` | 7 | 2026-09-23 | folder |
| `flow_link/` | 15 | 2026-09-23 | folder |
| `heisenberg/` | 8 | 2026-09-23 | folder |
| `hubble/` | 4 | 2026-09-23 | folder |
| `hubble_stars/` | 5 | 2026-09-23 | folder |
| `lamp_shell/` | 4 | 2026-09-23 | folder |
| `lensing/` | 9 | 2026-09-23 | folder |
| `massive_rows/` | 4 | 2026-09-23 | folder |
| `newton_side/` | 4 | 2026-09-23 | folder |
| `nucleus/` | 8 | 2026-09-23 | folder |
| `optical/` | 35 | 2026-09-23 | folder |
| `orbit/` | 8 | 2026-09-23 | folder |
| `orbit_lamp/` | 15 | 2026-09-23 | folder |
| `quarks/` | 8 | 2026-09-23 | folder |
| `redshift/` | 2 | 2026-09-23 | folder |
| `shell_clock/` | 11 | 2026-09-23 | folder |
| `weak/` | 12 | 2026-09-23 | folder |
| `one_content.json` | 1 | 2026-09-23 | a Beam Law world at the root, written by `make_worlds.py` |
| `two_contents.json` | 1 | 2026-09-23 | a Beam Law world at the root, written by `make_worlds.py` |
| `one_slit.json` | 1 | 2026-09-23 | a Beam Law world at the root, written by `make_worlds.py` |
| `two_slits.json` | 1 | 2026-09-23 | a Beam Law world at the root, written by `make_worlds.py` |
| `massive_record/cavity_24.json` | 1 | 2026-09-24 | an older variant, cited by no row |
| `massive_record/cavity_24_moving.json` | 1 | 2026-09-24 | an older variant, cited by no row |
| `massive_record/index_10.json` | 1 | 2026-09-24 | an older variant, cited by no row |
| `massive_record/index_20.json` | 1 | 2026-09-24 | an older variant, cited by no row |
| `massive_record/index_50.json` | 1 | 2026-09-24 | an older variant, cited by no row |
| `massive_record/index_reference.json` | 1 | 2026-09-24 | an older variant, cited by no row |
| `massive_record/index_moving_k3_away.json` | 1 | 2026-09-24 | an older variant, cited by no row |
| `massive_record/index_moving_k3_toward.json` | 1 | 2026-09-24 | an older variant, cited by no row |
| `massive_record/index_moving_k4_away.json` | 1 | 2026-09-24 | an older variant, cited by no row |
| `massive_record/index_moving_k4_toward.json` | 1 | 2026-09-24 | an older variant, cited by no row |
| `massive_record/index_moving_reference_k3_away.json` | 1 | 2026-09-24 | an older variant, cited by no row |
| `massive_record/index_moving_reference_k3_toward.json` | 1 | 2026-09-24 | an older variant, cited by no row |
| `massive_record/index_moving_reference_k4_away.json` | 1 | 2026-09-24 | an older variant, cited by no row |
| `massive_record/index_moving_reference_k4_toward.json` | 1 | 2026-09-24 | an older variant, cited by no row |
| `massive_record/index_moving_reference_omega.json` | 1 | 2026-09-24 | an older variant, cited by no row |
| `massive_record/index_moving_rest_k3_away.json` | 1 | 2026-09-24 | an older variant, cited by no row |
| `massive_record/index_moving_rest_k3_toward.json` | 1 | 2026-09-24 | an older variant, cited by no row |
| `massive_record/index_moving_rest_k4_away.json` | 1 | 2026-09-24 | an older variant, cited by no row |
| `massive_record/index_moving_rest_k4_toward.json` | 1 | 2026-09-24 | an older variant, cited by no row |
| `massive_record/index_moving_rest_omega.json` | 1 | 2026-09-24 | an older variant, cited by no row |
| `massive_record/index_moving_long_reference_omega.json` | 1 | 2026-09-24 | an older variant, cited by no row |
| `massive_record/matter_waves_16.json` | 1 | 2026-09-24 | an older variant, cited by no row |
