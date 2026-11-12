# What one node actually guarantees

Research task 3 of the owner's eight-part investigation, 12 November 2026.
Runtime inspected: main `4c494c1188f70eb8a677bf59765cc6e8571c6b88`.
This report and its source-only audit change no Engine, tensor contract,
accepted physical model or metric authority.

## Exact common law

Every valid retained triple has `a,b` integral and `0 <= r < 6`.
The tensor supplies an integer `u` from the same old snapshot. The Engine's
actual update is at `universe24/core/engine.py:361`; its staged inverse is
at line 383. The admissible tensor reads only old `a,b`, has degree at most
three and single-face monomial support, and has acyclic old-a dependencies
(`universe24/core/tensor.py:12–35`). Thus the universal statements are:

1. **Exact reversible accounting**, including the division remainder.
2. **Local influence**, at most one face edge per forward microtick.
3. **A second-order retained history**, with a native integer position/kick
   description, but no automatic identification with physical position or
   canonical gravitational momentum.
4. **A frozen parity at each node/channel**, with a three-state active carry.

These are structural results about every admissible tensor. Energy,
Lorentz symmetry, a metric, geodesic motion and gravitational constraints
require further properties of a particular tensor and physical readout.
The code itself says gear names carry no physics (`tensor.py:3–4`).

## Native q,p and the carry ledger

The native coordinates are already derived in
[PR #50, report 1](https://github.com/Closer24/Universe24/blob/62202fdccdd9a40d5dbbec104de6f97d9587a999/docs/research_eight/01_integer_algebra.md).
The actual report was read from the fetched PR #50 Git ref; the present
calculation reproduces its algebra rather than claiming a new discovery:

```text
q = b,             p = 6(b-a)+r
a = q-floor(p/6),  b = q,           r = p mod 6
p_next = p + 2(u-6q)
q_next = q + floor(p_next/6).
```

The algebraic identities hold even for permitted old-a reads. Interpreting
the update as a position-only kick followed by a drift requires **b-only**
inputs: otherwise `u` also depends on old momenta through old-a data, and
the inverse uses the tensor's staged dependency order. The change of
coordinates does not remove retained information or alter the channel count.

The acceleration defect has the exact form

```text
6(q_next-2q+q_previous) - 2(u-6q) = r-r_next.
```

Summing this defect along one retained channel telescopes to
`r_initial-r_final`, whose absolute value is at most **4**, since parity
is fixed. Consequently the sum of the acceleration residuals after division
by six has absolute value at most `2/3`. This is exact carry accounting;
it is **not** a bound on accumulated position error or on error against a
continuum trajectory. Nonlinear forces can amplify trajectory differences.

## Which part of the six-state wheel is observable?

The parity theorem is already stated in `docs/MODEL.md:60` and the allowed
click turns in `docs/CLICK_CAUSALITY.md`. Write

```text
r = 2s+epsilon,       s in {0,1,2}, epsilon in {0,1}
ell = floor((u+s)/3)
s_next = (u+s) mod 3
epsilon_next = epsilon.
```

Because the tensor never reads `r`, flipping any subset of the parity bits
while preserving `s,a,b` leaves the entire future `a,b,s` trajectory
unchanged, including for acyclic old-a tensors. The retained `r` arrays
remain distinct. The official click test also remains unchanged: its
quotient, triple-changed predicate and remainder-difference class are the
same. Therefore click streams cannot distinguish these complete states.

Only remainder differences `0,2,4` modulo six occur in valid evolution,
corresponding respectively to C0, C1, C2. This supplies a precise arithmetic
meaning; it does not identify C2 with collapse, a particle species or a
direction of physical entropy production.

## Actual Engine checks and counterexamples

Reproduce from the repository root:

```bash
python -m validation.einstein_node_audit.node_algebra
```

The run uses a three-channel cubic tensor with constants, signed coefficients,
face coupling and three inverse stages. An independent Python-integer oracle
evaluates factors by explicit periodic coordinates; it does not call Engine's
compiled plan or gather tables. Six complete seeds include all six remainders
and one seed with signed values above 100 bits. Five steps per seed check
**2,430 complete triples**, **2,380 paired official click rows**, the native
identities, the carry sum, both full rewinds and parity-blind trajectories.
The largest retained integer reaches **4,838 bits**. This is also direct
evidence that few channels and a short run do not imply small arithmetic cost.

The same legal tensor fails the reciprocal-gradient check: the update
contract does not enforce a common potential. This failure is preserved
in the audit output. Even reciprocal special cases need their own discrete
conservation and gravitational-constraint arguments; `core/reciprocity.py`
checks a particular b-only potential relation and skips old-a terms.

The one-channel controls start uniformly from `(a,b,r)=(0,1,5)` on 27 nodes:

| Input law | Actual field trajectory | Consequence |
| --- | --- | --- |
| `u=0` | `(a,b)` rotates with period four; **zero official clicks** at all twelve tested steps | A moving periodic internal state need not produce an arithmetic clock record. No state function can strictly improve on every step of this nontrivial cycle. |
| `u=6b` | `b_n=n+1` | Exact affine field evolution is easy, but a field amplitude is not yet a freely falling body's spacetime coordinate. |
| `u=6b+3` | `b_n=1+n+n(n+1)/2` | The same primitive admits acceleration simply by changing the tensor. |
| `u=9b` | `b_next=3b-a`, growing exponentially for this seed | Reversibility does not impose boundedness or minimize the integer magnitudes. |

Every complete control rewinds. The candidate norm `a²+b²` changes in the
last three cases; it is not a universal conserved energy. Other tensors
can have useful invariants: PR #50 already supplies the period-six
`u=3b` oscillator with `a²-ab+b²`. Neither the counterexample nor that
positive example identifies a physical stress-energy tensor.

Raw source-hashed evidence is `runs/einstein_node/node_algebra.json`.
The generic and negative-control assertions pass. Geodesic/proper-clock
identification remains `not_tested`, and Einstein acceptance is
`not_established`.

## What connects naturally to the Einstein task

The useful starting point is a local reversible **balance and transport law**:
no discarded remainder, explicit neighbor influence, and reciprocal forces
when actually derived from one potential. A common local action could then
tie matter response and geometric response together. This is a research
direction, not an implication of the scalar Rule3 primitive.

The repository already identifies a relevant obstruction in
`docs/PALATINI_TARGET.md:46–64`: the smooth remainder-free reciprocal Rule3
comparison has a regular kinetic Hessian, whereas first-order gravity has
multiplier constraints and gauge degeneracy. Merely giving every coframe or
connection component the same inertial update does not enforce those
constraints. An invariant constrained encoding or a counted retiming proof
is required.

The next discriminating test is consequently to specify one local action,
derive its actual exact balance identities and constrained invariant sector,
then measure independently calibrated clocks and free probes on that same
metric. The present algebra supplies reliable bookkeeping for that test;
it supplies neither a metric-null cone nor an Einstein field equation by
itself. A global claim that the board always reduces computational load is
already false for the generic contract, while a selected law's weaker,
measurable load-balance hypothesis remains open.
