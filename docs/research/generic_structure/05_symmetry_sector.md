# Exact symmetry-sector extraction from the actual common45 tensor

Published source: PR52, `8c53e69f4b466dcbd2da7dab7e3c365bd9731766`.
The constructor is `validation.completion.common45.build45()` at its unchanged
default `dt=1/64`, `dx=1/4`, mass squared one. No production code is changed.

The new reusable extractor derives a **six-channel, fourteen-monomial** lab
directly from that actual 45-channel tensor. It proves closure of the full
retained state, including both histories and every carry. This is an exact
homogeneous, isotropic, neutral sector, not a compression of arbitrary45
geometry or a new supported physical model.

## General construction and theorem

`extract_homogeneous_sector(full, reduced_names, mapping, omitted_carries=...)`
accepts any b-only integer polynomial tensor whose canonical coefficients in
`u` are divisible by three. Each full channel is either identified with one
reduced channel or set to zero in both retained `a,b` histories.

The declared state image has these requirements:

1. Every reduced `a,b` row is spatially homogeneous. The two histories may be
   distinct arbitrary signed integers; old history is not set to zero by the
   theorem.
2. Identified full channels copy the same reduced `(a,b,r)` at each node.
3. Omitted full channels have `a=b=0` and the exact legal carry specified in
   the certificate. This audit uses `full_channel_index mod6`, so omitted
   carries are not all zero.
4. Reduced carries can take any of the six values and can vary with node.
   They need not be spatially homogeneous.

For each source monomial the extractor replaces a factor by its identified
variable, removes monomials containing an omitted zero variable, collapses
face offsets using spatial homogeneity, and combines equal monomials with
integer coefficients. It checks **every source target row**: identified
targets must yield identical reduced polynomials, while omitted targets must
yield the zero polynomial. Failure prevents creation of the certificate.
This is exact coefficient comparison, not a sampled numerical closure test.

Let `E` copy all retained registers by the declared map and `P` read one
representative from each class. Then `PE=identity`, so the embedding is
injective. Because each `u` coefficient is divisible by three,

\[
\operatorname{divmod}(2u+r,6)=(u/3,r),\qquad 0\le r<6.
\]

Consequently the full map is `(a,b,r) -> (b, u(b)/3-a, r)`. The checked
polynomial identities imply `F_full E=E F_reduced`: copied histories remain
copied, omitted histories remain zero and every carry remains exactly as
declared. The inverse is `(a',b',r) -> (u(a')/3-b',a',r)`, so the same
identities prove `F_full^-1 E=E F_reduced^-1`. The image is invariant in both
directions. This proof covers arbitrary legal reduced carries and arbitrary
signed histories in the stated image, rather than just prepared physical
initial data.

`embed` checks that every reduced carry is an exact integer in0..5, rather
than relying on the State constructor to enforce that range. `project`
validates the complete image before returning a reduced state. It
rejects unrepresented old history, unequal copies, changed omitted carries
and nonhomogeneous histories. The fixed carry choices are part of the sector
definition, not erased data from an arbitrary incoming state. Changing them
defines a different sector. There is no claim of recovering arbitrary45
independent carry values from six channels.

## The common45 specialization

| Reduced channel | Full channels represented |
| --- | --- |
| D | projective.denominator |
| B | B00, B11, B22 |
| K | K00, K11, K22 |
| phi | phi |
| Pi | Pi_phi |
| dust | dust_amplitude |

All omitted geometric off-diagonal/connection channels, the second scalar
component, spatial gradients, Maxwell fields and potentials have zero `a,b`.
Every node carries the same field histories. This removes arbitrary spatial,
anisotropic and charged physics by an explicitly proved symmetry restriction.

With `C=256`, the extracted quotient-minus-history recurrence is

\[
\begin{aligned}
D'&=256D^2-D_{old},\\
B'&=256DB+4BK-B_{old},\\
K'&=256DK+12K^2-2\phi^2-2d^2-K_{old},\\
\phi'&=256D\phi+4D\Pi-\phi_{old},\\
\Pi'&=256D\Pi+12K\Pi-4D\phi-\Pi_{old},\\
d'&=256Dd+6Kd-d_{old}.
\end{aligned}
\]

The actual stored tensor contains `u` coefficients three times these
polynomial coefficients; the Engine divisor remains six. There are fourteen
degree-two monomials, no face reads in the reduced homogeneous law and eighteen
retained integers per node. The actual full law still contains45 channels.
The reduced tensor is derived from its monomials, not independently typed
from these displayed equations.

## Executed complete-state checks

The audit runs twelve deterministic random trials on27 nodes, each with
different signed old/current homogeneous histories and mixed carries. Each
trial checks backward commutation before any forward step, then three
forward steps against both full and reduced independent scalar oracles.
Every forward result, each inverse step and complete rewind match under the
embedding. All45 full channels and all `(a,b,r)` entries are compared:
**131,220 integer-entry comparisons**, plus the separate inverse and
projection comparisons. All six carry values occur and are retained.

Eleven malformed controls are rejected: changed copied old history, changed
copied current history, changed copied carry, changed omitted old history,
changed omitted carry, spatial inhomogeneity, illegal carries -1 and6, an
incorrect channel identification, forcing an omitted channel and removal of
carry transparency.
The last three are construction-level failures, not only runtime seed checks.

## The reduced lab preserves the physical failures

Start from physical `B=1`, `K=-1`, `phi=2`, `Pi=0`, `dust=1`, with current
denominator4 and all old registers zero. The original homogeneous Einstein
constraint is

\[
H=6K^2-\Pi^2-\phi^2-2d^2.
\]

Initially H is zero. The actual full and reduced first Engine states agree
and give **H_after=-7/4096=-7h²**. The full equation builder independently
returns the same residual. Carry choices differ from other published
fixtures only where required by this explicit embedding; since all carries
are frozen and do not affect the quotient, they cannot repair this failure.

The denominator recurrence is unchanged. On the physical preparation
`D_old=0`, `D0>=2`, `C>=2`, induction gives `D_n>=D0^(2^n)`. Six further
actual reduced steps record denominator and maximum retained bit lengths,
and rewind exactly. Reduced channel count does not remove exponential bit
growth or improve the source's integrator.

This lab is useful for proving or falsifying prospective constraint and
native-time laws with a known embedding back to the source. A changed six-field
law must obtain a new full-law embedding certificate before it can count as a
repair of common45. An exact theorem on this restricted image does not
establish Einstein convergence, operational clocks or generic geodesics.

## Reproduction

```bash
python -m validation.generic_structure.symmetry_sector
```

The output is `runs/generic-structure/symmetry_sector.json`. It includes the
complete embedding certificate, reduced tensor, source fingerprints/hashes,
malformed controls, exact constraint failure and bit-cost rows. No observer
or reduction callback feeds the evolving full Engine state.
