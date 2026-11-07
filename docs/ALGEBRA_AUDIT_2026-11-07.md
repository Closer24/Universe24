# Algebra audit — 7 November 2026

Reviewed reference: `Closer24/Universe24`, commit
`ed1556e202eb0f3cc60342c75d44012c2eeb71c3`. This is an independent review
of the specified integer map, not empirical validation or a proof of detector
physics. No core file was changed.

Research-document reference: “Universe24 — Could a Simple Automaton Be the
Logic Behind Nature?”, Google document
`1NDPfeFj9vldgb0RMSSvx2lBSmOo__E-F3t2cZwfjOjI`, fetched 7 November 2026;
the retrieved metadata reported modification `2026-11-07T01:37:38.239Z`.
Section references below refer to this snapshot, especially A1–A14.

## Findings and scope

| Claim | Classification | Exact scope and evidence |
| --- | --- | --- |
| Full-state evolution is bijective | Mathematical proof | Any complete valid state, any finite periodic cube `L>=3`, any one fixed permitted sign triple; constructive inverse below; `core/rule3.py:4`, `core/engine.py:27`; document A2 |
| Influence travels at most one spatial graph edge per update | Mathematical proof | Full-state dependency bound, not a measured physical light speed; `core/engine.py:15`, `core/state.py:38`; A1–A2 |
| Every channel's remainder parity is invariant | Mathematical proof | `r mod 2` is fixed at the same complete channel address, for every update; A9 |
| Positive-reference total Q is conserved | Mathematical proof | Periodic graph, signs `(1,1,1)`, complete retained state; A10; `observation/diagnostics.py:5` |
| The same Q is universally conserved for signed choices | Refuted universal claim | Exact residual below; `(1,-1,1)` with one `b=1` gives `Delta Q=-8` |
| An arbitrary nonzero net neighbor input can be completely blocked by the local state | Refuted universal claim | Same old triple, unequal input sums imply unequal new complete triples; does not exclude a useful effective clutch for restricted signals/readouts |
| All amplitudes remain bounded | Refuted universal claim | Positive-reference homogeneous exact solution `(a,b,r)=(t,t+1,0)` for all `t` |
| Signed reflection transformations commute with evolution | Conditional mathematical theorem plus finite exact algebra certificate | Scalar proof is correct; spatial theorem follows from the finite port/weight identities. See `docs/REFLECTION_AUDIT.md` and its exhaustive certificate/tests. This audit did not independently rerun their entire enumeration |
| Continuous spatial isotropy, physical particles, energy, quantum measurement or gravity follow | Not established | Neither invertibility nor channel representations establish these interpretations |

## Proof checks

Let `A` be the fixed signed adjacency operator on complete addresses and
`u=Ab`. Rule3 obeys `6 ell+r'=2u+r`, `a'=b`, `b'=ell-a`.

**Inverse.** Given any valid complete new state, set `b=a'`, reconstruct
`u=Aa'`, set `r=(r'-2u) mod 6`, and set
`a=(2u+r-r')/6-b'`. The quotient is integral and the recovered remainder
is uniquely in `0,...,5`. Substitution into the forward map returns the
given new state; applying this reconstruction to any forward state returns
its old state. This proves both directions and hence bijectivity. It does
not claim that a node or click alone contains its own inverse data.

The sparse implementation is consistent with the full map. Its background
has `a=b=0`, and any permitted constant background remainder is fixed when
the input sum is zero. An omitted address receives zero input unless present
in the generated sum dictionary. The update visits the union of stored
addresses and nonzero-input addresses. It drops a stored entry only when it
equals the known background; this is lossless compression, not state erasure.
Scattering in `Engine.input_sums` matches gathering in `update_node` because
the reverse port and weight identities are enforced by `Coupling.validate`.

**Locality.** One update reads the old triple at the address and the six
neighboring sites' selected `b` values. By induction, the state at time `t`
depends only on initial data at spatial graph distance at most `t`.
Periodic wraparound must be included in that graph distance. This is a
computational causal cone, not yet observer-independent physical spacetime.

**Remainder parity and mechanics coordinates.** Reduction of
`6 ell+r'=2u+r` modulo two gives `r'=r (mod 2)`. Write
`r=2 theta+epsilon` and `p=3(b-a)+theta-1`. Direct substitution gives
`p'=p+u-6b` and `b'=b+floor((p'+1)/3)`. The inverse coordinate formulas in
A9 recover `theta` and `a`. No new register or forward rule is introduced.

**Balance.** For `Q_nu=6(b_nu-a_nu)+r_nu-r_background`, subtraction gives
`Delta Q=2(A-6I)b`. Every signed row has sum
`rho=2(sigma_x+sigma_y+sigma_z)`. Reciprocity makes A symmetric, so
`sum Delta Q=2(rho-6) sum b`. Thus the positive choice conserves the total;
every choice containing a negative sign fails to conserve this particular
total for some states. Special states can nevertheless have zero change.
The antisymmetric flux `J(nu,eta)=2A(nu,eta)(b_nu-b_eta)` obeys
`Delta Q_nu+sum_eta J(nu,eta)=2(rho-6)b_nu`. No residual may be discarded.
This algebraic account has not been identified with physical energy.

**Full-state clutch obstruction.** Comparing two updates of the same old
triple with input difference `delta` gives
`6 Delta b'+Delta r'=2 delta`. For `delta!=0`, the two outputs cannot be
identical. For example, old `(0,0,2)` with inputs `0,1,2` gives respectively
`(0,0,2)`, `(0,0,4)`, `(0,1,0)`. The first unit input is invisible in `b'`
but remains in `r'`. Equal net sums caused by cancellation are a different
case. This obstruction does not rule out state-dependent transmission of
specified signal families or thresholded readouts over a declared horizon.

**Unbounded solution.** In the positive reference, a spatially and
channel-uniform state has `u=6b`. If `r=0`, then `ell=2b`, giving
`b'=2b-a`. Hence `a(t)=t`, `b(t)=t+1`, `r(t)=0` solves the exact map for
every integer time, on every permitted cube. Universal boundedness is false;
bounded restricted families remain possible.

## Document versus implementation

The update equations, exact integer arithmetic, retained remainder, 48
channels, six spatial ports, body actions `(0,1,3)`, passive arithmetic
readout and full-state inverse agree with A1–A2, A6, A10–A12. Dense matrix
notation in the document and sparse routing in the code are representations
of the same fixed map; this is not a model discrepancy.

There are three qualification issues to preserve in project reports:

1. `Coupling.body_signs` defaults to `(1,1,1)` (`core/coupling.py:10`).
   Reflection documentation sometimes calls `(1,-1,1)` “current.” Both are
   supported, but an experiment must name one structural candidate and its
   fingerprint. Results for the positive reference cannot silently become
   signed-candidate results.
2. A11 refers to clock disruption, guide records, a binary comparator and
   homogeneous effective-ratio encodings. The retrieved repository does not
   provide complete reproducible fixtures and proofs for all these historical
   constructions. This algebra audit does not promote those statements to
   independently reproduced results. Each needs an explicit preparation and
   retained-state evidence in the pinned engine.
3. `classify` assumes the supplied pair is a real transition; it checks parity
   but does not validate evolution (`observation/clicks.py:15`). Arithmetic
   event correctness therefore presumes states came from the fixed engine.
   Its exclusion of zero quotient may hide physical state changes. A detector
   confirmation requires a separately frozen, explicitly justified readout.

## Supplemental finite checks

The following were executed with standard Python, exact integers and no
runtime interventions. They supplement, rather than replace, the proofs.

Reproduce from the repository root with `python -m research.algebra_audit`.
The script writes `research/algebra_audit_results.json`, including executed
source hashes, coupling fingerprints, exact seed generator, state hashes,
counts and counterexamples. A source-commit label is accompanied by actual
file hashes so later source edits cannot be mistaken for the reviewed files.

| Check | Declared finite domain | Result |
| --- | --- | --- |
| Scalar inverse in both directions, parity, one-unit input identity, mechanics coordinates | `a,b=-2..2`, `r=0..5`, `u=-7..7`: 2,250 cases | All passed |
| Dense gather vs sparse scatter | RNG `Random(241107)`; all eight sign triples in `product((-1,1),repeat=3)` order; `L=3`; all 1,296 addresses; independent `a,b` uniform integers `-4..4`, `r=0..5`; one update per case | 10,368 channel comparisons passed |
| Full-state inverse in both directions | Same eight full preparations and couplings | 16 round trips passed |
| Total Q balance | Same eight preparations | Eight exact identities passed |
| Signed Q counterexample | `L=3`, signs `(1,-1,1)`, default background, sole deviation `(0,0,0,0):(0,1,2)` | `Delta Q=-8` |
| Uniform drift | `L=3`, signs `(1,1,1)`, background `(0,0,0)`, every address `(0,1,0)`, 10 updates | Exact sequence `(t,t+1,0)` |

For the random preparation, address order is
`for pos in product(range(3),repeat=3) for g in range(48)`; draw `a`, then
`b`, then `r` using the same RNG across all sign cases. The reference test
commands in `AGENTS.md` remain the required baseline checks. This review's
finite supplemental checks have not been substituted for that suite.

## Decision

Retain the core unchanged. The inverse, parity and balance foundations are
adequate to support a preregistered signal–clock–record experiment. Do not
spend search budget on an exact local switch blocking arbitrary net input;
the algebra already excludes it. Search instead for a restricted, measurable
effective transmission change while preserving hidden-state information.
The next decisive uncertainty is composability and record lifetime, not
whether a reversible round trip can be obtained.
