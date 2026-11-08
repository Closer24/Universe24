# A baseline internal frequency gap without changed coefficients

Status: exact coupling algebra and an exact finite-duration preparation
construction. No new trajectory or engine variant is needed for the proof.
The independent matrix oracle verified all eight integer coordinate vectors in
[this certificate](evidence/independent_audit/internal_channel_eigenvectors.json).
This concerns a spatially uniform internal mode, not a localized building block,
transported particle, physical mass, or complexity-selection mechanism.

## The unchanged channel algebra already has a nonuniform internal mode

At spatial wave vector k=0, the +++ input map on the48 channel values is

```text
F0 = 2I + R(q_y) + R(q_y^-1) + R(q_z^3) + R(q_z^-3),
```

where `(R(h)v)(g)=v(g*h)`. To see this directly from the coupling definition,
for any channel orientation g, the six world directions map bijectively to
the six body directions. Summing their body actions therefore gives the same
two identities and four right multiplications displayed above.

The actual quaternion generators are `q_y=(1+j)/sqrt(2)` and
`q_z=(1+k)/sqrt(2)`. Hence

```text
q_y + q_y^-1 = sqrt(2),
q_z^3 + q_z^-3 = -sqrt(2).
```

For any one of the four real quaternion-coordinate functions v(g), right
multiplication and addition thus give `F0*v=2*v`. The uniform channel function
instead has eigenvalue6. These are distinct internal response families under
the same fixed +++ coupling and num=den=1.

The repository represents each quaternion coordinate as `(A+B*sqrt(2))/2`
with integer A,B. Because F0 is an integer matrix, equating rational and
irrational parts proves `F0*A=2*A` and `F0*B=2*B` separately. This supplies
eight explicit integer eigenvectors from the four coordinates' two coefficient
parts. For a concrete nonzero choice use the A coefficient of the scalar
quaternion coordinate; its identity-channel entry is2. The independent
4x4-matrix oracle confirms each of these integer eigenvector identities without
using the production coupling table as its expected answer.

In the full-channel linear comparison from
[the wave derivation](coherent_wave_algebra.md), an F0 eigenvalue2 gives
`cos(omega)=2/6=1/3`, whereas the uniform eigenvalue6 gives zero frequency.
Thus an internal frequency gap `omega=arccos(1/3)` already exists in the
baseline comparison at k=0. Changing a primitive num/den ratio is not necessary
merely to obtain such a gap. Behavior at nonzero k, localization, group velocity
and physical mass remain separate questions. Continuity of the finite Bloch
matrix ensures nearby eigenvalue branches, but supplies none of those further
quantitative or physical identifications by itself.

## Exact native realization for any registered finite duration

Choose one of the integer eigenvectors v, a positive integer duration H>=1,
and any periodic side L>=3. At EVERY spatial site prepare, for channel g,

```text
b_g(0)=3^H*v_g,
a_g(0)=3^(H-1)*v_g,
r_g(0)=2.
```

This is one complete board preparation. It is spatially uniform, but the
channel values are not all equal. All later inputs are computed by the normal
fixed coupling; there is no supplied time sequence.

Define integers `C_0=C_1=1` and
`C_(t+1)=2*C_t-9*C_(t-1)`. Then the unchanged Rule3 gives exactly

```text
b_g(t)=3^(H-t)*C_t*v_g,       0<=t<=H,
a_g(t)=b_g(t-1),             1<=t<=H,
r_g(t)=2,                   0<=t<=H.
```

Proof: at every t<H the scalar amplitude of b(t) is divisible by3. The
eigenvector identity gives `u_g(t)=2*b_g(t)`, so
`divmod(2*u_g(t)+2,6)` gives exactly
`ell_g(t)=(2/3)*b_g(t)` and remainder2, including negative entries. The first
step is `b(1)=(2/3)*3^H*v-3^(H-1)*v=3^(H-1)*v`. At subsequent steps, factoring
`3^(H-t-1)` from `(2/3)*b(t)-b(t-1)` gives precisely the C recurrence.
This completes induction through state H.

Equivalently `C_t/3^t=cos(t*arccos(1/3))`. The integer board therefore follows
that internally gapped cosine mode exactly for the entire declared duration.
This is a family indexed by H, not one finite-amplitude eternal exact integer
oscillator: the initial counter magnitude grows exponentially with H, and the
divisibility proof makes no promise after H. It is also not a localized clock
with an independently composable halo, because the preparation fills the board.

For this construction, every nonzero eigenvector channel produces C0 at every
update1..H. Indeed C_t is nonzero modulo3, so the quotient is nonzero, and an
unchanged nonzero triple would require both a=b and `(2/3)*b=2*a`, impossible.
The remainder is unchanged, so the passive class is0. Channels with v_g=0 stay
stationary. These C0 events are internal arithmetic events in a prepared global
oscillation; they do not certify routing, unique outcomes or received approval.

## What a subsequent test would add

A native run would test implementation and provide a generic Presenter example
of this already specified finite construction. It should register H, the
integer eigenvector, size, complete initial state and exact counter/C predictions
before evolution, and retain every full-state inverse. It would not establish
transport or mass. A later nonzero-k family and localized packet comparison
would require their own frozen observables and error bounds. The proposal
adds no coefficients, force, runtime choice or state-dependent tensor.
