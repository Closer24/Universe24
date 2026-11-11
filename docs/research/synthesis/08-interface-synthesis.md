# One-system integration: ports, competing allocations and acceptance

Research task 8, based on PR47 `621fc1f55800e50e1db5f6a30ce24bb83716a49a`.
This is the integration map for the eight-task round. It does not combine the
independent controls into another universe or promote a physical default.
The supported bundle/Engine/decoder remains the one execution path.

## The actual interfaces

| Component | Retained channels | Readout or coupling | Established boundary |
| --- | ---: | --- | --- |
| Old staggered protected frame, PR42/merged PR46 reader |44| Per-field sign/phase decoding | Reader is pinned to this law; it cannot decode projective numerators |
| PR47 projective unprotected / protected frame |41 /44| Physical fields `P/D`; protected diagonal `(Pp²+Pq²)/D²` | New denominator law; short-horizon refinement evidence is mixed |
| Exact passive metric/source and structural diagnostics |0 added| Read saved state; no update inputs | A diagnostic is not a retained apparatus or detector outcome |
| Executed projective one-face intensity receiver |45 total| `u=3N`, `N=|Px+Py|²`; physical weight `ell/D_before²` | One-way test apparatus; source projection unchanged; not Born frequency |
| Four-receiver old-law intensity apparatus, issue45 |48 total| Local and three face intensities | External team's reported tensor has no receiver-to-source monomial; source handoff must remain separately pinned |
| Executed Boolean comparison control |4 standalone| Two supplied Boolean scores, two reversible responses | Would consume all four spare protected-frame slots; not a structural-score computer or recurrent selector |
| Reciprocal complex spring control |4 standalone| Symmetric face exchange, including both complex endpoints | A flat isolated balance primitive; not four fields appended to the existing physical law |
| Cubic normalized-link expression |One receiver plus two link components per direction| `N_transport/D_before³` | Static identity only; direct three-axis append to44 requires51 channels |
| Prospective massive scalar clock ports from issue41 |0 added readout fields| `I=phi²+chi²`, `S=phi Pi_phi+chi Pi_chi` | External reported invariant-port test; no complete material period or moving-clock acceptance |

Counts refer to complete `(a,b,r)` channels, not individual integers. The
four Boolean comparison channels and four intensity channels are competing
allocations; naming both groups "observer" does not allow them to share state.
Replacing three spatial potentials by six normalized link components plus one
receiver gives the arithmetic ledger `44-3+6+1=48`, but needs entirely new
link/current/stress dynamics. Existing potentials are not already unit links.

For projective intensity the numerator is evaluated from the complete old
snapshot. The quotient therefore pairs with `D_before`, never `D_after`.
Task3 actually observed 80 wrong nonzero readouts when the wrong denominator
was used. That calculation requires full-state scale data; arithmetic click
records alone do not contain a denominator certificate. The old sign reader
must retain its source identity check. A generic field name or model label
cannot determine the decoding law.

## Executed integration rejection and causality controls

```
python -m validation.synthesis.interface_contract --out runs/synthesis/interface_contract.json
```

The audit compiles the actual PR47 protected44 source and adds one onsite
quadratic audit receiver. It then:

1. Inspects every tensor monomial: zero source targets depend on the receiver.
   It perturbs the receiver's complete old/current/remainder history at all
   27 sites. All original44 states remain identical for three updates, and
   both complete runs rewind. Induction from the dependency graph extends
   source independence to every computable step, not just those three.
2. Adds a legal onsite receiver-to-source term as a mechanical positive
   control. The same intervention now changes the source on the first update,
   and both altered states still invert. This proves the audit can detect
   feedback; it does not supply physical backreaction or stress accounting.
3. Composes the actual four-channel comparison tensor with that45-channel
   tensor. The resulting49-channel law is polynomial and single-face local,
   but the real bundle validator rejects it: `got 49`. Local validity alone
   is insufficient for composition.
4. Runs/replays the45-channel bundle with deliberately grand model metadata.
   Physical gates C–F remain `not_tested`. Changing the saved C status to
   `passed` is rejected by actual reexecution; the original report is restored
   and verifies again. A label or forged summary cannot create acceptance.

The JSON preserves executable/core source hashes, tensor identity, command,
actual rejection messages and scope. No existing system source was modified.

## A useful principle from the literature

Krhač, Maschke and van der Schaft,
[*Port-Hamiltonian systems with energy and power ports* (2024), section2,
definition1 and equation4](https://arxiv.org/html/2405.01241v1), formulate
interconnection through conjugate variables whose pairing accounts for
exchanged power. The useful design requirement here is to specify the
exchange identity at a physical interface, not merely pass a field value to
a receiver. Their framework uses smooth continuous-time geometry and does
not certify a floor/remainder integer update, its allocation, or Einstein
constraints. Our new requirement is an explicit discrete two-time balance
for the actual retained law, including interaction storage and geometric
work. This complements, rather than replaces, the independently executed
reciprocal-spring and metric-work controls.

## Concrete next integration path

**First keep one source and make every readout typed by its law and time
slice.** The current projective source and old staggered source remain
separate research candidates. A physical run chooses one complete tensor,
one seed and one readout certificate before execution; observers cannot
switch the law after looking at the trajectory. Preserve task1's frozen
held-out failure as an acceptance fixture.

**Resolve core cost and constraint propagation before extending horizons.**
Task2 proves exponential bit growth for the current projective recurrence;
discarding a gcd changes its future ratios. The parallel algebra team reports
a native coordinate candidate `q=b, p=6(b-a)+r`, with a fixed-six kick/drift
interpretation. It is a candidate for a cheaper encoding, not yet an imported
GR law. Require its exact source handoff and compare the same fixed physical
endpoint/initial data, all carries, H/M/torsion/gradient residuals and maximum
bits. Do not replace one tuned refinement sequence by another after failure.

**Use existing matter for the first clock calibration.** The reported massive
scalar ports `I,S` reuse the existing scalar pair and covariant momenta. On a
projective state both quadratic expressions use `D_before²`. Use a declared
mass and noncircular preparation; retain massless and circular no-clock
controls. First demonstrate a complete period on the actual coupled law,
then compare pre-calibrated moving packets and off-axis directions with the
same metric. Passive extrema in a saved trace are still not arithmetic
detector events. A separate three-dimensional first-order real scalar receiver
would need its own `q,p,gradient_x,gradient_y,gradient_z` in the discussed
representation: five channels, exceeding protected44's four-slot reserve.

**Choose one physically accounted interaction before assigning the four
slots.** Derive source and receiver forces from one declared interaction,
include its stress/current and geometric work, and prove an actual discrete
exchange identity. An onsite oscillator with two or four fields is not by
itself a transported3D apparatus. A force that fits cubic degree alone is
insufficient: its geometry source, auxiliary constraints, gauge transport and
schedule must also compile within the same degree/locality/allocation. First
controls are reciprocal versus one-way coupling, zero interaction, source
removal and exact history intervention.

**Then reuse that interaction for local preference rather than append a
second observer bank.** Any alleged structural selection must have a causal
path from retained local history back into later carrier structure. Require
two seeds identical in all source variables but different in declared history,
a demonstrated future structural difference within the causal cone, and a
disconnected negative control. A first-step Boolean maximum and a one-way
intensity response do not meet this condition. Keep the other team's fixed
burst/phase-motif protocol, periodic controls and documented proxy ambiguities;
do not rename intensity or integer growth as structural growth.

## External handoffs inspected, not silently imported

- [Issue45 actual48 feedback/motif audit](https://github.com/Closer24/Universe24/issues/45#issuecomment-6804545655):
  zero source-feedback monomials, blocked burst horizon and frozen-random
  ambiguity. This is reported external evidence pending its source PR.
- [Issue41 massive-clock port handoff](https://github.com/Closer24/Universe24/issues/41#issuecomment-6804596958):
  three-update global-rotation audit, not a full clock period.
- [Issue40 native integer coordinate proposal](https://github.com/Closer24/Universe24/issues/40#issuecomment-6804592069):
  exact algebra claim and restricted controls, not a GR compiler handoff.

General Einstein convergence, operational measurement, Born/Bell, quantum
antiparticle behavior and recurrent structural growth remain unestablished.
The integration map supplies concrete shared ports and falsifiers; it is not
a claim that eight individually useful controls solve all those gates.
