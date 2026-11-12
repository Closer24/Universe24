# A generic interaction, encoding and proof structure

Eight-agent continuation of the owner's node/clock/Einstein investigation.
Baseline: final PR52 `8c53e69f4b466dcbd2da7dab7e3c365bd9731766`.
This is a source-only construction and proof proposal. The production Engine,
one-system runtime, decoder and physical acceptance status are unchanged.

The proposed organizing principle is: **describe each local interaction once,
generate all its responses, compile one complete reversible evolution, and
prove the domain and constraints on that actual evolution.** Matter, geometry,
clock mechanisms and records then have explicit roles inside one model. Their
names do not change the generic node primitive.

## Four core objects, one execution path

| Object | Meaning | What is implemented in this proposal |
| --- | --- | --- |
| State and physical interpretation | Complete fields, histories, carries, ownership, units and one metric | Exact restricted full45-to-six embedding; typed same-run observation contracts |
| Local interaction | Onsite/single-face polynomial with all endpoint and mediator responses | Reusable polynomial differentiation/reanchoring compiler, with degree, integer, physical support and reciprocal-response checks |
| Complete temporal encoding | Target map plus counted workspace/scheduler and physical-step interpretation | Nine-tick low-rank native drift/kick compiler; actual interaction-to-schedule-to-Engine example |
| Domain and measurement evidence | Exact invariant identities, validity domain, replay and independent physical observations | Complete-history constraint certificates and counterexamples; native packet/phase evidence; separate readout/provenance checks |

The target map is a construction/validation object, **never a runtime callback**.
Only the fixed integer tensor and Engine advance retained state. Record readers
and continuum oracles cannot repair that evolution.

## Proof 1: all responses from one interaction, with an exact shift charge

Let a translation-invariant local potential be a sum of onsite/face terms of
degree at most four. If its differentiated coefficients are integers, all
generated forces `F=-grad V` have degree at most three in the all-positive-sign
convention (`Phi=-V` in the compiler). Its general signed-gradient option must
carry the corresponding signs explicitly. Reanchor each response
at its target and include the physical endpoints of every link owner. The
compiler rejects a term if this produces anything beyond one physical face.
Locality and degree are therefore checked after the actual differentiation.

For the native coordinates `Q=b`, `P=6(b-a)+r`, choosing `u=6b+F(b)` gives
`P_next=P+2F(b)` exactly, with all carries retained. If `V` is invariant under
one common shift of the selected positive-sign node field, then the sum of its derivatives
vanishes and `sum P` is an exact invariant of the actual discrete update.
This is a specific algebraic charge; it is not a claim of physical Einstein
energy conservation. Reciprocity alone does not imply energy conservation.

The audit generates both endpoint and mediator backreaction. It preserves the
shift charge at -39; removing one endpoint response gives defect -560 despite
continued exact rewind. Full proof and source: [review 1](01_interactions.md).

## Proof 2: constrain the complete history, not only today's fields

For the actual complete map `T`, a sufficient invariant certificate is domain
closure and an exact identity `H(T(s))=A(s)H(s)`. Induction then preserves
`H=0`. Rational identities require a proved nonzero-denominator domain;
polynomial ideal membership is sufficient, not generally necessary.

For an intended physical macro-map `Phi`, the compiler must also establish

`T^m(E(z,eta)) = E(Phi(z), H_aux(z,eta))`.

Here `E` contains both histories, every carry and all workspace/scheduling
state. A matching first step or continuum equation is insufficient. The
existing `u=3(Phi+Phi^-1)` embedding supplies a useful exact subclass when its
integer inverse-sum, degree, support and allocation obligations hold.

Executed two- and three-channel examples preserve indefinite quadratic forms,
including the nonlinear cubic map
`(x,y,z) -> (x,y+2x²,z-2xy-2x³)`, which preserves `2xz+y²`.
In contrast, two independently constrained histories can leave the constraint
surface immediately. The existing reduced Einstein target's tiny but exactly
nonzero tick-two defect remains reproduced. [Review 2](02_constraints.md).

## Proof 3: workspace can be shared only for the drift it actually computes

The native compiler retains `n` data channels, `r` quotient-work channels and
three schedulers, totaling **n+r+3**. It executes one immutable tensor for nine
ticks and restores all workspace/scheduler triples at each macro boundary.
Its drift is explicitly `S* = S+B floor((2 A a+kappa)/6)`, followed by the
declared force kick. The general matrices do not implement componentwise
division merely because their product resembles an identity.

Within this layout, exact independent quotient drifts imply `BA=I`; testing
integer inputs `a=3e_j` already proves `r>=n`. Thus 44 data plus one work and
three scheduling channels fits 48 only for a restricted rank-one drift. The
direct full-rank 44-field layout costs 91. This is a scoped construction bound,
not an impossibility theorem for every other compiler.

The actual joined example is a cubic face potential, its generated quadratic
forces, a rank-one native schedule and the unchanged Engine: **six channels**.
It matches an independently derived macro-step and preserves the field shift
charge. Cubic forces requiring an extra gating factor are rejected rather than
silently exceeding the degree bound. [Review 3](03_native_schedule.md).

## Proof 4: a small exact sector is a laboratory, not a general compression

Exact sparse substitution of every full45 target polynomial derives the
homogeneous isotropic neutral six-channel sector `(D,B,K,phi,Pi,d)` with 14
terms. The complete-state embedding includes both histories and carries; it
commutes with forward and inverse updates. Omitted carry values are explicitly
fixed by the sector definition, not stored outside the budget.

The new reusable extractor verifies 131,220 full-state integer comparisons and
rejects malformed embeddings. It preserves `H_after=-7/4096` in its sourced
control and the original bit growth. Thus it is a useful cheap laboratory for
the temporal/constraint repair; it does not hide that repair or retain general
spatial/charged modes. [Review 5](05_symmetry_sector.md).

## What now runs, and what remains a physical proposal

| Construction | Established | Not established |
| --- | --- | --- |
| Generated reciprocal interaction | Integer/local/cubic force generation and an exact conditional shift charge | Einstein source/constraint or general energy law |
| Joined six-channel native primitive | Actual potential-to-compiler-to-Engine path; oracle, restored work and rewind | An implementation of the reduced Einstein target |
| Nonlinear constrained integer examples | Complete-history invariant quadratic forms under actual Rule3 | General gravitational constraint closure |
| Exact 45-to-six sector | Bidirectional complete-state equivalence on its stated symmetry image | Compression of arbitrary45 states or spatial packet physics |
| Three-channel massive packet | Actual one-axis-localized transport and phase agree with independent discrete dispersion | Common45 curved matter, exact relativistic proper clock or fixed-mass continuum refinement |
| Typed same-run receipts | Reject mismatched seed, metric/time interpretation, window and hidden-state record claims | Proof that declared interpretations or physical clocks are correct |

The two massive packet controls move about12.61348 nodes in64 actual Engine
ticks, with measured velocities about ±0.19708308 and peak25-bit integers.
The same fields supply a phase frequency. However phase/rest ratio0.80605
differs from continuum proper-time ratio0.79772; a high-frequency spectral
mode with zero group velocity also defeats a universal rest-clock interpretation. These failures
are retained. The integer mass coefficient blocks the claimed fixed-physical-
mass refinement in this simple stencil. [Review 4](04_packet_clock.md).

The physical action/coframe review and independent review complete the design:
[review 7](07_physical_structure.md), [review 8](08_review.md).
The detailed interface and budget ledger is [review 6](06_architecture.md).
Separate successful fixtures are never combined into one claimed physical law.

An additional exact frame primitive uses nine frame entries and two frozen
integer shear coefficients: `B_next=M B`, with `det M=1`. Its prepared
complete-history embedding preserves a nonsingular frame for every finite tick
in both time directions. It also exposes the boundary: fixed-volume shears
cannot describe expansion, and metric conditioning can worsen exponentially
despite fixed determinant. The Palatini action's quartic polynomial degree is
compatible with cubic variations, but its multipliers and constrained temporal
structure still require their own discrete map; treating every variable as an
ordinary inertial channel changes those equations.

## Recommended build order

1. Use the exact six-channel sector to develop a discrete sourced map with a
   genuine constraint and domain identity. Retain both the first-step `-7h²`
   and tick-two cross-history failures as mandatory rejection controls.
2. Prove a complete-state native encoding of **that map**, with counted work,
   physical scales, inverse and restored scheduling. Available channel room
   in a restricted sector does not by itself solve rational arithmetic or
   prove compatible time evolution.
3. Recover spatial modes and the full shared metric with a declared allocation.
   Require nonlinear constraint/domain evidence and stable controlled refinement
   for that exact tensor, not inherited proofs from another law.
4. Run actual neutral massive and Maxwell packets in that same geometry, with
   one flat calibration and held-out directions/velocities. Compare phase,
   transport and independent clock mechanisms, preserving finite-width,
   backreaction and bit-cost limits. The present three-channel packet is a
   scoped numerical primitive, not a substitute for this experiment.
5. Fit and couple retained apparatus/records with their stress/momentum account.
   A `45+3=48` arithmetic ledger or passive phase crossing is not physical
   completion. Read records only after retained dynamics has produced them.

This order targets the actual bottleneck: a correct physical evolution with a
compatible complete history. Repackaging already passing modules cannot replace
that proof. General Einstein dynamics and operational clock/detector physics
within48 channels remain unestablished.

## Reproduce and inspect

```bash
python -m validation.generic_structure.run_all
python -m unittest discover -s universe24/tests -t .
python -m validation.system_smoke --out runs/generic-structure/system-smoke
python -m universe24 verify --run runs/generic-structure/system-smoke/run
```

The runner executes the eight source-only audits, preserves raw evidence and
checks its source hashes. Large complete traces are committed as deterministic
`.json.gz` archives; each audit regenerates its documented plain JSON, and
`collection.json` records both hashes and the archive path. See
[VALIDATION.md](VALIDATION.md) for the final local
result. Existing production source remains unchanged. Coordination is through
[issue40](https://github.com/Closer24/Universe24/issues/40) and
[issue41](https://github.com/Closer24/Universe24/issues/41).
