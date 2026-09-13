# Detector integration prototype

Development branch: `feat/quantum-detector-trial` in `Closer24/Universe24`.
Pull request: https://github.com/Closer24/Universe24/pull/7.
Original reviewed base: `e74f2fdf390b5dc8036b707eefcfc53bc8a82c17`.
The PR metadata records subsequent main synchronizations and validation.
They preserve main's English documentation, physical-feature procedure, language
gate and run-acceptance diagnostics rather than replacing main from an archive.
Merge requires successful CI and explicit approval.

## Feature contract

| Part | Contract |
| --- | --- |
| Law | Deferred Gaussian-integer source, quarter-phase and binary-sum graph; prescribed two-output absorbing readout, not general unitary dynamics |
| Inputs | Bounded integer root IDs, 3D address, world tick, amplitudes, phase count and a supplied uniform integer ticket |
| Evolving state | One DeferredQuantum owner holds the bounded graph, query cache, counters and one optional terminal record; no new physical-cell state |
| Parameters | Immutable QuantumConfig bounds max_nodes, max_eval_nodes and max_cached_results; positive bounded integers |
| Derived values | Weight is real squared plus imaginary squared; output choice is derived from two weights and the ticket |
| Outputs | Fixed-size immutable query or terminal reply; a successful call has model cost 1 and world time cost 0 under Past is Present Calc (Q-ORACLE-1) |
| Consistency | Parent edges are same-cell or six-neighbor causal hops in an unwrapped chart; failed readout cannot commit; repeated readout reuses one record |
| Tests | Four phases yield weights (4,0), (2,2), (0,4), (2,2); enumerate all tickets, test invalid inputs, bounds, repeated calls and independent engine baseline |

The authoritative model postulate is in POSTULATES.md, exact contracts in
SIMULATOR_DEFINITIONS.md and ownership rules in docs/ARCHITECTURE.md.
No existing engine, field, movement or renderer implementation is replaced.

Run `python -m pytest tests/test_quantum_detector_trial.py -q` for the trial.
Trial execution is headless by default. The existing pytest HTML visualization
path is enabled only when visual checks are explicitly requested with
`--visualize-runs`.
Full gate: `python tools/check.py`. Missing checks must not be marked PASS.

## Limits

This is a prescribed finite 3D interferometer circuit and a terminal single-
excitation detector mock, not spontaneous detector physics. The test harness
stores a single physical-side record but Engine has no detector commit API.
The background classical particle is not a duplicate quantum excitation.
There is no automatic polling, quantum-field feedback, general post-measurement
evolution, energy or momentum proof, no-signalling or Bell validation. Tickets
are exhaustively controlled inputs, not a tested randomness source. Fixed graph
nodes and bounded integers remain mandatory; total host DAG work is not constant.
