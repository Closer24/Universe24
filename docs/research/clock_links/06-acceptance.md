# Independent acceptance review of the 48-channel clock-link proposal

The review accepts the demonstrated finite-run mechanical bridge. It does not
accept a physical clock, a Born measurement, Einstein convergence, or a
complexity-selection law. The four new retained records share the original
board and execution path; they do not feed back into the original carrier.

## Scope and reproducibility

The implementation base is main
`4c494c1188f70eb8a677bf59765cc6e8571c6b88`. The 44-channel tensor and preparation
come through the existing explicitly pinned #42 compatibility export in
`validation.team48_contract`; its unconstrained preparation and geometric
failures are not relabelled. `append_phase_observers` adds exactly four channels
without changing the original 44-channel law.

The integrated tensor fingerprint is
`094bb4edbe243e4f7654073e64688ebc7b56d951724a21a0f3af1526153df611`.
The supplied zero-apparatus bundle identity is
`f15c3c342d4a9ee807640fcd6357996a1c878cb43e448f8371e3a6b6b662fad9`.

```bash
python -m unittest universe24.tests.test_clock_link_acceptance -v
python -m validation.clock_links.acceptance_audit \
  --bundle runs/clock_links/phase/run/bundle \
  --out runs/clock_links/acceptance-final --steps 3
```

The output path must be new or empty. The audit stores its own source hash,
complete input bundle, full trace, canonical records, runtime replay report and
independent report. Fresh results are under `runs/`; this document records their
scope, not a replacement for the saved complete-state evidence.

## Independent method

The expected state is computed by scalar loops over the serialized tensor,
with coordinate arithmetic implemented directly and Python integers for every
product, sum and `divmod`. It does not call `Engine.step`, the production
tensor evaluator, or the new `relation_values` helper. Production evolution is
compared with this oracle for every `a`, `b` and `r`. Every saved transition is
read back and independently checked as well.

Support, degree and old-`a` dependency acyclicity are also recomputed without
calling the tensor's certificate methods. Physical link endpoints are included
in support. The independent source projection reconstructs the original
44-channel tensor and verifies its fingerprint before comparing it against
both original and intervened apparatus histories.

## Results

| Check | Finite-run evidence |
| --- | --- |
| Retained allocation | 48 channels, 144 integers per node, 27 nodes |
| Tensor | 613 terms: 593 cubic source terms and 20 quadratic apparatus terms |
| Support and inverse dependencies | Strict single-face support; two acyclic inverse stages |
| Independent complete-state comparisons | 58,320 integer comparisons: three supplied-seed updates and two updates for each of six uniform carry stress seeds |
| Signed large integers | Negative 101-bit and positive 110-bit initial values; stress reaches 313 bits, with exact rewind |
| Computational cones | 21 interventions (all retained channels in each of `a`, `b`, `r`, at seven source positions); 84,672 outside-cone integer equality checks over two updates |
| Original source unchanged | 21,384 source integer comparisons against the independent original-law evolution, with two apparatus histories |
| Saved run | Three complete transitions, 3,461 canonical arithmetic records, exact replay and independent saved-state oracle |
| Passive decoder | First-step membership, quotient and class agree independently; retained states and tensor unchanged |
| Focused regressions | Five acceptance tests pass; both fixed-divisor guard tests also pass |

The cone interventions cover all signed axes and periodic seams. They establish
the tested **computational** causal bound. They do not identify that bound with
the null cone of a validated physical metric. Stress seeds are deliberately
mechanical; they are not claimed to satisfy gravitational constraints.

## Scientific counterexamples and limitations

The observer recurrence has `u=3I`, hence
`ell=I`, `r_next=r`, `a_next=b`, `b_next=I-a`. Its arithmetic class is C0.
For constant even positive intensity, a receiver prepared with `a=b=I/2`
is stationary. The canonical rule excludes unchanged triples, so it produces
no event despite positive intensity. A zero-drive receiver can retain and
change hidden history while producing no event because its quotient is zero.
Both counterexamples are executable tests. Click absence cannot reconstruct
intensity, and quotient weights cannot be substituted for binary frequencies.

The independence certificate supplies a stronger conclusion than a seed
search: no source-targeted monomial reads any apparatus channel. Therefore
arbitrary changes in apparatus history **cannot** affect future carrier
structure under this tensor. Apparatus backreaction is absent; local
complexity selection through these four records is blocked by construction.
This result does not forbid a future different tensor with a compatible
feedback interaction, but it rules out claiming that this one implements one.

The structural audit was reviewed for checkpoint/event indexing and includes
its frozen-random ambiguity. Its short integrated horizon cannot meet the
preregistered minimum of four interior event peaks. The observer protocol was
reviewed for declared ports, all windows, none/single/multiple categories,
canonical order and hidden-state separation; no source-state reader enters its
records-only API. A count of multiple records at a four-port receiver window
is an arithmetic fact, not by itself a quantum emission protocol.

The actual two-detector Born calibration and its failed binary-frequency and
one-outcome gates are reported in `05-born-bell.md`. The independent acceptance
program alone leaves those scientific tests unassessed; the combined study
must retain the calibration's explicit failures. A green software suite is
not a physical acceptance decision.

## Peer corrections

Review requested full saved-control provenance and independent readback of the
Born calibration file, in addition to in-memory reversal. The calibration
agent added raw phase and indistinguishability transitions and uses the
independent scalar oracle for saved trials. The phase agent was asked to save
complete control seeds/transitions and hash the shared model source. These
checks preserve the exact distinction between repeatable code and already
verified saved evidence.
