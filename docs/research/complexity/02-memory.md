# Local retained motif memory: declaration and audit

Production baseline: main `7d238e84a2167a4d3fe7bc7942da0cbf97bd29b2`;
research checkout `1e22b18`. This is a new, explicitly optional toy tensor,
not a production change or a Born/Bell/Einstein model.

## Declared before the candidate runs

Fix six gears `mem.A`, `mem.B`, `mem.bit`, `mem.probe`, `mem.receiver`,
`mem.readout`. A,B are binary motif components transported along +x. The
retained bit is initially +1 or -1. A coincidence A=B=1 flips it; no
coincidence leaves it unchanged. This records motif parity, not an integer
count. It is a deliberately narrow definition of a local structural feature,
not algorithmic complexity or novelty in every possible sense.

Let S be +x transport, `(S X)(x)=X(x-e)`, and `T(A,B)=1-2AB`. Define

```text
F(A,B,m) = (SA, SB, T(A,B)m),
F^-1(A,B,m) = (S^-1 A, S^-1 B, T(S^-1 A,S^-1 B)m).
```

On binary A,B, `T^2=1`. Set `a=F^-1(b)` in the complete initial state and
use `u=3(F(b)+F^-1(b))`. This gives the fixed coefficients

```text
u_A = 3[A(x-e)+A(x+e)]       (and the same for B and probe)
u_bit = 6m - 6m A(x)B(x) - 6m A(x+e)B(x+e)
u_receiver = 6 receiver
u_readout = 3[readout(x-e)+readout(x+e)]
            + 3 receiver(x) m(x) probe(x).
```

Receiver markers have `a=b` and are fixed before the run. The readout is an
ordinary retained wave, not an observer callback. Every term has degree at
most three, reads the complete old b snapshot, and uses at most one face
edge. No separate clock, random choice, update-dependent coefficient or
forced reset is introduced. Nonzero remainder arrays are retained exactly.

Predeclared runs use L=3 and L=5, horizon 80, and a 128-bit limit checked
only after a complete Engine update. All stopped final states must rewind
through their actual completed horizons. Source/tensor/seed/final hashes and
complete seeds/finals will be exported; no run will be replaced to improve
its structural score.

Cases: quiet A=B=0; constant A=B=1; one coincident pulse; separated pulses
with the same lane populations; seeded random binary lanes (seed 1729);
a shuffled B lane preserving its population (seed 1730); a bit/probe scaling
control by two; a global scaling-by-two stress control, explicitly outside
the binary-signal proof. The receiver is at `(L//2,L//2,L//2)`. The probe is
placed so that, on L=5, it reaches that site only after a coincident motif
has passed and the local current and previous A/B values are quiet.

Two matched interventions are also declared: remove memory from the readout
coupling while retaining the learned bit, and compare equal complete signals
with opposite initial bit at just one receiver. Compare future local messages
and their complete-state cones. Neither intervention changes a running state.

Expected limitation, stated before results: on a finite periodic cube the
binary A/B/bit subsystem returns after 2L updates (or a divisor), because
every stored bit encounters each transported motif twice. The local bit is
durable between motifs but a second identical encounter cancels its parity.
The whole reversible state retains information; this finite feature memory
does not provide indefinitely increasing complexity or an irreversible
history archive. The purpose is to establish a concrete, bounded causal
memory primitive that could be tested inside a larger feedback construction.

## Results

The 16 grid cases, four fixed learning/readout ablations, and two matched-bit
interventions completed **22 runs**. All completed states rewind exactly.
The global-scale control at L=3 stops after full update 60 at 129 bits; all
other runs reach update 80. The L=5 global-scale case reaches 121 bits.
These two cases are outside the binary-signal invariant, are retained in the
report, and are not promoted to memory successes.

### Restricted-domain proof and observed memory behavior

For every retained remainder `0<=r<6`, if `u=3C` then
`divmod(2u+r,6)=(C,r)`. On the declared binary sector `F` and `F^-1` above
are mutual inverses. Therefore on `a=F^-1(b)` the actual Engine gives
`b_next=F(b)` and `a_next=b`, preserving the preparation relation. The bit
has constant magnitude; only its sign changes. All forward checks compare
the actual second-order Engine with the stated first-order map, including
nonzero remainders. All monomials pass strict single-edge support.

| L5 preparation | Initial A/B populations | Initial coincidences | Distinct bit-sign fields in 80 updates | First memory-subsystem return |
| --- | --- | --- | --- | --- |
| Quiet | 0 / 0 | 0 | 1 | 1 |
| Constant | 125 / 125 | 125 | 2 | 2 |
| Coincident pulse | 1 / 1 | 1 | 10 | 10 |
| Separated pulses | 1 / 1 | 0 | 1 | 5 |
| Seeded random | 56 / 61 | 32 | 10 | 10 |
| Shuffled B | 56 / 61 | 23 | 10 | 10 |

The bit stays unchanged whenever the local motif `A*B` vanishes. A passing
coincidence leaves a spatial sign trail; a later identical encounter flips
the bit back. Coincident and separated preparations have equal signal mass
but different retained features. The shuffle preserves both lane populations
while changing their local correlation and the resulting memory pattern.
This transfers prepared source structure into bounded retained features;
it is not a demonstration of new information or unbounded organization.

The constant case alternates two homogeneous signs and has no domain walls.
The coincident L5 pulse visits ten sign fields, then repeats. Its maximum
number of sign domain walls is 20; the seeded random/shuffled controls reach
186/168, respectively. More pattern diversity in the random control is not
called more useful organization. The complete previous `a` slice is included
in every saved seed; the apparent initial simplicity of current `b` is not
used to hide structure already present in that preparation.

### A retained motif changes later messages

Two independently initialized histories give an operational test. One has
coincident A/B pulses, the other separated pulses. At old snapshot four on
L=5, the receiver's complete local A, B, probe, receiver-marker and readout
triples agree. The retained memory triples differ. At the next actual Engine
step their readout b values are **-1 and +1**. With the bit removed only from
the fixed readout coupling, both histories produce identical complete readout
arrays throughout all 80 updates. A fixed no-learning ablation separately
retains the unmodified bit and removes the learned trail.

A stronger matched intervention begins with globally identical signals and
probe, changing just one retained bit and its consistent previous slice.
The initial complete-state difference has support at the receiver only.
The receiver emits opposite messages at update five; its neighbor receives
opposite readout values at update six. All complete-state differences remain
inside the cone of the initial one-site intervention over all 80 updates.
Neither matched experiment changes a running state or invokes an observer.

This establishes causal use of retained history in **future local messages**.
The original A/B and probe lanes remain independent of the readout: it is a
one-way message primitive, not yet a feedback-driven reassembly mechanism.
Adding a one-way consumer of `mem.bit` preserves this memory-subsystem proof.
Changing the A/B transport, driving it with arbitrary alarms, or feeding
readout back into it requires deriving the new F and its inverse again.

### Scaling, recurrence and limits

Scaling the bit and probe amplitudes by two leaves all normalized bit-sign
fields identical and multiplies the readout amplitudes by four. That larger
readout is not additional structure. Scaling every signal amplitude by two
breaks the binary identity `T^2=1`; the observed large counters and resource
stop are an explicit failed extension of the proof domain.

All transitions in these runs are **C0**, since every input coefficient is a
multiple of three and all remainders remain fixed. Bounded retained motifs
and causally effective memory therefore do not require a C2 event. This does
not establish any relation between either class and quantum measurement.

The A/B/bit subsystem is periodic with period dividing 2L. No entire six-gear
state returns to its initial state during these 80-update runs: the repeatedly
driven readout can accumulate wave amplitude. In particular, the quiet
memory controls reach 8-9-bit counters in the readout while their bit pattern
never changes. Only the **memory subsystem** has a boundedness proof; the
readout's amplitude growth is explicitly excluded from a complexity claim.

This closes one narrow gate: a retained local structural feature can change
future messages under the fixed-six law, with exact reversibility. It does
not close the cosmology protocol: no four growing reference-board reassembly
cycles, structural-stagnation detector, complexity objective, Born sampler,
or physical clock law follows from this construction.

## Reproduction and handoff

### Secondary interface check declared after the primary grid

The rotor handoff requires a retained 0/1 bit, whereas the primary candidate
stores a signed bit. Do not inject `(1-m)/2` from an observer. A separate
fixed tensor can retain `n=(1-m)/2` directly with

```text
u_n = 6n +3AB +3A(x+e)B(x+e)
          -6nAB -6nA(x+e)B(x+e).
u_readout = 3[readout(x-e)+readout(x+e)]
            +3receiver*probe -6receiver*probe*n.
```

On the Boolean preparation its local map is `n_next=n+AB-2nAB`; the inverse
uses the shifted A/B values. No division appears in evolution. The initial
state may be encoded from the already specified signed state before running.
The declared secondary check compares coincident/separated cases on L3/L5
for 80 updates: both memory histories must satisfy `m=1-2n`, every other
complete triple must match the signed construction, and both must rewind.
This is an exact representation check, not a new growth search or a silent
extension to arbitrary sensor values. Its outcomes are reported separately.

All four secondary cases passed 80 updates and complete rewind. Both memory
histories satisfy the affine encoding exactly, and every other full triple
matches the signed construction. `tensor(boolean_memory=True)` together with
`prepare(..., boolean_memory=True)` therefore supplies a directly retained
0/1 `mem.bit` for a possible Boolean-collision interface. This is a different
encoding of the same finite parity memory, not extra capacity or novelty.

```bash
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 \
  python -m experiments.complexity.structural_memory \
  --out runs/complexity-research/02-memory
```

Each case directory contains the actual fixed tensor, compressed complete
initial and final `(a,b,r)` states, and a per-step report. The aggregate report
retains all cases, stop reasons, source hashes and matched-control results.
All 22 full rewinds, domain-map checks, local interventions and difference
cones passed; the source compiles. No production files or core tests were
changed, and the full suite was not duplicated in this investigation.

The minimal public interface is `tensor(learning=True, memory_readout=True,
boolean_memory=False)` and `prepare(law, side, case, learning=True,
bit_flip=False, boolean_memory=False)` in
`experiments/complexity/structural_memory.py`. The handoff gear is `mem.bit`;
its full triple, not only its current sign, belongs to the retained state.

Next gates: (1) couple this proven bit to a fixed local scatterer and compare
whole reference-board reassembly against the disconnected control; (2) add
capacity for distinct motifs with an explicit finite-capacity and overwrite
law; (3) distinguish recurring familiarity from one-step equality before
calling an alarm a structural-stagnation sensor; (4) preserve the primitive's
domain/inverse or prove a new invariant when combining it with feedback.
