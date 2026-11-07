# Prepared signal–clock–memory experiment (2026-11-07)

## Decision and evidence level

**A reproducible prepared activation front writes a local 34-update record and starts a period-four counter clock under unchanged Rule3.** This is a finite computational result for the positive-reference candidate, not a proof for all preparations, a stable moving particle, a permanent detector, or a physical measurement theory. No core file was changed.

Baseline: `ed1556e202eb0f3cc60342c75d44012c2eeb71c3`; body signs `(1,1,1)`; coupling SHA-256 `44b672d96111e71a145a2a74cc93c83d41d917140e979186c308a5ecd52c6f77`. The preparation follows research-document A11; its previously claimed window was independently reproduced with the repository engine. Numerical precision is exact Python integers; tolerances are zero.

The initial protocol failed an **extra assertion that the record remains zero at all later sampled times**. That failure is retained. A second protocol preserved the observer and tested the actual first-window claim prospectively on a new guide length. This distinction prevents declaring the failed initial experiment successful after changing its acceptance criterion.

## Operational definitions, fixed before execution

All channels not explicitly prepared are `(a,b,r)=(0,0,2)`. Place a source at x-coordinate `x0` on the guide's y,z row; channels 0 and 14 respectively start `(0,1,2)` and `(0,-1,2)`. Receivers at `x0+j`, `j=1,...,N`, have `(0,0,4)` and `(0,0,0)`. The deterministic generator fixes `x0=L//2-N//2`, `y=z=L//2`. No RNG is used. Complete preparations and final states are saved as engine checkpoints.

| Component | Preparation/environment | Input/output | Response/range |
| --- | --- | --- | --- |
| Signal | Source pair and finite prepared x-axis guide | Initial source amplitude launches an activation front | Receiver j first has nonzero channel-0 b at reference t=j; tested N=18,20,22 |
| Local clock | The two receiver channels in the same board | Arrival starts channel-0 `(a,b)` sequence `(0,1),(1,0),(0,-1),(-1,0)`; channel14 counters have opposite signs | Exact projected period 4 within the first record window |
| Memory | Receiver remainder pair initially `(4,0)` | Fixed local bit `M=1 iff (r0,r14)=(0,4)`, otherwise 0 | Record window `[j,2(N+1)-j)`; 34 sampled updates in the tested detector choices |
| Click | Passive reading of the same two local channels | `M(t-1)=0 and M(t)=1` | First click at t=j; observer makes no state changes |

“Clock” here means the defined local projection, **not periodicity of the whole evolving board or configuration**. “Mobile signal” means a front of activation traveling through prepared receivers, **not a compact full-state pattern satisfying a translation identity**. All source, guide, clock and memory dynamics are the same channel states evolved by the same engine. The log is external evidence; the recorded bit is read from the internal remainder pair.

## Frozen protocols and results

The protocol files were written before their respective runs. Version 1 observations preceded the decision to register version 2; both are retained with their hashes in the results. These are within-session preregistrations, not independent timestamped registrations.

| Case | L | N, target j | First record window | Click times sampled | Outcome |
| --- | --- | --- | --- | --- | --- |
| v1 baseline | 101 | 18,2 | `[2,36)` | 2,40 (through t40) | First window/clock pass; no-later-record assertion fails |
| v1 larger cube | 121 | 18,2 | `[2,36)` | 2,40 | Complete translated trace matches L101 exactly |
| v1 held-out length | 121 | 20,4 | `[4,38)` | 4 (through t44) | v1 checks pass |
| No source | 101 | 18,2 | None | None | Negative control passes |
| Source, no prepared guide | 101 | 18,2 | None | None | Negative control passes |
| Missing prepared pair at j3 | 101 | 18,4 | None | None | Target beyond gap does not click |
| Target channel-0 r perturbed 4→5 | 101 | 18,2 | None under fixed M | None | Clock persists but exact memory readout fails |
| v2 fresh length | 141 | 22,6 | `[6,40)` | 6,52 (through t60) | Preregistered first-window criteria pass |
| v2 larger cube | 161 | 22,6 | `[6,40)` | 6,52 | Complete translated trace matches L141 exactly |

Every unperturbed prepared receiver first activates at t=j. Every checked forward step has exact inverse, and every run is rewound from final state all the way to its initial full state. The nine runs use 404 forward steps total, plus one-step and trajectory inverse audits; maximum sparse support is 146 explicitly stored channels. The logical cubes still have all `48L^3` channels. The initial runs took approximately 0.31 CPU seconds combined on Python 3.12.14; machine timings vary. Budgets were 120 CPU seconds per protocol, 100,000 explicitly stored channels, and the declared fixed step counts.

The one-neighbor causal bound excludes boundary crossing for L101/N18 through t40 (margin 41), L121/N20 through t44 (margin 50), and L161/N22 through t60 (margin 69). The smaller v2 cube L141 has margin 59, so that bound alone does not exclude crossing by t60. Its complete translated trace nevertheless matches the causally isolated L161 run exactly for every sampled state, which supplies the finite-run boundary control. Size comparisons check complete sparse states, rather than only detector readouts.

## Failures and information retention

The target's first record ends reversibly, and the same preparation later clicks again. The device therefore does not establish permanent retention, an exclusive one-shot outcome, or reusable ready-state restoration. In the N18 run, at t36 the memory bit returns to zero but the local triples are `(0,-2,4)` and `(0,2,0)`: the apparatus has not returned to its initial counters. At t37, the whole state differs from the no-source control at 104 channel addresses. A further witness at `(40,50,50,0)` is `(0,0,4)` versus `(0,0,2)` in the no-source control. Full-state inversion recovers the original source preparation. A zero readout thus does not erase the trajectory or imply quantum collapse.

The r=5 perturbation is an exact limitation: remainder parity is invariant, so the changed channel can never have the prescribed r=0 value. Its counter clock still operates within the window; the fixed memory readout rejects it. The result is certified only for the specified preparation and parity class. No broad basin of simple seeds, noise tolerance, spontaneous assembly, arbitrary signed tensor, effective clutch or bound structure has been demonstrated.

The gap control tests causal dependence on the prepared guide, not a runtime switch. A state-controlled effective clutch remains a separate research obligation.

## Reproduction and next decision

From the repository root:

```bash
python research/signal_memory/run.py
python research/signal_memory/confirm.py
python -m unittest discover -s tests -p test_signal_memory.py -v
```

The scripts intentionally regenerate their own experiment outputs. Version-1 and version-2 protocols/results have different filenames; do not remove failed version-1 evidence. The [results directory](../research/signal_memory/) contains protocols, runner hashes, source commit, coupling fingerprint, readouts, exact first-arrival times, normalized full-state trace hashes, and initial/final checkpoints. `information_witness.json` is explicitly a post hoc information-location diagnostic, not an observer change.

**Advance only to a bounded composition/robustness study.** Keep M fixed for this experiment family. First test a separately preregistered family of even-parity preparation perturbations, independent source amplitudes/phases, a second appended detector, and delayed competing signals. Success requires the specified first-window record and full inverses on held-out preparations; failure narrows the interface contract. Any alternate observer must be a new protocol, and any changed structural coupling a named separate candidate. Do not advance to claims about Born probabilities, Bell violations, gravity or general self-organization from this result.
