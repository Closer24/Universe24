# One-law interfaces and exact orientation covariance

This lane checks the same carrier/record construction from issue63, rooted in
the consolidated source `f4f64e062f07b3ca119eccf655df746be206908b`. It changes no
production runtime, decoder, physical gate or channel limit.

## Paired-bank locality theorem

Let `G` be the declared reversible onsite four-rail collision, and `S` the
permutation streaming the declared rails along their respective face directions.
For the paired banks define

\[
F(A,B)=(G(B),S(A)),\qquad F^{-1}(A,B)=(S^{-1}(B),G^{-1}(A)).
\]

If both onsite collision polynomials have degree at most three, the input
`u=3(F+F^-1)` is cubic and strict-face-local: every nonlinear monomial is onsite;
every streaming monomial is linear and uses only one face neighbour. Different
rails may stream in opposite directions because no product joins their remote
values. No old-a input is read, so the native staged inverse has one stage.

On the complete prepared sector `a=F^-1(b)` with legal carries,
`divmod(6(F(b)+F^-1(b))+r,6)` has quotient `F(b)+F^-1(b)` and remainder `r`.
Thus Rule3 gives `(a',b',r')=(b,F(b),r)`, which preserves the same history
condition. Bijection and any proved G/S invariant therefore persist for all
updates in the declared sector. This theorem needs the actual gate/domain
proof; it is not a generic stability or Einstein theorem.

Current ownership is eight channels,24 retained integers per node:

| Role | Channels |
|---|---|
| Record plus/minus, both banks | 0,1,4,5 |
| Carrier plus/minus, both banks | 2,3,6,7 |

Additional physical chart channels, if constructed later, must be counted and
proved separately. The general `allocation` validator permits at most48 total
channels, requires exclusive exhaustive ownership, reconstructs strict tensor
support, and checks declared directed coefficient paths. It rejects a detached
geometry block advertised as record-to-geometry influence. A path merely shows
possible algebraic influence; an inactive preparation can nullify it. Actual
causal interventions and source equations remain required.

## Coordinate covariance, not fixed-tensor isotropy

For an exact signed permutation R of the cubic lattice, move every retained
entry by `x -> R*x`, and transform each tensor offset by R. Polynomial
evaluation commutes with this permutation. Rule3 acts entrywise, hence

\[
W_{R T}(R S)=R W_T(S).
\]

The same follows for the unique inverse. For the chosen directed family,
`R T_d=T_(R d)` can therefore hold for all48 signed coordinate transformations.
It does **not** imply `R T_d=T_d`: a fixed preferred axis breaks full cubic
isotropy. The audit reports both the family covariance and the actual fixed-law
stabilizer count. The action here regards record/carrier labels as roles
relative to the transformed direction, not spinors or Cartesian vector
components. Link-gear and designation metadata are rejected rather than
silently transformed incorrectly. Reflections, time reversal and a spinor
central sign are not identified.

## Source-bound evidence joins

`run_identity` reexecutes the saved run through the existing verifier. It binds
the exact tensor, complete seed, bundle, run, horizon, full trace, canonical
clicks and the declared current implementation source hashes. `join_evidence`
requires the same identity and an exhaustive preregistered claim list for every
lane report. It rejects mixed seeds/laws, changed horizons, stale source, missing
claims, duplicate claims, booleans used as integer counts and float metadata.

This identifies which experiment a report describes; it does not establish
that the report's scientific claim is true. In particular, failed/blocked
physical gates remain present, and the joined record explicitly grants no
physical acceptance. Independent scalar/physical oracles must evaluate the
same run. Hashes provide identity and corruption checks, not authorship.

The regression suite executes coordinate covariance on nonzero carries,
rejects disconnected claimed composition, and deliberately corrupts evidence
seed/horizon/tensor/source identities. It also audits the actual native tensor
family, not only an abstract transformation helper.

```sh
python -m validation.local_unification.contracts --out runs/local-unification/contracts
python -m unittest universe24.tests.test_local_unification_contracts -v
```
