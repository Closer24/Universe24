# Light approval research

This prospective study examines signal-dependent arithmetic events, prepared common-cause correlations, local waiting records and the distinction between selected clicks and quantum entanglement. It preserves the fixed Rule3 engine. Base commit: `5894510ada12d22f17a70f93a41ec311aef13265`.

Start with the [integrated report](../../docs/LIGHT_APPROVAL_ENTANGLEMENT.md).

| Item | Purpose |
|---|---|
| [protocol.json](protocol.json) | Frozen 84-run preparation, readout, controls, horizon and budget |
| [compute.py](compute.py) | Generic component composition, full recording and exact finite statistics |
| [primary result](evidence/primary_v1/result.json) | Counts, complete-state hashes, inverse results and all-trial/conditional statistics |
| [Presenter](evidence/primary_v1/The_Presenter.html) | Eight prospectively selected recordings in the unchanged generic viewer |
| [audit.py](audit.py), [audit.json](audit.json) | Independent full-state matrix audit and explicitly synthetic selection control |
| [independent review](independent_review.md) | Verified scope, all-state counts, failure criteria and corruption regressions |
| [publication validation](evidence/publication_v1/validation.json) | All 129 tests passed in a fresh Git checkout; exact tested tree and retained log |
| [locality proof](locality_proof.md) | Exact causal cones, local factorization and full-trial CHSH bound |
| [approval mechanism](approval_mechanism.md) | Conditional write–wait–confirm algebra and missing whole-board waveform |
| [approval protocol](approval_protocol.json), [probe](approval_probe.py), [result](evidence/approval_v1/result.json) | Separate eight-run autonomous two-arrival probe; both registered families fail the strict approval criterion |
| [physics review](physics_review.md) | Primary sources, quantum interpretation requirements and selection loopholes |

Run from the repository root; use a new output directory:

```bash
python -m research.light_approval.compute --output runs/light-approval-reproduction
python -m research.light_approval.approval_probe --output runs/two-arrival-reproduction
python -m research.light_approval.audit --evidence runs/light-approval-reproduction --approval-evidence runs/two-arrival-reproduction --output runs/light-approval-audit.json
python -m unittest discover -s tests -p test_light_approval_audit.py -v
```

The primary study completed 84 runs, 1,428 full states and 1,344 transitions. The independent oracle checked every forward and inverse transition. Shared-phase full-trial CHSH is 1; independent-phase CHSH is 1/2. Both-click conditioned CHSH is 2 in both cases. No Bell violation or quantum-entanglement derivation is claimed.

All 80 clicked receiver instances have later primary clicks; zero meet the registered constant-magnitude or constant-remainder-pair criterion continuously from their first click through step 16. This does not rule out later finite plateaus. The source-absent whole boards are stationary.

The additional two-arrival probe has eight runs, 264 full states and 256 transitions. Both registered phase families fail the strict pending/confirmation criteria: the first isolated source already causes receiver C at step 10. Across both studies there are 92 runs, 1,692 full states and 1,600 transitions. The [secondary Presenter](evidence/approval_v1/The_Presenter.html) contains every source control.

The separate synthetic local-response control gives full-trial CHSH 1 and coincidence-selected CHSH 4. It is not a Rule3 run or a physical measurement. Its role is to demonstrate why accepting only selected clicks can invalidate an otherwise appropriate comparison.
