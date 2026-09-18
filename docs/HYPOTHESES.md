# Hypotheses under test

This page keeps the questions the model raises apart from the results it has
measured. Everything on it is a hypothesis: something the framework suggests,
stated so that a run can confirm or refute it, or stated as outside the model's
reach. Nothing here is a claim of the coupling summary
(`docs/QUANTUM_CLASSICAL_COUPLING.md`, deleted on 2026-09-17) or of the
[validation log](VALIDATION.md). A hypothesis moves off this page
only with a measured result and a fingerprint. The runs that confront these
hypotheses with known measurements, and the demonstrations the paper needs,
are entries of the [experiments register](EXPERIMENTS.md), each with its
features and its criterion pinned before the run.

## 1. The lottery is the only door for outside information

*Superseded on 2026-09-17: this hypothesis leans on the bond registry and the
shared quantum resource of Highlights section 3.18, deleted on that date;
under sections 3.19, 3.20 and 5.4 the only draw is the Detector's bit and a
pair's outcome travels on the returning ray. The text is kept as stated.*

[Postulate 22](../POSTULATES.md#22-historical-autonomous-sampling-candidates)
makes every uncertain outcome the value of one bounded integer. It follows,
without a further assumption, that the sequence of those integers is the only
place where information not already in the world's state can enter the world:
everything else is fixed by the rules and the initial state. The model does
not fix where the sequence comes from. A configured seed, a file, or a source
outside the world give the same physics as long as the numbers are used the
same way; how they are read is fixed, and for a bonded pair it is a reading by
both ends, the parameter dependence that
[postulate 22](../POSTULATES.md#22-historical-autonomous-sampling-candidates)
names.

What can be tested: an emitter whose pairs draw their numbers from an external
stream instead of the world's sequence. With a uniform stream the Bell value
and the even plus rates must be unchanged; with a stream biased in the coin
half the other end's plus rate must begin to depend on the first end's
setting, which is a signal faster than the causal speed; with a stream
biased in the agreement half the marginals stay even while the correlation
leaves the quantum value (the Popescu-Rohrlich box at `S = 4`), so
no-signalling bounds the coin and not the correlation; the size of the signal is a
measurement. The hypothesis is therefore sharp: outside influence enters only
through the number, and is visible exactly when it is biased. Measured: the
Bell probe (`examples/bell-chsh/`, deleted on 2026-09-17 with the bond
registry) with `--source uniform` gave
S = 2.7911 and rate shifts below 0.1, and with `--source biased` kept
S = 2.7792 while Bob's plus rate moves by 0.6866 with Alice's
setting. The derivation holds in the model; whether any real source is outside
the world in this sense stays a hypothesis.

**Measured on 2026-09-16** (commit `e5b5911`, fingerprint `4e0c9eeffd4a1ce1bb832c0687913c71a8c44dd4d79d100296c42e9238f50c36`): the
Bell and postulate 22 study (`examples/research/bell-postulate-22/`, deleted
on 2026-09-17 with the bond registry; its numbers stay in the
[validation log](VALIDATION.md))
found that replacing one pair's registry number alters no Node outside the
forward cone of the end whose answer changed (144 world pairs, 0 violations,
the front exactly on the cone edge), that the product of the two outcomes is
the same whichever end asks first (4,096 of 4,096 pairs) and depends only on
the setting present at the asking tick, that settings drawn from the world's
own generator show no dependence on the pair's number (pooled p = 0.44 over
2^20 registry pairs; the raw affine ticket state is a degenerate chooser), and
that two pairs born at one Node and tick share one bond, an implementation
limit of `origin_bond`. One rate cell at z = 3.59 and one seed at p = 0.002
are recorded as pre-fixed failures and traced to block fluctuations of
consecutive seeds. The README carries the pass/fail lines; what they decide
about this hypothesis is not decided here.

## 2. Living and inanimate as two kinds of number source

The framework can express one distinction between a living thing and an
inanimate one: where its numbers come from. An inanimate record's outcomes are
values of the world's own sequence; a living record would be one whose
numbers come from outside the world's state. This page states it as a
hypothesis because the model cannot decide it: a run can only show what such
a source would look like from inside, which is the measurement of hypothesis
1. Whether any real system is such a source is a question about nature, and
no result of this repository bears on it.

## 3. The size and shape of the universe

The lattice is finite and its boundary is configured, open or periodic. The
closed-universe probes (expansion and redshift (`examples/relativity-probes/`, deleted on 2026-09-17))
measure what a periodic lattice does to a ray that laps it: a stepwise stretch
within one lap, a delay-growth redshift, and a loss of outward momentum that
does not depend on radius when one dimension is short. The hypothesis is that
a closed lattice with one compressed dimension reproduces the transition from
Newtonian pull to a flat curve at a radius set by that dimension. What is
measured is the loss curve on small lattices; what is open is whether any
lattice size and any compression give the curve nature shows, and no size of
the universe is identified.

## 4. What the sequence is

The numbers decide every uncertain outcome and are themselves decided by
nothing in the model. A seed stands in for them. Two readings are possible
and neither is testable here: the sequence is a property of the world that
the model does not describe, or the sequence is the door of hypothesis 1 and
what stands behind it is outside physics. The framework can say only this:
whatever the sequence is, it is bounded by no-signalling, so it can choose
outcomes but cannot carry a message. The question is stated so that it is not
mistaken for a result.

## 5. The derivation program

*Superseded on 2026-09-17: the mixers, instruments and the singlet law in the
bond registry named below belong to the shared quantum resource of Highlights
section 3.18, deleted on that date, and to the bond registry that follows it;
the text is kept as stated.*

The framework is one setting in which mechanics, radiation, interference,
quantum contacts and Bell's test run on the same lattice. It is not yet one
theory: the mixers, the instruments, the phase advance per link, the `|p| / D`
rule, the cosine table and the singlet law in the bond registry are configured
data, measured to hold, not derived. The program is to replace each configured
law by a rule of the lattice and show by a run that the measured tables do not
change. Each replacement is a hypothesis with its own experiment; the
"what would make this a physics result" list of the deleted coupling summary
was its first four entries.

## 6. Dark matter is a closed dimension, not extra mass

The relativity probes (`examples/relativity-probes/`, deleted on 2026-09-17) measure the
model's own rotation-curve test: the momentum a body loses along an outward
path under one `1/r^2` coupling. In three open dimensions it is Newtonian
(escape speed as `1/sqrt(R)` within resolution); in a periodic slab whose
third dimension is short it is the same from `R = 3, 5, 9` and `15`, a flat
curve, with nothing added to the law. The hypothesis is that the flat rotation
curves of galaxies are what a `1/r^2` law looks like when its far field is
carried in one dimension fewer, so that the radius where a curve flattens
measures the size of the short closed dimension, and no unseen mass is needed.
What is measured is the loss curve on lattices up to period 9; what is
pending is the open three-dimensional control with the identical metric, and
until it lands the probe report itself calls this a candidate, not a result.
A size sweep of the slab (period 3, 9 and beyond, radii to the lattice edge)
shows how far the flat part reaches on each lattice; the radius where the
measured curve stops following the hypothesis is the size at which a larger
lattice is needed, and that number belongs in the report.
The gathered gravity probe (`examples/gathered-gravity/`, deleted on
2026-09-17 with claim-gather; its numbers stay in the
[validation log](VALIDATION.md)) closed
the other route: gathering a gravity train focused quanta, not a force law.

**Measured on 2026-09-16** (commit `e5b5911`, fingerprint `4e0c9eeffd4a1ce1bb832c0687913c71a8c44dd4d79d100296c42e9238f50c36`): the
anomalies study (`examples/research/anomalies/`, deleted on 2026-09-17)
ran the open three-dimensional control named above with the identical
metric. Pooled over 12 radii (r = 4 to 24, four directions each), the pull on
a held body falls as r^p with p = -0.97 +/- 0.10 in the closed period-3 slab,
-2.04 +/- 0.12 in the open cube, and the same -2.04 +/- 0.12 in an open slab of
depth 3; in the period-9 slab p = -1.47 +/- 0.19 inside the period (8 radii)
and -0.70 +/- 0.45 outside it (6 radii). The lattice's transition is set by a
length; whether that is what nature's rotation curves show is not decided
here.

## 7. Redshift without recession, and no dark energy

The closed-row sweep (`examples/relativity-probes/`, deleted on 2026-09-17)
measures the law: on a closed row whose computation load grows with age, and
whose rules delay rays but not local cycles, rays emitted one hop apart are
absorbed `k_o / k_e` hops apart on the eye's own clock, so
`1 + z = k_o / k_e`, the ratio of the hop time at reception to the hop time
at launch, with durations stretched by the same ratio; the stretch grows with
the distance as `1 + z = exp(alpha D)` for a load linear in age, with `alpha`
read off the hop schedule and scaling with the emission. A train of moving
bodies is not usable as light: a Node starts no new cycle until its delayed
departure has arrived, so bodies stall the clocks of the Nodes they wait at.
The hop time is a scale factor: with `D = int dt / k` these are the relations
of a Friedmann universe with `a(t) ~ k(t)`, so a static lattice with the
matching load history reproduces the Hubble diagram and the time dilation of
any expanding model, and cannot be told from it by those two tests.

That correspondence is kinematic (no dynamics is derived) and is the
hypothesis's limit. A single source emitting at a fixed interval of its own
clock gives the same law as the train (`z = 1.068` at 47 links against the
ray-by-ray `k_o / k_e` of 2.032). The luminosity distance rests on two
assumptions the closed row does not measure: a `1 / D^2` dilution and that a
quantum's energy follows its measured frequency. Against the Pantheon+
supernova sample (1,580 Hubble-flow objects, full covariance, one free
offset) the two load histories the model supplies on its own are
disfavoured: constant emission (`k ~ t`, the coasting universe, `q0 = 0`) by
`delta chi^2 = 106` against flat LambdaCDM and emission growing with age
(`k ~ t^2`, `q0 = -1/2`) by 64, both with residuals that grow with redshift;
the best power law, `k ~ t^1.4`, is still behind by `delta chi^2 = 9` with
one fitted parameter each (the families are not nested, so no significance
level follows; as an information criterion, a relative likelihood of about
0.01), and the reading in
which only the arrival rate is redshifted is behind at every exponent, its
`n -> infinity` limit included. The Tolman surface-brightness exponent is
where the lattice and expansion differ, `(1 + z)^-2` against `(1 + z)^-4`,
and the raw measured exponents (2.59 and 3.37 in R and I, Lubin and Sandage
2001, before any luminosity-evolution correction) lie above the lattice's
value. The wave's frequency follows the arrival gaps under the default
phase rule by construction, so it is not an independent measurement of the
stretch; the rule that clocks keep the bare rate under load is configured,
not derived from a clock built of the model's own parts. The model does not
remove dark energy: it relabels the acceleration as a load growing faster
than linearly, which no rule of the model yet derives. What would make it a
result: a clock built from the model's own moving parts whose rate under
load is measured; a rule that fixes the emission history, so that the
exponent is derived rather than fitted; and a surface-brightness exponent
the same rule predicts.

**Measured on 2026-09-16** (commit `e5b5911`, fingerprint `4e0c9eeffd4a1ce1bb832c0687913c71a8c44dd4d79d100296c42e9238f50c36`): the
anomalies study (`examples/research/anomalies/`, deleted on 2026-09-17) reads the
lattice's Tolman exponent as n = 2.0013 +/- 0.0008 under the per-link phase
rule (three loaded rows, stretch 1.18 to 3.68; dilution and angular size
identical with and without load), against 2.59 +/- 0.17 and 3.37 +/- 0.13 in
the raw data and 4 for expansion; finds H falling with age in both load
histories, with q = 0 for the linear load (FRW-family fit n = 1.00, interval
0.84 to 1.23) and -0.55 to -0.61 for the quadratic load read from the hop
schedule (its family fit has no degrees of freedom); and measures the first
item above with a mirror cavity in place of the bound pair: a light clock
built from the model's rays and mirrors has a period close to 6k + 4 in the
hop time k (log-log slope 0.956 +/- 0.006 over 28 periods, k = 4 to 62) and
reads z = 0.022 +/- 0.022 where the bare counter reads 0.608 +/- 0.042.
Which of the three outcomes named in section 8 this is, is left to the
owner; the README lists the pre-fixed conditions and their outcomes.

## 8. Everything that moves is a ray; records only hold

*Superseded on 2026-09-17: the bound-ray-pair candidate stated at the end of
this section is superseded by [Highlights](HIGHLIGHTS.md) 3.4, where matter is
rays bound in one Node by a declared binding coupling (issue #169, feature 8),
and the claims and bond registry that the ray-form inventory below lists among
the non-ray forms were deleted the same day (issue #164, bucket B.5). The text
is kept as stated.*

A Node starts no new cycle until its delayed departure has arrived, so a
moving record that waits under a computation load stalls the clock of every
Node it waits at (the emitters of a 24-row completed 320 to 436 cycles in 700
ticks with a train of bodies present and 700 without it), while a waiting ray
stalls no record. The hypothesis is that every moving disturbance is a ray and
records only hold, read and emit; a ray at rest would then be a particle,
which needs a binding rule the engine does not yet have (two counter-heading
rays that reflect each other, with the phase advancing per interval as the
particle's clock). What can be tested first: convert one moving-body probe
(the orbits) to rays and compare; then the bound pair's phase rate against
its speed, the model's own time dilation.

**Measured on 2026-09-16** (commit `e5b5911`, fingerprint `4e0c9eeffd4a1ce1bb832c0687913c71a8c44dd4d79d100296c42e9238f50c36`): the
ray-form study (`examples/research/ray-form/`, deleted on 2026-09-17) inventories the
engine's forms (outward and ray fields are ray-form; carrier records, local
fields, localized residue, claims, source envelopes, the quantum owner and the
bond registry are not) and finds that a bound ray pair cannot be built from
rays alone. A proxy cavity of two mirror records with one Kerengonen ray
bouncing each way stays bound for 600 ticks in all 22 mirror runs under every
load tried (k = 1 to 8 and the growing profile), with 16 (k + 2) / 3 ticks per
phase cycle without `ray_phase_per_tick` and 16.0 with it, against 2 links
per tick of separation in the no-mirror control; the isotropic delay refuses
the configuration explicitly. The first check of the third manuscript below
is therefore answered for a mirror cavity, not for a pair of rays. The
ray gallery (`examples/research/ray-gallery/`, deleted on 2026-09-17) draws one recorded
run of each of the eight ray forms (replay verified against the runner's
frames, 0 mismatches over 226 frames) with every record labelled as a record;
it is a drawing of recorded state, not evidence.

### The third manuscript: a clock built from the rules

Every review of the redshift manuscript returned to one gap: the eye is a
counter the rule keeps at the bare rate, and no clock built from the
model's own processes has been tested. The stakes are exact: a clock
running at `r(t)` cycles per tick reads `(r_o / r_e)(k_o / k_e)`, and one
that slowed as `1 / k` would cancel the stretch. The third manuscript is
that experiment, and it needs one engine change, an opt-in binding rule
for the bound ray above.

What is measured, in order, each step a result on its own:

1. **The clock's rate under load.** A bound pair at a Node whose load
   grows, its phase advancing per interval, read as ticks per cycle
   against the hop time `k`. Three outcomes: `r` constant (the redshift
   manuscript's rule is derived and the stretch stands), `r ~ 1 / k` (the
   stretch cancels and the redshift stays a demonstration), or between
   (the stretch stands with another coefficient and the law changes).
2. **An oscillating source.** The bound pair emits a ray each cycle: a
   frequency carried by a physical process, not by an emission schedule.
3. **A detector with a response.** A bound pair at the eye whose capture
   depends on the relative phase; the redshift read as a change in the
   capture rate, not as a count of ticks.
4. **The model's own time dilation.** A bound pair in motion (both rays
   sharing a velocity component): its phase rate against its speed. A
   Lorentz factor would be a derivation; anything else says what the model
   is not.

The first thing to check, before any of these, is whether the pair stays
bound at all under the one-wait-register rule and under load; that is a
day's run and decides whether there is a manuscript.

### Candidate rule `bound-ray-pair-v1` (a candidate, not implemented)

Stated on 2026-09-16 from the ray-form study, for the owner to accept, change
or retire; no engine code implements it and no run has measured it.

Statement: two counter-heading rays of equal amount arriving through opposite
Ports of one Node in one interval are retained at that Node with their
headings exchanged; the retained pair's phase advances once per interval;
nothing crosses a Link while the pair is bound; an absorber at the Node takes
the pair as it takes any ray; an unequal pair forwards as ordinary rays.

Open questions: how the rule composes with the same-heading merge and with
`ray_delay` when the two arrivals are staggered by a wait; whether the
exchanged headings keep the recoil accounting exact; how a bound pair moves
(both rays sharing a velocity component, step 4 above); and whether its phase
rate under load is the mirror cavity's `16 (k + 2) / 3`, the constant 16, or
neither, which is step 1 above measured on a pair instead of a cavity.

## 9. A candidate law, stated so that it can fail

Not yet a law: nothing here is derived from a principle, and its one
discriminating prediction is against it for now. Stated in three lines so
that the third manuscript can promote or retire it:

1. **The Hubble rate is the growth rate of the transport delay.**
   `H(t) = (1 / k) dk / dt`; for a linear load `H = lambda / (B k)`, the
   emission per Node per tick over the budget, over the hop time in force.
   A cosmological number tied to a local microscopic one.
2. **The acceleration is the exponent of the load's growth.**
   `q0 = -(n - 1) / n` for `k ~ t^n`; dark energy is `n > 1`, an emission
   growing with age. The fitted `n = 1.4` is a fit, not a derivation.
3. **Clocks are not slowed by the load; transport is.** The asymmetry on
   which the other two lines rest, a configured rule until step 1 above
   measures it.

What separates the candidate from expansion, and so lets it fail: a
Tolman exponent of 2 against 4 (the published exponents, reduced under an
expanding geometry, lie above 2); no mechanism for a background
temperature scaling as `1 + z`; and a stretch quantized in steps of
`1 / k_e` per gap, unobservable at any real scale. Line 3 is what the
third manuscript can turn into a result; line 1 then becomes a law with a
number, `H_0` from `lambda / B`.

## 10. Rest phase as the self-field

**Fails on geometry, 2026-09-17.** A ray's field is born where the ray is
and leaves at the causal speed, ahead of the ray or away from it; a ray is
never faster than its own field, so a ray traveling straight never meets it,
at any output-clock delay. There is no self-meeting from which a rest phase
could come. The hypothesis is kept on the page as a closed one; the declared
rate of [Highlights](HIGHLIGHTS.md) 3.3 stands. The text below is the
hypothesis as raised.

Under the ray-event model ([Highlights](HIGHLIGHTS.md) 3.3 and 3.5) a ray's
phase advances each step at a rate its family declares, and a ray's field is
not released ahead of it along its own line, so a ray never meets its own
field. The hypothesis is that the second rule could be relaxed for the
phase alone and the first rule then derived: a ray with mass is slower than
its field ([Highlights](HIGHLIGHTS.md) 3.28), so field released behind it on
its own line would catch it from behind, and the field's presence at the
ray's Node is an interaction that makes no event (3.5). If that meeting
advanced the ray's phase and changed nothing else (no heading, no momentum,
no energy, so no self-force and no cost to a free ray), the phase gained per
step would grow with the ray's slowness, that is with its mass: a rest
frequency derived from the strength of the field and the output-clock delay
instead of declared per family, the model's own `E = m c^2`. A ray with no
mass and no charge would gain nothing, as light should. The hypothesis is
raised by the model owner on 2026-09-17 and is not a law: 3.3 keeps the
declared rate.

What it would cost, stated so that it can fail: the field ray would have to
carry the identity of its source (the information of its last event) and
the rule would have to read it, since a field arriving from behind on the
same line may belong to another ray traveling behind; today no rule reads
that hidden variable ([Highlights](HIGHLIGHTS.md) 5.4). A neutral ray with
mass but no charge field would gain no rest phase from this mechanism alone
and would need another field to supply it. And the phase gained per
self-meeting is one more number to fix.

What can be tested, once the ray-event engine runs: one ray with an
output-clock delay and a charge field, no declared phase rate, on a straight
line on a small board; measure the phase gained per step as a function of the
delay `k_out`. Three outcomes: a fixed ratio that depends only on the delay
(the hypothesis lives and the declared rate of 3.3 becomes derivable), a
ratio that needs tuning per family (the parameter has only moved), or no
stable ratio (the hypothesis fails). The same run with a massless ray must
gain nothing.

## 11. The Bell prediction of the ray-event model, stated so that it can fail

Under the ray-event model ([Highlights](HIGHLIGHTS.md) 3.19, 3.20, 5.4) a
pair is two rays of one birth event, each carrying its share of that event;
every Detector draws 1 or 0 without reading the ray; only a pass is a
measurement; a return walks back to the birth event and transmits the share
and the bit along the partner's line at one Link per interval; no register
answers at a distance. The hypothesis raised by the model owner on
2026-09-17 is that this reproduces the correlations of entangled pairs. What
the model predicts, exactly:

1. Two Detectors at equal distance from the birth, settings chosen at the
   last moment, coincidences counted within a window: the first Detector's
   value reaches the other only after the round trip through the birth
   event, after the other has already drawn, so each measured outcome
   depends only on its own setting, the arriving ray and a local draw. Every
   such model obeys CHSH at most 2 (Bell's theorem); with a blind draw the
   passed pairs are a fair sample, so the coincidence subset obeys it too.
2. One arm delayed beyond the round trip before its Detector: the value
   arrives first, and the joint law of the declared couplings can give the
   quantum value.
3. A draw that reads the ray and the setting would bias which pairs count
   (the detection loophole); a shared draw sequence correlates the two bits
   with each other but not with the settings.

What is measured: the loophole-free experiments of 2015 (Delft, event-ready
electron spins over 1.3 km, S = 2.42; Vienna and NIST, photons with detection
efficiency above the fair-sampling bound and settings chosen at spacelike
separation) and the three-particle GHZ tests all report violations under
condition 1. The prediction of line 1 therefore contradicts existing data
unless the model's coincidence count differs from the experiments' in a way
the pair test can show. The test (issue #169, feature 4): the pair board with
the source as a marked Node, two Detectors at equal distance with settings
drawn per pair, coincidences counted within a declared window, CHSH computed
from clicks only; then the same board with one arm delayed by more than the
round trip. Three outcomes: at most 2 in the symmetric case (the model's
prediction stands and disagrees with the data; the hypothesis fails as a
model of entanglement and is kept as the model's stated limit), above 2 in
the symmetric case (the analysis above is wrong, to be understood before
anything else), or above 2 only in the delayed case (as predicted). The
only door left in the model's own terms is that the sequence feeding the
draws also feeds the settings (section 1 above); that reading explains any
correlation and is not a prediction.

Status (2026-09-17, Highlights 5.4): a Detector reads the bit since that day
(feature 2b): a ray carrying 1 passes a later Detector without a draw, a ray
carrying 0 is a transmission and is never drawn, and only a ray carrying no
bit is drawn. The premise above, every Detector drawing without reading the
ray, holds for a ray carrying no bit only, so the price of Highlights 5.4
(line 1, CHSH at most 2 in the symmetric geometry) is to be re-derived under
this rule by this hypothesis and experiment A13 before it is quoted again;
lines 1 to 3 stand as recorded until then.

Restated under the law of the bit (model owner, 2026-09-18; Highlights 5.4):
there is no draw. A mark meets a 0 or a 1, decided at the ray's birth and
along its one path; a mark that misses a thing returns it by its declared
table, one arrival in d, on its own steps to the birth event, where the
inverse split carries its value along the partner's line at one Link per
interval. Line 1 therefore reads: each outcome depends only on the local
setting and the arriving thing, the counted pairs are a fair sample because
the table reads nothing, and S ≤ 2 for spacelike settings, without
qualification: the model's declared limit, in every geometry. Line 2 is not
a prediction of the model: a value carried back can meet the partner's thing
on a longer arm, and what that meeting gives is a declared table of things
meeting (point 4), which the model does not supply; A3 tests a table if one
is declared. Line 3 is void: nothing reads the ray at a mark and nothing is
drawn, so there is no detection loophole to declare and no shared sequence.
The three outcomes above reduce to two: at most 2 in the symmetric geometry
(the model's limit, stated and kept) or above 2 there (the law is wrong
somewhere, to be understood before anything else). A2 runs after features
15 to 17.

## 12. One mass ladder, and the composite spectrum from binding

Under the ray-event model ([Highlights](HIGHLIGHTS.md) 3.3, 3.4) a rest mass
is a rest rate: a bounded integer number of phase steps per interval, zero for
light. Two hypotheses follow, raised by the model owner on 2026-09-17, each
with a test.

**The ladder.** Every rest mass is an integer multiple of one unit,
`m_0 = h / (N delta_t c^2)` with `N` the phase steps of the circle, so every
mass ratio in the world is a ratio of integers on one grid. The model does not
say which rungs are occupied: the masses of the elementary families
(electron, muon, quarks) are catalog values on that grid, not predictions.
What can be tested is representability: with the bounded integers of the
engine, the measured ratios (muon to electron 206.77, tau to electron
3477.2, proton to electron 1836.15) must all fit one grid within the encoding
error the [reference units](REFERENCE_UNITS.md) declare, at one `N`. If no
single `N` fits them within that error, the ladder fails. The external body
of Highlights 3.19 (model owner, 2026-09-17) stands outside the ladder: the
ladder comes from the spreading law, since a bound group is rays that must
keep moving and bind again every interval, so only the closed patterns the
binding table can hold exist, and a body that does not spread has no
closure condition and any amount is allowed.

**The composite spectrum.** A composite (a hadron, a nucleus, an atom) is a
bound group: rays held at one Node by a binding coupling, an interaction that
repeats every interval and releases no event (3.4). Given the elementary
families and their binding couplings as declared tables, every combination
can be run: whether it stays bound, what it retains (its mass, the retained
content plus or minus the binding), and what arriving ray unbinds it. The
list of combinations that stay bound is a prediction of the composite
spectrum, and the exact invariants of every meeting (charge, family counts,
momentum) predict which transitions are forbidden. A combination the model
holds stable that nature does not show, or a known particle the model cannot
hold, falsifies the declared couplings or the model. This test waits for
issue #169 feature 8 and for the strong binding as a declared table; its
cost is a full coupling table and long runs, and its first target is the
lightest cases (a two-nucleon bound state and its absence for two protons).

Status (2026-09-17, Highlights 3.4, binding is a periodic orbit of the
meeting rule): the ladder is the set of loop-closing contents, the contents
and phases whose meetings under the ordinary coupling table reproduce the
rays that entered them so that the pattern repeats, a pattern that does not
close dispersing; the held-ray binding of feature 8, which holds any
content, has no ladder. A10 counts the loop-closing contents once feature
14, binding as a loop, lands (after features 12, 8c, 2b and 8b), and the
composite spectrum is the list of loops the declared tables close.

## 13. Confinement from the quark's field rays binding to each other

Under the ray-event model ([Highlights](HIGHLIGHTS.md) 3.4, 3.5, 3.26) the
strong interaction is catalog work on the same engine, after feature 10 of
issue #169: quark families, colour a property with three values, the gluon
the quark's own field in ray form, the binding of three quarks a binding
coupling, and no new engine mechanism. The hypothesis raised by the model
owner on 2026-09-17, open and not measured: one more declared coupling, the
quark's field rays binding to each other, yields confinement, that is the
short range of the strong interaction and its growth with distance.
Highlights expects both from that coupling and leaves whether it holds to a
run; nothing in the engine decides it.

What the model predicts if the hypothesis holds, with the quark families, the
colour property, the three-quark binding coupling and the field-to-field
binding coupling all declared as tables and nothing else changed:

1. Short range: the field rays of a bound group of quarks bind to each other
   near the group instead of spreading in all directions, so a second group
   beyond a declared distance is crossed without a meeting, while a charge's
   field is met at every distance under the same rules.
2. Growth with distance: the content the bound field rays hold between two
   quarks grows with their separation instead of falling off as the released
   field of a charge does.
3. No free quark: pulling a quark ray away from its group costs content that
   grows with distance until a meeting produces new events, bound groups
   again, and no run ends with one quark ray alone on a straight line.

The test: the bound group under load (issue #169, feature 8, then the
composite of
[hypothesis 12](#12-one-mass-ladder-and-the-composite-spectrum-from-binding))
with the field-to-field coupling as one more declared table; measure the
content held between two quarks against their separation, the distance at
which a second group is met, and whether a quark ray is ever counted alone,
with pinned expectations written before the first run. Three outcomes: the
content grows with separation, the range is short and no lone quark appears
(the hypothesis stands as stated); the content falls off with distance as
for charge (the coupling as declared gives no confinement, and a different
table must be stated before it is run, or the question stays open); or the
group does not stay bound once the extra coupling is declared (the table is
wrong, not the engine). Status: open. This hypothesis waits for feature 8
and for the catalog entries of Highlights 3.26; it moves off this page only
with a measured result and a fingerprint.

Status (2026-09-17, Highlights 3.26 in the language of binding as a loop,
3.4): the strong field differs from light by one catalog line, its rays
couple to each other, so the field between quarks does not spread as a
sphere but closes into loops of gluon rays along the line between them, a
string whose content, and so whose mass, grows with the distance; only
colour-neutral patterns close a loop, which is confinement as a closure
condition; and a string stretched to the content at which a new loop closes
with a quark and an antiquark breaks into two hadrons, which is
hadronization. None of it is inserted: this hypothesis says whether the two
catalog lines, the gluon as the quark's field and `gluon_gluon_binding`,
produce it, in a research run after feature 14 (E7 of the register), and
lines 1 to 3 above read in that language as the closure of gluon loops.

## 14. The gravitational constant from the lattice, G = ħc/(N m₀)²

Recorded 2026-09-17 from the model owner's statement of that day; open.

**Statement.** In the ray-event model gravity is bending by delay (Highlights 3.28): the retained content of a Node makes it slow, and the information that it is heavy spreads in ray form. The unit of mass is the rest rate m₀ of the lightest massive family (one phase step per interval), and the largest rest rate the phase can represent is N steps per interval, N being the phase modulus declared by `phase_bits`. The hypothesis is that the effective gravitational coupling measured on the board scales as the inverse square of that ceiling, G_eff ∝ 1/N², so that in physical units G = ħc/(N m₀)², with N m₀ playing the role of the Planck mass. The real N is then of the order of 10²², which the 74-bit phase of the integer width convention can hold.

**Prediction.** Measure G_eff from the bending of a light ray passing an external body (Highlights 3.19, feature 7b, `external-body-v1`; named "fixed body" earlier on 2026-09-17) of declared family and amount, at rest and at its default coupling, absorption into its explicitly accounted sink, its motion caused by fields only and its velocity an exact accumulator that completes no Link at the body's amount, so that against the light ray it stands still (experiment A6 of `docs/EXPERIMENTS.md`) on one small board with N = 2⁸, 2¹⁰, 2¹², 2¹⁶ and everything else held fixed; G_eff · N² is the same number for all four, within the remainder tolerance of Highlights 3.17. If G_eff · N² drifts with N, the hypothesis fails as stated, and the drift's form says what the delay table does instead.

**What would falsify it.** A bending that does not fall as 1/N², or that depends on the board size, the impact parameter or the family in a way the delay rule does not predict; or a real-N run (experiment A11) whose G, converted with the measured m₀, is not the measured G of nature within the accuracy the board allows.

**Status.** Open. Feature 8 (`ray-binding-v1`, 2026-09-17) ran the owner's
acceptance criterion as `test_ray_binding.py` on a 21^3 board with a mass of
N / 4 phase steps per interval in place of the external body (an ordinary
bound group of the held form then; since 2026-09-17, when `loop-binding-v1`
removed the held form, resident content, a record holding stock of the
family whose field is met, with the same numbers), b = 4, the delay table `[4, 4, 4, 4, 4, 4]` per unit of the
field amount: the delay is 16 phase steps at every N, G_eff = 64 / N^2 and
G_eff x N^2 = 64 exactly for N = 2^8, 2^10, 2^12, 2^16. The constancy follows
from the delay being counted in phase steps of the field amount, which is
content and does not scale with N, while the mass does; a table acting on
the rate would give G_eff x N^2 growing with N. Experiment A6 (the five b,
the exponent, the linearity in M, feature 7b) is still to run. The formula
is a reparametrization of the input N until hypothesis 16 says what fixes
the lag modulus (Highlights 5.5, 2026-09-17): until then the model predicts
the form 1/N², not the value of G.

**Reading (2026-09-17, Highlights 3.28).** N is the lag modulus: the finest
lag a field can impress on the ray it meets, one part in N of a phase step,
carried in the ray's lag register with its own declared modulus (feature 8b
of `docs/RAY_EVENT_MODEL.md`, after feature 10), and not the phase circle,
which stays as small as the family's couplings need. The formula
G = ħc/(N m₀)² is unchanged, and so is the measurement above, whose delay is
counted in content and not in the rate; until feature 8b the code counts the
lag in phase steps, so those runs set the two moduli equal, and after it the
four N are declared on the lag alone. The reading of N as the ceiling of the
rest rate is withdrawn: mass is content, an amount (Highlights 3.19), and
the phase reads it only modulo the circle, so no rest rate needs a wide
phase to be represented.

## 15. Time dilation from transit: a moving bound group's clock runs at 1 − v

Recorded 2026-09-17 from the model owner's statement of that day ("speed is a clock slowing, otherwise everything would move at c"); open.

**Statement.** In the ray-event model everything moves at one Link per interval; matter is slower only because the output clock of its bound group delays its departures (Highlights 3.4, 3.28). A bound group that moves one Link every k intervals therefore has speed v = 1/k in units of c, and its internal clock, the binding rule that fires once per resident interval (its tick), fires only while the group is resident: of every k intervals one is spent on a Link with no tick. To first order the moving group's clock rate is (k − 1)/k = 1 − v relative to a group at rest. Highlights 3.28 states the premise as the model's rule ("speed is a clock slowing", model owner, 2026-09-17): there is no kinematic rule in the engine, so the dilation, if it appears, must emerge from this transit and from nothing else.

**Prediction.** Nature measures the rate √(1 − v²) (the Lorentz factor; the muon lifetime in flight). The model as stated predicts 1 − v for a single hop per k intervals; a group whose rays share the transit between them, or whose delay is per face (the six clocks of 3.28), may give a different curve. The run decides: measure the tick count of a bound group at rest and at v = 1/2, 1/3, 1/4, 1/8 over the same number of intervals and compare the ratio with both 1 − v and √(1 − v²).

**What would falsify it.** A measured rate that follows neither curve, or a rate that depends on the direction of motion relative to the lattice axes beyond the remainder tolerance of Highlights 3.17 (an anisotropy the lattice would then show at the scale of Links). If the model gives 1 − v and nature √(1 − v²), the discrepancy is a real prediction against experiment (the muon lifetime), and the binding rule or the per-face clocks are where the model would have to change, not the engine.

**Status.** Open. Needs feature 8 (binding) on `main`; experiment A14 of `docs/EXPERIMENTS.md`.

## 16. What fixes the lag modulus N

Recorded 2026-09-17 from Highlights 5.5 ("the constants: what is derived and
what is an input"); open.

**Statement.** The modulus N of the lag register (Highlights 3.28) is a
declared width today, an input: the finest delay a field can impress on the
ray it meets, one part in N of a phase step, and the N of hypothesis 14,
whose G = ħc/(N m₀)² is a reparametrization until something fixes N. The
hypothesis is that N is not free but fixed by one of three things: the top
of the mass ladder (the largest loop-closing content of hypothesis 12, so
that N m₀ is the Planck mass by construction), the resolution the spreading
field needs (the finest share a split table can carry before the Node-owned
remainder of Highlights 3.5 makes a quantum wait), or nothing, in which case
N stays an input.

**What confirms it.** One N from two runs: the largest loop-closing content
at which the spectrum of A10 fits, put into hypothesis 14's formula with the
measured m₀, returns the measured G within the accuracy the board allows
(A11 at the real N); or the resolution the spreading field needs (A1, A6)
and the lag width found equal at every phase width, one declared width
serving both.

**What refutes it.** A ladder whose top and a bending whose N disagree by
more than the remainder tolerance of Highlights 3.17, or a spectrum that
fits at every N alike, so that the ladder does not fix N; then N is an
input, the third answer, and hypothesis 14 stays a reparametrization.

**Status.** Open. Decided by experiments A10, A6 and A11, after feature 14
(binding as a loop) and feature 8b (the lag modulus); the catalog's
`lag_bits` entry names this hypothesis beside feature 8b, and until it is
answered the model predicts the form 1/N² and not the value of G.

## 17. What fixes the release ratio and the coupling table

Recorded 2026-09-17 from Highlights 5.5 ("the constants: what is derived and
what is an input"); open.

**Statement.** The release ratio n/d of a field family (the share of its
amount a charge releases per Port heading, `release` in the catalog, [1, 4]
for light today) and the integer tables of the couplings that read a field
(the Born table, the delay table, the strength table of the electron's turn)
are declared today, inputs: the strength of the electric coupling is the
ratio and the table, a reparametrization until something fixes them, as
hypothesis 14's formula is for N. The hypothesis is that they are fixed by
the symmetry of Highlights 3.27 (one rule for every Node, every Port and
every family) and the path counting of 3.5 (the multinomial count of paths
that makes the spread field a sphere at large scale and the same flux cross
every shell), or by nothing, in which case they stay inputs.

**What confirms it.** One ratio and one table written from the symmetry and
the path count before the run, giving A5's Coulomb exponent and A1's fringes
at every phase width without a fitted number, and the strength A5 measures,
in the units of the ladder, agreeing with the measured fine-structure
constant within the accuracy the board allows.

**What refutes it.** A5 or A1 passing only with a ratio or a table that the
symmetry and the path count do not single out, or two ratios fitting equally
well; then n/d and the tables are inputs, the second answer, and the value
of α is not predicted.

**Status.** Open. Decided by experiments A5 and A1 (the release ratio and
the tables) and A6 (the mass field's release), after feature 12b; the
catalog's undecided release ratios (`rays.mass_field.release`,
`rays.gluon.release`) name this hypothesis beside their runs, and until it
is answered the model predicts the form 1/r² and not the values of the
couplings.
