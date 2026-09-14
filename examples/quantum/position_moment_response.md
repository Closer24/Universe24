# Spatial momentum and local position output

`position-reencoding-local-moment-response-candidate-v1` derives post-capture
moments from a finite spatial operator, extending the previous
[moment experiment](local_moment_exchange.md). A separate diagnostic reads
actual evolving quantum density, including phase correlations. This is not
a derivation of closed quantum-to-classical dynamics.

## Definition and ownership

| Part | Contract |
| --- | --- |
| Observable | Edge `(a,b)` defines `P[a,b]=-i`, `P[b,a]=+i`; all other entries, including the diagonal, are zero. Edges must follow neighboring Links. |
| Exact readout | `mean=Tr(rho P)`, `second=Tr(rho P^2)`, `variance=second-mean^2`, from actual reduced density. |
| Local output | Position capture re-encodes its ordinary carrier as a position basis state. Mean is zero; variance is the sum of squared coefficients in the local operator row. |
| Physical preparation | At most six signed unit coefficients, bounded integer results. No state query, global normalization, formula or callback enters NodeState. |
| Runtime | The existing contact installs its prepared output at delayed commit. A later generic pair conversion exchanges moments with an arriving equal-mass reservoir. |
| Accounting | Mass and charge remain conserved inventory. Moments are metadata during quantum transitions; ordinary pair conversions explicitly guard first moment, second moment and variance sum. |
| Diagnosis | Exact rational density arithmetic and world sums are external read-only work. They never control outputs, repair inventory or contribute to ordinary delay. |

This **supplied finite derivative observable** has chosen units. On a periodic
chain its Fourier eigenvalue is `2 sin(k)`, not continuum momentum `hbar*k`.
The straight-chain example selects an axial component; the square-loop control
measures circulation around the loop, not one Cartesian component. Canonical
commutators, dispersion and a free-particle Hamiltonian are not established.
Ordinary transport retains the earlier scale of 300 momentum units per unit
mass times c.

Absorption leaves actual quantum **vacuum**, whose particle moments are
unavailable. The output's position-state re-encoding is an explicit additional
interpretation. Authoring derives source and output values independently from
their local rows and writes complete JSON. The engine does not query a global
wave observable or identify physical names.

The source is an endpoint of a three-mode chain, so its variance is 1. Endpoint
capture derives 1; middle capture derives 2. Each input has a single capture
location. Multiple locations with different rows would require matching local
outputs; one arbitrary template cannot represent all detectors.

## Independent quantum expectations

The first four states below have identical position probabilities:

| Four-mode ring state | Mean | Variance |
| --- | --- | --- |
| `(1,i,-1,-i)/2` | 2 | 0 |
| Complex conjugate | -2 | 0 |
| Uniform real coherent wave | 0 | 0 |
| Uniform incoherent mixture | 0 | 2 |
| Any position basis state | 0 | 2 |

Three-mode endpoint superpositions `(1,0,1)/sqrt(2)` and `(1,0,-1)/sqrt(2)`
also have identical probabilities and zero mean, but variances 0 and 2.
Density or nearest-edge current cannot replace the required phase correlations.
The implementation uses integer complex pairs; square roots here describe
normalized expectations only.

The independent projective control retains a position state after a click to
verify re-encoding. Native absorption instead retains vacuum. Both click at a
selected ring Node with probability 1/4. For the positive-phase wave:

| Event/readout | Probability | Mean | Second moment |
| --- | --- | --- | --- |
| Before measurement | 1 | 2 | 4 |
| Click | 1/4 | 0 | 2 |
| No click | 3/4 | 4/3 | 10/3 |
| Nonselective ensemble after | 1 | 1 | 3 |

Ensemble operation changes are -1 for each moment; the selected click changes
each by -2. The report separates conditional selection from ensemble drift.
There is no invented apparatus stock or inferred physical recoil. The real
uniform wave instead has second-moment ensemble drift +1 despite the same
click probability and output.

## Native execution and unresolved energy

Existing neighboring SWAPs change the derivative observable's second moment
`1 -> 2 -> 1` along the chain. Including reservoir second moment 9, the actual
combined audit gives `10 -> 11 -> 10`. Middle capture terminates at 11.
These are visible unclosed operation changes, not a simulated apparatus exchange.
Keeping old spread1 as fixed quantum inventory would hide this discrepancy.

After capture, ordinary pair and transport preserve mean and second moment,
including actual open-boundary escape. Middle variance2 transfers to the
reservoir; the target acquires supplied mean3 and variance0. Unit masses,
validity, capacity and computation waits remain enforced. Broken proposals
preserving only mean or only energy are rejected before conversion.

Default source/capture Events are at ticks0/1 for middle, or0/2 for endpoint.
Pair conversion occurs at300; first target send at399. Snapshot audit ticks
are recorded separately. Acceptance covers six directions, absent reservoir,
Link time3, budget20, generic names, bounded Node state and unchanged native
trace/cost with diagnostics enabled or disabled. Runs are headless without builds.

```powershell
$env:PYTHONPATH = "$PWD/src;$PWD"
python -m examples.quantum.run_position_moment_response --output artifacts/position-moments
```

Use the existing project Python3.14 interpreter and a fresh output directory.
Saved `input.json` runs directly with `python -m event_universe --init ...`.
Generated results and native traces expire after 24 hours. Authoring code and
this report remain in Git. Exact checks are in [validation](../../docs/VALIDATION.md).

## Remaining work

This derives **post-position-output moments** and diagnoses **incident wave
moments**. It does not infer incident direction in an ordinary record, replace
the supplied reservoir momentum or SWAP, model uncertainty spreading in that
reservoir, or close gate/measurement/field energy. A complete model needs a local
apparatus and quantum interaction that account for joint momentum and energy,
with compatible propagation. A global diagnostic residual is not that law.
Converted emitters and spatial source envelopes retain their previous limits.
No old profile, binding postulate or production source changes in this experiment.
