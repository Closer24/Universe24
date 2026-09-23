# The massive record kind: the readings of the check worlds

The worlds of `examples/events/massive_record/` (its README the declarations;
`expectations.json` the pins written before any run by `pins.py`;
`readings.json` the numbers `read_runs.py` reads from the run artifacts), run
headless with `python -m event_universe` on this machine (numpy int64, one
process per world), each read against its pin: the engine's number against the
algebra's, by kind (DETECTOR a click; GAMEBOARD a diagnostic of the rows;
COMPUTATION a number of the declaration). A reading matches the algebra's
number or does not; none is nature. The plan is BUILD.md (section 5 the worlds
and their pins, section 10 the findings); the design MASSIVE_RECORD.md (section
11 the order, item 4 the margin rule, item 6 the schedule of the pins).

## (i) One block at rest, 48^3 periodic, 3000 intervals: CONTROL

The margin rule at load (COMPUTATION, `run.json` `margin`): (i-a) omega_b
0.11046, eps 0.4526, the extent 5.73 Links, the side 48 against 31.5;
(i-b) omega_b 0.13053, eps 0.2356, the extent 7.94, the side 48 against 43.9.

| World | The pin (COMPUTATION) | The clicks' mean interval (GAMEBOARD, the `click` lines over [200, 3000]) | The spectral peak of the record's sum (GAMEBOARD) | The count over the window |
| --- | --- | --- | --- | --- |
| (i-a) `rest_20` | omega_b 0.11046, the period 56.88 intervals | 56.896 (the pin's period to 0.03 percent) | 0.11023 (0.998 of the pin: the transform's grain over 2800 intervals) | 49 (the pin's 49.2) |
| (i-b) `rest_28` | omega_b 0.13053, the period 48.14 | 48.140 (to 0.01 percent) | 0.13034 (0.9985) | 58 (the pin's 58.2) |

The block's own clock at rest matches the margin module's bound mode on the
world's own board to the clicks' grain; the design's 96^3 numbers (0.11066,
0.13184) differ from the 48^3 board's by the periodic image (0.2 and 1
percent), and the world's own number is the pin (BUILD.md section 10 (b)).
Wall time: 6 minutes each (three worlds in parallel).

## (iii-a) The rest cavity of form (I), s = 24, 48^3, 3000 intervals: CONTROL

| World | The pin (COMPUTATION, the separable form) | The clicks' mean interval | The spectral peak | The count |
| --- | --- | --- | --- | --- |
| `cavity_24` | omega 0.19485, the period 32.25 | 32.244 (to 0.01 percent) | 0.19499 (1.0008) | 87 (the pin's 86.8) |

The rows outside the cube are held at 0 by the declaration; the count is the
exact separable form's.

## (v) The index block at rest on a chain of 1400: CONTROL of the coupling

The block a CAVITY with the kind's own pair `[7, 8]` (BUILD.md section 10 (m));
the light clock `[153, 100]`, omega 0.15021; the window [1000, 1800] (the
design script's, before either end's reflection reaches the probe).

| World | g | The pin n (COMPUTATION, the closed form) | n read (GAMEBOARD, the phase delay at the probe against `index_reference`) | The delay (rad) | n - 1 over the form's | The transmitted amplitude |
| --- | --- | --- | --- | --- | --- | --- |
| `index_50` | 1 / 50 | 1.0421 | 1.0366 | 0.1143 | 0.871 | 0.993 |
| `index_20` | 1 / 20 | 1.1022 | 1.0887 | 0.2770 | 0.868 | 0.993 |
| `index_10` | 1 / 10 | 1.1956 | 1.1702 | 0.5314 | 0.870 | 0.989 |

The engine's index sits 0.5, 1.2 and 2.1 percent below the closed form, the
excess n - 1 at 0.87 of the form's at all three couplings (one factor: the
lattice's band and the faces' steps, as the design's own chain read 0.79 to
0.81 of its form at its omega_0 = 0.5); the coupling's algebra reads as the
closed form's dielectric with the lattice's factor, the control met in form.
Wall time: seconds per world.

## (ii) The block pushed to k = 3 on 64^3, the ramp 1500 and the hold 8000: PREDICTION of the block form's residual

The margin rule at load on the 64^3 box (COMPUTATION): (ii-a) omega_b 0.11065,
eps 0.4508, the extent 5.74; (ii-b) 0.13170, 0.2219, 8.18. The pin is section
8's one formula on the world's own box (`massive_moving_pins.out`, recomputed
by `pins.py`): f / f_0 = omega_b(gamma_m s) / (gamma_m omega_b(s)) with the
moving block a resting well of width gamma_m s along the motion. The rest
frequency f_0 is the rest world's on 48^3, scaled by the two boxes' omega_b
(1.0017 and 1.0090); the hold [1500, 9500] holds 2912 steps (one Link every
2.75 intervals: the ramp's tail inside the window, then one every 3).

| World | The pin f / f_0 (COMPUTATION) | The first order 1 / gamma_m (1 - eps (gamma_m^2 - 1) / 2) | By the spectral peak over the hold (GAMEBOARD) | By the clicks' mean interval (rest over hold, box-scaled) | By the count over the hold | The peak (rad per interval) | The clicks' mean interval over the hold |
| --- | --- | --- | --- | --- | --- | --- | --- |
| (ii-a) `moving_20` (eps 0.45) | 0.7831 | 0.7245 | 0.7833 (1.0002 of the pin) | 0.7826 (0.9993) | 0.7915 (1.011: the count's grain, 111 over 8000) | 0.08649 | 72.58 (56.90 at rest) |
| (ii-b) `moving_28` (eps 0.22) | 0.8048 | 0.7712 | 0.8055 (1.0009) | 0.8099 (1.006) | 0.8134 (1.011) | 0.10593 | 58.92 (48.14 at rest) |

MET: the moving block's clock reads the one formula's number on its own box
to 0.02 and 0.09 percent by the spectral peak (0.07 and 0.6 percent by the
clicks' mean interval), the block form's residual of 11 and 5.5 percent
against 1 / gamma_m = 0.8165 read in full and NOT the first order (0.7245
and 0.7712 are 7.5 and 4.3 percent away). The record re-forms behind the
stepped cells by the rule, as the design's head declares (the rows stay on
their Nodes); the summed record's amplitude over the hold stays at its rest
order (10^9 to 10^10, no pumping). The pump's two signatures read 0 (no
light and no coupling declared). Wall time: 47 and 49 minutes (two worlds
and the cavity in parallel).

## (iii-b) The cavity pushed to k = 3 on 64^3, the ramp 1500 and the hold 8000: CONTROL of the medium's clock

| World | The pin (COMPUTATION) | f / f_0 by the rate over the hold [1500, 9500] against the rest cavity's (GAMEBOARD) | f / f_0 by the spectral peak | The clicks' mean interval over the hold | The steps over the hold |
| --- | --- | --- | --- | --- | --- |
| `cavity_24_moving` | 1 / gamma_m^2 = 0.6667 (section 8's cavity limit, read by the design on a deep well: `massive_block_clock_motion.out`, the regime at s = 48) | 1.171 (the rate 0.03637 against 0.03107 per interval) | 1.381 (0.2693 against 0.1950) | 27.50 (32.24 at rest) | 2912 (one Link every 2.75 intervals over the hold: the ramp's tail inside the window) |

NOT MET, and in the other direction: the moving cavity's clock runs FASTER
than at rest (1.17 by the count), not slower by 1 / gamma_m^2. The reading's
condition, named: the engine's cavity is the declaration "its own record held
at 0 outside its cells" imposed at every interval, so in motion it is a hard
mirror stepping through the medium, each hop cutting the row the cavity
leaves and exposing a fresh zero cell; its summed record grows over the hold
(the sum across the cells reaching 1.5 x 10^10 against 2 x 10^9 at rest: the
hop pumps the record between moving mirrors), the count rising with it. The
design's cavity limit was read on a deep well (the cavity regime of a well,
not a hard cavity), which the engine's (ii) worlds read instead; a moving
hard cavity is a different object from the design's, and this reading says
so. No pin is moved. The pump's two signatures read 0 (no light declared).
Wall time: 19 minutes.

## (v-m) The index in motion at K = 3 and K = 4: PREDICTION of the model as built

The design's chain of 2200 (the source at 300, the probe at 1500, s = 24, the
well `[314, 315]` on the kind `[156, 157]`, g 1 / 200 with G 1, light at omega
0.035, the block from interval 2600, the window [3400, 4300]) and its receding
case on the chain of 4000 (the source at 300, the probe at 2500, the block from
1500, the window [5000, 6000]); light's faces open on x as declared (the
reflection from x = 0 reaches the probe at about 3118 and 4850, inside the
windows). The covariant expectation (n(omega') - 1) omega' gamma_m s / c is
formed from the engine's own rest world at omega' against its reference, as
the script forms it. At rest at omega the engine reads n = 1.2358 (the delay
+0.3431 rad) against the script's 1.2362 (+0.3436); at omega' toward (K = 3)
1.2346 against 1.2345, at omega' away 1.2429 against 1.2449.

| World | The pin (COMPUTATION, the script's same-Node ratio, the drive's pair) | The ratio read (GAMEBOARD: the delay over the covariant expectation) | The delay read (rad) | The expectation (rad) | The window's two halves (rad) | The transmitted amplitude | Light's energy drift per interval over the window (of its form 9 x 10^12) | The mode k = 2 pi / 3 (mean content) |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `index_moving_k3_toward` (head-on) | 0.500 | 0.498 | 0.4023 | 0.8076 | 0.394, 0.410 (steady) | 0.955 | -1.9 x 10^8 (the largest step 1.1 x 10^11) | 1.9 x 10^11 |
| `index_moving_k3_away` (from behind, the chain of 2200) | 2.569 (the script's halves 0.227, 0.973) | 2.451 | 0.5493 | 0.2241 | 0.152, 1.015 (not steady, as the script's) | 1.378 | +3.1 x 10^8 | 1.9 x 10^11 |
| `index_moving_long_k3_away` (from behind, the chain of 4000: the Boss's pin) | 6.74 (the script's halves 1.524, 1.648) | 3.582 | 0.8515 | 0.2377 | 1.561, 0.093 (the first half at the script's; the second after the face's reflection arrives at about 4850) | 1.569 | +2.2 x 10^9 | 1.7 x 10^11 |
| `index_moving_k4_toward` | none declared | 0.510 | 0.3030 | 0.5945 | 0.302, 0.303 (steady) | 0.992 | -1.5 x 10^8 | 1.9 x 10^11 |
| `index_moving_k4_away` (the chain of 2200) | none | 1.179 | 0.2816 | 0.2389 | 0.152, 0.414 | 1.134 | +3.6 x 10^8 | 2.0 x 10^11 |
| `index_moving_long_k4_away` (the chain of 4000) | none | 3.242 | 0.8172 | 0.2520 | 0.750, 0.886 | 0.947 | +2.2 x 10^9 | 1.7 x 10^11 |

Read against the pins: HEAD-ON the engine's ratio 0.498 at K = 3 MATCHES the
script's same-Node 0.500 (the drive's pair), and reads 0.510 at K = 4: the
head-on number is the same away from the degenerate resonance (exact at K = 3),
so it is not the resonance's. FROM BEHIND on the chain of 2200 the engine reads
2.451 against the script's 2.569 (the halves as unsteady as the script's own,
the amplitude 1.38 of the reference: light gains through the receding block,
the pump's sign), and 1.179 at K = 4. On the chain of 4000 the engine reads
3.58 against the pin 6.74: the first half of the window 1.561 rad at the
script's 1.524, the second half 0.093 after the face's reflection reaches the
probe (the script's chain wraps by np.roll and its second half stays at
1.648); the pin from behind is NOT MET on the engine's chain as declared, and
the reading's condition is named: the face. At K = 4 the long chain reads
3.24 with steadier halves (0.750, 0.886). The pump's signature: light's form
drifts at 10^-5 to 10^-4 of itself per interval over the windows (negative
head-on, positive from behind), the mode's content of order 2 x 10^11 in
both directions; these are the GAMEBOARD numbers the design asked for and
carry no pin. Wall time: seconds per world (the chain of 4000, 6000
intervals: about 30 seconds).
