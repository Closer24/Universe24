# One saved Universe24 run and its geodesic board

The code joins an explicitly massive corrected full-frame tensor to the existing
bundle/runtime and derives the event board from that saved run. It consolidates
the complementary #47–#50 proposals as source-only evidence. It does not append
their independent apparatus allocations or introduce another Engine.

```bash
python -m validation.geodesic_board --out runs/geodesic-board
python -m universe24 verify --run runs/geodesic-board/runtime
python -m unittest universe24.tests.test_geodesic_board -v
```

Open `runs/geodesic-board/board.html`. The standalone HTML contains the saved
display data and works offline. `runtime/` contains the exact bundle, complete
trace, arithmetic clicks and replay report. `board_data.json`, the four audit
reports and `evidence.json` retain identities and source/output hashes. Reports
and plots are passive: none of this history is input to a later Engine update.

## Shared physical and software boundary

The default preparation has 45 channels (135 retained integers per node), 889
degree-two monomials, 27 nodes and four updates of dt=1/32, at dx=1/4. Units are
c=8πG=m=1. The initial homogeneous state is B=I, K=-I, phi=2, Pi=0 and signed
dust amplitude=1; all other matter fields vanish. Its energy density is 3 and
its initial Einstein constraints vanish. Every remainder class is represented.

The metric authority is gamma_inverse=BᵀB with lapse one and shift zero.
The single tensor drives both its geometry and massive scalar/dust source.
The display derives null and timelike test paths using spatial translation
symmetry of this homogeneous saved metric. Numerical quadrature is explicitly
an observation operation, not an integer evolution callback or retained probe.
The readout validates homogeneity and nondegeneracy rather than inventing a
metric outside its supported domain.

| Result | Evidence | Scope |
| --- | --- | --- |
| Exact execution and replay | Complete states match scalar oracle; every inverse and rewind passes | Finite run, 45 total channels, strict face locality |
| Same-run material source and metric | Explicit mass=1 fingerprint; energy, dust and stress read from that trace | Homogeneous neutral preparation; no antiparticle count claim |
| Geodesic readout | Flat, transformed-flat, expanding, proper-time, covariance and 4D equation controls | Passive homogeneous test paths; not retained falling particles |
| Einstein constraints | First defect is exactly −7 dt²; flat control zero, massless −3 dt² | Exact discrete preservation fails |
| Finite-time refinement | At T=1/8, 2/4/8 updates improve all five homogeneous fields | Observed max-error orders about 1.08 and 1.04; no spatial/general-GR proof |
| Integer cost | Peak bits 39/186/3321 for the refinement series | Projective long-time efficiency fails; no bit normalization |
| Material clock diagnostics | U(1)-invariant expressions, global rotation and same-source checks | No complete period, winding register or operational clock |
| Quantum protocol checks | All-emission reader, nondetections, exclusivity and local CHSH bound | No Engine Born law or Bell apparatus |

Passing a regression that confirms a counterexample is software success and
physical failure. The board keeps that distinction visible. Its offline
renderer checks internal identities and recalculates paths; these checks are
not a signature authenticating arbitrary externally supplied JSON. Reproduce
the exact runtime and independent audits for physical provenance.

## Eight-agent contributions

| Work package | Report | Executable |
| --- | --- | --- |
| Massive law and saved run | [Law](law.md) | `validation.geodesic_board.run` |
| Independent Einstein constraint control | [Constraints](constraints.md) | `validation.geodesic_board.constraint_audit` |
| Shared-metric geodesics | [Geodesics](geodesics.md) | `validation.geodesic_board.test_geodesics` |
| Interactive board and identity boundary | [Board](board.md) | `validation.geodesic_board.board` |
| Clock and apparatus source ledger | [Clocks](clocks.md) | `validation.geodesic_board.clock_audit` |
| Quantum complete-trial controls | [Quantum](quantum.md) | `validation.geodesic_board.quantum_audit` |
| Independent integration review | [Review](integration_review.md) | `validation.geodesic_board.test_integration_review` |
| Independent temporal error and cost | [Time and cost](time_cost.md) | `validation.geodesic_board.time_cost_audit` |

The six initial agents and two subsequent reviewers coordinated with each other
and with the other active researchers through issues #40 and #41. Each report
contains its derivation, source references and limits. Another team's
`validation/completion/` work and the reciprocal pointer proposal remain
separate pending an exact published source handoff and joint checks.

## Remaining work and actionable handoffs

1. Derive a constraint-compatible temporal encoding. A correction proportional
   to constraints that vanish initially cannot remove the measured first-step
   defect. Preserve exact inversion without projection or a changed divisor.
2. Replace the projective denominator construction or establish an affordable
   bounded-horizon domain with all arithmetic workspace counted. Its current
   denominator obeys D_n≥32^(2^n) for the audited family.
3. Prove sourced nonlinear constraint propagation and metric nondegeneracy,
   then run transverse/oblique, boundary, space/time/quantization refinement.
4. Allocate at most three remaining channels jointly to apparatus and record
   dynamics. The old four-receiver attachment would require 49. A cubic
   homogeneous pointer proposal needs a stable energy and spatial transport
   account before it can serve as physical apparatus.
5. Derive exclusive detector outcomes and their probability measure. Under
   local responses, a setting-independent shared ensemble and bounded outcomes,
   CHSH≤2; coincidence selection is not a solution. Explicitly identify any
   changed assumption and its operational predictions before claiming Bell.
6. Keep complexity/selection work in #45 tied to the same allocation and source
   ledger. This board establishes neither recurrent bursts nor increasing
   structural complexity.

No general Einstein, quantum, antiparticle or complexity acceptance gate is
closed by this integration.
