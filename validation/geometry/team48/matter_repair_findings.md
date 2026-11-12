# Exact face fluxes and time-polarized matter balances

This is a research control based on PR #42 (`49b896c`), with new code in
`matter_repair_flux.py`. It neither changes the 41/44-channel evolution nor
claims its Einstein, Maxwell or detector gates are closed.

## What the literature changes in the design

Christiansen, Halvorsen and Scheid,
[Numerical Methods for PDEs 39 (2023), 3271–3308](https://doi.org/10.1002/num.23008),
derive a gauge-compatible Maxwell–Klein–Gordon discretization, prove a
semidiscrete convergence result in two spatial dimensions, and construct
a compatible fully discrete leapfrog method. Their equations use parallel
transport to compare neighboring scalar values. Separately differencing the
ordinary gradient and gauge-potential term breaks the local gauge symmetry.
Their result is not a proof about our integer tensor or general relativity.

This gives two specific directions: use the discrete action's conserved
quantity (which may involve both retained time slices), and use one
shared face flux for charge transport and the Maxwell divergence constraint.
Neither requires a runtime constraint projection.

## Exact identities already available in the retained state

The test field is one-dimensional, massless and flat, with two scalar
components `phi, chi`, momenta `P_phi, P_chi` and gradients `X_phi, X_chi`.
Let `D f=(f[x+1]-f[x-1])/2`. The physical recurrence is

```
phi_next = phi_previous + 2 P_phi
P_next   = P_previous   + 2 D X
X_next   = X_previous   + 2 D P
```

One computational sign channel compiles these six fields to **7 actual
channels**, all using the unchanged fixed-six Engine. All products below
are observations of those existing retained slices. They are not hidden
state or updated registers.

For current values `f` and previous values `f-`, define doubled densities

```
Q2 = phi P_chi- + phi- P_chi - chi P_phi- - chi- P_phi
E2 = sum_s (P_s P_s- + X_s X_s-)
M2 = -sum_s (P_s X_s- + P_s- X_s)
```

For neighboring current values at `x` and `y=x+1`, define face fluxes

```
JQ(x,y) = phi_x Xchi_y + phi_y Xchi_x
           - chi_x Xphi_y - chi_y Xphi_x
JE(x,y) = sum_s (P_s,x X_s,y + P_s,y X_s,x)
JM(x,y) = -sum_s (P_s,x P_s,y + X_s,x X_s,y)
```

Direct substitution, without a continuum product rule, gives

```
E2_next - E2 = JE(x,x+1) - JE(x-1,x)
M2_next - M2 = JM(x,x+1) - JM(x-1,x)
Q2_next - Q2 = JQ(x,x+1) - JQ(x-1,x)
```

With the conventional conservation equation `density_dot + div(flux)=0`,
the outward physical flux is the negative of the displayed `J`.

The charge identity additionally requires `X_phi=D phi` and `X_chi=D chi`.
These constraints propagate exactly as `C_next=C_previous`, so both
prepared slices must satisfy them. Energy and momentum identities hold for
arbitrary two-time scalar data, but their time-polarized densities are not
positive for arbitrary histories. They must not be advertised as a general
positive-energy stability theorem.

This is a special case of the elementary leapfrog identity: if a quadratic
form `y^T S y` has `y^T S f(y)=0`, then `y[n]^T S y[n-1]` is exactly
conserved by `y[n+1]=y[n-1]+2h f(y[n])`.

## Actual fixed-six Gauss propagation control

Adding one retained face field gives **8 channels**. It obeys

```
Eface_next = Eface_previous + JQ_current + JQ_previous.
```

The exact cubic tensor uses the sign phase times two scalar factors, and
old-`a` dependencies have stages `phase -> scalar -> Eface`. Every monomial
is on the target face, including the face-field endpoints. Preparing
`Eface_current-Eface_previous=JQ_previous` makes the first-order identity
`Eface_next-Eface_current=JQ_current` invariant. Consequently

```
G = Eface(x)-Eface(x-1)-Q2
```

is exactly constant. A zero initial `G` stays zero. The 12-update actual
Engine control has zero local Gauss residual and complete rewind.
Replacing the face flux with the same-node current breaks Gauss in the
matched negative control, while its arithmetic still rewinds.

This is a **one-way current-to-face accumulator control**. There is no
Lorentz-force return to the scalar, no dynamically evolved gauge potential,
and no combined scalar/electromagnetic energy balance. It is therefore not
a completed Maxwell–Klein–Gordon model and is not appended to the 44-channel
candidate.

## Fixed-domain integer refinement

The same 7-channel tensor runs at physical `dt=dx=1/L` by declared static
field units:

```
phi = Phi/A,  pi = P/(dt A),  physical_gradient = X/(dt A),
A = 2 L^6.
```

Both initial slices are exact sampled right/left traveling profiles built
from the periodic C2 polynomial `f(x)=x^3(1-x)^3`. No future trajectory is
stored; the immutable local linear tensor advances the seed. The sampled
scalar d'Alembert solution is exact for every tick, while the retained
centered derivatives approximate its continuum derivatives. At fixed
physical final time `1/4`:

| L | Engine steps | scalar grid error | maximum pi/gradient error |
|---:|---:|---:|---:|
| 8 | 2 | 0 | 159/8192 |
| 16 | 4 | 0 | 663/131072 |
| 24 | 6 | 0 | 3839/1327104 |

All three local balance residuals are exactly zero at every update.
The bound `|f'''|<=6` on each smooth portion of the periodic C2 profile,
and total profile weight at most three, gives the uniform centered
derivative error bound `3 dx^2`. The bounded one-sided third derivatives
also give this bound across the periodic join by the integral remainder.
This is an actual integer refinement family for this prepared 1D sector;
it is not a generic 3D CFL or curved-source refinement family. It shows why
raw unweighted coefficient integrality alone cannot rule out refinement.

## A precise remaining gauge defect

For a continuum pure gauge `theta(x)=2 atan(x)`, scalar
`Phi=(cos theta,sin theta)` and `A=2/(1+x^2)`, the centered additive
covariant derivative at `x=0` has residual

```
Xi_additive = (0,-2 dx^2/(1+dx^2)).
```

Transporting each neighbor with `U(0,y)=R(0) R(y)^T` gives exactly zero.
The audit checks both statements with exact rational arithmetic for
`dx=1,1/2,1/4,1/8,1/16`. This is an independent stencil calculation, not an
Engine implementation. At `dx=1/2`, the transport uses `3/5,4/5`; simply
replacing the retained additive potential by unscaled integer rotations
does not implement it. A compact reversible dynamic transport encoding and
its exact denominator invariant are still needed.

## Reproduction and acceptance boundary

```
python -m validation.geometry.team48.matter_repair_flux
```

Output: `runs/team48/matter/repair_flux.json`, with source/tensor hashes.
The audit also tests arbitrary integer preparations, 100-bit amplitudes,
all remainder classes, independent recurrence outputs, full inverse/rewind,
wrong same-time density diagnostics, and broken gradient constraints.

The full geometry still needs a compatible discrete stress/Bianchi pair.
Substituting these polarized scalar densities into the existing Einstein
Hamiltonian constraint would change its source definition and does not
constitute a proof of a consistent new gravitational law. That change
requires a joint discrete derivation and its own constraint/refinement tests.
