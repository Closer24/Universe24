# The far lamp through a detector: the brightness of a standard lamp under the growing wall, against the Hubble diagram

The model owner, 2026-09-21 (translated): "what stands against the
measurement, after a detector?", asked of the comparison "`q = 0` reached
for the form and nature's `-0.53` not" in
[DERIVATIONS_BEAM.md](../../DERIVATIONS_BEAM.md) section 16. The answer of
this note: that comparison was formula against formula (`q` is a number
fitted to a model, not a reading); what nature reads after its detector is
the brightness of standard lamps against the redshift z, and this note
derives what the law's detector reads of a standard lamp under the growing
wall of section 15, on the owner's word ("go for it"). Written by the
mathematician, read-only; nothing here is a rule, nothing is copied from
the owning sections, every number is made by the host script
[far_lamp_map.py](far_lamp_map.py) with its output
[far_lamp_map.out](far_lamp_map.out); no run (`expansion-v1` is not built).
Notation per record 184: a scalar plain, every symbol named at its first
use; rows and bodies, not light and matter.

**The verdict in one line.** After a detector the gap does not close, it
widens: the law's lamp is brighter than nature's at the same z by one whole
factor of `1 + z`, so its brightness reads an effective deceleration number
`q_eff = +1` against the measured `-0.55`, while the stretch of the lamp's
stream, `1 + z`, is the one reading the law passes exactly.

## 1. What the law's detector reads

Two numbers, both already the law's (section 6.4 and BEAM_LAW step 4):

- **The click count.** A detector at rest counts the rows that arrive, one
  click per row; a stream released at the lamp's rate arrives at the rate
  the flight delivers it.
- **The content per click.** A row carries the content its lamp stamped at
  birth, `h s` (the quantum times the lamp's turn, section 6.4), and the
  flight is a translation: section 6.4 states that "no rule makes the
  content of a row follow its frequency in flight". The click pays and
  reads that content, whatever the row's phase does on the way.

So the brightness the law reads is `(clicks per interval) x (content per
click)`, and the second factor does not depend on the distance.

## 2. The far lamp under the tick wall

The rule of section 15.2 as stated there, on its integers (`T_D = 110`,
`S_1 Q = 64`, `H = 1 / 400` per interval, the wall `2 T_D a` with `a =
H_den + H_num x tick`): a lamp at rest at the distance d (in original
Nodes) releases one row per interval, each of content 5; the detector at
rest counts.

| d, Links | `1 + z` read as the arrival spacing | `e^(H d / c_0)` (15.2) | clicks per interval | `1 / (1 + z)` | content per interval | content per click |
| --- | --- | --- | --- | --- | --- | --- |
| 50 | 1.241 | 1.240 | 0.806 | 0.807 | 4.03 | 5 |
| 100 | 1.539 | 1.537 | 0.650 | 0.651 | 3.25 | 5 |
| 200 | 2.366 | 2.362 | 0.423 | 0.423 | 2.11 | 5 |
| 300 | 3.639 | 3.629 | 0.275 | 0.276 | 1.37 | 5 |

The stream arrives `1 + z` times slower (section 15.3's redshift) and
every click carries its birth content: **one factor** `1 / (1 + z)` on the
count and the same one factor on the content. The geometric dilution is
section 3.2's: the rows leave on the fan's lines, which the growing wall
does not change (15.5), and the lines crossing a shell of radius d in
original Nodes are spread over `4 pi d^2` of it; on the periodic board the
images beyond the nearest add a tail that section 15.5 shows converging
under the wall (the flux of each image cut off at the Hubble length), small
when the board's extent is well beyond `c_0 / H`. With the lamp's distance
`d = (c_0 / H) ln(1 + z)` (the tick wall, 15.2), the flux a detector reads
of a lamp of rate R and content per row `h s` is

    F = R h s / (4 pi d^2 (1 + z)),    d = (c_0 / H) ln(1 + z),

and the law's effective luminosity distance (the d_L for which `F = L / (4
pi d_L^2)`) is

    d_L,law = (c_0 / H) ln(1 + z) sqrt(1 + z) = (c_0 / H) (z - z^3 / 24 + ...).

Nature's relativistic form has two factors, `F = L / (4 pi D_M^2 (1 +
z)^2)`: the arrival rate and the energy per quantum both fall by `1 + z`.
The law has the first and not the second, by section 6.4.

## 3. The deceleration number read from brightness

The Hubble diagram's second order, `d_L = (c / H)(z + (1 - q) z^2 / 2 +
...)`, gives an effective `q` for each form (the script reads it by finite
differences at small z):

| The form | `d_L` in units of `c / H` | `q_eff` | `d_L` at z = 0.5 | at z = 1.0 |
| --- | --- | --- | --- | --- |
| the law, one factor (the rule as stated) | `ln(1 + z) sqrt(1 + z)` | **+1.00** | 0.497 | 0.980 |
| the hypothetical second factor (not in the six) | `(1 + z) ln(1 + z)` | 0.00 | 0.608 | 1.386 |
| Milne (empty, coasting) | `z + z^2 / 2` | 0.00 | 0.625 | 1.500 |
| flat Lambda-CDM, `Omega_m = 0.3` (the measured curve's stand-in) | `(1 + z) int dz / E(z)` | -0.55 | 0.662 | 1.543 |
| Einstein-de Sitter (matter only) | `2 (1 + z)(1 - 1 / sqrt(1 + z))` | +0.50 | 0.551 | 1.172 |

The law's `z^2` term is zero: the flight's `z(d)` is Milne's (`q = 0`,
section 15.4), and the missing energy factor alone turns the brightness
reading into `q_eff = +1`, on the decelerating side of Einstein-de Sitter.
The second row is the one rule that would move it: a content that followed
the frequency in flight would give `d_L = (c_0 / H)(1 + z) ln(1 + z)`, the
flat coasting form known in the literature as `R_h = c t` (Melia), with
`q_eff = 0`; section 6.4 finds no such rule among the six, so it is a
hypothesis under an identity of its own, not the law, and even it does not
reach the measured `-0.55`.

## 4. Against the Hubble diagram

The supernova fits leave the intercept free (the lamp's absolute content
and H are one number), so only the shape counts. The script fits the
intercept of each form to flat Lambda-CDM at `Omega_m = 0.3`, the stand-in
for the measured curve, on z from 0.01 to 1.50 (the compilations' range),
and reads the residuals (positive: the form's lamp fainter than the
stand-in at that z):

| The form | rms, mag | worst, mag | at z = 0.1 | at z = 0.5 | at z = 1.0 | at z = 1.5 |
| --- | --- | --- | --- | --- | --- | --- |
| the law, one factor | 0.339 | +0.745 | +0.604 | +0.139 | -0.223 | -0.464 |
| the hypothetical second factor | 0.063 | +0.180 | +0.132 | +0.004 | -0.046 | -0.045 |
| Milne | 0.055 | +0.128 | +0.012 | -0.061 | +0.001 | +0.128 |
| Einstein-de Sitter | 0.194 | +0.455 | +0.361 | +0.067 | -0.132 | -0.243 |

And the one reading that needs no fit, the ratio of two fluxes (the lamp at
z = 0.5 against the lamp at z = 0.05): the law 4.985 mag, the hypothetical
second factor 5.373, Milne 5.431, the stand-in 5.527, Einstein-de Sitter
5.183.

The compilations pin the shape to a few hundredths of a magnitude per bin
over this range (Pantheon+, 1701 lamps) and exclude Milne, whose residual
here is 0.055 mag rms; the law's form lies six times farther from the
stand-in, on the same side at high z (too bright), and past Einstein-de
Sitter. **The stand-in is a model, not the data**: the number that closes
this row is the residual of `ln(1 + z) sqrt(1 + z)` against the Pantheon+
distance moduli themselves, a host computation on the published table,
which this note leaves to the next step; no plausible reading of those data
moves a 0.34 mag rms shape residual inside their errors. The register
already holds one such computation on an earlier form of the same idea:
[HYPOTHESES.md](../../HYPOTHESES.md) entry 7 (the closed row under a
growing load, before `beam-v1`) fitted the Pantheon+ sample (1,580
Hubble-flow lamps, full covariance, one free offset) and found the coasting
form disfavoured by `delta chi^2 = 106` against flat Lambda-CDM and "the
reading in which only the arrival rate is redshifted" (this note's one
factor) "behind at every exponent": the same verdict, on the data.

## 5. Two more readings after a detector

- **The stretch of a lamp's stream** (the light curve): 400 rows released
  over 400 intervals arrive over 1452 intervals at 300 Links, the factor
  3.639 = `1 + z` exactly (15.2's table). Nature: the supernova light
  curves and spectra age slower by `(1 + z)^(0.97 +- 0.10)` (Blondin and
  others, 2008). **The law passes this reading exactly.**
- **The surface brightness of a resolved source** (the flux over the
  angular area): the board's Nodes are fixed and the fan's lines are fixed
  (15.5), so a ruler of l Nodes at the distance d subtends `l / d` with
  the angular-diameter distance `d = (c_0 / H) ln(1 + z)` itself, and the
  surface brightness falls as `(1 + z)^-1`; the relativistic form gives
  `(1 + z)^-4` (Tolman), measured between 2.3 and 3.1 in the bands before
  any correction and consistent with 4 once the sources' own brightening
  with look-back time is removed (Lubin and Sandage, 2001). At z = 1 the
  law's ruler looks 0.56 times as large as the stand-in's (angular-diameter
  distances 0.693 against 0.386 in units of `c / H`) and its surface
  brightness 0.500 against 0.062. **A second reading against the law**,
  three powers of `1 + z` apart.

## 6. What this changes and what waits

- **A falsifiable row, stated so that it can fail** (for the derived laws
  table of [FULL_PICTURE.md](../../FULL_PICTURE.md) and the register of
  [PREDICTIONS.md](../../PREDICTIONS.md), on the owner's and the Boss's
  word; nothing written there by this note): a lamp at rest under the
  growing wall is read at `1 / (1 + z)` of its rate with its birth content
  per click, so its brightness against z is `L / (4 pi d^2 (1 + z))` with
  `d = (c_0 / H) ln(1 + z)`, `q_eff = +1`, and the stream's stretch is `1
  + z`. Nature: `q = -0.55` in the brightness, the stretch `1 + z`. The
  first differs, the second agrees.
- **Dark energy.** The growing wall carries none and the brightness says
  the law is short of it by more than Milne is: the coasting form was
  never the measured curve, and the law's detector reads a form on the far
  side of it. The periodic universe and `expansion-v1` stay the owner's
  declared assumptions (record 234, decided yes on both); what this note
  adds is the size of the gap after a detector.
- **What would change the reading.** Only a rule that lowers the content a
  click reads with the redshift (the second factor), and it is not one of
  the six (6.4); with it the law would read `q_eff = 0`, Milne's
  neighbourhood, still not the measured curve. Nothing in the wall's rate
  H, the grain or the width S moves the shape: they set the intercept.
- **What waits.** (i) The Pantheon+ table against `ln(1 + z) sqrt(1 + z)`
  with the intercept free, a host computation on public data (the stand-in
  replaced by the data). (ii) A run once `expansion-v1` is built: a lamp of
  rate 1 and a detector at 100 and 300 Links on a periodic board with `H =
  1 / 400`, pinned by this note at `1 + z` = 1.539 and 3.639, clicks per
  interval 0.650 and 0.275, content per click unchanged.

## 7. Links

- The growing wall, its local form and Seeliger: [DERIVATIONS_BEAM.md](../../DERIVATIONS_BEAM.md) section 15; the numbers of nature: section 16; the shell dilution: section 3.2; the click's content: section 6.4.
- The full picture and the inputs table: [FULL_PICTURE.md](../../FULL_PICTURE.md).
- The law's predictions against nature: [PREDICTIONS.md](../../PREDICTIONS.md).
- The map: [far_lamp_map.py](far_lamp_map.py), [far_lamp_map.out](far_lamp_map.out); the section's own stream: [growing_wall.py](../derivations_beam/growing_wall.py).
