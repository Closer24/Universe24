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
  [DESIGN.md section 0](designs/masses/DESIGN.md); registered on the model
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
  [`examples/events/masses/`](../examples/events/masses/README.md)
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
