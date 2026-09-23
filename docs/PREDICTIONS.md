# The law's own predictions against nature

The register of what the Beam Law predicts by itself, each entry stated so
that it can fail, with the detector reading that would test it and its
status against what is observed; a disagreement is registered as the law's
limit and never tuned (the model owner, 2026-09-20: "Arrange the weak
force according to our world, and check whether we predict more things";
[record 36](LOG_2026-09-20.md#36-the-physicists-design-of-the-weak-force-and-the-list-of-the-laws-own-predictions)).

**Entries 1 to 23** are the physicist's list of 2026-09-20, written in the
weak-force session's scratchpad (`scratchpad/weak/PREDICTIONS.md`) and cited
by number in [BEAM_LAW note 36](BEAM_LAW.md#10-implementation-notes-2026-09-19-the-implementation)
(entries 7, 10, 18), [the register's series J](EXPERIMENTS.md#j-the-weak-force-2026-09-20)
(7, 8, 10, 18), [HYPOTHESES 21](HYPOTHESES.md#21-a-moving-bodys-clock-the-engines-rate-is-one-at-every-speed-natures-gamma-a-limit-stated-so-that-it-can-fail)
(12) and [the catalog's gap list](ENTITY_CATALOG.md#the-gap-list); record 36
names the five strongest (M / r on the age clock against M / r^2 on the push;
light neither bent nor delayed, superseded by the meeting; the retarded
field of a moving body; the slowed active flux of a bound body; the wave
only in the detector). They keep their numbers here and are to be brought
into this file by the physicist from that scratchpad, unchanged; until then
this file holds the entries added after them.

## 24. A lamp's line is doubled by the clock's floor, unless K divides its content

- **Statement (the mathematician, 2026-09-20, from the masses design,
  `docs/designs/masses/DESIGN.md` section 0, deleted on 2026-09-22 with its cavity worlds (record 871; in the tree's history at 59c6b811); registered on the model
  owner's word, "write the two sentences in PREDICTIONS").** A lamp of
  content M releases at every self-creation whose turn s =
  `by_clock(age, M, K)` is above 0, and every unit it releases carries the
  content h x s (E = h f, BEAM_LAW step 5). The turn takes exactly the two
  values floor(M / K) and ceil(M / K) over the ages (one value when K
  divides M), so **every quantum a lamp emits carries one of two contents,
  h floor(M / K) or h ceil(M / K), alternating in the floor's pattern, and
  one content only when K divides M**. In the detector's world a lamp's
  emission line is therefore two lines one step of h apart, occupied in the
  proportion of the fractional part of M / K, or one line at the exact
  contents M = j K; there is no line width and no third value.
- **The detector reading.** Under the record click of `amplitude-v1` the
  `content` of the gathers of a `sum` set receiving the lamp's light (one
  click per birth); without the key the `content` of the `click` records of
  a measured event that measures it. Measured on the cavity worlds of
  `examples/events/masses/` (deleted on 2026-09-22, record 871)
  (`designs/masses/cavity_click.out`, 2026-09-20): at the end of the
  unequal world the lamp of content 20806 (M / K = 5.08 at K = 4096) is read
  as 5 and 6, the lamp of content 20035 (4.89) as 4 and 5; in the equal
  world the two lamps of content 20480 = 5 K are read as 5 at every one of
  their 588 clicks each. Nothing was tuned.
- **What would refute it.** A click whose content is neither h floor(M / K)
  nor h ceil(M / K); a lamp with K dividing M read at two contents; the
  proportion of the two contents over K consecutive clicks other than the
  fractional part of M / K.
- **Against nature.** A spectral line of a transition is one energy with a
  natural width (the lifetime's) and a Doppler width, never two sharp
  values one quantum apart in a fixed proportion; the law's line is the
  clock's arithmetic, not a transition's. A plain disagreement, the law's
  limit: a lamp is a clock that pays whole steps, and nature's emitter is
  not. Status: registered, not tuned; the two-valued line is a statement
  about a lamp, since a free body (matter) emits no content at all (the
  catalog: a free ray carries no content).

## 25. A detector learns a lamp's content to the grain K per click, and exactly only from K consecutive clicks

- **Statement (the same source).** What a click carries of the emitter's
  content is its turn, s in {floor(M / K), ceil(M / K)}: one click fixes M
  to within K (the interval [s K - K + 1, s K + K - 1] when the two values
  are unknown, [floor K, floor K + K - 1] once both are seen), and the
  exact M is read only from the pattern of K consecutive clicks, whose
  contents sum to exactly M x h (the telescoping of `by_clock` over K
  ages: floor((a + K) M / K) - floor(a M / K) = M) and whose sequence is
  periodic with the period K / gcd(M, K). So **the resolution of a mass
  read through the light it emits is K content units per click, and the
  content is exact after K clicks, never sooner and never finer**: a
  detector that has read n < K clicks knows M only to within K / n or so,
  by the count of the higher value among them.
- **The detector reading.** The contents of n consecutive gathers (or
  `click` records) of one emitter at one set: the estimate of M from them
  is K x (their sum) / n, and its error against the lamp's declared
  `amount` (a GameBoard control) is bounded by K / n content units; over
  n = K clicks the sum is M exactly. In `cavity_click.out` the sum of the
  5988 clicks read at lamp B's set is 35 650 for an emitter whose content
  fell from 32 768 to 20 806 during the run; a run at constant content (the
  equal world, 588 clicks of 5) reads 588 x 5 x K / 588 = 5 K = 20480, the
  declared content, exactly, since K divides it.
- **What would refute it.** Within the law, a theorem: only a source other
  than the clock's turn for the content of a click (a `become` product's
  declared content, a re-release, a home) would break it, and those are
  not the lamp's line. Against nature: the energy of a photon from a
  given transition is measured to far better than one part in K of the
  emitter's mass from a single photon (a spectrometer reads one line's
  energy to 10^-8 from one detection); the law's K-grain per click is its
  limit, and the exact reading after K clicks has no counterpart in
  nature, where the photon's energy is not the emitter's mass over a
  clock constant at all.
- **Status.** Registered, not tuned; a limit of the law that follows from
  E = h f read off a whole-step clock, and from nothing else.

## 26. The law quantises exactly what lives on a compact group, and leaves free what lives on a scale: charge, phase and direction have numbers, mass has none

- **Statement (the mathematician, 2026-09-21, from the vector form of the
  law, [TWO_SLITS.md](designs/fraction_free/TWO_SLITS.md) and the masses
  design; registered on the model owner's word, "write the sentence in
  PREDICTIONS").** The law's own numbers are of two kinds. The widths N,
  P, Q, W, G and K are the sizes of finite samplings of compact manifolds
  (N the circle of phases, P the sphere of directions, W the wheel of
  births, Q and K the clocks), and every observable that lives on such a
  manifold is quantised by them: a phase is a whole number of steps mod
  N, a direction one of F_P, a charge a whole number of steps per Link (a
  winding number on the circle), the content of a click h times a whole
  turn (E = h f with f whole steps per interval). The amounts of the state
  vector, contents and masses, live on the non-compact scale, and every
  map of the law on the state vector (flight, fan, splitter, rotation,
  the click's norm) is linear or homogeneous in it, so **no number of the
  law selects a mass: a linear law is scale-free in its coefficients, and
  a mass ratio can arise only from a nonlinear closure on amounts, which
  the law does not have** (the model owner, record 106: the masses and
  charges are the initialisation). The division is a theorem of the
  form, not a reading: the quantised observables are the windings and
  the samplings, the free ones are the coefficients.
- **The detector reading.** Every registered quantised reading is of the
  first kind and every free one of the second: the contents of clicks in
  whole turns (`designs/masses/cavity_click.out`, entries 24 and 25),
  the charges as whole steps per Link, the directions of every fan as
  primitive vectors; against them the masses of the catalog, declared
  amounts with no ratio the law reproduces (the harmonic ladder refuted,
  the masses design section 6). A run that finds a mass selected by the
  law would refute the statement; none exists.
- **What would refute it.** Within the law: a map on the amounts that is
  not homogeneous (a binding that costs content, issue #369, if it is
  ever built, would make masses selectable, and then this entry is
  superseded by that model's identity). Against nature: a quantised
  observable of nature that lives on a scale, or a free one that lives
  on a compact group.
- **Against nature.** Nature's numbers divide the same way: charge, spin,
  angular momentum and the winding numbers are quantised; the masses,
  the mixing angles and the couplings are free parameters, in the
  standard model the eigenvalues of coupling matrices declared by hand.
  The law reproduces this division exactly and for the same reason (the
  compact groups are sampled, the scale is not), which is a structural
  agreement and not a fitted one; what it does not give, as nature's
  theories do not either, is the mass numbers themselves. Status:
  registered, not tuned.

## 27. A far lamp under the growing wall is read at 1 / (1 + z) of its rate with its birth content per click: its brightness reads q_eff = +1, its stream is stretched by 1 + z

- **Statement (the mathematician, 2026-09-21, on the model owner's order
  of record 280, [designs/far_lamp/BRIGHTNESS.md](designs/far_lamp/BRIGHTNESS.md);
  received as record 282).** Under the growing wall of
  [DERIVATIONS_BEAM.md](DERIVATIONS_BEAM.md) section 15 (`expansion-v1`, H
  declared) a lamp at rest at the distance d releases rows at its own
  rate and a detector at rest reads them `1 + z` times slower, `1 + z =
  e^(H d / c_0)`, each click carrying the content its lamp stamped at
  birth (section 6.4: no rule makes the content of a row follow its
  frequency in flight). So the brightness the detector reads is `L / (4
  pi d^2 (1 + z))` with `d = (c_0 / H) ln(1 + z)`, one factor of `1 / (1
  + z)` where the expanding form has two; the effective luminosity
  distance `(c_0 / H) ln(1 + z) sqrt(1 + z) = (c_0 / H)(z - z^3 / 24 +
  ...)` has no `z^2` term, so the Hubble diagram's second order reads
  `q_eff = +1` although the flight's `z(d)` is Milne's (`q = 0`). The
  stream's stretch is `1 + z` exactly. The surface brightness of a
  resolved source falls as `(1 + z)^-1`, the board's Nodes and the fan's
  lines being fixed under the wall.
- **The detector reading.** The pin on section 15's integers (H = 1 / 400,
  `T_D = 110`, `S_1 Q = 64`): at 100 and 300 Links `1 + z` = 1.539 and
  3.639, clicks per interval 0.650 and 0.275, the content per click
  unchanged; 400 rows released over 400 intervals arrive over 1452 at
  300 Links (`far_lamp_map.out`). The run is not made (`expansion-v1` not
  built); the reading it must give is the click count and the content
  per click of a lamp of rate 1 at those two distances.
- **What would refute it.** Within the law: a click whose content falls
  with the redshift (a rule that ties a row's content to its frequency in
  flight, which section 6.4 finds absent), or a run under `expansion-v1`
  whose click rate at 300 Links is not 0.275 of the lamp's. Against
  nature: nothing; the entry is stated so that it fails against nature,
  and it does.
- **Against nature.** The stretch: the supernova light curves and
  spectra age slower by `(1 + z)^(0.97 +- 0.10)` (Blondin et al. 2008),
  PASS. The brightness: nature's Hubble diagram reads `q_0 = -0.53 +-
  0.01` (Planck 2018), FAIL by 1.53, on the decelerating side of
  Einstein-de Sitter; against flat Lambda-CDM as the stand-in for the
  measured curve with the intercept free the shape residual is 0.339 mag
  rms (Milne 0.055), and the register's own Pantheon+ fit
  ([HYPOTHESES 7](HYPOTHESES.md#7-redshift-without-recession-and-no-dark-energy))
  found the one-factor reading behind at every exponent. The surface
  brightness: `(1 + z)^-4` (Tolman; Lubin and Sandage 2001), FAIL by
  three powers. The dark sector: no rule of the six derives or needs dark
  energy, and the far lamp says the law is short of it, not free of it;
  unseen content is admitted as an input family and not derived
  ([designs/far_lamp/DARK_SECTOR.md](designs/far_lamp/DARK_SECTOR.md),
  record 283). Status: registered as the law's limit, [NATURE.md](NATURE.md)
  rows 11a to 11c; not tuned.
