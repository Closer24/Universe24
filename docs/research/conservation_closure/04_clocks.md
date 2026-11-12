# One retained source clock, with explicit detector limits

This audit uses the same eight-channel Bianchi-I law as the native, metric and
covector packages. It adds no oscillator, channel, update rule or decoder
feedback. The new positive result is an exact **integer clock relation** between
the source-driven volume history and the retained proper-time marker. Arithmetic
clicks and the massless scalar are tested independently of that relation.

Source: `validation/conservation_closure/clocks.py`. Reproduction:

```sh
python -m validation.conservation_closure.clocks
```

Fresh evidence: `runs/conservation_closure/clocks.json`.

## A clock derived from the actual source-driven history

The shared native state retains volume histories, dust charge D, the velocity
reference Jref, and a marker T. With the static resolution N, define

\[
J=b_W-a_W+3D,\qquad U=\frac{J}{4N},\qquad
U_{\rm ref}=\frac{J_{\rm ref}}{4N}.
\]

The actual Engine map is

\[
W_+=W+J+3D,\qquad J_+=J+6D,\qquad T_+=T+1,
\]

with D and Jref frozen in their complete histories. Therefore the additional
integer quantity

\[
\boxed{C_{\rm clock}=J-J_{\rm ref}-6DT}
\]

is invariant under every actual update. This is independent of the physical
energy constraint. Both invariants can be checked on the same complete state.

For the declared positive-dust chart, the source clock is

\[
\boxed{\tau_{\rm source}
 =\frac{J-J_{\rm ref}}{6DN}
 =\frac{2(U-U_{\rm ref})}{3D}.}
\]

It advances by exactly 1/N. The formula has no run step, seed trace or proper
marker T as an input. Its reference event is represented by the retained Jref,
not by an external lookup of a precomputed trajectory. It is a passive readout;
the division never feeds the Engine. No additional clock channel is concealed.

The relation to the retained marker is

\[
\tau_{\rm source}-\frac{T}{N}
 =\frac{C_{\rm clock}}{6DN}.
\]

The default preparation sets this constant to zero. A different time origin
changes the constant, not the source-driven elapsed time. One must **check its
invariance**; recomputing a changing offset to excuse a defective marker is not
an accepted repair.

This clock's physical calibration comes from the common metric and source
equations. The shared metric is

\[
ds^2=-d\tau^2+\sum_i a_i(\tau)^2(dx^i)^2.
\]

The comoving dust velocity has components u^mu=(1,0,0,0), while its covector is
u_mu=(-1,0,0,0)=-d_mu tau. The same inverse metric verifies u_mu u^mu=-1 and
u^mu d_mu tau=1. The independently checked Einstein/source dynamics give
dU/dtau=3D/2, so the source-clock expression is elapsed proper time along those
comoving dust worldlines. The conclusion is specific to this chart, including
D>0, and does not extend the formula to a dust-free or spatially varying system.

This is a useful relational clock identity. It does not provide a microscopic
oscillator, an emission event, a transported message, or an autonomous detector
that records reception. Those apparatus degrees of freedom are absent.

## Same-state execution at three resolutions

All three runs use exactly the tensor
`a51595cb6b4facd289fc40334527dc9ad4126c4f3244f70f8d5fcba53585231b`.
Their complete seeds differ because N changes the static integer units; their
physical source and shear initial data agree. The default N=24 complete seed is
`d1fcbb9266b7c9cb06ce10a33e900068ade4f83a01f7507c3f894efff103e1cc`.

| N | Actual updates | Source proper time | Canonical clicks, 27 nodes | Peak bits |
|---:|---:|---:|---:|---:|
| 24 | 3 | 1/8 | 135 | 13 |
| 48 | 6 | 1/8 | 297 | 15 |
| 96 | 12 | 1/8 | 621 | 17 |

Every sample has C_clock=0, and tau_source equals T/N exactly. Complete scalar
oracle comparisons, legal remainder retention, each inverse and full rewind
pass. All three physical endpoints have V=2185/768 and U=67/16. The audit reads
the source clock directly from each actual state before comparing samples.

The canonical decoder emits a record when its quotient is nonzero and the
complete channel triple changed. The constant source/anchor/shear channels emit
none. The volume channel emits once at every node and step; the marker's first
zero-origin quotient is zero, so it emits at subsequent steps. Thus a run of s
positive steps has exactly 27(2s-1) arithmetic records. All records in this law
are class C0 because its divisible coefficients retain the initial remainder.
The independent scalar readout checks the decoder's node, channel, quotient,
class and sign for every record.

The table establishes that uncalibrated click count is not proper time. More
strongly, merely shifting both histories of T by seven leaves the same scalar,
source and metric trajectory, but changes the three-step count from 135 to162.
Here C_clock=-42 remains exactly constant, and the marker/source offset is
7/24 throughout. The initial zero-quotient exception explains the extra records;
no physical clock acceleration occurred.

## Source, marker and carry interventions

Three controls keep arithmetic reversibility separate from physical time:

1. Increment every initial carry modulo six. The complete seed fingerprint
   changes and the changed carries remain retained. All a,b values, physical
   source times and canonical click records agree with the original run. Carry
   bookkeeping has not become a physical-rate mechanism.
2. Prepare the marker with zero slope instead of one while preserving the
   physical source histories. The Engine still reverses exactly, but C_clock
   takes values 0,6,12,18. The common prepared-domain reader rejects the marker.
3. Remove the real dust-to-volume tensor term in a deliberately wrong-law
   control. The marker still advances, while C_clock takes values
   0,-6,-12,-18. That wrong law also reverses exactly; its source-clock relation
   fails. Thus appending a free counter cannot certify source-driven time.

The latter two controls are rejected tests, not alternate accepted candidates.

## The massless scalar is monotone, not a periodic proper clock

For the same actual state, scalar velocity is P/V and the scalar value is
phi_ref+P I, where I is the passive retained-reference integral with dI/dtau=1/V.
For P>0 and increasing V, every interval obeys the strict bound

\[
\frac{P h}{V_+}<\Delta\phi<\frac{P h}{V}.
\]

The code checks the actual scalar readout against these rational bounds at
every sample. Over the default proper interval 1/8,

\[
\frac{192}{2185}<\Delta\phi<\frac{3}{28}<\frac18,
\qquad
\Delta\phi=0.0969446665723357998\ldots.
\]

The same value appears at all three resolutions because this source solution
is sampled exactly. Its gradient norm is -P²/V², not the -1 of a proper-time
covector. This real massless scalar has no implemented periodic phase, and
division by a rest mass would be undefined. It is a monotone relational variable
on this solution, but its value is not universally elapsed proper time.

Indeed its future range is finite. At the default preparation,

\[
\phi(\infty)-\phi_{\rm ref}=\frac23\log7
 =1.2972734327035422034\ldots.
\]

This follows from the exact retained-reference logarithm as U tends to infinity;
it is not a numerical extrapolation of the short run. A monotone scalar can
parametrize a restricted trajectory without being a periodic clock with a tick
record. The covector package separately predicts a moving test body's m/E
proper-time rate from this metric; that passive test body has no retained
worldline or detector allocation.

## A precise obstruction to adding a hidden threshold instruction

A fixed finite number of permitted polynomial/fixed-six Engine steps cannot
produce an exact global sign/threshold bit from an unrestricted integer input,
with all other input registers fixed. This statement is about that bounded-time
arithmetic interface, not a prohibition of all physical clocks.

Proof: restrict one input register to the integer n. Initially every register
is polynomial in n. A finite family of quasipolynomial functions has a common
finite residue partition. On each residue class, polynomial sums and products
remain rational polynomials in the class parameter. To take floor(p(n)/6),
refine the partition by a common denominator of the polynomial coefficients:
the fractional part is constant on each refined class. Subtracting that fixed
fractional part leaves a polynomial. The remainder output is obtained by
subtraction and therefore has the same property. Induction over any fixed
finite number of Engine steps proves that each output is quasipolynomial on a
finite residue partition. This argument allows every retained history/carry
and all finitely many nodes; locality is not needed for the obstruction.

If an output is globally confined to the bit values {0,1}, its polynomial on
each two-sided infinite residue class is bounded, hence constant. A threshold
bit is zero on arbitrarily negative and one on arbitrarily positive inputs of
every residue class. No such constant polynomial exists. This proves the claim.

The audit checks signed floor identities on all six residue classes for a cubic
example and a nonzero fourth finite difference for threshold samples. These
finite witnesses illustrate the proof; they are not an exhaustive program
search. On a declared finite alphabet, interpolation can work: x(x+1) is an
event code 0,0,2 for x=-1,0,1. It gives6 at x=2 and a false positive2 at x=-2,
so it is not a global sign mechanism. This illustrative code is not installed
in the candidate.

The theorem does not exclude bounded input domains, variable-time computations,
unbounded clock counters, passive canonical click decoding, or other material
clock mechanisms. It does prevent assuming that a general threshold or phase
winding counter is a free hidden instruction in a fixed finite macro update.

## Literature and acceptance boundary

[Brown and Kuchar](https://arxiv.org/pdf/gr-qc/9409001), section II A-C,
equations2.2 and2.6-2.10, derive a material dust reference covector and its
proper-time normalization; equations2.15-2.17 give the dust conservation laws.
Those continuum results motivate the separate source, covector and clock
checks here. They do not supply this discrete integer invariant or an
operational detector implementation.

[Rovelli](https://arxiv.org/pdf/gr-qc/0110035), sections II-III, distinguishes
individual readings from predicted relations between readings, including the
two-clock comparison in equation4. Here the proved relation is between retained
source history and a calibrated comoving marker. A transported physical
comparison would additionally require the emission, transport and reception
processes in the same retained law.

| Gate | Result |
|---|---|
| Same-state source-driven comoving dust proper time | Passed |
| Canonical arithmetic protocol and complete rewind | Passed |
| Arbitrary arithmetic click count as proper time | Failed, with origin/refinement controls |
| Massless scalar as unit-rate periodic proper clock | Failed, with exact rational bounds |
| Transported material detector and autonomous reception record | Not tested; not implemented |
| Global threshold in a fixed finite arithmetic macro | Obstructed under the stated input/interface assumptions |

The eight retained channels and 24 integers per node are the complete allocation
for these claims. No detector has been accepted by renaming arithmetic clicks.
