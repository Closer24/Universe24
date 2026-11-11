# Tensor, initial state, locality and click audit

This audit tests the current possible implementation. It does not certify that quantum mechanics or general relativity has emerged. The default polynomial dynamics and its fingerprint remain unchanged by the fixes below.

## Results of the executable check

A 4×4×4 board was evolved for 120 updates from the default J-pure preparation with load/remainder RNG seed 13. [Machine-readable results](evidence/contract_audit.json) record the full parameters and hashes.

| Property | Result and scope |
|---|---|
| Tensor rank | 4: one output index plus at most three input factors |
| Common divisor | D = 6Q, Q = 8,589,934,593 for every gear |
| State per node | 382 triples (a,b,r), including 90 link-gear types |
| Fixed tensor | 18,592 monomials; fingerprint unchanged during the run |
| Direct scalar cross-check | 2,292 sampled gear transitions, ordinary and arbitrary-precision states; no mismatch against an independent receiver loop |
| Inverse | Exact recovery of all initial a,b,r values after 120 updates |
| Saved-input replay | Saved tensor plus complete saved seed reproduces the exact final state |
| Readout | 152,616 official records: 122,856 in matter and 29,760 in cosmic gears |
| Offline decoder | Re-reading only exported event records reproduces counts, classes, quotient sums and the selected clock series |
| Audit-only raw events | 170,659 raw rows excluded from official readout |
| Local perturbation | On L=7, 7/25/63 sites changed after 1/2/3 updates; zero differences outside the respective Manhattan cones |
| Clock diagnostic | cosmic.M1 at (0,0,0): 115 recorded events, 57 sign crossings, estimated angular rate 1.50196 per computational update |

That last number is a diagnostic of this preparation. It is not calibrated physical proper time, a mass, or a proof of a universal clock law. Likewise, the approximately 261 million units in the cosmic carry ledger are **weights**, not 261 million observed click records.

## Exactly which locality holds?

For each monomial targeting site x, all stored input registers are at x or at one face neighbor x+d. The complete input can sum terms from all six neighbors. Every output reads the same old snapshot. Induction therefore bounds forward influence by one lattice edge per update. The numerical cone test checks an instance of this structural argument.

A link gear is stored at its base node, and its axis is metadata inside the tensor. Under the geometric interpretation it spans both endpoints. When those endpoints are included, **3,300 monomials exceed a single physical link**. Their maximum Manhattan diameter is two edges. They remain finite-range local interactions; they do not meet the stronger requirement that every term occupy only one physical edge. `strict_support=True` rejects that stronger violation. Silently enabling it on the default would reject the current construction, not repair it.

A second 120-update control changed the load/remainder RNG seed from 13 to 17. It kept the same total event counts and selected clock sequence, while changing the C1/C2 counts. [Control record](evidence/contract_seed_control.json). This is a property of the prepared construction, not a general quantum probability result.

The tensor defines the internal gear layout, polynomial coefficients, source offsets, readout labels and link axes. The periodic cube and its face-neighbor geometry are explicit additional fixed inputs. They are not derived uniquely from the polynomial coefficients. Link axes describe geometric support; the offsets determine actual register access.

## What is an official click?

A transition qualifies when `ell = b_next + a` is nonzero **and** its full triple changes. `Engine.clicks(..., stream='official')` applies that arithmetic condition to all gear labels. `observe.readout.official_clicks` additionally selects only gears whose tensor label is `official`. Its name previously promised this selection without actually performing it; this is fixed.

One qualifying transition produces one record even when `abs(ell)` is much greater than one. Signed quotient weights, record counts and the number of nodes with an event are distinct measurements. The default run report now counts actual official events, retains its final partial window, and labels the older carry-weight fields explicitly. The `born` compatibility field is a state-dependent carry-weight ledger, not a general quantum probability test. New reports also expose it as `carry_weight_frequencies`.

The offline decoder takes exported events only. It does not inspect the hidden amplitudes to assign a particle name or insert an outcome into the board. No entropy optimizer, global future-path search or collapse operator was added.

## Clear and reproducible initial conditions

```bash
python -m universe24.tools.audit_contract --L 4 --steps 120 --rng 13 --out runs/contract
python -m universe24.tools.audit_contract --replay runs/contract
```

The output directory contains:

- `tensor.json`: the complete integer polynomial, gear order, labels, link axes and Q.
- `initial_state.json.gz`: every a,b,r value at every site, including the background.
- `final_state.json.gz`: complete final state for exact replay comparison.
- `official_clicks.jsonl.gz`: step, location, gear, class and signed quotient of every official event.
- `report.json`: parameters, signatures, observed counts and limits of the checks.

The default initial preparation includes a J-pure matter packet, a cosmic hand at rest, two cosmic reader packets, static loads and correlated pair remainders. RNG seed 13 controls the loads/remainders; it is not the complete initial state. The preparation uses floating-point projection and normalization before converting to integer registers. Saving the complete integer seed avoids relying on platform-dependent preparation details. Evolution and inversion use exact integer arithmetic only.

## Bugs repaired without changing the scalar law or default tensor

1. Official readout included audit-only gears despite promising to exclude them. It now filters the tensor labels.
2. Equal int64 and Python-integer states produced different state hashes. The v2 hash uses canonical exact values and geometry; comparisons reject mixing old and new hash formats.
3. The choice-class diagnostic forced large remainders into int64. It now uses exact arithmetic even for divisors beyond int64.
4. A supposedly immutable tensor could be modified after compilation, making metadata and cached execution disagree. Tensor fields and maps are now immutable, and an existing engine cannot replace its tensor or common divisor.
5. Run-report counters confused nonzero carries with changed-triple clicks, and omitted the last incomplete reporting window. They now use the declared official records and preserve that window.
6. The rotating-frame helper silently treated unsupported angles as pi/2. It now rejects unsupported carriers.

Raw-quotient electromagnetic and chiral diagnostics remain available and are explicitly documented as state-derived quantities. They cannot automatically be presented as measurements reconstructed from official clicks.

## What the physics claim still needs

The run establishes an exact local automaton, repeatable event patterns and a candidate oscillatory signal. It does not establish physical units, Lorentz or general covariance, universal gravitational response, particles, a general Born rule or Bell-consistent quantum predictions. Some initial correlations and weights are prepared by construction. A meaningful physical test must derive a quantitative prediction in the declared observable stream, with independent apparatus/calibration and controlled alternative preparations.

No observation code feeds back into the run. Exact inversion and passive measurement are necessary consistency checks, not a substitute for those physical tests.
