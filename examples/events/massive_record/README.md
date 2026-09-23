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
is written by `make_worlds.py` from the design's declarations, its kind
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
face, a mirror): on the index chain (v) with the design script's geometry and
its window [1000, 1800], before either end's reflection reaches the probe; on
the moving-index chains (v-m) with the script's geometry, where the reflection
from the face at x = 0 reaches the probe at about 3118 on the chain of 2200 and
4850 on the chain of 4000 (inside the windows, named in the readings; a trial
with light's faces periodic, the script's np.roll, moved the rest readings away
from the script's own numbers by the wrapped wave and was not kept).

| World | What it declares | Kind | The pin (COMPUTATION, `expectations.json`) | What its record reads |
| --- | --- | --- | --- | --- |
| `rest_20.json` (i-a), `rest_28.json` (i-b) | one block at rest on a periodic 48^3 board, 3000 intervals: s = 20 at full depth (`[800, 809]`, the well `[800, 800]`), s = 28 at half depth (`[1600, 1618]`, the well `[1600, 1609]`), `margin` `"control"` | CONTROL | omega_b and the extent on the world's own board by the margin module (0.11046 and 5.73 Links; 0.13053 and 7.94), the design's 96^3 numbers beside them (`massive_board_margin.out`: 0.11066 and 5.7; 0.13184 and 8.2, the periodic image's shift) | GAMEBOARD: the block's count over the run (its `click` lines, the `clock` of its `block` lines) and the spectral peak of its record's sum against omega_b |
| `moving_20.json` (ii-a), `moving_28.json` (ii-b) | the same blocks pushed to k = 3 on a periodic 64^3 board over a ramp of 1500 intervals and a hold of 8000, `mode_axis` x | PREDICTION (the block form's residual, eps 0.45 and 0.22) | section 8's one formula per world on its own 64^3 box, f / f_0 = omega_b(gamma_m s, g) / (gamma_m omega_b(s, g)): 0.7831 and 0.8048 (`massive_moving_pins.out`, recomputed by `pins.py` to four places); the first order 1 / gamma_m (1 - eps (gamma_m^2 - 1) / 2) = 0.7245 and 0.7712 beside it as the band's second term only | GAMEBOARD: the count per interval over the hold against the rest world's rate (the 64^3 box's rest mode against the 48^3 box's, the ratio printed) and the spectral peak over the hold; the pump's signature (light's energy drift per interval, the mode k = 2 pi / 3 on x), 0 identically here: no light and no coupling declared |
| `cavity_24.json` (iii-a) | the rest cavity of form (I): s = 24 with the kind's own pair `[800, 809]`, `cavity` true, on 48^3, 3000 intervals | CONTROL | the exact separable form cos omega = (num / den) cos(pi / (s + 1)): omega 0.19485, the period 32.25 intervals (the design's quadrature 0.19515, section 4's table) | GAMEBOARD: the count and the spectral peak against omega |
| `cavity_24_moving.json` (iii-b) | the cavity pushed to k = 3 on 64^3, the ramp and the hold as (ii) | CONTROL (the medium's clock) | 1 / gamma_m^2 = 0.6667 (section 8's cavity limit, `massive_block_clock_motion.out`) | GAMEBOARD: the hold's rate over the rest cavity's |
| `index_50.json`, `index_20.json`, `index_10.json` (v) and `index_reference.json` | the index block at rest on a chain of 1400 (x open for light): the kind `[7, 8]` (omega_0 = 0.50536), a block of side 12 at x = 900 with seed 0, a CAVITY with the kind's own pair (the design script's oscillator, held at 0 outside its cells), G `[1, 1]`, g 1 / 50, 1 / 20, 1 / 10; the light clock `[153, 100]` (omega 0.15021), a lamp at x = 600 with a train of 64 periods, a probe at x = 1100, 1850 intervals; the reference without the block | CONTROL of the coupling | the closed form n^2 = 1 + G g / (omega_0^2 - omega^2) at the declared integers: n = 1.0421, 1.1022, 1.1956 (the design's chain read 1.034, 1.083, 1.159 at its omega_0 = 0.5, the lattice's band 0.8 to 3.4 percent below the form) | GAMEBOARD: light's phase delay at the probe against the reference over the window [1000, 1800] (the script's), n = 1 + delay / (k s) |
| `index_moving_k3_toward.json`, `index_moving_k3_away.json`, the same at k = 4 (v-m), with `index_moving_rest_*.json` and `index_moving_reference_*.json` | the moving index on the design's chain of 2200: the source at 300 (a train of 200 periods), the probe at 1500, s = 24 with the well `[314, 315]` on the kind `[156, 157]`, g `[1, 200]`, G `[1, 1]`, light at omega 0.035 (`[3565, 10000]`), the block stepping from interval 2600 (`start`) toward the source from x = 1300 or away from x = 700; the block at rest at x = 1100 at omega and at each K's block-frame frequencies omega' = gamma_m omega (1 +- beta) with a reference at each clock | PREDICTION of the model as built | the same-Node ratios of the delay to the covariant expectation (n(omega') - 1) omega' gamma_m s / c on this chain (`massive_moving_index.out` at the design's head, the drive's pair carried): head-on 0.500, from behind 2.569 (the window's halves unequal there); at K = 4 no number (read beside K = 3) | GAMEBOARD: light's phase at the probe by projection on the window [3400, 4300] against the reference, the covariant expectation formed from the engine's own rest reading at omega'; the window's two halves; the pump's signature over the window |
| `index_moving_long_k3_away.json`, `index_moving_long_k4_away.json`, with their rest and reference worlds | the design's receding case on the longer chain of 4000: the source at 300, the probe at 2500, the block from x = 1500 from interval 2600, the window [5000, 6000]; the rest world at omega' away at x = 2100 | PREDICTION | the design's pin from behind (the Boss's 16:13Z): 6.74 with the drive's pair (4.28 with G g unchanged) | the same readings on the window [5000, 6000] |

The worlds NOT here: (i-c) and (ii-c), the four smallest binding sides as PIN
worlds of five (191^3 to 288^3 boards, hours each: the Boss's word on the
HOST cost, BUILD.md section 7); (iv), the light clock on two bodies and the
take world (after this series, per the order); the two-arm relay and light's
push on the block (MASSIVE_RECORD.md section 11 item 3 (b), a step after
(iv)); the layer worlds of item 7 (on the Boss's word).

Run from the repository root (the worlds, then the pins, then each world
headless, then the readings):

    PYTHONPATH=src python examples/events/massive_record/make_worlds.py
    PYTHONPATH=src python examples/events/massive_record/pins.py
    python -m event_universe --init examples/events/massive_record/rest_20.json --output artifacts/massive_record/rest_20
    PYTHONPATH=src python examples/events/massive_record/read_runs.py
