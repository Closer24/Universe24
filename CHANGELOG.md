# Changelog

All notable changes to Universe24, the reference implementation of Reality
Theory (Universe24). Versions are tags on `main`; each is archived on Zenodo.

## 0.3.0 - 2026-09-14

153 commits since 0.2.0. Every number below is recorded with its source
fingerprint in [validation](docs/VALIDATION.md).

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
