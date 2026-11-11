# Recurrent-burst acceptance protocol, version 1

Declared before running the candidate grid. A positive outcome requires all
four gates below; a periodic signal or growing integers alone is insufficient.
No observation below is fed to Engine.step or used to reset a run.

1. At least four **reference-board** reassembly cycles, detected from actual
   retained reference amplitudes. A compact episode has at least 3/4 of the
   total absolute reference b mass in one radius-one face ball (center plus
   six neighbors). It must disperse below 1/2 before another compact episode
   counts. The first compact episode is preparation, not a recurrent burst.
   Message lanes are excluded from this detection. These are declared lattice
   diagnostics, not physical cosmological density or a spacetime scale factor.
2. At successive reassemblies, the vector (nonzero sign-pattern types at
   sites, nonzero sign-pattern types on face edges, persistent site-pattern
   types over three observations) must never decrease, and at least one
   component must increase at each reassembly. Persistent-pattern count must
   be nonzero. These finite-board structural proxies are not a theorem about
   algorithmic complexity, organized life, entropy or physical complexity.
3. A local feedback intervention must affect future messages. In a matched
   disconnected control, later reference reassemblies must change. Without
   both controls, repeated bursts cannot be attributed to a feedback mechanism.
   Even a passing intervention does not prove that stagnation itself is sensed.
   Stagnation-driven triggering requires an additional explicit mechanism.
4. The entire retained initial state must rewind exactly. The tensor, complete
   seed and observations are fixed before evolution. No reseeding, callbacks,
   hidden selectors, dynamic coefficient changes or truncation is permitted.

Also report carrier focus separately: six directed messages can regroup on a
periodic cube even when the reference board never contracts. Report full-state
recurrence, sign diversity saturation, maximum integer bit length, resource
stops and a scale-normalized reference fingerprint. Multiplying all amplitudes
by a common integer leaves the structural metrics unchanged.

A finite board bounds the selected structural metrics. Strict growth at every
cycle forever is impossible for these metrics. A complete-state periodic orbit
cannot have a strictly increasing single-valued state score on every return.
Unbounded integers allow nonperiodic histories, but magnitude growth alone is
not increasing structural complexity.

## Fixed search grid

Baseline: unmodified PR #29 communication model, L=3,5,7, 600 updates each.
Controls: removed seed messages; removed reception; a doubled message payload;
independent replay of the actual current tensor, not a plot or analytic surrogate.

Candidates, on L=5, 160 updates each, 128-bit counter stop checked only after a
complete step: local downstream reference feedback to each message lane,
with coefficients -3,-2,-1,1,2,3, in three families:

- `linear`: add g R(x+d) to u_message(x).
- `cubic`: add g R(x+d) message(x)^2 to u_message(x).
- `spring`: replace the reception coefficient 3 by g, and add paired spring
  terms g(message(x-d)-R(x)) and g(R(x+d)-message(x)).

The chosen coefficients are declared hypotheses. They are not derived from
Einstein equations or a physical complexity principle. Report every case and
all completed horizons, including instability and negative results. Do not
keep sampling until a favorable metric happens to appear.

## Detector calibration added after the fixed candidate grid

The first grid produced no accepted case. Add a separately labelled exact
periodic-shell control on L=7 for 70 updates. Six reference-labelled carriers
use the proven translation stencil and complete prepared histories. They
expand and reassemble, and the complete state returns every seven updates.
The detector must identify repeated reassembly, while the growth gate must
reject it. This calibrates the detector; it is not a successful research case.
A one-node reference intervention separately checks that the feedback families
really change neighboring message registers, while the baseline does not.
