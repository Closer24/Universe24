# A generic low-rank native schedule and its exact resource boundary

Agent 3 of this eight-agent round. Inspected base PR #52:
`8c53e69f4b466dcbd2da7dab7e3c365bd9731766`. Executable:
`validation/generic_structure/native_schedule.py`; raw evidence:
`runs/generic_structure/native_schedule.json`.

This extends the actual seven-channel nine-tick compiler. It changes no Engine,
supported model or physical acceptance gate. The new result is an exact
**low-rank drift plus polynomial-force compiler** with **n+r+3 channels**, where
n counts data coordinates and r counts quotient work channels. A concrete
two-field potential passes through the new interaction compiler into a
six-channel schedule and the unchanged Engine. An actual 44-data, rank-one
example fits 48 channels. It does **not** provide 44 independent kinetic drifts.

## 1. The precise reusable interface

For every data channel define the bijective boundary coordinates

\[
S_i=a_i+b_i,\qquad P_i=6a_i+r_i,
\quad a_i=\lfloor P_i/6\rfloor,\quad r_i=P_i\bmod6.
\]

Choose construction-time integer matrices A of shape r by n and B of shape
n by r. Prepare r work triples `(0,0,kappa_k)` with legal remainders, and
three scheduler channels with zero a,b and arbitrary legal remainders.
All scheduler phases initially agree across nodes. No phases are supplied
again during a run.

Given any static node-field force polynomial F of degree at most two with
strict single-face support, one immutable tensor implements, every nine ticks,

\[
Q_k=\left\lfloor\frac{2\sum_i A_{ki}a_i+\kappa_k}{6}\right\rfloor,
\qquad S^*=S+BQ,
\]
\[
P'=P+2F(S^*),\qquad S'=S^*.
\]

All workspace and scheduler triples return exactly to their prepared values.
Their remainders are retained and reused, not discarded. The matrices and F
are compiled into integer coefficients; no matrix operation, force callback
or quotient-by-three executes outside Rule3 during physical evolution.

For A=B=I and kappa in {0,1}, Q_i=floor(a_i/3)=floor(P_i/18), recovering
the old two-field seven-channel macro map. For general A the correct formula
is the one above: rounding a sum is not the sum of rounded values. The compiler
does not mislabel it as B floor(AP/18).

The inverse is explicit: read S', recover P=P'-2F(S'), recover old a=floor(P/6),
then subtract B floor((2Aa+kappa)/6) from S'. This establishes the boundary
bijection in the prepared schedule domain. The existing Engine inverse also
works on complete legal off-domain states; their evolution need not follow
this special macro formula.

## 2. Why one work channel can serve many fields safely

The existing two clocks are c=fast and z=slow. Their equations are unchanged:

\[
u_c=3-3b_c,\qquad
u_z=-3b_z+b_c(9b_z+3)+3a_cb_z.
\]

Replace the former one-work-per-data equations by

\[
u_{w_k}=-3b_{w_k}
-b_c(1-2a_z+b_z)\sum_i A_{ki}(a_i+b_i),
\]
\[
u_{d_i}=-3b_{d_i}-3a_ca_z\sum_k B_{ik}b_{w_k}
+b_tF_i(-b_d).
\]

The materialized pulse t is the existing retained channel, with

\[
u_t=3(2a_ca_z-2a_cb_z+a_c-b_cb_z+b_z).
\]

Its b is one only at phase seven and zero at the other eight phases. The
argument `F(-b_d)` means that each force monomial receives coefficient
(-1)^degree at construction. At phase seven, b_d=-S*. Thus constants and
linear forces, as well as the previous homogeneous quadratic forces, are
supported without changing the physical force sign.

The nine-tick proof follows the original three-block schedule:

| Block | Workspace action | Data action | Information retained |
| --- | --- | --- | --- |
| First three ticks | Compute each linear-combination quotient from A a | No boundary change | Quotient and exact carry in its work triple |
| Second three ticks | Retain quotient | Add BQ to S while preserving boundary a and r | All source a values remain recoverable |
| Final three ticks | Uncompute using the same source A a | Apply force at phase seven | The force and uncompute read the same old snapshot |

The source boundary a is unchanged until the uncompute's last source read.
The force cannot overwrite that read: Rule3 evaluates both outputs from the
same complete old state. Linear combination in the work equation is safe
because no product joins two different sources. Copying the quotient to
several S coordinates is a reversible shear: the source quotient and data
momentum remain available for inversion.

After expansion all scheduler/work terms have degree at most three and are
onsite. Force terms gain only one pulse factor, so degree at most two becomes
at most three without extending the face support. An old-a ordering is
fast, slow, data, work, with pulse after its clock dependencies. Data reads
work **b**, so the reverse old-a edge that would create a cycle is absent.

This proves reuse of a shared linear-combination quotient across several
targets, and reuse of fully restored workspace across periods. It does not
construct an arbitrary serial field-address selector.

## 3. Exact count and a restricted lower bound

| Allocation | Channels | Retained integer entries |
| --- | ---: | ---: |
| Data | n | 3n |
| Quotient work | r | 3r |
| Two clocks and one materialized force pulse | 3 | 9 |
| Total | n+r+3 | 3(n+r+3) |

Both histories and every carry are counted inside these triples. There are
no link registers, hidden banks, host schedule state or saved physical answers.
The returned compiler certificate counts all ownership, checks integer matrix
entries, reports ranks and validates the actual immutable tensor's degree,
physical support and old-a dependency graph.
The optional requested budget may tighten the cap but cannot raise it beyond
48; noninteger and Boolean budget values are rejected.

For this specific concurrent compute-copy-uncompute layout, r>=n is necessary
to reproduce all n independent quotients floor(a_i/3) for arbitrary integer a.
The proof is exact and finite. Set a=3 e_j. Since A is integer and
0<=kappa_k<6, the computed Q equals A e_j. Matching the desired drift e_j
requires BA e_j=e_j for every j, hence BA=I_n and rank(BA)=n<=r.
The matrix condition is necessary, not sufficient for all rounded inputs.

Therefore the direct 44-field identity compiler requires 44+44+3=**91**
channels. The existing implementation's bound of at most 22 independently
drifting coordinates within 48 follows. This is not a universal lower bound
for reversible encodings, different canonical variables or longer schedules.

With r=1, 44+1+3=**48** is possible, and has been run. Its drift lies in the
one-dimensional image of B, even though all 44 data channels are retained and
can participate in force couplings. Calling that full independent 44-field
dynamics would be false. The scalar countercontrol a=(3,0), A=(1,1),
B=(1,1)^T produces drift (1,1), while the independent desired drift is (1,0).
It still rewinds: reversibility does not certify that a proposed allocation
implements the intended map.

## 4. One actual interaction-to-Engine path

The new interaction compiler supplies all endpoint responses from one
positive-x-face potential

\[
V=\sum_{(i,j)}(g_i+g_j)(\phi_j-\phi_i)^2.
\]

We pass Phi=-V to `interactions.compile_potential(..., add_inertial=False)`.
The generated tensor is therefore the pure force F=-dV, with field order
phi,g. The schedule adapter checks this interface instead of treating a
`6b+F` input as F. It reconstructs the pure gradient from the actual supplied
potential and actual gear metadata, then compares the actual canonical tensor
fingerprint. Mutable certificate labels and claimed hashes are not trusted.
It rejects old-a force reads, undeclared fields and cubic
forces. It also rejects physical link-channel metadata because this version
only implements a proved lift for node data; silently dropping such metadata
would invalidate physical-support checks.

For A=(1,1), B=(1,1)^T, the result uses **six channels**: two data, one
work and three schedule channels. The independent oracle differentiates V
directly on each incident edge:

\[
F_{\phi_i,ij}=2(g_i+g_j)(\phi_j-\phi_i),\qquad
F_{g_i,ij}=-(\phi_j-\phi_i)^2.
\]

The neighboring phi force has the opposite sign. The oracle checks the
generated force before constructing each expected macro state. The actual
Engine preserves the exact boundary sum of P_phi. This is a uniform phi-shift
charge, not identified spacetime momentum or total physical energy. The
stiffness variable g is not established as an Einstein metric.

The complete path is executable, not a collection of unrelated comparisons:

`local potential -> all generated forces -> checked force port -> one six-channel tensor -> Engine -> independent macro/charge checks`.

## 5. Executed controls

Run from repository root:

```bash
python -m validation.generic_structure.native_schedule
```

The JSON retains each complete tensor, seed, all microstates, compiler
certificate, source hashes and bit growth. All cases use 27 nodes with signed
initial data and all six data/scheduler remainders. Work remainders are either
all six or the explicitly declared unbiased {0,1} sector.

| Case | Channels | Macro periods | Scalar register comparisons | Macro register comparisons | Maximum bits |
| --- | ---: | ---: | ---: | ---: | ---: |
| Generated cubic potential through six-channel schedule | 6 | 3 | 13,122 | 1,458 | 16 |
| Signed linear-combination drift with constant, linear and quadratic forces | 7 | 3 | 15,309 | 1,701 | 11 |
| Identity-factorization old two-field map | 7 | 3 | 15,309 | 1,701 | 16 |
| 44 data plus rank-one workspace | 48 | 2 | 69,984 | 7,776 | 4 |

Every microstep agrees with an independent scalar polynomial/Rule3 evaluator,
every microstep inverse passes, each complete macro matches the independently
calculated map and inverse, all work/scheduler triples restore, and all full
rewinds recover the seed. These short runs certify the arithmetic identities;
they do not establish long-time stability.

Failure controls retain rejection of 91-channel direct allocation, caller
attempts to raise the hard cap, Boolean budgets, quartic
gated force, two-face product, inexact matrix coefficient, nonzero work
preparation, mismatched clock phase, an added selector on an already cubic
copy term, and the actual stable native-wave monomial multiplied by a pulse.
The shared-work wrong-map counterexample remains an explicit failure of the
claimed independent drift. Four cross-module controls reject an inertial
baseline in the pure-force port, an inertial tensor with forged pure-force
certificate labels/hashes, a changed potential paired with the unchanged tensor,
and a quartic potential whose cubic force would need a quartic gated monomial.

## 6. What serial reuse and the stable wave still require

A logically safe serial reuse would compute one quotient, copy it, uncompute
it, then process another source while all needed source momentum values remain
unchanged. A force kick before the last source has been uncomputed changes
that argument; it must either be postponed or explicitly accounted for in a
different splitting map. The current fixed clock does not select arbitrary
field indices. Simply multiplying its cubic copy term by a new retained
selector is degree four and is rejected. A materialized longer schedule might
work, but every address, pulse and history register must be included in a new
proof and allocation.

The stable native wave in `completion/time_stability.py` uses a period-four
sign and degree-three terms `s_a*s_b*b_neighbor`. The present scheduler has
nine phases and different data coordinates. Appending a pulse to the actual
wave monomial produces degree four; sharing its sign with a different clock
would change the law. Its stability/refinement theorem therefore does not
transfer to this compiler. The reusable boundary is a static degree-at-most-two
force port, not a license to concatenate arbitrary already-gated tensors.

Next progress requires either a lower-dimensional physical kinetic sector
with a justified mass/constraint structure, or a proved longer internally
addressed schedule for independent drifts. Neither a different field basis
nor a canonical-pair compression of corrected45 is assumed here. Nonlinear
Einstein constraints, general refinement, positive geometry and operational
clocks remain open.
