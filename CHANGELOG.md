# Changelog

All notable changes to Universe24, the reference implementation of Reality
Theory (Universe24). Versions are tags on `main`; each is archived on Zenodo.

## 0.3.1 - 2026-09-15

### Redshift from delay growth (second manuscript)

- `redshift_sweep.py`: a train of twelve rays crosses closed rows of 16 to 96
  Nodes under `ray_delay` to an absorbing eye that counts its own cycles;
  `1 + z = k_o / k_e` on the eye's clock, durations stretch by the same
  ratio, `z` from 0.07 to 2.81 with the distance, the slope scaling with the
  emission; the wave's frequency redshifts with the rate under the default
  phase rule. Moving bodies stall the clocks of the Nodes they wait at and are
  not used ([report](examples/relativity-probes/README.md#redshift-sweep-the-law-its-statistics-and-the-supernova-test)).
- `redshift_hubble.py`: the law's shapes against the Pantheon+ Hubble-flow
  sample; the model's own load histories are disfavoured, a fitted power law
  is not; the Tolman exponent is the discriminating test. Manuscript in
  `paper/redshift/` ([hypotheses](docs/HYPOTHESES.md)).


A review pass on the paper's Bell narrative. No engine change; the Bell probe
gains two modes and the framework's claims are narrowed to what is measured.

### Bell's test

- The bonded value carries its statistics: `--sweep` re-measures the bonded
  CHSH value with fresh pairs for every setting pair, 64 to 4096 pairs per
  correlation on the lattice with four replicas each and the registry alone
  to a million pairs, with binomial standard errors; every lattice outcome
  equals the registry's answer from the same seed, and `S` converges to the
  table expectation `724/256 = 2.828125`. The first run's 2.889 was sampling
  spread on correlated samples ([report](examples/bell-chsh/README.md#standard-errors-and-convergence-of-the-bonded-value)).
- Which assumption of Bell's theorem each candidate breaks is measured at
  fixed hidden variable by `--causal`: the lottery and the threshold are
  parameter independent; the bonded pair is deterministic and
  measurement-independent and breaks parameter independence (Bob's answer
  moves with Alice's setting for 0.72 of the hidden variables at
  `b'`); the quantum owner breaks outcome independence
  ([report](examples/bell-chsh/README.md#which-assumption-of-bells-theorem-each-candidate-breaks),
  [coupling](docs/QUANTUM_CLASSICAL_COUPLING.md)).
- The door of postulate 22 is measured half by half: `--source agreement`
  keeps the coin even and fixes the agreement half, giving S = 4 (the
  Popescu-Rohrlich box) with even marginals and no signal; no-signalling
  bounds the coin, not the correlation ([report](examples/bell-chsh/README.md#the-door-of-postulate-22-a-number-source-outside-the-world)).
- Postulates 4 and 22 name the broken assumption: the registry is a nonlocal
  resource in Bell's sense, its unmoved plus rates are no-signalling and not
  locality, and how a number is read (one end, both ends, or correlated with
  the settings) decides which assumption is at stake ([POSTULATES](POSTULATES.md)).

### Paper

- The manuscript is reframed as a finite-integer causal-lattice testbed: the
  configured laws are named as inputs, the Bell section carries errors and the
  causal analysis, "what is new" and "what is not claimed" are explicit, and
  the bonded pair is stated not to be a local explanation of the Bell value
  ([paper](paper/main.tex)).

## 0.3.0 - 2026-09-14

153 commits since 0.2.0. Zenodo DOI 10.5281/zenodo.22749342. Every number
below is recorded with its source fingerprint in [validation](docs/VALIDATION.md).

### Framework

- The framework is named Reality Theory (Universe24); the simulator stays
  Universe24 ([README](README.md)).
- Postulate 4 is split: energy, momentum, matter and every controllable
  message move at most one Node per step; the joint outcome of a bonded pair is
  the one declared exception, answered by a bounded registry that carries
  nothing physical ([POSTULATES](POSTULATES.md)).
- Postulate 22: every uncertain interaction consumes exactly one bounded
  integer; a bonded pair draws one number, whichever end asks first; the
  sequence is the only door for outside information and is bound by
  no-signalling.
- A [hypotheses page](docs/HYPOTHESES.md) keeps the questions the framework
  raises apart from measured results.

### Quantum and classical coupling (causal source candidate)

- Two-arm interference on the canonical runner: exact capture weights, a
  balanced Hadamard splitter, which-path decoherence, causal termination
  ([report](examples/quantum/causal_interference.md)).
- Opt-in null notices restore the exact conditional Born weights after Link
  transit; crossing nulls are corrected locally by the later Node
  ([crossing nulls](examples/quantum/crossing_nulls.md)).
- Opt-in field-dependent phase: an external classical field on one arm shifts
  the fringe by an exact configured phase per field unit.
- Opt-in funded emission: the wave pays for its own field from its conserved
  stock; totals constant; the retarded emission after a capture is the measured
  residual.
- Emission-scale sweep: the integer field follows `amount x |psi|^2` within one
  unit per tick at every scale.
- Two-wing Bell CHSH on the finite quantum owner: 14/5 exact, no-signalling
  marginals, dephased control 6/5 ([report](examples/quantum/bell_chsh.md)).

### Straight and phased rays (Kerengonen candidate)

- Kerengonen phased rays with a fixed-point cosine table: double slit, Huygens
  slits, single-quantum lottery, de Broglie advance from momentum, mirror
  standing waves, matter-wave dissolution, Euclidean pace, claim and gather,
  bonded pairs.
- Bell's test on the ray with five captures on one scale: share 1.40 exact,
  lottery 1.48 and 1.38, threshold 2.00 exactly, bonded 2.89 against the
  quantum 2.83, plain field 2 ([phased-ray Bell](examples/kerengonen-bell/README.md),
  [ray Bell probe](examples/bell-chsh/README.md)).
- An outside number source for bonded pairs: uniform is invisible, biased is
  a measured signal.
- Signed-quanta gravity with a closed ledger, gathered gravity (no dark-matter
  substitute from focusing), isotropy probe, relativity probes (lensing,
  redshift without recession, flat curves from a compressed closed dimension,
  gravitational phase in an interferometer, replay).

### Engine

- Local Focus scheduling (opt-in), ray ownership guards, carried allocation
  phases, ray delay and ray phase per tick, bounded prepared tables, 24-slot
  envelope output banks.

### Repository

- MIT license, `CITATION.cff`, Zenodo DOI 10.5281/zenodo.22738746 (0.2.0);
  named-particle gallery; documentation cleaned of process noise.

## 0.2.0 - 2026-09-14

First archived version: the integer lattice simulator with configured
disturbances, spatial fields, the finite quantum owner and the causal source
candidate. Zenodo DOI 10.5281/zenodo.22738746.
