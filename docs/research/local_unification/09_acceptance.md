# Independent acceptance of the joined twelve-channel history

This boundary checks one actual saved twelve-channel execution. It cannot combine the eight-channel collision demonstration with a separate twelve-channel geometry demonstration and report that their conjunction ran. The bundle identity, exact tensor, seed, every complete transition, canonical click stream and finite source chart must all refer to the same history.

## Independence and the exact inverse

The implementation in validation/local_unification/acceptance.py does not call Engine.step, Engine.inverse_step, the candidate's native Boolean oracle, its transport helper, or the canonical decoder. It iterates the serialized monomials and scalar lattice indices literally. The tensor is first compared coefficient by coefficient against an independently stated collision polynomial and four source rows; accepting an arbitrary twelve-channel tensor would not establish the claimed law.

For every channel and node the forward calculation is

\[
(\ell,r')=\operatorname{divmod}(2u+r,6),\qquad
a'=b,\qquad b'=\ell-a.
\]

All three registers are compared at every transition. Because this particular tensor reads only current \(b\), the inverse is computed without the Engine:

\[
b=a',\qquad
z=6b'+r'-2u(b)=r-6a,\qquad
r=z\bmod 6,\qquad a=(r-z)/6.
\]

This is an algebraic inverse for arbitrary integer \(a,b\) and every legal carry \(0\le r<6\), rather than an empirical guess from the prepared Boolean sector. On a contiguous checked history, applying these inverses successively recovers the seed.

Canonical events are independently reconstructed in node/channel order, including event IDs, signs, quotients and carry classes. Exact canonical JSON comparison rejects booleans masquerading as integer click fields. Complete old and new states reject omitted channels, omitted nodes, illegal carries and noninteger values. Rehashing a corrupt file cannot bypass the independent calculation.

The report binds tensor_hash, bundle_id, run_id, seed_hash, steps, channels_per_node, nodes, and the acceptance source SHA-256. Its register-comparison count is \(2\times3\times12\times L^3\times T\): forward and inverse, every register, node and step. File hashes detect corruption; the scalar recomputation establishes agreement with the declared polynomial.

## Collision, transport and the source use the same snapshots

At every saved state, acceptance verifies Boolean packet occupancy, the prepared inverse relation for all old packet registers, and the literal collision \(1001\leftrightarrow0110\). It checks the following for the very same transitions:

- both local packet-energy and momentum continuity equations at every node;
- constant global positive packet energy and signed packet momentum;
- every detector opportunity, including failures to select;
- exact two-tick transport of total right- and left-moving occupation;
- each geometry channel's discrete source constraint throughout the valid causal interior.

For each bank and direction, the constraint is

\[
F(x+d)-2F(x)+F(x-d)+q(x)=0,
\]

where \(q\) is formed directly from that bank's packet rows in the same state. A passive protocol selects a finite chart and horizon; it cannot substitute a different history. With no chart supplied, mechanical acceptance can pass but the source-chart status is explicitly not_tested. A malformed or mismatched supplied chart is rejected.

These checks establish the discrete source history. The independent continuum metric, spline reconstruction, all Einstein components and covariant balances are reviewed separately by geometry_review.py. A packet count \(E=\sum q\) is a lattice conservation account; it is not silently equated to a general-relativistic global energy.

## Limits that cannot be promoted into successes

For this collision, both directional totals are individually invariant at a collision:

\[
n_+=a+c,\qquad n_-=b+d.
\]

The two-tick map therefore gives \(n_+(t+2,x)=n_+(t,x-d)\) and \(n_-(t+2,x)=n_-(t,x+d)\). Species and records can exchange, but the total directional densities stream freely. On an infinite lattice, any nonzero compact packet eventually leaves every fixed bounded region. Counterpropagating packets can have \(E^2-P^2>0\) while separating; that invariant alone does not establish a bound massive object. This is a limitation of the present map and observables, not a theorem against every Rule3 law.

On a finite lattice, the prepared native sector has finitely many Boolean current states, with old packet registers fixed by the inverse and each legal carry frozen. The native map is a permutation. Every orbit recurs; a state function cannot increase strictly around a complete cycle. Hence indefinite strictly increasing organization is impossible in this finite native sector. This statement does not bound the joined integer-valued geometry registers, prove monotonicity for a chosen finite interval, or rule out a different law or infinite-volume limit.

A globally periodic positive source for the displayed profile equation is impossible: summing its discrete Laplacian over a periodic cycle gives zero, hence \(\sum q=0\). Nonnegative \(q\) with at least one occupied site contradicts this. The exact solution is consequently a finite causal chart; the periodic seam must never be reported as satisfying the same positive-source equation.

Finally, an exact chart and repeated records do not by themselves construct a material proper-time clock. For the proposed metric and a stationary coordinate worldline,

\[
d\tau=\sqrt{2}\,R^{-1/4}\,dt.
\]

A fixed tick count or record sequence agrees with this only if a mechanism establishes the necessary metric-dependent rate. That operational mechanism is not supplied by the present acceptance checks. Four retained selections from finite prepared packets do not establish unlimited renewal or an extremal-complexity selector.

## Validation status

The recovered acceptance implementation is now included in the combined
source tree. All 65 focused local-unification tests passed in the independent
integration review, including the independent acceptance checker and its
adversarial cases. The exact prior source `fb4a09b2925a876d6c92493b2784fe30c16ed2e1`
also passed its published Python 3.11/3.12 CI. These scoped results do not
certify later source changes or promote the physical gates.

The central acceptance command runs the full collection on fresh saved inputs;
its output binds current sources, complete runs and all outcomes. See
`../system_acceptance/clean_local_source_review.md` for the independent review.

~~~sh
python -m unittest universe24.tests.test_local_unification_acceptance
python -m validation.local_unification.acceptance RUN_DIRECTORY --protocol PROTOCOL_JSON --out ACCEPTANCE_JSON
~~~

The adversarial suite includes a real twelve-channel saved run, an uncoupled
source tensor, truncated eight-channel state, rehashed profile corruption,
integer/Boolean aliases, mismatched horizons and coordinates, and an illegal
carry. General physical acceptance remains unestablished.
