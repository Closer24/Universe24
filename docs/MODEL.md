# Fixed-divisor Rule3 algebra

> Historical research/reference document. The current supported interface and acceptance status are defined in [ONE_SYSTEM.md](ONE_SYSTEM.md). Commands and default-model descriptions below refer to the earlier construction; see [the 0.6 migration](MIGRATION_0_6.md). No general ≤48-channel physical model is accepted.


The 0.5.0 consolidation adds disjoint channel ownership, local communication and explicit probe experiments; see [UNIFIED_SYSTEM.md](UNIFIED_SYSTEM.md) and [fresh validation](evidence/universe24_unification.json). The physical Einstein metric remains the sole metric of the main event board.

## Integrated Einstein event board

The default is now `python -m universe24`: nonlinear ADM, complex scalar matter with opposite U(1) charges and geodesic dark dust. All updates use the fixed-six Engine; the metric, stress and event records come from the same retained state. See [equations](INTEGER_ADM.md), [events and matter conventions](UNIVERSE24_EVENTS.md), and [commands](../README.md).

The reference baseline and fixed-six research results below remain controls; they no longer describe the CLI default. Retired variable-divisor calibrations stay retired.

The optional [compact null-wave sector](COMPACT_NULL_WAVE.md) stores a prepared
pp-wave profile in two retained integer channels and decodes its coframe with
a fixed null covector. Its invariant-sector proof includes both histories and
frozen remainders. It is a separate model with passive fixed-denominator
geometry readouts, not a replacement for the default ADM metric.

The [Frame48 candidate](FRAME48_RESEARCH.md) adds a horizon-independent,
48-channel exact lift of a nonlinear vacuum-frame time stencil. Its general
constraint, nondegeneracy, refinement and physical-clock gates remain false.
It is an explicitly separate research model with a published source ledger.


This is the current mathematical contract for the executable model. A node's
state, a fixed integer coupling tensor, and the complete seed specify a run.
The scalar divisor is the constant six. There is no adjustable divisor scale,
per-channel numerator/denominator, hidden arithmetic rescaling, or second
state-update rule.

### A0. Overview: what the algebra does

Write the full state as `S_n=(a_n,b_n,r_n)` and augment the old register vector
with a constant component, `v_n=(1,b_n,a_n)`. The fixed tensor supplies a local
integer polynomial `u_n=T(v_n,v_n,v_n)`, with unused input slots represented
by the constant component. The one evolution map and passive observation are

    S_(n+1) = W_T(S_n),       O_n = Theta(S_n,S_(n+1)).

The tensor and seed are construction choices. They are not derived from the
scalar recurrence alone. The reference cube block and the geometric examples
are possible constructions, not necessary models of nature.

### A1. Space, registers and degrees of freedom

The implemented storage lattice is a periodic cubic graph with six face
neighbors. At each node `x` and gear type `i`, retain

    S_(x,i) = (a_(x,i), b_(x,i), r_(x,i)),
    a,b in Z,       r in {0,1,2,3,4,5}.

For `G` gear types, a node has `2G` unbounded signed integer registers and `G`
six-state remainders. Signed integers can be stored as natural numbers via
`z -> 2*z` for `z>=0` and `z -> -2*z-1` otherwise; this is an injective
encoding, not an extra update. The old and current histories `a,b` are not independent
physical boards by definition. Interpreting them as two interacting boards
requires a separate construction and observation map.

Since the incoming numerator is even, each remainder's parity is invariant.
After choosing that parity, its accessible remainder alphabet has three
values. This is a sector restriction, not an additional coordinate.

The graph is closed by periodic boundaries. That does not imply that every
continuum coordinate chart assigned to its samples is globally periodic or
satisfies physical field equations across the seams.

### A2. Cube rotations, quaternions and reflections

The proper rotations of the cube form a group of order 24. Unit quaternions
act on spatial vectors by `v -> q v q^-1`; opposite quaternions give the same
spatial rotation. Lifting the cube rotations gives the binary octahedral
group `2O`, with 48 elements. Quarter-turn generators may be written

    q_x=(1+i)/sqrt(2), q_y=(1+j)/sqrt(2), q_z=(1+k)/sqrt(2),
    i^2=j^2=k^2=ijk=-1.

These formulas construct fixed algebraic matrices. The runtime register
values remain integers; it does not update floating quaternion components.
The 48-element double cover is not the 48-element cube group obtained by
adding spatial reflections. A reflection convention and its action on the
state must be specified separately.

### A3. The 48-channel reference block and its matrices

The reference block labels one channel by each element of `2O`. Multiplying
a group label gives a fixed permutation of the 48 coordinates. Neighbor
transport is represented by six fixed integer matrices `P_d`, each 48 by 48,
with the selected signs and direction conventions supplied by the builder.
The current default uses `body_signs=(1,-1,1)`, 288 nonzero linear terms
and actual tensor order two; the format also permits order-four examples:

    u_x = sum_(six directions d) P_d b_(x+d).

The matrices specify which channel at a face neighbor contributes to a local
channel. Opposite directions, sign choices, reciprocity and rotation
covariance are properties to verify for the chosen matrices. Merely naming
the group does not prove them for every coupled tensor.

The same coupling may be stored sparsely as nonzero matrix/tensor entries.
That storage choice does not add a lookup-dependent update law. The global
operator is assembled from these local blocks and the six spatial shifts;
a node never evaluates a dense global matrix.

### A4. Representations and the role of an ideal

The complex regular representation decomposes into irreducible group
representations. Appropriate linear readouts can therefore transform as
scalars, vectors, tensor components or spinorial representations of this
finite group. These are transformations of a shared integer state, not four
different scalar update rules. They do not by themselves establish photons,
fermions, continuous Lorentz symmetry or quantum statistics.

The group ring can be described by generators `[g]` with `[g][h]=[gh]`.
Equivalently, a two-sided ideal imposes the relations

    X_e-1=0,       X_g X_h-X_(gh)=0.

An ideal identifies algebraic expressions representing the same group
operation. It does not authorize deleting distinct dynamic states or division
remainders. A prepared invariant sector may also be expressed by polynomial
relations; its preservation must be proved under the full update and inverse.

### A5. One fixed polynomial coupling tensor

For each output gear, the input is

    u_(x,i) = sum_m c_m product_(f in m) v_(x+offset_f, gear_f),
    c_m in Z,       number of input factors <= 3.

This is an order-at-most-four tensor when the output index is counted. It is
not the rank-four Riemann curvature tensor. Its entries remain fixed during
the run. An effective link strength may depend on evolving registers because
the polynomial contains products; that is different from replacing tensor
entries at runtime.

Every monomial reads only its target node and at most one face neighbor.
For physical link gears, both geometric endpoints must be counted when
checking strict single-edge support. Storage-local reads alone are not a
proof of that stronger condition.

Old-`a` reads are permitted only when their gear dependency graph is acyclic.
All forward inputs still read one complete old snapshot; the ordering is
used by the inverse, not by the forward loop.

### A6. The single scalar operation

At every node and gear, use the same Euclidean division:

    ell, r_next = divmod(2*u+r, 6)
    a_next = b
    b_next = ell-a

Equivalently,

    2*u+r = 6*(b_next+a)+r_next,       0 <= r_next < 6.

The convention also applies to negative input. All intermediate values,
quotients and remainders are exact integers. There is no adjustable divisor
argument in the engine or tensor. The previous variable-divisor models are
superseded; their calibrated predictions do not automatically transfer to
this law. See the [migration note](DIVISOR_AUDIT.md).

### A6a. Exact inverse and the distinction from a mirror

Recover old `b=a_next`. In the validated dependency order, evaluate each old
input using the recovered old `b` and any earlier recovered old `a`, then set

    r = (r_next-2*u) mod 6,
    a = (2*u+r-r_next)//6 - b_next.

The division is exact. This recovers the full retained state. Invertibility
is not boundedness, physical energy conservation or a proof of a preferred
arrow of time. For b-only inputs, `M(a,b,r)=(b,a,5-r)` is a reversor; that
particular mirror need not apply to general old-history couplings.

### A7. Node code and connection to the rest of the board

The elementary operation is

```python
def rule3(a, b, r, u):
    quotient, remainder = divmod(2 * u + r, 6)
    return b, quotient - a, remainder
```

The shared engine first evaluates the fixed local tensor from the old
snapshot, then applies this operation componentwise. Preparation constructs
the graph, tensor and complete integer seed before the first update.
Observers read histories and never inject state, choose branches, reset
clocks or alter links between updates.

### A8. What remains free

The model designer chooses the number and interpretation of gear types,
the allowed graph and boundary conditions, fixed integer tensor entries,
and the initial `a,b,r` arrays. A decoder and any physical-unit calibration
must also be declared. They are not hidden dynamic variables.

There is no independently chosen `num/den` for a channel. Effective families
with other coefficients are hypotheses about collective or retimed dynamics.
An exact claim needs an injective encoding `E` and a fixed number of steps
`m` satisfying `W_T^m E = E F` on a declared invariant sector, including all
retained information required for reversal. Matching one frequency is weaker.

### A9. What a click means in the code

An official click is a passive record with nonzero quotient when the complete
local triple changes, subject to its declared observation label. For the
remainder increment modulo six, classes distinguish zero, positive and
negative turns. They do not select the next state.

An absent record does not always mean the quotient was zero: a nonzero
stationary triple can have a nonzero quotient and no click. Reconstructing a
state from clicks therefore needs a proved decoder and its declared initial
information. The [geodesic example](PPWAVE_OPERATIONAL_ROUTE.md) makes this
restriction explicit.

### A10. Balances, clocks and stability

The quotient-remainder ledger is exact by construction. A physical charge,
energy or stress balance needs its own definition and proof for the selected
tensor. Reciprocity can be checked as the existence of a polynomial potential,
but it is not sufficient to establish Einstein constraints or physical energy.

Periodic registers, transported patterns and prepared interacting cycles can
serve as clock candidates. A finite return of the complete state proves
repetition of that orbit, not stability for all seeds. Unbounded integer
orbits remain possible even under an invertible rule.

A score on a closed periodic orbit cannot increase strictly at every step.
A proposed complexity-oriented selection mechanism must retain the information
needed for reversal and define how observable outcomes follow from the state.
No such physical collapse or global optimization law is supplied by Rule3 alone.

### A11. Retained constructive examples

The [bounded circuit](BOUNDED_CIRCUITS.md) realizes routing and periodic clocks
on a proved Boolean sector. The [integer reciprocal examples](INTEGER_RECIPROCAL_GEOMETRY.md)
show prepared coupled cycles and explicit instability controls.

The [local pp-wave example](PPWAVE_PALATINI_LOCAL.md) transports a chosen
nonflat vacuum metric sector and checks exact interior geometric residuals.
Its periodic chart seams fail those equations. The [geodesic extension](PPWAVE_OPERATIONAL_ROUTE.md)
encodes selected one-axis worldlines at a carrier node, with exact calibrated
readouts. It does not yet produce a packet moving on board links, universal
clocks or matter backreaction.

Each construction must be validated under the fixed-six engine. Historical
large-divisor run records are not evidence for the migrated construction.

### A12. Physical acceptance requirements

A common spacetime metric must be inferred consistently from local clock
comparisons and signal propagation, and predict other test bodies without
species-specific fits. Geodesic motion is not enough: the metric must obey
a stated source equation and preserve its constraints. A coordinate chart,
local graph or set of tensor-named counters does not establish Einstein space.

Quantum claims separately require observable probabilities, interference,
contextuality or Bell-test consistency under stated assumptions, and appropriate
scaling of the state space. No reference to a finite group, complex readout,
reversible branch or click alone proves those properties.

### A13. Validation and source of truth

The executable tensor, complete seed, scalar engine and declared decoder are
the reproducible specification. Compare complete states, inverse results,
local support and event records. Keep exact theorems, finite run evidence and
physical hypotheses separate. See [validation](VALIDATION.md) for commands and
current scope; superseded record files must not be promoted by wording alone.
