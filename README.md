# Universe24

[Repository](https://github.com/Closer24/Universe24)

Universe24 implements one execution path:

**complete integer seed + immutable local tensor → reversible Engine → passive records → independent verification**.

The same Rule3 updates every retained channel. Geometry, matter, clocks, apparatus, scheduling and workspace share a hard budget of **48 total channels per node**. Each channel retains all three integers `(a,b,r)`:

```text
ell, r_next = divmod(2*u + r, 6)
a_next = b
b_next = ell - a
```

All inputs read the complete old snapshot. The fixed integer polynomial has degree at most three, target-plus-one-physical-face support and an acyclic old-`a` dependency graph. No projection, reset, external solver or click callback advances the state. Arbitrary integer bit growth is reported; a channel limit is not a memory bound.

The software execution system is implemented and reviewed. Restricted sourced Einstein sectors are reproducible. **A single physical construction combining spatial gravity, operational detectors, repeated cosmological bursts and sustained complexity growth has not been established.** The research controls below keep their distinct tensors and domains; their successes cannot be pooled into that claim.

## Run and verify

From the repository checkout, install the research dependencies and run the integrated acceptance entry point into a new directory:

```bash
python -m pip install '.[validation]'
python -m universe24 status
python -m validation.system_acceptance --out runs/system-acceptance
```

Read `runs/system-acceptance/acceptance.json`. The command creates fresh saved experiments, replays complete states and canonical clicks, rejects mixed-run evidence, and records accepted, rejected and blocked ideas. A successful command means the evidence and expected negative controls reproduced. Its joint physical gate remains explicit.

The installed interface is always `python -m universe24`. To execute your own complete prepared input:

```bash
python -m universe24 prepare   --tensor tensor.json --seed seed.json --channels channels.json   --protocol protocol.json --model model.json --out runs/input
python -m universe24 run --bundle runs/input --steps 12 --out runs/output
python -m universe24 verify --run runs/output
```

Use new output directories. Preparation validates and seals the inputs; it cannot invent a physical model or certify an equation. `verify --require-physics` deliberately rejects a general physical acceptance claim while its gates remain unresolved.

A bundle binds tensor, full seed, ownership, protocol and interpretation by hashes. A run saves its input bundle, full transitions, canonical records and validation. Replay checks every transition, inverse and emitted record. Stored traces are evidence, never extra evolving state.

## What is integrated

| Construction | Verified result | Boundary |
| --- | --- | --- |
| Native massless scalar + dust, six channels | Exact sourced expanding homogeneous FLRW flow, complete-history constraint, positive declared chart and independent Einstein-component checks | No mass term, spatial modes, detector or cosmological bounce |
| Native anisotropic massless scalar + dust, eight channels | Exact diagonal Bianchi I source, shear charges and source-based comoving proper-time invariant; independent metric and passive geodesic checks | Homogeneous only; passive moving probes; no retained detector or spatial momentum closure |
| Massive scalar + dust spinor coordinates, six channels | Exact decoded constraint, correct source pushforward and finite-time first-order convergence on a stated preparation family | Exponential integer cost; nonzero finite-step dust drift; no spatial detector |
| Generic interaction compiler | One local potential produces all declared reciprocal forces; counted native composition executes through the same Engine | Separate compiler controls do not implement the full gravity model |
| Full45 to six-channel symmetry restriction | Exact guarded reconstruction of both histories and all carries | Only the declared homogeneous neutral sector; the old massive45 constraint defect remains |
| Retained selection and record feedback | Local memory can change future carrier trajectories and phase | Record stress, bounded interaction energy and general spatial source closure remain incomplete |
| Repeated activity and structural growth | Exhaustive finite-sector recurrence and a fixed growth criterion are checked independently | Recurring activity is not a cosmological bang; sustained growth is not established |
| Quantum controls | Complete-trial, non-detection, preparation-measure and locality countercontrols | No derived universal Born rule or physical Bell instrument |

The anisotropic extension retains two shear charges in eight channels; its exact metric and source share the complete state. A 4,096-update check passed independent scalar comparisons, inverse and full rewind with 26-bit peak integers. Its moving-probe paths and proper-time integrals are passive diagnostics, with no retained transported body. A same-tensor spatial negative preserves pointwise Hamiltonian constraints but fails the momentum constraint.

The native massless experiment has also passed 16,384 actual updates and full rewind with 30-bit peak integers. This efficient result belongs to its linear native volume law. It does not transfer to the massive projective spinor law, whose three-resolution checks reach 207, 649 and 6101 bits.

For the expanding native massless scalar/dust source, density decreases and the scale factor decelerates. Repeated homogeneous density bursts are incompatible with that declared source. The finite Boolean selector instead has recurrent activity, but its closed cycles exclude indefinite strict increase of a state-defined complexity score. These are two explicit limits, not a joint burst-growth solution.

## Inspect the saved geodesic board

```bash
python -m validation.geodesic_board --out runs/geodesic-board
python -m universe24 verify --run runs/geodesic-board/runtime
```

Open `runs/geodesic-board/board.html`. This retained **massive45 negative-control board** shows passive null/timelike paths, source diagnostics and the signed Einstein residual from one saved run. It visibly retains the first-step defect `-7*dt**2`; it is not the newly constrained six-channel solution, a transported material probe or a default accepted universe. Playback never evolves a second system.

## Architecture and source map

| Path | Responsibility |
| --- | --- |
| `universe24/core/` | Fixed tensor, lattice, exact state and Rule3 Engine |
| `universe24/system/bundle.py` | Complete inputs, budget, strict locality and integrity |
| `universe24/system/runtime.py` | The sole run/replay/verify implementation |
| `universe24/system/decoder.py` | Canonical passive arithmetic records |
| `universe24/runtime.py` | Installed prepare/run/verify/status commands |
| `validation/system_acceptance/` | Source-only integrated evidence checks; no model selector |
| `validation/` | Independent research constructions and falsification controls, excluded from installation |

The architecture review is `docs/research/system_acceptance/architecture_review.md`. The complete idea decisions are in `docs/research/system_acceptance/idea_ledger.md`; the physical and massive-encoding boundaries are beside it. Current algebra is `docs/MODEL.md`, the execution contract is `docs/ONE_SYSTEM.md`, and source provenance is in `docs/research/central_integration/README.md`. Historical evidence retains its original source pin and is not relabeled as current validation.

```bash
python -m unittest discover -s universe24/tests -t . -v
python -m validation.system_smoke --out runs/new-smoke
python -m universe24 verify --run runs/new-smoke/run
```

A regression test may pass by reproducing a failed physical hypothesis. The corresponding physical result stays failed. No research label, channel name or successful replay can promote it.

## Local carrier–record interaction with a spatial source chart

The [local unification package](docs/research/local_unification/README.md)
constructs bounded, conservative record–carrier scattering and a twelve-channel
source-dependent extension through the same saved-bundle runtime:

```bash
python -m validation.local_unification.run_all --out runs/local-unification
python -m universe24 verify --run runs/local-unification/geometry/runtime
```

The declared preparation supports repeated encounters without resetting records.
Independent current, recoil, complete-history and source tests inspect the same
run. A cubic-spline readout gives an exact two-null-stream Einstein solution on
a proved finite causal interior. Nonphysical periodic-seam defects are retained
and exposed; the whole periodic board is not certified as an Einstein universe.

This construction does not establish localized massive bodies, operational
proper clocks, sustained complexity growth or a new production default.
See the linked construction report and its PR for
the actual source-pinned validation outcome.
