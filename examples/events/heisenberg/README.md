# The Heisenberg run A10: the width of an opening and the spread behind it

Eight worlds of the Beam Law written by `make_worlds.py`, the width
w of one opening (1, 3, 9, 27 Nodes) and the detectors' `reading` (`wave`,
`beam`) the only differences between the files; the register entry is
[A10, the width of an opening and the spread behind it, under the Beam Law](../../../docs/EXPERIMENTS.md#a10-the-width-of-an-opening-and-the-spread-behind-it-under-the-beam-law-2026-09-20)
and the readings tool `tools/heisenberg_readings.py`. The model owner asked
for it on 2026-09-19 as the test of the detector's sensitivity ([Highlights
5.4](../../../docs/HIGHLIGHTS.md#54-the-detector): a detector is a set of
Nodes with one record; the declared width is the position's uncertainty).

## The world

The plane of the two-slit world stretched to 120 x 161 x 1 (z periodic),
K 2^30, N 64, no suspension, 350 intervals:

- **The lamps**: a row of w + 4 measured events of the paid family `light`
  at x = 2, centred on y = 80, content 8 K + 1 400 000 (the turn 8 per
  self-creation, so a release at tick t carries the phase 8 t mod 64 for
  the whole run; the extra step of the 1 400 000 falls beyond it), each
  releasing F = 47 units per self-creation on (1, 0, 0) alone: a plane
  wave, in phase across the row, two Nodes wider than the opening on each
  side (the wall beside the opening absorbs it).
- **The wall** at x = 8: 161 measured events of the paid family `wall`
  measuring light (the rule the keys give). **The opening**: w Nodes
  centred on y = 80 that re-emit (`rerelease`) on the fan of the 47
  primitive in-plane directions (a, b, 0) with a >= 1, |b| <= a and
  a + |b| <= 12 (the forward half of the two-slit fan, up to 45 degrees);
  a release of 47 units gives every opening Node one unit per direction
  per interval. The opening is declared as ONE detector `opening` of w
  Nodes (threshold 1): its width is the declared uncertainty of the
  position of what passes it.
- **The screen** at x = 116 (L = 108 Links behind the wall): 161 measured
  events of `wall` read as 161 one-Node detectors `screen_<y>` (the
  screen's pixels, y = 0 .. 160, the angle theta = atan((y - 80) / 108),
  sin theta within +/- 0.595). Every detector of a world declares its
  `reading`: `wave` (the coherent record: the square of the pointer over
  the set, per pixel per interval) or `beam` (the rays paired by opposite
  phase over the set, the record the count of what clicked).

The flight to the screen takes about 190 intervals (6 + 108 Links at
1 / sqrt 3); the record accumulates over the remaining 160.

## The derivation, before the runs

The wavelength of the law is `lambda = c x period`: the lamp's phase
turns 8 steps of 64 per interval, the period is 8 intervals, the speed
1 / sqrt 3, so lambda = 8 / sqrt 3 = 4.619 Links. Two rays that reach a
pixel in the same interval from emitters at the path lengths L1 and L2
were released 8 (L1 - L2) sqrt 3 / 8 ... more precisely at ticks that
differ by the difference of their integer flight times, so their phases
differ by 8 x (that difference) mod 64: the two-slit fringes of
`test_nature_beam_worlds` (a) at this lambda.

**The coherent record of w emitters one Link apart** (the `wave` reading):
at the angle theta the w rays that reach one pixel in one interval carry
the phases 2 pi j sin theta / lambda (j = 0 .. w - 1) up to the common
one, so the record is the array factor `[sin(pi w s / lambda) / (w sin(pi
s / lambda))]^2` with s = sin theta, times the fan's own profile. For
w < lambda the factor has no zero within |s| <= 1: the record is the fan
(the declared directions), narrowed a little; for w >= lambda it is a
beam whose full width at half maximum in sin theta is `0.886 lambda / w`
(the width of sinc^2; solved exactly per w below), so that

    w x FWHM(sin theta) >= 0.886 lambda = 4.09 Links

for w >= lambda: the product of the opening's width and the spread of the
transverse momentum per unit of label (sin theta = p_y / |p| for a ray on
the direction (a, b, 0)) is bounded below by a constant of the law, the
wavelength that the lamp's clock rate (E = h f) and the flight speed set.
Below lambda the product is w x the declared fan's width and the law
bounds nothing (a Node emits within its table).

| w | regime (lambda = 4.62) | expected FWHM of the record in sin theta | expected w x FWHM |
| --- | --- | --- | --- |
| 1 | a fan: one emitter, no interference | the fan's (beyond the screen's +/- 0.595) | the fan's |
| 3 | below lambda: the fan barely narrowed | 1.434 (beyond the screen) | 4.30 |
| 9 | above lambda: a beam | 0.457 | 4.11 |
| 27 | a beam | 0.152 | 4.09 |

Named before the runs as what can break the reading: (i) the far-field
condition L >> w^2 / lambda (the Fresnel number w^2 / (lambda L): 0.002,
0.02, 0.16 and 1.46 for the four widths; w = 27 at L = 108 is at the
border of the far field); (ii) the fan is discrete: each emitter's 47
directions light about 47 of the 161 pixels, so a pixel one Node wide
receives, per interval, rays from about 0.3 w of the w emitters and not
from all of them, and the coherent sum the array factor assumes is formed
only where several emitters' lines converge; (iii) the phases are
quantized to multiples of 8 steps (45 degrees) by the integer flight
times. The `count` (the plain clicks per pixel) is the control: it is the
fan's profile at every w and never narrows.

**The `beam` reading** has no derived expectation for the spread: two
coherent beams meeting at a beam detector click n1 + n2 at phase
difference 0 and |n1 - n2| at N / 2 (the pairing cancels what is
opposite); what the screen reads under it is registered as measured.

## The readings (2026-09-20, measured against expected)

Source fingerprint `f3fb33607190c86c...` (the worktree of
`claude/universe24-new-3ytqde` after the detector-set commit), Python
3.14, headless, four cores; every run completed with the books balanced
at every tick (2.1 to 52.7 s). The tool's FWHM is taken on the record
smoothed by a moving mean over five pixels, the half maximum found by
linear interpolation on each side of the peak; the rms is the weighted
root mean square of sin theta over the screen.

| World | reading | w | record FWHM in sin theta (expected) | count FWHM (the fan, the control) | record rms | count rms | w x record FWHM (expected) | clicks on the screen | cancelled by the pairing | escaped |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `w1_wave` | wave | 1 | 0.057 (the fan) | 0.057 | 0.319 | 0.319 | 0.06 (the fan) | 5497 | - | 976 |
| `w3_wave` | wave | 3 | 0.049 (1.434) | 0.063 | 0.290 | 0.324 | 0.15 (4.30) | 16703 | - | 2722 |
| `w9_wave` | wave | 9 | 0.072 (0.457) | 0.168 | 0.222 | 0.324 | 0.64 (4.11) | 50099 | - | 8216 |
| `w27_wave` | wave | 27 | 0.185 (0.152) | 0.761 | 0.224 | 0.325 | 4.99 (4.09) | 150187 | - | 25666 |
| `w1_beam` | beam | 1 | 0.057 | 0.057 | 0.319 | 0.319 | 0.06 | 5497 | 0 | 976 |
| `w3_beam` | beam | 3 | 0.063 | 0.063 | 0.324 | 0.324 | 0.19 | 16703 | 0 | 2722 |
| `w9_beam` | beam | 9 | 0.148 | 0.148 | 0.324 | 0.324 | 1.34 | 46999 | 3100 | 11146 |
| `w27_beam` | beam | 27 | 0.486 | 0.486 | 0.330 | 0.330 | 13.11 | 98780 | 51407 | 74183 |

What the runs read, line by line:

- **The count never narrows** (measured = expected): the count-weighted
  rms of sin theta is 0.32 at every width under both readings, the fan's
  own spread (the screen spans +/- 0.595; a flat fan over it would give
  0.34); the count's FWHM grows with w as the geometric shadow of the
  opening (one to 27 pixels wide at the screen's centre, where the
  emitters' (1, 0, 0) lines land).
- **The record narrows under `wave`** and not under `beam`: the
  record-weighted rms falls from 0.319 (w = 1, equal to the count's:
  one emitter, no interference) through 0.290 (w = 3) to 0.222 (w = 9)
  and 0.224 (w = 27), while under `beam` it stays the count's (0.32 to
  0.33). At w = 27 the record's central peak (5.05 x 10^11 at y = 80,
  half of it at y = 80 +/- 3) sits on a floor of single-emitter spikes
  (1.7 to 2.3 x 10^11) that a pixel reached by one emitter records
  incoherently; the rms is dominated by that floor and by the screen's
  edges, which is why it does not fall further from w = 9 to w = 27.
- **The FWHM as the tool reads it** meets the expectation only at
  w = 27: 0.185 measured against 0.152 expected (+22 %; the Fresnel
  number 1.46 there widens the lobe), the product 4.99 against 4.09.
  At w = 3 and w = 9 the measured widths (0.049, 0.072) are the width
  of the central spike of one to three converging lines and not the
  lobe (1.43, 0.46): with the discrete fan a pixel beside the peak is
  reached by fewer emitters and the smoothed record falls under half the
  peak within a pixel or two (finding (ii) above, measured). The
  products 0.15 and 0.64 are therefore below the law's constant, not
  because the law is broken but because the reading of the lobe fails
  on a sparse fan: the interference of the w emitters' rays is formed
  only where their lines converge on one pixel in one interval.
- **Under `beam`** the pairing cancels nothing at w = 1 and 3 (no two
  opposite rays meet a pixel in one interval), 3100 of 50099 clicks at
  w = 9 (6 %) and 51407 of 150187 at w = 27 (34 %), the cancelled rays
  going on to the faces (the escapes 74183 against 25666); the surviving
  count keeps the fan's spread (rms 0.33): no narrowing with w, the
  product growing as w itself. The triangle the model owner expects
  between the two extremes is not resolved by this screen (one to
  four rays per pixel per interval).
- **Fingerprints**: `initialization_sha256` `307ccd7a3242...` (`w1_wave`),
  `6e9a551d2a12...` (`w27_wave`), `2fd0a3bab10d...` (`w27_beam`);
  `tools/heisenberg_readings.py`: 16 record checks passed, 0 failed.

**Verdict.** The `wave` record narrows with the width of the opening and
the count does not, as the Beam Law says (the interference is a
reading of the crowd and lives nowhere else); the product w x FWHM
reaches the law's constant 0.886 lambda within 22 % at the one width
where the discrete fan lets the lobe form (w = 27); at the smaller widths
the sparse fan (47 directions over 161 pixels) leaves each pixel with one
to three emitters per interval and the lobe is not formed, so the bound
is not read there. Nothing was tuned. What a cleaner reading needs, for
the model owner: a fan dense enough that every emitter reaches every
pixel in the lobe (about L directions per radian, some 200 within the
lobe at L = 108, or pixels declared as detectors of several Nodes, the
set reading a wider position), and a screen far enough for w = 27
(L > 160). The `beam` reading gives no bound: its record is the fan's
count less the pairings.

Run the worlds:

```bash
python examples/events/heisenberg/make_worlds.py
PYTHONPATH=src python tools/run_series.py --jobs 4 --out artifacts/heisenberg examples/events/heisenberg/*.json
PYTHONPATH=src python tools/heisenberg_readings.py artifacts/heisenberg --profiles
```
