# Integer reciprocal geometry candidates

These optional experiments keep the scalar engine unchanged and set **Q=1,
D=6**. Tensor coefficients, complete initial states, intermediate inputs,
quotients and remainders are integers. There are no fractional registers or
floating-point seed calculations. Each run fixes its tensor before its first
update. The examples establish particular interactions and obstructions,
not Einstein gravity. They do not replace the default model.

## 1. The only update

Every gear executes

```python
quotient, r_next = divmod(2 * u + r, 6)
a_next, b_next = b, quotient - a
```

The fixed integer tensor supplies u from the old snapshot. Each input
monomial has at most three factors and touches the target node and at most
one face neighbor. All these constructions are b-only, so the inverse
first recovers b=a_next and then recovers every old r and a directly. The
code checks the exact division ledger and complete-state rewind; an
independent input oracle also exercises arbitrary-precision integers.

A polynomial potential is used only to construct and check the fixed tensor.
No potential minimizer, extra force update, projection or click callback runs
between Rule3 steps. A reciprocal derivative relation does not establish
physical stress conservation or preservation of gravitational constraints.

## 2. A bounded interacting clock with an exact proof

Two local gears e and chi use the chosen potential

```
Phi = 2(e^2+chi^2) - e^2 chi^2,
u_e = 4e - 2e chi^2,
u_chi = 4chi - 2e^2 chi.
```

Both inputs are cubic integer polynomials, hence the coupling tensor has
order four. Prepare both gears with (a,b,r)=(-1,-1,0). Their equal triples
follow exactly

| Update | a | b | r |
|---|---:|---:|---:|
| 0 | -1 | -1 | 0 |
| 1 | -1 | 0 | 2 |
| 2 | 0 | 1 | 2 |
| 3 | 1 | 1 | 0 |
| 4 | 1 | -1 | 4 |
| 5 | -1 | -1 | 0 |

The entire retained state returns after five updates. Determinism therefore
proves repetition for all time on this orbit, with |a|,|b| at most one.
The signed official quotient sequence for either gear is (-1,0,1,0,0),
where absent event samples are zero. These are actual passive event records,
not a mechanism that selects the orbit.

Same-tensor controls change only one gear's initial values to zero. The
other gear changes at the first update, demonstrating both directions of
coupling. The chosen readout gamma=1+e^2 is always one or two on the joint
orbit, but it has no established operational metric interpretation. The
example has no spatial transport, geodesics or Einstein constraints, and
proves no bound for arbitrary initial states.

## 2a. The same period with genuine spatial coupling

A stronger two-gear example uses all six neighbors and the potential

```
Phi = sum_x (3e_x^2+7chi_x^2)
      - sum_undirected_edges_xy (1+e_x^2+e_y^2)(chi_y-chi_x)^2.
u_e = 6e - 2e sum_neighbors (chi_y-chi)^2,
u_chi = 14chi + 2 sum_neighbors (1+e^2+e_y^2)(chi_y-chi).
```

It produces a 40-monomial order-four tensor with strict single-edge support
and unsigned reciprocity. Its link coefficient K_xy=1+e_x^2+e_y^2 is always
a positive integer, even outside the prepared orbit. No link is inserted
or removed during evolution.

On the periodic L=4 board, set f(x)=(1,0,-1,0) along the x axis, independently
of y,z. Prepare a_e=b_e=-1, r_e=0, a_chi=b_chi=-f(x), and r_chi=5 where
f=-1 and zero elsewhere. The previous and current profiles remain
e=q and chi=q f. Indeed, sum_neighbors(chi_y-chi)^2=2q^2 and the
nearest-neighbor Laplacian of f is -2f. Hence

```
u_e = 6q-4q^3,
u_chi = (10-8q^2)q f.
```

On q in {-1,0,1}, these inputs reduce to 2q and 2q f. For f=1 this is
exactly the five-state cycle above. For f=-1 the counters have opposite
signs and the remainder is 5-r, using the integer identity

```
divmod(-2u+5-r,6) = (-quotient,5-r_next).
```

For f=0 the chi triple stays zero. Thus the entire spatial state returns
after five steps, and all counters stay between -1 and 1 for all time on
this orbit. The link coefficients alternate between one and three. Official
event counts per cycle are (96,0,96,0,0). Same-tensor controls that remove
either initial field change the other field's official origin record at
the first update. The spatial interaction is active, not merely a label
assigned to independent clocks.

This is a prepared standing pattern, not a travelling packet or a measured
spacetime metric. The same tensor has a rigorously unbounded control:
prepare e=0 and uniform chi with a=b=1,r=0. All edge differences vanish,
so u_chi=14b. Whenever b>=a>=1, the quotient is at least 4b and
b_next>=3b for every allowed remainder. Induction proves exponential growth.
A positive link coefficient and a bounded orbit therefore do not imply
general stability or Einstein geometry.

## 3. Completing the spatial interaction exposes a constraint failure

The 21-gear edge candidate uses the previous tensor-curl block, two phase
gears and one matter gear. Its additional potential is

```
Phi_int = sum_positive_xy_edges sigma_i (F_x+F_y)(chi_y-chi_x)^2,
F = c(E00-E11)+s(B01+B10),  sigma_x=1, sigma_y=-1.
```

Differentiating all factors supplies both the matter response and the
metric/phase response. The resulting 190-monomial tensor has order four,
strict single-edge support and full reciprocity with no one-way exemptions.
Initial-only controls change the opposite sector after one update. Actual
official matter records are selected separately from audit-labelled metric
and phase records.

Generic transverse matter breaks the raw transverse-traceless (TT)
divergence constraint at the first step. A special even-board checkerboard
preparation preserves the algebraic TT form, with complementary remainders
for opposite-valued counters. However, its phase decoding and former metric
translation identity fail at the first update, and its peak counter needs
328 bits by update five. It remains exactly reversible. This is a rejected
general gravitational completion, not a stable sourced metric.

The [constraint analysis](DYNAMICAL_GEOMETRY_CONSTRAINTS.md) proves why
reciprocity alone does not solve the problem, and describes the narrower
checkerboard invariant set precisely.

## 4. Local flux registers permit an off-diagonal response

The second spatial candidate stores a scalar f and three independent node
fluxes j_i for each of two matter species and six symmetric metric labels
H_ij. It has 32 gears. For every species its free inputs are identical:

```
u_f = D f + g sum_i delta_i j_i,
u_ji = -D j_i + g delta_i f,
delta_i = S_plus_i - S_minus_i,  D=6, g=1.
```

The construction potential is

```
Phi0 = sum_species [3(f^2+sum_i j_i^2) + f sum_i delta_i j_i],
Phi_int = sum_matter [sum_i Hii ji^2 + 2 sum_i<j Hij ji jj].
```

It uses signed reciprocity: s_f=+1 and s_ji=-1. These signs are compiled into
the fixed coefficients; they are not an engine branch or an assertion of
positive physical energy. Differentiation yields a local source for H and
the matter-flux response -2 sum_j H_ij j_j. All 158 monomials have degree at
most two. The order-three tensor can be padded with a constant input to fit
the order-at-most-four convention.

The product Hxy jx jy is wholly on-site. Neighbor terms carry only the
separate scalar/flux differences, so the construction satisfies strict
single-edge support. The j variables are independent node registers,
not gradients evaluated from two different neighbors and not physical link
registers hidden by metadata. Their additional freedom is part of this
chosen state space.

The same-tensor integer controls have a concrete response. Initial matter
flux (3,6,0) at one site produces new metric counters (H00,H01,H11)=(3,12,12).
Adding only initial H01=1 changes the two matter flux counters by (-4,-2).
In the finite transport histories, the off-diagonal preparation changes
both declared scalar detectors' official records at update three. Diagonal
preparations change those detector records at update four. All runs rewind
exactly, including every remainder. No background is held fixed after the
seed; it also responds.

Identical complete free blocks eliminate the earlier mismatch between two
chosen free operators. They do not prove universal observed propagation.
In this candidate, H changes the matter-flux operator but does not impose
that same change on the metric-flux operator. Equality is therefore limited
to the flat background, not a common curved characteristic geometry.
The passive frozen-background calculation has spatial principal coefficient
(I+H/D)^(-1), relative to the common small-wave-number speed squared 1/9.
The corresponding covariant candidate would be I+H/D under that particular
calibration. These are analytical ratios, not stored fractional values or
an independently applied update. Carries and the evolving background remain
in the actual integer experiment.

This candidate also fails the full target: the displayed source has nonzero
trace and divergence, and the finite interacting runs grow rapidly. An
exact uniform auxiliary mode obeys b_t=(-1)^t t, proving unboundedness for
some preparations despite unit-modulus free mode multipliers. Lapse, shift,
Einstein source conservation, metric positivity and a stable constrained
sector have not been supplied.

There is a stronger frozen-background stability failure. For constant H
with positive eigenvalue h, a uniform matter flux in that direction has
input eigenvalue -D-2h, outside the remainder-free stable interval [-D,D].
For H00=1 and D=6 its formal characteristic equation is z+z^(-1)=-8/3.
This analytical control holds the background fixed; it is not the same as
the full reciprocal history, whose background responds as well.

## 5. Reproduce and interpret the evidence

```sh
python experiments/geometry/reciprocal_metric_candidate.py
python experiments/geometry/metric_transport_candidate.py
python experiments/geometry/exact_constraint_audit.py
```

The first spatial run defaults to five steps and the flux run to eight;
their growing fields are explicit failure evidence. Reports include source
and tensor hashes, integer preparation definitions, complete history hashes,
readout comparisons and inverse checks. Published reports are
[reciprocal candidate](evidence/reciprocal_metric_candidate.json),
[local flux candidate](evidence/metric_transport_candidate.json) and
[constraint audit](evidence/exact_constraint_audit.json).

The constraint audit is passive algebra, not a third dynamical model. It
checks exact Bianchi identities, a pointwise lattice-stress counterexample
and the periodic flat-background mean-source obstruction. A nonzero
positive total energy cannot source the specified flat linearized periodic
Einstein target. A dynamic homogeneous background or boundary contribution,
together with an appropriate conserved discrete source, is needed before
that target can describe such matter. No theorem here rules out every
possible integer Rule3 encoding of gravity.
