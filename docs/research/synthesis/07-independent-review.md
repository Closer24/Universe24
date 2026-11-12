# Independent integration review

Reviewed base: PR47 `621fc1f55800e50e1db5f6a30ce24bb83716a49a`.
This is the seventh review in the eight-task synthesis. It independently reads
the six control implementations and their reports, reruns the five lightweight
audits, and derives symbolic identities without importing their helpers.
The coordinator owns the fresh held-out rerun and complete repository suite;
those executions are not attributed to this review.

## Reproduced results

| Control | Independent check | Acceptance boundary |
| --- | --- | --- |
| Integer growth | Reran 7,056 scalar/carry cases and all three protected44 runs; independently verified the induction and Wronskian identity | The exponential lower bound is for this prepared recurrence, not every possible encoding |
| Projective receiver | Reran 45-channel source projection, all 81 readouts and complete rewind; obtained 80 wrong-after-denominator examples | Exact intensity weight is `ell/D_before^2`; it is not click-only reconstruction or a detector frequency |
| Bounded preference | Reran all 5,184 Boolean/carry preparations, signed cases, inverse and seam control; independently derived the period-four response | First-step supplied-bit comparison does not compute structural complexity or select monotonically |
| Compatible calculus | Reran exact derivative/product identities and eight Engine updates on 64 nodes | A linear `div curl=0` identity and scalar product correction do not establish nonlinear Einstein constraint propagation |
| Reciprocal coupling | Reran 78,732 scalar/carry cases and 72 Engine transitions; independently proved pair charge/translation and linear polarized invariance symbolically | Internal momentum and polarized invariants are not calibrated spacetime stress-energy |
| Held-out geometry | Read the frozen protocol, preparation and diagnostics code; checked the distinction between exact Engine evolution and floating reference | The reported failed combined gate must remain failed even when H and field error improve |

No material correctness defect was found in these scoped algebraic claims.
The review does not certify the scientific claims that the reports explicitly
leave unestablished. Each control's own JSON remains authoritative for its
executed source hash and numeric results. Review reruns use
`runs/synthesis/independent-*.json`; the independent symbolic artifact records
the six source hashes visible at its execution.

## Independent derivations

`validation.synthesis.independent_review` imports SymPy, not any lane's audit
helper. It expands the following identities to exact zero:

- `p_next q-q_next p = p q_old-q p_old` when both pair components share the
  same linear coefficient. Thus any current-bank common divisor divides the
  prepared nonzero Wronskian. The denominator growth bound follows separately
  from `C>=2`, `d>=2`, and `0<=D_old<D`, giving `D_next>=D^d`.
- For a reciprocal pair force `(-k d,+k d)`, the sum of both two-time planar
  charges is invariant for arbitrary symbolic `k`. Substituting a scalar
  function of `|d|^2` preserves that cancellation. The linear time-polarized
  invariant is checked only at `k=1`, not asserted for nonlinear forces.
- The centered-product defect equals the signed difference of the two
  face-increment products divided by two. This identity is scalar algebra,
  not an evolving constraint correction.

Separate rational checks reproduce scale-dependent next ratios `11/17` and
`23/35`, the Boolean truth table and the response's exact four-cycle. These
symbolic/scalar checks are deliberately not counted as extra Engine runs.

The arbitrary-integer threshold obstruction in task4 was also checked as a
proof: if a polynomial quotient stays zero on the entire nonpositive integer
half-line with fixed auxiliary state and carry, its numerator is bounded on
that half-line and therefore constant. This excludes that one-update
interface, not variable-time reversible computation or bounded encodings.

## Literature verification

Independently read Bellon and Viallet, *Algebraic entropy*,
[primary full paper](https://arxiv.org/pdf/chao-dyn/9805006), sections 1–2.
Their definition concerns reduced degrees of rational-map iterates and
permits common-factor cancellation in a projective representation. It does
not identify integer bit length with physical complexity or authorize
information-discarding normalization of Universe24's complete retained state.
Task2's literature boundary is accurate; its denominator bound is a separately
proved repository result. The attempted independent retrieval of the linked
Bennett transcription was unavailable, so this review does not claim to have
read that source; task4's elementary threshold and cycle claims do not depend
on it.

## Shared acceptance obligations

The controls cannot be added as separate channel banks: the existing44,
four-slot intensity apparatus, four-slot Boolean comparison and six-slot
incidence example are different allocations. The useful handoff is an
equation or rejection test, not their sum. In particular, the proposed46-slot
reciprocal reuse and48-slot link replacement have not been compiled into the
projective matter equations.

Before any physical promotion, one exact tensor/seed/ownership manifest must
combine compatible geometry, reciprocal source/apparatus coupling and the
chosen observer protocol, with retained history and all carries included.
Then the same candidate must pass held-out physical refinement, calibration,
budget and long-horizon cost tests. Current mechanical positives coexist with
the failed held-out convergence gate, nonconserved naive energies, uncalibrated
clocks and absent burst-growth mechanism. None is hidden by this review.

```bash
python -m validation.synthesis.independent_review --out runs/synthesis/independent_review.json
```
