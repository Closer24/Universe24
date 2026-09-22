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

The GameBoard is finite and its boundary is configured, open or periodic. The
closed-universe probes (expansion and redshift (`examples/relativity-probes/`, deleted on 2026-09-17))
measure what a periodic GameBoard does to a ray that laps it: a stepwise stretch
within one lap, a delay-growth redshift, and a loss of outward momentum that
does not depend on radius when one dimension is short. The hypothesis is that
a closed GameBoard with one compressed dimension reproduces the transition from
Newtonian pull to a flat curve at a radius set by that dimension. What is
measured is the loss curve on small GameBoards; what is open is whether any
GameBoard size and any compression give the curve nature shows, and no size of
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
quantum contacts and Bell's test run on the same GameBoard. It is not yet one
theory: the mixers, the instruments, the phase advance per link, the `|p| / D`
rule, the cosine table and the singlet law in the bond registry are configured
data, measured to hold, not derived. The program is to replace each configured
law by a rule of the GameBoard and show by a run that the measured tables do not
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
What is measured is the loss curve on GameBoards up to period 9; what is
pending is the open three-dimensional control with the identical metric, and
until it lands the probe report itself calls this a candidate, not a result.
A size sweep of the slab (period 3, 9 and beyond, radii to the GameBoard edge)
shows how far the flat part reaches on each GameBoard; the radius where the
measured curve stops following the hypothesis is the size at which a larger
GameBoard is needed, and that number belongs in the report.
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
and -0.70 +/- 0.45 outside it (6 radii). The GameBoard's transition is set by a
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
of a Friedmann universe with `a(t) ~ k(t)`, so a static GameBoard with the
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
where the GameBoard and expansion differ, `(1 + z)^-2` against `(1 + z)^-4`,
and the raw measured exponents (2.59 and 3.37 in R and I, Lubin and Sandage
2001, before any luminosity-evolution correction) lie above the GameBoard's
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
GameBoard's Tolman exponent as n = 2.0013 +/- 0.0008 under the per-link phase
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
line on a small GameBoard; measure the phase gained per step as a function of the
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
the pair test can show. The test (issue #169, feature 4): the pair GameBoard with
the source as a marked Node, two Detectors at equal distance with settings
drawn per pair, coincidences counted within a declared window, CHSH computed
from clicks only; then the same GameBoard with one arm delayed by more than the
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

The verdict in one sentence (2026-09-20, the audit of issues #359 and #361
on the Beam Law, A2 registered): the model predicts S = 2; the loophole-free
experiments measured 2.4 to 2.7; the model fails here, by choice. The choice
stated exactly: the model keeps the local determination of every outcome by
the arriving event and the setting, which nature does not keep (that
assumption, not no-signalling, is what Bell's theorem says S > 2 refutes);
no-signalling, which nature does keep, the model keeps as well, measured
exact in A2. A narrow phase window with `pass` reaches S = 4 on the counted
coincidences at 72 % single-side efficiency while S over all pairs stays
below 2, which reproduces the experiments before 2015 and is refuted by the
loophole-free ones: the detection loophole, measured, not a reproduction of
Bell. The shared number of postulate 22 is not restored to reach 2.83; the
model declared that mechanism non-local, and restoring it for the number
would be tuning to the result.

The single-click counts, stated so that it can fail (the same audit; the
owner's decision of 2026-09-20 on issue #359: no memory at the detector):
the Beam Law says interference is a reading of the events that reach one
detector set in one interval, so with one event per interval per Node the
counts are additive and no fringe builds up one click at a time; the
single-photon and single-electron experiments (Tonomura 1989 and every one
since) build the fringes one particle at a time. The model predicts additive
single-click counts and is falsified there unless A10 at a low rate
(registered as the law's own prediction, measured on the branch) shows
otherwise; the owner refused the detector memory that would reproduce the
counts by a mechanism nature's detectors do not have.

The superdeterminism suspicion, stated so that it can fail and measured
(2026-09-20, issue #363, the owner's "Alice and Bob are part of the
GameBoard, no?"): A2's S = 2 was read with the settings written in the
world file, a hand from outside the universe, and a model in which
everything is on the GameBoard and everything is determined by the initial
state is open to the reading that the settings and the pairs are
correlated through their common past, in which case S says nothing either
way. The hypothesis, falsifiable: the law does not correlate things that
never met, so with the settings read from the phases of two streams
released by two further lamps that share no clock, no release and no
reading with the pair lamp, every E stays on the triangle 1 - 4 k / N and
S = 2 exactly on an ordered quadruple; it fails if any bin leaves the
triangle or any marginal leaves 1/2 while the same reading, on a world
whose three lamps are fed from one clock, sees the correlation built in.
Measured ([A2 with the choosers on the GameBoard](EXPERIMENTS.md#a2-with-the-choosers-on-the-gameboard-2026-09-20)):
fifteen bins of 128 pairs, every E the triangle exactly, S = 2 exactly on
(0, 25) x (8, 29), the largest S over every quadruple 2, every marginal
1/2 exactly; the one-clock control E = 1 in every bin with no quadruple
possible. Bell's assumption is an assumption in the universe and a
measurement in the model; the verdict above stands with its full weight,
and the model's limit is the local determination of each outcome, not a
conspiracy of the initial state.

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
error the reference units declare, at one `N`. If no
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

Status (2026-09-20, the model owner on issue #369; Highlights 5.4, the log's
record 106): the ladder half is closed by decision. The masses and the
charges are the initialisation, the catalog's declared contents and charge
per unit, and the Beam Law as it stands selects no content (every content is
a declared amount, the paid exchange is linear and conserving, so every
equal split is a fixed point; the charge per unit is any rational). The
composite-spectrum half stays open and depends on physics the law does not
have: a bound composite's content is today the exact sum of its parts (the
deuteron 2.225 MeV and the alpha 28.3 MeV above nature), so a rule under
which binding moves content off the bound bodies, exactly, into quanta a
detector can click is the missing design (issue #369, three candidates, the
owner's decision pending).

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

## 14. The gravitational constant from the GameBoard, G = ħc/(N m₀)²

Recorded 2026-09-17 from the model owner's statement of that day; open.

**Statement.** In the ray-event model gravity is bending by delay (Highlights 3.28): the retained content of a Node makes it slow, and the information that it is heavy spreads in ray form. The unit of mass is the rest rate m₀ of the lightest massive family (one phase step per interval), and the largest rest rate the phase can represent is N steps per interval, N being the phase modulus declared by `phase_bits`. The hypothesis is that the effective gravitational coupling measured on the GameBoard scales as the inverse square of that ceiling, G_eff ∝ 1/N², so that in physical units G = ħc/(N m₀)², with N m₀ playing the role of the Planck mass. The real N is then of the order of 10²², which the 74-bit phase of the integer width convention can hold.

**Prediction.** Measure G_eff from the bending of a light ray passing an external body (Highlights 3.19, feature 7b, `external-body-v1`; named "fixed body" earlier on 2026-09-17) of declared family and amount, at rest and at its default coupling, absorption into its explicitly accounted sink, its motion caused by fields only and its velocity an exact accumulator that completes no Link at the body's amount, so that against the light ray it stands still (experiment A6 of `docs/EXPERIMENTS.md`) on one small GameBoard with N = 2⁸, 2¹⁰, 2¹², 2¹⁶ and everything else held fixed; G_eff · N² is the same number for all four, within the remainder tolerance of Highlights 3.17. If G_eff · N² drifts with N, the hypothesis fails as stated, and the drift's form says what the delay table does instead.

**What would falsify it.** A bending that does not fall as 1/N², or that depends on the GameBoard size, the impact parameter or the family in a way the delay rule does not predict; or a real-N run (experiment A11) whose G, converted with the measured m₀, is not the measured G of nature within the accuracy the GameBoard allows.

**Status.** Open. Feature 8 (`ray-binding-v1`, 2026-09-17) ran the owner's
acceptance criterion as `test_ray_binding.py` on a 21^3 GameBoard with a mass of
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

**What would falsify it.** A measured rate that follows neither curve, or a rate that depends on the direction of motion relative to the GameBoard axes beyond the remainder tolerance of Highlights 3.17 (an anisotropy the GameBoard would then show at the scale of Links). If the model gives 1 − v and nature √(1 − v²), the discrepancy is a real prediction against experiment (the muon lifetime), and the binding rule or the per-face clocks are where the model would have to change, not the engine.

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
measured m₀, returns the measured G within the accuracy the GameBoard allows
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
constant within the accuracy the GameBoard allows.

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

## 18. K as a uniform background: the rest clock and the gravitational slowing as one reading

- **Statement (the model owner's question of 2026-09-18, recorded as a
  hypothesis, not acted on).** The clock of a thing is content / K (Highlights
  5.4, point 19) with one K for the world, and the wait near a mass reads the
  amplitude of the mass's field at the thing's Node (the direction of the same
  day, derived in DERIVATIONS.md round 6). If K were itself the amplitude of a
  uniform background of shadows on the whole GameBoard, the two would be one
  reading: the rest rate would be the content times the background's
  amplitude, and the slowing near a mass the content times the local excess of
  amplitude the mass adds. In the language of physics the uniform background
  plays the part the Higgs field plays for rest mass (a uniform field every
  massive thing is coupled to), while its local variation is the gravitational
  potential; physics keeps these two apart.
- **What it would need.** A background that is sourced: DERIVATIONS.md round 5
  shows an unsourced standing profile decays under the mixing (two thirds of a
  lone re-release radiate in twenty intervals), so a uniform background must be
  fed by something, or be the standing part of every thing's field summed over
  the GameBoard (a closed GameBoard), which is a claim to derive before anything else.
- **Status.** Open. Not needed for the four gravitational tests (A6 repeated),
  which read the local amplitude with K as a constant. Taken up only if the
  runs under the current reading fail in a way this would cure, or the model
  owner asks.

## 19. The wait per lane: light's index twice the clock's slowing from the two lanes of a Port

- **Statement (the mathematician's candidate of 2026-09-18, the evening, recorded
  and not acted on; DERIVATIONS.md section 55 (v)).** Under the law of the
  shadow light in flight is a wave and takes no push, so its bending and its
  Shapiro delay come from one index, n = 1 + w|u_M|, as in general relativity
  they come from one metric; with the one w that gives GR's clock the index is
  1 + GM/r, half of GR's 1 + 2GM/r, and the bending is 2GM/b, half of Einstein's.
  Both reach GR's values if a quantum of light pays the wait twice per Node. The
  candidate rule: the wait is owed per lane crossed (Highlights 5.4, point 25: a
  Port is two lanes, in and out). A quantum in flight crosses two lanes at every
  Node and owes 2w|u_M| per Node; a held content crosses none and reads once per
  interval, owing w|u_M|. One w then gives the clock 1 − GM/r, the redshift, the
  bending 4GM/b and the delay 2GM ln(4x_Ax_B/b²) to first order, the
  parametrized post-Newtonian γ = 1.
- **What it would need.** A hold per Node per family for a quantum in flight
  (DERIVATIONS.md section 35's option II-b with the amplitude), which is Node
  state beyond the six Ports unless it is written as the family's remainder
  counter at the Node; and the mass's field a wave in whole units at the light's
  Nodes (q_M ≥ 1740 r², section 47 (iii)), or the formula layer.
- **What would refute it.** A6 repeated on the formula layer with light as a wave:
  the tilt of the front read at a screen behind the mass against 4GM/b ·
  X/√(b² + X²), and the arrival of the crest against 2GM · 2asinh(X/b) in light's
  Links of travel; a per-family w declared instead (point 16) gives the same
  numbers and is the alternative if the lane rule is struck.
- **Status.** Open; the model owner's. (2026-09-20: the Beam Law has no
  wait per lane and no index; light in flight is bent under the meeting,
  section 20, and not delayed in time.)

## 20. Light beside a mass under the meeting: bent as a report, with the sign, the M / b form and the grain; an interferometric Shapiro phase; no delay in time, no horizon

- **Statement (the law's own prediction 2, updated on 2026-09-20 by the
  model owner's decision on the meeting, M-R: "an event in transit reads
  the crowd as a body does, a report, not a balance";
  [BEAM_LAW note 35](BEAM_LAW.md#10-implementation-notes-2026-09-19-the-implementation);
  the identity `meeting-v1` under the world key `meeting`).** Until that
  day the law predicted that light is neither bent nor delayed by a mass,
  and series K measured it (0.000 pixel, 0.00 interval). Under the meeting
  a paid unit in transit reads the free crowd of a mass at every free-space
  Node it shares with it and turns toward the crowd's source by one grain
  step of the direction table per N crowd units met, the sign the gravity
  column's (kappa = -1, the target -V), the count kept on its phase
  register. The prediction: (i) the sign: light is bent toward a mass, the
  centroid of a beam at a screen moving toward the mass's line, never away;
  (ii) the form: the deflection grows with the crowd met along the path,
  M / b within the finite path (doubling M doubles the crowd met, halving b
  raises it by less than two on a digital line), the same form as nature's
  4 G M / (b c^2) and not its value, since the grain is the fan's step (2.4
  degrees on series K's table, 3 at the finest fan the law allows), 10^4
  times nature's angle at the Sun's limb: a grain is the smallest
  deflection there is, so the beam does not shift as one but as a mix of
  0, 1, 2, 3 steps whose mean the centroid reads; (iii) the interferometric
  Shapiro phase: the light's phase at a detector is shifted by the crowd
  met along its path modulo N, so an interferometer reading two paths past
  a mass reads a fringe shift proportional to M / b, while the phase rate
  at a pixel stays the lamp's turn and no redshift of the light in flight
  appears; (iv) no delay in time: the flight table is one speed for every
  direction and the meeting turns a direction, never a pace, so the mean
  age of the arrivals moves only by the extra Links of the bent digital
  lines (about one interval at series K's b = 6), against nature's Shapiro
  delay in time; (v) no horizon: a dense crowd wraps the light back (the
  arc permutation's debt state, the direction nearest the source flung to
  the farthest), it does not hold it; light aimed within a grain of the
  source is reversed, not captured on a circle; (vi) what the meeting does
  not give: the aberration of gravity (prediction 3, the push along the
  arriving u_d) and the Nordtvedt-like effect (prediction 4) stay as they
  are, the mass defect stays absent, and two masses' crowds never turn each
  other (only paid units read).
- **What would refute it, stated so that it can fail.** At a screen behind
  a mass under `meeting: true`: a centroid moved away from the mass, or one
  that does not grow with M at fixed b, or a deflection below the grain of
  the fan (a continuous small angle), or a mean age moved by more than the
  bent path's extra Links (a delay in time), or a pixel's phase rate moved
  off the lamp's turn (a redshift in flight), or a phase offset at a pixel
  that does not follow the crowd met along that pixel's path; in an
  interferometer of two paths past a mass, a fringe shift that does not
  grow with M / b.
- **Read on series K under the key (2026-09-20, [EXPERIMENTS](EXPERIMENTS.md#k-under-the-meeting-2026-09-20)).**
  The sign held in every world (the centroid -1.8, -4.4 and -2.3 pixels
  toward the mass at (M, b) = (2^12, 6), (2^13, 6), (2^12, 3); 0.000 in z);
  the form held at twice the mass (-4.36 against the offline flight's
  -4.29; 210 rays wrapped to the faces against 209) and at half the impact
  distance (-2.30 against -2.59); at (2^12, 6) the centroid read -1.79
  where the offline flight said -3.0, because the mass, a measured event,
  measures the light that reaches it (122 rays of the beam clicked on the
  mass, the most turned ones, which the offline flight let pass through
  its Node); the mean age moved by 0.5 to 1.2 intervals (the bent path,
  no delay in time); the phase offset is sharp per pixel (the resultant
  0.9 to 1.0 at the lit pixels of `mass` and `near`) and differs from
  pixel to pixel by tens of steps, so the screen-wide offset is not one
  number (the expectation "about 55 steps" was the mean crowd met over
  the rays, not a reading any one pixel gives); the phase rate estimator
  of the tool (the unwrapped slope of a pixel's record phases) is not
  clean under the meeting (the pointer at a pixel mixes rays of different
  offsets), so the "no redshift" part is read off the per-click offsets
  and not off the rate; the lens world's two beams crossed 71 Links past
  the mass at b = 6, a grain of the fan. Nothing was tuned.
- **Status.** Landed as `meeting-v1` (2026-09-20); the register's K entry
  under the key is the reading; the value of nature's angle stays out of
  reach by the grain, and the Shapiro delay in time is not in the law.

## 21. A moving body's clock: the engine's rate is one at every speed, nature's gamma a limit stated so that it can fail

- **Statement (the physicist's finding of 2026-09-20, WEAK.md 2.4 and
  PREDICTIONS entry 12, recorded on the model owner's decision of the same
  day that the engine stands).** Under the Beam Law a measured event's
  clock is the count of its self-creations: `_frame_all` advances its age
  at every interval in which it owes nothing, whether or not `_move` steps
  its body in that interval, so a body thrown at the speed v (Links per
  interval on an axis: by the step rule one Link per (S x M + p) / p
  self-creations under the width S, with p its momentum in label units
  and M its content) ticks at the rate of a body at rest, and its range
  before a transformation at the key `at` is v x at Links, linear in v.
  TERMINOLOGY's earlier sentence on the self-creation, "a transfer is not
  one", read as if the interval of a body's step were skipped, which would
  give the rate 1 - v, first order in v and anisotropic (the Manhattan sum
  of the axis speeds; entry 15 above states that reading for a bound
  group of the earlier law); the engine never did that, and the sentence
  is corrected (2026-09-20). Nature: a moving clock runs at
  sqrt(1 - v^2) (the muon at rest 2.197 us and at gamma 29.3 in the CERN
  storage ring 64.4 us; Rossi and Hall 1941; the transverse Doppler of
  Ives and Stilwell 1938; GPS). The law has no kinematic rule (POSTULATES
  4: nothing slows a clock because of motion), so its prediction is
  stated as it stands, no slowing at any v, a plain disagreement with
  nature at every v, recorded so that it can fail and not tuned in.
- **The reading (series J4, defined and not yet run).** Muons (`mu`, a
  free family of content 207) with `become` at 64 into `e` and the
  products of the muon's decay declared, one at rest and one thrown at
  v = 1 / 4 and at 1 / 2 on an axis (the momentum p = S x M x v / (1 - v):
  69 and 207 in label units at S = 1 for M = 207) and one at 1 / 4 per
  axis on a diagonal, in an open bar with no crowd (`release` [1, 2^20]);
  the products' face clicks the DETECTOR reading (the tick and the Node of
  each click give the tick of the decay and the body's range), the
  `become` lines the GAMEBOARD reading. Expected on the engine as it is:
  every muon fires at tick 64, at rest at its Node, at v = 1 / 4 sixteen
  Links on and at 1 / 2 thirty-two Links on; under the corrected
  sentence's old reading at 64 / (1 - v), 85 and 128, the ranges 21 and
  64; under nature's gamma at 66 and 74 (gamma 1.033 and 1.155), the
  ranges 16.5 and 37. The three readings are told apart by one run.
- **What would refute it.** A measured trigger tick of a moving muon
  other than 64, or a rate that depends on the direction of motion (the
  engine's clock is then not what this entry says). Against nature the
  entry is not refuted by a run: it is a limit of the law. What the law
  would need to give nature's rate is a clock that counts the intervals
  in which the body does not step and weights them by the second order of
  the speed, a kinematic rule the law does not have and this entry does
  not propose.
- **Status.** Open; the model owner's (2026-09-20: the engine stands, the
  terminology corrected, nature's gamma a limit of the law). Series J4 is
  the reading to make.

## 22. The amplitude law: the world's clicks read from the GameBoard's paths, Born, interference and Bell below Tsirelson at finite N, stated so that it can fail

- **Statement (the model owner's decision of 2026-09-20, Highlights 5.4,
  "DECIDED: `amplitude-v1` is built"; the design
  `docs/designs/amplitude-v1/DESIGN.md`; [BEAM_LAW note 37](BEAM_LAW.md#10-implementation-notes-2026-09-19-the-implementation)).**
  Under the world key `amplitude` a lamp births one record per
  self-creation; the GameBoard carries the record's rows, each with its
  record, branch and multiplicity, through the splits, the turns, the
  rotations and the gates of the world's tables, locally and exactly,
  cancelling antiphase rows of one record at the merge; the record's
  click is read from its offers at the `sum` sets by its birth phase u on
  the ladder of its cells, the rungs at the nearest integer of N. The
  claim: the engine's own tables then give Born's rule as a count over
  the circle (the cells' weights the squares of the coherent sums, one
  Node at a time), interference (the Mach-Zehnder at one port,
  Elitzur-Vaidman), the pair's correlation with exact marginals and
  S = 2 sqrt 2 - epsilon(N) at or below Tsirelson at every N, GHZ, the
  which-path world and the CNOT, with no draw and no signal: the outcome
  of a pair is the one u of the one record. Not claimed: that quantum
  mechanics is solved; the circle's N, the tables' 1/256 grain and the
  ladder's rounding are the law's own and give the departures below. A
  non-absorbing read is a deferred offer, not an outcome: the layer keeps
  a selector keyed by the record's current label set and the click
  gathers at the record's far completion, a later rotation replacing that
  label set; a read followed by a rotation and a second read is not a
  sequential measurement and is out of the register's contract
  (sequential-instrument use is unsupported under `amplitude-v1`; issue
  #584, 2026-09-21).
- **The reading (series L, run on 2026-09-20, the fingerprint
  `ff5c382d672f`; [EXPERIMENTS](EXPERIMENTS.md), "L, the amplitude
  law").** Every acceptance integer of the design reproduced: the
  Mach-Zehnder 64/0, 0/64, 32/32, 64/0, 63/1 and the unequal arms 64/0,
  32/32, 0/64; Elitzur-Vaidman 32/17/15 and 32/16/16; the two slits at a
  low rate wall 34, screen 15, faces 15 of 64; the pair S = 176/64 with
  every marginal 32/64, the registered quadruple 156/64, the which-path
  world 88/64, no maintenance at 116 Links; GHZ's triples and products;
  the CNOT pair 176/64, CNOT twice the identity, GHZ by one gate;
  S = 2896/1024 and S = 11584/4096. The departures: the record's total
  over u takes eight values (65448 to 65773 of 65536) where the design
  read 0.0019 at u = 0; the two-slit shares are this geometry's under the
  per-Node rule, not the design's 3/5 and 2/5; the design's bound
  |E - cos| <= 1/N holds at N = 1024 only (at 64 the count's grain, at
  4096 the tables' 1/256 entries), and epsilon <= 4/N holds at 1024 and
  4096 and not at 64.
- **What would refute it.** A registered world under the key whose
  gathers differ from the reading tool's replay of its own record (the
  ladder is then not what this entry says); a Mach-Zehnder gather at the
  dark port with equal arms; a marginal of the pair other than 32/64; S
  above 2 sqrt 2 at any N with the rungs at the nearest integer; a GHZ
  triple outside the allowed four; a world where the crowd's `wave` or
  `beam` reading changes under the key. Against nature: the tables'
  rounding beyond 1/N at N = 4096 and the record's total over u are the
  law's own limits, recorded and not tuned; at large N the numbers are
  the paper's, not nature's exact ones.
- **Open.** The full register replay and the coverage-measured gate
  set; Grover beyond the register's ceiling; two sequential gates on an
  entangled record; the register's lamp worlds re-read under the one
  click (their verdicts, EXPERIMENTS). Landed at stage (vii) of
  2026-09-20 ([MIGRATION](MIGRATION.md), (vii-1) to (vii-4)): the one
  click (the design's section 6, the record form the law, the key
  deleted) and the K finding's two changes, u as the record's own field
  beside the running phase and a row's push by its share of the label
  (note 37 (ix) and (x)).
- **Status.** Open; the design's acceptance tests pass on the branch
  `amplitude-impl` (the runs in the register), not merged at this
  writing.

## 23. The hand: a left-handed product leaves against the parent's axis, the mirror world's click lands on the other side, stated so that it can fail

- **Statement (the model owner's decision of 2026-09-20, record 128 of
  [the log](LOG_2026-09-20.md), "the hand's three choices confirmed";
  the physicist's design hand/DESIGN.md, record 122; the mathematician's
  integer form, record 120; [BEAM_LAW note 39](BEAM_LAW.md#10-implementation-notes-2026-09-19-the-implementation)).**
  Under `hand-v1` a row carries a hand, the sense in which it turns about
  its own direction (one column, -1, 0, +1, a pseudoscalar under the 48
  symmetries of the cube), a body an axis (one of the six headings, an
  axial vector), and a `become` at a body with an axis sends a product of
  hand h on the body's directions d with sign(A . u_d) = h only: a
  left-handed product AGAINST the axis, a right-handed one along it. A
  table entry admits one hand (the parity filter); nothing else of the
  law reads the hand. The claim: on the GameBoard parity is exact for
  every world without an axis and a handed product, and it is broken
  exactly and only where a birth has both, as in nature (Wu, Goldhaber):
  the mirror image of the apparatus with the same left-handed catalog
  gives different counts, the click on the other side; the full mirror
  (the catalog mirrored too) gives the same counts; and the violation is
  the catalog's one-handed families, data of the law and not of the
  state. Not claimed: spin dynamics, an angular-momentum ledger, V-A's
  energy dependence, CP.
- **The reading (series P, run on 2026-09-20; [EXPERIMENTS](EXPERIMENTS.md),
  "P, the hand"; [the worlds](../examples/events/hand/README.md)).**
  `w_hand`: the W born at the neutron's key with the hand -1 on +x
  against the axis -x, clicked at the proton at x = 3 at tick 9 with the
  push (192, 0, 0); under the mirror in x with the hands and the axis
  kept, at the proton at x = 1 with the push (-192, 0, 0), the tick, the
  amounts, the contents and the charge line equal. `wu`: the beta on -x
  against the axis +x, clicked at the reader at x = 0 at tick 21, the
  antineutrino on +x out of the face at tick 23; under the mirror the
  click at x = 16 and the face -x. `nu_hand`: the reader of the right
  hand 0 clicks, the reader of the left hand 1022, the far detector 0,
  mirror-equal. The control `w_two_sides` and the full mirror and a
  proper rotation on all four: equal.
- **What would refute it.** A world without an axis or without a handed
  product whose polar mirror differs (a parity difference where the law
  says none); a world with both whose full mirror differs (the law not
  covariant); a handed product born on a direction of the other sign
  against the axis, or on the equator; a hand read by a push, a moment,
  a pointer or a clock; a `pass` entry admitting one hand; a merge of
  two rows of opposite hands. Against nature: the beta's asymmetry here
  is complete (one direction admitted among the six, a bar's one side),
  where nature's is a cosine of the angle to the spin with the
  electron's speed as its size; the limits above are the law's own,
  recorded and not tuned.
- **Open.** A fan of directions under an axis (the admitted hemisphere of
  a fan, the mathematician's count); a hand filter on a `read` entry as a
  neutral current of one hand (the Z with no family); circular light
  through a hand-selective mirror; the label rotation's composition with
  a label hand (the linear polariser as `rotate` plus the label click,
  Malus's 64 / 32 / 0 at s = 0, 16, 32 on the design's rung rule, not
  run).
- **Status.** Open; `hand-v1` built on 2026-09-20 with the three worlds
  of series P and the parity test (`tests/test_hand.py`).

## 24. The binding energy is the paid content a body gives at its first contact, measurable as the border's clicks

- **Statement (the model owner's records 115 and 137 of 2026-09-20; the
  physicist's design `docs/designs/binding_v1/DESIGN.md`, record 132;
  [BEAM_LAW note 40](BEAM_LAW.md#10-implementation-notes-2026-09-19-the-implementation);
  `binding-v1`).** A nucleon carries paid content (a paid family with a
  lifetime, held: content carried, never released) and gives it once, at
  its first contact under `measure`, to the flight on the heading away from
  its partner; the border `lifetime` clicks the rows two Links away with
  their content. The binding energy of a nucleus is then the content its
  bodies gave, read at the border as clicks (the gamma of n + p -> d +
  gamma), and the mass a detector reads of the bound pair is the declared
  content less what escaped, the books exact; after the formation the pair
  is stable for ever (nothing left to give; the contact is the momentum
  hand-over alone). The rule reads no family name, no partner and no shape.
- **The expectations (series N, [EXPERIMENTS](EXPERIMENTS.md#n-the-binding-that-costs-content-2026-09-20)).**
  The deuteron with `bond` 2 per nucleon: two border clicks of content 2,
  the escaped content 4 = 0.109 % of 3677 against nature's 4.353 m_e =
  0.1185 % (the register's grain is 1 m_e: 4 is the nearest integer, 8 %
  under); the mass read 3673. The alpha with the same one value: the give is
  per body, so 8 units, 0.109 % of 7354, the ratio 2.0 in energy to the
  deuteron where nature has 12.72: stated so that it fails, and it does. A
  prediction: the register's pp threshold G = 7111 becomes 7112 once both
  protons have given.
- **What it depends on.** The size is an input, the held paid content per
  nucleon (record 106: every content is an input; the law derives no
  binding energy, the content dynamics being linear). No form of the rule
  with one declared value gives the deuteron/alpha ratio; a second value
  (a content per bond that grows with the crowd, or a per-shape declaration)
  or a content-dependent rule would be needed for the alpha. "Every family
  paid" (the design's section 7) does not give the defect and costs two
  rules: recorded as a direction, not built.
- **What would refute it.** A third `bond` click of the deuteron; a `given`
  on a later contact; a step of either body after the formation; the books
  off by one unit at any tick; a bond click or a bond row in the control
  (one proton beside a lamp); a gather count of the control's lamp off
  I7's 2993. Against nature: the alpha's 2.0 x is the law's limit,
  registered and not tuned.
- **Status.** Built on 2026-09-20 (`binding-v1`, the register byte-identical
  where no body holds a paid family); series N run and registered: every
  pin of the design's run table inside; the design's momentum identity
  (measured + transit + escaped = 0) outside by +270 720 on x in the
  deuteron, the third-law gap of record 126 made visible by held paid
  content before the give (the review's finding, reported, not moved); the
  pp threshold not run.

## 25. The covariant readings: a body's energy as an exact square compared and never rooted, its clock gated by E'_0 / E', stated so that it can fail

- **Statement (the model owner's decision of 2026-09-21, record 270 of
  the log of 2026-09-20, on the derivation mathematician's section 17;
  the design as amended in [DERIVATIONS_BEAM 17.6](DERIVATIONS_BEAM.md#176-amended-per-the-physics-rule-review-of-covariant-readings-v1-record-297-the-nine-must-fixes-the-integer-forms-the-should-fixes)
  per the physics-rule reviews, records 297 and 314; `covariant-readings-v1`,
  the world key `covariant_readings`).** Beside the law, under its own
  identity: a body's record carries the exact square of its energy, W =
  E'_0^2 + 3 **p** . **p** with E'_0 = Q S M (c^2 = 1 / 3 declared as the
  pair [1, 3]; E' = 3 E), and E' the largest integer with E'^2 <= W, kept
  by comparisons alone (the load-time root once); after every
  self-creation the body owes `by_drive(acc_tau, E' - E'_0, E'_0)` further
  intervals, so its self-creations come one per E' / E'_0 = gamma
  intervals in the mean and everything counted per self-creation (the
  age, `become`, the turn, the lamp, the drive's gain) follows its proper
  time; the drive's wall loses its cap term, so the pace per lattice
  interval is p / E' = p c^2 / E, the covariant dispersion (on `main`'s
  per-axis drive, `step_axis`, for a momentum on one axis: the identity's
  domain until form B's directional drive lands, refused otherwise); the crowd's
  count is charged with the sum of the readings since the last
  self-creation; the free release runs per lattice interval at the
  content-equivalent of the body's own energy. E = m c^2 is then forced by
  the Newtonian limit (17.3 (iii)): E'_0 = Q S M with no freedom. Nothing
  of the six verbs changes; with the key absent every world reads as it
  did, byte for byte.
- **The expectations (series S, [EXPERIMENTS](EXPERIMENTS.md#s-the-covariant-readings-2026-09-21)).**
  The muon of J4 at p = 3640 and 12 856 label units (gamma 1.1074 and
  1.9558): its 64th self-creation at the design's 70.9 and 125.2 within one
  tick, the products' click on the +x face at 367 and 345 within two (the
  detector's reading); `coasting_none`'s `s_mz2` at its declared momentum:
  z = 0.369 +- 0.003 (the register's 0.2636 without the key); the invariant
  E'^2 <= W < (E' + 1)^2 at every interval.
- **What it depends on.** The pair c^2 = [1, 3] declared once (the flight
  table's per-direction (Q S_1 / T_D)^2 is the alternative and shifts the
  muon's 64th by 0.7 tick at 0.86 c); the grain g that fits W / g^2 in the
  word; the domain |p|_1 <= Q S M (above it the drive's one Link per
  self-creation gives a pace that falls with p); the push ceiling of one
  grain per interval, under which the root's comparisons are at most three
  per frame (a change of content moves E' by about Q S |dM| / g in that
  frame, counted and reported: the host cost apart from the model's).
- **What it does not give.** The contraction and the magnetic part of the
  push (17.6 M4, M5: `-grad(A)` alone is not Lorentz's 1904 pair; the
  vector potential needs a source's velocity no local reading gives,
  `source-velocity-v1` named and not designed); the fixed apparatus (a
  `fixed` measured event's momentum line is the push it took and never a
  motion: it carries no readings and keeps the lattice's clock); the
  discrete cadence from an empty accumulator puts the k-th self-creation
  at k + floor((k - 1) (gamma - 1)), one (gamma - 1) below k gamma.
- **What would refute it.** A `become` line of a moving muon at tick 64 (no
  slowing); a face click of the products off the flight table's derivation
  from the `become` line; a line where E'^2 > W or W >= (E' + 1)^2; a step
  of a body without the key that differs from the register.
- **Status.** Built on 2026-09-21 and run once (series S): the readings in
  [the register](EXPERIMENTS.md#s-the-covariant-readings-2026-09-21).

## 26. The free particle as a record of massive rows: de Broglie's fringes from h / p, stated so that it can fail

- **Statement (the model owner's yes of 2026-09-21, record 332 of
  docs/LOG_2026-09-20.md; the derivation mathematician's check,
  DERIVATIONS_BEAM section 23, record 336; the mathematician's design
  [docs/designs/massive_rows/DESIGN.md](designs/massive_rows/DESIGN.md),
  ADMISSIBLE in the physics-rule review's three rounds;
  [BEAM_LAW section 2](BEAM_LAW.md#2-the-record-of-a-ray-and-the-world-file);
  `massive-rows-v1`).** A free quantum of matter flies as a photon does:
  under the world key `massive_rows` a paid family declared `massive`
  births records of rows over its lamp's fan, each row carrying the
  momentum label p_D (the direction's unit vector at the scale p, the
  lamp's `momentum_magnitude`) and the content M (the family's `quantum`),
  flying by the flight's one accumulator at the rate 2 abs(p_D)_1 against
  the wall 2 E'_D (E'_D = isqrt((Q S M)^2 + 3 p_D . p_D) at load, the 3
  Flight's constant, the 3 of T_D, fixed by the law and read from no key
  where `covariant-readings-v1` declares the same factor as the d of its
  key `c2` = [1, d]; the photon its E'_0 = 0 case, one primitive), turning de Broglie's abs(p_a)
  N / h at every axis Link on one accumulator (the plane wave to one
  remainder), clicking by the click as built, and at the record's
  completion handing ONE quantum, M and the one label of the chosen row's
  direction, to the chosen set, a body from then on as series H's electron
  is; a body never becomes a record, and the bound electron stays a body.
  Every family carries the same tables by value (the photon's Flight's,
  the pair (1, 0)), no flag read at run time, no new verb. Claimed: de
  Broglie's wavelength h / p and the group pace p / E' from the declared
  integers alone, so the two-slit fringes of matter from the same law and
  apparatus as light's. Not claimed: the potential (23.4, the standing
  record under V), the transition of a body back to a record, Klein-Gordon
  or Schrodinger reached beyond the linear block (23.2).
- **The pin (`slits_matter`, [examples/events/massive_rows/README.md](../examples/events/massive_rows/README.md);
  the design's section 4, every number with its line, pinned before the
  run).** `slits_huygens`' plane, apparatus and Farey fan with `matter`
  (M 64, p 220, S 1, h 1024: E'_0 = 4096, E' = 4113, the pace 220 / 4113
  = 0.0926 c, the wavelength 256 / 55 = 4.6545 Links, the photon world's
  4.654): the lamp leg 139 (the photon's 13); the first `click` line at
  `screen_60` about the tick 955 within 5 (the group pace) and at
  `screen_37` and `screen_83` about 1016; the bright bands centred at the
  pixels 36.5, 60 and 83.5 within one; Pearson of the gathers' counts with
  the two-source cosine 0.89 +- 0.03 on the declared Farey fan (the
  registered photon's 0.891), the visibility 0.95 +- 0.03, the dark pixels
  0 to 3; the run 5750 intervals for every record of 4096 births, first
  at 1024 births (the wheel [633, 1024], 2700 intervals). The faces' and
  the wall's completions are a GAMEBOARD diagnostic beside it; the
  screen's gathers the DETECTOR reading.
- **What would refute it.** A band off by more than one pixel (the
  wavelength not h / p); the centre's first `click` line off by more than
  5 intervals of 955 (the pace not p / E'); no fringes (the phase not
  p . x); a registered world without the key whose bytes move; a books
  line off by one unit at any tick; a completion placing other than one
  quantum M and one label. The confrontation, dimensionless: Jonsson 1961
  and Tonomura et al. 1989 as 23.3 states them (the fringe positions in
  units of lambda D / s, the build-up one click per birth).
- **The price, named.** The completion's choice moves state (today the
  layer only reads): the apparatus's one non-local operation at the
  one-way border is physical under this identity, admitted by record 332
  ("the click gathering it to one Node"); the record's waiting is the
  host's, O(open records x ended Nodes), beside the offers it lives in.
- **Status.** Built on 2026-09-21 beside the law (`tests/test_massive_rows.py`,
  the register byte identical without the key); the pin's run and its
  verdict in the series README as run.

## 27. The conditional derivations of the Beam Law, each a declared hypothesis outside the law

- **Statement (the Boss's assignment under the owner's GO of 2026-09-21,
  about 23:28Z, its record to follow; the criterion of record 454 of
  docs/LOG_2026-09-20.md, under which the paper's cut dropped every
  conditional derivation).** A conditional derivation ties a formula to
  the law under a condition no derivation has closed: a limit taken, an
  identity beside the law, a calibration, a closure. In the repository
  such a derivation sat between the law and a hypothesis, and a reader
  could not tell which. From this entry on it has one status: a declared
  hypothesis outside the law, listed here with its condition, what would
  close it (a derivation in [DERIVATIONS_BEAM](DERIVATIONS_BEAM.md)) and
  what would refute it (a registered detector reading of the
  [confrontation register](NATURE.md) or the
  [experiments register](EXPERIMENTS.md)). No line of the law's text
  ([LAW.md](designs/vector_form/LAW.md), [BEAM_LAW](BEAM_LAW.md)) claims
  any of them; the paper carries them as HYPOTHESIS or OPEN rows without a
  number. The list is the derivation mathematician's closure of
  2026-09-21 (record 398, CONDITIONAL) with the conditional passages the
  paper's cut removed (the cut table of PLAN.md's wave 29). A row leaves
  this list when its derivation closes in DERIVATIONS_BEAM and a
  registered reading with its fingerprint confirms it (then it is the
  law's), or a registered reading refutes it (then a FAIL row under its
  identity); a closed derivation alone makes nothing the law's (record
  300: a formula gives, a run proves); nothing here is claimed by a run
  of the law.
- **The list.** Section numbers are DERIVATIONS_BEAM's; rows are NATURE's.

| Derivation | Where it lived | The condition | What would close it | What would refute it | Held by |
| --- | --- | --- | --- | --- | --- |
| The wave limit of the rows and its Poincare symmetry for arbitrary row data (the external reviewer's F06) | 4.1, 17.1; the paper's Lorentz theorem | derived for a plane-wave stream, second order in the Link; for arbitrary row data assumed | a proof in 4.1 for arbitrary row data with its error term (21.5's columns) | a registered front reading anisotropic or dispersive beyond the flight table's `1 / T_D` at the declared scale (series L7's cone, series Q's face clicks are the readings to date, inside) | this entry |
| Lorentz covariance of the bodies: the clock, the Doppler and the energy in motion | 17.6, 18.6; the paper's Lorentz section | the identity `covariant-readings-v1` (a body's readings covariant by declaration, one axis, gamma at most 2) | nothing closes it into the law: it is a hypothesis by construction; a derivation of the four readings from the six verbs would | rows 4a and 4b under the key (series S's readings inside their pins to date); a reading outside the identity's pins in its domain | entry 25 |
| The field equation's static case and the shell-mean inverse square | 3.3, 5.1, 5.5; the paper's Newton section | the fan dense at the reading's distance (`P >> r`), the reading a shell mean; on the 2616-direction fan `r^-1.83` against `r^-2` | the limit stated with its grain, order and error term per row (21.5's columns (3) and (5)) | series C's rings or series E's shells outside the stated ripple; a single-Node reading beside a mass is a comb, not a refutation | this entry |
| The kinetic closures on the six-heading gas: Euler's form, the sound speed, the viscosity, diffusion, Fick, Fourier | 25.5, 25.6; the paper's flow inventory (cut) | the product-measure (Boltzmann) closure of the slots' densities, its error unbounded | a bound on the closure's error | a registered gas reading outside its pin (none registered) | this entry |
| Kepler's three laws and the precession on the plane | 21.5 row 58; 3.3, 12b.2 | form B, the drive on the momentum's direction (BLOCKED in review, record 348, not on main); on main's per-axis drive the host's period is 687 | form B admitted into the law and the lamp worlds `s32_r24_lamp`, `s32_r12_lamp` run against row 58's pins | the periods and the apsidal angle outside row 58's pins; today series D closes no orbit (record 131) | this entry |
| The bending of light, the Shapiro delay, Snell's law, the second-order redshift | 5.4, 5.6; designs/gr_rows/DESIGN.md; designs/one_wall/NOTE.md (the generic form) | `optical-v1` in its generic form, built and merged as Part B (records 430 and 520; PR #659 at 2d5c7cf2) and, since 2026-09-22, the law's own for every world (record 847, the generic entry of the bending; no hypothesis, the key naming `gamma` alone, 0 by default) with `gamma` an input: the flight in the wall function's declared set at `1 + gamma` and the turn weighted by `(E^2 + 3 gamma` **p** `. ` **p**`) / E`; its readings in the register (examples/events/optical/README.md), the shifts' ratio at this fan unread | nothing closes it into the law: `gamma` is an input; a derivation of `gamma` from the six verbs would; the wall's and the push's terms are one, so no sum reaches 4 without the input (the mathematician's one-wall page) | series K under the key outside its pins; the law's own `0.000` a FAIL (24.3 row 14) | this entry
| Schrodinger's equation for a free particle | 23 | `massive-rows-v1`, named, not built | its build and the run of `slits_matter` against 23.3's pins | the bright bands off the pins by more than one pixel | entry 26 |
| The expansion as a growing wall and Hubble's law | 15, 20.4; record 279 | `expansion-v1`: the flight's wall `2 T_D a` with `H` declared, absent by default; a declared assumption | none: an assumption by the owner's word; a derivation of `H` from the law would | rows 3 and 11a to 11c (the coasting `q = -0.108` is the law's own reading, without the wall) | this entry |
| The magnetic part: Faraday, Ampere-Maxwell, the Lorentz force, Biot-Savart | 12.1, 17.6 | `source-velocity-v1`: a row carrying its source's velocity; named, not designed | a design passing the three tests, then a run against pins | row 5b (the two-arm anisotropy), the transverse push `1 / gamma` | this entry |
| The weak forms: the decay curve memoryless, the neutrino's passage | 18.2 with its addendum | `decay-by-crowd-v1`: the rate the family's, the crowd supplying the freshness | the run against the addendum's pins (J1's neutrons, the beam-and-bottle pin) | rows 8a and 8b under the identity (the law's own rows FAIL) | this entry |
| The uncertainty relation's physical reading (the external reviewer's F07) | 22.1, 22.2 | the phase circle read as position and its transform as momentum, a stated identification; the finite-Fourier bounds themselves are mathematics on `Z_N` | a derivation of the reading from a detector's rule | row 10, the single opening under the one click (pinned, not run) | this entry |

- **Two items of record 398's neighbourhood are not here**: the energy
  dictionary, closed as 24.1 row 25; the minimal mass, a theorem given P8.
- **What this entry does not do.** It adds no derivation and moves no
  number; it names no run. Where a row says "this entry", the hypothesis
  has no entry of its own on this page and gets one when a design with
  pins exists (the rule of this page's head).

## 28. The directional drive of a body: the Bresenham line of the momentum against one wall, stated so that it can fail

- **Statement (the model owner's approval of form B, 2026-09-22, record 652
  of docs/LOG_2026-09-20.md; the design
  [docs/designs/drive_b/DESIGN.md](designs/drive_b/DESIGN.md), form B in the
  integer form (c) of [light_speed/FORM.md 3.1](designs/light_speed/FORM.md#31-amended-after-the-physics-rule-review-of-the-build-m1-the-residue-across-lines-and-the-correction);
  [BEAM_LAW note 49](BEAM_LAW.md#10-implementation-notes-2026-09-19-the-implementation)).**
  Under the world key `drive_b` (`drive-b-v1`, absent by default) a free
  body's three drive accumulators gain `p_a Q` each against ONE wall `W =
  Q^2 S M + |p|_1 T_h` (`T_h = isqrt(3 Q^2) = 110`, formed at load; `Q^2 S
  M` alone under `covariant_readings`), and the axis furthest over the wall
  makes the Link, the others keeping their overflow: the Bresenham line of
  the momentum, one Link per interval at most, no coincident fire lost, no
  direction read, no root at run time. The Manhattan pace `|p|_1 Q / W` on
  every direction; on a heading form B's `|p| x 64 / (Q S M x 64 + 110
  |p|)`; Newton's `|p|_2 / (Q S M)` at a small momentum to zeroth order; the
  cap `64 / 110` Euclidean on every direction, below the rows' pace on
  every line and equal to it on the headings (Manhattan-isotropic off
  them). The one-axis refusals of `covariant_readings` are lifted under the
  key, so a body on a diagonal reads `|p|_2 / E'` per lattice interval.
- **The expectations (series X, [EXPERIMENTS](EXPERIMENTS.md#x-the-directional-drive-2026-09-22)).**
  A body of content 64 at `|p|_1 = 6000` from the centre of an open 41^3
  box clicks on face:+x (DETECTOR) at tick 51 from (40, 20, 20) on the
  axis, 101 from (40, 40, 20) on the plane diagonal and 152 from (40, 40,
  40) on the cube's; the per-axis drive's controls at 36, 50 and 65 from
  (40, 20, 20) with y and z never moved; every `step` line's Node within one
  Link of the line (GAMEBOARD); the reviewer's pins of record 348 (112, 112,
  83 Links against the whole parts 111, 111, 83 within 2 at every n; a
  cancelled transient leaving -0.050 Link and no Link).
- **What it depends on.** The constant `T_h = 110` (the flight table's own
  heading resolution) as the cap's scale; the cap term keyed off under the
  covariant key; nothing else of the six verbs.
- **What it does not give.** Form B's Euclidean-isotropic cap on the body's
  line (the line accumulator of the first build, BLOCKED in record 348: an
  exact form with a line-independent unit does not exist, FORM.md 3.1);
  the rows' triple pace `|p|_2 / E'` under the law alone (two dispersions
  are in the tree, both rung 1: DESIGN.md section 7); any change of the
  default drive or of a registered world.
- **What would refute it.** A click of the plane body from a Node with y
  below 39, or at a tick outside 101 +- 1; a `step` line more than one Link
  off the line of the momentum; an accumulator at or above 3 W; a world
  without the key whose record differs from `main`'s by a byte.
- **Status.** Built on 2026-09-22 and run once (series X): six worlds, 19
  readings inside, 0 outside, nothing moved; the key off by default; making
  it the default is the owner's later decision.

## 29. flow-link-v1: one arrival counts one Euclidean Link of its line, not one Node; the law's two constants of gravity are one, stated so that it can fail

- **Statement (the model owner's decision of 2026-09-22, record 915 of
  docs/LOG_2026-09-20.md, on his go of record 886; the Flow Weight
  Designer's design [docs/designs/flow_weight/DESIGN.md](designs/flow_weight/DESIGN.md)
  with [ALGEBRA.md](designs/flow_weight/ALGEBRA.md); the physics-rule
  reviewer's ADMISSIBLE of record 902).** Under the world key `flow_link`
  (absent by default) the arrival flow every reader sums carries per
  arriving row the flow label **f**_D, the integer vector nearest
  `|p_D| D / S_1` (per component `sign(D_i) x (2 |p_D| |D_i| + S_1) // (2
  S_1)`, one Euclidean division per component at load; `|p_D|` is Q for
  the photon and a massive family's `momentum_magnitude`, each family's
  flow labels from its own labels), in place of the unit label **u**_D
  nearest `|p_D| D / |D|`; the push's shell mean then carries no L1 factor
  (the fan's mean of `S_1 / |D|`, 1.4355 on series K's 290 directions,
  `3 / 2` in the isotropic limit) and the push's Newton constant equals the
  clock's, `q / (4 pi S)` at the pin `n S = d`, to three parts in a
  thousand on series K's fan (the fan's mean of incidence times weight
  1.0003; the crowd's shell mean 22.85 against the continuum's 23.08
  beside the clock's 68.72 against 69.23). The age moment, the wall, the
  flight, the collision, the phase and the momentum a click moves are
  untouched; the key stands alone or beside `optical`. The scope on record
  (the physics-rule reviewer's line on the build): a paid family's rays read
  by a body under `read` still push by their labels per Node (the momentum
  a click moves), so their flow keeps the L1 factor; the change is confined
  to a free family's rays, which the law's gravity pushes (series K, C, the
  atom) all are, and to every row's push by the interval's arrivals.
- **The expectations, before any run (the design's section 4, GAMEBOARD by
  the step algebra; DETECTOR when run).** The ring of starts at b = 6 on
  series K's box (the fan of 290, the mass 2^16, the width 16384, the
  suspension [1, 16384], 40 lamps on the heading at `|sqrt(y^2 + z^2) - 6|
  <= 1 / 2`, the screen of one-Node `wave` detectors reading `age`) under
  `optical: 1` reads the mean radial shift of the arrival Node `0.731 +-
  0.025` Links over 40 starts (`0.974` as built) and `0.128 +- 0.025` at
  `optical: 0` (the count of starts moving one Node, 6 +- 1 of 40);
  `1.625 / 0.845 +- 0.0625` at b = 3 over 16 starts, `0.628 / 0.107 +-
  0.021` at b = 8 over 48; the delays within 1 interval; `C_ring` expected
  `2 c_f x 0.990 x L / sqrt(L^2 + b^2)` = `3.86 / 3.93 / 3.79` at b = 6 /
  3 / 8 with the grain `0.085 / 0.107 / 0.095` (the design's read `3.65 /
  3.82 / 3.92`); the tangential mean 0; `C_nodes` 2.50 at b = 6, gamma 1,
  with the lever-arm factor 0.68 stated before the run. The calibration:
  the registered `optical/mass_g0.json` and `mass_g1.json` under the key
  read `-1.600 / -3.000` pixels by the algebra (`-1.993 / -3.989`
  registered, DETECTOR, never edited).
- **What it depends on.** The direction table's integers D and S_1 alone;
  no root, no float, no run-time division beyond the law's declared ones;
  the same six reads and nothing kept at a Node (the three tests written
  out in the design's section 2, all PASS).
- **What it does not give.** A derivation of Einstein's 4: the ring reads
  the declared `2 c_f` against the clock's constant, both on one ground
  now, the 2 of `c_f` an input of kind 2 (record 817). Newton's rows move
  by their fan's factor under the key (D3's periods `343 / 687` to `384 /
  768` by formula), re-derived by their generator before any run.
- **What would refute it.** A `C_ring` that, after the two stated factors,
  leaves `2 c_f` by more than the grain in either direction; any clock
  reading (the lamp's rate, the redshift ratio) that moves under the key;
  a world without the key whose record differs from `main`'s by a byte.
- **Status.** Built on 2026-09-22 (the world key `flow_link`, the identity
  `flow-link-v1`, `tests/test_flow_link.py`); the ring worlds and their
  pins under `examples/events/flow_link/`, run once the same day: the
  verdict NOT DECIDED, the deciding pin 0.731 +- 0.025 at b = 6, gamma 1
  unread (the gamma 1 rings and b = 3, 8 refused by the pair's working
  bound at d = 16384, the folder's README); the gamma 0 ring at b = 6
  inside its four pins (the mean radial shift 0.128 against 0.128 +- 0.025,
  every arrival Node the map's), its `C_ring` 1.806 OUTSIDE the one-grain
  pin 1.929 +- 0.085 by 0.038, 1.45 grains below as the algebra's 1.46;
  the calibration -1.573 / -3.180 pixels against -1.600 / -3.000; the key
  off by default; admitting it to the law, and the road past the refusal,
  are the owner's later decisions.
