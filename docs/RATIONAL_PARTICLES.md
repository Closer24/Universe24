# Opt-in bounded rational particle candidate

> **History (2026-09-19).** The engine this document describes was deleted on
> 2026-09-19 with the old engine ([migration](MIGRATION.md#one-engine-on-2026-09-19-the-old-engine-deleted));
> the one engine is the field-only engine of the law of the shadow
> ([SPATIAL_FIELDS.md](SPATIAL_FIELDS.md#the-law-of-the-shadow-field-only-v1)).
> The text below is kept as the record of what was built and measured; its
> links to code, worlds and tests name files that no longer exist.

This extension repairs representational and routing defects without choosing
physical species inside the engine. Existing integer ASTs and cyclic transport
retain their contracts. New configurations select balanced routing and rational
expression projections explicitly; their model_id identifies that choice.

The examples are numerical and mechanical reference benchmarks, not emergence
experiments. Their supplied elastic and energy formulas are independent from
the elementary-rule probes in [PHYSICAL_ENTITIES.md](PHYSICAL_ENTITIES.md).

| Part | Contract |
| --- | --- |
| Inputs | Only fields of the local participants or explicitly delivered field samples |
| Arithmetic | Rational expression regions: canonical signed numerator and positive denominator, each at most 127 magnitude bits; products/addition temporaries at most 255 magnitude bits |
| Bound | Fixed-width checks on bounded operands/results; bounded Euclid, at most 512 iterations; 65536 evaluate charges per rational AST node and 65536 route charges for fractional clock arithmetic |
| Storage | Existing 30-bit-magnitude payload components remain unchanged |
| Mixed values | Whole part truncates toward zero; remainder has the value's sign; all vector components share a positive denominator; representation fields are non-extensive |
| Transactions | All projections read one frozen input; declared rational invariants compare decoded values, never numerator sums |
| Routing | Optional balanced midpoint ordering of gcd-reduced six-port weights; fixed six counts and six cached weights, stored as positive codes; reset counts on direction change; 512 route charges per selection |
| Timing | Optional dynamic rate divisor; exact carried fractional credit with bounded numerator and denominator; overflow rejects the proposal |
| Errors | Zero denominator, register overflow, invalid energy stock or invariant failure rejects the local proposal; no truncation, saturation or global repair |
| Massless | Explicit configured transport independent of mass division; any energy/momentum relation is a named configured law |
| Energy | Joint field/carrier invariants may exchange kinetic energy with an explicit nonnegative local reservoir; no electromagnetic interpretation is implied |

Six cardinal links retain their L1 causal cone. Equal Euclidean maximum speed
in every direction at the axis maximum is impossible under one link per tick.
A slower, explicitly configured speed candidate may compensate hop rates within
that bound; finite rational/discrete approximations must state their error.

`routing: "balanced"` selects the corrected router; omitted or `"cyclic"`
retains the legacy block router for identified old configurations. `direction`
accepts a three-component expression in place of `direction_field` or weights.
`rate_divisor` is a scalar expression multiplying the constant `rate_denominator`.
When present, fractional credit is reduced and preserved through rate changes.
This adds one positive denominator register alongside the existing credit code.
Old constant-divisor transport retains its old cost and credit convention.
Type conversion retains its zero-carried-state requirement: balanced counters,
remembered weights and the fractional-credit denominator must also be in their
initial state before a new routing law can take ownership. Conversion rejects
noninitial registers atomically instead of silently resetting them.

Use a `rational_*` projection to enter an exact rational region. `ratio(a,b)`
performs exact division by a nonzero scalar inside that region. Existing add,
sub, mul, abs, dot, cross, transforms, comparisons and component operations
then act on exact ratios. `exact_div` still requires an integer result. Projections
are `rational_whole`, `rational_remainder`, `rational_denominator` (common vector
denominator), `rational_numerator`, `rational_direction` (reduced direction),
`rational_floor`, and `rational_key`. The last returns canonical numerator/denominator
pairs only at the root of an invariant expression. Keys cannot nest or feed
ordinary arithmetic, checks, routing or assignments; their width is at most
six integers. Other projections
must fit the existing payload bound. AST limits remain 64 nodes and depth 16.

Disturbance `checks` are named scalar predicates over its owned fields, evaluated
on local proposed inputs/outputs. A nonpositive result rejects the local plan.
For example `eq` can enforce a configured mass-shell relation. These checks are
local consistency requirements, not global repair or a physical law selected by name.

The JSON candidates in `examples/particle-contracts/` cover fine rounded mass
ratios and elastic backscatter, a massless c=1/2 candidate with E=|p|/2, and a
nonnegative local reservoir conserving carrier-plus-reservoir energy and momentum.
The massless axis (10,0,0) and oblique (6,8,0) examples travel the same Euclidean
distance over complete routing/credit periods. This is not a proof of isotropy
for all irrational directions; the lattice remains cardinal and discrete.
`entities.json` supplies named properties once; `build.py` is an optional development
helper that writes the standalone JSON files, not a compilation or per-run step.

New rational wrappers are a scoped extension of the old working-register limit,
not an implicit change to old integer arithmetic. They do not provide unbounded
precision. Repeated exact interactions can still exhaust finite storage and must
fail explicitly. Measurements remain read-only and count in-flight ownership.

From an installed development environment at the repository root:

```bash
python tools/audit_particle_contracts.py --output /path/to/particle-audit.json
python -m event_universe --init examples/particle-contracts/electron-proton.json --output artifacts/particle-contact
```

The audit runs 24 configurations without rendering, frame recording or event
files: seven named free carriers, unequal-mass contact at two transit times,
axis/oblique massless transport, local energy exchange, direction scaling,
coarse mass units and computational delay. It counts carriers in transit and
compares decoded rational values with host-only `Fraction` diagnostics every
tick. Its optional JSON records exact inputs, source fingerprint, trace hashes,
cost/delay summaries and maximum energy/momentum error. These diagnostics never
feed the engine. The normal run command likewise needs no compilation step.

Finite capacity, anisotropy and absent physical laws are not silently repaired:
repeated exact interactions can exceed the payload bound; c=1/2 is a configured
test value; the reservoir has no Maxwell constitutive relation; particle creation,
annihilation, spin and binding do not follow from the named properties. Existing
integer configurations must explicitly migrate their representation to use the
new contract; they are not reinterpreted automatically.
