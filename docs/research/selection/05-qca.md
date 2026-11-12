# Quantum automata: an exact state contract for the local selector

This lane supplies a constructive quantum comparator for the **same reversible
collision** used by the native selector. It does not add an alternative
runtime, a hidden wavefunction to an Engine seed, or a probability sampler.
Its result is an exact norm-preserving, entangling Hilbert-space lift of that
collision **conditional on an explicitly added coherent preparation**. The
classical integer Engine does not yet derive that preparation or its outcome
measure.

## Primary-paper findings and their limits here

[Schumacher and Werner, *Reversible Quantum Cellular Automata* (2004),
Sections II and III B, Lemma 4](https://arxiv.org/pdf/quant-ph/0405174), define
local quantum observable algebras and construct quantum lifts of locally
invertible classical automata. On a finite periodic lattice the classical
configuration permutation gives a unitary basis permutation. Their locality
argument uses both the forward and inverse neighborhoods; its bound can be
larger than the forward classical neighborhood. Thus classical dependency
tests alone do not establish the same quantum-observable causal radius.
This applies as a useful construction and warning, not as a derivation of
Universe24's preparation, amplitudes or detection probabilities.

[Arrighi, Nesme and Werner, *Unitarity plus causality implies localizability*
(2009 version), Definitions 3–5 and Theorem 1](https://arxiv.org/pdf/0711.3975),
start with configuration superpositions, tensor-product subsystems, unitary
evolution and quantum causality expressed through reduced states. They derive
a local representation, with local ancillary encoding/decoding in the
construction. Those assumptions and ancillary resources are not furnished
merely by a reversible integer polynomial. In particular, the theorem does
not provide the distribution or instrument that selects our detector records;
an imported auxiliary register would still count toward the 48-channel cap.

These are the imported results. The finite calculations and integral-norm
argument below are independently derived checks for this repository.

## Three different meanings of “state”

| Object | Meaning | What the present code supplies |
| --- | --- | --- |
| Complete Rule3 state | One exact assignment of every retained `(a,b,r)` | Native Engine dynamics and replay |
| Classical ensemble | A distribution over such assignments | Must be specified by preparation; reversibility does not select it |
| Quantum state | Complex amplitudes or a density operator over a tensor-product configuration basis | An explicitly assumed small validation reference here; no Engine encoding or measure derivation |

Individual real field components are not automatically amplitudes of complete
configuration alternatives. Likewise, interpreting a Boolean polynomial on
real arguments is not the quantum lift of its truth table. For example,
`xor(x,y)=x+y-2xy` is reversible as part of a suitable Boolean gate, but
`xor(1,1)=0` differs from `xor(1,0)+xor(0,1)=2`: it is not a linear amplitude
operator. The Hilbert lift instead permutes **basis indices** and acts linearly
on the externally supplied configuration amplitudes.

## Constructive lift of the retained-memory collision

Use the exact `SORT_GATE` exported by `validation.selection.complexity`, in
the order `(m,x,y)`. Set

\[
s=y(1-x),\qquad m'=m\mathbin{\mathrm{XOR}}s,
\]

and swap x and y when `m'=1`. Its complete truth table is a permutation of
eight configurations. Keeping m is essential: a ready-memory sorting action
can retain which input order occurred. Erasing that provenance would lose the
inverse. The native-clock lane embeds this finite collision and face transport
in the unchanged Rule3; its actual Engine evidence is separate from this
amplitude comparator.

Define `U|mxy> = |SORT_GATE(m,x,y)>`. The audit constructs the full 8×8
permutation matrix and checks `U^T U=1`, every basis inverse, and `U^3=1` for
the collision without transport. Basis inputs remain basis inputs: U does not
create quantum superposition from an ontic Engine assignment.

For a deliberately supplied coherent **product** input,

\[
|0\rangle_m\otimes(3|0\rangle_x+4|1\rangle_x)/5\otimes|1\rangle_y,
\]

the same permutation gives

\[
U|\psi\rangle=(3|110\rangle+4|011\rangle)/5.
\]

Its norm is exactly one. Tracing the carrier bits gives the provenance state

\[
\rho_m=\operatorname{diag}(16/25,9/25),\qquad
\operatorname{tr}(\rho_m^2)=337/625<1.
\]

Thus the pure reference state is entangled between carrier and retained
provenance. The observable connecting `|011>` and `|110>` has expectation
`24/25`, while a classical diagonal mixture with the same diagonal weights
has expectation zero. This distinguishes retained quantum coherence from
merely assigning classical probabilities to two configurations.

The input superposition, tensor-product Hilbert state and off-diagonal
observable were **declared by the reference**. No Engine trial was sampled,
and the squared amplitudes above are not reported detector frequencies.
The result makes a possible coherent information-preserving choice mechanism
mathematically explicit; it does not close the Born or physical-instrument gate.

## Exact mixing and an integer-coordinate obstruction

Let a finite matrix A have integer entries and preserve the ordinary
orthonormal amplitude norm for every input. Then `A^T A=1`. Each column has
integer squared entries summing to one, so exactly one entry is ±1; column
orthogonality forces distinct occupied rows. A is a signed permutation.
For Gaussian-integer entries the allowed nonzero values are ±1 and ±i.

The code enumerates all 81 real 2×2 candidates with entries in `{-1,0,1}`
and finds exactly 8; it enumerates 6,561 Gaussian candidates and finds exactly
32. The sum-of-squares proof covers all integer magnitudes and dimensions.
This is specifically an obstruction to **linear mixing in ordinary integral
orthonormal amplitude coordinates**. It does not exclude the native clock's
different positive quadratic form, a constrained representation, a rational
encoding, or emergent quantum behavior. A different norm/encoding needs its
own composition, locality and measurement proof.

A constructive rational mixing comparator is

\[
C=\frac15\begin{pmatrix}3&4\\-4&3\end{pmatrix},\qquad C^T C=1.
\]

It preserves norms and inverts exactly in 169 signed preparation controls.
From `(1,0)`, C gives `(3/5,-4/5)` and C^T recombines to `(1,0)`.
Flipping the second phase before recombination instead gives
`(-7/25,24/25)`. Its squared components are `49/625` and `576/625`.
Keeping only the integer numerator matrix would multiply the squared norm by
25. A scale cannot simply be omitted or declared to be already retained.
This rational reference never supplies an Engine input and adds no claimed
physical channel capacity.

## Quantum locality is an additional test

The audit also computes exact Heisenberg conjugations for a CNOT on one face.
The classical control bit stays unchanged, but quantum observables transform
as `X_control -> X_control X_target` and
`Z_target -> Z_control Z_target`. Both remain supported on that face.
This illustrates why a statement about classical source values does not
describe every phase-sensitive quantum observable. It is a finite edge check,
not a proof of quantum causality for the full Rule3 polynomial or the full
streamed selector.

## Required next handoff

1. Keep the proven native collision, retained provenance and complete inverse.
   Test the physically coupled model's independent structural feedback gates.
2. Specify whether any proposed amplitude is a local physical field, a
   one-particle amplitude, or an amplitude of a complete many-body configuration.
   Give the exact preparation and tensor-product composition map.
3. If a quantum lift is claimed, prove its linearity, inner product and local
   observable support with the actual encoding and all retained capacity.
4. Supply a physical apparatus interaction and instrument. Declare a
   preparation measure, retain no/double outcomes, and derive or falsify the
   conditional outcome frequencies; the reference here samples nothing.
5. Test structural preference before and after the recorded outcome with the
   same causal/disconnected and recurrent-burst controls. Quantum unitarity
   and classical reversibility alone do not imply increasing complexity.

Run the exact reference after the native selector module is present:

```bash
python -m validation.selection.qca --out runs/selection/qca
```

`qca.json` stores the literal truth table, exact rational states, norm and
entanglement checks, assumptions, failed/missing physical gates and source
hashes. No physical default, additional runtime, Born sampler or full QCA
derivation is introduced.
