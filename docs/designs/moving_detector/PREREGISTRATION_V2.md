# The moving detector's preregistration, version 2: the radar coordinate's sign (issue #937), the frozen definitions before any rerun

Issue [#937](https://github.com/Closer24/Universe24/issues/937) (the model
owner's batch #933 of 2026-09-22, 19:50Z; the protocol
`MD-RADAR-ECHO-CLOSURE` on `main` at `4376712ebbb927e36d27f8ace702c194a4a32c08`):
the design's frozen radar coordinate `x_D = c (n_r - n_e) / 2`, `t_D = (n_r +
n_e) / 2` with `q = delta n_r / delta n_e = (1 + beta) / (1 - beta)` gives
`delta x_D / delta t_D = c (q - 1) / (q + 1) = + c beta = + v`, while
[DESIGN.md](DESIGN.md) sections 2, 5 and 6, `examples/events/moving_detector/expectations.json`,
its README and the reader's prints pin `- v`. The five transponder worlds
read `+ 0.3323`, `+ 0.2008`, `+ 0.1105`, `+ 0.0584` and `+ 0.4279` against
`- 1/3`, `- 1/5`, `- 1/9`, `- 1/17` and `- 3/7`: five FAILs, which stay
recorded as such (section 4). This file is the versioned preregistration
that supersedes the sign; version 1 (DESIGN.md section 5 and 6 and the
register's `expectations.json`) is kept verbatim and marked superseded
where it stands. Docs only: no world file, no code and no run change
here; the rerun waits on the model owner's word (record 1046 of
[the log](../../LOG_2026-09-20.md): the cart set aside; the click
instrument `clock_stamp` and the radar map stand).

## 1. The decision: option 1, the coordinate kept and the prediction `+ v`

The coordinate stays `x_D = c (n_r - n_e) / 2`, and the future prediction
is `+ v`. The design as written names no orientation: `x_D` is a ray
distance (the half of the round trip's counts at c, never negative), and
the words "R receding behind it" describe the geometry, they do not sign a
coordinate; the source the design cites for the arithmetic, the click
frame's [DERIVATION.md](../click_frame/DERIVATION.md) section 2 (Bondi's
radar convention, the symmetric half of the round trip), gives a receding
reflector `+ v` on that same distance. An operational, detector-local
orientation that yields `- v` can be written (the cart's own drive heading
as the axis, R on its negative side, `x = - x_D` since the cart's pulses
leave on the heading opposite its momentum), but it is not in the design
as written and it needs a second reading of the cart (its momentum's
heading) that the ray distance does not; the ray distance is the more
primitive detector-local quantity. So version 2 is option 1 of the issue.

## 2. The frozen definitions, operational and detector-local

- **Origin.** The cart D's own Node at the birth of the pulse, on its own
  count `n_e` (the pulse's ordinal, `record` mod 2^32).
- **Orientation.** Along the ray of the pulse, the cart's lamp heading
  (`directions` [[-1, 0, 0]] in the five worlds): `x_D` grows away from the
  cart along that ray. Nothing of the GameBoard's axes enters: a cart with
  its lamp on `+x` would read the same numbers.
- **The radar pair of a return.** `x_D = c (n_r - n_e) / 2` Links (c the
  flight table's pace on a heading, 32 / 55 Links per interval, supplied),
  `t_D = (n_r + n_e) / 2` counts, both from the cart's own counts `n_e` (the
  birth ordinal the returned pulse carries) and `n_r` (the cart's count at
  the return click, `clock` under the key `clock_stamp`).
- **The radar velocity.** `delta x_D / delta t_D` over the window from the
  first return to the last, in Nodes per count: the prediction `+ v` (`+
  1/3`, `+ 1/5`, `+ 1/9`, `+ 1/17`, `+ 3/7` in the five worlds), R receding
  along the ray at the cart's pace; equivalently `c (q - 1) / (q + 1)` with
  `q` the round trip below.
- **The round trip.** `q = delta n_r / delta n_e` over the same window,
  `(1 + beta) / (1 - beta)`, unchanged from version 1 (`151/41`, `43/21`,
  `343/233`, `599/489`, `389/59`).
- **The one-way factors and the least step.** As in version 1, unchanged:
  `k_AB = 1 / (1 - beta)`, `k_BA = 1 + beta`, their ratio `1 - beta^2`, the
  least step per count, the pace over the window `v`.
- **The kinds.** The counts, Nodes and ordinals are DETECTOR; `k_AB`,
  `k_BA`, the ratio, the round trip and the radar velocity are COMPUTATION
  from DETECTOR readings (each a ratio of two differences of counts; the
  physics-rule reviewer's read Q); the tick of every line GAMEBOARD.

## 3. Supplied, not derived

`v` (the cart's pace, from its declared momentum `Q S M / (k - 1)` and the
drive's rule), `c` (the flight table's 32 / 55 on a heading), the geometry
(the bar, the post at x = 1, the lamp at x = 3, the cart from x = 20 on
`+x`), the re-release (the post's rule `rerelease`: the pulse re-emitted
on `+x` at the post's next self-creation, stamped with its number) and the
radar map (the pair `(x_D, t_D)` above) are inputs of the world and of the
reading, supplied by the world file and this file. None of them is derived
by the run; what the run reads is whether the cart's own counts, made into
the ratios above, give the predictions.

## 4. History preserved: the batch-933 readings, five FAILs against version 1

The five worlds on `main` at `4376712e` (`cart_k3`, `cart_k5`, `cart_k9`,
`cart_k17`, `cart_quantum`, 600 intervals each, completed, the return
identities complete, no engine error; the readings recomputed by the
independent reviewer from `events.jsonl` alone, no host tick), the frozen
pin of version 1 and its verdict, as issue #937 records them:

| World | observed `delta x_D / delta t_D` (COMPUTATION from DETECTOR counts) | version 1's pin | version 1's verdict |
| --- | ---: | ---: | --- |
| `cart_k3` | +0.3323177723 | -1/3 | FAIL |
| `cart_k5` | +0.2007627014 | -1/5 | FAIL |
| `cart_k9` | +0.1104718067 | -1/9 | FAIL |
| `cart_k17` | +0.0584252568 | -1/17 | FAIL |
| `cart_quantum` | +0.4278510294 | -3/7 | FAIL |

These stand as recorded. The magnitudes near the paces do not change the
verdict and are not read as a pass of anything: version 2's prediction
`+ v` is a prediction for the rerun, not a reclassification of batch 933.
The same five world files are retained unchanged as the rerun's inputs, so
that batch 933 is its regression evidence.

## 5. The round-trip closure finding, by kind

The independent review found the round trip `q` outside the band for
`cart_k3`, `cart_k5` and `cart_quantum` (the three largest `beta`) and
inside for `cart_k9` and `cart_k17`. The reviewer's read Z adds that the
`k_AB` reading also lies outside the band in three of the worlds,
`cart_k3`, `cart_k5` and `cart_quantum`. The closure numbers themselves
are not in the issue and not in the register; nothing is said of their
size here.

- **What the band is.** Version 1's tolerance, `2 / W` over a window of W
  counts apart (DESIGN.md section 5: "the hop's one-count remainder at
  each end"), applied by the reader to every ratio as written
  (`compare`, `tools/moving_detector_readings.py`: `2 / window`, the window
  the numerator's span). It is the design's band, and the reader applies
  the design's band; the finding is the design's, not the reader's.
- **Why the three fall outside.** The band was written for a ratio near 1
  whose grain is the hop's remainder. The round trip's numerator is the
  return count `n_r`, whose grain is not the hop's: each leg of the pulse
  is an integer walk of the flight table (a heading's Link arrives at the
  interval `(2 tau S_1 Q + T_D) // (2 T_D)` reaches it, so a leg of L
  Links departs from the continuous `L / c` within a range of one count),
  the post re-emits at its next self-creation (one count), and on the
  back leg the cart's hop can move the meeting Node by one Link (one
  dwell, 55 / 32 intervals). A grain of `delta` counts on `n_r` at an end
  of the window moves `q_read = delta n_r / delta n_e` by `delta / delta
  n_e = delta q / W`: the same count of grain costs `q` times more on the
  round trip than the band allows, and `q` is 3.68, 2.05 and 6.59 in the
  three worlds outside against 1.47 and 1.22 in the two inside. The sign
  of the radar velocity, `c (q - 1) / (q + 1)`, is untouched by this grain;
  its magnitude carries the same `q`-scaled grain, which is why the five
  magnitudes sit near the paces and not on them.
- **Version 2's band, one rule for every ratio, stated once (the
  physics-rule reviewer's read Z).** For every ratio R read over a window,
  `abs(R_read - R) <= 2 g / (ordinals apart)`, with g = 1 for a whole-k
  reading and g = 3 for the quantum reading, and a round trip counting +2
  counts. No ratio carries a band of its own: the one-way factors, the
  round trip and the radar velocity are all read against this rule.
  The batch-933 readings were not used to set it; whether they lie inside
  it is the rerun's to say, and a reading outside it under version 2
  refutes as section 6 of the design says (a packet not passing one Node
  per interval at the table's pace, or a re-emission not keeping the
  record).

## 6. What changes where, and when

Docs now (this file; the superseded marks in DESIGN.md section 5 and the
README's pins; the index row). On the owner's word, before the rerun, in
one build commit: the generator's `radar_velocity` pin to `+ v` and its
`reads` sentence to the ray distance, the reader's print and its band,
the tests' closed form, the README's line; the five world files unchanged.
No rerun before that word.
