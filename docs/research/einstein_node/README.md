# Node laws, clocks, Einstein geometry and computational load

Eight-reviewer investigation requested by the owner, 12 November 2026.
Main source: `4c494c1188f70eb8a677bf59765cc6e8571c6b88`; published geometry
source: PR50 `62202fdccdd9a40d5dbbec104de6f97d9587a999`.

**The strongest existing unification is the common metric in the scalar and
Maxwell kinetic terms.** A controlled field-phase limit can connect that
metric to geodesics and proper time. Neither the fixed-six node rule nor a
scalar computation-load value supplies Einstein's field equations. This work
adds exact tests and a concrete next experiment; it does not promote a model,
alter the Engine, allocate channels or introduce a second metric/runtime.

## Eight completed reviews

| Review | Result |
| --- | --- |
| [1. Einstein's actual route](01_einstein_history.md) | Equivalence and clocks preceded the metric and correct sourced field equation; the 1911 half-bending result is a useful warning. |
| [2. Clock geometry](02_clock_geometry.md) | Nonuniform clocks can occur in flat spacetime; equal rest rates can occur with different curvature. Ten suitable rates identify a metric only under stated assumptions. |
| [3. Generic node algebra](03_node_algebra.md) | Reproduced native q,p and frozen parity; exact carry residual telescopes. Periodic state can have zero clicks; arbitrary legal tensors need not conserve a physical energy. |
| [4. Published geometry](04_geometry.md) | Scalar and Maxwell principal cones use the same frame. Actual45 replay passes; packet geodesics and physical clocks remain open. |
| [5. Load hypothesis](05_load_balance.md) | Exact backend changes and extra host work leave all states/clicks unchanged. A local reversible control fails monotone equalization. |
| [6. Current issue handoffs](06_live_handoffs.md) | Preserves published source pins and distinguishes newer reported completion/geodesic results awaiting publication. |
| [7. Constructive common-field route](07_variational_bridge.md) | Massive Hamilton–Jacobi phase can jointly produce timelike motion and proper phase under a controlled semiclassical limit; proposes an actual packet experiment. |
| [8. Independent review](08_review.md) | Independent Rindler pullback, all de Sitter curvature components, rank tests and nonmetric impostor control; all audit programs rerun. |

The eight reviewers ran in two waves because only six child agents can run
concurrently with the coordinator. Published earlier native-coordinate and
parity results are credited; their reproduction is not relabelled a discovery.

## Fresh executable evidence

| Audit | Result and scope |
| --- | --- |
| Generic algebra | 2,430 complete scalar-oracle triples and 2,380 parity-paired click rows; all carries, cubic face terms, old-a stages and rewinds. Maximum 4,838 bits. |
| Host workload | 128 steps on 27 nodes: 20,736 backend integer comparisons, 10,368 independent scalar comparisons, 256 complete click-transition comparisons. 64,000 extra host multiplications change no physical output; three rewinds pass. |
| Clock controls | Full Rindler curvature zero; de Sitter Ricci scalar 12H² with unit rest clocks; exact ten-sample reconstruction and two held-out rates. These are passive/continuum oracles. |
| Independent clock review | Rank ten, rank nine after any sample removal, 20 algebraic metrics, all 256 de Sitter components, nonmetric impostor rejected at held-out velocity by 9/12800. |
| Common kinetic cone | Symbolic `A³=|Bn|² A` for each matter block; nonorthogonal/oblique speed² 146 versus wrong-metric 14. This is continuum principal-part evidence. |
| Published45 rerun | 45 channels, 881 quadratic terms, 27 nodes, three actual updates; independent scalar equality and full rewind, maximum 77 bits. |

The node/clock/load controls are different fixtures, not components secretly
concatenated into a new 48-channel physical law. The common-cone check uses
the exact published proposal in an isolated checkout. The reference spacetime
calculations do not feed any Engine run.

## A precise answer to the load hypothesis

Host CPU work and integer representation are implementation costs. Current
evolution does not read them; the executed workload intervention changes
them while retaining identical trajectories and clicks. They therefore do
not cause gravitational clock dilation in the present implementation.

An **intrinsic** retained-state workload could be a different physical
hypothesis. It needs an explicit observable, encoding invariance, local
couplings and predictions. A scalar stationary rate determines too little:
directional spatial geometry and shift also matter. A scalar may encode more
through a proved encoding, but that would no longer be merely a clock rate.
Local conservation/reciprocal exchange is a more precise target than generic
load equalization; even it does not uniquely determine Einstein dynamics.

## Next experiment and acceptance boundary

Use existing massive scalar and Maxwell fields in the same pinned tensor.
First measure flat-space packet velocity, then an oblique packet on a slowly
varying Kasner background. Compare actual transported field center and phase
with geodesics and proper time independently reconstructed from **that run's
metric**. Fix calibration in flat space and refine space, time, packet scale
and seed quantization. Massive semiclassical and massless high-frequency
limits are different. Charged matter can follow a Lorentz force rather than
a geodesic. Retain all source constraints and bit costs.

This proposed packet experiment is **not_tested**. The projective cost may
block a resolved run. Operational retained clock readout, general Einstein
constraint propagation and convergence remain unestablished. The newer
reported `C_after=-7h²` failure and phase/proper-time mismatch in the live
handoffs must remain in downstream acceptance. No proof has been supplied
that the event board works exactly like Einstein for general data.

## Reproduce

From this checkout, with its declared Python dependencies installed:

```bash
git fetch origin 62202fdccdd9a40d5dbbec104de6f97d9587a999
git worktree add --detach ../einstein-node-pr50 62202fdccdd9a40d5dbbec104de6f97d9587a999
python -m validation.einstein_node_audit.node_algebra
python -m validation.einstein_node_audit.clock_geometry
python -m validation.einstein_node_audit.load_invariance
python -m validation.einstein_node_audit.principal_cones --source ../einstein-node-pr50
python -m validation.einstein_node_audit.independent_review
```

Raw evidence is committed under `runs/einstein-node/` and
`runs/einstein_node/node_algebra.json`; each audit records source hashes.
The new CI workflow repeats these programs and uploads their raw records.
Existing reliability CI remains responsible for the full repository suite.
The validation summary in this directory records the final local checks.

Coordination: [issue40](https://github.com/Closer24/Universe24/issues/40),
[issue41](https://github.com/Closer24/Universe24/issues/41).
