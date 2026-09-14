# Local moment response after quantum capture

This explicit candidate connects a captured, held record to subsequent ordinary
motion through an existing generic local interaction. It transfers uncertainty
to a colocated reservoir rather than interpreting unknown momentum as zero.
It is a moment-closure hybrid, not a derived quantum-to-classical limit.

## Candidate contract

| Part | Definition |
| --- | --- |
| Law | Swap the pair's coarse mean momentum, trace of momentum covariance and validity marker; copy their individual masses and charges |
| Input owners | One captured unit-mass record and one unit-mass reservoir that arrives through ordinary Links |
| Evolving state | Existing generic vector `coarse_momentum`, scalar `momentum_spread`, validity marker and ordinary bounded transport metadata |
| Initial moments | Target: mean zero, variance one, unresolved; reservoir: signed axial mean three, variance zero, resolved |
| Parameters | Equal unit masses; 300 momentum units per unit mass times c; ordinary rate numerator is the L1 mean magnitude, denominator 300 |
| Outputs | Two replacement types in the same slots; a second local conversion records detector completion and retains the recoil record |
| Consistency | Pair mean sum and variance sum are conserved; `sum(dot(mean,mean)+variance)` is an exact pair invariant; local checks reject non-unit body masses and inconsistent validity |
| Capacity and timing | No new slots, state banks or quantum modes; actual arrival precedes a frozen local computation delay and simultaneous commit |
| Scope | Schema 1, no converted emitters or spatial field response, fixed one-shot contact domain |

The initial zero mean is supplied together with **nonzero variance**. It does
not state that the target's microscopic momentum equals zero. For equal unit
masses, `dot(mean,mean)+variance` is twice expected nonrelativistic kinetic energy
in the declared momentum units. The pair's value is initially `1+9=10` and after
exchange `9+1=10`. This is expectation-level closure in the ordinary runtime;
it does not store each momentum branch, phases or cross-record correlations.

Both replacement types are distinct from both inputs. The second conversion
changes the spent reservoir and detector into `stored_recoil` and `retired_probe`,
copying every payload. This local one-shot lifecycle prevents repeated capture
attempts from blocking the slow carrier's ordinary cycles. The uncertain recoil
keeps mean zero and variance one; it is retained locally, without modeled spreading.

The quantum capture remains held with unknown momentum as required by the
[contact contract](../../docs/LOCALIZED_QUANTUM_CONTACT.md). The later conversion
uses [existing bounded local conversion](../../docs/LOCAL_CONVERSIONS.md), with
both sides already at the same Node. No global audit, remote quantum query,
diagnostic estimate or new force supplies its physical update.

## Reproduce

Use the project Python environment with `PYTHONPATH=src`:

```sh
python examples/quantum/run_local_moment_exchange.py --output artifacts/local-moment-result
```

[local_moment_exchange.py](local_moment_exchange.py) authors the complete JSON
input from [localized_charge.json](localized_charge.json). The output folder
contains `input.json`, the primary runner's complete `native` recording, and a
`summary.json` containing all audits. The saved input can also be run directly
with `python -m event_universe --init INPUT --output FRESH_OUTPUT`. No simulator
build or visualization is needed. Generated inputs and output evidence have
24-hour retention; the authoring code and this report remain versioned.

## Observed default sequence

The table lists Event ticks. Snapshots separately record their completed audit
tick: the exchange at Event tick 300 first appears in the audit at tick 301.

| Event tick | Local event |
| ---: | --- |
| 0 | Initial source transfers its inventory to the finite spatial wave |
| 2 | Capture creates a held record at coordinate 3 on the chosen axis |
| 99, 199, 299 | The independent reservoir departs along its three incoming Links |
| 300 | Both local conversions commit: moments swap and the detector records completion |
| 399, 499, 599 | Target departs toward coordinates 4, 5 and 6 for the positive orientation |
| 699 | Target exits the open world, with explicit escaped inventory accounting |

All six signed axes pass. With no reservoir the target remains held, mean zero,
variance one and unresolved. With three-tick Links, capture occurs at 6, exchange
at 900 and the first target departure at 1197. With normal budget 20, exchange
commits at 302 and first departure at 501: the local computation delay is real.
Original owners remain present while the response is pending.

Every audited tick balances mass, charge, mean momentum and variance across
ordinary residents, in-flight packets, the single quantum inventory and escaped
content. The independent energy readout also includes escaped energy. Missing
moment fields fault; unit-mass scope is checked. A deliberately unbalanced
response with the same mean sum fails the nonlinear invariant before conversion.
Renamed fields/types retain the result. Nominal transport is c/100; computation
delay changes world-time motion, so a universal world-time `velocity=p/m`
relation and relativistic energy are not established.

## Independent exact quantum control

[momentum_state_exchange.py](momentum_state_exchange.py) uses the existing quantum
owner with two co-located four-level registers. A target state
`(|-1>+|+1>)/sqrt(2)` and environment `|+3>` undergo a supplied SWAP. The target
receives `|+3>` and the environment receives the complete original state.

Both branches preserve total momentum (2 or 4) and doubled kinetic energy 10.
All sixteen basis combinations, an unequal 3:4 superposition, no exchange,
coherent reversal and an explicit dephasing control pass. Reversing retained
states restores interference; dephasing the environment prevents that recovery.
There are no sampled measurement records in this control.

This is a separate full-state check. It does not give the ordinary moment fields
quantum coherence or joint correlations. Neither experiment supplies canonical
position/momentum operators or claims simultaneous exact position and momentum.
Local state exchange is an established collision-model mechanism, not a new
discovery; see [Ziman et al., Quantum homogenization](https://arxiv.org/abs/quant-ph/0110164).

## Remaining gap and implementation correction

Spatial amplitudes do not derive the captured mean and variance. A complete
continuation needs a joint spatial/momentum state, environmental recoil and
spreading, compatible classical field sources, and quantitative classical-limit
acceptance under the same dynamics. This candidate supplies an explicit local
response and slow path while retaining those limits.

The experiment also exposed an existing receipt defect: a delivered record
selected an empty slot reserved by a pending capture although another slot was
free. `RecordOperations.receive` now selects the first unlocked empty slot.
Eight regression cases failed before the correction; afterward the two affected
test modules passed 71 tests. A delayed-capture regression receives a messenger
in spare slot 2 at tick 4 and completes capture at tick 11, preserving both
owners. True capacity exhaustion still rejects the whole proposal. This fixes
the existing lock contract and adds no physical law.

Work is based on `3a2fdfd`, which includes the unmerged PR #100 candidate. Exact
source and final checks are recorded in [validation](../../docs/VALIDATION.md).
Physics review accepts the bounded expectation-level scope. The physics review
Skill now explicitly checks missing momentum versus zero mean and nonzero
variance. Boss, configuration and runner Skills need no additional workflow.
