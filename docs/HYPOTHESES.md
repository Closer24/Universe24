# Hypotheses under test

This page keeps the questions the model raises apart from the results it has
measured. Everything on it is a hypothesis: something the framework suggests,
stated so that a run can confirm or refute it, or stated as outside the model's
reach. Nothing here is a claim of the [coupling summary](QUANTUM_CLASSICAL_COUPLING.md)
or of the [validation log](VALIDATION.md). A hypothesis moves off this page
only with a measured result and a fingerprint.

## 1. The lottery is the only door for outside information

[Postulate 22](../POSTULATES.md#22-the-lottery-is-the-reality-one-integer-per-interaction)
makes every uncertain outcome the value of one bounded integer. It follows,
without a further assumption, that the sequence of those integers is the only
place where information not already in the world's state can enter the world:
everything else is fixed by the rules and the initial state. The model does
not fix where the sequence comes from. A configured seed, a file, or a source
outside the world give the same physics as long as the numbers are used the
same way; how they are read is fixed, and for a bonded pair it is a reading by
both ends, the parameter dependence that
[postulate 22](../POSTULATES.md#22-the-lottery-is-the-reality-one-integer-per-interaction)
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
[Bell probe](../examples/bell-chsh/README.md) with `--source uniform` gives
S = 2.7911 and rate shifts below 0.1, and with `--source biased` keeps
S = 2.7792 while Bob's plus rate moves by 0.6866 with Alice's
setting. The derivation holds in the model; whether any real source is outside
the world in this sense stays a hypothesis.

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
closed-universe probes ([expansion and redshift](../examples/relativity-probes/README.md))
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

The framework is one setting in which mechanics, radiation, interference,
quantum contacts and Bell's test run on the same lattice. It is not yet one
theory: the mixers, the instruments, the phase advance per link, the `|p| / D`
rule, the cosine table and the singlet law in the bond registry are configured
data, measured to hold, not derived. The program is to replace each configured
law by a rule of the lattice and show by a run that the measured tables do not
change. Each replacement is a hypothesis with its own experiment; the
[what would make this a physics result](QUANTUM_CLASSICAL_COUPLING.md#what-would-make-this-a-physics-result)
list is its first four entries.

## 6. Dark matter is a closed dimension, not extra mass

The [relativity probes](../examples/relativity-probes/README.md) measure the
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
The [gathered gravity probe](../examples/gathered-gravity/README.md) closes
the other route: gathering a gravity train focuses quanta, not a force law.

## 7. Redshift without recession, and no dark energy

The [closed-row sweep](../examples/relativity-probes/README.md#redshift-sweep-the-law-its-statistics-and-the-supernova-test)
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

## 8. Everything that moves is a ray; records only hold

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
