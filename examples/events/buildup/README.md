# A10 at a low rate: the single-click build-up, under the Beam Law

Three worlds written by `make_worlds.py`, the registered A10 world at
w = 27 under the `wave` reading ([heisenberg/](../heisenberg/README.md),
`w27_wave`; the same generator, called here) run at three source rates;
the register entry is
[A10 at a low rate, the single-click build-up (2026-09-20)](../../../docs/EXPERIMENTS.md#a10-at-a-low-rate-the-single-click-build-up-2026-09-20)
and the evidence is in [validation](../../../docs/VALIDATION.md). The
model owner's go of 2026-09-20 on the law's own predictions
([Highlights 5.4](../../../docs/HIGHLIGHTS.md#54-the-detector), "go on
everything; just make sure again that it is good and generic"), on the
physicist's list, entry 5: "The wave is only in the detector: a screen
that counts single clicks shows no fringes. The rule: the plain count of
a detector's set is additive over the arrivals; the fringe is the square
of the coherent pointer over the rays the set clicks in one interval
(`wave`), so a cross term exists only when two rays of one number reach
the set in the same interval; a single ray never interferes with itself.
Disagrees, plainly: the law predicts that fringes appear only in the
squared record and only at a rate high enough for coincidences within one
interval; nature's fringes are in the counts at any rate (Merli 1976,
Tonomura 1989, Grangier 1986). The test is the contrast against the
rate." And the owner's decision on issue #359 the same day (Highlights
5.4, "step A yes, step B no"): no memory in the detector; "if A10 at a
low rate shows no build-up one click at a time, that is registered as the
law's limit (the wave in the crowd, not in the single event)". A research
run under the [experimenter skill](../../../skills/experimenter/SKILL.md),
made once, never a test; the design and the expectation below were
written before the runs; a reading outside its bracket is reported with
its numbers, never moved. Every number is a **DETECTOR reading** (the
screen's pixels are `DetectorSet`s of one Node); the picture of the
GameBoard is a GameBoard reading, allowed as a picture.

## The worlds

The registered `w27_wave` world unchanged but for three keys: the lamps'
`rate`, the world's `ticks` and the `model_id`. The plane 120 x 161 x 1
(z periodic), K 2^30, N 64, no suspension; a row of 31 lamps of the paid
family `light` at x = 2 (the turn 8 per self-creation, the wavelength
lambda = c x period = 8 / sqrt 3 = 4.62 Links) each releasing `rate`
units per self-creation on (1, 0, 0); the wall at x = 8 of `wall` events
measuring light, with the opening of 27 Nodes centred on y = 80 declared
as ONE detector `opening` whose Nodes re-emit what arrives on the fan of
the 47 primitive directions (a, b, 0) with a >= 1, |b| <= a, a + |b| <= 12
(`apportion_whole`: at the rate 47 one unit per direction per interval;
at the rate n < 47, n units on n consecutive directions of the fan per
interval, counted from the Node's age, so the fan cycles every 47
intervals and every direction gets the same over a cycle); the screen at
x = 116 (L = 108 Links behind the wall) of 161 `wall` events read as the
one-Node `wave` detectors `screen_<y>` (the pixels), the angle theta =
atan((y - 80) / 108).

| World | lamp `rate` | rays released per interval | rays per pixel per interval at the screen (the mean) | ticks | the window |
| --- | --- | --- | --- | --- | --- |
| `w27_rate47` | [47, 1] | 27 x 47 = 1269 | about 6 ("many") | 420 | [260, 420] |
| `w27_rate8` | [8, 1] | 27 x 8 = 216 | about 1 ("about one") | 1200 | [260, 1200] |
| `w27_rate1` | [1, 1] | 27 | about 0.14 ("well below one") | 7780 | [260, 7780] |

The window opens at tick 260, when every direction of the fan that lands
on the screen has arrived (every pixel has clicked by tick 235), and is
160 x 47 / n intervals long so that the three runs accumulate the same
number of clicks (about 172 000) at the three rates. The lamps are in
phase and in step (the same content and age), so at the rate 1 the 27
opening Nodes re-emit in the same interval on the same direction: 27
parallel rays one Node apart, landing on 27 consecutive pixels; a
coincidence at one pixel in one interval then needs two rays of
different directions released in different intervals whose flight times
differ by the same amount, which the 47-interval cycle of the fan
produces for some pairs of directions.

## The derivation and the expectation, before the runs

The record of a `wave` pixel is the square of the pointer of the rays it
clicks in one interval, summed over the intervals (BEAM_LAW section 5):
R = sum over intervals of |sum over the interval's rays of A_i e^(i
phi_i)|^2. Writing I for the sum over every click of its own |A_i|^2 (the
record every unit would leave alone in its interval, "the incoherent sum",
computed by the engine's own `coherent_pointer` on one unit at the click's
phase), the cross term R - I is the sum, over the (pixel, interval) cells
holding two or more units, of the pairs' 2 A_i A_j cos(phi_i - phi_j). So:

- at the rate 47 every cell holds several rays of several emitters and
  the cross terms form the lobe of A10 (the record's FWHM 0.185 in sin
  theta against the count's 0.76; the rms of sin theta 0.224 against
  0.325, a narrowing 1 - 0.224 / 0.325 = 0.31);
- at the rate 1 a cell holds one ray but for the rare coincidences of the
  fan's cycle, so R = I at almost every pixel: no lobe, the record's
  spread the count's, the narrowing 0, R / I = 1;
- at the rate 8 between.

**The brackets, pinned.** At the highest rate the narrowing 1 - rms_R /
rms_C at least 0.2 (A10 read 0.31). At the lowest rate the narrowing 0
within +-0.02 and R / I within +-0.02 of 1 at the record's peak pixel. The
middle rate is reported. Nature: the same lobe at every rate (Tonomura's
fringes build up one electron at a time; the contrast is independent of
the intensity), so nature's narrowing at the lowest rate is the highest
rate's, 0.3: the bracket the law's prediction and nature's disagree on.
Read beside them: the count's and the record's FWHM (as A10, the
five-pixel moving mean), w x FWHM, the number of (pixel, interval) cells
with two or more rays and their share of the cells and of the clicks.

## The readings (2026-09-20, measured against expected)

Source fingerprint
`a1b2a949ccda2194537ecae4c6ff7380642f8f7d7877c01ab0e1649ba51c5d4b` (the
worktree of `claude/universe24-new-3ytqde` at the tip `9fc895a2`, the
Beam Law `beam-v1`), Python 3.14.0rc2, numpy 2.5.3, headless, four cores,
`tools/run_series.py --jobs 3`; every run completed (55.4, 38.8, 91.8 s
for the rates 47, 8, 1) with the books balanced at every tick;
`tools/buildup_readings.py`: 0 record checks failed, 2 readings inside, 1
outside, none moved.

| World | rate | clicks in the window | rays per pixel per interval | cells with a click | cells with 2+ rays (share) | clicks in such cells (share) | record FWHM (count FWHM) | w x record FWHM | record rms (count rms) | narrowing (expected) | R / I at the record's peak (expected) | R / I at the centre pixel y = 80 (reported) | R / I least .. greatest | cross term R - I |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `w27_rate47` | 47 | 172753 | 6.665 | 25921 | 25921 (1.000) | 172753 (1.000) | 0.184 (0.904) | 4.98 | 0.236 (0.341) | 0.307 (>= 0.2: inside) | 5.498 at y = 80 | 5.498 | 0.034 .. 5.498 | +4.39 x 10^12 |
| `w27_rate8` | 8 | 171871 | 1.134 | 106737 | 46174 (0.433) | 111308 (0.648) | 0.075 (0.904) | 2.02 | 0.324 (0.341) | 0.052 (reported) | 2.862 at y = 80 | 2.862 | 0.393 .. 2.862 | +6.52 x 10^11 |
| `w27_rate1` | 1 | 171742 | 0.142 | 161182 | 10560 (0.066) | 21120 (0.123) | 0.278 (0.904) | 7.51 | 0.347 (0.341) | -0.017 (0 +- 0.02: inside) | 1.200 at y = 58 (1 +- 0.02: outside) | 0.843 | 0.429 .. 1.200 | -9.31 x 10^11 |

- **The narrowing** (the law: 0.3 at the highest rate, 0 at the lowest;
  nature: 0.3 at both): measured 0.307, 0.052, -0.017 at the rates 47, 8,
  1. Inside at both ends of the law's bracket; nature's value at the
  lowest rate is outside by 0.3. The record's rms of sin theta at the rate
  1 (0.347) is the count's (0.341): no lobe.
- **R / I at the record's peak** (the law: 1 at the lowest rate): measured
  1.200 at y = 58, outside the bracket 1 +- 0.02. The record's peak at
  the rate 1 is not the lobe's centre: at y = 80 the ratio is 0.843
  (reported), and over the screen R / I runs from 0.43 to 1.20 pixel by
  pixel. The coincidences the fan's cycle produces (6.6 % of the cells,
  12.3 % of the clicks) leave cross terms, in phase at some pixels and
  in antiphase at others by the pair's flight-time difference, whose sum
  over the screen is negative (the cross term -9.3 x 10^11 against the
  incoherent sum of 1.2 x 10^13): a fixed pattern of the synchronized
  comb, not a lobe. The bracket was set on the peak pixel, which by
  construction is the pixel of the most constructive coincidence, so it
  reads the comb's largest spike; it is registered outside as pinned.
- **The middle rate** (reported): 43 % of the cells hold two or more
  rays and the narrowing is 0.052, a sixth of the full rate's; R / I at
  the centre 2.86.
- **The count's FWHM** is 0.904 at every rate (the fan's shadow of the
  opening, the control), the record's 0.184 at the rate 47 (A10's 0.185)
  and 0.278 at the rate 1, where the smoothed record has no lobe and the
  half width is that of the comb's spikes about y = 58; w x FWHM 4.98
  (the law's 4.09 within 22 %, as A10) against 7.51.
- Host cost: 55, 39 and 92 s for 420, 1200 and 7780 intervals; the
  events record 64, 73 and 125 MB (a click line per unit).

## Verdict

Fringes do not build up one click at a time in this law: the lobe of the
27-wide opening (the narrowing 0.31 of the coherent record against the
count) exists at six rays per pixel per interval, is a sixth of itself at
about one, and is gone at 0.14 (the narrowing -0.017, the record's spread
the count's), where nature builds the same lobe click by click. The law's
own prediction held in its substance (the wave is a reading of the crowd
in one interval) and failed in one letter: at the lowest rate the record
is not the count exactly but the count plus the cross terms of the rare
coincidences of the synchronized emitters (12 % of the clicks), which
make spikes of 0.43 to 1.20 of the count and no lobe, so the pinned R / I
at the peak reads 1.20 and is registered outside. The physicist's entry 5
is registered as measured: a plain disagreement with nature (Merli,
Tonomura, Grangier), and by the owner's decision of the same day the
law's limit: the wave is in the crowd, not in the single event. Nothing
was tuned. What the law lacked: a single ray that carries something of
the wave (a spread, or a memory between intervals in the detector, both
removed or refused on purpose: the wave at the Node on 2026-09-19, the
detector's memory on 2026-09-20); nature's single particle interferes
with itself, and this law's single event does not. A follow-up that
would sharpen the reading without changing the law: the opening's Nodes
with their fans rotated against each other (each Node's `directions`
list a different rotation of the fan), which breaks the synchronized comb
and its fixed coincidences, and a fourth rate at 27 rays per 27
intervals, one ray on the whole screen per interval.

Run the worlds:

```bash
python examples/events/buildup/make_worlds.py
PYTHONPATH=src python tools/run_series.py --jobs 3 --out artifacts/buildup examples/events/buildup/w27_rate47.json examples/events/buildup/w27_rate8.json examples/events/buildup/w27_rate1.json
PYTHONPATH=src python tools/buildup_readings.py artifacts/buildup --profiles
```
