# An exact sourced map that includes its retained history

Task 1 of the eight-agent issue #58 investigation. Baseline:
`f4f64e062f07b3ca119eccf655df746be206908b`.

There is an actual six-channel Rule3 implementation of the construction
below in `validation/sourced_map/native.py`. This report supplies its
physical coordinate map, exact identities and passive decoder. The result
is restricted to a **spatially homogeneous, spatially flat, expanding
massless scalar plus positive dust sector**. It does not solve the massive
scalar or general spatial Einstein problem and does not promote a default.

## Physical target and the useful coordinate change

Use proper time, unit lapse, zero shift, and the inverse scale factor `B`:

```text
ds² = -dt² + B^(-2)(dx²+dy²+dz²),   8 pi G = c = 1.
Bdot = k B
kdot = 3k² - d²/2
pdot = 3kp
phidot = p
ddot = 3kd/2
C = 6k² - p² - 2d² = 0.
```

These are the requested equations with `mu=0`. Here `p` is the scalar's
proper-time derivative and `d²` is the comoving dust's energy density.
Define

```text
V = B^(-3),   U = Vdot = -3kV,
P = pV,       D = d²V.
```

The source equations make `P,D` constant. Direct substitution gives

```text
Vdot = U,    Udot = 3D/2,
I = U² - 3DV - 3P²/2,
C = 2I/(3V²).
```

The exact proper-time step is consequently polynomial:

```text
V_next = V + hU + 3Dh²/4
U_next = U + 3Dh/2.
```

It has exact inverse obtained by replacing `h` by `-h`, preserves `I`, and
composes as `R_j R_h = R_(h+j)`. This is the exact flow in this sector,
not a first-order numerical approximation. No physical time is relabelled
to improve agreement.

The cosmological solution itself is established physics. Chavanis,
[*Cosmology with a stiff matter era*](https://arxiv.org/pdf/1412.0743),
section V.B, equations (38)–(40), gives the stiff-matter/dust solution
without a cosmological constant; equation (39) makes the volume quadratic
in proper time. That section was inspected directly. A homogeneous free
scalar has the stiff equation of state used here. The contribution of this
work is the complete-state fixed-six encoding and its checked interface,
not a new Friedmann solution. The formulas and code identities below were
derived directly for the repository's normalization.

## The full physical decoder, including scalar phase

Let `s=sqrt(3P²/2)`. The selected physical domain is

```text
D>0, P!=0, V>0, U>s, Uref>s, I=0.
```

Positive dust amplitude is the selected branch. The scalar reference values
`Uref` and `phi_ref` are **retained constant channels**. The current physical
fields are

```text
B = V^(-1/3)
k = -U/(3V)
p = P/V
d = sqrt(D/V)
phi = phi_ref + (P/s) log[ ((U-s)/(U+s)) / ((Uref-s)/(Uref+s)) ].
```

Since `U²-s²=3DV` on the physical constraint, differentiating the last
expression gives `phidot=P/V=p`. Changing the retained phase anchor changes
the decoded scalar phase. Changing only the coordinate tick does not change
any physical field. Thus this is a present-state coordinate map; it neither
looks up future answers nor reconstructs fields from an elapsed-time
trajectory table.

Square roots, the cube root and logarithm are mathematical parts of the
passive observable map. Numerical display uses explicitly requested
high-precision evaluation. They are not integer Engine operations, and
the displayed irrational values are not claimed to be exact rational
registers. The physical proof is symbolic; numerical print precision is
reported separately. `k,p,d²,B³` and the constraint remain exactly rational
readouts.

The numerical phase reader evaluates the anchored logarithm with exact
rational branch products and the exact rational difference `U-Uref`, then
uses `log1p`. It never subtracts rounded `U-s` values or forms a rounded
ratio near one. Controls compare 80 with 160 digits for a rational point
within `10^-120` of the branch boundary, a nonzero phase of order `10^-301`,
and a 90th-power Pell preparation with `U²-3P²/2=1`. The initial anchored
Pell phase is exactly zero; its advanced phase remains finite and positive.

The scalar integration constant cannot in general be stored as one rational
number `phi-F(U)`, because `F(U)` is logarithmic. Keeping both the rational
reference velocity and reference phase avoids hiding that information in
the decoder. The current integer preparation restricts `D,P,phi_ref` to
integers in the declared units and requires the scaled volume/velocity
to be integral. It does not encode every arbitrary real initial datum.

## Why the actual Rule3 map implements this flow

For static resolution `N>0`, let `h=1/N` and retain

```text
q = 4N² V,
J = b_volume-a_volume+3D = 4NU.
```

The one immutable volume input is

```text
u_volume = 6 b_volume + 18 b_dust_charge.
```

All other channel inputs are `u=6b`. Prepare each source/reference/offset
channel with `a=b`; prepare the coordinate tick with `a=b-1`. Every input
is a multiple of three, so all six valid remainder values remain retained
and unchanged. The actual mandatory-history update becomes

```text
q_next = 2q-q_previous+6D = q+J+3D
J_next = q_next-q+3D = J+6D.
```

Dividing by the static scales gives exactly the proper-time map above.
The integer invariant is

```text
J²-12Dq-24N²P² = 16N² I.
```

For any pair `(V,U)` representable at the declared scales, its complete
volume history is uniquely

```text
b_volume = 4N²V
a_volume = 4N²V-4NU+3D.
```

Conversely that history recovers both `V` and `U`. The history is used as a
physical velocity coordinate, not discarded or reset. On the fixed source
and reference graph this is an invertible coordinate change on the allowed
integer grid; it is not a compression theorem for the full 45-field model.
All frozen remainder labels remain present in the complete mechanical state.

This is why the independently-null-target-minus-null-history obstruction
from `temporal_handoff.md` does not apply. The retained volume registers
are not separately null four-vectors. The physical constraint is an
identity of the **complete history** through `J`, rather than a constraint
imposed on `b` alone.

The complete allocation is:

| Channel | Retained role |
| --- | --- |
| `volume` | Present/past volume; their difference carries `U` |
| `dust_charge` | Constant `D=d²V` |
| `scalar_charge` | Constant `P=pV` |
| `reference_velocity` | Constant `4N Uref` for scalar phase |
| `scalar_offset` | Constant `phi_ref` |
| `proper_tick` | Proper-time coordinate counter in units `1/N` |

There are **six channels, 18 retained integer entries per node, seven
degree-one monomials**, no workspace or scheduler bank, and no runtime
callback. The tensor is the same at every tested resolution; `N` changes
the exact preparation/readout scales. The proper-time counter is a
coordinate counter for this unit-lapse solution, not an independently
calibrated operational clock apparatus.

## Exact Einstein and source identities

`physical_map.symbolic_audit()` verifies all five differential equations
in the same proper time and the exact identities

```text
Cdot = 6k C
C_next = C (V/V_next)²
rho = P²/(2V²) + D/V
pressure = P²/(2V²)
rho_dot + 3H(rho+pressure) = 0,   H=-k.
```

The separate `metric_curvature_audit()` constructs
`g=diag(-1,V^(2/3),V^(2/3),V^(2/3))`, computes its Christoffel symbols,
Ricci tensor, scalar curvature and Einstein tensor, and subtracts the
homogeneous scalar/dust stress. All 16 component identities are checked:

```text
G00-T00 = I/(3V²)
Gii-Tii = I/(3V^(4/3))
Gmunu-Tmunu = 0 for mu!=nu.
```

Thus all Einstein components vanish exactly on `I=0`. This is stronger
than observing one scalar constraint, and the curvature calculation does
not call the production frame RHS.

The scalar source influences the geometry through the constrained
integration constant: `U²=3DV+3P²/2`. `P` need not appear again as a
separate force term in the constant-acceleration volume coordinate.
Changing `P` alone at fixed `V,U,D` generally leaves the physical
constraint surface and is rejected as a physical interpretation. This
does not supply a spatial scalar-gradient interaction or general source
backreaction outside the stated homogeneous sector.

## Reproduction and present evidence

```bash
python -m validation.sourced_map.physical_map
python -m validation.sourced_map.native
```

The physical-map audit imports the actual native tensor, prepares complete
states and runs the unchanged Engine for 3, 6 and 12 steps at `N=24,48,96`.
At **the same proper time `T=1/8`**, all three runs give exactly

```text
V = 355/256, U = 51/16, P=2, D=1, I=0.
```

All intermediate decoded maps equal the independent rational target, all
step inverses and complete rewinds pass, and all three decoded endpoints
agree at the requested 80-digit evaluation precision. Representative values:

| Field | At proper time 1/8 |
| --- | ---: |
| `B` | 0.89674824916111762018 |
| `k` | -0.76619718309859154930 |
| `p` | 1.44225352112676056338 |
| `phi` | 0.21170443766110203839 |
| `d` | 0.84919182789484042567 |

These 21 Engine steps overlap the native and independent-oracle audits;
they are not counted as additional disjoint physical trials. Agreement
across resolution is exact sampling of an integrable restricted flow,
not evidence of convergence of a general discretized Einstein solver.

The source-hashed physical proof/readout evidence is
`runs/sourced-map/physical_map.json`. The native audit separately supplies
the complete tensor, seed, trace, all-carry/scalar-oracle checks, held-out
sources, raw bit counts and exact source-disconnection controls.

The physical decoder rejects massive relabelling, nonzero exact constraint,
nonpositive volume, zero scalar charge, contracting data and an invalid
scalar anchor. A negative scalar charge is supported: it reverses `p,phi`
while preserving geometry and dust. Pure dust, zero dust and contracting
analytic controls are outside this selected implemented chart. No physical
acceptance is inferred for them from a separate formula.

## Remaining boundary

For `mu!=0`, `Pdot=-mu*phi*V`; the conserved-charge volume construction is
not the requested massive system. Homogeneity also removes the spatial
gradients, shear, momentum constraints, gauge dynamics and transport needed
for the full frame theory. The present decoder requires its complete
declared branch and homogeneous preparation, including the previous
physical slice. An inverse crossing a big-bang boundary remains a valid
integer operation but leaves this physical chart.

The progress is an implemented, constrained, nonzero-source Einstein sector
whose mandatory memory has a physical role. Extending it to a massive or
spatially varying common model requires a new invariant-compatible map;
the unchanged historical failure controls remain relevant. No general GR,
physical detector, Born/Bell or complexity-growth claim follows from this
restricted success.
