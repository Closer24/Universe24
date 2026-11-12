# An actual six-channel sourced native map

Agent 3, issue #58. Source base:
`f4f64e062f07b3ca119eccf655df746be206908b`. Implementation:
`validation/sourced_map/native.py`; complete evidence:
`runs/sourced_map/native.json`.

The unchanged Rule3 Engine now implements the **exact homogeneous expanding
massless scalar plus normal-dust volume flow** in six channels. One microtick
is one physical macro step. It uses seven linear onsite monomials, all six
carry classes, both retained histories, and no workspace, scheduler, reset,
runtime solve or external evolution callback. It is a restricted sourced
Einstein sector, not the massive six-sector target or a spatial/full-frame
solution. Its nonrational physical coordinates are explicitly passive readouts.

## The physical map that is actually compiled

Write V=B^-3, U=dV/dtau=-3kV, P=pV and D=d²V. In the massless homogeneous
sector, P and D are constants and the reduced equations give

\[
\dot V=U,\qquad \dot U=\frac32D,\qquad
I_{\rm phys}=U^2-3DV-\frac32P^2=0.
\]

Their exact time-h map is

\[
V'=V+hU+\frac34Dh^2,\qquad U'=U+\frac32Dh.
\]

The companion physical-map derivation checks all five physical evolution
equations, the homogeneous Einstein equations and source conservation. This
compiler implements that map, rather than replacing its force with a similar
mechanical potential or compiling a constraint-preserving numerator and then
discarding the mandatory history subtraction.

Take h=1/N with N a positive construction/preparation integer. Define W=4N²V
and infer the current scaled velocity from the complete retained volume pair:

\[
J=b_W-a_W+3D,\qquad U=J/(4N).
\]

The immutable tensor is independent of N:

\[
u_W=6b_W+18b_D,
\qquad u_j=6b_j\quad\text{for the other five channels}.
\]

Every u is a multiple of three. For any legal carry r,
`divmod(2u+r,6)=(u/3,r)`. Hence the actual Engine gives

\[
a_W'=b_W,\qquad b_W'=2b_W-a_W+6D,
\qquad r_W'=r_W.
\]

Substituting the complete-state decoder proves

\[
W'=W+J+3D,\qquad J'=J+6D,
\]

which is precisely the exact physical map above. The old physical velocity
is retained in the volume history, not stored in an uncounted register. The
history subtraction is essential to the correct map and is not an unwanted
error term to be projected away.

The invariant is an exact integer polynomial of the actual state:

\[
I_{\mathbb Z}=(b_W-a_W+3D)^2-12Db_W-24N^2P^2.
\]

Expansion gives I_Z'=I_Z on the frozen-source sector. Its physical meaning is
I_phys=I_Z/(16N²). Thus the original physical constraint
`6k²-p²-2d²` equals `I_Z/(24N²V²)`. Exact closure is not a small residual
threshold and is not obtained by defining a new unrelated diagnostic.

## Complete allocation and seed

| Index | Channel | Retained role | Preparation of a,b |
| --- | --- | --- | --- |
| 0 | `volume` | Current volume and the history encoding its velocity | a=4N²V-4NU+3D, b=4N²V |
| 1 | `dust_charge` | Conserved D=d²V | a=b=D |
| 2 | `scalar_charge` | Conserved P=pV | a=b=P |
| 3 | `reference_velocity` | Scalar integration anchor, raw 4N Uref | a=b=4N Uref |
| 4 | `scalar_offset` | Retained phi_ref in fixed scalar units | a=b=phi_ref |
| 5 | `proper_tick` | Coordinate-time counter | a=-1, b=0 |

Each row retains its own r, for **six channels and eighteen integer entries
per node**. All legal carry values are supported and remain unchanged. The
physical homogeneous a,b data may coexist with spatially nonuniform carries;
no carry is discarded to obtain homogeneity. Source/reference/offset channels
are fixed only on their explicit a=b preparation sector. Their off-sector
raw Engine evolution remains reversible but does not have this physical
interpretation.

The default seed has (V,U,P,D)=(1,3,2,1), Uref=3 and phi_ref=0. Therefore
the physical initial data are (B,k,p,phi,d)=(1,-1,2,0,1). The past volume
W_old=4N²-12N+3 is part of the complete seed and is the exact earlier volume,
not a future answer. No list of subsequent states is prepared.

## Readout is explicit and uses the actual state

`read_conserved(program,state)` returns V,U,D,P,Uref,phi_ref,tau and I_Z.
It reads volume and velocity directly from a_W,b_W and retained D. It never
reconstructs them from elapsed time and the initial seed. Tau=b_tick/N is a
coordinate-time readout and never drives the tensor.

The companion `physical_map.physical_decode` supplies

\[
B=V^{-1/3},\quad k=-\frac{U}{3V},\quad
p=\frac P V,\quad d=+\sqrt{D/V},
\]

and, for s=sqrt(3P²/2),

\[
\phi=\phi_{\rm ref}+\frac P s
\log\left[\frac{(U-s)/(U+s)}{(U_{\rm ref}-s)/(U_{\rm ref}+s)}\right].
\]

These roots and logarithm are declared physical coordinate transformations,
not integer Engine arithmetic. Scalar phase is not an additional uncounted
stored field: its integration anchor and offset occupy two of the six
channels, while U and P determine its current value. This is an analytic
reduction of the massless sector; it must not be described as the original
rational six-field representation or a massive phase integrator.

The chart is D>0, P!=0, V>0, U>s and Uref>s, with positive dust amplitude.
The preparation and decoder also check the previous physical volume and
velocity implied by the retained history. D>0 and positive U make the
volume monotone on that single step, so this check covers the history interval.
Arbitrary long inverse paths need their own whole-interval domain check;
raw arithmetic reversibility permits states beyond the physical chart.

`prepare_native` requires exactly integral 4N²V and 4NU, integer D/P/phi_ref
in the declared units, and all complete carries. It rejects floats, bools,
invalid scales, unsupported zero-source charts and inhomogeneous physical
a,b data. It does **not** solve or project the constraint. Off-constraint
data within the chart remain observable through a nonzero I_Z.

## Joined APIs

```python
program = build_native(N)                     # NativeProgram(N, tensor)
seed = prepare_native(program, L=3, V=F(1), U=F(3),
                      D=1, P=2, phi_ref=0, remainders=None)
after = Engine(program.tensor).step(seed)      # only evolution operation
coordinates = read_conserved(program, after)
physical = physical_decode(coordinates, mass_squared=0, precision=80)
```

`volume_step` and `target_step` from the independently developed physical-map
module agree exactly with the actual decoded macro. The native audit also
uses its own direct Fraction macro formula and a scalar Rule3 register oracle
which does not call the compiled Tensor evaluator.

## Executed evidence

Run:

```bash
python -m validation.sourced_map.native
```

There are eleven complete Engine runs and **26,244** scalar retained-integer
comparisons. Every step agrees with the independent scalar oracle, every
single-step inverse passes, and every run completely rewinds. All carries
are checked against the seed. Maximum retained size is **18 bits** across
these runs. Evidence includes every tensor, seed, microstate, exact decoded
coordinate and source hash.

| Case family | Actual steps | Physical endpoint | Evidence |
| --- | ---: | --- | --- |
| N=24,48,96, mixed all-six carries at every channel | 3,6,12 | tau=1/8 | One identical tensor; exact physical macro and zero constraint at every boundary |
| D=2,P=-2,V=1/2,U=3,phi_ref=-1 | 3 | tau=1/8 | Signed scalar and nondefault source/offset |
| V=1,D=1,P=22,U=27 | 12 | tau=1/8 | Constrained scalar intervention at unchanged initial volume/dust |
| Six uniform carry preparations r=0,...,5 | 3 each | tau=1/8 | All declared complete-state carry classes |

For the default fixture the exact endpoint is V=355/256, U=51/16.
The separate physical decoder gives approximately B=.896748249161118,
k=-.766197183098592, p=1.44225352112676, phi=.211704437661102 and
d=.849191827894840. Independent ODE/refinement evidence belongs to the
oracle report, rather than being inferred from these identities alone.

The scalar charge P does not appear explicitly in the volume acceleration
because the reduced Einstein equations give Udot=3D/2. It affects admissible
initial velocity through the independently required source constraint and
subsequently determines scalar density and phase. The same-V,D intervention
from P=2,U=3 to P=22,U=27 checks that this source information is present;
it is not a runtime adjustment or a second tensor.

Two meaningful failed controls are retained:

* Shifting both initial volume histories by one preserves velocity but gives
  I_Z=-12. Three actual steps retain exactly -12. The implementation does
  not repair or hide an initially violated constraint.
* Removing the actual `18D` volume coupling from the tensor, while retaining
  the same prepared dust, produces nonzero constraint defects. Its full
  arithmetic rewind still succeeds. Inversion alone is not physical closure.

## Remaining boundary

There is no cubic-gating or changing-denominator problem in this affine
reduction. This does not solve those problems for the massive model. When
mass squared is nonzero, Pdot=-mass_squared*phi*V generally does not vanish;
freezing P would violate the scalar equation. The scalar primitive, volume
flow and invariant used here cannot be relabeled as massive-source success.

The six-channel result also has no spatial gradients, propagated signals,
independently ticking apparatus or general-frame constraint proof. Its counter
records proper coordinate time along the declared comoving FLRW congruence;
it is not an operational clock. Subsequent spatial or massive extensions must
retain the same accounting discipline and supply their own constraint,
readout-domain and convergence evidence.
