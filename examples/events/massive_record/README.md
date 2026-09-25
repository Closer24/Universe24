# The massive record kind: the check worlds

The worlds of `massive-record-v1` (the chief physicist's design
[docs/designs/detector_law/MASSIVE_RECORD.md](../../../docs/designs/detector_law/MASSIVE_RECORD.md),
its section 11 the order of the engine's work; the build's plan
[docs/designs/detector_law/BUILD.md](../../../docs/designs/detector_law/BUILD.md),
its section 5 the worlds with their pins; the readings of the runs
[docs/designs/detector_law/BUILD_READINGS.md](../../../docs/designs/detector_law/BUILD_READINGS.md)).
A massive record is a record of the local detector law whose family declares a
`pair` `[num, den]` on the six-neighbour term of the rule (den > num: a gap, the
rest frequency cos omega_0 = num / den); a block is a cube of declared Nodes
carrying a lowered pair (the well of the pair) with a momentum per axis (the
coupling to light at its Nodes RETIRED, the model owner's decision (2) of record
1962: mass and light meet only at the click; BUILD.md section 26 item 30), a
clock (the upward zero crossings of
its own record's sum across its Nodes); the cavity and the take are retired
(the cavity refused by name, BUILD.md section 26 item 28; the take, item 14). Every world here
is written by `make_worlds.py` from the design's declarations (since
body-check, 2026-09-24, every bound body's `seed` is the bound mode's integer
profile over the whole board at the declared amplitude, `seed_on_the_mode`,
on the model owner's word of 16:48Z: the engine refuses at load a body whose
initial state is not its mode, DECLARATIONS.md section 15 M1-11), its kind
(CONTROL, PIN or PREDICTION) and its pin written by `pins.py` into
`expectations.json` BEFORE the world runs and never moved after; `read_runs.py`
reads the run artifacts (`artifacts/massive_record/<world>/`) against the pins
into `readings.json`, every number labelled DETECTOR (a click), GAMEBOARD (a
diagnostic of the rows) or COMPUTATION (a number of the declaration). A reading
matches the algebra's number or does not; none is nature.

The pairs (BUILD.md section 5): at mu = 0.15 the medium D_out = 1 + mu^2 / 2 =
809 / 800 is the kind `[800, 809]`; the well at full depth g = mu^2 is D_in = 1,
the pair `[800, 800]`; at half depth the kind is written `[1600, 1618]` and the
well `[1600, 1609]`. The drive: the wall 3 Q S M = 192 (Q = 64, width 1, amount
1), so the momentum 64 on an axis is one Link every three intervals (k = 3,
beta_c = 1 / sqrt 3, gamma_m = sqrt(3 / 2)) and 48 is k = 4 (the pace bound
3 P . P < 192^2 admits no K = 5 as an integer of the drive). ONE BORDER FOR
EVERY FAMILY (BUILD.md section 26 item 28, 2026-09-25): every family reads the
world's `boundary` (the massive kind's own periodic faces, the family key
`faces`, HISTORY, refused by name at load), with the margin rule of section 11
item 4 checked at load (the module `diagnostics/massive_record_margin`, its
lines printed before the run and recorded under `margin` in `run.json`; an axis
whose periodic extent is below the block's side is a folded axis, a layer's or
a chain's, with no face for the rule to compare). A chain open on x is open for
light and for matter alike (a zero face beyond the ends, the receiver slab of
`face_depth` there, declared on every open board); the held index chains' notes
on their faces stand with their files (the section below). Every well declares
its `seed` (no loader default, item 28). Every world declares `node_clock`, the
Node clock's Gamma (10^6; ALGEBRA.md 9.35 (3); BUILD.md section 26 item 31: the
clock pair (Gamma - c, Gamma) at every Node under the fixed wall 3 den Gamma, c the
family of clicks' level there, item 34), and
`amplitude_bound` 2^28, its ceiling under the clock. Every world declares the
family `clicks` (the pair [1, 1], the quantum 1) and names it by `clock_family`
(ALGEBRA.md 9.45; item 32): the family of clicks, whose level at a Node is the
M of that Node's clock pair, held at every body's Nodes at the body's content
and spreading elsewhere by its own plain step, stepped last in the interval.

| World | What it declares | Kind | The pin (COMPUTATION, `expectations.json`) | What its record reads |
| --- | --- | --- | --- | --- |
| `boxed_clock_side_20_at_rest.json`, `boxed_clock_side_28_at_rest.json` | one block at rest on a periodic 48^3 board, 3000 intervals: s = 20 at full depth (`[800, 809]`, the well `[800, 800]`), s = 28 at half depth (`[1600, 1618]`, the well `[1600, 1609]`), `margin` `"control"` | CONTROL | omega_b and the extent on the world's own board by the margin module (0.11046 and 5.73 Links; 0.13053 and 7.94), the design's 96^3 numbers beside them (`massive_board_margin.out`: 0.11066 and 5.7; 0.13184 and 8.2, the periodic image's shift) | GAMEBOARD: the block's count over the run (its `click` lines, the `clock` of its `block` lines) and the spectral peak of its record's sum against omega_b |
| `boxed_clock_side_20_moving.json`, `boxed_clock_side_28_moving.json` | the same blocks pushed to k = 3 on a periodic 64^3 board over a ramp of 1500 intervals and a hold of 8000, `mode_axis` x | PREDICTION (the block form's residual, eps 0.45 and 0.22) | section 8's one formula per world on its own 64^3 box, f / f_0 = omega_b(gamma_m s, g) / (gamma_m omega_b(s, g)): 0.7831 and 0.8048 (`massive_moving_pins.out`, recomputed by `pins.py` to four places); the first order 1 / gamma_m (1 - eps (gamma_m^2 - 1) / 2) = 0.7245 and 0.7712 beside it as the band's second term only | GAMEBOARD: the count per interval over the hold against the rest world's rate (the 64^3 box's rest mode against the 48^3 box's, the ratio printed) and the spectral peak over the hold; the pump's signature (light's energy drift per interval, the mode k = 2 pi / 3 on x), 0 identically here: no light and no coupling declared |
| `medium_index_at_rest_50.json`, `medium_index_at_rest_20.json`, `medium_index_at_rest_10.json` (at rest) and `medium_index_reference.json` | the index block at rest on a chain of 1400 (x open for light): the kind `[7, 8]` (omega_0 = 0.50536), a block of side 12 at x = 900 with seed 0, a CAVITY with the kind's own pair (the design script's oscillator, held at 0 outside its Nodes), G `[1, 1]`, g 1 / 50, 1 / 20, 1 / 10; the light clock `[153, 100]` (omega 0.15021), a lamp at x = 600 with a train of 64 periods, a probe at x = 1100, 1850 intervals; the reference without the block | CONTROL of the coupling | the closed form n^2 = 1 + G g / (omega_0^2 - omega^2) at the declared integers: n = 1.0421, 1.1022, 1.1956 (the design's chain read 1.034, 1.083, 1.159 at its omega_0 = 0.5, the lattice's band 0.8 to 3.4 percent below the form) | GAMEBOARD: light's phase delay at the probe against the reference over the window [1000, 1800] (the script's), n = 1 + delay / (k s) |
| `receding_index_short_speed_third_toward.json`, `receding_index_short_speed_third_away.json`, the same at k = 4 (in motion), with `index_moving_rest_*.json` and `index_moving_reference_*.json` | the moving index on the design's chain of 2200: the source at 300 (a train of 200 periods), the probe at 1500, s = 24 with the well `[314, 315]` on the kind `[156, 157]`, g `[1, 200]`, G `[1, 1]`, light at omega 0.035 (`[3565, 10000]`), the block stepping from interval 2600 (`start`) toward the source from x = 1300 or away from x = 700; the block at rest at x = 1100 at omega and at each K's block-frame frequencies omega' = gamma_m omega (1 +- beta) with a reference at each clock | PREDICTION of the model as built | the same-Node ratios of the delay to the covariant expectation (n(omega') - 1) omega' gamma_m s / c on this chain (`massive_moving_index.out` at the design's head, the drive's pair carried): head-on 0.500, from behind 2.569 (the window's halves unequal there); at K = 4 no number (read beside K = 3) | GAMEBOARD: light's phase at the probe by projection on the window [3400, 4300] against the reference, the covariant expectation formed from the engine's own rest reading at omega'; the window's two halves; the pump's signature over the window |
| `receding_index_speed_third_away.json`, `receding_index_speed_quarter_away.json`, with their rest and reference worlds | the receding case on the longer chain of 4000, REGENERATED on the declared geometry of DECLARATIONS.md section 11 (2026-09-24): the source at 800, the probe at 2400, the block from x = 1500 stepping away from interval 3000, the window [3800, 5400] (the front at the probe at 2770, the reflection from x = 0 at 5543); the rest world at omega' away at x = 2100 (the first geometry, whose window sat inside the train's own arrival, withdrawn before any run) | PREDICTION (P) | the script's number on the same geometry (section 11): the lab phase delay +1.0144 rad over the window (the covariant expectation +0.2323, the ratio 4.37), the halves +0.5539 and +1.5234, the drift 1.2 x 10^-3 rad per interval; the bands +- 0.04 rad and +- 10 percent of the rate | the window's phase against the reference at omega and its drift rate (GAMEBOARD, the row's own reader), the pump beside |
| `deep_well_clock_at_rest_40.json`, `deep_well_clock_speed_third_40.json` | the deep well in motion (RUN_LIST.md step 3, the cavity row's control): a periodic 128 x 128 x 1 layer, the kind `[800, 809]`, the block s = 40 at full depth `[800, 800]` (eps 0.87, the relaxation time 11 intervals), the seed the bound mode's integer profile at 2^20 (`seed_on_the_mode`; the flat seed 2^20 HISTORY), the block centred at (44, 44); at rest 3500 intervals, and pushed to k = 3 over the ramp 1500 and the hold 8000 with `mode_axis` x | CONTROL | the one formula at the exact cone on the layer's own mode: 0.7531 (`expectations.json`, the RUN_LIST's number by `massive_layer_pins.py` beside) | DETECTOR: the clicks' mean interval over the hold over the rest world's; GAMEBOARD: the peaks and the pump |

| `muon_moving_clock_at_rest_14.json`, `muon_moving_clock_speed_third_14.json` | the layer pin world of MASSIVE_RECORD.md section 11 item 7: a periodic 200 x 200 x 1 layer, the kind `[3200, 3236]` (mu = 0.15), the block s = 14 at the well `[3200, 3227]` (g = mu^2 / 4), `margin` "pin" (s + 4 extents = 159 < 200); the `seed` the BOUND MODE'S INTEGER PROFILE at 2^20 over the whole layer (the generator's integers in the file, the same at both levels: the reader of record is the clicks, which a flat seed makes beat on this wide mode); at rest 3500 intervals, and pushed to k = 3 over the ramp 10000 (ten relaxation times of the well, DECLARATIONS.md section 8) and the hold 8000, the ticks 18500, with `mode_axis` x | PIN (layer) | the mode's period 42.33 at rest (omega_b 0.14844); in motion the one formula at the exact cone 0.8116 (the second order 0.8108 and light's 0.8132 the CONTROLS; the script's own layer reading 0.8113) | DETECTOR: the clicks over the hold, the reader of record; GAMEBOARD: the summed record's and the centre Node's peaks beside |

The pins' gamma: `pins.py` takes the exact cone of the massive kind's band,
c_eff^2 = cos omega_0 (omega_0 / sin omega_0) c^2 (MASSIVE_RECORD.md section 8
at the design's 14e3657e), for the moving worlds' pins, with the second order
(c_m) and light's gamma beside as CONTROLS; `expectations.json` was regenerated
so before any pinned run and after the exploratory readings of BUILD_READINGS.md,
which stay beside the numbers they were read against.

The folders `EXPLORATORY_layer_rest_14/` and `EXPLORATORY_layer_k3_14/` hold
copies of two exploratory runs (the events, the run's record without its audit,
the world file; no per-Node state) for the visualizer; EXPLORATORY, not
registered, their numbers in BUILD_READINGS.md's exploration log only (the
runs of the ramp 1500, before section 8 declared the ramp 10000).

The readers of clicks of the launch list (RUN_LIST.md) are Builder 2's in
`read_runs.py` (`clicks_of`, `screen_clicks`, `light_clicks`; PRs #1073 and
#1076, `tests/test_detector_law_readers.py`). The launch
list's worlds this series does NOT hold, each named in BUILD.md section 12: the
emitters' worlds (4b's `moving_emitter_redshift_speed_third` and `moving_emitter_redshift_at_rest`, the light clock)
refused at load by MUST 3 with the declared g = [1, 50000]; the Sagnac, the
matter waves, the ray law's and the tables' worlds, whose declarations lack a
line the builder may not supply.

The worlds NOT here: (i-c) and (ii-c), the four smallest binding sides as PIN
worlds of five (191^3 to 288^3 boards, hours each: the Boss's word on the
HOST cost, BUILD.md section 7); (iv), the light clock on two bodies and the
take world (after this series, per the order); the two-arm relay and light's
push on the block (MASSIVE_RECORD.md section 11 item 3 (b), a step after
(iv)); the layer worlds of item 7 beyond its first row (on the Boss's word), and every pinned RUN, which waits on the owner's word and the Boss's GO.

Run from the repository root (the worlds, then the pins, then each world
headless, then the readings):

    PYTHONPATH=src python examples/events/massive_record/make_worlds.py
    PYTHONPATH=src python examples/events/massive_record/pins.py
    python -m event_universe --init examples/events/massive_record/boxed_clock_side_20_at_rest.json --output artifacts/massive_record/boxed_clock_side_20_at_rest
    PYTHONPATH=src python examples/events/massive_record/read_runs.py

## The born train and the rows held under it (2026-09-25; ALGEBRA.md 9.17 (6a); BUILD.md section 26 item 27)

Every birth is a travelling train: an emitting body carries `train` (the direction and the periods) and `born` (the train's two levels over its Nodes and its norm on the vacuum, the generator's integers, checked at load). THE LIGHT CLOCK (`light_clock.json`, written by the detector-law generator into this folder) stands in the one table's form: [760, 3, 3] periodic on y and z, x open with the face slabs 32 deep, N = 1024, light with the born clock [512, 1], A [800, 801] of the extents [32, 3, 3] at [600, 632) with its coupling, its seed on its mode and a stock of 64, its train along +x, the mirror the gap [1, 2] over [4, 3, 3] at [690, 694), the set `at_well` A's own Nodes; its blind pins in `../pins.json` (the mean click interval 300 +- 9, the first click 250 +- 8). THE ROWS HELD under the train, their files moved as written (the one-Node birth, HISTORY) to `docs/designs/detector_law/held_worlds/` and their builders retired here, to be rebuilt from the table of ALGEBRA.md 9.22 (8) through the generator: `sagnac_light_times_at_rest`, `sagnac_light_times_speed_third`, `moving_emitter_redshift_at_rest`, `moving_emitter_redshift_speed_third`, `de_broglie_fringes_12`, `de_broglie_fringes_16`, `moving_mass_energy_12`, the four `medium_index_*` and the twenty-one `receding_index_*` worlds (the eight short rest and reference worlds without an emitter held with their row). The readers `pins.py`, `read_runs.py`, `expectations.json` and `readings.json` name them as HISTORY. The worlds this generator still writes: the four boxed clocks, the two cavities, the two muon layers and the two deep wells.

CANCELLED WITH THE CAVITY (2026-09-25; BUILD.md section 26 item 28): `cavity_24.json` and
`cavity_24_moving.json` (the rest cavity of form (I) and the cavity pushed to k = 3) are
refused by name at load (a body's record is held by the law alone, its border the
world's) and stand as written in `docs/designs/detector_law/held_worlds/`; their pins in
`expectations.json` and their readings in `readings.json` are the record, never moved;
`pins.py` and `read_runs.py` keep their rows as written (HISTORY; neither runs under the
gate).

## The worlds' names since 2026-09-25 (the model owner's rule, record 1924; the names review, record 1925)

Every registered world of this folder is named by its experiment (the canonical names of the names review), the speed of a drive by its fraction of a Link per interval (`speed_third` for k = 3, `speed_quarter` for k = 4) and the rest world by `at_rest`; the world's identity (`model_id`) follows its name, so the files were regenerated under the new names (the same integers, the identity line the only change). The readers, the pins (`expectations.json`) and the readings (`readings.json`) carry the new keys. The migration, old to new:

| Was | Is |
| --- | --- |
| `light_clock_60` | `light_clock` |
| `sagnac_k3` | `sagnac_light_times_speed_third` |
| `sagnac_rest` | `sagnac_light_times_at_rest` |
| `redshift_k3` | `moving_emitter_redshift_speed_third` |
| `redshift_control` | `moving_emitter_redshift_at_rest` |
| `matter_waves_12` | `de_broglie_fringes_12` |
| `matter_waves_16` | `de_broglie_fringes_16` |
| `matter_front_12` | `moving_mass_energy_12` |
| `layer_pin_rest_14` | `muon_moving_clock_at_rest_14` |
| `layer_pin_k3_14` | `muon_moving_clock_speed_third_14` |
| `deep_well_rest_40` | `deep_well_clock_at_rest_40` |
| `deep_well_k3_40` | `deep_well_clock_speed_third_40` |
| `rest_20` | `boxed_clock_side_20_at_rest` |
| `moving_20` | `boxed_clock_side_20_moving` |
| `rest_28` | `boxed_clock_side_28_at_rest` |
| `moving_28` | `boxed_clock_side_28_moving` |
| `index_50` | `medium_index_at_rest_50` |
| `index_20` | `medium_index_at_rest_20` |
| `index_10` | `medium_index_at_rest_10` |
| `index_reference` | `medium_index_reference` |
| `index_moving_rest_omega` | `receding_index_short_omega_rest` |
| `index_moving_reference_omega` | `receding_index_short_omega_reference` |
| `index_moving_long_reference_omega` | `receding_index_omega_reference` |
| `index_moving_k3_toward` | `receding_index_short_speed_third_toward` |
| `index_moving_rest_k3_toward` | `receding_index_short_speed_third_toward_rest` |
| `index_moving_reference_k3_toward` | `receding_index_short_speed_third_toward_reference` |
| `index_moving_k3_away` | `receding_index_short_speed_third_away` |
| `index_moving_rest_k3_away` | `receding_index_short_speed_third_away_rest` |
| `index_moving_reference_k3_away` | `receding_index_short_speed_third_away_reference` |
| `index_moving_long_k3_away` | `receding_index_speed_third_away` |
| `index_moving_long_rest_k3_away` | `receding_index_speed_third_away_rest` |
| `index_moving_long_reference_k3_away` | `receding_index_speed_third_away_reference` |
| `index_moving_k4_toward` | `receding_index_short_speed_quarter_toward` |
| `index_moving_rest_k4_toward` | `receding_index_short_speed_quarter_toward_rest` |
| `index_moving_reference_k4_toward` | `receding_index_short_speed_quarter_toward_reference` |
| `index_moving_k4_away` | `receding_index_short_speed_quarter_away` |
| `index_moving_rest_k4_away` | `receding_index_short_speed_quarter_away_rest` |
| `index_moving_reference_k4_away` | `receding_index_short_speed_quarter_away_reference` |
| `index_moving_long_k4_away` | `receding_index_speed_quarter_away` |
| `index_moving_long_rest_k4_away` | `receding_index_speed_quarter_away_rest` |
| `index_moving_long_reference_k4_away` | `receding_index_speed_quarter_away_reference` |

The light clock's receiving set is `at_well` (was `at_a`); Sagnac's two sets are `at_near_well` beside the body at x = 700 and `at_far_well` beside the body at x = 772 (were `at_a` and `at_b`). The exploratory folders keep their names as history.
