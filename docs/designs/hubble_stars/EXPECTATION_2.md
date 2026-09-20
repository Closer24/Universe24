# Series G2, the third run: the expectation under the reading's weight at the relative speed (`doppler-v1`), pinned before the run

The experimenter session, 2026-09-20, on `claude/series-g2-stars` with main
`56a258f` merged (PR #379, `doppler-v1`, the grain flux form; PR #377, the
signed drive). Written and committed before any world is run under the key.
The Boss's brief (the trigger of 15:31 UTC): pin the expected detector
readings of the G2 series under `doppler: true` and the signed drive, the
same twenty-four stars, from record 124's reading with the flux weight now
on the stars' pushes; state the direction each star's push changes and the
number for the fastest star; say what q the detector should read if the
deceleration is the gravity's alone, and what reading would show the weight
doing something other than the flux. Nothing here is registered; the
readings go beside this expectation when the run is done.

The numbers of this file are the generator's (`examples/events/hubble_stars/
make_worlds.py --doppler`, the reading rule `flux`), pinned in
`examples/events/hubble_stars/doppler/expectations.json` with the nine
worlds `doppler/<crowd>_<clock>.json` (the record-click worlds of the second
run with the key `doppler` added and nothing else changed; the model id
`rays-hubble-stars-record-doppler-<crowd>-<clock>-space-v1`). Rule (a) of
the suspension (record 128, PR #383) is not on main at this writing; the run
is under the law of main as merged.

## 1. What the key does to a star, in the star's integers

Every row a star reads is a mass row on the heading of its own axis (the six
chains are three lines; BEAM_LAW note 31, DESIGN.md section 2.3), so the
weight is the heading pair of note 38, one scalar per direction:

    f = (G Q - T_d s w, G Q)        G = 2^12, Q = 64, G Q = 262144,
                                    T_d = 110 (the flight table: c = Q / T_d = 32 / 55 Links per interval),
                                    w = G |p| // D the star's speed at the grain, s = +1 receding from the rows, -1 head-on.

The push of a group of rows is then the columns of step 4 on the weighted
flow, `(G Q - T_d s w) / (G Q)` of today's push: the fraction removed for a
receding reader is `T_d w / (G Q)`, the quantised v / c.

| star | r_0 | v (Links per interval) | v / c | w = floor(G v) | receding: the pair, its value | head-on: the pair, its value | exact 1 - v / c | the grain's bias |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| rank 1, the slowest (`s_px1`) | 3 | 0.03333 | 0.05729 | 136 | (247184, 262144) = 0.94293 | (277104, 262144) = 1.05707 | 0.94271 | +2.2e-4 |
| rank 4, the fastest (`s_mz4`) | 26 | 0.28889 | 0.49653 | 1183 | (132014, 262144) = 0.50359 | (392274, 262144) = 1.49641 | 0.50347 | +1.2e-4 |

So the fastest star takes 0.5036 of today's push from every row it recedes
from and 1.4964 from every row it meets head-on: the term `T_d w / (G Q)` =
130130 / 262144 = 0.4964 per unit of its speed (the Boss's "111994 /
262144-like value" is this pair at v = 1 / 3, w = 1365: (111994, 262144) =
0.4272 receding). The grain's bias, below 1 / G = 2.4e-4 in v on every star
(note 38), is toward the weight 1; it is smaller than every bracket below and
is not modelled beyond the quantisation in the derivation.

**The direction of each star's change.** On a chain, a star of rank k reads
three kinds of rows (the design's "mass inside"):

- the rows of the inner stars of its own chain and of the whole opposite
  chain travel outward, in the star's own direction of motion: the star
  recedes from them and takes them at `(c - v) / c` < 1. These are the rows
  that pull it toward the centre, so THE INWARD PULL WEAKENS by the star's
  v / c (5.7 % on rank 1, 49.7 % on rank 4);
- the rows of the outer stars of its own chain travel inward, head-on: the
  star takes them at `(c + v) / c` > 1. These push it outward, so THE
  OUTWARD PUSH STRENGTHENS by the same fraction;
- the light of the other stars passes it (`pass`) and is not a push;
  the detector is fixed and reads at the weight 1 (note 38: a fixed body
  has no speed), so THE CLICKS AND z OF EVERY STAR'S LIGHT ARE NOT
  WEIGHTED; what changes in z is the stars' motion alone.

Both changes act the same way: less deceleration than under the emitter-only
reading (the source rule of record 124, where the star's own motion did
nothing to what it read). On the innermost star of a fast line the head-on
rows of the three outer stars outweigh the receding rows of the opposite
chain and the star GAINS speed; under the source rule no star gained.

## 2. The derivation: the acoustic rule was the flux all along

The continuum derivation of DESIGN.md section 4 (`throw_derivation`) took the
rows of a star l to reach a star j at the acoustic rate
`F (c - u_r) / (c - u_s)`: the emitter's Doppler `c / (c - u_s)` times the
reader's factor `(c - u_r) / c`, which on a heading is exactly the flux
`1 - (v . c_d) / |c_d|^2` of note 38. The second run pinned the source rule
(the reader's factor dropped) because the engine of that day read that way
(RULES.md section 2, record 107). Under the key the reader's factor is
restored at the grain: the rule `flux` quantises `u_r` toward zero at 1 / G
and is otherwise the acoustic rule. Derived at t_0 = 350 (the late window
[300, 400), the registered one), F = 64 rows per direction per interval
(128 in the double crowd), the same brackets as the design's (iii):

| crowd | rule pinned for the run | q derived | q bracket | H (t_0 + T_0) derived | H bracket | \|p(end)\| / p(0) derived | its bracket | nearest form | farthest form |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| coasting | flux (no push: unchanged) | 0.000 | -0.25 .. +0.25 | 1.0000 | 0.90 .. 1.10 | 1.000 | 0.99 .. 1.01 | not pinned (the three forms within the grain) | (not pinned) |
| gravity | flux | +0.245 | +0.045 .. +0.445 | 0.9325 | 0.839 .. 1.026 | 0.673 .. 1.108 | 0.510 .. 1.162 | q = 0 or q = +0.5 | q = -0.55 |
| double | flux | +0.596 | +0.298 .. +0.894 | 0.8539 | 0.769 .. 0.939 | 0.284 .. 1.269 | 0.000 .. 1.404 | q = +0.5 or q = 0 | q = -0.55 |
| gravity, for comparison | source (the second run, record 124) | +0.859 | +0.429 .. +1.288 | 0.8268 | 0.744 .. 0.910 | 0.209 .. 1.000 | | q = +0.5 or q = 0 | q = -0.55 |
| gravity, for comparison | acoustic (the first design, DESIGN.md section 4) | +0.245 | +0.045 .. +0.445 | 0.9326 | 0.839 .. 1.026 | 0.674 .. 1.108 | 0.510 .. 1.163 | | |

The flux and the acoustic derivations differ in the fourth digit (the grain).
Also pinned, as in the second run: the reading's formula
`1 + z = (1 + k)(1 + v / c)` within 2 % and the luminosity `1 / (1 + z)`
within 5 % in every world, `k` within 0 .. 0.05, the ordering coasting <
gravity < double with gaps above 0.1, q = -0.55 not the nearest form in any
world, the longest burst of the step rule 1 Link per interval.

**Per star, the gravity crowd, the late window** (z the derived redshift at
the window's centre from the star's speed at emission; the momentum ratio
|p(end)| / p(0) on the GameBoard, a labelled control):

| star | r_0 | z under the source rule (record 124's pinned derivation) | z under the flux (pinned now) | the change in z | \|p(end)\| / p(0), source | \|p(end)\| / p(0), flux |
| --- | --- | --- | --- | --- | --- | --- |
| s_px1 | 3 | 0.0343 | 0.0440 | +0.0097 | 0.473 | 0.676 |
| s_mx1 | 4 | 0.0529 | 0.0656 | +0.0126 | 0.579 | 0.789 |
| s_py1 | 5 | 0.0813 | 0.0964 | +0.0151 | 0.761 | 0.980 |
| s_my1 | 6 | 0.1000 | 0.1172 | +0.0172 | 0.786 | 1.003 |
| s_pz1 | 7 | 0.1288 | 0.1470 | +0.0183 | 0.894 | 1.108 |
| s_mz1 | 8 | 0.1474 | 0.1671 | +0.0196 | 0.897 | 1.107 |
| s_px2 | 9 | 0.1178 | 0.1403 | +0.0225 | 0.488 | 0.673 |
| s_mx2 | 10 | 0.1385 | 0.1626 | +0.0241 | 0.533 | 0.721 |
| s_py2 | 11 | 0.1697 | 0.1933 | +0.0236 | 0.631 | 0.815 |
| s_my2 | 12 | 0.1901 | 0.2147 | +0.0246 | 0.657 | 0.842 |
| s_pz2 | 13 | 0.2222 | 0.2454 | +0.0231 | 0.738 | 0.916 |
| s_mz2 | 14 | 0.2423 | 0.2659 | +0.0235 | 0.754 | 0.930 |
| s_px3 | 15 | 0.2228 | 0.2499 | +0.0271 | 0.532 | 0.702 |
| s_mx3 | 16 | 0.2445 | 0.2721 | +0.0277 | 0.560 | 0.731 |
| s_py3 | 17 | 0.2769 | 0.3012 | +0.0243 | 0.631 | 0.795 |
| s_my3 | 18 | 0.2978 | 0.3225 | +0.0246 | 0.650 | 0.814 |
| s_pz3 | 19 | 0.3272 | 0.3489 | +0.0216 | 0.719 | 0.870 |
| s_mz3 | 20 | 0.3476 | 0.3694 | +0.0218 | 0.732 | 0.883 |
| s_px4 | 21 | 0.3396 | 0.3644 | +0.0248 | 0.582 | 0.736 |
| s_mx4 | 22 | 0.3614 | 0.3863 | +0.0249 | 0.602 | 0.756 |
| s_py4 | 23 | 0.3892 | 0.4113 | +0.0220 | 0.663 | 0.801 |
| s_my4 | 24 | 0.4104 | 0.4324 | +0.0221 | 0.677 | 0.815 |
| s_pz4 | 25 | 0.4358 | 0.4557 | +0.0199 | 0.721 | 0.849 |
| s_mz4 | 26 | 0.4565 | 0.4764 | +0.0199 | 0.731 | 0.860 |

Every star is expected to read a HIGHER z than under the source rule, by
+0.010 (rank 1 of the slow line) to +0.028 (rank 3 of the x line), and to
keep more of its momentum; the three innermost stars of the fast lines
(`s_my1`, `s_pz1`, `s_mz1`) end above their initial momentum. A measured
z per star is compared with this column at the grain of the digital step
(0.003 in z, DESIGN.md section 4); the pinned brackets are on the fits, not
on a single star.

## 3. What the detector should read if the deceleration is the gravity's alone

In the clock-free control `doppler/gravity_none`: q = +0.245 within +0.045 ..
+0.445, H (t_0 + T_0) 0.9325 within 0.839 .. 1.026, against record 124's
+0.922 and 0.811 under the source rule: the key is expected to take about
two thirds of the read deceleration away, because two thirds of what the
detector read as gravity was the emitter-only reading of a receding crowd
(the inner stars pulled back by rows they could not outrun). The reading
stays a deceleration, q > 0, the nearest form q = 0 or +0.5, the farthest
q = -0.55: the weight changes how much the model's gravity decelerates the
stars, not its sign, and nothing in it pushes two masses apart.

The clock worlds `doppler/gravity_scalar` and `doppler/gravity_age` are
pinned to the same brackets. Reported beside them, not bracketed: the second
run read the clock worlds below the control (q +0.749 scalar and +0.461 age
against +0.922, the bend of the age clock), so a like offset is expected
here, and under the key it may carry q_age below the bracket's floor; if it
does, that is the clock's, read against the control, as in the second run.
`doppler/double_none`: q = +0.596 within +0.298 .. +0.894 (the source rule
read the fit's edge, +1.5). `doppler/coasting_none`: byte-identical gather
and click lines to `record/coasting_none` (no push is read; a fixed detector
reads at the weight 1), checked to the digit.

## 4. What would show the weight doing something other than the flux

- **The weight did nothing on the pushes** if `gravity_none` reads q inside
  the source rule's bracket and outside the flux's (q > +0.445, in
  particular near +0.92 again) with the momentum ratios in 0.21 .. 1.00 and
  no star above 1: the key was not read at a `read` entry, or it weighted
  rows other than the arrivals for the push.
- **The weight removed more than the flux** if q falls below the coasting
  bracket (q < -0.25) or any star's |p(end)| / p(0) is above 1.16 in the
  gravity crowd: an overstated Doppler term (the per-axis pair's error on an
  oblique direction has no place on a heading; on a heading such a reading
  would be a wrong pair or a weight applied twice).
- **The weight touched the light** if the coasting worlds' gather or click
  lines differ from `record/coasting_none` at all, or if the reading's
  formula or the luminosity leaves its 2 % and 5 % in any world: a fixed
  detector must read at the weight 1, and a star's own motion must not
  weight its lamp's release (the emitter's side is untouched, note 38).
- **The weight is on the wrong side** if the outer stars' z rises while no
  inner star of a fast line gains momentum: the head-on rows were weighted
  down and the receding ones up (the sign of `s` reversed).

Anything else inside the brackets is read as the flux acting as derived, and
the residual deceleration as the gravity's alone, at the grain of the
digital step. What the run cannot decide is DESIGN.md section 5 unchanged:
one-dimensional beams, no luminosity distance, three lines.

## 5. The run, when main carries the key

Main carries it (`56a258f`, PR #379). The five worlds `doppler/gravity_none`,
`doppler/gravity_scalar`, `doppler/gravity_age`, `doppler/double_none` and
`doppler/coasting_none` at their registered 400 intervals with `tools/
run_series.py --jobs 3`; the readings with `tools/hubble_stars_readings.py
<root> --expectations examples/events/hubble_stars/doppler/expectations.json`,
every reading from the gather lines; the record's integers compared with
record 124's; the readings written beside this expectation in the worlds'
README under a dated heading; the page with its frame player; nothing
registered until the model owner says so.
