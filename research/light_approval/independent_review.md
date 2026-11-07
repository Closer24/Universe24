# Independent audit: signal approval and click correlations

## Decision

The recorded computations are reproducible and obey the reference Rule3 dynamics. They do **not** demonstrate quantum entanglement or a successful autonomous approval latch. The first experiment produces a precisely identifiable common-cause detection correlation. The second rejects both tested two-source preparations against their registered waiting and confirmation criteria.

An audit passing means that the retained states and reported observations are correct. It does not turn a failed scientific prediction into a successful one.

## Audited scope and commands

Base model: `5894510ada12d22f17a70f93a41ec311aef13265`.

```bash
python -m research.light_approval.audit \
  --evidence research/light_approval/evidence/primary_v1 \
  --approval-evidence research/light_approval/evidence/approval_v1
python -m unittest discover -s tests -p test_light_approval_audit.py -v
```

The [audit script](audit.py) uses the existing [exact matrix oracle](../component_review/audit.py), whose routing is derived independently in `research/reference/algebra.py`. It does not import the production updater, the production coupling tables or either study's observation function.

| Study | Runs | Complete states | Independent forward checks | Independent inverse checks |
| --- | ---: | ---: | ---: | ---: |
| Paired receivers | 84 | 1,428 | 1,344 | 1,344 |
| Autonomous approval probe | 8 | 264 | 256 | 256 |
| Total | 92 | 1,692 | 1,600 | 1,600 |

All checks passed in approximately four CPU seconds on the audit environment. The complete report is [audit.json](audit.json). Every initial state was also reconstructed independently from the registered positions, source counters, guide remainders and receiver settings. Every retained state hash, fixed tensor fingerprint, full 48-channel receiver trace and actual six-neighbor input trace was verified. All registered source fingerprints still match.

Two corruption regressions passed: a modified state with its original hash is rejected by the hash check, and a modified state with a newly computed hash is rejected by the independent forward oracle. These tests check detection of incorrect evidence, not merely agreement with the production summary.

The protocol files and registration hashes match those supplied before outcome inspection. This is a recorded prospective workflow, not an independently timestamped registration service. No adaptive parameter search or changed click definition is included in these studies.

## Primary result: shared detection, not derived entanglement

The [primary protocol](protocol.json) fixes a single `L=97` board, the `+++` tensor, horizon 16, and receiver positions `(32,24,48)` and `(32,72,48)`. The toroidal receiver separation is 48, greater than the combined backward-cone radius 32. Each receiver's setting changes exactly its own initial channel 0 and 14 remainders. No other initial address changes when only that setting changes.

The complete local receiver trajectories were identical across the remote setting and remote source phase for all 20 applicable signature groups. The initial support enlarged by the horizon fits inside the coordinate cube, so no periodic seam affects this audit. All four source-absent full boards remain stationary.

All trials, including no-click outcome `0`, are retained in the primary correlations. The audit independently obtains:

| Ensemble | Trials per setting pair | Joint clicks per pair | `(E00,E01,E10,E11)` over all trials | All-trial CHSH magnitude | Paired-click-conditioned CHSH |
| --- | ---: | ---: | --- | ---: | ---: |
| Shared source phase | 4 | 2 | `(1/2,-1/2,-1/2,1/2)` | 1 | 2 |
| Independent source phases | 16 | 4 | `(1/4,-1/4,-1/4,1/4)` | 1/2 | 2 |
| Sources absent | 1 | 0 | `(0,0,0,0)` | 0 | Undefined: no paired detections |

The exact finite response table has a simple explanation:

`A(x,p) = (-1)^x d(p)` and `B(y,q) = (-1)^y d(q)`,

where `d(p)=1` only for a present source with phase index 0 or 3; it is zero for phases 1 and 2 and for absent sources. Therefore the local preparation setting fixes the sign whenever a first click occurs. Sharing the source phase correlates **whether a detection occurs**. This is a direct description of every enumerated trial, not a new prediction for untested preparations.

For phase 0 the first primary click is at step `8+2*setting`; for phase 3 it is at `9+2*setting`. Each detected receiver then produces another primary C event exactly two board updates later. There are 80 detected receiver instances among the 168 receiver observations. None retains its first-click magnitude or remainder pair unchanged through step 16.

The first-click sign is an externally recorded trajectory statistic. It has not been shown to be a persistent internal signed memory. A local signal response is demonstrated; an internal operation that approves an alternative and suppresses every premature or later confirmation is not.

## Secondary result: the proposed waiting interface fails in its tested family

The [secondary protocol](approval_protocol.json) fixes `L=101`, horizon 32, a receiver at `(50,50,50)` with initial remainder pair `(2,4)`, and two preloaded sources at offsets `-8` and `+16`. Both prespecified right-source signs are crossed with all four source-presence masks. These are new prospective trajectories, not externally prescribed input values.

The independent audit accepts **zero of the two phase families**. In each family only the null-control predicate passes. The isolated-source quietness, four-state pending interval, unique joint event, approval window and eight-state retained-record requirements all fail.

The most direct counterexample is the first-source-only control. Its actual paired input first becomes `(1,-1)` in state 7, affecting the update to state 8. The declared pending state is present only at states 8 and 9. A C event already occurs at update 10, followed by further events. In the joint preparations the first C also occurs at update 10, earlier than the registered approval window `[15,19]`. The exact confirmed-record predicate is never reached in any of these eight trajectories.

These are failures of the stated preparations and interface requirements. They do not prove that every possible initial-state implementation of a reversible approval mechanism is impossible.

## Why filtering approved clicks can mislead

The script separately enumerates all 16 deterministic binary local response tables and all 81 ternary tables, including no-click zero. Every table has CHSH magnitude at most 2. This is an exact finite check of the elementary algebra, not a Rule3 simulation or a physical experiment.

A second **synthetic control, explicitly not Rule3**, demonstrates selection bias. Choose a uniform setting-independent hidden variable `lambda=(u,v,s)` with `u,v` binary and `s` equally likely to be `-1` or `+1`. Let

`A(a,lambda) = s if a=u, otherwise 0`,

`B(b,lambda) = s*(-1)^(u*v) if b=v, otherwise 0`.

Each response is local. Over all trials, CHSH equals 1. If only trials with both nonzero outcomes are retained, CHSH becomes 4. Every setting pair has the same joint detection probability `1/4`, each local detection probability is `1/2`, and the accepted outcome means are zero. Equal rates and apparently nonsignalling accepted marginals therefore do not by themselves establish fair sampling. The retained hidden variables satisfy `(u,v)=(a,b)`, so the four accepted ensembles differ by the settings.

This counterexample does not predict a Rule3 result. It identifies a failure mode that any claim based only on approved clicks must exclude.

## Assumptions and remaining tests

| Requirement | Status in these computations | Limit of the conclusion |
| --- | --- | --- |
| Fixed local law and tensor | Verified with an independent full-state oracle | Physical light is not derived |
| Local preparation settings | Verified: only declared receiver remainder addresses change | These settings are not yet calibrated quantum measurement axes |
| Same hidden-variable weights for all four settings | Exact enumeration with fixed weights | This is a designed ensemble, not an experimental freedom-of-choice demonstration |
| Remote-setting exclusion | Complete histories agree inside the bounded detector region | Long approval waits require a new causal-separation calculation |
| No-click accounting | All zeros included in primary statistics | Coincidence-conditioned statistics have a different denominator |
| Persistent internal confirmation | Failed in the registered scopes | A first-click log is not an internal latch |
| Quantum identification | Not established | Requires operational state/measurement mapping and justified witnesses or Bell predictions |

The [locality proof](locality_proof.md) explains why finite local readouts with setting-independent hidden data obey CHSH. It also explains why many board updates during zero elapsed click-count time can still allow causal communication. The board-to-observed spacetime relation must be derived separately. CHSH at most 2 does not exclude every quantum-entangled state; it excludes the proposed Bell-nonlocal statistics under the stated assumptions.

The next bounded experiment should first establish an internal pending state and confirmed record with actual autonomous input waveforms. Source preparations or compatible guide patterns may be changed before a run. Runtime cancellation gates, externally imposed approval and deletion of losing state information are not permitted. A new search should register its waveform, isolation, retention and resource criteria before evaluating candidates, preserve the failed current protocols, and retain all trials in any later correlation test.
