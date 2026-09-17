# Experiments register

This register lists the research runs of the ray-event model: section A, the
runs in which the model is confronted with a known measurement and can be
falsified; section B, the runs that demonstrate what the manuscript claims;
section C, the order in which they become possible as the features of issue
#169 land; section D, what this register replaces. It is a register, not an
essay: one entry per run, its rule stated before any code.

**What an entry is.** Every entry is a research run under
[Highlights](HIGHLIGHTS.md#55-acceptance-tests-and-open-decisions) 5.5: made
once, on a stated date, at one runtime source fingerprint (the SHA-256 of the
package files that every run records), with its expectation written before
the run and its result recorded with that fingerprint in the
[validation log](VALIDATION.md). None of these runs is a test of the test
suite, and no test of the test suite is an experiment: a test pins a contract
of the code, an experiment asks the model a question it may answer either way.
A stated acceptance requirement is not a passing test, and a passing run is
not a law of nature (Highlights 3.21, 5.5).

**Who decides.** The model owner decides which entries exist, in what order
they run, what each one pins, and what an outcome means for the model. A
specialist may propose an entry or a criterion; the register changes only by
the model owner's decision, dated.

**The rule of every entry.** Before its run, an entry names the features it
needs (numbers 1 to 11 below), the board, the families, the Detector marks
with their settings, the return mode and the phase width, what is recorded,
and its pass or fail criterion as an exact statement. Nothing is retuned
against the result and no criterion is redefined after a failure
([physics comparison method](../skills/workflow.md#physics-comparison-method)).
A failed confrontation is recorded as the model's stated limit; it does not
reopen an adopted decision and does not authorize a new law.

**Features.** The numbers are the ten features of issue #169 and the eleventh
of Highlights 3.26, in the order they land
([ray-event model](RAY_EVENT_MODEL.md#6-migration-in-order)): 1 ray state
(done on 2026-09-17, `ray-event-state-v1`); 2 the Node Detector bit (mark,
setting, ticket seed; done on 2026-09-17, `detector-mark-v1`, the
`detectors` key with `position`, `setting` `[n, d]` and `seed`); 3 the
return; 4 the inverse split with `return_mode`
(siblings, straight, annul); 5 layers; 6 the meeting of rays with N-to-M
conversion; 7 the field as the ray's own information in ray form; 8 binding
and gravity by delay; 9 every ray a wave ray with family, charge and
`phase_bits`; 10 the audits; 11 polarization (after the ten).

**Status values.** `planned` (this page, criterion fixed, not run);
`measured` with date, commit and fingerprint, and the outcome in one word
(pass, fail, or the named alternative); `withdrawn` by the model owner, dated.
Today every entry is `planned`.

**Conventions.** The board is the cubic Node lattice of Highlights 3.1 with
its boundary stated per entry; c is one Link per interval; a Detector setting
is the declared ratio n/d of its draw, the `setting` `[n, d]` of the mark
(1 = every arrival passes, 0 = every arrival returned); N is the
number of phase steps of the circle, N = 2^`phase_bits`; the steering table
is the Born rule as a coupling, cos²(δ/2) to sin²(δ/2) in bounded integer
ratios with the remainder owned (Highlights 3.3, 3.17). A statistical
criterion states its count and its standard error; an exactness criterion
states "exactly" and means integer equality at every tick.

## A. Confrontation with physics

### A1. Two-slit intensities against the Born rule

- **Confronts.** Young's two-slit fringes, intensity proportional to
  cos²(δ/2) with δ = 2π ΔL/λ for a path difference ΔL (the Born rule for two
  paths), built one quantum at a time (Tonomura and others, 1989, single
  electrons; Grangier, Roger and Aspect, 1986, single photons, fringe
  visibility 0.98).
- **Model prediction today.** Highlights 3.3: interference is steering; where
  two rays of one emitter meet in one layer the declared coupling reads their
  phase difference and splits the shared content between the two candidate
  Ports in the ratio cos²(δ/2) to sin²(δ/2); two paths of different length
  reach one place at one time only if their rays were emitted at different
  times, so δ is the emitter's rate times the path difference; light's own
  rate is zero; the Detector reads none of this and click intensity is the
  content that arrived. The fringe period is therefore λ = N/r Links for an
  emitter of rate r steps per interval.
- **Features.** 1, 2, 5, 6, 9, 10.
- **Run.** A slab of 129 × 65 × 3 Nodes, open boundary. One emitter, a bound
  clock of rate r = 32 at N = 2^8 (λ = 8 Links, so that the integer path
  differences of the screen hit the table's exact zero), a marked Node with
  setting 1, emitting one light ray per interval toward two slit Nodes 16
  Links apart;
  each slit a declared catalog coupling that re-emits the arriving light ray
  over the forward headings with its phase unchanged. A screen row 48 Links
  behind the slits: at each screen Node the meeting of the two slit rays is
  steered by the declared table between the Port toward a marked Node behind
  the screen (setting 1, its click the record) and the sideways Port (a
  declared sink). No returns in the main run; a second run with the screen
  Detectors at setting 1/2 and `return_mode` siblings (features 3 and 4) as
  the control that returns change the normalization only. Recorded: per
  screen column, the content that clicked over 2^12 intervals; the path
  difference ΔL of that column in intervals on the declared pace; the audit
  totals per tick.
- **Criterion.** Pass: for every screen column the clicked content equals the
  content that arrived times the table entry for δ = r ΔL mod N, exactly,
  with the remainder owned; the columns of the maxima and minima of the
  clicked content are those of cos²(π ΔL/λ) with λ = N/r within one Node;
  the visibility (max − min)/(max + min) is at least 1 − 4/N; the control
  run's normalized pattern equals the main run's within its binomial error
  (2^12 draws per column at 1/2, error 1/64 of the column's content). Fail:
  any column off the table, a maximum or minimum displaced by more than one
  Node, visibility below 1 − 4/N, or content in unequal to content out at
  any tick.
- **Status.** planned.

### A2. Bell test in phase form, symmetric geometry

- **Confronts.** The CHSH inequality, S ≤ 2 for every local model (Clauser,
  Horne, Shimony and Holt, 1969), and its violation with spacelike settings in
  the loophole-free experiments of 2015: Delft (Hensen and others, event-ready
  spins over 1.3 km, S = 2.42 ± 0.20), Vienna (Giustina and others) and NIST
  (Shalm and others), photons above the fair-sampling bound; the quantum
  maximum 2√2 = 2.828. In the phase form, Franson's two-photon interference
  (1989) with unbalanced interferometers, where the settings are phases and
  the quantum correlation is cos of the phase sum with visibility 1.
- **Model prediction today.** Highlights 5.4 and
  [hypothesis 11](HYPOTHESES.md#11-the-bell-prediction-of-the-ray-event-model-stated-so-that-it-can-fail),
  line 1: two Detectors at equal distance from the birth draw independently,
  the first Detector's value reaches the other only after the round trip
  through the birth event, so S ≤ 2 for symmetric spacelike settings; the
  passed pairs are a fair sample because the draw reads nothing.
- **Features.** 1, 2, 3, 4, 5, 6, 9, 10. No polarization (feature 11) is
  needed: the settings are phases.
- **Run.** A board of 161 × 17 × 17 Nodes, open boundary; the pair source at
  the center, a marked Node with setting 1, emitting one pair per 8 intervals
  as two light rays of one birth event on opposite headings ±x carrying the
  source clock's phase. Each arm at 64 Links: a splitter event with two
  outputs, a long path ΔL = 8 Links longer than the short one, a phase plate
  on the long path (a declared coupling adding the setting to the phase),
  and a recombiner meeting steered by the table between a + Port and a − Port,
  each leading to a marked Detector Node with setting 1/2, `return_mode`
  siblings. Settings at N = 2^8 from a declared per-pair list switched in the
  interval before the ray arrives: Alice 0 and 64, Bob 32 and 96 (0°, 90°,
  45°, 135°), 4096 coincident pairs per setting pair, the singlet sign
  S = |E(a,b) − E(a,b') + E(a',b) + E(a',b')|. A coincidence is a click at
  one of Alice's two Detectors and one of Bob's in the same window of 2ΔL + 1
  intervals around the pair's arrival interval; a pair with a return on
  either side is unpaired and counted. Recorded: per setting pair the four
  click counts, E, the unpaired count; per Detector its click rate; S with
  its binomial standard error σ_S (about 0.03 at 4096 pairs per correlation);
  a control with `return_mode` straight; the audits.
- **Criterion.** Pass against physics requires S > 2 + 3σ_S. The model
  predicts S ≤ 2: a value at or below 2 + 3σ_S is a fail of the model
  against the 2015 data and is recorded as the model's stated limit
  (hypothesis 11, outcome 1); a value above 2 + 3σ_S in this geometry
  contradicts hypothesis 11 line 1 and stops the register's Bell entries
  until the mechanism is understood. In either case each Detector's click
  rate must equal its setting 1/2 within 3 binomial standard errors and move
  with the other side's setting by less than 3 standard errors
  (no-signalling; a larger shift is a fail whatever S is), and every pair
  with a return must be counted unpaired, not dropped.
- **Status.** planned.

### A3. Bell test in phase form, delayed geometry

- **Confronts.** The same CHSH data as A2 and the quantum value at the
  settings of A2, 2√2; on the 256-step integer table, whose cosine of 45°
  is 181/256, the exact expectation of a mechanism obeying the singlet law
  is 724/256 = 2.828125.
- **Model prediction today.** Highlights 5.4 and hypothesis 11, line 2: the
  joint law's value appears only when the second ray's path exceeds the round
  trip through the first Detector; then the first Detector's value, carried
  through the birth event by the inverse split, meets the delayed share, and
  the declared coupling of that meeting can give the quantum value.
- **Features.** 1, 2, 3, 4, 5, 6, 9, 10, and an output-clock delay on Bob's
  line (Highlights 3.28, existing). The coupling between the transmission and
  the held ray is a declared table, written before the run, and its exact
  expectation on the 256-step circle is computed independently before the
  run.
- **Run.** The board of A2 with one change: Bob's ray is held by an
  output-clock delay k_out = 160 intervals at the Node before his analyzer,
  longer than the 128 intervals of the round trip through Alice's Detector,
  so that a value returned by Alice, which reaches that Node 128 intervals
  after Bob's ray did, finds the share still standing. Same settings, same counts, same
  window measured from Bob's release. Recorded as in A2, plus the tick at
  which each transmission meets the held share and the invariants at that
  Node.
- **Criterion.** Pass: S > 2 + 3σ_S in the delayed geometry, S within 3σ_S
  of the declared joint law's exact expectation, every Detector's click rate
  equal to its setting within 3 standard errors and moved by the other
  side's setting by less than 3 standard errors, and the energy and momentum
  at every meeting of a transmission with a held share exact. Fail: S ≤
  2 + 3σ_S in this geometry (the joint law as declared gives no violation;
  hypothesis 11 line 2 fails and a different table must be declared before
  another run), or a marginal that moves with the other side's setting
  (signalling: the table as declared is not admissible against physics), or
  an inexact meeting.
- **Status.** planned.

### A4. Single-Detector PASS statistics against the declared setting

- **Confronts.** The Born rule for one detector: at a splitter of
  transmission T a quantum clicks on one side only, never on both (Grangier,
  Roger and Aspect, 1986, anticorrelation 0.18 ± 0.06 < 1), and the click
  count over M quanta is binomial with mean T M; independent detectors give
  independent clicks.
- **Model prediction today.** Highlights 3.19 and 5.4: a marked Node draws
  1 or 0 once for each arriving transfer, independently for up to six
  arrivals in one interval, reads nothing of the ray, and the distribution is
  its declared setting, not an assumed 50/50; the click is the record of 1
  only; replay never redraws.
- **Features.** 1, 2, 3, 4, 9, 10.
- **Run.** A board of 17 × 17 × 17 Nodes, open boundary; one source (marked,
  setting 1) emitting one ray per interval toward a marked Node 8 Links away,
  `return_mode` annul so that a returned ray leaves the world into the
  accounted sink at its event Node. Settings 1/8, 1/2 and 7/8; three
  families (light, rate 0; a massive neutral family, rate 3; a massive
  charged family, rate 3, charge −1); three amounts (1, 16, 256); 2^12
  arrivals per cell. One further run with six sources around the marked Node
  at setting 1/2, one arrival per Port per interval, 2^12 intervals; and a
  replay of one run with the same seed. Recorded: arrivals, clicks and
  returns per Port and per cell; the 2^6-cell joint click table of the
  six-Port run; the annulled total per tick; the click sequence of the run
  and of its replay.
- **Criterion.** Pass, all of: clicks + returns = arrivals exactly in every
  cell; |clicks/arrivals − n/d| ≤ 3 √(n/d (1 − n/d)/arrivals) in every cell;
  the click fraction differs between families, amounts and phases at one
  setting by less than 3 standard errors; in the six-Port run the chi-square
  of the 64-cell table against the product of its six marginals is below the
  99.9 percent quantile for 57 degrees of freedom; the replay's click
  sequence equals the run's bit for bit; initial = current + escaped +
  annulled at every tick. Fail: any one.
- **Status.** planned.

### A5. Electron-electron repulsion through released fields

- **Confronts.** Coulomb's law, force k e²/r² (its inverse-square exponent
  verified to 1 part in 10^15 by Williams, Faller and Hill, 1971), and
  Rutherford's scattering law for charged rays: at speed v and impact
  parameter b a small-angle pass transfers momentum 2 k e²/(b v), inversely
  proportional to b; equal and opposite recoil; attraction for opposite
  charges.
- **Model prediction today.** Highlights 3.5: a ray's field is its own
  information spreading in ray form in all directions with the outward
  dilution; where a field ray meets a ray whose declared coupling responds
  the meeting changes that ray's trajectory, and the field ray returns
  reversed with the opposite momentum to the ray that released it, which
  recoils when the return arrives at finite speed; until its field meets
  something a traveling ray pays nothing; momentum is exact (3.14, 3.16).
  Charge is a family property read at the meeting (3.26).
- **Features.** 1, 2, 5, 6, 7, 9, 10.
- **Run.** A board of 49 × 49 × 49 Nodes, open boundary, N = 2^12. Two
  electron rays (charge −1, rate r_e, equal content) from two marked sources
  at setting 1, on antiparallel lines along x with impact parameter b = 4,
  6, 8, 12 and 16 Links, one run per b; the same with an electron and a
  positron (+1); a control with a neutral family of the same rate and
  content. The coupling "electron field ray meets a charged ray" is a
  declared integer table over the arriving field content and the charge
  product, written before the run. Recorded per tick: each matter ray's
  momentum components; every field ray in flight; the tick at which the first
  field return reaches each releaser; the transverse momentum transfer Δp(b)
  of each ray read when both are 3b past closest approach; the audits.
- **Criterion.** Pass, all of: the component-wise momentum sum over matter
  rays, field rays and returns equals the initial sum at every tick exactly;
  after all returns have arrived the two rays' Δp are equal and opposite
  exactly, and before that their difference equals the momentum carried by
  field rays in flight exactly; the first recoil of each releaser arrives at
  exactly twice the transit of the field ray to the meeting; the log-log
  least-squares exponent of |Δp(b)| over the five b is −1.0 ± 0.15 (standard
  error from the five points); like charges deflect apart and the
  electron-positron pair together; the neutral control goes straight; no
  ray meets a field ray of its own event (the audit reads the carried
  record). Fail: any one; an exponent outside the band is a fail of the
  outward dilution or of the declared table against Coulomb, stated as
  which.
- **Status.** planned.

### A6. Light bending by a bound group and G_eff N² over N = 2^8 to 2^16

- **Confronts.** The deflection of light by a mass, α = 4GM/(c² b) for
  impact parameter b (1.75 arcsec at the solar limb, Dyson, Eddington and
  Davidson, 1920; the post-Newtonian γ within 2 × 10^-4 of 1 by VLBI,
  Shapiro and others, 2004): inversely proportional to b, linear in M, and
  twice the Newtonian value for a slow body at the same b.
- **Model prediction today.** Highlights 3.28: gravity is bending by delay;
  the retained content of a Node (its mass) makes it slow, the information
  that it is heavy spreads in ray form in all directions, a met ray is
  delayed more on its nearer side and bends toward the heavy Node, and the
  field ray returns with the opposite momentum; nothing is inserted as a
  force and momentum is exact. On the ladder of
  [hypothesis 12](HYPOTHESES.md#12-one-mass-ladder-and-the-composite-spectrum-from-binding),
  m₀ = h/(N δt c²), the model owner's statement of 2026-09-17 is
  G = ħc/(N m₀)², N m₀ the Planck mass, so that the coupling measured in
  lattice units scales as 1/N²: G_eff · N² is constant across the phase
  width. This statement is not yet in Highlights or on the hypotheses page;
  the run pins it as stated.
- **Features.** 1, 2, 5, 6, 7, 8, 9, 10.
- **Run.** A board of 65 × 65 × 9 Nodes, open boundary. A bound group of
  declared families with retained content M at the center (feature 8), its
  computation field released in all directions (3.28); a light source
  (marked, setting 1) launching one light ray on a line parallel to x at
  impact parameter b = 4, 6, 8, 12 and 16, one ray per run, on both sides
  of the group; a slow massive ray (rate r, content equal to the light ray's)
  on the same lines; a control run with no group. The phase width N = 2^8,
  2^10, 2^12, 2^14 and 2^16, with the group's retained content M fixed at
  2^6 units of m₀ = 1 phase step per interval (its rate 64 steps per
  interval at every N); M doubled once at N = 2^12. The delay table of the computation
  field is a declared integer table written before the run. Recorded: the
  ray's heading and momentum components before and after the pass (the
  deflection α from the integer heading), the delay k_out incurred per Node,
  the returning field ray's momentum delivered to the group, the group's
  momentum per tick, the audits. G_eff(N) := α b /(4 M) with M in units of
  m₀ and α in radians from the heading change.
- **Criterion.** Pass, all of: momentum exact at every tick over the ray, the
  group and every field ray; the control goes straight; the ray bends toward
  the group on both sides; the log-log exponent of α over the five b is
  −1.0 ± 0.1; α at 2M is 2α at M within 1/16 relative; G_eff(N) · N² is
  constant over the five N within 1/16 relative of its value at N = 2^12.
  Reported and not pinned: the ratio of the light ray's α to the slow ray's
  α at equal b and M against the value 2 of general relativity. Fail: momentum
  inexact or a control that bends (the engine); an exponent or a linearity
  outside its band (the delay table as declared against nature); G_eff · N
  constant instead of G_eff · N², or neither (the identification of m₀ or of
  the unit of action in the derivation, not the engine), each stated as
  which.
- **Status.** planned.

### A7. Newtonian attraction between two bound groups

- **Confronts.** Newton's law, force G M₁ M₂/r², G = 6.674 30 × 10^-11
  m³ kg^-1 s^-2 (CODATA 2022), equal and opposite, with no deviation from the
  inverse square found by torsion balances down to 52 µm (Lee and others,
  2020).
- **Model prediction today.** Highlights 3.28 as in A6: the field ray of a
  heavy Node that meets a ray whose coupling responds returns reversed with
  the opposite momentum, and the heavy Node is drawn toward the ray; for two
  bound groups each is met by the other's field, so each is drawn toward the
  other, retarded by the field's transit, with the field's content falling
  by the outward dilution of the lattice, 1/r² by exact shell counts.
- **Features.** 1, 5, 6, 7, 8, 9, 10.
- **Run.** A board of 97 × 33 × 33 Nodes, open boundary, N = 2^10. Two bound
  groups of retained content M₁ and M₂ at separations r = 6, 8, 12, 16, 24
  and 32 along x, one run per r, and the same separations along the (1,1,0)
  diagonal at equal Euclidean length rounded to the lattice; M₁ doubled once
  at r = 12; 4r intervals after the first meeting. Recorded per tick: each
  group's momentum (the sum over its bound rays), every field ray in flight,
  the tick of the first return, the audits. The rate of momentum gain
  dp/dt of group 1 is read over the 2r intervals after its first return.
- **Criterion.** Pass, all of: momentum exact at every tick over both groups
  and all field rays; each group's momentum points toward the other; the
  log-log exponent of dp/dt over the six axial r is −2.0 ± 0.1; dp/dt at
  2M₁ is twice its value at M₁ within 1/16 relative; the diagonal value at
  equal Euclidean r is within 1/8 relative of the axial value (a lattice
  effect larger than that is measured and recorded under Highlights 3.23,
  not hidden). Fail: any one, stated as engine (inexact momentum), table
  (exponent) or lattice (direction).
- **Status.** planned.

### A8. Hydrogen-like binding and the Balmer ratio

- **Confronts.** The hydrogen levels E_n = −13.606 eV / n² (Balmer 1885,
  Rydberg, Bohr 1913): the ratio of the two lowest transition frequencies,
  Lyman-α (121.57 nm) to Balmer-α (656.3 nm), is (1 − 1/4)/(1/4 − 1/9) =
  27/5 = 5.4; the ionization energy of the ground state, 13.6 eV, equals its
  binding.
- **Model prediction today.** Highlights 3.4: matter is a bound group, an
  electron ray around a bound proton whose trajectory is changed at every
  step by the field rays the pair releases; the group's phase advance is its
  clock; it is unbound by an arriving ray through the declared coupling.
  Highlights 3.3: light carries the phase of the clock that emitted it, so
  the frequency of light is the rate of its emitter's clock. No level
  structure is stated anywhere: whether bound orbits exist only at discrete
  retained energies, and which clock an emitted light ray carries, the
  group's rest rate or the orbit's, is what the run decides.
- **Features.** 1, 2, 5, 6, 7, 8, 9, 10.
- **Run.** A board of 33 × 33 × 33 Nodes, open boundary, N = 2^12. A proton
  group (charge +1, retained content M_p, marked as a source with setting 1)
  at the center; an electron ray (charge −1, rate r_e) launched at distances
  d = 2 to 8 Links with transverse momentum p = 1 to 8 units, one run per
  (d, p), 2^14 intervals each, the field coupling of A5 and the binding
  coupling of feature 8 as declared tables. A second series: onto each bound
  state found, a light ray of content E from a marked source, E swept from 1
  to 64 units. Recorded: the electron ray's trajectory per tick; the group's
  retained energy per tick; every light ray leaving the group, its emission
  tick and the phase it carries (the rate read from consecutive emissions);
  the content E at which the electron ray leaves; the audits.
- **Criterion.** Pass, all of: at least two distinct bound electron
  trajectories with distinct retained energies E₁ < E₂ (< E₃) each stable
  for 2^12 intervals; with three states, (E₁ − E₂)/(E₂ − E₃) = 27/5 within
  1/8 relative; the light emitted at the two lowest transitions carries
  rates in the ratio 27/5 within 1/8 relative; the smallest content E_ion
  that unbinds the lowest state equals its binding energy E₁ within one
  unit. Reported and not pinned: the content of each emitted light ray
  against the rate it carries, for E = hf. Fail: a continuum of bound
  energies with no discrete states (the model as stated has no levels); every
  emitted ray carrying the group's rest rate (the frequency of light as the
  emitter's clock fails against the Balmer series as stated in 3.3); a ratio
  outside 27/5 ± 1/8 (the declared field table); E_ion unequal to E₁ (the
  binding accounting); each stated as which.
- **Status.** planned.

### A9. Neutron decay from the bound-group draw

- **Confronts.** The free neutron's mean lifetime 878.4 ± 0.5 s (Particle
  Data Group, 2024), half-life 878.4 ln 2 = 608.8 s, exponential survival;
  the decay n → p + e⁻ + ν̄ with electron endpoint m_n − m_p − m_e = 782 keV;
  the proton stable (lifetime above 10^34 years) and the neutron stable when
  bound in the deuteron.
- **Model prediction today.** Highlights 3.26: a free particle never decays;
  a neutron is a bound group whose ticks are events; a bound group that can
  decay is a source, and a source is a Detector, so at each tick it draws
  with its declared ratio as the setting, 1 = the conversion fires (an
  N-to-M conversion with charge, energy and momentum exact), 0 = the group
  ticks on unchanged; half-life follows, T½ = −ln 2 / ln(1 − n/d) intervals,
  and nothing else in the world draws.
- **Features.** 1, 2, 5, 6, 8, 9, 10.
- **Run.** A board of 65 × 65 × 65 Nodes, periodic, N = 2^10. 4096 neutron
  groups (the binding coupling of feature 8, catalog masses in keV: neutron
  939 565, proton 938 272, electron 511), each at its own Node 4 Links from
  any other so that products never meet, each marked with setting n/d =
  1/1024 and the conversion n → p + e⁻ + ν̄ declared as the event of a 1 with
  its invariants; 2^14 intervals. A control of 64 proton groups with setting
  0. Recorded: per group the tick of its firing or its survival; the
  products' families, charges, energies and momenta at every conversion;
  the number of draws per tick (from the ticket consumption, feature 10);
  the audits. Recorded as a finding, not pinned: the ratio n/d that the
  physical half-life needs at one Planck time per interval, about 2^-154,
  and whether the bounded setting of feature 2 can hold it.
- **Criterion.** Pass, all of: exactly one draw per neutron group per tick
  and exactly one conversion per group ever; the Kolmogorov-Smirnov distance
  between the empirical survival curve and (1 − 1/1024)^t is below 0.0255
  (the 1 percent critical value at 4096); the half-life fitted by maximum
  likelihood is 709.4 intervals within 3 standard errors (about 33
  intervals); at every conversion charge sums to zero, energy and momentum
  are exact component by component, and the electron's energy never exceeds
  782 keV; no proton group ever fires. Fail: any one; a survival curve that
  is not memoryless is a fail of the draw as the decay against nature.
- **Status.** planned.

### A10. The mass ladder against the known spectrum

- **Confronts.** The measured mass ratios m_μ/m_e = 206.768 28 (relative
  uncertainty 2 × 10^-8), m_τ/m_e = 3477.23 (7 × 10^-5) and m_p/m_e =
  1836.152 67 (2 × 10^-11), CODATA 2022.
- **Model prediction today.** Hypothesis 12, the ladder: every rest mass is
  an integer number of phase steps per interval on one circle of N steps,
  m₀ = h/(N δt c²), so every ratio is a ratio of integers; the rungs of the
  elementary families are catalog values, not predictions; the test is
  representability at one N within the declared encoding error
  ([reference units](REFERENCE_UNITS.md)).
- **Features.** 9 (and, for the real N, A11).
- **Run.** A catalog fit, no board: at N = 2^12 (the engine's circle today)
  and at the N of A11, find the smallest integer k (the electron's rung,
  r_e = k) such that k · 206.768 28, k · 3477.23 and k · 1836.152 67 are
  each within their measured relative uncertainty of an integer, and the
  largest rung k · 3477.23 is below N. Recorded: the smallest k at each N or
  its absence; whether k = 1 fits (the electron as the first rung).
- **Criterion.** Pass: a k exists at the real N. Fail: no k with the largest
  rung below N (the ladder fails at that width). Reported: at N = 2^12 no k
  fits (k = 1 puts the muon at 207, 1.1 × 10^-3 off, and k = 4 puts the tau
  above N), so the ladder is a statement about the real N only, and the
  smallest k found there is the electron's rung; k = 1 does not fit since
  206.768 28 is not an integer, so the electron is not the first rung.
- **Status.** planned.

### A11. The wide-phase run at the real N

- **Confronts.** The identification of the phase circle with nature's scale:
  with N m₀ the Planck mass and m₀ the electron's rung, N = m_P/m_e = 2.39 ×
  10^22 = 2^74.3 (the 74-bit phase; a register of 75 bits holds it, and the
  exact integer is the model owner's declaration before the run); the
  electron's Compton wavelength ħ/(m_e c) = 3.86 × 10^-13 m is then N Planck
  lengths, and the gravitational coupling of two electrons, G m_e²/(ħc) =
  (m_e/m_P)² = 1.75 × 10^-45 = 1/N², is 4.2 × 10^42 times smaller than their
  electric coupling.
- **Model prediction today.** Highlights 3.11 and 3.17: bounded integers,
  overflow rejecting before mutation; hypothesis 12 for m₀; the statement of
  A6 for G. At the real N a clock of rate 1 advances one step per interval,
  so over any board of feasible size the phase difference between two rays
  of one emitter is below 2^-50 of a turn, the steering table sends all
  shared content to the first Port, and the bending of A6 at G_eff = C/N² is
  below one heading step; the charge coupling reads charge and content, not
  the phase width, so A5 is unchanged.
- **Features.** 1, 5, 6, 7, 8, 9 with `phase_bits` = 75 and a bounded
  evaluation of the steering table at that width (no table of N entries), 10.
- **Run.** The worlds of A1, A5 and A6 repeated at `phase_bits` = 75 with the
  emitter of A1 at rate 1, the electron rays of A5 at rate k of A10, and the
  group of A6 at content 2^40 m₀; 2^12 intervals each; a replay of each with
  the same seed. Recorded: the audits per tick; the phase carried by every
  ray as a 75-bit integer; the content per Port at the screen of A1; Δp(b)
  of A5; the heading of the light ray of A6 before and after; any overflow
  rejection; the host time per tick separately (Highlights 3.10).
- **Criterion.** Pass, all of: no overflow rejection and every audit identity
  exact at every tick at 75 bits; the replay equal bit for bit; at the screen
  of A1 the phase difference of the two arriving rays equals r ΔL exactly
  and all shared content leaves by the first Port; Δp(b) of A5 equals its
  value at N = 2^12 exactly for every b; the light ray of A6 leaves with its
  heading unchanged (a deflection below the heading's resolution of one part
  in 2^30), consistent with nature's ratio 2^-142 of gravitational to
  electric coupling and not a measurement of it. Fail: an overflow or an
  inexact audit (the width,
  not physics); a fringe at the real N or a changed Δp (the phase width
  leaking into a coupling that must not read it); a deflection (G_eff · N²
  not constant to the real N).
- **Status.** planned.

### A12. Malus's law and the three-polarizer chain (after feature 11)

- **Confronts.** Malus's law (1809), transmitted intensity I₀ cos²θ through a
  polarizer at angle θ to the light's polarization; crossed polarizers pass
  nothing, and a third polarizer at 45° between them passes 1/8 of the
  unpolarized intensity (1/4 of the polarized).
- **Model prediction today.** Highlights 3.26: polarization is a family
  property, a transverse mode perpendicular to the heading with two states
  for light (the two lattice axes perpendicular to an axial heading), read by
  the declared couplings at a meeting; a polarizer is then a coupling table.
  Whether a two-state property carries the intermediate polarizer's angle
  through the chain is what the run decides; Highlights states no more.
- **Features.** 1, 2, 5, 6, 9, 10, 11.
- **Run.** A board of 65 × 9 × 9 Nodes, open boundary, N = 2^8. A source
  (marked, setting 1) of light rays polarized along y; a polarizer as a
  declared coupling of a bound group at a Node, splitting content between the
  pass Port and a declared sink by the table cos²(θ − θ_ray) for θ = 0,
  22.5, 45, 67.5 and 90 degrees, one run each, a marked Node (setting 1)
  behind it; then chains: y, 90°; y, 45°, 90°; y, 22.5°, 45°, 67.5°, 90°.
  Recorded: the content that clicks behind the last polarizer per run; the
  polarization state of every ray leaving each polarizer; the audits.
- **Criterion.** Pass, all of: one polarizer passes the table's cos²θ of the
  content exactly with the remainder owned; the chain y, 90° passes 0; the
  chain y, 45°, 90° passes 1/4 of the content within the table's rounding;
  the chain of four polarizers passes cos⁸(22.5°) = 0.531 within the
  rounding; content
  exact at every tick. Fail: the chain y, 45°, 90° passing 0 or 1/2 (the
  two-state property does not carry the intermediate angle and the catalog
  needs a transverse direction, as 3.26 allows for the circular case), or
  any inexact split.
- **Status.** planned.

### A13. Bell test with polarization settings (after feature 11)

- **Confronts.** The CHSH violation with polarizers, S = 2.697 ± 0.015
  (Aspect, Grangier and Roger, 1982, two-channel polarizers; Aspect,
  Dalibard and Roger, 1982, time-varying analyzers) and the 2015 photon
  experiments of A2, at the settings 0°, 45°, 22.5°, 67.5°, quantum value
  2√2.
- **Model prediction today.** The same as A2 and A3: S ≤ 2 in the symmetric
  geometry (hypothesis 11 line 1), the joint law's value only in the delayed
  geometry (line 2); polarization changes the settings' form, not the
  mechanism (3.26).
- **Features.** 1, 2, 3, 4, 5, 6, 9, 10, 11.
- **Run.** The board and counts of A2 with each analyzer a polarizer of A12
  at the setting, its pass Port and sink Port each leading to a marked
  Detector at setting 1/2, the pair source emitting two light rays of one
  birth event carrying the same polarization record; the settings from a
  declared per-pair list; the symmetric geometry and then the delayed
  geometry of A3.
- **Criterion.** As A2 for the symmetric geometry and A3 for the delayed one,
  with the same no-signalling and unpaired-count conditions.
- **Status.** planned.

## B. Proof for the paper

### B1. Exact conservation at every tick under every operation

- **Claim.** Highlights 3.15: "Every declared invariant is exact across an
  interaction so that the event can be rebuilt from its pieces when they
  return"; "Exact integer arithmetic is what makes the undoing exact."
- **Features.** 1, 2, 3, 4, 5, 6, 7, 8, 9, 10.
- **Run.** One world of 33 × 33 × 33 Nodes, open boundary, N = 2^8, that
  performs every operation of the engine within 2^12 intervals: a step on a
  Link, a split at an event, a meeting with N-to-M conversion, a field
  released and returned with recoil, a bound group formed and unbound, a
  Detector pass and a Detector return with its inverse split in each of the
  three modes (three runs), an escape at the open boundary. The audit sums
  energy, each momentum component, charge and family counts over resident,
  bound, in-flight, escaped and annulled content at every tick.
- **Shows.** A table of the per-tick sums, one constant line per invariant
  over the whole run, beside the count of operations of each kind per tick,
  and the residual line at zero; and, for the return, the invariants before
  the split and after the return equal, with the other shares untouched.
- **Status.** planned.

### B2. One draw only at a marked Node, and replay determinism

- **Claim.** Highlights 3.19: "For each transfer that arrives, whatever it
  is, it draws 1 or 0, the only lottery in the model"; 3.20: "Replaying one
  committed Detector decision returns the same result without another draw,
  emission or inventory charge."
- **Features.** 1, 2, 10.
- **Run.** A board of 33 × 33 × 33 Nodes, one marked Node with setting 1/2
  and 2^10 unmarked Nodes crossed by rays, 2^10 intervals; the audit counts
  tickets consumed per tick against arrivals at marked Nodes; a replay with
  the same seed; a second run with a different seed.
- **Shows.** Tickets consumed equal to arrivals at the marked Node at every
  tick and zero elsewhere; the replay's click record equal to the run's; and
  a spacetime diagram of the Nodes that differ between the two seeds, all
  inside the forward cone of the marked Node's first differing draw, one
  Link per interval.
- **Status.** planned.

### B3. The return retracing its steps, and the inverse split in three modes

- **Claim.** Highlights 3.19: "On 0 the Node returns that wave ray on the
  same line in the opposite direction, unchanged, back the same number of
  steps it has made since its event"; 3.20: "A return is the inverse split"
  and "Return modes": siblings, straight, annul.
- **Features.** 1, 2, 3, 4, 10.
- **Run.** A board of 65 × 65 × 65 Nodes; one event at the center with six
  outputs; a marked Node at distance d = 16 on the +x line with setting 0
  (every arrival returned); one run per mode. In the siblings run one sibling
  share is held by an output-clock delay on its line so that the transmission
  catches it. Recorded per tick: the returning ray's position and content;
  the transmission on the other lines; the sink total in annul mode; the
  audits.
- **Shows.** Three spacetime panels: the returned ray at position d − t
  reaching its event Node at tick 2d with steps 0 and content unchanged;
  siblings, the share and bit transmitted on the five other lines one Link
  per interval and the held share cancelled exactly where it is caught, with
  the invariants restored; straight, the ray continuing on the opposite
  line; annul, initial = current + escaped + annulled at every tick.
- **Status.** planned.

### B4. Two events at one Node in different layers

- **Claim.** Highlights 5.1: "two events can happen at the same Node in the
  same interval in layers that do not communicate, because rays whose
  families have no declared coupling never meet; they cross as if the other
  were not there."
- **Features.** 1, 5, 6, 10.
- **Run.** Four families A, B, C, D with couplings declared for {A, B} and
  {C, D} only; two rays A and B and two rays C and D arriving at one Node in
  one interval; the same two pairs run alone in two further worlds.
- **Shows.** A table of the events leaving the Node in the joint run beside
  the two solo runs, equal bit for bit, and the invariants of each layer
  summed separately and together.
- **Status.** planned.

### B5. N-to-M conversion with its invariants

- **Claim.** Highlights 3.3: "its result is at most six events, one per
  Port"; 3.26: "The weak interaction is a change of family: an N-to-M
  conversion at an event with its declared invariants (charge, energy,
  momentum)."
- **Features.** 1, 5, 6, 9, 10.
- **Run.** Five meetings on a small board in catalog keV units: 1 to 3
  (neutron to proton, electron, antineutrino), 2 to 2 (a Compton-like
  exchange), 2 to 3 (electron-positron to three light rays), 4 to 2 (a joint
  conversion), and a declared 1 to 7 that must be refused before commit.
- **Shows.** One table: inputs and outputs per meeting with energy, each
  momentum component, charge and family counts summed per column and the
  residual zero; the refusal of the seventh output with nothing mutated.
- **Status.** planned.

### B6. The field released in all directions, the recoil, and the free ray paying nothing

- **Claim.** Highlights 3.5: "The field is released in all directions";
  "the field ray itself returning reversed: the return is the opposite
  momentum of the field, carried back along the field ray's line to the ray
  that released it, which recoils when the return arrives, at finite speed";
  "Until its field meets something, a traveling ray pays nothing for it."
- **Features.** 1, 5, 6, 7, 9, 10.
- **Run.** A board of 33 × 33 × 33 Nodes; one charged ray on a straight
  line, 2^6 intervals, its field rays counted per shell per tick; a second
  world with a target ray of a responding family at distance 8.
- **Shows.** The shell of field rays at successive ticks in three orthogonal
  cross-sections with the count per shell; the releasing ray's content
  constant tick by tick in the first world; in the second, the momentum
  lines of the releaser, the target and the field in flight summing to a
  constant, the target's change at tick 8 and the releaser's recoil at tick
  16, equal and opposite.
- **Status.** planned.

### B7. A straight ray never meets its own field

- **Claim.** Highlights 3.5: "A ray traveling straight never meets its own
  field: the field is born where the ray is and leaves at the causal speed,
  ahead of the ray or away from it, and the ray is never faster than its
  field; no exclusion rule is needed."
- **Features.** 1, 7, 10, and an output-clock delay (3.28, existing).
- **Run.** One ray with output-clock delay k = 1, 2, 4 and 8 on a straight
  line for 2^10 intervals; the audit counts every meeting of a ray with a
  field ray whose carried record is the ray's own event; a parallel ray at
  distance 3 as the control that is met; a run with one mirror event after
  which the ray crosses field it released earlier.
- **Shows.** A table: self-meetings per k, zero in every row; meetings with
  the parallel ray, nonzero; after the mirror event, the crossing counted as
  an ordinary meeting.
- **Status.** planned.

### B8. Binding as a delay, and unbinding by an arriving ray

- **Claim.** Highlights 3.4: "Binding is the interaction whose result is zero
  events: the rays stay at the Node and interact again every interval"; "The
  binding may be nothing more than a very large output-clock delay"; "It is
  unbound the same way anything else happens on the board: a ray arrives."
- **Features.** 1, 5, 6, 7, 8, 9, 10.
- **Run.** Two rays of declared families meeting at a Node under the binding
  coupling, held for 2^12 intervals; then a light ray of content E arriving,
  E below and above the declared threshold.
- **Shows.** The group's residence, retained energy and phase against tick
  (zero events, the phase advancing once per interval); the arrival below
  threshold crossing or returned by the coupling with the group intact; the
  arrival above threshold producing the events that leave, with the
  invariants exact.
- **Status.** planned.

### B9. Interference as steering by the declared table

- **Claim.** Highlights 3.3: "interference is steering: where rays meet in one
  layer, the declared coupling reads their phase difference and decides
  through which Port the shared content leaves, with every invariant exact;
  nothing is erased"; the table "cos²(δ/2) to sin²(δ/2)"; "It is declared,
  not derived."
- **Features.** 1, 5, 6, 9, 10.
- **Run.** Two rays of one event meeting again at one Node with phase
  difference δ swept over all N = 2^8 steps, content 2^8 units per ray; and
  the two-slit world of A1.
- **Shows.** A table of δ against the content on the first Port, the second
  Port and the owned remainder, equal to the declared table at every δ (all
  to one Port at 0, all to the other at N/2, half at N/4); and the fringe of
  A1 as the figure, with nothing read by any Detector.
- **Status.** planned.

### B10. Charge conservation

- **Claim.** Highlights 3.15 with 3.26: charge is "a family property in the
  catalog or a coupling table, read only at a meeting"; every declared
  invariant "exact across an interaction".
- **Features.** 1, 5, 6, 9, 10.
- **Run.** A world with electron (−1), positron (+1), proton (+1) and light
  (0) rays performing every conversion of B5 and a pair creation; and one
  declared conversion that would not conserve charge.
- **Shows.** The per-tick sum of charge over resident, bound, in-flight,
  escaped and annulled rays as one constant line; the non-conserving
  conversion refused before commit with nothing mutated.
- **Status.** planned.

### B11. The wide phase breaks nothing

- **Claim.** Highlights 3.11: "Ordinary core operations and their
  intermediates use bounded integers, without floating point, roots or
  trigonometry"; 3.17: "An overflow or unsupported numerical representation
  rejects the operation before mutation."
- **Features.** 1, 6, 9 with `phase_bits` from 12 to 75, 10.
- **Run.** The worlds of B1, B3 and B9 repeated at `phase_bits` = 12, 32, 64
  and 75, with a replay at each width; the steering table evaluated by the
  bounded rule at each width and compared at the 2^12 angles of the
  12-bit table.
- **Shows.** One table: width against audit residual (zero), draws, replay
  equality, the largest difference between the wide table at the 12-bit
  angles and the 12-bit table (within the declared rounding), and the host
  time per tick reported separately as host cost, not model time.
- **Status.** planned.

### B12. Siblings of one event: the record and the bit travel one Link per interval

- **Claim.** Highlights 3.20: "Rays that left the same last event carry the
  same record of it, and nothing reads that record until a Detector; that
  shared record, and the trajectory back to the event, are all there is to
  entanglement"; 5.4: "the value was carried through the birth event in event
  spacetime, one Link per interval."
- **Features.** 1, 2, 3, 4, 10.
- **Run.** The pair board of A2 without analyzers: the source at the center,
  Alice's Detector at 32 Links with setting 0 (every arrival returned), Bob's
  at 96 Links with setting 1, `return_mode` siblings; 2^8 pairs.
- **Shows.** A spacetime diagram of one pair: Alice's return at tick 32, the
  ray at the birth Node at tick 64, the transmission on Bob's line, and Bob's
  Detector receiving the bit at tick 64 + 96 = 160, after Bob's own ray
  arrived at tick 96; the table of arrival ticks over the 2^8 pairs, all
  equal.
- **Status.** planned.

## C. Order

The features land in the order 1 to 11. Each line names what its feature
unlocks; an entry runs when the last feature it names has landed.

1. Feature 1, ray state (done on 2026-09-17): unlocks no run by itself; every
   entry needs it.
2. Feature 2, the Node Detector bit (done on 2026-09-17): B2, whose
   return-free part can run today.
3. Feature 3, the return: the retrace panel of B3.
4. Feature 4, the inverse split with `return_mode`: B3 complete, B12, A4.
5. Feature 5, layers: B4.
6. Feature 6, the meeting with N-to-M conversion: B5 (its charge column
   after 9), B9 (its table at N = 2^12 today; the sweep after 9).
7. Feature 7, the field: B6, B7.
8. Feature 8, binding and gravity by delay: B8, A7.
9. Feature 9, every ray a wave ray with charge and `phase_bits`: A1, A2, A3,
   A5, A6, A8, A9, A10, A11, B10, B11.
10. Feature 10, the audits: B1, and the exactness clauses of every entry
    above in their final form.
11. Feature 11, polarization: A12, A13.

## D. What is deleted

The historical example worlds and the study directories of the repository
(the dated research explorations of 2026-09-16, the named-particle gallery,
the family-conversion, isotropy, relativity, gravity and double-slit probes,
and the other example worlds and their runners) were removed on 2026-09-17
under the model owner's instruction that everything not used is deleted
(issue #164). Their dated results stay in the
[validation log](VALIDATION.md) with their original scope and fingerprints,
as history and not as evidence for the ray-event model. This register
replaces them: an experiment exists as an entry here, runs once at one
fingerprint under its pinned criterion, and is recorded in the validation
log; no experiment directory, harness or example world is kept in the tree.
