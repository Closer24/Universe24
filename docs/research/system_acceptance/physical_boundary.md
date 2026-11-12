# Physical acceptance boundary

Reviewed source: `228f581d02971435c0cd70548ff56267378ffc31`.
Native tensor fingerprint:
`403a33d61251b07266a24d0944b51b6b2b75844975995e9fb6a44b8e277425bc`.

This source supplies an exact, sourced, spatially flat homogeneous expanding
FLRW sector with a massless scalar and positive dust. Its complete native
history preserves the Einstein constraint. That is a physical result within
the declared sector, beyond reversible arithmetic alone. It does not supply
general spatial Einstein dynamics or a quantum theory.

## What closes exactly

Use volume `V>0`, volume velocity `U>0`, conserved dust `D>0` and nonzero
scalar charge `P`. In units of the source, with proper-time coordinate `tau`,

\[
\dot V=U,\qquad \dot U=\tfrac32D,\qquad
I=U^2-3DV-\tfrac32P^2=0.
\]

The exact time-h map is

\[
V'=V+hU+\tfrac34Dh^2,\qquad U'=U+\tfrac32Dh.
\]

The six retained channels are volume, dust charge, scalar charge, reference
velocity, scalar offset and coordinate-time counter. Each has all three
Rule3 integers. There is no additional workspace or scheduler. The seven
degree-one onsite tensor terms give

\[
W_{n+1}=2W_n-W_{n-1}+6D,\qquad
W_n=4N^2V_n,\qquad
J_n=W_n-W_{n-1}+3D=4NU_n,\qquad h=1/N.
\]

All remainders `0..5` are retained unchanged. The previous volume slice is
physical velocity information, not an error term to delete. The integer
invariant is

\[
J_n^2-12DW_n-24N^2P^2=16N^2I.
\]

This is how the construction overcomes the earlier independently-null-target
minus-old-history obstruction: the observable constraint uses both retained
volume slices, and the chosen conserved coordinates make the complete
recurrence an exact flow. It does not cancel, reset or hide history.

The passive reconstruction uses

\[
a=V^{1/3},\quad B=V^{-1/3},\quad k=-U/(3V),\quad
p=P/V,\quad d^2=D/V,
\]

and a declared anchored logarithm for scalar phase. The reference velocity and
scalar offset are retained channels. Field values are not read from a stored
future trajectory or reconstructed solely from the tick counter. Roots and
logarithms are passive coordinate evaluations, not Engine updates.

## Einstein source and the limit on expansion claims

For `ds^2=-d tau^2+a^2 dx^2`, the source is

\[
\rho=\frac{P^2}{2V^2}+\frac DV,\qquad
p_{\rm fluid}=\frac{P^2}{2V^2}.
\]

The metric-derived component residuals are

\[
G_{00}-T_{00}=\frac{I}{3V^2},\qquad
G_{ii}-T_{ii}=\frac{I}{3V^{4/3}},\qquad
G_{\mu\nu}-T_{\mu\nu}=0\ (\mu\ne\nu).
\]

Thus all components vanish on the declared constraint. The scalar contribution
does not disappear because `Vddot` contains only dust: its conserved charge
enters the constraint and therefore the allowed expansion velocity. The source
also satisfies `rho_dot+3H(rho+p_fluid)=0`, with `H=U/(3V)`.

A bounce or repeated homogeneous density bursts cannot occur in this source.
On the constraint,

\[
\dot H=-\frac{D}{2V}-\frac{P^2}{2V^2}<0,\qquad
\frac{\ddot a}{a}=-\frac{D}{6V}-\frac{P^2}{3V^2}<0,\qquad
\dot\rho=-U\left(\frac{P^2}{V^3}+\frac{D}{V^2}\right)<0.
\]

The expanding branch has positive `H` and decreasing density. Positive
`Vddot` is not accelerated scale-factor expansion: volume is `a^3`.
These identities were checked independently with symbolic off-constraint
residuals before imposing `I=0`.

The arithmetic polynomial continues through zero or negative volume; its
physical chart does not. Two positive endpoints can straddle a singular
interval. The existing contracting-to-expanding negative control has positive
endpoint volumes but an interior minimum `V=-2`; it is not a bounce solution.
Extending the integer recurrence across that interval cannot establish a
regular physical continuation.

## Fresh focused verification

Tests were run in an isolated checkout of the exact reviewed commit.

| Verification | Observed result |
|---|---|
| `python -m unittest universe24.tests.test_sourced_map -q` | All 14 tests passed |
| `physical_map.symbolic_audit()` | Flow, constraint, scalar/dust balances and field equations passed |
| `physical_map.metric_curvature_audit()` | All 16 metric-derived Einstein component identities passed |
| `domain.audit()` | Exact interval and integer-growth controls passed |
| `native.negative_controls()` | Invalid charts rejected; off-constraint invariant `-12` remained nonzero; deleting source coupling broke the constraint while preserving rewind |
| Independent expansion/acceleration/density identities above | Passed exactly |

A further actual Engine run used `N=24`, the standard mixed-remainder seed,
27 nodes and **16,384 consecutive forward steps**. Every step was compared
against the independent scalar integer oracle and its full inverse; every
remainder was checked unchanged. The full final state rewound to the seed.
There were 7,962,624 retained-integer comparisons and 64 exact physical
checkpoints, each with zero constraint. The exact closed-form volume register
was checked at every step.

| Long-run quantity | Value |
|---|---|
| Final proper-time coordinate | `2048/3` |
| Final volume | `1054723/3` |
| Final volume velocity | `1027` |
| Maximum retained integer size | 30 bits |
| Observed elapsed time, including oracle/inverse/rewind checks | About 7.62 seconds |

The timing is one local observation, not a hardware-independent performance
promise. No fresh full-repository suite or CI result is claimed by this review.

## Scalability and the remaining integration work

For fixed initial integers and dust charge,

\[
W_n=W_0+nJ_0+3Dn^2.
\]

Retained integer size grows as `O(log n)` in this sector. This removes the
projective denominator explosion of the earlier particular encoding; it does
not establish the cost of massive, spatial or interacting apparatus models.
The expanding positive-volume chart is forward invariant for all positive
time. It still has a finite past singularity for the declared mixed source.

The native tensor contains no spatial-edge interactions. Identically prepared
nodes are copies of the same homogeneous solution. Forty-two unallocated
channels are capacity, not evidence that spatial waves, operational clocks,
detectors and memory can be coupled consistently. The coordinate counter is
not an independent material clock. Passive geodesics of the reconstructed
metric do not by themselves demonstrate propagating matter packets.

The concrete next solution boundary is a source-preserving extension of this
complete-state construction. For a massive scalar, `P=pV` is no longer
conserved: `Pdot=-m^2*phi*V`, so keeping the present frozen charge and merely
relabeling the mass is invalid. A candidate must retain the evolving scalar
phase/momentum, include the resulting stress in geometry, and recover this
exact massless limit under the same declared physical decoding. Its full
workspace and clock allocation must still fit 48 channels.

Acceptance must compare complete-state oracle/inverse behavior, all Einstein
source residuals, a fixed-time refinement test, positivity over whole physical
intervals, and retained-bit growth. Spatial propagation and an operational
clock need separate same-run tests after that source extension. A requested
bounce requires a separately justified source or geometry extension with a
new physical acceptance argument; neither a decoder plot nor a scheduler can
create it under the current positive flat scalar+dust equations.

Source file SHA-256 values:

```
validation/sourced_map/native.py
714aaf6d716c3e8877dd284a33562ba81b5c57221825b679e87e5d9827b7dee8
validation/sourced_map/physical_map.py
457abf84385637b00f5adcb0aa071048fbbf17d12f7cb70168a0ce7f8b83d092
validation/sourced_map/domain.py
2f40e23559d81e9cf530ba892544710d08028b97745c3caf6afa5d7caa5dad64
```
