# The massive record kind: the check worlds

The worlds of `massive-record-v1` (the chief physicist's design
[docs/designs/detector_law/MASSIVE_RECORD.md](../../../docs/designs/detector_law/MASSIVE_RECORD.md),
its section 11 the order of the engine's work; the build's plan
[docs/designs/detector_law/BUILD.md](../../../docs/designs/detector_law/BUILD.md),
its section 5 the worlds with their pins; the readings of the runs
[docs/designs/detector_law/BUILD_READINGS.md](../../../docs/designs/detector_law/BUILD_READINGS.md)).
A massive record is a record of the local detector law whose family declares a
`pair` `[num, den]` on the six-neighbour term of the rule (den > num: a gap, the
rest frequency cos omega_0 = num / den); a block is a cube of declared cells
carrying a lowered pair (the well of the pair) with a momentum per axis, a
coupling to light at its cells (one g with G, the dielectric of section 7,
folded into the rule's one division), a clock (the upward zero crossings of
its own record's sum across its cells) and, when declared, a cavity (its
record held at 0 outside its cells) or a take (`absorbing`). Every world here
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
3 P . P < 192^2 admits no K = 5 as an integer of the drive). The massive kind's
faces are periodic by default with the margin rule of section 11 item 4 checked
at load (the module `diagnostics/massive_record_margin`, its lines printed before
the run and recorded under `margin` in `run.json`; an axis whose periodic extent
is below the block's side is a folded axis, a layer's or a chain's, with no face
for the rule to compare). On the chains light's faces are open on x (a zero
face, a mirror): on the index chain at rest with the design script's geometry and
its window [1000, 1800], before either end's reflection reaches the probe; on
the moving-index chains with the script's geometry, where the reflection
from the face at x = 0 reaches the probe at about 3118 on the chain of 2200 and
4850 on the chain of 4000 (inside the windows, named in the readings; a trial
with light's faces periodic, the script's np.roll, moved the rest readings away
from the script's own numbers by the wrapped wave and was not kept).

| World | What it declares | Kind | The pin (COMPUTATION, `expectations.json`) | What its record reads |
| --- | --- | --- | --- | --- |
| `rest_20.json`, `rest_28.json` | one block at rest on a periodic 48^3 board, 3000 intervals: s = 20 at full depth (`[800, 809]`, the well `[800, 800]`), s = 28 at half depth (`[1600, 1618]`, the well `[1600, 1609]`), `margin` `"control"` | CONTROL | omega_b and the extent on the world's own board by the margin module (0.11046 and 5.73 Links; 0.13053 and 7.94), the design's 96^3 numbers beside them (`massive_board_margin.out`: 0.11066 and 5.7; 0.13184 and 8.2, the periodic image's shift) | GAMEBOARD: the block's count over the run (its `click` lines, the `clock` of its `block` lines) and the spectral peak of its record's sum against omega_b |
| `moving_20.json`, `moving_28.json` | the same blocks pushed to k = 3 on a periodic 64^3 board over a ramp of 1500 intervals and a hold of 8000, `mode_axis` x | PREDICTION (the block form's residual, eps 0.45 and 0.22) | section 8's one formula per world on its own 64^3 box, f / f_0 = omega_b(gamma_m s, g) / (gamma_m omega_b(s, g)): 0.7831 and 0.8048 (`massive_moving_pins.out`, recomputed by `pins.py` to four places); the first order 1 / gamma_m (1 - eps (gamma_m^2 - 1) / 2) = 0.7245 and 0.7712 beside it as the band's second term only | GAMEBOARD: the count per interval over the hold against the rest world's rate (the 64^3 box's rest mode against the 48^3 box's, the ratio printed) and the spectral peak over the hold; the pump's signature (light's energy drift per interval, the mode k = 2 pi / 3 on x), 0 identically here: no light and no coupling declared |
| `cavity_24.json` | the rest cavity of form (I): s = 24 with the kind's own pair `[800, 809]`, `cavity` true, on 48^3, 3000 intervals | CONTROL | the exact separable form cos omega = (num / den) cos(pi / (s + 1)): omega 0.19485, the period 32.25 intervals (the design's quadrature 0.19515, section 4's table) | GAMEBOARD: the count and the spectral peak against omega |
| `cavity_24_moving.json` | the cavity pushed to k = 3 on 64^3, the ramp and the hold as (ii) | CONTROL (the medium's clock) | 1 / gamma_m^2 = 0.6667 (section 8's cavity limit, `massive_block_clock_motion.out`) | GAMEBOARD: the hold's rate over the rest cavity's |
| `index_50.json`, `index_20.json`, `index_10.json` (at rest) and `index_reference.json` | the index block at rest on a chain of 1400 (x open for light): the kind `[7, 8]` (omega_0 = 0.50536), a block of side 12 at x = 900 with seed 0, a CAVITY with the kind's own pair (the design script's oscillator, held at 0 outside its cells), G `[1, 1]`, g 1 / 50, 1 / 20, 1 / 10; the light clock `[153, 100]` (omega 0.15021), a lamp at x = 600 with a train of 64 periods, a probe at x = 1100, 1850 intervals; the reference without the block | CONTROL of the coupling | the closed form n^2 = 1 + G g / (omega_0^2 - omega^2) at the declared integers: n = 1.0421, 1.1022, 1.1956 (the design's chain read 1.034, 1.083, 1.159 at its omega_0 = 0.5, the lattice's band 0.8 to 3.4 percent below the form) | GAMEBOARD: light's phase delay at the probe against the reference over the window [1000, 1800] (the script's), n = 1 + delay / (k s) |
| `index_moving_k3_toward.json`, `index_moving_k3_away.json`, the same at k = 4 (in motion), with `index_moving_rest_*.json` and `index_moving_reference_*.json` | the moving index on the design's chain of 2200: the source at 300 (a train of 200 periods), the probe at 1500, s = 24 with the well `[314, 315]` on the kind `[156, 157]`, g `[1, 200]`, G `[1, 1]`, light at omega 0.035 (`[3565, 10000]`), the block stepping from interval 2600 (`start`) toward the source from x = 1300 or away from x = 700; the block at rest at x = 1100 at omega and at each K's block-frame frequencies omega' = gamma_m omega (1 +- beta) with a reference at each clock | PREDICTION of the model as built | the same-Node ratios of the delay to the covariant expectation (n(omega') - 1) omega' gamma_m s / c on this chain (`massive_moving_index.out` at the design's head, the drive's pair carried): head-on 0.500, from behind 2.569 (the window's halves unequal there); at K = 4 no number (read beside K = 3) | GAMEBOARD: light's phase at the probe by projection on the window [3400, 4300] against the reference, the covariant expectation formed from the engine's own rest reading at omega'; the window's two halves; the pump's signature over the window |
| `index_moving_long_k3_away.json`, `index_moving_long_k4_away.json`, with their rest and reference worlds | the receding case on the longer chain of 4000, REGENERATED on the declared geometry of DECLARATIONS.md section 11 (2026-09-24): the source at 800, the probe at 2400, the block from x = 1500 stepping away from interval 3000, the window [3800, 5400] (the front at the probe at 2770, the reflection from x = 0 at 5543); the rest world at omega' away at x = 2100 (the first geometry, whose window sat inside the train's own arrival, withdrawn before any run) | PREDICTION (P) | the script's number on the same geometry (section 11): the lab phase delay +1.0144 rad over the window (the covariant expectation +0.2323, the ratio 4.37), the halves +0.5539 and +1.5234, the drift 1.2 x 10^-3 rad per interval; the bands +- 0.04 rad and +- 10 percent of the rate | the window's phase against the reference at omega and its drift rate (GAMEBOARD, the row's own reader), the pump beside |
| `deep_well_rest_40.json`, `deep_well_k3_40.json` | the deep well in motion (RUN_LIST.md step 3, the cavity row's control): a periodic 128 x 128 x 1 layer, the kind `[800, 809]`, the block s = 40 at full depth `[800, 800]` (eps 0.87, the relaxation time 11 intervals), the seed the bound mode's integer profile at 2^20 (`seed_on_the_mode`; the flat seed 2^20 HISTORY), the block centred at (44, 44); at rest 3500 intervals, and pushed to k = 3 over the ramp 1500 and the hold 8000 with `mode_axis` x | CONTROL | the one formula at the exact cone on the layer's own mode: 0.7531 (`expectations.json`, the RUN_LIST's number by `massive_layer_pins.py` beside) | DETECTOR: the clicks' mean interval over the hold over the rest world's; GAMEBOARD: the peaks and the pump |

| `layer_pin_rest_14.json`, `layer_pin_k3_14.json` | the layer pin world of MASSIVE_RECORD.md section 11 item 7: a periodic 200 x 200 x 1 layer, the kind `[3200, 3236]` (mu = 0.15), the block s = 14 at the well `[3200, 3227]` (g = mu^2 / 4), `margin` "pin" (s + 4 extents = 159 < 200); the `seed` the BOUND MODE'S INTEGER PROFILE at 2^20 over the whole layer (the generator's integers in the file, the same at both levels: the reader of record is the clicks, which a flat seed makes beat on this wide mode); at rest 3500 intervals, and pushed to k = 3 over the ramp 10000 (ten relaxation times of the well, DECLARATIONS.md section 8) and the hold 8000, the ticks 18500, with `mode_axis` x | PIN (layer) | the mode's period 42.33 at rest (omega_b 0.14844); in motion the one formula at the exact cone 0.8116 (the second order 0.8108 and light's 0.8132 the CONTROLS; the script's own layer reading 0.8113) | DETECTOR: the clicks over the hold, the reader of record; GAMEBOARD: the summed record's and the centre cell's peaks beside |

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
emitters' worlds (4b's `redshift_k3` and `redshift_control`, the light clock)
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
    python -m event_universe --init examples/events/massive_record/rest_20.json --output artifacts/massive_record/rest_20
    PYTHONPATH=src python examples/events/massive_record/read_runs.py
