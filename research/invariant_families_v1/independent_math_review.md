# Independent review of exact invariant pattern families

This review concerns a new mathematical and computational scope. It does not change the frozen 890-case clock-selection evidence or validate an unavailable historical 48-run claim. The implementation remains one board, 48 channels, six spatial neighbors, synchronous Rule3 and a tensor fixed before startup. Every elementary update has `num=den=1`.

## Exact embedding

Write the fixed linear neighbor operator as F. Let a full-address pattern v have entries only −1, 0 or +1 and satisfy Fv=λv. For any integers a,b and any remainder r in0..5, assign positive-pattern addresses `(a,b,r)`, negative-pattern addresses `(-a,-b,J(r))`, and zero-pattern addresses `(0,0,r_background)`, where each zero-address remainder is fixed and valid. Here

`J(r)=4-r+2*(r mod2)`.

The remainder map sends0..5 to4,5,2,3,0,1. It is an involution and preserves parity. If `2u+r=6*ell+s`, then s and r have the same parity p, and

`-2u+J(r)=-6*ell+J(s)`.

Because J(s) is again the unique remainder in0..5, its quotient is exactly `-ell`. Therefore one full native update maps the embedded scalar state to the embedding of

`ell,r_next=divmod(2*λ*b+r,6); a_next=b; b_next=ell-a`.

Zero-pattern addresses have zero neighbor sum and remain motionless. This proves closure for all scalar integers and valid remainders, by induction for every duration. It does not assert closure under arbitrary perturbations outside the encoded family.

The matrix reference in `reference.py` constructs rotations and couplings independently of the production quaternion/routing implementation. It checks every address of the finite representative boards, rather than reading the production tensor table as its own oracle.

| Pattern under +++ | Compatible board | λ | Scalar coefficient multiplying b before the remainder correction | Normalized effective ratio λ/6 |
| --- | --- | ---: | ---: | ---: |
| Every address has v=1 | Any L≥3 | 6 | 2 | 1 |
| Every channel uses x-profile(1,−1,0) | L divisible by3 | 3 | 1 | 1/2 |
| Every channel uses x-profile(1,0,−1,0) | L divisible by4 | 4 | 4/3 | 2/3 |
| v_g=(R(g)e_y)_y, constant in space | Any L≥3 | 4 | 4/3 | 2/3 |

The internal pattern has eight positive channels, eight negative channels and32 zero channels. The exact independent operator also gives eigenvalue0 for this same R_yy pattern under the fixed signs(+,-,+), yielding a quarter-turn scalar orbit. The rotated R_zz pattern instead has eigenvalue4 under(+,-,+). The independent reference checks all72 combinations of eight sign triples and nine rotation-matrix entries; generally its eigenvalue is2*sigma_x+2*sigma_y*[j=y]+2*sigma_z*[j=z] for(R(g)e_j)_k. These signed/operator identities are separate from the initially planned all-+++ native batch.

For λ=6, every remainder stays fixed and the scalar counters obey `b_next=2b-a`; this can drift and is not an oscillator claim. For λ=3, every remainder stays fixed and the pair obeys `(a,b)->(b,b-a)`, with minimal period6 for every nonzero integer pair. The λ=4 family retains a nontrivial remainder correction; one must not replace its complete nonlinear integer family by an exact sinusoid merely because its linear comparison has a frequency.

## Effective ratio and remainder domain

The coefficient multiplying b in this reduced recurrence is λ/3. The normalized comparison parameter is instead `alpha_eff=λ/6`, since a spatially uniform scalar field has six identical neighbors. Neither number changes a primitive channel parameter.

If `p/q=λ/6` in lowest terms, the general normalized scalar comparison has remainder ρ in0..6q−1 and update `divmod(12*p*b+ρ,6*q)`. Setting `ρ=q*r+j`, with a fixed integer0≤j<q, gives exactly the embedded six-remainder recurrence and preserves j. A batch using only the six baseline remainders and fixed zero-pattern remainder2 checks the j=0 slice. It does not by itself test all6q generalized remainder states. An extension storing j in otherwise stationary zero-pattern channels can be specified separately; it is not implicit in that six-remainder batch.

These are global invariant preparations, including periodic sheets and channel patterns. They are not localized particles, transported intrinsic masses, detectors, generic interacting components or a proof of a physical effective law.

## Exact planar additive symmetry

For +++ and periodic L, let s=x+y+z modulo L and let f be any integer periodic profile. The exact planar trajectory is `a_P(t)=f(s+1-t)`, `b_P(t)=f(s-t)`. Its input is `u_P=3*(f(s-1-t)+f(s+1-t))`, so2u_P is divisible by6.

Given any other baseline+++ solution S, add these planar counters to its counters at every channel while retaining its original remainders. Native division then shifts the quotient by exactly u_P/3 and leaves every remainder unchanged. The sum evolves as S+P forever. This is a particular exact additive solution symmetry, not general superposition of arbitrary nonlinear solutions. No state is added during execution; the initial sum is prepared once.

Consequently, a proposed interaction test between this exact planar sector and an encoded residual has identically zero counter/remainder interaction defect. It cannot demonstrate that this plane activates or changes the residual. Since u_P is divisible by3, the potential arithmetic event class is unchanged; the actual guarded C event can nevertheless appear or disappear when the quotient or unchanged-triple guard changes. Event-class equality must not be confused with equality of observed clicks.

## Other transparent additions and a prospective nonlinear carry

The same additive argument holds for any counter-field trajectory P obeying a_P_next=b_P and b_P_next=F(b_P)/3-a_P with F(b_P) divisible by3 everywhere and at every step. The eigenvalue3 period-six family and eigenvalue6 uniform family satisfy this exactly. Their addition to a residual under the same tensor cannot change that residual's counters or remainders.

Two eigenvalue4 ternary preparations with initial a=0, b equal to each pattern, and common r=2 instead have a precise possible first-step interaction. At a double-positive address, either singleton has quotient1/remainder4, whereas the joint has quotient3/remainder0. Its counter-additivity defect is+1; at a double-negative address it is−1. This prediction follows directly from native arithmetic and does not require a new force. It does require a separately frozen four-mask native test before being reported as a recorded overlap result. It says nothing by itself about localized propagation, binding, approval or preferred complexity.
