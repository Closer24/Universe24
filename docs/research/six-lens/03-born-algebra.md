# Algebra, amplitudes and Born probabilities

Baseline: GitHub main `7d238e84a2167a4d3fe7bc7942da0cbf97bd29b2`, including
Frame48 and the merged Bell/Born audit. All active source and text blobs were
verified against the remote tree by the coordinator. Local commit `467b685`
is a reconstructed snapshot, not GitHub ancestry. This audit changes no
production law, preparation API, classifier or default runtime.

The algebra supplies exact complex structures, interference weights and a
reversible transport sector. It does not yet connect these to a physical
quantum state, its measurement operators and Born-distributed exclusive
detector records. The nearest obstruction is explicit: the present detector
is a saturating arithmetic threshold, not a normalized probability reader.

## Reproduction and new local evidence

```sh
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 python -m experiments.research.six_lens_born --out runs/six-lens/03-born-algebra
python -m compileall -q experiments/research/six_lens_born.py
```

The [runner](../../../experiments/research/six_lens_born.py) writes
`runs/six-lens/03-born-algebra/report.json`, including source hashes.
It reruns the current 144-preparation transported-router calibration and
adds 396 preparations (11 fixed amplitude pairs, all 36 residue pairs).
All 540 runs have no detector event before arrival and rewind the complete
state exactly. The amplitude packet reaches the detector at update two;
the fixed old-snapshot law reads it at update three. All 17 existing
`layers.matter.check_algebra()` checks pass.

### The actual detector law in the tested preparation

At the measurement update the detector has `a=b=0`, input intensity `I>=0`,
and initial remainder `r` uniformly enumerated over 0,...,5. Independent
scalar arithmetic gives

```text
ell = floor((2 I + r)/6)
official click iff ell != 0 and the retained triple changes
P(click | I, uniform r, this preparation) = min(1,I/3).
```

For this preparation nonzero ell already ensures a changed triple. The
formula matches every tested Engine event. Uniform residue enumeration is
a declared calibration ensemble; its physical preparation has not been
derived. It is not a random draw inserted into the Engine.

| Input arms | Output intensities | Normalized Born reference | Actual counts / 36 trials | Double clicks |
| --- | --- | --- | --- | --- |
| 2, 1 | 9, 1 | 9/10, 1/10 | 36, 12 | 12 |
| 4, 2 | 36, 4 | 9/10, 1/10 | 36, 36 | 36 |
| 6, 3 | 81, 9 | 9/10, 1/10 | 36, 36 | 36 |
| 10, 5 | 225, 25 | 9/10, 1/10 | 36, 36 | 36 |

The comparison is conditional: if the registers encode unnormalized
single-particle probability amplitudes, common scaling represents the same
quantum ray and requires unchanged outcome probabilities. If they encode
classical field strength or occupation, scaling can legitimately change the
physical preparation and detector response. The experiment diagnoses an
absent physical encoding/calibration; scaling dependence alone is not a
falsification of every quantum interpretation of the model. Normalizing
binary event counts after the fact also hides the double-click problem.
Even the unsaturated baseline `I=(2,2)` yields 24 clicks per arm in 36
emissions, including 16 double-click and 4 silent emissions. Equal normalized
click shares therefore do not establish an exclusive one-quantum outcome.

### Fixed-strength phase scan

Both arms below have squared norm 25. Relative phase changes while their
separate strengths stay fixed. The detector still has the same preparation.

| Arms | Output intensities | Born reference | Actual counts / 36 |
| --- | --- | --- | --- |
| 5, 5 | 100, 0 | 1, 0 | 36, 0 |
| 5, 3+4i | 80, 20 | 4/5, 1/5 | 36, 36 |
| 5, 5i | 50, 50 | 1/2, 1/2 | 36, 36 |
| 5, -3+4i | 20, 80 | 1/5, 4/5 | 36, 36 |
| 5, -5 | 0, 100 | 0, 1 | 0, 36 |

The cross term works, but saturation flattens the three interior binary
readouts. This can describe a saturated classical detector; it does not
establish the ideal single-quantum detector sought here. Global multiplication
by i preserves intensities and counts exactly. A common rational phase
rotation maps (10,5) to (6+8i,3+4i) with the same intensities and counts.
Those exact controls do not establish arbitrary continuous U(1) covariance
of every production sector.

## What algebra does and does not force

For a single complex coordinate z=x+iy, suppose a local weight is a homogeneous
real quadratic form `q=A*x*x+2*B*x*y+C*y*y`. Invariance under z->i*z gives
`A=C` and `B=0`. Positivity then gives `q=c*|z|^2`, c>0. This is an elementary
conditional identity: the quadratic, phase-invariant assumptions motivate
the squared norm. Phase invariance alone would also permit functions such
as `|z|^4`, and says nothing about a probability ensemble or sampling.

For indistinguishable paths, a linear combination is formed before taking
the norm. The current `_square_terms` implementation includes the resulting
cross terms. Feynman's amplitude rules distinguish addition of alternative
amplitudes from multiplication along successive stages; probabilities follow
the absolute square [1]. Counting clocks or local structures without signed
phase contributions does not reproduce destructive interference.

There is also a useful encoding constraint. A finite matrix with Gaussian
integer entries and `U†U=I` in the ordinary coordinate norm can only be a
permutation with unit phases ±1,±i: every column has nonnegative integer
squared entries summing to one, and orthogonality forces distinct occupied
rows. Nontrivial beam splitting therefore needs a decoded normalization,
a different encoding or a suitable limit; it cannot be obtained by an
arbitrary norm-preserving matrix of those raw integer amplitudes. This is
not a prohibition on quantum encodings in a larger integer engine.

For example, the integer Hadamard matrix has `H†H=2I`. The separate reference
can cancel its common scale when it normalizes probabilities. The current
physical detector responds to that absolute scale instead. Deriving the
meaning of that scale is part of the missing interface.

## Reversibility, Hilbert structure and tensor products

The prepared directed fibre is an exact shift and preserves the sum of the
squared amplitude components. All new detector runs verify that norm at each
step. With the same fibre law but off that preparation, a localized `b=1`
and `a=0` gives:

| Update | sum a² | sum b² | sum (a²+b²) |
| --- | --- | --- | --- |
| 0 | 0 | 1 | 1 |
| 1 | 1 | 2 | 3 |
| 2 | 2 | 3 | 5 |
| 3 | 3 | 4 | 7 |

Rewind is exact. This refutes universal preservation of these particular
register norms, not every possible inner product or quantum embedding.
Indeed every bijective classical update formally induces a unitary
permutation on a Hilbert basis labelled by complete configurations. That
construction alone supplies neither a physical amplitude decoder, a Born
ensemble, quantum observables nor a preparation of entangled states.

The existing `J²=-I`, commutant and Kramers identities are useful algebraic
structure. They do not identify the detector readout with a quantum POVM or
prove that the full nonlinear integer update is a physical unitary evolution.
`core.tensor.Tensor` is the fixed polynomial law data structure; its name
does not supply the quantum composition rule `H_A tensor H_B`.

The external singlet benchmark explicitly supplies joint amplitudes and
uses both analyzer settings in its joint sampler. It demonstrates a
well-defined reference calculation, not an Engine derivation. Quantum rays,
measurement operators, unitary evolution and composite systems are distinct
parts of the formalism [2]. A general Born-rule reconstruction, such as the
effects-based theorem of Busch, assumes a specified quantum effect space
and additive probability assignments [3]; those assumptions must themselves
be justified here rather than inferred from the existence of squares.

## Four decisive next gates

1. **Declare the physical encoding.** Specify which retained variables represent
   a field strength, particle number, an unnormalized ray, apparatus state and
   environment. State a normalized inner product and observables. If scaling
   is only representational, a simultaneous rescaling must leave physical
   predictions unchanged; if scaling is physical, predict its energy and count
   effect. Freeze this interpretation before fitting statistics.
2. **Prove and test coherent composition.** Find an invariant encoded sector
   with norm-preserving evolution and basis changes; then test multi-stage
   interference, arbitrary phase approximations and the composition of two
   systems. A signed-permutation identity or an exact inverse alone is
   insufficient. Keep the existing integer recurrence unchanged unless a new
   model is explicitly declared.
3. **Build a calibrated measurement instrument.** With a declared
   single-excitation source and apparatus ensemble, require exclusive outcomes,
   all-emission accounting, the full phase fringe and Born ratios across
   independently chosen preparations. Include record retention, conditional
   subsequent measurements and which-path/erasure controls. External CDF
   sampling is an honest benchmark, not a solution inside Rule3.
4. **Give complexity a falsifiable role.** Define a structural statistic and
   its coupling, distinguishing it from raw magnitude or bit length. If it
   weights branches, derive its phase-sensitive weights and measurement
   normalization, then test alternatives without postselection. A common
   oscillator can organize phases; an asserted preference for complexity
   supplies no probability law by itself.

## Sources and scope

[1] R. Feynman, *Probability Amplitudes*, sections 3-1 onward,
https://www.feynmanlectures.caltech.edu/III_03.html.

[2] J. Preskill, *Foundations I: States and Ensembles*, section 2.1,
https://www.preskill.caltech.edu/ph219/chap2_15.pdf; *Measurement and Evolution*,
https://www.preskill.caltech.edu/ph219/chap3_15.pdf.

[3] P. Busch, *Quantum states and generalized observables: a simple proof of
Gleason's theorem*, https://arxiv.org/abs/quant-ph/9909073.

The positive-quadratic identity, Gaussian-integer unitary restriction and
configuration-permutation observation above are elementary mathematical
arguments, not claims that the complete physical model is ruled out. The
tables are current local Engine evidence. The proposed quantum encoding,
measurement instrument and complexity coupling remain research hypotheses.
