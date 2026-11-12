# One local interaction generates every response

Task 1 of the owner's eight-agent constructive investigation, 12 November
2026. Based on PR #52 at `8c53e69f4b466dcbd2da7dab7e3c365bd9731766`.
This is a source-only compiler and proof/audit. It does not alter the Engine,
add a supported physical model, or establish Einstein dynamics.

## Proposed primitive

Specify a translation-invariant polynomial **once**, then differentiate it
to generate every participating field's response, including the response
at the other endpoint of an edge. This replaces separately handwritten
forces with one checkable interaction definition.

Let the unit-cell polynomial be a sum of monomials

```text
Phi = sum_x sum_m c_m product_j b[g_mj, x+offset_mj].
```

Each monomial has degree at most four and occupies one physical node or one
physical face edge. A link field occupies both of its declared endpoints.
The compiler constructs

```text
u_i = 6 b_i + s_i dPhi/db_i,
```

where `s_i` is the declared field sign, normally +1. A negative sign requires
the existing `GearType` justification. Passing `add_inertial=False` omits
`6b`, exposing the pure response for another validated construction. For
the customary `-dV/db` convention, supply `Phi=-V`; no sign inference or
physical field naming is hidden in the compiler.

The preparation polynomial may have rational coefficients such as `q^4/4`.
The **complete derivative coefficients must be integers** after collection.
Fractions occur only in construction and in the independent audit; the
compiled tensor and all Engine evolution use exact integers.

## Compiler and certificate

The reusable API lives in
`validation/generic_structure/interactions.py`:

```python
from fractions import Fraction
from validation.generic_structure.interactions import (
    Variable, PotentialTerm, compile_potential,
)

p = Variable("phi")
q = Variable("chi", (1, 0, 0))
compiled = compile_potential(
    ["phi", "chi"],
    [PotentialTerm(Fraction(1, 2), (p, p, q, q))],
    owners={"phi": "shared_interaction", "chi": "shared_interaction"},
)
tensor = compiled.tensor
certificate = compiled.certificate
```

The compiler performs the following construction-time work:

1. Validate all declared channels, ownership and the complete 48-channel cap.
2. Include both endpoints of every link factor in physical-support checks.
   Normalize monomials by an irrelevant common spatial translation.
3. Differentiate every factor occurrence, preserving repeated-factor
   multiplicity. Move the chosen target's storage site to offset zero and
   shift the remaining factors by the same displacement.
4. Combine identical derivative monomials exactly, reject any noninteger
   coefficient, and optionally add the native inertial term.
5. Construct the actual immutable `Tensor(..., strict_support=True)` and
   run its full signed reciprocal-gradient check with no one-way exemptions
   and no old-a terms.
6. Return the normalized potential, actual tensor/fingerprint, degree and
   support results, and an exhaustive channel ledger.

The certificate is an inspectable record of those checks, not a claim of
physical acceptance or a cryptographic proof independent of its generator.
The independent scalar oracle below verifies the resulting derivatives
without reusing the symbolic differentiation implementation.

## Primitive theorem

For every accepted input polynomial and every periodic lattice with side
at least three, the generated tensor equals the declared signed derivative
of the global polynomial at every node.

To prove this, choose one occurrence of field `g` at offset `p` in one
monomial. Its contribution to the derivative at node `y` comes from the
unique translated term anchored at `x=y-p`. Removing that occurrence
leaves every other factor at offset `q-p` from `y`. The compiler emits
exactly this product with its original coefficient and target sign.
Summing all occurrences accounts for powers and multiplicities; summing
all unit-cell terms gives the complete derivative.

Differentiation reduces degree by one, hence response degree is at most
three. Reanchoring preserves physical support. Because the removed target
field's link endpoints remain included by the target metadata, the final
strict-support check also covers that case. No old-a factor is emitted,
so the inverse has one dependency stage. Integer coefficient collection
gives a legal unchanged fixed-six Engine tensor.

Mixed derivatives of the polynomial commute. Accordingly the signed force
Jacobian is symmetric; the repository reciprocity checker confirms the
same identity in its translation-normalized representation. Constant
responses arise from linear potentials and are explicitly counted; they
are not unreported exclusions. The native baseline has the signed
potential `3 sum_i s_i b_i^2`, so adding `6b_i` preserves the identity.

This theorem establishes the response and reciprocity, **not** exact
conservation of the potential, of an assumed total energy, or of Einstein's
constraints. A real rotation is never assumed to preserve the integer
lattice; the compiler only uses exact index translations and permutations.

## A stronger exact balance from an actual symmetry

Define the native retained momentum-like coordinate

```text
P_i = 6(b_i-a_i)+r_i.
```

The unchanged Rule3 update gives

```text
P_i_next - P_i = 2(u_i-6b_i) = 2 s_i dPhi/db_i.
```

If one field `psi` has sign +1 and the global polynomial is invariant under
the simultaneous additive shift `psi_x -> psi_x+c`, then differentiating
that polynomial identity in `c` gives `sum_x dPhi/dpsi_x=0`. Therefore

```text
Q_psi = sum_x [6(b_psi-a_psi)+r_psi]
Q_psi_next = Q_psi
```

**exactly, for every valid integer seed and every remainder class.** The
carry terms are retained in `Q`; no approximate division argument is used.
This is a global charge on the periodic graph associated with an internal
field shift. It has not been identified with physical spatial momentum,
energy or a gravitational constraint. Reciprocity by itself does not
imply this symmetry or this charge.

The executable charge example uses the shared polynomial

```text
Phi = -1/2 sum_edges (1+eta_x^2+eta_y^2)(psi_y-psi_x)^2.
```

Both `psi` and the nonuniform material `eta` receive the compiler-generated
response. The model uses two retained channels, **six retained integers per
node**, with no extra memory, link storage, clock or solver. Four actual
Engine steps preserve `Q_psi` and rewind completely. Independent scalar
potential evaluations verify four shifts, and an exact scalar derivative
oracle verifies the zero total `psi` force on the seed.

The balance is also local. For each oriented face edge define
`J_(x->y)=2(1+eta_x^2+eta_y^2)(psi_x-psi_y)` from the complete old snapshot.
Then `P_x_next-P_x=-sum_y J_(x->y)` and `J_(y->x)=-J_(x->y)` exactly.
The actual Engine audit checks **108 local balances** and, for an x=0 slab,
four regional charge changes equal to the inward boundary flux. These checks
use an independently written edge formula. Thus the global invariant is the
closed-boundary case of an explicit local storage-and-transfer identity.
The fourth slab exchange is already of order `10^50` for this unconstrained
seed. Exact balance therefore does not establish bounded dynamics or a
useful continuum regime; the large signed exchange is preserved in evidence.

A deliberately removed endpoint-response monomial leaves a legal reversible
local tensor, but fails reciprocity and changes `Q_psi` even when `psi`
starts spatially constant. Its exact nonzero defect is retained in the raw
evidence. Thus the successful balance depends on including the complete
interaction, not on the name given to the fields or the fact of rewinding.

## Actual Engine and rejection evidence

Run:

```bash
python -m validation.generic_structure.interactions
```

The principal demonstration combines onsite quadratic/quartic interactions,
three-axis endpoint coupling, and three actual link fields. There are five
declared channels (`phi`, `chi`, `link_0`, `link_1`, `link_2`), **15 retained
integer entries per node**, and **36 final response monomials**. Every link
is counted once at its storage node while both endpoints participate in
the physical-support audit. No channel is added by differentiation.

On 27 nodes and three steps, the run checks **405 actual complete triples**
against an independent oracle. For each field coordinate, the oracle
evaluates the global scalar polynomial at perturbations `-2,-1,+1,+2` and
uses

```text
f'(0) = [f(-2)-8f(-1)+8f(1)-f(2)]/12.
```

This identity is exact for degree at most four. It neither differentiates
the term list symbolically nor reads the compiled derivative tensor. The
result is compared with actual Engine inputs, then used in an independent
scalar Rule3 calculation. All six initial remainder classes, stepwise
inversion and complete rewind pass. The largest retained integers in these
three steps have 3, 8 and 21 bits, while the potential grows sharply. The
audit does not claim stability or conservation of that potential.

Additional actual Engine controls check a negative declared field sign and
signed inputs above 100 bits. Reordering factors/terms and translating their
common anchor leave the compiled dynamics unchanged. Two half-coefficient
terms that combine into one integer response are accepted.

The following are rejected or fail as intended:

| Control | Result |
| --- | --- |
| Degree-five potential | Rejected before tensor construction |
| Half-integer mixed derivative | Rejected after exact coefficient collection |
| Three storage nodes or a distance-two neighbor | Rejected by physical support |
| Crossed x/y link fields at the same storage node | Rejected because their endpoints span three physical nodes |
| 49 retained channels | Rejected with the complete count |
| Missing owner, undeclared field or floating coefficient | Rejected |
| Omitted reciprocal partner | Legal local tensor, failed reciprocity |
| Omitted endpoint response in the shift-charge model | Reversible tensor, failed charge conservation |

Raw evidence, source hashes, the normalized potential, complete compiled
tensor, channel ledger, seed and final state are written to
`runs/generic-structure/interactions.json`.

## Composition boundary

The compiler has no hidden update stages. Its pure response tensor can be
consumed by another counted native construction; the separate native
schedule audit directly consumes the generated quadratic forces of
`V=(g_x+g_y)(phi_y-phi_x)^2` and compares them with an independent edge
formula. That integration must retain its own degree and state accounting:
a clock pulse multiplying an already cubic force would have degree four
and must be rejected unless a different proved encoding is supplied.

The constructive structure is therefore: **one declared local interaction,
all reciprocal responses, an exact symmetry where available, and one
counted update implementation**. A metric, calibrated clocks, propagation
on that metric, stress-energy identification and a constrained Einstein
limit remain additional obligations. This grammar makes their shared
couplings auditable; it does not derive them from polynomial degree alone.
